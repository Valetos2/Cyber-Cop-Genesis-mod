exec(open('v34/common.py').read())
# Movement vector rotates, camera and scalar speed do not receive a diagonal bonus.
for directions,angle in [(4,768),(8,256),(5,896),(9,128),(6,640),(10,384)]:
 u=machine();w(u,0xffff0004,255^(64|directions));w(u,0xffff260c,0);w(u,0xffff441c,110);w(u,0xffff4440,110);w(u,0xffff443c,0);w(u,0xffff243c,0x6000);w(u,0xffff26fc,0,1);w(u,0xffff26e4,0,1);w(u,0xffff26e5,0,1)
 run(u,0xa0ea);assert rd(u,0xffff443a)==angle,(directions,rd(u,0xffff443a));assert rd(u,0xffff260c)==0;assert rd(u,0xffff013e,1)==255
# Jump only on A release; used strafe gesture cancels it.
for used in [0,255]:
 u=machine();w(u,0xffff441c,110);w(u,0xffff4440,110);w(u,0xffff26e8,0,1);w(u,0xffff013e,used,1);w(u,0xffff0004,0xbe);w(u,0xffff0006,0xfe);run(u,0xabe0);assert rd(u,0xffff26e8,1)==0
 w(u,0xffff0004,0xfe);w(u,0xffff0006,0xbe);run(u,0xabe0);assert rd(u,0xffff26e8,1)==(0 if used else 255)
# Short action press and release while main loop is blocked survives until consume.
u=machine();w(u,0xffff014e,0xa6,1);w(u,0xffff0014,0);w(u,0xffff270a,0,1);w(u,0xffff0004,255);w(u,0xffff0140,255);w(u,0xffff0144,0);samples=iter([(255,239,0,2),(239,255,2,0)])
def raw(u,pc,s,d):
 if pc==L['raw26']:
  prev,cur,ep,ec=next(samples);w(u,0xffff0142,prev);w(u,0xffff0140,cur);w(u,0xffff0146,ep);w(u,0xffff0144,ec);u.reg_write(UC_M68K_REG_D0,cur);ret(u)
u.hook_add(UC_HOOK_CODE,raw)
run(u,L['buffer26_sample'],0x1755e);run(u,L['buffer26_sample'],0x1755e);run(u,L['buffer26_consume']);assert rd(u,0xffff0004)==239 and rd(u,0xffff0006)&16 and rd(u,0xffff0010)==2 and rd(u,0xffff0012)==0
run(u,L['buffer26_consume']);assert rd(u,0xffff0004)==255 and rd(u,0xffff0010)==0 and rd(u,0xffff0148)==0
print('PASS six strafe vectors, A-release jump/cancellation, buffered B/Y tap consumed once')
# Never queue walking or gesture A in player mode; external panels permit A.
for menu,cursor,sleep,expected in [(0,0x561c,0x2106,0xb0),(255,0x561c,0x2106,0xbf),(255,0xffff6000,0x2106,0xff),(255,0x561c,0x7070,0xff)]:
 u=machine();w(u,0xffff270a,menu,1);w(u,0xffff202a,cursor,4);w(u,0xffff26b8,sleep,4)
 if cursor==0xffff6000:w(u,cursor+2,10)
 run(u,L['buffer26_mask']);assert u.reg_read(UC_M68K_REG_D1)&255==expected
# Jetpack and levitation permit side travel above normal standing height.
for hover in [None,0xffff26e4,0xffff26e5]:
 u=machine();w(u,0xffff0004,0xbb);w(u,0xffff260c,0);w(u,0xffff441c,140);w(u,0xffff4440,110);w(u,0xffff26e4,0,1);w(u,0xffff26e5,0,1)
 if hover:w(u,hover,255,1);run(u,0xa0ea);assert rd(u,0xffff443a)==768
 else:run(u,0xa0ea,0xa0f0)
print('PASS per-context buffer mask; airborne strafe blocked during normal jump, allowed for both hover flags')
