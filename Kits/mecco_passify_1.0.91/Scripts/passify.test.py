#python

lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true')
lx.eval('layout.createOrClose passify_testify "passify_testify" title:Test width:800 height:400 persistent:true')

def open_scene(slug):
    scenesFolder = lx.eval("query platformservice alias ? {kit_mecco_passify:testing}")

    lx.eval("pref.value application.defaultScene {%s/%s.lxo}" % (scenesFolder,slug))
    lx.eval("scene.new")
    lx.eval("pref.value application.defaultScene {}")

open_scene('Ultralight')

lx.eval('passify.UltralightSetup true true true 0.2')
lx.eval('passify.UltralightDestroy')

lx.eval('select.drop item')
lx.eval('select.subItem Ramp set')
lx.eval('passify.QuickFloorAddItems background')

lx.eval('select.drop item')
lx.eval('select.subItem product_geo set')
lx.eval('passify.QuickFloorAddItems foreground')

lx.eval('select.drop item')
lx.eval('select.subItem Ramp set')
lx.eval('passify.QuickFloorRemoveItems background')

lx.eval('select.drop item')
lx.eval('select.subItem product_geo set')
lx.eval('passify.QuickFloorRemoveItems foreground')

lx.eval('passify.QuickFloorSetup true')
lx.eval('passify.QuickFloorDestroy')

lx.eval('select.drop item')
lx.eval('select.subItem test_ball set')
lx.eval('select.subItem test_ball2 add')
lx.eval('passify.TogglerAddItems')

lx.eval('passify.TogglerRemoveItems')
lx.eval('passify.TogglerDestroy')

lx.eval('passify.UltralightSetup true true true 0.2')

lx.eval('select.drop item')
lx.eval('select.subItem Ramp set')
lx.eval('passify.QuickFloorAddItems background')

lx.eval('select.drop item')
lx.eval('select.subItem product_geo set')
lx.eval('passify.QuickFloorAddItems foreground')

lx.eval('select.drop item')
lx.eval('select.subItem test_ball set')
lx.eval('select.subItem test_ball2 add')
lx.eval('passify.TogglerAddItems')

lx.eval('group.current {QuickFloor Passes} pass')
lx.eval('passify.ManagerRename group {QuickFloor Renamed}')

lx.eval('group.current {Ultralight Passes} pass')
lx.eval('passify.ManagerDelete group')

lx.eval('passify.UltralightSetup true true true 0.2')

lx.eval('group.current {Ultralight Passes} pass')
lx.eval('passify.ManagerHaulGroupChannels')
lx.eval('tool.set channel.haul off 0')

lx.eval('attr.formPopover {passify_ManagerPassChannelsFCL:sheet}')

lx.eval('passify.ManagerAutoAdd 1')
lx.eval('passify.ManagerAutoAdd 0')

lx.eval('passify.ManagerAutoAdd 1')
lx.eval('select.drop item')
lx.eval('item.channel item:BaseMaterial name:diffCol value:{0.4 0.6 0.6}')
lx.eval('passify.ManagerApplyDiscard discard')
lx.eval('item.channel item:BaseMaterial name:diffCol value:{0.6 0.4 0.6}')
lx.eval('passify.ManagerApplyDiscard apply')

lx.eval('layout.createOrClose Groups "Groups Palette" title:Groups width:300 height:450 persistent:true style:palette')

lx.eval('select.drop item')
lx.eval('select.item {Toggler Passes} set')
lx.eval('select.item {Ultralight Passes} add')
lx.eval('passify.ManagerCombinePassGroups')

lx.eval('layer.active {} type:pass')
lx.eval('group.current {} pass')

lx.eval('layout.createOrClose Preview iView_layout title:Preview width:500 height:400 persistent:true style:palette')
