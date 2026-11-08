exec(open('v36/test_core.py').read().split('levels=json')[0])
old=Path('v36/release_test05/Cyber-Cop_v36_test05.bin').read_bytes()
for raw in list(range(37,62))+[63]:
 a=machine(old);item=old[0x9ee2+raw-31] if raw!=63 else 0
 for broken in [0,64]:
  u=machine();u.reg_write(UC_M68K_REG_D0,raw|broken);u.reg_write(UC_M68K_REG_A1,0xffff2f84);u.reg_write(UC_M68K_REG_A3,0x9ee2);w(u,0xffff2716,0,1);run(u,0x9ea8);assert rd(u,0xffff2f84,1)==item|broken
  u.reg_write(UC_M68K_REG_D1,item|broken);u.reg_write(UC_M68K_REG_A1,0xffff1234);run(u,0x9f1e);assert u.reg_read(UC_M68K_REG_D1)&255==raw|broken,(raw,item,broken,hex(u.reg_read(UC_M68K_REG_D1)))
  assert u.reg_read(UC_M68K_REG_A1)==0xffff1234
  # Drop-store sees original inventory byte in D7; marker follows it only.
  u.reg_write(UC_M68K_REG_D1,raw);u.reg_write(UC_M68K_REG_D7,item|broken);u.reg_write(UC_M68K_REG_A2,0xffff3500);run(u,0x6d2c,0x6d34);assert rd(u,0xffff3500,1)==raw|broken
print('PASS all26 pickup types roundtrip broken flag and drop-store; unrelated register preserved')
for item in [7,12,14,28]:
 for broken in [0,64]:
  for rng in [0,63,64,255]:
   u=machine();u.reg_write(UC_M68K_REG_D1,item|broken);u.reg_write(UC_M68K_REG_A1,0xffff2f50);u.reg_write(UC_M68K_REG_D7,0);w(u,0xffff2f50,item|broken,1);calls=[]
   u.mem_write(0x5054,bytes.fromhex('303c')+rng.to_bytes(2,'big')+bytes.fromhex('4e75'));u.hook_add(UC_HOOK_CODE,lambda uc,a,s,d:calls.append(a) if a==0x5054 else None);run(u,0x6b36)
   assert bool(calls)==(not broken);assert rd(u,0xffff2f50,1)==(item|(64 if broken or rng<=63 else 0))
print('PASS broken pickup bypasses RNG; intact pickup retains both RNG outcomes')
# Floor-change persistence must retain the marker, including raw63 special item.
for camp in [0,1]:
 u=machine();w(u,S['CAMP'],camp);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,0);run(u,0x4882)
 u.mem_write(0xffff305a,bytes(4000));w(u,0xffff2608,0)
 cells=[37,37|64,49,49|64,63,63|64]
 for i,v in enumerate(cells):w(u,0xffff305a+100+i,v,1)
 run(u,0x4a80);u.mem_write(0xffff305a,bytes(4000));run(u,0x4a40)
 assert bytes(u.mem_read(0xffff305a+100,6))==bytes(cells)
print('PASS floor-change persistence in both campaigns, intact/broken ordinary/special pickups')
# Execute complete native pickup action, including inventory compaction and
# matching removal of the world cell. Only audio/UI refreshes are stubbed.
for raw in list(range(37,62))+[63]:
 item=old[0x9ee2+raw-31] if raw!=63 else 0
 for broken in [0,64]:
  u=machine();u.mem_write(0xffff2f50,bytes([255])*52);w(u,0xffff2f50,1,1);u.mem_write(0xffff2f84,bytes([255])*10);w(u,0xffff2f84,item|broken,1);w(u,0xffff2740,0);w(u,0xffff2742,0)
  u.mem_write(0xffff3400,bytes(256));w(u,0xffff2442,0xffff3480,4);w(u,0xffff3480,raw|broken,1)
  for addr in [0x6e98,0x6738]:u.mem_write(addr,bytes.fromhex('4e75'))
  u.mem_write(0x5054,bytes.fromhex('303c00ff4e75'));run(u,0x6ace)
  assert rd(u,0xffff3480,1)==0,(raw,broken)
  assert item|broken in bytes(u.mem_read(0xffff2f50,52)),(raw,broken)
print('PASS52 complete native pickups: inventory retention and matching world-cell removal')
for raw in list(range(37,62))+[63]:
 item=old[0x9ee2+raw-31] if raw!=63 else 0
 for broken in [0,64]:
  u=machine();u.mem_write(0xffff2f50,bytes([255])*52);w(u,0xffff2f50,item|broken,1);w(u,0xffff2740,0);w(u,0xffff26e0,255,1);w(u,0xffff26e2,0,1);w(u,0xffff26e4,0,1);w(u,0xffff441c,0);w(u,0xffff4440,100)
  for addr in [0x6e98,0x6738,0x150d8]:u.mem_write(addr,bytes.fromhex('4e75'))
  u.mem_write(0x96ba,bytes.fromhex('45f9ffff348170004e75'));w(u,0xffff3480,0,1);run(u,0x6cb2)
  assert rd(u,0xffff3480,1)==raw|broken,(raw,item,broken,rd(u,0xffff3480,1))
print('PASS52 complete native drops: map byte matches original inventory damage status')
