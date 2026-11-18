# Polls happen once per VBlank. A good packet resets this counter in poll03_ok.
MOUSE_MISSES=0xffff0224
MOUSE_DISCONNECT_FRAMES=30
POLL_END=0x1802f4
POLL_CLEAR_INPUT=0x1802d8
assert src[POLL_CLEAR_INPUT:POLL_END]==bytes.fromhex(
 '33fc0000ffff018c33fc0000ffff019042b9ffff018442b9ffff0188')
p=S['poll03_bad']
assert r[p:p+14]==bytes.fromhex('5279ffff02240c790002ffff0224')
c.label('mouse_missed11')
c.emit('0c79'+f'{MOUSE_DISCONNECT_FRAMES:04x}');c.long(MOUSE_MISSES)
c.branch('6400','mouse_disconnect11')
c.abs('5279',MOUSE_MISSES)
c.emit('0c79'+f'{MOUSE_DISCONNECT_FRAMES:04x}');c.long(MOUSE_MISSES)
c.branch('6400','mouse_disconnect11')
# Keep the legacy tolerance of one lost packet with a held button. From
# the second, discard stale buttons and movement, but keep device presence.
c.emit('0c790002');c.long(MOUSE_MISSES);c.branch('6400','mouse_idle11')
c.jump(POLL_END)
c.label('mouse_idle11');c.jump(POLL_CLEAR_INPUT)
c.label('mouse_disconnect11');c.jump(S['poll03_disconnect'])
patch(p,'mouse_missed11')

# With the old held state discarded, the first good packet is the new
# baseline. Held bits still reflect the device, but do not synthesize presses.
p=0x1802ae
assert r[p:p+6]==bytes.fromhex('3039ffff018c')
c.label('mouse_resume11')
c.emit('0c790002');c.long(MOUSE_MISSES);c.branch('6500','mouse_resume_old11')
c.emit('3002');c.jump(p+6)
c.label('mouse_resume_old11');c.emit(src[p:p+6].hex());c.jump(p+6)
patch(p,'mouse_resume11')
