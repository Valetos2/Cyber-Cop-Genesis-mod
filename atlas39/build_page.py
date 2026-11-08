from pathlib import Path
import json,re
D=Path('atlas39');s=Path('atlas37/template.html').read_text()
s=s.replace('CYBER-COP · 16 уровней','CYBER-COP · Original + Mission · 32 уровня')
s=s.replace('</span> <button id="minus"','</span> <button id="originalCampaign" aria-pressed="true">Original game</button> <button id="missionCampaign" aria-pressed="false">Mission Disk</button> <button id="minus"',1)
s=re.sub(r'<div class="warn">Коды обычных замков:.*?</div>','<div class="warn" id="codeNote"></div>',s,count=1)
s=re.sub(r'<div class="warn">Доступ \(каждый следующий включает предыдущие\):.*?</div>','<div class="warn" id="accessInfo"></div>',s,count=1)
s=s.replace('Свет и газ — состояния этажа, а не самостоятельные клетки.','Светильники отмечены контуром клетки. Камеры — красные круги, аварийные лампы — оранжевые. Враги — светлые треугольники. У предметов есть точка: красная у редких, зелёная у эмбриона. Общие свет и газ остаются состояниями этажа.')
s=s.replace('● — исходный враг','▲ — исходный враг')
s=s.replace('R на L4 — место спасения с Bomb.','R — место спасения с Bomb (L4 в Original, L3 в Mission).')
s=s.replace('версия для Sega Mega Drive / Genesis (1992). Превью сцен получены её рендерером.','версия для Sega Mega Drive / Genesis (1992), а также ресурсы Amiga Mission Disk, перенесённые в наш ROM v36 test04. Превью сцен получены рендерером ROM.')
s=s.replace('return {floor:', 'return {campaign,floor:',1)
s=s.replace('const data=__DATA__,images=__IMAGES__,$=', 'const banks=__DATA__,imageBanks=__IMAGES__,$=')
s=s.replace("let scale=18,chosen=null,highlightType=null,terminalOn=true;", "let campaign=0,data=banks[0],images=imageBanks[0],scale=18,chosen=null,highlightType=null,terminalOn=true;")
s=s.replace("const spawnTypes=data.map", "let spawnTypes=data.map")
s=s.replace("const enemyNames={", "const enemyNames={'801D':'Робот Mission',")
s=s.replace("function current(){return data[+$('floor').value]}","function current(){return data[+$('floor').value]}\nfunction rescue(){return campaign?{floor:10,x:69,y:25}:{floor:11,x:42,y:14}}")
# Derive access additions from the exact ROM tables, rather than copy old legend.
r=Path('v36/Cyber-Cop_v36_WORK_IN_PROGRESS.bin').read_bytes();sy=json.loads(Path('v36/symbols.json').read_text());names=[l['name'] for l in json.loads((D/'data.json').read_text())[0]];floor_ids=list(range(6))+list(range(8,16));access=[]
for base in [0x1119c,sy['mission_lift_access']]:
 groups=[];seen=set()
 for level in range(8):
  allowed={f for i,f in enumerate(floor_ids) if int.from_bytes(r[base+level*32+i*2:base+level*32+i*2+2],'big')<0x8000}
  groups.append([names[f] for f in sorted(allowed-seen)]);seen=allowed
 access.append(groups)
