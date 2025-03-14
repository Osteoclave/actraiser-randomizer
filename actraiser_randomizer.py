#!/usr/bin/env python3
#
# ActRaiser Randomizer for Professional Mode
# Osteoclave
# 2019-10-19

import argparse
import hashlib
import itertools
import random
import struct
import textwrap



# Randomizer version: The current version's release date in YYYY-MM-DD format.
# Update this with each new release.
# Add a suffix (e.g. "/b", "/c") if there's more than one release in a day.
# Title screen space is limited, so don't use more than 15 characters.
randomizerVersion = "2025-03-14"



# Extended map metadata
# In vanilla, maps don't always load all of their required assets.
# For example, graphics data might only be loaded by the first room
# of an Act, with later rooms expecting it to already be there.
# This works with a fixed room order, but breaks when randomized.
# Solution: Make each map load all of its required assets.
extendedMapMetadata = bytes.fromhex(" ".join([
    # Map [53 59]
    "53 59",
    "00",
    # Map [00 00]
    # Title Screen
    "00 00",
    "08             01",
    "20 80 20 00 01 1A 88 0C",
    "20 80 20 00 04 1A 90 0C",
    "02 00 00       B8 14 0D",
    "40 00 80 00    93 3A 0E",
    "80 80 20 FF    00 83 05",
    "10 80          7D 8E 02",
    "80 00 08 50    FB EC 0B",
    "00",
    # Map [00 01]
    # Town of Fillmore
    "00 01",
    "08             02",
    "40 00 80 00    93 3B 0E",
    "20 80 20 00 01 1A 88 0C",
    "80 80 20 00    00 00 06",
    "80 80 20 00    00 40 06",
    "20 80 20 00 02 1A 98 0C",
    "20 80 20 00 04 1A 90 0C",
    "40 00 80 80    93 3C 0E",
    "80 80 20 20    00 80 06",
    "10 82          98 DE 0D",
    "02 01 00       ED AB 0D",
    "02 01 01       63 6F 0D",
    "02 01 02       54 85 0D",
    "02 01 03       AB A2 0D",
    "00",
    # Map [00 02]
    # Town of Bloodpool
    "00 02",
    "08             02",
    "40 00 80 00    93 3B 0E",
    "20 80 20 00 01 1A 88 0C",
    "80 80 20 00    00 00 06",
    "80 80 20 00    00 40 06",
    "20 80 20 00 02 1A 98 0C",
    "20 80 20 00 04 1A 90 0C",
    "40 00 80 80    93 3C 0E",
    "80 80 20 20    00 80 06",
    "10 82          98 DE 0D",
    "02 01 00       ED AB 0D",
    "02 01 01       63 6F 0D",
    "02 01 02       54 85 0D",
    "02 01 03       AB A2 0D",
    "00",
    # Map [00 03]
    # Town of Kasandora
    "00 03",
    "08             02",
    "40 00 80 00    93 3B 0E",
    "20 80 20 00 01 1A 88 0C",
    "80 80 20 00    00 00 06",
    "80 80 20 00    00 40 06",
    "20 80 20 00 02 1A 98 0C",
    "20 80 20 00 04 1A 90 0C",
    "40 00 80 80    93 3C 0E",
    "80 80 20 20    00 80 06",
    "10 82          98 DE 0D",
    "02 01 00       ED AB 0D",
    "02 01 01       63 6F 0D",
    "02 01 02       54 85 0D",
    "02 01 03       AB A2 0D",
    "00",
    # Map [00 04]
    # Town of Aitos
    "00 04",
    "08             02",
    "40 00 80 00    93 3B 0E",
    "20 80 20 00 01 1A 88 0C",
    "80 80 20 00    00 00 06",
    "80 80 20 00    00 40 06",
    "20 80 20 00 02 1A 98 0C",
    "20 80 20 00 04 1A 90 0C",
    "40 00 80 80    93 3C 0E",
    "80 80 20 20    00 80 06",
    "10 82          98 DE 0D",
    "02 01 00       ED AB 0D",
    "02 01 01       63 6F 0D",
    "02 01 02       54 85 0D",
    "02 01 03       AB A2 0D",
    "00",
    # Map [00 05]
    # Town of Marahna
    "00 05",
    "08             02",
    "40 00 80 00    93 3B 0E",
    "20 80 20 00 01 1A 88 0C",
    "80 80 20 00    00 00 06",
    "80 80 20 00    00 40 06",
    "20 80 20 00 02 1A 98 0C",
    "20 80 20 00 04 1A 90 0C",
    "40 00 80 80    93 3C 0E",
    "80 80 20 20    00 80 06",
    "10 82          98 DE 0D",
    "02 01 00       ED AB 0D",
    "02 01 01       63 6F 0D",
    "02 01 02       54 85 0D",
    "02 01 03       AB A2 0D",
    "00",
    # Map [00 06]
    # Town of Northwall
    "00 06",
    "08             02",
    "40 00 80 00    93 3D 0E",
    "20 80 20 00 01 1A 88 0C",
    "80 80 20 00    00 00 06",
    "80 80 20 00    00 40 06",
    "20 80 20 00 02 1A 98 0C",
    "20 80 20 00 04 1A 90 0C",
    "40 00 80 80    93 3C 0E",
    "80 80 20 20    00 80 06",
    "10 82          98 DE 0D",
    "02 01 00       ED AB 0D",
    "02 01 01       63 6F 0D",
    "02 01 02       54 85 0D",
    "02 01 03       AB A2 0D",
    "00",
    # Map [00 07]
    # Sky Palace
    "00 07",
    "08             00",
    "40 00 80 00    93 3E 0E",
    "20 80 20 00 03 1A A0 0C",
    "80 80 20 00    00 C0 06",
    "40 00 80 80    93 3C 0E",
    "80 80 20 20    00 80 06",
    "10 81          8F 38 0E",
    "10 82          9A E2 0D",
    "02 01 00       88 29 0E",
    "02 01 03       AB A2 0D",
    "02 01 04       8F 2B 03",
    "00",
    # Map [00 08]
    # Temple Interior
    "00 08",
    "08             00",
    "40 00 80 00    93 3E 0E",
    "20 80 20 00 01 1A A0 0C",
    "80 80 20 00    00 C0 06",
    "80 80 10 20    7F CE 02",
    "10 81          91 39 0E",
    "10 82          9C E6 0D",
    "02 01 00       ED AB 0D",
    "02 01 01       63 6F 0D",
    "02 01 02       54 85 0D",
    "02 01 03       AB A2 0D",
    "00",
    # Map [00 09]
    # Overworld
    "00 09",
    "08             01",
    "40 00 80 00    93 3F 0E",
    "80 80 20 FF    00 00 07",
    "02 01 01       CC 27 0E",
    "10 80          3F 33 03",
    "40 00 80 80    93 40 0E",
    "80 80 08 40    7F CE 02",
    "02 01 00       88 29 0E",
    "02 01 03       AB A2 0D",
    "00",
    # Map [01 01]
    # Forest
    # Centaur Knight
    "01 01",
    "08             03",
    "40 00 40 40    80 FF 02",
    "40 00 40 00    80 FF 0A",
    "20 00 20 00 01 CA 41 0D",
    "20 00 20 00 02 87 D6 0D",
    "80 00 10 00    00 40 07",
    "80 00 10 10    00 80 07",
    "80 00 08 50    FB EC 0B",
    "10 01          31 F1 0A",
    "10 02          04 07 0D",
    "80 00 10 30    00 00 08",
    "40 00 40 80    F8 4E 0E    80 00 10 40    2F B1 09",
    "01 00 00 00    95 D6 0C    01 01 00 00    C7 EF 03",
    "02 01 00       7F 14 0C",
    "00",
    # Map [01 02]
    # Caves I
    # Skeltous
    "01 02",
    "08             04",
    "40 00 40 40    78 4F 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 A6 3B 0D",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    00 80 0A",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          EE CF 0B",
    "10 02          62 B9 0D",
    "80 00 10 30    43 46 0A",
    "40 00 40 80    78 50 0E",
    "01 00 00 00    35 F3 0C",
    "02 01 00       9F 76 07",
    "00",
    # Map [01 03]
    # Caves II
    # Endless climb
    "01 03",
    "08             05",
    "40 00 40 40    78 4F 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 A6 3B 0D",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    00 80 0A",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          73 53 0D",
    "10 02          15 6A 0E",
    "80 00 10 30    43 46 0A",
    "40 00 40 80    78 50 0E",
    "01 00 00 00    35 F3 0C",
    "02 01 00       9F 76 07",
    "00",
    # Map [01 04]
    # Caves III
    # Minotaurus
    "01 04",
    "08             06",
    "40 00 40 40    78 4F 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 A6 3B 0D",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    00 80 0A",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          67 67 0E",
    "10 02          41 69 0E",
    "80 00 10 30    76 5D 0A",
    "40 00 40 80    F8 50 0E",
    "01 00 00 00    35 F3 0C    01 01 00 00    17 B0 0C",
    "02 01 00       70 94 0D",
    "00",
    # Map [02 01]
    # Swamp
    # Manticore
    "02 01",
    "08             07",
    "40 00 40 40    78 51 0E",
    "40 00 40 00    F8 51 0E",
    "20 00 20 00 01 E6 C1 0D",
    "20 00 20 00 02 A2 1C 0E",
    "80 00 10 00    C3 AD 0A",
    "80 00 10 10    00 80 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          C6 BF 0C",
    "10 02          78 65 0E",
    "80 00 10 30    00 C3 05",
    "40 00 40 80    78 52 0E    80 00 10 40    00 00 0A",
    "01 00 00 00    1F 07 0E    01 01 00 00    77 1B 03",
    "02 01 00       CC 5D 0C",
    "00",
    # Map [02 02]
    # Castle I
    # Front gate
    "02 02",
    "08             09",
    "40 00 40 40    F8 52 0E",
    "40 00 40 00    F8 51 0E",
    "20 00 20 00 01 FD 2E 0D",
    "20 00 20 00 02 A2 1C 0E",
    "80 00 10 00    BD B3 08",
    "80 00 10 10    00 80 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          84 37 0E",
    "10 02          74 4E 0E",
    "80 00 10 30    C8 DA 0A",
    "40 00 40 80    78 53 0E",
    "01 00 00 00    2E 78 05",
    "02 01 00       CC 5D 0C",
    "00",
    # Map [02 03]
    # Castle II
    # First elevator
    "02 03",
    "08             0A",
    "40 00 40 40    F8 52 0E",
    "40 00 40 00    F8 51 0E",
    "20 00 20 00 01 FD 2E 0D",
    "20 00 20 00 02 A2 1C 0E",
    "80 00 10 00    BD B3 08",
    "80 00 10 10    00 80 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          4A 7A 0D",
    "10 02          74 4E 0E",
    "80 00 10 30    C8 DA 0A",
    "40 00 40 80    78 53 0E",
    "01 00 00 00    2E 78 05",
    "02 01 00       CC 5D 0C",
    "00",
    # Map [02 04]
    # Castle III
    # Glowing cellar
    "02 04",
    "08             0B",
    "40 00 40 40    F8 52 0E",
    "40 00 40 00    F8 51 0E",
    "20 00 20 00 01 FD 2E 0D",
    "20 00 20 00 02 A2 1C 0E",
    "80 00 10 00    BD B3 08",
    "80 00 10 10    00 80 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          86 FE 07",
    "10 02          74 4E 0E",
    "80 00 10 30    C8 DA 0A",
    "40 00 40 80    78 53 0E",
    "01 00 00 00    2E 78 05",
    "02 01 00       CC 5D 0C",
    "00",
    # Map [02 05]
    # Castle IV
    # Second elevator
    "02 05",
    "08             0C",
    "40 00 40 40    F8 53 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 FD 2E 0D",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    BD B3 08",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          5D 66 0C",
    "10 02          2E FD 04",
    "80 00 10 30    C8 DA 0A",
    "40 00 40 80    78 53 0E",
    "01 00 00 00    2E 78 05",
    "02 01 00       CC 5D 0C",
    "00",
    # Map [02 06]
    # Castle V
    # Atop the wall
    "02 06",
    "08             0D",
    "40 00 40 40    F8 52 0E",
    "40 00 40 00    F8 51 0E",
    "20 00 20 00 01 FD 2E 0D",
    "20 00 20 00 02 A2 1C 0E",
    "80 00 10 00    BD B3 08",
    "80 00 10 10    00 80 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          28 43 0E",
    "10 02          74 66 0E",
    "80 00 10 30    C8 DA 0A",
    "40 00 40 80    78 53 0E",
    "01 00 00 00    2E 78 05",
    "02 01 00       CC 5D 0C",
    "00",
    # Map [02 07]
    # Castle VI
    # Yoku blocks
    "02 07",
    "08             0E",
    "40 00 40 40    F8 52 0E",
    "40 00 40 00    F8 51 0E",
    "20 00 20 00 01 FD 2E 0D",
    "20 00 20 00 02 A2 1C 0E",
    "80 00 10 00    BD B3 08",
    "80 00 10 10    00 80 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          93 EE 0D",
    "10 02          74 66 0E",
    "80 00 10 30    C8 DA 0A",
    "40 00 40 80    78 53 0E",
    "01 00 00 00    2E 78 05",
    "02 01 00       CC 5D 0C",
    "00",
    # Map [02 08]
    # Castle VII
    # Zeppelin Wolf
    "02 08",
    "08             0F",
    "40 00 40 40    F8 52 0E",
    "40 00 40 00    F8 51 0E",
    "20 00 20 00 01 FD 2E 0D",
    "20 00 20 00 02 A2 1C 0E",
    "80 00 10 00    BD B3 08",
    "80 00 10 10    00 80 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          57 49 0E",
    "10 02          74 66 0E",
    "80 00 10 30    00 00 0B",
    "40 00 40 80    78 54 0E",
    "01 00 00 00    2E 78 05    01 01 00 00    CF 27 0C",
    "02 01 00       70 94 0D",
    "00",
    # Map [03 01]
    # Desert I
    # Shifting sands
    "03 01",
    "08             10",
    "40 00 40 40    F8 54 0E",
    "40 00 40 00    78 55 0E",
    "20 00 20 00 01 AF 4D 0D",
    "20 00 20 00 02 02 B5 0D",
    "80 00 10 00    E2 99 08",
    "80 00 10 10    3C E1 09",
    "80 00 08 50    FB EC 0B",
    "10 01          41 3A 0C",
    "10 02          47 4C 0E",
    "80 00 10 30    D5 E6 08",
    "40 00 40 80    F8 55 0E",
    "01 00 00 00    00 00 0D",
    "02 01 00       CC 5D 0C",
    "00",
    # Map [03 02]
    # Desert II
    # Dagoba
    "03 02",
    "08             11",
    "40 00 40 40    F8 54 0E",
    "40 00 40 00    78 55 0E",
    "20 00 20 00 01 AF 4D 0D",
    "20 00 20 00 02 02 B5 0D",
    "80 00 10 00    E2 99 08",
    "80 00 10 10    3C E1 09",
    "80 00 08 50    FB EC 0B",
    "10 01          A2 F7 0B",
    "10 02          63 42 0E",
    "80 00 10 30    D5 E6 08",
    "40 00 40 80    F8 55 0E    80 00 10 40    68 A0 0B",
    "01 00 00 00    00 00 0D    01 01 00 00    7E B0 0D",
    "02 01 00       CC 5D 0C",
    "00",
    # Map [03 03]
    # Pyramid I
    # Mummy crypt
    "03 03",
    "08             12",
    "40 00 40 40    78 56 0E",
    "40 00 40 00    F8 56 0E",
    "20 00 20 00 01 57 64 0D",
    "20 00 20 00 02 56 14 0E",
    "80 00 10 00    00 00 09",
    "80 00 10 10    04 42 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          DE 0D 0E",
    "10 02          A0 32 0E",
    "80 00 10 30    34 32 09",
    "40 00 40 80    78 57 0E",
    "01 00 00 00    43 99 0D    01 01 00 00    7A D2 0D",
    "02 01 00       9F 76 07",
    "00",
    # Map [03 04]
    # Pyramid II
    # Anubis statues
    "03 04",
    "08             13",
    "40 00 40 40    78 56 0E",
    "40 00 40 00    F8 56 0E",
    "20 00 20 00 01 57 64 0D",
    "20 00 20 00 02 56 14 0E",
    "80 00 10 00    00 00 09",
    "80 00 10 10    04 42 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          8F 8A 0D",
    "10 02          A0 32 0E",
    "80 00 10 30    6A CD 08",
    "40 00 40 80    F8 57 0E",
    "01 00 00 00    43 99 0D    01 01 00 00    7A D2 0D",
    "02 01 00       9F 76 07",
    "00",
    # Map [03 05]
    # Pyramid III
    # Elevator race
    "03 05",
    "08             14",
    "40 00 40 40    78 56 0E",
    "40 00 40 00    F8 56 0E",
    "20 00 20 00 01 57 64 0D",
    "20 00 20 00 02 56 14 0E",
    "80 00 10 00    00 00 09",
    "80 00 10 10    04 42 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          03 E5 0C",
    "10 02          A0 32 0E",
    "80 00 10 30    34 32 09",
    "40 00 40 80    78 57 0E",
    "01 00 00 00    43 99 0D    01 01 00 00    7A D2 0D",
    "02 01 00       9F 76 07",
    "00",
    # Map [03 06]
    # Pyramid IV
    # Pharaoh
    "03 06",
    "08             15",
    "40 00 40 40    78 56 0E",
    "40 00 40 00    F8 56 0E",
    "20 00 20 00 01 57 64 0D",
    "20 00 20 00 02 56 14 0E",
    "80 00 10 00    00 00 09",
    "80 00 10 10    04 42 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          6F 36 0E",
    "10 02          A0 32 0E",
    "80 00 10 30    6A CD 08",
    "40 00 40 80    F8 57 0E",
    "01 00 00 00    43 99 0D    01 01 00 00    7A D2 0D",
    "02 01 00       70 94 0D",
    "00",
    # Map [04 01]
    # Mountains I
    # Auto-scroller
    "04 01",
    "08             16",
    "40 00 40 40    78 58 0E",
    "40 00 40 00    F8 58 0E",
    "20 00 20 00 01 FB 0D 0D",
    "20 00 20 00 02 0D 45 05",
    "80 00 10 00    2F 19 09",
    "80 00 10 10    09 6B 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          8E DF 0B",
    "10 02          DF 67 0E",
    "80 00 10 30    00 80 08",
    "40 00 40 80    78 59 0E",
    "01 00 00 00    17 4C 0C",
    "02 01 00       54 85 0D",
    "00",
    # Map [04 02]
    # Mountains II
    # Waterfall
    "04 02",
    "08             17",
    "40 00 40 40    78 58 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 FB 0D 0D",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    2F 19 09",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          58 A7 0D",
    "10 02          65 7F 0C",
    "80 00 10 30    00 80 08",
    "40 00 40 80    78 59 0E",
    "01 00 00 00    17 4C 0C",
    "02 01 00       54 85 0D",
    "00",
    # Map [04 03]
    # Mountains III
    # Serpent
    "04 03",
    "08             18",
    "40 00 40 40    78 58 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 FB 0D 0D",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    2F 19 09",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          B3 4B 0E",
    "10 02          65 7F 0C",
    "80 00 10 30    50 16 0B",
    "40 00 40 80    78 5A 0E",
    "01 00 00 00    17 4C 0C    01 01 00 00    24 CC 03",
    "02 01 00       E2 69 0D",
    "00",
    # Map [04 04]
    # Volcano I
    # Hall of giants
    "04 04",
    "08             19",
    "40 00 40 40    F8 5A 0E",
    "40 00 40 00    78 5B 0E",
    "20 00 20 00 01 1A F6 0D",
    "20 00 20 00 02 92 03 0E",
    "80 00 10 00    00 80 09",
    "80 00 10 10    E6 1A 08",
    "80 00 08 50    FB EC 0B",
    "10 01          93 DA 0D",
    "10 02          8E 0A 0E",
    "80 00 10 30    4A C9 09",
    "40 00 40 80    F8 5B 0E",
    "01 00 00 00    E6 6E 0C",
    "02 01 00       54 85 0D",
    "00",
    # Map [04 05]
    # Volcano II
    # Magma chamber
    "04 05",
    "08             1A",
    "40 00 40 40    F8 5A 0E",
    "40 00 40 00    78 5B 0E",
    "20 00 20 00 01 1A F6 0D",
    "20 00 20 00 02 92 03 0E",
    "80 00 10 00    00 80 09",
    "80 00 10 10    E6 1A 08",
    "80 00 08 50    FB EC 0B",
    "10 01          C7 46 0E",
    "10 02          EE 66 0E",
    "80 00 10 30    4A C9 09",
    "40 00 40 80    F8 5B 0E",
    "01 00 00 00    E6 6E 0C",
    "02 01 00       54 85 0D",
    "00",
    # Map [04 06]
    # Volcano III
    # Samurai archers
    "04 06",
    "08             1B",
    "40 00 40 40    F8 5A 0E",
    "40 00 40 00    78 5B 0E",
    "20 00 20 00 01 1A F6 0D",
    "20 00 20 00 02 92 03 0E",
    "80 00 10 00    00 80 09",
    "80 00 10 10    E6 1A 08",
    "80 00 08 50    FB EC 0B",
    "10 01          9D 8F 0D",
    "10 02          A7 BD 0D",
    "80 00 10 30    4A C9 09",
    "40 00 40 80    F8 5B 0E",
    "01 00 00 00    E6 6E 0C",
    "02 01 00       54 85 0D",
    "00",
    # Map [04 07]
    # Volcano IV
    # Fire Wheel
    "04 07",
    "08             1C",
    "40 00 40 40    F8 5A 0E",
    "40 00 40 00    78 5B 0E",
    "20 00 20 00 01 1A F6 0D",
    "20 00 20 00 02 92 03 0E",
    "80 00 10 00    00 80 09",
    "80 00 10 10    E6 1A 08",
    "80 00 08 50    FB EC 0B",
    "10 01          71 47 0E",
    "10 02          EC 43 0E",
    "80 00 10 30    7F EE 02",
    "40 00 40 80    78 5C 0E",
    "01 00 00 00    E6 6E 0C    01 01 00 00    76 7C 09",
    "02 01 00       70 94 0D",
    "00",
    # Map [05 01]
    # Jungle I
    # Overgrown ruins
    "05 01",
    "08             1D",
    "40 00 40 40    F8 5C 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 00 80 0D",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    3A B6 07",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          F8 B7 0C",
    "10 02          F7 65 0E",
    "80 00 10 30    8A 17 0A",
    "40 00 40 80    78 5D 0E",
    "01 00 00 00    F8 21 0D",
    "02 01 00       9F 76 07",
    "00",
    # Map [05 02]
    # Jungle II
    # Falling snakes
    "05 02",
    "08             1E",
    "40 00 40 40    F8 5C 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 00 80 0D",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    3A B6 07",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          D7 47 0D",
    "10 02          F7 65 0E",
    "80 00 10 30    8A 17 0A",
    "40 00 40 80    78 5D 0E",
    "01 00 00 00    F8 21 0D",
    "02 01 00       9F 76 07",
    "00",
    # Map [05 03]
    # Jungle III
    # Rafflasher
    "05 03",
    "08             1F",
    "40 00 40 40    F8 5C 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 00 80 0D",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    3A B6 07",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          DA 2C 0E",
    "10 02          B2 7F 0D",
    "80 00 10 30    05 4B 09",
    "40 00 40 80    F8 5D 0E",
    "01 00 00 00    F8 21 0D    01 01 00 00    9D 74 0A",
    "02 01 00       E2 69 0D",
    "00",
    # Map [05 04]
    # Temple I
    # Stone elevator
    "05 04",
    "08             20",
    "40 00 40 40    78 5E 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 DC DD 0C",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    17 5B 05",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          E1 74 0D",
    "10 02          93 41 0E",
    "80 00 10 30    86 2C 0B",
    "40 00 40 80    F8 5E 0E",
    "01 00 00 00    22 CF 0C",
    "02 01 00       54 85 0D",
    "00",
    # Map [05 05]
    # Temple II
    # Choose a path
    "05 05",
    "08             21",
    "40 00 40 40    78 5E 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 DC DD 0C",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    17 5B 05",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          63 17 0E",
    "10 02          B0 44 0E",
    "80 00 10 30    86 2C 0B",
    "40 00 40 80    F8 5E 0E",
    "01 00 00 00    22 CF 0C",
    "02 01 00       54 85 0D",
    "00",
    # Map [05 06]
    # Temple III
    # Left path
    "05 06",
    "08             22",
    "40 00 40 40    78 5E 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 DC DD 0C",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    17 5B 05",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          22 DF 05",
    "10 02          00 00 0E",
    "80 00 10 30    86 2C 0B",
    "40 00 40 80    F8 5E 0E",
    "01 00 00 00    22 CF 0C",
    "02 01 00       54 85 0D",
    "00",
    # Map [05 07]
    # Temple IV
    # Right path
    "05 07",
    "08             23",
    "40 00 40 40    78 5E 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 DC DD 0C",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    17 5B 05",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          22 DF 05",
    "10 02          00 00 0E",
    "80 00 10 30    86 2C 0B",
    "40 00 40 80    F8 5E 0E",
    "01 00 00 00    22 CF 0C",
    "02 01 00       54 85 0D",
    "00",
    # Map [05 08]
    # Temple V
    # Kalia
    "05 08",
    "08             24",
    "40 00 40 40    78 5E 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 DC DD 0C",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    17 5B 05",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          67 2E 0E",
    "10 02          65 45 0E",
    "80 00 10 30    4D C4 0A",
    "40 00 40 80    78 5F 0E",
    "01 00 00 00    22 CF 0C    01 01 00 00    00 80 0C",
    "02 01 00       70 94 0D",
    "00",
    # Map [06 01]
    # Arctic I
    # Snowfield
    "06 01",
    "08             25",
    "40 00 40 40    F8 5F 0E",
    "40 00 40 00    78 60 0E",
    "20 00 20 00 01 8A FA 05",
    "20 00 20 00 02 F9 9D 0D",
    "80 00 10 00    A8 98 09",
    "80 00 10 10    4B EC 07",
    "80 00 08 50    FB EC 0B",
    "10 01          7B 28 0D",
    "10 02          1A 46 0E",
    "80 00 10 30    05 2F 0A",
    "40 00 40 80    F8 60 0E",
    "01 00 00 00    75 35 0D",
    "02 01 00       4B FA 0C",
    "00",
    # Map [06 02]
    # Arctic II
    # Ice-cube rafts
    "06 02",
    "08             26",
    "40 00 40 40    F8 5F 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 8A FA 05",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    A8 98 09",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          34 59 0D",
    "10 02          9E 21 0E",
    "80 00 10 30    05 2F 0A",
    "40 00 40 80    F8 60 0E",
    "01 00 00 00    75 35 0D",
    "02 01 00       4B FA 0C",
    "00",
    # Map [06 03]
    # Arctic III
    # Ride the sled
    "06 03",
    "08             27",
    "40 00 40 40    F8 5F 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 8A FA 05",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    A8 98 09",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          92 0A 0C",
    "10 02          9E 21 0E",
    "80 00 10 30    05 2F 0A",
    "40 00 40 80    F8 60 0E",
    "01 00 00 00    75 35 0D",
    "02 01 00       4B FA 0C",
    "00",
    # Map [06 04]
    # Arctic IV
    # Merman Fly
    "06 04",
    "08             28",
    "40 00 40 40    F8 5F 0E",
    "40 00 40 00    F8 4F 0E",
    "20 00 20 00 01 8A FA 05",
    "20 00 20 00 02 5D F2 0D",
    "80 00 10 00    A8 98 09",
    "80 00 10 10    C8 56 0B",
    "80 00 08 50    FB EC 0B",
    "10 01          3D 35 0E",
    "10 02          77 7F 03",
    "80 00 10 30    A2 35 08",
    "40 00 40 80    78 61 0E",
    "01 00 00 00    75 35 0D    01 01 00 00    22 C6 0D",
    "02 01 00       E2 69 0D",
    "00",
    # Map [06 05]
    # Great Tree I
    # Tree entrance
    "06 05",
    "08             29",
    "40 00 40 40    F8 61 0E",
    "40 00 40 00    78 60 0E",
    "20 00 20 00 01 27 F9 09",
    "20 00 20 00 02 F9 9D 0D",
    "80 00 10 00    28 9B 07",
    "80 00 10 10    4B EC 07",
    "80 00 08 50    FB EC 0B",
    "10 01          2D 11 0E",
    "10 02          1A 46 0E",
    "80 00 10 30    1C 97 0A",
    "40 00 40 80    78 62 0E",
    "01 00 00 00    1D EC 0C",
    "02 01 00       27 C0 0B",
    "00",
    # Map [06 06]
    # Great Tree II
    # Lower trunk
    "06 06",
    "08             2A",
    "40 00 40 40    F8 61 0E",
    "40 00 40 00    78 60 0E",
    "20 00 20 00 01 27 F9 09",
    "20 00 20 00 02 F9 9D 0D",
    "80 00 10 00    28 9B 07",
    "80 00 10 10    4B EC 07",
    "80 00 08 50    FB EC 0B",
    "10 01          41 73 03",
    "10 02          D0 23 0E",
    "80 00 10 30    1C 97 0A",
    "40 00 40 80    78 62 0E",
    "01 00 00 00    1D EC 0C",
    "02 01 00       27 C0 0B",
    "00",
    # Map [06 07]
    # Great Tree III
    # Upper trunk
    "06 07",
    "08             2B",
    "40 00 40 40    F8 61 0E",
    "40 00 40 00    F8 62 0E",
    "20 00 20 00 01 27 F9 09",
    "20 00 20 00 02 F9 9D 0D",
    "80 00 10 00    28 9B 07",
    "80 00 10 10    4B EC 07",
    "80 00 08 50    FB EC 0B",
    "10 01          C6 5E 0D",
    "10 02          49 31 0E",
    "80 00 10 30    1C 97 0A",
    "40 00 40 80    78 62 0E",
    "01 00 00 00    1D EC 0C",
    "02 01 00       27 C0 0B",
    "00",
    # Map [06 08]
    # Great Tree IV
    # Arctic Wyvern
    "06 08",
    "08             2C",
    "40 00 40 40    F8 61 0E",
    "40 00 40 00    F8 62 0E",
    "20 00 20 00 01 27 F9 09",
    "20 00 20 00 02 F9 9D 0D",
    "80 00 10 00    28 9B 07",
    "80 00 10 10    4B EC 07",
    "80 00 08 50    FB EC 0B",
    "10 01          F1 49 0E",
    "10 02          55 68 0E",
    "80 00 10 30    62 5B 07",
    "40 00 40 80    78 63 0E",
    "01 00 00 00    1D EC 0C    01 01 00 00    37 31 0C",
    "02 01 00       70 94 0D",
    "00",
    # Map [07 01]
    # Death Heim
    # Hub room
    "07 01",
    "08             2D",
    "40 00 40 40    F8 63 0E",
    "40 00 40 00    78 64 0E",
    "20 00 20 00 01 56 CA 0D",
    "20 00 20 00 02 9E EA 0D",
    "80 00 10 00    27 6A 08",
    "80 00 10 10    46 D1 07",
    "80 00 08 50    FB EC 0B",
    "10 01          65 4D 0E",
    "10 02          13 7F 0B",
    "80 00 10 30    58 90 0B",
    "40 00 40 80    F8 64 0E",
    "01 00 00 00    00 00 0C",
    "02 01 00       70 94 0D    02 01 01       FA 54 0C",
    "00",
    # Map [07 02]
    # Death Heim
    # Minotaurus
    "07 02",
    "08             06",
    "40 00 40 40    78 4F 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 A6 3B 0D",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    00 80 0A",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          D8 4C 0E",
    "10 02          B5 69 0E",
    "80 00 10 30    58 90 0B",
    "40 00 40 80    F8 64 0E    80 00 10 40    76 5D 0A",
    "01 00 00 00    00 00 0C    01 01 00 00    78 C7 0C",
    "02 01 00       70 94 0D",
    "00",
    # Map [07 03]
    # Death Heim
    # Zeppelin Wolf
    "07 03",
    "08             0F",
    "40 00 40 40    F8 52 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 FD 2E 0D",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    BD B3 08",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          87 4A 0E",
    "10 02          B5 69 0E",
    "80 00 10 30    58 90 0B",
    "40 00 40 80    F8 64 0E    80 00 10 40    00 00 0B",
    "01 00 00 00    00 00 0C    01 01 00 00    65 1E 0C",
    "02 01 00       70 94 0D",
    "00",
    # Map [07 04]
    # Death Heim
    # Pharaoh
    "07 04",
    "08             15",
    "40 00 40 40    78 56 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 57 64 0D",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    00 00 09",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          BC 48 0E",
    "10 02          B5 69 0E",
    "80 00 10 30    58 90 0B",
    "40 00 40 80    F8 64 0E    80 00 10 40    6A CD 08",
    "01 00 00 00    00 00 0C    01 01 00 00    6A CE 0D",
    "02 01 00       70 94 0D",
    "00",
    # Map [07 05]
    # Death Heim
    # Fire Wheel
    "07 05",
    "08             1C",
    "40 00 40 40    F8 5A 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 1A F6 0D",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    00 80 09",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          17 48 0E",
    "10 02          B5 69 0E",
    "80 00 10 30    58 90 0B",
    "40 00 40 80    F8 64 0E    80 00 10 40    7F EE 02",
    "01 00 00 00    00 00 0C    01 01 00 00    D7 F9 0D",
    "02 01 00       70 94 0D",
    "00",
    # Map [07 06]
    # Death Heim
    # Kalia
    "07 06",
    "08             24",
    "40 00 40 40    78 5E 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 DC DD 0C",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    17 5B 05",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          41 2B 0E",
    "10 02          B5 69 0E",
    "80 00 10 30    58 90 0B",
    "40 00 40 80    F8 64 0E    80 00 10 40    4D C4 0A",
    "01 00 00 00    00 00 0C    01 01 00 00    1A A8 0C",
    "02 01 00       70 94 0D",
    "00",
    # Map [07 07]
    # Death Heim
    # Arctic Wyvern
    "07 07",
    "08             2C",
    "40 00 40 40    F8 61 0E",
    "40 00 40 00    F8 59 0E",
    "20 00 20 00 01 27 F9 09",
    "20 00 20 00 02 06 1A 0E",
    "80 00 10 00    28 9B 07",
    "80 00 10 10    01 50 08",
    "80 00 08 50    FB EC 0B",
    "10 01          1D 4B 0E",
    "10 02          B5 69 0E",
    "80 00 10 30    58 90 0B",
    "40 00 40 80    F8 64 0E    80 00 10 40    62 5B 07",
    "01 00 00 00    00 00 0C    01 01 00 00    2C 43 0C",
    "02 01 00       70 94 0D",
    "00",
    # Map [07 08]
    # Death Heim
    # Tanzra
    "07 08",
    "08             2E",
    "40 00 40 40    F8 63 0E",
    "40 00 40 00    78 64 0E",
    "20 00 20 00 01 56 CA 0D",
    "20 00 20 00 02 9E EA 0D",
    "80 00 10 00    27 6A 08",
    "80 00 10 10    46 D1 07",
    "80 00 08 50    FB EC 0B",
    "10 01          EF 4D 0E",
    "10 02          CB 68 0E",
    "80 00 10 30    58 90 0B",
    "40 00 40 80    F8 64 0E    80 00 10 40    C0 63 09",
    "01 00 00 00    00 00 0C    01 01 00 00    27 77 0C",
    "02 01 00       FA 54 0C",
    "00",
    # Map [08 01]
    # Ending
    "08 01",
    "08             2F",
    "40 00 10 00    C5 C7 03",
    "80 00 08 50    6F 1B 0D",
    "01 00 00 00    A0 D1 03",
    "02 01 00       5C B0 0B",
    "02 01 01       88 29 0E",
    "00",
]))



