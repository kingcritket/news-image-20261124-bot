#!/usr/bin/env python3
"""
build_entry.py -- renderer for "TUESDAY, IN FULL".

A one-page typographic broadsheet (1024 x 1024) in the Sunlit Crime-Noir
house style: sun-scorched cream paper, a warm sand numbers band, charcoal
ink and section bars, and exactly one red accent family (kicker, ticks,
sun disc). Type and flat geometry only -- no photographs, no generated
imagery.

Deterministic: no clock, no network, no randomness. Run locally:

    python3 build_entry.py            # writes entry.png next to this file

Every band measures its strings with Pillow's own metrics and asserts
they fit before drawing the next band, so an overflowing string fails
the build loudly instead of clipping.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ palette
PAPER = (243, 233, 208)      # pale cream, left out in the sun
SAND = (233, 212, 169)       # warm sand for the numbers band
SAND_EDGE = (214, 188, 138)  # hairline tone derived from the sand
INK = (33, 29, 23)           # charcoal ink
INK_SOFT = (88, 78, 62)      # softened charcoal for decks and notes
RED = (176, 30, 22)          # the single accent
WHITE = (250, 246, 236)      # warm white for text on charcoal

PAGE = 1024
MARGIN = 36
RIGHT = PAGE - MARGIN        # 988, right edge of the text block
MASTHEAD_LIMIT = 888         # masthead text never passes this x

FONT_DIR = Path("/usr/share/fonts/truetype/noto")


def load(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def f_display(size):   # masthead and hero headlines
    return load("NotoSans-CondensedExtraBold.ttf", size)


def f_head(size):      # story headlines
    return load("NotoSans-CondensedBold.ttf", size)


def f_body(size):      # decks and running text
    return load("NotoSans-SemiCondensed.ttf", size)


def f_label(size):     # kickers, bars, captions
    return load("NotoSans-SemiCondensedBold.ttf", size)


# ------------------------------------------------------------------ content
# Every item is dated Tuesday 24 November 2026. Where the underlying
# event fell on Monday, the wording says so and frames the Tuesday part
# -- the reaction, the follow-up, the report reaching Tuesday's wires --
# as the news.

LEAD_KICKER = "LEAD — UKRAINE · OFF LIBYA"
LEAD_HEADLINE = ["SEA DRONES SINK RUSSIAN", "WARSHIP OFF LIBYA"]
LEAD_DECK = (
    "President Zelenskyy said seven Ukrainian naval drones sank the "
    "Russian corvette Merkury at Benghazi and hit the cargo ship "
    "Angara, which Kyiv says carried weapons. Kyiv released the video "
    "on Monday; on Tuesday Libya's eastern government complained to "
    "the UN and the Kremlin deferred questions to the military."
)
LEAD_SOURCE = "ZELENSKYY ANNOUNCEMENT · MONDAY; TUESDAY REACTION · 24 NOV 2026"

SIDE_STORIES = [
    (
        "FOOTBALL — ZURICH",
        "FIFA NAMES 2031 AND 2035 WOMEN'S CUP HOSTS",
        "The US, Mexico, Costa Rica and Jamaica stage the first "
        "48-team Women's World Cup in 2031; the UK hosts in 2035. "
        "Decided by acclamation.",
    ),
    (
        "MARKETS — NVIDIA",
        "HUANG RETURNS; NVIDIA SOARS ABOUT 31%",
        "Nvidia's board unanimously reinstated Jensen Huang as chief "
        "executive on Monday, 11 days after he resigned. Shares "
        "jumped about a third; the S&P 500 rose 4.82%.",
    ),
    (
        "INDONESIA — CIKANDE",
        "SEARCH GOES ON FOR ABOUT 30 AFTER FIRE",
        "Rescuers kept searching the Cikande factory ruins on Tuesday "
        "for about 30 workers still missing. The toll of 24 dead was "
        "confirmed on Monday.",
    ),
]

NUMBERS = [
    ("7", "NAVAL DRONES IN\nTHE LIBYA STRIKE"),
    ("48", "TEAMS AT THE\n2031 WOMEN'S CUP"),
    ("+31%", "NVIDIA SHARES\nON HUANG'S RETURN"),
    ("4.82%", "S&P 500 RISE —\nBEST SINCE APRIL"),
    ("24", "DEAD IN THE\nCIKANDE FIRE"),
    ("22", "EU SANCTIONS\nPACKAGE NUMBER"),
]

# One-line grid: (headline, deck). Decks are capped at 46 characters.
GRID = [
    ("EU UNVEILS 22ND SANCTIONS PACKAGE", "Brussels proposes the package on Monday"),
    ("SEOUL NAMES FIRST WOMAN SPY CHIEF", "Kang Kum-sil tapped to lead the NIS"),
    ("MODI UNVEILS NEPAL AID PACKAGE", "Rs 15,000 crore; eight pacts signed"),
    ("ARMENIA PROPOSES NEW CONSTITUTION", "Step toward peace with Azerbaijan"),
    ("BANGLADESH VOWS TO ARREST HASINA", "If the ex-premier returns from India"),
    ("CHINA SETS 2030 CARE TARGETS", "Elderly care and childcare in focus"),
    ("CYPRUS EXPELS TWO RUSSIAN DIPLOMATS", "Pair ordered out over spying claims"),
    ("MOSCOW ACCUSES ESTONIA OF HOSTILITY", "Claims verge on triggering open war"),
    ("ZELENSKYY WARNS OF NEW RUSSIAN STRIKES", "Intelligence points to fresh attacks"),
    ("US TO BLACKLIST MEGASPEED CHIP FIRM", "Linked to the Nvidia scandal, source says"),
    ("CANADA–QATAR PACT DUE ON TUESDAY", "Investment deal to be signed today"),
    ("NATO SENDS WARNING JETS TO POLAND", "After the missile incident, alliance says"),
    ("TRUMP HALTS ARMY LEAD AZIDE BLAST", "Iowa detonation paused on his order"),
    ("MURMANSK GOVERNOR HELD FOR GRAFT", "Detained on embezzlement suspicion"),
    ("US SANCTIONS IRAN SHADOW BANKING", "Dozens targeted in the new measures"),
    ("MASSACHUSETTS SUES OVER ICE ARRESTS", "State seeks to block courthouse raids"),
    ("KALSHI PAUSES OPERATIONS IN UTAH", "After an adverse federal court ruling"),
    ("US SEEKS $1BN IN STOLEN BINANCE CRYPTO", "Action filed to recover the funds"),
    ("IRAN FLOGS SINGER AND HER TEAM", "Iranian website reports the punishment"),
    ("ERDOGAN: COP31 LAID GROUNDWORK", "Despite the lack of a deal, he says"),
    ("ANTHROPIC LAUNCHES CLAUDE SHIP", "New tool helps developers ship code"),
    ("FED'S WILLIAMS: INFLATION TOO HIGH", "Signals more rate hikes are possible"),
    ("KILAUEA VOLCANO ERUPTS IN HAWAII", "Live reports track the eruption"),
    ("ISRAELI STRIKES KILL THREE IN GAZA", "Monday strikes; UN worker among dead"),
    ("SEOUL: DPRK AIRCRAFT ENTERED AIRSPACE", "Seoul reports a suspected incursion"),
    ("THAILAND TO BAN MINING CHEMICALS", "Shipments to Myanmar face a ban"),
    ("BOMB ALERTS HIT EUROPEAN SCHOOLS", "Hundreds in Germany and Denmark warned"),
    ("WAYMO PULLS TAXIS FROM US FREEWAYS", "Driverless cars off the highways"),
    ("DENMARK BACKS “GHETTO LAW”", "Top court backs the hardline law"),
    ("SUPERMOON MEETS THE SEVEN SISTERS", "Pleiades line up in Tuesday's night sky"),
    ("TAJIKISTAN QUITS THE ICC", "Fourth state to leave after US push"),
    ("14 NATIONS BACK ICJ ROHINGYA RULING", "Fourteen states acknowledge the verdict"),
]

SPORT = [
    ("WELLINGTON TEST ENDS IN A DRAW", "NZ 239–5 after 120 overs; Mitchell 49*"),
    ("DE BRUYNE: CITY FEELINGS NEVER CHANGE", "Midfielder reflects on Manchester City"),
]

BRIEFS = [
    ("KITTEN DYM FOUND ALIVE IN DYMER", "Days under the rubble, and alive"),
    ("LANDMINE BLAST KILLS FIVE CHILDREN", "Northwest Syria blast, Tuesday reports"),
    ("ZAMBIA OPPOSITION LEADER CHARGED", "Accused of seeking to overthrow state"),
    ("MANCHESTER GIG EVACUATED", "12,000 leave after unknown substance"),
    ("CHINESE OFFICIAL GETS DEATH SENTENCE", "Over disclosing state secrets"),
]

STORY_TOTAL = 1 + len(SIDE_STORIES) + len(GRID) + len(SPORT) + len(BRIEFS)


# ------------------------------------------------------------------ helpers
def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured in pixels; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, s, fnt, fill, spacing=2.0):
    """Draw a string with manual letter tracking; returns the end x."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += text_w(draw, ch, fnt) + spacing
    return x - spacing