extra="""
const accessGroups=__ACCESS__;
function campaignInfo(){
 $('originalCampaign').setAttribute('aria-pressed',String(campaign===0));$('missionCampaign').setAttribute('aria-pressed',String(campaign===1));
 $('codeNote').textContent='Коды обычных замков — исходные значения; в новой игре v26+ они перемешиваются. Шлюз: '+(campaign?'8652':'9831')+' (фиксированный).';
 $('accessInfo').innerHTML='Доступ (каждый следующий включает предыдущие): '+accessGroups[campaign].map((g,i)=>'<span class="accessGroup">'+i+' — '+(i?'+':'')+'[<b>'+g.join('</b>, <b>')+'</b>]'+(i===7?'.':';')+'</span>').join('')+' Parking и Warehouse — отдельные переходы.';
}
function switchCampaign(next){
 if(next===campaign)return;
 const sx=$('viewport').scrollLeft,sy=$('viewport').scrollTop,ly=$('legendScroll').scrollTop;
 campaign=next;data=banks[campaign];images=imageBanks[campaign];spawnTypes=data.map(l=>[...new Set(l.respawn_types.filter(Boolean))]);
 campaignInfo();draw();if(chosen)describe(chosen.x,chosen.y);else{$('info').textContent='Выберите клетку';$('preview').innerHTML=''}
 $('viewport').scrollLeft=sx;$('viewport').scrollTop=sy;$('legendScroll').scrollTop=ly;
}
$('originalCampaign').onclick=()=>switchCampaign(0);$('missionCampaign').onclick=()=>switchCampaign(1);
campaignInfo();
function pickupDot(l,t){const item=l.item_ids[t];return item===30?'#00ff66':l.rare_items.includes(item)?'#ff162f':'#142d24'}
function markerClass(l,t){return t===2?'lampMarker':t===9||t===16?'circleMarker':t>=37?'pickupMarker':''}
function legendMarker(l,t,m){return '<span class="sw '+markerClass(l,t)+(t===33&&!terminalOn?' terminalOff':'')+'" style="background:'+m.color+';--dot:'+pickupDot(l,t)+'">'+((t>=37||t===2||t===9||t===16)?'':m.symbol)+'</span>'}
function paintCell(l,i){
 const t=l.cells[i]&63,m=l.legend[t],x=i%80*scale,y=Math.floor(i/80)*scale;
 ctx.fillStyle=t===2||t===9||t===16||t===33&&!terminalOn?'#15212c':m.color;ctx.fillRect(x,y,scale,scale);ctx.strokeStyle='#273747';ctx.lineWidth=1;ctx.strokeRect(x,y,scale,scale);
 if(t===2){ctx.strokeStyle=m.color;ctx.lineWidth=1.5;ctx.strokeRect(x+2,y+2,scale-4,scale-4)}
 else if(t===9||t===16){ctx.fillStyle=m.color;ctx.beginPath();ctx.arc(x+scale/2,y+scale/2,scale*.34,0,Math.PI*2);ctx.fill()}
 else if(t>=37){ctx.fillStyle=pickupDot(l,t);ctx.beginPath();ctx.arc(x+scale/2,y+scale/2,Math.max(2,scale*.15),0,Math.PI*2);ctx.fill();ctx.strokeStyle='#fff4d0';ctx.lineWidth=1;ctx.stroke()}
 else if(scale>=18&&m.symbol&&t!==1&&(t!==33||terminalOn)){ctx.fillStyle='#07101a';ctx.font=Math.floor(scale*.52)+'px monospace';ctx.fillText(m.symbol,x+scale/2,y+scale/2)}
}
""".replace('__ACCESS__',json.dumps(access))
s=s.replace('function outline(',extra+'\nfunction outline(')
start=s.index('for(let i=0;i<4000;i++)');end=s.index('\nif(l.id===11)',start)
s=s[:start]+'for(let i=0;i<4000;i++)paintCell(l,i);'+s[end:]
s=s.replace("if(l.id===11){outline(42,14,'#65e6ff');ctx.fillStyle='#65e6ff';ctx.font=Math.floor(scale*.65)+'px monospace';ctx.fillText('R',42.5*scale,14.5*scale)}", "if(l.id===rescue().floor){const p=rescue();outline(p.x,p.y,'#65e6ff');ctx.fillStyle='#65e6ff';ctx.font=Math.floor(scale*.65)+'px monospace';ctx.fillText('R',(p.x+.5)*scale,(p.y+.5)*scale)}")
s=s.replace("l.objects.forEach(p=>{ctx.fillStyle='#ed506c';ctx.beginPath();ctx.arc((p.x+.5)*scale,(p.y+.5)*scale,scale*.38,0,Math.PI*2);ctx.fill()});","l.objects.forEach(p=>{ctx.fillStyle='#fff3ba';ctx.beginPath();ctx.moveTo((p.x+.5)*scale,(p.y+.08)*scale);ctx.lineTo((p.x+.9)*scale,(p.y+.9)*scale);ctx.lineTo((p.x+.1)*scale,(p.y+.9)*scale);ctx.closePath();ctx.fill()});")
s=s.replace("outline(42,14,'#ffff00')","outline(rescue().x,rescue().y,'#ffff00')")
s=s.replace("l.id===11?", "l.id===rescue().floor?")
s=s.replace("Спасение с Bomb · X42 Y14", "Спасение с Bomb · X'+rescue().x+' Y'+rescue().y+'")
old="'<span class=\"sw '+(+id===33&&!terminalOn?'terminalOff':'')+'\" style=\"background:'+m.color+'\">'+m.symbol+'</span><span>'"
# Replace the actual concatenated sw segment without rebuilding the whole legend.
needle="'<div class=\"entry '+(highlightType===+id?'active':'')+'\" data-type=\"'+id+'\"><span class=\"sw '+(+id===33&&!terminalOn?'terminalOff':'')+'\" style=\"background:'+m.color+'\">'+m.symbol+'</span><span>'"
replacement="'<div class=\"entry '+(highlightType===+id?'active':'')+'\" data-type=\"'+id+'\">'+legendMarker(l,+id,m)+'<span>'"
assert needle in s;s=s.replace(needle,replacement)
s=s.replace('l.id===11&&x===42&&y===14','l.id===rescue().floor&&x===rescue().x&&y===rescue().y')
s=s.replace("if(t===33)info+='<br>Пример маршрута: security access '+accessRoute[l.id]+'.<br>На новом этаже доступ +1, максимум 7. Значение зависит от порядка посещения.';", "if(t===33)info+='<br>'+(campaign?'':('Пример маршрута: security access '+accessRoute[l.id]+'.<br>'))+'На новом этаже доступ +1, максимум 7. Значение зависит от порядка посещения.';")
s=s.replace("t===24?'Игровой рендер с расстояния три клетки'", "t===2?'Светильник: потолочный свет и тень на полу':t===24?'Игровой рендер с расстояния три клетки'")
s=s.replace("const valid=(x,lo,hi)=>Number.isFinite(x)&&x>=lo&&x<=hi;", "const valid=(x,lo,hi)=>Number.isFinite(x)&&x>=lo&&x<=hi;\n if(v.campaign===0||v.campaign===1)switchCampaign(v.campaign);")
s=s.replace('</style>','button[aria-pressed="true"]{background:#526c82;border-color:#d9ecff}.sw.enemy{background:#fff3ba;border-radius:0;clip-path:polygon(50% 5%,95% 95%,5% 95%)}.sw.lampMarker{background:transparent!important;border:2px solid #dae6bf}.sw.circleMarker{border-radius:50%;transform:scale(.75)}.sw.pickupMarker{position:relative}.sw.pickupMarker:after{content:"";position:absolute;width:7px;height:7px;left:8px;top:8px;background:var(--dot);border:1px solid #fff4d0;border-radius:50%}</style>')
# test04 visual refinements; keep data-driven campaign/view state intact.
s=s.replace('#dae6bf','#788474').replace('#fff3ba','#ff2436')
s=s.replace('светлые треугольники','алые треугольники').replace('зелёная у эмбриона','зелёный круг у капсулы с эмбрионом')
s=s.replace("function pickupDot(l,t){const item=l.item_ids[t];return item===30?'#00ff66':l.rare_items.includes(item)?'#ff162f':'#142d24'}", "const pickupColors={7:'#4c80ff',9:'#994bce',10:'#9fdfff',19:'#000000',21:'#13d8c8',22:'#ef75c2',23:'#ffffff',24:'#a37848'};function pickupDot(l,t){const item=l.item_ids[t];return l.rare_items.includes(item)?'#ff162f':pickupColors[item]||'hsl('+((item*137.508+180)%360)+',65%,40%)'}")
s=s.replace("terminalOn=true;", "terminalOn=true,airlockOn=true,blinkPhase=0;")
s=s.replace("t===33&&!terminalOn", "(t===33&&!terminalOn||t===31&&!airlockOn)")
s=s.replace("(t!==33||terminalOn)", "(t!==33||terminalOn)&&(t!==31||airlockOn)")
s=s.replace("t===2?'lampMarker'", "t===22?'capsuleMarker':t===2?'lampMarker'")
s=s.replace("else if(t>=37){", "else if(t===22){ctx.fillStyle='#00e86a';ctx.beginPath();ctx.arc(x+scale/2,y+scale/2,scale*.34,0,Math.PI*2);ctx.fill();if(scale>=18){ctx.fillStyle='#07101a';ctx.font=Math.floor(scale*.52)+'px monospace';ctx.fillText(m.symbol,x+scale/2,y+scale/2)}}\n else if(t>=37){")
s=s.replace("function blinkTerminals(){terminalOn=!terminalOn;", "function blinkTerminals(){terminalOn=!terminalOn;blinkPhase++;if(blinkPhase%3===0){airlockOn=!airlockOn;const l=current();l.cells.forEach((v,i)=>{if((v&63)!==31)return;paintCell(l,i);if(highlightType===31)outline(i%80,Math.floor(i/80),'#ffff00');if(chosen&&chosen.x===i%80&&chosen.y===Math.floor(i/80))outline(chosen.x,chosen.y,'#ffffff')});const sw=document.querySelector('#legend [data-type=\"31\"] .sw');if(sw)sw.classList.toggle('terminalOff',!airlockOn)}")
s=s.replace('</style>', '.sw.capsuleMarker{position:relative;isolation:isolate}.sw.capsuleMarker:before{content:\"\";position:absolute;inset:16%;background:#00e86a;border-radius:50%;z-index:-1}</style>')

(D/'template.html').write_text(s)
page=s.replace('__DATA__',(D/'data.json').read_text()).replace('__IMAGES__',(D/'images.json').read_text())
(D/'Cyber-Cop_Atlas.html').write_text(page)
print('Built dual-campaign atlas with persistent view, markers, access and codes')
