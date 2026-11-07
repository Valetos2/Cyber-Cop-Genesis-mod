exec(open('v36/test_blastem_front.py').read().split("cmd('frames 900')")[0])
cmd('frames 900');press('start');press('b');press('down')
for _ in range(4):press('down')
press('down');print('SUBMENU',cmd('p/x [$ffff011e].w [$ffff026e].w'),flush=True)
press('start');cmd('frames 150');state=cmd('p/x [$ffff026c].w [$ffff0800].w [$ffff26b8].l');print('LAB02',state,flush=True)
assert '[$ffff026c].w: 101' in state and '[$ffff0800].w: 1' in state and '[$ffff26b8].l: 2106' in state
cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');print(cmd('frames 2'),flush=True)
c.sendline('quit');c.expect(pexpect.EOF);log.close()
