# python

import modo

lx.eval('!cmds.mapKey ctrl-s scene.save .global (stateless) .anywhere')
lx.eval('!cmds.clearKey ctrl-alt-s .global (stateless) .anywhere')

modo.dialogs.alert("Unmapped Snap Hotkeys", "Reset ctrl + S and cleared mapping for ctrl + alt + S. Enjoy.")
