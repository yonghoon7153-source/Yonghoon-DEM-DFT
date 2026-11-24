"""Synthetic row checks. The test inputs all live in a new temporary directory."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

_here=Path(__file__).resolve().parent
_tmp=tempfile.TemporaryDirectory()
_pkg=Path(_tmp.name)
(_pkg/"b7").mkdir()
shutil.copyfile(_here/"read_after_go.py",_pkg/"read_after_go.py")
_repo=_here.parents[2]
for _name in ("lhs_pressure_record.py","parse_liggghts.py","press_units.py"):
    raw=subprocess.check_output(["git","-c","safe.directory="+_repo.as_posix(),"-C",str(_repo),
                                 "show","35f0327377a4213774010a090df4d224e50d29e1:scripts/"+_name])
    (_pkg/"b7"/_name).write_bytes(raw)
sys.path.insert(0,str(_pkg))
import read_after_go as app


def tearDownModule():
    _tmp.cleanup()


class FreezeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        folder=self.root/"lhs00_100"
        folder.mkdir()
        self.log=folder/"log.liggghts"
        deck=folder/"input_lhs00_100.liggghts"
        deck.write_text('variable target_press equal 0.3\nlabel loop_press\n'
                        'print "Current Pressure: ${current_press} MPa (Target: ${target_press})"\n'
                        'if "${current_press} < ${target_press}" then "jump SELF loop_press"\n')
        self.row=dict(case=folder.name,run_segment=folder.name+"/run1",harvest_step=100,deck=deck.name,
                      deck_sha256=hashlib.sha256(deck.read_bytes()).hexdigest(),canonical_log=self.log.name)
        self.write("0.31")

    def write(self,last):
        rows=["Current Pressure: 0.4 MPa (Target: 0.3)","Current Pressure: "+last+" MPa (Target: 0.3)"]
        self.row.update(b7_line_count=2,b7_lines_sha256_prefix12=app.digest("\n".join(rows).encode())[:12])
        self.log.write_text("\n".join(["LIGGGHTS (Version fixture)",*rows,"100 0","Finished!"])+"\n")

    def test_nominal(self):
        # A second screen file must not displace or duplicate the canonical source.
        (self.log.parent/"log.txt").write_text("Current Pressure: 0.01 MPa (Target: 0.3)\n")
        r=app.assess(self.root,self.row)
        self.assertEqual((r["pressure_check"],r["b7"]["status"],float(r["b7"]["target_mpa"])),("OK","OK",300.))

    def test_last_not_peak(self):
        self.write("0.29")
        r=app.assess(self.root,self.row)
        self.assertEqual((r["pressure_check"],r["b7"]["status"]),("HOLD","NOT_REACHED"))

    def test_multiple_runs(self):
        self.log.write_text(self.log.read_text()+"LIGGGHTS (Version repeated)\n")
        self.assertEqual(app.assess(self.root,self.row)["reason"],"RUN_SEGMENT")

    def test_truncated_or_appended_output(self):
        self.log.write_text(self.log.read_text().replace("Finished!",""))
        self.assertEqual(app.assess(self.root,self.row)["reason"],"RUN_FINISH")
        self.write("0.31")
        with self.log.open("a") as out:
            out.write("Current Pressure: 0.31 MPa (Target: 0.3)\n")
        self.assertEqual(app.assess(self.root,self.row)["reason"],"B7_LINE_SHAPE_OR_SEGMENT")

    def test_identity(self):
        self.log.write_text(self.log.read_text().replace("0.31","0.309"))
        self.assertEqual(app.assess(self.root,self.row)["reason"],"REPORTED_B7_SEQUENCE")

    def test_harvest_marker(self):
        self.row["harvest_step"]=101
        self.assertEqual(app.assess(self.root,self.row)["reason"],"HARVEST_STEP_MARKER")

    def test_deck(self):
        self.row["deck_sha256"]="0"*64
        self.assertEqual(app.assess(self.root,self.row)["reason"],"DECK_IDENTITY")

    def test_nonfinite(self):
        self.write("nan")
        r=app.assess(self.root,self.row)
        self.assertEqual((r["pressure_check"],r["b7"]["status"]),("HOLD","REFUSED"))


if __name__=="__main__":
    unittest.main()
