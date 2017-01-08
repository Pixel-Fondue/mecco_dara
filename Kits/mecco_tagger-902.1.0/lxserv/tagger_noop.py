#python

import lx, lxu, modo, tagger, traceback

class CommandClass(tagger.Commander):
    _commander_default_values = []

    def commander_arguments(self):
        return [
                {
                    'name': 'label',
                    'datatype': 'string',
                    'value': 'blank',
                    'flags': ['optional'],
                }
            ]

    def basic_ButtonName(self):
        return self.commander_arg_value(0)

    def basic_Enable(self, msg):
        return False

    def commander_execute(self, msg, flags):
        pass

lx.bless(CommandClass, tagger.CMD_NOOP)
