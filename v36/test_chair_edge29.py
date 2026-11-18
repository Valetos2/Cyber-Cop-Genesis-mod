"""Verify the exactly scoped asset change and its effect in the reported scene."""
exec(open('v36/probe_saves04.py').read().split("if __name__")[0])
import sys
old=Path(sys.argv[1]).read_bytes()
ptr=0x8eef0+int.from_bytes(R[S['sprite_offsets36']+0xb1*4:S['sprite_offsets36']+0xb2*4],'big')
span=range(ptr-2*992,ptr+6*992) # all the standing frames, including the other angles
assert [a-ptr for a in span if R[a]!=old[a]]==[15*62+y for y in (30,31,32,40,41,42)]
assert all(R[a]==(old[a]&0xf0) for a in span if R[a]!=old[a])
if len(sys.argv)>2:
    from PIL import ImageChops
    def restore_asset(u):
        u.mem_write(ptr,old[ptr:ptr+992])
    before,_=render_save(sys.argv[2],0x204,restore_asset)
    after,_=render_save(sys.argv[2],0x204)
    dif=ImageChops.difference(before,after)
    mask=[(x,y) for y in range(128) for x in range(192) if dif.getpixel((x,y))!=(0,0,0)]
    assert mask and all(x==79 for x,y in mask),dif.getbbox()
    print('PASS original gs7: only the detached right pixel column disappears at yaw $204')
else:
    print('PASS chair frame delta: only six rightmost pixels of the affected view are removed')
