import { boardPropsFromRules, netPropsFor, pcbRules } from './lib/makit-pcb';
import { board, placement as p } from './layout';
export default () => <board {...boardPropsFromRules()} width={board.width} height={board.height} thickness={board.thickness} title="Window button daughterboard">
 {Object.keys(pcbRules.nets).map(name=><net key={name} name={name} {...netPropsFor(name)}/>)}
 <chip name="SW1" footprint="jlcpcb:C2837530" supplierPartNumbers={{jlcpcb:['C2837530']}} cadModel={{stepUrl:"./source/models/kinghelm-kh-6x6x4p3h-drawing.step",modelOriginPosition:{x:0,y:0,z:0},positionOffset:{x:0,y:0,z:0},rotationOffset:{x:0,y:0,z:0},modelUnitToMmScale:1,modelBoardNormalDirection:"z+"}} pcbX={p.key[0]} pcbY={p.key[1]} pinLabels={{pin1:'A',pin2:'C',pin3:'B',pin4:'D'}} connections={{A:'net.KEY',B:'net.KEY',C:'net.GND',D:'net.GND'}}/>
 <chip name="J1" footprint="kicad:Connector_PinHeader_2.54mm/PinHeader_1x02_P2.54mm_Vertical" pcbX={p.wire[0]} pcbY={p.wire[1]} layer="bottom" pinLabels={{pin1:'KEY',pin2:'GND'}} connections={{KEY:'net.KEY',GND:'net.GND'}}/>
 <copperpour name="GND_TOP" layer="top" connectsTo="net.GND" clearance="0.25mm" boardEdgeMargin="1mm"/>
 <copperpour name="GND_BOTTOM" layer="bottom" connectsTo="net.GND" clearance="0.25mm" boardEdgeMargin="1mm"/>
</board>;
