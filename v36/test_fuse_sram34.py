"""Migrate a real test20-format checkpoint without resetting campaign progress."""
exec(open('v36/test_sram_audio33.py').read().split('for flags in range(4):')[0])
def data(u):
    return [bytes(u.mem_read(a,n)) for a,n in ((0xffff2150,28),(0xffff086c,2),(0xffff0134,3))]
sram=bytes([255])*0x4000
for campaign in (0,1):
    sram=checkpoint(fresh(PRIOR,sram),campaign,campaign)
states=[]
for campaign in (0,1):
    u=resume(sram,campaign,campaign)
    # Native destruction, then a mixture of switched/restored floors.
    if campaign: run(u,0x7b12)
    for i in range(14):w(u,0xffff2150+i*2,65535 if (i+campaign)%3 else 0)
    w(u,0xffff086c,198+campaign);w(u,0xffff0134,11 if campaign else 0)
    states.append(data(u))
    run(u,0x8faa);run(u,V['save21'])
    nxt=bytes(u.mem_read(BUS,0x4000));other=(1-campaign)*0x2000
    assert nxt[other:other+0x2000]==sram[other:other+0x2000]
    sram=nxt
for camp in (0,1):
    u=resume(sram,camp,camp);assert data(u)==states[camp]
    bad=bytearray(sram);bad[camp*0x2000+SIDE+20]^=1
    u=resume(bytes(bad),camp,camp);assert not any(b for region in data(u) for b in region)
    for lab in (0x100,0x101):
        w(u,0xffff026c,lab);before=bytes(u.mem_read(BUS,0x4000))
        for pc in (0x8f74,V['save21'],V['sram17_save']):run(u,pc)
        assert bytes(u.mem_read(BUS,0x4000))==before
print('PASS migrate test20, cold Continue, both campaigns, corrupt suffix and both test map write guards')
