from pathlib import Path
from PIL import Image,ImageDraw
import json,base64,io
R=Path('v29/Cyber-Cop_v29.bin').read_bytes()
def word(a):return int.from_bytes(R[a:a+2],'big')
def long(a):return int.from_bytes(R[a:a+4],'big')
def pal(a):return [tuple(round(((word(a+i*2)>>s)&14)*255/14) for s in [0,4,8]) for i in range(16)]
def part(idx,w,h,p):
 a=0x8eef0+long(0x8eafc+idx*4);b=0x8eef0+long(0x8eafc+(idx+1)*4);stride=(b-a)//(w//2);assert stride>=h,(idx,w,h,stride)
 im=Image.new('RGBA',(w,h))
 for x in range(w):
  for y in range(h):
   n=R[a+x//2*stride+y]>>(4 if x%2==0 else 0)&15
   im.putpixel((x,y),p[n]+(255 if n else 0,))
 return im
specs=[('8004',187,32,96,195,15),('8006',215,64,98,226,25),('801C',62,64,98,None,0),('8119',76,32,80,None,0),('811A',135,64,98,None,0),('811B',57,64,98,None,0)]
def enemy(spec,delta,p):
 t,idx,w,h,second,top=spec
 if second:
  im=Image.new('RGBA',(w,h));im.paste(part(idx+delta,w,top,p),(0,0));im.paste(part(second+delta,w,h-top,p),(0,top));return im
 return part(idx+delta,w,h,p)
if __name__=='__main__':
 sheet=Image.new('RGB',(6*160,260*2),'#18212c');d=ImageDraw.Draw(sheet);p=pal(long(0x10b8c))
 for j,s in enumerate(specs):
  for k,delta in enumerate([0,4]):
   im=enemy(s,delta if s[0]!='811B' else 0,p);im=im.resize((im.width*2,im.height*2));sheet.paste(im,(j*160,k*260+25),im);d.text((j*160,k*260+5),s[0]+' +'+str(delta),fill='white')
 sheet.save('atlas35/contact.png')

def pngdata(im):
 b=io.BytesIO();im.save(b,format='PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
def icon(item):
 offset=word(0xa052+item*4);cols=word(0xa054+item*4)*2
 im=Image.new('RGBA',(cols*8,32));p=pal(0x2870)
 for row in range(4):
  for col in range(cols):
   tile=word(0x3f520+offset+row*128+col*2)
   if tile==0:continue
   a=0x39aa0+((tile&2047)-40)*32
   for y in range(8):
    for x in range(8):
     xx=7-x if tile&0x800 else x;yy=7-y if tile&0x1000 else y
     n=R[a+yy*4+xx//2]>>(4 if xx%2==0 else 0)&15
     im.putpixel((col*8+x,row*8+y),p[n]+(255 if n else 0,))
 return im
objects={9:(5,32,26),10:(14,32,27),15:(165,32,45),16:(30,32,14),17:(121,32,32),19:(180,32,58),20:(41,32,32),21:(184,32,42),22:(54,32,100),23:(55,32,100),25:(129,32,28),26:(174,32,120),31:(39,32,41),32:(134,32,41),33:(40,32,41),35:(38,32,41)}
if __name__=='__main__':
 images={'enemies':{},'objects':{},'items':{}}
 for f in range(16):
  p=pal(long(0x10b8c+f*4));images['enemies'][str(f)]={s[0]:pngdata(enemy(s,4 if s[0]!='811B' else 0,p)) for s in specs}
  images['objects'][str(f)]={str(t):pngdata(part(idx,w,h,p)) for t,(idx,w,h) in objects.items()}
 images['items']={str(i):pngdata(icon(i)) for i in range(35)}
 Path('atlas35/images.json').write_text(json.dumps(images))
 sheet=Image.new('RGB',(800,560),'#18212c');d=ImageDraw.Draw(sheet)
 for i in range(35):
  im=icon(i);im=im.resize((im.width*2,im.height*2));x=i%8*100;y=i//8*110;sheet.paste(im,(x,y+18),im);d.text((x,y),str(i),fill='white')
 sheet.save('atlas35/items_check.png')
