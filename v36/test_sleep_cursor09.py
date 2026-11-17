exec(open('v36/test_core.py').read().split('levels=json')[0])

old = json.loads(Path('v35c/symbols.json').read_text())
P, N, M = 0xffff0200, 0xffff01a0, 0xffff0180
owner, pending, active, selection = 0xffff0862, 0xffff0863, 0xffff0118, 0xffff0119
mode, sprite_x, sprite_y = 0xffff26b8, 0xffff29ce, 0xffff29c8

def fixture(sel):
    u = machine()
    u.mem_write(0x2930, bytes.fromhex("4e75")) # no asynchronous VBlank in the CPU fixture
    w(u, mode, 0x7070, 4)
    w(u, active, 1, 1)
    w(u, selection, sel, 1)
    w(u, P, 1)
    w(u, P+38, 1)
    w(u, M+18, 1, 1)
    w(u, N, 1)
    w(u, N+2, 4)
    w(u, N+4, 140)
    w(u, N+6, 106)
    w(u, 0xffff270a, 0, 1)
    w(u, 0xffff2798, 21)
    w(u, 0xffff011a, 20)
    return u

def activity(u, pad=0, dx=0, dy=0, mouse=0, held=None):
    w(u, 0xffff0004, 0xffff ^ (pad if held is None else held))
    w(u, 0xffff0006, pad)
    w(u, P+48, dx, 4)
    w(u, P+52, dy, 4)
    w(u, P+58, mouse)
    run(u, S['sleep_cursor_activity36'])

def draw_ticks(u):
    run(u, 0x7070, 0x7088)

# Every requested edge works on both pages, unlike Start and held buttons.
for sel in [0, 4, 9, 10, 11]:
    for pad in [1, 2, 4, 8, 16, 32, 64]:
        u = fixture(sel)
        run(u, old['cursor'])
        assert (rd(u, sprite_x), rd(u, sprite_y)) == (256, 230)
        activity(u, pad=pad)
        assert (rd(u, owner, 1), rd(u, pending, 1), rd(u, P+4)) == (1, 1, 0)
        run(u, old['cursor'])
        assert not (rd(u, sprite_x) or rd(u, sprite_y))
        assert (rd(u, N+4), rd(u, N+6), rd(u, P)) == (140, 106, 1)
        activity(u, held=pad)
        assert rd(u, owner, 1) == 1
        activity(u, mouse=2)
        assert (rd(u, owner, 1), rd(u, pending, 1), rd(u, P+4)) == (0, 0, 1)
        run(u, old['cursor'])
        assert (rd(u, sprite_x), rd(u, sprite_y)) == (256, 230)
u = fixture(0)
activity(u, pad=128)
assert rd(u, owner, 1) == 0
activity(u, pad=1, dx=1)
assert rd(u, owner, 1) == 0

# The very first pad edge still navigates or acts. A row that ignores an
# action still redraws once; subsequent idle ticks don't draw a second arrow.
for sel, pad, expected in [(0, 2, 1), (0, 1, 10), (4, 1, 0), (10, 8, 10), (10, 16, 10)]:
    u = fixture(sel)
    draw_calls = []
    u.hook_add(UC_HOOK_CODE, lambda *args: draw_calls.append(1),
               begin=V['sleep16_draw'], end=V['sleep16_draw'])
    activity(u, pad=pad)
    draw_ticks(u)
    assert rd(u, selection, 1) == expected
    assert rd(u, N+2) == (5 if pad == 8 else 4)
    assert rd(u, pending, 1) == 0 and len(draw_calls) == 1
    activity(u)
    draw_ticks(u)
    assert len(draw_calls) == 1

# Down from Mouse On actually draws the stationary arrow beside the slider
# and clears the old arrow. Inspect the live framebuffer, not just selection.
def arrow_pixels(u):
    base = 0xffff8934
    return bytes().join(bytes(u.mem_read(base+512*col,512)) for col in range(20,23))

u = fixture(9)
run(u, V['sleep16_draw'])
background = arrow_pixels(u)
w(u, selection, 11, 1)
activity(u, pad=2)
draw_ticks(u)
assert rd(u, selection, 1) == 9
before = arrow_pixels(u)
activity(u)
draw_ticks(u)
activity(u, pad=2)
draw_ticks(u)
after = arrow_pixels(u)
assert rd(u, selection, 1) == 10
pixels = lambda frame: {(i//512, i%512) for i, (a,b) in enumerate(zip(frame,background)) if a != b}
assert pixels(before)
assert pixels(after) == {(col,y+64) for col,y in pixels(before)}

# Returning the mouse sprite erases the native arrow on the real framebuffer.
u = fixture(9)
draw_ticks(u)
run(u, V['sleep16_draw'])
frame = lambda: bytes(u.mem_read(0xffff8934, 24*512))
mouse_frame = frame()
activity(u, pad=1)
run(u, V['sleep16_draw'])
assert frame() != mouse_frame
for dx,dy,edge in [(1,0,0),(0,-1,0),(0,0,1),(0,0,2)]:
    activity(u, pad=4)
    activity(u, dx=dx, dy=dy, mouse=edge)
    assert rd(u, owner, 1) == 0
    draw_ticks(u)
    assert frame() == mouse_frame

# Mouse Off by a real menu click, then recover at the same location using
# either button. Waking or closing the menu invalidates that recovery.
for edge in [1, 2, 4]:
    u = fixture(9)
    w(u,N+14,1)
    run(u,old['sleep_click'])
    assert (rd(u,P),rd(u,P+70)) == (0,1)
    activity(u,mouse=edge)
    run(u,old['soft_off06'])
    assert rd(u,P) == (edge != 4)
    assert (rd(u,N+4),rd(u,N+6)) == (140,106)
for exit_sleep in [False, True]:
    u = fixture(9)
    w(u,N+14,1)
    run(u,old['sleep_click'])
    if exit_sleep:
        run(u,0x709a,V['sleep16_wake'])
    else:
        w(u,active,0,1)
    activity(u,mouse=1)
    run(u,old['soft_off06'])
    assert not (rd(u,P) or rd(u,P+70))
print('PASS sleep: both pages, seven pad edges, redraw and first action, mouse activity, soft-off and wake')
