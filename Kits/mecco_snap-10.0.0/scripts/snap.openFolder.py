#python

import snapUtil

if not snapUtil.snapsPathExists():
	snapUtil.errorDialog('No snaps folder exists for this scene.')
else:
	lx.eval('file.open {%s}' % snapUtil.snapsPath())