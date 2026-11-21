import importlib.util
from pathlib import Path
import unittest


spec = importlib.util.spec_from_file_location("shared_control", Path(__file__).with_name("shared_control.py"))
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class SharedControlTests(unittest.TestCase):
    def test_cancels_shared_error_with_different_knots(self):
        curves = {"Sc": [(0, 0), (1, 3)], "Sf": [(0, 0), (.5, 1), (1, 2)],
                  "Fc": [(0, 0), (1, 4)], "Ff": [(0, 0), (.25, .75), (1, 3)]}
        result = reader.control(curves)
        self.assertEqual(result["union_knots"], 4)
        self.assertEqual(result["peaks"]["F_minus_S_grid_difference"]["absolute_MPa"], 0)
        self.assertEqual(result["at_F_abs_peak"]["S_grid_difference_MPa"], 1)

    def test_interior_peak_and_common_endpoint(self):
        curves = {"Sc": [(0, 0), (1, 2)], "Sf": [(0, 0), (.5, 1)],
                  "Fc": [(0, 0), (.25, 3), (1, 0)], "Ff": [(0, 0), (1, 0), (2, 5)]}
        result = reader.control(curves)
        self.assertEqual(result["four_way_end_u"], .5)
        self.assertEqual(result["two_way_end_u"], {"S": .5, "F": 1})
        self.assertEqual(result["at_F_abs_peak"], {"u": .25, "S_grid_difference_MPa": 0,
                                                   "F_grid_difference_MPa": 3})
        self.assertEqual(result["peaks"]["F_minus_S_grid_difference"]["absolute_MPa"], 3)

    def test_rejects_invalid_displacement_or_pressure(self):
        for invalid in ([(0, 0), (0, 1)], [(0, 1), (1, float("nan"))], [(0, 0)]):
            curves = {key: [(0, 0), (1, 1)] for key in ("Sc", "Sf", "Fc", "Ff")}
            curves["Ff"] = invalid
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                reader.control(curves)


if __name__ == "__main__":
    unittest.main()
