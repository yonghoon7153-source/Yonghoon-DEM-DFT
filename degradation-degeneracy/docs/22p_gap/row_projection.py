"""warm-probe 다리의 **행 수준 감사 투영**을 만든다 — 21차 리뷰 발견 6·7.

왜 필요한가
-----------
21차 리뷰가 확인할 수 있었던 것은 이것뿐이다:

    문서 숫자 == 커밋된 summary 숫자
    summary 가 적은 fits digest == manifest 가 적은 fits digest

확인할 수 **없던** 것:

    봉인 fits 를 직접 재계산한 summary == 커밋된 summary
    조건별 결과와 restart trace 가 aggregate 숫자를 실제로 만들었는가
    복원 후 validate → score → analyze 가 같은 값을 내는가

원자료(`fits.parquet`)는 다리당 수십 MB 라 git 에 못 넣는다. 리뷰가 제시한
대안이 **compact keyed projection + full digest** 다. 이 스크립트가 그것을
만든다:

    cond_id · objective · truth · hats · J · degenerate · restart-source

그리고 같은 실행에서 **재계산 검증**을 한다 — 원자료를 `src.scoring` 의
정규 경로로 다시 채점해서 봉인 summary 와 자리별로 대조한다. 이것이
"복원 후 score → analyze 가 같은 값을 내는가" 에 대한 답이다.

RUN_SCOPE 밖이다
----------------
`docs/` 에 둔다 (`leg_probe.py` 와 같은 이유). `source_digest` 는
`src/ tools/ configs/ scripts/ run.sh requirements*` 만 보므로 이 파일을
추가·수정해도 기존 산출물의 code identity 가 안 바뀐다. 단계 3 에서 정식
도구로 `tools/` 에 옮길 때 그때 digest 가 바뀐다.

읽기 전용이다 — `results/` 를 건드리지 않는다.

사용법
------
    python docs/22p_gap/row_projection.py <leg> [<leg> ...]
    python docs/22p_gap/row_projection.py --all      # warm_probe 의 8다리

출력: `docs/22p_gap/warm_probe/<leg>.projection.csv.gz`
      `docs/22p_gap/warm_probe/<leg>.projection.yaml`
"""
from __future__ import annotations

import argparse
import os
import shutil
import time
import tempfile
import uuid
import gzip
import math
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))

WARM = REPO / "docs" / "22p_gap" / "warm_probe"
RESULTS = REPO / "results"

#: 투영에 담는 열과 순서. **순서가 digest 의 일부**다 — 바꾸면 digest 가 바뀐다.
#: 리뷰가 지정한 최소 집합(cond_id, objective, truth, hats, J, degenerate,
#: restart-source)에 귀속 판단에 필요한 축(noise·예산·warm·경계)을 더했다.
COLUMNS = [
    "cond_id", "objective", "noise",
    "lli", "lam_pe", "lam_ne",                       # truth
    "lli_hat", "lam_pe_hat", "lam_ne_hat",           # hats
    "J", "abs_err_max", "degenerate", "recoverable",
    "n_restarts", "n_restarts_agree", "warm_started",
    "converged", "any_bound_active",
    "best_restart_source", "restart_sources",
]

#: restart 수준 투영의 열. 여기까지 있어야 random-only 다봉성을 투영에서
#: **독립 재계산**할 수 있다 (22차 발견 5).
RESTART_COLUMNS = ["cond_id", "objective", "i", "source", "J",
                   "p0", "p1", "p2", "p3", "warm"]

#: 두 감사 경로가 **공유하는** semantic view. 비교 전에 양쪽에서 떼는 키다.
#:
#: ★ 28차 P1-4 — `make_receipt` 는 `_F4_주의` 를 다시 넣었는데 여기 비교기는
#:   계속 떼고 있었다. 봉인 summary 의 인용 금지 경고를 "안전" 으로 바꿔도
#:   `재계산_검증.전체_일치` 에 diff 가 안 생겼다. 두 audit 경로의 semantic
#:   계약이 또 갈린 것이다. **한 곳에서 정의하고 양쪽이 import 한다.**
#:
#: `_채점원본` 만 남는다 — `run_scoring` 이 붙이는 실행 메타라 재채점이 만들
#: 수 없다. 그 안의 인용 안전 flag 는 `make_receipt._citation_safety` 가
#: 값으로 검사한다.
SEMANTIC_SKIP = ("_채점원본",)

#: 이 투영이 무엇을 어떻게 만들었는지 — 바뀌면 digest 비교가 의미를 잃는다.
#: ★ 23차 발견 5 — `projection_schema: 2` 를 산출물에 쓰면서 여기는 `1` 이었다.
#:   그리고 spec 에 restart 투영·전면 대조·fits 결속이 아예 없었다. 산출물이
#:   무엇인지 spec 이 모르면 `analysis_spec_sha256` 은 앵커가 아니다.
ANALYSIS_SPEC = {
    "schema_version": 3,
    "row_projection": {
        "columns": COLUMNS,
        "sort_key": ["cond_id", "objective"],
        "digest": "sha256 of the uncompressed canonical TSV",
    },
    "restart_projection": {
        "columns": RESTART_COLUMNS,
        "sort_key": ["cond_id", "objective", "i"],
        "digest": "sha256 of the uncompressed canonical TSV",
    },
    "summary_comparison": {
        # ★ 29차 P1-4 — spec 이 `_F4_주의` 도 뗀다고 **선언**하고 있었다.
        #   실제 `SEMANTIC_SKIP` 과 모순이다. 값을 두 곳에 두지 않는다.
        "skip_top_level_keys": list(SEMANTIC_SKIP),
        "type_policy": "exact",      # int↔float·str↔float 를 같다고 보지 않는다
    },
    "fits_binding": {
        "actual_bytes": True,        # 읽은 바이트를 직접 해시
        "manifest": True,            # manifest.fits_seal 과 대조
        "summary": True,             # summary._채점원본 과 대조
    },
    "float_repr": "python repr (shortest round-trip)",
    "line_sep": "\\n",
    "score_path": "src.scoring: add_error_columns → classify_recoverability "
                  "→ clean_bias → apply_bias_correction → summarize",
    "tolerance": 0.02,
}


def _spec_sha256() -> str:
    blob = json.dumps(ANALYSIS_SPEC, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _cell(v) -> str:
    """자리별로 결정론적인 문자열. 부동소수는 repr — 왕복 보장 + 플랫폼 무관."""
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, float):
        return repr(v)
    return str(v)


def score_canonical(df):
    """정본 채점 경로. **여기 한 곳에서만 정의한다.**

    ★ 자체 발견 — `make_receipt.py` 가 같은 네 단계를 각자 적고 있었다. 한쪽만
      고치면 두 감사 도구가 서로 다른 것을 검증하게 되고, 그것을 알아차릴
      방법이 없다. 회귀
      `test_the_two_audit_tools_share_one_canonical_score_path` 가 복제를
      막는다.

    `ANALYSIS_SPEC["score_path"]` 의 문자열이 이 함수를 서술한다 — 둘이 갈리면
    같은 회귀가 잡는다.
    """
    from src.scoring import (DEFAULT_TOL, add_error_columns,
                             apply_bias_correction, classify_recoverability,
                             clean_bias)

    df = add_error_columns(df, DEFAULT_TOL)
    df = classify_recoverability(df)
    bias = clean_bias(df)
    return apply_bias_correction(df, bias, DEFAULT_TOL)


#: restart `source` 로 허용되는 값. 여기 없는 값은 코드가 바뀐 것이다.
_RESTART_SOURCES = frozenset({"base_init", "warm", "random"})


