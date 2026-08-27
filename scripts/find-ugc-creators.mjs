// Find street-interview UGC creators in NYC + Miami for GemBreak outreach.
//
// Produces the exact shortlist we want: creators under a follower cap, who posted
// in the last N days, ranked by how viral their videos actually go, with the
// GemBreak-relevant ones (watches, jewelry, gambling, mystery packs, finance,
// crypto) pushed to the top.
//
// Setup (one time):
//   1. Sign up at apify.com -> Settings -> API & Integrations -> copy the token.
//   2. npm i            (no new deps -- this uses plain fetch)
//
// Run:
//   APIFY_TOKEN=apify_api_xxx node scripts/find-ugc-creators.mjs
//
// Options (env vars):
//   MAX_FOLLOWERS=50000     follower ceiling
//   DAYS=7                  only keep creators who posted this recently
//   PER_QUERY=60            videos pulled per search query (cost knob)
//   PLATFORMS=tiktok,instagram
//
// Output: out/creators-nyc.md, out/creators-miami.md, out/creators.csv
// A run at the defaults is ~40 queries and costs a couple of dollars of Apify
// credit -- the free tier covers a first pass.

import { mkdir, writeFile } from "node:fs/promises";

const TOKEN = process.env.APIFY_TOKEN;
if (!TOKEN) {
  console.error("Missing APIFY_TOKEN. Get one at apify.com -> Settings -> API & Integrations.");
  process.exit(1);
}

const MAX_FOLLOWERS = Number(process.env.MAX_FOLLOWERS ?? 50_000);
const DAYS = Number(process.env.DAYS ?? 7);
const PER_QUERY = Number(process.env.PER_QUERY ?? 60);
const PLATFORMS = (process.env.PLATFORMS ?? "tiktok,instagram").split(",").map((p) => p.trim());
const CUTOFF = Date.now() - DAYS * 864e5;

// ---------------------------------------------------------------- search plan

// Street-interview format terms, crossed with each city's own vocabulary.
// Kept broad on purpose -- filtering happens after, on real numbers.
const FORMAT = [
  "street interview",
  "asking strangers",
  "public interview",
  "asking people on the street",
  "how much is your outfit",
  "how much was your watch",
  "what do you do for a living",
];

// The niches that matter for GemBreak. A creator already asking strangers about
// their watch is a warm intro to a mystery-pack sponsorship.
const NICHE = [
  "how much is your watch",
  "watch check street",
  "asking rich people what they do",
  "jewelry street interview",
  "asking people how much they make",
  "crypto street interview",
  "asking strangers about bitcoin",
  "gambling street interview",
  "mystery box street",
];

const CITIES = {
  nyc: {
    label: "New York City",
    terms: ["nyc", "new york", "manhattan", "soho nyc", "times square", "brooklyn"],
    hashtags: ["nycstreetinterview", "streetinterviewnyc", "nyc", "diamonddistrict"],
    // Used to confirm a creator is actually local, not just passing through.
    signals: ["nyc", "new york", "manhattan", "brooklyn", "queens", "bronx", "soho", "harlem", "47th"],
  },
  miami: {
    label: "Miami",
    terms: ["miami", "brickell", "wynwood", "south beach", "miami beach", "design district miami"],
    hashtags: ["miamistreetinterview", "streetinterviewmiami", "miami", "brickell", "wynwood"],
    signals: ["miami", "brickell", "wynwood", "south beach", "mia", "305", "doral", "coral gables"],
  },
};

// Caption/bio keywords -> GemBreak category. Drives the priority boost.
const CATEGORIES = {
  watch: ["watch", "rolex", "patek", "ap ", "audemars", "richard mille", "cartier", "omega", "timepiece", "watchtok"],
  jewelry: ["jewelry", "jewellery", "chain", "diamond", "iced out", "grillz", "vvs", "bust down"],
  gambling: ["gambling", "casino", "bet", "betting", "slots", "blackjack", "roulette", "parlay"],
  "mystery pack": ["mystery box", "mystery pack", "unboxing", "blind box", "pack opening", "case opening"],
  finance: ["salary", "how much do you make", "net worth", "invest", "money", "finance", "stocks", "portfolio"],
  crypto: ["crypto", "bitcoin", "btc", "ethereum", "solana", "memecoin", "web3", "nft"],
};

// ------------------------------------------------------------------ apify i/o

async function runActor(actorId, input) {
  const url = `https://api.apify.com/v2/acts/${actorId}/run-sync-get-dataset-items?token=${TOKEN}`;
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(input),
    });
    if (!res.ok) {
      console.error(`  ! ${actorId} -> ${res.status} ${(await res.text()).slice(0, 200)}`);
      return [];
    }
    return await res.json();
  } catch (err) {
    // One dead actor shouldn't sink the run -- keep whatever the others returned.
    console.error(`  ! ${actorId} -> ${err.message}`);
    return [];
  }
}

