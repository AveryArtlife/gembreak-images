// Find US creators who can shoot pack rip / pack rip reaction videos for GemBreak.
//
// Ranks for cost-per-conversion, not reach: comment rate and format fit lead,
// raw views trail. See campaigns/creator-search-prompt.md for why.
//
// Setup (one time):
//   1. apify.com -> Settings -> API & Integrations -> copy the token.
//   2. npm i            (no new deps -- plain fetch)
//
// Run:
//   APIFY_TOKEN=apify_api_xxx node scripts/find-ugc-creators.mjs
//
// Options (env vars):
//   MIN_FOLLOWERS=5000       floor
//   MAX_FOLLOWERS=500000     ceiling
//   DAYS=30                  only creators who posted this recently
//   PER_QUERY=50             results per query (cost knob)
//   PLATFORMS=tiktok,instagram,youtube
//
// Output: out/creators-<platform>.md (split by tier) and out/creators.csv
// (every creator, best first -- the top of that file is the outreach queue).

import { mkdir, writeFile } from "node:fs/promises";

const TOKEN = process.env.APIFY_TOKEN;
if (!TOKEN) {
  console.error("Missing APIFY_TOKEN. Get one at apify.com -> Settings -> API & Integrations.");
  process.exit(1);
}

const MIN_FOLLOWERS = Number(process.env.MIN_FOLLOWERS ?? 5_000);
const MAX_FOLLOWERS = Number(process.env.MAX_FOLLOWERS ?? 500_000);
const DAYS = Number(process.env.DAYS ?? 30);
const PER_QUERY = Number(process.env.PER_QUERY ?? 50);
const PLATFORMS = (process.env.PLATFORMS ?? "tiktok,instagram,youtube").split(",").map((p) => p.trim());
const CUTOFF = Date.now() - DAYS * 864e5;

// ---------------------------------------------------------------- search plan

const FORMAT = [
  "pack rip", "ripping packs", "pack opening", "unboxing", "mystery box",
  "mystery pack", "case break", "box break", "whats inside", "blind box",
];

const NICHE = [
  "watch unboxing", "watch collection", "jewelry unboxing", "iced out",
  "sneaker unboxing", "card break", "sports cards", "collectibles haul",
  "grail unboxing", "reseller haul",
];

const REACTION = [
  "insane pull", "best pull", "worst pull", "pull reaction", "opening reaction",
];

const HASHTAGS = [
  "packrip", "packopening", "mysterybox", "unboxing", "watchtok",
  "cardbreak", "boxbreak", "hypebeast", "grail", "whatsinside",
];

// Cities are tags, not filters -- useful for clustering shoots, never a reason
// to exclude someone.
const CITY_TAGS = {
  nyc: ["nyc", "new york", "manhattan", "brooklyn", "queens", "bronx"],
  miami: ["miami", "brickell", "wynwood", "south beach", "305"],
  la: ["los angeles", "la ", "hollywood", "socal", "dtla"],
  atlanta: ["atlanta", "atl", "buckhead"],
  dallas: ["dallas", "dfw", "fort worth"],
  chicago: ["chicago", "chi town", "windy city"],
  vegas: ["las vegas", "vegas"],
  houston: ["houston", "htx"],
  phoenix: ["phoenix", "scottsdale", "az"],
  philly: ["philadelphia", "philly"],
};

const CATEGORIES = {
  watch: ["watch", "rolex", "patek", "audemars", "richard mille", "cartier", "omega", "timepiece", "watchtok"],
  jewelry: ["jewelry", "jewellery", "chain", "diamond", "iced out", "grillz", "vvs", "bust down"],
  sneakers: ["sneaker", "jordan", "yeezy", "kicks", "hypebeast", "stockx"],
  cards: ["card break", "pokemon", "sports card", "psa", "topps", "panini", "slab"],
  "mystery pack": ["mystery box", "mystery pack", "blind box", "pack opening", "pack rip", "case break"],
  finance: ["net worth", "invest", "money", "finance", "stocks", "portfolio", "resell"],
  crypto: ["crypto", "bitcoin", "btc", "ethereum", "solana", "web3", "nft"],
};

// Having already shot a reveal is the single strongest signal that a creator
// can execute this brief on the first take.
const FORMAT_FIT = [
  "unbox", "pack rip", "pack opening", "mystery box", "mystery pack",
  "break", "whats inside", "what's inside", "blind box", "pull",
];

// Cheap to check, expensive to miss.
const DISQUALIFY = {
  giveaway: ["tag 3 friends", "tag three friends", "giveaway", "enter to win", "follow to win"],
  kids: ["kid friendly", "family channel", "toys for kids", "kids toys"],
};

