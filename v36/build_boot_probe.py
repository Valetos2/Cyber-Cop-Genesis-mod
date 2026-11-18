"""Build a one-change cold-boot diagnostic from a local v36b test01 ROM."""
from pathlib import Path
import hashlib

BASE = 'bbcf44f728058e1cba83dd252900cd65610b001968ca2ac22a80d2bfc84fdf26'
base = Path('Cyber-Cop_v36b_test01.bin').read_bytes()
assert len(base) == 0x400000 and hashlib.sha256(base).hexdigest() == BASE
rom = bytearray(base)
# v35c's two MOVE.W instructions set arguments for the stock hook at $39C.
assert rom[0x394:0x396] == bytes.fromhex('4ef9')
rom[0x394:0x39c] = bytes.fromhex('323c1000343ce000')
checksum = sum((rom[i] << 8) | rom[i+1] for i in range(0x200, len(rom), 2)) & 0xffff
rom[0x18e:0x190] = checksum.to_bytes(2, 'big')
assert all(a == b for i, (a, b) in enumerate(zip(base, rom)) if not (0x18e <= i < 0x190 or 0x394 <= i < 0x39c))
out = Path('Cyber-Cop_v36b_test01_boot_probe.bin')
out.write_bytes(rom)
print(hashlib.sha256(rom).hexdigest(), out)
