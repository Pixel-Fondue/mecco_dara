#python

import lx, lxu, modo, tagger, traceback

CMD_NAME = tagger.CMD_PTAG_INSPECT

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):
        tags = {
            tagger.MATERIAL:set(),
            tagger.PART:set(),
            tagger.PICK:set()
        }

        for layer in tagger.items.get_active_layers():
            with layer.geometry as geo:
                polys = geo.polygons.selected

                for p in polys:
                    if p.tags()[tagger.MATERIAL]:
                        tags[tagger.MATERIAL].add(p.tags()[tagger.MATERIAL])
                    if p.tags()[tagger.PART]:
                        tags[tagger.PART].add(p.tags()[tagger.PART])
                    if p.tags()[tagger.PICK]:
                        tags[tagger.PICK] = tags[tagger.PICK].union(set(p.tags()[tagger.PICK].split(";")))

        output = ""
        for tagType in tags:
            output += tagType + ": "
            if tags[tagType]:
                output += ", ".join(tags[tagType]) + "\n"
            else:
                output += tagger.LABEL_NONE + "\n"

        modo.dialogs.alert(tagger.LABEL_TAGS, output)

lx.bless(CommandClass, CMD_NAME)
