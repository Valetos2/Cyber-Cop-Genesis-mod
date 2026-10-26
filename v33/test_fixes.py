exec(open('v33/common.py').read())
orig=Path('upload/Cyber-Cop_(W)_[c][!].bin').read_bytes();v23=Path('v23/Cyber-Cop_v23.bin').read_bytes()
assert ROM[0x32be:0x32c4]==orig[0x32be:0x32c4]==v23[0x32be:0x32c4]
def frames(rom,save,energy,visor):
 u=machine(rom);u.mem_write(0xffff0000,Path(f'upload/Cyber-Cop_v23.gs{save}').read_bytes()[0x2478:0x12478]);u.mem_write(0xffff0104,bytes(3));w(u,0xffff2a26,0);w(u,0xffff2298,visor);w(u,0xffff26b8,0x2106,4)
 def hk(u,a,s,d):
  if a==0x2680:ret(u)
 u.hook_add(UC_HOOK_CODE,hk);out=[]
 for f in range(128):
  w(u,0xffff29ac,f);w(u,0xffff2a2a,energy);run(u,0x507a);run(u,0x324c);run(u,0x208c,0x20b0);out.append(bytes(u.mem_read(0xffff28ac,128)))
 return out
for save in range(1,6):
 for visor in range(4):
  a=frames(orig,save,512,visor);b=frames(v23,save,512,visor);c=frames(ROM,save,512,visor);assert a==b==c,(save,visor)
  d=frames(ROM,save,51,visor)
  for f in range(128):
   if f%64 not in range(8,15):assert d[f]==a[f],(save,visor,f)
print('Five scenes x four visor modes x128 updates: battery palettes exactly original/v23; low energy only changes its separate window')
# Real provided SRAM through full resume, including the actual native music gate.
for off in [0,255]:
 u=machine();u.mem_write(0x200000,Path('upload/Cyber-Cop_v23.srm').read_bytes());w(u,0xffff2710,off,1);w(u,0xffff7d2a,0);calls=[]
 def hk(u,a,s,d):
  if a==0x150b4:calls.append(u.reg_read(UC_M68K_REG_D0)&65535)
  if a in [0x1612,0x1646,0x2930,0x249c,0x150d8,0x2580,0x31b0,0x1602]:ret(u)
 u.hook_add(UC_HOOK_CODE,hk);run(u,L['resume17'],0xe94);assert rd(u,0xffff7d2c)==1;run(u,0xe94,0x124a);w(u,0xffff2712,255,1);run(u,0x1ee0,0x207a)
 assert calls==([] if off else [1]);assert rd(u,0xffff7d2c)==(1 if off else 2);assert rd(u,0xffff2710,1)==off
print('Provided SRAM -> full v25 resume: theme queued only with Music On, Off retained')
