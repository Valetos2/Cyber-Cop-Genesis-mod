# Cursor ownership is transient and separate from the actual Mouse On setting.
SLEEP_PAD=0xffff0862       # byte: zero = mouse, one = pad
SLEEP_REDRAW=0xffff0863    # byte: pad took ownership; erase/redraw if needed
START_WAKE_PENDING=0xffff087c
START_SLEEP=0xffff0864     # byte: require a new Start press for this sleep
SLEEP_ACTIVE=0xffff0118
SLEEP_MODE=0xffff26b8

def sleep_branch(op,target):
 c.emit('0cb900007070');c.long(SLEEP_MODE);c.branch(op,target)

def sleep_owner_clear():
 c.abs('4279',SLEEP_PAD)   # both bytes, also initially zeroed by reset36

# At the input boundary, before the world or sleep logic consumes the snapshot.
# A new mouse click or movement wins if both devices report activity this frame.
c.label('sleep_cursor_activity36')
sleep_branch('6600','sleep_cursor_inactive36')
c.abs('4a39',SLEEP_ACTIVE);c.branch('6700','sleep_cursor_inactive36')
c.abs('4a79',P);c.branch('6700','sleep_cursor_activity_done36')
c.abs('4a39',0xffff0192);c.branch('6700','sleep_cursor_try_pad36')
c.abs('4ab9',P+48);c.branch('6600','sleep_cursor_to_mouse36')
c.abs('4ab9',P+52);c.branch('6600','sleep_cursor_to_mouse36')
c.abs('3039',P+58);c.emit('02400003');c.branch('6600','sleep_cursor_to_mouse36')
c.label('sleep_cursor_try_pad36')
# The same low seven edge bits sleep16_armed uses; exclude Start.
c.abs('3039',0xffff0004);c.emit('4640');c.abs('c079',0xffff0006)
c.emit('0240007f');c.branch('6700','sleep_cursor_activity_done36')
c.abs('4a39',SLEEP_PAD);c.branch('6600','sleep_cursor_activity_done36')
bi(SLEEP_PAD,1);bi(SLEEP_REDRAW,1)
# A held mouse button must not continue dragging after handing control to the pad.
c.abs('4279',P+64)
c.branch('6000','sleep_cursor_activity_done36')
c.label('sleep_cursor_to_mouse36')
c.abs('4a39',SLEEP_PAD);c.branch('6700','sleep_cursor_activity_done36')
sleep_owner_clear();wi(P+4,1);c.branch('6000','sleep_cursor_activity_done36')
c.label('sleep_cursor_inactive36')
sleep_owner_clear();c.abs('4279',P+70)
c.label('sleep_cursor_activity_done36');c.jump(S['lift_busy35c'])

needle=bytes.fromhex('4eb9')+struct.pack('>I',S['lift_busy35c'])
p=src.index(needle,S['consume'],S['mouse_present'])
assert r[p:p+6]==needle
r[p+2:p+6]=struct.pack('>I',c.labels['sleep_cursor_activity36'])

# Only the visibility gates change. The native cursor offsets and draw calls
# still match the current page, including the lamps and sensitivity entries.
p=S['cursor']
assert r[p:p+10]==bytes.fromhex('4a79ffff02006700')+struct.pack('>h',S['cursor_hide05']-p-8)
c.label('sleep_cursor_sprite36')
c.abs('4a79',P);c.branch('6700','sleep_cursor_hide36')
c.abs('4a39',SLEEP_PAD);c.branch('6700','sleep_cursor_sprite_native36')
sleep_branch('6600','sleep_cursor_sprite_native36')
c.abs('4a39',SLEEP_ACTIVE);c.branch('6600','sleep_cursor_hide36')
c.label('sleep_cursor_sprite_native36');c.jump(p+10)
c.label('sleep_cursor_hide36');c.jump(S['cursor_hide05']);patch(p,'sleep_cursor_sprite36',10)

p=S['sleep_arrow03_check']
assert r[p:p+10]==bytes.fromhex('4a79ffff02006600')+struct.pack('>h',S['arrow03_done']-p-8)
c.label('sleep_cursor_arrow36')
c.abs('4239',SLEEP_REDRAW)
c.abs('4a79',P);c.branch('6700','sleep_cursor_arrow_draw36')
c.abs('4a39',SLEEP_PAD);c.branch('6700','sleep_cursor_arrow_done36')
c.label('sleep_cursor_arrow_draw36');c.jump(p+10)
c.label('sleep_cursor_arrow_done36');c.emit('4e75')
patch(p,'sleep_cursor_arrow36',10)

# Do not use P+4 for the pad handoff: sleep_frame03 would bypass native input.
# Normal actions redraw and clear the pending byte at the arrow gate. A
# button with no action on this row gets just the redraw here.
p=V['sleep16_show']
assert r[p:p+6]==bytes.fromhex('4eb900002930')
c.label('sleep_cursor_show36')
c.abs('4a39',SLEEP_REDRAW);c.branch('6700','sleep_cursor_show_native36')
c.call(V['sleep16_draw'])
c.label('sleep_cursor_show_native36');c.call(0x2930);c.jump(p+6)
patch(p,'sleep_cursor_show36')

# In pad mode a previously held mouse button cannot run cursor-side actions.
p=S['sleep_mouse']
assert r[p:p+8]==bytes.fromhex('33fc0001ffff01a0')
c.label('sleep_cursor_mouse36')
c.abs('4a39',SLEEP_PAD);c.branch('6600','sleep_cursor_mouse_pad36')
c.emit(r[p:p+8].hex());c.jump(p+8)
c.label('sleep_cursor_mouse_pad36');c.jump(S['consume_end'])
patch(p,'sleep_cursor_mouse36',8)

# Soft-off recovers on either mouse button without moving the pointer. On
# wake, expire it immediately rather than waiting for the next awake poll.
p=S['soft_off06']
needle=bytes.fromhex('3039ffff023a08000000')
i=src.index(needle,p,S['disabled05'])
assert r[i:i+len(needle)]==needle
r[i+6:i+10]=bytes.fromhex('02400003')
p=S['toggle05_on']
assert r[p:p+6]==bytes.fromhex('4279ffff0246')
c.label('sleep_cursor_toggle_on36')
sleep_owner_clear();c.emit(r[p:p+6].hex());c.jump(p+6)
patch(p,'sleep_cursor_toggle_on36')

assert r[0x709a:0x70a2]==bytes.fromhex('4ef9')+struct.pack('>I',V['sleep16_wake'])+bytes.fromhex('4e71')
c.label('sleep_cursor_wake36')
sleep_owner_clear();c.abs('4279',P+70);c.abs('4279',P+4)
c.abs('4239',START_SLEEP);c.abs('4239',START_WAKE_PENDING)
c.jump(V['sleep16_wake'])
patch(0x709a,'sleep_cursor_wake36',8)
