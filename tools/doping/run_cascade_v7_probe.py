#!/usr/bin/env python3
"""run_cascade_v7_probe.py — cascade 카드 v7 + 개정 CP **탐침** 러너 (비준 2026-10-03 · 실행 승인 2026-10-03 사용자 '지금 kgy에서 돌리자').

    python3 tools/doping/run_cascade_v7_probe.py --selftest
    python3 tools/doping/run_cascade_v7_probe.py --dry_run \
        --out_root ~/work/runs/cascade_v7_probe_1003 \
        --prep_root ~/work/runs/cascade_v6_40run_0921 \
        --python /home/kgy/apps/miniforge3/envs/uma/bin/python
    (실행)   같은 명령에서 --dry_run 만 뺀다 — tmux 안에서.  이어받기는 --resume.
    (감시)   … --status --out_root <같은 경로>          (읽기만 · D 안 찍음)

무엇을 하나
  · 한 번에 런 하나. **매 런 전에 판독기**(`judge_eprime.py --probe <out_root>`)를 부르고, 그 산출물
    `cascade_v7_probe.json` 의 `next` (T, 구조, 시드) 하나만 돌린다.
    ⇒ 다음 런을 고르는 규칙(그 온도의 계획 6 런이 전부 통과해야 T* · 하나라도 불통과면 다음 사다리 ·
       부모 교체 없음 · 계획 밖 런은 안 센다)은 **판독기 한 곳에만** 있다 (`select_probe_temperature`).
       러너가 순서를 따로 들고 있으면 규칙이 두 곳이 되고 두 판정이 갈린다 — 그래서 러너는 고르지 않는다.
  · `T_star_K` 가 나오거나 사다리가 다 떨어지면(next 없음) **멈춘다**.
    ⛔ 본 라운드 40 런을 이어서 띄우지 않는다 (회신 CP P0-3 · 개정 §7 — 본 라운드 상한 비준이 먼저다).
  · 프로토콜은 **판독기 상수**에서 온다 (V7_PROTOCOL · V7_LADDER_K · V7_PROBE_PLAN = 400 ps · dt 2 fs · save 100 fs).
    평형 5 ps · friction 0.02 · 창 2–50 ps · UMA-s-1p1(omat) **default** 는 v6 러너 상수 그대로 (개정 §5).
    태그 = `<구조>__T<T>__s<시드>` (개정 ⑥) · 드라이버 `--seed` = 그 시드 (탐침 쌍은 3·4).
  · 준비 구조는 v6 prep 을 **초기 좌표로만** 재사용한다 (개정 ⑩). 원본 기록(수렴 · 해시 · 입력 해시 ·
    공통 셀)을 검사하고 out_root/prep 에 **복사**해 해시를 박은 뒤 그 사본만 쓴다.
  · 상한은 원장에서 읽는다 — 결정 D-2026-10-03-cascade-v7-amend-cp 의 `cost_cap.total_gpu_h` (141).
    두 결정(카드 · 개정)이 `active` 가 아니면 시작하지 않는다.
  · 드라이버는 기존 것(`tools/modelc_v3/disorder_ensemble_diffusion.py`)을 `--disorder_levels 0.0 --n_configs 1
    --save_traj` 로 부른다 — 새 MD 코드를 쓰지 않는다. 런마다 run_meta(설정) · 추론 모드 · md.log dt 를 보고
    어긋나면 **우리 런만** (PID 트리로) 죽이고 멈춘다.

비용 게이트 (개정 §4 · 결정 cost_cap '넘으면 멈추고 보고한다')
  · 런 시작 전: 누적 + 단가 > 상한이면 그 런을 띄우지 않고 멈춘다. 단가 = 끝난 런 실측의 **최댓값**
    (아직 없으면 추정 11.8 GPU-h). 실패·중단한 런의 시간도 누적에 들어간다.
  ⚠ 12 런 × 11.8 = 141.6 > 141 — 단가가 11.75 GPU-h 를 넘으면 계획의 12 번째 런(1000 K 마지막)은 이 게이트에서
    멈추고 보고한다 (그때 상한을 다시 비준한다). 상한을 코드에서 올리지 않는다.

GPU (kgy — 점착 P1b pw.x 와 공유 · 사용자 실행 승인 2026-10-03)
  · 시작 문턱만 있다: nvidia-smi 합계 ≤ --gpu_start_max_mib (기본 16000) 일 때만 띄운다. P1b 기록 피크
    13.8 GB + 출처 모를 잡 0.8 GB 보다 많으면 제3의 잡이 있다는 뜻이라 기다린다 (--gpu_wait_s 넘으면 멈춤).
    못 읽음은 '비어 있음' 이 아니다 — 기다리고, 넘으면 멈춘다.
  · 런 중에는 합계를 gpu_log.tsv 에 남기기만 한다.

멈춤 코드
  0  탐침 규칙상 끝 (T* 확정 또는 사다리 소진 — 산출물 cascade_v7_probe.json 이 말한다) · dry_run · status
  2  사전점검 불통과 (결정 · 상수 · 준비 입력 · 드라이버 · python · 판독기 selftest · 작업트리 · 이어받기 규약)
  3  비용 게이트 (상한)
  4  런이 rc ≠ 0 이거나 산출물(msd · aimd_results · traj · 프레임 수)이 모자라게 끝남
  5  판독기 실패 · 산출물이 러너 상수와 다름 · D 가 섞임 · '확인 못 함' 표지(오류 · 골격 경보 못 잼)
  6  판독기와 디스크가 어긋남 (next 가 이미 끝난 런) · 이번 실행 런 수가 계획 최대를 넘음
  9  런 설정 불일치 (run_meta · 추론 모드 · md.log dt) — 우리 런만 죽였다
  10 이미 실행 중 (잠금)
  11 새 시작인데 out_root 가 비어 있지 않음 · 또는 next 런 폴더가 msd.json 없이 남아 있음 (끊긴 런)
  12 GPU 대기 초과 · 디스크 부족
  130 사람이 중단 (SIGINT · SIGTERM · SIGHUP) — 돌던 우리 런을 죽이고 시간을 누적에 남겼다

⛔ 이 러너가 **못 하는 것 / 안 하는 것**
  · 다음 런을 고르지 않는다 — 판독기가 고른다. 판독기가 틀리면 러너도 따라 틀린다.
  · D 를 보지도 찍지도 않는다. ⚠ 드라이버는 런 끝에 D 를 stdout 에 찍는다 → 그 출력은 `logs/<태그>.log` 로만 가고
    러너 화면에는 안 나온다. **그 로그를 tail 하지 않는다** (감시는 --status 나 md.log 의 시간·온도만).
  · 프로세스별 VRAM 가드가 없다 (kgy 는 nvidia-smi 프로세스 정보가 막혀 있다) — 합계 기준 시작 문턱뿐이다.
    넘치면 P1b 러너(`run_sese_gpu.sh` KILL_MIB 23000)가 **자기 잡을** 멈춘다 — 탐침 쪽은 안 멈춘다.
  · 끊긴 런을 이어 돌리지 않는다 — 사람이 흔적을 `<out_root>/attic/` 로 옮기고 --resume 한다. 그때도 **같은
    (T, 구조, 시드)** 만 다시 돈다 (대체가 아니라 인프라 재시도다).
  · '확인 못 함' 표지(판독기 오류 · 골격 경보 unavailable)가 뜨면 판독기의 다음 지시를 따르지 않고 멈춘다 —
    카드상 그 런은 자격 없음이 맞지만, 못 잰 것 때문에 사다리를 넘기기 전에 사람이 본다.
    `--accept_flagged <태그>` 로 그 런을 명시적으로 받아들이면 (budget.json 에 남는다) 판독기 지시대로 간다.
  · md.log 의 실제 온도는 **기록만** 한다 (생산 구간 평균·표준편차) — 문턱은 카드가 정하지 않았다.
  · 준비 구조가 그 온도에서 평형이라는 보장을 안 한다 · 5 ps 평형화의 충분성을 검사하지 않는다 (개정 ⑩).
  · 본 라운드를 띄우지 않는다 · 원자료를 repo 로 옮기지 않는다 (결정 record = db/raw/cascade_v7_probe/ — 사람이 한다).
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import random
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
import judge_eprime as J                     # noqa: E402  프로토콜·사다리·계획·태그 규칙의 정본
import run_eprime_pilot as R                 # noqa: E402  v6 동결값 (평형·friction·창·UMA·드라이버·공통 셀)

DECISIONS = REPO / "db" / "governance" / "decisions.json"
DECISION_CARD = "D-2026-10-01-cascade-v7-probe-card"
DECISION_AMEND = "D-2026-10-03-cascade-v7-amend-cp"
CARD = "db/properties/cascade_estimand_card_v7_probe_2026_10_01.json"
AMENDMENT = "db/properties/cascade_estimand_card_v7_probe_amendment_cp_2026_10_03.json"
JUDGE = HERE / "judge_eprime.py"

PROD_PS = float(J.V7_PROTOCOL["prod_ps"])
DT_FS = float(J.V7_PROTOCOL["dt_fs"])
SAVE_FS = float(J.V7_PROTOCOL["save_fs"])
LADDER = tuple(int(t) for t in J.V7_LADDER_K)
PLAN = tuple((str(s), int(sd)) for s, sd in J.V7_PROBE_PLAN)
PAIR_PARENT = J.V7_PAIR_PARENT
PROBE_STRUCTURES = tuple(dict.fromkeys(s for s, _ in PLAN))
MAX_RUNS = len(LADDER) * len(PLAN)
UMA_MODE = "default"                         # 카드 §2b — turbo 와 섞지 않는다

#: 개정 §4 — v6 실측 5.89 GPU-h/런(200 ps) × 2. 실측이 생기면 그 **최댓값**이 이걸 대신한다.
EST_GPU_H_PER_RUN = 11.8
#: 개정 §3 — 대표 부모 추첨 (결과 전). 상수가 바뀌었는지 여기서도 재현해 본다.
PARENT_DRAW_SEED, PARENT_DRAW_POOL = 20261003, ("C", "D", "E", "F", "G", "H", "I", "J")
#: 사전점검에서 --python 으로 불러 보는 모듈 (드라이버·판독기가 쓴다)
ENV_IMPORTS = ("fairchem.core", "ase", "numpy")
NVSMI_ARGS = ("--query-gpu=memory.used", "--format=csv,noheader,nounits", "-i", "0")
SUBDIR = "d0.00_cfg0"                        # 드라이버 d=0 · cfg0 폴더 (판독기 scan 의 md/<태그>/<sub>/T<T>/)


class _Stop(Exception):
    """SIGTERM·SIGHUP → 정리 경로 (돌던 우리 런을 죽이고 시간을 남긴다)."""


def _on_signal(signum, _frame):
    raise _Stop(signal.Signals(signum).name)


def ts() -> str:
    return time.strftime("%F %T")


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def say(msg: str) -> None:
    print(f"[{ts()}] {msg}", flush=True)


def tag_of(T, structure, seed) -> str:
    return f"{structure}__T{int(T)}__s{int(seed)}"


def frozen_now() -> dict:
    """이 탐침이 얼려 둔 규약. 이어받기는 이게 같을 때만 된다."""
    return {"prod_ps": PROD_PS, "dt_fs": DT_FS, "save_fs": SAVE_FS,
            "equilib_ps": R.EQUILIB_PS, "friction": R.FRICTION,
            "fit_window_ps": list(R.FIT_WINDOW_PS),
            "uma": {"model": R.UMA_MODEL, "task": R.UMA_TASK, "mode": UMA_MODE},
            "ladder_K": list(LADDER), "plan": [list(x) for x in PLAN],
            "pair_parent": PAIR_PARENT, "V_common_A3": R.V_COMMON_A3,
            "cell_diag": list(R.CELL_DIAG)}


# ── 순수 검사 (selftest 가 직접 부른다) ─────────────────────────────────────────
def _eq(got, want) -> bool:
    """기록값 대조. bool 은 bool 로만 (1 ≠ True) · 수는 상대 1e-6 · 목록은 원소마다."""
    if isinstance(want, bool):
        return isinstance(got, bool) and got == want
    if isinstance(want, (int, float)):
        return isinstance(got, (int, float)) and not isinstance(got, bool) and J._same(got, want)
    if isinstance(want, (list, tuple)):
        return (isinstance(got, (list, tuple)) and len(got) == len(want)
                and all(_eq(g, w) for g, w in zip(got, want)))
    return got == want


def constant_errors(plan=PLAN, ladder=LADDER, pair=PAIR_PARENT, roster=None) -> list[str]:
    """판독기·v6 러너·개정 문서 사이의 상수가 서로 맞는가. 하나라도 어긋나면 시작하지 않는다."""
    errs = []
    if not J._same(DT_FS, R.DT_FS) or not J._same(SAVE_FS, R.SAVE_FS):
        errs.append(f"dt/save {DT_FS}/{SAVE_FS} ≠ v6 동결 {R.DT_FS}/{R.SAVE_FS} (개정 §5 '바꾸지 않는 것')")
    if list(ladder) != sorted(ladder) or len(set(ladder)) != len(ladder):
        errs.append(f"사다리 {list(ladder)} 가 오름차순·고유가 아니다")
    draw = random.Random(PARENT_DRAW_SEED).choice(list(PARENT_DRAW_POOL))
    if draw != pair:
        errs.append(f"대표 부모 {pair!r} ≠ 개정 §3 추첨 재현 {draw!r}")
    want = [("H0_host", 1), ("H0_host", 2), (f"P1_Al2O3_{pair}", 3), (f"P2_Al2S3_{pair}", 3),
            (f"P1_Al2O3_{pair}", 4), (f"P2_Al2S3_{pair}", 4)]
    if [tuple(x) for x in plan] != want:
        errs.append(f"계획 {list(plan)} ≠ 개정 ③ 순서 {want}")
    roster = R.MD_STRUCTURES if roster is None else roster
    for s in {s for s, _ in plan if s != R.HOST_STRUCTURE}:
        if s not in roster:
            errs.append(f"{s} 가 v6 부모 census 에 없다")
    for s, sd in plan:
        t = tag_of(ladder[0], s, sd)
        if J.parse_tag(t) != (s, sd) or J._TAG_T.search(t) is None:
            errs.append(f"태그 {t} 를 판독기가 못 읽는다 (개정 ⑥)")
    return errs


def decision_gate(path) -> tuple[float | None, list[str]]:
    """원장에서 두 결정이 active 인지 · 탐침 상한 → (상한, 오류)."""
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        items = d["decisions"] if isinstance(d, dict) else d
    except (OSError, ValueError, KeyError, TypeError) as e:
        return None, [f"결정 원장을 못 읽는다 ({path}: {type(e).__name__})"]
    by = {e.get("id"): e for e in items if isinstance(e, dict)}
    errs, cap = [], None
    for did in (DECISION_CARD, DECISION_AMEND):
        e = by.get(did)
        if e is None:
            errs.append(f"{did} 가 원장에 없다")
        elif e.get("decision_state") != "active":
            errs.append(f"{did} 가 active 가 아니다 ({e.get('decision_state')!r})")
    try:
        cap = float(by[DECISION_AMEND]["cost_cap"]["total_gpu_h"])
        if not cap > 0:
            raise ValueError
    except (KeyError, TypeError, ValueError):
        cap = None
        errs.append(f"{DECISION_AMEND} 의 cost_cap.total_gpu_h 를 못 읽는다")
    return cap, errs


def budget_gate(used, measured, cap, est=EST_GPU_H_PER_RUN) -> tuple[bool, str, float]:
    """다음 런을 시작해도 되나 → (ok, 사유, 쓴 단가). 단가 = 실측 최댓값 (없으면 추정)."""
    unit = max(measured) if measured else est
    src = "실측 최댓값" if measured else "추정"
    if used >= cap:
        return False, f"⛔ 누적 {used:.2f} ≥ 상한 {cap:g} GPU-h — 멈추고 보고 (개정 §4)", unit
    if used + unit > cap:
        return False, (f"⛔ 누적 {used:.2f} + 단가 {unit:.2f} ({src}) = {used + unit:.2f} > 상한 {cap:g} GPU-h — "
                       f"다음 런을 시작하지 않는다 (개정 §4 · 상한 재비준이 필요하다)"), unit
    return True, f"누적 {used:.2f} + 단가 {unit:.2f} ({src}) ≤ 상한 {cap:g}", unit


def meta_expect(T, structure, seed, v0, n_atoms) -> dict:
    return {"label": f"cv7probe_{structure}", "n_atoms": int(n_atoms), "supercell": [1, 1, 1],
            "v0_xyz": str(v0), "temperatures": [float(T)], "prod_ps": PROD_PS,
            "equilib_ps": R.EQUILIB_PS, "seed": int(seed), "fit_window_ps": list(R.FIT_WINDOW_PS),
            "save_traj": True, "uma_model": R.UMA_MODEL, "uma_inference_mode_requested": UMA_MODE}


def meta_errors(meta, exp) -> list[str]:
    if not isinstance(meta, dict):
        return ["run_meta.json 이 dict 가 아니다"]
    return [f"{k}: {meta.get(k)!r} ≠ {v!r}" for k, v in exp.items() if not _eq(meta.get(k), v)]


def md_cmd(py, driver, v0, out_dir, T, structure, seed, device) -> list[str]:
    return [str(py), str(driver),
            "--v0_xyz", str(v0), "--label", f"cv7probe_{structure}", "--out_root", str(out_dir),
            "--disorder_levels", "0.0", "--n_configs", "1",
            "--temperatures", str(int(T)),
            "--equilib_ps", str(R.EQUILIB_PS), "--prod_ps", str(PROD_PS),
            "--timestep_fs", str(DT_FS), "--friction", str(R.FRICTION),
            "--save_fs", str(SAVE_FS),
            "--fit_window_ps", str(R.FIT_WINDOW_PS[0]), str(R.FIT_WINDOW_PS[1]),
            "--save_traj",                   # 자격 게이트의 사건 수·카드 정의 곡선은 궤적에서 나온다 (v6 러너 GATE_INPUT_FLAGS)
            "--seed", str(int(seed)),
            "--uma_model", R.UMA_MODEL, "--uma_task", R.UMA_TASK,
            "--device", device]


def expected_frames() -> int:
    return int(round(PROD_PS * 1000.0 / SAVE_FS))


def _mdlog_rows(path):
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            p = line.split()
            if len(p) < 2:
                continue
            try:
                yield float(p[0]), float(p[-1])
            except ValueError:
                continue                    # 머리줄


def mdlog_dt_ps(path) -> float | None:
    """md.log 첫 두 데이터 줄의 시간 차 (ps). 두 줄이 없으면 None — '못 봄' 이지 통과가 아니다."""
    try:
        rows = []
        for t, _ in _mdlog_rows(path):
            rows.append(t)
            if len(rows) == 2:
                return rows[1] - rows[0]
    except OSError:
        return None
    return None


def dt_matches(dt_ps) -> bool:
    """md.log 시간 간격이 dt 와 같은가. md.log 는 시간을 소수 4 자리(0.0020)로 찍으므로 그 반 자리(5e-5 ps)로 본다.

    ⛔ `judge_eprime._same` 을 쓰지 않는다 — 허용오차가 `rel × max(1, |b|)` 라 |b| < 1 에서 **절대 1e-3** 이 되고,
       rel=1e-3 이면 0.001 ps 와 0.002 ps 를 같다고 한다 (2026-10-03 이 러너 selftest 음성 시험이 잡았다).
    """
    return dt_ps is not None and abs(dt_ps - DT_FS / 1000.0) <= 5e-5


def mdlog_tail(path) -> tuple[float, float] | None:
    """md.log 마지막 데이터 줄 (시간 ps, 온도 K) — 진행 표시용."""
    try:
        with open(path, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            fh.seek(max(0, fh.tell() - 4096))
            lines = fh.read().decode("utf-8", "ignore").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        p = line.split()
        try:
            return float(p[0]), float(p[-1])
        except (ValueError, IndexError):
            continue
    return None


def mdlog_T_stats(path, t_from_ps) -> dict | None:
    """생산 구간(시간 > 평형) 온도 평균·표준편차 — **기록만** (문턱 없음)."""
    n, s, ss = 0, 0.0, 0.0
    try:
        for t, T in _mdlog_rows(path):
            if t > t_from_ps:
                n += 1; s += T; ss += T * T
    except OSError:
        return None
    if n == 0:
        return None
    m = s / n
    return {"n": n, "mean_K": round(m, 2), "sd_K": round(max(ss / n - m * m, 0.0) ** 0.5, 2)}


def post_run_errors(run_dir, T) -> list[str]:
    """런이 rc 0 으로 끝난 뒤 산출물 검사. ⛔ msd.json 의 D 는 읽지 않는다."""
    d = Path(run_dir)
    errs = [f"{n} 가 없다" for n in ("msd.json", "aimd_results.json", "traj.xyz") if not (d / n).is_file()]
    try:
        a = json.loads((d / "aimd_results.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return errs or ["aimd_results.json 을 못 읽는다"]
    want = {"T_K": float(T), "prod_ps": PROD_PS, "dt_fs": DT_FS, "save_fs": SAVE_FS, "n_frames": expected_frames()}
    errs += [f"aimd_results {k} {a.get(k)!r} ≠ {v!r}" for k, v in want.items() if not _eq(a.get(k), v)]
    return errs


def judge_output_errors(d) -> list[str]:
    """판독기 산출물이 이 러너의 상수와 같은 규칙으로 나왔는가 · D 가 섞이지 않았는가."""
    if not isinstance(d, dict):
        return ["산출물이 dict 가 아니다"]
    errs = []
    try:
        if [int(x) for x in d.get("ladder_K") or []] != list(LADDER):
            errs.append(f"ladder_K {d.get('ladder_K')} ≠ {list(LADDER)}")
    except (TypeError, ValueError):
        errs.append("ladder_K 를 못 읽는다")
    proto = d.get("protocol") or {}
    for k, v in J.V7_PROTOCOL.items():
        if not (isinstance(proto, dict) and k in proto and J._same(proto[k], v)):
            errs.append(f"protocol.{k} {proto.get(k) if isinstance(proto, dict) else proto!r} ≠ {v}")
    if d.get("pair_parent") != PAIR_PARENT:
        errs.append(f"pair_parent {d.get('pair_parent')!r} ≠ {PAIR_PARENT!r}")
    try:
        if [(str(x[0]), int(x[1])) for x in d.get("plan") or []] != list(PLAN):
            errs.append("plan 이 러너 계획과 다르다")
    except (TypeError, ValueError, IndexError):
        errs.append("plan 을 못 읽는다")
    nxt, Ts = d.get("next"), d.get("T_star_K")
    if nxt is not None:
        try:
            T, s, sd = int(nxt[0]), str(nxt[1]), int(nxt[2])
        except (TypeError, ValueError, IndexError):
            errs.append(f"next 형식 {nxt!r}")
        else:
            if T not in LADDER:
                errs.append(f"next 온도 {T} K 가 사다리 밖이다")
            if (s, sd) not in PLAN:
                errs.append(f"next ({s}, 시드 {sd}) 가 계획 밖이다 — 대체 금지")
    if Ts is not None:
        if nxt is not None:
            errs.append("T* 와 next 가 같이 있다")
        try:
            if int(Ts) not in LADDER:
                errs.append(f"T* {Ts} 가 사다리 밖이다")
        except (TypeError, ValueError):
            errs.append(f"T* 형식 {Ts!r}")
    for r in d.get("runs") or []:
        if isinstance(r, dict) and any(k == "D" or str(k).startswith("D_") for k in r):
            errs.append(f"runs[{r.get('tag')}] 에 D 키가 있다 — 봉인 위반 (값은 찍지 않는다)")
    return errs


def infra_flags(d, accepted=()) -> list[tuple[str, list[str]]]:
    """'확인 못 함' 표지 — 판독기 오류 · 골격 경보 unavailable. 받아들인 태그는 뺀다."""
    out = []
    for r in (d or {}).get("runs") or []:
        if not isinstance(r, dict):
            continue
        why = []
        if r.get("error"):
            why.append(f"오류: {r['error']}")
        fa = str(r.get("framework_alarm") or "")
        if fa.startswith("unavailable"):
            why.append(f"골격 경보 못 잼 ({fa})")
        if why and r.get("tag") not in set(accepted):
            out.append((str(r.get("tag")), why))
    return out


def prep_check(prep_root, struct_dir, structures=PROBE_STRUCTURES) -> tuple[dict, list[str]]:
    """v6 준비 기록 → {구조: 사실}, 오류. 수렴 · 사본 해시 · 입력 해시(repo 구조) · 공통 셀 · 원자 수."""
    rows, errs = {}, []
    for s in structures:
        j = Path(prep_root) / "prep" / f"{s}.prepared.json"
        x = Path(prep_root) / "prep" / f"{s}.prepared.xyz"
        src = Path(struct_dir) / f"{s}.xyz"
        try:
            rec = json.loads(j.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            errs.append(f"{s}: 준비 기록을 못 읽는다 ({j}: {type(e).__name__})")
            continue
        if rec.get("structure") != s:
            errs.append(f"{s}: 기록의 structure {rec.get('structure')!r}")
        if rec.get("converged") is not True:
            errs.append(f"{s}: 준비 미수렴 (converged {rec.get('converged')!r}) — 그 구조로 탐침을 돌리지 않는다")
        if not x.is_file():
            errs.append(f"{s}: {x} 가 없다")
            continue
        sha = R.sha256(x)
        if sha != rec.get("prepared_sha256"):
            errs.append(f"{s}: prepared.xyz 해시 {sha[:16]} ≠ 기록 {str(rec.get('prepared_sha256'))[:16]}")
        if not src.is_file():
            errs.append(f"{s}: repo 구조 {src} 가 없다")
        elif R.sha256(src) != rec.get("input_sha256"):
            errs.append(f"{s}: 준비의 입력 해시가 repo 구조({src.name})와 다르다 — 다른 구조에서 준비됐다")
        try:
            A, n = R.read_cell(x)
        except ValueError as e:
            errs.append(f"{s}: {e}")
            continue
        V = abs(R.det3(A))
        off = max(abs(A[i][k]) for i in range(3) for k in range(3) if i != k)
        diag = max(abs(A[i][i] - R.CELL_DIAG[i]) for i in range(3))
        if abs(V - R.V_COMMON_A3) > R.V_TOL_A3 or off > R.CELL_TOL_A or diag > 1e-6:
            errs.append(f"{s}: 셀이 공통 셀이 아니다 (V {V:.6f} · 비대각 {off:.1e} · 대각 오차 {diag:.1e})")
        if rec.get("n_atoms") is not None and int(rec["n_atoms"]) != n:
            errs.append(f"{s}: 원자 수 {n} ≠ 기록 {rec['n_atoms']}")
        rows[s] = {"source_json": str(j), "source_xyz": str(x), "sha256": sha,
                   "input_sha256": rec.get("input_sha256"), "n_atoms": n, "V_A3": V,
                   "final_fmax_eV_A": rec.get("final_fmax_eV_A"), "converged": rec.get("converged")}
    return rows, errs


def git_state(repo) -> tuple[str, bool | None]:
    """(HEAD, 추적 파일이 바뀌었나). 못 읽으면 ('', None)."""
    try:
        head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=60)
        st = subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=no"],
                            capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return "", None
    if head.returncode or st.returncode:
        return "", None
    return head.stdout.strip(), bool(st.stdout.strip())


def python_env_errors(py) -> list[str]:
    code = "import " + ", ".join(ENV_IMPORTS) + "; print('env-ok')"
    try:
        r = subprocess.run([str(py), "-c", code], capture_output=True, text=True, timeout=900)
    except (OSError, subprocess.TimeoutExpired) as e:
        return [f"{py} 를 못 돌렸다 ({type(e).__name__})"]
    if r.returncode != 0 or "env-ok" not in r.stdout:
        tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or ["?"]
        return [f"{py} 에서 {', '.join(ENV_IMPORTS)} import 실패 — {tail[0][:160]} "
                f"(base python 이면 fairchem 이 없다 · uma env 절대경로를 준다)"]
    return []


def judge_selftest_errors(py, judge) -> tuple[list[str], str]:
    try:
        r = subprocess.run([str(py), str(judge), "--selftest"], capture_output=True, text=True, timeout=1800)
    except (OSError, subprocess.TimeoutExpired) as e:
        return [f"판독기 selftest 를 못 돌렸다 ({type(e).__name__})"], ""
    tail = "\n".join((r.stdout or "").strip().splitlines()[-2:])
    if r.returncode != 0 or "selftest PASS" not in (r.stdout or ""):
        return [f"판독기 selftest 불통과 (rc {r.returncode}) — 이 python 에서 판정을 믿을 수 없다: {tail[-200:]}"], tail
    return [], tail


def gpu_total_mib(nvsmi) -> int | None:
    try:
        r = subprocess.run([str(nvsmi), *NVSMI_ARGS], capture_output=True, text=True, timeout=60)
        return int(r.stdout.strip().splitlines()[0].strip()) if r.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired, ValueError, IndexError):
        return None


def wait_gpu(nvsmi, max_mib, wait_s, poll_s) -> tuple[bool, int | None, float]:
    """합계 ≤ max_mib 일 때까지 기다린다 → (ok, 마지막 합계, 기다린 초). 못 읽음은 통과가 아니다."""
    t0, said = time.time(), False
    while True:
        tot = gpu_total_mib(nvsmi)
        if tot is not None and tot <= max_mib:
            return True, tot, time.time() - t0
        if time.time() - t0 >= wait_s:
            return False, tot, time.time() - t0
        if not said:
            say(f"⏳ GPU 합계 {tot if tot is not None else '못 읽음'} MiB > 시작 문턱 {max_mib} — 기다린다 "
                f"(최대 {wait_s / 3600:.1f} h)")
            said = True
        time.sleep(poll_s)


# ── 프로세스 — 우리 런만, PID 트리로 ─────────────────────────────────────────
def _stat(pid):
    """(ppid, starttime) — 못 읽으면 None."""
    try:
        f = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        return int(f[1]), int(f[19])
    except (OSError, IndexError, ValueError):
        return None


def tree_of(pid) -> list[tuple[int, int]]:
    """pid 와 그 자손 → [(pid, starttime)]. starttime 을 같이 잡아 PID 재사용에 안 속는다."""
    kids = {}
    for d in Path("/proc").iterdir():
        if d.name.isdigit():
            st = _stat(int(d.name))
            if st:
                kids.setdefault(st[0], []).append((int(d.name), st[1]))
    root = _stat(pid)
    out, stack = ([(pid, root[1])] if root else []), [pid]
    while stack:
        for c in kids.get(stack.pop(), []):
            out.append(c); stack.append(c[0])
    return out


def kill_tree(proc, grace=10.0) -> None:
    tree = tree_of(proc.pid)
    for p, _ in tree:
        try:
            os.kill(p, signal.SIGTERM)
        except ProcessLookupError:
            pass
    try:
        proc.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        pass
    for p, st0 in tree:
        cur = _stat(p)
        if cur and cur[1] == st0:
            try:
                os.kill(p, signal.SIGKILL)
            except ProcessLookupError:
                pass
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        pass


def take_lock(out_root):
    fd = os.open(str(Path(out_root) / ".runner.lock"), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(fd)
        return None
    os.ftruncate(fd, 0)
    os.write(fd, f"{os.getpid()}\n".encode())
    return fd


def _read_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _write_json(p, obj) -> None:
    tmp = Path(str(p) + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, p)


# ── 판독기 ───────────────────────────────────────────────────────────────────
def judge_once(py, judge, out_root, timeout_s=7200) -> tuple[dict | None, str]:
    pj = Path(out_root) / "cascade_v7_probe.json"
    pj.unlink(missing_ok=True)               # 낡은 산출물을 새 판정으로 읽지 않는다
    with open(Path(out_root) / "judge_probe.log", "a", encoding="utf-8") as fh:
        fh.write(f"\n===== {utc()} judge --probe =====\n")
        fh.flush()
        try:
            r = subprocess.run([str(py), str(judge), "--probe", str(out_root)],
                               stdout=fh, stderr=subprocess.STDOUT, timeout=timeout_s)
        except subprocess.TimeoutExpired:
            return None, f"판독기가 {timeout_s:.0f} s 안에 안 끝났다"
    if r.returncode != 0:
        return None, f"판독기 rc={r.returncode} (judge_probe.log)"
    d = _read_json(pj)
    if d is None:
        return None, "판독기가 cascade_v7_probe.json 을 안 남겼거나 못 읽는다"
    errs = judge_output_errors(d)
    if errs:
        return None, "산출물이 러너 상수와 다르다 — " + " · ".join(errs)
    return d, "ok"


def show_judge(d) -> None:
    """판독기 결과를 화면에 — 자격 · 골격 · 부창비 · 사건 · 오류만 (D 는 산출물에 없고 여기서도 안 찍는다)."""
    for r in d.get("runs") or []:
        ratios = [round(float(x), 2) for x in (r.get("sub_window_ratios") or []) if isinstance(x, (int, float))]
        print(f"     {r.get('T_K')} K {r.get('structure')} s{r.get('seed')}: "
              f"자격 {'통과' if r.get('eligible') else '미달'} · 골격 {r.get('framework_alarm', '—')} · "
              f"부창비 {ratios} · 사건 {r.get('events', '—')}"
              + (f" · ⛔ {r['error']}" if r.get("error") else ""), flush=True)
    nxt = d.get("next")
    print(f"     → {d.get('why')}" + (f" · 다음 {nxt[0]} K {nxt[1]} s{nxt[2]}" if nxt else ""), flush=True)


# ── 한 런 ────────────────────────────────────────────────────────────────────
def run_one(ctx, budget, T, s, seed) -> int:
    out_root = ctx["out_root"]
    tag = tag_of(T, s, seed)
    root = out_root / "md" / tag
    rdir = root / SUBDIR / f"T{int(T)}"
    if root.exists():
        if (rdir / "msd.json").exists():
            say(f"⛔ 판독기가 이미 끝난 런 {tag} 을 다음으로 지목했다 — 판독기와 디스크가 어긋난다 (rc 6)")
            return 6
        say(f"⛔ {tag} 폴더가 msd.json 없이 남아 있다 (끊긴 런) — 이어 돌리지 않는다. 흔적을 옮긴 뒤 --resume:\n"
            f"     mkdir -p {out_root}/attic && mv {root} {out_root}/attic/{tag}.$(date +%Y%m%d_%H%M%S)")
        return 11
    v0 = out_root / "prep" / f"{s}.prepared.xyz"
    if not v0.is_file() or R.sha256(v0) != ctx["prep"][s]["sha256"]:
        say(f"⛔ 준비 사본 {v0} 가 없거나 해시가 바뀌었다 — 시작하지 않는다 (rc 2)")
        return 2
    if R.sha256(ctx["driver"]) != ctx["driver_sha256"]:
        say("⛔ 드라이버 해시가 manifest 와 다르다 — 탐침 도중 코드가 바뀌었다 (rc 2)")
        return 2
    ok, tot, waited = wait_gpu(ctx["nvsmi"], ctx["gpu_start_max_mib"], ctx["gpu_wait_s"], ctx["poll_s"])
    if not ok:
        say(f"⛔ GPU 합계 {tot if tot is not None else '못 읽음'} MiB 가 {waited / 3600:.2f} h 동안 시작 문턱 "
            f"{ctx['gpu_start_max_mib']} 을 안 내려왔다 — 멈춘다 (rc 12)")
        return 12
    free_gb = shutil.disk_usage(out_root).free / 1e9
    if free_gb < ctx["disk_min_gb"]:
        say(f"⛔ 디스크 여유 {free_gb:.1f} GB < {ctx['disk_min_gb']} GB — 멈춘다 (rc 12)")
        return 12
    cmd = md_cmd(ctx["python"], ctx["driver"], v0, root, T, s, seed, ctx["device"])
    exp = meta_expect(T, s, seed, v0, ctx["prep"][s]["n_atoms"])
    step = {"tag": tag, "T_K": int(T), "structure": s, "seed": int(seed), "start_utc": utc(),
            "gpu_total_mib_at_start": tot, "gpu_wait_s": round(waited, 1), "disk_free_gb_at_start": round(free_gb, 1),
            "cmd": cmd}
    budget["steps"].append(step)
    _write_json(ctx["budget_path"], budget)
    (out_root / "logs").mkdir(exist_ok=True)
    say(f"▶ {tag} (GPU 합계 {tot} MiB · 디스크 {free_gb:.0f} GB) — 드라이버 출력은 logs/{tag}.log (⛔ tail 하지 않는다 · D 가 찍힌다)")
    t0 = time.time()
    code, why, gmax = None, None, tot or 0
    with open(out_root / "logs" / f"{tag}.log", "w", encoding="utf-8") as fh:
        proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT)
        step["pid"] = proc.pid
        _write_json(ctx["budget_path"], budget)
        try:
            meta_ok = mode_ok = dt_ok = False
            t_meta, last_g, last_hb = None, 0.0, t0
            while True:
                time.sleep(ctx["poll_s"])
                if proc.poll() is not None:
                    break                   # 끝났으면 아래 '늦은 검사' 한 곳에서 본다 (두 경로가 갈리지 않게)
                now = time.time()
                if not meta_ok:
                    m = _read_json(root / "run_meta.json")
                    if m is not None:
                        bad = meta_errors(m, exp)
                        if bad:
                            code, why = 9, "run_meta 가 탐침 설정과 다르다 — " + " · ".join(bad)
                            break
                        meta_ok, t_meta = True, now
                    elif now - t0 > ctx["meta_wait_s"]:
                        code, why = 9, f"run_meta.json 이 {ctx['meta_wait_s']:.0f} s 안에 안 생겼다"
                        break
                if meta_ok and not mode_ok:
                    mode = (_read_json(root / "run_meta.json") or {}).get("uma_inference_mode")
                    if mode is not None:
                        if mode != UMA_MODE:
                            code, why = 9, f"추론 모드 {mode!r} ≠ {UMA_MODE!r} (카드 §2b — 섞지 않는다)"
                            break
                        mode_ok = True
                    elif now - t_meta > ctx["meta_wait_s"]:
                        code, why = 9, "추론 모드가 기록되지 않았다 (UMA 로드 후 run_meta 갱신 없음)"
                        break
                if mode_ok and not dt_ok:
                    dt = mdlog_dt_ps(rdir / "md.log")
                    if dt is not None:
                        if not dt_matches(dt):
                            code, why = 9, f"md.log 시간 간격 {dt:.4f} ps ≠ dt {DT_FS / 1000.0:.4f} ps"
                            break
                        dt_ok = True
                if now - last_g >= ctx["gpu_log_s"]:
                    g = gpu_total_mib(ctx["nvsmi"])
                    gmax = max(gmax, g or 0)
                    with open(out_root / "gpu_log.tsv", "a", encoding="utf-8") as gl:
                        gl.write(f"{utc()}\t{tag}\t{g if g is not None else 'NA'}\n")
                    last_g = now
                if now - last_hb >= ctx["heartbeat_s"]:
                    tl = mdlog_tail(rdir / "md.log")
                    say(f"  … {tag} · {(now - t0) / 3600:.2f} h · md.log t "
                        f"{f'{tl[0]:.1f}' if tl else '—'} / {R.EQUILIB_PS + PROD_PS:g} ps · "
                        f"T {f'{tl[1]:.0f}' if tl else '—'} K · GPU 최대 {gmax} MiB")
                    last_hb = now
            if code is None and proc.returncode == 0:
                # 너무 빨리 끝나 루프에서 못 본 검사는 여기서 본다
                bad = meta_errors(_read_json(root / "run_meta.json"), {**exp, "uma_inference_mode": UMA_MODE})
                dt = mdlog_dt_ps(rdir / "md.log")
                if bad:
                    code, why = 9, "run_meta 가 탐침 설정과 다르다 — " + " · ".join(bad)
                elif not dt_matches(dt):
                    code, why = 9, f"md.log 시간 간격 {dt} ps ≠ dt {DT_FS / 1000.0:.4f} ps (또는 md.log 없음)"
        except (KeyboardInterrupt, _Stop) as e:
            code, why = 130, f"사람이 중단 ({type(e).__name__} {e})"
        if code is not None and proc.poll() is None:
            kill_tree(proc)
        elif proc.poll() is None:
            proc.wait()
    gpu_h = (time.time() - t0) / 3600.0
    budget["used_gpu_h"] = float(budget.get("used_gpu_h") or 0.0) + gpu_h
    step.update({"end_utc": utc(), "rc": proc.returncode, "gpu_h": round(gpu_h, 4),
                 "used_after": round(budget["used_gpu_h"], 4), "gpu_total_mib_max_sampled": gmax})
    if code is not None:
        step["stopped"] = why
        _write_json(ctx["budget_path"], budget)
        say(f"⛔ {tag}: {why} — 우리 런만 멈췄다 · {gpu_h:.2f} GPU-h · 누적 {budget['used_gpu_h']:.2f} (rc {code})")
        return code
    errs = [] if proc.returncode == 0 else [f"드라이버 rc {proc.returncode}"]
    errs += post_run_errors(rdir, T) if proc.returncode == 0 else []
    if errs:
        step["failed"] = errs
        _write_json(ctx["budget_path"], budget)
        say(f"⛔ {tag}: " + " · ".join(errs) + f" — 멈춘다 (rc 4) · 로그 logs/{tag}.log 의 **마지막 오류 줄만** 본다 "
            f"(`grep -a -iE 'error|traceback' … | tail -3`)")
        return 4
    step["ok"] = True
    step["mdlog_T_production"] = mdlog_T_stats(rdir / "md.log", R.EQUILIB_PS)
    _write_json(ctx["budget_path"], budget)
    say(f"✔ {tag} 끝 · {gpu_h:.2f} GPU-h · 누적 {budget['used_gpu_h']:.2f} / {ctx['cap']:g} · "
        f"생산 구간 T {step['mdlog_T_production']}")
    return 0


# ── 사전점검 · 라운드 ─────────────────────────────────────────────────────────
def preflight(a) -> tuple[dict, list[str]]:
    errs = []
    ctx = {"out_root": Path(a.out_root).expanduser().resolve(),
           "prep_root": Path(a.prep_root).expanduser().resolve() if a.prep_root else None,
           "python": a.python, "device": a.device,
           "decisions": Path(a._decisions or DECISIONS), "judge": Path(a._judge or JUDGE),
           "driver": Path(a._driver or R.MD_DRIVER), "struct_dir": Path(a._struct_dir or (REPO / R.STRUCT_DIR)),
           "nvsmi": a._nvidia_smi or "nvidia-smi", "repo": Path(a._repo or REPO),
           "gpu_start_max_mib": a.gpu_start_max_mib, "gpu_wait_s": a.gpu_wait_s, "meta_wait_s": a.meta_wait_s,
           "poll_s": a.poll_s, "heartbeat_s": a.heartbeat_s, "gpu_log_s": a.gpu_log_s,
           "disk_min_gb": a.disk_min_gb}
    ctx["injected"] = {k: v for k, v in (("decisions", a._decisions), ("judge", a._judge), ("driver", a._driver),
                                         ("struct_dir", a._struct_dir), ("nvidia_smi", a._nvidia_smi),
                                         ("repo", a._repo)) if v}
    ctx["budget_path"] = ctx["out_root"] / "budget.json"
    errs += constant_errors()
    ctx["cap"], e = decision_gate(ctx["decisions"]); errs += e
    if ctx["prep_root"] is None:
        errs.append("--prep_root (v6 라운드 out_root) 가 없다")
        ctx["prep"] = {}
    else:
        ctx["prep"], e = prep_check(ctx["prep_root"], ctx["struct_dir"]); errs += e
    for k in ("driver", "judge"):
        if not ctx[k].is_file():
            errs.append(f"{k} {ctx[k]} 가 없다")
    ctx["driver_sha256"] = R.sha256(ctx["driver"]) if ctx["driver"].is_file() else ""
    ctx["judge_sha256"] = R.sha256(ctx["judge"]) if ctx["judge"].is_file() else ""
    ctx["code_id"], dirty = git_state(ctx["repo"])
    if dirty is None:
        errs.append(f"작업트리 상태를 못 읽는다 ({ctx['repo']}) — 어떤 코드로 돌았는지 못 적는다")
    elif dirty:
        errs.append(f"작업트리 {ctx['repo']} 에 커밋 안 된 수정이 있다 — 새 worktree 에서 돌린다")
    errs += python_env_errors(a.python)
    if ctx["judge"].is_file():
        e, ctx["judge_selftest_tail"] = judge_selftest_errors(a.python, ctx["judge"]); errs += e
    return ctx, errs


def manifest_of(ctx) -> dict:
    m = {"schema": "cascade_v7_probe_round/v1", "created_utc": utc(), "code_id": ctx["code_id"],
         "card": CARD, "amendment": AMENDMENT, "decisions": [DECISION_CARD, DECISION_AMEND],
         "execution_approval": "사용자 2026-10-03 '지금 kgy에서 돌리자' (개정 §7 '탐침 실행 승인')",
         "frozen": frozen_now(), "cap_gpu_h": ctx["cap"], "est_gpu_h_per_run": EST_GPU_H_PER_RUN,
         "max_runs": MAX_RUNS, "prep_root": str(ctx["prep_root"]), "prep": ctx["prep"],
         "driver": {"path": str(ctx["driver"]), "sha256": ctx["driver_sha256"]},
         "judge": {"path": str(ctx["judge"]), "sha256": ctx["judge_sha256"],
                   "selftest_tail": ctx.get("judge_selftest_tail", "")},
         "python": str(ctx["python"]), "device": ctx["device"],
         "gpu_start_max_mib": ctx["gpu_start_max_mib"],
         "⛔": ["D 를 싣지 않는다 · 대표 쌍의 D 를 열지 않는다 (개정 §6)",
               "본 라운드 40 런을 띄우지 않는다 — 탐침 뒤 상한 비준 (개정 §7)",
               "탐침 시드 3·4 런은 본 라운드 집계에 안 넣는다 (개정 ④)"]}
    if ctx["injected"]:
        m["⚠_시험_주입"] = ctx["injected"]
    return m


def resume_check(ctx) -> tuple[dict | None, list[str]]:
    m = _read_json(ctx["out_root"] / "manifest.json")
    if m is None:
        return None, [f"--resume 인데 {ctx['out_root']}/manifest.json 이 없다"]
    errs = []
    old, new = m.get("frozen") or {}, frozen_now()
    diff = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
    if diff:
        errs.append("물리 규약(frozen)이 달라졌다 — " + ", ".join(f"{k}: {old.get(k)!r} → {new.get(k)!r}" for k in diff))
    if (m.get("driver") or {}).get("sha256") != ctx["driver_sha256"]:
        errs.append("드라이버 해시가 manifest 와 다르다 — 한 탐침 안에 두 드라이버가 섞인다")
    for s, row in (m.get("prep") or {}).items():
        if (ctx["prep"].get(s) or {}).get("sha256") != row.get("sha256"):
            errs.append(f"{s}: 준비 원본 해시가 manifest 와 다르다")
    b = _read_json(ctx["budget_path"])
    if b is None:
        errs.append("budget.json 을 못 읽는다 — 누적을 승계할 수 없다")
    return b, errs


def run_probe(a) -> int:
    ctx, errs = preflight(a)
    if ctx["injected"]:
        say(f"⚠ 시험 주입 사용: {ctx['injected']} — 실제 탐침이면 이 줄이 나오면 안 된다")
    say(f"v7 탐침 · 사다리 {list(LADDER)} K · 계획 {len(PLAN)} 런/온도 (최대 {MAX_RUNS}) · 생산 {PROD_PS:g} ps · "
        f"dt {DT_FS:g} fs · save {SAVE_FS:g} fs · UMA {R.UMA_MODEL} {UMA_MODE} · 대표 부모 {PAIR_PARENT}")
    say(f"상한 {ctx['cap']} GPU-h (원장 {DECISION_AMEND}) · 단가 추정 {EST_GPU_H_PER_RUN} GPU-h/런 · "
        f"최대 투영 {MAX_RUNS * EST_GPU_H_PER_RUN:.1f} — 단가 > {((ctx['cap'] or 0) / MAX_RUNS):.2f} 이면 마지막 런에서 게이트가 멈춘다")
    for s, row in ctx["prep"].items():
        say(f"  준비 {s}: {row['n_atoms']} 원자 · sha {row['sha256'][:16]} · fmax {row['final_fmax_eV_A']} · 입력 해시 = repo 구조 ✓")
    st_tail = (ctx.get("judge_selftest_tail") or "—").splitlines()[-1]
    say(f"  드라이버 sha {ctx['driver_sha256'][:16]} · 판독기 sha {ctx['judge_sha256'][:16]} · code {ctx['code_id'][:12]} · "
        f"python {a.python} · 판독기 selftest: {st_tail}")
    tot = gpu_total_mib(ctx["nvsmi"])
    say(f"  GPU 합계 지금 {tot if tot is not None else '못 읽음'} MiB (시작 문턱 {a.gpu_start_max_mib})")
    if errs:
        say("⛔ 사전점검 불통과 — 시작하지 않는다 (rc 2):")
        for e in errs:
            print(f"     · {e}", flush=True)
        return 2
    if a.dry_run:
        T_star, why, nxt = J.select_probe_temperature({})
        say(f"계획 (빈 out_root 에서 판독기 규칙의 첫 지목: {nxt}):")
        for T in LADDER:
            for s, sd in PLAN:
                print(f"     {T} K  {tag_of(T, s, sd)}", flush=True)
        v0 = ctx["out_root"] / "prep" / f"{nxt[1]}.prepared.xyz"
        print("     첫 명령: " + " ".join(md_cmd(a.python, ctx["driver"], v0, ctx["out_root"] / "md" / tag_of(*nxt),
                                                    nxt[0], nxt[1], nxt[2], a.device)), flush=True)
        say("■ dry_run — 아무것도 만들지 않았다")
        return 0

    out_root = ctx["out_root"]
    if not a.resume:
        if out_root.exists() and any(out_root.iterdir()):
            say(f"⛔ out_root 가 비어 있지 않다: {out_root} — 새 탐침은 폴더를 재사용하지 않는다 (이어받기면 --resume) (rc 11)")
            return 11
        out_root.mkdir(parents=True, exist_ok=True)
    elif not out_root.is_dir():
        say(f"⛔ --resume 인데 {out_root} 가 없다 (rc 2)")
        return 2
    lock = take_lock(out_root)
    if lock is None:
        say(f"⛔ 이미 다른 러너가 {out_root} 를 잡고 있다 (rc 10)")
        return 10
    if a.resume:
        budget, rerrs = resume_check(ctx)
        if rerrs:
            say("⛔ 이어받기 거부 (rc 2):")
            for e in rerrs:
                print(f"     · {e}", flush=True)
            return 2
        say(f"↻ 이어받기 · 누적 {float(budget.get('used_gpu_h') or 0):.2f} GPU-h 승계 · 끝난 런 "
            f"{sum(1 for st in budget.get('steps', []) if st.get('ok'))}")
    else:
        (out_root / "prep").mkdir(exist_ok=True)
        for s, row in ctx["prep"].items():
            dst = out_root / "prep" / f"{s}.prepared.xyz"
            shutil.copy2(row["source_xyz"], dst)
            if R.sha256(dst) != row["sha256"]:
                say(f"⛔ 준비 사본 해시가 원본과 다르다 ({s}) (rc 2)")
                return 2
            _write_json(out_root / "prep" / f"{s}.reuse.json",
                        {**row, "copied_to": str(dst), "copied_utc": utc(),
                         "⚠": "v6 준비를 초기 좌표로만 재사용 (개정 ⑩) — 이 온도에서의 평형을 뜻하지 않는다"})
        _write_json(out_root / "manifest.json", manifest_of(ctx))
        budget = {"cap_gpu_h": ctx["cap"], "est_gpu_h_per_run": EST_GPU_H_PER_RUN, "used_gpu_h": 0.0,
                  "steps": [], "accepted_flags": [],
                  "⛔": "상한은 원장(cost_cap) 값이다 — 코드·CLI 로 못 올린다. 넘으면 멈추고 보고한다 (개정 §4)."}
        _write_json(ctx["budget_path"], budget)
    accepted = {x.get("tag") for x in budget.get("accepted_flags", [])}
    launched = 0
    for sig in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, _on_signal)
    try:
        while True:
            say("판독기 (--probe) …")
            d, why = judge_once(a.python, ctx["judge"], out_root)
            if d is None:
                say(f"⛔ {why} (rc 5)")
                return 5
            show_judge(d)
            flagged_all = dict(infra_flags(d))
            for t in [t for t in a.accept_flagged if t not in accepted]:
                if t in flagged_all:
                    budget.setdefault("accepted_flags", []).append({"tag": t, "at_utc": utc(), "reasons": flagged_all[t]})
                    accepted.add(t)
                    _write_json(ctx["budget_path"], budget)
                    say(f"  받아들임 기록: {t} ({' · '.join(flagged_all[t])}) — 카드상 자격 없음 그대로 · 판독기 지시대로 간다")
            flags = infra_flags(d, accepted)
            if flags:
                say("⛔ '확인 못 함' 표지 — 판독기 지시를 따르기 전에 사람이 본다 (rc 5):")
                for t, w in flags:
                    print(f"     · {t}: {' · '.join(w)}", flush=True)
                print("     (받아들이려면 --resume --accept_flagged <태그> · 인프라 문제면 그 런을 attic 으로 옮기고 --resume)",
                      flush=True)
                return 5
            if d.get("T_star_K") is not None:
                say(f"■ T* = {d['T_star_K']} K — 탐침 끝 · 산출물 {out_root}/cascade_v7_probe.json")
                say("  ⛔ 본 라운드 40 런은 이 러너가 띄우지 않는다 — 탐침 실측 단가 × 40 으로 상한을 내고 사용자 비준 (개정 §7)")
                return 0
            nxt = d.get("next")
            if nxt is None:
                say(f"■ {d.get('why')} — 탐침 끝 · v7 본 라운드를 열지 않는다 (재개 조건 밖 · 새 카드)")
                return 0
            T, s, sd = int(nxt[0]), str(nxt[1]), int(nxt[2])
            if launched >= MAX_RUNS:
                say(f"⛔ 이번 실행에서 런 {launched} 개를 띄웠는데 또 지목됐다 — 계획 최대 {MAX_RUNS} 초과 (rc 6)")
                return 6
            measured = [float(st["gpu_h"]) for st in budget.get("steps", []) if st.get("ok")]
            ok, gwhy, unit = budget_gate(float(budget.get("used_gpu_h") or 0.0), measured, ctx["cap"])
            if not ok:
                budget["steps"].append({"tag": tag_of(T, s, sd), "stopped": gwhy, "at_utc": utc()})
                _write_json(ctx["budget_path"], budget)
                say(gwhy + " (rc 3)")
                return 3
            say(f"  비용: {gwhy}")
            rc = run_one(ctx, budget, T, s, sd)
            launched += 1
            if rc != 0:
                return rc
    except (KeyboardInterrupt, _Stop) as e:
        say(f"⛔ 사람이 중단 ({type(e).__name__}) — 돌던 런은 없었다 (rc 130)")
        return 130
    finally:
        os.close(lock)


def status(a) -> int:
    """읽기만 — 진행 · 누적 · 마지막 판독 (D 없음). 잠금·파일을 건드리지 않는다."""
    out_root = Path(a.out_root).expanduser().resolve()
    m, b = _read_json(out_root / "manifest.json"), _read_json(out_root / "budget.json")
    if m is None or b is None:
        print(f"⛔ {out_root} 에 manifest/budget 이 없다")
        return 2
    steps = b.get("steps", [])
    done = [st for st in steps if st.get("ok")]
    print(f"■ v7 탐침 {out_root} · code {str(m.get('code_id'))[:12]} · 상한 {b.get('cap_gpu_h')} · 누적 "
          f"{float(b.get('used_gpu_h') or 0):.2f} GPU-h · 끝난 런 {len(done)} · 단가 실측 "
          f"{[round(float(st['gpu_h']), 2) for st in done]}")
    for st in steps:
        state = ("✔" if st.get("ok") else "⛔ " + str(st.get("stopped") or st.get("failed")) if ("rc" in st or "stopped" in st)
                 else "▶ 도는 중")
        print(f"  {st.get('tag')}: {state} · {st.get('gpu_h', '—')} GPU-h · 시작 {st.get('start_utc', st.get('at_utc', '—'))}"
              + (f" · 생산 T {st['mdlog_T_production']}" if st.get("mdlog_T_production") else ""))
        if "rc" not in st and "stopped" not in st and st.get("T_K"):
            tl = mdlog_tail(out_root / "md" / st["tag"] / SUBDIR / f"T{st['T_K']}" / "md.log")
            if tl:
                print(f"     md.log t {tl[0]:.1f} / {R.EQUILIB_PS + PROD_PS:g} ps ({100 * tl[0] / (R.EQUILIB_PS + PROD_PS):.0f} %) · T {tl[1]:.0f} K")
    d = _read_json(out_root / "cascade_v7_probe.json")
    if d:
        print(f"  마지막 판독: T* {d.get('T_star_K')} · next {d.get('next')} · {d.get('why')}")
        if judge_output_errors(d):
            print("  ⚠ 판독 산출물 검사: " + " · ".join(judge_output_errors(d)))
    return 0


# ── selftest — 양성 + **음성** ───────────────────────────────────────────────
_FAKE_DRIVER = r'''
import argparse, json, os, sys, time
from pathlib import Path
ap = argparse.ArgumentParser()
for k in ("--v0_xyz", "--label", "--out_root", "--device", "--friction", "--timestep_fs", "--equilib_ps",
          "--prod_ps", "--save_fs", "--seed", "--uma_model", "--uma_task", "--n_configs"):
    ap.add_argument(k)
ap.add_argument("--disorder_levels", nargs="+"); ap.add_argument("--temperatures", nargs="+")
ap.add_argument("--fit_window_ps", nargs=2); ap.add_argument("--save_traj", action="store_true")
ap.add_argument("--turbo", action="store_true")
a = ap.parse_args(); E = os.environ
root = Path(a.out_root); tag = root.name; T = float(a.temperatures[0])
bad = dict(x.split("=", 1) for x in E.get("FAKE_BAD", "").split() if "=" in x).get(tag, "")
root.mkdir(parents=True, exist_ok=True)
(root / "fake.pid").write_text(str(os.getpid()))
meta = {"label": a.label, "n_atoms": int(E.get("FAKE_NATOMS", "4")), "supercell": [1, 1, 1], "v0_xyz": a.v0_xyz,
        "temperatures": [T], "prod_ps": float(a.prod_ps), "equilib_ps": float(a.equilib_ps),
        "seed": int(a.seed) + (1 if bad == "seed" else 0), "fit_window_ps": [float(x) for x in a.fit_window_ps],
        "save_traj": bool(a.save_traj), "uma_model": a.uma_model,
        "uma_inference_mode_requested": "turbo" if a.turbo else "default"}
if bad != "nometa":
    (root / "run_meta.json").write_text(json.dumps(meta))
time.sleep(0.15)
if bad != "nometa":
    meta["uma_inference_mode"] = "turbo" if bad == "turbo" else "default"
    (root / "run_meta.json").write_text(json.dumps(meta))
d = root / "d0.00_cfg0" / f"T{int(T)}"; d.mkdir(parents=True, exist_ok=True)
dt = 0.001 if bad == "dt" else float(a.timestep_fs) / 1000.0
with open(d / "md.log", "w") as fh:
    fh.write("Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]\n")
    for i in range(3):
        fh.write(f"{i * dt:<10.4f} -1.0 -1.0 0.0 {T:.1f}\n")
    fh.write(f"{float(a.equilib_ps) + 1:<10.4f} -1.0 -1.0 0.0 {T + 3:.1f}\n")
time.sleep(float(E.get("FAKE_SLEEP_BAD", "6") if bad in ("seed", "turbo", "dt", "nometa") else E.get("FAKE_SLEEP", "0.3")))
print(f"    d=0.00 cfg0 T={int(T)}: D_Li=1.234e-06 cm²/s  (0.0 min)", flush=True)   # 진짜 드라이버처럼 D 를 찍는다
if bad == "crash":
    sys.exit(1)
n = int(round(float(a.prod_ps) * 1000.0 / float(a.save_fs))) - (1 if bad == "frames" else 0)
(d / "traj.xyz").write_text("")
(d / "aimd_results.json").write_text(json.dumps({"T_K": T, "save_fs": float(a.save_fs), "n_frames": n,
                                                 "prod_ps": float(a.prod_ps), "dt_fs": float(a.timestep_fs)}))
(d / "msd.json").write_text(json.dumps({"T_K": T, "D_Li_cm2_s": 1.234e-6, "times_ps": [0.1 * i for i in range(n)],
                                        "msd_Li_A2": [0.0] * n, "fit_window_ps": [2.0, 50.0]}))
'''

_FAKE_JUDGE = r'''
import glob, json, os, sys
from pathlib import Path
sys.path.insert(0, os.environ["FAKE_TOOLS"])
import judge_eprime as J
E = os.environ
if sys.argv[1] == "--selftest":
    print("selftest FAIL" if E.get("FAKE_JUDGE_ST_FAIL") else "selftest PASS")
    sys.exit(1 if E.get("FAKE_JUDGE_ST_FAIL") else 0)
root = Path(sys.argv[2])
fails, errs = set(E.get("FAKE_FAIL", "").split()), set(E.get("FAKE_ERR", "").split())
res = {}
for f in sorted(glob.glob(str(root / "md" / "*" / "*" / "T*" / "msd.json"))):
    tag = Path(f).relative_to(root / "md").parts[0]
    st, sd = J.parse_tag(tag)
    T = int(json.load(open(f))["T_K"])
    key = f"{T}:{st}:{sd}"
    r = {"tag": tag, "eligible": key not in fails, "framework_alarm": "ok",
         "sub_window_ratios": [1.0, 0.97, 1.02, 1.01], "events": 99}
    if key in errs:
        r = {"tag": tag, "eligible": False, "error": "프로토콜 결속 실패 — 시험 주입"}
    if E.get("FAKE_UNAV") == key:
        r["eligible"] = False; r["framework_alarm"] = "unavailable (ImportError)"
    if E.get("FAKE_LEAK_D"):
        r["D_Li_cm2_s"] = 9.87e-6
    res[(T, st, sd)] = r
plan = set(J.V7_PROBE_PLAN)
runs = {k: v for k, v in res.items() if (k[1], k[2]) in plan}
T_star, why, nxt = J.select_probe_temperature(runs)
out = {"ladder_K": list(J.V7_LADDER_K), "protocol": dict(J.V7_PROTOCOL), "pair_parent": J.V7_PAIR_PARENT,
       "plan": [list(x) for x in J.V7_PROBE_PLAN], "T_star_K": T_star, "why": why, "next": nxt,
       "runs": [{"T_K": T, "structure": st, "seed": sd, **r} for (T, st, sd), r in sorted(runs.items())]}
if E.get("FAKE_PROTO"):
    out["protocol"]["prod_ps"] = 200.0
if E.get("FAKE_NEXT_OFFPLAN") and nxt:
    out["next"] = [nxt[0], "P1_Al2O3_D", 3]
if not E.get("FAKE_NO_JSON"):
    (root / "cascade_v7_probe.json").write_text(json.dumps(out, ensure_ascii=False))
print("-> " + why)
'''


def _selftest() -> int:
    fails, last = [], {"out": ""}

    def ck(name, cond):
        print(f"  {'✓' if cond else '✗'} {name}", flush=True)
        if not cond:
            fails.append(name)
            print("      ↳ 마지막 러너 출력 끝: " + last["out"][-700:].replace("\n", "\n        "), flush=True)

    print("── 순수 검사 ──")
    ck("상수: 판독기 ↔ v6 러너 ↔ 개정 §3 추첨 ↔ 계획 순서 일치", constant_errors() == [])
    ck("⛔음성 상수: 대표 부모를 D 로 바꾸면 잡는다", any("추첨" in e for e in constant_errors(pair="D")))
    ck("⛔음성 상수: 계획 순서를 바꾸면 잡는다", any("계획" in e for e in constant_errors(plan=PLAN[::-1])))
    ck("⛔음성 상수: census 에 없는 부모 쌍", any("census" in e for e in constant_errors(roster=["P1_Al2O3_A"])))
    t = tag_of(800, "P1_Al2O3_C", 3)
    ck("태그 규약 ⑥: 판독기 parse_tag·_TAG_T 가 읽는다",
       t == "P1_Al2O3_C__T800__s3" and J.parse_tag(t) == ("P1_Al2O3_C", 3) and J._TAG_T.search(t).group(1) == "800")
    cmd = md_cmd("PY", "DRV", "V0", "OUT", 800, "P1_Al2O3_C", 3, "cuda")
    ck("명령: 400 ps · dt 2 · save 100 · 창 2–50 · --save_traj · 시드 3 · turbo 없음",
       cmd[cmd.index("--prod_ps") + 1] == "400.0" and cmd[cmd.index("--timestep_fs") + 1] == "2.0"
       and cmd[cmd.index("--save_fs") + 1] == "100.0" and cmd[cmd.index("--fit_window_ps") + 1:][:2] == ["2.0", "50.0"]
       and "--save_traj" in cmd and cmd[cmd.index("--seed") + 1] == "3" and "--turbo" not in cmd
       and cmd[cmd.index("--temperatures") + 1] == "800")
    ok, _, u = budget_gate(0.0, [], 141.0)
    ck("비용: 첫 런 0 + 11.8 ≤ 141 → 시작", ok and u == EST_GPU_H_PER_RUN)
    ok, _, u = budget_gate(129.6, [11.0, 11.8, 1.0], 141.0)
    ck("⛔음성 비용: 129.6 + 실측 **최댓값** 11.8 > 141 → 멈춤 (최솟값·평균이면 통과해 버린다)", (not ok) and u == 11.8)
    ck("⛔음성 비용: 누적 ≥ 상한", not budget_gate(141.0, [], 141.0)[0])
    ck("비용: 12 × 11.8 = 141.6 — 단가 11.8 이면 12 번째 런이 막힌다 (머리글 ⚠)",
       not budget_gate(11 * 11.8, [11.8], 141.0)[0] and budget_gate(11 * 11.7, [11.7], 141.0)[0])
    exp = meta_expect(800, "H0_host", 1, "/x/prep/H0_host.prepared.xyz", 204)
    good = dict(exp)
    ck("run_meta: 같으면 통과", meta_errors(good, exp) == [])
    for k, v in (("seed", 2), ("prod_ps", 200.0), ("temperatures", [600.0]), ("uma_inference_mode_requested", "turbo"),
                 ("save_traj", 1), ("v0_xyz", "/other.xyz"), ("n_atoms", 208), ("equilib_ps", 10.0)):
        ck(f"⛔음성 run_meta {k} = {v!r} 를 잡는다", meta_errors({**good, k: v}, exp) != [])
    ck("⛔음성 run_meta 키 없음 = 불통과", meta_errors({k: v for k, v in good.items() if k != "seed"}, exp) != [])
    dj = {"ladder_K": [800, 1000], "protocol": dict(J.V7_PROTOCOL), "pair_parent": PAIR_PARENT,
          "plan": [list(x) for x in PLAN], "T_star_K": None, "next": [800, "H0_host", 1], "runs": []}
    ck("판독 산출물: 같으면 통과", judge_output_errors(dj) == [])
    for name, mut in (("사다리", {"ladder_K": [600, 800]}),
                      ("생산 길이", {"protocol": {**J.V7_PROTOCOL, "prod_ps": 200.0}}),
                      ("대표 부모", {"pair_parent": "D"}), ("계획", {"plan": [list(x) for x in PLAN[:4]]}),
                      ("next 계획 밖", {"next": [800, "P1_Al2O3_D", 3]}), ("next 사다리 밖", {"next": [600, "H0_host", 1]}),
                      ("T* 와 next 동시", {"T_star_K": 800}), ("D 섞임", {"runs": [{"tag": "x", "D": 1e-6}]}),
                      ("D_ 섞임", {"runs": [{"tag": "x", "D_legacy_sto_lab": 1e-6}]})):
        ck(f"⛔음성 판독 산출물 {name} 를 잡는다", judge_output_errors({**dj, **mut}) != [])
    fl = {"runs": [{"tag": "a", "error": "x"}, {"tag": "b", "framework_alarm": "unavailable (E)"},
                   {"tag": "c", "framework_alarm": "ok", "eligible": False}]}
    ck("표지: 오류·unavailable 은 표지 · 과학적 불통과(c)는 아님", [t for t, _ in infra_flags(fl)] == ["a", "b"])
    ck("표지: 받아들인 태그는 뺀다", [t for t, _ in infra_flags(fl, accepted={"a"})] == ["b"])

    tmp = Path(tempfile.mkdtemp(prefix="cv7probe_st_"))
    try:
        p = tmp / "md.log"
        p.write_text("Time[ps]      Etot[eV]\n0.0000 -1 300\n0.0020 -1 301\n10.0000 -1 800\n12.0000 -1 806\n")
        ck("md.log dt = 0.002 ps", dt_matches(mdlog_dt_ps(p)))
        ck("⛔음성 dt 0.001 · 0.0021 · None 은 dt 2 fs 가 아니다 (판독기 _same 이면 0.001 이 통과했다)",
           not dt_matches(0.001) and not dt_matches(0.0021) and not dt_matches(None) and dt_matches(0.0020))
        ck("md.log 생산 구간 T 평균 (t > 5 ps 만)", (mdlog_T_stats(p, 5.0) or {}).get("mean_K") == 803.0)
        ck("md.log 끝 줄", mdlog_tail(p) == (12.0, 806.0))
        p.write_text("Time[ps]      Etot[eV]\n")
        ck("⛔음성 md.log 머리줄뿐 → dt None (통과 아님)", mdlog_dt_ps(p) is None)

        print("── 끝에서 끝 (가짜 드라이버·판독기·nvidia-smi · 진짜 select_probe_temperature) ──")
        cell = R.CELL_DIAG
        lat = f'Lattice="{cell[0]} 0.0 0.0 0.0 {cell[1]} 0.0 0.0 0.0 {cell[2]}" Properties=species:S:1:pos:R:3 pbc="T T T"'
        structs, v6 = tmp / "structs", tmp / "v6" / "prep"
        structs.mkdir(); v6.mkdir(parents=True)
        for i, s in enumerate(PROBE_STRUCTURES):
            (structs / f"{s}.xyz").write_text(f"4\n{lat}\nLi 0 0 {i}\nLi 1 0 0\nS 0 1 0\nCl 0 0 1\n")
            (v6 / f"{s}.prepared.xyz").write_text(f"4\n{lat}\nLi 0 0 {i}.01\nLi 1 0 0\nS 0 1 0\nCl 0 0 1\n")
            (v6 / f"{s}.prepared.json").write_text(json.dumps({
                "structure": s, "converged": True, "n_atoms": 4, "final_fmax_eV_A": 0.01,
                "prepared_sha256": R.sha256(v6 / f"{s}.prepared.xyz"), "input_sha256": R.sha256(structs / f"{s}.xyz")}))
        dec = tmp / "decisions.json"

        def write_dec(state="active", cap=141):
            dec.write_text(json.dumps({"decisions": [
                {"id": DECISION_CARD, "decision_state": "active"},
                {"id": DECISION_AMEND, "decision_state": state, "cost_cap": {"total_gpu_h": cap}}]}))
        write_dec()
        drv, jdg = tmp / "fake_driver.py", tmp / "fake_judge.py"
        drv.write_text(_FAKE_DRIVER); jdg.write_text(_FAKE_JUDGE)
        gpu = tmp / "gpu"; gpu.write_text("3000\n")
        nvs = tmp / "nvidia-smi"
        nvs.write_text('#!/bin/sh\n[ -f "$FAKE_GPU_FILE" ] || exit 1\ncat "$FAKE_GPU_FILE"\n'); nvs.chmod(0o755)
        stubs, broken = tmp / "stubs", tmp / "broken"
        for mod in ("fairchem", "fairchem/core", "ase", "numpy"):
            (stubs / mod).mkdir(parents=True, exist_ok=True); (stubs / mod / "__init__.py").write_text("")
        (broken / "fairchem" / "core").mkdir(parents=True)
        (broken / "fairchem" / "__init__.py").write_text("")
        (broken / "fairchem" / "core" / "__init__.py").write_text("raise ImportError('stub broken')\n")
        repo = tmp / "repo"; repo.mkdir()
        g = ["git", "-C", str(repo), "-c", "user.email=t@t", "-c", "user.name=t"]
        subprocess.run(g + ["init", "-q"], check=True)
        (repo / "f.txt").write_text("a\n")
        subprocess.run(g + ["add", "f.txt"], check=True); subprocess.run(g + ["commit", "-qm", "x"], check=True)

        def run(out, *extra, env=None, pypath=None):
            e = dict(os.environ, PYTHONPATH=str(pypath or stubs), FAKE_TOOLS=str(HERE), FAKE_GPU_FILE=str(gpu),
                     **(env or {}))
            c = [sys.executable, str(Path(__file__).resolve()), "--out_root", str(out), "--prep_root", str(tmp / "v6"),
                 "--python", sys.executable, "--device", "cpu", "--poll_s", "0.05", "--meta_wait_s", "2",
                 "--gpu_wait_s", "0.3", "--heartbeat_s", "999", "--gpu_log_s", "999", "--disk_min_gb", "0",
                 "--_decisions", str(dec), "--_judge", str(jdg), "--_driver", str(drv), "--_struct_dir", str(structs),
                 "--_nvidia_smi", str(nvs), "--_repo", str(repo), *extra]
            r = subprocess.run(c, env=e, capture_output=True, text=True, timeout=300)
            last["out"] = f"[rc {r.returncode}] " + r.stdout + r.stderr
            return r.returncode, r.stdout + r.stderr

        def steps(out):
            return [(st.get("tag"), bool(st.get("ok"))) for st in (_read_json(out / "budget.json") or {}).get("steps", [])]

        def alive(out, tag):
            try:
                os.kill(int((out / "md" / tag / "fake.pid").read_text()), 0)
                return True
            except (OSError, ValueError):
                return False

        o = tmp / "dry"
        rc, txt = run(o, "--dry_run")
        ck("dry_run: rc 0 · 아무것도 안 만든다 · 첫 지목 800 K H0 s1", rc == 0 and not o.exists() and "H0_host__T800__s1" in txt)

        o = tmp / "allpass"
        rc, txt = run(o)
        want = [tag_of(800, s, sd) for s, sd in PLAN]
        ck("양성 전부 통과: rc 0 · 계획 순서대로 6 런 · T* = 800 · 러너가 T* 에서 멈췄다고 말한다",
           rc == 0 and steps(o) == [(t, True) for t in want] and "■ T* = 800 K" in txt
           and (_read_json(o / "cascade_v7_probe.json") or {}).get("T_star_K") == 800)
        ck("⛔ D 봉인: 러너 화면에 드라이버의 D 가 안 샌다 (그런데 런 로그에는 있다 = 시험이 헛것이 아니다)",
           "D_Li" not in txt and "1.234e-06" not in txt and "D_Li" in (o / "logs" / f"{want[0]}.log").read_text())
        ck("본 라운드를 안 띄운다: P1/P2 는 시드 3·4 뿐", all(t.endswith(("__s3", "__s4")) for t, _ in steps(o) if t.startswith("P")))
        ck("manifest 에 시험 주입이 남는다", "⚠_시험_주입" in (_read_json(o / "manifest.json") or {}))
        ck("준비 사본 + reuse 기록", all((o / "prep" / f"{s}.reuse.json").is_file() for s in PROBE_STRUCTURES))

        o = tmp / "fail800"
        rc, txt = run(o, env={"FAKE_FAIL": "800:H0_host:2"})
        want = [tag_of(800, "H0_host", 1), tag_of(800, "H0_host", 2)] + [tag_of(1000, s, sd) for s, sd in PLAN]
        ck("800 K H0 s2 불통과 → 1000 K 계획 6 런 → T* = 1000 (800 의 나머지 4 런은 안 돈다)",
           rc == 0 and [t for t, _ in steps(o)] == want and (_read_json(o / "cascade_v7_probe.json") or {}).get("T_star_K") == 1000)

        o = tmp / "exhaust"
        rc, txt = run(o, env={"FAKE_FAIL": "800:H0_host:1 1000:P2_Al2S3_C:4"})
        ck("사다리 소진: 1000 K 마지막 런 불통과 → rc 0 · T* 없음 · '열지 않는다' · 런 7",
           rc == 0 and len(steps(o)) == 7 and (_read_json(o / "cascade_v7_probe.json") or {}).get("T_star_K") is None
           and "열지 않는다" in txt)

        rc, txt = run(tmp / "allpass")
        ck("⛔음성 새 시작인데 out_root 가 차 있다 → 11", rc == 11)

        write_dec(state="proposed")
        o = tmp / "dec"
        rc, txt = run(o)
        ck("⛔음성 개정 결정이 active 가 아니다 → 2 · 폴더도 안 만든다", rc == 2 and not o.exists())
        write_dec(cap=5)
        rc, txt = run(o)
        ck("⛔음성 상한 5 GPU-h → 첫 런 전에 3 · 런 0", rc == 3 and [x for x in steps(o) if x[1]] == [])
        write_dec()

        o = tmp / "lock"
        o.mkdir()
        fd = take_lock(o)
        rc, txt = run(o, "--resume")
        os.close(fd)
        ck("⛔음성 다른 러너가 잠금을 쥐고 있다 → 10", rc == 10)

        o = tmp / "seed"
        tg = tag_of(800, "H0_host", 2)
        rc, txt = run(o, env={"FAKE_BAD": f"{tg}=seed"})
        ck("⛔음성 run_meta seed 불일치 → 9 · 우리 런을 죽였다 · msd.json 없음",
           rc == 9 and not alive(o, tg) and not (o / "md" / tg / SUBDIR / "T800" / "msd.json").exists())
        rc, txt = run(o, "--resume")
        ck("⛔음성 끊긴 런 폴더가 남아 있으면 이어 돌리지 않는다 → 11 (attic 안내)", rc == 11 and "attic" in txt)
        rc, txt = run(o, "--resume", env={"FAKE_NO_JSON": "1"})
        ck("⛔음성 판독기가 산출물을 안 남기면 **낡은 산출물**을 읽지 않는다 → 5", rc == 5 and "안 남겼" in txt)
        (o / "attic").mkdir()
        (o / "md" / tg).rename(o / "attic" / tg)
        drv.write_text(_FAKE_DRIVER + "\n# changed\n")
        rc, txt = run(o, "--resume")
        ck("⛔음성 이어받기인데 드라이버 해시가 바뀌었다 → 2", rc == 2)
        drv.write_text(_FAKE_DRIVER)
        rc, txt = run(o, "--resume")
        b = _read_json(o / "budget.json") or {}
        ua = [st["used_after"] for st in b.get("steps", []) if "used_after" in st]
        ck("이어받기: 같은 (T, 구조, 시드) 로 다시 → T* 800 · 죽인 런 시간도 누적 (단조 증가)",
           rc == 0 and (_read_json(o / "cascade_v7_probe.json") or {}).get("T_star_K") == 800
           and ua == sorted(ua) and any(st.get("stopped") for st in b.get("steps", [])))
        m = _read_json(o / "manifest.json"); m["frozen"]["prod_ps"] = 200.0; _write_json(o / "manifest.json", m)
        rc, txt = run(o, "--resume")
        ck("⛔음성 이어받기인데 frozen 이 다르다 (200 ps) → 2", rc == 2 and "frozen" in txt)

        for kind, want_rc in (("turbo", 9), ("dt", 9), ("nometa", 9), ("crash", 4), ("frames", 4)):
            o = tmp / f"bad_{kind}"
            tg = tag_of(800, "H0_host", 1)
            rc, txt = run(o, env={"FAKE_BAD": f"{tg}={kind}"})
            early = not alive(o, tg) and not (o / "md" / tg / SUBDIR / "T800" / "msd.json").exists()
            ck(f"⛔음성 드라이버 {kind} → {want_rc}" + (" · 도는 중에 잡아 우리 런을 죽였다 (msd.json 없음)" if want_rc == 9 else ""),
               rc == want_rc and (want_rc != 9 or early))

        o = tmp / "late"
        tg = tag_of(800, "H0_host", 1)
        rc, txt = run(o, "--poll_s", "3", env={"FAKE_BAD": f"{tg}=seed", "FAKE_SLEEP_BAD": "0"})
        ck("⛔음성 첫 폴링 전에 끝난 런도 run_meta 를 늦게라도 본다 → 9 (런은 끝까지 갔다 = 늦은 경로)",
           rc == 9 and (o / "md" / tg / SUBDIR / "T800" / "msd.json").exists())
        gpu.write_text("20000\n")
        rc, txt = run(tmp / "gpuhi")
        ck("⛔음성 GPU 합계 20000 > 문턱 16000 → 기다리다 12", rc == 12)
        gpu.unlink()
        rc, txt = run(tmp / "gpuna")
        ck("⛔음성 nvidia-smi 못 읽음 → '비어 있음' 아님 → 12", rc == 12)
        gpu.write_text("3000\n")
        rc, txt = run(tmp / "disk", "--disk_min_gb", "1e12")
        ck("⛔음성 디스크 부족 → 12", rc == 12)

        o = tmp / "flag"
        tg = tag_of(800, "H0_host", 1)
        rc, txt = run(o, env={"FAKE_ERR": f"800:H0_host:1"})
        ck("⛔음성 판독기 '오류' 표지 → 사다리 넘기기 전에 5 (런 1)", rc == 5 and len(steps(o)) == 1)
        rc, txt = run(o, "--resume", "--accept_flagged", tg, env={"FAKE_ERR": f"800:H0_host:1"})
        b = _read_json(o / "budget.json") or {}
        ck("받아들임 → 판독기 지시대로 1000 K → T* 1000 · 받아들임이 budget 에 남는다",
           rc == 0 and (_read_json(o / "cascade_v7_probe.json") or {}).get("T_star_K") == 1000
           and [x.get("tag") for x in b.get("accepted_flags", [])] == [tg])
        rc, txt = run(tmp / "unav", env={"FAKE_UNAV": "800:H0_host:1"})
        ck("⛔음성 골격 경보 unavailable → 5", rc == 5)
        rc, txt = run(tmp / "leak", env={"FAKE_LEAK_D": "1"})
        ck("⛔음성 판독 산출물에 D 가 섞임 → 5 · 값은 안 찍는다", rc == 5 and "9.87" not in txt)
        for i, (name, env) in enumerate((("프로토콜 200 ps", {"FAKE_PROTO": "1"}),
                                         ("next 계획 밖", {"FAKE_NEXT_OFFPLAN": "1"}), ("산출물 없음", {"FAKE_NO_JSON": "1"}))):
            rc, txt = run(tmp / f"judge_bad_{i}", env=env)
            ck(f"⛔음성 판독기 {name} → 5 · 런 0", rc == 5 and steps(tmp / f"judge_bad_{i}") == [])
        rc, txt = run(tmp / "jst", env={"FAKE_JUDGE_ST_FAIL": "1"})
        ck("⛔음성 판독기 selftest 불통과 → 2", rc == 2)
        rc, txt = run(tmp / "env", pypath=broken)
        ck("⛔음성 python 에 fairchem 이 없다 (base python) → 2", rc == 2 and "fairchem" in txt)
        s0 = PROBE_STRUCTURES[1]
        jf = v6 / f"{s0}.prepared.json"
        keep = jf.read_text()
        for name, mut in (("미수렴", {"converged": False}), ("prepared 해시", {"prepared_sha256": "0" * 64}),
                          ("입력 해시 ≠ repo 구조", {"input_sha256": "0" * 64}), ("원자 수", {"n_atoms": 5})):
            jf.write_text(json.dumps({**json.loads(keep), **mut}))
            rc, txt = run(tmp / "prep_x")
            ck(f"⛔음성 준비 {name} → 2", rc == 2)
        jf.write_text(keep)
        xf = v6 / f"{s0}.prepared.xyz"
        kx = xf.read_text()
        xf.write_text(kx.replace(str(R.CELL_DIAG[2]), "10.5"))
        jf.write_text(json.dumps({**json.loads(keep), "prepared_sha256": R.sha256(xf)}))
        rc, txt = run(tmp / "prep_x")
        ck("⛔음성 준비 셀이 공통 셀이 아니다 → 2", rc == 2 and "공통 셀" in txt)
        xf.write_text(kx); jf.write_text(keep)
        (repo / "f.txt").write_text("b\n")
        rc, txt = run(tmp / "dirty")
        ck("⛔음성 작업트리에 커밋 안 된 수정 → 2", rc == 2 and "커밋 안 된" in txt)
        (repo / "f.txt").write_text("a\n")
        rc, txt = run(tmp / "allpass2")
        ck("복원 뒤 양성 다시 rc 0 (음성들이 고정 상태를 망가뜨리지 않았다)", rc == 0)
        rc, txt = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--status", "--out_root",
                                  str(tmp / "allpass")], capture_output=True, text=True).returncode, ""
        ck("--status: 읽기만 rc 0", rc == 0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"selftest {'PASS' if not fails else 'FAIL'} ({len(fails)} 실패)")
    return 0 if not fails else 1


def main() -> int:
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="cascade v7 탐침 러너 (개정 CP · 400 ps · 판독기가 다음 런을 고른다)")
    ap.add_argument("--out_root")
    ap.add_argument("--prep_root", help="v6 라운드 out_root (prep/<구조>.prepared.{json,xyz})")
    ap.add_argument("--python", default=sys.executable or "python3", help="uma env 의 절대경로 (드라이버·판독기 모두 이걸로)")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--dry_run", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--status", action="store_true", help="읽기만 — 진행·누적·마지막 판독 (D 없음)")
    ap.add_argument("--accept_flagged", action="append", default=[], metavar="TAG",
                    help="'확인 못 함' 표지가 뜬 런을 명시적으로 받아들인다 (budget.json 에 남는다)")
    ap.add_argument("--gpu_start_max_mib", type=int, default=16000)
    ap.add_argument("--gpu_wait_s", type=float, default=3 * 3600.0)
    ap.add_argument("--meta_wait_s", type=float, default=900.0)
    ap.add_argument("--poll_s", type=float, default=60.0)
    ap.add_argument("--heartbeat_s", type=float, default=1800.0)
    ap.add_argument("--gpu_log_s", type=float, default=600.0)
    ap.add_argument("--disk_min_gb", type=float, default=5.0)
    ap.add_argument("--selftest", action="store_true")
    for k in ("--_decisions", "--_judge", "--_driver", "--_struct_dir", "--_nvidia_smi", "--_repo"):
        ap.add_argument(k, help=argparse.SUPPRESS)  # 시험 주입 — 쓰이면 화면·manifest 에 남는다
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.out_root:
        ap.error("--out_root 가 필요하다")
    if a.status:
        return status(a)
    return run_probe(a)


if __name__ == "__main__":
    sys.exit(main())
