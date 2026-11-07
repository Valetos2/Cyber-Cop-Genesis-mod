from pathlib import Path
from capstone import *
import sys
b=Path(sys.argv[3] if len(sys.argv)>3 else 'v35c/Cyber-Cop_v35c.bin').read_bytes();m=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000)
for i in m.disasm(b[int(sys.argv[1],16):int(sys.argv[2],16)],int(sys.argv[1],16)):print(f'{i.address:06x} {i.mnemonic} {i.op_str}')
