exec(open('v36/test_core.py').read().split('levels=json')[0])

def setup():
    u = machine()
    u.mem_write(0x4d18, b'\x4e\x75')
    w(u, 0xffff26b8, 0x77a8, 4)
    w(u, 0xffff2282, S['airlock_shaded_bank36e'], 4)
    w(u, 0xffff227e, 0xffff7dc6, 4)
    u.mem_write(0xffff7dc6, bytes(192))
    u.mem_write(0xffff8934, bytes(12288))
    return u

def frame(u, lens, dirty=255):
    w(u, 0xffff7dce, lens)
    w(u, 0xffff2700, dirty, 1)
    run(u, S['airlock_alarm_draw14'])
    assert rd(u, 0xffff7dce) == lens
    return bytes(u.mem_read(0xffff8934, 12288))

u = setup()
off = frame(u, 0xb3)
red = frame(u, 0xb2)
assert red != off
u = setup()
assert frame(u, 0xb3) == off
w(u, 0xffff29ba, 1)
assert frame(u, 0xb3, dirty=0) == red # transition requests redraw
w(u, 0xffff026c, 0x100)
w(u, 0xffff26ec, 255, 1) # a valid code entered before the alarm
w(u, 0xffff7e3a, 0)
run(u, 0x784c)
assert rd(u, 0xffff7e3a) == 0
w(u, 0xffff29ba, 0)
assert frame(u, 0xb3, dirty=0) == off
assert rd(u, 0xffff26ec, 1) == 255
run(u, 0x784c)
assert rd(u, 0xffff7e3a) == 0xc0
print('PASS airlock reuses the red lens on entry, redraws on alarm change, and blocks an already-authorized open')
