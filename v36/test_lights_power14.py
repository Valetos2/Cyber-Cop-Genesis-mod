exec(open('v36/test_core.py').read().split('levels=json')[0])

def circle(u):
    base = 0xffff533c
    for i, x in enumerate((7, 96, 64, 4, 14)):
        w(u, base+i*2, x)
    w(u, 0xffff5338, base+10, 4)

def render(u):
    u.mem_write(0xffff8934, bytes(12288))
    run(u, 0x4584, 0x458a)
    return any(u.mem_read(0xffff8934, 12288))

for camp in (0, 1):
    u = machine()
    w(u, S['CAMP'], camp)
    w(u, 0xffff2606, 15)
    run(u, 0x7ad6)
    run(u, 0x7afa)
    circle(u)
    assert render(u)
    u.reg_write(UC_M68K_REG_D0, 0)
    run(u, 0x7a92)
    assert render(u) # a different floor's fuse is irrelevant
    u.reg_write(UC_M68K_REG_D0, 13)
    run(u, 0x7a92)
    assert not render(u)
    for opt in (255, 0):
        w(u, 0xffff0856, opt, 1)
        assert not render(u)
    u.reg_write(UC_M68K_REG_D0, 13)
    run(u, 0x7a92)
    assert render(u) and rd(u, 0xffff0856, 1) == 0
print('PASS actual fuse toggles suppress and restore live lamp pixels in both campaigns')
