"""Run equipment, drain, movement, hit and death dispatch from both builds."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
stock=Path(sys.argv[1]).read_bytes()
for rom in (stock,R):
 for armor in range(5):
    for charge in (0,1,0x200):
        u=machine(rom)
        w(u,0xffff2fde,int(bool(armor)))
        w(u,0xffff2fe0,0x22+armor,1)
        run(u,0x2a18)
        assert rd(u,0xffff2a24)==armor
        for a in (0xffff26e4,0xffff26de,0xffff0105):w(u,a,0,1)
        w(u,0xffff2298,0);w(u,0xffff29ac,0)
        w(u,0xffff2a26,charge)
        run(u,0x324c,0x32a4)
        assert rd(u,0xffff2a26)==(charge-int(armor==4))&0xffff
        if charge<=1:
            u.mem_write(0x5122,b'\x4e\x75')
            run(u,0x32a4,0x32c4)
            assert rd(u,0xffff2a26)==0 if charge==0 or armor==4 else rd(u,0xffff2a26)==1
        u.reg_write(UC_M68K_REG_D4,16)
        run(u,0xad06,0xad10)
        assert u.reg_read(UC_M68K_REG_D4)&0xffff==13-armor
        a=0xffff4412
        w(u,0xffff243c,0x1800);w(u,0xffff26fc,0,1);w(u,a+0xa,0x800);w(u,a+0x2a,0)
        u.reg_write(UC_M68K_REG_A0,a);run(u,0xa268)
        assert rd(u,a+0x2a)==0xc00
        w(u,0xffff2a2a,0x40)
        w(u,0xffff2f92,0);w(u,0xffff2fa2,0);w(u,0xffff270f,0,1)
        run(u,0x2ce2)
 for bomb,captured,expected in [(0xb,0,0x2d92),(0x4b,0,0x2d26),(0xb,1,0x2d26),(0xff,0,0x2d26)]:
    u=machine(rom)
    u.mem_write(0x2f80,b'\x4e\x75')
    w(u,0xffff2a2a,0);w(u,0xffff270f,0,1);w(u,0xffff26fa,captured,1)
    u.mem_write(0xffff2f50,bytes([bomb])+b'\xff'*51)
    run(u,0x2ce2,expected)
print('PASS armour 1–4 equip, battery drain and zero-charge movement/protection; prison needs first defeat and an intact Bomb')
