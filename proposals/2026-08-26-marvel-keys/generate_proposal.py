#!/usr/bin/env python3
"""Generate the private sales proposal PDF for the Aug 2026 comic keys group.

Cover images: drop files into ./covers/ named by each book's key
(af15, ms5, ff1, hulk181, asm13, action241) with a .jpg or .png extension
and re-run this script; any book without an image gets a typographic panel.
"""

import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
COVERS = os.path.join(HERE, "covers")
OUT = os.path.join(HERE, "Private-Sales-Proposal-Comic-Keys-Aug-2026.pdf")

W, H = letter  # 612 x 792

INK = HexColor("#161b26")
NAVY = HexColor("#1d2433")
GOLD = HexColor("#b08d3e")
GOLD_LIGHT = HexColor("#cfb578")
CREAM = HexColor("#f7f3ea")
GRAY = HexColor("#5d6470")
FAINT = HexColor("#c9c4b8")
WHITE = HexColor("#ffffff")

BOOKS = [
    {
        "key": "af15",
        "title": "Amazing Fantasy #15",
        "publisher": "Marvel Comics",
        "year": "August 1962",
        "grade": "CGC 8.0",
        "grade_note": "Off-White Pages · QES",
        "table_note": "Off-White · QES Sticker",
        "cert": "1971545001",
        "story": "Stan Lee",
        "art": "Steve Ditko",
        "cover": "Jack Kirby",
        "significance": "The origin and first appearance of Spider-Man (Peter "
        "Parker), along with the first appearances of Uncle Ben and Aunt May. "
        "The single most important Silver Age comic book and the definitive "
        "Marvel key.",
        "condition": "A handsome high-grade copy with off-white pages, bearing "
        "a QES (Quality Evaluation Service) sticker — an independent "
        "endorsement of superior quality within the grade, assessing color "
        "strike, spine, cover edges, and staple placement.",
        "price": "$375,000",
        "price_note": None,
        "abbrev": ("AMAZING FANTASY", "No. 15"),
    },
    {
        "key": "ms5",
        "title": "Marvel Spotlight #5",
        "publisher": "Marvel Comics",
        "year": "August 1972",
        "grade": "CGC 9.8",
        "grade_note": "White Pages",
        "table_note": "White Pages",
        "cert": "4757016020",
        "story": "Gary Friedrich & Roy Thomas",
        "art": "Mike Ploog",
        "cover": "Mike Ploog",
        "significance": "The origin and first appearance of Ghost Rider "
        "(Johnny Blaze), with the first appearance of Roxanne Simpson. The "
        "defining supernatural key of the Bronze Age, behind a classic Mike "
        "Ploog cover.",
        "condition": "A stunning CGC 9.8 with white pages — the top tier of "
        "certified examples of this book, and the grade sophisticated "
        "collectors compete for.",
        "price": "$325,000",
        "price_note": None,
        "abbrev": ("MARVEL SPOTLIGHT", "No. 5"),
    },
    {
        "key": "ff1",
        "title": "Fantastic Four #1",
        "publisher": "Marvel Comics",
        "year": "November 1961",
        "grade": "CGC 8.5",
        "grade_note": "Off-White Pages",
        "table_note": "Off-White Pages",
        "cert": "1201137001",
        "story": "Stan Lee",
        "art": "Jack Kirby",
        "cover": "Jack Kirby",
        "significance": "The origin and first appearance of the Fantastic "
        "Four — Marvel's first super-hero team — and the Mole Man. The book "
        "that launched the Marvel Universe and, with it, the modern age of "
        "comics.",
        "condition": "A strong, well-presenting high-grade copy with off-white "
        "pages. Fantastic Four #1 is notoriously difficult in grades above "
        "Very Fine, making an 8.5 a genuine collection centerpiece.",
        "price": "$220,000",
        "price_note": None,
        "abbrev": ("FANTASTIC FOUR", "No. 1"),
    },
    {
        "key": "hulk181",
        "title": "The Incredible Hulk #181",
        "publisher": "Marvel Comics",
        "year": "November 1974",
        "grade": "CGC 9.8",
        "grade_note": "Off-White to White Pages",
        "table_note": "Off-White to White",
        "cert": "4748401011",
        "story": "Len Wein",
        "art": "Herb Trimpe & Jack Abel",
        "cover": "Herb Trimpe & John Romita",
        "significance": "The first full appearance of Wolverine (James "
        "“Logan” Howlett), with a Wendigo appearance. The most "
        "important Bronze Age comic book and one of the most demanded keys "
        "in the entire hobby.",
        "condition": "A pristine CGC 9.8 with off-white to white pages — the "
        "trophy grade for this perennially sought-after book.",
        "price": "$80,000",
        "price_note": None,
        "abbrev": ("INCREDIBLE HULK", "No. 181"),
    },
    {
        "key": "asm13",
        "title": "The Amazing Spider-Man #13",
        "publisher": "Marvel Comics",
        "year": "June 1964",
        "grade": "CGC 9.4",
        "grade_note": "White Pages",
        "table_note": "White Pages",
        "cert": "3949630002",
        "story": "Stan Lee",
        "art": "Steve Ditko",
        "cover": "Steve Ditko",
        "significance": "The origin and first appearance of Mysterio (Quentin "
        "Beck), one of the great villains of Spider-Man's rogues' gallery, "
        "with cover and interior art by Steve Ditko.",
        "condition": "An exceptional CGC 9.4 with white pages — outstanding "
        "preservation for an early Ditko Amazing Spider-Man issue.",
        "price": "$27,500",
        "price_note": None,
        "abbrev": ("AMAZING SPIDER-MAN", "No. 13"),
    },
    {
        "key": "action241",
        "title": "Action Comics #241",
        "publisher": "DC Comics",
        "year": "June 1958",
        "grade": "CGC 9.2",
        "grade_note": "White Pages",
        "table_note": "White Pages",
        "cert": "4614192004",
        "story": "Jerry Coleman & Otto Binder",
        "art": "Wayne Boring, Jim Mooney & Howard Sherman",
        "cover": "Curt Swan",
        "significance": "The first appearance of the Fortress of Solitude "
        "(“Fort Superman”), one of the enduring pillars of Superman mythology, "
        "in the story “The Super-Key to Fort Superman.” Also features a Batman "
        "appearance, behind a classic Curt Swan cover.",
        "condition": "A superb CGC 9.2 with white pages — a genuinely scarce "
        "state of preservation for a late-1950s DC title, and the top end of "
        "the market for this key.",
        "price": "$27,500",
        "price_note": None,
        "abbrev": ("ACTION COMICS", "No. 241"),
    },
]

