exec(open('v36/test_core.py').read().split('levels=json')[0])
for camp in [0,1]:
 for floor,target in [(0,2),(8,0),(15,26),(3,6)]:
  u=machine();w(u,S['CAMP'],camp);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,floor);run(u,0x4882)
  u.mem_write(0x200000,b'\xff'*0x4000);w(u,0xffff218e,target);u.reg_write(UC_M68K_REG_D3,0xb1);u.reg_write(UC_M68K_REG_A0,0xffff7dca)
  run(u,0x8e9e);assert rd(u,0xffff2606)==floor
  ram=bytes(u.mem_read(0x200000,0x4000));lo=camp*0x2000;assert ram[lo+1:lo+9:2]==b'CC17' and ram[(1-camp)*0x2000:(1-camp)*0x2000+0x2000]==b'\xff'*0x2000
  v=machine();v.mem_write(0x200000,ram);w(v,S['CAMP'],camp);run(v,V['load21']);assert v.reg_read(UC_M68K_REG_D0)==1;run(v,0xe94,0x124a)
  assert rd(v,0xffff2606)==int.from_bytes(R[0x8e58+target:0x8e5a+target],'big'),(camp,floor,target,rd(v,0xffff2606))
for lab,d3 in [(0x100,0xb1),(0x101,0xb1),(0,0xb2)]:
 u=machine();u.mem_write(0x200000,b'\xff'*0x4000);w(u,0xffff026c,lab);u.reg_write(UC_M68K_REG_D3,d3);u.reg_write(UC_M68K_REG_A0,0xffff7dca);run(u,0x8e9e);assert bytes(u.mem_read(0x200000,0x4000))==b'\xff'*0x4000
print('PASS destination saves/loads in both campaigns, current floor restored, denied calls and both labs never save')
