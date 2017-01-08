# python

import modo, lx, lxu, traceback, passify

class CMD(lxu.command.BasicCommand):

    def basic_Execute(self, msg, flags):
        try:
            scene = modo.Scene()
            selected_groups = scene.selectedByType(lx.symbol.sITYPE_GROUP)

            if selected_groups:
                selected_pass_groups = [g for g in selected_groups if g.type == 'render']

                if selected_pass_groups:
                    monkey.passes.create_master_pass_group(selected_pass_groups)
                else:
                    modo.dialogs.alert(passify.message('error'), passify.message('select_a_pass_group'))

            else:
                modo.dialogs.alert(passify.message('error'), passify.message('select_a_pass_group'))

        except Exception:
            monkey.util.debug(traceback.format_exc())

        notifier = passify.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)


    def basic_Enable(self,msg):
        try:
            group = lx.eval('group.current group:? type:pass')
        except:
            return False

        if group:
            return True

        return False

class Notifiers(lxu.command.BasicHints):

    def __init__(self):
        self._notifiers = [('notifier.layerAutoAdd',''),('notifier.editAction','')]

lx.bless(CMD, passify.CMD_MANAGER_COMBINE_PASS_GROUPS)
