exec(open('v33/common.py').read())
# Sleep: four native Energy tiles, never numeric glyphs or mutation of stored energy.
for energy in [0,1,200,500,512]:
 for elapsed in [0,255,256,4096,65535]:
  u=machine();w(u,0xffff015c,65535);w(u,0xffff20e4,elapsed);w(u,0xffff2a2a,energy);w(u,0xffff2798,100);writes=[]
  def tile(uc,pc,s,d):
   if pc==0x35fe:writes.append((uc.reg_read(UC_M68K_REG_D2)&65535,uc.reg_read(UC_M68K_REG_D0)&65535));ret(uc)
  u.hook_add(UC_HOOK_CODE,tile);before=bytes(u.mem_read(0xffff0200,512));run(u,L['sleep33_bar']);total=min(512,energy+(min(elapsed>>4,496)&496))
  assert rd(u,0xffff015c)==total and rd(u,0xffff2a2a)==energy and bytes(u.mem_read(0xffff0200,512))==before
  assert [a for a,v in writes]==[0xe904,0xe906,0xe908,0xe90a]
  ref=machine();refwrites=[]
  def rt(uc,pc,s,d):
   if pc==0x35fe:refwrites.append((uc.reg_read(UC_M68K_REG_D2)&65535,uc.reg_read(UC_M68K_REG_D0)&65535));ret(uc)
  ref.hook_add(UC_HOOK_CODE,rt);ref.reg_write(UC_M68K_REG_A1,0x3440);ref.reg_write(UC_M68K_REG_D4,total);ref.reg_write(UC_M68K_REG_D6,0xe904);run(ref,0x3406);assert writes==refwrites
  writes.clear();w(u,0xffff2798,101);run(u,L['sleep33_bar']);assert not writes
print('PASS live native Energy bar, unchanged stored energy, no glyph cache, no redundant tile writes')
# Native wake still adds the original gain exactly once after many previews.
u=machine();w(u,0xffff2a2a,200);w(u,0xffff20e4,4096);w(u,0xffff015c,65535);u.mem_write(0x35fe,bytes.fromhex('4e75'));run(u,L['sleep33_bar']);run(u,0x70be,0x70ec);assert rd(u,0xffff2a2a)==456
print('PASS wake adds gain once, matching the displayed bar')
# Gas priority and broken masks across positions: compare actual damage call, not text.
for masks,want in [([],True),([16],True),([15],False),([16,15],False),([15,16],False),([16,79],True),([80,15],False)]:
 for reverse in [False,True]:
  u=machine();u.mem_write(0xffff2f50,bytes([255])*52);seq=masks[::-1] if reverse else masks
  for i,item in enumerate(seq):w(u,0xffff2f50+i*51,item,1)
  w(u,0xffff26f3,255,1);w(u,0xffff26f2,255,1);w(u,0xffff272a,4000);w(u,0xffff2a2a,200);hits=[]
  def damage(uc,pc,s,d):
   if pc==0xacfe:hits.append(1);ret(uc)
  u.hook_add(UC_HOOK_CODE,damage);u.reg_write(UC_M68K_REG_D2,0x12345678);run(u,0x31f4);assert bool(hits)==want,(seq,hits);assert u.reg_read(UC_M68K_REG_D2)==0x12345678
print('PASS intact Gas Mask overrides Face Mask in either order; broken masks ignored')
# Decoder cannot start while game alarm flag is set, whether B or Y calls it.
for alarm in [0,65535]:
 u=machine();w(u,0xffff29ba,alarm);w(u,0xffff26b8,0x9916,4);w(u,0xffff21aa,123);u.reg_write(UC_M68K_REG_D7,12);run(u,0x9bdc)
 assert rd(u,0xffff26b8,4)==(0x9916 if alarm else 0x98dc);assert (rd(u,0xffff21aa)==123)==bool(alarm)
