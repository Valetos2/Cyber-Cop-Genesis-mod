exec(open('v34/common.py').read())
from pending_fixes import darken_scanman_inset
r=bytearray(Path('v35c/Cyber-Cop_v35c.bin').read_bytes());s=json.loads(Path('v35c/symbols.json').read_text())
pos=darken_scanman_inset(r,s)
for mode in [2,3]:
 u=machine(bytes(r));before=bytes((i*71+19)&255 for i in range(0x3000));u.mem_write(0xffff8934,before);u.reg_write(UC_M68K_REG_D3,mode);run(u,s['scan_contrast35']);after=bytes(u.mem_read(0xffff8934,0x3000))
 def px(b,x,y):return b[x//8*512+y*4+x%8//2]>>(0 if x%2 else 4)&15
 arrow=set([(167,y) for y in range(39,48)]+[(166,y) for y in range(43,48)]+[(165,47)])
 for y in range(128):
  for x in range(192):
   expected=px(before,x,y)
   if mode==3 and 162<=x<169 and 35<=y<48:expected=0
   if mode==3 and (x,y) in arrow:expected=3
   assert px(after,x,y)==expected,(mode,x,y)
print('PASS Scanman dark inset, preserved arrow and all outside pixels, no effect on opposite action; patch',hex(pos))
