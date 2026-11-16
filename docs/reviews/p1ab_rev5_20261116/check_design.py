"""Revision-5 design-document regression only; never imports kit/engine code."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import unittest

A = "docs/reviews/dem_unloading_ps45_prereg_20261009.md"
B = "docs/reviews/p1_g2c_mpi_stage2_registration_20261112.md"
Q = "docs/reviews/codex_p1_g2c_ab_design_request_20261112.md"
ROOT = None

def section(text, heading):
    match = re.search(r"(?m)^" + re.escape(heading) + r"(?:[^\n]*)\n", text)
    if not match:
        raise AssertionError("missing active section: " + heading)
    level = len(heading) - len(heading.lstrip("#"))
    lines = []
    fenced = False
    for line in text[match.end():].splitlines(keepends=True):
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and re.match(r"^#{1," + str(level) + r"} ", line):
            break
        lines.append(line)
    return "".join(lines)

class DesignRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a, cls.b, cls.q = ((ROOT / p).read_text(encoding="utf-8") for p in (A, B, Q))

    def test_01_reread_is_not_publication(self):
        s = section(self.a, "### 15-5c.")
        for clause in ("기본 restore = stdout 보고만", "잡 폴더에 쓰기 0", "--publish-new",
                       "기존 증서 바이트 보존", "기존 영수증 바이트 보존"):
            self.assertIn(clause, s)
        self.assertIn("SYNTAX_FAIL", s)
        self.assertIn("UNCONFIRMED", s)
        self.assertNotIn("reread_<시각>", s)  # no uncontrolled new sibling output

    def test_02_publication_failure_and_collision(self):
        s = section(self.a, "### 15-5c.")
        for clause in ("배타적 새 파일", "symlink", "동시 두 발행", "부분 쓰기",
                       "reader_rc=0 금지", "증서 없는 다시 읽기"):
            self.assertIn(clause, s)
        self.assertIn("동시 두 발행은 최대 한 개만 성공해야 한다.", s)
        self.assertIn("검사 후 덮어쓰는 open(w)/replace 방식 금지.", s)

    def test_03_raw_id_tokens(self):
        s = section(self.a, "### 15-2.")
        for token in ("ID_COLS", "c_ul_ph[7]", "c_ul_ph[8]", "_id_value",
                      "9007199254740993", "2.0000000000000001", "float 변환 전"):
            self.assertIn(token, s)
        self.assertIn("`9007199254740993` · `2.0000000000000001`은 두 열 각각 거부", s)

    def test_04_binding_duplicates_and_hash_shape(self):
        s = section(self.a, "### 15-5d.")
        for token in ("job_dir", "rt1_bin", "rt2_ckpt", "각각 정확히 한 줄",
                      "[0-9a-f]{64}", "read_kv 사용 금지", "같은 값 중복",
                      "SYNTAX_FAIL", "UNCONFIRMED", "파일 존재 검사보다 먼저"):
            self.assertIn(token, s)
        self.assertIn("기술 실패·결합 중복/잘못된 형식/서로 다른 경로·해시가 확인되면 SYNTAX_FAIL이 우선.", s)

    def test_05_mpi_attempt_scope(self):
        s = section(self.b, "## 5.")
        for token in ("N ∈ {200, 40000}", "N 39900", "attempt 줄 앞",
                      "G2CP_LEDGER", "고정 기본 경로", "ledger_override"):
            self.assertIn(token, s)
        self.assertIn("N 39900 등 그 밖은 attempt 줄 앞 rc 3 (reason=n_scope).", s)
        self.assertIn("기존 기본값과 같은 글자만 허용; 우회 값은 reason=ledger_override,", s)
        s = section(self.b, "## 8.")
        self.assertIn("#SBATCH --no-requeue", s)
        self.assertIn("n ∉ {200, 40000} = 어긋남", s)
        self.assertIn("자동 재큐", s)
        self.assertIn("같은 잡 번호", s)
        self.assertIn("정직한 복구라도 어긋남 → 그 NP 결론 없음;", s)
        self.assertIn("attempt 이전의 재큐는 이 장부만으로 검출하지 못한다.", s)
        self.assertIn("독립 재큐 이력 증거의 원천·필드·보존 규약", s)
        self.assertIn("미확정이면 B 현장 GO 보류", s)
        self.assertIn("증거 누락이면 그 NP 결론 없음", s)

    def test_06_fixture_pair_only_growth(self):
        s = section(self.a, "### 15-2.")
        line = next(x for x in s.splitlines() if x.startswith("| 기존 시험 — 판독기"))
        self.assertIn("쌍 덤프만 키움", line)
        self.assertIn("원자 덤프 그대로", line)
        self.assertIn("pre_bot", line)
        self.assertNotIn("원자 덤프 (원 · R/g2 · RT) 에 그 원자를 같은 자리로", line)

    def test_07_shear_scope(self):
        s = section(self.a, "### 15-8.")
        self.assertIn("deltaMax 단독 어긋남은 못 봄", s)
        self.assertIn("shear (접선) 이력의 거친 소실만", s)
        self.assertIn("setup", s)

    def test_08_observation_deck(self):
        s = section(self.a, "### 15-4.")
        atom = next(x for x in s.splitlines() if x.startswith("dump ul_ra "))
        fmt = next(x for x in s.splitlines() if x.startswith("dump_modify ul_ra "))
        fields = atom.split("rt_atom_*.dump ", 1)[1].split()
        formats = fmt.split('format "', 1)[1].rstrip('"').split()
        self.assertEqual(len(fields), 16)
        self.assertEqual(formats, ["%d", "%d"] + ["%.17g"] * 14)
        self.assertEqual(fields[-4:], [f"f_history_zwall_bot[{i}]" for i in range(1, 5)])
        wall = next(x for x in s.splitlines() if x.startswith("dump ul_rw "))
        self.assertIn("${out}/obs/rt_wall_*.dump", wall)
        self.assertEqual(wall.split("rt_wall_*.dump ", 1)[1].split(),
                         [f"c_ul_wh[{i}]" for i in range(1, 11)])
        self.assertIn("undump ul_rw", s)
        self.assertIn("compute ul_wh all wall/gran/local id history force_normal", s)

    def test_09_fixture_and_stage_rules(self):
        s = section(self.a, "### 15-4b.")
        self.assertIn("10–56", s)
        self.assertNotIn("10–54", s)
        self.assertIn("접두별", s)
        self.assertIn("obs/", s)
        self.assertIn("fixture 머리 = 생산 R 머리", section(self.a, "### 15-4."))
        s = section(self.a, "### 15-2.")
        self.assertIn("RT1 실패면 RT2 안 돎 (stage=RT2 skipped 한 줄)", s)

    def test_10_history_hashes_are_current_blobs(self):
        for text in (self.a, self.b):
            s = section(text, "### 15-14.") if text is self.a else section(text, "## 15.")
            pairs = re.findall(r"\| `([^\`]+\.md)` \| `([0-9a-f]{64})` \|", s)
            self.assertEqual(len(pairs), 4)
            for path, digest in pairs:
                self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest)
            self.assertIn("스크래치 판", s)
        self.assertIn("별도 후속 개정", section(self.a, "### 15-7."))
        self.assertNotIn("개정 5", section(self.a, "### 15-7."))

    def test_11_request_scope_and_pending_verdict(self):
        first = self.q.split("## 0.", 1)[0]
        self.assertIn("이번에 닫는 것", first)
        self.assertIn("닫지 않는 것", first)
        self.assertIn("외부 판정 미수령", first)
        line = next(x for x in self.q.splitlines() if x.startswith("| Q2"))
        self.assertIn("N 하한 밖", line)
        self.assertIn("UNCONFIRMED 24/24", line)
        self.assertIn("SR5-01–08", self.q)
        self.assertIn("B 구현 전", first)
        self.assertNotIn("A (개정 4)", self.q)
        self.assertNotIn("C12 중력 팔 (개정 5)", self.q)

    def test_12_guard_thresholds_preserved(self):
        s = section(self.a, "### 15-5b.")
        # Parse active inequalities, not occurrences in nearby historical examples.
        for pattern, expected in (
            (r"전역 W ≤ \*\*([0-9.]+)\*\* ∧", "0.05"),
            (r"쓴 격자 칸별 안쪽 W 최대 ≤ ([0-9.]+)\*\*", "0.5"),
            (r"칸마다 안쪽 하중 쌍 ≥ \*\*([0-9]+)\*\*", "100"),
        ):
            self.assertEqual(re.findall(pattern, s), [expected])
        for token in ("VALUE_MISMATCH", "UNCONFIRMED"):
            self.assertIn(token, s)
        s = section(self.b, "## 9.")
        self.assertIn("NP 마다 2 시도", s)
        self.assertIn("칸 하나라도", s)
        self.assertIn("새 등록", s)

    def test_13_historical_and_synthetic_cell_expectations(self):
        s = section(self.a, "### 15-10.")
        cell_row = next(line for line in s.splitlines() if line.startswith("| 쓴 격자 칸별 막이"))
        for token in ("역사 6×4·11×1 정직 B/C = UNCONFIRMED", "나머지 세 격자 = PASS",
                      "모든 칸 N≥100인 새 합성 fixture", "VALUE_MISMATCH"):
            self.assertIn(token, cell_row)
        self.assertNotIn("샌드박스 다섯 격자 · 칸 최대 0.0604) → 통과해야", cell_row)
        expected = {
            "N99_EQUAL": "UNCONFIRMED", "N100_EQUAL": "PASS",
            "N99_RESET_ONE": "UNCONFIRMED", "N100_RESET_ONE": "VALUE_MISMATCH",
            "N99_VALID_OTHER": "VALUE_MISMATCH", "N99_GLOBAL": "VALUE_MISMATCH",
        }
        for name, status in expected.items():
            row = next(line for line in s.splitlines() if line.startswith("| " + name + " |"))
            self.assertEqual(row.split("|")[-2].strip(), status)
        global_row = next(line for line in s.splitlines() if line.startswith("| 이력 소실 막이"))
        self.assertIn("전역 W 단독 통과; 전체 판정은 칸 N 조건 포함", global_row)
        self.assertIn("유효 N≥100", section(self.a, "### 15-8."))

    def test_14_active_revision_scope_and_checks(self):
        active = self.a[self.a.index("## 15."):]
        self.assertNotIn("⛔ 개정 4 §15", active)
        self.assertIn("⛔ 개정 5 §15", active)
        scope = section(self.a, "### 15-13.")
        self.assertNotIn("C12 중력 팔 (개정 5)", scope)
        self.assertIn("C12 중력 팔 (별도 후속 개정)", scope)
        row = next(line for line in self.q.splitlines() if line.startswith("- 리포 검사:"))
        self.assertNotIn("이 요청서 커밋에서 실패 0", row)
        for token in ("과거 작성 측 기록", "핀 미확인", "5ae5acdd5e77", "12/12",
                      "참조 rc1", "96", "원장 rc0", "전체 gate 미실행"):
            self.assertIn(token, row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    ROOT = args.root.resolve()
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DesignRegression))
    report = {"scope": "design_document_contract_only", "methods": result.testsRun,
              "failures": len(result.failures), "errors": len(result.errors),
              "skipped": len(result.skipped), "research_results": 0,
              "kit_implementation_verified": False,
              "documents": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                            for p in (A, B, Q)}}
    if args.report:
        with args.report.open("x", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            f.write("\n")
    raise SystemExit(0 if result.wasSuccessful() else 1)
