# Decoder codes contain four decimal digits, packed in nibbles. Testing the
# remaining value for zero loses one or more zeroes at the end (7650, 1200).
PICK_DIGITS=0xffff087e
p=0x9c14
assert r[p:p+10]==bytes.fromhex('33f9ffff243affff21ac')
c.label('lockpick_start28')
bi(PICK_DIGITS,4);c.emit(r[p:p+10].hex());c.jump(p+10)
patch(p,'lockpick_start28',10)
p=0x98e4
assert r[p:p+12]==bytes.fromhex('72003239ffff21ac67000216')
c.label('lockpick_digit28')
c.abs('4a39',PICK_DIGITS);c.branch('6600','lockpick_more28')
c.jump(0x9b04)
c.label('lockpick_more28')
c.abs('5339',PICK_DIGITS)
c.emit(r[p:p+8].hex());c.jump(p+12)
patch(p,'lockpick_digit28',12)
