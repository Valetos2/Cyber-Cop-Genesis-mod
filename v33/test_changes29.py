exec(open('v33/common.py').read())
orig=Path('upload/Cyber-Cop_(W)_[c][!].bin').read_bytes()
# Background tile and palette at every cleared/text position match the original HUD.
for col in range(15,29):
 a=0x38a9e+18*128+col*2
 assert orig[a:a+2]==bytes.fromhex('011b'),(col,orig[a:a+2].hex())
background=orig[0x37dde:0x37dfe]
for state in ['Cyber-Cop_v25.gs2','Cyber-Cop_v25.gs3','Cyber-Cop_v25.gs4','Cyber-Cop_v25.gs5']:
 v=Path('upload/'+state).read_bytes()[0x12478:0x22478]
 assert v[0x11b*32:0x11c*32]==background
font=ROM[L['name27_font']:L['name27_font']+1280]
for i,b in enumerate(orig[0x30716:0x30716+1280]):
 for shift in [0,4]:
  assert ((font[i]>>shift)&15)==(7 if ((b>>shift)&15) else ((background[i%32]>>shift)&15))
print('PASS all glyph background pixels equal original HUD; palette0 retained; four save-state backgrounds agree')
# Main theme queued/current: do not restart. Silence, sirens and elevator: queue main.
for off in [0,255]:
 for pending,current,track in [(2,2,1),(0,2,1),(0,2,2),(0,1,0),(1,2,1),(34,2,1),(0,34,33),(0,32,31),(0,36,35),(0,2,0)]:
  u=machine();w(u,0xffff2710,off,1);w(u,0xffff7d2a,0);w(u,0xffff7d2c,pending);w(u,0xffff0122,current);w(u,0xffff7d30,track)
  calls=[]
  def h(u,a,s,d):
   if a==0x150c0:calls.append(u.reg_read(UC_M68K_REG_D0)&65535)
  u.hook_add(UC_HOOK_CODE,h);u.reg_write(UC_M68K_REG_D0,0x12345678);u.reg_write(UC_M68K_REG_D1,0xabcdef01)
  run(u,L['ending29_music'])
  keep=pending==2 or (pending==0 and current==2 and track!=0)
  assert calls==([] if keep else [1]),(off,pending,current,track,calls)
  assert rd(u,0xffff7d2c)==(pending if keep else 2)
  assert rd(u,0xffff2710,1)==off
  assert u.reg_read(UC_M68K_REG_D0)==0x12345678 and u.reg_read(UC_M68K_REG_D1)==0xabcdef01
assert ROM[0x2f58:0x2f78]==Path('v28/Cyber-Cop_v28.bin').read_bytes()[0x2f58:0x2f78]
print('PASS ending main theme under music on/off, no restart when already queued/playing, setting and post-credits path unchanged')
