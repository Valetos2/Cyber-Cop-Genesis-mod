from pathlib import Path
from PIL import Image,ImageDraw
import struct,hashlib,json
out=[]
for name,path,disk,table,index,paladdr in [('Mission','amiga3/mission.bin','amiga_research/mission.adf',0x62d0,15,0x5504),('Original','amiga3/d2.bin','amiga_research/d2.adf',0x6666,24,0x596c)]:
 b=Path(path).read_bytes();d=Path(disk).read_bytes();s,n=struct.unpack_from('>HH',b,table+index*4);raw=d[s*512:(s+n)*512];p=34;data=bytearray()
 while len(data)<32000:
  v=raw[p];p+=1
  if v<128:data+=raw[p:p+v+1];p+=v+1
  elif v>128:data+=bytes([raw[p]])*(257-v);p+=1
 pal=[tuple(((int.from_bytes(b[paladdr+2*i:paladdr+2*i+2],'big')>>s)&15)*17 for s in [8,4,0]) for i in range(16)]
 im=Image.new('RGB',(320,200))
 for y in range(200):
  for x in range(320):
   v=sum(((data[y*160+plane*40+x//8]>>(7-x%8))&1)<<plane for plane in range(4));im.putpixel((x,y),pal[v])
 im.save('v36/ending_'+name.lower()+'.png');out.append((name,im))
sheet=Image.new('RGB',(640,224));draw=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(out):sheet.paste(im,(i*320,24));draw.text((i*320+8,5),name,fill='white')
sheet.save('v36/ending_comparison.png')
