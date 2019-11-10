#!/usr/bin/env python3
#
# ActRaiser Randomizer for Professional Mode
# Osteoclave
# 2019-10-19

import argparse
import random
import struct



exits = {
    0x101 : None,
    0x102 : 0x3031,
    0x103 : 0x303C,
    0x104 : None,
    0x201 : None,
    0x202 : 0x392C,
    0x203 : 0x393A,
    0x204 : 0x3948,
    0x205 : 0x3956,
    0x206 : 0x3964,
    0x207 : 0x3972,
    0x208 : None,
    0x301 : 0x415F,
    0x302 : None,
    0x303 : 0x416D,
    0x304 : 0x4187,
    0x305 : 0x419D,
    0x306 : None,
    0x401 : 0x4DEC,
    0x402 : 0x4DFA,
    0x403 : None,
    0x404 : 0x4E10,
    0x405 : 0x4E1E,
    0x406 : 0x4E34,
    0x407 : None,
    0x501 : 0x66C7,
    0x502 : 0x66D5,
    0x503 : None,
    0x504 : 0x66EB,
    0x505 : 0x66F9,
    0x506 : 0x671D,
    0x507 : 0x671D,
    0x508 : None,
    0x601 : 0x6767,
    0x602 : 0x6775,
    0x603 : 0x678B,
    0x604 : None,
    0x605 : 0x67A1,
    0x606 : 0x67AC,
    0x607 : 0x67B7,
    0x608 : None,
}



parser = argparse.ArgumentParser(
    description = "ActRaiser Randomizer for Professional Mode"
)
parser.add_argument(
    "-s", "--seed",
    type = int,
    help = "specify the RNG seed value"
)
forcePathGroup = parser.add_mutually_exclusive_group()
forcePathGroup.add_argument(
    "--force-left",
    action = "store_const",
    const = "left",
    dest = "force_path",
    help = "use the left path in Marahna II"
)
forcePathGroup.add_argument(
    "--force-right",
    action = "store_const",
    const = "right",
    dest = "force_path",
    help = "use the right path in Marahna II"
)
parser.add_argument(
    "-n", "--dry-run",
    action = "store_true",
    help = "execute without saving any changes"
)
parser.add_argument(
    "-v", "--verbose",
    action = "count",
    help = "print spoiler log"
)
# This option should be named "input-file". It isn't because of a bug with
# dash-to-underscore replacement for positional arguments:
# https://bugs.python.org/issue15125
# Solution: Name the option "input_file" so we can use "args.input_file" to
# get its value, and set "metavar" so the name appears as "input-file" in
# help messages.
parser.add_argument(
    "input_file",
    metavar = "input-file",
    nargs = "?",
    help = "input file name: an 'ActRaiser (USA)' ROM"
)
parser.add_argument(
    "-o", "--output-file",
    type = str,
    help = "output file name"
)
args = parser.parse_args()



if args.input_file is None and not args.dry_run:
    parser.error("Argument 'input-file' is required when not in dry-run mode")

rng = random.Random()
seed = args.seed
if seed is None:
    seed = random.SystemRandom().getrandbits(32)
seed %= 2**32

print("RNG seed: {}".format(seed))
rng.seed(seed)

# Always do the coin flip, even if we're going to override the result.
# This way, the shuffled map order for a given seed will stay the same, even
# if the chosen force-path option (left, right or unspecified) changes.
marahnaCoinFlip = rng.choice(["left", "right"])
if args.force_path:
    if args.verbose:
        print("Marahna II path: {}".format(marahnaCoinFlip))
    marahnaPath = args.force_path
    print("Marahna II path: {} (forced by command-line option)".format(marahnaPath))
else:
    marahnaPath = marahnaCoinFlip
    if args.verbose:
        print("Marahna II path: {}".format(marahnaPath))

mapNumbers = [
    0x101,
    0x102, 0x103, 0x104,
    0x201,
    0x202, 0x203, 0x204, 0x205, 0x206, 0x207, 0x208,
    0x301, 0x302,
    0x303, 0x304, 0x305, 0x306,
    0x401, 0x402, 0x403,
    0x404, 0x405, 0x406, 0x407,
    0x501, 0x502, 0x503,
    0x504, 0x505, (0x506 if marahnaPath == "left" else 0x507), 0x508,
    0x601, 0x602, 0x603, 0x604,
    0x605, 0x606, 0x607, 0x608,
]
rng.shuffle(mapNumbers)
mapNumbers.append(0x701)

