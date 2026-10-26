exec(open('v33/common.py').read())
from collections import Counter
from unicorn import UC_HOOK_CODE
u=machine();u.mem_write(0xffff0000,Path('upload/Cyber-Cop_v16.gs1').read_bytes()[0x2478:0x12478]);w(u,0xffff26b8,0x2106,4)
for a in [0x2930,0x4d18,0x35fe,0xf7b2,0x2654]:u.mem_write(a,bytes.fromhex('4e75'))
run(u,0x6fb2)
assert rd(u,0xffff202a,4)==0x561c and rd(u,0xffff270a,1)==255
assert rd(u,0xffff29ce)==200 and rd(u,0xffff29c8)==288
assert rd(u,0xffff29ca,1)==9 # menu arrow replaces crosshair shape
assert rd(u,0xffff285c)==0 and rd(u,0xffff28dc)==0
w(u,0xffff0004,255);w(u,0xffff0006,255);run(u,0x7070,0x7078)
assert set(bytes(u.mem_read(0xffff8934,0x3000)))=={0x88}
assert rd(u,0xffff28dc)==0
print('PASS native sleep fades complete to black; original menu arrow on Sleep; dots clear uses index 8')
# The automatic route and a real Mode rising edge reach identical native sleep.
def entry(auto):
 u=machine();u.mem_write(0xffff0000,Path('upload/Cyber-Cop_v23.gs3').read_bytes()[0x2478:0x12478]);w(u,0xffff26b8,0x2106,4);w(u,0xffff2a2a,16);w(u,0xffff012c,255,1);w(u,0xffff0010,8);w(u,0xffff0012,0)
 for a in [0x2930,0x4d18,0x35fe,0xf7b2,0x2654]:u.mem_write(a,bytes.fromhex('4e75'))
 if auto=='pad':
  w(u,0xffff0154,255,1);w(u,0xffff270f,0,1);run(u,L['pad28_sleep'])
 else:run(u,L['autosleep24'] if auto else L['mode_action'])
 return u
x,y=entry(True),entry(False)
for a,n in [(0x202a,4),(0x20e0,6),(0x26b8,4),(0x26e2,1),(0x270a,5),(0x282c,256),(0x29c8,8),(0x2a2a,2)]:assert x.mem_read(0xffff0000+a,n)==y.mem_read(0xffff0000+a,n),(hex(a))
print('Auto Sleep and actual Mode edge: identical native sleep state/palette/cursor/energy')

z=entry('pad')
for a,n in [(0x202a,4),(0x20e0,6),(0x26b8,4),(0x26e2,1),(0x270a,5),(0x282c,256),(0x29c8,8),(0x2a2a,2)]:assert z.mem_read(0xffff0000+a,n)==y.mem_read(0xffff0000+a,n),hex(a)
print('Disconnected-pad route reaches identical native sleep as Mode, including palette/cursor/energy')
