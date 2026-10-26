from pathlib import Path
import sys,json,hashlib
import build_v12 as previous
import build_v11 as base

def build(source):
 rom,oldlabels=previous.build(source);r=bytearray(rom);c=base.Code();c.b=bytearray(b'\xff'*(0xf3600-base.BASE));start=len(c.b)
 for entry,end,slot in [(0xeac2,0xead2,0xe9a0),(0xeae4,0xeaf4,0xe9a4),(0xeb06,0xeb16,0xe99c),(0xeb28,0xeb38,0xe998)]:
  tag=f'sprite13_{entry:x}';c.label(tag)
  c.emit('3e280014be680018');c.branch('6c00',tag+'_native')
  c.emit('2f0d');c.abs('4bf9',0xeb4a);c.emit('3e1c')
  c.label(tag+'_calculate');c.emit(source[entry+2:end].hex());c.branch('6700',tag+'_zero_write')
  c.emit('18350000');c.branch('6700',tag+'_opaque_write');c.branch('6000',tag+'_mixed_write')
  for state in ['opaque','mixed','zero']:
   c.label(tag+'_'+state+'_next');c.emit('3e1c');c.branch('6600',tag+'_calculate')
   c.label(tag+'_'+state+'_write')
   if state=='opaque':c.emit('1680') # move.b d0,(a3)
   if state=='mixed':c.emit('c9138113')
   c.emit('584b');c.branch('51cd',tag+'_'+state+'_next');c.emit('2a5f4e75')
  c.label(tag+'_native');c.jump(entry)
  r[slot:slot+4]=c.labels[tag].to_bytes(4,'big')
 # Precomposed nearest-neighbour pixel pairs for the 64x98 sprite family.
 # Original columns have 100-byte stride (98 logical rows plus padding).
 metadata=0xf5000;expanded=bytearray(b'\xff'*0x100000);pointers=[0]*253;assetpos=0x100000
 for idx in range(135,165):
  asset=0x8eef0+int.from_bytes(source[0x8eafc+idx*4:0x8eb00+idx*4],'big')
  following=0x8eef0+int.from_bytes(source[0x8eafc+(idx+1)*4:0x8eb00+(idx+1)*4],'big')
  assert following-asset==3200
  pointers[idx]=assetpos
  for x in range(64):
   for step in [0,1]:
    for y in range(128):
     def pixel(xx):return (source[asset+(xx//2)*100+y]>>(4 if xx%2==0 else 0))&15
     expanded[assetpos-0x100000]=pixel(x)*16+pixel(x+step);assetpos+=1
 for entry,slot in [(0xeac2,0xe9a0),(0xeae4,0xe9a4),(0xeb06,0xe99c),(0xeb28,0xe998)]:
  tag=f'pair13_{entry:x}';c.label(tag);c.emit('48e70206') # preserve D6/A5/A6
  c.emit('0c6800400012');c.branch('6600',tag+'_fallback')
  c.emit('0c6800620014');c.branch('6600',tag+'_fallback')
  c.emit('0c6800620018');c.branch('6f00',tag+'_fallback')
  c.emit('3e2800200c4700fc');c.branch('6200',tag+'_fallback')
  c.emit('e54f');c.abs('4bf9',metadata);c.emit('2a757000bafc0000');c.branch('6700',tag+'_fallback')
  c.emit('302efffc322efffe0c40003f');c.branch('6200',tag+'_fallback')
  c.emit('0c41003f');c.branch('6200',tag+'_fallback')
  # Verify actual native source pointers before using precomposed data.
  c.emit('3e00e24fcffc0064');c.abs('deb9',0xffff40ba);c.emit('be89');c.branch('6600',tag+'_fallback')
  c.emit('3e01e24fcffc0064');c.abs('deb9',0xffff40ba);c.emit('be8a');c.branch('6600',tag+'_fallback')
  # D4 = second x - first x, require 0 or 1.
  c.emit('380198400c440001');c.branch('6200',tag+'_fallback')
  c.emit('3e00e14fef4cde44') # D7=x*256; D4=step*128; add.w D4,D7
  c.emit('dac7');c.emit('2c0d') # D6 = starting precomposed pointer
  c.abs('4df9',0xeb4a);c.emit('3e1c')
  c.label(tag+'_calculate');c.emit('dac710154a00');c.branch('6700',tag+'_zero_write')
  c.emit('18360000');c.branch('6700',tag+'_opaque_write');c.branch('6000',tag+'_mixed_write')
  for state in ['opaque','mixed','zero']:
   c.label(tag+'_'+state+'_next');c.emit('3e1c');c.branch('6600',tag+'_calculate')
   c.label(tag+'_'+state+'_write')
   if state=='opaque':c.emit('1680')
   if state=='mixed':c.emit('c9138113')
   c.emit('584b');c.branch('51cd',tag+'_'+state+'_next');c.branch('6000',tag+'_done')
  c.label(tag+'_done');c.emit('2e0d9e86d2c7d4c74cdf60404e75')
  c.label(tag+'_fallback');c.emit('4cdf6040');c.jump(c.labels[f'sprite13_{entry:x}'])
  r[slot:slot+4]=c.labels[tag].to_bytes(4,'big')
 c.label('down_a13');c.abs('50f9',0xffff26e9)
 c.abs('1039',0xffff26e4);c.abs('8039',0xffff26e5) # OR.B: was either hover mode active?
 c.branch('6700','down_quiet')
 c.abs('51f9',0xffff26e4);c.abs('51f9',0xffff26e5);c.emit('7001');c.jump(0x150b4)
 c.label('down_quiet');c.abs('51f9',0xffff26e4);c.abs('51f9',0xffff26e5);c.emit('4e75')
 assert r[0x9dce:0x9dd4]==bytes.fromhex('50f9ffff26e9')
 r[0x9dce:0x9dd4]=bytes.fromhex('4ef9')+c.labels['down_a13'].to_bytes(4,'big')
 blob=c.finish()[start:];assert set(r[0xf3600:0xf3600+len(blob)])=={255};r[0xf3600:0xf3600+len(blob)]=blob
 assert 0xf3600+len(blob)<metadata
 r[metadata:metadata+len(pointers)*4]=b''.join(x.to_bytes(4,'big') for x in pointers)
 r.extend(expanded);r[0x1a4:0x1a8]=(len(r)-1).to_bytes(4,'big')
 r[0x18e:0x190]=(sum(int.from_bytes(r[i:i+2],'big') for i in range(0x200,len(r),2))&65535).to_bytes(2,'big')
 return bytes(r),dict(oldlabels,**c.labels)
if __name__=='__main__':
 src=Path(sys.argv[1]).read_bytes();out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True);rom,labels=build(src)
 (out/'Cyber-Cop_v13.bin').write_bytes(rom);(out/'Cyber-Cop_v13.ips').write_bytes(base.ips(src+bytes(len(rom)-len(src)),rom));(out/'symbols.json').write_text(json.dumps(labels,indent=2));print(hashlib.sha256(rom).hexdigest())
