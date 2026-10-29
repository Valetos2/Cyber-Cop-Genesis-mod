# Panel lifetime: save the pre-panel pointer mode once, restore on native close.
# P+84 active; P+86 saved mode; P+90 suppress held mouse buttons across close.
c.label('save_mode08');c.emit('4e75')
c.label('panel_enter08');tst(P);branch('6700','enter08_done');tst(P+84);branch('6600','enter08_done');wi(P+84,1);ld(0,N);st(0,P+86)
c.label('enter08_done');c.emit('4e75')
c.label('panel_return08');tst(P+104);branch('6600','return08_done');tst(P+84);branch('6700','return08_done');c.emit('0cb900002106');c.address(0xffff26b8);branch('6600','return08_done');clear(P+84);tst(P);branch('6700','return08_done');ld(0,P+86);st(0,N);wi(P+90,1);clear(P+40);clear(M+22);clear(N+24,True);clear(N+28,True)
c.label('return08_done');c.emit('4e75')
c.label('close08');c.emit(source[0x21d8:0x21e2].hex());c.emit('48e7fffe');call('panel_return08');call('cursor');c.emit('4cdf7fff4e75');hook(0x21d8,'close08',10)
c.label('guard08');tst(P+90);branch('6700','guard08_done');ld(0,P+56);imm(0x0240,0,7);branch('6600','guard08_mask');clear(P+90)
c.label('guard08_mask');clear(P+56);clear(P+58)
c.label('guard08_done');c.emit('4e75')
# East wall cabin, with native service cell immediately inside the door.
def cell08(x,z,v):r[old['map']+(49-z)*80+x]=v
for z in range(15,20):
 for x in range(29,34):cell08(x,z,0x81 if x in [29,33] or z in [15,19] else 0)
cell08(29,17,0xa4);cell08(30,17,0x0c);cell08(32,17,0xa3)
# Test cabin keeps its map when the native travel animation reaches a selected floor.
c.label('lift_arrive08');tst(P+108);branch('6700','lift_native35');st(0,0xffff260a);c.abs('2079',0xffff227e);c.emit('317c00b30004');bi(0xffff2700,255);bi(0xffff218c,0);bi(0xffff2715,0);c.emit('7001');c.call(0x150b4);c.emit('4e75');hook(0x8e1c,'lift_arrive08')
c.label('fuse_enter08');c.emit('48e7fffe');call('panel_enter08');c.emit('4cdf7fff');c.emit(source[0x7a00:0x7a06].hex());c.jump(0x7a06);hook(0x7a00,'fuse_enter08')
# Native item/menu callbacks can rewrite the hardware sprite after input handling.
# Reassert the mouse hotspot just before the native sprite list is assembled.
c.label('sprite_publish08');c.emit('48e7fffe');tst(P+116);branch('6700','sprite08_native');c.emit('0c795348');c.address(P+6);branch('6600','sprite08_native');tst(P);branch('6700','sprite08_native');tst(N);branch('6700','sprite08_native');call('cursor')
c.label('sprite08_native');c.emit('4cdf7fff');c.emit(source[0x30b8:0x30be].hex());c.jump(0x30be);hook(0x30b8,'sprite_publish08')
