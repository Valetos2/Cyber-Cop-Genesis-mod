from capstone import Cs,CS_ARCH_M68K,CS_MODE_BIG_ENDIAN,CS_MODE_M68K_000
import re
md=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000)
def label_native(p):return 'robot36_'+hex(p)[2:]
# Relocate the existing 1A behaviour into independent robot callbacks. No original
# enemy callback, attack table, or constructor is overwritten.
lo,hi=0xc8a4,0xca60
for ins in md.disasm(src[lo:hi],lo):
 p=ins.address;b=bytearray(ins.bytes);op=int.from_bytes(b[:2],'big');c.label(label_native(p))
 if p in (0xc996,0xca20):c.call(c.labels['robot_stop_sound36'])
 if op>>12==6:
  target=int(re.search(r'\$([0-9a-f]+)',ins.op_str)[1],16)
  c.branch(f'{op&0xff00:04x}',label_native(target))
 elif op in (0x4eba,0x4efa) or (op&0xf1ff)==0x41fa:
  target=p+2+int.from_bytes(b[2:4],'big',signed=True)
  newop=op-1 # PC-relative d16 -> absolute long EA ($3A->$39)
  if lo<=target<0xca72:c.ref(f'{newop:04x}',label_native(target))
  else:c.abs(f'{newop:04x}',c.labels['robot_walk36'] if target==0xc6f0 else target)
 elif len(b)>=6 and lo<=int.from_bytes(b[2:6],'big')<hi and op in (0x217c,0x237c):
  c.ref(b[:2].hex(),label_native(int.from_bytes(b[2:6],'big')));c.emit(b[6:].hex())
 else:
  if p==0xca32:b[2:4]=struct.pack('>H',robot_death[0])
  if op==0x4eb9 and b[2:6]==bytes.fromhex('000150d8'):b[2:6]=struct.pack('>I',c.labels['robot_attack_event36'])
  c.emit(b.hex())
c.label(label_native(0x68d8));c.jump(0x68d8)
c.label(label_native(0xca60));c.emit(struct.pack('>3H',*robot_death).hex())
c.label(label_native(0xca66));c.emit(struct.pack('>6H',*[robot_attack[i] for i in (0,1,2,1,2,0)]).hex())

def fieldw(reg,off,value):c.emit(f'{0x317c+(reg<<9):04x}{value:04x}{off:04x}')
def fieldl(reg,off,value):c.emit(f'{0x217c+(reg<<9):04x}');c.long(value);c.emit(f'{off:04x}')
c.label('robot_constructor36');c.call(0x4144);c.branch('6b00','robot_ctor_failed36')
fieldw(0,2,0x801d);fieldw(0,0x1e,robot_frames[0]);fieldw(0,0x20,robot_frames[0]);fieldl(0,0x3a,c.labels[label_native(0xc8a4)]);fieldl(0,0x4a,c.labels[label_native(0xca1a)]);c.emit('7000')
c.label('robot_ctor_failed36');c.emit('4e75')
c.label('robot_spawn36');c.call(0xaae6);c.emit('0c12008e');c.branch('6600','robot_spawn_done36');c.call(c.labels['robot_constructor36']);c.branch('6600','robot_spawn_done36')
fieldw(0,0x28,0x200);fieldw(0,0x2a,0x2000);c.ref('217c','robot_spawn_walk36');c.emit('003a');fieldl(0,0x4a,0xb426);fieldw(0,0x38,40)
c.label('robot_spawn_done36');c.emit('4e75')
c.label('robot_spawn_walk36');c.emit('53680038');c.branch('6b00','robot_spawn_ready36');c.call(c.labels['robot_walk36']);c.call(0xbd66);c.call(0xaee2);c.jump(0xbd5e)
c.label('robot_spawn_ready36');fieldw(0,0x38,0);fieldl(0,0x3a,c.labels[label_native(0xc8a4)]);fieldl(0,0x4a,c.labels[label_native(0xca1a)]);c.jump(0xbd5e)

# New map codes are free dispatch entries in Genesis ($1C..$1E). They are gated
# to Mission so unused original codes retain their original no-op behaviour.
strides={h:asset('sprite_stride_'+str(h),struct.pack('>64H',*[i*h for i in range(64)])) for h in (9,19,42)}
for raw,name,idx,h,small in [(0x1c,'barrel36',barrel,42,None),(0x1d,'stool_blue36',stool_blue,19,stool_blue_small),(0x1e,'stool_green36',stool_green,19,stool_green_small)]:
 c.label(name);tstcamp();c.branch('6700',name+'_done');c.call(0xb474)
 fieldw(1,2,7 if raw==0x1c else 5);fieldl(1,4,0xe6e0);fieldw(1,0x12,32);fieldw(1,0x1c,1000);fieldw(1,0x24,0);fieldw(1,0x28,0x200);fieldl(1,0x3a,0xbd62)
 if small is not None:
  c.emit('08000006');c.branch('6700',name+'_large');fieldw(1,0xa,18);fieldw(1,0x14,9);fieldw(1,0x20,small);fieldl(1,0x4e,strides[9]);c.branch('6000',name+'_done');c.label(name+'_large')
 fieldw(1,0xa,h*2);fieldw(1,0x14,h);fieldw(1,0x20,idx);fieldl(1,0x4e,strides[h])
 if raw==0x1c:fieldw(1,0x2c,64);fieldw(1,0x2e,84)
 c.label(name+'_done');c.emit('4e75');r[0x6588+raw*4:0x658c+raw*4]=struct.pack('>I',c.labels[name])

# Native Genesis function equivalents for Mission floor spawns and initial actors.
spawnmap={0x68c0:0x3fde,0x69ac:0x40de,0x6bd0:0x42c8,0x6cda:0x43d8,0xd31e:0xb426,0x69e0:c.labels['robot_spawn36']}
rows=[]
for f in range(16):
 period,limit,*funcs=struct.unpack_from('>HHIII',A,0x130a8+f*16)
 rows.append(struct.pack('>HHIII',period,limit,*[spawnmap[x] for x in funcs]))
table_hook(0x4a0e,asset('mission_spawns',b''.join(rows)),'spawns36')
constructors={0x6918:0x4038,0x6a5a:0x4144,0x6c38:0x432e,0x6d3a:0x4438,0x6b58:0x4250}
extras={0x6986:0x40b8,0x6cca:0x43c8,0x6db2:0x44ba}
ptrs=[]
for f in range(16):
 p=al(0x175de+f*4);data=bytearray()
 while aw(p)!=65535:
  x,z,ctor,extra=struct.unpack_from('>HHII',A,p);p+=12
  data+=struct.pack('>HHII',x,z,constructors[ctor],extras[extra])
 data+=b'\xff\xff';ptrs.append(asset('mission_enemies_'+str(f),data))
table_hook(0x3fbc,asset('mission_enemies',struct.pack('>16I',*ptrs)),'enemies36')
