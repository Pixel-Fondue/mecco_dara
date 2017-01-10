# python

import lx, lxu, lxifc, modo

import monkey
from monkey.symbols import *
from monkey.util import markup, bitwise_rgb, bitwise_hex
# from monkey.util import debug, breakpoint

from os.path import basename

# Text Colors
RED = markup('c', bitwise_rgb(255, 0, 0))
BLUE = markup('c', bitwise_hex('#0e76b7'))
GRAY = markup('c', '4113')

# Font Styles
FONT_DEFAULT = markup('f', 'FONT_DEFAULT')
FONT_NORMAL = markup('f', 'FONT_NORMAL')
FONT_BOLD = markup('f', 'FONT_BOLD')
FONT_ITALIC = markup('f', 'FONT_ITALIC')


class TreeNode(object):

    _primary = None

    def __init__(self, key, value=None, parent=None, node_region=None, value_type=None, selectable=True, ui_only=False):
        self._key = key
        self._value = value
        self._parent = parent
        self._node_region = node_region
        self._value_type = value_type
        self._children = []
        self._state = 0
        self._selected = False
        self._selectable = selectable
        self._ui_only = ui_only
        self._tooltips = {}

        self._columns = ((COL_NAME, -1), (COL_VALUE, -3))

    @classmethod
    def set_primary(cls, primary=None):
        cls._primary = primary

    @classmethod
    def primary(cls):
        return cls._primary

    def add_child(self, key, value=None, node_region=None, value_type=None, selectable=True, ui_only=False):
        self._children.append(TreeNode(key, value, self, node_region, value_type, selectable, ui_only))
        return self._children[-1]

    def clear_children(self):
        if len(self._children) > 0:
            for child in self._children:
                self._children.remove(child)

    def clear_selection(self):
        if self.primary():
            self.set_primary(None)

        self.set_selected(False)

        for child in self._children:
            child.clear_selection()

    def ui_only(self):
        return self._ui_only

    def set_ui_only(self, ui_only=True):
        self._ui_only = ui_only

    def set_selected(self, val=True):
        if val:
            self.set_primary(self)
        self._selected = val

    def is_selected(self):
        return self._selected

    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def add_state_flag(self, flag):
        self._state = self._state | flag

    def set_tooltip(self, idx, tip):
        self._tooltips[idx] = tip

    def tooltip(self, idx):
        if idx in self._tooltips:
            return self._tooltips[idx]

    def raw_value(self):
        return self._value

    def display_value(self):
        m = ''
        if self._value_type in (list.__name__, dict.__name__, tuple.__name__):
            m = GRAY
        elif self._node_region == REGIONS[1]:
            m = GRAY
        elif self._node_region == REGIONS[5]:
            m = GRAY

        if self._node_region == REGIONS[1]:
            v = self.child_by_key(SCENE_PATH).raw_value()
        elif self._value_type == IMAGE_FORMAT:
            v = monkey.util.get_imagesaver(self._value)[1]
        else:
            v = str(self._value)

        return m + v

    def display_name(self):
        m = ''
        if self._node_region == REGIONS[1]:
            m = ''
        elif self._ui_only:
            m = GRAY
        elif self._node_region == REGIONS[7]:
            m = FONT_BOLD
        elif isinstance(self._key, int):
            m = GRAY

        if self._node_region == REGIONS[1]:
            k = basename(self.child_by_key(SCENE_PATH).raw_value())
        elif isinstance(self._key, int):
            k = str(self._key + 1)
        else:
            k = str(self._key)
            k = k.replace('_', ' ')
            k = k.title() if "." not in k else k

        return m + k

    def key(self):
        return str(self._key)

    def set_key(self, key):
        self._key = key

    def node_region(self):
        return str(self._node_region)

    def set_node_region(self, node_region):
        self._node_region = node_region
        return self._node_region

    def set_value(self,value):
        self._value = value

    def value_type(self):
        return self._value_type

    def set_value_type(self, value_type):
        self._value_type = value_type
        return self._value_type

    def selectable(self):
        return self._selectable

    def set_selectable(self, selectable=True):
        self._selectable = selectable

    def columns(self):
        return self._columns

    def child_by_key(self, key):
        for child in self._children:
            if key == child.key():
                return child
        return False

    def selected_children(self, recursive=True):
        sel = []
        for child in self._children:
            if child.is_selected():
                sel.append(child)
            if recursive:
                sel += child.selected_children()

        return sel

    def ancestors(self, path=None):
        if self._parent:
            return self._parent.ancestors() + [self]
        else:
            return path if path else []

    def ancestor_keys(self):
        return [ancestor.key() for ancestor in self.ancestors()[1:]]

    def parent(self):
        return self._parent

    def children(self):
        return self._children

    def insert_child(self, index, node):
        self._children.insert(index, node)

    def parent_child_index(self):
        return self.parent().children().index(self)

    def set_parent_child_index(self,index):
        self.destroy()
        self.parent().insert_child(index, self)

    def reorder_up(self):
        if self.parent_child_index() > 0:
            self.set_parent_child_index(self.parent_child_index()-1)

    def reorder_down(self):
        if self.parent_child_index() + 1 < len(
                [i for i in self.parent().children() if not i.ui_only()]
        ):
            self.set_parent_child_index(self.parent_child_index()+1)

    def reorder_top(self):
        self.set_parent_child_index(0)

    def reorder_bottom(self):
        self.set_parent_child_index(
            len([i for i in self.parent().children() if not i.ui_only()]) - 1
        )

    def select_shift_up(self):
        if self.parent_child_index() > 0:
            self.set_selected(False)
            self.parent().children()[self.parent_child_index() - 1].set_selected()

    def select_shift_down(self):
        if self.parent_child_index() + 1 < len(
                [i for i in self.parent().children() if not i.ui_only()]
        ):
            self.set_selected(False)
            self.parent().children()[self.parent_child_index() + 1].set_selected()

    def update_child_keys(self):
        if self.value_type() in (list.__name__, tuple.__name__):
            legit_kids = [child for child in self.children() if not child.ui_only()]
            for key, child in enumerate(sorted(legit_kids, key=lambda x: x.key())):
                child.set_key(key if isinstance(key, int) else child.key())

    def destroy(self):
        self.clear_selection()
        self.parent().children().remove(self)

    def tier(self):
        return len(self.ancestors())


