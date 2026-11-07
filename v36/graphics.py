"""Convert Mission planar resources to the existing Genesis column-pair format."""
A=(ROOT/'amiga3/mission.bin').read_bytes();DISK=(ROOT/'amiga_research/mission.adf').read_bytes()
def aw(a):return int.from_bytes(A[a:a+2],'big')
def al(a):return int.from_bytes(A[a:a+4],'big')
def mdcolor(word):
 rgb=[round(((word>>s)&15)*7/15)*2 for s in (8,4,0)]
 return rgb[0]|rgb[1]<<4|rgb[2]<<8
palettes=[];amiga_palettes=[]
for f in range(16):
 ap=[aw(al(0x131e8+f*4)+i*2) for i in range(35)];amiga_palettes.append(ap[8:24])
 # Retain Genesis semantic indices and neutral wall shades2..7. Amiga has
 # independent wall/sprite palettes; Genesis world shares one16-color palette.
 colors=[0,0xf00]+ap[2:8]+[ap[9],0]+ap[18:24]
 colors += [ap[i] for i in (24,26,28,29,30,32,34)]
 native=[mdcolor(x) for x in colors]
 # Use the corresponding Genesis background where Amiga's gray bands merge
 # with gray walls. If that original band is also gray, use original floor0.
 oldpal=struct.unpack_from('>23H',src,struct.unpack_from('>I',src,0x10b8c+f*4)[0])
 fallback=struct.unpack_from('>23H',src,struct.unpack_from('>I',src,0x10b8c)[0])
 def gray(v):return (v&15)==((v>>4)&15)==((v>>8)&15)
 for lo,hi in [(16,19),(20,23)]:
  if all(gray(v) for v in native[lo:hi]):
   replacement=oldpal[lo:hi]
   if all(gray(v) for v in replacement):replacement=fallback[lo:hi]
   native[lo:hi]=replacement
 palettes.append(native)
ptrs=[asset('mission_palette_'+str(f),struct.pack('>23H',*p)) for f,p in enumerate(palettes)]
table_hook(0x50fe,asset('mission_palettes',struct.pack('>16I',*ptrs)),'palettes36')

def indices(res):
 sector,count=struct.unpack_from('>HH',A,0x62d0+res*4);raw=DISK[sector*512:(sector+count)*512];out=bytearray();p=34
 while len(out)<32000:
  n=raw[p];p+=1
  if n<128:out+=raw[p:p+n+1];p+=n+1
  elif n>128:out+=bytes([raw[p]])*(257-n);p+=1
 assert len(out)==32000
 return [[sum(((out[y*160+plane*40+x//8]>>(7-x%8))&1)<<plane for plane in range(4)) for x in range(320)] for y in range(200)]
sheets={n:indices(n) for n in (18,21,22,23,24)}
sprite_offsets=list(struct.unpack_from('>253I',src,0x8eafc))
# Index252 is the original final entry, not a sentinel: no original code is changed.
# New sprites begin at253 and retain the native data base for all original offsets.
sprite_specs={}
def sprite(name,res,x,y,w,h):
 image=sheets[res];assert x+w<=320 and y+h<=200
 # Native renderer indexes shaded pairs using each sprite's actual height.
 # The fixed mapping keeps frame indices independent of the current floor palette.
 mapping=[0,8,2,3,4,5,6,7,9,9,10,11,12,13,14,15]
 stride=100 if name.startswith('robot_') else h+2
 data=bytes((mapping[image[yy][xx]]<<4)|mapping[image[yy][xx+1]] if yy<y+h else 0 for xx in range(x,x+w,2) for yy in range(y,y+stride))
 idx=len(sprite_offsets);addr=asset(name,data);sprite_offsets.append(addr-0x8eef0);sprite_specs[name]={'index':idx,'resource':res,'crop':[x,y,w,h],'address':addr}
 return idx
robot_frames=[]
for n in range(24):
 address=al(0xec74+n*4)
 for res,base in [(22,0x4f4a0),(23,0x477a0),(24,0x3faa0)]:
  if base<=address<base+32000:
   y,xb=divmod(address-base,160);robot_frames.append(sprite('robot_walk_'+str(n),res,xb*2,y,64,98));break
 else:raise AssertionError(hex(address))
robot_attack=[sprite('robot_attack_'+str(n),24,x,y,64,98) for n,(x,y) in enumerate([(256,0),(64,100),(0,100)])]
robot_death=[sprite('robot_death_'+str(n),24,x,100,64,98) for n,x in enumerate([128,192,256])]
barrel=sprite('barrel',21,288,0,32,42)
stool_blue=sprite('stool_blue',21,0,12,32,19)
stool_blue_small=sprite('stool_blue_small',21,32,21,32,9)
stool_green=sprite('stool_green',18,288,0,32,19)
stool_green_small=sprite('stool_green_small',18,288,31,32,9)
sprite_table=asset('sprite_offsets36',struct.pack('>'+str(len(sprite_offsets))+'I',*sprite_offsets))
r[0xe826:0xe82a]=struct.pack('>I',sprite_table)
hitflags=bytearray(src[0x10872:0x10872+253])+bytearray(len(sprite_offsets)-253)
for idx in (stool_blue,stool_blue_small,stool_green,stool_green_small):hitflags[idx]=255
r[0xec54:0xec58]=struct.pack('>I',asset('sprite_hitflags36',hitflags))
(OUT/'sprites.json').write_text(json.dumps(sprite_specs,indent=2))
