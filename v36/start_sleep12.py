# Keep Start distinct from a panel's synthetic right-click Start and from the
# Mode gesture. As with Mode, enter only from the ordinary gameplay view.
p=V['start15']
assert r[p:p+8]==bytes.fromhex('0a3900ffffff270a')
c.label('start_sleep12')
c.emit('0cb900007070ffff26b8');c.branch('6600','start_sleep_awake12')
c.abs('4a79',P);c.branch('6600','start_sleep_done12')
c.abs('4a39',START_SLEEP);c.branch('6600','start_sleep_done12')
c.branch('6000','start_sleep_native12')
c.label('start_sleep_awake12')
c.abs('4a79',P);c.branch('6700','start_sleep_native12')
c.emit('0cb900002106ffff26b8');c.branch('6600','start_sleep_native12')
c.emit('08390007ffff0197');c.branch('6600','start_sleep_native12')
for a in [0xffff270e,0xffff270f]:
 c.abs('4a39',a);c.branch('6600','start_sleep_done12')
c.emit('48e7fffe');c.call(0x6fb2);c.emit('4cdf7fff')
bi(START_SLEEP,1);bi(0xffff0118,1);bi(0xffff0119,0)
c.abs('4239',0xffff011c) # bypass Mode's ABC chord gate
wi(P+4,1)
c.emit('08b90007ffff0007') # don't deliver the entry edge again next tick
c.emit('08b90003ffff023b') # simultaneous fourth mouse button must not wake immediately
c.label('start_sleep_done12');c.emit('4e75')
c.label('start_sleep_native12');c.emit(src[p:p+8].hex());c.jump(p+8)
patch(p,'start_sleep12',8)

# Wake on a Start press edge in either mouse mode. Check both halves so
# the transition back to released never counts as a press.
p=0x708e
assert r[p:p+12]==bytes.fromhex('3039ffff0004080000076678')
c.label('start_sleep_check12')
c.abs('4a39',START_WAKE_PENDING);c.branch('6600','start_sleep_consume12')
c.abs('3039',0xffff0004);c.emit('08000007');c.branch('6600','start_sleep_wait12')
c.emit('08390007ffff0007');c.branch('6700','start_sleep_wait12')
c.label('start_sleep_consume12');c.abs('4239',START_WAKE_PENDING)
c.emit('08b90007ffff0007')
c.label('start_sleep_wake12');c.jump(0x709a)
c.label('start_sleep_wait12');c.jump(0x7112)
patch(p,'start_sleep_check12',12)
