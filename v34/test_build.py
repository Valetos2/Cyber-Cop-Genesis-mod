from pathlib import Path
import hashlib,sys,struct
sys.path.insert(0,'v34')
from build_v34 import build
source=Path('upload/Cyber-Cop_(W)_[c][!].bin').read_bytes();corp=Path('upload/Corporation_(E)_[c][!].bin').read_bytes();rom,labels=build(source,corp)
assert rom==Path('v34/Cyber-Cop_v34.bin').read_bytes()
assert int.from_bytes(rom[0x18e:0x190],'big')==sum(int.from_bytes(rom[i:i+2],'big') for i in range(0x200,len(rom),2))&65535
p=Path('v34/Cyber-Cop_v34.ips').read_bytes();assert p[:5]==b'PATCH';i=5;out=bytearray(source)
while p[i:i+3]!=b'EOF':
 a=int.from_bytes(p[i:i+3],'big');n=int.from_bytes(p[i+3:i+5],'big');i+=5
 if n:b=p[i:i+n];i+=n
 else:n=int.from_bytes(p[i:i+2],'big');b=p[i+2:i+3]*n;i+=3
 if len(out)<a+n:out.extend(bytes(a+n-len(out)))
 out[a:a+n]=b
assert bytes(out)==rom
print('PASS reproducible build, Genesis checksum, IPS expansion and exact ROM match:',hashlib.sha256(rom).hexdigest())
