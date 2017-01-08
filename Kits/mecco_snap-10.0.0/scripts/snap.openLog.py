#python

import snapUtil
import os

logPath = snapUtil.logPath()

if logPath:
	if os.path.isfile(logPath):
		lx.eval('file.open {%s}' % logPath)
	else:
		snapUtil.errorDialog('No log file exists.')
else:
	snapUtil.errorDialog('Something\'s gone terribly wrong.')