def section_bar(draw, y, label, right_note=None):
    """A charcoal bar with a red leading tick and a warm-white label."""
    draw.rectangle([MARGIN, y, RIGHT, y + 19], fill=INK)
    draw.rectangle([MARGIN, y, MARGIN + 7, y + 19], fill=RED)
    draw.text((MARGIN + 15, y + 3), label, font=f_label(12), fill=WHITE)
    if right_note:
        fnt = f_label(11)
        w = text_w(draw, right_note, fnt)
        draw.text((RIGHT - w - 10, y + 4), right_note, font=fnt, fill=SAND)
    return y + 19


# ------------------------------------------------------------------ drawing
def draw_masthead(draw):
    # Red sun disc, high at the right, then a hard diagonal charcoal
    # shadow thrown across its top corner. Pure geometry -- no text is
    # ever set over the shadow; masthead text stops at MASTHEAD_LIMIT.
    draw.ellipse([900, -14, 1036, 122], fill=RED)
    draw.polygon([(940, 0), (PAGE, 0), (PAGE, 110)], fill=INK)

    kicker = (
        f"{STORY_TOTAL} STORIES · EVERY ITEM DATED "
        "TUESDAY 24 NOVEMBER 2026"
    )
    end = tracked(draw, (MARGIN, 22), kicker, f_label(15), RED, 2.0)
    assert end <= MASTHEAD_LIMIT, f"kicker overruns: {end}"

    title_f = f_display(97)
    draw.text((MARGIN - 2, 44), "TUESDAY, IN FULL", font=title_f, fill=INK)
    tw = text_w(draw, "TUESDAY, IN FULL", title_f)
    assert MARGIN + tw <= MASTHEAD_LIMIT, "title overruns the sun zone"

    # Dateline row: date at the left, edition tag at the right.
    y = 152
    draw.text((MARGIN, y), "TUESDAY · 24 NOVEMBER 2026",
              font=f_label(13), fill=INK_SOFT)
    tag = "TUESDAY EDITION"
    tag_f = f_label(13)
    tag_w = text_w(draw, tag, tag_f) + 18
    tag_x = MASTHEAD_LIMIT - tag_w
    draw.rectangle([tag_x, y - 3, MASTHEAD_LIMIT, y + 19], outline=RED, width=2)
    draw.text((tag_x + 9, y), tag, font=tag_f, fill=RED)

    draw.rectangle([MARGIN, 178, RIGHT, 182], fill=INK)
    draw.rectangle([MARGIN, 185, RIGHT, 186], fill=INK)
    return 196


