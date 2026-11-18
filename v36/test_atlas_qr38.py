"""Check the intro overlay's tile geometry and native continuation."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import struct
m=Path('v36/atlas_qr_matrix.txt').read_text().splitlines()
tile,names=S['atlas_qr_tiles38'],S['atlas_qr_names38']
def pixel(x,y):
    i=struct.unpack_from('>H',R,names+(y//8*64+x//8)*2)[0]
    if not i:
        return 0
    p=R[tile+(i-40)*32+(y%8)*4+(x%8)//2]
    return (p>>(0 if x%2 else 4))&15
for y in range(19,204):
    for x in range(320):
        expected=int(m[(y-39)//5][(x-87)//5]) if 39<=y<184 and 87<=x<232 else 0
        assert pixel(x,y)==expected
assert any(pixel(x,y) for y in range(6,14) for x in range(320))
assert any(pixel(x,y) for y in range(209,217) for x in range(320))

# Sample real 68000 wait code with controlled active-low button inputs.
# Stubs remove I/O and count VBlanks; the register and branch logic is native.
for seq,count in [([0xf0],300),([0x70,0x70,0xf0,0x70],3),([0xf0,0xb0],1)]:
    u=machine();frames=[];poll=[]
    for p in (0x1602,0x31b0,0x2580,0x1646,0x2930,0x53a8,0x1612,0x7994):
        u.mem_write(p,b'\x4e\x75')
    def input_(uc,*_):
        uc.reg_write(UC_M68K_REG_D0,seq[min(len(poll),len(seq)-1)])
        poll.append(1)
    u.hook_add(UC_HOOK_CODE,input_,begin=0x53a8,end=0x53a8)
    u.hook_add(UC_HOOK_CODE,lambda *_:frames.append(1),begin=0x2930,end=0x2930)
    run(u,0x4f2,0x4fa)
    assert len(frames)==count,(seq,len(frames))
    assert rd(u,0xffff282c)==0xccc
print('PASS QR geometry, 300 VBlanks, held-key rejection, fresh button skip, native story continuation')
