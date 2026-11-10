#!/bin/bash
# =============================================================================
# run_stage2_kgy_v2.sh — li2s-3 2 단계 고친 큐 v2 (리뷰 DZ 최소 조건 · 내부 리뷰 EB · 결과 전)
#   카드 db/properties/lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json (기계_판독_값 · 개정_DZ_회신 · 개정_EB)
#   두 갈래 (사람이 PHASE 를 준다 — 큐가 스스로 정하지 않는다)
#     PHASE=cond550  조건부 550 K · 800 ps · A · B × 11 · 12 (카드 stage2.conditional) — 고정 판독 기록
#                    (READOUT_RECORD + READOUT_SHA256) 이 '두 계 모두 600 K 측정 가능' 을 보일 때만 (카드 cond550_Q6)
#     PHASE=rerun    판정 보류 기록 (HOLD_RECORD + HOLD_SHA256) 에 invalid · incomplete 로 적힌 런만 (RERUN='A:11:600 …') ·
#                    같은 카드 값 · 옛 런 폴더는 지우지 않고 '<T>.superseded_<UTC>' 로 옮겨 남긴다
#   v1 큐 (run_stage2_kgy.sh) 는 그대로다 — 같은 잠금 ($BASE/.stage2.lock) 을 v1 이 (또는 v1 의 드라이버가) 쥐고 있으면
#   시작하지 않는다. v2 는 옛 러너 (glass_kgy_q_v2.sh — 드라이버 종료 코드를 삼킨다 · 리뷰 DZ P1-1) 를 거치지 않고
#   드라이버를 직접 부른다 — 러너 사본이 따로 없다 (이 파일이 실행 경로다 · 카드 stage2.queue_v2.sha16 이 이 파일을 고정한다).
#
# 리뷰 DZ P1 반례 → v2
#   P1-1 실패 · 깨진 파일을 완료로      → 완료 = 드라이버 종료 코드 0 ∧ 필수 산출물 (run_meta · ensemble_results 끝 요약 ·
#                                        config.xyz = init · aimd · traj 프레임 수 · md.log · msd.json 배열) · 실행 기록 없는
#                                        폴더는 건너뛰지 않는다 (거부) · 실패는 끝 기록 + 장부 + 멈춤 기록
#   P1-2 재시작으로 첫 런 한도 우회     → 멈춤 기록 ($BASE/queue_v2_stops.jsonl) 을 영구로 남기고 시작 때 본다 — 다시 띄우려면
#                                        ACK_STOP · ACK_BY · ACK_REASON (사람 결정 · 기록) · 첫 런 한도는 기록에서 다시 판정
#   P1-3 비용 미확정 = 0 · 길이 무시   → 장부 (v1 의 cost_ledger.tsv 를 이어 쓴다) 와 실행 흔적을 맞춘다 — 흔적이 있는데 장부
#                                        행이 없거나 장부가 깨졌으면 시작하지 않는다 (COST_CHARGE 로 사람이 정해 기록하기 전에는) ·
#                                        다음 런 어림 = max(카드 cost_estimate_h_per_ps, 장부의 최대 h/ps) × 그 런의 prod
#   P1-4 실행 설정 ≠ 카드              → 온도 · 길이 · 시드 · 계 · 난수 offset · 상한 · 한도는 카드 기계 값에서만 (환경변수로 못 바꾼다)
#   P1-5 GPU 대기 뒤 입력 결속         → 런마다 GPU 대기 **뒤 · 실행 직전에** 카드 · 큐 파일 · 드라이버 · 입력을 다시 해시 ·
#                                        시작 뒤 드라이버가 쓴 run_meta · config.xyz (= init) · md.log dt · 실제 추론 모드를 확인
#   런마다 실행 기록 (런 폴더) exec_v2_start.json (실행 전) · exec_v2_end.json (실행 뒤) — 큐 · 드라이버 sha16 · 카드 sha256 ·
#   카드 값 · 입력 sha256 · 실제 명령 인수 · 시작 / 끝 · 드라이버 종료 코드 · GPU-h · 산출물 sha256 · 장부 행
#   (판독 도구 li2s3_stage2_readout.py 가 이 기록으로 v2 런을 읽는다 — v1 런은 러너 로그로)
#
# 쓰는 법 (kgy · 큐가 돈 worktree 가 아닌 새 worktree 에서 · tmux 안에서)
#   bash db/inputs/li2s3_dense_ensemble_2026_11_10/run_stage2_kgy_v2.sh --selftest      # PY = numpy · ase 있는 python
#   DRY_RUN=1 PHASE=cond550 READOUT_RECORD=… READOUT_SHA256=… bash …/run_stage2_kgy_v2.sh  # 검사 · 계획만 (아무것도 안 쓴다)
#   PHASE=cond550 READOUT_RECORD=… READOUT_SHA256=… bash …/run_stage2_kgy_v2.sh
#   PHASE=rerun RERUN='A:11:600' HOLD_RECORD=… HOLD_SHA256=… bash …/run_stage2_kgy_v2.sh
#   멈춘 뒤 이어서:  ACK_STOP=<멈춤 id> ACK_BY=<누가> ACK_REASON=<왜> + 같은 명령
#   비용 미확정 흔적:  COST_CHARGE='A/seed11/T600=5.2' COST_BY=<누가> COST_REASON=<근거> + 같은 명령 (장부에 'charge' 행)
#   그 밖 환경변수: BASE · SRC · CARD · DECISIONS · PY · POLL · GPU_WAIT · META_WAIT (과학 값은 카드에서만)
#
# 종료 코드: 0 끝 · 2 사용법 · 4 런 실패 (멈춤) · 6 카드 · 결정 · 7 큐 · 드라이버 sha · 8 입력 (없음 · 바뀜 — 실행 직전 다시 해시 ·
#   멈춤) · 9 실행 설정이 카드와 다르다 (드라이버를 세운다 · 멈춤) · 10 잠금 (v1 · 다른 큐) · 12 GPU 대기 초과 (멈춤) ·
#   13 PHASE · RERUN 꼴 · 14 풀리지 않은 멈춤 · 15 비용 미확정 · 16 결속 기록 (판독 · 보류) 이 조건을 못 채운다 ·
#   17 이미 있는 런 폴더를 이 갈래가 받을 수 없다 · 21 첫 런 한도 (멈춤) · 22 상한 (멈춤) · 23 기록 · 장부를 못 썼다 (멈춤)
#
# ⛔ 이 파일이 못 하는 것
#   · 결과를 판정하지 않는다 (C1 · C2 · 골격 · W) — 판독은 tools/ionic/li2s3_stage2_readout.py (카드 판독 허가 뒤).
#   · 해시 검사와 드라이버가 파일을 읽는 순간 사이 (초 단위) 는 시작 뒤 config.xyz = init 대조로만 메운다 · 패키지 판 변경은
#     시작 때 판 줄로만 남긴다 · 프로세스별 GPU 점유는 못 잰다 (합계 문턱 · 벽시계 비용 — GPU 대기가 섞이면 넉넉하게 센다).
#   · 첫 런 한도는 400 ps 당 first_run_max_h 로 센다 (800 ps 첫 런은 2 배) — 길이를 안 보면 cond550 첫 런이 늘 걸린다.
#   · 큐가 죽으면 (kill · 정전) 끝 기록 · 장부 행이 없다 — 드라이버는 잠금을 쥔 채 끝까지 돌 수 있고 (그동안 다시 띄우면 10),
#     그 뒤 시작은 비용 미확정 (15) 이다. 그 런의 시간 · 처리 (COST_CHARGE · 판정 보류 → PHASE=rerun) 는 사람이 정한다.
#   · 멈춤 · 풂 · 비용 정함은 기록만 남긴다 — 그 사람 결정이 옳은지는 보지 않는다 (판독 도구는 풀리지 않은 멈춤이 있으면 보류).
#
# --selftest — 임시 폴더에서 이 파일 → 실제 MD 드라이버 (fairchem 스텁 · 가짜 nvidia-smi · GPU 안 씀 · 저장소 파일은 안 바꾼다 —
#   드라이버 · 이 파일을 바꾸는 시험은 임시 루트 사본에서). FAKE_* 환경변수는 스텁만 읽는다 (실행 경로에는 없다).
# =============================================================================
set -u
SELF=$(realpath "$0")
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
command -v "$PY" >/dev/null 2>&1 || { echo "⛔ PY=$PY 를 못 찾는다 (numpy · ase 있는 python 절대경로)"; exit 2; }
exec "$PY" - "$SELF" "$@" <<'PYEOF'
import datetime as _dt
import fcntl
import hashlib
import json
import math
import os
import pathlib
import re
import shutil
import socket
import subprocess
import sys
import time
import uuid

SELF = pathlib.Path(sys.argv[1]).resolve()
ARGV = sys.argv[2:]
REPO = SELF.parents[3]
E = os.environ
PY = sys.executable
CARD_REPO = REPO / "db" / "properties" / "lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json"
DRV = REPO / "tools" / "modelc_v3" / "disorder_ensemble_diffusion.py"
START, END, PIDF = "exec_v2_start.json", "exec_v2_end.json", "exec_v2_pid.json"
LEDGER_HEADER = ["system", "T_K", "seed", "prod_ps", "start", "end", "hours", "rc"]
NEED = ("systems", "seeds", "temperatures_K", "prod_ps", "equilib_ps", "vseed_offset", "n_atoms", "save_fs", "dt_fs",
        "conditional", "cap_gpu_h", "first_run_max_h", "gpu_start_max_mib", "cost_estimate_h_per_ps", "queue_v2")
BASE = LOGF = STOPS = LEDGER = None
PHASE = ""
SELF_SHA = ""


def now_local():
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_utc():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def g(x):
    return f"{float(x):g}"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_json(p):
    try:
        return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def same(gv, w):
    if isinstance(w, bool):
        return gv is w
    if isinstance(w, (int, float)):
        return gv is not None and not isinstance(gv, bool) and isinstance(gv, (int, float)) and abs(float(gv) - float(w)) <= 1e-9
    if isinstance(w, list):
        return isinstance(gv, list) and len(gv) == len(w) and all(same(a, b) for a, b in zip(gv, w))
    return gv == w


