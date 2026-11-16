"""Read real v36 assets using the header and upper-bank filler of working test D."""
from hashlib import sha256
from pathlib import Path
from struct import pack

def checked(path, digest):
    data=Path(path).read_bytes()
    assert len(data)==0x400000 and sha256(data).hexdigest()==digest
    return data

d=checked('D_v35c_upper_ROM_readout.bin','f97ee3f4b8db8aa5ef4c408fc54f31c14a51148f447914acf7eadf890a237c03')
g=checked('G_v36b_asset_readout.bin','28d60b5a5a7e5f732de3115435cea2a58552f3731a225b1fe93d83f151ca79c0')
rom=bytearray(g)
# Reuse D's header and filler. Preserve the real v36 asset block exactly.
lo,hi=0x220000,0x2aa392
assert g[0x200000:lo]==b'\xff'*(lo-0x200000)
assert g[hi:]==b'\xff'*(len(g)-hi)
rom[0x100:0x200]=d[0x100:0x200]
rom[0x200000:lo]=d[0x200000:lo]
rom[hi:]=d[hi:]
rom[0x18e:0x190]=pack('>H',sum((rom[i]<<8)|rom[i+1] for i in range(0x200,len(rom),2))&0xffff)
assert rom[:0x100]==g[:0x100] and rom[0x200:0x200000]==g[0x200:0x200000]
assert rom[lo:hi]==g[lo:hi]
out=Path('H_v36b_asset_readout_D_layout.bin')
out.write_bytes(rom)
print(sha256(rom).hexdigest(),out)
