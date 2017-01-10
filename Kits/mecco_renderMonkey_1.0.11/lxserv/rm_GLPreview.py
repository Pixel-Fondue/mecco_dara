#python

import lx
import lxu.command
import traceback
import modo
import monkey
import re

from fractions import Fraction
from monkey.symbols import *

BORDER = 8
BACKGROUND_DEFAULT = '0.5 0.5 0.5'

class GLRenderWindow(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        #command accepts an argument
        self.dyna_Add('width', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('ratio', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)

        self.dyna_Add('background', lx.symbol.sTYPE_COLOR)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)


    def scene_ratio(self):
        x = int(modo.Scene().renderItem.channel('resX').get())
        y = int(modo.Scene().renderItem.channel('resY').get())
        return str(Fraction(x,y))

    def basic_Execute(self, msg, flags):
        width = self.dyna_Int(0, 0.0) if self.dyna_IsSet(0) else 1280
        ratio_string = self.dyna_String(1, 0.0) if self.dyna_IsSet(1) else self.scene_ratio()
        background = self.dyna_String(2, 0.0) if self.dyna_IsSet(2) else BACKGROUND_DEFAULT
        ratio_string = "".join([i for i in ratio_string if i in "0123456789:/,."])

        try:
            ratio_float = float(ratio_string)
        except:
            try:
                ratio_parts = re.split(":|/|,",ratio_string)
                ratio_float = float(ratio_parts[0])/float(ratio_parts[1])
            except:
                modo.dialogs.alert(
                    "Invalid Ratio",
                    "Could not parse \"{}\".\nRatio should be either a decimal (e.g. 1.777) or a ratio (e.g. 16:9).".format(ratio_string),
                    'error'
                )
                return lx.symbol.e_FAILED

        height = int(round(width / ratio_float))

        lx.eval('layout.create width:%s height:%s style:palette' % (width+BORDER,height+BORDER))
        lx.eval('viewport.restore base.3DSceneView false 3Dmodel')
        lx.eval('view3d.bgEnvironment background solid')
        lx.eval('view3d.showGrid false')
        lx.eval('view3d.projection cam')
        lx.eval('view3d.controls false')
        lx.eval('view3d.showLights false')
        lx.eval('view3d.showCameras false')
        lx.eval('view3d.showLocators false')
        lx.eval('view3d.showTextureLocators false')
        lx.eval('view3d.showBackdrop false')
        lx.eval('view3d.showSelections false')
        lx.eval('view3d.fillSelected false')
        lx.eval('view3d.outlineSelected false')
        lx.eval('view3d.showSelectionRollover false')
        lx.eval('view3d.shadingStyle advgl active')
        lx.eval('view3d.wireframeOverlay none active')
        lx.eval('view3d.renderCamera')
        lx.eval('view3d.shadingStyle gnzgl')
        lx.eval('view3d.sameAsActive true')

        lx.eval('scheme.savePreset monkey_temp')
        lx.eval('pref.value color.deformers {{{}}}'.format(background))
        lx.eval('scheme.savePreset monkey_temp')
        lx.eval('viewport.scheme monkey_temp.3d')

    def cmd_DialogInit(self):
        if not self.dyna_IsSet(0):
            self.attr_SetInt(0, 1280)
        if not self.dyna_IsSet(1):
            self.attr_SetString(1, self.scene_ratio())
        if not self.dyna_IsSet(2):
            self.attr_SetString(2, BACKGROUND_DEFAULT)


lx.bless(GLRenderWindow, CMD_GLRenderWindow)
