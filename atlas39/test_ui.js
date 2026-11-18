const fs=require('fs'),vm=require('vm'),assert=require('assert');
for(const filename of ['Cyber-Cop_Atlas.html','Cyber-Cop_Atlas_en.html']){
const page=fs.readFileSync('atlas39/'+filename,'utf8'),script=page.match(/<script>([\s\S]*)<\/script>/)[1];
const context=new Proxy({}, {get:(o,k)=>o[k]||(()=>{}),set:(o,k,v)=>(o[k]=v,true)}),els={};let legend=[],outside;
function el(id){if(els[id])return els[id];return els[id]={value:'0',scrollLeft:0,scrollTop:0,style:{setProperty(){}},dataset:{},checked:true,disabled:false,textContent:'',_html:'',setAttribute(k,v){this[k]=v},classList:{toggle(){}},get innerHTML(){return this._html},set innerHTML(v){this._html=v;if(id==='legend')legend=[...v.matchAll(/data-type="([^"]+)"/g)].map(m=>({dataset:{type:m[1]}}));},add(){},addEventListener(){},getContext(){return context},getBoundingClientRect(){return {left:0,top:0,width:360,height:190}}};}
const sandbox={document:{documentElement:{lang:filename.includes('_en')?'en':'ru'},getElementById:el,querySelectorAll:()=>legend,querySelector:s=>s==='aside'?el('aside'):s==='main'?el('main'):null,addEventListener:(n,f)=>outside=f},Option:function(){},console,navigator:{language:'ru'},location:{hash:'',replace(){}},localStorage:{getItem(){return 'ru'},setItem(){}},window:{scrollX:0,scrollY:0,scrollTo(){}},innerWidth:1440,innerHeight:1000,setInterval(){},requestAnimationFrame(f){f()}};
vm.createContext(sandbox);vm.runInContext(script,sandbox);
const english=filename.includes('_en');
assert.equal(el('langRu')['aria-pressed'],String(!english));
assert.equal(el('langEn')['aria-pressed'],String(english));
el(english?'langEn':'langRu').onclick();
assert(!sandbox.location.href);
el('floor').value='9';vm.runInContext('scale=30;chosen={x:10,y:10};draw()',sandbox);el('viewport').scrollLeft=123;el('viewport').scrollTop=456;el('legendScroll').scrollTop=71;
el('missionCampaign').onclick();assert.equal(vm.runInContext('campaign',sandbox),1);assert.equal(+el('floor').value,9);assert.equal(vm.runInContext('scale',sandbox),30);assert.equal(el('viewport').scrollLeft,123);assert.equal(el('viewport').scrollTop,456);assert.equal(el('legendScroll').scrollTop,71);assert(el('codeNote').textContent.includes('8652'));assert(el('accessInfo').innerHTML.includes('L5'));
for(let camp=0;camp<2;camp++)for(let f=0;f<16;f++){
 vm.runInContext(`switchCampaign(${camp})`,sandbox);el('floor').value=String(f);vm.runInContext('draw()',sandbox);
 // Exercise every occupied/interactive map type and each initial enemy.
 vm.runInContext(`{let seen=new Set();current().cells.forEach((v,i)=>{if(!seen.has(v&63)){seen.add(v&63);describe(i%80,Math.floor(i/80))}});current().objects.forEach(o=>describe(o.x,o.y))}`,sandbox);
 const [cells,counts,total]=vm.runInContext('[current().cells,current().pickup_counts,current().pickup_total]',sandbox);
 const expected={};
 for(const v of cells){const t=v&63;if(t>=37)expected[t]=(expected[t]||0)+1}
 assert.equal(JSON.stringify(counts),JSON.stringify(expected));
 assert.equal(total,Object.values(expected).reduce((a,b)=>a+b,0));
 assert(el('pickupTotal').textContent.endsWith(': '+total));
 for(const [t,count] of Object.entries(expected))
  assert.match(el('legend').innerHTML,new RegExp('data-type="'+t+'"[^]*? ×'+count+'</span>'));
 assert(!/undefined/.test(el('info').innerHTML),[camp,f,el('info').innerHTML]);assert(!/src="undefined"/.test(el('preview').innerHTML));
}
vm.runInContext('switchCampaign(1);scale=26',sandbox);el('floor').value='12';el(english?'langRu':'langEn').onclick();const transferred=JSON.parse(decodeURIComponent(sandbox.location.href.split('#view=')[1]));assert.equal(transferred.campaign,1);assert.equal(transferred.floor,12);assert.equal(transferred.scale,26);
vm.runInContext('terminalOn=true;airlockOn=true;blinkPhase=0',sandbox);for(let i=0;i<5;i++){vm.runInContext('blinkTerminals()',sandbox);assert.equal(vm.runInContext('airlockOn',sandbox),true)}vm.runInContext('blinkTerminals()',sandbox);assert.equal(vm.runInContext('airlockOn',sandbox),false);
assert(vm.runInContext('legendRank(33)<legendRank(34)&&legendRank(34)<legendRank(39)&&legendRank(61)<legendRank(14)&&legendRank(16)>legendRank(9)&&legendRank(16)<legendRank(10)',sandbox));
const dots=vm.runInContext('[7,9,10,19,21,22,23,24].map(i=>pickupDot({item_ids:{37:i},rare_items:[]},37))',sandbox);assert.equal(new Set(dots).size,8);assert.equal(dots[3],'#000000');
const show=(camp,f,x,y)=>vm.runInContext(`switchCampaign(${camp});$('floor').value=${f};describe(${x},${y})`,sandbox);
for(const [camp,f,x,y,type,name] of [
 [1,0,15,39,42,'screen 1'], [0,10,76,46,47,'medi kit'], [1,15,3,3,47,'medi kit'],
 [1,7,21,34,51,'face mask'], [1,7,30,48,52,'gas mask']
]){
 show(camp,f,x,y);
 assert.equal(vm.runInContext(`current().cells[${y}*80+${x}]&63`,sandbox),type);
 assert(el('info').innerHTML.includes(name));
 assert(el('preview').innerHTML.includes('data-preview="tile"'));
 if(type===42)assert(el('preview').innerHTML.includes('data-preview="panel"'));
}
for(const [camp,f,x,y] of [[1,11,30,10],[0,15,36,18],[0,13,7,43]]){
 show(camp,f,x,y);
 assert(el('preview').innerHTML.includes('data-preview="tile"'));
 assert(el('preview').innerHTML.includes('data-preview="enemy"'));
 assert(!el('preview').innerHTML.includes('undefined'));
}
for(let camp=0;camp<2;camp++){
 const scene=vm.runInContext(`imageBanks[${camp}].scenes[11]`,sandbox);
 assert(Buffer.from(scene.split(',')[1],'base64').equals(fs.readFileSync('atlas39/scenes/11.png')));
}
assert(!page.includes('Visor 1'));
assert(page.includes(english?'Laser (normal palette)':'Лазер (в обычной палитре)'));
const vertices=[];
context.moveTo=(x,y)=>vertices.push([x,y]);context.lineTo=context.moveTo;
vm.runInContext('scale=20;paintEnemy({x:30,y:10})',sandbox);
assert.deepEqual(vertices,[[610,201.6],[618,218],[602,218]]);
console.log('PASS',filename,'32 maps, pickups and counts, stacked previews, laser, campaign/language view state');
}
