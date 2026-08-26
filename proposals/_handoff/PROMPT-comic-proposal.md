# Prompt: Build a comic book sales proposal PDF

Paste everything below into a new Claude conversation, and **attach the slab
photo for each book** (drag them in with the message). Claude will read the CGC
labels from the images, build the PDF, and give it back to you as a file.

---

You are producing a private sales proposal PDF for a high-value comic book
collection. I've attached photos of each CGC-slabbed book. Build the document
with Python + reportlab and give me the finished PDF as a downloadable file.

## Design spec

- US Letter, 9+ pages. Serif body type (Times), sans-serif small-caps labels
  (Helvetica) with generous letter-spacing.
- Palette: deep navy `#1d2433`, gold `#b08d3e`, light gold `#cfb578`, ink
  `#161b26`, warm gray `#5d6470`, cream `#f7f3ea`, faint rule `#c9c4b8`.
- **Cover page:** full-bleed navy with a double gold rule border. Small-caps
  "PRIVATE SALES PROPOSAL" eyebrow, large serif title, italic gold subtitle
  naming the characters, a small centered ornament (two rules + a circle), then
  a centered list of every book with its grade. Footer: presenter name, date,
  "Private & Confidential".
- **Page 2 — "The Offering":** an intro paragraph, then a three-column table
  (WORK / CERTIFICATION / OFFERED AT) with a hairline rule under each row, a
  bold "The collection, entire" total row, and an italic note that prices are
  USD and subject to prior sale.
- **One page per book:** running header ("PRIVATE SALES PROPOSAL" left, month
  right) over a hairline rule; gold "LOT n OF N" eyebrow; large serif title;
  italic "Publisher · Date". Left column: the slab photo, scaled to fit a
  236×372pt panel on a cream ground with a hairline border. Right column: a
  rounded-rect badge with the CGC grade and page quality; a metadata block
  (CGC CERT NO. / STORY / ART / COVER) with small-caps labels — auto-shrink the
  value type so long credits never overflow; a gold "SIGNIFICANCE" heading and
  paragraph; a gold "THIS COPY" heading and paragraph; then a gold rule and the
  price in large serif type.
- **Final page — "Terms & Next Steps":** short sections for Certification,
  Availability, Pricing, Viewing, and Acquisition, then a contact block.
- Every page except the cover gets a footer: "PRIVATE & CONFIDENTIAL" left,
  contact centered in italic, "n / total" right.

## Rules

- Read each attached image's CGC label and use it as the source of truth for
  grade, page quality, certification number, creator credits, and the
  first-appearance notes. Match each photo to its book by the label.
- Never invent a price. Use only the prices listed below.
- Order lots by price, highest first.
- Client-facing document: include asking prices only, never internal cost.

## Presenter

Avery — ArtLife · avery@artlife.com · Private & Confidential

## The books

| Book | Grade | Pages | Cert | Price |
| --- | --- | --- | --- | --- |
| Amazing Fantasy #15 (Marvel, 8/62) | CGC 8.0 | Off-White, **QES sticker** | 1971545001 | $375,000 |
| Marvel Spotlight #5 (Marvel, 8/72) | CGC 9.8 | White | 4757016020 | $325,000 |
| Fantastic Four #1 (Marvel, 11/61) | CGC 8.5 | Off-White | 1201137001 | $220,000 |
| The Incredible Hulk #181 (Marvel, 11/74) | CGC 9.8 | Off-White to White | 4748401011 | $80,000 |
| The Amazing Spider-Man #13 (Marvel, 6/64) | CGC 9.4 | White | 3949630002 | $27,500 |
| Action Comics #241 (DC, 6/58) | CGC 9.2 | White | 4614192004 | $27,500 |

Collection total: **$1,055,000**

### Creator credits and significance

- **Amazing Fantasy #15** — Stan Lee story, Steve Ditko art, Jack Kirby cover.
  Origin and 1st appearance of Spider-Man (Peter Parker); 1st appearance of
  Uncle Ben and Aunt May. The definitive Silver Age key. Note the QES (Quality
  Evaluation Service) sticker: an independent endorsement of superior quality
  within the grade, assessing color strike, spine, cover edges, and staple
  placement.
- **Marvel Spotlight #5** — Gary Friedrich and Roy Thomas story, Mike Ploog
  cover and art. Origin and 1st appearance of Ghost Rider (Johnny Blaze); 1st
  appearance of Roxanne Simpson.
- **Fantastic Four #1** — Stan Lee story, Jack Kirby cover and art. Origin and
  1st appearance of the Fantastic Four (Marvel's first super-hero team) and the
  Mole Man. The book that launched the Marvel Universe.
- **The Incredible Hulk #181** — Len Wein story, Herb Trimpe and Jack Abel art,
  Herb Trimpe and John Romita cover. 1st full appearance of Wolverine (James
  "Logan" Howlett); Wendigo appearance. The most important Bronze Age comic.
- **The Amazing Spider-Man #13** — Stan Lee story, Steve Ditko cover and art.
  Origin and 1st appearance of Mysterio (Quentin Beck).
- **Action Comics #241** — Jerry Coleman and Otto Binder stories; Wayne Boring,
  Jim Mooney and Howard Sherman art; Curt Swan cover. 1st appearance of the
  Fortress of Solitude ("Fort Superman") in "The Super-Key to Fort Superman";
  Batman appearance.

### Optional extra lots — only if I give you a price

- **The Incredible Hulk #1** (Marvel, 5/62) — CGC 8.0, Off-White to White,
  **QES sticker**, cert 3832523002. Stan Lee story; Jack Kirby and Paul Reinman
  art; Jack Kirby and George Roussos cover. Origin and 1st appearance of the
  Incredible Hulk; 1st appearance of Rick Jones, Betty Ross, and General Ross.
- **A second Amazing Fantasy #15** — CGC 8.0, Off-White to White, cert
  4615094001. A different copy from the one above (which is Off-White with QES).
