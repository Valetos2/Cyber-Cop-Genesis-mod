from PIL import Image,ImageDraw
from pathlib import Path
r=Path('v25/Cyber-Cop_v25.bin').read_bytes();out=Image.new('RGB',(1000,500),'#222');d=ImageDraw.Draw(out)
for j,(idx,lab) in enumerate([(175,'13'),(9,'0A'),(0,'09')]):
 a=0x8eef0+int.from_bytes(r[0x8eafc+idx*4:0x8eb00+idx*4],'big');b=0x8eef0+int.from_bytes(r[0x8eafc+(idx+1)*4:0x8eb04+idx*4],'big');h=(b-a)//16
 im=Image.new('RGB',(32,h))
 for x in range(32):
  for y in range(h):
   v=r[a+(x//2)*h+y]>>(4 if x%2==0 else 0)&15;im.putpixel((x,y),(v*17,)*3)
 im=im.resize((96,h*3));x=(j%8)*125;y=24;out.paste(im,(x,y));d.text((x,5),lab,fill='white')
out.save('atlas/object_check.png')
