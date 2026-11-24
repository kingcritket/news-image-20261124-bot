# BUILD REPORT — "TUESDAY, IN FULL"

Entry for make.fun bounty **news-image-20261124** ("Sum up 24 November's
world news in one image"). Built fresh in this session: new renderer,
new shipper, new repository — the previous day's entry was read for
reference only (layout pattern, font choices) and no file was copied
from it.

## Concept

A one-page typographic broadsheet in the user's **Sunlit Crime-Noir**
brief: pale sun-scorched cream paper, a warm sand panel for the day's
numbers, charcoal ink and section bars, and exactly one red accent
family (kicker, ticks, panel rule, sun disc). The masthead sun is a flat
red disc cut by a hard diagonal charcoal shadow — pure geometry, no text
over the shadow, and all masthead text is asserted to stop at x ≤ 888
with the disc beginning at x ≈ 900. No photographs, no AI imagery;
type only, set in Noto Sans Condensed / SemiCondensed for a condensed
editorial feel.

## Contents and the count

43 stories, recounted from the data tables in `build_entry.py`
(`STORY_TOTAL` is computed, not typed, and the masthead kicker prints it):

| Section | Items |
| --- | --- |
| Lead (hero) | 1 |
| Hero side stories | 3 |
| One-line grid | 32 |
| Sport | 2 |
| Briefs | 5 |
| **Total (kicker)** | **43** |

The six-figure numbers panel is furniture, not stories, and is excluded
from the count.

## Date discipline — verification per item

Every item is dated Tuesday 24 November 2026. Where the underlying event
fell on Monday, the item is framed honestly as Tuesday's development:

- **Lead — Ukraine sinks Russian warship off Libya.** Operation on
  Sunday; President Zelenskyy announced it and released the video on
  Monday (SBU video, 23 Nov). The Tuesday news is the reaction: Libya's
  eastern government complained to the UN about the Benghazi attacks
  and the Kremlin deferred questions to the military (Tuesday digests,
  24 Nov 00:47–02:20 UTC). The deck states both dates plainly.
- **Side 1 — FIFA Women's World Cup hosts.** Decided by acclamation at
  the Extraordinary FIFA Congress on Monday 23 Nov in Zurich — Tuesday
  24 Nov in New Zealand (Friends of Football dateline). US, Mexico,
  Costa Rica and Jamaica host 2031 (first 48-team edition); England,
  Scotland, Wales and Northern Ireland host 2035.
- **Side 2 — Nvidia.** Board unanimously reinstated Jensen Huang as CEO
  on Monday, 11 days after he resigned; shares jumped about 31–33% and
  the S&P 500 rose 4.82%, its best day since April 2025 (Monday's
  session, reported across Tuesday's wires).
- **Side 3 — Cikande.** No new Tuesday toll was found: the 24 dead were
  confirmed on Monday (Reuters, Jakarta, 23 Nov) and the search for
  about 30 missing was still the running story in Tuesday's digests.
  The item says the search "kept searching ... on Tuesday" and dates
  the toll to Monday — it is NOT reused as the lead, per the brief.
- **Numbers panel.** 7 (naval drones), 48 (2031 teams), +31% (Nvidia),
  4.82% (S&P 500), 24 (Cikande dead), 22 (EU sanctions package) — all
  Monday/Tuesday figures.
- **Grid / sport / briefs.** Drawn from the verified Tuesday list:
  Reuters items datelined 24 Nov (Zelenskyy warning of new Russian
  strikes; Moscow accusing Estonia; US to blacklist Megaspeed;
  Canada–Qatar pact due Tuesday; NATO jets to Poland; Trump halting the
  lead-azide blast; Murmansk governor detained; Iran shadow-banking
  sanctions; 14 nations acknowledging the ICJ Rohingya ruling), Monday
  events labelled as Monday (EU sanctions package proposed; Seoul
  reshuffle; Modi Nepal package; Gaza strikes; Kilauea live reports),
  and Tuesday-digest items (Cyprus expulsions; DPRK airspace incursion
  claim; bomb alerts in Germany/Denmark; Waymo freeway pull-out;
  Denmark "ghetto law" ruling; Tajikistan leaving the ICC; kitten Dym
  found alive after days under the Dymer rubble; Manchester gig
  evacuation; Zambia charge; Syria landmine deaths). The ICJ Myanmar
  ruling itself (19 Nov) is NOT used as an event — only the 24 Nov
  acknowledgement of it by 14 nations. The Wellington Test item carries
  its Monday day-five scoreline (NZ 239–5, 120 overs; Mitchell 49*).

## Self-audit trail

- **Layout engine assertions.** The renderer measures every string with
  Pillow metrics and asserts: masthead kicker and title end ≤ x 888;
  every grid headline + deck fits its column; every grid deck ≤ 46
  characters; lead headline lines fit the 592 px column; the hero band
  fits its budget; the page bottom lands at y ≤ 1016. Four overflows
  were caught and fixed by the engine during development (hero band
  35 px over; three grid lines over the column width) before any
  visual pass.
- **Visual round 1** (full page read back): no clipped or overlapping
  text; edition label clear of the sun disc; no text over the shadow.
  Two defects found: (a) the sun disc was almost entirely hidden behind
  the diagonal shadow — only a small red sliver showed; (b) the grid
  headline "SEOUL: DPRK JETS ENTERED AIRSPACE" overstated the source
  (Seoul reported a *suspected* aircraft incursion, not jets).
- **Revision round.** Shadow triangle narrowed (starts x 940, ends
  y 110) so the red disc reads clearly beside it; headline corrected
  to "SEOUL: DPRK AIRCRAFT ENTERED AIRSPACE". Re-rendered.
- **Visual round 2** (full page + top crop + bottom crop + 300 px
  downscale read back): disc now clearly visible, cut by the hard
  diagonal shadow; no new overlaps; masthead, lead headline, numbers
  panel and section bars stay legible at 300 px; the grid becomes fine
  print, as expected of a 43-story page, but its structure holds.
- **Determinism.** `build_entry.py` was run again after the final
  render; `entry.png` sha256 was identical (no clock, network or
  randomness anywhere in the renderer).

## Local test results

`main.py` (stdlib-only shipper) was run twice:

| Run | Command | Exit | Output sha256 |
| --- | --- | --- | --- |
| 1 | `MAKEFUN_OUTPUT_DIR=out python3 main.py` | 0 | 58f8d837… |
| 2 | `MAKEFUN_OUTPUT_DIR=out python3 main.py` | 0 | 58f8d837… |

Both runs delivered copies byte-identical to the committed `entry.png`
(full sha256
`58f8d83726652b5a62df14d9f38be220a2a742aed5ee10c8a0c7378156da5015`).
A re-run of `build_entry.py` after the final render produced the same
hash again.

Independent verification of the committed file: PNG signature valid,
IHDR reads 1024×1024, file size 226,006 bytes (< 1 MiB).

## Files

- `build_entry.py` — renderer (Pillow, local build only)
- `entry.png` — the rendered page, 1024×1024
- `main.py` — stdlib-only shipper
- `README.md`, `LICENSE` (MIT), `BUILD_REPORT.md`
