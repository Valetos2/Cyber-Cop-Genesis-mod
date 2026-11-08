"""Controlled native-renderer comparison, without modifying the ROM on disk."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
from PIL import Image

def capture():
 u=machine();w(u,S['CAMP'],1);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,0);run(u,0x4882);run(u,0x685e)
 u.mem_write(0xffff305a,bytes(4000));u.mem_write(0xffff2f50,bytes([255])*52)
 for x in range(25,56):w(u,0xffff305a+(49-27)*80+x,0x81,1)
 for x,raw in [(39,0x95),(40,0x82),(41,0x9c)]:w(u,0xffff305a+(49-26)*80+x,raw,1)
 # Wall near face Z=27*256; camera exactly six cells away.
 for a in [0xffff4412,0xffff261a]:
  w(u,a+8,40*256+128);w(u,a+12,21*256);w(u,a+10,270)
 for a,v,n in [(0xffff260c,0,2),(0xffff443a,0,2),(0xffff4444,0,2),(0xffff0107,255,1),(0xffff0108,255,1),(0xffff0120,0,1),(0xffff2706,0,1),(0xffff23b0,0xffff,2)]:w(u,a,v,n)
 run(u,0x4ae8);u.mem_write(0x150d8,bytes.fromhex('4e75'));w(u,0xffff444c,0xb426,4)
 for a in [0x3b46,0x3b7c,0xb428,0x3eb0,0x3e3a,0xdf6a,0x4584,0xcf72]:run(u,a)
 b=bytes(u.mem_read(0xffff8934,12288));bg=bytes(u.mem_read(0xffff2d40,512))
 colors=lambda base,n:[tuple(round(((rd(u,base+i*2)>>s)&14)*255/14) for s in [0,4,8]) for i in range(n)]
 p=colors(0xffff296c,16);bp=colors(0xffff298c,8);im=Image.new('RGB',(192,128))
 for y in range(128):
  ptr=int.from_bytes(R[0x6348+(127-y)*4:0x634c+(127-y)*4],'big')
  for x in range(192):
   off=ptr-0xffff8934+x//8*512+x%8//2;v=b[off]>>(4 if x%2==0 else 0)&15;im.putpixel((x,y),p[v] if v else bp[bg[y*4]&7])
 im.save('v36/barrels_lamp_native.png');im.resize((768,512),Image.Resampling.NEAREST).save('v36/barrels_lamp_6cells.png')
if __name__=='__main__':capture()
