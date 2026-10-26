exec(open('v34/ui_common.py').read())
for menu in ['options14','cheats31']:
 u,tiles,_=ui([255],start=L[menu]);assert rd(u,0xffff4416)==0
 u,_,_=ui([255,254,255],start=L[menu]);assert rd(u,0xffff4416)==5
 u,_,_=ui([255,127],start=L[menu],stop=0x6dc);assert rd(u,0xffff4416)==5
 u,_,_=ui([255]+[x for _ in range(6) for x in [253,255]],start=L[menu]);assert rd(u,0xffff4416)==0
for idx,addr in enumerate([0xffff0104,0xffff0105,0xffff0106,0xffff012c]):
 for key in [239,251,247]:
  u,_,_=ui([255]+[x for _ in range(idx) for x in [253,255]]+[key,255],start=L['cheats31']);assert rd(u,addr,1)==255,(idx,key)
seq=[255]+[x for _ in range(4) for x in [253,255]]
u,_,_=ui(seq+[x for _ in range(10) for x in [247,255]],start=L['cheats31']);assert rd(u,0xffff010e,1)==7 and rd(u,0xffff26bc)==224
u,_,_=ui(seq+[x for _ in range(10) for x in [251,255]],start=L['cheats31']);assert rd(u,0xffff010e,1)==0
# Main menu secret navigation is covered by test_changes32.py.
# Sleep two pages, redraw and value controls, reset on invocation and timeout.
def sleep(sel,key=255,prev=255,active=1,tick=100):
 u=machine();w(u,0xffff0118,active,1);w(u,0xffff0119,sel,1);w(u,0xffff011a,100);w(u,0xffff011c,0,1);w(u,0xffff2798,tick);w(u,0xffff0004,key);w(u,0xffff0006,prev)
 for a in [0x2930,0x4d18]:u.mem_write(a,bytes.fromhex('4e75'))
 run(u,0x7070,0x7088 if active or key!=255 else 0x7078);return u
for sel,key,want in [(0,254,8),(3,253,4),(4,254,3),(8,253,0)]:
 u=sleep(sel,key);assert rd(u,0xffff0119,1)==want,(sel,key,rd(u,0xffff0119,1))
for idx,addr in enumerate([0xffff0104,0xffff0105,0xffff0106,0xffff012c],4):
 u=sleep(idx,239);assert rd(u,addr,1)==255
u=sleep(8,239,active=0);assert rd(u,0xffff0119,1)==0
for sel in range(9):
 u=machine();w(u,0xffff0119,sel,1);run(u,L['sleep16_draw']);assert len(set(u.mem_read(0xffff8934,0x3000)))>1
print('PASS sleep page transitions, flag toggles, invocation resets first page, all nine cursor positions render')
# HUD parity: odd length remains unchanged, even lengths shift right exactly one tile.
for length in range(1,12):
 u=machine();w(u,0xffff0138,255,1);w(u,0xffff26b8,0x2106,4);w(u,0xffff21ba,0);u.mem_write(0x103f3,('a'*length).ljust(11).encode());pos=[]
 def h(uc,a,s,d):
  if a==0x35fe:ret(uc)
  elif a==L['name27_text']:pos.append(uc.reg_read(UC_M68K_REG_D3)&65535);ret(uc)
 u.hook_add(UC_HOOK_CODE,h);run(u,L['name26_frame']);old=0xe900+((44-(length-1))&~1);assert pos==[old+(2 if length%2==0 else 0)],(length,pos)
print('PASS exact one-immediate HUD parity correction for lengths1..11')
# No-input timeout, PAL/NTSC. Crossing pages retains the same timer mechanism.
for pal,frames in [(0,300),(64,250)]:
 u=machine();w(u,0xffff0118,1,1);w(u,0xffff0119,8,1);w(u,0xffff011a,100);w(u,0xffff011c,0,1);w(u,0xffff2798,100+frames);w(u,0xffff0004,255);w(u,0xffff0006,255);w(u,0xa10001,pal,1)
 run(u,0x7070,0x7078);assert rd(u,0xffff0118,1)==0
for key in [191,239,223]:
 u=sleep(0,key,active=0);assert rd(u,0xffff0119,1)==0 and rd(u,0xffff0118,1)==1
# Sleep access edits real current access; action keys do not change numeric selections.
u=machine();w(u,0xffff26bc,96);w(u,0xffff0119,8,1);w(u,0xffff0118,1,1);w(u,0xffff011c,0,1);w(u,0xffff0004,247);w(u,0xffff0006,255)
for a in [0x2930,0x4d18]:u.mem_write(a,bytes.fromhex('4e75'))
run(u,0x7070,0x7088);assert rd(u,0xffff26bc)==128 and rd(u,0xffff010e,1)==4
for key in [191,239,223]:
 u=sleep(2,key);assert rd(u,0xffff0120,1)==0 and rd(u,0xffff0107,1)==0
print('PASS PAL/NTSC timeout, A/B/C invocation, live access editing, dithering arrows-only')
