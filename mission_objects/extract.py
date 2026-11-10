from pathlib import Path
import struct,json
from PIL import Image,ImageDraw
b=Path('amiga3/mission.bin').read_bytes();disk=Path('amiga_research/mission.adf').read_bytes()
def w(a):return int.from_bytes(b[a:a+2],'big')
def l(a):return int.from_bytes(b[a:a+4],'big')
def resource(n):
 s,k=struct.unpack_from('>HH',b,0x62d0+n*4);raw=disk[s*512:(s+k)*512];p=34;out=bytearray()
 while p<len(raw) and len(out)<32000:
  v=raw[p];p+=1
  if v<128:out.extend(raw[p:p+v+1]);p+=v+1
  elif v>128:out.extend([raw[p]]*(257-v));p+=1
 return raw,bytes(out)
def sheet(n):
 raw,d=resource(n);h=len(d)//160;pal=[tuple(((int.from_bytes(raw[2+i*2:4+i*2],'big')>>s)&15)*17 for s in [8,4,0]) for i in range(16)]
 im=Image.new('RGBA',(320,h))
 for y in range(h):
  for x in range(320):
   v=sum(((d[y*160+p*40+x//8]>>(7-x%8))&1)<<p for p in range(4));im.putpixel((x,y),pal[v]+(255 if v else 0,))
 return im,pal,d
for n in [17,18,19,20,21,22,23,24]:
 im,pal,d=sheet(n);im.save(f'mission_objects/sheet_{n}.png');print(n,im.size,pal)
for f in [3,8,9]:
 a=l(0x1352a+f*4);lst=[]
 while (p:=l(a))<0x80000000:lst.append(hex(p));a+=4
 print('floor',f,lst)
