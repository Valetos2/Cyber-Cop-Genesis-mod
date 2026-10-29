V={'id18_selected': 1015192, 'sleep31_arrow': 1012172, 'music21_toggle': 1016342, 'dither19_index': 1015312, 'dither19_store': 1015378, 'sleep16': 1011570}
# Additional state is independent from both SRAM and v34 options.
c.label('init03');c.emit('4e75')
# Static native nodes have cursor anchor BELOW the button, not its upper corner.
entries=[]
for root,nodes,kind in [
 (0x5b8a,list(range(0x5c3e,0x5d1a,20)),'keypad'),
 (0x5d1c,list(range(0x5dd0,0x5ec0,20)),'bomb'),
 (0x5ec2,list(range(0x5f76,0x6066,20)),'airlock'),
 (0x6068,list(range(0x611c,0x620c,20))+[0x6210,0x6224],'fuse'),
 (0x56d2,list(range(0x5786,0x589e,20)),'inside'),
 (0x58a0,[0x5954,0x5968],'lift'),
 (0x5a98,[0x5b4c,0x5b60,0x5b74],'terminal'),
 (0x597e,[0x5a32,0x5a46,0x5a5a,0x5a6e,0x5a82],'scanman')]:
 for node in nodes:
  x=source[node]*8;y=source[node+1]*8;ident=int.from_bytes(source[node+2:node+4],'big');left=x;top=y-16;right=x+16;bottom=y;style=1
  if kind in ['keypad','airlock','bomb'] and ident==83:left=x-16
  if kind=='lift':style=0
  if kind=='inside':style=4
  if kind=='terminal':left=16;right=160;top=y-8;bottom=y;style=0
  if kind=='fuse':left=x+1;right=x+14;top=y-14;bottom=y-2
  if kind=='scanman':
   x1,x2,y1,y2,style={0x5a32:(165,175,114,125,1),0x5a46:(128,159,109,120,1),0x5a5a:(96,127,109,120,1),0x5a6e:(224,235,56,72,3),0x5a82:(224,235,40,56,2)}[node]
  else:
   shift=0 if kind=='fuse' or kind=='terminal' else 1
   x1,x2,y1,y2=left+64+shift,right+64+shift,top+8+shift,bottom+8+shift
  entries.append((root,node,x1,x2,y1,y2,style))
# Explicit bounds avoid malformed/padded records near the end of the fuse-box list.
table=0x18e000
for i,(root,node,x1,x2,y1,y2,style) in enumerate(entries):
 data=root.to_bytes(4,'big')+node.to_bytes(4,'big')+b''.join(v.to_bytes(2,'big') for v in [x1,x2,y1,y2,style]);r[table+i*18:table+(i+1)*18]=data
# Click rectangles include exactly the visible reversed perimeter. Keep original
# geometry records for pixel overlays/glyph origins; only hit-testing uses this map.
click_table=0x1d8000
assert set(source[click_table:click_table+len(entries)*18])=={255}
for i,(root,node,x1,x2,y1,y2,style) in enumerate(entries):
 if style==1 and root in [0x5b8a,0x5ec2,0x5d1c,0x6068]:
  x2-=1;y2-=1
  if root==0x6068:x1+=1;y1+=1
 data=root.to_bytes(4,'big')+node.to_bytes(4,'big')+b''.join(v.to_bytes(2,'big') for v in [x1,x2,y1,y2,style])
 r[click_table+i*18:click_table+(i+1)*18]=data
c.label('hit_panel03');c.emit('0cb900002106');c.address(0xffff26b8);branch('6700','panel05_none');c.emit('0cb900007070');c.address(0xffff26b8);branch('6700','panel05_none');c.abs('41f9',click_table);c.emit('3e3c'+f'{len(entries)-1:04x}');ld(2,N+40,True)
c.label('panel03_loop');c.emit('b490');branch('6600','panel03_next');c.emit('b0680008');branch('6d00','panel03_next');c.emit('b068000a');branch('6c00','panel03_next');c.emit('b268000c');branch('6d00','panel03_next');c.emit('b268000e');branch('6c00','panel03_next');c.emit('23e80004');c.address(N+16);c.emit('d1fc');c.address((table-click_table)&0xffffffff);c.emit('23c8');c.address(P+8);c.emit('4e75')
c.label('panel03_next');c.emit('41e8001251cf');c.fix.append((len(c.b),'panel03_loop',2));c.emit('00004e75')
c.label('panel05_none');c.emit('4e75')
# Capture button origin once; moving while held never invokes a second action.
c.label('save_press');ld(0,P+8,True);st(0,P+12,True);c.emit('4e75')
# Keep native selection in the active table: its Up links lead to the panel.
c.label('select03');c.call(V['id18_selected']);c.emit('48e7c080');c.abs('2079',N+40);c.emit('2008');branch('6700','select03_done');ld(0,0xffff26b8,True);c.emit('0c8000009916');branch('6600','select03_done');c.emit('41e8008c');c.abs('23c8',0xffff202a)
c.label('select03_done');c.emit('4cdf01034e75');hook(0x8f66,'select03',8)
# Mouse cursor must never be moved to a joystick selection by automatic item focus.
c.label('no_snap');tst(P+116);branch('6700','snap_native');tst(P);branch('6700','snap_native');c.emit('48e7fffe');call('cursor');c.emit('4cdf7fff4e75');c.label('snap_native');c.emit(source[0x540a:0x5410].hex());c.jump(0x5410);hook(0x540a,'no_snap')
# Clicking the sleep icon while asleep wakes via the normal exit.
c.label('press03');c.emit('0cb900007070');c.address(0xffff26b8);branch('6600','press03_normal');c.abs('2079',N+16);c.emit('4a680002');branch('6600','press03_normal');c.abs('23c8',N+20);call('feedback07');c.jump(0x709a)
c.label('press03_normal');jmp('press_ui')
# Redirect calls rather than overwriting the existing entry.
for p,label,n in list(c.fix):
 if label=='press_ui' and p<c.labels['press03']-BASE:c.fix.remove((p,label,n));c.fix.append((p,'press03',n))
