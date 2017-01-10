# python

import lx, lxifc, lxu.command, modo, tagger, random

CMD_NAME = tagger.CMD_PTAG_SELECTION_FCL

global_tags = None
global_poly_count = 0

def list_commands():
    timer = tagger.DebugTimer()

    global global_tags
    global global_poly_count

    fcl = []

    global_tags = [
        set(),
        set(),
        set()
    ]

    global_poly_count = 0

    mesh_editor = MeshEditorClass()
    mesh_read_successful = mesh_editor.do_mesh_read()

    selmode = tagger.selection.get_mode()

    if global_poly_count == 0 or selmode not in ['polygon', 'edge', 'vertex']:
        fcl.append("%s {%s}" % (tagger.CMD_NOOP, tagger.LABEL_NO_POLYS))

        timer.end()
        return fcl

    elif global_poly_count > tagger.MAX_FCL_POLY_INSPECT:
        fcl.append("%s {%s}" % (tagger.CMD_NOOP, tagger.LABEL_MAX_POLY))

        timer.end()
        return fcl

    if sum([len(tags) for tags in global_tags]) == 0:
        fcl.append("%s {%s}" % (tagger.CMD_NOOP, tagger.LABEL_NO_TAGS))

        timer.end()
        return fcl

    if len(global_tags) > tagger.MAX_FCL:
        fcl.append("%s {%s}" % (tagger.CMD_NOOP, tagger.LABEL_MAX_FCL))

        timer.end()
        return fcl

    for n in range(len(global_tags)):
        if not global_tags[n]:
            continue

        for tag in sorted(global_tags[n]):
            tagType = [tagger.MATERIAL, tagger.PART, tagger.PICK][n]

            if tagType == tagger.MATERIAL:
                command = tagger.CMD_SELECT_ALL_BY_MATERIAL
            elif tagType == tagger.PART:
                command = tagger.CMD_SELECT_ALL_BY_PART
            elif tagType == tagger.PICK:
                command = tagger.CMD_SELECT_ALL_BY_SET

            fcl.append("%s {%s}" % (command, tag))

    timer.end()
    return fcl


class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': tagger.QUERY,
                    'label': tagger.LABEL_QUERY,
                    'datatype': 'integer',
                    'value': '',
                    'fcl': list_commands,
                    'flags': ['query'],
                }
            ]

    def commander_notifiers(self):
        return [("select.event", "polygon +ldt"),("select.event", "item +ldt"), ("tagger.notifier", "")]


lx.bless(CommandClass, CMD_NAME)


class MeshEditorClass(tagger.MeshEditorClass):

    def mesh_read_action(self):
        global global_tags
        global global_poly_count

        stringTag = lx.object.StringTag()
        stringTag.set(self.polygon_accessor)

        selected_polys = self.get_selected_polys()

        for poly in selected_polys:
            global_poly_count += 1

            if global_poly_count > tagger.MAX_FCL_POLY_INSPECT:
                break

            self.polygon_accessor.Select(poly)

            material = stringTag.Get(lx.symbol.i_POLYTAG_MATERIAL)
            if material:
                global_tags[0].add(material)

            part = stringTag.Get(lx.symbol.i_POLYTAG_PART)
            if part:
                global_tags[1].add(part)

            pick = stringTag.Get(lx.symbol.i_POLYTAG_PICK)
            if pick:
                global_tags[2].update(pick.split(";"))
