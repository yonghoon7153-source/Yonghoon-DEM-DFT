"""α·β 검증 하네스 — "이 답이 데이터로 정해지는가" 를 숫자로 묻는다.

물음 넷:

  A. **포팅 충실도** — 그들이 보고한 파라미터를 우리 목적함수에 넣으면
     최적점 근처인가. (아니면 이 하네스로 잰 것은 그들 모델이 아니다.)
  B. **경계** — 최적해가 상자 경계에 붙는가. 붙으면 그 좌표는 데이터가 아니라
     상자가 정한 것이다.
  C. **축퇴** — 최적 RMSE 의 (1+ε) 안에 드는 파라미터들이 만드는 LAM/LLI 의
     폭. 폭이 크면 "α·β 가 맞다" 를 말할 수 없다.
  D. **비결정성** — 원본은 목적함수의 scale 을 `rand` 50 개로 잡는데 seed 가
     없다. seed 를 바꾸면 목적함수 자체가 달라진다. 그 크기를 잰다.

실행:

    python -m bms_balancing.verify port --data-root … --state pristine
    python -m bms_balancing.verify degeneracy --data-root … --state 300_0009
    python -m bms_balancing.verify scale-noise --data-root … --state pristine
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import tempfile
import uuid
from pathlib import Path

import numpy as np
from scipy.optimize import NonlinearConstraint, minimize

from . import data as D
from .model import (LB5, UB5, Blend, HalfCell, Objective, average_duplicates,
                    degradation_modes)


def run_id_of(args) -> str:
    """이번 **시도**의 식별자 (Codex R4-06). `--run-id` → 환경 `BMS_RUN_ID`(run_states.sh 가 준다) → 새 uuid.
    산출물 행/JSON 에 박혀서 wrapper 가 "이번 시도가 게시한 bytes" 인지 확인한다 — 시각이 아니라 id 로."""
    rid = getattr(args, "run_id", None) or os.environ.get("BMS_RUN_ID")
    return rid or uuid.uuid4().hex


_PROV = None


def _provenance():
    """`scripts/provenance.py` 를 경로로 적재한다 (패키지가 아니다) — sha256·env 서명·git 상태의 정본은 거기 하나."""
    global _PROV
    if _PROV is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "bms_provenance", Path(__file__).resolve().parents[1] / "scripts" / "provenance.py")
        _PROV = importlib.util.module_from_spec(spec); spec.loader.exec_module(_PROV)
    return _PROV


from .schema import inputs_digest                       # noqa: E402  — producer·checker 의 한 정본 (Codex R9-03)
from . import schema as S                                # noqa: E402


def scale_audit_line(root, args, audit: dict, inputs_sha: str | None = None) -> str:
    r"""eval 의 `# scale_audit,…` 줄 (R5-09 식별자 · R5-06 eps_rel/equiv · U13 root). R6 내부 F1: root 라벨은 URL
    인코딩으로 공백을 살리고(사본 파서 `\S+`), 진짜 identity 는 `inputs=<소비 입력 digest>` 가 준다."""
    import urllib.parse
    root_label = urllib.parse.quote(Path(str(root)).name or str(root), safe="")
    head = (f"root={root_label} state={args.state} source={args.source} si={args.si_source} "
            f"seed={args.seed} n={next(iter(audit.values()))['n']}")
    if inputs_sha:
        head += f" inputs={inputs_sha}"
    return "# scale_audit," + head + "; " + "; ".join(
        f"{k}:n={v['n']}/finite={v['n_finite']}/inf={v['n_inf']}/nan={v['n_nan']}"
        f"/exc={v.get('n_exception', 0)}/eps_rel={v.get('eps_rel', float('nan')):.3g}"
        f"/equiv={int(bool(v.get('equivalent_within_rel', False)))}" for k, v in audit.items())


class publish_lock:
    """`<산출>.lock` 의 flock (R5-04). 산출 게시와 meta 게시가 **같은 잠금** 안에서 일어나야 두 시도가 섞인
    묶음(CSV 는 B, meta 는 A)이 남지 않는다. run_states.sh 의 `flock`·write_meta 도 같은 파일을 잡는다."""
    def __init__(self, path):
        self.lock_path = str(path) + ".lock"
        self.fh = None
    def __enter__(self):
        import fcntl
        self.fh = open(self.lock_path, "a+")
        fcntl.flock(self.fh, fcntl.LOCK_EX)
        return self
    def __exit__(self, *exc):
        import fcntl
        fcntl.flock(self.fh, fcntl.LOCK_UN); self.fh.close()


def atomic_write_csv(path, rows, fieldnames):
    """시도별 **고유** 임시 파일에 쓰고 잠금 안에서 한 번에 옮긴다 (R4-06: 공유 `.part` 는 두 시도가 서로의
    행을 게시했다; R5-04: 게시는 `<산출>.lock` 안에서 — meta 작성자가 같은 잠금 안에서 id 를 다시 확인한다)."""
    import csv
    out = Path(path)
    fh = tempfile.NamedTemporaryFile("w", dir=out.parent, prefix=out.name + ".", suffix=".part",
                                     delete=False, newline="", encoding="utf-8")
    try:
        with fh:
            # ⚠ U14-01: `csv` 기본 lineterminator 는 **CRLF** 다. git 은 `.gitattributes` 로 LF 로 정규화해
            #   저장하므로 디스크 bytes 와 커밋 bytes 가 갈리고, meta 의 sha256 이 fresh clone 에서 안 맞아
            #   `verify_unit` 이 False → F07 수정이 그 상태를 표에서 뺀다. 서명이 사는 유일한 길은 둘을 같게.
            w_ = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
            w_.writeheader(); w_.writerows(rows)
    except BaseException:
        Path(fh.name).unlink(missing_ok=True)
        raise
    _publish_or_keep(fh.name, out)


def atomic_write_json(path, obj):
    """`atomic_write_csv` 의 JSON 판 (R6 내부 F01): degeneracy 는 전 판에 stdout 리다이렉트로 고정 이름 `.part` 에
    쓰고 shell 이 `flock mv` 했다 — producer 의 stdout fd 가 rename 을 넘어 살아남아, 빠른 다른 시도가 게시·meta·
    검사를 전부 끝낸 뒤 느린 시도가 그 inode 에 잠금 밖에서 썼다 (JSON=B, meta=A). 게시는 여기서, 잠금 안에서."""
    import json
    out = Path(path)
    fh = tempfile.NamedTemporaryFile("w", dir=out.parent, prefix=out.name + ".", suffix=".part",
                                     delete=False, encoding="utf-8")
    try:
        with fh:
            # ⚠ Codex R11 P1-8: 기본 `json` 은 `NaN`/`Infinity` 를 그대로 쓴다 — 표준 JSON 이 아니고 소비자는
            #   조용히 받는다. 유한하지 않은 값은 애초에 산출이 될 수 없다 (`ValueError` 로 여기서 멈춘다).
            fh.write(json.dumps(obj, ensure_ascii=False, indent=2, default=float, allow_nan=False) + "\n")
    except BaseException:
        Path(fh.name).unlink(missing_ok=True)
        raise
    _publish_or_keep(fh.name, out)


def _publish_or_keep(tmp_name, out):
    """잠금 안 교체. 잠금 자체가 실패하면(ENOLCK 등 — flock 없는 파일시스템) 계산 결과 `.part` 는 **지우지 않고**
    예외에 그 경로를 적는다 (R6 내부 F10: 전 판은 행 전부를 버렸다)."""
    try:
        with publish_lock(out):
            os.replace(tmp_name, out)
    except OSError as e:
        raise OSError(e.errno, f"{e.strerror}: 게시 잠금 실패 — 계산 결과는 {Path(tmp_name).name} 에 남아 있다 "
                               f"({tmp_name}); flock 을 지원하는 파일시스템에서 손으로 게시할 것") from e


class SharedSnapshot:
    """한 명령이 공유하는 입력의 **immutable snapshot** — full-cell workbook + 문헌 gr/si (조건 8 축 ①).

    왜 필요한가 (R12 §5 답변 3): 전에는 기준(pristine)과 대상이 **같은 workbook 을 각자 읽었다.** 그 사이에
    재-export 가 있으면 두 행이 다른 bytes 로 계산되는데 우리는 그것을 나중에 **적기만** 했다
    (`shared_full_cell_mismatch_accepted: true`). 적는 것과 막는 것은 다르다.

    리뷰어가 자리까지 제안했다 (R6_LEDGER "열어 둔 것"): **command/build 경계에서 한 번 읽은 typed
    snapshot 을 양쪽에 전달.** 여기가 그것이다 — 한 번 읽고, 받은 쪽은 다시 읽지 않는다.

    ⚠ **읽기는 지연한다** (처음 쓸 때 읽고 그 뒤로는 그 bytes 다). 명령 시작에서 미리 읽으면 입력이 없는
      경우의 실패 시점이 앞당겨져, `build` 가 내던 친절한 진단("이 소스에 있는 상태는 …")보다 먼저
      죽는다 — 2026-09-16 실측으로 11 건이 그렇게 깨졌다. 지연해도 "한 명령 안에서 한 번" 은 그대로다.
    """

    def __init__(self, root: Path, si_source: str):
        self.root = Path(root)
        self.si_source = si_source
        self._full_cell = None
        self._lit_id: dict | None = None
        self._lit = None

    @property
    def full_cell(self):
        if self._full_cell is None:
            self._full_cell = D.read_input(D.full_cell_workbook(self.root))
        return self._full_cell

    def _literature_once(self):
        if self._lit is None:
            self._lit_id = {}
            self._lit = D.load_literature(self.root, self.si_source, identity=self._lit_id)
        return self._lit, self._lit_id

    def identity(self) -> dict:
        _, lit_id = self._literature_once()
        return {"full_cell": dict(self.full_cell.identity()), "literature": json.loads(json.dumps(lit_id))}

    def literature(self, si_source: str):
        """이 snapshot 이 읽은 **그 소스**의 문헌. 다른 소스를 물으면 멈춘다 — 조용히 틀린 영수증을 만들지 않는다."""
        if si_source != self.si_source:
            raise ValueError(f"이 snapshot 은 si_source={self.si_source!r} 로 읽었다 — {si_source!r} 로 쓸 수 없다 "
                             f"(receipt 는 새 소스를 적는데 bytes 는 옛 소스가 된다)")
        lit, lit_id = self._literature_once()
        return lit, dict(lit_id)

    def full_cell_columns(self, state: str):
        ident: dict = {}
        c, v = D.load_full_cell_from(self.full_cell, state, identity=ident)
        return c, v, ident


def shared_snapshot(root: Path, si_source: str) -> SharedSnapshot:
    """명령 경계에서 **한 번** 부른다 — 그 뒤 모든 `build` 에 같은 것을 넘긴다 (조건 8 축 ①)."""
    return SharedSnapshot(root, si_source)


def build(root: Path, source: str, state: str, si_source: str,
          w_dqdv: float = 0.0, use_peak_weight: bool = True,
          scale_seed: int = 0, shared: "SharedSnapshot | None" = None) -> Objective:
    # ⚠ 입력이 없으면 **적합을 시작하기 전에** 죽는다. 2026-09-10 실측:
    #   `degeneracy --state 300_0147 --source GITT` 가 기준(pristine) 적합
    #   24 회를 다 돌린 **뒤에** 대상 파일이 없다는 걸 알았다 (23 초 낭비, 그리고
    #   로그 첫 줄이 성공한 multistart 라 실패 원인이 가려졌다).
    hc = D.half_cell_path(root, source, state)
    if not hc.is_file():
        have = sorted(s2 for s2 in D.STATES
                      if D.half_cell_path(root, source, s2).is_file())
        other = [src for src in D.HALF_FILE if src != source
                 and D.half_cell_path(root, src, state).is_file()]
        raise SystemExit(
            f"반쪽전지 파일이 없다: {hc}\n"
            f"  `{source}` 에 있는 상태: {', '.join(have) or '(없음)'}\n"
            + (f"  `{state}` 는 `--source {other[0]}` 에는 있다.\n" if other else "")
            + "  (상태마다 반쪽전지를 따로 재는 파이프라인이라 없는 상태는 못 돈다)")
    # ⚠ Codex R6-03: 입력은 **한 번 읽은 bytes** 로 파싱하고 그 bytes 를 해시한다. 전 판은 로더가 경로로 읽은 뒤
    #   경로를 다시 열어 해시했다 — 그 사이 같은 이름으로 재-export 된 B 가 있으면 A 로 계산하고 B 의 서명을 적었다.
    hb = D.read_input(hc)
    half = HalfCell(hb.stream(), window=11, poly_order=3)
    # ⚠ R16 (조건 8 축 ①): `shared` 를 받으면 **다시 읽지 않는다** — 한 명령 안의 모든 행이 같은 bytes 를
    #   본다. 안 받으면 전처럼 각자 읽는다 (단일 build 를 부르는 소비자·시험용). 명령은 항상 넘긴다.
    if shared is not None:
        (si_c, si_v, gr_c, gr_v), lit_id = shared.literature(si_source)
        c, v, fc_id = shared.full_cell_columns(state)
    else:
        lit_id = {}
        si_c, si_v, gr_c, gr_v = D.load_literature(root, si_source, identity=lit_id)
        fc_id = {}
        c, v = D.load_full_cell(root, state, workbook=D.full_cell_workbook(root), identity=fc_id)
    blend = Blend(si_c, si_v, gr_c, gr_v, window=11, poly_order=3)
    obj = Objective(half, blend, c, v, window=11, poly_order=3,
                    w_pocv=1.0, w_dvdq=1.0, w_dqdv=w_dqdv,
                    use_peak_weight=use_peak_weight, scale_seed=scale_seed)
    # ⚠ R6 내부 F4: 풀셀 워크북은 폴더의 이름순 첫 xlsx 라 사본 하나로 조용히 바뀌는데 이름·sha256 이 어디에도
    #   없었다 (R5-05 는 ne_shape 만). 소비한 입력 셋의 identity 를 Objective 가 들고 다니고 산출마다 적는다.
    # ⚠ Codex R7-02: 잡음 진단은 **원시** capacity/voltage 가 필요한데 (Objective 는 평균·정규화한다) 전 판은
    #   경로를 다시 열어 다시 읽었다 — 그 사이 정상 재-export 가 있으면 분자는 A 의 부적합, 분모는 B 의 σ 가 된다.
    #   같은 snapshot 의 원시 배열을 여기서 들려 보낸다.
    obj.full_cell_raw = (c, v)
    obj.consumed_inputs = {"half_cell": hb.identity(), "full_cell": fc_id, "literature": lit_id}
    obj.inputs_sha = inputs_digest(obj.consumed_inputs)
    return obj


def resolve_box(lb=None, ub=None):
    """상자를 **한 자리에서** 정하고 검사한다 (기본은 원본 `LB5`/`UB5`).

    ⚠ W-01~W-05 (2026-09-14): 폭을 재는 세 함수(`active_bounds`·`near_optimal_extrema`·
      `mode_profile_extrema`)가 상자를 모듈 상수로 **하드코딩**하고 있었다. `fit_cycles` 는 이미
      `--gamma-lb` 로 상자를 바꾸므로(`multistart` 만 `lb`/`ub` 를 받았다), 그대로 폭을 붙이면
      **적합은 좁은 상자에서 하고 폭은 넓은 상자에서 재는** 산출이 나온다. 규칙을 한 함수로 모은다 —
      R14 P2-2 에서 "존재·비공백" 규칙이 두 벌이라 절반만 구현됐던 것과 같은 교훈이다.

    검사는 fail-closed 다. 폭은 인용되는 숫자라, 뒤집힌 상자로 조용히 이상한 폭을 내는 것보다
    거절하는 편이 낫다.
    """
    lo = np.asarray(LB5 if lb is None else lb, dtype=float)
    hi = np.asarray(UB5 if ub is None else ub, dtype=float)
    if lo.shape != (5,) or hi.shape != (5,):
        raise ValueError(f"상자는 5-파라미터여야 한다 — lb {tuple(lo.shape)} · ub {tuple(hi.shape)}")
    if not np.all(np.isfinite(lo)) or not np.all(np.isfinite(hi)):
        raise ValueError(f"상자에 비유한 값이 있다 — lb {lo.tolist()} · ub {hi.tolist()}")
    bad = [i for i in range(5) if lo[i] > hi[i]]
    if bad:
        names = ["a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si"]
        raise ValueError("lb > ub 인 축: " + ", ".join(
            f"{names[i]} [{lo[i]}, {hi[i]}]" for i in bad))
    return lo, hi


def multistart(obj: Objective, n_starts: int = 24, seed: int = 0,
               x0: np.ndarray | None = None, require_success: bool = True,
               lb=None, ub=None):
    """fmincon+MultiStart 대응 — L-BFGS-B 다중 시작.

    ⚠ 2026-09-10 리뷰 [A3]: 전 판은 `OptimizeResult.success` 를 보지 않아
      **비정상 종료한 결과를 성공한 fit 으로 채택**했다. 합성 반례에서
      success=False 결과가 그대로 best 와 all_sols 에 들어갔다. 이제
      기본으로 거른다. 거른 개수는 `multistart.last_stats` 와 stderr 에 남긴다
      — 조용히 버리면 그것대로 감사가 안 된다.
    """
    # ⚠ 경계는 인자로 받는다 (기본은 원본 lb5/ub5). pyDMA Track C 대조처럼 γ 하한을 0.02 로 올리는 실행이 있고,
    #   그때 **무작위 시작점도 같은 경계 안**에서 뽑혀야 한다 — 모듈 상수를 읽으면 시작점만 옛 경계를 쓴다.
    lo, hi = resolve_box(lb, ub)
    rng = np.random.default_rng(seed)
    starts = [np.asarray(x0, dtype=float)] if x0 is not None else []
    starts += list(lo + rng.random((n_starts, 5)) * (hi - lo))
    best, best_val = None, np.inf
    all_sols = []
    stats = {"tried": 0, "raised": 0, "not_success": 0, "nonfinite": 0, "accepted": 0}
    bounds = list(zip(lo, hi))
    for s in starts:
        stats["tried"] += 1
        try:
            r = minimize(obj, s, method="L-BFGS-B", bounds=bounds,
                         options={"maxiter": 500, "ftol": 1e-12, "gtol": 1e-10})
        except Exception:                               # noqa: BLE001
            stats["raised"] += 1
            continue
        if not np.isfinite(r.fun):
            stats["nonfinite"] += 1
            continue
        if require_success and not bool(getattr(r, "success", True)):
            stats["not_success"] += 1
            continue
        stats["accepted"] += 1
        all_sols.append((float(r.fun), r.x.copy()))
        if r.fun < best_val:
            best, best_val = r.x.copy(), float(r.fun)
    multistart.last_stats = stats
    if stats["not_success"] or stats["raised"] or stats["nonfinite"]:
        print(f"[multistart] 시작점 {stats['tried']}개 중 채택 {stats['accepted']} — "
              f"비정상종료 {stats['not_success']} · 예외 {stats['raised']} · "
              f"비유한 {stats['nonfinite']}", file=sys.stderr)
    return best, best_val, all_sols


multistart.last_stats = {}


def active_bounds(p, tol=1e-6, lb=None, ub=None):
    """해가 **실제로 쓴 상자**의 경계에 붙었는가 (기본 상자는 `LB5`/`UB5`).

    ⚠ W-01: 상자를 안 받던 판은 `--gamma-lb 0.02` 로 돌린 적합이 γ=0.0200 에 정확히 붙어도 `[]` 를 냈다.
      "경계에 붙은 값" 을 세는 것은 이 프로젝트가 규진팀 97 행에서 32 행을 잡아낸 바로 그 검사다
      (`BML_R1_RESPONSE` §2). 우리 산출에서 그걸 못 세면 같은 종류의 사실을 숨기는 셈이다.
    """
    lo, hi = resolve_box(lb, ub)
    names = ["a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si"]
    hits = []
    for i, n in enumerate(names):
        if abs(p[i] - lo[i]) < tol:
            hits.append(f"{n}=lb")
        if abs(p[i] - hi[i]) < tol:
            hits.append(f"{n}=ub")
    return hits


# ── A. 포팅 충실도 ──────────────────────────────────────────────────────

#: 그들이 보고한 값 (exp10_si_source_sensitivity.csv, 반쪽전지=GITT)
REPORTED = {
    ("Li", "pristine"): [1.077218, -0.022949, 1.001342, 0.000309, 0.295099],
    ("Li", "300_0009"): [1.181472, -0.141171, 1.080759, None, 0.239466],
    ("Kunz", "pristine"): [1.097789, -0.038349, 1.058563, -0.013455, 0.260566],
    ("Kunz", "300_0009"): [1.190057, -0.147223, 1.162316, -0.014875, 0.186959],
}


def cmd_port(args):
    root = D.data_root(args.data_root)
    obj = build(root, args.source, args.state, args.si_source,
                w_dqdv=args.w_dqdv, scale_seed=args.seed)
    out = {"state": args.state, "si_source": args.si_source,
           "half_cell": args.source, "c_cell": obj.c_cell,
           "scales": obj.scales,
           "raw_len_mismatch": obj.half.raw_len_mismatch,
           "pe_direction": obj.half.pe_direction,
           "ne_direction": obj.half.ne_direction,
           "dv_window_quantile_15_85": obj.dv_window,
           "dq_window_quantile_05_95": obj.dq_window}

    rep = REPORTED.get((args.si_source, args.state))
    if rep and all(x is not None for x in rep):
        p = np.array(rep, dtype=float)
        out["reported_p"] = rep
        out["reported_rmse_pocv"] = obj.rmse_pocv(p)
        out["reported_rmse_dvdq"] = obj.rmse_dvdq(p)
        out["reported_obj"] = obj(p)

    # ⚠ 2026-09-10 리뷰 [A2]: 전 판은 보고값을 **항상** 첫 시작점으로 넣고
    #   그 결과를 "독립 재적합" 이라고 불렀다. 그건 독립이 아니다.
    #   `--blind` 는 보고값을 시작점에서 빼고 무작위 시작만으로 다시 찾는다.
    seed_x0 = None
    if rep and all(x is not None for x in rep) and not args.blind:
        seed_x0 = np.array(rep, dtype=float)
    out["blind"] = bool(args.blind)
    out["reported_used_as_start"] = seed_x0 is not None
    best, val, _ = multistart(obj, n_starts=args.starts, seed=args.seed, x0=seed_x0)
    out["multistart_stats"] = dict(multistart.last_stats)
    out["our_p"] = [float(x) for x in best]
    out["our_obj"] = val
    # 산문 대신 **실제 차이**를 적는다 (리뷰 [A2]: 자릿수 주장이 사실과 달랐다)
    if rep and all(x is not None for x in rep):
        d = np.abs(np.array(rep, dtype=float) - np.asarray(best, float))
        out["abs_diff_vs_reported"] = [float(x) for x in d]
        out["max_abs_diff_vs_reported"] = float(d.max())
        out["obj_abs_diff_vs_reported"] = float(abs(out.get("reported_obj", np.nan) - val))
    out["our_rmse_pocv"] = obj.rmse_pocv(best)
    out["our_rmse_dvdq"] = obj.rmse_dvdq(best)
    out["active_bounds"] = active_bounds(best)
    # 반쪽전지 곡선의 어느 구간을 실제로 쓰는가 (0~1 밖이면 외삽이다)
    for tag, a, b in (("PE", best[0], best[1]), ("NE", best[2], best[3])):
        lo, hi = (0 - b) / a, (1 - b) / a
        out[f"{tag}_argument_range"] = [float(lo), float(hi)]
        out[f"{tag}_extrapolated"] = bool(lo < 0 or hi > 1)
    print(json.dumps(out, ensure_ascii=False, indent=2, default=float))


# ── C. 축퇴 ────────────────────────────────────────────────────────────

def near_optimal_extrema(obj: Objective, ref_p, ref_c, c_cell, best, best_val,
                         tol: float, seeds: list, n_starts: int = 8, seed: int = 0,
                         lb=None, ub=None):
    """근최적 집합 {p : obj(p) ≤ best_obj·(1+tol)} 위에서 각 mode 의 min·max.

    ⚠ 2026-09-10 리뷰 [B1]: 전 판은 최적점 둘레에 등방 Gaussian 400점을 뿌리고
      **관측된** min·max 를 '폭' 이라고 불렀다. 그건 폭이 아니라 표집 하한이다.
      정확히 평평한 굽은 ridge(참 폭 40 %p)를 넣은 반례에서 그 방식은 0 %p 를
      보고했다 — 식별성이 아니라 표집 실패를 식별성으로 보고한 것이다.
      더 결정적으로, **우리가 커밋한 γ 프로파일 자신**이 같은 설정에서 1 % 안
      두 점만으로 1.59 %p 를 보인다 (문서의 0.87 %p 보다 넓다).

    그래서 무작위 대신 제약 최적화로 각 방향의 극값을 직접 민다:
        maximize / minimize  mode(p)   s.t.  obj(p) ≤ best_val·(1+tol),  lb ≤ p ≤ ub

    이것도 전역 보장은 아니다 (SLSQP 는 국소 해법이다). 여러 시작점에서 밀어
    가장 넓은 것을 취하므로 **여전히 하한**이지만, 등방 구름보다 훨씬 조인다.
    반환값에 `is_lower_bound: True` 를 같이 실어 그 사실을 지운 채 인용하지
    못하게 한다.
    """
    # ⚠ Codex R17 P2-01: 전 판은 tol·best_val 을 검사하지 않았고, 허용집합이 비면 `best` 를 조용히 넣어
    #   `measured / 폭 0` 을 냈다 — 읽는 쪽은 그것을 "완벽히 식별됐다" 로 읽는다. 폭이 **뜻을 갖는 전제**를 먼저 본다:
    #   tol 은 유한한 비음수, best_val 은 유한, best 는 상자 안. 어긋나면 값을 지어내지 않고 예외다 —
    #   `cycles._width_fields` 가 이것을 받아 `failed` 로 적는다 (안 잼/실패/빈 집합은 0 이 아니다).
    tol = float(tol)
    if not (np.isfinite(tol) and tol >= 0.0):
        raise ValueError(f"폭 허용 tol 은 유한한 비음수여야 한다 — {tol!r} 이면 근최적 집합이 정의되지 않는다 (R17 P2-01)")
    if not np.isfinite(float(best_val)):
        raise ValueError(f"best_val 이 유한하지 않다 ({best_val!r}) — 근최적 집합의 기준값이 없다 (R17 P2-01)")
    limit = best_val * (1.0 + tol)
    lo, hi = resolve_box(lb, ub)                     # ⚠ W-02: 상자는 인자다 (적합이 쓴 그것과 같아야 한다)
    _b = np.asarray(best, float)
    if _b.shape != lo.shape or np.any(_b < lo - 1e-12) or np.any(_b > hi + 1e-12):
        raise ValueError(f"best 가 상자 밖이다 (best {_b.tolist()}, lb {lo.tolist()}, ub {hi.tolist()}) — "
                         f"적합이 쓴 상자와 폭의 상자가 다르다 (R17 P2-01 · W-02)")
    bounds = list(zip(lo, hi))
    rng = np.random.default_rng(seed + 7)
    # 시작점은 **상자 전체**에 뿌린다. 최적점 둘레에만 뿌리면 멀리 뻗은
    # 골짜기 끝을 못 민다 — 그게 전 판이 0 %p 를 보고한 이유다.
    starts = [np.asarray(best, float)]
    starts += [np.asarray(x, float) for x in seeds[:n_starts]]
    for i in range(5):                               # 각 축의 양 끝에서 한 번씩
        for frac in (0.02, 0.98):
            q = np.asarray(best, float).copy()
            q[i] = lo[i] + frac * (hi[i] - lo[i])
            starts.append(q)
    starts += list(lo + rng.random((n_starts, 5)) * (hi - lo))

    def mode_of(p, key):
        return degradation_modes(ref_p, ref_c, np.asarray(p, float), c_cell)[key]

    con = NonlinearConstraint(lambda p: limit - obj(np.asarray(p, float)), 0.0, np.inf)

    # ── 1단계: 실현가능성 복원 ──
    #   시작점이 제약 밖이면 SLSQP 가 목적 개선과 복원을 동시에 하다 실패한다
    #   (합성 ridge 에서 min 방향 시도가 **전부** 버려졌다). 그래서 먼저
    #   obj 를 낮춰 근최적 집합 안으로 들여보낸 뒤 극값을 민다. 복원된 점
    #   자체도 집합의 원소이므로 후보에 같이 넣는다.
    feasible = []
    for s0 in starts:
        q = np.asarray(s0, float)
        if obj(q) > limit:
            try:
                r0 = minimize(obj, q, method="L-BFGS-B", bounds=bounds,
                              options={"maxiter": 300, "ftol": 1e-14})
                if np.isfinite(r0.fun):
                    q = np.asarray(r0.x, float)
            except Exception:                        # noqa: BLE001
                continue
        if obj(q) <= limit * (1 + 1e-9):
            feasible.append(q)
    if not feasible:
        # ⚠ R17 P2-01: 전 판은 여기서 `best` 를 복구값으로 넣었다. 유효 witness 가 하나도 없으면 폭은 **없는 것**이지
        #   0 이 아니다 — 결과를 내지 않고 실패한다 (`best` 자체가 제약을 못 지키면 `best_val` 이 그 점의 목적값이
        #   아니라는 뜻이고, 그것은 호출자의 버그다).
        raise RuntimeError(f"근최적 집합 {{J ≤ {limit:.6g}}} 안에 유효한 점이 하나도 없다 — obj(best)={obj(_b):.6g}. "
                           f"폭을 0 으로 적지 않는다 (R17 P2-01)")

    out = {}
    for key in ("LAM_PE", "LAM_NE", "LLI"):
        vals = [mode_of(best, key)] + [mode_of(q, key) for q in feasible]
        for sign in (+1.0, -1.0):                    # +1: 최대화, -1: 최소화
            for s0 in feasible:
                try:
                    r = minimize(lambda p: -sign * mode_of(p, key), s0,
                                 method="SLSQP", bounds=bounds, constraints=[con],
                                 options={"maxiter": 200, "ftol": 1e-12})
                except Exception:                    # noqa: BLE001
                    continue
                if not np.isfinite(r.fun):
                    continue
                # 제약을 실제로 지키는지 직접 확인한다 (SLSQP 는 살짝 넘길 수 있다)
                if obj(np.asarray(r.x, float)) <= limit * (1 + 1e-9):
                    vals.append(mode_of(r.x, key))
        v = np.array(vals, dtype=float) * 100.0
        out[key] = {"min": float(v.min()), "max": float(v.max()),
                    "span": float(v.max() - v.min()), "n_points": int(v.size),
                    "is_lower_bound": True}
    return out


def mode_profile_extrema(obj: Objective, ref_p, ref_c, c_cell, best, best_val,
                         tol: float, n_grid: int = 21, n_starts: int = 3,
                         seed: int = 0, hint: dict | None = None,
                         lb=None, ub=None):
    """각 mode 값 v 가 근최적 집합 안에서 **도달 가능한가**를 직접 묻는다.

        for v in grid:   min_p obj(p)  s.t.  mode(p) = v,  lb ≤ p ≤ ub
        v 가 도달 가능 ⟺ 그 최소값 ≤ best_obj·(1+tol)

    왜 이쪽이 옳은가 (리뷰 B1 의 ridge 반례가 가르쳐 준 것):
      제약을 `obj(p) ≤ limit` 로 걸고 mode 를 최적화하면, 정확히 평평한
      골짜기 위에서 **제약의 기울기가 0 이 된다** (g = limit − 1 − (Δ/ε)²,
      Δ=0 에서 ∇g=0). LICQ 가 깨져서 SLSQP 가 골짜기를 따라 못 미끄러진다.
      실측: 참 폭 40 %p 인 ridge 에서 19.9 %p 만 나왔다.
      반대로 mode 를 **등식 제약**으로 묶고 obj 를 최소화하면 mode 제약은
      a 에 대해 선형이라 조건수가 좋고, obj 는 골짜기로 곧장 내려간다.

    반환값은 여전히 **하한**이다 (국소 해법 + 격자). `is_lower_bound` 를 같이
    실어 그 사실을 지운 채 인용하지 못하게 한다.
    """
    limit = best_val * (1.0 + tol)
    lo, hi = resolve_box(lb, ub)                     # ⚠ W-03: bounds 와 **격자를 까는 box** 둘 다 이 상자다
    bounds = list(zip(lo, hi))
    rng = np.random.default_rng(seed + 11)
    box = lo + rng.random((256, 5)) * (hi - lo)

    def mode_of(p, key):
        return degradation_modes(ref_p, ref_c, np.asarray(p, float), c_cell)[key]

    out = {}
    for key in ("LAM_PE", "LAM_NE", "LLI"):
        vals_box = np.array([mode_of(q, key) for q in box])
        v_lo, v_hi = float(vals_box.min()), float(vals_box.max())
        v_best = mode_of(best, key)

        # ⚠ 2026-09-10 실측: 상자 전체에 격자를 깔면 근최적 집합 근처가 성기다.
        #   LLI 는 22 개 중 **1 개**, LAM_PE 는 2 개만 도달 가능했다 — 방법이
        #   실패한 게 아니라 격자가 엉뚱한 데 깔린 것이다. 제약 최적화가 이미
        #   찾아 놓은 범위를 힌트로 받아 그 둘레(폭의 ±50 %)에 격자를 모은다.
        #   힌트 밖으로도 밀 수 있게 넓혀서 깔아야 하한이 더 조여진다.
        if hint and key in hint:
            h_lo, h_hi = hint[key]
            h_lo, h_hi = h_lo / 100.0, h_hi / 100.0        # % → 분수
            pad = max((h_hi - h_lo) * 0.5, 1e-4)
            g_lo = max(v_lo, h_lo - pad)
            g_hi = min(v_hi, h_hi + pad)
            if g_hi <= g_lo:
                g_lo, g_hi = v_lo, v_hi
        else:
            g_lo, g_hi = v_lo, v_hi
        grid = np.unique(np.concatenate([np.linspace(g_lo, g_hi, n_grid), [v_best]]))
        starts = [np.asarray(best, float)]
        starts += list(lo + rng.random((n_starts, 5)) * (hi - lo))

        attainable = []
        for v in grid:
            con = {"type": "eq", "fun": (lambda p, _v=v, _k=key: mode_of(p, _k) - _v)}
            hit = np.inf
            for s0 in starts:
                try:
                    r = minimize(obj, s0, method="SLSQP", bounds=bounds,
                                 constraints=[con],
                                 options={"maxiter": 200, "ftol": 1e-12})
                except Exception:                    # noqa: BLE001
                    continue
                if not np.isfinite(r.fun):
                    continue
                q = np.asarray(r.x, float)
                # 등식 제약을 실제로 지켰는지 확인 — SLSQP 는 살짝 어긴다
                if abs(mode_of(q, key) - v) > 1e-6 * max(1.0, abs(v)):
                    continue
                hit = min(hit, float(obj(q)))
            if hit <= limit * (1 + 1e-9):
                attainable.append(v)

        if not attainable:
            attainable = [v_best]
        a = np.array(attainable, dtype=float) * 100.0
        out[key] = {"min": float(a.min()), "max": float(a.max()),
                    "span": float(a.max() - a.min()),
                    # ⚠ Codex R2-05: 외곽 [min,max] 만으로는 가능집합이 비연결인지 모른다.
                    #   도달한 격자점을 그대로 남겨 "공유 가능값" 을 나중에 물을 수 있게.
                    "attainable_pct": [float(x) for x in a],
                    "grid_pct": [float(x) * 100.0 for x in grid],
                    "n_grid_attainable": int(a.size), "n_grid": int(grid.size),
                    "grid_range_pct": [g_lo * 100.0, g_hi * 100.0],
                    "grid_from_hint": bool(hint and key in hint),
                    "is_lower_bound": True}
    return out


def cmd_degeneracy(args):
    root = D.data_root(args.data_root)
    # ⚠ R16 (조건 8 축 ①): 공유 입력(full-cell workbook · 문헌)을 **명령 경계에서 한 번** 읽어
    #   아래로 넘긴다 — 기준과 대상이 각자 읽으면 그 사이의 재-export 가 두 행을 갈라놓는다.
    shared = shared_snapshot(root, args.si_source)
    ref_obj = build(root, args.source, "pristine", args.si_source, shared=shared,
                    w_dqdv=args.w_dqdv, scale_seed=args.seed)
    ref_best, _, _ = multistart(ref_obj, n_starts=args.starts, seed=args.seed)

    obj = build(root, args.source, args.state, args.si_source, shared=shared,
                w_dqdv=args.w_dqdv, scale_seed=args.seed)
    best, best_val, sols = multistart(obj, n_starts=args.starts, seed=args.seed)

    # 최적점 주변 무작위 탐색 — 목적함수가 (1+tol) 배 안에 드는 점을 모은다
    rng = np.random.default_rng(args.seed + 1)
    keep = [(best_val, best)]
    span = UB5 - LB5
    for _ in range(args.samples):
        scale = 10 ** rng.uniform(-3, -0.7)             # 0.1 % ~ 20 % 폭
        cand = np.clip(best + rng.normal(0, scale, 5) * span, LB5, UB5)
        v = obj(cand)
        if v <= best_val * (1 + args.tol):
            keep.append((v, cand))
    # 다중 시작이 찾은 국소해도 후보다
    keep += [(v, p) for v, p in sols if v <= best_val * (1 + args.tol)]

    modes = [degradation_modes(ref_best, ref_obj.c_cell, p, obj.c_cell)
             for _, p in keep]
    arr = {k: np.array([m[k] for m in modes]) * 100 for k in ("LAM_PE", "LAM_NE", "LLI")}
    out = {
        "state": args.state, "si_source": args.si_source,
        "half_cell": args.source, "w_dqdv": args.w_dqdv,
        "tol_percent_of_best": args.tol * 100,
        # ⚠ 설정을 산출 **안에** 남긴다. 2026-09-11 자체 리뷰: 파우치 100·200·
        #   300_0009 산출에 starts·seed 가 어디에도 없어서(meta 사이드카는 그
        #   뒤에 생겼다) 나머지 행과 같은 설정이었다는 것을 증명할 수 없었다.
        "n_starts": args.starts, "seed": args.seed,
        "n_grid": args.grid, "n_samples": args.samples,  # R6 내부 F5: 인자 전부가 산출 안에
        "run_id": run_id_of(args),                     # R4-06: 이 시도의 식별자
        "env": _provenance().env_signature(),          # R6 내부 F3
        # ⚠ R16 (조건 8 축 ②): 모집단 선언의 식별자 — 어느 dataset manifest 로 roster 를 정했는가
        "dataset_manifest": D.half_cell_manifest_identity(),
        "consumed_inputs": getattr(obj, "consumed_inputs", None),          # R6 내부 F4 (대상 상태)
        "ref_consumed_inputs": getattr(ref_obj, "consumed_inputs", None),  # (기준 pristine)
        "inputs_sha": getattr(obj, "inputs_sha", None),
        # R4-05: scale 표본의 비유한 개수 — 원본(NaN 만 제거)과의 동치는 Inf 표본이 0 인 영역에서만
        "scale_audit": getattr(obj, "scale_audit", None),
        "ref_scale_audit": getattr(ref_obj, "scale_audit", None),
        "n_accepted": len(keep),
        "best_obj": best_val,
        "best_p": [float(x) for x in best],
        "best_active_bounds": active_bounds(best),
        "ref_p": [float(x) for x in ref_best],
        "ref_active_bounds": active_bounds(ref_best),
        "best_modes_percent": {k: float(v * 100) for k, v in
                               degradation_modes(ref_best, ref_obj.c_cell,
                                                 best, obj.c_cell).items()},
    }
    # ── 2차 진단: 무작위 구름의 **관측** 폭. 폭이 아니라 표집 하한이다 ──
    for k, v in arr.items():
        out[f"{k}_percent_observed_cloud"] = {
            "min": float(v.min()), "max": float(v.max()),
            "span": float(v.max() - v.min()), "median": float(np.median(v)),
            "warning": "무작위 표집의 관측 폭 — 근최적 집합의 폭이 아니다"}

    # ── 1차: 두 방법의 **합집합**. 둘 다 하한이므로 넓은 쪽이 더 나은 하한이다 ──
    ext = near_optimal_extrema(obj, ref_best, ref_obj.c_cell, obj.c_cell,
                               best, best_val, args.tol,
                               seeds=[p for _, p in keep[1:]],
                               n_starts=8, seed=args.seed)
    # 제약 최적화를 **먼저** 돌려 그 범위를 프로파일 격자의 힌트로 준다.
    prof = mode_profile_extrema(obj, ref_best, ref_obj.c_cell, obj.c_cell,
                                best, best_val, args.tol,
                                n_grid=getattr(args, "grid", 21),
                                n_starts=3, seed=args.seed,
                                hint={k: (v["min"], v["max"]) for k, v in ext.items()})
    for k in ("LAM_PE", "LAM_NE", "LLI"):
        lo = min(ext[k]["min"], prof[k]["min"])
        hi = max(ext[k]["max"], prof[k]["max"])
        out[f"{k}_percent"] = {
            "min": lo, "max": hi, "span": hi - lo, "is_lower_bound": True,
            "from_constrained_extrema": ext[k], "from_mode_profile": prof[k]}
    out["span_method"] = (
        "근최적 집합 {obj ≤ best·(1+tol)} 위에서 (a) mode 등식 제약 프로파일과 "
        "(b) 직접 제약 최적화를 둘 다 돌려 **합집합**을 취한다. 둘 다 국소 "
        "해법이므로 결과는 여전히 **하한**이다 — 정확한 폭도, 신뢰구간도 아니다.")
    # ⚠ Codex R9-03: producer 가 쓰는 키 == checker 가 요구하는 키 (`schema.DEGENERACY_KEYS`).
    # ⚠ Codex R10 P2-2: 전 판은 그 강제를 `--out` 에만 걸었다 — stdout 모드는 receipt·`inputs_sha` 가 빠진 JSON 을
    #   그대로 흘리고 stderr 경고 뒤 rc 0 이었다. **sink 는 semantic validity 의 경계가 아니다.** invalid 면 어느 sink
    #   에서도 비영 종료하고, 소비자가 artifact 로 오해하지 않게 bare artifact 대신 typed diagnostic 을 낸다.
    schema_problems = S.check_degeneracy(out)
    if schema_problems:
        print(json.dumps({"status": "invalid", "artifact_kind": "degeneracy", "problems": schema_problems,
                          "note": "스키마를 어긴 산출은 게시하지도 흘리지도 않는다 (Codex R10 P2-2). 값이 필요하면 "
                                  "producer 의 입력(receipt)을 갖춰 다시 부를 것",
                          "run_id": out.get("run_id"), "state": out.get("state")},
                         ensure_ascii=False, indent=2, default=float))
        print(f"! degeneracy 산출이 스키마를 어긴다 ({len(schema_problems)} 건) — 게시하지 않는다: {schema_problems[:4]}",
              file=sys.stderr)
        return 2
    if getattr(args, "out", None):                   # R6 내부 F01: 게시는 잠금 안 원자적 교체로, stdout 은 로그
        atomic_write_json(args.out, out)
        print(f"wrote {args.out}  (run_id {out['run_id']})")
        return 0
    print(json.dumps(out, ensure_ascii=False, indent=2, default=float))


# ── A2. dd_eval.m 대조 — **적합 없이** 같은 p 에서 목적함수만 ──────────

#: `matlab/dd_eval.m` 의 기본 격자와 **같은 순서·같은 값**이어야 한다.
#: 한쪽만 고치면 대조가 조용히 어긋나므로 둘을 같이 고칠 것.
DD_EVAL_P = [
    [1.077218, -0.022949, 1.001342, 0.000309, 0.295099],
    [1.076074, -0.022129, 1.001279, 0.000299, 0.295298],
    [1.181472, -0.141171, 1.080759, -0.000775, 0.239466],
    [1.080000, -0.040000, 1.050000, -0.030000, 0.250000],
    [1.100000, -0.050000, 1.100000, -0.010000, 0.100000],
    [1.100000, -0.050000, 1.100000, -0.010000, 0.200000],
    [1.100000, -0.050000, 1.100000, -0.010000, 0.300000],
    [1.100000, -0.050000, 1.100000, -0.010000, 0.400000],
]

#: 앵커 → 그 값이 갈리면 **어느 단계**가 범인인가. 순서가 곧 이분 순서다.
ANCHOR_STAGE = [
    ("c_cell",         "풀셀 적재 + averageDuplicates + 방향 정규화"),
    ("dv_lo",          "풀셀 differential + quantile(0.15)"),
    ("dv_hi",          "풀셀 differential + quantile(0.85)"),
    ("dv_n",           "dV/dQ 창 마스크가 먹은 격자점 수"),
    ("dq_lo",          "풀셀 differential + quantile(0.05)"),
    ("dq_hi",          "풀셀 differential + quantile(0.95)"),
    ("dq_n",           "dQ/dV 창 마스크가 먹은 격자점 수"),
    ("n_peaks",        "findpeaks(prominence=0.1·range) 가 찾은 피크 수"),
    ("w_peak_sum",     "피크 가중 합 — peak_weight·sigma_ratio·피크 위치"),
    ("w_peak_max",     "피크 가중 최댓값 — 가중 봉우리가 겹쳤는지"),
    ("dq_nuniq_p1",    "첫 행 p 에서 unique(v_smooth) 뒤 남은 점 (모델 단조성)"),
    ("dq_nin_p1",      "첫 행 p 에서 보간 범위에 든 실측 점 (5 미만이면 1e6)"),
    ("E_PE_0p5",       "반쪽전지 적재 (electrode_ocv) — PE OCP"),
    ("E_NE_0p5_0p25",  "문헌 적재 + build_blend_functions — 블렌드 OCP"),
    ("dv_PE_0p5",      "반쪽전지 differential — PE dV/dQ"),
    ("dv_NE_0p5_0p25", "블렌드 differential — NE dV/dQ"),
]


def dd_eval_anchors(obj: Objective, p1=None) -> list[tuple[str, float]]:
    """`matlab/dd_eval.m` 이 CSV 앞머리에 적는 앵커와 **같은 이름·같은 순서**.

    `p1` 은 dQ/dV 쪽 앵커(`dq_nuniq_p1`·`dq_nin_p1`)를 재는 파라미터 —
    dd_eval.m 은 격자의 **첫 행**에서 잰다. 그 둘은 원본이 점을 조용히
    버리는 두 자리(비단조 모델전압 · 보간범위 밖)를 각각 드러낸다.
    """
    p1 = np.array(DD_EVAL_P[0], dtype=float) if p1 is None else np.asarray(p1, float)
    v_u, _ = obj._model_dqdv(p1)
    nin = int(((obj.vol_dq_fit >= v_u.min()) & (obj.vol_dq_fit <= v_u.max())).sum())
    return [
        ("c_cell",         float(obj.c_cell)),
        ("dv_lo",          float(obj.dv_window[0])),
        ("dv_hi",          float(obj.dv_window[1])),
        ("dv_n",           float(len(obj.cap_dv_fit))),
        ("dq_lo",          float(obj.dq_window[0])),
        ("dq_hi",          float(obj.dq_window[1])),
        ("dq_n",           float(len(obj.vol_dq_fit))),
        ("n_peaks",        float(len(obj.peak_locs))),
        ("w_peak_sum",     float(obj.w_peak.sum())),
        ("w_peak_max",     float(obj.w_peak.max())),
        ("dq_nuniq_p1",    float(len(v_u))),
        ("dq_nin_p1",      float(nin)),
        ("E_PE_0p5",       float(np.atleast_1d(obj.half.E_PE(0.5))[0])),
        ("E_NE_0p5_0p25",  float(np.atleast_1d(obj.blend.E(np.atleast_1d(0.5), 0.25))[0])),
        ("dv_PE_0p5",      float(np.atleast_1d(obj.half.dv_PE(0.5))[0])),
        ("dv_NE_0p5_0p25", float(np.atleast_1d(obj.blend.dv(np.atleast_1d(0.5), 0.25))[0])),
    ]


from typing import NamedTuple


class DdEvalText(NamedTuple):
    """dd_eval CSV 의 **한 번 읽은** immutable snapshot — parse·precision·audit·compare 가 전부 이것을 소비한다 (Codex R9-07)."""
    path: str
    text: str
    sha256: str      # 디코드한 text(utf-8) 의 sha256 — 어느 bytes 를 판정했는지 결과에 남긴다


def load_dd_eval(path) -> DdEvalText:
    """경로를 **정확히 한 번** 연다. 이후 어떤 단계도 pathname 을 다시 열지 않는다.

    ⚠ Codex R9-07: 전 판은 `_compare_dd_eval` 이 같은 경로를 세 번 열었다 (parse · precision · audit). 첫 read 가 malformed
      A(중복 헤더) 이고 직후 정상 B 로 원자 교체되면 A 의 32 셀이 B 의 precision/audit 로 승인돼 complete 였다 — 단독 A 는
      invalid 인데. 검증과 사용이 같은 bytes 여야 한다 (R6 내부 F03·F07 과 같은 축, 이번엔 MATLAB 산출 쪽)."""
    import hashlib
    text = Path(path).read_text(encoding="utf-8-sig")
    return DdEvalText(str(path), text, hashlib.sha256(text.encode("utf-8")).hexdigest())


def _dd_eval_lines(src) -> list:
    """snapshot 이면 그 text 를, 경로면 (호환 — 단독 호출용) 한 번 읽는다. 비교기는 항상 snapshot 을 준다."""
    if isinstance(src, DdEvalText):
        return src.text.splitlines()
    return Path(src).read_text(encoding="utf-8-sig").splitlines()


def read_dd_eval_csv(path):
    """dd_eval.m 산출(`# 이름,값` 앞머리 + 헤더 + 파라미터 행)을 읽는다.

    ⚠ 열 구성이 판마다 다르다. 2026-09-10 이전 산출은 `rmse_pocv`·`rmse_dvdq`
      둘뿐이고 그 뒤는 dQ/dV 두 열이 더 붙는다. **헤더를 읽어서** 양쪽에 다
      있는 열만 대조한다 — 그래야 옛 산출 4개(104 값 일치)가 무효가 되지 않는다.
    """
    anchors, rows, header = {}, [], []
    for line in _dd_eval_lines(path):
        line = line.strip()
        if line.startswith("#") and "," in line:
            k, _, v = line.lstrip("# ").partition(",")
            try:
                anchors[k.strip()] = float(v)
            except ValueError:
                pass
        elif line.startswith("a_PE"):
            header = [c.strip() for c in line.split(",")]
        elif line and not line.startswith("#"):
            try:
                rows.append([float(x) for x in line.split(",")])
            except ValueError:
                pass
    return anchors, rows, header


def dd_eval_csv_audit(path, spec=None, spec_label="선언 형식") -> list[str]:
    """이름의 유일성·역할과 행 모양을 **파싱 단계에서** 검사한다 (Codex R4-04 · R5-01 · R5-02 · R5-03).

    전 판은 같은 이름의 열을 `header.index` 로 첫 열만 다시 읽고, 같은 이름의 앵커 줄은 dict 덮어쓰기로
    잃어서 NaN 이 유한성 검사 전에 사라졌다. 중복·열 수 불일치·숫자 아닌 행은 옛 스키마가 아니라
    malformed 다 → 비교하지 않고 `invalid`.
    ⚠ R6 내부 V6-01·V6-03: 행별 검사(열 수·토큰 재출력)는 헤더를 본 **뒤**에만 돌았다 — 헤더가 데이터 뒤에
      있거나 아예 없으면 검사가 한 번도 안 돌고 비교기는 그대로 진행했다. `dd_eval.m` 은 첫 판(56a35a8)부터
      헤더를 먼저 썼으므로 그 두 모양은 옛 스키마가 아니라 malformed 다.
    `spec` 은 토큰이 재출력되어야 하는 형식 (파일 선언, 또는 선언이 없을 때 `--precision` 옵션 — V6-02),
    `spec_label` 은 문제 메시지에 적을 그 출처.
    """
    from collections import Counter
    problems, anchors, header, n_row, n_before_header = [], Counter(), None, 0, 0
    n_decl, known = 0, {k for k, _ in ANCHOR_STAGE}
    tokens = []                                    # (행, 열 이름, 토큰) — 선언 형식과의 일치 검사용
    try:
        lines = _dd_eval_lines(path)
    except OSError as e:
        return [f"읽기 실패: {e}"]
    for line in lines:
        t = line.strip()
        if not t:
            continue
        if t.startswith("#"):
            if "," in t:
                k, _, v = t.lstrip("# ").partition(",")
                k = k.strip()
                # ⚠ Codex R5-02: 역할은 값 변환 **전에** 이름으로 정한다. 형식 선언은 유효한 하나만,
                #   알려진 앵커는 유한 숫자 하나만 — 숫자가 아니면 meta 로 넘기지 않고 malformed 다.
                if k == PRINTED_FORMAT_KEY:
                    n_decl += 1
                    continue
                if k in known:
                    anchors[k] += 1
                    try:
                        float(v)                  # 비유한(nan/inf)은 숫자다 — 비교기가 incomplete 로 처리한다
                    except ValueError:
                        problems.append(f"앵커 {k} 의 값이 숫자가 아니다: {v.strip()!r}")
                    continue
                try:
                    float(v)
                except ValueError:
                    continue                      # 알려지지 않은 이름의 텍스트 값 — impl 표시 등 meta
                anchors[k] += 1                   # 알려지지 않은 숫자 앵커 — 비교엔 안 쓰지만 중복은 본다
            continue
        if t.startswith("a_PE"):
            if header is not None:
                problems.append("헤더가 두 번 나온다")
            header = [c.strip() for c in t.split(",")]
            continue
        n_row += 1
        if header is None:
            n_before_header += 1
        fields = t.split(",")
        if header is not None and len(fields) != len(header):
            problems.append(f"행 {n_row - 1} 열 수 {len(fields)} ≠ 헤더 {len(header)}")
        try:
            [float(x) for x in fields]
        except ValueError:
            problems.append(f"행 {n_row - 1} 숫자가 아닌 칸")
        if header is not None and len(fields) == len(header):
            tokens.extend((n_row - 1, name, tok.strip()) for name, tok in zip(header[5:], fields[5:]))
    if n_decl > 1:
        problems.append(f"{PRINTED_FORMAT_KEY} 선언이 {n_decl} 번 나온다 (유효한 하나만 허용)")
    if header is None and n_row:
        problems.append(f"헤더가 없다 (데이터 행 {n_row} 개) — dd_eval.m 은 첫 판부터 헤더를 썼다: 옛 스키마가 아니라 malformed")
    elif n_before_header:
        problems.append(f"헤더 앞에 데이터 행 {n_before_header} 개 — 행별 검사가 닿지 않는 순서: malformed")
    for k, n in anchors.items():
        if n > 1:
            problems.append(f"중복 앵커 {k} ({n}회)")
    if header:
        for k, n in Counter(header).items():
            if n > 1:
                problems.append(f"중복 열 {k} ({n}회)")
        # ⚠ Codex R5-03: 파라미터 다섯 열은 이름·순서가 정확해야 같은 p 다 — 위치만 보면 b_PE/b_NE 를
        #   바꿔 적어도 complete 였다.
        if header[:5] != PARAM_COLS:
            problems.append(f"파라미터 열 이름/순서가 다르다: {header[:5]} ≠ {PARAM_COLS}")
    # ⚠ Codex R5-01: 선언된 형식으로 토큰을 다시 찍었을 때 같은 문자열이어야 그 선언이 그 토큰의 형식이다.
    if spec is not None and token_format(spec) is not None:
        fmt = token_format(spec)
        for i, name, tok in tokens:
            try:
                x = float(tok)
            except ValueError:
                continue
            if np.isfinite(x) and format(x, fmt) != tok:
                problems.append(f"행 {i} {name} 토큰 {tok!r} 이 {spec_label}({fmt})으로 찍은 {format(x, fmt)!r} 와 다르다")
                break
    return problems


PARAM_COLS = ["a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si"]
#: 첫 판 dd_eval.m (56a35a8:118) 이 쓴 rmse 열 — 부분 대조(옛 스키마)가 성립하려면 최소한 이 둘은 있어야 한다.
OLD_SCHEMA_MIN_COLS = ("rmse_pocv", "rmse_dvdq")


#: 이보다 큰 상대차는 **모델·산술의 차이**로 본다. 앵커에 쓰는 문턱과 같다.
#: 그 아래는 구현 수준의 부동소수점 차이 — 같은 식을 두 언어로 쓰면 남는 양이다.
MODEL_REL = 1e-9


def _token_precision(f: str):
    """토큰 하나의 (소수 자리수, 유효 자리수). 정수 토큰은 (None, n), nan/inf 는 (None, 0)."""
    f = f.strip().lower()
    if not f or f in ("nan", "inf", "-inf", "+inf"):
        return None, 0
    mant, _, exp = f.partition("e")
    dec = len(mant.split(".")[1]) if "." in mant else None
    sig = len(mant.replace("-", "").replace("+", "").replace(".", "").lstrip("0")) or 1
    if dec is not None and exp:
        dec = dec - int(exp)
    return dec, sig


def printed_abs_tols(path, default_decimals: int = 10) -> dict:
    """**열마다** 적힌 자리수가 허용하는 절대 한계.

    ⚠ 2026-09-11 Codex R2-02: 전 판은 파일 전체에서 소수 자리수의 **최솟값**을
      한계로 썼다. 그러면 `%.17g` 파일에 정확한 `1.5` 하나만 있어도 파일 전체
      한계가 0.1 이 되어, 다른 행의 163 % 차이가 "적힌 자리수 안" 으로 덮였다.
      짧은 토큰은 값이 정확히 표현된다는 뜻이지 producer 의 정밀도가 낮다는
      뜻이 아니다. 그래서 (1) 열마다 따로 보고, (2) 유효 15자리 이상 토큰이 하나라도
      있는 열은 **전정밀도 producer**(dd_eval.m 의 `%.17g`)로 보아 한계 0 — 차이는
      상대 띠(`MODEL_REL`)로만 판정한다. 고정 소수 producer(`%.10f` 등)만 열의 최대
      자리수로 한계를 준다.
    """
    cols, decs, sigs = None, {}, {}
    try:
        for line in _dd_eval_lines(path):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("a_PE"):
                cols = [c.strip() for c in line.split(",")][5:]
                continue
            fields = line.split(",")[5:]
            names = cols if cols and len(cols) == len(fields) else [f"col{j}" for j in range(len(fields))]
            for name, field in zip(names, fields):
                dec, sig = _token_precision(field)
                if sig:
                    sigs[name] = max(sigs.get(name, 0), sig)
                if dec is not None:
                    decs[name] = max(decs.get(name, 0), dec)
    except (OSError, ValueError):
        pass
    out = {}
    for name in set(sigs) | set(decs):
        if sigs.get(name, 0) >= 15:
            out[name] = 0.0
        elif name in decs:
            out[name] = 10.0 ** (-decs[name])
        else:
            out[name] = 10.0 ** (-default_decimals)
    return out


def printed_abs_tol(path, default_decimals: int = 10) -> float:
    """파일 전체 한 값이 필요할 때 — 열별 한계의 **최솟값**(가장 빡빡한 열)."""
    tols = printed_abs_tols(path, default_decimals)
    return min(tols.values()) if tols else 10.0 ** (-default_decimals)


#: `# printed_format,%.17g` — dd_eval.m 과 `eval --out` 이 CSV 앞머리에 적는 **형식 선언**.
PRINTED_FORMAT_KEY = "printed_format"


def read_dd_eval_meta(path) -> dict:
    """앞머리 `# 이름,값` 중 **숫자가 아닌** 것 (`impl_*`, `printed_format` …). 앵커와 분리해 읽는다.

    ⚠ R6 내부 V6-06: `printed_format` 은 값이 숫자(`17`)여도 선언이다 — 값의 숫자 여부로 역할을 정하면
      해석 못 하는 선언이 "선언 없음(추정)" 으로 흘러 invalid 가 아니라 partial 이 됐다 (R5-02 의 원칙을
      meta 리더에도: 역할은 이름으로 먼저)."""
    meta = {}
    try:
        for line in _dd_eval_lines(path):
            line = line.strip()
            if line.startswith("#") and "," in line:
                k, _, v = line.lstrip("# ").partition(",")
                if k.strip() == PRINTED_FORMAT_KEY:
                    meta[k.strip()] = v.strip()
                    continue
                try:
                    float(v)
                except ValueError:
                    meta[k.strip()] = v.strip()
    except OSError:
        pass
    return meta


def parse_precision_spec(text):
    """형식 문자열 → (kind, N). kind: exact(전정밀도 — 파싱값이 원래 double) · fixed(소수 N자리) · sig(유효 N자리).

    받는 것: `g17`/`full`, `fixed:N`, `sig:N`, printf 형 `%.Nf` · `%.Ng` (N ≥ 17 이면 exact — 17 유효자리는
    double 을 그대로 복원한다). 해석 못 하면 None — **추정으로 넘기지 않는다** (Codex R4-02).
    """
    t = str(text).strip().lower()
    if t in ("g17", "full", "exact"):
        return ("exact", 17)
    m = re.fullmatch(r"fixed:(\d+)", t)
    if m:
        return ("fixed", int(m.group(1)))
    m = re.fullmatch(r"sig:(\d+)", t)
    if m:
        n = int(m.group(1)); return ("exact", 17) if n >= 17 else ("sig", n)
    m = re.fullmatch(r"%\.(\d+)([fg])", t)
    if m:
        n, kind = int(m.group(1)), m.group(2)
        if kind == "f":
            return ("fixed", n)
        return ("exact", 17) if n >= 17 else ("sig", n)
    return None


def token_format(spec):
    """(kind, N) → Python format 문자열. exact 는 None (파싱값이 원래 double)."""
    kind, n = spec
    if kind == "exact":
        return None
    return f".{n}f" if kind == "fixed" else f".{max(n, 1)}g"      # C 의 %.0g 는 %.1g 다


def token_excess(spec, mv: float, pv: float) -> float:
    """MATLAB 토큰(파싱값 `mv`, 선언 형식 `spec`)이 가리키는 값 구간에서 Python 값 `pv` 가 얼마나 벗어나는가.

    ⚠ Codex R4-03 은 반 단위를, R5-01 은 그 반 단위가 `%g` 에서 틀리다는 것을 보였다 — 10 의 거듭제곱 경계
      아래쪽은 다른 자릿수에서 반올림되고(`%.2g` 의 "10" 은 [9.95, 10.5)), 0 은 정확히 0 만 "0" 이며,
      `%.0g` 는 `%.1g` 다. 공식을 세우는 대신 **같은 형식으로 실제로 찍어서** 정한다: `pv` 가 같은 토큰으로
      찍히면 자리수 안(0), 아니면 구간 경계(형식이 바뀌는 지점, 이분법)까지의 거리가 초과분이다.
      전제: Python 의 format 이 C/MATLAB 의 printf 와 같은 규칙(유효자리 반올림·뒤 0 제거·지수 전환)이다.
    """
    fmt = token_format(spec)
    if fmt is None:
        return abs(mv - pv)
    tok = format(mv, fmt)
    if format(pv, fmt) == tok:
        return 0.0
    lo, hi = mv, pv                                  # lo: 구간 안, hi: 밖 — 단조 형식이라 경계는 하나다
    for _ in range(400):
        mid = (lo + hi) / 2.0
        if mid == lo or mid == hi:
            break
        if format(mid, fmt) == tok:
            lo = mid
        else:
            hi = mid
    return abs(pv - hi)


def cell_tol(spec, value) -> float:
    """구간 반 단위 — **참고용**. 판정은 `token_excess` 가 한다 (R5-01: `%g` 에서 이 값은 대칭이 아니다)."""
    kind, n = spec
    if kind == "exact":
        return 0.0
    if kind == "fixed":
        return 0.5 * 10.0 ** (-n)
    if value == 0 or not np.isfinite(value):
        return 0.5 * 10.0 ** (-(n - 1))
    return 0.5 * 10.0 ** (math.floor(math.log10(abs(value))) - n + 1)


def _infer_column_specs(path) -> dict:
    """선언이 없을 때 값의 자리수에서 열별 (kind, N) 을 **추정**한다 — 탐색용이지 증거가 아니다."""
    cols, decs, sigs = None, {}, {}
    try:
        for line in _dd_eval_lines(path):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("a_PE"):
                cols = [c.strip() for c in line.split(",")][5:]
                continue
            fields = line.split(",")[5:]
            names = cols if cols and len(cols) == len(fields) else [f"col{j}" for j in range(len(fields))]
            for name, field in zip(names, fields):
                dec, sig = _token_precision(field)
                if sig:
                    sigs[name] = max(sigs.get(name, 0), sig)
                if dec is not None:
                    decs[name] = max(decs.get(name, 0), dec)
    except (OSError, ValueError):
        pass
    out = {}
    for name in set(sigs) | set(decs):
        if sigs.get(name, 0) >= 15:
            out[name] = ("exact", 17)
        else:
            out[name] = ("fixed", decs.get(name, 10))
    return out


def declared_precision(path):
    """파일의 `# printed_format,…` 선언 → 'g17' | 'fixed:N' | 'sig:N' | None (선언 없음) | 'invalid' (해석 불가)."""
    fmt = read_dd_eval_meta(path).get(PRINTED_FORMAT_KEY)
    if not fmt:
        return None
    spec = parse_precision_spec(fmt)
    if spec is None:
        return "invalid"
    kind, n = spec
    return "g17" if kind == "exact" else f"{kind}:{n}"


def resolve_precision(path, precision=None) -> dict:
    """대조에 쓸 정밀도 **정책**과 그 출처.

    ⚠ Codex R3-06: 값의 길이로 producer 형식을 추정하는 것은 증거가 아니라 추정이다.
    ⚠ Codex R4-02: 추정은 탐색이다 — 결과가 맞아도 complete 가 아니라 `partial`(사유 정밀도 추정)이고,
      해석 못 하는 선언은 추정으로 넘기지 않고 `invalid` 다. 명시 옵션이 선언보다 느슨하면 그것도
      complete 가 아니다 (Codex Q3: 충돌은 기록하고, 느슨한 override 아래의 일치를 선언된 전정밀도의
      일치로 읽지 않는다).
    우선순위: 명시 옵션 → 파일 선언 → 추정.
    반환 dict: source(option|declared|inferred|invalid) · spec · declared_raw · declared_spec · conflict ·
    inferred_cols · label.
    """
    raw = read_dd_eval_meta(path).get(PRINTED_FORMAT_KEY)
    declared_spec = parse_precision_spec(raw) if raw else None
    out = {"source": None, "spec": None, "declared_raw": raw, "declared_spec": declared_spec,
           "conflict": False, "inferred_cols": {}, "label": ""}
    if precision and str(precision).lower() != "auto":
        spec = parse_precision_spec(precision)
        if spec is None:
            raise ValueError(f"--precision 은 auto | g17 | full | fixed:N | sig:N | %.Nf | %.Ng 중 하나다: {precision!r}")
        out.update(source="option", spec=spec, label=f"--precision {precision}")
        if declared_spec is not None and declared_spec != spec:
            out["conflict"] = True
            out["label"] += f" (파일 선언 `{raw}` 과 다르다 — 옵션을 적용)"
        elif raw and declared_spec is None:
            out["label"] += f" (파일 선언 `{raw}` 은 해석 불가 — 옵션을 적용)"
        return out
    if raw:
        if declared_spec is None:
            out.update(source="invalid", label=f"# {PRINTED_FORMAT_KEY},{raw} — 해석 못 하는 선언 (추정으로 넘기지 않는다)")
        else:
            out.update(source="declared", spec=declared_spec, label=f"# {PRINTED_FORMAT_KEY},{raw}")
        return out
    out.update(source="inferred", inferred_cols=_infer_column_specs(path),
               label="값의 자리수에서 **추정** (파일에 형식 선언 없음) — 탐색용, complete 가 되지 않는다")
    return out


def cmd_eval(args):
    """적합 없이 주어진 p 에서 rmse 를 찍고, 원하면 MATLAB 산출과 대조한다.

    툴박스가 없는 기계에서도 포팅 대조를 할 수 있게 만든 우회로다:
    포팅이 맞는지 묻는 데 정말 필요한 것은 최적화기가 아니라 **모델**이므로,
    같은 p 에서 두 구현이 같은 rmse 를 내는지만 보면 된다.
    """
    root = D.data_root(args.data_root)
    obj = build(root, args.source, args.state, args.si_source,
                w_dqdv=args.w_dqdv, scale_seed=args.seed)

    P = np.array(DD_EVAL_P, dtype=float)
    anchors = dd_eval_anchors(obj, P[0])
    print(f"# dd_eval  state={args.state}  halfcell=data/half_cell/{args.source}/  "
          f"Si={args.si_source}  w_dqdv={args.w_dqdv:g}")
    print(f"# {PRINTED_FORMAT_KEY},%.17g")          # R3-06: 형식은 선언한다, 추정시키지 않는다
    # R6 내부 F3·F4: 어떤 인터프리터·라이브러리로, 어떤 입력 파일(sha256)로 찍은 값인지 파일이 스스로 말한다
    #   (`# 이름,값` 의 값이 숫자가 아니라 audit 는 meta 로 넘기고 비교기는 무시한다).
    env_line = "# env," + ";".join(f"{k}={v}" for k, v in _provenance().env_signature().items())
    ci = getattr(obj, "consumed_inputs", {}) or {}
    flat = [(k, v) for k, v in ci.items() if "sha256" in v] + [(f"literature_{k}", v) for k, v in ci.get("literature", {}).items()]
    inputs_line = (f"# inputs,sha={getattr(obj, 'inputs_sha', '')} "
                   + " ".join(f"{k}={Path(v['path']).name}:{v['sha256'][:12]}" for k, v in flat))
    print(env_line); print(inputs_line)
    audit = getattr(obj, "scale_audit", None)
    audit_line = None
    if audit:                                        # R4-05: 이 자료에서 scale 표본에 비유한 값이 있었나
        # R5-09: 줄 자체에 식별자(상태·소스·Si·seed·표본 수)를 붙인다 — 붙여 넣은 사본만으로 구성 집합을 셀 수 있게.
        # R5-06: eps 상대 영향과 동치 flag 도 같이.
        # U13 사본에는 data root 식별자가 없어 루트 차원을 보고 순서로만 알았다 — 이제 root 이름도 붙인다.
        audit_line = scale_audit_line(root, args, audit, inputs_sha=getattr(obj, "inputs_sha", None))
        print(audit_line)
    for k, v in anchors:
        print(f"# {k},{v:.17g}")

    # ⚠ 열 이름·순서는 `matlab/dd_eval.m` 의 `hdr` 과 **같아야 한다**.
    cols = ["rmse_pocv", "rmse_dvdq", "rmse_dqdv", "rmse_dqdv_w"]
    vals = {"rmse_pocv":   [obj.rmse_pocv(q) for q in P],
            "rmse_dvdq":   [obj.rmse_dvdq(q) for q in P],
            "rmse_dqdv":   [obj.rmse_dqdv(q, False) for q in P],
            "rmse_dqdv_w": [obj.rmse_dqdv(q, True) for q in P]}
    lines = ["a_PE,b_PE,a_NE,b_NE,gamma_Si," + ",".join(cols)]
    print(lines[0])
    for i, q in enumerate(P):
        r = ",".join([f"{x:.6f}" for x in q] + [f"{vals[c][i]:.17g}" for c in cols])
        lines.append(r)
        print(r)

    # ⚠ Codex R10 P1-1: `--compare` 의 근거는 **어떤 쓰기보다 먼저** 한 번 읽어 snapshot 으로 든다. 전 판은 `--out` 이
    #   먼저 파일을 교체한 뒤 comparator 가 처음 읽어서, `--out X --compare X` 가 독립 근거 X 를 제 출력으로 덮고
    #   그것과 자기를 대조해 16/16 앵커·32/32 RMSE `complete` rc 0 을 냈다 (포팅 identity 가 아니라 자기대조다).
    #   같은 object 인지는 경로 문자열이 아니라 realpath/samefile 로 본다 — symlink·hardlink alias 도 같은 파일이다.
    snap = None
    if args.compare:
        if args.out and same_object(args.out, args.compare):
            print(f"! `--out` 과 `--compare` 가 **같은 파일**이다 ({args.out}) — 출력이 비교 근거를 덮으면 그 대조는 "
                  f"자기대조다. 독립 근거를 다른 경로로 두고 다시 부를 것 (Codex R10 P1-1)\n종료 코드 2 (invalid)")
            return 2
        try:
            snap = load_dd_eval(args.compare)
        except OSError:
            snap = None                                  # 못 읽는 경우는 비교기가 invalid 로 판정한다

    if args.out:
        head = [f"# dd_eval  state={args.state}  halfcell=data/half_cell/{args.source}/  "
                f"Si={args.si_source}  w_dqdv={args.w_dqdv:g}",
                f"# {PRINTED_FORMAT_KEY},%.17g", env_line, inputs_line]
        if audit_line:                               # U12: 파일에도 남긴다 (stdout 사본에 기대지 않게)
            head.append(audit_line)
        head += [f"# {k},{v:.17g}" for k, v in anchors]
        Path(args.out).write_text("\n".join(head + lines) + "\n", encoding="utf-8")
        print(f"\nwrote {args.out}")

    if args.compare:
        # ⚠ 2026-09-11 Codex R3-07: 전 판은 여기서 dict 를 버리고 None 을 올려 `sys.exit(None)` = 0 —
        #   "rmse 가 갈린다" 를 찍고도 명령은 성공이었다. 판정이 곧 종료 코드다.
        try:
            result = _compare_dd_eval(dict(anchors), P, vals, snap if snap is not None else args.compare,
                                      precision=getattr(args, "precision", None))
        except ValueError as e:                      # 잘못된 --precision 은 대조 미완이다
            print(f"! {e}\n종료 코드 2 (invalid)")
            return 2
        rc = EXIT_BY_STATUS.get(result["status"], 2)
        note = ""
        if rc == 3 and getattr(args, "allow_partial", False):
            # R4-02: `--allow-partial` 은 **옛 스키마**(앵커·열 누락)만 허용한다. 정밀도 추정·느슨한
            #   override 는 그 옵션으로도 0 이 되지 않는다 — 형식을 `--precision` 으로 명시할 것.
            others = [r for r in result.get("partial_reasons", []) if not r.startswith("스키마")]
            if others:
                note = " — `--allow-partial` 은 스키마 누락만 허용한다; 남은 사유: " + "; ".join(others)
            else:
                rc, note = 0, " — `--allow-partial` 로 옛 스키마의 부분 대조를 허용했다"
        print(f"종료 코드 {rc} ({result['status']}{note})")
        return rc
    return 0


#: producer 의 typed 완전성 → 종료 코드 (Codex R9-06 의 ne_shape 규약을 matrix·profile 로 넓힌다, Codex R10 P1-3·P1-4).
#:   0 complete — 기대 모집단 전부가 성공했다 → canonical 에 원자 교체
#:   1 none     — 성공이 하나도 없다 (부분이 아니라 없음)
#:   3 partial  — 일부만 성공했거나 입력이 없는 조합이 있다
#: none·partial 은 canonical 을 **건드리지 않고** `<out>/partial/` 에만 쓴다 — 완전성 판정이 게시보다 먼저다.
PRODUCER_EXIT = {"complete": 0, "none": 1, "partial": 3, "subset": 3}


#: 부분 산출의 index — 소비자가 **wildcard 로 훑지 않도록** 시도마다 한 줄 (Codex R10 P2-2 가 없앤 그 소비).
PARTIAL_INDEX = "index.json"


def publish_target(out, status, run_id: str | None = None):
    """complete 만 canonical 자리로. 나머지는 `partial/<종류>/<attempt-id>/<이름>` 으로 (조건 8 축 ④).

    ⚠ R16: 전 판은 `partial/<이름>` 하나였다 — **같은 이름의 다음 부분 실행이 그 자리를 덮었다.**
      canonical 은 안 건드리므로 과학 값은 안전했지만, "언제 무엇을 시도해 무엇이 나왔나" 가 사라졌다.
      부분의 기록 자체가 증거다.

    **attempt-id(`run_id`) 가 정본이다** (R12 Q4 는 답이 안 왔으므로 우리가 정하고 근거를 적는다):
    이 저장소의 provenance 는 산출을 **시도**에 묶고(행마다 `run_id`, 자체 리뷰 C02), content-id 로 하면
    같은 bytes 를 낸 **두 시도가 한 자리로 합쳐진다** — 그 사실이야말로 이 축이 남기려는 것이다.
    "같은 bytes 가 여러 번 쌓인다" 는 받아들이고, index 가 digest 를 적어 **드러낸다**.

    같은 시도 자리에 두 번 쓰는 것은 버그이므로 `FileExistsError` 다 (immutable 이라는 말이 무엇도
    막지 않으면 이름뿐이다). `run_id` 가 없으면 자리를 정할 수 없으므로 거부한다 — 부재는 안전값이 아니다.
    """
    import re as _re
    out = Path(out)
    if status == "complete":
        out.parent.mkdir(parents=True, exist_ok=True)
        return out
    if not run_id:
        raise ValueError("부분 산출은 attempt-id(run_id) 없이 자리를 정할 수 없다 (조건 8 축 ④)")
    # ⚠ Codex R17 P1-02: `Path / str(run_id)` 에서 run_id 가 **절대경로**면 앞의 `partial/<종류>` 가 버려진다 —
    #   `run_id=str(canonical.parent)` 하나로 partial 목적지가 **canonical 자체**가 됐다 (반환 경로 실측).
    #   production 은 그 경로에 먼저 쓰고 `record_partial` 을 부르므로 뒤의 `relative_to` 오류는 예방이 아니다.
    #   attempt-id 는 **단일 경로 성분**이어야 한다: 구분자·상위 이동(`..`)·alias(`.`)·절대경로·빈 값을 첫
    #   mkdir 전에 거부하고, 해석된 목적지가 고정 partial root 아래인지 **쓰기 전에** 확인한다.
    rid = str(run_id)
    if not _re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", rid):
        raise ValueError(f"attempt-id(run_id) 는 단일 경로 성분이어야 한다 ([A-Za-z0-9._-], 선두는 영숫자, "
                         f"128 자 이하) — 받은 것: {rid!r} (Codex R17 P1-02)")
    root = out.parent / "partial"
    dest = root / S.kind_of(out.name) / rid / out.name
    if not dest.resolve().is_relative_to(root.resolve()) or dest.resolve() == out.resolve():
        raise ValueError(f"부분 산출의 목적지가 partial root 밖이다: {dest} (Codex R17 P1-02)")
    if dest.exists():
        raise FileExistsError(f"같은 시도 자리에 두 번 쓴다: {dest} — 부분 단위는 immutable 이다")
    dest.parent.mkdir(parents=True, exist_ok=True)
    return dest


def read_partial_index(out) -> dict:
    """`partial/index.json` 을 읽는다 (없으면 빈 index) — **소비자는 디렉터리를 훑지 않는다** (R10 P2-2)."""
    p = Path(out).parent / "partial" / PARTIAL_INDEX
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"index_version": 1, "attempts": []}
    return doc if isinstance(doc, dict) and isinstance(doc.get("attempts"), list) else {"index_version": 1, "attempts": []}


def latest_partial(out) -> Path | None:
    """그 산출의 **가장 최근 시도** 경로 (index 기준). 없으면 None.

    index 의 소비자다 — 부분 단위가 `partial/<종류>/<attempt-id>/` 로 흩어졌으므로 이름만으로는 못 찾고,
    그래서 index 가 있다. wildcard 로 훑으면 stale 을 고를 수 있다 (R11 P2-2 가 `ls | head -1` 에서 본 것).
    """
    out = Path(out)
    root = out.parent / "partial"
    rows = [e for e in read_partial_index(out)["attempts"] if e.get("artifact") == out.name]
    if not rows:
        return None
    return root / rows[-1]["path"]


def record_partial(out, dest, *, status: str, run_id: str) -> dict:
    """게시한 부분 단위를 `partial/index.json` 에 **한 줄** 더한다 → 그 줄.

    index 가 있어야 소비자가 디렉터리를 훑지 않는다. digest 를 같이 적는 이유는 attempt-id 를 정본으로
    골랐기 때문이다 — 같은 bytes 의 중복을 **숨기지 않고 보이게** 하는 것이 그 선택의 조건이다.
    """
    import datetime as _dt
    out, dest = Path(out), Path(dest)
    root = out.parent / "partial"
    root.mkdir(parents=True, exist_ok=True)
    idx_path = root / PARTIAL_INDEX
    try:
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        if not isinstance(idx, dict) or not isinstance(idx.get("attempts"), list):
            raise ValueError
    except (OSError, ValueError):
        idx = {"index_version": 1, "attempts": []}
    row = {"attempt": str(run_id), "kind": S.kind_of(out.name), "artifact": out.name,
           "status": status, "path": str(dest.relative_to(root)),
           "sha256": _provenance().sha256_file(dest),
           "recorded_utc": _dt.datetime.now(_dt.timezone.utc).isoformat()}
    idx["attempts"].append(row)
    atomic_write_json(idx_path, idx)
    return row


def same_object(a, b) -> bool:
    """두 경로가 **같은 object** 인가 — 문자열이 아니라 realpath·samefile 로 (Codex R10 P1-1: symlink·hardlink alias)."""
    if a is None or b is None:
        return False
    pa, pb = Path(a), Path(b)
    try:
        if pa.exists() and pb.exists():
            return os.path.samefile(pa, pb)
    except OSError:
        pass
    return os.path.realpath(pa) == os.path.realpath(pb)


#: 대조 판정 → process 종료 코드 (R3-07). 완전한 지원 범위의 일치만 0 이다.
#:   1 = 갈렸다(앵커/목적함수)  2 = 대조 미완·빈 파일(성공 아님)  3 = 부분(옛 스키마: 앵커·열 누락) —
#:   3 은 `--allow-partial` 을 **명시**했을 때만 0 이 된다.
EXIT_BY_STATUS = {"complete": 0, "anchor_mismatch": 1, "model_mismatch": 1,
                  "incomplete": 2, "empty": 2, "invalid": 2, "partial": 3}


def _compare_dd_eval(py_anchors, py_P, py_vals, matlab_csv, precision=None):
    """MATLAB 산출과 대조하고, **갈린 첫 단계**를 이름으로 말한다.

    `py_vals` 는 열이름 → 값 목록. MATLAB CSV 의 **헤더에 있는 열만** 댄다
    (옛 산출은 rmse 두 열뿐이다). 반환 dict 의 `status`:
      complete        앵커 16 · 행 8 · 열 4 전부 비교했고 전부 일치 (유일한 성공)
      partial         비교한 것은 전부 일치하지만 옛 스키마라 앵커/열이 빠졌다 (성공 아님)
      incomplete      비교 못 한 값이 있다 — 행 누락·격자 불일치·비유한(NaN) 앵커/파라미터/metric
      anchor_mismatch 앵커가 갈린다 (단계 이름을 말한다) / model_mismatch 목적함수가 갈린다
    `precision` 은 `--precision` (R3-06): None/'auto' 면 파일 선언 → 추정 순.
    """
    result = {"status": "complete", "expected": 0, "compared": 0, "problems": [],
              "worst_rel": 0.0, "first_bad": None,
              "anchors_expected": len(ANCHOR_STAGE), "anchors_compared": 0, "missing_anchors": [],
              "partial": False, "partial_reasons": [],
              "precision_source": None, "precision_label": "", "precision_declared": None,
              "precision_conflict": False, "precision_override_looser": False, "matlab_sha256": None}
    try:
        # 한 번 읽은 snapshot 으로 parse·precision·audit 전부 (Codex R9-07). 호출자가 이미 **쓰기 전에** 읽어 두었으면
        # 그 snapshot 을 그대로 받는다 (Codex R10 P1-1) — 여기서 경로를 다시 열지 않는다.
        snap = matlab_csv if isinstance(matlab_csv, DdEvalText) else load_dd_eval(matlab_csv)
        m_anchors, m_rows, m_header = read_dd_eval_csv(snap)
        policy = resolve_precision(snap, precision)
    except OSError as e:
        # ⚠ R6 내부 V6-07: 전 판은 여기서 traceback 으로 죽어 종료 1 = "갈림" 이었다. 못 읽은 파일은 미완이다.
        print(f"\n=== dd_eval.m 대조: {matlab_csv} ===\n  ! 읽을 수 없다: {e}\n판정: **대조 미완 (invalid)**")
        result["problems"].append(f"읽기 실패: {e}"); result.update(status="invalid"); return result
    prec_source, prec_label = policy["source"], policy["label"]
    result.update(precision_source=prec_source, precision_label=prec_label,
                  precision_declared=policy["declared_raw"], precision_conflict=policy["conflict"])
    result["matlab_sha256"] = snap.sha256
    print(f"\n=== dd_eval.m 대조: {snap.path} ===")
    print(f"  (snapshot sha256 {snap.sha256[:16]}… — 한 번 읽은 text 로 parse·precision·audit·compare 전부; 검증 뒤 경로를 다시 "
          f"열지 않는다, Codex R9-07)")
    print(f"  (정밀도: {prec_label})")
    if prec_source == "inferred":
        print("  ⚠ 한계는 **추정**이다 — 값의 길이는 producer 형식의 증거가 아니다 (Codex R3-06·R4-02)."
              " 추정으로는 complete 가 되지 않는다: dd_eval.m 의 `# printed_format` 선언이 있는 파일을"
              " 쓰거나 `--precision g17|fixed:N` 으로 명시할 것.")
        print("  (추정한 열별 형식: " + ", ".join(f"{k} {a}:{b}" for k, (a, b) in policy["inferred_cols"].items()) + ")")
    print("  (판정: Python 값이 MATLAB 토큰과 같은 형식으로 같은 문자열로 찍히면 '자리수 안', 토큰 구간 경계 밖의 "
          f"초과분이 상대 {MODEL_REL:.0e} 이하면 '수치 잡음', 그 이상이면 '모델 차이' — Codex R4-03 · R5-01)")
    # ⚠ 2026-09-11 Codex R2-01: 전 판은 비교하지 **않은** 셀(행 누락·격자 불일치·
    #   NaN)도 "전부 일치" 로 인증했다. 이제 기대 셀 수와 실제 비교한 셀 수를 세고,
    #   하나라도 못 비교했으면 성공 문장을 내지 않는다.
    # ⚠ 2026-09-11 Codex R3-05: 그 개수·유한성 검사가 metric 에만 있었다 — 누락 앵커는 `continue`,
    #   NaN 앵커는 `r > 1e-9` 가 거짓, NaN 파라미터는 `max(...) > tol` 이 거짓이라 셋 다 complete.
    #   앵커도 기대 16 개를 세고, 비유한 값은 어디서든 성공이 아니다.
    if not m_anchors and not m_rows:
        print("  ! 읽을 내용이 없다 — 경로가 맞나?")
        result.update(status="empty"); return result
    # ⚠ Codex R4-04: 이름의 유일성·행 모양은 비교 전에 본다. 중복 열/앵커는 옛 스키마가 아니라 malformed.
    # 토큰 검사는 파일 자신의 선언으로; 선언이 없으면(또는 해석 불가면) `--precision` 옵션이 "이 파일은 이 형식"
    # 이라는 주장이므로 그 형식으로 검사한다 (R6 내부 V6-02: 전 판은 옵션을 토큰과 대조하지 않아 선언 없는
    # 파일이 선언된 파일보다 관대했다). 선언과 옵션이 둘 다 있으면 선언으로 검사하고 충돌은 R4-02 Q3 대로 기록.
    if policy["declared_spec"] is not None:
        malformed = dd_eval_csv_audit(snap, spec=policy["declared_spec"])
    else:
        malformed = dd_eval_csv_audit(snap, spec=policy["spec"], spec_label="옵션 형식")
    if prec_source == "invalid":
        malformed.append(f"{PRINTED_FORMAT_KEY} 선언 해석 불가: {policy['declared_raw']!r}")
    if malformed:
        print("판정: **파일이 malformed 다 — 비교하지 않았다 (invalid)**")
        for pmsg in malformed[:12]:
            print(f"      - {pmsg}")
        result["problems"].extend(malformed)
        result.update(status="invalid"); return result
    if prec_source == "inferred":
        result["partial_reasons"].append("정밀도 추정 (파일에 형식 선언 없음, 옵션 없음)")

    def rel(a, b):
        return abs(a - b) / max(abs(b), 1e-30)

    hard = result["problems"]
    print(f"  {'앵커':<16} {'MATLAB':>22} {'Python':>22} {'상대차':>10}   단계")
    first_bad = None
    for k, stage in ANCHOR_STAGE:
        if k not in m_anchors:
            print(f"  {k:<16} {'(없음)':>22} — 옛 dd_eval.m 산출인가?")
            result["missing_anchors"].append(k)
            continue
        a, b = m_anchors[k], py_anchors.get(k, float("nan"))
        if not (np.isfinite(a) and np.isfinite(b)):
            print(f"  {k:<16} {a!s:>22} {b!s:>22} {'비유한':>10}   {stage}")
            hard.append(f"앵커 {k} 비유한 (MATLAB {a!r}, Python {b!r})")
            continue
        result["anchors_compared"] += 1
        if k == "dv_n":
            mark = "" if a == b else "  ← 다르다"
            print(f"  {k:<16} {a:>22.0f} {b:>22.0f} {'':>10}{mark}   {stage}")
            if a != b and first_bad is None:
                first_bad = (k, stage)
            continue
        r = rel(a, b)
        mark = "  ←" if r > 1e-9 else ""
        print(f"  {k:<16} {a:>22.12g} {b:>22.12g} {r:>10.2e}{mark}   {stage}")
        if r > 1e-9 and first_bad is None:
            first_bad = (k, stage)

    print()
    worst_row = 0.0
    shared = [c for c in m_header[5:] if c in py_vals] if m_header else []
    if not m_header:
        shared = ["rmse_pocv", "rmse_dvdq"]        # 헤더 없는 아주 옛 산출
        print("  (헤더가 없다 — 앞 두 열만 rmse 로 본다)")
    missing = [c for c in py_vals if c not in shared]
    absent_min = [c for c in OLD_SCHEMA_MIN_COLS if c not in shared]
    if absent_min:
        # ⚠ R6 내부 V6-04: "스키마 누락" 에 하한이 없어 rmse 열 0 개(앵커 0 개)여도 partial → `--allow-partial` 로
        #   "앵커 0개와 rmse 0개가 전부 일치" 가 0 이었다. 가장 오래된 산출(56a35a8)도 이 두 열은 썼다.
        msg = (f"옛 스키마 최소 열 {list(OLD_SCHEMA_MIN_COLS)} 중 {absent_min} 가 없다 — 옛 dd_eval.m 산출이 아니라 "
               f"비교할 것이 없는 파일이다 (헤더: {m_header})")
        print(f"판정: **{msg} (invalid)**")
        result["problems"].append(msg); result.update(status="invalid"); return result
    if missing:
        print(f"  (MATLAB 산출에 없는 열은 건너뛴다: {', '.join(missing)}"
              f" — 옛 dd_eval.m 산출이다 → **부분 대조**)")
    if result["missing_anchors"]:
        print(f"  (MATLAB 산출에 없는 앵커 {len(result['missing_anchors'])} 개: "
              f"{', '.join(result['missing_anchors'])} → **부분 대조**)")
    schema_partial = bool(missing) or bool(result["missing_anchors"])
    if schema_partial:
        result["partial_reasons"].insert(0, "스키마 누락 (옛 dd_eval.m 산출: "
                                         + ", ".join(missing + result["missing_anchors"]) + ")")
    result["expected"] = len(py_P) * len(shared)

    def spec_for(col):
        if policy["spec"] is not None:
            return policy["spec"]
        return policy["inferred_cols"].get(col, ("fixed", 10))
    if len(m_rows) != len(py_P):
        print(f"  ! 행 수가 다르다: MATLAB {len(m_rows)} vs Python {len(py_P)} — 대조 미완")
        hard.append(f"행 수 {len(m_rows)} vs {len(py_P)}")
    n_rows = min(len(m_rows), len(py_P))
    if n_rows:
        head = "  " + f"{'p 행':<5}" + "".join(f"{c + ' 상대차':>22}" for c in shared) + "   판정"
        print(head)
        for i, mr in enumerate(m_rows[:n_rows]):
            pp = [float(x) for x in py_P[i][:5]]
            if len(mr) < 5 or not all(np.isfinite(mr[:5])) or not all(np.isfinite(pp)):
                print(f"  {i:<5} ! 파라미터에 비유한 값이 있다 — 이 행은 비교하지 않았다")
                hard.append(f"행 {i} 파라미터 비유한")
                continue
            if max(abs(mr[j] - pp[j]) for j in range(5)) > 1e-6:
                print(f"  {i:<5} ! 파라미터가 다른 행이다 — 격자가 어긋났다 (이 행은 비교하지 않았다)")
                hard.append(f"행 {i} 파라미터 불일치")
                continue
            cells, eff = [], 0.0
            for c in shared:
                j = m_header.index(c) if m_header else (5 + shared.index(c))
                mv = mr[j] if j < len(mr) else float("nan")
                pv = py_vals[c][i] if i < len(py_vals[c]) else float("nan")
                if not (np.isfinite(mv) and np.isfinite(pv)):
                    cells.append(f"{'비유한':>22}")
                    hard.append(f"행 {i} {c} 비유한")
                    continue
                r = rel(mv, pv)
                cells.append(f"{r:>22.2e}")
                result["compared"] += 1
                # 토큰이 가리키는 값 구간 안이면 "차이" 가 아니다; 구간 경계 밖의 초과분만 수치 차이로
                # 센다 (R4-03 반 단위 → R5-01 실제 형식으로 정한 구간)
                sp = spec_for(c)
                if policy["conflict"] and policy["declared_spec"] is not None \
                        and token_excess(policy["declared_spec"], mv, pv) > token_excess(sp, mv, pv):
                    result["precision_override_looser"] = True
                excess = token_excess(sp, mv, pv)
                if excess > 0.0:
                    eff = max(eff, excess / max(abs(pv), 1e-30))
            worst_row = max(worst_row, eff)
            if eff == 0.0:
                verdict = "적힌 자리수 안"
            elif eff <= MODEL_REL:
                verdict = "수치 잡음"
            else:
                verdict = "모델 차이  ←"
            print(f"  {i:<5}" + "".join(cells) + f"   {verdict}")

    print()
    result["worst_rel"] = worst_row
    result["first_bad"] = first_bad
    if result["precision_override_looser"]:
        result["partial_reasons"].append(
            f"명시 옵션이 파일 선언 `{policy['declared_raw']}` 보다 느슨하다 — 선언된 정밀도의 일치가 아니다")
    partial = bool(result["partial_reasons"])
    result["partial"] = partial
    n_a, n_e = result["anchors_compared"], result["anchors_expected"]
    tag = "판정:"
    if partial:
        tag = (f"판정(부분 — 앵커 {n_a}/{n_e} · 열 {len(shared)}/{len(py_vals)}"
               + ("" if not [r for r in result["partial_reasons"] if not r.startswith("스키마")] else " · 정밀도")
               + "):")
    if first_bad:
        k, stage = first_bad
        print(f"판정: **{k}** 에서 처음 갈린다 → 범인 단계는 「{stage}」")
        print("      그 앞 앵커는 맞았으므로 그 앞 단계는 용의선상에서 빠진다.")
        result["status"] = "anchor_mismatch"
    elif hard:
        print(f"판정: **대조 미완 — 성공 아님** (비교한 앵커 {n_a}/{n_e}, rmse {result['compared']}/{result['expected']}).")
        for pmsg in hard[:12]:
            print(f"      - {pmsg}")
        print("      비교하지 못한 값이 있으면 이 파일로는 '일치' 를 말할 수 없다.")
        result["status"] = "incomplete"
    elif worst_row > MODEL_REL:
        print(f"{tag} 앵커는 전부 맞는데 rmse 가 갈린다 (최대 상대차 {worst_row:.2e})")
        print("      → 곡선은 같고 **목적함수 산술**이 다르다는 뜻이다.")
        result["status"] = "model_mismatch"
    elif worst_row > 0.0:
        n_rmse = result["compared"]
        print(f"{tag} 앵커 {n_a}개가 전부 맞고, rmse {n_rmse}개는")
        print(f"      **적힌 자리수보다는 크고 {MODEL_REL:.0e} 보다는 작은**")
        print(f"      차이만 남는다 (반올림 반 단위를 뺀 최대 상대차 {worst_row:.2e}).")
        print("      토큰의 반올림 구간을 넘는 양이므로 이건 출력 반올림이 아니라")
        print("      **실제 수치 차이**다 — 같은 식을 MATLAB 과 Python 으로 각각")
        print("      쓰면 남는 양(평활·보간·누산 순서)이고, 모델의 차이가 아니다.")
        print("      같은 p 에서 두 구현이 같은 목적함수를 낸다 = 포팅이 그들 모델이다.")
        result["status"] = "partial" if partial else "complete"
    else:
        n_rmse = result["compared"]
        print(f"{tag} 앵커 {n_a}개와 rmse {n_rmse}개가"
              f" **적힌 자리수 안에서 전부 일치**.")
        result["status"] = "partial" if partial else "complete"
        print("      남은 차이는 전부 토큰의 반올림 반 단위 안이다 —")
        print("      이 파일로는 그보다 정밀하게 비교할 수 없다.")
        print("      같은 p 에서 두 구현이 같은 목적함수를 낸다 = 포팅이 그들 모델이다.")
    if result["status"] == "partial":
        print("      ⚠ **부분 대조**다 (성공 아님):")
        for reason in result["partial_reasons"]:
            print(f"        - {reason}")
    return result


# ── D. scale 비결정성 ──────────────────────────────────────────────────
    return result

def cmd_scale_noise(args):
    root = D.data_root(args.data_root)
    rows = []
    for seed in range(args.repeats):
        obj = build(root, args.source, args.state, args.si_source,
                    w_dqdv=args.w_dqdv, scale_seed=seed)
        best, val, _ = multistart(obj, n_starts=args.starts, seed=seed)
        rows.append({"seed": seed, "scales": obj.scales,
                     "p": [float(x) for x in best], "obj": val,
                     "rmse_pocv": obj.rmse_pocv(best),
                     "bounds": active_bounds(best)})
    P = np.array([r["p"] for r in rows])
    out = {"state": args.state, "si_source": args.si_source,
           "repeats": args.repeats, "rows": rows,
           "scale_pocv_spread": [min(r["scales"]["pocv"] for r in rows),
                                 max(r["scales"]["pocv"] for r in rows)],
           "scale_dvdq_spread": [min(r["scales"]["dvdq"] for r in rows),
                                 max(r["scales"]["dvdq"] for r in rows)],
           "param_span": {n: float(P[:, i].max() - P[:, i].min())
                          for i, n in enumerate(["a_PE", "b_PE", "a_NE",
                                                 "b_NE", "gamma_Si"])}}
    print(json.dumps(out, ensure_ascii=False, indent=2, default=float))


# ── E. 모델 선택 매트릭스 ──────────────────────────────────────────────

def cmd_matrix(args):
    """같은 데이터에 **모델 선택만** 바꿔 가며 답이 얼마나 움직이는지.

    축: 문헌 Si 소스 8 × 반쪽전지 소스 2 × dQ/dV 포함 여부 2.
    각 조합에서 pristine 과 대상 상태를 **같은 조합으로** 적합해 LAM/LLI 를 낸다
    (원본 파이프라인이 그렇게 한다 — 기준도 그 조합의 pristine 이다).
    """
    root = D.data_root(args.data_root)
    rows = []
    sources = ([args.source] if args.only_source else list(D.HALF_FILE))
    # ⚠ Codex R10 P1-4: 기대 조합 roster 를 **돌기 전에** 정한다. 전 판은 존재하지 않는 입력을 조용히 건너뛰고
    #   (R9-04 와 같은 축), 전 조합이 실패해도 4 열짜리 error 행 16 개로 기존 complete canonical 을 덮은 뒤
    #   함수가 None 을 돌려 process rc 0 이었다. 알려진 부재(`D.HALF_CELL_ABSENT`)만 모집단에서 빠진다.
    # ⚠ Codex R11 P1-2: **authority 는 caller 옵션 밖**이다. 전 판은 `--only-source --only-wdqdv` 가 requested 자체를
    #   8 개로 줄이고 그것을 complete·canonical·rc 0 으로 게시했다 (진짜 authority 는 2 소스 × 8 Si × 2 가중 = 32).
    #   정본 roster 를 먼저 세고, 진단 selector 가 그것을 줄이면 그 실행은 `subset` 이다 (canonical 아님).
    # ⚠ Codex R11 P1-4: 부재 선언(`HALF_CELL_ABSENT`)과 **실제 파일이 모순**이면 조용히 빼지 않고 실패한다 —
    #   오래된 선언이 새로 생긴 측정을 숨기면 32 개짜리 실행이 16 개로 줄어든 채 complete 가 된다.
    # ⚠ Codex R13 P1-1: 모집단 **구성원**의 정본은 `S.canonical_combo_keys` 한 곳이다. 전 판은 여기서 만든 집합이
    #   산출에 **개수로만** 실렸고 checker 는 그 개수끼리만 댔다 — 32 행 중 하나를 미등록 Si 로 바꾸거나 1 행이
    #   "authority=1" 이라 적으면 통과했다. 이제 producer 와 checker 가 **같은 함수**를 쓴다.
    contradictions = []
    for hc in D.HALF_FILE:
        if args.state not in D.HALF_FILE.get(hc, {}):
            continue
        if (hc, args.state) in D.HALF_CELL_ABSENT:
            if D.half_cell_path(root, hc, args.state).is_file():
                contradictions.append(f"{hc}/{args.state}")
            continue                                     # 알려진 부재 — 요청 자체가 아니다
    authority = sorted(S.canonical_combo_keys(args.state))
    if contradictions:
        print(f"! 부재 선언과 실제 파일이 모순이다 — `D.HALF_CELL_ABSENT` 는 {contradictions} 를 없다고 선언했는데 "
              f"파일이 있다. 선언을 고치기 전에는 이 상태의 모집단을 말할 수 없다 (Codex R11 P1-4) → 종료 코드 2",
              file=sys.stderr)
        return 2
    weights = [args.w_dqdv] if args.only_wdqdv else [0.0, 1.0]
    requested, available, missing_input = [], [], []
    for hc in sources:
        if args.state not in D.HALF_FILE.get(hc, {}) or (hc, args.state) in D.HALF_CELL_ABSENT:
            continue
        combos = [(hc, si, w) for si in D.SI_SOURCES for w in weights]
        requested += combos
        (available if D.half_cell_path(root, hc, args.state).is_file() else missing_input).extend(combos)
    subset = sorted(requested) != sorted(authority)       # 진단 selector 가 authority 를 줄였다
    # ⚠ 자체 리뷰 C05: 모집단 주장을 **행마다** 봉인한다 (profile 의 `gamma_roster` 와 같은 축). 전 판은 stdout
    #   `SUMMARY` 한 줄에만 있어 소비자가 0 이었고, 축소된 묶음을 canonical 자리에 놓으면 게이트가 못 알아봤다.
    #   실패 목록은 아래 루프가 채우므로 여기서는 자리만 잡고 루프 뒤에 한 번에 적는다.
    for hc, si, w in available:
        try:
            ro = build(root, hc, "pristine", si, w_dqdv=w, scale_seed=args.seed)
            rp, _, _ = multistart(ro, n_starts=args.starts, seed=args.seed)
            o = build(root, hc, args.state, si, w_dqdv=w, scale_seed=args.seed)
            p, val, _ = multistart(o, n_starts=args.starts, seed=args.seed)
        except Exception as e:                  # noqa: BLE001
            rows.append({"half_cell": hc, "si": si, "w_dqdv": w,
                         "error": f"{type(e).__name__}: {e}"})
            continue
        m = degradation_modes(rp, ro.c_cell, p, o.c_cell)
        # ⚠ 리뷰 [B4-4]: 전 판은 `ref_bounds` 만 남겼다. 그러면
        #   LAM = 1 − state/ref 의 변화가 **기준이 움직인 것인지 대상이
        #   움직인 것인지 분리할 수 없다** (둘 다 같은 LAM 을 낸다).
        #   기준 적합의 전체 파라미터·목적함수·c_cell 을 같이 남긴다.
        aud_t, aud_r = getattr(o, "scale_audit", None), getattr(ro, "scale_audit", None)
        rows.append({
            "half_cell": hc, "si": si, "w_dqdv": w, "run_id": run_id_of(args),
            "inputs_sha": getattr(o, "inputs_sha", None),   # R6 내부 F4: 소비 입력 identity
            # ⚠ Codex R7-03: 행은 **기준 적합도** 소비한다. 기준 전용 입력(pristine 반쪽전지)만 바뀌어도
            #   LAM 이 움직이는데 서명은 대상 것뿐이라 두 실행의 행을 구분할 수 없었다. 양쪽을 남긴다.
            "ref_inputs_sha": getattr(ro, "inputs_sha", None),
            "consumed_inputs": json.dumps(getattr(o, "consumed_inputs", None), ensure_ascii=False),
            "ref_consumed_inputs": json.dumps(getattr(ro, "consumed_inputs", None), ensure_ascii=False),
            # ⚠ Codex R5-07: 이 조합이 scale 동치 영역 안인지는 행이 스스로 말해야 한다
            "scale_seed": args.seed, "n_scale_samples": getattr(o, "n_scale_samples", None),
            "scale_pocv_target": o.scales.get("pocv"), "scale_dvdq_target": o.scales.get("dvdq"),
            "scale_dqdv_target": o.scales.get("dqdv"),
            "scale_pocv_ref": ro.scales.get("pocv"), "scale_dvdq_ref": ro.scales.get("dvdq"),
            "scale_dqdv_ref": ro.scales.get("dqdv"),
            "scale_audit_target": json.dumps(aud_t, ensure_ascii=False) if aud_t else "",
            "scale_audit_ref": json.dumps(aud_r, ensure_ascii=False) if aud_r else "",
            "obj": val, "rmse_pocv": o.rmse_pocv(p),
            "a_PE": p[0], "b_PE": p[1], "a_NE": p[2], "b_NE": p[3],
            "gamma_Si": p[4], "c_cell": o.c_cell,
            "bounds": ",".join(active_bounds(p)) or "-",
            "ref_a_PE": rp[0], "ref_b_PE": rp[1], "ref_a_NE": rp[2],
            "ref_b_NE": rp[3], "ref_gamma_Si": rp[4],
            "ref_obj": float(ro(rp)), "ref_rmse_pocv": ro.rmse_pocv(rp),
            "ref_c_cell": ro.c_cell,
            "ref_bounds": ",".join(active_bounds(rp)) or "-",
            "LAM_PE_pct": m["LAM_PE"] * 100,
            "LAM_NE_pct": m["LAM_NE"] * 100,
            "LLI_pct": m["LLI"] * 100,
            # 자체 리뷰 C05: 자리를 스키마 순서 끝에 잡아 두고 루프 뒤에 실패 목록까지 확정해 채운다
            "combo_roster": None})
        assert tuple(rows[-1]) == S.MATRIX_ROW, (tuple(rows[-1]), S.MATRIX_ROW)   # producer == schema (Codex R9-03)
        print(json.dumps(rows[-1], ensure_ascii=False, default=float),
              flush=True)

    ok = [r for r in rows if "error" not in r]
    failed = [r for r in rows if "error" in r]
    status = ("complete" if ok and not failed and not missing_input and len(ok) == len(requested)
              else ("none" if not ok else "partial"))
    if subset and status != "none":
        status = "subset"                                 # 축소한 진단 실행은 완전성 주장을 하지 않는다 (R11 P1-2)
    combo_roster = {"authority": len(authority), "requested": len(requested),
                    "succeeded": len(ok),
                    "missing_input": [f"{h}|{s}|{w:g}" for h, s, w in missing_input],
                    "failed": [f"{r['half_cell']}|{r['si']}|{float(r['w_dqdv']):g}" for r in failed],
                    #: 알려진 부재(`D.HALF_CELL_ABSENT`) — 분모에서 뺀 이유를 산출이 스스로 말한다
                    "absent": [f"{h}|{args.state}" for h in sorted(D.HALF_FILE)
                               if (h, args.state) in getattr(D, "HALF_CELL_ABSENT", frozenset())]}
    for r in ok:
        r["combo_roster"] = json.dumps(combo_roster, ensure_ascii=False)
    summary = {"state": args.state, "n_combinations": len(rows),
               "status": status,
               # Codex R10 P1-4: 축소 전 모집단을 산출이 스스로 말한다 (요청·입력 있음·입력 없음·실패).
               # 자체 리뷰 C05 뒤로 같은 주장이 **행에도** 봉인된다 — 여기 요약은 사람용이고 정본은 행이다.
               "combo_roster": dict(combo_roster, available=len(available)),
               "n_ok": len(ok),
               "n_with_active_bound": sum(1 for r in ok if r["bounds"] != "-"),
               "n_negative_LAM": sum(1 for r in ok if min(r["LAM_PE_pct"],
                                                          r["LAM_NE_pct"]) < 0)}
    for k in ("LAM_PE_pct", "LAM_NE_pct", "LLI_pct"):
        v = np.array([r[k] for r in ok], dtype=float)
        if v.size:
            summary[k] = {"min": float(v.min()), "max": float(v.max()),
                          "span": float(v.max() - v.min()),
                          "median": float(np.median(v))}

    # ── 축별 폭은 **분모를 제목에 적어서** 낸다 (리뷰 B4) ──
    #   전 판은 "경계에 안 붙은 10" 과 "그중 6" 사이에서 기준을 설명 없이
    #   바꿨다. 사후선택 집합과 전체를 나란히 적어 그 일이 다시 없게 한다.
    def _span(g, k):
        v = [r[k] for r in g]
        return (float(max(v) - min(v)), len(g)) if v else (None, 0)

    axes = {}
    for hc in sorted({r["half_cell"] for r in ok}):
        g = [r for r in ok if r["half_cell"] == hc and r["w_dqdv"] == 0.0]
        if g:
            sp, n = _span(g, "LLI_pct")
            axes[f"{hc}_dqdv_off_all_Si"] = {
                "n": n, "si_sources": sorted({r["si"] for r in g}),
                "LLI_span_pct": sp,
                "LAM_NE_span_pct": _span(g, "LAM_NE_pct")[0],
                "LAM_PE_span_pct": _span(g, "LAM_PE_pct")[0]}
    interior = [r for r in ok
                if r["bounds"] == "-" and r["ref_bounds"] == "-" and r["w_dqdv"] == 0.0]
    if interior:
        sp, n = _span(interior, "LLI_pct")
        axes["dqdv_off_BOTH_interior_only"] = {
            "n": n, "half_cells": sorted({r["half_cell"] for r in interior}),
            "si_sources": sorted({r["si"] for r in interior}),
            "LLI_span_pct": sp,
            "warning": "사후선택 집합이다 — '문헌 곡선 선택' 축의 값이 아니다"}
    summary["axes_with_denominator"] = axes

    # ── dQ/dV on/off 는 **같은 조합의 대응쌍**으로만 (리뷰 B4) ──
    by = {(r["half_cell"], r["si"], r["w_dqdv"]): r for r in ok}
    matched, all_pairs = [], []
    for hc in sorted({r["half_cell"] for r in ok}):
        for si in sorted({r["si"] for r in ok}):
            a, b = by.get((hc, si, 0.0)), by.get((hc, si, 1.0))
            if a is None or b is None:
                continue
            d = b["LLI_pct"] - a["LLI_pct"]
            all_pairs.append(d)
            if all(r["bounds"] == "-" and r["ref_bounds"] == "-" for r in (a, b)):
                matched.append({"half_cell": hc, "si": si, "delta_LLI_pct": d})
    if all_pairs:
        v = np.array(all_pairs, dtype=float)
        summary["dqdv_paired_contrast"] = {
            "all_pairs": {"n": int(v.size), "n_positive": int((v > 0).sum()),
                          "n_negative": int((v < 0).sum()),
                          "median_pct": float(np.median(v)),
                          "min_pct": float(v.min()), "max_pct": float(v.max())},
            "both_endpoints_interior": {
                "n": len(matched), "rows": matched,
                "delta_range_pct": [min(m["delta_LLI_pct"] for m in matched),
                                    max(m["delta_LLI_pct"] for m in matched)]
                if matched else None},
            "note": "비대응 비교는 부호가 섞인다 — 대응쌍으로만 말할 것"}
    print("\nSUMMARY " + json.dumps(summary, ensure_ascii=False, default=float))
    if args.out and rows:
        # ⚠ 완전성 판정이 **게시보다 먼저**다 (Codex R10 P1-4). complete 만 canonical 을 원자 교체하고, error 행이
        #   하나라도 있거나 입력이 빠진 조합이 있으면 `partial/` 로 간다 — 기존 canonical 은 건드리지 않는다.
        keys = sorted({k for r in rows for k in r})
        # ⚠ R16 (조건 8 축 ④): 부분은 `partial/<종류>/<attempt-id>/` 로 가고 index 에 한 줄 남는다 —
        #   전 판은 같은 이름의 다음 부분 실행이 그 자리를 덮어 시도의 역사가 사라졌다.
        dest = publish_target(args.out, status, run_id=run_id_of(args))
        atomic_write_csv(dest, rows, keys)               # R4-06: 시도별 임시 파일 → 한 번에 게시
        if status != "complete":
            record_partial(args.out, dest, status=status, run_id=run_id_of(args))
        print(f"wrote {dest}" + ("" if status == "complete" else
                                 f"  [{status} — canonical {args.out} 은 건드리지 않았다 (Codex R10 P1-4)]"))
    if status != "complete":
        print(f"[matrix] status **{status}** — 정본 authority {len(authority)} · 요청 {len(requested)} · 성공 {len(ok)} · "
              f"실패 {len(failed)} · 입력 없음 {len(missing_input)} → 종료 코드 {PRODUCER_EXIT[status]}"
              + ("  (진단 selector 가 authority 를 줄였다 — canonical 아님, Codex R11 P1-2)" if subset else ""))
    return PRODUCER_EXIT[status]



# ── F. γ_Si ↔ a_NE 프로파일 (Schmitt 2022 가 "같은 서명" 이라 쓰고 안 잰 자리) ──

def cmd_profile(args):
    """γ_Si 를 고정하고 나머지 넷을 다시 적합 — 프로파일 목적함수.

    평평하면 γ 와 나머지가 서로를 대신할 수 있다는 뜻이고, 그때 LAM_NE 는
    데이터가 아니라 **γ 를 준 사람**이 정한 값이다.
    """
    root = D.data_root(args.data_root)
    # ⚠ R16 (조건 8 축 ①): 공유 입력(full-cell workbook · 문헌)을 **명령 경계에서 한 번** 읽어
    #   아래로 넘긴다 — 기준과 대상이 각자 읽으면 그 사이의 재-export 가 두 행을 갈라놓는다.
    shared = shared_snapshot(root, args.si_source)
    ref = build(root, args.source, "pristine", args.si_source, shared=shared,
                w_dqdv=args.w_dqdv, scale_seed=args.seed)
    ref_p, _, _ = multistart(ref, n_starts=args.starts, seed=args.seed)
    obj = build(root, args.source, args.state, args.si_source, shared=shared,
                w_dqdv=args.w_dqdv, scale_seed=args.seed)
    best, best_val, _ = multistart(obj, n_starts=args.starts, seed=args.seed)

    # ⚠ Codex R11 P1-3: γ 격자는 **계약**이다 (`S.CANONICAL_GAMMA_GRID_N`). `--grid 1` 은 1 점짜리 산출을 냈고 모든
    #   span 이 0 인 채 complete·canonical·rc 0 이었다. 다른 격자는 진단이고 canonical 이 아니다.
    # ⚠ Codex R13 P1-1: 정본 격자의 **값**도 `S.canonical_gamma_grid` 한 곳에서 나온다 — 전 판은 개수만 계약이라
    #   21 점을 0~0.4 로 깔아도 canonical 로 통과했다. 다른 격자 수는 진단이고 canonical 이 아니다.
    grid_subset = int(args.grid) != S.CANONICAL_GAMMA_GRID_N
    gammas = (np.array(S.canonical_gamma_grid()) if not grid_subset
              else np.linspace(LB5[4], UB5[4], args.grid))
    per_gamma_scale = getattr(args, "profile_scale", "global") == "per-gamma"
    global_scales = dict(obj.scales)
    rows, skipped = [], []
    for g in gammas:
        if per_gamma_scale:
            # MATLAB 검증기 절차: lb(5)=ub(5)=g 를 넘겨서 fit 을 부르므로,
            # 원 scale 식이 넘겨받은 경계를 쓰면 γ 마다 scale 이 달라진다 [A1].
            # ⚠ 그러면 행마다 **다른 목적함수**라서 obj_ratio_to_best 를 행끼리
            #   비교할 수 없다. 그 사실을 산출에 같이 적는다.
            lbg, ubg = LB5.copy(), UB5.copy()
            lbg[4] = ubg[4] = g
            obj.scales = obj._auto_scales(args.seed, obj.n_scale_samples,
                                          lb=lbg, ub=ubg)
        f = lambda q: obj(np.array([q[0], q[1], q[2], q[3], g]))   # noqa: E731
        bnds = list(zip(LB5[:4], UB5[:4]))
        bv, bx = np.inf, None
        rng = np.random.default_rng(args.seed)
        starts = [best[:4]] + list(LB5[:4] + rng.random((args.starts, 4))
                                   * (UB5[:4] - LB5[:4]))
        # ⚠ 2026-09-11 Codex R2-03: 이 loop 는 multistart 의 success 필터를 안 받아
        #   비정상 종료 결과를 완료 적합처럼 저장했다 (리뷰 A3 의 미종결 경로).
        #   같은 정책으로 거르고, 시도/성공 수를 행에 남기며, 전부 실패한 γ 는
        #   저장하지 않는다.
        n_tried = n_ok = 0
        for s in starts:
            n_tried += 1
            try:
                r = minimize(f, s, method="L-BFGS-B", bounds=bnds,
                             options={"maxiter": 400, "ftol": 1e-12})
            except Exception:                            # noqa: BLE001
                continue
            if not np.isfinite(r.fun) or not bool(getattr(r, "success", True)):
                continue
            n_ok += 1
            if r.fun < bv:
                bv, bx = float(r.fun), r.x.copy()
        if bx is None:
            print(f"[profile] γ={g:.4f}: 시작점 {n_tried}개 전부 실패 (not_success/비유한) — "
                  f"이 γ 는 저장하지 않는다 (skipped)", flush=True)
            skipped.append(float(g))
            continue
        p = np.array([bx[0], bx[1], bx[2], bx[3], g])
        m = degradation_modes(ref_p, ref.c_cell, p, obj.c_cell)
        rows.append({"gamma_Si": float(g), "obj": bv,
                     "obj_ratio_to_best": bv / best_val,
                     "rmse_pocv": obj.rmse_pocv(p),
                     "a_PE": float(p[0]), "b_PE": float(p[1]),
                     "a_NE": float(p[2]), "b_NE": float(p[3]),
                     "bounds": ",".join(active_bounds(p)) or "-",
                     "LAM_PE_pct": m["LAM_PE"] * 100,
                     "LAM_NE_pct": m["LAM_NE"] * 100,
                     "LLI_pct": m["LLI"] * 100,
                     "n_ok": n_ok, "n_tried": n_tried, "run_id": run_id_of(args),
                     # R6 내부 F5: 같은 run_id·같은 스키마에 숫자만 달랐던 인자와 소비 입력 identity 를 행에
                     "profile_scale": "per-gamma" if per_gamma_scale else "global",
                     "inputs_sha": getattr(obj, "inputs_sha", None),
                     # ⚠ Codex R7-03: LAM 은 기준 적합에도 달려 있다 — 기준 입력이 바뀌면 행이 움직이므로 그
                     #   서명을 같이 적는다.
                     "ref_inputs_sha": getattr(ref, "inputs_sha", None),
                     # ⚠ Codex R8-04: 전체 identity 를 summary(stdout → `.csv.log`) 에만 두면 다음 정상 재시도가 실패할 때
                     #   redirect 가 log 를 먼저 잘라 이전 정상 묶음의 출처가 사라진다 — 실행 log 는 durable receipt 가
                     #   아니다. 검증되는 묶음(CSV) 자체에 둔다 (matrix 행과 같은 모양).
                     "consumed_inputs": json.dumps(getattr(obj, "consumed_inputs", None), ensure_ascii=False),
                     "ref_consumed_inputs": json.dumps(getattr(ref, "consumed_inputs", None), ensure_ascii=False),
                     # ⚠ Codex R10 P1-3: 실패한 γ 는 행에서 빠진다 — 행만으로 모집단을 알 수 없으면 1 행짜리 부분
                     #   산출이 canonical 을 덮어도 아무도 모른다. loop 뒤에 요청·성공·누락을 채운다 (자리는 여기).
                     "gamma_roster": None})
        assert tuple(rows[-1]) == S.PROFILE_ROW, (tuple(rows[-1]), S.PROFILE_ROW)   # producer == schema (Codex R9-03)
        print(json.dumps(rows[-1], ensure_ascii=False, default=float), flush=True)

    # ⚠ Codex R10 P1-3: γ 모집단은 계산 **전에** 정해진 격자다. 요청·성공·누락을 행마다 봉인한다 (사라지는 stdout
    #   요약이 아니라 검증되는 묶음이 스스로 말한다 — R8-04 와 같은 축).
    roster = {"authority": S.CANONICAL_GAMMA_GRID_N, "requested": int(len(gammas)), "succeeded": len(rows),
              "missing": [float(g) for g in skipped]}
    for r in rows:
        r["gamma_roster"] = json.dumps(roster, ensure_ascii=False)
    status = "complete" if (rows and not skipped) else ("none" if not rows else "partial")
    if grid_subset and status != "none":
        status = "subset"                                # 정본 격자가 아니면 완전성 주장을 하지 않는다 (R11 P1-3)
    inside = [r for r in rows if r["obj_ratio_to_best"] <= 1 + args.tol]
    obj.scales = global_scales
    summary = {"state": args.state, "si_source": args.si_source,
               "half_cell": args.source, "best_obj": best_val,
               # Codex R7-03: 이 실행이 실제로 소비한 대상·기준 입력 (행의 `inputs_sha`·`ref_inputs_sha` 의 원본)
               "consumed_inputs": getattr(obj, "consumed_inputs", None),
               "ref_consumed_inputs": getattr(ref, "consumed_inputs", None),
               "inputs_sha": getattr(obj, "inputs_sha", None),
               "ref_inputs_sha": getattr(ref, "inputs_sha", None),
               "profile_scale": "per-gamma" if per_gamma_scale else "global",
               "ratio_comparable_across_rows": not per_gamma_scale,
               "scale_note": (
                   "per-gamma 는 행마다 목적함수가 달라 obj_ratio_to_best 를 "
                   "행끼리 비교할 수 없다. global 은 비교는 되지만 MATLAB "
                   "검증기가 넘기는 경계와 다르다 [리뷰 A1 — 미결]."
                   if per_gamma_scale else
                   "global: 모든 행이 같은 목적함수라 비교는 되지만, MATLAB "
                   "검증기는 γ 를 묶은 경계를 넘긴다 [리뷰 A1 — 미결]."),
               "best_gamma": float(best[4]),
               "tol_percent": args.tol * 100,
               "gamma_inside_tol": [float(min(r["gamma_Si"] for r in inside)),
                                    float(max(r["gamma_Si"] for r in inside))]
               if inside else None,
               "n_inside": len(inside),
               "status": status, "gamma_roster": roster,
               "gamma_all_failed": skipped}
    for k in ("a_NE", "LAM_NE_pct", "LAM_PE_pct", "LLI_pct"):
        if inside:
            v = np.array([r[k] for r in inside], dtype=float)
            summary[k + "_span_inside_tol"] = float(v.max() - v.min())
    print("\nSUMMARY " + json.dumps(summary, ensure_ascii=False, default=float))
    # ⚠ 2026-09-11 Codex R3-08: 전 판은 전부 실패하면 파일을 안 쓰고 **정상 반환**했다 — 같은
    #   경로에 옛 CSV 가 있으면 wrapper 가 그것을 새 성공으로 읽었다. 이제 (i) 산출은 임시 파일에
    #   쓴 뒤 한 번에 옮기고(반쯤 쓰인 파일이 남지 않는다), (ii) 저장할 행이 없으면 종료 코드 2 —
    #   옛 파일은 지우지 않지만(보존) 이번 실행의 결과가 아니다.
    # ⚠ Codex R11 P2-1: **종료 코드는 semantic status 에서 온다** — sink 유무가 그것을 바꾸면 안 된다. 전 판은
    #   `--out` 없이 돌린 부분 실행이 summary 에 `partial` 을 찍고도 rc 0 이었다.
    if args.out and rows:
        # ⚠ Codex R4-06: 고정 이름 `.part` 는 같은 목적지를 쓰는 두 시도가 서로의 행을 게시했다 —
        #   시도별 고유 임시 파일 + 행마다 run_id 로 계산과 게시 bytes 를 묶는다.
        # ⚠ Codex R10 P1-3: complete 만 canonical. 부분은 `partial/` 로 — 완전성 판정이 게시보다 먼저다.
        # ⚠ R16 (조건 8 축 ④): 위와 같다 — 시도마다 자기 자리, index 에 한 줄.
        dest = publish_target(args.out, status, run_id=run_id_of(args))
        atomic_write_csv(dest, rows, list(rows[0]))
        if status != "complete":
            record_partial(args.out, dest, status=status, run_id=run_id_of(args))
        print(f"wrote {dest} [status {status}] (run_id {run_id_of(args)})"
              + ("" if status == "complete" else f"  — canonical {args.out} 은 건드리지 않았다"))
    if rows and status != "complete":
        print(f"[profile] status **{status}** — 정본 격자 {roster['authority']} · γ 요청 {roster['requested']} · "
              f"성공 {roster['succeeded']} · 누락 {roster['missing']} → 종료 코드 {PRODUCER_EXIT[status]} "
              f"(부분·축소는 승격 대상이 아니다)")
    if rows:
        return PRODUCER_EXIT[status]
    if not rows:
        print(f"[profile] 저장할 행이 없다 (모든 γ 가 실패)"
              + (f" — {args.out} 를 쓰지 않는다 (기존 파일이 있어도 이번 실행의 산출이 아니다)"
                 if args.out else "") + " → 종료 코드 2")
        return 2
    return 0



# ── G. 측정 잡음 규모 — "1 % 띠" 를 정확도 언어로 쓸 수 있나 ──────────────

def diff_sigma(y: np.ndarray, order: int = 2, stride: int = 1) -> float:
    """m 차 차분 잡음 추정 — **모델도 반복측정도 필요 없다.**

        sigma^2 = sum (D^m y)^2 / ( (n-m) * C(2m, m) )

    m=2 가 고전적인 Rice/GSJS 추정기다 (C(4,2)=6). 왜 되나: 참 곡선이
    매끄러우면 m 차 차분이 그 부분을 거의 지우고(다항식 차수 m-1 까지는
    정확히 0) 잡음만 남는다. 계수 C(2m,m) 은 독립 잡음의 m 차 차분 분산이다.

    `order` 를 올리면 곡률 오염이 줄고, `stride` 를 올리면 **상관된 잡음이
    분리된다.** 둘을 같이 훑는 것이 `noise_diagnosis` 의 판정이다.
    """
    from math import comb
    y = np.asarray(y, dtype=float)[::max(1, int(stride))]
    m = int(order)
    if y.size <= m + 1:
        return float("nan")
    d = y
    for _ in range(m):
        d = np.diff(d)
    return float(np.sqrt(np.sum(d ** 2) / (d.size * comb(2 * m, m))))


def rice_sigma(y: np.ndarray) -> float:
    """m=2 고정 — 옛 이름 유지."""
    return diff_sigma(y, order=2, stride=1)


def noise_diagnosis(y: np.ndarray) -> dict:
    """sigma 를 재고, **이 방법이 어디서 멈추는지**를 같이 적는다.

    2026-09-10. 이 함수는 네 번 고쳐 쓴 끝에 "가르지 않는다" 로 끝났다.
    실패의 기록을 남긴다 — 같은 길을 다시 걷지 않게.

    (1) 1 차 차분의 lag-1 자기상관이 양수면 "평활된 신호" 라고 단정했다.
        못 가른다. 촘촘히 표본된 깨끗한 신호에서도, 표본 간 전압 변화가 잡음과
        같은 규모면 양수가 된다. 실측(`300_0009`)이 정확히 그 경계였다
        (표본당 dV 약 20 uV, sigma 약 28 uV, 자기상관 +0.417).
    (2) 스트라이드 스캔을 넣고 "커지면 평활" 이라 했다. **곡률도 커진다.**
        잡음 0 인 해석 곡선에서 406 배 커졌다.
    (3) 배증당 성장률로 세 경우를 가르려 했다. 문턱이 합성 경계에서 흔들렸다
        (독립 1.00 / 평활 1.41 / 해석곡선 2.46 — 뒤의 둘이 안 갈린다).
    (4) 스캔 최댓값을 상한으로 쓰려 했다. **상관 길이보다 스캔이 짧으면
        상한이 못 된다** (savgol(201) 신호를 k<=64 로 훑으면 참 0.500 mV 를
        0.033 mV 로 본다). 멀리까지 훑으면 이번엔 곡률이 먼저 올라와서
        평탄부가 안 생긴다 — 네 합성 케이스 전부 평탄 판정 실패.

    **구조적인 이유**: 한 곡선에서 "측정 잡음" 과 "매끄러운 신호" 를 가르려면
    둘의 주파수 대역이 갈라져 있어야 한다. 잡음이 이미 필터링됐고 신호에 그와
    비슷한 스케일의 곡률이 있으면, **한 곡선만으로는 원리적으로 못 가른다.**
    이 프로젝트가 다루는 축퇴와 같은 종류의 문제다.

    그래서 판정하지 않고 **두 해석을 다 적는다**:

        원자료(필터 안 걸림)이면  -> k=1 의 sigma 가 잡음. 비율을 그대로 씀
        필터 걸린 자료면          -> k=1 의 sigma 는 하한, 비율은 **상한**

    어느 쪽인지는 **곡선이 아니라 계측 쪽에 물어야 답이 나온다** — 그 질문을
    `FOR_BMS_TEAM.md` 에 넣었다. 원자료 export 가 따로 있으면 거기에 이 명령을
    걸어 보는 것이 곧바로 답이다.

    차수 스캔(m=1..4)은 여전히 쓸모가 있다: k=1 에서 m 을 올려도 sigma 가 거의
    안 변하면 **그 지점에서는 곡률 오염이 없다**는 뜻이다 (합성 독립잡음:
    0.0328 / 0.0299 / 0.0299 / 0.0299).
    """
    orders = {m: diff_sigma(y, order=m) for m in (1, 2, 3, 4)}
    n = int(np.asarray(y).size)
    ks, k = [], 1
    while k <= max(1, n // 64) and k <= 1024:
        ks.append(k); k *= 2
    strides = {k: diff_sigma(y, order=4, stride=k) for k in ks}
    o = [orders[m] for m in (2, 3, 4) if orders[m] == orders[m] and orders[m] > 0]
    order_flat = bool(o and max(o) / min(o) < 1.15)
    return {
        "sigma_by_order_V": orders,
        "sigma_by_stride_order4_V": strides,
        "sigma_at_k1_V": strides.get(1, float("nan")),
        "order_scan_flat": order_flat,
        "order_scan_reading": (
            "m=2..4 에서 sigma 가 15 % 안에서 같다 -> k=1 에서 **곡률 오염은 없다**."
            if order_flat else
            "m 을 올리면 sigma 가 15 % 넘게 줄어든다 -> k=1 에 **곡률이 섞여 있다** "
            "(참 잡음은 더 작다)."),
        "note": ("이 값이 잡음인지 필터의 잔재인지는 **한 곡선으로 못 가른다** "
                 "(머리말 참조). 원자료 export 에 같은 명령을 걸면 곧바로 답이 "
                 "나온다."),
    }


def cmd_noise(args):
    """측정 잡음 σ 를 재고, 모델 부적합과 견준다.

    이 명령이 답하는 질문: **"최적의 1 % 안" 을 오차막대라고 불러도 되나?**

    안 된다는 것을 보이는 방식이 중요하다. 잡음을 못 재서가 아니라, 재고 나면
    **부적합이 잡음보다 압도적으로 크다**는 것이 드러나기 때문이다. 그러면
    목적함수를 likelihood 로 바꿔 신뢰구간을 만드는 절차 자체가 성립하지 않는다
    (χ² 이 자유도보다 훨씬 커서 곡률 기반 구간이 **거짓으로 좁아진다**).
    """
    root = D.data_root(args.data_root)
    obj = build(root, args.source, args.state, args.si_source,
                w_dqdv=args.w_dqdv, scale_seed=args.seed)

    # ⚠ Codex R7-02: 경로를 다시 열지 않는다 — `build` 가 적합에 쓴 **그 bytes** 의 원시 배열을 그대로 쓴다.
    cap_raw, vol_raw = obj.full_cell_raw
    cap_ad, vol_ad = average_duplicates(cap_raw, vol_raw)
    order = np.argsort(cap_ad)
    v_ad = vol_ad[order]

    best, best_val, _ = multistart(obj, n_starts=args.starts, seed=args.seed)
    resid = obj.voltage - obj.E_cell(best, obj.capacity)
    misfit = float(np.sqrt(np.mean(resid ** 2)))

    s_raw = rice_sigma(v_ad)
    s_res = rice_sigma(resid)
    d1 = np.diff(v_ad)
    ac1 = float(np.corrcoef(d1[:-1], d1[1:])[0, 1]) if d1.size > 2 else float("nan")
    diag = noise_diagnosis(v_ad)
    s_k1 = diag["sigma_at_k1_V"]

    out = {
        "state": args.state, "si_source": args.si_source, "half_cell": args.source,
        "n_points_raw": int(cap_raw.size), "n_points_after_avg": int(v_ad.size),
        "sigma_meas_from_raw_V": s_raw,
        "sigma_meas_from_residual_V": s_res,
        "lag1_autocorr_of_first_diff": ac1,
        "misfit_rmse_pocv_V": misfit,
        "misfit_over_sigma": misfit / s_raw if s_raw > 0 else float("inf"),
        "sigma_at_k1_V": s_k1,
        "misfit_over_sigma_if_raw_data": misfit / s_k1 if s_k1 > 0 else float("inf"),
        "diagnosis": diag,
        "best_p": [float(x) for x in best], "best_obj": float(best_val),
        # 분자(부적합)와 분모(σ)가 **같은 입력**에서 나왔다는 것을 산출이 스스로 말한다 (Codex R7-02)
        "consumed_inputs": getattr(obj, "consumed_inputs", None),
        "inputs_sha": getattr(obj, "inputs_sha", None),
    }
    # lag-1 자기상관은 **단독으로는 판정 못 한다** (noise_diagnosis 머리말).
    # 판정은 스트라이드 스캔이 한다. 자기상관은 참고로만 남긴다.
    # 어느 오염 방향이든 결론이 같은가 — 그것만 본다 (noise_diagnosis 머리말)
    r = out["misfit_over_sigma_if_raw_data"]
    out["verdict"] = (
        "**원자료라면** 부적합이 잡음보다 {:.0f} 배 크다. 목적함수를 likelihood 로 바꿔 신뢰구간을 "
        "만들면 χ² 이 자유도보다 {:.0f}² 배 커서 **거짓으로 좁은** 구간이 나온다. "
        "그러므로 '1 % 띠' 는 오차막대가 아니라 **분석자 선택 민감도**로만 읽어야 "
        "한다 — 이것은 잡음을 못 재서가 아니라, 재고 나서 내린 결론이다."
    ).format(r, r) if r > 3 else (
        "부적합이 잡음과 같은 규모다 ({:.1f} 배). 이 경우에는 likelihood 기반 "
        "구간을 논의할 여지가 있다.".format(r))
    out["caveat"] = (
        "σ 는 **고주파** 성분만 잡는다. 드리프트·오프셋 같은 저주파 측정오차는 "
        "이 방법으로 안 잡히므로 σ 는 **하한**이고 따라서 misfit/σ 는 **상한**이다. "
        "잡음이 상관돼 있으면 k=1 의 σ 는 더 작게 나오므로 스캔이 평평해지는 "
        "값을 쓴다.")
    print(json.dumps(out, ensure_ascii=False, indent=2, default=float))



def main(argv=None):
    ap = argparse.ArgumentParser(prog="bms_balancing.verify")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("port", cmd_port), ("degeneracy", cmd_degeneracy),
                     ("scale-noise", cmd_scale_noise), ("matrix", cmd_matrix),
                     ("profile", cmd_profile), ("eval", cmd_eval),
                     ("noise", cmd_noise)):
        p = sub.add_parser(name)
        p.add_argument("--data-root", default=None)
        p.add_argument("--source", default="GITT", choices=list(D.HALF_FILE))
        p.add_argument("--state", default="pristine", choices=D.STATES)
        p.add_argument("--si-source", default="Li", choices=D.SI_SOURCES)
        p.add_argument("--w-dqdv", type=float, default=0.0)
        p.add_argument("--starts", type=int, default=24)
        p.add_argument("--seed", type=int, default=0)
        p.add_argument("--samples", type=int, default=400)
        p.add_argument("--tol", type=float, default=0.01)
        p.add_argument("--repeats", type=int, default=5)
        p.add_argument("--out", default=None)
        p.add_argument("--only-source", action="store_true")
        p.add_argument("--only-wdqdv", action="store_true")
        p.add_argument("--grid", type=int, default=21)
        p.add_argument("--blind", action="store_true",
                       help="port: 보고값을 시작점에서 뺀다 (독립 재적합)")
        p.add_argument("--profile-scale", choices=["global", "per-gamma"],
                       default="global",
                       help="profile: 목적함수 scale 을 전역 경계에서 한 번 "
                            "뽑을지(기본 — 원 파이프라인과 같다), γ 를 묶은 "
                            "경계에서 행마다 다시 뽑을지. per-gamma 는 그들 "
                            "절차가 아니라 dd_verify.m profile 모드의 부작용을 "
                            "재현하는 진단용이다 (행끼리 비교 불가)")
        p.add_argument("--compare", default=None,
                       help="dd_eval.m 이 낸 CSV 와 대조한다 (eval 전용). 종료 코드: 0 complete · "
                            "1 갈림 · 2 미완 · 3 부분(옛 스키마)")
        p.add_argument("--precision", default="auto",
                       help="eval --compare: CSV 의 출력 정밀도. auto(파일의 `# printed_format` 선언 → "
                            "없으면 자리수 추정 = partial) | g17 | full | fixed:N | sig:N. 옵션이 선언보다 "
                            "느슨하면 complete 가 아니다")
        p.add_argument("--run-id", default=None,
                       help="이번 시도의 식별자 — 산출물(degeneracy JSON · matrix/profile 행)에 박힌다. "
                            "없으면 환경 BMS_RUN_ID(run_states.sh 가 준다) → 새 uuid")
        p.add_argument("--allow-partial", action="store_true",
                       help="eval --compare: 옛 스키마(앵커·열 누락)의 부분 대조를 종료 코드 0 으로 "
                            "허용한다 — 판정문에는 그대로 '부분' 이 남는다")
        p.set_defaults(func=fn)
    args = ap.parse_args(argv)
    args.run_id = run_id_of(args)                    # R5-08: 이 명령의 시도 식별자는 하나다 (행·JSON·로그 공통)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
