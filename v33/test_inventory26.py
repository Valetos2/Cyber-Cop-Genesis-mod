exec(open('v33/common.py').read())
for inv,slot,expected in [([23,23,9,9],0,23),([23,9,9,255],0,9),([9,255,255,255,23,23],4,23),([23,255,255,255,9],4,31)]:
 u=machine();u.mem_write(0xffff2f50,bytes([255]*52));u.mem_write(0xffff2f50,bytes(inv));w(u,0xffff2f70,31,1);w(u,0xffff2740,slot)
 def h(u,a,s,d):
  if a==0x6e98:
   i=u.reg_read(UC_M68K_REG_D1)&65535;assert rd(u,0xffff2f50+i,1)==expected,(inv,i,expected);w(u,0xffff2740,i);ret(u)
  elif a==0x6738:ret(u)
 u.hook_add(UC_HOOK_CODE,h);run(u,0x7204)
 assert sum(x!=255 for x in u.mem_read(0xffff2f50,52))==sum(x!=255 for x in inv)
for item in [0,9,19,21,29,83,85]:
 for panel in [0x2106,0x8476,0x8576,0x7c42]:
  u=machine();w(u,0xffff21ba,item);w(u,0xffff26b8,panel,4);run(u,L['refill26_allowed']);ok=(u.reg_read(UC_M68K_REG_D0)&65535)==0
  assert ok==((item&63)not in [19,21] or panel==({19:0x8576,21:0x8476}.get(item&63)))
print('PASS: duplicate retention, last-item right neighbour, context-only refill validity')
