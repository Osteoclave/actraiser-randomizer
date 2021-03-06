#!/usr/bin/env python3
#
# ActRaiser Randomizer for Professional Mode
# Osteoclave
# 2019-10-19

import argparse
import random
import struct



parser = argparse.ArgumentParser(
    description = "ActRaiser Randomizer for Professional Mode"
)
parser.add_argument(
    "-s", "--seed",
    type = int,
    help = "specify the RNG seed value"
)
parser.add_argument(
    "-v", "--verbose",
    action = "count",
    help = "print spoiler log"
)
parser.add_argument(
    "-n", "--dry-run",
    action = "store_true",
    help = "execute without saving any changes"
)
parser.add_argument(
    "-B", "--boss-rush-last",
    action = "store_true",
    help = "keep the boss rush at the end"
)
forcePathGroup = parser.add_mutually_exclusive_group()
forcePathGroup.add_argument(
    "-L", "--left-path",
    action = "store_const",
    const = "left",
    dest = "force_path",
    help = "use the left path in Marahna II"
)
forcePathGroup.add_argument(
    "-R", "--right-path",
    action = "store_const",
    const = "right",
    dest = "force_path",
    help = "use the right path in Marahna II"
)
parser.add_argument(
    "-T", "--tanzra-last",
    action = "store_true",
    help = "fight Tanzra last in the boss rush"
)
# This option should be named "input-file". It isn't because of a bug with
# dash-to-underscore replacement for positional arguments:
# https://bugs.python.org/issue15125
# Workaround: Name the option "input_file" so we can use "args.input_file"
# to get its value, and set "metavar" so the name appears as "input-file"
# in help messages.
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

randomizerFlags = ""
if args.boss_rush_last:
    randomizerFlags += "B"
if args.force_path == "left":
    randomizerFlags += "L"
elif args.force_path == "right":
    randomizerFlags += "R"
if args.tanzra_last:
    randomizerFlags += "T"



rng = random.Random()
seed = args.seed
if seed is None:
    seed = random.SystemRandom().getrandbits(32)
seed %= 2**32

print("RNG seed: {}".format(seed))
print("Randomizer flags: {}".format((randomizerFlags if randomizerFlags else "-")))
rng.seed(seed)

# Always do the coin flip, even if we're going to override the result.
# This way, the shuffled map order for a given seed will stay the same, even
# if the chosen force-path option (left, right or unspecified) changes.
marahnaCoinFlip = rng.choice(["left", "right"])
marahnaPath = (args.force_path if args.force_path else marahnaCoinFlip)

# Shuffle the maps.
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
bossRushIndex = rng.randint(0, len(mapNumbers))
if args.boss_rush_last:
    bossRushIndex = len(mapNumbers)
mapNumbers.insert(bossRushIndex, 0x701)

# Shuffle the boss rush.
bossRush = [0x702, 0x703, 0x704, 0x705, 0x706, 0x707,]
rng.shuffle(bossRush)
tanzraIndex = rng.randint(0, len(bossRush))
if args.tanzra_last:
    tanzraIndex = len(bossRush)
bossRush.insert(tanzraIndex, 0x708)

# If we're in verbose mode, print the spoiler log.
if args.verbose:
    print("Marahna II path: {}".format(marahnaPath))
    spoilerLog = list(mapNumbers)
    spoilerLog[bossRushIndex:bossRushIndex] = bossRush
    for i, mapNumber in enumerate(spoilerLog, 1):
        print("{:3X} ".format(mapNumber), end="")
        if i % 10 == 0:
            print()
    print()

