"""Render Hoshiyar Shield app icon / adaptive icon / splash PNGs (no external assets)."""
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[2] / "apps" / "mobile" / "assets"
NAVY, NAVY_DEEP = (11, 18, 32), (7, 12, 23)
EM, TEAL = (52, 211, 153), (20, 184, 166)


def gradient(size):
    g = Image.new("RGB", (size, size))
    px = g.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)
            px[x, y] = tuple(int(EM[i] * (1 - t) + TEAL[i] * t) for i in range(3))
    return g


def shield(size, scale=1.0, bg=None):
    """Shield mark on a transparent (or coloured) square canvas."""
    S = size * 4
    img = Image.new("RGBA", (S, S), bg + (255,) if bg else (0, 0, 0, 0))
    def P(pts):  # viewBox 0..64 mapped into centred square of `scale`
        off = S * (1 - scale) / 2
        return [(off + x / 64 * S * scale, off + y / 64 * S * scale) for x, y in pts]
    def bez(p0, p1, p2, p3, n=48):
        return [tuple((1 - t) ** 3 * p0[i] + 3 * (1 - t) ** 2 * t * p1[i] + 3 * (1 - t) * t ** 2 * p2[i] + t ** 3 * p3[i]
                      for i in range(2)) for t in (k / n for k in range(1, n + 1))]
    def shape(top, side_top, side_x, mid_y, c1, c2, bottom):
        # Mirrors the SVG path: M32 top L side_x side_top V mid_y C c1 c2 32 bottom (+ mirror)
        right = [(32, top), (side_x, side_top), (side_x, mid_y)] + bez((side_x, mid_y), c1, c2, (32, bottom))
        left = [(64 - x, y) for x, y in reversed(right[1:-1])]
        return right + left
    outer = shape(4, 12, 54, 30, (54, 44), (44.5, 54.5), 60)
    inner = shape(9.5, 15.8, 49, 30, (49, 41.2), (41.6, 49.6), 54.2)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).polygon(P(outer), fill=255)
    img.paste(gradient(S).convert("RGBA"), (0, 0), mask)
    ImageDraw.Draw(img).polygon(P(inner), fill=NAVY + (255,))
    d = ImageDraw.Draw(img)
    w = int(S * scale * 5 / 64)
    off = S * (1 - scale) / 2
    m = lambda x, y: (off + x / 64 * S * scale, off + y / 64 * S * scale)
    grad = gradient(S).convert("RGBA")
    hmask = Image.new("L", (S, S), 0)
    hd = ImageDraw.Draw(hmask)
    for a, b in (((24, 22), (24, 40)), ((40, 22), (40, 40)), ((24, 31), (40, 31))):
        hd.line([m(*a), m(*b)], fill=255, width=w)
        for p in (a, b):
            cx, cy = m(*p)
            hd.ellipse([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2], fill=255)
    img.paste(grad, (0, 0), hmask)
    return img.resize((size, size), Image.LANCZOS)


shield(1024, 0.78, NAVY).convert("RGB").save(OUT / "icon.png")
shield(1024, 0.56).save(OUT / "android-icon-foreground.png")
Image.new("RGB", (1024, 1024), NAVY).save(OUT / "android-icon-background.png")
mono = shield(1024, 0.56)
alpha = mono.split()[3]
Image.merge("RGBA", (alpha.point(lambda _: 255),) * 3 + (alpha,)).save(OUT / "android-icon-monochrome.png")
shield(512, 0.9).save(OUT / "splash-icon.png")
shield(48, 0.9, NAVY).convert("RGB").save(OUT / "favicon.png")
print("icons written to", OUT)
