# The ground sensor at $AD82 can skip its cell lookup in mid-air, leaving the
# cached $2442 unsuitable for placement. Resolve X/Z regardless of height.
p=0x7fde
assert r[p:p+10]==bytes.fromhex('4eba16da6b2c45eaffff')
c.label('disruptor_place17')
c.abs('3039',0xffff441a);c.emit('0c405000');c.branch('6400','disruptor_no_place17')
c.abs('3439',0xffff441e);c.emit('0c423200');c.branch('6400','disruptor_no_place17')
c.call(0xab3e)  # bounded native world lookup; A2 is the map cell
c.emit('4a12');c.branch('6700','disruptor_plant17')
# The native 3x3 search assumes all nine cells are within the map.
for compare in ('0c400100','0c404f00','0c420100','0c423100'):
 c.emit(compare);c.branch('6500' if compare.endswith('0100') else '6400','disruptor_no_place17')
c.call(0x96c0);c.branch('6b00','disruptor_no_place17')
c.emit('45eaffff')  # native search returns one byte beyond the free cell
c.label('disruptor_plant17');c.jump(0x7fe8)
c.label('disruptor_no_place17');c.emit('4e75')
patch(p,'disruptor_place17',10)

# Only a successful placement reaches consumption. Use the common selector
# to stay on an identical item or advance to its old right-hand neighbour.
# An empty inventory has no selectable group: don't enter its unbounded scan.
p=0x7fec
assert r[p:p+8]==bytes.fromhex('720043f9ffff2f50')
c.label('disruptor_consume17')
c.abs('41f9',0xffff2f50);c.abs('3239',0xffff2740)
c.emit('70007433')
c.label('disruptor_item_loop17')
c.emit('b041');c.branch('6700','disruptor_item_next17')
c.emit('4a300000');c.branch('6a00','disruptor_consume_group17')
c.label('disruptor_item_next17')
c.emit('5240');c.branch('51ca','disruptor_item_loop17')
c.emit('50f01000');wi(0xffff2740,0);wi(0xffff21ba,0xffff);c.jump(0x6738)
c.label('disruptor_consume_group17');c.jump(0x7204)
patch(p,'disruptor_consume17',8)
