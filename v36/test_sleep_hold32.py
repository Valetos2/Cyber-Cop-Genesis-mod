"""Compare the actual entry and exit mouse-icon transitions per VBlank."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
previous=Path(sys.argv[1]).read_bytes()
s=json.loads(Path('v35c/symbols.json').read_text())
P,N=0xffff0200,0xffff01a0
VIEW=0xffff26b8

def sleep_click(rom,restore_mode,wake):
    u=machine(rom)
    # Simulate one VBlank at every native frame wait. The actual click,
    # feedback and HUD branches run; only DMA/graphics setup is stubbed.
    u.mem_write(0x2930,bytes.fromhex('4eb9')+s['hud_draw'].to_bytes(4,'big')+b'\x4e\x75')
    for a in (0x1646,0xffbe,0x249c,0x4d18,0xdf6e,0x9342,0x5122,0x184214,0x184320):
        u.mem_write(a,b'\x4e\x75')
    for a,value in [(P,1),(P+6,0x5348),(P+116,1),(N,1),(N+4,80),(N+6,160),(N+12,1),(N+14,1)]:
        w(u,a,value)
    w(u,N+16,0x561c,4)
    w(u,0xffff0192,255,1)
    w(u,VIEW,0x7070 if wake else 0x2106,4);w(u,0xffff20e0,0x2106,4)
    w(u,0xffff0868,restore_mode+1,1)
    calls=[]; frames=[]
    u.hook_add(UC_HOOK_CODE,lambda *_:frames.append(1),begin=0x2930,end=0x2930)
    for event in ('hud_names','hud_restore'):
        a=s[event]
        u.hook_add(UC_HOOK_CODE,lambda uc,pc,sz,name:calls.append((name,len(frames))),event,begin=a,end=a)
    if wake:
        run(u,s['press03'],0x2190)
        assert rd(u,VIEW,4)==0x2106 and rd(u,N)==restore_mode
        assert rd(u,P+90)==1 and rd(u,P)==1
    else:
        run(u,s['press_ui'])
        assert rd(u,VIEW,4)==0x7070
    return calls,rd(u,P+24)

for m in (0,1):
    old,slot=sleep_click(previous,m,True)
    assert old==[('hud_names',1),('hud_restore',2)] and not slot,(old,slot)
    for wake in (False,True):
        new,slot=sleep_click(R,m,wake)
        assert new==[('hud_names',i) for i in range(1,7)]+[('hud_restore',7)] and not slot,(wake,new,slot)
print('PASS: mouse entry and wake each hold exactly six VBlanks, restore on frame seven, and keep both mouse modes')
