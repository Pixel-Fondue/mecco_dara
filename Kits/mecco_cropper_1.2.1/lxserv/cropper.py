# python

import lx
import lxu.command
import lxifc
import traceback
import modo
import datetime

GROUP_NAME = 'mecco_regions'
DEFAULT_PASSNAME = 'crop'

SUFFIX = '_cropper'
CAM_TAG = 'CROP'

def get_tracer_camera():
    if modo.Scene().renderCamera.hasTag(CAM_TAG) == False:
        return None

    if SUFFIX in modo.Scene().renderCamera.getTags()[CAM_TAG]:
        return None

    tagValue = modo.Scene().renderCamera.getTags()[CAM_TAG] + SUFFIX

    for i in modo.Scene().iterItems():
        if i is not modo.Scene.renderCamera and i.hasTag(CAM_TAG):
            if i.getTags()[CAM_TAG] == tagValue:
                return i

    return None

def create_tracer_camera():
    camera = modo.Scene().addItem('camera')
    renderCam = modo.Scene().renderCamera

    camera.channel('visible').set('allOff')
    camera.channel('lock').set('on')
    camera.name = renderCam.name + SUFFIX
    camera.setParent(renderCam)

    tagValue = ''.join([i for i in str(datetime.datetime.now()) if i.isalnum()])
    camera.setTag(CAM_TAG, tagValue + SUFFIX)
    renderCam.setTag(CAM_TAG, tagValue)

    channels_to_link = [
        'wposMatrix',
        'wrotMatrix',
        'focalLen',
        'size',
        'squeeze',
        'dof',
        'focusDist',
        'fStop',
        'irisBlades',
        'irisRot',
        'irisBias',
        'distort',
        'motionBlur',
        'blurLen',
        'blurOff',
        'stereo',
        'stereoEye',
        'stereoComp',
        'ioDist',
        'convDist',
        'target',
        'clipDist',
        'clipping'
    ]

    for channel in channels_to_link:
    	lx.eval("channel.link add {%s:%s} {%s:%s}" % (renderCam.id, channel, camera.id, channel))

    channels_to_copy = [
        'apertureX',
        'apertureY',
        'offsetX',
        'offsetY'
    ]

    for channel in channels_to_copy:
        camera.channel(channel).set(renderCam.channel(channel).get())

    return camera


def get_render_region():
    return {
        'left': modo.Scene().renderItem.channel('regX0').get(),
        'right': modo.Scene().renderItem.channel('regX1').get(),
        'top': modo.Scene().renderItem.channel('regY0').get(),
        'bottom': modo.Scene().renderItem.channel('regY1').get()
    }


def get_target_frame():
    render_region = get_render_region()

    return [
        int(modo.Scene().renderItem.channel('resX').get()) * abs(render_region['right'] - render_region['left']),
        int(modo.Scene().renderItem.channel('resY').get()) * abs(render_region['bottom'] - render_region['top']),
    ]


def get_target_offset():
    proportional_aperture = get_proportional_aperture()

    frame = [
        int(modo.Scene().renderItem.channel('resX').get()),
        int(modo.Scene().renderItem.channel('resY').get())
    ]

    offset = [
        modo.Scene().renderCamera.channel('offsetX').get(),
        modo.Scene().renderCamera.channel('offsetY').get()
    ]

    render_region = get_render_region()

    x_step = 1
    y_step = x_step

    if frame[0] == frame[1]:
        x_step = proportional_aperture[1]
        y_step = proportional_aperture[1]

    elif frame[0] > frame[1]:
        mdf = float(frame[0]) / frame[1]
        x_step = proportional_aperture[0]
        y_step = proportional_aperture[0] / mdf

    elif frame[0] < frame[1]:
        mdf = float(frame[1]) / frame[0]
        x_step = proportional_aperture[1] / mdf
        y_step = proportional_aperture[1]

    offset = [
        ((render_region['left']+render_region['right'])/2 - .5) * x_step + offset[0],
        ((render_region['top']+render_region['bottom'])/2 - .5) * -y_step + offset[1],
    ]

    return offset


def deactivate_pass():
    graph_kids = modo.Scene().item(GROUP_NAME).itemGraph('itemGroups').forward()
    passes = [i for i in graph_kids if i.type == lx.symbol.a_ACTIONCLIP]

    for pass_ in passes:
        pass_.actionClip.SetActive(0)


def active_pass():
    try:
        modo.Scene().item(GROUP_NAME)
    except LookupError:
        return None

    graph_kids = modo.Scene().item(GROUP_NAME).itemGraph('itemGroups').forward()
    passes = [i for i in graph_kids if i.type == lx.symbol.a_ACTIONCLIP]

    for pass_ in passes:
        if pass_.actionClip.Active():
            return pass_

    return None


def activate_latest_pass():
    try:
        graph_kids = modo.Scene().item(GROUP_NAME).itemGraph('itemGroups').forward()
    except NameError:
        return

    passes = [i for i in graph_kids if i.type == lx.symbol.a_ACTIONCLIP]
    max(passes, key=lambda p: p.index).actionClip.SetActive(1)


