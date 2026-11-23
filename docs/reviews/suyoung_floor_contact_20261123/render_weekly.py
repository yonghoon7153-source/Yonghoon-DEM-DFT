"""Draw the four verified early-loading curves. Requires only Python and NumPy."""
import argparse
import csv
import hashlib
import io
import json
import math
import struct
import tempfile
import zlib
from pathlib import Path

import numpy as np


DIAMETER = 0.1  # solver length units per disk diameter
GRIDS = {8: 270, 16: 540}
MODELS = ("original", "candidate")
FIELDS = ["wall_model", "cells", "step", "time_code", "height", "displacement_code", "pressure_MPa"]
ORIGINAL_DIGESTS = {
    8: "0e5e021706abbc88a728a305807edfce02aa877bcd92d824d5aa2988515aebce",
    16: "60b31c9055734a24cd9aaa0ed1b5809fad338fb6d5848ab0a49f4d52f9945eca",
}
TYPE = Path(__file__).with_name("weekly_type.npz")
INK = (24, 42, 55)
MUTED = (68, 87, 97)
COARSE = (11, 103, 115)
FINE = (171, 76, 28)
GRID = (220, 228, 230)
WIDTH, HEIGHT = 1740, 858


def require(value, message):
    if not value:
        raise ValueError(message)


def native_rows(path, model, cells):
    data = path.read_bytes()
    if model == "original":
        require(hashlib.sha256(data).hexdigest() == ORIGINAL_DIGESTS[cells],
                f"Original F{cells} trace differs from the registered source.")
    else:
        receipt = json.loads(path.with_name("receipt.json").read_text(encoding="utf-8"))
        expected = {"status": "SHORT_PREFIX_COMPLETE", "wall_model": model, "cells": cells,
                    "steps": GRIDS[cells], "trace_sha256": hashlib.sha256(data).hexdigest()}
        require(all(receipt.get(k) == v for k, v in expected.items()) and
                receipt.get("u6_qualified") is False, f"Invalid candidate F{cells} receipt.")
    records = list(csv.DictReader(io.StringIO(data.decode("ascii"))))
    require(len(records) == GRIDS[cells] + 1, f"Incomplete {model} F{cells} trace.")
    h0 = float(records[0]["height"])
    rows = []
    for step, record in enumerate(records):
        t = float(record["time_code"])
        h = float(record["height"])
        u = h0 - h
        p = float(record["bottom_pressure_E"]) * 10.0
        require(all(map(math.isfinite, (t, h, u, p))) and h > 0 and p >= 0
                and int(record["step"]) == step, f"Invalid {model} F{cells} native step {step}.")
        if step == 0:
            require(t == 0 and u == 0 and p == 0, f"Incorrect {model} F{cells} origin.")
        else:
            require(t > rows[-1][0] and u > rows[-1][2], f"Nonmonotonic {model} F{cells} trace.")
        rows.append((t, h, u, p))
    return rows


def read_curves(source):
    raw = source.read_bytes()
    reader = csv.DictReader(io.StringIO(raw.decode("ascii")))
    require(reader.fieldnames == FIELDS, "Unexpected pressure-displacement CSV columns.")
    data = {(model, cells): [] for model in MODELS for cells in GRIDS}
    for r in reader:
        key = (r["wall_model"], int(r["cells"]))
        require(key in data and int(r["step"]) == len(data[key]), "Invalid model, grid or step order.")
        data[key].append(tuple(float(r[f]) for f in FIELDS[3:]))
    for (model, cells), series in data.items():
        native = source.parent / model / f"F{cells}" / "trace.csv"
        require(series == native_rows(native, model, cells), f"Source disagreement in {model} F{cells}.")
    for cells in GRIDS:
        require([row[:3] for row in data["original", cells]] ==
                [row[:3] for row in data["candidate", cells]], f"Unmatched F{cells} platen travel.")
    require([row[:3] for row in data["original", 8]] ==
            [row[:3] for row in data["original", 16][::2]], "Unmatched grid schedules.")
    return {key: [(u / DIAMETER, p) for _, _, u, p in rows] for key, rows in data.items()}, raw


def stroke(image, start, end, color, width):
    """Antialiased line segment with round caps, directly in raster coordinates."""
    x1, y1 = start
    x2, y2 = end
    reach = width / 2 + 1
    left = max(0, math.floor(min(x1, x2) - reach))
    right = min(image.shape[1], math.ceil(max(x1, x2) + reach) + 1)
    top = max(0, math.floor(min(y1, y2) - reach))
    bottom = min(image.shape[0], math.ceil(max(y1, y2) + reach) + 1)
    x = np.arange(left, right) - x1
    y = np.arange(top, bottom)[:, None] - y1
    dx, dy = x2 - x1, y2 - y1
    norm = dx * dx + dy * dy
    along = np.clip((x * dx + y * dy) / norm, 0, 1) if norm else 0.0
    alpha = np.clip(width / 2 + .5 - np.hypot(x - along * dx, y - along * dy), 0, 1)[..., None]
    patch = image[top:bottom, left:right]
    patch[:] = np.rint(patch * (1 - alpha) + np.asarray(color) * alpha).astype(np.uint8)


def line_series(image, points, color, dashed=False):
    on, remaining = True, 13.0
    for a, b in zip(points, points[1:]):
        if not dashed:
            stroke(image, a, b, color, 3.9)
            continue
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        # The dash phase follows actual screen-space length across every native sample.
        offset = 0.0
        while length - offset > 1e-10:
            delta = min(remaining, length - offset)
            if on:
                p0 = (a[0] + dx * offset / length, a[1] + dy * offset / length)
                p1 = (a[0] + dx * (offset + delta) / length, a[1] + dy * (offset + delta) / length)
                stroke(image, p0, p1, color, 4.1)
            offset += delta
            remaining -= delta
            if remaining < 1e-10:
                on = not on
                remaining = 13.0 if on else 8.0