// Actor output shapes drift between versions, so read every field defensively.
const pick = (...vals) => vals.find((v) => v !== undefined && v !== null);
const num = (v) => (typeof v === "number" ? v : Number(v)) || 0;

function normalizeTikTok(item) {
  const a = item.authorMeta ?? item.author ?? {};
  const username = pick(a.name, a.uniqueId, a.nickName, item.authorUsername);
  if (!username) return null;
  const created = pick(item.createTimeISO, item.createTime && item.createTime * 1000, item.uploadedAt);
  return {
    platform: "tiktok",
    username,
    followers: num(pick(a.fans, a.followerCount, a.followers)),
    bio: pick(a.signature, a.bio, "") ?? "",
    caption: pick(item.text, item.description, "") ?? "",
    views: num(pick(item.playCount, item.views, item.playCountRaw)),
    likes: num(pick(item.diggCount, item.likes)),
    postedAt: created ? new Date(created).getTime() : 0,
    url: pick(item.webVideoUrl, item.videoUrl, `https://www.tiktok.com/@${username}`),
  };
}

function normalizeInstagram(item) {
  const username = pick(item.ownerUsername, item.username, item.owner?.username);
  if (!username) return null;
  return {
    platform: "instagram",
    username,
    // Hashtag results rarely carry follower counts; backfilled below.
    followers: num(pick(item.ownerFollowersCount, item.followersCount)),
    bio: pick(item.ownerBiography, item.biography, "") ?? "",
    caption: pick(item.caption, item.text, "") ?? "",
    views: num(pick(item.videoViewCount, item.videoPlayCount, item.likesCount)),
    likes: num(pick(item.likesCount, item.likes)),
    postedAt: item.timestamp ? new Date(item.timestamp).getTime() : 0,
    url: pick(item.url, `https://www.instagram.com/${username}/`),
  };
}

// ------------------------------------------------------------------- scraping

async function scrapeTikTok(city) {
  const queries = [
    ...FORMAT.flatMap((f) => city.terms.slice(0, 3).map((t) => `${f} ${t}`)),
    ...NICHE.map((n) => `${n} ${city.terms[0]}`),
  ];
  console.log(`  tiktok: ${queries.length} search queries + ${city.hashtags.length} hashtags`);

  const [bySearch, byTag] = await Promise.all([
    runActor("clockworks~tiktok-scraper", {
      searchQueries: queries,
      resultsPerPage: PER_QUERY,
      searchSection: "/video",
      shouldDownloadVideos: false,
      shouldDownloadCovers: false,
      shouldDownloadSubtitles: false,
      proxyCountryCode: "US",
    }),
    runActor("clockworks~tiktok-hashtag-scraper", {
      hashtags: city.hashtags,
      resultsPerPage: PER_QUERY,
      shouldDownloadVideos: false,
      shouldDownloadCovers: false,
    }),
  ]);

  return [...bySearch, ...byTag].map(normalizeTikTok).filter(Boolean);
}

async function scrapeInstagram(city) {
  const posts = await runActor("apify~instagram-scraper", {
    search: city.hashtags[0],
    searchType: "hashtag",
    resultsType: "posts",
    resultsLimit: PER_QUERY * 2,
    onlyPostsNewerThan: new Date(CUTOFF).toISOString().slice(0, 10),
  });
  const rows = posts.map(normalizeInstagram).filter(Boolean);

  // Backfill follower counts -- hashtag results don't include them.
  const handles = [...new Set(rows.map((r) => r.username))].slice(0, 200);
  if (!handles.length) return rows;
  const profiles = await runActor("apify~instagram-profile-scraper", { usernames: handles });
  const followersBy = new Map(
    profiles.map((p) => [p.username, num(pick(p.followersCount, p.followers))]),
  );
  const bioBy = new Map(profiles.map((p) => [p.username, pick(p.biography, "") ?? ""]));
  for (const r of rows) {
    r.followers = followersBy.get(r.username) ?? r.followers;
    r.bio = bioBy.get(r.username) || r.bio;
  }
  return rows;
}

// ------------------------------------------------------------------ analysis

function categoriesFor(text) {
  const t = text.toLowerCase();
  return Object.entries(CATEGORIES)
    .filter(([, words]) => words.some((w) => t.includes(w)))
    .map(([cat]) => cat);
}

function isLocal(creator, city) {
  const t = `${creator.bio} ${creator.samples.map((s) => s.caption).join(" ")}`.toLowerCase();
  return city.signals.some((s) => t.includes(s));
}

function groupCreators(rows) {
  const by = new Map();
  for (const r of rows) {
    const key = `${r.platform}:${r.username}`;
    if (!by.has(key)) {
      by.set(key, {
        platform: r.platform,
        username: r.username,
        followers: r.followers,
        bio: r.bio,
        samples: [],
      });
    }
    const c = by.get(key);
    c.followers = Math.max(c.followers, r.followers); // most complete reading wins
    if (!c.bio) c.bio = r.bio;
    c.samples.push({ url: r.url, views: r.views, likes: r.likes, postedAt: r.postedAt, caption: r.caption });
  }
  return [...by.values()];
}

