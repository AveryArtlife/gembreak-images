// Push every image to Vercel Blob at watches/<SKU>/<n>.jpg
// Run: BLOB_READ_WRITE_TOKEN=xxx node scripts/sync-to-blob.mjs   (npm i @vercel/blob)
import { put } from "@vercel/blob";
import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";
const ROOT = "watches";
for (const sku of await readdir(ROOT)) {
  for (const f of await readdir(join(ROOT, sku))) {
    const body = await readFile(join(ROOT, sku, f));
    const { url } = await put(`watches/${sku}/${f}`, body, { access: "public", contentType: "image/jpeg", addRandomSuffix: false });
    console.log(url);
  }
}
