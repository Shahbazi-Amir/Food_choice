export function totalMinutes(food){return Number(food.prep||0)+Number(food.cook||0)}
export function formatMinutes(minutes){const value=Number(minutes||0);if(value<60)return `${value} دقیقه`;const h=Math.floor(value/60),m=value%60;return m?`${h} ساعت و ${m} دقیقه`:`${h} ساعت`}
const COST_ORDER=['اقتصادی','معمولی','گران'];
const WEIGHT_ORDER=['سبک','متوسط','سنگین'];
function minDistance(value,selected,order){if(!selected?.length)return 0;const index=order.indexOf(value);return Math.min(...selected.map(item=>Math.abs(index-order.indexOf(item))))}
function timeLimit(time){return time==='any'||time==null?null:Number(time)}

export function buildCandidatePool(foods,usualNames,tryNames,{allowTry=true}={}){
 const usual=new Set(usualNames||[]),tries=new Set(tryNames||[]);
 const pool=foods.filter(food=>usual.has(food.name)||(allowTry&&tries.has(food.name)));
 return pool.map(food=>({...food,_source:usual.has(food.name)?'usual':'try'}));
}
function semanticMatch(food,prefs){
 const families=[...(prefs.families||prefs.categories||[])];
 const methods=[...(prefs.methods||[])];
 const familyOk=!families.length||families.includes(food.family);
 const methodOk=!methods.length||methods.some(m=>(food.methods||[]).includes(m));
 return {familyOk,methodOk,exact:familyOk&&methodOk};
}
function semanticCandidates(foods,prefs,priority){
 const families=[...(prefs.families||prefs.categories||[])], methods=[...(prefs.methods||[])];
 if(!families.length&&!methods.length)return {foods,relaxed:[]};
 const exact=foods.filter(f=>semanticMatch(f,prefs).exact);
 if(exact.length)return {foods:exact,relaxed:[]};
 if(families.length&&methods.length){
   if(priority==='category'){
     const familyOnly=foods.filter(f=>semanticMatch(f,{families}).familyOk);
     if(familyOnly.length)return {foods:familyOnly,relaxed:['روش پخت']};
   }
   const methodOnly=foods.filter(f=>semanticMatch(f,{methods}).methodOk);
   if(methodOnly.length)return {foods:methodOnly,relaxed:['نوع غذا']};
   const familyOnly=foods.filter(f=>semanticMatch(f,{families}).familyOk);
   if(familyOnly.length)return {foods:familyOnly,relaxed:['روش پخت']};
 }
 if(methods.length){const methodOnly=foods.filter(f=>semanticMatch(f,{methods}).methodOk);if(methodOnly.length)return {foods:methodOnly,relaxed:[]};}
 if(families.length){const familyOnly=foods.filter(f=>semanticMatch(f,{families}).familyOk);if(familyOnly.length)return {foods:familyOnly,relaxed:[]};}
 return {foods:[],relaxed:[]};
}

export function scoreFood(food,prefs={},priority='balanced',history=[]){
 const multiplier=key=>priority===key?4:1;
 let score=food._source==='usual'?70:food._source==='try'?30:food._source==='catalog-fallback'?18:0;
 const misses=[];const matches=[];
 const limit=timeLimit(prefs.time);
 if(limit){const over=totalMinutes(food)-limit;if(over<=0){score+=24*multiplier('time');matches.push('زمان');}else{score-=Math.min(70,8+(over/10)*5)*multiplier('time');misses.push(`${formatMinutes(over)} بیشتر از زمان دلخواه`);}}
 const costs=[...(prefs.costs||[])];
 if(costs.length){if(costs.includes(food.cost)){score+=20*multiplier('cost');matches.push('هزینه');}else{const d=minDistance(food.cost,costs,COST_ORDER);score-=(10+10*d)*multiplier('cost');misses.push(`هزینه ${food.cost}`);}}
 const weights=[...(prefs.weights||[])];
 if(weights.length){if(weights.includes(food.weight)){score+=20*multiplier('weight');matches.push('سبکی/سنگینی');}else{const d=minDistance(food.weight,weights,WEIGHT_ORDER);score-=(8+9*d)*multiplier('weight');misses.push(`${food.weight} است`);}}
 const recent=history.map(item=>typeof item==='string'?item:item.name).slice(0,6);const pos=recent.indexOf(food.name);if(pos===0)score-=60;else if(pos>0&&pos<3)score-=32;else if(pos>=3)score-=12;
 return {...food,_score:score,_misses:misses,_matches:matches,_exact:misses.length===0};
}

export function rankFoods(foods,usualNames,tryNames,prefs={},priority='balanced',history=[]){
 const userPool=buildCandidatePool(foods,usualNames,tryNames,{allowTry:prefs.allowTry!==false});
 let sem=semanticCandidates(userPool,prefs,priority);let sourcePool=sem.foods;
 if(!sourcePool.length){
   const catalog=foods.map(food=>({...food,_source:'catalog-fallback'}));
   sem=semanticCandidates(catalog,prefs,priority);sourcePool=sem.foods;
 }
 if(!sourcePool.length) sourcePool=userPool.length?userPool:foods.map(food=>({...food,_source:'catalog-fallback'}));
 return sourcePool.map(food=>({...scoreFood(food,prefs,priority,history),_semanticRelaxations:sem.relaxed}))
  .sort((a,b)=>b._score-a._score||totalMinutes(a)-totalMinutes(b)||a.name.localeCompare(b.name,'fa'));
}
export function fitMessage(food){
 if(!food)return '';
 const relaxed=(food._semanticRelaxations||[]).length?` برای پیدا کردن گزینه، ${food._semanticRelaxations.join(' و ')} کمی آزاد شد.`:'';
 if(food._exact&&!relaxed)return food._source==='catalog-fallback'?'✨ گزینه سازگار پیدا شد، ولی خارج از غذاهای معمول/انتخابی توست.':'✅ با انتخاب‌های امروزت جور است.';
 const details=food._misses.slice(0,2).join('، ');
 return `🔎 نزدیک‌ترین پیشنهاد است${details?`؛ ${details}`:''}.${relaxed}`;
}
