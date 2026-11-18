exec(open('v36/test_core.py').read().split('levels=json')[0])
old = json.loads(Path('v35c/symbols.json').read_text())

def menu(camp):
    u = machine()
    for addr in [0x2930, 0xffbe, 0xf7b2]:
        u.mem_write(addr, b'\x4e\x75')
    w(u, S['CAMP'], camp)
    return u

def down(u):
    start = old['newmenu35_down']
    # Run the native Down branch through its cursor/update and back to polling.
    u.reg_write(UC_M68K_REG_D1, rd(u, 0xffff4416))
    run(u, start, old['newmenu35_loop'])

for camp in [0, 1]:
    u = menu(camp)
    down(u)
    assert rd(u, 0xffff4416) == 1
    down(u)
    assert rd(u, 0xffff4416) == 2 and rd(u, 0xffff0270) == 0
    u.reg_write(UC_M68K_REG_D1, 2)
    run(u, old['newmenu35_accept'], 0x6dc)
    assert rd(u, S['CAMP']) == camp and rd(u, 0xffff026c) == 0

    for n in range(4):
        down(u)
        assert rd(u, 0xffff4416) == (2 if n < 3 else 3)
        assert rd(u, 0xffff026e) == (1 if n == 3 else 0)
    down(u)
    down(u)  # stays on last row, no wrap
    assert rd(u, 0xffff4416) == 4

    for sel, target, namespace, lab in [(0,0xa56,camp,0),(1,0xa2e,camp,0),(3,0xa56,0,0x100),(4,0xa56,1,0x101)]:
        w(u, S['CAMP'], camp)
        u.reg_write(UC_M68K_REG_D1, sel)
        run(u, old['newmenu35_accept'], target)
        assert (rd(u, S['CAMP']), rd(u, 0xffff026c)) == (namespace, lab)

print('PASS Back and hidden labs in both campaigns')
