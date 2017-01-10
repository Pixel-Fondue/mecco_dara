#!/usr/bin/env python

################################################################################
#
# cj.matcap
#
# Version: 1.1
#
# Author: Tim Vazquez - CGM Studios
# Email: tim@cgmstudios.com
#
# Description: Dyamically creates a popup list of available matcaps.
#
# Added view3d.shadingStyle advgl command when switching
#
################################################################################

import lx
import lxifc
import lxu
import os
import re
import glob
import traceback
import time

KIT_NAME = "mecco_bling"
MATCAP_PREFIX = "bling_"
IMAGE_FOLDER = "Images"
ASSETS_FOLDER = ""
MATCAP_FOLDER = ""
RESOURCES_FOLDER = "Resources"
TN_FOLDER = "thumbs_cache"
MATCAP_NAME = "mecco_bling"
TN_W = 32
TN_H = 32

created = False
glob_CJ_MatcapList = ''
selected_image = ''


def getMatcapImage(matcapName):
    scene_svc = lx.service.Scene()
    scene = lxu.select.SceneSelection().current()
    shadeloc_graph = lx.object.ItemGraph(scene.GraphLookup(lx.symbol.sGRAPH_SHADELOC))
    matcap_item = scene.ItemLookup(matcapName)

    for x in range(shadeloc_graph.FwdCount(matcap_item)):
        next_item = shadeloc_graph.FwdByIndex(matcap_item, x)
        if next_item.Type():
            next_item_type = next_item.Type()
            if next_item_type == scene_svc.ItemTypeLookup(lx.symbol.sITYPE_VIDEOSTILL):
                return scene.ItemLookup(next_item.Ident())

    return False


def GetTNImage(w, h, path=None, R=255.0, G=255.0, B=255.0, A=255.0):
    imgSrvc = lx.service.Image()
    im = imgSrvc.Create(w, h, lx.symbol.iIMP_RGB24, 0)

    iout = lx.object.ImageWrite(im)

    pixel = lx.object.storage()
    pixel.setType('b')
    pixel.setSize(w * 4)

    for ih in range(h):
        pixel.set((R, G, B, A) * w)
        iout.SetLine(ih, lx.symbol.iIMP_RGBA32, pixel)

    if path != None:
        imLOAD = imgSrvc.Load(path)
        imgSrvc.Resample(im, imLOAD, 0)

    return im


def findKitPath():
    pltSrvc = lx.service.Platform()

    paths = []

    for i in range(pltSrvc.PathCount()):
        paths.append(pltSrvc.PathByIndex(i))

    for i in range(pltSrvc.ImportPathCount()):
        paths.append(pltSrvc.ImportPathByIndex(i))

    for path in paths:
        try:
            checkedPath = os.path.join(path, KIT_NAME)
            if os.path.isdir(checkedPath):
                return checkedPath
        except:
            pass

    return None


class imageCache():
    imageCahce = {}

    def addImage(self, image, TN):
        if not self.imageCahce.has_key(image):
            #lx.out('++ Adding Image: %s' % image)
            imgSrvc = lx.service.Image()
            im = imgSrvc.Load(TN)
            self.imageCahce[image] = im

    def removeImage(self, image):
        if self.imageCahce.has_key(image):
            #lx.out('-- Removing Image: %s' % image)
            del self.imageCahce[image]

    def GetImageTN(self, index):
        if self.imageCahce.has_key(index):
            return self.imageCahce[index]
        else:
            return


class CJ_MatcapList(lxifc.UIValueHints):
    def __init__(self):
        self._imagePaths = []
        self.imageCahce = imageCache()
        self._list = self.getMatcapList()
        self._notifiers = [('select.event', 'item +vdlt')]

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_POPUPS

    def uiv_PopCount(self):
        return len(self._list)

    def uiv_PopUserName(self, index):
        return self._list[index]

    def uiv_PopInternalName(self, index):
        return self._imagePaths[index]

    def uiv_PopIconSize(self):
        return (TN_W, TN_W, TN_H)

    def uiv_PopIconImage(self, index):
        return self.imageCahce.GetImageTN(self._imagePaths[index])

    #return GetTNImage(self._imagePaths[index],TN_W,TN_H)

    def uiv_NotifierCount(self):
        return len(self._notifiers)

    def uiv_NotifierByIndex(self, index):
        return self._notifiers[index]

    def getMatcapList(self):
        kitPath = findKitPath()

        names = []
        self._imagePaths = []
        if kitPath != None:
            images = glob.glob(os.path.join(kitPath, ASSETS_FOLDER, IMAGE_FOLDER, MATCAP_FOLDER, "%s*" % MATCAP_PREFIX))

            # Adam's hack to make sure we're only getting image files
            images = [image for image in images if
                      os.path.isfile(image) and re.search('([^\\s]+(\\.(?i)(jpg|png|psd|exr|tga))$)', image.lower())]

            tnFolder = os.path.join(kitPath, RESOURCES_FOLDER, TN_FOLDER)

            if not os.path.isdir(tnFolder):
                os.mkdir(tnFolder)

            for image in images:
                baseName = os.path.basename(image)[:-4]
                cleanFileName = baseName.replace(MATCAP_PREFIX, "")
                modTime = os.path.getmtime(image)
                TN_Name = "%s_%s_%s" % (modTime, baseName, TN_W)

                Full_TN_Search_Path = os.path.join(tnFolder, "*_%s_%s*" % (baseName, TN_W))
                Full_TN_Path = os.path.join(tnFolder, TN_Name)

                Existing_TN = glob.glob(Full_TN_Search_Path)

                if len(Existing_TN) > 0:
                    #check out mod times
                    tnMod = float(os.path.basename(Existing_TN[0]).split('_')[0])
                    if modTime > tnMod:
                        os.remove(Existing_TN[0])
                        self.imageCahce.removeImage(image)
                        self.makeTN(image, Full_TN_Path)

                    else:
                        Full_TN_Path = Existing_TN[0][:-4]
                else:
                    self.makeTN(image, Full_TN_Path)

                self._imagePaths.append(image)
                names.append(cleanFileName)

                self.imageCahce.addImage(image, "%s.png" % Full_TN_Path)

        names.append('(none)')
        names.append('Open Matcaps Folder')
        names.append('Update Images')
        self._imagePaths.append('(none)')
        self._imagePaths.append('openFolder')
        self._imagePaths.append('updateImages')
        return names

    def makeTN(self, image, Full_TN_Path):
        #lx.out('TN dest path: '+Full_TN_Path)
        imgSrvc = lx.service.Image()
        tnObj = GetTNImage(TN_W, TN_H, image, A=0)
        imgSrvc.Save(tnObj, "%s.png" % Full_TN_Path, "PNG", None)


