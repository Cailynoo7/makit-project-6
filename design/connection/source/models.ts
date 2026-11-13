// Exact published models; see models/SOURCES.md for hashes and native transforms.
const source = (file:string) => `./source/models/${file}`;
export const headerModel = (pins:number) => ({
  stepUrl: source(`PinHeader_1x0${pins}_P2.54mm_Vertical.step`),
  modelOriginPosition:{x:0,y:0,z:0},
  rotationOffset:{x:0,y:0,z:0},
  positionOffset:{x:0,y:0,z:0},
  modelUnitToMmScale:1,
  modelBoardNormalDirection:'z+' as const,
});
export const packageModel = (ref:string,code:string) => {
  if(code==='C544396') return {
    stepUrl:source('csd85301q2-supplier-faceted.step'),
    modelOriginPosition:{x:0,y:0.0635,z:0},
    rotationOffset:{x:0,y:0,z:90},
    positionOffset:{x:0,y:0,z:0},
    modelUnitToMmScale:1,
    modelBoardNormalDirection:'z+' as const,
  };
  if(ref==='U1') return {
    stepUrl:source('tps61500pwp-supplier.step'),
    modelOriginPosition:{x:0,y:0,z:-0.15},
    rotationOffset:{x:0,y:0,z:0},
    positionOffset:{x:0,y:0,z:0},
    modelUnitToMmScale:1,
    modelBoardNormalDirection:'z+' as const,
  };
  return undefined;
};
