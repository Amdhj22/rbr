#!/usr/bin/env python3
"""
Generate preview images for RBR theme.
Reads palette.json as the single source of truth and renders:

  - assets/palette.png           : full color showcase (accents + neutrals)
  - assets/preview-terminal.png  : mock terminal UI demonstrating the theme

Usage:
    python3 scripts/generate_previews.py
"""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PALETTE = json.loads((ROOT / "palette.json").read_text())
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


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


def colors() -> dict:
    return PALETTE["flavors"]["classic"]["colors"]


def by_name(name: str) -> tuple[int, int, int]:
    return hx(colors()[name]["hex"])


def label_on(bg: tuple[int, int, int]) -> tuple[int, int, int]:
    """Pick a readable label color for a given background using perceptual
    luminance (Y' = 0.299R + 0.587G + 0.114B). Yellow hues are bright
    perceptually even when HSL lightness is moderate, so luminance beats
    HSL.l for this decision."""
    r, g, b = bg
    y = 0.299 * r + 0.587 * g + 0.114 * b
    return by_name("base") if y > 140 else by_name("text")


# ---------------------------------------------------------------------------
# palette showcase
# ---------------------------------------------------------------------------

def rounded_chip(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    fill: tuple[int, int, int],
    radius: int = 14,
) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def generate_palette() -> Path:
    W, H = 1600, 1100
    base = by_name("base")
    img = Image.new("RGB", (W, H), base)
    d = ImageDraw.Draw(img)

    # ---- title block ------------------------------------------------------
    d.text((60, 52), "RBR", fill=by_name("kerb_red"), font=font(96))
    d.text(
        (60, 160),
        "Red Bull Racing color scheme",
        fill=by_name("text"),
        font=font(34),
    )
    d.text(
        (60, 208),
        "Classic · v2.1.0 · 26 colors",
        fill=by_name("subtext1"),
        font=font(22),
    )

    # Kerb-red signature bar on the right
    rounded_chip(d, (W - 340, 70, W - 60, 90), by_name("kerb_red"), radius=10)
    rounded_chip(d, (W - 340, 100, W - 60, 112), by_name("rb_yellow"), radius=6)
    d.text((W - 340, 128), "two-accent scheme", fill=by_name("subtext1"), font=font(20))

    # ---- accent grid (7 x 2) ---------------------------------------------
    accents = [k for k, v in colors().items() if v["accent"]]
    d.text((60, 290), "ACCENTS", fill=by_name("subtext0"), font=font(22))
    d.line((60, 325, W - 60, 325), fill=by_name("overlay0"), width=1)

    ROWS, COLS = 2, 7
    cell_w = (W - 120 - (COLS - 1) * 18) // COLS
    cell_h = 140
    top = 355

    for idx, name in enumerate(accents):
        r, c = divmod(idx, COLS)
        x = 60 + c * (cell_w + 18)
        y = top + r * (cell_h + 18)
        info = colors()[name]
        color = hx(info["hex"])

        rounded_chip(d, (x, y, x + cell_w, y + cell_h), color)

        label_color = label_on(color)
        d.text((x + 16, y + 14), info["name"], fill=label_color, font=font(20))
        d.text(
            (x + 16, y + cell_h - 32),
            f"#{info['hex']}",
            fill=label_color,
            font=font(16),
        )

    # ---- neutral ladder (12 x 1, full-width bar) -------------------------
    neutrals = [k for k, v in colors().items() if not v["accent"]]
    # Re-order from darkest to brightest for a readable ladder.
    neutrals = sorted(neutrals, key=lambda k: colors()[k]["hsl"]["l"])

    ladder_top = 760
    d.text((60, ladder_top - 42), "NEUTRAL LAYERS", fill=by_name("subtext0"), font=font(22))
    d.line((60, ladder_top - 12, W - 60, ladder_top - 12), fill=by_name("overlay0"), width=1)

    bar_w = (W - 120 - 11 * 8) // 12
    for idx, name in enumerate(neutrals):
        x = 60 + idx * (bar_w + 8)
        info = colors()[name]
        color = hx(info["hex"])
        chip_box = (x, ladder_top + 10, x + bar_w, ladder_top + 170)
        rounded_chip(d, chip_box, color, radius=10)

        # Outline for chips that are too close to the page background,
        # otherwise they disappear.
        if 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2] < 20:
            d.rounded_rectangle(
                chip_box, radius=10, outline=by_name("overlay0"), width=1
            )

        label_color = label_on(color)
        d.text((x + 10, ladder_top + 16), info["name"], fill=label_color, font=font(15))
        d.text((x + 10, ladder_top + 148), f"#{info['hex']}", fill=label_color, font=font(12))

    # ---- footer -----------------------------------------------------------
    d.text(
        (60, H - 54),
        "github.com/Amdhj22/rbr-theme",
        fill=by_name("subtext1"),
        font=font(18),
    )
    d.text(
        (W - 340, H - 54),
        "MIT License",
        fill=by_name("subtext1"),
        font=font(18),
    )

    out = ASSETS / "palette.png"
    img.save(out, "PNG", optimize=True)
    return out


# ---------------------------------------------------------------------------
# mock terminal preview
# ---------------------------------------------------------------------------