class mecco_cmd_bling(lxu.command.BasicCommand):
    def __init__(self):

        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('image', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)
        self.imageCache = imageCache()

        global created
        global glob_CJ_MatcapList

        if not created:
            created = True
            glob_CJ_MatcapList = CJ_MatcapList()
        self.matcap_list = glob_CJ_MatcapList

    def arg_UIValueHints(self, index):
        return self.matcap_list

    def basic_ButtonName(self):
        return "Matcap"

    def basic_Execute(self, msg, flags):
        try:
            self.CMD_EXE(msg, flags)
        except Exception:
            #lx.out(traceback.format_exc())
            lx.eval(
                'layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')

    def CMD_EXE(self, msg, flags):

        image = self.dyna_String(0, "(none)")
        scnSel = lxu.select.SceneSelection().current()
        render = self.lookUP('Render')
        scnSrv = lx.service.Scene()

        global created
        global selected_image

        if image == "(none)":
            self.removeMatCap()

        if image == "openFolder":
            lx.eval('file.open {%s}' % os.path.join(findKitPath(), ASSETS_FOLDER, IMAGE_FOLDER, MATCAP_FOLDER))

        if image == "updateImages":
            created = False
            if not os.path.isfile(selected_image):
                self.removeMatCap()

        if os.path.isfile(image) or not created and os.path.isfile(selected_image):
            self.removeMatCap()

            if created:
                selected_image = image

            matCapObj = scnSel.ItemAdd(scnSrv.ItemTypeLookup('matcapShader'))
            matCapObj.SetName(MATCAP_NAME)

            parentGraph = scnSel.GraphLookup('parent')
            itemGraph = lx.object.ItemGraph(parentGraph)
            childrenCount = itemGraph.RevCount(render)
            itemGraph.SetLink(matCapObj, -1, render, -1)

            lx.eval('clip.addStill {%s}' % selected_image)
            lx.eval('item.channel videoStill$colorspace "nuke-default:sRGB"')
            lx.eval('select.item {%s} set' % matCapObj.Ident())
            imageName = os.path.basename(selected_image)
            lx.eval('matcap.image {%s:videoStill001}' % imageName[:imageName.rfind('.')])

            self.writeChannel(matCapObj, 'glOnly', 1)
            self.writeChannel(matCapObj, 'gamma', 1.0)

            try:
                # Since we currently can not target a GL window, we
                # are wrapping this in a try just in case there is no available
                # GL window, or we are focused on a UV window
                lx.eval('!!view3d.shadingStyle advgl')
            except:
                pass

    def removeMatCap(self):
        scnSel = lxu.select.SceneSelection().current()
        existingMatCap = self.lookUP(MATCAP_NAME)
        if existingMatCap != None:
            scnSel.ItemRemove(getMatcapImage(MATCAP_NAME))
            scnSel.ItemRemove(existingMatCap)

    def cmd_Query(self, index, vaQuery):
        pass

    def lookUP(self, itemName):

        scnSel = lxu.select.SceneSelection().current()

        try:
            itemObj = scnSel.ItemLookup(itemName)
        except:
            return None

        return itemObj

    def writeChannel(self, item, channelName, value, actionLayer='edit', valType=None):
        scnSel = lxu.select.SceneSelection().current()
        chan = scnSel.Channels(actionLayer, 0.0)
        chnWrite = lx.object.ChannelWrite(chan)

        try:
            idx = item.ChannelLookup(channelName)

            if valType == None:
                valType = type(value)

            if valType == str:
                return chnWrite.String(item, idx, str(value))
            elif valType == int:
                return chnWrite.Integer(item, idx, int(value))
            elif valType == float:
                return chnWrite.Double(item, idx, float(value))
        except Exception, e:
            #lx.out('%s - %s : %s' % (channelName,value,traceback.format_exc()))
            return "Error"

    def basic_Enable(self, msg):
        return True


lx.bless(mecco_cmd_bling, "mecco.bling")
