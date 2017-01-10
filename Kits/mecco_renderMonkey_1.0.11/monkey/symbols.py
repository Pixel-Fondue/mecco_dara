# python

from os.path import join

# Globals
KIT_ALIAS = 'kit_mecco_renderMonkey'
QUICK_BATCH_PATH = join('tmp', 'quick_batch.yaml')

# Blessings
CMD_BatchOpen = "monkey.BatchOpen"
CMD_BatchClose = "monkey.BatchClose"
CMD_BatchAddTask = "monkey.BatchAddTask"
CMD_BatchAddParam = "monkey.BatchAddParam"
CMD_BatchAddToList = "monkey.BatchAddToList"
CMD_BatchAddToDict = "monkey.BatchAddToDict"
CMD_BatchDeleteNodes = "monkey.BatchDeleteNodes"
CMD_BatchReorderNodes = "monkey.BatchReorderNodes"
CMD_BatchSelectShift = "monkey.BatchSelectShift"
CMD_BatchEditNodes = "monkey.BatchEditNodes"
CMD_BatchEditNodesAdvanced = "monkey.BatchEditNodesAdvanced"
CMD_BatchResetNodes = "monkey.BatchResetNodes"
CMD_BatchOpenTaskScene = "monkey.BatchOpenTaskScene"
CMD_BatchRender = "monkey.BatchRender"
CMD_BatchExample = "monkey.BatchExample"
CMD_BatchOpenInFilesystem = "monkey.BatchOpenInFilesystem"
CMD_BatchExportTemplate = 'monkey.BatchExportTemplate'
CMD_BatchRevealInFilesystem = 'monkey.BatchRevealInFilesystem'
CMD_BatchNew = 'monkey.BatchNew'
CMD_BatchSaveAs = 'monkey.BatchSaveAs'
CMD_BatchParamsList = 'monkey.BatchParamsList'
CMD_BatchOpenStatusFile = 'monkey.BatchOpenStatusFile'
CMD_GLRenderWindow = 'monkey.GLRenderWindow'

CMD_BatchEditNumber = 'monkey.BatchEditNumber'
CMD_BatchEditString = 'monkey.BatchEditString'

# Special Node Names
BATCHFILE = "batch"
ADD_GENERIC = '(add...)'
ADD_TASK = '(add task...)'
ADD_PARAM = '(add parameter...)'
NO_FILE_SELECTED = "(no batch file)"

# Special Node Values
LIST = '(list)'
DICT = '(dict)'

# Useful Strings
TASK = 'Task'
SP = " "
EMPTY = ''

# Special Data Types
PATH_OPEN_SCENE = 'path_open_scene'
PATH_SAVE_SCENE = 'path_save_scene'
PATH_SAVE_IMAGE = 'path_save_image'
IMAGE_FORMAT = 'image_format'
FRAME_RANGE = 'frame_range'

# Task Parameters
SCENE_PATH = "scene"
FORMAT = "format"
FRAMES = "frames"
COMMANDS = "pre_task_commands"
FRAME_COMMANDS = "pre_frame_commands"
DESTINATION = "destination"
PATTERN = "output_pattern"
GROUPS = "pass_groups"
WIDTH = "frame_width"
HEIGHT = "frame_height"
OUTPUTS = "outputs"
CAMERA = "camera"
RENDER_CHANNELS = "render_channels"
RENDER_OVERRIDE = "render_command_override"

ALL_PARAMS = [
    SCENE_PATH,
    FORMAT,
    FRAMES,
    COMMANDS,
    FRAME_COMMANDS,
    DESTINATION,
    PATTERN,
    GROUPS,
    WIDTH,
    HEIGHT,
    OUTPUTS,
    CAMERA,
    RENDER_CHANNELS,
    RENDER_OVERRIDE
]

# Status Messages
STATUS = "status"
STATUS_COMPLETE = "(Complete)"
STATUS_IN_PROGRESS = "(In progress...)"
STATUS_FAILED = "(Failed)"
STATUS_ABORT = "(Aborted)"
STATUS_AVAILABLE = "(Available)"
STATUS_FILE_SUFFIX = "status"
DRYRUN_FILE_SUFFIX = "dryRun"
MESSAGE = 'Message'

