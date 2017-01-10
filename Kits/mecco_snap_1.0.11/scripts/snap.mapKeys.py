# python

import modo

lx.eval('!cmds.mapKey ctrl-s @snap.noLog.py .global (stateless) .anywhere')
lx.eval('!cmds.mapKey ctrl-alt-s @snap.py .global (stateless) .anywhere')

modo.dialogs.alert("Mapped Snap Hotkeys", "Set ctrl + S to Quick Snap and ctrl + alt + S to Log Snap. Safety first. Have a nice day.")
