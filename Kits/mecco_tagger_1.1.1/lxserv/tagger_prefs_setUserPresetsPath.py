#python

import lx, lxu, modo, tagger, traceback

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):
        target = modo.dialogs.dirBrowse(tagger.LABEL_CHOOSE_FOLDER)
        lx.eval('user.value mecco_tagger.userPresetsPath {%s}' % target)

lx.bless(CommandClass, tagger.CMD_PREFS_SET_USER_PRESETS_PATH)
