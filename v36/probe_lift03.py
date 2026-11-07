from pathlib import Path
import os,sys,json
import pty_helper as pexpect
variant=sys.argv[1];camp=int(sys.argv[2]);root=Path.cwd();rom=bytearray(Path('v36/Cyber-Cop_v36_WORK_IN_PROGRESS.bin').read_bytes())
if variant=='native':rom[0x8df4:0x8dfa]=Path('v35c/Cyber-Cop_v35c.bin').read_bytes()[0x8df4:0x8dfa]
p=Path('v36/probe_lift_'+variant+str(camp)+'.bin');p.write_bytes(rom)
env=os.environ.copy();env.update(LD_PRELOAD='/usr/lib/x86_64-linux-gnu/libSDL2-2.0.so.0',SDL_VIDEODRIVER='offscreen',SDL_AUDIODRIVER='dummy')
c=pexpect.spawn(str(root/'emulator_check/blastem64-1.0.0/blastem'),['-g','-d',str(root/p)],env=env,encoding='utf8',timeout=60)
def cmd(s):c.sendline(s);c.expect('> ');return c.before
c.expect('> ')
def press(k):
 cmd('binddown "gamepads.1.'+k+'"');cmd('frames 6');cmd('bindup "gamepads.1.'+k+'"');cmd('frames 90')
cmd('frames 900');press('start');press('b');press('b');press('b');press('start')
cmd('set [$ffff0800].w '+str(camp));cmd('set [$ffff26b8].l $8c78');cmd('frames 60')
for a,v,sz in [(0xffff2190,0,'w'),(0xffff218e,26,'w'),(0xffff7dca,0xb1,'w'),(0xffff26eb,0,'b')]:cmd('set [$'+format(a,'x')+'].'+sz+' $'+format(v,'x'))
cmd('breakpoint $8e14');results=[]
for _ in range(8):
 cmd('continue');results.append(cmd('p/x [$ffff2798].w [$ffff2190].w'))
print(variant,camp,results,flush=True);c.sendline('quit');c.expect(pexpect.EOF)
