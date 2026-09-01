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
import contextlib
import os
import posixpath
import shutil
import stat
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

    # ★ 50차 — "module-level 정의란 무엇인가" 의 authority 는 **하나**다.
    #   49차까지 이 함수가 같은 walk 의 사본을 들고 있었고, 그래서 tuple
    #   대입을 담게 고칠 때 한쪽만 고치면 약한 쪽이 실효 규칙이 된다
    #   (실측: 여기만 고쳤더니 `_module_defs()` 는 그대로였다).
    defs: dict[str, ast.AST] = _module_defs(src)

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


#: ★ 47차 #9 — producer 닫힘에서 **잘라 내는** 이름. 게시 경로는 바이트를
#:   만들지 않으므로 producer identity 가 아니다.
#:
#:   46차까지 `compute_sha256` 닫힘은 `build()` 가 뿌리라서 publisher 전체를
#:   빨아들였고, 그래서 게시 코드를 고칠 때마다 값이 움직였다. 그 값을 봉인에
#:   넣으면 라운드마다 새 cohort ID 가 필요해지고, 빼면 producer 가 섞인다
#:   (46차가 뺐고 47차 리뷰가 섞이는 schedule 을 보였다). 답은 셋째다:
#:   **바이트를 만드는 코드만** 닫힘에 넣는다.
#:   절단면은 두 종류다 — **게시**(바이트를 어디에 굳히는가)와
#:   **원장 authority**(어디에·써도 되는가). 둘 다 행 바이트를 만들지 않는다.
#:   이름이 사라지면 `_producer_closure()` 가 fail-closed 로 거부하므로,
#:   절단면이 조용히 넓어지거나 좁아질 수 없다.
#: ★ 48차 P0-2 — 절단면 **정의 자체**가 봉인 preimage 에 들어간다
#:   (`_producer_semantic_over()`). 47차는 이름이 *사라지면* fail-closed 였지만
#:   *늘어나면* 아무 일도 없었다 — 아직 닫힘에 없는 이름을 미리 넣어 두면
#:   나중 refactor 가 그 이름을 계산 경로로 끌어오는 순간 조용히 제외된다.
_PRODUCER_CUT = ("promote_cohort_generation",
                 "_ledger_roster", "_ledger_cohort", "_ledger_cohorts",
                 "_ledger_dir", "_frozen_cohort_dirs", "_cohort_dir",
                 "_assert_writable")


def _keep_docstrings(tree):
    """docstring 을 **남긴다** — 51차 P0-I.

    50차까지 이 자리는 `_strip_docstrings()` 였다. 산문 변경이 identity 를
    흔들지 않게 하려는 것이었고, 그 대신 "버린 것을 읽는 코드" 를 guard 가
    막았다: `.__doc__` 이라는 **철자**를 거부했다.

    리뷰어가 그 철자를 피해 갔다:

        read_attribute = getattr
        read_attribute(score_canonical, "__doc__")

        digest_A == digest_B                       (같다)
        result_A={'doc_result': 1}  result_B={'doc_result': 9}

    철자 blacklist 를 alias 까지 넓히는 것은 종결 조건이 아니다 — alias 의
    alias, 부분 적용, dict 에 담은 함수로 계속 이어진다. 종결 조건은 **버리는
    것을 없애는 것**이다. 버린 것이 없으면 그것을 읽어 생기는 괴리도 없다.

    대가는 명확하다: 계산 경로 함수의 docstring 을 고치면 producer identity 가
    움직이고 cohort 를 새로 만들어야 한다. 산문 한 줄이 그만한 값인가 — 그렇다.
    "digest 가 거짓일 수 있다" 를 남기는 것보다 싸다. (계산 경로 **밖**의
    docstring 은 애초에 닫힘에 안 들어가므로 영향이 없다.)

    함수는 identity 로 남긴다 — 정규형 pipeline 의 자리를 지우면 다음 사람이
    "여기서 무엇을 버리나" 를 다시 묻게 된다. 지금 답은 **아무 것도 안 버린다** 다.
    """
    return tree


def _ast_normal_node(node) -> str:
    """정의 **node** 하나를 정규형 소스로 — 주석·공백·줄바꿈이 사라진다.

    ★ 48차 P0-2 두 가지를 함께 고친다.

    1. **node 를 직접 본다.** 47차는 `ast.get_source_segment()` 로 소스를 오려
       다시 parse 했는데, `FunctionDef.lineno` 는 `def` 줄을 가리키고
       `decorator_list` 는 그 **위**에 있다 — 그래서 `@lru_cache` 를 붙이거나
       떼도 digest 가 그대로였다. node 를 쓰면 decorator 가 정규형에 들어온다.

    2. **`ast.unparse` 로 찍는다.** 47차의 `ast.dump` 는 node 필드 목록을 그대로
       쓰므로 인터프리터 버전에 묶인다. 실측: 같은 바이트에 대해
       3.11 `908503e65162e7d9` · 3.12 `d4ae1c027b434e83` ·
       3.13 `aa1cf2cf045c41ea` — 세 값이었다. 인터프리터를 올리는 것만으로
       봉인이 깨지면, 그때 사람은 "코드는 그대로니 pin 을 갱신하자" 고 판단하게
       되고 봉인의 뜻이 사라진다. `unparse` 는 **코드 자체**를 찍으므로 문법이
       바뀌지 않는 한 버전을 타지 않는다 (회귀가 이 기계의 3.10~3.13 에서
       실제로 대조한다).
    """
    import copy

    return _ast_canon(_keep_docstrings(copy.deepcopy(node)))


#: ★ 49차 P0-2 — **지원하는 인터프리터 집합.** 정규형이 버전에 안 묶인다는
#: 주장을 지키는 것은 지금 도는 인터프리터 하나뿐이었다. 새 문법이 새 field 를
#: 들고 오면 정규형이 조용히 달라지고 producer identity 가 이유 없이 움직인다.
#: 게시 identity 는 이 집합 **안에서만** 계산한다 (fail-closed).
SUPPORTED_PYTHON = ((3, 11), (3, 12), (3, 13))


def _ast_canon_of(source: str) -> str:
    """구문 조각 하나의 정규형 — golden vector 를 재려고 연 창구다."""
    import ast

    return _ast_canon(ast.parse(source).body[0])


#: 대표 구문의 정규형 golden. 새 인터프리터에서 달라지면 **여기서** 깨진다.
#: (`python3 -c` 로 `_ast_canon_of` 를 찍어 갱신하되, 값이 달라졌다는 것은
#:  그 버전에서 producer identity 가 달라진다는 뜻이므로 그냥 덮어쓰면 안 된다 —
#:  `SUPPORTED_PYTHON` 을 좁히거나 정규형을 그 버전까지 덮게 고쳐야 한다.)
AST_CANON_GOLDEN = {
    "def f(a, b=1, *ar, c, **kw):\n    return a + b\n":
        "FunctionDef(name='f', args=arguments(args=[arg(arg='a'), "
        "arg(arg='b')], vararg=arg(arg='ar'), kwonlyargs=[arg(arg='c')], "
        "kw_defaults=[None], kwarg=arg(arg='kw'), "
        "defaults=[Constant(value=1, kind=None)]), "
        "body=[Return(value=BinOp(left=Name(id='a', ctx=Load()), op=Add(), "
        "right=Name(id='b', ctx=Load())))])",
    "x = f'{a!r:>{w}} {b}'\n":
        "Assign(targets=[Name(id='x', ctx=Store())], "
        "value=JoinedStr(values=[FormattedValue(value=Name(id='a', "
        "ctx=Load()), conversion=114, "
        "format_spec=JoinedStr(values=[Constant(value='>', kind=None), "
        "FormattedValue(value=Name(id='w', ctx=Load()), conversion=-1)])), "
        "Constant(value=' ', kind=None), FormattedValue(value=Name(id='b', "
        "ctx=Load()), conversion=-1)]))",
    "y = [i for i in r if i]\n":
        "Assign(targets=[Name(id='y', ctx=Store())], "
        "value=ListComp(elt=Name(id='i', ctx=Load()), "
        "generators=[comprehension(target=Name(id='i', ctx=Store()), "
        "iter=Name(id='r', ctx=Load()), ifs=[Name(id='i', ctx=Load())], "
        "is_async=0)]))",
    "match p:\n    case {'k': v}:\n        pass\n":
        "Match(subject=Name(id='p', ctx=Load()), "
        "cases=[match_case(pattern=MatchMapping(keys=[Constant(value='k', "
        "kind=None)], patterns=[MatchAs(name='v')]), body=[Pass()])])",
}


def assert_supported_interpreter() -> None:
    """게시 identity 를 **선언한 인터프리터 밖에서** 계산하지 않는다 (49차 P0-2)."""
    if sys.version_info[:2] not in SUPPORTED_PYTHON:
        raise SystemExit(
            f"✗ 이 인터프리터({sys.version_info[0]}.{sys.version_info[1]})는 "
            f"지원 집합 {SUPPORTED_PYTHON} 밖이다 — producer identity 정규형이 "
            "그 버전에서 같다는 증거가 없다. `AST_CANON_GOLDEN` 으로 확인한 뒤 "
            "`SUPPORTED_PYTHON` 에 넣어라")


def _ast_canon(node) -> str:
    """AST 를 **버전에 안 묶이는** 구조 문자열로 (48차 P0-2).

    `ast.dump` 도 `ast.unparse` 도 인터프리터 버전을 탄다 — 이 기계에서 실측한
    두 원인이 각각 하나씩이다.

    - `ast.dump`: 3.12 가 `FunctionDef` 에 `type_params` 를 더했다. 필드가 하나
      늘면 모든 함수의 문자열이 달라진다.
    - `ast.unparse`: 3.12 의 PEP 701 이후 f-string 안 따옴표를 재사용해 찍는다
      (`f'{r.get('i')}'` vs `f"{r.get('i')}"`). **같은 AST** 인데 렌더링이 다르다.

    그래서 렌더링을 우리가 한다. 규칙 둘:

    1. 노드의 `_fields` 만 쓰고 **빈 값(None·빈 목록)은 뺀다** — 새 버전이 더한
       필드는 기본값이 비어 있으므로 저절로 무시된다. 값이 실제로 차면 그때는
       digest 가 움직인다 (그게 맞다 — 그건 코드가 바뀐 것이다).
    2. f-string 은 `JoinedStr(values=[...])` 구조로만 적는다 — 따옴표가 아예
       등장하지 않으므로 렌더링 차이가 생길 자리가 없다.

    `Constant` 만 `value` 를 무조건 적는다 (`None` 리터럴이 빈 노드로 접히면
    서로 다른 코드가 같은 문자열이 된다).

    ★ 50차 P0 — 규칙 3: `JoinedStr.values` 안의 **빈 문자열 조각**을 버린다.
      PEP 701(3.12) 파서가 중첩 format spec 끝에 `Constant(value='')` 를 붙인다
      — 같은 AST 의미인데 3.11 과 3.13 에는 없다. 49차 golden 이 3.12 에서
      실제로 어긋난 원인이 이것이다 (리뷰어 실측, 이 기계에서 재현했다).
      빈 조각은 렌더링 결과를 바꾸지 않으므로 뜻을 잃지 않고 지울 수 있다.
    """
    import ast

    if isinstance(node, ast.AST):
        parts = []
        for f in node._fields:
            v = getattr(node, f, None)
            # ★ 50차 P0 — PEP 701(3.12) 이 중첩 format spec 끝에 붙이는 빈
            #   조각을 버린다. 같은 뜻인데 3.11·3.13 에는 없다.
            if isinstance(node, ast.JoinedStr) and f == "values" \
                    and isinstance(v, list):
                v = [x for x in v
                     if not (isinstance(x, ast.Constant) and x.value == "")]
            if not isinstance(node, ast.Constant):
                if v is None or (isinstance(v, list) and not v):
                    continue
            parts.append(f"{f}={_ast_canon(v)}")
        return f"{type(node).__name__}({', '.join(parts)})"
    if isinstance(node, list):
        return "[" + ", ".join(_ast_canon(x) for x in node) + "]"
    return repr(node)


#: ★ 48차 P0-2 — 행 바이트를 만드는 코드는 **이 파일 밖에도** 있다.
#:   `score_canonical()` 은 `src.scoring` 의 채점 함수를 불러 행을 만든다.
#:   47차 닫힘은 module-level 이름만 따라갔으므로 채점 의미를 통째로 바꿔도
#:   `producer_semantic_sha256` 이 움직이지 않았다. `src_scoring_py_sha256` 은
#:   답이 아니었다 — 파일 전체 sha 라 주석 한 줄에도 움직이고, `_PIN_SEALED`
#:   밖이라 그것으로 게시를 막는 검사도 없었다.
_PRODUCER_MODULES = ("src.scoring",)


def _target_names(node):
    """대입 target 이 묶는 **모든** 이름 (tuple·list·starred 를 편다)."""
    import ast

    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, ast.Starred):
        return _target_names(node.value)
    if isinstance(node, (ast.Tuple, ast.List)):
        out = []
        for el in node.elts:
            out += _target_names(el)
        return out
    return []                       # Attribute·Subscript 는 module 이름이 아니다


#: module scope 에서 **이름을 묶지 않는** 단순문.
_MODULE_NONBINDING = ("Expr", "Pass", "Raise", "Assert", "Delete", "AugAssign",
                      "Global", "Nonlocal", "Break", "Continue", "Return",
                      "Import", "ImportFrom")

#: **안으로 들어가야 하는** 복합문 — 그 안의 정의도 module scope 다.
_MODULE_COMPOUND = ("If", "Try", "TryStar", "For", "AsyncFor", "While",
                    "With", "AsyncWith", "Match")


def _module_defs(src: str) -> dict:
    """module-level 정의 이름 → node. **모르는 문은 거부한다** (51차 P0-I).

    50차까지 이 함수는 Function/Class/Assign/AnnAssign 네 형태만 담고 나머지를
    조용히 지나쳤다. 조용히 지나치는 것은 "그 이름은 없다" 고 답하는 것과 같고
    그 답은 거짓일 수 있다. 리뷰어가 실제 파일의 `_RESTART_SOURCES = ...` 한
    줄을 `for _RESTART_SOURCES in (...): pass` 로 바꾼 두 변형을 만들었다 —
    **동작이 다른데 sealed identity 가 같았다.**

    철자를 하나씩 추가하는 방식(49차 Import, 50차 tuple target)은 종결 조건이
    아니다. 종결 조건은 셋이다:

      · 복합문은 **안으로 들어간다** (`_MODULE_COMPOUND`) — `if`/`try` 안의
        정의도 module scope 이고, `for`/`with`/`except` 는 자기 target 도 묶는다.
      · 이름을 안 묶는 단순문은 지나간다 (`_MODULE_NONBINDING`).
      · **그 밖은 멈춘다.** 새 문법이 필요해지면 여기 넣고 그때 의미를 정한다.

    묶는 이름은 그 문 **전체** node 에 매핑한다 — 값이 어디서 오든 그 문의
    소스가 identity 에 들어가야 값 변경이 digest 를 움직인다.
    """
    import ast

    defs: dict = {}

    def _walrus(node):
        for sub in ast.walk(node):
            if isinstance(sub, ast.NamedExpr):
                for name in _target_names(sub.target):
                    defs[name] = node

    def _visit(body, top):
        for node in body:
            kind = type(node).__name__
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef)):
                defs[node.name] = node
                continue
            _walrus(top or node)
            if isinstance(node, ast.Assign):
                # ★ 50차 P0 — `A, B = 1, 2` · `(D,) = (4,)` · `[E, *F] = …` 도
                #   module 정의다. 49차는 `ast.Name` target 만 담았으므로 계산
                #   상수를 tuple 대입으로 바꾸면 identity 에서 통째로 빠졌다.
                for t in node.targets:
                    for name in _target_names(t):
                        defs[name] = top or node
            elif isinstance(node, ast.AnnAssign):
                for name in _target_names(node.target):
                    defs[name] = top or node
            elif kind in _MODULE_NONBINDING:
                continue                  # import 는 `_crossed_*` 가 따로 본다
            elif kind in _MODULE_COMPOUND:
                here = top or node
                for name in _target_names(getattr(node, "target", None)
                                          or ast.Pass()):
                    defs[name] = here
                for item in getattr(node, "items", ()) or ():
                    if item.optional_vars is not None:
                        for name in _target_names(item.optional_vars):
                            defs[name] = here
                for h in getattr(node, "handlers", ()) or ():
                    if getattr(h, "name", None):
                        defs[h.name] = here
                    _visit(h.body, here)
                for attr in ("body", "orelse", "finalbody"):
                    _visit(getattr(node, attr, ()) or (), here)
                for case in getattr(node, "cases", ()) or ():
                    _visit(case.body, here)
            else:
                raise SystemExit(
                    f"✗ producer 소스의 module scope 에 모델링하지 않은 binding "
                    f"form 이 있다: `{kind}` ({getattr(node, 'lineno', '?')}행) "
                    "— 닫힘이 볼 수 없는 이름은 identity 밖 계산을 만든다. 이 "
                    "문법을 쓰려면 `_MODULE_COMPOUND`/`_MODULE_NONBINDING` 에 "
                    "넣고 `_module_defs()` 가 무엇을 묶는지 정하라 (fail-closed)")

    _visit(ast.parse(src).body, None)
    return defs


