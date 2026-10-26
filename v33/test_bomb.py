exec(open('v33/common.py').read())
# Bomb cannot arm until Enter; each digit clears confirmation.
for confirmed in [0,255]:
 u=machine();w(u,0xffff013c,confirmed,1);w(u,0xffff2198,0x25);u.reg_write(UC_M68K_REG_D0,100)
 run(u,L['bomb26_input'],0x98ae if confirmed else STOP)
for digit in [5,10]:
 u=machine();w(u,0xffff013c,255 if digit==5 else 0,1);w(u,0xffff2198,0x25);u.reg_write(UC_M68K_REG_D0,0)
 def h2(u,a,s,d):
  if a==0x9a96:u.reg_write(UC_M68K_REG_D1,digit);ret(u)
 u.hook_add(UC_HOOK_CODE,h2);run(u,L['bomb26_input'],0x9898 if digit==5 else STOP);assert rd(u,0xffff013c,1)==(0 if digit==5 else 255)
print('PASS bomb Enter/arm/edit state')
