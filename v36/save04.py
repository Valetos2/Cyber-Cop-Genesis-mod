# Checkpoint on accepted elevator destination. Commit the CURRENT map before
# encoding the destination; never write current map items into the target slot.
c.label('lift_save36d');c.emit('48e7fffe');c.emit('0c4300b1');c.branch('6600','lift_save_done36d');c.abs('4a79',0xffff026c);c.branch('6600','lift_save_done36d')
c.abs('3f39',0xffff2608);c.abs('33f9',0xffff2606);c.long(0xffff2608);c.call(0x4a80);c.abs('33df',0xffff2608)
c.abs('3f39',0xffff2606);c.abs('3039',0xffff218e);c.abs('41f9',0x8e58);c.emit('30300000');c.abs('33c0',0xffff2606);c.call(0x8faa)
# save21+32 begins after its own map commit. Supply its normal MOVEM frame.
c.ref('4eb9','lift_save_body36d');c.abs('33df',0xffff2606)
c.label('lift_save_done36d');c.emit('4cdf7fff');c.emit(src[0x8e9e:0x8ea6].hex());c.jump(0x8ea6);patch(0x8e9e,'lift_save36d',8)
c.label('lift_save_body36d');c.emit('48e7fffe');c.jump(V['save21']+32)
