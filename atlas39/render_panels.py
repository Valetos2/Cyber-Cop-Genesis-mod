exec(open('v36/test_core.py').read().split('levels=json')[0])
from PIL import Image
import base64,io
ROM=R
def ret(u):
 sp=u.reg_read(UC_M68K_REG_A7);u.reg_write(UC_M68K_REG_PC,rd(u,sp,4));u.reg_write(UC_M68K_REG_A7,sp+4)
def pngdata(im):
 b=io.BytesIO();im.save(b,format='PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
def capture(kind,floor=0,code=None,access=0):
 u=machine();w(u,S['CAMP'],1);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,floor);run(u,0x4882);run(u,0x685e)
 u.mem_write(0xffff2f50,bytes([255])*52);w(u,0xffff0004,255);w(u,0xffff26bc,access*32);w(u,0xffff29ba,0);w(u,0xffff29bc,0);w(u,0xffff216e,0);w(u,0xffff2170,0);u.mem_write(0xffff2150,bytes(28));w(u,0xffff2701,0,1)
 def hk(uc,a,s,d):
  if a in [0x1646,0x2930,0x4d18,0x150b4,0x150d8,0x8f4a,0x8f24,0x9342]:ret(uc)
 u.hook_add(UC_HOOK_CODE,hk)
 if kind=='terminal':
  run(u,0x7b86);w(u,0xffff26eb,255,1);run(u,0x7c42);run(u,0x38c8);run(u,0x7df4)
 elif kind=='lift_inside':
  run(u,0x8c78)
  floor_code=rd(u,0xffff260a)
  w(u,0xffff218e,floor_code);w(u,0xffff2190,floor_code)
  run(u,0x8ec8)
 elif kind=='scanman':
  u.reg_write(UC_M68K_REG_D7,0);run(u,0x8720)
 elif kind=='keypad':
  run(u,0x943e)
  if code is not None:
   w(u,0xffff2438,int(code,16));u.reg_write(UC_M68K_REG_D0,0x1040);run(u,0x9956)
 elif kind=='airlock':
  run(u,0x771c)
  if code is not None:
   w(u,0xffff2438,int(code,16));u.reg_write(UC_M68K_REG_D0,0x840);run(u,0x9956)
 elif kind=='fuse':
  u.mem_write(0xffff819e,ROM[0x1782a:0x1782a+0xe8]);run(u,0x7a00)
 elif kind=='lift':
  run(u,0x8a74)
  # Show the actual selected map floor rather than the panel's random initial cabin location.
  floor_codes=[0,2,4,6,8,10,10,10,12,14,16,18,20,22,24,26]
  w(u,0xffff260a,floor_codes[floor]);run(u,0x8b76)
 elif kind.startswith('screen'):
  u.reg_write(UC_M68K_REG_D7,0);run(u,0x8720);u.reg_write(UC_M68K_REG_D7,0);run(u,[0x7f44,0x7f74,0x7fa4][int(kind[-1])-1]);run(u,0x89c0)
 b=bytes(u.mem_read(0xffff8934,0x3000));p=[tuple(round(((rd(u,0xffff284c+i*2)>>s)&14)*255/14) for s in [0,4,8]) for i in range(16)];im=Image.new('RGB',(192,128))
 for y in range(128):
  for x in range(192):
   v=b[x//8*512+y*4+x%8//2]>>(4 if x%2==0 else 0)&15;im.putpixel((x,y),p[v])
 if kind.startswith('screen'):
  # Native Scanman overlay:10 columns,48 rows at framebuffer+$C80.
  return im.crop((48,32,128,80)).resize((320,192),Image.Resampling.NEAREST)
 # Remove only border-connected black, preserving black inside the instrument.
 im=im.convert('RGBA');todo=[(x,y) for x in range(192) for y in [0,127]]+[(x,y) for y in range(128) for x in [0,191]];seen=set()
 while todo:
  x,y=todo.pop()
  if not(0<=x<192 and 0<=y<128) or (x,y) in seen:continue
  seen.add((x,y))
  if im.getpixel((x,y))[:3]!=(0,0,0):continue
  im.putpixel((x,y),(0,0,0,0));todo.extend([(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
 box=im.getbbox();assert box;im=im.crop(box)
 return im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST)

if __name__=='__main__':
 banks=json.loads(Path('atlas39/images.json').read_text());levels=json.loads(Path('atlas39/data.json').read_text())[1];p=banks[1]['panels']
 for k in ['scanman','screen1','screen2','screen3','airlock']:
  p[k]=pngdata(capture(k,code='8652' if k=='airlock' else None))
 p['keypads']={};p['terminals']={};p['lift_inside_floors']={}
 for f,l in enumerate(levels):
  if any(v&63==34 for v in l['cells']):p['keypads'][str(f)]=pngdata(capture('keypad',f,code=l['code_gs5']))
  if any(v&63==33 for v in l['cells']):p['terminals'][str(f)]=pngdata(capture('terminal',f,access=0))
  p['lift_inside_floors'][str(f)]=pngdata(capture('lift_inside',f))
 Path('atlas39/images.json').write_text(json.dumps(banks,separators=(',',':')))
 print('Built Mission Scanman/recordings/8652/keypads/terminal/lift panels')