# Constants for the randomizer's gameplay options.
INITIAL_LIVES___EXTRA = "extra"
INITIAL_LIVES___UNLIMITED = "unlimited"
INITIAL_LIVES___DEATHCOUNT = "deathcount"
MARAHNA_PATH___LEFT = "left"
MARAHNA_PATH___RIGHT = "right"
MARAHNA_PATH_CHOICES = [
    MARAHNA_PATH___LEFT,
    MARAHNA_PATH___RIGHT,
]
BOSS_RUSH_TYPE___CONSECUTIVE = "consecutive"
BOSS_RUSH_TYPE___SCATTERED = "scattered"
BOSS_RUSH_TYPE_CHOICES = [
    BOSS_RUSH_TYPE___CONSECUTIVE,
    BOSS_RUSH_TYPE___SCATTERED,
]



def getFlagString(initialLives, zantetsuken, marahnaPath, bossRushType):
    flagString = ""

    if initialLives == INITIAL_LIVES___EXTRA:
        flagString += "E"
    elif initialLives == INITIAL_LIVES___UNLIMITED:
        flagString += "U"
    elif initialLives == INITIAL_LIVES___DEATHCOUNT:
        flagString += "D"

    if zantetsuken:
        flagString += "Z"

    if marahnaPath == MARAHNA_PATH___LEFT:
        flagString += "L"
    elif marahnaPath == MARAHNA_PATH___RIGHT:
        flagString += "R"

    if bossRushType == BOSS_RUSH_TYPE___CONSECUTIVE:
        flagString += "C"
    elif bossRushType == BOSS_RUSH_TYPE___SCATTERED:
        flagString += "S"

    return flagString



