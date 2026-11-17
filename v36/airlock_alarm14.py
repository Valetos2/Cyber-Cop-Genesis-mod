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
