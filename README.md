[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/kingcritket/news-image-20261124-bot/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/kingcritket/news-image-20261124-bot/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# TUESDAY, IN FULL — 24 November 2026

A one-page typographic broadsheet summing up the world's news of
Tuesday 24 November 2026, rendered in the Sunlit Crime-Noir style:
sun-scorched cream paper, a warm sand numbers panel, charcoal ink, one
red accent family, and a flat red sun disc cut by a hard diagonal
charcoal shadow in the masthead.

## The entry

- `build_entry.py` — deterministic Pillow renderer. All 43 stories live
  in its data tables (lead, middle stories, one-line grid, sport strip);
  the story count is computed from those tables and printed on the page.
  Layout assertions fail loudly on any overflow, and the page bottom is
  checked against the 1024 px bound.
- `entry.png` — the rendered page, 1024×1024, 259,189 bytes.
- `main.py` — standard library only. It verifies the PNG header
  (1024×1024 IHDR) and copies `entry.png` byte-identical to
  `$MAKEFUN_OUTPUT_DIR` (default `output/`).

## Run it

```sh
python3 build_entry.py            # re-render entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## The day, in brief

Lead: Kyiv's sea drones sank the Russian corvette *Merkury* at Benghazi
on Sunday; Kyiv claimed the sinking on Monday, and on Tuesday Libya
took the case to the United Nations while the Kremlin said nothing.
Around it: Nvidia brings Jensen Huang back and the market roars, the US
blacklists Megaspeed, FIFA names its 2031 and 2035 Women's World Cup
hosts, the EU unveils a 22nd sanctions package, a US appeals court gives
Trump a new path at his hush-money conviction, 24 are confirmed dead in
the Cikande factory fire, and a boy, a woman — and a cat named Dym —
are pulled alive from the rubble in Dymer.

Every story is dated as reported: MON = Monday 23 Nov, SUN = Sunday
22 Nov, THU = Thursday 19 Nov. See `BUILD_REPORT.md` for the full story
list with a date and source note per item.
