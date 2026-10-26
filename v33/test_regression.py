exec(open('v33/common.py').read())
# All native music commands: restore v20 gating, except elevator and return-to-theme stop.
for off in [0,255]:
 for busy in [0,1]:
  for cmd in range(54):
   u=machine();w(u,0xffff26e4,0,1);w(u,0xffff2710,off,1);w(u,0xffff7d2a,busy);w(u,0xffff7d2c,0)
   u.reg_write(UC_M68K_REG_D0,cmd);run(u,0x150b4)
   expected=0 if busy else 1 if off and cmd==1 else cmd+1
   assert rd(u,0xffff7d2c)==expected,(off,busy,cmd,expected,rd(u,0xffff7d2c))
print('216 music command/mute/busy combinations passed')
# Native elevator start/arrival commands, including actual entry path and arrival call site.
for off in [0,255]:
 u=machine();w(u,0xffff26e4,0,1);w(u,0xffff2710,off,1);w(u,0xffff7d2a,0);w(u,0xffff7d2c,0);w(u,0xffff218c,0,1);w(u,0xffff7dca,0xb1)
 run(u,0x8d9c,0x8de4);assert rd(u,0xffff7d2c)==34
 w(u,0xffff7d2c,0);run(u,0x8e28,0x8e32);assert rd(u,0xffff7d2c)==(1 if off else 2)
 # Timed environmental sound return-to-theme: muted -> stop, no stuck v21 loop.
 w(u,0xffff7d2c,0);run(u,0x34ae);assert rd(u,0xffff7d2c)==(1 if off else 2)
 w(u,0xffff7d2c,0);w(u,0xffff29ba,65535);w(u,0xffff29bc,100);run(u,0x7cf8);assert rd(u,0xffff7d2c)==(1 if off else 2) and rd(u,0xffff29ba)==0 and rd(u,0xffff29bc)==0
print('Native lift start/arrival and timed-loop completion passed, Music On and Off')
# No-save path cannot clear/reload planes, fade palettes, hide/move cursor or leave main menu.
u=machine();tiles=[];waits=[]
w(u,0xffff29c8,0x108);w(u,0xffff29ce,368);w(u,0xffff011e,1);w(u,0xffff286a,0xeee)
before=bytes(u.mem_read(0xffff282c,256))
def hk(u,a,s,d):
 if a in [0x6dc,0x31b0,0x1612,0x1646,0x2580,0x1602,0xf7b2]:raise AssertionError(('unexpected scene mutation',hex(a)))
 if a==0x35fe:tiles.append((u.reg_read(UC_M68K_REG_D2)&65535,u.reg_read(UC_M68K_REG_D0)&65535));ret(u)
 if a==0x7994:waits.append(u.reg_read(UC_M68K_REG_D1)&65535);ret(u)
u.hook_add(UC_HOOK_CODE,hk);run(u,L['resume17_empty'],L['main18_loop'])
assert waits==[100] and len(tiles)==40
assert [x for x,v in tiles]==list(range(0xe014,0xe03c,2))*2
assert rd(u,0xffff29ce)==368 and rd(u,0xffff29c8)==0x108 and rd(u,0xffff011e)==1
assert bytes(u.mem_read(0xffff282c,256))==before and rd(u,0xffff286a)==0xeee
assert len(set(v for x,v in tiles[20:]))==1
print('No saved game: same v20 tiles, timed erase, main menu/cursor/palette retained')
# Music On/Off toggles preserve active ambient tracks; theme and silence follow setting.
for cmd in [0,1,31,32,33,34,35]:
 for off in [0,255]:
  u=machine();w(u,0xffff0122,cmd+1);w(u,0xffff26e4,0,1);w(u,0xffff2710,off,1);w(u,0xffff7d2a,0);w(u,0xffff7d2c,0);run(u,L['music21_toggle'])
  assert rd(u,0xffff7d2c)==(0 if cmd>=31 else 1 if off else 2)
print('Music toggle preserves all five environmental musical commands')
