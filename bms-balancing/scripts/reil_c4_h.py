"""REIL C4-0b1 — H 실행기 핵심 + 맞춤 전 배열 · 규칙 봉인 (상태 문서 §46 · 사용자 B 안).

근거: 부속 A §1 (문턱 · ρ · 공통 갱신) · §2 (증인 · 수치 규칙 · 종료 · P0 닫힌 식) · §3-1–§3-6 (옵션 · 순서 · 격자 · 동시 · seed) ·
§4-2–§4-3 (교차 · 끝점) · 부속 B §1-2 (feasibility_class) · §2-1 (봉인 시점) · §3 (격자 index 교차) · v2 §5 (H4 정규화).

    <venv>/bin/python -I bms-balancing/scripts/reil_c4_h.py seal-arrays --out <새 폴더> --p0-result <P0_RESULT.json>
    <venv>/bin/python -I bms-balancing/scripts/reil_c4_h.py dryrun --venv <venv> --seal <C6 봉인> --seal-manifest-sha256 <sha>
        --arrays <Phase A 배열> --h-arrays <0b1 배열> --h-manifest-sha256 <sha> --util-copy <util 사본> --p0-result <P0> --out <새 폴더>

이 파일이 아닌 것: Phase B (profile 순회 · 대체 사슬 · 적응적 시작점 봉인 연결 · 동시 · 명목) · H4 대조 · ray · 표지 (C4-0b2) ·
자료 개봉 · 맞춤 · 실제 H 실행 (C4-A · C4-B). 건조는 계획 · seed · 봉인만 읽는다 (C4 v2 §4-5 · 승인 경계 C4-0B1-A1) —
합성 입력 · 보존 util 사본은 시험에서만 쓴다.
"""
from __future__ import annotations

import copy
import hashlib
import inspect
import io
import json
import math
import os
import sys
import time
import traceback
import warnings
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve()
BMS = HERE.parents[1]
if str(BMS) not in sys.path:
    sys.path.insert(0, str(BMS))

from scripts import reil_c4_e3a as e3a  # noqa: E402
from scripts import reil_c4_monitor as mon  # noqa: E402
from scripts import reil_c5_pilot as c5  # noqa: E402

p0 = c5.p0
prof = c5.prof

LABEL_PREFIX = "reil-v2a"
LABEL_FORMAT = "reil-v2a|<셀 #>|<영역>|<목적>|<단계>|<k>|<격자 index>|<τ>"
ROWS = tuple(range(11))
REGIONS = ("A0", "A1", "A2")
OBJECTIVES = ("J_V", "J_D", "rho", "J_Vs")
STAGES = ("profile", "simultaneous")
COORDS = ("m_P", "m_N", "LII")
SIM_TAUS = ("0.02", "0.05")
#: 단위 77 = 11 셀 × 7 (C4 v2 §1 · 부속 A §3-8) — 순서는 셀마다 이 표 순
UNIT_KINDS = (("J_V", "A0"), ("J_V", "A1"), ("J_V", "A2"), ("J_D", "A0"), ("rho", "A0"), ("J_Vs", "A0"), ("J_Vs", "A1"))
HYPOTHESIS = {"J_V": "H1/H2", "J_D": "H3", "rho": "H3", "J_Vs": "H4"}
VARS = ("m_P", "m_N", "d_P", "d_N")
#: d 상자 (십진 문자열 = 정확 유리수) — m 상자는 P0 의 BOX_M (v2 §1-1 · §4-1 · C6 봉인 BOXES 와 대조 시험)
BOX_D = {"A0": (("0.005", "0.5"), ("0", "1")), "A1": (("-0.5", "1.5"), ("-0.5", "1.5")), "A2": (("-0.5", "1.5"), ("-0.5", "1.5"))}
G_REGIONS = frozenset({"A0", "A1"})
G_LB = F("1e-4")
TOL = F("1e-10")                      # 부속 A §2-2 수용 허용치
NEAR = 1e-9                           # 경계 근접 라벨 (A §2-2 · §1-4)
N_EQ = 41                             # t 범위의 41 등분점 (양 끝 포함 · 상한 46 = 41 + 5 와 맞는 읽기)
GRID_OFFSETS = ("0", "0.02", "-0.02", "0.05", "-0.05")
PROFILE_M, SIM_M, SIM_USE = 1, 4, 12  # Sobol 2 = 2**1 · 16 = 2**4 (앞 12 사용 — 균형 성질 주장 없음, B §2-3)
CUTOFFS = ("2.0", "3.6")
NU = F("0.01")
N_GRID, N_S = 1000, 100
DVDQ_MASK = 0.4
DELTAS = ("0.01", "0.05", "0.1", "0.2")
DELTA_MAIN = "0.1"
PHASE_A_SEEDS, PHASE_A_N = (0, 1), 64
REGION_ARRAY = {"A0": "A0_their_box", "A1": "A1_A2_wide_box", "A2": "A1_A2_wide_box"}
CONTROL_STAGES = frozenset({"control_pos", "control_neg"})
OPTIONS = dict(c5.OPTIONS)            # 부속 A §3-1 의 8 개 = C6 봉인 COBYQA_OPTIONS
DRY_OPTIONS = dict(c5.DRY_OPTIONS)    # 건조 전용 (maxfev 50 · maxiter 100) — 경로 확인
ANNEX_A = BMS / "docs" / "REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md"
ANNEX_B = BMS / "docs" / "REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md"
#: 규칙 기록에 원문 그대로 싣는 절 (파일 · 규칙 · 줄 범위) — 문서 sha256 과 함께 봉인
RULE_EXCERPTS = (
    ("annex_A", "Sobol", (199, 201)), ("annex_A", "격자", (213, 214)), ("annex_A", "중복", (213, 214)),
    ("annex_A", "소거", (215, 216)), ("annex_A", "순회", (217, 218)), ("annex_A", "동률", (217, 218)),
    ("annex_A", "대체", (219, 227)), ("annex_A", "동률", (221, 222)), ("annex_A", "부족", (226, 227)),
    ("annex_A", "격자", (228, 228)), ("annex_A", "동시", (230, 234)), ("annex_A", "seed", (242, 246)),
    ("annex_A", "label", (244, 246)), ("annex_B", "봉인 시점", (95, 102)), ("annex_B", "대체", (104, 112)),
    ("annex_B", "부족", (104, 112)), ("annex_B", "중복", (110, 111)), ("annex_B", "동시", (114, 120)),
    ("annex_B", "동률", (116, 116)), ("annex_B", "중복", (119, 119)), ("annex_B", "부족", (118, 118)),
)
_OURS = frozenset(os.path.realpath(p) for p in (__file__, e3a.__file__, mon.__file__, c5.__file__))


class HStop(Exception):
    """C4-0b1 전역 중단 — 봉인 · 식별 · P0 대조 · 갱신 불변식 · 설정 오류."""


class VFullUnbuildable(ValueError):
    """그들 V_full 구성 (objective_fun 173–189 와 같은 슬라이스) 이 2 점 미만 — 그 x 의 H4 목적은 비유한."""


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def frac_str(x: F) -> str:
    return c5.frac_str(F(x))


def _fin(v) -> bool:
    return v is not None and not isinstance(v, bool) and math.isfinite(float(v))


def _fin_pos(v) -> bool:
    return _fin(v) and float(v) > 0


# ---------------------------------------------------------------- label · seed (부속 A §3-6 · 확인 요청 §1 토큰)
def _int_token(v, name: str, lo: int, hi: int | None = None) -> str:
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or (hi is not None and v > hi):
        raise ValueError(f"{name} 토큰 {v!r} 이 토큰 표 밖")
    return str(v)


def label(row, region, objective, stage, k="-", grid_index="-", tau="-") -> str:
    """`reil-v2a|<셀 #>|<영역>|<목적>|<단계>|<k>|<격자 index>|<τ>` — 해당 없는 칸은 `-` · 표 밖 토큰은 ValueError."""
    cell = _int_token(row, "셀", 0, 10)
    if region not in REGIONS:
        raise ValueError(f"영역 토큰 {region!r} 이 표 밖")
    if objective not in OBJECTIVES:
        raise ValueError(f"목적 토큰 {objective!r} 이 표 밖")
    if stage == "profile":
        if k not in COORDS:
            raise ValueError(f"profile 의 k 토큰 {k!r} 이 표 밖")
        gi = _int_token(grid_index, "격자 index", 0)
        if tau != "-":
            raise ValueError("profile label 의 τ 는 '-'")
        ks, ts = k, "-"
    elif stage == "simultaneous":
        if k != "-" or grid_index != "-":
            raise ValueError("simultaneous label 의 k · 격자 index 는 '-'")
        if tau not in SIM_TAUS:
            raise ValueError(f"τ 토큰 {tau!r} 이 표 밖")
        ks, gi, ts = "-", "-", tau
    else:
        raise ValueError(f"단계 토큰 {stage!r} 이 표 밖")
    return "|".join((LABEL_PREFIX, cell, region, objective, stage, ks, gi, ts))


