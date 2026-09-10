#!/usr/bin/env python3
"""Generate 1200x630 OG/social image at assets/og.png (comic style, Pillow only).
Usage: python3 tools/make_og.py
"""
import math
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "og.png"
SRC = ROOT / "assets" / "maya" / "pose-alarm.png"

W, H = 1200, 630
PAPER = "#F3EBD6"
RED = "#E5322B"
YELLOW = "#FFD22E"
INK = "#111111"

BOLD_CANDIDATES = [
    "Bangers-Regular.ttf",
    "Bangers.ttf",
    "DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
]


def load_font(size):
    for cand in BOLD_CANDIDATES:
        try:
            return ImageFont.truetype(cand, size)
        except Exception:
            continue
    return ImageFont.load_default()


def burst_points(cx, cy, rx_out, ry_out, rx_in, ry_in, spikes=16):
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes - math.pi / 2
        rx, ry = (rx_out, ry_out) if i % 2 == 0 else (rx_in, ry_in)
        pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
    return pts


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Red halftone dots band (bottom strip).
    band_y = 500
    d.rectangle([0, band_y, W, H], fill=RED)
    d.line([0, band_y, W, band_y], fill=INK, width=4)
    dot_fill = PAPER
    spacing, r = 20, 4
    row = 0
    y = band_y + 12
    while y < H:
        xoff = (spacing // 2) if row % 2 else 0
        x = 12 + xoff
        while x < W:
            d.ellipse([x - r, y - r, x + r, y + r], fill=dot_fill)
            x += spacing
        y += spacing
        row += 1

    # Yellow title burst with ink border + hard shadow.
    cx, cy = 385, 225
    pts = burst_points(cx, cy, 370, 160, 325, 122, spikes=16)
    shadow = [(x + 10, y + 10) for x, y in pts]
    d.polygon(shadow, fill=INK)
    d.polygon(pts, fill=YELLOW, outline=INK)
    # 4px outline: redraw scaled outline via line loop.
    d.line(pts + [pts[0]], fill=INK, width=4, joint="curve")

    # Big title (two lines, auto-fit inside burst).
    lines = ["JUST MOVE", "THE BUTTON"]
    size = 76
    while size > 40:
        f_try = load_font(size)
        if max(d.textlength(ln, font=f_try) for ln in lines) <= 500:
            break
        size -= 4
    f_title = load_font(size)
    for i, line in enumerate(lines):
        tw = d.textlength(line, font=f_title)
        # ascent/descent for vertical centering of the two-line block
        bbox = d.textbbox((0, 0), line, font=f_title)
        th = bbox[3] - bbox[1]
        ly = cy - th - 6 + i * (th + 12)
        d.text((cx - tw / 2, ly), line, font=f_title, fill=INK)

    # Subtitle badge: white box, 4px ink border, hard shadow.
    f_sub = load_font(30)
    sub = "Issue #1 \u00b7 A five-minute job"
    sw = d.textlength(sub, font=f_sub)
    sbbox = d.textbbox((0, 0), sub, font=f_sub)
    sh = sbbox[3] - sbbox[1]
    pad_x, pad_y = 18, 10
    bx0, by0 = 60, 372
    bx1, by1 = bx0 + sw + pad_x * 2, by0 + sh + pad_y * 2
    d.rectangle([bx0 + 7, by0 + 7, bx1 + 7, by1 + 7], fill=INK)
    d.rectangle([bx0, by0, bx1, by1], fill="white", outline=INK, width=4)
    d.text((bx0 + pad_x, by0 + pad_y - 2), sub, font=f_sub, fill=INK)

    # Small description, wrapped.
    f_small = load_font(24)
    desc = "An interactive comic about the invisible work behind a five-minute change."
    for j, ln in enumerate(wrap(d, desc, f_small, 660)):
        d.text((60, 438 + j * 32), ln, font=f_small, fill=INK)

    # Maya on the right, fit height ~560px.
    maya = Image.open(SRC).convert("RGBA")
    target_h = 560
    if maya.height != target_h:
        maya = maya.resize((int(maya.width * target_h / maya.height), target_h), Image.LANCZOS)
    mx = W - maya.width - 36
    my = (H - maya.height) // 2 - 6
    img.paste(maya, (mx, my), maya)

    # Outer ink frame.
    d.rectangle([2, 2, W - 3, H - 3], outline=INK, width=4)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