COLLECTION_TOTAL = "$1,055,000"

DOC_LABEL = "PRIVATE SALES PROPOSAL"
DOC_DATE = "August 26, 2026"
CONTACT = "Avery  ·  avery@artlife.com"


def find_cover(key):
    for ext in ("jpg", "jpeg", "png"):
        p = os.path.join(COVERS, f"{key}.{ext}")
        if os.path.exists(p):
            return p
    return None


def small_caps(c, x, y, text, size, color, tracking=1.6, font="Helvetica"):
    c.setFont(font, size)
    c.setFillColor(color)
    cx = x
    for ch in text:
        c.drawString(cx, y, ch)
        cx += c.stringWidth(ch, font, size) + tracking


def small_caps_width(c, text, size, tracking=1.6, font="Helvetica"):
    return sum(c.stringWidth(ch, font, size) for ch in text) + tracking * (len(text) - 1)


def small_caps_centered(c, cx, y, text, size, color, tracking=1.6, font="Helvetica"):
    small_caps(c, cx - small_caps_width(c, text, size, tracking, font) / 2, y, text, size, color, tracking, font)


def small_caps_fit(c, cx, y, text, size, color, max_width, tracking=2.6, font="Helvetica-Bold"):
    while size > 6 and small_caps_width(c, text, size, tracking, font) > max_width:
        size -= 0.5
    small_caps_centered(c, cx, y, text, size, color, tracking, font)


