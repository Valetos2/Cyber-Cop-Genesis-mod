exec(open('v36/test_core.py').read().split('levels=json')[0])
from PIL import Image,ImageDraw

def render(raw,name,robot=False):
 u=machine();w(u,S['CAMP'],1);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,9);run(u,0x4882);run(u,0x685e);run(u,0x50f4)
 u.mem_write(0xffff305a,bytes(4000));u.mem_write(0xffff2f50,bytes([255])*52)
 for k in range(-3,4):w(u,0xffff305a+(49-26)*80+40+k,0x81,1)
 w(u,0xffff305a+(49-24)*80+40,raw,1)
 for a in [0xffff4412,0xffff261a]:
  w(u,a+8,40*256+128);w(u,a+12,20*256+128);w(u,a+10,270)
 w(u,0xffff260c,0);w(u,0xffff443a,0);w(u,0xffff4444,0);w(u,0xffff0107,255,1);w(u,0xffff0108,255,1);w(u,0xffff0120,0,1);w(u,0xffff2706,0,1)
 w(u,0xffff23b0,0xffff);run(u,0x4ae8);u.mem_write(0x150d8,bytes.fromhex('4e75'));w(u,0xffff4412+0x3a,0xb426,4)
 if robot:
  u.reg_write(UC_M68K_REG_D0,40*256+128);u.reg_write(UC_M68K_REG_D2,24*256+128);run(u,S['robot_constructor36']);a=u.reg_read(UC_M68K_REG_A0);w(u,a+0x28,0x200);w(u,a+0x3a,0xbd5e,4);w(u,a+0x20,257)
 for a in [0x3b46,0x3b7c,0xb428,0x3eb0,0x3e3a,0xdf6a,0x4584,0xcf72]:run(u,a)
 b=bytes(u.mem_read(0xffff8934,0x3000));p=[tuple(round(((rd(u,0xffff296c+i*2)>>s)&14)*255/14) for s in [0,4,8]) for i in range(16)];bg=bytes(u.mem_read(0xffff2d40,512));bp=[tuple(round(((rd(u,0xffff298c+i*2)>>s)&14)*255/14) for s in [0,4,8]) for i in range(8)]
 im=Image.new('RGB',(192,128))
 for y in range(128):
  ptr=int.from_bytes(R[0x6348+(127-y)*4:0x634c+(127-y)*4],'big')
  for x in range(192):
   off=ptr-0xffff8934+x//8*512+x%8//2;v=b[off]>>(4 if x%2==0 else 0)&15;im.putpixel((x,y),p[v] if v else bp[bg[y*4]&7])
 im.resize((576,384),Image.Resampling.NEAREST).save('v36/'+name+'.png');return im
for raw,name,robot in [(0x9c,'barrel',False),(0x9d,'stool_blue',False),(0x9e,'stool_green',False),(0,'robot',True)]:render(raw,name,robot)
print('Rendered four scenes with native Genesis renderer')
