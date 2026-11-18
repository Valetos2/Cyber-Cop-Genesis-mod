# The display starts using the sleep cache as soon as $26B8 becomes $7070,
# before the fade and the final sleep initializer. Seed it at that transition.
p=0x6fc8
assert r[p:p+10]==bytes.fromhex('23fc00007070ffff26b8')
c.label('sleep_meter_enter30')
c.abs('33f9',0xffff2a2a);c.long(0xffff015c)
c.emit(r[p:p+10].hex());c.jump(p+10)
patch(p,'sleep_meter_enter30',10)
