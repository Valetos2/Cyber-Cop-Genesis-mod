"""Work-in-progress integration. Not a release until remaining features/tests pass."""
from pathlib import Path
import json,struct,hashlib,sys
ROOT=Path(__file__).resolve().parent.parent;OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'mission_port36'))
from pending_fixes import darken_scanman_inset
src=(ROOT/'v35c/Cyber-Cop_v35c.bin').read_bytes();r=bytearray(src)+bytearray([255])*0x200000
S=json.loads((ROOT/'v35c/symbols.json').read_text());V=json.loads((ROOT/'v34/symbols.json').read_text())
darken_scanman_inset(r,S)
CAMP=0xffff0800;BASE=0x1f0000;DATA=0x220000
assert set(src[BASE:BASE+0x10000])=={255}
class Code:
 def __init__(self):self.b=bytearray();self.labels={};self.fix=[]
 def emit(self,h):self.b+=bytes.fromhex(h)
 def long(self,n):self.b+=struct.pack('>I',n)
 def label(self,n):assert n not in self.labels;self.labels[n]=BASE+len(self.b)
 def abs(self,op,n):self.emit(op);self.long(n)
 def call(self,n):self.abs('4eb9',n)
 def jump(self,n):self.abs('4ef9',n)
 def branch(self,op,label):self.emit(op);self.fix.append((len(self.b),label,2));self.emit('0000')
 def ref(self,op,label):self.emit(op);self.fix.append((len(self.b),label,4));self.long(0)
c=Code();assets={};pos=DATA

def asset(name,data):
 global pos
 if pos&1:pos+=1
 a=pos;r[a:a+len(data)]=data;pos+=len(data);assets[name]=a;return a

