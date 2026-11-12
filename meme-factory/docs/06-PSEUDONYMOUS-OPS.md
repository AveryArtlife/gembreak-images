# 06 · Pseudonymous operations: domains, handles, payments, wallets

**What this buys you:** the public, competitors, and reporters can't tie the launches to you. **What it does not buy you:** anonymity from registrars, exchanges, platforms or courts; all of them keep records and answer subpoenas. That is fine. The goal is a clean public persona, not evasion. Everything below is legal; the places where a platform's terms bite are marked.

## 1. Identity layer
- Create a **persona** (name, avatar, voice) once and reuse it across every launch. Pseudonymous founders are normal in memecoins; what gets punished is *inconsistency*, not anonymity.
- Dedicated email: Proton or Tuta, created over VPN, no recovery phone tied to you. Optionally a second one for registrars/billing.
- Dedicated device or at minimum a dedicated browser profile; VPN paid in crypto (Mullvad accepts Monero). Never log the persona in on your personal phone.
- Strip metadata from every image and video before posting (EXIF, filenames). Watch time-zone leaks in screenshots and posting patterns.

## 2. Domains
| Option | Anonymity | Payment | Notes |
|---|---|---|---|
| **Njalla** (njal.la) | Highest: Njalla is the legal registrant, you are the "customer"; only an email/XMPP is required | Bitcoin, Monero, Litecoin, Dash, PayPal | ~$15–30/yr; the trade-off is that Njalla technically owns the domain. Good for the launch sites, not for the brand you want to own for years. |
| Porkbun / Namecheap with WHOIS privacy | Standard: WHOIS redacted, registrar has your details | Card; Namecheap has accepted crypto via BitPay | Use the persona email; pay with a prepaid card or crypto where offered. |
| Cloudflare Registrar | WHOIS redacted; good DNS/proxy | Card | Cloudflare proxying also hides your hosting origin. |
| `.sol` / ENS names | On-chain, pseudonymous by default | Crypto | Cheap brand insurance (`chachaforever.sol`), not a substitute for a web domain. |

Register the `.com` for the flagship brand through the registrar you trust to keep it (Porkbun/Cloudflare, persona identity); use Njalla for throwaway launch domains in the factory.

## 3. Hosting
- Static sites (this kit) on Vercel or Cloudflare Pages under the persona account, or on Njalla's VPS / 1984.hosting / MyNymBox (Monero) if you want the hosting account anonymous too.
- Put Cloudflare in front so the origin IP is never public. IPFS via Fleek is a fine mirror.

## 4. Social handles
- **X**: requires a phone number for most new accounts and for anything that looks automated; VoIP numbers are usually rejected. A **prepaid SIM bought with cash** is legal and is the standard answer. Age the account for a week with normal activity before launch; buying aged accounts breaks ToS and they get mass-suspended.
- **Telegram**: phone number required; same prepaid SIM; create the group from the official app, add bots (Rose/Combot) for moderation. Automating a *user* account (MTProto) that floods gets permanent bans, so bots post, humans talk.
- **TikTok/Instagram**: email signup works; phone for 2FA. Instagram embeds of other people's posts are the clean way to show real photos.
- Register the same handle everywhere before the story is public: `@<name>forever`, `@<name>sol`, `t.me/<name>`.
- Apply for X's paid API (pay-per-use since Feb 2026) under the persona for scheduled posting. Keep community replies human.

## 5. Payments
- Crypto first (USDC/SOL/XMR where accepted), prepaid cards second. Keep a persona-only card.
- KOLs and vendors are paid from the **treasury multisig**, with the disclosure line in the post. The on-chain trail is a feature: it is your receipt.

## 6. Wallet hygiene
- Fresh launch, treasury and pledge wallets per project. Fund them from an exchange account you control (KYC'd, which is fine: invisible to the public, visible to authorities).
- Never move funds between a persona wallet and any wallet linked to your name, ENS, or a doxxed NFT. Bubblemaps and Arkham cluster by funding path, and so does every curious trader.
- Hardware wallet for the multisig signers; separate seed per project.

## 7. What still exposes you
- Your own behaviour: reusing a wallet, posting from the wrong account, a voice on a livestream, a photo with a reflection.
- Legal process: registrars, CEXs, Vercel and X all comply with subpoenas. Pseudonymity is not a defence to anything on the red list in `05-LEGAL-LINES.md`.
- Payment processors for merch and donations: use crypto-native rails or accept that the processor knows the entity.

## 8. The other option
Some of the biggest 2024–2026 launches had a **doxxed** founder on a livestream (pump.fun's stream meta rewards it). A known face is the single fastest trust accelerator. Decide per brand: the factory can be pseudonymous while a flagship like Cha Cha Forever is fronted by a real person.
