"""Reproduce the stale HUD energy tiles at the sleep mode change."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
previous=Path(sys.argv[1]).read_bytes()

def meter(rom,ram,awake):
    u=machine(rom)
    u.mem_write(0xffff0000,ram)
    w(u,0xffff26b8,0x2106,4)
    tiles={}
    def collect(uc,*_):
        a=uc.reg_read(UC_M68K_REG_D2)&0xffff
        if a in range(0xe904,0xe90c,2):tiles[a]=uc.reg_read(UC_M68K_REG_D0)&0xffff
    for p in (0x35fe,0x3852):u.mem_write(p,b'\x4e\x75')
    u.hook_add(UC_HOOK_CODE,collect,begin=0x35fe,end=0x35fe)
    if not awake:run(u,0x6fc8,0x6fd2)
    run(u,0x33e2)
    assert len(tiles)==4,tiles
    return tiles
for path in sys.argv[2:]:
    ram=Path(path).read_bytes()[0x2478:0x12478]
    orig=meter(previous,ram,True)
    first=meter(previous,ram,False)
    patched=meter(R,ram,False)
    assert orig!=first and orig==patched,(orig,first,patched)
    print(Path(path).suffix, 'awake',list(orig.values()), 'old sleep flash',list(first.values()), 'fixed',list(patched.values()))
# Normal recovery still updates the cache after the entry seed.
u=machine()
w(u,0xffff2a2a,0x80);w(u,0xffff20e4,0)
run(u,0x6fc8,0x6fd2)
assert rd(u,0xffff015c)==0x80
w(u,0xffff20e4,0x100);w(u,0xffff2798,300);w(u,0xffff015a,0)
run(u,V['sleep33_bar'])
assert rd(u,0xffff015c)==0x90
print('PASS sleep entry retains awake bar; gradual recovery still updates the HUD')
