exec(open('v33/ui_common.py').read())
def fresh(u):
 u.mem_write(0xffff0100,bytes(0x100));w(u,0xffff0100,0x434332,4)
def events(n):return [255]+[k for _ in range(n) for k in (253,255)]
# Hidden menu clamps; exactly four Down edges at Options reveal Cheats.
u,_,_=ui([255,254,255],L['main18_enter'],init=fresh);assert rd(u,0xffff011e)==0
for n,want in [(3,3),(4,3),(5,3),(6,3),(7,4),(8,0)]:
 u,_,_=ui(events(n),L['main18_enter'],init=fresh);assert rd(u,0xffff011e)==want,(n,rd(u,0xffff011e));assert bool(rd(u,0xffff0157,1))==(n>=7)
u,_,_=ui(events(5)+[251,255]+events(3),L['main18_enter'],init=fresh);assert rd(u,0xffff0157,1)==0 and rd(u,0xffff0158,1)==3
u,_,_=ui(events(7)+[239],L['main18_enter'],stop=L['cheats31'],init=fresh);assert u.reg_read(UC_M68K_REG_PC)==L['cheats31']
u=machine();w(u,0xffff0157,255,1);w(u,0xffff0158,3,1);run(u,L['seed26'],0x1f82);assert rd(u,0xffff0157,1)==rd(u,0xffff0158,1)==0
print('PASS hidden Cheats, four separate taps, reset by another button, clamp then wrap, new-session reset')
# New threshold arithmetic and unchanged battery routine.
for energy,want in [(76,True),(77,False),(51,True),(512,False)]:
 u=machine();w(u,0xffff26b8,0x2106,4);w(u,0xffff29ac,8);w(u,0xffff2a2a,energy);w(u,0xffff2a2c,512);u.mem_write(0xffff28cc,b'\x06\x66'*16);u.mem_write(L['name26_frame'],bytes.fromhex('4e75'))
 run(u,L['warnings24'],0x2092);assert (bytes(u.mem_read(0xffff28cc,32))==bytes(32))==want
print('PASS energy warning <=15%, with exact boundary at 76/512')
# Lamp is persistent during alarm; native reset removes it afterward.
u=machine();w(u,0xffff227e,0xffff7dc6,4);w(u,0xffff223e,0x50);u.mem_write(0x9d5c,bytes.fromhex('4e75'));u.mem_write(0x2930,bytes.fromhex('4e75'));u.mem_write(0x38c8,bytes.fromhex('4e75'))
for alarm in [65535,65535,0]:
 w(u,0xffff29ba,alarm);run(u,L['keypad32_lamps'],0x9936);assert rd(u,0xffff7dd2)==(0xb2 if alarm else 0xb3)
print('PASS keypad red lamp persists while alarm active, resets on clear')
# Auto-selection exact inventory lookup: absent retains slot; present focuses Use.
for has in [False,True]:
 u=machine();u.mem_write(0xffff2f50,bytes([255])*52);w(u,0xffff2740,7);w(u,0xffff202a,0x5b8a,4);w(u,0xffff26b8,0x9916,4)
 if has:w(u,0xffff2f55,12,1)
 for a in [0x540a,0xf7b2]:u.mem_write(a,bytes.fromhex('4e75'))
 u.reg_write(UC_M68K_REG_D0,12);run(u,0x8f4a)
 assert rd(u,0xffff2740)==(5 if has else 7);assert rd(u,0xffff202a,4)==(0x56a8 if has else 0x5b8a)
print('PASS actual lockpick scan and native item selection; absent case leaves slot/cursor untouched')
# Sleep and expanded lift never write name-label tiles.
for view,slp,card in [(0x7070,255,0),(0x7070,0,0),(0x8d42,0,255)]:
 u=machine();w(u,0xffff26b8,view,4);w(u,0xffff270e,slp,1);w(u,0xffff26eb,card,1);w(u,0xffff0138,255,1);w(u,0xffff013a,100);calls=[]
 def hk(uc,pc,s,d):
  if pc in [0x35fe,L['name27_text']]:calls.append(pc);ret(uc)
 u.hook_add(UC_HOOK_CODE,hk);run(u,L['name26_frame']);assert not calls and rd(u,0xffff013a)==0 and rd(u,0xffff0138,1)==0
print('PASS no item text or clearing writes over expanded sleep/lift HUD')
# Alarm transitions must clear the displayed light, not just the backing tile.
u=machine();w(u,0xffff227e,0xffff7dc6,4);w(u,0xffff223e,0x50);w(u,0xffff7dd2,0xb3);shown=[]
def display(uc,pc,s,d):
 if pc==0x2930:ret(uc)
 if pc==0x38c8:
  if rd(uc,0xffff2700,1):shown.append(rd(uc,0xffff7dd2));w(uc,0xffff2700,0,1)
  ret(uc)
u.hook_add(UC_HOOK_CODE,display)
for alarm in [65535,65535,0,0]:
 w(u,0xffff29ba,alarm);run(u,L['keypad32_frame'],0x991e)
assert shown==[0xb2,0xb3],shown
print('PASS alarm on/off redraws the displayed lamp only on state changes')
