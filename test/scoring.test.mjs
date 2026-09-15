import test from 'node:test';
import assert from 'node:assert/strict';
import {buildCandidatePool,formatMinutes,rankFoods} from '../js/scoring.js';

const foods=[
 {name:'آشنا کند',category:'خورش',weight:'سنگین',cost:'گران',prep:20,cook:80},
 {name:'آشنا سریع',category:'خوراک',weight:'سبک',cost:'اقتصادی',prep:10,cook:25},
 {name:'غریبه عالی',category:'خوراک',weight:'سبک',cost:'اقتصادی',prep:5,cook:15},
 {name:'جدید منتخب',category:'خوراک',weight:'سبک',cost:'اقتصادی',prep:10,cook:30},
];

test('formatMinutes shows hours and minutes',()=>assert.equal(formatMinutes(110),'1 ساعت و 50 دقیقه'));

test('catalog foods outside usual/try are excluded from user pool',()=>{
 const pool=buildCandidatePool(foods,new Set(['آشنا کند','آشنا سریع']),new Set(['جدید منتخب']),{allowTry:true});
 assert.deepEqual(pool.map(x=>x.name).sort(),['آشنا سریع','آشنا کند','جدید منتخب'].sort());
});

test('no exact match still returns nearest option',()=>{
 const ranked=rankFoods(foods,new Set(['آشنا کند','آشنا سریع']),new Set(),{time:'20',costs:['اقتصادی'],weights:['سبک'],categories:['خورش'],allowTry:false},'time',[]);
 assert.ok(ranked.length>0);
 assert.equal(ranked[0].name,'آشنا سریع');
 assert.equal(ranked[0]._exact,false);
});

test('priority changes ranking weight',()=>{
 const usual=new Set(['آشنا کند','آشنا سریع']);
 const prefs={time:'40',costs:['اقتصادی'],weights:[],categories:['خورش'],allowTry:false};
 const byTime=rankFoods(foods,usual,new Set(),prefs,'time',[]);
 const byCategory=rankFoods(foods,usual,new Set(),prefs,'category',[]);
 assert.equal(byTime[0].name,'آشنا سریع');
 assert.equal(byCategory[0].name,'آشنا کند');
});

test('most recent meal is penalized',()=>{
 const usual=new Set(['آشنا کند','آشنا سریع']);
 const ranked=rankFoods(foods,usual,new Set(),{time:'any',allowTry:false},'balanced',[{name:'آشنا سریع'}]);
 assert.equal(ranked[0].name,'آشنا کند');
});
