from pathlib import Path
import os,json,struct
import pty_helper as pexpect
root=Path.cwd();S=json.loads(Path('v36/symbols.json').read_text());log=Path('v36/BlastEm_audio_session.log').open('w');env=os.environ.copy();env.update(LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libSDL2-2.0.so.0',SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy')
c=pexpect.spawn(str(root/'emulator_check/blastem64-1.0.0/blastem'),['-g','-d',str(root/'v36/Cyber-Cop_v36_WORK_IN_PROGRESS.bin')],env=env,encoding='utf8',timeout=60);c.logfile=log;c.expect('> ')
def cmd(s):c.sendline(s);c.expect('> ');return c.before
def press(k):
 cmd('binddown "gamepads.1.'+k+'"');cmd('frames 6');cmd('bindup "gamepads.1.'+k+'"');return cmd('frames 90')
call_id=0
def call_main(symbol):
 global call_id
 addr=0xffff0900+call_id*32;call_id+=1
 code=bytes.fromhex('4eb9')+struct.pack('>I',S[symbol])+bytes.fromhex('23fc00002106ffff26b84e75')
 for i in range(0,len(code),2):cmd('set [$'+hex(addr)[2:]+'+'+str(i)+'].w $'+code[i:i+2].hex())
 cmd('set [$ffff26b8].l $'+hex(addr)[2:])
cmd('frames 900');press('start');press('b');press('b');press('b');press('start');state=cmd('p/x [$ffff26b8].l');print(state,flush=True);assert '2106' in state;cmd('binddown "ui.vgm_log"');cmd('bindup "ui.vgm_log"');cmd('frames 2')
call_main('robot_attack_sound36');print(cmd('frames 30'),flush=True);print(cmd('p/x [$ffff0804].b'),flush=True);call_main('robot_stop_sound36');print(cmd('frames 15'),flush=True);print(cmd('p/x [$ffff0804].b'),flush=True);call_main('robot_step_sound36');print(cmd('frames 20'),flush=True);cmd('binddown "ui.vgm_log"');cmd('bindup "ui.vgm_log"');print(cmd('frames 2'),flush=True)
c.sendline('quit');c.expect(pexpect.EOF);log.close()