def draw_hero(draw, top):
    left_w = 592
    # Lead story, left column.
    chip_f = f_label(13)
    chip_w = text_w(draw, LEAD_KICKER, chip_f) + 18
    draw.rectangle([MARGIN, top, MARGIN + chip_w, top + 21], fill=RED)
    draw.text((MARGIN + 9, top + 4), LEAD_KICKER, font=chip_f, fill=WHITE)
    y = top + 29
    head_f = f_display(50)
    for line in LEAD_HEADLINE:
        assert text_w(draw, line, head_f) <= left_w, f"lead line too wide: {line}"
        draw.text((MARGIN - 1, y), line, font=head_f, fill=INK)
        y += 49
    y += 4
    deck_f = f_body(15)
    for line in wrap(draw, LEAD_DECK, deck_f, left_w):
        draw.text((MARGIN, y), line, font=deck_f, fill=INK)
        y += 19.5
    y += 7
    draw.text((MARGIN, y), LEAD_SOURCE, font=f_label(11), fill=INK_SOFT)
    lead_bottom = y + 15

    # Vertical rule between the columns.
    draw.rectangle([644, top + 2, 645, top + 282], fill=SAND_EDGE)

    # Three side stories, right column.
    sx = 664
    sw = RIGHT - sx
    sy = top
    for bar, headline, deck in SIDE_STORIES:
        draw.rectangle([sx, sy, RIGHT, sy + 16], fill=INK)
        draw.rectangle([sx, sy, sx + 6, sy + 16], fill=RED)
        draw.text((sx + 13, sy + 2.5), bar, font=f_label(11), fill=WHITE)
        sy += 20
        head_f2 = f_head(17)
        for line in wrap(draw, headline, head_f2, sw):
            draw.text((sx, sy), line, font=head_f2, fill=INK)
            sy += 19
        sy += 1
        deck_f2 = f_body(11.5)
        for line in wrap(draw, deck, deck_f2, sw):
            draw.text((sx, sy), line, font=deck_f2, fill=(52, 46, 36))
            sy += 13.5
        sy += 7
    side_bottom = sy - 7 + 4
    bottom = max(lead_bottom, side_bottom)
    assert bottom <= top + 318, f"hero overflows: {bottom - top}"
    return bottom


