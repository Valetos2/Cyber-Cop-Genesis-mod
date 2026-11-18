"""Exterior pad and cursor behaviour, using the original route dispatcher."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
pad,active,mode,xy=0xffff0004,0xffff0200,0xffff01a0,0xffff01a4
call,button_tile=0xffff2186,0xffff7e30
symbols35=json.loads(Path('v35c/symbols.json').read_text())

def scene(mouse=True, opener=0xff):
    u=machine()
    for p in (0x2930,0x38c8):
        u.mem_write(p,b'\x4e\x75')
    w(u,0xffff202a,0x5644,4)
    w(u,0xffff26b8,0x8b08,4)
    w(u,0xffff0192,255,1)
    w(u,active,mouse)
    w(u,pad,opener)
    w(u,mode,0)
    w(u,xy,0x013f00da,4)
    for p in (0xffff0184,0xffff0188,0xffff01bc):
        w(u,p,0x123456,4)
    w(u,0xffff2606,7) # Warehouse shares the access code for G
    w(u,0xffff260a,8)
    w(u,call,0)
    w(u,button_tile,0x00ad00ae,4)
    run(u,0x8afe)
    return u

def press(u, value):
    w(u,pad,value)
    run(u,0x8b08,0x8b10)

for mask,index in [(0x40,0),(0x10,1)]:
    u=scene(opener=0xff^mask)  # entry while the shortcut is already held
    assert rd(u,mode)==1 and (rd(u,xy),rd(u,xy+2))==(153,81)
    assert all(rd(u,p,4)==0 for p in (0xffff0184,0xffff0188,0xffff01bc))
    run(u,symbols35['hit_test'])
    assert rd(u,0xffff01b0,4)==0x5954
    press(u,0xff^mask)
    assert rd(u,call)==0
    press(u,0xff)
    press(u,0xff^mask)
    assert rd(u,call)==1
    assert rd(u,button_tile+index*2)==0xc1+index
    route=bytes(u.mem_read(0xffff0858,10))
    tiles=rd(u,button_tile,4)
    press(u,0xff^mask)
    press(u,0xff^(mask^0x50))  # opposite key during an active route
    assert bytes(u.mem_read(0xffff0858,10))==route and rd(u,button_tile,4)==tiles
    assert (rd(u,xy),rd(u,xy+2))==(153,81)
    assert rd(u,pad)==0xff^(mask^0x50)

u=scene(False)
press(u,0xbf);press(u,0xef)
assert rd(u,call)==0 and rd(u,xy,4)==0x013f00da and rd(u,mode)==0
assert rd(u,0xffff0184,4)==0x123456
u=scene()
press(u,0x3f)  # A + Start leaves the idle panel on the native cancel path
assert rd(u,call)==0
print('PASS A/B direction, held-on-entry protection, no busy reversal, left-button cursor and Mouse Off')
