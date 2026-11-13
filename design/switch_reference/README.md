# KH-6X6X4.3H-STM drawing reference

Internal model input for the two window daughterboards; purchased switch, not a printable part. Deliberately modeled from exact C2837530 manufacturer drawing because the supplied STEP is5.01mm above its lead plane instead of H4.3mm. Conservative external assembly envelope, not an original manufacturer STEP or internal switch model:6x6 body,3.15mm case plus0.3mm conservative cover envelope,diameter3.5mm plunger,total4.3mm above lead seating plane. Lead envelopes:9mm overall span,4.5mm pitch,0.7mm width,0.23mm thickness; bend position is an engineering envelope and does not define copper. lead_mounting_clearance defaults0; the PCB exporter supplies its own component mounting datum. Do not double-count solder stand-off.

Evidence: controls interface,switch_drawing reference; references/suppliers/c2837530/c2837530-datasheet.pdf SHA2565686a865fc368784abc6e8805e710e62f4395d8b7a8c39ed3d3ddb1714d7a0b2. Exact MPN KH-6X6X4.3H-STM/C2837530,travel0.3+/-0.1mm. Supplier footprint,netlist and component position unchanged.

Making and assembly: do not print or trim a real switch. Bind this source-owned model to SW1 in the keys PCB and use the released PCB assembly in the helicopter. Verify actual mounted height, free gap, return and press feel in a first assembly; nominal simulation does not validate manufacturing tolerance or feel.
