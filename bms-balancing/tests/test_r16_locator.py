"""R16 — 조건 8 축 ⑤ + C34: locator 무결성에 **소비자**를 붙인다 (2026-09-16).

두 줄이 같은 일을 가리킨다:

  C34   `receipt_paths` 에 production 소비자가 **0** 이다 — 원장·요청문은 "역할별 path 를 드러낸다" 고
        적었는데 실제로는 아무도 안 읽는다. 드러내기만 하고 소비하지 않으면 그 필드는 장식이다.
  축 ⑤  "확장자·sheet·parser 선택처럼 **해석을 바꾸는** locator 는 semantic identity" — receipt 에
        role→path 는 있지만 **parser selector 를 별도 필드로 묶지는** 않았다.

경계는 리뷰어가 정했다 (R12 Q2 → R13 Q5 답): **경로를 digest 에 넣지 않는다** — 그것은 R6 F1/F4 의
의도된 결정이고(같은 bytes 면 같은 실행; 이름만 다른 사본은 같은 digest), 넣으면 byte 가 같은
재-export 가 다른 실행으로 읽힌다. 대신 **정보로 표시**한다.

그래서 이 라운드가 가르는 것은 **둘**이다:

  경로만 다르다 (같은 bytes·같은 파서)        → **정보 줄**. rc 를 바꾸지 않는다 (Q5 답 그대로)
  파서 선택이 다르다 (확장자/reader 가 다르다)  → **실행 조건 불일치**. 같은 bytes 라도 다르게 읽힌다

둘째가 핵심이다: `x.csv` 와 `x.xlsx` 는 우리 로더에서 **다른 함수**가 읽는다. 같은 digest 를 가진
두 실행이 서로 다른 파서를 탔다면 그것은 "같은 실행의 재현" 이 아니다.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
from bms_balancing import schema as S          # noqa: E402

_CI = {"half_cell": {"path": "d/half.xlsx", "sha256": "1" * 64},
       "full_cell": {"path": "d/full.xlsx", "sha256": "2" * 64},
       "literature": {"gr": {"path": "d/gr.xlsx", "sha256": "3" * 64},
                      "si": {"path": "d/si.csv", "sha256": "4" * 64}}}


def test_r16_41_locators_name_the_parser_not_just_the_path():
    """[R16-41 · 축 ⑤] 역할마다 **어떻게 읽혔는지**가 드러나야 한다 — 경로만으로는 해석이 안 보인다."""
    loc = S.receipt_locators(_CI)
    assert set(loc) == set(S.receipt_paths(_CI)), (sorted(loc), sorted(S.receipt_paths(_CI)))
    assert loc["literature.si"]["reader"] != loc["literature.gr"]["reader"], loc
    assert loc["literature.si"]["ext"] == ".csv" and loc["literature.gr"]["ext"] == ".xlsx", loc
    assert loc["half_cell"]["path"] == "d/half.xlsx", loc
    # 모르는 확장자를 **추측하지 않는다** — 모른다고 적는다 (부재는 안전값이 아니다)
    odd = S.receipt_locators({"half_cell": {"path": "d/x.bin", "sha256": "5" * 64}})
    assert odd["half_cell"]["reader"] == "unknown", odd


def test_r16_42_the_digest_still_ignores_the_path(tmp_path):
    """[R16-42] 이 라운드가 **깨면 안 되는 것**: 경로는 여전히 digest 밖이다 (R6 F1/F4 의 의도된 결정).

    locator 를 다루기 시작했다고 경로를 identity 로 승격시키면, byte 가 같은 재-export 가 다른 실행이
    된다 — `test_i6p_04` 가 고정한 축이다.
    """
    moved = json.loads(json.dumps(_CI))
    moved["half_cell"]["path"] = "전혀/다른/곳/half.xlsx"
    assert S.inputs_digest(moved) == S.inputs_digest(_CI), "경로가 digest 를 바꿨다"


def _bundle(tmp_path, tag, rid, mutate=None):
    from bms_balancing import verify as V                  # noqa: PLC0415
    from test_r7_codex import _sign                        # noqa: PLC0415
    from test_r8_codex import _full_matrix_rows            # noqa: PLC0415
    d = tmp_path / tag; d.mkdir()
    f = d / "matrix_100.csv"
    rows = _full_matrix_rows(rid)
    if mutate:
        for r in rows:
            for col in ("consumed_inputs", "ref_consumed_inputs"):
                if r.get(col):
                    r[col] = json.dumps(mutate(json.loads(r[col])), ensure_ascii=False)
    V.atomic_write_csv(f, rows, list(rows[0]))
    _sign(f, rid, "100", full=True)
    return d


def _run(new, old):
    r = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(new), "--old", str(old)],
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    line = next(l for l in r.stdout.splitlines() if l.startswith("PROMOTION "))
    return r.returncode, json.loads(line[len("PROMOTION "):]), r.stdout


def test_r16_43_a_moved_input_is_reported_as_information_not_as_a_blocker(tmp_path):
    """[R16-43 · C34] 경로만 바뀌면 **정보 줄**이다 — rc 도 blocker 도 바꾸지 않는다 (R13 Q5 답 그대로).

    소비자가 **있다**는 것이 C34 의 요구였다. 없으면 `receipt_paths` 는 아무도 안 읽는 필드다.
    """
    def move(ci):
        ci["half_cell"]["path"] = "다른/곳/" + ci["half_cell"]["path"].split("/")[-1]
        return ci
    old = _bundle(tmp_path, "old", "r16-loc-old")
    new = _bundle(tmp_path, "new", "r16-loc-new", mutate=move)
    rc, promo, out = _run(new, old)
    assert "locator" in out or "경로가 바뀌었다" in out, ("소비자가 없다 — C34 그대로다", out[-1200:])
    assert promo["blocked_by"]["controls"] == 0 and promo["blocked_by"]["inputs"] == 0, promo["blocked_by"]
    assert rc in (0, 4), ("경로 이동이 rc 를 바꿨다 — 정보여야 한다", rc, out[-1200:])


def test_r16_44_a_different_parser_on_the_same_bytes_is_a_condition_mismatch(tmp_path):
    """[R16-44 · 축 ⑤] 같은 bytes 를 **다른 파서**로 읽었으면 그것은 같은 실행의 재현이 아니다.

    `x.csv` 와 `x.xlsx` 는 우리 로더에서 다른 함수가 읽는다 — digest 는 같아도 해석이 다르다.
    이것이 "해석을 바꾸는 locator 는 semantic identity" 의 최소선이다.
    """
    def repar(ci):
        ci["literature"]["si"]["path"] = ci["literature"]["si"]["path"].replace(".csv", ".xlsx")
        return ci
    old = _bundle(tmp_path, "old", "r16-par-old")
    new = _bundle(tmp_path, "new", "r16-par-new", mutate=repar)
    rc, promo, out = _run(new, old)
    assert promo["blocked_by"]["controls"] > 0, ("파서가 바뀐 것이 안 잡혔다", promo["blocked_by"], out[-1200:])
    assert "reader" in out or "파서" in out, out[-1200:]
    assert promo["promotion_eligible"] is False, promo
