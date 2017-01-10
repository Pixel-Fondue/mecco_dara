# python

import lx, lxifc, lxu, passify

class MySelectionListener(lxifc.SelectionListener):
    def __init__ (self):
        self.COM_object = lx.object.Unknown (self)
        self.lis_svc = lx.service.Listener ()
        self.lis_svc.AddListener (self.COM_object)

        sel_svc = lx.service.Selection ()
        self.cinetype = lxu.lxID4 ('CINE')

    def __del__ (self):
        self.lis_svc.RemoveListener (self.COM_object)

    def notify (self):
        notifier = passify.Notifier()
        notifier.Notify (lx.symbol.fCMDNOTIFY_DATATYPE)
        # notifier.Notify (lx.symbol.fCMDNOTIFY_LABEL)
        # notifier.Notify (lx.symbol.fCMDNOTIFY_VALUE)

    ''' Listener Method Overrides '''
    def selevent_Current (self, typ):
        if typ == self.cinetype:
            self.notify ()

    def selevent_Add (self, typ, subtType):
        if typ == self.cinetype:
            self.notify ()

    def selevent_Remove (self, typ, subtType):
        if typ == self.cinetype:
            self.notify ()


MySelectionListener ()
