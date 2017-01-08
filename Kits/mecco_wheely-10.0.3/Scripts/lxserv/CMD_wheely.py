#python
import sys
import lx

def exclog(script=''):
	""" Outputs error to log """
	lx.out("Exception \"%s\" on line %d: %s" % (sys.exc_value, sys.exc_traceback.tb_lineno, script))

import lxu
import lxifc
import re
from math import ceil, floor, pi, sin, cos
from copy import deepcopy
import mm_tags

""" RADIAL ARRAY HELPER
Usage notes:

"""

""" Constants """
# pi = math.pi
tau = 2.0*pi
radToDeg = 180.0/pi
"""####"""


""" Names """
NAME_CMD_HDKRADIAL_CREATE   = "mecco.wheely.create"
NAME_CMD_HDKRADIAL_COMMIT   = "mecco.wheely.commit"
NAME_CMD_HDKRADIAL_EDIT	 = "mecco.wheely.edit"

NAME_CMDARG_STEPS	   = "spokes"
NAME_CMDARG_RADIUS	  = "radius"
NAME_CMDARG_SEGMENTS	= "segments"
NAME_CMDARG_SIDES	   = "spans"
NAME_CMDARG_TOLERANCE   = "tolerance"

NAME_ITEM_NAME	  = "wheely"

NAME_CHAN_ROTAXIS   = "rot.X"

NAME_TAG			= "WHLY"
NAME_PTAG_INSTANCES = "Wheely Instances"
"""####"""


""" Symbols """
s_ACTIONLAYER_EDIT		  = lx.symbol.s_ACTIONLAYER_EDIT
s_ACTIONLAYER_SETUP		 = lx.symbol.s_ACTIONLAYER_SETUP
sTYPE_STRING				= lx.symbol.sTYPE_STRING
sTYPE_INTEGER			   = lx.symbol.sTYPE_INTEGER
sTYPE_FLOAT				 = lx.symbol.sTYPE_FLOAT
sTYPE_DISTANCE			  = lx.symbol.sTYPE_DISTANCE
sITYPE_GROUP				= lx.symbol.sITYPE_GROUP
sITYPE_MESH				 = lx.symbol.sITYPE_MESH
sITYPE_MESHINST			 = lx.symbol.sITYPE_MESHINST
sSELTYP_ITEM				= lx.symbol.sSELTYP_ITEM
sGRAPH_MESHINST			 = lx.symbol.sGRAPH_MESHINST
fCMDARG_OPTIONAL			= lx.symbol.fCMDARG_OPTIONAL
fCMDARG_QUERY			   = lx.symbol.fCMDARG_QUERY
fCMDARG_DYNAMIC_DEFAULTS	= lx.symbol.fCMDARG_DYNAMIC_DEFAULTS
fCMD_UI					 = lx.symbol.fCMD_UI
fCMD_UNDO				   = lx.symbol.fCMD_UNDO
fCMD_MODEL				  = lx.symbol.fCMD_MODEL
f_LAYERSCAN_PRIMARY		 = lx.symbol.f_LAYERSCAN_PRIMARY
f_LAYERSCAN_EDIT			= lx.symbol.f_LAYERSCAN_EDIT
f_MESHEDIT_GEOMETRY		 = lx.symbol.f_MESHEDIT_GEOMETRY
iPTYP_FACE				  = lx.symbol.iPTYP_FACE
iXFRM_POSITION			  = lx.symbol.iXFRM_POSITION
iXFRM_ROTATION			  = lx.symbol.iXFRM_ROTATION
iXFRM_SCALE				 = lx.symbol.iXFRM_SCALE
"""####"""

""" Global services """
svc_scene = lx.service.Scene()
svc_msg   = lx.service.Message()
svc_layer = lx.service.Layer()
svc_sel   = lx.service.Selection()
mo		= svc_msg.Allocate()
"""####"""

""" Selection types """
iSELTYP_ITEM = svc_sel.LookupType(sSELTYP_ITEM)
"""####"""


""" Global properties """
"""####"""


