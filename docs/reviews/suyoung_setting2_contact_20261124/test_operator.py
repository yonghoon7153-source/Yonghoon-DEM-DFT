import io
import runpy
import tarfile
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class OperatorContract(unittest.TestCase):
    def setUp(self):
        self.b = runpy.run_path(str(HERE / "build_block.py"))

    def test_source_roundtrip_and_manifest(self):
        files = {"RELEASE": b"x\n", "sub/one": b"1\n"}
        files["SOURCE_SHA256SUMS"] = self.b["sums"](files)
        packed = self.b["pack"](files)
        self.assertEqual(self.b["unpack_verified"](packed), files)
        self.assertEqual(self.b["pack"](files), packed)
        files["sub/one"] = b"2\n"
        with self.assertRaises(ValueError):
            self.b["unpack_verified"](self.b["pack"](files))

    def test_dangerous_and_duplicate_member(self):
        for names in (("../b",), ("a", "a"), ("A", "a")):
            buf = io.BytesIO()
            with tarfile.open(fileobj=buf, mode="w:gz") as tar:
                for name in names:
                    tar.addfile(tarfile.TarInfo(name))
            with self.subTest(names=names), self.assertRaises(ValueError):
                self.b["unpack_verified"](buf.getvalue())

    def test_old_block_rejects_edits(self):
        with self.assertRaisesRegex(ValueError, "operator identity"):
            self.b["baseline"](b"tampered")

    def test_preserve_existing_output(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/"block.txt"
            put = self.b["write_once"]
            put(p, b"x")
            put(p, b"x")
            with self.assertRaises(FileExistsError):
                put(p, b"y")
            self.assertEqual(p.read_bytes(), b"x")


if __name__ == "__main__":
    unittest.main()
