from pathlib import Path
import os,json
import pty_helper as pexpect
root=Path.cwd();log=Path('v36/BlastEm_mouse_session.log').open('w');env=os.environ.copy();env.update(LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libSDL2-2.0.so.0',SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy')
c=pexpect.spawn(str(root/'emulator_check/blastem64-1.0.0/blastem'),['-g','-d',str(root/'v36/Cyber-Cop_v36_WORK_IN_PROGRESS.bin')],env=env,encoding='utf8',timeout=60);c.logfile=log;c.expect('> ')
def cmd(s):c.sendline(s);c.expect('> ');return c.before
def press(k):
 cmd('binddown "gamepads.1.'+k+'"');cmd('frames 6');cmd('bindup "gamepads.1.'+k+'"');return cmd('frames 90')

S=json.loads(Path('v36/symbols.json').read_text())
cmd('frames 900');press('start');press('b');press('down');press('b')
cmd('breakpoint $'+hex(S['front_mouse36'])[2:]);cmd('continue')
def click(x,y,edge):
 cmd('set [$ffff0190].w 0');cmd('set [$ffff018c].w 0');cmd('continue')
 for a,v in [(0xffff0200,1),(0xffff0192,0x0100),(0xffff01a4,x),(0xffff01a6,y),(0xffff0190,edge),(0xffff018c,edge)]:cmd('set [$'+hex(a)[2:]+'].w $'+hex(v)[2:])
 return cmd('continue')
old=cmd('p/x [$ffff2a38].w');print('CHAR BEFORE',old,flush=True)
click(176,92,1);print('PASS CHARACTER',cmd('p/x [$ffff2a38].w'),flush=True)
click(140,92,1);print('ACCEPT',cmd('p/x [$ffff0802].w'),flush=True)
assert '[$ffff0802].w: 2' in cmd('p/x [$ffff0802].w')
print('GEAR BEFORE',cmd('p/x [$ffff4412].w'),flush=True)
click(140,92,1);print('GEAR NEXT',cmd('p/x [$ffff4412].w'),flush=True)
click(140,92,2);state=cmd('p/x [$ffff4412].w');print('GEAR RIGHT IGNORED',state,flush=True);assert '[$ffff4412].w: 1' in state
cmd('delete 0');cmd('breakpoint $2106')
for a,v in [(0xffff0200,1),(0xffff0192,0x0100),(0xffff0190,8),(0xffff018c,8)]:cmd('set [$'+hex(a)[2:]+'].w $'+hex(v)[2:])
print('FOURTH START',cmd('continue'),flush=True);print(cmd('p/x [$ffff0802].w [$ffff26b8].l'),flush=True)
c.sendline('quit');c.expect(pexpect.EOF);log.close()
