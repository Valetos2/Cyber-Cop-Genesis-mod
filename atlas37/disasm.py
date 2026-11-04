from capstone import *
from pathlib import Path
import sys
r=Path('v30/Cyber-Cop_v30.bin').read_bytes();m=Cs(CS_ARCH_M68K,CS_MODE_BIG_ENDIAN|CS_MODE_M68K_000)
for a,b in zip(sys.argv[1::2],sys.argv[2::2]):
 s=int(a,16);e=int(b,16)
 for i in m.disasm(r[s:e],s):print(f'{i.address:06x} {i.mnemonic:10} {i.op_str}')
