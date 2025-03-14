"use strict";

let worker = null;

const storageWrapper = {
  keyNamePrefix: "actraiser_randomizer",
  storageBackend: window.localStorage,
  getItem(keyName) {
    return this.storageBackend.getItem(`${this.keyNamePrefix}___${keyName}`);
  },
  setItem(keyName, keyValue) {
    return this.storageBackend.setItem(`${this.keyNamePrefix}___${keyName}`, keyValue);
  },
  removeItem(keyName) {
    return this.storageBackend.removeItem(`${this.keyNamePrefix}___${keyName}`);
  },
};



function bytesToBase64(bytes) {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" + "=";
  const PADDING_INDEX = alphabet.length - 1;
  const base64 = new Array(4 * Math.ceil(bytes.length / 3));

  // With each pass of the loop, process three bytes of input
  for (let i = 0; 3*i < bytes.length; i++) {
    // 1st input byte
    base64[4*i + 0] = (bytes[3*i + 0] & 0b11111100) >> 2;
    base64[4*i + 1] = (bytes[3*i + 0] & 0b00000011) << 4;
    // 2nd input byte
    if (3*i + 1 < bytes.length) {
      base64[4*i + 1] |= (bytes[3*i + 1] & 0b11110000) >> 4;
      base64[4*i + 2]  = (bytes[3*i + 1] & 0b00001111) << 2;
    } else {
      base64[4*i + 2]  = PADDING_INDEX;
    }
    // 3rd input byte
    if (3*i + 2 < bytes.length) {
      base64[4*i + 2] |= (bytes[3*i + 2] & 0b11000000) >> 6;
      base64[4*i + 3]  = (bytes[3*i + 2] & 0b00111111);
    } else {
      base64[4*i + 3]  = PADDING_INDEX;
    }
    // Convert the four output values to Base64 characters
    base64[4*i + 0] = alphabet[base64[4*i + 0]];
    base64[4*i + 1] = alphabet[base64[4*i + 1]];
    base64[4*i + 2] = alphabet[base64[4*i + 2]];
    base64[4*i + 3] = alphabet[base64[4*i + 3]];
  }

  return base64.join("");
}

function base64ToBytes(base64) {
  const binString = atob(base64);
  return Uint8Array.from(binString, (m) => m.codePointAt(0));
}



function isValidROM(romBytes) {
  // A valid ROM is 1,048,576 bytes long.
  if (romBytes.length !== 1048576) {
    return false;
  }
  // A valid ROM's internal name is "ACTRAISER-USA        ".
  // The internal name field is 21 bytes long, hence the trailing spaces.
  const romName = String.fromCharCode(...romBytes.slice(0x7FC0, 0x7FD5));
  const goodName = "ACTRAISER-USA        ";
  if (romName !== goodName) {
    return false;
  }
  // If a candidate ROM passes all of the tests, consider it valid.
  return true;
}



function updateStatusMessage(message = "", textClass = "") {
  const textClasses = ["text-success", "text-danger"];
  document.getElementById("statusIcon").classList.remove(...textClasses);

  if (textClass === "success") {
    document.getElementById("statusIcon").classList.add("text-success");
    document.getElementById("statusIcon").innerText = "\u2713"; // &check;
    document.getElementById("statusIcon").classList.remove("d-none");
  } else if (textClass === "danger") {
    document.getElementById("statusIcon").classList.add("text-danger");
    document.getElementById("statusIcon").innerText = "\u2717"; // &cross;
    document.getElementById("statusIcon").classList.remove("d-none");
  } else {
    document.getElementById("statusIcon").classList.add("d-none");
    document.getElementById("statusIcon").innerText = "";
  }

  document.getElementById("statusMessage").innerText = String(message);
}



function updateFileButton() {
  const buttonClasses = ["btn-success", "btn-danger", "btn-warning"];
  document.getElementById("fileButton").classList.remove(...buttonClasses);

  const romBase64 = storageWrapper.getItem("rom_base64");
  if (romBase64 !== null) {
    const romBytes = base64ToBytes(romBase64);
    if (isValidROM(romBytes)) {
      document.getElementById("fileButton").classList.add("btn-success");
      document.getElementById("fileButton").innerText = "Valid ROM selected";
      document.getElementById("generate").disabled = false;
    } else {
      document.getElementById("fileButton").classList.add("btn-danger");
      document.getElementById("fileButton").innerText = "Invalid ROM selected";
      document.getElementById("generate").disabled = true;
    }
  } else {
    document.getElementById("fileButton").classList.add("btn-warning");
    document.getElementById("fileButton").innerText = "No ROM selected";
    document.getElementById("generate").disabled = true;
  }
}



async function changeFileName(event) {
  updateStatusMessage();
  const fileList = document.getElementById("fileName").files;
  if (fileList.length > 0) {
    const fileObject = fileList.item(0);
    const fileBuffer = await fileObject.arrayBuffer();
    const fileBytes = new Uint8Array(fileBuffer);
    try {
      storageWrapper.setItem("rom_base64", bytesToBase64(fileBytes));
    } catch (e) {
      if (e instanceof DOMException && e.name === "QuotaExceededError") {
        storageWrapper.removeItem("rom_base64");
        updateStatusMessage("Could not store ROM: localStorage quota exceeded", "danger");
      } else {
        throw e;
      }
    }
    updateFileButton();
  }
}
document.getElementById("fileName").addEventListener("change", changeFileName);

