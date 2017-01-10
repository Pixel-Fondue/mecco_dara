# python

import lx, lxifc, lxu, passify

class MySceneListener(lxifc.SceneItemListener):
    def __init__ (self):
        self.COM_object = lx.object.Unknown (self)
        self.lis_svc = lx.service.Listener ()
        self.lis_svc.AddListener (self.COM_object)

    def __del__ (self):
        self.lis_svc.RemoveListener (self.COM_object)

    def notify (self):
        notifier = passify.Notifier()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)
        # notifier.Notify (lx.symbol.fCMDNOTIFY_LABEL)
        # notifier.Notify (lx.symbol.fCMDNOTIFY_VALUE)

    ''' Listener Method Overrides '''
    def sil_SceneCreate (self, scene):
        # print 'Scene created.'
        self.notify ()

    def sil_SceneDestroy (self, scene):
        # print 'Scene destroyed.'
        self.notify ()

    def sil_SceneClear (self, scene):
        # print 'Scene cleared.'
        self.notify ()

MySceneListener ()
