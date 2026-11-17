"""Disruptor placement and selection, running the real Use dispatcher."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys

MAP, INV = 0xffff305a, 0xffff2f50
PLACED = 0x12

def new(rom, camp, x, z, y, items, slot, fill=0):
    u=machine(rom)
    u.mem_write(MAP,bytes([fill])*4000)
    run(u,0x4948,0x495e)  # native map row offsets (used by $AB3E)
    w(u,S['CAMP'],camp)
    w(u,0xffff26b8,0x2106,4)
    w(u,0xffff26e2,0,1)
    w(u,0xffff2715,0,1)
    w(u,0xffff441a,x)
    w(u,0xffff441c,y)
    w(u,0xffff441e,z)
    w(u,0xffff4440,80)
    w(u,0xffff2442,MAP+700,4)  # stale cached cell well away from the player
    u.mem_write(INV,bytes(items)+b'\xff'*(52-len(items)))
    w(u,0xffff2740,slot)
    w(u,0xffff21ba,items[slot])
    for p in (0x6eda,0x6738):
        u.mem_write(p,b'\x4e\x75')
    return u

def cell(x,z):
    return MAP+(49-(z>>8))*80+(x>>8)

def chosen(u):
    return rd(u,INV+rd(u,0xffff2740),1)

x,z=0x1480,0x0a80
target=cell(x,z)
items=[2,255,8,9,8,255,8,7]
if len(sys.argv)==2:
    old=Path(sys.argv[1]).read_bytes()
    u=new(old,1,x,z,300,items,2)
    run(u,0x72ac)
    assert rd(u,MAP+700,1)==PLACED and rd(u,target,1)==0
    assert chosen(u)!=8
    print('PASS baseline shows stale-cell placement and selection changing away from remaining Disruptors')

for camp in (0,1):
    for y in (0,80,81,300):
        u=new(R,camp,x,z,y,items,2)
        run(u,0x72ac)
        assert rd(u,target,1)==PLACED and rd(u,MAP+700,1)==0
        assert u.mem_read(MAP,4000).count(PLACED)==1
        assert u.mem_read(INV,52).count(8)==2 and chosen(u)==8
        assert rd(u,0xffff21ba)==8
        run(u,0x72ac)
        assert u.mem_read(MAP,4000).count(PLACED)==2
        assert rd(u,target-81,1)==PLACED  # same first fallback as the native search
        assert u.mem_read(INV,52).count(8)==1 and chosen(u)==8
        run(u,0x72ac)
        assert u.mem_read(INV,52).count(8)==0 and chosen(u) in (7,9)
print('PASS grounded and airborne placements match; fallback only uses empty cells; selection follows remaining Disruptors')

for x,z,fill,success in [(0x1480,0xa80,0x81,False),(0x5000,0xa80,0,False),
                        (0x1100,0xffff,0,False),(0,0,0,True),(0x4fff,0x31ff,0x81,False)]:
    u=new(R,0,x,z,300,[8],0,fill)
    before=bytes(u.mem_read(MAP-81,4162))
    run(u,0x72ac)
    if success:
        after=bytes(u.mem_read(MAP-81,4162))
        assert [i for i,(a,b) in enumerate(zip(before,after)) if a!=b]==[81+cell(x,z)-MAP]
        assert rd(u,cell(x,z),1)==PLACED and chosen(u)==255
    else:
        assert u.mem_read(MAP-81,4162)==before and chosen(u)==8
print('PASS invalid/blocked placement consumes nothing; edge placement cannot write outside map; empty inventory returns')
