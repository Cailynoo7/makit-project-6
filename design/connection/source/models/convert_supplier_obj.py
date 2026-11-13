"""Lossless geometry conversion of the exact C544396 EasyEDA OBJ to faceted STEP.

No synthesized package geometry: all vertices and faces come from the supplier.
The source is JLCEDA/EasyEDA Official Library: https://lceda.cn/ https://easyeda.com
"""
from collections import Counter
from pathlib import Path
import hashlib
import math

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / 'product/references/csd85301q2-model-obj.txt'
DST = Path(__file__).with_name('csd85301q2-supplier-faceted.step')
assert hashlib.sha256(SRC.read_bytes()).hexdigest() == '11669e90fe126856fe54bc9a8a33f7c762d73fb4aa49c260fb3c521f6f001481'
vertices, faces, unique = [], [], {}
indices = []
for line in SRC.read_text().splitlines():
    a = line.split()
    if not a:
        continue
    if a[0] == 'v':
        v = tuple(map(float, a[1:4]))
        if v not in unique:
            unique[v] = len(vertices)
            vertices.append(v)
        indices.append(unique[v])
    if a[0] == 'f':
        f = [indices[int(t.split('/')[0]) - 1] for t in a[1:]]
        assert len(f) == 3
        faces.append(f)
edges = Counter(tuple(sorted((f[i], f[(i+1) % 3]))) for f in faces for i in range(3))
assert set(edges.values()) == {2}, 'Supplier mesh must be closed/manifold'
def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def sub(a, b):
    return tuple(a[i]-b[i] for i in range(3))
def norm(a):
    l = math.sqrt(sum(v*v for v in a))
    assert l > 1e-12
    return tuple(v/l for v in a)
volume = sum(sum(vertices[f[0]][i]*cross(vertices[f[1]], vertices[f[2]])[i] for i in range(3))/6 for f in faces)
assert abs(volume) > 1
if volume < 0:
    faces = [list(reversed(f)) for f in faces]
lines = []
def entity(s):
    lines.append(f'#{len(lines)+1}={s};')
    return len(lines)
def tup(p):
    return '(' + ','.join(f'{v:.9f}' for v in p) + ')'
def refs(ids):
    return '(' + ','.join(f'#{i}' for i in ids) + ')'
app = entity("APPLICATION_CONTEXT('automotive design')")
entity(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#{app})")
pc = entity(f"PRODUCT_CONTEXT('',#{app},'mechanical')")
prod = entity(f"PRODUCT('CSD85301Q2','CSD85301Q2 supplier faceted model','JLCEDA/EasyEDA Official Library OBJ conversion',({refs([pc])[1:-1]}))")
form = entity(f"PRODUCT_DEFINITION_FORMATION('','',#{prod})")
pdc = entity(f"PRODUCT_DEFINITION_CONTEXT('part definition',#{app},'design')")
pd = entity(f"PRODUCT_DEFINITION('design','',#{form},#{pdc})")
pds = entity(f"PRODUCT_DEFINITION_SHAPE('','',#{pd})")
mm = entity('(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.))')
rad = entity('(NAMED_UNIT(*)PLANE_ANGLE_UNIT()SI_UNIT($,.RADIAN.))')
sr = entity('(NAMED_UNIT(*)SI_UNIT($,.STERADIAN.)SOLID_ANGLE_UNIT())')
unc = entity(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(0.000001),#{mm},'distance_accuracy_value','source vertex precision')")
ctx = entity(f"(GEOMETRIC_REPRESENTATION_CONTEXT(3)GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{unc}))GLOBAL_UNIT_ASSIGNED_CONTEXT((#{mm},#{rad},#{sr}))REPRESENTATION_CONTEXT('',''))")
pts = [entity(f"CARTESIAN_POINT('',{tup(v)})") for v in vertices]
out = []
for f in faces:
    a, b, c = (vertices[i] for i in f)
    lp = entity(f"POLY_LOOP('',{refs([pts[i] for i in f])})")
    bd = entity(f"FACE_OUTER_BOUND('',#{lp},.T.)")
    z = entity(f"DIRECTION('',{tup(norm(cross(sub(b,a),sub(c,a))))})")
    x = entity(f"DIRECTION('',{tup(norm(sub(b,a)))})")
    ax = entity(f"AXIS2_PLACEMENT_3D('',#{pts[f[0]]},#{z},#{x})")
    plane = entity(f"PLANE('',#{ax})")
    out.append(entity(f"FACE_SURFACE('',(#{bd}),#{plane},.T.)"))
shell = entity(f"CLOSED_SHELL('',{refs(out)})")
brep = entity(f"FACETED_BREP('CSD85301Q2 supplier mesh',#{shell})")
rep = entity(f"FACETED_BREP_SHAPE_REPRESENTATION('CSD85301Q2',({refs([brep])[1:-1]}),#{ctx})")
entity(f'SHAPE_DEFINITION_REPRESENTATION(#{pds},#{rep})')
header = "ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('Exact supplier OBJ facets; not an analytic manufacturer STEP'),'2;1');\nFILE_NAME('csd85301q2-supplier-faceted.step','2026-11-12T00:00:00',('Makit project'),('JLCEDA/EasyEDA Official Library'),'supplier OBJ conversion','project converter','');\nFILE_SCHEMA(('AUTOMOTIVE_DESIGN'));\nENDSEC;\nDATA;\n"
DST.write_text(header+'\n'.join(lines)+'\nENDSEC;\nEND-ISO-10303-21;\n')
print('vertices',len(vertices),'faces',len(faces),'volume_mm3',abs(volume))
print('bounds_mm',[(min(v[i]for v in vertices),max(v[i]for v in vertices))for i in range(3)])
print('sha256',hashlib.sha256(DST.read_bytes()).hexdigest())
