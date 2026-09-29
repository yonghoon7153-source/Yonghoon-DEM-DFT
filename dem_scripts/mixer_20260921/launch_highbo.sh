#!/usr/bin/env bash
# 고-Bo 확장 `LH` 발사 — **첫 시드 하나 → bin 0 스모크 증서 → 나머지 둘** (2026-09-28, Codex 3차 HBR3-08 · Q5)
#
# 왜: 사전등록 docs/reviews/mixer_highbo_prereg_20260927.md §8 (D-4) 는 `LH_s32452843` 를 먼저 띄우고 첫 완전 바퀴 (bin 0)
#   기술 스모크가 통과한 뒤에만 `LH_s49979687` · `LH_s67867967` 을 띄우기로 했다.  그런데 옛 §2-5 의 `MAXJ=3 run_all.sh` 는
#   미실행 `_s*` 를 전부 돌고 스모크를 읽지 않으므로 LH 덱 셋을 **한꺼번에** 띄운다 (`MAXJ=1` 도 첫 런이 끝나면 다음을 띄울 뿐
#   판정을 기다리지 않는다).  ⇒ run_all.sh 는 이제 LH 를 기본으로 건너뛰고, 이 스크립트만 `ALLOW_LH=1 ONLY=<런>` 으로 **한 개씩**
#   부른다 (pid · 동시 상한 · 완주 판정 · 죽은 런 비재발사는 run_all.sh 그대로).
#
# 사용 (리포 루트에서):
#   ① bash dem_scripts/mixer_20260921/launch_highbo.sh first
#        관문: 덱 비교 (`python3 scripts/mixer_deck_diff.py --runs <OUT> --allow B --expect-deck <기대 LH 덱>` 가 0 으로 끝남 —
#              기대 덱 = 비교기 모듈의 expected_deck('LH', 32452843), 생성기 CLI 와 바이트 동일 · HBR4-06) · LH 세 시드 모두 log.lmp · pid 없음
#        → 슬롯 (전 런 합산 live < MAXJ) → 봉인 <OUT>/LH_s32452843/launch_record.json → LH_s32452843 **하나만** 발사하고 끝난다
#   ② bin 0 (첫 완전 바퀴) 이 끝나면 스모크 증서:
#        python3 scripts/measure_mixing_index.py <OUT>/LH_s32452843 --ref <OUT>/E0_s32452843 --r-container 0.013138 --axis x … --json <smoke.json>
#        (칸 · 규약은 사전등록 §2-3 · §8 그대로 — 이 스크립트는 칸을 정하지 않는다)
#   ③ bash dem_scripts/mixer_20260921/launch_highbo.sh rest <smoke.json>
#        관문: 첫 시드가 ① 로 봉인 · 발사됨 · 증서 (JSON 목록의 첫 원소) `run` = LH_s32452843 · `smoke.complete` = true ·
#        `smoke.tech_smoke` = [] · `smoke.qc_repr.pass` = true (JSON true 만 — 1 · "true" 는 거부) · 증서가 첫 봉인보다 나중 ·
#        코호트 (나머지 둘의 in.mixer · STL · 바이너리 sha256 = 첫 봉인 때) · 덱 비교 재통과 ·
#        ★ 증서 출처 (HBR4-05): 판독 규약 = 등록 (16×16×4 · n_min 20 · x · r 0.013138) · 판독기 sha256 = 지금 리포 · run = 첫 시드 ·
#          덱 = 첫 봉인 때 · 증서가 본 발사 봉인 sha256 = 지금 봉인 · 판독 프레임 · E0 기준 프레임을 **이 폴더에서 다시 해시** (mtime 은 참고)
#        → 하나라도 틀리면 **발사 0** · 0 이 아닌 종료.  통과하면 런마다 슬롯 → 봉인 → 발사 (LH_s49979687 · LH_s67867967)
#   환경변수: OUT (기본 dem_scripts/mixer_20260921/runs) · LMP (기본 lmp_serial) · MAXJ (기본 nproc — **전 런** 합산 상한)
#            DECKDIFF (덱 비교기 경로 — 기본 scripts/mixer_deck_diff.py, python3 로 부른다 · 시험은 대역을 꽂는다)
#
# ★ 봉인 (Codex Q5 — 실행 **직전**): 바이너리 (`command -v $LMP`) · in.mixer · Drum/Front/Back.stl sha256 · 리포 git HEAD (없으면
#   no-git) · 지역 · UTC 시각 · 호스트 · nproc · LMP 경로 · 런 · 시드.  슬롯이 난 **뒤**, 발사 **앞**에 쓴다 (대기 중에는 봉인도 없다).
#   first 봉인에는 세 시드의 덱 · STL 해시 (코호트) 도 적는다 — rest 는 첫 시드가 스모크를 받은 그 코호트인지 대조한다.
# ⛔ 로그 · pid 가 있는 LH 는 다시 띄우지 않고 그 봉인도 덮지 않는다 (재개는 resume_all.sh).  정지는 PID 로만 (pkill -f 금지).
# ⚠ rest 가 기계로 읽는 것은 판독기 증서 (§8 ③ 의 smoke 필드) 뿐이다 — §8 ① 보존 · ② 접촉 계약 · ③ 의 8×8×2 바닥 비 · ④ step/s 는
#   사람이 확인한다 (그 중 하나라도 실패면 rest 를 부르지 않는다 = 전체 확장 HOLD).
#   회귀: test_launcher.sh HL①–⑦ (가짜 실행파일 · 덱 비교기 대역).
#
# ★ SLURM 판 (2026-09-28, 1저자 결정: LH 를 ibb 에서 20 코어 × 3) — `BACKEND=slurm`.  관문 (덱 비교 · first/rest 순서 · 스모크 증서 ·
#   출처 · 코호트) 은 **한 글자도 안 바뀐다**.  바뀌는 것은 발사 한 줄뿐이다:
#     로컬   봉인 → run_all.sh 가 `setsid lmp_serial` (봉인 바로 뒤 exec — 틈이 없다)
#     SLURM  러너 <런>/run_lh.sbatch (ibb 실물 형식: docs/data/pure_se_*_20260927/run_pse_*.sh — `#SBATCH -n NP` ↔
#            `mpirun --oversubscribe --bind-to none -np NP` 짝) → 봉인 (러너 · 시작 대조기 sha256 포함) → 런 폴더에서 `sbatch --parsable` →
#            <런>/jobid.  job 이 **시작하면** 러너가 start_check.py 로 봉인을 다시 대조하고 (바이너리 · 덱 · STL · 실행 중인 러너 자신 ·
#            SLURM_NTASKS · log.lmp 없음) 하나라도 다르면 LIGGGHTS 를 부르지 않는다 (대기열 틈 = Codex Q5 의 "실행 직전" 을 지키는 자리).
#   "아직 안 뜬 런" = log.lmp · pid · **jobid** 가 모두 없음 (대기열에만 있는 job 은 log.lmp 가 아직 없다 — 두 번 제출하지 않는다).
#   동시 실행은 SLURM 대기열이 맡는다 (MAXJ 는 기다리지 않는다 · 봉인의 live_at_seal = 대기열에 있는 우리 job 수).
#   환경변수: NP (기본 20) · LMP (기본 lmp_mpi — 봉인은 `command -v` 의 절대경로) · SB_QOS (cpu-60) · SB_PARTITION (cpu) ·
#            SB_TIME (5-00:00:00) · SB_ENV (conda env, 기본 myenv — 빈 값이면 source/activate 줄 없음) · SB_PATH (러너가 PATH 앞에 붙일 것)
#   예 (ibb, 리포 루트): BACKEND=slurm SB_PATH=/home/yonghoon/LIGGGHTS-PUBLIC/src:/home/yonghoon/.conda/envs/myenv/bin \
#                        bash dem_scripts/mixer_20260921/launch_highbo.sh first
#   회귀: test_launcher.sh HS①–⑦b (가짜 sbatch · squeue · mpirun — 러너를 실제로 돌려 시작 대조를 본다).
#
# ★ `all` — **저자 편차** (2026-09-28 밤, 1저자 *"60 다"* · 세 시드 × 20 코어 동시): 사전등록 §8 (D-4) 의 순서 (첫 시드 → bin 0 스모크
#   → 나머지 둘) 를 **건너뛰고** 세 시드를 한꺼번에 봉인 · 제출한다.  관문 (덱 비교 · 세 시드 모두 안 뜸 · 바이너리 · sbatch) 은 first 그대로,
#   bin 0 스모크 증서 관문만 없다.  ⛔ 그래서 두 가지를 강제한다: ① DEVIATION='<저자 결정 · 날짜>' 가 없으면 발사 0 ② 봉인에
#   `stage: all` · `deviation` (그 문구 · 생략한 관문 · 등록 순서) 을 적는다 — 결과 문장에 병기할 근거가 봉인에 남는다.  SLURM 판 전용.
#   bin 0 스모크 (§8 ①–④) 는 여전히 **사람이 확인**한다 (관문이 아니라 기록) · all 뒤의 rest 는 발사 0 (첫 봉인 stage ≠ first).
#   예 (ibb, 리포 루트): DEVIATION='1저자 결정 2026-09-28 밤 — 세 시드 동시' BACKEND=slurm LMP=<lmp_mpi 절대경로> \
#                        bash dem_scripts/mixer_20260921/launch_highbo.sh all
#   회귀: test_launcher.sh HA①–⑦.
#
# ★★ 강성 축 새 단계 (2026-09-30 · 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md v2.5 · 코드 선행조건 2 단계 piece 1 · 5)
#   dev-e0 · dev-rot · confirm-first · confirm-rest — **SLURM 판 전용** (§8-1 "ibb 같은 바이너리 · 같은 MPI launcher · 같은 rank 수 NP").
#   결정은 scripts/mixer_stage_gate.py (정책 v2 · 등록 코호트 · 폴더 계약 · fresh · 디스크 · 선행 기록 · 증서 · 승인), 발사는 이 파일
#   (러너 → 봉인 (+ SEAL_EXTRA) → sbatch [--hold] / scontrol release).  옛 first · rest · all 은 **한 글자도 안 바뀐다**.
#     dev-e0            "① E0 5 런 (E0_ref ×3 · E0_ref2 · E0_ref@dt/2 · 회전 없음) … NP 프로브 = E0_ref 첫 시드를 NP 5/10/20 으로 1 h 씩
#                       (같은 덱 · 처리량만 · 확인 자료 전용 금지)" (§8-2 ②) — 프로브 폴더 npprobe<NP>_E0_ref_s32452843 는 기준 셀에서 만든다
#     dev-rot <기록>    "② 통과 시에만 LC_ref · LH_ref 회전 2 런 · E0 진단 실패 시 회전 보류" — 기록 = mixer_smoke_blind.py --e0-diag 의
#                       봉인된 E0 진단 PASS 기록 (verify_e0_record) · 봉인 requires 에 그 sha256 → job 시작 직전 start_check 가 다시 대조
#     confirm-first     "확인 18 런을 한 번에 제출 — 첫 holdout 시드 블록 (6 런) 은 즉시 · 나머지 두 시드 블록 (12 런) 은 sbatch --hold
#                       (처음부터 held …)" (§8-2 ④ · first-seed-block(6)) → <OUT>/confirm_manifest.json (18 칸 · job ID · 해시 · held 조회)
#     confirm-rest <증서 폴더>  "… 관문 → 통과면 관문이 scontrol release 를 낸다 … 실제 시작 직전 (러너 시작 스크립트) 에 봉인 · 유효 승인
#                       증서를 다시 대조한다" (§8-2 ⑤ · rest(12)) — 증서 = <폴더>/<첫 seed 6 셀>.json (mixer_smoke_blind.py --contract)
#   ⛔ DEV 단계는 확인 셀 · holdout seed 를 못 띄우고 (정책 = 등록 코호트 정확히 · 덱 = 이름에서 재생성한 등록 덱과 바이트 동일),
#     확인 단계는 DEV 덱을 못 띄운다.  새 단계는 모든 런이 아직 안 떴을 때만 (fresh · 재개 없음) · 시간 한도 = 정책 stages.<단계>.time
#     (SB_TIME 을 주면 거부) · NP = 환경 NP (dev-rot 은 E0 진단 기록의 NP 와 같아야 — 블록 NP 통일).
#   ★ 디스크 (piece 5): preflight 가 덱에서 프레임 수 (E0 385 → 867 (×14) → 1,227 (×28)) · 프레임 바이트 상한을 세어 필요 × 1.10 ≤ df 가용 이 아니면 발사 0.
#   회귀: test_launcher.sh DV① … · CF① … (가짜 sbatch · squeue · scontrol · df).
set -uo pipefail
unset SEAL_EXTRA NP_RUN TIME_RUN                                     # 새 단계 내부 변수 — 밖에서 새어 들어오지 않게
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"
OUT="${OUT:-$HERE/runs}"
BACKEND="${BACKEND:-local}"
#  ★ 발사 정책 (2026-09-29, Codex 6 차 §7-2 · Q8): 허용 stage 는 **파일** launch_policy.json (id · sha256 이 봉인에 남는다) 이 정한다.
#    all 은 기본 정책에 없다 — 옛 DEVIATION 환경변수만 남아 있어도 다시 열리지 않는다.  정책을 바꾸려면 파일을 고쳐 커밋 + 사전등록 §0.
POLICY_FILE="${POLICY_FILE:-$HERE/launch_policy.json}"
STAGEGATE="${STAGEGATE:-$ROOT/scripts/mixer_stage_gate.py}"      # 새 단계 관문 (강성 축)
SB_TIME_USER="${SB_TIME:-}"                                         # 새 단계는 시간 한도를 정책에서 읽는다 — 사람이 준 SB_TIME 이면 거부
case "$BACKEND" in
  local) LMP="${LMP:-lmp_serial}";;
  slurm) LMP="${LMP:-lmp_mpi}"; NP="${NP:-20}"
         SB_QOS="${SB_QOS:-cpu-60}"; SB_PARTITION="${SB_PARTITION:-cpu}"; SB_TIME="${SB_TIME:-5-00:00:00}"
         SB_ENV="${SB_ENV-myenv}"; SB_PATH="${SB_PATH:-}"
         MPIRUN_FLAGS='--oversubscribe --bind-to none'; RUNNER=run_lh.sbatch      # ibb: 둘이 없으면 여러 코어에서 바인딩 오류
         [[ "$NP" =~ ^[1-9][0-9]*$ ]] || { echo "⛔ NP=$NP — 양의 정수여야 한다 (#SBATCH -n ↔ mpirun -np).  발사 0"; exit 2; };;
  *) echo "⛔ BACKEND=$BACKEND — local | slurm.  발사 0"; exit 2;;
