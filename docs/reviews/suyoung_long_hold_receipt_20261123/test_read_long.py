"""Contract tests of offline intake. Accept a verified old archive and manufactured new snapshots."""
import importlib.util
import io
from pathlib import Path
import tarfile
import tempfile
import unittest


here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("reader", here/"read_long.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class ArchiveContract(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.addCleanup(self.root.cleanup)
        self.path = Path(self.root.name)/"case.tar.gz"

    def manufacture(self, members, *, external=b"COMMAND_RC=0\n"):
        with tarfile.open(self.path, "w:gz") as tar:
            for key, raw in members:
                info = tarfile.TarInfo(key)
                info.size = len(raw)
                tar.addfile(info, io.BytesIO(raw))
        self.path.with_name("screen.txt").write_bytes(external)
        self.path.with_name("SHA256SUMS").write_text(
            f"{reader.sha(self.path.read_bytes())}  case.tar.gz\n{reader.sha(external)}  screen.txt\n")

    def test_outer_and_inner_screen(self):
        self.manufacture([("run/screen.txt", b"COMMAND_RC=0\n")])
        members, times, hashes = reader.archive(self.path)
        self.assertEqual(members["screen.txt"], b"COMMAND_RC=0\n")
        self.assertIn("screen.txt", times)
        self.assertEqual(hashes["case.tar.gz"], reader.sha(self.path.read_bytes()))
        self.path.with_name("screen.txt").write_bytes(b"another screen")
        with self.assertRaisesRegex(ValueError, "return manifest"):
            reader.archive(self.path)
        self.manufacture([("run/screen.txt", b"wrong")])
        with self.assertRaisesRegex(ValueError, "inner screen"):
            reader.archive(self.path)

    def test_unsafe_and_duplicate(self):
        for bad in ("run/../outside","RUN/screen.txt","run/other/../screen.txt","run/SCREEN.TXT"):
            with self.subTest(bad):
                self.manufacture([("run/screen.txt", b"COMMAND_RC=0\n"),(bad,b"x")])
                with self.assertRaisesRegex(ValueError, "unexpected or duplicate"):
                    reader.archive(self.path)


if __name__ == "__main__":
    unittest.main()
