"""Pad the known v35c base to v36's ROM size without changing its game code."""
from hashlib import sha256
from pathlib import Path

base = Path('v35c/Cyber-Cop_v35c.bin').read_bytes()
assert len(base) == 0x200000
assert sha256(base).hexdigest() == 'fc4ac6984e0499d5bfbf7c18df0c3a153e077c9f67973b57edb1981b14b2fde4'
rom = bytearray(base + b'\xff' * len(base))
rom[0x1a4:0x1a8] = (len(rom) - 1).to_bytes(4, 'big')
checksum = sum((rom[i] << 8) | rom[i+1] for i in range(0x200, len(rom), 2)) & 0xffff
rom[0x18e:0x190] = checksum.to_bytes(2, 'big')
assert rom[:0x1a4] == base[:0x1a4] and rom[0x1a8:len(base)] == base[0x1a8:]
out = Path('Cyber-Cop_v35c_4MiB_boot_control.bin')
out.write_bytes(rom)
print(sha256(rom).hexdigest(), out)
