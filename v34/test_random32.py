exec(open('v34/common.py').read())
from collections import Counter
codes=Counter()
for ticks in range(100):
 u=machine();run(u,0x2360);w(u,0xffff2712,0,1);w(u,0xffff2798,ticks);original=sorted(rd(u,0xffff2fea+i*2) for i in range(16));run(u,L['seed26'],0x1f82);run(u,0x33b6)
 assert sorted(rd(u,0xffff2fea+i*2) for i in range(16))==original
 code=rd(u,0xffff2fec);codes[f'{code:04X}']+=1
 assert len(set(f'{code:04X}'))==4
assert len(codes)>1
print('PASS original 8-swap shuffle preserves table and distinct digits; 4F across seeds0..99:',dict(codes))
