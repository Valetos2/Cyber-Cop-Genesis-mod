SCAN_VISUAL=0xffff0872
# $79BA installs the whole panel palette, including the eight colors that
# the earlier $88E6 call set for brightness 8. Apply brightness afterwards.
p=0x875c
assert r[p:p+4]==bytes.fromhex('4eba0188')
r[p:p+4]=bytes.fromhex('4e714e71')
p=0x87a2
assert r[p:p+8]==bytes.fromhex('41fad1da4eba077c')
c.label('scanman_entry20')
wi(SCAN_VISUAL,0)
c.abs('3039',0xffff2180)
c.call(0x88e6)
c.abs('41f9',0x597e);c.call(0x8f24)
# Auto-selection sets a world HUD node. Restore the equivalent panel node
# after it runs so the Up link actually reaches the Scanman controls.
for screen in (0x19,0x1a,0x1b):
 c.emit(f'303c{screen:04x}');c.call(0x8f4a)
 if screen!=0x1b:c.branch('6b00','scanman_entry_focus20')
c.label('scanman_entry_focus20')
c.abs('4a79',P);c.branch('6600','scanman_entry_continue20')
# Start on the panel's Use slot; B loads the chosen Screen, Up reaches Reset.
c.emit('50f9ffff270a')
c.emit('23fc00005a0affff202a')
c.label('scanman_entry_continue20');c.emit('4e75')
patch(p,'scanman_entry20',8)
