"""Verify fuse tiles, world lighting, and recovery using the assembled 68000 code."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
import struct

VIEW, STATE, PANEL, AGE = 0xffff26b8, 0xffff2150, 0xffff81c6, 0xffff086c
OFFSETS = struct.unpack_from('>14H', R, 0x7aba)
MAP_SLOTS = (0,1,2,3,4,5,14,5,6,7,8,9,10,11,12,13)

def scene(rom=R, save=None):
    u = machine(rom)
    if save:
        u.mem_write(0xffff0000, save.read_bytes()[0x2478:0x12478])
    for addr in (0x2930, 0x150b4, 0x1646):
        u.mem_write(addr, b'\x4e\x75')
    return u

def statuses(u):
    return tuple(bool(rd(u, STATE+i*2)) for i in range(14))

def display(u):
    return tuple(rd(u, PANEL+i) for i in OFFSETS)

def assert_display(u):
    assert display(u) == tuple(0xee if off else 0xed for off in statuses(u))

def set_view(u, view):
    w(u, VIEW, view, 4)

def lamps(u):
    u.mem_write(0xffff8934, bytes(12288))
    for i, x in enumerate((7, 96, 64, 4, 14)):
        w(u, 0xffff533c+i*2, x)
    w(u, 0xffff5338, 0xffff5346, 4)
    run(u, 0x4584, 0x458a)
    return any(u.mem_read(0xffff8934, 12288))

if len(sys.argv) == 4:
    legacy, gs0, gs1 = (Path(p) for p in sys.argv[1:])
    u = scene(legacy.read_bytes(), gs0)
    run(u, 0x507a)
    assert all(tile==0xee for tile in display(u)) and rd(u, 0xffff2706, 1)==255
    u = scene(R, gs0)
    assert not lamps(u)
    run(u, 0x507a)
    assert all(statuses(u)) and rd(u, 0xffff2706, 1)==0
    assert_display(u)
    print('PASS gs0: legacy contradictory state reproduced; automatic import matches the visible switch, extinguishes world and lamps')

    old = scene(legacy.read_bytes(), gs1)
    before = statuses(old)
    set_view(old, 0x2106)
    for n in range(1,13):
        w(old, 0xffff29ac, (0xf4+n)&255)
        run(old, 0x3302)
        assert [i for i,(a,b) in enumerate(zip(before,statuses(old))) if a!=b]==([0,11] if n==12 else [])
    assert [i for i,(a,b) in enumerate(zip(display(old), (0xee if off else 0xed for off in before))) if a!=b]==[11]

    u = scene(R, gs1)
    # Native exit via Start/translated right-click; leave VRAM waits stubbed.
    w(u, 0xffff0004, 0x7f)
    w(u, 0xffff0006, 0xff)
    run(u, 0x7a60, 0x2190)
    set_view(u, 0x2106)
    for n in range(1,13):
        w(u, 0xffff29ac, (0xf4+n)&255)
        run(u, 0x3302)
    run(u, 0x7a00)
    assert statuses(u)==before and rd(u, AGE)==0
    assert_display(u)
    print('PASS gs1: legacy switch 11 restores after 12 world ticks; fixed save reopens with the same three switches on')

for lab in (0, 0x100, 0x101):
    for camp in (0, 1):
        u = scene()
        w(u, 0xffff026c, lab)
        w(u, S['CAMP'], camp)
        set_view(u,0x2106)
        w(u, 0xffff26e2, 0, 1)
        run(u, 0x7ad6)
        run(u, 0x7afa)
        run(u, 0x7a00)
        for i in range(14):
            u.reg_write(UC_M68K_REG_D0, i)
            run(u, 0x7a92)
            assert statuses(u)==tuple(j<=i for j in range(14))
            assert_display(u)
        for floor, slot in enumerate(MAP_SLOTS):
            for i in range(14):
                w(u, STATE+i*2, 0xffff if i==slot else 0)
            w(u, 0xffff2606, floor)
            run(u, 0x507a)
            assert bool(rd(u,0xffff2706,1))==(slot==14)
        w(u, 0xffff26e2, 0, 1)
        set_view(u,0x2106)
        run(u,0x7a00)
        assert_display(u)
print('PASS all fourteen independent switches and all native floor mappings, both campaigns and both lab flags')

u = scene()
set_view(u, 0x2106)
w(u, 0xffff26e2, 0, 1)
run(u, 0x7ad6)
run(u, 0x7afa)
w(u, AGE, 255)
run(u, 0x7a00)
assert rd(u, AGE)==0
w(u, AGE, 255)
u.reg_write(UC_M68K_REG_D0, 11)
run(u, 0x7a92)
assert rd(u, AGE)==0
for destroyed in (False, True):
    set_view(u, 0x2106)
    if destroyed:
        w(u, AGE, 255)
        run(u,0x7b12)
        assert all(statuses(u)) and rd(u,AGE)==0
    w(u, AGE, 243)
    divider = rd(u, 0xffff0134)
    for view in (0x7070, 0x7a60):
        set_view(u, view)
        for _ in range(270):
            run(u, 0x3302)
        assert rd(u, AGE)==243 and rd(u,0xffff0134)==divider
    set_view(u, 0x2106)
    for _ in range(12):
        run(u, 0x3302)
    assert rd(u, AGE)==255
    if destroyed:
        for opportunity in range(19):
            w(u, AGE, 255)
            run(u, 0x3302)
            assert rd(u, 0xffff0134)==opportunity+1 and all(statuses(u))
        w(u, AGE, 255)
    # The RNG picks switch 11. A stale pointer to another panel must not be written.
    w(u, 0xffff2294, 0x4f3228eb, 4)
    w(u, 0xffff227e, 0xffff7dc6, 4)
    mark = bytes(u.mem_read(0xffff7dc6, 196))
    run(u, 0x3302)
    assert rd(u, AGE)==0 and not statuses(u)[11]
    assert bytes(u.mem_read(0xffff7dc6, 196))==mark
    assert rd(u,0xffff0134)==0
print('PASS opening and switching reset recovery; sleep freezes both counters; automatic repair and destroyed delay preserved')
