exec(open('mission_port36/guards.py').read().split('for file in Path')[0])
d=next(Path('next/dos').rglob('CORPRTNC.DAT')).read_bytes()
p=variants[(False,True)]
for x in range(32):
 s=p[x*40:x*40+20];off=d.find(s) if len(set(s))>4 else -1
 if off>=0:print(x,hex(off))
