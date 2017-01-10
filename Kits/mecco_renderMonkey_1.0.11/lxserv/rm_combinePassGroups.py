# python

# By Adam O'Hern for Mechanical Color LLC

import monkey, modo, lx, lxu, traceback

CMD_NAME = 'renderMonkey.passGroupsCombineSelected'


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
                    modo.dialogs.alert('Try again.', 'Select at least one pass group.')

            else:
                modo.dialogs.alert('Try again.', 'Select at least one pass group.')

        except Exception:
            monkey.util.debug(traceback.format_exc())


lx.bless(CMD, CMD_NAME)