def seed_of(lab: str) -> int:
    return int(hashlib.sha256(lab.encode("utf-8")).hexdigest()[:8], 16)


def units() -> list:
    return [{"unit": f"{o}|{r}|{row}", "objective": o, "region": r, "row": row, "hypothesis": HYPOTHESIS[o]}
            for row in ROWS for o, r in UNIT_KINDS]


# ---------------------------------------------------------------- 상자 · 격자 (부속 A §2-5 · §3-3 · §3-4)
def region_box_str(region) -> tuple:
    if region not in REGIONS:
        raise ValueError(f"영역 {region!r}")
    (pl, ph), (nl, nh) = p0.BOX_M[region]
    (dpl, dph), (dnl, dnh) = BOX_D[region]
    return (pl, nl, dpl, dnl), (ph, nh, dph, dnh)


def region_bounds(region) -> tuple:
    lo, hi = region_box_str(region)
    return tuple(float(v) for v in lo), tuple(float(v) for v in hi)


def t_range(k, region, max_q) -> tuple:
    """닫힌 식 (A §2-5 끝): m_P · m_N = 상자 구간 · LII = [lo(m_P) − hi(D)/max_q, hi(m_P) − lo(D)/max_q] (정확 유리수)."""
    q = F(max_q)
    if q <= 0:
        raise ValueError("max_q 가 양수가 아님")
    if region not in REGIONS:
        raise ValueError(f"영역 {region!r}")
    (pl, ph), (nl, nh) = p0.BOX_M[region]
    if k == "m_P":
        return F(pl), F(ph)
    if k == "m_N":
        return F(nl), F(nh)
    if k == "LII":
        dlo, dhi = (F(v) for v in p0.D_INT[region])
        return F(pl) - dhi / q, F(ph) - dlo / q
    raise ValueError(f"좌표 {k!r}")


def profile_grid(k, region, row, max_q) -> dict:
    """41 등분점 (정확 유리수 → float) + 명목 · 명목 ± 0.02 · ± 0.05. 범위 밖 (정확 비교) · 같은 float 은 빼고 기록 · 오름차순."""
    lo, hi = t_range(k, region, max_q)
    nominal = F(p0.NOMINAL[row][COORDS.index(k)])
    cand = [(f"등분 {i}", lo + (hi - lo) * F(i, N_EQ - 1)) for i in range(N_EQ)]
    cand += [("명목" if o == "0" else f"명목{'+' if o[0] != '-' else ''}{o}", nominal + F(o)) for o in GRID_OFFSETS]
    pts, skipped, seen = [], [], set()
    for src, v in cand:
        f = float(v)
        if v < lo or v > hi:
            skipped.append({"source": src, "t": frac_str(v), "reason": "미평가 (영역 밖)"})
            continue
        if f in seen:
            skipped.append({"source": src, "t": frac_str(v), "reason": "미평가 (중복)"})
            continue
        seen.add(f)
        pts.append((f, v, src))
    pts.sort(key=lambda p: p[0])
    return {"k": k, "region": region, "row": row, "range": [frac_str(lo), frac_str(hi)], "t": [p[0] for p in pts],
            "t_fraction": [frac_str(p[1]) for p in pts], "source": [p[2] for p in pts], "skipped": skipped}


def free_box(k, region) -> tuple:
    """등식 소거 뒤 자유 변수와 그 상자 (A §3-3): m_P · m_N → 나머지 셋 · LII → d_N 소거 (m_P · m_N · d_P)."""
    lo, hi = region_box_str(region)
    box = {n: (a, b) for n, a, b in zip(VARS, lo, hi)}
    names = {"m_P": ("m_N", "d_P", "d_N"), "m_N": ("m_P", "d_P", "d_N"), "LII": ("m_P", "m_N", "d_P")}[k]
    return names, tuple(box[n][0] for n in names), tuple(box[n][1] for n in names)


def sim_box(row, region, tau, max_q):
    """동시 양립 상자 P × N × (d_P 상자) × (d_N 상자) (A §3-4) — P0 닫힌 식이 PRIOR_INCOMPATIBLE 이면 None."""
    st = p0.prior_compat(p0.NOMINAL[row], tau, region, F(max_q))
    if st["status"] == "PRIOR_INCOMPATIBLE":
        return None
    if st["status"] != "PRIOR_COMPATIBLE":
        raise HStop(f"P0 상태 {st['status']} (#{row} · τ {tau} · {region})")
    t = F(tau)
    P = p0._clip(F(p0.NOMINAL[row][0]), t, p0.BOX_M[region][0])
    N = p0._clip(F(p0.NOMINAL[row][1]), t, p0.BOX_M[region][1])
    (dpl, dph), (dnl, dnh) = BOX_D[region]
    return (P[0], N[0], F(dpl), F(dnl)), (P[1], N[1], F(dph), F(dnh))


def _p0_max_q(res) -> F:
    mq = res.get("max_q") or {}
    if mq.get("status") != "OK":
        raise HStop(f"P0 max_q 상태 {mq.get('status')}")
    q = F(mq["fraction"])
    if q <= 0 or float(q) != float(mq["float"]):
        raise HStop("P0 max_q 의 분수와 float 이 맞지 않는다")
    return q


def array_plan(res, units_sel=None) -> dict:
    """P0 기록 → 봉인할 label 전부 (profile Sobol 2 · 동시 Sobol 16). 99 칸 사전표를 닫힌 식으로 다시 계산해 기록과 대조한다."""
    q = _p0_max_q(res)
    recorded = {(e.get("row"), e.get("tau"), e.get("region")): e.get("status") for e in res.get("prior_table", [])}
    for row in ROWS:
        for tau in p0.TAUS:
            for region in REGIONS:
                st = p0.prior_compat(p0.NOMINAL[row], tau, region, q)["status"]
                if recorded.get((row, tau, region)) != st:
                    raise HStop(f"P0 사전표 기록 {recorded.get((row, tau, region))} ≠ 재계산 {st} (#{row} · τ {tau} · {region})")
    us = units()
    if units_sel is not None:                              # 부분 봉인 (시험용) — 요청 순서 그대로 · 전체 봉인은 units() 순서
        want, by = list(units_sel), {u["unit"]: u for u in us}
        if len(want) != len(set(want)) or any(w not in by for w in want):
            raise HStop(f"모르는 · 중복 단위: {want}")
        us = [by[w] for w in want]
    entries, skipped_sim, grids = [], [], []
    for u in us:
        for k in COORDS:
            g = profile_grid(k, u["region"], u["row"], q)
            names, lo, hi = free_box(k, u["region"])
            grids.append({"unit": u["unit"], "k": k, "range": g["range"], "n": len(g["t"]), "source": g["source"],
                          "skipped": g["skipped"]})
            for gi, (t, tf) in enumerate(zip(g["t"], g["t_fraction"])):
                lab = label(u["row"], u["region"], u["objective"], "profile", k=k, grid_index=gi)
                entries.append({"label": lab, "seed": seed_of(lab), "unit": u["unit"], "stage": "profile", "k": k,
                                "grid_index": gi, "t": t, "t_fraction": tf, "tau": "-", "box_names": list(names),
                                "box_lo": list(lo), "box_hi": list(hi), "n": 2, "m": PROFILE_M})
        for tau in SIM_TAUS:
            sb = sim_box(u["row"], u["region"], tau, q)
            if sb is None:
                skipped_sim.append({"unit": u["unit"], "tau": tau, "reason": "PRIOR_INCOMPATIBLE (P0) — 돌리지 않는다 (부속 A §3-4)"})
                continue
            lab = label(u["row"], u["region"], u["objective"], "simultaneous", tau=tau)
            entries.append({"label": lab, "seed": seed_of(lab), "unit": u["unit"], "stage": "simultaneous", "k": "-",
                            "grid_index": "-", "t": None, "t_fraction": None, "tau": tau, "box_names": list(VARS),
                            "box_lo": [frac_str(v) for v in sb[0]], "box_hi": [frac_str(v) for v in sb[1]], "n": 16,
                            "m": SIM_M, "use": SIM_USE})
    return {"max_q_fraction": frac_str(q), "units": [u["unit"] for u in us], "entries": entries,
            "skipped_simultaneous": skipped_sim, "grids": grids}


# ---------------------------------------------------------------- Sobol · 봉인 (부속 A §3-1 · B §2-1 · C4 v2 §4-3)
def _seed_keyword() -> str:
    from scipy.stats import qmc
    return "rng" if "rng" in inspect.signature(qmc.Sobol).parameters else "seed"


def sobol_points(seed, lo, hi, m):
    """C6 봉인 `sobol` 과 같은 호출: `qmc.Sobol(d, scramble=True, <kw>=seed).random_base2(m)` → `qmc.scale`. 경고는 fail-closed."""
    import numpy as np
    from scipy.stats import qmc
    lo_f, hi_f = [float(F(str(v))) for v in lo], [float(F(str(v))) for v in hi]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        unit = qmc.Sobol(d=len(lo_f), scramble=True, **{_seed_keyword(): seed}).random_base2(m=m)
        a = qmc.scale(unit, lo_f, hi_f)
    if caught:
        raise HStop(f"Sobol 생성 경고 (seed {seed}): {[str(w.message) for w in caught][:3]}")
    return np.ascontiguousarray(a, dtype="<f8")


