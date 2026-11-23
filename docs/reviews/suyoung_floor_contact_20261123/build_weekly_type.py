"""Rebuild the optional offline graphic's lettering with Pillow and Bitstream Vera."""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


LABELS = {
    "title": (48, True, "Bottom pressure during early loading"),
    "before": (33, True, "Before floor change"),
    "after": (33, True, "After floor change"),
    "coarse": (25, False, "8 cells per diameter"),
    "fine": (25, False, "16 cells per diameter"),
    "x": (27, False, "Platen displacement (disk diameters)"),
    "y": (27, False, "Bottom pressure (MPa)"),
    "zero": (24, False, "Both grids recorded 0 MPa throughout this interval."),
    "note": (23, False, "Native samples through step 270 (8 cells) and step 540 (16 cells). Both panels use the same scales."),
}


def lettering(font, words):
    left, top, right, bottom = font.getbbox(words)
    img = Image.new("L", (right - left, bottom - top))
    ImageDraw.Draw(img).text((-left, -top), words, 255, font=font)
    return np.asarray(img)


def make(font_dir, output):
    faces = {bold: font_dir / name for bold, name in [(False, "Vera.ttf"), (True, "VeraBd.ttf")]}
    result = {key: lettering(ImageFont.truetype(str(faces[bold]), size), words)
              for key, (size, bold, words) in LABELS.items()}
    digits = ImageFont.truetype(str(faces[False]), 23)
    # Tick labels share a baseline and the exact advance of the font's figures.
    for char in "0123456789.-+e":
        width = round(digits.getlength(char))
        canvas = Image.new("L", (width, 31))
        ImageDraw.Draw(canvas).text((0, 24), char, font=digits, fill=255, anchor="ls")
        result["char_" + str(ord(char))] = np.asarray(canvas)
    result["license"] = np.frombuffer((font_dir / "bitstream-vera-license.txt").read_bytes(), np.uint8)
    np.savez_compressed(output, **result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    make(args.font_dir, args.output)
