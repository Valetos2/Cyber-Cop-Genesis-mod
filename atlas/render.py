from pathlib import Path
import json,csv,zipfile,html
from PIL import Image,ImageDraw,ImageFont
D=Path('atlas');levels=json.loads((D/'data.json').read_text());rom=Path('v25/Cyber-Cop_v25.bin').read_bytes()
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';f=ImageFont.truetype(font,15);small=ImageFont.truetype(font,12);large=ImageFont.truetype(font,26)
meta={0:('Пол / пустая клетка','', '#15212c'),1:('Стена','#','#526474'),3:('Клетка дверного проёма','·','#6e5239'),4:('Дверь','D','#e9a347'),9:('Камера','09','#a57bed'),10:('Лазерный детектор','0A','#a57bed'),11:('Детектор / луч','L','#f1dc69'),12:('Зона лифта / перехода','E','#3d7d85'),14:('Сценарная клетка 0E','0E','#aa80a8'),15:('Растение','0F','#a57bed'),16:('Сигнальная лампа','!','#ee6383'),17:('Голографический проектор','11','#a57bed'),19:('Кресло','13','#a57bed'),20:('Стол','14','#a57bed'),21:('Бочка','15','#a57bed'),22:('Капсула с объектом','16','#a57bed'),23:('Пустая капсула','17','#a57bed'),24:('Барьер / тревожная зона','B','#e5d76b'),25:('Ящик','19','#a57bed'),26:('Колонна','1A','#a57bed'),27:('Триггер / переход 1B','T','#aa80a8'),31:('Шлюз: код 9831','A','#f6ab69'),32:('Fuse Box','F','#fae168'),33:('Терминал (window)','T','#5fc8d0'),34:('Кодовый замок','K','#f6ab69'),35:('Пульт внутри лифта','I','#5fc8d0'),36:('Вызов лифта','C','#5fc8d0')}
for t in range(37,64):
 item=rom[0x9ee2+t-31];name=rom[0x103f3+item*12:0x103f3+item*12+11].decode('ascii').strip();meta[t]=(name,f'{t:02X}','#80d3a8')
