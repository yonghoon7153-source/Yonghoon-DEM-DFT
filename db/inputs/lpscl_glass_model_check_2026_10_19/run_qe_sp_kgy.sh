#!/usr/bin/env bash
# =============================================================================
# run_qe_sp_kgy.sh — li2s 모델 검증 축소안 (QE 13 잡) · kgy · Nd EOS 러너가 끝나면 바로 시작
#
#   카드: db/properties/lpscl_smallcell_glass_model_check_estimand_2026_10_19.json (9_개정_2026_10_21_단일점_축소)
#   입력: tools/ionic/glass_model_check.py --qe_inputs --mode sp 가 만든 <RUN>/{sp,pulay,kpt}/<잡>/scf.in
#   러너: tools/doping/run_force_check_scf.sh (ldd 런타임 · 완료 판정 · 점마다 VRAM 문턱) 를 폴더마다 한 번
#
#   bash run_qe_sp_kgy.sh <RUN>          # Nd EOS 잠금 대기 → sp (10) → pulay (2) → kpt (1)
#   bash run_qe_sp_kgy.sh --selftest     # 가짜 러너 · 가짜 nvidia-smi 로 순서 · 대기 · 거부 경로
#
#   WAIT_LOCK=/tmp/ndsite_eos.lock   Nd EOS 러너의 flock (그 러너 · 그 자식 pw.x 가 끝나야 풀린다)
#   ND_LOG=$HOME/work/runs/ndo_site_eos_2026_10_16/run.log   잠금이 풀린 뒤 그 마지막 '끝 —' 줄을 기록만 한다
#   MIN_FREE_MIB=20000               VRAM 여유 문턱 (시작 전 · 러너가 점마다 다시 본다)
#   POLL_S=120 · MAX_WAIT_H=96       VRAM 기다림 간격 · 상한 · MAX_TRY=20 (러너가 물러난 뒤 다시 부르는 횟수)
#
# ⛔ 이 스크립트가 못 하는 것
#   · 판독하지 않는다 — 회수 뒤 glass_model_check.py --sp.
#   · Nd EOS 가 '성공으로' 끝났는지 가리지 않는다 — 잠금이 풀리면 그 러너의 마지막 '끝 —' 줄을 기록만 하고 시작한다.
#   · 남의 GPU 잡을 죽이지 않는다 — VRAM 이 모자라면 기다린다 (MAX_WAIT_H 를 넘으면 그 폴더부터 그만둔다).
#   · 실패한 잡을 대체하지 않는다 (카드: Pulay · k 실패 = 문장 단서 · sp 실패 = 그 구조 'QE 없음').
#   · 메모리 견적을 보지 않는다 — 프로브는 묶기 전에 따로 (검사용).
# =============================================================================
set -u
ts() { date '+%m-%d %H:%M:%S'; }
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
RUNNER=${RUNNER:-$REPO/tools/doping/run_force_check_scf.sh}
WAIT_LOCK=${WAIT_LOCK:-/tmp/ndsite_eos.lock}
ND_LOG=${ND_LOG:-$HOME/work/runs/ndo_site_eos_2026_10_16/run.log}
MIN_FREE_MIB=${MIN_FREE_MIB:-20000}
POLL_S=${POLL_S:-120}
MAX_WAIT_H=${MAX_WAIT_H:-96}
MAX_TRY=${MAX_TRY:-20}
CHAIN_LOCK=${CHAIN_LOCK:-/tmp/li2s_qe_sp_chain.lock}
RUN_LOCK=${RUN_LOCK:-/tmp/li2s_qe_sp.lock}

free_mib() { nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null | head -1; }

# 폴더 안 대기 잡 수 — 러너 DRY_RUN 의 '대기' 줄 (완료 판정을 러너 한 곳에 둔다)
pending() { DRY_RUN=1 LOCK="$RUN_LOCK" bash "$RUNNER" "$1" 2>/dev/null | grep -c " 대기$"; }

wait_vram() {
  local t0 f; t0=$(date +%s)
  while :; do
    f=$(free_mib)
    if [ -n "$f" ] && [ "$f" -ge "$MIN_FREE_MIB" ]; then
      echo "[$(ts)] VRAM 여유 ${f} MiB ≥ ${MIN_FREE_MIB} — 시작"; return 0
    fi
    if [ $(( $(date +%s) - t0 )) -ge $(( MAX_WAIT_H * 3600 )) ]; then
      echo "[$(ts)] ⛔ VRAM 여유 ${f:-?} MiB 가 ${MAX_WAIT_H} h 동안 ${MIN_FREE_MIB} 에 못 미쳤다 — 그만둔다"; return 1
    fi
    echo "[$(ts)] VRAM 여유 ${f:-?} MiB < ${MIN_FREE_MIB} — ${POLL_S} 초 뒤 다시 (남의 잡을 죽이지 않는다)"
    sleep "$POLL_S"
  done
}

