# Component models

JLCEDA/EasyEDA Official Library: https://lceda.cn/ and https://easyeda.com

C544396/CSD85301Q2 supplier OBJ https://modules.easyeda.com/3dmodel/cec58c53873d413fa827b6a5400714bb , SHA256 11669e90fe126856fe54bc9a8a33f7c762d73fb4aa49c260fb3c521f6f001481. Native STEP endpoint returns404. Converter preserves all1020 vertices/2036 faces; closed manifold,3.2194677795mm3,2.02x2.00x0.81mm. This is a faceted conversion of the actual supplier model, not an analytic manufacturer STEP or generated package box. Supplier mesh height0.81mm is0.01mm above datasheet0.8mm maximum, retained conservatively for envelope checking. Native supplier transform: rotationZ90,originY0.0635mm.

TPS61500PWP: native C1554283 package740f2953fa8a4127969c239262e66498 references model eeaefb9dd4784aac84005d52f9c63fdb. https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/eeaefb9dd4784aac84005d52f9c63fdb , SHA256 284276d725d48c4d5b8b4d6b8c356ebd11eb0de3fcba22be6d02ab2af45d5df1.28 solids; model seating plane normalized fromZ=-0.15mm,conservative mounted height1.251mm.

KiCad official library pin headers: native footprint and matching STEP copied from installed KiCad standard library, CC-BY-SA4.0 with library exception, https://gitlab.com/kicad/libraries/kicad-footprints and https://gitlab.com/kicad/libraries/kicad-packages3D . Native pins, holes and pitch preserved. Model records removed from local footprint copies to bind exactly one matching STEP via cadModel. Explicit cadModel placements use declared pcbX/pcbY at pin1. The native header STEP has pin1 at(0,0), so modelOriginPosition=(0,0,0). Using a row-centre origin here would displace the header by half its row length.

PinHeader_1x02_P2.54mm_Vertical.kicad_mod: SHA256 5301303268f72ba9cc94b7fdbac355951933e6854272ce8d300b679b86b5d45d
PinHeader_1x03_P2.54mm_Vertical.kicad_mod: SHA256 e5f24b6fea852f86171042806da48490229c9c8025b6d266b8cad6485b26e79f
PinHeader_1x07_P2.54mm_Vertical.kicad_mod: SHA256 b68c5749fd4d81ff8a7e3ef1223a9081acd4a879079e7c2c9d5bcb9363b02630
