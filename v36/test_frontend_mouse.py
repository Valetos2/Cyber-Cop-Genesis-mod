exec(open('v36/test_core.py').read().split('levels=json')[0])
original_machine=machine
def machine():
 u=original_machine();u.mem_write(0x2930,bytes.fromhex('4e75'));u.mem_write(0x249c,bytes.fromhex('4e75'));return u
FRONT=0xffff0802;N=0xffff01a0;M=0xffff0180;P=0xffff0200
for mode,x,y,edge,expected in [(1,140,92,1,0x108),(1,176,92,1,0x128),(2,140,92,1,0),(2,160,92,1,1),(2,180,92,1,2)]:
 u=machine();w(u,FRONT,mode);w(u,P,1);w(u,M+18,1,1);w(u,N+2,4);w(u,N+4,x);w(u,N+6,y);w(u,M+16,edge);w(u,M+12,edge);u.reg_write(UC_M68K_REG_D0,255);run(u,S['front_mouse36'])
 assert u.reg_read(UC_M68K_REG_D0)&16==0
 assert rd(u,0xffff29ce if mode==1 else 0xffff4416)==expected
 # Continued hold has no new down edge: never generate another click.
 u.reg_write(UC_M68K_REG_D0,255);run(u,S['front_mouse36']);assert u.reg_read(UC_M68K_REG_D0)==255
for x,y in [(126,92),(193,92),(140,86),(140,100)]:
 u=machine();w(u,FRONT,2);w(u,P,1);w(u,M+18,1,1);w(u,N+4,x);w(u,N+6,y);w(u,M+16,1);u.reg_write(UC_M68K_REG_D0,255);run(u,S['front_mouse36']);assert u.reg_read(UC_M68K_REG_D0)==255
u=machine();w(u,FRONT,2);w(u,P,1);w(u,M+18,1,1);w(u,M+16,8);u.reg_write(UC_M68K_REG_D0,255);run(u,S['front_mouse36']);assert u.reg_read(UC_M68K_REG_D0)==127
print('PASS character Accept/Pass, equipment forward/Use/back, right-click ignored, fourth Start, hit boundaries and no held-repeat')

# A held click highlights only the initially pressed region and cannot reactivate
# by leaving and re-entering it while held. No additional action is generated.
u=machine();w(u,FRONT,2);w(u,P,1);w(u,M+18,1,1);w(u,N+4,140);w(u,N+6,92);w(u,M+12,1);w(u,M+16,1);u.reg_write(UC_M68K_REG_D0,255);run(u,S['front_mouse36']);assert rd(u,0xffff0828)==3
w(u,N+4,160);u.reg_write(UC_M68K_REG_D0,255);run(u,S['front_mouse36']);assert rd(u,0xffff0828)==0 and u.reg_read(UC_M68K_REG_D0)==255
w(u,N+4,140);u.reg_write(UC_M68K_REG_D0,255);run(u,S['front_mouse36']);assert rd(u,0xffff0828)==0
print('PASS pressed bevel cancels on exit and never rearms from held drag')

for x in [140,160,180]:
 u=machine();w(u,FRONT,2);w(u,P,1);w(u,M+18,1,1);w(u,N+4,x);w(u,N+6,92);w(u,M+16,2);u.reg_write(UC_M68K_REG_D0,255);run(u,S["front_mouse36"]);assert u.reg_read(UC_M68K_REG_D0)==255
print("PASS right clicks do not select equipment")
