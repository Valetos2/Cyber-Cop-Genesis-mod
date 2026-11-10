from extract import resource,b,l,w
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json
out=Path('mission_objects')
def indexed(n):
 raw,d=resource(n);im=Image.new('P',(320,len(d)//160));im.putdata([sum(((d[y*160+p*40+x//8]>>(7-x%8))&1)<<p for p in range(4)) for y in range(im.height) for x in range(320)]);return im

def palette(f):
 a=l(0x131e8+f*4)+16
 return [tuple(((w(a+i*2)>>s)&15)*17 for s in [8,4,0]) for i in range(16)]
def color(im,f):
 pal=palette(f);r=Image.new('RGBA',im.size);r.putdata([pal[v]+(0 if v==0 else 255,) for v in im.getdata()]);return r
items=[('9C_barrel',21,(288,0,320,42)),('9D_stool',21,(0,12,32,31)),('9E_stool',18,(288,0,320,19))]
can=Image.new('RGB',(780,360),(74,74,74));draw=ImageDraw.Draw(can)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
for i,(name,n,box) in enumerate(items):
 im=indexed(n).crop(box);im.save(out/(name+'_indices.png'));c=color(im,9);c.save(out/(name+'.png'));c=c.resize((im.width*5,im.height*5),Image.Resampling.NEAREST);can.paste(c,(i*260+50,290-c.height),c);draw.text((i*260+40,310),name,font=font,fill='white')
can.save(out/'objects_same_palette.png')
a=indexed(21).crop((0,12,32,31));c=indexed(18).crop((288,0,320,19));print('same raw',a.tobytes()==c.tobytes());print('diff',sum(x!=y for x,y in zip(a.tobytes(),c.tobytes())));print('colors9d',sorted(set(a.getdata())),'9e',sorted(set(c.getdata())))
for n in [18,21,22,23,24]:
 im=color(indexed(n),9);im.save(out/f'bank_{n}_L2_palette.png')
# Actual level palettes alongside the controlled comparison.
can=Image.new('RGB',(780,360),(74,74,74));draw=ImageDraw.Draw(can)
for i,((name,n,box),f) in enumerate(zip(items,[3,8,9])):
 im=color(indexed(n).crop(box),f);im.save(out/(name+'_level_palette.png'));im=im.resize((im.width*5,im.height*5),Image.Resampling.NEAREST);can.paste(im,(i*260+50,290-im.height),im);draw.text((i*260+30,310),name+' / '+['2F','L1','L2'][i],font=font,fill='white')
can.save(out/'objects_level_palettes.png')
robot=Image.new('RGB',(600,340),(74,74,74));dr=ImageDraw.Draw(robot)
for i,(name,n,box) in enumerate([('Walk',23,(128,0,192,98)),('Attack 1',24,(0,100,64,198)),('Attack 2',24,(64,100,128,198))]):
 im=color(indexed(n).crop(box),9);im.save(out/('robot_'+name.replace(' ','_')+'.png'));im=im.resize((192,294),Image.Resampling.NEAREST);robot.paste(im,(i*200+4,10),im);dr.text((i*200+50,315),name,font=font,fill='white')
robot.save(out/'robot_comparison.png')
# Compare silhouette and non-seat pixels at native resolution.
print('silhouette differences',sum((x==0)!=(y==0) for x,y in zip(a.getdata(),c.getdata())))
print('different rows', sorted({i//32 for i,(x,y) in enumerate(zip(a.getdata(),c.getdata())) if x!=y}))
