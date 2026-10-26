"""Execute original intro/menu setup, model frame ticks and DMA/audio hardware.
This is a CPU/control-flow/resource test, not full console or VDP emulation.
"""
from pathlib import Path
from unicorn import *
from unicorn.m68k_const import *
import json
P=Path('v33');ROM=(P/'Cyber-Cop_v33.bin').read_bytes();L=json.loads((P/'symbols.json').read_text())
STOP=0x180000
class Harness:
 def __init__(self):
  self.u=Uc(UC_ARCH_M68K,UC_MODE_BIG_ENDIAN);u=self.u
  u.ctl_set_cpu_model(UC_CPU_M68K_M68000)
  u.mem_map(0,0x200000);u.mem_write(0,ROM);u.mem_map(0xffff0000,0x10000)
  u.mem_map(0xa00000,0x20000);u.mem_map(0xc00000,0x1000)
  self.buttons=255;self.th=0x40;self.frames=0;self.transfers=[];self.hit=[];self.trigger=None
  self.vram=bytearray(65536);self.w(0xffff0002,0x8164);self.shadow_transfers=[]
  u.hook_add(UC_HOOK_MEM_READ|UC_HOOK_MEM_WRITE,self.io,begin=0xa10003,end=0xa10003)
  u.hook_add(UC_HOOK_CODE,self.code)
  u.reg_write(UC_M68K_REG_SR,0x2500);u.reg_write(UC_M68K_REG_A7,0xfffffffe)
 def w(self,a,v,n=2):self.u.mem_write(a,(v&((1<<(n*8))-1)).to_bytes(n,'big'))
 def r(self,a,n=2):return int.from_bytes(self.u.mem_read(a,n),'big')
 def ret(self):
  u=self.u;sp=u.reg_read(UC_M68K_REG_A7);u.reg_write(UC_M68K_REG_PC,self.r(sp,4));u.reg_write(UC_M68K_REG_A7,sp+4)
 def io(self,u,access,address,size,value,data):
  if access==UC_MEM_WRITE:self.th=value&64
  else:u.mem_write(address,bytes([(64|(self.buttons&63)) if self.th else (((self.buttons>>2)&48)|(self.buttons&3))]))
 def code(self,u,pc,size,data):
  if pc==self.trigger:self.buttons=127;self.hit.append(pc);self.trigger=None
  if pc==0x2938:
   self.frames+=1;self.w(0xffff2798,self.r(0xffff2798)+1)
  if pc in [0x150b4,0x150d8,0x15062]:self.ret()
  if pc==0x249c:
   shadow=self.r(0xffff0002);self.shadow_transfers.append((self.r(0xffff0156,1),shadow));assert not self.r(0xffff0156,1) or not shadow&0x40, 'DMA would re-enable display from stale shadow';count=self.r(0xffff0016)*2;src=self.r(0xffff0018,4);dest=self.r(0xffff001c)
   self.transfers.append((src,dest,count))
   data=bytes(u.mem_read(src,count))
   for i,v in enumerate(data):self.vram[(dest+i)&65535]=v
   self.ret()
  # VDP status reads must return idle independently of prior control writes.
 def run_intro(self,trigger=None):
  self.trigger=trigger
  # initial game font count is in ROM; RAM starts clear just as after boot.
  self.u.emu_start(0x386,0x7a0,count=5000000)
  assert self.u.reg_read(UC_M68K_REG_PC)==0x7a0,hex(self.u.reg_read(UC_M68K_REG_PC))
  assert self.u.reg_read(UC_M68K_REG_A7)==0xfffffffe
  assert self.r(0xffff0014,1)==0 and self.r(0xffff0015,1)==2
  assert self.r(0xffff2794,4)==0xb426
  assert self.r(0xffff4416)==0
  return self
 def status(self,u,access,address,size,value,data):
  u.mem_write(0xc00004,b'\0\0')

def intro(trigger=None):
 h=Harness();h.u.hook_add(UC_HOOK_MEM_READ,h.status,begin=0xc00004,end=0xc00005)
 return h.run_intro(trigger)

for phase in [0x3fc,0x466,0x4cc,0x5e8,0x632,0x6ce]:
 h=Harness();h.trigger=phase;h.u.hook_add(UC_HOOK_MEM_READ,h.status,begin=0xc00004,end=0xc00005);writes=[]
 def wr(u,access,addr,size,value,data):
  if addr==0xc00004 and size==2 and value in [0x8124,0x8164]:writes.append((value,len(h.transfers)))
 h.u.hook_add(UC_HOOK_MEM_WRITE,wr,begin=0xc00004,end=0xc00005)
 h.u.emu_start(0x386,L['main18_loop'],count=5000000)
 assert h.u.reg_read(UC_M68K_REG_PC)==L['main18_loop'],hex(h.u.reg_read(UC_M68K_REG_PC))
 if phase==0x6ce:
  assert 0x8124 not in [x[0] for x in writes];print('PASS already-ready title proceeds without unnecessary display blanking');continue
 assert [x[0] for x in writes][-2:]==[0x8124,0x8164],(hex(phase),writes)
 assert writes[-1][1]>writes[-2][1]
 assert h.r(0xffff0156,1)==0
 print('PASS intro skip',hex(phase),'display disabled across resource transfers',writes)
# Execute the actual DMA register sequence, including shadow-register rewrites.

exec(open('v33/common.py').read())
for blank in [True,False]:
 u=machine();w(u,0xffff0002,0x8124 if blank else 0x8164);w(u,0xffff0016,16);w(u,0xffff0018,0x30716,4);w(u,0xffff001c,0x2000);writes=[]
 def io(uc,access,a,size,value,data):
  if access==UC_MEM_READ and a in [0xc00004,0xa11100]:uc.mem_write(a,bytes(size))
  elif access==UC_MEM_WRITE and a==0xc00004 and size==2 and value&0xff00==0x8100:writes.append(value)
 u.hook_add(UC_HOOK_MEM_READ|UC_HOOK_MEM_WRITE,io);run(u,0x249c)
 assert writes and all(bool(v&0x40)!=blank for v in writes),writes
 assert rd(u,0xffff0002)==(0x8124 if blank else 0x8164)
print('PASS actual 68000 DMA sequence retains display-off in both register writes; old 8164 shadow re-enables display (negative control)')
