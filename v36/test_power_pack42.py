exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
rom=Path(sys.argv[1]).read_bytes() if len(sys.argv)>1 else R
u=machine(rom)
# Optional private GST supplies the starting work RAM; reconstruct the
# actionable moment BEFORE opening the pack, not the already stuck screen.
if len(sys.argv)>2:
    u.mem_write(0xffff0000,Path(sys.argv[2]).read_bytes()[0x2478:0x12478])
def pad(now,old=255):
    w(u,0xffff0004,now);w(u,0xffff0006,old)
    u.reg_write(UC_M68K_REG_D0,now)
    run(u,0x5370)
for a in (0x2930,0x51bc,0x9342,0xdf6e,0x4d18,0x5122,0x38bc,0x79ba,0x38c8,0x7994,0x150d8,0x6738):
    u.mem_write(a,b'\x4e\x75')
view,inv,cursor=0xffff26b8,0xffff270a,0xffff202a
w(u,view,0x87c8,4);w(u,inv,255,1);w(u,0xffff26e2,255,1)
w(u,0xffff0200,0);w(u,0xffff270e,0,1);w(u,0xffff2715,0,1)
u.mem_write(0xffff2f50,bytes([7,6])+b'\xff'*50)
w(u,0xffff2740,0);w(u,0xffff21ba,7);w(u,cursor,0x56a8,4)
w(u,0xffff2a26,394);w(u,0xffff2a28,512)
pad(0xef)
assert rd(u,view,4)==0x8358 and rd(u,0xffff21ba)==6
assert rd(u,inv,1)==255,'inventory lost on Scanman -> Power Pack'
pad(255,0xef);pad(0xfb)
assert rd(u,cursor,4)!=0x56a8
pad(255,0xfb);pad(0xf7)
assert rd(u,cursor,4)==0x56a8
pad(255,0xf7);pad(0xef)
assert rd(u,0xffff26ef,1)==255
run(u,0x8358,0x8378)
assert rd(u,0xffff2a26)==512 and bytes(u.mem_read(0xffff2f50,2))==bytes([255,6])
print('PASS Scanman -> B opens pack, Left/Right moves focus, B charges 394 -> 512; only pack consumed')
