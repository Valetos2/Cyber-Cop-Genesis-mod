# Advance once per80 VBlanks (measured native cadence), even when slow frames skip the exact multiple.
# Testing the low counter bits can repeat a step or never hit the target phase.
c.label('lift_clock36b');c.abs('3039',0xffff2798);c.abs('9079',0xffff0832);c.emit('0c400050');c.branch('6500','lift_clock36b_wait');c.abs('33f9',0xffff2798);c.long(0xffff0832);c.jump(0x8e00)
c.label('lift_clock36b_wait');c.jump(0x8e1a);patch(0x8df4,'lift_clock36b')
c.label('lift_select36b');c.abs('33f9',0xffff2798);c.long(0xffff0832);c.emit(src[0x8e74:0x8e7a].hex());c.jump(0x8e7a);patch(0x8e74,'lift_select36b')
# Genesis retains the light-circle builder but never calls its rasterizer.
# Draw lights after clearing the framebuffer and before walls/actors occlude them.
c.label('lights_draw36b');c.emit('48e7fffe');c.call(0x45b8);c.emit('4cdf7fff');c.emit(src[0x4584:0x458a].hex());c.jump(0x458a);patch(0x4584,'lights_draw36b')
# A terminal may leave a nametable word from its graphics in the HUD button row.
# Rebuild both rows from the tracked native HUD state after the normal close.
# This does not reload tiles or overwrite the inventory/energy indicators.
c.label('terminal_hud36b');c.call(int.from_bytes(src[0x21da:0x21de],'big'));c.emit('48e7fffe')
for row in range(2):
 for col in range(24):
  c.abs('3039',0xffff0280+row*48+col*2);c.emit('343c'+f'{0xe992+row*128+col*2:04x}');c.call(0x35fe)
c.emit('4cdf7fff4e75');patch(0x21d8,'terminal_hud36b')
