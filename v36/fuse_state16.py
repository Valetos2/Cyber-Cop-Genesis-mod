# Native fuse words ($2150..$216a) drive world palette, lamps and panel tiles.
# Test maps still render native floor 0. Switch 0 controls that floor, not the
# parity of all fourteen clicks. Automatic restoration never writes to $227e:
# it can point to the data of an entirely different panel after closing one.
FUSE_WORDS=0xffff2150
FUSE_BOX_TILES=0xffff81c6
FUSE_TICK=0xffff086c
FUSE_MIGRATED=0xffff086e
FUSE_INTERVAL=256  # only the low byte of native $29ac advances in gameplay

# Old laboratory savestates can have the first tile right and word 0 wrong.
# Import only that displayed switch once and only if the tile is recognizable.
c.label('fuse_migrate16')
c.abs('4a39',FUSE_MIGRATED);c.branch('6600','fuse_migrate_done16')
c.emit('50f9');c.long(FUSE_MIGRATED)
c.abs('4a79',P+108);c.branch('6700','fuse_migrate_done16')
tile0=FUSE_BOX_TILES+struct.unpack_from('>H',src,0x7aba)[0]
c.emit('0c7900ed');c.long(tile0);c.branch('6700','fuse_migrate_on16')
c.emit('0c7900ee');c.long(tile0);c.branch('6600','fuse_migrate_done16')
wi(FUSE_WORDS,0xffff);c.emit('4e75')
c.label('fuse_migrate_on16');c.abs('4279',FUSE_WORDS)
c.label('fuse_migrate_done16');c.emit('4e75')

p=0x7ad6
assert r[p:p+6]==bytes.fromhex('45f9ffff81c6')
c.label('fuse_init16')
c.abs('4279',FUSE_TICK);c.emit('50f9');c.long(FUSE_MIGRATED)
c.emit(src[p:p+6].hex());c.jump(p+6);patch(p,'fuse_init16')

p=0x7b2a
assert r[p:p+6]==bytes.fromhex('3039ffff2606')
c.label('fuse_power16')
c.call(c.labels['fuse_migrate16'])
c.emit(src[p:p+6].hex());c.jump(p+6);patch(p,'fuse_power16')

# The open routine is also a timer refresh. Regenerate the display from the
# fuse words; ED is on and EE is off.
p=0x7a00
assert r[p:p+6]==bytes.fromhex('4ef9')+struct.pack('>I',S['open09_7a00'])
c.label('fuse_open16')
c.emit('48e7e070')
c.call(c.labels['fuse_migrate16']);c.abs('4279',FUSE_TICK)
c.abs('43f9',0x7aba);c.abs('45f9',FUSE_BOX_TILES);c.abs('47f9',FUSE_WORDS)
c.emit('700d')
c.label('fuse_open_loop16')
# D1 = tile-map offset, D2 = displayed tile.
c.emit('3219343c00ed')
c.emit('4a5b');c.branch('6700','fuse_open_show16')
c.emit('5242')
c.label('fuse_open_show16')
c.emit('35821000');c.branch('51c8','fuse_open_loop16')
c.emit('4cdf0e07')
c.jump(S['open09_7a00']);patch(p,'fuse_open16')

p=0x7a92
assert r[p:p+6]==bytes.fromhex('4ef9')+struct.pack('>I',S['fuse_lab'])
c.label('fuse_switch16')
c.emit('0c40000d');c.branch('6200','fuse_switch_done16')
c.call(c.labels['fuse_migrate16'])
c.emit('3200d241');c.abs('41f9',FUSE_WORDS)
c.emit('0a70ffff1000')
c.branch('6700','fuse_switch_on16');c.emit('343c00ee')
c.branch('6000','fuse_switch_show16')
c.label('fuse_switch_on16');c.emit('343c00ed')
c.label('fuse_switch_show16')
c.abs('41f9',0x7aba);c.emit('32301000');c.abs('41f9',FUSE_BOX_TILES);c.emit('31821000')
c.emit('0cb900007a60ffff26b8');c.branch('6600','fuse_switch_done16')
c.abs('4279',FUSE_TICK);c.emit('50f9ffff2700')
c.label('fuse_switch_done16');c.emit('4e75')
patch(p,'fuse_switch16')

# Count updates spent in the world, instead of triggering on an absolute
# counter phase. Keep the native RNG and twentyfold destroyed-box delay.
p=0x3302
assert r[p:p+6]==bytes.fromhex('4ef9')+struct.pack('>I',V['fuse26_tick'])
c.label('fuse_tick16')
c.emit('0cb900002106ffff26b8');c.branch('6600','fuse_tick_done16')
c.emit('5279');c.long(FUSE_TICK)
c.emit(f'0c79{FUSE_INTERVAL:04x}');c.long(FUSE_TICK)
c.branch('6500','fuse_tick_done16');c.abs('4279',FUSE_TICK)
c.jump(V['fuse26_tick']+14) # past the native absolute phase check
c.label('fuse_tick_done16');c.emit('4e75')
patch(p,'fuse_tick16')

p=0x7b12
assert r[p:p+6]==bytes.fromhex('4ef9')+struct.pack('>I',V['fuse26_destroy'])
c.label('fuse_destroy16')
c.abs('4279',FUSE_TICK)
c.jump(V['fuse26_destroy']);patch(p,'fuse_destroy16')
