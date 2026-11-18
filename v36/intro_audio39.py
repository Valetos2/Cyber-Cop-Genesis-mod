# Keep the title theme silent through the QR. Fire when the logo palette is
# armed. The stock early-skip path still uses the menu's idempotent ensure.
assert r[0x4de:0x4e8]==bytes.fromhex('303c00014eb9000150b4')
r[0x4de:0x4e8]=bytes.fromhex('4e71')*5
assert r[0x5cc:0x5d2]==bytes.fromhex('50f9ffff2702')
c.label('intro_logo_music39')
c.abs('50f9',0xffff2702)
c.call(V['music20_ensure'])
c.jump(0x5d2)
patch(0x5cc,'intro_logo_music39')

# The screen is already faded out. During the story uploads the blanked
# display gives the VDP more DMA slots. Keep VINT enabled and leave the
# stock DMA's SR and Z80 bus arbitration untouched.
assert r[0x658:0x660]==bytes.fromhex('323c1000343cc000')
assert r[0x6bc:0x6c4]==bytes.fromhex('4eba0e384eba0dcc')
c.label('intro_story_blank39')
c.abs('3f39',0xffff0002)
c.emit('08b90006');c.long(0xffff0003)
c.abs('33f9',0xffff0002);c.long(0xc00004)
c.emit(r[0x658:0x660].hex())
c.jump(0x660)
patch(0x658,'intro_story_blank39',8)

c.label('intro_story_show39')
c.emit('082f00060001')  # prior display-enable bit in saved register word
c.branch('6700','intro_story_saved_blank39')
c.emit('08f90006');c.long(0xffff0003)
c.label('intro_story_saved_blank39')
c.emit('548f')          # discard saved word
c.abs('33f9',0xffff0002);c.long(0xc00004)
c.call(0x14f6);c.call(0x148e)
c.jump(0x6c4)
patch(0x6bc,'intro_story_show39',8)
