const fs=require('fs'),vm=require('vm'),assert=require('assert');
for(const filename of ['Cyber-Cop_Atlas.html','Cyber-Cop_Atlas_en.html']){
const page=fs.readFileSync('atlas39/'+filename,'utf8'),script=page.match(/<script>([\s\S]*)<\/script>/)[1];
const context=new Proxy({}, {get:(o,k)=>o[k]||(()=>{}),set:(o,k,v)=>(o[k]=v,true)}),els={};let legend=[],outside;
function el(id){if(els[id])return els[id];return els[id]={value:'0',scrollLeft:0,scrollTop:0,style:{setProperty(){}},dataset:{},checked:true,disabled:false,textContent:'',_html:'',setAttribute(k,v){this[k]=v},classList:{toggle(){}},get innerHTML(){return this._html},set innerHTML(v){this._html=v;if(id==='legend')legend=[...v.matchAll(/data-type="([^"]+)"/g)].map(m=>({dataset:{type:m[1]}}));},add(){},addEventListener(){},getContext(){return context},getBoundingClientRect(){return {left:0,top:0,width:360,height:190}}};}
const sandbox={document:{documentElement:{lang:filename.includes('_en')?'en':'ru'},getElementById:el,querySelectorAll:()=>legend,querySelector:s=>s==='aside'?el('aside'):s==='main'?el('main'):null,addEventListener:(n,f)=>outside=f},Option:function(){},console,navigator:{language:'ru'},location:{hash:'',replace(){}},localStorage:{getItem(){return 'ru'},setItem(){}},window:{scrollX:0,scrollY:0,scrollTo(){}},innerWidth:1440,innerHeight:1000,setInterval(){},requestAnimationFrame(f){f()}};
vm.createContext(sandbox);vm.runInContext(script,sandbox);
el('floor').value='9';vm.runInContext('scale=30;chosen={x:10,y:10};draw()',sandbox);el('viewport').scrollLeft=123;el('viewport').scrollTop=456;el('legendScroll').scrollTop=71;
el('missionCampaign').onclick();assert.equal(vm.runInContext('campaign',sandbox),1);assert.equal(+el('floor').value,9);assert.equal(vm.runInContext('scale',sandbox),30);assert.equal(el('viewport').scrollLeft,123);assert.equal(el('viewport').scrollTop,456);assert.equal(el('legendScroll').scrollTop,71);assert(el('codeNote').textContent.includes('8652'));assert(el('accessInfo').innerHTML.includes('L5'));
for(let camp=0;camp<2;camp++)for(let f=0;f<16;f++){
 vm.runInContext(`switchCampaign(${camp})`,sandbox);el('floor').value=String(f);vm.runInContext('draw()',sandbox);
 // Exercise every occupied/interactive map type and each initial enemy.
 vm.runInContext(`{let seen=new Set();current().cells.forEach((v,i)=>{if(!seen.has(v&63)){seen.add(v&63);describe(i%80,Math.floor(i/80))}});current().objects.forEach(o=>describe(o.x,o.y))}`,sandbox);
 assert(!/undefined/.test(el('info').innerHTML),[camp,f,el('info').innerHTML]);assert(!/src="undefined"/.test(el('preview').innerHTML));
}
vm.runInContext('switchCampaign(1);scale=26',sandbox);el('floor').value='12';el('langEn').onclick();const transferred=JSON.parse(decodeURIComponent(sandbox.location.href.split('#view=')[1]));assert.equal(transferred.campaign,1);assert.equal(transferred.floor,12);assert.equal(transferred.scale,26);
vm.runInContext('terminalOn=true;airlockOn=true;blinkPhase=0;blinkTerminals()',sandbox);assert.equal(vm.runInContext('airlockOn',sandbox),true);vm.runInContext('blinkTerminals()',sandbox);assert.equal(vm.runInContext('airlockOn',sandbox),true);vm.runInContext('blinkTerminals()',sandbox);assert.equal(vm.runInContext('airlockOn',sandbox),false);
const dots=vm.runInContext('[7,9,10,19,21,22,23,24].map(i=>pickupDot({item_ids:{37:i},rare_items:[]},37))',sandbox);assert.equal(new Set(dots).size,8);assert.equal(dots[3],'#000000');
console.log('PASS',filename,'32 maps, every type/enemy, campaigns retain view and language carries campaign');
}
