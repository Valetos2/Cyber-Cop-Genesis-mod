exec(open('v36/test_core.py').read().split('levels=json')[0])
# Busy call never changes initial latched button, route, or timers.
for button in [0,1]:
 u=machine();w(u,0xffff2186,1);w(u,0xffff7e30,0xc100ae,4);u.mem_write(0xffff0858,b'\x12\x34'*4);before=bytes(u.mem_read(0xffff0858,8));u.reg_write(UC_M68K_REG_D0,button);run(u,0x8c36)
 assert rd(u,0xffff7e30,4)==0xc100ae and bytes(u.mem_read(0xffff0858,8))==before
# Idle native up/down paths still initiate the requested journey.
for button in [0,1]:
 u=machine();w(u,0xffff2186,0);w(u,0xffff260a,12);w(u,0xffff2182,16);u.reg_write(UC_M68K_REG_D0,button);run(u,0x8c36);assert rd(u,0xffff2186)==1
 assert rd(u,0xffff7e30+button*2)==0xc1+button
print('PASS busy action guard and idle native calls')
old=json.loads(Path('v35c/symbols.json').read_text())
for node in [0x5954,0x5968]:
 table=next(0x18e000+i*18 for i in range(100) if int.from_bytes(R[0x18e004+i*18:0x18e008+i*18],'big')==node);bounds=0x1d8000+table-0x18e000
 x,y=[int.from_bytes(R[bounds+j:bounds+j+2],'big') for j in [8,12]]
 for held,inside,owned in [(1,True,True),(0,True,True),(1,False,True),(1,True,False)]:
  u=machine();w(u,0xffff0200,1);w(u,0xffff01c8,0x58a0,4);w(u,0xffff01b4,node if owned else 0,4);w(u,0xffff020c,table,4);w(u,0xffff01ac,held);w(u,0xffff01a4,x if inside else x-1);w(u,0xffff01a6,y)
  pair=0xad00c2 if node==0x5954 else 0xc100ae;w(u,0xffff7e30,pair,4);seen=[]
  u.mem_write(old['panel_render06'],bytes.fromhex('4e75'));u.hook_add(UC_HOOK_CODE,lambda uc,a,s,d:seen.append(rd(uc,0xffff7e30,4)) if a==old['panel_render06'] else None)
  run(u,S['lift_feedback36e']);assert seen==[0xc100c2 if held and inside and owned else pair],(node,held,inside,owned,seen)
  assert rd(u,0xffff7e30,4)==pair
print('PASS temporary second-button texture: hold, release, pointer exit, ownership and restoration')
# Version is drawn by the new main menu, not a dead previous menu text routine.
u=machine();u.mem_write(0xffbe,bytes.fromhex('4e75'));u.mem_write(V['sram17_load'],bytes.fromhex('70004e75'));texts=[]
def text_hook(uc,a,s,d):
 if a==0xffbe:texts.append(bytes(uc.mem_read(uc.reg_read(UC_M68K_REG_A5),(uc.reg_read(UC_M68K_REG_D7)&65535)+1)))
u.hook_add(UC_HOOK_CODE,text_hook);run(u,S['main36_text']);assert b'v36' in texts
print('PASS main menu draws v36')
assert R[0xb8b0:0xb8b2]==bytes.fromhex('0040')
assert R[0x196000+0xb1*128:0x196000+0xb2*128]==OLD[0x196000+0xb1*128:0x196000+0xb2*128]
print('PASS native barrel world centre64; armed red bomb lens unchanged')
