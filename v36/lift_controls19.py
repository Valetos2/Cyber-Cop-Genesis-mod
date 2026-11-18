# Exterior call panel: controller shortcuts are available while Mouse On
# owns the pointer. Both use the existing call handler and its busy check.
LIFT_PAD_HELD=0xffff0870
p=0x8b08
assert r[p:p+8]==bytes.fromhex('4eba9e264ebaadba')
c.label('lift_control_tick19')
c.call(0x2930)
c.ref('4eb9','lift_pad19')
c.call(0x38c8)
c.jump(p+8)
patch(p,'lift_control_tick19',8)

c.label('lift_pad19')
c.emit('48e7e000')
c.abs('3039',0xffff0004);c.emit('464002400050')
c.abs('3239',LIFT_PAD_HELD)
c.abs('33c0',LIFT_PAD_HELD)
c.emit('4641c041')
c.branch('6700','lift_pad_done19')
c.abs('4a79',P);c.branch('6700','lift_pad_done19')
# Start/translated right-click retains the existing cancel behaviour.
c.emit('08390007ffff0005');c.branch('6700','lift_pad_done19')
c.emit('08000006');c.branch('6600','lift_pad_left19')
c.emit('7001');c.branch('6000','lift_pad_call19')
c.label('lift_pad_left19');c.emit('7000')
c.label('lift_pad_call19');c.call(0x8c36)
c.label('lift_pad_done19');c.emit('4cdf00074e75')

# Seed the edge latch on opening, so an A press that opened the panel isn't
# also a call. Put the mouse on the actual right button, once per entry.
p=0x8afe
assert r[p:p+8]==bytes.fromhex('41facda04eba0420')
c.label('lift_call_entry19')
c.abs('41f9',0x58a0);c.call(0x8f24)
c.abs('3039',0xffff0004);c.emit('464002400050');c.abs('33c0',LIFT_PAD_HELD)
c.abs('4a79',P);c.branch('6700','lift_call_entry_done19')
wi(N,1)
wi(N+4,169);wi(N+6,81)
c.abs('42b9',N+28)  # X/Y subpixel remainders
# Discard motion sampled before the panel opened. Guard the VBlank buffer.
c.emit('40e7007c0700')
c.abs('42b9',0xffff0184);c.abs('42b9',0xffff0188)
c.emit('46df')
c.call(S['cursor'])
c.label('lift_call_entry_done19');c.emit('4e75')
patch(p,'lift_call_entry19',8)
