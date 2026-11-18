# The panel close used to paint plain HUD names synchronously after the
# pressed Drop overlay, so the following VBlank appeared to press it again.
# Publish the base and the overlay in the same VBlank instead.
HUD_REPAINT37=0xffff0880 # zero on reset and on old emulator states
p=0x21d8
assert r[p:p+6]==bytes.fromhex('4ef9')+struct.pack('>I',c.labels['terminal_hud36b'])
c.label('hud_close37')
c.call(S['close08'])
c.abs('4239',HUD_REPAINT37)
c.emit('4e75')
patch(p,'hud_close37')

p=S['hud_draw']
assert r[p:p+6]==bytes.fromhex('4a79ffff0274')
c.label('hud_publish37')
c.abs('4a39',HUD_REPAINT37);c.branch('6600','hud_publish_done37')
c.abs('4a79',P+116);c.branch('6700','hud_publish_done37')
c.emit('0c795348');c.long(P+6);c.branch('6600','hud_publish_done37')
c.abs('4a79',P+34);c.branch('6700','hud_publish_done37')
c.emit('0cb900002106ffff26b8');c.branch('6600','hud_publish_done37')
wi(0xc00004,0x8f02)
c.abs('41f9',P+128)
for row in range(2):
    dst=0xe992+row*128
    c.abs('23fc',(((dst&0x3fff)|0x4000)<<16)|(dst>>14));c.long(0xc00004)
    c.emit('7e17')
    c.label('hud_publish_row37_'+str(row))
    c.abs('33d8',0xc00000)
    c.branch('51cf','hud_publish_row37_'+str(row))
bi(HUD_REPAINT37,1)
c.label('hud_publish_done37')
c.emit(src[p:p+6].hex());c.jump(p+6)
patch(p,'hud_publish37')

# A panel exit masks the mouse until physical release to avoid a second
# click in the world. Keep the existing Drop hold only for its visual;
# the press/event bits stay masked and no action can be repeated.
p=S['guard08_mask']
assert r[p:p+6]==bytes.fromhex('4279ffff0238')
c.label('drop_hold37')
c.emit('0cb9000056bc');c.long(N+20)
c.branch('6600','drop_hold_other37')
c.abs('4a79',N);c.branch('6700','drop_hold_other37')
c.emit('02790001');c.long(P+56)
c.jump(p+6)
c.label('drop_hold_other37')
c.emit(src[p:p+6].hex());c.jump(p+6)
patch(p,'drop_hold37')
