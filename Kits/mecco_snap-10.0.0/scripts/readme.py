#python

#by Alex

import readmeUtil
import snapUtil

readmeEntry = snapUtil.quickUserValue('snapLog_tmp','string','Readme Entry','This is an awesome scene, meant to create awesome images.')

if not readmeEntry:
	readmeEntry = '(blank log entry)'
	
readmeUtil.readme(readmeEntry)