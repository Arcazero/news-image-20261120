#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: a 1024x1024 newspaper front page
summing up Friday 20 November 2026.

Six verified stories (all happened or first reported on 20 Nov 2026):
  1. WEATHER  - Cyclone Akvan makes landfall near Gopalpur, Odisha (IMD)
  2. KYIV     - Russia strikes Kyiv with ballistic missiles overnight (Reuters)
  3. GULF     - Houthis hit Saudi East-West pipeline; missile intercepted (Reuters/EIA)
  4. USA      - Florida flooding; storm may become Tropical Storm Kyle (CNN)
  5. COP31    - Climate summit reaches its final day still split on a deal (NexusEuropa)
  6. TOKYO    - 13,000 march against the Takaichi government (News.Az/EIN)

Six AI-generated illustrations (assets/, no text in them) + clean PIL text
(DejaVu Sans/Serif). Weather strip uses REAL 20 Nov 2026 conditions from
the Open-Meteo archive API (ERA5 reanalysis) for five story cities.
Output entry.png; PNG first, JPEG q85 fallback if over 1 MiB.
Layout asserts nothing overflows its card.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
OUT = "entry.png"
ASSETS = "assets"

NAVY = (15, 42, 67)
GOLD = (184, 124, 22)
PAPER = (247, 245, 240)
INK = (26, 26, 26)
MUTED = (92, 92, 92)
WHITE = (255, 255, 255)
BORDER = (208, 203, 193)
SKY = (228, 237, 243)
TAG_BG = (15, 42, 67)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap and cap to max_lines, adding an ellipsis if truncated."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        # trim last line until the ellipsis fits
        while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_w:
            lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else ""
        lines[-1] = (lines[-1] + " ...").strip()
    return lines


