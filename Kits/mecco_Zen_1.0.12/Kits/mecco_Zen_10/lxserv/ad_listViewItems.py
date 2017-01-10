#python

# by Simon Lundberg, pilfered and modded by Adam O'Hern

import lx
import lxifc
import lxu.command
import sys


VIEW_CMD_NAME = "view3d_zen.viewFromItem"
POPULATE_CMD_NAME = "view3d_zen.listItems"
VIEW_POPUP_NAME = "view3d_zen.viewItemPopup"
SET_RENDER_CAM_UVALUE = "view3d_zen.SetRenderCam"
SHOW_CAM_UVALUE = "view3d_zen.ShowCamList"
SHOW_LGT_UVALUE = "view3d_zen.ShowLgtList"
FIRST_RUN_UVALUE = "view3d_zen.FirstRun"
OVERFLOW_THRESHOLD_UVALUE = "view3d_zen.OverflowThreshold"


def exclog(script=''):
    lx.out("Exception \"%s\" on line %d: %s" % (sys.exc_value, sys.exc_traceback.tb_lineno, script))

def ItemsOfType(itype=None):
    #Lists all items of type "itype" in scene
    #None means all items in scene
    #TODO:
    #       Switch to using Python API hooks
    #       instead of old query sceneservice
    #       method (2013-12-02)

    try:
        if not itype:
            itype = "item"
        items = []
        n_items = lx.eval("query sceneservice %s.n ?" % itype)
        for index in xrange(n_items):
            item_id = lx.eval("query sceneservice %s.id ? {%s}" % (itype, index))
            items.append(item_id)
        return items
    except:
        exclog("ItemsOfType")
        return None

def GetUserValue(name, default=None):
    try:
        return lx.eval('user.value "{}" ?'.format(name))
    except RuntimeError:
        if default is None:
            raise
        return default


def shortenLists(maxLength, *input_lists):
    newLists = [list(l) for l in input_lists]
    overflows = [[] for n in input_lists]
    # newLists.reverse()

    while sum(len(l) for l in newLists) > maxLength:
        maxIndex = max(enumerate(newLists), key = lambda tup: len(tup[1]))[0]
        longestList = newLists[maxIndex]
        overflows[maxIndex].append(longestList.pop())

    # newLists.reverse()
    # overflows.reverse()
    [o.reverse() for o in overflows]
    return zip(newLists, overflows)


class ViewItemList_FCL(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class ViewItemList_Popup(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._items[0])

    def uiv_PopUserName(self,index):
        return self._items[1][index]

    def uiv_PopInternalName(self,index):
        return self._items[0][index]


class ViewItemPopup(lxu.command.BasicCommand):
    """
        Creates a Popup list of "fromItems", a semi-colon separated
        list of items.

        Syntax:
                (command name) ?item:string mode:string fromItems:string
                item:       the item to use; queryable for menu to choose which
                mode:       string (really integer), gets passed to VIEW_CMD_NAME
                fromItems:  string consisting of semi-colon separated items (camera001;camera013;)

        TODO:
                - mode should probably be an integer
                - sceneservice queries should be replaced with API hooks
    """
    def __init__(self):
        try:
            lxu.command.BasicCommand.__init__(self)
            self.dyna_Add("item", lx.symbol.sTYPE_STRING)
            self.dyna_Add("mode", lx.symbol.sTYPE_STRING)
            self.dyna_Add("fromItems", lx.symbol.sTYPE_STRING)

            self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)
            self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)
        except:
            exclog("ViewItemPopup: __init__")


    def arg_UIValueHints(self, index):
        try:
            #first we try to get the list of items to display
            #if the argument isn't used, we just default to a blank
            #string.
            try:
                itemlist = self.attr_GetString(2).split(';')
            except:
                itemlist = ''

            #"itemlist" is a list of item IDs; we need to build a list
            #of item names to go with that.
            itemnames = []
            for item in itemlist:
                name = lx.eval("query sceneservice item.name ? {%s}" % item)
                itemnames.append(name)

            items = [tuple(itemlist), tuple(itemnames)]
            if index == 0:
                return ViewItemList_Popup(items)
        except:
            exclog("ViewItemPopup: arg_UIValueHints")

    def cmd_Execute(self,flags):
        #When executing the command, it simply uses the lx.eval()
        #method, passing to it a formatted command string.
        try:
            item = self.dyna_String(0)
            mode = self.dyna_String(1)
            lx.eval(VIEW_CMD_NAME + " {0} {1}".format(mode, item))
        except:
            exclog("ViewItemPopup: cmd_Execute")

    def cmd_Query(self,index,vaQuery):
        return lx.result.OK

    def basic_ButtonName(self):
        #The label on the popup list is "More:" to indicate that there
        #are more items to choose from
        return "More:"


