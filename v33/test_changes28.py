exec(open('v33/common.py').read())
# First TH-low sample: preserve raw value, no extra port reads, debounce six samples.
u=machine();u.mem_write(0xffff0150,bytes(8));u.reg_write(UC_M68K_REG_D0,0x33);u.reg_write(UC_M68K_REG_D1,0x12345678);run(u,L['pad28_sample']);assert rd(u,0xffff0150,1)==255 and u.reg_read(UC_M68K_REG_D0)==0x33 and u.reg_read(UC_M68K_REG_D1)==0x12345678
for n in range(1,7):
 u.reg_write(UC_M68K_REG_D0,0x3f);run(u,L['pad28_sample']);assert rd(u,0xffff0152)==n and rd(u,0xffff0154,1)==(255 if n==6 else 0)
# Wait while a panel is open, sleep when world becomes available, never automatically wake.
calls=[]
def h(u,a,s,d):
 if a==0x6fb2:calls.append(a);ret(u)
u.hook_add(UC_HOOK_CODE,h);w(u,0xffff26b8,0x9916,4);w(u,0xffff270e,0,1);w(u,0xffff270f,0,1);run(u,L['pad28_sleep']);assert not calls and rd(u,0xffff0154,1)==255
w(u,0xffff26b8,0x2106,4);run(u,L['pad28_sleep']);assert calls==[0x6fb2] and rd(u,0xffff0154,1)==0
for i in range(12):u.reg_write(UC_M68K_REG_D0,0x3f);run(u,L['pad28_sample']);run(u,L['pad28_sleep'])
assert len(calls)==1
u.reg_write(UC_M68K_REG_D0,0x33);run(u,L['pad28_sample']);assert rd(u,0xffff0152)==0 and rd(u,0xffff0154,1)==0 and len(calls)==1
# VBlank polling reads exactly the same four hardware samples as before.
for low,phase3,extras in [(0x33,0,0x0f),(0x33,0x33,0x3f),(0x3f,0x0f,0x3f)]:
 u=machine();u.mem_write(0xffff0150,bytes(8));reads=[]
 def io(u,acc,a,s,v,d):
  if a==0xa10003:
   value=[low,0x3f,phase3,extras][len(reads)];reads.append(value);u.mem_write(a,bytes([value]))
 u.hook_add(UC_HOOK_MEM_READ,io);run(u,L['raw26']);assert len(reads)==4 and rd(u,0xffff0140)==255
 assert rd(u,0xffff0150,1)==(255 if low==0x33 else 0)
print('PASS existing four pad reads, TH-low detection, six-frame debounce, safe-context sleep once, no automatic wake')
# HUD white is palette0 slot7; world/visor/panel palette routines leave it intact.
for visor in range(4):
 for dark in [0,65535]:
  u=machine();w(u,0xffff283a,0xeee);w(u,0xffff2706,255 if dark else 0,1);u.reg_write(UC_M68K_REG_D0,visor);run(u,0x5122);assert rd(u,0xffff283a)==0xeee
  u.mem_write(0x1646,bytes.fromhex('4e75'));run(u,0x51bc);assert rd(u,0xffff283a)==0xeee
font=ROM[L['name27_font']:L['name27_font']+1280];assert set(n for b in font for n in [b>>4,b&15])=={0,2,7}
print('PASS HUD palette entry unchanged by all visor modes, lights-out choice and panel palette clearing; gray/white glyph index7')
# Native credits: all original nonblank rows first, then one blank, then our block and original tail.
orig=Path('upload/Cyber-Cop_(W)_[c][!].bin').read_bytes();old=[orig[a:a+40] for a in range(0x1736,0x1eb6,40)];last=max(i for i,row in enumerate(old) if row.strip());a=L['credits26_text'];new=[]
while ROM[a]:new.append(ROM[a:a+40]);a+=40
assert new[:last+1]==old[:last+1] and new[last+1]==b' '*40
expected=[' romhack by',' '*18+'valentin valet2 kozin',' '*18+'and gpt 6 astra',' '*18+'2026']
assert new[last+2:last+6]==[x.ljust(40).encode() for x in expected]
assert new[last+6:]==old[last+1:] and len(new)==len(old)+5
print('PASS credits at end after one blank line, all original credits and trailing blank rows retained')
# Record actual SRAM writes, all odd addresses and below header end, no mapper overlap.
u=machine();run(u,0x8faa);writes=[]
def wr(u,acc,a,s,v,d):
 if 0x200000<=a<0x204000:writes.append((a,s))
u.hook_add(UC_HOOK_MEM_WRITE,wr);run(u,L['save21']);assert all(a&1 and s==1 for a,s in writes);assert max(a for a,s in writes)==0x200803
assert ROM[0x1b0:0x1bc]==bytes.fromhex('5241f8200020000100203fff')
print('PASS SRAM odd-address byte writes, highest address $200803, 1026-byte used span within 8 KiB declared SRAM')
