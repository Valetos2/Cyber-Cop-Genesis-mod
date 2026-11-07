from pathlib import Path
import json,struct
R=Path('v36/Cyber-Cop_v36_WORK_IN_PROGRESS.bin').read_bytes();S=json.loads(Path('v36/symbols.json').read_text())
from scan_research import sheet
orig,_,_=sheet('d2',20);mission,_,_=sheet('mission',11)
diff=[]
for f in range(15):
 a=[orig[f//4*48+y][f%4*80+x] for y in range(48) for x in range(80)]
 b=[mission[f//4*48+y][f%4*80+x] for y in range(48) for x in range(80)]
 diff.append(sum(x!=y for x,y in zip(a,b)))
assert all(0<n<25 for n in diff[:5]) and all(n>1000 for n in diff[5:10]) and diff[10:]==[0]*5,diff
print('PASS Scanman: robot replaces middle hologram; hand has minor pixel differences; text identical')
exec(open('v36/test_core.py').read().split('levels=json')[0])
u=machine();w(u,S['CAMP'],1);w(u,0xffff026c,0x101);run(u,0x685e);run(u,0x3fb2)
live=[(rd(u,a+2),rd(u,a+8),rd(u,a+12)) for a in range(0xffff4468,0xffff4f7e,0x56) if rd(u,a+2)]
assert live==[(0x801d,0x1980,0xe80)],live
print('PASS lab02 robot behind code door')
