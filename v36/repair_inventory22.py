# Keep focus on Repair between the stock B press and release. The world
# callback is installed before the counter advances, so look it up too.
p=0x54d2
native=bytes.fromhex('4ef9000f0000')
assert r[p:p+6]==native
c.label('repair_motion22')
c.emit('08390004ffff0005');c.branch('6600','repair_motion_native22')
c.emit('2f09');c.abs('2279',0xffff202a)
c.emit('0c6900040002');c.branch('6600','repair_motion_pop22')
c.abs('4a79',0xffff214c);c.branch('6600','repair_motion_locked22')
c.emit('2f00');c.abs('43f9',0xffff202e);c.emit('701f')
c.label('repair_motion_search22')
c.emit('0c9900007192');c.branch('6700','repair_motion_found22')
c.emit('51c8');c.fix.append((len(c.b),'repair_motion_search22',2));c.emit('0000')
c.emit('201f');c.branch('6000','repair_motion_pop22')
c.label('repair_motion_found22');c.emit('201f')
c.label('repair_motion_locked22');c.emit('225f4e75')
c.label('repair_motion_pop22');c.emit('225f')
c.label('repair_motion_native22');c.emit(native.hex())
patch(p,'repair_motion22')
