"""Cyber-Cop v35: main game plus isolated laboratory and Sega Mouse."""
from pathlib import Path
import json,hashlib,math,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
source=(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'mouse_lab/MouseLab_A_Direct.bin').read_bytes()
assert hashlib.sha256(source).hexdigest()=='707ffdee9b6abdd97d3197128f5b9dbae674b1305781dd1167f6ae4a060fb675', 'Expected exact MouseLab_A_Direct from Test01'
old={'map': 1573978, 'start_world': 1572936, 'step': 1573140}
L={'band21_fix': 1017832, 'band21_native': 1018012, 'cursor24': 1018276, 'main_input': 983742, 'object15_input': 1010796, 'pad28_consume': 1022648, 'project17': 1013468, 'sleep16_changed': 1012012, 'sleep16_draw': 1012070, 'sleep16_show': 1012028, 'sleep16_toggle': 1011780, 'sleep31_toggle': 1011896}
r=bytearray(source);BASE=0x183000;M=0xffff0180;N=0xffff01a0;P=0xffff0200
class Code:
 def __init__(self):self.b=bytearray();self.labels={};self.fix=[]
 def emit(self,h):self.b.extend(bytes.fromhex(h))
 def address(self,a):self.b.extend(a.to_bytes(4,'big'))
 def label(self,s):self.labels[s]=BASE+len(self.b)
 def abs(self,op,a):self.emit(op);self.address(a)
 def call(self,a):self.abs('4eb9',a)
 def jump(self,a):self.abs('4ef9',a)
 def branch(self,op,s):self.emit(op);self.fix.append((len(self.b),s,2));self.emit('0000')
 def ref(self,op,s):self.emit(op);self.fix.append((len(self.b),s,4));self.address(0)
