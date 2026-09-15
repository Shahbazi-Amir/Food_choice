import {fitMessage,formatMinutes,rankFoods,totalMinutes} from './scoring.js';

let FOODS=[];
let CATEGORIES=[];
const DEFAULT_USUAL=new Set(['قورمه‌سبزی','قیمه','زرشک‌پلو با مرغ','عدس‌پلو','ماکارونی','کتلت','کوکو سبزی','املت گوجه','کباب تابه‌ای','لوبیاپلو','آش رشته','میرزا قاسمی']);
const STORAGE_KEY='food-choice-browser-prototype-v2';
const OLD_STORAGE_KEY='food-choice-browser-prototype-v1';
const $=id=>document.getElementById(id);
const state={usual:new Set(),tryFoods:new Set(),people:4,time:'any',costs:new Set(),weights:new Set(),categories:new Set(),priority:'balanced',current:null,ranked:[],rankIndex:0,history:[]};

function saveState(){localStorage.setItem(STORAGE_KEY,JSON.stringify({usual:[...state.usual],tryFoods:[...state.tryFoods],people:state.people,history:state.history}))}
function loadState(){try{const raw=localStorage.getItem(STORAGE_KEY)||localStorage.getItem(OLD_STORAGE_KEY);const saved=JSON.parse(raw||'null');if(!saved)return false;const names=new Set(FOODS.map(f=>f.name));state.usual=new Set((saved.usual||[]).filter(x=>names.has(x)));state.tryFoods=new Set((saved.tryFoods||[]).filter(x=>names.has(x)&&!state.usual.has(x)));state.people=Math.max(1,Math.min(12,Number(saved.people)||4));state.history=(saved.history||[]).filter(x=>names.has(x.name)).slice(0,20);saveState();return state.usual.size>=3}catch{return false}}
function toast(msg){const el=$('toast');el.textContent=msg;el.classList.add('show');clearTimeout(toast.t);toast.t=setTimeout(()=>el.classList.remove('show'),1900)}
function show(id){$(id).classList.remove('hidden')}
function hide(id){$(id).classList.add('hidden')}

function renderUsualFoods(){const box=$('usualFoodGroups');box.innerHTML='';for(const category of CATEGORIES){const group=document.createElement('div');group.className='food-group';group.innerHTML=`<div class="food-group-title">${category}</div><div class="food-chips"></div>`;const chips=group.querySelector('.food-chips');FOODS.filter(f=>f.category===category).forEach(food=>{const b=document.createElement('button');b.type='button';b.className='food-chip'+(state.usual.has(food.name)?' selected':'');b.textContent=food.name;b.onclick=()=>{state.usual.has(food.name)?state.usual.delete(food.name):state.usual.add(food.name);state.tryFoods.delete(food.name);b.classList.toggle('selected');hide('usualError')};chips.appendChild(b)});box.appendChild(group)}}
function renderPeople(){$('peopleCount').textContent=state.people}

function suggestedNewFoods(){
  const usualCats=new Set(FOODS.filter(f=>state.usual.has(f.name)).map(f=>f.category));
  const candidates=FOODS.filter(f=>!state.usual.has(f.name));
  candidates.sort((a,b)=>Number(usualCats.has(a.category))-Number(usualCats.has(b.category))||totalMinutes(a)-totalMinutes(b)||(a.cost==='اقتصادی'?-1:1));
  const picked=[];
  for(const category of CATEGORIES){for(const food of candidates.filter(f=>f.category===category).slice(0,2)){if(!picked.some(x=>x.name===food.name))picked.push(food)}}
  for(const food of candidates){if(picked.length>=20)break;if(!picked.some(x=>x.name===food.name))picked.push(food)}
  return picked.slice(0,20);
}
function renderTryFoods(){const list=$('tryFoodList');list.innerHTML='';suggestedNewFoods().forEach(food=>{const b=document.createElement('button');b.type='button';b.className='try-card'+(state.tryFoods.has(food.name)?' selected':'');b.innerHTML=`${food.name}<small>${food.category} · ${food.weight} · ${formatMinutes(totalMinutes(food))}</small>`;b.onclick=()=>{state.tryFoods.has(food.name)?state.tryFoods.delete(food.name):state.tryFoods.add(food.name);b.classList.toggle('selected')};list.appendChild(b)})}
function renderCategoryFilters(){const box=$('categoryOptions');box.innerHTML='';CATEGORIES.forEach(cat=>{const b=document.createElement('button');b.type='button';b.className='choice';b.dataset.value=cat;b.textContent=cat;b.onclick=()=>toggleMulti(b,state.categories);box.appendChild(b)})}
function toggleMulti(button,set){const value=button.dataset.value;set.has(value)?set.delete(value):set.add(value);button.classList.toggle('active')}

function renderProfileSummary(){$('profileSummary').textContent=`${state.usual.size} غذای معمول · ${state.tryFoods.size} غذای جدید · ${state.people} نفر`}
function showMain(){hide('setupStep1');hide('setupStep2');show('mainScreen');show('resetApp');renderProfileSummary();renderHistory()}
function showSetup(){show('setupStep1');hide('setupStep2');hide('mainScreen');renderUsualFoods();renderPeople();$('resetApp').classList.toggle('hidden',state.usual.size<3)}

