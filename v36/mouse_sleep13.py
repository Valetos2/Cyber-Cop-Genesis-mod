# Optional fourth button follows the existing Mode action. Ignore it in
# object panels and consume it on a simultaneous physical Start.
p=V['mode_action']
assert r[p:p+6]==bytes.fromhex('3039ffff0012')
c.label('mouse_sleep_toggle13')
c.abs('4a79',P);c.branch('6700','mouse_sleep_native13')
c.abs('4a39',MOUSE_PRESENT);c.branch('6700','mouse_sleep_native13')
c.emit('08390003ffff023b');c.branch('6700','mouse_sleep_native13')
c.jump(p+0x16) # the guard and native Mode sleep/wake entry
c.label('mouse_sleep_native13');c.emit(src[p:p+6].hex());c.jump(p+6)
patch(p,'mouse_sleep_toggle13')