# New sixth row on the second sleep page and optional joystick marker.
c.label('sleep_arrow03');c.emit('7000');c.abs('1039',P+44);cmp(0,4);branch('6d00','arrow05_main');cmp(0,9);branch('6d00','sleep_arrow03_check');c.label('arrow05_main');tst(P+38);branch('6700','sleep_arrow03_check');call('mouse_text');tst(P);branch('6700','sleep_arrow03_check');call('slider_row04')
c.label('sleep_arrow03_check');tst(P);branch('6600','arrow03_done');c.emit('7000');c.abs('1039',P+44);cmp(0,9);branch('6d00','arrow05_regular');c.emit('303c0100');branch('6000','arrow05_draw');c.label('arrow05_regular');cmp(0,4);branch('6500','arrow05_options');c.emit('5940ed48064001e0');branch('6000','arrow05_draw');c.label('arrow05_options');c.emit('ed48');c.label('arrow05_draw');c.jump(0xf71ea);c.label('arrow03_done');c.emit('4e75');hook(V['sleep31_arrow'],'sleep_arrow03',8)
# Small sparse ROM pixel patches, in the existing sleep framebuffer/palette.
c.label('mouse_text');c.abs('41f9',0x193000);tst(P);branch('6700','mouse_text_copy');c.emit('41e80a00');c.label('mouse_text_copy');c.abs('43f9',0xffff8934);c.emit('3e3c027f');c.label('mouse_text_loop');c.emit('30183218e0491381000051cf');c.fix.append((len(c.b),'mouse_text_loop',2));c.emit('00004e75')
# Mouse sleep actions are processed on edges only, before the native sleep frame.
c.label('sleep_click');c.emit('0cb900007070');c.address(0xffff26b8);branch('6600','sleep_click_done');call('in_world');c.emit('4a40');branch('6700','sleep_click_done');clear(N+16,True);ld(4,N+14);imm(0x0240,4,3);branch('6700','sleep_click_done');tst(0xffff0118,True);branch('6600','sleep_menu_click');bi(0xffff0118,1);bi(0xffff0119,0);branch('6000','sleep_click_changed')
c.label('sleep_menu_click');c.emit('7000');c.abs('1039',0xffff0119);cmp(0,4);branch('6d00','sleep_page0');cmp(0,9);branch('6c00','sleep_page0');ld(1,N+6);imm(0x0440,1,32);branch('6b00','sleep_next_page');cmp(1,72);branch('6c00','sleep_next_page');movw(2,1);imm(0x0240,2,15);cmp(2,8);branch('6c00','sleep_click_done');c.emit('e849');imm(0x0640,1,4);branch('6000','sleep_row')
c.label('sleep_page0');ld(1,N+6);cmp(1,120);branch('6c00','sleep_slider04');imm(0x0440,1,40);branch('6b00','sleep_next_page');cmp(1,72);branch('6c00','sleep_next_page');movw(2,1);imm(0x0240,2,15);cmp(2,8);branch('6c00','sleep_click_done');c.emit('e849');cmp(1,4);branch('6600','sleep_row');tst(P+38);branch('6700','sleep_next_page');c.emit('7209');
c.label('sleep_row');ld(2,N+4);cmp(2,72);branch('6d00','sleep_next_page');cmp(2,232);branch('6c00','sleep_next_page');c.abs('13c1',0xffff0119);cmp(1,9);branch('6700','sleep_toggle_mouse');cmp(1,8);branch('6700','sleep_access');cmp(1,2);branch('6700','sleep_dither')
# Boolean rows, including main-theme-only music behavior.
for idx,addr in [(0,0xffff2710),(1,0xffff2711),(3,0xffff0108),(4,0xffff0104),(5,0xffff0105),(6,0xffff0106),(7,0xffff012c)]:
 cmp(1,idx);branch('6600','sleep_bool_next'+str(idx));c.emit('4639');c.address(addr)
 if idx==0:c.call(V['music21_toggle'])
 branch('6000','sleep_click_changed');c.label('sleep_bool_next'+str(idx))
