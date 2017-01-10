#python

# By Adam O'Hern for Mechanical Color LLC

import lx, lxu
import monkey, yaml
import traceback, os

from monkey.symbols import *
from monkey.defaults import get


class BatchExportTemplate(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.startPath = None

        self.dyna_Add('path', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def basic_Execute(self, msg, flags):
        try:
            tree = [
                {
                    SCENE_PATH: get('test_path'),
                    FRAMES: get(FRAMES)
                }, {
                    SCENE_PATH: get('test_path'),
                    FORMAT: get(FORMAT),
                    DESTINATION: get('test_output_path'),
                    GROUPS: get('test_passgroup'),
                    FRAMES: get(FRAMES)
                }, {
                    SCENE_PATH: get('test_path'),
                    FORMAT: get(FORMAT),
                    FRAMES: get('test_single_frame'),
                    DESTINATION: get('test_output_path'),
                    PATTERN: get(PATTERN),
                    GROUPS: get('test_pass_groups'),
                    CAMERA: get('test_camera'),
                    RENDER_CHANNELS: get('test_render_channels'),
                    OUTPUTS: get('test_outputs'),
                    WIDTH: get('test_width'),
                    HEIGHT: get('test_height')
                }
            ]

            if self.dyna_IsSet(0):
                output_path = self.dyna_String(0)
            else:
                output_path = monkey.io.yaml_save_dialog()

            monkey.io.write_yaml(tree, output_path)

        except Exception:
            monkey.util.debug(traceback.format_exc())


lx.bless(BatchExportTemplate, CMD_BatchExportTemplate)
