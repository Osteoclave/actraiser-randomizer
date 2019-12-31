# actraiser-randomizer
Randomizer for ActRaiser's Professional Mode

## Getting Started
1. Check if you have Python 3 installed.
   * Open a command prompt and type:  
     * `python3 --version`  
   * If you get back a version string, you should be good to go. If not, [download and install Python 3](https://www.python.org/downloads/).
1. Click the "Clone or download" button at the upper right of this repository page, then "Download ZIP".
1. Extract the ZIP archive's contents to a convenient directory.
1. Copy an ActRaiser (USA) ROM into the directory from the previous step.
1. **Optional:** Validate your ActRaiser (USA) ROM.
   * The ROM should be 1,048,576 bytes long.
     * If your ROM is 1,049,088 bytes long, it has a 512-byte copier header at the start.
       You can remove the copier header with NSRT ([Windows](https://www.romhacking.net/utilities/400/),
       [Mac](https://www.romhacking.net/utilities/484/), [Linux](https://www.romhacking.net/utilities/401/)).
   * The ROM should have the following checksums:
     ```
     CRC32: EAC3358D
       MD5: 635D5D7DD2AAD4768412FBAE4A32FD6E
     SHA-1: E8365852CC20178D42C93CD188A7AE9AF45369D7
     ```

## Usage
* Open a command prompt and navigate to the directory with the randomizer files and ActRaiser (USA) ROM.  
  These examples assume the ROM file name is: `ActRaiser (USA).sfc`
* To see the randomizer's own usage text:
  * `python3 actraiser_randomizer.py -h`
* To generate a randomized ROM with no particular settings:
  * `python3 actraiser_randomizer.py "ActRaiser (USA).sfc"`
    * This will generate a randomized ROM named: `ActRaiser (USA)_SEED.sfc`
* To generate a randomized ROM from a specific seed (here, 3816547290):
  * `python3 actraiser_randomizer.py -s 3816547290 "ActRaiser (USA).sfc"`
    * Valid seed values are 0-4294967295. Values outside that range will be mapped into that range via modulus.
* To view a spoiler log when generating the randomized ROM, use `-v`:
  ```
  python3 actraiser_randomizer.py -s 3816547290 -v "ActRaiser (USA).sfc"
  
  RNG seed: 3816547290
  Randomizer flags: -
  Marahna II path: right
  607 604 504 103 605 304 601 102 205 303 
  206 202 401 505 204 101 405 501 608 503 
  406 203 508 402 407 708 705 707 706 704 
  703 702 701 104 208 207 403 306 301 603 
  305 302 404 201 606 507 602 502
  ```
* To perform a dry-run (do all the randomization, but don't generate a new ROM), use `-n`.
  * This can be useful with `-s` and `-v` to preview the outcome for a given seed.
  * In dry-run mode, the ROM file name is optional and can be omitted.
* To force a particular path in Marahna II, use `-L` (left) or `-R` (right).
* To keep the boss rush at the end, use `-B`.
* To ensure Tanzra is the last boss in the boss rush, use `-T`.
* To specify the generated ROM's file name, use `-o OUTPUT_FILE_NAME`.

## Gameplay
* If everything worked correctly, the "START" option on the title screen will include the seed and flags used.
* The "descending ball of light brings statue to life" animation no longer happens.  
  (With some starting rooms, it caused the player to take unavoidable damage.)
* There is now a room counter in the upper-left corner, where "[ACT]" would normally be.  
  You start in room 01, and the credits roll after you exit room 48.