def _crossed_aliases(src: str) -> dict:
    """`from src.scoring import x as y` → {지역이름: 원래이름}.

    import 는 함수 안에 있으므로 module body 가 아니라 **트리 전체**를 훑는다.
    """
    import ast

    out: dict = {}
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.ImportFrom) and node.module in _PRODUCER_MODULES:
            for al in node.names:
                if al.name != "*":
                    out[al.asname or al.name] = al.name
    return out


def _crossed_modules(src: str) -> set:
    """`import src.scoring as sc` → {지역이름}. `sc.foo` 를 따라가기 위한 것 (49차).

    ★ 49차 P0-2 — 48차 닫힘은 `from ... import` **한 가지 문법만** 따라갔다.
      같은 함수를 `import src.scoring as sc` + `sc.add_error_columns(...)` 로
      부르면 닫힘이 그 자리에서 멈췄고, 채점 의미를 통째로 바꿔도 digest 가
      움직이지 않았다. 문법 하나를 바꾸는 것만으로 identity 밖으로 나갈 수
      있으면 그것은 identity 가 아니다.
    """
    import ast

    out: set = set()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Import):
            for al in node.names:
                if al.name in _PRODUCER_MODULES:
                    # `import src.scoring` (alias 없음) 은 지역 이름이
                    # `src` 이고 `src.scoring.foo` 로 쓴다 — 그 형태는
                    # 아래 `_dynamic_escapes()` 가 잡는 대신 여기서 정직하게
                    # alias 를 요구한다 (as 없이 쓰면 닫힘이 애매해진다).
                    if al.asname:
                        out.add(al.asname)
                    else:
                        raise SystemExit(
                            f"✗ `import {al.name}` 을 alias 없이 쓴다 — producer "
                            "닫힘이 `src.scoring.foo` 형태를 따라가려면 "
                            f"`import {al.name} as <이름>` 이어야 한다")
    return out


#: 이름 공간을 통째로 여는 호출 — 인자와 무관하게 거부한다.
_DYNAMIC_ALWAYS = ("eval", "exec", "__import__")

#: 대상이 **module 이름 공간**일 때만 거부하는 호출. `getattr(self, …)` 이나
#: `getattr(node, …)` 처럼 객체의 속성을 읽는 정상 용법까지 막지 않는다 —
#: 그것은 module-level 이름을 푸는 것이 아니므로 정적 닫힘이 잃는 것이 없다.
_DYNAMIC_ON_NAMESPACE = ("globals", "locals", "vars", "getattr", "setattr")


def _assert_no_dynamic_resolution(node, where: str, mods: set) -> None:
    """계산 경로 안에서 **module-level 이름**을 동적으로 푸는가 (49차 P0-2).

    `globals()[...]` · `getattr(sc, ...)` · `eval` 은 module-level 이름을 실행
    시점에 고른다. 그런 코드가 닫힘 안에 있으면 닫힘은 "그 이름을 안 쓴다" 고
    답하고 digest 는 태연히 값을 낸다 — 그것이 곧 identity 밖의 계산이다.
    **볼 수 없으면 거부한다.**

    경계는 좁게 잡는다: 막는 것은 이름 공간을 푸는 용법뿐이고,
    `getattr(node, f, None)` 처럼 객체 속성을 읽는 것은 그대로 둔다 (실제로
    이 파일의 정규형 함수들이 그렇게 쓰고, 그것은 닫힘을 흐리지 않는다).
    """
    import ast

    for sub in ast.walk(node):
        if not isinstance(sub, ast.Call) or not isinstance(sub.func, ast.Name):
            # ★ 51차 P0-I — `__doc__` 은 여기서 빠졌다. 이제 정규형이
            #   docstring 을 **버리지 않으므로** 그것을 읽는 것은 identity 밖
            #   계산이 아니다. 나머지 셋은 여전히 정규형이 못 보는 것이고,
            #   그쪽은 철자 목록이 아니라 "실행 시점 이름 풀기" 축이다.
            if isinstance(sub, ast.Attribute) and sub.attr in (
                    "__dict__", "__globals__", "__code__"):
                raise SystemExit(
                    f"✗ producer 닫힘 안에서 정규형이 **버리는 것**을 읽는다: "
                    f"{where} 의 `.{sub.attr}` — `_ast_canon()` 이 못 보는 값을 "
                    "계산이 쓰면 digest 가 거짓이 된다 (둘 중 하나만 참일 수 있다)")
            continue
        fn = sub.func.id
        if fn in _DYNAMIC_ALWAYS:
            raise SystemExit(
                f"✗ producer 닫힘 안에서 이름을 **동적으로** 푼다: "
                f"{where} 의 `{fn}(...)` — 정적 닫힘이 볼 수 없는 계산은 "
                "producer identity 밖이다. 직접 import 해서 부르라")
        if fn not in _DYNAMIC_ON_NAMESPACE:
            continue
        # 인자가 없으면 **현재 module 이름 공간** 전체다
        first = sub.args[0] if sub.args else None
        if first is None or (isinstance(first, ast.Name) and first.id in mods):
            target = "현재 module" if first is None else first.id
            raise SystemExit(
                f"✗ producer 닫힘 안에서 이름 공간({target})을 동적으로 푼다: "
                f"{where} 의 `{fn}(...)` — 정적 닫힘이 볼 수 없는 계산은 "
                "producer identity 밖이다")


def _producer_closure(src: str, scoring_src: str | None = None) -> dict[str, str]:
    """**바이트를 만드는** 코드의 닫힘 (게시 경로는 절단면에서 멈춘다).

    `_compute_closure()` 와 같은 walk 이지만 두 가지가 다르다.

    - `_PRODUCER_CUT` 의 이름은 소스를 담지 않고 절단 표식만 남긴다 — 그 이름이
      **불렸다는 사실**은 identity 에 남기고(호출이 사라지면 digest 가 움직인다)
      그 구현은 뺀다.
    - ★ 48차 — `src.scoring` **안으로 건너간다.** 계산 경로가 부르는 채점
      함수와 그 함수가 다시 읽는 module-level 이름까지 따라간다. 키는
      `src.scoring:<name>` 으로 namespace 를 붙여 이름 충돌을 없앤다.
    """
    import ast

    if scoring_src is None:
        scoring_src = (REPO / "src" / "scoring.py").read_text(encoding="utf-8")

    defs = _module_defs(src)
    sdefs = _module_defs(scoring_src)
    alias = _crossed_aliases(src)
    mods = _crossed_modules(src)          # ★ 49차 P0-2 — `sc.foo` 형태

    missing = [x for x in _COMPUTE_NAMES if x not in defs]
    if missing:
        raise SystemExit(f"✗ 계산 함수를 못 찾았다: {sorted(missing)}")
    cut_missing = [x for x in _PRODUCER_CUT if x not in defs]
    if cut_missing:
        raise SystemExit(
            f"✗ producer 절단면 이름이 없다: {sorted(cut_missing)} — 이름을 "
            "바꿨다면 `_PRODUCER_CUT` 도 고쳐라 (조용히 닫힘이 넓어지면 게시 "
            "코드가 producer identity 에 들어온다)")
    # 건너갈 이름이 상대 모듈에 실제로 있어야 한다 — 없으면 fail-closed.
    alias_missing = sorted({v for v in alias.values() if v not in sdefs})
    if alias_missing:
        raise SystemExit(
            f"✗ `src.scoring` 에서 가져오는 이름이 그 모듈에 없다: "
            f"{alias_missing} — 닫힘이 조용히 좁아진다")

    out: dict[str, str] = {}
    todo = [("rp", x) for x in _COMPUTE_NAMES]
    while todo:
        kind, name = todo.pop()
        key = name if kind == "rp" else f"src.scoring:{name}"
        if key in out:
            continue
        if kind == "rp" and name in _PRODUCER_CUT:
            out[key] = f"<cut:{name}>"          # 이름별 표식 (48차)
            continue
        node = defs[name] if kind == "rp" else sdefs[name]
        # ★ 49차 P0-2 — 볼 수 없는 계산은 identity 밖이다. 닫힘에 들어오는
        #   **모든** 노드에 대해 동적 이름 풀이를 거부한다.
        _assert_no_dynamic_resolution(node, key, mods)
        out[key] = _ast_normal_node(node)
        for sub_node in ast.walk(node):
            # ★ 49차 P0-2 — `sc.foo` (Import + Attribute). 48차는 이 문법을
            #   전혀 따라가지 않아, import 형태만 바꾸면 채점 의미가 통째로
            #   닫힘 밖으로 나갔다.
            if kind == "rp" and isinstance(sub_node, ast.Attribute) \
                    and isinstance(sub_node.value, ast.Name) \
                    and sub_node.value.id in mods:
                attr = sub_node.attr
                if attr not in sdefs:
                    raise SystemExit(
                        f"✗ `src.scoring` 에 없는 이름을 참조한다: "
                        f"{sub_node.value.id}.{attr} ({key}) — 닫힘이 조용히 "
                        "좁아진다")
                if f"src.scoring:{attr}" not in out:
                    todo.append(("sc", attr))
                continue
            if not isinstance(sub_node, ast.Name):
                continue
            nid = sub_node.id
            if kind == "rp":
                if nid in alias and f"src.scoring:{alias[nid]}" not in out:
                    todo.append(("sc", alias[nid]))
                elif nid in defs and nid not in out:
                    todo.append(("rp", nid))
            else:
                if nid in sdefs and f"src.scoring:{nid}" not in out:
                    todo.append(("sc", nid))
    return out


def _producer_semantic_over(src: str, scoring_src: str | None = None) -> str:
    """주어진 소스에 대한 producer 의미 digest (시험이 변형본을 넣을 수 있게)."""
    assert_supported_interpreter()
    closure = _producer_closure(src, scoring_src)
    parts = [f"{k}\n{closure[k]}" for k in sorted(closure)]
    parts.append(json.dumps({"COLUMNS": COLUMNS,
                             "RESTART_COLUMNS": RESTART_COLUMNS,
                             "ANALYSIS_SPEC": ANALYSIS_SPEC,
                             # ★ 48차 P0-2 — 절단면·건너감 **정의 자체**를 봉인
                             #   preimage 에 넣는다. 그래야 절단면을 넓히는 것도
                             #   건너감을 끊는 것도 digest 를 움직인다.
                             "_PRODUCER_CUT": list(_PRODUCER_CUT),
                             "_PRODUCER_MODULES": list(_PRODUCER_MODULES)},
                            sort_keys=True, ensure_ascii=False))
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]


def _producer_semantic_sha256() -> str:
    """이 트리의 producer 의미 identity — **봉인 대상**이다 (계약 §13.3.2)."""
    return _producer_semantic_over(
        Path(__file__).resolve().read_text(encoding="utf-8"))


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
        # ★ 47차 #9 — **봉인되는** producer identity. 주석·서식·게시 코드에는
        #   흔들리지 않고 계산 정의에는 흔들린다.
        "producer_semantic_sha256": _producer_semantic_sha256(),
        "row_projection_py_sha256": _sha(Path(__file__).resolve()),   # 참고용(전체 파일)
        "src_scoring_py_sha256": _sha(REPO / "src" / "scoring.py"),
        "python": _sys.version.split()[0],
        "platform": platform.platform(),
    }
    # ★ 49차 P0-2 — `__import__(mod)` 는 이름을 **실행 시점에** 푼다. producer
    #   닫힘은 그것을 볼 수 없으므로 거부되며, 여기서는 정적 import 로 같은
    #   값을 얻는다 (버전 기록은 provenance 이고 행 바이트를 만들지 않지만,
    #   그 판단을 정적 분석기에게 시킬 수는 없다).
    import numpy as _np49
    import pandas as _pd49
    import pyarrow as _pa49
    import yaml as _yaml49

    for mod, _m in (("pandas", _pd49), ("pyarrow", _pa49),
                    ("numpy", _np49), ("yaml", _yaml49)):
        try:
            out[mod] = _m.__version__
        except Exception:                                  # noqa: BLE001
            out[mod] = None
    return out


def build(leg: str, out: Path | None = None) -> dict:
    import pandas as pd
    import yaml

    from src.scoring import (DEFAULT_TOL, add_error_columns, apply_bias_correction,
                             classify_recoverability, clean_bias, summarize)

    # ★ 50차 P0 — **목적지 판정이 맨 앞이다.** 49차는 원자료 존재 검사가 먼저라,
    #   frozen cohort 로 쓰라는 호출이 원자료가 없는 기계에서는 다른 이유로
    #   죽었다 (리뷰어 실측: clean checkout 에서 그 회귀가 빨개졌다). 그것은
    #   시험의 이식성 문제이기 전에 **순서 결함**이다 — 원자료가 있는 기계에서는
    #   frozen 목적지를 향해 읽기·계산을 먼저 하게 된다. 거절은 아무 일도 하기
    #   전에 나야 한다.
    _dest_check = out or WARM
    _assert_writable(_dest_check)

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
    # ★ 46차 #9 — staging 을 치우는 것은 **만든 쪽**의 일이다. publisher 는
    #   caller 경로에 쓰거나 지우지 않는다 (45차까지는 지웠다).
    try:
        promote_cohort_generation(_stage, _out, leg, roster=_ledger_roster(_out))
    finally:
        shutil.rmtree(_stage, ignore_errors=True)

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

CURRENT_SCHEMA = "projection-current/v2"      # 45차 #9 — cohort·원장 결속
#: ★ 46차 #9 — 이 문자열은 **generation 의 내용 주소에 들어간다**
#:   (`generation_id()` 참조). 그래서 올리면 이미 굳은 generation 의
#:   이름이 전부 바뀐다 — pointer 표현이 바뀌었다고 올릴 값이 아니다.
#:   46차의 key 집합 변경(`cohort_id` echo 제거)은 닫힌 schema 검사가
#:   그 자리에서 fail-closed 로 잡고, 이미 커밋된 pointer 는
#:   `docs/22p_gap/migrate_pointer.py` 가 **같은 generation 을 가리킨 채**
#:   한 번 옮긴다.


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

