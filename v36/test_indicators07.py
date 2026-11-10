exec(open('v36/test_core.py').read().split('levels=json')[0])
from PIL import Image
source=open('v36/render_indicators05.py').read().split("if __name__")[0]
source=source.replace("'bomb':0x94f2", "'bomb':0x94f2,'lift':0x8c78")
source=source.replace("if kind=='bomb':", "if kind=='lift':\n  w(u,base+4,0xb2);w(u,base+0x6e,0xaf)\n elif kind=='bomb':")
source=source.replace("w(u,0xffff2700,255,1);run(u,0x38c8)","if kind=='airlock':w(u,base+14,0xaf)\n w(u,0xffff2700,255,1);run(u,0x38c8)\n # Exercise all digit glyphs, including illuminated segments absent at init.\n for i in range(10):\n  u.reg_write(UC_M68K_REG_A1,0x8bb0);u.reg_write(UC_M68K_REG_A2,0xffff8934+0x100+i*512);u.reg_write(UC_M68K_REG_D2,i);run(u,0x9a5a)")
exec(source)
for p in [0x18052,0x18222,0x17572]:assert R[p:p+32]==OLD[p:p+32]
assert R[0x1eb32:0x1ee72]==OLD[0x1eb32:0x1ee72]
for k in ['keypad','lift','airlock']:
 a=panel(k,OLD);b=panel(k,R)
 changed=[(x,y) for y in range(128) for x in range(192) if a.getpixel((x,y))!=b.getpixel((x,y))]
 assert all(not (x<80 and 64<=y<80) for x,y in changed),(k,changed) # ten glyphs occupy rows64..79
 print('PASS',k,'native palette and all10 filled digits unchanged; lens pixels changed',len(changed))
 im=Image.new('RGB',(384,128));im.paste(a);im.paste(b,(192,0));im.resize((768,256),Image.Resampling.NEAREST).save('v36/'+k+'_v36a.png')