def patch(addr,label,n=6):r[addr:addr+n]=bytes.fromhex('4ef9')+struct.pack('>I',c.labels[label])+bytes.fromhex('4e71')*((n-6)//2)
def wi(addr,n):c.emit('33fc'+f'{n:04x}');c.long(addr)
def tstcamp():c.abs('4a79',CAMP)
def table_hook(addr,dest,name):
 """Replace an absolute LEA, preserving CCR and every other register."""
 op=src[addr:addr+2].hex();assert (int(op,16)&0xf1ff)==0x41f9,(hex(addr),op)
 c.label(name);c.emit('40e7');tstcamp();c.branch('6700',name+'_original');c.abs(op,dest);c.branch('6000',name+'_done');c.label(name+'_original');c.emit(src[addr:addr+6].hex());c.label(name+'_done');c.emit('46df');c.jump(addr+6);patch(addr,name)

# Logical IDs: original $0000..$000F, mission $0010..$001F; native floor remains0..15.
# Campaign is an independent namespace, never an out-of-range native table index.
c.label('reset36');c.abs('41f9',CAMP);c.emit('703f429851c8fffc');c.jump(S['reset35']);patch(0x332,'reset36')
# Native parser already verified checksum before this point. Extract the new bit
# before constructors/restore paths consume campaign-specific data.
c.label('decode36');c.emit('7000');c.abs('1039',0xffff25d8);c.emit('02400001');c.abs('33c0',CAMP);c.emit(src[0xf4a:0xf50].hex());c.jump(0xf50);patch(0xf4a,'decode36')
# Add campaign bit BEFORE the native checksum. Zero is byte-identical to v35c.
c.label('encode36');tstcamp();c.branch('6700','encode36_native');c.emit('08ed0000000a');c.label('encode36_native');c.emit('42407e0a');c.label('checksum36_loop');c.emit('d01d');c.branch('51cf','checksum36_loop');c.emit(src[0x92c6:0x92c8].hex());c.jump(0x92c8);patch(0x92bc,'encode36')

# Use the native planar decoder and its item/door/spawn processing unchanged.
levels=json.loads((ROOT/'amiga_research/maps.json').read_text())[1]
packed=bytearray(32000)
for lev in levels:
 f=lev['slot']
 for y in range(50):
  for x in range(80):
   v=int(lev['pixels'][y*80+x],16);xx=f%4*80+x;yy=f//4*50+y
   off=yy*160+(xx//16)*8;bit=15-xx%16
   for plane in range(4):
    if v>>plane&1:
     p=off+plane*2;val=int.from_bytes(packed[p:p+2],'big')|(1<<bit);packed[p:p+2]=val.to_bytes(2,'big')
mapaddr=asset('mission_planar_maps',packed);table_hook(0x48b2,mapaddr,'maps36')
luts=[asset('lut_'+str(i),bytes(lev['lut'][9:16])) for i,lev in enumerate(levels)]
table_hook(0x48ca,asset('mission_dictionary',b''.join(struct.pack('>I',p) for p in luts)),'dictionary36')
items=bytearray(768)
for i,lev in enumerate(levels):
 for j,(x,y,v) in enumerate(lev['items']):items[i*48+j*3:i*48+j*3+3]=bytes([x,49-y,v])
table_hook(0x2944,asset('mission_items',items),'items36')
# Every SRAM absolute address in native checkpoint routines is selected at runtime.
# Keep CC17/X21 original byte locations. Mission uses second 4096-byte slot,
# bus offset $2000 on odd-byte SRAM. Code remains below2MiB while SRAM is enabled.
# This code includes save/load/late restore; references outside those ranges untouched.
start=V['sram17_save'];end=V['resume17']
ranges=[(start,end),(V['save21'],V['restore21_late_end']+60)]
seen=set()
# Explicit opcodes whose long operand is an SRAM bus address.
for lo,hi in ranges:
 for p in range(lo,hi,2):
  if p in seen:continue
  op=int.from_bytes(src[p:p+2],'big');q=p+2
  if op in [0x13fc,0x33fc]:q=p+4
  if op not in [0x41f9,0x43f9,0x45f9,0x13c0,0x13c2,0x13fc,0x33fc,0x1039]:continue
  a=int.from_bytes(src[q:q+4],'big')
  if not 0x200001<=a<0x202000:continue
  n=q+4-p;name='sram36_'+hex(p)[2:];seen.add(p)
  c.label(name);c.emit('40e7');tstcamp();c.branch('6700',name+'_original')
  c.emit(src[p:q].hex());c.long(a+0x2000);c.branch('6000',name+'_done')
  c.label(name+'_original');c.emit(src[p:p+n].hex());c.label(name+'_done');c.emit('46df');c.jump(p+n);patch(p,name,n)

exec((OUT/'menus.py').read_text())
exec((OUT/'graphics.py').read_text())
exec((OUT/'audio.py').read_text())
exec((OUT/'actors.py').read_text())
exec((OUT/'world.py').read_text())
exec((OUT/'ending.py').read_text())
exec((OUT/'frontend_mouse.py').read_text())
exec((OUT/'lamps.py').read_text())
exec((OUT/'fixes02.py').read_text())
exec((OUT/'screens02.py').read_text())
exec((OUT/'lab02.py').read_text())
exec((OUT/'memorial02.py').read_text())
exec((OUT/'cosmetics03.py').read_text())

for p,name,n in c.fix:c.b[p:p+n]=(c.labels[name] if n==4 else c.labels[name]-(BASE+p)).to_bytes(n,'big',signed=n==2)
assert len(c.b)<0x10000
r[BASE:BASE+len(c.b)]=c.b
r[0x120:0x150]=b'Cyber-Cop v36 test03'.ljust(48,b' ')
r[0x150:0x180]=b'Cyber-Cop v36 test03'.ljust(48,b' ')
assert src[0xf9f85:0xf9f88]==b'v35';r[0xf9f85:0xf9f88]=b'v36'
r[0x1a4:0x1a8]=(len(r)-1).to_bytes(4,'big')
r[0x18e:0x190]=(sum(int.from_bytes(r[i:i+2],'big') for i in range(0x200,len(r),2))&65535).to_bytes(2,'big')
(OUT/'Cyber-Cop_v36_WORK_IN_PROGRESS.bin').write_bytes(r)
(OUT/'symbols.json').write_text(json.dumps(dict(c.labels,**assets,CAMP=CAMP),indent=2))
print('WIP built',len(r),'code',len(c.b),'assets',pos-DATA,'SRAM patches',len(seen))
