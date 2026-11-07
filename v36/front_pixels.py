from pathlib import Path
from PIL import Image
b=Path('v35c/Cyber-Cop_v35c.bin').read_bytes();v=bytearray(65536)
for addr,dest in [(0x30714,0),(0x4d066,0x500),(0x8e4fa,0x48c0),(0x39a9e,0x4ec0)]:
 n=int.from_bytes(b[addr:addr+2],'big');v[dest:dest+n]=b[addr+2:addr+2+n]
v[0xe000:0xf000]=b[0x51428:0x52428]
pix=[]
for y in range(224):
 for x in range(320):
  i=0xe000+(y//8*64+x//8)*2;t=int.from_bytes(v[i:i+2],'big');xx=x%8;yy=y%8
  if t&0x800:xx=7-xx
  if t&0x1000:yy=7-yy
  q=v[(t&0x7ff)*32+yy*4+xx//2];pix.append(q>>4 if xx%2==0 else q&15)
im=Image.new('P',(320,224));im.putdata(pix);im.putpalette([c for i in range(16) for c in (i*17,)*3]);im.crop((130,90,210,120)).resize((640,240)).save('v36/button_pixels.png')
for y in range(94,113):print(y,''.join(hex(pix[y*320+x])[2:] for x in range(138,202)))