def get_proportional_aperture():
    frame = [
        int(modo.Scene().renderItem.channel('resX').get()),
        int(modo.Scene().renderItem.channel('resY').get())
    ]

    ratio = float(max(frame)) / min(frame)

    aperture = [
        modo.Scene().renderCamera.channel('apertureX').get(),
        modo.Scene().renderCamera.channel('apertureY').get()
    ]

    apr_ratio = float(max(aperture)) / min(aperture)

    if ratio <= apr_ratio:
        if aperture[0] > aperture[1]:
            aperture[0] = aperture[1] * ratio

        elif aperture[0] < aperture[1]:
            aperture[1] = aperture[0] * ratio

    return aperture


def get_target_aperture():
    target_frame = get_target_frame()
    proportional_aperture = get_proportional_aperture()

    render_region = get_render_region()

    region_size = [
        render_region['right'] - render_region['left'],
        render_region['bottom'] - render_region['top']
    ]

    if target_frame[0] > target_frame[1]:
        target_aperture = [
            proportional_aperture[0] * region_size[0],
            modo.Scene().renderCamera.channel('apertureY').get()
        ]

    elif target_frame[0] == target_frame[1]:
        target_aperture = [
            proportional_aperture[1] * region_size[0],
            modo.Scene().renderCamera.channel('apertureY').get()
        ]

    else:
        target_aperture = [
            modo.Scene().renderCamera.channel('apertureX').get(),
            proportional_aperture[1] * region_size[1]
        ]

    return target_aperture


class CropperNotify(lxifc.Notifier):
    masterList = {}

    def noti_Name(self):
        return "cropper.notifier"

    def noti_AddClient(self,event):
        self.masterList[event.__peekobj__()] = event

    def noti_RemoveClient(self,event):
        del self.masterList[event.__peekobj__()]

    def Notify(self, flags):
        for event in self.masterList:
            evt = lx.object.CommandEvent(self.masterList[event])
            evt.Event(flags)


class Cropper(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('name', lx.symbol.sTYPE_STRING)

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            lx.out(traceback.format_exc())

    def CMD_EXE(self, msg, flags):
        pass_name = self.dyna_String(0) if self.dyna_IsSet(0) else DEFAULT_PASSNAME

        if modo.Scene().renderCamera.channel('resOverride').get() == 1:
            modo.dialogs.alert(
                'Resolution Override Not Supported',
                'The resolution override setting is enabled for this camera, and is not currently supported by cropper. Disable this setting and try again.',
                'error'
                )
            return lx.symbol.e_FAILED

        tracerCam = get_tracer_camera() if get_tracer_camera() else create_tracer_camera()

        modo.Scene().renderItem.channel('region').set(False)
        lx.eval("view3d.renderCamera")

        try:
            modo.Scene().item(GROUP_NAME)
        except LookupError:
            lx.eval('group.create {} pass empty'.format(GROUP_NAME))

        channels_list = [
            modo.Scene().renderItem.channel('resX'),
            modo.Scene().renderItem.channel('resY'),
            modo.Scene().renderItem.channel('cameraIndex'),
            tracerCam.channel('offsetX'),
            tracerCam.channel('offsetY'),
            tracerCam.channel('apertureX'),
            tracerCam.channel('apertureY')
        ]

        for channel in channels_list:
            if channel not in modo.Scene().item(GROUP_NAME).groupChannels:
                modo.Scene().item(GROUP_NAME).addChannel(channel)

        lx.eval('group.layer group:{%s} name:{%s} grpType:pass' % (GROUP_NAME, pass_name))

        target_frame = get_target_frame()
        target_offset = get_target_offset()
        target_aperture = get_target_aperture()

        modo.Scene().renderItem.channel('resX').set(target_frame[0])
        modo.Scene().renderItem.channel('resY').set(target_frame[1])
        lx.eval('render.camera {%s}' % tracerCam.id)
        tracerCam.channel('offsetX').set(target_offset[0])
        tracerCam.channel('offsetY').set(target_offset[1])
        tracerCam.channel('apertureX').set(target_aperture[0])
        tracerCam.channel('apertureY').set(target_aperture[1])

        lx.eval('edit.apply')

        notifier = CropperNotify()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)


class CropperToggle(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('quick', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def basic_Execute(self, msg, flags):
        if active_pass():
            deactivate_pass()

        elif modo.Scene().renderItem.channel('region').get():
            arg = ' {%s}' % DEFAULT_PASSNAME if self.dyna_Bool(0) else ''
            lx.eval('cropper.crop{}'.format(arg))

        else:
            activate_latest_pass()

class CropperDisable(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def basic_Execute(self, msg, flags):
        if active_pass():
            deactivate_pass()

class CropperClearAll(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def basic_ButtonName(self):
        return "Delete All Crops"

    def basic_Execute(self, msg, flags):
        try:
            modo.Scene().removeItems(modo.Scene().item(GROUP_NAME))
        except:
            pass

        hitlist = set()
        for i in modo.Scene().iterItems():
            if i.hasTag(CAM_TAG):
                if SUFFIX in i.getTags()[CAM_TAG]:
                    hitlist.add(i)

            if i.hasTag(CAM_TAG):
                i.setTag(CAM_TAG, None)

        for hit in hitlist:
            modo.Scene().removeItems(hit)

        notifier = CropperNotify()
        notifier.Notify(lx.symbol.fCMDNOTIFY_DATATYPE)

lx.bless(CropperToggle, "cropper.toggleButton")
lx.bless(CropperDisable, "cropper.disable")
lx.bless(Cropper, "cropper.crop")
lx.bless(CropperClearAll, "cropper.clearAll")
lx.bless(CropperNotify, "cropper.notifier")
