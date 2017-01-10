# python

import lx, modo
import os, traceback, re, sys
import defaults

from os.path import basename
from math import copysign


def debug(string):
    """
    By Adam O'Hern for Mechanical Color

    Prints a string to lx.out() if defaults.get('debug') returns True. (See defaults.py)
    Intended for developer debugging only; user messages should use 'status'.
    """
    if defaults.get('debug'):
        t = traceback.extract_stack()[-2]
        lx.out("debug '{}' line {}, {}".format(basename(t[0]), t[1], t[2], string))


def breakpoint(string):
    """
    By Adam O'Hern for Mechanical Color

    Essentially a breakpoint function for debugging purposes.
    Prints a string to lx.out() and, if defaults.get('breakpoint') returns True, throws a dialog as well. 
    (See defaults.py)
    """
    t = traceback.extract_stack()[-2]
    string = "'{}' line {}, {}(): {}".format(basename(t[0]), t[1], t[2], string)

    if defaults.get('breakpoints'):
        lx.out("breakpoint: ", string)
        if defaults.get('breakpoints'):
            if modo.dialogs.okCancel("breakpoint", string) == 'cancel':
                sys.exit()


def status(string):
    """
    By Adam O'Hern for Mechanical Color

    Prints a string to lx.out(). Differs from "debug" only in that it's always enabled.
    Useful for user-related messages.
    """

    lx.out("status: {}".format(string))


def markup(pre, string):
    """
    By Adam O'Hern for Mechanical Color

    Returns a formatting string for modo treeview objects.
    Requires a prefix (usually "c" or "f" for colors and fonts respectively),
    followed by a string.

    Colors are done with "\03(c:color)", where "color" is a string representing a
    decimal integer computed with 0x01000000 | ((r << 16) | (g << 8) | b).
    Italics and bold are done with "\03(c:font)", where "font" is the string
    FONT_DEFAULT, FONT_NORMAL, FONT_BOLD or FONT_ITALIC.

    \03(c:4113) is a special case gray color specifically for treeview text.
    """
    return '\03({}:{})'.format(pre, string)


def bitwise_rgb(r, g, b):
    """
    By Adam O'Hern for Mechanical Color

    Input R, G, and B values (0-255), and get a bitwise RGB in return.
    (Used for colored text in treeviews.)
    """
    return str(0x01000000 | ((r << 16) | (g << 8 | b)))


