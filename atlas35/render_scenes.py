exec(open('v30/common.py').read())
import sys
sys.path.insert(0,'atlas35')
from sprites import pal,long,pngdata
from PIL import ImageDraw

def scene(raw,name):
 u=machine();run(u,0x2360);run(u,0x2944);w(u,0xffff2606,2 if raw==24 else 0);run(u,0x4882);run(u,0x685e)
 u.mem_write(0xffff305a,bytes(4000));u.mem_write(0xffff2f50,bytes([255])*52)
 if raw not in [24,0x4b]:
  for k in range(-3,4):
   x,z=(40,26+k) if raw&63==36 else (40+k,26)
   w(u,0xffff305a+(49-z)*80+x,0x81,1)
 w(u,0xffff305a+(49-26)*80+40,raw,1)
 if raw==0x4b:
  for x in [39,40,41]:w(u,0xffff305a+(49-26)*80+x,raw,1)
  u.reg_write(UC_M68K_REG_D0,1);run(u,0x5122)
 for a in [0xffff4412,0xffff261a]:
  w(u,a+8,(34 if raw&63==36 else 40)*256+128);w(u,a+12,(26 if raw&63==36 else (18 if raw==0x4b else 23 if raw==24 else 20))*256+128);w(u,a+10,220 if raw==0x4b else 110 if raw==24 else 270)
 w(u,0xffff260c,256 if raw&63==36 else 0);w(u,0xffff443a,0);w(u,0xffff4444,0);w(u,0xffff0107,255 if raw not in [24,0x4b] else 0,1);w(u,0xffff0108,255 if raw not in [24,0x4b] else 0,1);w(u,0xffff0120,0,1);w(u,0xffff2706,0,1)
 w(u,0xffff23b0,0xffff);run(u,0x4ae8)
 u.mem_write(0x150d8,bytes.fromhex('4e75'));w(u,0xffff4412+0x3a,0xb426,4)
 beam_quads=[]
 def capture_quad(uc,pc,size,data):
  if raw==0x4b and pc==0xe4d0:
   b=bytes(uc.mem_read(0xffff2458,16));beam_quads.append([(int.from_bytes(b[i:i+2],'big',signed=True),127-int.from_bytes(b[i+2:i+4],'big',signed=True)) for i in range(0,16,4)])
 u.hook_add(UC_HOOK_CODE,capture_quad)
 for a in [0x3b46,0x3b7c,0xb428,0x3eb0,0x3e3a,0xdf6a,0x4584,0xcf72]:run(u,a)
 b=bytes(u.mem_read(0xffff8934,0x3000));palette_addr=long(0x10b8c+(8 if raw==24 else 0));p=pal(palette_addr);bg=bytes(u.mem_read(0xffff2d40,512));bp=[(0,0,0)]+pal(palette_addr+32)[:7];im=Image.new('RGB',(192,128))
 for y in range(128):
  ptr=int.from_bytes(ROM[0x6348+(127-y)*4:0x634c+(127-y)*4],'big')
  for x in range(192):
   off=ptr-0xffff8934+x//8*512+x%8//2;v=b[off]>>(4 if x%2==0 else 0)&15;im.putpixel((x,y),p[v] if v else bp[bg[y*4] & 7])
 
 if raw==0x4b:
  vp=[tuple(round(((rd(u,0xffff284c+i*2)>>s)&14)*255/14) for s in [0,4,8]) for i in range(16)]
  for y in range(128):
   ptr=int.from_bytes(ROM[0x6348+(127-y)*4:0x634c+(127-y)*4],'big')
   for x in range(192):
    off=ptr-0xffff8934+x//8*512+x%8//2;v=b[off]>>(4 if x%2==0 else 0)&15
    im.putpixel((x,y),vp[v] if v else tuple(round(((rd(u,0xffff288c+(bg[y*4]&7)*2)>>s)&14)*255/14) for s in [0,4,8]))
 
 if raw==0x4b:
  # Geometry and palette come from native routines; rasterize the three captured
  # quads explicitly to make this static preview legible: select bright native phases for all three cells.
  for y in range(128):
   bgcol=tuple(round(((rd(u,0xffff288c+(bg[y*4]&7)*2)>>s)&14)*255/14) for s in [0,4,8])
   for x in range(192):im.putpixel((x,y),bgcol)
  draw=ImageDraw.Draw(im)
  assert len(beam_quads)==3
  for i,q in enumerate(beam_quads):draw.polygon([q[j] for j in [0,1,3,2]],fill=vp[[14,15,14][i]])
 im.save('atlas35/'+name+'_full.png');im=im.crop((32,0,160,128));im.resize((512,512),Image.Resampling.NEAREST).save('atlas35/'+name+'.png');return im
if __name__=='__main__':
 for raw,name in [(0x84,'door'),(0xa2,'locked_door'),(0xa4,'elevator_door'),(24,'alarm_floor'),(0x4b,'laser_beam')]:
  im=scene(raw,name);print(name,im.getbbox())