esac
MAXJ="${MAXJ:-$(nproc)}"
DECKDIFF="${DECKDIFF:-$ROOT/scripts/mixer_deck_diff.py}"
FIRST=LH_s32452843; REST=(LH_s49979687 LH_s67867967)     # §8 (D-4) 순서 = 생성기 CAMPAIGN_HIGHBO 순서 (첫 시드 = 캠페인 첫 시드)
EXPECT_ARM=LH; EXPECT_SEED=32452843                       # 사전등록 §2-2 — 목표 CED 덱 (seed 는 CED 와 무관 — 등록 명령 그대로)
EXPECT_DECK=""; EXP_DIR=""

usage() {
  cat <<EOF
사용 (리포 루트에서) — 사전등록 §8 (D-4) 순서:
  bash dem_scripts/mixer_20260921/launch_highbo.sh first               # 관문 → 봉인 → $FIRST 하나만
  bash dem_scripts/mixer_20260921/launch_highbo.sh rest <smoke.json>   # bin 0 스모크 증서 · 코호트 · 덱 비교 → 봉인 → ${REST[*]}
  DEVIATION='<저자 결정>' BACKEND=slurm bash dem_scripts/mixer_20260921/launch_highbo.sh all   # ⚠ 저자 편차 — 세 시드 동시 (스모크 관문 생략)
  강성 축 (SLURM 판 전용 · 사전등록 mixer_highbo_stiffness_prereg_20260929 §8-2):
    BACKEND=slurm bash dem_scripts/mixer_20260921/launch_highbo.sh dev-e0                        # E0 5 + NP 프로브 3
    BACKEND=slurm bash dem_scripts/mixer_20260921/launch_highbo.sh dev-rot <E0 진단 PASS 기록>    # LC_ref · LH_ref 2 바퀴
    BACKEND=slurm bash dem_scripts/mixer_20260921/launch_highbo.sh confirm-first                 # 18 제출 (6 즉시 · 12 held)
    BACKEND=slurm bash dem_scripts/mixer_20260921/launch_highbo.sh confirm-rest <증서 폴더>       # 관문 → 승인 12 → scontrol release
  증서 = python3 scripts/measure_mixing_index.py <OUT>/$FIRST --ref <OUT>/E0_s32452843 … --json <smoke.json>
  환경변수: OUT · LMP (기본 lmp_serial) · MAXJ (기본 nproc, 전 런 합산) · DECKDIFF (기본 scripts/mixer_deck_diff.py)
EOF
}