class _PublishLock:
    """게시 전체를 덮는 writer critical section (37~40차 #9).

    ★ 이력이 곧 설계 근거다:
        37차 `O_CREAT|O_EXCL` + mtime 600초 → 살아 있는 owner 를 빼앗고 ABA
        38차 `fcntl.flock` + token 삭제      → pathname split ABA
        39차 persistent inode + `assert_held_for` → **method 이름으로 위조 가능**
        40차 구체 타입 + 활성 registry + kernel lock 재확인

    ★ 40차 #9 — `assert_held_for` 라는 **이름**을 갖는 것으로는 부족하다.
      no-op method 하나면 새 capability 가 됐다. 39차가 고친 것이 duck-typed
      boolean 에서 duck-typed method 이름으로 옮겨간 것뿐이었다.

      · 구체 타입이어야 하고
      · 이 process 의 **활성 registry** 에 있어야 하고
      · kernel lock 을 **지금** 들고 있어야 한다 (밖에서 `LOCK_UN` 하면 거부)

    ★ 40차 #9 — lock 파일 **내용은 authority 가 아니다.** 39차는 취득마다
      PID·token 을 쓰고 fsync 했는데 그 값은 아무 판정에도 안 쓰이면서
      worktree 만 더럽혔다 (실제로 저장소에 커밋됐다). 빈 sentinel 로 둔다.
    """

    #: 이 process 가 **지금 들고 있는** lock 들. 위조 객체는 여기 없다.
    _ACTIVE: set = set()

    def __init__(self, out: Path):
        self.out = Path(out).resolve()
        self.path = self.out / ".publish.lock"
        self.fd = None
        self.ino = None
        self.pid = None

    def __enter__(self):
        try:
            import fcntl
        except ImportError as e:                 # pragma: no cover - POSIX 전제
            # native Windows 에는 `fcntl` 이 없다. 조용히 lock 없이 진행하면
            # 상호배제가 사라지므로 **명시적으로 거부**한다.
            raise SystemExit(
                "✗ 이 platform 에는 fcntl 이 없다 — 게시 상호배제를 보장할 수 "
                "없으므로 진행하지 않는다 (POSIX 단일 호스트 전제)") from e

        self.path.parent.mkdir(parents=True, exist_ok=True)
        # ★ 41차 #9 — **파괴적 반례를 닫는다.** 40차는 `O_NOFOLLOW` 없이 열고
        #   flock 뒤 `ftruncate(fd, 0)` 했다. 미리 `.publish.lock -> CURRENT`
        #   symlink(또는 hardlink)를 두면 게시자가 lock 을 잡는 순간 권위
        #   파일이 빈 파일이 됐고, 뒤따르는 inode 대조는 symlink 를 따라가므로
        #   그 손상을 못 봤다.
        #
        #   셋을 바꾼다: symlink 를 따라가지 않고, **평범한 regular inode 를
        #   나만 가리키는지** 확인하고, **truncate 하지 않는다.** sentinel 의
        #   내용은 어차피 authority 가 아니므로 쓸 일도 지울 일도 없다.
        try:
            fd = os.open(self.path,
                         os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o644)
        except OSError as e:
            raise SystemExit(
                f"✗ 게시 lock 을 열 수 없다: {self.path} ({e}) — symlink 로 "
                "만들어져 있으면 그것을 지우고 다시 시도하라. lock sentinel 은 "
                "평범한 파일이어야 한다") from e
        try:
            self._assert_plain_sentinel(fd)      # flock **전에** 본다
        except BaseException:
            os.close(fd)
            raise
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(fd)
            raise SystemExit(
                f"✗ 다른 게시가 진행 중이다: {self.path} — 그 process 가 살아 "
                "있다. 끝난 뒤 다시 시도하라")
        # ★ 40차 #9 — flock 을 **잡은 뒤** 실패하면 반드시 풀고 나간다.
        #   39차는 cleanup 이 없어 다음 writer 가 영영 못 들어왔다.
        try:
            # 검사와 잠금 사이에 pathname 이 교체됐을 수 있다 — 다시 본다.
            self.ino = self._assert_plain_sentinel(fd).st_ino
        except BaseException:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
            except OSError:
                pass
            os.close(fd)
            raise
        self.fd = fd
        self.pid = os.getpid()
        type(self)._ACTIVE.add(id(self))
        return self

    def __exit__(self, *exc):
        import fcntl

        if self.fd is None:
            return False
        # ★ 39차 #9 — **파일을 지우지 않는다.** 지우면 pathname 이 다른 inode 로
        #   교체될 수 있고, 옛 owner 가 새 owner 의 lock path 를 지우는 ABA 가
        #   난다. flock 은 process 가 죽으면 kernel 이 푸니 잔여 파일은 다음
        #   owner 를 막지 않는다. persistent inode 가 모든 writer 를 한 곳으로
        #   모으고 삭제 경합 자체를 없앤다.
        type(self)._ACTIVE.discard(id(self))
        try:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
        except OSError:
            pass
        os.close(self.fd)
        self.fd = None
        return False

    @staticmethod
    def _assert_plain_sentinel(fd: int):
        """이 fd 가 **나만 가리키는 평범한 파일**인가 (41차 #9).

        hardlink 는 `O_NOFOLLOW` 로 막을 수 없다 — `st_nlink` 로 본다. 다른
        이름이 같은 inode 를 공유하면 이 자리에서 하는 어떤 조작도 그 파일에
        그대로 간다.
        """
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise SystemExit(
                "✗ 게시 lock sentinel 이 regular file 이 아니다 — 평범한 파일만 "
                "쓴다 (남의 inode 를 잡지 않기 위해)")
        if st.st_nlink != 1:
            raise SystemExit(
                f"✗ 게시 lock sentinel 이 다른 이름과 inode 를 공유한다 "
                f"(st_nlink={st.st_nlink}) — hardlink 로 남의 파일을 겨눌 수 "
                "있으므로 거부한다")
        return st

    def _reassert_kernel_lock(self) -> None:
        """게시 직전에 **원래 fd 로** 배타 lock 을 다시 강제한다 (41차 #9).

        ★ 40차는 같은 pathname 을 **두 번째 fd** 로 열어 잡히지 않으면 "내가
          들고 있다" 고 결론냈다. 그 실패가 말하는 것은 *누군가* 잠갔다는
          것뿐이다::

              A enter → A LOCK_UN → B LOCK_EX → A.assert_held_for()
              probe 는 B 때문에 실패 → A 를 승인한다

          반대로 아무도 안 잠근 상태에서는 probe 가 **실제로** lock 을 잠깐
          잡았다 놨다 — 무부작용 관측도 아니었다. 그리고 contention 이 아닌
          `OSError` 까지 "locked" 로 읽었다.

          관측을 그만두고 **강제**한다. 원래 fd 에 다시 `LOCK_EX|LOCK_NB` 를
          걸면, 이미 내가 들고 있으면 성공하고 (그 플랫폼 성질은
          `..._reapplying_flock_to_an_fd_that_already_holds_it_succeeds` 가
          고정한다) 남이 들고 있으면 실패한다. 남의 lock 은 건드리지 않는다.
        """
        import fcntl

        try:
            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as e:
            raise SystemExit(
                f"✗ 게시 직전에 배타 lock 을 보유하지 못한다 ({e}) — 다른 "
                "writer 가 같은 inode 를 잡고 있다. fd·pathname 을 갖는 것과 "
                "지금 잠그고 있는 것은 다르다") from e

    def assert_held_for(self, out: Path) -> None:
        """이 lock 이 **바로 그 cohort** 의 살아 있는 것인가 (39·40·41차 #9)."""
        want = Path(out).resolve()
        if self.fd is None or id(self) not in type(self)._ACTIVE:
            raise SystemExit(f"✗ lock 을 들고 있지 않다: {want}")
        if self.out != want:
            raise SystemExit(
                f"✗ 이 lock 은 {self.out} 의 것이다 — {want} 를 게시할 수 없다")
        if self.pid != os.getpid():
            raise SystemExit("✗ 다른 process 가 잡은 lock 이다")
        try:
            st = os.fstat(self.fd)
            # ★ 41차 #9 — `Path.stat()` 은 symlink 를 **따라간다.** 그 사이에
            #   pathname 이 남의 파일을 가리키는 symlink 로 바뀌면 대상의
            #   inode 를 보고 통과할 수 있다. 링크 자체를 본다.
            live = os.stat(self.path, follow_symlinks=False)
        except OSError as e:
            raise SystemExit(f"✗ lock 파일을 확인할 수 없다: {e}") from e
        if st.st_ino != self.ino or live.st_ino != self.ino:
            raise SystemExit(
                "✗ lock 파일의 inode 가 바뀌었다 — 잡고 있는 것이 그 파일이 "
                "아니다 (pathname 이 교체됐다)")
        # ★ 42차 #9 — **내부도 unbound 로 부른다.** 41차는 바깥 호출만 unbound
        #   였고 안에서 다시 `self.` 로 dispatch 했다. 정확한 `_PublishLock`
        #   인스턴스도 평범한 객체라 속성을 붙일 수 있으므로, subclass 없이
        #   마지막 kernel proof 하나만 no-op 으로 덮으면 registry·pid·fd·inode
        #   가 전부 진짜인 채로 통과했다 — B 가 잠근 상태에서도.
        _PublishLock._assert_plain_sentinel(self.fd)
        _PublishLock._reassert_kernel_lock(self)


def _publish_pointer(out: Path, rec: dict, name: str = "CURRENT",
                     auth: "_Authority" = None) -> None:
    """CURRENT 를 **원자적으로** 옮긴다. 여기가 유일한 가시성 전환점이다.

    ★ 39차 #9 — `name=".PENDING"` 은 bootstrap 용 **비활성** pointer 다.
      어떤 reader 도 그것을 권위로 보지 않는다 (`read_current()` 는 `CURRENT`
      만 본다). 다음 leg 의 publisher 가 base 를 찾는 데만 쓴다.
    """
    tmp = _write_pointer_tmp(out, rec)
    # ★ 44차 #9 — 대조를 **`os.replace` 직전**으로 내린다. 43차는 guard 가
    #   통과한 뒤 temp write·fsync 를 거쳐 commit 했고, 그 사이에 다른 valid
    #   pointer 가 생기면 그대로 덮었다. 여기까지 내려도 마지막 syscall 앞
    #   창은 남는다 — 그것을 없애려면 권한 경계나 provider 의 원자적
    #   conditional write 가 필요하다 (`_TRUST_BOUNDARY` 참조).
    if auth is not None:
        _Authority.assert_pointers_unmoved(auth)
    os.replace(tmp, out / name)
    _fsync_dir(out)


def _write_pointer_tmp(out: Path, rec: dict) -> Path:
    """pointer 를 temp 로 쓰고 fsync 한다 — 남은 것은 `os.replace` 하나다."""
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
    return tmp


#: ★ 44차 #9 — **신뢰 경계를 좁혀 명시한다** (44차 리뷰 Q1 답변의 두 갈래 중
#: 후자를 택했다). 39~43차에 걸쳐 "적대적 same-process/namespace writer" 를
#: 위협 모델에 두고 검사를 계속 늘렸지만, 마지막 창은 검사 횟수로 닫히지
#: 않는다: `_commit_guard()` 와 `os.replace` 사이에 다른 valid pointer 가
#: 생기면 그대로 덮는다. 그것을 없애려면 별도 OS principal 이 lock·pointer·
#: generation·원장 namespace 의 create/rename/link/write 를 독점하거나
#: provider 의 원자적 conditional write 가 있어야 한다 — 둘 다 이 저장소의
#: 배포 형태 밖이다.
#:
#: 그래서 **보장을 철회하고 전제를 적는다.** 이 전제가 깨지면 아래 어떤
#: 검사도 손실을 막지 못하고, **탐지하지도 못한다** (45차 정정 — 44차판은
#: "탐지는 된다" 고 적었는데 틀렸다. 마지막 창에서 덮인 pointer 는 아무도
#: 못 본다. generation 바이트는 남지만 "어느 pointer 가 정본이었는가" 는
#: 회수되지 않는다 — 계약 §13.3.1).
_TRUST_BOUNDARY = """cohort 출력 디렉터리(`CURRENT`·`.PENDING`·`gen/`·
`.publish.lock`)와 보존 원장은 **하나의 OS principal 이 소유**하고, 그 안에
쓰는 모든 writer 는 `promote_cohort_generation()` 을 지나 같은 게시 lock 을
따른다. 비협조적 writer(같은 principal 로 lock 없이 pointer 를 바꾸는 코드,
pathname 을 교체하는 코드)는 지원 범위 **밖**이다."""


class _Authority:
    """이 게시가 근거로 삼은 **모든 authority 를 한 번에 고정한** snapshot.

    ★ 43차 #9 — 42차의 raw publisher 는 유효한 lock 만 있으면 caller 가
      `roster` 를 고르고 `recheck=None` 으로 원장을 통째로 우회할 수 있었다::

          with _PublishLock(out) as lock:
              _promote_generation(stage, out, lock=lock,
                                  roster={"caller-chosen-leg"}, recheck=None)

      "private 라는 이름은 trust boundary 가 아니다" 를 우리가 또 어긴 자리다.
      이제 게시에 필요한 **모든 근거**는 이 객체 하나에서만 온다: lock ·
      원장 cohort record 전체 · `CURRENT` bytes · `.PENDING` bytes.
      caller 가 넘길 수 있는 인자가 없다.

    `_ACTIVE` 는 `_authority()` 가 만든 것만 담는다 — 조립한 객체는 여기
    없다. same-process 의 적대적 Python 을 완전한 보안 경계로 만들 수는
    없다 (그 한계는 요청문에 신고한다). 목표는 **우연한 우회 경로를 남기지
    않는 것**이다.
    """

    _ACTIVE: set = set()
    #: ★ 45차 #9 — `cohort` snapshot 을 **뺐다.** sink 가 쓰지 않는데 mutable
    #:   dict 라 "고정된 근거" 를 약하게 만들 뿐이었다 (근거는 `seal` 이다).
    __slots__ = ("out", "lock", "cohort_id", "seal", "roster", "roster_digest",
                 "pend_stale", "producer",
                 "cur_raw", "pend_raw", "base_ptr", "base_raw", "cur_gid",
                 "_sealed")

    def __init__(self, out, lock):
        object.__setattr__(self, "_sealed", False)
        self.out, self.lock = Path(out), lock

    def __setattr__(self, name, value):
        """★ 44차 #9 — 고정된 뒤에는 **바꿀 수 없다.**

        43차 slot 은 mutable 이라, genuine authority 를 받은 caller 가
        `auth.roster` 나 pointer snapshot 을 바꿔도 registry 검사는 그대로
        통과했다. snapshot 이 근거인데 근거를 고칠 수 있으면 근거가 아니다.

        ★ 45차 #9 — **이 동결은 얕았다.** `auth.roster` 가 mutable `set` 이라
          `roster.clear(); roster.add("evil")` 는 `__setattr__` 를 아예 지나지
          않는다. 44차 회귀는 **재대입** 둘만 봤다. 이제 담기는 값 자체가
          immutable 이다 (`frozenset`·`bytes`·`str`) — 특별한 우회가 아니라
          ordinary set API 로 뚫리던 자리였다.
        """
        if getattr(self, "_sealed", False):
            raise SystemExit(
                f"✗ 고정된 게시 authority 를 바꿀 수 없다 ({name}) — "
                "근거는 `_authority()` 가 한 번 고정한 그 값이다")
        object.__setattr__(self, name, value)

    def ledger_seal_now(self) -> str:
        return _ledger_seal(_ledger_cohort(self.out))

    def frozen_values(self) -> bool:
        """담긴 값이 전부 immutable 인가 — 동결이 **얕지 않은지** 본다."""
        return (isinstance(self.roster, frozenset)
                and all(isinstance(x, str) for x in self.roster)
                and isinstance(self.roster_digest, str)
                and isinstance(self.cohort_id, str)
                and isinstance(self.seal, str)
                and all(r is None or isinstance(r, bytes)
                        for r in (self.cur_raw, self.pend_raw, self.base_raw)))

    def pointers_now(self):
        return (_pointer_bytes(self.out, "CURRENT"),
                _pointer_bytes(self.out, ".PENDING"))

    def assert_pointers_unmoved(self) -> None:
        """두 pointer 가 snapshot 그대로인가 — `os.replace` **직전**에 부른다."""
        live_cur, live_pend = self.pointers_now()
        if live_cur != self.cur_raw or live_pend != self.pend_raw:
            raise SystemExit(
                "✗ CURRENT 또는 `.PENDING` 이 그 사이에 움직였다 — 남의 승격을 "
                "덮지 않는다. base 를 다시 읽고 재시도하라")


