"""Exercise the complete Scanman Use, pad navigation and palette setup."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
view, focus, inv, palette=0xffff26b8,0xffff202a,0xffff270a,0xffff285c
defaults=R[0x8a5c:0x8a6c]

def opened(rom,mouse,via,camp,save=None):
    u=machine(rom)
    if save:
        u.mem_write(0xffff0000,save.read_bytes()[0x2478:0x12478])
    else:
        u.mem_write(0xffff2f50,bytes([0xff])*52)
        w(u,0xffff2f50+39,0x1c,1) # Scanman
        w(u,0xffff2f50+11,0x1b,1) # Screen 3
    for addr in (0x2930,0x4d18,0x1646,0x249c):
        u.mem_write(addr,b'\x4e\x75')
    w(u,view,0x2106,4);w(u,focus,0x56a8,4);w(u,inv,0,1)
    for addr in (0xffff270e,0xffff26e2,0xffff2715):w(u,addr,0,1)
    w(u,S['CAMP'],camp);w(u,0xffff0200,mouse);w(u,0xffff01a0,mouse)
    w(u,0xffff2740,39);w(u,0xffff21ba,0x1c)
    w(u,0xffff0010,2);w(u,0xffff0012,0)
    run(u,via)
    assert rd(u,view,4)==0x87c8 and rd(u,0xffff21ba)==0x1b
    return u

def pad(u,cur):
    w(u,0xffff0004,cur);w(u,0xffff0006,0xff)
    u.reg_write(UC_M68K_REG_D0,cur)
    run(u,0x5370)

if len(sys.argv)==3:
    old,gs1=(Path(p) for p in sys.argv[1:])
    u=opened(old.read_bytes(),0,0x72ac,1,gs1)
    assert rd(u,focus,4)==0x56a8
    initial=bytes(u.mem_read(palette,16))
    pad(u,0xef);assert rd(u,0xffff2178,4)!=0
    pad(u,0xfe);assert rd(u,focus,4)==0x56a8
    run(u,0x8816);assert u.mem_read(palette,16)==defaults and initial!=defaults
    u=opened(R,0,V['item_keys'],1,gs1)
    pad(u,0xef);pad(u,0xfe)
    assert rd(u,focus,4)==0x5a32 and rd(u,0xffff2178,4)!=0
    print('PASS original gs1: old dead-end and brightness mismatch reproduced; new navigation works')

for camp in (0,1):
    for via in (0x72ac,V['item_keys']):
        for mouse in (0,1):
            u=opened(R,mouse,via,camp)
            assert u.mem_read(palette,16)==defaults and rd(u,0xffff2180)==8
            if mouse:
                assert rd(u,focus,4)==0x56a8
                continue
            assert rd(u,inv,1) and rd(u,focus,4)==0x5a0a
            pad(u,0xef);assert rd(u,0xffff2178,4)!=0
            pad(u,0xfe);assert rd(u,focus,4)==0x5a32  # Up -> Reset
            pad(u,0xfe);assert rd(u,focus,4)==0x5a6e  # dimmer
            pad(u,0xef)
            assert rd(u,0xffff2180)<8 and u.mem_read(palette,16)!=defaults
            pad(u,0xfd);assert rd(u,focus,4)==0x5a32  # Down -> Reset
            pad(u,0xef)
            assert rd(u,0xffff2180)==8 and u.mem_read(palette,16)==defaults
print('PASS both campaigns: initial brightness equals Reset, joystick Use/Up/brightness/Reset, and Mouse On unchanged')
