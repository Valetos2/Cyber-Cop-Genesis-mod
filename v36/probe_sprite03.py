exec(open('v36/render_scene.py').read().split('for raw,name,robot in [')[0].split('def render(')[0])
source=open('v36/render_scene.py').read().split('for raw,name,robot in [')[0]
source=source[source.index('def render('):]
source=source.replace('def render(raw,name,robot=False):','def render(raw,name,distance):').replace('if robot:','if False:').replace('20*256+128','24*256+128-distance')
source=source.replace('for a in [0x3b46,','reads=[]\n spec=json.loads(Path("v36/sprites.json").read_text())[name];base=spec["address"];h=spec["crop"][3];stride=h+2\n u.hook_add(UC_HOOK_MEM_READ,lambda uc,access,address,size,value,data: reads.append((address-base)%stride) if base<=address<base+16*stride and (address-base)%stride>=h else None)\n for a in [0x3b46,')
source=source[:source.index(' b=bytes(u.mem_read')]+ ' return reads\n'
exec(source)
for raw,name in [(0x9c,'barrel'),(0x9d,'stool_blue'),(0x9e,'stool_green')]:
 cases=[]
 for dist in range(300,1801,50):
  reads=render(raw,name,dist)
  if reads:cases.append((dist,sorted(set(reads))))
 print(name,'padding samples',cases)
