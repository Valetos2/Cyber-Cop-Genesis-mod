from pathlib import Path
import json,csv,zipfile,html
from PIL import Image,ImageDraw,ImageFont
D=Path('atlas35');levels=json.loads((D/'data.json').read_text());rom=Path('v30/Cyber-Cop_v30.bin').read_bytes()
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';f=ImageFont.truetype(font,15);small=ImageFont.truetype(font,12);large=ImageFont.truetype(font,26)
meta={0:('Пол / пустая клетка','', '#15212c'),1:('Стена','#','#526474'),3:('Клетка дверного проёма','·','#6e5239'),4:('Дверь','D','#e9a347'),9:('Камера','09','#ee6383'),10:('Лазерный детектор','0A','#a57bed'),11:('Детектор / луч','L','#f1dc69'),12:('Зона лифта / перехода','E','#3d7d85'),14:('Точка появления · сценарная клетка 0E','S','#ffe45c'),15:('Растение','0F','#a57bed'),16:('Сигнальная лампа','!','#ee6383'),17:('Голографический проектор','11','#a57bed'),19:('Кресло','13','#a57bed'),20:('Стол','14','#a57bed'),21:('Бочка','15','#a57bed'),22:('Капсула с объектом','16','#a57bed'),23:('Пустая капсула','17','#a57bed'),24:('Барьер / тревожная зона','B','#e5d76b'),25:('Ящик','19','#a57bed'),26:('Колонна','1A','#a57bed'),27:('Триггер / переход 1B','T','#aa80a8'),31:('Шлюз: код 9831','A','#f6ab69'),32:('Fuse Box','F','#fae168'),33:('Терминал (window)','T','#5fc8d0'),34:('Кодовый замок','K','#f6ab69'),35:('Пульт внутри лифта','I','#5fc8d0'),36:('Вызов лифта','C','#5fc8d0')}
for t in range(37,64):
 item=rom[0x9ee2+t-31];name=rom[0x103f3+item*12:0x103f3+item*12+11].decode('ascii').strip();meta[t]=(name,f'{t:02X}','#80d3a8')
for l in levels:
 l['item_ids']={str(t):rom[0x9ee2+t-31] for t in range(37,64)}
 l['legend']={str(t):dict(name=meta[t][0],symbol=meta[t][1],color=meta[t][2]) for t in sorted(set(v&63 for v in l['cells']))}
 l['locks']=[dict(x=i%80,y=i//80,code=l['code_gs5'] if v&63==34 else '9831',kind='session' if v&63==34 else 'fixed') for i,v in enumerate(l['cells']) if v&63 in [31,34]]
arrivals={0:[(6,6)],6:[(3,24),(30,5)],7:[(18,46),(71,46)]}
cell=24;ox=42;oy=100;W=2460;H=1390
(D/'png').mkdir(exist_ok=True)
rows=[]
for l in levels:
 im=Image.new('RGB',(W,H),'#0b121a');d=ImageDraw.Draw(im)
 d.text((ox,18),f"CYBER-COP / {l['name']} — ID {l['id']:02d}",font=large,fill='white');d.text((ox,57),'Начальное состояние ROM · X 0–79 слева направо · Y 0–49 сверху вниз',font=f,fill='#9db0c5')
 for x in range(80):
  if x%5==0:d.text((ox+x*cell,oy-24),str(x),font=small,fill='#b1bdca')
 for y in range(50):
  if y%5==0:d.text((8,oy+y*cell),str(y),font=small,fill='#b1bdca')
 for i,v in enumerate(l['cells']):
  x=i%80;y=i//80;t=v&63;name,sym,color=meta[t];px=ox+x*cell;py=oy+y*cell
  d.rectangle((px,py,px+cell-1,py+cell-1),fill=color,outline='#233343')
  if sym and t!=1:d.text((px+cell/2,py+cell/2),sym,font=small,fill='#08131b',anchor='mm')
  rows.append([l['id'],l['name'],x,y,f'{v:02X}',f'{t:02X}',name, l['code_gs5'] if t==34 else '9831' if t==31 else ''])
 for o in l['objects']:
  px=ox+o['x']*cell;py=oy+o['y']*cell;d.ellipse((px+1,py+1,px+22,py+22),fill='#ef546b',outline='white');d.text((px+cell/2,py+cell/2),'●',font=small,fill='white',anchor='mm')
 if l['id']==11:
  px=ox+42*cell;py=oy+14*cell;d.rectangle((px+1,py+1,px+22,py+22),outline='#65e6ff',width=3);d.text((px+12,py+12),'R',font=small,fill='#65e6ff',anchor='mm')
 for ax,ay in arrivals.get(l['id'],[]):
  px=ox+ax*cell;py=oy+ay*cell;d.rectangle((px+1,py+1,px+22,py+22),outline='#65e6ff',width=3);d.text((px+12,py+12),'P',font=small,fill='#65e6ff',anchor='mm')
 x=2000;y=100;d.text((x,y),'ОБОЗНАЧЕНИЯ',font=large,fill='white');y+=42
 if l['objects']:d.text((x,y),'● — исходный враг',font=f,fill='#ff8a9a');y+=24
 if l['id'] in arrivals:d.text((x,y),'P — появление / ориентир прибытия',font=f,fill='#65e6ff');y+=24
 if l['id']==11:d.text((x,y),'R — спасение с Bomb (42,14)',font=f,fill='#65e6ff');y+=24
 for t in sorted(set(v&63 for v in l['cells'])):
  name,sym,color=meta[t];d.rectangle((x,y,x+18,y+18),fill=color);d.text((x+27,y),f'{t:02X}  {name}',font=f,fill='#d8e0ed');y+=24
 d.text((x,y+33),'S — точка повторного появления',font=f,fill='#ffe45c');y+=76
 if l['locks']:
  d.text((x,y),'КОДЫ / КООРДИНАТЫ',font=f,fill='white');y+=28
  for k in l['locks']:
   d.text((x,y),f"({k['x']:02},{k['y']:02})  {k['code']}"+('  [случ. v26+]'  if k['kind']=='session' else '  [фикс.]'),font=f,fill='#ffd9a6');y+=22
 d.text((ox,1320),'Коды: оригинал / v25. В новой игре v26 обычные замки перемешиваются; шлюз 9831 неизменен.',font=f,fill='#ffce86')
 d.text((ox,1345),'Атлас: GPT-6 Astra по запросу Valentin (Valet2) Kozin · 2026. Враги показаны на исходных позициях.',font=f,fill='#9db0c5')
 assert y<H-25,(l['id'],y)
 im.save(D/'png'/f"{l['id']:02}_{l['name']}.png")
with (D/'cells.csv').open('w',encoding='utf-8-sig',newline='') as fp:
 w=csv.writer(fp);w.writerow(['floor_id','floor','x','y','raw_hex','tile_hex','label','code_gs5_or_fixed']);w.writerows(rows)
(D/'data.json').write_text(json.dumps(levels,ensure_ascii=False,separators=(',',':')))

page=Path('atlas35/template.html').read_text().replace('__DATA__',json.dumps(levels,ensure_ascii=False,separators=(',',':'))).replace('__IMAGES__',Path('atlas35/images.json').read_text())
(D/'Cyber-Cop_Atlas.html').write_text(page)