for l in levels:
 l['legend']={str(t):dict(name=meta[t][0],symbol=meta[t][1],color=meta[t][2]) for t in sorted(set(v&63 for v in l['cells']))}
 l['locks']=[dict(x=i%80,y=i//80,code=l['code_gs5'] if v&63==34 else '9831',kind='session' if v&63==34 else 'fixed') for i,v in enumerate(l['cells']) if v&63 in [31,34]]
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
  px=ox+o['x']*cell;py=oy+o['y']*cell;d.ellipse((px+1,py+1,px+22,py+22),fill='#ef546b',outline='white');d.text((px+cell/2,py+cell/2),o['type'][-2:],font=small,fill='white',anchor='mm')
 for o in l['spawn_points']:
  px=ox+o['x']*cell;py=oy+o['y']*cell;d.rectangle((px+2,py+2,px+21,py+21),outline='#ffe45c',width=2);d.text((px+cell/2,py+cell/2),'S',font=small,fill='#ffe45c',anchor='mm')
 x=2000;y=100;d.text((x,y),'ОБОЗНАЧЕНИЯ',font=large,fill='white');y+=42
 for t in sorted(set(v&63 for v in l['cells'])):
  name,sym,color=meta[t];d.rectangle((x,y,x+18,y+18),fill=color);d.text((x+27,y),f'{t:02X}  {name}',font=f,fill='#d8e0ed');y+=24
 d.text((x,y+9),'● XX — враг: младший байт типа',font=f,fill='#ff8a9a');d.text((x,y+33),'S — точка повторного появления',font=f,fill='#ffe45c');y+=76
 if l['locks']:
  d.text((x,y),'КОДЫ / КООРДИНАТЫ',font=f,fill='white');y+=28
  for k in l['locks']:
   d.text((x,y),f"({k['x']:02},{k['y']:02})  {k['code']}"+('  [табл.]' if k['kind']=='session' else '  [фикс.]'),font=f,fill='#ffd9a6');y+=22
 d.text((ox,1320),'Коды: оригинал / v25. В новой игре v26 обычные замки перемешиваются; шлюз 9831 неизменен.',font=f,fill='#ffce86')
 d.text((ox,1345),'Неопознанные декорации подписаны точным ID; враги показаны на исходных позициях, а не из текущего сейва.',font=f,fill='#9db0c5')
 assert y<H-25,(l['id'],y)
 im.save(D/'png'/f"{l['id']:02}_{l['name']}.png")
with (D/'cells.csv').open('w',encoding='utf-8-sig',newline='') as fp:
 w=csv.writer(fp);w.writerow(['floor_id','floor','x','y','raw_hex','tile_hex','label','code_gs5_or_fixed']);w.writerows(rows)
(D/'data.json').write_text(json.dumps(levels,ensure_ascii=False,separators=(',',':')))
page='''<!doctype html><html lang="ru"><meta charset="utf-8"><title>Cyber-Cop — атлас 16 уровней</title><style>
*{box-sizing:border-box}body{margin:0;background:#0b121a;color:#e6edf6;font:15px system-ui}header{padding:18px 24px;border-bottom:1px solid #334455}h1{font-size:24px;margin:0 0 12px}select,button{background:#243549;color:white;padding:7px;border:1px solid #60768f;border-radius:5px}label{margin-left:16px}main{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:18px;padding:18px}#viewport{overflow:auto;max-height:80vh;border:1px solid #334455}canvas{display:block;image-rendering:pixelated}aside{max-height:80vh;overflow:auto}h2{font-size:18px}.entry{display:flex;gap:9px;padding:4px 0}.sw{width:16px;height:16px;flex:none}#info{background:#233549;padding:12px;height:180px;overflow:auto}#enemyPreview{height:220px;display:flex;align-items:center;justify-content:center}#enemyPreview img{height:196px;image-rendering:pixelated}.entry{cursor:pointer}.levelstep{display:inline-flex;vertical-align:middle;flex-direction:column}.levelstep button{padding:0 9px}small{color:#aebed0}.warn{color:#ffc77d;margin:10px 0}button{cursor:pointer}ul{padding-left:20px}
</style><header><h1>CYBER-COP · 16 уровней</h1><select id="floor"></select> <span class="levelstep"><button id="prevLevel" aria-label="Предыдущий этаж">▴</button><button id="nextLevel" aria-label="Следующий этаж">▾</button></span> <button id="minus">−</button> <button id="plus">+</button><label><input type="checkbox" id="enemies" checked>Исходные враги</label><label><input type="checkbox" id="spawns" checked>Точки появления</label><label><input type="checkbox" id="scripts">Сценарные точки</label><div class="warn">Коды обычных замков здесь — для оригинала / v25. В новой игре v26 они перемешиваются. Шлюзы: фиксированный 9831.</div><small>Щелчок закрепляет клетку и её описание. Щелчок по легенде выделяет все объекты этого типа. Колесо прокручивает карту; +/− меняют масштаб. Файлы PNG и CSV входят в архив.</small></header><main><div id="viewport"><canvas id="map"></canvas></div><aside><div id="info">Выберите клетку</div><div id="enemyPreview"></div><h2>Легенда этажа</h2><div id="legend"></div><h2>Замки</h2><div id="locks"></div><h2>Группы врагов</h2><small>8004, 8006, 801C — группа, реагирующая на Disruptor; 8119, 811A, 811B — группа, чьё движение зависит от света. 801C восстанавливается после обычного урона. Точные типы и callbacks сохранены в JSON.</small></aside></main><script>
const data=DATA;const $=id=>document.getElementById(id);let scale=18;const ctx=$('map').getContext('2d');data.forEach((l,i)=>$('floor').add(new Option(l.name+' / ID '+i,i)));function current(){return data[+$('floor').value]}
function draw(){const l=current(),c=$('map');c.width=80*scale;c.height=50*scale;for(let i=0;i<4000;i++){let t=l.cells[i]&63,m=l.legend[t],x=i%80*scale,y=Math.floor(i/80)*scale;ctx.fillStyle=m.color;ctx.fillRect(x,y,scale,scale);ctx.strokeStyle='#273747';ctx.strokeRect(x,y,scale,scale);if(scale>=18&&m.symbol&&t!=1){ctx.fillStyle='#07101a';ctx.font=Math.floor(scale*.52)+'px monospace';ctx.textAlign='center';ctx.fillText(m.symbol,x+scale/2,y+scale*.72);ctx.textAlign='left'}}
function marker(p,text,color,circle){let x=(p.x+.5)*scale,y=(p.y+.5)*scale;ctx.strokeStyle=color;ctx.lineWidth=2;if(circle){ctx.fillStyle=color;ctx.beginPath();ctx.arc(x,y,scale*.43,0,7);ctx.fill();ctx.fillStyle='white'}else{ctx.strokeRect(x-scale*.4,y-scale*.4,scale*.8,scale*.8);ctx.fillStyle=color}ctx.font=Math.floor(scale*.52)+'px monospace';ctx.textAlign='center';ctx.fillText(text,x,y+scale*.19);ctx.textAlign='left'}
if($('scripts').checked)l.scripted.forEach(p=>marker(p,'?', '#ab90e7',false));if($('enemies').checked)l.objects.forEach(p=>marker(p,p.type.slice(-2),'#ed506c',true));if($('spawns').checked)l.spawn_points.forEach(p=>marker(p,'S','#ffe45c',false));$('legend').innerHTML=Object.entries(l.legend).map(([id,m])=>'<div class="entry"><span class="sw" style="background:'+m.color+'"></span><span>'+Number(id).toString(16).toUpperCase().padStart(2,'0')+' · '+m.name+'</span></div>').join('');$('locks').innerHTML=l.locks.map(k=>'<p>('+k.x+', '+k.y+') → <b>'+k.code+'</b> '+(k.kind==='fixed'?'фиксированный':'[табл.]')+'</p>').join('')||'Нет кодовых панелей';}
function inspect(ev){let b=$('map').getBoundingClientRect(),x=Math.floor((ev.clientX-b.left)/scale),y=Math.floor((ev.clientY-b.top)/scale);if(x<0||x>=80||y<0||y>=50)return;let l=current(),raw=l.cells[y*80+x],m=l.legend[raw&63],os=l.objects.filter(o=>o.x===x&&o.y===y),ss=l.scripted.filter(o=>o.x===x&&o.y===y),ks=l.locks.filter(o=>o.x===x&&o.y===y);$('info').innerHTML='<b>X '+x+', Y '+y+'</b><br>'+m.name+'<br>Байт: $'+raw.toString(16).toUpperCase().padStart(2,'0')+' · мировой Z: '+(49-y)+os.map(o=>'<br>Враг $'+o.type+' · спрайт '+o.sprite).join('')+ss.map(o=>'<br>Сценарий $'+o.init+' / $'+o.extra).join('')+ks.map(k=>'<br>Код <b>'+k.code+'</b>').join('');}
$('map').onmousemove=inspect;$('map').onclick=inspect;['floor','enemies','spawns','scripts'].forEach(id=>$(id).onchange=draw);$('plus').onclick=()=>{scale=Math.min(40,scale+4);draw()};$('minus').onclick=()=>{scale=Math.max(10,scale-4);draw()};draw();

let chosen=null,highlightType=null;const originalDraw=draw,originalInspect=inspect;
function outline(x,y,color){ctx.strokeStyle=color;ctx.lineWidth=2;ctx.strokeRect(x*scale+1,y*scale+1,scale-2,scale-2)}
draw=function(){originalDraw();let l=current();if(highlightType!==null)l.cells.forEach((v,i)=>{if((v&63)===highlightType)outline(i%80,Math.floor(i/80),'#ffff00')});if(chosen)outline(chosen.x,chosen.y,'#ffffff');document.querySelectorAll('#legend .entry').forEach((el,i)=>{let t=Number(Object.keys(l.legend)[i]);el.onclick=e=>{e.stopPropagation();if(t===0||t===1)return;highlightType=t;draw()}});$('prevLevel').disabled=+$('floor').value===0;$('nextLevel').disabled=+$('floor').value===data.length-1;};
function resetSelection(){chosen=null;highlightType=null;$('info').textContent='Выберите клетку';$('enemyPreview').innerHTML='';draw()}
function choose(ev){let b=$('map').getBoundingClientRect(),x=Math.floor((ev.clientX-b.left)/scale),y=Math.floor((ev.clientY-b.top)/scale);if(x<0||x>=80||y<0||y>=50)return;chosen={x,y};originalInspect(ev);let o=current().objects.find(o=>o.x===x&&o.y===y);$('enemyPreview').innerHTML=o&&enemyImages[o.type]?'<img alt="Исходный кадр противника" src="'+enemyImages[o.type]+'">':'';draw();}
$('map').onmousemove=ev=>{if(!chosen)originalInspect(ev)};$('map').onclick=ev=>{ev.stopPropagation();choose(ev)};
$('floor').onchange=resetSelection;for(let id of ['enemies','spawns','scripts'])$(id).onchange=draw;
$('prevLevel').onclick=()=>{if(+$('floor').value>0){$('floor').value=+$('floor').value-1;resetSelection()}};
$('nextLevel').onclick=()=>{if(+$('floor').value<data.length-1){$('floor').value=+$('floor').value+1;resetSelection()}};
document.addEventListener('click',ev=>{if(ev.target.closest('button,select,input,label,#legend,#info,#enemyPreview'))return;if(ev.target!==$('map'))resetSelection()});
const enemyImages=ENEMY_IMAGES;draw();
</script></html>'''.replace('DATA',json.dumps(levels,ensure_ascii=False,separators=(',',':')))
page=page.replace('ENEMY_IMAGES',Path('atlas/enemy_images.json').read_text())
(D/'Cyber-Cop_Atlas.html').write_text(page)
print('16 PNG, offline atlas, 64000 CSV cells and JSON exported')
