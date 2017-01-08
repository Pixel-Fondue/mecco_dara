#python

import lx, lxu, modo, traceback

DEBUG = True

try:
    import presets
    import items
    import shadertree
    import selection
    import scene
    import colors
    from var import *
    from util import *
    from debug import *
    from notifier import *
    from commander import *
    from PopupClass import *
    from PolysConnectedByTag import *
    from PolysByIsland import *
except:
    traceback.print_exc()
