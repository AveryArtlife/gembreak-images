// Renders brand/logo/*.svg to PNG at the sizes each surface needs.
// Usage: node scripts/export.mjs [outDir]   (default: brand/exports)
// Requires: playwright with Chromium (pre-installed in Claude cloud; locally: npx playwright install chromium)
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
import { readFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const outDir = resolve(process.argv[2] || resolve(root, 'brand/exports'));
mkdirSync(outDir, { recursive: true });

const fontsDir = resolve(root, 'site/assets/fonts');
const fontFace = (fam, file, w) => existsSync(resolve(fontsDir, file))
  ? `@font-face{font-family:'${fam}';font-weight:${w};src:url('file://${resolve(fontsDir, file)}') format('truetype');}` : '';
const css = [
  fontFace('Fredoka', 'Fredoka-600.ttf', 600), fontFace('Fredoka', 'Fredoka-700.ttf', 700),
  fontFace('Inter', 'Inter-400.ttf', 400), fontFace('Inter', 'Inter-600.ttf', 600),
  fontFace('JetBrains Mono', 'JetBrainsMono-500.ttf', 500),
].join('\n');

// [svg file, output basename, [sizes as width x height], transparent?]
const jobs = [
  ['cha-mark.svg',   'cha-mark',   [[512, 512], [1024, 1024], [256, 256], [64, 64], [32, 32]], true],
  ['cha-coin.svg',   'cha-coin',   [[512, 512], [1024, 1024], [200, 200]], true],
  ['cha-avatar.svg', 'cha-avatar', [[400, 400], [800, 800]], true],
  ['cha-wordmark.svg', 'cha-wordmark', [[1200, 400]], true],
  ['cha-lockup.svg', 'cha-lockup', [[1600, 480]], true],
  ['cha-banner.svg', 'cha-banner', [[1500, 500], [3000, 1000]], false],
  ['cha-og.svg',     'cha-og',     [[1200, 630]], false],
];

const browser = await chromium.launch();
const page = await browser.newPage();
for (const [file, base, sizes, transparent] of jobs) {
  const svgPath = resolve(root, 'brand/logo', file);
  if (!existsSync(svgPath)) { console.log('skip (missing)', file); continue; }
  const svg = readFileSync(svgPath, 'utf8');
  for (const [w, h] of sizes) {
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(`<!doctype html><html><head><style>${css}
      html,body{margin:0;padding:0;background:${transparent ? 'transparent' : '#0B0F1A'};}
      svg{display:block;width:${w}px;height:${h}px;}</style></head><body>${svg}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    const out = resolve(outDir, `${base}-${w}x${h}.png`);
    await page.screenshot({ path: out, omitBackground: transparent, clip: { x: 0, y: 0, width: w, height: h } });
    console.log('wrote', out);
  }
}
await browser.close();
