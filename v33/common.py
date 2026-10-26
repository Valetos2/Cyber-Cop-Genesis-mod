from pathlib import Path
import json,random
from unicorn import *
from unicorn.m68k_const import *
from PIL import Image
ROM=Path('v33/Cyber-Cop_v33.bin').read_bytes();OLD=Path('v19/Cyber-Cop_v19.bin').read_bytes();L=json.loads(Path('v33/symbols.json').read_text());STOP=0x1f0000
RAM=Path('upload/Cyber-Cop_v12.gs4').read_bytes()[0x2478:0x12478]
def machine(rom=ROM):
 u=Uc(UC_ARCH_M68K,UC_MODE_BIG_ENDIAN);u.ctl_set_cpu_model(UC_CPU_M68K_M68000);u.mem_map(0,0x210000);u.mem_write(0,rom);u.mem_map(0xffff0000,65536);u.mem_write(0xffff0000,RAM);u.mem_map(0xa00000,0x20000);u.mem_map(0xc00000,0x10000);u.reg_write(UC_M68K_REG_SR,0x2700);u.mem_write(0xffff0100,bytes(16));return u
def w(u,a,v,size=2):u.mem_write(a,(v% (1<<(size*8))).to_bytes(size,'big'))
def rd(u,a,size=2):return int.from_bytes(u.mem_read(a,size),'big')
def ret(u):
 sp=u.reg_read(UC_M68K_REG_A7);p=rd(u,sp,4);u.reg_write(UC_M68K_REG_A7,sp+4);u.reg_write(UC_M68K_REG_PC,p)
def run(u,a,end=STOP):
 u.reg_write(UC_M68K_REG_A7,0xfffffe00);w(u,0xfffffe00,STOP,4);u.emu_start(a,end,count=2000000)
 assert u.reg_read(UC_M68K_REG_PC)==end,(hex(a),hex(u.reg_read(UC_M68K_REG_PC)),hex(end))
