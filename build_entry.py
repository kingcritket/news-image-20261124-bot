#!/usr/bin/env python3
"""TUESDAY, IN FULL — a one-page typographic broadsheet of the world's news
for Tuesday 24 November 2026, rendered with Pillow.

Sunlit Crime-Noir treatment: sun-scorched cream paper, warm sand numbers
panel, charcoal ink, one red accent family, a flat red sun disc cut by a
hard diagonal charcoal shadow in the masthead, and no text over the shadow.

Every story is drawn from fresh web research done in this session (Reuters,
AP, AFP, FIFA, the European Commission, court records). Items that happened
before Tuesday carry an explicit day tag (MON / SUN / THU); Tuesday items
are tagged TUE. The story count is computed from the data tables below.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (247, 237, 216)        # sun-scorched cream
SAND = (233, 211, 165)         # warm sand panel
SAND_EDGE = (214, 186, 132)    # sand panel border
INK = (28, 25, 22)             # charcoal ink
INK_SOFT = (88, 78, 64)        # soft charcoal for small print
RED = (198, 16, 46)            # the one red accent
RED_DARK = (148, 10, 32)       # red, darker shade (same family)
RED_LIGHT = (228, 62, 80)      # red, lighter shade for dark ground
CREAM = (250, 246, 236)        # text on charcoal

# ---------------------------------------------------------------- geometry
W, H = 1024, 1024
MARGIN = 26
COL_W = 320                    # three-column width
GUT = 14                       # gutter between columns
COL_X = [MARGIN, MARGIN + COL_W + GUT, MARGIN + 2 * (COL_W + GUT)]

FONT_DIR = "/usr/share/fonts/truetype"


def _pick(*names):
    """Return the first font file that exists on disk."""
    for name in names:
        path = os.path.join(FONT_DIR, name)
        if os.path.exists(path):
            return path
    raise FileNotFoundError("none of %s found" % (names,))


F_TITLE = _pick("noto/NotoSans-CondensedBlack.ttf")
F_HEAD = _pick("noto/NotoSans-CondensedBold.ttf")
F_KICK = _pick("noto/NotoSans-CondensedBold.ttf")
F_BODY = _pick("noto/NotoSans-Regular.ttf")
F_MED = _pick("noto/NotoSans-Medium.ttf")


def _font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data
# Lead: (kicker, headline, deck). Deck must wrap to at most 4 lines.
LEAD = (
    "LEAD  ·  THE WAR SAILS TO LIBYA  ·  TUESDAY'S FALLOUT",
    "KYIV'S SEA DRONES SINK A RUSSIAN WARSHIP IN LIBYA",
    "Seven sea drones struck the corvette Merkury at Benghazi on Sunday; "
    "Kyiv claimed the sinking on Monday. On Tuesday Libya asked the United "
    "Nations to investigate while the Kremlin said nothing. A Ka-27 "
    "helicopter was destroyed with her; the cargo ship MV Angara was hit too.",
)

# Numbers panel: (big figure, caption)
NUMBERS = [
    ("7", "sea drones, Kyiv says it sent"),
    ("1", "corvette sunk — in service since 2023"),
    ("2", "ships hit: Merkury and MV Angara"),
    ("2,400", "km from Ukraine's front line"),
]

# Middle stories: (kicker with day tag, headline, deck <= 2 lines).
MIDDLE = [
    ("MARKETS  ·  MON",
     "HUANG IS BACK — NVIDIA SOARS 31%",
     "Huang is back 11 days after quitting; shares closed up 31.5%, their "
     "best day since 2003."),
    ("TECH  ·  MON",
     "US BLACKLISTS MEGASPEED",
     "The Commerce Dept put the Singapore cloud firm at the heart of the "
     "Nvidia scandal on its Entity List."),
    ("SPORT  ·  MON",
     "FIFA NAMES ITS NEXT TWO WOMEN'S WORLD CUPS",
     "US, Mexico, Costa Rica and Jamaica host 2031; England, Northern "
     "Ireland, Scotland and Wales take 2035."),
    ("EUROPE  ·  MON",
     "EU UNVEILS ITS 22ND SANCTIONS PACKAGE",
     "60 banks face SWIFT removal; 70-plus shadow-fleet ships listed; "
     "Russia's flag barred at EU events."),
    ("WASHINGTON  ·  MON",
     "A COURT GIVES TRUMP A NEW PATH TO ERASE HIS CONVICTION",
     "The 2nd Circuit revived his bid to move the case to federal court, "
     "to seek dismissal on immunity grounds."),
    ("INDONESIA  ·  MON",
     "24 DEAD IN THE CIKANDE FACTORY FIRE",
     "Confirmed Monday as rescuers searched unstable wreckage for about "
     "30 still missing."),
    ("UKRAINE  ·  SUN–MON",
     "A BOY, A WOMAN — AND A CAT — PULLED FROM THE RUBBLE",
     "A drone flattened a five-storey block in Dymer, killing 11. A boy "
     "of seven was freed after 14 hours."),
    ("ASIA  ·  MON",
     "INDIA GIVES NEPAL A $1.63BN PACKAGE",
     "Modi announced the aid after talks with Nepal's PM Balendra Shah; "
     "eight deals signed, a new train launched."),
    ("SEOUL  ·  MON",
     "SOUTH KOREA NAMES ITS FIRST WOMAN SPY CHIEF",
     "Lee Jae Myung reshuffled his security team, tapping ex-justice "
     "minister Kang Kum-sil to lead the NIS."),
    ("CLIMATE  ·  SUN",
     "COP31 COLLAPSES WITHOUT A DEAL",
     "Talks in Antalya ended Sunday with no deal; the EU rejected a text "
     "that ignored fossil fuels."),
    ("WEST BANK  ·  SUN",
     "EISENKOT CALLS SETTLER ARSON 'JEWISH TERRORISM'",
     "Settlers burned vehicles and sprayed racist graffiti near Ramallah "
     "early Sunday; police are investigating."),
    ("INDIA  ·  MON",
     "TOP COURT FREES GODHRA CONVICT ON MEDICAL GROUNDS",
     "The court suspended Irfan Siraj Pada's life sentence; jailed 18 "
     "years over the 2002 Sabarmati Express fire."),
]

# One-line grid: (tag, line). Each must wrap to at most 2 lines.
LINES = [
    ("KREMLIN, MON", "Defence ministry handles the Merkury; next "
     "Russia–Ukraine–US talks \"soon\"."),
    ("SBU", "Drones were launched from a \"mother ship\"; Russia has \"no "
     "safe routes, even far beyond the Black Sea\"."),
    ("LIBYA", "The navy intercepted more than 20 drone boats off the coast "
     "late on Sunday."),
    ("CIKANDE", "29 confirmed safe, five in hospital; about 300 were on the "
     "Saturday shift."),
    ("DYMER", "15 killed across the Kyiv region as of Monday; two people "
     "still missing."),
    ("DYM", "Three cats were rescued at the Dymer site; the first was "
     "reunited with its owner."),
    ("NVIDIA", "Still ~29% below its 6 Oct record close of $239.24; Huang "
     "testifies on Capitol Hill in Dec."),
    ("MARKETS, MON", "Bitcoin jumped from $61,200 to $63,900 on the news; "
     "gold rose $50 to $3,666 an ounce."),
    ("WALL ST, MON", "Dow +1,448 points; S&P +4.7%; Nasdaq +6.5% — the best "
     "day since April 2025."),
    ("ANTHROPIC", "Shares slipped to $86.47 on Monday, below the $97.17 "
     "first-day close."),
    ("FIFA", "2031: 48 teams, 104 games; 20 cities — 14 in the US, four in "
     "Mexico, San José, Kingston."),
    ("EU", "The sanctions package needs all 27 member states before it can "
     "take force."),
    ("TRUMP", "His lawyers laud a \"prompt and correct\" ruling; the "
     "conviction stands for now."),
    ("INDIA–NEPAL", "Joint Vision Document signed; an offshore IIT campus "
     "for Nepal; weekly train from 28 Nov."),
    ("KOREA", "Nominees face parliamentary hearings; no confirmation votes "
     "are needed."),
    ("CLIMATE", "October 2026 was the warmest month on record (+1.8°C); "
     "2026 is set to be the warmest year."),
    ("WEST BANK", "500,000+ settlers; 1,100+ Palestinians killed there "
     "since October 2023."),
    ("GODHRA", "58 were killed in the 2002 coach fire; Pada's appeal is "
     "pending; Gujarat did not oppose bail."),
    ("BANGKOK, TUE", "Protesters march today to the Bangchak refinery over "
     "fuel refining margins."),
    ("MADURAI, TUE", "Supreme Court allows the Karthigai Deepam lamp to be "
     "lit today, a one-off order."),
    ("COP31", "The 35-by-35 electrification pledge was signed by dozens of "
     "nations, but did not pass."),
    ("COP31", "Unfinished business is deferred to next year's talks in "
     "Ethiopia."),
    ("MEGASPEED", "Under US probe since 2024; Alice Huang left in August "
     "2025; the firm denies wrongdoing."),
    ("ICJ, THU", "Myanmar committed genocide against the Rohingya; the first "
     "state ever found responsible."),
    ("SHENZHEN, THU", "Trump, Xi and Putin met; nuclear-risk talks agreed, "
     "no word on Ukraine or Iran."),
    ("WORLD CUP", "The 2027 edition is in Brazil, 24 June–25 July, the "
     "first in South America."),
    ("CIKANDE", "Victims cannot be identified visually; DNA samples are "
     "being taken from relatives."),
]

# Sport strip: terse one-liners, at most 2 lines each.
SPORT = [
    "CRICKET — India 720/9 dec; NZ 368 & 239/5. Wellington Test drawn.",
    "CRICKET — Mitchell 49* (186) and Phillips 26* (126) bat out 120 overs.",
    "CRICKET — Nicholls 175* is player of the match; four Tests drawn in November.",
]

FOOTER = ("All stories dated as reported — MON = Monday 23 Nov · SUN = Sunday 22 Nov · "
          "THU = Thursday 19 Nov · Sources: Reuters, AP, AFP, FIFA, European "
          "Commission, court records.")

# ---------------------------------------------------------------- helpers
def wrap_text(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # a single over-long word is hard-split by characters
            while draw.textlength(word, font=font) > width:
                cut = len(word)
                while cut > 1 and draw.textlength(word[:cut], font=font) > width:
                    cut -= 1
                lines.append(word[:cut])
                word = word[cut:]
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_rule(draw, x0, x1, y, width=2, colour=INK):
    draw.line([(x0, y), (x1, y)], fill=colour, width=width)


def section_head(draw, y, title):
    """Red square + condensed title + hairline rule. Returns next y."""
    draw.rectangle([MARGIN, y + 3, MARGIN + 12, y + 15], fill=RED)
    draw.text((MARGIN + 20, y), title, font=_font(F_HEAD, 19), fill=INK)
    draw_rule(draw, MARGIN + 20 + draw.textlength(title, font=_font(F_HEAD, 19)) + 12,
              W - MARGIN, y + 9, width=1)
    return y + 24


def story_block(draw, x, y, width, kicker, headline, deck, max_head_lines=2,
                max_deck_lines=2):
    """One middle story: red kicker, condensed headline, short deck.

    Raises loudly if anything overflows its line budget.
    """
    kick_f = _font(F_KICK, 12)
    head_f = _font(F_HEAD, 19)
    deck_f = _font(F_BODY, 12)
    draw.text((x, y), kicker, font=kick_f, fill=RED)
    y += 15
    head_lines = wrap_text(draw, headline, head_f, width)
    if len(head_lines) > max_head_lines:
        raise AssertionError("headline overflows: %r -> %d lines"
                             % (headline, len(head_lines)))
    for line in head_lines:
        draw.text((x, y), line, font=head_f, fill=INK)
        y += 21
    deck_lines = wrap_text(draw, deck, deck_f, width)
    if len(deck_lines) > max_deck_lines:
        raise AssertionError("deck overflows: %r -> %d lines"
                             % (deck, len(deck_lines)))
    for line in deck_lines:
        draw.text((x, y), line, font=deck_f, fill=INK_SOFT)
        y += 14
    return y


# ---------------------------------------------------------------- render
def render(out_path):
    story_total = 1 + len(MIDDLE) + len(LINES) + len(SPORT)
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- top red bar -----------------------------------------------------
    draw.rectangle([0, 0, W, 6], fill=RED)

    # --- masthead: sun disc cut by a hard diagonal shadow ----------------
    # Disc on the right; title text is kept left of x=780, so no text
    # ever crosses the shadow band.
    sun_cx, sun_cy, sun_r = 912, 74, 50
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r,
                  sun_cx + sun_r, sun_cy + sun_r], fill=RED)
    # diagonal charcoal band, top edge to just above the dateline rule
    draw.polygon([(848, 0), (904, 0), (996, 142), (940, 142)], fill=INK)

    draw.text((MARGIN, 14), "THE WORLD IN ONE PAGE",
              font=_font(F_KICK, 14), fill=RED)
    draw.text((MARGIN, 30), "TUESDAY, IN FULL",
              font=_font(F_TITLE, 64), fill=INK)
    dateline = ("TUESDAY 24 NOVEMBER 2026  ·  %d STORIES  ·  "
                "THE DAY'S WORLD NEWS" % story_total)
    draw.text((MARGIN, 104), dateline, font=_font(F_HEAD, 17), fill=INK_SOFT)
    draw_rule(draw, MARGIN, W - MARGIN, 130, width=2)

    # --- lead ------------------------------------------------------------
    lead_y = 140
    lead_w = 640
    draw.text((MARGIN, lead_y), LEAD[0], font=_font(F_KICK, 13), fill=RED)
    y = lead_y + 18
    head_lines = wrap_text(draw, LEAD[1], _font(F_TITLE, 36), lead_w)
    if len(head_lines) > 2:
        raise AssertionError("lead headline overflows: %d lines" % len(head_lines))
    for line in head_lines:
        draw.text((MARGIN, y), line, font=_font(F_TITLE, 36), fill=INK)
        y += 40
    y += 2
    deck_lines = wrap_text(draw, LEAD[2], _font(F_BODY, 15), lead_w)
    if len(deck_lines) > 4:
        raise AssertionError("lead deck overflows: %d lines" % len(deck_lines))
    for line in deck_lines:
        draw.text((MARGIN, y), line, font=_font(F_BODY, 15), fill=INK)
        y += 18
    lead_bottom = y
    if lead_bottom > 318:
        raise AssertionError("lead block too tall: bottom %d" % lead_bottom)

    # numbers panel: warm sand, right of the lead text
    px0, px1 = 692, W - MARGIN
    py0, py1 = lead_y, 310
    draw.rectangle([px0, py0, px1, py1], fill=SAND, outline=SAND_EDGE, width=1)
    draw.text((px0 + 14, py0 + 10), "THE SINKING, IN NUMBERS",
              font=_font(F_KICK, 13), fill=RED_DARK)
    draw_rule(draw, px0 + 14, px1 - 14, py0 + 32, width=1, colour=SAND_EDGE)
    row_y = py0 + 40
    for big, caption in NUMBERS:
        draw.text((px0 + 14, row_y), big, font=_font(F_TITLE, 26), fill=INK)
        draw.text((px0 + 118, row_y + 7), caption, font=_font(F_BODY, 12),
                  fill=INK_SOFT)
        row_y += 32
    if row_y > py1:
        raise AssertionError("numbers panel overflows")

    # --- middle stories: three columns, four each -----------------------
    y = section_head(draw, 320, "THE DAY'S BIG STORIES")
    if len(MIDDLE) != 12:
        raise AssertionError("expected 12 middle stories, got %d" % len(MIDDLE))
    col_bottoms = []
    for ci in range(3):
        cy = y
        for si in range(4):
            kicker, headline, deck = MIDDLE[ci * 4 + si]
            cy = story_block(draw, COL_X[ci], cy, COL_W, kicker, headline, deck)
            cy += 6
        col_bottoms.append(cy)
    mid_bottom = max(col_bottoms)
    if mid_bottom > 736:
        raise AssertionError("middle section too tall: bottom %d" % mid_bottom)

    # --- one-line grid: three columns, nine rows -------------------------
    y = section_head(draw, mid_bottom + 8, "THE DAY IN LINES")
    if len(LINES) != 27:
        raise AssertionError("expected 27 line items, got %d" % len(LINES))
    line_f = _font(F_BODY, 11)
    tag_f = _font(F_KICK, 11)
    row_h = 24
    for ri in range(9):
        for ci in range(3):
            tag, line = LINES[ri * 3 + ci]
            x = COL_X[ci]
            draw.rectangle([x, y + 4, x + 7, y + 11], fill=RED)
            tag_w = draw.textlength(tag + "  ", font=tag_f)
            draw.text((x + 12, y), tag, font=tag_f, fill=RED_DARK)
            wrapped = wrap_text(draw, line, line_f, COL_W - 12 - tag_w)
            if len(wrapped) > 2:
                raise AssertionError("line item overflows: %r -> %d lines"
                                     % (line, len(wrapped)))
            ly = y
            for wline in wrapped:
                draw.text((x + 12 + tag_w, ly), wline, font=line_f, fill=INK)
                ly += 12
        y += row_h
    if y > 984:
        raise AssertionError("lines section too tall: bottom %d" % y)

    # --- sport strip: charcoal band --------------------------------------
    band_y = y + 4
    draw.rectangle([MARGIN, band_y, W - MARGIN, band_y + 40], fill=INK)
    sport_f = _font(F_MED, 11)
    for ci, item in enumerate(SPORT):
        wrapped = wrap_text(draw, item, sport_f, COL_W - 8)
        if len(wrapped) > 2:
            raise AssertionError("sport item overflows: %r" % item)
        sy = band_y + 6
        for wline in wrapped:
            draw.text((COL_X[ci], sy), wline, font=sport_f, fill=CREAM)
            sy += 14

    # --- footer ----------------------------------------------------------
    foot_f = _font(F_BODY, 10)
    foot_w = draw.textlength(FOOTER, font=foot_f)
    if foot_w > W - 2 * MARGIN:
        raise AssertionError("footer too wide: %d" % foot_w)
    draw.text(((W - foot_w) / 2, band_y + 46), FOOTER, font=foot_f, fill=INK_SOFT)
    page_bottom = band_y + 46 + 12
    if page_bottom > H - 4:
        raise AssertionError("page bottom out of bounds: %d" % page_bottom)
    # bottom red bar, mirroring the top bar
    draw.rectangle([0, H - 6, W, H], fill=RED)

    img.save(out_path, "PNG")
    size = os.path.getsize(out_path)
    digest = hashlib.sha256(open(out_path, "rb").read()).hexdigest()
    print("rendered %s" % out_path)
    print("stories: lead 1 + middle %d + lines %d + sport %d = %d"
          % (len(MIDDLE), len(LINES), len(SPORT), story_total))
    print("sections: lead bottom %d, middle bottom %d, lines bottom %d, "
          "sport band %d-%d, page bottom %d"
          % (lead_bottom, mid_bottom, y, band_y, band_y + 40, page_bottom))
    print("size: %d bytes (limit 1048576), sha256: %s" % (size, digest))
    if size > 1048576:
        raise AssertionError("entry.png exceeds 1 MiB")
    return story_total, size, digest


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render(target)