const US_SIGNALS = [
  "usa", "united states", "🇺🇸", "us based", "shipping from us",
  ...Object.values(CITY_TAGS).flat(),
];

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
const ms = (v) => (v ? new Date(v).getTime() : 0);

function normalizeTikTok(item) {
  const a = item.authorMeta ?? item.author ?? {};
  const username = pick(a.name, a.uniqueId, a.nickName);
  if (!username) return null;
  return {
    platform: "tiktok",
    username,
    followers: num(pick(a.fans, a.followerCount, a.followers)),
    bio: pick(a.signature, a.bio, "") ?? "",
    caption: pick(item.text, item.description, "") ?? "",
    views: num(pick(item.playCount, item.views)),
    likes: num(pick(item.diggCount, item.likes)),
    comments: num(pick(item.commentCount, item.comments)),
    postedAt: ms(pick(item.createTimeISO, item.createTime && item.createTime * 1000)),
    url: pick(item.webVideoUrl, `https://www.tiktok.com/@${username}`),
  };
}

function normalizeInstagram(item) {
  const username = pick(item.ownerUsername, item.username, item.owner?.username);
  if (!username) return null;
  return {
    platform: "instagram",
    username,
    followers: num(pick(item.ownerFollowersCount, item.followersCount)), // backfilled below
    bio: pick(item.ownerBiography, item.biography, "") ?? "",
    caption: pick(item.caption, item.text, "") ?? "",
    views: num(pick(item.videoViewCount, item.videoPlayCount)),
    likes: num(pick(item.likesCount, item.likes)),
    comments: num(pick(item.commentsCount, item.comments)),
    postedAt: ms(item.timestamp),
    url: pick(item.url, `https://www.instagram.com/${username}/`),
  };
}

function normalizeYouTube(item) {
  const username = pick(item.channelUsername, item.channelName, item.channelTitle);
  if (!username) return null;
  return {
    platform: "youtube",
    username: String(username).replace(/^@/, ""),
    followers: num(pick(item.numberOfSubscribers, item.channelTotalSubscribers, item.subscriberCount)),
    bio: pick(item.channelDescription, "") ?? "",
    caption: `${pick(item.title, "") ?? ""} ${pick(item.text, item.description, "") ?? ""}`,
    views: num(pick(item.viewCount, item.views)),
    likes: num(pick(item.likes, item.likeCount)),
    comments: num(pick(item.commentsCount, item.commentCount)),
    postedAt: ms(pick(item.date, item.uploadDate)),
    url: pick(item.url, item.channelUrl, ""),
  };
}

// ------------------------------------------------------------------- scraping

const QUERIES = [...FORMAT, ...NICHE, ...REACTION];

async function scrapeTikTok() {
  console.log(`  tiktok: ${QUERIES.length} queries + ${HASHTAGS.length} hashtags`);
  const [bySearch, byTag] = await Promise.all([
    runActor("clockworks~tiktok-scraper", {
      searchQueries: QUERIES,
      resultsPerPage: PER_QUERY,
      searchSection: "/video",
      shouldDownloadVideos: false,
      shouldDownloadCovers: false,
      shouldDownloadSubtitles: false,
      proxyCountryCode: "US",
    }),
    runActor("clockworks~tiktok-hashtag-scraper", {
      hashtags: HASHTAGS,
      resultsPerPage: PER_QUERY,
      shouldDownloadVideos: false,
      shouldDownloadCovers: false,
    }),
  ]);
  return [...bySearch, ...byTag].map(normalizeTikTok).filter(Boolean);
}

async function scrapeInstagram() {
  console.log(`  instagram: ${HASHTAGS.length} hashtags`);
  const posts = await runActor("apify~instagram-scraper", {
    search: HASHTAGS.join(" "),
    searchType: "hashtag",
    resultsType: "posts",
    resultsLimit: PER_QUERY * HASHTAGS.length,
    onlyPostsNewerThan: new Date(CUTOFF).toISOString().slice(0, 10),
  });
  const rows = posts.map(normalizeInstagram).filter(Boolean);

  // Hashtag results don't carry follower counts -- backfill from profiles.
  const handles = [...new Set(rows.map((r) => r.username))].slice(0, 300);
  if (!handles.length) return rows;
  const profiles = await runActor("apify~instagram-profile-scraper", { usernames: handles });
  const byHandle = new Map(profiles.map((p) => [p.username, p]));
  for (const r of rows) {
    const p = byHandle.get(r.username);
    if (!p) continue;
    r.followers = num(pick(p.followersCount, p.followers)) || r.followers;
    r.bio = pick(p.biography, "") || r.bio;
  }
  return rows;
}

