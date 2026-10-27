#!/usr/bin/env bash
# =============================================================================
# CEI 생성물 띠틈 — kgy 실행기
#   카드 db/properties/cei_product_gap_card_2026_10_27.json · D-2026-10-27-cei-product-gaps (+ 개정 1)
#
#   ① 점검 (DRY_RUN=1 이면 여기서 끝 · 계산 안 함)
#      pw.x · dos.x · projwfc.x · ldd 로 읽은 MPI · PP md5 · 입력 12 · 입력의 pseudo_dir = $R/pseudo
#      · 결정 상태 · 러너/게이트 selftest · tmux 이름
#   ② $R 로 PP · 입력 복사 (이미 있는 상 폴더는 안 덮는다 — 이어 돌리기)
#   ③ tmux ceigap: Nd Q3′ (tmux ndq3p) 가 끝날 때까지 기다림 → 대조 잡 P2O5 → 게이트
#      (extract_gap.py --control_gate · |Δ| ≤ 0.02 eV) → 통과면 11 종 · 실패면 멈춤
#   GPU 는 run_sei_dft.sh 의 SEI_MIN_FREE_MIB 로 모자라면 기다린다 (cascade v7 UMA 옆).
#
# Env: W (worktree · 필수 · 도는 동안 지우지 말 것) · R (/home/kgy/work/runs/cei_gap_1027)
#      PW (/home/kgy/apps/qe-7.4.1-gpu/bin/pw.x) · MIN_FREE_MIB (8000) · DRY_RUN (0)
# ⛔ 못 하는 것: 결과를 판독하지 않는다 (카드 §7 은 회수 뒤) · ndq3p 말고 다른 pw.x 잡은 모른다
#    (VRAM 대기만 한다) · 이미 있는 $R/<상> 이 다른 입력으로 만든 것인지는 run_sei_dft.sh 의
#    입력 지문 검사에 맡긴다.
# =============================================================================
set -uo pipefail
W=${W:?W=<worktree 경로> 가 필요하다}
R=${R:-/home/kgy/work/runs/cei_gap_1027}
PW=${PW:-/home/kgy/apps/qe-7.4.1-gpu/bin/pw.x}
BIN=$(dirname "$PW"); DOSX=${DOSX:-$BIN/dos.x}; PROJ=${PROJ:-$BIN/projwfc.x}
MINF=${MIN_FREE_MIB:-8000}
TMUX_NAME=${TMUX_NAME:-ceigap}
WAIT_FOR=${WAIT_FOR:-ndq3p}
I=$W/db/inputs/cei_product_gap_2026_10_27
CARD=$W/db/properties/cei_product_gap_card_2026_10_27.json
MD5=$W/db/raw/cei_product_gap_2026_10_27/pseudo_md5.txt
CONTROL=(P2O5_mp-aaaaadqi)
# 닫힌 껍질 → TM 절연체 (갭 값) → TM 금속 (DOS 로 확인)
MAIN=(licl_mp-22905 li3po4_mp-13725 Li2SO4_mp-aaaaagtg SO2_mp-aaaabpak SCl_mp-aaaabpoq
      NiP2O6_mp-aaaabchz MnP2O6_mp-aaabevzn
      CoS2_mp-aaaaadbq NiS2_mp-aaaaadju Ni3S4_mp-aaaaabok MnS2_mp-aaacfzcu)
ts(){ date '+%m-%d %H:%M:%S'; }
fail=0; no(){ echo "  ⛔ $*"; fail=1; }; ok(){ echo "  ✓ $*"; }

echo "[$(ts)] ① 점검 — W=$W · R=$R"
[ -x "$PW" ] && ok "pw.x $PW" || no "pw.x 가 없다: $PW"
[ -x "$DOSX" ] && ok "dos.x" || echo "  ⚠ dos.x 없음 ($DOSX) — 05 가 실패한다 (금속 판정은 04 출력의 E_F 상태로 다시 본다)"
[ -x "$PROJ" ] && ok "projwfc.x" || echo "  ⚠ projwfc.x 없음 ($PROJ) — PDOS 만 빠진다"
envline=$(QE_FROM_LDD=1 PW="$PW" bash -c ". '$W/tools/sei/qe_env.sh' _sourced >/dev/null 2>&1; echo \"\${QE_ENV_ERROR:-OK}|\$MPIRUN|\${QE_LDD_MPI:-}\"")
case "$envline" in OK\|*) ok "MPI (ldd) ${envline#OK|}";; *) no "QE 환경: ${envline%%|*}";; esac
if [ -f "$MD5" ]; then
  (cd "$I/pseudo" && md5sum -c --quiet "$MD5") >/dev/null 2>&1 && ok "PP md5 $(wc -l < "$MD5") 개 (gabia 09-19 세트 + GBRV Co·Ni·Mn)" \
    || no "PP md5 불일치 — $I/pseudo"
