"""Small, manual transcriptions of memo rules; NOT a production decision engine.

Text witnesses bind each interpretation to the supplied memo. Passing verifies
these cases and witnesses, not arbitrary prose equivalence or physical truth.
The previous report-only/missing-data paths model the permissive interpretation
identified by review; they are not claims about executed production software.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import unittest

P = argparse.ArgumentParser()
P.add_argument('--memo', type=Path, required=True)
P.add_argument('--report', type=Path, required=True)
ARGS = P.parse_args()
TEXT = ARGS.memo.read_text(encoding='utf-8')
LINES = TEXT.splitlines()
OLD_SHA = '2faf58241c7d657e1bda97ac1dc3fcf4b0619bac0fe814c844242eca9188cbe0'
DIGEST = hashlib.sha256(ARGS.memo.read_bytes()).hexdigest()
BODY, APP = TEXT.split('## 부록 D.', 1)
def line(prefix):
    rows = [x for x in LINES if x.startswith(prefix)]
    assert len(rows) == 1, prefix
    return rows[0]

CAP_NEW = '못 닿음 = 목표점 응력 미확정' in line('- 팔의 구간')
DENSE_NEW = '위반 하나라도 → 문 불합격' in line('| U6 |')
BOX_NEW = '필수 비교 집합 완전성' in line('  - 하는 일.')
if not (CAP_NEW and DENSE_NEW and BOX_NEW):
    # Mixed candidates are allowed for mutation checks, but unrecognized prose
    # must never quietly select old semantics.
    assert CAP_NEW or '못 닿음 = [ln 상한 , +∞)' in line('- 팔의 구간')
    assert DENSE_NEW or '응력 차를 보고한다.' in line('| U6 |')
    assert BOX_NEW or '최종 상자의 S 짝이 걸은 σ_y 점도 모두 돈다' in line('  - 하는 일.')

def grade(intervals):
    a, b = math.log(1.15), math.log(1.3)
    lows, highs = zip(*intervals)
    if all(x >= a for x in lows) and sum(lows)/3 >= b: return 'DIFFERENT'
    if all(lo >= -b and hi <= b for lo,hi in intervals) and sum(lows)/3 >= -a and sum(highs)/3 <= a: return 'SAME'
    if all(x <= -a for x in highs) and sum(highs)/3 <= -b: return 'REVERSE'
    return 'MIDDLE'

def point(pairs):
    # Synthetic inputs are already valid, finite positive point stresses.
    if CAP_NEW and any('cap' in (s,f) for s,f in pairs): return 'MIDDLE'
    if any(s == f == 'cap' for s,f in pairs): return 'DISCARD'
    iv=[]
    for s,f in pairs:
        si = (math.log(2.4), math.inf) if s == 'cap' else (math.log(s)-.02, math.log(s)+.02)
        fi = (math.log(2.4), math.inf) if f == 'cap' else (math.log(f)-.02, math.log(f)+.02)
        iv.append((si[0]-fi[1],si[1]-fi[0]))
    return grade(iv)

def cap_band(): return 'UNDETERMINED' if CAP_NEW else 'OUT'

def dense(violations, registered=True, complete=True):
    if DENSE_NEW and (not registered or not complete or any(violations)): return 'HOLD'
    return 'PASS'  # old permissive reading: report (c), (a)/(b) passed

def box(rows, required, context, f_hold=False, box_effect=False):
    fallback = 'S-soft' if context == '4-ii' else 'AUTHOR'
    # Observation schema here is synthetic; all keys are (arm, sigma, fill).
    complete = bool(required) and len(rows)==len(required) and len(set(k for k,v in rows))==len(rows)
    complete = complete and {k for k,v in rows}==set(required)
    complete = complete and all(type(v) in (int,float) and math.isfinite(v) for k,v in rows)
    if f_hold: return ('F-HOLD',fallback)
    if BOX_NEW and not complete: return ('F-COMPARISON-UNKNOWN',fallback)
    if box_effect: return ('F-BOX',fallback)
    return ('F-i','F-real')  # synthetic F-real crosses; other guards assumed pass

class ContractChecks(unittest.TestCase):
    def test_cap_nonmonotone_same_prefix(self):
        phi=.94
        self.assertLess(phi+.002,.95)
        self.assertAlmostEqual(math.exp(math.log(2.4)-.02),2.352476815936,places=11)
        self.assertEqual(grade([(math.log(.6),math.log(.6))]*3),'REVERSE')
        self.assertEqual(point([('cap',1.)]*3),'MIDDLE')

    def test_cap_band_not_out(self):
        self.assertEqual(cap_band(),'UNDETERMINED')

    def test_section6_rule38_rejects_cap_target_bound(self):
        # M32RF-01: inspect the active prohibition list itself. The older
        # body/appendix witnesses do not cover this separate rule.
        section = TEXT.split('## 6.', 1)[1].split('## 7.', 1)[0]
        rules = [s for s in section.splitlines() if s.startswith('38. ')]
        self.assertEqual(len(rules), 1)
        rule = rules[0]
        self.assertIn('목표점 응력 미확정', rule)
        self.assertIn('목표점 응력의 한쪽 경계를 만들지 않는다', rule)
        self.assertIn('해당 점은 중간 (미도달)', rule)
        self.assertIn('해당 F 띠 점은 미정', rule)
        self.assertNotIn('[ln 상한', rule)
        self.assertNotIn('확인될 때만이다', rule)

    def test_cap_both_and_mixed_never_discard_or_infer(self):
        for pairs in [[('cap','cap')]*3, [(1.,'cap')]*3, [('cap',1.),(1.,1.),(1.,1.)]]:
            with self.subTest(pairs=pairs): self.assertEqual(point(pairs),'MIDDLE')

    def test_observed_points_preserved(self):
        for ratio, expected in [(1.,'SAME'),(1.5,'DIFFERENT'),(.6,'REVERSE'),(1.2,'MIDDLE')]:
            with self.subTest(ratio=ratio): self.assertEqual(point([(ratio,1.)]*3),expected)

    def test_dense_energy_and_momentum_counterexample(self):
        before=[1.,-1.,0.];after=[1.1,-1.1,0.]
        self.assertEqual(sum(before),sum(after))
        self.assertAlmostEqual(sum(v*v/2 for v in after),1.21)
        self.assertEqual(dense([True]),'HOLD')

    def test_dense_each_obligation(self):
        for idx in range(8):
            flags=[False]*8;flags[idx]=True
            with self.subTest(obligation=idx): self.assertEqual(dense(flags),'HOLD')

    def test_dense_missing_registration_or_observation(self):
        self.assertEqual(dense([False]*8,registered=False),'HOLD')
        self.assertEqual(dense([False]*8,complete=False),'HOLD')
        self.assertEqual(dense([False]*8),'PASS')

    def test_required_box_point_outside_own_walk(self):
        required=[('soft','.18',1),('soft','.12',1)]
        rows=[(required[0],.8),(required[1],None)]
        for ctx,following in [('4-ii','S-soft'),('4-iii','AUTHOR')]:
            with self.subTest(context=ctx): self.assertEqual(box(rows,required,ctx),('F-COMPARISON-UNKNOWN',following))

    def test_box_missing_duplicate_nonfinite(self):
        keys=[('soft','.12',1),('soft','.12',2)]
        for rows in [[],[(keys[0],.8)],[(keys[0],.8)]*2,[(keys[0],.8),(keys[1],float('nan'))],[(keys[0],.8),(keys[1],float('inf'))],[(keys[0],.8),(keys[1],{'valid':False,'leftover':.8})]]:
            with self.subTest(rows=rows): self.assertEqual(box(rows,keys,'4-ii')[0],'F-COMPARISON-UNKNOWN')

    def test_box_complete_and_other_guards_preserved(self):
        keys=[('soft','.12',1),('soft','.12',2)];rows=[(k,.8) for k in keys]
        self.assertEqual(box(rows,keys,'4-ii'),('F-i','F-real'))
        self.assertEqual(box(rows,keys,'4-iii',box_effect=True),('F-BOX','AUTHOR'))
        self.assertEqual(box([],keys,'4-ii',f_hold=True,box_effect=True),('F-HOLD','S-soft'))

    def test_O7_has_explicit_law_qualifier(self):
        # Same three-node stencil, linear nodal velocity gives unequal G2P
        # velocities: gap .3 -> .6. This is not a traction-free contact law.
        self.assertAlmostEqual((.9+.9)-(.6+.6),.6)
        self.assertIn('| 명시적 분리 법칙 없음 |',line('| O7 |'))

    def test_M0_common_policy(self):
        self.assertIn('적합 1',line('| **M0**'))
        self.assertIn('사전 고정 2',line('| **M0**'))
        self.assertNotIn('M0 = 셋 (모두 적합)',BODY)

    def test_LA25_timing_in_both_summaries(self):
        a=line('- **랩 표준과 다른 문헌 값')
        b=line('- 무엇 (값):')
        for summary in (a,b):
            with self.subTest(summary=summary[:20]):
                for token in ('약 6 시간','Cu 포일 제거','카드 해석'):
                    self.assertIn(token,summary)
        self.assertAlmostEqual(1-(1-.024)/1.01,.03366336633663369)

    def test_body_appendix_rule_witnesses(self):
        for body, appendix in [
            ('못 닿음 = 목표점 응력 미확정','못닿음  목표점 응력 미확정 → 점 중간'),
            ('위반 하나라도 → 문 불합격','U6(c) 문 불합격 → 단계 3 / 3D F 판정 중단'),
            ('필수 비교 집합 완전성','필수비교 미완전 → F-비교미확정'),
        ]:
            with self.subTest(body=body):
                self.assertIn(body,BODY);self.assertIn(appendix,APP)

suite=unittest.defaultTestLoader.loadTestsFromTestCase(ContractChecks)
result=unittest.TextTestRunner(verbosity=2).run(suite)
report={'scope':'manual document-contract regression, not production/physical tests',
        'memo_sha256':DIGEST,'original_reviewed_memo':DIGEST==OLD_SHA,
        'methods':result.testsRun,'failed_methods':len({t.id().split(' ')[0] for t,_ in result.failures}),
        'failure_observations':len(result.failures),'errors':len(result.errors),
        'successful':result.wasSuccessful()}
ARGS.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if result.wasSuccessful() else 1)
