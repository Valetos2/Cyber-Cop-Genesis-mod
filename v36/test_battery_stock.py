"""Compare battery sources in the saved equipment setup with stock Cyber-Cop."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
original=Path(sys.argv[1]).read_bytes()
fixture=Path(sys.argv[2]).read_bytes()[0x2478:0x12478]

def drain(rom,*,armor=None,phase=0):
    u=machine(rom)
    u.mem_write(0xffff0000,fixture)
    assert rd(u,0xffff26e4,1)==rd(u,0xffff26de,1)==rd(u,0xffff2298)==0
    assert rd(u,0xffff2a24)==4 and rd(u,0xffff2a26)==0x1de
    if armor is not None:w(u,0xffff2a24,armor)
    w(u,0xffff29ac,phase)
    run(u,0x324c,0x32d2 if phase else 0x32c4)
    return 0x1de-rd(u,0xffff2a26)

for rom in (original,R):
    assert drain(rom)==1
    assert all(drain(rom,phase=p)==0 for p in range(1,16))
    assert drain(rom,armor=3)==0
print('PASS original and current ROM agree: gs2 Armor 3 drains one charge per 16 updates with other drains off')
