exec(open('v36/test_blastem_front.py').read().split("cmd('frames 900')")[0])
cmd('frames 900');press('start');cmd('frames 120');cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');print(cmd('frames 2'),flush=True)
print(cmd('bt'),flush=True);c.sendline('quit');c.expect(pexpect.EOF);log.close()
