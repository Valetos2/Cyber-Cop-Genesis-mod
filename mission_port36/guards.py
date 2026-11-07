import sys,struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'mission_objects')
from render import indexed,color,b,l,w
out=Path('mission_port36/guards');out.mkdir(exist_ok=True)
im=indexed(7);color(im,6).save(out/'amiga_sheet.png')
print('guardframes',[hex(l(0xe8a6+i*4)) for i in range(24)])
raw=im.tobytes()
for p in Path('next/dos').rglob('CORPRTN*.DAT'):
 d=p.read_bytes();print(p.name,len(d),d[:16].hex())
guard=im.crop((128,0,160,80));color(guard,6).save(out/'Amiga_front.png')
# Locate exact indexed pixels regardless of offsets or palette in DOS assets.
variants={}
for rev in [False,True]:
 for trans in [False,True]:
  g=guard.transpose(Image.Transpose.TRANSPOSE) if trans else guard
  arr=list(g.getdata());p=bytes((arr[i+1]<<4|arr[i]) if rev else (arr[i]<<4|arr[i+1]) for i in range(0,len(arr),2))
  variants[(rev,trans)]=p
for file in Path('next/dos').rglob('CORPRTN*.DAT'):
 d=file.read_bytes()
 for k,p in variants.items():
  # Nonempty head row, first 14 bytes long.
  for q in range(0,min(len(p),200),16):
   s=p[q:q+16]
   if len(set(s))<5:continue
   off=d.find(s)
   if off>=0:print('DOSmatch',file.name,k,q,hex(off));break
# ST packed sheets may retain the complete Amiga resource.
from extract import resource
packed,_=resource(7)
for file in Path('st2/files').iterdir():
 d=file.read_bytes();off=d.find(packed[34:234])
 if off>=0:print('STmatch',file.name,hex(off))
d=next(Path('next/dos').rglob('CORPRTNC.DAT')).read_bytes();start=0x1450
p=variants[(False,True)];print('DOSfullsame',d[start:start+len(p)]==p, 'diff',sum(x!=y for x,y in zip(d[start:start+len(p)],p)))
g=Image.new('P',(32,80));g.putdata([((d[start+x*40+y//2]>>(4 if y%2==0 else 0))&15) for y in range(80) for x in range(32)])
color(g,6).save(out/'DOS_front_common_palette.png')
sys.path.insert(0,'atlas36');import sprites
pgen=sprites.pal(sprites.long(0x10b8c+6*4));gen=sprites.part(80,32,80,pgen);gen.save(out/'Genesis_front.png')
