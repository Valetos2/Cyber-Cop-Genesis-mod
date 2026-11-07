from pathlib import Path
import os,json
import pty_helper as pexpect
root=Path.cwd();log=Path('v36/BlastEm_gear_session.log').open('w');env=os.environ.copy();env.update(LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libSDL2-2.0.so.0',SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy')
c=pexpect.spawn(str(root/'emulator_check/blastem64-1.0.0/blastem'),['-g','-d',str(root/'v36/Cyber-Cop_v36_WORK_IN_PROGRESS.bin')],env=env,encoding='utf8',timeout=60);c.logfile=log;c.expect('> ')
def cmd(s):c.sendline(s);c.expect('> ');return c.before
def press(k):
 cmd('binddown "gamepads.1.'+k+'"');cmd('frames 6');cmd('bindup "gamepads.1.'+k+'"');return cmd('frames 90')
cmd('frames 900');press('start');press('b');press('down');press('b');press('left');press('b');cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');print(cmd('frames 2'),flush=True);print(cmd('bt'),flush=True);print(cmd('p/x [$ffff29c8].w [$ffff29ce].w'),flush=True)
c.sendline('quit');c.expect(pexpect.EOF);log.close()
