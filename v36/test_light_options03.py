exec(open('v36/test_core.py').read().split('levels=json')[0])
v35=json.loads(Path('v35c/symbols.json').read_text());P=0xffff0200;N=0xffff01a0;OFF=0xffff0856
# Renderer switch prevents even building lamp queue; no gameplay map mutation.
u=machine();w(u,OFF,255,1);w(u,0xffff5338,0xffff533c,4);run(u,0xcfc8);assert rd(u,0xffff5338,4)==0xffff533c
for present,on,expected in [(0,0,6),(1,0,7),(1,1,8)]:
 u=machine();w(u,0xffff0192,present,1);w(u,P,on);run(u,v35['options35_max']);assert u.reg_read(UC_M68K_REG_D2)==expected
for present,on in [(0,0),(1,0),(1,1)]:
 order=[0,1,2,3,11]+([9] if present else [])+([10] if present and on else [])+[4,5,6,7,8]
 for i,sel in enumerate(order):
  for edge,offset in [(1,-1),(2,1)]:
   u=machine();w(u,P+38,present);w(u,P,on);w(u,0xffff0119,sel,1);u.reg_write(UC_M68K_REG_D4,edge)
   run(u,v35['sleep_nav04'],V['sleep16_changed']);assert rd(u,0xffff0119,1)==order[(i+offset)%len(order)],(present,on,sel,edge,rd(u,0xffff0119,1))
for y,sel in [(24,0),(40,1),(56,2),(72,3),(88,11),(104,9)]:
 u=machine();w(u,P+38,1);w(u,N+4,100);w(u,N+6,y);u.reg_write(UC_M68K_REG_D4,1)
 run(u,v35['sleep_page0'],v35['sleep_click_changed']);assert rd(u,0xffff0119,1)==sel,(y,rd(u,0xffff0119,1))
 if sel==11:assert rd(u,OFF,1)==255
for y in [32,39,48,55,64,71,80,87,96,103,112,119]:
 u=machine();w(u,P+38,1);w(u,N+4,100);w(u,N+6,y);w(u,0xffff0119,3,1)
 run(u,v35['sleep_page0']);assert rd(u,0xffff0119,1)==3 and rd(u,OFF,1)==0
# Render the shifted page with the real native text copier and arrow.
for selected in [0,1,2,3,9,10,11]:
 u=machine();w(u,P+38,1);w(u,0xffff0119,selected,1);run(u,V['sleep16_draw'])
 assert rd(u,0xffff0119,1)==selected
print('PASS lamps option max, complete joystick orders, mouse rows/gaps and native sleep draw')