function currentPrefs(){return {time:state.time,costs:[...state.costs],weights:[...state.weights],categories:[...state.categories],allowTry:$('allowTryFoods').checked}}
function recommend(){
  state.ranked=rankFoods(FOODS,state.usual,state.tryFoods,currentPrefs(),state.priority,state.history);
  state.rankIndex=0;
  if(!state.ranked.length){hide('resultCard');show('noResult');return}
  hide('noResult');state.current=state.ranked[0];renderResult(state.current);show('resultCard');$('resultCard').scrollIntoView({behavior:'smooth',block:'start'});
}
function renderResult(food){
  state.current=food;
  $('sourceBadge').textContent=food._source==='usual'?'🏠 از غذاهای معمول خودت':food._source==='try'?'✨ از غذاهایی که خودت برای امتحان انتخاب کردی':'🍽️ از کاتالوگ';
  $('foodName').textContent=food.name;
  $('foodBadges').innerHTML=`<span>${food.category}</span><span>${food.weight}</span><span>${food.cost}</span>`;
  $('fitMessage').textContent=fitMessage(food);
  $('prepTime').textContent=formatMinutes(food.prep);$('cookTime').textContent=formatMinutes(food.cook);$('totalTime').textContent=formatMinutes(totalMinutes(food));
  $('peopleLabel').textContent=`برای ${state.people} نفر`;
  $('ingredientsList').innerHTML=food.ingredients.map(item=>`<span>${item}</span>`).join('');
}
function anotherFood(){if(!state.ranked.length){recommend();return}state.rankIndex=(state.rankIndex+1)%state.ranked.length;renderResult(state.ranked[state.rankIndex]);$('resultCard').scrollIntoView({behavior:'smooth',block:'start'})}

function renderHistory(){const card=$('historyCard'),list=$('historyList');if(!state.history.length){hide('historyCard');return}show('historyCard');list.innerHTML=state.history.slice(0,8).map(item=>`<div class="history-row"><strong>${item.name}</strong><span>${new Date(item.at).toLocaleDateString('fa-IR')}</span></div>`).join('')}
function acceptCurrent(){if(!state.current)return;state.history=state.history.filter(x=>x.name!==state.current.name);state.history.unshift({name:state.current.name,at:new Date().toISOString()});state.history=state.history.slice(0,20);saveState();renderHistory();toast('ثبت شد؛ نوش جان 🌿')}

function bindSingle(containerId,dataKey,stateKey){$(containerId).querySelectorAll(`[${dataKey}]`).forEach(button=>button.onclick=()=>{$(containerId).querySelectorAll('.choice').forEach(x=>x.classList.remove('active'));button.classList.add('active');state[stateKey]=button.dataset[dataKey.replace('data-','')]})}
function bindMulti(containerId,set){$(containerId).querySelectorAll('.choice').forEach(button=>button.onclick=()=>toggleMulti(button,set))}

function bindEvents(){
  $('selectDefaults').onclick=()=>{state.usual=new Set([...DEFAULT_USUAL].filter(name=>FOODS.some(f=>f.name===name)));renderUsualFoods()};
  $('clearUsual').onclick=()=>{state.usual.clear();renderUsualFoods()};
  $('peopleMinus').onclick=()=>{state.people=Math.max(1,state.people-1);renderPeople()};
  $('peoplePlus').onclick=()=>{state.people=Math.min(12,state.people+1);renderPeople()};
  $('goToTryFoods').onclick=()=>{if(state.usual.size<3){show('usualError');return}hide('setupStep1');show('setupStep2');renderTryFoods()};
  $('skipTryFoods').onclick=()=>{state.tryFoods.clear();saveState();showMain()};
  $('saveProfile').onclick=()=>{saveState();showMain()};
  $('editProfile').onclick=()=>showSetup();
  $('resetApp').onclick=()=>{localStorage.removeItem(STORAGE_KEY);localStorage.removeItem(OLD_STORAGE_KEY);location.reload()};
  bindSingle('timeOptions','data-time','time');
  bindSingle('priorityOptions','data-priority','priority');
  bindMulti('costOptions',state.costs);bindMulti('weightOptions',state.weights);
  $('recommendBtn').onclick=recommend;$('anotherFood').onclick=anotherFood;$('acceptFood').onclick=acceptCurrent;
  $('clearHistory').onclick=()=>{state.history=[];saveState();renderHistory();toast('تاریخچه پاک شد')};
}

async function boot(){
  try{const response=await fetch('./data/foods.json',{cache:'no-store'});if(!response.ok)throw new Error('catalog');FOODS=await response.json();CATEGORIES=[...new Set(FOODS.map(f=>f.category))];renderCategoryFilters();bindEvents();if(loadState())showMain();else showSetup();}
  catch(error){console.error(error);document.body.innerHTML='<main class="app-shell"><section class="card"><h2>کاتالوگ غذا بارگذاری نشد</h2><p>صفحه را یک بار Refresh کن.</p></section></main>'}
}

boot();
