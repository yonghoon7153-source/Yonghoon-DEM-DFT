#!/usr/bin/env python3
"""run_eos_10sweep.py — §4b 구조 저장용 진단 **한 라운드** (회신 BQ-3 Q5·Q6 사양, 2026-09-13).

    python3 tools/doping/run_eos_10sweep.py --dry_run
    python3 tools/doping/run_eos_10sweep.py --python ~/miniforge3/envs/uma/bin/python

무엇을 하나
  5구조 × {W3_f02, W3_f005} = **10스윕**. 같은 ±3 % 창·같은 7점·같은 연쇄 양방향 규칙·
  같은 모델·추론·스텝 한도. **힘 문턱만** 다르다 (0.02 vs 0.005).
  점별 프레임 저장 + 최근접 수렴점 승계는 run_mlip_postproc.py 가 한다 (--apply_eos_v0).

⛔ 이 라운드가 **하지 않는 것** (회신 BQ-3 Q6 중단 규칙)
  · 조건·분율·창을 CLI 로 바꿀 수 없다 — **코드에 동결**돼 있다. 실패했다고 창·시드·문턱을
    넓히는 길을 구조적으로 막는다. 바꾸려면 코드를 고치고 커밋해야 한다 (= 새 라운드).
  · 결과를 보고 구조별로 유리한 조건을 골라 섞지 않는다. 집계는 **조건별 5/5 여부**다.
  · MD·탄성으로 자동 진행하지 않는다 (--no_anneal --no_elastic 고정, MD 호출 없음).
  · 기존 결과 폴더를 재사용하지 않는다 — out_root 는 매 실행 새로 만든다.
  · **판정하지 않는다.** round_closed.json 은 자격 집계와 종료 문구 후보를 적을 뿐이다.
    "준비 확보" / "정한 준비법·비용 안에서 v4 파일럿 준비 미확보" 는 사람이 고른다.
"""
import argparse, hashlib, json, os, subprocess, sys, time
from pathlib import Path

# ── 동결 사양 (회신 BQ-3 Q5-1) — 바꾸려면 커밋이 필요하다 ─────────────────────
FRACTIONS = (0.97, 0.98, 0.99, 1.00, 1.01, 1.02, 1.03)
CONDITIONS = {"W3_f02": 0.02, "W3_f005": 0.005}          # 힘 문턱만 다르다
RELAX_STEPS = 3000
STRUCTURES = ["H0_host", "P1_Al2O3_A", "P1_Al2O3_B", "P2_Al2S3_A", "P2_Al2S3_B"]
STRUCT_DIR = Path("db/structures/cascade_pilot")
FIXED_FLAGS = ["--no_anneal", "--no_elastic", "--eos_continuation", "--apply_eos_v0",
               "--fixed_shape_relax"]

REPO = Path(__file__).resolve().parents[2]
POSTPROC = REPO / "tools" / "doping" / "run_mlip_postproc.py"


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def build_plan(out_root, python, device, task, uma_mode):
    """조건 2개 × 명령 1개씩. 구조 5개는 한 명령에 같이 넘긴다 (지난 스윕과 같은 모양)."""
    xyz = [STRUCT_DIR / f"{s}.xyz" for s in STRUCTURES]
    plan = []
    for cond, fmax in CONDITIONS.items():
        cmd = [python, str(POSTPROC), "--xyz", *map(str, xyz),
               "--out", str(Path(out_root) / cond),
               "--device", device, "--task", task,
               *FIXED_FLAGS,
               "--eos_fractions", *(f"{f:.2f}" for f in FRACTIONS),
               "--eos_fmax", str(fmax), "--relax_steps", str(RELAX_STEPS),
               "--run_tag", cond]
        if uma_mode:
            cmd += ["--uma_mode", uma_mode]
        plan.append({"condition": cond, "fmax": fmax, "cmd": cmd})
    return plan


