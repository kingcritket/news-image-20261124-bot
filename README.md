# TUESDAY, IN FULL

Entry for make.fun bounty **news-image-20261124** ("Sum up 24 November's
world news in one image"). A one-page typographic broadsheet of Tuesday
24 November 2026: **43 stories** — a lead, three side stories, a 32-item
one-line grid, sport, and five briefs — set in the user's **Sunlit
Crime-Noir** brief: sun-scorched cream paper, a warm sand numbers panel,
charcoal ink and section bars, and exactly one red accent family. The
masthead sun is a flat red disc cut by a hard diagonal charcoal shadow;
no text is ever set over the shadow.

Lead story: Ukraine says its naval drones sank the Russian corvette
Merkury off Libya — announced Monday, with Tuesday's reaction (Libya's
eastern government complaining to the UN, the Kremlin deferring
questions) as the Tuesday development. Side stories: FIFA naming the
2031 and 2035 Women's World Cup hosts, Jensen Huang's return to Nvidia
and the market surge, and the Cikande factory-fire search going on for
about 30 missing. Every item is dated Tuesday 24 November 2026; where
the underlying event fell on Monday, the wording says so (see
`BUILD_REPORT.md` for the per-item date notes).

## Files

- `build_entry.py` — deterministic Pillow renderer (local build only);
  run `python3 build_entry.py` to regenerate `entry.png`
- `entry.png` — the rendered page, 1024x1024
- `main.py` — standard-library-only shipper: verifies the PNG and
  copies it byte-identical to `$MAKEFUN_OUTPUT_DIR` (default `output`)
- `README.md`, `LICENSE` (MIT), `BUILD_REPORT.md`

## Practice run

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
