# Checkpoint on accepted elevator destination. Commit the CURRENT map before
# encoding the destination; never write current map items into the target slot.
c.label('lift_save36d');c.emit('48e7fffe');c.emit('0c4300b1');c.branch('6600','lift_save_done36d');c.abs('4a79',0xffff026c);c.branch('6600','lift_save_done36d')
c.abs('3f39',0xffff2608);c.abs('33f9',0xffff2606);c.long(0xffff2608);c.call(0x4a80);c.abs('33df',0xffff2608)
c.abs('3f39',0xffff2606);c.abs('3f39',0xffff216e)
c.abs('3039',0xffff218e);c.abs('41f9',0x8e58);c.emit('30300000');c.abs('33c0',0xffff2606)
c.ref('4eb9','terminal_latch12');c.call(0x8faa)
# save21+32 begins after its own map commit. Supply its normal MOVEM frame.
c.ref('4eb9','lift_save_body36d');c.abs('33df',0xffff216e);c.abs('33df',0xffff2606)
c.label('lift_save_done36d');c.emit('4cdf7fff');c.emit(src[0x8e9e:0x8ea6].hex());c.jump(0x8ea6);patch(0x8e9e,'lift_save36d',8)
c.label('lift_save_body36d');c.emit('48e7fffe');c.jump(V['save21']+32)

# The password packs the current-floor access latch in bit 2. During a lift
# checkpoint it must describe the destination, not the departure floor.
c.label('terminal_latch12')
c.abs('4279',0xffff216e)
c.abs('3039',0xffff2606);c.abs('41f9',0xffff2718)
c.emit('4a300000');c.branch('6700','terminal_latch_done12');wi(0xffff216e,0xffff)
c.label('terminal_latch_done12');c.emit('4e75')

# After X21 restores the full floor history, repair the latch in older saves
# too. Manually entered passwords keep their original latch and semantics.
p=0x1fbc
assert r[p:p+6]==bytes.fromhex('51f9ffff26e6')
c.label('restore_terminal_latch12')
c.abs('4a39',0xffff2712);c.branch('6700','restore_terminal_latch_done12')
c.emit('0c390001ffff0124');c.branch('6600','restore_terminal_latch_done12')
c.emit('48e78080');c.call(c.labels['terminal_latch12']);c.emit('4cdf0101')
c.label('restore_terminal_latch_done12');c.emit(src[p:p+6].hex());c.jump(p+6)
patch(p,'restore_terminal_latch12')
