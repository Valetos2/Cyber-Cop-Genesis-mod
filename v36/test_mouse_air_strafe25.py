"""Exercise the native airborne strafe branch."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
P=0xffff0200
INPUT=0xffff0004
for mouse,present,air,end in [(1,255,True,0xf8f3e),(0,255,True,0xf8fc2),(1,0,True,0xf8fc2),
                              (1,255,False,0xf8f3e),(0,255,False,0xf8f3e)]:
    u=machine()
    w(u,P,mouse);w(u,0xffff0192,present,1);w(u,INPUT,0xbb)
    w(u,0xffff441c,120 if air else 80);w(u,0xffff4440,100)
    for addr in (0xffff26e4,0xffff26e5):w(u,addr,0,1)
    run(u,0xf8eec,end)
print('PASS left+A uses real strafe path in air only with a present, enabled mouse; pad motion unchanged')
