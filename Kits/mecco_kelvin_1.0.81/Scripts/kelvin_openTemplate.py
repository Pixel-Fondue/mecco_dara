#python
import lx, modo

event = lx.args()[0]

# if event == ('beforeCreate'):
#     lx.eval("scene.closeAll")

if len(lx.args()) > 1:
    group = lx.args()[1]

    if event in ('onDrop', 'onDo'):
        slug = modo.Scene().item(group).name.split("__")[0]
        modo.scene.current().removeItems(group)
        scenesFolder = lx.eval("query platformservice alias ? {kit_mecco_kelvin:Scenes}")

        lx.eval("pref.value application.defaultScene {%s/%s.lxo}" % (scenesFolder,slug))
        lx.eval("scene.new")
        lx.eval("pref.value application.defaultScene {}")