def _build_arrays(plan) -> dict:
    import numpy as np
    by_file: dict = {}
    for e in plan["entries"]:
        rel = f"{e['stage']}/{e['unit'].replace('|', '_')}.npy"
        a = sobol_points(e["seed"], e["box_lo"], e["box_hi"], e["m"])
        if a.shape != (e["n"], len(e["box_lo"])):
            raise HStop(f"{e['label']}: 배열 모양 {a.shape}")
        blocks = by_file.setdefault(rel, [])
        r0 = sum(b.shape[0] for b in blocks)
        blocks.append(a)
        e.update(file=rel, rows=[r0, r0 + a.shape[0]], raw_sha256=_sha(a.tobytes()))
    return {rel: np.ascontiguousarray(np.vstack(bl), dtype="<f8") for rel, bl in by_file.items()}


def _attach_from_files(plan, d) -> dict:
    """생성기 없이 봉인 npy 에서 블록을 잘라 file · rows · raw_sha256 을 붙인다 — `_build_arrays` 와 같은 배치 (단위 · 단계마다 계획 순서로 쌓음).
    npy 는 float64 little-endian 2 차원이어야 하고, 행 수가 계획의 합과 같아야 한다."""
    import numpy as np
    loaded, used = {}, {}
    for e in plan["entries"]:
        rel = f"{e['stage']}/{e['unit'].replace('|', '_')}.npy"
        if rel not in loaded:
            a = np.load(io.BytesIO(e3a._read(Path(d) / rel)), allow_pickle=False)
            if a.dtype != np.dtype("<f8") or a.ndim != 2:
                raise HStop(f"{rel}: dtype · 차원 {a.dtype} · {a.shape}")
            loaded[rel] = a
        r0 = used.get(rel, 0)
        block = loaded[rel][r0:r0 + e["n"]]
        if block.shape != (e["n"], len(e["box_lo"])):
            raise HStop(f"{e['label']}: 블록 모양 {block.shape}")
        e.update(file=rel, rows=[r0, r0 + e["n"]], raw_sha256=_sha(np.ascontiguousarray(block, dtype="<f8").tobytes()))
        used[rel] = r0 + e["n"]
    short = sorted(rel for rel, a in loaded.items() if a.shape[0] != used[rel])
    if short:
        raise HStop(f"npy 행 수가 계획의 합과 다르다: {short[:3]}")
    return loaded


def rules_record() -> dict:
    """규칙 · label 형식 기록 (B §2-1 맞춤 전 봉인) — 순회 · 동률 · 대체 · 중복 · 부족은 등록 원문 그대로 (줄 범위 · 문서 sha256)."""
    sources = {}
    for key, path in (("annex_A", ANNEX_A), ("annex_B", ANNEX_B)):
        b = path.read_bytes()
        lines = b.decode("utf-8").splitlines()
        sources[key] = {"path": str(path.relative_to(BMS)), "sha256": _sha(b), "excerpts": [
            {"rule": rule, "lines": [a, z], "text": "\n".join(lines[a - 1:z])} for k2, rule, (a, z) in RULE_EXCERPTS if k2 == key]}
    return {
        "schema": "reil-c4-0b1-rules-v1",
        "label_format": LABEL_FORMAT,
        "tokens": {"셀 #": [str(r) for r in ROWS], "영역": list(REGIONS), "목적": list(OBJECTIVES), "단계": list(STAGES),
                   "k": list(COORDS) + ["-"], "격자 index": "오름차순 격자의 0 부터 번호 (해당 없으면 '-')", "τ": list(SIM_TAUS) + ["-"]},
        "seed": "int(hashlib.sha256(label.encode('utf-8')).hexdigest()[:8], 16)",
        "grid": {"equal_points": N_EQ, "equal_points_reading": "t 범위 양 끝 포함 41 점 (lo + (hi − lo)·i/40 · 정확 유리수 → float)",
                 "extra": list(GRID_OFFSETS), "outside": "정확 유리수로 범위 밖 → 미평가 (영역 밖)",
                 "duplicate": "같은 float → 미평가 (중복) · 41 등분점이 먼저", "order": "float 오름차순 · 격자 index = 그 순번"},
        "sobol": {"call": "scipy.stats.qmc.Sobol(d, scramble=True, <rng|seed>=label seed).random_base2(m) → qmc.scale(lo, hi)",
                  "profile": "m = 1 (2 점) · 자유 변수 상자 (A §3-3 소거)", "simultaneous": "m = 4 (16 점) · 앞 12 사용 (B §2-3)",
                  "warnings": "생성 경고는 봉인 중단"},
        "simultaneous_skip": "P0 닫힌 식 PRIOR_INCOMPATIBLE 인 (셀 · τ · 영역) 의 단위는 label 을 만들지 않는다 (A §3-4)",
        "not_sealed_here": "적응적 시작점 (profile s1 · s2 · 동시 양립의 Phase A 상위 증인) — 그것을 쓰는 지역 실행 직전 봉인 (부속 B §2-1 둘째 행 · C4-0b2)",
        "interpretations": [
            "C4 v2 §4-3 의 'label-seed 배열' = label → seed 표 (LABEL_SEED_TABLE.json) — 검토 확인 대상",
            "41 등분점 = 양 끝 포함 41 점 (확인 요청 §1 의 상한 ≤ 46 = 41 + 5 와 맞는 읽기)",
        ],
        "sources": sources,
    }


def _index_obj(plan) -> dict:
    return {"schema": "reil-c4-0b1-h-arrays-index-v1", "max_q_fraction": plan["max_q_fraction"], "units": plan["units"],
            "entries": plan["entries"], "skipped_simultaneous": plan["skipped_simultaneous"], "grids": plan["grids"]}


def _generator_record() -> dict:
    import numpy
    import scipy
    return {"call": "scipy.stats.qmc.Sobol(d, scramble=True, <kw>=seed).random_base2(m) → qmc.scale", "seed_keyword": _seed_keyword(),
            "scipy": scipy.__version__, "numpy": numpy.__version__}


def seal_h_arrays(out, *, p0_result, units=None) -> dict:
    """맞춤 전 봉인 (B §2-1 첫 행) — 단위마다 npy (profile · simultaneous) + INDEX · LABEL_SEED_TABLE · RULES · MANIFEST. 새 폴더만."""
    import numpy as np
    out = Path(out)
    e3a._guard([out, p0_result])
    part = out.with_name(out.name + ".partial")
    if out.exists() or part.exists():
        raise HStop(f"{out} (또는 .partial) 가 이미 있다 — 덮어쓰지 않는다")
    p0b = e3a._read(p0_result)
    plan = array_plan(json.loads(p0b), units)
    arrays = _build_arrays(plan)
    docs = {"INDEX.json": c5.dump(_index_obj(plan)),
            "LABEL_SEED_TABLE.json": c5.dump([[e["label"], e["seed"]] for e in plan["entries"]]),
            "RULES.json": c5.dump(rules_record())}
    part.mkdir(parents=False)
    for rel, a in arrays.items():
        (part / rel).parent.mkdir(exist_ok=True)
        np.save(part / rel, a, allow_pickle=False)
    for name, b in docs.items():
        (part / name).write_bytes(b)
    files = {str(p.relative_to(part)): p.read_bytes() for p in sorted(part.rglob("*")) if p.is_file()}
    n_prof = sum(e["stage"] == "profile" for e in plan["entries"])
    man = {"schema": "reil-c4-0b1-h-arrays-v1", "files": {rel: {"bytes": len(b), "sha256": _sha(b)} for rel, b in files.items()},
           "units": plan["units"], "complete": len(plan["units"]) == len(UNIT_KINDS) * len(ROWS),
           "n_labels": len(plan["entries"]), "n_profile_labels": n_prof, "n_simultaneous_labels": len(plan["entries"]) - n_prof,
           "n_skipped_simultaneous": len(plan["skipped_simultaneous"]), "p0_result_sha256": _sha(p0b),
           "max_q_fraction": plan["max_q_fraction"], "generator": _generator_record(), "label_format": LABEL_FORMAT,
           "not_sealed_here": rules_record()["not_sealed_here"]}
    mb = c5.dump(man)
    (part / "MANIFEST.json").write_bytes(mb)
    part.rename(out)
    if _sha((out / "MANIFEST.json").read_bytes()) != _sha(mb):
        raise HStop("MANIFEST 를 다시 읽은 바이트가 쓴 것과 다르다")
    return {"ok": True, "out": str(out), "manifest_sha256": _sha(mb), "n_labels": man["n_labels"],
            "n_profile_labels": n_prof, "n_simultaneous_labels": man["n_simultaneous_labels"],
            "n_skipped_simultaneous": man["n_skipped_simultaneous"], "complete": man["complete"], "n_files": len(files) + 1}


