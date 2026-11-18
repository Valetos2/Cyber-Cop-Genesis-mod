"""Exercise SRAM byte handling, campaign separation and fallbacks."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys

PRIOR = Path(sys.argv[1]).read_bytes()
BUS, SIDE, MUSIC, SOUND = 0x200000, 0x805, 0xffff2710, 0xffff2711

def fresh(rom=R, sram=bytes([255])*0x4000):
    u=machine(rom)
    u.mem_write(0xffff0000,bytes(65536))
    u.mem_write(BUS,sram)
    return u

def checkpoint(u,camp,flags):
    w(u,S['CAMP'],camp)
    run(u,0x2360);run(u,0x2944);run(u,0x4832)
    w(u,MUSIC,0 if flags&2 else 255,1);w(u,SOUND,0 if flags&1 else 255,1)
    run(u,0x8faa);run(u,V['save21'])
    return bytes(u.mem_read(BUS,0x4000))

def resume(sram,camp,flags,manual=False,fallback=False):
    u=fresh(sram=sram)
    u.mem_write(0x6e98,b'\x4e\x75');u.mem_write(0x6e86,b'\x4e\x75')
    # Pretend options have just been initialized oppositely on cold boot.
    w(u,MUSIC,0 if not flags&2 else 255,1);w(u,SOUND,0 if not flags&1 else 255,1)
    run(u,S['resume_mission36' if camp else 'resume_original36'],0x124a)
    if manual:w(u,0xffff0124,0,1)
    run(u,0x2066,0x2074)
    got=2*(not rd(u,MUSIC,1))+(not rd(u,SOUND,1))
    assert got==(flags^3 if manual or fallback else flags),(camp,got,flags,manual)
    if not manual: assert rd(u,0xffff7d2c)==(2 if (flags^3 if fallback else flags)&2 else 1)
    return u

for flags in range(4):
    u=fresh()
    writes=[]
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,acc,a,n,d,ud:writes.append((a,n)), begin=BUS,end=BUS+0x3fff)
    sram=checkpoint(u,0,flags)
    assert sram[0x2000:]==bytes([255])*0x2000
    sram=checkpoint(u,1,flags^3)
    for camp,expected in [(0,flags),(1,flags^3)]:
        off=camp*0x2000
        assert sram[off+SIDE:off+SIDE+10:2]==bytes([0xa1,sram[off+0x4d],sram[off+0x4f],expected,expected^255])
        resume(sram,camp,expected)
        for offset in (0,2,8):
            corrupt=bytearray(sram);corrupt[off+SIDE+offset]^=1
            resume(bytes(corrupt),camp,expected,fallback=True)
        resume(sram,camp,expected,manual=True)
    assert all(a&1 and n==1 and (a-BUS)%0x2000<=SIDE+8 for a,n in writes)

sram=checkpoint(fresh(PRIOR),0,0)
assert sram[SIDE:SIDE+10]==bytes([255])*10
resume(sram,0,0,fallback=True)
print('PASS all four sound settings, both campaigns, legacy/corrupt SRAM fallback, and odd-lane writes')
