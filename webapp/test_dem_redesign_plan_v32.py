"""Memo 3.2 communication regression; document bytes only, no research inputs."""
import argparse
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DOC = Path('docs/reviews/dem_redesign_direction_20261109')
SOURCES = ('briefing_ko.md', 'plan_newcomer_ko.md')
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
WITNESSES = ('메모 3.2', 'M32R-01–06', 'M32RF-01', '전체 HOLD',
             '목표점 응력', '미확정', 'U6(c)', '필수 비교', 'F-비교미확정',
             '명시적 분리 법칙 없음', '적합 1', '사전 고정 2', 'Cu 포일')


def source(name):
    return (ROOT / DOC / name).read_text(encoding='utf-8')


class Content32(unittest.TestCase):
    def both(self, required, forbidden=()):
        for name in SOURCES:
            text = source(name)
            for item in required:
                with self.subTest(source=name, required=item):
                    self.assertIn(item, text)
            for item in forbidden:
                with self.subTest(source=name, forbidden=item):
                    self.assertNotIn(item, text)

    def test_current_source_and_date(self):
        self.both(('<!-- BRIEFING:UPDATED 2026-11-13 -->', '메모 3.2', '5afa16488'),
                  ('방향 메모 3.1 판', '3.2 는 판정을 받은 뒤'))

    def test_scoped_closure_not_execution(self):
        self.both(('M32R-01–06', 'M32RF-01', '문서 범위', '종결 가능', '전체 HOLD',
                   'DRD-01', '물리 자격', '자동 승격'))

    def test_cap_does_not_bound_target(self):
        self.both(('목표점 응력', '미확정', '한쪽 경계', '해당 F 띠 점', '미정'))

    def test_dense_contact_is_a_gate(self):
        self.both(('U6(c)', '위반', '중단', '등록', '누락', '보류'))

    def test_missing_box_comparison_not_discarded(self):
        self.both(('필수 비교', 'F-비교미확정', '결측', '제외하지', 'F 채택'))

    def test_separation_and_parameter_accounting(self):
        self.both(('명시적 분리 법칙 없음', '적합 1', '사전 고정 2', '값·출처'))

    def test_literature_state_not_relabelled(self):
        self.both(('약 6 시간', '운전압 시험', 'Cu 포일', '압밀 직후', '옮기지'))

    def test_conditional_2d_and_registration(self):
        self.both(('등록한 2D 조건', '3D', '보편 수렴', '실행 승인'))
        self.assertNotIn('붙음이 주원인.', source('briefing_ko.md'))
        self.assertNotIn('붙음은 주원인 아님.', source('briefing_ko.md'))

    def test_generated_html_witnesses(self):
        for name in ('dem_redesign_plan_20261110.html', 'dem_redesign_plan_newcomer_20261110.html'):
            raw = (ROOT/'webapp/static/explain'/name).read_text(encoding='utf-8')
            text = html.unescape(re.sub(r'<[^>]+>', '', raw))
            for item in WITNESSES:
                with self.subTest(page=name, required=item):
                    self.assertIn(item, text)

    def test_docx_witnesses_and_pinned_memo(self):
        with zipfile.ZipFile(ROOT/DOC/'DEM_redesign_plan_for_newcomers_20261110.docx') as z:
            xml = ET.fromstring(z.read('word/document.xml'))
        text = ''.join(t.text or '' for t in xml.iter(W+'t'))
        for item in WITNESSES:
            with self.subTest(required=item): self.assertIn(item, text)
        self.assertEqual(hashlib.sha256((ROOT/DOC/'memo_v3_2.md').read_bytes()).hexdigest(),
                         '1724056626d78db6477bf3bc3213447c94527ea1621ed10cbc6c30e25ca5aaf0')

    def test_status_requires_evidence_and_preserves_legacy(self):
        spec = importlib.util.spec_from_file_location('plan_v32_builder', ROOT/'scripts/build_dem_redesign_plan.py')
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        current = source('plan_newcomer_ko.md')
        doc = mod.parse(current, 'current.md', extended=True)
        self.assertEqual(mod._newcomer_status_line(doc)[-1], '외부 검토 = 문서 잔여 종결 가능, 전체 HOLD')
        for missing in ('전체 HOLD', '문서 범위 종결 가능'):
            with self.subTest(missing=missing), self.assertRaises(mod.ParseError):
                mod._newcomer_status_line(mod.parse(current.replace(missing, '근거 누락'), 'missing.md', extended=True))
        fixture = (ROOT/'webapp/test_fixtures/dem_redesign_plan/fixture_ko.md').read_text(encoding='utf-8')
        legacy = mod.parse(fixture, 'legacy.md', extended=True)
        self.assertEqual(mod._newcomer_status_line(legacy)[-1], '외부 검토 = 방향은 맞음, 판정 규칙은 고치는 중')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.root: ROOT = args.root.resolve()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Content32)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    data = {'methods': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
            'failed_methods': len({t.id().split(' (')[0] for t, _ in result.failures}),
            'rc': 0 if result.wasSuccessful() else 1,
            'scope': 'document communication, HTML and DOCX; not physical qualification'}
    if args.report:
        with args.report.open('xb') as f: f.write((json.dumps(data, indent=2)+'\n').encode())
    raise SystemExit(data['rc'])
