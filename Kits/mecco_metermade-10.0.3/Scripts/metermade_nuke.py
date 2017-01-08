#python

import sys, metermade

lx.eval('dialog.setup yesNo')
lx.eval('dialog.title {Metermade: The Nuclear Option}')
lx.eval('dialog.msg {All dimensions will be permanently deleted. Are you sure?}')
try:
    lx.eval('dialog.open')
    result = lx.eval('dialog.result ?')
except:
    lx.out('user aborted')
    sys.exit()

lx.eval("select.drop item")
metermade.select_mm_group()
lx.eval('delete')