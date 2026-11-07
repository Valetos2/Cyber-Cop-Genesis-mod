exec(open('v36/test_core.py').read().split('levels=json')[0])
# Every initial enemy must have valid callbacks, correct count and map coordinates.
import struct
A=Path('amiga3/mission.bin').read_bytes()
for f in range(16):
 u=machine();w(u,S['CAMP'],1);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,f);run(u,0x4882);run(u,0x685e);run(u,0x3fb2)
 p=struct.unpack_from('>I',A,0x175de+f*4)[0];expected=[]
 while A[p:p+2]!=b'\xff\xff':
  x,z,ctor,extra=struct.unpack_from('>HHII',A,p);expected.append((x,z));p+=12
 live=[]
 for a in range(0xffff4468,0xffff4f7e,0x56):
  if rd(u,a+2):
   live.append((rd(u,a+8),rd(u,a+12)))
   assert 0<rd(u,a+0x3a,4)<len(R),(f,hex(a),hex(rd(u,a+0x3a,4)))
   assert 0<rd(u,a+0x4a,4)<len(R),(f,hex(a),'damage')
 assert sorted(live)==sorted(expected),(f,live,expected)
print('PASS all16 initial enemy lists: constructors, callbacks, coordinates')
u=machine();run(u,0x685e);u.reg_write(UC_M68K_REG_D0,0x1080);u.reg_write(UC_M68K_REG_D2,0x2080);run(u,S['robot_constructor36']);a=u.reg_read(UC_M68K_REG_A0)
assert rd(u,a+2)==0x801d and rd(u,a+0x1a)==15 and rd(u,a+0x1e)==253
# Enter melee explicitly. Only the third frame should deliver eight damage, once.
u.mem_write(0x150d8,b'\x4e\x75');w(u,0xffff441a,0x1080);w(u,0xffff441e,0x2080);w(u,a+0x34,0)
hits=[]
def hook(uc,pc,size,data):
 if pc==0xacfe:
  hits.append(uc.reg_read(UC_M68K_REG_D4));sp=uc.reg_read(UC_M68K_REG_A7);uc.reg_write(UC_M68K_REG_PC,rd(uc,sp,4));uc.reg_write(UC_M68K_REG_A7,sp+4)
u.hook_add(UC_HOOK_CODE,hook)
for i in range(5):
 u.reg_write(UC_M68K_REG_A0,a);run(u,S['robot36_c92c']);assert rd(u,a+0x20) in [277,278,279]
assert hits==[8],hits
# Native negative-health threshold, three death images then free the actor.
u.reg_write(UC_M68K_REG_A1,a);u.reg_write(UC_M68K_REG_D4,16);run(u,S['robot36_ca1a']);assert rd(u,a+0x3a,4)==S['robot36_ca3a']
for i in range(6):u.reg_write(UC_M68K_REG_A0,a);run(u,S['robot36_ca3a'])
assert rd(u,a+2)==0
print('PASS robot constructor, five-frame attack, single eight-point hit, death and release')