def manifest(out_root, plan):
    xyz = [STRUCT_DIR / f"{s}.xyz" for s in STRUCTURES]
    try:
        code = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                              text=True, timeout=10).stdout.strip() or None
    except Exception:                                        # noqa: BLE001
        code = None
    return {"schema": 1, "kind": "eos_10sweep_round", "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "frozen": {"fractions": list(FRACTIONS), "conditions": CONDITIONS,
                       "relax_steps": RELAX_STEPS, "fixed_flags": FIXED_FLAGS,
                       "structures": STRUCTURES},
            "inputs_sha256": {s: (sha256(x) if x.exists() else None) for s, x in zip(STRUCTURES, xyz)},
            "code_git": code, "postproc_sha256": (sha256(POSTPROC) if POSTPROC.exists() else None),
            "out_root": str(out_root),
            "stop_rules": ["한 라운드로 고정 — 조건·분율·창 CLI 변경 불가",
                           "구조별 유리한 조건 골라 섞지 않음 — 집계는 조건별 5/5",
                           "실패 시 창·시드·문턱 자동 확대 없음",
                           "MD·탄성 자동 진행 없음"],
            "declared_differences_from_25row_sweep": {
                "--fixed_shape_relax": ("25줄 스윕(40ffa697)은 이 플래그가 **없었다** — 0단계 완화가 "
                                        "형상 무제한 CellFilter(GAP-2)였다. 카드 v4 §4b ①③ 은 고정셀을 "
                                        "요구하므로 이번 라운드는 켠다. ⇒ 25줄과 **직접 비교 불가** 축이다"),
                "--apply_eos_v0": "25줄 스윕은 V₀ 를 적용하지 않았다. 이번엔 최근접 수렴점 승계까지 돈다",
                "code": "회신 BQ-2·BQ-3 이행본 (자격·양방향 수렴·1:1 대응·유한 힘·점별 프레임)"},
            "closure_options": ["준비 확보 (어느 한 조건에서 5/5 자격)",
                                "정한 준비법·비용 안에서 v4 파일럿 준비 미확보"],
            "⛔": "이 파일은 판정하지 않는다. 종료 문구는 사람이 고른다 (회신 BQ-3 Q6)"}


def prepared(rec):
    """한 기록이 **준비됐는가** — EOS 자격만이 아니라 최종 적용·수렴·후속 입력까지.

    ⛔⛔ 회신 BQ-4 Q1 P1-② (2026-09-13) — 종전 tally 는 `eos.downstream_eligible` 만 셌다.
      EOS 는 통과했지만 최종 V₀ 완화가 **차단**된 기록 다섯 개를 넣어도 `all_five=true` 가
      나왔다. "준비 확보" 는 후속 입력 파일이 실제로 있어야 성립한다.
    ⛔ 못 하는 것: 파일의 해시를 원본과 대조하지 않는다 — 기록에 적힌 이름과 플래그만 본다.
      (리뷰어도 최종 파일의 해시·부재까지는 확인하지 않았다고 적었다.)
    반환: True / False / None(기록을 못 읽음 — 없는 것을 있다고도 없다고도 하지 않는다)
    """
    if not isinstance(rec, dict):
        return None
    e = rec.get("eos") or {}
    cp = rec.get("cell_policy") or {}
    sw = rec.get("structures_written") or {}
    return bool(e.get("downstream_eligible") is True
                and cp.get("eos_v0_applied") is True
                and cp.get("downstream_blocked") is False
                and (cp.get("apply_report") or {}).get("converged") is True
                and "final_v0_applied.xyz" in sw)


def tally(out_root):
    """조건별 **준비** 집계 — 판정이 아니라 **세기**다. 무엇을 세는지는 `prepared()`."""
    res = {}
    for cond in CONDITIONS:
        rows = {}
        for s in STRUCTURES:
            f = Path(out_root) / cond / s / "postproc.json"
            if not f.exists():
                rows[s] = None
                continue
            try:
                rows[s] = prepared(json.loads(f.read_text()))
            except Exception:                                # noqa: BLE001
                rows[s] = None
        n_ok = sum(1 for v in rows.values() if v is True)
        res[cond] = {"eligible": rows, "n_eligible": n_ok, "all_five": n_ok == len(STRUCTURES)}
    return res


