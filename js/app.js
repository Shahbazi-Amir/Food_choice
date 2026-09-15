const FOODS=[
{name:'عدس‌پلو',category:'پلو و چلو',weight:'متوسط',cost:'اقتصادی',prep:20,cook:40,ingredients:['برنج','عدس','پیاز','کشمش']},
{name:'لوبیاپلو',category:'پلو و چلو',weight:'سنگین',cost:'معمولی',prep:30,cook:55,ingredients:['برنج','لوبیا سبز','گوشت چرخ‌کرده','پیاز','رب']},
{name:'زرشک‌پلو با مرغ',category:'پلو و چلو',weight:'سنگین',cost:'معمولی',prep:25,cook:60,ingredients:['برنج','مرغ','زرشک','پیاز','زعفران']},
{name:'سبزی‌پلو با ماهی',category:'پلو و چلو',weight:'متوسط',cost:'گران',prep:30,cook:50,ingredients:['برنج','سبزی پلویی','ماهی','لیمو']},
{name:'استانبولی پلو',category:'پلو و چلو',weight:'متوسط',cost:'اقتصادی',prep:20,cook:40,ingredients:['برنج','سیب‌زمینی','گوجه','پیاز']},
{name:'دمپختک',category:'پلو و چلو',weight:'متوسط',cost:'اقتصادی',prep:15,cook:40,ingredients:['برنج','باقالی زرد','پیاز']},
{name:'رشته‌پلو',category:'پلو و چلو',weight:'متوسط',cost:'معمولی',prep:20,cook:45,ingredients:['برنج','رشته پلویی','کشمش','پیاز']},
{name:'قورمه‌سبزی',category:'خورش',weight:'سنگین',cost:'معمولی',prep:35,cook:130,ingredients:['گوشت خورشتی','سبزی قورمه','لوبیا','لیموعمانی']},
{name:'قیمه',category:'خورش',weight:'سنگین',cost:'معمولی',prep:25,cook:100,ingredients:['گوشت خورشتی','لپه','پیاز','رب','لیموعمانی']},
{name:'فسنجان',category:'خورش',weight:'سنگین',cost:'گران',prep:25,cook:120,ingredients:['مرغ','گردو','رب انار']},
{name:'خورش کرفس',category:'خورش',weight:'متوسط',cost:'معمولی',prep:35,cook:100,ingredients:['گوشت خورشتی','کرفس','نعنا','جعفری']},
{name:'خورش بادمجان',category:'خورش',weight:'سنگین',cost:'معمولی',prep:35,cook:90,ingredients:['گوشت خورشتی','بادمجان','گوجه','پیاز']},
{name:'آش رشته',category:'آش و سوپ',weight:'سنگین',cost:'اقتصادی',prep:35,cook:85,ingredients:['حبوبات','سبزی آش','رشته آش','کشک']},
{name:'آش جو',category:'آش و سوپ',weight:'متوسط',cost:'اقتصادی',prep:25,cook:75,ingredients:['جو','حبوبات','سبزی آش']},
{name:'سوپ جو و سبزیجات',category:'آش و سوپ',weight:'سبک',cost:'اقتصادی',prep:20,cook:40,ingredients:['جو','هویج','قارچ','کرفس']},
{name:'سوپ مرغ',category:'آش و سوپ',weight:'سبک',cost:'معمولی',prep:20,cook:50,ingredients:['مرغ','هویج','سیب‌زمینی','رشته سوپ']},
{name:'عدسی',category:'آش و سوپ',weight:'سبک',cost:'اقتصادی',prep:10,cook:40,ingredients:['عدس','پیاز','سیب‌زمینی']},
{name:'میرزا قاسمی',category:'غذای نانی و خوراک',weight:'سبک',cost:'اقتصادی',prep:25,cook:30,ingredients:['بادمجان','گوجه','تخم‌مرغ','سیر']},
{name:'کشک بادمجان',category:'غذای نانی و خوراک',weight:'متوسط',cost:'اقتصادی',prep:30,cook:35,ingredients:['بادمجان','کشک','پیاز','نعنا']},
{name:'خوراک لوبیا',category:'غذای نانی و خوراک',weight:'متوسط',cost:'اقتصادی',prep:15,cook:70,ingredients:['لوبیا چیتی','پیاز','رب']},
{name:'خوراک مرغ و سبزیجات',category:'غذای نانی و خوراک',weight:'سبک',cost:'معمولی',prep:20,cook:30,ingredients:['مرغ','فلفل دلمه','هویج','کدو']},
{name:'کوکو سبزی',category:'کوکو، کتلت و تخم‌مرغی',weight:'سبک',cost:'اقتصادی',prep:15,cook:20,ingredients:['سبزی کوکو','تخم‌مرغ','گردو']},
{name:'کوکو سیب‌زمینی',category:'کوکو، کتلت و تخم‌مرغی',weight:'متوسط',cost:'اقتصادی',prep:20,cook:25,ingredients:['سیب‌زمینی','تخم‌مرغ','پیاز']},
{name:'کتلت',category:'کوکو، کتلت و تخم‌مرغی',weight:'سنگین',cost:'معمولی',prep:25,cook:30,ingredients:['گوشت چرخ‌کرده','سیب‌زمینی','پیاز','تخم‌مرغ']},
{name:'املت گوجه',category:'کوکو، کتلت و تخم‌مرغی',weight:'سبک',cost:'اقتصادی',prep:10,cook:15,ingredients:['تخم‌مرغ','گوجه','پیاز']},
{name:'نرگسی اسفناج',category:'کوکو، کتلت و تخم‌مرغی',weight:'سبک',cost:'اقتصادی',prep:15,cook:20,ingredients:['اسفناج','تخم‌مرغ','پیاز']},
{name:'ماکارونی',category:'پاستا',weight:'سنگین',cost:'معمولی',prep:20,cook:45,ingredients:['ماکارونی','گوشت چرخ‌کرده','پیاز','رب']},
{name:'لازانیا',category:'پاستا',weight:'سنگین',cost:'گران',prep:35,cook:45,ingredients:['لازانیا','گوشت چرخ‌کرده','پنیر','قارچ']},
{name:'پاستا مرغ و قارچ',category:'پاستا',weight:'متوسط',cost:'معمولی',prep:20,cook:30,ingredients:['پاستا','مرغ','قارچ','شیر']},
{name:'فلافل خانگی',category:'ساندویچ و فست‌فود خانگی',weight:'متوسط',cost:'اقتصادی',prep:25,cook:20,ingredients:['نخود','پیاز','سیر','نان']},
{name:'الویه',category:'ساندویچ و فست‌فود خانگی',weight:'سنگین',cost:'معمولی',prep:30,cook:35,ingredients:['مرغ','سیب‌زمینی','تخم‌مرغ','خیارشور']},
{name:'ساندویچ مرغ',category:'ساندویچ و فست‌فود خانگی',weight:'متوسط',cost:'معمولی',prep:20,cook:25,ingredients:['مرغ','نان','کاهو','گوجه']},
{name:'همبرگر خانگی',category:'ساندویچ و فست‌فود خانگی',weight:'سنگین',cost:'معمولی',prep:20,cook:20,ingredients:['گوشت چرخ‌کرده','نان برگر','پیاز','گوجه']},
{name:'پیتزای خانگی',category:'ساندویچ و فست‌فود خانگی',weight:'سنگین',cost:'گران',prep:35,cook:25,ingredients:['خمیر پیتزا','پنیر','قارچ','فلفل دلمه']},
{name:'ساندویچ تخم‌مرغ و سیب‌زمینی',category:'ساندویچ و فست‌فود خانگی',weight:'متوسط',cost:'اقتصادی',prep:15,cook:20,ingredients:['تخم‌مرغ','سیب‌زمینی','نان']},
{name:'دلمه فلفل',category:'غذای نانی و خوراک',weight:'متوسط',cost:'معمولی',prep:35,cook:55,ingredients:['فلفل دلمه','برنج','لپه','سبزی دلمه']},
{name:'کباب تابه‌ای',category:'غذای نانی و خوراک',weight:'سنگین',cost:'معمولی',prep:20,cook:30,ingredients:['گوشت چرخ‌کرده','پیاز','گوجه']},
{name:'جوجه تابه‌ای',category:'غذای نانی و خوراک',weight:'متوسط',cost:'معمولی',prep:20,cook:30,ingredients:['مرغ','پیاز','لیمو']},
{name:'خوراک نخود و سبزیجات',category:'غذای نانی و خوراک',weight:'سبک',cost:'اقتصادی',prep:15,cook:35,ingredients:['نخود پخته','گوجه','فلفل دلمه','پیاز']},
{name:'سمبوسه خانگی',category:'ساندویچ و فست‌فود خانگی',weight:'متوسط',cost:'اقتصادی',prep:25,cook:20,ingredients:['نان لواش','سیب‌زمینی','سبزی','پیاز']}
];

