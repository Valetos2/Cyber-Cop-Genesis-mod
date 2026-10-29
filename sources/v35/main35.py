MAIN=(ROOT/'v34/Cyber-Cop_v34.bin').read_bytes()
VL=json.loads((ROOT/'v34/symbols.json').read_text())
# Restore the real title flow and native hostile constructor from the lab base.
r[0x386:0x38c]=MAIN[0x386:0x38c]
r[0x3fb2:0x3fb4]=MAIN[0x3fb2:0x3fb4]
# Every hard or soft reset runs this path before interrupts are enabled.
c.label('reset35');c.abs('41f9',0xffff0100);c.emit('303c01bf429851c8fffc');wi(M,0x4d53);wi(P,1);wi(N+2,4);wi(N+4,160);wi(N+6,72);wi(N+32,70);wi(P+6,0x5348);c.emit(MAIN[0x332:0x338].hex());c.jump(0x338);hook(0x332,'reset35')
# Initialize only transient mouse state at gameplay entry; retain option choices.
c.label('world35');call('init03_all');clear(P+2);clear(P+24);clear(P+32);wi(P+116,1);clear(N);clear(N+8);clear(N+10);wi(N+32,70);clear(N+16,True);clear(N+20,True);clear(N+24,True);clear(N+28,True);clear(M+4,True);clear(M+8,True);clear(M+16);clear(M+22);clear(P+84);clear(P+90);tst(P+108);branch('6700','world35_native');call('lab_spawn35');call('lab_inventory35')
c.label('world35_native');c.emit(MAIN[0x2074:0x207a].hex());c.jump(0x207a);hook(0x2074,'world35')
c.label('lab_spawn35')
for addr,val in [(0xffff441a,14*256+128),(0xffff441e,12*256+128),(0xffff443a,0),(0xffff260c,0),(0xffff2622,14*256+128),(0xffff2626,12*256+128)]:wi(addr,val)
c.emit('33f9');c.address(0xffff441c);c.address(0xffff2624);c.emit('4e75')
c.label('lab_inventory35')
for i in range(52):bi(0xffff2f50+i,255)
for i,item in enumerate([0,6,7,11,12,14,28,25,26,27,29,13,17,20,20,9]):bi(0xffff2f50+i,item)
bi(0xffff2f70,0x26);wi(0xffff2740,0);wi(0xffff2fea,0x0451);c.call(0x6e98);c.emit('4e75')
# Separate world namespace $0100; legacy index0 below is only a render/profile adapter.
c.label('floor35');tst(P+108);branch('6700','floor35_main');wi(0xffff2606,0);c.call(0x4882);c.abs('41f9',old['map']);c.abs('43f9',0xffff305a);c.emit('303c03e722d851c8fffc');c.call(0x4966);c.call(0x685e);call('lab_spawn35');c.emit('4e75')
c.label('floor35_main');c.call(0x4882);c.call(0x685e);c.emit('4e75')
r[0x4838:0x4840]=bytes.fromhex('4eb9')+c.labels['floor35'].to_bytes(4,'big')+bytes.fromhex('4e71')
c.label('construct35');tst(P+108);branch('6600','construct35_done');c.emit(MAIN[0x3fb2:0x3fb8].hex());c.jump(0x3fb8);c.label('construct35_done');c.emit('4e75');hook(0x3fb2,'construct35')
# SRAM guard before any write or floor-history serialization; password generation is skipped.
for addr,tag,n in [(VL['save21'],'save',4),(VL['sram17_save'],'save_password',4),(0x8f74,'password',8)]:
 # save prologues are MOVEM + MOVE/byte; determine full initial instruction span.
 if tag=='save':n=10
 if tag=='save_password':n=12
 c.label('guard35_'+tag);tst(P+108);branch('6700','guard35_'+tag+'_native');c.emit('4e75');c.label('guard35_'+tag+'_native');
 if tag=='password':c.emit('363ce88e');c.abs('41f9',0x9366)
 else:c.emit(MAIN[addr:addr+n].hex())
 c.jump(addr+n);hook(addr,'guard35_'+tag,n)
