"""Verify exported cell buffers against original Amiga 68000 subroutines.
Usage in the analysis directory: python check68k.py (needs unicorn and the scratch sector views)."""
from maps import *
from unicorn import *
from unicorn.m68k_const import *
for i,(name,d,load,reg,prep,src) in enumerate([('d2',0x97800,0x9ed6c,0x9fef0,0x9c968,0x37c00),('mission',0x75000,0x7c1ae,0x7d280,0x79d08,0x9c00)]):
 b=Path(name+'.adf').read_bytes();u=Uc(UC_ARCH_M68K,UC_MODE_BIG_ENDIAN);u.ctl_set_cpu_model(UC_CPU_M68K_M68000);u.mem_map(0,0x200000);u.mem_write(0x4000,b[d+0x4000:]);u.reg_write(UC_M68K_REG_SR,0x2700)
 def run(p):
  u.mem_write(0xeff00,(0xf0000).to_bytes(4,'big'));u.reg_write(UC_M68K_REG_A7,0xeff00);u.emu_start(p-d,0xf0000,count=3000000);assert u.reg_read(UC_M68K_REG_PC)==0xf0000
 u.mem_write(0x100000,b[src+34:src+34+32000]);u.reg_write(UC_M68K_REG_A0,0x100000);u.reg_write(UC_M68K_REG_A1,0x5eea0)
 run(b.index(bytes.fromhex('383c00c7424742002f09'),d));run(prep)
 for f in maps(b,i):
  u.mem_write(reg-d,f['slot'].to_bytes(2,'big'));run(load);g=bytes(u.mem_read(0x3ea9e,4000));assert g.hex()==f['cells'],(name,f['slot'],sum(x!=y for x,y in zip(g,bytes.fromhex(f['cells']))))
 print(name,'16 x 4000 cells OK')
