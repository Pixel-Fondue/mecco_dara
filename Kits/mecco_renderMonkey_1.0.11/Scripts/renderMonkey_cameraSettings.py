#python

def get_camera_id():
    try:
        renderCamera = lx.eval("render.camera ?")
    except:
        renderCamera = "Camera"
    return lx.eval('query sceneservice item.ID ? {%s}' % renderCamera)

lx.eval("select.subItem {%s} set" % get_camera_id())
lx.eval("attr.formPopover {44124912882:sheet}")