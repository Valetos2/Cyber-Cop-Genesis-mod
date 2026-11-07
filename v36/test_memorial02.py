exec(open('v36/test_blastem_front.py').read().split("cmd('frames 900')")[0])
s=json.loads(Path('v36/symbols.json').read_text());cmd('breakpoint $'+format(s['memorial_wait36b'],'x'));cmd('continue');cmd('delete 0');cmd('breakpoint $39c');cmd('binddown "gamepads.1.b"');result=cmd('continue');assert '39C:' in result,result;cmd('bindup "gamepads.1.b"');cmd('delete 1');print('PASS memorial skip returns to intact SEGA entry',flush=True)
cmd('frames 900');press('start');print(cmd('p/x [$ffff0850].w'),flush=True);cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');print(cmd('frames 2'),flush=True)
c.sendline('quit');c.expect(pexpect.EOF);log.close()
