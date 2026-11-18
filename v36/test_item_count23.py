"""Verify the inventory count through its real HUD tile writer."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
ITEMS=0xffff2f50
ITEM=0xffff21ba
u=machine()
writes={}
def vdp(uc,address,size,data):
    pos=uc.reg_read(UC_M68K_REG_D2)&0xffff
    if pos in (0xed32,0xed34):writes[pos]=uc.reg_read(UC_M68K_REG_D0)&0xffff
u.hook_add(UC_HOOK_CODE,vdp,begin=0x35fe,end=0x35fe)
for qty in (0,1,2,9,10,11,19,52,7,1,0):
    u.mem_write(ITEMS,bytes([0x13])*qty+b'\xff'*(52-qty))
    w(u,ITEM,0x13 if qty else -1)
    run(u,0x6eea)
    tens, units = divmod(qty,10)
    want=(0x1b+tens,0x1b+units) if tens else (0x1b+qty if qty>1 else 0,0)
    assert (writes[0xed32],writes[0xed34])==want,(qty,writes)
# Match the selected item's existing condition grouping (including broken flag).
u.mem_write(ITEMS,b'\x53'*12+b'\x13'*5+b'\xff'*35)
w(u,ITEM,0x53);run(u,0x6eea)
assert (writes[0xed32],writes[0xed34])==(0x1c,0x1d)
print('PASS inventory HUD: genuine digits up to 52, old one-digit placement, stale digit erased and empty slot blank')
