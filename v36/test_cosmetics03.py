from pathlib import Path
import json,struct
from PIL import Image
r=Path('v36/Cyber-Cop_v36_WORK_IN_PROGRESS.bin').read_bytes();s=json.loads(Path('v36/symbols.json').read_text());bank=s['item_graphics36c']+2
pal=[tuple(((int.from_bytes(r[0x2870+i*2:0x2872+i*2],'big')>>s)&14)*255//14 for s in [0,4,8]) for i in range(16)]
im=Image.new('RGB',(384,128))
for j,item in enumerate([25,26,27]):
 off=int.from_bytes(r[0xa052+item*4:0xa054+item*4],'big');icon=Image.new('RGB',(32,32))
 for y in range(32):
  for x in range(32):
   tile=int.from_bytes(r[0x3f520+off+y//8*128+x//8*2:0x3f522+off+y//8*128+x//8*2],'big');a=bank+((tile&2047)-40)*32+(y%8)*4+x%8//2
   v=r[a]>>(4 if x%2==0 else 0)&15;icon.putpixel((x,y),pal[v])
 im.paste(icon.resize((128,128),Image.Resampling.NEAREST),(j*128,0))
im.save('v36/holo_labels03.png')
ref=Image.open('upload/holo_labels02_fixed.png').convert('RGB');assert ref.size==im.size
# Actual supplied preview colours are rounded, allow a one-channel quantization step.
assert max(abs(x-y) for a,b in zip(im.getdata(),ref.getdata()) for x,y in zip(a,b))<=1
print('PASS all three Holo icons match supplied pixel reference')

exec(open('v36/test_core.py').read().split('levels=json')[0])
v35=json.loads(Path('v35c/symbols.json').read_text())
for camp in [0,1]:
 for cell,expected in [(0x9c,0x9c if camp else 0),(0x9d,0x5d if camp else 0),(0x9e,0x5e if camp else 0)]:
  u=machine();w(u,S['CAMP'],camp);w(u,0xffff1000,cell,1);u.reg_write(UC_M68K_REG_A2,0xffff1000);run(u,0xab72)
  assert rd(u,0xffff1000,1)==expected,(camp,cell)
 for index,height in [(28,168),(29,76),(30,76)]:
  u=machine();w(u,S['CAMP'],camp);u.reg_write(UC_M68K_REG_D3,index*4)
  run(u,0xab14,0xab1c);ptr=u.reg_read(UC_M68K_REG_A3)
  assert rd(u,ptr)==0 and rd(u,ptr+2)==(height if camp else 0)
print('PASS campaign-specific prop destruction and collision tables')

def pixel(u,x,y):
 a=0xffff8934+(x//8)*512+y*4+(x%8)//2
 return rd(u,a,1)>>(0 if x&1 else 4)&15
u=machine();u.reg_write(UC_M68K_REG_D3,3);run(u,v35['scan_contrast35'])
for x,y in [(167,39),(167,40),(166,43),(166,44),(165,47)]:assert pixel(u,x,y)==2
for x,y in [(167,41),(167,46),(166,45)]:assert pixel(u,x,y)==3
assert pixel(u,162,35)==0
print('PASS Scanman arrow retains intermediate tones and black inset')

# No held input is needed for a native latched activation texture.
for mouse,callback,texture,changed in [(1,0x77a8,0xc0,True),(1,0x77a8,0,False),(0,0x77a8,0xc0,False),(1,0x2106,0xc0,False)]:
 u=machine();w(u,0xffff0200,mouse);w(u,0xffff26b8,callback,4);w(u,0xffff22f2,texture)
 buf=bytes((i*19+i//7)%256 for i in range(12288));u.mem_write(0xffff8934,buf)
 run(u,v35['panel_border']);after=bytes(u.mem_read(0xffff8934,len(buf)))
 assert (after!=buf)==changed
 run(u,v35['panel_border']);assert bytes(u.mem_read(0xffff8934,len(buf)))==buf
print('PASS latched airlock frame follows native texture; upload swap restores framebuffer')

# Automatic skip must not call the SFX routine; a real forward action must.
u=machine();w(u,0xffff4412,0);w(u,0xffff4418,1)
for i in range(45):w(u,0xffff441c+i*4,0xffff1100,4)
w(u,0xffff1100,0xffff);u.mem_write(0x150d8,bytes.fromhex('4e75'));calls=[]
u.hook_add(UC_HOOK_CODE,lambda uc,a,sz,d: calls.append(a) if a==0x150d8 else None)
run(u,0xfc66);assert calls==[]
run(u,0xfd16);assert len(calls)==1
print('PASS automatic equipment search silent; first actual selection still sounds')

for text in [b'card',b'bomb',b'mask',b'cardx']:
 u=machine();u.mem_write(0xffff1000,text+b' ');u.reg_write(UC_M68K_REG_A5,0xffff1000);u.reg_write(UC_M68K_REG_D7,len(text)-1)
 run(u,V['name26_draw'],V['name26_draw']+14)
 actual=u.reg_read(UC_M68K_REG_D3)&65535
 expected=0xe900+((45-(4 if text==b'card' else len(text)-1))&0xfffe)
 assert actual==expected,(text,hex(actual),hex(expected))
assert int.from_bytes(R[0x7d48:0x7d4a],'big')==500
print('PASS only card shifts one character left; alarm countdown increased fivefold')

for char in range(6):
 u=machine();w(u,0xffff2a38,char);uploads=[];names=[]
 for addr in [0x2580,0x35fe]:u.mem_write(addr,bytes.fromhex('4e75'))
 def capture(uc,a,sz,d):
  if a==0x2580:uploads.append((uc.reg_read(UC_M68K_REG_A0),uc.reg_read(UC_M68K_REG_D0)&65535,uc.reg_read(UC_M68K_REG_D1)&65535))
  if a==0x35fe:names.append((uc.reg_read(UC_M68K_REG_D2)&65535,uc.reg_read(UC_M68K_REG_D0)&65535))
 u.hook_add(UC_HOOK_CODE,capture);run(u,0xfb88,0xfb8e)
 assert uploads==[(S['gear_portrait_gfx36c_'+str(char)],512,0xbe00)]
 assert len(names)==16 and [a for a,b in names]==[0xe804+y*128+x*2 for y in range(4) for x in range(4)]
 pp=int.from_bytes(OLD[0xf7d4+char*4:0xf7d8+char*4],'big')
 assert bytes(u.mem_read(0xffff286c,32))==OLD[pp:pp+32]
 assert rd(u,0xffff2702,1)==255
print('PASS all six equipment portraits: native selected palette, 16 tiles, correct position before fade')