@contextlib.contextmanager
def _authority(lock: "_PublishLock", out: Path):
    """lock 을 든 채 **원장과 두 pointer 를 한 번에** 고정한다 (43차 #9).

    ★ 42차는 `CURRENT` 와 `.PENDING` 을 각각 한 번씩 읽었지만 **선택한 한
      쪽만** CAS 했다. 그래서 이런 schedule 이 통과했다::

          초기: CURRENT=C0 · 호환 PENDING=P0
          A: C0 를 읽음
          X: CURRENT=C1 을 게시 (P0 는 그대로)
          A: P0 를 base 로 고르고 P0 fingerprint 만 대조 → 통과
          A: CURRENT 를 자기 generation 으로 덮어 C1 을 잃는다

      "각각 한 번 읽는다" 와 "둘을 하나의 authority snapshot 으로 읽는다" 는
      다르다. 그리고 원장도 `set(legs)` 가 아니라 **record 전체**여야 한다 —
      같은 legs 로 `active → frozen` 이 되어도 옛 writer 가 게시했다.
    """
    auth = _Authority(out, lock)
    # ★ 43차 #9 — capability 판정을 **snapshot 을 만들기 전에** 한다.
    #   정확히 그 타입 + unbound 호출 (39~41차의 위조 계보를 그대로 막는다).
    if type(lock) is not _PublishLock:
        raise SystemExit(
            "✗ 게시 lock 없이 authority 를 고정할 수 없다 — "
            "`promote_cohort_generation()` 을 쓰라")
    _PublishLock.assert_held_for(lock, auth.out)
    cohort = _ledger_cohort(auth.out)
    auth.cohort_id = str(cohort.get("cohort_id") or "")
    auth.seal = _ledger_seal(cohort)
    # ★ 45차 #9 — **immutable 값**만 담는다 (`set` → `frozenset`).
    auth.roster = frozenset(cohort.get("legs") or ())
    # ★ 48차 P0-1 — 봉인된 producer 를 authority 에 싣는다 (sink 가 대조한다).
    auth.producer = (_ledger_authority(cohort)["pin"] or {}).get(
        "producer_semantic_sha256", "")
    auth.roster_digest = _roster_digest(auth.roster)
    auth.cur_raw, auth.pend_raw = auth.pointers_now()
    auth.cur_gid = (_parse_pointer(auth.out, "CURRENT", auth.cur_raw)["generation_id"]
                    if auth.cur_raw is not None else None)
    auth.base_ptr = "CURRENT" if auth.cur_raw is not None else ".PENDING"
    # ★ 47차 P1-a — **완전한 `CURRENT` 는 남아 있는 `.PENDING` 을 supersede 한다.**
    #
    #   publisher 는 `os.replace(tmp, CURRENT)` 로 가시성을 넘긴 **뒤**
    #   `.PENDING` 을 지운다. 그 사이에 예외가 나면 (power-loss 가 아니라
    #   평범한 소프트웨어 예외로도) 새 CURRENT 는 유효한데 옛 pending 이 남고,
    #   46차는 그 상태에서 "pending base 가 현재와 다르다" 로 **영구 정지**
    #   했다 — 사람이 파일을 지워야만 풀렸다.
    #
    #   구조적으로 그럴 필요가 없다: `CURRENT` 는 계약상 항상 명부가 찬
    #   generation 이고(불완전한 것은 `.PENDING` 으로만 간다), `.PENDING` 은
    #   완성을 향해 쌓는 중간물이다. 그러므로 유효한 `CURRENT` 옆의
    #   `.PENDING` 은 **정의상 그 이전** 것이고, 버려도 굳은 바이트를 잃지
    #   않는다 (generation 은 immutable 하게 남는다).
    #
    #   `CURRENT` 가 없을 때(=bootstrap 누적 중)는 46차 규칙 그대로다 —
    #   base 가 어긋난 pending 은 승인되지 않은 구성이므로 거부한다.
    auth.pend_stale = auth.pend_raw is not None and auth.cur_raw is not None
    if auth.pend_raw is not None and not auth.pend_stale:
        # ★ 42차 #9 — pending 은 **닫힌 schema** 로 읽는다. key 가 빠지면
        #   `.get()` 의 `None` 이 "bootstrap 이다" 와 구별되지 않는다.
        pend = _parse_pointer(auth.out, ".PENDING", auth.pend_raw,
                              complete=False, pending=True)
        if pend["roster_digest"] != auth.roster_digest:
            raise SystemExit(
                f"✗ 남아 있는 `.PENDING` 이 다른 명부의 것이다 "
                f"({str(pend['roster_digest'])[:12]} ≠ {auth.roster_digest[:12]}) — "
                "승인되지 않은 구성을 이어받지 않는다. 원장을 확정한 뒤 "
                "그 명부로 처음부터 다시 쌓아라. (`.PENDING` 을 지우고 시작하라)")
        # ★ 42차 #9 — 41차는 불일치면 아무 말 없이 `CURRENT` 로 떨어졌다.
        #   bootstrap 중에는 그 fallback 이 곧 stale pending 상속이었다.
        if pend["base_generation"] != auth.cur_gid:
            raise SystemExit(
                f"✗ 남아 있는 `.PENDING` 이 다른 base 위에서 만들어졌다 "
                f"(pending base {str(pend['base_generation'])[:12]} ≠ 현재 "
                f"{str(auth.cur_gid)[:12]}) — 승인되지 않은 구성을 이어받지 "
                "않는다. `.PENDING` 을 지우고 지금의 base 에서 다시 쌓아라")
        auth.base_ptr = ".PENDING"
    auth.base_raw = (auth.pend_raw if auth.base_ptr == ".PENDING"
                     else auth.cur_raw)
    object.__setattr__(auth, "_sealed", True)      # 44차 #9 — 여기서 굳는다
    _Authority._ACTIVE.add(id(auth))
    try:
        yield auth
    finally:
        _Authority._ACTIVE.discard(id(auth))


def _dir_identity(p) -> tuple:
    """디렉터리의 **kernel identity** — pathname 이 아니다 (46차 #9).

    `Path.resolve()` 는 symlink 만 편다. bind mount 는 다른 pathname·같은
    `(st_dev, st_ino)` 이므로 경로 비교로는 보이지 않는다.
    """
    st = os.stat(p)
    return (st.st_dev, st.st_ino)


def _assert_outside_generations(stage: Path, out: Path) -> None:
    """staging 이 generation namespace **안**인가 — 판정은 kernel identity 로.

    ★ 45차는 `resolve()` 로 경로만 봤다. bind mount 는 다른 pathname · 같은
      inode 이므로 안 보였다.

    ★ 46차 초판은 **두 구현**을 나란히 뒀다 (경로 포함 검사 + inode 대조).
      변이 재생이 잡았다: 경로 검사를 통째로 지워도 아무 시험이 안 빨개진다 —
      inode 대조가 같은 경우를 전부 먼저 잡기 때문이다. 두 검사를 따로 두면
      서로를 가린다는 것을 44차에도 실측했고, 이번에도 같은 형태였다.
      그래서 **하나로 합친다**: `stage` 와 그 조상들을 `(st_dev, st_ino)` 로
      `gen/` · 각 generation 과 대조한다. 이 한 함수가 셋을 다 덮는다.

        · stage 가 generation 자신          (44차 반례 — 자기 자신을 지웠다)
        · stage 가 `gen/` 바로 아래
        · stage 가 generation **아래 더 깊은** 디렉터리
        · 위 셋을 bind mount·symlink 로 우회한 경우
    """
    gen = Path(out) / "gen"
    if not gen.is_dir():
        return
    forbidden = {}
    for q in [gen] + [d for d in sorted(gen.iterdir()) if d.is_dir()]:
        try:
            forbidden[_dir_identity(q)] = q
        except OSError:
            continue
    node, seen = Path(stage), set()
    while True:
        try:
            key = _dir_identity(node)
        except OSError:
            return
        hit = forbidden.get(key)
        if hit is not None:
            raise SystemExit(
                f"✗ staging 이 generation namespace 안이다 (inode 일치): "
                f"{stage} → {node} ≡ {hit} — pathname 이 달라도 bind "
                "mount·symlink 면 같은 실물이다. generation 을 입력으로 삼으면 "
                "immutable 하지 않다. 별도 staging 디렉터리를 쓰라")
        if key in seen:
            return
        seen.add(key)
        parent = node.parent
        if parent == node:
            return
        node = parent


def _entries_from_dirfd(dfd: int, what: str) -> dict:
    """붙잡은 dirfd 아래 entry 를 **exact**·no-follow 로 읽는다 (48차 #9).

    `_staging_entries()` 의 body 를 나눈 것이다 — generation namespace 는
    성분마다 붙잡은 fd 로 들어오고, caller staging 은 경로로 들어온다.
    """
    out_map, bad = {}, []
    for name in sorted(os.listdir(dfd)):
        st = os.stat(name, dir_fd=dfd, follow_symlinks=False)
        if not stat.S_ISREG(st.st_mode):        # symlink·FIFO·directory
            bad.append(f"{name}: regular file 이 아니다 "
                       f"({'symlink' if stat.S_ISLNK(st.st_mode) else 'other'})")
            continue
        if st.st_nlink != 1:
            bad.append(f"{name}: 다른 이름과 inode 를 공유한다 "
                       f"(st_nlink={st.st_nlink})")
            continue
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)
        try:
            out_map[name] = _read_all(fd)
        finally:
            os.close(fd)
    if bad:
        raise SystemExit(
            f"✗ {what} 에 게시할 수 없는 entry 가 있다 — generation 은 우리가 "
            "소유한 regular file 만 담는다 (regular · st_nlink == 1 · "
            "no-follow):\n  " + "\n  ".join(bad))
    return out_map


def _staging_entries(stage: Path, out: Path,
                     allow_inside_gen: bool = False,
                     what: str = "staging") -> dict:
    """staging 디렉터리의 **정확한** entry 집합을 bytes 로 읽는다 (45차 #9).

    `Path.is_file()` 은 symlink 를 따라가고, 걸러진 entry 도 디렉터리를
    통째로 옮기면 딸려온다. 여기서는 `lstat` 으로 **따라가지 않고** 보고,
    regular·`st_nlink == 1` 이 아닌 것이 하나라도 있으면 거부한다.

    또 stage 가 generation namespace 안(또는 목적지 자신)이면 거부한다 —
    44차에는 active `gen/<gid>` 를 stage 로 주면 자기 자신과 비교한 뒤
    `rmtree` 로 지웠다.
    """
    stage, out = Path(stage), Path(out)
    if not allow_inside_gen:
        # ★ 46차 #9 — namespace 판정은 **이 함수 하나**다 (경로 사본을 지웠다 —
        #   변이가 안 물었고, 그것은 중복이라는 뜻이었다).
        _assert_outside_generations(stage, out)
    # ★ 47차 #9 — **root 자신도 따라가지 않는다.** 46차는 child 만 lstat/
    #   O_NOFOLLOW 로 열고 root 는 `exists()`·`is_dir()`·`os.listdir(path)` 로
    #   봤다. 그래서 `gen/<gid>` 를 바깥 디렉터리 symlink 로 바꾸면 immutable
    #   generation 의 바이트가 namespace 밖에 있게 되고, 나중에 그 target 을
    #   고치면 "immutable" 이 아니다. child hardlink 는 막으면서 root alias 는
    #   허용하는 경계는 성립하지 않는다.
    #
    #   그리고 root 를 검사한 뒤 child 를 **pathname 으로 다시 열면** 그 사이의
    #   root 교체를 못 본다. 한 번 연 dirfd 를 붙잡고 `openat` 으로만 읽는다.
    dfd = _open_dir_nofollow(stage, what)
    try:
        return _entries_from_dirfd(dfd, what)
    finally:
        os.close(dfd)


def _open_dir_nofollow(d: Path, what: str = "staging") -> int:
    """디렉터리를 **따라가지 않고** 연다. 실패는 fail-closed.

    ★ 48차 — 이 함수는 **마지막 성분만** 보장한다. `O_NOFOLLOW` 는 POSIX 에서
      마지막 성분에만 적용되고 조상은 그대로 따라가기 때문이다. 그래서 신뢰
      경계 안의 경로(=caller 가 준 staging)에만 쓰고, generation namespace 는
      `_open_child_dir()` 로 **성분마다** 붙잡는다.
    """
    try:
        return os.open(d, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as e:
        raise SystemExit(
            f"✗ {what} 을 실물 디렉터리로 열 수 없다: {d} ({e.strerror}) — "
            "symlink·junction 으로 가리킨 디렉터리는 generation 이 될 수 없다 "
            "(바깥에서 바이트가 바뀌면 immutable 이 아니다)") from e


def _open_child_dir(dfd: int, name: str, what: str) -> int:
    """붙잡은 dirfd 아래 **한 성분**을 따라가지 않고 연다 (48차 #9 P0-7).

    47차는 `os.open(out/"gen"/gid, O_DIRECTORY|O_NOFOLLOW)` 하나로 root 를
    열었다. `O_NOFOLLOW` 는 마지막 성분(`<gid>`)만 보므로 `out/gen` 자체를
    바깥 디렉터리 symlink 로 두면 generation 실물이 namespace **밖**에 놓였고
    reader 도 그것을 승인했다. 비협조 writer 도 동시성도 필요 없는, 정적
    오배치 하나짜리 반례였다.

    신뢰하는 `out` 에서 시작해 `gen` → `<gid>` 를 각각 이 함수로 붙잡는다.
    """
    if "/" in name or name in (".", ".."):
        raise SystemExit(f"✗ generation namespace 성분이 아니다: {name!r}")
    try:
        return os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                       dir_fd=dfd)
    except OSError as e:
        raise SystemExit(
            f"✗ {what} 성분 {name!r} 을 실물 디렉터리로 열 수 없다 "
            f"({e.strerror}) — generation namespace 의 어느 성분도 symlink·"
            "junction 일 수 없다 (그러면 바이트가 namespace 밖에 놓인다)") from e


@contextlib.contextmanager
def _generation_dirfd(out: Path, gid: str | None = None):
    """`out` → `gen` → `<gid>` 를 **성분마다** 붙잡는다 (48차 #9 P0-7).

    `gid` 가 `None` 이면 `gen` 까지만 연다 (생성 경로용).
    """
    ofd = _open_dir_nofollow(Path(out), "cohort 출력 디렉터리")
    gfd = None
    try:
        gfd = _open_child_dir(ofd, "gen", "generation namespace")
        if gid is None:
            yield gfd
            return
        dfd = _open_child_dir(gfd, str(gid), "generation")
        try:
            yield dfd
        finally:
            os.close(dfd)
    finally:
        if gfd is not None:
            os.close(gfd)
        os.close(ofd)


def _generation_entries_by_id(out: Path, gid: str) -> dict:
    """generation 을 **성분마다 붙잡은** fd 로 읽는다 (48차 #9 P0-7)."""
    with _generation_dirfd(out, gid) as dfd:
        return _entries_from_dirfd(dfd, "generation")


def _generation_entries(gdir: Path, out: Path) -> dict:
    """굳은 generation 을 **자재화와 같은 validator** 로 읽는다 (46차 #9).

    45차는 no-follow·`nlink == 1` 검사를 자재화 경로에만 뒀다. 독자와 멱등
    분기는 `Path.is_file()` + `read_bytes()` 였으므로, generation 안의 파일에
    바깥에서 hardlink 를 걸면 "immutable generation" 의 바이트를 바깥 이름으로
    바꿀 수 있는데도 둘 다 통과했다. 세 소비자가 같은 함수를 지난다.
    """
    return _staging_entries(gdir, out, allow_inside_gen=True, what="generation")


def _read_all(fd: int) -> bytes:
    chunks = []
    while True:
        b = os.read(fd, 1 << 20)
        if not b:
            return b"".join(chunks)
        chunks.append(b)


def _write_owned(dst: Path, data: bytes) -> None:
    """**새 inode** 에 bytes 를 쓰고 fsync 한다 (alias 를 들여오지 않는다)."""
    fd = os.open(dst, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o644)
    try:
        n = 0
        while n < len(data):
            n += os.write(fd, data[n:])
        os.fsync(fd)
    finally:
        os.close(fd)


