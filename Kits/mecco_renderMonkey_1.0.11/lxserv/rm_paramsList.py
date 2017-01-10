# python

# Copyright 0000

import lx
import lxifc
import lxu

from monkey.symbols import *


def is_enabled(cmd_string) :
  msg = lx.service.Message().Allocate()
  cmd = lx.service.Command().SpawnFromString(cmd_string)[2]
  try:
    cmd.Enable(msg)
  except RuntimeError, e:
    if e.message == 'bad result: CMD_DISABLED':
      return False
    raise
  return True


class BatchParamsPopup(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items[0])

    def uiv_PopUserName(self,index):
        return self._items[1][index]

    def uiv_PopInternalName(self,index):
        return self._items[0][index]

class BatchParamsList(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('parameter', lx.symbol.sTYPE_STRING)

    def basic_ButtonName(self):
        return ADD_PARAM

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        if self.dyna_IsSet(0):
            lx.eval('monkey.BatchAddParam %s' % self.dyna_Int(0))

    def arg_UIValueHints(self, index):
        commands = [[],[]]
        for param in ALL_PARAMS:
              commands[0].append(param)
              commands[1].append(param.replace('_', ' ').title())
        if index == 0:
            return BatchParamsPopup(commands)


lx.bless(BatchParamsList, CMD_BatchParamsList)