class BatchManager:

    def __init__(self, batch_file_path=''):
        self._batch_file_path = batch_file_path
        self._tree = TreeNode(TREE_ROOT_TITLE, LIST)

        self.regrow_tree()

    def add_task(self, paths_list, batch_root_node=None):
        if not batch_root_node:
            batch_root_node = self._tree.children()[0]

        if not paths_list:
            return False

        paths_list = paths_list if isinstance(paths_list, list) else [paths_list]

        for path in paths_list:
            self.grow_node([{SCENE_PATH: path, FRAMES: monkey.defaults.get(FRAMES)}], batch_root_node, 1)

        if self._batch_file_path:
            self.save_to_file()
        else:
            self.save_temp_file()

        self.regrow_tree()

    def node_file_root(self, tree_node):
        return tree_node.ancestors()[0]

    def set_batch_file(self, file_path=None):
        self._batch_file_path = file_path

    def close_file(self):
        self._tree.clear_selection()
        self._batch_file_path = None
        self.regrow_tree()

    def save_to_file(self, file_path=None):
        if file_path:
            self._batch_file_path = file_path

        elif not self._batch_file_path:
            self._batch_file_path = monkey.io.yaml_save_dialog()

        return monkey.io.write_yaml(self.tree_to_object(), self._batch_file_path)

    def save_temp_file(self):
        file_path = monkey.util.path_alias(':'.join((KIT_ALIAS, QUICK_BATCH_PATH)))
        if monkey.batch.batch_has_status(file_path):
            monkey.batch.batch_status_delete(file_path)
        self.save_to_file(file_path)

    @staticmethod
    def iterate_anything(obj):
        if isinstance(obj, (list, tuple)):
            return {k: v for k, v in enumerate(obj)}.iteritems()
        if isinstance(obj, dict):
            return obj.iteritems()

    def grow_node(self, branch, parent_node, depth=0):

        if depth == 0:
            node_region = REGIONS[1]
            add_node = ADD_TASK
            add_region = REGIONS[8]
        elif depth == 1:
            node_region = REGIONS[2]
            add_node = ADD_PARAM
            add_region = REGIONS[9]
        elif depth == 2:
            node_region = REGIONS[4]
            add_node = ADD_GENERIC
            if isinstance(branch, dict):
                add_region = REGIONS[11]
            else:
                add_region = REGIONS[10]
        else:
            node_region = REGIONS[6]
            add_node = ADD_GENERIC
            if isinstance(branch, dict):
                add_region = REGIONS[11]
            else:
                add_region = REGIONS[10]

        if isinstance(branch, (list, tuple, dict)):
            for key, value in sorted(self.iterate_anything(branch)):

                if key == SCENE_PATH:
                    value_type = PATH_OPEN_SCENE
                elif key == DESTINATION:
                    value_type = PATH_SAVE_IMAGE
                elif key == FORMAT:
                    value_type = IMAGE_FORMAT
                elif key == FRAMES:
                    value_type = FRAME_RANGE
                else:
                    value_type = type(value).__name__

                if isinstance(value, (list, tuple, dict)):
                    node = parent_node.add_child(key, value_type, node_region, value_type)
                    self.grow_node(value, node, depth + 1)

                else:
                    parent_node.add_child(key, value, node_region, value_type)

        parent_node.add_child(add_node, EMPTY, add_region, selectable=False, ui_only=True)

    def regrow_tree(self):
        batch_file_path = self._batch_file_path if self._batch_file_path else NO_FILE_SELECTED

        self._tree.clear_selection()
        self._tree.clear_children()

        batch_root_node = self._tree.add_child(
            BATCHFILE,
            batch_file_path,
            REGIONS[7]
        )

        batch_root_node.add_state_flag(fTREE_VIEW_ITEM_EXPAND)

        if self._batch_file_path:
            batch = monkey.io.read_yaml(self._batch_file_path)
            self.grow_node(batch, batch_root_node)

        if len(batch_root_node.children()) == 0:
            batch_root_node.add_child(ADD_TASK, EMPTY, REGIONS[8], selectable=False, ui_only=True)

        return self._tree

    def node_data(self, node):
        if node.value_type() in (list.__name__, tuple.__name__):
            data = []
            for child in node.children():
                if not child.ui_only():
                    child_value = self.node_data(child)
                    data.append(child_value)
            return data

        elif node.value_type() == dict.__name__:
            data = {}
            for child in node.children():
                if not child.ui_only():
                    child_value = self.node_data(child)
                    data[child.key()] = child_value
            return data

        elif node.value_type() == type(None).__name__:
            return None

        else:
            return node.raw_value()

    def tree_to_object(self):
        batch = []
        for child in self._tree.child_by_key(BATCHFILE).children():
            if child.value_type() is not None:
                batch.append(self.node_data(child))
        return batch

    def batch_file_path(self):
        return self._batch_file_path

    def tree(self):
        return self._tree


