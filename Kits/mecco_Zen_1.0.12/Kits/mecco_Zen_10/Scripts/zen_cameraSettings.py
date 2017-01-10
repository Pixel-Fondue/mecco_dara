#python

import modo

def get_camera_id():
    try:
        renderCamera = lx.eval("render.camera ?")
    except:
        pass

    cameras = modo.Scene().cameras

    if len(cameras) == 0:
        return None
    elif len(cameras) >= 1:
        lx.eval('render.camera {%s}' % cameras[0].id)
        return cameras[0].id

lx.eval("select.drop item")

camera_id = get_camera_id()

if camera_id:
    lx.eval("select.subItem {%s} set" % camera_id)
    lx.eval("attr.formPopover {99877091315:sheet}")
else:
    modo.dialogs.alert("No Render Camera", "There is no render camera to select.")
