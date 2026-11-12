import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const root=process.cwd();
const evidence=path.join(root,'evidence');
await fs.mkdir(evidence,{recursive:true});
const data=JSON.parse(await fs.readFile(path.join(root,'results/dashboard_groups.json'),'utf8'));
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});
const errors=[];page.on('pageerror',e=>errors.push(String(e)));
const loads=[];
for(let i=0;i<5;i++){
 await page.goto('http://127.0.0.1:8501/',{waitUntil:'load'});
 await page.waitForSelector('body[data-ready="true"]');
 loads.push(await page.evaluate(()=>performance.now()));
}
const checks=[];
for(const smoker of ['all','no','yes']) for(const dim of ['bmi','age','region','children']){
 await page.locator('#smoker').selectOption(smoker);
 await page.locator('#dimension').selectOption(dim);
 const groups=data.comparisons[smoker][dim].filter(x=>x.n>=5);
 assert.equal(await page.locator('#detail tr').count(),groups.length);
 const n=groups.reduce((a,g)=>a+g.n,0);
 const shown=await page.locator('#count').innerText();
 assert.equal(Number(shown.replace(/\D/g,'')),n);
 assert.equal(await page.locator('#chart .bar').count(),2*groups.length);
 const avg=groups.reduce((a,g)=>a+g.charges_sum,0)/n;
 const displayed=Number((await page.locator('#observed').innerText()).replace(/\D/g,''));
 assert.equal(displayed,Math.round(avg));
 checks.push({smoker,dimension:dim,n,groups:groups.length,counts_match:true,weighted_mean_matches:true});
}
await page.locator('#smoker').selectOption('all');await page.locator('#dimension').selectOption('bmi');
await page.screenshot({path:path.join(evidence,'dashboard_desktop.png'),fullPage:true});
const mobile=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
await mobile.goto('http://127.0.0.1:8501/');await mobile.waitForSelector('body[data-ready="true"]');
await mobile.locator('#smoker').selectOption('yes');
const overflow=await mobile.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);
assert.equal(overflow,false);
await mobile.screenshot({path:path.join(evidence,'dashboard_mobile.png'),fullPage:true});
assert.equal(errors.length,0);assert.ok(Math.max(...loads)<3000);
const result={executed_at:new Date().toISOString(),timezone:'America/Santiago',environment:'Chromium headless local, HTTP 127.0.0.1, sin red externa',desktop:{width:1440,height:1100},mobile:{width:390,height:844,horizontal_document_overflow:overflow},load_measurement:'performance.now después de load y render sin red, 5 navegaciones de esta sesión; no prueba de producción',load_ms:loads,max_load_ms:Math.max(...loads),passes_under_3s:true,filter_checks:checks,javascript_errors:errors,limitations:'Viewport móvil emulado. No se probó un teléfono físico ni una conexión de producción.'};
await fs.writeFile(path.join(evidence,'dashboard_validation.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify({max_load_ms:result.max_load_ms,combinations_tested:checks.length,mobile_overflow:overflow,errors}));
await browser.close();
