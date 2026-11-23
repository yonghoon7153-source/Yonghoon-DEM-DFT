#!/usr/bin/env bash
# =============================================================================
# run_b2o3_11b_md.sh — b2o3 11b 골격 열적 안정 MD 큐 (gabia · UMA · 두 줄)
#
# 근거: db/properties/b2o3_bo_placement_estimand_2026_11_09.json
#         개정_1_셀구축_v1_2026_11_09.단계별_값.11b_골격_열적안정 (active · 온도 · 시드 · 대조 · 문턱)
#       db/properties/cell_construction_protocol_v1_2026_11_09.json 단계.11_안정성.11b (방법 · 대조 · 판정 틀)
#       사용자 발사 2026-11-23 ('발사 — gabia 혼자' · 한 번에 2 런) · 런로그 11b_* 키
#
# 하는 일: 계획 (PLAN · b2o3_bo_11b_plan/v1) 의 단위 (배치 · 시드) 마다 표준 MD 드라이버
#   (tools/modelc_v3/disorder_ensemble_diffusion.py) 를 한 번 띄워 네 온도를 차례로 돈다 →
#   $OUT/<이름>/s<시드>/d0.00_cfg0/T<K>/traj.xyz — 판독 도구 framework_site_census.py --aggregate 의
#   s<seed>/d…_cfg…/T<K> 꼴 그대로. 줄 (lane) 마다 단위를 차례로 · 두 줄을 같이 돌린다.
#
# 쓰는 법
#   bash tools/doping/run_b2o3_11b_md.sh --selftest
#   R=… PY=… DRV=… PLAN=… DRY_RUN=1 bash tools/doping/run_b2o3_11b_md.sh   # 계획 · 해시 · 시작 파일만 (드라이버 안 띄움)
#   R=… PY=… DRV=… PLAN=… bash tools/doping/run_b2o3_11b_md.sh             # tmux 안에서
#
# 단위를 띄우기 전에 (단위마다)
#   ① 시작 파일: b2o3 = 계획의 sha256 · 대조 = 대조 이완 기록 (converged · fmax ≤ 계획 · TIME 0 · 셀 포함 · 목적 ·
#      입력 파일 해시 · 출력 해시 = 실제 파일) 을 대조 — 어긋나면 그 줄을 멈춘다 (5)
#   ② pw.x 없음 (gabia: GPU pw.x 와 UMA 공존 금지) — 있으면 기다린다 (POLL_S 마다 · 30 분마다 한 줄)
#   ③ GPU 여유 ≥ MIN_FREE_MIB — 아니면 기다린다 (WAIT_MAX_S > 0 이면 그만큼만 기다리고 멈춘다 — 시험용)
#   ④ 같은 out_root 로 도는 python 이 있으면 멈춘다 (9) · out_root 가 이미 있으면 끝 기록이 있으면 건너뛰고
#      없으면 그 줄을 멈춘다 (6 · 반쯤 남은 출력에 새 런을 섞지 않는다)
#   ⑤ 큐 시작부터 CAP_WALL_H 시간이 지났으면 새 단위를 띄우지 않는다 (카드 안정성 상한 150 GPU-h)
# 단위가 끝나면: rc 0 · 네 온도 모두 traj.xyz (프레임 ≥ MIN_FRAMES) · aimd_results.json · msd.json · ensemble_results.json
#   → <out_root>.done.json (traj sha256 · 프레임 수 · 시간) · 아니면 <out_root>.fail.json 을 쓰고 다음 단위로
#
# 종료 코드: 0 모두 끝 (실패 단위가 있어도 — 요약 줄에 셈) · 2 환경 · 3 계획 · 4 드라이버 판 · 5 시작 파일 ·
#   6 끝 기록 없는 자리 · 7 pw.x 대기 시간 초과 · 8 GPU 대기 시간 초과 · 9 같은 런이 돈다
#   (줄 하나가 멈추면 다른 줄은 계속 돈다 — 요약 줄에 줄마다 코드)
#
# ⛔ 이 도구가 못 하는 것
#   · 판정하지 않는다 — 골격 사건 (census) · β 는 판독 블록이 한다 (계약 = 런로그 11b_판독_계약_결과_전)
#   · 수송값을 읽지 않는다 — 드라이버가 D · Ea 를 파일에 쓰지만 2 단계는 전도도를 재지 않는다 (08-25 마감 · 카드 ⛔)
#   · 런 도중에 뜬 pw.x 는 막지 못한다 — 단위를 띄우기 전에만 막고, 도중에는 로그에 경고 줄만 남긴다
#   · 실패한 단위를 다시 돌리지 않는다 (사용자 결정) · 궤적이 물리적으로 맞는지 보지 않는다 (프레임 수 · 해시만)
#   · GPU 에 우리 말고 다른 UMA 잡이 있어도 막지 않는다 (여유 VRAM 만 본다)
# =============================================================================
set -u

