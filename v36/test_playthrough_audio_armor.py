"""Confirm the behavior reported in the user-provided Kega saves gs15 and gs16."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys

def from_save(path):
    u=machine()
    u.mem_write(0xffff0000,Path(path).read_bytes()[0x2478:0x12478])
    return u

for toggle in (255,0):
    u=from_save(sys.argv[1])
    assert rd(u,0xffff2710,1)==255 and rd(u,0xffff26b8,4)==0x8d42
    w(u,0xffff2710,toggle,1);w(u,0xffff7d2a,0)
    u.mem_write(0x51bc,b'\x4e\x75')
    run(u,0x8e22,0x8e34)
    assert rd(u,0xffff7d2c)==(1 if toggle else 2)
print('PASS gs15 arrival: Music Off sends stop, Music On starts the normal track')

for armor in (3,2):
    u=from_save(sys.argv[2])
    a=0xffff4e26
    assert rd(u,0xffff2a24)==3 and not rd(u,0xffff0106,1) and rd(u,a+2)==0x801c
    w(u,0xffff2a24,armor)
    w(u,a+0x34,2);w(u,0xffff26fb,0,1)
    u.reg_write(UC_M68K_REG_A0,a)
    shots=[]
    def projectile(uc,*args):
        shots.append(rd(uc,0xffff2228))
    u.hook_add(UC_HOOK_CODE,projectile,begin=0xca72,end=0xca72)
    run(u,0xc342,0xc388)
    assert shots==[6]
    body=lambda:sum(rd(u,0xffff2f92+i*8) for i in range(10))
    prior=body()
    u.reg_write(UC_M68K_REG_D4,shots[0])
    run(u,0xad06)
    assert body()-prior==3-armor
print('PASS gs16 regenerating robot: shot strength six; Armor 3 absorbs it, Armor 2 takes one')
