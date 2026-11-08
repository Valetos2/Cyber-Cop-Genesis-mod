exec(open('v36/test_core.py').read().split('levels=json')[0])
# Reset from both brightness extremes; native opening still sets defaults.
for brightness in range(0,17,2):
 u=machine();w(u,0xffff217c,0);w(u,0xffff2180,brightness);run(u,0x8836)
 assert rd(u,0xffff217c)==4 and rd(u,0xffff2180)==8
 assert bytes(u.mem_read(0xffff285c,16))==R[0x8a5c:0x8a6c]
for a in [0xffff217c,0xffff2178,0xffff217a,0xffff217e,0xffff2180]:w(u,a,0x1234)
u.mem_write(0x38bc,bytes.fromhex('4e75'));run(u,0x873c,0x8760)
assert [rd(u,a) for a in [0xffff217c,0xffff2178,0xffff217a,0xffff217e,0xffff2180]]==[4,0,0,0,8]
print('PASS Scanman reset palette and every-entry defaults')
# Projection radius cannot oscillate from rounding two screen positions.
for radius in [64,128]:
 for height in [0,1,128,270,512]:
  previous=65535
  for near in range(256,8193,17):
   u=machine();u.reg_write(UC_M68K_REG_A0,0xffff1000);w(u,0xffff100a,height);w(u,0xffff2624,270);w(u,0xffff2234,radius);u.reg_write(UC_M68K_REG_D7,near)
   u.reg_write(UC_M68K_REG_D0,0x1234);u.reg_write(UC_M68K_REG_D1,0x5678);run(u,0xd050,0xd074)
   got=u.reg_read(UC_M68K_REG_D2)&65535
   expected=max(1,abs(height-270)*256*radius//(near+radius)//near)
   assert got==expected and got<=previous,(radius,height,near,got,expected);previous=got
   assert u.reg_read(UC_M68K_REG_D0)==0x1234 and u.reg_read(UC_M68K_REG_D1)==0x5678
print('PASS lamp radius formula, monotonic depth sweep and preserved centre coordinates')
exec(open('v36/test_lights03.py').read().split('for h in [1,2,3')[0])
for h in [1,2,3,8,17]:
 u,n=ellipse(h,12);p=pixels(u)
 for y in [64-h,64+h]:assert sum(yy==y for x,yy in p)>=3,(h,y)
print('PASS no one-pixel vertical tips at representative lamp sizes')
# Sleep release works for both mouse-owned and ordinary repair state.
for mouse_owned in [0,0x566c]:
 u=machine();w(u,0xffff214c,255);w(u,0xffff202e,0x7192,4);w(u,0xffff01b4,mouse_owned,4)
 run(u,S['sleep_release36d'],S['sleep_sound_stop36']);assert rd(u,0xffff214c)==0 and rd(u,0xffff202e,4)==0 and rd(u,0xffff01b4,4)==0
print('PASS forced/Mode sleep prelude releases repair action and mouse ownership')
for item in [12,13,14,15,16,17,18,20]:
 u=machine();u.reg_write(UC_M68K_REG_A0,0xffff441c);u.reg_write(UC_M68K_REG_D0,item);w(u,0xffff441c+item*4,0xffff1000,4);w(u,0xffff1000,0x1234);run(u,0xfd84,0xfdb0);assert rd(u,0xffff1000)==65535
for item,stop in [(11,0xfd8a),(19,0xfd94),(21,0xfd94),(35,0xfd94)]:
 u=machine();u.reg_write(UC_M68K_REG_D0,item);run(u,0xfd84,stop)
print('PASS unique tools plus preserved native bomb/armour/consumable routes')
# Both character classes pass through the native availability gate. Item first
# aid is human-only; electronics retains its native universal availability.
for char in range(6):
 for item in [15,16,23,24,44]:
  u=machine();w(u,0xffff2a38,char);u.reg_write(UC_M68K_REG_D0,item*4)
  stop=0xfc70 if (item in [15,16,23] and char<2) or (item==44 and char>=2) else 0xfd10
  run(u,0xfce2,stop)
print('PASS all six characters: first aid, electronics and program availability')
# Simulate arbitrary boot palette and menu re-entry. Check writes before fade.
u=machine();u.mem_write(0xffff282c,bytes([0xee])*256);writes=[];texts=[]
for a in [0x31b0,0x2576,0x2580,0xffbe,0x1646]:u.mem_write(a,bytes.fromhex('4e75'))
u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,address,size,value,data:writes.append((address,size,value)) if address in [0xc00000,0xc00004] else None)
u.hook_add(UC_HOOK_CODE,lambda uc,a,s,d:texts.append(uc.reg_read(UC_M68K_REG_D3)&65535) if a==0xffbe else None)
run(u,S['memorial36b'],S['memorial_wait36b'])
assert texts==[0xe58e,0xe68e];assert bytes(u.mem_read(0xffff28ac,128))==bytes(128)
assert writes[:65]==[(0xc00004,4,0xc0000000)]+[(0xc00000,2,0)]*64
assert writes[65:]==[(0xc00004,2,0x4000),(0xc00004,2,0x10),(0xc00000,2,0)]
print('PASS memorial black palette upload before fade, scroll reset and exact test02 text addresses')
# Two terminals share a per-floor access flag; reopening cannot award twice.
for floor in [8,9]:
 u=machine();w(u,0xffff2606,floor);w(u,0xffff26bc,0);w(u,0xffff2718+floor,0,1)
 for visit in range(2):
  w(u,0xffff216e,0);run(u,0x7d76,0x7db2);assert rd(u,0xffff26bc)==32
print('PASS both Mission L1/L2 terminal visits award only one access level per floor')
u=machine();w(u,S['CAMP'],1);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,0);run(u,0x4882);run(u,0x685e);run(u,0x3fb2)
assert rd(u,0xffff305a+27*80+32,1)==0x82
assert any(rd(u,a+2)==0x8006 and rd(u,a+8)//256==32 and 49-rd(u,a+12)//256==27 for a in range(0xffff4468,0xffff4f7e,0x56))
print('PASS Mission 5F lamp and initial robot coexist at X32 Y27')
