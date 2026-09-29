// Isolated tests for the static client. No browser, live site, or network calls.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const source=fs.readFileSync(process.argv[2]||new URL('./pages-course.js',import.meta.url),'utf8');
const trackCourse=(track='A')=>[
 {id:`${track.toLowerCase()}-day-0`,day0:true,week:0,day:'Setup',minutes:0,url:'/courses/test/setup/',title:'Setup',checks:['ready']},
 {id:`${track.toLowerCase()}-week-01-monday`,week:1,day:'Monday',minutes:60,url:'/courses/test/one/',title:'One',checks:['c1']},
 {id:`${track.toLowerCase()}-week-01-tuesday`,week:1,day:'Tuesday',minutes:60,url:'/courses/test/two/',title:'Two',checks:['c2']}
];
class StorageBus{
 constructor(){this.data=new Map();this.clients=[];this.events=[];this.failRead=false;this.failWrite=false;this.writes=0}
 client(){const client={handlers:new Map()};this.clients.push(client);client.storage={getItem:key=>{if(this.failRead)throw Error('Blocked storage');return this.data.get(key)??null},setItem:(key,value)=>{if(this.failWrite)throw Error('QuotaExceededError');const oldValue=this.data.get(key)??null;this.data.set(key,value);this.writes++;if(value!==oldValue)for(const other of this.clients)if(other!==client)this.events.push([other,{key,oldValue,newValue:value}])}};return client}
 drain(){let count=0;while(this.events.length){if(++count>100)throw Error('Storage events failed to converge');const [client,event]=this.events.shift();client.handlers.get('storage')?.(event)}}
}
function harness({bus=new StorageBus(),track='A',index=trackCourse(track),lesson=index.find(x=>!x.day0)?.id}={}){
 const client=bus.client(),listeners=new Map(),ids={},rows=new Map();
 const make=id=>{const classes=new Set();return {id,textContent:'',value:0,checked:false,disabled:false,hidden:false,dataset:{},classList:{toggle(k,on){const yes=on??!classes.has(k);yes?classes.add(k):classes.delete(k);return yes}},setAttribute(k,v){this[k]=v},addEventListener(event,handler){listeners.set(`${id}:${event}`,handler)}}};
 for(const id of ['save-status','progress-message','retry-load','retry-save','lesson-progress','check-count','lesson-complete','resume-title','resume-detail','export-progress','import-progress'])ids[id]=make(id);
 const inputs=(index.find(l=>l.id===lesson)?.checks||[]).map(check=>{const el=make(check);el.dataset.check=check;return el});
 const total=make('total'),bar=make('course-bar'),week=make('week'),resume=make('resume');week.dataset.weekProgress='1';
 const document={body:{dataset:{lesson}},querySelector(selector){return ids[selector.slice(1)]??null},querySelectorAll(selector){
  if(selector==='input[data-check]')return inputs;
  if(selector==='[data-total-progress]')return [total];
  if(selector==='[data-course-progress]')return [bar];
  if(selector==='[data-week-progress]')return [week];
  if(selector==='[data-resume-link]')return [resume];
  const m=selector.match(/^\[data-lesson-row="([^"]+)"\]$/);if(m){if(!rows.has(m[1])){const row=make('row'+m[1]),circle=make('circle');row.querySelector=()=>circle;rows.set(m[1],row)}return [rows.get(m[1])]}
  return [];
 },getElementById(id){return ids[id]??null}};
 const scope={console,document,window:{localStorage:client.storage,addEventListener(event,fn){client.handlers.set(event,fn)}},location:{pathname:'/courses/test/one/',hash:''},COURSE_INDEX:index,COURSE_CONFIG:{track,title:'Test Course',basePath:'/courses/test',knownCheckIds:['old']},AbortController,URL,Blob,setTimeout,clearTimeout};
 vm.createContext(scope);vm.runInContext(source+`\nglobalThis.test={setCheck,importText,exportText,loadProgress,parseImport};globalThis.inspect=()=>({records:JSON.parse(JSON.stringify(records)),dirty,storageReady,loaded,completed:regular.filter(complete).length,total:regular.length,next:nextLesson()?.id,storageKey});`,scope);
 return {bus,scope,ids,inputs,total,bar,week,resume,client,click(id){return listeners.get(id+':click')()},change(check,done){const el=inputs.find(i=>i.dataset.check===check);el.checked=done;listeners.get(check+':change')()},inspect(){return scope.inspect()},tool:scope.test};
}
const native=(records,course='A')=>JSON.stringify({format:'llm-course-progress',version:1,course,records});
function checkNoUnloadWarning(h,expected){let prevented=false;h.client.handlers.get('beforeunload')({preventDefault(){prevented=true}});assert.equal(prevented,expected)}
let tests=0;
{
 const h=harness();assert.equal(h.inspect().total,2);assert.equal(h.inspect().next,'a-week-01-monday');assert.equal(h.resume.href,'/courses/test/one/');assert.equal(h.inputs[0].disabled,false);
 h.change('c1',true);assert.equal(h.inspect().completed,1);assert.equal(h.inspect().dirty,false);assert.match(h.ids['save-status'].textContent,/this browser only/);
 const reload=harness({bus:h.bus});assert.equal(reload.inputs[0].checked,true);assert.equal(reload.inspect().completed,1);checkNoUnloadWarning(h,false);
 const reordered=trackCourse();reordered[1].id='a-week-07-friday';reordered[1].week=7;
 const moved=harness({bus:h.bus,index:reordered,lesson:reordered[1].id});assert.equal(moved.inputs[0].checked,true,'Progress must use stable checks, not old calendar IDs');
 const other=harness({bus:h.bus,track:'K'});assert.equal(other.inputs[0].checked,false,'Each course needs its own storage key');
 const exported=JSON.parse(h.tool.exportText());assert.equal(exported.course,'A');assert.equal(exported.version,1);assert.equal(exported.records.c1.done,true);assert.ok(!('lesson' in exported.records.c1));tests++;
}
{
 const h=harness();h.change('c1',true);const ts=h.inspect().records.c1.updatedAt;
 h.tool.importText(native({c1:{done:false,updatedAt:ts+1}}));assert.equal(h.inputs[0].checked,false,'A newer explicit false must clear a check');
 h.tool.importText(native({c1:{done:true,updatedAt:ts}}));assert.equal(h.inputs[0].checked,false,'An older import must not resurrect cleared progress');
 h.tool.importText(native({c1:{done:true,updatedAt:ts+1}}));assert.equal(h.inputs[0].checked,false,'False wins timestamp ties');
 h.tool.importText(native({old:{done:true,updatedAt:1}}));assert.equal(h.inspect().records.old.done,true);assert.equal(h.inspect().completed,0,'Archived checks must not count');assert.match(h.ids['save-status'].textContent,/1 archived/);
 const before=h.tool.exportText(),stored=h.bus.data.get(h.inspect().storageKey);
 for(const bad of ['not json',native({c2:{done:true,updatedAt:1}},'K'),native({unknown:{done:true,updatedAt:1}}),native({c2:{done:'true',updatedAt:1}}),native({c2:{done:true,updatedAt:-1}}),JSON.stringify({format:'llm-course-progress',version:99,course:'A',records:{}}),native({c2:{done:true,updatedAt:2},unknown:{done:true,updatedAt:3}})])assert.throws(()=>h.tool.importText(bad));
 assert.equal(h.bus.data.get(h.inspect().storageKey),stored,'Invalid imports must not write or partly import valid entries');assert.deepEqual(JSON.parse(h.tool.exportText()).records,JSON.parse(before).records);tests++;
}
{
 const h=harness();
 h.tool.importText(JSON.stringify({checks:[{lesson:'a-week-01-monday',check:'c1'}]}));assert.equal(h.inputs[0].checked,true);
 h.tool.importText(JSON.stringify({course:'A',checks:{'a-week-01-monday:c1':{done:false,updated_at:'2026-09-29T12:00:00Z'}}}));assert.equal(h.inputs[0].checked,false);
 h.tool.importText(JSON.stringify({course:'A',checks:[{lesson:'week-03-thursday',check:'old',done:true}]}));assert.equal(h.inspect().records.old.done,true);
 for(const bad of [{checks:[{lesson:'k-week-01-monday',check:'c1'}]},{checks:[{lesson:'week-03-thursday',check:'c1'}]},{course:'K',checks:[]},{checks:{'a-week-01-monday:c1':42}}])assert.throws(()=>h.tool.importText(JSON.stringify(bad)));
 tests++;
}
{
 const h=harness();h.bus.failWrite=true;h.change('c1',true);assert.equal(h.inspect().dirty,true);assert.equal(h.inputs[0].checked,true);assert.match(h.ids['save-status'].textContent,/Not saved/);assert.equal(h.ids['retry-load'].hidden,false);checkNoUnloadWarning(h,true);
 const backup=JSON.parse(h.tool.exportText());assert.equal(backup.records.c1.done,true,'A failed local write must still be exportable');
 h.bus.failWrite=false;h.click('retry-load');assert.equal(h.inspect().dirty,false);assert.equal(h.inspect().storageReady,true);checkNoUnloadWarning(h,false);assert.equal(harness({bus:h.bus}).inputs[0].checked,true);tests++;
}
{
 const bus=new StorageBus();bus.data.set('llm-course-progress:v1:A',native({c2:{done:true,updatedAt:1}}));bus.failRead=true;
 const h=harness({bus});assert.equal(h.inputs[0].disabled,false);assert.match(h.ids['save-status'].textContent,/could not be read/);h.change('c1',true);assert.equal(h.inspect().dirty,true);
 bus.failRead=false;h.click('retry-load');assert.equal(h.inspect().records.c1.done,true);assert.equal(h.inspect().records.c2.done,true,'Recovered storage must merge old records with unsaved work');tests++;
}
{
 const bus=new StorageBus();bus.data.set('llm-course-progress:v1:A','broken json');const h=harness({bus});h.change('c1',true);assert.equal(bus.data.get(h.inspect().storageKey),'broken json','Unreadable stored data must not be silently overwritten');assert.equal(h.inspect().dirty,true);assert.equal(JSON.parse(h.tool.exportText()).records.c1.done,true);tests++;
}
{
 const bus=new StorageBus(),a=harness({bus}),b=harness({bus});a.change('c1',true);bus.drain();assert.equal(b.inputs[0].checked,true,'Other tabs must reflect saved checks');
 b.change('c1',false);bus.drain();assert.equal(a.inputs[0].checked,false,'Other tabs must reflect unchecks');
 a.tool.setCheck('c2',true);bus.drain();assert.equal(b.inspect().records.c2.done,true);
 // Simulate a concurrent last-writer snapshot lacking the first tab's c2 edit.
 const snapshot=native({c1:{done:true,updatedAt:a.inspect().records.c1.updatedAt+1}});bus.data.set(a.inspect().storageKey,snapshot);
 a.client.handlers.get('storage')({key:a.inspect().storageKey,newValue:snapshot});bus.drain();
 assert.equal(a.inspect().records.c2.done,true);assert.equal(b.inspect().records.c2.done,true);assert.equal(JSON.parse(bus.data.get(a.inspect().storageKey)).records.c2.done,true,'Concurrent tab writes must converge without losing unrelated checks');
 b.client.handlers.get('storage')({key:'llm-course-progress:v1:K',newValue:native({},'K')});assert.equal(b.inspect().records.c2.done,true,'Another course storage event must be ignored');
 bus.data.delete(a.inspect().storageKey);a.client.handlers.get('storage')({key:a.inspect().storageKey,newValue:null});assert.equal(a.inspect().completed,0);tests++;
}
{
 const h=harness();h.change('c1',true);h.bus.data.delete(h.inspect().storageKey);
 h.client.handlers.get('pageshow')({persisted:true});assert.equal(h.inputs[0].checked,false,'Restored pages must respect a storage reset');
 h.bus.data.set(h.inspect().storageKey,'broken json');h.client.handlers.get('storage')({key:h.inspect().storageKey,newValue:'broken json'});
 assert.equal(h.inspect().storageReady,false);assert.equal(h.inspect().dirty,true);assert.match(h.ids['save-status'].textContent,/could not be read/);checkNoUnloadWarning(h,true);tests++;
}
console.log(`PASS: ${tests} portable-progress scenarios covering storage/reload, stable IDs, Day 0, import validation/merge, legacy imports, archived records, quota/read failure, cross-tab synchronization and backup export.`);
