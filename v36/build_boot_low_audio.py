"""Move the v36b startup Z80 image below 2 MiB for a hardware A/B test."""
from hashlib import sha256
import json
from pathlib import Path
from struct import pack

base = Path('Cyber-Cop_v36b_test01.bin').read_bytes()
assert sha256(base).hexdigest() == 'bbcf44f728058e1cba83dd252900cd65610b001968ca2ac22a80d2bfc84fdf26'
symbols = json.loads(Path('v36/symbols.json').read_text())
source = symbols['z80_driver36']
entry = symbols['sound_boot36']
dest = 0x1F8000
length = 0x1400
assert source >= 0x200000 and dest+length <= 0x200000
assert base[0x1567a:0x15680] == b'\x4e\xf9' + pack('>I',entry)
assert base[entry:entry+6] == b'\x41\xf9' + pack('>I',source)
assert base[dest:dest+length] == b'\xff'*length
rom = bytearray(base)
# Keep the upper copy in place, so every other reference remains valid.
rom[dest:dest+length] = base[source:source+length]
rom[entry+2:entry+6] = pack('>I',dest)
rom[0x18e:0x190] = pack('>H',sum((rom[i]<<8)|rom[i+1] for i in range(0x200,len(rom),2))&0xffff)
assert all(a == b for i,(a,b) in enumerate(zip(base,rom))
           if not (0x18e<=i<0x190 or entry+2<=i<entry+6 or dest<=i<dest+length))
out = Path('F_Cyber-Cop_v36b_low_audio.bin')
out.write_bytes(rom)
print(f'{source:06x} -> {dest:06x}',sha256(rom).hexdigest(),out)
