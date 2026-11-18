"""Verify the four known-label saves without injecting replacement equipment."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
assert len(sys.argv)==5
for expected, path in enumerate(sys.argv[1:],1):
    raw=Path(path).read_bytes()
    assert raw[:3]==b'GST'
    u=machine()
    u.mem_write(0xffff0000,raw[0x2478:0x12478])
    gear=0xffff2fde
    armor,battery=0xffff2a24,0xffff2a26
    charge=rd(u,battery)
    assert rd(u,gear)==1 and rd(u,gear+2,1)==0x22+expected
    assert rd(u,armor)==expected
    run(u,0x2a18)  # derive the profile again from the exact equipped item
    assert rd(u,armor)==expected
    assert rd(u,0xffff26e4,1)==rd(u,0xffff26de,1)==rd(u,0xffff2298)==0
    assert not rd(u,0xffff0105,1)
    for tick in range(16):
        w(u,0xffff29ac,tick)
        run(u,0x324c,0x32c4 if tick==0 else 0x32d2)
    assert rd(u,battery)==charge-(expected==4)
    for current in (rd(u,battery),0):
        w(u,battery,current)
        u.reg_write(UC_M68K_REG_D4,16)
        run(u,0xad06,0xad10)
        assert u.reg_read(UC_M68K_REG_D4)&0xffff==13-expected
    print(f'{Path(path).suffix}: Armour {expected}, item ${expected+0x22:02X}, battery {charge} -> {charge-(expected==4)}, reduction {expected+3}')
