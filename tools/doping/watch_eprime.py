#!/usr/bin/env python3
"""watch_eprime.py — E′ 파일럿 한 화면 (run_eprime_pilot.py 의 감시용 짝).

    python3 tools/doping/watch_eprime.py --out_root $STORE/runs/eprime_2026_09_14
    watch -n 120 python3 tools/doping/watch_eprime.py --out_root ...
    python3 tools/doping/watch_eprime.py --selftest

왜 bash 가 아니라 python 인가
  `watch_eos_sweep.py`·`watch_all.py` 와 같은 이유다 — JSON 을 grep 으로 파면 중첩
  구조에서 **다른 블록의 첫 매치**를 집어 조용히 틀린 값을 띄운다.

왜 계획을 다시 안 적나
  구조·온도·시드·상한을 여기 베껴 두면 러너가 바뀔 때 **화면만 옛 계획을 보여준다**.
  그래서 `run_eprime_pilot.build_plan()` 을 그대로 불러 쓴다. 화면과 실행이 같은
  한 곳에서 나온다.

무엇을 보나
  ① 마스터가 살아 있나 (pgrep + 경과) · 로그 신선도
  ② 예산 — 누적 / 총상한, 속도 시험 실측 / 소상한, 남은 런 투영
  ③ 준비 5건 — 수렴 여부 · 최종 잔여힘 · 스텝수 (미수렴이면 그 쌍은 MD 를 안 돈다)
  ④ MD 30런 — 끝난 것은 D_Li, 도는 것은 md.log 의 누적 시간(205 ps 중), 안 시작한 것은 대기
  ⑤ GPU

⛔ 이 도구가 **못 하는 것**
  · **판정하지 않는다.** D 가 맞는지, Ea 가 물리적인지, 어느 쌍이 나은지 말하지 않는다.
    집계·자격·판정은 `msd_diffusive_check.aggregation_eligible` 쪽이고 여기가 아니다.
  · **왜 느린지 못 짚는다.** 누적 시간과 갱신 시각만 보인다. 느림·멈춤의 구분은
    `kb/platforms/v100_uma_setup_2026_09_14.md` 의 진단표를 쓴다.
  · **비용 상한을 집행하지 않는다.** 집행은 러너의 게이트다. 여기는 읽기만 한다.
  · md.log 의 `Time[ps]` 는 equilib(5) + prod(200) 누적이라 **생산 구간만 따로 못 센다**.\n  · prep 진행은 `--log` 를 줘야 보인다 (prep 은 md.log 를 안 만든다). 안 주면 '대기'\n    처럼 보이는데 그건 **모른다**는 뜻이지 안 돈다는 뜻이 아니다.
  · 남은 시간(ETA)을 예측하지 않는다 — 구조마다 원자수가 같아도 온도가 다르면
    스텝 속도가 달라진다. 투영은 러너가 속도 시험 실측으로 하는 것만 보여준다.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_eprime_pilot as EP                                   # noqa: E402

MISSING = "—"          # ⛔ 없는 값을 0 으로 그리지 않는다 (CLAUDE.md 코드 규율)
TOTAL_PS = EP.EQUILIB_PS + EP.PROD_PS


# ── 읽기 — "못 찾음" 과 "없음" 과 "깨짐" 을 구분한다 ──────────────────────────
def read_json(p) -> tuple[dict | None, str]:
    """→ (obj, 상태).  상태 ∈ {ok, 못찾음, 깨짐}.

    ⛔ 셋을 하나로 뭉개지 않는다. '파일이 없다'와 '파일이 깨졌다'는 다른 사건이고,
      뭉개면 다음 사람이 깨진 기록을 '아직 안 나왔다'로 읽는다.
    """
    f = Path(p)
    if not f.is_file():
        return None, "못찾음"
    try:
        return json.loads(f.read_text(encoding="utf-8")), "ok"
    except Exception as e:                                       # noqa: BLE001
        return None, f"깨짐({type(e).__name__})"


def age_str(path) -> str:
    f = Path(path)
    if not f.exists():
        return MISSING
    s = time.time() - f.stat().st_mtime
    if s < 90:
        return f"{int(s)}초 전"
    if s < 5400:
        return f"{s / 60:.0f}분 전"
    return f"{s / 3600:.1f}시간 전"


def pick_master(procs, self_pid, script="run_eprime_pilot.py", flag="--out_root"):
    """argv 목록에서 러너 프로세스를 고른다. procs = [(pid, [argv…])]. → pid 또는 None.

    ⛔ `pgrep -f '<패턴>'` 을 셸로 부르지 않는다. 그 셸 **자신의 명령줄에 패턴이 들어 있어서**
      pgrep 이 자기를 잡는다 — 아무것도 안 도는데 '마스터 ✅' 가 뜬다 (2026-09-14 실측).
    ⛔ 부분문자열로도 안 본다. `bash -c '<스크립트 본문>'` 은 argv 가 **세 개**인데 그 셋째에
      스크립트 전문이 통째로 들어 있어서, 본문 어딘가에 이 파일 이름이 적혀 있기만 하면
      걸린다 (이 파일을 편집하는 셸이 정확히 그랬다). **토큰이 그 값과 같아야** 한다.
    """
    for pid, argv in procs:
        if str(pid) == str(self_pid) or not argv:
            continue
        if any(a == script or a.endswith("/" + script) for a in argv) and flag in argv:
            return str(pid)
    return None


def proc_list() -> list[tuple[str, list[str]]]:
    out = []
    for d in Path("/proc").iterdir():
        if not d.name.isdigit():
            continue
        try:
            raw = (d / "cmdline").read_bytes()
        except OSError:                                          # 죽은 pid — 정상
            continue
        out.append((d.name, [x.decode("utf-8", "ignore")
                             for x in raw.split(b"\0") if x]))
    return out


def gpu_samples(n=6, dt=0.5) -> list[tuple[float, float]]:
    """(util %, mem MiB) 를 n 번 찍는다.

    ⛔ **한 번만 찍지 않는다.** 2026-09-14 에 같은 자리에서 세 번 틀렸다 — `0 %, 4 MiB`
      한 점을 보고 '멈췄다'고 경보를 울렸는데, 열 번 찍으니 `0,0,0,95,95,94,96,95,95,0`
      이었다. GPU util 은 표본이지 상태가 아니다.
    """
    out = []
    for i in range(max(1, n)):
        if i:
            time.sleep(dt)
        raw = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used "
                 "--format=csv,noheader,nounits")
        for line in raw.splitlines()[:1]:
            try:
                u, m = (x.strip() for x in line.split(","))
                out.append((float(u), float(m)))
            except ValueError:
                pass
    return out


def gpu_line(sams) -> str:
    """표본을 한 줄로. '못 찍었다' 와 '0 이었다' 를 구분한다."""
    if not sams:
        return "(nvidia-smi 못 읽음)"
    us = [u for u, _ in sams]
    ms = [m for _, m in sams]
    busy = sum(1 for u in us if u > 0)
    return (f"util {min(us):.0f}–{max(us):.0f} % (표본 {len(us)}개 중 {busy}개가 >0)"
            f" · mem {min(ms):.0f}–{max(ms):.0f} MiB")


def sh(cmd) -> str:
    try:
        return subprocess.run(cmd, shell=True, capture_output=True,
                              text=True, timeout=10).stdout.strip()
    except Exception:                                            # noqa: BLE001
        return ""


# ── ② 예산 ──────────────────────────────────────────────────────────────────
def budget_row(out_root) -> dict:
    b, st = read_json(Path(out_root) / "budget.json")
    if b is None:
        return {"상태": st, "used": None, "cap": EP.TOTAL_CAP_GPU_H,
                "perf": None, "n_done": None, "n_stopped": 0}
    steps = b.get("steps")
    steps = steps if isinstance(steps, list) else []
    # ⚠ used_gpu_h 는 **0.0 이 유효한 값**이다 (막 시작한 라운드). `or` 로 기본값을
    #   씌우면 0.0 이 '없음'으로 둔갑한다 — e_above_hull 사고와 같은 모양.
    used = b.get("used_gpu_h")
    perf = next((s.get("gpu_h") for s in steps if str(s.get("key", "")).endswith(
        f"{EP.PERF_RUN['structure']}__T{EP.PERF_RUN['temp']}__s{EP.PERF_RUN['seed']}")), None)
    return {"상태": "ok",
            "used": used if isinstance(used, (int, float)) else None,
            "cap": b.get("total_cap_gpu_h", EP.TOTAL_CAP_GPU_H),
            "perf": perf,
            "n_done": sum(1 for s in steps if "rc" in s),
            "n_stopped": sum(1 for s in steps if "stopped" in s),
            "stopped_why": [s["stopped"] for s in steps if "stopped" in s]}


# ── ③ 준비 ──────────────────────────────────────────────────────────────────
def prep_rows(out_root) -> list[dict]:
    rows = []
    for s in EP.STRUCTURES:
        j, st = read_json(Path(out_root) / "prep" / f"{s}.prepared.json")
        if j is None:
            rows.append({"구조": s, "상태": st, "conv": None,
                         "fmax": None, "steps": None, "min": None})
            continue
        rows.append({"구조": s, "상태": "ok",
                     "conv": j.get("converged"),
                     "fmax": j.get("final_fmax_eV_A"),
                     "steps": j.get("n_steps"),
                     "max_steps": j.get("max_steps"),
                     "min": (j["wall_s"] / 60.0) if isinstance(j.get("wall_s"),
                                                               (int, float)) else None})
    return rows


# ── ④ MD ────────────────────────────────────────────────────────────────────
def md_log_ps(path) -> tuple[float | None, str]:
    """md.log 의 마지막 `Time[ps]`.  → (ps, 사유).

    ⛔ 헤더만 있는 파일을 0 ps 로 읽지 않는다 — '0 ps 진행'과 '아직 한 줄도 안 씀'은
      다르다. 후자는 아직 equilib 첫 스텝도 못 돈 것이다.
    """
    f = Path(path)
    if not f.is_file():
        return None, "못찾음"
    try:
        tail = f.read_bytes()[-4096:].decode("utf-8", "ignore").split("\n")
    except Exception as e:                                       # noqa: BLE001
        return None, f"깨짐({type(e).__name__})"
    for line in reversed(tail):
        tok = line.split()
        if not tok:
            continue
        try:
            return float(tok[0]), "ok"
        except ValueError:
            continue                                             # 헤더 줄
    return None, "줄없음"


def md_rows(out_root, plan) -> list[dict]:
    """계획의 MD 스텝을 (구조·온도·시드) 런 단위로 펼친다.

    ⛔ 계획에 있는데 폴더가 없는 런을 **목록에서 빼지 않는다** — 조용히 사라지면
      '아직 안 돈 것'과 '계획에 없던 것'을 구분할 수 없다.
    """
    rows = []
    for st in plan:
        if not str(st.get("stage", "")).startswith("md"):
            continue
        tag = st["key"].split("/", 1)[1]
        base = Path(out_root) / "md" / tag
        for T in st["temps"]:
            cdir = base / "d0.00_cfg0" / f"T{int(T)}"
            j, jst = read_json(cdir / "msd.json")
            D = j.get("D_Li_cm2_s") if j else None
            ps, pst = md_log_ps(cdir / "md.log")
            rows.append({"구조": st["structure"], "T": int(T), "seed": st["seed"],
                         "perf": st["stage"] == "md_perf",
                         "D": D if isinstance(D, (int, float)) else None,
                         "D상태": jst if j is None else ("없음" if D is None else "ok"),
                         "ps": ps, "ps상태": pst,
                         "갱신": age_str(cdir / "md.log"), "dir": cdir})
    return rows


# ── 러너 로그 — prep 진행은 여기에만 있다 ────────────────────────────────────
def log_state(path) -> dict:
    """러너 stdout 로그에서 (지금 스텝, 그 스텝의 FIRE 마지막 줄) 을 읽는다.

    자식(`--_prep_one`)의 fd1/2 는 이 로그다. ASE Optimizer 는 줄마다 flush 하므로
    FIRE 진행이 실시간으로 여기 떨어진다 — prep 진행을 볼 곳은 **여기뿐**이다
    (prep 은 md.log 를 안 만든다).

    ⛔ **현재 스텝 뒤의 FIRE 줄만** 본다. 앞 스텝이 남긴 마지막 줄을 지금 진행으로
      읽으면 끝난 계산의 숫자를 도는 계산의 것으로 보여준다.
    """
    f = Path(path) if path else None
    if f is None or not f.is_file():
        return {"상태": "못찾음", "step": None, "fire": None, "phase": None}
    try:
        lines = f.read_text(encoding="utf-8", errors="ignore").split("\n")
    except OSError as e:
        return {"상태": f"깨짐({type(e).__name__})", "step": None, "fire": None,
                "phase": None}
    step, fire, phase = None, None, None
    for ln in lines:
        s = ln.strip()
        if s.startswith("▶ "):
            step, fire, phase = s[2:].split(" …")[0].strip(), None, None   # 새 스텝 → 초기화
        elif "Model is being compiled" in s and step is not None:
            phase = "컴파일"
        elif s.startswith("FIRE:") and step is not None:
            tok = s.split()
            if len(tok) >= 5:
                try:
                    fire = {"n": int(tok[1]), "E_eV": float(tok[3]),
                            "fmax_eV_A": float(tok[4])}
                    phase = "FIRE"
                except ValueError:
                    pass
    return {"상태": "ok", "step": step, "fire": fire, "phase": phase}


# ── 화면 ────────────────────────────────────────────────────────────────────
def fmt(v, spec="{:.3f}") -> str:
    return MISSING if v is None else spec.format(v)


def render(out_root, log=None, n_gpu=6) -> int:
    out_root = Path(out_root)
    print(f"════════ {time.strftime('%Y-%m-%d %H:%M:%S')}  E′ 파일럿 watch ════════")
    print(f"out_root: {out_root}")

    mani, mst = read_json(out_root / "manifest.json")
    print(f"code_id : {(mani or {}).get('code_id') or MISSING}   (manifest {mst})")

    # ① 마스터
    pid = pick_master(proc_list(), os.getpid())
    if pid:
        et = sh(f"ps -o etime= -p {pid}").strip()
        print(f"마스터 ✅ PID={pid} 가동 {et}")
    else:
        print("마스터 ⛔ 안 돎 (끝났거나 중단 — 아래 예산의 중단 사유를 본다)")
    if log:
        print(f"로그    : {log}  ({age_str(log)})")

    # ② 예산
    b = budget_row(out_root)
    if b["상태"] != "ok":
        print(f"\n── 예산 ── budget.json {b['상태']} "
              f"(아직 안 만들어졌으면 준비 첫 스텝 전이다)")
    else:
        print(f"\n── 예산 ── 누적 {fmt(b['used'], '{:.2f}')} / {b['cap']:.0f} GPU-h"
              f" · 완료 스텝 {b['n_done']}/{len(EP.STRUCTURES) + 11}"
              f" · 속도시험 {fmt(b['perf'], '{:.2f}')} / {EP.PERF_SUBCAP_GPU_H:.0f}")
        for w in b.get("stopped_why", []):
            print(f"   ⛔ 중단: {w}")

    # ③ 준비
    print("\n── 준비 (고정셀 FIRE, fmax 목표 "
          f"{EP.PREP_FMAX} eV/Å) ──")
    ls = log_state(log)
    if ls["상태"] == "ok" and ls["step"]:
        if ls["fire"]:
            fr = ls["fire"]
            print(f"  ▶ 지금: {ls['step']}  FIRE {fr['n']} 스텝 · "
                  f"fmax {fr['fmax_eV_A']:.4f} → 목표 {EP.PREP_FMAX} eV/Å · "
                  f"E {fr['E_eV']:.4f} eV")
        elif ls["phase"] == "컴파일":
            print(f"  ▶ 지금: {ls['step']}  **torch.compile 중** — 첫 스텝만 낸다"
                  f" (GPU util 이 0 과 95 를 오간다. 멈춘 게 아니다)")
        else:
            print(f"  ▶ 지금: {ls['step']}  (FIRE 줄도 컴파일 표시도 없음 — "
                  f"체크포인트 읽는 중일 수 있다. rchar 로 확인)")
    elif log:
        print(f"  (러너 로그 {ls['상태']})")
    for r in prep_rows(out_root):
        if r["상태"] != "ok":
            print(f"  {r['구조']:12s} {r['상태']}")
            continue
        mark = "✅" if r["conv"] is True else ("⛔미수렴" if r["conv"] is False else "?")
        print(f"  {r['구조']:12s} {mark:8s} fmax {fmt(r['fmax'], '{:.4f}')} eV/Å"
              f" · {r['steps']}/{r.get('max_steps')} 스텝 · {fmt(r['min'], '{:.1f}')} 분")

    # ④ MD
    plan = EP.build_plan(out_root)
    rows = md_rows(out_root, plan)
    done = sum(1 for r in rows if r["D"] is not None)
    print(f"\n── MD {done}/{len(rows)} 런 끝 (런당 {TOTAL_PS:.0f} ps = equilib "
          f"{EP.EQUILIB_PS:.0f} + prod {EP.PROD_PS:.0f}) ──")
    for r in rows:
        tagp = "★속도시험" if r["perf"] else "        "
        if r["D"] is not None:
            state = f"D_Li {r['D']:.3e} cm²/s"
        elif r["ps"] is not None:
            state = (f"도는 중 {r['ps']:6.1f}/{TOTAL_PS:.0f} ps "
                     f"({100 * r['ps'] / TOTAL_PS:4.1f} %) · {r['갱신']}")
        elif r["ps상태"] == "못찾음":
            state = "대기"
        else:
            state = f"시작했는데 진행줄 없음 ({r['ps상태']})"
        print(f"  {tagp} {r['구조']:12s} T{r['T']:<5d} s{r['seed']}  {state}")

    # ⑤ GPU
    print(f"\n── GPU ── {gpu_line(gpu_samples(n_gpu))}")
    if n_gpu <= 1:
        print("   ⚠ 표본 1개 — 0 % 가 나와도 '멈췄다'로 읽지 마라 (--gpu_n 을 올려라)")
    return 0


# ── selftest — 음성 경로 포함 ────────────────────────────────────────────────
def _selftest() -> int:
    import tempfile
    bad, _n = [], [0]

    def chk(cond, msg):
        _n[0] += 1
        print(("  ✓ " if cond else "  ✗ ") + msg)
        if not cond:
            bad.append(msg)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        # ── 예산: 파일이 없을 때 0 으로 그리지 않는다 ──
        b = budget_row(root)
        chk(b["상태"] == "못찾음" and b["used"] is None,
            "⛔음성: budget.json 이 없으면 '못찾음'이고 used 는 None 이다 (0 아님)")
        chk(fmt(b["used"], "{:.2f}") == MISSING,
            f"⛔음성: 없는 누적을 '{MISSING}' 로 그린다 (0.00 으로 그리지 않는다)")

        # ── 예산: 0.0 은 **유효한 값**이다 ──
        (root / "budget.json").write_text(json.dumps(
            {"total_cap_gpu_h": 120.0, "used_gpu_h": 0.0, "steps": []}), encoding="utf-8")
        b = budget_row(root)
        chk(b["used"] == 0.0 and fmt(b["used"], "{:.2f}") == "0.00",
            "양성: 누적 0.0 은 유효값이라 '0.00' 으로 나온다 (— 로 둔갑하지 않는다)")

        # ── 예산: 깨진 JSON 은 '없음'이 아니라 '깨짐' ──
        (root / "budget.json").write_text("{not json", encoding="utf-8")
        chk(budget_row(root)["상태"].startswith("깨짐"),
            "⛔음성: 깨진 budget.json 을 '못찾음'으로 뭉개지 않는다")

        # ── 예산: 속도 시험 실측과 중단 사유를 집어낸다 ──
        (root / "budget.json").write_text(json.dumps({
            "total_cap_gpu_h": 120.0, "used_gpu_h": 3.5,
            "steps": [{"key": "prep/H0_host", "rc": 0, "gpu_h": 0.2},
                      {"key": f"md/{EP.PERF_RUN['structure']}__T"
                              f"{EP.PERF_RUN['temp']}__s{EP.PERF_RUN['seed']}",
                       "rc": 0, "gpu_h": 3.3},
                      {"key": "md/x", "stopped": "투영이 총상한을 넘는다"}]}),
            encoding="utf-8")
        b = budget_row(root)
        chk(b["perf"] == 3.3, "양성: 속도 시험 스텝의 실측 GPU-h 를 찾는다")
        chk(b["n_done"] == 2 and b["n_stopped"] == 1 and b["stopped_why"],
            "양성: 완료·중단 스텝을 나눠 세고 중단 사유를 들고 온다")

        # ── 준비: 미수렴을 수렴으로 읽지 않는다 ──
        pd = root / "prep"
        pd.mkdir()
        (pd / "H0_host.prepared.json").write_text(json.dumps(
            {"converged": False, "final_fmax_eV_A": 0.31, "n_steps": 3000,
             "max_steps": 3000, "wall_s": 600.0}), encoding="utf-8")
        rows = {r["구조"]: r for r in prep_rows(root)}
        chk(rows["H0_host"]["conv"] is False and rows["H0_host"]["fmax"] == 0.31,
            "⛔음성: 미수렴 준비를 그대로 미수렴으로 읽는다")
        chk(rows["P1_Al2O3_A"]["상태"] == "못찾음" and rows["P1_Al2O3_A"]["conv"] is None,
            "⛔음성: 아직 없는 준비를 '수렴 아님'이 아니라 '못찾음'으로 둔다")
        chk(len(prep_rows(root)) == len(EP.STRUCTURES),
            "양성: 준비 행은 언제나 다섯이다 (없는 것을 목록에서 빼지 않는다)")

        # ── md.log: 헤더만 있는 파일을 0 ps 로 읽지 않는다 ──
        cd = root / "md" / f"{EP.PERF_RUN['structure']}__T{EP.PERF_RUN['temp']}__s" \
                           f"{EP.PERF_RUN['seed']}" / "d0.00_cfg0" / f"T{EP.PERF_RUN['temp']}"
        cd.mkdir(parents=True)
        (cd / "md.log").write_text(
            "Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]\n", encoding="utf-8")
        ps, st = md_log_ps(cd / "md.log")
        chk(ps is None and st == "줄없음",
            "⛔음성: 헤더만 있는 md.log 를 '0 ps 진행'으로 읽지 않는다")
        (cd / "md.log").write_text(
            "Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]\n"
            "0.0000       -1.0         -2.0          1.0       600.0\n"
            "12.3400      -1.1         -2.1          1.0       601.0\n", encoding="utf-8")
        ps, st = md_log_ps(cd / "md.log")
        chk(abs(ps - 12.34) < 1e-9 and st == "ok", "양성: 마지막 Time[ps] 를 읽는다")
        chk(md_log_ps(cd / "없는파일.log")[1] == "못찾음",
            "⛔음성: 없는 md.log 를 '줄없음'과 구분한다")

        # ── MD 행: 계획 전체가 나오고, 안 시작한 런도 남는다 ──
        plan = EP.build_plan(root)
        rows = md_rows(root, plan)
        chk(len(rows) == EP.plan_run_count(plan) == 30,
            f"양성: MD 행이 계획 런 수와 같다 (실제 {len(rows)})")
        chk(sum(1 for r in rows if r["ps상태"] == "못찾음") == 29,
            "⛔음성: 시작 안 한 29런이 '대기'로 남는다 (목록에서 사라지지 않는다)")
        chk(sum(1 for r in rows if r["perf"]) == 1,
            "양성: 속도 시험 런이 정확히 하나로 표시된다")

        # ── msd.json 의 D 가 null 이면 '없음'이지 0 이 아니다 ──
        (cd / "msd.json").write_text(json.dumps({"T_K": 600, "D_Li_cm2_s": None}),
                                     encoding="utf-8")
        r = next(r for r in md_rows(root, plan) if r["perf"])
        chk(r["D"] is None and r["D상태"] == "없음",
            "⛔음성: D 가 null 이면 '없음' 이다 (0 으로 그리지 않는다)")
        (cd / "msd.json").write_text(json.dumps({"T_K": 600, "D_Li_cm2_s": 1.5e-6}),
                                     encoding="utf-8")
        r = next(r for r in md_rows(root, plan) if r["perf"])
        chk(r["D"] == 1.5e-6 and r["D상태"] == "ok", "양성: D 가 있으면 그 값을 읽는다")

        # ── 마스터 탐지: 자기 자신도, 이름만 품은 셸도 잡지 않는다 ──
        SELF = "4242"
        SHELL_BODY = ("python3 tools/doping/run_eprime_pilot.py --out_root /x\n"
                      "echo done")          # 셸의 셋째 argv 에 통째로 들어 있는 본문
        procs = [
            (SELF, ["python3", "tools/doping/watch_eprime.py", "--out_root", "/x"]),
            ("7", ["bash", "-c", SHELL_BODY]),
            ("8", ["python3", "tools/doping/watch_eprime.py", "--out_root", "/x"]),
        ]
        chk(pick_master(procs, SELF) is None,
            "⛔음성: 러너 이름을 **본문에 품은 셸**을 마스터로 잡지 않는다 (토큰 일치만 센다)")
        chk(pick_master(procs + [("99", ["python3", "/a/b/run_eprime_pilot.py",
                                         "--out_root", "/x", "--device", "cuda"])],
                        SELF) == "99",
            "양성: 진짜 러너 프로세스는 절대경로여도 잡는다")
        chk(pick_master([(SELF, ["python3", "tools/doping/run_eprime_pilot.py",
                                 "--out_root", "/x"])], SELF) is None,
            "⛔음성: 자기 pid 는 건너뛴다")
        chk(pick_master([("5", ["python3", "tools/doping/run_eprime_pilot.py",
                                "--selftest"])], SELF) is None,
            "⛔음성: --out_root 없이 도는 selftest 를 라운드로 착각하지 않는다")

        # ── 러너 로그: 앞 스텝의 FIRE 줄을 지금 진행으로 읽지 않는다 ──
        lg = root / "runner.log"
        lg.write_text(
            "계획: 준비 5건 · MD 호출 11건 = **30런**\n"
            "▶ prep/H0_host …\n"
            "      Step     Time          Energy          fmax\n"
            "FIRE:    0 01:48:03    -1234.567890        1.2345\n"
            "FIRE:   40 01:52:11    -1240.100000        0.0300\n"
            "  ← rc=0 · 0.30 GPU-h · 누적 0.30 / 120\n"
            "▶ prep/P1_Al2O3_A …\n", encoding="utf-8")
        s = log_state(lg)
        chk(s["step"] == "prep/P1_Al2O3_A",
            "양성: 로그의 **마지막** ▶ 스텝을 현재 스텝으로 읽는다")
        chk(s["fire"] is None,
            "⛔음성: 앞 스텝이 남긴 FIRE 줄을 지금 진행으로 읽지 않는다")
        lg.write_text(lg.read_text(encoding="utf-8")
                      + "FIRE:    7 01:53:00    -1300.000000        0.4400\n",
                      encoding="utf-8")
        s = log_state(lg)
        chk(s["fire"] == {"n": 7, "E_eV": -1300.0, "fmax_eV_A": 0.44},
            "양성: 현재 스텝의 FIRE 줄은 읽는다 (스텝·E·fmax)")
        chk(log_state(root / "없는.log")["상태"] == "못찾음" and
            log_state(None)["상태"] == "못찾음",
            "⛔음성: 로그가 없으면 '못찾음' 이다 (0 스텝으로 그리지 않는다)")

        # ── 컴파일 단계를 FIRE 진행으로 착각하지 않는다 ──
        lg.write_text(
            "▶ prep/H0_host …\n"
            "WARNING:root:Model is being compiled this might take a while for the first time\n",
            encoding="utf-8")
        s = log_state(lg)
        chk(s["phase"] == "컴파일" and s["fire"] is None,
            "양성: torch.compile 중임을 읽는다 (FIRE 0 스텝으로 그리지 않는다)")
        lg.write_text(lg.read_text(encoding="utf-8")
                      + "FIRE:    0 01:59:00    -1300.000000        1.1000\n",
                      encoding="utf-8")
        chk(log_state(lg)["phase"] == "FIRE",
            "양성: FIRE 줄이 뜨면 단계가 컴파일→FIRE 로 넘어간다")
        lg.write_text(lg.read_text(encoding="utf-8") + "▶ prep/P1_Al2O3_A …\n",
                      encoding="utf-8")
        chk(log_state(lg)["phase"] is None,
            "⛔음성: 새 스텝에서 단계가 초기화된다 (앞 스텝의 컴파일 표시가 안 새어 나온다)")

        # ── GPU: '못 찍음' 과 '0 이었음' 을 구분한다 ──
        chk(gpu_line([]) == "(nvidia-smi 못 읽음)",
            "⛔음성: GPU 를 못 찍은 것을 '0 %' 로 그리지 않는다")
        chk("6개 중 0개가 >0" in gpu_line([(0.0, 10.0)] * 6),
            "양성: 표본이 전부 0 이면 그렇게 적는다 (표본 수를 같이 보여준다)")
        chk("6개 중 3개가 >0" in gpu_line(
            [(0.0, 10.0), (0.0, 10.0), (95.0, 20.0), (94.0, 20.0), (96.0, 30.0), (0.0, 30.0)]),
            "양성: 0 과 95 가 섞이면 '몇 개가 >0' 로 보여준다 (한 점으로 판단 못 하게)")

        # ── 계획을 베끼지 않았다는 증거: 러너의 상수와 같은 것을 쓴다 ──
        chk(TOTAL_PS == EP.EQUILIB_PS + EP.PROD_PS == 205.0,
            "양성: 런 길이를 러너 상수에서 가져온다 (여기 숫자를 따로 안 적는다)")

    print(f"selftest {_n[0] - len(bad)}/{_n[0]} · "
          + ("FAIL: " + "; ".join(bad) if bad else "PASS"))
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="E′ 파일럿 감시 (판정하지 않는다)")
    ap.add_argument("--out_root", default=None)
    ap.add_argument("--log", default=None, help="러너 stdout 로그 (신선도 표시용)")
    ap.add_argument("--gpu_n", type=int, default=6,
                    help="GPU 표본 수 (기본 6 — 한 점으로 판단하지 않는다)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.out_root:
        ap.error("--out_root 가 필요하다")
    return render(a.out_root, a.log, a.gpu_n)


if __name__ == "__main__":
    raise SystemExit(main())
