from sprites import *
S=[(9,0,32,26),(10,9,32,27),(17,116,32,32),(19,175,32,58),(25,125,32,28)]
im=Image.new('RGB',(8*160,5*170),'#18212c');d=ImageDraw.Draw(im)
for row,(t,base,w,h) in enumerate(S):
 for angle in range(8):
  p=part(base+angle,w,h,pal(long(0x10b8c)));p=p.resize((w*3,h*3));im.paste(p,(angle*160,row*170+20),p);d.text((angle*160,row*170),f'{t:02X} {base+angle} (+{angle})',fill='white')
im.save('atlas35/objects_angles.png')
