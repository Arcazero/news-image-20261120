# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Arcazero/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Arcazero/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

An infographic summing up Friday 20 November 2026 in one image (1024×1024): Cyclone Akvan's landfall in Odisha, ballistic missiles over Kyiv, Houthi strikes on a Saudi oil pipeline, flooding in Florida, COP31's final day in Antalya, and a 13,000-strong march in Tokyo.

Six AI-generated illustrations (in `assets/`, no text in them) plus clean PIL text, with a weather strip of real Open-Meteo ERA5 data for five cities. `draw.py` composes `entry.png`; `main.ts` (Node 22, stdlib only) copies it byte-for-byte to `/output/entry.png`.

## Run it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ackjrmv3&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
