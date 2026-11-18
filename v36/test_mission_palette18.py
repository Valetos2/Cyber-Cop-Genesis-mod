"""Mission background palette regression, through the real floor loader."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import struct, sys

before=Path(sys.argv[1]).read_bytes()
amiga=Path('amiga3/mission.bin').read_bytes()
def converted(color):
    rgb=[2*round((color>>shift&15)*7/15) for shift in (8,4,0)]
    return rgb[0]+16*rgb[1]+256*rgb[2]
def colors(rom,camp,slot):
    u=machine(rom)
    w(u,S['CAMP'],camp)
    w(u,0xffff2606,slot)
    run(u,0x50f4)
    return struct.unpack('>24H',bytes(u.mem_read(0xffff296c,48)))

changed=[]
for slot in range(16):
    original=colors(before,0,slot)
    assert colors(R,0,slot)==original
    old=colors(before,1,slot)
    new=colors(R,1,slot)
    if slot in (10,11,12):
        table=struct.unpack_from('>I',amiga,0x131e8+slot*4)[0]
        exact=tuple(converted(struct.unpack_from('>H',amiga,table+i*2)[0]) for i in (24,26,28))
        assert new[17:20]==exact and old[17:20]!=exact
        assert new[:17]+new[20:]==old[:17]+old[20:]
        changed.append(slot)
    else:
        assert new==old
assert changed==[10,11,12]
# Every byte outside the intended palette entries and ROM checksum is identical.
allowed=set(range(0x18e,0x190))
for slot in changed:
    p=S[f'mission_palette_{slot}']
    allowed.update(range(p+32,p+38))
assert len(R)==len(before)==0x400000
assert {i for i,(a,b) in enumerate(zip(R,before)) if a!=b}<=allowed
assert sum(struct.unpack_from('>2096896H',R,0x200))&0xffff==int.from_bytes(R[0x18e:0x190],'big')
print('PASS all 32 runtime palettes; only the Mission L3/L4/L5 ceilings change, to converted Amiga colors')
