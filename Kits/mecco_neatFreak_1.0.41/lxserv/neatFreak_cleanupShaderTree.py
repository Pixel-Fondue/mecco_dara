#python

import lx, lxu, modo, traceback

NAME_CMD = 'neatFreak.cleanupShaderTree'


def get_layers_by_pTag(pTags,i_POLYTAG=lx.symbol.i_POLYTAG_MATERIAL):
    """Returns a list of all mesh layers containing any of the provided pTag(s)
    of type i_POLYTAG, e.g. lx.symbol.i_POLYTAG_MATERIAL.
    """

    if not isinstance(pTags,list):
        pTags = [pTags]

    scene = modo.Scene()

    mm = set()
    for m in scene.meshes:
        for i in range(m.geometry.internalMesh.PTagCount(i_POLYTAG)):
            tag = m.geometry.internalMesh.PTagByIndex(i_POLYTAG,i)
            if i_POLYTAG == lx.symbol.i_POLYTAG_PICK:
                if [i for i in tag.split(";") if i in pTags]:
                    mm.add(m)
            else:
                if tag in pTags:
                    mm.add(m)

    return list(mm)


def get_i_POLYTAG(sICHAN_MASK_PTYP):
    """Returns an lx.symbol.i_POLYTAG_* symbol based on a mask
    item's lx.symbol.sICHAN_MASK_PTYP channel string."""

    return {
        '':lx.symbol.i_POLYTAG_MATERIAL,
        'Material':lx.symbol.i_POLYTAG_MATERIAL,
        'Selection Set':lx.symbol.i_POLYTAG_PICK,
        'Part':lx.symbol.i_POLYTAG_PART
    }[sICHAN_MASK_PTYP]


class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('del_empty', lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add('del_unused', lx.symbol.sTYPE_BOOLEAN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label("Delete empty groups")
        if index == 1:
            hints.Label("Delete unused groups")

    def cmd_DialogInit(self):
        if self._first_run:
            self.attr_SetInt(0, 1)
            self.attr_SetInt(1, 1)
            self.after_first_run()

    @classmethod
    def after_first_run(cls):
        cls._first_run = False

    def basic_Execute(self, msg, flags):
        try:
            scene = modo.scene.current()

            hitlist = set()
            for m in scene.iterItems(lx.symbol.sITYPE_MASK):
                del_empty = self.dyna_String(0) if self.dyna_IsSet(0) else True
                del_unused = self.dyna_String(1) if self.dyna_IsSet(1) else True

                # delete empty groups
                if not m.children() and del_empty:
                    hitlist.add(m)

                if del_unused:
                    # type of poly tag (material, selection set, etc)
                    i_POLYTAG = get_i_POLYTAG(m.channel(lx.symbol.sICHAN_MASK_PTYP).get())

                    # poly tag ("myGreatMaterialTag")
                    sICHAN_MASK_PTAG = m.channel(lx.symbol.sICHAN_MASK_PTAG).get()

                    # delete obsolete (unused) polytag groups
                    if (sICHAN_MASK_PTAG and not get_layers_by_pTag(sICHAN_MASK_PTAG,i_POLYTAG)):
                        hitlist.add(m)

            for hit in hitlist:
                # TD SDK removeItems() method crashes on some groups. This is more robust.
                lx.eval("item.delete item:{%s}" % hit.id)

        except:
            traceback.print_exc()

lx.bless(CMD_neatFreak, NAME_CMD)
