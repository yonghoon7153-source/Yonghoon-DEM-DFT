#!/usr/bin/env bash
# =============================================================================
# run_sese_gpu.sh — SE|SE 대조 DFT 잡들을 GPU pw.x 로 **순서대로**, VRAM 가드를 걸고 돌린다.
#
#   입력: tools/wad/se_sym_slab.py --qe_out 이 만든 <IN>/jobs.json + <IN>/<잡>/pw.in
#   결정: D-2026-09-23-wad-se-termination-symmetric · D-2026-09-23-wad-d3-twobody-atm-separate
#         D-2026-09-23-gabia-gpu-exception-sese — gabia 의 *"GPU pw.x ↔ UMA 동시 실행 금지"* 에
#         1저자가 준 **범위 한정 예외**. 아래 가드 조건이 곧 예외의 범위다.
#         ⛔ 2026-09-23 **실행 전 철회 · 미사용 종료** (6층 슬랩 추정 50–56 GB > 48 GB · Codex BW Q8).
#         이제 ALLOW_UMA_COEXIST=1 은 원장에서 **active** 인 결정 ID 를 EXCEPTION_ID 로 줄 때만 켜진다 (⑧).
#
# 실행 (gabia · tmux 안에서):
#   RUN=/data/work/runs/wad_sese_2026_09_23
#   WAIT_PIDS="<li2s 시드 PID 들>" ALLOW_UMA_COEXIST=1 \
#     bash tools/wad/run_sese_gpu.sh db/inputs/wad_sese_control_2026_09_23 $RUN
#   DRY_RUN=1 ...                           점검만 (입력 해시·PP·D3 명시·GPU 상태·가드값). 계산 안 함
#   JOBS="01_bulk_scf 02_s_outer_scf" ...   일부만 (기본 = jobs.json 순서 전부)
#   bash tools/wad/run_sese_gpu.sh --selftest
#
# 예외 가드 (1저자 2026-09-23):
#   ① WAIT_PIDS 가 전부 끝날 때까지 기다린다 — `kill -0` + **cmdline 대조**(PID 재사용 방지).
#   ② 시작 직전 GPU 합계 사용량 < START_MAX_MIB (기본 40960 = 40 GB). 넘으면 60 초마다 다시
#      보고, START_WAIT_S (기본 3600) 안에 안 내려가면 **시작하지 않고** 끝낸다.
#   ③ 도는 동안 SAMPLE_S (기본 2) 초마다 합계 사용량을 본다. KILL_MIB (기본 45056 = 44 GB) 를
#      넘으면 **이 러너가 띄운 트리(래퍼 → mpirun → pw.x)를 PID·comm 대조로** TERM → ≤ 15 초 →
#      남은 것만 KILL 하고 러너를 멈춘다 (⑩).
#      남의 프로세스(UMA)는 건드리지 않는다. 이름으로 죽이지 않는다 (CLAUDE.md: pkill 금지).
#   ④ GPU 에 python(UMA)이 있으면 ALLOW_UMA_COEXIST=1 없이는 시작하지 않는다 —
#      규칙의 기본값은 금지이고, 예외는 **켜야** 켜진다.
#   ④′ 호스트 RAM — gabia 는 CPU 잡(Nd k-탐침 34 GB)과 RAM 을 나눈다. 시작은 MemAvailable ≥
#      HOST_START_MIB (기본 16384), 도는 중 < HOST_KILL_MIB (기본 4096) 면 우리 잡만 멈춘다
#      (OOM 킬러는 우리가 아니라 **가장 큰 잡**을 고른다 — 그게 k-탐침이나 b2o3 일 수 있다).
#   ⑤ 잡마다 피크 합계 VRAM · 우리 pw.x 자기 사용량(읽히면 · **못 읽으면 '—'**, 0 이 아니다) · 벽시계를
#      jobs_run.tsv 에 남긴다. 컨테이너 안에서는 nvidia-smi 가 호스트 PID 를 줘서 자기 사용량은 원리적으로 못 읽는다.
#   ⑩ pw.x 는 **comm 이 pw.x 인 자손**으로 찾는다 — hpcx mpirun 은 래퍼라 첫 자식이 pw.x 가 아니다
#      (2026-09-24 V100 실측: 기록된 PID 는 곧 사라진 보조였고, 가드가 죽은 PID 와 래퍼만 TERM 하게 돼 있었다).
#   ⑦ KISTI 등 여러 GPU: NP=<랭크 수> (≤ 보이는 GPU 수 · 평면파를 랭크에 나눠 GPU 한 장당 메모리를 줄인다 —
#      tools/sdcp/sbatch_phaseB_v3_kisti.sh 와 같은 방식) · PSEUDO_DIR=<그 기계 경로> (실행 폴더 복사본에서만
#      바꾼다 — 원본 입력 해시는 그대로) · NO_LOCK=1 (Lustre 는 flock 이 안 될 수 있다 — 그러면 '이미 도는 중' 으로
#      오판해 조용히 끝난다. Slurm 체인이 단일 실행을 보장할 때만 쓴다).
#   ⑥ ONLY_PIDS (예: b2o3 드라이버 PID) — 잡 시작 직전 GPU 위 프로세스가 **이 목록 안**이어야 한다.
#      예외 조건 *"li2s 시드가 끝나고 b2o3 만 남았을 때"* 를 기계로 건다. WAIT_PIDS 만으로는
#      그 사이 새 UMA 잡(예: li2s seed 5)이 떠도 모른다 (2026-09-23 DRY_RUN 뒤 보강). 목록 밖이 있으면
#      시작하지 않고 ② 와 같이 기다린다. 목록 안 프로세스가 **끝나는 것**은 막지 않는다.
#   ⑧ ALLOW_UMA_COEXIST=1 은 예외를 **쓰겠다**는 선언이다 — EXCEPTION_ID 가 결정 ID(D-…)면
#      db/governance/decisions.json 에서 decision_state 가 **active** 여야 시작한다. 철회·대체·반려·없는 ID·
#      원장을 못 읽음 → 시작하지 않는다 (exit 3). 결정 ID 가 아닌 근거(다른 기계의 승인 문구)는 경고만 남긴다.
#      2026-09-23 예외 철회 뒤 추가: 기본 EXCEPTION_ID 가 철회된 그 결정이라, 이 게이트가 없으면
#      공존 스위치 하나로 **철회된 예외가 조용히 다시 쓰인다**.
#
# ⛔ 이 스크립트가 **못 하는 것**
#   · VRAM 이 표본 간격(SAMPLE_S)보다 빨리 치솟으면 못 막는다 — 가드는 확률적 보호다.
#     UMA 쪽 CUDA OOM 을 **줄일 뿐 막지 못한다**. b2o3 사건빈도 카드는 16번째 런을 금지하므로
#     (D-2026-09-23-b2o3-framework-event-rate) b2o3 런이 죽으면 그 카드의 판정이 먼저다.
#   · 수렴·물리 타당성은 안 본다 — 완료 판정은 JOB DONE + 수렴 줄(+ relax 면 최종 좌표)뿐.
#   · γ·W 를 계산하지 않는다 — 집계는 `python3 tools/wad/se_sym_slab.py --collect <RUN>`.
#   · 문턱 기본값은 gabia A6000 48 GB 기준이다. 다른 기계는 문턱·PWX·EXCEPTION_ID 를 env 로 넘긴다
#     (kgy 3090 24 GB 는 프로세스별 GPU 정보가 막혀 UMA 판정·ONLY_PIDS 가 무력하다 — 러너가 경고한다).
#   · 한 잡이 실패하면 **뒤 잡을 돌리지 않는다** (체계적 원인일 수 있다 — 사람이 본다).
# =============================================================================
set -u
IN=${1:-}; RUN=${2:-}
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# ── 완료 판정 (한 곳에만 둔다 — 재개와 성공이 같은 기준이어야 한다) ─────────────
#   ⛔ 2026-09-25 Codex BX P0 — 옛 판은 relax 를 `End final coordinates` **또는** `bfgs converged` 로 인정했다.
#   QE 7.4.1 은 이완이 **실패**해도(`bfgs failed after … convergence not achieved` · bfgs_module.f90) 최종 좌표와
#   JOB DONE 을 찍으므로, 실패한 이완이 완료로 통과해 집계까지 갔다 (합성 출력으로 재현됨). 이제:
#   ① **마지막 실행**(마지막 `Program PWSCF` 헤더 이후)만 본다 — 앞선 실행의 성공 문구가 살아남지 않게
#   ② relax 는 `bfgs converged` 를 **명시적으로** 요구하고 `bfgs failed` · `convergence not achieved` · nstep 소진을 거부한다
#   ③ scf 도 마지막 실행에서 `convergence has been achieved` 를 요구하고 `convergence NOT achieved` 를 거부한다
_last_run() {  # $1 = pw.out → 마지막 실행의 텍스트 (헤더가 없으면 전체)
  awk '/Program PWSCF/{buf=""} {buf=buf $0 "\n"} END{printf "%s", buf}' "$1"
}
_done() {   # $1 = pw.out · $2 = calc (scf|relax|vc-relax|probe)
  [ -f "$1" ] || return 1
  local T; T=$(_last_run "$1")
  printf '%s' "$T" | grep -aq "JOB DONE" || return 1
  if [ "$2" = probe ]; then
    # 비용 프로브(electron_maxstep 을 자른 SCF)는 수렴이 목적이 아니다 — iteration 이 실제로 돌았는지만 본다.
    # ⛔ 이 갈래로 끝난 잡의 에너지는 값이 아니다 (build_neb_inputs.py --scf_probe 의 금지문).
    printf '%s' "$T" | grep -aqE "convergence (NOT achieved|has been achieved)" || return 1
    printf '%s' "$T" | grep -aq "total energy" || return 1
    return 0
  fi
  printf '%s' "$T" | grep -aq "convergence has been achieved" || return 1
  printf '%s' "$T" | grep -aq "convergence NOT achieved" && return 1
  # ⛔ 2026-09-25 — vc-relax 도 같은 이완 규칙 (옛 판은 relax 만 갈라 vc-relax 를 SCF 기준으로 통과시켰다)
  if [ "$2" = relax ] || [ "$2" = vc-relax ]; then
    printf '%s' "$T" | grep -aq "bfgs converged" || return 1
    printf '%s' "$T" | grep -aqiE "bfgs failed|convergence not achieved|maximum number of steps has been reached" && return 1
  fi
  return 0
}

