"""Run the actual controller path to check repair focus."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
FOCUS=0xffff202a
REPAIR=0x566c
u=machine()
for a in (0x1646,0x2930,0x4d18):u.mem_write(a,b'\x4e\x75')
w(u,0xffff26b8,0x2106,4);w(u,FOCUS,REPAIR,4)
w(u,0xffff270a,255,1);w(u,0xffff270e,0,1)
w(u,0xffff214c,0);u.mem_write(0xffff202e,bytes(128))
def pad(cur,prev):
    w(u,0xffff0004,cur);w(u,0xffff0006,prev)
    u.reg_write(UC_M68K_REG_D0,cur);run(u,0x5370)
pad(0xef,0xff)
assert rd(u,0xffff202e,4)==0x7192 and rd(u,0xffff214c)==0
pad(0xe7,0xef)  # B + Right before the first repair tick
assert rd(u,FOCUS,4)==REPAIR
run(u,0x7192)
assert rd(u,0xffff214c)==1
pad(0xeb,0xef)  # B + Left while the repair counter is ticking
assert rd(u,FOCUS,4)==REPAIR
pad(0xff,0xef)
assert rd(u,0xffff202e,4)==0 and rd(u,0xffff214c)==0
pad(0xf7,0xff)
assert rd(u,FOCUS,4)!=REPAIR
print('PASS real gamepad B+direction locks Repair before and during ticking; release cleans up and restores navigation')
