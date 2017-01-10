#python

def get_camera_id():
    try:
        renderCamera = lx.eval("render.camera ?")
    except:
        renderCamera = "Camera"
    return lx.eval('query sceneservice item.ID ? {%s}' % renderCamera)

lx.eval("select.drop item")
lx.eval("select.subItem {%s} set" % get_camera_id())
lx.eval("attr.formPopover {99877091315:sheet}")