# All external password entry/resume routes explicitly select the main universe.
for addr,tag,n in [(VL['resume17'],'resume',6),(0xe94,'decode',6)]:
 c.label('main35_'+tag);clear(P+108);c.emit(MAIN[addr:addr+n].hex());c.jump(addr+n);hook(addr,'main35_'+tag,n)
# Lab-only substitutions must not alter the main story, fuse timers, or elevator travel.
c.label('airlock_native35');c.emit(MAIN[0x784c:0x7852].hex());c.jump(0x7852)
c.label('fuse_native35');c.emit(MAIN[0x7ab2:0x7ab8].hex());c.emit('4e75')
c.label('lift_native35');c.emit(MAIN[0x8e1c:0x8e22].hex());c.jump(0x8e22)
c.label('airlock_code35');tst(P+108);branch('6700','airlock_code35_main');wi(0xffff243a,0x0451);c.jump(0x7798);c.label('airlock_code35_main');c.emit(MAIN[0x7790:0x7798].hex());c.jump(0x7798);hook(0x7790,'airlock_code35',8)
# Movement stays live under mouse inventory clicks; native joystick-only cruise is untouched.
c.label('movement35');tst(P);branch('6700','movement35_native');tst(0xffff270a,True);branch('6700','movement35_native');c.emit('0cb900002106');c.address(0xffff26b8);branch('6600','movement35_stop');c.emit('48e7fffe');call('force_strafe');c.call(0xa0ea);c.call(0xabe0);c.emit('4cdf7fff4e75')
c.label('movement35_stop');clear(0xffff443c);c.emit('4e75');c.label('movement35_native');c.emit(MAIN[0xabc0:0xabc6].hex());c.jump(0xabc6);hook(0xabc0,'movement35')
# Keep the upper brightness-arrow visible only while its opposite half is pressed.
c.label('scan_contrast35');cmp(3,3);branch('6600','scan_contrast35_done');c.emit('48e7fffe')
# Upper inset rectangle must stay distinct from the darkened rocker surround.
c.emit('3e3c0023');c.label('scan_inset35c_row');c.emit('3c3c00a2')
c.label('scan_inset35c_pixel');c.emit('30063207');call('pixel_address');c.emit('7204');imm(0x0240,0,1);call('pixel_write')
c.emit('5246');cmp(6,169);branch('6d00','scan_inset35c_pixel');c.emit('5247');cmp(7,48);branch('6d00','scan_inset35c_row')
for x,y in [(167,y) for y in range(39,48)]+[(166,y) for y in range(43,48)]+[(165,47)]:
 c.emit('303c'+f'{x:04x}'+'323c'+f'{y:04x}');call('pixel_address');c.emit('7203');imm(0x0240,0,1);call('pixel_write')
c.emit('4cdf7fff');c.label('scan_contrast35_done');c.emit('4e75')
# Fourth mouse button is Start in native title/menu input, without extra port polls.
c.label('pad_front35');call('pad_front35_native');tst(P);branch('6700','pad_front35_done');tst(M+18,True);branch('6700','pad_front35_done');c.emit('08390003');c.address(M+13);branch('6700','pad_front35_done');imm(0x0240,0,0xff7f);c.abs('08b90007',0xffff0005)
c.label('pad_front35_done');c.emit('4e75');c.label('pad_front35_native');c.emit(MAIN[0x53a8:0x53b0].hex());c.jump(0x53b0);hook(0x53a8,'pad_front35',8)
# Frontend text uses the existing font and plane; all strings are ROM-owned.
textpos=0x1d6000
assert set(source[0x1d6000:0x1d8000])=={255}
def draw35(text,addr):
 global textpos
 pos=textpos;b=text.encode('ascii');r[pos:pos+len(b)]=b;textpos+=len(b)+(len(b)%2)
 c.abs('4bf9',pos);c.emit('363c'+f'{addr:04x}'+'3e3c'+f'{len(b)-1:04x}'+'3c3c2000');c.call(0xffbe)
