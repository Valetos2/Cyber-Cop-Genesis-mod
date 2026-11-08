from pathlib import Path
import os,json
import pty_helper as pexpect
root=Path.cwd();env=os.environ.copy();env.update(LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libSDL2-2.0.so.0',SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy')
c=pexpect.spawn(str(root/'emulator_check/blastem64-1.0.0/blastem'),['-g','-d','-s',str(root/'upload/Cyber-Cop_v36_test05.gs0'),str(root/'v36/release_test05/Cyber-Cop_v36_test05.bin')],env=env,encoding='utf8',timeout=30);log=Path('v36/probe_cursor06.log').open('w');c.logfile=log;c.expect('> ')
def cmd(s):c.sendline(s);c.expect('> ');return c.before
s=json.loads(Path('v35c/symbols.json').read_text());cmd('set [$18013c].w $4e75');cmd('breakpoint $'+format(s['consume'],'x'));cmd('continue')
for i in range(60):
 for a,v,size in [(0xffff0184,0,'l'),(0xffff0188,0,'l'),(0xffff018c,i%2,'w'),(0xffff0190,i%2,'w'),(0xffff0192,0xff00,'w')]:cmd('set [$'+format(a,'x')+'].'+size+' $'+format(v,'x'))
 cmd('continue');state=cmd('p/x [$ffff01a6].w [$ffff29c8].w [$ffff0234].l');print(i,state.strip(),flush=True)
c.sendline('quit');c.expect(pexpect.EOF);log.close()