def _promote_generation(stage: Path, auth: "_Authority") -> dict:
    """staging 을 immutable generation 으로 굳히고 pointer 를 옮긴다.

    ★ 36차 #9b — **비공개다.** 이 함수는 staging 을 그대로 믿으므로 한 파일
      짜리 staging 을 넘기면 cohort 를 한 파일로 줄인 generation 이 정상
      게시된다. 완전성을 보는 유일한 입구는 cohort publisher 다.

    ★ 43차 #9 — 그런데 42차까지 그 "유일한 입구" 를 **인자로 우회**할 수
      있었다 (`roster=` · `recheck=None`). 이제 근거는 `auth` 하나에서만
      오고, `auth` 는 `_authority()` 만 만든다.
    """
    if type(auth) is not _Authority or id(auth) not in _Authority._ACTIVE:
        raise SystemExit(
            "✗ 게시 authority 없이 pointer 를 옮길 수 없다 — "
            "`promote_cohort_generation()` 을 쓰라 (원장·lock·두 pointer 를 "
            "한 번에 고정한 snapshot 만 근거가 된다)")
    out, lock = auth.out, auth.lock
    # ★ 38차 #9 — **유효한 lock 을 들고 있어야** pointer 를 옮길 수 있다.
    # ★ 40차 #9 — **구체 타입**이어야 한다 (duck-typed method 이름 금지).
    # ★ 41차 #9 — `isinstance` + virtual 호출은 둘 다 인스턴스가 고를 수 있다.
    #   **정확히 그 타입** + **unbound** 호출이어야 한다.
    if type(lock) is not _PublishLock:
        raise SystemExit(
            "✗ 게시 lock 없이 CURRENT 를 옮길 수 없다 — "
            "`promote_cohort_generation()` 을 쓰라")
    _PublishLock.assert_held_for(lock, out)
    stage = Path(stage)
    _assert_writable(out)
    # ★ 45차 #9 — **자재화 전에 staging 자체를 검사한다.** 44차는 셋을 놓쳤다:
    #   (a) stage 가 현재 active `gen/<gid>` 자신이면 idempotent 분기가 그
    #       디렉터리를 자기 자신과 비교한 뒤 `rmtree(stage)` 로 **지웠고**,
    #       같은 gid 를 다시 `CURRENT` 로 게시했다 (public API 만으로 성립).
    #   (b) `Path.is_file()` 은 symlink 를 따라가므로 alias stage 가 그대로
    #       generation 으로 **이동**했다 — 나중에 바깥 target 을 고치면
    #       "immutable" generation 바이트가 바뀐다.
    #   (c) directory·FIFO·broken link 는 `is_file()` 에서 빠지지만 디렉터리
    #       **이동**에는 딸려가 record 밖 untracked entry 가 됐다.
    entries = _staging_entries(stage, out)
    files = {n: _sha(b) for n, b in entries.items()}
    if not files:
        raise SystemExit(f"✗ staging 이 비었다: {stage}")
    gid = generation_id(files)
    # ★ 44차 #9 — **되돌릴 수 없는 sink 가 자기 불변식을 스스로 본다.**
    #   43차는 exact suffix 와 `assert_cohort_complete()` 를 wrapper 에만 두고,
    #   sink 는 leg **이름 집합**만 roster 와 대조했다. 그래서 genuine
    #   authority 를 든 caller 가 `{a.projection.yaml, b.projection.yaml}` 로
    #   roster {a,b} 를 만족시켜 **reader 가 못 읽는 active state** 를 게시할
    #   수 있었다. (36차에 이 사본을 "중복" 이라며 지웠던 것이 37차에 오판으로
    #   판명된 그 자리다 — sink 는 wrapper 의 검사를 신뢰하지 않는다.)
    #   sink 가 부르는 것은 **reader 와 같은 validator** 하나다 (leg 마다 세
    #   파일 exact set · 빈 generation 금지 · active 로 갈 때는 명부 일치).
    #   두 검사를 따로 두면 서로를 가려 변이가 안 문다 — 실측했다.
    #   자재화보다 **먼저** 불러야 거부가 아무것도 남기지 않는다.
    seen = {_leg_of(n) for n in files}
    # ★ 45차 #9 — **모든 경로에서** 명부의 부분집합이어야 한다. 44차는
    #   `seen == roster` 일 때만 명부를 대조해서, complete 한 **undeclared**
    #   leg (`evil.*` 세 파일) 가 `.PENDING` 으로 게시됐다. 다음 publisher 가
    #   그 pending 을 base 로 읽고 undeclared 검사에서 막혀, 사람이 치우기
    #   전까지 cohort 가 멈춘다. equality 는 active/pending **선택**에만 쓴다.
    undeclared = sorted(seen - auth.roster)
    if undeclared:
        raise SystemExit(
            f"✗ 명부에 없는 다리를 게시하려 한다: {undeclared} "
            f"(roster={sorted(auth.roster)}) — 원장을 먼저 고쳐라")
    assert_cohort_complete(
        files, gid, expect_legs=auth.roster if seen == auth.roster else None)
    # ★ 48차 P0-1 — 봉인한 producer 를 **실제 바이트**에 결속한다. 이 대조가
    #   없으면 봉인은 "무엇을 승인했는가" 만 말하고 들어온 것은 안 본다.
    assert_producer_binding(entries, auth.producer, "게시하려는 generation")
    gdir = out / "gen" / gid

    if gdir.is_dir():
        # 같은 내용이면 멱등. 다른 바이트가 있으면 **덮지 않고 거부**한다.
        # ★ 46차 #9 — 멱등 분기도 **자재화와 같은 validator** 를 지난다.
        #   45차는 여기서 `is_file()` + `read_bytes()` 였으므로 alias 가 걸린
        #   generation 을 "같은 내용" 으로 보고 그대로 CURRENT 로 올렸다.
        got = {n: _sha(b) for n, b in _generation_entries_by_id(out, gid).items()}
        if got != files:
            raise SystemExit(
                f"✗ generation {gid[:16]} 자리에 다른 내용이 있다 — immutable "
                f"generation 은 덮지 않는다 (기대 {sorted(files)} · 실제 {sorted(got)})")
    else:
        # ★ 45차 #9 — caller 디렉터리를 **옮기지 않는다.** 우리가 읽은
        #   바이트로 **새 inode** 를 만든다. rename 은 alias(symlink·hardlink)
        #   와 untracked entry 를 그대로 들여왔고, 그러면 게시 뒤 바깥에서
        #   generation 을 고칠 수 있다 (= immutable 이 아니다).
        # ★ 48차 #9 P0-7 — `gen` 을 만들 때도 조상을 따라가지 않는다.
        out.mkdir(parents=True, exist_ok=True)
        _ofd = _open_dir_nofollow(out, "cohort 출력 디렉터리")
        try:
            try:
                os.mkdir("gen", dir_fd=_ofd)
            except FileExistsError:
                pass
            os.close(_open_child_dir(_ofd, "gen", "generation namespace"))
        finally:
            os.close(_ofd)
        _fsync_dir(out)
        tmp = out / "gen" / f".{gid}.{uuid.uuid4().hex}.tmp"
        tmp.mkdir()
        for name in sorted(entries):
            _write_owned(tmp / name, entries[name])
        # 우리가 만든 것을 **되읽어** 확인한다 (이름·바이트·regular·nlink)
        back = _staging_entries(tmp, out, allow_inside_gen=True)
        if back != entries:
            raise SystemExit(
                f"✗ generation {gid[:16]} 을 자재화한 바이트가 staging 과 "
                "다르다 — 게시하지 않는다")
        _fsync_dir(tmp)
        os.rename(tmp, gdir)              # generation 이 통째로 보인다
        _fsync_dir(out / "gen")
    # ★ 46차 #9 — **caller 의 staging 을 지우지 않는다.** 45차는 두 분기 모두
    #   `shutil.rmtree(stage)` 로 끝났다. staging 은 caller 가 소유한 입력이고,
    #   publisher 가 거기에 쓰거나 지우면 caller 가 무엇을 주든 (자기 소스
    #   디렉터리든 bind alias 든) 파괴된다. 만든 쪽이 치운다 (`main()`).

    # ★ 46차 #9 — pointer 는 **봉인 하나**만 싣는다. 45차는 `cohort_id` 를
    #   echo 로 함께 실었지만 비교는 하지 않았다 (봉인이 덮으므로 중복이라고
    #   판단했다 — 실제로 그 대조 변이가 안 물었다). 그러면 그 필드는 seal 과
    #   **어긋날 수 있는 진단 문자열**로 남는다: 사람이 읽는 오류 메시지가
    #   거짓말을 한다. 대조를 더하는 대신 **필드를 없앤다** — 진단이 필요하면
    #   그때 살아 있는 원장에서 읽는다 (아래 `_parse_pointer` 가 그렇게 한다).
    rec = {"schema": CURRENT_SCHEMA, "generation_id": gid, "files": files,
           "ledger_seal": auth.seal}

    def _commit_guard():
        """**가시성 전환 직전에** 근거 전체를 다시 결속한다 (42·43차 #9).

        ★ 42차 — 41차의 마지막 lock 검사는 이 함수 초입에서 끝났고, 그 뒤
          staging scan·자재화·fsync·CAS 동안 sentinel pathname 을 갈아 끼울
          수 있었다. 그래서 pointer 를 옮기기 직전에 다시 보게 했다.

        ★ 43차 — 그런데 42차의 pointer CAS 는 이 guard **밖**에서, 그것도
          base 한 쪽만 대조했다. 그래서 (a) CAS 뒤 commit 전에 pointer 를
          바꾸면 그대로 덮었고 (b) base 가 아닌 pointer 의 변화는 아예 안
          봤다. 대조를 전부 여기로 옮기고 **두 pointer 를 다** 본다.
          원장도 `set(legs)` 가 아니라 record 전체 seal 로 본다.

          실패하면 이미 굳은 generation directory 는 immutable 잔여로 남을
          뿐 어떤 reader 에게도 보이지 않는다 (가시성 전환점은 pointer 하나다).

          이 재검사가 검사-직후 창까지 없애지는 못한다. 그것을 없애려면 lock
          namespace 의 write authority 를 publisher 하나로 제한해야 하고,
          그것은 설계 항목으로 신고한다.
        """
        _PublishLock.assert_held_for(lock, out)
        # ★ 48차 — **쓰기 권한은 살아 있는 원장에서 다시 본다.**
        #
        #   43차가 못 박은 것: 게시 도중 cohort 가 얼면 옛 writer 는 져야 한다
        #   (freeze 는 진행 중인 게시보다 우선하는 전환이다). 그때는 `status` 가
        #   봉인 안에 있어서 seal 대조가 그 일을 대신 해 줬다.
        #
        #   48차에 `status` 를 봉인에서 뺐다 — 얼린 cohort 의 CURRENT 가 영원히
        #   재검증 불가가 되기 때문이다. 그래서 그 검사를 **원래 있어야 할
        #   자리**로 옮긴다: 봉인(과거의 사본)이 아니라 임계 구역 안에서 읽는
        #   **현재의 사실**. 두 요구는 충돌하지 않는다 — 서로 다른 질문이었다.
        _live = _ledger_cohort(out)
        if _live.get("status") != "active":
            raise SystemExit(
                f"✗ 원장 cohort 가 게시 도중에 active 가 아니게 됐다 "
                f"({_live.get('status')!r}) — freeze 는 진행 중인 게시보다 "
                "우선한다. 아무 것도 옮기지 않고 멈춘다")
        # ★ 49차 P0 — 임계 구역 안에서 **다시** 본다. 사전 점검은 판정 전용
        #   사본이고 게시의 근거는 여기서 읽은 값이다.
        assert_not_thawed(_live["cohort_id"])
        if auth.ledger_seal_now() != auth.seal:
            raise SystemExit(
                "✗ 원장이 게시 도중에 바뀌었다 — 옛 근거로 게시하지 않는다. "
                "원장을 확정한 뒤 다시 시도하라")
        _Authority.assert_pointers_unmoved(auth)

    # ★ 39차 #9 — **명부가 다 차야** active pointer 를 옮긴다. bootstrap
    #   partial 을 active `CURRENT` 로 게시하면 roster 를 받지 않는 public
    #   reader 가 그것을 정상으로 읽는다. generation directory 는 이미
    #   immutable 하게 굳었으므로 잃는 것은 없다.
    if seen != auth.roster:
        # bootstrap 중이다 — generation 은 굳었지만 **active 가 아니다.**
        # ★ 40차 #9 — **어느 명부·어느 base 의 것인지** 함께 봉인한다.
        _commit_guard()
        _publish_pointer(out, dict(rec, roster_digest=auth.roster_digest,
                                   base_generation=auth.cur_gid),
                         name=".PENDING", auth=auth)
        return dict(rec, published=False,
                    pending=sorted(auth.roster - seen))
    _commit_guard()
    _publish_pointer(out, rec, auth=auth)
    (out / ".PENDING").unlink(missing_ok=True)     # 명부가 찼다 — 더는 필요 없다
    _materialize(out, rec)      # 호환 사본 — 권위는 CURRENT 다
    return dict(rec, published=True)


def read_current(out: Path, expect_legs=None) -> dict:
    """CURRENT 를 따라간다. 없거나 깨졌거나 실물과 어긋나면 **fail-closed**."""
    return _read_pointer(out, "CURRENT", expect_legs=expect_legs)


