# python

import lx, lxifc, lxu, modo
import tagger
from os import listdir, sep
from os.path import isfile, join, basename, splitext, dirname

CMD_NAME = tagger.CMD_SET_PTAG_REMOVE

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.TAGTYPE,
                    'label': tagger.LABEL_TAGTYPE,
                    'datatype': 'string',
                    'value': tagger.MATERIAL,
                    'popup': tagger.POPUPS_TAGTYPES,
                    'flags': ['optional']
                }, {
                    'name': tagger.REMOVE_SCOPE,
                    'label': tagger.LABEL_REMOVE_SCOPE,
                    'datatype': 'string',
                    'value': tagger.SCOPE_SELECTED,
                    'flags': ['optional'],
                    'sPresetText': tagger.POPUPS_REMOVE_SCOPE
                }, {
                    'name': tagger.DELETE_UNUSED_MASKS,
                    'label': tagger.LABEL_DELETE_UNUSED_MASKS,
                    'datatype': 'boolean',
                    'value': True,
                    'popup': tagger.POPUPS_SCOPE,
                    'flags': ['optional']
                }
            ]

    def commander_execute(self, msg, flags):
        tagType = self.commander_arg_value(0, tagger.MATERIAL)
        scope = self.commander_arg_value(1, tagger.SCOPE_SELECTED)
        delete_unused = self.commander_arg_value(2, True)

        i_POLYTAG = tagger.convert_to_iPOLYTAG(tagType)
        pTags_to_remove = tagger.selection.get_ptags(i_POLYTAG)

        # if we're just nixing tags in a selection, easy.
        if scope in [tagger.SCOPE_SELECTED, tagger.SCOPE_CONNECTED, tagger.SCOPE_FLOOD]:
            args = tagger.build_arg_string({
                tagger.TAGTYPE: tagType,
                tagger.TAG: "",
                tagger.SCOPE: scope
            })
            lx.eval("!" + tagger.CMD_PTAG_SET + args)

        # if we want to nix tags for the whole scene, do some work.
        if scope == tagger.SCOPE_SCENE:
            for  pTag in pTags_to_remove:
                lx.eval("%s %s %s {}" % (tagger.CMD_PTAG_REPLACE, tagType, pTag))

        # see if we need to delete any masks in the shader tree
        if not delete_unused:
            return

        mask_tags_to_destroy = set()
        for pTag in pTags_to_remove:
            if not tagger.scene.meshes_with_pTag(pTag, i_POLYTAG):
                tagger.shadertree.seek_and_destroy(pTags={pTag:i_POLYTAG})

        notifier = tagger.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

lx.bless(CommandClass, CMD_NAME)