# ── D3 명시 검사 (D-2026-09-23-wad-d3-twobody-atm-separate enforcement) ─────────
_d3_ok() {  # grimme-d3 를 켠 입력이면 dftd3_threebody 가 적혀 있어야 한다
  if grep -aqiE "vdw_corr *= *'(grimme-d3|dft-d3|d3)'" "$1"; then
    grep -aqiE "dftd3_threebody *= *\.(false|true)\." "$1" || return 1
  fi
  return 0
}

# ── nvidia-smi 프로세스 목록에서 **진짜 프로세스 줄**만 (첫 칸이 PID 숫자) ─────────
_apps_filter() { awk -F', *' '$1 ~ /^[0-9]+$/'; }

# ── ⑦ 랭크 수 ≤ GPU 수 (한 GPU 에 랭크 여럿 = 2026-09-09 gabia np 8 즉사) ──────────
_np_ok() {  # $1 = NP · $2 = 보이는 GPU 수
  case "$1" in ''|*[!0-9]*) return 1;; esac
  case "$2" in ''|*[!0-9]*) return 1;; esac
  [ "$1" -ge 1 ] && [ "$1" -le "$2" ]
}
# ── pseudo_dir 교체 (실행 폴더 복사본에서만) ───────────────────────────────
_sub_pseudo() {  # $1 = pw.in · $2 = 새 경로
  sed -i -E "s#^( *pseudo_dir *= *)'[^']*'#\1'$2'#" "$1"
}

# ── ⑥ 허용 목록 밖 GPU 프로세스 ─────────────────────────────────────────
_unexpected() {  # $1 = 지금 GPU PID 들 · $2 = 허용 PID 들 → 허용 밖 PID 를 한 줄씩
  local p q ok
  for p in $1; do ok=0; for q in $2; do [ "$p" = "$q" ] && ok=1; done; [ "$ok" = 1 ] || echo "$p"; done
}

