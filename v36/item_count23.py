# $6F06 counts matching inventory bytes (52 slots); the old HUD capped at 9.
# The second tile is empty in the stock plane. Clear it on every short count.
assert r[0x6f22:0x6f2a]==bytes.fromhex('0c4000096f027009')
r[0x6f22:0x6f2a]=bytes.fromhex('4e71')*4
assert r[0x6eee:0x6ef4]==bytes.fromhex('0c4000016e04')
c.label('inventory_count23')
c.abs('4a79',0xffff21ba);c.branch('6b00','inventory_count_blank23')
c.emit('0c400001');c.branch('6f00','inventory_count_blank23')
c.emit('0c40000a');c.branch('6d00','inventory_count_single23')
c.emit('80fc000a2f00') # quotient low, remainder high
c.emit('0640001b343ced32');c.call(0x35fe)
c.emit('201f48400640001b');c.branch('6000','inventory_count_units23')
c.label('inventory_count_blank23');c.emit('7000');c.branch('6000','inventory_count_short23')
c.label('inventory_count_single23');c.emit('0640001b')
c.label('inventory_count_short23')
c.emit('343ced32');c.call(0x35fe);c.emit('7000')
c.label('inventory_count_units23')
c.emit('343ced34');c.jump(0x35fe)
patch(0x6eee,'inventory_count23')
