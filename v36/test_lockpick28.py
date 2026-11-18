"""Execute the decoder and keypad confirmation against packed decimal codes."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
old=Path(sys.argv[1]).read_bytes() if len(sys.argv)>1 else None
saves=[Path(a).read_bytes()[0x2478:0x12478] for a in sys.argv[2:]]

def check(rom,code,*,alarm=False,broken=False,fixture=None,late_alarm=False):
    u=machine(rom)
    if fixture:u.mem_write(0xffff0000,fixture)
    for p in (0x38c8,0x4d18,0x2930,0x7994,0x150d8,0x2190,0x9956,0x9d5c):
        u.mem_write(p,b'\x4e\x75')
    view=0xffff26b8
    w(u,view,0x9916,4)
    w(u,0xffff21a2,0x9b52,4);w(u,0xffff21a6,0x9c50,4)
    w(u,0xffff227e,0xffff7dc6,4)
    w(u,0xffff2438,0x4321);w(u,0xffff243a,code)
    w(u,0xffff29ba,1 if alarm else 0)
    w(u,0xffff0004,0xff)
    u.reg_write(UC_M68K_REG_D7,0x40 if broken else 0)
    run(u,0x9bdc)
    if alarm or broken:
        assert rd(u,view,4)==0x9916
        return False
    assert rd(u,view,4)==0x98dc
    if late_alarm:w(u,0xffff29ba,1)
    w(u,0xffff21aa,0) # skip the random preview; real digit + submit handlers
    opened=[]
    errored=[]
    u.hook_add(UC_HOOK_CODE,lambda *_:opened.append(rd(u,0xffff2438)),begin=0x9c50,end=0x9c50)
    u.hook_add(UC_HOOK_CODE,lambda *_:errored.append(True),begin=0x9b3e,end=0x9b3e)
    for _ in range(5):
        run(u,0x98dc)
        if opened or errored:break
    assert bool(opened)^bool(errored),hex(code)
    if opened:assert opened==[code]
    return bool(opened)

for code in (0,1,0x12,0x7650,0x1200,0x9000,0x9283,0x1001,0x9999):
    assert check(R,code),hex(code)
assert not check(R,0x7650,alarm=True)
assert not check(R,0x7650,broken=True)
assert not check(R,0x7650,late_alarm=True)
if old:
    for saved in saves:
        c=int.from_bytes(saved[0x243a:0x243c],'big')
        assert c==0x7650 and not check(old,c,fixture=saved) and check(R,c,fixture=saved)
print('PASS four-digit decoding, including leading/trailing zeroes and 0000; alarm and broken-item gates')
