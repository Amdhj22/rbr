# RBR Style Guide

> The rules that make an RBR port feel like RBR, and not just "a dark theme with red in it."

This document is the source of truth for color semantics. If you are building a port (Neovim, tmux, VS Code, etc.), follow these rules so every RBR-flavored surface behaves consistently.

---

## Philosophy

RBR is a **three-accent scheme**: **Kerb Red** (`#e84a55`), **RB Yellow** (`#ffd84d`), and **Chequer White** (`#ffffff`). Every other color is deliberately pastel so the trio dominates the viewport — the same three colors that own the Red Bull Racing livery.

Five principles govern every color choice:

1. **Red means "this one."** Kerb Red marks the *single* active/selected thing on screen — the current branch, the active tab, the focused pane. If two things are red, neither reads as primary.
2. **Yellow means "look here now."** RB Yellow marks urgency — the cursor, an unread notification, a modified file, a warning. It is motion in a still image.
3. **White means "this is callable."** Chequer White is the function/method accent — the third dominant color in any code buffer. Function names jump out so the eye can scan call sites at a glance.
4. **Everything else steps back.** Greens, blues, and cyans stay in a narrow pastel band (HSL lightness 60–78). They exist to classify content, not to compete with the trio.
5. **Magenta is intentionally neutral grey.** Numbers and constants get visual weight without color noise — the magenta slot is reserved for that, not for another saturated accent.

If you ever feel like adding a fourth "shouty" color, you are drifting away from RBR. Use a layer (`surface*`, `overlay*`) instead.

---

## Flavors

| Flavor    | Emoji | Mode | Hex Base   | Notes                                   |
| --------- | ----- | ---- | ---------- | --------------------------------------- |
| `classic` | 🏁    | dark | `#0a1128`  | The only flavor in v2.1. Night-race navy. |

Future flavors (e.g. `monza` for a light variant) will follow the same scheme structure — only hex values change.

---

## Color Categories

Every color belongs to exactly one of two categories:

### 1. Accent colors (14 total)

High-saturation, hue-rich colors used to **classify semantic meaning**. Accents are the vocabulary a port uses to paint syntax, git status, diagnostics, and prompts.

Accents are ordered by visual priority:

| Order | Name            | Hex       | Role             | Primary use                                   |
| ----: | --------------- | --------- | ---------------- | --------------------------------------------- |
|     0 | Kerb Red        | `#e84a55` | **primary**      | Selected/active, branch name, prod indicator  |
|     1 | Kerb Bright     | `#f56570` | error            | Errors, deletions, destructive actions        |
|     2 | Kerb Pure       | `#cc1e4a` | brand-pure       | Badges, logos, brand marks                    |
|     3 | RB Yellow       | `#ffd84d` | **secondary**    | Cursor, warnings, current-line, modifications |
|     4 | RB Warm         | `#f5c842` | warning          | ANSI yellow slot, sustained warnings          |
|     5 | RB Pure         | `#ffc906` | brand-pure       | Logos, brand marks                            |
|     6 | Oracle Blue     | `#82a0d8` | info             | Links, info messages, k8s context             |
|     7 | Sky Blue        | `#a4bde8` | info-bright      | Directories, renamed files                    |
|     8 | Track Green     | `#9cc080` | success-subtle   | ANSI green slot, hostname, staged files       |
|     9 | Paddock Green   | `#b8d49e` | success          | Test passes, successful runs, added files     |
|    10 | Cool Grey       | `#a8a8b0` | magenta-neutral  | ANSI magenta slot — intentionally desaturated |
|    11 | Light Grey      | `#c8c8d0` | bright-neutral   | Numbers, constants — visual weight without color noise |
|    12 | Livery Blue            | `#2563eb` | cyan             | ANSI cyan slot, hint text                     |
|    13 | Livery Blue Bright       | `#4D7EFF` | hint             | Subtle guidance, pit-lane signals             |

