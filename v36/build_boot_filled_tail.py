"""Change only v36b test01's unused trailing padding, keeping its checksum."""
from hashlib import sha256
from pathlib import Path

base = Path('Cyber-Cop_v36b_test01.bin').read_bytes()
assert len(base) == 0x400000
assert sha256(base).hexdigest() == 'bbcf44f728058e1cba83dd252900cd65610b001968ca2ac22a80d2bfc84fdf26'
tail = 0x2AA392
assert base[tail:] == b'\xff' * (len(base) - tail)
# Each pair of words sums to -2 mod 65536, as did the two erased words.
pattern = bytes.fromhex('5194ae6a')
length = len(base) - tail
rom = base[:tail] + pattern * (length // 4)
if length % 4:
    rom += bytes.fromhex('ffff')
assert len(rom) == len(base) and rom[:tail] == base[:tail]
def checksum(b):
    return sum((b[i] << 8) | b[i+1] for i in range(0x200, len(b), 2)) & 0xffff
assert checksum(rom) == checksum(base) == int.from_bytes(base[0x18e:0x190], 'big')
out = Path('E_Cyber-Cop_v36b_filled_tail.bin')
out.write_bytes(rom)
print(sha256(rom).hexdigest(), out)
