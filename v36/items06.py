# Bit6 is unused for pickup cells25..3F in both campaigns. Preserve it as a
# broken-item marker in world maps, which native floor persistence copies.
# D7 still contains the original inventory byte at the drop store.
c.label('drop_broken36f');c.emit('08070006');c.branch('6700','drop_store36f');c.emit('00010040')
c.label('drop_store36f');c.emit(src[0x6d2c:0x6d34].hex());c.jump(0x6d34);patch(0x6d2c,'drop_broken36f',8)
# Wrap native nearby scanner; retain its shared return at9EE0 and append marker
# only when a pickup was actually appended to the nearby-inventory list.
c.label('nearby_broken36f');c.emit('2f08204912000200003f');c.call(0x9eae);c.emit('b3c8');c.branch('6700','nearby_done36f');c.emit('0c010065');c.branch('6500','nearby_done36f');c.emit('0c01007f');c.branch('6200','nearby_done36f');c.emit('08e90006ffff')
c.label('nearby_done36f');c.emit('205f4e75');patch(0x9ea8,'nearby_broken36f',6)
# Eligibility ignores the damage bit, but icon/name rendering receives it.
c.label('nearby_eligible36f');c.emit('2f0008800006');c.abs('4a79',0xffff219a);c.branch('6700','nearby_limit36f');c.emit('0c40000b');c.branch('6700','nearby_eligible_done36f')
c.label('nearby_limit36f');c.emit('0c40001e');c.branch('6e00','nearby_eligible_done36f');bi(0xffff270d,255)
c.label('nearby_eligible_done36f');c.emit('201f');c.jump(0x6f78);patch(0x6f5c,'nearby_eligible36f',28)
# Inventory->world mapping must retain the marker for matching/removing pickups.
c.label('item_world36f');c.emit('2f002f0930010241003f');c.abs('43f9',0x9f24);c.emit('1231100008000006');c.branch('6700','item_world_done36f');c.emit('00010040')
c.label('item_world_done36f');c.emit('225f201f4e75');patch(0x9f1e,'item_world36f',6)
# A previously broken pickup must neither roll RNG nor become intact.
c.label('pickup_broken36f');c.emit('08010006');c.branch('6600','pickup_broken_done36f');c.emit('0c01001e');c.branch('6700','pickup_broken_done36f');c.jump(0x6b3c)
c.label('pickup_broken_done36f');c.emit('4e75');patch(0x6b36,'pickup_broken36f',6)
# Native floor-change persistence otherwise strips bit6 before saving the cell.
c.label('persist_broken36f');c.emit('12c112c21628ffff0203007f12c3');c.jump(0x4ab6);patch(0x4ab0,'persist_broken36f',6)