def para(c, text, x, y, w, h, style):
    f = Frame(x, y, w, h, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList([Paragraph(text, style)], c)


BODY = ParagraphStyle("body", fontName="Times-Roman", fontSize=10.5, leading=15.5, textColor=INK)
BODY_ITAL = ParagraphStyle("bodyi", fontName="Times-Italic", fontSize=10, leading=14.5, textColor=GRAY)


def footer(c, page_num, total):
    c.setStrokeColor(FAINT)
    c.setLineWidth(0.6)
    c.line(54, 46, W - 54, 46)
    small_caps(c, 54, 33, "PRIVATE & CONFIDENTIAL", 6.5, GRAY, 1.4)
    c.setFont("Times-Italic", 8.5)
    c.setFillColor(GRAY)
    c.drawCentredString(W / 2, 32.5, CONTACT.replace("  ·  ", "   ·   "))
    c.setFont("Helvetica", 7)
    c.drawRightString(W - 54, 33, f"{page_num}  /  {total}")


def header(c):
    small_caps(c, 54, H - 52, DOC_LABEL, 7, GRAY, 2.2)
    txt = "AUGUST 2026"
    small_caps(c, W - 54 - small_caps_width(c, txt, 7, 2.2), H - 52, txt, 7, GOLD, 2.2)
    c.setStrokeColor(FAINT)
    c.setLineWidth(0.6)
    c.line(54, H - 62, W - 54, H - 62)


def cover_page(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.rect(40, 40, W - 80, H - 80, fill=0, stroke=1)
    c.setLineWidth(0.4)
    c.rect(46, 46, W - 92, H - 92, fill=0, stroke=1)

    small_caps_centered(c, W / 2, H - 175, DOC_LABEL, 11, GOLD_LIGHT, 5)

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.7)
    c.line(W / 2 - 90, H - 200, W / 2 + 90, H - 200)

    c.setFillColor(WHITE)
    c.setFont("Times-Roman", 34)
    c.drawCentredString(W / 2, H - 300, "Six Certified")
    c.drawCentredString(W / 2, H - 344, "Comic Book Keys")

    c.setFont("Times-Italic", 12.5)
    c.setFillColor(GOLD_LIGHT)
    c.drawCentredString(W / 2, H - 386, "Spider-Man · Ghost Rider · The Fantastic Four")
    c.drawCentredString(W / 2, H - 404, "Wolverine · Mysterio · Superman")

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.7)
    c.line(W / 2 - 60, H - 440, W / 2 - 12, H - 440)
    c.line(W / 2 + 12, H - 440, W / 2 + 60, H - 440)
    c.circle(W / 2, H - 440, 3.2, fill=0, stroke=1)

    y = 268
    for line in [
        "Amazing Fantasy #15  ·  CGC 8.0  ·  QES",
        "Marvel Spotlight #5  ·  CGC 9.8",
        "Fantastic Four #1  ·  CGC 8.5",
        "The Incredible Hulk #181  ·  CGC 9.8",
        "The Amazing Spider-Man #13  ·  CGC 9.4",
        "Action Comics #241  ·  CGC 9.2",
    ]:
        c.setFont("Times-Roman", 11.5)
        c.setFillColor(HexColor("#dcd5c4"))
        c.drawCentredString(W / 2, y, line)
        y -= 21

    small_caps_centered(c, W / 2, 118, "PRESENTED BY", 7, GRAY, 2.4)
    c.setFont("Times-Roman", 12)
    c.setFillColor(WHITE)
    c.drawCentredString(W / 2, 98, "Avery — ArtLife")
    c.setFont("Times-Italic", 9.5)
    c.setFillColor(GOLD_LIGHT)
    c.drawCentredString(W / 2, 82, f"{DOC_DATE}   ·   Private & Confidential")
    c.showPage()