def _roster_digest(roster) -> str:
    """명부의 정본 digest — pending 이 **어느 명부의 것인지** 봉인한다."""
    return hashlib.sha256(
        json.dumps(sorted(roster or ()), separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _pointer_bytes(out: Path, name: str):
    """pointer 파일의 raw bytes — **읽는 자리는 여기 하나다** (42차 #9).

    parse 와 fingerprint 를 서로 다른 read 에서 얻으면 그 사이에 교체된
    authority 를 못 본다 (41차가 그랬다). 모든 소비자가 이 함수를 지나고,
    한 판정에 쓰이는 값들은 **한 번의 반환값**에서 나온다.
    """
    p = Path(out) / name
    return p.read_bytes() if p.is_file() else None


def _pointer_fingerprint(out: Path, name: str):
    """그 pointer 파일의 **바이트 전체** digest — CAS 의 기대값 (41차 #9).

    `generation_id` 는 `files` 만 요약한다. `.PENDING` 이 싣는
    `roster_digest`·`base_generation` 은 그 밖이므로, gid 로 CAS 하면 같은
    generation·다른 authority metadata 교체가 통과한다.
    """
    raw = _pointer_bytes(out, name)
    return _sha(raw) if raw is not None else None


def _read_pointer(out: Path, name: str, expect_legs=None,
                  complete: bool = True, pending: bool = False,
                  bind_ledger: bool = True) -> dict:
    raw = _pointer_bytes(out, name)
    if raw is None:
        raise SystemExit(f"✗ CURRENT 가 없다: {Path(out) / name}")
    return _parse_pointer(out, name, raw, expect_legs=expect_legs,
                          complete=complete, pending=pending,
                          bind_ledger=bind_ledger)


#: `.PENDING` 이 싣는 **닫힌** key 집합 (42차 #9). authority 를 담는 pointer 는
#: 계약이 닫혀 있어야 한다 — key 가 빠지면 `.get()` 이 `None` 을 돌려주고,
#: 그 `None` 이 "bootstrap 이다" 와 구별되지 않는다.
#: ★ 45차 #9 — pointer 가 **어느 cohort·어느 원장 record 아래** 게시됐는지
#:   함께 봉인한다. 44차까지 `CURRENT` 는 generation ID 와 files 뿐이라,
#:   원장의 roster·status·cohort ID 가 바뀐 뒤에는 published state 의 authority
#:   를 판정할 수 없었다 (reader 는 원장을 보지도 않았다).
_CURRENT_KEYS = {"schema", "generation_id", "files", "ledger_seal"}
_PENDING_KEYS = _CURRENT_KEYS | {"roster_digest", "base_generation"}


def _parse_pointer(out: Path, name: str, raw: bytes, expect_legs=None,
                   complete: bool = True, pending: bool = False,
                   bind_ledger: bool = True) -> dict:
    out = Path(out)
    p = out / name
    try:
        rec = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        raise SystemExit(f"✗ CURRENT 를 읽을 수 없다: {p} ({e})") from e
    if not isinstance(rec, dict) or rec.get("schema") != CURRENT_SCHEMA \
            or not isinstance(rec.get("files"), dict):
        raise SystemExit(f"✗ CURRENT schema 가 계약이 아니다: {rec!r}")
    want_keys = _PENDING_KEYS if pending else _CURRENT_KEYS
    if set(rec) != want_keys:
        raise SystemExit(
            f"✗ `{name}` 의 key 가 계약과 다르다: "
            f"{sorted(set(rec) ^ want_keys)} — authority 를 담는 pointer 는 "
            "닫힌 schema 여야 한다 (빠진 key 의 `None` 은 bootstrap 과 "
            "구별되지 않는다)")
    # ★ 45차 #9 — **published state 를 원장에 결속한다.** reader 도 대조한다:
    #   원장의 roster·status·cohort ID 가 바뀌었으면 이 pointer 는 더 이상
    #   그 원장 아래의 authority 가 아니다 (roster 는 cohort lifetime 동안
    #   immutable 이고, 바꾸려면 새 cohort ID 로 간다 — 계약 §13.3.2).
    if bind_ledger:
        cohort = _ledger_cohort(out)
        # ★ 46차 #9 — 봉인 **하나**가 authority 다. pointer 에 `cohort_id`
        #   echo 를 따로 싣지 않으므로 (그 echo 는 seal 과 어긋날 수 있는 사본
        #   이었다) 진단용 ID 는 **살아 있는 원장**에서 지금 읽는다.
        live = _ledger_seal(cohort)
        if rec["ledger_seal"] != live:
            raise SystemExit(
                f"✗ `{name}` 이 봉인한 원장 record 가 지금과 다르다 "
                f"({rec['ledger_seal'][:12]} ≠ {live[:12]}; 원장 cohort "
                f"{cohort.get('cohort_id')!r}) — cohort lifetime 동안 원장 "
                "record(명부·상태·producer pin·사용 정책)는 고정이다. 그 중 "
                "무엇이든 바꾸려면 **새 cohort ID 와 새 출력 디렉터리**로 "
                "가라 (계약 §13.3.2)")
    gid = rec.get("generation_id")
    if generation_id(rec["files"]) != gid:
        raise SystemExit(f"✗ CURRENT 의 generation_id 가 files 와 다르다")
    gdir = out / "gen" / str(gid)
    if not gdir.is_dir():
        raise SystemExit(f"✗ CURRENT 가 없는 generation 을 가리킨다: {gid[:16]}")
    # ★ 46차 #9 — 독자도 **자재화와 같은 validator** 를 지난다 (no-follow ·
    #   regular · `st_nlink == 1`). 45차 독자는 `is_file()` 이었으므로 바깥
    #   hardlink 로 바이트를 바꿀 수 있는 generation 을 immutable 로 읽었다.
    _ents = _generation_entries_by_id(out, gid)
    got = {n: _sha(b) for n, b in _ents.items()}
    if got != rec["files"]:
        raise SystemExit(f"✗ generation {gid[:16]} 의 실물이 CURRENT 와 다르다")
    if bind_ledger:
        # ★ 48차 P0-1 — 독자도 generation 안 **모든 leg** 의 producer 를 본다.
        assert_producer_binding(
            _ents, (_ledger_authority(cohort)["pin"] or {}).get(
                "producer_semantic_sha256", ""), f"`{name}` 의 generation")
    # `.PENDING` 은 정의상 불완전할 수 있다 — 완전성은 `CURRENT` 의 계약이다.
    if complete:
        assert_cohort_complete(rec["files"], gid, expect_legs=expect_legs)
    return rec


def assert_producer_binding(entries: dict, want: str, where: str) -> None:
    """generation 의 **모든 leg 가 봉인된 producer 를 스스로 밝히는가** (48차 P0-1).

    47차는 `producer_semantic_sha256` 을 원장 봉인에 넣었지만 publisher 도
    reader 도 **파일 안**을 보지 않았다. 그래서 원장 pin 을 A 로 그대로 둔 채
    B 가 만든 세 파일을 넘기면 A+B generation 이 만들어졌다 — 봉인은 "무엇을
    승인했는가" 만 말하고 "실제로 무엇이 들어왔는가" 는 말하지 않았다.

    manifest 는 `<leg>.projection.yaml` 이고 `analyzer.producer_semantic_sha256`
    을 담아야 한다. 없으면 거부한다 — 밝히지 않은 것은 대조할 수 없다.
    """
    import yaml

    bad = []
    for name in sorted(entries):
        if not name.endswith(".projection.yaml"):
            continue
        try:
            doc = yaml.safe_load(entries[name].decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as e:
            bad.append(f"{name}: manifest 를 읽을 수 없다 ({e})")
            continue
        got = ((doc or {}).get("analyzer") or {}).get("producer_semantic_sha256") \
            if isinstance(doc, dict) else None
        if not isinstance(got, str) or not got:
            bad.append(f"{name}: `analyzer.producer_semantic_sha256` 이 없다")
        elif got != want:
            bad.append(f"{name}: producer {got} ≠ 봉인 {want}")
    if bad:
        raise SystemExit(
            f"✗ {where} 의 producer 가 원장 봉인과 다르다 — 한 cohort 안에 "
            "서로 다른 producer 가 만든 leg 를 섞지 않는다:\n  "
            + "\n  ".join(bad))


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
    # ★ 39차 #9 — **caller 의 신고를 믿지 않는다.** 38차판은 bare set 을 그대로
    #   받아, 원장에 없는 leg 를 caller 가 roster 에 넣어 승인시킬 수 있었다.
    #   필수 인자는 *누락*을 막을 뿐 provenance 를 만들지 않는다. `out` 을 원장
    #   cohort 로 resolve 해 **직접 읽고**, caller 의 신고와 다르면 거부한다
    #   (인자는 이제 "내가 이렇게 알고 있다" 는 주장이고, 원장이 정본이다).
    # ★ 41차 #9 — 원장 조회를 **임계 구역 안**으로 옮긴다. 40차는 lock 밖에서
    #   읽고 비교했으므로, 그 사이에 원장 authority 가 바뀌면 임계 구역이 옛
    #   값으로 게시했다. 원장은 이 게시의 근거이므로 근거를 읽는 순간부터
    #   상호배제 안이어야 한다.
    claimed = set(roster or ())
    # ★ 47차 P1-b — **첫 write 전에** 원장 authority 를 확정한다. 46차는 exact
    #   status·pin·policy 검사가 `_ledger_seal()` 안에 늦게 있어서, 그 앞에서
    #   lock 파일·출력 디렉터리·private temp 가 만들어질 수 있었다. crash 가
    #   나면 frozen namespace 에 잔여물이 남는다.
    #
    #   여기서 읽는 것은 **판정 전용 사본**이고, 게시의 근거는 여전히 임계
    #   구역 안에서 다시 읽는 `_authority()` 다 (그 사이 변경은 seal 대조가
    #   잡는다). 이 앞선 검사는 "쓰기 전에 거절한다" 만 담당한다.
    _pre = _ledger_cohort_preflight(Path(out))
    if _pre.get("status") != "active":
        raise SystemExit(
            f"✗ cohort {_pre.get('cohort_id')!r} 가 active 가 아니다 "
            f"({_pre.get('status')!r}) — frozen cohort 에는 쓸 수 없다. "
            "아무 것도 만들지 않고 멈춘다")
    # ★ 49차 P0 — 원장이 `active` 라고 **말하는** 것과 이 cohort 가 얼린 적이
    #   없다는 것은 다른 주장이다. 앞의 것은 사람이 고칠 수 있는 한 줄이고,
    #   뒤의 것은 되돌릴 수 없는 journal 이 답한다.
    assert_not_thawed(_pre["cohort_id"])
    # ★ 49차 P0 — 얼렸다는 **흔적**이 원장에 남아 있는데 status 만 active 인
    #   경우도 해동이다. journal 이 생기기 전에 얼린 cohort(g1·g2)까지 덮는다.
    if _pre.get("frozen_reason"):
        raise SystemExit(
            f"✗ cohort {_pre['cohort_id']!r} 에 `frozen_reason` 이 남아 있다 "
            f"({_pre['frozen_reason']!r}) — status 만 active 로 되돌린 해동이다. "
            "얼린 cohort 는 자라지 않는다. 새 cohort 를 만들어라")
    _pre_roster = set(_pre.get("legs") or ())
    if claimed != _pre_roster:
        raise SystemExit(
            f"✗ 신고한 roster {sorted(claimed)} 가 원장 {sorted(_pre_roster)} 와 "
            "다르다 — 원장이 정본이다 (아무 것도 만들지 않고 멈춘다)")
    with _PublishLock(out) as lock, _authority(lock, out) as auth:
        if claimed != auth.roster:
            raise SystemExit(
                f"✗ 신고한 roster {sorted(claimed)} 가 원장 "
                f"{sorted(auth.roster)} 와 다르다 — 원장이 정본이다")
        # 게시는 lifecycle 을 **움직이지 않는다.** 기록해야 할 전이는 freeze
        # 하나뿐이고(`freeze_cohort()`), "아직 안 얼었다" 를 매 게시마다
        # 적으면 journal 이 게시 로그가 된다 — 그것은 다른 파일의 일이다.
        return _promote_cohort_locked(stage, auth, leg)


def _promote_cohort_locked(stage: Path, auth: "_Authority", leg: str) -> dict:
    """★ 43차 #9 — base 선택·명부·pointer 는 전부 `auth` 에서 온다.

    42차는 이 함수가 원장과 두 pointer 를 **직접** 읽고 그 값을 raw publisher
    에 인자로 넘겼다. 인자로 넘길 수 있으면 인자로 위조할 수 있다.
    """
    out = auth.out
    stage = Path(stage)
    # ── 1. caller staging 을 **처음부터 no-follow exact read** 로 본다 ──────
    # ★ 46차 #9 — 45차는 `{p.name for p in stage.iterdir() if p.is_file()}` 로
    #   이름 집합을 먼저 얻었다. `is_file()` 은 symlink 를 **따라가므로**
    #   dangling symlink 는 그 집합에서 조용히 빠졌고, exact-set 검사를 통과한
    #   뒤 아래 base 복사(`shutil.copyfile`)가 그 symlink 를 목적지에서
    #   **따라가** cohort 디렉터리 **바깥**에 파일을 만들었다 (public API 만으로
    #   성립한 반례다). 이제 첫 접촉이 `_staging_entries()` 이고, 그것이
    #   regular · `st_nlink == 1` · no-follow 를 강제한다.
    fresh_bytes = _staging_entries(stage, out)
    fresh = set(fresh_bytes)
    # ★ 34차 #9 — "완전한 snapshot" 을 **구조로** 강제한다. 초판은 stage 의
    #   이름 집합을 얻은 뒤 그 leg 의 기존 파일을 base 에서 전부 제외했지만,
    #   stage 가 exact set 인지 보지 않았다. `{a.projection.yaml}` 만 넘기면
    #   그 leg 의 CSV·restart 를 **제거한** generation 이 정상 게시됐다.
    want = {f"{leg}{sfx}" for sfx in LEG_SUFFIXES}
    if fresh != want:
        raise SystemExit(
            f"✗ {leg} 의 staging 이 세 파일 exact set 이 아니다 — 남음 "
            f"{sorted(fresh - want)} · 모자람 {sorted(want - fresh)}")

    # ── 2. base generation 도 **같은 safe reader** 로 읽는다 ────────────────
    base: dict = {}
    base_bytes: dict = {}
    if auth.base_raw is None:
        # ★ 46차 #9 — pointer 가 **둘 다** 없는데 generation 이 이미 있으면
        #   그것은 bootstrap 이 아니라 **pointer 소실**이다. 45차는 이 상태에서
        #   한 leg 만 담은 새 계보를 조용히 시작했고, 그 순간 "roster 는 cohort
        #   수명 동안 불변" 이 깨졌다 — 무엇이 지워졌는지 알 방법이 없다
        #   (durable history 를 두지 않기로 했으므로 복구할 근거가 없다).
        #   지속 이력을 만드는 대신 **terminal fail-closed** 로 선언한다.
        gen_root = out / "gen"
        lost = sorted(q.name[:16] for q in gen_root.iterdir()
                      if q.is_dir() and not q.name.startswith(".")) \
            if gen_root.is_dir() else []
        if lost:
            raise SystemExit(
                f"✗ cohort 에 generation 이 {len(lost)} 개 있는데 `CURRENT` 도 "
                f"`.PENDING` 도 없다 ({out}) — bootstrap 이 아니라 pointer "
                "소실이다. 여기서 새 계보를 시작하면 명부 불변식이 조용히 "
                "깨진다(무엇이 있었는지 알 수 없다). 이 cohort 는 여기서 "
                "끝이다 — **새 cohort ID 와 새 출력 디렉터리**로 가라 "
                "(계약 §13.3.2)")
    else:
        # base 는 **명부 부분집합**이면 된다. 여기서 exact 를 요구하면
        # bootstrap 이 불가능하다. exact 는 **reader** 의 주장이다.
        # ★ 42차 #9 — record 와 기대 digest 가 **같은 바이트**에서 나온다.
        cur = _parse_pointer(out, auth.base_ptr, auth.base_raw,
                             pending=auth.base_ptr == ".PENDING",
                             complete=auth.base_ptr != ".PENDING")
        base = dict(cur["files"])
        gdir = out / "gen" / cur["generation_id"]
        base_bytes = _generation_entries_by_id(out, cur["generation_id"])

    # ── 3. 병합은 **메모리에서** 한다 — caller 경로에 쓰지 않는다 ──────────
    # ★ 36차 #9b — base 완전성 검사를 여기서 **뺐다.** `read_current()` 가
    #   모든 독자에 대해 같은 것을 보므로 여기 사본은 중복이었다 — 변이로
    #   확인했다: 그 loop 를 지워도 suite 가 초록이었다.
    merged = dict(fresh_bytes)
    for name, want_sha in sorted(base.items()):
        if _leg_of(name) == leg:
            continue                       # 이번 갱신이 대체한다
        blob = base_bytes.get(name)
        if blob is None or _sha(blob) != want_sha:
            raise SystemExit(
                f"✗ base generation 의 {name} 이 그 pointer 와 다르다 — "
                "옛 generation 을 근거로 새 generation 을 만들지 않는다")
        merged[name] = blob
    # ★ 37차 #9 — publish 쪽에서도 **같은** validator 를 부른다. 36차에 이
    #   사본을 지웠던 것은 오판이었다: 변이가 안 문 것은 중복이어서가 아니라
    #   validator 가 약해서였다. 기대 명부는 base 에 있던 leg 들 ∪ {이번 leg}
    #   — 승격이 남의 leg 를 **줄이는** 것을 여기서 막는다.
    # ★ 38차 #9 — 명부에 대한 publisher 의 의무는 둘이다. exact 는 위에서
    #   설명한 이유로 여기서 요구할 수 없고, **reader** 가 요구한다.
    #     1) 명부에 없는 leg 를 만들지 않는다
    #     2) 이미 있던 leg 를 **줄이지 않는다** (한 leg 갱신이 cohort 를 깎지
    #        못하게 — 34차부터의 요구다)
    staged = {n: _sha(b) for n, b in merged.items()}
    have = {_leg_of(n) for n in staged}
    undeclared = sorted(have - auth.roster)
    if undeclared:
        raise SystemExit(
            f"✗ 명부에 없는 다리를 게시하려 한다: {undeclared} "
            f"(roster={sorted(auth.roster)}) — 원장을 먼저 고쳐라")
    #   (기존 leg 를 줄이는 것은 위 base 병합이 구조로 막는다 — 검사를 하나
    #    더 두려 했으나 도달 불가능이었다. 확인했고 두지 않는다.)
    assert_cohort_complete(staged, "staging")

    # ── 4. **publisher 소유** private temp 에만 자재화한다 ──────────────────
    #   실패하면 이 temp 만 지운다. caller 의 stage 는 어느 경로에서도
    #   write·copy·unlink·rmtree 대상이 아니다.
    out.mkdir(parents=True, exist_ok=True)
    work = out / f".merge.{uuid.uuid4().hex}.tmp"
    work.mkdir()
    try:
        for name in sorted(merged):
            _write_owned(work / name, merged[name])
        return _promote_generation(work, auth)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def _ledger_cohorts() -> list[dict]:
    """보존 원장의 cohort 목록 — **하나의 parser** 가 위생을 강제한다 (41차 #9).

    ★ 40차는 소비자 넷이 원장을 각자 파싱했다. `_ledger_roster()` 에만 "같은
      디렉터리 중복" 검사를 붙였고, `_cohort_dir()` 은 **첫 ID** 를 즉시
      돌려주고 `_frozen_cohort_dirs()` 는 dict comprehension 으로 조용히
      덮었다. 그래서 같은 `cohort_id` 가 서로 다른 디렉터리에 두 번 있으면
      authority 가 다시 **목록 순서**에 달렸다 — 이 저장소가 반복해서 겪은
      형태다 (30차 P2, 39차 #9, 40차 #9).

      ID 도 디렉터리도 유일해야 하고, 그 판정은 어느 소비자를 부르든·원장
      항목 순서가 어떻든 같아야 한다. 그래서 조회 **전에** 전체를 본다.
    """
    import yaml

    reg_path = REPO / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"
    if not reg_path.is_file():
        # ★ 28차 P1-5 — 원장이 없으면 빈 값을 돌려 **fail-open** 했다.
        #   보호 장치가 없다는 뜻이므로 쓰지 못하게 막는 것이 맞다.
        raise SystemExit(
            f"✗ 보존 원장이 없다: {reg_path} — cohort 명부·frozen 여부를 알 수 "
            "없으므로 아무 데도 쓰지 않는다")
    reg = yaml.safe_load(reg_path.read_text(encoding="utf-8")) or {}
    cohorts = list(reg.get("cohorts") or [])
    ids = [c.get("cohort_id") for c in cohorts]
    # ★ 46차 #9 — `dir` 을 **먼저** 위생 검사한다. 45차는 곧장
    #   `(REPO / c["dir"]).resolve()` 를 했는데, `pathlib` 의 `/` 는 오른쪽이
    #   절대 경로면 왼쪽을 **버린다**. `dir: /etc` 인 항목은 `/etc` 를 cohort
    #   디렉터리로 만들었고, 중복 검사도 조회도 저장소 밖 경로에 대고 돌았다.
    #   원장은 신뢰 입력이 아니라 파일이다 — 여기가 fail-closed 지점이다.
    dirs = [str(_ledger_dir(c, reg_path)) for c in cohorts]
    dup_id = sorted({i for i in ids if ids.count(i) > 1})
    dup_dir = sorted({d for d in dirs if dirs.count(d) > 1})
    if dup_id or dup_dir:
        raise SystemExit(
            f"✗ 보존 원장이 중복 선언을 담고 있다 ({reg_path}) — 중복 "
            f"cohort_id {dup_id} · 중복 디렉터리 {dup_dir}. 어느 항목이 정본인지 "
            "정할 수 없다 (조용히 앞의 것을 쓰면 authority 가 목록 순서에 달린다)")
    return cohorts


def _ledger_dir(cohort: dict, where) -> Path:
    """원장 항목의 `dir` 을 **정규 · 저장소-상대 · 격리**로 강제한다 (46차 #9).

    셋 다 필요하다:
      · 절대 경로 금지 — `REPO / "/etc"` 는 `/etc` 다 (탈출)
      · `..` 성분 금지 · `posixpath.normpath` 항등 — `a/../b`·`./a`·`a//b` 처럼
        같은 곳을 가리키는 **여러 표기**가 있으면 중복 검사가 무의미하다
        (같은 디렉터리를 두 표기로 두 번 선언할 수 있다)
      · resolve 후에도 `REPO` 안 — symlink 로 나가는 것을 막는다
    """
    raw = cohort.get("dir")
    cid = cohort.get("cohort_id")
    if type(raw) is not str or not raw:
        raise SystemExit(
            f"✗ 원장 cohort {cid!r} 의 `dir` 이 비어 있지 않은 문자열이 아니다: "
            f"{raw!r} ({where})")
    if posixpath.isabs(raw) or posixpath.normpath(raw) != raw \
            or ".." in raw.split("/"):
        raise SystemExit(
            f"✗ 원장 cohort {cid!r} 의 `dir` 이 정규 저장소-상대 경로가 아니다: "
            f"{raw!r} — 절대 경로·`..`·`.`·중복 slash 를 쓰지 않는다 (같은 곳을 "
            f"가리키는 표기가 여럿이면 중복 선언을 검사할 수 없다) ({where})")
    root = REPO.resolve()
    got = (REPO / raw).resolve()
    if got != root and root not in got.parents:
        raise SystemExit(
            f"✗ 원장 cohort {cid!r} 의 `dir` 이 저장소 밖을 가리킨다: {raw!r} → "
            f"{got} ({where})")
    return got


def _ledger_cohort_preflight(out: Path) -> dict:
    """**게시 authority 가 아닌** 사전 점검용 원장 조회 (47차 P1-b).

    쓰기(=lock 파일 생성) 전에 frozen·schema 위반을 걸러 내기 위한 것이다.
    여기서 읽은 값은 게시의 근거가 **아니다** — 근거는 임계 구역 안에서
    `_authority()` 가 다시 읽고, 그 사이의 변경은 게시 직전 seal 대조가
    잡는다. 이름을 따로 두는 이유는 "원장을 lock 안에서 읽는다"(41차 #9)는
    불변식이 이 사전 점검 때문에 흐려지지 않게 하기 위해서다.
    """
    global _IN_PREFLIGHT
    _IN_PREFLIGHT = True
    try:
        rec = _ledger_cohort(out)
        _ledger_seal(rec)          # schema·enum·정책 위생을 **쓰기 전에**
        return rec
    finally:
        _IN_PREFLIGHT = False


#: 사전 점검 중인가 — "원장은 lock 안에서 읽는다"(41차 #9) 불변식의 회귀가
#: 사전 점검 읽기를 authority 읽기와 구별할 수 있게 하는 표식이다.
_IN_PREFLIGHT = False


def _ledger_cohort(out: Path) -> dict:
    """이 cohort 디렉터리를 선언한 원장 항목 **전체** (43차 #9).

    선행 authority 다 — `CURRENT` 도 staging 도 아니다. 원장이 이 디렉터리를
    모르면 게시하지 않는다 (fail-closed).

    ★ 42차는 `set(legs)` 만 돌려줬고 게시 직전 재확인도 그것만 비교했다.
      그래서 **같은 legs 로 `active → frozen`** 이 되어도 옛 writer 가
      게시했다. cohort ID·디렉터리·status 도 authority 다.
    """
    want = Path(out).resolve()
    reg_path = REPO / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"
    hit = [c for c in _ledger_cohorts() if _ledger_dir(c, reg_path) == want]
    if hit:
        return hit[0]
    raise SystemExit(
        f"✗ 원장이 모르는 cohort 디렉터리다: {out} — 먼저 "
        "`LEG_PRESERVATION.yaml` 에 선언하라")


#: seal 이 다룰 수 있는 **정확한** 타입 (45차 #9 — `isinstance` 가 아니라
#: `type(...) is`). subclass·tuple·YAML `!!omap` 은 전부 밖이다.
_SEAL_SCALARS = (str, int, float, bool, type(None))


def _assert_sealable(node, where: str = "cohort") -> None:
    """canonicalizer 가 **접어 버릴 수 있는 값**을 입력 단계에서 거부한다.

    ★ 44차 #9 — 43차 seal 은 `json.dumps(..., default=str)` 이었다. 원장은
      `yaml.safe_load()` 로 읽으므로 PyYAML 이 타입을 붙인다::

          legs: ["2026-08-28"]   → str
          legs: [2026-08-28]     → datetime.date

      `default=str` 이 둘 다 `"2026-08-28"` 로 접었다. record 의 의미가
      바뀌었는데 seal 이 같아져, 게시 직전 재확인이 변경을 놓쳤다.
      **injective 하지 않은 canonicalizer 는 봉인이 아니다.**

      흡수하지 말고 거부한다 — 원장에 date-shaped scalar 를 쓰려면 따옴표로
      감싸 문자열로 적으면 된다 (그러면 seal 이 달라진다).
    """
    t = type(node)
    if t is float:
        # ★ 45차 #9 — NaN·Infinity 는 표준 JSON 밖이다. `json.dumps` 가
        #   `NaN`·`Infinity` 라는 비표준 token 을 뱉는다.
        if not math.isfinite(node):
            raise SystemExit(
                f"✗ 원장 {where} 에 유한하지 않은 수가 있다: {node!r} — "
                "표준 JSON 밖이라 봉인 domain 에 넣지 않는다")
        return
    if t in _SEAL_SCALARS:
        return
    if t is dict:
        for k, v in node.items():
            if type(k) is not str:
                raise SystemExit(
                    f"✗ 원장 {where} 의 key 타입이 봉인 가능하지 않다: "
                    f"{type(k).__name__} — 문자열로 적어라")
            _assert_sealable(v, f"{where}.{k}")
        return
    if t is list:
        for i, v in enumerate(node):
            _assert_sealable(v, f"{where}[{i}]")
        return
    # ★ 45차 #9 — `isinstance(..., (list, tuple))` 이 **tuple 을 허용**했다.
    #   PyYAML SafeLoader 는 표준 `!!omap` 을 list[tuple] 로 만들고,
    #   `json.dumps` 는 tuple 과 list 를 똑같은 JSON array 로 직렬화한다::
    #
    #       extra: !!omap        →  [("k", "v")]   ┐ 둘 다
    #       extra: [[k, v]]      →  [["k", "v"]]   ┘ {"extra":[["k","v"]]}
    #
    #   record 의 타입이 다른데 seal 이 같아진다. `type(...) is` 로 좁힌다 —
    #   subclass 도 마찬가지다 (canonicalizer 가 조용히 접는 통로다).
    raise SystemExit(
        f"✗ 원장 {where} 의 값 타입이 봉인 가능하지 않다: "
        f"{type(node).__name__} ({node!r}) — canonicalizer 가 다른 타입을 같은 "
        "bytes 로 접으면 서로 다른 record 가 같은 seal 이 된다 (tuple/`!!omap`· "
        "date·subclass). YAML 에서 표준 scalar·list·map 으로 적어라")


#: ★ 45차 #9 — **게시 authority 는 이 네 필드다** (닫힌 schema).
#:
#:   43·44차는 cohort record **전체**를 봉인했다. 그런데 이 저장소의 원장
#:   record 는 `pin`·`runtime` 같은 **기록용 bookkeeping** 을 함께 담고, 그것은
#:   라운드마다 바뀐다 — 전체를 봉인하면 pin 을 갱신하는 순간 이미 게시된
#:   pointer 가 전부 무효가 된다 (실측했다). "무엇이 authority 인가" 를 정하지
#:   않고 전부 봉인한 것이 과했다.
#:
#:   publication authority 는 **어느 cohort 가 · 어디에 · 어떤 상태로 · 어떤
#:   명부로** 게시되는가다. 그 밖(pin·runtime·산문)은 기록이며 authority 가
#:   아니다. 계약 §13.3.2 가 같은 것을 말한다.
#:
#:   ★ 46차 #9 — 그 좁히기가 **지나쳤다.** `pin` 은 bookkeeping 이 아니라 이
#:     cohort 의 바이트를 만든 **producer identity** 다. authority 에서 빼면
#:     `row_projection.py` 가 바뀌고 원장 pin 이 갱신돼도 옛 producer 가 만든
#:     `CURRENT` 가 그대로 유효하고, bootstrap 중간에 pin 을 갈면 한 cohort
#:     안에 서로 다른 producer 의 generation 이 섞인다 (`.PENDING` 은 옛 pin ·
#:     `CURRENT` 는 새 pin). `cross_leg_comparison` 은 소비자가 **지켜야 하는
#:     사용 정책**이므로 같은 이유로 authority 다.
#:
#:     `runtime` 과 산문 필드는 여전히 authority 밖이다 — 그것은 관측 기록이고,
#:     바뀌어도 이미 게시된 바이트의 의미를 바꾸지 않는다.
#: 원장 cohort record 가 **만족해야 하는** 필드 (타입·enum 검사 대상).
_LEDGER_AUTHORITY = ("cohort_id", "dir", "status", "legs",
                     "pin", "cross_leg_comparison")

#: ★ 48차 — `status` 는 **봉인에서 뺐다.**
#:
#:   47차는 `status` 를 봉인에 담았다. 그러면 `active → frozen` 이라는 **계약이
#:   정한 정상 전이**를 하는 순간 그 cohort 의 `CURRENT` 가 봉인과 어긋나
#:   영원히 재검증 불가가 된다. 48차에 g2 를 얼리며 실측했다:
#:   `check_materialized(proj_g2)` 가 `ea56c4ed11d4 ≠ fba9073e065d` 로 죽었다.
#:   보존 저장소에서 이것은 뒤집힌 결론이다 — **얼린 것일수록 검증 가능해야
#:   한다.**
#:
#:   봉인의 일은 게시된 바이트의 **뜻**이 흔들리지 않게 하는 것이다: 어느
#:   다리들인가(`legs`) · 무엇이 만들었는가(`pin`) · 어떤 비교가 허용되는가
#:   (`cross_leg_comparison`) · 어디인가(`cohort_id`·`dir`). lifecycle 상태는
#:   그 뜻의 일부가 아니다.
#:
#:   `frozen → active` 로 되돌려 얼린 cohort 에 쓰는 것은 이것으로 막지 않는다
#:   — `_assert_writable()` 과 `_ledger_cohort_preflight()` 가 **살아 있는
#:   원장**을 읽어 막는다. 그쪽이 맞는 자리다: 봉인은 과거의 사본이고 쓰기
#:   권한은 현재의 사실이다.
_LEDGER_UNSEALED = ("status",)

#: 실제로 **봉인되는** 부분집합. 검사 대상(`_LEDGER_AUTHORITY`)과 봉인 대상은
#: 다른 질문이다 — 48차에 그 둘을 한 tuple 로 섞어 두었다가 `status` 를 봉인에서
#: 빼면서 **검사까지 함께 사라졌다** (`..._ledger_status_is_an_exact_enum` 4건이
#: 잡았다). 검사는 "원장이 위생적인가", 봉인은 "게시된 바이트의 뜻이 고정인가".
_LEDGER_SEALED = tuple(k for k in _LEDGER_AUTHORITY if k not in _LEDGER_UNSEALED)

#: 원장이 인정하는 **정확한** cohort 상태 (46차 #9). 45차는 "비어 있지 않은
#: 문자열" 만 봤으므로 오타(`Active`)·새로 지어낸 값(`retired`)이 그대로
#: 봉인됐고, `status == "active"` 를 보는 소비자에게는 frozen 도 active 도 아닌
#: cohort 가 생겼다 (어느 검사도 안 걸린다).
_LEDGER_STATUS = ("active", "frozen")

#: cohort 간 비교 정책 — 소비자가 지켜야 하는 값이므로 자유 문자열이 아니다.
_CROSS_LEG_POLICY = ("allowed_within_cohort", "not_applicable_single_leg")


# ─────────────────────────────────────────────────────────────────────────────
# ★ 49차 P0 — **해동**(frozen → active)을 막는 단조 전이 journal
#
# 48차에 `status` 를 봉인에서 뺐다. freeze 가 이미 게시된 generation 을 무효로
# 만들면 안 되기 때문이고, 그 결정 자체는 옳다. 그런데 그러면 `status` 는 원장
# 파일의 한 줄일 뿐이고 `active → frozen → active` 로 되돌린 뒤 게시하면
# **얼렸다는 사실이 아무 데도 남지 않는다.** 얼린다는 것은 "이 cohort 는 더
# 이상 자라지 않는다" 는 선언인데, 조용히 되돌릴 수 있으면 선언이 아니다.
#
# 답은 봉인이 아니라 단조 journal 이다. append-only 이고 각 줄이 앞줄의 digest
# 를 담으므로 중간을 들어내면 사슬이 끊긴다. `frozen → active` 전이는 **표현할
# 수 없다** — 없는 상태를 막는 가장 싼 방법은 그 상태를 만들 수 없게 하는 것이다.
#
# frozen cohort 의 CURRENT 는 계속 읽힌다. 막아야 하는 것은 읽기가 아니라
# **새 게시**다.
# ─────────────────────────────────────────────────────────────────────────────

#: 전이 journal 한 줄의 **닫힌** key 집합.
#:
#: ★ 51차 P0-F — `dir` 이 추가됐다. 50차까지 lifecycle 의 key 는 mutable 한 raw
#: cohort ID 하나였다. 그래서 원장 **한 파일만** 고쳐 같은 `dir` row 의
#: `cohort_id` 를 바꾸면 (journal 도 anchor 도 손대지 않고) frozen 목적지에
#: public publisher 가 그대로 게시했다 (리뷰어 실측). 얼린 것은 **이름이 아니라
#: 그 디렉터리**다 — 봉인이 이름만 잡으면 이름을 바꿔서 빠져나간다.
_LIFECYCLE_KEYS = ("seq", "at", "cohort_id", "dir", "from", "to", "note", "prev")

#: 허용 전이. 여기 없는 순서쌍은 만들 수 없다.
_LIFECYCLE_MOVES = ((None, "active"), (None, "frozen"), ("active", "frozen"))


def _lifecycle_path() -> Path:
    """전이 journal 의 자리 — 원장 **옆**이다 (cohort 디렉터리 안이 아니다).

    cohort 디렉터리 안에 두면 generation 완전성 검사의 열거 대상이 되어,
    lifecycle 기록이 게시 내용의 일부인 것처럼 섞인다. 두 질문은 다르다.
    """
    return Path(REPO) / "docs" / "22p_gap" / "COHORT_LIFECYCLE.jsonl"


def _lifecycle_head_path() -> Path:
    """사슬의 **끝**을 고정하는 anchor.

    해시 사슬은 중간을 지키지만 **마지막 줄은 지키지 못한다** — 뒤따르는 줄이
    없어 그 digest 를 담을 곳이 없기 때문이다. 끝 digest 를 따로 두면 tip 을
    위조하려는 사람은 두 파일을 **일관되게** 고쳐야 한다.

    한계는 분명히 적는다: 두 파일 모두에 쓸 수 있는 주체는 역사를 다시 쓸 수
    있다. 여기서 막는 것은 "조용한" 되돌림이고, 그 밖은 tracked 파일의 diff 를
    사람이 보는 것이 바깥 통제다 (`flock` 이 같은 기계만 가정하는 것과 같은
    종류의 경계다).
    """
    return _lifecycle_path().with_suffix(".head")


def _lifecycle_line(rec: dict) -> str:
    return json.dumps(rec, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"))


def read_lifecycle() -> list:
    """journal 을 읽고 **사슬을 검증한다** (49차 P0).

    append-only 를 파일 권한으로만 주장하면 그것은 주장이지 증거가 아니다.
    `seq` 가 0부터 빈틈없이 이어지고, 각 줄의 `prev` 가 앞줄 바이트의 digest 와
    같아야 한다. 중간을 고치거나 들어내면 여기서 보인다.
    """
    p = _lifecycle_path()
    if not p.is_file():
        # ★ 50차 P0 — **anchor 가 있으면 journal 도 있어야 한다.** 49차는 여기서
        #   끝 대조 전에 빠져나갔고, 그래서 파일 하나를 지우는 것만으로 frozen
        #   기록이 사라져 public 재게시가 통과했다 (리뷰어 실측). anchor 를 둔
        #   이유가 "사슬의 끝을 고정한다" 인데 사슬 자체가 없을 때를 안 봤다.
        if _lifecycle_head_path().is_file():
            raise SystemExit(
                f"✗ cohort lifecycle journal 이 없는데 끝 anchor 는 남아 있다 "
                f"({_lifecycle_head_path()}) — 사슬이 지워졌다. 없는 것과 "
                "지워진 것은 다르다")
        return []
    out, prev = [], ""
    for i, raw in enumerate(p.read_text(encoding="utf-8").splitlines()):
        if not raw.strip():
            continue
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(
                f"✗ cohort lifecycle journal {i}번째 줄이 JSON 이 아니다: {exc}")
        if type(rec) is not dict or set(rec) != set(_LIFECYCLE_KEYS):
            raise SystemExit(
                f"✗ cohort lifecycle journal {i}번째 줄의 schema 가 계약과 "
                f"다르다: {sorted(rec) if type(rec) is dict else type(rec).__name__}")
        if rec["seq"] != i:
            raise SystemExit(
                f"✗ cohort lifecycle journal 의 사슬이 끊겼다 — {i}번째 줄의 "
                f"seq 가 {rec['seq']!r} 이다 (줄이 지워졌거나 순서가 바뀌었다)")
        if rec["prev"] != prev:
            raise SystemExit(
                f"✗ cohort lifecycle journal 의 사슬이 끊겼다 — {i}번째 줄의 "
                "prev 가 앞줄의 digest 와 다르다 (앞줄이 고쳐졌다)")
        prev = hashlib.sha256(
            _lifecycle_line(rec).encode("utf-8")).hexdigest()
        out.append(rec)
    hp = _lifecycle_head_path()
    head = hp.read_text(encoding="utf-8").strip() if hp.is_file() else ""
    if head != prev:
        raise SystemExit(
            f"✗ cohort lifecycle journal 의 사슬이 끊겼다 — 끝 digest 가 anchor "
            f"와 다르다 ({prev[:16] or '없음'} ≠ {head[:16] or '없음'}). "
            "마지막 줄이 고쳐졌거나 anchor 가 낡았다")
    return out


def cohort_lifecycle_state(cohort_id: str, entries=None):
    """이 cohort 의 **마지막으로 기록된** 상태 (기록이 없으면 `None`)."""
    last = None
    for rec in (read_lifecycle() if entries is None else entries):
        if rec["cohort_id"] == cohort_id:
            last = rec["to"]
    return last


def _cohort_dir_key(cohort_id: str) -> str:
    """원장이 이 cohort 에 준 목적지를 **저장소 상대 canonical 경로**로.

    journal 이 봉인할 대상 identity 다 (51차 P0-F).
    """
    for c in _ledger_cohorts():
        if c.get("cohort_id") == cohort_id:
            d = (REPO / str(c.get("dir") or "")).resolve()
            try:
                return d.relative_to(Path(REPO).resolve()).as_posix()
            except ValueError:
                return d.as_posix()
    raise SystemExit(f"✗ 원장에 cohort {cohort_id!r} 이 없다")


def frozen_dirs_from_journal(entries=None) -> dict[str, str]:
    """journal 이 frozen 이라고 **기록한** 목적지 → 그때의 cohort ID (51차 P0-F).

    원장의 현재 ID 와 무관하다. 원장은 사람이 고칠 수 있는 한 줄이고 journal 은
    되돌릴 수 없다 — 그래서 "이 디렉터리가 얼린 적이 있는가" 의 정본은 여기다.
    """
    out = {}
    for rec in (read_lifecycle() if entries is None else entries):
        d = rec.get("dir")
        if not d:
            continue
        if rec["to"] == "frozen":
            out[str(d)] = rec["cohort_id"]
        else:
            out.pop(str(d), None)
    return out


def _append_lifecycle(cohort_id: str, frm, to: str, note: str) -> dict:
    """전이 하나를 **덧붙인다.** 허용 전이가 아니면 만들지 않는다."""
    entries = read_lifecycle()
    live = cohort_lifecycle_state(cohort_id, entries)
    if live != frm:
        raise SystemExit(
            f"✗ cohort {cohort_id!r} 의 기록된 상태는 {live!r} 인데 {frm!r} 에서 "
            "옮기려 한다 — 전이는 기록된 상태에서만 출발한다")
    if (frm, to) not in _LIFECYCLE_MOVES:
        raise SystemExit(
            f"✗ 허용되지 않는 cohort 전이다: {frm!r} → {to!r} — 얼린 cohort 는 "
            "되돌릴 수 없다 (그것이 freeze 의 뜻이다). 다시 쓰려면 **새 "
            "cohort** 를 만들어라")
    prev = ""
    if entries:
        prev = hashlib.sha256(
            _lifecycle_line(entries[-1]).encode("utf-8")).hexdigest()
    rec = {"seq": len(entries), "cohort_id": cohort_id,
           "dir": _cohort_dir_key(cohort_id), "from": frm, "to": to,
           "note": str(note),
           "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "prev": prev}
    p = _lifecycle_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(_lifecycle_line(r) + "\n" for r in entries + [rec])
    tmp = p.with_name(f".{p.name}.{uuid.uuid4().hex}.tmp")
    tmp.write_text(body, encoding="utf-8")
    fd = os.open(tmp, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, p)
    # 사슬의 끝을 anchor 에 고정한다 — journal **다음**에 쓴다. 그 사이에
    # 죽으면 anchor 가 낡아 `read_lifecycle()` 이 fail-closed 로 멈춘다
    # (조용히 통과하는 것보다 낫다).
    hp = _lifecycle_head_path()
    tip = hashlib.sha256(_lifecycle_line(rec).encode("utf-8")).hexdigest()
    htmp = hp.with_name(f".{hp.name}.{uuid.uuid4().hex}.tmp")
    htmp.write_text(tip + "\n", encoding="utf-8")
    hfd = os.open(htmp, os.O_RDONLY)
    try:
        os.fsync(hfd)
    finally:
        os.close(hfd)
    os.replace(htmp, hp)
    dfd = os.open(p.parent, os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return rec


def assert_not_thawed(cohort_id: str) -> None:
    """얼린 적이 있는 cohort 인가 — **첫 write 전에** 묻는다 (49차 P0).

    원장의 `status` 는 사람이 고칠 수 있는 한 줄이다. journal 은 되돌릴 수 없다.
    """
    if cohort_lifecycle_state(cohort_id) == "frozen":
        raise SystemExit(
            f"✗ cohort {cohort_id!r} 는 이미 frozen 으로 기록됐다 "
            f"({_lifecycle_path()}) — 원장의 status 를 active 로 되돌려도 게시할 "
            "수 없다. 얼린 cohort 는 자라지 않는다. 새 cohort 를 만들어라")
    # ★ 51차 P0-F — 이름이 아니라 **목적지**로도 묻는다. 원장의 cohort_id 만
    #   바꾸면 이 cohort 에는 frozen 기록이 없지만, 그 디렉터리에는 있다.
    frozen = frozen_dirs_from_journal()
    here = _cohort_dir_key(cohort_id)
    if here in frozen:
        raise SystemExit(
            f"✗ cohort {cohort_id!r} 의 목적지 {here} 는 {frozen[here]!r} 로 "
            f"이미 frozen 기록이 있다 ({_lifecycle_path()}) — 원장에서 ID 를 "
            "바꿔도 그 디렉터리는 얼려 있다. 새 세대는 **새 디렉터리**를 쓴다")


def freeze_cohort(cohort_id: str, reason: str) -> dict:
    """cohort 를 얼린다 — 원장과 전이 journal **양쪽**에 (49차 P0).

    원장만 고치면 그 사실이 되돌릴 수 있는 한 줄로만 남는다.
    """
    import yaml

    led = Path(REPO) / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"
    doc = yaml.safe_load(led.read_text(encoding="utf-8")) or {}
    row = next((c for c in doc.get("cohorts") or []
                if c.get("cohort_id") == cohort_id), None)
    if row is None:
        raise SystemExit(f"✗ 원장에 cohort {cohort_id!r} 이 없다")
    recorded = cohort_lifecycle_state(cohort_id)
    # ★ 51차 P1-O — **crash 복구가 먼저다.** journal·anchor 를 먼저 쓰고 원장을
    #   나중에 쓰므로, 그 사이에 죽으면 journal 은 frozen 인데 원장은 active 다.
    #   게시는 안전하게 막히지만(fail-closed) 같은 API 로 다시 부르면
    #   `frozen → frozen` 이라 거부됐다 — 원장은 영영 active 로 남는다 (리뷰어
    #   실측). fail-closed 는 정지가 아니다. 남은 전이를 **완주**한다.
    if recorded == "frozen":
        if row.get("status") == "active":
            prev = next((r for r in read_lifecycle()
                         if r["cohort_id"] == cohort_id and r["to"] == "frozen"),
                        None)
            _write_ledger_doc(led, doc, row, prev["note"] if prev else reason)
            return prev
        raise SystemExit(
            f"✗ cohort {cohort_id!r} 는 이미 frozen 으로 기록됐다 — 두 번 "
            "얼릴 수 없다")
    if row.get("status") != "active":
        raise SystemExit(
            f"✗ cohort {cohort_id!r} 의 상태가 {row.get('status')!r} 이라 "
            "얼릴 수 없다")
    # 출발점은 **기록된** 상태다. journal 이 생기기 전부터 active 이던 cohort 는
    # 기록이 없고(`None`), 그 경우도 얼릴 수 있어야 한다 — 게시는 lifecycle 을
    # 움직이지 않으므로 "active 기록" 은 없는 것이 정상이다.
    rec = _append_lifecycle(cohort_id, recorded, "frozen", reason)
    _write_ledger_doc(led, doc, row, reason)
    return rec


def _write_ledger_doc(led: Path, doc: dict, row: dict, reason: str) -> None:
    """freeze 의 **두 번째** 쓰기 — 원장 전이. 재시도해도 같은 결과다."""
    import yaml

    row["status"] = "frozen"
    row["frozen_reason"] = str(reason)
    led.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False),
                   encoding="utf-8")

#: producer identity 의 **닫힌** 필드 집합. 하나라도 빠지거나 남으면 거부한다.
_PIN_AUTHORITY = ("schema_version", "compute_sha256", "row_projection_py_sha256",
                  "src_scoring_py_sha256", "analysis_spec_sha256",
                  "producer_semantic_sha256")

#: 그 중 **cohort 수명 동안 불변**인 부분 — 봉인에 들어가는 것은 이것뿐이다.
#:
#:   `schema_version` 은 산출 schema 이고 `analysis_spec_sha256` 은 비교 규칙
#:   이다. 둘은 이 cohort 의 바이트가 **무엇을 뜻하는가** 를 정하므로, 바뀌면
#:   같은 cohort 안에 뜻이 다른 generation 이 섞인다 → 새 cohort ID 로 가야
#:   한다.
#:
#:   나머지 셋(`compute_sha256`·두 파일 digest)은 **provenance 기록**이다.
#:   주석 한 줄만 고쳐도 움직이므로 봉인에 넣으면 라운드마다 cohort 를 새로
#:   만들어야 한다 — 그것은 불변식이 아니라 잡음이다. 대신 그쪽 축은
#:   `test_projection_analyzer_digests_recompute_from_the_current_tree` 가
#:   **active cohort 의 manifest 는 현행 트리와 같아야 한다** 로 강제한다
#:   (producer 가 바뀌면 cohort 를 통째로 재생성해야 통과한다). 두 규칙이
#:   합쳐져야 "이 바이트를 누가 만들었는가" 가 닫힌다 — 계약 §13.3.2.
_PIN_SEALED = ("schema_version", "analysis_spec_sha256",
               "producer_semantic_sha256")


def _ledger_authority(cohort: dict) -> dict:
    """원장 record 를 **검사하고** 그 중 봉인 대상만 닫힌 타입으로 뽑는다.

    ★ 48차 — 검사 대상(`_LEDGER_AUTHORITY`)과 봉인 대상(`_LEDGER_SEALED`)은
      **다른 질문**이다. 한 tuple 로 섞어 두었다가 `status` 를 봉인에서 빼면서
      그 필드의 enum 검사까지 함께 사라졌다 — `..._ledger_status_is_an_exact_enum`
      4건이 그것을 잡았다. 검사는 "원장이 위생적인가"이고 봉인은 "게시된
      바이트의 뜻이 고정인가"이다. 이제 loop 는 `_LEDGER_AUTHORITY` 전체를
      검사하고, `rec` 에는 `_LEDGER_SEALED` 만 담는다.
    """
    # 전체 record 가 canonical domain 안인지 먼저 본다 — authority 밖 필드라도
    # canonicalizer 가 접을 수 있는 타입(tuple·date·NaN)은 원장 위생 문제다.
    _assert_sealable(cohort)
    rec = {}
    for k in _LEDGER_AUTHORITY:
        v = cohort.get(k)
        if k == "legs":
            if type(v) is not list or any(type(x) is not str for x in v):
                raise SystemExit(
                    f"✗ 원장 cohort 의 `legs` 가 문자열 목록이 아니다: {v!r}")
            # ★ 49차 P1 — 명부는 **집합**이다 (multiset 이 아니다). 이 값을
            #   쓰는 쪽은 모두 `frozenset` 이거나 집합 대조인데, 48차는
            #   `sorted(v)` 를 그대로 봉인했다. 중복이 있으면 봉인은 2개를
            #   말하고 runtime 은 1개를 보므로 "seal 이 roster 를 덮는다" 가
            #   깨지고, `not_applicable_single_leg` 의 길이 검사도 뜻이 뒤집힌다.
            dup = sorted({x for x in v if v.count(x) > 1})
            if dup:
                raise SystemExit(
                    f"✗ 원장 cohort 의 `legs` 에 중복이 있다: {dup} — 명부는 "
                    "집합이고, 중복이 있으면 봉인이 세는 수와 runtime 이 보는 "
                    "수가 달라진다")
            rec[k] = sorted(v)
        elif k == "pin":
            # ★ 46차 #9 — producer identity 는 **닫힌 schema** 다. key 가 빠지면
            #   `.get()` 이 `None` 을 돌려주고, 그 `None` 이 "선언하지 않았다" 와
            #   구별되지 않는다 (pointer schema 에서 이미 겪은 형태다).
            if type(v) is not dict or set(v) != set(_PIN_AUTHORITY):
                raise SystemExit(
                    f"✗ 원장 cohort 의 `pin` 이 계약 필드 집합이 아니다: "
                    f"{sorted(v) if type(v) is dict else v!r} — "
                    f"{sorted(_PIN_AUTHORITY)} 를 정확히 담아야 한다")
            if type(v["schema_version"]) is not int:
                raise SystemExit(
                    f"✗ 원장 cohort 의 `pin.schema_version` 이 정수가 아니다: "
                    f"{v['schema_version']!r}")
            for pk in _PIN_AUTHORITY[1:]:
                if type(v[pk]) is not str or not v[pk]:
                    raise SystemExit(
                        f"✗ 원장 cohort 의 `pin.{pk}` 가 비어 있지 않은 "
                        f"문자열이 아니다: {v[pk]!r}")
            rec[k] = {pk: v[pk] for pk in _PIN_SEALED}
        elif type(v) is not str or not v:
            raise SystemExit(
                f"✗ 원장 cohort 의 `{k}` 가 비어 있지 않은 문자열이 아니다: {v!r}")
        elif k == "status" and v not in _LEDGER_STATUS:
            raise SystemExit(
                f"✗ 원장 cohort 의 `status` 가 계약 enum 이 아니다: {v!r} — "
                f"{list(_LEDGER_STATUS)} 중 하나여야 한다 (자유 문자열이면 "
                "frozen 도 active 도 아닌 cohort 가 조용히 생긴다)")
        elif k == "cross_leg_comparison" and v not in _CROSS_LEG_POLICY:
            raise SystemExit(
                f"✗ 원장 cohort 의 `cross_leg_comparison` 이 계약 enum 이 "
                f"아니다: {v!r} — {list(_CROSS_LEG_POLICY)} 중 하나여야 한다")
        elif k == "cross_leg_comparison" and v == "not_applicable_single_leg" \
                and len(rec.get("legs") or ()) != 1:
            # ★ 47차 P1-c — 정책 **문자열**만 봉인하고 의미를 안 보면,
            #   multi-leg cohort 가 "단일 leg 라 해당 없음" 을 달고 통과한다.
            raise SystemExit(
                f"✗ `not_applicable_single_leg` 은 단일 leg cohort 의 값이다 — "
                f"명부가 {len(rec.get('legs') or ())} 개다 "
                f"({sorted(rec.get('legs') or ())}). multi-leg 라면 "
                f"`allowed_within_cohort` 를 쓰라")
        elif k in _LEDGER_SEALED:
            rec[k] = v
    return rec


def _ledger_seal(cohort: dict) -> str:
    """게시 authority 네 필드의 정규 digest — pointer 가 봉인하는 값 (43~45차 #9).

    ★ 44차 — `default=str` 을 없앴다. 접을 수 없는 값은 `_assert_sealable()`
      이 **거부**한다. canonicalizer 가 흡수하면 서로 다른 record 가 같은
      seal 로 접힌다 (43차 반례).

    ★ 45차 — 봉인 범위를 **authority 네 필드**로 좁혔다 (위 `_LEDGER_AUTHORITY`).
    """
    return hashlib.sha256(json.dumps(
        _ledger_authority(cohort), sort_keys=True, ensure_ascii=False,
        allow_nan=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def _ledger_roster(out: Path) -> set:
    """`_ledger_cohort()` 의 `legs` — 얇은 사본이다 (authority 는 record)."""
    return set(_ledger_cohort(out).get("legs") or ())


def _frozen_cohort_dirs() -> dict[str, Path]:
    """`LEG_PRESERVATION.yaml` 이 frozen 이라고 선언한 cohort 디렉터리.

    ★ 26차 P1-9 — `--out` 을 생략하면 기본값이 `warm_probe`(= frozen g1)라
      원자료를 잃은 여덟 투영을 실수로 덮을 수 있었다. 목적지는 cohort 로
      고르고, frozen 이면 여기서 막는다.
    """
    out = {c["cohort_id"]: (REPO / c["dir"]).resolve()
           for c in _ledger_cohorts() if c.get("status") == "frozen"}
    # ★ 51차 P0-F — journal 이 기록한 목적지도 **합집합**이다. 원장의 현재 ID 와
    #   status 는 한 파일 수정으로 바뀐다. 얼린 적이 있는 디렉터리는 그 뒤 어떤
    #   이름을 붙여도 얼린 디렉터리다.
    for d, cid in frozen_dirs_from_journal().items():
        out.setdefault(cid, (REPO / d).resolve())
    return out


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
    for c in _ledger_cohorts():
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
