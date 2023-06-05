# actraiser-randomizer
Randomizer for ActRaiser's Professional Mode

## Getting Started
1. Check if you have Python installed.
   * Open a command prompt and try the following commands:
      * `py --version`
      * `python --version`
      * `python3 --version`
   * If one of these returns a Python 3.x version string (e.g. `Python 3.11.2`), you should be good to go.
   * If not, [download and install Python](https://www.python.org/downloads/).
1. Click the green "Code" button at the upper right of this repository page, then "Download ZIP".
1. Extract the ZIP archive's contents to a convenient directory.
1. Copy an ActRaiser (USA) ROM into the directory from the previous step.
1. **Optional:** Validate your ActRaiser (USA) ROM.
   * The ROM should be 1,048,576 bytes long.
      * If your ROM is 1,049,088 bytes long, it has a 512-byte copier header at the start.
      * You can remove the copier header with NSRT ([Windows](https://www.romhacking.net/utilities/400/),
        [Mac](https://www.romhacking.net/utilities/484/), [Linux](https://www.romhacking.net/utilities/401/)).
   * The ROM should have the following checksums:
     ```
       CRC32: EAC3358D
         MD5: 635D5D7DD2AAD4768412FBAE4A32FD6E
       SHA-1: E8365852CC20178D42C93CD188A7AE9AF45369D7
     SHA-256: B8055844825653210D252D29A2229F9A3E7E512004E83940620173C57D8723F0
     ```

## Usage
* Open a command prompt and navigate to the directory with the randomizer files and ActRaiser (USA) ROM.<br/>
  These examples assume the ROM file name is: `ActRaiser (USA).sfc`
* To see the randomizer's own usage text:
   * `py actraiser_randomizer.py -h`
* To generate a randomized ROM with no particular settings:
   * `py actraiser_randomizer.py "ActRaiser (USA).sfc"`
   * This will generate a randomized ROM named: `ActRaiser (USA)_SEED.sfc`
* To generate a randomized ROM from a specific seed, use `-s SEED`
   * Valid seed values are 0 to 4294967295 (= 0 to 2<sup>32</sup> - 1).
   * Values outside that range will be mapped into that range via modulus.
   * Sample run:
     ```
     py actraiser_randomizer.py -s 3816547290 "ActRaiser (USA).sfc"

     RNG seed: 3816547290
     Seed hash: 465E42D7
     Randomizer flags: -
     ```
* To mask the seed in the resulting ROM (i.e. for a race seed, to prevent cheating), use `-m`
   * Sample run:
     ```
     py actraiser_randomizer.py -s 3816547290 -m "ActRaiser (USA).sfc"

     RNG seed: (masked)
     Seed hash: 465E42D7
     Randomizer flags: -
     ```
* To view the spoiler log for the resulting ROM, use `-v`
   * Note that if you've masked the seed with `-m`, the spoiler log will include the unmasked seed.
   * Sample run:
     ```
     py actraiser_randomizer.py -s 3816547290 -v "ActRaiser (USA).sfc"

     RNG seed: 3816547290
     Seed hash: 465E42D7
     Randomizer flags: -
     ---------------------------------------
     Marahna II path: right
     Boss rush type: scattered
     406 204 208 301 202 502 504 704 702 102
     608 402 206 603 503 205 708 104 103 306
     304 401 207 601 705 303 101 407 707 508
     505 607 605 606 706 203 405 403 604 501
     703 305 302 404 201 701 507 602
     ---------------------------------------
     ```
* To perform a dry-run (do all the randomization, but don't generate a new ROM), use `-n`
   * This can be useful with `-s` and `-v` to preview the outcome for a given seed.
   * In dry-run mode, the ROM file name is optional and can be omitted.
* To start with 10 lives instead of 5, use `-E`
* To play with unlimited lives, use `-U`
* To show a death count instead of lives remaining, use `-D`
* To play with a permanent sword upgrade, use `-Z`
* To force a particular path in Marahna II, use `-L` (left) or `-R` (right)
* To force a boss rush type, use `-C` (consecutive) or `-S` (scattered)
* To specify the generated ROM's file name, use `-o OUTPUT_FILE_NAME`

## Gameplay
* If everything worked correctly, the title screen will show the seed (or masked seed) and flags used.
* The "descending ball of light brings statue to life" animation no longer happens.<br/>
  (With some starting rooms, it caused the player to take unavoidable damage.)
* There is now a room counter in the upper-left corner, where "[ACT]" would normally be.<br/>
  You start in room 01, and the credits roll after you exit room 48.
