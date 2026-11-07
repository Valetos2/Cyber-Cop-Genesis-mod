exec((OUT/'make_front_frames.py').read_text())
# The native focus arrow stays separate from the free pointer. A private two-
# sprite staging buffer avoids overwriting character stats next to $29C8.
FRONT=0xffff0802;SPRITES=0xffff0810;M=0xffff0180
c.label('character_enter36');wi(FRONT,1);wi(0xffff0828,0);wi(0xffff0830,0);c.emit(src[0xf61c:0xf622].hex());c.jump(0xf622);patch(0xf61c,'character_enter36')
c.label('equipment_enter36');wi(FRONT,2);wi(0xffff0828,0);wi(0xffff0830,0);c.call(0x1612);c.jump(0xfb1a);patch(0xfb14,'equipment_enter36')
c.label('equipment_leave36');c.call(0xfb14);wi(FRONT,0);c.call(0x5342);c.jump(0xf75c);patch(0xf752,'equipment_leave36',10)
for site,ret,name in [(0xf6a4,0xf6aa,'character_input36'),(0xfbd2,0xfbd8,'equipment_input36')]:
 c.label(name);c.call(0x53a8);c.ref('4eb9','front_mouse36');c.jump(ret);patch(site,name)

c.label('front_mouse36');c.emit('48e77ffe3c00');c.abs('4a79',P);c.branch('6700','front_mouse36_done');c.abs('4a39',M+18);c.branch('6700','front_mouse36_done')
c.emit('40e7007c0700');c.call(S['snapshot05']);c.emit('46df')
for axis,source,dest,limit,neg in [('x',P+48,N+4,319,False),('y',P+52,N+6,223,True)]:
 c.abs('2039',source);c.call(S['scale_'+axis])
 if neg:c.emit('4440')
 c.abs('d079',dest);c.branch('6a00','front_'+axis+'_positive');c.emit('7000')
 c.label('front_'+axis+'_positive');c.emit('0c40'+f'{limit:04x}');c.branch('6f00','front_'+axis+'_clamped');c.emit('303c'+f'{limit:04x}')
 c.label('front_'+axis+'_clamped');c.abs('33c0',dest)
c.ref('4eb9','front_hold36');c.abs('3839',P+58);c.emit('08040003');c.branch('6700','front_mouse36_click');c.emit('0c790002');c.long(FRONT);c.branch('6600','front_mouse36_accept_character');c.emit('08860007');c.branch('6000','front_mouse36_store')
c.label('front_mouse36_accept_character');wi(0xffff29ce,0x108);c.emit('08860004');c.branch('6000','front_mouse36_store')
c.label('front_mouse36_click');c.emit('02440001');c.branch('6700','front_mouse36_done')
# Inclusive top/left and exclusive bottom/right, in native320x224 coordinates.
c.abs('3039',N+6);c.emit('0c400057');c.branch('6d00','front_mouse36_done');c.emit('0c400064');c.branch('6c00','front_mouse36_done')
c.abs('3039',N+4);c.emit('0c40007f');c.branch('6d00','front_mouse36_done');c.emit('0c4000c1');c.branch('6c00','front_mouse36_done')
c.emit('0c790002');c.long(FRONT);c.branch('6700','front_mouse36_equipment')
c.emit('08040000');c.branch('6700','front_mouse36_done');c.emit('0c4000a0');c.branch('6c00','front_mouse36_pass');wi(0xffff29ce,0x108);wi(0xffff0828,1);c.branch('6000','front_mouse36_press')
c.label('front_mouse36_pass');wi(0xffff29ce,0x128);wi(0xffff0828,2);c.branch('6000','front_mouse36_press')
c.label('front_mouse36_equipment');c.emit('74030c400096');c.branch('6d00','front_visual_ready36');c.emit('74040c4000aa');c.branch('6d00','front_visual_ready36');c.emit('7405');c.label('front_visual_ready36');c.emit('7200');c.emit('0c400096');c.branch('6d00','front_mouse36_select');c.emit('72010c4000aa');c.branch('6d00','front_mouse36_select')
c.label('front_mouse36_back');c.emit('7202')
c.label('front_mouse36_select');c.abs('33c1',0xffff4416);c.abs('33c2',0xffff0828);c.emit('3001c0fc001406400104');c.abs('33c0',0xffff29ce)
c.label('front_mouse36_press');c.abs('33c4',0xffff082a);c.emit('08860004');c.ref('4eb9','front_sprites36');c.call(0x2930)
c.label('front_mouse36_store');c.abs('33c6',0xffff0004)
c.label('front_mouse36_done');c.emit('30064cdf7ffe4e75')

c.label('front_sprites36');c.abs('4a79',FRONT);c.branch('6700','front_sprites36_native');c.abs('4a79',P);c.branch('6700','front_sprites36_native');c.abs('4a39',M+18);c.branch('6700','front_sprites36_native');c.emit('48e7fffe')
c.abs('4a79',0xffff0830);c.branch('6600','front_frames_ready36');wi(0xffff0016,640);c.abs('23fc',front_frames);c.long(0xffff0018);wi(0xffff001c,0xd000);c.call(0x249c);wi(0xffff0830,1);c.label('front_frames_ready36');c.abs('41f9',0xffff29c8);c.abs('43f9',SPRITES);c.emit('42994299');bi(SPRITES+3,1)
c.abs('3039',N+6);c.emit('0640007c');c.abs('33c0',SPRITES+8);wi(SPRITES+10,0x0900)
c.abs('3039',0xffff29c4);c.emit('06400014');c.abs('33c0',SPRITES+12)
c.abs('3039',N+4);c.emit('06400074');c.abs('33c0',SPRITES+14)
c.abs('3039',0xffff0828);c.branch('6700','front_no_frame36');bi(SPRITES+11,2);wi(SPRITES+16,216);wi(SPRITES+18,0x0d00);c.emit('5340e74806400680');c.abs('33c0',SPRITES+20);c.abs('3039',0xffff0828);c.emit('5340d040');c.ref('43f9','front_press_x36');c.emit('30310000');c.abs('33c0',SPRITES+22);c.label('front_no_frame36');wi(0xffff0016,12);c.abs('23fc',SPRITES);c.long(0xffff0018);wi(0xffff001c,0xdc00);c.call(0x249c);c.emit('4cdf7fff4e75')
c.label('front_sprites36_native');c.emit(src[0xf7b2:0xf7ba].hex());c.jump(0xf7ba);patch(0xf7b2,'front_sprites36',8)

# Cancel the held highlight on release or on the first exit from its button.
c.label('front_hold36');c.abs('3039',0xffff0828);c.branch('6700','front_hold_done36');c.abs('3239',P+56);c.abs('c279',0xffff082a);c.branch('6700','front_hold_clear36');c.abs('3239',N+6);c.emit('0c410057');c.branch('6d00','front_hold_clear36');c.emit('0c410064');c.branch('6c00','front_hold_clear36');c.emit('5340e548');c.ref('43f9','front_press_bounds36');c.abs('3239',N+4);c.emit('b2710000');c.branch('6d00','front_hold_clear36');c.emit('b2710002');c.branch('6c00','front_hold_clear36');c.branch('6000','front_hold_done36')
c.label('front_hold_clear36');wi(0xffff0828,0)
c.label('front_hold_done36');c.emit('4e75')
c.label('front_press_x36')
for x in [128,160,128,150,170]:c.emit(f'{x+128:04x}')
c.label('front_press_bounds36')
for lo,hi in [(127,160),(160,193),(127,150),(150,170),(170,193)]:c.emit(f'{lo:04x}{hi:04x}')
