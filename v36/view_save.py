from pathlib import Path
from PIL import Image
b=Path('upload/Cyber-Cop_v36_test01.gs0').read_bytes();v=b[0x12478:0x22478];ram=b[0x2478:0x12478]
im=Image.new('RGB',(320,224))
for y in range(224):
 for x in range(320):
  o=0xe000+y//8*128+x//8*2;n=int.from_bytes(v[o:o+2],'big');xx=x%8;yy=y%8
  if n&0x800:xx=7-xx
  if n&0x1000:yy=7-yy
  o=(n&2047)*32+yy*4+xx//2;p=v[o]>>(0 if xx%2 else 4)&15;q=0x27ec+((n>>13)&3)*32+p*2;c=int.from_bytes(ram[q:q+2],'big');im.putpixel((x,y),tuple(((c>>s)&14)*255//14 for s in [0,4,8]))
im.resize((640,448),Image.Resampling.NEAREST).save('v36/user_save_plane.png')
print('oddtiles',[(x,y,hex(int.from_bytes(v[0xe000+y*128+x*2:0xe002+y*128+x*2],'big'))) for y in range(17,20) for x in range(25,32)])
