import {boardPropsFromRules,keepoutPropsFromRules,netPropsFor,pcbRules} from './lib/makit-pcb';
import {board,mounting,headers} from './layout';
import {passives,ics} from './reading-light';
import {headerModel,packageModel} from './models';
const supplier=(code?:string)=>code?{supplierPartNumbers:{jlcpcb:[code]}}:{};
const fp=(type:string,size:string,code?:string)=>code?`jlcpcb:${code}`:`kicad:${type}_SMD/${type==='Resistor'?'R':'C'}_${size}`;
export default()=> <board {...boardPropsFromRules()} width={board.width} height={board.height} thickness={board.thickness}
 doubleSidedAssembly minViaPadDiameter="0.5mm" minViaHoleDiameter="0.25mm" minTraceWidth="0.2mm"
 minTraceToPadEdgeClearance="0.2mm" minPadEdgeToPadEdgeClearance="0.2mm" minViaEdgeToPadEdgeClearance="0.2mm"
 minViaHoleEdgeToViaHoleEdgeClearance="0.2mm" minBoardEdgeClearance="1mm" title="Helicopter COB reading light,fan and1S protection">
 {Object.keys(pcbRules.nets).map(name=><net key={name} name={name} {...netPropsFor(name)}/>)}
 {['Control','Fan','Light','Protection','Temperature'].map(name=><schematicsection key={name} name={name}/>)}
 {headers.map(h=><chip key={h.name} name={h.name} pcbX={h.x} pcbY={h.y} pcbRotation={h.rotation}
 footprint={h.nets.length===2&&h.nets[1]==='GND'?'vendor:PinHeader_1x02_SolidGround':`vendor:PinHeader_1x0${h.nets.length}_P2.54mm_Vertical_ModelBound`}
 cadModel={headerModel(h.nets.length)}
 pinLabels={Object.fromEntries(h.nets.map((n,i)=>[`pin${i+1}`,`P${i+1}`]))}
 connections={Object.fromEntries(h.nets.map((n,i)=>[`P${i+1}`,`net.${n}`]))} schSectionName={h.section}/>)}
 {ics.map(c=><chip key={c.name} name={c.name} footprint={c.name==='U1'?'vendor:TPS61500PWP_LCSC_NoEmbeddedVias':`jlcpcb:${c.code}`} {...supplier(c.code)}
 pcbX={c.x} pcbY={c.y} pcbRotation={c.rotation||0} layer={c.side} cadModel={packageModel(c.name,c.code)}
 pinLabels={Object.fromEntries(c.pins.map((v,i)=>[`pin${i+1}`,v[0]]))}
 connections={Object.fromEntries(c.pins.filter(v=>v[1]).map(v=>[v[0],`net.${v[1]}`]))}
 noConnect={c.pins.filter(v=>!v[1]).map(v=>v[0])} schSectionName={c.section}/>)}
 {passives.map(c=>c.type==='R'?<resistor key={c.name} name={c.name} resistance={c.value}
 pcbX={c.x} pcbY={c.y} pcbRotation={c.rotation||0} layer={c.side} pcbStyle={{silkscreenTextVisibility:'hidden'}} footprint={fp('Resistor',c.size||'0603_1608Metric',c.code)} {...supplier(c.code)}
 connections={{pin1:`net.${c.a}`,pin2:`net.${c.b}`}} schSectionName={c.section}/>:
 <capacitor key={c.name} name={c.name} capacitance={c.value}
 pcbX={c.x} pcbY={c.y} pcbRotation={c.rotation||0} layer={c.side} pcbStyle={{silkscreenTextVisibility:'hidden'}} footprint={fp('Capacitor',c.size||'0603_1608Metric',c.code)} {...supplier(c.code)}
 connections={{pin1:`net.${c.a}`,pin2:`net.${c.b}`}} schSectionName={c.section}/>)}
 <inductor name="L1" inductance="10uH" pcbX={-9.4} pcbY={9.672} pcbRotation={180} footprint="jlcpcb:C280564" {...supplier('C280564')}
 connections={{pin1:'net.VBAT',pin2:'net.BOOST_SW'}} schSectionName="Light"/>
 {mounting.map((h,i)=><hole key={i} name={`MH${i+1}`} diameter="2.4mm" pcbX={h.x} pcbY={h.y}/>)}
 {keepoutPropsFromRules().map(props=><keepout {...props}/>)}
 <copperpour name="GND_TOP" layer="top" connectsTo="net.GND" clearance="0.25mm" boardEdgeMargin="1mm"/>
 <copperpour name="GND_INNER1" layer="inner1" connectsTo="net.GND" clearance="0.25mm" boardEdgeMargin="1mm"/>
 <copperpour name="GND_INNER2" layer="inner2" connectsTo="net.GND" clearance="0.25mm" boardEdgeMargin="1mm"/>
 <copperpour name="GND_INNER4" layer="inner4" connectsTo="net.GND" clearance="0.25mm" boardEdgeMargin="1mm"/>
 <copperpour name="GND_BOTTOM" layer="bottom" connectsTo="net.GND" clearance="0.25mm" boardEdgeMargin="1mm"/>
</board>;
