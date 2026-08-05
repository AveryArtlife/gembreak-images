// Sync GemBreak watch images to Vercel Blob and emit a SKU -> public URL map.
//
// Setup (one time):
//   1. In Vercel: Storage -> Blob -> Create store. Copy the BLOB_READ_WRITE_TOKEN.
//   2. npm i            (installs @vercel/blob from package.json)
//
// Run:
//   BLOB_READ_WRITE_TOKEN=vercel_blob_rw_xxx node scripts/sync-to-blob.mjs
//
// Output: uploads every image and writes scripts/blob-urls.json:
//   { "<SKU>": { "cutout": "<public png url>", "icybox": "<public jpg url>" }, ... }
// These URLs are public, permanent, CDN-served -- hand them straight to the site.

import { put } from "@vercel/blob";
import { readdir, readFile, writeFile } from "node:fs/promises";
import { join, extname, basename } from "node:path";

if (!process.env.BLOB_READ_WRITE_TOKEN) {
  console.error("Missing BLOB_READ_WRITE_TOKEN. Create a Vercel Blob store and pass its token.");
  process.exit(1);
}

// folder -> { key on blob, contentType, field name in the output map }
const SETS = [
  { dir: "watches-only", prefix: "watches-only", type: "image/png", field: "cutout" },
  { dir: "icybox",       prefix: "icybox",       type: "image/jpeg", field: "icybox" },
];

const map = {};
let n = 0, fail = 0;

for (const set of SETS) {
  let files;
  try { files = await readdir(set.dir); } catch { console.log(`skip ${set.dir} (not found)`); continue; }
  for (const f of files) {
    const ext = extname(f).toLowerCase();
    if (![".png", ".jpg", ".jpeg", ".webp"].includes(ext)) continue; // skip README etc.
    const sku = basename(f, ext);
    try {
      const body = await readFile(join(set.dir, f));
      const { url } = await put(`${set.prefix}/${f}`, body, {
        access: "public",
        contentType: set.type,
        addRandomSuffix: false,       // stable URL per SKU
        allowOverwrite: true,
      });
      (map[sku] ||= {})[set.field] = url;
      if (++n % 25 === 0) console.log(`  uploaded ${n}...`);
    } catch (e) {
      fail++; console.error(`  FAIL ${set.dir}/${f}: ${e.message}`);
    }
  }
}

await writeFile("scripts/blob-urls.json", JSON.stringify(map, null, 1));
console.log(`\nDone. ${n} uploaded, ${fail} failed, ${Object.keys(map).length} SKUs.`);
console.log("URL map -> scripts/blob-urls.json");
