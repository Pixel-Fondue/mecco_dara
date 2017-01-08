#python
import modo

try:
    modo.scene.current().removeItems(modo.Scene().item("Directional Light"),True)
except:
    lx.out("Default directional light not found.")

try:
    hitlist = []
    for i in modo.Scene().iterItems():
        if "analytical.lxe" in i.name:
            hitlist.append(i)
    for i in hitlist:
        modo.scene.current().removeItems(i)
except:
    lx.out("No items containing 'analytical.lxe' found.")
