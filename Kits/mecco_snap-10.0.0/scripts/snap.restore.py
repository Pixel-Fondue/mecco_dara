#python

import snapUtil, os

if snapUtil.snapsPathExists():

	targetFilePath = snapUtil.fileLoc()

	lx.eval('dialog.setup style:fileOpen')
	lx.eval('dialog.title {Snap to restore}')
	lx.eval('dialog.fileTypeCustom {lxo} {Luxology Scene} {*.lxo} lxo')
	
	# The dialog won't actually grab the snapLog.txt since the file type is LXO,
	# we just use the txt file as a known handle for grabbing the snaps directory.
	lx.eval('dialog.result {%s}' % os.path.join(snapUtil.logPath()))
	try: 
		lx.eval('dialog.open')
		restoreFilePath = lx.eval('dialog.result ?')
	except:
		lx.out('user aborted')
		sys.exit()

	restoreFileName = snapUtil.basename(restoreFilePath)

	lx.eval('dialog.setup style:yesNo')
	lx.eval('dialog.title {Are you sure?}')
	lx.eval('dialog.msg {"%s" will be replaced with "%s". Continue?}' % (snapUtil.fileName(),restoreFileName))
	try:
		lx.eval('dialog.open')
		result = lx.eval('dialog.result ?')
	except:
		lx.out('user aborted')
		sys.exit()

	snapUtil.snap('[Backup before restoring "%s" to current.]' % restoreFileName)

	try:
		lx.eval('scene.close')
		lx.eval('scene.open {%s}' % restoreFilePath)
		lx.eval('scene.saveAs {%s}' % targetFilePath)
	except:
		snapUtil.errorDialog('Something went wrong restoring "%s".' % restoreFileName)

	snapUtil.log('["%s" successfully restored to current.]' % restoreFileName)
	
else:
	
	snapUtil.errorDialog('No snaps directory found for this file.')