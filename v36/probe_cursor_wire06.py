from pathlib import Path
import os,json
import pty_helper as pexpect
root=Path.cwd();env=os.environ.copy();env.update(LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libSDL2-2.0.so.0',SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy')
c=pexpect.spawn(str(root/'emulator_check/blastem64-1.0.0/blastem'),['-g','-d','-s',str(root/'upload/Cyber-Cop_v36_test05.gs0'),str(root/'v36/release_test05/Cyber-Cop_v36_test05.bin')],env=env,encoding='utf8',timeout=30);log=Path('v36/probe_cursor_wire06.log').open('w');c.logfile=log;c.expect('> ')
def cmd(s):c.sendline(s);c.expect('> ');return c.before
cmd('frames 10')
for i in range(80):
 cmd(('binddown' if i%2 else 'bindup')+' "mouse.1.left"');cmd('frames 4');state=cmd('p/x [$ffff01a6].w [$ffff29c8].w [$ffff0188].l [$ffff0192].w');print(i,state.strip(),flush=True)
c.sendline('quit');c.expect(pexpect.EOF);log.close()
