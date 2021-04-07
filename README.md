# actraiser-randomizer
Randomizer for ActRaiser's Professional Mode

## Getting Started
1. Check if you have Python installed.
   * Open a command prompt and type:
      * `python --version`
   * If that doesn't work, try:
      * `python3 --version`
   * If you get back a Python 3.x version string (e.g. `Python 3.9.2`), you should be good to go.
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
     ```

## Usage
* Open a command prompt and navigate to the directory with the randomizer files and ActRaiser (USA) ROM.<br/>
  These examples assume the ROM file name is: `ActRaiser (USA).sfc`
* To see the randomizer's own usage text:
   * `python actraiser_randomizer.py -h`
* To generate a randomized ROM with no particular settings:
   * `python actraiser_randomizer.py "ActRaiser (USA).sfc"`
   * This will generate a randomized ROM named: `ActRaiser (USA)_SEED.sfc`
* To generate a randomized ROM from a specific seed, use `-s SEED`
   * Valid seed values are 0 to 4294967295 (= 0 to 2<sup>32</sup> - 1).
   * Values outside that range will be mapped into that range via modulus.
   * Sample run:
     ```
     python actraiser_randomizer.py -s 3816547290 "ActRaiser (USA).sfc"

     RNG seed: 3816547290
     Randomizer flags: -
     ```
* To mask the seed in the resulting ROM (i.e. for a race seed, to prevent cheating), use `-m`
   * Sample run:
     ```
     python actraiser_randomizer.py -s 3816547290 -m "ActRaiser (USA).sfc"

     RNG seed (masked): 5E3E6F8B
     Randomizer flags: -
     ```
* To view the spoiler log for the resulting ROM, use `-v`
   * Note that if you've masked the seed with `-m`, the spoiler log will include the unmasked seed.
   * Sample run:
     ```
     python actraiser_randomizer.py -s 3816547290 -v "ActRaiser (USA).sfc"

     RNG seed: 3816547290
     Randomizer flags: -
     Marahna II path: right
     Boss rush position: scattered
     Boss rush order: random
     406 204 208 301 202 502 504 704 702 102
     608 402 206 603 503 205 707 104 103 306
     304 401 207 601 705 303 101 407 706 508
     505 607 605 606 708 203 405 403 604 501
     703 305 302 404 201 701 507 602
     ```
* To perform a dry-run (do all the randomization, but don't generate a new ROM), use `-n`
   * This can be useful with `-s` and `-v` to preview the outcome for a given seed.
   * In dry-run mode, the ROM file name is optional and can be omitted.
* To start with 10 lives instead of 5, use `-E`
* To play with unlimited lives, use `-U`
* To force a particular path in Marahna II, use `-L` (left) or `-R` (right)
* To change the position of the boss rush, use `-P POSITION`
   * `POSITION` can be any one of the following:
      * `vanilla`: The boss rush is consecutive and happens at the end
      * `random`: The boss rush is consecutive and happens at a random location
      * `scattered`: The boss rush is split into individual boss fights and scattered among the other rooms
   * If this option is omitted, the position will be either `random` or `scattered`, based on the seed.
* To change the order of the boss rush, use `-O ORDER`
   * `ORDER` can be any one of the following:
      * `vanilla`: Minotaurus, Zeppelin Wolf, Pharaoh, Fire Wheel, Kalia, Arctic Wyvern, Tanzra
      * `random`: The seven bosses will be fought in a random order
      * `tanzralast`: The first six bosses will be fought in a random order, with Tanzra last
   * If this option is omitted, the order will be `random`.
* To specify the generated ROM's file name, use `-o OUTPUT_FILE_NAME`

## Gameplay
* If everything worked correctly, the title screen will show the seed (or masked seed) and flags used.
* The "descending ball of light brings statue to life" animation no longer happens.<br/>
  (With some starting rooms, it caused the player to take unavoidable damage.)
* There is now a room counter in the upper-left corner, where "[ACT]" would normally be.<br/>
  You start in room 01, and the credits roll after you exit room 48.