async function scrapeYouTube() {
  console.log(`  youtube: ${QUERIES.length} queries (shorts)`);
  const items = await runActor("streamers~youtube-scraper", {
    searchQueries: QUERIES,
    maxResults: PER_QUERY,
    maxResultsShorts: PER_QUERY,
    uploadDate: "month",
    sortingOrder: "relevance",
  });
  return items.map(normalizeYouTube).filter(Boolean);
}

// ------------------------------------------------------------------ analysis

const has = (text, words) => {
  const t = text.toLowerCase();
  return words.some((w) => t.includes(w));
};

function groupCreators(rows) {
  const by = new Map();
  for (const r of rows) {
    const key = `${r.platform}:${r.username.toLowerCase()}`;
    if (!by.has(key)) {
      by.set(key, { platform: r.platform, username: r.username, followers: 0, bio: "", samples: [] });
    }
    const c = by.get(key);
    c.followers = Math.max(c.followers, r.followers); // most complete reading wins
    if (!c.bio) c.bio = r.bio;
    c.samples.push(r);
  }
  return [...by.values()];
}

function tierOf(followers) {
  if (followers < 25_000) return "nano";
  if (followers < 100_000) return "micro";
  return "mid";
}

// Rough published-norm rate ladder for UGC with usage rights. An estimate for
// ranking only -- real quotes vary wildly and land in negotiation.
function estimateRate(followers) {
  return Math.max(150, Math.round((followers / 10_000) * 100));
}

const median = (arr) => {
  if (!arr.length) return 0;
  const s = [...arr].sort((a, b) => a - b);
  return s[Math.floor(s.length / 2)];
};

function analyze(c) {
  const text = `${c.bio} ${c.samples.map((s) => s.caption).join(" ")}`;
  const views = c.samples.map((s) => s.views).filter((v) => v > 0);

  c.medianViews = median(views);
  c.bestViews = Math.max(0, ...views);
  c.lastPost = Math.max(...c.samples.map((s) => s.postedAt));

  const totalViews = views.reduce((a, b) => a + b, 0);
  const totalComments = c.samples.reduce((a, s) => a + s.comments, 0);
  const totalLikes = c.samples.reduce((a, s) => a + s.likes, 0);

  // Comments are the cheapest proxy for purchase intent we can measure.
  c.commentRate = totalViews ? (totalComments / totalViews) * 100 : 0;
  c.likeRate = totalViews ? (totalLikes / totalViews) * 100 : 0;
  c.reachMultiple = c.followers ? Number((c.medianViews / c.followers).toFixed(1)) : 0;

  c.estRate = estimateRate(c.followers);
  c.costPerK = c.medianViews ? Number((c.estRate / (c.medianViews / 1000)).toFixed(2)) : Infinity;

  c.formatFit = has(text, FORMAT_FIT);
  c.categories = Object.entries(CATEGORIES).filter(([, w]) => has(text, w)).map(([k]) => k);
  c.cities = Object.entries(CITY_TAGS).filter(([, w]) => has(text, w)).map(([k]) => k);
  c.usSignal = has(text, US_SIGNALS);

  // Posting cadence over the window we scraped.
  const span = Math.max(1, (Date.now() - Math.min(...c.samples.map((s) => s.postedAt))) / 6048e5);
  c.postsPerWeek = Number((c.samples.length / span).toFixed(1));

  c.flags = [];
  if (has(text, DISQUALIFY.giveaway)) c.flags.push("giveaway-farm");
  if (has(text, DISQUALIFY.kids)) c.flags.push("kid-facing");
  // Engagement well outside normal band reads as a pod or bought followers.
  if (c.likeRate > 25) c.flags.push("engagement-anomaly");
  if (c.commentRate > 5) c.flags.push("engagement-anomaly");

  return c;
}

// Weighted for cost-per-conversion. Reach is deliberately last.
function score(c) {
  const commentSignal = Math.min(c.commentRate, 2) * 60;   // intent, capped
  const fit = c.formatFit ? 80 : 0;                        // already shoots reveals
  const efficiency = Number.isFinite(c.costPerK)
    ? Math.max(0, 40 - Math.min(c.costPerK, 40))           // cheaper per 1k = better
    : 0;
  const cadence = Math.min(c.postsPerWeek, 7) * 5;
  const adjacency = c.categories.length * 20;
  const reach = Math.log10(c.medianViews + 1) * 8;         // trails on purpose
  const penalty = c.flags.length * 100;

  return commentSignal + fit + efficiency + cadence + adjacency + reach - penalty;
}

// -------------------------------------------------------------------- reports