#  run_all.sh 와 같은 정의 — pid 파일 + kill -0 로 **살아 있는 런만**, LH 가 아닌 런까지 전부 센다
#  SLURM 판: 대기열 (squeue) 에 있는 우리 job (<런>/jobid) 만 센다 — 대기 · 실행 둘 다
live() {
  local c=0 f q
  if [ "$BACKEND" = slurm ]; then
    q=$(squeue -h -o %i 2>/dev/null) || q=""
    for f in "$OUT"/*_s*/jobid; do [ -s "$f" ] && grep -qxF "$(cat "$f")" <<<"$q" && c=$((c+1)); done
  else
    for f in "$OUT"/*_s*/pid; do [ -f "$f" ] && kill -0 "$(cat "$f")" 2>/dev/null && c=$((c+1)); done
  fi
  echo $c
}
fresh() { [ ! -e "$OUT/$1/log.lmp" ] && [ ! -e "$OUT/$1/pid" ] && [ ! -e "$OUT/$1/jobid" ]; }   # 한 번도 안 뜬 (제출도 안 된) 런
stamp() { date -u +%Y%m%dT%H%M%S.%NZ; }                                 # 옆으로 옮긴 봉인 이름 — 같은 초에 둘이어도 안 덮게

wait_slot() {  # 전 런 합산 live < MAXJ 가 될 때까지 (run_all.sh 와 같은 30 초 주기) — 봉인은 그 **뒤**
  [ "$BACKEND" = slurm ] && return 0                                  # SLURM 판: 대기열이 동시 실행을 맡는다
  local said=0
  while [ "$(live)" -ge "$MAXJ" ]; do
    [ "$said" = 1 ] || { echo "… 동시 상한 대기 — 살아 있는 런 $(live)/$MAXJ (30 초마다 다시 본다 · 봉인은 슬롯이 난 뒤)"; said=1; }
    sleep 30
  done
}

deckdiff() {  # 관문 — 실행 덱 LC_s* → LH_s* 허용 diff B **+ 목표 CED** (사전등록 §2-2 · Codex HB-03 · 4 차 HBR4-06)
  #  ★ HBR4-06 — 옛 판은 `--runs … --allow B` 만 불렀다 = "어디를 바꿀 수 있나" 만 보고 "얼마로 바꾸기로 했나" 는 안 봤다 (LH 허용
  #    다섯 CED 를 전부 두 배로 한 실제 생성 덱이 3/3 PASS · rc 0).  이제 등록된 기대 덱을 **이 리포의 비교기 모듈**로 만들어
  #    (expected_deck — 생성기 CLI 와 바이트 동일, 비교기 셀프테스트 ㉒) `--expect-deck` 로 넘기고 발사 봉인에 그 sha256 을 적는다.
  if [ -z "$EXPECT_DECK" ]; then
    EXP_DIR=$(mktemp -d) || { echo "⛔ 임시 폴더를 못 만든다 — 발사 0"; return 1; }
    trap 'rm -rf "$EXP_DIR"' EXIT
    python3 - "$ROOT/scripts" "$EXPECT_ARM" "$EXPECT_SEED" > "$EXP_DIR/in.mixer" <<'PY' || { echo "⛔ 기대 덱 생성 실패 — 발사 0"; return 1; }
import sys
sys.path.insert(0, sys.argv[1])
import mixer_deck_diff as dd
sys.stdout.write(dd.expected_deck(sys.argv[2], int(sys.argv[3])))
PY
    EXPECT_DECK="$EXP_DIR/in.mixer"
  fi
  echo "── 관문: 덱 비교 — python3 $DECKDIFF --runs $OUT --allow B --expect-deck <기대 $EXPECT_ARM s$EXPECT_SEED 덱>"
  python3 "$DECKDIFF" --runs "$OUT" --allow B --expect-deck "$EXPECT_DECK"; local rc=$?
  [ "$rc" -eq 0 ] || { echo "⛔ 덱 비교 관문 실패 (종료 코드 $rc) — 발사 0"; return 1; }
}

policy_allows() {  # policy_allows <stage> — 정책 파일이 이 stage 를 허용하는가 (파일 없음 · 모양 아님 · 미허용 = 발사 0)
  python3 - "$POLICY_FILE" "$1" <<'PY'
import json, sys
p, st = sys.argv[1:]
try:
    d = json.load(open(p, encoding='utf-8'))
except (OSError, ValueError) as e:
    sys.exit(f'⛔ 발사 정책 파일을 읽을 수 없다 ({p}: {type(e).__name__}: {e}) — 발사 0')
#  v1 = 옛 (first · rest · all) · v2 (2026-09-30 · 강성 축) = + dev-e0 · dev-rot · confirm-first · confirm-rest (단계 인자는 mixer_stage_gate.py policy 가 따로 본다)
KNOWN = {'mixer_highbo_launch_policy/1': ('first', 'rest', 'all'),
         'mixer_highbo_launch_policy/2': ('first', 'rest', 'all', 'dev-e0', 'dev-rot', 'confirm-first', 'confirm-rest')}
sc = d.get('schema') if isinstance(d, dict) else None
ok = (isinstance(d, dict) and sc in KNOWN and isinstance(d.get('policy_id'), str)
      and d['policy_id'].strip() and isinstance(d.get('allowed_stages'), list) and d['allowed_stages']
      and all(isinstance(x, str) and x in KNOWN[sc] for x in d['allowed_stages']))
if not ok:
    sys.exit(f'⛔ 발사 정책 파일 모양이 아니다 ({p}: schema (v1 · v2) · policy_id · allowed_stages ⊂ 그 판의 단계) — 발사 0')
if st not in d['allowed_stages']:
    sys.exit(f"⛔ 발사 정책 {d['policy_id']} 은 stage '{st}' 를 허용하지 않는다 (허용: {d['allowed_stages']}) — 정책을 바꾸려면 "
             f"{p} 를 고쳐 커밋하고 사전등록 §0 에 적는다 (봉인에 id · sha256 이 남는다).  발사 0")
print(f"   발사 정책 {d['policy_id']} — stage '{st}' 허용 ({p})")
PY
}

