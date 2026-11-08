exec(open('v36/test_core.py').read().split('levels=json')[0])
from PIL import Image,ImageDraw

def panel(kind,rom):
 u=machine(rom);w(u,S['CAMP'],0)
 for a in [0x1646,0x2930,0x4d18,0x150b4,0x150d8,0x8f4a]:u.mem_write(a,bytes.fromhex('4e75'))
 run(u,0x2360);run(u,0x2944);run(u,0x4882);run(u,0x685e)
 w(u,0xffff0200,0);w(u,0xffff0004,255);w(u,0xffff219a,1);w(u,0xffff013c,255,1)
 u.reg_write(UC_M68K_REG_D7,0);run(u,{'keypad':0x943e,'airlock':0x771c,'bomb':0x94f2}[kind])
 base=rd(u,0xffff227e,4)
 if kind=='airlock':w(u,0xffff223e,0x4c)
 if kind=='bomb':w(u,base+10,0xe1)
 else:
  a=base+rd(u,0xffff223e)-0x48;w(u,a,0xb1);w(u,a+4,0xb2)
 w(u,0xffff2700,255,1);run(u,0x38c8)
 b=bytes(u.mem_read(0xffff8934,12288));p=[tuple(round(((rd(u,0xffff284c+i*2)>>s)&14)*255/14) for s in [0,4,8]) for i in range(16)];im=Image.new('RGB',(192,128))
 for y in range(128):
  for x in range(192):
   v=b[x//8*512+y*4+x%8//2]>>(4 if x%2==0 else 0)&15;im.putpixel((x,y),p[v])
 return im
if __name__=='__main__':
 old=Path('v36/release_test04/Cyber-Cop_v36_test04.bin').read_bytes();out=Image.new('RGB',(384,144*3));d=ImageDraw.Draw(out)
 for i,k in enumerate(['keypad','airlock','bomb']):
  a=panel(k,old);b=panel(k,R);changed=[(x,y) for y in range(128) for x in range(192) if a.getpixel((x,y))!=b.getpixel((x,y))];print(k,'changed pixels',len(changed),'bounds', (min(x for x,y in changed),min(y for x,y in changed),max(x for x,y in changed),max(y for x,y in changed)))
  assert len(changed)<=24,(k,len(changed))
  out.paste(a,(0,i*144));out.paste(b,(192,i*144));d.text((2,i*144+128),k+' test04 | test05',fill='white')
 out.resize((768,864),Image.Resampling.NEAREST).save('v36/indicators_test05.png')
