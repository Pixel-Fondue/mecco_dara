#python

import lx
import re
import os
import sys
import time
from inspect import currentframe, getframeinfo

SNAPTIME = time.strftime("%Y%m%d-%H%M%S")

def quickSnapMax():
    return lx.eval('user.value mecco_snap.quickSnapMax ?')


def listSnaps():
    if snapsPathExists():
        snapsList = [f for f in os.listdir(snapsPath()) if
                     (os.path.isfile(os.path.join(snapsPath(), f))) and ('.lxo' in f.lower())]
        if isinstance(snapsList, list):
            return snapsList
        else:
            return False
    else:
        errorDialog('Could not find a snaps folder for this file.')
        return False


def purgeQuickSnaps():
    if quickSnapMax():
        regex = ['q\.lxo$', '^(?:%s)' % sceneName()]
        snaps = [f for f in listSnaps() if re.search(regex[0], f.lower()) and re.search(regex[1], f)]
        if isinstance(snaps, list) and len(snaps) > quickSnapMax():
            lx.out('Purging quick snaps:')
            i = 0
            while (i < len(snaps)) and (len(snaps) - i > quickSnapMax()):
                os.remove(os.path.join(snapsPath(), snaps[i]))
                if debugMode():
                    log('deleted %s' % snaps[i], 'purgeQuickSnaps()')
                i += 1
        else:
            lx.out('No quick snaps to purge.')


def errorDialog(msg="I've made a huge mistake.", title="error"):
    lx.eval('dialog.setup error')
    lx.eval('dialog.title {%s}' % title)
    lx.eval('dialog.msg {%s}' % msg)
    lx.out("%s: %s" % (title, msg))
    log('%s - %s' % (title, msg))
    lx.eval('dialog.open')
    sys.exit()


def debugMode():
    if lx.eval('user.value mecco_snap.debug ?'):
        return True
    else:
        return False


def debug(msg='okay so far...'):
    if debugMode():
        frame = currentframe()
        frameinfo = getframeinfo(frame.f_back)
        filename = basename(frameinfo.filename)
        line = frameinfo.lineno
        try:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {debug}')
            lx.eval('dialog.msg {%s line %s: %s}' % (filename, line, msg))
            lx.out('%s: %s' % ('debug', msg))
            lx.eval('dialog.open')
            return True
        except:
            return False


def projectPath():
    project = lx.eval('query platformservice alias ? {project:}')
    if os.path.isdir(project):
        return project
    else:
        return False


def pathname(string):
    pathname = re.findall('^.*[\/\\\]', string)
    try:
        return pathname[0]
    except:
        lx.out('Pathname for "%s" could not be parsed. Abort.' % string)
        sys.exit()


def basename(string):
    basename = re.sub('^.*[\/\\\]', '', string);
    lx.out('basename: ' + basename);
    return basename;


def fileLoc():
    return lx.eval('query sceneservice scene.file ? current')


def fileName():
    return lx.eval('query sceneservice scene.name ? current')


def filePath():
    filePath = lx.eval('query sceneservice scene.file ? current')

    if filePath:
        return pathname(filePath)
    else:
        return False


def initialSave():
    try:
        tagScene(snapTime() + ' - initial save')
        lx.eval('scene.save')
        return lx.eval('query sceneservice scene.file ? current')
    except:
        lx.out('user aborted save')
        return False


def sceneName():
    return re.sub('\..*', '', fileName())

def isProject():
    if projectPath() and lx.eval('user.value mecco_snap.projectSnaps ?'):
        return True
    else:
        return False

def snapsDirName():
    if isProject():
        return os.path.join('Snaps', sceneName())
    else:
        return sceneName() + '_snaps'

def snapsBasePath():
    if isProject():
        return projectPath()
    else:
        return filePath()

def snapsPath():
    return os.path.join(snapsBasePath(), snapsDirName())

def snapsPathExists():
    if os.path.isdir(snapsPath()) == 0:
        return False
    else:
        return True


def snapTime():
    return SNAPTIME