def log(msg):
    line = f"[{now_local()}] {msg}"
    print(line, flush=True)
    if LOGF is not None:
        try:
            with open(LOGF, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except OSError:
            pass


def die(code, msg):
    log(msg)
    sys.exit(code)


def write_new(p, obj):
    p = pathlib.Path(p)
    with open(p, "x", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def append_line(p, line):
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
        fh.flush()
        os.fsync(fh.fileno())


# ───────────────────────── 카드 · 결정 ─────────────────────────
def card_values(path):
    try:
        c = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        die(6, f"⛔ 카드 {path} 를 못 읽었다 ({type(e).__name__})")
    mv = c.get("기계_판독_값") or {}
    s2 = mv.get("stage2") or {}
    miss = [f"stage2.{k}" for k in NEED if k not in s2] + [k for k in ("decision", "md_driver_sha16", "inputs_sha256") if k not in mv]
    cond, q2 = s2.get("conditional") or {}, s2.get("queue_v2") or {}
    if "conditional" in s2 and not all(k in cond for k in ("T_K", "prod_ps")):
        miss.append("stage2.conditional.{T_K · prod_ps}")
    if "queue_v2" in s2 and not all(q2.get(k) for k in ("sha16", "decision")):
        miss.append("stage2.queue_v2.{sha16 · decision}")
    if miss:
        die(6, f"⛔ 카드 기계 값이 모자란다 {miss} — v2 는 값을 따로 갖지 않는다 (카드가 이 v2 판을 고정해야 돈다)")
    cv = {"systems": [str(x) for x in s2["systems"]], "seeds": [int(x) for x in s2["seeds"]], "temps": [int(x) for x in s2["temperatures_K"]],
          "prod": float(s2["prod_ps"]), "equilib": float(s2["equilib_ps"]), "voff": int(s2["vseed_offset"]), "n_atoms": int(s2["n_atoms"]),
          "save": float(s2["save_fs"]), "dt": float(s2["dt_fs"]), "condT": int(cond["T_K"]), "condP": float(cond["prod_ps"]),
          "cap": float(s2["cap_gpu_h"]), "first_max": float(s2["first_run_max_h"]), "gpu_max": int(s2["gpu_start_max_mib"]),
          "rate": float(s2["cost_estimate_h_per_ps"]), "q2_sha16": str(q2["sha16"]), "q2_decision": str(q2["decision"]),
          "decision": str(mv["decision"]), "drv16": str(mv["md_driver_sha16"]), "inputs": dict(mv["inputs_sha256"])}
    if cv["condT"] in cv["temps"]:
        die(6, "⛔ 카드 conditional.T_K 가 사다리 온도와 겹친다 — 런의 길이를 정할 수 없다")
    return cv


def run_values(cv, T):
    """런을 정하는 카드 값 — 판독 도구가 지금 카드와 다시 맞추는 것 · '이미 끝났다' 판정도 이것만 본다 (상한 · 한도가 바뀌어도 끝난 런은 끝난 런)."""
    return {"T_K": int(T), "block": block_of(cv, T), "prod_ps": prod_of(cv, T), "equilib_ps": cv["equilib"], "vseed_offset": cv["voff"],
            "save_fs": cv["save"], "dt_fs": cv["dt"], "n_atoms": cv["n_atoms"]}


def card_public(cv, T):
    """실행 기록에 싣는 카드 값 (런을 정하는 값 + 그때의 상한 · 한도 · 견적 · 문턱)."""
    return {**run_values(cv, T), "cap_gpu_h": cv["cap"], "first_run_max_h": cv["first_max"], "gpu_start_max_mib": cv["gpu_max"],
            "cost_estimate_h_per_ps": cv["rate"]}


def parse_utc(s):
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return _dt.datetime.strptime(str(s), fmt)
        except (TypeError, ValueError):
            continue
    return None


def decision_state(path, did):
    d = load_json(path)
    L = d.get("decisions", []) if isinstance(d, dict) else (d or [])
    return next((e.get("decision_state") for e in L if isinstance(e, dict) and e.get("id") == did), None)


# ───────────────────────── 런 이름 · 명령 ─────────────────────────
def key(s, sd, T):
    return f"{s}{sd}_T{T}"


def rdir(s, sd, T):
    return BASE / s / f"seed{sd}" / f"T{T}"


def init_of(s, sd):
    return BASE / s / "init" / f"seed{sd}_final.xyz"


def prod_of(cv, T):
    return cv["condP"] if int(T) == cv["condT"] else cv["prod"]


def block_of(cv, T):
    return "cond550" if int(T) == cv["condT"] else "ladder"


def argv_for(cv, s, sd, T):
    """드라이버 명령 — v1 러너 (glass_kgy_q_v2.sh:243-245) 와 같은 틀 · 값은 카드에서 (--save_fs 만 더해 명시한다)."""
    return [PY, str(DRV), "--v0_xyz", str(init_of(s, sd)), "--supercell", "1", "1", "1", "--label", f"li2s3_{s}_s{sd}_T{T}",
            "--out_root", str(rdir(s, sd, T)), "--disorder_levels", "0", "--n_configs", "1", "--temperatures", str(int(T)),
            "--equilib_ps", g(cv["equilib"]), "--prod_ps", g(prod_of(cv, T)), "--timestep_fs", g(cv["dt"]), "--save_fs", g(cv["save"]),
            "--friction", "0.02", "--fit_window_ps", "2", "50", "--save_traj", "--seed", str(cv["voff"] + int(sd)), "--turbo",
            "--device", "cuda"]


# ───────────────────────── 멈춤 기록 ─────────────────────────
def read_jsonl(p):
    if not p.exists():
        return []
    out = []
    for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not ln.strip():
            continue
        try:
            out.append(json.loads(ln))
        except ValueError:
            die(14, f"⛔ {p.name} {i} 번째 줄이 깨졌다 — 멈춤 기록을 믿을 수 없다 (사람이 보고 고친다)")
    return out


def unacked():
    recs = read_jsonl(STOPS)
    acked = {r.get("id") for r in recs if r.get("type") == "ack"}
    return [r for r in recs if r.get("type") == "stop" and r.get("id") not in acked], acked


def stop(code, reason, run=None, dry=False):
    if dry:
        die(code, f"⛔ (DRY_RUN — 멈춤 기록 안 씀) {reason}")
    sid = uuid.uuid4().hex[:12]
    try:
        append_line(STOPS, json.dumps({"type": "stop", "id": sid, "utc": now_utc(), "local": now_local(), "phase": PHASE, "code": code,
                                       "reason": reason, "run": run, "queue_v2_sha16": SELF_SHA[:16]}, ensure_ascii=False))
    except OSError as e:
        log(f"⛔ 멈춤 기록을 못 썼다 ({type(e).__name__}: {e}) — 다음 시작은 실행 흔적으로 판단한다")
    die(code, f"⛔ 멈춤 {sid} (종료 {code}) — {reason} · 이어서 돌리려면 ACK_STOP={sid} ACK_BY=<누가> ACK_REASON=<왜> (사람 결정 · 기록된다)")


# ───────────────────────── 장부 · 흔적 · 비용 ─────────────────────────
def ledger_rows():
    if not LEDGER.exists():
        return None
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].split("\t") != LEDGER_HEADER:
        die(15, f"⛔ 장부 {LEDGER.name} 머리 줄이 v1 꼴 {LEDGER_HEADER} 이 아니다 — 비용 미확정 (시작하지 않는다)")
    rows = []
    for i, ln in enumerate(lines[1:], start=2):
        if not ln.strip():
            continue
        f = ln.split("\t")
        if len(f) != 8:
            die(15, f"⛔ 장부 {i} 번째 줄 칸 수 {len(f)} ≠ 8 — 비용 미확정 (0 으로 세지 않는다)")
        try:
            h = float(f[6])
        except ValueError:
            die(15, f"⛔ 장부 {i} 번째 줄 시간 {f[6]!r} 을 못 읽었다 — 비용 미확정")
        if not (math.isfinite(h) and h >= 0):
            die(15, f"⛔ 장부 {i} 번째 줄 시간 {h} — 비용 미확정")
        rows.append({"raw": ln, "system": f[0], "T": f[1], "seed": f[2], "prod": f[3], "start": f[4], "end": f[5], "hours": h, "rc": f[7]})
    return rows


def traces(cv):
    out = []
    for s in cv["systems"]:
        if not (BASE / s).is_dir():
            continue
        for sdd in sorted((BASE / s).iterdir()):
            m = re.fullmatch(r"seed(\d+)", sdd.name)
            if not m or not sdd.is_dir():
                continue
            for td in sorted(sdd.iterdir()):
                mt = re.fullmatch(r"T(\d+)(\.superseded_.+)?", td.name)
                if not mt or not td.is_dir():
                    continue
                out.append({"path": td, "rel": str(td.relative_to(BASE)), "system": s, "seed": int(m.group(1)), "T": int(mt.group(1)),
                            "superseded": bool(mt.group(2)), "kind": "v2" if (td / START).exists() else "v1"})
    return out


def cost_state(rows, tr):
    rows = rows or []
    used, und, charged = set(), [], {}
    for i, r in enumerate(rows):
        if r["rc"] == "charge" and r["start"].startswith("charge:"):
            charged[r["start"][len("charge:"):]] = r
            used.add(i)
    for t in tr:
        if t["kind"] != "v2":
            continue
        en = load_json(t["path"] / END)
        if en is None:
            if t["rel"] not in charged:
                und.append((t, "v2 실행 기록 끝이 없다 (끊긴 런)"))
            continue
        hit = [i for i, r in enumerate(rows) if i not in used and r["raw"] == en.get("ledger_row")]
        if hit:
            used.add(hit[0])
        elif t["rel"] not in charged:
            und.append((t, "v2 실행 기록은 끝났는데 장부 행이 없다"))
    for t in sorted((x for x in tr if x["kind"] == "v1"), key=lambda x: x["rel"]):
        if t["rel"] in charged:
            continue
        cand = [i for i, r in enumerate(rows) if i not in used and r["rc"] != "charge"
                and (r["system"], r["T"], r["seed"]) == (t["system"], str(t["T"]), str(t["seed"]))]
        if cand:
            used.add(cand[0])
        else:
            und.append((t, "v1 런 흔적에 장부 행이 없다"))
    return sum(r["hours"] for r in rows), und


def estimate(cv, rows, prod):
    rates = []
    for r in rows or []:
        try:
            p = float(r["prod"])
        except ValueError:
            continue
        if r["rc"] == "0" and p > 0:
            rates.append(r["hours"] / p)
    rate = max([cv["rate"]] + rates)
    return rate * float(prod), rate


def first_limit_h(cv, prod):
    return cv["first_max"] * float(prod) / cv["prod"]


# ───────────────────────── 결속 기록 (판독 · 보류) ─────────────────────────
def base_matches(d):
    if d.get("base_original") == str(BASE):
        return True
    try:
        return bool(d.get("base_now")) and pathlib.Path(d["base_now"]).resolve() == BASE.resolve()
    except OSError:
        return False


def linked_record(pvar, hvar):
    p, h = E.get(pvar, "").strip(), E.get(hvar, "").strip()
    if not p or not h:
        die(16, f"⛔ {pvar} 와 {hvar} 가 있어야 한다 (고정 기록 파일과 그 sha256)")
    f = pathlib.Path(p).expanduser()
    if not f.is_file():
        die(16, f"⛔ {pvar} {f} 가 없다")
    if sha256(f) != h:
        die(16, f"⛔ {pvar} sha256 ≠ {hvar} — 그 기록이 아니다")
    d = load_json(f)
    if not isinstance(d, dict):
        die(16, f"⛔ {pvar} 를 못 읽었다")
    return f.resolve(), h, d


def rel_to_base(f):
    try:
        return str(pathlib.Path(f).resolve().relative_to(BASE.resolve()))
    except ValueError:
        return None


def check_readout_link(cv):
    f, h, d = linked_record("READOUT_RECORD", "READOUT_SHA256")
    lo, probs = min(cv["temps"]), []
    if d.get("kind") != "li2s3_stage2_readout/v2" or d.get("status") != "판독":
        probs.append("kind · status 가 판독 기록 (li2s3_stage2_readout/v2 · 판독) 이 아니다")
    if d.get("phase", "ladder") != "ladder":
        probs.append(f"사다리 판독이 아니다 (phase {d.get('phase')!r})")
    if d.get("cond550_eligible") is not True:
        probs.append("cond550_eligible 이 True 가 아니다")
    for s in cv["systems"]:
        if (d.get("measurable") or {}).get(f"{s}_T{lo}") is not True:
            probs.append(f"{s} {lo} K 이 측정 가능이 아니다")
    if not base_matches(d):
        probs.append("다른 BASE 의 판독 기록이다")
    if probs:
        die(16, "⛔ cond550 결속 판독 기록이 조건을 못 채운다 — " + " · ".join(probs) + " (카드 cond550_Q6)")
    return {"kind": "readout", "path": str(f), "rel_to_base": rel_to_base(f), "sha256": h, "record_utc": (d.get("provenance") or {}).get("utc")}


def parse_rerun(cv):
    raw = E.get("RERUN", "").split()
    if not raw:
        die(13, "⛔ PHASE=rerun 은 RERUN='A:11:600 B:12:650' (계:시드:온도) 목록이 있어야 한다")
    items = []
    for it in raw:
        m = re.fullmatch(r"([A-Za-z]+):(\d+):(\d+)", it)
        if not m:
            die(13, f"⛔ RERUN 항목 꼴 {it!r} (계:시드:온도)")
        s, sd, T = m.group(1), int(m.group(2)), int(m.group(3))
        if s not in cv["systems"] or sd not in cv["seeds"] or (T not in cv["temps"] and T != cv["condT"]):
            die(13, f"⛔ RERUN 항목 {it} 가 카드 밖이다 (계 {cv['systems']} · 시드 {cv['seeds']} · 온도 {cv['temps']} + {cv['condT']})")
        items.append((s, sd, T))
    if len(set(items)) != len(items):
        die(13, "⛔ RERUN 에 같은 런이 두 번 있다")
    return sorted(items, key=lambda x: (x[2], x[1], cv["systems"].index(x[0])))


def check_hold_link(cv, items):
    f, h, d = linked_record("HOLD_RECORD", "HOLD_SHA256")
    probs = []
    if d.get("kind") != "li2s3_stage2_readout_hold/v2" or d.get("status") != "판정 보류":
        probs.append("kind · status 가 판정 보류 기록 (li2s3_stage2_readout_hold/v2) 이 아니다")
    if not base_matches(d):
        probs.append("다른 BASE 의 보류 기록이다")
    runs = d.get("runs") or {}
    for s, sd, T in items:
        st = (runs.get(key(s, sd, T)) or {}).get("status")
        if st not in ("invalid", "incomplete"):
            probs.append(f"{key(s, sd, T)}: 보류 기록의 상태 {st!r} (invalid · incomplete 만 다시 돈다)")
    if probs:
        die(16, "⛔ 재실행 결속 보류 기록이 조건을 못 채운다 — " + " · ".join(probs))
    return {"kind": "hold", "path": str(f), "rel_to_base": rel_to_base(f), "sha256": h, "record_utc": (d.get("provenance") or {}).get("utc")}


# ───────────────────────── 런 하나 — 검사 ─────────────────────────
def meta_problems(m, cv, s, sd, T, final):
    if not isinstance(m, dict):
        return ["run_meta.json 없음 · 못 읽음"]
    want = {"label": f"li2s3_{s}_s{sd}_T{T}", "n_atoms": cv["n_atoms"], "supercell": [1, 1, 1], "v0_xyz": str(init_of(s, sd)),
            "temperatures": [float(T)], "prod_ps": prod_of(cv, T), "equilib_ps": cv["equilib"], "seed": cv["voff"] + int(sd),
            "fit_window_ps": [2.0, 50.0], "save_traj": True, "uma_model": "uma-s-1p1", "uma_inference_mode_requested": "turbo"}
    bad = [f"run_meta {k} {m.get(k)!r} ≠ 카드 {w!r}" for k, w in want.items() if not same(m.get(k), w)]
    if "uma_inference_mode" in m or final:
        if m.get("uma_inference_mode") != "turbo":
            bad.append(f"run_meta 실제 추론 모드 {m.get('uma_inference_mode')!r} ≠ 'turbo'")
    return bad


def same_structure(a_path, b_path):
    import numpy as np
    from ase.io import read
    a, b = read(str(a_path)), read(str(b_path))
    if a.get_chemical_symbols() != b.get_chemical_symbols():
        return False, "원소 순서"
    ca, cb = np.asarray(a.get_cell()), np.asarray(b.get_cell())
    if float(np.abs(ca - cb).max()) > 1e-6:
        return False, "셀"
    d = b.get_positions() - a.get_positions()
    f = d @ np.linalg.inv(ca)
    f -= np.round(f)
    if float(np.linalg.norm(f @ ca, axis=1).max()) > 1e-6:
        return False, "좌표"
    return True, ""


def md_times(p, with_T=False):
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    heads = [i for i, ln in enumerate(lines) if ln.strip().startswith("Time[ps]")]
    if not heads:
        return (heads, [], []) if with_T else (heads, [])
    hdr = lines[heads[0]].split()
    it, iT = hdr.index("Time[ps]"), (hdr.index("T[K]") if "T[K]" in hdr else None)
    body = [ln.split() for ln in lines[1:] if ln.strip() and not ln.strip().startswith("Time[ps]")]
    ts = [float(r[it]) for r in body]
    if not with_T:
        return heads, ts
    return heads, ts, ([float(r[iT]) for r in body] if iT is not None else [])


def traj_frames(p, n_atoms):
    n = 0
    with open(p, encoding="utf-8", errors="replace") as fh:
        while True:
            hd = fh.readline()
            if not hd:
                return n
            try:
                k = int(hd.strip())
            except ValueError:
                return None
            if k != n_atoms or not fh.readline():
                return None
            for _ in range(k):
                if not fh.readline():
                    return None
            n += 1


def completion(rc, cv, s, sd, T, mon):
    rd = rdir(s, sd, T)
    tdir = rd / "d0.00_cfg0" / f"T{T}"
    prod = prod_of(cv, T)
    n_frames = int(round(prod * 1000.0 / cv["save"]))
    n_rows = int(round((cv["equilib"] + prod) / (cv["dt"] / 1000.0))) + 1
    R = list(mon)
    if rc != 0:
        R.append(f"드라이버 종료 코드 {rc} ≠ 0")
    R += meta_problems(load_json(rd / "run_meta.json"), cv, s, sd, T, final=True)
    er = load_json(rd / "ensemble_results.json")
    if not isinstance(er, dict):
        R.append("ensemble_results.json 없음 · 못 읽음")
    else:
        want = {"uma_inference_mode": "turbo", "uma_task": "omat", "uma_model": "uma-s-1p1", "n_atoms": cv["n_atoms"],
                "temperatures": [float(T)], "prod_ps": prod, "equilib_ps": cv["equilib"], "label": f"li2s3_{s}_s{sd}_T{T}"}
        R += [f"ensemble_results {k} {er.get(k)!r} ≠ {w!r}" for k, w in want.items() if not same(er.get(k), w)]
    cf = rd / "d0.00_cfg0" / "config.xyz"
    try:
        ok, why = same_structure(init_of(s, sd), cf) if cf.is_file() else (False, "없음")
    except Exception as e:
        ok, why = False, f"못 읽음 ({type(e).__name__})"
    if not ok:
        R.append(f"config.xyz ≠ init ({why})")
    ar = load_json(tdir / "aimd_results.json")
    if not isinstance(ar, dict):
        R.append("aimd_results.json 없음 · 못 읽음")
    else:
        for k, w in (("T_K", float(T)), ("save_fs", cv["save"]), ("prod_ps", prod), ("dt_fs", cv["dt"]), ("n_frames", n_frames)):
            if not same(ar.get(k), w):
                R.append(f"aimd_results {k} {ar.get(k)!r} ≠ {w!r}")
    nf = traj_frames(tdir / "traj.xyz", cv["n_atoms"]) if (tdir / "traj.xyz").is_file() else None
    if nf != n_frames:
        R.append(f"traj.xyz 프레임 {nf} ≠ 계획 {n_frames}")
    try:
        heads, ts, TT = md_times(tdir / "md.log", with_T=True)
        dtp = cv["dt"] / 1000.0
        if heads != [0] or len(ts) != n_rows or abs(ts[0]) > 1e-9 or any(abs((b - a) - dtp) > 1e-6 for a, b in zip(ts, ts[1:])) \
                or abs(ts[-1] - (cv["equilib"] + prod)) > 1e-6:
            R.append(f"md.log 머리 {heads[:2]} · 행 {len(ts)} (계획 {n_rows}) · 간격 · 끝 시각이 계획과 다르다")
        if len(TT) != len(ts) or not all(math.isfinite(x) for x in TT):
            R.append("md.log 온도가 유한하지 않다 (동역학이 깨졌다)")
    except (OSError, ValueError, IndexError) as e:
        R.append(f"md.log 를 못 읽었다 ({type(e).__name__})")
    d = load_json(tdir / "msd.json")
    try:
        arrs = [d["times_ps"], d["msd_Li_A2"], d["times_ps_mto"], d["msd_Li_A2_mto"]]
        vals = [float(x) for a in arrs for x in a]
        if not (same(d.get("T_K"), float(T)) and len(arrs[0]) == n_frames and len(arrs[1]) == n_frames and len(arrs[2]) >= 3
                and len(arrs[2]) == len(arrs[3]) and all(math.isfinite(v) for v in vals)):
            R.append("msd.json T · 길이 · 유한 (MTO 포함) 이 계획과 다르다")
    except (TypeError, KeyError, ValueError):
        R.append("msd.json 을 못 읽었거나 배열이 없다")
    return ("complete" if not R else "failed"), R


def kill(proc):
    proc.terminate()
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def monitor(proc, cv, s, sd, T, poll, meta_wait):
    """드라이버가 도는 동안 — run_meta (카드 값 · 실제 모드) · config.xyz = init · md.log dt 를 확인하고 어긋나면 세운다.
    → (문제 목록, 본 것, 실제로 세웠나) — 드라이버가 먼저 끝나 버린 뒤 찾은 문제는 '세웠다' 가 아니다 (끝 기록 killed 는 실제 정지만)."""
    rd = rdir(s, sd, T)
    tdir = rd / "d0.00_cfg0" / f"T{T}"
    seen = {"meta": False, "mode": False, "config": False, "dt": False}
    t0 = time.time()
    while True:
        alive = proc.poll() is None
        probs = []
        m = load_json(rd / "run_meta.json")
        if isinstance(m, dict) and not (seen["meta"] and seen["mode"]):
            bad = meta_problems(m, cv, s, sd, T, final=False)
            if bad:
                probs += bad
            else:
                seen["meta"] = True
                seen["mode"] = seen["mode"] or m.get("uma_inference_mode") == "turbo"
        cf = rd / "d0.00_cfg0" / "config.xyz"
        if not seen["config"] and cf.is_file():
            try:
                ok, why = same_structure(init_of(s, sd), cf)
                if ok:
                    seen["config"] = True
                elif not alive:
                    probs.append(f"config.xyz ≠ init ({why})")
                elif why in ("원소 순서", "셀", "좌표"):
                    probs.append(f"config.xyz ≠ init ({why}) — 드라이버가 다른 구조를 읽었다")
            except Exception:
                pass                                         # 쓰는 중 — 다음 표본에서
        if not seen["dt"] and (tdir / "md.log").is_file():
            try:
                _, ts = md_times(tdir / "md.log")
                if len(ts) >= 3:
                    if abs((ts[1] - ts[0]) - cv["dt"] / 1000.0) > 1e-6:
                        probs.append(f"md.log dt {ts[1] - ts[0]} ≠ 카드 {cv['dt'] / 1000.0}")
                    else:
                        seen["dt"] = True
            except (OSError, ValueError, IndexError):
                pass
        if probs and alive:
            kill(proc)
            return probs, seen, True
        if not alive:
            return probs, seen, False
        if not seen["meta"] and time.time() - t0 > meta_wait:
            kill(proc)
            return [f"run_meta.json 이 {meta_wait:g} s 안에 카드 값으로 안 생겼다"], seen, True
        time.sleep(poll)


def gpu_mib():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits", "-i", "0"],
                           capture_output=True, text=True, timeout=60)
        return int(r.stdout.strip().split()[0])
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        return None


