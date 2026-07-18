# GemBreak Watch Images

High-resolution watch images for gembreak.com inventory. Organized by SKU.

## Structure
```
watches/<SKU>/1.jpg   # primary product shot
watches/<SKU>/2.jpg   # secondary
watches/<SKU>/3.jpg   # tertiary
```
`<SKU>` matches the **SKU column** in the GemBreak inventory Sheet exactly
(slashes/spaces replaced with `-`/`_`).

## Using in code (URL by convention — no mapping table needed)
```js
const CDN = "https://cdn.gembreak.com";           // or the raw GitHub base
const img = (sku, n=1) => `${CDN}/watches/${sku.replaceAll('/','-').replaceAll(' ','_')}/${n}.jpg`;
```

## Production hosting: sync to Vercel Blob (recommended)
```
npm i @vercel/blob
BLOB_READ_WRITE_TOKEN=xxx node scripts/sync-to-blob.mjs
```
