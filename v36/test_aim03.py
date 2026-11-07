exec(open('v36/test_core.py').read().split('levels=json')[0])
for order,expected in [([17,3],[3,17]),([3,17],[3,17]),([7,17,8,3],[7,3,17,8]),([17,17,3,3],[3,3,17,17]),([7,8,3],[7,8,3]),([17,7],[17,7])]:
 u=machine();w(u,0xffff23b2,0)
 for i,kind in enumerate(order):
  a=0xffff1000+i*0x56;w(u,a+2,kind);u.reg_write(UC_M68K_REG_A2,a);run(u,0xec62)
 ptrs=[rd(u,0xffff23b4+i*4,4) for i in range(rd(u,0xffff23b2)//4)]
 assert [rd(u,p+2) for p in ptrs]==expected,(order,ptrs)
 assert len(set(ptrs))==len(order)
print('PASS autoaim camera-before-lamp stable insertion; all other target order retained')