def paste_text(image, mask, position, color=INK, align="left"):
    y, x = position[1], position[0]
    h, w = mask.shape
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    x, y = round(x), round(y)
    require(0 <= x and 0 <= y and x + w <= image.shape[1] and y + h <= image.shape[0],
            "Graphic text exceeds the canvas.")
    rect = image[y:y+h, x:x+w]
    alpha = mask[..., None] / 255.0
    rect[:] = np.rint(rect * (1 - alpha) + np.asarray(color) * alpha).astype(np.uint8)


def tick_plan(peak, count=5):
    require(peak > 0 and math.isfinite(peak), "Axis maximum must be positive and finite.")
    rough = peak / count
    decade = 10.0 ** math.floor(math.log10(rough))
    spacing = next(f for f in (1, 2, 2.5, 5, 10) if f >= rough / decade) * decade
    return spacing, math.ceil(peak / spacing)


def tick_mask(atlas, n, spacing):
    dec = max(0, -math.floor(math.log10(spacing)))
    if not math.isclose(spacing, round(spacing, dec), rel_tol=1e-12):
        dec += 1
    word = (f"{n * spacing:.{dec}f}" if 0.0001 <= spacing < 10000
            else f"{n * spacing:.2g}")
    return np.concatenate([atlas["char_" + str(ord(c))] for c in word], axis=1)


def render_image(curves, atlas):
    graphic = np.full((HEIGHT, WIDTH, 3), 255, dtype=np.uint8)
    paste_text(graphic, atlas["title"], (82, 51))
    line_series(graphic, [(87, 140), (149, 140)], COARSE)
    paste_text(graphic, atlas["coarse"], (163, 130), MUTED)
    line_series(graphic, [(489, 140), (551, 140)], FINE, dashed=True)
    paste_text(graphic, atlas["fine"], (565, 130), MUTED)
    xstep, xn = tick_plan(max(u for series in curves.values() for u, _ in series), 6)
    ystep, yn = tick_plan(max(p for series in curves.values() for _, p in series))
    top, bottom, panel_w = 255, 657, 650
    for model, left in (("original", 146), ("candidate", 995)):
        right = left + panel_w
        middle = (left + right) / 2
        paste_text(graphic, atlas["before" if model == "original" else "after"], (left, 192))
        for n in range(yn + 1):
            y = bottom - n / yn * (bottom - top)
            if 0 < n < yn:
                stroke(graphic, (left, y), (right, y), GRID, 1)
            stroke(graphic, (left - 8, y), (left, y), MUTED, 1.5)
            paste_text(graphic, tick_mask(atlas, n, ystep), (left - 15, y - 16), MUTED, "right")
        for n in range(xn + 1):
            x = left + n / xn * panel_w
            stroke(graphic, (x, bottom), (x, bottom + 8), MUTED, 1.5)
            paste_text(graphic, tick_mask(atlas, n, xstep), (x, bottom + 14), MUTED, "center")
        stroke(graphic, (left, top), (left, bottom), MUTED, 1.6)
        stroke(graphic, (left, bottom), (right, bottom), MUTED, 1.6)
        for cells, color in ((8, COARSE), (16, FINE)):
            points = [(left + u / (xstep*xn) * panel_w, bottom - p / (ystep*yn) * (bottom-top))
                      for u, p in curves[model, cells]]
            line_series(graphic, points, color, dashed=(cells == 16))
        if all(p == 0 for cells in GRIDS for _, p in curves[model, cells]):
            paste_text(graphic, atlas["zero"], (middle, bottom - 49), MUTED, "center")
        paste_text(graphic, atlas["x"], (middle, 722), MUTED, "center")
        y_label = np.rot90(atlas["y"])
        paste_text(graphic, y_label, (left - 123, (top + bottom - y_label.shape[0]) / 2), MUTED)
    paste_text(graphic, atlas["note"], (82, 801), MUTED)
    return graphic


def png_chunk(kind, body):
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))


def save(curves, csv_bytes, destination, atlas_path=TYPE):
    with np.load(atlas_path, allow_pickle=False) as stored:
        atlas = {key: stored[key] for key in stored.files if key != "license"}
    image = render_image(curves, atlas)
    scan = b"".join(b"\0" + row.tobytes() for row in image)
    png = b"\x89PNG\r\n\x1a\n" + b"".join((
        png_chunk(b"IHDR", struct.pack(">2I5B", WIDTH, HEIGHT, 8, 2, 0, 0, 0)),
        png_chunk(b"pHYs", struct.pack(">2IB", 11811, 11811, 1)),
        png_chunk(b"tEXt", b"CSV_SHA256\0" + hashlib.sha256(csv_bytes).hexdigest().encode("ascii")),
        png_chunk(b"tEXt", b"Description\0Original and candidate early prefixes only. Both grids use identical axes. Displacement in disk diameters; bottom pressure in MPa."),
        png_chunk(b"IDAT", zlib.compress(scan, 7)), png_chunk(b"IEND", b"")))
    with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as tmp:
        temp_path = Path(tmp.name)
    try:
        temp_path.write_bytes(png)
        temp_path.replace(destination)
    finally:
        temp_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--png", type=Path, required=True)
    args = parser.parse_args()
    require(args.png.suffix.lower() == ".png", "Destination must be a .png file.")
    curves, raw = read_curves(args.csv)
    save(curves, raw, args.png)
    print(f"WEEKLY_PRESSURE_DISPLACEMENT_PNG {args.png}")


if __name__ == "__main__":
    main()
