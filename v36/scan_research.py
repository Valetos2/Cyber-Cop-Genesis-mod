from pathlib import Path
import struct,json
from PIL import Image

def sheet(camp,res):
 a=Path('amiga3/'+camp+'.bin').read_bytes();disk=Path('amiga_research/'+camp+'.adf').read_bytes();table=0x62d0 if camp=='mission' else 0x6666
 sec,n=struct.unpack_from('>HH',a,table+res*4);raw=disk[sec*512:(sec+n)*512];out=bytearray();p=34
 if raw[:2]==b'\0\0':out=raw[34:32034]
 while len(out)<32000:
  n=raw[p];p+=1
  if n<128:out+=raw[p:p+n+1];p+=n+1
  elif n>128:out+=raw[p:p+1]*(257-n);p+=1
 px=[[sum(((out[y*160+((x//16)*8+k*2+(x%16)//8 if raw[:2]==b'\0\0' else k*40+x//8)]>>(7-x%8))&1)<<k for k in range(4)) for x in range(320)] for y in range(200)]
 return px,raw[2:34],bytes(out)
if __name__=='__main__':
 mi,mp,mb=sheet('mission',11);oi,op,ob=sheet('d2',20);print('equal',mb==ob,'differing bytes',sum(x!=y for x,y in zip(mb,ob)))
 for name,pix,pal in [('mission',mi,mp),('original',oi,op)]:
  im=Image.new('P',(320,200));im.putdata(sum(pix,[]));im.putpalette([c for w in struct.unpack('>16H',pal) for c in [(w>>8&15)*17,(w>>4&15)*17,(w&15)*17]]);im.resize((640,400),Image.Resampling.NEAREST).save('v36/scan_'+name+'.png')