def _restart_list(raw) -> list[dict]:
    """restarts_json → dict 목록. **깨진 것을 조용히 버리지 않는다.**

    ★ 23차 발견 5 — 초판은 `None`·float 를 빈 목록으로 돌리고 non-dict 항목을
      버렸다. 그러면 restart 가 통째로 없는 행이 "restart 0개" 로 조용히
      기록되고, 그 행이 aggregate 를 만들었는지 아무도 모른다.
    """
    if raw is None or (isinstance(raw, float) and raw != raw):   # NaN
        raise SystemExit("✗ restarts_json 이 비어 있다 — 이 행은 재계산 불가다")
    if isinstance(raw, float):
        raise SystemExit(f"✗ restarts_json 이 float 이다: {raw!r}")
    try:
        rs = json.loads(raw) if isinstance(raw, str) else list(raw)
    except (ValueError, TypeError) as e:                    # noqa: BLE001
        raise SystemExit(f"✗ restarts_json 을 못 읽는다: {e}") from e
    if not isinstance(rs, list) or not rs:
        raise SystemExit(f"✗ restarts_json 이 비어 있거나 목록이 아니다: {type(rs)}")
    bad = [r for r in rs if not isinstance(r, dict)]
    if bad:
        raise SystemExit(f"✗ restart 항목이 dict 가 아니다: {bad[:2]}")
    for r in rs:
        s = str(r.get("source"))
        if s not in _RESTART_SOURCES:
            raise SystemExit(f"✗ 모르는 restart source: {s!r} "
                             f"(허용: {sorted(_RESTART_SOURCES)})")
    return rs


def _restart_facts(raw) -> tuple[str, str]:
    """restarts_json → (최적 J 를 낸 restart 의 source, source 구성).

    ★ 이 열이 발견 3 의 핵심이다. warm 이 바꾼 것이 "다봉성" 이 아니라
      **후보 집합** 이라면, 그 증거는 최적해를 낸 restart 의 source 에 있다.
    """
    if raw is None or (isinstance(raw, float)):
        return ("", "")
    try:
        rs = json.loads(raw) if isinstance(raw, str) else list(raw)
    except (ValueError, TypeError):
        return ("?", "?")
    if not rs:
        return ("", "")
    best = min(rs, key=lambda r: (r.get("J") if r.get("J") is not None else float("inf")))
    counts: dict[str, int] = {}
    for r in rs:
        counts[str(r.get("source"))] = counts.get(str(r.get("source")), 0) + 1
    comp = ";".join(f"{k}={counts[k]}" for k in sorted(counts))
    return (str(best.get("source")), comp)


def _add_multistart_blocks(df, summary: dict) -> None:
    """`multistart` · `multistart_random_only` 를 **restart trace 에서** 다시 만든다.

    ★ 22차 리뷰 발견 5 — `summarize()` 는 이 두 블록을 만들지 않는다.
      `run_scoring` 이 `restarts_json` 에서 따로 붙인다. 초판 재계산은 그래서
      두 블록을 통째로 못 봤고, 전면 대조로 바꾸자 "봉인에만 있다" 로 드러났다.
      **발견 3(random-only 다봉성 동일)의 근거가 바로 이 블록**이므로 재계산
      대상에서 빠져 있으면 안 된다.

    `src/scoring.py` 의 구성 순서를 그대로 따른다 — 다르게 조립하면 대조가
    "다르다" 를 낼 뿐 무엇이 다른지 못 가린다.
    """
    import itertools

    from src.scoring import multistart_diagnostics, multistart_summary

    rec_df = df[df["recoverable"]] if "recoverable" in df else df
    ms = multistart_diagnostics(rec_df)
    if ms.empty:
        return
    summary["multistart"] = multistart_summary(ms)

    ms_r = multistart_diagnostics(rec_df, skip_first=True)
    if ms_r.empty:
        return
    blk = multistart_summary(ms_r)
    summary["multistart_random_only"] = blk
    ok_random = bool(ms_r["random_only"].all()) if "random_only" in ms_r else False
    blk["random_only_적용"] = ok_random
    if "n_nonrandom_dropped" in ms_r:
        blk["평균_제외_restart수"] = float(ms_r["n_nonrandom_dropped"].mean())
    if not (ok_random and {"objective", "cond_id"} <= set(ms_r.columns)):
        return

    sets = {o: set(g["cond_id"]) for o, g in ms_r.groupby("objective")}
    blk["n_conditions_per_objective"] = {o: len(v) for o, v in sets.items()}
    key = ms_r.set_index(["objective", "cond_id"])["restart_indices"]
    objs = sorted(sets)
    pairs = {}
    for a, b in itertools.combinations(objs, 2):
        common = sets[a] & sets[b]
        pr = {c for c in common if key[(a, c)] == key[(b, c)]}
        ent = {"n_common": len(common), "n_paired": len(pr),
               "비교가능": bool(len(pr) >= 30)}
        if pr:
            sub = ms_r[ms_r["cond_id"].isin(pr) & ms_r["objective"].isin([a, b])]
            ent["summary"] = multistart_summary(sub)
        pairs[f"{a}__vs__{b}"] = ent
    blk["pairwise"] = pairs
    common_all = set.intersection(*sets.values()) if sets else set()
    paired = {c for c in common_all if len({key[(o, c)] for o in objs}) == 1}
    blk["n_common_conditions"] = len(common_all)
    blk["n_paired_conditions"] = len(paired)
    blk["제외율_목적함수별"] = {
        o: round(1 - len(paired) / len(v), 4) if v else None for o, v in sets.items()}
    blk["비교가능"] = bool(len(paired) >= 30)
    blk["_주의_전역교집합"] = (
        "`n_paired_conditions`·`비교가능`은 **모든 목적함수 동시** "
        "교집합이라 33p↔34p 비교에는 과도하게 엄격하다. 두 목적함수를 "
        "비교할 때는 `pairwise` 블록의 해당 항목을 쓸 것 (F44b).")
    blk["_선택편향"] = (
        f"paired subset은 무작위 표본이 아니다 — adaptive 조기 종료를 "
        f"겪지 않은(=모든 목적함수가 끝까지 간) 조건만 남는다. "
        f"목적함수별 제외율이 "
        f"{min(blk['제외율_목적함수별'].values()):.0%}~"
        f"{max(blk['제외율_목적함수별'].values()):.0%}로 크게 다르다는 것이 "
        f"그 증거다. 여기서 잰 비율을 격자 전체로 일반화하지 말 것.")
    if paired:
        blk["paired"] = multistart_summary(ms_r[ms_r["cond_id"].isin(paired)])
    blk["_주의"] = (
        "★ 목적함수 간 비교는 이 블록을 쓸 것 — source == 'random'인 restart만 "
        "남긴다. 위 multistart 블록은 warm start 지점과 공통 결정론적 초기값을 "
        "포함하므로, warm start를 받은 목적함수(w_dqdv≠0)가 인위적으로 "
        "multimodal 쪽으로 쏠린다. 단 `비교가능`이 false면 목적함수마다 남은 "
        "무작위 restart 수가 달라(adaptive 조기 종료) 검정력이 다르므로 "
        "그대로 비교하지 말 것 — `paired` 블록(공통 cond_id + 동일 restart 수)만 "
        "목적함수 간 비교에 쓸 수 있다."
        if ok_random else
        "⚠ 무효 — 이 fits.parquet은 restart 출처를 저장하지 않은 옛 형식이라 "
        "보정을 하지 못했습니다. restarts_json이 J 오름차순이라 위치로 "
        "추정하면 warm이 아니라 best restart를 버립니다. 이 블록을 인용하지 "
        "마세요 — 출처를 저장하는 현재 코드로 재fit해야 복구됩니다 (F25/F31).")


#: 계산 닫힘의 **뿌리**. 여기서 출발해 실제로 읽는 module-level 이름을
#: 따라가며 닫는다 — 목록에 손으로 적는 것은 이 여섯 개뿐이다.
_COMPUTE_NAMES = ("_cell", "_restart_list", "_restart_facts",
                  "_add_multistart_blocks", "_analyzer_provenance",
                  "score_canonical", "build")