class ViewItemList_Populate(lxu.command.BasicCommand):
    """
        Populates the list of commands to be fired: one for each
        light and camera in the scene, plus special cases.
    """
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('cmds', lx.symbol.sTYPE_INTEGER)
        self.dyna_Add('autoCamera', lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)


    def arg_UIValueHints(self, index):
        """
            Build list of commands.
            "commandList" gets rebuilt every time the UI updates
            The first commands are a labeled divider for "Cameras", followed
            by two special-case buttons, one for render cam and one for selected
            camera. Then it gets a list of all cameras and all lights in the scene,
            and builds additional buttons for all the cameras. The lights are within
            their own labeled divider.

            syntax:
                cmds:       Query this to return list of view-setting commmands
                autoCamera: Boolean attribute, if true it will automatically set the
                            viewport to camera as soon as popup appears. Leave this out
                            or set it to false if using in a non-popup.

            TODO:
                - USERNAMES on buttons! (2013-11-27) (done 2013-12-02)
                - Add preference (user value?) for overflow_limit (2013-12-02)
        """

        try:
            commandList = []
            showCams = GetUserValue(SHOW_CAM_UVALUE, 1)
            showLgts = GetUserValue(SHOW_LGT_UVALUE, 1)

            # if showCams:
            #     commandList.extend([    "user.value " + SET_RENDER_CAM_UVALUE + " ?",
            #                             VIEW_CMD_NAME + " 1",
            #                             VIEW_CMD_NAME + " 0"])

            cameras = ItemsOfType(lx.symbol.sITYPE_CAMERA)
            lights = ItemsOfType(lx.symbol.sITYPE_LIGHT)

            if index == 0 and cameras:
                auto = self.dyna_Bool(1, 0)
                if auto == 1:
                    lx.eval("view3d.projection cam")

            overflow_limit = int(GetUserValue(OVERFLOW_THRESHOLD_UVALUE, 15))

            try:
                croppedLists = shortenLists(overflow_limit, cameras, lights)

                cam_lists = croppedLists[0]
                lgt_lists = croppedLists[1]

                cameras_short = cam_lists[0]
                if len(cam_lists[1])==1:
                    #if there is only one item in the "overflow",
                    #we move it to the standard list
                    cameras_short.extend(cam_lists[1])
                    cameras_overflow = None
                else:
                    cameras_overflow = cam_lists[1]

                lights_short = lgt_lists[0]
                if len(lgt_lists[1])==1:
                    lights_short.extend(lgt_lists[1])
                    lights_overflow = None
                else:
                    lights_overflow = lgt_lists[1]
            except:
                exclog()
                return None

            if showCams:
                for camera in cameras_short:
                    commandList.append(VIEW_CMD_NAME + " 1 {" + camera + "}")
                if cameras_overflow:
                    commandList.append(VIEW_POPUP_NAME + " ? 1 " + ";".join(cameras_overflow))


            if showLgts:
                if showCams:
                    commandList.append("- ")

                commandList.append(VIEW_CMD_NAME + " 2")

                #LIGHTS
                for light in lights_short:
                    commandList.append(VIEW_CMD_NAME + " 2 {" + light + "}")
                if lights_overflow:
                    commandList.append(VIEW_POPUP_NAME + " ? 2 " + ";".join(lights_overflow))

            if index == 0:
                return ViewItemList_FCL(commandList)
        except:
            exclog("ViewItemList_Populate: arg_UIValueHints")

    def cmd_Execute(self,flags):
        # dummy execute method
        pass

    def cmd_Query(self,index,vaQuery):
        # dummy query method
        pass



