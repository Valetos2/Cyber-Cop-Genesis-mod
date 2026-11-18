"""Validate the user save and full-row / occupied-coordinate migration."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
specs=[tuple(map(int,line.split(','))) for line in Path('v36/pickups36.csv').read_text().splitlines()]
raw=Path(sys.argv[1]).read_bytes()
sram=raw.ljust(0x4000,b'\xff')
assert len(sram)==0x4000 and sram[1:9:2]==b'CC17'
def resume(camp,bank=sram):
    u=machine()
    u.mem_write(0xffff0000,bytes(65536))
    u.mem_write(0x200000,bank)
    u.mem_write(0x1602,b'\x4e\x75')
    run(u,S['resume_mission36' if camp else 'resume_original36'],0x124a)
    run(u,V['restore21_floor'],0x1f66)
    return u
for camp in (0,1):
    u=resume(camp)
    for _,f,x,y,t in (q for q in specs if q[0]==camp):
        data=bytes(u.mem_read(0xffff2a3a+48*f,48))
        assert bytes([x,49-y,t]) in [data[i:i+3] for i in range(0,48,3)]
    assert bytes(u.mem_read(0x200000,0x4000))==sram
    # A consumed pickup must not be reinserted after a new checkpoint.
    _,f,x,y,t=next(q for q in specs if q[0]==camp)
    w(u,0xffff2606,f);run(u,0x4882)
    assert rd(u,0xffff305a+y*80+x,1)==t
    w(u,0xffff305a+y*80+x,0,1)
    run(u,0x8faa);run(u,V['save21'])
    saved=bytes(u.mem_read(0x200000,0x4000))
    v=resume(camp,saved)
    assert rd(v,0xffff305a+y*80+x,1)==0
print('PASS provided SRAM: both banks, all five additions, no disk writes on load, no respawn after checkpoint')

# Run the same migration hook on a packed full row and a row with an item
# already on the target coordinate. No array entry may be overwritten.
for data in (bytes(v for i in range(16) for v in (i,0,0x30)),
             bytes([15,10,0x30])+bytes(45)):
    u=machine();w(u,S['CAMP'],1)
    u.mem_write(0x200000,sram)
    u.mem_write(0xffff2a3a,data)
    run(u,S['pickup_restore36'],0xf8638)
    assert bytes(u.mem_read(0xffff2a3a,48))==data
print('PASS full and conflicting legacy rows unchanged')
