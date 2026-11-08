exec(open('v36/test_blastem_front.py').read().split("cmd('frames 900')")[0])
s=json.loads(Path('v36/symbols.json').read_text());cmd('breakpoint $'+format(s['memorial_wait36b'],'x'));cmd('continue');cmd('delete 0');cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');print('first',cmd('frames 2'),flush=True)
cmd('frames 900');press('start');cmd('breakpoint $'+format(s['memorial_wait36b'],'x'));print(cmd('continue'),flush=True);cmd('delete 1');cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');print('repeat',cmd('frames 2'),flush=True)
c.sendline('quit');c.expect(pexpect.EOF);log.close()
