exec(open('v36/test_core.py').read().split('levels=json')[0])
u=machine();u.mem_write(0x200000,b'\xff'*0x4000)
for camp in [0,1]:
 w(u,S['CAMP'],camp);run(u,0x8faa);run(u,V['save21'])
both=bytes(u.mem_read(0x200000,0x4000))
for mask in range(4):
 for cheats in range(2):
  v=machine();sr=bytearray(both)
  for camp in [0,1]:
   if not(mask>>camp&1):sr[camp*0x2000:(camp+1)*0x2000]=b'\xff'*0x2000
  v.mem_write(0x200000,bytes(sr));v.mem_write(0xffbe,b'\x4e\x75');w(v,0xffff0157,cheats,1);w(v,S['CAMP'],1)
  run(v,S['main36_text']);want=[0,1]+([2] if mask&1 else [])+([3] if mask&2 else [])+[4,5]+([6] if cheats else [])
  got=[rd(v,0xffff0840+2*i) for i in range(rd(v,0xffff0850))]
  assert got==want,(mask,cheats,got,want)
  assert rd(v,S['CAMP'])==1
print('PASS compact menus: four SRAM combinations, cheats hidden/visible, campaign preserved')