# ── ⑩ 우리 프로세스 트리 · 우리 pw.x (2026-09-24 V100 실측으로 고침) ─────────────────
#   종전: `PW=$(pgrep -P $MP | head -1)` — **첫 자식**을 pw.x 로 믿었다. hpcx 의 mpirun 은 래퍼라
#   트리가 래퍼($MP) → [곧 사라지는 보조 · mpirun] → pw.x 로 한 단 더 깊다. V100 실측: 기록된
#   pw.x PID 563677 은 **없었고** 실제 pw.x 563705 는 mpirun 563691 의 자식이었다.
#   그 결과 ① 자기 VRAM 칸이 세 잡 모두 거짓 0 ② `_stop` 이 죽은 PID(재사용되면 **남의 프로세스**)와
#   래퍼만 TERM — 래퍼(bash)만 죽으면 mpirun·pw.x 는 고아로 계속 돈다. 가드가 조용히 무력했다.
#   ⇒ pw.x 는 **comm 이 pw.x 인 자손**으로 찾고, 멈출 때는 **트리 통째로** PID+comm 대조로 멈춘다.
_descendants() {  # $1 = 뿌리 PID → 자손 PID 한 줄씩 (넓이 우선 · 최대 6 단)
  local q="$1" next p k d=0
  while [ -n "${q// /}" ] && [ "$d" -lt 6 ]; do
    next=""
    for p in $q; do for k in $(pgrep -P "$p" 2>/dev/null); do echo "$k"; next="$next $k"; done; done
    q="$next"; d=$((d+1))
  done
}
_find_pw() {  # $1 = 뿌리 PID → comm 이 pw.x 인 첫 자손 (없으면 빈 줄 · rc 1 — 아무 PID 나 채우지 않는다)
  local k
  for k in $(_descendants "$1"); do
    [ "$(cat /proc/$k/comm 2>/dev/null)" = pw.x ] && { echo "$k"; return 0; }
  done
  return 1
}
_alive_as() {  # $1 = PID · $2 = comm → 0 = 살아 있고(좀비 아님) comm 이 그대로다 (PID 재사용 방지)
  [ "$(cat /proc/$1/comm 2>/dev/null)" = "$2" ] || return 1
  [ "$(sed 's/.*) //' /proc/$1/stat 2>/dev/null | cut -d' ' -f1)" != Z ]
}
_stop_tree() {  # $1 = 뿌리 PID → 트리(자손+뿌리) TERM → ≤ 15 초 → comm 이 그대로인 것만 KILL · 멈춘 목록을 stdout
  local pairs="" p c x alive
  for p in $(_descendants "$1") "$1"; do c=$(cat /proc/$p/comm 2>/dev/null) && pairs="$pairs $p:$c"; done
  for x in $pairs; do kill -TERM "${x%%:*}" 2>/dev/null; done
  for _ in $(seq 15); do
    alive=0; for x in $pairs; do _alive_as "${x%%:*}" "${x#*:}" && alive=1; done
    [ "$alive" = 0 ] && break; sleep 1
  done
  for x in $pairs; do _alive_as "${x%%:*}" "${x#*:}" && kill -KILL "${x%%:*}" 2>/dev/null; done
  echo "${pairs# }"
}
# 자기 VRAM 칸: 한 번도 못 쟀으면 0 이 아니라 '—'. 컨테이너 안에서는 nvidia-smi 가 **호스트 PID** 를 준다
#   (V100 실측: pw.x 563705 ↔ 목록 3312066) — 이름공간이 다르면 PID 로는 원리적으로 못 잰다.
_self_field() {  # $1 = 잰 적 있음(0/1) · $2 = 피크 → 칸 값
  if [ "$1" = 1 ]; then echo "$2"; else echo "—"; fi
}

# ── ⑨ PP 내용 해시 (jobs.json settings.pp_sha256 — 없으면 경고만) ──────────────────
#   이름이 같아도 내용이 다른 PP 가 있다 (P rrkjus v6.3 ≠ v5.1). 기계를 옮기면 **내용**으로 대조한다.
_pp_want() {  # $1 = jobs.json · $2 = PP 파일명 → 기준 sha256 (없으면 빈 줄)
  python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('settings',{}).get('pp_sha256',{}).get(sys.argv[2],''))" "$1" "$2" 2>/dev/null
}
_pp_ok() {    # $1 = PP 파일 경로 · $2 = 기준 sha256 → 0 = 같음
  [ -f "$1" ] && [ -n "$2" ] && [ "$(sha256sum "$1" | cut -d' ' -f1)" = "$2" ]
}

# ── ⑪ kind ↔ calc 일치 (2026-09-27) — 완료 판정(_done)은 jobs.json 의 **calc** 로 간다 (kind 가 아니다) ──
#   A′ V4 GPU 시험 패키지를 kind=probe · calc=scf 로 만들었다가 발사 전에 발견: electron_maxstep 2 로 자른 SCF 가
#   scf 규칙(수렴 요구)으로 판정돼 '미완료' → 첫 시험 뒤 러너가 끝나 두 번째 시험이 안 돈다 (조용히 틀린 경로).
#   반대(calc=probe · kind≠probe)는 더 나쁘다 — 진짜 SCF 가 잘려도 완료로 받는다. 그래서 양쪽 다 거부한다.
_kind_calc_ok() {  # $1 = jobs.json · $2 = 잡 dir → 0 = 일치 · 1 = 불일치 또는 잡 없음
  python3 - "$1" "$2" 2>/dev/null <<'PY'
import json, sys
j = next((x for x in json.load(open(sys.argv[1]))["jobs"] if x.get("dir") == sys.argv[2]), None)
sys.exit(1 if j is None else (0 if (j.get("kind") == "probe") == (j.get("calc") == "probe") else 1))
PY
}

# ── ⑧ 공존 예외의 근거 결정 상태 ───────────────────────────────────────
_exception_state() {  # $1 = 결정 ID · $2 = decisions.json → 상태 한 단어 (없는 ID = missing · 못 읽음 = unreadable)
  python3 - "$1" "$2" 2>/dev/null <<'PY' || echo unreadable
import json, sys
try:
    ds = json.load(open(sys.argv[2], encoding="utf-8"))["decisions"]
except Exception:
    print("unreadable"); sys.exit(0)
print(next((d.get("decision_state") or d.get("status") or "unknown" for d in ds if d.get("id") == sys.argv[1]), "missing"))
PY
}
_coexist_gate() {  # $1 = EXCEPTION_ID · $2 = decisions.json → 0 = 결정 active · 1 = 거부 · 2 = 결정 ID 아님(경고만)
  case "$1" in
    D-*) [ "$(_exception_state "$1" "$2")" = active ];;
    *)   return 2;;
  esac
}