run_step() {   # $1 = 폴더 · 러너가 VRAM 으로 물러나면 기다렸다 다시 부른다 (끝난 점은 러너가 건너뛴다)
  local d=$1 n try rc
  for try in $(seq 1 "$MAX_TRY"); do
    wait_vram || return 3
    MIN_FREE_MIB="$MIN_FREE_MIB" LOCK="$RUN_LOCK" bash "$RUNNER" "$d"; rc=$?
    n=$(pending "$d")
    if [ "$rc" -ne 0 ]; then echo "[$(ts)] ⚠ $(basename "$d"): 러너 rc $rc (실패한 잡 있음 · 대기 $n) — 대체하지 않고 다음 폴더로"; return 1; fi
    [ "$n" -eq 0 ] && { echo "[$(ts)] ✓ $(basename "$d") 끝"; return 0; }
    echo "[$(ts)] $(basename "$d"): 대기 $n 남음 (러너가 VRAM 으로 물러남) — 다시 ($try/$MAX_TRY)"
  done
  echo "[$(ts)] ⛔ $(basename "$d"): $MAX_TRY 번 불러도 남았다 — 그만둔다"; return 2
}

main() {
  local RUN=$1 st=() s rc
  [ -d "$RUN" ] && [ -f "$RUN/MANIFEST.json" ] || { echo "⛔ $RUN/MANIFEST.json 이 없다 — --qe_inputs --mode sp 출력이 아니다 · 시작하지 않는다"; return 2; }
  grep -q '"mode": "sp"' "$RUN/MANIFEST.json" || { echo "⛔ MANIFEST 가 축소안 (mode sp) 이 아니다 — 시작하지 않는다"; return 2; }
  [ -f "$RUNNER" ] || { echo "⛔ 러너가 없다: $RUNNER"; return 2; }
  exec 8>"$CHAIN_LOCK" || return 2
  flock -n 8 || { echo "[$(ts)] 이미 도는 묶음이 있다 ($CHAIN_LOCK) — 중단"; return 0; }
  echo "[$(ts)] ■ li2s 축소안 묶음 · RUN=$RUN · 러너 $(sha256sum "$RUNNER" | cut -c1-16) · 문턱 ${MIN_FREE_MIB} MiB"
  if [ -e "$WAIT_LOCK" ]; then
    echo "[$(ts)] Nd EOS 잠금 대기 ($WAIT_LOCK) — 그 러너가 끝나야 풀린다"
    flock "$WAIT_LOCK" true
    echo "[$(ts)] Nd EOS 잠금 풀림 · 마지막 끝 줄: $(grep -a '끝 —' "$ND_LOG" 2>/dev/null | tail -1)"
  else
    echo "[$(ts)] ⚠ 잠금 파일이 없다 ($WAIT_LOCK) — VRAM 문턱으로만 기다린다"
  fi
  for s in sp pulay kpt; do
    if [ ! -d "$RUN/$s" ]; then echo "[$(ts)] ⚠ $s 폴더 없음 — 건너뜀"; st+=("$s:없음"); continue; fi
    run_step "$RUN/$s"; rc=$?
    st+=("$s:rc$rc")
    [ "$rc" -eq 3 ] && break
  done
  echo "[$(ts)] ■ 끝 — ${st[*]} · 다음: 회수 → glass_model_check.py --sp --qe_root <회수본>"
}

if [ "${1:-}" = "--selftest" ]; then
  T=$(mktemp -d); okn=0; badn=0
  chk() { if eval "$2"; then okn=$((okn+1)); echo "  ✓ $1"; else badn=$((badn+1)); echo "  ✗ $1"; fi; }
  mkdir -p "$T/bin" "$T/run/sp/A_s1" "$T/run/sp/B_s1" "$T/run/pulay/ecut_hi_A_s3" "$T/run/kpt/k222_A_s3"
  echo '{"mode": "sp"}' > "$T/run/MANIFEST.json"
  for d in "$T"/run/*/*/; do : > "$d/scf.in"; done
  # 가짜 nvidia-smi: 처음엔 늘 넉넉 (① 잠금 시험의 지연이 잠금 때문만이게) — ② 에서 '처음 두 번 모자람' 으로 바꾼다
  printf '#!/usr/bin/env bash\necho 24000\n' > "$T/bin/nvidia-smi"
  # 가짜 러너: DRY_RUN 이면 scf.out 없는 잡을 '대기' 로 · 아니면 잡마다 scf.out 을 만들고 순서를 적는다
  cat > "$T/runner.sh" <<'EOS'
#!/usr/bin/env bash
for i in $(find "$1" -mindepth 2 -maxdepth 2 -name scf.in | sort); do
  d=$(dirname "$i")
  if [ "${DRY_RUN:-0}" = 1 ]; then [ -f "$d/scf.out" ] && echo "  $(basename "$d") 완료(건너뜀)" || echo "  $(basename "$d") 대기"
  else [ -f "$d/scf.out" ] || { echo done > "$d/scf.out"; echo "$(basename "$1")/$(basename "$d")" >> "$(dirname "$1")/order"; }; fi
