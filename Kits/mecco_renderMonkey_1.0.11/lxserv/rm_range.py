# python

# By Adam O'Hern for Mechanical Color LLC
# Attempts to render a series of frames from an arbitrary string, like "1-5, 10, 20-15"

import monkey, modo, lx, lxu, traceback

CMD_NAME = 'renderMonkey.range'


class CMD(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.startPath = None

        self.dyna_Add('range', lx.symbol.sTYPE_STRING)

    def basic_Execute(self, msg, flags):
        try:
            frames_string = self.dyna_String(0)
            frames_list = monkey.util.frames_from_string(frames_string)

            if frames_list:
                monkey.render.render_frames(frames_list)
            else:
                modo.dialogs.alert(
                    "Invalid Frame Range", "error", 'No frame range recognized in "{}".'.format(frames_string)
                )
                return lx.symbol.e_FAILED

        except:
            monkey.util.debug(traceback.format_exc())
            return lx.symbol.e_FAILEDs


lx.bless(CMD, CMD_NAME)
