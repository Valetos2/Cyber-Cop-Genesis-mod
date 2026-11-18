"""Follow a mouse click on the sleep icon through the two real HUD uploads."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
previous=Path(sys.argv[1]).read_bytes()
s=json.loads(Path('v35c/symbols.json').read_text())
P,N=0xffff0200,0xffff01a0
VIEW=0xffff26b8

def mouse_wake(rom,restore_mode):
    u=machine(rom)
    # Simulate one VBlank at every native frame wait. The actual click,
    # feedback and HUD branches run; only DMA/graphics setup is stubbed.
    u.mem_write(0x2930,bytes.fromhex('4eb9')+s['hud_draw'].to_bytes(4,'big')+b'\x4e\x75')
    for a in (0x4d18,0xdf6e,0x9342,0x5122,0x184214,0x184320):
        u.mem_write(a,b'\x4e\x75')
    for a,value in [(P,1),(P+6,0x5348),(P+116,1),(N,1),(N+4,80),(N+6,160),(N+12,1),(N+14,1)]:
        w(u,a,value)
    w(u,N+16,0x561c,4)
    w(u,0xffff0192,255,1)
    w(u,VIEW,0x7070,4);w(u,0xffff20e0,0x2106,4)
    w(u,0xffff0868,restore_mode+1,1)
    calls=[]
    for event in ('hud_names','hud_restore'):
        a=s[event]
        u.hook_add(UC_HOOK_CODE,lambda uc,pc,sz,name:calls.append(name),event,begin=a,end=a)
    run(u,s['press03'],0x2190)
    assert rd(u,VIEW,4)==0x2106 and rd(u,N)==restore_mode
    assert rd(u,P+90)==1 and rd(u,P)==1
    return calls,rd(u,N+20,4),rd(u,P+24)

for m in (0,1):
    old,owner,slot=mouse_wake(previous,m)
    assert old==['hud_names','hud_names'] and owner and slot,(old,owner,slot)
    new,owner,slot=mouse_wake(R,m)
    assert new==['hud_names','hud_restore'] and not owner and not slot,(new,owner,slot)
print('PASS mouse wake: one pressed upload, then normal icon; free look and pointer both restored')
