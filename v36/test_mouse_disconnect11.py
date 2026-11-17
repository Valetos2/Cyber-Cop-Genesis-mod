exec(open('v36/test_core.py').read().split('levels=json')[0])
old = json.loads(Path('v35c/symbols.json').read_text())
M, P = 0xffff0180, 0xffff0200
end = 0x1802f4

def miss(u):
    run(u, old['poll03_bad'], end)

def good(u, buttons):
    # Valid packet: D2 is the decoded button state at the start of edge detection.
    u.reg_write(UC_M68K_REG_D2, buttons)
    run(u, 0x1802ae, end)

for enabled in [0, 1]:
    u = machine()
    good(u, 1)
    run(u, old['detect04'])
    w(u, P, enabled)
    w(u, M+4, 8, 4)
    w(u, M+8, -2, 4)
    miss(u)
    assert rd(u, M+12) == 1 and rd(u, M+4, 4) == 8
    for n in range(2, 30):
        miss(u)
        run(u, old['detect04'])
        assert rd(u, P+36) == n and rd(u, M+18, 1) == 255
        assert rd(u, P) == enabled and rd(u, P+38) == 1
        assert rd(u, M+12) == rd(u, M+16) == rd(u, M+4, 4) == rd(u, M+8, 4) == 0
    good(u, 1)
    run(u, old['detect04'])
    assert rd(u, P) == enabled and rd(u, P+36) == 0
    assert rd(u, M+16) == 0 and rd(u, M+12) == 1
    good(u, 0)
    assert rd(u, M+12) == 0
    good(u, 1)
    assert rd(u, M+16) == 1

    for _ in range(31):
        miss(u)
    assert rd(u, P+36) == 30 and rd(u, M+18, 1) == 0
    w(u, 0xffff270a, 0, 1)
    run(u, old['detect04'])
    assert rd(u, P) == rd(u, P+38) == 0
    good(u, 0)
    run(u, old['detect04'])
    assert rd(u, P) == enabled and rd(u, P+38) == 1

u = machine()
for _ in range(31):
    miss(u)
assert rd(u, M+18, 1) == 0
good(u, 0)
good(u, 0)
good(u, 1)
assert rd(u, M+16) == 1
print('PASS mouse polling: transient misses, clean click recovery, disconnect and reconnect')
