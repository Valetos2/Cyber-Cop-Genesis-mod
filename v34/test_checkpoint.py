exec(open('v34/common.py').read())
u=machine();pw=Path('upload/Cyber-Cop_v19.srm').read_bytes()[1::2][4:28]
u.mem_write(0xffff2580,pw);run(u,0xe94,0x124a)
d=[rd(u,0xffff2f92+i*8) for i in range(10)];assert sum(d)==93 and d[0]<8 and d[2]<16,d
w(u,0xffff270f,0,1);run(u,0x2ce2);print('Legacy password alive; total damage preserved:',d)
# Empty tail -> compatible legacy save, full checkpoint -> exact restore.
u.mem_write(0x200000,Path('upload/Cyber-Cop_v19.srm').read_bytes());run(u,L['load21']);assert rd(u,0xffff0124,1)==0 and u.reg_read(UC_M68K_REG_D0)==1
u.mem_write(0xffff25b4,pw);w(u,0xffff2606,1);w(u,0xffff2608,0);u.mem_write(0xffff305a,bytes(4000));u.mem_write(0xffff305a+87,b'\x25')
u.mem_write(0xffff2718,bytes([255,255])+bytes(14));w(u,0xffff2a2a,113);w(u,0xffff2a26,399)
u.mem_write(0xffff2f50,bytes([0,7,0x47])+b'\xff'*49);w(u,0xffff2740,2)
run(u,L['save21']);assert rd(u,0xffff2608)==0
ranges=[(0xffff2a3a,768),(0xffff2718,16),(0xffff2f8e,80),(0xffff2a26,12),(0xffff2f50,52),(0xffff2740,2)]
expected={a:bytes(u.mem_read(a,n)) for a,n in ranges}
assert expected[0xffff2a3a][48:96]==bytes([7,48,37])+bytes(45)
run(u,L['load21']);assert rd(u,0xffff0124,1)==1
for a,n in ranges:u.mem_write(a,bytes(n))
w(u,0xffff2712,255,1)
# Native floor loading and HUD are separate tested components: isolate restore order.
for a in [0x4832,0x2ca0,0x33b6,0x6e98]:u.mem_write(a,b'\x4e\x75')
run(u,L['restore21_floor'],0x1f66);run(u,L['restore21_terminal'],0x1fbc);run(u,L['restore21_late'],0x2074)
for a,n in ranges:assert bytes(u.mem_read(a,n))==expected[a],hex(a)
assert rd(u,0xffff0124,1)==0
print('Full checkpoint round-trip: floor items, terminal flags, exact body/energy/battery/ammo/inventory/selection OK')
# Corruption and password mismatch must not activate the tail.
w(u,0x200081,rd(u,0x200081,1)^1,1);run(u,L['load21']);assert rd(u,0xffff0124,1)==0 and u.reg_read(UC_M68K_REG_D0)==0
print('Corrupt extension rejected instead of silently discarding floor history')