const CATEGORIES=[...new Set(FOODS.map(f=>f.category))];
const DEFAULT_USUAL=new Set(['قورمه‌سبزی','قیمه','زرشک‌پلو با مرغ','عدس‌پلو','ماکارونی','کتلت','کوکو سبزی','املت گوجه']);
const STORAGE_KEY='food-choice-browser-prototype-v1';
const $=id=>document.getElementById(id);
const state={usual:new Set(),tryFoods:new Set(),people:4,time:'any',costs:new Set(),weights:new Set(),categories:new Set(),current:null,lastPool:[],history:[]};

function total(food){return food.prep+food.cook}
function formatMinutes(minutes){if(minutes<60)return`${minutes} دقیقه`;const h=Math.floor(minutes/60),m=minutes%60;return m?`${h} ساعت و ${m} دقیقه`:`${h} ساعت`}
function saveState(){localStorage.setItem(STORAGE_KEY,JSON.stringify({usual:[...state.usual],tryFoods:[...state.tryFoods],people:state.people,history:state.history}))}
function loadState(){try{const saved=JSON.parse(localStorage.getItem(STORAGE_KEY)||'null');if(!saved)return false;state.usual=new Set(saved.usual||[]);state.tryFoods=new Set(saved.tryFoods||[]);state.people=saved.people||4;state.history=saved.history||[];return state.usual.size>=3}catch{return false}}
function toast(msg){const el=$('toast');el.textContent=msg;el.classList.add('show');clearTimeout(toast.t);toast.t=setTimeout(()=>el.classList.remove('show'),1900)}
function show(id){$(id).classList.remove('hidden')}function hide(id){$(id).classList.add('hidden')}