def outputs_sha(s, sd, T):
    rd = rdir(s, sd, T)
    rels = ["run_meta.json", "ensemble_results.json", "d0.00_cfg0/config.xyz"] + [
        f"d0.00_cfg0/T{T}/{x}" for x in ("traj.xyz", "msd.json", "aimd_results.json", "md.log")]
    return {r: (sha256(rd / r) if (rd / r).is_file() else None) for r in rels}


def versions():
    try:
        r = subprocess.run([PY, "-c", "import ase, numpy; v = ['ase ' + ase.__version__, 'numpy ' + numpy.__version__]\n"
                                      "try:\n import torch; v.append('torch ' + torch.__version__)\nexcept Exception: v.append('torch ?')\n"
                                      "try:\n import fairchem.core as f; v.append('fairchem ' + getattr(f, '__version__', '?'))\n"
                                      "except Exception: v.append('fairchem ?')\nprint(' · '.join(v))"],
                           capture_output=True, text=True, timeout=180)
        return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "?"
    except (OSError, subprocess.SubprocessError):
        return "?"


# ───────────────────────── 본 실행 ─────────────────────────
def main():
    global BASE, LOGF, STOPS, LEDGER, PHASE, SELF_SHA
    if "--selftest" in ARGV:
        return selftest()
    PHASE = E.get("PHASE", "").strip()
    dry = E.get("DRY_RUN", "0") == "1"
    poll, gpu_wait, meta_wait = float(E.get("POLL", "60")), float(E.get("GPU_WAIT", "3600")), float(E.get("META_WAIT", "900"))
    BASE = pathlib.Path(E.get("BASE", "~/work/runs/li2s3_stage2_2026_11_10")).expanduser()
    SRC = pathlib.Path(E.get("SRC", "~/work/runs/li2s2_dense_1103")).expanduser()
    CARD = pathlib.Path(E.get("CARD", str(CARD_REPO))).expanduser()
    DEC = pathlib.Path(E.get("DECISIONS", str(REPO / "db" / "governance" / "decisions.json"))).expanduser()
    if PHASE not in ("cond550", "rerun"):
        die(13, f"⛔ PHASE={PHASE!r} — cond550 · rerun 만 안다 (사다리 16 런은 v1 큐 몫 · 시작하지 않는다)")
    if not BASE.is_dir():
        die(2, f"⛔ BASE {BASE} 가 없다")
    STOPS, LEDGER = BASE / "queue_v2_stops.jsonl", BASE / "cost_ledger.tsv"
    if not dry:
        LOGF = BASE / "stage2_kgy_v2.log"
    SELF_SHA = sha256(SELF)
    log(f"▶ li2s-3 2 단계 큐 v2 · PHASE {PHASE}{' · DRY_RUN' if dry else ''} · 큐 sha16 {SELF_SHA[:16]} · BASE {BASE} · 카드 {CARD}")
    # 카드 · 결정 · 코드 지문
    card_sha = sha256(CARD)
    cv = card_values(CARD)
    st = {cv["decision"]: decision_state(DEC, cv["decision"]), cv["q2_decision"]: decision_state(DEC, cv["q2_decision"])}
    if any(v != "active" for v in st.values()):
        die(6, f"⛔ 결정이 active 가 아니다 {st} — 시작하지 않는다 (v2 는 카드가 고정한 판 · 승인된 결정으로만 돈다)")
    if SELF_SHA[:16] != cv["q2_sha16"]:
        die(7, f"⛔ 이 큐 파일 sha16 {SELF_SHA[:16]} ≠ 카드 stage2.queue_v2.sha16 {cv['q2_sha16']} — 카드가 고정한 v2 판이 아니다")
    drv_sha = sha256(DRV) if DRV.is_file() else ""
    if drv_sha[:16] != cv["drv16"]:
        die(7, f"⛔ 드라이버 sha16 {drv_sha[:16] or '없음'} ≠ 카드 {cv['drv16']} ({DRV})")
    log(f"카드 sha256 {card_sha[:16]}… · 결정 {st} · 드라이버 sha16 {drv_sha[:16]} ✅ · 큐 sha16 = 카드 ✅")
    ignored = [k for k in ("TEMPS", "PROD", "SEEDS", "SYSTEMS", "VSEED_OFFSET", "CAP_H", "FIRST_RUN_MAX_H", "GPU_START_MAX", "DRV", "RUNNER")
               if k in E]
    if ignored:
        log(f"⚠ 환경변수 {ignored} 는 v2 가 읽지 않는다 — 과학 값 · 코드 경로는 카드 · 저장소에서만 (리뷰 DZ P1-4)")
    # 잠금 (v1 과 같은 파일) — 드라이버에 넘겨 드라이버가 도는 동안 쥐고 있게 한다
    lockfd = os.open(str(BASE / ".stage2.lock"), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        die(10, f"⛔ 잠금 {BASE / '.stage2.lock'} 을 다른 큐 (v1 run_stage2_kgy.sh · v2) 나 그 드라이버가 쥐고 있다 — 시작하지 않는다")
    if dry:
        fcntl.flock(lockfd, fcntl.LOCK_UN)
        log("잠금 비어 있음 (DRY_RUN — 쥐지 않고 놓았다)")
    # 멈춤 · 사람 결정
    ua, acked = unacked()
    ack_ids = [x for x in re.split(r"[,\s]+", E.get("ACK_STOP", "").strip()) if x]
    acks_now = []
    if ack_ids and not dry:
        by, why = E.get("ACK_BY", "").strip(), E.get("ACK_REASON", "").strip()
        if not by or not why:
            die(14, "⛔ ACK_STOP 에는 ACK_BY · ACK_REASON 이 같이 있어야 한다 (사람 결정 기록)")
        known = {s_["id"] for s_ in ua}
        bad = [i for i in ack_ids if i not in known]
        if bad:
            die(14, f"⛔ ACK_STOP {bad} 는 풀리지 않은 멈춤이 아니다 (풀리지 않은 멈춤: {sorted(known)})")
        for i in ack_ids:
            append_line(STOPS, json.dumps({"type": "ack", "id": i, "utc": now_utc(), "local": now_local(), "by": by, "reason": why,
                                           "queue_v2_sha16": SELF_SHA[:16]}, ensure_ascii=False))
            log(f"멈춤 {i} 풀림 — {by}: {why}")
        acks_now = ack_ids
        ua, acked = unacked()
    if ua:
        die(14, f"⛔ 풀리지 않은 멈춤 {len(ua)} 개 — " + " · ".join(f"{s_['id']} (종료 {s_['code']}: {s_['reason'][:90]})" for s_ in ua)
            + " · 다시 띄우는 것은 사람 결정의 대체물이 아니다 (ACK_STOP · ACK_BY · ACK_REASON)")
    # 계획 · 결속 기록
    if PHASE == "cond550":
        link = check_readout_link(cv)
        plan = [(s, sd, cv["condT"]) for sd in cv["seeds"] for s in cv["systems"]]
    else:
        plan = parse_rerun(cv)
        link = check_hold_link(cv, plan)
    log(f"결속 기록 {link['kind']} {link['path']} · sha256 {link['sha256'][:16]}… ✅")
    # 입력 (init 사본) — 카드 sha256 · 없으면 SRC 에서 (SRC 도 카드 sha256)
    for s, sd in sorted({(s, sd) for s, sd, _ in plan}):
        want, ini = cv["inputs"].get(f"{s}{sd}"), init_of(s, sd)
        if not want:
            die(8, f"⛔ {s}{sd} 의 입력 sha256 이 카드에 없다")
        if not ini.is_file():
            src = SRC / s / f"seed{sd}" / "final.xyz"
            if not src.is_file() or sha256(src) != want:
                die(8, f"⛔ {ini} 가 없고 SRC {src} 도 없거나 sha256 ≠ 카드 — 시작하지 않는다")
            if not dry:
                ini.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, ini)
        elif sha256(ini) != want:
            die(8, f"⛔ {ini} sha256 ≠ 카드 입력 기록 — 시작하지 않는다")
    # 흔적 · 비용 (장부를 이어 쓴다)
    rows = ledger_rows()
    tr = traces(cv)
    total, und = cost_state(rows, tr)
    charges = [x for x in re.split(r"[;\s]+", E.get("COST_CHARGE", "").strip()) if x]
    if charges and not dry and und:
        by, why = E.get("COST_BY", "").strip(), E.get("COST_REASON", "").strip()
        if not by or not why:
            die(15, "⛔ COST_CHARGE 에는 COST_BY · COST_REASON 이 같이 있어야 한다 (사람 결정 기록)")
        want_rel = {t["rel"]: t for t, _ in und}
        for c in charges:
            m = re.fullmatch(r"([^=]+)=([0-9.]+)", c)
            if not m or m.group(1) not in want_rel or not math.isfinite(float(m.group(2))):
                die(15, f"⛔ COST_CHARGE 항목 {c!r} — 비용 미확정 흔적 {sorted(want_rel)} 중 하나 = 시간 (h) 이어야 한다")
            t = want_rel[m.group(1)]
            if rows is None:
                append_line(LEDGER, "\t".join(LEDGER_HEADER))
                rows = []
            append_line(LEDGER, f"{t['system']}\t{t['T']}\t{t['seed']}\t{g(prod_of(cv, t['T']))}\tcharge:{t['rel']}\t{now_utc()}\t"
                                f"{float(m.group(2)):.4f}\tcharge")
            append_line(BASE / "cost_charges_v2.jsonl", json.dumps({"utc": now_utc(), "trace": t["rel"], "hours": float(m.group(2)),
                                                                     "by": by, "reason": why}, ensure_ascii=False))
            log(f"비용 미확정 흔적 {t['rel']} 에 {float(m.group(2)):g} h (사람 결정 · {by}: {why}) — 장부에 charge 행")
        rows = ledger_rows()
        total, und = cost_state(rows, tr)
    elif charges and not und:
        log("⚠ COST_CHARGE 를 쓰지 않았다 — 비용 미확정 흔적이 없다")
    if und:
        die(15, "⛔ 비용 미확정 흔적 — " + " · ".join(f"{t['rel']} ({why})" for t, why in und)
            + " — 0 으로 세지 않는다 · COST_CHARGE='<흔적>=<h>' COST_BY · COST_REASON 으로 사람이 정해 기록하기 전에는 시작하지 않는다")
    if rows is None and not dry:
        append_line(LEDGER, "\t".join(LEDGER_HEADER))
        rows = []
    log(f"장부 누적 {total:.4f} h / 상한 {cv['cap']:g} h · 흔적 {len(tr)} 개 모두 비용 확인")
    # 첫 런 한도 — 기록에서 다시 판정 (이 갈래의 첫 v2 런)
    def phase_first():
        cands = []
        for t in traces(cv):
            if t["kind"] == "v2":
                s0, e0 = load_json(t["path"] / START), load_json(t["path"] / END)
                if isinstance(s0, dict) and isinstance(e0, dict) and s0.get("phase") == PHASE:
                    cands.append((s0.get("start_utc", ""), s0, e0))
        return min(cands, key=lambda x: x[0]) if cands else None
    fr = phase_first()
    if fr:
        s0, e0 = fr[1], fr[2]
        lim = first_limit_h(cv, (s0.get("card_values") or {}).get("prod_ps", cv["prod"]))
        k0 = key(s0["system"], s0["seed"], s0["T_K"])
        if float(e0.get("wall_h_total", 0.0)) > lim:
            recs = read_jsonl(STOPS)
            ack_ok = any(r.get("type") == "stop" and r.get("code") == 21 and r.get("run") == k0 and r.get("id") in acked for r in recs)
            if not ack_ok:
                stop(21, f"이 갈래의 첫 런 {k0} 벽시계 {float(e0['wall_h_total']):.3f} h > 한도 {lim:g} h (기록에서 다시 판정)", k0, dry)
    # 이미 있는 폴더
    todo = []
    for s, sd, T in plan:
        rd = rdir(s, sd, T)
        if not rd.exists():
            todo.append((s, sd, T, None))
            continue
        s0, e0 = load_json(rd / START), load_json(rd / END)
        t_rec, t_run = parse_utc(link.get("record_utc")), parse_utc((s0 or {}).get("start_utc")) if isinstance(s0, dict) else None
        later = bool(t_rec and t_run and t_run > t_rec)
        done = (isinstance(s0, dict) and isinstance(e0, dict) and e0.get("status") == "complete" and e0.get("run_id") == s0.get("run_id")
                and s0.get("phase") == PHASE
                and {k: (s0.get("card_values") or {}).get(k) for k in run_values(cv, T)} == run_values(cv, T))
        if PHASE == "cond550":
            if done:
                log(f"건너뜀 — {key(s, sd, T)} 는 이 카드 값으로 이미 끝났다 (v2 실행 기록)")
                continue
            die(17, f"⛔ {rd} 가 있는데 완료된 v2 실행 기록이 아니다 — cond550 은 빈 폴더에서만 돈다 (판정 보류 기록 + PHASE=rerun 으로만 다시)")
        if later and done:
            log(f"건너뜀 — {key(s, sd, T)} 는 이 보류 기록 뒤에 이미 다시 돌아 끝났다")
            continue
        if later:
            die(17, f"⛔ {rd} 는 이 보류 기록 뒤에 시작한 런인데 끝나지 않았다 — 새 판독 보류 기록이 필요하다")
        todo.append((s, sd, T, rd))
    log("계획 — " + (" · ".join(f"{key(s, sd, T)}{' (옛 폴더 옮김)' if old else ''}" for s, sd, T, old in todo) or "없음 (다 끝났다)"))
    for s, sd, T, _ in todo:
        log("   " + " ".join(argv_for(cv, s, sd, T)[2:]))
    if dry:
        log("DRY_RUN 끝 — 아무것도 쓰지 않았다")
        return 0
    VERS = versions()
    log(f"판 — {VERS} · python {sys.version.split()[0]} · repo {(subprocess.run(['git', '-C', str(REPO), 'rev-parse', '--short=9', 'HEAD'], capture_output=True, text=True).stdout.strip() or '?')}")
    first_done = fr is not None
    for s, sd, T, old in todo:
        k = key(s, sd, T)
        prod = prod_of(cv, T)
        t0, s0l, s0u = time.time(), now_local(), now_utc()
        rows = ledger_rows() or []
        total, und = cost_state(rows, traces(cv))
        if und:
            stop(15, f"비용 미확정 흔적이 생겼다 {[t['rel'] for t, _ in und]}", k)
        est, rate = estimate(cv, rows, prod)
        if total + est > cv["cap"]:
            stop(22, f"누적 {total:.4f} h + {k} 어림 {est:.4f} h ({rate:.5f} h/ps × {g(prod)} ps) > 상한 {cv['cap']:g} h — "
                     f"멈춘 시점의 시드 · 온도로 판정하지 않는다 (사용자 결정)", k)
        w0 = time.time()
        while True:
            gm = gpu_mib()
            if gm is None:
                stop(12, "nvidia-smi 로 GPU 메모리를 못 잰다", k)
            if gm <= cv["gpu_max"]:
                break
            if time.time() - w0 >= gpu_wait:
                stop(12, f"GPU {gm} MiB > {cv['gpu_max']} 가 {gpu_wait:g} s 계속", k)
            log(f"대기 · GPU {gm} MiB > {cv['gpu_max']}")
            time.sleep(poll)
        waited = time.time() - w0
        # 실행 직전 — 다시 해시 (GPU 대기 뒤 · 리뷰 DZ P1-5): 카드 · 큐 파일 · 드라이버 (큐 시작 때 값) · 입력 (카드 값) — 한 경로로
        ini = init_of(s, sd)
        pins = (("카드", CARD, card_sha), ("큐 파일", SELF, SELF_SHA), ("드라이버", DRV, drv_sha),
                (f"입력 {ini.name}", ini, cv["inputs"].get(f"{s}{sd}")))
        now_sha = {lab: (sha256(p) if p.is_file() else None) for lab, p, _ in pins}
        probs = [f"{lab} sha256 ≠ 고정 값 (큐 시작 · 카드) — GPU 대기 중 바뀌었다" for lab, _, want in pins if now_sha[lab] != want]
        if probs:
            stop(8, f"{k} 실행 직전 다시 해시 — " + " · ".join(probs), k)
        in_sha = now_sha[f"입력 {ini.name}"]
        superseded = None
        if old is not None:
            dst = old.with_name(f"{old.name}.superseded_{_dt.datetime.now(_dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
            old.rename(dst)
            superseded = {"path": str(dst), "rel": str(dst.relative_to(BASE)), "had_v2_record": (dst / START).exists()}
            log(f"  옛 폴더를 옮겨 남김 → {dst.name}")
        rd = rdir(s, sd, T)
        rd.mkdir(parents=True, exist_ok=False)
        rid = uuid.uuid4().hex
        argv = argv_for(cv, s, sd, T)
        src = SRC / s / f"seed{sd}" / "final.xyz"
        start = {"kind": "li2s3_stage2_exec_start/v2", "run_id": rid, "phase": PHASE, "system": s, "seed": int(sd), "T_K": int(T),
                 "queue_v2_path": str(SELF), "queue_v2_sha256": SELF_SHA, "queue_v2_sha16": SELF_SHA[:16],
                 "driver_path": str(DRV), "driver_sha256": drv_sha, "driver_sha16": drv_sha[:16],
                 "card_path": str(CARD), "card_sha256": card_sha, "card_is_repo_card": CARD.resolve() == CARD_REPO.resolve(),
                 "card_values": card_public(cv, T), "decisions": st,
                 "input_path": str(ini), "input_sha256": in_sha, "src_path": str(src), "src_sha256": sha256(src) if src.is_file() else None,
                 "python": PY, "python_version": sys.version.split()[0], "versions": VERS, "host": socket.gethostname(), "base": str(BASE),
                 "argv": argv, "start_utc": s0u, "start_local": s0l, "launch_utc": now_utc(), "gpu_mib_at_launch": gm,
                 "gpu_wait_s": round(waited, 1), "superseded": superseded, "link": link, "acks_this_invocation": acks_now}
        try:
            write_new(rd / START, start)
        except OSError as e:
            stop(23, f"{k} 시작 기록을 못 썼다 ({type(e).__name__}: {e})", k)
        logd = BASE / s / "logs_v2"
        logd.mkdir(parents=True, exist_ok=True)
        lf = logd / f"s{sd}_T{T}_{rid[:8]}.log"
        log(f"▶ {k} · prod {g(prod)} ps · --seed {cv['voff'] + sd} · GPU {gm} MiB · 시작 기록 {rid[:8]} · 로그 {lf}")
        with open(lf, "w", encoding="utf-8") as fh:
            proc = subprocess.Popen(argv, stdout=fh, stderr=subprocess.STDOUT, pass_fds=(lockfd,))
        try:
            write_new(rd / PIDF, {"run_id": rid, "pid": proc.pid, "utc": now_utc()})
        except OSError:
            pass
        mon, seen, killed = monitor(proc, cv, s, sd, T, poll=min(poll, 5.0), meta_wait=meta_wait)
        rc = proc.wait()
        status, reasons = completion(rc, cv, s, sd, T, mon)
        e0l, h = now_local(), (time.time() - t0) / 3600.0
        row = f"{s}\t{T}\t{sd}\t{g(prod)}\t{s0l}\t{e0l}\t{h:.4f}\t{rc}"
        end = {"kind": "li2s3_stage2_exec_end/v2", "run_id": rid, "end_utc": now_utc(), "end_local": e0l, "driver_rc": rc, "pid": proc.pid,
               "wall_h_total": round(h, 6), "wall_h_driver": round((time.time() - t0 - waited) / 3600.0, 6), "gpu_h": round(h, 6),
               "status": status, "reasons": reasons, "monitor_seen": seen, "killed": killed,
               "outputs_sha256": outputs_sha(s, sd, T), "ledger_row": row}
        try:
            write_new(rd / END, end)
            append_line(LEDGER, row)
        except OSError as e:
            stop(23, f"{k} 끝 기록 · 장부를 못 썼다 ({type(e).__name__}: {e})", k)
        log(f"{'✅' if status == 'complete' else '⛔'} {k} 끝 · 드라이버 종료 {rc} · {h:.4f} h · {status}"
            + (f" — {'; '.join(reasons)[:200]}" if reasons else ""))
        if status != "complete":
            stop(9 if mon else 4, f"{k} {'실행 설정이 카드와 달라 세웠다' if mon else '런 실패'} — {'; '.join(reasons)[:300]}", k)
        if not first_done:
            first_done = True
            lim = first_limit_h(cv, prod)
            if h > lim:
                stop(21, f"이 갈래의 첫 런 {k} 벽시계 {h:.3f} h > 한도 {lim:g} h ({cv['first_max']:g} h / {g(cv['prod'])} ps × {g(prod)} ps) "
                         "— 멈추고 보고한다 (카드 멈춤 규칙)", k)
    log(f"■ v2 큐 끝 · PHASE {PHASE} · 누적 {sum(r['hours'] for r in (ledger_rows() or [])):.4f} h")
    return 0


# ───────────────────────── selftest ─────────────────────────
STUB_PM = '''import atexit, json, os
if os.environ.get("FAKE_EXIT_RC"):                 # 산출물을 다 쓴 뒤 종료 코드만 0 이 아니게 (끝에서 죽는 드라이버 흉내)
    atexit.register(lambda: os._exit(int(os.environ["FAKE_EXIT_RC"])))
def _corrupt():                                    # 드라이버가 다 쓰고 종료 코드 0 으로 끝난 뒤 산출물 하나를 깬다
    k, d = os.environ["FAKE_CORRUPT"], os.environ["FAKE_CORRUPT_DIR"]
    t = [x for x in os.listdir(os.path.join(d, "d0.00_cfg0")) if x.startswith("T")][0]
    td = os.path.join(d, "d0.00_cfg0", t)
    def rw(p, fn):
        p = os.path.join(td, p); s = open(p).read(); open(p, "w").write(fn(s))
    if k == "msd": rw("msd.json", lambda s: "{broken")
    if k == "traj": rw("traj.xyz", lambda s: "".join(s.splitlines(True)[:-122]))
    if k == "aimd": rw("aimd_results.json", lambda s: json.dumps(dict(json.loads(s), n_frames=json.loads(s)["n_frames"] + 1)))
    if k == "mdlog": rw("md.log", lambda s: "".join(s.splitlines(True)[:-1]))
    if k == "mdhead": rw("md.log", lambda s: s + "Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]\\n")
    if k == "ens":
        p = os.path.join(d, "ensemble_results.json"); e = json.load(open(p)); e.pop("uma_task", None); json.dump(e, open(p, "w"))
if os.environ.get("FAKE_CORRUPT"):
    atexit.register(_corrupt)
def get_predict_unit(name, device="cuda", inference_settings=None):
    if inference_settings == "turbo" and os.environ.get("FAKE_NO_TURBO"):
        raise RuntimeError("stub: turbo unavailable")
    return {"name": name, "settings": inference_settings}
'''
STUB_CALC = '''import os
import numpy as np
from ase.calculators.calculator import Calculator, all_changes
class FAIRChemCalculator(Calculator):
    implemented_properties = ["energy", "forces", "stress"]
    def __init__(self, pu, task_name="omat", k=50.0):
        super().__init__(); self.k, self.ref, self.n = k, None, 0
    def calculate(self, atoms=None, properties=("energy",), system_changes=all_changes):
        super().calculate(atoms, properties, system_changes)
        self.n += 1
        sym = np.asarray(atoms.get_chemical_symbols()); pos = atoms.get_positions(); cell = np.asarray(atoms.get_cell())
        if self.ref is None:
            self.ref = pos.copy()
        d = pos - self.ref; f = d @ np.linalg.inv(cell); f -= np.round(f); d = f @ cell; d[sym == "Li"] = 0.0
        F = -self.k * d
        if os.environ.get("FAKE_NAN_AFTER") and self.n > int(os.environ["FAKE_NAN_AFTER"]):
            F[sym != "Li"] = float("nan")          # 골격만 NaN — Li MSD 는 유한해 드라이버는 종료 코드 0 으로 끝난다
        if os.environ.get("FAKE_TOUCH_INIT") and self.n == int(os.environ.get("FAKE_TOUCH_AFTER", "1400")):
            from ase.io import read, write         # 런 도중 init 사본을 바꾼다 (감시가 config = init 을 이미 본 뒤)
            a = read(os.environ["FAKE_TOUCH_INIT"]); p = a.get_positions(); p[0, 0] += 0.5; a.set_positions(p)
            write(os.environ["FAKE_TOUCH_INIT"], a, format="extxyz")
        self.results.update(energy=float(0.5 * self.k * (d ** 2).sum()), forces=F, stress=np.zeros(6))
'''


def selftest():
    global BASE
    import tempfile
    sys.path.insert(0, str(REPO / "tools" / "ionic"))
    import melt_quench_uma as mq
    from ase import Atoms
    from ase.io import write
    n_ok, fails = 0, []
    t_all = time.time()

    def chk(c, msg):
        nonlocal n_ok
        if c:
            n_ok += 1
            print(f"  ✔ {msg}", flush=True)
        else:
            fails.append(msg)
            print(f"  ✘ {msg}", flush=True)

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        (td / "stub" / "fairchem" / "core" / "calculate").mkdir(parents=True)
        for rel, txt in (("fairchem/__init__.py", ""), ("fairchem/core/__init__.py", '__version__ = "stub-0"\n'),
                         ("fairchem/core/calculate/__init__.py", ""), ("fairchem/core/pretrained_mlip.py", STUB_PM),
                         ("fairchem/core/calculate/ase_calculator.py", STUB_CALC)):
            (td / "stub" / rel).write_text(txt)
        (td / "bin").mkdir()
        (td / "gpu").write_text("3000\n")
        (td / "bin" / "nvidia-smi").write_text(f'#!/bin/bash\ncat "{td / "gpu"}"\n')
        (td / "bin" / "nvidia-smi").chmod(0o755)
        sha_in = {}
        for s_, nfu in (("A", 12), ("B", 15)):
            for sd in (11, 12):
                sym, pos, cell = mq.build_random_cell(s_, sd, density_g_cm3=1.2, n_fu=nfu)
                f = td / "src" / s_ / f"seed{sd}" / "final.xyz"
                f.parent.mkdir(parents=True, exist_ok=True)
                write(str(f), Atoms(list(sym), positions=pos, cell=cell, pbc=True), format="extxyz")
                sha_in[f"{s_}{sd}"] = sha256(f)
        dec = td / "dec.json"
        D_CARD, D_Q2 = "D-TEST-card", "D-TEST-queue-v2"
        dec.write_text(json.dumps({"decisions": [{"id": D_CARD, "decision_state": "active"}, {"id": D_Q2, "decision_state": "active"},
                                                 {"id": "D-TEST-proposed", "decision_state": "proposed"}]}))
        me16 = sha256(SELF)[:16]

        def card(name, **over):
            s2 = {"systems": ["A", "B"], "seeds": [11, 12], "temperatures_K": [600, 650], "prod_ps": 2.5, "equilib_ps": 0.2,
                  "vseed_offset": 3000, "n_atoms": 120, "save_fs": 100.0, "dt_fs": 2.0, "conditional": {"T_K": 550, "prod_ps": 3.0},
                  "cap_gpu_h": 160, "first_run_max_h": 8, "gpu_start_max_mib": 6000, "cost_estimate_h_per_ps": 0.0001,
                  "queue_v2": {"sha16": me16, "decision": D_Q2}}
            s2.update({k: v for k, v in over.items() if k in s2 or k in NEED})
            mvd = {"decision": over.get("decision", D_CARD), "stage2": s2, "md_driver_sha16": over.get("drv16", sha256(DRV)[:16]),
                   "inputs_sha256": sha_in}
            p = td / name
            p.write_text(json.dumps({"기계_판독_값": mvd}, ensure_ascii=False))
            return p
        CARD0 = card("card0.json")
        n_base = [0]

        def mkbase(rows=None, v1=(), ledger=True):
            n_base[0] += 1
            b = td / f"base{n_base[0]}"
            for s_ in ("A", "B"):
                for sd in (11, 12):
                    (b / s_ / "init").mkdir(parents=True, exist_ok=True)
                    shutil.copy2(td / "src" / s_ / f"seed{sd}" / "final.xyz", b / s_ / "init" / f"seed{sd}_final.xyz")
            if ledger:
                (b / "cost_ledger.tsv").write_text("\t".join(LEDGER_HEADER) + "\n" + "".join("\t".join(map(str, r)) + "\n" for r in (rows or [])))
            for rel in v1:
                (b / rel).mkdir(parents=True)
                (b / rel / "run_meta.json").write_text("{}")
            return b

        def readout_rec(b, **over):
            d = {"kind": "li2s3_stage2_readout/v2", "status": "판독", "phase": "ladder", "cond550_eligible": True,
                 "measurable": {"A_T600": True, "B_T600": True, "A_T650": False, "B_T650": True}, "base_original": str(b),
                 "base_now": str(b.resolve()), "provenance": {"utc": "2026-11-14T00:00:00Z"}}
            d.update(over)
            p = b / "readout_stage2" / f"readout_{uuid.uuid4().hex[:6]}.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(d, ensure_ascii=False))
            return p

        def hold_rec(b, runs, **over):
            d = {"kind": "li2s3_stage2_readout_hold/v2", "status": "판정 보류", "runs": runs, "base_original": str(b),
                 "base_now": str(b.resolve()), "provenance": {"utc": now_utc()}}
            d.update(over)
            p = b / "readout_stage2" / f"hold_{uuid.uuid4().hex[:6]}.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(d, ensure_ascii=False))
            return p

        def run(b, phase, card_p=CARD0, wait=True, script=None, **env):
            e = {"HOME": E.get("HOME", str(td)), "PATH": f"{td / 'bin'}:{E.get('PATH', '/usr/bin:/bin')}", "PYTHONPATH": str(td / "stub"),
                 "PYTHONIOENCODING": "utf-8", "PY": PY, "BASE": str(b), "SRC": str(td / "src"), "CARD": str(card_p),
                 "DECISIONS": str(dec), "PHASE": phase, "POLL": "0.2", "GPU_WAIT": "20", "META_WAIT": "60"}
            e.update({k: str(v) for k, v in env.items()})
            p = subprocess.Popen(["bash", str(script or SELF)], env=e, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if not wait:
                return p
            out, _ = p.communicate(timeout=900)
            return p.returncode, out

        def link_env(p):
            return {"READOUT_RECORD": str(p), "READOUT_SHA256": sha256(p)}

        def hold_env(p, items):
            return {"HOLD_RECORD": str(p), "HOLD_SHA256": sha256(p), "RERUN": items}

        def stops_of(b):
            p = b / "queue_v2_stops.jsonl"
            return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []

        def ledger_n(b):
            return len([x for x in (b / "cost_ledger.tsv").read_text().splitlines()[1:] if x.strip()])
        cond_runs = ["A/seed11/T550", "B/seed11/T550", "A/seed12/T550", "B/seed12/T550"]
        # ── 양성: cond550 (고정 판독 기록 결속) ──
        b1 = mkbase(rows=[("A", 600, 11, 2.5, "2026-11-11 00:00:00", "2026-11-11 05:00:00", "5.1000", "0")], v1=("A/seed11/T600",))
        rc, out = run(b1, "cond550", **link_env(readout_rec(b1)))
        BASE = b1                                                   # argv_for 를 이 BASE 로 다시 만들어 맞춘다
        recs = [(load_json(b1 / r / START), load_json(b1 / r / END)) for r in cond_runs]
        okrec = all(isinstance(a, dict) and isinstance(z, dict) and z["status"] == "complete" and z["driver_rc"] == 0
                    and a["run_id"] == z["run_id"] and a["queue_v2_sha16"] == me16 and a["driver_sha16"] == sha256(DRV)[:16]
                    and a["card_sha256"] == sha256(CARD0) and a["input_sha256"] == sha_in[f"{a['system']}{a['seed']}"]
                    and a["argv"][2:] == argv_for(card_values(CARD0), a["system"], a["seed"], 550)[2:] and a["link"]["kind"] == "readout"
                    for a, z in recs) if rc == 0 else False
        outs_ok = rc == 0 and all(z["outputs_sha256"][k] == sha256(b1 / r / k) for (a, z), r in zip(recs, cond_runs) for k in z["outputs_sha256"])
        led = (b1 / "cost_ledger.tsv").read_text().splitlines()
        chk(rc == 0 and okrec and outs_ok and len(led) == 1 + 1 + 4 and all(z["ledger_row"] in led for _, z in recs),
            f"[양성] PHASE=cond550 (판독 기록 결속) — 4 런 · 실행 기록 (큐 · 드라이버 sha16 · 카드 sha256 · 입력 sha256 · 명령 인수 = 카드 · "
            f"종료 코드 0 · 산출물 sha256) · v1 장부를 이어 써 4 행 (종료 {rc})")
        a0 = recs[0][0] if recs[0][0] else {}
        chk(a0.get("argv", [])[2:][a0.get("argv", [])[2:].index("--prod_ps") + 1] == "3" if a0 else False,
            "[양성] cond550 런의 길이는 카드 conditional.prod_ps (3 ps — 사다리 2.5 ps 가 아니다)")
        rc2, out2 = run(b1, "cond550", **link_env(readout_rec(b1)))
        chk(rc2 == 0 and out2.count("건너뜀") == 4 and ledger_n(b1) == 5, f"[양성] 다시 띄우면 끝난 4 런은 건너뛴다 (장부 그대로) — 종료 {rc2}")
        h1 = float((load_json(b1 / cond_runs[0] / END) or {}).get("wall_h_total") or 1e-4)   # 이 기계에서 3 ps 런 한 번의 벽시계
        # ── 음성: 잠금 (v1 이 쥐고 있다) ──
        b2 = mkbase()
        holder = subprocess.Popen(["bash", "-c", f'exec 8>"{b2}/.stage2.lock"; flock -n 8 && sleep 8'])
        time.sleep(0.8)
        rc, out = run(b2, "cond550", **link_env(readout_rec(b2)))
        holder.wait()
        chk(rc == 10 and not any((b2 / r).exists() for r in cond_runs) and not stops_of(b2),
            f"⛔음성: v1 이 잠금을 쥐고 있으면 시작하지 않는다 (종료 {rc} · 런 폴더 0 · 멈춤 기록 없음)")
        # ── 음성: cond550 결속 기록 ──
        b3 = mkbase()
        chk(run(b3, "cond550")[0] == 16, "⛔음성: cond550 에 READOUT_RECORD 가 없으면 시작하지 않는다")
        rr = readout_rec(b3)
        chk(run(b3, "cond550", READOUT_RECORD=rr, READOUT_SHA256="0" * 64)[0] == 16, "⛔음성: READOUT_SHA256 ≠ 파일 → 거부")
        chk(run(b3, "cond550", **link_env(readout_rec(b3, measurable={"A_T600": True, "B_T600": False})))[0] == 16,
            "⛔음성: 판독 기록이 B 600 K 측정 불가 → cond550 거부")
        chk(run(b3, "cond550", **link_env(readout_rec(b3, cond550_eligible=False)))[0] == 16, "⛔음성: cond550_eligible False → 거부")
        chk(run(b3, "cond550", **link_env(readout_rec(b3, status="판정 보류", kind="li2s3_stage2_readout_hold/v2")))[0] == 16,
            "⛔음성: 보류 기록을 cond550 결속으로 주면 거부")
        chk(run(b3, "cond550", **link_env(readout_rec(b3, base_original="/elsewhere", base_now="/elsewhere")))[0] == 16,
            "⛔음성: 다른 BASE 의 판독 기록 → 거부")
        chk(not any((b3 / r).exists() for r in cond_runs), "⛔음성: 결속이 안 서면 런 폴더를 만들지 않는다")
        # ── 양성 · 음성: rerun (보류 기록 결속) ──
        b4 = mkbase(rows=[("A", 600, 11, 2.5, "2026-11-11 00:00:00", "2026-11-11 05:00:00", "5.1000", "0")], v1=("A/seed11/T600",))
        (b4 / "A/seed11/T600/msd.json").write_text("{broken")
        hr = hold_rec(b4, {"A11_T600": {"status": "invalid", "reasons": ["드라이버 종료 코드 7"]}, "B11_T600": {"status": "valid"}})
        chk(run(b4, "rerun", **hold_env(hr, "B:11:600"))[0] == 16, "⛔음성: 보류 기록에 valid 로 적힌 런은 다시 안 돈다")
        chk(run(b4, "rerun", **hold_env(hr, "A:12:600"))[0] == 16, "⛔음성: 보류 기록에 없는 런은 다시 안 돈다")
        chk(run(b4, "rerun", HOLD_RECORD=hr, HOLD_SHA256="1" * 64, RERUN="A:11:600")[0] == 16, "⛔음성: HOLD_SHA256 ≠ 파일 → 거부")
        chk(run(b4, "rerun", RERUN="A:11:600")[0] == 16, "⛔음성: 보류 기록 없이 rerun → 거부")
        chk(run(b4, "rerun", **hold_env(hr, "A:11:999"))[0] == 13 and run(b4, "rerun", **hold_env(hr, "A-11-600"))[0] == 13,
            "⛔음성: RERUN 항목이 카드 밖 · 꼴이 틀리면 거부")
        rc, out = run(b4, "rerun", **hold_env(hr, "A:11:600"))
        sup = sorted((b4 / "A" / "seed11").glob("T600.superseded_*"))
        a4, z4 = load_json(b4 / "A/seed11/T600" / START), load_json(b4 / "A/seed11/T600" / END)
        chk(rc == 0 and len(sup) == 1 and (sup[0] / "msd.json").read_text() == "{broken" and isinstance(z4, dict) and z4["status"] == "complete"
            and a4["link"]["kind"] == "hold" and a4["superseded"]["rel"] == str(sup[0].relative_to(b4)) and ledger_n(b4) == 2,
            f"[양성] PHASE=rerun — 보류 기록의 invalid 런만 · 옛 폴더는 지우지 않고 옮겨 남김 · 같은 카드 값 · 장부 한 행 더 (종료 {rc})")
        # ── 음성: 실행 기록 없는 폴더는 건너뛰지 않는다 (리뷰 DZ P1-1) ──
        b5 = mkbase()
        (b5 / "A/seed11/T550/d0.00_cfg0/T550").mkdir(parents=True)
        (b5 / "A/seed11/T550/d0.00_cfg0/T550/msd.json").write_text("{broken")
        (b5 / "cost_ledger.tsv").write_text("\t".join(LEDGER_HEADER) + "\nA\t550\t11\t3\tx\ty\t0.0010\t0\n")
        rc, out = run(b5, "cond550", **link_env(readout_rec(b5)))
        chk(rc == 17 and not (b5 / "B/seed11/T550").exists(),
            f"⛔음성: 깨진 msd.json 만 있는 폴더 (실행 기록 없음) 를 끝난 것으로 건너뛰지 않는다 (종료 {rc})")
        # ── 음성: 비용 (리뷰 DZ P1-3) ──
        b6 = mkbase(v1=("A/seed11/T600",), ledger=False)
        chk(run(b6, "cond550", **link_env(readout_rec(b6)))[0] == 15, "⛔음성: 흔적이 있는데 장부가 없으면 비용 미확정 — 시작하지 않는다 (0 아님)")
        b7 = mkbase(v1=("A/seed11/T600", "B/seed11/T600"), rows=[("A", 600, 11, 2.5, "x", "y", "5.0", "0")])
        rc, out = run(b7, "cond550", **link_env(readout_rec(b7)))
        chk(rc == 15 and "B/seed11/T600" in out, "⛔음성: 장부 행이 없는 흔적 (B11 600) → 비용 미확정 · 그 흔적을 이름으로 알린다")
        b8 = mkbase(v1=("A/seed11/T600",))
        (b8 / "cost_ledger.tsv").write_text("\t".join(LEDGER_HEADER) + "\nA\t600\t11\t2.5\tx\ty\tNaN\t0\n")
        chk(run(b8, "cond550", **link_env(readout_rec(b8)))[0] == 15, "⛔음성: 장부 시간이 NaN → 비용 미확정")
        rc, out = run(b7, "cond550", COST_CHARGE="B/seed11/T600=4.5", **link_env(readout_rec(b7)))
        chk(rc == 15, "⛔음성: COST_CHARGE 에 COST_BY · COST_REASON 이 없으면 거부")
        rc, out = run(b7, "cond550", COST_CHARGE="B/seed11/T600=4.5", COST_BY="selftest", COST_REASON="정전 런 · 사람이 정함",
                      **link_env(readout_rec(b7)))
        chk(rc == 0 and "charge:B/seed11/T600" in (b7 / "cost_ledger.tsv").read_text(),
            f"[양성] 사람이 정한 비용 (COST_CHARGE · 장부 charge 행 · 근거 기록) 뒤에는 시작한다 (종료 {rc})")
        rows157 = [("A", 600, 11, 2.5, f"r{i}", "e", "11.0714", "0") for i in range(14)] + [("A", 650, 11, 2.5, "last", "e", "2.0000", "0")]
        b9 = mkbase(rows=rows157)
        rc, out = run(b9, "cond550", **link_env(readout_rec(b9)))
        st9 = stops_of(b9)
        chk(rc == 22 and len(st9) == 1 and st9[0]["code"] == 22 and not any((b9 / r).exists() for r in cond_runs),
            "⛔음성: 누적 157 h · 직전 2 h — 다음 런 어림 = 장부의 최대 h/ps × 3 ps (직전 시간이 아니다) → 상한 160 h 를 넘어 첫 런 전에 멈춘다 "
            f"(종료 {rc})")
        chk(run(b9, "cond550", **link_env(readout_rec(b9)))[0] == 14, "⛔음성: 멈춘 뒤 그대로 다시 띄우면 거부 (풀리지 않은 멈춤)")
        chk(run(b9, "cond550", ACK_STOP=st9[0]["id"], **link_env(readout_rec(b9)))[0] == 14, "⛔음성: ACK_STOP 에 ACK_BY · ACK_REASON 이 없으면 거부")
        chk(run(b9, "cond550", ACK_STOP="deadbeef0000", ACK_BY="x", ACK_REASON="y", **link_env(readout_rec(b9)))[0] == 14,
            "⛔음성: 없는 멈춤 id 를 풀 수 없다")
        rc, out = run(b9, "cond550", ACK_STOP=st9[0]["id"], ACK_BY="selftest", ACK_REASON="상한 확인", **link_env(readout_rec(b9)))
        chk(rc == 22 and len(stops_of(b9)) == 3, f"⛔음성: 풀어도 상한은 카드 값이라 다시 멈춘다 (새 멈춤 기록 · 종료 {rc})")
        # ── 음성: 첫 런 한도 · 다시 띄우기 (리뷰 DZ P1-2) ──
        cF = card("cardF.json", first_run_max_h=1e-7)
        b10 = mkbase()
        rc, out = run(b10, "cond550", card_p=cF, **link_env(readout_rec(b10)))
        s10 = stops_of(b10)
        chk(rc == 21 and len(s10) == 1 and (b10 / cond_runs[0] / END).exists() and not (b10 / cond_runs[1]).exists(),
            f"⛔음성: 첫 런 벽시계 > 한도 → 첫 런 뒤 멈춘다 (둘째 런 안 띄움 · 종료 {rc})")
        chk(run(b10, "cond550", card_p=cF, **link_env(readout_rec(b10)))[0] == 14,
            "⛔음성: 첫 런 한도로 멈춘 큐를 다시 띄우면 나머지를 돌지 않는다 (리뷰 DZ P1-2 반례)")
        b10b = td / "base10b"
        shutil.copytree(b10, b10b)
        (b10b / "queue_v2_stops.jsonl").unlink()
        for f_ in b10b.rglob(START):
            d_ = load_json(f_)
            d_["base"] = str(b10b)
            f_.write_text(json.dumps(d_, ensure_ascii=False))
        rc, out = run(b10b, "cond550", card_p=cF, **link_env(readout_rec(b10b)))
        chk(rc == 21 and len(stops_of(b10b)) == 1, f"⛔음성: 멈춤 기록 없이 죽었어도 첫 런 기록에서 한도 초과를 다시 판정해 멈춘다 (종료 {rc})")
        rc, out = run(b10, "cond550", card_p=cF, ACK_STOP=s10[0]["id"], ACK_BY="selftest", ACK_REASON="느린 기계 확인 · 계속",
                      **link_env(readout_rec(b10)))
        chk(rc == 0 and all((b10 / r / END).exists() for r in cond_runs),
            f"[양성] 사람이 멈춤을 풀면 (ACK) 남은 런을 돈다 · 첫 런 한도는 갈래의 첫 런만 (종료 {rc})")
        # ── 음성: 두 런 사이에 입력이 바뀐다 (GPU 대기 중 · 리뷰 DZ P1-5) ──
        b11 = mkbase()
        p = run(b11, "cond550", wait=False, **link_env(readout_rec(b11)))
        t_ = time.time()
        while not (b11 / cond_runs[0] / START).exists() and time.time() - t_ < 120:
            time.sleep(0.05)
        (td / "gpu").write_text("9000\n")                             # 첫 런이 도는 동안 GPU 를 바쁘게 — 둘째 런은 GPU 를 기다린다
        while not (b11 / cond_runs[0] / END).exists() and time.time() - t_ < 300:
            time.sleep(0.05)
        time.sleep(0.5)
        ini = b11 / "B" / "init" / "seed11_final.xyz"
        ini.write_text(ini.read_text().replace("Li ", "Li  ", 1))   # 둘째 런 (B11) 입력을 바꾼다
        (td / "gpu").write_text("3000\n")
        out, _ = p.communicate(timeout=600)
        s11 = stops_of(b11)
        chk(p.returncode == 8 and (b11 / cond_runs[0] / END).exists() and not (b11 / cond_runs[1]).exists() and len(s11) == 1
            and s11[0]["code"] == 8 and "입력" in s11[0]["reason"],
            f"⛔음성: GPU 대기 중 둘째 런 입력이 바뀌면 실행 직전 다시 해시에서 둘째 런 전에 멈춘다 (종료 {p.returncode})")
        # ── 음성: 런 실패 · 깨진 산출물 (리뷰 DZ P1-1) ──
        cX = card("cardX.json", conditional={"T_K": 550, "prod_ps": 2.0})
        b12 = mkbase()
        rc, out = run(b12, "cond550", card_p=cX, **link_env(readout_rec(b12)))
        z12 = load_json(b12 / cond_runs[0] / END) or {}
        lr = (b12 / "cost_ledger.tsv").read_text().splitlines()
        chk(rc == 4 and z12.get("status") == "failed" and z12.get("driver_rc") == 1 and lr[-1].endswith("\t1")
            and not (b12 / cond_runs[1]).exists(),
            f"⛔음성: 드라이버가 msd.json 을 쓴 뒤 종료 코드 1 → 실패 (끝 기록 · 장부 rc 1 · 멈춤 · 다음 런 안 띄움 · 종료 {rc})")
        chk(run(b12, "cond550", card_p=cX, **link_env(readout_rec(b12)))[0] == 14, "⛔음성: 실패로 멈춘 큐를 다시 띄우면 거부")
        b13 = mkbase()
        rc, out = run(b13, "cond550", FAKE_NAN_AFTER="300", **link_env(readout_rec(b13)))
        z13 = load_json(b13 / cond_runs[0] / END) or {}
        chk(rc == 4 and z13.get("driver_rc") == 0 and z13.get("status") == "failed" and any("온도" in r for r in z13.get("reasons", [])),
            f"⛔음성: 드라이버 종료 코드 0 인데 동역학이 깨졌다 (골격 NaN · md.log 온도 NaN) → 완료가 아니다 (종료 {rc})")
        b14 = mkbase()
        rc, out = run(b14, "cond550", FAKE_NO_TURBO="1", **link_env(readout_rec(b14)))
        z14 = load_json(b14 / cond_runs[0] / END) or {}
        chk(rc == 9 and z14.get("status") == "failed" and z14.get("killed") is True and any("추론 모드" in r for r in z14.get("reasons", [])),
            f"⛔음성: 실제 추론 모드가 turbo 가 아니면 (기본 모드로 내려감) 감시가 드라이버를 세운다 · 실패 · 멈춤 (종료 {rc})")
        b18 = mkbase()
        rc, out = run(b18, "cond550", FAKE_EXIT_RC="3", **link_env(readout_rec(b18)))
        z18 = load_json(b18 / cond_runs[0] / END) or {}
        chk(rc == 4 and z18.get("driver_rc") == 3 and z18.get("status") == "failed" and z18.get("reasons") == ["드라이버 종료 코드 3 ≠ 0"]
            and not (b18 / cond_runs[1]).exists(),
            f"⛔음성: 산출물은 다 멀쩡한데 드라이버 종료 코드만 3 → 실패 (종료 코드를 삼키지 않는다 · 리뷰 DZ P1-1 · 종료 {rc})")
        for kind, kw in (("msd", "msd.json"), ("traj", "traj.xyz 프레임 29"), ("aimd", "aimd_results n_frames"),
                         ("ens", "ensemble_results uma_task"), ("mdlog", "md.log 머리"), ("mdhead", "md.log 머리 [0, ")):
            bC = mkbase()
            rc, out = run(bC, "cond550", FAKE_CORRUPT=kind, FAKE_CORRUPT_DIR=str(bC / cond_runs[0]), **link_env(readout_rec(bC)))
            zC = load_json(bC / cond_runs[0] / END) or {}
            chk(rc == 4 and zC.get("driver_rc") == 0 and zC.get("status") == "failed" and any(kw in r for r in zC.get("reasons", []))
                and not (bC / cond_runs[1]).exists(),
                f"⛔음성: 종료 코드 0 인데 산출물 ({kind}) 이 깨졌다 → 완료가 아니다 (실패 · 멈춤 · 종료 {rc} · "
                f"{'; '.join(zC.get('reasons', []))[:80]})")
        b19 = mkbase()
        ini19 = b19 / "A" / "init" / "seed11_final.xyz"
        rc, out = run(b19, "cond550", FAKE_TOUCH_INIT=str(ini19), FAKE_TOUCH_AFTER="1400", **link_env(readout_rec(b19)))
        z19 = load_json(b19 / cond_runs[0] / END) or {}
        chk(rc == 4 and z19.get("status") == "failed" and z19.get("killed") is False and any("config.xyz ≠ init" in r for r in z19.get("reasons", [])),
            f"⛔음성: 런 도중 init 사본이 바뀌면 (감시가 config = init 을 본 뒤) 끝 검사가 잡는다 · 실패 · 멈춤 (종료 {rc})")
        # ── 음성: 큐가 죽어도 드라이버가 잠금을 쥔다 (pass_fds) · 끊긴 런 = 비용 미확정 (리뷰 DZ P1 — 끊긴 상태에서 이어 돌기) ──
        cL = card("cardL.json", conditional={"T_K": 550, "prod_ps": 20.0})
        b20 = mkbase()
        p20 = run(b20, "cond550", card_p=cL, wait=False, **link_env(readout_rec(b20)))
        t_ = time.time()
        while not (b20 / cond_runs[0] / PIDF).exists() and time.time() - t_ < 120:
            time.sleep(0.05)
        dpid = (load_json(b20 / cond_runs[0] / PIDF) or {}).get("pid")

        def alive(pid):
            try:
                return pid is not None and "State:\tZ" not in pathlib.Path(f"/proc/{pid}/status").read_text()
            except OSError:
                return False
        os.kill(p20.pid, 9)                                          # 큐 (python) 만 죽인다 — 드라이버는 고아로 계속 돈다
        p20.communicate(timeout=60)
        was_alive = alive(dpid)
        rc_a, _ = run(b20, "cond550", card_p=cL, **link_env(readout_rec(b20)))
        while alive(dpid) and time.time() - t_ < 600:
            time.sleep(0.2)
        rc_b, out_b = run(b20, "cond550", card_p=cL, **link_env(readout_rec(b20)))
        chk(was_alive and rc_a == 10 and rc_b == 15 and not (b20 / cond_runs[0] / END).exists() and "끊긴 런" in out_b
            and not (b20 / cond_runs[1]).exists(),
            f"⛔음성: 큐를 죽여도 고아 드라이버가 잠금을 쥔다 (다시 띄우면 종료 {rc_a}) · 드라이버가 끝난 뒤에는 끝 기록 없는 런 = 비용 미확정 "
            f"(종료 {rc_b} · 0 으로 세지 않는다)")
        # ── 양성: 첫 런 한도는 길이를 본다 (400 ps 당 first_run_max_h — 800 ps 첫 런은 2 배) ──
        cLA = card("cardLA.json", prod_ps=0.3, first_run_max_h=h1 / 3.0)   # 사다리 0.3 ps · 550 K 3 ps → 한도 = 10 × h1/3
        b21 = mkbase()
        rc, out = run(b21, "cond550", card_p=cLA, **link_env(readout_rec(b21)))
        chk(rc == 0 and all((b21 / r / END).exists() for r in cond_runs),
            f"[양성] 첫 런 한도 = first_run_max_h × (그 런 prod / 사다리 prod) — 사다리 길이 한도 (h1/3) 보다 긴 cond550 첫 런도 멈추지 않는다 (종료 {rc})")
        # ── 음성: GPU 대기 중 카드 · 드라이버 · 큐 파일이 바뀐다 (드라이버 · 큐 파일은 임시 루트 사본 — 저장소 파일은 안 건드린다) ──
        def tamper_between(label, path_of, kw, rooted=False):
            root = None
            if rooted:
                root = td / f"root_{uuid.uuid4().hex[:6]}"
                for f_ in (SELF, DRV):
                    (root / f_.relative_to(REPO)).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f_, root / f_.relative_to(REPO))
            cT = card(f"cardT_{uuid.uuid4().hex[:6]}.json")
            bT = mkbase()
            script = (root / SELF.relative_to(REPO)) if root else None
            pT = run(bT, "cond550", card_p=cT, wait=False, script=script, **link_env(readout_rec(bT)))
            t0_ = time.time()
            while not (bT / cond_runs[0] / START).exists() and time.time() - t0_ < 120:
                time.sleep(0.05)
            (td / "gpu").write_text("9000\n")                         # 첫 런이 도는 동안 GPU 를 바쁘게 — 둘째 런은 GPU 를 기다린다
            while not (bT / cond_runs[0] / END).exists() and time.time() - t0_ < 300:
                time.sleep(0.05)
            time.sleep(0.5)
            f_ = path_of(cT, root)
            f_.write_bytes(f_.read_bytes() + b"\n#")                   # 바이트만 바꾼다 (동작은 같다) — 지문이 바뀐다
            (td / "gpu").write_text("3000\n")
            pT.communicate(timeout=600)
            sT = stops_of(bT)
            chk(pT.returncode == 8 and not (bT / cond_runs[1]).exists() and len(sT) == 1 and kw in sT[0]["reason"],
                f"⛔음성: GPU 대기 중 바뀐 {label} → 실행 직전 다시 해시에서 둘째 런 전에 멈춘다 (종료 {pT.returncode})")
        tamper_between("카드 파일", lambda c_, r_: c_, "카드 sha256")
        tamper_between("드라이버", lambda c_, r_: r_ / DRV.relative_to(REPO), "드라이버 sha256", rooted=True)
        tamper_between("큐 파일 (이 파일)", lambda c_, r_: r_ / SELF.relative_to(REPO), "큐 파일 sha256", rooted=True)
        # ── 음성: 끊긴 v2 런 ──
        b15 = mkbase()
        (b15 / cond_runs[0]).mkdir(parents=True)
        (b15 / cond_runs[0] / START).write_text(json.dumps({"kind": "li2s3_stage2_exec_start/v2", "run_id": "x", "phase": "cond550"}))
        chk(run(b15, "cond550", **link_env(readout_rec(b15)))[0] == 15, "⛔음성: 시작 기록만 있는 (끊긴) v2 런 → 비용 미확정 · 시작하지 않는다")
        # ── 음성: 카드 · 결정 · 코드 지문 · 환경변수 ──
        b16 = mkbase()
        chk(run(b16, "cond550", card_p=card("cS.json", queue_v2={"sha16": "0" * 16, "decision": D_Q2}), **link_env(readout_rec(b16)))[0] == 7,
            "⛔음성: 카드가 고정한 v2 sha16 ≠ 이 파일 → 거부")
        chk(run(b16, "cond550", card_p=card("cD.json", drv16="1" * 16), **link_env(readout_rec(b16)))[0] == 7, "⛔음성: 드라이버 sha16 ≠ 카드 → 거부")
        chk(run(b16, "cond550", card_p=card("cP.json", queue_v2={"sha16": me16, "decision": "D-TEST-proposed"}), **link_env(readout_rec(b16)))[0] == 6,
            "⛔음성: v2 를 승인한 결정이 active 가 아니면 거부")
        cNo = td / "cNo.json"
        d_ = json.loads(CARD0.read_text())
        d_["기계_판독_값"]["stage2"].pop("cost_estimate_h_per_ps")
        cNo.write_text(json.dumps(d_, ensure_ascii=False))
        chk(run(b16, "cond550", card_p=cNo, **link_env(readout_rec(b16)))[0] == 6, "⛔음성: 카드에 v2 기계 값 (길이 반영 견적) 이 없으면 거부")
        chk(run(b16, "ladder")[0] == 13, "⛔음성: 모르는 PHASE (사다리 16 런은 v1 몫) → 거부")
        rc, out = run(b16, "cond550", DRY_RUN="1", TEMPS="900", PROD="7", VSEED_OFFSET="9000", SEEDS="99", **link_env(readout_rec(b16)))
        chk(rc == 0 and "--temperatures 550" in out and "--prod_ps 3 " in out and "--seed 3011" in out and "900" not in out.split("계획")[-1]
            and not (b16 / "queue_v2_stops.jsonl").exists() and not any((b16 / r).exists() for r in cond_runs),
            f"⛔음성: TEMPS=900 PROD=7 VSEED_OFFSET=9000 은 무시 — 계획은 카드 값 (550 K · 3 ps · --seed 3011) · DRY_RUN 은 아무것도 안 쓴다 (종료 {rc})")
    print(f"selftest {'PASS' if not fails else 'FAIL'} — {n_ok}/{n_ok + len(fails)} ({time.time() - t_all:.0f} s)")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
PYEOF