def _compute_closure(src: str) -> dict[str, str]:
    """계산 경로가 **실제로 읽는** module-level 정의의 닫힘.

    ★ 25차 발견 2 — 초판은 손으로 고른 함수 여섯 개와 상수 셋만 해시했다.
      그런데 `_restart_list()` 는 `_RESTART_SOURCES` 를 읽어 허용·거부를
      정한다. 그 frozenset 에 값을 하나 더하면 analyzer 의 의미가 바뀌는데
      digest 는 그대로였고, breaker 는 파일 전체 SHA 를 일부러 제외하므로
      교차비교도 `intact` 로 남았다. **의미가 바뀌었는데 아무 것도 안 깨졌다.**

      그래서 목록이 아니라 닫힘으로 만든다: 뿌리 함수에서 시작해 body 가
      참조하는 module-level 이름을 따라가고, 그것이 module-level 정의면
      포함하고 다시 따라간다.

    import 는 일부러 포함하지 않는다 — runtime/library 버전은 별도 축이고,
    투영이 py3.11/3.12·pandas 2/3 에서 바이트 동일하게 재생성된다는 것을
    세 기계에서 실측했다. 버전을 digest 에 넣으면 그 성질을 잃는다.
    """
    import ast

    tree = ast.parse(src)
    defs: dict[str, ast.AST] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs[node.name] = node
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    defs[t.id] = node
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            defs[node.target.id] = node

    missing = [n for n in _COMPUTE_NAMES if n not in defs]
    if missing:
        raise SystemExit(f"✗ 계산 함수를 못 찾았다: {sorted(missing)} — "
                         f"이름을 바꿨다면 _COMPUTE_NAMES 도 고쳐라")

    out: dict[str, str] = {}
    todo = list(_COMPUTE_NAMES)
    while todo:
        name = todo.pop()
        if name in out:
            continue
        node = defs[name]
        out[name] = ast.get_source_segment(src, node) or ""
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name) and sub.id in defs and sub.id not in out:
                todo.append(sub.id)
    return out


def _compute_sha256() -> str:
    """계산 경로의 **닫힘** + 출력 규격 상수를 해시한다.

    표시 코드 변경이 provenance 를 흔들지 않게 하고, 반대로 계산이 바뀌면
    반드시 흔들리게 한다. `analysis_spec_sha256` 이 **무엇을 만들기로 했는가**
    라면 이것은 **무엇이 만들었는가** 다.
    """
    src = Path(__file__).resolve().read_text(encoding="utf-8")
    closure = _compute_closure(src)
    parts = [f"{k}\n{closure[k]}" for k in sorted(closure)]
    # 값 수준 대조 — 계산식으로 만들어진 상수까지 잡는다 (source 만으로는 부족)
    parts.append(json.dumps({"COLUMNS": COLUMNS,
                             "RESTART_COLUMNS": RESTART_COLUMNS,
                             "ANALYSIS_SPEC": ANALYSIS_SPEC},
                            sort_keys=True, ensure_ascii=False))
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]


def _analyzer_provenance() -> dict:
    """★ 22차 발견 5 — 투영이 **무엇으로 만들어졌는지** 스스로 밝힌다.

    투영 digest 가 같아도 생성기가 다르면 같은 뜻이 아니다.
    """
    import platform
    import sys as _sys

    def _sha(p: Path) -> str:
        return hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.is_file() else ""

    out = {
        # ★ 22차 자체 발견 — 파일 전체 sha 를 provenance 로 쓰면 **출력 문구만
        #   고쳐도** 다리마다 값이 갈린다. 실제로 8다리가 두 판으로 갈렸고,
        #   차이는 `main()` 의 표시 코드뿐이었다 (계산 함수는 바이트 동일).
        #   리뷰어는 sha 만 보고 그것을 알 수 없다 → **계산 경로만** 해시한다.
        "compute_sha256": _compute_sha256(),
        "row_projection_py_sha256": _sha(Path(__file__).resolve()),   # 참고용(전체 파일)
        "src_scoring_py_sha256": _sha(REPO / "src" / "scoring.py"),
        "python": _sys.version.split()[0],
        "platform": platform.platform(),
    }
    for mod in ("pandas", "pyarrow", "numpy", "yaml"):
        try:
            out[mod] = __import__(mod).__version__
        except Exception:                                  # noqa: BLE001
            out[mod] = None
    return out