# New-game submenu: two choices, hidden third after four Down edges at the bottom.
c.label('newmenu35');clear(P+108);clear(P+110);clear(P+112);clear(0xffff286a);bi(0xffff2702,255);c.call(0x1646);c.emit('323c1000343ce000');c.call(0x31b0);c.abs('4df9',0xc00000);c.emit('303c00a8');c.call(0x1602)
draw35('select default character',0xe20e);draw35('create new character',0xe30e);clear(0xffff4416);wi(0xffff29ce,376);bi(0xffff0015,2);call('newmenu35_cursor');wi(0xffff286a,0xeee);bi(0xffff2702,255);c.call(0x1646)
c.label('newmenu35_loop');c.call(0x2930);c.call(0x53a8);ld(4,0xffff0006);c.emit('32004641c841');branch('6700','newmenu35_loop');ld(1,0xffff4416);cmp(4,2);branch('6700','newmenu35_down');clear(P+112);c.emit('08040007');branch('6600','newmenu35_accept');c.emit('08040000');branch('6700','newmenu35_action');c.emit('4a41');branch('6700','newmenu35_loop');c.emit('5341');branch('6000','newmenu35_changed')
c.label('newmenu35_down');tst(P+110);branch('6600','newmenu35_unlocked');cmp(1,1);branch('6d00','newmenu35_inc');c.emit('5279');c.address(P+112);ld(0,P+112);cmp(0,4);branch('6d00','newmenu35_loop');wi(P+110,1);draw35('load test map 01',0xe40e);c.emit('7202');branch('6000','newmenu35_changed')
c.label('newmenu35_unlocked');cmp(1,2);branch('6c00','newmenu35_loop');c.label('newmenu35_inc');c.emit('5241');c.label('newmenu35_changed');st(1,0xffff4416);call('newmenu35_cursor');branch('6000','newmenu35_loop')
c.label('newmenu35_action');c.emit('08040004');branch('6700','newmenu35_loop');c.label('newmenu35_accept');clear(P+108);cmp(1,2);branch('6600','newmenu35_main');wi(P+108,0x100);c.jump(0xa56)
c.label('newmenu35_main');c.emit('4a41');branch('6700','newmenu35_default');c.jump(0xa2e);c.label('newmenu35_default');c.jump(0xa56);c.label('newmenu35_back');c.jump(0x6dc)
c.label('newmenu35_cursor');ld(0,0xffff4416);c.emit('e948064000f8');st(0,0xffff29c8);c.call(0xf7b2);c.emit('4e75');hook(VL['start16_menu'],'newmenu35')
# Menu version label (same length, native font).
for off in range(len(r)-3):
 if r[off:off+3]==b'v34':r[off:off+3]=b'v35'
# Options rows expand only while a mouse is present; sensitivity is retained on Off.
c.label('options35');c.call(VL['settings_init']);clear(0xffff286a);bi(0xffff2702,255);c.call(0x1646);bi(0xffff2712,0);c.emit('323c1000343ce000');c.call(0x31b0);c.abs('4df9',0xc00000);c.emit('7000');c.call(0x1602);clear(0xffff4416);bi(0xffff0015,2);wi(0xffff29ce,360);call('options35_draw');wi(0xffff286a,0xeee);bi(0xffff2702,255);c.call(0x1646)
c.label('options35_loop');c.call(0x2930);c.call(0x53a8);ld(4,0xffff0006);c.emit('32004641c841');branch('6700','options35_loop');call('options35_max');ld(1,0xffff4416);c.emit('08040007');branch('6600','options35_exit');c.emit('08040000');branch('6700','options35_down');c.emit('5341');branch('6a00','options35_store');movw(1,2);branch('6000','options35_store')
c.label('options35_down');c.emit('08040001');branch('6700','options35_action');c.emit('5241b242');branch('6f00','options35_store');c.emit('7200');c.label('options35_store');st(1,0xffff4416);branch('6000','options35_redraw')
c.label('options35_action');c.emit('b242');branch('6600','options35_notexit');c.emit('08040004');branch('6600','options35_exit');branch('6000','options35_loop');c.label('options35_notexit')
for idx,addr in [(0,0xffff2710),(1,0xffff2711),(4,0xffff0108)]:
 cmp(1,idx);branch('6600','options35_next'+str(idx));imm(0x0240,4,0x7c);branch('6700','options35_loop');c.emit('0a3900ff');c.address(addr)
 if idx==0:c.call(VL['music21_toggle'])
 branch('6000','options35_redraw');c.label('options35_next'+str(idx))