# Treeview Basics
COL_NAME = "Name"
COL_VALUE = "Value"
SERVERNAME = 'RenderMonkeyBatch'
EMPTY_PROMPT = 'no batch file'
EMPTY_TASKS = 'no tasks'

TREE_ROOT_TITLE = 'Tasks'
IDENT = 'RMTV'
sSRV_USERNAME = "rendermonkeybatch"
NICE_NAME = "RenderMonkey_Batch"
OPEN_FILE_DIALOG_TITLE = 'Open File(s)'
VPTYPE = 'vpapplication'


# Node Types
REGIONS = [
    '(anywhere)', # 0 is reserved ".anywhere" region index
    'batchTask', #1
    'taskParam', #2
    'taskParamMulti', #3
    'taskParamSub', #4
    'addNode', #5
    'null', #6
    'batchFile', #7
    'addTask', #8
    'addParam', #9
    'addToList', #10
    'addToDict' #11
]
# Misc
LXO_FILE = '$LXOB'

# BatchReorderNodes Arguments
REORDER_ARGS = {
    'TOP': 'top',
    'BOTTOM': 'bottom',
    'UP': 'up',
    'DOWN': 'down'
}

# BatchSelectShift Arguments
SELECT_SHIFT_ARGS = {
    'UP': 'up',
    'DOWN': 'down'
}

# Flags
fTREE_VIEW_ITEM_ATTR             = 0x00000001
fTREE_VIEW_ITEM_EXPAND           = 0x00000002
fTREE_VIEW_ATTR_EXPAND           = 0x00000004
fTREE_VIEW_HIDDEN                = 0x00002000        # Item is hidden and will note be drawn.
fTREE_VIEW_ISATTR                = 0x00004000        # Item is an attribute of it's parent, instead of a normal child for ISTREE columns
fTREE_VIEW_NOSELECT              = 0x00000100        # Item is not selectable, and should not show roll-over hilighting
fTREE_VIEW_EXPATTR               = 0x00000010        # Attribute children are expanded and visible for ISTREE columns
fTREE_VIEW_EXPSUB                = 0x00000004        # Sub-items are expanded and the children are visible for ISTREE columns
fTREE_VIEW_SELECTED              = 0x00000040

# More Flags
fTREE_VIEW_ROWCOLOR_NONE         = 0x00000000        # No color
fTREE_VIEW_ROWCOLOR_RED          = 0x00010000
fTREE_VIEW_ROWCOLOR_MAGENTA      = 0x00020000
fTREE_VIEW_ROWCOLOR_PINK         = 0x00030000
fTREE_VIEW_ROWCOLOR_BROWN        = 0x00040000
fTREE_VIEW_ROWCOLOR_ORANGE       = 0x00050000
fTREE_VIEW_ROWCOLOR_YELLOW       = 0x00060000
fTREE_VIEW_ROWCOLOR_GREEN        = 0x00070000
fTREE_VIEW_ROWCOLOR_LIGHT_GREEN  = 0x00080000
fTREE_VIEW_ROWCOLOR_CYAN         = 0x00090000
fTREE_VIEW_ROWCOLOR_BLUE         = 0x000A0000
fTREE_VIEW_ROWCOLOR_LIGHT_BLUE   = 0x000B0000
fTREE_VIEW_ROWCOLOR_ULTRAMARINE  = 0x000C0000
fTREE_VIEW_ROWCOLOR_PURPLE       = 0x000D0000
fTREE_VIEW_ROWCOLOR_LIGHT_PURPLE = 0x000E0000
fTREE_VIEW_ROWCOLOR_DARK_GREY    = 0x000F0000
fTREE_VIEW_ROWCOLOR_GREY         = 0x00100000
fTREE_VIEW_ROWCOLOR_WHITE        = 0x00110000
