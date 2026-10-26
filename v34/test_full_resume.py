exec(open('v34/common.py').read())
u=machine();u.mem_write(0xffff0000,Path('upload/Cyber-Cop_v19.gs4').read_bytes()[0x2478:0x12478])
w(u,0xffff2718+rd(u,0xffff2606),255,1) # simulate already used terminal on this floor
run(u,0x8faa);pw=bytes(u.mem_read(0xffff25b4,24));print('Native encoded password',pw)
run(u,L['save21']);saved=bytes(u.mem_read(0x200000,0x1000))
ranges=[(0xffff2a3a,768),(0xffff2718,16),(0xffff2f8e,80),(0xffff2a26,12),(0xffff2f50,52),(0xffff2740,2),(0xffff2fea,32)]
expect={a:bytes(u.mem_read(a,n)) for a,n in ranges}
u=machine();u.mem_write(0x200000,saved);run(u,L['load21']);assert rd(u,0xffff0124,1)==1
run(u,0xe94,0x124a)
# Boot through the genuine new-game/password initialization; stub hardware only.
for a in [0x1612,0x1646,0x2930,0x249c,0x150d8,0x150b4,0x2580,0x31b0,0x1602]:u.mem_write(a,b'\x4e\x75')
w(u,0xffff2712,255,1);run(u,0x1ee0,0x207a)
for a,n in ranges:assert bytes(u.mem_read(a,n))==expect[a],(hex(a),bytes(u.mem_read(a,n)).hex(),expect[a].hex())
assert rd(u,0xffff26bc)==64
# Used terminal cannot grant access again after this full initialization.
w(u,0xffff216e,0);before=rd(u,0xffff26bc);run(u,0x7d76);assert rd(u,0xffff26bc)==before
print('Native encoder -> SRAM -> native decoder -> full initialization: exact checkpoint, used terminal does not grant access again')
