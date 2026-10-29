from pathlib import Path
import sys,json,hashlib
BASE=0x180000
OUT=Path(__file__).resolve().parent
SOURCE=Path(sys.argv[1]) if len(sys.argv)>1 else OUT.parent/'v34/Cyber-Cop_v34.bin'
SOURCE_HASH='3d8de656abcea8684ffd616812b173b28dfac7522b1953f974a4befa66e2e846'
class Code:
 def __init__(self):self.b=bytearray();self.labels={};self.fix=[]
 def label(self,n):self.labels[n]=BASE+len(self.b)
 def emit(self,h):self.b.extend(bytes.fromhex(h))
 def address(self,a):self.b.extend(a.to_bytes(4,'big'))
 def abs(self,op,a):self.emit(op);self.address(a)
 def jump(self,a):self.abs('4ef9',a)
 def call(self,a):self.abs('4eb9',a)
 def branch(self,op,label):self.emit(op);self.fix.append((len(self.b),label));self.emit('0000')
L={'settings_init': 1007616, 'buffer26_sample': 1020406, 'pad28_consume': 1022648, 'main_input': 983742};M=0xffff0180
# Independent laboratory overlay; main v34 bytes/resources remain intact.
def build(name,divide=0,smooth=False,pan=False):
 source=SOURCE.read_bytes();assert hashlib.sha256(source).hexdigest()==SOURCE_HASH,'Expected exact v34 source ROM'
 r=bytearray(source);c=Code()
 def word(a,v):c.emit('33fc'+f'{v&65535:04x}');c.address(a)
 def byte(a,v):c.emit('13fc'+f'{v&255:04x}');c.address(a)
 def hook(a,label,n=6):r[a:a+n]=bytes.fromhex('4ef9')+c.labels[label].to_bytes(4,'big')+bytes.fromhex('4e71')*((n-6)//2)
 def labelptr(op,label):c.emit(op);c.fix.append((len(c.b),('abs',label)));c.address(0)
 def safety():
  for a in [0xffff0104,0xffff0105,0xffff0106]:byte(a,255)
  for a in [0xffff2a26,0xffff2a28,0xffff2a2a,0xffff2a2c]:word(a,512)
  word(0xffff2a2e,127);word(0xffff2a30,127)
 c.label('boot');c.call(L['settings_init']);c.call(0x26b8);c.abs('43f9',0x1eb8);c.call(0x28d0);c.jump(0xa56);hook(0x386,'boot')
 # Replace only the map after native loading; retain rows and door setup.
 c.label('floor');c.call(0x4882);labelptr('41f9','map');c.abs('43f9',0xffff305a);c.emit('303c03e722d851c8fffc')
 c.call(0x4966);c.call(0x685e);c.emit('4e75')
 # 4838: two original JSR(pc) instructions, now JSR absolute and NOP.
 r[0x4838:0x4840]=bytes.fromhex('4eb9')+c.labels['floor'].to_bytes(4,'big')+bytes.fromhex('4e71')
 r[0x3fb2:0x3fb4]=bytes.fromhex('4e75') # no scripted hostile constructors
 c.label('start_world');safety();word(0xffff441a,14*256+128);word(0xffff441e,12*256+128);word(0xffff443a,0);word(0xffff260c,0);word(0xffff2622,14*256+128);word(0xffff2626,12*256+128);c.emit('33f9');c.address(0xffff441c);c.address(0xffff2624)
 c.abs('41f9',M);c.emit('701f421851c8fffc');word(M,0x4d53)
 byte(0xffff0107,0);byte(0xffff0108,0);byte(0xffff0120,0);byte(0xffff0014,0);byte(0xffff0015,0)
 c.emit(r[0x2074:0x207a].hex());c.jump(0x207a);hook(0x2074,'start_world')
 # Protocol step: all waits bounded by a shared 255-read retry budget.
 c.label('step');c.emit('10803200e24902410010') # write D0, D1 expected TL
 c.label('step_wait');c.emit('74001410360202430010b641');c.branch('6700','step_ok');c.emit('5347');c.branch('6600','step_wait');c.emit('4e75')
 c.label('step_ok');c.emit('0242000f4e75')
 def phase(v):
  c.emit('303c'+f'{v:04x}');c.call(c.labels['step']);c.emit('4a47');c.branch('6700','poll_bad')
 c.label('poll');c.emit('0c794d53');c.address(M);c.branch('6600','poll_return')
 # Z80 bus ownership is preserved, including failed acquisition.
 c.emit('7c00303c00ff');c.abs('4a39',0xa11100);c.branch('6700','bus_ready');c.emit('7c01');word(0xa11100,256)
 c.label('bus_wait')
 c.emit('08390000');c.address(0xa11100);c.branch('6700','bus_ready');c.emit('51c8');c.fix.append((len(c.b),'bus_wait'));c.emit('0000');c.branch('6000','poll_release')
 c.label('bus_ready');c.emit('3f06');c.abs('41f9',0xa10005);byte(0xa1000b,0x60);c.emit('3e3c00ff');phase(0x60);c.emit('4a42');c.branch('6600','poll_bad');phase(0x20);c.emit('0c42000b');c.branch('6600','poll_bad');phase(0);phase(0x20)
 phase(0);c.emit('3802') # D4 flags
 phase(0x20);c.abs('33c2',M+30) # temporary buttons
 phase(0);c.emit('3a02e94d');phase(0x20);c.emit('8a42') # X byte
 phase(0);c.emit('3c02e94e');phase(0x20);c.emit('8c42') # Y byte
 for reg,sign,over in [(5,0,2),(6,1,3)]:
  c.emit('0804'+f'{over:04x}');c.branch('6700',f'no_over{reg}');c.emit(f'{0x303c|(reg<<9):04x}0100')
  c.label(f'no_over{reg}');c.emit('0804'+f'{sign:04x}');c.branch('6700',f'signed{reg}');c.emit(f'{0x4a40|reg:04x}');c.branch('6600',f'nonzero{reg}');c.emit(f'{0x303c|(reg<<9):04x}ffff');c.branch('6000',f'signed{reg}');c.label(f'nonzero{reg}');c.emit(f'{0x0040|reg:04x}ff00');c.label(f'signed{reg}');c.emit(f'{0x48c0|reg:04x}')
 c.abs('dbb9',M+4);c.abs('ddb9',M+8) # add.l d5/d6 to accumulators
 c.abs('3439',M+30);c.abs('3039',M+12);c.emit('4640c042');c.abs('8179',M+16);c.abs('33c2',M+12);byte(M+18,255);c.branch('6000','poll_end')
 c.label('poll_bad');byte(M+18,0);word(M+12,0);word(M+16,0);c.abs('42b9',M+4);c.abs('42b9',M+8)
 c.label('poll_end');byte(0xa10005,0x60);c.emit('3c1f')
 c.label('poll_release');c.emit('4a46');c.branch('6700','poll_return');word(0xa11100,0)
 c.label('poll_return');c.emit('4e75')
 c.label('vblank');c.emit('40e748e7fffe');c.call(c.labels['poll']);c.emit('4cdf7fff46df');c.jump(L['buffer26_sample']);hook(0x17558,'vblank')
 # Consumer runs at a game-frame boundary, not in the middle of rendering.
 c.label('consume');c.call(L['pad28_consume']);c.emit('40e7007c070048e7fffe');safety()
 c.abs('4a39',M+18);c.branch('6700','consume_done')
 c.abs('3039',M+12);c.abs('8079',M+16);word(M+16,0);c.emit('7200')
 # Independent mouse mapping: L=fire B, R=context A, M=target C.
 for bit,mask in [(0,16),(1,64),(2,32)]:
  c.emit('0800'+f'{bit:04x}');c.branch('6700',f'btn{bit}');c.emit('0041'+f'{mask:04x}');c.label(f'btn{bit}')
 c.abs('3039',M+22);c.emit('4640');c.abs('c179',0xffff0006);c.abs('33c1',M+22);c.emit('4641');c.abs('c379',0xffff0004)
 # Left/right pad become strafe only in the world, while a mouse is detected.
 c.abs('4a39',0xffff270a);c.branch('6600','discard_motion')
 c.abs('3039',0xffff0004);c.emit('0240000c0c40000c');c.branch('6700','no_strafe');c.emit('08b90006');c.address(0xffff0005);c.label('no_strafe')
 c.abs('2039',M+4);c.abs('42b9',M+4)
 if smooth:
  c.abs('d1b9',M+24);c.abs('2039',M+24);c.emit('0c8000000001');c.branch('6700','smooth_step');c.emit('e280');c.label('smooth_step');c.abs('91b9',M+24)
 c.abs('3239',M+20);c.emit('48c1d081')
 # heading indexes a word sine table: retain one or two low fractional bits.
 shift=1+divide
 c.emit('22000281'+f'{(1<<shift)-1:08x}');c.abs('33c1',M+20)
 for _ in range(shift):c.emit('e280')
 c.emit('d040');c.abs('d179',0xffff260c);c.emit('027903fe');c.address(0xffff260c);c.abs('d179',0xffff443a);c.emit('027903fe');c.address(0xffff443a)
 if pan:
  c.abs('3039',M+10);c.abs('d179',M+28);c.abs('3039',M+28);c.emit('0c400018');c.branch('6f00','pan_low');c.emit('7018');c.label('pan_low');c.emit('0c40ffe8');c.branch('6c00','pan_store');c.emit('70e8');c.label('pan_store');c.abs('33c0',M+28)
 c.label('discard_motion');c.abs('42b9',M+4);c.abs('42b9',M+8)
 c.label('consume_done');c.emit('4cdf7fff46df4e75')
 # main input already calls pad28_consume in v34.
 at=L['main_input'];assert r[at:at+6]==bytes.fromhex('4eb9')+L['pad28_consume'].to_bytes(4,'big');r[at+2:at+6]=c.labels['consume'].to_bytes(4,'big')
 # Optional pan shifts final columns, preserving the rendered geometry and HUD.
 # It is a deliberately bounded screen pan, not perspective-correct pitch.
 if pan:
  c.label('pan_frame');c.call(0xcf72);c.emit('48e7fffe');c.abs('3039',M+28);c.branch('6700','pan_done');c.abs('4a39',0xffff270a);c.branch('6600','pan_done')
  # In-place, overlap-safe movement of each framebuffer column.
  c.abs('41f9',0xffff8934);c.emit('7c17')
  c.label('pan_col');c.emit('2248747f94404a40');c.branch('6b00','pan_negative')
  # Positive amount: image shifts toward larger framebuffer row indices.
  c.emit('43e802003a00')
  # A2 = end - shift*4; backward copy 128-shift longs.
  c.emit('24493a00e54d94c5')
  c.label('pan_pos_loop');c.emit('232251cafffc')
  c.emit('3a005345');c.label('pan_pos_fill');c.emit('42a151cdfffc');c.branch('6000','pan_next')
  c.label('pan_negative');c.emit('3a0044452448e54dd4c5') # abs shift bytes in D5
  c.emit('343c007fd440') # count =127+negative shift
  c.label('pan_neg_loop');c.emit('22da51cafffc');c.emit('3a0044455345');c.label('pan_neg_fill');c.emit('429951cdfffc')
  c.label('pan_next');c.emit('41e8020051ce');c.fix.append((len(c.b),'pan_col'));c.emit('0000')
  c.label('pan_done');c.emit('4cdf7fff4e75')
  # Native prologue moved to a trampoline after the complete payload.
  hook(0xcf72,'pan_frame')
  c.label('pan_aim');c.call(0x182010);c.emit('2f00');c.abs('3039',M+28);c.abs('9179',0xffff29b0);c.abs('9179',0xffff29c8);c.emit('201f4e75');hook(0xac1e,'pan_aim')
 # Map: four connected rooms and a bent corridor; no hostiles or alarm triggers.
 cells=bytearray([0x81]*4000)
 def put(x,z,v):cells[(49-z)*80+x]=v
 def room(x1,z1,x2,z2):
  for z in range(z1,z2+1):
   for x in range(x1,x2+1):put(x,z,0)
 room(10,10,18,18);room(20,10,28,18);room(10,22,18,30);room(30,24,38,32)
 room(14,19,14,21);room(19,14,19,14);room(29,14,34,14);room(34,15,34,23)
 for x,z in [(19,14),(14,20),(34,22)]:put(x,z,0x84)
 for x,z,v in [(12,16,0x95),(16,16,0x93),(23,16,0x99),(26,12,0x95),(12,27,0x8f),(16,28,0x94),(32,28,0x95),(36,30,0x99)]:put(x,z,v)
 # Only the room shells are walls: a solid-filled 80x50 map overloads
 # the original surface list when looking along the narrow corridor.
 original=bytes(cells)
 for z in range(1,49):
  for x in range(1,79):
   i=(49-z)*80+x
   if original[i]==0x81 and all(original[i+dz*80+dx]==0x81 for dz in [-1,0,1] for dx in [-1,0,1]):cells[i]=0
 c.label('map');c.b.extend(cells)
 for p,n in c.fix:
  if isinstance(n,tuple):c.b[p:p+4]=c.labels[n[1]].to_bytes(4,'big')
  else:c.b[p:p+2]=(c.labels[n]-(BASE+p)).to_bytes(2,'big',signed=True)
 assert len(c.b)<0x2000
 # map makes payload >4KB; trampoline intentionally moved beyond payload
 if pan:
  native=bytes(source[0xcf72:0xcf78]);r[0x182000:0x18200c]=native+bytes.fromhex('4ef9')+(0xcf78).to_bytes(4,'big');r[0x182010:0x18201c]=source[0xac1e:0xac24]+bytes.fromhex('4ef9')+(0xac24).to_bytes(4,'big');off=c.labels['pan_frame']-BASE+2;c.b[off:off+4]=(0x182000).to_bytes(4,'big')
 r[BASE:BASE+len(c.b)]=c.b
 r[0x120:0x150]=name.encode().ljust(48,b' ');r[0x150:0x180]=name.encode().ljust(48,b' ')
 r[0x18e:0x190]=(sum(int.from_bytes(r[i:i+2],'big') for i in range(0x200,len(r),2))&65535).to_bytes(2,'big')
 (OUT/(name+'.bin')).write_bytes(r);(OUT/(name+'.json')).write_text(json.dumps(c.labels,indent=2));return c.labels
if __name__=='__main__':
 for args in [('MouseLab_A_Direct',0,False,False),('MouseLab_B_Precise',1,False,False),('MouseLab_C_Pan',0,False,True),('MouseLab_D_Smooth',0,True,False)]:
  print(args[0]);build(*args)