def check_h_arrays(arrays_dir, *, manifest_sha256, p0_result, regenerate=True) -> dict:
    """봉인 대조 — MANIFEST 를 명시 sha256 으로 인증 · 파일 목록 · 바이트 · P0 · 계획 (label · seed · 격자 · 상자) · 기록 문서를 맞춘다.
    regenerate=True: Sobol 배열을 다시 만들어 바이트 대조 (봉인 단계 · 시험). regenerate=False: 생성기를 부르지 않고 봉인 npy 바이트에서
    블록 raw sha 를 다시 계산해 INDEX 와 맞춘다 — 읽기 전용 건조용 (C4 v2 §4-5 '계획 · seed · 봉인만 읽음' · 승인 경계 C4-0B1-A1)."""
    import numpy as np
    d = Path(arrays_dir)
    e3a._guard([d, p0_result])
    mb = e3a._read(d / "MANIFEST.json")
    if _sha(mb) != manifest_sha256:
        raise HStop(f"0b1 배열 MANIFEST sha256 {_sha(mb)} ≠ 명시 {manifest_sha256}")
    man = json.loads(mb)
    present = sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file() and p.name != "MANIFEST.json")
    if present != sorted(man["files"]):
        raise HStop(f"0b1 배열 파일 목록이 MANIFEST 와 다르다: {sorted(set(present) ^ set(man['files']))[:5]}")
    for rel, rec in man["files"].items():
        if _sha(e3a._read(d / rel)) != rec["sha256"]:
            raise HStop(f"{rel} 의 바이트가 MANIFEST 와 다르다")
    p0b = e3a._read(p0_result)
    if _sha(p0b) != man["p0_result_sha256"]:
        raise HStop("P0 결과 sha256 이 봉인 기록과 다르다")
    plan = array_plan(json.loads(p0b), man["units"])
    npy = sorted(r for r in man["files"] if r.endswith(".npy"))
    if regenerate:
        arrays = _build_arrays(plan)
        if sorted(arrays) != npy:
            raise HStop("재생성한 배열 파일 집합이 봉인과 다르다")
        for rel, a in arrays.items():
            got = np.load(io.BytesIO(e3a._read(d / rel)), allow_pickle=False)
            if got.dtype != a.dtype or got.shape != a.shape or got.tobytes() != a.tobytes():
                raise HStop(f"{rel}: 재생성 배열이 봉인과 다르다")
    elif sorted(_attach_from_files(plan, d)) != npy:
        raise HStop("계획이 가리키는 배열 파일 집합이 봉인과 다르다")
    want = {"INDEX.json": c5.dump(_index_obj(plan)), "LABEL_SEED_TABLE.json": c5.dump([[e["label"], e["seed"]] for e in plan["entries"]]),
            "RULES.json": c5.dump(rules_record())}
    for name, b in want.items():
        if e3a._read(d / name) != b:
            raise HStop(f"{name}: 재생성 기록이 봉인과 다르다")
    return {"ok": True, "arrays_dir": str(d), "manifest_sha256": manifest_sha256, "n_labels": len(plan["entries"]),
            "units": len(man["units"]), "complete": bool(man["complete"]) and len(man["units"]) == len(UNIT_KINDS) * len(ROWS),
            "mode": "regenerate" if regenerate else "bytes", "regenerated_match": True if regenerate else None,
            "generator": man["generator"]}


# ---------------------------------------------------------------- 목적 (v2 §2 · §5 · 부속 A §4-2–§4-3 · B §3)
def jv_jd(util, x, model, halfcell) -> tuple:
    """J_V = sqrt(f2) · J_D = sqrt(f4) — 그들 objective_fun 1 회 (f4 는 그들 마스크 dVdQ_exp < 0.4 를 이미 쓴다)."""
    import numpy as np
    f = util.objective_fun(np.asarray(x, dtype=float), model, halfcell)
    return float(np.sqrt(f[1])), float(np.sqrt(f[3]))


def rho(jv, jd, jhat_v, jhat_d) -> float:
    """ρ = max(J_V/Ĵ_V, J_D/Ĵ_D) (A §1-3) — 분모가 유한한 양수가 아니면 ValueError · 성분 하나라도 비유한이면 nan."""
    if not (_fin_pos(jhat_v) and _fin_pos(jhat_d)):
        raise ValueError(f"ρ 분모가 유한한 양수가 아님: {jhat_v!r} · {jhat_d!r}")
    if not (_fin(jv) and _fin(jd)):
        return float("nan")
    return max(float(jv) / float(jhat_v), float(jd) / float(jhat_d))


def jd_gate(model) -> dict:
    """자료 쪽 J_D 조건 (v2 그대로) — 마스크 dVdQ_exp_interp < 0.4 가 비면 그 셀의 J_D · ρ = UNFIT."""
    import numpy as np
    m = np.asarray(model["dVdQ_exp_interp"], dtype=float) < DVDQ_MASK
    return {"ok": True, "reason": None} if bool(np.any(m)) else {"ok": False, "reason": "빈 마스크 (dVdQ_exp_interp < 0.4 인 점 0)"}


def crossings(Q, V, c) -> dict:
    """cutoff c 교차 (부속 B §3): 평탄 거부 → 격자점 교차 (정체성 = index j · 위치 Q_j) → 엄격 부호 변화 구간의 선형 보간."""
    import numpy as np
    Q, V, c = np.asarray(Q, dtype=float), np.asarray(V, dtype=float), float(c)
    eq = V == c
    if bool(np.any(eq[:-1] & eq[1:])):
        return {"c": c, "flat": True, "items": [], "n_unique": None}
    items = [{"kind": "grid", "index": int(j), "Q": float(Q[j])} for j in np.flatnonzero(eq)]
    dv = V - c
    for j in np.flatnonzero((dv[:-1] * dv[1:] < 0) & ~eq[:-1] & ~eq[1:]):
        j = int(j)
        items.append({"kind": "interior", "interval": [j, j + 1],
                      "Q": float(Q[j] + (c - V[j]) * (Q[j + 1] - Q[j]) / (V[j + 1] - V[j]))})
    items.sort(key=lambda it: it["index"] if it["kind"] == "grid" else it["interval"][0] + 0.5)
    return {"c": c, "flat": False, "items": items, "n_unique": len(items)}


def endpoint_gate(v_first, v_last) -> dict:
    """실험 쪽 끝점 수용 (A §4-3): c_a = V_first 에 가까운 cutoff (같으면 2.0) · 수용 ⇔ |V_first − c_a| ≤ ν 且 |V_last − c_b| ≤ ν (정확 비교)."""
    fa, fb = F(float(v_first)), F(float(v_last))
    cs = [F(c) for c in CUTOFFS]
    ia = 0 if abs(fa - cs[0]) <= abs(fa - cs[1]) else 1
    c_a, c_b = cs[ia], cs[1 - ia]
    dev_a, dev_b = abs(fa - c_a), abs(fb - c_b)
    return {"accepted": dev_a <= NU and dev_b <= NU, "c_a": float(c_a), "c_b": float(c_b), "V_first": float(v_first),
            "V_last": float(v_last), "dev_first": float(dev_a), "dev_last": float(dev_b), "nu": float(NU)}


def synthetic_wide_inputs(util) -> tuple:
    """건조 · 시험 입력 — 해석식 단조 곡선 (REIL 자료 아님). 완전지 V 가 2.0 · 3.6 V 를 한 번씩 지나고 실험 곡선이 2.0 → 3.6 V."""
    import numpy as np
    q_pe = np.linspace(0.0, 3.2, 400)
    v_pe = 3.2 + 0.2 * q_pe / 3.2 + 0.2 * (1.0 + np.tanh(10.0 * (q_pe - 3.05)))
    q_ne = np.linspace(0.0, 3.6, 400)
    v_ne = 0.05 + 1.5 * np.exp(-3.0 * q_ne)
    q = np.linspace(0.0, 3.0, 300)
    v = 2.0 + 1.6 * (q / 3.0) ** 2
    model = util.extract_battery_data([np.vstack([q, v])], 0)
    return model, [q_pe, v_pe, q_ne, v_ne]


def v_full(util, x, halfcell) -> tuple:
    """모델 완전지 V_full(Q) — 그들 objective_fun 173–189 와 같은 구성 (dVdQ_hc 500 점 · [Q0:Qmax] 슬라이스 · 같은 interp1d 채움값).
    반환: (V_full 호출 가능 객체, max Q_PE = Q_PE_hc_ad[argmax]). 슬라이스가 2 점 미만이면 VFullUnbuildable."""
    import numpy as np
    from scipy.interpolate import interp1d
    m_P, m_N, d_P, d_N = (float(v) for v in x)
    out = util.dVdQ_hc(halfcell[1], halfcell[0], halfcell[3], halfcell[2], m_P, m_N, d_P, d_N, interp_len=500)
    qp, qn, vp, vn = (np.asarray(out[i], dtype=float) for i in (0, 1, 4, 5))
    p0i, n0i, pmi, nmi = int(np.argmin(np.abs(qp))), int(np.argmin(np.abs(qn))), int(np.argmax(qp)), int(np.argmax(qn))
    if pmi - p0i < 2 or nmi - n0i < 2:
        raise VFullUnbuildable(f"슬라이스 PE {pmi - p0i} · NE {nmi - n0i} 점 < 2")
    fp = interp1d(qp[p0i:pmi], vp[p0i:pmi], fill_value="extrapolate")
    fn = interp1d(qn[n0i:nmi], vn[n0i:nmi], fill_value=(1.5, 0.01), bounds_error=False)
    return (lambda q: fp(q) - fn(q)), float(qp[pmi])


