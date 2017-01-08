#python

from lx import symbol

DEFAULT_PTAG = symbol.i_POLYTAG_MATERIAL
DEFAULT_RANDOM_COLOR_SATURATION = .7
DEFAULT_RANDOM_COLOR_VALUE = .95
DEFAULT_MATERIAL_NAME = 'material'
DEFAULT_GROUP_NAME = 'tagger_group'
MAX_FCL = 25
MAX_MASK_FCL = 10
MAX_FCL_POLY_INSPECT = 250
MAX_PTAG_ISLANDS = 50
DEBUG_TIMER_THRESHOLD = .005

SCENE_TAG_RECENT = 'TAGR'
SCENE_TAG_RECENT_MAX = 25

TAGTYPE_SEP = ":"
TAG_SEP = ";"

CMD = 'command'
CMD_PREFS_SET_USER_PRESETS_PATH = 'tagger.prefsSetUserPresetsPath'
CMD_PTAG_CONVERT = 'tagger.pTagConvert'
CMD_PTAG_QUICK_ASSIGN_POPUP = 'tagger.pTagQuickAssignPopup'
CMD_PTAG_QUICK_SELECT_POPUP = 'tagger.pTagQuickSelectPopup'
CMD_SET_MATERIAL = 'tagger.setMaterial_auto'
CMD_SET_AUTO_REMOVE = 'tagger.setMaterial_autoRemove'
CMD_SET_PTAG = 'tagger.setMaterial_pTag'
CMD_SET_AUTO_QUICK = 'tagger.setMaterial_autoQuick'
CMD_SET_PTAG_ISLANDS = 'tagger.setMaterial_pTagIslands'
CMD_SET_PTAG_REMOVE = 'tagger.setMaterial_pTagRemove'
CMD_SET_ITEM = 'tagger.setMaterial_item'
CMD_SET_ITEM_REMOVE = 'tagger.setMaterial_itemRemove'
CMD_SET_GROUP = 'tagger.setMaterial_group'
CMD_FLOOD_SELECT_MATERIAL = 'tagger.floodSelectMaterial'
CMD_FLOOD_SELECT_PART = 'tagger.floodSelectPart'
CMD_FLOOD_SELECT_SET = 'tagger.floodSelectSelectionSet'
CMD_PTAG_SET = 'tagger.pTagSet'
CMD_PTAG_COPY = 'tagger.pTagCopy'
CMD_PTAG_COPYMASK = 'tagger.pTagCopyMask'
CMD_PTAG_PASTE_MAT = 'tagger.pTagPasteMaterial'
CMD_PTAG_PASTE_PART = 'tagger.pTagPastePart'
CMD_PTAG_PASTE_SET = 'tagger.pTagPasteSelectionSet'
CMD_PTAG_PASTE_DIALOG = 'tagger.pTagPasteDialog'
CMD_PTAG_INSPECT = 'tagger.pTagInspect'
CMD_PTAG_REMOVEALL = 'tagger.pTagRemoveAll'
CMD_PTAG_REPLACE = 'tagger.pTagReplace'
CMD_PTAG_SELECTION_FCL = 'tagger.pTagSelectionFCL'
CMD_SELECT_ALL_BY_DIALOG = 'tagger.selectAllByTagDialog'
CMD_SELECT_ALL_BY_MATERIAL = 'tagger.selectAllByMaterial'
CMD_SELECT_ALL_BY_PART = 'tagger.selectAllByPart'
CMD_SELECT_ALL_BY_SET = 'tagger.selectAllBySelectionSet'
CMD_SET_EXISTING = 'tagger.setMaterial_existing'
CMD_SET_EXISTING_FCL = 'tagger.setMaterial_existing_FCL'
CMD_SET_EXISTING_POPUP = 'tagger.setMaterial_existing_Popup'
CMD_SHADERTREE_MASK_UNMASKED = 'tagger.shaderTree_maskUnmasked'
CMD_PTAG_REMOVE_UNMASKED = 'tagger.pTagRemoveUnmasked'
CMD_SHADERTREE_CLEANUP = 'tagger.shaderTree_cleanup'
CMD_SHADERTREE_CONSOLIDATE_BY_COLOR = 'tagger.shaderTree_consolidateByColor'
CMD_NOOP = 'tagger.noop'

GROUPNAME = "group"
MATNAME = "material"
SHADERNAME = "shader"