def generate_terminal() -> Path:
    """A mocked terminal window showing prompt + git status + ls + neovim strip."""
    W, H = 1600, 1000
    base = by_name("base")
    img = Image.new("RGB", (W, H), by_name("mantle"))
    d = ImageDraw.Draw(img)

    # --- window chrome ----------------------------------------------------
    chrome_h = 54
    d.rounded_rectangle((30, 30, W - 30, H - 30), radius=18, fill=base)
    d.rounded_rectangle((30, 30, W - 30, 30 + chrome_h), radius=18, fill=by_name("surface0"))
    # square the bottom of the chrome so it blends into the body
    d.rectangle((30, 30 + chrome_h - 18, W - 30, 30 + chrome_h), fill=by_name("surface0"))

    # traffic lights
    cx = 58
    for i, c in enumerate([by_name("kerb_bright"), by_name("rb_warm"), by_name("paddock_green")]):
        d.ellipse((cx + i * 22, 30 + chrome_h // 2 - 8, cx + i * 22 + 16, 30 + chrome_h // 2 + 8), fill=c)

    # tabs in chrome
    tab_y = 30 + 10
    d.rounded_rectangle((150, tab_y, 370, tab_y + 34), radius=8, fill=by_name("surface2"))
    d.text((164, tab_y + 7), "zsh · ~/dev/rbr-theme", fill=by_name("text"), font=font(18))
    # active tab indicator (kerb red bar)
    d.rectangle((150, tab_y + 30, 370, tab_y + 34), fill=by_name("kerb_red"))

    d.rounded_rectangle((384, tab_y, 560, tab_y + 34), radius=8, fill=by_name("surface1"))
    d.text((398, tab_y + 7), "nvim", fill=by_name("subtext1"), font=font(18))

    # --- body -------------------------------------------------------------
    mono = font(22)
    y = chrome_h + 70
    line_h = 32
    x = 74

    def line(segments: list[tuple[str, tuple[int, int, int]]], yy: int):
        cx = x
        for text, col in segments:
            d.text((cx, yy), text, fill=col, font=mono)
            # width approximation; SFNSMono at size 22 ≈ 13.2 px per char
            cx += int(len(text) * 13.2)

    text_col = by_name("text")
    sub = by_name("subtext1")
    red = by_name("kerb_red")
    yellow = by_name("rb_yellow")
    warm = by_name("rb_warm")
    green = by_name("paddock_green")
    green_sub = by_name("track_green")
    blue = by_name("oracle_blue")
    sky = by_name("sky_blue")
    orange = by_name("crowd_orange")
    err = by_name("kerb_bright")

    # prompt 1: git status
    line([
        ("~/dev/rbr-theme ", sky),
        ("on ", sub),
        ("git:", sub), ("main", red),
        ("  [", sub), ("!2", yellow), (" ?1", warm), ("]", sub),
    ], y); y += line_h
    line([("> ", yellow), ("git status --short", text_col)], y); y += line_h
    line([(" M ", yellow), ("README.md", text_col)], y); y += line_h
    line([(" M ", yellow), ("palette.json", text_col)], y); y += line_h
    line([("?? ", warm), ("assets/palette.png", text_col)], y); y += line_h
    y += 8

    # prompt 2: ls
    line([
        ("~/dev/rbr-theme ", sky),
        ("on ", sub),
        ("git:", sub), ("main", red),
    ], y); y += line_h
    line([("> ", yellow), ("ls -la", text_col)], y); y += line_h
    line([("drwxr-xr-x  ", sub), ("assets", sky), ("/", sub)], y); y += line_h
    line([("drwxr-xr-x  ", sub), ("scripts", sky), ("/", sub)], y); y += line_h
    line([("drwxr-xr-x  ", sub), ("terminals", sky), ("/", sub)], y); y += line_h
    line([("-rw-r--r--  ", sub), ("LICENSE", green_sub)], y); y += line_h
    line([("-rw-r--r--  ", sub), ("README.md", green_sub)], y); y += line_h
    line([("-rw-r--r--  ", sub), ("STYLE-GUIDE.md", green_sub)], y); y += line_h
    line([("-rw-r--r--  ", sub), ("palette.json", green_sub)], y); y += line_h
    y += 8

    # prompt 3: test run (success)
    line([
        ("~/dev/rbr-theme ", sky),
        ("on ", sub),
        ("git:", sub), ("main", red),
    ], y); y += line_h
    line([("> ", yellow), ("cargo test", text_col)], y); y += line_h
    line([("   Compiling", green_sub), (" rbr-theme v2.1.0", text_col)], y); y += line_h
    line([("    Finished", green), (" test [optimized] in 1.82s", sub)], y); y += line_h
    line([("running 12 tests", text_col)], y); y += line_h
    line([
        ("test result: ", text_col),
        ("ok", green),
        (". ", text_col),
        ("12", green),
        (" passed; ", text_col),
        ("0", sub), (" failed; ", text_col),
        ("0", sub), (" ignored", text_col),
    ], y); y += line_h
    y += 8

    # prompt 4: k8s context line (shows prod warning in red)
    line([
        ("~/dev/rbr-theme ", sky),
        ("on ", sub),
        ("git:", sub), ("main", red),
        ("  k8s:", blue), ("eks-prod", err), ("/", sub), ("api", orange),
    ], y); y += line_h

    # current line: active prompt with cursor
    line([("> ", yellow)], y)
    # cursor block right after the "> "
    d.rectangle((x + 28, y + 2, x + 28 + 14, y + 28), fill=yellow)

    # --- footer caption ---------------------------------------------------
    d.text(
        (74, H - 70),
        "Ghostty / iTerm2 · Classic flavor",
        fill=by_name("subtext0"),
        font=font(18),
    )

    out = ASSETS / "preview-terminal.png"
    img.save(out, "PNG", optimize=True)
    return out


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

def main() -> None:
    p1 = generate_palette()
    p2 = generate_terminal()
    print(f"wrote {p1.relative_to(ROOT)}")
    print(f"wrote {p2.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
