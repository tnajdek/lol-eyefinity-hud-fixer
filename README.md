Leauge of Legends HUD Fixer for Eyefinity setup
=======================
This little python script can help you get your HUD in LOL fixed if you're playing on multiple screens using AMD's eyefinity (or NVIDIA's Vision Surround most likely!)

By default many HUD elements like the Minimap and Character's status are anchored to either left or right hand side of the screen. This works well for single-screen setups but is very inconvienient when playing on 3 or 5 screens placed side-by-side. This script will allow you to anchor these HUD elements centrally, keeping them all on the central screen.

Prerequests
-----------

* Python 2.7
* Raf Manager to parse and pack raf files (see below)

Simplified Guide
------------------

0. Backup your LOL folder in case something goes wrong.
1. You will need a [Rafiki](https://github.com/tnajdek/rafiki)
2. Using Rafiki extract all folders with RAF path **DATA/Menu/HUD/Elements** (see README.md in Rafiki repo for details how to do it)
3. Execute the HUD fixer

        hudfixer.py -i -r 1920 -s path_to_extracted_files

5. HUD fixer will convert extracted files inline, changing values so that all HUD elements are located on the center screen
6. Use Rafiki again to pack modified files back to **raf**
7. Copy created raf files to **$LOL_PATH/Contents/LoL/RADS/projects/lol_game_client/filearchives/** (where $LOL_PATH represents path to Leauge of Legends)
8. That's it, start the game and you should see your HUD realigned on the central monitor. If it's slightly mispositioned go to LOL options and choose 'reset HUD' option, for details see `known issues` below

Configuration
-------------

I've only tested this on a 3-screen eyefinity with total resolution of 1920x1080, however this should work with different setups such as 5 or 7 screens side-by-side. For different screen resolutions modify the value of -r argument.

Known Issues
------------

**Scaling doesn't work very well**. Because we now anchor HUD elements centrally, scaling the HUD will result in slightly oddly positioned interface. You probably want to stick with the default HUD/Minimap scale (there is a 'Reset HUD' option in LOL).

**Chat window is not repositioned**. Currently it's untouched but I suspect it's a matter of finding the right `.ini` file. I don't care too much, there are way too many trolls in LOL for me to bother with the chat.

**Win/Loss screens and tooltips are still broken.** Yepp, that means quitting the game with alt+f4 and having to live with oversized tooltips. I might look into this in future

License
-------
HUD Fixer is open source software released under the MIT License (MIT)

Copyright (c) 2013 Tom Najdek


