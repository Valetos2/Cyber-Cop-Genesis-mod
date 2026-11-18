"""Separate the SRAM declaration and filler changes in hardware-confirmed test H."""
from hashlib import sha256
from pathlib import Path
from struct import pack

def checked(path, digest):
    data=Path(path).read_bytes()
    assert len(data)==0x400000 and sha256(data).hexdigest()==digest
    return data

h=checked('H_v36b_asset_readout_D_layout.bin','612ecaddce22a9e0028c8309dc5a11de3c3de66b3ba2709b496b1a6986804767')
g=checked('G_v36b_asset_readout.bin','28d60b5a5a7e5f732de3115435cea2a58552f3731a225b1fe93d83f151ca79c0')
assert g[0x1b0:0x1b2]==b'RA' and h[0x1b0:0x1bc]==b' '*12
i=bytearray(h)
i[0x1b0:0x1bc]=g[0x1b0:0x1bc]
assert i[:0x1b0]==h[:0x1b0] and i[0x1bc:]==h[0x1bc:]
j=bytearray(h)
j[0x200000:0x220000]=g[0x200000:0x220000]
j[0x2aa392:]=g[0x2aa392:]
j[0x18e:0x190]=pack('>H',sum((j[a]<<8)|j[a+1] for a in range(0x200,len(j),2))&0xffff)
assert j[0x220000:0x2aa392]==h[0x220000:0x2aa392]
assert j[:0x18e]==h[:0x18e] and j[0x190:0x200000]==h[0x190:0x200000]
for name,rom in [('I_v36b_readout_SRAM_header.bin',i),('J_v36b_readout_erased_padding.bin',j)]:
    Path(name).write_bytes(rom)
    print(sha256(rom).hexdigest(),name)
