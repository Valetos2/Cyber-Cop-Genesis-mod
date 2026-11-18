# In mouse look, a fresh LMB edge with forward held starts the same jump as
# A+Up. Do not also synthesize A for this mouse gesture, so button release
# cannot jump again. Physical A is still available.
MOUSE_JUMP_HANDLED=0xffff087a
p=0x1833da
assert r[p:p+6]==bytes.fromhex('33c1ffff0196')
c.label('mouse_jump26')
c.emit('08040000');c.branch('6700','mouse_jump_released26')
c.emit('08050000');c.branch('6700','mouse_jump_held26')
c.abs('4239',MOUSE_JUMP_HANDLED)
c.emit('0cb900002106ffff26b8');c.branch('6600','mouse_jump_store26')
for addr,bit in [(0xffff270a,None),(0xffff270e,None),(0xffff0005,0)]:
 if bit is None:c.abs('4a39',addr)
 else:c.abs('08390000',addr)
 c.branch('6600','mouse_jump_store26')
bi(MOUSE_JUMP_HANDLED,1)
c.abs('4a39',0xffff26e8);c.branch('6600','mouse_jump_held26')
c.emit('2f01');c.call(0x9dea);c.call(0x9dbe);c.emit('221f')
c.label('mouse_jump_held26')
c.abs('4a39',MOUSE_JUMP_HANDLED);c.branch('6700','mouse_jump_store26')
c.emit('08810006');c.branch('6000','mouse_jump_store26')
c.label('mouse_jump_released26');c.abs('4239',MOUSE_JUMP_HANDLED)
c.label('mouse_jump_store26');c.emit(r[p:p+6].hex());c.jump(p+6)
patch(p,'mouse_jump26')
