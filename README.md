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
1. You will need a [Raf Manager](http://www.itzwarty.com/raf/)
2. Using Raf Manager extract all folders with RAF path `Menu/HUD/Hud2012/Elements` from all versions that contain in (use built-in search function to find term 'Hud2012' and extract underlying 'Elements' folder). I suspect extracting from the oldest version to the most recent one make sense in case Riot introduced a newer version of any of the files at some point
3. Raf Manager will build a full directory structure, something like `DATA/Menu/HUD/Hud2012/Elements`
4. Execute the HUD fixer (default will work for 3x1920 screen setup, see section Configuration below)

        hudfixer.py path_to_mod/DATA/Menu/HUD/Hud2012/Elements/*

5. HUD fixer will create folder `processed` where modified *.ini files will be placed
6. Copy all files from `processed` folder to `path_to_mod/DATA/Menu/HUD/Hud2012/Elements/` overrding existing files
7. Use folder `path_to_mod` as a mod in Raf Manager (you can just drag-n-drop the folder and give a mod a name). Remember to enable it and to run file->pack to apply the mod.
8. That's it, start the game and you should see your HUD realigned on the central monitor. If it's slightly mispositioned go to LOL options and choose 'reset HUD' option, for details see `known issues` below

Configuration
-------------

I've only tested this on a 3-screen eyefinity with total resolution of 1920x1080, however this should work with different setups with little tweak. If your screens has different resolution thant 1920 you can edit `hudfxier.py` and change the value of `TARGET_RESOLUTION` in the top section of the file. This **might** work, let me know!

Known Issues
------------

**Scaling doesn't work very well**. Because we now anchor HUD elements centrally, scaling the HUD will result in slightly oddly positioned interface. You probably want to stick with the default HUD/Minimap scale (there is a 'Reset HUD' option in LOL).

**Chat window is not repositioned**. Currently it's untouched but I suspect it's a matter of finding the right `.ini` file. I don't care too much, there are way too many trolls in LOL for me to bother with the chat.

**Win/Loss screens and tooltips are still broken.** Yepp, that means quitting the game with alt+f4 and having to live with oversized tooltips. I might look into this in future

License
-------
HUD Fixer is open source software released under the MIT License (MIT)

Copyright (c) 2013 Tom Najdek


