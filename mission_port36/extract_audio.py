from pathlib import Path
import struct,wave,json,hashlib
out=Path('mission_port36/audio');out.mkdir(exist_ok=True)
b=Path('amiga3/mission.bin').read_bytes();d=Path('amiga3/d2.bin').read_bytes()
rows=[]
for id,name in [(5,'robot_steps_shared'),(12,'shared_sample_normal_pitch'),(19,'robot_attack_loop_unit')]:
 addr,n,period=struct.unpack_from('>IHH',b,0x10bb8+id*8)
 raw=b[addr:addr+n];assert len(raw)==n
 # $791A adds $80 before Paula sees this bank: disk representation is WAV unsigned PCM8.
 rate=round(3546895/period)
 for loop in [False,True] if id==19 else [False]:
  samples=raw*(max(1,round(rate/n)) if loop else 1)
  filename=name+('_one_second_loop' if loop else '')+'.wav'
  with wave.open(str(out/filename),'wb') as f:f.setnchannels(1);f.setsampwidth(1);f.setframerate(rate);f.writeframes(samples)
 rows.append(dict(id=id,name=name,address=hex(addr),bytes=n,period=period,pal_rate=rate,sha256=hashlib.sha256(raw).hexdigest(),occurrences_original=[hex(i) for i in range(len(d)) if d.startswith(raw,i)]))
assert b[0x32078:0x32138]==b[struct.unpack_from('>I',b,0x10bb8+19*8)[0]:struct.unpack_from('>I',b,0x10bb8+19*8)[0]+192]
(out/'samples.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
