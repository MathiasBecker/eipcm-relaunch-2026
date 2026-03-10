"""
Create dark monochrome versions of logos for light backgrounds.
Takes the monochrome SVGs/PNGs (light #E5E5E5) and converts to dark #333333.
"""

import os
import re
import subprocess
from PIL import Image

SRC_SVG_DIR = os.path.join(r"D:\04 work\Claude Code\logos", "monochrome")
SRC_ORIG_DIR = r"D:\04 work\Claude Code\logos"
OUT_DIR = os.path.join(SRC_ORIG_DIR, "monochrome-dark")
LIGHT_COLOR = "#E5E5E5"
DARK_COLOR = "#333333"
TARGET_HEIGHT = 60

os.makedirs(OUT_DIR, exist_ok=True)


def process_svg(src_path, out_name):
    """Replace #E5E5E5 with #333333 in monochrome SVG, export PNG."""
    with open(src_path, "r", encoding="utf-8", errors="replace") as f:
        svg = f.read()

    svg_dark = svg.replace(LIGHT_COLOR, DARK_COLOR)
    svg_dark = svg_dark.replace(LIGHT_COLOR.lower(), DARK_COLOR)

    dark_svg_path = os.path.join(OUT_DIR, out_name + ".svg")
    with open(dark_svg_path, "w", encoding="utf-8") as f:
        f.write(svg_dark)

    dark_png_path = os.path.join(OUT_DIR, out_name + ".png")
    try:
        subprocess.run([
            "inkscape", dark_svg_path,
            "--export-type=png",
            f"--export-filename={dark_png_path}",
            f"--export-height={TARGET_HEIGHT}",
            "--export-background-opacity=0"
        ], capture_output=True, timeout=30)
        if os.path.exists(dark_png_path) and os.path.getsize(dark_png_path) > 100:
            print(f"  OK SVG: {out_name}.png")
            return True
    except Exception as e:
        print(f"  ERROR: {e}")
    return False


def process_png(src_path, out_name):
    """Recolor light monochrome PNG to dark."""
    img = Image.open(src_path).convert("RGBA")
    pixels = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = pixels[x, y]
            if a > 10:
                pixels[x, y] = (0x33, 0x33, 0x33, a)

    dark_png_path = os.path.join(OUT_DIR, out_name + ".png")
    img.save(dark_png_path, "PNG")
    print(f"  OK PNG: {out_name}.png")


# Process each logo
mono_files = sorted(os.listdir(SRC_SVG_DIR))
svg_names = {os.path.splitext(f)[0] for f in mono_files if f.endswith(".svg")}
png_names = {os.path.splitext(f)[0] for f in mono_files if f.endswith(".png")}

for name in sorted(svg_names | png_names):
    print(f"Processing: {name}")
    svg_path = os.path.join(SRC_SVG_DIR, name + ".svg")
    png_path = os.path.join(SRC_SVG_DIR, name + ".png")

    if os.path.exists(svg_path):
        ok = process_svg(svg_path, name)
        if not ok and os.path.exists(png_path):
            process_png(png_path, name)
    elif os.path.exists(png_path):
        process_png(png_path, name)

print(f"\nDone! Dark monochrome logos in: {OUT_DIR}")