def summary_page(c, page_num, total):
    header(c)
    c.setFont("Times-Roman", 24)
    c.setFillColor(INK)
    c.drawString(54, H - 120, "The Offering")

    intro = (
        "We are pleased to present a private opportunity to acquire six certified "
        "keys spanning the Silver and Bronze Ages: the first appearances of the "
        "Fantastic Four, Spider-Man, Mysterio, Ghost Rider, and Wolverine, together "
        "with the debut of Superman's Fortress of Solitude. Every book is "
        "professionally graded and encapsulated by CGC, with the certification "
        "number, page quality, and creative credits set out in the pages that "
        "follow. The group leads with an Amazing Fantasy #15 carrying a QES "
        "sticker — independent recognition of superior quality within its grade."
    )
    para(c, intro, 54, H - 265, W - 108, 125, BODY)

    ty = H - 300
    small_caps(c, 54, ty, "WORK", 7, GRAY, 1.8)
    small_caps(c, 300, ty, "CERTIFICATION", 7, GRAY, 1.8)
    small_caps(c, 462, ty, "OFFERED AT", 7, GRAY, 1.8)
    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.line(54, ty - 8, W - 54, ty - 8)

    y = ty - 36
    for b in BOOKS:
        c.setFont("Times-Roman", 12)
        c.setFillColor(INK)
        c.drawString(54, y, b["title"])
        c.setFont("Helvetica", 8.5)
        c.setFillColor(GRAY)
        c.drawString(300, y + 0.5, f"{b['grade']}  ·  {b['table_note']}")
        c.setFont("Times-Roman", 12)
        c.setFillColor(INK)
        c.drawRightString(W - 54, y, b["price"])
        c.setStrokeColor(FAINT)
        c.setLineWidth(0.5)
        c.line(54, y - 11, W - 54, y - 11)
        y -= 32

    c.setFont("Times-Roman", 12.5)
    c.setFillColor(INK)
    c.drawString(54, y - 6, "The collection, entire")
    c.drawRightString(W - 54, y - 6, COLLECTION_TOTAL)
    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.line(54, y - 18, W - 54, y - 18)

    note = (
        "Detailed presentations of each book follow. All prices are quoted in U.S. "
        "dollars; availability is subject to confirmation and prior sale."
    )
    para(c, note, 54, y - 70, W - 108, 40, BODY_ITAL)
    footer(c, page_num, total)
    c.showPage()


def placeholder_panel(c, x, y, w, h, book):
    c.setFillColor(CREAM)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.rect(x + 8, y + 8, w - 16, h - 16, fill=0, stroke=1)
    c.setLineWidth(0.4)
    c.rect(x + 12, y + 12, w - 24, h - 24, fill=0, stroke=1)

    cx = x + w / 2
    cy = y + h / 2
    name, number = book["abbrev"]

    small_caps_fit(c, cx, cy + 46, name, 12, INK, w - 44)
    c.setFont("Times-Roman", 30)
    c.setFillColor(GOLD)
    c.drawCentredString(cx, cy + 4, number)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(cx - 34, cy - 14, cx + 34, cy - 14)
    c.setFont("Times-Italic", 9.5)
    c.setFillColor(GRAY)
    c.drawCentredString(cx, cy - 34, book["year"])
    c.setFont("Times-Italic", 8)
    c.drawCentredString(cx, y + 30, "Photography of the certified copy")
    c.drawCentredString(cx, y + 19, "available upon request")


def image_panel(c, x, y, w, h, path):
    img = ImageReader(path)
    iw, ih = img.getSize()
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
    c.setFillColor(CREAM)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.drawImage(img, dx, dy, dw, dh, preserveAspectRatio=True, mask="auto")
    c.setStrokeColor(FAINT)
    c.setLineWidth(0.6)
    c.rect(dx, dy, dw, dh, fill=0, stroke=1)