seal() {  # seal <런> <first|rest> [증서] — 발사 직전 봉인 <OUT>/<런>/launch_record.json (임시 파일 → rename)
  local nm="$1" stage="$2" cert="${3:-}" d="$OUT/$1" lp head
  lp=$(command -v "$LMP") || { echo "⛔ $LMP 없음 — LMP=<실행파일>"; return 1; }
  head=$(git -C "$ROOT" rev-parse HEAD 2>/dev/null) || head=no-git
  #  fresh 인데 봉인이 있다 = 발사되지 않은 옛 봉인 — 지우지 않고 옆으로
  if [ -e "$d/launch_record.json" ]; then mv "$d/launch_record.json" "$d/launch_record.unlaunched.$(stamp).json" || return 1; fi
  SEAL_BACKEND="$BACKEND" SEAL_NP="${NP_RUN:-${NP:-}}" SEAL_FLAGS="${MPIRUN_FLAGS:-}" SEAL_RUNNER="${RUNNER:-}" SEAL_QOS="${SB_QOS:-}" \
  SEAL_PARTITION="${SB_PARTITION:-}" SEAL_TIME="${TIME_RUN:-${SB_TIME:-}}" SEAL_ENV="${SB_ENV:-}" SEAL_PATH="${SB_PATH:-}" SEAL_CHECK="$HERE/start_check.py" \
  SEAL_DEVIATION="${DEVIATION:-}" SEAL_POLICY="$POLICY_FILE" SEAL_EXTRA="${SEAL_EXTRA:-}" \
  python3 - "$d" "$stage" "$LMP" "$lp" "$head" "$(nproc)" "$MAXJ" "$(live)" "$DECKDIFF" "$OUT" "$EXPECT_DECK" "$EXPECT_ARM" \
      "$EXPECT_SEED" "$cert" "$FIRST" "${REST[@]}" <<'PY'
import hashlib, json, os, platform, socket, sys, time
from datetime import datetime, timezone
d, stage, lmp, lmp_path, head, nproc, maxj, live, dd, out, exp, earm, eseed, cert, first, *rest = sys.argv[1:]
FILES = ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


nm, now = os.path.basename(d), time.time()
rec = {
    'schema': 'mixer_highbo_launch_record/1',
    'run': nm, 'seed': int(nm.rsplit('_s', 1)[1]), 'stage': stage,
    'time_local': datetime.fromtimestamp(now).astimezone().isoformat(timespec='seconds'),
    'time_utc': datetime.fromtimestamp(now, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'hostname': socket.gethostname(), 'platform': platform.platform(),
    'nproc': int(nproc), 'maxj': int(maxj), 'live_at_seal': int(live),
    'lmp': lmp, 'lmp_path': lmp_path, 'lmp_realpath': os.path.realpath(lmp_path), 'lmp_sha256': sha(lmp_path),
    'sha256': {f: sha(os.path.join(d, f)) for f in FILES},
    'git_head': head,
}
#  ★ 새 단계 (2026-09-30 · 강성 축) — 덱 관문 = 등록 코호트 (mixer_deck_diff --cohort) · 단계 필드는 mixer_stage_gate.py seal-extra 가 준다.
#    옛 단계 (SEAL_EXTRA 없음) 는 그대로 — 기대 LH 덱 한 벌 (--expect-deck).
extra = os.environ.get('SEAL_EXTRA', '')
if extra:
    ex = json.loads(extra)
    core = set(rec) | {'backend', 'policy', 'slurm', 'cohort', 'deviation', 'smoke_certificate'}
    if not isinstance(ex, dict) or not ex or set(ex) & core:
        sys.exit(f'⛔ SEAL_EXTRA 가 비었거나 핵심 필드와 겹친다 ({sorted(set(ex) & core) if isinstance(ex, dict) else type(ex).__name__}) — 봉인하지 않는다')
else:
    ex = {}
    rec['gate_deckdiff'] = {'script': os.path.realpath(dd), 'script_sha256': sha(dd), 'argv': ['--runs', out, '--allow', 'B', '--expect-deck', exp],
                            'expect_deck_sha256': sha(exp), 'expect_deck_source': f'mixer_deck_diff.expected_deck({earm!r}, {int(eseed)})', 'rc': 0}
rec['backend'] = os.environ.get('SEAL_BACKEND', 'local')
pf = os.environ['SEAL_POLICY']          # ★ 발사 정책 (Codex 6 차 §7-2) — 봉인이 id · sha256 · 허용 stage 를 적는다 · 이 stage 가 허용이 아니면 봉인 없음
with open(pf, encoding='utf-8') as f:
    pol = json.load(f)
if stage not in (pol.get('allowed_stages') or []):
    sys.exit(f"⛔ 정책 {pol.get('policy_id')} 이 stage {stage} 를 허용하지 않는다 — 봉인하지 않는다")
rec['policy'] = {'file': os.path.realpath(pf), 'sha256': sha(pf), 'policy_id': pol.get('policy_id'), 'allowed_stages': pol.get('allowed_stages')}
if rec['backend'] == 'slurm':      # SLURM 판 — 러너 · 시작 대조기까지 봉인한다 (job 이 시작할 때 start_check.py 가 다시 대조)
    ev = os.environ
    rec['slurm'] = {'np': int(ev['SEAL_NP']), 'mpirun_flags': ev['SEAL_FLAGS'], 'qos': ev['SEAL_QOS'], 'partition': ev['SEAL_PARTITION'],
                    'time': ev['SEAL_TIME'], 'conda_env': ev['SEAL_ENV'], 'path_prefix': ev['SEAL_PATH'],
                    'runner': ev['SEAL_RUNNER'], 'runner_sha256': sha(os.path.join(d, ev['SEAL_RUNNER'])),
                    'start_check': os.path.realpath(ev['SEAL_CHECK']), 'start_check_sha256': sha(ev['SEAL_CHECK']),
                    'concurrency': 'SLURM 대기열 (MAXJ 는 관문이 아니다 · live_at_seal = 대기열에 있는 우리 job 수)'}
if stage in ('first', 'all'):      # 코호트 — rest 가 '첫 시드가 스모크를 받은 그 덱 · STL' 인지 대조한다 (바이너리는 lmp_sha256)
    rec['cohort'] = {n: {f: sha(os.path.join(out, n, f)) for f in FILES} for n in [first] + rest}
if stage == 'all':                 # ★ 저자 편차 — 생략한 관문과 결정 문구를 봉인에 남긴다 (결과 문장에 병기할 근거)
    dv = os.environ.get('SEAL_DEVIATION', '')
    if not dv.strip():
        sys.exit('⛔ stage all 인데 DEVIATION 이 비었다 — 봉인하지 않는다')
    rec['deviation'] = {'author_decision': dv,
                        'registered_order': '사전등록 §8 (D-4): 첫 시드 → bin 0 스모크 → 나머지 둘',
                        'skipped_gate': 'bin 0 스모크 증서 (§8 ③ — rest 전 관문).  §8 ①–④ 확인은 사람이 기록으로 남긴다',
                        'launched_together': [first] + rest}
elif stage == 'rest':
    rec['smoke_certificate'] = {'path': os.path.realpath(cert), 'sha256': sha(cert)}
rec.update(ex)
tmp = os.path.join(d, '.launch_record.json.tmp')
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(rec, f, ensure_ascii=False, indent=1)
    f.write('\n')
os.replace(tmp, os.path.join(d, 'launch_record.json'))
print(f"🔒 봉인 {nm}/launch_record.json — {rec['time_local']} · lmp {rec['lmp_sha256'][:12]}… · "
      f"in.mixer {rec['sha256']['in.mixer'][:12]}… · git {head[:12]} · {rec['backend']}"
      + (f" -n {rec['slurm']['np']} · 러너 {rec['slurm']['runner_sha256'][:12]}…" if rec['backend'] == 'slurm' else ''))
PY
}

write_runner() {  # write_runner <런> — ibb 실물 형식 러너 · 바이너리는 봉인과 같은 절대경로 · 시작 대조가 mpirun 앞
  #  (새 단계: NP_RUN · TIME_RUN 이 있으면 그 런의 -n · --time — NP 프로브 5/10/20 · 1 h · 정책의 단계 시간)
  local nm="$1" d="$OUT/$1" lp lpr dabs np_r="${NP_RUN:-$NP}" tm_r="${TIME_RUN:-$SB_TIME}"
  lp=$(command -v "$LMP") || return 1
  lpr=$(readlink -f "$lp") || return 1
  dabs=$(cd "$d" && pwd) || return 1
  {
    echo '#!/bin/bash'
    echo "#SBATCH --job-name=$nm"
    echo "#SBATCH --output=logs/output_${nm}_%j.out"
    echo "#SBATCH --qos=$SB_QOS"
    echo "#SBATCH --partition=$SB_PARTITION"
    echo "#SBATCH -n $np_r"
    echo "#SBATCH --time=$tm_r"
    echo "# 고-Bo LH (SLURM 판) — dem_scripts/mixer_20260921/launch_highbo.sh 가 썼다.  고치지 말 것 (봉인 · 시작 대조가 이 파일의 sha256 을 본다)"
    echo
    echo 'SELF=$(readlink -f "$0")      # SLURM 이 제출 때 복사해 둔 이 러너 — 시작 대조가 봉인한 러너와 같은지 본다'
    if [ -n "$SB_ENV" ]; then echo 'source ~/.bashrc'; echo "conda activate $SB_ENV"; fi
    if [ -n "$SB_PATH" ]; then printf 'export PATH=%q:$PATH\n' "$SB_PATH"; fi
    echo
    printf 'cd %q || exit 3\n' "$dabs"
    printf 'python3 %q %q %q "$SELF" || { echo "⛔ 시작 대조 실패 — LIGGGHTS 를 부르지 않는다 (job_start.refused.*.json)"; exit 3; }\n' \
        "$HERE/start_check.py" "$dabs" "$lpr"
    printf 'mpirun %s -np %s %q -in in.mixer > log.lmp 2>&1\n' "$MPIRUN_FLAGS" "$np_r" "$lpr"
  } > "$d/.$RUNNER.tmp" && mv -f "$d/.$RUNNER.tmp" "$d/$RUNNER"
}

submit() {  # submit <런> [held 1] — 런 폴더에서 sbatch (러너의 logs/ 가 제출 폴더 기준) → <런>/jobid
  #  held = `sbatch --hold` — **처음부터 held** (priority 0 · 제출 뒤 hold 는 race — 강성 축 §8-2 ④ · Codex 7 차 §9-1)
  local nm="$1" hold="${2:-0}" d="$OUT/$1" jid args=(--parsable)
  [ "$hold" = 1 ] && args+=(--hold)
  mkdir -p "$d/logs" || return 1
  jid=$(cd "$d" && sbatch "${args[@]}" "$RUNNER") || { echo "⛔ $nm: sbatch 실패"; return 1; }
  jid=${jid%%;*}
  [[ "$jid" =~ ^[0-9]+$ ]] || { echo "⛔ $nm: sbatch 가 job id 를 주지 않았다 ('$jid')"; return 1; }
  echo "$jid" > "$d/jobid" || return 1
  echo "▶ $nm 제출 — job $jid · -n ${NP_RUN:-$NP}$([ "$hold" = 1 ] && echo ' · held (처음부터 --hold)') · 봉인 $d/launch_record.json · 러너 $d/$RUNNER (job 이 시작하면 러너가 봉인을 다시 대조한다)"
}

launch_one() {  # launch_one <런> <first|rest> [증서] — 슬롯 → 봉인 → run_all.sh (ALLOW_LH=1 ONLY=<런>) → pid 확인
  local nm="$1" d="$OUT/$1"
  wait_slot
  if [ "$BACKEND" = slurm ]; then                                    #  SLURM 판 — 러너 → 봉인 → sbatch → jobid
    write_runner "$nm" || { echo "⛔ $nm: 러너를 못 썼다 — 발사 0"; return 1; }
    seal "$@" || { echo "⛔ $nm: 봉인 실패 — 발사 0"; return 1; }
    submit "$nm" && return 0
    mv "$d/launch_record.json" "$d/launch_record.unlaunched.$(stamp).json" 2>/dev/null
    echo "⛔ $nm: 제출되지 않았다 — 봉인은 launch_record.unlaunched.*.json 으로 옮겼다 (대기열에 들어갔다면 시작 대조가 봉인 없음으로 막는다)"
    return 1
  fi
  seal "$@" || { echo "⛔ $nm: 봉인 실패 — 발사 0"; return 1; }
  OUT="$OUT" LMP="$LMP" MAXJ="$MAXJ" FORCE=0 ALLOW_LH=1 ONLY="$nm" bash "$HERE/run_all.sh"
  if [ -s "$d/pid" ]; then echo "▶ $nm 발사 확인 — pid $(cat "$d/pid") · 봉인 $d/launch_record.json"; return 0; fi
  mv "$d/launch_record.json" "$d/launch_record.unlaunched.$(stamp).json" 2>/dev/null
  echo "⛔ $nm: 발사되지 않았다 (위 run_all.sh 출력 확인) — 봉인은 launch_record.unlaunched.*.json 으로 옮겼다"; return 1
}

cmd_first() {
  [ $# -eq 0 ] || { usage; return 2; }
  echo "[LH first] OUT=$OUT · LMP=$LMP · BACKEND=$BACKEND$([ "$BACKEND" = slurm ] && echo " -n $NP" || echo " · MAXJ=$MAXJ (전 런 합산)") — 사전등록 §8 (D-4): $FIRST 하나만"
  local nm bad=0
  command -v "$LMP" >/dev/null || { echo "⛔ $LMP 없음 — LMP=<실행파일>.  발사 0"; return 1; }
  if [ "$BACKEND" = slurm ]; then
    command -v sbatch >/dev/null && command -v squeue >/dev/null || { echo "⛔ BACKEND=slurm 인데 sbatch / squeue 가 없다 — SLURM 기계에서.  발사 0"; return 1; }
  fi
  policy_allows first || return 2                                   #  관문 0 — 발사 정책 (파일)
  for nm in "$FIRST" "${REST[@]}"; do
    [ -f "$OUT/$nm/in.mixer" ] || { echo "⛔ $OUT/$nm/in.mixer 없음 — 먼저 SET=highbo gen_all.sh"; bad=1; }
  done
  [ "$bad" = 0 ] || { echo "⛔ 발사 0"; return 1; }
  deckdiff || return 1                                               #  관문 1
  for nm in "$FIRST" "${REST[@]}"; do                                #  관문 2 — 세 시드 모두 아직 안 떴다
    fresh "$nm" || { echo "⛔ $nm 에 이미 log.lmp / pid / jobid 가 있다 — first 는 LH 세 시드가 모두 아직 안 떴을 (제출도 안 된) 때만 (§8 순서 · 재개는 resume_all.sh).  사람이 판단"; bad=1; }
  done
  [ "$bad" = 0 ] || { echo "⛔ 발사 0"; return 1; }
  launch_one "$FIRST" first || return 1
  echo "다음: bin 0 (첫 완전 바퀴) 이 끝나면 스모크 증서 (measure_mixing_index.py … --json <smoke.json>) → bash $HERE/launch_highbo.sh rest <smoke.json>"
}

cmd_rest() {
  [ $# -eq 1 ] && [ -n "$1" ] || { usage; return 2; }
  local cert="$1" nm lp k=0 todo=()
  echo "[LH rest] OUT=$OUT · LMP=$LMP · BACKEND=$BACKEND$([ "$BACKEND" = slurm ] && echo " -n $NP" || echo " · MAXJ=$MAXJ (전 런 합산)") · 증서 $cert — 사전등록 §8 (D-4): ${REST[*]}"
  if [ "$BACKEND" = slurm ]; then
    command -v sbatch >/dev/null && command -v squeue >/dev/null || { echo "⛔ BACKEND=slurm 인데 sbatch / squeue 가 없다 — SLURM 기계에서.  발사 0"; return 1; }
  fi
  #  관문 0 — 첫 시드가 first 로 봉인 · 발사됐다 (순서)
  if [ ! -s "$OUT/$FIRST/launch_record.json" ] || [ ! -e "$OUT/$FIRST/log.lmp" ]; then
    echo "⛔ 첫 시드 $FIRST 가 'launch_highbo.sh first' 로 봉인 · 발사된 기록 (launch_record.json · log.lmp) 이 없다 — first 먼저.  발사 0"
    return 1
  fi
  lp=$(command -v "$LMP") || { echo "⛔ $LMP 없음 — LMP=<실행파일>.  발사 0"; return 1; }
  policy_allows rest || return 2                                    #  관문 0 — 발사 정책 (파일)
  #  관문 1 — 스모크 증서 · 관문 2 — 코호트 (표준 라이브러리 python3 만)
  python3 - "$cert" "$OUT" "$FIRST" "$lp" "$ROOT" "${REST[@]}" <<'PY' || { echo "⛔ 증서 · 코호트 관문 불합격 — 나머지 둘 발사 0"; return 1; }
import glob, hashlib, json, math, os, re, sys
cert, out, first, lmp_path, root, *rest = sys.argv[1:]
FILES = ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')
bad = 0


def say(ok, msg):
    global bad
    print(('  ✓ ' if ok else '  ✗ ') + msg)
    bad += not ok


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def show(x):
    return json.dumps(x, ensure_ascii=False)


print(f'── 관문: 스모크 증서 (bin 0 · 사전등록 §8 ③ · D-4) — {cert}')
try:
    with open(cert, encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    say(False, f'증서 파일 없음: {cert}')
    sys.exit(1)
except (OSError, UnicodeDecodeError, ValueError) as e:
    say(False, f'증서를 읽을 수 없다 ({type(e).__name__}: {e})')
    sys.exit(1)
e = data[0] if isinstance(data, list) and data else None
if not isinstance(e, dict):
    say(False, '증서 모양 — measure_mixing_index.py --json 의 목록 [{run, smoke, …}] 이 아니다')
    sys.exit(1)
run = e.get('run')
rb = os.path.basename(os.path.normpath(run)) if isinstance(run, str) and run else None
say(rb == first, f'run = {rb} (목록의 첫 원소 · 기대 {first})')
sm = e.get('smoke')
if not isinstance(sm, dict):
    say(False, 'smoke 없음 — 스모크 창 (HBR2-02) 이 없는 판독기 판의 증서')
    sm = {}
c = sm.get('complete')
say(c is True, f'smoke.complete = {show(c)} (true 여야 — bin 0 계획 프레임 전부)')
t = sm.get('tech_smoke')
say(isinstance(t, list) and t == [], f'smoke.tech_smoke = {show(t)} ([] 여야)')
q = sm.get('qc_repr')
qp = q.get('pass') if isinstance(q, dict) else None
say(qp is True, f'smoke.qc_repr.pass = {show(qp)} (true 여야 — bin 0 부피 누락 QC)')
fs = os.path.join(out, first, 'launch_record.json')
try:
    with open(fs, encoding='utf-8') as f:
        fr = json.load(f)
except (OSError, ValueError) as e_:
    say(False, f'첫 시드 봉인을 읽을 수 없다 ({e_})')
    sys.exit(1)
say(fr.get('stage') == 'first' and fr.get('run') == first, f'첫 시드 봉인 = {first} · first 단계')
#  ★ 증서 출처 (2026-09-28, Codex 4 차 HBR4-05) — 옛 관문은 run 을 basename 으로만 · "다른 발사가 아니다" 를 mtime 으로 봤다 ⇒
#    다른 폴더 · 2×2×1 칸의 **실제** 판독 결과를 봉인 뒤에 복사하면 통과했다.  이제 불변 식별자로 잇는다 (mtime 은 참고로만).
print('── 관문: 증서 출처 — 판독 규약 · 판독기 · 덱 · 발사 봉인 · 프레임 (이 폴더에서 다시 해시)')
REG = {'cells': 16, 'x_cells': 4, 'n_min': 20, 'axis': 'x', 'r_container': 0.013138}      # 사전등록 §2-3 · §8 ③
pv = e.get('provenance') if isinstance(e.get('provenance'), dict) else {}
say(pv.get('schema') == 'mixing_provenance/1', f'provenance.schema = {show(pv.get("schema"))} (출처 블록이 없는 판독기의 증서는 받지 않는다)')
say(pv.get('args') == REG, f'판독 규약 {show(pv.get("args"))} = 등록 {show(REG)}')
rdr = os.path.join(root, 'scripts', 'measure_mixing_index.py')
say(os.path.isfile(rdr) and pv.get('tool_sha256') == sha(rdr), f'판독기 sha256 {str(pv.get("tool_sha256"))[:12]}… = 지금 리포의 판독기')
ru = pv.get('run') if isinstance(pv.get('run'), dict) else {}
say(ru.get('name') == first and ru.get('deck_sha256') == (fr.get('sha256') or {}).get('in.mixer'),
    f'출처 run = {show(ru.get("name"))} · 덱 sha256 = 첫 봉인 때')
say(ru.get('launch_record_sha256') == sha(fs), '증서가 본 발사 봉인 sha256 = 지금 첫 시드 봉인 (다른 발사 · 옛 봉인 때의 증서가 아니다)')


def refiles(post, b):
    fl = b.get('files') if isinstance(b, dict) else None
    if not isinstance(fl, list) or not fl:
        return ['프레임 목록 없음']
    bad = []
    for it in fl:
        try:
            st_, name, h = it
            p_ = os.path.join(post, os.path.basename(str(name)))
            if not os.path.isfile(p_) or sha(p_) != h:
                bad.append(f'{st_}:{name}')
        except (TypeError, ValueError):
            bad.append(str(it)[:40])
    try:
        dg = hashlib.sha256(''.join(f'{int(a)}:{b_}:{c}\n' for a, b_, c in sorted(fl, key=lambda t: int(t[0]))).encode()).hexdigest()
    except (TypeError, ValueError):
        dg = None
    if dg != b.get('sha256'):
        bad.append('묶음 sha256')
    return bad


b1 = refiles(os.path.join(out, first, 'post'), ru.get('frames'))
say(not b1, '판독 프레임 = 첫 시드 post/ 의 그 파일 (다시 해시)' + (f' — 어긋남 {b1[:3]}' if b1 else ''))
rf = pv.get('ref') if isinstance(pv.get('ref'), dict) else {}
e0 = 'E0_s' + first.rsplit('_s', 1)[1]
e0d = os.path.join(out, e0, 'in.mixer')
b2 = refiles(os.path.join(out, e0, 'post'), rf.get('frames'))
say(rf.get('name') == e0 and os.path.isfile(e0d) and rf.get('deck_sha256') == sha(e0d) and not b2,
    f'기준 = {e0} · 덱 · 프레임 (다시 해시)' + (f' — 어긋남 {b2[:3]}' if b2 else ''))
#  ★ 스모크 창의 **입력 집합** (2026-09-28, Codex 5 차 HBR5-02) — 위 refiles 는 증서 목록 **안** 파일만 다시 해시한다 ⇒ 증서 뒤 bin 0 에
#    같은 step 의 복제 (copy_400) 를 넣어도 통과했는데, 같은 폴더를 판독기로 재판독하면 24/25 · smoke.complete=false 였다.
#    판독기와 **같은 파일 규칙** (scripts/measure_bed_aspect.py STEP_RE · frames — test_launcher HL④o 가 같음을 본다) 으로 지금 폴더의
#    bin 0 창 [t₀, t₀ + 한 바퀴) 과 E0 t₀ 를 다시 열거해 중복 · 격자 밖 · 결손 · 증서와 다른 파일을 거부한다.  bin 1 이후의 정상 프레임
#    추가는 막지 않는다 (첫 런은 계속 돈다).  바이트가 증서 판독 때와 같으면 스키마 검사도 그때 선 것이다 (판독기 validate_frame).
print('── 관문: 스모크 창 입력 집합 — 지금 폴더를 판독기 파일 규칙으로 다시 열거 (bin 0 · E0 t₀ · HBR5-02)')
STEP_RE = re.compile(r'_(\d+)\.[A-Za-z]+$')


def enum(post):
    got = {}
    for f_ in glob.glob(os.path.join(post, '*')):
        m_ = STEP_RE.search(os.path.basename(f_))
        if m_:
            got.setdefault(int(m_.group(1)), []).append(f_)
    return got


def _int(x):
    return isinstance(x, int) and not isinstance(x, bool)


t0 = e.get('t0_step')
pl = e.get('plan') if isinstance(e.get('plan'), dict) else {}
spr, de_, end_ = pl.get('steps_per_rev'), pl.get('dump_every'), pl.get('steps_total')
okw = (_int(t0) and t0 >= 0 and isinstance(spr, (int, float)) and not isinstance(spr, bool) and math.isfinite(spr) and spr > 0
       and _int(de_) and de_ > 0 and _int(end_) and end_ >= t0)
say(okw, f'증서의 창 정의 — t0_step {show(t0)} · plan.steps_per_rev {show(spr)} · dump_every {show(de_)} · steps_total {show(end_)}')
if okw:
    def in0(s_):
        return s_ >= t0 and math.floor((s_ - t0) / spr + 1e-9) == 0        # 판독기 _bin 과 같은 식
    lat0 = {s_ for s_ in range(t0, end_ + 1, de_) if in0(s_)}
    cur = {s_: ps_ for s_, ps_ in enum(os.path.join(out, first, 'post')).items() if in0(s_)}
    dup = sorted(s_ for s_, ps_ in cur.items() if len(ps_) > 1)
    off = sorted(set(cur) - lat0)
    miss = sorted(lat0 - set(cur))
    say(not dup, f'bin 0 에 같은 step 의 덤프 둘 이상: {dup[:4] if dup else "없음"}')
    say(not off, f'bin 0 격자 밖 프레임 (격자 = t₀ + k·dump_every): {off[:4] if off else "없음"}')
    say(not miss, f'bin 0 결손: {miss[:4] if miss else "없음"} (계획 격자 {len(lat0)} 장)')
    try:
        cf = sorted([int(a_), os.path.basename(str(b_)), str(c_)] for a_, b_, c_ in ((ru.get('frames') or {}).get('files') or [])
                    if in0(int(a_)))
    except (TypeError, ValueError):
        cf = None
    now = sorted([s_, os.path.basename(ps_[0]), sha(ps_[0])] for s_, ps_ in cur.items() if len(ps_) == 1)
    say(cf is not None and bool(now) and cf == now,
        f'bin 0 파일 (step · 이름 · sha256) = 증서가 판독한 그 파일들 ({len(now)} 장 / 증서 {len(cf) if cf is not None else "읽기 실패"})')
rfl = (rf.get('frames') or {}).get('files') or []
try:
    rst0 = int(rfl[0][0]) if len(rfl) == 1 else None
except (TypeError, ValueError, IndexError):
    rst0 = None
e0cur = enum(os.path.join(out, e0, 'post')).get(rst0, []) if rst0 is not None else []
say(rst0 is not None and len(e0cur) == 1 and [rst0, os.path.basename(e0cur[0]), sha(e0cur[0])] == [rst0, os.path.basename(str(rfl[0][1])), str(rfl[0][2])],
    f'E0 기준 t₀ step {rst0} 의 덤프 = 정확히 한 장 · 증서와 같은 파일 (지금 {len(e0cur)} 장)')
print(f'  · (참고) 증서 mtime {"≥" if os.stat(cert).st_mtime_ns >= os.stat(fs).st_mtime_ns else "<"} 첫 시드 봉인 mtime — 판정에 안 쓴다 '
      '(복사 · 재판독이면 mtime 은 새로워진다 · HBR4-05)')
print('── 관문: 코호트 — 첫 시드 봉인 (first) 때의 덱 · STL · 바이너리 그대로인가')
co = fr.get('cohort') if isinstance(fr.get('cohort'), dict) else {}
for n in rest:
    want = co.get(n)
    if not isinstance(want, dict):
        say(False, f'{n}: 첫 봉인에 코호트 기록이 없다 (코호트 불일치)')
        continue
    changed = []
    for f_ in FILES:
        try:
            got = sha(os.path.join(out, n, f_))
        except OSError:
            got = None
        if got is None or got != want.get(f_):
            changed.append(f_)
    say(not changed, f'{n}: ' + ('in.mixer · Drum/Front/Back.stl sha256 = 첫 봉인 때' if not changed
                                 else f'첫 봉인 뒤에 바뀜 · 없음 — {", ".join(changed)} (코호트 불일치)'))
try:
    ls = sha(lmp_path)
except OSError as e_:
    ls = None
    print(f'     ({lmp_path}: {e_})')
say(ls is not None and ls == fr.get('lmp_sha256'),
    f'바이너리 sha256 {str(ls)[:12]}… {"=" if ls == fr.get("lmp_sha256") else "≠"} 첫 시드 {str(fr.get("lmp_sha256"))[:12]}…')
sys.exit(1 if bad else 0)
PY
  deckdiff || return 1                                               #  관문 3 — 덱 비교 (발사 직전 다시)
  for nm in "${REST[@]}"; do
    if fresh "$nm"; then todo+=("$nm")
    else echo "· $nm: 이미 log.lmp / pid / jobid 가 있다 — 건너뜀 (다시 띄우지 않고 봉인도 덮지 않는다 · 재개는 resume_all.sh)"; fi
  done
  for nm in "${todo[@]}"; do launch_one "$nm" rest "$cert" || return 1; k=$((k+1)); done
  echo "rest 끝 — 발사 $k 개 · 건너뜀 $(( ${#REST[@]} - ${#todo[@]} )) 개.  진행: bash $HERE/watch.sh"
}

cmd_all() {  # ★ 저자 편차 (2026-09-28 밤) — 세 시드를 한꺼번에 · bin 0 스모크 관문 생략 · DEVIATION 필수 · SLURM 판 전용
  [ $# -eq 0 ] || { usage; return 2; }
  echo "[LH all] OUT=$OUT · LMP=$LMP · BACKEND=$BACKEND$([ "$BACKEND" = slurm ] && echo " -n $NP") — ⚠ 저자 편차: 사전등록 §8 (D-4) 의 bin 0 스모크 관문 없이 $FIRST ${REST[*]}"
  local nm bad=0 k=0
  if [ -z "$(printf '%s' "${DEVIATION:-}" | tr -d '[:space:]')" ]; then
    echo "⛔ all 은 등록 순서 (§8 D-4: 첫 시드 → bin 0 스모크 → 나머지 둘) 를 건너뛴다 — DEVIATION='<저자 결정 · 날짜>' 를 주어야 한다 (봉인에 그대로 적힌다).  발사 0"
    return 2
  fi
  [ "$BACKEND" = slurm ] || { echo "⛔ all 은 SLURM 판 전용 (1저자 결정: ibb 20 코어 × 3) — BACKEND=slurm.  발사 0"; return 2; }
  policy_allows all || return 2                                     #  ★ 관문 0 — 발사 정책 (파일): 기본 정책에 all 은 없다 (DEVIATION 만으로는 안 열린다)
  command -v "$LMP" >/dev/null || { echo "⛔ $LMP 없음 — LMP=<실행파일>.  발사 0"; return 1; }
  command -v sbatch >/dev/null && command -v squeue >/dev/null || { echo "⛔ BACKEND=slurm 인데 sbatch / squeue 가 없다 — SLURM 기계에서.  발사 0"; return 1; }
  for nm in "$FIRST" "${REST[@]}"; do
    [ -f "$OUT/$nm/in.mixer" ] || { echo "⛔ $OUT/$nm/in.mixer 없음 — 먼저 SET=highbo gen_all.sh"; bad=1; }
  done
  [ "$bad" = 0 ] || { echo "⛔ 발사 0"; return 1; }
  deckdiff || return 1                                               #  관문 1 — first 와 같다
  for nm in "$FIRST" "${REST[@]}"; do                                #  관문 2 — 세 시드 모두 아직 안 떴다
    fresh "$nm" || { echo "⛔ $nm 에 이미 log.lmp / pid / jobid 가 있다 — all 은 세 시드가 모두 아직 안 떴을 때만 (재개는 resume 절차).  사람이 판단"; bad=1; }
  done
  [ "$bad" = 0 ] || { echo "⛔ 발사 0"; return 1; }
  echo "   DEVIATION = $DEVIATION"
  for nm in "$FIRST" "${REST[@]}"; do
    launch_one "$nm" all || { echo "⛔ $nm 에서 멈춤 — 앞서 제출된 $k 개는 대기열에 있다 (squeue 로 확인 · 사람이 판단)"; return 1; }
    k=$((k+1))
  done
  echo "all 끝 — 제출 $k 개 (봉인 stage all · deviation 기록).  ⚠ bin 0 스모크 (§8 ①–④) 는 관문이 아니라 사람이 확인해 기록한다 · rest 는 쓰지 않는다"
}

new_stage_env() {  # new_stage_env <단계> — 새 단계 공통 전제 (SLURM · 바이너리 · sbatch · squeue [· scontrol] · SB_TIME 없음 · 정책 두 층)
  local stage="$1"
  [ "$BACKEND" = slurm ] || { echo "⛔ $stage 는 SLURM 판 전용 (강성 축 §8-1 같은 환경 · 같은 rank 수) — BACKEND=slurm.  발사 0"; return 2; }
  [ -z "$SB_TIME_USER" ] || { echo "⛔ $stage: SB_TIME=$SB_TIME_USER — 새 단계의 시간 한도는 정책 stages.$stage.time 이 정한다 (사람이 주지 않는다).  발사 0"; return 2; }
  command -v "$LMP" >/dev/null || { echo "⛔ $LMP 없음 — LMP=<실행파일>.  발사 0"; return 1; }
  command -v sbatch >/dev/null && command -v squeue >/dev/null || { echo "⛔ BACKEND=slurm 인데 sbatch / squeue 가 없다 — SLURM 기계에서.  발사 0"; return 1; }
  if [ "$stage" = confirm-rest ]; then command -v scontrol >/dev/null || { echo "⛔ scontrol 이 없다 — release 불가.  0"; return 1; }; fi
  policy_allows "$stage" || return 2                                                   #  관문 0a — 정책 파일 모양 · 단계 허용
  python3 "$STAGEGATE" policy "$POLICY_FILE" "$stage" > /dev/null || { echo "⛔ 정책 stages.$stage 인자 불합격 (등록 코호트 · soft 범위 · 시간) — 발사 0"; return 2; }
  mkdir -p "$OUT/.stage_gate" || return 1
}

cmd_stage() {  # cmd_stage <dev-e0|dev-rot|confirm-first> [E0 진단 PASS 기록 (dev-rot)] — 강성 축 새 단계 발사 (SLURM 판 전용)
  local stage="$1" rec="" cohort ts cj pre plan nm np tm hold kind k=0 fail=0
  shift
  case "$stage" in
    dev-rot) [ $# -eq 1 ] && [ -n "$1" ] || { usage; return 2; }; rec="$1";;
    *)       [ $# -eq 0 ] || { usage; return 2; };;
  esac
  case "$stage" in dev-e0) cohort=dev-e0;; dev-rot) cohort=dev-rot;; *) cohort=confirm;; esac
  echo "[$stage] OUT=$OUT · LMP=$LMP · BACKEND=$BACKEND -n ${NP:-?} — 강성 축 (사전등록 mixer_highbo_stiffness_prereg_20260929 §8-2)"
  new_stage_env "$stage" || return $?
  python3 "$STAGEGATE" prepare "$stage" "$OUT" --policy "$POLICY_FILE" || { echo "⛔ 준비 (NP 프로브 폴더) 실패 — 발사 0"; return 1; }
  ts=$(stamp); cj="$OUT/.stage_gate/cohort_${stage}_$ts.json"; pre="$OUT/.stage_gate/preflight_${stage}_$ts.json"
  echo "── 관문 1: 덱 코호트 — python3 $DECKDIFF --runs $OUT --cohort $cohort --json $cj"
  python3 "$DECKDIFF" --runs "$OUT" --cohort "$cohort" --json "$cj" || { echo "⛔ 덱 코호트 관문 실패 — 발사 0"; return 1; }
  echo "── 관문 2: preflight (폴더 계약 · fresh · 디스크 추정${rec:+ · E0 진단 PASS 기록})"
  plan=$(python3 "$STAGEGATE" preflight "$stage" "$OUT" --policy "$POLICY_FILE" --np "$NP" --cohort-json "$cj" --out-json "$pre" \
         ${rec:+--e0-record "$rec"}) || { echo "⛔ preflight 불합격 — 발사 0 (기록 $pre)"; return 1; }
  while IFS=$'\t' read -r nm np tm hold kind; do
    [ -n "$nm" ] || continue
    NP_RUN="$np"; TIME_RUN="$tm"
    if ! write_runner "$nm"; then echo "⛔ $nm: 러너를 못 썼다"; fail=1; break; fi
    if ! SEAL_EXTRA=$(python3 "$STAGEGATE" seal-extra "$OUT" "$nm" --preflight "$pre"); then echo "⛔ $nm: 봉인 필드 실패"; fail=1; break; fi
    if ! seal "$nm" "$stage"; then echo "⛔ $nm: 봉인 실패"; fail=1; break; fi
    if ! submit "$nm" "$hold"; then
      mv "$OUT/$nm/launch_record.json" "$OUT/$nm/launch_record.unlaunched.$(stamp).json" 2>/dev/null
      echo "⛔ $nm: 제출되지 않았다 — 봉인은 launch_record.unlaunched.*.json 으로 옮겼다"; fail=1; break
    fi
    k=$((k+1))
  done <<< "$plan"
  unset NP_RUN TIME_RUN SEAL_EXTRA
  if [ "$stage" = confirm-first ]; then                                                  #  18 칸 manifest — 실패해도 남긴다 (제출 일부 실패의 기록)
    python3 "$STAGEGATE" manifest "$OUT" --preflight "$pre" || fail=1
  fi
  if [ "$fail" != 0 ]; then
    echo "⛔ $stage 멈춤 — 앞서 제출된 $k 개는 대기열에 있다 (squeue 로 확인 · 사람이 판단 · 새 단계는 fresh 만 다시 받는다)"; return 1
  fi
  echo "$stage 끝 — 제출 $k 개 (봉인 stage $stage · preflight $pre)"
  case "$stage" in
    dev-e0) echo "다음: E0 다섯 완주 뒤  python3 scripts/mixer_smoke_blind.py --e0-diag $OUT --record $OUT/dev_e0_diag.json  →  PASS 면  launch_highbo.sh dev-rot $OUT/dev_e0_diag.json";;
    confirm-first) echo "다음: 첫 seed 6 런 bin 0 · E0 완주 뒤  mixer_smoke_blind.py … --contract --cert <폴더>/<런>.json  →  launch_highbo.sh confirm-rest <폴더>";;
  esac
}

