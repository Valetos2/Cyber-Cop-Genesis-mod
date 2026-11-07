from pathlib import Path
from unicorn import *
from unicorn.m68k_const import *
from struct import unpack_from
u=Uc(UC_ARCH_M68K,UC_MODE_BIG_ENDIAN);u.ctl_set_cpu_model(UC_CPU_M68K_M68000);u.mem_map(0,0x200000);u.mem_write(0,Path('st2/loader.bin').read_bytes());u.reg_write(UC_M68K_REG_SR,0x2700)
for name in ['MAIN','INTRO']:
 b=Path('st2/files/'+name).read_bytes();n=unpack_from('>I',b,8)[0];u.mem_write(0x40000,b);u.reg_write(UC_M68K_REG_A0,0x40000);u.reg_write(UC_M68K_REG_A7,0x180000);u.mem_write(0x180000,(0x190000).to_bytes(4,'big'));u.emu_start(0xc86,0x190000,count=20000000);assert u.reg_read(UC_M68K_REG_PC)==0x190000;out=bytes(u.mem_read(0x40000,n));Path('st2/'+name+'.bin').write_bytes(out);print(name,n,out[:12].hex())
