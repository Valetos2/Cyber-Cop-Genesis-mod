exec(open('v36/test_core.py').read().split('levels=json')[0])
P, N, MODE = 0xffff0200, 0xffff01a0, 0xffff26b8

for previous in (0, 1):
    for enabled, present in [(1, 255), (0, 255), (1, 0)]:
        u = machine()
        w(u, P, 1)
        w(u, N, previous)
        w(u, 0xffff0192, 255, 1)
        w(u, MODE, 0x2106, 4)
        for a in (0x2930, 0x4d18, 0x1646, 0x9342):
            u.mem_write(a, b'\x4e\x75')
        run(u, 0x6fb2)
        assert rd(u, 0xffff0868, 1) == previous+1 and rd(u, MODE, 4) == 0x7070
        w(u, N, 1) # sleep input temporarily uses the pointer
        w(u, P, enabled)
        w(u, 0xffff0192, present, 1)
        # The common exit for Start, Mode, mouse button and sleep icon.
        run(u, 0x709a, 0x2190)
        assert rd(u, MODE, 4) == 0x2106 and not rd(u, 0xffff0868, 1)
        assert rd(u, P) == enabled
        if enabled and present:
            assert rd(u, N) == previous and rd(u, P+90) == 1
        else:
            assert rd(u, N) == 1 and rd(u, P+90) == 0
print('PASS two mouse modes restored at the native sleep exit; Mouse Off and absent mouse unchanged')
