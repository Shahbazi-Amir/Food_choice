import test from'node:test';import assert from'node:assert/strict';import{scaleIngredients,countTags,scoreMeal,healthNudge,weekEntries}from'../js/recommender.js';
const meals=[{id:'fish',tags:['fish','healthy'],minutes:30,cost:3},{id:'meat',tags:['red_meat'],minutes:60,cost:4},{id:'lentil',tags:['legume','budget'],minutes:40,cost:1}],now=new Date('2026-08-25T12:00:00Z');
test('scales ingredients by people count',()=>assert.deepEqual(scaleIngredients([['برنج',4,'پیمانه']],2),[{name:'برنج',amount:2,unit:'پیمانه'}]));
test('weekEntries excludes meals older than seven days',()=>{const h=[{mealId:'fish',cookedAt:'2026-08-24T12:00:00Z'},{mealId:'meat',cookedAt:'2026-08-10T12:00:00Z'}];assert.equal(weekEntries(h,now).length,1)});
test('counts weekly meal tags',()=>assert.equal(countTags([{mealId:'fish',cookedAt:'2026-08-24T12:00:00Z'}],meals,now).fish,1));
test('fish gets a diversity boost when absent this week',()=>{const h=[{mealId:'meat',cookedAt:'2026-08-24T12:00:00Z'}];assert.ok(scoreMeal(meals[0],h,meals,'default',now)>scoreMeal(meals[1],h,meals,'default',now))});
test('health nudge prefers fish when none exists in the week',()=>assert.match(healthNudge([{mealId:'meat',cookedAt:'2026-08-24T12:00:00Z'}],meals,now),/ماهی/));