def build(leg: str, out: Path | None = None) -> dict:
    import pandas as pd
    import yaml

    from src.scoring import (DEFAULT_TOL, add_error_columns, apply_bias_correction,
                             classify_recoverability, clean_bias, summarize)

    d = RESULTS / leg
    fits = d / "fits.parquet"
    if not fits.is_file():
        raise SystemExit(
            f"✗ {leg}: 원자료가 없다 — {fits}\n"
            f"  이 스크립트는 fits.parquet 이 **있는 기계**에서 돌려야 한다.\n"
            f"  컨테이너에는 대부분의 다리가 없다 (results/ 는 git 밖이다).")

    # ★ 22차 리뷰 발견 5 — 초판은 manifest 의 `fits_seal` 을 **복사**했다.
    #   그러면 "내가 읽은 fits 가 봉인된 그 fits 였다" 를 투영 자신이 증명하지
    #   못한다. 실제 바이트를 해시해 manifest·summary 와 **삼중 대조**한다.
    # ★ 23차 발견 5 — 초판은 해시한 뒤 경로를 **다시** 열었다. 그 사이에 파일이
    #   바뀌면 해시와 내용이 어긋난다. 한 번 읽은 바이트로 둘 다 한다.
    import io

    fits_payload = fits.read_bytes()
    fits_bytes_sha = hashlib.sha256(fits_payload).hexdigest()

    df = pd.read_parquet(io.BytesIO(fits_payload))
    df = score_canonical(df)

    src_col = df["restarts_json"] if "restarts_json" in df.columns else [None] * len(df)
    facts = [_restart_facts(v) for v in src_col]
    df = df.assign(best_restart_source=[f[0] for f in facts],
                   restart_sources=[f[1] for f in facts])

    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(f"✗ {leg}: 투영에 필요한 열이 없다: {missing}")

    proj = df[COLUMNS].sort_values(["cond_id", "objective"], kind="mergesort")

    # ★ 22차 발견 5 — malformed 입력을 조용히 통과시키지 않는다.
    import math
    dup = proj.duplicated(subset=["cond_id", "objective"]).sum()
    if dup:
        raise SystemExit(f"✗ {leg}: (cond_id, objective) 중복 {dup}행 — 투영 키가 깨졌다")
    for col in ("J", "abs_err_max", "lli_hat", "lam_pe_hat", "lam_ne_hat"):
        bad_n = sum(1 for v in proj[col] if not math.isfinite(float(v)))
        if bad_n:
            raise SystemExit(f"✗ {leg}: {col} 에 비유한값 {bad_n}행")
    if (proj["restart_sources"] == "?").any():
        raise SystemExit(f"✗ {leg}: restarts_json 을 못 읽은 행이 있다")

    lines = ["\t".join(COLUMNS)]
    lines += ["\t".join(_cell(v) for v in row)
              for row in proj.itertuples(index=False, name=None)]
    text = "\n".join(lines) + "\n"
    full_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()

    # 목적함수별 부분 digest — 33p 만 따로 대조할 수 있어야 한다 (발견 7 항목 3).
    per_obj = {}
    for obj, g in proj.groupby("objective", sort=True):
        sub = ["\t".join(COLUMNS)]
        sub += ["\t".join(_cell(v) for v in row)
                for row in g.itertuples(index=False, name=None)]
        blob = ("\n".join(sub) + "\n").encode("utf-8")
        per_obj[str(obj)] = {"n_rows": int(len(g)),
                             "sha256": hashlib.sha256(blob).hexdigest()}

    # ── restart 수준 투영 (22차 발견 5 항목 4) ────────────────────────────
    # 행 투영은 restart **개수**만 담아서, random-only 다봉성을 투영에서
    # 독립 재계산할 수 없다. 발견 3 의 근거가 바로 그 지표이므로 각 restart 의
    # (index, source, J, p) 를 따로 봉인한다.
    # ★ 23차 발견 5 — 초판은 렌더링된 **문자열**을 정렬했다. 예산이 10 을 넘는
    #   순간 `i=10` 이 `i=2` 앞에 와서, spec 이 선언한 정렬키
    #   `[cond_id, objective, i]` 와 실제 순서가 갈린다. 단계 3 은 예산 40 을
    #   쓰므로 지금 고친다 — 튜플로 정렬하고 그 다음에 렌더링한다.
    rrows = []
    for cond, obj, raw in zip(df["cond_id"], df["objective"],
                              df["restarts_json"] if "restarts_json" in df.columns
                              else [None] * len(df)):
        for r in _restart_list(raw):
            pv = list(r.get("p") or [])
            # 초판은 짧으면 NaN 으로 채우고 길면 잘랐다 — 둘 다 조용한 손실이다.
            if len(pv) != 4:
                raise SystemExit(
                    f"✗ restart p 의 길이가 4가 아니다: {len(pv)} @ "
                    f"({cond}, {obj}, i={r.get('i')})")
            if r.get("J") is None:
                raise SystemExit(f"✗ restart J 가 없다 @ ({cond}, {obj}, i={r.get('i')})")
            rrows.append((str(cond), str(obj), int(r.get("i")), str(r.get("source")),
                          float(r["J"]), *[float(x) for x in pv],
                          bool(r.get("warm"))))
    rrows.sort(key=lambda x: (x[0], x[1], x[2]))

    # fail-closed: index 중복 · 비유한값 · main 의 n_restarts 합과의 일치
    seen_idx: set = set()
    for row in rrows:
        key = (row[0], row[1], row[2])
        if key in seen_idx:
            raise SystemExit(f"✗ restart index 중복: {key}")
        seen_idx.add(key)
        for name, v in zip(RESTART_COLUMNS[4:9], row[4:9]):
            if not math.isfinite(v):
                raise SystemExit(f"✗ restart 비유한값 {name}={v!r} @ {key}")
    n_expect = int(sum(int(x) for x in proj["n_restarts"]))
    if len(rrows) != n_expect:
        raise SystemExit(f"✗ restart 행 수가 main 과 안 맞는다: "
                         f"{len(rrows)} vs n_restarts 합 {n_expect}")

    r_lines = ["\t".join(RESTART_COLUMNS)]
    r_lines += ["\t".join(_cell(v) for v in row) for row in rrows]
    r_text = "\n".join(r_lines) + "\n"
    r_sha = hashlib.sha256(r_text.encode("utf-8")).hexdigest()
    # ★ 26차 P1-9 — 초판은 **검증 전에** gzip payload 부터 목적지에 썼다.
    #   실수 한 번으로 잃어버린 다리의 유일한 사본을 덮을 수 있었다. 이제
    #   staging 에 쓰고 마지막에 원자적으로 옮긴다.
    _out = out or WARM                       # ★ 25차 발견 1 — cohort 디렉터리
    # ★ 27차 P1-8 — frozen 거부가 `main()` 에만 있었다. public `build(leg, out)`
    #   는 frozen `WARM` 을 그대로 받아 썼고 회귀도 CLI subprocess 만 봤다.
    #   검사를 **쓰기 지점**으로 내린다.
    _assert_writable(_out)
    _out.mkdir(parents=True, exist_ok=True)
    _stage = Path(tempfile.mkdtemp(prefix=f".stage_{leg}_", dir=_out))
    r_csv = _stage / f"{leg}.restarts.csv.gz"
    with gzip.GzipFile(r_csv, "wb", compresslevel=9, mtime=0) as fh:
        fh.write(r_text.encode("utf-8"))

    out_csv = _stage / f"{leg}.projection.csv.gz"
    # mtime=0 은 timestamp 만 고정한다. **deflate 구현 차이는 고정하지 않는다** —
    # 22차 리뷰가 zlib-ng 1.3.1 에서 다른 바이트를 실측했다 (zlib 1.3 끼리는 같다).
    # git noise 를 줄이는 효과는 있지만, 정본 앵커는 아래 `full_sha`(압축 전)다.
    with gzip.GzipFile(out_csv, "wb", compresslevel=9, mtime=0) as fh:
        fh.write(text.encode("utf-8"))

    # ── 재계산 검증: 봉인 summary **전체**와 대조 ──────────────────────────
    # ★ 22차 발견 5 — 초판은 `by_objective` 아래 **이미 있는 숫자만** 부분
    #   순회했다. key 집합·`by_objective_noise`·`overall_recoverable`·
    #   `restart_conditioned`·`multistart*`·문자열·불리언·누락 키를 전부 놓쳤다.
    #   이제 재귀 비교로 **전 블록**을 본다.
    recomputed = summarize(df, DEFAULT_TOL)
    _add_multistart_blocks(df, recomputed)
    sealed_path = WARM / f"{leg}.summary.yaml"
    verdict: dict = {"봉인_summary": str(sealed_path.relative_to(REPO))}

    #: 재계산이 만들 수 없는 키 — 채점이 아니라 실행 메타다.
    _SKIP = set(SEMANTIC_SKIP)

    def _cmp(a, b, path: str, out: list) -> None:
        if isinstance(a, dict) and isinstance(b, dict):
            ka, kb = set(a) - _SKIP, set(b) - _SKIP
            for k in sorted(ka - kb):
                out.append(f"{path}.{k}: 봉인에만 있다")
            for k in sorted(kb - ka):
                out.append(f"{path}.{k}: 재계산에만 있다")
            for k in sorted(ka & kb):
                _cmp(a[k], b[k], f"{path}.{k}", out)
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                out.append(f"{path}: 길이 {len(a)} vs {len(b)}")
            else:
                for i, (x, y) in enumerate(zip(a, b)):
                    _cmp(x, y, f"{path}[{i}]", out)
        elif type(a) is not type(b):
            # ★ 23차 발견 5 — 초판은 한쪽이 float 이면 양쪽을 `float()` 로 바꿔
            #   비교했다. 그래서 `0.1` 과 문자열 `"0.1"`, 정수 `1` 과 실수 `1.0`
            #   이 같다고 나왔다. "문자열·불리언까지 자리별 exact" 라는 설명이
            #   실제보다 강했다. 타입이 다르면 그 자체가 불일치다.
            out.append(f"{path}: 타입이 다르다 — 봉인 {type(a).__name__}({a!r}) "
                       f"vs 재계산 {type(b).__name__}({b!r})")
        elif isinstance(a, float):
            if repr(a) != repr(b):
                out.append(f"{path}: 봉인 {a!r} vs 재계산 {b!r}")
        elif a != b:
            out.append(f"{path}: 봉인 {a!r} vs 재계산 {b!r}")

    if sealed_path.is_file():
        sealed = yaml.safe_load(sealed_path.read_text(encoding="utf-8"))
        diffs: list = []
        _cmp(sealed, recomputed, "summary", diffs)
        verdict["전체_일치"] = not diffs
        verdict["by_objective_일치"] = not [d for d in diffs
                                            if d.startswith("summary.by_objective.")]
        verdict["불일치"] = diffs or None
        # ★ 삼중 대조 — 읽은 바이트 == summary 가 채점했다는 fits == manifest 봉인
        s_src = ((sealed.get("_채점원본") or {}).get("fits_sha256"))
        verdict["fits_sha256_읽은바이트"] = fits_bytes_sha
        verdict["fits_sha256_summary"] = s_src
        verdict["fits_삼중일치"] = (s_src == fits_bytes_sha)
        if s_src and s_src != fits_bytes_sha:
            verdict["불일치"] = (verdict["불일치"] or []) + [
                f"읽은 fits 바이트({fits_bytes_sha[:16]})가 summary 가 채점한 "
                f"fits({s_src[:16]})와 다르다"]
            verdict["전체_일치"] = False
    else:
        verdict["전체_일치"] = None
        verdict["by_objective_일치"] = None
        verdict["불일치"] = ["봉인 summary 가 없다"]

    man_path = WARM / f"{leg}.manifest.yaml"

    meta = {
        # 3 = 23차 발견 5 대응 — ANALYSIS_SPEC 이 산출물과 정합(2 는 spec 이
        #     1 이라 어긋났다) · 타입 exact 대조 · restart fail-closed ·
        #     봉인 원본 digest. 2 는 실제 fits 바이트 SHA·전체 대조·restart
        #     투영까지, 1 은 그 셋이 없다.
        "projection_schema": 3,
        "leg_id": leg,
        "projection_file": out_csv.name,
        "n_rows": int(len(proj)),
        "projection_sha256": full_sha,
        "by_objective_sha256": per_obj,
        "restart_projection_file": r_csv.name,
        "restart_projection_sha256": r_sha,
        "n_restart_rows": len(rrows),
        "analysis_spec_sha256": _spec_sha256(),
        "analyzer": _analyzer_provenance(),
        "analysis_spec": ANALYSIS_SPEC,
        "재계산_검증": verdict,
        # ★ 23차 발견 5 — 투영 YAML 에 봉인 원본의 digest 가 없어, 회귀가
        #   "생성 당시 기록된 boolean" 을 다시 믿는 수밖에 없었다. 원본을
        #   해시해 남기면 리뷰어가 그 boolean 이 **어느 파일에 대한 것인지**
        #   독립 검산할 수 있다.
        "summary_sha256": (hashlib.sha256(sealed_path.read_bytes()).hexdigest()
                           if sealed_path.is_file() else None),
        "manifest_sha256": (hashlib.sha256(man_path.read_bytes()).hexdigest()
                            if man_path.is_file() else None),
        "_주의": ("이 투영은 원자료가 아니다. 감사·대조용 축약이며, 여기 없는 열"
                  "(restarts_json 전체, p_spread, 경계 플래그 세부)은 담기지 않는다. "
                  "완전 복원에는 results/<leg>/ 원본이 필요하다."),
    }

    # manifest 가 있으면 fits 봉인·code identity 를 함께 못박는다
    if man_path.is_file():
        man = yaml.safe_load(man_path.read_text(encoding="utf-8")) or {}
        rs = man.get("run_spec") or {}
        seal = ((man.get("fits_seal") or {}).get("file_sha256"))
        meta["fits_sha256_manifest_seal"] = seal
        meta["fits_sha256"] = fits_bytes_sha          # 실제 읽은 바이트
        meta["fits_봉인일치"] = (seal == fits_bytes_sha)
        meta["source_digest"] = rs.get("source_digest")
        meta["warm_start"] = rs.get("warm_start")

    (_stage / f"{leg}.projection.yaml").write_text(
        yaml.safe_dump(meta, allow_unicode=True, sort_keys=False), encoding="utf-8")
    # ── 승격 — **verdict 가 통과했을 때만** ──────────────────────────────
    # ★ 27차 P1-8 — 초판은 semantic verdict 가 false 여도 세 파일을 먼저
    #   승격하고 CLI 가 나중에 exit 1 을 냈다. staging 이 promotion gate 가
    #   아니었다. 이제 실패하면 staging 째로 버린다.
    _v = meta.get("재계산_검증") or {}
    _ok = (_v.get("전체_일치") is True and _v.get("fits_삼중일치") is True
           and meta.get("fits_봉인일치") is True)
    if not _ok:
        shutil.rmtree(_stage, ignore_errors=True)
        raise SystemExit(
            f"✗ {leg}: 재계산 검증이 실패해 승격하지 않는다 — "
            f"전체={_v.get('전체_일치')} fits삼중={_v.get('fits_삼중일치')} "
            f"봉인일치={meta.get('fits_봉인일치')} · 불일치={_v.get('불일치')}")

    # YAML 을 **마지막에** 옮긴다 (manifest-last). YAML 이 나머지 둘의 digest 를
    # 들고 있으므로, 중간에 죽으면 옛 YAML 이 옛 payload 를 계속 가리켜
    # 세대가 섞이지 않는다.
    # ★ 33차 #9 — 초판은 세 파일을 하나씩 `os.replace` 했다. manifest-last 로
    #   섞임을 줄였을 뿐 set atomicity 가 아니어서, 첫 파일 뒤 중단하면 reader
    #   가 두 세대를 함께 봤다. cohort 전체의 immutable generation 을 만들고
    #   **pointer 하나**를 원자적으로 옮긴다.
    # ★ 38차 #9 — roster 는 **보존 원장**에서 온다. 산출물에서 유도하지 않는다.
    promote_cohort_generation(_stage, _out, leg, roster=_ledger_roster(_out))

    return meta