def _selftest():
    ok = fail = 0
    def chk(c, m):
        nonlocal ok, fail
        ok += c; fail += (not c); print(("  ✓ " if c else "  ⛔ ") + m)
    import tempfile
    plan = build_plan("/tmp/x", "python3", "cuda", "omat", None)
    chk(len(plan) == 2 and {p["condition"] for p in plan} == set(CONDITIONS),
        "조건 2개 = 명령 2개")
    c0, c1 = plan[0]["cmd"], plan[1]["cmd"]
    d = [i for i, (a, b) in enumerate(zip(c0, c1)) if a != b]
    chk(len(c0) == len(c1) and all(c0[i - 1] in ("--eos_fmax", "--run_tag", "--out") for i in d),
        "⛔음성: 두 명령의 차이는 **fmax·run_tag·out 뿐**이다 (창·점·스텝·플래그 동일)")
    chk("--no_anneal" in c0 and "--no_elastic" in c0 and "--apply_eos_v0" in c0,
        "MD·탄성 없음 · V₀ 승계 있음이 명령에 박혀 있다")
    chk(all(x not in " ".join(c0) for x in ("--n_eos_seeds", "0.94", "1.06")),
        "⛔음성: 시드 확대·±6 % 창이 명령에 없다 (동결)")
    ap = _parser()
    chk(all(o.dest not in ("fractions", "conditions", "relax_steps") for o in ap._actions),
        "⛔음성: 분율·조건·스텝을 바꾸는 CLI 플래그가 **존재하지 않는다**")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "diag"
        root.mkdir()
        (root / "W3_f02" / "H0_host").mkdir(parents=True)
        # ⚠ 회신 BQ-4 P1-② 이후 fixture 는 **준비 완료** 기록이어야 1 로 센다 —
        #   종전 fixture(`eos.downstream_eligible` 만)는 옛 집계의 구멍을 방어하고 있었다.
        (root / "W3_f02" / "H0_host" / "postproc.json").write_text(json.dumps(
            {"eos": {"downstream_eligible": True},
             "cell_policy": {"eos_v0_applied": True, "downstream_blocked": False,
                             "apply_report": {"converged": True}},
             "structures_written": {"final_v0_applied.xyz": "x"}}))
        t = tally(root)
        chk(t["W3_f02"]["n_eligible"] == 1 and t["W3_f02"]["all_five"] is False
            and t["W3_f005"]["n_eligible"] == 0,
            "집계: 1/5 는 all_five=False, 없는 조건은 0 (없는 것을 있다고 안 한다)")
        chk(t["W3_f02"]["eligible"]["P1_Al2O3_A"] is None,
            "⛔음성: 결과 없는 구조는 None 이지 False 가 아니다")
        # 회신 BQ-4 Q1 P1-② — EOS 자격만으로 all_five 가 되면 안 된다
        _full = {"eos": {"downstream_eligible": True},
                 "cell_policy": {"eos_v0_applied": True, "downstream_blocked": False,
                                 "apply_report": {"converged": True}},
                 "structures_written": {"final_v0_applied.xyz": "x"}}
        _eos_only = {"eos": {"downstream_eligible": True},
                     "cell_policy": {"eos_v0_applied": False, "downstream_blocked": True},
                     "structures_written": {"DIAGNOSTIC_blocked_not_for_downstream.xyz": "x"}}
        for s in STRUCTURES:
            (root / "W3_f005" / s).mkdir(parents=True)
            (root / "W3_f005" / s / "postproc.json").write_text(json.dumps(_eos_only))
        t2 = tally(root)
        chk(t2["W3_f005"]["n_eligible"] == 0 and t2["W3_f005"]["all_five"] is False,
            "⛔음성 BQ-4 P1-②: EOS 자격은 있는데 최종 V₀ 적용이 차단된 5줄은 **0/5** 다 (all_five 아님)")
        for s in STRUCTURES:
            (root / "W3_f005" / s / "postproc.json").write_text(json.dumps(_full))
        chk(tally(root)["W3_f005"]["all_five"] is True,
            "양성: 적용·수렴·최종 파일까지 갖춘 5줄은 all_five")
        chk(prepared({"eos": {"downstream_eligible": True}}) is False and prepared("x") is None,
            "⛔음성: 자격 필드만 있는 기록은 False · 기록이 아닌 것은 None")
        _nofile = json.loads(json.dumps(_full)); _nofile["structures_written"] = {}
        chk(prepared(_nofile) is False,
            "⛔음성: 플래그가 다 참이어도 final_v0_applied.xyz 가 기록에 없으면 준비 아님")
        try:
            _refuse_existing(root); r = False
        except SystemExit:
            r = True
        chk(r, "⛔음성: 이미 있는 out_root 는 거부한다 (폴더 재사용 금지)")
    m = manifest("/tmp/x", plan)
    chk(m["frozen"]["fractions"] == list(FRACTIONS) and "판정하지 않는다" in m["⛔"],
        "manifest 에 동결 사양과 '판정하지 않는다' 가 박힌다")
    print(f"  selftest: ⭕ {ok} · ⛔ {fail}")
    return 0 if fail == 0 else 1