def setViewCam(item='', renderCam=False):
    """
        Sets current 3D viewport to camera type. Special case
        "renderCam" means a different command is used. If "item"
        is left blank, the command will end up using whichever
        item is selected. If setRenderCam is True, it will also
        set the render camera to the clicked-on camera.
    """
    try:
        try:
            lx.eval("view3d.projection cam")
            viewport = True
        except:
            viewport = False

        if renderCam:
            if viewport:
                lx.eval("view3d.renderCamera")
        else:
            setRenderCam = GetUserValue(SET_RENDER_CAM_UVALUE, 1)
            if item and setRenderCam:
                lx.eval("render.camera {%s}" % item)
            if viewport:
                lx.eval("view3d.cameraItem {%s}" % item)
    except:
        exclog("setViewCam")

def setViewLgt(item=''):
    """
        Sets current 3D viewport to light type.
        Same syntax as setViewCam, except there is no
        render light, meaning no special cases.
    """
    try:
        lx.eval("view3d.projection lgt")
        lx.eval("view3d.lightItem {%s}" % item)
    except:
        exclog("setViewLgt")


class SetViewFromItem(lxu.command.BasicCommand):
    """
        Command encapsulates two commands:
            "view3d.projection (cam|lgt)", which sets the 3D view to either light or camera
            "view3d.cameraItem"/"view3d.lightItem", which sets the item to be used

        Syntax:
            "mode" argument determines mode according to the following:
                0: render camera
                1: specified camera; if "item" argument is blank it will use selection
                2: specified light; if "item" argument is blank it will use selection
            "item" argument determines which item should be used, if mode is 1 or 2.
            If mode is 0, "item" is ignored. A blank string for the item to be used
            works fine.

        TODO:
            Is dyna_String correctly? "mode" should probably be "dyna_Int" or something.
            Need to look up syntax for this. 2013-11-27
    """
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('mode', lx.symbol.sTYPE_INTEGER)
        self.dyna_Add('item', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.scene = lxu.select.SceneSelection().current()

    def cmd_Flags(self):
        return lx.symbol.fCMD_UI | lx.symbol.fCMDBLOCK_UI

    def cmd_Execute(self, flags):
        try:
            #modes:
            #   0:  render camera
            #   1:  specified camera
            #   2:  specified light
            mode = int(self.dyna_String(0, ""))
            item = self.dyna_String(1, "")

            if mode == 0:
                setViewCam(renderCam=True)
            elif mode == 1:
                setViewCam(item)
            elif mode == 2:
                setViewLgt(item)
            else:
                sys.exit()
        except:
            exclog(VIEW_CMD_NAME)

    def basic_ButtonName(self):
        #initialize mode and item
        try:
            mode, item, itemName = None, None, None
            modes = {   "0": 0,
                        "rendercam": 0,
                        "render": 0,
                        "rendercamera": 0,
                        "1": 1,
                        "cam": 1,
                        "camera": 1,
                        "2": 2,
                        "lgt": 2,
                        "light": 2}

            try:
                if self.dyna_IsSet(0):
                    mode_read = self.attr_GetString(0)
                    if mode_read in modes:
                        mode = modes[mode_read]
            except:
                exclog("self.attr_GetString(0)")
                return "ERROR: Getting mode"

            if self.dyna_IsSet(1):
                item = self.attr_GetString(1)

            if item:
                try:
                    itemName = self.scene.ItemLookupIdent(item).UniqueName()
                except:
                    #item not found
                    itemName = "ERROR: Item '{0}' not found".format(item)
                    exclog()

            if mode == 0:
                return "(Render Camera)     "
            elif mode in (1, 2):
                if item:
                    return str(itemName)
                elif mode == 1:
                    return "(Selected Camera)"
                elif mode == 2:
                    return "(Selected Light)"
            else:
                return "ERROR: Mode not set"
        except:
            exclog("SetViewFromItem: basic_ButtonName")
            return "ERROR"


try:
    lx.bless(SetViewFromItem, VIEW_CMD_NAME)
    lx.bless(ViewItemList_Populate, POPULATE_CMD_NAME)
    lx.bless(ViewItemPopup, VIEW_POPUP_NAME)
except:
    exclog("Blessing")
