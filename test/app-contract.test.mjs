import test from'node:test';import assert from'node:assert/strict';import{readFile,access}from'node:fs/promises';
const html=await readFile(new URL('../index.html',import.meta.url),'utf8');
const app=await readFile(new URL('../js/app.js',import.meta.url),'utf8');
const manifest=JSON.parse(await readFile(new URL('../manifest.webmanifest',import.meta.url),'utf8'));

test('every app DOM lookup exists in index.html',()=>{const ids=[...app.matchAll(/\$\('([^']+)'\)/g)].map(match=>match[1]);for(const id of new Set(ids))assert.match(html,new RegExp(`id=["']${id}["']`),`missing #${id}`)});
test('manifest has installable identity and standalone mode',()=>{assert.equal(manifest.id,'./');assert.equal(manifest.start_url,'./');assert.equal(manifest.scope,'./');assert.equal(manifest.display,'standalone');assert.ok(manifest.icons.some(icon=>icon.sizes==='192x192'));assert.ok(manifest.icons.some(icon=>icon.sizes==='512x512'))});
test('manifest icon files exist',async()=>{for(const icon of manifest.icons)await access(new URL(`../${icon.src.replace(/^\.\//,'')}`,import.meta.url))});
test('mobile install metadata is present',()=>{assert.match(html,/apple-mobile-web-app-capable/);assert.match(html,/manifest\.webmanifest/)});
