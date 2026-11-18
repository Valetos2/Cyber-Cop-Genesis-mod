# Offset the round biped's screen projection by 22 world units, four pixels
# in the six-cell comparison. The common centre feeds both sprite halves
# and the death poses. Leave the actor's position and hitbox intact.
p=0x44f0
assert r[p:p+8]==bytes.fromhex('3140000e31410010')
c.label('robot_floor27')
c.emit('0c2800060003');c.branch('6600','robot_floor_store27')
c.abs('b1fc',0xffff4468);c.branch('6500','robot_floor_store27')
c.abs('b1fc',0xffff4f7e);c.branch('6400','robot_floor_store27')
c.emit('4a47');c.branch('6f00','robot_floor_store27')
c.emit('2f02243c0000160085c79242241f')
c.label('robot_floor_store27')
c.emit(r[p:p+8].hex());c.jump(p+8)
patch(p,'robot_floor27',8)
