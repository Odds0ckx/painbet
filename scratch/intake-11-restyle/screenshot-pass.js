const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = '/tmp/claude-0/-home-user-painbet/a8b1436e-c0f8-51e1-a987-d33b627a2081/scratchpad/shots';
const fs = require('fs');
fs.mkdirSync(path, { recursive: true });

(async () => {
  const b = await chromium.launch();
  const errs = [];
  const page = await b.newPage({ viewport: { width: 420, height: 900 }, deviceScaleFactor: 2 });
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });

  await page.goto('file:///home/user/painbet/painbet-intake-11-v2.html');
  await page.waitForTimeout(3500);
  await page.screenshot({ path: path + '/01-intro.png' });

  // skip the film
  await page.click('#skip');
  await page.waitForTimeout(1400);
  await page.screenshot({ path: path + '/02-cover.png', fullPage: true });

  // menu
  await page.click('#menuBtn');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path + '/03-menu.png' });
  await page.click('#menuClose');
  await page.waitForTimeout(300);

  // check in -> exam
  await page.click('#go');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path + '/04-exam.png', fullPage: true });

  // answer all five with the heaviest option to push the room to "other"
  for (let i = 0; i < 5; i++) {
    const opts = await page.$$('#opts .opt');
    await opts[0].click();
    await page.waitForTimeout(500);
  }
  await page.waitForTimeout(900);
  await page.screenshot({ path: path + '/05-diagnosis.png', fullPage: true });

  // claim -> giveaway station
  await page.click('#claim');
  await page.waitForTimeout(700);
  await page.screenshot({ path: path + '/06-giveaway.png', fullPage: true });

  // log a wallet
  await page.fill('#txh', '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa');
  await page.fill('#amt', '250');
  await page.fill('#casino', 'Rollchain');
  await page.click('#submitTx');
  await page.waitForTimeout(700);
  await page.screenshot({ path: path + '/07-entry-logged.png', fullPage: true });

  // discharge
  await page.click('#toQuiz');
  await page.waitForTimeout(600);
  await page.fill('#handle', '@painpatient');
  await page.fill('#pw', 'Str0ngPass!word');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path + '/08-discharge.png', fullPage: true });
  await page.click('#send');
  await page.waitForTimeout(900);
  await page.screenshot({ path: path + '/09-locker.png', fullPage: true });
  await page.click('#locker');
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path + '/10-locker-pried.png', fullPage: true });

  await page.click('#toExit');
  await page.waitForTimeout(800);
  await page.screenshot({ path: path + '/11-channels.png', fullPage: true });

  // dispensary
  await page.click('#wheelCard');
  await page.waitForTimeout(900);
  await page.screenshot({ path: path + '/12-dispensary-wheel.png', fullPage: true });
  await page.click('#wSpin');
  await page.waitForTimeout(5200);
  await page.screenshot({ path: path + '/13-spun.png', fullPage: true });

  // open every section of the dispensary
  for (const d of await page.$$('.sect')) { await d.evaluate(n => n.open = true); }
  await page.click('.wodds summary');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path + '/14-dispensary-all.png', fullPage: true });

  // chart
  await page.click('#fBack');
  await page.waitForTimeout(800);
  await page.screenshot({ path: path + '/15-chart.png', fullPage: true });

  // private ward
  await page.click('#dOut');
  await page.waitForTimeout(600);
  await page.click('#vipCard');
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path + '/16-private-ward.png', fullPage: true });

  // staff entrance
  await page.click('#vBack');
  await page.waitForTimeout(600);
  await page.click('#staffCard');
  await page.waitForTimeout(600);
  await page.click('[data-t="stream"]');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path + '/17-staff.png', fullPage: true });

  // login screen
  await page.click('#staffBack');
  await page.waitForTimeout(500);
  await page.click('#menuBtn');
  await page.waitForTimeout(300);
  await page.click('#loginLink');
  await page.waitForTimeout(600);
  await page.screenshot({ path: path + '/18-login.png', fullPage: true });

  // desktop pass
  const d2 = await b.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  await d2.goto('file:///home/user/painbet/painbet-intake-11-v2.html');
  await d2.waitForTimeout(3000);
  await d2.click('#skip');
  await d2.waitForTimeout(1200);
  await d2.screenshot({ path: path + '/19-desktop-cover.png' });

  // horizontal overflow check
  const ov = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  console.log('horizontal overflow px:', ov);
  console.log(errs.length ? errs.join('\n') : 'no console/page errors');
  await b.close();
})();