if [ "$IN" = "--selftest" ]; then
  T=$(mktemp -d); n=0; f=0
  ck() { if eval "$2"; then n=$((n+1)); else f=$((f+1)); echo "  ✗ $1"; fi; }
  printf "convergence has been achieved\nJOB DONE\n" > "$T/s.out"
  ck "scf 완료"                         "_done $T/s.out scf"
  ck "⛔scf 완료를 relax 로 보면 미완료"   "! _done $T/s.out relax"
  printf "convergence has been achieved\nbfgs converged\nEnd final coordinates\nJOB DONE\n" > "$T/r.out"
  ck "relax 완료"                       "_done $T/r.out relax"
  printf "convergence has been achieved\nThe maximum number of steps has been reached.\nEnd final coordinates\nJOB DONE\n" > "$T/m.out"
  ck "⛔nstep 소진 relax → 미완료"        "! _done $T/m.out relax"
  printf "JOB DONE\n" > "$T/n.out"
  ck "⛔수렴 줄 없음 → 미완료"            "! _done $T/n.out scf"
  printf "     total energy              =   -1.0 Ry\n     convergence NOT achieved after   3 iterations: stopping\nJOB DONE\n" > "$T/p.out"
  ck "probe: maxstep 에서 멈춤 → 완료"    "_done $T/p.out probe"
  ck "⛔같은 출력을 scf 로 보면 미완료"     "! _done $T/p.out scf"
  ck "⛔probe 인데 iteration 흔적 없음"     "! _done $T/n.out probe"
  printf "     total energy              =   -1.0 Ry\nJOB DONE\n" > "$T/q.out"
  ck "⛔probe · 에너지 줄만 있고 수렴 판정 줄 없음" "! _done $T/q.out probe"
  printf "     convergence NOT achieved after   3 iterations: stopping\nJOB DONE\n" > "$T/e.out"
  ck "⛔probe · 판정 줄만 있고 에너지 줄 없음"     "! _done $T/e.out probe"
  ck "⛔파일 없음 → 미완료"               "! _done $T/없음.out scf"
  # ⛔ Codex BX P0 (2026-09-25) — QE 7.4.1 실패 문구 · 마지막 실행 규칙
  printf "convergence has been achieved\n!    total energy = -2152.35487740 Ry\n     bfgs failed after 200 scf cycles and 199 bfgs steps, convergence not achieved\nEnd final coordinates\nJOB DONE\n" > "$T/f.out"
  ck "⛔bfgs failed + 최종 좌표 + JOB DONE → 미완료 (BX P0 재현)" "! _done $T/f.out relax"
  printf "convergence has been achieved\nEnd final coordinates\nJOB DONE\n" > "$T/g.out"
  ck "⛔최종 좌표만 있고 bfgs converged 없음 → 미완료 (성공을 명시적으로 요구)" "! _done $T/g.out relax"
  printf "     Program PWSCF v.7.4.1 starts\nconvergence has been achieved\nbfgs converged in 20 scf cycles\nEnd final coordinates\nJOB DONE\n     Program PWSCF v.7.4.1 starts\nconvergence has been achieved\n     bfgs failed after 200 scf cycles, convergence not achieved\nEnd final coordinates\nJOB DONE\n" > "$T/h.out"
  ck "⛔앞 실행은 성공 · 마지막 실행은 실패 → 미완료 (마지막 실행만 본다)" "! _done $T/h.out relax"
  printf "     Program PWSCF v.7.4.1 starts\nconvergence has been achieved\n     bfgs failed after 200 scf cycles, convergence not achieved\nEnd final coordinates\nJOB DONE\n     Program PWSCF v.7.4.1 starts\nconvergence has been achieved\nbfgs converged in 20 scf cycles\nEnd final coordinates\nJOB DONE\n" > "$T/i.out"
  ck "앞 실행은 실패 · 마지막 실행은 성공 → 완료" "_done $T/i.out relax"
  printf "     Program PWSCF v.7.4.1 starts\nconvergence has been achieved\n!    total energy = -1.0 Ry\nJOB DONE\n     Program PWSCF v.7.4.1 starts\n     convergence NOT achieved after 200 iterations: stopping\nJOB DONE\n" > "$T/j.out"
  ck "⛔scf: 앞 실행 성공 · 마지막 실행 미수렴 → 미완료" "! _done $T/j.out scf"
  printf "     Program PWSCF v.7.4.1 starts\nconvergence has been achieved\nbfgs converged in 20 scf cycles\nEnd final coordinates\nJOB DONE\n     Program PWSCF v.7.4.1 starts\n     iteration #  3     ecut=    52.00 Ry\n" > "$T/k.out"
  ck "⛔앞 실행 성공 · 마지막 실행은 도중에 죽음(JOB DONE 없음) → 미완료" "! _done $T/k.out relax"
  # ⛔ 2026-09-25 — vc-relax 도 이완이다. 옛 판은 `[ "$2" = relax ]` 로만 갈라 vc-relax 가 SCF 기준으로 통과했다
  #   (A′ 선행 배치에 vc-relax 가 들어가며 발견 · 실제로 통과한 실패 이완은 없다 — 05 는 bfgs converged 확인됨).
  ck "⛔vc-relax: bfgs failed + 최종 좌표 + JOB DONE → 미완료" "! _done $T/f.out vc-relax"
  ck "⛔vc-relax: bfgs converged 없음 → 미완료"               "! _done $T/g.out vc-relax"
  ck "vc-relax: 앞 실패 · 마지막 성공 → 완료"                  "_done $T/i.out vc-relax"
  printf "  vdw_corr = 'grimme-d3'\n  dftd3_version = 4\n  dftd3_threebody = .false.\n" > "$T/a.in"
  ck "D3 + threebody 명시 → 통과"        "_d3_ok $T/a.in"
  printf "  vdw_corr = 'grimme-d3'\n  dftd3_version = 4\n" > "$T/b.in"
  ck "⛔D3 인데 threebody 없음 → 거부"    "! _d3_ok $T/b.in"
  printf "  vdw_corr = 'none'\n" > "$T/c.in"
  ck "분산 끔 → threebody 불요구"         "_d3_ok $T/c.in"
  ck "허용 목록 안 → 밖 없음"             '[ -z "$(_unexpected "10 20" "20 10")" ]'
  ck "⛔새 GPU 프로세스 → 잡힌다"          '[ "$(_unexpected "10 20 30" "10 20")" = 30 ]'
  ck "허용 프로세스가 끝난 것은 막지 않음" '[ -z "$(_unexpected "" "10")" ]'
  ck "⛔허용 목록이 비면 전부 밖"          '[ "$(_unexpected "10" "" | wc -l)" = 1 ]'
  ck "⛔kgy 막힘 문장은 프로세스가 아니다"  '[ -z "$(echo "Process-level GPU information is restricted." | _apps_filter)" ]'
  ck "진짜 프로세스 줄은 남긴다"           '[ "$(printf "3322562, python, 9338\n" | _apps_filter)" = "3322562, python, 9338" ]'
  ck "NP 4 · GPU 4 → 허용"                  '_np_ok 4 4'
  ck "⛔NP 8 · GPU 1 → 거부 (한 GPU 에 랭크 여럿)" '! _np_ok 8 1'
  ck "⛔NP 0 · 빈 값 · 문자 → 거부"          '! _np_ok 0 4 && ! _np_ok "" 4 && ! _np_ok x 4'
  printf "&CONTROL\n  pseudo_dir = '/data/work/pseudo'\n  prefix = 'x'\n/\n" > "$T/ps.in"
  _sub_pseudo "$T/ps.in" /scratch/k/pseudo
  ck "pseudo_dir 교체"                     "grep -q \"pseudo_dir = '/scratch/k/pseudo'\" $T/ps.in"
  ck "⛔교체가 다른 줄을 건드리지 않음"      "grep -q \"prefix = 'x'\" $T/ps.in && [ \$(grep -c /data/work/pseudo $T/ps.in) = 0 ]"
  ck "⛔섞여 오면 숫자 줄만"               '[ "$(printf "No running processes found\n12, pw.x, 900\n" | _apps_filter | wc -l)" = 1 ]'
  printf 'PPDATA\n' > "$T/pp.UPF"; H=$(sha256sum "$T/pp.UPF" | cut -d" " -f1)
  printf '{"settings":{"pp_sha256":{"pp.UPF":"%s"}}}' "$H" > "$T/jobs.json"
  ck "PP 기준 해시 읽기"                     "[ \"\$(_pp_want $T/jobs.json pp.UPF)\" = \"$H\" ]"
  ck "PP 내용이 기준과 같음 → 통과"           "_pp_ok $T/pp.UPF $H"
  printf 'PPDATA-v6.3\n' > "$T/pp2.UPF"
  ck "⛔이름만 같고 내용이 다른 PP → 거부"     "! _pp_ok $T/pp2.UPF $H"
  ck "⛔PP 파일 없음 → 거부"                  "! _pp_ok $T/없음.UPF $H"
  ck "⛔기준 해시가 비면 → 통과시키지 않는다" "! _pp_ok $T/pp.UPF \"\""
  printf '{"jobs":[{"dir":"a","kind":"probe","calc":"probe"},{"dir":"b","kind":"probe","calc":"scf"},{"dir":"c","kind":"scf","calc":"scf"},{"dir":"d","kind":"g3","calc":"probe"},{"dir":"e","calc":"relax"},{"dir":"f","calc":"probe"}]}' > "$T/kc.json"
  ck "kind probe · calc probe → 통과"                      "_kind_calc_ok $T/kc.json a"
  ck "⛔kind probe · calc scf → 거부 (V4 시험 패키지 실수)"   "! _kind_calc_ok $T/kc.json b"
  ck "kind scf · calc scf → 통과"                          "_kind_calc_ok $T/kc.json c"
  ck "⛔calc probe 인데 kind 가 probe 아님 → 거부"           "! _kind_calc_ok $T/kc.json d && ! _kind_calc_ok $T/kc.json f"
  ck "kind 없는 옛 패키지 · calc relax → 통과"              "_kind_calc_ok $T/kc.json e"
  ck "⛔jobs.json 에 없는 잡 → 거부"                        "! _kind_calc_ok $T/kc.json 없음"
  ck "기준 없는 파일명 → 빈 값(경고 갈래)"    "[ -z \"\$(_pp_want $T/jobs.json 다른.UPF)\" ]"
  printf '{"decisions":[{"id":"D-a","decision_state":"active"},{"id":"D-r","decision_state":"retracted"},{"id":"D-s","decision_state":"superseded"}]}' > "$T/dec.json"
  ck "공존 근거 결정이 active → 통과"          "_coexist_gate D-a $T/dec.json"
  ck "⛔철회된 예외로 공존 → 거부"              "! _coexist_gate D-r $T/dec.json"
  ck "⛔대체된 결정으로 공존 → 거부"            "! _coexist_gate D-s $T/dec.json"
  ck "⛔원장에 없는 ID → 거부"                  "! _coexist_gate D-없음 $T/dec.json"
  ck "⛔원장을 못 읽음 → 거부"                  "! _coexist_gate D-a $T/없음.json && [ \"\$(_exception_state D-a $T/없음.json)\" = unreadable ]"
  ck "결정 ID 아닌 근거 → 경고 갈래(2)"          '_coexist_gate "kgy 1저자 승인 문구" '"$T/dec.json"'; [ $? = 2 ]'
  ck "실제 원장: gabia 공존 예외는 철회됨"       "[ \"\$(_exception_state D-2026-09-23-gabia-gpu-exception-sese $HERE/../../db/governance/decisions.json)\" = retracted ]"
  # ── ⑩ 트리: 래퍼 → [곧 사라지는 보조 · mpirun] → pw.x (V100 hpcx 실측 모양) ──
  cp "$(command -v sleep)" "$T/pw.x"; cp "$(command -v sleep)" "$T/helper"
  printf '#!/usr/bin/env bash\n"%s/pw.x" 30\n' "$T" > "$T/mpirun_fake"; chmod +x "$T/mpirun_fake"
  printf '#!/usr/bin/env bash\n"%s/helper" 30 &\n"%s/mpirun_fake"\nwait\n' "$T" "$T" > "$T/wrapper"; chmod +x "$T/wrapper"
  "$T/wrapper" & R0=$!; sleep 0.8
  PWT=$(_find_pw "$R0")
  ck "pw.x 는 comm 으로 찾는다 (두 단 아래)"      '[ -n "$PWT" ] && [ "$(cat /proc/$PWT/comm)" = pw.x ]'
  ck "⛔옛 방식(첫 자식)은 pw.x 가 아닌 보조를 잡는다 — 고친 이유" '[ "$(cat /proc/$(pgrep -P "$R0" | head -1)/comm 2>/dev/null)" != pw.x ]'
  ck "자손 셋 (보조 · mpirun · pw.x)"              '[ "$(_descendants "$R0" | wc -l)" = 3 ]'
  ck "⛔comm 이 다르면 살아 있어도 '그 프로세스' 가 아니다 (PID 재사용)" '_alive_as "$PWT" pw.x && ! _alive_as "$PWT" helper'
  "$T/helper" 30 & R1=$!
  ck "⛔pw.x 없는 트리 → 빈 값 (아무 PID 나 안 채운다)" '! _find_pw "$R1" >/dev/null && [ -z "$(_find_pw "$R1")" ]'
  _stop_tree "$R0" >/dev/null; sleep 0.3
  ck "트리를 멈추면 pw.x 도 멈춘다 (래퍼만 죽이면 고아로 산다)" '! _alive_as "$PWT" pw.x'
  ck "⛔트리 밖(다른 뿌리)은 안 건드린다"          '_alive_as "$R1" helper'
  kill "$R1" 2>/dev/null; wait "$R0" "$R1" 2>/dev/null
  ck "자기 VRAM 을 잰 적 있으면 그 값"             '[ "$(_self_field 1 2048)" = 2048 ]'
  ck "⛔한 번도 못 쟀으면 0 이 아니라 —"            '[ "$(_self_field 0 0)" = "—" ]'
  rm -rf "$T"; echo "run_sese_gpu selftest: $n 통과 · $f 실패"; [ "$f" = 0 ]; exit $?
