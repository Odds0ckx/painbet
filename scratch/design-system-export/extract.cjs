// Captures every view/modal/sheet/component state out of the live index.html into
// frames.json, for assemble.py to turn into painbet-design-system.html. Re-run both
// scripts (in this order) any time index.html's screens/popups change.
//
// Requires Playwright (this repo's dev environment has it at the path below; adjust
// if running elsewhere) and Chromium.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const REPO_ROOT = path.resolve(__dirname, '..', '..');
const OUT = path.join(__dirname, 'frames.json');
const filePath = 'file://' + path.join(REPO_ROOT, 'index.html');

async function captureClean(page, sel) {
  return page.evaluate((sel) => {
    const src = document.querySelector(sel);
    if (!src) return '';
    const clone = src.cloneNode(true);
    clone.querySelectorAll('[style*="display:none"], [style*="display: none"]').forEach(n => n.remove());
    return clone.outerHTML;
  }, sel);
}

(async () => {
  const browser = await chromium.launch();
  const frames = [];

  // ---------- desktop pass ----------
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    await page.goto(filePath);
    await page.waitForTimeout(400);
    await page.evaluate(() => {
      document.body.classList.add('signedIn');
      const m = document.getElementById('auth-modal'); if (m) m.classList.remove('on');
      window.openAuth = () => {};
    });

    // chrome: sidebar casino (mode-seg highlight is also body[data-mode]-driven, force it inline)
    await page.evaluate(() => setMode('casino'));
    await page.waitForTimeout(150);
    await page.evaluate(() => {
      const seg = document.querySelector('.mode-seg[data-mode="casino"]');
      if (seg) { seg.style.background = 'var(--red)'; seg.style.color = '#fff'; }
    });
    frames.push({ id:'chrome-sidebar-casino', label:'Sidebar — Casino mode', kind:'chrome-vertical',
      html: await captureClean(page, '.sidebar') });

    // chrome: sidebar sports
    // the sb-casino/sb-sports toggle is driven by a CSS rule keyed off body[data-mode],
    // which the standalone export document doesn't carry — force the equivalent inline
    // styles onto this specific capture so it renders correctly out of context
    await page.evaluate(() => setMode('sports'));
    await page.waitForTimeout(150);
    await page.evaluate(() => {
      document.querySelectorAll('.sidebar .sb-casino').forEach(el => el.style.display = 'none');
      document.querySelectorAll('.sidebar .sb-sports').forEach(el => el.style.display = 'block');
      const seg = document.querySelector('.mode-seg[data-mode="sports"]');
      if (seg) { seg.style.background = 'var(--red)'; seg.style.color = '#fff'; }
    });
    frames.push({ id:'chrome-sidebar-sports', label:'Sidebar — Sports mode', kind:'chrome-vertical',
      html: await captureClean(page, '.sidebar') });
    await page.evaluate(() => {
      document.querySelectorAll('.sidebar .sb-casino').forEach(el => el.style.display = '');
      document.querySelectorAll('.sidebar .sb-sports').forEach(el => el.style.display = '');
    });

    // chrome: topbar + ticker
    frames.push({ id:'chrome-topbar', label:'Topbar', kind:'chrome-horizontal',
      html: await captureClean(page, '.topbar') });
    frames.push({ id:'chrome-ticker', label:'Live relief ticker', kind:'chrome-horizontal',
      html: await captureClean(page, '.ticker') });

    // views
    const views = ['home','painscale','rails','pk','anesthesia','affiliate','support','games','provider','promos','arcade','synapse','sports'];
    for (const v of views) {
      await page.evaluate((v) => show(v), v);
      if (v === 'provider') {
        await page.evaluate(() => openProvider('Pragmatic Play','PP',null));
      }
      await page.waitForTimeout(350);
      const html = await captureClean(page, '#view-'+v);
      frames.push({ id:'view-'+v, label:'View — '+v, kind:'view', html });
    }

    // modals (uniform openModal pattern, single state)
    const modals = ['providers-modal','community-modal','apply-modal','chat-modal','ginfo-modal','account-modal'];
    for (const id of modals) {
      await page.evaluate((id) => { document.querySelectorAll('.modal-bg.on').forEach(m=>m.classList.remove('on')); }, id);
      if (id === 'ginfo-modal') {
        await page.evaluate(() => {
          document.getElementById('gi-title').textContent='Sweet Bonanza';
          document.getElementById('gi-prov').textContent='Pragmatic Play';
          document.getElementById('gi-cats').textContent='Slots · Popular';
        });
      }
      await page.evaluate((id) => openModal(id), id);
      await page.waitForTimeout(200);
      const html = await captureClean(page, '#'+id);
      frames.push({ id, label:'Modal — '+id.replace('-modal',''), kind:'modal', html });
      await page.evaluate((id) => document.getElementById(id).classList.remove('on'), id);
    }

    // legal modal, every tab
    const legalTabs = ['terms','privacy','aml','fair','rg'];
    for (const tab of legalTabs) {
      await page.evaluate((tab) => openLegal(tab), tab);
      await page.waitForTimeout(150);
      const html = await captureClean(page, '#legal-modal');
      frames.push({ id:'legal-modal-'+tab, label:'Modal — legal ('+tab+')', kind:'modal', html });
      await page.evaluate(() => document.getElementById('legal-modal').classList.remove('on'));
    }

    // auth modal, login + register
    await page.evaluate(() => { document.body.classList.remove('signedIn'); });
    await page.evaluate(() => { document.getElementById('auth-modal').classList.add('on'); });
    await page.waitForTimeout(200);
    frames.push({ id:'auth-modal-login', label:'Modal — sign in (login)', kind:'modal', html: await captureClean(page, '#auth-modal') });
    await page.evaluate(() => {
      document.getElementById('ab-login').style.display='none';
      document.getElementById('ab-register').style.display='block';
      document.querySelectorAll('.mtabs [data-atab]').forEach(b=>b.classList.toggle('active', b.dataset.atab==='register'));
    });
    await page.waitForTimeout(150);
    frames.push({ id:'auth-modal-register', label:'Modal — sign in (register)', kind:'modal', html: await captureClean(page, '#auth-modal') });
    await page.evaluate(() => { document.getElementById('auth-modal').classList.remove('on'); document.body.classList.add('signedIn'); });

    // wallet modal, every tab
    const walletTabs = ['dep','wd','pk'];
    for (const tab of walletTabs) {
      await page.evaluate((tab) => openWallet(tab), tab);
      await page.waitForTimeout(150);
      const html = await captureClean(page, '#wallet-modal');
      frames.push({ id:'wallet-modal-'+tab, label:'Modal — wallet ('+tab+')', kind:'modal', html });
      await page.evaluate(() => closeWallet());
    }

    // game-modal (gmodal, arcade launcher chrome)
    await page.evaluate(() => { document.getElementById('game-modal').classList.add('on'); });
    await page.waitForTimeout(150);
    frames.push({ id:'game-modal', label:'Modal — arcade launcher', kind:'gmodal', html: await captureClean(page, '#game-modal') });
    await page.evaluate(() => { document.getElementById('game-modal').classList.remove('on'); });

    // components swatch: pull representative live elements into one labeled gallery
    await page.evaluate(() => show('home'));
    await page.waitForTimeout(150);
    const swatchHtml = await page.evaluate(() => {
      const grab = (sel) => { const el = document.querySelector(sel); return el ? el.cloneNode(true) : null; };
      const row = (title, els) => {
        const wrap = document.createElement('div');
        wrap.className = 'swatch-row';
        const h = document.createElement('div'); h.className='swatch-title'; h.textContent = title;
        wrap.appendChild(h);
        const items = document.createElement('div'); items.className = 'swatch-items';
        els.filter(Boolean).forEach(el => { if(el.dataset) delete el.dataset.wired; items.appendChild(el); });
        wrap.appendChild(items);
        return wrap;
      };
      const out = document.createElement('div');
      out.className = 'swatch-board';

      // buttons
      const btnRed = grab('.btn.btn-red'); const btnGhost = grab('.btn.btn-ghost'); const btnBlue = grab('.btn.btn-blue');
      out.appendChild(row('Buttons', [btnRed, btnGhost, btnBlue]));

      // chips (default + active)
      const chip1 = grab('.cat-row .chip'); const chip2 = grab('.cat-row .chip.active');
      out.appendChild(row('Chips', [chip1, chip2]));

      // sidebar items (default + selected)
      const sbItem = grab('.sb-item'); const sbSel = grab('.sb-item.sel');
      out.appendChild(row('Sidebar items', [sbItem, sbSel]));

      // pills / badges / tags
      const badge = grab('.gcard .badge'); const badgeRelief = grab('.gcard .badge.relief'); const tag = grab('.sec-head .tag');
      out.appendChild(row('Badges &amp; tags', [badge, badgeRelief]));

      // game card (normally sized by its grid/rail parent — pin an explicit width here)
      const gcardBox = document.createElement('div'); gcardBox.style.width = '180px';
      const gcard = grab('.gcard'); if (gcard) gcardBox.appendChild(gcard);
      out.appendChild(row('Game card', [gcard ? gcardBox : null]));

      // promo card (same — normally sized by the promos grid)
      const promoBox = document.createElement('div'); promoBox.style.width = '360px';
      const promo = grab('.promo'); if (promo) promoBox.appendChild(promo);
      out.appendChild(row('Promo card', [promo ? promoBox : null]));

      document.body.appendChild(out);
      const html = out.outerHTML;
      out.remove();
      return html;
    });

    // odds buttons: default + selected, 3-way + 2-way
    await page.evaluate(() => show('sports'));
    await page.waitForTimeout(200);
    const oddsHtml = await page.evaluate(() => {
      const wrap = document.createElement('div'); wrap.className='swatch-row';
      const h = document.createElement('div'); h.className='swatch-title'; h.textContent='Odds buttons';
      wrap.appendChild(h);
      const items = document.createElement('div'); items.className='swatch-items';
      const mcard = document.querySelector('.sp-mcard .oddsrow');
      if (mcard) { const c = mcard.cloneNode(true); c.style.width = '260px'; items.appendChild(c); }
      const selOdds = document.querySelector('.odds');
      if (selOdds) {
        const c = selOdds.cloneNode(true); c.classList.add('sel'); c.style.flex = 'none';
        items.appendChild(c);
      }
      wrap.appendChild(items);
      document.body.appendChild(wrap);
      const html = wrap.outerHTML;
      wrap.remove();
      return html;
    });
    const combinedSwatch = swatchHtml.slice(0, -6) + oddsHtml + '</div>'; // insert before swatch-board's closing tag
    frames.push({ id:'components-swatch', label:'Components — buttons, chips, cards, odds', kind:'swatch', html: combinedSwatch });

    // betslip desktop
    await page.evaluate(() => show('sports'));
    await page.evaluate(() => { const o=document.querySelector('.odds'); if(o) togglePick(o); });
    await page.waitForTimeout(200);
    frames.push({ id:'betslip-desktop', label:'Betslip — desktop panel', kind:'betslip-desktop', html: await captureClean(page, '#betslip') });
    frames.push({ id:'betslip-tab', label:'Betslip — edge tab', kind:'chrome-vertical', html: await captureClean(page, '#betslip-tab') });

    await page.close();
  }

  // ---------- mobile pass ----------
  {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await page.goto(filePath);
    await page.waitForTimeout(400);
    await page.evaluate(() => {
      document.body.classList.add('signedIn');
      const m = document.getElementById('auth-modal'); if (m) m.classList.remove('on');
      window.openAuth = () => {};
    });

    frames.push({ id:'chrome-mobilebar', label:'Mobile bottom bar', kind:'chrome-horizontal-mobile',
      html: await captureClean(page, '.mobilebar') });

    await page.evaluate(() => openSheet('more'));
    await page.waitForTimeout(200);
    frames.push({ id:'sheet-more', label:'Sheet — more', kind:'sheet', html: await captureClean(page, '#sheet-more') });
    await page.evaluate(() => closeSheet('more'));

    await page.evaluate(() => openSheet('scale'));
    await page.waitForTimeout(200);
    frames.push({ id:'sheet-scale', label:'Sheet — pain scale', kind:'sheet', html: await captureClean(page, '#sheet-scale') });
    await page.evaluate(() => closeSheet('scale'));

    // betslip mobile bottom sheet
    await page.evaluate(() => setMode('sports'));
    await page.waitForTimeout(150);
    await page.evaluate(() => { const o=document.querySelector('.odds'); if(o) togglePick(o); });
    await page.waitForTimeout(250);
    frames.push({ id:'betslip-mobile', label:'Betslip — mobile bottom sheet', kind:'sheet', html: await captureClean(page, '#betslip') });

    await page.close();
  }

  fs.writeFileSync(OUT, JSON.stringify(frames, null, 2));
  console.log('captured', frames.length, 'frames ->', OUT);
  await browser.close();
})();