def j_vs(util, x, model, halfcell, gate) -> dict:
    """J_V^s = RMSE_k |V_sim(s_k) − V_exp(s_k)| · s_k = linspace(0, 1, 100) (v2 §5).
    모델: 1000 점 격자 Q_j = linspace(0, max Q_PE, 1000) 의 교차 (B §3) · V_sim(s_k) = V_full(Q_a + s_k·span) 직접 평가.
    실험: Q_exp_interp = linspace(0, Q_exp_max, 100) 이 곧 s_k 격자이므로 V_exp(s_k) = V_exp_interp[k] (보간 없음).
    비유한 사유: V_full 구성 불가 · V_j 비유한 · 평탄 · 유일 교차 ≠ 1 · span ≤ 0. 수용되지 않은 끝점 셀은 ValueError (정의하지 않음)."""
    import numpy as np
    if not gate.get("accepted"):
        raise ValueError("H4 끝점 수용이 아닌 셀 — J_V^s 를 정의하지 않는다 (부속 A §4-3)")
    v_exp = np.asarray(model["V_exp_interp"], dtype=float)
    if v_exp.shape != (N_S,):
        raise ValueError(f"V_exp_interp 모양 {v_exp.shape} ≠ ({N_S},)")
    rec = {"value": float("nan"), "reason": None, "crossings": None, "Q_a": None, "Q_b": None, "span": None, "max_Q_PE": None}
    try:
        fn, qmax = v_full(util, x, halfcell)
    except VFullUnbuildable as e:
        rec["reason"] = f"V_full 구성 불가 ({e})"
        return rec
    rec["max_Q_PE"] = qmax
    if not (math.isfinite(qmax) and qmax > 0):
        rec["reason"] = "V_full 격자 불가 (max Q_PE ≤ 0 · 비유한)"
        return rec
    qg = np.linspace(0.0, qmax, N_GRID)
    vg = np.asarray(fn(qg), dtype=float)
    if not bool(np.all(np.isfinite(vg))):
        rec["reason"] = "V_j 비유한"
        return rec
    cr = {c: crossings(qg, vg, float(c)) for c in CUTOFFS}
    rec["crossings"] = cr
    for c in CUTOFFS:
        if cr[c]["flat"]:
            rec["reason"] = f"평탄 ({c} V)"
            return rec
        if cr[c]["n_unique"] != 1:
            rec["reason"] = f"유일 교차 {cr[c]['n_unique']} ≠ 1 ({c} V)"
            return rec
    key = {float(c): c for c in CUTOFFS}
    q_a, q_b = cr[key[gate["c_a"]]]["items"][0]["Q"], cr[key[gate["c_b"]]]["items"][0]["Q"]
    rec.update(Q_a=q_a, Q_b=q_b, span=q_b - q_a)
    if not rec["span"] > 0:
        rec["reason"] = "span"
        return rec
    s = np.linspace(0.0, 1.0, N_S)
    v_sim = np.asarray(fn(q_a + s * rec["span"]), dtype=float)
    val = float(np.sqrt(np.mean((v_sim - v_exp) ** 2)))
    if not math.isfinite(val):
        rec["reason"] = "RMSE 비유한"
    rec["value"] = val
    return rec


# ---------------------------------------------------------------- 정확 잔차 · 증인 · 종료 (부속 A §2-1–§2-3 · B §1-2 · §2-5)
def exact_residuals(x, region):
    """상자 (좌표별) · G (A0 · A1 만) 잔차를 정확 유리수로. 비유한 x → None (그 점은 NONFINITE)."""
    if region not in REGIONS:
        raise ValueError(f"영역 {region!r}")
    try:
        fx = [F(float(v)) for v in x]
    except (ValueError, OverflowError, TypeError):
        return None
    if len(fx) != 4:
        raise ValueError(f"x 길이 {len(fx)} ≠ 4")
    lo, hi = region_box_str(region)
    by = [max(F(a) - v, v - F(b), F(0)) for v, a, b in zip(fx, lo, hi)]
    g = max(G_LB - (fx[2] - fx[3]), F(0)) if region in G_REGIONS else None
    return {"box": max(by), "box_by_coord": by, "g": g}


def feasibility_class(res) -> str:
    """B §1-2: exact_feasible (모든 잔차 = 0) · numerically_accepted (> 0 이 있으나 모두 ≤ 1e-10) · 그 밖 infeasible · nonfinite."""
    if res is None:
        return "nonfinite"
    vals = [res["box"]] + ([res["g"]] if res.get("g") is not None else [])
    if all(v == 0 for v in vals):
        return "exact_feasible"
    return "numerically_accepted" if all(v <= TOL for v in vals) else "infeasible"


def witness(*, solver_error, value, residuals, reeval_error=False) -> str:
    """A §2-1 · C4 v2 §5-3: SOLVER_ERROR (최적화 중 지역 예외 — 반환점 없음) · REEVAL_ERROR (반환점의 독립 재평가 중 지역 예외 — C4 · H 에도
    따로 기록 · C4-0B1-N3) · NONFINITE (재평가가 정상 반환한 비유한 · 교차 실패 · x 비유한) · INFEASIBLE_RETURN (§2-2 밖). termination 은 따로."""
    if solver_error:
        return "invalid:SOLVER_ERROR"
    if reeval_error:
        return "invalid:REEVAL_ERROR"
    if value is None or not math.isfinite(value) or residuals is None:
        return "invalid:NONFINITE"
    return "valid" if feasibility_class(residuals) in ("exact_feasible", "numerically_accepted") else "invalid:INFEASIBLE_RETURN"


def termination(res) -> str:
    """A §2-3 · C4 v2 §5-4: converged (solver 성공) · budget (MAX_EVAL · MAX_ITER) · 그 밖 status 는 unclassified (C5 `termination_of` 그대로) —
    알려진 셋에 매핑하지 않고 전체 중지한다 (C4 v2 §6 · C4-0B1-N2). solver_error 는 최적화 중 지역 예외 (반환점 없음) 에만 쓴다."""
    return c5.termination_of(res)


def active_set(x, region) -> dict:
    """활성 경계 · 활성 G (B §2-5 기록 항목) — 경계와의 정확 거리 ≤ 1e-10."""
    fx = [F(float(v)) for v in x]
    lo, hi = region_box_str(region)
    b = []
    for n, v, a, z in zip(VARS, fx, lo, hi):
        if abs(v - F(a)) <= TOL:
            b.append([n, "lo"])
        if abs(v - F(z)) <= TOL:
            b.append([n, "hi"])
    return {"bounds": b, "g": (abs(fx[2] - fx[3] - G_LB) <= TOL) if region in G_REGIONS else None}


def classify(exc: BaseException, stage: str, util_file=None) -> dict:
    """오류 분류 — C5 규칙 (지역 = 구조 목록 밖 且 (optimize: util · optimizer) 또는 (reeval · label: util)) 에 '우리' 파일 집합만 넓힘."""
    frames = traceback.extract_tb(exc.__traceback__)
    uf = os.path.realpath(str(util_file)) if util_file else None
    origin, seen_scipy = None, False
    for fr in reversed(frames):
        f = os.path.realpath(fr.filename)
        if uf and f == uf:
            origin = "util"
            break
        if f in _OURS:
            origin = "optimizer" if seen_scipy else "ours"
            break
        if f"{os.sep}scipy{os.sep}" in f:
            seen_scipy = True
    if origin is None:
        origin = "optimizer" if seen_scipy else "ours"
    local = not isinstance(exc, c5.STRUCTURAL) and (
        (stage == "optimize" and origin in ("util", "optimizer")) or (stage in ("reeval", "label") and origin == "util"))
    return {"kind": "local" if local else "structural", "origin": origin, "stage": stage, "type": type(exc).__name__,
            "message": str(exc)[:500], "traceback": [f"{Path(fr.filename).name}:{fr.lineno}:{fr.name}" for fr in frames[-6:]]}