fi

[ -n "$IN" ] && [ -f "$IN/jobs.json" ] || { echo "⛔ 입력 폴더에 jobs.json 이 없다: '$IN'"; exit 1; }
[ -n "$RUN" ] || { echo "⛔ 실행 폴더를 두 번째 인자로 준다"; exit 1; }
IN=$(cd "$IN" && pwd)
PWX=${PWX:-/data/apps/qe-7.4.1-gpu/bin/pw.x}
START_MAX_MIB=${START_MAX_MIB:-40960}; KILL_MIB=${KILL_MIB:-45056}
SAMPLE_S=${SAMPLE_S:-2}; START_WAIT_S=${START_WAIT_S:-3600}
ALLOW_UMA_COEXIST=${ALLOW_UMA_COEXIST:-0}; DRY_RUN=${DRY_RUN:-0}; WAIT_PIDS=${WAIT_PIDS:-}
HOST_START_MIB=${HOST_START_MIB:-16384}; HOST_KILL_MIB=${HOST_KILL_MIB:-4096}
NP=${NP:-1}; PSEUDO_DIR=${PSEUDO_DIR:-}; NO_LOCK=${NO_LOCK:-0}
ONLY_PIDS=${ONLY_PIDS:-}
# 공존 근거 — 기본은 gabia 예외 결정. 다른 기계에서 쓰면 그 근거를 적어 넘긴다 (예: kgy 1저자 승인 문구)
EXCEPTION_ID=${EXCEPTION_ID:-D-2026-09-23-gabia-gpu-exception-sese}
[ "$KILL_MIB" -gt "$START_MAX_MIB" ] || { echo "⛔ KILL_MIB($KILL_MIB) 는 START_MAX_MIB($START_MAX_MIB) 보다 커야 한다"; exit 1; }
JOBS=${JOBS:-$(python3 -c "import json;print(' '.join(j['dir'] for j in json.load(open('$IN/jobs.json'))['jobs']))")}