document.getElementById("fileButton").addEventListener("click", function (event) {
  document.getElementById("fileName").click();
});



function clearFileName(event) {
  updateStatusMessage();
  storageWrapper.removeItem("rom_base64");
  updateFileButton();
}
document.getElementById("clearFileName").addEventListener("click", clearFileName);



function raceSeed(event) {
  updateStatusMessage();
  document.getElementById("seedCustomizer").classList.add("invisible");
}
document.getElementById("raceSeed").addEventListener("change", raceSeed);



function customSeed(event) {
  updateStatusMessage();
  document.getElementById("seedCustomizer").classList.remove("invisible");
}
document.getElementById("customSeed").addEventListener("change", customSeed);



function newSeed(event) {
  updateStatusMessage();
  document.getElementById("seed").value = Math.trunc(Math.random() * 2**32);
}
document.getElementById("newSeed").addEventListener("click", newSeed);



function generate(event) {
  // Verify that the stored ROM is OK
  updateStatusMessage();
  const romBase64 = storageWrapper.getItem("rom_base64");
  if (romBase64 === null) {
    updateStatusMessage("No ROM selected", "danger");
    return;
  }
  const romBytes = base64ToBytes(romBase64);
  if (!isValidROM(romBytes)) {
    updateStatusMessage("Invalid ROM selected", "danger");
    return;
  }

  // Verify that the provided seed is OK
  let seed = null;
  const isRaceSeed = document.getElementById("raceSeed").checked;
  if (!isRaceSeed) {
    const seedString = document.getElementById("seed").value.trim();
    const integerRegex = new RegExp("^[0-9]+$");
    if (!integerRegex.test(seedString)) {
      updateStatusMessage("Seed must be a number", "danger");
      return;
    }
    seed = parseInt(seedString, 10);
    if (seed === NaN) {
      updateStatusMessage("Seed must be a number", "danger");
      return;
    }
    seed %= 2**32
  }

  // Get the selected randomizer options
  let initialLives = null;
  const initialLivesString = document.getElementById("initialLives").value;
  if (["extra", "unlimited", "deathcount"].includes(initialLivesString)) {
    initialLives = initialLivesString;
  }
  const zantetsukenString = document.getElementById("zantetsuken").value;
  const zantetsuken = (zantetsukenString === "on");
  let marahnaPath = null;
  const marahnaPathString = document.getElementById("marahnaPath").value;
  if (["left", "right"].includes(marahnaPathString)) {
    marahnaPath = marahnaPathString;
  }
  let bossRushType = null;
  const bossRushTypeString = document.getElementById("bossRushType").value;
  if (["consecutive", "scattered"].includes(bossRushTypeString)) {
    bossRushType = bossRushTypeString;
  }

  // Enter "Generating..." mode
  document.getElementById("generate").disabled = true;
  document.getElementById("generateSpinner").classList.remove("d-none");
  document.getElementById("generateText").innerText = "Generating...";
  updateStatusMessage("Generation in progress, this may take some time...")

  // Send a message to the web worker to run the randomizer
  const randomizerArgs = new Map();
  randomizerArgs.set("romBytes", romBytes);
  randomizerArgs.set("isRaceSeed", isRaceSeed);
  randomizerArgs.set("seed", seed);
  randomizerArgs.set("initialLives", initialLives);
  randomizerArgs.set("zantetsuken", zantetsuken);
  randomizerArgs.set("marahnaPath", marahnaPath);
  randomizerArgs.set("bossRushType", bossRushType);
  worker.postMessage(randomizerArgs, [romBytes.buffer]);
}
document.getElementById("generate").addEventListener("click", generate);



function downloadSeed(event) {
  // Retrieve the generated seed
  const generatedSeed = event.data;
  const romByteArray = generatedSeed.get("romByteArray");
  const romFileName = generatedSeed.get("romFileName");

  // Prompt the user to download the generated seed
  const romBlob = new Blob([romByteArray], { type: "application/vnd.nintendo.snes.rom" });
  const romURL = window.URL.createObjectURL(romBlob);
  const downloadAnchor = document.createElement("a");
  downloadAnchor.setAttribute("href", romURL);
  downloadAnchor.setAttribute("download", romFileName);
  document.body.appendChild(downloadAnchor);
  downloadAnchor.click();
  document.body.removeChild(downloadAnchor);
  window.URL.revokeObjectURL(romURL);

  // Exit "Generating..." mode
  updateStatusMessage(`Generated '${romFileName}'`, "success");
  document.getElementById("generateText").innerText = "Generate";
  document.getElementById("generateSpinner").classList.add("d-none");
  document.getElementById("generate").disabled = false;
}



async function main() {
  worker = new Worker("web_worker.js");
  worker.addEventListener("message", downloadSeed);

  const fileName = "actraiser_randomizer.py"
  const response = await fetch(fileName);
  if (!response.ok) {
    throw new Error(`Could not fetch '${fileName}'. HTTP response status code: ${response.status}`);
  }
  const fileString = await response.text();
  const versionRegex = /^randomizerVersion = \"(.*)\"$/m;
  const versionMatch = versionRegex.exec(fileString);
  if (versionMatch !== null) {
    document.getElementById("version").innerText = versionMatch[1];
  }

  updateFileButton();
  document.getElementById("newSeed").click();
  updateStatusMessage();

  document.getElementById("loading").style.display = "none";
  document.getElementById("application").style.display = "block";
}
main();
