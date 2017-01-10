#python

import modo
from lx import symbol, out
from var import *

def random_color():
    import colorsys, random
    return colorsys.hsv_to_rgb(
        random.random(),
        DEFAULT_RANDOM_COLOR_SATURATION,
        DEFAULT_RANDOM_COLOR_VALUE
    )

def build_arg_string(arg_dict):
    arg_string = ''
    for k,v in arg_dict.iteritems():
        if v is not None:
            v = str(v) if str(v).isalnum() else '{%s}' % str(v)
            arg_string += " %s:%s" % (str(k),v)
    return arg_string

def convert_to_iPOLYTAG(tagType):
    if not tagType:
        return symbol.i_POLYTAG_MATERIAL
    elif tagType.lower() == 'material':
        return symbol.i_POLYTAG_MATERIAL
    elif tagType.lower() == 'part':
        return symbol.i_POLYTAG_PART
    elif tagType.lower() in ('pick', 'selection set'):
        return symbol.i_POLYTAG_PICK

def convert_to_tagType_string(tagType):
    if tagType in (symbol.i_POLYTAG_MATERIAL, 'Material'):
        return 'material'
    elif tagType in (symbol.i_POLYTAG_PART, 'Part'):
        return 'part'
    elif tagType in (symbol.i_POLYTAG_PICK, 'Selection Set'):
        return 'pick'

def convert_to_tagType_label(tagType):
    if tagType in (symbol.i_POLYTAG_MATERIAL, 'Material', 'material'):
        return LABEL_MATERIAL
    elif tagType in (symbol.i_POLYTAG_PART, 'Part', 'part'):
        return LABEL_PART
    elif tagType in (symbol.i_POLYTAG_PICK, 'Selection Set', 'pick'):
        return LABEL_PICK

def convert_to_sICHAN_MASK_PTYP(tagType):
    if tagType in (symbol.i_POLYTAG_MATERIAL, 'material'):
        return 'Material'
    elif tagType in (symbol.i_POLYTAG_PART, 'part'):
        return 'Part'
    elif tagType in (symbol.i_POLYTAG_PICK, 'pick'):
        return 'Selection Set'

def safe_removeItems(items, children = False):
    for i in items:
        # make sure item exists before trying to delete it
        # (lest ye crash)
        try:
            modo.Item(i.id)
        except:
            continue

        modo.Scene().removeItems(i, children)
