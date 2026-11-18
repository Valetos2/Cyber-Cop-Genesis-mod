# On the post-death route the memorial's name table can still be present
# on plane A after the usual clears. SEGA uses plane B and overwrites the
# memorial tile patterns, making those old references display wrong art.
# Clear plane A with the stock RAM->VDP DMA routine immediately before SEGA.
sega_blank41=asset('sega_blank_plane41',bytes(0x1000))
assert r[0x3be:0x3c8]==bytes.fromhex('4eba21b641f900081374')
c.label('sega_clear_plane41')
c.abs('41f9',sega_blank41)
c.emit('303c1000323ce000')
c.call(0x2580)
c.call(0x2576)
c.abs('41f9',0x81374)
c.jump(0x3c8)
patch(0x3be,'sega_clear_plane41',10)
