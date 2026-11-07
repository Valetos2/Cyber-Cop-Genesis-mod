# Native autoaim collects eligible rendered actors in draw order. Preserve this
# order, except insert a camera before the first emergency lamp already present.
# Actor IDs: camera3 (BED6), emergency lamp17 (B738). Free mouse aim bypasses it.
c.label('aim_priority36c');c.emit('48e7fffe');c.abs('41f9',0xffff23b4);c.abs('3239',0xffff23b2);c.emit('30010c6a00030002');c.branch('6600','aim_priority_append36c');c.emit('7000')
c.label('aim_priority_find36c');c.emit('b041');c.branch('6400','aim_priority_append36c');c.emit('227000000c6900110002');c.branch('6700','aim_priority_insert36c');c.emit('5840');c.branch('6000','aim_priority_find36c')
c.label('aim_priority_insert36c');c.emit('3401')
c.label('aim_priority_shift36c');c.emit('b440');c.branch('6300','aim_priority_append36c');c.branch('6700','aim_priority_append36c');c.emit('263020fc');c.emit('21832000');c.emit('5942');c.branch('6000','aim_priority_shift36c')
c.label('aim_priority_append36c');c.emit('218a0000');c.abs('5879',0xffff23b2);c.emit('4cdf7fff');c.jump(0xec7a);patch(0xec62,'aim_priority36c')