cmp(1,2);branch('6600','options35_not_sound');c.emit('08040002');branch('6700','options35_soundright');ld(0,0xffff010a);c.emit('5340');branch('6a00','options35_soundstore');c.emit('7017');branch('6000','options35_soundstore');c.label('options35_soundright');c.emit('08040003');branch('6700','options35_soundplay');ld(0,0xffff010a);c.emit('5240');cmp(0,24);branch('6d00','options35_soundstore');c.emit('7000');c.label('options35_soundstore');st(0,0xffff010a);c.call(VL['sound_stop14']);branch('6000','options35_redraw');c.label('options35_soundplay');c.emit('08040004');branch('6700','options35_loop');c.call(VL['sound_play14']);branch('6000','options35_redraw');c.label('options35_not_sound')
cmp(1,3);branch('6600','options35_not_dither');c.call(VL['dither19_change']);branch('6000','options35_redraw');c.label('options35_not_dither');cmp(1,5);branch('6600','options35_sensitivity');imm(0x0240,4,0x7c);branch('6700','options35_loop');c.emit('0a790001');c.address(P);branch('6000','options35_redraw')
c.label('options35_sensitivity');ld(0,N+2);c.emit('08040002');branch('6700','options35_sensright');c.emit('5340');branch('6000','options35_senslimit');c.label('options35_sensright');c.emit('08040003');branch('6700','options35_loop');c.emit('5240');c.label('options35_senslimit');clamp(0,0,8,'frontsens35');st(0,N+2)
c.label('options35_redraw');call('options35_draw');branch('6000','options35_loop')
c.label('options35_exit');st(2,0xffff4416);call('options35_draw');wi(0xffff7d46,256);bi(0xffff7d3c,0);bi(0xffff0015,2);c.jump(0x6dc)
c.label('options35_max');c.emit('7405');tst(M+18,True);branch('6700','options35_maxdone');wi(P+38,1);c.emit('7406');tst(P);branch('6700','options35_maxdone');c.emit('7407');c.label('options35_maxdone');c.emit('4e75')
c.label('options35_draw');draw35('options         ',0xe0a0)
for idx,name in enumerate(['music','sound fx','sound test','wall dithering','wall stripe','','','']):draw35(name.ljust(26),0xe20e+idx*0x100)
for idx,addr in [(0,0xffff2710),(1,0xffff2711),(4,0xffff0108)]:
 tst(addr,True);branch('6600','options35_off'+str(idx));draw35('on ',0xe234+idx*0x100);branch('6000','options35_endflag'+str(idx));c.label('options35_off'+str(idx));draw35('off',0xe234+idx*0x100);c.label('options35_endflag'+str(idx))
# Preserve the original native sound-test number and dither names.
ld(0,0xffff010a);c.emit('80fc000a06400030');c.abs('13c0',0xffff010c);c.emit('484006400030');c.abs('13c0',0xffff010d);c.abs('4bf9',0xffff010c);c.emit('363ce4347e013c3c2000');c.call(0xffbe)
c.call(VL['dither19_index']);c.emit('3200d040d041');c.abs('4bf9',VL['dither19_names']);c.emit('dac0363ce5347e023c3c2000');c.call(0xffbe)
call('options35_max');cmp(2,5);branch('6700','options35_exit5');draw35('mouse',0xe70e);tst(P);branch('6700','options35_mouseoff');draw35('on ',0xe734);draw35('sensitivity',0xe80e);call('front_slider35');draw35('exit',0xe90e);branch('6000','options35_arrow');c.label('options35_mouseoff');draw35('off',0xe734);draw35('exit',0xe80e);branch('6000','options35_arrow');c.label('options35_exit5');draw35('exit',0xe70e)
c.label('options35_arrow');call('options35_max');ld(0,0xffff4416);c.emit('b042');branch('6f00','options35_arrowvalid');movw(0,2);st(0,0xffff4416);c.label('options35_arrowvalid');c.emit('e948064000a0');st(0,0xffff29c8);c.call(0xf7b2);c.emit('4e75');hook(VL['options14'],'options35')
# VRAM D400..D51F is outside plane B names C000..CFFF, HScroll D800 and SAT DC00.
# A 9-tick graphical slider: nine 8x8 tiles, menu palette1, independent of HUD tiles.
for value in range(9):
 data=bytearray(9*32)
 def px(x,y,v):
  o=x//8*32+y*4+x%8//2;sh=0 if x%2 else 4;data[o]=(data[o]&~(15<<sh))|(v<<sh)
 for x in range(1,71):px(x,4,15)
 for i in range(9):
  for y in range(2,7):px(3+i*8,y,15)
 for x in range(2+value*8,5+value*8):
  for y in range(1,8):px(x,y,15)
 r[0x1d7000+value*288:0x1d7000+(value+1)*288]=data
