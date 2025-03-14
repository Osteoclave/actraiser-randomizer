"use strict";

self.importScripts("https://cdn.jsdelivr.net/pyodide/v0.27.3/full/pyodide.js");

async function loadPyodideAndFiles() {
  self.pyodide = await loadPyodide();

  async function fetchFile(fileName) {
    const response = await fetch(fileName);
    if (!response.ok) {
      throw new Error(`Could not fetch '${fileName}'. HTTP response status code: ${response.status}`);
    }
    const fileBuffer = await response.arrayBuffer();
    const fileBytes = new Uint8Array(fileBuffer);
    self.pyodide.FS.writeFile(fileName, fileBytes);
  }

  await fetchFile("actraiser_randomizer.py");
}
const pyodideReadyPromise = loadPyodideAndFiles();



async function runRandomizer(event) {
  await pyodideReadyPromise;

  const randomizerArgs = event.data;
  const romBytes = randomizerArgs.get("romBytes");
  const isRaceSeed = randomizerArgs.get("isRaceSeed");
  const seed = randomizerArgs.get("seed");
  const initialLives = randomizerArgs.get("initialLives");
  const zantetsuken = randomizerArgs.get("zantetsuken");
  const marahnaPath = randomizerArgs.get("marahnaPath");
  const bossRushType = randomizerArgs.get("bossRushType");

  pyodide.globals.set("romBytes", pyodide.toPy(romBytes));
  pyodide.globals.set("isRaceSeed", pyodide.toPy(isRaceSeed));
  pyodide.globals.set("seed", pyodide.toPy(seed));
  pyodide.globals.set("initialLives", pyodide.toPy(initialLives));
  pyodide.globals.set("zantetsuken", pyodide.toPy(zantetsuken));
  pyodide.globals.set("marahnaPath", pyodide.toPy(marahnaPath));
  pyodide.globals.set("bossRushType", pyodide.toPy(bossRushType));

  const pythonCode = `
import actraiser_randomizer

flagString = actraiser_randomizer.getFlagString(
    initialLives,
    zantetsuken,
    marahnaPath,
    bossRushType,
)

# Generate the seed.
(
    romByteArray,
    mapNumbers,
    chosenMarahnaPath,
    chosenBossRushType,
) = actraiser_randomizer.generate(
    romBytes,
    isRaceSeed,
    seed,
    initialLives,
    zantetsuken,
    marahnaPath,
    bossRushType,
)

hashString = actraiser_randomizer.getHashString(mapNumbers)

# Construct the output filename.
basename = "actraiser"
basename += f"_{'RACE' if isRaceSeed else seed}"
if flagString:
    basename += f"_{flagString}"
if isRaceSeed:
    basename += f"_{hashString}"

romFileName = f"{basename}.sfc"
`
  pyodide.runPython(pythonCode);

  const romByteArray = pyodide.globals.get("romByteArray").toJs();
  const romFileName = pyodide.globals.get("romFileName");
  const generatedSeed = new Map();
  generatedSeed.set("romByteArray", romByteArray);
  generatedSeed.set("romFileName", romFileName);
  self.postMessage(generatedSeed, [romByteArray.buffer]);
}
self.addEventListener("message", runRandomizer);
