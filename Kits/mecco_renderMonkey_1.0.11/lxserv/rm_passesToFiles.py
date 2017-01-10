#python
import lx, lxu.command, modo
from os.path import splitext

BLESS = "monkey.passesToFiles"

class commandClass(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        try:
            # Note that backslashes for Windows path names have to be escaped (\\). Mac/Linux paths should be fine as normal (/).
            OUTPUT = ''
            PATTERN = '_<output>_<FFFF>'
            PASS_GROUP = modo.Scene().selectedByType(lx.symbol.sITYPE_GROUP)[0]

            if not PASS_GROUP.type == 'render':
                raise Exception("Not a render pass group.")

            scene = modo.Scene()
            group = scene.item(PASS_GROUP)
            outputs = [i for i in scene.iterItems() if i.type == 'renderOutput']
            passes = [i for i in group.itemGraph('itemGroups').forward() if i.type == lx.symbol.a_ACTIONCLIP and i.enabled]

            if PATTERN:
                restorePat = scene.renderItem.channel('outPat').get()
                scene.renderItem.channel('outPat').set(PATTERN)

            for pass_ in passes:
                pass_.actionClip.SetActive(1)

                restoreOut = []
                for output in outputs:
                    if not output.channel('filename').get():
                        restoreOut.append('')
                        continue

                    restoreOut.append(output.channel('filename').get())

                    if OUTPUT:
                        output.channel('filename').set(OUTPUT + '_' + pass_.name)
                    else:
                        output.channel('filename').set(output.channel('filename').get() + '_' + pass_.name)

                splitpath = splitext(lx.eval('query sceneservice scene.file ? current'))
                lx.eval('scene.saveAs {%s_%s%s} $LXOB true' % (splitpath[0], pass_.name + "_floor", splitpath[1]) )

                for i, output in enumerate(outputs):
                    output.channel('filename').set(restoreOut[i])

            if PATTERN:
                scene.renderItem.channel('outPat').set(restorePat)
        except:
            lx.out("Aw dang.")


lx.bless(commandClass, BLESS)
