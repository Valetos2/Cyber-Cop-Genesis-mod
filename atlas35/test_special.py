exec(open('v30/common.py').read())
import json
D=json.load(open('atlas35/data.json'));parking=D[6];points=[(i%80,i//80,v) for i,v in enumerate(parking['cells']) if v&63==27];print('Parking ending triggers:',points)
for item in [255,30,94]:
 u=machine();u.mem_write(0xffff2f50,bytes([255])*52);w(u,0xffff2f50+51,item,1);run(u,0xaec6,0x2eb0 if item==30 else STOP)
print('PASS ending trigger accepts exact embryo $1E in any inventory slot; broken $5E does not match')
for used in [0,255]:
 for item in [11,75,255]:
  u=machine();u.mem_write(0x2f80,bytes.fromhex('4e75'));u.mem_write(0xffff2f50,bytes([255])*52);w(u,0xffff2f50+51,item,1);w(u,0xffff26fa,used,1);run(u,0x2d08,0x2d92 if item==11 and used==0 else 0x2d26)
u=machine()
for a in [0x2580,0x15f0,0x1646,0x7994,0x4a80,0x4832]:u.mem_write(a,bytes.fromhex('4e75'))
run(u,0x2d92,0x2e08);assert rd(u,0xffff2606)==11 and rd(u,0xffff441a)==0x2a00 and rd(u,0xffff441e)==0x2300 and rd(u,0xffff26fa,1)==255
assert D[11]['cells'][14*80+42]==0
print('PASS one-time rescue with intact Bomb only, L4 X42 Y14 (world X$2A00 Z$2300), marker lies on floor')
