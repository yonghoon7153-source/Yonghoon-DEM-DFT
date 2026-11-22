from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import initial_support as s


class SupportTests(unittest.TestCase):
    def test_distinct_pair_and_distinct_node_counts(self):
        record = s.contacts(np.array([0, 0, 1, 1, 2]), np.array([0, 1, 0, 1, 0]),
                            np.ones(5), np.array([[0., 0.], [2., 0.], [0., 2.]]), 1., 2)
        self.assertEqual(record['shared_nodes'], 2)
        self.assertEqual(record['at_least_three_fields_nodes'], 1)
        self.assertEqual(record['unique_candidate_pairs'], 3)
        self.assertEqual(record['oblique_center_pairs'], 1)
        self.assertEqual(record['candidate_pair_node_entries'], 4)
        self.assertEqual(record['positive_geometric_gap_pairs'], 3)
        self.assertEqual(record['candidate_pair_node_entries_times_dx_squared'], 1.)

    def test_contact_threshold_is_strict(self):
        record = s.contacts(np.array([0, 1]), np.array([0, 0]), np.array([1., 1.e-14]),
                            np.array([[0., 0.], [1., 0.]]), 1., 1)
        self.assertEqual(record['unique_candidate_pairs'], 0)
        self.assertIsNone(record['largest_candidate_geometric_gap'])

    def test_candidate_can_be_touching(self):
        record = s.contacts(np.array([0, 1]), np.array([0, 0]), np.ones(2),
                            np.array([[0., 0.], [1., 0.]]),1.,1)
        self.assertEqual(record['positive_geometric_gap_pairs'], 0)
        self.assertEqual(record['largest_candidate_geometric_gap'], 0.)


if __name__ == '__main__':
    unittest.main()