def draw_numbers(draw, top):
    draw.rectangle([MARGIN, top, RIGHT, top + 86], fill=SAND)
    draw.rectangle([MARGIN, top, RIGHT, top + 4], fill=RED)
    cell_w = (RIGHT - MARGIN) / len(NUMBERS)
    num_f = f_display(35)
    lab_f = f_label(10)
    for i, (value, label) in enumerate(NUMBERS):
        cx = MARGIN + i * cell_w
        if i:
            draw.rectangle([cx, top + 13, cx + 1, top + 73], fill=SAND_EDGE)
        draw.text((cx + 13, top + 9), value, font=num_f, fill=INK)
        ly = top + 49
        for line in label.split("\n"):
            draw.text((cx + 14, ly), line, font=lab_f, fill=(96, 44, 30))
            ly += 13
    return top + 86


def draw_grid(draw, top):
    y = section_bar(draw, top, "THE TUESDAY GRID",
                    f"{len(GRID)} ONE-LINE BRIEFS")
    y += 5
    col_w = (RIGHT - MARGIN - 28) / 2
    col_x = [MARGIN, MARGIN + col_w + 28]
    head_f = f_label(11.5)
    deck_f = f_body(11.5)
    rows = (len(GRID) + 1) // 2
    row_h = 15.3
    for idx, (headline, deck) in enumerate(GRID):
        assert len(deck) <= 46, f"deck too long: {deck!r}"
        col = idx % 2
        row = idx // 2
        x = col_x[col]
        ry = y + row * row_h
        draw.rectangle([x, ry + 4, x + 5, ry + 9], fill=RED)
        hw = text_w(draw, headline, head_f)
        draw.text((x + 11, ry), headline, font=head_f, fill=INK)
        deck_txt = " — " + deck
        dw = text_w(draw, deck_txt, deck_f)
        assert hw + 11 + dw <= col_w, f"grid line overflows: {headline}"
        draw.text((x + 11 + hw, ry + 0.5), deck_txt, font=deck_f,
                  fill=INK_SOFT)
        if row < rows - 1:
            draw.rectangle([x, ry + row_h - 1.5, x + col_w, ry + row_h - 0.5],
                           fill=(228, 214, 178))
    return y + rows * row_h


def draw_sport(draw, top):
    y = section_bar(draw, top, "SPORT")
    y += 5
    col_w = (RIGHT - MARGIN - 28) / 2
    head_f = f_head(15)
    deck_f = f_body(11.5)
    for i, (headline, deck) in enumerate(SPORT):
        x = MARGIN + i * (col_w + 28)
        draw.text((x, y), headline, font=head_f, fill=INK)
        draw.text((x, y + 18), deck, font=deck_f, fill=INK_SOFT)
    return y + 33


def draw_briefs(draw, top):
    y = section_bar(draw, top, "BRIEFS — FIVE MORE FROM TUESDAY")
    y += 5
    col_w = (RIGHT - MARGIN - 4 * 16) / 5
    head_f = f_head(12)
    deck_f = f_body(10)
    bottom = y
    for i, (headline, deck) in enumerate(BRIEFS):
        x = MARGIN + i * (col_w + 16)
        if i:
            draw.rectangle([x - 8, y, x - 7.5, y + 40], fill=SAND_EDGE)
        ly = y
        for line in wrap(draw, headline, head_f, col_w):
            draw.text((x, ly), line, font=head_f, fill=INK)
            ly += 13.5
        for line in wrap(draw, deck, deck_f, col_w):
            draw.text((x, ly), line, font=deck_f, fill=INK_SOFT)
            ly += 12
        bottom = max(bottom, ly)
    return bottom


def draw_footer(draw, top):
    draw.rectangle([MARGIN, top, RIGHT, top + 1.5], fill=INK)
    note = ("Compiled from Tuesday's wires — Reuters · BBC · AFP · AP · "
            "FIFA · ICC · USGS PAGER")
    fnt = f_body(10.5)
    w = text_w(draw, note, fnt)
    draw.text(((PAGE - w) / 2, top + 6), note, font=fnt, fill=INK_SOFT)
    return top + 6 + 14


def main():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)

    y = draw_masthead(draw)
    y = draw_hero(draw, y + 4)
    y = draw_numbers(draw, y + 8)
    y = draw_grid(draw, y + 10)
    y = draw_sport(draw, y + 6)
    y = draw_briefs(draw, y + 8)
    y = draw_footer(draw, y + 5)

    assert y <= PAGE - 8, f"page overflow: bottom at {y}"
    out = Path(__file__).with_name("entry.png")
    img.save(out, optimize=True)
    print(f"wrote {out} -- bottom edge at y={y}, stories={STORY_TOTAL}")


if __name__ == "__main__":
    main()
