
import lx, modo, lxifc, lxu.command, tagger

CMD_NAME = tagger.CMD_SHADERTREE_CONSOLIDATE_BY_COLOR

def color_convert(color):
    return [i*256 for i in color]

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_execute(self, msg, flags):
        all_masks = modo.Scene().items('mask')
        target_masks = []
        unique_colors = set()
        consolidation_masks = []

        for mask in all_masks:
            if mask.parent.id != modo.Scene().renderItem.id:
                continue
            if mask.channel(lx.symbol.sICHAN_MASK_PTYP).get() not in ('Material', ''):
                continue
            if len(mask.children()) != 1:
                continue
            material = mask.children()[0]
            if material.type != 'advancedMaterial':
                continue

            target_masks.append({"mask_item": mask})
            target_masks[-1]["material_item"] = material
            target_masks[-1]["color"] = material.channel('diffCol').get()
            target_masks[-1]["pTag"] = target_masks[-1]["mask_item"].channel(lx.symbol.sICHAN_MASK_PTAG).get()

            unique_colors.add(target_masks[-1]["color"])

        for c in unique_colors:
            consolidation_masks.append({"color": c})
            consolidation_masks[-1]["colorname"] = tagger.colors.ColorNames.findNearestWebColorName(color_convert(c))
            consolidation_masks[-1]["hitlist"] = [m for m in target_masks if m["color"] == c]

        for c in consolidation_masks:
            c["pTag"] = c["colorname"]

            all_existing_tags = tagger.scene.all_tags_by_type(lx.symbol.i_POLYTAG_MATERIAL)
            n = 0
            while c["pTag"] in all_existing_tags:
                n += 1
                c["pTag"] = "_".join((c["colorname"], str(n)))

            c["consolidation_mask"] = tagger.shadertree.build_material(pTag = c["pTag"])
            c["consolidation_mask"].children()[0].channel('diffCol').set(c["color"])

            for hit in c["hitlist"]:
                tagger.safe_removeItems([hit["mask_item"]], True)
                lx.eval('!material.reassign {%s} %s' % (hit["pTag"], c["pTag"]))



lx.bless(CommandClass, CMD_NAME)
