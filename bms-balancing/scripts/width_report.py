#!/usr/bin/env python3
"""폭을 읽는다 — `cycles_*.csv` 하나면 표로, 둘이면 **한 축만 다른 두 실행**을 견준다.

    python3 scripts/width_report.py <cycles.csv>                     # 표
    python3 scripts/width_report.py <A.csv> <B.csv> --axis w_dqdv    # 비교 (축 하나만 달라야 한다)

왜 스크립트인가 (`compare_states.py` 와 같은 이유): 이 비교를 손으로 하면 그 숫자가 **문서에만 있는 주장**이
된다. 그리고 두 실행의 설정이 축 하나 말고 또 다르면 그 비교는 아무것도 뜻하지 않는데, 눈으로는 안 보인다 —
sidecar 를 읽어 **기계가 막는다**.

종료 코드: 0 정상 · 2 입력 문제 (파일 없음 · 폭이 안 실림 · 축 말고 다른 설정이 다름).

⚠ 폭은 **하한**이다 (`width_is_lower_bound`). 국소 해법 + 격자로 미는 값이라 참 폭보다 좁을 수 있다.
⚠ 이 폭은 **모델 고정 축**이다 — 문헌 곡선 선택이 만드는 폭(`matrix_*`)은 여기 안 들어간다. 두 축을 합치지 않는다.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from bms_balancing import schema as S          # noqa: E402
# ⚠ R17 후속 2차 F2-03: 상자 규칙은 **적합이 쓰는 그 함수**(`resolve_box`)가 정본이다 — 읽는 쪽이
#   따로 적으면 규칙이 두 벌이 된다 (R14 P2-2 에서 겪은 일).
from bms_balancing import verify as V          # noqa: E402

MODES = ("LAM_PE", "LAM_NE", "LLI")

#: ⚠ Codex R17 P1-04: 전 판의 rc 0 은 "열거한 설정 스무 개가 같다" 만 뜻했다 — 입력 SHA 가 바뀌어도, cycle 하나가
#:   빠져도(교집합으로 비교), 같은 cycle 이 두 번 있어도(dict 가 마지막 행을 고름), 끝점이 NaN 이어도 rc 0 이었고,
#:   키가 양쪽에 **없으면** `None == None` 으로 통과했다. 그래서 `BML_R1_RESPONSE` §14-1 의 "rc 0 이 그 자체로
#:   증거다" 는 성립하지 않았다. 이제 reader 가 **일반 검증 경로**(`schema.check_rows`: 스키마·유한·receipt·
#:   union·중복 key)를 먼저 타고, 본문↔sidecar↔입력을 SHA 로 묶고, 두 실행의 **코드·환경·입력·모집단**이 같음을
#:   요구한다. 부분 비교는 하지 않는다 — 필요하면 그것은 다른 이름의 다른 도구다.
#: 두 실행이 **같아야** 하는 결속 — 이것이 다르면 "축 하나만 다르다" 가 거짓이다.
BOUND_IDENTITY = ("git_commit", "env", "consumed_inputs", "dataset_manifest")
#: sidecar 에 **있어야** 하는 키 — 없는 키는 `None` 으로 견주지 않는다 (부재는 안전값이 아니다).
REQUIRED_META = ("sha256", "run_id", "cycles") + BOUND_IDENTITY

#: 두 실행이 **같아야** 하는 설정 — 여기가 다르면 그 비교는 축 하나의 것이 아니다.
#: (`--axis` 로 지정한 것 하나만 예외다. `run_states.sh` 의 "같은 설정이어야 비교가 성립한다" 와 같은 규율.)
COMPARED_SETTINGS = ("lb", "ub", "initial", "gamma_prefit", "gamma_lb", "n_multistart", "seed",
                     "scale_seed", "w_pocv", "w_dvdq", "w_dqdv", "optimizer",
                     # ⚠ W-21: `width_method` 는 켬/끔만 가른다 — **격자 수가 다른 두 켠 실행**은 이름이 같아서
                     #   그대로 견줘졌다. 폭 차이의 일부가 격자 탓인데 눈에 안 보인다.
                     "widths", "width_tol", "width_starts", "width_method", "width_grid",
                     "cell", "si_source", "starts", "cycles",
                     # ⑥ chain rule 계약: 어느 미분으로 적합했나. 축으로 고르면(`--axis objective_version`) 두 판을 견주고,
                     #   아니면 같아야 한다 — 두 판을 한 판인 것처럼 섞지 않는다 (Codex R17 §4).
                     "objective_version")

#: ⚠ Codex R17 후속 P1-02: **행이 선언한 실행 조건**과 sidecar 의 선언이 같은 것을 말해야 한다.
#:   전 판은 행 enum 이 "각각 유효한 값인가" 만 보고, 비교 조건은 sidecar 에서만 읽었다 — 그래서
#:   행만 `chain_rule_v2` 로 바꾸거나(한 파일 안에서 섞어도) `width_tol`·`cell` 을 어긋나게 해도
#:   rc 0 이었다 (본문 sha256 과 입력 receipt 는 정확한 채로). 왼쪽이 행의 열, 오른쪽이 sidecar 키다.
#: ⚠ R17 후속 3차 F3-02: **같은 실행 축의 두 이름**. `fit_cycles.py` 는 `--starts` 하나를 받아
#:   sidecar 에 `starts` 와 `n_multistart` 로 **두 번** 적는다. 단일 파일 안에서 둘의 일치를
#:   요구한 것(F2-02)은 옳지만, 비교에서 **독립 축 둘로 세면** 정상 변경이 표현 불가능해진다 —
#:   `--axis starts` 면 `n_multistart` 가, `--axis n_multistart` 면 `starts` 가 남아 **둘 다 rc 2**
#:   였다 (리뷰어가 실제 producer 산출 두 벌로 실측). 축을 고르면 그 **무리 전체**를 뺀다.
SETTING_ALIASES = (("starts", "n_multistart"),)


def alias_group(key: str) -> tuple:
    """`key` 와 같은 의미 축의 이름들 — 무리에 없으면 자기 자신 하나."""
    for group in SETTING_ALIASES:
        if key in group:
            return group
    return (key,)


#: ⚠ R17 후속 2차 F2-02: 행에만 남아 있던 실행 조건 둘이 **결속 목록에 없었다** — 한쪽 파일의 행만
#:   `scale_seed=99`/`n_starts=999` 로 바꾸고 본문 sha256 을 정확히 갱신하면 rc 0 · "동일 확인" 이었다.
#:   둘 다 생산자가 행에 적는 값이고(`cycles.py` 의 `scale_seed`·`n_starts` 열), sidecar 의 짝은
#:   `scale_seed`·`n_multistart` 다. `si_source` 는 **현재 `CYCLES_ROW` 에 없으므로** 넣지 않는다
#:   (없는 열을 결속 목록에 적으면 `row_key not in rows[0]` 로 조용히 건너뛰는 항목이 하나 늘 뿐이다).
BODY_META_BOUND = (("objective_version", "objective_version"),
                   ("cell", "cell"),
                   ("width_tol", "width_tol"),
                   ("run_id", "run_id"),
                   ("scale_seed", "scale_seed"),
                   ("n_starts", "n_multistart"))

#: ⚠ R17 후속 P1-03: 필수 키를 넣고 **`null` 로 채우면** 동일성 검사가 다시 열린다 (absent==absent 가
#:   null==null 로 옮겨 간 것). 그래서 값의 **타입까지** 본다. `gamma_lb` 처럼 합법적으로 nullable 한
#:   항목은 여기 넣지 않는다 — "null 이면 전부 거부" 로 넓히면 정상 산출이 막힌다.
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _is_int_like(v) -> bool:
    """`"3"`·`3`·`3.0` 은 정수, `"0.9"`·`""`·`"x"` 는 아니다 (본문 cycle 은 CSV 문자열이다)."""
    try:
        return float(v).is_integer()
    except (TypeError, ValueError):
        return False


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v))


def _int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _typed_meta_problems(meta: dict, name: str) -> list:
    """sidecar 의 **필수 값**이 타입·형식·**의미**까지 맞는가. 문제 목록을 돌려준다.

    ⚠ R17 후속 P1-03 에서 "키 존재 ≠ 완전성" 을 닫았고, ⚠ **R17 후속 2차 F2-03** 에서 그것이
      한 단계 더 안으로 옮겨 간 것을 닫는다: `env` 여섯 축이 전부 `null`/공백이어도, `dataset_manifest`
      가 `"   "` 여도, `lb=ub=initial=[0]` 이나 `lb=[NaN]*5` 여도, `width_starts=null` 이어도 rc 0
      이었다 (리뷰어 실측 7 case). **비어 있지 않은 객체는 유효한 환경이 아니고 수 목록은 상자가 아니다.**

      그래서 규칙을 이 파일에 새로 적지 않고 **발행 쪽 정본을 부른다**:
        env              → `schema.env_axes_missing()` (존재·비공백 규칙의 정본, R14 P2-2)
        상자 lb/ub       → `verify.resolve_box()` (5차원·유한·순서의 정본, W-01~W-05)
        dataset_manifest → `data.half_cell_manifest_identity()` 가 내는 {version, dataset_id, sha256}
      한 규칙을 두 벌로 적으면 절반만 구현된다 — 이 저장소에서 두 번 겪은 일이다.

    **합법 nullable 은 건드리지 않는다** (`gamma_lb`·`gamma_init`·`literature`). "null 이면 전부
    거부" 로 넓히면 정상 산출이 막힌다 — 리뷰어가 같이 요구한 조건이다.
    """
    p = []

    def _need(key, ok, what):
        if key in meta and not ok(meta.get(key)):
            p.append(f"{name}: `{key}` 가 {what} 가 아니다 ({meta.get(key)!r})")

    _need("sha256", lambda v: isinstance(v, str) and _HEX64.fullmatch(v), "64자리 hex")
    _need("git_commit", lambda v: isinstance(v, str) and _HEX40.fullmatch(v), "40자리 hex commit")
    _need("run_id", lambda v: isinstance(v, str) and v.strip(), "비지 않은 문자열")
    _need("consumed_inputs", lambda v: isinstance(v, dict) and bool(v), "비지 않은 객체")
    _need("cycles", lambda v: isinstance(v, list) and bool(v) and all(_int(c) for c in v), "정수 목록")
    for k in ("seed", "scale_seed", "n_multistart", "starts"):
        _need(k, _int, "정수")
    _need("objective_version", lambda v: v in S.OBJECTIVE_VERSIONS,
          f"{list(S.OBJECTIVE_VERSIONS)} 중 하나")
    for k in ("cell", "si_source", "optimizer", "width_method"):
        _need(k, lambda v: isinstance(v, str) and v.strip(), "비지 않은 문자열")
    for k in ("w_pocv", "w_dvdq", "w_dqdv"):
        _need(k, _num, "유한한 수")
    _need("gamma_prefit", lambda v: isinstance(v, bool), "bool")
    _need("width_tol", lambda v: _num(v) and float(v) >= 0.0, "0 이상의 유한한 수")

    # ── env — 여섯 축의 **존재·비공백**은 `schema.env_axes_missing` 하나가 정한다 (F2-03) ──
    if "env" in meta:
        env = meta.get("env")
        if not isinstance(env, dict) or not env:
            p.append(f"{name}: `env` 가 비지 않은 객체가 아니다 ({env!r})")
        else:
            gone = S.env_axes_missing(env)
            if gone:
                aged = S.env_axes_added_only(gone) and all(k not in env for k in gone)
                why = ("나중에 더해진 축이 키째 없다 (옛 sidecar) — 이 도구는 나이도 비교 근거로 쓰지 않는다"
                       if aged else "값이 null·공백이면 환경을 기록하지 않은 것이다")
                p.append(f"{name}: `env` 의 축 {gone} 이 없거나 비었다 ({why}) — "
                         f"두 파일의 잘못된 값이 같다는 사실은 '같은 환경' 이 아니다")

    # ── dataset_manifest — 실제 발행자(`half_cell_manifest_identity`)의 계약 (F2-03) ──
    if "dataset_manifest" in meta:
        dm = meta.get("dataset_manifest")
        if not isinstance(dm, dict):
            p.append(f"{name}: `dataset_manifest` 가 {{version, dataset_id, sha256}} 객체가 아니다 "
                     f"({dm!r}) — 아무 비공백 문자열은 모집단 선언이 아니다")
        else:
            # `version` 은 발행자가 `manifest_version`(정수)을 그대로 싣는다 — 문자열로 굳히지 않는다
            if not (_int(dm.get("version")) or (isinstance(dm.get("version"), str) and dm["version"].strip())):
                p.append(f"{name}: `dataset_manifest.version` 이 정수도 비지 않은 문자열도 아니다 "
                         f"({dm.get('version')!r})")
            if not (isinstance(dm.get("dataset_id"), str) and dm["dataset_id"].strip()):
                p.append(f"{name}: `dataset_manifest.dataset_id` 가 비지 않은 문자열이 아니다 "
                         f"({dm.get('dataset_id')!r})")
            if not (isinstance(dm.get("sha256"), str) and _HEX64.fullmatch(dm.get("sha256") or "")):
                p.append(f"{name}: `dataset_manifest.sha256` 가 64자리 hex 가 아니다 ({dm.get('sha256')!r})")

    # ── 상자 — 5차원·유한·순서는 `verify.resolve_box` 하나가 정하고, initial 은 그 안이어야 한다 (F2-03) ──
    if all(k in meta for k in ("lb", "ub")):
        lb, ub = meta.get("lb"), meta.get("ub")
        if not (isinstance(lb, list) and isinstance(ub, list)):
            p.append(f"{name}: `lb`/`ub` 가 목록이 아니다 ({lb!r} · {ub!r})")
        else:
            try:
                lo, hi = V.resolve_box(lb, ub)
            except (ValueError, TypeError) as e:
                p.append(f"{name}: `lb`/`ub` 가 유효한 상자가 아니다 ({e}) — "
                         f"`resolve_box` 가 적합에 쓰는 그 규칙이다")
            else:
                init = meta.get("initial")
                if not (isinstance(init, list) and len(init) == 5 and all(_num(x) for x in init)):
                    p.append(f"{name}: `initial` 이 5개의 유한한 수가 아니다 ({init!r})")
                elif any(not (lo[i] - 1e-12 <= float(init[i]) <= hi[i] + 1e-12) for i in range(5)):
                    p.append(f"{name}: `initial` 이 그 상자 밖이다 (initial {init} · lb {lo.tolist()} · "
                             f"ub {hi.tolist()}) — 적합이 쓸 수 없는 시작점이다")

    # ── 폭의 실행 조건 — 이 도구는 **전부 measured** 인 산출만 읽는다. 그러면 켜져 있었고,
    #    켜진 실행의 격자·시작점은 `null` 일 수 없다 (F2-03 `width_untyped_width_starts`) ──
    if meta.get("widths") is not True:
        p.append(f"{name}: `widths` 가 True 가 아니다 ({meta.get('widths')!r}) — 행이 전부 measured 인데 "
                 f"sidecar 는 폭을 안 켰다고 말한다")
    else:
        for k in ("width_starts", "width_grid"):
            _need(k, lambda v: _int(v) and v >= 0, "0 이상의 정수")

    # ── sidecar 가 같은 것을 두 번 적는 자리 — 두 선언이 어긋나면 어느 쪽이 실행 조건인지 말할 수 없다 (F2-02) ──
    if _int(meta.get("starts")) and _int(meta.get("n_multistart")) \
            and int(meta["starts"]) != int(meta["n_multistart"]):
        p.append(f"{name}: `starts` {meta['starts']} 와 `n_multistart` {meta['n_multistart']} 가 다르다 — "
                 f"같은 실행의 시작점 수를 두 번 적는 자리다")
    return p


def load(path: pathlib.Path):
    """(rows, meta) — 폭이 실려 있지 않으면 여기서 멈춘다."""
    if not path.is_file():
        print(f"! 파일이 없다: {path}", file=sys.stderr); raise SystemExit(2)
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    if not rows:
        print(f"! 행이 없다: {path}", file=sys.stderr); raise SystemExit(2)
    if "width_status" not in rows[0]:
        print(f"! 폭 열이 없다 ({path.name}) — `--widths` 없이 만든 산출이다", file=sys.stderr); raise SystemExit(2)
    st = {r["width_status"] for r in rows}
    if st != {"measured"}:
        print(f"! 폭이 전부 measured 가 아니다 ({path.name}): {sorted(st)} — "
              f"안 잰 행이 섞이면 이 표는 모집단을 말할 수 없다", file=sys.stderr)
        raise SystemExit(2)
    # ① 일반 검증 경로 — 스키마·유한값·receipt·폭 union(뜻까지)·중복 (cell, cycle). 이 도구만의 검사를 따로 두지 않는다.
    header = list(rows[0].keys())
    problems = S.check_rows("cycles", rows, header, path.name)
    if problems:
        print(f"! {path.name} 이 cycles 계약을 어긴다 — 표를 그리지 않는다:", file=sys.stderr)
        for q in problems[:20]:
            print(f"    {q}", file=sys.stderr)
        raise SystemExit(2)
    # ② sidecar 는 선택이 아니다 — 없으면 이 CSV 가 무엇을 읽어 어떤 코드로 나왔는지 말할 수 없다.
    mp = path.with_name(path.name + ".meta.json")
    if not mp.is_file():
        print(f"! sidecar 가 없다: {mp.name} — 결속 없는 폭은 표로 옮길 수 없다", file=sys.stderr); raise SystemExit(2)
    try:
        meta = json.loads(mp.read_text(encoding="utf-8"))
    except ValueError as e:
        print(f"! sidecar 를 못 읽었다 ({mp.name}): {e}", file=sys.stderr); raise SystemExit(2)
    missing = [k for k in REQUIRED_META + COMPARED_SETTINGS if k not in meta]
    if missing:
        print(f"! sidecar 에 필수 키가 없다 ({mp.name}): {missing} — 없는 키는 None 으로 견주지 않는다", file=sys.stderr)
        raise SystemExit(2)
    # ⚠ R17 후속 P1-03 — 키가 **있기만** 하면 통과하던 자리. 필수 값의 타입·형식까지 본다.
    typed = _typed_meta_problems(meta, mp.name)
    if typed:
        print(f"! sidecar 의 필수 값이 타입·형식을 어긴다 ({mp.name}) — 키 존재는 완전성이 아니다:",
              file=sys.stderr)
        for q in typed[:20]:
            print(f"    {q}", file=sys.stderr)
        raise SystemExit(2)
    # ③ 본문 ↔ sidecar — sidecar 가 적은 sha256 이 **이 bytes** 의 것이어야 한다.
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    if str(meta["sha256"]) != sha:
        print(f"! sidecar 의 sha256 이 본문과 다르다 ({path.name}): sidecar {str(meta['sha256'])[:12]} ≠ "
              f"본문 {sha[:12]} — 다른 파일의 sidecar 다", file=sys.stderr)
        raise SystemExit(2)
    # ⚠ R17 후속 2차 F2-04 — ④ 보다 먼저 **행의 cycle 이 정수인지** 본다. ④ 가 그 cycle 로 기대
    #   receipt 를 만들기 때문이다 (전 판은 이 검사가 ⑤ 에 있었고, `cycles_key` 의 `int(float(...))` 가
    #   0.9 를 0 으로 접는 것을 막는 것이 목적이었다 — 그 목적은 그대로다).
    bad_cyc = [r.get("cycle") for r in rows
               if not (str(r.get("cycle")).strip() != "" and _is_int_like(r.get("cycle")))]
    if bad_cyc:
        print(f"! 본문의 cycle 이 정수가 아니다 ({path.name}): {bad_cyc[:8]} — "
              f"절단해서 같은 행으로 취급하지 않는다", file=sys.stderr)
        raise SystemExit(2)
    # ④ 행 ↔ sidecar 입력 결속 — **공통 receipt 와 사이클별 receipt 는 다른 것이다** (R17 후속 2차 F2-04).
    #   sidecar 는 공통 receipt 를 싣고 producer 는 행마다 `full_cell.cycle=k` 를 붙인다. 전 판은 둘이
    #   통째로 같기를 요구해 **정상 생산자의 산출을 rc 2 로 거부**했다 (리뷰어 실측). 이제 그 행의
    #   cycle 로 기대 receipt 를 **구성해** 정확 대조한다 — 부분 비교로 느슨해지는 것이 아니라,
    #   비교 대상이 바뀐 것이다 (digest 도 그 기대 receipt 의 것이어야 한다).
    for i, r in enumerate(rows):
        try:
            want_rec = S.per_cycle_receipt(meta["consumed_inputs"], S.cycles_key(r))
        except (ValueError, TypeError) as e:
            print(f"! sidecar 의 공통 receipt 로 행 {i} 의 기대 receipt 를 만들 수 없다 ({mp.name}): {e}",
                  file=sys.stderr)
            raise SystemExit(2)
        want_inputs = json.dumps(want_rec, sort_keys=True)
        want_sha = S.inputs_digest(want_rec)
        try:
            got = json.dumps(json.loads(r.get("consumed_inputs") or "null"), sort_keys=True)
        except ValueError:
            got = None
        if got != want_inputs or str(r.get("inputs_sha")) != want_sha:
            print(f"! 행 {i} (cycle {r.get('cycle')}) 의 receipt 가 **그 cycle 의 기대 receipt** 와 다르다 "
                  f"({path.name}) — 이 행은 이 sidecar 의 것이 아니다", file=sys.stderr)
            raise SystemExit(2)
    # ⚠ R17 후속 P1-02 — ④ 의 연장: 입력 receipt 만이 아니라 **행이 선언한 실행 조건**도 sidecar 와
    #   같아야 하고, 한 파일 안에서 **하나**여야 한다 (파일 안 버전 혼합을 막는다).
    for row_key, meta_key in BODY_META_BOUND:
        if row_key not in rows[0]:
            continue                                  # 이 산출의 행이 선언하지 않는 축은 건너뛴다
        seen = {str(r.get(row_key)) for r in rows}
        if len(seen) != 1:
            print(f"! 한 파일 안에서 `{row_key}` 가 섞여 있다 ({path.name}): {sorted(seen)} — "
                  f"비교 조건은 파일당 하나여야 한다", file=sys.stderr)
            raise SystemExit(2)
        want = meta.get(meta_key)
        got = seen.pop()
        same = (str(want) == got)
        if not same and isinstance(want, (int, float)) and not isinstance(want, bool):
            try:                                      # 0.01 ↔ "0.01" 같은 표기 차이는 값으로 견준다
                same = float(want) == float(got)
            except (TypeError, ValueError):
                same = False
        if not same:
            print(f"! 본문의 `{row_key}` 가 sidecar 의 `{meta_key}` 와 다르다 ({path.name}): "
                  f"본문 {got!r} ≠ sidecar {want!r} — 이 행들은 그 선언의 것이 아니다", file=sys.stderr)
            raise SystemExit(2)

    # ⑤ 명부 — 본문의 cycle 집합이 sidecar 가 선언한 `cycles` 와 **정확히** 같아야 한다 (중복은 ① 이 잡았다).
    # ⚠ R17 후속 P1-02 — `cycles_key` 는 `int(float(...))` 라 0.9 를 0 으로 접는다. **절단하기 전에**
    #   정수성을 본다 (그러지 않으면 0.9/1.9 가 선언 [0,1] 과 같아 보인다). 그 검사는 ④ 가 그 cycle 로
    #   기대 receipt 를 만들어야 해서 **④ 앞으로 옮겼다** (R17 후속 2차 F2-04) — 규칙은 그대로다.
    body_cycles = sorted(S.cycles_key(r) for r in rows)
    try:
        declared = sorted(int(c) for c in meta["cycles"])
    except (TypeError, ValueError):
        print(f"! sidecar 의 cycles 가 정수 목록이 아니다 ({mp.name}): {meta['cycles']!r}", file=sys.stderr); raise SystemExit(2)
    if body_cycles != declared:
        print(f"! 본문의 cycle 집합 {body_cycles} 이 sidecar 의 선언 {declared} 과 다르다 ({path.name}) — "
              f"빠졌거나 넘친 행이 있다", file=sys.stderr)
        raise SystemExit(2)
    return rows, meta


def span(r, mode) -> float:
    """폭 (%p) — 행의 단위는 분수라 100 을 곱한다."""
    return (float(r[f"{mode}_hi"]) - float(r[f"{mode}_lo"])) * 100.0


def table(rows, meta, path):
    tol = rows[0].get("width_tol", "?")
    print(f"\n══ {path.name}  (허용 {tol} · w_dqdv {meta.get('w_dqdv', '?')} · "
          f"seed {meta.get('seed', '?')} · starts {meta.get('n_multistart', meta.get('starts', '?'))}) ══")
    print(f"{'cyc':>4}  " + "".join(f"{m:^30}" for m in MODES))
    print(f"{'':>4}  " + "".join(f"{'점추정   [ 하한 ,  상한 ]':^30}" for _ in MODES))
    for r in rows:
        line = f"{r['cycle']:>4}  "
        for m in MODES:
            pt = float(r[m]) * 100.0
            lo = float(r[f"{m}_lo"]) * 100.0
            hi = float(r[f"{m}_hi"]) * 100.0
            line += f"{pt:7.2f} [{lo:7.2f},{hi:7.2f}] "
        print(line)
    print(f"{'폭':>4}  " + "".join(
        f"{'':7} 최대 {max(span(r, m) for r in rows):7.2f} %p " for m in MODES))
    if not all(str(r.get("width_is_lower_bound")) == "True" for r in rows):
        print("  ⚠ 어떤 행의 width_is_lower_bound 가 True 가 아니다 — 확인할 것")
    else:
        print("  ⚠ 이 폭은 **하한**이다 (국소 해법 + 격자). 참 폭은 이보다 넓을 수 있다.")
    print("  ⚠ **모델 고정 축**의 폭이다 — 문헌 곡선 선택이 만드는 폭은 여기 안 들어간다.")


def guard_same_except(axis, ma, mb, pa, pb):
    """축 하나 말고 다른 설정이 다르면 **비교를 거부한다.**

    ⚠ R17 후속 3차 F3-02 — 고른 축의 **별칭 무리 전체**를 뺀다. 한 의미를 두 이름으로 세면
      정상 변경이 어느 이름으로도 표현되지 않는다. 무리 안의 일치는 파일마다 이미
      `_typed_meta_problems` 가 요구하므로(`starts == n_multistart`), 무리를 통째로 빼도
      "축 하나만 다르다" 는 약해지지 않는다 — 무리 밖 설정은 전부 그대로 본다.
    """
    if axis not in COMPARED_SETTINGS:
        print(f"! `--axis {axis}` 는 견주는 설정 목록에 없다: {COMPARED_SETTINGS}", file=sys.stderr); raise SystemExit(2)
    group = alias_group(axis)
    diff = [k for k in COMPARED_SETTINGS
            if k not in group and json.dumps(ma.get(k), sort_keys=True) != json.dumps(mb.get(k), sort_keys=True)]
    moved = [k for k in group
             if json.dumps(ma.get(k), sort_keys=True) != json.dumps(mb.get(k), sort_keys=True)]
    if not moved:
        print(f"! 두 실행의 {axis} 가 같다 ({ma.get(axis)!r}) — 이 비교는 그 축의 것이 아니다"
              + (f" (같은 축의 이름 {list(group)} 도 전부 같다)" if len(group) > 1 else ""),
              file=sys.stderr); raise SystemExit(2)
    if diff:
        print(f"! 축({axis}) 말고 다른 설정이 다르다 — 비교하지 않는다:", file=sys.stderr)
        for k in diff:
            print(f"    {k}: {pa.name} {ma.get(k)!r}  ↔  {pb.name} {mb.get(k)!r}", file=sys.stderr)
        raise SystemExit(2)


def guard_same_identity(ma, mb, pa, pb):
    """코드·환경·입력·모집단 선언이 다르면 **비교를 거부한다** — 설정 스무 개가 같아도 그 비교는 축 하나의 것이 아니다."""
    diff = [k for k in BOUND_IDENTITY
            if json.dumps(ma.get(k), sort_keys=True) != json.dumps(mb.get(k), sort_keys=True)]
    if diff:
        print(f"! 두 실행의 결속이 다르다 — 비교하지 않는다 (같은 코드·환경·입력·모집단이어야 축 하나의 비교다):",
              file=sys.stderr)
        for k in diff:
            print(f"    {k}: {pa.name} ≠ {pb.name}", file=sys.stderr)
        raise SystemExit(2)


def compare(axis, ra, ma, pa, rb, mb, pb):
    guard_same_except(axis, ma, mb, pa, pb)
    guard_same_identity(ma, mb, pa, pb)
    ca, cb = {S.cycles_key(r): r for r in ra}, {S.cycles_key(r): r for r in rb}
    # ⚠ R17 P1-04: 교집합으로 비교하지 않는다 — 한쪽에 없는 cycle 이 있으면 두 파일은 같은 모집단이 아니다.
    if sorted(ca) != sorted(cb):
        print(f"! 두 실행의 cycle 집합이 다르다 ({sorted(ca)} ↔ {sorted(cb)}) — 부분 비교는 이 도구가 하지 않는다",
              file=sys.stderr)
        raise SystemExit(2)
    common = sorted(ca)
    print(f"\n══ 폭 비교 — 축 `{axis}`: {ma.get(axis)!r} → {mb.get(axis)!r}  (cycle {len(common)} · 코드·환경·입력·모집단 동일 확인) ══")
    print(f"{'축':>8}  {'A 최대 폭':>12}  {'B 최대 폭':>12}  {'B/A':>8}   판정")
    for m in MODES:
        a = max(span(ca[c], m) for c in common)
        b = max(span(cb[c], m) for c in common)
        ratio = (b / a) if a > 0 else float("nan")
        verdict = ("좁아졌다" if b < a * 0.9 else "넓어졌다" if b > a * 1.1 else "거의 그대로")
        print(f"{m:>8}  {a:9.3f} %p  {b:9.3f} %p  {ratio:8.3f}   {verdict}")
    print("\n  ⚠ 이것은 **이 셀·이 사이클 집합·이 허용**에서의 비교다. 다른 셀로 일반화하지 않는다.")
    print("  ⚠ 폭이 좁아졌다고 그 설정이 '옳다' 는 뜻은 아니다 — 좁은 답이 참에 가깝다는 근거가 따로 필요하다.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="+", type=pathlib.Path, help="cycles_*.csv (하나 또는 둘)")
    ap.add_argument("--axis", default="w_dqdv", help="두 실행에서 **유일하게** 달라야 하는 설정 이름 (기본 w_dqdv)")
    a = ap.parse_args(argv)
    if len(a.csv) > 2:
        print("! 파일은 하나 또는 둘이다", file=sys.stderr); return 2
    loaded = [(p, *load(p)) for p in a.csv]
    for p, rows, meta in loaded:
        table(rows, meta, p)
    if len(loaded) == 2:
        (pa, ra, ma), (pb, rb, mb) = loaded
        compare(a.axis, ra, ma, pa, rb, mb, pb)
    return 0


if __name__ == "__main__":
    sys.exit(main())
