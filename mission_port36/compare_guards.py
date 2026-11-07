from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys,struct
sys.path.insert(0,'mission_objects');from extract import resource,b,l,w
out=Path('mission_port36/guards')
def decode(raw):
 if raw[:2]==b'\0\0':return raw[34:32034]
 p=34;d=bytearray()
 while p<len(raw) and len(d)<32000:
  n=raw[p];p+=1
  if n<128:d+=raw[p:p+n+1];p+=n+1
  elif n>128:d+=bytes([raw[p]])*(257-n);p+=1
 return d[:32000]
def pix(d):
 im=Image.new('P',(320,200));im.putdata([sum(((d[y*160+k*40+x//8]>>(7-x%8))&1)<<k for k in range(4)) for y in range(200) for x in range(320)]);return im
raw,d=resource(7);am=pix(d).crop((128,0,160,80));st=None;best=999999
for f in Path('mission_port36/st_resources').glob('*.bin'):
 dd=decode(f.read_bytes())
 if len(dd)!=32000:continue
 im=pix(dd);g=im.crop((128,0,160,80));err=sum(x!=y for x,y in zip(g.tobytes(),am.tobytes()))
 if err<best:best=err;st=g;st_name=f.name
assert st is not None;print('ST best',st_name,best)
rawdos=next(Path('next/dos').rglob('CORPRTNC.DAT')).read_bytes();dos=Image.new('P',(32,80));dos.putdata([((rawdos[0x1450+x*38+y//2]>>(4 if y%2==0 else 0))&15) if y<76 else 0 for y in range(80) for x in range(32)])
print('ST DOS differences',sum(x!=y for x,y in zip(dos.tobytes(),st.tobytes())))
print('DOS diff',sum(x!=y for x,y in zip(dos.tobytes(),am.tobytes())))
a=l(0x131e8+6*4)+16;pal=[tuple(((w(a+i*2)>>s)&15)*17 for s in [8,4,0]) for i in range(16)]
def normalize(im):
 r=Image.new('P',im.size);r.putdata([{8:1,9:8}.get(v,v) for v in im.tobytes()]);return r
st=normalize(st);dos=normalize(dos)
print('Normalized Amiga/ST pixel differences',sum(x!=y for x,y in zip(am.tobytes(),st.tobytes())))
print('Normalized Amiga/DOS pixel differences',sum(x!=y for x,y in zip(am.tobytes(),dos.tobytes())))
def color(im):
 r=Image.new('RGBA',im.size);r.putdata([pal[v]+(0 if v==0 else 255,) for v in im.tobytes()]);return r
sys.path.insert(0,'atlas36');import sprites
gen=sprites.part(80,32,80,sprites.pal(sprites.long(0x10b8c+6*4)))
canvas=Image.new('RGB',(640,410),(70,70,70));dr=ImageDraw.Draw(canvas);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
for i,(name,im) in enumerate([('Amiga',color(am)),('Atari ST',color(st)),('DOS',color(dos)),('Genesis',gen)]):
 im.save(out/(name.replace(' ','_')+'_front.png'));im=im.resize((128,320),Image.Resampling.NEAREST);canvas.paste(im,(i*160+16,16),im);dr.text((i*160+35,345),name,font=font,fill='white')
dr.text((22,383),'Amiga / ST / DOS: common palette, black normalized',font=font,fill='white')
canvas.save(out/'guard_comparison.png')
