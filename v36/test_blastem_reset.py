from pathlib import Path
import os,json
import pty_helper as pexpect
root=Path.cwd();log=Path('v36/BlastEm_reset_session.log').open('w');env=os.environ.copy();env.update(LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libSDL2-2.0.so.0',SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy')
c=pexpect.spawn(str(root/'emulator_check/blastem64-1.0.0/blastem'),['-g','-d',str(root/'v36/Cyber-Cop_v36_WORK_IN_PROGRESS.bin')],env=env,encoding='utf8',timeout=90);c.logfile=log;c.expect('> ')
def cmd(s):
 c.sendline(s);c.expect('> ');return c.before
print(cmd('frames 900'),flush=True)
cmd('binddown "gamepads.1.start"');cmd('frames 6');cmd('bindup "gamepads.1.start"');print(cmd('frames 120'),flush=True)
print(cmd('bt'),flush=True);print(cmd('p/x [$ffff0192].b'),flush=True)
cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');cmd('frames 2')
def press(key,frames=8):
 cmd('binddown "gamepads.1.'+key+'"');cmd('frames '+str(frames));cmd('bindup "gamepads.1.'+key+'"');return cmd('frames 100')
print('SELECT MISSION',press('down'),flush=True)
print('NEW GAME',press('b'),flush=True)
print('DEFAULT',press('b'),flush=True)
print('STATE',cmd('bt'),flush=True)
cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');cmd('frames 2')
print('CONFIRM AGENT',press('b'),flush=True)
print('START',press('start'),flush=True)
cmd('binddown "ui.screenshot"');cmd('bindup "ui.screenshot"');print(cmd('frames 10'),flush=True)
print(cmd('bt'),flush=True);state=cmd('p/x [$ffff0274].w [$ffff026c].w [$ffff26b8].l [$ffff0800].w');print(state,flush=True);assert '[$ffff0274].w: 1' in state and '[$ffff26b8].l: 2106' in state and '[$ffff0800].w: 1' in state

# Soft reset must discard all new volatile state, including cursor/PCM flags.
cmd('set [$ffff0804].b $ff');cmd('set [$ffff0828].w 5');cmd('set [$ffff0104].w $7777')
cmd('breakpoint $332');cmd('softreset');cmd('delete 0');print(cmd('frames 900'),flush=True)
state=cmd('p/x [$ffff0800].w [$ffff0802].w [$ffff0804].b [$ffff0828].w');print('RESET',state,flush=True)
for expected in ['[$ffff0800].w: 0','[$ffff0802].w: 0','[$ffff0804].b: 0','[$ffff0828].w: 0']:assert expected in state
c.sendline('quit');c.expect(pexpect.EOF);log.close()
