"""python maps.py disk2.ipf mission.ipf > maps.json (these specific pressings)"""
from pathlib import Path
from unpack import unpack
import sys,struct,json
def maps(b,mission):
 start,t,delta,ptr=((0x9c00,0x7d13a,0x75000,0x13c2a) if mission else (0x37c00,0x9fdaa,0x97800,0x138d2))
 assert b[start:start+2]==b'\x80\0'
 i=start+34; out=bytearray()
 while len(out)<32000:
  n=b[i];i+=1
  if n<128:out.extend(b[i:i+n+1]);i+=n+1
  elif n>128:out.extend([b[i]]*(257-n));i+=1
 assert len(out)==32000
 levels=[]
 for f in range(16):
  p=delta+struct.unpack_from('>I',b,delta+ptr+4*f)[0];lut=b[t:t+9]+b[p:p+7];assert len(lut)==16
  s=''
  for y in range((f//4)*50,(f//4+1)*50):
   for x in range((f%4)*80,(f%4+1)*80):
    s+=format(sum((out[y*160+k*40+x//8]>>(7-x%8)&1)<<k for k in range(4)),'x')
  c=bytearray(lut[int(v,16)] for v in s)
  t0=delta+(0x1392a if mission else 0x135d2)+48*f
  items=[]
  for x,z,v in struct.iter_unpack('BBB',b[t0:t0+48]):
   if v:
    assert x<80 and z<50
    c[(49-z)*80+x]=v;items.append([x,49-z,v])
  for j in range(4000):
   v=c[j]
   if v==0x84:
    if c[j+1]==0x81:c[j-80]=c[j+80]=0x43
    elif c[j-80]==0x81:c[j]|=64;c[j-1]=c[j+1]=3
   elif v==0xa2 and c[j+1]!=0x81 and c[j-80]==0x81:c[j]|=64
   elif v==0xa3:
    c[j-160]=12
    if c[j-159]:c[j-159]=0xe4
    elif c[j-161]:c[j-161]=0xa4
   elif v==0x8a:c[j+1:j+4]=b'KKK'
  assert len(c)==4000
  q=delta+struct.unpack_from('>I',b,(0x8c5de if mission else 0xaea86)+f*4)[0]
  enemies=[]
  while b[q:q+2]!=b'\xff\xff':
   x,z,init,extra=struct.unpack_from('>HHII',b,q);q+=12
   assert x<20480 and z<12800 and len(enemies)<128
   enemies.append([x//256,49-z//256,init,extra])
  levels.append(dict(enemies=enemies,slot=f,lut=list(lut),pixels=s,cells=c.hex(),items=items))
 return levels
if __name__=='__main__':
 def read(p):
  s,_=unpack(Path(p));return b''.join(s.get((i//11,i%11),bytes(512)) for i in range(1760))
 print(json.dumps([maps(read(p),i==1) for i,p in enumerate(sys.argv[1:3])]))