GTYP = "GTYP"

GROUP_TYPES_STANDARD = ''
GROUP_TYPES_ASSEMBLY = 'assembly'

NAME = 'name'
MODE = 'mode'
OPERATION = 'operation'
SCOPE = 'scope'
REMOVE_SCOPE = 'scope'
PRESET = 'preset'
TAGTYPE = 'tagType'
COPY = 'copy'
PASTE = 'paste'
MATERIAL = 'material'
PICK = 'pick'
PART = 'part'
ALL = 'all'
TAG = 'tag'
i_POLYTAG = 'i_POLYTAG'
MASK = 'mask'
COPYMASK = 'copyMask'
REPLACETAG = 'replaceTag'
WITHTAG = 'withTag'
QUERY = 'query'
RANDOM = 'random'
DELETE_UNUSED_MASKS = 'delete_unused'
WITH_EXISTING = 'withExisting'
GET_MORE_PRESETS = 'getMorePresets'
GET_MORE_PRESETS_URL = 'http://www.mechanicalcolor.com/coming-soon'
OPERATION = 'operation'
REMOVE = 'remove'
ADD = 'add'
USE = 'use'
KEEP = 'keep'
REMOVE = 'remove'
CONSOLIDATE = 'consolidate'
SCOPE_SELECTED = 'selected'
SCOPE_CONNECTED = 'connected'
SCOPE_FLOOD = 'flood'
SCOPE_SELECTED_ITEMS = 'selected_items'
SCOPE_SCENE = 'scene'
SCOPE_ALL = 'all'
FROM_TAG_TYPE = 'fromTagType'
TO_TAG_TYPE = 'toTagType'
DEL_EMPTY = 'delEmpty'
DEL_UNUSED = 'delUnused'
NEW_TAG = "newTag"

# These should probably be pulled from message tables
LABEL_NEW_TAG = "(new tag)"
LABEL_ASSIGN_TAG = "Assign"
LABEL_SELECT_TAG = "Select by"
LABEL_CHOOSE_FOLDER = "Select Folder"
LABEL_MODE = "Mode"
LABEL_TAGTYPE = "Tag Type"
LABEL_TAG = "Tag"
LABEL_TAGS = "Tags"
LABEL_PRESET = "Quick Preset"
LABEL_SCOPE = "Scope"
LABEL_REMOVE_SCOPE = "Remove From"
LABEL_NONE = "(none)"
LABEL_REPLACE_TAG = "Replace Tag"
LABEL_WITH_TAG = "With Tag"
LABEL_RANDOM_COLOR = "Random Color"
LABEL_GET_MORE_PRESETS = "Get more presets..."
LABEL_WITH_EXISTING = "With Existing"
LABEL_DELETE_UNUSED_MASKS = "Cleanup unused masks"
LABEL_OPERATION = "Operation"
LABEL_GROUP_NAME = "Group Name"
LABEL_TAG_WITH_MASKED = "Assign Existing Mask"
LABEL_MATERIAL = "Material"
LABEL_PART = "Part"
LABEL_PICK = "Selection Set"
LABEL_ALL = "All"
LABEL_SCOPE_SELECTED = 'Selected Polys'
LABEL_SCOPE_CONNECTED = 'Connected Polys'
LABEL_SCOPE_FLOOD = 'Flood Polys'
LABEL_SCOPE_SELECTED_ITEMS = 'Selected Items'
LABEL_SCOPE_SCENE = 'Entire Scene'
LABEL_USE = 'Use'
LABEL_KEEP = 'Keep and add'
LABEL_REMOVE = 'Remove and add'
LABEL_CONSOLIDATE = 'Consolidate and add'
LABEL_FROM_TAGTYPE = 'From Tag Type'
LABEL_TO_TAGTYPE = 'To Tag Type'
LABEL_COPY = 'Copy'
LABEL_PASTE = 'Paste'
LABEL_QUERY = 'Query'
LABEL_SET = 'Set'
LABEL_SELECT = 'Select'
LABEL_TO = 'to'
LABEL_SELECT_ALL = 'Select All by'
LABEL_SELECT_CONNECTED_BY = 'Flood select by'
LABEL_REMOVE_ALL = 'Remove All'
LABEL_DELETE_EMPTY_GROUPS = 'Delete Empty Masks'
LABEL_DELETE_UNUSED_GROUPS = 'Delete Unused Masks'
LABEL_CONVERT = 'Convert'
LABEL_NO_POLYS = 'No polys selected'
LABEL_NO_TAGS = 'No tags on selected polys'
LABEL_MAX_POLY = 'Too many to polys'
LABEL_MAX_FCL = 'Too many tags to list'
LABEL_NO_MASKS = 'No masks to display'
DIALOGS_NO_MASK_SELECTED = ("No Mask Selected", "Select a mask to apply.")
DIALOGS_TOO_MANY_MASKS = ("Too Many Masks", "Select only one mask to apply.")
DIALOGS_NO_PTAG_FILTER = ("No pTag Filter", "The selected mask applies to all polygons. No tag to apply.")
DIALOGS_NONE_PTAG_FILTER = ("(none) pTag Filter", "The selected mask applies to nothing. No tag to apply.")
DIALOGS_REMOVE_ALL_TAGS = ("Remove All Tags", "%s tags will be removed from the %s. Continue?")
DIALOGS_TAG_NOT_FOUND = ("Tag Not Found", "No instances of %s tag '%s' were found in the scene.")
DIALOGS_TAG_REPLACED = ("Tag Replaced", "Replaced %s instances of %s tag '%s'.")
DIALOGS_TAGGED_POLY_ISLANDS_COUNT = ("Tagged Polygons", "Tagged %s polygons in %s polygon islands.")
DIALOGS_TAGGED_POLYS_COUNT = ("Tagged Polygons", "Tagged %s polygons.")
DIALOGS_UNTAGGED_POLYS_COUNT = ("Removed Polygon Tags", "Removed %s polytags from %s polygons in the scene.")
DIALOGS_MASKED_TAGS_COUNT = ("Masked Unmasked Tags", "Added %s new masks.")
DIALOGS_NOTHING_TO_PASTE = ("Nothing to Paste", "Nothing to paste. Copy a tag before pasting.")
DIALOGS_TOO_MANY_ISLANDS = ("Too many islands", "Too many poly islands to mask safely. (Max %s, found %s)")
DIALOGS_REMOVED_ALL_TAGS = ("Removed tags", "Reset %s tags accross %s polygons in %s items.")
DIALOGS_CLEANED_UP_SHADERTREE = ("Cleaned up shader tree", "Removed %s items from the shader tree.")

