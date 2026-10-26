const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync('atlas35/Cyber-Cop_Atlas.html','utf8');const script=html.split('<script>')[1].split('</script>')[0];
let entries=[],docclick;const ctx=new Proxy({},{get:(t,p)=>t[p]||(()=>{})});
const elements={};for(const id of ['map','floor','legend','locks','info','preview','prevLevel','nextLevel','plus','minus','langEn','langRu','splitter','previewGrip'])elements[id]={value:'0',_html:'',add(){},getContext(){return ctx},getBoundingClientRect(){return {left:0,top:0}},set innerHTML(s){this._html=s;if(id==='legend')entries=[...s.matchAll(/data-type="([^"]+)"/g)].map(m=>({dataset:{type:m[1]}}))},get innerHTML(){return this._html}};
const box={setInterval(){},innerWidth:1200,innerHeight:900,document:{getElementById:id=>elements[id],querySelectorAll:()=>entries,querySelector:()=>null,addEventListener:(n,f)=>docclick=f},Option:function(){}};vm.createContext(box);vm.runInContext(script,box);
const ev={stopPropagation(){}};let assertions=0;
for(let floor=0;floor<16;floor++){
 elements.floor.value=String(floor);elements.floor.onchange();
 let legend=vm.runInContext('Object.keys(current().legend)',box);
 for(let t of legend){if(+t<2)continue;let entry=entries.find(e=>e.dataset.type===t);entry.onclick(ev);assert.strictEqual(vm.runInContext('highlightType',box),+t);entries.find(e=>e.dataset.type===t).onclick(ev);assert.strictEqual(vm.runInContext('highlightType',box),null);assertions+=2;}
 for(const t of legend){let i=vm.runInContext(`current().cells.findIndex(v=>(v&63)===${t})`,box);vm.runInContext(`describe(${i%80},${Math.floor(i/80)})`,box);if(+t>=37)assert(elements.preview.innerHTML.includes('data:image/png;base64,'));if(+t===34)assert(elements.info.innerHTML.includes('случайный'));assertions++;}
 let os=vm.runInContext('current().objects',box);for(const o of os){vm.runInContext(`describe(${o.x},${o.y})`,box);assert(elements.preview.innerHTML.includes('data:image/png;base64,'));assert(elements.info.innerHTML.includes('Disruptor'));assertions++;}
}
elements.nextLevel.onclick();assert.strictEqual(+elements.floor.value,15);elements.floor.value='0';elements.floor.onchange();elements.prevLevel.onclick();assert.strictEqual(+elements.floor.value,0);
elements.map.onclick({clientX:100,clientY:100,stopPropagation(){}});assert(vm.runInContext('chosen!==null',box));docclick({target:{closest(){return false}}});assert(vm.runInContext('chosen===null',box));
assert(!html.includes('type="checkbox"'));assert(html.includes('#legendScroll{overflow:auto'));assertions+=5;
console.log('PASS',assertions,'atlas JS assertions: all16 floors, legend toggle, all cell types, item/enemy previews, random-code labels, clamped navigation, pin/unpin');
for(let f=0;f<16;f++){
 elements.floor.value=String(f);elements.floor.onchange();
 if(vm.runInContext('current().objects.length',box))assert.strictEqual(entries[0].dataset.type,'enemy');
 if(f===11){const r=entries.find(e=>e.dataset.type==='rescue');assert(r);r.onclick(ev);assert.strictEqual(vm.runInContext('highlightType',box),'rescue');entries.find(e=>e.dataset.type==='rescue').onclick(ev);assert.strictEqual(vm.runInContext('highlightType',box),null);vm.runInContext('describe(42,14)',box);assert(elements.info.innerHTML.includes('Спасение при смерти'));}
 if(f===6){vm.runInContext('describe(27,8)',box);assert(elements.info.innerHTML.includes('embryo'));}
}
vm.runInContext('describe(42,14)',box);
assert(vm.runInContext('Object.keys(images.scenes).length',box)===5);
console.log('PASS enemy legend first, rescue toggle/description, Parking ending details, five embedded scene previews');

assert(vm.runInContext("Object.keys(images.panels.lift).length",box)===16);
for(const t of [31,32,33,34,36]){let floor=dataUnused=0; for(let f=0;f<16;f++){elements.floor.value=String(f);let i=vm.runInContext(`current().cells.findIndex(v=>(v&63)===${t})`,box);if(i>=0){vm.runInContext(`describe(${i%80},${Math.floor(i/80)})`,box);assert(elements.preview.innerHTML.includes("panelImage"));break;}}}
console.log("PASS interaction previews and 16 lift displays");
const en=fs.readFileSync('atlas35/Cyber-Cop_Atlas_en.html','utf8');assert(!/[А-Яа-яЁё]/.test(en));
const enscript=en.split('<script>')[1].split('</script>')[0];
for(const [language,saved,blocked,want] of [['ru-RU',null,false,null],['en-US',null,false,'Cyber-Cop_Atlas_en.html'],['de-DE',null,true,'Cyber-Cop_Atlas_en.html'],['en-US','ru',false,null]]){
 let moved=null;const b={...box,document:{...box.document,documentElement:{lang:'ru'}},navigator:{language},localStorage:{getItem(){if(blocked)throw Error();return saved},setItem(){}},location:{replace(x){moved=x}}};vm.createContext(b);vm.runInContext(script,b);assert.strictEqual(moved,want);
}
let langSaved=null;const eb={...box,document:{...box.document,documentElement:{lang:'en'}},navigator:{language:'en'},localStorage:{getItem(){return null},setItem(k,v){langSaved=v}},location:{}};vm.createContext(eb);vm.runInContext(enscript,eb);
assert.strictEqual(vm.runInContext('data.length',eb),16);assert.strictEqual(vm.runInContext('JSON.stringify(data.map(f=>f.cells))',eb),vm.runInContext('JSON.stringify(data.map(f=>f.cells))',box));
elements.langRu.onclick();assert.strictEqual(langSaved,'ru');assert.strictEqual(eb.location.href,'Cyber-Cop_Atlas.html');
console.log('PASS English contains no untranslated Cyrillic; language default/override/storage denial and Ru switching');

// Arrival markers and coordinate transform match native fixtures.
for(const [f,x,y,df,dx,dy] of [[5,76,24,6,3,24],[5,59,4,7,18,46],[6,32,4,7,71,46],[7,71,45,6,30,5],[7,18,45,5,59,5]]){assert.strictEqual(vm.runInContext(`JSON.stringify(airlockDestination(${f},${x},${y}))`,box),JSON.stringify({floor:df,x:dx,y:dy}));}
for(let f of [0,6,7]){elements.floor.value=String(f);elements.floor.onchange();assert(entries.some(e=>e.dataset.type==='arrival'));}
let phase=vm.runInContext('terminalOn',box);vm.runInContext('blinkTerminals()',box);assert.strictEqual(vm.runInContext('terminalOn',box),!phase);vm.runInContext('blinkTerminals()',box);assert.strictEqual(vm.runInContext('terminalOn',box),phase);
assert(html.includes('setInterval(blinkTerminals,250)'));assert(html.includes('resizeHandle'));console.log('PASS arrival references, terminal blink phase/period, resizing handles');
