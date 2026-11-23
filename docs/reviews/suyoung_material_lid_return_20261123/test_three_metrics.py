"""Build a manufactured complete candidate on the frozen clocks. No integration is run."""
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tarfile
import tempfile
from types import SimpleNamespace
import unittest

spec = importlib.util.spec_from_file_location("read_three_metrics", Path(__file__).with_name("read_three_metrics.py"))
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


def encode_csv(data):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, data[0].keys(), lineterminator="\n")
    writer.writeheader()
    writer.writerows(data)
    return stream.getvalue().encode("ascii")


def manufactured():
    native = reader.load_native(reader.DEFAULT_NATIVE)
    prior = reader.read_run(reader.DEFAULT_BASELINE, reader.IDENTITY["baseline_sha256"], "wall_impulses.csv", "balance_receipt.json")
    old, new, receipts = {}, {}, {}
    files = {"run/RELEASE": (reader.IDENTITY["release"]+"\n").encode(),
             "run/screen.txt": b"F12_RC=0\nF24_RC=0\nMATERIAL_LID_PREFIX_READBACK_COMPLETE\nCOMMAND_RC=0\n"}
    # Reuse the manifest exactly as supplied in the release-bound source handoff.
    import base64
    block = Path(os.environ["SUYOUNG_MATERIAL_LID_BLOCK"]).read_bytes()
    encoded = block.split(b"<<'MATERIAL_LID_SOURCES'\n", 1)[1].split(b"\nMATERIAL_LID_SOURCES\n", 1)[0]
    with tarfile.open(fileobj=io.BytesIO(base64.b64decode(encoded))) as pack:
        files["run/SOURCE_SHA256SUMS"] = pack.extractfile("SOURCE_SHA256SUMS").read()
    for n, count in native.STEPS.items():
        key = f"run/F{n}/"
        old[n] = native.rows(prior[key+"trace.csv"])
        new[n] = [dict(row) for row in old[n]]
        width = float(old[n][0]["height"])
        dt = float(old[n][1]["time_code"])
        prescribed = {465: .02, 569: .02} if n == 12 else {930: .01, 931: .08, 1137: .03, 1138: .015}
        walls = []
        for i, row in enumerate(new[n][1:], 1):
            p = prescribed.get(i, 0.)
            row["bottom_pressure_E"] = str(p)
            floor = p*dt*width
            down = floor/2 if n == 12 else 0.
            walls.append(dict(step=i, floor_impulse=floor, lid_downward_impulse=down, lid_signed_impulse=-down,
                              top_gap_before=0., top_gap_after=0., floor_gap_after=0., lid_grid_impulse_error=0.))
        floor = dict(steps=count, floor_passes=2*count, positive_passes=len(prescribed), max_penetration=0.,
                     max_grid_impulse_error=0., max_g2p_momentum_error=0., accumulated_impulse=sum(r["floor_impulse"] for r in walls))
        lid = dict(steps=count, lid_passes=2*count, positive_passes=len(prescribed) if n == 12 else 0, max_clock_error=0.,
                   max_penetration=0., max_grid_impulse_error=0., accumulated_downward_impulse=sum(r["lid_downward_impulse"] for r in walls))
        files[key+"trace.csv"], files[key+"wall_steps.csv"] = encode_csv(new[n]), encode_csv(walls)
        receipts[str(n)] = native.receipt(SimpleNamespace(DT={n: dt}), SimpleNamespace(solver=SimpleNamespace(WIDTH=width)),
                                          reader.IDENTITY, n, files[key+"trace.csv"], files[key+"wall_steps.csv"], floor, lid)
        files[key+"candidate_receipt.json"] = json.dumps(receipts[str(n)]).encode()
    summary = dict(**reader.IDENTITY, label="DEVELOPMENT_ONLY", arms=receipts, status="MATCHED_PREFIX_COMPLETE",
                   old_grid_lid=native.compare(old, width), new_material_lid=native.compare(new, width), reference_MPa=native.REF_MPA,
                   u6_qualified=False, stage3_go=False, three_dimensional_go=False)
    files["run/summary.json"] = json.dumps(summary).encode()
    return files


class OfflineMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = manufactured()

    def attempt(self, changes=None, wrong_digest=False):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "synthetic.tar.gz"
            with tarfile.open(path, "w:gz") as archive:
                for name, raw in (self.files | (changes or {})).items():
                    entry = tarfile.TarInfo(name)
                    entry.size = len(raw)
                    archive.addfile(entry, io.BytesIO(raw))
            digest = "0"*64 if wrong_digest else hashlib.sha256(path.read_bytes()).hexdigest()
            return reader.evaluate(path, digest)

    def test_union_and_fixed_native_steps(self):
        report = self.attempt()
        union = report["new_material_lid"]["pressure_union"]
        self.assertEqual((union["samples"], union["peak"]["step_F24"]), (1139, 931))
        self.assertAlmostEqual(union["max_abs_gap_MPa"], .7)
        self.assertAlmostEqual(union["peak"]["signed_gap_MPa"], -.7)
        old_union = report["old_grid_lid"]["pressure_union"]
        self.assertAlmostEqual(old_union["max_abs_gap_MPa"], .09719855047759547)
        records = report["new_material_lid"]["fixed_landmarks"]
        self.assertEqual([[v["steps"][0] for v in record["native_steps"].values()] for record in records],
                         [[465, 930], [569, 1138]])
        self.assertFalse(report["u6_qualified"] or report["stage3_go"] or report["three_dimensional_go"])

    def test_signed_wall_inference_null_ratio_and_shared_window(self):
        last = self.attempt()["new_material_lid"]["fixed_landmarks"][1]
        a, b = last["native_steps"].values()
        self.assertEqual(a["floor_over_abs_lid"], 2.)
        self.assertIsNone(b["floor_over_abs_lid"])
        self.assertAlmostEqual(a["inferred_whole_delta_Py_J"], a["floor_J"]+a["lid_signed_J"])
        self.assertAlmostEqual(a["inferred_whole_delta_Py_equivalent_MPa"], .1)
        self.assertAlmostEqual(b["inferred_whole_delta_Py_equivalent_MPa"], .15)
        self.assertAlmostEqual(last["F12_minus_F24_native"]["inferred_whole_delta_Py_equivalent_MPa"], -.05)
        common = last["identical_window"]
        self.assertEqual(common["F24"]["steps"], [1137, 1138])
        self.assertEqual(common["F24"]["duration_code"], common["F12"]["duration_code"])
        self.assertAlmostEqual(common["F12_minus_F24"]["inferred_whole_delta_Py_equivalent_MPa"], -.125)

    def test_rejects_wrong_sha_release_manifest_or_incomplete(self):
        with self.assertRaisesRegex(ValueError, "archive SHA"):
            self.attempt(wrong_digest=True)
        for name, bad, match in (("run/RELEASE", b"old\n", "release"), ("run/SOURCE_SHA256SUMS", b"other\n", "manifest"),
                                 ("run/screen.txt", b"COMMAND_RC=1\n", "status"), ("run/F12/incomplete.json", b"{}", "partial")):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, match):
                self.attempt({name: bad})

    def test_rejects_resealed_tampered_csv_or_flags(self):
        for name in ("run/F12/trace.csv", "run/F24/wall_steps.csv"):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "arm receipt"):
                self.attempt({name: self.files[name].replace(b"\n", b"\r\n")})
        for name, flag in (("run/F12/candidate_receipt.json", "u6_qualified"), ("run/summary.json", "stage3_go")):
            obj = json.loads(self.files[name])
            obj[flag] = 0
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.attempt({name: json.dumps(obj).encode()})


if __name__ == "__main__":
    unittest.main()
