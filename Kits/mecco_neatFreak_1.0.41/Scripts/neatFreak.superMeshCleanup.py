#python

# See if the user value exists
if lx.eval("query scriptsysservice userValue.isDefined ? cj_tolerance")==0:
    lx.eval( 'user.defNew cj_tolerance distance' );
    lx.eval( 'user.def cj_tolerance username \"merge verts closer than:\"' );

# See if a value has been set yet
if lx.eval( "query scriptsysservice userValue.isSet ? cj_tolerance" )==0:
    lx.eval('user.value cj_tolerance 1mm' );

lx.eval('user.value cj_tolerance')
cj_tolerance = lx.eval('user.value cj_tolerance ?')

lx.eval("select.polygon add type subdiv 1")
lx.eval("poly.convert face subdiv false")
lx.eval("select.polygon add type psubdiv 2")
lx.eval("poly.convert face psubdiv false")

for i in range(3):
    lx.eval("!!vert.merge fixed false %s false true" % cj_tolerance)
    lx.eval("!!mesh.cleanup true true true true true true true true true true")
    lx.eval("!!poly.align")

try:
    lx.eval('vertMap.updateNormals')
except:
    pass