""" Item type integers """
iTYPE_GROUP	 = svc_scene.ItemTypeLookup(lx.symbol.sITYPE_GROUP)
iTYPE_MESH	  = svc_scene.ItemTypeLookup(lx.symbol.sITYPE_MESH)
iTYPE_MESHINST  = svc_scene.ItemTypeLookup(lx.symbol.sITYPE_MESHINST)
"""####"""


#Default replaced with user value "mecco_wheely_mergeDist" initialized in index
#""" Defaults """
#DEFAULT_TOLERANCE = 0.001
#"""####"""


""" Basic functions """

#returns current scene as an lxu.object.Scene instance
GetScene		= lxu.select.SceneSelection().current

def GetItemsOfType(nameFilter, *itemTypes):
	""" Returns all items in scene of *itemTypes (item type strings or ints),
		matching nameFilter string. Empty string or None will match all items. """
	scene = GetScene()
	items = []
	nameFilter = str() or nameFilter
	for itemType in itemTypes:
		try:
			if type(itemType) == str:
				itemType = svc_scene.ItemTypeLookup(itemType)
			if type(svc_scene.ItemTypename(itemType)) is type(None):
				raise LookupError
			num = scene.ItemCount(itemType)
			for n in xrange(num):
				item = scene.ItemByIndex(itemType, n)
				if nameFilter in item.UniqueName():
					items.append(scene.ItemByIndex(itemType, n))
		except LookupError:
			raise LookupError("item type \"%s\" not found" % itemType)
	return items

def clamp(value, lower=None, upper=None):
	""" Returns value no lower than lower and no greater than upper.
		Use None to clamp in one direction only. """
	if lower is not None:
		value = max(value, lower)
	if upper is not None:
		value = min(value, upper)
	return value

def StrToInt(s, default=None):
	""" Returns first valid integer in input string. """
	try:
		number = re.search(r"[-+]?\d*\d+|\d+", s).group(0)
		return int(number)
	except AttributeError:
		if default is not None:
			return default
		else:
			raise ValueError

def StrToFlt(s, default=None):
	""" Returns first valid float in input string. """
	try:
		number = re.search(r"[-+]?\d*\.\d+|\d+", s).group(0)
		return float(number)
	except AttributeError:
		if default is not None:
			return default
		else:
			raise ValueError

def InitXfrms(item):
	""" Initializes zero-transforms for a given item.
		item = lx.object.Item instance """
	try:
		#get a chanWrite interface
		scene = GetScene()
		chanRead = scene.Channels(s_ACTIONLAYER_EDIT, 0.0)
		chanWrite = lx.object.ChannelWrite(chanRead)

		#get a locator interface for item
		loc = lx.object.Locator(item)

		#scale
		try:
			scl = loc.GetTransformItem(iXFRM_SCALE)
		except LookupError:
			scl = loc.AddTransformItem(iXFRM_SCALE)[0]
		#position
		try:
			pos = loc.GetTransformItem(iXFRM_POSITION)
		except LookupError:
			pos = loc.AddTransformItem(iXFRM_POSITION)[0]
		#rotation
		try:
			rot = loc.GetTransformItem(iXFRM_ROTATION)
		except LookupError:
			rot = loc.AddTransformItem(iXFRM_ROTATION)[0]

		#write zeroes...
		for chanIdx in range(2, 5):
			chanWrite.Double(scl, chanIdx, 1.0)
			chanWrite.Double(pos, chanIdx, 0.0)
			chanWrite.Double(rot, chanIdx, 0.0)
	except:
		exclog("InitXfrms")
		raise Exception

def MakeInstances(item, steps):
	""" Creates steps-1 instances in a radial formation, using
		item as the source """

	scene = GetScene()
	chanRead = scene.Channels(s_ACTIONLAYER_EDIT, 0.0)
	chanWrite = lx.object.ChannelWrite(chanRead)
	angle = tau/steps
	for n in range(1, steps):
		#create a new instance of the mesh item
		inst = scene.ItemInstance(item)

		#set the instance to be a child of the mesh
		inst.SetParent(item)

		#initialize transforms for the instance
		InitXfrms(inst)

		#get a locator interface for the instance
		instLoc = lx.object.Locator(inst)
		instRot = instLoc.GetTransformItem(iXFRM_ROTATION)

		axis = NAME_CHAN_ROTAXIS
		try:
			chanIndex = instRot.ChannelList().index(axis)
		except ValueError:
			ident = instRot.Ident()
			raise LookupError("no such channel on item: {%s:%s}" % (ident, axis))

		rotValue = n*angle
		chanWrite.Double(instRot, chanIndex, rotValue)