HPY=${HPY:-python3}
NVSMI=${NVSMI:-nvidia-smi}
MIN_FREE_MIB=${MIN_FREE_MIB:-6000}
POLL_S=${POLL_S:-300}
WAIT_MAX_S=${WAIT_MAX_S:-0}
MIN_FRAMES=${MIN_FRAMES:-4000}
DRY_RUN=${DRY_RUN:-0}

ts(){ date '+%F %T'; }

helper(){   # $1 = 하위 명령 · 나머지 인자 — 계획 · 대조 이완 기록 · 끝 기록
"$HPY" - "$@" <<'PY'
import hashlib, json, math, os, sys
from pathlib import Path

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def die(msg, code=3):
    print(f"⛔ {msg}", file=sys.stderr); sys.exit(code)

TEMPS = [300, 600, 800, 1000]
NEED_ARGS = [["--supercell", "1", "1", "1"], ["--disorder_levels", "0"], ["--n_configs", "1"],
             ["--temperatures", "300", "600", "800", "1000"], ["--equilib_ps", "5"], ["--prod_ps", "400"],
             ["--timestep_fs", "2"], ["--friction", "0.02"], ["--save_fs", "100"], ["--fit_window_ps", "2", "50"],
             ["--save_traj"], ["--turbo"], ["--device", "cuda"]]
RUNNER_OWNS = {"--v0_xyz", "--label", "--out_root", "--seed"}

def load_plan(p):
    try:
        P = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        die(f"계획을 못 읽는다: {e}")
    if P.get("schema") != "b2o3_bo_11b_plan/v1": die("계획 schema 가 b2o3_bo_11b_plan/v1 이 아니다")
    if P.get("purpose") != "b2o3_bo/stage11b_md": die("계획 purpose 가 b2o3_bo/stage11b_md 가 아니다")
    if P.get("temperatures") != TEMPS: die(f"온도가 카드 값 {TEMPS} 가 아니다")
    a = P.get("driver_args")
    if not isinstance(a, list) or not all(isinstance(x, str) for x in a): die("driver_args 가 문자열 목록이 아니다")
    for need in NEED_ARGS:
        if not any(a[i:i + len(need)] == need for i in range(len(a))):
            die(f"driver_args 에 {' '.join(need)} 가 없다")
    if set(a) & RUNNER_OWNS: die(f"driver_args 에 실행기가 정할 인자 {sorted(set(a) & RUNNER_OWNS)} 가 있다")
    if not (isinstance(P.get("vseed_offset"), int) and P["vseed_offset"] >= 0): die("vseed_offset 이 0 이상 정수가 아니다")
    d = P.get("driver_sha256", "")
    if not (isinstance(d, str) and len(d) == 64): die("driver_sha256 이 없다")
    cap = P.get("cap_wall_h")
    if not (isinstance(cap, (int, float)) and 0 < cap <= 150): die("cap_wall_h 가 (0, 150] 밖이다 (카드 상한 150)")
    C = P.get("control") or {}
    for k in ("source_sha256", "relax_out", "relax_purpose", "relax_fmax", "name"):
        if k not in C: die(f"control.{k} 가 없다")
    U = P.get("units")
    if not isinstance(U, list) or len(U) != 8: die("단위가 8 개가 아니다 (배치 3 + 대조 1 · 시드 2)")
    ids, pairs = set(), set()
    seeds_by_name = {}
    for u in U:
        for k in ("id", "lane", "name", "kind", "seed", "start"):
            if k not in u: die(f"단위에 {k} 가 없다: {u}")
        if u["id"] in ids: die(f"단위 id 중복 {u['id']}")
        ids.add(u["id"])
        if (u["name"], u["seed"]) in pairs: die(f"(이름, 시드) 중복 {u['name']} s{u['seed']}")
        pairs.add((u["name"], u["seed"]))
        if u["lane"] not in (1, 2): die(f"줄은 1 · 2 만: {u['id']}")
        if u["seed"] not in (1, 2): die(f"시드는 1 · 2 만: {u['id']}")
        if any(c in u["name"] for c in "/ \t") or not u["name"]: die(f"이름에 / · 공백: {u['id']}")
        if u["kind"] == "b2o3":
            if not (isinstance(u.get("sha256"), str) and len(u["sha256"]) == 64): die(f"b2o3 단위에 sha256 이 없다: {u['id']}")
        elif u["kind"] == "control":
            if u.get("sha256") is not None: die(f"대조 단위에 고정 sha256 을 적지 않는다 (이완 기록에서 읽는다): {u['id']}")
            if u["name"] != C["name"]: die(f"대조 단위 이름 ≠ control.name: {u['id']}")
            if u["start"] != f"{C['relax_out']}/{C['name']}/post_relax.xyz": die(f"대조 단위 시작 ≠ 이완 출력: {u['id']}")
        else:
            die(f"kind 는 b2o3 · control 만: {u['id']}")
        if u["start"].startswith("/") or ".." in Path(u["start"]).parts: die(f"시작 경로는 R 아래 상대경로만: {u['id']}")
        seeds_by_name.setdefault(u["name"], set()).add(u["seed"])
    if len(seeds_by_name) != 4 or any(s != {1, 2} for s in seeds_by_name.values()):
        die("이름 넷 (배치 3 + 대조 1) 마다 시드 1 · 2 가 다 있어야 한다")
    if sum(1 for u in U if u["kind"] == "control") != 2: die("대조 단위가 2 개 (시드 1 · 2) 가 아니다")
    return P

def control_check(R, P):
    C = P["control"]
    f = Path(R) / C["relax_out"] / "anneal_results.json"
    if not f.is_file(): die(f"대조 이완 기록이 없다: {f}", 5)
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        die(f"대조 이완 기록을 못 읽는다: {e}", 5)
    rs = [x for x in d.get("results", []) if x.get("name") == C["name"]]
    if len(rs) != 1: die(f"대조 이완 기록에 {C['name']} 가 하나가 아니다 ({len(rs)})", 5)
    r = rs[0]; idn = r.get("identity") or {}
    probs = []
    if r.get("status") != "converged" or r.get("converged") is not True: probs.append(f"status {r.get('status')}")
    fm = r.get("fmax_final")
    if not (isinstance(fm, (int, float)) and math.isfinite(fm) and fm <= float(C["relax_fmax"])): probs.append(f"fmax_final {fm}")
    if idn.get("time_ps") != 0 or idn.get("stage") != "relax_only": probs.append(f"time_ps {idn.get('time_ps')} · stage {idn.get('stage')}")
    if idn.get("cell_relax") is not True: probs.append("cell_relax 아님")
    if idn.get("relax_fmax") != C["relax_fmax"]: probs.append(f"relax_fmax {idn.get('relax_fmax')}")
    if idn.get("purpose") != C["relax_purpose"]: probs.append(f"purpose {idn.get('purpose')}")
    if idn.get("input_file_sha256") != C["source_sha256"]: probs.append("입력 파일 해시 ≠ 계획 control.source_sha256")
    out = (r.get("outputs") or {}).get("post_relax") or {}
    pr = Path(R) / C["relax_out"] / C["name"] / "post_relax.xyz"
    if not pr.is_file(): probs.append(f"이완 구조가 없다 {pr}")
    elif out.get("sha256") != sha(pr): probs.append("이완 구조 해시 ≠ 기록의 outputs.post_relax.sha256")
    if probs: die("대조 이완 기록 불일치 — " + " · ".join(probs), 5)
    print(sha(pr))

def finish(out_root, rc, t0, t1, start_sha, driver_sha, min_frames):
    o = Path(out_root)
    per_t, probs = {}, []
    if rc != 0: probs.append(f"rc {rc}")
    if not (o / "ensemble_results.json").is_file(): probs.append("ensemble_results.json 없음")
    for T in TEMPS:
        d = o / "d0.00_cfg0" / f"T{T}"
        tr, ar, mj = d / "traj.xyz", d / "aimd_results.json", d / "msd.json"
        rec = {}
        if tr.is_file():
            n = 0
            with open(tr, "rb") as f:
                lines = f.read().split(b"\n")
            i = 0
            while i < len(lines) and lines[i].strip():
                try:
                    k = int(lines[i].strip())
                except ValueError:
                    probs.append(f"T{T} traj 머리줄이 원자 수가 아니다 (줄 {i + 1})"); break
                n += 1; i += k + 2
            rec.update(traj_sha256=sha(tr), frames=n, bytes=tr.stat().st_size)
            if n < min_frames: probs.append(f"T{T} 프레임 {n} < {min_frames}")
        else:
            probs.append(f"T{T} traj.xyz 없음")
        for nm, p in (("aimd_results.json", ar), ("msd.json", mj)):
            if not p.is_file(): probs.append(f"T{T} {nm} 없음")
        per_t[f"T{T}"] = rec
    body = {"out_root": str(o), "rc": rc, "start_s": t0, "end_s": t1, "wall_h": round((t1 - t0) / 3600, 3),
            "start_sha256": start_sha, "driver_sha256": driver_sha, "per_T": per_t, "problems": probs,
            "note": "판정 아님 — 끝 기록 (rc · 파일 · 프레임 · 해시) · 수송값은 읽지 않는다"}
    tgt = Path(str(o) + (".fail.json" if probs else ".done.json"))
    tgt.write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(("FAIL " + " · ".join(probs)) if probs else f"DONE {body['wall_h']} h · 프레임 " + " ".join(f"{k}:{v.get('frames')}" for k, v in per_t.items()))

cmd = sys.argv[1]
if cmd == "plan":
    P = load_plan(sys.argv[2])
    print("G", P["driver_sha256"], P["vseed_offset"], P["cap_wall_h"])
    print("A", json.dumps(P["driver_args"]))
    for u in P["units"]:
        print("U", u["id"], u["lane"], u["name"], u["kind"], u["seed"], u["start"], u.get("sha256") or "-")
elif cmd == "control":
    control_check(sys.argv[2], load_plan(sys.argv[3]))
elif cmd == "finish":
    finish(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], sys.argv[7], int(sys.argv[8]))
