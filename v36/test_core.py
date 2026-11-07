from pathlib import Path
import json
from unicorn import *
from unicorn.m68k_const import *
R=Path('v36/Cyber-Cop_v36_WORK_IN_PROGRESS.bin').read_bytes();S=json.loads(Path('v36/symbols.json').read_text());V=json.loads(Path('v34/symbols.json').read_text());OLD=Path('v35c/Cyber-Cop_v35c.bin').read_bytes();STOP=0x1efff0
RAM=Path('upload/Cyber-Cop_v12.gs4').read_bytes()[0x2478:0x12478]
def machine(rom=R):
 u=Uc(UC_ARCH_M68K,UC_MODE_BIG_ENDIAN);u.ctl_set_cpu_model(UC_CPU_M68K_M68000);u.mem_map(0,0x400000);u.mem_write(0,rom);u.mem_map(0xffff0000,65536);u.mem_write(0xffff0000,RAM);u.mem_map(0xa00000,0x20000);u.mem_map(0xc00000,0x10000);u.reg_write(UC_M68K_REG_SR,0x2700);u.mem_write(0xffff0100,bytes(0x800));u.hook_add(UC_HOOK_MEM_READ,lambda uc,access,address,size,value,data: uc.mem_write(0xa11100,b'\x00\x00') if address==0xa11100 else None);return u
def w(u,a,v,n=2):u.mem_write(a,(v%(1<<(n*8))).to_bytes(n,'big'))
def rd(u,a,n=2):return int.from_bytes(u.mem_read(a,n),'big')
def run(u,a,end=STOP):
 u.reg_write(UC_M68K_REG_A7,0xfffffe00);w(u,0xfffffe00,STOP,4);u.emu_start(a,end,count=3000000);assert u.reg_read(UC_M68K_REG_PC)==end,(hex(a),hex(u.reg_read(UC_M68K_REG_PC)))
levels=json.loads(Path('amiga_research/maps.json').read_text())[1]
for camp in [0,1]:
 for f in range(16):
  u=machine();w(u,S['CAMP'],camp);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,f);run(u,0x4882)
  got=bytes(u.mem_read(0xffff305a,4000))
  if camp:expected=bytes.fromhex(levels[f]['cells'])
  else:
   v=machine(OLD);run(v,0x2360);run(v,0x2944);w(v,0xffff2606,f);run(v,0x4882);expected=bytearray(v.mem_read(0xffff305a,4000))
   for i in json.loads(Path('v36/original_lamps.json').read_text())[f]:
    assert expected[i]==0;expected[i]=0x82
  assert got==expected,(camp,f,[(i,a,b) for i,(a,b) in enumerate(zip(got,expected)) if a!=b][:8])
print('PASS all32 maps: original changes only verified empty lamp cells; Mission matches Amiga byte-for-byte')
# Independent passwords and SRAM. No menu bypass can mix the two banks.
u=machine();u.mem_write(0x200000,b'\xff'*0x4000)
for camp in [0,1]:
 w(u,S['CAMP'],camp);run(u,0x8faa);raw=bytes(u.mem_read(0xffff259a,12));assert raw[10]&1==camp
 password=bytes(u.mem_read(0xffff25b4,24));before=bytes(u.mem_read(0x200000,0x4000));run(u,V['save21']);after=bytes(u.mem_read(0x200000,0x4000))
 lo=camp*0x2000;assert before[:lo]==after[:lo] and before[lo+0x2000:]==after[lo+0x2000:]
 assert after[lo+1:lo+9:2]==b'CC17'
 v=machine();v.mem_write(0x200000,after);w(v,S['CAMP'],camp);run(v,V['sram17_load']);assert v.reg_read(UC_M68K_REG_D0)==1;assert bytes(v.mem_read(0xffff2580,24))==password
 # Incoming password overrides campaign selection; choose opposite beforehand.
 w(v,S['CAMP'],1-camp);run(v,0xe94,0x124a);assert rd(v,S['CAMP'])==camp
print('PASS password encode/decode campaign routing, independent SRAM banks and original signatures')