# Add the end credits as the last map.
mapNumbers.append(0x801)

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
    if randomizerFlags:
        menuString += "-{}".format(randomizerFlags)
    menuBytes = menuString.center(32).encode("ascii")
    struct.pack_into("{}s".format(len(menuBytes) + 1), romBytes, 0x129A7, menuBytes)

    # Always enter Professional Mode from the initial menu.
    romBytes[0x40] = 0xEA
    romBytes[0x41] = 0xEA

    # In the event of player death, respawn on the same map.
    romBytes[0x13D61] = 0xEA
    romBytes[0x13D62] = 0xEA
    romBytes[0x13D63] = 0xA5
    romBytes[0x13D64] = 0x19

    # Add a room counter to the HUD.
    # You can't get or use magic in Professional Mode, so this feature
    # repurposes storage and memory normally used by magic.

    # Replace the code that draws a scroll for each MP you have (always zero
    # in Professional Mode) with code to display the room counter.
    romBytes[0x142C8] = 0xE2 # SEP #$20
    romBytes[0x142C9] = 0x20
    romBytes[0x142CA] = 0xA5 # LDA $21
    romBytes[0x142CB] = 0x21
    romBytes[0x142CC] = 0x4A # LSR
    romBytes[0x142CD] = 0x4A # LSR
    romBytes[0x142CE] = 0x4A # LSR
    romBytes[0x142CF] = 0x4A # LSR
    romBytes[0x142D0] = 0x09 # ORA #$30
    romBytes[0x142D1] = 0x30
    romBytes[0x142D2] = 0x8F # STA $7FB046
    romBytes[0x142D3] = 0x46
    romBytes[0x142D4] = 0xB0
    romBytes[0x142D5] = 0x7F
    romBytes[0x142D6] = 0xA5 # LDA $21
    romBytes[0x142D7] = 0x21
    romBytes[0x142D8] = 0x29 # AND #$0F
    romBytes[0x142D9] = 0x0F
    romBytes[0x142DA] = 0x09 # ORA #$30
    romBytes[0x142DB] = 0x30
    romBytes[0x142DC] = 0x8F # STA $7FB048
    romBytes[0x142DD] = 0x48
    romBytes[0x142DE] = 0xB0
    romBytes[0x142DF] = 0x7F
    romBytes[0x142E0] = 0xEA # NOP
    romBytes[0x142E1] = 0xEA # NOP
    romBytes[0x142E2] = 0xEA # NOP
    romBytes[0x142E3] = 0xEA # NOP
    romBytes[0x142E4] = 0xEA # NOP
    romBytes[0x142E5] = 0xEA # NOP
    romBytes[0x142E6] = 0xEA # NOP
    romBytes[0x142E7] = 0xEA # NOP

    # Update the HUD's fixed content to replace "[ACT]" with the person icon
    # and two reserved spaces for the room counter's digits.
    struct.pack_into("<H", romBytes, 0x10E7E, 0x0000)
    struct.pack_into("<H", romBytes, 0x10E80, 0x003A)
    struct.pack_into("<H", romBytes, 0x10E82, 0x003B)
    struct.pack_into("<H", romBytes, 0x10E84, 0x0030)
    struct.pack_into("<H", romBytes, 0x10E86, 0x0030)
    struct.pack_into("<H", romBytes, 0x10E88, 0x0000)

    # Update the HUD's fixed content to not show ten MP scrolls.
    # For some reason, the fixed content has the variable fields filled in
    # (mostly with zeroes, but for MP, with ten scroll icons). Without the
    # scroll-drawing code, there's nothing to erase them, so let's remove
    # them here.
    for offset in range(0x10EE8, 0x10EFC, 0x2):
        struct.pack_into("<H", romBytes, offset, 0x0000)

    # Update the map-changing function to increment the room counter.
    # There's not enough space in the map-changing function for all of the
    # new code, so let's put in a subroutine call to some unused space...
    romBytes[0x26C] = 0x22 # JSL $00FF40
    romBytes[0x26D] = 0x40
    romBytes[0x26E] = 0xFF
    romBytes[0x26F] = 0x00
    # ...and write the new code into that unused space.
    # If the map change is happening because of player death, don't advance
    # the room counter.
    romBytes[0x7F40] = 0xAD # LDA $032C
    romBytes[0x7F41] = 0x2C
    romBytes[0x7F42] = 0x03
    romBytes[0x7F43] = 0xD0 # BNE $7F60
    romBytes[0x7F44] = 0x1B
    # If the current map is the Death Heim hub (0x701), and the destination
    # map is one of the Death Heim boss rooms (0x7##), don't advance the
    # room counter.
    romBytes[0x7F45] = 0xA5 # LDA $18
    romBytes[0x7F46] = 0x18
    romBytes[0x7F47] = 0xC9 # CMP #$07
    romBytes[0x7F48] = 0x07
    romBytes[0x7F49] = 0xD0 # BNE $7F57
    romBytes[0x7F4A] = 0x0C
    romBytes[0x7F4B] = 0xA5 # LDA $19
    romBytes[0x7F4C] = 0x19
    romBytes[0x7F4D] = 0xC9 # CMP #$01
    romBytes[0x7F4E] = 0x01
    romBytes[0x7F4F] = 0xD0 # BNE $7F57
    romBytes[0x7F50] = 0x06
    romBytes[0x7F51] = 0xA5 # LDA $1B
    romBytes[0x7F52] = 0x1B
    romBytes[0x7F53] = 0xC9 # CMP #$07
    romBytes[0x7F54] = 0x07
    romBytes[0x7F55] = 0xF0 # BEQ $7F60
    romBytes[0x7F56] = 0x09
    # Advance the room counter.
    romBytes[0x7F57] = 0xF8 # SED
    romBytes[0x7F58] = 0xA5 # LDA $21
    romBytes[0x7F59] = 0x21
    romBytes[0x7F5A] = 0x18 # CLC
    romBytes[0x7F5B] = 0x69 # ADC #$01
    romBytes[0x7F5C] = 0x01
    romBytes[0x7F5D] = 0x85 # STA $21
    romBytes[0x7F5E] = 0x21
    romBytes[0x7F5F] = 0xD8 # CLD
    # Do the instructions that were overwritten by the subroutine call.
    romBytes[0x7F60] = 0xA5 # LDA $1A
    romBytes[0x7F61] = 0x1A
    romBytes[0x7F62] = 0x85 # STA $19
    romBytes[0x7F63] = 0x19
    # Return.
    romBytes[0x7F64] = 0x6B # RTL

    # Skip the "descending ball of light brings statue to life" animation.
    # On some maps, it causes the player to take unavoidable damage.
    romBytes[0x12B0D] = 0x9C

    # Make both exits from Marahna II.b go to the same destination map.
    romBytes[0x6702] = 0xEA

    # Prevent animated tiles from glitching.
    # Not sure exactly why the glitching occurs, but this change fixes it.
    for offset in range(0x1093E + 0x18, 0x10E7E, 0x1C):
        romBytes[offset] &= 0x7F

    # Prepare to update the "next map" values.
    nextMapOffsets = {
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
        0x701 : None,
    }

    # Specify which map to load first.
    # The map number at 0x11013 seems to be ignored in favour of 0x12B1C, but
    # the following map numbers (0x11015 onward) do get used, so I'm updating
    # 0x11013 as well for consistency.
    struct.pack_into("<H", romBytes, 0x12B1C, mapNumbers[0])
    struct.pack_into(">H", romBytes, 0x11013, mapNumbers[0])
    professionalModeOffset = 0x11015

    # Update the "next map" values.
    for i in range(len(mapNumbers) - 1):
        mapNumber = mapNumbers[i]
        nextMapNumber = mapNumbers[i+1]

        if nextMapOffsets[mapNumber]:
            struct.pack_into("<H", romBytes, nextMapOffsets[mapNumber], nextMapNumber)
        else:
            struct.pack_into(">H", romBytes, professionalModeOffset, nextMapNumber)
            professionalModeOffset += 2

    # Update the boss rush.
    # After defeating a boss, take away the sword upgrade (so you don't keep
    # it after fighting Tanzra), and advance the boss rush counter by adding
    # one (instead of setting it based on the boss room's map number).
    romBytes[0x7EEC] = 0xE2 # SEP #$20
    romBytes[0x7EED] = 0x20
    romBytes[0x7EEE] = 0x64 # STZ $E4
    romBytes[0x7EEF] = 0xE4
    romBytes[0x7EF0] = 0xC2 # REP #$20
    romBytes[0x7EF1] = 0x20
    romBytes[0x7EF2] = 0xEE # INC $0347
    romBytes[0x7EF3] = 0x47
    romBytes[0x7EF4] = 0x03

    # Write the new boss rush order to some unused space.
    for i, boss in enumerate(bossRush):
        struct.pack_into("<H", romBytes, 0x7F80 + (i*2), boss)

    # Use the new boss rush order.
    romBytes[0x73E2] = 0xDA # PHX
    romBytes[0x73E3] = 0xAD # LDA $0347
    romBytes[0x73E4] = 0x47
    romBytes[0x73E5] = 0x03
    romBytes[0x73E6] = 0x0A # ASL
    romBytes[0x73E7] = 0xAA # TAX
    romBytes[0x73E8] = 0xBD # LDA $FF80,X
    romBytes[0x73E9] = 0x80
    romBytes[0x73EA] = 0xFF
    romBytes[0x73EB] = 0x85 # STA $1A
    romBytes[0x73EC] = 0x1A
    romBytes[0x73ED] = 0xFA # PLX
    romBytes[0x73EE] = 0xEA # NOP
    romBytes[0x73EF] = 0xEA # NOP

    # Update the order of faces in the Death Heim hub.
    bossRushFaces = {
        0x702 : bytes.fromhex("01 09 00 0C 01 09 00 0F"),
        0x703 : bytes.fromhex("0F 09 00 0D 0F 09 00 10"),
        0x704 : bytes.fromhex("03 08 00 0C 03 08 00 0F"),
        0x705 : bytes.fromhex("0C 08 00 16 0D 08 00 10"),
        0x706 : bytes.fromhex("05 07 00 0C 05 07 00 0F"),
        0x707 : bytes.fromhex("0B 07 00 0D 0B 07 00 10"),
        0x708 : bytes.fromhex("08 07 00 0E 08 05 00 11"),
    }
    for i, boss in enumerate(bossRush):
        faceOffset = 0x54432 + (i*8)
        romBytes[faceOffset:faceOffset+8] = bossRushFaces[boss]

    # The unmodified code uses a loop to control the eyes and gems of the
    # first six faces, with Tanzra's eyes and gem working separately. Let's
    # simplify things by making Tanzra's face work like the others.
    # First, Tanzra's eyes...
    romBytes[0x7467] = 0xBD # LDA $0038,X
    romBytes[0x7468] = 0x38
    romBytes[0x7469] = 0x00
    romBytes[0x746A] = 0xF0 # BEQ $F482
    romBytes[0x746B] = 0x16
    romBytes[0x746C] = 0x30 # BMI $F47C
    romBytes[0x746D] = 0x0E
    romBytes[0x746E] = 0xEA # NOP
    romBytes[0x746F] = 0xEA # NOP
    romBytes[0x7470] = 0xEA # NOP
    romBytes[0x7471] = 0xEA # NOP
    romBytes[0x7472] = 0xEA # NOP
    romBytes[0x7473] = 0xEA # NOP
    # ...then Tanzra's gem.
    romBytes[0x74CB] = 0xBD # LDA $0038,X
    romBytes[0x74CC] = 0x38
    romBytes[0x74CD] = 0x00
    romBytes[0x74CE] = 0x10 # BPL $F4DF
    romBytes[0x74CF] = 0x0F
    romBytes[0x74D0] = 0xEA # NOP
    romBytes[0x74D1] = 0xEA # NOP
    romBytes[0x74D2] = 0xEA # NOP

    # Change the conditions that break the loop.
    # Wait until after we've dimmed the eyes and shattered the gem of the
    # current face to try breaking the loop.
    romBytes[0x7558] = 0xEA
    romBytes[0x7559] = 0xEA
    romBytes[0x755A] = 0xEA
    romBytes[0x755B] = 0xEA
    romBytes[0x755C] = 0xEA
    # Break the loop if all of the bosses have been defeated.
    romBytes[0x7581] = 0x07
    romBytes[0x7584] = 0x24

    # Write the output file.
    outFileName = args.output_file
    if outFileName is None:
        suffix = "_{}".format(seed)
        if randomizerFlags:
            suffix += "_{}".format(randomizerFlags)

        basename, dot, extension = inFileName.rpartition(".")
        if basename and extension:
            basename += suffix
        else:
            extension += suffix
        outFileName = basename + dot + extension

    with open(outFileName, "xb") as outFile:
        outFile.write(romBytes)
