# python

import lx, lxu, modo

class CommandClass(lxu.command.BasicCommand):

    def cmd_Execute(self,flags):

        safety = modo.dialogs.yesNo("Not Recommended", "Zen Double-Click has unresolved problems, and it's currently not recommended. Are you sure you want to use it?")

        if safety == "no":
            return

        command = "zen.doubleClick"
        key = "lmb-dblclick"
        mapping = "view3DSelect"
        state = "(stateless)"
        region = ".anywhere"
        context = "(contextless)"

        lx.eval('!cmds.mapKey {%s} {%s} {%s} {%s} {%s} {%s}' % (key, command, mapping, state, region, context))
        lx.eval('pref.value opengl.mouseRegionsSelect false')

        modo.dialogs.alert("Mapped Zen Double-Click", "Double-click in a 3D viewport\nis now mapped to 'zen.doubleClick', and\nPreferences > OpenGL > Selection > Mouse Regions Trigger Selection\nis now disabled.")
        lx.eval("OpenURL {kit_mecco_zen:Documentation/doubleclick.html}")

lx.bless(CommandClass, "zen.enableZenDoubleClick")

class RemoveCommandClass(lxu.command.BasicCommand):

    def cmd_Execute(self,flags):
        command = ""
        key = "lmb-dblclick"
        mapping = "view3DSelect"
        state = "(stateless)"
        region = ".anywhere"
        context = "(contextless)"

        lx.eval('!cmds.clearKey {%s} {%s} {%s} {%s} {%s}' % (key, mapping, state, region, context))
        lx.eval('pref.value opengl.mouseRegionsSelect true')

        modo.dialogs.alert("Mapped Zen Double-Click", "Zen Double-Click has been disabled, and \nPreferences > OpenGL > Selection > Mouse Regions Trigger Selection\nis now enabled.")

lx.bless(RemoveCommandClass, "zen.disableZenDoubleClick")