elif cmd == "args":
    for x in json.loads(sys.argv[2]):
        print(x)
else:
    die(f"모르는 하위 명령 {cmd}")
PY
}

free_mib(){ "$NVSMI" --query-gpu=memory.total,memory.used --format=csv,noheader,nounits 2>/dev/null | awk -F, 'NR==1 { t=$1+0; u=$2+0; if (t > 0) print t-u }'; }
pwx_on(){ pgrep -x pw.x > /dev/null 2>&1; }

wait_for(){   # $1 이름 · $2 조건 함수 (참이면 기다림) · $3 시간 초과 코드
  local what=$1 cond=$2 code=$3 t0 last=0 now
  t0=$(date +%s)
  while $cond; do
    now=$(date +%s)
    if [ "$WAIT_MAX_S" -gt 0 ] && [ $((now - t0)) -ge "$WAIT_MAX_S" ]; then say "⛔ $what 대기 ${WAIT_MAX_S} 초 초과 — 이 줄을 멈춘다"; return "$code"; fi
    if [ $((now - last)) -ge 1800 ]; then say "… $what 기다리는 중 ($(( (now - t0) / 60 )) 분)"; last=$now; fi
    sleep "$POLL_S"
  done
  return 0
}
vram_low(){ local f; f=$(free_mib); [ -z "$f" ] || [ "$f" -lt "$MIN_FREE_MIB" ]; }

