"""Count executed subtests (passed + failed) per test method of scripts/test_mixer_d2_consumers.py.

unittest's normal output does not count passing subtests; this runner records every addSubTest call so
the README's subtest numbers are measured, not inferred from the test source.

Usage: python3 -I count_subtests.py <repo>/scripts <out.json>
"""
import collections
import json
import sys
import unittest


def main(scripts, out):
    sys.path.insert(0, scripts)
    import test_mixer_d2_consumers as t

    counts = collections.defaultdict(lambda: dict(subtests_pass=0, subtests_fail=0, tests_pass=0, tests_fail=0))

    class Result(unittest.TestResult):
        def addSubTest(self, test, subtest, outcome):
            super().addSubTest(test, subtest, outcome)
            counts[test._testMethodName]['subtests_fail' if outcome is not None else 'subtests_pass'] += 1

        def addSuccess(self, test):
            super().addSuccess(test)
            counts[test._testMethodName]['tests_pass'] += 1

        def addFailure(self, test, err):
            super().addFailure(test, err)
            counts[test._testMethodName]['tests_fail'] += 1

        def addError(self, test, err):
            super().addError(test, err)
            counts[test._testMethodName]['tests_fail'] += 1

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(t.D2Consumers)
    result = Result()
    suite.run(result)
    report = dict(tool='count_subtests.py', python=sys.version.split()[0], tests_run=result.testsRun,
                  failures=len(result.failures), errors=len(result.errors), methods=dict(sorted(counts.items())))
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
        f.write('\n')
    for name, c in sorted(counts.items()):
        print(name.ljust(52), c)
    print('tests run', result.testsRun, 'failures', len(result.failures), 'errors', len(result.errors))


if __name__ == '__main__':
    main(*sys.argv[1:])