# ─────────────────────────────────────────────────────────────────────────────
# immutable generation + 단일 CURRENT (★ 32차 최소 증거 #9)
# ─────────────────────────────────────────────────────────────────────────────
#
# 왜: 초판 승격은 **fixed-name 세 파일**을 하나씩 `os.replace` 했다. YAML 을
#   마지막에 옮겨(manifest-last) 섞임을 줄였지만 set atomicity 는 아니다 —
#   중간에 죽으면 새 payload 와 옛 YAML 이 공존한다. 27~31차 리뷰가 "다음
#   checkpoint" 로 계속 지목한 자리다.
#
# 어떻게: generation 은 내용 주소를 이름으로 갖는 **immutable directory** 이고,
#   덮어쓰지 않는다. 승격은 그 directory 를 만든 뒤 **단일 pointer** 하나를
#   원자적으로 옮기는 것이다. 읽는 쪽은 pointer 를 따른다.
#
#       out/gen/<generation_id>/…      ← 한 번 쓰고 절대 안 고친다
#       out/CURRENT                    ← 이 한 파일만 원자적으로 바뀐다

CURRENT_SCHEMA = "projection-current/v1"


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def generation_id(files: dict) -> str:
    """generation 의 내용 주소 — 이름 → 바이트 digest 의 정본 해시."""
    payload = json.dumps({"schema": CURRENT_SCHEMA, "files": files},
                         sort_keys=True, ensure_ascii=False,
                         separators=(",", ":")).encode("utf-8")
    return _sha(payload)


