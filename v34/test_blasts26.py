exec(open('v34/common.py').read())
# bounded cell lookup, specifically X > 50; all coordinates remain inside map.
u=machine();run(u,0x2360);u.mem_write(0xffff305a,bytes([0x95]*4000));u.reg_write(UC_M68K_REG_D0,70*256);u.reg_write(UC_M68K_REG_D2,25*256);run(u,0xab3e)
assert rd(u,0xffff305a+24*80+70,1)!=0x95
# Grenade terrain loop visits exactly 121 positions while preserving object registers.
u=machine();a=0xffff4468;w(u,a+8,40*256);w(u,a+12,25*256);u.reg_write(UC_M68K_REG_A0,a);hits=[]
def hk(u,pc,s,d):
 if pc==0xab3e:
  hits.append((u.reg_read(UC_M68K_REG_D0)&65535,u.reg_read(UC_M68K_REG_D2)&65535));u.reg_write(UC_M68K_REG_D0,65535);u.reg_write(UC_M68K_REG_D2,0x15);ret(u)
u.hook_add(UC_HOOK_CODE,hk);run(u,L['grenade26_map'],0x81e2)
assert len(hits)==len(set(hits))==121
assert set(hits)=={(x*256,z*256) for x in range(35,46) for z in range(20,31)}
assert rd(u,a+0x2e)==300
# No widening of map/RAM. Eye preserves both coordinates around cell destruction.
u=machine();u.reg_write(UC_M68K_REG_D0,0x4000);u.reg_write(UC_M68K_REG_D2,0x2000)
def hk2(u,pc,s,d):
 if pc==0xab3e:u.reg_write(UC_M68K_REG_D0,65535);u.reg_write(UC_M68K_REG_D2,0);ret(u)
u.hook_add(UC_HOOK_CODE,hk2);run(u,L['eye26_cell'],0x7680);assert u.reg_read(UC_M68K_REG_D0)&65535==0x4100 and u.reg_read(UC_M68K_REG_D2)&65535==0x2000
print('PASS bounded eastern-map lookup, 121 grenade cells, Eye coordinate preservation')