def book_page(c, book, idx, page_num, total):
    header(c)

    small_caps(c, 54, H - 100, f"LOT {idx}  OF  {len(BOOKS)}", 7.5, GOLD, 2.2)

    c.setFont("Times-Roman", 25)
    c.setFillColor(INK)
    c.drawString(54, H - 130, book["title"])
    c.setFont("Times-Italic", 11)
    c.setFillColor(GRAY)
    c.drawString(54, H - 150, f"{book['publisher']}  ·  {book['year']}")

    px, py, pw, ph = 54, 170, 236, 372
    cover = find_cover(book["key"])
    if cover:
        image_panel(c, px, py, pw, ph, cover)
    else:
        placeholder_panel(c, px, py, pw, ph, book)

    rx = 322
    rw = W - 54 - rx

    by = 500
    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.roundRect(rx, by, rw, 46, 4, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(INK)
    c.drawString(rx + 14, by + 17, book["grade"])
    if book["grade_note"]:
        small_caps(c, rx + 92, by + 19.5, book["grade_note"].upper(), 6.4, GOLD, 1.1)
    small_caps(c, rx + 14, by + 34.5, "CERTIFIED GRADE", 5.8, GRAY, 1.6)

    meta = [
        ("CGC CERT NO.", book["cert"]),
        ("STORY", book["story"]),
        ("ART", book["art"]),
        ("COVER", book["cover"]),
    ]
    my = 476
    value_x = rx + 78
    value_max = W - 54 - value_x
    for label, value in meta:
        small_caps(c, rx, my, label, 6, GRAY, 1.3)
        size = 9.5
        while size > 6.5 and c.stringWidth(value, "Times-Roman", size) > value_max:
            size -= 0.25
        c.setFont("Times-Roman", size)
        c.setFillColor(INK)
        c.drawString(value_x, my - 0.5, value)
        my -= 14.5

    small_caps(c, rx, 396, "SIGNIFICANCE", 7, GOLD, 2)
    para(c, book["significance"], rx, 302, rw, 88, BODY)

    small_caps(c, rx, 282, "THIS COPY", 7, GOLD, 2)
    para(c, book["condition"], rx, 192, rw, 84, BODY)

    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(rx, 172, rx + rw, 172)
    small_caps(c, rx, 152, "OFFERED AT", 7, GRAY, 2)
    c.setFont("Times-Roman", 26)
    c.setFillColor(INK)
    c.drawString(rx, 120, book["price"])
    if book["price_note"]:
        para(c, book["price_note"], rx, 76, rw, 38, BODY_ITAL)

    footer(c, page_num, total)
    c.showPage()


def terms_page(c, page_num, total):
    header(c)
    c.setFont("Times-Roman", 24)
    c.setFillColor(INK)
    c.drawString(54, H - 120, "Terms & Next Steps")

    items = [
        ("Certification", "Every book in this offering has been graded and "
         "encapsulated by Certified Guaranty Company (CGC), the industry's leading "
         "third-party certification service; certification numbers are printed with "
         "each lot and can be verified against the CGC registry. Amazing Fantasy #15 "
         "additionally bears a QES (Quality Evaluation Service) sticker, an "
         "independent mark of superior quality within its grade."),
        ("Availability", "All works are offered subject to availability and prior "
         "sale. The collection may be acquired entire for " + COLLECTION_TOTAL + "."),
        ("Pricing", "Prices are quoted in U.S. dollars and are exclusive of any "
         "applicable taxes, shipping, and insurance. Terms of payment will be set "
         "out in the invoice."),
        ("Viewing", "Private viewings can be arranged. High-resolution photography "
         "of each certified copy, including slab and label, is available upon "
         "request."),
        ("Acquisition", "To proceed with any individual book or the collection as "
         "a whole, or to discuss terms, please contact us directly. Given the "
         "caliber of this material, we recommend prompt commitment to secure "
         "availability."),
    ]

    y = H - 170
    for title, body in items:
        small_caps(c, 54, y, title.upper(), 7.5, GOLD, 2)
        para(c, body, 54, y - 66, W - 108, 60, BODY)
        y -= 92

    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.line(54, y + 4, W - 54, y + 4)
    small_caps(c, 54, y - 22, "CONTACT", 7.5, GRAY, 2)
    c.setFont("Times-Roman", 13)
    c.setFillColor(INK)
    c.drawString(54, y - 44, "Avery")
    c.setFont("Times-Roman", 10.5)
    c.setFillColor(GRAY)
    c.drawString(54, y - 60, "avery@artlife.com")

    footer(c, page_num, total)
    c.showPage()


def main():
    c = canvas.Canvas(OUT, pagesize=letter)
    c.setTitle("Private Sales Proposal — Six Certified Comic Book Keys")
    c.setAuthor("Avery — ArtLife")
    total = 3 + len(BOOKS)
    cover_page(c)
    summary_page(c, 2, total)
    for i, book in enumerate(BOOKS, 1):
        book_page(c, book, i, 2 + i, total)
    terms_page(c, total, total)
    c.save()
    print(f"Wrote {OUT}")
    missing = [b["key"] for b in BOOKS if not find_cover(b["key"])]
    if missing:
        print(f"Placeholder panels used for: {', '.join(missing)}")


if __name__ == "__main__":
    main()