else no "md5 목록 없음: $MD5"; fi
for t in "${CONTROL[@]}" "${MAIN[@]}"; do [ -f "$I/work/$t/02_scf.in" ] || no "입력 없음: $t"; done
[ "$fail" = 0 ] && ok "입력 $(( ${#CONTROL[@]} + ${#MAIN[@]} )) 상"
pd=$(grep -ah "pseudo_dir" "$I/work/${CONTROL[0]}/02_scf.in" | head -1 | sed "s/.*= *'//; s/'.*//")
[ "$pd" = "$R/pseudo" ] && ok "입력의 pseudo_dir = $R/pseudo" || no "입력의 pseudo_dir ($pd) ≠ $R/pseudo — R 을 바꾸면 입력을 다시 만들어야 한다"
st=$(python3 - "$W/db/governance/decisions.json" <<'PY'
import json, sys
d = {x["id"]: x for x in json.load(open(sys.argv[1]))["decisions"]}
a = d.get("D-2026-10-27-cei-product-gaps", {}).get("decision_state")
b = d.get("D-2026-10-27-cei-product-gaps-amend1", {}).get("decision_state")
print(f"{a}|{b}")
PY
)
case "$st" in
  active\|active) ok "결정 active · 개정 1 active";;
  active\|proposed) echo "  ⚠ 개정 1 은 proposed — **잠정 실행** (사용자 비준 대기 · 결과는 비준 뒤 판독)";;
  *) no "결정 상태 $st — 본 결정이 active 여야 시작한다";;
esac
bash "$W/tools/sei/run_sei_dft.sh" --selftest >/dev/null 2>&1 && ok "run_sei_dft.sh selftest" || no "run_sei_dft.sh selftest 실패"
python3 "$W/tools/sei/extract_gap.py" --selftest >/dev/null 2>&1 && ok "control_gate selftest" || no "extract_gap.py selftest 실패"
if tmux has-session -t "$TMUX_NAME" 2>/dev/null; then no "tmux $TMUX_NAME 가 이미 있다"; fi
tmux has-session -t "$WAIT_FOR" 2>/dev/null && echo "  ⏳ tmux $WAIT_FOR 도는 중 — 끝나면 시작한다" || ok "tmux $WAIT_FOR 없음 — 바로 시작"
command -v nvidia-smi >/dev/null 2>&1 && echo "  GPU $(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader 2>/dev/null | head -1) · 문턱 여유 ${MINF} MiB"
[ "$fail" = 0 ] || { echo "[$(ts)] ⛔ 점검 실패 — 시작하지 않는다"; exit 2; }
[ "${DRY_RUN:-0}" = 1 ] && { echo "[$(ts)] DRY_RUN — 계산은 하지 않았다"; exit 0; }

echo "[$(ts)] ② $R 로 복사"
mkdir -p "$R/pseudo" || exit 2
cp -n "$I/pseudo/"* "$R/pseudo/"
(cd "$R/pseudo" && md5sum -c --quiet "$MD5") >/dev/null 2>&1 || { echo "  ⛔ $R/pseudo md5 불일치 — 손으로 넣은 다른 파일이 있나 본다"; exit 2; }
for t in "${CONTROL[@]}" "${MAIN[@]}"; do
  if [ -d "$R/$t" ]; then echo "  ↺ $t 있음 — 안 덮는다 (이어 돌리기)"; else cp -r "$I/work/$t" "$R/"; fi
done
git -C "$W" rev-parse HEAD > "$R/SOURCE_COMMIT"

cat > "$R/driver.sh" <<EOF
#!/usr/bin/env bash
set -uo pipefail
cd "$R" || exit 2
echo "[\$(date '+%m-%d %H:%M:%S')] 시작 · commit \$(cat SOURCE_COMMIT)"
w=0
while tmux has-session -t "$WAIT_FOR" 2>/dev/null; do
  [ \$w = 0 ] && echo "⏳ $WAIT_FOR 도는 중 — 같은 GPU 에 pw.x 둘을 안 올린다. 기다린다"
  sleep 300; w=\$((w + 300))
  [ \$w -ge 259200 ] && { echo "⛔ $WAIT_FOR 가 72 h 넘게 안 끝난다 — 멈춘다"; exit 4; }
done
export WORK="$R" QE_FROM_LDD=1 PW="$PW" QE="$PW" DOSX="$DOSX" PROJ="$PROJ" SEI_MIN_FREE_MIB="$MINF"
bash "$W/tools/sei/run_sei_dft.sh" ${CONTROL[*]}
python3 "$W/tools/sei/extract_gap.py" --control_gate "$CARD" --work "$R" \\
  || { echo "⛔ 대조 잡 실패 — 11 종을 돌리지 않는다 (control_gate.json)"; exit 3; }
bash "$W/tools/sei/run_sei_dft.sh" ${MAIN[*]}
echo "[\$(date '+%m-%d %H:%M:%S')] 끝"
EOF
chmod +x "$R/driver.sh"
tmux new-session -d -s "$TMUX_NAME" "bash '$R/driver.sh' >> '$R/run.log' 2>&1" \
  && echo "[$(ts)] ③ tmux $TMUX_NAME 시작 → $R/run.log" || { echo "⛔ tmux 시작 실패"; exit 2; }
