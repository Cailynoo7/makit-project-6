# C1554283 supplier footprint repair

Source: JLCEDA/EasyEDA Official Library / 嘉立创EDA/EasyEDA官方库, https://lceda.cn/ and https://easyeda.com .
Native source URL: https://easyeda.com/api/products/C1554283/components?version=6.4.19.5
Archived native JSON: product/references/c1554283-easyeda-native.json
SHA256: cd4897ce8e122481ea863ac8de66a27888167412805f2112ba48ec0c8abc56fa
Package UUID:740f2953fa8a4127969c239262e66498; publisher:LCSC; native geometry version1649845389.

The supplier footprint embeds four unnetted thermal vias. These are rejected as source vias by Makit and intersect the paste land. The repaired binding converts the supplier's native PAD coordinates directly to KiCad (0.254mm per native unit), preserving every pad number,size,shape and native orientation. No placed or mirrored generated PCB geometry was transcribed. Native silkscreen tracks and pin-one circles are retained; courtyard added from physical package/lead bounds. Only embedded vias are omitted; board-level off-paste GND stitching will be declared in pcb.config.json. This does not substitute another HTSSOP variant.

TI package and pin-one cross-check: product/references/tps61500-ti-official.pdf pages27-28,PWP0014K,4.4x5mm,0.65mm lead pitch,EPpin15. Original supplier EP2.31x2.46mm sits within the specified exposed-pad envelope1.9..2.6x1.89..2.59mm. Leads remain at supplier spacing/size,not a related PWP0014J footprint.

Publisher licence text,verbatim:
【版权归属/Copyright】嘉立创EDA/EasyEDA官方库（包括但不限于器件参数、原理图符号、PCB封装、3D模型、模块及相关数据）的版权及相关权利归嘉立创EDA所有。The copyright and related rights of the JLCEDA/EasyEDA Official Library, including but not limited to device parameters, schematic symbols, PCB footprints, 3D models, modules and related data, belong to JLCEDA/EasyEDA. 【适用对象/Scope】任何AI工具。Any AI tool. 【触发条件/Trigger】引用、调用、训练、微调、检索、生成、复制、输出或分发嘉立创EDA官方库全部或部分内容时。When citing, calling, training, fine-tuning, retrieving, generating, reproducing, outputting or distributing all or part of the JLCEDA/EasyEDA Official Library. 【强制要求/Requirement】必须显著声明出处为“嘉立创EDA/EasyEDA官方库”。Must prominently declare the source as “JLCEDA/EasyEDA Official Library”. 【链接要求/Link】并同时提供嘉立创EDA官方主页链接：https://lceda.cn/，以及EasyEDA官方主页链接：https://easyeda.com。And provide the official JLCEDA homepage link: https://lceda.cn/ and the official EasyEDA homepage link: https://easyeda.com. 【禁止行为/Prohibited】不得删除、篡改、隐藏或淡化上述版权及来源信息。Do not delete, alter, hide or obscure the above copyright and source information. 【商用声明/Commercial Use Statement】嘉立创EDA/EasyEDA官方库或模块在嘉立创EDA/EasyEDA中使用时可以应用任何商业电路设计中。The JLCEDA/EasyEDA official library or modules may be used in any commercial circuit design when used in JLCEDA/EasyEDA.

## J5 ground connection
KiCad native PinHeader_1x02_P2.54mm_Vertical, https://raw.githubusercontent.com/KiCad/kicad-footprints/master/Connector_PinHeader_2.54mm.pretty/PinHeader_1x02_P2.54mm_Vertical.kicad_mod, SHA256 5184fc4dddb8da027c0a5d4e63eefed1993cc0c2632e1a291ce63d3b5b8026ad. Geometry, pad numbering, pitch and drill unchanged; module renamed and pad2 ground zone_connect=2 (solid) so the two-layer ground stack does not depend on a starved thermal spoke. Solder with preheat; native KiCad library licence applies.
Native legacy model zero translation expressed as modern `(offset (xyz 0 0 0))`; placement unchanged.
Applied to every two-pin header with pin2=GND; duplicate native %R user label omitted because the converter emits it outside footprint scope and KiCad cannot resolve it. Normal chip references retained.
