import lx
from lxifc import UIValueHints

class PopupClass(UIValueHints):
    def __init__(self, items):
        if not items or not isinstance(items, (list, tuple)):
            self._user = []
            self._internal = []

        elif isinstance(items[0], (list, tuple)):
            self._user = [str(i[1]) for i in items]
            self._internal = [str(i[0]) for i in items]

        else:
            self._user = [str(i) for i in items]
            self._internal = [str(i) for i in items]

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._internal)

    def uiv_PopUserName(self,index):
        return self._user[index]

    def uiv_PopInternalName(self,index):
        return self._internal[index]
