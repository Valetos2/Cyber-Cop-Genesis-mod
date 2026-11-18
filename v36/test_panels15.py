"""Run actual 68000 panel handlers, mouse hit/dispatch and visible border changes."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys

S35 = json.loads(Path('v35c/symbols.json').read_text())
VIEW, PAD, OWNER, MOUSE = 0xffff26b8, 0xffff0004, 0xffff01b4, 0xffff0200
LEGACY = Path(sys.argv[1]).read_bytes() if len(sys.argv) > 1 else None

def controller(u, current=0xff, previous=0xff):
    w(u, PAD, current)
    w(u, PAD+2, previous)

def setup(rom=R):
    u = machine(rom)
    for address in (0x2930, 0x150b4, 0x1646):
        u.mem_write(address, b'\x4e\x75')
    controller(u)
    w(u, MOUSE, 1)
    w(u, 0xffff01a0, 1)
    w(u, 0xffff01ac, 1)
    return u

def click(u, x, y):
    w(u, 0xffff01a4, x)
    w(u, 0xffff01a6, y)
    run(u, S35['hit_test'])
    run(u, S35['press_ui'])

fuses = [0x611c + 20*i for i in range(12)] + [0x6210, 0x6224]
for i, node in enumerate(fuses):
    u = setup()
    for routine in (0x7ad6, 0x7afa, 0x7a00):
        run(u, routine)
    x, y = R[node:node+2]
    for want in (0xffff, 0):
        click(u, x*8+72, y*8)
        assert rd(u, OWNER, 4) == node
        run(u, 0x7a60)
        assert rd(u, VIEW, 4) == 0x7a60 and rd(u, 0xffff2150+2*i) == want
    # A sampled Start state that overlaps a mouse switch press is not exit.
    controller(u, 0x7f)
    run(u, 0x7a60)
    assert rd(u, VIEW, 4) == 0x7a60
    # After the left button is released, a new Start/right edge still exits.
    run(u, S35['release_ui'])
    controller(u, 0x7f, 0x7f)
    run(u, 0x7a60)
    assert rd(u, VIEW, 4) == 0x7a60
    controller(u, 0x7f)
    run(u, 0x7a60, 0x2190)

if LEGACY:
    u = setup(LEGACY)
    controller(u, 0x7f, 0x7f)
    run(u, 0x7a60, 0x2190)  # original tick exits even on old Start state
print('PASS 14 fuses toggle both ways, overlapping/stale exit ignored, fresh exit still works')

def airlock():
    u = setup()
    w(u, VIEW, 0x77a8, 4)
    w(u, 0xffff226e, 0x9af0, 4)
    w(u, 0xffff227e, 0xffff7dc6, 4)
    w(u, 0xffff2282, S['airlock_shaded_bank36e'], 4)
    w(u, 0xffff01c8, 0x5ec2, 4)
    w(u, 0xffff026c, 0x100)  # native lab: draw the action tile but stay open
    u.mem_write(0xffff7dc6, bytes(192))
    u.mem_write(0xffff8934, bytes((11*i+i//7)%256 for i in range(12288)))
    return u

def border(u):
    initial = bytes(u.mem_read(0xffff8934, 12288))
    run(u, S35['panel_border'])
    changed = bytes(u.mem_read(0xffff8934, 12288)) != initial
    run(u, S35['panel_border'])
    assert bytes(u.mem_read(0xffff8934, 12288)) == initial
    return changed

for valid, alarm, mouse in [(0,0,1),(1,1,1),(1,0,1),(1,0,0)]:
    u = airlock()
    w(u, 0xffff26ec, 255*valid, 1)
    w(u, 0xffff29ba, alarm)
    if mouse:
        click(u, 232, 80)
    else:
        run(u, 0x784c)
    assert rd(u, 0xffff7e3a) == (0xc0 if valid and not alarm else 0)
    assert border(u) == bool(valid and not alarm and mouse)
    run(u, S35['release_ui'])
    assert border(u) == bool(valid and not alarm and mouse)
    w(u, 0xffff7e3a, 0xbf)
    assert not border(u)
print('PASS airlock frame follows actual button tile after a valid mouse click only')

for auth in (False, True):
    u = setup()
    w(u, VIEW, 0x7c42, 4)
    w(u, 0xffff7e62, 0x9a if auth else 0x96)
    w(u, 0xffff26ef, 0, 1)
    u.mem_write(0xffff2f50, b'\x06')
    w(u, 0xffff2740, 0)
    w(u, 0xffff21ba, 6)
    w(u, 0xffff2715, 0, 1)
    run(u, 0x72ac)
    assert bool(rd(u, 0xffff26ef, 1)) == auth
    # Access command can be dispatched only after insertion.
    w(u, 0xffff2606, 4)
    w(u, 0xffff216e, 0)
    w(u, 0xffff26bc, 0)
    w(u, 0xffff271c, 0, 1)
    u.mem_write(0x7dc2, b'\x4e\x75')
    u.reg_write(UC_M68K_REG_D0, 2)
    run(u, 0x7cce)
    assert rd(u, 0xffff26bc) == (32 if auth else 0)
    # Same inventory item in Computer is still accepted with no terminal card.
    w(u, VIEW, 0x8358, 4)
    w(u, 0xffff26ef, 0, 1)
    run(u, 0x72ac)
    assert rd(u, 0xffff26ef, 1) == 255
print('PASS unauthenticated terminal does not queue cable or run a command, Computer unaffected')

for pointer in (0,1):
    for name in ('gs0','gs14'):
        u = setup()
        # Known stale Use owner and coordinates in both v36a saves.
        w(u, VIEW, 0x2106, 4)
        w(u, 0xffff01a0, pointer)
        w(u, 0xffff01a4, 226 if name=='gs0' else 231)
        w(u, 0xffff01a6, 162 if name=='gs0' else 158)
        w(u, OWNER, 0x56a8, 4)
        u.mem_write(S35['hud_generate'], b'\x4e\x75')
        run(u, S35['visual_update'])
        assert bool(rd(u, 0xffff0202)) == bool(pointer)
        assert rd(u, OWNER, 4) == (0x56a8 if pointer else 0)
print('PASS stale Use owner from gs0/gs14 cannot flash in free look, real HUD click still draws')
