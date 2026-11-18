# Use the stock button pairs for the duration of a valid mouse hold.
# The hitboxes and the edge-triggered action dispatch remain unchanged.
p=0x38c8
assert r[p:p+6]==bytes.fromhex('4ef9')+struct.pack('>I',c.labels['lift_feedback36e'])
c.label('scanman_draw21')
c.emit('0cb9000087c8ffff26b8');c.branch('6600','scanman_normal_draw21')
c.emit('48e7fffe')
c.abs('4a79',P);c.branch('6700','scanman_draw_idle21')
c.call(0x8940) # normalize any tile changes made by the native action
c.emit('08390000ffff01ad');c.branch('6700','scanman_draw_idle21')
c.call(S['owned_hover04'])
c.emit('4a40');c.branch('6700','scanman_draw_idle21')
c.abs('2039',N+20)
c.ref('45f9','scanman_native_tiles21')
c.emit('7404')
c.label('scanman_find_tile21')
c.emit('b09a');c.branch('6700','scanman_draw_held21')
c.emit('45ea000851ca');c.fix.append((len(c.b),'scanman_find_tile21',2));c.emit('0000')
c.label('scanman_draw_idle21')
c.abs('4a79',SCAN_VISUAL);c.branch('6700','scanman_draw_restore21')
wi(SCAN_VISUAL,0);bi(0xffff2700,255)
c.label('scanman_draw_restore21');c.emit('4cdf7fff')
c.label('scanman_normal_draw21');c.jump(c.labels['lift_feedback36e'])
c.label('scanman_draw_held21')
c.emit('5242')
c.abs('b479',SCAN_VISUAL);c.branch('6700','scanman_same_tile21')
c.abs('33c2',SCAN_VISUAL);bi(0xffff2700,255)
c.label('scanman_same_tile21')
c.abs('2279',0xffff227e)
c.emit('301a321a')
c.emit('3f3110003f310000')
c.emit('339a0000339a1000')
c.call(c.labels['lift_feedback36e'])
c.emit('339f0000339f1000')
c.emit('4cdf7fff4e75')
patch(p,'scanman_draw21')

# For each operation the two map offsets and tile indices come from the
# corresponding native handler at $8816/$8874/$8840/$890A/$88AC.
c.label('scanman_native_tiles21')
for node,off1,off2,tile1,tile2 in [
 (0x5a32,0x9c,0xb4,0x48,0x49), (0x5a46,0x98,0x9a,0x44,0x45),
 (0x5a5a,0x94,0x96,0x40,0x41), (0x5a6e,0x44,0x5c,0x3c,0x3d),
 (0x5a82,0x44,0x5c,0x3a,0x3b),
]:
 c.long(node)
 c.emit(struct.pack('>4H',off1,off2,tile1,tile2).hex())