# If we're in verbose mode, print the spoiler log.
if args.verbose:
    for mapNumber in mapNumbers:
        print("{:3X} ".format(mapNumber), end="")
    print()

if not args.dry_run:
    # Read the input file.
    inFileName = args.input_file
    with open(inFileName, "rb") as inFile:
        romBytes = bytearray(inFile.read())

    # Sanity-check the input file.
    if len(romBytes) != 1048576:
        raise ValueError("Input file '{}' is not 1048576 bytes in size".format(inFileName))
    romName = bytes(romBytes[0x7FC0:0x7FD5])
    actName = b"ACTRAISER-USA        "
    if romName != actName:
        raise ValueError("Unexpected internal ROM name: {} # Expected: {}".format(romName, actName))

    # Write the extended map metadata to 0xF8000.
    with open("actraiser_map_metadata_extended.hex", "rb") as f:
        metadata = f.read()
    romBytes[0xF8000:0xF8000 + len(metadata)] = metadata
    # Look for map metadata at 0xF8000 instead of 0x28000.
    romBytes[0x13E29] = 0x1F

    # Make the initial menu only have "START" as an option.
    romBytes[0x1270D] = 0xEA
    romBytes[0x1270E] = 0xEA
    # Print the menu option starting at the left side of the screen.
    romBytes[0x12712] = 0x00
    # We need more space than the "START" option text provides, so we'll
    # repurpose the space used by the "CONTINUE" / "NEW GAME" option text.
    struct.pack_into("<H", romBytes, 0x12715, 0xA9A7)
    menuString = "> START < {}".format(seed)
    if args.force_path == "left":
        menuString += "-L"
    elif args.force_path == "right":
        menuString += "-R"
    menuBytes = menuString.center(32).encode("ascii")
    struct.pack_into("{}s".format(len(menuBytes) + 1), romBytes, 0x129A7, menuBytes)

    # Always enter Professional Mode from the initial menu.
    romBytes[0x40] = 0xEA
    romBytes[0x41] = 0xEA

    # Make both exits from Marahna II.b go to the same destination map.
    romBytes[0x6702] = 0xEA

    # In the event of player death, respawn on the same map.
    romBytes[0x13D61] = 0xEA
    romBytes[0x13D62] = 0xEA
    romBytes[0x13D63] = 0xA5
    romBytes[0x13D64] = 0x19

    # Prevent animated tiles from glitching.
    # Not sure exactly why the glitching occurs, but this change fixes it.
    for offset in range(0x1093E + 0x18, 0x10E7E, 0x1C):
        romBytes[offset] &= 0x7F

    # Specify which map to load first.
    # The map number at 0x11013 seems to be ignored in favour of 0x12B1C, but
    # the following map numbers (0x11015 onward) do get used, so I'm updating
    # 0x11013 as well for consistency.
    struct.pack_into("<H", romBytes, 0x12B1C, mapNumbers[0])
    struct.pack_into(">H", romBytes, 0x11013, mapNumbers[0])
    professionalModeOffset = 0x11015

    # Update the exit destinations.
    for i in range(len(mapNumbers) - 1):
        mapNumber = mapNumbers[i]
        nextMapNumber = mapNumbers[i+1]

        if exits[mapNumber]:
            struct.pack_into("<H", romBytes, exits[mapNumber], nextMapNumber)
        else:
            struct.pack_into(">H", romBytes, professionalModeOffset, nextMapNumber)
            professionalModeOffset += 2

    # Write the output file.
    outFileName = args.output_file
    if outFileName is None:
        suffix = "_{}".format(seed)
        if args.force_path == "left":
            suffix += "_L"
        elif args.force_path == "right":
            suffix += "_R"

        basename, dot, extension = inFileName.rpartition(".")
        if basename and extension:
            basename += suffix
        else:
            extension += suffix
        outFileName = basename + dot + extension

    with open(outFileName, "xb") as outFile:
        outFile.write(romBytes)
