exec(open('v34/common.py').read())
# Each previously unused floor increments any access value once, independent of floor number.
for floor in range(16):
 for access in range(8):
  u=machine();u.mem_write(0xffff2718,bytes(16));w(u,0xffff2606,floor);w(u,0xffff26bc,access*32);w(u,0xffff216e,0)
  run(u,0x7d76,0x7db2);assert rd(u,0xffff26bc)==min(access+1,7)*32;assert rd(u,0xffff2718+floor,1)==255
  w(u,0xffff216e,0);run(u,0x7d76,0x7db2);assert rd(u,0xffff26bc)==min(access+1,7)*32
print('PASS terminal: every floor adds one access once, cap7, 128 floor/access combinations')
for access in range(8):
 for button in range(14):
  u=machine();w(u,0xffff26bc,access*32);u.reg_write(UC_M68K_REG_D0,button*2);run(u,0x8e74)
  allowed=int.from_bytes(ROM[0x1119c+access*32+button*2:0x1119e+access*32+button*2],'big')<32768
  assert rd(u,0xffff7dca)==(0xb1 if allowed else 0xb2)
print('PASS all 112 elevator access/button decisions match exported access table')
# Normalized 03 and 43 activate adjacent doors along X and map Y respectively.
for tile,delta in [(3,1),(0x43,80)]:
 u=machine();u.mem_write(0xffff305a,bytes(4000));run(u,0x2944);run(u,0x4882)
 u.mem_write(0xffff305a,bytes(4000));a=0xffff4468;x,y=30,25;cell=0xffff305a+y*80+x;w(u,a+8,x*256+128);w(u,a+12,(49-y)*256+128);w(u,a+2,0x8004);w(u,cell,tile,1);w(u,cell+delta,0x84,1)
 u.reg_write(UC_M68K_REG_A0,a);run(u,0xaee2);assert rd(u,cell+delta,1)==0x86
print('PASS actor opens door along correct axis from 03/43')
u=machine();run(u,0x2944);run(u,0x4882);u.mem_write(0xffff305a,bytes(4000));a=0xffff4412;x,y=30,25;cell=0xffff305a+y*80+x
w(u,a+8,x*256+128);w(u,a+12,(49-y)*256+128);w(u,a+10,0);w(u,a+46,100);w(u,cell,12,1);w(u,cell+1,0xe4,1);u.reg_write(UC_M68K_REG_A0,a);events=[]
def h(u,pc,s,d):
 if pc==0x6764:events.append(u.reg_read(UC_M68K_REG_A1));ret(u)
u.hook_add(UC_HOOK_CODE,h);run(u,0xad82)
assert rd(u,cell+1,1)==0x48 and rd(u,0xffff21ae)==50 and events==[0x9d00]
w(u,0xffff21ae,3);u.reg_write(UC_M68K_REG_A0,a);run(u,0xad82);assert rd(u,0xffff21ae)==50 and len(events)==1
print('PASS 0C opens adjacent elevator exit and refreshes closing timer; no floor travel command')
