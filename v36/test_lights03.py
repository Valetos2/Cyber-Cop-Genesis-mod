exec(open('v36/test_core.py').read().split('levels=json')[0])
def ellipse(h,rx,cx=96,cy=64,native=False):
 u=machine();u.mem_write(0xffff8934,bytes(12288));u.mem_write(0xffff1000,bytes(10))
 for off,val in [(0,7),(2,cx),(4,cy),(6,h),(8,rx)]:w(u,0xffff1000+off,val)
 u.reg_write(UC_M68K_REG_A0,0xffff1000);u.reg_write(UC_M68K_REG_D3,7);w(u,0xffff2690,7);run(u,0xe146)
 if native:u.mem_write(0xd4a0,OLD[0xd4a0:0xd4a6])
 count=[0];u.hook_add(UC_HOOK_CODE,lambda uc,a,sz,d:count.__setitem__(0,count[0]+1));run(u,0xd4a0)
 return u,count[0]
def pixels(u):
 b=bytes(u.mem_read(0xffff8934,12288));out=set()
 for y in range(128):
  ptr=int.from_bytes(R[0x6348+y*4:0x634c+y*4],'big')
  for x in range(192):
   off=ptr-0xffff8934+x//8*512+x%8//2
   if b[off]>>(0 if x&1 else 4)&15:out.add((x,y))
 return out
for h in [1,2,3,7,17,64,128,300,512]:
 for rx in [1,3,16,64,128]:
  u,n=ellipse(h,rx);p=pixels(u);assert p,(h,rx)
  assert all((192-x,y) in p for x,y in p if 0<192-x<192),(h,rx,'x')
  assert all((x,128-y) in p for x,y in p if 0<=128-y<128),(h,rx,'y')
  if h==1:assert len({y for x,y in p})==3,(h,rx,p)
for h,rx,cy in [(1,4,64),(10,32,64),(100,64,64),(300,128,64),(300,128,350)]:
 a,old=ellipse(h,rx,cy=cy,native=True);b,new=ellipse(h,rx,cy=cy);print('ellipse',h,rx,cy,'native',old,'new',new)
print('PASS ellipses at45 scales: symmetry, visibility and three-row smallest light')
