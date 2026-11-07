exec(open('v36/test_core.py').read().split('levels=json')[0])
# Lab entry at4966 must remain intact, including orientation postprocessing.
v35=json.loads(Path('v35c/symbols.json').read_text())
assert R[0x4966:0x496c]==OLD[0x4966:0x496c]
for rom in [OLD,R]:
 u=machine(rom);w(u,0xffff026c,0x100);run(u,0x2360);run(u,0x2944);run(u,v35['floor35']);got=bytes(u.mem_read(0xffff305a,4000))
 if rom==OLD:expect=got
 else:assert got==expect
print('PASS test map01 geometry and door postprocessing match v35c')
# Each trip completes with skipped VBlanks as well as repeated calls in one tick.
for start in range(0,28,2):
 for target in range(0,28,2):
  u=machine();w(u,0xffff2190,start);w(u,0xffff218e,target);w(u,0xffff0832,1)
  for tick in range(1,1000,3):
   w(u,0xffff2798,tick)
   # Stop at native arrival before floor transition, otherwise at RTS.
   u.reg_write(UC_M68K_REG_A7,0xfffffe00);w(u,0xfffffe00,STOP,4)
   done=[]
   def hk(uc,a,sz,d):
    if a==0x8e1c:done.append(True);uc.emu_stop()
   hook=u.hook_add(UC_HOOK_CODE,hk);u.emu_start(S['lift_clock36b'],STOP,count=1000);u.hook_del(hook)
   if done:break
   before=rd(u,0xffff2190);run(u,S['lift_clock36b']);assert rd(u,0xffff2190)==before
  else:raise AssertionError((start,target))
  assert rd(u,0xffff2190)==target
print('PASS all196 elevator trips, same-floor trips, skipped ticks and no repeated step perVBlank')
# Reproduce the supplied saved HUD: EA3C contains item tile0220 instead of013F.
gst=Path('upload/Cyber-Cop_v36_test01.gs0').read_bytes();u=machine();u.mem_write(0xffff0000,gst[0x2478:0x12478]);vram=bytearray(gst[0x12478:0x22478]);before=bytes(vram)
old_close=int.from_bytes(OLD[0x21da:0x21de],'big');u.mem_write(old_close,b'\x4e\x75');u.mem_write(0x35fe,b'\x4e\x75')
def names(uc,a,sz,d):
 if a==0x35fe:
  dst=uc.reg_read(UC_M68K_REG_D2)&65535;val=uc.reg_read(UC_M68K_REG_D0)&65535;vram[dst:dst+2]=val.to_bytes(2,'big')
u.hook_add(UC_HOOK_CODE,names);run(u,S['terminal_hud36b'])
assert before[0xea3c:0xea3e]==bytes.fromhex('0220') and vram[0xea3c:0xea3e]==bytes.fromhex('013f')
assert [i for i,(a,b) in enumerate(zip(before,vram)) if a!=b]==[0xea3c,0xea3d]
print('PASS saved terminal artifact repaired; every other VRAM byte unchanged')
# Second laboratory keeps native doors, includes both barrels, new stools/lights.
u=machine();w(u,S['CAMP'],1);w(u,0xffff026c,0x101);run(u,0x2360);run(u,0x2944);run(u,v35['floor35']);lab=bytes(u.mem_read(0xffff305a,4000))
for x,z,value in [(22,10,0x9c),(24,10,0x9d),(26,10,0x9e),(26,12,0x95),(14,15,0x82)]:assert lab[(49-z)*80+x]==value,(x,z)
u.mem_write(0x200000,b'\xff'*0x4000);run(u,V['save21']);assert bytes(u.mem_read(0x200000,0x4000))==b'\xff'*0x4000
print('PASS test map02 objects and SRAM write isolation')
