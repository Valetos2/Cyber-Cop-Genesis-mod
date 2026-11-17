exec(open('v36/test_core.py').read().split('levels=json')[0])
VIEW, INV, P = 0xffff26b8, 0xffff270a, 0xffff0200

def setup(mouse, inventory):
    u = machine()
    w(u, VIEW, 0x2106, 4)
    w(u, P, mouse)
    w(u, INV, inventory, 1)
    w(u, 0xffff270e, 0, 1)
    w(u, 0xffff270f, 0, 1)
    w(u, 0xffff202a, 0x56a8, 4)
    # No hardware VBlank in this CPU test; run real sleep and item logic.
    for a in (0x2930, 0x4d18, 0x1646, 0x7994, 0x150d8, 0x249c, 0x9342):
        u.mem_write(a, b'\x4e\x75')
    return u

def start(u):
    u.reg_write(UC_M68K_REG_D0, 0x7f)
    w(u, 0xffff0004, 0x7f)
    w(u, 0xffff0006, 0xff)
    run(u, 0x5370)

for pad, inv in [(0, 0), (255, 255)]:
    u = setup(1, inv)
    w(u, 0xffff0150, pad, 1)
    start(u)
    assert rd(u, VIEW, 4) == 0x7070 and rd(u, 0xffff0118, 1) == 1
    run(u, 0x7070, 0x7088)
    run(u, 0x7088)  # still physically held, no new press
    assert rd(u, VIEW, 4) == 0x7070
    w(u, 0xffff0004, 0xff)
    run(u, 0x7088)
    if inv:
        w(u, P, 0)  # disabling mouse within this sleep doesn't disable Start wake
    start(u)
    run(u, 0x7088, 0x2190)
    assert rd(u, VIEW, 4) == 0x2106 and not rd(u, 0xffff0864, 1)

u = setup(0, 0)
start(u)
assert rd(u, VIEW, 4) == 0x2106 and rd(u, INV, 1) == 255
print('PASS Start sleep and wake, held Start ignored, Mouse Off retains inventory')

for item, refill, supply, panel, applied in [
    (0x12, 0x13, 0xffff272e, 0x8576, 0xffff26f1), # Drink / Refill
    (0x14, 0x15, 0xffff272c, 0x8476, 0xffff26f0), # Medi Kit / Chemicals
    (0x07, 0x06, 0, 0x8358, 0xffff26ef),         # Computer / Program
]:
    for mouse, inv in [(0, 0), (0, 255), (1, 0)]:
        u = setup(mouse, inv)
        u.mem_write(0xffff2f50, bytes([item, refill]) + b'\xff' * 50)
        w(u, 0xffff2740, 0)
        w(u, 0xffff21ba, item)
        w(u, 0xffff26e2, 0, 1)
        w(u, 0xffff2715, 0, 1)
        if supply:
            w(u, supply, 0)
        w(u, 0xffff0010, 2)
        w(u, 0xffff0012, 0)
        run(u, V['item_keys'])
        assert rd(u, VIEW, 4) == panel and rd(u, 0xffff2740) == 1
        assert rd(u, 0xffff21ba) == refill
        assert rd(u, INV, 1) == (255 if mouse or inv else 0)
        if not (mouse or inv):
            for edge, want in [(4, item), (1, refill)]:
                w(u, 0xffff0010, edge)
                run(u, V['item_keys'])
                assert rd(u, 0xffff21ba) == want and rd(u, INV, 1) == 0
            w(u, 0xffff0010, 2)
        run(u, V['item_keys'])  # a second Y uses the preselected item
        assert rd(u, applied, 1) == 255
        assert rd(u, INV, 1) == (255 if mouse or inv else 0)
print('PASS Drink, Medi Kit and Computer hotkeys outside/inside inventory and with mouse enabled')