_BATCH = BatchManager()


class BatchTreeView(lxifc.TreeView,
                    lxifc.Tree,
                    lxifc.ListenerPort,
                    lxifc.Attributes
                    ):

    _listenerClients = {}

    def __init__(self, node=None, current_index=0):

        if node is None:
            node = _BATCH.tree()

        self.m_currentNode = node
        self.m_currentIndex = current_index

    @classmethod
    def addListenerClient(cls, listener):
        tree_listener_obj = lx.object.TreeListener(listener)
        cls._listenerClients[tree_listener_obj.__peekobj__()] = tree_listener_obj

    @classmethod
    def removeListenerClient(cls, listener):
        tree_listener_object = lx.object.TreeListener(listener)
        if tree_listener_object.__peekobj__() in cls._listenerClients:
            del cls._listenerClients[tree_listener_object.__peekobj__()]

    @classmethod
    def notify_NewShape(cls):
        for client in cls._listenerClients.values():
            if client.test():
                client.NewShape()

    @classmethod
    def notify_NewAttributes(cls):
        for client in cls._listenerClients.values():
            if client.test():
                client.NewAttributes()

    def lport_AddListener(self, obj):
        self.addListenerClient(obj)

    def lport_RemoveListener(self, obj):
        self.removeListenerClient(obj)

    def targetNode(self):
        return self.m_currentNode.children()[self.m_currentIndex]

    def tree_Spawn(self, mode):
        new_tree = BatchTreeView(self.m_currentNode, self.m_currentIndex)
        new_tree_obj = lx.object.Tree(new_tree)

        if mode == lx.symbol.iTREE_PARENT:
            new_tree_obj.ToParent()

        elif mode == lx.symbol.iTREE_CHILD:
            new_tree_obj.ToChild()

        elif mode == lx.symbol.iTREE_ROOT:
            new_tree_obj.ToRoot()

        return new_tree_obj

    def tree_ToParent(self):
        m_parent = self.m_currentNode.parent()

        if m_parent:
            self.m_currentIndex = m_parent.children().index(self.m_currentNode)
            self.m_currentNode = m_parent

    def tree_ToChild(self):
        self.m_currentNode = self.m_currentNode.children()[self.m_currentIndex]

    def tree_ToRoot(self):
        self.m_currentNode = _BATCH.tree()

    def tree_IsRoot(self):
        if self.m_currentNode == _BATCH.tree():
            return True
        else:
            return False

    def tree_ChildIsLeaf(self):
        if len(self.m_currentNode.children()) > 0:
            return False
        else:
            return True

    def tree_Count(self):
        return len(self.m_currentNode.children())

    def tree_Current(self):
        return self.m_currentIndex

    def tree_SetCurrent(self, index):
        self.m_currentIndex = index

    def tree_ItemState(self, guid):
        return self.targetNode().state()

    def tree_SetItemState(self, guid, state):
        self.targetNode().set_state(state)

    def treeview_ColumnCount(self):
        return len(_BATCH.tree().columns())

    def treeview_ColumnByIndex(self, columnIndex):
        return _BATCH.tree().columns()[columnIndex]

    def treeview_ToPrimary(self):
        if self.m_currentNode.primary():
            self.m_currentNode = self.m_currentNode.primary()
            self.tree_ToParent()
            return True
        return False

    def treeview_IsSelected(self):
        return self.targetNode().is_selected()

    def treeview_Select(self, mode):

        if mode == lx.symbol.iTREEVIEW_SELECT_PRIMARY:
            _BATCH.tree().clear_selection()

            if self.targetNode().selectable():
                self.targetNode().set_selected()
            else:
                self.targetNode().parent().set_selected()

        elif mode == lx.symbol.iTREEVIEW_SELECT_ADD and self.targetNode().selectable():
            self.targetNode().set_selected()

        elif mode == lx.symbol.iTREEVIEW_SELECT_REMOVE:
            self.targetNode().set_selected(False)

        elif mode == lx.symbol.iTREEVIEW_SELECT_CLEAR:
            _BATCH.tree().clear_selection()

    def treeview_ToolTip(self, column_index):
        tooltip = self.targetNode().tooltip(column_index)
        if tooltip:
            return tooltip
        lx.notimpl()

    def treeview_IsInputRegion(self, column_index, regionID):
        if regionID == 0:
            return True
        if self.targetNode().node_region() == REGIONS[regionID]:
            return True

        return False

    def attr_Count(self):
        return len(_BATCH.tree().columns())

    def attr_GetString(self, index):
        if index == 0:
            return self.targetNode().display_name()

        elif self.targetNode().display_value():
            return self.targetNode().display_value()

        else:
            return EMPTY