same_run(){   # $1 out_root — 그 경로로 도는 python 이 있나 (pgrep 은 자기 자신 · 감싼 셸을 세니 comm 으로 거른다)
  local p
  for p in $(pgrep -f -- "--out_root $1" 2>/dev/null); do
    case "$(cat /proc/$p/comm 2>/dev/null)" in python*) return 0;; esac
  done
  return 1
}

say(){ echo "$(ts) [줄 ${LANE:-·}] $*" | tee -a "$QLOG"; }

run_lane(){   # $1 = 줄 번호 — 그 줄의 단위를 계획 순서대로
  local LANE=$1 id lane name kind seed start want out cur t0 t1 rc res wpid
  while read -r _ id lane name kind seed start want; do
    [ "$lane" = "$LANE" ] || continue
    if [ $(( $(date +%s) - QSTART )) -ge $(( CAP_H * 3600 )) ]; then say "⛔ 큐 시작부터 ${CAP_H} 시간 (카드 상한) — $id 부터 띄우지 않는다"; return 0; fi
    out=$OUT/$name/s$seed
    if [ -e "$out.done.json" ]; then say "↷ $id 끝 기록 있음 — 건너뜀"; continue; fi
    if [ -e "$out" ] || [ -e "$out.fail.json" ]; then say "⛔ $id 자리 $out 가 이미 있는데 끝 기록이 없다 — 이 줄을 멈춘다 (반쯤 남은 출력에 섞지 않는다 · 사용자 결정)"; return 6; fi
    if [ "$kind" = control ]; then
      cur=$(helper control "$R" "$PLAN") || { say "⛔ $id 대조 이완 기록 검사 실패 — 이 줄을 멈춘다"; return 5; }
    else
      [ -f "$R/$start" ] || { say "⛔ $id 시작 파일 없음 $R/$start — 이 줄을 멈춘다"; return 5; }
      cur=$(sha256sum "$R/$start" | cut -c1-64)
      [ "$cur" = "$want" ] || { say "⛔ $id 시작 파일 해시 ${cur:0:16} ≠ 계획 ${want:0:16} — 이 줄을 멈춘다"; return 5; }
    fi
    wait_for "pw.x 없어지기" pwx_on 7 || return 7
    wait_for "GPU 여유 ${MIN_FREE_MIB} MiB" vram_low 8 || return 8
    if same_run "$out"; then say "⛔ $id 같은 out_root 로 도는 python 이 있다 — 이 줄을 멈춘다"; return 9; fi
    mkdir -p "$OUT/$name"
    say "▶ $id ($kind · 시드 $seed · 드라이버 --seed $((VOFF + seed))) 시작 · 시작 파일 ${cur:0:16} · GPU 여유 $(free_mib) MiB"
    t0=$(date +%s)
    ( while sleep "$POLL_S"; do pwx_on && echo "$(ts) [줄 $LANE] ⚠ $id 도는 중 pw.x 가 떴다 — UMA 공존 금지 규칙 (사용자 확인)" >> "$QLOG"; done ) < /dev/null &
    wpid=$!
    "$PY" "$DRV" --v0_xyz "$R/$start" --label "b2o3_11b_${name}_s${seed}" --out_root "$out" --seed $((VOFF + seed)) "${DARGS[@]}" < /dev/null > "$out.log" 2>&1
    rc=$?
    kill "$wpid" 2>/dev/null; wait "$wpid" 2>/dev/null
    t1=$(date +%s)
    res=$(helper finish "$out" "$rc" "$t0" "$t1" "$cur" "$DSHA" "$MIN_FRAMES" 2>&1)
    say "■ $id $res"
  done < "$UNITS"
  return 0
}