def load_pic(name, tw, th):
    """Load an illustration, centre-crop to the target aspect, resize,
    and quantize to a 256-colour palette so the final PNG stays small."""
    path = os.path.join(ASSETS, name)
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (tw, th), Image.LANCZOS)
    return im.convert("P", palette=Image.ADAPTIVE, colors=256).convert("RGB")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font(SERIF_B, 50)
    f_date = font(SANS_B, 17)
    f_wlab = font(SANS_B, 13)
    f_wcity = font(SANS_B, 13)
    f_wval = font(SANS, 12)
    f_tag = font(SANS_B, 12)
    f_head = font(SANS_B, 19)
    f_body = font(SANS, 14)
    f_foot = font(SANS, 12)

    # ---- Masthead ----
    d.text((W // 2, 6), "THE WORLD TODAY", font=f_mast, fill=NAVY,
           anchor="mt")
    d.line([(14, 58), (W - 14, 58)], fill=GOLD, width=3)
    d.text((W // 2, 74), "Friday, 20 November 2026", font=f_date,
           fill=INK, anchor="ma")

    # ---- Weather strip (REAL 20 Nov 2026 data, Open-Meteo archive / ERA5) ----
    wy, wh = 112, 58
    d.rectangle([14, wy, W - 14, wy + wh], fill=SKY,
                outline=BORDER, width=1)
    d.text((26, wy + 8), "WEATHER", font=f_wlab, fill=NAVY)
    d.text((26, wy + 28), "20 NOV 2026", font=f_wlab, fill=NAVY)
    d.text((26, wy + 43), "OPEN-METEO ERA5", font=f_wval, fill=MUTED)
    cities = [
        ("Gopalpur", "28\u00b0 / 23\u00b0", "100 mm rain", "28 km/h"),
        ("Kyiv", "8\u00b0 / 6\u00b0", "14 mm rain", "25 km/h"),
        ("Daytona Beach", "23\u00b0 / 21\u00b0", "68 mm rain", "37 km/h"),
        ("Riyadh", "29\u00b0 / 16\u00b0", "dry", "7 km/h"),
        ("Tokyo", "14\u00b0 / 6\u00b0", "dry", "14 km/h"),
    ]
    x0 = 190
    cw = (W - 14 - x0) // len(cities)
    for i, (city, temp, rain, wind) in enumerate(cities):
        cx = x0 + i * cw
        if i:
            d.line([(cx, wy + 8), (cx, wy + wh - 8)], fill=BORDER, width=1)
        d.text((cx + 10, wy + 6), city, font=f_wcity, fill=INK)
        d.text((cx + 10, wy + 24), temp, font=f_wval, fill=INK)
        d.text((cx + 10, wy + 40), f"{rain} \u00b7 {wind}", font=f_wval,
               fill=MUTED)

    # ---- Story cards: 2 columns x 3 rows ----
    stories = [
        dict(tag="WEATHER", pic="cyclone.webp",
             head="Cyclone Akvan slams into India's east coast",
             body="The storm crossed near Gopalpur, Odisha, with winds of "
                  "70\u201380 kmph. Over 300,000 people were moved to safety "
                  "as red alerts covered the coast."),
        dict(tag="KYIV", pic="kyiv.webp",
             head="Ballistic missiles strike Kyiv overnight",
             body="Russia hit the capital with ballistic missiles, setting "
                  "fires in several districts. Debris struck a three-storey "
                  "building in Obolonskyi; no casualties were reported "
                  "in early accounts."),
        dict(tag="GULF", pic="gulf.webp",
             head="Houthis hit Saudi oil pipeline; missile intercepted",
             body="The Houthis said drones struck two pumping stations on "
                  "the East-West pipeline, starting fires. Saudi defences "
                  "intercepted a ballistic missile aimed at the south."),
        dict(tag="USA", pic="florida.webp",
             head="Florida floods as storm threatens holiday travel",
             body="A storm off the coast may become Tropical Storm Kyle. "
                  "More than 100 people were rescued in Brevard County and "
                  "schools closed as rivers hit record levels."),
        dict(tag="COP31", pic="cop31.webp",
             head="COP31 reaches its final day still split on a deal",
             body="Negotiators in Antalya faced the closing deadline divided "
                  "over fossil fuels and climate finance, with a draft deal "
                  "stripped of a fossil-fuel pledge."),
        dict(tag="TOKYO", pic="tokyo.webp",
             head="13,000 march in Tokyo against Takaichi government",
             body="Thousands rallied in the capital against the policies of "
                  "Prime Minister Sanae Takaichi's government. The march "
                  "through central Tokyo drew about 13,000 people, "
                  "reports said."),
    ]

    mx, gutter = 14, 12
    cw_card = (W - 2 * mx - gutter) // 2
    top = wy + wh + 12
    rows = 3
    ch_card = (H - top - 34) // rows - 10
    pic_h = 140

    for idx, s in enumerate(stories):
        col, row = idx % 2, idx // 2
        x = mx + col * (cw_card + gutter)
        y = top + row * (ch_card + 10)
        d.rectangle([x, y, x + cw_card, y + ch_card], fill=WHITE,
                    outline=BORDER, width=1)
        pic = load_pic(s["pic"], cw_card - 2, pic_h)
        img.paste(pic, (x + 1, y + 1))
        # tag chip over the picture's bottom-left
        tag = s["tag"]
        tw = d.textlength(tag, font=f_tag) + 16
        ty = y + 1 + pic_h - 24
        d.rectangle([x + 1, ty, x + 1 + tw, ty + 23], fill=TAG_BG)
        d.text((x + 9, ty + 4), tag, font=f_tag, fill=WHITE)
        tx = x + 12
        tw_text = cw_card - 24
        hy = y + pic_h + 12
        head_lines = fit_lines(d, s["head"], f_head, tw_text, 2)
        for i, ln in enumerate(head_lines):
            d.text((tx, hy + i * 22), ln, font=f_head, fill=INK)
        by = hy + len(head_lines) * 22 + 4
        body_lines = fit_lines(d, s["body"], f_body, tw_text, 3)
        for i, ln in enumerate(body_lines):
            d.text((tx, by + i * 17), ln, font=f_body, fill=(60, 60, 60))
        # overflow assert: last body line must end inside the card
        assert by + len(body_lines) * 17 <= y + ch_card - 6, \
            f"card {s['tag']} overflows"

    # ---- Footer ----
    fy = H - 26
    d.line([(14, fy - 8), (W - 14, fy - 8)], fill=BORDER, width=1)
    foot = ("Sources: Reuters \u00b7 IMD \u00b7 CNN \u00b7 EIA \u00b7 "
            "COP31 \u00b7 News.Az \u00b7 Open-Meteo ERA5 \u2014 "
            "six stories verified 20 November 2026")
    d.text((W // 2, fy), foot, font=f_foot, fill=MUTED, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"saved {OUT}: {img.size}, {size} bytes")
    if size > 1048576:
        img.save(OUT, "JPEG", quality=88)
        print(f"over 1 MiB, saved as JPEG: {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
