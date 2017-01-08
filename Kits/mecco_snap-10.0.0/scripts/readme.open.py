#python

#by Alex

import snapUtil
import readmeUtil
import os

readmePath = readmeUtil.readmePath()

if readmePath:
	if os.path.isfile(readmePath):
		lx.eval('file.open {%s}' % readmePath)
	else:
		snapUtil.errorDialog('No log file exists.')
else:
	snapUtil.errorDialog('Something\'s gone terribly wrong.')