cmd_confirm_rest() {  # cmd_confirm_rest <증서 폴더> — 관문 → 승인 증서 12 → scontrol release (사람이 손으로 풀지 않는다)
  [ $# -eq 1 ] && [ -n "$1" ] || { usage; return 2; }
  local certdir="$1" ts cj ids rc
  echo "[confirm-rest] OUT=$OUT · 증서 $certdir — 강성 축 §8-2 ⑤ (첫 seed bin 0 스모크 + E0 둘 → 나머지 두 seed 블록 release)"
  new_stage_env confirm-rest || return $?
  ts=$(stamp); cj="$OUT/.stage_gate/cohort_confirm-rest_$ts.json"
  echo "── 관문 1: 덱 코호트 (confirm) — 봉인 뒤 덱이 그대로인가"
  python3 "$DECKDIFF" --runs "$OUT" --cohort confirm --json "$cj" || { echo "⛔ 덱 코호트 관문 실패 — release 0 (전체 HOLD)"; return 1; }
  echo "── 관문 2: manifest · held 상태 · 증서 6 (arm × E × 검사 관문표) · 승인 증서"
  ids=$(python3 "$STAGEGATE" rest-gate "$OUT" "$certdir" --policy "$POLICY_FILE" --cohort-json "$cj") || { echo "⛔ confirm-rest 관문 불합격 — release 0 (전체 HOLD)"; return 1; }
  if [ -z "$ids" ]; then
    echo "· 풀 held job 이 없다 (앞선 confirm-rest 가 이미 풀었다)"; python3 "$STAGEGATE" release-record "$OUT" --ids "" --rc 0; return $?
  fi
  echo "── scontrol release $(tr ' ' ',' <<< "$ids")"
  scontrol release "$(tr ' ' ',' <<< "$ids")"; rc=$?
  python3 "$STAGEGATE" release-record "$OUT" --ids "$ids" --rc "$rc" || { echo "⛔ release 미완 — 다시 confirm-rest (승인 증서는 같으면 그대로)"; return 1; }
  echo "confirm-rest 끝 — release $(wc -w <<< "$ids") 개 (승인 증서 = <런>/release_approval.json · job 시작 직전 start_check 가 다시 대조)"
}

case "${1:-}" in
  first) shift; cmd_first "$@"; exit $?;;
  all)   shift; cmd_all "$@"; exit $?;;
  rest)  shift; cmd_rest "$@"; exit $?;;
  dev-e0|dev-rot|confirm-first) cmd_stage "$@"; exit $?;;
  confirm-rest) shift; cmd_confirm_rest "$@"; exit $?;;
  *)     usage; exit 2;;
esac
