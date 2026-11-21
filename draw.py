#!/usr/bin/env python3
"""
Draw the news infographic for 21 November 2026.
Renders to entry.png at 1024x1024.
Polished: tighter spacing, gradient masthead, cleaner card dividers.
"""
from PIL import Image, ImageDraw, ImageFont
import json
import os

# Canvas
W, H = 1024, 1024
BG_COLOR = (18, 22, 30)
CARD_BG = (28, 34, 46)
ACCENT = (255, 185, 60)
WHITE = (240, 240, 240)
MUTED = (150, 155, 170)
REGION_COLORS = {
    "Asia": (60, 180, 255),
    "Europe": (100, 220, 100),
    "Middle East": (255, 120, 60),
    "US": (255, 80, 80),
    "Global": (180, 140, 255),
    "Sport": (255, 200, 50),
    "Science-Tech": (80, 220, 220),
    "Economy": (255, 160, 60),
}

def load_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_symbol(draw, cx, cy, size, symbol_type, color=ACCENT):
    s = size // 2
    if symbol_type == "globe":
        draw.ellipse([cx-s, cy-s, cx+s, cy+s], outline=color, width=2)
        draw.line([cx, cy-s, cx, cy+s], fill=color, width=2)
        draw.line([cx-s, cy, cx+s, cy], fill=color, width=2)
        draw.line([cx-s, cy-s, cx+s, cy+s], fill=color, width=1)
    elif symbol_type == "missile":
        pts = [(cx, cy-s), (cx-8, cy+6), (cx-4, cy+6), (cx-4, cy+s), (cx+4, cy+s), (cx+4, cy+6), (cx+8, cy+6)]
        draw.polygon(pts, fill=color)
        draw.polygon([(cx-3, cy+s), (cx, cy+s+8), (cx+3, cy+s)], fill=(255, 100, 40))
    elif symbol_type == "scales":
        draw.line([cx-s, cy-4, cx+s, cy-4], fill=color, width=2)
        draw.line([cx, cy-4, cx, cy-s], fill=color, width=2)
        draw.ellipse([cx-s-6, cy+6, cx-s+6, cy+18], outline=color, width=2)
        draw.line([cx-s, cy-4, cx-s, cy+6], fill=color, width=2)
        draw.ellipse([cx+s-6, cy+6, cx+s+6, cy+18], outline=color, width=2)
        draw.line([cx+s, cy-4, cx+s, cy+6], fill=color, width=2)
    elif symbol_type == "chart":
        pts = [(cx-s, cy+s), (cx-s//2, cy), (cx, cy-s//2), (cx+s//2, cy-s), (cx+s, cy-s-4)]
        for i in range(len(pts)-1):
            draw.line([pts[i], pts[i+1]], fill=color, width=3)
        for x in range(cx-s, cx+s, 8):
            h = (x - (cx-s)) * 2
            draw.line([x, cy+s, x, cy+s-h], fill=color, width=4)
    elif symbol_type == "handshake":
        draw.ellipse([cx-16, cy-4, cx-4, cy+16], outline=color, width=2)
        draw.ellipse([cx+4, cy-4, cx+16, cy+16], outline=color, width=2)
        draw.line([cx-4, cy+4, cx+4, cy+4], fill=color, width=3)
    elif symbol_type == "flag":
        draw.line([cx, cy-s, cx, cy+s], fill=color, width=3)
        draw.polygon([(cx, cy-s), (cx+16, cy-s+6), (cx, cy-s+12)], fill=color)
    elif symbol_type == "tennis":
        draw.ellipse([cx-8, cy-8, cx+8, cy+8], outline=color, width=2)
        draw.line([cx, cy+8, cx, cy+18], fill=color, width=2)
        draw.ellipse([cx-6, cy-12, cx+6, cy-2], outline=color, width=2)
    elif symbol_type == "satellite":
        draw.ellipse([cx-8, cy-8, cx+8, cy+8], outline=color, width=2)
        for i in range(8):
            angle = i * 3.14159 / 4
            x1 = cx + int(10 * (angle % 1))
            y1 = cy + int(10 * (angle % 1))
            x2 = cx + int(18 * (angle % 1))
            y2 = cy + int(18 * (angle % 1))
            draw.line([x1, y1, x2, y2], fill=color, width=2)
    elif symbol_type == "ship":
        draw.line([cx-14, cy+6, cx+14, cy+6], fill=color, width=3)
        draw.line([cx-10, cy+6, cx-8, cy-4], fill=color, width=2)
        draw.line([cx-8, cy-4, cx+8, cy-4], fill=color, width=2)
        draw.line([cx+8, cy-4, cx+10, cy+6], fill=color, width=2)
    elif symbol_type == "document":
        draw.rectangle([cx-10, cy-12, cx+10, cy+12], outline=color, width=2)
        draw.line([cx-4, cy, cx-1, cy+3], fill=color, width=2)
        draw.line([cx-1, cy+3, cx+5, cy-4], fill=color, width=2)

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = []
    for w in words:
        test = ' '.join(current + [w])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(w)
        else:
            if current:
                lines.append(' '.join(current))
            current = [w]
    if current:
        lines.append(' '.join(current))
    return lines

def draw_card(draw, fonts, x, y, w, h, story, card_idx):
    # Card background with subtle top accent line
    draw_rounded_rect(draw, [x, y, x+w, y+h], 12, CARD_BG, outline=(55, 65, 85), width=1)
    # Thin top accent bar inside card
    draw.line([x+12, y+1, x+w-12, y+1], fill=ACCENT, width=1)
    
    # Region tag at top-left
    region = story.get('region', 'Global')
    first_region = region.split(' / ')[0].split('/')[0].strip()
    tag_color = REGION_COLORS.get(first_region, (180, 140, 255))
    
    tag_text = first_region
    tag_font = fonts['small']
    tag_padding = 6
    tb = draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_w = tb[2] - tb[0] + tag_padding * 2
    tag_h = tb[3] - tb[1] + tag_padding
    tag_x = x + 10
    tag_y = y + 8
    draw_rounded_rect(draw, [tag_x, tag_y, tag_x+tag_w, tag_y+tag_h], 4, tag_color)
    draw.text((tag_x + tag_padding, tag_y + 1), tag_text, font=tag_font, fill=(10, 10, 10))
    
    # Symbol/icon - top right
    symbol_map = {
        0: "scales", 1: "missile", 2: "handshake", 3: "missile",
        4: "chart", 5: "flag", 6: "ship", 7: "handshake",
        8: "tennis", 9: "satellite",
    }
    sym = symbol_map.get(card_idx, "globe")
    draw_symbol(draw, x + w - 38, y + 36, 32, sym, ACCENT)
    
    # Headline
    headline = story['headline']
    if len(headline) > 60:
        headline = headline[:57] + "..."
    h_lines = wrap_text(draw, headline, fonts['headline'], w - 28)
    hy = y + 42
    for line in h_lines[:2]:
        draw.text((x + 12, hy), line, font=fonts['headline'], fill=WHITE)
        hy += 24
    
    # Summary fact
    summary = story['summary_1line']
    s_lines = wrap_text(draw, summary, fonts['body'], w - 28)
    sy = hy + 6
    for line in s_lines[:3]:
        draw.text((x + 12, sy), line, font=fonts['body'], fill=MUTED)
        sy += 20

def make_gradient_background(w, h, top_color, bottom_color):
    """Create a vertical gradient image."""
    grad = Image.new('RGB', (w, h))
    for y in range(h):
        t = y / h
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        for x in range(w):
            grad.putpixel((x, y), (r, g, b))
    return grad

def main():
    with open('data-news.json') as f:
        stories = json.load(f)
    
    img = Image.new('RGB', (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    fonts = {
        'title': load_font(44, bold=True),
        'subtitle': load_font(18),
        'headline': load_font(17, bold=True),
        'body': load_font(13),
        'small': load_font(11, bold=True),
    }
    
    # ====== MASTHEAD with subtle gradient ======
    masthead_h = 120
    # Draw gradient background for masthead
    grad = make_gradient_background(W, masthead_h, (22, 28, 38), (12, 16, 24))
    img.paste(grad, (0, 0))
    
    # Accent line at bottom of masthead
    draw.line([0, masthead_h, W, masthead_h], fill=ACCENT, width=2)
    
    # Title
    title = "Saturday 21 November 2026"
    tb = draw.textbbox((0, 0), title, font=fonts['title'])
    tx = (W - (tb[2] - tb[0])) // 2
    draw.text((tx, 20), title, font=fonts['title'], fill=WHITE)
    
    # Subtitle
    sub = "— The World in One Day —"
    sb = draw.textbbox((0, 0), sub, font=fonts['subtitle'])
    sx = (W - (sb[2] - sb[0])) // 2
    draw.text((sx, 72), sub, font=fonts['subtitle'], fill=ACCENT)
    
    # ====== CARDS GRID ======
    start_y = masthead_h + 16
    card_w = 484
    card_h = 168
    gap_x = 32
    gap_y = 14
    margin_x = 22
    
    cols = 2
    rows = 5
    
    for idx, story in enumerate(stories[:10]):
        col = idx % cols
        row = idx // cols
        x = margin_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        draw_card(draw, fonts, x, y, card_w, card_h, story, idx)
    
    # Save
    img.save('entry.png', 'PNG', optimize=True)
    print(f"Saved entry.png ({W}x{H})")
    
    size = os.path.getsize('entry.png')
    print(f"File size: {size} bytes ({size/1024:.1f} KB)")
    if size > 1048576:
        print("WARNING: Over 1 MiB limit!")

if __name__ == '__main__':
    main()
