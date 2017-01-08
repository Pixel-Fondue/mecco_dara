import lx, lxu.command, modo

BLESS = "cropper.focalLength"
SUFFIX = '_cropper'
CAM_TAG = 'CROP'

class commandClass(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        lx.eval('cropper.disable')

        tagValue = modo.Scene().renderCamera.getTags()[CAM_TAG] + SUFFIX

        lx.eval('select.drop item')
        lx.eval('select.drop channel')
        modo.Scene().renderCamera.select()
        lx.eval('select.channel {%s:focalLen} add' % modo.Scene().renderCamera.id)
        lx.eval('tool.set channel.haul on')

lx.bless(commandClass, BLESS)