# ---------------------------------------------------------------- Phase A (부속 A §3-2 · §2-3 · §2-4)
def load_phase_a_arrays(arrays_dir) -> dict:
    """C4-0a 봉인 배열 (seed 0 · 1 · 영역 상자) — 폴더 MANIFEST 의 sha 와 바이트 대조 (C6 결속은 e3a.check_arrays 가 따로)."""
    import numpy as np
    d = Path(arrays_dir)
    man = json.loads(e3a._read(d / "MANIFEST.json"))
    out = {}
    for region in REGIONS:
        for seed in PHASE_A_SEEDS:
            name = f"sobol_{REGION_ARRAY[region]}_seed{seed}.npy"
            b = e3a._read(d / name)
            if _sha(b) != man.get(name):
                raise HStop(f"Phase A 배열 {name} 의 바이트가 MANIFEST 와 다르다")
            a = np.load(io.BytesIO(b), allow_pickle=False)
            if a.shape != (PHASE_A_N, 4) or a.dtype != np.dtype("<f8"):
                raise HStop(f"Phase A 배열 {name} 모양 {a.shape} · {a.dtype}")
            out[(region, seed)] = a
    return out


def phase_a_tasks(unit_list, arrays, n_workers, start_id=0) -> list:
    """단위마다 128 실행 = seed 0 의 64 (run_id 0–63) + seed 1 의 64 (64–127) · 작업자 = task_id % n (G 위반 시작점 그대로)."""
    tasks, tid = [], start_id
    for u in unit_list:
        for seed in PHASE_A_SEEDS:
            a = arrays[(u["region"], seed)]
            for i in range(PHASE_A_N):
                tasks.append({"task_id": tid, "worker": tid % n_workers, "run_id": seed * PHASE_A_N + i, "unit": u["unit"],
                              "objective": u["objective"], "region": u["region"], "row": u["row"], "seed": seed,
                              "start_index": i, "x0": [float(v) for v in a[i]]})
                tid += 1
    return tasks


def _evaluate(task, ctx, x, model) -> tuple:
    obj, util, hc, row = task["objective"], ctx["util"], ctx["halfcell"], task["row"]
    if obj == "J_Vs":
        rec = j_vs(util, x, model, hc, ctx["gates"][row])
        return rec["value"], rec
    jv, jd = jv_jd(util, x, model, hc)
    if obj == "J_V":
        return jv, None
    if obj == "J_D":
        return jd, None
    den = ctx["denominators"][row]
    return rho(jv, jd, den[0], den[1]), {"J_V": jv, "J_D": jd}


def _check_task(task, ctx) -> None:
    if task["objective"] not in OBJECTIVES or task["region"] not in REGIONS:
        raise HStop(f"작업 {task.get('task_id')}: 목적 · 영역 {task['objective']} · {task['region']}")
    if task["objective"] == "rho":
        den = ctx["denominators"][task["row"]]
        if not (_fin_pos(den[0]) and _fin_pos(den[1])):
            raise HStop(f"#{task['row']} ρ 분모 {den} 가 유한한 양수가 아님")
    if task["objective"] == "J_Vs" and not ctx["gates"][task["row"]].get("accepted"):
        raise HStop(f"#{task['row']} H4 끝점 수용 아님 — 실행하지 않는다")


def _partial(acc, info) -> dict:
    """구조 중지의 부분 기록 (C4-0B1-N1 · 부속 B §2-5 · C4 v2 §6) — 그때까지의 행 · 평가 수 · 비유한 수 · 경고 원문 · 중지 오류.
    아직 생기지 않은 값은 넣지 않는다 (0 · 성공값으로 채우지 않음)."""
    part = dict(acc.get("row") or {})
    count = acc.get("count")
    if count is not None:
        part.update(n_eval=count["n"], n_nonfinite=count["nonfinite"])
    caught = acc.get("caught")
    if caught is not None:
        part["warnings"] = sorted({f"{w.category.__name__}: {w.message}" for w in caught})[:20]
    part["stop_error"] = info
    return part


def _run_phase_a(task, ctx, notify, progress, acc) -> dict:
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, minimize
    _check_task(task, ctx)
    uf, region = ctx.get("util_file"), task["region"]
    t0, c0 = time.monotonic(), time.process_time()
    row = {k: task[k] for k in ("task_id", "run_id", "unit", "objective", "region", "row", "seed")}
    row.update(x0=[float(v) for v in task["x0"]], worker=task.get("worker"), t_start=t0)
    acc["row"] = row
    model_run = copy.deepcopy(ctx["models"][task["row"]])
    count = acc["count"] = {"n": 0, "nonfinite": 0}

    def fun(x):
        count["n"] += 1
        if progress is not None:
            progress(count["n"])
        v = _evaluate(task, ctx, x, model_run)[0]
        if not math.isfinite(v):
            count["nonfinite"] += 1
        return v
    opts = dict(ctx["options"])
    row["options_received"] = {k: repr(v) for k, v in sorted(opts.items())}
    lo, hi = region_bounds(region)
    cons = [LinearConstraint([[0.0, 0.0, 1.0, -1.0]], float(G_LB), np.inf)] if region in G_REGIONS else []
    res, err = None, None
    with warnings.catch_warnings(record=True) as caught:
        acc["caught"] = caught
        warnings.simplefilter("always")
        try:
            res = minimize(fun, np.asarray(row["x0"], dtype=float), method="COBYQA", bounds=Bounds(list(lo), list(hi)),
                           constraints=cons, options=opts)
        except BaseException as e:  # noqa: BLE001 — 분류해서 지역 / 구조로 나눈다
            info = classify(e, "optimize", uf)
            if info["kind"] == "structural":
                raise mon.Structural(info, partial=_partial(acc, info)) from None
            err = info
    msgs = sorted({f"{w.category.__name__}: {w.message}" for w in caught})
    row.update(n_eval=count["n"], n_nonfinite=count["nonfinite"], warnings=msgs[:20])
    if err is not None:                                         # 반환 없음 — 원 지역 오류만 적는다 (반환 필드 · termination 을 채우지 않음)
        row["error"] = err
    else:                                                       # 정상 반환 — 경고 중지보다 먼저 받은 반환 필드를 적는다 (C4-0B1-N1 잔여)
        row.update(x=[float(v) for v in res.x], fun=float(res.fun), status=int(res.status), message=str(res.message),
                   nfev=int(getattr(res, "nfev", -1)), nit=int(getattr(res, "nit", -1)), termination=termination(res), error=None)
    if any("Unknown solver options" in m for m in msgs):
        info = {"kind": "structural", "origin": "optimizer", "stage": "optimize", "type": "OptimizeWarning",
                "message": "알 수 없는 옵션 경고 — fail-closed (부속 A §3-1)", "traceback": msgs[:3]}
        raise mon.Structural(info, partial=_partial(acc, info))
    if err is not None:
        row.update(termination="solver_error", witness="invalid:SOLVER_ERROR", x=None, fun=None, status=None,
                   message=None, nfev=None, nit=None, value=None, components=None, reeval_error=None, residuals=None,
                   feasibility_class=None, active=None, n_out_PE=None, n_out_NE=None)
    else:
        x = row["x"]
        if row["termination"] == "unclassified":                # C4 v2 §5-4 · §6 — 재평가 · 증인으로 넘어가지 않고 전체 중지 (C4-0B1-N2)
            info = {"kind": "structural", "origin": "optimizer", "stage": "optimize", "type": "UnclassifiedTermination",
                    "message": f"미분류 termination — status {row['status']} · {row['message']} (C4 v2 §5-4 · §6: 전체 중지)"[:500],
                    "traceback": []}
            raise mon.Structural(info, partial=_partial(acc, info))
        notify("returned", {"run_id": row["run_id"], "x": x, "status": row["status"], "termination": row["termination"],
                            "n_eval": count["n"]})
        value, comp, rerr = None, None, None
        try:
            value, comp = _evaluate(task, ctx, np.asarray(x, dtype=float), copy.deepcopy(ctx["models"][task["row"]]))
        except BaseException as e:  # noqa: BLE001
            info = classify(e, "reeval", uf)
            if info["kind"] == "structural":
                raise mon.Structural(info, partial=_partial(acc, info)) from None
            rerr = info
        resid = exact_residuals(x, region)
        row.update(value=value, components=comp, reeval_error=rerr,
                   witness=witness(solver_error=False, value=value, residuals=resid, reeval_error=rerr is not None),
                   feasibility_class=feasibility_class(resid),
                   residuals=None if resid is None else {"box": frac_str(resid["box"]),
                                                         "box_by_coord": [frac_str(v) for v in resid["box_by_coord"]],
                                                         "g": None if resid["g"] is None else frac_str(resid["g"])},
                   active=None if resid is None else active_set(x, region))
        lab = {"n_out_PE": "미확인", "n_out_NE": "미확인"}
        if rerr is None and resid is not None:
            try:
                lab = c5.n_out_labels(ctx["util"], x, ctx["halfcell"], ctx["models"][task["row"]]["Q_exp_interp"])
            except BaseException as e:  # noqa: BLE001 — 라벨 실패는 '미확인' (증인 불변) · 구조 오류는 전역 중단
                info = classify(e, "label", uf)
                if info["kind"] == "structural":
                    raise mon.Structural(info, partial=_partial(acc, info)) from None
                lab = {"n_out_PE": "미확인", "n_out_NE": "미확인", "label_error": info}
        row.update(lab)
    t1 = time.monotonic()
    row.update(t_end=t1, wall=t1 - t0, cpu=time.process_time() - c0, state="COMPLETED")
    return row