### 2. Neutral layers (12 total)

Low-saturation colors arranged on a **lightness ladder** from deepest background (`crust`) to brightest foreground (`text`). Neutrals carry no semantic meaning — they provide spatial hierarchy.

| Order | Name      | Hex       | Role             | Primary use                              |
| ----: | --------- | --------- | ---------------- | ---------------------------------------- |
|    14 | Text      | `#c8d0e8` | fg               | Primary body text                        |
|    15 | Subtext 1 | `#8590ae` | fg-muted         | Secondary text, captions                 |
|    16 | Subtext 0 | `#6a7495` | fg-subtle        | Disabled text, placeholders, comments    |
|    17 | Overlay 2 | `#565f80` | overlay-strong   | Strong borders, inactive highlights      |
|    18 | Overlay 1 | `#4a5580` | overlay          | Medium borders, rulers                   |
|    19 | Overlay 0 | `#3a4466` | overlay-subtle   | ANSI bright-black, line numbers          |
|    20 | Surface 2 | `#1f2a52` | surface-strong   | Selection background, active tabs        |
|    21 | Surface 1 | `#15203f` | surface          | Current-line highlight, hover            |
|    22 | Surface 0 | `#121a36` | surface-subtle   | Floating panels, tooltips                |
|    23 | Base      | `#0a1128` | bg               | Primary editor/terminal background       |
|    24 | Mantle    | `#070d1f` | bg-dim           | Sidebar, secondary panes                 |
|    25 | Crust     | `#05091a` | bg-darkest       | ANSI black slot, gutter shadow           |

---

## Applying the Color Rules

### UI chrome

| Element             | Use              | Why                                                     |
| ------------------- | ---------------- | ------------------------------------------------------- |
| Window background   | `base`           | The baseline surface.                                   |
| Sidebar / gutter    | `mantle`         | One step darker separates chrome from content.          |
| Floating panel      | `surface0`       | One step lighter lifts transient UI off the background. |
| Active tab          | `surface2` bg + `kerb_red` accent bar | Red marks "this is the one".  |
| Inactive tab        | `mantle`         | Recede without disappearing.                            |
| Status bar          | `surface1`       | Subtly distinct from editor.                            |
| Focus ring / border | `kerb_red`       | Only one focused element exists at a time — earn the red. |
| Unfocused border    | `overlay0`       | Muted structural lines.                                 |
| Selection           | `surface2`       | Preserves text legibility over an accent highlight.     |
| Cursor              | `rb_yellow`      | Highest-attention pixel; yellow is reserved for this.   |
| Cursor-line bg      | `surface1`       | A quiet "you are here" without yelling.                 |

### Syntax highlighting

| Token            | Color          | Rationale                                                  |
| ---------------- | -------------- | ---------------------------------------------------------- |
| Keywords         | `kerb_red`     | Control flow is the "verb" — the most important syntax element. |
| Strings          | `paddock_green`| Data content reads calmly.                                 |
| Numbers          | `light_grey`   | Visible but no color noise — the v2.2 magenta-neutral idea. |
| Functions        | `chequer_white`   | Third brand accent — call sites jump out at a glance.      |
| Types / Classes  | `rb_yellow`    | Structure declarations earn attention.                     |
| Constants        | `cool_grey`    | Immutable values get weight without competing with accents. |
| Variables        | `text`         | The default — no color is also a choice.                   |
| Comments         | `subtext0`     | Visible but clearly deprioritized.                         |
| Operators / Punct| `subtext1`     | Present but not loud.                                      |
| Preproc / Macros | `sky_blue`     | Meta-level code.                                           |

### Diagnostics & git

| Meaning     | Color            |
| ----------- | ---------------- |
| Error       | `kerb_bright`    |
| Warning     | `rb_yellow`      |
| Info        | `oracle_blue`    |
| Hint        | `livery_blue_bright`      |
| Added       | `paddock_green`  |
| Modified    | `rb_yellow`      |
| Deleted     | `kerb_bright`    |
| Renamed     | `sky_blue`       |
| Staged      | `track_green`    |
| Conflict    | `kerb_red`       |

