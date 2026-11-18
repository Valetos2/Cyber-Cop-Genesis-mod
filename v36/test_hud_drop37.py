"""Model the visible HUD at the end of each VBlank from stock tile writes."""
exec(open('v36/test_scanman20.py').read().split('if len(sys.argv)==3:')[0])
s=json.loads(Path('v35c/symbols.json').read_text())
old=Path(sys.argv[1]).read_bytes()
gst=Path(sys.argv[2]).read_bytes()
P,N=0xffff0200,0xffff01a0
A=0xea36
def names_at(u,vram):
    def store(uc,*_):
        dst=uc.reg_read(UC_M68K_REG_D2)&65535
        val=uc.reg_read(UC_M68K_REG_D0)&65535
        vram[dst:dst+2]=val.to_bytes(2,'big')
    a=s['vdp_name']
    u.hook_add(UC_HOOK_CODE,store,begin=a,end=a)
    for row in range(2):
        a=S['hud_publish_row37_'+str(row)]
        def bulk(uc,pc,size,row):
            left=uc.reg_read(UC_M68K_REG_D7)&65535
            ptr=uc.reg_read(UC_M68K_REG_A0)
            start=0xe992+row*128+(23-left)*2
            vram[start:start+2]=uc.mem_read(ptr,2)
        u.hook_add(UC_HOOK_CODE,bulk,row,begin=a,end=a)
    return store
for rom,expected in [(old,0x0691),(R,0x0148)]:
    u=machine(rom)
    u.mem_write(0xffff0000,gst[0x2478:0x12478])
    vram=bytearray(gst[0x12478:0x22478]);before=bytes(vram)
    assert int.from_bytes(vram[A:A+2],'big')==0x0691
    names_at(u,vram)
    run(u,s['hud_draw'])
    assert int.from_bytes(vram[A:A+2],'big')==expected
    assert sum(a!=b for a,b in zip(vram,before))==(2 if rom==R else 0)
print('PASS gs0: only corrupted Use name corrected on the next VBlank')

def click(rom,panel):
    if panel==0x87c8:
        u=opened(rom,1,0x72ac,1)
    else:
        u=machine(rom)
        w(u,view,panel,4);w(u,0xffff21ba,0x14 if panel==0x8476 else 0x1b)
        w(u,0xffff2740,11);w(u,0xffff2f5b,rd(u,0xffff21ba),1)
    for a in (0x51bc,0x9342,0xdf6e,0x4d18,0x5122,0x150d8,0x1646,0x249c):
        u.mem_write(a,b'\x4e\x75')
    u.mem_write(0x96ba,bytes.fromhex('45f9ffff334170004e75')) # valid empty target
    for a,v in [(P,1),(P+6,0x5348),(P+116,1),(N,1),(N+4,248),(N+6,157),
                (N+12,1),(N+14,1),(0xffff0004,0xff),
                (P+84,int(panel!=0x2106)),(P+86,1)]:
        w(u,a,v)
    w(u,N+16,0x56bc,4);w(u,0xffff26e0,255,1)
    w(u,0xffff26e2,255 if panel!=0x2106 else 0,1)
    w(u,0xffff441c,0);w(u,0xffff4440,0x200)
    w(u,0xffff0192,255,1)
    u.mem_write(0x2930,bytes.fromhex('48e7fffe4eb9')+s['hud_draw'].to_bytes(4,'big')+bytes.fromhex('4cdf7fff4e75'))
    vram=bytearray(65536);store=names_at(u,vram)
    if rom==old:
        # Sample the old close routine as it submits the base Drop tile.
        a=S['terminal_hud36b']+10+16*21+10
        u.hook_add(UC_HOOK_CODE,store,begin=a,end=a)
    count=[]
    u.hook_add(UC_HOOK_CODE,lambda *_:count.append(1),begin=0x6cb2,end=0x6cb2)
    ran=[]
    value=lambda: int.from_bytes(vram[0xe9bc:0xe9be],'big')==0x0690
    run(u,s['press_ui']);ran.append(value())
    run(u,s['hud_draw']);ran.append(value())
    for held in (True,True,False):
        w(u,0xffff018c,int(held))
        w(u,0xffff0004,0xff)
        run(u,s['consume'])
        run(u,s['visual_update'])
        run(u,s['hud_draw']);ran.append(value())
    assert len(count)==1 and rd(u,view,4)==0x2106
    return ran

assert click(old,0x87c8)==[False,True,False,False,False]
for panel in (0x2106,0x87c8,0x8476):
    assert click(R,panel)==[True,True,True,True,False],hex(panel)
print('PASS drop: world, Scanman and Medi Kit stay pressed continuously until physical release; one drop')
