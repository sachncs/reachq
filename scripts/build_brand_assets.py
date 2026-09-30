"""Generate reachq brand assets (PNG) from the SVG descriptions.

Produces:
  - docs/assets/favicon-16.png   (16x16)
  - docs/assets/favicon-32.png   (32x32)
  - docs/assets/favicon.png      (32x32, legacy alias)
  - docs/assets/logo-256.png     (256x256)
  - docs/assets/social-preview.png (1280x640)

Pure-Pillow drawing, no SVG rendering dependency.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSET_DIR = Path(__file__).resolve().parents[1] / "docs" / "assets"

INDIGO = (13, 19, 28)
TEAL = (30, 43, 55)
LIME = (184, 255, 61)
WHITE = (242, 238, 229)
SOFT = (255, 255, 255, 44)
INK = (13, 19, 28)


def gradient(size: tuple[int, int], c1: tuple[int, int, int], c2: tuple[int, int, int]) -> Image.Image:
    """Render a diagonal bilinear gradient as RGB."""
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    denom = max(1, w + h - 2)
    for y in range(h):
        for x in range(w):
            t = (x + y) / denom
            r = round(c1[0] * (1 - t) + c2[0] * t)
            g = round(c1[1] * (1 - t) + c2[1] * t)
            b = round(c1[2] * (1 - t) + c2[2] * t)
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
    """Build the q-loop app icon at the requested pixel size."""
    bg = gradient((size, size), INDIGO, TEAL)
    mask = rounded_rect_mask((size, size), int(size * radius_ratio))
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(bg, (0, 0), mask)
    draw = ImageDraw.Draw(out)
    s = size / 160.0
    sw = max(1, int(10 * s))
    box = (int(29 * s), int(28 * s), int(143 * s), int(143 * s))
    for start, end in ((205, 315), (325, 80), (92, 170)):
        draw.arc(box, start, end, fill=WHITE, width=sw)
    for x, y, color, radius in ((47, 48, LIME, 13), (30, 99, WHITE, 12), (84, 139, WHITE, 12)):
        r = int(radius * s)
        draw.ellipse((int((x * s) - r), int((y * s) - r), int((x * s) + r), int((y * s) + r)), fill=color)
    points = [(68, 111), (83, 101), (73, 83), (93, 71)]
    draw.line([(int(x * s), int(y * s)) for x, y in points], fill=LIME, width=max(1, int(9 * s)), joint="curve")
    arrow = [(int(x * s), int(y * s)) for x, y in ((88, 67), (107, 68), (95, 83))]
    draw.polygon(arrow, fill=LIME)
    draw.line([(int(111 * s), int(121 * s)), (int(133 * s), int(145 * s))], fill=WHITE, width=sw)
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
    build_icon(16).save(ASSET_DIR / "favicon-16.png")
    build_icon(32).save(ASSET_DIR / "favicon-32.png")
    build_icon(32).save(ASSET_DIR / "favicon.png")
    build_icon(64).save(ASSET_DIR / "favicon-64.png")
    build_icon(256).save(ASSET_DIR / "logo-256.png")
    build_social_preview().save(ASSET_DIR / "social-preview.png")
    print(f"wrote brand assets to {ASSET_DIR}")


if __name__ == "__main__":
    main()