mkdir -p "$RUN"; RUN=$(cd "$RUN" && pwd)
if [ "$NO_LOCK" != 1 ]; then
  exec 9>"$RUN/.lock"
  flock -n 9 || { echo "이미 도는 중이다 ($RUN/.lock) — 중복 실행 안 한다 (Lustre 면 flock 미지원일 수 있다 → NO_LOCK=1)"; exit 0; }
fi
LOG=$RUN/runner.log; TSV=$RUN/jobs_run.tsv
ts() { date '+%F %T'; }
say() { echo "[$(ts)] $*" | tee -a "$LOG"; }
# 여러 장이면 **장별 최댓값** — 가드는 한 장의 한도를 지키는 것이다 (첫 장만 보면 나머지가 넘쳐도 모른다)
gpu_used() { nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | tr -d ' ' | sort -n | tail -1; }
gpu_apps_raw() { nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader,nounits 2>&1; }
# ⛔ 2026-09-23 kgy 실측: 프로세스별 정보가 막힌 기계는 목록 대신 문장
#   "Process-level GPU information is restricted." 을 돌려준다 — 비어 오지 않는다.
#   그 문장을 PID 로 읽어 `/proc/$p/cmdline: ambiguous redirect` 가 났고, ONLY_PIDS 를 켰다면
#   단어들을 '허용 밖 프로세스' 로 읽어 영원히 기다렸다. ⇒ 첫 칸이 숫자인 줄만 프로세스다.
gpu_apps() { gpu_apps_raw | _apps_filter; }
self_mib() { gpu_apps | awk -F', *' -v p="$1" '$1==p{print $3}' | head -1; }
host_avail() { awk '/^MemAvailable:/{printf "%d", $2/1024}' /proc/meminfo; }

say "════ run_sese_gpu · IN=$IN · RUN=$RUN · JOBS=[$JOBS]"
say "공존 근거: ${EXCEPTION_ID} · START<${START_MAX_MIB} MiB · KILL>${KILL_MIB} MiB · 표본 ${SAMPLE_S}s · UMA 공존 허용=${ALLOW_UMA_COEXIST} · 허용 PID=[${ONLY_PIDS:-제한 없음}]"
DECISIONS=${DECISIONS:-$HERE/../../db/governance/decisions.json}
if [ "$ALLOW_UMA_COEXIST" = 1 ]; then
  _coexist_gate "$EXCEPTION_ID" "$DECISIONS"; rc=$?
  case $rc in
    0) say "공존 근거 ${EXCEPTION_ID} — 원장에서 active" ;;
    2) say "⚠ 공존 근거가 결정 ID 가 아니다 ('${EXCEPTION_ID}') — 원장으로 확인하지 못한다. 사람이 확인한 근거일 때만 쓴다" ;;
    *) say "⛔ UMA 공존 예외의 근거 ${EXCEPTION_ID} 가 원장에서 '$(_exception_state "$EXCEPTION_ID" "$DECISIONS")' 다 (active 아님) — 시작하지 않는다"
       exit 3 ;;
  esac
fi
if [ "$ALLOW_UMA_COEXIST" = 1 ] && [ -z "$ONLY_PIDS" ]; then
  say "⚠ UMA 공존을 켰는데 ONLY_PIDS 가 비었다 — 공존 조건을 PID 로 걸지 못한다 (새 GPU 잡이 떠도 시작한다)"
fi
command -v nvidia-smi >/dev/null 2>&1 || { say "⛔ nvidia-smi 없음 — GPU 가드를 못 건다. 시작하지 않는다"; exit 2; }

