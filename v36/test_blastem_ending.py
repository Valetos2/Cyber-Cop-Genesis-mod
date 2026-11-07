from pathlib import Path
import os,json
import pty_helper as pexpect
root=Path.cwd();log=Path('v36/BlastEm_ending_session.log').open('w');env=os.environ.copy();env.update(LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libSDL2-2.0.so.0',SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy')
c=pexpect.spawn(str(root/'emulator_check/blastem64-1.0.0/blastem'),['-g','-d',str(root/'v36/Cyber-Cop_v36_WORK_IN_PROGRESS.bin')],env=env,encoding='utf8',timeout=60);c.logfile=log;c.expect('> ')
def cmd(s):c.sendline(s);c.expect('> ');return c.before
def press(k):
 cmd('binddown "gamepads.1.'+k+'"');cmd('frames 6');cmd('bindup "gamepads.1.'+k+'"');return cmd('frames 90')
cmd('frames 900');press('start');press('down');press('b');press('b');cmd('breakpoint $2106');print(cmd('frames 60'),flush=True);cmd('delete 0');cmd('set [$ffff26b8].l $2eb0');print(cmd('frames 350'),flush=True);cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');print(cmd('frames 2'),flush=True);print(cmd('p/x [$ffff0800].w'),flush=True)
c.sendline('quit');c.expect(pexpect.EOF);log.close()
