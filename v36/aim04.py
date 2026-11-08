# Priority is stable inside each group. Only actual enemy actor IDs count as
# threats, including the holographic crab. Crawlers/props are deliberately out.
walk_ids=[0x8004,0x8006,0x801c,0x8019,0x801a,0x801b,0x801d]
c.label('aim_rank36d');c.emit('30290002024080ff')
for kind in walk_ids:c.emit('0c40'+f'{kind:04x}');c.branch('6700','aim_rank_enemy36d')
c.emit('0c400003');c.branch('6700','aim_rank_camera36d');c.emit('0c400011');c.branch('6700','aim_rank_lamp36d');c.emit('70014e75')
c.label('aim_rank_enemy36d');c.emit('70034e75');c.label('aim_rank_camera36d');c.emit('70024e75');c.label('aim_rank_lamp36d');c.emit('70004e75')
c.label('aim_priority36d');c.emit('48e7fffe224a');c.call(c.labels['aim_rank36d']);c.emit('3600')
# Native visibility buffer stores wall distance /64 per screen column. The
# native sprite test accepts even a sliver; check the actual aim centre too.
c.emit('302a000e');c.branch('6b00','aim_priority_reject36d');c.emit('0c4000bf');c.branch('6200','aim_priority_reject36d');c.abs('43f9',0xffff40ce);c.emit('7200123100003012ec489041');c.branch('6f00','aim_priority_visible36d');c.emit('302a0002024080ff0c40801b');c.branch('6700','aim_priority_reject36d');c.emit('3012ec4890410c430003');c.branch('6600','aim_priority_reject36d');c.emit('0c400004');c.branch('6200','aim_priority_reject36d')
c.label('aim_priority_visible36d');c.abs('41f9',0xffff23b4);c.abs('3239',0xffff23b2);c.emit('7400')
c.label('aim_priority_find36d');c.emit('b441');c.branch('6400','aim_priority_insert36d');c.emit('22702000');c.call(c.labels['aim_rank36d']);c.emit('b640');c.branch('6e00','aim_priority_insert36d');c.emit('5842');c.branch('6000','aim_priority_find36d')
c.label('aim_priority_insert36d');c.emit('3801')
c.label('aim_priority_shift36d');c.emit('b842');c.branch('6300','aim_priority_append36d');c.emit('2a3040fc218540005944');c.branch('6000','aim_priority_shift36d')
c.label('aim_priority_append36d');c.emit('218a2000');c.abs('5879',0xffff23b2)
c.label('aim_priority_reject36d');c.emit('4cdf7fff');c.abs('3e39',0xffff23b2);c.abs('4df9',0xffff23b4);c.emit('4e75');patch(0xec62,'aim_priority36d')
