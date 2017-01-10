# python

import lx, lxu, modo

HOTKEYS = [
    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"j",
        "command":"vert.join false"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "layout_zen6_layout"]
        ],
        "key":"ctrl-shift-space",
        "command":"attr.formPopover {ZenPie_Frames:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"alt-backquote",
        "command":"viewport.maximize"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"],
            [".global", "(stateless)", ".anywhere", ".itemMode"]
        ],
        "key":"v",
        "command":"attr.formPopover {31757584531:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"],
            ["IView", "(stateless)", ".anywhere", "(contextless)"],
            ["view3DCamera", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"g",
        "command":"attr.formPopover {zen_palettesPopover:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"q",
        "command":"zen.dropEverything"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"ctrl-r",
        "command":"attr.formPopover {55281439258:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"alt-w",
        "command":"attr.formPopover [ZenPie_Workplane:sheet]"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"alt-x",
        "command":"attr.formPopover {ZenPie_Snapping:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"],
            ["view3DTools", "tool.ink.image", ".anywhere", "(contextless)"]
        ],
        "key":"alt-f",
        "command":"attr.formPopover {ZenPie_Falloff:sheet}"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"alt-a",
        "command":"attr.formPopover {ZenPie_ActionCtr:sheet}"
    },

    {
        "contexts":[
            ["deformerList", "(stateless)", ".anywhere", "(contextless)"],
            ["schematic", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"enter",
        "command":"item.name"
    },

    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)"],
            ["meshList", "(stateless)", ".anywhere", "(contextless)"],
            ["meshList_inline", "(stateless)", ".anywhere", "(contextless)"],
            ["meshList_slot", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"enter",
        "command":"layer.renameSelected"
    },

    {
        "contexts":[
            ["shaderTree", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"enter",
        "command":"texture.name"
    },

    {
        "contexts":[
            ["shaderTree", "(stateless)", ".anywhere", "(contextless)"]
        ],
        "key":"ctrl-d",
        "command":"texture.duplicate"
    },

    {
        "contexts":[
            ["view3DSelect", "(stateless)", "item", "(contextless)"],
            ["shaderTree", "(stateless)", ".anywhere", "(contextless)"],
            ["deformerList", "(stateless)", ".anywhere", "(contextless)"],
            ["schematic", "(stateless)", ".anywhere", "(contextless)"],
            ["meshList", "(stateless)", "meshoperation", "(contextless)"],
            ["meshList", "(stateless)", "deformName", "(contextless)"],
            ["meshList", "(stateless)", "chanEffect", "(contextless)"],
            ["meshList", "(stateless)", "chanModify", "(contextless)"],
            ["meshList", "(stateless)", "itemModify", "(contextless)"],
            ["meshList", "(stateless)", "itemRef", "(contextless)"],
            ["meshList", "(stateless)", "cinemaRef", "(contextless)"],
            ["meshList", "(stateless)", "cinemaName", "(contextless)"]
        ],
        "key":"mmb",
        "command":"attr.formPopover {itemprops:general}"
    }

]


class CommandClass(lxu.command.BasicCommand):

    def cmd_Execute(self,flags):
        for hotkey in HOTKEYS:
            command = hotkey["command"]
            key = hotkey["key"]

            for context in hotkey["contexts"]:
                mapping = context[0]
                state = context[1]
                region = context[2]
                context = context[3]

                lx.eval('!cmds.mapKey {%s} {%s} {%s} {%s} {%s} {%s}' % (key, command, mapping, state, region, context))

        modo.dialogs.alert("Mapped Zen Hotkeys", "Mapped %s Zen hotkeys. See Zen documentation for details." % len(HOTKEYS))
        lx.eval("OpenURL {kit_mecco_zen:Documentation/hotkeys.html}")

lx.bless(CommandClass, "zen.mapDefaultHotkeys")


class RemoveCommandClass(lxu.command.BasicCommand):

    def cmd_Execute(self,flags):
        for hotkey in HOTKEYS:
            key = hotkey["key"]

            for context in hotkey["contexts"]:
                mapping = context[0]
                state = context[1]
                region = context[2]
                context = context[3]

                lx.eval('!cmds.clearKey {%s} {%s} {%s} {%s} {%s}' % (key, mapping, state, region, context))

        modo.dialogs.alert("Cleared Zen Hotkeys", "Cleared %s Zen hotkeys." % len(HOTKEYS))

lx.bless(RemoveCommandClass, "zen.unmapDefaultHotkeys")
