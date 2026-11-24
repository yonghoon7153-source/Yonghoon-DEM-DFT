import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock


def load():
    path = Path(__file__).with_name("ladder.py")
    spec = importlib.util.spec_from_file_location("ladder", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LadderTest(unittest.TestCase):
    def setUp(self):
        self.app = load()

    def test_author_two_levels_only(self):
        self.assertEqual(self.app.ARMS, ("L020", "L050"))

    def test_both_fit_with_ub(self):
        self.assertEqual(self.app.budget("368469|RUNNING|6", None), 46)

    def test_refuse_before_either_submission(self):
        with self.assertRaises(ValueError):
            self.app.budget("111|RUNNING|21", None)

    def test_count_pending_and_completing(self):
        with self.assertRaises(ValueError):
            self.app.budget("111|PENDING|12\n222|COMPLETING|9", None)

    def test_missing_acknowledged_first_still_costs_twenty(self):
        self.assertEqual(self.app.budget("368469|RUNNING|6", "999"), 46)
        with self.assertRaises(ValueError):
            self.app.budget("111|RUNNING|21", "999")

    def test_visible_first_counted_once(self):
        self.assertEqual(self.app.budget("368469|RUNNING|6\n999|PENDING|20", "999"), 46)
        self.assertEqual(self.app.budget("111|RUNNING|20\n999|RUNNING|20", "999"), 60)

    def test_unknown_duplicate_or_wrong_first_rejected(self):
        for raw in ("11|RUNNING|0", "11|FUTURE|4", "11|RUNNING|4\n11|PENDING|4", "999|RUNNING|19"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.app.budget(raw, "999")

    def test_submit_and_monitor_in_order_with_two_capacity_reads(self):
        send = Mock(side_effect=["101","102"])
        with tempfile.TemporaryDirectory() as tmp:
            events = []
            self.app.dispatch(Path(tmp), lambda prior: events.append(prior), send,
                              lambda a,j: events.append((a,j)))
            self.assertEqual(events, [None,("L020","101"),"101",("L050","102")])
            with self.assertRaises(FileExistsError):
                self.app.dispatch(Path(tmp), Mock(), send, Mock())
            self.assertEqual(send.call_count,2)

    def test_partial_failure_does_not_resubmit_or_cancel_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            send = Mock(return_value="101")
            cap = Mock(side_effect=[None, ValueError("capacity")])
            watch = Mock()
            with self.assertRaises(ValueError):
                self.app.dispatch(Path(tmp), cap, send, watch)
            self.assertEqual(send.call_count, 1)
            watch.assert_called_once_with("L020","101")
            with self.assertRaises(FileExistsError):
                self.app.dispatch(Path(tmp), Mock(), send, Mock())

    def test_ambiguous_first_reply_stops_second(self):
        with tempfile.TemporaryDirectory() as tmp:
            send = Mock(side_effect=RuntimeError("no receipt"))
            watch = Mock()
            with self.assertRaises(RuntimeError):
                self.app.dispatch(Path(tmp),Mock(),send,watch)
            self.assertEqual(send.call_count,1)
            watch.assert_not_called()

    def test_wall_and_w9(self):
        a = self.app.classify
        self.assertEqual(a("TIMEOUT",False,False,"UNKNOWN_TIME"),"TECH_MISSING_TIMEOUT")
        self.assertEqual(a("COMPLETED",True,True,"LIVE_TERMINAL_MATCH"),"COMPLETE")
        self.assertEqual(a("COMPLETED",True,True,"RECOVERY_ONLY"),"TECH_MISSING")
        self.assertEqual(a("COMPLETED",True,False,"LIVE_TERMINAL_MATCH"),"TECH_MISSING")


if __name__ == "__main__":
    unittest.main()
