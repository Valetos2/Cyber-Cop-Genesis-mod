exec(open('v34/common.py').read())
# Entire elevator context is text-free, including timer expiry and pending labels.
for pending in [0,255]:
 for timer in [0,990,1100]:
  u=machine();w(u,0xffff26b8,0x8d42,4);w(u,0xffff26eb,255,1);w(u,0xffff0138,pending,1);w(u,0xffff013a,timer);w(u,0xffff2798,1000);calls=[]
  def h(u,a,s,d):
   if a in [0x35fe,L['name27_text']]:calls.append(a);ret(u)
  u.hook_add(UC_HOOK_CODE,h);run(u,L['name26_frame']);assert not calls and rd(u,0xffff0138,1)==rd(u,0xffff013a)==0
# A new selection after leaving elevator still displays normally at shifted coordinates.
u=machine();w(u,0xffff26b8,0x2106,4);w(u,0xffff0138,255,1);w(u,0xffff21ba,23);tiles=[]
def h(u,a,s,d):
 if a==0x35fe:tiles.append(u.reg_read(UC_M68K_REG_D2)&65535);ret(u)
u.hook_add(UC_HOOK_CODE,h);run(u,L['name26_frame']);assert tiles[:14]==list(range(0xe91e,0xe93a,2));assert tiles[14:]==list(range(0xe924,0xe936,2))
print('PASS elevator pending/expired names write no HUD tiles; new world selection renders at x180')
# Both exits from native credit scroller share the reset before intro; no premature music request.
for off in [0,255]:
 u=machine();w(u,0xffff2710,off,1);calls=[]
 def h(u,a,s,d):
  if a==0x150b4:calls.append(u.reg_read(UC_M68K_REG_D0)&65535);ret(u)
 u.hook_add(UC_HOOK_CODE,h);run(u,0x2f78,0x386);assert rd(u,0xffff2710,1)==0 and not calls and u.reg_read(UC_M68K_REG_A7)==0xfffffffe
print('PASS post-credits music on reset before intro, stack preserved, no early theme start')

# Before ID-card/password, remove a still-visible old name once; afterwards never touch password frame.
u=machine();w(u,0xffff26b8,0x8d42,4);w(u,0xffff26eb,0,1);w(u,0xffff013a,1000);calls=[]
def h(u,a,s,d):
 if a==0x35fe:calls.append(a);ret(u)
u.hook_add(UC_HOOK_CODE,h);run(u,L['name26_frame']);assert len(calls)==14;run(u,L['name26_frame']);assert len(calls)==14
print('PASS entering elevator before card removes old visible label once; no stale text remains')
