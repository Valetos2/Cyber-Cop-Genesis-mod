"""Render local savestate RAM using native frame routines; no inputs are bundled."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
from PIL import Image,ImageDraw

def render_save(path,angle=None,patcher=None):
 u=machine();u.mem_write(0xffff0000,Path(path).read_bytes()[0x2478:0x12478]);u.mem_write(0x150d8,bytes.fromhex('4e75'))
 if angle is not None:w(u,0xffff260c,angle);w(u,0xffff443a,angle)
 if patcher:patcher(u)
 for a in [0x3b46,0x3b7c,0xb428,0x3eb0,0x3e3a,0xdf6a,0x4584,0xcf72]:run(u,a)
 im=Image.new('RGB',(192,128));b=bytes(u.mem_read(0xffff8934,12288));bg=bytes(u.mem_read(0xffff2d40,512))
 colors=lambda base,n:[tuple(round(((rd(u,base+i*2)>>s)&14)*255/14) for s in [0,4,8]) for i in range(n)]
 p=colors(0xffff296c,16);bp=colors(0xffff298c,8)
 for y in range(128):
  ptr=int.from_bytes(R[0x6348+(127-y)*4:0x634c+(127-y)*4],'big')
  for x in range(192):
   off=ptr-0xffff8934+x//8*512+x%8//2;v=b[off]>>(4 if x%2==0 else 0)&15;im.putpixel((x,y),p[v] if v else bp[bg[y*4]&7])
 return im,u
if __name__=='__main__':
 out=Image.new('RGB',(192*4,144*3));d=ImageDraw.Draw(out)
 for i,angle in enumerate(range(288,480,16)):
  im,u=render_save('upload/Cyber-Cop_v36_test03.gs2',angle);x=i%4*192;y=i//4*144;out.paste(im,(x,y));d.text((x,y+128),str(angle),fill='white')
 out.save('v36/wall_gs2_test04.png')