def randomize(seed, marahnaPath, bossRushType):
    # Create and seed the random number generator.
    rng = random.Random(seed)

    # Always do the coin flip, even if we're going to override the result.
    # This way, the shuffled map order for a given seed will stay the same,
    # even if the chosen Marahna-path option changes.
    marahnaCoinFlip = rng.choice(MARAHNA_PATH_CHOICES)
    if marahnaPath is None:
        marahnaPath = marahnaCoinFlip
    if marahnaPath not in MARAHNA_PATH_CHOICES:
        raise ValueError(f"Unexpected marahnaPath value: {marahnaPath!r}")

    bossRushTypeCoinFlip = rng.choice(BOSS_RUSH_TYPE_CHOICES)
    if bossRushType is None:
        bossRushType = bossRushTypeCoinFlip
    if bossRushType not in BOSS_RUSH_TYPE_CHOICES:
        raise ValueError(f"Unexpected bossRushType value: {bossRushType!r}")

    # Shuffle the maps.
    BOSS_RUSH_PLACEHOLDER = 0x700
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
        0x504, 0x505, (0x506 if marahnaPath == MARAHNA_PATH___LEFT else 0x507), 0x508,
        0x601, 0x602, 0x603, 0x604,
        0x605, 0x606, 0x607, 0x608,
        *([BOSS_RUSH_PLACEHOLDER] * 8),
    ]
    rng.shuffle(mapNumbers)

    # Shuffle the boss rooms, and end the boss rush with Death Heim Clear.
    bossRush = [0x702, 0x703, 0x704, 0x705, 0x706, 0x707, 0x708]
    rng.shuffle(bossRush)
    bossRush.append(0x701)

    # Combine the shuffled maps and boss rush.
    if bossRushType == BOSS_RUSH_TYPE___CONSECUTIVE:
        # Remove the boss rush placeholders.
        mapNumbers = [i for i in mapNumbers if i != BOSS_RUSH_PLACEHOLDER]
        # Insert the entire boss rush at a random index.
        consecutiveIndex = rng.randint(0, len(mapNumbers))
        mapNumbers[consecutiveIndex:consecutiveIndex] = bossRush
    elif bossRushType == BOSS_RUSH_TYPE___SCATTERED:
        # Replace the boss rush placeholders with boss rooms.
        for boss in bossRush:
            placeholderIndex = mapNumbers.index(BOSS_RUSH_PLACEHOLDER)
            mapNumbers[placeholderIndex] = boss

    return mapNumbers, marahnaPath, bossRushType



