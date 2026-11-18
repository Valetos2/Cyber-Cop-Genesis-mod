"""Exercise the ROM hooks and title-theme guard with the assembled 68000."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
for original in (0x8164,0x8124):
    u=machine()
    for stub in (0x14f6,0x148e):
        u.mem_write(stub,b'\x4e\x75')
    # Replace the native loader body with a jump to its exit hook.
    u.mem_write(0x660,bytes.fromhex('4ef9000006bc'))
    w(u,0xffff0002,original)
    writes=[]
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,op,a,n,v,d:writes.append(v),
               begin=0xc00004,end=0xc00005)
    run(u,0x658,0x6c4)
    assert writes==[original&~0x40,original],writes
    assert rd(u,0xffff0002)==original
    assert u.reg_read(UC_M68K_REG_A7)==0xfffffe00

for muted,queued,playing,expected in [(0,0,0,2),(0,2,0,2),(0,0,2,0),(255,0,0,0)]:
    u=machine()
    w(u,0xffff2710,muted,1)
    w(u,0xffff7d2c,queued)
    w(u,0xffff0122,playing)
    w(u,0xffff7d30,1 if playing else 0)
    # Enter the native logo reveal and then the normal/skip title setup.
    run(u,0x5cc,0x5d2)
    assert rd(u,0xffff2702,1)==0xff
    assert rd(u,0xffff7d2c)==expected,(muted,queued,playing,rd(u,0xffff7d2c))
    if not muted:
        w(u,0xffff7d2c,0)
        w(u,0xffff0122,2)
        w(u,0xffff7d30,1)
        run(u,0xf042c,0xf0432)
        assert rd(u,0xffff7d2c)==0
print('PASS VDP blank/restore and stack, theme at logo, no restart at menu, Music Off')
