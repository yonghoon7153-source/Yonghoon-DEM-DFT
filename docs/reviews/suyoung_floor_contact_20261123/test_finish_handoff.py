"""End-to-end packaging tests using fixed historical inputs and scratch-only synthetic candidates.

Set SUYOUNG_CROSS_RETURN to the pinned historical cross archive when testing outside
the local work tree. No trajectory driver or material solver is invoked by these tests.
"""
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
import struct
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

import finish_handoff as handoff


HERE = Path(__file__).resolve().parent
CASE = "docs/reviews/suyoung_floor_contact_20261123/"
PIN = "f" * 40  # Deliberately synthetic source-release identity, never an author release.
ARCHIVE = "suyoung_floor_prefix_result.tar.gz"


def load(filename, locations):
    path = next((p / filename for p in locations if (p / filename).is_file()), None)
    if path is None:
        raise FileNotFoundError(f"Cannot find test input {filename} in {locations}")
    spec = importlib.util.spec_from_file_location("test_input_" + path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


def json_bytes(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("ascii")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def manifest(files):
    return "".join(sha(raw) + "  " + name + "\n" for name, raw in sorted(files.items())).encode("ascii")


def fixture_sources():
    work = HERE.parent.parent
    checkout = work / "resume/floor-1123"
    operator, op_path = load("floor_operator.py", [HERE, HERE.parent / "operator"])
    figure, fig_path = load("render_weekly.py", [HERE, HERE.parent / "figure"])
    matched, matched_path = load("matched_controls.py", [
        HERE.parent / "suyoung_wall_layers_20261123", (checkout / operator.MATCHED).parent])
    candidates = [work / "suyoung_cross_readback_1123/suyoung_wall_cross_result.tar.gz"]
    if os.environ.get("SUYOUNG_CROSS_RETURN"):
        candidates.insert(0, Path(os.environ["SUYOUNG_CROSS_RETURN"]))
    cross = next((p for p in candidates if p.is_file()), None)
    if cross is None:
        raise FileNotFoundError("Set SUYOUNG_CROSS_RETURN to the pinned historical cross archive.")
    phys = next(p for p in (HERE / "material_floor.py", HERE.parent / "physics/material_floor.py") if p.is_file())
    programs = {
        "material_floor.py": phys, "floor_operator.py": op_path,
        "run_floor.sh": op_path.with_name("run_floor.sh"), "render_weekly.py": fig_path,
        "weekly_type.npz": fig_path.with_name("weekly_type.npz"),
    }
    release_files = {"RELEASE": (PIN + "\n").encode(), operator.MATCHED: matched_path.read_bytes()}
    release_files.update({CASE + name: path.read_bytes() for name, path in programs.items()})
    if sha(release_files[operator.MATCHED]) != operator.MATCHED_HASH:
        raise ValueError("Fixture requires the registered matched control reader.")
    hashes = {name: sha(raw) for name, raw in release_files.items()}
    hashes.update({"scripts/"+name: value for name, value in matched.SOURCES.items()})
    execution_manifest = "".join(value+"  "+name+"\n" for name, value in sorted(hashes.items())).encode()
    source = dict(release=PIN, release_manifest_sha256=sha(execution_manifest), physics_pin=matched.PHY,
                  native_protocol_pin=operator.MATCHED_PIN, physics_sha256=matched.SOURCES,
                  candidate_sha256=sha(phys.read_bytes()), operator_sha256=sha(op_path.read_bytes()),
                  archive_sha256=matched.PRIOR)
    return operator, matched, figure, cross, release_files, execution_manifest, source


def synthetic_zero_trace(raw):
    reader = csv.DictReader(io.StringIO(raw.decode("ascii")))
    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=reader.fieldnames, lineterminator="\r\n")
    writer.writeheader()
    for row in reader:
        writer.writerow(dict(row, bottom_pressure_E="0.0"))
    return text.getvalue().encode("ascii")


def build_fixture(root):
    op, matched, figure, cross, release, execution_manifest, src = fixture_sources()
    old = op.original(matched, cross)
    code = {"snapshot/" + n: v for n, v in release.items() if n.startswith("docs/")}
    code["CHAIN.json"] = json_bytes({"base": "e"*40, "release": PIN, "items": []})
    code["SHA256SUMS"] = manifest(code)
    source_zip = root / "source.zip"
    with zipfile.ZipFile(source_zip, "w") as z:
        for name, raw in code.items():
            z.writestr(name, raw)
    run = root / "fixture/run"
    for cells, originals in old.items():
        orig = run / "original" / f"F{cells}"
        orig.mkdir(parents=True)
        for name, raw in originals.items():
            (orig / name).write_bytes(raw)
        after = run / "candidate" / f"F{cells}"
        after.mkdir(parents=True)
        raw = synthetic_zero_trace(originals["trace.csv"])
        (after / "trace.csv").write_bytes(raw)
        steps = op.END[cells]
        audit = dict(steps=steps, floor_passes=2*steps, positive_passes=0, accumulated_impulse=0.,
                     max_grid_impulse_error=0., max_g2p_momentum_error=0., max_penetration=0.,
                     disk_boundary_vertices=256)
        receipt = op.candidate_receipt(matched, src, cells, raw, steps, audit)
        (after / "receipt.json").write_bytes(json_bytes(receipt))
    (run / "SOURCE_SHA256SUMS").write_bytes(execution_manifest)
    (run / "RELEASE").write_bytes(release["RELEASE"])
    screen = (f"DEVELOPMENT_ONLY\nRELEASE={PIN}\nCPU=0\nHARD_LIMIT_SECONDS_PER_ARM=600\nRETRIES=0\n"
              "F8_BEGIN=2000-01-01T00:00:00Z\nF8_RC=0\nF16_BEGIN=2000-01-01T00:01:00Z\n"
              "F16_RC=0\nFOUR_NATIVE_CURVES_AND_WEEKLY_PNG_OK\nCOMMAND_RC=0\n").encode()
    (run / "screen.txt").write_bytes(screen)
    summary = op.summarize((matched, src), old, run, write_outputs=True)
    curves, table = figure.read_curves(run / "pressure_displacement.csv")
    png = run / "weekly_pressure_displacement.png"
    figure.save(curves, table, png)
    summary["weekly_png_sha256"] = sha(png.read_bytes())
    (run / "summary.json").write_bytes(json_bytes(summary))
    members = {p.relative_to(run).as_posix(): p.read_bytes() for p in run.rglob("*") if p.is_file()}
    return source_zip, members, curves, figure


def write_return(dest, members):
    archive = dest / ARCHIVE
    with tarfile.open(archive, "w:gz") as z:
        for name, raw in sorted(members.items()):
            entry = tarfile.TarInfo("run/" + name)
            entry.size = len(raw)
            z.addfile(entry, io.BytesIO(raw))
    (dest / "screen.txt").write_bytes(members["screen.txt"])
    (dest / "SHA256SUMS").write_bytes(manifest({ARCHIVE: archive.read_bytes(), "screen.txt": members["screen.txt"]}))


class HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.base.cleanup)
        cls.source, cls.members, cls.curves, cls.figure = build_fixture(Path(cls.base.name))
        cls.source_sha = sha(cls.source.read_bytes())

    def setUp(self):
        scratch = tempfile.TemporaryDirectory(dir=self.base.name)
        self.addCleanup(scratch.cleanup)
        self.returned = Path(scratch.name)
        self.content = self.members.copy()
        self.target = self.returned / ("codex_suyoung_floor_contact_" + PIN[:12] + "_with_weekly.zip")

    def finish(self):
        with contextlib.redirect_stdout(io.StringIO()):
            handoff.finish(self.source, self.source_sha, self.returned, PIN)

    def rejects(self, diagnostic):
        write_return(self.returned, self.content)
        with self.assertRaisesRegex((ValueError, KeyError), diagnostic):
            self.finish()
        self.assertFalse(self.target.exists())
        self.assertFalse((self.returned / "HANDOFF_SHA256SUMS").exists())

    def test_complete_retry_and_interrupted_sidecar_repair(self):
        write_return(self.returned, self.content)
        self.finish()
        expected = self.target.read_bytes()
        sidecar = self.returned / "HANDOFF_SHA256SUMS"
        self.assertEqual(sidecar.read_bytes(), manifest({self.target.name: expected}))
        with zipfile.ZipFile(io.BytesIO(expected)) as z:
            self.assertIsNone(z.testzip())
            for name in ("pressure_displacement.csv", "weekly_pressure_displacement.png", "summary.json"):
                self.assertEqual(z.read("weekly/"+name), self.content[name])
            members = {n: z.read(n) for n in z.namelist() if n != "SHA256SUMS"}
            self.assertEqual(z.read("SHA256SUMS"), manifest(members))
        self.finish()
        self.assertEqual(self.target.read_bytes(), expected)
        sidecar.unlink()
        self.finish()
        self.assertEqual(self.target.read_bytes(), expected)
        self.assertEqual(sidecar.read_bytes(), manifest({self.target.name: expected}))

    def test_conflicting_existing_zip_is_preserved(self):
        write_return(self.returned, self.content)
        self.target.write_bytes(b"existing test handoff")
        with self.assertRaises(ValueError):
            self.finish()
        self.assertEqual(self.target.read_bytes(), b"existing test handoff")
        self.assertFalse((self.returned / "HANDOFF_SHA256SUMS").exists())

    def test_changed_png_with_stale_summary_is_rejected(self):
        key = "weekly_pressure_displacement.png"
        self.content[key] = self.content[key][:-12]
        self.rejects("weekly PNG")

    def test_damaged_png_with_resealed_outer_checksums_is_rejected(self):
        key = "weekly_pressure_displacement.png"
        raw = bytearray(self.content[key])
        start = raw.index(b"IDAT")
        length = struct.unpack(">I", raw[start-4:start])[0]
        raw[start + 4 + length // 2] ^= 1
        self.content[key] = bytes(raw)
        summary = json.loads(self.content["summary.json"])
        summary["weekly_png_sha256"] = sha(raw)
        self.content["summary.json"] = json_bytes(summary)
        self.rejects("PNG CRC")

    def test_valid_png_with_wrong_curve_pixels_is_rejected(self):
        key = "weekly_pressure_displacement.png"
        wrong = self.curves.copy()
        wrong["candidate", 16] = wrong["original", 16]
        with tempfile.TemporaryDirectory(dir=self.base.name) as d:
            image = Path(d) / "temp.png"
            self.figure.save(wrong, self.content["pressure_displacement.csv"], image)
            self.content[key] = image.read_bytes()
        summary = json.loads(self.content["summary.json"])
        summary["weekly_png_sha256"] = sha(self.content[key])
        self.content["summary.json"] = json_bytes(summary)
        self.rejects("PNG pixels")

    def test_failed_second_arm_has_no_weekly_handoff(self):
        self.content["screen.txt"] = self.content["screen.txt"].split(b"F16_RC=0")[0]+b"F16_RC=4\nCOMMAND_RC=4\n"
        self.content["incomplete.json"] = json_bytes(dict(status="INCOMPLETE", phase="F16", rc=4,
                                                          u6_qualified=False, stage3_go=False))
        for name in ("candidate/F16/receipt.json", "summary.json", "weekly_pressure_displacement.png",
                     "pressure_displacement.csv"):
            del self.content[name]
        self.rejects("field status")

    def test_missing_candidate_receipt_is_rejected(self):
        del self.content["candidate/F16/receipt.json"]
        self.rejects("candidate/F16/receipt.json")

    def test_conflicting_last_field_status_is_rejected(self):
        self.content["screen.txt"] += b"COMMAND_RC=4\n"
        self.rejects("field status")

    def test_synthetic_screen_marker_is_rejected(self):
        self.content["screen.txt"] = b"SYNTHETIC_QA_ONLY\n" + self.content["screen.txt"]
        self.rejects("field status")

    def test_synthetic_or_incomplete_archive_marker_is_rejected(self):
        for path in ("SYNTHETIC_QA_ONLY", "candidate/F8/incomplete.json"):
            with self.subTest(path=path):
                self.content[path] = b"test"
                self.rejects("incomplete run")
                del self.content[path]

    def changed_csv(self, field, number):
        table_name = "pressure_displacement.csv"
        reader = csv.DictReader(io.StringIO(self.content[table_name].decode("ascii")))
        rows = list(reader)
        rows[1][field] = number
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=reader.fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        raw = stream.getvalue().encode("ascii")
        self.content[table_name] = raw
        # Rebind the synthetic fixture's remaining containers to this edited table
        # so rejection must come from the independent comparison with native data.
        with tempfile.TemporaryDirectory(dir=self.base.name) as d:
            image = Path(d) / "temp.png"
            self.figure.save(self.curves, raw, image)
            self.content["weekly_pressure_displacement.png"] = image.read_bytes()
        summary = json.loads(self.content["summary.json"])
        summary["pressure_displacement_sha256"] = sha(raw)
        summary["weekly_png_sha256"] = sha(self.content["weekly_pressure_displacement.png"])
        self.content["summary.json"] = json_bytes(summary)

    def test_changed_pressure_with_resealed_checksums_is_rejected(self):
        self.changed_csv("pressure_MPa", "0.125")
        self.rejects("weekly data point")

    def test_changed_clock_with_resealed_checksums_is_rejected(self):
        self.changed_csv("time_code", "0.125")
        self.rejects("weekly data point")

    def test_changed_height_with_resealed_checksums_is_rejected(self):
        self.changed_csv("height", "0.625")
        self.rejects("weekly data point")


if __name__ == "__main__":
    unittest.main()
