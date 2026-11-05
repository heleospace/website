#!/usr/bin/env python3
"""Builds every logo file on the site from the master artwork.

Run this only when the logo changes:  python3 _build/brand_assets.py
Replace _build/brand/heleospace-logo-source.svg first. It holds the logo twice
(black, then white); each copy is a wordmark group followed by a mark group.
PNG files are rendered with Google Chrome, which must be installed."""
import pathlib, re, subprocess, tempfile, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_build/brand/heleospace-logo-source.svg"
SITE = ROOT / "site"
KIT = SITE / "assets/brand"
IMG = SITE / "assets/img"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

groups = re.findall(r'<g transform="matrix\(([^)]*)\)">(.*?)</g>', SRC.read_text(), re.S)
assert len(groups) == 4, "expected wordmark and mark groups, in black and in white"

def artwork(body):
    return " ".join(re.sub(r'\s*style="[^"]*"', "", body).split()).replace("/> <", "/><")

(word_m, word_raw), (mark_m, mark_raw) = groups[:2]
word_a, _, _, _, word_x, word_y = map(float, word_m.split(","))
mark_a, _, _, _, mark_x, mark_y = map(float, mark_m.split(","))
word, mark = artwork(word_raw), artwork(mark_raw)

# Measured from the artwork, in source units before each group's matrix.
M_X0, M_Y0, M_SIZE = 141.598, 651.598, 199.804
W_X1, W_Y1 = 785.825, 765.772
x0, y0 = mark_a * M_X0 + mark_x, mark_a * M_Y0 + mark_y
LOGO_W = round(word_a * W_X1 + word_x - x0, 2)
LOGO_H = round(word_a * W_Y1 + word_y - y0, 2)

def matrix(a, x, y):
    return f"matrix({a} 0 0 {a} {round(x - x0, 4)} {round(y - y0, 4)})"

LOGO_ART = (f'<g fill-rule="evenodd" transform="{matrix(mark_a, mark_x, mark_y)}">{mark}</g>'
            f'<g transform="{matrix(word_a, word_x, word_y)}">{word}</g>')
MARK_ART = f'<g fill-rule="evenodd" transform="translate({-M_X0} {-M_Y0})">{mark}</g>'
LOGO_BOX = f"0 0 {LOGO_W} {LOGO_H}"
MARK_BOX = f"0 0 {M_SIZE} {M_SIZE}"

def svg(box, art, fill, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" role="img" aria-label="{title}">'
            f'<title>{title}</title><g fill="{fill}">{art}</g></svg>\n')

def render(items):
    """items: (html body, width, height, output path, transparent)."""
    with tempfile.TemporaryDirectory() as tmp:
        for i, (body, w, h, out, clear) in enumerate(items):
            page = pathlib.Path(tmp) / f"{i}.html"
            page.write_text(f'<!doctype html><html><body style="margin:0;background:{"transparent" if clear else "#fff"}">{body}</body></html>')
            args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={tmp}/profile",
                    f"--window-size={w},{h}", f"--screenshot={out}", page.as_uri()]
            if clear:
                args.insert(4, "--default-background-color=00000000")
            subprocess.run(args, check=True, capture_output=True, timeout=120)

def box_svg(box, art, fill, w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" width="{w}" height="{h}" '
            f'style="display:block"><g fill="{fill}">{art}</g></svg>')

KIT.mkdir(parents=True, exist_ok=True)
FILES = {"logo-black": (LOGO_BOX, LOGO_ART, "#000000", "Heleospace"),
         "logo-white": (LOGO_BOX, LOGO_ART, "#FFFFFF", "Heleospace"),
         "mark-black": (MARK_BOX, MARK_ART, "#000000", "Heleospace mark"),
         "mark-white": (MARK_BOX, MARK_ART, "#FFFFFF", "Heleospace mark")}
jobs = []
for name, (box, art, fill, title) in FILES.items():
    (KIT / f"heleospace-{name}.svg").write_text(svg(box, art, fill, title))
    w = 3000 if name.startswith("logo") else 1024
    h = round(w * LOGO_H / LOGO_W) + 1 if name.startswith("logo") else 1024
    jobs.append((box_svg(box, art, fill, w, h), w, h, KIT / f"heleospace-{name}.png", True))

# The sprite the site header and footer draw from, so the logo can follow the text colour.
(IMG / "logo-sprite.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg"><symbol id="logo" viewBox="{LOGO_BOX}"><g fill="currentColor">{LOGO_ART}</g></symbol></svg>\n')

# Older file names keep working, now with the current artwork.
(IMG / "heleospace-mark.svg").write_text(svg(MARK_BOX, MARK_ART, "#000000", "Heleospace mark"))
jobs.append((box_svg(LOGO_BOX, LOGO_ART, "#000000", 1431, round(1431 * LOGO_H / LOGO_W) + 1), 1431, round(1431 * LOGO_H / LOGO_W) + 1, IMG / "heleospace-logo-official.png", True))

# Favicons: the black mark on a white tile.
scale = round(44 / M_SIZE, 5)
(SITE / "favicon.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#FFFFFF"/>'
    f'<g fill="#000000" transform="translate(10 10) scale({scale})">{MARK_ART}</g></svg>\n')
def tile(size, radius):
    inner = round(size * 44 / 64)
    return (f'<div style="width:{size}px;height:{size}px;background:#fff;border-radius:{radius}px;display:flex;align-items:center;justify-content:center">'
            f'{box_svg(MARK_BOX, MARK_ART, "#000000", inner, inner)}</div>')
jobs.append((tile(32, 6), 32, 32, SITE / "favicon-32.png", True))
jobs.append((tile(180, 0), 180, 180, SITE / "apple-touch-icon.png", False))

# Social sharing image.
og_w = 760
og_h = round(og_w * LOGO_H / LOGO_W)
jobs.append((f'<div style="width:1200px;height:630px;background:#F4F2ED;display:flex;align-items:center;justify-content:center">'
             f'{box_svg(LOGO_BOX, LOGO_ART, "#000000", og_w, og_h)}</div>', 1200, 630, IMG / "og-image.png", False))
render(jobs)

README = """Heleospace brand kit
====================

logo-black / logo-white   The full logo. Use this one by default.
mark-black / mark-white   The mark alone, for small and square spaces.

SVG is best for almost everything. PNG files have transparent backgrounds.

Use the files as they are. Do not recolour, stretch, redraw or add effects.
Full guidelines and terms of use: https://heleo.space/brand/
Questions: hello@heleo.space
"""
# Fixed dates keep the zip byte-identical between runs when the artwork has not changed.
with zipfile.ZipFile(KIT / "heleospace-brand-kit.zip", "w", zipfile.ZIP_DEFLATED) as z:
    entries = [("heleospace-brand-kit/README.txt", README.encode())]
    for name in FILES:
        for ext in ("svg", "png"):
            entries.append((f"heleospace-brand-kit/{ext}/heleospace-{name}.{ext}", (KIT / f"heleospace-{name}.{ext}").read_bytes()))
    for arc, data in entries:
        info = zipfile.ZipInfo(arc, date_time=(2026, 11, 5, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, data)
print(f"logo {LOGO_W} x {LOGO_H}; wrote assets to {KIT}")
