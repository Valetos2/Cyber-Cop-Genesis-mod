exec(open('v36/test_core.py').read().split('levels=json')[0])
u=machine();u.mem_write(0x200000,b'\xff'*0x4000);saved={}
for camp in [0,1]:
 w(u,S['CAMP'],camp);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,3+camp);run(u,0x4882)
 # Distinct persistent door flags, inventory and state in each namespace.
 u.mem_write(0xffff2718,bytes(range(16)) if not camp else bytes(range(16,32)))
 u.mem_write(0xffff2a26,bytes([0x20+camp])*12)
 run(u,0x8faa);run(u,V['save21'])
 saved[camp]={a:bytes(u.mem_read(a,n)) for a,n in [(0xffff25b4,24),(0xffff2a3a,768),(0xffff2718,16),(0xffff2f8e,80),(0xffff2a26,12),(0xffff2f50,52),(0xffff2740,2),(0xffff2fea,32)]}
sram=bytes(u.mem_read(0x200000,0x4000))
for camp in [0,1]:
 v=machine();v.mem_write(0x200000,sram);w(v,S['CAMP'],camp);run(v,V['load21']);assert v.reg_read(UC_M68K_REG_D0)==1;assert rd(v,0xffff0124,1)==1
 run(v,0xe94,0x124a);assert rd(v,S['CAMP'])==camp
 # Exercise the real restore sections, stopping at native continuation points.
 w(v,0xffff2712,255,1);run(v,V['restore21_floor'],0x1f66)
 for a in [0xffff2a3a,0xffff2f8e]:assert bytes(v.mem_read(a,len(saved[camp][a])))==saved[camp][a],(camp,hex(a))
 # Skip renderer refresh; the same SRAM restore is otherwise unmodified.
 v.mem_write(0x2ca0,b'\x4e\x75');v.mem_write(0x33b6,b'\x4e\x75');run(v,V['restore21_terminal'],0x1fbc)
 assert bytes(v.mem_read(0xffff2718,16))==saved[camp][0xffff2718]
 v.mem_write(0x6e98,b'\x4e\x75');v.mem_write(0x150b4,b'\x4e\x75');run(v,V['restore21_late'],0x2074)
 for a in [0xffff2a26,0xffff2f50,0xffff2740,0xffff2fea]:assert bytes(v.mem_read(a,len(saved[camp][a])))==saved[camp][a],(camp,hex(a))
 # Corruption of one extension must reject that continue without touching other.
 bad=bytearray(sram);bad[camp*0x2000+0x51+200]^=1
 v=machine();v.mem_write(0x200000,bytes(bad));w(v,S['CAMP'],camp);run(v,V['load21']);assert v.reg_read(UC_M68K_REG_D0)==0
 w(v,S['CAMP'],1-camp);run(v,V['load21']);assert v.reg_read(UC_M68K_REG_D0)==1
print('PASS both complete SRAM restores, distinct inventory/flags/doors/body/items, corrupt-slot isolation')
