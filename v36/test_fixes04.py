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