def run_phase_a(task, ctx, notify=None, progress=None) -> dict:
    """Phase A 지역 실행 하나 — 감시 모듈 `supervise` 의 task_fn 계약. 최적화 → 독립 재평가 1 회 → 정확 잔차 · 분류 · 라벨.
    지역 오류는 행 (SOLVER_ERROR · REEVAL_ERROR · NONFINITE). 구조 목록 오류 · 미분류 termination · 옵션 경고 · 우리 코드의 예외는
    `mon.Structural` (행을 만들지 않는다 · partial = 그때까지의 행 · 계수 · 경고 · 중지 오류 — C4-0B1-N1)."""
    acc = {"row": {k: task.get(k) for k in ("task_id", "run_id", "unit", "objective", "region", "row", "seed")}}
    try:
        return _run_phase_a(task, ctx, notify or (lambda kind, payload: None), progress, acc)
    except mon.Structural:
        raise
    except BaseException as e:  # noqa: BLE001 — 우리 코드 · 설정의 예외 = 구조 오류
        info = classify(e, "ours", ctx.get("util_file"))
        raise mon.Structural(info, partial=_partial(acc, info)) from None


def phase_a_summary(rows, expected=2 * PHASE_A_N) -> dict:
    """A §2-4: Ĵ⁽⁰⁾ = 유효 증인의 재평가 최소 (같으면 실행 번호 순) · seed 묶음별 유효 최소 · 무효 이유별 수 · UNFIT = 유효 0."""
    valid = sorted((r for r in rows if r.get("witness") == "valid"), key=lambda r: (r["value"], r["run_id"]))
    inv = Counter(r["witness"].split(":", 1)[1] for r in rows if str(r.get("witness", "")).startswith("invalid:"))
    term = Counter(r.get("termination") for r in rows)
    per_seed = {}
    for s in PHASE_A_SEEDS:
        vs = [r["value"] for r in valid if r["seed"] == s]
        per_seed[str(s)] = min(vs) if vs else None
    best = valid[0] if valid else None
    return {"n_rows": len(rows), "expected": expected, "complete": len(rows) == expected, "n_valid": len(valid),
            "unfit": not valid, "J0": best["value"] if best else None, "x_hat": best["x"] if best else None,
            "argmin_run_id": best["run_id"] if best else None, "per_seed_min": per_seed,
            "invalid_by_reason": dict(sorted(inv.items())), "termination_counts": dict(sorted(term.items())),
            "ranked_run_ids": [r["run_id"] for r in valid]}


def rho_denominators(summaries, row):
    """결합 Phase A 의 분모 (Ĵ⁽⁰⁾_V, Ĵ⁽⁰⁾_D) — A0 의 J_V · J_D 단위가 둘 다 UNFIT 이 아니고 유한한 양수일 때만 (A §1-2 · §3-2)."""
    sv, sd = summaries.get(f"J_V|A0|{row}"), summaries.get(f"J_D|A0|{row}")
    if not sv or not sd or sv.get("unfit") or sd.get("unfit"):
        return None
    if not (_fin_pos(sv.get("J0")) and _fin_pos(sd.get("J0"))):
        return None
    return float(sv["J0"]), float(sd["J0"])


# ---------------------------------------------------------------- 문턱 · 판독 · 공통 갱신 (부속 A §1)
def _unfit(reason: str) -> dict:
    return {"status": "UNFIT", "reason": reason}


def thresholds(objective, region, *, J_hat, sigma_v, J_hat_V=None, J_hat_D=None) -> dict:
    """대응표 A §1-2: H2 T_V = Ĵ_V + 2σ̂_v · H3 (1 + δ) Ĵ (V · D) · 결합 1 + δ · H4 T_s = Ĵ_s + 2σ̂_v. 퇴화는 판정별 UNFIT."""
    out = {}
    sig_ok = _fin_pos(sigma_v)
    if objective == "J_V":
        if region not in REGIONS:
            raise ValueError(region)
        out["H2"] = (_unfit("σ̂_v 가 유한한 양수가 아님") if not sig_ok else _unfit("Ĵ_V 비유한") if not _fin(J_hat)
                     else {"status": "OK", "T": float(J_hat) + 2 * float(sigma_v)})
        if region == "A0":
            out["H3"] = ({"status": "OK", "T_by_delta": {d: (1 + float(d)) * float(J_hat) for d in DELTAS}} if _fin_pos(J_hat)
                         else _unfit("Ĵ_V 가 유한한 양수가 아님"))
    elif objective == "J_D":
        if region != "A0":
            raise ValueError(region)
        out["H3"] = ({"status": "OK", "T_by_delta": {d: (1 + float(d)) * float(J_hat) for d in DELTAS}} if _fin_pos(J_hat)
                     else _unfit("Ĵ_D 가 유한한 양수가 아님 (빈 마스크 · 비유한 포함)"))
    elif objective == "rho":
        if region != "A0":
            raise ValueError(region)
        out["H3"] = ({"status": "OK", "T_by_delta": {d: 1 + float(d) for d in DELTAS}} if _fin_pos(J_hat_V) and _fin_pos(J_hat_D)
                     else _unfit("Ĵ_V · Ĵ_D 중 하나라도 유한한 양수가 아님 — 결합 UNFIT"))
    elif objective == "J_Vs":
        if region not in ("A0", "A1"):
            raise ValueError(region)
        out["H4"] = (_unfit("σ̂_v 가 유한한 양수가 아님") if not sig_ok else _unfit("Ĵ_s 비유한") if not _fin(J_hat)
                     else {"status": "OK", "T": float(J_hat) + 2 * float(sigma_v)})
    else:
        raise ValueError(objective)
    return out


def reading(J, T) -> dict:
    """J ≤ T (같음은 충족) · |T − J| ≤ 1e-9 이면 경계 근접 라벨 (판정은 그대로) — A §2-2 마지막 행."""
    if not (_fin(J) and _fin(T)):
        return {"pass": False, "near_boundary": False}
    return {"pass": float(J) <= float(T), "near_boundary": abs(float(T) - float(J)) <= NEAR}


def common_update(records, pre=None) -> dict:
    """A §1-1: (셀 · 영역) 의 등록 탐색이 끝난 뒤 한 번 — 최종 Ĵ = 그 목적을 자기 탐색 목적으로 쓴 단위의 유효 기록 점의 최소.
    결합 단위의 점은 J_V · J_D 풀에 넣지 않고 `결합이 본 더 낮은 단일 목적값` 으로 따로 · 대조 점 제외 · ray 는 H4 만.
    ρ 판독은 저장된 (J_V, J_D) 를 최종 Ĵ 분모로 다시 나눈다. 갱신 뒤 Ĵ > 갱신 전 이면 HStop (Phase A 점이 풀에 없다는 뜻)."""
    final: dict = {}
    for r in records:
        if r.get("stage") in CONTROL_STAGES or not r.get("valid") or r["objective"] == "rho":
            continue
        if r["objective"] not in ("J_V", "J_D", "J_Vs"):
            raise HStop(f"모르는 목적 {r['objective']}")
        if r.get("stage") == "ray" and r["objective"] != "J_Vs":
            raise HStop("ray 점은 H4 (J_V^s) 풀에만")
        v = float(r["value"])
        if not math.isfinite(v):
            raise HStop(f"유효 기록 점의 값이 비유한: {r}")
        key = (r["objective"], r["region"], r["row"])
        final[key] = min(final.get(key, math.inf), v)
    for k, v0 in (pre or {}).items():
        if k in final and final[k] > v0:
            raise HStop(f"갱신 뒤 Ĵ {final[k]} > 갱신 전 Ĵ⁽⁰⁾ {v0} ({k}) — Phase A 점이 풀에 없다")
    combined_lower, rho_hat = [], {}
    for r in records:
        if r.get("objective") != "rho" or r.get("stage") in CONTROL_STAGES or not r.get("valid"):
            continue
        row, region, comp = r["row"], r["region"], r["components"]
        for o in ("J_V", "J_D"):
            m = final.get((o, region, row))
            if m is not None and comp[o] < m:
                combined_lower.append({"row": row, "region": region, "objective": o, "value": comp[o], "pool_min": m})
        jv_f, jd_f = final.get(("J_V", region, row)), final.get(("J_D", region, row))
        rf = rho(comp["J_V"], comp["J_D"], jv_f, jd_f) if (_fin_pos(jv_f) and _fin_pos(jd_f)) else None
        hat = rho_hat.setdefault(row, {"search": math.inf, "final": None})
        hat["search"] = min(hat["search"], float(r["value"]))
        if rf is not None:
            hat["final"] = rf if hat["final"] is None else min(hat["final"], rf)
    return {"final": final, "pre": dict(pre or {}), "combined_lower": combined_lower, "rho_hat": rho_hat}


