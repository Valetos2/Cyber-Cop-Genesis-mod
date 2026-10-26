exec(open('v34/ui_common.py').read())
# Invalid Drop falls left through Use if necessary; valid Drop remains selected.
for item,slot,want in [(31,32,0x5694),(29,0,0x56bc),(23,0,0x56bc)]:
 u=machine();w(u,0xffff2740,slot);w(u,0xffff21ba,item);w(u,0xffff202a,0x56bc,4);u.reg_write(UC_M68K_REG_D7,255);run(u,0x54d2)
 assert rd(u,0xffff202a,4)==want,(item,hex(rd(u,0xffff202a,4)))
print('PASS invalid Drop moves left to a valid icon; valid Drop remains selected')
# Actual Scanman setup and native priority scan, with hardware only stubbed.
for ids,expected in [([27,26,25],2),([27,26],1),([27],0),([],None)]:
 u=machine();u.mem_write(0xffff2f50,bytes([255])*52);u.mem_write(0xffff2f50,bytes(ids));w(u,0xffff2740,10);w(u,0xffff202a,0x56a8,4);u.reg_write(UC_M68K_REG_D7,28)
 for a in [0x1646,0x2930,0x4d18,0x35fe,0xf7b2]:u.mem_write(a,bytes.fromhex('4e75'))
 run(u,0x8720)
 assert rd(u,0xffff26b8,4)==0x87c8
 if expected is not None:assert rd(u,0xffff2740)==expected and rd(u,0xffff202a,4)==0x56a8
 else:assert rd(u,0xffff2740)==10
print('PASS Scanman native Screen priority and Use focus; no selection change when no Screen exists')
# Exterior call action changes neither cursor nor selected inventory item.
for direction in [0,1]:
 u=machine();w(u,0xffff202a,0x5990,4);w(u,0xffff2740,3);w(u,0xffff21ba,9);u.reg_write(UC_M68K_REG_D0,direction);run(u,0x8c36)
 assert rd(u,0xffff202a,4)==0x5990 and rd(u,0xffff2740)==3 and rd(u,0xffff21ba)==9 and rd(u,0xffff2186)==10
print('PASS both external lift call buttons preserve cursor and item, retain native arrival timer')
# Reproduce competing renderers in v33, and prove native HUD uses the same preview in v34.
from capstone import *
oldrom=Path('v33/Cyber-Cop_v33.bin').read_bytes();oldlabels=json.loads(Path('v33/symbols.json').read_text())
for rom,labels,legacy in [(oldrom,oldlabels,True),(ROM,L,False)]:
 u=machine(rom);w(u,0xffff26b8,0x7070,4);w(u,0xffff015c,65535);w(u,0xffff20e4,4096);w(u,0xffff2a2a,200);w(u,0xffff2798,100);values=[];tiles=[]
 def display(uc,pc,size,data):
  if pc==0x3406 and uc.reg_read(UC_M68K_REG_D6)&65535==0xe904:values.append(uc.reg_read(UC_M68K_REG_D4)&65535)
  if pc==0x35fe:tiles.append(uc.reg_read(UC_M68K_REG_D2)&65535);ret(uc)
 u.hook_add(UC_HOOK_CODE,display);run(u,labels['sleep33_bar']);run(u,0x33e2)
 assert values==([456,200] if legacy else [456]),values
 for tick in range(101,130):
  w(u,0xffff2798,tick);run(u,labels['sleep33_bar']);run(u,0x33e2)
 if not legacy:assert set(values)=={456} and rd(u,0xffff2a2a)==200
 if not legacy:
  w(u,0xffff26b8,0x2106,4);run(u,0x33e2);assert values[-1]==200
print('PASS v33 competing Energy writers reproduced (456 then 200); v34 sole native HUD writer stays at 456 during sleep, returns to real energy outside sleep')
# Menu clamps both ends even after Cheats, idle timeout doubled exactly.
def fresh(u):u.mem_write(0xffff0100,bytes(256));w(u,0xffff0100,0x434332,4)
events=[255]+[k for _ in range(12) for k in (253,255)]
u,_,_=ui(events,L['main18_enter'],init=fresh);assert rd(u,0xffff011e)==4
u,_,_=ui(events+[k for _ in range(9) for k in (254,255)],L['main18_enter'],init=fresh);assert rd(u,0xffff011e)==0
u,_,_=ui([65535]*1250,L['main18_enter'],init=fresh);assert rd(u,0xffff0008)==1250
u,_,_=ui([65535]*2501,L['main18_enter'],stop=0x77a,init=fresh);assert u.reg_read(UC_M68K_REG_PC)==0x77a and rd(u,0xffff0008)==0
print('PASS bounded main menu after unlocking Cheats; exactly 2500 idle updates instead of 1250')
# Toggle off clears hover/jump/crouch, keeps native vertical gravity, and releases only owned audio.
for owner in [31,32,33]:
 u=machine();w(u,0xffff26e4,255,1);w(u,0xffff26e5,0,1);w(u,0xffff26e8,255,1);w(u,0xffff26e9,255,1);w(u,0xffff7d2a,0);w(u,0xffff7d2c,0);w(u,0xffff0122,owner+1);w(u,0xffff29ba,0);w(u,0xffff2710,0,1);u.reg_write(UC_M68K_REG_D7,13);run(u,0x7b64)
 assert all(rd(u,a,1)==0 for a in [0xffff26e4,0xffff26e8,0xffff26e9]);assert rd(u,0xffff7d2c)==(2 if owner==32 else 0)
 w(u,0xffff441c,300);w(u,0xffff243e,0)
 heights=[]
 for i in range(12):
  u.reg_write(UC_M68K_REG_A0,0xffff4412);u.reg_write(UC_M68K_REG_D1,110);u.reg_write(UC_M68K_REG_D2,110);run(u,0xb3b0);heights.append(rd(u,0xffff441c))
 assert heights[:3]==[290,270,240] and heights[-1]==110,heights
print('PASS repeat Jet Pack use switches off, preserves other audio, descends with native gravity to standing')
# Opening the outer panel must also retain the selected item, even with an ID card present.
u=machine();u.mem_write(0xffff2f50,bytes([9,29])+bytes([255])*50);w(u,0xffff2740,0);w(u,0xffff21ba,9);w(u,0xffff202a,0x5644,4)
for a in [0x1646,0x2930,0x4d18,0x35fe,0xf7b2]:u.mem_write(a,bytes.fromhex('4e75'))
run(u,0x8a74);assert rd(u,0xffff2740)==0 and rd(u,0xffff21ba)==9 and rd(u,0xffff26b8,4)==0x8b08
print('PASS actual outer lift panel initialization does not select the available ID card')
