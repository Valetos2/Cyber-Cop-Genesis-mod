exec(open('v25/common.py').read())
# Fuse Box: real quick-interaction release vs native inventory activation.
def panel(hot):
 u=machine();u.mem_write(0xffff0000,Path('upload/Cyber-Cop_v23.gs3').read_bytes()[0x2478:0x12478]);w(u,0xffff26b8,0x2106,4);w(u,0xffff202a,0x5644,4);w(u,0xffff270a,0 if hot else 255,1);w(u,0xffff21bc,36);w(u,0xffff2f84,36,1);w(u,0xffff2742,0);w(u,0xffff0010,0);w(u,0xffff0022,255,1);w(u,0xffff0004,255);w(u,0xffff0006,0xbf)
 def hk(u,a,s,d):
  if a in [0x51bc,0x38bc,0x38c8,0x4d18,0x79ba,0x150b4]:ret(u)
 u.hook_add(UC_HOOK_CODE,hk);run(u,0x7afa);run(u,L['quick_interact'] if hot else 0x727c);return u
u,v=panel(True),panel(False)
for a,n in [(0x202a,4),(0x26b8,4),(0x226e,4),(0x270a,1),(0x227e,4)]:assert u.mem_read(0xffff0000+a,n)==v.mem_read(0xffff0000+a,n)
assert rd(u,0xffff270a,1)==255 and rd(u,0xffff26b8,4)==0x7a60
before=rd(u,0xffff2150);u.reg_write(UC_M68K_REG_D0,0);run(u,0x7a92);assert rd(u,0xffff2150)==(before^65535)
print('Fuse Box quick A release: native panel/cursor/input-mode state identical, switch works')
# Disruptor: robotic type even, while organic group bit0 set is not disabled.
for typ in [0x8004,0x8006,0x8119,0x811a,0x811b,0x801c]:
 u=machine();a=0xffff4468;w(u,a+2,typ);w(u,a+8,0x2880);w(u,a+12,0x1880);u.mem_write(0xffff305a,bytes(4000));w(u,0xffff305a+25*80+40,0x12,1);u.reg_write(UC_M68K_REG_A0,a);run(u,0xaee2)
 assert bool(rd(u,a+2)&0x400)==(not bool(typ&0x100)) # bit0 of high byte at offset2 is tested
 if not(typ&0x100):
  assert rd(u,a+0x3a,4)==0xbd5e and rd(u,a+0x4a,4)==0xb426
print('Disruptor discriminator confirmed: bit0 of TYPE HIGH BYTE; normal low type IDs are not the discriminator')
# Stop at free routine to verify render counter removal without running actual renderer.
u=machine();a=0xffff4468;w(u,a+2,0x8404);w(u,a+0x38,0);u.reg_write(UC_M68K_REG_A0,a)
def hk(u,pc,s,d):
 if pc==0xe624:ret(u)
u.hook_add(UC_HOOK_CODE,hk);run(u,0xe5b0,0x68d8)
print('Electrical render callback with expired counter enters object removal')
