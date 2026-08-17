#!/usr/bin/env python3
"""Generate the private sales proposal PDF for the Aug 2026 comic want list.

Cover images: drop files into ./covers/ named by each book's key
(action1, ff1, af15, hulk1, allstar8) with a .jpg or .png extension and
re-run this script; any book without an image gets a typographic panel.
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
OUT = os.path.join(HERE, "Private-Sales-Proposal-Comics-Aug-2026.pdf")

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
        "key": "action1",
        "title": "Action Comics #1",
        "publisher": "DC Comics",
        "year": "June 1938",
        "grade": "CGC 9.0",
        "grade_note": "Slight Restoration",
        "significance": "The first appearance of Superman and the birth of the "
        "superhero genre itself. Action Comics #1 is the most important comic "
        "book ever published and the cornerstone of any world-class collection.",
        "condition": "An exceptionally well-preserved copy. The consignor — among "
        "the most experienced Action #1 dealers in the world — describes it as "
        "one of the nicest copies he has ever handled.",
        "price": "$1,400,000",
        "price_note": None,
    },
    {
        "key": "ff1",
        "title": "Fantastic Four #1",
        "publisher": "Marvel Comics",
        "year": "November 1961",
        "grade": "CGC 9.2",
        "grade_note": "White Mountain Pedigree",
        "significance": "The book that launched the Marvel Universe. Stan Lee and "
        "Jack Kirby's Fantastic Four #1 marks the beginning of the Silver Age "
        "Marvel dynasty and remains one of the most sought-after keys in the hobby.",
        "condition": "One of the finest copies in the world, from the White "
        "Mountain pedigree — one of the most highly respected pedigree "
        "collections known to the market.",
        "price": "Price upon request",
        "price_note": None,
    },
    {
        "key": "af15",
        "title": "Amazing Fantasy #15",
        "publisher": "Marvel Comics",
        "year": "August 1962",
        "grade": "CGC 9.6",
        "grade_note": "Highest Graded (tied with three others)",
        "significance": "The first appearance of Spider-Man — the most valuable "
        "Silver Age comic book in existence. Copies in this grade essentially "
        "never reach the open market.",
        "condition": "The single highest grade awarded by CGC for this issue, "
        "shared with only three other copies worldwide. A generational "
        "acquisition opportunity.",
        "price": "$10,000,000",
        "price_note": None,
    },
    {
        "key": "hulk1",
        "title": "The Incredible Hulk #1",
        "publisher": "Marvel Comics",
        "year": "May 1962",
        "grade": "CGC 9.2",
        "grade_note": None,
        "significance": "The first appearance of the Hulk, by Stan Lee and Jack "
        "Kirby. Notoriously difficult to find in high grade due to its "
        "poorly-printed gray cover, which shows every flaw.",
        "condition": "A superb high-grade example of one of the most "
        "condition-sensitive keys of the Silver Age.",
        "price": "$900,000",
        "price_note": None,
    },
    {
        "key": "allstar8",
        "title": "All Star Comics #8",
        "publisher": "DC Comics",
        "year": "December 1940",
        "grade": "CGC 9.4",
        "grade_note": None,
        "significance": "The first appearance of Wonder Woman — the most "
        "important female character debut in comics history and a Golden Age "
        "key of the first rank.",
        "condition": "An extraordinary near-mint copy of a book rarely seen in "
        "any high grade.",
        "price": "$2,000,000",
        "price_note": "Subject to availability — currently being sourced from a "
        "private holder.",
    },
]

DOC_LABEL = "PRIVATE SALES PROPOSAL"
DOC_DATE = "August 17, 2026"
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


def para(c, text, x, y, w, h, style):
    f = Frame(x, y, w, h, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList([Paragraph(text, style)], c)


BODY = ParagraphStyle("body", fontName="Times-Roman", fontSize=10.5, leading=15.5, textColor=INK)
BODY_GRAY = ParagraphStyle("bodyg", fontName="Times-Roman", fontSize=10.5, leading=15.5, textColor=GRAY)
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
    # frame rules
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
    c.drawCentredString(W / 2, H - 300, "Five Museum-Grade")
    c.drawCentredString(W / 2, H - 344, "Comic Books")

    c.setFont("Times-Italic", 13.5)
    c.setFillColor(GOLD_LIGHT)
    c.drawCentredString(W / 2, H - 386, "A Curated Offering of Golden & Silver Age Keys")

    # centered ornament
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.7)
    c.line(W / 2 - 60, H - 425, W / 2 - 12, H - 425)
    c.line(W / 2 + 12, H - 425, W / 2 + 60, H - 425)
    c.circle(W / 2, H - 425, 3.2, fill=0, stroke=1)

    y = 250
    for line in [
        "Action Comics #1  ·  CGC 9.0",
        "Fantastic Four #1  ·  CGC 9.2  White Mountain",
        "Amazing Fantasy #15  ·  CGC 9.6",
        "The Incredible Hulk #1  ·  CGC 9.2",
        "All Star Comics #8  ·  CGC 9.4",
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
        "We are pleased to present a private opportunity to acquire five of the most "
        "important comic books ever published, each professionally certified by CGC. "
        "Together they span the two defining character debuts of the Golden Age — "
        "Superman and Wonder Woman — and the three cornerstones of the Marvel Silver "
        "Age: the Fantastic Four, Spider-Man, and the Hulk. Individually or as a group, "
        "these books represent a caliber of material that reaches the market only rarely, "
        "and almost never in these grades."
    )
    para(c, intro, 54, H - 260, W - 108, 120, BODY)

    # table
    ty = H - 300
    small_caps(c, 54, ty, "WORK", 7, GRAY, 1.8)
    small_caps(c, 320, ty, "CERTIFICATION", 7, GRAY, 1.8)
    small_caps(c, 462, ty, "OFFERED AT", 7, GRAY, 1.8)
    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.line(54, ty - 8, W - 54, ty - 8)

    rows = [
        (b["title"], b["grade"] + (f"  ·  {b['grade_note']}" if b["grade_note"] and len(b["grade_note"]) < 30 else ""), b["price"])
        for b in BOOKS
    ]
    y = ty - 36
    for i, (title, grade, price) in enumerate(rows):
        c.setFont("Times-Roman", 12)
        c.setFillColor(INK)
        c.drawString(54, y, title)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(GRAY)
        c.drawString(320, y + 0.5, grade)
        if price.startswith("$"):
            c.setFont("Times-Roman", 12)
            c.setFillColor(INK)
        else:
            c.setFont("Times-Italic", 10.5)
            c.setFillColor(GRAY)
        c.drawRightString(W - 54, y, price)
        c.setStrokeColor(FAINT)
        c.setLineWidth(0.5)
        c.line(54, y - 11, W - 54, y - 11)
        y -= 32

    note = (
        "Detailed presentations of each book follow. All prices are quoted in U.S. "
        "dollars. Availability and pricing are subject to confirmation and prior sale; "
        "the price for Fantastic Four #1 will be quoted upon request."
    )
    para(c, note, 54, y - 70, W - 108, 55, BODY_ITAL)
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

    abbrev = {
        "action1": ("ACTION", "No. 1"),
        "ff1": ("FANTASTIC FOUR", "No. 1"),
        "af15": ("AMAZING FANTASY", "No. 15"),
        "hulk1": ("INCREDIBLE HULK", "No. 1"),
        "allstar8": ("ALL STAR", "No. 8"),
    }[book["key"]]

    small_caps_centered(c, cx, cy + 46, abbrev[0], 12, INK, 2.6, "Helvetica-Bold")
    c.setFont("Times-Roman", 30)
    c.setFillColor(GOLD)
    c.drawCentredString(cx, cy + 4, abbrev[1])
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(cx - 34, cy - 14, cx + 34, cy - 14)
    c.setFont("Times-Italic", 9.5)
    c.setFillColor(GRAY)
    c.drawCentredString(cx, cy - 34, book["year"])
    c.setFont("Times-Italic", 8)
    c.drawCentredString(cx, y + 30, "Cover photography of the certified copy")
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

    # numbered eyebrow
    small_caps(c, 54, H - 100, f"LOT {idx}  OF  {len(BOOKS)}", 7.5, GOLD, 2.2)

    c.setFont("Times-Roman", 26)
    c.setFillColor(INK)
    c.drawString(54, H - 130, book["title"])
    c.setFont("Times-Italic", 11)
    c.setFillColor(GRAY)
    c.drawString(54, H - 150, f"{book['publisher']}  ·  {book['year']}")

    # image panel, left
    px, py, pw, ph = 54, 170, 236, 372
    cover = find_cover(book["key"])
    if cover:
        image_panel(c, px, py, pw, ph, cover)
    else:
        placeholder_panel(c, px, py, pw, ph, book)

    # right column
    rx = 322
    rw = W - 54 - rx

    # grade badge
    by = 496
    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.roundRect(rx, by, rw, 46, 4, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(INK)
    c.drawString(rx + 14, by + 17, book["grade"])
    if book["grade_note"]:
        small_caps(c, rx + 92, by + 19.5, book["grade_note"].upper(), 6.4, GOLD, 1.1)
    small_caps(c, rx + 14, by + 34.5, "CERTIFIED GRADE", 5.8, GRAY, 1.6)

    small_caps(c, rx, 462, "SIGNIFICANCE", 7, GOLD, 2)
    para(c, book["significance"], rx, 370, rw, 86, BODY)

    small_caps(c, rx, 348, "THIS COPY", 7, GOLD, 2)
    para(c, book["condition"], rx, 262, rw, 80, BODY)

    # price block
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(rx, 232, rx + rw, 232)
    small_caps(c, rx, 212, "OFFERED AT", 7, GRAY, 2)
    if book["price"].startswith("$"):
        c.setFont("Times-Roman", 26)
        c.setFillColor(INK)
        c.drawString(rx, 180, book["price"])
    else:
        c.setFont("Times-Italic", 19)
        c.setFillColor(INK)
        c.drawString(rx, 184, book["price"])
    if book["price_note"]:
        para(c, book["price_note"], rx, 134, rw, 40, BODY_ITAL)

    footer(c, page_num, total)
    c.showPage()


def terms_page(c, page_num, total):
    header(c)
    c.setFont("Times-Roman", 24)
    c.setFillColor(INK)
    c.drawString(54, H - 120, "Terms & Next Steps")

    items = [
        ("Certification", "Every book in this offering has been graded and encapsulated "
         "by Certified Guaranty Company (CGC), the industry's leading third-party "
         "certification service. Certification numbers and full grading notes are "
         "available upon request."),
        ("Availability", "All works are offered subject to availability and prior sale. "
         "All Star Comics #8 is currently being sourced from a private holder and its "
         "availability will be confirmed at the time of commitment."),
        ("Pricing", "Prices are quoted in U.S. dollars and are exclusive of any "
         "applicable taxes, shipping, and insurance. The price for Fantastic Four #1 "
         "will be quoted upon request. Terms of payment will be set out in the invoice."),
        ("Viewing", "Private viewings can be arranged. High-resolution photography of "
         "each certified copy, including slab and label, is available upon request."),
        ("Acquisition", "To proceed with any individual book or the collection as a "
         "whole, or to discuss terms, please contact us directly. Given the caliber of "
         "this material, we recommend prompt commitment to secure availability."),
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
    c.setTitle("Private Sales Proposal — Golden & Silver Age Comic Books")
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
