import lx
from os import listdir, sep
from os.path import isfile, join, basename, splitext, dirname, isdir
from var import *

def presets_popup():
    popup_list = [(RANDOM, LABEL_RANDOM_COLOR)]
    popup_list.extend(list_presets())
    return popup_list

def string_beautify(string):
    return string.title().replace("_", " ")

def first_preset():
    presets = list_presets()

    if presets:
        return presets[0]

    elif not presets:
        return (None, None)

def list_presets():
    presets_paths = [
        "kit_mecco_tagger:basics"
    ]

    kelvin_presets = lx.eval('user.value mecco_tagger.includeKelvin ?')
    if kelvin_presets:
        presets_paths.append("kit_mecco_kelvin:Kelvin/kelvin_materials")

    user_presets = lx.eval('user.value mecco_tagger.userPresetsPath ?')
    if user_presets:
        presets_paths.append(user_presets)

    raw_presets_list = []
    for path in presets_paths:

        presets_folder = lx.eval("query platformservice alias ? {%s}" % path)

        if not isdir(presets_folder):
            continue

        for f in listdir(presets_folder):
            if f.startswith('.'):
                continue
            if splitext(f)[1] != '.lxp':
                continue
            if not isfile(join(presets_folder, f)):
                continue

            raw_presets_list.append(join(presets_folder, f))

    if not raw_presets_list:
        return []

    presets_list = []
    for p in raw_presets_list:
        nice_name = string_beautify(dirname(p).split(sep)[-1]) + " - "
        nice_name += string_beautify(splitext(basename(p))[0])
        internal_name = p
        presets_list.append((internal_name, nice_name))

    return presets_list