class BatchOpen(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        path = monkey.io.yaml_open_dialog()
        if path:
            _BATCH.set_batch_file(path)
            _BATCH.regrow_tree()
            BatchTreeView.notify_NewShape()


class BatchClose(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        _BATCH.close_file()
        BatchTreeView.notify_NewShape()


class BatchAddTask(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        paths_list = monkey.io.lxo_open_dialog()
        if not isinstance(paths_list, list):
            paths_list = [paths_list]

        if paths_list:
            for path in paths_list:
                _BATCH.add_task(path)
            BatchTreeView.notify_NewShape()


class BatchAddParam(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('parameter', lx.symbol.sTYPE_STRING)

    def basic_Execute(self, msg, flags):
        param = self.dyna_String(0).lower() if self.dyna_IsSet(0) else None
        if not param:
            return lx.symbol.e_FAILED

        primary_node = _BATCH.tree().primary()
        if not primary_node:
            lx.out("Nothing selected.")
            return lx.symbol.e_FAILED

        sel = _BATCH.tree().children()[0].selected_children()
        sel = set([node for node in sel if node.node_region() == REGIONS[1]])
        sel = [node for node in sel if not param in [child.key() for child in node.children()]]

        val = monkey.defaults.get(param)
        if val is None:
            lx.out("Invalid parameter name.")
            return lx.symbol.e_FAILED

        if isinstance(val, (list, tuple, dict)):
            val = type(val).__name__
            val_type = val
        elif param == SCENE_PATH:
            val_type = PATH_SAVE_SCENE
        elif param == FORMAT:
            val_type = IMAGE_FORMAT
        elif param == DESTINATION:
            val_type = PATH_SAVE_IMAGE
        else:
            val_type = type(val).__name__

        for node in sel:
            new_node = node.add_child(param, val, REGIONS[2], val_type)
            new_node.reorder_bottom()

            if val_type in (list.__name__, tuple.__name__, dict.__name__):
                region = REGIONS[11] if val_type == dict.__name__ else REGIONS[10]
                new_node.add_child(ADD_GENERIC, EMPTY, region, selectable=False, ui_only=True)
                new_node.add_state_flag(fTREE_VIEW_ITEM_EXPAND)

        _BATCH.save_to_file()
        BatchTreeView.notify_NewShape()


class BatchAddToList(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('value', lx.symbol.sTYPE_STRING)

    def basic_Execute(self, msg, flags):
        value = self.dyna_String(0) if self.dyna_IsSet(0) else None
        if not value:
            return lx.symbol.e_FAILED

        primary_node = _BATCH.tree().primary()
        if not primary_node:
            lx.out("Nothing selected.")
            return lx.symbol.e_FAILED

        sel = _BATCH.tree().children()[0].selected_children()
        sel = set([node for node in sel if node.value_type() in (list.__name__, tuple.__name__)])
        sel = [node for node in sel if not value in [child.raw_value() for child in node.children()]]

        if not sel:
            lx.out("Invalid selection.")
            return lx.symbol.e_FAILED

        for node in sel:
            new_node = node.add_child(len(node.children())-1,value,REGIONS[4],type(value).__name__)
            new_node.reorder_bottom()

        _BATCH.save_to_file()
        BatchTreeView.notify_NewShape()


class BatchAddToDict(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('key', lx.symbol.sTYPE_STRING)
        self.dyna_Add('value', lx.symbol.sTYPE_STRING)

    def basic_Execute(self, msg, flags):
        key = self.dyna_String(0) if self.dyna_IsSet(0) else None
        value = self.dyna_String(1) if self.dyna_IsSet(0) else None
        if not key or not value:
            return lx.symbol.e_FAILED

        primary_node = _BATCH.tree().primary()
        if not primary_node:
            lx.out("Nothing selected.")
            return lx.symbol.e_FAILED

        sel = _BATCH.tree().children()[0].selected_children()
        sel = set([node for node in sel if node.value_type() == dict.__name__])
        sel = [node for node in sel if not key in [child.key() for child in node.children()]]

        if not sel:
            lx.out("Invalid selection.")
            return lx.symbol.e_FAILED

        for node in sel:
            new_node = node.add_child(key,value,REGIONS[4],type(value).__name__)
            new_node.reorder_bottom()

        _BATCH.save_to_file()
        BatchTreeView.notify_NewShape()


class BatchDeleteNodes(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        sel = _BATCH.tree().selected_children()
        _BATCH.tree().clear_selection()

        for node in sel:
            if node.key() != SCENE_PATH:
                node.destroy()
                node.parent().update_child_keys()

        _BATCH.save_to_file()

        BatchTreeView.notify_NewShape()


class BatchReorderNodes(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def basic_Execute(self, msg, flags):
        mode = self.dyna_String(0).lower() if self.dyna_IsSet(0) else REORDER_ARGS['TOP']

        if mode not in [v for k, v in REORDER_ARGS.iteritems()]:
            lx.out("Wow, no idea to do with \"{}\". Sorry.".format(mode))
            return lx.symbol.e_FAILED

        sel = _BATCH.tree().selected_children()

        for node in sel:
            if mode == REORDER_ARGS['TOP']:
                node.reorder_top()
            elif mode == REORDER_ARGS['BOTTOM']:
                node.reorder_bottom()
            elif mode == REORDER_ARGS['UP']:
                node.reorder_up()
            elif mode == REORDER_ARGS['DOWN']:
                node.reorder_down()

        _BATCH.save_to_file()
        BatchTreeView.notify_NewShape()

        # Unsure why we lose selection, but we do. Have to re-select.
        _BATCH.tree().clear_selection()
        for node in sel:
            node.set_selected()


class BatchSelectShift(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def basic_Execute(self, msg, flags):
        mode = self.dyna_String(0).lower() if self.dyna_IsSet(0) else SELECT_SHIFT_ARGS['UP']

        if mode not in [v for k, v in SELECT_SHIFT_ARGS.iteritems()]:
            lx.out("Wow, no idea to do with \"{}\". Sorry.".format(mode))
            return lx.symbol.e_FAILED

        sel = _BATCH.tree().selected_children()

        for node in sel:
            if mode == SELECT_SHIFT_ARGS['UP']:
                node.select_shift_up()
            elif mode == SELECT_SHIFT_ARGS['DOWN']:
                node.select_shift_down()

        BatchTreeView.notify_NewShape()

        # Unsure why we lose selection, but we do. Have to re-select.
        _BATCH.tree().clear_selection()
        for node in sel:
            node.set_selected()


class BatchEditNodes(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        primary_node = _BATCH.tree().primary()
        if not primary_node:
            lx.out("Nothing selected.")
            return lx.symbol.e_FAILED

        sel = _BATCH.tree().children()[0].selected_children()
        if len(set([i.value_type() for i in sel])) > 1:
            sel = [_BATCH.tree().primary()]

        if primary_node.node_region() == REGIONS[1]:
            path = monkey.io.lxo_open_dialog()
            if path is not False:
                for node in sel:
                    node.child_by_key(SCENE_PATH).set_value(path)

        elif primary_node.value_type() == PATH_OPEN_SCENE:
            path = monkey.io.lxo_open_dialog()
            if path is not False:
                for node in sel:
                    node.set_value(path)

        elif primary_node.value_type() == PATH_SAVE_IMAGE:
            path = monkey.io.image_save_dialg()
            format = lx.eval("dialog.fileSaveFormat ? format")

            if path is not False:
                for node in sel:
                    node.set_value(path)
                    if node.parent().child_by_key(FORMAT):
                        node.parent().child_by_key(FORMAT).set_value(format)
                    else:
                        new_node = node.parent().add_child(FORMAT, format, REGIONS[2], IMAGE_FORMAT)
                        new_node.reorder_bottom()

        elif primary_node.value_type() == IMAGE_FORMAT:
            path = monkey.io.image_save_dialg()
            format = lx.eval("dialog.fileSaveFormat ? format")

            if path is not False:
                for node in sel:
                    if node.parent().child_by_key(DESTINATION):
                        node.parent().child_by_key(DESTINATION).set_value(path)
                    else:
                        new_node = node.parent().add_child(DESTINATION, path, REGIONS[2], PATH_SAVE_IMAGE)
                        new_node.reorder_bottom()

                    node.set_value(format)

        elif primary_node.value_type() == FRAME_RANGE:
            old_value = primary_node.raw_value()
            lx.eval('monkey.BatchEditString')
            frames_list = monkey.util.frames_from_string(primary_node.raw_value())
            if not frames_list:
                modo.dialogs.alert('Invalid Frame Range','Invalid frame range.','error')
                primary_node.set_value(old_value)
            else:
                for node in sel:
                    node.set_value(''.join([i for i in primary_node.raw_value() if i in "0123456789-:,"]))


        elif primary_node.value_type() in (int.__name__, float.__name__):
            try:
                lx.eval('monkey.BatchEditNumber')
            except:
                pass

        elif primary_node.value_type() == (str.__name__):
            try:
                lx.eval('monkey.BatchEditString')
            except:
                pass

        BatchTreeView.notify_NewShape()
        _BATCH.save_to_file()


class BatchEditNodesAdvanced(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        primary_node = _BATCH.tree().primary()
        if not primary_node:
            lx.out("Nothing selected.")
            return lx.symbol.e_FAILED

        sel = _BATCH.tree().children()[0].selected_children()
        if len(set([i.value_type() for i in sel])) > 1:
            sel = [_BATCH.tree().primary()]

        if primary_node.node_region() == REGIONS[1]:
            path = monkey.io.lxo_open_dialog()
            if path is not False:
                for node in sel:
                    node.child_by_key(SCENE_PATH).set_value(path)

        elif primary_node.value_type() == PATH_OPEN_SCENE:
            try:
                lx.eval('monkey.BatchEditString')
            except:
                pass

        elif primary_node.value_type() == PATH_SAVE_IMAGE:
            try:
                lx.eval('monkey.BatchEditString')
            except:
                pass

        elif primary_node.value_type() == IMAGE_FORMAT:
            try:
                lx.eval('monkey.BatchEditString')
            except:
                pass

        elif primary_node.value_type() == FRAME_RANGE:
            try:
                lx.eval('monkey.BatchEditString')
            except:
                pass

        elif primary_node.value_type() in (int.__name__, float.__name__):
            try:
                lx.eval('monkey.BatchEditNumber')
            except:
                pass

        elif primary_node.value_type() == (str.__name__):
            try:
                lx.eval('monkey.BatchEditString')
            except:
                pass

        BatchTreeView.notify_NewShape()
        _BATCH.save_to_file()


class BatchEditNumber(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('value', lx.symbol.sTYPE_FLOAT)

    def basic_Execute(self, msg, flags):
        if not self.dyna_IsSet(0) or self.dyna_Float(0) is None:
            return lx.symbol.e_FAILED

        sel = _BATCH.tree().children()[0].selected_children()
        if not sel:
            return lx.symbol.e_FAILED

        if len(set([i.value_type() for i in sel])) > 1:
            sel = [_BATCH.tree().primary()]

        for node in sel:
            if self.dyna_Float(0).is_integer():
                node.set_value(int(self.dyna_Float(0)))
            else:
                node.set_value(self.dyna_Float(0))

    def cmd_DialogInit(self):
        self.attr_SetFlt(0, float(_BATCH.tree().primary().raw_value()))


class BatchEditString(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('value', lx.symbol.sTYPE_STRING)

    def basic_Execute(self, msg, flags):
        if not self.dyna_IsSet(0) or self.dyna_String(0) is None:
            return lx.symbol.e_FAILED

        sel = _BATCH.tree().children()[0].selected_children()
        if not sel:
            return lx.symbol.e_FAILED

        if len(set([i.value_type() for i in sel])) > 1:
            sel = [_BATCH.tree().primary()]

        for node in sel:
            node.set_value(self.dyna_String(0))

    def cmd_DialogInit(self):
        self.attr_SetString(0, str(_BATCH.tree().primary().raw_value()))


class BatchResetNodes(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        primary_node = _BATCH.tree().primary()
        if not primary_node:
            lx.out("Nothing selected.")
            return lx.symbol.e_FAILED

        sel = _BATCH.tree().children()[0].selected_children()
        sel = set([node for node in sel if node.node_region() == REGIONS[2]])

        for node in sel:
            node.set_value(monkey.defaults.get(node.key()))

        BatchTreeView.notify_NewAttributes()
        _BATCH.save_to_file()


class BatchRender(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add('mode', lx.symbol.sTYPE_STRING)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)

    def basic_Execute(self, msg, flags):
        try:
            mode = self.dyna_String(0).lower() if self.dyna_IsSet(0) else 'run'

            if _BATCH._batch_file_path:
                dry = False
                if mode == 'test':
                    dry = True

                res = 1
                if mode == 'half':
                    res = .5
                elif mode == 'quarter':
                    res = .25
                elif mode == 'eighth':
                    res = .125
                elif mode == 'sixteenth':
                    res = 1.0/16

                monkey.batch.run(_BATCH.batch_file_path(), dry_run=dry, res_multiply=res)

            else:
                return lx.symbol.e_FAILED

        except SystemExit:
            pass


class BatchExample(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        path = monkey.util.path_alias(':'.join((KIT_ALIAS, QUICK_BATCH_PATH)))
        if path:
            lx.eval('{} {{{}}}'.format(CMD_BatchExportTemplate, path))
            _BATCH.set_batch_file(path)
            _BATCH.regrow_tree()
            BatchTreeView.notify_NewShape()


class BatchOpenStatusFile(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        path = _BATCH.batch_file_path()
        if not path:
            modo.dialogs.alert("no batch file", "No batch file selected.", 'error')
            return lx.symbol.e_FAILED
        if not monkey.batch.batch_has_status(path):
            modo.dialogs.alert("no status file", "No batch status file exists.", 'error')
            return lx.symbol.e_FAILED

        lx.eval('file.open {{{}}}'.format(monkey.batch.batch_status_file(path)))


class BatchOpenInFilesystem(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        if _BATCH.batch_file_path():
            lx.eval('file.open {{{}}}'.format(_BATCH.batch_file_path()))


class BatchRevealInFilesystem(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        if _BATCH.batch_file_path():
            lx.eval('file.revealInFileViewer {{{}}}'.format(_BATCH.batch_file_path()))


class BatchNew(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        path = monkey.io.yaml_save_dialog()
        if path:
            monkey.io.write_yaml([], path)

            _BATCH.set_batch_file(path)
            _BATCH.regrow_tree()
            BatchTreeView.notify_NewShape()


class BatchSaveAs(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        path = monkey.io.yaml_save_dialog()
        if path:
            _BATCH.save_to_file(path)
            BatchTreeView.notify_NewShape()


class BatchOpenTaskScene(lxu.command.BasicCommand):
    def basic_Execute(self, msg, flags):
        sel = _BATCH.tree().children()[0].selected_children()
        sel = set([node for node in sel if node.node_region() == REGIONS[1]])
        if len(sel):
            for node in sel:
                lx.eval('scene.open {{{}}}'.format(node.child_by_key(SCENE_PATH).raw_value()))

sTREEVIEW_TYPE = " ".join((VPTYPE, IDENT, sSRV_USERNAME, NICE_NAME))

sINMAP = "name[{}] regions[{}]".format(
    sSRV_USERNAME, " ".join(
        ['{}@{}'.format(n, i) for n, i in enumerate(REGIONS) if n != 0]
    )
)

tags = {lx.symbol.sSRV_USERNAME: sSRV_USERNAME,
        lx.symbol.sTREEVIEW_TYPE: sTREEVIEW_TYPE,
        lx.symbol.sINMAP_DEFINE: sINMAP}

lx.bless(BatchTreeView, SERVERNAME, tags)

lx.bless(BatchOpen, CMD_BatchOpen)
lx.bless(BatchClose, CMD_BatchClose)
lx.bless(BatchAddTask, CMD_BatchAddTask)
lx.bless(BatchAddParam, CMD_BatchAddParam)
lx.bless(BatchAddToList, CMD_BatchAddToList)
lx.bless(BatchAddToDict, CMD_BatchAddToDict)
lx.bless(BatchDeleteNodes, CMD_BatchDeleteNodes)
lx.bless(BatchReorderNodes, CMD_BatchReorderNodes)
lx.bless(BatchSelectShift, CMD_BatchSelectShift)
lx.bless(BatchEditNodes, CMD_BatchEditNodes)
lx.bless(BatchEditNodesAdvanced, CMD_BatchEditNodesAdvanced)
lx.bless(BatchResetNodes, CMD_BatchResetNodes)
lx.bless(BatchOpenTaskScene, CMD_BatchOpenTaskScene)
lx.bless(BatchRender, CMD_BatchRender)
lx.bless(BatchExample, CMD_BatchExample)
lx.bless(BatchOpenInFilesystem, CMD_BatchOpenInFilesystem)
lx.bless(BatchRevealInFilesystem, CMD_BatchRevealInFilesystem)
lx.bless(BatchNew, CMD_BatchNew)
lx.bless(BatchSaveAs, CMD_BatchSaveAs)
lx.bless(BatchOpenStatusFile, CMD_BatchOpenStatusFile)

lx.bless(BatchEditNumber, CMD_BatchEditNumber)
lx.bless(BatchEditString, CMD_BatchEditString)
