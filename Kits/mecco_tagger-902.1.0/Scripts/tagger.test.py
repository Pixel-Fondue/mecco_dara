#python

import tagger, traceback

errors = 0

lx.eval('layout.createOrClose EventLog "Event Log_layout" title:@macros.layouts@EventLog@ width:600 height:600 persistent:true open:true')

def open_scene(slug):
    scenesFolder = lx.eval("query platformservice alias ? {kit_mecco_tagger:testing}")

    lx.eval("pref.value application.defaultScene {%s/%s.lxo}" % (scenesFolder,slug))
    lx.eval("scene.new")
    lx.eval("pref.value application.defaultScene {}")

lx.eval('scene.closeAll')
open_scene('testScene')

lx.eval('select.drop item')
lx.eval('select.drop channel')
lx.eval('select.subItem Cube set')
lx.eval('select.typeFrom polygon;edge;vertex;item;pivot;center;ptag true')


try:
    lx.eval("tagger.pTagQuickSelectPopup pick seedSel")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.pTagCopy")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.pTagQuickSelectPopup pick hoopSet")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.pTagPasteMaterial")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.setMaterial_pTagRemove")
except:
    lx.out(traceback.print_exc())
    errors += 1

lx.eval("select.drop polygon")


try:
    lx.eval("tagger.pTagQuickSelectPopup pick seedSel")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.floodSelectMaterial")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.setMaterial_pTag test random selected material use")
except:
    lx.out(traceback.print_exc())
    errors += 1


lx.eval("select.drop polygon")


try:
    lx.eval("tagger.pTagQuickSelectPopup pick seedSel")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.setMaterial_auto")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.setMaterial_auto")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.selectAllByMaterial test")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.selectAllByPart p4")
except:
    lx.out(traceback.print_exc())
    errors += 1


lx.eval("select.drop polygon")


try:
    lx.eval("tagger.pTagQuickSelectPopup pick hoopSet")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.setMaterial_existing_Popup {material:m3}")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.setMaterial_existing_Popup {material:m1}")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.setMaterial_autoQuick /Users/adam/Desktop/kits/mecco_dara/Kits/mecco_Tagger/basics/matte.lxp")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.pTagSet material test flood")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.pTagConvert material pick")
except:
    lx.out(traceback.print_exc())
    errors += 1


lx.eval("select.drop polygon")


try:
    lx.eval("tagger.setMaterial_pTagIslands test material")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.shaderTree_cleanup true true")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.pTagQuickSelectPopup pick seedSel")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.floodSelectMaterial")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.pTagSet pick great flood")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.setMaterial_pTagRemove")
except:
    lx.out(traceback.print_exc())
    errors += 1


lx.eval("select.drop polygon")


try:
    lx.eval("tagger.shaderTree_maskUnmasked material")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.pTagRemoveUnmasked material")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.pTagRemoveAll material selected_items")
except:
    lx.out(traceback.print_exc())
    errors += 1


try:
    lx.eval("tagger.pTagRemoveAll material scene")
except:
    lx.out(traceback.print_exc())
    errors += 1

lx.eval('!scene.closeAll')
open_scene('testScene')

if not errors:
    lx.out("Found zero errors. Well done, you. Be sure to check the UI buttons.")

else:
    lx.out("Found %s errors. Get to work." % errors)
