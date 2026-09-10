#!/usr/bin/env python3
"""Generate 1200x630 OG/social image at assets/og.png, mirroring the live cover.

Mirrors div.coverart (src/engine.js:28-31) styled by src/comic.css:110-113:
full-bleed red bg + halftone dots, yellow title top-left, Maya right,
yellow SFX bottom-left, white issue tag, ink frame. Pillow only.
Usage: python3 tools/make_og.py
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "og.png"
SRC = ROOT / "assets" / "maya" / "pose-alarm.png"

W, H = 1200, 630
RED = (0xE5, 0x32, 0x2B, 255)
YELLOW = (0xFF, 0xD2, 0x2E, 255)
INK = (0x11, 0x11, 0x11, 255)
WHITE = (255, 255, 255, 255)
# Red blended 20% toward ink: approximates ink dots at opacity .2 over red.
DOT = (int(0xE5 * 0.8 + 0x11 * 0.2), int(0x32 * 0.8 + 0x11 * 0.2), int(0x2B * 0.8 + 0x11 * 0.2), 255)

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


def draw_outlined(d, xy, text, font, fill=YELLOW, outline=INK, sw=3, shadow=(6, 6)):
    x, y = xy
    if shadow is not None:
        d.text((x + shadow[0], y + shadow[1]), text, font=font, fill=outline)
    for dx in range(-sw, sw + 1):
        for dy in range(-sw, sw + 1):
            if dx == 0 and dy == 0:
                continue
            if dx * dx + dy * dy > sw * sw:
                continue
            d.text((x + dx, y + dy), text, font=font, fill=outline)
    d.text((x, y), text, font=font, fill=fill)


def main():
    img = Image.new("RGBA", (W, H), RED)
    d = ImageDraw.Draw(img)

    # Full-bleed ink halftone dots overlay (grid approx of .half, opacity .2).
    spacing, r = 14, 2
    row = 0
    y = spacing // 2
    while y < H:
        xoff = (spacing // 2) if row % 2 else 0
        x = spacing // 2 + xoff
        while x < W:
            d.ellipse([x - r, y - r, x + r, y + r], fill=DOT)
            x += spacing
        y += spacing
        row += 1

    # Hero right: height ~605px (96%), ~6% right margin, bottom-anchored (-8px bleed).
    maya = Image.open(SRC).convert("RGBA")
    target_h = 605
    if maya.height != target_h:
        maya = maya.resize((int(maya.width * target_h / maya.height), target_h), Image.LANCZOS)
    hx = W - maya.width - int(W * 0.06)
    hy = H - maya.height + 8
    shadow = Image.new("RGBA", maya.size, INK)
    shadow.putalpha(maya.split()[3])
    img.paste(shadow, (hx + 6, hy + 6), shadow)
    img.paste(maya, (hx, hy), maya)

    # Small tag top-left above title: white box, ink 3px border.
    f_tag = load_font(26)
    tag = "ISSUE #1 \u00b7 A FIVE-MINUTE JOB"
    tb = d.textbbox((0, 0), tag, font=f_tag)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y, sh = 14, 8, 4
    tag_w, tag_h = tw + pad_x * 2, th + pad_y * 2
    tag_layer = Image.new("RGBA", (tag_w + sh + 8, tag_h + sh + 8), (0, 0, 0, 0))
    td = ImageDraw.Draw(tag_layer)
    td.rectangle([sh, sh, sh + tag_w, sh + tag_h], fill=INK)
    td.rectangle([0, 0, tag_w, tag_h], fill=WHITE, outline=INK, width=3)
    td.text((pad_x - tb[0], pad_y - tb[1]), tag, font=f_tag, fill=INK)
    tag_layer = tag_layer.rotate(2, expand=True, resample=Image.BICUBIC)
    img.paste(tag_layer, (60, 36), tag_layer)

    # Title top-left: two yellow lines, ink stroke + drop shadow, rotated -3deg.
    lines = ["JUST MOVE", "THE BUTTON"]
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    size = 120
    max_w = hx - 60 - 30
    while size > 48:
        f_try = load_font(size)
        if max(probe.textlength(ln, font=f_try) for ln in lines) <= max_w:
            break
        size -= 4
    f_title = load_font(size)
    widths = [probe.textlength(ln, font=f_title) for ln in lines]
    bboxes = [probe.textbbox((0, 0), ln, font=f_title) for ln in lines]
    heights = [b[3] - b[1] for b in bboxes]
    lh = int(size * 0.9)
    tpad, tsh = 20, 6
    title_w = int(max(widths)) + tpad * 2 + tsh + 8
    title_h = lh * len(lines) + tpad * 2 + tsh + 8
    title_layer = Image.new("RGBA", (title_w, title_h), (0, 0, 0, 0))
    tld = ImageDraw.Draw(title_layer)
    for i, line in enumerate(lines):
        draw_outlined(tld, (tpad - bboxes[i][0], tpad - bboxes[i][1] + i * lh),
                      line, f_title, fill=YELLOW, outline=INK, sw=3, shadow=(6, 6))
    _ = heights
    title_layer = title_layer.rotate(-3, expand=True, resample=Image.BICUBIC)
    img.paste(title_layer, (56, 104), title_layer)

    # SFX bottom-left: yellow with ink outline, rotated -8deg, ~44px.
    f_sfx = load_font(44)
    sfx_lines = ["IT'S JUST", "ONE WORD!"]
    sb = [probe.textbbox((0, 0), ln, font=f_sfx) for ln in sfx_lines]
    sws = [b[2] - b[0] for b in sb]
    slh = int(44 * 0.95)
    spad, ssh = 16, 4
    sfx_w = int(max(sws)) + spad * 2 + ssh + 8
    sfx_h = slh * len(sfx_lines) + spad * 2 + ssh + 8
    sfx_layer = Image.new("RGBA", (sfx_w, sfx_h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sfx_layer)
    for i, line in enumerate(sfx_lines):
        draw_outlined(sd, (spad - sb[i][0], spad - sb[i][1] + i * slh),
                      line, f_sfx, fill=YELLOW, outline=INK, sw=2, shadow=(4, 4))
    sfx_layer = sfx_layer.rotate(-8, expand=True, resample=Image.BICUBIC)
    img.paste(sfx_layer, (60, H - sfx_layer.height - 50), sfx_layer)

    # Outer 4px ink frame.
    d = ImageDraw.Draw(img)
    d.rectangle([2, 2, W - 3, H - 3], outline=INK, width=4)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
