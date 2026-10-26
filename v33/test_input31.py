exec(open('v33/common.py').read())
# C is already included in $B0: B=$10,C=$20,Start=$80.
# Simulate a short C tap entirely between game-loop iterations, then native target cycling.
u=machine();w(u,0xffff014e,0xa6,1);w(u,0xffff0014,0);w(u,0xffff270a,0,1);w(u,0xffff0004,255);w(u,0xffff0140,255);w(u,0xffff0144,0)
samples=iter([(255,223),(223,255)])
def h(u,a,s,d):
 if a==L['raw26']:
  prev,cur=next(samples);w(u,0xffff0142,prev);w(u,0xffff0140,cur);w(u,0xffff0146,0);w(u,0xffff0144,0);u.reg_write(UC_M68K_REG_D0,cur);ret(u)
u.hook_add(UC_HOOK_CODE,h)
run(u,L['buffer26_sample'],0x1755e);run(u,L['buffer26_sample'],0x1755e);assert rd(u,0xffff0148)&32
run(u,L['buffer26_consume']);assert rd(u,0xffff0004)==223 and rd(u,0xffff0006)&32
w(u,0xffff29b8,4);w(u,0xffff23b2,8);w(u,0xffff23b4,0xffff4468,4);w(u,0xffff23b8,0xffff44be,4);run(u,0xac1e);assert rd(u,0xffff29b8)==0
run(u,L['buffer26_consume']);run(u,0xac1e);assert rd(u,0xffff29b8)==0
print('PASS short buffered C tap survives release and advances native target selection exactly once; no extra mask change needed')