# ── 입력 점검: 해시 고정 · D3 명시 · PP 실재·해시 ────────────────────────────
bad=0
for J in $JOBS; do
  P="$IN/$J/pw.in"
  [ -f "$P" ] || { say "⛔ $P 없음"; bad=1; continue; }
  want=$(python3 -c "import json;print(next((j['pw_in_sha256'] for j in json.load(open('$IN/jobs.json'))['jobs'] if j['dir']=='$J'),''))")
  got=$(sha256sum "$P" | cut -d' ' -f1)
  [ "$want" = "$got" ] || { say "⛔ $J/pw.in 해시가 jobs.json 과 다르다 (입력이 고쳐졌다) — $got"; bad=1; }
  _d3_ok "$P" || { say "⛔ $J: grimme-d3 인데 dftd3_threebody 가 명시되지 않았다 (결정 enforcement)"; bad=1; }
  _kind_calc_ok "$IN/jobs.json" "$J" || { say "⛔ $J: jobs.json 의 kind 와 calc 가 probe 여부에서 갈린다 — 완료 판정은 calc 로 간다 (⑪)"; bad=1; }
  PD=${PSEUDO_DIR:-$(grep -aE "pseudo_dir" "$P" | head -1 | sed -E "s/.*'([^']+)'.*/\1/")}
  for U in $(awk '/ATOMIC_SPECIES/{f=1;next} f&&NF==0{exit} f{print $3}' "$P"); do
    [ -f "$PD/$U" ] || { say "⛔ $J: PP 없음 $PD/$U"; bad=1; }
  done
