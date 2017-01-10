import lx
import lxu.command
import traceback
import monkey, modo, time, os

DEFAULT_TIME = '00:30:00'
DEFAULT_FRAMES = '1'
DEFAULT_USE_PASSES = 0
BLESS = 'monkey.renderProg'

class myGreatCommand(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        #command accepts an argument
        self.dyna_Add('time', lx.symbol.sTYPE_STRING)
        self.dyna_Add('frames', lx.symbol.sTYPE_STRING)
        self.dyna_Add('usePasses', lx.symbol.sTYPE_BOOLEAN)

    def basic_Execute(self, msg, flags):
        try:
            frames_string = self.dyna_String(1) if self.dyna_IsSet(1) else DEFAULT_FRAMES
            frames_list = monkey.util.frames_from_string(frames_string)
            if not frames_list:
                lx.out('Invalid frame range.')
                return False



            use_passes = self.dyna_String(2) if self.dyna_IsSet(2) else DEFAULT_USE_PASSES

            if use_passes:
                lx.out("Trying to use passes...")
                try:
                    pass_group = modo.Scene().item(lx.eval('group.current ? pass'))
                    lx.out("Pass group: %s" % pass_group.name)
                    pass_list = [i for i in pass_group.itemGraph('itemGroups').forward() if i.type == lx.symbol.a_ACTIONCLIP and i.actionClip.Enabled()]
                    lx.out("Passes:")
                    for i in pass_list:
                        lx.out("\t%s" % i.name)
                except:
                    lx.out('No active pass group. Rendering without passes.')
                    use_passes = False
                    pass_list = []



            time_string = self.dyna_String(0) if self.dyna_IsSet(0) else DEFAULT_TIME

            hms = time_string.split(':')

            if len(hms) == 3:
                h = int(hms[0])
                m = int(hms[1])
                s = int(hms[2])
            elif len(hms) == 2:
                h = 0
                m = int(hms[0])
                s = int(hms[1])
            elif len(hms) == 1:
                h = 0
                m = 0
                s = int(hms[0])

            total_seconds = h * 3600 + m * 60 + s

            if not total_seconds:
                lx.out('Invalid render time.')
                return False

            lx.out("Total seconds: %s" % total_seconds)

            per_render_seconds = total_seconds / ( len(frames_list) * (len(pass_list) if pass_list else 1) )
            lx.out("Seconds per render: %s" % per_render_seconds)

            m, s = divmod(per_render_seconds, 60)
            h, m = divmod(m, 60)
            per_render_string = "%d:%02d:%02d" % (h, m, s)
            lx.out("Seconds as string: %s" % per_render_string)

            destination = os.path.join("E:\\","Users","Adam","Desktop","test.jpg")
            image_saver = "JPG"
            frame_rate = 24

            lx.eval('iview.resume')

            for f in frames_list:
#                render_command = '!!iview.renderAnim {%s} %04d %04d sequence false' % (per_render_string,f,f)
                lx.out("Rendering frame %04d..." % f)
                lx.eval('select.time %s 0 0' % str(f/24.0))

                if use_passes and pass_list:
                    lx.out("Rendering passes:")
                    for p in pass_list:
                        lx.out("Pass %s..." % p.name)

                        p.actionClip.SetActive(1)

                        time.sleep(per_render_seconds)
                        lx.eval('iview.saveImage {%s} %s' % (destination,image_saver))

                        lx.out("...complete.")
                else:
                    time.sleep(per_render_seconds)
                    lx.eval('iview.saveImage {%s} %s' % (destination,image_saver))

                    lx.out("Frame %04d complete." % f)

        except Exception:
            lx.out(traceback.format_exc())

    def cmd_DialogInit(self):
        if not self.dyna_IsSet(0):
            self.attr_SetString(0, DEFAULT_TIME)
        if not self.dyna_IsSet(1):
            self.attr_SetString(1, DEFAULT_FRAMES)
        if not self.dyna_IsSet(2):
            self.attr_SetInt(2, DEFAULT_USE_PASSES)


lx.bless(myGreatCommand, BLESS)