branch('6000','sleep_click_changed')
c.label('sleep_toggle_mouse');clear(P);call('mouse_toggle05');branch('6000','sleep_click_changed')
c.label('sleep_access');ld(0,0xffff26bc);c.emit('ea48');call('cycle_value');clamp(0,0,7,'access06');c.emit('eb48');st(0,0xffff26bc);branch('6000','sleep_click_changed')
c.label('sleep_dither');c.call(V['dither19_index']);call('cycle_value');clamp(0,0,4,'dither06');c.call(V['dither19_store']);branch('6000','sleep_click_changed')
c.label('sleep_slider04');tst(P);branch('6700','sleep_next_page');ld(4,N+14);c.emit('08040000');branch('6700','sleep_click_done');ld(0,N+4);cmp(0,94);branch('6d00','sleep_next_page');cmp(0,224);branch('6c00','sleep_next_page');ld(1,N+6);cmp(1,120);branch('6d00','sleep_next_page');cmp(1,128);branch('6c00','sleep_next_page');wi(P+64,1);call('slider_value06');branch('6000','sleep_click_changed')
c.label('sleep_next_page');c.emit('7000');c.abs('1039',0xffff0119);cmp(0,4);branch('6d00','sleep_to_second');cmp(0,9);branch('6c00','sleep_to_second');bi(0xffff0119,0);branch('6000','sleep_click_changed');c.label('sleep_to_second');bi(0xffff0119,4);branch('6000','sleep_click_changed');c.label('sleep_to_third');bi(0xffff0119,4)
c.label('sleep_click_changed');ld(0,0xffff2798);st(0,0xffff011a);wi(P+4,1)
c.label('sleep_click_done');c.emit('4e75')
c.label('cycle_value');c.emit('08040001');branch('6600','cycle_prev');c.emit('52404e75');c.label('cycle_prev');c.emit('53404e75')
# Draw on the next sleep tick, retaining native timeout, fade and energy-bar updates.
c.label('sleep_frame03');tst(P+4);branch('6700','sleep_frame03_native');clear(P+4);c.jump(L['sleep16_changed']);c.label('sleep_frame03_native');c.jump(V['sleep16']);hook(0x7070,'sleep_frame03',8)
# HUD desired visual index (0=none, 1..9=button), based on press ownership and hover.
c.label('visual_update');clear(P+34);clear(P+2);tst(P);branch('6700','visual03_done');ld(0,N+20,True);branch('6700','visual03_done');call('owned_hover04');c.emit('4a40');branch('6700','visual03_done');ld(0,N+20,True);ld(1,N+12);c.emit('08010000');branch('6700','visual03_done');c.emit('204030280002');cmp(0,8);branch('6e00','visual03_done');c.emit('5240');st(0,P+2);c.label('visual03_done');ld(0,P+2);c.abs('b079',P+32);branch('6700','visual03_ready');st(0,P+32);c.emit('4a40');branch('6700','visual03_ready');call('hud_generate');c.label('visual03_ready');wi(P+34,1);c.emit('4e75')
# Rotate external panel borders only during its existing framebuffer upload.
c.label('panel_upload');c.emit('48e7fffe');call('key_texture07');call('panel_border');c.emit('4cdf7fff');call('upload_native');c.emit('48e7fffe');call('panel_border');call('key_restore07');c.emit('4cdf7fff4e75')
c.label('upload_native');c.emit(source[0x4d18:0x4d20].hex());c.jump(0x4d20);hook(0x4d18,'panel_upload',8)
c.label('panel_border');tst(P+98);branch('6600','circle_restore09');tst(P+72);branch('6600','unshade06');c.emit('0cb900002106');c.address(0xffff26b8);branch('6700','border_done');tst(P);branch('6700','border_done');ld(0,N+20,True);branch('6700','border_done');call('owned_hover04');c.emit('4a40');branch('6700','border_done');ld(0,N+20,True);c.emit('20400c6800080002');branch('6f00','border_done');ld(0,N+12);c.emit('08000000');branch('6700','border_done');c.abs('2479',P+12);c.emit('200a');branch('6700','border_done');c.emit('4a6a0010');branch('6700','border_done');ld(0,N+40,True);c.emit('b092');branch('6600','border_done');c.emit('0cb900007070');c.address(0xffff26b8);branch('6700','border_done')
c.emit('0c6a00040010');branch('6700','circle_shade09');c.emit('0c6a00020010');branch('6400','shade06')
# Enumerate top+left half of perimeter and swap with its 180-degree counterpart.
c.emit('302a000804400040342a000c04420008362a000a04430041382a000e04440009')
# Visual bevel bounds are independent of the clickable bounds.
ld(1,N+40,True)
for root in [0x5b8a,0x5ec2,0x5d1c,0x6068]:
 c.emit('0c81');c.address(root);branch('6700','border_shrink06')
