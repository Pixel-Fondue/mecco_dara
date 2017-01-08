#python

#by Adam

import snapUtil

logEntry = snapUtil.quickUserValue('snapLog_tmp','string','Log Entry','Made it more awesomer.')

if not logEntry:
	logEntry = '(blank log entry)'
	
snapUtil.snap(logEntry)