done
exit 0
EOS
  chmod +x "$T/bin/nvidia-smi" "$T/runner.sh"
  # ① 잠금이 잡혀 있으면 기다린다 — 4 초 잡고 있는 다른 프로세스 (VRAM 은 넉넉 · 지연은 잠금 몫뿐)
  ( flock "$T/nd.lock" sleep 4 ) & sleep 0.5
  t0=$(date +%s)
  out=$(PATH="$T/bin:$PATH" RUNNER="$T/runner.sh" WAIT_LOCK="$T/nd.lock" ND_LOG=/dev/null POLL_S=1 CHAIN_LOCK="$T/c.lock" RUN_LOCK="$T/r.lock" main "$T/run" 2>&1)
  dt=$(( $(date +%s) - t0 ))
  chk "[양성] Nd 잠금이 풀릴 때까지 기다린다 (${dt} 초 ≥ 3)" "[ $dt -ge 3 ] && echo \"\$out\" | grep -q '잠금 풀림'"
  chk "[양성] 순서 sp → pulay → kpt" "[ \"\$(tr '\n' ' ' < $T/run/order)\" = 'sp/A_s1 sp/B_s1 pulay/ecut_hi_A_s3 kpt/k222_A_s3 ' ]"
  chk "[양성] 끝 줄에 폴더별 rc" "echo \"\$out\" | grep -q '■ 끝 — sp:rc0 pulay:rc0 kpt:rc0'"
  # ② VRAM 이 모자라면 기다렸다 시작한다 (처음 두 번 9000 MiB)
  printf '#!/usr/bin/env bash\nn=$(cat %s/cnt 2>/dev/null || echo 0); echo $((n+1)) > %s/cnt\n[ "$n" -lt 2 ] && echo 9000 || echo 24000\n' "$T" "$T" > "$T/bin/nvidia-smi"
  rm -f "$T"/run/*/*/scf.out "$T/run/order"
  outv=$(PATH="$T/bin:$PATH" RUNNER="$T/runner.sh" WAIT_LOCK="$T/none.lock" POLL_S=1 CHAIN_LOCK="$T/cv.lock" RUN_LOCK="$T/rv.lock" main "$T/run" 2>&1)
  chk "[양성] VRAM 모자라면 기다렸다 시작한다" "echo \"\$outv\" | grep -q '9000 MiB < 20000' && [ -s $T/run/order ]"
  rm -f "$T/run/MANIFEST.json"
  out2=$(PATH="$T/bin:$PATH" RUNNER="$T/runner.sh" WAIT_LOCK="$T/nd.lock" CHAIN_LOCK="$T/c2.lock" main "$T/run" 2>&1); rc2=$?
  chk "[음성] MANIFEST 없으면 시작하지 않는다 (rc 2)" "[ $rc2 -eq 2 ]"
  echo '{"mode": "path"}' > "$T/run/MANIFEST.json"
  out3=$(PATH="$T/bin:$PATH" RUNNER="$T/runner.sh" WAIT_LOCK="$T/nd.lock" CHAIN_LOCK="$T/c3.lock" main "$T/run" 2>&1); rc3=$?
  chk "[음성] 원 설계 (mode path) 입력이면 거부 (rc 2)" "[ $rc3 -eq 2 ]"
  echo '{"mode": "sp"}' > "$T/run/MANIFEST.json"
  exec 7>"$T/c4.lock"; flock -n 7
  out4=$(PATH="$T/bin:$PATH" RUNNER="$T/runner.sh" WAIT_LOCK="$T/nd.lock" CHAIN_LOCK="$T/c4.lock" main "$T/run" 2>&1)
  chk "[음성] 같은 묶음이 이미 돌면 중단" "echo \"\$out4\" | grep -q '이미 도는 묶음'"
  exec 7>&-
  echo "1" > "$T/cnt0"; printf '#!/usr/bin/env bash\necho 100\n' > "$T/bin/nvidia-smi"
  rm -f "$T"/run/*/*/scf.out
  out5=$(PATH="$T/bin:$PATH" RUNNER="$T/runner.sh" WAIT_LOCK="$T/none.lock" POLL_S=1 MAX_WAIT_H=0 CHAIN_LOCK="$T/c5.lock" RUN_LOCK="$T/r5.lock" main "$T/run" 2>&1)
  chk "[음성] VRAM 이 상한 시간 안에 안 나면 그만둔다 (잡 0 개 · 남의 잡을 안 죽임)" "echo \"\$out5\" | grep -q '그만둔다' && [ -z \"\$(find $T/run -name scf.out)\" ]"
  chk "[음성] 잠금 파일이 없으면 경고 후 VRAM 문턱으로만" "echo \"\$out5\" | grep -q '잠금 파일이 없다'"
  rm -rf "$T"; echo "selftest: $okn 통과 · $badn 실패"; [ "$badn" = 0 ]; exit $?
fi

[ -n "${1:-}" ] || { echo "usage: $0 <RUN> | --selftest"; exit 2; }
main "$1"
