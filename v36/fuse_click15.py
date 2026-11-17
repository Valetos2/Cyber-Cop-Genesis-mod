# Fuse tick used the Start level, unlike the mouse's once-per-press dispatch.
# Keep a left click on a fuse independent of the exit input, and only close on
# a new Start/right click. Use the actual held switch owner, not hover alone.
p=0x7a72
assert r[p:p+6]==bytes.fromhex('080000076618')
c.label('fuse_exit15')
c.emit('08000007');c.branch('6600','fuse_keep15')
c.emit('08390007ffff0007');c.branch('6700','fuse_keep15')
c.abs('4a79',P);c.branch('6700','fuse_close15')
c.emit('08390000ffff01ad');c.branch('6700','fuse_close15')
c.emit('0cb900006068ffff01c8');c.branch('6600','fuse_close15')
c.abs('2039',N+20);c.emit('0c800000611c');c.branch('6500','fuse_close15')
c.emit('0c8000006224');c.branch('6500','fuse_keep15')
c.branch('6700','fuse_keep15')
c.label('fuse_close15');c.jump(0x7a78)
c.label('fuse_keep15');c.emit('4e75')
patch(p,'fuse_exit15')

# The shared dispatcher subtracts 9 from a UI node ID. Only 14 indices
# belong to this callback; don't let a mismatched selection write past either table.
p=0x7a92
assert r[p:p+6]==bytes.fromhex('4ef9')+struct.pack('>I',S['fuse_lab'])
c.label('fuse_switch15')
c.emit('0c40000d');c.branch('6200','fuse_keep15')
c.jump(S['fuse_lab'])
patch(p,'fuse_switch15')
