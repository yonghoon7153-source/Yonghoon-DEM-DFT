"""Graphic regression tests. All generated traces and images are temporary fixtures."""
import csv
import hashlib
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch

import numpy as np

import render_weekly as plot


def make_fixture(base):
    target = base / "pressure_displacement.csv"
    original = {}
    with target.open("w", newline="", encoding="ascii") as file:
        long_form = csv.writer(file)
        long_form.writerow(plot.FIELDS)
        for model in plot.MODELS:
            for cells, nsteps in plot.GRIDS.items():
                folder = base / model / f"F{cells}"
                folder.mkdir(parents=True)
                path = folder / "trace.csv"
                with path.open("w", newline="", encoding="ascii") as f:
                    writer = csv.writer(f)
                    writer.writerow(["step", "time_code", "height", "bottom_pressure_E", "phi_m"])
                    for step in range(nsteps + 1):
                        t = step / nsteps
                        h = .7 - t * .012
                        pressure_e = .0046 * t**3 * (8 / cells) if model == "original" else 0.0
                        writer.writerow([step, t, h, pressure_e, .78])
                        long_form.writerow([model, cells, step, t, h, .7 - h, pressure_e * 10])
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                if model == "original":
                    original[cells] = digest
                else:
                    receipt = dict(status="SHORT_PREFIX_COMPLETE", wall_model=model, cells=cells,
                                   steps=nsteps, trace_sha256=digest, u6_qualified=False)
                    (folder / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    return target, original


def read_png(path):
    raw = path.read_bytes()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    chunks = {}
    start = 8
    while start < len(raw):
        n = struct.unpack(">I", raw[start:start+4])[0]
        kind = raw[start+4:start+8]
        data = raw[start+8:start+8+n]
        crc = struct.unpack(">I", raw[start+8+n:start+12+n])[0]
        assert zlib.crc32(kind + data) == crc
        chunks.setdefault(kind, []).append(data)
        start += n + 12
    return chunks


class WeeklyFigureTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path, self.pins = make_fixture(self.root)
        mock_pins = patch.object(plot, "ORIGINAL_DIGESTS", self.pins)
        mock_pins.start()
        self.addCleanup(mock_pins.stop)

    def test_preserves_four_native_series_and_units(self):
        curves, raw = plot.read_curves(self.path)
        self.assertEqual(len(raw.splitlines()), 1625)
        self.assertEqual([len(rows) for rows in curves.values()], [271, 541, 271, 541])
        self.assertAlmostEqual(curves["original", 8][-1][0], .12)
        self.assertAlmostEqual(curves["original", 8][-1][1], .046)
        self.assertTrue(all(p == 0.0 for _, p in curves["candidate", 8]))

    def test_rejects_mismatched_pressure(self):
        self.path.write_bytes(self.path.read_bytes().replace(b"0.046", b"0.246", 1))
        with self.assertRaises(ValueError):
            plot.read_curves(self.path)

    def test_rejects_incomplete_long_csv(self):
        self.path.write_bytes(b"\n".join(self.path.read_bytes().splitlines()[:-1]))
        with self.assertRaises(ValueError):
            plot.read_curves(self.path)

    def test_rejects_changed_original_pin(self):
        self.pins[8] = "0" * 64
        with self.assertRaisesRegex(ValueError, "registered source"):
            plot.read_curves(self.path)

    def test_rejects_missing_candidate_inputs(self):
        for missing in ["trace.csv", "receipt.json"]:
            with self.subTest(missing=missing):
                target = self.root / "candidate" / "F8" / missing
                data = target.read_bytes()
                target.unlink()
                with self.assertRaises(FileNotFoundError):
                    plot.read_curves(self.path)
                target.write_bytes(data)

    def test_rejects_unbound_candidate(self):
        for field, invalid in [("status", "HOLD"), ("trace_sha256", "0" * 64),
                               ("cells", 16), ("u6_qualified", True)]:
            with self.subTest(field=field):
                target = self.root / "candidate/F8/receipt.json"
                old = target.read_bytes()
                receipt = json.loads(old)
                receipt[field] = invalid
                target.write_text(json.dumps(receipt), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "receipt"):
                    plot.read_curves(self.path)
                target.write_bytes(old)

    def test_png_links_csv_and_shows_zero_on_pressure_baseline(self):
        output = self.root / "weekly.png"
        curves, data = plot.read_curves(self.path)
        plot.save(curves, data, output)
        chunks = read_png(output)
        self.assertEqual(struct.unpack(">2I", chunks[b"IHDR"][0][:8]), (1740, 858))
        self.assertIn(b"CSV_SHA256\0" + hashlib.sha256(data).hexdigest().encode(),
                      chunks[b"tEXt"])
        scanlines = np.frombuffer(zlib.decompress(b"".join(chunks[b"IDAT"])), np.uint8)
        rows = scanlines.reshape(plot.HEIGHT, 1 + 3 * plot.WIDTH)
        self.assertTrue(np.all(rows[:, 0] == 0))
        rgb = rows[:, 1:].reshape(plot.HEIGHT, plot.WIDTH, 3)
        for color in (plot.COARSE, plot.FINE):
            self.assertTrue(np.all(rgb[653:662, 995:1500] == color, axis=2).any())
        self.assertTrue((rgb[607:644, 1010:1640].min(axis=2) < 120).any())
        self.assertTrue(np.all(rgb[255, 1000:1640] == 255))  # no top spine
        self.assertTrue(np.all(rgb[260:310, 1645] == 255))  # no right spine

    def test_nonzero_candidate_shows_both_series_without_the_zero_annotation(self):
        curves, _ = plot.read_curves(self.path)
        for cells in plot.GRIDS:
            curves["candidate", cells] = [(u, p * .75) for u, p in curves["original", cells]]
        with np.load(plot.TYPE, allow_pickle=False) as atlas:
            rgb = plot.render_image(curves, atlas)
        for color in (plot.COARSE, plot.FINE):
            panel = rgb[300:630, 1000:1640]
            self.assertTrue(np.all(panel == color, axis=2).any())
        self.assertTrue(np.all(rgb[608:633, 1020:1130] == 255))


if __name__ == "__main__":
    unittest.main()