"""####"""




class HDKRadial_Create(lxu.command.BasicCommand):
	def __init__(self):
		lxu.command.BasicCommand.__init__(self)
		self.dyna_Add(NAME_CMDARG_STEPS, sTYPE_INTEGER)
		self.dyna_Add(NAME_CMDARG_SIDES, sTYPE_INTEGER)
		self.dyna_Add(NAME_CMDARG_RADIUS, sTYPE_DISTANCE)

	def cmd_Flags(self):
		return fCMD_MODEL | fCMD_UNDO

	def cmd_Interact(self):
		pass
	def cmd_Execute(self,flags):
		try:
			steps	   = self.dyna_Int(0, 4)
			sides	   = self.dyna_Int(1, 8)
			diameter	= self.dyna_Float(2, 1.0)

			scene = GetScene()


			#angle per step
			angle = tau/steps

			lx.eval("layer.new")
			#get a LayerScan interface for our primary mesh layer, and we also want to edit it
			layerScan = lx.object.LayerScan(svc_layer.ScanAllocate(f_LAYERSCAN_PRIMARY | f_LAYERSCAN_EDIT))
			#if the test fails we must abort
			if layerScan.Count() is 0:
				raise Exception("no mesh layer")

			#our new mesh item
			item = lx.object.Item(layerScan.MeshItem(0))
			mesh = lx.object.Mesh(layerScan.MeshEdit(0))
			item_ident = item.Ident()

			#rename it and set some tags
			item.SetName(NAME_ITEM_NAME)
			mm_tags.set_tag(item, NAME_TAG, str(steps))

			#create geometry accessors
			pointAccessor = mesh.PointAccessor()
			polyAccessor  = mesh.PolygonAccessor()

			#list of points starting with one at origin
			pointList = [pointAccessor.New((0.0,0.0,0.0))]

			angleStart = -angle/2.0
			rotPerSide = angle/sides

			for a in range(sides+1):
				currentAngle = angleStart + a * rotPerSide
				x = 0.0
				y = cos(currentAngle) * diameter
				z = sin(currentAngle) * diameter
				pos = (x, y, z)

				point = pointAccessor.New(pos)
				pointList.append(point)

			for p in range(sides):
				#for each side in the wheel we create a triangle

				#first we get a list of the points needed
				points = [pointList[0], pointList[p+1], pointList[p+2]]
				#then we set up a storage buffer for the particular poly
				pointStorage = lx.object.storage()
				pointStorage.setType('p')
				pointStorage.setSize(3)
				pointStorage.set(points)

				#then we create a polygon from the buffer
				polyAccessor.New(iPTYP_FACE, pointStorage, 3, 0)

			#finally we apply the mesh changes
			layerScan.SetMeshChange(0, lx.symbol.f_MESHEDIT_GEOMETRY)
			layerScan.Apply()

			#we now move on to creating the instances
			MakeInstances(item, steps)
		except:
			exclog("HDKRadial_Create.cmd_Execute")
		return lx.result.OK

	def cmd_Query(self,index,vaQuery):
		try:
			va = lx.object.ValueArray(vaQuery)
			if index == 0:
				va.AddInt(8)
			elif index == 1:
				va.AddInt(4)
			elif index == 2:
				va.AddFloat(0.5)
		except:
			exclog("HDKRadial_Create.cmd_Query")
		return lx.result.OK
	def basic_Execute(self, flags, msg):
		pass