selftest(){
  local T pass=0 fail=0 rc out
  T=$(mktemp -d)
  ck(){ if eval "$2"; then pass=$((pass + 1)); echo "  ✔ $1"; else fail=$((fail + 1)); echo "  ✘ $1"; fi; }
  mkdir -p "$T/bin" "$T/R/s11a_relax/A" "$T/R/s11a_relax/B" "$T/R/s11a_relax/C" "$T/R/ctrl/M"
  cat > "$T/bin/nvidia-smi" <<'EOF'
#!/bin/sh
echo "49140, ${FAKE_USED:-1000}"
EOF
  cat > "$T/drv.py" <<'EOF'
import argparse, json, os, sys
from pathlib import Path
ap = argparse.ArgumentParser()
for k in ("--v0_xyz", "--label", "--out_root", "--seed", "--disorder_levels", "--n_configs", "--equilib_ps", "--prod_ps",
          "--timestep_fs", "--friction", "--save_fs", "--device"):
    ap.add_argument(k)
ap.add_argument("--supercell", nargs=3); ap.add_argument("--temperatures", nargs="+"); ap.add_argument("--fit_window_ps", nargs=2)
ap.add_argument("--save_traj", action="store_true"); ap.add_argument("--turbo", action="store_true")
a = ap.parse_args()
o = Path(a.out_root); o.mkdir(parents=True, exist_ok=True)
(o / "run_meta.json").write_text(json.dumps(vars(a)))
fail = os.environ.get("FAKE_FAIL", "")
short = os.environ.get("FAKE_SHORT", "")
for T in a.temperatures:
    d = o / "d0.00_cfg0" / f"T{T}"; d.mkdir(parents=True, exist_ok=True)
    n = 3 if (short and short in a.label and T == "800") else 5
    with open(d / "traj.xyz", "w") as f:
        for i in range(n):
            f.write("2\nLattice=\"5 0 0 0 5 0 0 0 5\"\nLi 0 0 0\nS 1 1 1\n")
    (d / "aimd_results.json").write_text("{}"); (d / "msd.json").write_text("{}")
if fail and fail in a.label:
    sys.exit(3)
(o / "ensemble_results.json").write_text("{}")
EOF
  chmod +x "$T/bin/nvidia-smi"
  for x in A B C; do echo "start $x" > "$T/R/s11a_relax/$x/post_relax.xyz"; done
  echo "ctrl src" > "$T/ctrl_src.xyz"
  echo "ctrl relaxed" > "$T/R/ctrl/M/post_relax.xyz"
  local DS SA SB SC SM SS
  DS=$(sha256sum "$T/drv.py" | cut -c1-64); SS=$(sha256sum "$T/ctrl_src.xyz" | cut -c1-64)
  SA=$(sha256sum "$T/R/s11a_relax/A/post_relax.xyz" | cut -c1-64); SB=$(sha256sum "$T/R/s11a_relax/B/post_relax.xyz" | cut -c1-64)
  SC=$(sha256sum "$T/R/s11a_relax/C/post_relax.xyz" | cut -c1-64); SM=$(sha256sum "$T/R/ctrl/M/post_relax.xyz" | cut -c1-64)
  mkplan(){   # $1 출력 · $2 b2o3 A 의 sha (바꿔 음성) · $3 드라이버 sha
    "$HPY" - "$1" "$2" "$SB" "$SC" "$3" "$SS" <<'EOF'
import json, sys
o, sa, sb, sc, ds, ss = sys.argv[1:7]
args = ["--supercell", "1", "1", "1", "--disorder_levels", "0", "--n_configs", "1", "--temperatures", "300", "600", "800", "1000",
        "--equilib_ps", "5", "--prod_ps", "400", "--timestep_fs", "2", "--friction", "0.02", "--save_fs", "100",
        "--fit_window_ps", "2", "50", "--save_traj", "--turbo", "--device", "cuda"]
U = []
for s in (1, 2):
    U.append({"id": f"ctrl_s{s}", "lane": s, "name": "M", "kind": "control", "seed": s, "start": "ctrl/M/post_relax.xyz"})
    for n, h in (("A", sa), ("B", sb), ("C", sc)):
        U.append({"id": f"{n}_s{s}", "lane": s, "name": n, "kind": "b2o3", "seed": s, "start": f"s11a_relax/{n}/post_relax.xyz", "sha256": h})
json.dump({"schema": "b2o3_bo_11b_plan/v1", "purpose": "b2o3_bo/stage11b_md", "temperatures": [300, 600, 800, 1000],
           "driver_args": args, "vseed_offset": 11000, "driver_sha256": ds, "cap_wall_h": 150,
           "control": {"name": "M", "source_sha256": ss, "relax_out": "ctrl", "relax_purpose": "b2o3_bo/stage11b_control_relax", "relax_fmax": 0.01},
           "units": U}, open(o, "w"), indent=1)
EOF
  }
  mkrec(){   # $1 status · $2 fmax · $3 purpose · $4 출력 sha
    "$HPY" - "$T/R/ctrl/anneal_results.json" "$1" "$2" "$3" "$4" "$SS" <<'EOF'
import json, sys
o, st, fm, pu, osha, ss = sys.argv[1:7]
json.dump({"results": [{"name": "M", "status": st, "converged": st == "converged", "fmax_final": float(fm),
           "identity": {"time_ps": 0, "stage": "relax_only", "cell_relax": True, "relax_fmax": 0.01, "purpose": pu, "input_file_sha256": ss},
           "outputs": {"post_relax": {"rel": "M/post_relax.xyz", "sha256": osha}}}]}, open(o, "w"))
EOF
  }
  runq(){   # 환경을 깨끗이 해 하위 셸로 · 출력은 $T/q.out
    ( export PATH="$T/bin:$PATH" R="$T/R" PY="$HPY" DRV="$T/drv.py" PLAN="$T/plan.json" OUT="$T/R/out" POLL_S=1 MIN_FRAMES=5 "$@"
      bash "$SELF" > "$T/q.out" 2>&1 ); echo $?
  }
  reset_out(){ rm -rf "$T/R/out"; }

  echo "== selftest run_b2o3_11b_md.sh"
  mkplan "$T/plan.json" "$SA" "$DS"; mkrec converged 0.009 b2o3_bo/stage11b_control_relax "$SM"
  rc=$(runq); ck "[양성] 8 단위 다 끝 → 종료 0 · 끝 기록 8 · 실패 0" \
    "[ $rc = 0 ] && [ \$(ls $T/R/out/*/*.done.json 2>/dev/null | wc -l) = 8 ] && [ \$(ls $T/R/out/*/*.fail.json 2>/dev/null | wc -l) = 0 ]"
  ck "[양성] 드라이버 --seed = 11000 + 시드 · 계획 인자 그대로 (run_meta)" \
    "grep -q '\"seed\": \"11002\"' $T/R/out/B/s2/run_meta.json && grep -q '\"prod_ps\": \"400\"' $T/R/out/B/s2/run_meta.json && grep -q '\"temperatures\": \[\"300\", \"600\", \"800\", \"1000\"\]' $T/R/out/B/s2/run_meta.json"
  ck "[양성] 대조 단위는 이완 기록에서 읽은 해시로 시작 (로그 줄)" "grep -q \"ctrl_s1 (control .* 시작 파일 ${SM:0:16}\" $T/R/out/queue.log"
  rc=$(runq); ck "[양성] 다시 띄우면 끝 기록 있는 단위는 건너뜀 (드라이버 안 띄움)" "[ $rc = 0 ] && [ \$(grep -c '건너뜀' $T/R/out/queue.log) = 8 ]"

  reset_out; mkplan "$T/plan.json" "$(printf '0%.0s' {1..64})" "$DS"
  rc=$(runq); ck "⛔음성: b2o3 시작 파일 해시가 계획과 다르면 그 줄을 멈춘다 (A_s1 · A_s2 둘 다 · 드라이버 안 띄움)" \
    "[ $rc = 5 ] && [ ! -e $T/R/out/A ] && grep -q 'A_s1 시작 파일 해시' $T/R/out/queue.log"
  reset_out; mkplan "$T/plan.json" "$SA" "$DS"; mkrec unconverged 0.02 b2o3_bo/stage11b_control_relax "$SM"
  rc=$(runq); ck "⛔음성: 대조 이완이 미수렴이면 대조 단위를 안 띄우고 그 줄을 멈춘다" "[ $rc = 5 ] && [ ! -e $T/R/out/M ] && grep -q '대조 이완 기록 불일치' $T/q.out"
  reset_out; mkrec converged 0.009 b2o3_bo/stage11a_phonon_relax "$SM"
  rc=$(runq); ck "⛔음성: 대조 이완 기록의 목적이 다르면 멈춘다 (11a 이완 기록을 대조로 쓰지 않는다)" "[ $rc = 5 ] && grep -q 'purpose b2o3_bo/stage11a_phonon_relax' $T/q.out"
  reset_out; mkrec converged 0.009 b2o3_bo/stage11b_control_relax "$(printf 'f%.0s' {1..64})"
  rc=$(runq); ck "⛔음성: 이완 구조 파일이 기록의 출력 해시와 다르면 멈춘다" "[ $rc = 5 ] && grep -q '이완 구조 해시' $T/q.out"
  reset_out; mkrec converged 0.009 b2o3_bo/stage11b_control_relax "$SM"; mkplan "$T/plan.json" "$SA" "$(printf 'a%.0s' {1..64})"
  rc=$(runq); ck "⛔음성: 드라이버 판 (sha256) 이 계획과 다르면 아무것도 안 띄운다 (4)" "[ $rc = 4 ] && [ ! -e $T/R/out/M ]"
  reset_out; mkplan "$T/plan.json" "$SA" "$DS"; mkdir -p "$T/R/out/B/s1"
  rc=$(runq); ck "⛔음성: 끝 기록 없는 자리가 있으면 그 줄을 멈춘다 (6) · 다른 줄은 끝까지" \
    "[ $rc = 6 ] && [ ! -e $T/R/out/B/s1.done.json ] && [ ! -e $T/R/out/C/s1.done.json ] && [ -e $T/R/out/C/s2.done.json ]"
  reset_out; rc=$(runq FAKE_FAIL=b2o3_11b_B_s2); ck "[실패 기록] 드라이버 rc ≠ 0 → fail.json · 다음 단위는 계속 · 종료 0 · 요약에 실패 1" \
    "[ $rc = 0 ] && [ -e $T/R/out/B/s2.fail.json ] && [ -e $T/R/out/C/s2.done.json ] && grep -q '실패 1' $T/R/out/queue.log"
  reset_out; rc=$(runq FAKE_SHORT=b2o3_11b_C_s1); ck "⛔음성: 한 온도라도 프레임이 모자라면 끝이 아니라 실패 기록 (rc 0 이어도)" \
    "[ -e $T/R/out/C/s1.fail.json ] && grep -q 'T800 프레임 3 < 5' $T/R/out/C/s1.fail.json"
  reset_out; rc=$(runq FAKE_USED=46000 WAIT_MAX_S=2); ck "⛔음성: GPU 여유가 모자라면 기다리다 시간 초과로 멈춘다 (8) · 드라이버 안 띄움" "[ $rc = 8 ] && [ ! -e $T/R/out/M ]"
  reset_out; cp /bin/sleep "$T/bin/pw.x"; "$T/bin/pw.x" 30 & local PP=$!; sleep 0.3
  rc=$(runq WAIT_MAX_S=2); kill $PP 2>/dev/null; wait $PP 2>/dev/null
  ck "⛔음성: pw.x 가 돌면 기다리다 시간 초과로 멈춘다 (7) · 드라이버 안 띄움" "[ $rc = 7 ] && [ ! -e $T/R/out/M ]"
  reset_out; "$HPY" - "$T/plan.json" <<'EOF'
import json, sys
p = sys.argv[1]; P = json.load(open(p)); P["driver_args"] = [x for x in P["driver_args"] if x != "--save_traj"]; json.dump(P, open(p, "w"))
EOF
  rc=$(runq); ck "⛔음성: 계획 인자에 --save_traj 가 없으면 계획 거부 (3)" "[ $rc = 3 ] && grep -q 'save_traj' $T/q.out"
  mkplan "$T/plan.json" "$SA" "$DS"; "$HPY" - "$T/plan.json" <<'EOF'
import json, sys
p = sys.argv[1]; P = json.load(open(p)); P["temperatures"] = [600, 650, 700, 1000]; json.dump(P, open(p, "w"))
EOF
  rc=$(runq); ck "⛔음성: 온도가 카드 값이 아니면 계획 거부 (3 · 옛 §8 600/650/700 꼴)" "[ $rc = 3 ]"
  mkplan "$T/plan.json" "$SA" "$DS"; "$HPY" - "$T/plan.json" <<'EOF'
import json, sys
p = sys.argv[1]; P = json.load(open(p)); P["units"] = P["units"][:-1]; json.dump(P, open(p, "w"))
EOF
  rc=$(runq); ck "⛔음성: 단위가 8 개가 아니면 계획 거부 (3)" "[ $rc = 3 ]"
  mkplan "$T/plan.json" "$SA" "$DS"; reset_out; rc=$(runq DRY_RUN=1)
  ck "[DRY_RUN] 시작 파일 · 대조 기록만 보고 드라이버를 안 띄운다" "[ $rc = 0 ] && [ ! -e $T/R/out/M ] && grep -q 'DRY_RUN' $T/q.out"
  echo "  selftest $pass/$((pass + fail)) 통과"
  rm -rf "$T"
  [ "$fail" = 0 ]
}