c=Code()
def ld(reg,a,long=False):c.abs(f'{(0x2039 if long else 0x3039)+(reg<<9):04x}',a)
def st(reg,a,long=False):c.abs(f'{(0x23c0 if long else 0x33c0)+reg:04x}',a)
def wi(a,v):c.emit('33fc'+f'{v&65535:04x}');c.address(a)
def bi(a,v):c.emit('13fc'+f'{v&255:04x}');c.address(a)
def imm(op,reg,v):c.emit(f'{op+reg:04x}{v&65535:04x}')
def cmp(reg,v):imm(0x0c40,reg,v)
def tst(a,byte=False):c.abs('4a39' if byte else '4a79',a)
def clear(a,long=False):c.abs('42b9' if long else '4279',a)
def hook(a,label,n=6):r[a:a+n]=bytes.fromhex('4ef9')+c.labels[label].to_bytes(4,'big')+bytes.fromhex('4e71')*((n-6)//2)
def call(s):c.ref('4eb9',s)
def jmp(s):c.ref('4ef9',s)
def branch(op,s):c.branch(op,s)
def movw(dst,src):c.emit(f'{0x3000+(dst<<9)+src:04x}')
def clamp(reg,lo,hi,name):
 cmp(reg,lo);branch('6c00',name+'lo');imm(0x303c+(reg<<9)-reg,reg,lo);c.label(name+'lo')
 cmp(reg,hi);branch('6f00',name+'hi');imm(0x303c+(reg<<9)-reg,reg,hi);c.label(name+'hi')
# New independent state; no SRAM serialization.
c.label('init');c.abs('41f9',N);c.emit('703f421851c8fffc');wi(N+2,4);wi(N+4,160);wi(N+6,72);wi(N+32,70);call('init03');c.jump(0x207a)
a=source.index(bytes.fromhex('4ef90000207a'),old['start_world'],old['step']);hook(a,'init')
# Capture active external panel node list; use native matching/validation.
c.label('capture_panel');c.abs('23c8',N+40);c.jump(L['cursor24']);hook(0x8f24,'capture_panel')
# A new panel starts with no clickable external list until its native UI enables it.
c.label('panel_load');call('panel_enter08');clear(N+40,True);c.emit(source[0x8c66:0x8c6c].hex());c.jump(0x8c6c);hook(0x8c66,'panel_load')
# Inventory and external-panel native B handling is superseded only in free-pointer mode.
c.label('native_ui');tst(N);branch('6700','native_ui_go');c.emit('4e75');c.label('native_ui_go');c.jump(L['object15_input']);hook(0x53ea,'native_ui')
# Projection offsets precede clipping: no post-render image shift.
c.label('project_wall');c.call(L['project17']);c.abs('d279',N+8);c.abs('dc79',N+8);c.emit('023c00f74e75');hook(0x4c86,'project_wall')
c.label('project_point');call('point_native');branch('6b00','project_point_done');c.abs('d279',N+8);c.emit('023c00f7');c.label('project_point_done');c.emit('4e75')
c.label('point_native');c.emit(source[0x4c04:0x4c0a].hex());c.jump(0x4c0a);hook(0x4c04,'project_point')
c.label('background');c.emit('323c0046');c.abs('9279',N+8);c.emit('9243');c.jump(0x4bfe);hook(0x4bf8,'background')
# Other native vertical computations: projectile shadows and beam thickness.
c.label('shadow_y');c.emit('323c0046');c.abs('d279',N+8);c.emit('d243');c.jump(0x4556);hook(0x4550,'shadow_y')
c.label('beam_radius');c.emit('06420046');c.abs('d479',N+8);c.emit('9469fffe');c.jump(0xd06c);hook(0xd064,'beam_radius',8)
# Near-plane stripe reconstruction uses the same shifted vanishing point.
for idx in range(2):
 start=L['band21_fix'];end=L['band21_native'];needle=bytes.fromhex('04410046c3c5');positions=[p for p in range(start,end) if source[p:p+6]==needle];a=positions[idx]
 c.label('stripe_sub'+str(idx));c.abs('9279',N+32);c.emit('c3c5');c.jump(a+6);hook(a,'stripe_sub'+str(idx))
 needle=bytes.fromhex('064100466900');positions=[p for p in range(start,end) if source[p:p+6]==needle];a=positions[idx];target=a+6+int.from_bytes(source[a+6:a+8],'big',signed=True)
 c.label('stripe_add'+str(idx));c.abs('d279',N+32);branch('6800','stripe_add_ok'+str(idx));c.jump(target);c.label('stripe_add_ok'+str(idx));c.jump(a+8);hook(a,'stripe_add'+str(idx),8)
# Ordinary free shot: disable native homing, keep native projectile collisions.
c.label('aim');tst(N);branch('6700','aim_native_go');call('set_aim');call('cursor');c.emit('4e75');c.label('aim_native_go');jmp('aim_native')
c.label('aim_native');c.emit(source[0xac1e:0xac24].hex());c.jump(0xac24);hook(0xac1e,'aim')
c.label('set_aim');bi(0xffff2714,0);ld(0,N+4);imm(0x0440,0,64);clamp(0,0,191,'aimx');st(0,0xffff29ae);ld(0,N+6);imm(0x0440,0,8);clamp(0,0,127,'aimy');st(0,0xffff29b0);c.emit('4e75')
# Screen-space angular tables use the original game's projection (focal length256).
c.label('shot_x');tst(N);branch('6700','shot_x_native');ld(0,0xffff29ae);c.emit('d040');c.abs('49f9',0x18d800);c.emit('30340000');c.abs('d079',0xffff260c);imm(0x0240,0,1022);c.emit('31400028');c.jump(0xa7ce)
c.label('shot_x_native');c.emit(source[0xa7ac:0xa7b4].hex());c.jump(0xa7b4);hook(0xa7ac,'shot_x',8)
c.label('shot_y');ld(0,0xffff29b0);c.abs('d079',N+8);tst(N);branch('6600','shot_y_free');clamp(0,0,127,'native_pitch');c.emit('e448');c.abs('49f9',0x11456);c.emit('103400004880024003fe31400032');c.jump(0xa7ea);c.label('shot_y_free');clamp(0,-100,227,'shoty');imm(0x0640,0,100);c.emit('d040');c.abs('49f9',0x18da00);c.emit('30340000024003fe31400032');c.jump(0xa7ea);hook(0xa7ce,'shot_y')
# A free ray originates at the actual camera height, so cursor and collision ray agree.
c.label('shot_origin');tst(N);branch('6700','shot_origin_native');ld(0,0xffff2624);c.emit('3140000a');c.jump(0xa790);c.label('shot_origin_native');c.emit(source[0xa788:0xa790].hex());c.jump(0xa790);hook(0xa788,'shot_origin',8)
# Consume input atomically. Mouse driver and VBlank buffering from Direct are reused.
c.label('consume');c.call(L['pad28_consume']);c.emit('40e7007c070048e7fffe');call('snapshot05');c.emit('46ef003c')
call('lift_busy35c');c.emit('4a40');branch('6600','consume_end');call('detect04');call('panel_return08');call('guard08');tst(P);branch('6700','mouse_off');tst(M+18,True);branch('6600','mouse_present');call('release_ui');clear(N);clear(M+22);branch('6000','consume_end');c.label('mouse_off');clear(N);call('soft_off06');branch('6000','consume_end');c.label('mouse_present')
ld(4,P+56);c.abs('8879',P+58);ld(5,P+58)
c.emit('08050002');branch('6700','mode_set');c.emit('0cb900007070');c.address(0xffff26b8);branch('6700','mode_set');c.emit('0a790001');c.address(N);tst(N);branch('6600','mode_keep_menu');c.emit('0cb900002106');c.address(0xffff26b8);branch('6600','mode_keep_menu');bi(0xffff270a,0);c.label('mode_keep_menu');call('release_ui');clear(M+22);clear(N+24,True);clear(N+28,True);imm(0x0240,4,4);imm(0x0240,5,4)
c.label('mode_set');st(4,N+12);st(5,N+14)
# Restore prior synthetic button state before merging this frame.
ld(0,M+22);c.emit('4640');c.abs('c179',0xffff0006);clear(M+22)
c.emit('0cb900007070');c.address(0xffff26b8);branch('6700','sleep_mouse')
tst(0xffff270a,True);branch('6700','mouse_no_inventory');wi(N,1);c.label('mouse_no_inventory');tst(N);branch('6600','free_move')
# Capture mode: left=A, right=B. Middle toggles, no C alias.
c.emit('720008040000');branch('6700','look_right');imm(0x0040,1,64);c.label('look_right');c.emit('08040001');branch('6700','look_buttons');imm(0x0040,1,16);c.label('look_buttons');st(1,M+22);c.emit('4641');c.abs('c379',0xffff0004)
tst(0xffff270a,True);branch('6600','discard')
call('force_strafe');ld(0,P+48,True);call('scale_yaw');c.abs('d179',0xffff260c)
c.emit('027903fe');c.address(0xffff260c);c.abs('d179',0xffff443a);c.emit('027903fe');c.address(0xffff443a)
ld(0,P+52,True);call('scale_y');c.emit('4440');c.abs('d079',N+8);clamp(0,-100,100,'pan');st(0,N+8);imm(0x0640,0,70);st(0,N+32);ld(0,N+8);c.abs('b079',N+10);branch('6700','discard');st(0,N+10);wi(0xffff23b0,65535);branch('6000','discard')
c.label('free_move');ld(0,P+48,True);call('scale_x');c.abs('d079',N+4);clamp(0,0,319,'cursorx');st(0,N+4)
ld(0,P+52,True);call('scale_y');c.emit('4440');c.abs('d079',N+6);clamp(0,0,223,'cursory');st(0,N+6)
call('press_origin04');call('hit_test');call('slider_drag06');tst(P+64);branch('6600','free_after_click');call('sleep_click');ld(4,N+12);ld(5,N+14)
# Release a button action even if pointer moved away, preserving repair semantics.
c.emit('08040000');branch('6600','free_down');call('release_ui');branch('6000','free_after_click')
c.label('free_down');c.emit('08050000');branch('6700','free_hold');ld(0,N+16,True);branch('6700','free_hold');call('press_ui')
c.label('free_hold');branch('6000','free_after_click')
c.label('free_after_click');call('lift_busy35c');c.emit('4a40');branch('6600','discard');c.emit('0cb900007070');c.address(0xffff26b8);branch('6700','discard');c.emit('0cb900002106');c.address(0xffff26b8);branch('6700','free_shoot')
# Free pointer in a panel: right edge is native Start, never an A action.
ld(4,N+14);c.emit('08040001');branch('6700','discard');c.emit('08b90007');c.address(0xffff0005);c.emit('08f90007');c.address(0xffff0007);wi(M+22,128);branch('6000','discard')
c.label('free_shoot');tst(P+40);branch('6700','free_walk');call('in_world');c.emit('4a40');branch('6700','free_walk');ld(4,N+12);c.emit('08040001');branch('6700','free_walk');bi(0xffff270a,0);call('set_aim');c.call(0xa704)
c.label('free_walk');tst(0xffff270a,True);branch('6600','discard');call('force_strafe');branch('6000','discard')
c.label('sleep_mouse');wi(N,1);branch('6000','free_move')
c.label('discard')
c.label('consume_end');call('stop_inventory09');c.emit('4cdf7fff46df4e75')
r[L['main_input']+2:L['main_input']+6]=c.labels['consume'].to_bytes(4,'big')
c.label('force_strafe');ld(0,0xffff0004);imm(0x0240,0,12);cmp(0,12);branch('6700','force_done');c.emit('08b90006');c.address(0xffff0005);c.label('force_done');c.emit('4e75')
# Signed fixed point; remainder preserves slow motion and avoids asymmetry.
for kind,rem,shift in [('yaw',N+24,4),('x',N+28,3),('y',N+30,3)]:
 c.label('scale_'+kind);ld(1,N+2);c.emit('d241');c.abs('43f9',0x18d000);c.emit('c1f11000');ld(1,rem);c.emit('48c1d0812200');imm(0x0240,1,(1<<shift)-1);st(1,rem)
 for _ in range(shift):c.emit('e280')
 if kind=='yaw':c.emit('d040')
 c.emit('4e75')
c.label('in_world');ld(0,N+4);cmp(0,64);branch('6d00','not_world');cmp(0,255);branch('6e00','not_world');ld(0,N+6);cmp(0,8);branch('6d00','not_world');cmp(0,135);branch('6e00','not_world');c.emit('70014e75');c.label('not_world');c.emit('70004e75')
# Hit testing native UI nodes. Inventory rectangles cover actual button spacing.
c.label('hit_test');clear(N+16,True);clear(P+8,True);ld(0,N+4);ld(1,N+6);c.abs('43f9',0x561c);c.abs('45f9',0x18d020);c.emit('7e08')
c.label('hit_inventory');c.emit('b052');branch('6d00','hit_next');c.emit('b06a0002');branch('6c00','hit_next');cmp(1,153);branch('6d00','hit_next');cmp(1,167);branch('6c00','hit_next')
c.emit('0cb900007070');c.address(0xffff26b8);branch('6600','inventory_awake');c.emit('4a690002');branch('6600','hit_next');c.label('inventory_awake');c.emit('48e7fffe30290002e548');c.abs('4bf9',0x5542);c.emit('2a7500004e954a404cdf7fff');branch('6600','hit_next');c.abs('23c9',N+16);c.emit('4e75')
c.label('hit_next');c.emit('43e9001445ea000451cf');c.fix.append((len(c.b),'hit_inventory',2));c.emit('0000')
call('hit_panel03');c.emit('4e75')
c.label('press_ui');call('save_mode08');call('save_press');c.abs('2279',N+16);c.abs('23c9',0xffff202a);c.abs('23c9',N+20);bi(0xffff270a,255);call('feedback07');c.abs('2279',N+20);ld(7,0xffff0004);imm(0x0240,7,0xffef);c.emit('302900020c400008');branch('6e00','press_external');c.emit('e548');c.abs('4bf9',0x548a);c.emit('2a7500004ed5')
c.label('press_external');imm(0x0440,0,9);c.abs('2a79',0xffff226e);c.emit('4ed5')
c.label('release_ui');c.abs('2279',N+20);clear(N+20,True);c.emit('2009');branch('6700','release_done');c.emit('302900020c400008');branch('6e00','release_done');c.emit('e548');c.abs('4bf9',0x54ae);c.emit('2a7500004ed5');c.label('release_done');c.emit('4e75')
# Draw after all native input/hotkey processing, so joystick code cannot snap it back.
c.label('cursor_tail');c.emit('48e7fffe');call('cursor');call('visual_update');c.emit('4cdf7fff');c.jump(0x20b8)
a=source.index(bytes.fromhex('4ef9000020b8'),L['main_input'],L['main_input']+80);hook(a,'cursor_tail')
c.label('cursor');tst(P);branch('6700','cursor_hide05');tst(N);branch('6700','cursor_done');tst(M+18,True);branch('6700','cursor_done');c.emit('0cb900007070');c.address(0xffff26b8);branch('6700','cursor_arrow');call('in_world');c.emit('4a40');branch('6700','cursor_arrow');c.emit('0cb900002106');c.address(0xffff26b8);branch('6600','cursor_arrow')
ld(0,N+4);imm(0x0640,0,120);st(0,0xffff29ce);ld(0,N+6);imm(0x0640,0,120);st(0,0xffff29c8);bi(0xffff29ca,5);ld(0,0xffff29c4);imm(0x0640,0,44);st(0,0xffff29cc);branch('6000','cursor_done')
c.label('cursor_arrow');ld(0,N+4);imm(0x0640,0,116);st(0,0xffff29ce);ld(0,N+6);imm(0x0640,0,124);st(0,0xffff29c8);bi(0xffff29ca,9);ld(0,0xffff29c4);imm(0x0640,0,20);st(0,0xffff29cc)
c.label('cursor_done');c.emit('4e75')
# Third sleep page, same existing timeout. Left/right only, clamped nine positions.
r[0xf701a:0xf701c]=bytes.fromhex('700a');r[0xf7032:0xf7034]=bytes.fromhex('000b')
c.label('sleep_input');cmp(0,9);branch('6600','sleep_not_mouse');c.emit('0244007c');branch('6700','sleep_still');c.emit('0a790001');c.address(P);call('mouse_toggle05');c.jump(L['sleep16_changed']);c.label('sleep_not_mouse');cmp(0,10);branch('6600','sleep_input_native');ld(0,N+2);c.emit('08040002');branch('6700','sleep_right');c.emit('5340');branch('6000','sleep_limit');c.label('sleep_right');c.emit('08040003');branch('6700','sleep_still');c.emit('5240');c.label('sleep_limit');clamp(0,0,8,'sensitivity');st(0,N+2);clear(N+24,True);clear(N+28,True);c.jump(L['sleep16_changed']);c.label('sleep_still');c.jump(L['sleep16_show'])
c.label('sleep_input_native');cmp(0,4);branch('6c00','sleep_input_cheats');c.jump(L['sleep16_toggle']+8);c.label('sleep_input_cheats');c.jump(L['sleep31_toggle']);hook(L['sleep16_toggle'],'sleep_input',8)
c.label('sleep_draw');c.emit('7000');c.abs('1039',0xffff0119);c.abs('13c0',P+44);cmp(0,9);branch('6d00','draw05_native');bi(0xffff0119,3);c.label('draw05_native');call('sleep_draw_native');c.emit('7000');c.abs('1039',P+44);c.abs('13c0',0xffff0119);c.emit('4e75')
c.label('sleep_draw_native');c.emit(source[L['sleep16_draw']:L['sleep16_draw']+8].hex());c.jump(L['sleep16_draw']+8);hook(L['sleep16_draw'],'sleep_draw',8)
exec((OUT/'extension.py').read_text())
exec((OUT/'changes08.py').read_text())
exec((OUT/'changes09.py').read_text())
exec((OUT/'main35.py').read_text())
# Resolve and emit code, separate from the first laboratory and v34.
for p,label,n in c.fix:
 value=c.labels[label] if n==4 else c.labels[label]-(BASE+p)
 c.b[p:p+n]=value.to_bytes(n,'big',signed=n==2)
assert len(c.b)<0x5000 and set(source[BASE:BASE+len(c.b)])=={255}
r[BASE:BASE+len(c.b)]=c.b
# Assets generated exclusively from the supplied ROM's own font.
def pixel(b,x,y,v):
 i=x//8*512+y*4+x%8//2;shift=0 if x%2 else 4;b[i]=(b[i]&~(15<<shift))|(v<<shift)
def text(b,s,x,y):
 for j,ch in enumerate(s):
  tile=0 if ch==' ' else ord(ch)-21 if ch.isdigit() else ord(ch)-96
  for yy in range(8):
   for xx in range(8):
    v=source[0x30716+tile*32+yy*4+xx//2]>>(0 if xx%2 else 4)&15
    if v:pixel(b,x+j*8+xx,y+yy,15)
b=bytearray(0x3000);text(b,'mouse',72,24);text(b,'sensitivity',48,40);text(b,'low',24,88);text(b,'high',136,88);r[0x188000:0x18b000]=b
for value in range(9):
 b=bytearray(0x3000)
 for x in range(32,160):pixel(b,x,68,11)
 for i in range(9):
  for y in range(66,71):pixel(b,32+i*15,y,13)
 for y in range(64,72):
  for x in range(32+value*15,37+value*15):pixel(b,x,y,15)
 strip=b''.join(b[x*512+256:x*512+288] for x in range(4,20));r[0x18b000+value*512:0x18b000+(value+1)*512]=strip
r[0x18d000:0x18d012]=b''.join(v.to_bytes(2,'big') for v in [2,3,4,6,8,12,16,24,32])
rects=[(73,94),(97,118),(121,142),(145,166),(169,190),(193,204),(204,214),(217,238),(241,262)]
r[0x18d020:0x18d044]=b''.join(a.to_bytes(2,'big')+b.to_bytes(2,'big') for a,b in rects)
r[0x18d800:0x18d980]=b''.join(((2*round(math.atan((x-96)/256)*512/(2*math.pi)))&1022).to_bytes(2,'big') for x in range(192))
r[0x18da00:0x18dc90]=b''.join(((2*round(math.atan((57-y)/256)*512/(2*math.pi)))&1022).to_bytes(2,'big') for y in range(-100,228))
# One safe terminal near spawn permits testing the real interface without leaving the lab.
r[old['map']+(49-12)*80+16]=0xa1
name='Cyber-Cop_v35c';r[0x120:0x150]=name.encode().ljust(48,b' ');r[0x150:0x180]=name.encode().ljust(48,b' ')
r[0x18e:0x190]=(sum(int.from_bytes(r[i:i+2],'big') for i in range(0x200,len(r),2))&65535).to_bytes(2,'big')
(OUT/f'{name}.bin').write_bytes(r);(OUT/'symbols.json').write_text(json.dumps(c.labels,indent=2));print(name,len(c.b),'bytes of new code',hashlib.sha256(r).hexdigest())