function renderUsualFoods(){const box=$('usualFoodGroups');box.innerHTML='';for(const category of CATEGORIES){const group=document.createElement('div');group.className='food-group';group.innerHTML=`<div class="food-group-title">${category}</div><div class="food-chips"></div>`;const chips=group.querySelector('.food-chips');FOODS.filter(f=>f.category===category).forEach(food=>{const b=document.createElement('button');b.type='button';b.className='food-chip'+(state.usual.has(food.name)?' selected':'');b.textContent=food.name;b.onclick=()=>{state.usual.has(food.name)?state.usual.delete(food.name):state.usual.add(food.name);b.classList.toggle('selected');hide('usualError')};chips.appendChild(b)});box.appendChild(group)}}
function renderPeople(){$('peopleCount').textContent=state.people;$('peopleLabel').textContent=`برای ${state.people} نفر`}
function suggestedNewFoods(){const picked=[];for(const category of CATEGORIES){const food=FOODS.find(f=>f.category===category&&!state.usual.has(f.name));if(food)picked.push(food)}for(const food of FOODS){if(picked.length>=12)break;if(!state.usual.has(food.name)&&!picked.some(x=>x.name===food.name))picked.push(food)}return picked.slice(0,12)}
function renderTryFoods(){const list=$('tryFoodList');list.innerHTML='';suggestedNewFoods().forEach(food=>{const b=document.createElement('button');b.type='button';b.className='try-card'+(state.tryFoods.has(food.name)?' selected':'');b.innerHTML=`${food.name}<small>${food.category} · ${food.weight}</small>`;b.onclick=()=>{state.tryFoods.has(food.name)?state.tryFoods.delete(food.name):state.tryFoods.add(food.name);b.classList.toggle('selected')};list.appendChild(b)})}
function renderCategoryFilters(){const box=$('categoryOptions');box.innerHTML='';CATEGORIES.forEach(cat=>{const b=document.createElement('button');b.type='button';b.className='choice';b.dataset.value=cat;b.textContent=cat;b.onclick=()=>toggleSetChoice(b,state.categories,cat);box.appendChild(b)})}
function toggleSetChoice(btn,set,value){set.has(value)?set.delete(value):set.add(value);btn.classList.toggle('active',set.has(value))}
function renderSummary(){$('profileSummary').textContent=`${state.usual.size} غذای معمول · ${state.tryFoods.size} غذای جدید · ${state.people} نفر`;renderHistory()}
function switchToMain(){hide('setupStep1');hide('setupStep2');show('mainScreen');show('resetApp');renderSummary()}
function startSetup(){show('setupStep1');hide('setupStep2');hide('mainScreen');hide('resetApp');renderUsualFoods();renderPeople()}

function candidateFoods(){const max=state.time==='any'?Infinity:Number(state.time);return FOODS.filter(f=>total(f)<=max&&(state.costs.size===0||state.costs.has(f.cost))&&(state.weights.size===0||state.weights.has(f.weight))&&(state.categories.size===0||state.categories.has(f.category)))}
function recentlyCooked(name){return state.history.slice(0,4).some(h=>h.name===name)}
function pickRecommendation(pool,excludeCurrent=false){if(!pool.length)return null;let candidates=pool.filter(f=>!excludeCurrent||f.name!==state.current?.name);if(!candidates.length)candidates=pool;const allowTry=$('allowTryFoods').checked;
  const scored=candidates.map(food=>{let score=10;let source='other';if(state.usual.has(food.name)){score+=28;source='usual'}if(allowTry&&state.tryFoods.has(food.name)){score+=6;source='try'}if(state.tryFoods.has(food.name)&&!allowTry)score-=100;if(recentlyCooked(food.name))score-=18;return{food,score,source}}).filter(x=>x.score>-50).sort((a,b)=>b.score-a.score);
  if(!scored.length)return null;const top=scored.slice(0,Math.min(6,scored.length));let roll=Math.random()*top.reduce((s,x)=>s+Math.max(1,x.score),0);for(const item of top){roll-=Math.max(1,item.score);if(roll<=0)return{...item.food,_source:item.source}}return{...top[0].food,_source:top[0].source}}