SELF=$(readlink -f "$0")
if [ "${1:-}" = "--selftest" ]; then selftest; exit $?; fi

for v in R PY DRV PLAN; do
  [ -n "${!v:-}" ] || { echo "⛔ 환경 변수 $v 가 없다"; exit 2; }
done
OUT=${OUT:-$R/s11b_md}
[ -f "$DRV" ] || { echo "⛔ 드라이버 없음 $DRV"; exit 2; }
[ -x "$PY" ] || command -v "$PY" > /dev/null || { echo "⛔ PY 실행 못함 $PY"; exit 2; }
mkdir -p "$OUT"; QLOG=$OUT/queue.log
UNITS=$(mktemp); trap 'rm -f "$UNITS"' EXIT
helper plan "$PLAN" > "$UNITS.all" || { echo "⛔ 계획 거부 — 위 줄"; rm -f "$UNITS.all"; exit 3; }
read -r _ DSHA VOFF CAP_H < <(grep '^G ' "$UNITS.all")
CAP_H=${CAP_H%.*}
mapfile -t DARGS < <(helper args "$(grep '^A ' "$UNITS.all" | cut -c3-)")
grep '^U ' "$UNITS.all" > "$UNITS"; rm -f "$UNITS.all"
cur=$(sha256sum "$DRV" | cut -c1-64)
[ "$cur" = "$DSHA" ] || { echo "⛔ 드라이버 판 ${cur:0:16} ≠ 계획 ${DSHA:0:16} — 아무것도 안 띄운다"; exit 4; }
LANE=·
say "== 11b 큐 · 계획 $(sha256sum "$PLAN" | cut -c1-16) · 드라이버 ${DSHA:0:16} · 단위 $(wc -l < "$UNITS") · 줄 2 · 상한 ${CAP_H} h · GPU 여유 $(free_mib) MiB · pw.x $(pwx_on && echo 있음 || echo 없음)"
if [ "$DRY_RUN" = 1 ]; then
  st=0
  while read -r _ id lane name kind seed start want; do
    if [ "$kind" = control ]; then c=$(helper control "$R" "$PLAN") && say "  DRY_RUN $id 줄 $lane · 대조 이완 기록 통과 · 시작 ${c:0:16}" || { say "  DRY_RUN ⛔ $id 대조 이완 기록"; st=5; }
    else c=$(sha256sum "$R/$start" 2>/dev/null | cut -c1-64); [ "$c" = "$want" ] && say "  DRY_RUN $id 줄 $lane · 시작 해시 같음 ${c:0:16}" || { say "  DRY_RUN ⛔ $id 시작 해시 ${c:0:16} ≠ ${want:0:16}"; st=5; }
    fi
  done < "$UNITS"
  say "DRY_RUN 끝 (드라이버 안 띄움) · 종료 $st"; exit "$st"
fi
QSTART=$(date +%s)
run_lane 1 & P1=$!
run_lane 2 & P2=$!
wait "$P1"; C1=$?; wait "$P2"; C2=$?
LANE=·
nd=$(ls "$OUT"/*/*.done.json 2>/dev/null | wc -l); nf=$(ls "$OUT"/*/*.fail.json 2>/dev/null | wc -l)
say "끝 · 끝 기록 $nd · 실패 $nf · 줄 1 코드 $C1 · 줄 2 코드 $C2"
[ "$C1" = 0 ] && [ "$C2" = 0 ] && exit 0
[ "$C1" != 0 ] && exit "$C1"; exit "$C2"
