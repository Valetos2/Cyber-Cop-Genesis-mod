# The red denial lamp is tile B2. Override it only while drawing this
# airlock, so the stored keypad/card state is independent of the alarm.
AIR_ALARM_DRAWN=0xffff086a
c.label('airlock_alarm_draw14')
c.abs('4a79',0xffff29ba);c.branch('6700','airlock_alarm_clear14')
c.abs('4a39',AIR_ALARM_DRAWN);c.branch('6600','airlock_alarm_lens14')
bi(AIR_ALARM_DRAWN,1);bi(0xffff2700,255)
c.label('airlock_alarm_lens14')
c.abs('3f39',0xffff7dce);wi(0xffff7dce,0xb2)
c.call(0x38c8);c.abs('33df',0xffff7dce);c.jump(0x4d18)
c.label('airlock_alarm_clear14')
c.abs('4a39',AIR_ALARM_DRAWN);c.branch('6700','airlock_clear_draw14')
c.abs('4239',AIR_ALARM_DRAWN);bi(0xffff2700,255)
c.label('airlock_clear_draw14');c.call(0x38c8);c.jump(0x4d18)
for p,expected in [(0x7764,'4ebac1624ebad5ae'),(0x77ac,'4ebac11a4ebad566')]:
 assert r[p:p+8]==bytes.fromhex(expected)
 name='airlock_frame_'+hex(p)
 c.label(name);c.call(c.labels['airlock_alarm_draw14']);c.jump(p+8)
 patch(p,name,8)

# A code entered before the alarm must not bypass the lockdown.
p=0x784c
assert r[p:p+6]==bytes.fromhex('4ef9')+struct.pack('>I',S['airlock_lab'])
c.label('airlock_alarm_open14')
c.abs('4a79',0xffff29ba);c.branch('6600','airlock_alarm_block14')
c.jump(S['airlock_lab'])
c.label('airlock_alarm_block14');c.emit('4e75')
patch(p,'airlock_alarm_open14')

# Only the successful mouse action owns the activation frame. Generic hover
# feedback must not rotate it before authorization, or for joystick activation.
AIR_MOUSE_OPEN=0xffff086b
p=0x771c
assert r[p:p+6]==src[p:p+6] and src[p:p+2]==bytes.fromhex('4ef9')
c.label('airlock_enter15')
c.abs('4239',AIR_MOUSE_OPEN);c.emit(src[p:p+6].hex())
patch(p,'airlock_enter15')
p=S['press_external']
assert r[p:p+10]==bytes.fromhex('044000092a79ffff226e')
c.label('airlock_pressed15')
c.emit('0c40006d');c.branch('6600','airlock_dispatch15')
c.emit('0cb9000077a8ffff26b8');c.branch('6600','airlock_dispatch15')
c.abs('4a79',0xffff29ba);c.branch('6600','airlock_dispatch15')
c.abs('4a39',0xffff26ec);c.branch('6700','airlock_dispatch15')
bi(AIR_MOUSE_OPEN,1)
c.label('airlock_dispatch15');c.emit(src[p:p+10].hex());c.jump(p+10)
patch(p,'airlock_pressed15',10)

p=S['panel_border']
c.label('airlock_border15')
c.emit('0cb9000077a8ffff26b8');c.branch('6600','airlock_border_native15')
c.abs('4a79',P);c.branch('6700','airlock_border_native15')
c.abs('4a39',AIR_MOUSE_OPEN);c.branch('6700','airlock_border_wait15')
c.abs('2079',0xffff227e);c.emit('0c6800c00074')
c.branch('6600','airlock_border_wait15')
# Same bounds as the generic projected button ($6052), in framebuffer pixels.
c.emit('303c00a1343c0041363c00af383c004f3a003c02');c.jump(S['border_top'])
c.label('airlock_border_wait15')
c.emit('0cb900006052ffff01b4');c.branch('6700','airlock_border_done15')
c.label('airlock_border_native15');c.emit(src[p:p+6].hex());c.jump(p+6)
c.label('airlock_border_done15');c.emit('4e75')
patch(p,'airlock_border15')
