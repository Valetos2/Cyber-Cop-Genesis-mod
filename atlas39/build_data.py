"""Build private atlas data/images from locally supplied ROM assets."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
from PIL import Image
import copy,base64,io,struct,sys
out=Path('atlas39');out.mkdir(exist_ok=True)
def pngdata(im):
 b=io.BytesIO();im.save(b,format='PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
def pal(a):return [tuple(round(((int.from_bytes(R[a+i*2:a+i*2+2],'big')>>s)&14)*255/14) for s in (0,4,8)) for i in range(16)]
original=json.loads(Path('atlas37/data.json').read_text());meta={k:v for l in original for k,v in l['legend'].items()}
meta.update({'2':{'name':'Светильник','symbol':'','color':'#788474'},'28':{'name':'Бочка Mission (неразрушаемая)','symbol':'1C','color':'#a57bed'},'29':{'name':'Синий стул Mission','symbol':'1D','color':'#a57bed'},'30':{'name':'Зелёный стул Mission','symbol':'1E','color':'#a57bed'}})
meta['9']=dict(meta['9'],color='#d93949',symbol='');meta['16']=dict(meta['16'],color='#d98430',symbol='')
ctor={}
for addr in [0x4038,0x4144,0x432e,0x4438]:
 u=machine();run(u,0x685e);u.reg_write(UC_M68K_REG_D0,0x1080);u.reg_write(UC_M68K_REG_D2,0x2080);run(u,addr);ctor[addr]=f'{rd(u,u.reg_read(UC_M68K_REG_A0)+2):04X}'
spawnmap={0x3fde:ctor[0x4038],0x40de:ctor[0x4144],0x42c8:ctor[0x432e],0x43d8:ctor[0x4438],S['robot_spawn36']:'801D',0xb426:None}
banks=[]
for camp in [0,1]:
 levels=[]
 for f in range(16):
  u=machine();w(u,S['CAMP'],camp);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,f);run(u,0x4882);run(u,0x685e);run(u,0x3fb2)
  l=copy.deepcopy(original[f]);l['cells']=list(u.mem_read(0xffff305a,4000));l['campaign']=camp;l['logical_id']=f+camp*16
  l['objects']=[]
  for a in range(0xffff4468,0xffff4f7e,0x56):
   if rd(u,a+2):l['objects'].append(dict(x=rd(u,a+8)//256,y=49-rd(u,a+12)//256,type=f'{rd(u,a+2):04X}',sprite=rd(u,a+0x20)))
  if camp:
   l['scripted']=[];p=S['mission_spawns']+f*16
   l['respawn_interval'],l['active_limit'],*funcs=struct.unpack_from('>HHIII',R,p);l['respawn_types']=[spawnmap[x] for x in funcs]
  l['spawn_points']=[dict(x=i%80,y=i//80) for i,v in enumerate(l['cells']) if v&63==14]
  l['legend']={str(t):copy.deepcopy(meta[str(t)]) for t in sorted({v&63 for v in l['cells']})}
  if '31' in l['legend']:l['legend']['31']['name']='Шлюз: код '+('8652' if camp else '9831')
  l['locks']=[dict(x=i%80,y=i//80,code=l['code_gs5'] if v&63==34 else '8652' if camp else '9831',kind='session' if v&63==34 else 'fixed') for i,v in enumerate(l['cells']) if v&63 in [31,34]]
  levels.append(l)
 banks.append(levels)
# Rare pickups: explicit requested categories, plus <=3 occurrences per campaign.
from collections import Counter
for levels in banks:
 counts=Counter(l['item_ids'][str(v&63)] for l in levels for v in l['cells'] if v&63>=37)
 for l in levels:
  l['rare_items']=sorted({i for i,n in counts.items() if n<=3}|{8,12,15,16})
(out/'data.json').write_text(json.dumps(banks,ensure_ascii=False,separators=(',',':')))
images=json.loads(Path('atlas37/images.json').read_text());imagebanks=[images,copy.deepcopy(images)]
# New Holo names use the relocated item bank.
for item in [25,26,27]:
 off=int.from_bytes(R[0xa052+item*4:0xa054+item*4],'big');im=Image.new('RGBA',(32,32));p=pal(0x2870)
 for y in range(32):
  for x in range(32):
   tile=int.from_bytes(R[0x3f520+off+y//8*128+x//8*2:0x3f522+off+y//8*128+x//8*2],'big')&2047
   a=S['item_graphics36c']+2+(tile-40)*32+y%8*4+x%8//2;n=R[a]>>(0 if x&1 else 4)&15;im.putpixel((x,y),p[n]+(255 if n else 0,))
 for bank in imagebanks:bank['items'][str(item)]=pngdata(im)
# Reuse known native sprite layouts, recoloured with each Mission floor palette.
sys.path.insert(0,'atlas37');import sprites
sprites.R=R
# Existing native indices retain their original addresses. Mission indices use
# the expanded table and explicit padded stride; avoid inferring last size.
specs=json.loads(Path('v36/sprites.json').read_text())
def newpart(name,p):
 sp=specs[name];x,y,w0,h=sp['crop'];stride=100 if name.startswith('robot_') else h+2;im=Image.new('RGBA',(w0,h))
 for yy in range(h):
  for xx in range(w0):
   n=R[sp['address']+xx//2*stride+yy]>>(0 if xx&1 else 4)&15;im.putpixel((xx,yy),p[n]+(255 if n else 0,))
 return im
for f in range(16):
 p=pal(S['mission_palette_'+str(f)])
 imagebanks[1]['enemies'][str(f)]={sp[0]:pngdata(sprites.enemy(sp,4 if sp[0]!='811B' else 0,p)) for sp in sprites.specs}
 imagebanks[1]['enemies'][str(f)]['801D']=pngdata(newpart('robot_walk_0',p))
 imagebanks[1]['objects'][str(f)]={str(t):pngdata(sprites.part(idx,w0,h,p)) for t,(idx,w0,h) in sprites.objects.items()}
 for t,name in [(28,'barrel'),(29,'stool_blue'),(30,'stool_green')]:imagebanks[1]['objects'][str(f)][str(t)]=pngdata(newpart(name,p))
# Native world preview: distant wall and a light six cells ahead, like the
# existing alarm-floor preview. No synthetic object art.
ns={};source=Path('v36/render_scene.py').read_text().split('for raw,name,robot in [')[0]
source=source.replace('(49-26)*80','(49-40)*80').replace('(49-24)*80','(49-26)*80')
exec(source,ns);im=ns['render'](0x82,'lamp_atlas03');(out/'scenes').mkdir(exist_ok=True);im.save(out/'scenes/2.png')
for bank in imagebanks:bank['scenes']['2']=pngdata(im)
(out/'images.json').write_text(json.dumps(imagebanks,separators=(',',':')))
print('Built32 ROM maps, actor lists, lamp scene, Mission sprites and Holo icons')
