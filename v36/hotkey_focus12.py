# Y already calls native Use and the native panel chooses its consumable.
# When playing with the pad's movement controls, don't switch into inventory
# mode just because Use opened a panel. X/Z still select items normally.
p=V['item_keys']
needle=bytes.fromhex('4ef9')+struct.pack('>I',V['use24'])
p=src.index(needle,p,p+90)
assert r[p:p+6]==needle
c.label('hotkey_use12')
c.abs('4a79',P);c.branch('6600','hotkey_use_native12')
c.abs('4a39',0xffff270a);c.branch('6600','hotkey_use_native12')
c.call(0x72ac)
c.abs('4239',0xffff270a)
c.emit('4e75')
c.label('hotkey_use_native12');c.jump(V['use24'])
patch(p,'hotkey_use12')