print('PASS alarm blocks lockpick activation; clear alarm allows native decoder')
# Reproduce old first-use suppression, and clear it at the actual lift-exit hook.
u=machine();w(u,0xffff2715,255,1);w(u,0xffff26de,0,1);w(u,0xffff2740,0);u.mem_write(0xffff2f50,bytes([14])+bytes([255])*51);w(u,0xffff21ba,14);run(u,0x72ac);assert rd(u,0xffff26de,1)==0 and rd(u,0xffff2715,1)==0
w(u,0xffff2715,255,1);u.mem_write(0x9342,bytes.fromhex('4e75'));run(u,L['lift33_arrived'],0x2190);assert rd(u,0xffff2715,1)==0
w(u,0xffff014e,0xa6,1);w(u,0xffff0014,0);w(u,0xffff270a,0,1);w(u,0xffff26b8,0x2106,4);w(u,0xffff0004,255);w(u,0xffff0140,255);w(u,0xffff0144,0);samples=iter([(0,2),(2,0)])
def tap(uc,pc,s,d):
 if pc==L['raw26']:
  prev,cur=next(samples);w(uc,0xffff0142,255);w(uc,0xffff0140,255);w(uc,0xffff0146,prev);w(uc,0xffff0144,cur);uc.reg_write(UC_M68K_REG_D0,255);ret(uc)
u.hook_add(UC_HOOK_CODE,tap);run(u,L['buffer26_sample'],0x1755e);run(u,L['buffer26_sample'],0x1755e);assert rd(u,0xffff014a)&2
run(u,L['buffer26_consume']);run(u,L['item_keys']);assert rd(u,0xffff26de,1)==255
run(u,L['buffer26_consume']);run(u,L['item_keys']);assert rd(u,0xffff26de,1)==255
print('PASS Y press+release buffered between loops, real Computer toggles once; lift latch cleared before use')
# Jetpack ownership: never stop an active alarm on jet shutdown; battery empty releases jet loop.
for music_off in [0,255]:
 for owner in [32,31,1,33]:
  u=machine();w(u,0xffff2710,music_off,1);w(u,0xffff7d2a,0);w(u,0xffff7d2c,0);w(u,0xffff0122,owner+1);w(u,0xffff26e4,255,1);w(u,0xffff26de,255,1);w(u,0xffff29ba,0);run(u,L['jet33_empty'],0x32be)
  assert rd(u,0xffff26e4,1)==0 and rd(u,0xffff26de,1)==0
  assert rd(u,0xffff7d2c)==((1 if music_off else 2) if owner==32 else 0)
for alarm in [0,65535]:
 u=machine();w(u,0xffff29ba,alarm);w(u,0xffff7d2a,0);w(u,0xffff7d2c,0);w(u,0xffff26e4,0,1);u.reg_write(UC_M68K_REG_D7,13);run(u,0x7b64);assert rd(u,0xffff26e4,1)==255 and rd(u,0xffff7d2c)==(0 if alarm else 33)
 u=machine();w(u,0xffff26e4,255,1);w(u,0xffff7d2a,0);w(u,0xffff7d2c,0);w(u,0xffff29ba,alarm);run(u,0x7cf8);assert rd(u,0xffff7d2c)==33
print('PASS jetpack battery/manual audio ownership, alarm priority, jet sound resumes after False Alarm')
# Exercise native manual shutdown and timer expiry, not just isolated helpers.
for off in [0,255]:
 for owner in [1,31,32,33]:
  u=machine();w(u,0xffff2710,off,1);w(u,0xffff7d2a,0);w(u,0xffff7d2c,0);w(u,0xffff0122,owner+1);w(u,0xffff26e4,255,1);w(u,0xffff26e5,0,1);w(u,0xffff29ba,0);run(u,0x9dce)
  assert rd(u,0xffff26e4,1)==0 and rd(u,0xffff26e9,1)==255
  assert rd(u,0xffff7d2c)==((1 if off else 2) if owner==32 else 0)
 for jet in [0,255]:
  u=machine();w(u,0xffff2710,off,1);w(u,0xffff7d2a,0);w(u,0xffff7d2c,0);w(u,0xffff26e4,jet,1);w(u,0xffff29ba,65535);w(u,0xffff29bc,1);run(u,0x3498)
  assert rd(u,0xffff29ba)==0 and rd(u,0xffff7d2c)==(33 if jet else 1 if off else 2)
print('PASS actual Down+A shutdown and native alarm timeout, Music On/Off, active jet/no jet')
