import test from 'node:test';
import assert from 'node:assert/strict';
import {buildCandidatePool,formatMinutes,rankFoods} from '../js/scoring.js';
import {recipeFor} from '../js/recipe.js';

const foods=[
 {name:'خورش آشنا',family:'خورش و قلیه',methods:['خورشتی/آرام‌پز'],weight:'سنگین',cost:'گران',prep:20,cook:80,ingredients:['گوشت','پیاز']},
 {name:'کوکو آشنا',family:'کوکو و املت',methods:['تابه‌ای','فر/تنوری'],weight:'سبک',cost:'اقتصادی',prep:10,cook:25,ingredients:['تخم‌مرغ','سبزی']},
 {name:'جوجه گریل جدید',family:'کباب، بریان و تنوری',methods:['گریل/منقل'],weight:'متوسط',cost:'معمولی',prep:15,cook:25,ingredients:['مرغ','پیاز']},
 {name:'برگر گریل منتخب',family:'ساندویچ و غذای سریع',methods:['گریل/منقل','تابه‌ای'],weight:'سنگین',cost:'معمولی',prep:10,cook:20,ingredients:['گوشت','نان']},
];

test('formatMinutes shows hours and minutes',()=>assert.equal(formatMinutes(110),'1 ساعت و 50 دقیقه'));

test('catalog foods outside usual/try are excluded from basic user pool',()=>{
 const pool=buildCandidatePool(foods,new Set(['خورش آشنا','کوکو آشنا']),new Set(['برگر گریل منتخب']),{allowTry:true});
 assert.deepEqual(pool.map(x=>x.name).sort(),['خورش آشنا','کوکو آشنا','برگر گریل منتخب'].sort());
});

test('grill never returns kuku merely because time fits',()=>{
 const ranked=rankFoods(foods,new Set(['کوکو آشنا']),new Set(),{time:'60',methods:['گریل/منقل'],allowTry:false},'time',[]);
 assert.ok(ranked.length>0);
 assert.notEqual(ranked[0].name,'کوکو آشنا');
 assert.ok(ranked[0].methods.includes('گریل/منقل'));
 assert.equal(ranked[0]._source,'catalog-fallback');
});

test('semantic method constraint is preserved over soft time/cost preferences',()=>{
 const ranked=rankFoods(foods,new Set(['کوکو آشنا']),new Set(['برگر گریل منتخب']),{time:'20',costs:['اقتصادی'],methods:['گریل/منقل'],allowTry:true},'time',[]);
 assert.equal(ranked[0].name,'برگر گریل منتخب');
 assert.ok(ranked[0].methods.includes('گریل/منقل'));
});

test('family filter only yields compatible family when available',()=>{
 const ranked=rankFoods(foods,new Set(['خورش آشنا','کوکو آشنا']),new Set(),{families:['خورش و قلیه'],time:'30',allowTry:false},'time',[]);
 assert.equal(ranked[0].name,'خورش آشنا');
});

test('recipe payload always includes ingredients-compatible steps and variants',()=>{
 const food={name:'کوکو سبزی',family:'کوکو و املت',methods:['تابه‌ای','فر/تنوری'],ingredients:['سبزی کوکو','تخم‌مرغ']};
 const recipe=recipeFor(food);
 assert.ok(recipe.steps.length>=3);
 assert.equal(recipe.variants.length,2);
 assert.ok(recipe.notes.length>=1);
});

test('most recent meal is penalized among compatible candidates',()=>{
 const usual=new Set(['خورش آشنا','کوکو آشنا']);
 const ranked=rankFoods(foods,usual,new Set(),{time:'any',allowTry:false},'balanced',[{name:'کوکو آشنا'}]);
 assert.equal(ranked[0].name,'خورش آشنا');
});
