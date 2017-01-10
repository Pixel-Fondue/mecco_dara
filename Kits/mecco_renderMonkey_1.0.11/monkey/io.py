# python

import os, traceback, json, re, random
import modo
import util, yaml

from symbols import *
from defaults import get


def yaml_save_dialog():
    """
    By Adam O'Hern for Mechanical Color

    File dialog requesting YAML file destination.
    """

    try:
        return os.path.normpath(
            modo.dialogs.customFile(
                dtype='fileSave',
                title='Save Batch File',
                names=['yaml'],
                unames=['Batch File (YAML)'],
                patterns=['*.yaml'],
                ext=['yaml']
            )
        )
    except:
        return False


def lxo_open_dialog():
    """
    By Adam O'Hern for Mechanical Color

    File dialog requesting LXO file source.
    """

    try:
        paths_list = modo.dialogs.customFile(
                dtype='fileOpenMulti',
                title='Select Scene File',
                names=('lxo',),
                unames=('MODO Scene file',),
                patterns=('*.lxo',),
        )
        return [os.path.normpath(i) for i in paths_list]
    except:
        return False

def image_save_dialg():
    savers = util.get_imagesavers()

    return modo.dialogs.customFile(
        'fileSave',
        'Image Destination',
        [i[0] for i in savers],
        [i[1] for i in savers],
        ext=[i[2] for i in savers],
    )

def yaml_open_dialog():
    """
    By Adam O'Hern for Mechanical Color

    File dialog requesting YAML file source.
    """

    try:
        return os.path.normpath(
            modo.dialogs.customFile(
                dtype='fileOpen',
                title='Select Batch File',
                names=('yaml',),
                unames=('renderMonkey Batch File',),
                patterns=('*.yaml',),
                path=None
            )
        )
    except:
        return False


def read_json(file_path):
    """
    By Adam O'Hern for Mechanical Color

    Returns a Python object (list or dict, as appropriate) from a given JSON file path.
    """

    try:
        json_file = open(file_path, 'r')
    except:
        util.debug(traceback.format_exc())
        return False

    try:
        json_object = json.loads(json_file.read())
    except:
        util.debug(traceback.format_exc())
        json_file.close()
        return False

    json_file.close()
    return json_object


def read_yaml(file_path):
    """
    By Adam O'Hern for Mechanical Color

    Returns a Python object (list or dict, as appropriate) from a given YAML file path.
    We use YAML because it's easier and more human readable than JSON. It's harder to mess up,
    easier to learn, and--imagine!--it supports commenting.

    Note: YAML does not support hard tabs (\t), so this script replaces those with four spaces ('    ').
    """

    yaml_file = open(file_path, 'r')
    yaml_data = yaml.safe_load(re.sub('\\t', '    ', yaml_file.read()))

    yaml_file.close()
    return yaml_data


def test_writeable(test_dir_path):
    """
    By Adam O'Hern for Mechanical Color

    Easier to ask forgiveness than permission.
    If the test path doesn't exist, tries to create it. If it can't, returns False.
    Then writes to a file in the target directory. If it can't, returns False.
    If all is well, returns True.
    """

    if not os.path.exists(test_dir_path):
        try:
            os.mkdir(test_dir_path)
        except OSError:
            return False

    test_path = os.path.join(test_dir_path, "tmp_%s.txt" % random.randint(100000, 999999))
    try:
        test = open(test_path, 'w')
        test.write("Testing write permissions.")
        test.close()
        os.remove(test_path)
        return True
    except:
        return False


def yamlize(data):
    return yaml.dump(data, indent=4, width=999, default_flow_style=False).replace("\n-", "\n\n-")


def write_yaml(data, output_path):
    if not test_writeable(os.path.dirname(output_path)):
        return False

    target = open(output_path, 'w')
    target.write("\n\n".join((yamlize(data), generate_readme())))
    target.close()

def generate_readme():
    readme = open(util.path_alias(':'.join((KIT_ALIAS, 'monkey/batch_file_docs.txt'))), 'r')
    readme = readme.read()

    substitutions = {
        'scene_path': SCENE_PATH,
        'format': FORMAT,
        'format_default': get(FORMAT),
        'frames': FRAMES,
        'frames_default': get(FRAMES),
        'destination': DESTINATION,
        'destination_default': get(DESTINATION),
        'output_pattern': PATTERN,
        'groups': GROUPS,
        'camera': CAMERA,
        'render_channels': RENDER_CHANNELS,
        'outputs': OUTPUTS,
        'width': WIDTH,
        'height': HEIGHT,
        'commands': COMMANDS,
        'frame_commands': FRAME_COMMANDS,
        'render_override': RENDER_OVERRIDE
    }

    substitutions['format_examples'] = "#" + "\n#".join(["    %s: %s (*.%s)" % (i[0],i[1],i[2]) for i in util.get_imagesavers()]) + "\n\n"

    substitutions['frames_examples'] = "#    '*'                       Start/end frames defined in scene file.\n"
    rr = ['1','1-5','5-1','0-10:2','1-21:5','1-3,10-16:2,20-23','1,1-5','(1 - 5),, 10-!@#15']
    substitutions['frames_examples'] += "#" + "\n#".join(["    '%s'%s%s" % (i," "*(24-len(i)),str(util.frames_from_string(i))) for i in rr]) + "\n\n"

    indent = 32
    rr = [
        ['*', 'Render output filenames defined in scene file.'],
        ['frames' + os.sep, os.path.normpath(os.sep + os.path.join('path','to','scene','file','frames'))],
        ['.frames' + os.sep, os.path.normpath(os.sep + os.path.join('path','to','scene','file','frames'))],
        [os.sep + os.path.join('path','with','filename.xyz'), os.path.normpath(os.sep + os.path.join('path','with','filename.jpg'))]
    ]
    substitutions['destination_examples'] = "#" + "\n#".join(["    %s%s%s" % (i[0]," "*(indent-len(i[0])),i[1]) for i in rr]) + "\n"

    rr = [
        os.sep + os.path.join('already','perfectly','good','path') + os.sep,
        os.sep + os.path.join('path','with','no','trailing_slash'),
        os.path.join('~','path','to','righteousness'),
        "kit_mecco_renderMonkey:path" + os.sep
    ]
    substitutions['destination_examples'] += "#" + "\n#".join(["    %s%s%s" % (i," "*(indent-len(i)),str(util.expand_path(i))) for i in rr]) + "\n\n"

    return readme.format(s=substitutions)
