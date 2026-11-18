"""Compare native actor projections with and without the sprite-only offset."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
old=Path(sys.argv[1]).read_bytes()
initialization=Path('v36/compare_barrels_lamp04.py').read_text()
initialization=initialization[initialization.index(' u=machine()'):initialization.index(' for a in [0x3b46')]
exec('def setup(rom):\n'+initialization.replace('machine()','machine(rom)')+' return u\n')

def ground_parts(rom,biped,offset,x,dead=False):
    u=setup(rom)
    u.reg_write(UC_M68K_REG_D0,x*256+128)
    u.reg_write(UC_M68K_REG_D2,26*256+128)
    run(u,biped)
    a=u.reg_read(UC_M68K_REG_A0)
    frame=rd(u,a+0x20)+offset
    if dead:w(u,a+2,6)
    w(u,a+0x20,frame)
    before=bytes(u.mem_read(a,0x56))
    run(u,0x3b46);run(u,0x3b7c)
    u.reg_write(UC_M68K_REG_A0,a)
    run(u,0x44e0)
    after=bytes(u.mem_read(a,0x56))
    assert before[2:14]==after[2:14] and before[0x1a:]==after[0x1a:]
    return after[:0x10]+after[0x12:],rd(u,a+0x10)

for facing in range(8):
    for x in (39,41):
        a,y0=ground_parts(old,0x4038,facing,x)
        b,y1=ground_parts(R,0x4038,facing,x)
        assert a==b and y0-y1==4,(y0,y1)
a,y0=ground_parts(old,0x4038,0,41,dead=True)
b,y1=ground_parts(R,0x4038,0,41,dead=True)
assert a==b and y0-y1==4
for other in (0x4144,0x4250,0x4438):
    assert ground_parts(old,other,0,41)==ground_parts(R,other,0,41)
print('PASS all eight angles lower four pixels at six cells; other actors and gameplay fields unchanged')