### Prompts & status bars

| Segment                     | Color          |
| --------------------------- | -------------- |
| Current git branch          | `kerb_red`     |
| Working directory           | `sky_blue`     |
| Hostname                    | `track_green`  |
| User                        | `rb_yellow`    |
| k8s context                 | `oracle_blue`  |
| k8s namespace               | `livery_blue`         |
| k8s production indicator    | `kerb_bright`  |
| Elapsed time / exit status  | `subtext1` (ok), `kerb_bright` (fail) |

---

## ANSI Mapping

Ports that only expose 16 ANSI slots should use this canonical mapping. Every terminal port in this repo conforms to it.

| Code | Slot            | Palette color   | Hex       |
| ---: | --------------- | --------------- | --------- |
|    0 | black           | `crust`         | `#05091a` |
|    1 | red             | `kerb_red`      | `#e84a55` |
|    2 | green           | `track_green`   | `#9cc080` |
|    3 | yellow          | `rb_warm`       | `#f5c842` |
|    4 | blue            | `oracle_blue`   | `#82a0d8` |
|    5 | magenta         | `cool_grey`     | `#a8a8b0` |
|    6 | cyan            | `livery_blue`          | `#2563eb` |
|    7 | white           | `text`          | `#c8d0e8` |
|    8 | bright black    | `overlay0`      | `#3a4466` |
|    9 | bright red      | `kerb_bright`   | `#f56570` |
|   10 | bright green    | `paddock_green` | `#b8d49e` |
|   11 | bright yellow   | `rb_yellow`     | `#ffd84d` |
|   12 | bright blue     | `sky_blue`      | `#a4bde8` |
|   13 | bright magenta  | `light_grey`    | `#c8c8d0` |
|   14 | bright cyan     | `livery_blue_bright`     | `#4D7EFF` |
|   15 | bright white    | `track_line`    | `#e8ecf5` |

Notes:
- `ansi.yellow` (slot 3) uses `rb_warm` rather than `rb_yellow` so bulk yellow text stays readable — `rb_yellow` is saved for the bright slot and the cursor.
- `ansi.bright_white` (slot 15) uses a dedicated `#e8ecf5` (the same value `special.track_line` exposes) so it sits one step brighter than `text` (slot 7). v2.1 had the two slots collapsed; v2.2 separates them again so `man` pages and `bat` headers get a distinctly hotter white.

---

## Don'ts

- **Don't** invent new accent colors. If you need another category, reuse an existing accent at reduced alpha, or move the distinction into a neutral layer.
- **Don't** use `kerb_pure` or `rb_pure` for UI surfaces — they are too saturated. Reserve them for logos, badges, or decorative brand marks.
- **Don't** paint large regions in red or yellow. The brand pair is for point-accents, not fills.
- **Don't** mix red and yellow on adjacent pixels. Separate them with a neutral layer to keep both readable.
- **Don't** use `kerb_red` for errors. Errors belong to `kerb_bright`; red is reserved for "the selected thing" so an error never looks like the focused item.

---

## Contrast

All foreground/accent colors meet WCAG AA against `base` (`#0a1128`) for normal text:

| Foreground       | Ratio vs. base | WCAG |
| ---------------- | -------------: | ---- |
| `text`           | 11.2 : 1       | AAA  |
| `rb_yellow`      | 10.4 : 1       | AAA  |
| `bright yellow`  | 11.9 : 1       | AAA  |
| `paddock_green`  |  9.4 : 1       | AAA  |
| `oracle_blue`    |  6.4 : 1       | AA   |
| `kerb_bright`    |  6.2 : 1       | AA   |
| `kerb_red`       |  5.8 : 1       | AA   |