def getHashString(mapNumbers):
    hashInput = ",".join([randomizerVersion, *[format(x, "X") for x in mapNumbers]])
    hashString = hashlib.md5(hashInput.encode()).hexdigest().upper()[:8]
    return hashString



# Helper function for writing blocks of bytes.
def writeHelper(buffer, offset, data):
    nextOffset = offset + len(data)
    buffer[offset:nextOffset] = data
    return nextOffset



def modifyROM(romBytes, titleString, mapNumbers, initialLives, zantetsuken):
    # Limit the number of rooms.
    # (The room counter uses BCD and cannot store values higher than 99.)
    mapNumbersLimit = 99
    if len(mapNumbers) > mapNumbersLimit:
        raise ValueError(f"Too many map numbers: {len(mapNumbers)!r} # Limit: {mapNumbersLimit!r}")

    # Create a mutable copy of romBytes.
    romByteArray = bytearray(romBytes)

    # Write the extended map metadata to 0xF8000.
    writeHelper(romByteArray, 0xF8000, extendedMapMetadata)

    # Look for map metadata at 0xF8000 instead of 0x28000.
    writeHelper(romByteArray, 0x13E28, bytes.fromhex(" ".join([
        "A9 1F",       # 02/BE28: LDA #$1F ; Map metadata bank (was #$05)
    ])))

    # Always show exactly one menu option on the title screen.
    # (ActRaiser does this to show "> START" when there's no save data.)
    writeHelper(romByteArray, 0x1270D, bytes.fromhex(" ".join([
        "EA",          # 02/A70D: NOP
        "EA",          # 02/A70E: NOP
    ])))

    # Change the one menu option to show the selected seed and flags.
    # We need more space to store the seed-and-flags string, so let's
    # repurpose the space used by the menu-cursor strings at 0x12A34.
    writeHelper(romByteArray, 0x12711, bytes.fromhex(" ".join([
        "A9 00 11",    # 02/A711: LDA #$1100 ; Text location (was #$120C)
        "A0 34 AA",    # 02/A714: LDY #$AA34 ; Text pointer  (was #$A9D6)
    ])))
    menuOptionBytes = f"{'> ' + titleString[:25]:^32.32s}\x00".encode("ascii")
    writeHelper(romByteArray, 0x12A34, menuOptionBytes)

    # Display the seed hash and randomizer version on the title screen.
    # (Prepend the new line to the existing copyright/license text.)
    writeHelper(romByteArray, 0x1271B, bytes.fromhex(" ".join([
        "A9 00 15",    # 02/A71B: LDA #$1500 ; Text location (was #$1700)
        "A0 BF A9",    # 02/A71E: LDY #$A9BF ; Text pointer  (was #$A9DE)
    ])))
    hashString = getHashString(mapNumbers)
    hvLineBytes = f"  {hashString:<8.8s}  {'v.' + randomizerVersion[:15]:>17.17s}\x0D\x0D".encode("ascii")
    writeHelper(romByteArray, 0x129BF, hvLineBytes)

    # Always enter Professional Mode from the title screen menu.
    writeHelper(romByteArray, 0x40, bytes.fromhex(" ".join([
        "EA",          # 00/8040: NOP
        "EA",          # 00/8041: NOP
    ])))

    # Add the room counter to the HUD.
    # You can't get or use magic in Professional Mode, so this feature
    # repurposes storage and memory normally used by magic.

    # Replace the code that draws a scroll for each MP you have (always zero
    # in Professional Mode) with code to display the room counter.
    writeHelper(romByteArray, 0x142C8, bytes.fromhex(" ".join([
        "E2 20",       # 02/C2C8: SEP #$20
        "A5 21",       # 02/C2CA: LDA $21
        "4A",          # 02/C2CC: LSR
        "4A",          # 02/C2CD: LSR
        "4A",          # 02/C2CE: LSR
        "4A",          # 02/C2CF: LSR
        "09 30",       # 02/C2D0: ORA #$30
        "8F 46 B0 7F", # 02/C2D2: STA $7FB046 ; Tens digit
        "A5 21",       # 02/C2D6: LDA $21
        "29 0F",       # 02/C2D8: AND #$0F
        "09 30",       # 02/C2DA: ORA #$30
        "8F 48 B0 7F", # 02/C2DC: STA $7FB048 ; Ones digit
        "EA",          # 02/C2E0: NOP
        "EA",          # 02/C2E1: NOP
        "EA",          # 02/C2E2: NOP
        "EA",          # 02/C2E3: NOP
        "EA",          # 02/C2E4: NOP
        "EA",          # 02/C2E5: NOP
        "EA",          # 02/C2E6: NOP
        "EA",          # 02/C2E7: NOP
    ])))

    # Update the HUD's fixed content to replace "[ACT]" with the person icon
    # and two reserved spaces for the room counter's digits.
    struct.pack_into("<6H", romByteArray, 0x10E7E, *[
        0x0000,
        0x003A, # Person icon, left half
        0x003B, # Person icon, right half
        0x0030, # Room counter, tens digit placeholder
        0x0030, # Room counter, ones digit placeholder
        0x0000,
    ])

    # Handle the "extra lives", "unlimited lives", and "death count" cases.
    if initialLives is None:
        pass
    elif initialLives == INITIAL_LIVES___EXTRA:
        # The value in memory is BCD and one less than the displayed value.
        # e.g. 0x09 --> 9 decimal --> 10 lives shown on the HUD
        writeHelper(romByteArray, 0x12B13, bytes.fromhex(" ".join([
            "A9 09",       # 02/AB13: LDA #$09 ; Initial number of lives (was #$04)
        ])))
    elif initialLives == INITIAL_LIVES___UNLIMITED:
        # The value in memory is BCD and one less than the displayed value.
        # e.g. 0x98 --> 98 decimal --> 99 lives shown on the HUD
        writeHelper(romByteArray, 0x12B13, bytes.fromhex(" ".join([
            "A9 98",       # 02/AB13: LDA #$98 ; Initial number of lives (was #$04)
        ])))
        # Upon death, don't lose a life.
        writeHelper(romByteArray, 0x2AD, bytes.fromhex(" ".join([
            "EA",          # 00/82AD: NOP
            "EA",          # 00/82AE: NOP
            "EA",          # 00/82AF: NOP
            "EA",          # 00/82B0: NOP
            "EA",          # 00/82B1: NOP
            "EA",          # 00/82B2: NOP
            "EA",          # 00/82B3: NOP
            "EA",          # 00/82B4: NOP
            "EA",          # 00/82B5: NOP
        ])))
        # If you collect a 1-Up, don't gain a life.
        writeHelper(romByteArray, 0x7C7, bytes.fromhex(" ".join([
            "EA",          # 00/87C7: NOP
            "EA",          # 00/87C8: NOP
            "EA",          # 00/87C9: NOP
        ])))
    elif initialLives == INITIAL_LIVES___DEATHCOUNT:
        # On the HUD, replace the heart icon with a slash.
        # (Visual indicator of deathcount mode.)
        struct.pack_into("<H", romByteArray, 0x10E8A, *[
            0x0C2F, # Red slash (was 0x0C7B, red heart)
        ])
        # On the HUD, display "deathcount" instead of "deathcount + 1".
        writeHelper(romByteArray, 0x14285, bytes.fromhex(" ".join([
            "EA",          # 02/C285: NOP ; Tens digit
            "EA",          # 02/C286: NOP
            "EA",          # 02/C287: NOP
        ])))
        writeHelper(romByteArray, 0x14297, bytes.fromhex(" ".join([
            "EA",          # 02/C297: NOP ; Ones digit
            "EA",          # 02/C298: NOP
            "EA",          # 02/C299: NOP
        ])))
        # Start with zero deaths.
        writeHelper(romByteArray, 0x12B13, bytes.fromhex(" ".join([
            "A9 00",       # 02/AB13: LDA #$00 ; Initial number of lives in vanilla (was #$04)
        ])))
        # Don't "prepare for Game Over" if you die with zero deaths.
        writeHelper(romByteArray, 0x13D1B, bytes.fromhex(" ".join([
            "80 1C",       # 02/BD1B: BRA $BD39 ; Always branch (was BNE)
        ])))
        # Upon death, increment the death count.
        # The function we're calling is the "gain a life" function used
        # by 1-Ups in vanilla. It gracefully handles the "99 + 1" case.
        writeHelper(romByteArray, 0x2AD, bytes.fromhex(" ".join([
            "20 50 88",    # 00/82AD: JSR $8850
            "EA",          # 00/82B0: NOP
            "EA",          # 00/82B1: NOP
            "EA",          # 00/82B2: NOP
            "EA",          # 00/82B3: NOP
            "EA",          # 00/82B4: NOP
            "EA",          # 00/82B5: NOP
        ])))
        # If you collect a 1-Up, don't change the death count.
        writeHelper(romByteArray, 0x7C7, bytes.fromhex(" ".join([
            "EA",          # 00/87C7: NOP
            "EA",          # 00/87C8: NOP
            "EA",          # 00/87C9: NOP
        ])))
    else:
        raise ValueError(f"Unexpected initialLives value: {initialLives!r}")

    # Update the HUD's fixed content to not show ten MP scrolls.
    # For some reason, the fixed content has the variable fields filled in
    # (mostly with zeroes, but for MP, with ten scroll icons). Without the
    # scroll-drawing code, there's nothing to erase them, so let's remove
    # them here.
    struct.pack_into("<10H", romByteArray, 0x10EE8, *[0x0000] * 10)

    # Write the list of map numbers to ROM.
    # Prepend 0x801 to roll the credits after completing room 99.
    # (The room counter overflows, so it reads room 00 after room 99.)
    # Append 0x801 to roll the credits after completing the last room.
    struct.pack_into(
        f"<{1+len(mapNumbers)+1}H",
        romByteArray,
        0xF9800,
        *[0x801, *mapNumbers, 0x801],
    )

    # Update the map-changing function to use and update the room counter.
    # There's not enough space in the map-changing function for all of the
    # new code, so let's put in a subroutine call to some unused space...
    writeHelper(romByteArray, 0x26C, bytes.fromhex(" ".join([
        "22 00 97 1F", # 00/826C: JSL $1F9700
    ])))
    # ...and write the new code in that unused space.
    writeHelper(romByteArray, 0xF9700, bytes.fromhex(" ".join([
        # Check if the room counter is zero (start of a new game).
        # If so, skip ahead to advancing the room counter.
        "A5 21",       # 1F/9700: LDA $21
        "F0 40",       # 1F/9702: BEQ $9744
        # If the given vanilla destination is map 0x801, go there.
        # (This handles the "map change because of Game Over" case.)
        "A5 1B",       # 1F/9704: LDA $1B
        "C9 08",       # 1F/9706: CMP #$08
        "D0 09",       # 1F/9708: BNE $9713
        "A5 1A",       # 1F/970A: LDA $1A
        "C9 01",       # 1F/970C: CMP #$01
        "D0 03",       # 1F/970E: BNE $9713
        "4C 8B 97",    # 1F/9710: JMP $978B
        # Check if we're changing maps because of player death.
        "AD 2C 03",    # 1F/9713: LDA $032C
        "F0 0B",       # 1F/9716: BEQ $9723
        # If so, reload the current map.
        "A5 18",       # 1F/9718: LDA $18
        "85 1B",       # 1F/971A: STA $1B
        "A5 19",       # 1F/971C: LDA $19
        "85 1A",       # 1F/971E: STA $1A
        "4C 8B 97",    # 1F/9720: JMP $978B
        # If we're in the Death Heim hub room (0x701), on the way to
        # a Death Heim boss room (0x702 to 0x708), go there.
        "A5 18",       # 1F/9723: LDA $18
        "C9 07",       # 1F/9725: CMP #$07
        "D0 1B",       # 1F/9727: BNE $9744
        "A5 19",       # 1F/9729: LDA $19
        "C9 01",       # 1F/972B: CMP #$01
        "D0 15",       # 1F/972D: BNE $9744
        "AD 47 03",    # 1F/972F: LDA $0347
        "C9 07",       # 1F/9732: CMP #$07
        "F0 0E",       # 1F/9734: BEQ $9744
        "A9 07",       # 1F/9736: LDA #$07
        "85 1B",       # 1F/9738: STA $1B
        "AD 47 03",    # 1F/973A: LDA $0347
        "1A",          # 1F/973D: INC
        "1A",          # 1F/973E: INC
        "85 1A",       # 1F/973F: STA $1A
        "4C 8B 97",    # 1F/9741: JMP $978B
        # Advance the room counter.
        "F8",          # 1F/9744: SED
        "A5 21",       # 1F/9745: LDA $21
        "18",          # 1F/9747: CLC
        "69 01",       # 1F/9748: ADC #$01
        "85 21",       # 1F/974A: STA $21
        "D8",          # 1F/974C: CLD
        # Use the room counter to get the map number of the next room.
        "A5 21",       # 1F/974D: LDA $21
        "4A",          # 1F/974F: LSR
        "4A",          # 1F/9750: LSR
        "4A",          # 1F/9751: LSR
        "4A",          # 1F/9752: LSR
        "8D 02 42",    # 1F/9753: STA $4202
        "A9 0A",       # 1F/9756: LDA #$0A
        "8D 03 42",    # 1F/9758: STA $4203
        "A9 00",       # 1F/975B: LDA #$00
        "EB",          # 1F/975D: XBA
        "A5 21",       # 1F/975E: LDA $21
        "29 0F",       # 1F/9760: AND #$0F
        "18",          # 1F/9762: CLC
        "6D 16 42",    # 1F/9763: ADC $4216
        "0A",          # 1F/9766: ASL
        "AA",          # 1F/9767: TAX
        "BF 01 98 1F", # 1F/9768: LDA $1F9801,X
        "85 1B",       # 1F/976C: STA $1B
        "BF 00 98 1F", # 1F/976E: LDA $1F9800,X
        "85 1A",       # 1F/9772: STA $1A
        # If the next room is in Death Heim (0x701 to 0x708), change
        # the "number of boss-rush bosses defeated" value to control
        # the hub room's behaviour, then detour to the hub room.
        "A5 1B",       # 1F/9774: LDA $1B
        "C9 07",       # 1F/9776: CMP #$07
        "D0 11",       # 1F/9778: BNE $978B
        "A5 1A",       # 1F/977A: LDA $1A
        "3A",          # 1F/977C: DEC
        "3A",          # 1F/977D: DEC
        "29 07",       # 1F/977E: AND #$07
        "8D 47 03",    # 1F/9780: STA $0347
        "A9 07",       # 1F/9783: LDA #$07
        "85 1B",       # 1F/9785: STA $1B
        "A9 01",       # 1F/9787: LDA #$01
        "85 1A",       # 1F/9789: STA $1A
        # Execute the instructions we overwrote to call this new subroutine.
        "A5 1A",       # 1F/978B: LDA $1A
        "85 19",       # 1F/978D: STA $19
        # Return.
        "6B",          # 1F/978F: RTL
    ])))

    # Skip the "descending ball of light brings statue to life" animation.
    # On some maps, it causes the player to take unavoidable damage.
    writeHelper(romByteArray, 0x12B0D, bytes.fromhex(" ".join([
        "9C FC 00",    # 02/AB0D: STZ $00FC
    ])))

    # Handle the "permanent sword upgrade" case.
    if zantetsuken:
        # Check-if-sword-upgraded helper function: Sword is always upgraded
        writeHelper(romByteArray, 0x8CE, bytes.fromhex(" ".join([
            "EA",          # 00/88CE: NOP
            "EA",          # 00/88CF: NOP
        ])))
        # Sword attack power: Always 2
        writeHelper(romByteArray, 0x1DD9, bytes.fromhex(" ".join([
            "80 01",       # 00/9DD9: BRA $9DDC ; Always branch (was BNE)
        ])))

    # Prevent animated tiles from glitching.
    for offset in range(0x1093E + 0x18, 0x10E7E, 0x1C):
        romByteArray[offset] &= 0x7F

    # When entering the Death Heim hub room:
    # - Always show the "warp in" visual effect
    writeHelper(romByteArray, 0x74FE, bytes.fromhex(" ".join([
        "EA",          # 00/F4FE: NOP
        "EA",          # 00/F4FF: NOP
    ])))
    # - Always play the "warp in" sound effect
    writeHelper(romByteArray, 0x7677, bytes.fromhex(" ".join([
        "EA",          # 00/F677: NOP
        "EA",          # 00/F678: NOP
    ])))
    # - Always play the "gem shatter" sound effect
    writeHelper(romByteArray, 0x7687, bytes.fromhex(" ".join([
        "EA",          # 00/F687: NOP
        "EA",          # 00/F688: NOP
    ])))

    # Update the "boss eyes and gems" animation in the Death Heim hub room.
    writeHelper(romByteArray, 0x7534, bytes.fromhex(" ".join([
        # Hide all of the boss eyes and gems, except for those of the
        # boss you're about to fight.
        "A0 00 00",    # 00/F534: LDY #$0000
        "DA",          # 00/F537: PHX
        "CC 47 03",    # 00/F538: CPY $0347
        "F0 09",       # 00/F53B: BEQ $F546
        "A9 00 40",    # 00/F53D: LDA #$4000
        "9D 40 00",    # 00/F540: STA $0040,X ; Hide eyes
        "9D 80 00",    # 00/F543: STA $0080,X ; Hide gem
        "8A",          # 00/F546: TXA
        "18",          # 00/F547: CLC
        "69 80 00",    # 00/F548: ADC #$0080
        "AA",          # 00/F54B: TAX
        "C8",          # 00/F54C: INY
        "C0 07 00",    # 00/F54D: CPY #$0007
        "90 E6",       # 00/F550: BCC $F538
        "FA",          # 00/F552: PLX
        # Skip the eye-dimming and gem-shattering animations.
        "AD 47 03",    # 00/F553: LDA $0347
        "C9 07 00",    # 00/F556: CMP #$0007
        "F0 4E",       # 00/F559: BEQ $F5A9
        "80 20",       # 00/F55B: BRA $F57D
    ])))

    # Upon defeating a boss-rush boss:
    # - Don't change the "number of boss-rush bosses defeated" value
    # - Take away the sword upgrade, so you don't keep it after defeating Tanzra
    # Let's overwrite the code for the former with code for the latter.
    writeHelper(romByteArray, 0x7EEE, bytes.fromhex(" ".join([
        "E2 20",       # 00/FEEE: SEP #$20
        "64 E4",       # 00/FEF0: STZ $E4
        "C2 20",       # 00/FEF0: REP #$20
    ])))
    # - Stop playing Tanzra's theme after leaving Tanzra's boss room
    writeHelper(romByteArray, 0x7F00, bytes.fromhex(" ".join([
        "80 05",       # 00/FF00: BRA $FF07 ; Always branch (was BNE)
    ])))

    # Update detection of "roll credits" vs "Game Over".
    # Map 0x801 is used for both the end credits and the Game Over screen.
    # In vanilla, the game decided which to show by keeping a count of Acts
    # cleared (with Death Heim counting as an Act). If all of the Acts were
    # cleared, roll the credits. Otherwise, game over.
    # This led to a bug in earlier versions of the randomizer, where you
    # could defeat all the end-of-Act bosses and clear Death Heim, then run
    # out of lives. The game would load map 0x801 for the Game Over screen,
    # but since you'd cleared every Act, it would roll the credits instead.
    # To fix this, let's use the room counter to decide which to show.
    # The credits threshold is the highest room number (in BCD), plus one:
    # - 48 rooms = 0x48 highest room number = 0x49 credits threshold
    # - 19 rooms = 0x19 highest room number = 0x1A credits threshold
    # If the room counter is below the threshold, show the Game Over screen.
    # Otherwise, roll the credits.
    creditsThreshold = ((len(mapNumbers) // 10) << 4) + (len(mapNumbers) % 10) + 1
    writeHelper(romByteArray, 0x12AA4, bytes.fromhex(" ".join([
        "EA",          # 02/AAA4: NOP
        "A5 21",       # 02/AAA5: LDA $21
        "F0 04",       # 02/AAA7: BEQ $AAAD ; Roll credits if in room 00 (overflow after room 99)
        f"C9 {creditsThreshold:02X}",
                       # 02/AAA9: CMP #$--  ; Threshold is #$49 for a normal 48-room game
        "90 3C",       # 02/AAAB: BCC $AAE9 ; Game Over if below the credits threshold
    ])))

    # After clearing an Act, keep the "current Act" counter at 1.
    # In vanilla, the "current Act" counter is used to select the next
    # map after clearing an Act. After clearing 13 Acts (12 end-of-Act
    # bosses plus Death Heim Clear), it selects map 0x801 in order to
    # roll the credits.
    # In the randomizer, the updated map-changing function usually
    # disregards the given vanilla destinations... but not 0x801.
    # When given 0x801, it goes to 0x801 immediately in order to
    # handle the "Game Over" case.
    # Consequently: After clearing the 13th end-of-Act room in the
    # shuffle, we get an unexpected Game Over.
    # Solution: Prevent the "current Act" counter from counting up.
    writeHelper(romByteArray, 0x788, bytes.fromhex(" ".join([
        "A9 01 00",    # 00/8788: LDA #$0001
        "8D 49 03",    # 00/878B: STA $0349
    ])))

    return romByteArray



def generate(romBytes, isRaceSeed, seed, initialLives, zantetsuken, marahnaPath, bossRushType):
    # If we're generating a race seed, override the seed argument
    if isRaceSeed:
        seed = None

    # Flag string
    flagString = getFlagString(initialLives, zantetsuken, marahnaPath, bossRushType)

    # Randomize
    mapNumbers, chosenMarahnaPath, chosenBossRushType = randomize(seed, marahnaPath, bossRushType)

    # Title string
    titleString = f"{'RACE!' if isRaceSeed else seed}"
    if flagString:
        titleString += f" -{flagString}"

    # Modify ROM
    romByteArray = None
    if romBytes:
        romByteArray = modifyROM(romBytes, titleString, mapNumbers, initialLives, zantetsuken)

    return romByteArray, mapNumbers, chosenMarahnaPath, chosenBossRushType



if __name__ == "__main__":
    # Process the command line arguments.
    parser = argparse.ArgumentParser(
        description = textwrap.dedent(f"""\
            ActRaiser Randomizer for Professional Mode
            (version: {randomizerVersion})"""
        ),
        formatter_class = argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = randomizerVersion,
    )
    seedGroup = parser.add_mutually_exclusive_group()
    seedGroup.add_argument(
        "-s", "--seed",
        type = int,
        help = "specify the RNG seed value",
    )
    seedGroup.add_argument(
        "-r", "--race-seed",
        action = "store_true",
        help = "generate a race seed with a hidden seed value",
    )
    parser.add_argument(
        "-l", "--spoiler-log",
        action = "store_true",
        help = "print spoiler log",
    )
    parser.add_argument(
        "-n", "--dry-run",
        action = "store_true",
        help = "execute without saving any changes",
    )
    initialLivesGroup = parser.add_mutually_exclusive_group()
    initialLivesGroup.add_argument(
        "-E", "--extra-lives",
        action = "store_const",
        const = INITIAL_LIVES___EXTRA,
        dest = "initial_lives",
        help = "start with 10 lives instead of 5",
    )
    initialLivesGroup.add_argument(
        "-U", "--unlimited-lives",
        action = "store_const",
        const = INITIAL_LIVES___UNLIMITED,
        dest = "initial_lives",
        help = "play with unlimited lives",
    )
    initialLivesGroup.add_argument(
        "-D", "--death-count",
        action = "store_const",
        const = INITIAL_LIVES___DEATHCOUNT,
        dest = "initial_lives",
        help = "show death count instead of lives remaining",
    )
    parser.add_argument(
        "-Z", "--zantetsuken",
        action = "store_true",
        help = "play with a permanent sword upgrade",
    )
    marahnaPathGroup = parser.add_mutually_exclusive_group()
    marahnaPathGroup.add_argument(
        "-L", "--left-path",
        action = "store_const",
        const = MARAHNA_PATH___LEFT,
        dest = "marahna_path",
        help = "use the left path in Marahna II",
    )
    marahnaPathGroup.add_argument(
        "-R", "--right-path",
        action = "store_const",
        const = MARAHNA_PATH___RIGHT,
        dest = "marahna_path",
        help = "use the right path in Marahna II",
    )
    bossRushTypeGroup = parser.add_mutually_exclusive_group()
    bossRushTypeGroup.add_argument(
        "-C", "--consecutive-boss-rush",
        action = "store_const",
        const = BOSS_RUSH_TYPE___CONSECUTIVE,
        dest = "boss_rush_type",
        help = textwrap.dedent("""\
            fight all seven boss-rush bosses back-to-back, in
            random order, at a random location in the shuffle"""
        ),
    )
    bossRushTypeGroup.add_argument(
        "-S", "--scattered-boss-rush",
        action = "store_const",
        const = BOSS_RUSH_TYPE___SCATTERED,
        dest = "boss_rush_type",
        help = textwrap.dedent("""\
            split the boss rush into individual boss battles,
            scattered randomly among the other shuffled rooms"""
        ),
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

    if args.race_seed and args.spoiler_log:
        parser.error("You cannot print a spoiler log when generating a race seed")
    if args.input_file is None and not args.dry_run:
        parser.error("Argument 'input-file' is required when not in dry-run mode")

    # Seed
    seed = args.seed
    if seed is None:
        seed = random.getrandbits(32)
    seed %= 2**32

    # Flag string
    flagString = getFlagString(
        args.initial_lives,
        args.zantetsuken,
        args.marahna_path,
        args.boss_rush_type,
    )

    # If there's an input file, read it.
    romBytes = None
    if args.input_file:
        # Read the input file.
        inFileName = args.input_file
        with open(inFileName, "rb") as inFile:
            romBytes = inFile.read()

        # Sanity-check the input file.
        if len(romBytes) != 1048576:
            raise ValueError(f"Input file {inFileName!r} is not 1048576 bytes in size")
        romName = romBytes[0x7FC0:0x7FD5]
        goodName = b"ACTRAISER-USA        "
        if romName != goodName:
            raise ValueError(f"Unexpected internal ROM name: {romName!r} # Expected: {goodName!r}")

    # Generate the seed.
    (
        romByteArray,
        mapNumbers,
        chosenMarahnaPath,
        chosenBossRushType,
    ) = generate(
        romBytes,
        args.race_seed,
        seed,
        args.initial_lives,
        args.zantetsuken,
        args.marahna_path,
        args.boss_rush_type,
    )

    # Hash string
    hashString = getHashString(mapNumbers)

    # Print the basic seed details.
    print(f"Version: {randomizerVersion}")
    print(f"Seed: {'(race seed)' if args.race_seed else seed}")
    print(f"Flags: {flagString if flagString else '-'}")
    print(f"Hash: {hashString}")

    # Optional: Print the spoiler log.
    if args.spoiler_log:
        print("---------------------------------------")
        print(f"Marahna II path: {chosenMarahnaPath}")
        print(f"Boss rush type: {chosenBossRushType}")
        for row in itertools.batched(mapNumbers, 10):
            print(" ".join([format(x, "X") for x in row]))
        print("---------------------------------------")

    # Print a trailing newline.
    print()

    # If we're not in dry-run mode, write the output file.
    if not args.dry_run:
        outFileName = args.output_file
        if outFileName is None:
            suffix = f"_{'RACE' if args.race_seed else seed}"
            if flagString:
                suffix += f"_{flagString}"
            if args.race_seed:
                suffix += f"_{hashString}"

            basename, dot, extension = inFileName.rpartition(".")
            if basename and extension:
                basename += suffix
            else:
                extension += suffix
            outFileName = basename + dot + extension

        with open(outFileName, "xb") as outFile:
            outFile.write(romByteArray)