# ---------------------------------------------------------------- 건조 (계획 · seed · 봉인만 읽음 — C4 v2 §4-5 · 승인 경계 C4-0B1-A1)
def dryrun(out, *, venv, seal, manifest_sha256, arrays_dir, h_arrays_dir, h_manifest_sha256, util_copy, p0_result,
           env_identity=None, n_workers=4) -> dict:
    """무자료 건조 = 계획 · seed · 봉인만 읽음 (C4 v2 §4-5 · 승인 경계 C4-0B1-A1) — identity · util 사본 (sha · AST · import 0) · Phase A 배열
    (C6 결속) · 0b1 배열 (바이트 대조 · 생성기 0 · 77 단위) · P0 게이트 → PLAN.json 하나. 최적화 · 목적 호출 · util import · Sobol 생성 0 ·
    자료 개봉 0. 합성 실행은 여기 넣지 않는다 (넣으려면 횟수 · 예산을 밝힌 별도 사전 승인)."""
    import numpy as np
    out = Path(out)
    e3a._guard([out, seal, arrays_dir, h_arrays_dir, util_copy, p0_result])
    if out.exists():
        raise HStop(f"{out} 가 이미 있다 — 덮어쓰지 않는다")
    t0 = time.monotonic()
    ident = e3a.identity(venv=venv, seal=seal, manifest_sha256=manifest_sha256, env_identity=env_identity)
    if not ident["ok"]:
        raise HStop(f"identity 실패: {ident['problems']}")
    ub = e3a._read(util_copy)
    if _sha(ub) != c5.UTIL_COPY_SHA:
        raise HStop(f"util 사본 sha256 {_sha(ub)} ≠ 기대 {c5.UTIL_COPY_SHA}")
    ust = p0.util_static_check(ub.decode("utf-8"))
    if not ust["ok"] or any(f not in ust["functions"] for f in ("objective_fun", "dVdQ_hc", "extract_battery_data")):
        raise HStop(f"util 사본 정적 검사 실패: {ust.get('bad')}")
    arr = e3a.check_arrays(arrays_dir, seal=seal, manifest_sha256=manifest_sha256)
    phase_a = load_phase_a_arrays(arrays_dir)
    hchk = check_h_arrays(h_arrays_dir, manifest_sha256=h_manifest_sha256, p0_result=p0_result, regenerate=False)
    if not hchk["complete"]:
        raise HStop(f"0b1 배열 봉인이 77 단위 전부가 아니다 ({hchk['units']})")
    p0b = e3a._read(p0_result)
    res = json.loads(p0b)
    ext = {e.get("row"): e for e in res.get("extraction", []) if e.get("kind") == "analysis"}
    if set(ext) != set(ROWS) or any(ext[r].get("status") != "OK" for r in ROWS):
        raise HStop("P0 분석 추출 기록이 #0–#10 전부 OK 가 아니다")
    sig = {s.get("row"): s for s in res.get("sigma_v", [])}
    gates = {str(r): endpoint_gate(ext[r]["V_first"], ext[r]["V_last"]) for r in ROWS}
    sig_state = {str(r): {"status": sig.get(r, {}).get("status"), "sigma_v_V": sig.get(r, {}).get("sigma_v_V"),
                          "finite_positive": sig.get(r, {}).get("status") == "OK" and _fin_pos(sig.get(r, {}).get("sigma_v_V"))}
                 for r in ROWS}
    us = units()
    wave1 = [u for u in us if u["objective"] != "rho"]
    wave2 = [u for u in us if u["objective"] == "rho"]
    t1 = phase_a_tasks(wave1, phase_a, n_workers)
    t2 = phase_a_tasks(wave2, phase_a, n_workers, start_id=len(t1))
    h4_gated = [u["unit"] for u in us if u["objective"] == "J_Vs" and not gates[str(u["row"])]["accepted"]]
    per_unit = []
    for u in us:
        ts = [t for t in (t1 if u["objective"] != "rho" else t2) if t["unit"] == u["unit"]]
        per_unit.append({"unit": u["unit"], "hypothesis": u["hypothesis"], "wave": 1 if u["objective"] != "rho" else 2,
                         "task_ids": [ts[0]["task_id"], ts[-1]["task_id"]], "arrays": [f"sobol_{REGION_ARRAY[u['region']]}_seed{s}.npy" for s in PHASE_A_SEEDS],
                         "p0_gate": ("H4 끝점 수용 아님 → 그 셀 H4 UNFIT · 실행하지 않음 (부속 A §4-3)" if u["unit"] in h4_gated else
                                     "ρ: A0 의 J_V · J_D Phase A 뒤 분모 Ĵ⁽⁰⁾ (UNFIT · 비양수면 결합 UNFIT)" if u["objective"] == "rho" else None)})
    plan = {
        "schema": "reil-c4-0b1-plan-v2",
        "scope": "무자료 건조 = 계획 · seed · 봉인만 읽음 (C4 v2 §4-5 · 승인 경계 C4-0B1-A1) — Phase A 계획 · P0 게이트 · 봉인 바이트 대조. "
                 "자료 개봉 0 · 실제 셀 맞춤 0",
        "execution": {"optimizer_calls": 0, "objective_calls": 0, "util_imported": False, "sobol_generated": 0},
        "phase_a": {"registered_runs": len(t1) + len(t2), "wave1_runs": len(t1), "wave2_rho_runs": len(t2), "per_unit": 2 * PHASE_A_N,
                    "n_units": len(us), "n_workers": n_workers, "options": {k: repr(v) for k, v in sorted(OPTIONS.items())},
                    "task_rule": "단위 순서 = units() (셀마다 J_V A0 · A1 · A2 · J_D A0 · ρ A0 · J_Vs A0 · A1) · 1 파 = ρ 밖 66 단위 · 2 파 = ρ 11 단위 · "
                                 "run_id 0–63 = seed 0 · 64–127 = seed 1 · worker = task_id % n",
                    "x0_float64_sha256": _sha(np.ascontiguousarray([t["x0"] for t in t1 + t2], dtype="<f8").tobytes()),
                    "h4_endpoint_gated_units": h4_gated, "runs_after_p0_gates": len(t1) + len(t2) - 2 * PHASE_A_N * len(h4_gated),
                    "units": per_unit},
        "gates": {"h4_endpoint": gates, "sigma_v": sig_state,
                  "jd_mask": "자료 쪽 — 셀의 dVdQ_exp_interp 를 보는 C4-A 에서 판정 (빈 마스크 → 그 셀 J_D · ρ UNFIT) · 여기서는 판정하지 않음"},
        "arrays": {"phase_a": {k: arr[k] for k in ("arrays_dir", "manifest_sha256", "c6_manifest_sha256", "c6_direct_match")}, "h": hchk},
        "identity": ident, "util_copy": str(util_copy), "util_copy_sha256": c5.UTIL_COPY_SHA,
        "p0_result": str(p0_result), "p0_result_sha256": _sha(p0b),
        "not_this_step": "C4-0b2 (Phase B · H4 대조 · ray · 표지) · C4-E / C4-A / C4-B (자료 실행) — 별도 확인 · 승인",
    }
    plan["elapsed_s"] = time.monotonic() - t0
    pb = c5.dump(plan)
    out.mkdir(exist_ok=False)
    (out / "PLAN.json").write_bytes(pb)
    if (out / "PLAN.json").read_bytes() != pb:
        raise HStop("다시 읽은 바이트가 쓴 것과 다르다")
    return {"ok": True, "out": str(out), "plan_sha256": _sha(pb), "registered_runs": len(t1) + len(t2),
            "h4_endpoint_gated_units": len(h4_gated), "execution": plan["execution"], "identity_ok": True,
            "elapsed_s": plan["elapsed_s"]}


# ---------------------------------------------------------------- CLI
def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="reil_c4_h", description="REIL C4-0b1 — 배열 · 규칙 봉인 · 건조 (기본 경로 없음)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("seal-arrays")
    s.add_argument("--out", required=True)
    s.add_argument("--p0-result", required=True)
    d = sub.add_parser("dryrun")
    for a in ("--venv", "--seal", "--seal-manifest-sha256", "--arrays", "--h-arrays", "--h-manifest-sha256", "--util-copy",
              "--p0-result", "--out"):
        d.add_argument(a, required=True)
    d.add_argument("--n-workers", type=int, default=4)
    a = ap.parse_args(argv)
    if a.cmd == "seal-arrays":
        rec = seal_h_arrays(Path(a.out), p0_result=Path(a.p0_result))
    else:
        rec = dryrun(Path(a.out), venv=a.venv, seal=Path(a.seal), manifest_sha256=a.seal_manifest_sha256, arrays_dir=Path(a.arrays),
                     h_arrays_dir=Path(a.h_arrays), h_manifest_sha256=a.h_manifest_sha256, util_copy=Path(a.util_copy),
                     p0_result=Path(a.p0_result), n_workers=a.n_workers)
    print(json.dumps(c5._jsonable(rec), ensure_ascii=False, sort_keys=True))
    return 0 if rec.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
