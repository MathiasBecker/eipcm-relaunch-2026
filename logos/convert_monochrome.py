"""
Convert all logos to monochrome versions for dark background banner.
- SVGs: Replace all fill/stroke colors with #E5E5E5 (light gray)
- PNGs/JPGs: Convert to monochrome light gray on transparent background
Output: logos/monochrome/ folder with uniform-height PNGs (60px tall)
"""

import os
import re
import subprocess
from PIL import Image, ImageOps

SRC_DIR = r"D:\04 work\Claude Code\logos"
OUT_DIR = os.path.join(SRC_DIR, "monochrome")
TARGET_COLOR = "#E5E5E5"
TARGET_HEIGHT = 60  # px for final PNG export

os.makedirs(OUT_DIR, exist_ok=True)


def process_svg_to_monochrome(src_path, out_name):
    """Replace all colors in SVG with monochrome, then export to PNG."""
    with open(src_path, "r", encoding="utf-8", errors="replace") as f:
        svg_content = f.read()

    # Replace fill colors (hex, rgb, named colors) with target color
    # But preserve fill="none" and stroke="none"
    def replace_color(match):
        full = match.group(0)
        attr = match.group(1)  # fill or stroke
        value = match.group(2)
        if value.lower() in ("none", "transparent"):
            return full
        return f'{attr}="{TARGET_COLOR}"'

    # Replace fill="..." and stroke="..." attributes
    svg_mono = re.sub(
        r'(fill|stroke)="([^"]*)"',
        replace_color,
        svg_content
    )

    # Replace fill: and stroke: in style attributes and style tags
    def replace_style_color(match):
        prop = match.group(1)
        value = match.group(2).strip()
        if value.lower() in ("none", "transparent"):
            return match.group(0)
        return f"{prop}:{TARGET_COLOR}"

    svg_mono = re.sub(
        r'(fill|stroke)\s*:\s*([^;}"]+)',
        replace_style_color,
        svg_mono
    )

    # Save monochrome SVG
    mono_svg_path = os.path.join(OUT_DIR, out_name + ".svg")
    with open(mono_svg_path, "w", encoding="utf-8") as f:
        f.write(svg_mono)

    # Export to PNG with Inkscape at target height
    mono_png_path = os.path.join(OUT_DIR, out_name + ".png")
    try:
        subprocess.run([
            "inkscape", mono_svg_path,
            "--export-type=png",
            f"--export-filename={mono_png_path}",
            f"--export-height={TARGET_HEIGHT}",
            "--export-background-opacity=0"
        ], capture_output=True, timeout=30)
        if os.path.exists(mono_png_path):
            print(f"  OK SVG->PNG: {out_name}.png")
        else:
            print(f"  WARN: PNG export failed for {out_name}")
    except Exception as e:
        print(f"  ERROR exporting {out_name}: {e}")

    return mono_svg_path


def process_raster_to_monochrome(src_path, out_name):
    """Convert PNG/JPG to monochrome light gray on transparent background."""
    img = Image.open(src_path)

    # Convert to RGBA if not already
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Convert to grayscale to get luminance
    gray = img.convert("L")

    # Create new image: where original has content (not transparent),
    # make it the target color with opacity based on darkness
    r, g, b, a = img.split()
    gray_data = gray.load()
    new_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pixels = new_img.load()

    # Target color RGB
    tr, tg, tb = 0xE5, 0xE5, 0xE5

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            orig_a = a.getpixel((x, y))
            if orig_a > 10:  # Has content
                # Use inverse of luminance as alpha (darker = more opaque)
                lum = gray_data[x, y]
                # Invert: dark pixels become opaque, light pixels transparent
                new_alpha = int((255 - lum) * (orig_a / 255))
                if new_alpha > 10:
                    pixels[x, y] = (tr, tg, tb, min(255, new_alpha))

    # Resize to target height maintaining aspect ratio
    ratio = TARGET_HEIGHT / new_img.size[1]
    new_width = int(new_img.size[0] * ratio)
    new_img = new_img.resize((new_width, TARGET_HEIGHT), Image.LANCZOS)

    mono_png_path = os.path.join(OUT_DIR, out_name + ".png")
    new_img.save(mono_png_path, "PNG")
    print(f"  OK Raster: {out_name}.png ({new_width}x{TARGET_HEIGHT})")


# Process all logos
files = sorted(os.listdir(SRC_DIR))
for fname in files:
    fpath = os.path.join(SRC_DIR, fname)
    if not os.path.isfile(fpath):
        continue
    if fname.startswith("convert_") or fname.startswith("."):
        continue

    name, ext = os.path.splitext(fname)
    ext = ext.lower()

    print(f"Processing: {fname}")

    if ext == ".svg":
        process_svg_to_monochrome(fpath, name)
    elif ext in (".png", ".jpg", ".jpeg"):
        process_raster_to_monochrome(fpath, name)
    else:
        print(f"  SKIP: unsupported format {ext}")

print(f"\nDone! Monochrome logos in: {OUT_DIR}")
