import sys
import unittest
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import repeat

def projection(snapshot,previous):
    return repeat.projected_rows(repeat.allocations(snapshot),previous)

class Schedule(unittest.TestCase):
    def test_block_until_both_ladders_terminal(self):
        self.assertFalse(repeat.finished(["COMPLETED","RUNNING"]))
        self.assertFalse(repeat.finished(["COMPLETED",""]))
        self.assertTrue(repeat.finished(["COMPLETED","TIMEOUT"]))
    def test_each_wave_waits_for_40_and_allows_at_limit(self):
        q="373356|RUNNING|20\n373357|PENDING|20\n368469|RUNNING|6"
        self.assertEqual(projection(q,None),86)
        self.assertEqual(projection("1|PENDING|20",None),60)
        self.assertEqual(projection("1|RUNNING|18",None),58)
    def test_second_reserves_invisible_ack(self):
        self.assertEqual(projection("1|RUNNING|18","10"),58)
        self.assertEqual(projection("1|RUNNING|18\n10|PENDING|20","10"),58)
        self.assertEqual(projection("1|PENDING|21","10"),61)
    def test_refuse_invalid_snapshot(self):
        for q in ("1|RUNNING|0","1|?", "1|PENDING|10\n1|PENDING|10"):
            with self.assertRaises(ValueError):
                projection(q,None)
    def test_terminal_ids_exact(self):
        self.assertEqual(repeat.state_of("10.batch|COMPLETED|0:0\n11|COMPLETED|0:0","10"),"")
        with self.assertRaises(ValueError):
            repeat.state_of("10|RUNNING|0:0\n10|COMPLETED|0:0","10")
    def test_finished_first_arm_no_longer_reserves_20(self):
        with patch.object(repeat,"queue",return_value="9|PENDING|39"), \
             patch.object(repeat,"account",return_value="COMPLETED"), \
             patch.object(repeat.time,"sleep",side_effect=AssertionError("unneeded wait")), \
             patch.object(repeat,"progress"):
            self.assertEqual(repeat.room("11"),59)
    def test_terminal_jobs_must_also_leave_queue(self):
        with patch.object(repeat,"account",return_value="COMPLETED"), \
             patch.object(repeat,"queue",side_effect=["11|COMPLETING|20","99|PENDING|6"]), \
             patch.object(repeat.time,"sleep") as wait,patch.object(repeat,"progress"):
            repeat.wait_done(("11","12"))
            wait.assert_called_once()
if __name__=="__main__":unittest.main()
