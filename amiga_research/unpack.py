from pathlib import Path
import struct,glob,zlib,collections
def unpack(p):
 b=p.read_bytes();o=0;sectors={}; tracks={};miss=[]
 while o<len(b):
  t,n,c=struct.unpack_from('>4sII',b,o);assert zlib.crc32(b[o:o+8]+bytes(4)+b[o+12:o+n])==c
  d=b[o+12:o+n];o+=n
  if t==b'IMGE':
   im=struct.unpack('>17I',d);tracks[im[13]]=im
  if t!=b'DATA':continue
  size,bits,crc,key=struct.unpack('>4I',d);d=b[o:o+size];o+=size;assert zlib.crc32(d)==crc
  im=tracks[key];tr=im[0]*2+im[1];found=[]
  for j in range(im[10]):
   pos=struct.unpack_from('>I',d,j*32+28)[0];data=b''
   while pos<len(d) and d[pos]:
    a=d[pos];n=a>>5;sz=int.from_bytes(d[pos+1:pos+1+n],'big');pos+=1+n
    if a&31==2:data+=d[pos:pos+sz]
    if a&31 in (1,2,3):pos+=sz
    else:break
   if len(data)<540:continue
   data=data[-542:] if len(data)>=542 else data
   if len(data)>540 and data[:2]==bytes(2):data=data[2:]
   def join(v):
    mid=len(v)//2
    def expand(x):return sum(((x>>k)&1)<<(2*k) for k in range(16))
    return b''.join(((expand(int.from_bytes(v[i:i+2],'big'))<<1)|expand(int.from_bytes(v[mid+i:mid+i+2],'big'))).to_bytes(4,'big') for i in range(0,mid,2))
   h=join(data[:4])
   if h[0]!=255 or h[1]!=tr or h[2]>=11:continue
   assert (tr,h[2]) not in sectors
   sectors[tr,h[2]]=join(data[28:540]);found.append(h[2])
  if len(found)!=11:miss.append((tr,len(found)))
 return sectors,miss
if __name__=='__main__':
 for p in sorted(Path('upload').glob('*.ipf')):
  id='mission' if 'Mission' in p.name else ('d1' if 'Disk 1' in p.name else 'd2')
  s,m=unpack(p);out=b''.join(s.get((t,i),bytes(512)) for t in range(160) for i in range(11));Path('amiga_research/'+id+'.adf').write_bytes(out);print(id,len(s),m[:16],out[:48])
