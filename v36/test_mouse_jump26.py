"""Exercise mouse jump dispatch."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
P=0xffff0200
INPUT=0xffff0004
JUMP=0xffff26e8
SINK=0x1833f2
def capture(u,button,edge,pad,view=0x2106):
    w(u,INPUT,pad);w(u,0xffff26b8,view,4)
    u.reg_write(UC_M68K_REG_D4,button);u.reg_write(UC_M68K_REG_D5,edge)
    u.reg_write(UC_M68K_REG_D1,64 if button else 0)
    run(u,0x1833da,SINK)
    return rd(u,0xffff0196)
u=machine()
for a in (0xffff270a,0xffff270e,JUMP):w(u,a,0,1)
assert capture(u,1,1,0xfe)==0 and rd(u,JUMP,1)==255
w(u,JUMP,0,1) # land while mouse remains held
assert capture(u,1,0,0xfe)==0 and rd(u,JUMP,1)==0
assert capture(u,0,0,0xfe)==0 and rd(u,JUMP,1)==0
assert capture(u,1,1,0xff)==64 and rd(u,JUMP,1)==0
assert capture(u,1,0,0xfe)==64 and rd(u,JUMP,1)==0 # no new mouse press
capture(u,0,0,0xfe)
assert capture(u,1,1,0xfe,0x87c8)==64 and rd(u,JUMP,1)==0
w(u,JUMP,255,1)
assert capture(u,1,1,0xfe)==0 # a second click in the same jump does not arm A
print('PASS forward+LMB jumps on press only; other gestures retain old mapping')
