const DB_NAME='food-choice-db',DB_VERSION=1,HISTORY_STORE='history',SETTINGS_STORE='settings';
const LS_HISTORY='food-choice-history-v1',LS_SETTINGS='food-choice-settings-v1';
const memory={history:[],settings:{}};

function openDB(){return new Promise((resolve,reject)=>{if(typeof indexedDB==='undefined'){reject(new Error('IndexedDB unavailable'));return}const request=indexedDB.open(DB_NAME,DB_VERSION);request.onupgradeneeded=()=>{const db=request.result;if(!db.objectStoreNames.contains(HISTORY_STORE)){const store=db.createObjectStore(HISTORY_STORE,{keyPath:'id',autoIncrement:true});store.createIndex('cookedAt','cookedAt')}if(!db.objectStoreNames.contains(SETTINGS_STORE))db.createObjectStore(SETTINGS_STORE,{keyPath:'key'})};request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error||new Error('IndexedDB open failed'));request.onblocked=()=>reject(new Error('IndexedDB blocked'))})}
function txDone(tx){return new Promise((resolve,reject)=>{tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error||new Error('IndexedDB transaction failed'));tx.onabort=()=>reject(tx.error||new Error('IndexedDB transaction aborted'))})}
function sortHistory(items){return [...items].sort((a,b)=>new Date(b.cookedAt)-new Date(a.cookedAt))}
function readLocal(key,fallback){try{const raw=localStorage.getItem(key);return raw?JSON.parse(raw):fallback}catch{return fallback}}
function writeLocal(key,value){try{localStorage.setItem(key,JSON.stringify(value));return true}catch{return false}}
function fallbackHistory(){const saved=readLocal(LS_HISTORY,null);return Array.isArray(saved)?saved:memory.history}
function saveFallbackHistory(items){memory.history=[...items];writeLocal(LS_HISTORY,items)}
function fallbackSettings(){const saved=readLocal(LS_SETTINGS,null);return saved&&typeof saved==='object'?saved:memory.settings}
function saveFallbackSettings(settings){memory.settings={...settings};writeLocal(LS_SETTINGS,settings)}
async function withFallback(primary,fallback){try{return await primary()}catch(error){console.warn('[Food Choice] storage fallback:',error);return fallback()}}

export async function getHistory(){return withFallback(async()=>{const db=await openDB();return new Promise((resolve,reject)=>{const tx=db.transaction(HISTORY_STORE,'readonly');const req=tx.objectStore(HISTORY_STORE).getAll();req.onsuccess=()=>resolve(sortHistory(req.result));req.onerror=()=>reject(req.error)})},()=>sortHistory(fallbackHistory()))}
export async function addHistory(entry){return withFallback(async()=>{const db=await openDB();const tx=db.transaction(HISTORY_STORE,'readwrite');tx.objectStore(HISTORY_STORE).add(entry);await txDone(tx)},()=>{const items=fallbackHistory();items.push({...entry,id:`fallback-${Date.now()}-${Math.random().toString(16).slice(2)}`});saveFallbackHistory(items)})}
export async function clearHistory(){return withFallback(async()=>{const db=await openDB();const tx=db.transaction(HISTORY_STORE,'readwrite');tx.objectStore(HISTORY_STORE).clear();await txDone(tx)},()=>saveFallbackHistory([]))}
export async function getSetting(key){return withFallback(async()=>{const db=await openDB();return new Promise((resolve,reject)=>{const tx=db.transaction(SETTINGS_STORE,'readonly');const req=tx.objectStore(SETTINGS_STORE).get(key);req.onsuccess=()=>resolve(req.result?.value);req.onerror=()=>reject(req.error)})},()=>fallbackSettings()[key])}
export async function setSetting(key,value){return withFallback(async()=>{const db=await openDB();const tx=db.transaction(SETTINGS_STORE,'readwrite');tx.objectStore(SETTINGS_STORE).put({key,value});await txDone(tx)},()=>{const settings={...fallbackSettings(),[key]:value};saveFallbackSettings(settings)})}
