/* Portable static course progress. No account, backend, or network requests. */
const $=selector=>document.querySelector(selector), $$=selector=>[...document.querySelectorAll(selector)];
const course=COURSE_INDEX;
const regular=course.filter(lesson=>!lesson.day0);
const lessonId=document.body.dataset.lesson;
const courseId=COURSE_CONFIG.track;
const storageKey=`llm-course-progress:v1:${courseId}`;
const visibleChecks=new Set(course.flatMap(lesson=>lesson.checks));
const allowedChecks=new Set([...visibleChecks,...(COURSE_CONFIG.knownCheckIds||[])]);
const FORMAT='llm-course-progress', VERSION=1, MAX_IMPORT_BYTES=1024*1024;
const inputs=$$('input[data-check]');
let records=Object.create(null), loaded=false, storageReady=false, dirty=false;

function message(text,error=false){
 for(const el of new Set([$('#save-status'),$('#progress-message')]))if(el){el.textContent=text;el.classList.toggle('error',error)}
}
function retryVisible(show){for(const id of ['#retry-load','#retry-save']){const el=$(id);if(el)el.hidden=!show}}
function isObject(value){return value!==null&&typeof value==='object'&&!Array.isArray(value)}
function timestamp(value){
 if(typeof value==='number'&&Number.isSafeInteger(value)&&value>=0&&value<Number.MAX_SAFE_INTEGER-1)return value;
 if(typeof value==='string'&&/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?Z$/.test(value)){
  const parsed=Date.parse(value);if(Number.isSafeInteger(parsed)&&parsed>=0)return parsed;
 }
 throw Error('A progress timestamp is invalid.');
}
function checkRecord(check,value){
 if(typeof check!=='string'||!allowedChecks.has(check))throw Error('This file contains a checklist item that is not in this course.');
 if(!isObject(value)||typeof value.done!=='boolean')throw Error('Every progress record must have a true or false completion value.');
 return {done:value.done,updatedAt:timestamp(value.updatedAt)};
}
function parseNative(value){
 if(!isObject(value)||value.format!==FORMAT||value.version!==VERSION)throw Error('Unsupported progress file format or version.');
 if(value.course!==courseId)throw Error('This progress file belongs to a different course.');
 if(!isObject(value.records))throw Error('The progress file is missing its checklist records.');
 if(value.exportedAt!==undefined)timestamp(value.exportedAt);
 const result=Object.create(null);
 for(const [check,record] of Object.entries(value.records))result[check]=checkRecord(check,record);
 return result;
}
function mergeRecords(left,right){
 const result=Object.assign(Object.create(null),left);
 for(const [check,incoming] of Object.entries(right)){
  const current=result[check];
  // A false tombstone wins an exact timestamp tie, avoiding accidental completion.
  if(!current||incoming.updatedAt>current.updatedAt||
     (incoming.updatedAt===current.updatedAt&&!incoming.done&&current.done))result[check]={...incoming};
 }
 return result;
}
function orderedRecords(value){return Object.fromEntries(Object.entries(value).sort(([a],[b])=>a.localeCompare(b)).map(([check,record])=>[check,{done:record.done,updatedAt:record.updatedAt}]))}
function envelope(value=records){return {format:FORMAT,version:VERSION,course:courseId,records:orderedRecords(value)}}
function encode(value){return JSON.stringify(envelope(value))}
function readStorage(){
 const raw=window.localStorage.getItem(storageKey);
 return {raw,records:raw===null?Object.create(null):parseNative(JSON.parse(raw))};
}
function nextTimestamp(){return Math.max(Date.now(),...Object.values(records).map(record=>record.updatedAt+1))}
function count(lesson){return lesson.checks.filter(check=>records[check]?.done===true).length}
function complete(lesson){return lesson.checks.length>0&&count(lesson)===lesson.checks.length}
function nextLesson(){return regular.find(lesson=>!complete(lesson))||regular[regular.length-1]||null}
function render(){
 const completed=regular.filter(complete).length;
 for(const lesson of course){const n=count(lesson),done=complete(lesson);
  $$(`[data-lesson-row="${lesson.id}"]`).forEach(row=>{
   row.classList.toggle('partial',n>0&&!done);const circle=row.querySelector('.status-circle');
   if(circle){circle.classList.toggle('done',done);circle.textContent=done?'✓':'';circle.setAttribute('aria-label',done?'Completed':n?'In progress':'Not started')}
  });
 }
 $$('[data-total-progress]').forEach(el=>el.textContent=loaded?`${completed} of ${regular.length} lessons complete${storageReady?'':' · this page only'}`:'Loading progress…');
 $$('[data-course-progress]').forEach(el=>{el.max=regular.length;el.value=completed});
 $$('[data-week-progress]').forEach(el=>{const week=regular.filter(lesson=>lesson.week===Number(el.dataset.weekProgress));el.textContent=`${week.filter(complete).length} / ${week.length} complete`});
 const next=nextLesson();
 if(next){
  $$('[data-resume-link]').forEach(el=>{el.href=next.url;el.textContent=completed===regular.length?'Review final lesson':completed?'Continue learning':'Start learning'});
  if($('#resume-title'))$('#resume-title').textContent=next.title;
  if($('#resume-detail'))$('#resume-detail').textContent=`Week ${next.week} · ${next.day} · ${next.minutes} min`;
 }
 inputs.forEach(input=>{input.checked=records[input.dataset.check]?.done===true;input.disabled=!loaded});
 const current=course.find(lesson=>lesson.id===lessonId);
 if(current){
  const n=count(current);
  if($('#lesson-progress'))$('#lesson-progress').value=n;
  if($('#check-count'))$('#check-count').textContent=`${n} of ${current.checks.length} checked`;
  if($('#lesson-complete'))$('#lesson-complete').hidden=!complete(current);
 }
}
function loadProgress(){
 try{
  const stored=readStorage();records=dirty?mergeRecords(stored.records,records):stored.records;storageReady=true;loaded=true;
  if(dirty){persist();return}
  retryVisible(false);message('Progress is stored in this browser only. Export a backup to move it to another browser or device.');
 }catch{
  loaded=true;storageReady=false;retryVisible(true);
  message('Browser storage could not be read. Your checks will work in this page only. Export a backup before closing, or retry storage.',true);
 }
 render();
}
function persist(successMessage='Saved in this browser only. Export a backup to keep a portable copy.'){
 try{
  const stored=readStorage();records=mergeRecords(stored.records,records);
  const value=encode(records);if(value!==stored.raw)window.localStorage.setItem(storageKey,value);
  storageReady=true;dirty=false;retryVisible(false);message(successMessage);
 }catch{
  storageReady=false;dirty=true;retryVisible(true);
  message('Not saved to browser storage. Keep this page open and export a backup, or retry storage. Storage may be blocked or full.',true);
 }
 render();
 return !dirty;
}
function setCheck(check,done){
 if(!visibleChecks.has(check)||typeof done!=='boolean')return;
 // Read again before a local edit, so another tab's latest timestamp is respected.
 try{records=mergeRecords(records,readStorage().records)}catch{}
 records[check]={done,updatedAt:nextTimestamp()};dirty=true;persist();
}
function parseImport(value){
 if(isObject(value)&&value.format===FORMAT)return parseNative(value);
 // Legacy server exports: {course:'A',checks:[{lesson,check,done?,updated_at?}]}
 // or {checks:{'a-week-01-monday:a101-p1-c1':true}}. An unlabelled
 // export must identify this course in every original lesson ID.
 if(!isObject(value)||!Object.hasOwn(value,'checks'))throw Error('Unsupported progress file format.');
 if(value.format!==undefined&&value.format!=='llm-course-server-progress')throw Error('Unsupported progress file format.');
 if(value.version!==undefined&&value.version!==1)throw Error('Unsupported progress file version.');
 if(value.course!==undefined&&value.course!==courseId)throw Error('This progress file belongs to a different course.');
 let rows;
 if(Array.isArray(value.checks))rows=value.checks;
 else if(isObject(value.checks))rows=Object.entries(value.checks).map(([identity,state])=>{
  const split=identity.lastIndexOf(':');
  if(split<1)throw Error('A legacy checklist identity is invalid.');
  if(typeof state!=='boolean'&&(!isObject(state)||typeof state.done!=='boolean'))throw Error('A legacy checklist state is invalid.');
  return {...(typeof state==='boolean'?{done:state}:state),lesson:identity.slice(0,split),check:identity.slice(split+1)};
 });
 else throw Error('The legacy progress file has no valid checks.');
 const fallback=value.exportedAt===undefined?0:timestamp(value.exportedAt);
 let result=Object.create(null);
 for(const row of rows){
  if(!isObject(row)||typeof row.lesson!=='string'||typeof row.check!=='string')throw Error('A legacy checklist record is invalid.');
  const prefix=row.lesson.match(/^([akh])-/i);
  if((prefix&&prefix[1].toUpperCase()!==courseId)||(!prefix&&value.course!==courseId))throw Error('This legacy file does not identify the current course.');
  const record=checkRecord(row.check,{done:row.done===undefined?true:row.done,updatedAt:row.updatedAt??row.updated_at??fallback});
  result=mergeRecords(result,{[row.check]:record});
 }
 return result;
}
function importText(text){
 if(typeof text!=='string'||text.length>MAX_IMPORT_BYTES)throw Error('The progress file is too large. Choose a file under 1 MB.');
 let value;try{value=JSON.parse(text)}catch{throw Error('The selected file is not valid JSON.')}
 const incoming=parseImport(value);
 // Validation finishes before any state is changed.
 try{records=mergeRecords(records,readStorage().records)}catch{}
 records=mergeRecords(records,incoming);loaded=true;dirty=true;
 const archived=Object.keys(incoming).filter(check=>!visibleChecks.has(check)).length;
 persist(`Imported ${Object.keys(incoming).length} checklist records${archived?` (${archived} archived)`:''}. Newer choices are kept. Saved in this browser only.`);
 return Object.keys(incoming).length;
}
function exportText(){return JSON.stringify({...envelope(),exportedAt:new Date().toISOString()},null,2)+'\n'}
function exportProgress(){
 try{
  const url=URL.createObjectURL(new Blob([exportText()],{type:'application/json'}));
  const link=document.createElement('a');link.href=url;link.download=`${courseId.toLowerCase()}-course-progress.json`;
  document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  message(storageReady?'Backup exported. It contains checklist progress only and stays on your device.':'Backup exported from this page. Browser storage is unavailable, so it may omit previously saved progress.',!storageReady);
 }catch{message('Could not export a backup. Keep this page open and try again.',true)}
}
inputs.forEach(input=>input.addEventListener('change',()=>setCheck(input.dataset.check,input.checked)));
$('#retry-load')?.addEventListener('click',()=>dirty?persist():loadProgress());
$('#retry-save')?.addEventListener('click',()=>persist());
$('#export-progress')?.addEventListener('click',exportProgress);
$('#import-progress')?.addEventListener('change',async event=>{
 const input=event.target,file=input.files?.[0];if(!file)return;
 try{if(file.size>MAX_IMPORT_BYTES)throw Error('The progress file is too large. Choose a file under 1 MB.');importText(await file.text())}
 catch(error){message(`Import failed: ${error.message}`,true)}
 finally{input.value=''}
});
window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue=''}});
window.addEventListener('storage',event=>{
 if(event.key!==storageKey&&event.key!==null)return;
 try{
  // A deliberate clear/removal is reflected in other tabs unless unsaved edits exist.
  if(event.newValue===null){
   const latest=readStorage();
   if(latest.raw!==null){records=mergeRecords(records,latest.records);persist('Progress updated from another tab. It is stored in this browser only.');return}
   if(!dirty){records=Object.create(null);storageReady=true;loaded=true;retryVisible(false);message('Browser progress was cleared in another tab.');render()}
   else message('Browser progress was cleared in another tab. Unsaved edits remain here; export them before closing.',true);
   return;
  }
  const incoming=parseNative(JSON.parse(event.newValue));records=mergeRecords(records,incoming);loaded=true;
  // Reconcile overlapping writes by different tabs without discarding either edit.
  persist('Progress updated from another tab. It is stored in this browser only.');
 }catch{storageReady=false;dirty=true;retryVisible(true);message('Another tab changed progress, but its data could not be read. Your checklist has been kept in this page. Export a backup or retry storage.',true);render()}
});
window.addEventListener('pageshow',event=>{if(event.persisted)loadProgress()});
$('#menu-button')?.addEventListener('click',()=>{const open=$('#sidebar').classList.toggle('open');$('#menu-button').setAttribute('aria-expanded',String(open))});
function localPath(path){
 const base=(COURSE_CONFIG.basePath||'').replace(/\/$/,'');
 return base&&path!==base&&!path.startsWith(base+'/')?base+path:path;
}
function openHash(){if(location.hash){const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(target?.tagName==='DETAILS')target.open=true}}
try{openHash()}catch{}
window.addEventListener('hashchange',()=>{try{openHash()}catch{}});
loadProgress();
if(document.modelContext?.registerTool){
 const lifecycle=new AbortController();
 try{Promise.resolve(document.modelContext.registerTool({name:'read_course_progress',title:'Read course progress',description:'Read checklist progress saved in this browser and the next incomplete course lesson. Setup is excluded from lesson totals. Does not change completion.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true,untrustedContentHint:false},execute(input){
  if(!isObject(input)||Object.keys(input).length)throw Error('Expected an empty object.');
  if(!loaded||!storageReady||dirty)throw Error('Browser progress is not saved. Retry storage or export a backup from the page.');
  return {course:COURSE_CONFIG.title,storage:'this browser only',complete:regular.filter(complete).length,total:regular.length,next:regular.find(lesson=>!complete(lesson))||null};
 }},{signal:lifecycle.signal})).catch(()=>{})}catch{}
 window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});
}

// Load third-party video players only after the learner asks to watch.
$$('[data-video]').forEach(button=>button.addEventListener('click',()=>{
 const id=button.dataset.video;if(!/^[\w-]{11}$/.test(id))return;
 const frame=document.createElement('iframe');frame.src=`https://www.youtube-nocookie.com/embed/${id}`;
 frame.title=button.dataset.videoTitle||'Course video';frame.loading='lazy';frame.allow='encrypted-media; picture-in-picture; fullscreen';
 frame.allowFullscreen=true;frame.referrerPolicy='strict-origin-when-cross-origin';button.parentNode.replaceChildren(frame);
}));