def snapName(suffix=''):
    return sceneName() + '_' + snapTime() + suffix + '.lxo'


def destPath(suffix=''):
    return os.path.join(snapsPath(), snapName(suffix))


def sceneID():
    # [6/26/14, 9:26:39 PM] Simon Lundberg:
    # 48 is the item type integer for scene items
    import lxu.select

    sceneInterface = lxu.select.SceneSelection().current()
    sceneItem = sceneInterface.ItemByIndex(48, 0)
    return sceneItem.Ident()


def quickUserValue(valHandle, valType='string', nicename='', default=''):
    if lx.eval('query scriptsysservice userValue.isDefined ? %s' % valHandle) == 0:
        lx.eval('user.defNew %s %s' % (valHandle, valType))

    try:
        lx.eval('user.def %s username {%s}' % (valHandle, nicename))
        lx.out('user.def %s type %s' % (valHandle, valType))
        lx.eval('user.def %s type %s' % (valHandle, valType))
        lx.eval('user.value %s {%s}' % (valHandle, default))
        lx.eval('user.value %s' % valHandle)
        return lx.eval('user.value %s value:?' % valHandle)
    except:
        return False


def logPath():
    logPath = os.path.join(snapsPath(), 'snapLog.txt')
    if isinstance(logPath, basestring):
        return logPath
    else:
        return False


def log(entry='generic', stamp=False):
    if snapsPathExists():
        log = open(logPath(), 'a')
        if not stamp:
            stamp = time.strftime("%Y/%m/%d - %H:%M:%S")
        if entry:
            log.write('%s: %s\n' % ( stamp, entry))
        else:
            log.write('%s: %s\n' % ( stamp, '-'))
        lx.out('log entry: "%s"' % entry)
        return True
    else:
        return False


def selection_mode(*types):
    if not types:
        types = ('vertex', 'edge', 'polygon', 'item', 'pivot', 'center', 'ptag')
        for t in types:
            if lx.eval('select.typeFrom %s;vertex;edge;polygon;item;pivot;center;ptag ?' %t):
                return t


def tagScene(tag):
    try:
        curr_sel = selection_mode()
        lx.eval('select.drop item')
        lx.eval('select.item {%s} set' % sceneID())
        lx.eval('item.tag string "Revi:scene" {%s}' % tag)
        lx.eval('select.type %s' % curr_sel)
        return True
    except:
        return False


def createSnapsPath():
    try:
        if not snapsPathExists():
            lx.eval('file.newDir {%s} {%s}' % (snapsDirName(), snapsBasePath()))
        lx.out('created snaps folder "%s"' % snapsDirName())
    except:
        errorDialog('Folder "%s" does not exist and could not be created. Nothing was saved.' % snapsDirName())


def snap(logEntry=False):
    debug('getting started...')
    if not fileLoc():
        initialSave()

    debug('checking if quick snap')
    quickFlag = 'q' if logEntry is False else ''

    debug('tagging file...')
    if not tagScene(snapTime()):
        errorDialog('Could not add timecode to "Ravi:scene" tag for "%s". Nothing was saved.' % sceneID())

    if not snapsPathExists():
        debug('creating snaps dir...')
        createSnapsPath()

    debug('attempting to save snap...')
    try:
        lx.eval('scene.saveAs {%s} export:1' % destPath(quickFlag))
        lx.out('saved snap: %s' % destPath(quickFlag))
        if logEntry:
            log(logEntry, snapName(quickFlag))
        elif logEntry == False and debugMode() == True:
            log('(quick snap)', snapName(quickFlag))
    except:
        errorDialog('Unable to save snap "%s". Nothing was saved.' % snapName(quickFlag))

    debug('attempting to save current...')
    try:
        lx.eval('scene.save')
        lx.out('saved current: %s' % fileLoc())
    except:
        errorDialog('Snap was saved successfully to "%s", but current scene could not be saved.' % snapName())

    debug('purging quick snaps...')
    purgeQuickSnaps()
