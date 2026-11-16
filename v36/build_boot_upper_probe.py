"""Build a read probe on the exact 4 MiB v35c control that ran on hardware."""
from hashlib import sha256
from pathlib import Path

base = Path('Cyber-Cop_v35c_4MiB_boot_control.bin').read_bytes()
assert sha256(base).hexdigest() == '7acea947eb1cfb0a7e610b251a3e22a319b2dc230a0af60b793cbf714981c0af'
rom = bytearray(base)
stub = 0x1F0000
assert rom[0x394:0x39c] == bytes.fromhex('323c1000343ce000')
# The checked addresses cover the beginning and tail of v36's asset area.
# Each CMP.L reads two adjacent 16-bit words from the cart. Wrong data loops
# locally; all correct reads restore the overwritten SEGA setup and boot v35c.
checks = {0x220000: 0xA55A39C6, 0x260000: 0x6D92E718, 0x2AA000: 0xF00D347B}
code = bytearray()
branches = []
for addr, marker in checks.items():
    assert rom[addr:addr+4] == b'\xff'*4
    rom[addr:addr+4] = marker.to_bytes(4, 'big')
    code += bytes.fromhex('0cb9') + marker.to_bytes(4, 'big') + addr.to_bytes(4, 'big')
    code += bytes.fromhex('6600')
    branches.append(len(code))
    code += b'\0\0'
code += rom[0x394:0x39c] + bytes.fromhex('4ef90000039c')
for pos in branches:
    code[pos:pos+2] = (len(code)-pos).to_bytes(2, 'big')
code += bytes.fromhex('60fe')
assert rom[stub:stub+len(code)] == b'\xff'*len(code)
rom[stub:stub+len(code)] = code
rom[0x394:0x39c] = bytes.fromhex('4ef9001f00004e71')
checksum = sum((rom[i]<<8) | rom[i+1] for i in range(0x200, len(rom), 2)) & 0xFFFF
rom[0x18e:0x190] = checksum.to_bytes(2, 'big')
out = Path('Cyber-Cop_v35c_4MiB_upper_read_probe.bin')
out.write_bytes(rom)
print(sha256(rom).hexdigest(), out)