function recommend(exclude=false){const pool=candidateFoods();state.lastPool=pool;state.current=pickRecommendation(pool,exclude);if(!state.current){hide('resultCard');show('noResult');return}hide('noResult');renderResult(state.current);show('resultCard');$('resultCard').scrollIntoView({behavior:'smooth',block:'start'})}
function renderResult(food){$('foodName').textContent=food.name;$('prepTime').textContent=formatMinutes(food.prep);$('cookTime').textContent=formatMinutes(food.cook);$('totalTime').textContent=formatMinutes(total(food));$('peopleLabel').textContent=`حدود ${state.people} نفر`;$('foodBadges').innerHTML=`<span class="badge">${food.category}</span><span class="badge">${food.weight}</span><span class="badge">${food.cost}</span>`;$('ingredientsList').innerHTML=food.ingredients.map(i=>`<span>${i}</span>`).join('');const badge=$('sourceBadge');if(food._source==='try'){badge.textContent='✨ برای امتحان';badge.className='source-badge'}else if(food._source==='usual'){badge.textContent='🏠 از غذاهای معمول خودت';badge.className='source-badge usual'}else{badge.textContent='🍽️ از فهرست غذاها';badge.className='source-badge usual'}}
function renderHistory(){const card=$('historyCard'),list=$('historyList');if(!state.history.length){hide('historyCard');return}show('historyCard');list.innerHTML=state.history.slice(0,8).map(h=>`<div class="history-row"><strong>${h.name}</strong><small>${h.date}</small></div>`).join('')}
function acceptCurrent(){if(!state.current)return;const date=new Intl.DateTimeFormat('fa-IR',{month:'short',day:'numeric'}).format(new Date());state.history.unshift({name:state.current.name,date});state.history=state.history.slice(0,20);saveState();renderHistory();toast('در تاریخچه ثبت شد ✓')}

$('selectDefaults').onclick=()=>{state.usual=new Set(DEFAULT_USUAL);renderUsualFoods()};
$('clearUsual').onclick=()=>{state.usual.clear();renderUsualFoods()};
$('peopleMinus').onclick=()=>{state.people=Math.max(1,state.people-1);renderPeople()};
$('peoplePlus').onclick=()=>{state.people=Math.min(12,state.people+1);renderPeople()};
$('goToTryFoods').onclick=()=>{if(state.usual.size<3){show('usualError');return}hide('setupStep1');show('setupStep2');renderTryFoods()};
$('skipTryFoods').onclick=()=>{state.tryFoods.clear();saveState();switchToMain()};
$('saveProfile').onclick=()=>{saveState();switchToMain()};
$('editProfile').onclick=()=>{hide('mainScreen');hide('setupStep2');show('setupStep1');hide('resetApp');renderUsualFoods();renderPeople()};
$('resetApp').onclick=()=>{if(!confirm('انتخاب‌های ذخیره‌شده پاک شود و از اول شروع کنیم؟'))return;localStorage.removeItem(STORAGE_KEY);state.usual.clear();state.tryFoods.clear();state.history=[];state.people=4;state.current=null;startSetup()};
$('timeOptions').addEventListener('click',e=>{const b=e.target.closest('[data-time]');if(!b)return;state.time=b.dataset.time;document.querySelectorAll('[data-time]').forEach(x=>x.classList.toggle('active',x===b))});
$('costOptions').addEventListener('click',e=>{const b=e.target.closest('[data-value]');if(b)toggleSetChoice(b,state.costs,b.dataset.value)});
$('weightOptions').addEventListener('click',e=>{const b=e.target.closest('[data-value]');if(b)toggleSetChoice(b,state.weights,b.dataset.value)});
$('recommendBtn').onclick=()=>recommend(false);
$('anotherFood').onclick=()=>recommend(true);
$('acceptFood').onclick=acceptCurrent;
$('clearHistory').onclick=()=>{state.history=[];saveState();renderHistory();toast('تاریخچه پاک شد')};

renderCategoryFilters();
if(loadState())switchToMain();else startSetup();
