exec(open('v36/test_core.py').read().split('levels=json')[0])
for kind in [3,17,7,0x8004,0x8006,0x801c,0x8119,0x811a,0x811b,0x801d,0x8005,0x8008]:
 enemy=kind in [0x8004,0x8006,0x801c,0x8119,0x811a,0x801d]
 for behind in [-1,0,1,4,5,20]:
  u=machine();w(u,0xffff23b2,0);w(u,0xffff1002,kind);w(u,0xffff100e,96);w(u,0xffff1000,(20+behind)*64);w(u,0xffff40ce+96,20,1);u.reg_write(UC_M68K_REG_A2,0xffff1000);run(u,0xec62)
  assert rd(u,0xffff23b2)==(4 if behind<=0 or enemy and behind<=4 else 0),(hex(kind),behind)
  assert u.reg_read(UC_M68K_REG_D7)==rd(u,0xffff23b2) and u.reg_read(UC_M68K_REG_A6)==0xffff23b4
order=[17,7,3,0x811a,0x8005,0x811b,0x801d,3];expected=[0x811a,0x811b,0x801d,3,3,7,0x8005,17]
u=machine();w(u,0xffff23b2,0);w(u,0xffff40ce+96,255,1)
for i,kind in enumerate(order):
 a=0xffff1000+i*0x56;w(u,a+2,kind);w(u,a,256);w(u,a+14,96);u.reg_write(UC_M68K_REG_A2,a);run(u,0xec62)
ptrs=[rd(u,0xffff23b4+i*4,4) for i in range(len(order))];assert [rd(u,p+2) for p in ptrs]==expected
print('PASS aim threat priority, stable peers, behind-wall one-cell bound and native register contract')
