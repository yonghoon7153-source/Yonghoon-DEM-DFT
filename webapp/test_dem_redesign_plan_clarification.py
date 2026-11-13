"""M32P-01/02: targeted prose contracts and dimensionless counterexamples.

No solver, physical qualification, source data, or external service is used.
These finite wording checks do not establish arbitrary prose consistency.
"""
import argparse
from fractions import Fraction as F
import hashlib
import html
import json
from pathlib import Path
import re
import unittest
import zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOC = Path('docs/reviews/dem_redesign_direction_20261109')
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def source():
    return (ROOT / DOC / 'plan_newcomer_ko.md').read_text(encoding='utf-8')


def section(text, number):
    matches = re.findall(r'^## ' + str(number) + r'\..*?(?=^## |\Z)', text, re.M | re.S)
    if len(matches) != 1:
        raise AssertionError('expected exactly one numbered section')
    return matches[0]


def assert_local(case, text, required, forbidden):
    for phrase in required:
        case.assertIn(phrase, text)
    for phrase in forbidden:
        case.assertNotIn(phrase, text)


class Clarification(unittest.TestCase):
    def test_contact_explanation_in_section4(self):
        assert_local(self, section(source(), 4),
                     ('별도의 접촉 법칙으로 풀지 않습니다', '보간 속도가 달라',
                      '거리가 변하거나', '지지 영역이 갈릴 수', '가설'),
                     ('그 순간부터 한 덩어리', '미끄러지지도 떨어지지도 못합니다'))

    def test_glossary_not_permanent_weld(self):
        rows = re.findall(r'^\| 붙음 \| (.+) \|$', section(source(), 11), re.M)
        self.assertEqual(len(rows), 1)
        assert_local(self, rows[0], ('수치적 속도 공유', '영구 용접', '뜻하지 않습니다'),
                     ('한 덩어리처럼 움직이는 것',))

    def test_unloading_reporting_not_zero_recovery(self):
        assert_local(self, section(source(), 3),
                     ('정량 보고', '분리·탈압 자격', '회복이 전혀 없다는 뜻은 아닙니다'),
                     ('떨어지지 못하기 때문입니다', '지금 MPM 으로 계산할 수 없습니다'))

    def test_calibration_is_not_validation(self):
        assert_local(self, section(source(), 10),
                     ('보정에 사용한 기준', '독립 검증이 되지는 않습니다'),
                     ('손잡이 하나로 값 하나는 늘 맞출',))
        assert_local(self, section(source(), 7),
                     ('탐색 실패와 보류', '적합 1 + 사전 고정 2', '값·출처는 미정'), ())

    def test_review_scopes_are_distinct(self):
        assert_local(self, section(source(), 8),
                     ('원 메모', 'M32R-01–06', 'M32P-01', 'M32P-02',
                      '재확인 대기', '전체 HOLD'), ())

    def test_generated_outputs_carry_corrections(self):
        h = (ROOT/'webapp/static/explain/dem_redesign_plan_newcomer_20261110.html').read_text(encoding='utf-8')
        h = html.unescape(re.sub(r'<[^>]+>', '', h))
        model = (ROOT/DOC/'plan_newcomer_docx_model.json').read_text(encoding='utf-8')
        with zipfile.ZipFile(ROOT/DOC/'DEM_redesign_plan_for_newcomers_20261110.docx') as z:
            x = ET.fromstring(z.read('word/document.xml'))
        docx = ''.join(t.text or '' for t in x.iter(W+'t'))
        for output in (h, model, docx):
            assert_local(self, output,
                         ('별도의 접촉 법칙으로 풀지 않습니다', '보간 속도가 달라',
                          '영구 용접', '보정에 사용한 기준', '재확인 대기',
                          '원 메모 = 문서 잔여 종결 가능'),
                         ('미끄러지지도 떨어지지도 못합니다',
                          '손잡이 하나로 값 하나는 늘 맞출 수'))

    def test_shared_nodes_allow_different_interpolated_velocity(self):
        def weight(distance):
            a = abs(distance)
            return F(3, 4)-a*a if a < F(1, 2) else (F(3, 2)-a)**2/F(2) if a < F(3, 2) else F(0)
        nodes = [F(0), F(1), F(2)]
        positions = [F(3, 5), F(9, 10)]
        weights = [[weight(x-n) for n in nodes] for x in positions]
        self.assertTrue(all(all(w > 0 for w in row) and sum(row) == 1 for row in weights))
        velocities = [sum(w*v for w, v in zip(row, nodes)) for row in weights]
        self.assertEqual(velocities, positions)
        moved = [x+v for x, v in zip(positions, velocities)]
        self.assertEqual(positions[1]-positions[0], F(3, 10))
        self.assertEqual(moved[1]-moved[0], F(3, 5))

    def test_one_parameter_can_have_unreachable_target(self):
        lower, upper = F(15, 100), F(16, 100)
        target = F(115, 1000)
        self.assertLess(target, lower)
        for theta in (F(0), F(1, 2), F(1)):
            y = lower + F(1, 100)*theta
            self.assertTrue(lower <= y <= upper)
            self.assertNotEqual(y, target)

    def test_section_locator_does_not_accept_witness_elsewhere(self):
        # A correct sentence elsewhere must not hide the reviewed wrong section.
        text = '## 4. Contact\nwrong\n## 5. History\n보간 속도가 달라\n'
        self.assertNotIn('보간 속도가 달라', section(text, 4))
        with self.assertRaises(AssertionError):
            section(text+'## 4. Duplicate\n', 4)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    if args.root:
        ROOT = args.root.resolve()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Clarification))
    report = {'methods': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
              'rc': int(not result.wasSuccessful()), 'source_sha256': hashlib.sha256(source().encode()).hexdigest(),
              'scope': 'targeted document assertions and dimensionless arithmetic, not physics or arbitrary semantic validation'}
    if args.report:
        with args.report.open('xb') as f:
            f.write((json.dumps(report, indent=2)+'\n').encode())
    raise SystemExit(report['rc'])