class HDKRadial_Commit(lxu.command.BasicCommand):
	def __init__(self):
		lxu.command.BasicCommand.__init__(self)
		self.dyna_Add(NAME_CMDARG_TOLERANCE, sTYPE_DISTANCE)
		self.basic_SetFlags(0, fCMDARG_OPTIONAL)

	def cmd_Flags(self):
		return fCMD_MODEL | fCMD_UNDO
	def cmd_Interact(self):
		pass
	def cmd_Execute(self,flags):
		#get the current scene and selection
		scene	 = GetScene()
		selection = lxu.select.ItemSelection().current()

		#get ItemGraph interface for instances
		inst_sceneGraph = scene.GraphLookup(sGRAPH_MESHINST)
		inst_itemGraph  = lx.object.ItemGraph(inst_sceneGraph)

		#read dynamic attributes
		DEFAULT_TOLERANCE = lx.eval('user.value {mecco_wheely_mergeDist} ?')
		tol = self.dyna_Float(0, DEFAULT_TOLERANCE)

		for item in selection:
			#make sure it's of the right type
			if not item.TestType(iTYPE_MESH):
				continue

			#make sure it's got the right tag
			try:
				tagData = mm_tags.get_tag(item, NAME_TAG)
			except:
				continue

			#if we made it this far everything must be ok
			item_ident = item.Ident()

			selectionList = [item_ident, ]

			#build list of idents for children
			children = [m.Ident() for m in item.SubList()]


			#drop selection
			lx.eval("select.drop item")

			#grab all instances that are also children
			for n in range(inst_itemGraph.FwdCount(item)):
				#get the instance for this index
				inst = inst_itemGraph.FwdByIndex(item, n)
				inst_ident = inst.Ident()
				#make sure instance is a child
				if inst_ident in children:
					lx.eval("select.item {%s} add" % inst_ident)

			#all instances selected, convert to meshes and assign ptag
			lx.eval("item.setType Mesh")
			lx.eval("poly.setPart {%s}" % NAME_PTAG_INSTANCES)


			""" temporary workaround:
				the layer.mergeMeshes command causes a crash
				when you undo. The workaround is to select
				only the former instances, cut their polygons,
				delete the items, and paste them into the
				first item.
			"""
			""" START BUGGED CODE """
			# selectionList.extend(
			#	 lx.evalN(
			#		 "query sceneservice selection ? mesh"
			#		 )
			#	 )
			# lx.eval("select.drop item")
			# for ident in selectionList:
			#	 lx.eval("select.item {%s} add" % ident)
			# lx.eval("layer.mergeMeshes true")
			""" END BUGGED CODE / START WORKAROUND """
			lx.eval("select.type polygon")
			lx.eval("cut")
			lx.eval("item.delete")
			lx.eval("select.item {%s} set" % item_ident)
			lx.eval("paste")
			""" END WORKAROUND """

			lx.eval("select.edge add bond equal")
			lx.eval("vert.merge fixed dist:%s morph:true disco:false" % tol)
			lx.eval("select.drop edge")

		lx.eval("select.type item")
		return lx.result.OK

	def cmd_Query(self,index,vaQuery):
		pass
	def basic_Execute(self, flags, msg):
		pass

class HDKRadial_Edit(lxu.command.BasicCommand):
	def __init__(self):
		lxu.command.BasicCommand.__init__(self)
	def cmd_Flags(self):
		return fCMD_MODEL | fCMD_UNDO
	def cmd_Interact(self):
		pass
	def cmd_Execute(self,flags):
		scene = GetScene()
		selection = lxu.select.ItemSelection().current()
		# GetSelection = lxu.select.ItemSelection().current
		selectionIdents = []
		for item in selection:
			if not item.TestType(iTYPE_MESH):
				continue
			try:
				tagData = mm_tags.get_tag(item, NAME_TAG)
			except LookupError:
				continue
			ident = item.Ident()
			name = item.UniqueName()
			steps = StrToInt(tagData)
			selectionIdents.append(ident)
			lx.eval("select.item {%s} set" % ident)
			lx.eval("select.drop polygon")
			lx.eval("select.polygon add part face {%s}" % NAME_PTAG_INSTANCES)
			lx.eval("delete")

			MakeInstances(item, steps)

		for ident in selectionIdents:
			lx.eval("select.item {%s} add" % ident)

		return lx.result.OK
	def cmd_Query(self,index,vaQuery):
		pass
	def basic_Execute(self, flags, msg):
		pass


lx.bless(HDKRadial_Create, NAME_CMD_HDKRADIAL_CREATE)
lx.bless(HDKRadial_Commit, NAME_CMD_HDKRADIAL_COMMIT)
lx.bless(HDKRadial_Edit, NAME_CMD_HDKRADIAL_EDIT)