branch('6000','border_bounds06');c.label('border_shrink06');c.emit('53435344');c.label('border_bounds06');c.emit('0c8100006068');branch('6600','border_bounds07');c.emit('52405242');c.label('border_bounds07');c.emit('3a003c02')
c.label('border_top');call('swap_pixel');c.emit('5245b645');branch('6c00','border_top');c.emit('3a005246')
c.label('border_side');c.emit('b846');branch('6f00','border_done');call('swap_pixel');c.emit('5246');branch('6000','border_side');c.label('border_done');c.emit('4e75')
# D0 left,D2 top,D3 right,D4 bottom,D5 x,D6 y; save all.
c.label('swap_pixel');c.emit('48e7fffe');movw(0,5);movw(1,6);call('pixel_address');c.emit('24481e1002400001');branch('6600','swap_odd1');c.emit('e80f');c.label('swap_odd1');imm(0x0240,7,15);c.emit('3f07')
# Reflect coordinates using saved registers on stack (D0 at SP+2 after pushed word).
c.emit('302f0004d06f0010906f0018322f000cd26f0014926f001c');call('pixel_address');c.emit('7e001e104a40');c.emit('02400001');branch('6600','swap_odd2');c.emit('e80f');c.label('swap_odd2');imm(0x0240,7,15);c.emit('321f');call('pixel_write');c.emit('204a302f0016024000013207');call('pixel_write');c.emit('4cdf7fff4e75')
c.label('pixel_address');c.emit('3400024200f8ed4ae549d4413200e24902410003d441');c.abs('41f9',0xffff8934);c.emit('d0c24e75')
c.label('pixel_write');c.emit('4a40');branch('6600','pixel_low');c.emit('e9090210000f83104e75');c.label('pixel_low');c.emit('021000f083104e75')
# HUD: six private tile slots immediately after the 192x128 world tiles.
# The experiment never uses these slots elsewhere. Name-table entries are restored
# before the pressed variant changes. Only the active button consumes VRAM.
VR=Path(OUT/'boot_vram.bin').read_bytes()
# Preserve live name table writes, including enabled/disabled icon variants.
original_tile=int.from_bytes(source[0x3600:0x3604],'big')
c.label('hud_track');c.emit('48e7e080');movw(1,2);imm(0x0440,1,0xe992);cmp(1,46);branch('6300','track_first');imm(0x0440,1,128);cmp(1,46);branch('6200','track_done');imm(0x0640,1,48)
c.label('track_first');c.abs('41f9',P+128);c.emit('31801000');c.label('track_done');c.emit('4cdf0107');c.jump(original_tile);hook(0x35fe,'hud_track')
# The game's regular VBlank path remains responsible for mouse polling and buffers.
oldvb=int.from_bytes(source[0x1755a:0x1755e],'big')
c.label('hud_vblank');c.emit('40e748e7fffe');call('hud_draw');c.emit('4cdf7fff46df');c.jump(oldvb);hook(0x17558,'hud_vblank')
# A signature guards VBlank calls before the experiment is initialized.
c.label('hud_draw');tst(P+116);branch('6700','hud_done');c.emit('0c795348');c.address(P+6);branch('6600','hud_done');c.emit('33fc8f02');c.address(0xc00004);tst(P+34);branch('6700','hud_done');ld(0,P+2);ld(1,P+24);c.emit('b041');branch('6700','hud_same');tst(P+24);branch('6700','hud_new');call('hud_restore');c.label('hud_new');ld(0,P+2);st(0,P+24);branch('6700','hud_done');call('hud_upload')
c.label('hud_same');tst(P+24);branch('6700','hud_done');call('hud_names');c.label('hud_done');c.emit('4e75')
c.label('hud_restore');ld(0,P+24);call('hud_index');c.abs('41f9',P+128);c.emit('d0c0');c.emit('7e017c02');c.label('restore_tile');c.emit('3018');call('vdp_name');c.emit('544251ce');c.fix.append((len(c.b),'restore_tile',2));c.emit('00000642007a41e8002a7c0251cf');c.fix.append((len(c.b),'restore_tile',2));c.emit('00004e75')
# Button IDs map to their shared 24x16 group and the two rows in the HUD table.
c.label('hud_index');c.emit('53400c400006');branch('6d00','hud_index_ok');c.emit('5340');c.label('hud_index_ok');c.emit('c0fc00063400323ce992d4414e75')
c.label('vdp_name');c.emit('48e76000');movw(1,2);c.emit('02413fff0041400033c1');c.address(0xc00004);c.emit('33fc0003');c.address(0xc00004);c.abs('33c0',0xc00000);c.emit('4cdf00064e75')
# Copy native 6 tiles to scratch, then modify perimeter pixels only.
c.label('hud_generate');ld(0,P+2);call('hud_index');c.abs('43f9',P+128);c.emit('d2c0');c.abs('45f9',P+256);c.emit('7e017a02');c.label('hud_copy_tile');c.emit('70003019024007ffeb48');c.abs('41f9',0x35a7e);c.emit('d0c07c07');c.label('hud_copy_pixels');c.emit('24d851cefffc51cd');c.fix.append((len(c.b),'hud_copy_tile',2));c.emit('000043e9002a7a0251cf');c.fix.append((len(c.b),'hud_copy_tile',2));c.emit('0000')
# Border pairs precomputed as byte offsets/masks. Avoid touching the pictogram.
c.abs('41f9',0x194800);c.emit('7e20');c.label('hud_pair');c.emit('7000301834003418');c.abs('43f9',P+256);c.abs('45f9',P+256);c.emit('d2c0d4c232183618');c.emit('18111a12024400ff024500ff');c.emit('0241000102430001');c.emit('4a41');branch('6600','hud_pair_a');c.emit('e80c');c.label('hud_pair_a');imm(0x0240,4,15);c.emit('4a43');branch('6600','hud_pair_b');c.emit('e80d');c.label('hud_pair_b');imm(0x0240,5,15)
c.emit('4a41');branch('6600','hud_pair_alow');c.emit('0211000fe90d8b11');branch('6000','hud_pair_putb');c.label('hud_pair_alow');c.emit('021100f08b11');c.label('hud_pair_putb');c.emit('4a43');branch('6600','hud_pair_blow');c.emit('0212000fe90c8912');branch('6000','hud_pair_next');c.label('hud_pair_blow');c.emit('021200f08912');c.label('hud_pair_next');c.emit('51cf');c.fix.append((len(c.b),'hud_pair',2));c.emit('0000')
# Beige highlight for the held half of the shared two-arrow button.
ld(0,P+2);cmp(0,6);branch('6700','hud_tint');cmp(0,7);branch('6600','hud_generated');c.label('hud_tint');imm(0x0440,0,6);imm(0x0240,0,1);c.emit('c0fc0100');c.abs('41f9',0x194a00);c.emit('d0c0');c.abs('43f9',P+256);c.emit('7e3f');c.label('tint_loop');c.emit('30183218e0491381000051cf');c.fix.append((len(c.b),'tint_loop',2));c.emit('0000');c.label('hud_generated');c.emit('4e75')
c.label('hud_upload');c.emit('23fc52000003');c.address(0xc00004);c.abs('41f9',P+256);c.emit('7e2f');c.label('hud_upload_loop');c.abs('23d8',0xc00000);c.emit('51cf');c.fix.append((len(c.b),'hud_upload_loop',2));c.emit('00004e75')
c.label('hud_names');ld(0,P+24);call('hud_index');c.emit('303c06907e017c02');c.label('hud_name_loop');call('vdp_name');c.emit('5240544251ce');c.fix.append((len(c.b),'hud_name_loop',2));c.emit('00000642007a7c0251cf');c.fix.append((len(c.b),'hud_name_loop',2));c.emit('00004e75')
# Extra initialization hook composed with the native cursor-safe init.
c.label('init03_all');call('init03');c.abs('41f9',0x194600);c.abs('43f9',P+128);c.emit('7e1722d851cffffc');wi(P+6,0x5348);wi(P+34,1);c.emit('4e75')
for p,label,n in list(c.fix):
 if label=='init03' and p < c.labels['init03_all']-BASE:c.fix.remove((p,label,n));c.fix.append((p,'init03_all',n))
r[0x194600:0x194660]=VR[0xe992:0xe9c2]+VR[0xea12:0xea42]
# Sparse patches for mouse on/off row, same font/palette as original sleep text.
def px(b,x,y,v):
 i=x//8*512+y*4+x%8//2;shift=0 if x%2 else 4;b[i]=(b[i]&~(15<<shift))|(v<<shift)
