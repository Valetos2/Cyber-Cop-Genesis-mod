"""Build a playable v36b hardware test using the confirmed I ROM layout."""
from hashlib import sha256
from pathlib import Path
from struct import pack

def checked(path, digest):
    data=Path(path).read_bytes()
    assert len(data)==0x400000 and sha256(data).hexdigest()==digest
    return data

f=checked('F_Cyber-Cop_v36b_low_audio.bin','89873b4b91ff3a66cb8d8ae1cf9d90cf4da93f5b95437fde9f1a13788963dfa7')
i=checked('I_v36b_readout_SRAM_header.bin','692b20edc62d7f6c9184f50181d9b97b4fff8de315eb259b14de9f46bb020032')
assert i[0x220000:0x2aa392]==f[0x220000:0x2aa392]
assert i[0x1b0:0x1bc]==f[0x1b0:0x1bc] and i[0x1b0:0x1b2]==b'RA'
# Retain all game code and the lower startup driver from F. Match I's loader
# facing header (except checksum) and its complete upper-half byte layout.
rom=bytearray(f)
rom[0x100:0x200]=i[0x100:0x200]
rom[0x200000:]=i[0x200000:]
rom[0x18e:0x190]=pack('>H',sum((rom[a]<<8)|rom[a+1] for a in range(0x200,len(rom),2))&0xffff)
assert rom[0x200:0x200000]==f[0x200:0x200000]
out=Path('K_Cyber-Cop_v36b_hardware_test.bin')
out.write_bytes(rom)
print(sha256(rom).hexdigest(),out)
