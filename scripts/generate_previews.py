#!/usr/bin/env python3
"""
Generate the README hero image from palette.json (v2.2 schema).

Run:
    python3 scripts/generate_previews.py

Output:
    assets/palette.png
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PALETTE = json.loads((ROOT / "palette.json").read_text())
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

ui = PALETTE["ui"]
brand = PALETTE["brand"]
ansi = PALETTE["ansi"]
sem = PALETTE["semantic"]
meta = PALETTE["meta"]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def hx(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore


_FONT_CANDIDATES = [
    "/System/Library/Fonts/SFNSMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/SFNS.ttf",
    "/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
]


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in _FONT_CANDIDATES:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def label_on(bg: tuple[int, int, int]) -> tuple[int, int, int]:
    """Pick a readable label color via Rec. 601 luminance."""
    r, g, b = bg
    y = 0.299 * r + 0.587 * g + 0.114 * b
    return hx(ui["bg"]) if y > 140 else hx(ui["fg"])


def chip(d, xy, fill, radius=6, outline=None, width=0):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------------------
# hero image
# ---------------------------------------------------------------------------

def palette_hero() -> Path:
    W, H = 1080, 920
    img = Image.new("RGB", (W, H), hx(ui["bg"]))
    d = ImageDraw.Draw(img)

    # ---- Header ----------------------------------------------------------
    chip(d, (24, 24, W - 24, 110), hx(ui["bg_float"]), radius=10)
    d.text((44, 32), "RBR", fill=hx(brand["kerb_red"]), font=font(40))
    d.text((44, 78),
           f"v{meta['version']}  ·  Red Bull Racing kerb red × RB yellow × chequer white",
           fill=hx(ui["fg_dim"]), font=font(13))
    chip(d, (W - 92, 32, W - 44, 50), hx(brand["kerb_red"]), radius=4)
    chip(d, (W - 92, 56, W - 44, 74), hx(brand["rb_yellow"]), radius=4)
    chip(d, (W - 92, 80, W - 44, 98), hx(brand["chequer_white"]), radius=4,
         outline=hx(ui["fg_subtle"]), width=1)

    # ---- Signature trio --------------------------------------------------
    d.text((28, 130), "SIGNATURE TRIO", fill=hx(ui["fg_subtle"]), font=font(11))

    cw3 = (W - 48 - 2 * 8) // 3
    sy0, sh = 150, 96

    chip(d, (24, sy0, 24 + cw3, sy0 + sh), hx(brand["kerb_red"]), radius=8)
    d.text((44, sy0 + 12), "KERB RED", fill=hx(ui["bg"]), font=font(18))
    d.text((44, sy0 + 42), brand["kerb_red"], fill=hx(ui["bg"]), font=font(12))
    d.text((44, sy0 + 70), "active  ·  selected  ·  branch",
           fill=hx(ui["bg"]), font=font(10))

    x_y = 24 + cw3 + 8
    chip(d, (x_y, sy0, x_y + cw3, sy0 + sh), hx(brand["rb_yellow"]), radius=8)
    d.text((x_y + 20, sy0 + 12), "RB YELLOW", fill=hx(ui["bg"]), font=font(18))
    d.text((x_y + 20, sy0 + 42), brand["rb_yellow"], fill=hx(ui["bg"]), font=font(12))
    d.text((x_y + 20, sy0 + 70), "cursor  ·  warning  ·  attention",
           fill=hx(ui["bg"]), font=font(10))

    x_w = 24 + 2 * (cw3 + 8)
    chip(d, (x_w, sy0, x_w + cw3, sy0 + sh), hx(brand["chequer_white"]), radius=8,
         outline=hx(ui["fg_subtle"]), width=1)
    d.text((x_w + 20, sy0 + 12), "CHEQUER WHITE", fill=hx(ui["bg"]), font=font(18))
    d.text((x_w + 20, sy0 + 42), brand["chequer_white"], fill=hx(ui["bg"]), font=font(12))
    d.text((x_w + 20, sy0 + 70), "function  ·  method",
           fill=hx(ui["bg"]), font=font(10))

    # ---- Background tones (6) -------------------------------------------
    d.text((28, 268), "BACKGROUND TONES", fill=hx(ui["fg_subtle"]), font=font(11))
    bg_items = [
        ("bg",            ui["bg"],            "canvas"),
        ("bg_dim",        ui["bg_dim"],        "subdued"),
        ("bg_float",      ui["bg_float"],      "floating"),
        ("bg_highlight",  ui["bg_highlight"],  "hover"),
        ("bg_selection",  ui["bg_selection"],  "selected"),
        ("border",        ui["border"],        "divider"),
    ]
    cw = (W - 48 - 5 * 8) // 6
    cy0, ch = 286, 64
    for i, (name, hex_, role) in enumerate(bg_items):
        x = 24 + i * (cw + 8)
        chip(d, (x, cy0, x + cw, cy0 + ch), hx(hex_), radius=6,
             outline=hx(ui["fg_subtle"]), width=1)
        d.text((x + 10, cy0 + 8),  name,  fill=hx(ui["fg"]),       font=font(11))
        d.text((x + 10, cy0 + 26), hex_,  fill=hx(ui["fg_dim"]),   font=font(10))
        d.text((x + 10, cy0 + 44), role,  fill=hx(ui["fg_subtle"]), font=font(9))

    # ---- Foreground tones (3) -------------------------------------------
    d.text((28, 372), "FOREGROUND TONES", fill=hx(ui["fg_subtle"]), font=font(11))
    fg_items = [
        ("fg",        ui["fg"],        "primary text"),
        ("fg_dim",    ui["fg_dim"],    "secondary"),
        ("fg_subtle", ui["fg_subtle"], "muted / comments"),
    ]
    cw3 = (W - 48 - 2 * 8) // 3
    fy0, fh = 390, 76
    for i, (name, hex_, role) in enumerate(fg_items):
        x = 24 + i * (cw3 + 8)
        chip(d, (x, fy0, x + cw3, fy0 + fh), hx(ui["bg_float"]), radius=6)
        d.text((x + 14, fy0 + 10), "Aa sample text",
               fill=hx(hex_), font=font(20))
        d.text((x + 14, fy0 + 42), f"{name}    {hex_}",
               fill=hx(ui["fg_dim"]), font=font(10))
        d.text((x + 14, fy0 + 58), role,
               fill=hx(ui["fg_subtle"]), font=font(9))

    # ---- ANSI 16 ---------------------------------------------------------
    d.text((28, 484), "ANSI 16", fill=hx(ui["fg_subtle"]), font=font(11))
    d.text((W - 350, 484),
           "Red @ index 1, Yellow @ index 3 (ANSI-correct, tools depend on this)",
           fill=hx(ui["fg_subtle"]), font=font(9))
    ansi_keys = [
        "black", "red", "green", "yellow",
        "blue", "magenta", "cyan", "white",
        "bright_black", "bright_red", "bright_green", "bright_yellow",
        "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
    ]
    ay0, row_h = 504, 22
    half_w = (W - 48) // 2
    for i, key in enumerate(ansi_keys):
        col = i // 8
        row = i % 8
        x = 24 + col * (half_w + 8)
        y = ay0 + row * row_h
        chip(d, (x, y + 2, x + 30, y + 18), hx(ansi[key]), radius=2)
        d.text((x + 40, y + 3), str(i), fill=hx(ui["fg_subtle"]), font=font(10))
        d.text((x + 72, y + 3), key,    fill=hx(ui["fg"]),        font=font(11))
        d.text((x + half_w - 90, y + 3), ansi[key],
               fill=hx(ui["fg_dim"]), font=font(10))

    # ---- Semantic roles --------------------------------------------------
    sy0 = 690
    d.text((28, sy0), "SEMANTIC ROLES", fill=hx(ui["fg_subtle"]), font=font(11))

    rows = [
        [
            ("× red flag",     "error",       sem["error"]["value"]),
            ("⚠ yellow flag",  "warning",     sem["warning"]["value"]),
            ("✓ green flag",   "success",     sem["success"]["value"]),
            ("◆ blue flag",    "info",        sem["info"]["value"]),
            ("main",           "branch",      sem["branch"]),
        ],
        [
            ("◆ dev",          "k8s_context", sem["k8s_context"]),
            ("☢ prod",         "k8s_prod",    sem["k8s_prod"]),
            ("+ added",        "git_added",   sem["git_added"]),
            ("~ modified",     "git_modified",sem["git_modified"]),
            ("- deleted",      "git_deleted", sem["git_deleted"]),
        ],
    ]
    cw5 = (W - 48 - 4 * 8) // 5
    cell_h = 50
    for ri, row in enumerate(rows):
        for ci, (text, role, hex_) in enumerate(row):
            x = 24 + ci * (cw5 + 8)
            y = sy0 + 18 + ri * (cell_h + 8)
            chip(d, (x, y, x + cw5, y + cell_h), hx(ui["bg_float"]), radius=6)
            chip(d, (x, y, x + 4, y + cell_h),  hx(hex_), radius=2)
            d.text((x + 14, y + 6),  text, fill=hx(hex_),       font=font(13))
            d.text((x + 14, y + 28), f"{role}  {hex_}",
                   fill=hx(ui["fg_dim"]), font=font(9))

    # ---- Footer ----------------------------------------------------------
    d.text((28, H - 38), "github.com/Amdhj22/rbr",
           fill=hx(ui["fg_dim"]), font=font(11))
    d.text((W - 240, H - 38), f"MIT License  ·  v{meta['version']}",
           fill=hx(ui["fg_dim"]), font=font(11))

    out = ASSETS / "palette.png"
    img.save(out, "PNG", optimize=True)
    return out


def main() -> None:
    p = palette_hero()
    print(f"wrote {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