def bitwise_hex(h):
    """
    By Adam O'Hern for Mechanical Color

    Input an HTML color hex (#ffffff), and get a bitwise RGB in return.
    (Used for colored text in treeviews.)
    """
    h = h.strip()
    if h[0] == '#':
        h = h[1:]
    r, g, b = h[:2], h[2:4], h[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return bitwise_rgb(r, g, b)


def get_imagesaver(key):
    """
    By Adam O'Hern for Mechanical Color

    Returns a tuple with three elements: name, username, and file extension.
    """

    savers = get_imagesavers()

    match = None
    for i in savers:
        if str(i[0]).lower() == key.lower():
            match = i
            break

    return match


def get_imagesavers():
    """
    By The Foundry
    http://sdk.luxology.com/wiki/Snippet:Image_Savers

    Returns a list of available image savers. Each entry in the returned list
       is a tuple made up of the format's internal name, it's username and it's
       DOS type (extension).
    """
    host_svc = lx.service.Host()
    savers = []
    for x in range(host_svc.NumServers('saver')):
        saver = host_svc.ServerByIndex('saver', x)
        out_class = saver.InfoTag(lx.symbol.sSAV_OUTCLASS)
        if out_class == 'image' or out_class == 'layeredimage':
            name = saver.Name()
            uname = saver.UserName()
            try:
                dostype = saver.InfoTag(lx.symbol.sSAV_DOSTYPE)
            except:
                dostype = ''
            savers.append((name, uname, dostype,))
    return savers


def expand_path(input_string):
    """
    By Adam O'Hern for Mechanical Color

    Returns a normalized absolute path with trailing slash based on an input string.

    Examples:
    "/path/with/file.xyz"               becomes     "/path/with/file.xyz"
    "/path/with/no_trailing_slash"      becomes     "/path/with/no_trailing_slash/"
    "/already/perfectly/good/path/"     becomes     "/already/perfectly/good/path/"
    "frames/"                           becomes     "/path/to/scene/file/frames/"
    "./frames/"                         becomes     "/path/to/scene/file/frames/"
    "~/fruit/loops/"                    becomes     "/path/to/user/home/fruit/loops/"
    "pathalias:path/to/righteousness"   becomes     "/expanded/path/alias/path/to/righteousness/"

    NOTE: Parsing is rather primitive. If the string begins with "~", it assumes you're parsing a
    user folder. If it starts with ".", it assumes a relative path from the current scene. If it
    contains a ":" anywhere at all, it assumes a MODO path alias.
    """

    input_string = os.path.normpath(input_string)

    if input_string.startswith(os.path.sep):
        full_path = input_string

    elif input_string.startswith('~'):
        try:
            full_path = os.path.expanduser(input_string)
        except:
            return False

    elif ":" in input_string:
        try:
            full_path = lx.eval("query platformservice alias ? {{{}}}".format(input_string))
        except:
            debug('Could not expand path alias. Path cannot be parsed.')
            return False

    else:
        try:
            current_scene_path = os.path.dirname(lx.eval('query sceneservice scene.file ? current'))
        except:
            debug('Could not get current scene folder. Path cannot be parsed.')
            return False

        if input_string.startswith('.'):
            full_path = os.path.join(current_scene_path, input_string[1:])
        else:
            full_path = os.path.join(current_scene_path, input_string)

    if not os.path.splitext(full_path)[1]:
        full_path = os.path.join(full_path, '')

    full_path = os.path.normpath(full_path)
    return full_path


def path_alias(path):
    """
    By Adam O'Hern for Mechanical Color

    Expand modo path alias, e.g. "kit_mecco_renderMonkey:test/passGroups.lxo"
    """
    try:
        return lx.eval("query platformservice alias ? {{{}}}".format(path))
    except:
        return False


def get_scene_render_range():
    start = modo.Scene().renderItem.channel('first').get()
    end = modo.Scene().renderItem.channel('last').get()

    return "-".join((str(start), str(end)))


def frames_from_string(input_string="*"):
    """
    By Simon Lundberg & Adam O'Hern for Mechanical Color

    function:
        parses a string on the form "1, 5, 10-20:2" into a range like this:
        [1, 5, 10, 12, 14, 16, 18, 20]
        Filters out illegal stuff to it won't break if you make typos.
        Filters out duplicate frames, so "1, 1, 1, 1-5" will only output
        [1, 2, 3, 4, 5], rather than [1, 1, 1, 1, 2, 3, 4, 5]
    syntax:
        Commas divide up each "chunk".
        If there is a dash ("-") in a chunk, it gets treated as a range of frames.
        If there is also a colon (":") in the chunk, that number indicates the frame step.

        In the case of two colons present, like this: "2:0-100:3", the last one
        will take precedence (the range becomes 0-100 step 3, not step 2).

        In the case of a colon but no dash, like this: "3:5", the colon is ignored and
        only the first number is parsed.

        To get a negative frame step (rendering 1-100, starting at 100), simply enter
        the large number first and the lower number after, like this: "100-1". Negative
        frame steps are ignored.
    output:
        returns a LIST object with INTEGERS for each frame in the range, in the same order
        they were entered. Does NOT SORT. This is easy to do once it's a list anyway:
            sortedList = frames_from_string(myRangeString).sort()
    """
    try:
        input_string = get_scene_render_range() if input_string == "*" else input_string

        frames = []

        cleanstring = ''.join([i for i in input_string if i in "0123456789-:,"])
        range_strings = cleanstring.split(',')

        for rangeString in range_strings:
            if "-" not in rangeString[1:]:
                try:
                    frames.append(int(re.split(r"\D", rangeString)[0]))
                except:
                    pass
                continue

            bookends = rangeString.split('-')
            start, end = bookends[0], bookends[1]
            step = 1

            if ":" in start:
                parts = start.split(":")
                start = filter_numerical(parts[-1])
                step = filter_numerical(parts[0])
            if ":" in end:
                parts = end.split(":")
                end = filter_numerical(parts[0])
                step = filter_numerical(parts[-1])

            try:
                start = int(start)
                end = int(end)
                step = int(step)
            except ValueError:
                debug('Error in {}'.format(rangeString))
                break

            step = max(step, 1)

            if start > end:
                step *= -1
                sign = int(copysign(1, step))
                first = max(start, end)
                last = min(start, end)+sign
            else:
                sign = int(copysign(1, step))
                first = min(start, end)
                last = max(start, end)+sign
            try:
                frames.extend(range(first, last, step))
            except:
                debug('Error in {}'.format(rangeString))

        frames = list(orderedSet(frames))
        return frames if frames else False

    except:
        debug(traceback.format_exc())


def filter_numerical(string):
    return "".join([c for c in string if c in "0123456789.-"]) if string else None


def check_output_paths():
    """
    By Simon Lundberg and Adam O'Hern for Mechanical Color

    utility function
    returns True if there is at least one render output that is:
       Enabled, has an output path, an output format, and all its parents
       are enabled as well, and the top-level parent is the Render item
    """

    for output in modo.Scene().iterItems('renderOutput'):
        output_path = output.channel('filename').get()
        output_format = output.channel('format').get()
        output_enable = check_enable(output)
        if all((output_path, output_format, output_enable)):
            return True

    return False


def check_enable(texture):
    """
    By Simon Lundberg and Adam O'Hern for Mechanical Color

    iterates through shader tree parents of item "texture"
    returns True if all shader tree parents are enabled; otherwise False
    uses recursion to work its way through hierarchy
    """

    if not texture.channel('enable'):
        return False
    if texture.parent.type == "polyRender":
        return True
    if texture.parent.type == "scene":
        return False

    return check_enable(texture.parent)


def get_user_value(name):
    if not lx.eval("!query scriptsysservice userValue.isDefined ? {{{}}}".format(name)):
        return None
    return lx.eval("!user.value {{{}}} ?".format(name))


def set_or_create_user_value(name, value, valueType="string", life="config", username=None):
    """
    By Simon Lundberg for Mechanical Color

    sets a user value
    if user value does not exist, it creates it first
    """
    try:
        lx.eval("!user.value {{{}}} {{{}}}".format(name, value))
        if username:
            lx.eval("!user.def name:{{{}}} attr:username value:{{{}}}".format(name, username))
    except:
        try:
            lx.eval("!user.defNew {{{}}} {{{}}} {{{}}}".format(name, valueType, life))
            lx.eval("!user.value {{{}}} {{{}}}".format(name, value))
        except:
            lx.out("Error creating user value: ", "; ".join((name, valueType, life)))
            return


def build_arg_string(arg_dict):
    arg_string = ''
    for k, v in arg_dict.iteritems():
        if v is not None:
            v = str(v) if str(v).isalnum() else '{{{}}}'.format(str(v))
            arg_string += " {}:{}".format(str(k), v)
    return arg_string


def orderedSet(sequence):
    checked = []
    for i in sequence:
        if i not in checked:
            checked.append(i)
    return checked