function score(creator) {
  const views = creator.samples.map((s) => s.views).sort((a, b) => b - a);
  const best = views[0] ?? 0;
  const median = views[Math.floor(views.length / 2)] ?? 0;
  // Videos that cleared 100k are the real signal -- a small account with three
  // of those is worth more to us than a bigger one with none.
  const hits = views.filter((v) => v >= 100_000).length;
  // How far past their own audience a video travels. This is what makes a
  // sub-50k creator a bargain.
  const reach = creator.followers > 0 ? best / creator.followers : 0;

  creator.bestViews = best;
  creator.medianViews = median;
  creator.viralHits = hits;
  creator.reachMultiple = Number(reach.toFixed(1));
  creator.categories = [
    ...new Set(creator.samples.flatMap((s) => categoriesFor(`${s.caption} ${creator.bio}`))),
  ];
  creator.lastPost = Math.max(...creator.samples.map((s) => s.postedAt));

  return (
    hits * 40 +
    Math.log10(best + 1) * 12 +
    Math.log10(median + 1) * 6 +
    Math.min(reach, 50) * 2 +
    creator.categories.length * 25 // GemBreak-niche creators float to the top
  );
}

// -------------------------------------------------------------------- reports

const fmt = (n) => n.toLocaleString("en-US");
const day = (ms) => (ms ? new Date(ms).toISOString().slice(0, 10) : "unknown");

function toMarkdown(cityLabel, creators) {
  const lines = [
    `# Street-interview UGC creators — ${cityLabel}`,
    "",
    `Under ${fmt(MAX_FOLLOWERS)} followers · posted within ${DAYS} days · ranked by viral reach.`,
    `Generated ${new Date().toISOString().slice(0, 10)}.`,
    "",
  ];
  creators.forEach((c, i) => {
    const handle = c.platform === "tiktok" ? `https://www.tiktok.com/@${c.username}` : `https://www.instagram.com/${c.username}/`;
    lines.push(`## ${i + 1}. @${c.username} — ${fmt(c.followers)} followers (${c.platform})`);
    lines.push(`- Profile: ${handle}`);
    lines.push(`- Best video: ${fmt(c.bestViews)} views · ${c.viralHits} video(s) over 100k · ${c.reachMultiple}x their follower count`);
    lines.push(`- Categories: ${c.categories.length ? c.categories.join(", ") : "general street interview"}`);
    lines.push(`- Last posted: ${day(c.lastPost)}`);
    lines.push("- Examples:");
    for (const s of c.samples.sort((a, b) => b.views - a.views).slice(0, 3)) {
      lines.push(`  - ${s.url} — ${fmt(s.views)} views (${day(s.postedAt)})`);
    }
    lines.push("");
  });
  if (!creators.length) lines.push("_No creators matched. Loosen MAX_FOLLOWERS or DAYS and re-run._");
  return lines.join("\n");
}

function toCsv(all) {
  const head = "city,platform,username,followers,best_views,viral_hits_100k,reach_multiple,categories,last_post,profile_url,top_video";
  const rows = all.map((c) => {
    const top = c.samples.sort((a, b) => b.views - a.views)[0];
    const profile = c.platform === "tiktok" ? `https://www.tiktok.com/@${c.username}` : `https://www.instagram.com/${c.username}/`;
    return [
      c.city, c.platform, c.username, c.followers, c.bestViews, c.viralHits,
      c.reachMultiple, `"${c.categories.join(" | ")}"`, day(c.lastPost), profile, top?.url ?? "",
    ].join(",");
  });
  return [head, ...rows].join("\n");
}

// ----------------------------------------------------------------------- main

const all = [];

for (const [key, city] of Object.entries(CITIES)) {
  console.log(`\n${city.label}`);
  const rows = [];
  if (PLATFORMS.includes("tiktok")) rows.push(...(await scrapeTikTok(city)));
  if (PLATFORMS.includes("instagram")) rows.push(...(await scrapeInstagram(city)));
  console.log(`  ${rows.length} videos scraped`);

  const creators = groupCreators(rows)
    .filter((c) => c.followers > 0 && c.followers <= MAX_FOLLOWERS)
    .filter((c) => c.samples.some((s) => s.postedAt >= CUTOFF))
    .filter((c) => isLocal(c, city));

  for (const c of creators) {
    c.rank = score(c);
    c.city = key;
  }
  creators.sort((a, b) => b.rank - a.rank);

  console.log(`  ${creators.length} creators match (<=${fmt(MAX_FOLLOWERS)} followers, posted in ${DAYS}d)`);
  await mkdir("out", { recursive: true });
  await writeFile(`out/creators-${key}.md`, toMarkdown(city.label, creators));
  all.push(...creators);
}

await writeFile("out/creators.csv", toCsv(all));
console.log(`\nWrote out/creators-nyc.md, out/creators-miami.md, out/creators.csv (${all.length} creators).`);
