from pathlib import Path
import struct,wave,json,hashlib
from capstone import Cs,CS_ARCH_M68K,CS_MODE_BIG_ENDIAN,CS_MODE_M68K_000
b=Path('amiga3/mission.bin').read_bytes();md=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000)
for a,z in [(0x10930,0x1099a),(0x66b0,0x680c)]:
 for ins in md.disasm(b[a:z],a):print(f'{ins.address:06x} {ins.mnemonic} {ins.op_str}')
print('samples',b[0x32078:0x32098].hex())
