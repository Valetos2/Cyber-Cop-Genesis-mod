from pathlib import Path
import runpy,json,base64
runpy.run_path('atlas37/sprites.py',run_name='__main__')
runpy.run_path('atlas37/render_scenes.py',run_name='__main__')
p=Path('atlas37/images.json');d=json.loads(p.read_text())
d['scenes']={str(k):'data:image/png;base64,'+base64.b64encode(Path('atlas37/'+n+'.png').read_bytes()).decode() for k,n in [(4,'door'),(34,'locked_door'),(36,'elevator_door'),(24,'alarm_floor'),(11,'laser_beam')]}
p.write_text(json.dumps(d))
for group in ['enemies','objects']:
 for floor,items in d[group].items():
  p=Path('atlas37/sprites')/('floor_'+floor.zfill(2))/group;p.mkdir(parents=True,exist_ok=True)
  for name,data in items.items():(p/(name+'.png')).write_bytes(base64.b64decode(data.split(',')[1]))
for group in ['items','scenes']:
 p=Path('atlas37/sprites')/group;p.mkdir(parents=True,exist_ok=True)
 for name,data in d[group].items():(p/(name.zfill(2)+'.png')).write_bytes(base64.b64decode(data.split(',')[1]))

runpy.run_path('atlas37/render_panels.py',run_name='__main__')
p=Path('atlas37/images.json');d=json.loads(p.read_text());d['panels']=json.loads(Path('atlas37/panels.json').read_text());p.write_text(json.dumps(d))
