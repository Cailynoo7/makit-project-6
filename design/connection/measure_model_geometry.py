"""Read the published assembly and compare real header pins with PCB drills."""
from pathlib import Path
import hashlib
import json
import math
from build123d import import_step, Box, Pos

root = Path(__file__).resolve().parents[2]
step = root/'.work/pcb/connection/release/package/assembly.step'
circuit = json.loads((root/'.work/pcb/connection/build/circuit.json').read_text())
assembly = import_step(str(step))
headers = [c for c in assembly.children if c.label.startswith('PinHeader')]
pins = []
for h in headers:
    section = h & Pos(100,-100,.8)*Box(80,80,.002)
    pins.extend([(s.center().X,s.center().Y) for s in section.solids()])
holes = [(100+c['x'],-100+c['y']) for c in circuit if c['type']=='pcb_plated_hole']
assert len(headers)==12 and len(pins)==len(holes)==30
errors = [min(math.dist(p,h) for h in holes) for p in pins]
assert max(errors)<0.001
cad = [c for c in circuit if c['type']=='cad_component']
assert len(cad)==76 and all(c.get('model_step_url') for c in cad)
low = [c for c in assembly.children if c.bounding_box().min.Z < -2]
data = {
    'assembly_step_sha256':hashlib.sha256(step.read_bytes()).hexdigest(),
    'units':'mm',
    'model_bindings':len(cad),
    'headers':len(headers),
    'header_metal_pin_sections':pins,
    'PCB_drill_centres_STEP_frame':holes,
    'max_header_axis_error_mm':max(errors),
    'assembly_bbox':{'min':list(assembly.bounding_box().min),'max':list(assembly.bounding_box().max)},
    'lowest_components_in_STEP_frame':[
        {'label':c.label,'min':list(c.bounding_box().min),'max':list(c.bounding_box().max)}for c in low
    ],
}
(root/'product/references/connection-model-measurements.json').write_text(json.dumps(data,indent=2)+'\n')
print('76 models;12 headers;30 pins;max drill-axis error mm:',max(errors))
print('Lowest mounted body:',data['lowest_components_in_STEP_frame'])
