# Scanman reset restores both view selection and its palette immediately.
# Native entry 8754 already initializes brightness to 8 on every opening.
c.label('scan_reset36d');wi(0xffff217c,4);wi(0xffff2180,8);c.emit('7008');c.call(0x88e6);c.emit('4e75');patch(0x8836,'scan_reset36d',8)
# Compute lamp vertical radius before screen-coordinate rounding. Subtracting
# two rounded projected positions made the radius oscillate 1 -> 3 -> 1.
# near = depth-radius; ry = abs(height-cameraY)*256*radius/(depth*near).
c.label('lamp_radius36d');c.emit('48e7c0003028000a');c.abs('9079',0xffff2624);c.branch('6a00','lamp_radius_positive36d');c.emit('4440')
c.label('lamp_radius_positive36d');c.abs('c0f9',0xffff2234);c.emit('7a08eba03207');c.abs('d279',0xffff2234);c.emit('80c102800000ffff80c73000');c.emit('3400');c.emit('4cdf0003');c.emit('0c420001');c.branch('6c00','lamp_radius_ready36d');c.emit('7401')
c.label('lamp_radius_ready36d');c.jump(0xd074);patch(0xd050,'lamp_radius36d',10)

# Native repair release updates its icon and clears the repair-active word.
c.label('sleep_release36d');c.emit('48e7fffe');c.call(S['release_ui']);c.call(0x71e2);c.emit('4cdf7fff');c.jump(c.labels['sleep_sound_stop36']);patch(V['sleep17_begin'],'sleep_release36d')
# One copy per reusable tool in equipment selection. Use the existing disabled
# icon sentinel; each distinct mask remains a separate choice.
c.label('gear_unique36d');c.emit('0c400014');c.branch('6700','gear_disable36d');c.emit('0c40000c');c.branch('6500','gear_unique_native36d');c.emit('0c400012');c.branch('6200','gear_unique_native36d')
c.label('gear_disable36d')
c.emit('3200e54922701000337cffff0000');c.jump(0xfdb0)
c.label('gear_unique_native36d');c.emit('0c40000b');c.branch('6600','gear_unique_other36d');c.jump(0xfd8a);c.label('gear_unique_other36d');c.jump(0xfd94);patch(0xfd84,'gear_unique36d')
# First aid explicitly does nothing for droids (native754C/7552). Keep
# electronics available to humans: bionic limbs can require it.
# Gas loop31F4 exits for droids before testing either mask (3210/3216).
for a in [0x104a6,0x104b2,0x10506]:r[a]=255
