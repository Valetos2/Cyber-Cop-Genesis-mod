from pathlib import Path
from PIL import Image
b=Path('upload/Cyber-Cop_v36_test01.gs0').read_bytes();v=b[0x12478:0x22478];ram=b[0x2478:0x12478]
colors=[]
for q in range(64):
 c=int.from_bytes(ram[0x28ac+q*2:0x28ae+q*2],'big');colors.append(tuple(((c>>s)&14)*255//14 for s in [0,4,8]))
for name,base in [('a',0xe000),('b',0xc000)]:
 im=Image.new('RGB',(320,224))
 for y in range(224):
  for x in range(320):
   o=base+y//8*128+x//8*2;n=int.from_bytes(v[o:o+2],'big');xx=x%8;yy=y%8
   if n&0x800:xx=7-xx
   if n&0x1000:yy=7-yy
   o=(n&2047)*32+yy*4+xx//2;p=v[o]>>(0 if xx%2 else 4)&15;im.putpixel((x,y),colors[(n>>13&3)*16+p])
 im.resize((640,448)).save('v36/gst_'+name+'.png')
