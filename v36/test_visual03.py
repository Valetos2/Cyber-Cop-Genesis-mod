exec(open('v36/test_blastem_front.py').read().split("cmd('frames 900')")[0])
import re
s=json.loads(Path('v36/symbols.json').read_text())
def shot(label):
 cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');print(label,cmd('frames 2'),flush=True)
cmd('breakpoint $'+format(s['memorial_wait36b'],'x'));cmd('continue');cmd('delete 0');shot('memorial');cmd('frames 900');press('start')
count=int(re.search(r': ([0-9a-f]+)',cmd('p/x [$ffff0850].w'))[1],16)
ids=[int(re.search(r': ([0-9a-f]+)',cmd('p/x [$'+format(0xffff0840+i*2,'x')+'].w'))[1],16) for i in range(count)]
for _ in range(ids.index(5)):press('down')
press('b');shot('options lamps on')
for _ in range(5):press('down')
press('b');print(cmd('p/x [$ffff0856].b'),flush=True);shot('options lamps off');press('b');press('start')
for _ in range(ids.index(5)):press('up')
press('b');press('b');press('b');press('start');print('game',cmd('p/x [$ffff26b8].l'),flush=True)
press('mode');cmd('set [$ffff0118].b 1');cmd('set [$ffff0119].b $b');cmd('set [$ffff0204].w 1');cmd('frames 6');shot('sleep lamps')
c.sendline('quit');c.expect(pexpect.EOF);log.close()