done
[ "$bad" = 0 ] || { say "⛔ 입력 점검 실패 — 시작하지 않는다"; exit 1; }
PD=${PSEUDO_DIR:-$(grep -aE "pseudo_dir" "$IN/$(echo $JOBS | awk '{print $1}')/pw.in" | head -1 | sed -E "s/.*'([^']+)'.*/\1/")}
NGPU=$(nvidia-smi -L 2>/dev/null | grep -c '^GPU')
_np_ok "$NP" "$NGPU" || { say "⛔ NP=$NP 인데 보이는 GPU 는 $NGPU 장 — 한 GPU 에 랭크 여럿은 안 된다. 시작하지 않는다"; exit 2; }
say "랭크 NP=$NP · GPU $NGPU 장 · pseudo=$PD${PSEUDO_DIR:+ (PSEUDO_DIR 로 교체)}"
for U in $(cat "$IN"/*/pw.in | awk '/ATOMIC_SPECIES/{f=1;next} f&&NF==0{f=0} f{print $3}' | sort -u); do
  W=$(_pp_want "$IN/jobs.json" "$U")
  if [ -z "$W" ]; then
    say "PP $U sha256 $(sha256sum "$PD/$U" | cut -c1-16) · ⚠ 기준 해시 없음 (jobs.json) — 사람이 대조한다"
  elif _pp_ok "$PD/$U" "$W"; then
    say "PP $U sha256 $(sha256sum "$PD/$U" | cut -c1-16) · 기준과 같음 ✓"
  else
    say "⛔ PP $U 내용이 기준과 다르다 — 지금 $(sha256sum "$PD/$U" 2>/dev/null | cut -c1-16) · 기준 ${W:0:16} (이름만 같은 다른 파일일 수 있다)"; bad=1
  fi
done
[ "$bad" = 0 ] || { say "⛔ PP 해시 불일치 — 시작하지 않는다"; exit 1; }
say "디스크 $(df -h "$RUN" | awk 'NR==2{print $4" 남음 ("$5" 사용)"}')"

# ── GPU 위의 다른 프로세스 (UMA 판정) ──────────────────────────────────────
UMA=0
while IFS= read -r L; do
  [ -n "$L" ] || continue
  p=$(echo "$L" | awk -F', *' '{print $1}'); m=$(echo "$L" | awk -F', *' '{print $3}')
  c=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | cut -c1-150)
  case "$(cat /proc/$p/comm 2>/dev/null)" in python*) UMA=1;; esac
  say "GPU 사용 중: PID $p · ${m} MiB · $c"
done <<< "$(gpu_apps)"
if [ "$UMA" = 1 ] && [ "$ALLOW_UMA_COEXIST" != 1 ]; then
  say "⛔ GPU 에 python(UMA)이 있다. 규칙 기본값은 GPU pw.x ↔ UMA 동시 금지다 —"
  say "   예외(${EXCEPTION_ID})로 돌리려면 ALLOW_UMA_COEXIST=1 을 준다."
  exit 3
fi
# ⚠ 프로세스별 GPU 정보가 막힌 기계(kgy 실측)에서는 목록이 비어 나온다 — 그때 UMA 판정과
#   ONLY_PIDS 는 **말없이 무력**하다. 사용량이 있는데 목록이 비면 그 사실을 드러낸다.
if [ -z "$(gpu_apps)" ] && [ "$(gpu_used)" -gt 500 ] 2>/dev/null; then
  say "⚠ GPU 사용량 $(gpu_used) MiB 인데 프로세스 목록이 비었다 — 프로세스별 정보가 막힌 기계다."
  say "   nvidia-smi 원문: $(gpu_apps_raw | head -1 | cut -c1-100)"
  say "   UMA 판정·ONLY_PIDS 가 여기서는 **작동하지 않는다**. 남는 가드는 합계 VRAM·호스트 RAM 뿐이다."
fi
say "GPU 합계 사용량 지금 $(gpu_used) MiB · 호스트 MemAvailable $(host_avail) MiB (시작 문턱 ${HOST_START_MIB} · 중단 ${HOST_KILL_MIB})"

if [ "$DRY_RUN" = 1 ]; then say "DRY_RUN — 점검만 하고 끝낸다"; exit 0; fi

# ── ① 기다릴 PID ─────────────────────────────────────────────────────────
declare -A CMD0
for p in $WAIT_PIDS; do
  if [ -r /proc/$p/cmdline ]; then
    CMD0[$p]=$(tr '\0' ' ' < /proc/$p/cmdline)
    say "대기 대상 PID $p · ${CMD0[$p]:0:150}"
  else
    say "대기 대상 PID $p 는 이미 없다 (끝난 것으로 본다)"
  fi
done
for p in "${!CMD0[@]}"; do
  while kill -0 "$p" 2>/dev/null && [ "$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)" = "${CMD0[$p]}" ]; do
    sleep 60
  done
  say "PID $p 끝남"
done

# ── GPU pw.x 런타임 (ldd 로 바이너리에게 묻는다 — 못 읽으면 시작하지 않는다) ─────
# shellcheck source=/dev/null
source "$HERE/../lib/qe_gpu_runtime.sh"
qe_gpu_require "$PWX" 2>&1 | tee -a "$LOG"
qe_gpu_setup "$PWX" >/dev/null || exit 2
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-1}
# gabia 는 root 계정이다 — OpenMPI 가 root 실행을 가드로 막는다 (CLAUDE.md: --allow-run-as-root 필수)
ROOTFLAG=""; [ "$(id -u)" = 0 ] && ROOTFLAG="--allow-run-as-root"
# 단일 노드는 공유메모리 BTL 만 — 안 정하면 TCP 를 골라 좀비가 된 사고 (run_gap_nscf_gabia.sh 2026-08-31)
MPI_MCA=${MPI_MCA:---mca btl self,vader}

[ -f "$TSV" ] || printf "job\trc\tdone\twall_s\tpeak_total_MiB\tpeak_self_MiB\tkilled\tstart\thost_avail_min_MiB\n" > "$TSV"

for J in $JOBS; do
  CALC=$(python3 -c "import json;print(next(j['calc'] for j in json.load(open('$IN/jobs.json'))['jobs'] if j['dir']=='$J'))")
  D=$RUN/$J; mkdir -p "$D"
  if _done "$D/pw.out" "$CALC"; then say "⏭ $J 이미 완료 — 건너뛴다"; continue; fi
  cp "$IN/$J/pw.in" "$D/pw.in"
  [ -n "$PSEUDO_DIR" ] && _sub_pseudo "$D/pw.in" "$PSEUDO_DIR"

  # ② 시작 문턱
  waited=0
  while :; do
    U=$(gpu_used); H=$(host_avail); X=""
    [ -n "$ONLY_PIDS" ] && X=$(_unexpected "$(gpu_apps | awk -F', *' '{print $1}')" "$ONLY_PIDS" | tr '\n' ' ')
    [ -n "$U" ] && [ "$U" -lt "$START_MAX_MIB" ] && [ "${H:-0}" -ge "$HOST_START_MIB" ] && [ -z "${X// /}" ] && break
    [ "$waited" -ge "$START_WAIT_S" ] && { say "⛔ $J: GPU 합계 ${U} MiB (문턱 ${START_MAX_MIB}) · 호스트 ${H} MiB (문턱 ${HOST_START_MIB}) · 허용 밖 PID [${X}] 가 ${START_WAIT_S}s 지속 — 시작하지 않는다"; exit 4; }
    for x in $X; do say "… 허용 밖 GPU 프로세스 PID $x · $(tr '\0' ' ' < /proc/$x/cmdline 2>/dev/null | cut -c1-120)"; done
    say "… $J: GPU 합계 ${U} MiB · 호스트 여유 ${H} MiB · 허용 밖 [${X}] — 조건 밖, 60초 뒤 다시"
    sleep 60; waited=$((waited+60))
  done
  say "▶ $J ($CALC) 시작 · GPU 합계 ${U} MiB · 호스트 여유 ${H} MiB"
  t0=$(date +%s); start=$(ts)
  # shellcheck disable=SC2086
  ( cd "$D" && exec "$QE_GPU_MPIRUN" $ROOTFLAG $MPI_MCA -np "$NP" "$PWX" -nk 1 -in pw.in > pw.out 2> pw.err ) &
  MP=$!
  PW=""
  for _ in $(seq 60); do PW=$(_find_pw "$MP") && break; kill -0 "$MP" 2>/dev/null || break; sleep 1; done
  say "   래퍼(mpirun) PID $MP · pw.x PID ${PW:-? — 60 초 안에 comm=pw.x 자손을 못 찾음 (자기 VRAM 은 '—')}"
  peak=0; peak_self=0; self_seen=0; nsamp=0; killed=0; hmin=999999
  _stop() {   # 우리 잡만 PID 로 — 이름으로 잡지 않는다 · 래퍼 아래 **트리 통째로** (⑩)
    local what; what=$(_stop_tree "$MP")
    say "⛔ $J: $1 — 우리 트리를 PID·comm 대조로 멈췄다 [${what}]"
    killed=1
  }
  while kill -0 "$MP" 2>/dev/null; do
    U=$(gpu_used); H=$(host_avail); nsamp=$((nsamp+1))
    [ -n "$H" ] && [ "$H" -lt "$hmin" ] && hmin=$H
    if [ -n "$U" ]; then
      [ "$U" -gt "$peak" ] && peak=$U
      if [ -n "$PW" ]; then
        S=$(self_mib "$PW")
        if [ -n "$S" ]; then self_seen=1; [ "$S" -gt "$peak_self" ] && peak_self=$S; fi
      fi
      if [ "$nsamp" = 15 ] && [ "$self_seen" = 0 ]; then
        say "   ⚠ nvidia-smi 목록에 우리 pw.x(${PW:-?}) 가 안 보인다 — 컨테이너 PID 이름공간이 다르거나 프로세스 정보가 막혔다. 자기 VRAM 칸은 '—' 로 적는다 (0 이 아니다)"
      fi
      if [ "$U" -gt "$KILL_MIB" ]; then _stop "GPU 합계 ${U} MiB > ${KILL_MIB}"; break; fi
    fi
    if [ -n "$H" ] && [ "$H" -lt "$HOST_KILL_MIB" ]; then _stop "호스트 MemAvailable ${H} MiB < ${HOST_KILL_MIB}"; break; fi
    sleep "$SAMPLE_S"
  done
  wait "$MP"; rc=$?
  wall=$(( $(date +%s) - t0 ))
  dn=0; _done "$D/pw.out" "$CALC" && dn=1
  PSF=$(_self_field "$self_seen" "$peak_self")
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$J" "$rc" "$dn" "$wall" "$peak" "$PSF" "$killed" "$start" "$hmin" >> "$TSV"
  # 파동함수는 우리 보고량에 안 쓴다 — 디스크만 먹는다 (전하밀도·xml 은 남긴다)
  find "$D/tmp" -name "wfc*.dat" -delete 2>/dev/null; find "$D/tmp" -name "*.wfc*" -delete 2>/dev/null
  say "■ $J rc=$rc 완료=$dn 벽시계 ${wall}s · 피크 합계 ${peak} MiB · 자기 ${PSF} MiB · 호스트 최저 ${hmin} MiB · 중단=$killed"
  if [ "$killed" = 1 ]; then say "⛔ 가드로 멈췄다 — 러너를 끝낸다 (재시작은 사람이 판단)"; exit 5; fi
  if [ "$dn" != 1 ]; then
    say "⛔ $J 미완료 — 뒤 잡을 돌리지 않는다. 확인: tail -30 $D/pw.out ; cat $D/pw.err"
    exit 6
  fi
done
# ⚠ --qe_in 을 같이 적는다 — collect 의 기본 입력은 6층(wad_sese_control_2026_09_23)이라 4층 런에 기본값을 쓰면
#   nat 불일치로 전 잡이 missing 이 된다 (막히긴 하지만 사람이 원인을 한참 찾는다 · 2026-09-24).
say "✅ 전부 완료 — 집계: python3 tools/wad/se_sym_slab.py --collect $RUN --qe_in $IN"
