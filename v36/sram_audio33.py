"""Save music/SFX preferences alongside each campaign's verified X21 checkpoint."""
# This record starts immediately after the existing X21 payload. It remains
# in the odd-byte SRAM lane. Every routine touching SRAM runs below 2 MiB.
AUDIO_SIDE = 0x200805
c.label('sram_audio_addr33')
c.abs('47f9',AUDIO_SIDE);tstcamp()
c.branch('6700','sram_audio_addr_done33');c.emit('d6fc2000') # adda.w #$2000,a3
c.label('sram_audio_addr_done33');c.emit('4e75')

p=0xf83c2
assert r[p:p+8] == bytes.fromhex('42114ef9')+struct.pack('>I',c.labels['sram36_f83c4'])
c.label('sram_audio_invalidate33')
c.emit('4211') # existing X21 mark clear
c.call(c.labels['sram_audio_addr33']);c.emit('4213') # sidecar mark clear
c.jump(c.labels['sram36_f83c4'])
patch(p,'sram_audio_invalidate33',8)

p=0xf84cc
assert r[p:p+8] == bytes.fromhex('13fc000000a130f1')
c.label('sram_audio_save33')
c.call(c.labels['sram_audio_addr33'])
c.emit('3002e0481740000217420004') # X21 checksum high and low
c.emit('7000')
c.abs('4a39',0xffff2710);c.emit('57c0') # music on -> FF
c.emit('02000001d000') # bit 1 = music on
c.abs('4a39',0xffff2711);c.branch('6600','sram_audio_mark33')
c.emit('5200') # bit 0 = SFX on
c.label('sram_audio_mark33')
c.emit('17400006460017400008')
fuse_fields34('write');c.emit('16bc00b4') # flags, complement, validity mark
c.emit(src[p:p+8].hex());c.jump(p+8);patch(p,'sram_audio_save33',8)

# Restore before the existing late-resume music check. This path runs only
# after validation of the X21 checksum and its binding to the saved password.
p=0xf872a
assert r[p:p+8] == bytes.fromhex('13fc000000a130f1')
c.label('sram_audio_restore33')
c.call(c.labels['sram_audio_addr33'])
for mark in (0xb4,0xa2):
    c.emit(f'0c13{mark:04x}');c.branch('6700','sram_audio_valid34')
c.emit('0c1300a1');c.branch('6600','sram_audio_done33')
c.label('sram_audio_valid34')
for off, legacy in [(2,0x20004d),(4,0x20004f)]:
    rel=(legacy-AUDIO_SIDE)&0xffff
    c.emit(f'102b{off:04x}b02b{rel:04x}');c.branch('6600','sram_audio_done33')
c.emit('102b00060c000003');c.branch('6200','sram_audio_done33')
c.emit('12004601b22b0008');c.branch('6600','sram_audio_done33')
for bit,addr in [(1,0xffff2710),(0,0xffff2711)]:
    c.emit(f'0800{bit:04x}');c.abs('57f9',addr) # seq.b: clear bit means off
c.emit('0c1300a1');c.branch('6700','fuse_bad34')
fuse_fields34('check');fuse_fields34('read')
c.label('fuse_bad34')
c.label('sram_audio_done33')
c.emit(src[p:p+8].hex());c.jump(p+8);patch(p,'sram_audio_restore33',8)