def _refuse_existing(out_root):
    if Path(out_root).exists():
        raise SystemExit(f"⛔ out_root 가 이미 있다: {out_root} — 재사용 금지. 새 경로를 써라.")


def _parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--python", default=sys.executable, help="UMA 환경의 python 절대경로")
    ap.add_argument("--out_root", default=None,
                    help="기본 runs/cascade_pilot/diag10_<시각> — 매 실행 새 폴더")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--task", default="omat")
    ap.add_argument("--uma_mode", default=None, help="선언적 추론 설정 (기록됨)")
    ap.add_argument("--dry_run", action="store_true", help="명령만 찍고 돌리지 않는다")
    ap.add_argument("--selftest", action="store_true")
    return ap


def main():
    a = _parser().parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    out_root = Path(a.out_root or f"runs/cascade_pilot/diag10_{time.strftime('%m%d_%H%M%S')}")
    _refuse_existing(out_root)
    plan = build_plan(out_root, a.python, a.device, a.task, a.uma_mode)
    if a.dry_run:
        for p in plan:
            print(f"# {p['condition']} (fmax {p['fmax']})\n  " + " ".join(p["cmd"]) + "\n")
        print(json.dumps(manifest(out_root, plan)["frozen"], ensure_ascii=False, indent=1))
        return
    out_root.mkdir(parents=True)
    (out_root / "manifest.json").write_text(json.dumps(manifest(out_root, plan), ensure_ascii=False, indent=2))
    # 중복 실행 가드 — pgrep 이 아니라 flock (CLAUDE.md 관례: 래퍼까지 세어 즉사한 사고)
    import fcntl
    lock = open(out_root.parent / ".eos_10sweep.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise SystemExit("⛔ 다른 10스윕이 돌고 있다 (flock). 끝나길 기다려라.")
    log = out_root / "driver.log"
    for p in plan:
        with log.open("a") as lf:
            lf.write(f"######## {p['condition']} fmax={p['fmax']} {time.strftime('%H:%M:%S')}\n")
        print(f"######## {p['condition']} fmax={p['fmax']} {time.strftime('%H:%M:%S')}", flush=True)
        rc = subprocess.call(p["cmd"], cwd=REPO)
        with log.open("a") as lf:
            lf.write(f"  rc={rc} {time.strftime('%H:%M:%S')}\n")
        # ⛔ 실패해도 확대하지 않는다 — 기록하고 다음 조건으로
    res = {"tally": tally(out_root), "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "⛔": "판정 아님 — 종료 문구는 사람이 고른다: " + " / ".join(manifest(out_root, plan)["closure_options"])}
    (out_root / "round_closed.json").write_text(json.dumps(res, ensure_ascii=False, indent=2))
    print(json.dumps(res["tally"], ensure_ascii=False, indent=1))
    print(f"ALLDONE {time.strftime('%H:%M:%S')} → {out_root}/round_closed.json")


if __name__ == "__main__":
    main()