const fmt = (n) => (Number.isFinite(n) ? n.toLocaleString("en-US") : "n/a");
const day = (t) => (t ? new Date(t).toISOString().slice(0, 10) : "unknown");
const profileUrl = (c) =>
  c.platform === "tiktok" ? `https://www.tiktok.com/@${c.username}`
  : c.platform === "instagram" ? `https://www.instagram.com/${c.username}/`
  : `https://www.youtube.com/@${c.username}`;

function toMarkdown(platform, creators) {
  const lines = [
    `# Pack-rip creators — ${platform}`,
    "",
    `${fmt(MIN_FOLLOWERS)}–${fmt(MAX_FOLLOWERS)} followers · posted within ${DAYS} days · US.`,
    `Ranked for cost-per-conversion: comment rate and format fit lead, reach trails.`,
    `Generated ${new Date().toISOString().slice(0, 10)}.`,
    "",
  ];

  for (const tier of ["nano", "micro", "mid"]) {
    const group = creators.filter((c) => c.tier === tier);
    lines.push(`## ${tier} (${group.length})`, "");
    if (!group.length) { lines.push("_none matched_", ""); continue; }
    group.forEach((c, i) => {
      lines.push(`### ${i + 1}. @${c.username} — ${fmt(c.followers)} followers`);
      lines.push(`- ${profileUrl(c)}`);
      lines.push(`- Median ${fmt(c.medianViews)} views · ${c.reachMultiple}x followers · comment rate ${c.commentRate.toFixed(2)}%`);
      lines.push(`- Est. $${fmt(c.estRate)}/video → **$${c.costPerK} per 1k views**`);
      lines.push(`- ${c.formatFit ? "**Has shot reveal content**" : "No reveal content found"} · ${c.postsPerWeek} posts/wk · last ${day(c.lastPost)}`);
      lines.push(`- Categories: ${c.categories.join(", ") || "none matched"}${c.cities.length ? ` · ${c.cities.join(", ")}` : ""}`);
      if (c.flags.length) lines.push(`- ⚠️ ${c.flags.join(", ")}`);
      for (const s of [...c.samples].sort((a, b) => b.views - a.views).slice(0, 2)) {
        lines.push(`- ${s.url} — ${fmt(s.views)} views`);
      }
      lines.push("");
    });
  }
  return lines.join("\n");
}

function toCsv(all) {
  const head = "platform,tier,username,followers,median_views,reach_multiple,comment_rate_pct,est_rate_usd,cost_per_1k_views,format_fit,posts_per_week,categories,cities,flags,last_post,profile_url,top_video";
  const rows = all.map((c) => {
    const top = [...c.samples].sort((a, b) => b.views - a.views)[0];
    return [
      c.platform, c.tier, c.username, c.followers, c.medianViews, c.reachMultiple,
      c.commentRate.toFixed(2), c.estRate, Number.isFinite(c.costPerK) ? c.costPerK : "",
      c.formatFit, c.postsPerWeek,
      `"${c.categories.join(" | ")}"`, `"${c.cities.join(" | ")}"`, `"${c.flags.join(" | ")}"`,
      day(c.lastPost), profileUrl(c), top?.url ?? "",
    ].join(",");
  });
  return [head, ...rows].join("\n");
}

// ----------------------------------------------------------------------- main

const SCRAPERS = { tiktok: scrapeTikTok, instagram: scrapeInstagram, youtube: scrapeYouTube };
const all = [];
await mkdir("out", { recursive: true });

for (const platform of PLATFORMS) {
  const scrape = SCRAPERS[platform];
  if (!scrape) { console.log(`\nskip ${platform} (unknown)`); continue; }

  console.log(`\n${platform}`);
  const rows = await scrape();
  console.log(`  ${rows.length} videos scraped`);

  const creators = groupCreators(rows)
    .filter((c) => c.followers >= MIN_FOLLOWERS && c.followers <= MAX_FOLLOWERS)
    .filter((c) => c.samples.some((s) => s.postedAt >= CUTOFF))
    .map(analyze)
    // Keep flagged creators visible but ranked down -- a human should see why
    // they were rejected rather than wonder where they went.
    .filter((c) => !c.flags.includes("kid-facing"));

  for (const c of creators) {
    c.tier = tierOf(c.followers);
    c.rank = score(c);
  }
  creators.sort((a, b) => b.rank - a.rank);

  console.log(`  ${creators.length} creators match (${fmt(MIN_FOLLOWERS)}-${fmt(MAX_FOLLOWERS)}, posted in ${DAYS}d)`);
  await writeFile(`out/creators-${platform}.md`, toMarkdown(platform, creators));
  all.push(...creators);
}

all.sort((a, b) => b.rank - a.rank);
await writeFile("out/creators.csv", toCsv(all));
console.log(`\nWrote out/creators-*.md and out/creators.csv (${all.length} creators).`);
console.log("Top of creators.csv is the outreach queue.");