POPUPS_CLIPBOARD = [
        (COPY, LABEL_COPY),
        (PASTE, LABEL_PASTE)
    ]

POPUPS_SCOPE = [
        (SCOPE_SELECTED, LABEL_SCOPE_SELECTED),
        (SCOPE_CONNECTED, LABEL_SCOPE_CONNECTED),
        (SCOPE_FLOOD, LABEL_SCOPE_FLOOD)
    ]

POPUPS_REMOVE_SCOPE = [
        (SCOPE_SELECTED, LABEL_SCOPE_SELECTED),
        (SCOPE_CONNECTED, LABEL_SCOPE_CONNECTED),
        (SCOPE_FLOOD, LABEL_SCOPE_FLOOD),
        (SCOPE_SCENE, LABEL_SCOPE_SCENE)
    ]

POPUPS_REMOVE_ALL_SCOPE = [
        (SCOPE_SELECTED_ITEMS, LABEL_SCOPE_SELECTED_ITEMS),
        (SCOPE_SCENE, LABEL_SCOPE_SCENE)
    ]

POPUPS_TAGTYPES = [
        (MATERIAL, LABEL_MATERIAL),
        (PART, LABEL_PART),
        (PICK, LABEL_PICK)
    ]

POPUPS_TAGTYPES_WITH_ALL = [
        (MATERIAL, LABEL_MATERIAL),
        (PART, LABEL_PART),
        (PICK, LABEL_PICK),
        (ALL, LABEL_ALL)
    ]

POPUPS_WITH_EXISTING = [
        (USE, LABEL_USE),
        (KEEP, LABEL_KEEP),
        (REMOVE, LABEL_REMOVE),
        (CONSOLIDATE, LABEL_CONSOLIDATE)
    ]

POPUPS_ADD_REMOVE = [(ADD, ADD.title()), (REMOVE, REMOVE.title())]

OPERATIONS_ADD = ADD
OPERATIONS_REMOVE = REMOVE
