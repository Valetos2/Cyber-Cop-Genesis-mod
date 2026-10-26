exec(open('v34/common.py').read())
# Include native post-movement camera reconstruction; this caught the v26 bug.
for directions in [4,8,5,9,6,10]:
 for angle in [0,2,128,256,510,768,1022]:
  u=machine();w(u,0xffff0004,255^(64|directions));w(u,0xffff260c,angle);w(u,0xffff441c,110);w(u,0xffff4440,110);w(u,0xffff443c,0);w(u,0xffff243c,0x6000);w(u,0xffff26fc,0,1);w(u,0xffff26e4,0,1);w(u,0xffff26e5,0,1)
  for frame in range(20):
   run(u,0xa0ea);run(u,0xb01c)
   assert rd(u,0xffff260c)==angle,(directions,angle,frame,rd(u,0xffff260c))
  assert rd(u,0xffff443c)>0
# Negative control: identical v26 routine rotates 90 degrees in one update.
u=machine(Path('v26/Cyber-Cop_v26.bin').read_bytes());w(u,0xffff0004,0xbb);w(u,0xffff260c,0);w(u,0xffff441c,110);w(u,0xffff4440,110);w(u,0xffff26e4,0,1);w(u,0xffff26e5,0,1);run(u,0xa0ea);run(u,0xb01c);assert rd(u,0xffff260c)==768
print('PASS 840 side/diagonal movement+camera updates at wraparound angles; v26 bug reproduced as negative control')
# Credits run until NUL, not a shared fixed-duration timer. Include all native scrolling.
def credits(rom,addr):
 u=machine(rom);rows=[];waits=[]
 def h(u,a,s,d):
  if a==0xffbe:rows.append(bytes(u.mem_read(u.reg_read(UC_M68K_REG_A5),40)).decode('ascii'));ret(u)
  if a==0x53a8:u.reg_write(UC_M68K_REG_D0,255);ret(u)
  if a==0x2930:waits.append(1);ret(u)
  if a==0x1602:ret(u)
 u.hook_add(UC_HOOK_CODE,h);run(u,addr);return rows,len(waits)
new,nw=credits(ROM,0xbb6);old,ow=credits(Path('upload/Cyber-Cop_(W)_[c][!].bin').read_bytes(),0xbb6)
assert len(new)==len(old)+5 and nw==ow+5*8*7
print('PASS full native credits scroll to NUL with five extra rows')
# Glyphs copied to VRAM: capture genuine native font rendering and tile map updates.
u=machine();w(u,0xffff0138,255,1);w(u,0xffff21ba,23);w(u,0xffff2798,1000);tiles=[];commands=[];pixels=[]
def h(u,a,s,d):
 if a==0x35fe:tiles.append((u.reg_read(UC_M68K_REG_D2)&65535,u.reg_read(UC_M68K_REG_D0)&65535));ret(u)
def writes(u,access,address,size,value,d):
 if address==0xc00004 and size==4:commands.append(value)
 if address==0xc00000:pixels.extend(value.to_bytes(size,'big'))
u.hook_add(UC_HOOK_CODE,h);u.hook_add(UC_HOOK_MEM_WRITE,writes);run(u,L['name26_frame'])
assert [a for a,t in tiles[:14]]==list(range(0xe91e,0xe93a,2))
assert [a for a,t in tiles[14:]]==list(range(0xe924,0xe936,2)),tiles
slots=list(range(277,283))+list(range(288,291));assert [t for a,t in tiles[14:]]==slots
assert len(pixels)==9*32 and set(n for b in pixels for n in [b>>4,b&15])=={0,2,7}
assert commands==[0x40000000|(x*32<<16) for x in slots],commands
# Check this display's glyph tiles are absent from the complete original static HUD map.
orig=Path('upload/Cyber-Cop_(W)_[c][!].bin').read_bytes();used={int.from_bytes(orig[a:a+2],'big')&2047 for a in range(0x38a9e,0x39a9e,2)}
assert not used.intersection(set(range(277,283))|set(range(288,293)))
print('PASS item text centered at x180, native font in gray palette entry7, only unused HUD tiles overwritten')
Path('v34/name_pixels.bin').write_bytes(bytes(pixels))
