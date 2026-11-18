# The same item callback is used for Program and the recharge cable.
# A terminal enters the authenticated state when its card symbol becomes $9A.
# Discard a cable request before then, leaving Computer/Program untouched.
p=0x7602
assert r[p:p+6]==bytes.fromhex('50f9ffff26ef')
c.label('terminal_charge15')
c.emit('0cb900007c42ffff26b8');c.branch('6600','terminal_charge_native15')
c.emit('0c79009affff7e62');c.branch('6600','terminal_charge_done15')
c.label('terminal_charge_native15');c.emit(src[p:p+6].hex())
c.label('terminal_charge_done15');c.emit('4e75')
patch(p,'terminal_charge15')

# Native card insertion installs this dispatcher, but its pointer can survive
# until a subsequent visit. Protect all three commands at the callback too.
p=0x7cce
assert r[p:p+8]==bytes.fromhex('d040d040287b0004')
c.label('terminal_commands15')
c.emit('0c79009affff7e62');c.branch('6600','terminal_charge_done15')
c.emit('0c400002');c.branch('6200','terminal_charge_done15')
c.emit('d040d040');c.abs('49f9',0x7cd8);c.emit('287400004ed4')
patch(p,'terminal_commands15',8)
