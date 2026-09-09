"""Generate reachq brand assets (PNG) from the SVG descriptions.

Produces:
  - docs/assets/favicon.png      (32x32)
  - docs/assets/logo-256.png     (256x256)
  - docs/assets/social-preview.png (1280x640)

Pure-Pillow drawing, no SVG rendering dependency.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSET_DIR = Path(__file__).resolve().parents[1] / "docs" / "assets"

INDIGO = (79, 70, 229)
TEAL = (20, 184, 166)
WHITE = (255, 255, 255)
SOFT = (255, 255, 255, 82)
INK = (24, 24, 27)


def gradient(size: tuple[int, int], c1: tuple[int, int, int], c2: tuple[int, int, int]) -> Image.Image:
    """Render a diagonal bilinear gradient as RGB."""
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    denom = max(1, w + h - 2)
    for y in range(h):
        for x in range(w):
            t = (x + y) / denom
            r = int(round(c1[0] * (1 - t) + c2[0] * t))
            g = int(round(c1[1] * (1 - t) + c2[1] * t))
            b = int(round(c1[2] * (1 - t) + c2[2] * t))
            px[x, y] = (r, g, b)
    return img


def rounded_rect_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def draw_q(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    r_ring: int,
    ring_w: int,
    tail: tuple[tuple[int, int], tuple[int, int]],
    tail_w: int,
    inner_dot_r: int,
) -> None:
    draw.ellipse(
        (cx - r_ring, cy - r_ring, cx + r_ring, cy + r_ring),
        outline=WHITE,
        width=ring_w,
    )
    draw.line([tail[0], tail[1]], fill=WHITE, width=tail_w, joint="curve")
    draw.ellipse(
        (cx - inner_dot_r, cy - inner_dot_r, cx + inner_dot_r, cy + inner_dot_r),
        fill=WHITE,
    )


def draw_network(
    draw: ImageDraw.ImageDraw,
    nodes: list[tuple[int, int]],
    edges: list[tuple[int, int, int, int]],
    node_r: int,
    edge_w: int,
) -> None:
    for x1, y1, x2, y2 in edges:
        draw.line([(x1, y1), (x2, y2)], fill=SOFT, width=edge_w)
    for x, y in nodes:
        draw.ellipse((x - node_r, y - node_r, x + node_r, y + node_r), fill=WHITE)


def build_icon(size: int, radius_ratio: float = 0.22) -> Image.Image:
    """Build a square app icon of the given pixel size."""
    bg = gradient((size, size), INDIGO, TEAL)
    mask = rounded_rect_mask((size, size), int(size * radius_ratio))
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(bg, (0, 0), mask)
    draw = ImageDraw.Draw(out)
    s = size / 256.0
    cx, cy = int(138 * s), int(128 * s)
    r_ring = int(56 * s)
    ring_w = max(2, int(14 * s))
    tail_w = max(2, int(14 * s))
    inner_r = max(1, int(9 * s))
    tail = ((int(166 * s), int(156 * s)), (int(198 * s), int(188 * s)))
    draw_q(draw, cx, cy, r_ring, ring_w, tail, tail_w, inner_r)
    nodes = [
        (int(56 * s), int(80 * s)),
        (int(200 * s), int(120 * s)),
        (int(128 * s), int(160 * s)),
        (int(200 * s), int(200 * s)),
    ]
    edges = [
        (56, 80, 128, 80),
        (128, 80, 200, 120),
        (56, 80, 200, 120),
        (56, 80, 128, 160),
        (200, 120, 128, 160),
        (128, 160, 200, 200),
        (56, 80, 200, 200),
    ]
    edges = [(int(x1 * s), int(y1 * s), int(x2 * s), int(y2 * s)) for x1, y1, x2, y2 in edges]
    draw_network(draw, nodes, edges, node_r=max(1, int(6 * s)), edge_w=max(1, int(3 * s)))
    return out


def build_social_preview() -> Image.Image:
    """Build a 1280x640 social preview banner."""
    W, H = 1280, 640
    img = gradient((W, H), INDIGO, TEAL)
    draw = ImageDraw.Draw(img, "RGBA")

    for i, off in enumerate(range(0, W + H, 32)):
        x1, y1 = off, 0
        x2, y2 = 0, off
        if x1 > W:
            x1, y1 = W, off - W
        if y2 > H:
            x2, y2 = off - H, H
        draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 18), width=1)

    nodes = [
        (140, 160),
        (340, 220),
        (240, 360),
        (440, 460),
        (560, 320),
        (700, 200),
        (820, 380),
        (980, 280),
        (1120, 420),
    ]
    edges = [
        (0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (1, 5),
        (4, 5), (4, 6), (5, 7), (6, 7), (7, 8), (3, 6),
    ]
    for a, b in edges:
        draw.line([nodes[a], nodes[b]], fill=(255, 255, 255, 64), width=2)
    for x, y in nodes:
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=WHITE)

    draw.ellipse((900, 220, 1080, 400), outline=WHITE, width=14)
    draw.line([(1020, 340), (1100, 420)], fill=WHITE, width=14)
    draw.ellipse((974, 294, 1006, 326), fill=WHITE)

    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    font_big = font_med = font_sm = None
    for path in candidates:
        if not Path(path).exists():
            continue
        try:
            font_big = ImageFont.truetype(path, 140)
            font_med = ImageFont.truetype(path, 56)
            font_sm = ImageFont.truetype(path, 28)
        except OSError:
            continue
        if font_big is not None:
            break
    if font_big is None:
        font_big = ImageFont.load_default()
        font_med = ImageFont.load_default()
        font_sm = ImageFont.load_default()

    draw.text((70, 110), "reachq", font=font_big, fill=WHITE)
    draw.text((70, 280), "Graph reachability, queryable.", font=font_med, fill=(255, 255, 255, 235))
    draw.text(
        (70, 360),
        "Parallel shortcut sets and hopsets for reachability",
        font=font_med,
        fill=(255, 255, 255, 200),
    )
    draw.text(
        (70, 425),
        "and shortest paths in dense digraphs.",
        font=font_med,
        fill=(255, 255, 255, 200),
    )
    draw.text(
        (70, 540),
        "github.com/sachncs/reachq  ·  pip install reachq",
        font=font_sm,
        fill=(255, 255, 255, 220),
    )

    return img


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    build_icon(32).save(ASSET_DIR / "favicon.png")
    build_icon(64).save(ASSET_DIR / "favicon-64.png")
    build_icon(256).save(ASSET_DIR / "logo-256.png")
    build_social_preview().save(ASSET_DIR / "social-preview.png")
    print(f"wrote brand assets to {ASSET_DIR}")


if __name__ == "__main__":
    main()