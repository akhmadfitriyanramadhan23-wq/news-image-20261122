#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Sunday 22 November 2026.

A newspaper-style summary of the day's world news, drawn entirely with
Pillow vector shapes (no external images, no network). Writes entry.png
(1024x1024) next to this script.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 242, 230)
INK = (26, 24, 20)
RED = (158, 27, 27)
NAVY = (30, 58, 95)
SKY = (176, 205, 224)
GRAY = (110, 104, 92)
PALE = (233, 225, 206)
GOLD = (201, 148, 42)
GREEN = (46, 110, 72)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, f, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=f) <= max_width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_lines(draw, x, y, text, f, max_width, fill, leading=None, align="left"):
    """Draw wrapped text; return the y just below the last line."""
    if leading is None:
        leading = int(f.size * 1.18)
    for line in wrap_text(draw, text, f, max_width):
        if align == "center":
            lx = x + (max_width - draw.textlength(line, font=f)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=f, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def double_rule(draw, x0, y, x1):
    rule(draw, x0, y, x1, 3)
    rule(draw, x0, y + 5, x1, 1)


# ---------------------------------------------------------------- motifs

def star(draw, cx, cy, r, fill, points=5, inner=0.42):
    import math

    pts = []
    for i in range(points * 2):
        ang = -math.pi / 2 + i * math.pi / points
        rad = r if i % 2 == 0 else r * inner
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_flags_panel(draw, x, y, w, h):
    """Three flags on poles above a Shenzhen skyline."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 236, 242))
    # skyline silhouette along the bottom
    base = y + h
    skyline = [(0, 46), (34, 46), (34, 30), (52, 30), (52, 52), (86, 52),
               (86, 18), (104, 18), (104, 52), (138, 52), (138, 34),
               (160, 34), (160, 52), (196, 52), (196, 26), (214, 26),
               (214, 52), (250, 52), (250, 40), (272, 40), (272, 52),
               (306, 52), (306, 30), (330, 30), (330, 52), (364, 52),
               (364, 44), (396, 44)]
    for bx, bh in skyline:
        draw.rectangle([x + bx, base - bh, x + bx + 30, base], fill=NAVY)
    # tall tower with a spire
    draw.rectangle([x + 168, base - 108, x + 196, base], fill=NAVY)
    draw.polygon([(x + 182, base - 138), (x + 174, base - 108),
                  (x + 190, base - 108)], fill=NAVY)
    for wx in range(x + 8, x + w - 8, 14):
        for wy in range(base - 96, base - 8, 12):
            if (wx + wy) % 28 < 10:
                draw.rectangle([wx, wy, wx + 3, wy + 4], fill=GOLD)
    # flag poles
    pole_top = y + 8
    pole_bot = y + 118
    fw, fh = 104, 66
    positions = [x + 16, x + 140, x + 264]
    for px in positions:
        draw.line([(px, pole_top), (px, pole_bot)], fill=GRAY, width=3)
        draw.ellipse([px - 4, pole_top - 4, px + 4, pole_top + 4], fill=GOLD)
    # --- United States flag
    fx, fy = positions[0] + 4, pole_top + 4
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([fx, fy + i * fh // 13, fx + fw, fy + (i + 1) * fh // 13], fill=c)
    draw.rectangle([fx, fy, fx + 44, fy + fh * 7 // 13], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            draw.ellipse([fx + 6 + c * 8, fy + 5 + r * 7,
                          fx + 9 + c * 8, fy + 8 + r * 7], fill=(255, 255, 255))
    # --- China flag
    fx = positions[1] + 4
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
    star(draw, fx + 20, fy + 18, 12, (255, 222, 0))
    for sx, sy in [(fx + 44, fy + 10), (fx + 54, fy + 20), (fx + 50, fy + 34), (fx + 38, fy + 40)]:
        star(draw, sx, sy, 4, (255, 222, 0))
    # --- Russia flag
    fx = positions[2] + 4
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([fx, fy + i * fh // 3, fx + fw, fy + (i + 1) * fh // 3], fill=c)
    draw.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=1)


def draw_scales(draw, x, y, w, h):
    """Scales of justice, drawn with lines and arcs."""
    cx = x + w // 2
    top = y + 8
    beam_y = y + 34
    pan_y = y + h - 58
    # post and base
    draw.line([(cx, top), (cx, y + h - 22)], fill=INK, width=5)
    draw.ellipse([cx - 6, top - 6, cx + 6, top + 6], fill=INK)
    draw.polygon([(cx - 34, y + h - 22), (cx + 34, y + h - 22),
                  (cx + 24, y + h - 6), (cx - 24, y + h - 6)], fill=INK)
    # beam
    draw.line([(cx - 78, beam_y), (cx + 78, beam_y)], fill=INK, width=5)
    draw.ellipse([cx - 82, beam_y - 5, cx - 72, beam_y + 5], fill=INK)
    draw.ellipse([cx + 72, beam_y - 5, cx + 82, beam_y + 5], fill=INK)
    for side in (-1, 1):
        px = cx + side * 78
        draw.line([(px, beam_y), (px - 26, pan_y)], fill=INK, width=3)
        draw.line([(px, beam_y), (px + 26, pan_y)], fill=INK, width=3)
        draw.line([(px, beam_y), (px, pan_y)], fill=INK, width=3)
        draw.arc([px - 34, pan_y - 10, px + 34, pan_y + 26],
                 start=0, end=180, fill=INK, width=4)
        draw.line([(px - 34, pan_y + 8), (px + 34, pan_y + 8)], fill=INK, width=4)


def draw_bridge(draw, x, y, w, h):
    """The Kerch Bridge: an arched span over waves."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(58, 110, 158))
    for i in range(4):
        wx = x + 18 + i * 72
        draw.arc([wx, y + h - 20, wx + 56, y + h - 2],
                 start=180, end=360, fill=(255, 255, 255), width=3)
    # deck and arch
    draw.line([(x, y + 26), (x + w, y + 26)], fill=INK, width=4)
    draw.arc([x + 30, y - 6, x + w - 30, y + 62], start=180, end=360, fill=INK, width=4)
    for px in (x + 70, x + w // 2, x + w - 70):
        draw.line([(px, y + 26), (px, y + h - 14)], fill=INK, width=4)
    # a small blast burst over the deck
    star(draw, x + w // 2 + 40, y + 12, 9, GOLD)


def draw_tanker(draw, x, y, w, h):
    """An oil tanker on Gulf waves under a hot sun."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.ellipse([x + 10, y + 2, x + 38, y + 30], fill=GOLD)
    draw.rectangle([x + 30, y + h - 34, x + w - 30, y + h - 18], fill=(120, 30, 30))
    draw.polygon([(x + 30, y + h - 34), (x + 44, y + h - 34),
                  (x + 38, y + h - 18), (x + 30, y + h - 18)], fill=(120, 30, 30))
    draw.rectangle([x + w - 92, y + h - 52, x + w - 56, y + h - 34], fill=(240, 240, 240))
    draw.rectangle([x + w - 88, y + h - 60, x + w - 76, y + h - 52], fill=INK)
    for i in range(3):
        wx = x + 10 + i * 92
        draw.arc([wx, y + h - 14, wx + 60, y + h + 2],
                 start=180, end=360, fill=NAVY, width=3)


def draw_quake(draw, x, y, w, h):
    """Andean peaks split by a crack."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.polygon([(x, y + h), (x + 90, y + 6), (x + 180, y + h)], fill=(96, 96, 100))
    draw.polygon([(x + 150, y + h), (x + 250, y + 2), (x + w, y + h)], fill=(70, 74, 82))
    draw.polygon([(x + 90, y + 6), (x + 72, y + 26), (x + 90, y + 34),
                  (x + 108, y + 26)], fill=(255, 255, 255))
    draw.polygon([(x + 250, y + 2), (x + 232, y + 22), (x + 250, y + 30),
                  (x + 268, y + 22)], fill=(255, 255, 255))
    # crack zig-zag down the middle peak
    pts = [(x + 150, y + 18), (x + 142, y + 30), (x + 152, y + 42),
           (x + 140, y + 54), (x + 148, y + 66)]
    draw.line(pts, fill=RED, width=3)
    for rx, ry in [(x + 60, y + h - 12), (x + 200, y + h - 8), (x + 280, y + h - 14)]:
        draw.polygon([(rx, ry), (rx + 8, ry - 6), (rx + 16, ry)], fill=(60, 60, 64))


def draw_climate(draw, x, y, w, h):
    """A globe beside a factory chimney."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy, r = x + 62, y + h // 2 + 2, 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 110, 158))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=300, end=60, fill=GREEN, width=3)
    draw.ellipse([cx - 14, cy - 18, cx + 4, cy + 2], fill=GREEN)
    draw.ellipse([cx - 2, cy + 8, cx + 16, cy + 24], fill=GREEN)
    # factory
    fx = x + 130
    draw.rectangle([fx, y + h - 26, fx + 130, y + h], fill=INK)
    draw.rectangle([fx + 96, y + 8, fx + 112, y + h - 26], fill=INK)
    for sx, sy, sr in [(fx + 104, y + 2, 6), (fx + 116, y - 4, 8), (fx + 100, y - 10, 5)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GRAY)
    draw.rectangle([fx + 10, y + h - 18, fx + 26, y + h - 6], fill=GOLD)
    draw.rectangle([fx + 36, y + h - 18, fx + 52, y + h - 6], fill=GOLD)


def draw_handcuffs(draw, x, y, w, h):
    """Handcuffs: two linked rings."""
    draw.rectangle([x, y, x + w, y + h], fill=PALE)
    cy = y + h // 2
    for cx in (x + 78, x + w - 78):
        draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=INK, width=7)
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=INK, width=4)
    draw.line([(x + 78, cy - 8), (x + w - 78, cy - 8)], fill=INK, width=5)
    draw.line([(x + 78, cy + 8), (x + w - 78, cy + 8)], fill=INK, width=5)
    draw.rectangle([x + w // 2 - 10, cy - 14, x + w // 2 + 10, cy + 14], fill=INK)


def draw_border(draw, x, y, w, h):
    """A closed border barrier, red and white stripes."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h - 12, x + w, y + h], fill=(96, 110, 82))
    for px in (x + 24, x + w - 24):
        draw.rectangle([px - 5, y + 12, px + 5, y + h - 12], fill=INK)
    bar_y = y + 16
    seg = (w - 48) // 8
    for i in range(8):
        c = RED if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x + 24 + i * seg, bar_y, x + 24 + (i + 1) * seg, bar_y + 12], fill=c)
    draw.rectangle([x + 24, bar_y, x + w - 24, bar_y + 12], outline=INK, width=2)
    # small round sign on the barrier
    sx = x + w // 2
    draw.ellipse([sx - 16, bar_y + 16, sx + 16, bar_y + 48], fill=(255, 255, 255), outline=RED, width=3)
    draw.line([(sx - 9, bar_y + 25), (sx + 9, bar_y + 39)], fill=RED, width=3)
    draw.line([(sx - 9, bar_y + 39), (sx + 9, bar_y + 25)], fill=RED, width=3)


# ---------------------------------------------------------------- page

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 30                      # side margin
    RX = W - MX                  # right edge

    # ---- masthead
    rule(d, MX, 22, RX, 3)
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 68)
    d.text(((W - d.textlength(title, font=tf)) / 2, 30), title, font=tf, fill=INK)
    date_line = "SUNDAY  22  NOVEMBER  2026"
    df = font(SANS_B, 27)
    d.text(((W - d.textlength(date_line, font=df)) / 2, 112), date_line, font=df, fill=RED)
    sub = "THE WORLD'S NEWS IN ONE PAGE  •  SUNDAY EDITION"
    sf = font(SANS, 16)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 146), sub, font=sf, fill=GRAY)
    double_rule(d, MX, 172, RX)

    # ---- lead story: APEC peace pact
    y = 190
    kf = font(SANS_B, 19)
    d.text((MX, y), "APEC SUMMIT  •  SHENZHEN, CHINA", font=kf, fill=RED)
    y += 30
    hf = font(SERIF_B, 40)
    y = draw_lines(d, MX, y, "TRUMP, XI AND PUTIN\nSIGN PEACE PACT\nIN SHENZHEN",
                   hf, 570, INK, leading=47)
    y += 8
    bf = font(SERIF, 19)
    y = draw_lines(d, MX, y, "The three leaders sign a four-point declaration "
                   "as the summit closes — a deal that says nothing about Ukraine.",
                   bf, 570, INK, leading=24)
    draw_flags_panel(d, 610, 196, 384, 218)

    rule(d, MX, 448, RX, 2)

    # ---- second lead: World Court ruling
    y = 466
    d.text((MX, y), "THE HAGUE  •  WORLD COURT", font=kf, fill=RED)
    draw_scales(d, 30, 492, 210, 150)
    hf2 = font(SERIF_B, 34)
    tx = 268
    yy = draw_lines(d, tx, y + 30, "MYANMAR GUILTY OF GENOCIDE\nAGAINST THE ROHINGYA",
                    hf2, RX - tx, INK, leading=40)
    yy += 6
    draw_lines(d, tx, yy, "The first time any international court has found a state\nguilty of genocide — a landmark ruling for the Rohingya.",
               bf, RX - tx, INK, leading=26)

    rule(d, MX, 656, RX, 2)

    # ---- grid of six stories
    stories = [
        ("UKRAINE", "UKRAINE STRIKES KERCH BRIDGE",
         "A third attack in four days on the link to Crimea. Zelensky calls it a fair response.",
         draw_bridge),
        ("THE GULF", "IRAN STRIKES U.S. BASE IN KUWAIT",
         "Tehran targets Bahrain too as tensions soar; tankers are hit off Oman.",
         draw_tanker),
        ("PERU", "6.9 QUAKE SHAKES PERU'S ANDES",
         "A powerful tremor rattles the highlands; rescuers reach remote villages.",
         draw_quake),
        ("CLIMATE", "COP31 DEADLOCKED ON FOSSIL FUELS",
         "Climate talks stall as nations split over phasing out oil and gas.",
         draw_climate),
        ("MEXICO", "MEXICO ARRESTS 'EL CHAPO ISIDRO'",
         "The cartel leader is seized as deadly violence grips Sinaloa.",
         draw_handcuffs),
        ("ESTONIA", "ESTONIA TO CLOSE BORDER WITH RUSSIA",
         "Tallinn shuts the crossings, citing security threats from Moscow.",
         draw_border),
    ]
    col_w = 306
    col_x = [MX, MX + col_w + 16, MX + 2 * (col_w + 16)]
    row_y = [672, 842]
    cell_h = 158
    for i, (kicker, head, summ, motif) in enumerate(stories):
        cx = col_x[i % 3]
        cy = row_y[i // 3]
        motif(d, cx, cy, col_w, 46)
        yy = cy + 54
        d.text((cx, yy), kicker, font=font(SANS_B, 15), fill=RED)
        yy += 20
        yy = draw_lines(d, cx, yy, head, font(SERIF_B, 21), col_w, INK, leading=24)
        yy += 3
        draw_lines(d, cx, yy, summ, font(SANS, 15), col_w, (60, 56, 48), leading=18)

    for gx in (MX + col_w + 8, MX + 2 * col_w + 24):
        d.line([(gx, 672), (gx, 1000)], fill=PALE, width=2)
    rule(d, MX, 834, RX, 1, fill=PALE)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
