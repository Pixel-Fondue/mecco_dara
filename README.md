# mecco_dara

Dara is a MODO kit of MODO kits. Its sole purpose is to simplify the download and installation of its member kits. It was originally developed by Mechanical Color LLC as a proprietary paid product, and is now released as open-source under the MIT license.

**Note**: Download the latest zip file [here](https://github.com/pixelfondue/mecco_dara/releases/latest) to install. This repository does _not_ contain all of the Dara member kits. 

Instead, this repository contains a Python script for cloning and assembling the kits into a given release of Dara. You'll have to enter your github username and password the first time you run the script. (Note that an obfuscated version of the login credentials will be saved in a gitignored location in the repo for convenience.) The script will then loop through each Dara kit and clone it into a gitignored "wip" directory for your coding pleasure, then zip it up into a single release in another gitignored "releases" directory. (I found this much easier to manage than submodules.)

If you would prefer to install the kits individually, get them [here](https://github.com/pixelfondue).
