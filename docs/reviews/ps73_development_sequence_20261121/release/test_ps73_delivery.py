"""Offline checks for one-shot packaging and author readback."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile


def sibling(name):
    p = Path(__file__).resolve().with_name(name + ".py")
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


boot = sibling("field_boot")
collector = sibling("collect_ps73")
reader = sibling("check_return")


class Delivery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        self.ops = self.work / "ops"
        self.rj = self.work / "research"
        self.bed = self.rj / "ps_7_3_r45"
        self.bed.mkdir(parents=True)
        self.files = {n:b"test\n" for n in ("phase_controller.py", "phase_arm.sbatch", "run_arm.sh",
                                           "ps73_node.py", "ps73_sequence.py", "collect_ps73.py")}
        self.raw = "".join(boot.digest(v)+"  "+n+"\n" for n,v in self.files.items()).encode("ascii")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            for n,v in self.files.items():
                z.writestr(n,v)
            z.writestr("SOURCE_SHA256SUMS", self.raw)
        self.data = buf.getvalue()
        self.ph = boot.digest(self.data)
        self.sh = boot.digest(self.raw)

    def test_same_deployment_reused_changed_deployment_fails(self):
        boot.install(self.ops, self.data, self.ph, self.sh)
        old = (self.ops / "phase_controller.py").stat().st_mtime_ns
        boot.install(self.ops, self.data, self.ph, self.sh)
        self.assertEqual((self.ops / "phase_controller.py").stat().st_mtime_ns, old)
        (self.ops / "phase_controller.py").write_text("different")
        with self.assertRaises(ValueError):
            boot.install(self.ops, self.data, self.ph, self.sh)

    def test_unexpected_payload_never_installed(self):
        with self.assertRaises(ValueError):
            boot.install(self.ops, self.data+b"x", self.ph, self.sh)
        self.assertFalse(self.ops.exists())
        with self.assertRaises(ValueError):
            boot.inventory(self.raw + (boot.digest(b"x")+"  ../x\n").encode())
        with self.assertRaises(ValueError):
            boot.inventory(self.raw + self.raw)

    def test_collect_terminal_only(self):
        jobs = self.ops / "state" / "jobs"
        for arm in ("UB","UT"):
            (jobs / arm).mkdir(parents=True)
            (self.bed / (arm+".report.tgz")).write_bytes(b"synthetic report")
        (jobs/"UB"/"receipt.json").write_text('{"test": true}')
        dst=self.work/"returned.zip"
        with dst.open("wb") as out:
            collector.collect(self.ops,self.rj,out)
        result=reader.verify(dst)
        self.assertEqual(result["terminal_reports"],["UB"])
        with zipfile.ZipFile(dst) as z:
            self.assertNotIn("reports/UT.report.tgz",z.namelist())

    def test_collection_manifest_rejects_substitution(self):
        p=self.work/"wrong.zip"
        with zipfile.ZipFile(p,"w") as z:
            z.writestr("collection.json",b"{}")
            z.writestr("SHA256SUMS","0"*64+"  collection.json\n")
        with self.assertRaises(ValueError):
            reader.verify(p)


if __name__=="__main__":
    unittest.main()
