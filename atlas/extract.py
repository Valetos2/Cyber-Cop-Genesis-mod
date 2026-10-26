exec(open('v25/common.py').read())
from collections import Counter
r=ROM;codes=Path('upload/Cyber-Cop_v23.gs5').read_bytes()[0x2478+0x2fea:0x2478+0x300a]
names=['5F','4F','3F','2F','1F','G','Parking','Warehouse','L1','L2','L3','L4','L5','L6','L7','L8']
levels=[]
for f in range(16):
 u=machine();run(u,0x2360);run(u,0x2944);w(u,0xffff2606,f);run(u,0x4882);run(u,0x685e)
 data=bytes(u.mem_read(0xffff305a,4000));Path(f'atlas/floor_{f:02d}.bin').write_bytes(data)
 addr=int.from_bytes(r[0x136ee+f*4:0x136f2+f*4],'big');p=addr;spawns=[]
 while int.from_bytes(r[p:p+2],'big',signed=True)>=0:
  x,z,init,extra=__import__('struct').unpack('>HHII',r[p:p+12]);spawns.append(dict(x=x//256,y=49-z//256,world_x=x,world_z=z,init=f'{init:04X}',extra=f'{extra:04X}'));p+=12
  assert len(spawns)<100
 run(u,0x3fb2)
 objects=[]
 for a in range(0xffff4468,0xffff4f7e,86):
  typ=rd(u,a+2)
  if typ:objects.append(dict(x=rd(u,a+8)//256,y=49-rd(u,a+12)//256,type=f'{typ:04X}',sprite=rd(u,a+32),callback=f'{rd(u,a+58,4):04X}',damage=f'{rd(u,a+74,4):04X}'))
 pts=[]
 for p in range(0xffff2744,0xffff2794,4):
  z=rd(u,p);x=rd(u,p+2)
  if z==x==0:continue
  pts.append(dict(x=z//256,y=49-x//256))
 lev=dict(id=f,name=names[f],code_gs5=codes[f*2:f*2+2].hex(),cells=list(data),scripted=spawns,objects=objects,spawn_points=pts)
 levels.append(lev);print(f,names[f],Counter(v&63 for v in data),'scripted',len(spawns),'objects',objects,'respawn',pts)
Path('atlas/data.json').write_text(json.dumps(levels,ensure_ascii=False))
print('constructors',[(i,hex(int.from_bytes(r[0x6588+i*4:0x658c+i*4],'big'))) for i in range(37)])
