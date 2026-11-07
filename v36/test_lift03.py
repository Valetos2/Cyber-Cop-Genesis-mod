exec(open('v36/test_core.py').read().split('levels=json')[0])
for start in range(0,28,2):
 for target in range(0,28,2):
  for button in [0,1]:
   u=machine();w(u,0xffff260a,start);w(u,0xffff2182,target);w(u,0xffff2186,0);w(u,0xffff2798,65500);u.reg_write(UC_M68K_REG_D0,button);run(u,0x8c4c,0x8c54)
   expected=20 if start==target else abs(start-target)//2*80+(160 if (target<start)!=(button==0) else 0)
   assert rd(u,0xffff085a)==expected,(start,target,button)
   for t in range(5,expected+1,5):
    w(u,0xffff2798,65500+t)
    try:run(u,0x8b18,0x8b2a if t>=expected else STOP)
    except Exception:
     print(start,target,button,t,expected,rd(u,0xffff085a),rd(u,0xffff0858));raise
    shown=rd(u,0xffff260a);assert min(start,target)<=shown<=max(start,target)
   assert rd(u,0xffff2186)==0 and rd(u,0xffff260a)==target
print('PASS all392 external lift calls: floor distance, directional penalty, visible route, tick wrap and arrival')
for camp in [0,1]:
 u=machine();w(u,S['CAMP'],camp);w(u,0xffff2190,0);w(u,0xffff218e,2);w(u,0xffff0832,0)
 for tick in range(80):w(u,0xffff2798,tick);run(u,S['lift_clock36b']);assert rd(u,0xffff2190)==0
 w(u,0xffff2798,80);run(u,S['lift_clock36b']);assert rd(u,0xffff2190)==2
print('PASS original and Mission use identical80-VBlank travel period')
for camp in [0,1]:
 for lab in [0,0x100,0x101]:
  u=machine();w(u,S['CAMP'],camp);w(u,0xffff026c,lab);run(u,0x7790,0x7798);assert rd(u,0xffff243a)==(0x451 if lab else 0x8652 if camp else 0x9831)
print('PASS fixed Mission8652, original9831 and lab0451 code routing')
