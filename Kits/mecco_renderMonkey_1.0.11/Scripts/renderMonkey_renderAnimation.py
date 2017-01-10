#python

import sys

render_id = lx.eval('query sceneservice item.ID ? {Render}')
using_IC = lx.eval('item.channel polyRender$irrCache ? item:%s' % render_id )

if using_IC:
    lx.eval("dialog.setup YesNo")
    lx.eval("dialog.title {Switch to Monte Carlo?}")
    lx.eval("dialog.msg {Irradiance Caching speeds up still images, but can create visible artifacts in animations.\nSwitch to Brute-Force ('Monte Carlo') Global Illumination? (Recommended.)}")
    try:
        lx.eval("dialog.open")
        lx.out('Disable IC: Yes')
        lx.eval("item.channel polyRender$irrCache false item:%s" % render_id)
    except:
        lx.out('Disable IC: No')
    
try:
    lx.eval("iview.renderAnim")
except:
    # revert IC state on abort
    lx.eval("item.channel polyRender$irrCache %s item:%s" % (using_IC,render_id))
    lx.out('User abort.')