def txt(b,s,x,y):
 for j,ch in enumerate(s):
  tile=0 if ch==' ' else ord(ch)-21 if ch.isdigit() else ord(ch)-96
  for yy in range(8):
   for xx in range(8):
    v=source[0x30716+tile*32+yy*4+xx//2]>>(0 if xx%2 else 4)&15
    if v:px(b,x+j*8+xx,y+yy,15)
for on in range(2):
 b=bytearray(0x3000);txt(b,'mouse',8,96);txt(b,'on' if on else 'off',128,96)
 offsets=sorted({x//8*512+y*4+x%8//2 for x in range(8,168) for y in range(96,104)})
 data=b''.join(o.to_bytes(2,'big')+bytes([b[o],0]) for o in offsets);assert len(data)==2560;r[0x193000+on*2560:0x193000+(on+1)*2560]=data
# 21x14 frame in a 24x16 tile group (matches user's green region).
def hudoff(x,y):return (y//8*3+x//8)*32+y%8*4+x%8//2
pairs=[((x,1),(22-x,14)) for x in range(1,22)]+[((1,y),(21,15-y)) for y in range(2,14)]
data=b''.join(b''.join(v.to_bytes(2,'big') for v in [hudoff(*a),hudoff(*b),a[0]&1,b[0]&1]) for a,b in pairs);assert len(pairs)==33;r[0x194800:0x194800+len(data)]=data
# Arrow tint touches only non-background pixels well inside the frame.
for side in range(2):
 patches=[]
 for y in range(3,13):
  for x in range(2+10*side,10+12*side,2):
   tile=int.from_bytes(VR[0xe992+(15+x//8)*2+(y//8)*128:0xe994+(15+x//8)*2+(y//8)*128],'big')&2047
   val=source[0x35a7e+tile*32+y%8*4+x%8//2]
   conv={0:15,2:12,3:3,5:12,6:11,7:10};new=(conv.get(val>>4,val>>4)<<4)|conv.get(val&15,val&15)
   if x==20:
    yy=15-y;ti=int.from_bytes(VR[0xe992+30+(yy//8)*128:0xe994+30+(yy//8)*128],'big')&2047
    reflected=source[0x35a7e+ti*32+yy%8*4]&15
    new=(new&240)|reflected
   patches.append((hudoff(x,y),new))
 patches=(patches+[patches[-1]]*64)[:64]
 r[0x194a00+side*256:0x194b00+side*256]=b''.join(a.to_bytes(2,'big')+bytes([v,0]) for a,v in patches)
# Laboratory content and native panel behavior; never teleport out of the test map.
for x,z,v in [(12,12,0x89),(26,16,0x89),(17,16,0x9f),(12,24,0xa0),(19,14,0xa2)]:r[old['map']+(49-z)*80+x]=v
r[0x7792:0x7794]=bytes.fromhex('0451')
# Airlock action: require a confirmed code, flash the original action tile, stay in lab.
c.label('airlock_lab');tst(P+108);branch('6700','airlock_native35');tst(0xffff26ec,True);branch('6700','airlock_lab_done');c.abs('2279',0xffff227e);c.emit('337c00c00074');bi(0xffff2700,255);c.label('airlock_lab_done');c.emit('4e75');hook(0x784c,'airlock_lab')
# Every fuse click affects this test floor, with the original countdown machinery.
c.label('fuse_lab');c.emit(source[0x7a92:0x7a9a].hex());c.emit('2f00');ld(0,0xffff2150);st(0,P+28);c.emit('201f');c.jump(0x7a9a);hook(0x7a92,'fuse_lab',8)
c.label('fuse_lab_end');tst(P+108);branch('6700','fuse_native35');ld(0,P+28);c.emit('4640');st(0,0xffff2150);bi(0xffff2700,255);c.emit('4e75');hook(0x7ab2,'fuse_lab_end',6)
# Clip background band boundaries BEFORE taking differences. Native bands force
# one row even for negative heights, which is visible at the enlarged tilt.
c.label('background03');bi(0xffff2704,0);ld(0,0xffff2624);c.abs('b079',0xffff23b0);branch('6700','background03_done');st(0,0xffff23b0);bi(0xffff2704,255);c.abs('41f9',0xffff2d40);c.emit('7c00283c11111111')
for i,(height,depth) in enumerate([(512,3072),(512,4096),(512,5120),(0,5120),(0,4096),(0,3072)]):
 c.emit('323c'+f'{height:04x}'+'343c'+f'{depth:04x}');c.call(0x4bea);clamp(1,0,128,'bg03_'+str(i));call('bg03_fill');c.emit('068411111111')
c.emit('323c0080');call('bg03_fill');c.label('background03_done');c.emit('4e75')
c.label('bg03_fill');c.emit('bc41');branch('6c00','bg03_fill_done');c.emit('20c45246');branch('6000','bg03_fill');c.label('bg03_fill_done');c.emit('4e75');hook(0x4ae8,'background03')
# A single failed hardware handshake must not cancel a held repair. Two consecutive
# failed VBlank packets still disconnect normally; valid button-up is never delayed.
oldmouse={'poll_bad': 1573584, 'poll_end': 1573620}
c.label('poll03_ok');clear(P+36);bi(M+18,255);c.jump(oldmouse['poll_end']);hook(oldmouse['poll_bad']-12,'poll03_ok',8)
c.label('poll03_bad');c.emit('5279');c.address(P+36);c.emit('0c790002');c.address(P+36);branch('6400','poll03_disconnect');c.jump(oldmouse['poll_end']);c.label('poll03_disconnect');c.emit(source[oldmouse['poll_bad']:oldmouse['poll_bad']+8].hex());c.jump(oldmouse['poll_bad']+8);hook(oldmouse['poll_bad'],'poll03_bad',8)

# Copy the original nine-position slider strips to row120, one line below Mouse.
c.label('slider_row04');ld(0,N+2);tst(P+64);branch('6700','slider_draw06');ld(0,P+66);c.label('slider_draw06');c.emit('c0fc0200');c.abs('41f9',0x18b000);c.emit('d0c0');c.abs('43f9',0xffff92f4);c.emit('7e0f');c.label('slider04_col');c.emit('7c07');c.label('slider04_row');c.emit('22d851cefffc43e901e051cf');c.fix.append((len(c.b),'slider04_col',2));c.emit('00004e75')
# Menu bounds depend on hardware presence and enabled state; value survives off.
# Native IDs stay stable; visible order is 0,1,2,3,9,10 / 4,5,6,7,8.
c.label('sleep_nav04');c.emit('7000');c.abs('1039',0xffff0119);c.emit('08040000');branch('6700','nav05_down');cmp(0,0);branch('6600','nav05_up_middle');c.emit('7008');branch('6000','sleep04_store');c.label('nav05_up_middle');cmp(0,4);branch('6700','nav05_lastmouse');cmp(0,9);branch('6600','nav05_up_one');c.emit('7003');branch('6000','sleep04_store');c.label('nav05_up_one');c.emit('5340');branch('6000','sleep04_store')
c.label('nav05_lastmouse');c.emit('7003');tst(P+38);branch('6700','sleep04_store');c.emit('7009');tst(P);branch('6700','sleep04_store');c.emit('700a');branch('6000','sleep04_store')
c.label('nav05_down');c.emit('08040001');branch('6700','sleep04_action');cmp(0,3);branch('6600','nav05_notstripe');tst(P+38);branch('6700','nav05_down_one');c.emit('7009');branch('6000','sleep04_store');c.label('nav05_notstripe');cmp(0,9);branch('6600','nav05_notswitch');tst(P);branch('6600','nav05_down_one');c.emit('7004');branch('6000','sleep04_store');c.label('nav05_notswitch');cmp(0,10);branch('6600','nav05_notlast');c.emit('7004');branch('6000','sleep04_store');c.label('nav05_notlast');cmp(0,8);branch('6600','nav05_down_one');c.emit('7000');branch('6000','sleep04_store');c.label('nav05_down_one');c.emit('5240');c.label('sleep04_store');c.abs('13c0',0xffff0119);c.jump(L['sleep16_changed']);c.label('sleep04_action');jmp('sleep_input')
# Address taken from the v34 symbol table at build authoring time.
hook(0xf7004,'sleep_nav04',8)
# Presence comes from bounded VBlank polling. Preserve a deliberate Mouse off
# until the physical device is removed and reconnected.
c.label('detect04');tst(M+18,True);branch('6600','detect04_present');ld(0,P+38);c.abs('8079',P);branch('6700','detect04_done');clear(P);clear(P+38);call('mouse_toggle05');c.emit('0c390009');c.address(0xffff0119);branch('6500','detect04_refresh');bi(0xffff0119,3);branch('6000','detect04_refresh')
c.label('detect04_present');tst(P+38);branch('6600','detect04_done');wi(P+38,1);wi(P,1)
c.label('detect04_refresh');c.emit('0cb900007070');c.address(0xffff26b8);branch('6600','detect04_done');tst(0xffff0118,True);branch('6700','detect04_done');wi(P+4,1)
c.label('detect04_done');c.emit('4e75')
# Geometric press ownership is independent of the action becoming unavailable
# after it has already executed (e.g. dropping the last item).
c.label('owned_hover04');c.emit('48e77ffe');c.abs('2279',N+20);c.emit('2009');branch('6700','owned04_no');c.emit('30290002');cmp(0,8);branch('6e00','owned04_panel');c.emit('e548');c.abs('41f9',0x18d020);c.emit('d0c0');ld(1,N+4);c.emit('b250');branch('6d00','owned04_no');c.emit('b2680002');branch('6c00','owned04_no');ld(1,N+6);cmp(1,153);branch('6d00','owned04_no');cmp(1,167);branch('6c00','owned04_no');branch('6000','owned04_yes')
c.label('owned04_panel');c.abs('2079',P+12);c.emit('2008');branch('6700','owned04_no');ld(1,N+40,True);c.emit('b290');branch('6600','owned04_no');c.emit('d1fc');c.address(click_table-table);ld(1,N+4);c.emit('b2680008');branch('6d00','owned04_no');c.emit('b268000a');branch('6c00','owned04_no');ld(1,N+6);c.emit('b268000c');branch('6d00','owned04_no');c.emit('b268000e');branch('6c00','owned04_no');c.label('owned04_yes');c.emit('7001');branch('6000','owned04_end');c.label('owned04_no');c.emit('7000');c.label('owned04_end');c.emit('4cdf7ffe4e75')
# Lock world shooting to the location where the left press began.
c.label('press_origin04');ld(0,N+12);c.emit('08000001');branch('6600','origin04_held');clear(P+40);c.emit('4e75');c.label('origin04_held');ld(0,N+14);c.emit('08000001');branch('6700','origin04_done');clear(P+40);c.emit('0cb900002106');c.address(0xffff26b8);branch('6600','origin04_done');call('in_world');st(0,P+40);c.label('origin04_done');c.emit('4e75')

# Snapshot only: never call native UI/audio/VDP code with IRQs masked.
c.label('snapshot05');ld(0,M+4,True);st(0,P+48,True);ld(0,M+8,True);st(0,P+52,True);ld(0,M+12);st(0,P+56);ld(0,M+16);st(0,P+58);clear(M+4,True);clear(M+8,True);clear(M+16);c.emit('4e75')
# Off resets the view, hides the pointer immediately and releases click ownership.
c.label('mouse_toggle05');tst(P);branch('6600','toggle05_on');clear(N);clear(P+2);clear(P+40);call('release_ui');clear(M+22);wi(P+70,1);call('cursor_hide05');c.emit('4e75');c.label('toggle05_on');clear(P+70);wi(N,1);c.emit('4e75')
c.label('cursor_hide05');c.emit('0cb900007070');c.address(0xffff26b8);branch('6600','cursor_done');clear(0xffff29c8);clear(0xffff29ce);c.emit('4e75')
c.label('soft_off06');c.emit('0cb900007070');c.address(0xffff26b8);branch('6600','disabled05');tst(P+70);branch('6700','disabled05_done');tst(M+18,True);branch('6700','disabled05_done');ld(0,P+58);c.emit('08000000');branch('6700','disabled05_done');wi(P,1);call('mouse_toggle05');call('cursor');bi(0xffff0118,1);bi(0xffff0119,9);wi(P+4,1);ld(0,0xffff2798);st(0,0xffff011a);c.emit('4e75')
# Off takes full effect when sleep is left, including centering the horizon.
c.label('disabled05');clear(P+70);clear(P+64);clear(N+8);clear(N+10);wi(N+32,70);wi(0xffff23b0,65535);wi(N+4,160);wi(N+6,72);clear(N+24,True);clear(N+28,True);clear(N+16,True);clear(N+20,True);clear(P+12,True);clear(P+8,True);c.label('disabled05_done');c.emit('4e75')
# Drag uses the old sensitivity until release. Vertical movement does not cancel it.
c.label('slider_value06');ld(0,N+4);imm(0x0440,0,96);imm(0x0640,0,7);clamp(0,0,127,'drag06');c.emit('02800000ffff80fc000f');clamp(0,0,8,'dragval06');st(0,P+66);c.emit('4e75')
c.label('slider_drag06');tst(P+64);branch('6700','drag06_done');c.emit('0cb900007070');c.address(0xffff26b8);branch('6600','drag06_commit');clear(N+16,True);ld(0,N+12);c.emit('08000000');branch('6700','drag06_commit');call('slider_value06');ld(0,0xffff2798);st(0,0xffff011a);wi(P+4,1);c.emit('4e75');c.label('drag06_commit');call('slider_value06');ld(0,P+66);st(0,N+2);clear(P+64);clear(N+24,True);clear(N+28,True);wi(P+4,1);c.label('drag06_done');c.emit('4e75')
# Double the native PAL/NTSC menu timeout, preserving the native timer source.
r[0xf6fe2:0xf6fe4]=(600).to_bytes(2,'big');r[0xf6ff2:0xf6ff4]=(500).to_bytes(2,'big')
# Dedicated copy of the panel tile bank for bomb only; no global palette changes.
# E1 is the confirmed-but-not-armed indicator. B1 retains native red/armed semantics.
bank=0x196000
r[bank:bank+0x8000]=source[0x183f2:0x203f2]
for i in range(0x8000):
 v=r[bank+i];r[bank+i]=((13 if v>>4==1 else v>>4)<<4)|(13 if v&15==1 else v&15)
tile=bytearray(source[0x183f2+0xb3*128:0x183f2+0xb4*128])
for y in range(4,8):
 for x in range(5,11):
  off=x//8*64+y*4+x%8//2;shift=0 if x&1 else 4
  color=1
  tile[off]=(tile[off]&~(15<<shift))|(color<<shift)
r[bank+0xe1*128:bank+0xe2*128]=tile
c.label('bomb_bank05');wi(0xffff7da0,0x0770);call('bomb_indicator06');c.emit('23fc');c.address(bank);c.address(0xffff2282);c.jump(0x953c);hook(0x9532,'bomb_bank05',10)
c.label('bomb_input05');c.call(int.from_bytes(source[0x988a:0x988e],'big'));c.abs('2079',0xffff227e);c.emit('0c6800b1000a');branch('6700','bomb05_done');c.emit('303c00b3');tst(0xffff013c,True);branch('6700','bomb05_store');c.emit('303c00e1');c.label('bomb05_store');c.emit('3140000a');bi(0xffff2700,255);c.label('bomb05_done');c.emit('4e75');hook(0x9888,'bomb_input05')
# Preserve confirmation on reopen. Original opening sets A0 to the panel resource.
c.label('bomb_open06');call('preopen09');c.abs('41f9',0x1813a);c.jump(0x9500);hook(0x94fa,'bomb_open06')
c.label('bomb_indicator06');c.abs('2079',0xffff227e);c.emit('303c00b3');tst(0xffff013c,True);branch('6700','bomb_indicator_store06');c.emit('303c00e1');c.label('bomb_indicator_store06');c.emit('3140000a');bi(0xffff2700,255);c.emit('4e75')
c.label('bomb_idle06');call('bomb_indicator06');c.jump(0x9638);hook(0x9632,'bomb_idle06')
c.label('bomb_planted06');bi(0xffff013c,0);c.emit(source[0x9610:0x9616].hex());c.jump(0x9616);hook(0x9610,'bomb_planted06')
# Scanman brightness overlays: exact marked 11x32 toggle; backup prevents
# information loss when clamping the lightest/darkest palette entries.
shade_offsets=[]
for y in range(32,64):
 for x in range(160,172,2):
  off=x//8*512+y*4+x%8//2
  shade_offsets.append(off|(0x8000 if x==170 else 0))
r[0x19e400:0x19e580]=b''.join(o.to_bytes(2,'big') for o in shade_offsets)
for amount in [1,2]:
 for half in range(2):
  for dim in range(2):
   def sh(v):return max(2,min(7,v+(-amount if dim else amount))) if 2<=v<=7 else v
   a=0x19e000 if amount==1 else 0x19e600
   r[a+half*512+dim*256:a+half*512+dim*256+256]=bytes((sh(v>>4)<<4)|(v&15 if half else sh(v&15)) for v in range(256))
c.label('shade06');wi(P+72,1);c.emit('362a0010302a00105540e148');c.abs('45f9',0x19e000);c.emit('d4c0');c.abs('41f9',0x19e400);c.abs('47f9',0xffff0500);c.emit('3e3c00bf')
c.label('shade06_loop');c.emit('3418320202417fff');c.abs('43f9',0xffff8934);c.emit('d2c17000101116c0');c.emit('4a42');branch('6a00','shade06_full');c.emit('06400200');c.label('shade06_full');cmp(3,2);branch('6600','shade07_lower');cmp(7,96);branch('6d00','shade07_two');branch('6000','shade07_apply');c.label('shade07_lower');cmp(7,96);branch('6d00','shade07_apply');c.label('shade07_two');imm(0x0640,0,0x600);c.label('shade07_apply');c.emit('12b2000051cf');c.fix.append((len(c.b),'shade06_loop',2));c.emit('0000');call('scan_contrast35');c.emit('4e75')
c.label('unshade06');clear(P+72);c.abs('41f9',0x19e400);c.abs('47f9',0xffff0500);c.emit('3e3c00bf');c.label('unshade06_loop');c.emit('321802417fff');c.abs('43f9',0xffff8934);c.emit('d2c112db51cf');c.fix.append((len(c.b),'unshade06_loop',2));c.emit('00004e75')
# The game's own transient Scanman highlight must not compete with held bevels.
c.label('panel_render06');c.emit('48e7fffe');call('code_green09');tst(P);branch('6700','render06_native');ld(0,N+40,True);c.emit('0c800000597e');branch('6600','render07_keys');c.call(0x8940);branch('6000','render06_native');c.label('render07_keys')
for root in [0x5b8a,0x5d1c,0x5ec2]:
 c.emit('0c80');c.address(root);branch('6700','render07_key_reset')
branch('6000','render06_native');c.label('render07_key_reset');c.label('render06_native');c.emit('4cdf7fff');c.emit(source[0x38c8:0x38ce].hex());c.jump(0x38ce);hook(0x38c8,'panel_render06')

# Publish click feedback before native actions that can wait or redraw the HUD.
# Action dispatch remains edge-only; there is no synthetic B during UI holds.
c.label('feedback07');c.emit('48e7fffe');call('cursor');c.abs('2079',N+20);c.emit('30280002');cmp(0,8);branch('6e00','feedback07_panel');call('visual_update');c.call(0x2930);branch('6000','feedback07_done')
c.label('feedback07_panel');c.abs('2079',P+12);c.emit('2008');branch('6700','feedback07_done');c.emit('4a680010');branch('6700','feedback07_done');c.call(0x38c8);c.call(0x2930);c.call(0x4d18)
c.label('feedback07_done');c.emit('4cdf7fff4e75')
# Keep the game's native depressed digit/Enter graphics throughout the hold.
# Tile map remains untouched: action decoding still sees its expected original data.
c.label('key_texture07');clear(P+74);tst(P);branch('6700','key07_done');c.emit('0cb900002106');c.address(0xffff26b8);branch('6700','key07_done');c.emit('0cb900007070');c.address(0xffff26b8);branch('6700','key07_done');ld(0,N+20,True);branch('6700','key07_done');call('owned_hover04');c.emit('4a40');branch('6700','key07_done');ld(0,N+12);c.emit('08000000');branch('6700','key07_done');c.abs('2479',P+12);c.emit('200a');branch('6700','key07_done');ld(0,N+40,True);c.emit('b092');branch('6600','key07_done')
for root in [0x5b8a,0x5d1c,0x5ec2]:
 c.emit('0c80');c.address(root);branch('6700','key07_root')
branch('6000','key07_done')
c.label('key07_root');c.abs('2279',N+20);c.emit('30290002');cmp(0,83);branch('6e00','key07_done');cmp(0,9);branch('6d00','key07_done');imm(0x0440,0,9);c.abs('2079',0xffff227e);c.abs('d0f9',0xffff223e);c.emit('34300000');cmp(2,0xb4);branch('6d00','key07_normal');cmp(2,0xbf);branch('6e00','key07_done');imm(0x0440,2,20);c.label('key07_normal');cmp(2,0xa0);branch('6d00','key07_done');cmp(2,0xab);branch('6e00','key07_done');imm(0x0640,2,20);st(2,P+82)
# Cell origin lies one pixel above/left of the clickable/visible bevel.
c.emit('302a000804400041322a000c04410009');call('pixel_address');c.abs('23c8',P+76);wi(P+80,2);c.emit('0c6900530002');branch('6600','key07_width');wi(P+80,4);c.label('key07_width')
c.abs('43f9',0xffff0600);ld(7,P+80);c.emit('5347');c.label('key07_copy_col');c.emit('7c0f');c.label('key07_copy_row');c.emit('22d851cefffc41e801c051cf');c.fix.append((len(c.b),'key07_copy_col',2));c.emit('0000');wi(P+74,1)
c.abs('2079',P+76);ld(0,P+82);c.call(0x3900);c.emit('0c790004');c.address(P+80);branch('6600','key07_done');c.abs('2079',P+76);c.emit('41e80400');ld(0,P+82);c.emit('5240');c.call(0x3900);c.label('key07_done');c.emit('4e75')
c.label('key_restore07');tst(P+74);branch('6700','restore07_done');clear(P+74);c.abs('2079',P+76);c.abs('43f9',0xffff0600);ld(7,P+80);c.emit('5347');c.label('key07_restore_col');c.emit('7c0f');c.label('key07_restore_row');c.emit('20d951cefffc41e801c051cf');c.fix.append((len(c.b),'key07_restore_col',2));c.emit('0000');c.label('restore07_done');c.emit('4e75')
# Experimental correction restricted to the live plant: reverse eight azimuth views.
# The shared facing routine and other objects keep their original behavior.
c.label('flower07');c.emit('30280028');c.call(0xce76);c.emit('e849444102410007d268001e31410020');c.jump(0x44e0)
r[0xb5e2:0xb5e6]=c.labels['flower07'].to_bytes(4,'big')