def _fsync_dir(d: Path) -> None:
    fd = os.open(d, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


#: "인자가 안 왔다" 와 "None 이 왔다" 를 구별하는 표식 (36차 #9b — CAS 기대값이
#: `None` 인 것은 "CURRENT 가 아직 없어야 한다" 는 뜻이라 생략과 다르다).
_UNSET = object()

class _PublishLock:
    """게시 전체를 덮는 writer critical section (37차 #9 · 38차 #9).

    ★ 37차판은 `O_CREAT|O_EXCL` + **mtime 600초** 였다. 그것이 상호배제를
      다시 열었다:

        · PID 를 쓰기만 하고 읽지 않았다 (owner liveness 미확인)
        · heartbeat 가 없어 오래 걸리는 작업이 곧 stale 로 보였다
        · `__exit__` 가 자기 lock 인지 확인 없이 unlink 했다 → ABA:
          A 가 늦게 깨어나 **B 의 lock 을 지운다**

    ★ 38차 — 시간 기반 lease 를 **버린다.** `fcntl.flock` 은 process 가 죽으면
      kernel 이 자동으로 푼다. owner liveness·heartbeat·stale 판정·fencing 이
      전부 필요 없어진다 — 있어야 할 것을 더 만드는 대신 필요 없게 만든다.
      (단일 호스트 로컬 filesystem 전제다. 그것이 이 저장소의 실제 배치다.)

    release 는 **token 을 대조**한다. 어떤 이유로든 lock 파일이 자기 것이
    아니게 됐으면 지우지 않는다.
    """

    def __init__(self, out: Path):
        self.path = Path(out) / ".publish.lock"
        self.fd = None
        self.token = None

    def __enter__(self):
        import fcntl

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fd = os.open(self.path, os.O_CREAT | os.O_RDWR, 0o644)
        try:
            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(self.fd)
            self.fd = None
            raise SystemExit(
                f"✗ 다른 게시가 진행 중이다: {self.path} — 그 process 가 살아 "
                "있다. 끝난 뒤 다시 시도하라")
        self.token = uuid.uuid4().hex
        os.ftruncate(self.fd, 0)
        os.pwrite(self.fd, f"{os.getpid()} {self.token}".encode(), 0)
        os.fsync(self.fd)
        return self

    def __exit__(self, *exc):
        import fcntl

        if self.fd is None:
            return False
        try:
            # ★ 38차 — **내 token 일 때만** 지운다. 아니면 남의 lock 이다.
            cur = os.pread(self.fd, 4096, 0).decode("utf-8", "replace")
            if self.token and self.token in cur:
                self.path.unlink(missing_ok=True)
        except OSError:
            pass
        finally:
            try:
                fcntl.flock(self.fd, fcntl.LOCK_UN)
            except OSError:
                pass
            os.close(self.fd)
            self.fd = None
        return False

    def held(self) -> bool:
        return self.fd is not None


def _publish_pointer(out: Path, rec: dict) -> None:
    """CURRENT 를 **원자적으로** 옮긴다. 여기가 유일한 가시성 전환점이다."""
    tmp = out / f".CURRENT.{uuid.uuid4().hex}.tmp"
    data = json.dumps(rec, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")
    fd = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    try:
        n = 0
        while n < len(data):
            n += os.write(fd, data[n:])
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, out / "CURRENT")
    _fsync_dir(out)


def _promote_generation(stage: Path, out: Path, *, expect=_UNSET,
                        lock: "_PublishLock" = None) -> dict:
    """staging 을 immutable generation 으로 굳히고 CURRENT 를 옮긴다.

    ★ 36차 #9b — **비공개다.** 이 함수는 staging 을 그대로 믿으므로 한 파일
      짜리 staging 을 넘기면 cohort 를 한 파일로 줄인 generation 이 정상
      게시된다. 34차에 `promote_cohort_generation()` 에 세 파일 exact set
      검사를 붙였지만, 그 검사를 **건너뛰는 공개 이름**을 옆에 남겨 두면
      검사가 아니라 권고다. 완전성을 보는 유일한 입구는 cohort publisher 다.

    `expect` 는 CURRENT 의 compare-and-swap 기대값이다 (36차 #9b). base 를
    읽은 뒤 게시까지 사이에 CURRENT 가 움직였으면 덮지 않고 거부한다.
    """
    # ★ 38차 #9 — **유효한 lock 을 들고 있어야** pointer 를 옮길 수 있다.
    #   37차판은 이 함수가 이름만 private 였고 lock 없이도 게시할 수 있었다.
    #   "private 라는 이름은 trust boundary 가 아니다" 를 스스로 어겼다.
    if lock is None or not getattr(lock, "held", lambda: False)():
        raise SystemExit(
            "✗ 게시 lock 없이 CURRENT 를 옮길 수 없다 — "
            "`promote_cohort_generation()` 을 쓰라")
    stage, out = Path(stage), Path(out)
    _assert_writable(out)
    files = {p.name: _sha(p.read_bytes())
             for p in sorted(stage.iterdir()) if p.is_file()}
    if not files:
        raise SystemExit(f"✗ staging 이 비었다: {stage}")
    gid = generation_id(files)
    gdir = out / "gen" / gid

    if gdir.is_dir():
        # 같은 내용이면 멱등. 다른 바이트가 있으면 **덮지 않고 거부**한다.
        got = {p.name: _sha(p.read_bytes())
               for p in sorted(gdir.iterdir()) if p.is_file()}
        if got != files:
            raise SystemExit(
                f"✗ generation {gid[:16]} 자리에 다른 내용이 있다 — immutable "
                f"generation 은 덮지 않는다 (기대 {sorted(files)} · 실제 {sorted(got)})")
        shutil.rmtree(stage, ignore_errors=True)
    else:
        (out / "gen").mkdir(parents=True, exist_ok=True)
        _fsync_dir(out)
        tmp = out / "gen" / f".{gid}.{uuid.uuid4().hex}.tmp"
        shutil.move(str(stage), str(tmp))
        for p in sorted(tmp.iterdir()):
            if p.is_file():
                fd = os.open(p, os.O_RDONLY)
                try:
                    os.fsync(fd)
                finally:
                    os.close(fd)
        _fsync_dir(tmp)
        os.rename(tmp, gdir)              # generation 이 통째로 보인다
        _fsync_dir(out / "gen")

    rec = {"schema": CURRENT_SCHEMA, "generation_id": gid, "files": files}
    if expect is not _UNSET:
        live = None
        if (out / "CURRENT").is_file():
            live = read_current(out)["generation_id"]
        if live != expect:
            raise SystemExit(
                f"✗ CURRENT 가 그 사이에 움직였다 (기대 "
                f"{str(expect)[:16]} · 실제 {str(live)[:16]}) — 남의 승격을 "
                "덮지 않는다. base 를 다시 읽고 재시도하라")
    _publish_pointer(out, rec)
    _materialize(out, rec)      # 호환 사본 — 권위는 CURRENT 다
    return rec


def read_current(out: Path, expect_legs=None) -> dict:
    """CURRENT 를 따라간다. 없거나 깨졌거나 실물과 어긋나면 **fail-closed**."""
    out = Path(out)
    p = out / "CURRENT"
    if not p.is_file():
        raise SystemExit(f"✗ CURRENT 가 없다: {p}")
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        raise SystemExit(f"✗ CURRENT 를 읽을 수 없다: {p} ({e})") from e
    if not isinstance(rec, dict) or rec.get("schema") != CURRENT_SCHEMA \
            or not isinstance(rec.get("files"), dict):
        raise SystemExit(f"✗ CURRENT schema 가 계약이 아니다: {rec!r}")
    gid = rec.get("generation_id")
    if generation_id(rec["files"]) != gid:
        raise SystemExit(f"✗ CURRENT 의 generation_id 가 files 와 다르다")
    gdir = out / "gen" / str(gid)
    if not gdir.is_dir():
        raise SystemExit(f"✗ CURRENT 가 없는 generation 을 가리킨다: {gid[:16]}")
    got = {q.name: _sha(q.read_bytes())
           for q in sorted(gdir.iterdir()) if q.is_file()}
    if got != rec["files"]:
        raise SystemExit(f"✗ generation {gid[:16]} 의 실물이 CURRENT 와 다르다")
    assert_cohort_complete(rec["files"], gid, expect_legs=expect_legs)
    return rec


def assert_cohort_complete(files: dict, gid: str, expect_legs=None) -> None:
    """generation 이 완전한가 — **publish 와 read 가 함께 쓰는** validator.

    ★ 36차 #9b 는 관측된 leg 를 순회했다. 그래서 셋이 통과했다:
        · `files={}` 인 빈 generation (공허참)
        · expected roster 의 leg 가 **통째로** 빠진 generation
        · 한 leg 의 세 파일만 넘겨 multi-leg cohort 를 축소하는 호출
      완전성은 관측된 것이 아니라 **기대 명부**에 대해 닫혀야 한다.

    ★ 36차에 publisher 쪽 사본을 "중복" 으로 보고 지웠는데, 그것이 틀렸다.
      변이가 안 문 이유는 중복이어서가 아니라 **validator 가 약해서** 였다.
      이제 pure 함수 하나를 양쪽에서 부른다 — publisher 가 private 라는 이름
      규약은 trust boundary 가 아니므로 read-side 검사를 없앨 근거가 못 된다.

    `expect_legs` 를 주면 그 명부와 **정확히** 같아야 한다. 명부는 고정 파일
    목록에서 유도하면 안 되고 (그러면 자기 자신을 근거로 삼는다) 원장·계약
    처럼 밖에서 와야 한다.
    """
    if not files:
        raise SystemExit(
            f"✗ generation {str(gid)[:16]} 이 비었다 — 빈 generation 은 "
            "'모든 leg 가 완전하다' 를 공허참으로 만족한다")
    seen = {_leg_of(n) for n in files}
    bad = []
    for leg in sorted(seen):
        have = {n for n in files if _leg_of(n) == leg}
        need = {f"{leg}{sfx}" for sfx in LEG_SUFFIXES}
        if have != need:
            bad.append(f"{leg}: 모자람 {sorted(need - have)} · "
                       f"남음 {sorted(have - need)}")
    if expect_legs is not None:
        want = set(expect_legs)
        if seen != want:
            bad.append(f"명부와 다르다: 빠진 leg {sorted(want - seen)} · "
                       f"명부에 없는 leg {sorted(seen - want)}")
    if bad:
        raise SystemExit(
            f"✗ generation {str(gid)[:16]} 이 불완전하다 — " + " / ".join(bad))


def _materialize(out: Path, rec: dict) -> None:
    """CURRENT 의 generation 을 fixed name 으로 **파생**시킨다 (호환 reader 용).

    권위는 `CURRENT` 다. 이 사본은 편의이며 `check_materialized()` 가
    CURRENT 와 갈리는지 본다.
    """
    gdir = out / "gen" / rec["generation_id"]
    for name in sorted(rec["files"]):
        dst = out / name
        src = gdir / name
        if dst.exists() and _sha(dst.read_bytes()) == rec["files"][name]:
            continue
        tmp = out / f".{name}.{uuid.uuid4().hex}.tmp"
        tmp.write_bytes(src.read_bytes())
        os.replace(tmp, dst)
    _fsync_dir(out)


def check_materialized(out: Path) -> dict:
    """fixed-name 사본이 CURRENT 와 같은지. 갈리면 **오류**다."""
    rec = read_current(out)
    for name, want in sorted(rec["files"].items()):
        q = Path(out) / name
        if not q.is_file() or _sha(q.read_bytes()) != want:
            raise SystemExit(
                f"✗ {name} 사본이 CURRENT 와 다르다 — 권위는 CURRENT 다")
    return rec


def cohort_bytes(out: Path, name: str) -> bytes:
    """**CURRENT 를 통해서만** 읽는다. fixed path 는 authority 가 아니다."""
    rec = read_current(out)
    if name not in rec["files"]:
        raise SystemExit(f"✗ CURRENT 가 {name} 을 담고 있지 않다")
    data = (Path(out) / "gen" / rec["generation_id"] / name).read_bytes()
    if _sha(data) != rec["files"][name]:
        raise SystemExit(f"✗ {name} 의 바이트가 CURRENT 와 다르다")
    return data


#: leg 하나가 반드시 갖는 세 파일. generation 완전성의 정본이다.
LEG_SUFFIXES = (".projection.csv.gz", ".projection.yaml", ".restarts.csv.gz")


def _leg_of(name: str) -> str:
    return name.split(".", 1)[0]


def promote_cohort_generation(stage: Path, out: Path, leg: str, *, roster) -> dict:
    """한 leg 를 갱신하되 **cohort 전체**의 새 generation 을 만든다.

    ★ 33차 #9 — 32차판은 `promote_generation(stage, out)` 을 그대로 쓰면
      cohort 가 **한 leg 로 줄어드는** 구조였다 (stage 가 한 leg 만 담으므로).
      요구는 immutable **cohort** generation 이다. 현재 generation 을 base 로
      읽어 그 leg 의 파일만 갈아 끼운 **완전한 snapshot** 을 만든다.
    """
    stage, out = Path(stage), Path(out)
    # ★ 37차 #9 — base 읽기 · 완전성 판정 · generation 자재화 · pointer 전환을
    #   **한 임계 구역**으로 묶는다. 이 중 어느 둘 사이에 남의 게시가 끼면
    #   그 leg 가 조용히 사라진다.
    # ★ 38차 #9 — `roster` 는 **필수**다. 선행 authority(보존 원장)가 선언한
    #   cohort 구성이며, staged files 나 관측된 `CURRENT` 에서 유도하면 안 된다
    #   — 그러면 자기 출력이 자기 근거가 된다. 37차판은 그렇게 했고, 원장에
    #   빠진 leg 가 있는 base 를 그대로 영속화하거나 원장에 없는 leg 를 게시할
    #   수 있었다.
    #   빈 roster 와 "이 leg 가 명부 밖" 은 아래 `undeclared` 검사가 그대로
    #   잡는다 (staging 에는 언제나 이 leg 가 들어 있다). 같은 규칙을 두 곳에
    #   두면 강한 쪽을 지워도 초록이 된다 — 변이로 확인했다.
    roster = set(roster or ())
    with _PublishLock(out) as lock:
        return _promote_cohort_locked(stage, out, leg, lock, roster)


def _promote_cohort_locked(stage: Path, out: Path, leg: str,
                           lock: "_PublishLock", roster: set) -> dict:
    base: dict = {}
    gdir = None
    expect = None
    if (out / "CURRENT").is_file():
        # ★ 38차 #9 — base 는 **명부 부분집합**이면 된다. 여기서 exact 를
        #   요구하면 bootstrap 이 불가능하다: roster={a,b} 인 cohort 에 a 를
        #   처음 게시할 때 base 는 비어 있고, b 를 게시하려면 base={a} 여야
        #   한다. exact 는 **reader** 의 주장이다 (`_Snapshot` 이 그것을 한다).
        cur = read_current(out)
        base = dict(cur["files"])
        gdir = out / "gen" / cur["generation_id"]
        expect = cur["generation_id"]

    fresh = {p.name for p in stage.iterdir() if p.is_file()}
    # ★ 34차 #9 — "완전한 snapshot" 을 **구조로** 강제한다. 초판은 stage 의
    #   이름 집합을 얻은 뒤 그 leg 의 기존 파일을 base 에서 전부 제외했지만,
    #   stage 가 exact set 인지 보지 않았다. `{a.projection.yaml}` 만 넘기면
    #   그 leg 의 CSV·restart 를 **제거한** generation 이 정상 게시됐다.
    want = {f"{leg}{sfx}" for sfx in LEG_SUFFIXES}
    if fresh != want:
        raise SystemExit(
            f"✗ {leg} 의 staging 이 세 파일 exact set 이 아니다 — 남음 "
            f"{sorted(fresh - want)} · 모자람 {sorted(want - fresh)}")
    # ★ 36차 #9b — base 완전성 검사를 여기서 **뺐다.** `read_current()` 가
    #   모든 독자에 대해 같은 것을 보므로 (위 `read_current(out)` 호출이
    #   그것이다) 여기 사본은 중복이었다 — 변이로 확인했다: 이 loop 를 지워도
    #   suite 가 초록이었다. 검사가 하나 더 있는 것과 불변식이 한 곳에 있는
    #   것은 다르다.
    keep = {n: h for n, h in base.items() if _leg_of(n) != leg}

    # base 에서 넘길 파일을 staging 에 복사한다 — generation 은 self-contained
    for name in sorted(keep):
        shutil.copyfile(gdir / name, stage / name)
    # ★ 37차 #9 — publish 쪽에서도 **같은** validator 를 부른다. 36차에 이
    #   사본을 지웠던 것은 오판이었다: 변이가 안 문 것은 중복이어서가 아니라
    #   validator 가 약해서였다. 기대 명부는 base 에 있던 leg 들 ∪ {이번 leg}
    #   — 승격이 남의 leg 를 **줄이는** 것을 여기서 막는다.
    # ★ 38차 #9 — 명부에 대한 publisher 의 의무는 둘이다. exact 는 위에서
    #   설명한 이유로 여기서 요구할 수 없고, **reader** 가 요구한다.
    #     1) 명부에 없는 leg 를 만들지 않는다
    #     2) 이미 있던 leg 를 **줄이지 않는다** (한 leg 갱신이 cohort 를 깎지
    #        못하게 — 34차부터의 요구다)
    staged = {p.name: _sha(p.read_bytes())
              for p in sorted(stage.iterdir()) if p.is_file()}
    have = {_leg_of(n) for n in staged}
    undeclared = sorted(have - roster)
    if undeclared:
        raise SystemExit(
            f"✗ 명부에 없는 다리를 게시하려 한다: {undeclared} "
            f"(roster={sorted(roster)}) — 원장을 먼저 고쳐라")
    #   (기존 leg 를 줄이는 것은 위 `keep` 복사가 구조로 막는다 — 검사를 하나
    #    더 두려 했으나 도달 불가능이었다. 확인했고 두지 않는다.)
    assert_cohort_complete(staged, "staging")
    return _promote_generation(stage, out, expect=expect, lock=lock)


def _ledger_roster(out: Path) -> set:
    """이 cohort 디렉터리를 선언한 원장 항목의 `legs` (38차 #9).

    선행 authority 다 — `CURRENT` 도 staging 도 아니다. 원장이 이 디렉터리를
    모르면 게시하지 않는다 (fail-closed).
    """
    import yaml

    reg_path = REPO / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"
    if not reg_path.is_file():
        raise SystemExit(f"✗ 보존 원장이 없다: {reg_path} — roster 를 알 수 없다")
    reg = yaml.safe_load(reg_path.read_text(encoding="utf-8")) or {}
    want = Path(out).resolve()
    for c in reg.get("cohorts") or []:
        if (REPO / c["dir"]).resolve() == want:
            return set(c.get("legs") or ())
    raise SystemExit(
        f"✗ 원장이 모르는 cohort 디렉터리다: {out} — 먼저 "
        "`LEG_PRESERVATION.yaml` 에 선언하라")


def _frozen_cohort_dirs() -> dict[str, Path]:
    """`LEG_PRESERVATION.yaml` 이 frozen 이라고 선언한 cohort 디렉터리.

    ★ 26차 P1-9 — `--out` 을 생략하면 기본값이 `warm_probe`(= frozen g1)라
      원자료를 잃은 여덟 투영을 실수로 덮을 수 있었다. 목적지는 cohort 로
      고르고, frozen 이면 여기서 막는다.
    """
    import yaml

    reg_path = REPO / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"
    if not reg_path.is_file():
        # ★ 28차 P1-5 — 원장이 없으면 빈 dict 를 돌려 **fail-open** 했다.
        #   보호 장치가 없다는 뜻이므로 쓰지 못하게 막는 것이 맞다 (fail-closed).
        raise SystemExit(f"✗ 보존 원장이 없다: {reg_path} — frozen cohort 를 "
                         "구별할 수 없으므로 아무 데도 쓰지 않는다")
    reg = yaml.safe_load(reg_path.read_text(encoding="utf-8")) or {}
    return {c["cohort_id"]: (REPO / c["dir"]).resolve()
            for c in (reg.get("cohorts") or []) if c.get("status") == "frozen"}


def _assert_writable(dest: Path) -> None:
    """frozen cohort 로는 쓸 수 없다. **쓰기 지점**에서 막는다 (27차 P1-8)."""
    d = Path(dest).resolve()
    for cid, frozen in _frozen_cohort_dirs().items():
        # ★ 28차 P1-5 — exact equality 만 봤다. `frozen/child` 는 frozen tree
        #   **안**인데 통과했다. 자손까지 막는다.
        if d == frozen or frozen in d.parents:
            raise SystemExit(
                f"✗ `{cid}` 는 frozen cohort 다 ({d}) — 쓸 수 없다.\n"
                f"  원자료를 잃은 투영이 들어 있어 덮으면 복구할 수 없다.\n"
                f"  활성 cohort 를 지정하세요: --cohort <id>")


def _cohort_dir(cohort_id: str) -> Path:
    import yaml

    reg_path = REPO / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"
    reg = yaml.safe_load(reg_path.read_text(encoding="utf-8")) or {}
    for c in reg.get("cohorts") or []:
        if c["cohort_id"] == cohort_id:
            if c.get("status") == "frozen":
                raise SystemExit(
                    f"✗ `{cohort_id}` 는 frozen cohort 다 — 쓸 수 없다.\n"
                    f"  원자료를 잃은 투영이 들어 있어 덮으면 복구할 수 없다.\n"
                    f"  새 세대는 새 cohort 를 만들어라 (계약 v4 §13.3).")
            return REPO / c["dir"]
    raise SystemExit(f"✗ 모르는 cohort: {cohort_id!r}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("legs", nargs="*")
    ap.add_argument("--all", action="store_true",
                    help="warm_probe 에 summary 가 있는 다리 전부")
    ap.add_argument("--cohort", default=None, help=(
        "쓸 cohort id (`LEG_PRESERVATION.yaml` 의 `cohorts`). "
        "frozen cohort 는 거부한다 — 권장 경로다."))
    ap.add_argument("--out", default=None, help=(
        "투영을 쓸 디렉터리 (repo 상대). 기본은 warm_probe. "
        "★ 25차 발견 1 — analyzer 세대가 바뀌면 옛 cohort 를 덮지 않고 "
        "새 디렉터리에 쓴다. 봉인 summary/manifest 는 언제나 warm_probe 에서 읽는다."))
    a = ap.parse_args()
    if a.cohort and a.out:
        ap.error("--cohort 와 --out 을 함께 쓰지 마세요")
    if a.cohort:
        out_dir = _cohort_dir(a.cohort)
    else:
        out_dir = (REPO / a.out) if a.out else None
        # ★ 26차 P1-9 — 목적지가 frozen cohort 면 거부한다. `--out` 생략도
        #   기본값이 frozen g1 이므로 같은 검사를 받는다.
        dest = (out_dir or WARM).resolve()
        frozen = {d: cid for cid, d in _frozen_cohort_dirs().items()}
        if dest in frozen:
            raise SystemExit(
                f"✗ `{frozen[dest]}` 는 frozen cohort 다 ({dest}) — 쓸 수 없다.\n"
                f"  원자료를 잃은 투영이 들어 있어 덮으면 복구할 수 없다.\n"
                f"  활성 cohort 를 지정하세요: --cohort <id>")

    legs = list(a.legs)
    if a.all:
        legs += sorted(p.name[: -len(".summary.yaml")]
                       for p in WARM.glob("*.summary.yaml"))
    legs = sorted(dict.fromkeys(legs))
    if not legs:
        ap.error("다리를 지정하거나 --all 을 쓰세요")

    rc = 0
    for leg in legs:
        try:
            m = build(leg, out_dir)
        except SystemExit as e:
            print(e)
            rc = 1
            continue
        v = m["재계산_검증"]
        # ★ 22차 자체 발견 — 초판은 `by_objective_일치` 하나만 찍었다. 전체
        #   semantic 대조나 fits 삼중 대조가 실패해도 화면에는 ✅ 가 떴다.
        #   **가장 엄격한 판정**을 요약 줄에 올린다.
        checks = {"전체": v.get("전체_일치"),
                  "by_obj": v.get("by_objective_일치"),
                  "fits삼중": v.get("fits_삼중일치"),
                  "봉인일치": m.get("fits_봉인일치")}
        ok = all(c is True for c in checks.values())
        mark = "✅" if ok else ("⚠" if any(c is None for c in checks.values()) else "❌")
        print(f"{mark} {leg}: {m['n_rows']}행 · restart {m['n_restart_rows']}행 · "
              f"proj {m['projection_sha256'][:16]} · "
              + " · ".join(f"{k} {c}" for k, c in checks.items()))
        for d in (v.get("불일치") or [])[:5]:
            print(f"     {d}")
        if not ok:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
