"""Cumulative v12: retained 2x2 dither; reject off-screen wall/band quads."""
from pathlib import Path
import sys,json,hashlib
import build_v11 as base

def build(source):
 _,rom,labels,size=base.build(source);r=bytearray(rom)
 # Exact 2x2 table from the selected v11 variant.
 old=list(source[0xe4aa:0xe4d0]);table=bytearray();bayer=[[0,2],[3,1]]
 for index in range(256):
  depth=index*128;slot=min(depth//256,len(old)-1);hi=old[slot];first=slot;end=slot+1
  while first and old[first-1]==hi:first-=1
  while end<len(old) and old[end]==hi:end+=1
  lo=old[end] if end<len(old) else hi
  k=0 if lo==hi else min(16,(depth-first*256)*16//((end-first)*256))
  for y in range(8):table.extend(bytes.fromhex(''.join(format(lo if bayer[y%2][x%2]*4<k else hi,'x') for x in range(8))))
 t=labels['bayer_patterns'];r[t:t+8192]=table
 c=base.Code();c.b=bytearray(b'\xff'*(0xf3300-base.BASE));start=len(c.b)
 for name,target in [('wall_guard',labels['wall_with_band']),('band_guard',0xe4d0)]:
  c.label(name);c.abs('43f9',0xffff2458)
  for edge,offsets,bound,condition in [('left',[0,4,8,12],0,'6c00'),('right',[0,4,8,12],191,'6f00'),('below',[2,6,10,14],0,'6c00'),('above',[2,6,10,14],127,'6f00')]:
   for off in offsets:
    c.emit(f'0c690{bound:03x}{off:04x}');c.branch(condition,name+'_'+edge+'_keep')
   c.label(name+'_'+edge+'_reject');c.emit('4e75');c.label(name+'_'+edge+'_keep')
  c.jump(target)
 blob=c.finish()[start:];assert set(r[0xf3300:0xf3300+len(blob)])=={255}
 r[0xf3300:0xf3300+len(blob)]=blob
 r[0xe498:0xe49e]=bytes.fromhex('4ef9')+c.labels['wall_guard'].to_bytes(4,'big')
 tail=labels['intro_enter']-6;assert r[tail:tail+6]==bytes.fromhex('4ef90000e4d0')
 r[tail:tail+6]=bytes.fromhex('4ef9')+c.labels['band_guard'].to_bytes(4,'big')
 return bytes(r),dict(labels,**c.labels)
if __name__=='__main__':
 src=Path(sys.argv[1]).read_bytes();out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True);rom,labels=build(src)
 (out/'Cyber-Cop_v12.bin').write_bytes(rom);(out/'Cyber-Cop_v12.ips').write_bytes(base.ips(src,rom));(out/'symbols.json').write_text(json.dumps(labels,indent=2));print(hashlib.sha256(rom).hexdigest())
