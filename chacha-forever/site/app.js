/* Cha Cha Forever — site config + behaviour.
   Fill CONFIG at launch. Everything on the page keys off CONTRACT_ADDRESS. */
const CONFIG = {
  CONTRACT_ADDRESS: '',          // ← paste the pump.fun CA here at T-0 and deploy
  PLEDGE_WALLET: '',             // public Pledge wallet (50% of creator fees)
  LAUNCH_WALLET: '',             // public launch wallet (1.5–2% creation buy, locked 30d)
  TREASURY_MULTISIG: '',         // Squads 2-of-3
  LINKS: {
    x: 'https://x.com/chachaforever',
    telegram: 'https://t.me/chachaforever',
    tiktok: 'https://www.tiktok.com/@chachaforever',
    instagram: 'https://www.instagram.com/chachaforever',
    wallForm: '',                // Tally / Google Form for Forever Wall submissions
  },
  DONATIONS: [
    // { date: '2026-11-05', org: 'Best Friends Animal Society', amountSol: 12.5, tx: 'https://solscan.io/tx/...' }
  ],
};

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const ca = CONFIG.CONTRACT_ADDRESS.trim();
const live = ca.length > 30;

const links = live ? {
  pump: `https://pump.fun/coin/${ca}`,
  dex: `https://dexscreener.com/solana/${ca}`,
  jup: `https://jup.ag/swap/SOL-${ca}`,
  rug: `https://rugcheck.xyz/tokens/${ca}`,
  bubble: `https://app.bubblemaps.io/sol/token/${ca}`,
  solscan: `https://solscan.io/token/${ca}`,
} : {};

// --- contract address boxes ---
$$('[data-ca]').forEach(el => {
  el.textContent = live ? ca : 'TBA — drops at launch, only from this site, our X and our Telegram';
  el.classList.toggle('is-tba', !live);
});
$$('[data-copy]').forEach(btn => {
  btn.disabled = !live;
  btn.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(ca); btn.textContent = 'Copied'; setTimeout(() => btn.textContent = 'Copy', 1500); }
    catch { btn.textContent = 'Select & copy'; }
  });
});

// --- wallet boxes ---
const wallets = { pledge: CONFIG.PLEDGE_WALLET, launch: CONFIG.LAUNCH_WALLET, treasury: CONFIG.TREASURY_MULTISIG };
$$('[data-wallet]').forEach(el => {
  const v = (wallets[el.dataset.wallet] || '').trim();
  if (v) { el.innerHTML = `<a href="https://solscan.io/account/${v}" target="_blank" rel="noopener">${v}</a>`; }
  else { el.textContent = 'Published before launch'; el.classList.add('is-tba'); }
});

// --- links that need the CA ---
$$('[data-link]').forEach(a => {
  const key = a.dataset.link;
  if (links[key]) { a.href = links[key]; a.removeAttribute('aria-disabled'); }
  else if (CONFIG.LINKS[key]) { a.href = CONFIG.LINKS[key]; }
  else { a.setAttribute('aria-disabled', 'true'); a.addEventListener('click', e => e.preventDefault()); }
});

// --- live stats from DexScreener (only once the pair exists) ---
async function stats() {
  if (!live) return;
  try {
    const r = await fetch(`https://api.dexscreener.com/latest/dex/tokens/${ca}`);
    const d = await r.json();
    const p = (d.pairs || []).sort((a, b) => (b.liquidity?.usd || 0) - (a.liquidity?.usd || 0))[0];
    if (!p) return;
    const fmt = n => n >= 1e9 ? `$${(n/1e9).toFixed(2)}B` : n >= 1e6 ? `$${(n/1e6).toFixed(2)}M` : n >= 1e3 ? `$${(n/1e3).toFixed(1)}K` : `$${Number(n).toFixed(0)}`;
    $('[data-stat=mcap]').textContent = fmt(p.marketCap || p.fdv || 0);
    $('[data-stat=vol]').textContent = fmt(p.volume?.h24 || 0);
    $('[data-stat=price]').textContent = `$${Number(p.priceUsd).toPrecision(3)}`;
    $('[data-stat=change]').textContent = `${(p.priceChange?.h24 ?? 0) > 0 ? '+' : ''}${p.priceChange?.h24 ?? 0}%`;
    $('#live-stats').hidden = false;
  } catch {}
}
stats(); setInterval(stats, 30000);

// --- donations log ---
const log = $('#donation-log');
if (log) {
  if (CONFIG.DONATIONS.length === 0) {
    log.innerHTML = `<p class="muted">First donation within 7 days of launch. Every transfer is posted here with its transaction hash.</p>`;
  } else {
    log.innerHTML = `<table><thead><tr><th>Date</th><th>To</th><th>Amount</th><th>Tx</th></tr></thead><tbody>` +
      CONFIG.DONATIONS.map(d => `<tr><td>${d.date}</td><td>${d.org}</td><td>${d.amountSol} SOL</td><td><a href="${d.tx}" target="_blank" rel="noopener">view</a></td></tr>`).join('') +
      `</tbody></table>`;
  }
}

// --- Forever Wall ---
fetch('wall.json').then(r => r.json()).then(({ pets }) => {
  const grid = $('#wall-grid'); if (!grid) return;
  grid.innerHTML = pets.map(p => `
    <figure class="pet">
      <div class="pet-art">${p.img ? `<img src="${p.img}" alt="${p.name}" loading="lazy" onerror="this.replaceWith(document.querySelector('#halo-fallback').content.cloneNode(true))">` : `<span class="halo-fallback"></span>`}<span class="pet-halo"></span></div>
      <figcaption><strong>${p.name}</strong><span>${p.kind}</span>${p.years ? `<span class="years">${p.years}</span>` : ''}${p.note ? `<em>${p.note}</em>` : ''}</figcaption>
    </figure>`).join('');
}).catch(() => {});
const wallBtn = $('[data-wall-form]');
if (wallBtn) { if (CONFIG.LINKS.wallForm) wallBtn.href = CONFIG.LINKS.wallForm; else { wallBtn.setAttribute('aria-disabled', 'true'); wallBtn.textContent = 'Submissions open at launch'; } }

// --- marquee duplication for seamless loop ---
$$('.marquee-track').forEach(t => { t.innerHTML += t.innerHTML; });

// --- mobile nav ---
const burger = $('.burger'); const nav = $('.nav-links');
if (burger) burger.addEventListener('click', () => { const o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o); });
$$('.nav-links a').forEach(a => a.addEventListener('click', () => nav.classList.remove('open')));

// --- year ---
$$('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
