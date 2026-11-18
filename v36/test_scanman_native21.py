"""Scanman must draw the stock gamepad pixels for every valid mouse hold."""
exec(open('v36/test_scanman20.py').read().split('if len(sys.argv)==3:')[0])
from struct import unpack_from

s35=json.loads(Path('v35c/symbols.json').read_text())
n=0xffff01a0
boxes={}
for off in range(0x18e000,0x18e000+18*256,18):
    root,node,x0,x1,y0,y1=unpack_from('>IIhhhh',R,off)
    if root==0x597e and node in (0x5a32,0x5a46,0x5a5a,0x5a6e,0x5a82):
        boxes[node]=((x0+x1)//2,(y0+y1)//2)
assert len(boxes)==5

def move(u, xy):
    w(u,n+4,xy[0]);w(u,n+6,xy[1])
def frame(u):
    run(u,0x38c8)
    return bytes(u.mem_read(0xffff8934,0x3000))
def state(u):
    return rd(u,0xffff2180),rd(u,0xffff217c)
for camp in (0,1):
    for node,xy in boxes.items():
        p=opened(R,0,0x72ac,camp)
        m=opened(R,1,0x72ac,camp)
        if node==0x5a32: # make Reset change brightness too
            for u in (p,m): run(u,0x890a);run(u,0x8940)
        w(p,0xffff2700,255,1);w(m,0xffff2700,255,1)
        normal=frame(p)
        assert normal==frame(m)
        w(p,focus,node,4)
        pad(p,0xef)
        expected=frame(p)
        assert expected!=normal, hex(node)
        move(m,xy);w(m,n+12,1)
        run(m,s35['hit_test'])
        assert rd(m,n+16,4)==node,(hex(node),xy,hex(rd(m,n+16,4)))
        run(m,s35['press_ui'])
        assert frame(m)==expected and state(m)==state(p), hex(node)
        before=state(m)
        run(m,s35['panel_border'])
        assert bytes(m.mem_read(0xffff8934,0x3000))==expected
        other=next(k for k in boxes if k!=node)
        move(m,boxes[other]);assert frame(m)==normal and state(m)==before
        move(m,xy);assert frame(m)==expected and state(m)==before
        run(m,s35['release_ui']);w(m,n+12,0)
        assert frame(m)==normal and state(m)==before
print('PASS identical stock button pixels on both campaigns: click, hold, drag out/in, release; actions fire once')
