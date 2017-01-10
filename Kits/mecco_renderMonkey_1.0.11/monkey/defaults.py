# python

import lx
import os

from symbols import *

DEFAULTS = {
    FORMAT: 'JPG',
    FRAMES: '1',
    COMMANDS: [],
    GROUPS: [],
    WIDTH: 0,
    HEIGHT: 0,
    OUTPUTS: [],
    CAMERA: '',
    RENDER_CHANNELS: {},
    DESTINATION: './frames/',
    PATTERN: '[<pass>]_[<output>]_<FFFF>',
    FRAME_COMMANDS: [],
    RENDER_OVERRIDE: '',
    'debug': True,
    'breakpoints': True,
    'test_path': os.path.normpath(
        lx.eval("query platformservice alias ? {%s}" % "kit_mecco_renderMonkey:test/passGroups.lxo")
    ),
    'test_output_path': os.path.normpath(os.path.expanduser('~/Desktop/renderMonkey/filename.xyz')),
    'test_passgroup': 'Shots',
    'test_pass_groups': ['Shots', 'Materials', 'Cars'],
    'test_framerange': '1-3,5,10-8',
    'test_camera': 'Camera',
    'test_render_channels': {'irrCache': False, 'globLimit': 5, 'aa': 's128'},
    'test_outputs': ['FCO'],
    'test_width': 256,
    'test_height': 256.0*(9.0/16),
    'test_single_frame': '1'
}


def get(key):
    if key in DEFAULTS:
        return DEFAULTS[key]
    else:
        return None

TASK_PARAMS = {
                FORMAT: DEFAULTS[FORMAT],
                FRAMES: DEFAULTS[FRAMES],
                COMMANDS: DEFAULTS[COMMANDS],
                DESTINATION: DEFAULTS[DESTINATION],
                PATTERN: DEFAULTS[PATTERN],
                GROUPS: DEFAULTS[GROUPS],
                WIDTH: DEFAULTS[WIDTH],
                HEIGHT: DEFAULTS[HEIGHT],
                OUTPUTS: DEFAULTS[OUTPUTS],
                CAMERA: DEFAULTS[CAMERA],
                RENDER_CHANNELS: DEFAULTS[RENDER_CHANNELS]
            }