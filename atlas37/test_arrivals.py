exec(open('v33/common.py').read())
for f,x,y,df,dx,dy in [(5,76,24,6,3,24),(5,59,4,7,18,46),(6,32,4,7,71,46),(7,71,45,6,30,5),(7,18,45,5,59,5)]:
 u=machine();w(u,0xffff441a,x*256+128);w(u,0xffff441e,(49-y)*256+128);u.reg_write(UC_M68K_REG_A0,0xffff4412);run(u,{5:0x78de,6:0x7918,7:0x7952}[f]);assert (rd(u,0xffff2606),rd(u,0xffff441a)//256,49-rd(u,0xffff441e)//256)==(df,dx,dy)
u=machine();w(u,0xffff2713,0,1);w(u,0xffff2712,255,1);run(u,0x3f02);assert(rd(u,0xffff441a)//256,49-rd(u,0xffff441e)//256)==(6,6)
print('PASS native airlock transforms and 5F initial position')