c.label('front_slider35');c.emit('40e7007c070048e7fffe');ld(0,N+2);c.emit('c0fc0120');c.abs('41f9',0x1d7000);c.emit('d0c0');c.emit('33fc8f02');c.address(0xc00004);c.emit('23fc54000003');c.address(0xc00004);c.emit('7e47');c.label('front_slider35_upload');c.abs('23d8',0xc00000);c.emit('51cf');c.fix.append((len(c.b),'front_slider35_upload',2));c.emit('0000');c.emit('23fc68300003');c.address(0xc00004);c.emit('303c26a07e08');c.label('front_slider35_names');c.abs('33c0',0xc00000);c.emit('524051cf');c.fix.append((len(c.b),'front_slider35_names',2));c.emit('00004cdf7fff46df4e75')

# Never overlay gameplay mouse sprites/HUD tiles on credits or frontend screens.
for addr,tag in [(VL['main18_enter'],'title'),(VL['ending29'],'ending')]:
 c.label('leave35_'+tag);clear(P+116);clear(N);clear(N+20,True);clear(P+34);clear(P+24);clear(P+2);clear(P+84);c.emit(MAIN[addr:addr+6].hex());c.jump(addr+6);hook(addr,'leave35_'+tag)

# Mouse serial I/O uses only port2, never Z80 RAM. Do not acquire/release BUSREQ:
# an IRQ can arrive while native sound code is waiting for its own pending grant.
# Reading BUSACK cannot distinguish that pending request from an unrequested bus.
# Releasing it in the IRQ leaves native sound waiting forever at $156E4.
mouse_poll=0x18013c;mouse_ready=0x180176
r[mouse_poll+12:mouse_poll+20]=bytes.fromhex('7c004ef9')+mouse_ready.to_bytes(4,'big')


# While the native elevator indicator is B1, its destination must be immutable.
# snapshot05 already drained VBlank deltas/edges. Suppress held keys until release.
c.label('lift_busy35c');c.emit('7000');tst(P);branch('6700','lift_busy35c_done')
c.emit('0cb900008d42');c.address(0xffff26b8);branch('6600','lift_busy35c_done')
c.emit('0c7900b1');c.address(0xffff7dca);branch('6600','lift_busy35c_done')
ld(0,M+22);c.abs('8179',0xffff0004);c.emit('4640');c.abs('c179',0xffff0006)
clear(M+22);clear(N+14);wi(P+90,1);c.emit('7001')
c.label('lift_busy35c_done');c.emit('4e75')
# Keep native airborne maintenance above gesture26_pad. Gate only A gestures.
c.label('gesture_free35c');tst(P);branch('6700','gesture_native35c');tst(N);branch('6700','gesture_native35c')
bi(0xffff013e,0);bi(0xffff013f,0);c.emit('4e75')
c.label('gesture_native35c');c.emit(MAIN[VL['gesture26_pad']:VL['gesture26_pad']+6].hex());c.jump(VL['gesture26_pad']+6)
hook(VL['gesture26_pad'],'gesture_free35c')
