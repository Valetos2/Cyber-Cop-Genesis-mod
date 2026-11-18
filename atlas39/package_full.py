"""Export every embedded preview alongside offline HTML; never publish output assets."""
from pathlib import Path
import base64,json,shutil,zipfile
D=Path('atlas39');out=Path('atlas41_full');out.mkdir(exist_ok=True)
for n in ['Cyber-Cop_Atlas.html','Cyber-Cop_Atlas_en.html','data.json','cells.csv','README_RU.md']:shutil.copy2(D/n,out/n)
banks=json.loads((D/'images.json').read_text());count=0

def export(node,path):
 global count
 if isinstance(node,dict):
  for k,v in node.items():export(v,path/str(k))
 elif isinstance(node,list):
  for k,v in enumerate(node):export(v,path/str(k))
 elif isinstance(node,str) and node.startswith('data:image/png;base64,'):
  dest=path.with_suffix('.png');dest.parent.mkdir(parents=True,exist_ok=True);raw=base64.b64decode(node.split(',',1)[1]);dest.write_bytes(raw);assert dest.read_bytes()==raw;count+=1
for i,b in enumerate(banks):export(b,out/'sprites'/('mission' if i else 'original'))
# Historical scenes path, with campaign-specific images retained in both banks.
export(banks[0]['scenes'],out/'sprites'/'scenes')
for scene in ('2','11'):
 raw=base64.b64decode(banks[0]['scenes'][scene].split(',',1)[1])
 for bank in (out/'sprites/scenes',out/'sprites/original/scenes',out/'sprites/mission/scenes'):
  assert (bank/scene).with_suffix('.png').read_bytes()==raw
with zipfile.ZipFile('Cyber-Cop_Atlas41_full.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(out.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(out))
print('PASS full export:',count,'PNG files; lamp and normal-palette laser match embedded scenes')
