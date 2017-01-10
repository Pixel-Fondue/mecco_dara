#python

#by Alex

import snapUtil
import lx
import re
import os
import sys
import time
from inspect import currentframe, getframeinfo

def readmeName(suffix='readme'):
	return snapUtil.sceneName() + '_' + suffix + '.txt'
	
def readmePath():
	readmePath = os.path.join(snapUtil.filePath(), readmeName())
	if isinstance(readmePath, basestring):
		return readmePath
	else:
		return False
	
def readmeWrite(entry='generic', stamp=False):
	if snapUtil.fileLoc():
		if not os.path.isfile(readmePath()):
			header = "# " + snapUtil.sceneName() + " Read Me"
		else:
			header = ""
		readme = open(readmePath(), 'a')
		if not stamp:
			stamp = time.strftime("%Y/%m/%d - %H:%M:%S")
			stamp = "\n\n## " + stamp + "\n\n"
		if entry:
			readme.write('%s %s %s\n' % (header, stamp, entry))
		lx.out('readme entry: "%s"' % entry)
		return True
	else:
		return False
	
def readme(readmeEntry=False):
	snapUtil.debug('getting started...')
	if not snapUtil.fileLoc():
		snapUtil.initialSave()

	snapUtil.debug('attempting to save readme...')
	try:
		if readmeEntry:
			readmeWrite(readmeEntry)
	except:
		snapUtil.errorDialog('Unable to save readme "%s". Nothing was saved.' % readmePath())