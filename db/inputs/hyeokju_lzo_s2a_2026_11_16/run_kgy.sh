#!/usr/bin/env bash
# =============================================================================
# [혁주] 2a — Li₂ZrO₃ 띠틈 · DOS/PDOS — kgy 실행기 (CEI 생성물 띠틈 실행기와 같은 꼴)
#   카드 db/properties/hyeokju_lzo_stage2a_li2zro3_gap_card_2026_11_16.json (+ 개정 1)
#   결정 D-2026-11-16-hyeokju-lzo-stage2a-li2zro3-gap (+ -amend1)
#
#   ① 점검 (DRY_RUN=1 이면 여기서 끝 · 계산 안 함)
#      pw.x · dos.x · projwfc.x · ldd 로 읽은 MPI · PP md5 (Li · O · P = CEI 세트 · Zr = gabia 검사값)
#      · Zr PP 원자 파동함수 · 구조 · 대조 잡 입력 · 결정 상태 · run_sei_dft / extract_gap selftest · tmux 이름
#   ② 입력: 구조를 $R/struct/<TAG>.vasp 로 복사 (같은 바이트) → build_dft_inputs.py 두 번
#      (본 60/480 → $R/main · 컷오프 탐침 90/720 → $R/ecut90) · 대조 잡 P2O5 입력 복사 (pseudo_dir → $R/pseudo)
#   ③ tmux hjgap: 대조 잡 P2O5 → control_gate (|Δ| ≤ 0.02 eV) → 통과면 본 → 탐침
#
# Env: W (worktree · 필수 · 도는 동안 지우지 말 것) · R (/home/kgy/work/runs/hj_s2a_1116)
#      STRUCT · TAG · REGKEY (기본 = Li₂ZrO₃ · 2026-11-17 개정 2 ZrO₂ 를 같은 실행기로 돌리려고 연 자리) ·
#      EXTRA_DECISION (비우면 안 본다 · 주면 그 결정도 active 또는 proposed 여야 시작 · proposed 면 '잠정 실행' 줄)
#      PW (/home/kgy/apps/qe-7.4.1-gpu/bin/pw.x) · PY (uma python · 입력 생성기용 ase) · MIN_FREE_MIB (8000) · DRY_RUN (0)
# ⛔ 못 하는 것: 결과를 판독하지 않는다 (회수 뒤 카드 §2 · 개정 1 규칙) · 다른 pw.x 잡은 모른다 (VRAM 대기만) ·
#    Zr PP 를 받아 오지 않는다 (블록이 gabia 에서 scp) · 이미 있는 $R/<폴더> 를 덮지 않는다 (이어 돌리기).
# =============================================================================
set -uo pipefail
W=${W:?W=<worktree 경로> 가 필요하다}
R=${R:-/home/kgy/work/runs/hj_s2a_1116}
PW=${PW:-/home/kgy/apps/qe-7.4.1-gpu/bin/pw.x}
BIN=$(dirname "$PW"); DOSX=${DOSX:-$BIN/dos.x}; PROJ=${PROJ:-$BIN/projwfc.x}
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
MINF=${MIN_FREE_MIB:-8000}
TMUX_NAME=${TMUX_NAME:-hjgap}
CARD_CEI=$W/db/properties/cei_product_gap_card_2026_10_27.json
MD5_CEI=$W/db/raw/cei_product_gap_2026_10_27/pseudo_md5.txt
PP_CEI=$W/db/inputs/cei_product_gap_2026_10_27/pseudo
CTRL=P2O5_mp-aaaaadqi
CTRL_SRC=$W/db/inputs/cei_product_gap_2026_10_27/work/$CTRL
STRUCT=${STRUCT:-$W/db/structures/hyeokju_Li2ZrO3_mp-aaaaagdw.vasp}
TAG=${TAG:-Li2ZrO3_mp-aaaaagdw}
REGKEY=${REGKEY:-li2zro3}
EXTRA_DECISION=${EXTRA_DECISION:-}
ZR=Zr_pbe_v1.uspp.F.UPF; ZR_MD5=5db81b1e868ab7776c4564c113de050b
PPS=(Li.pbe-sl-kjpaw_psl.1.0.0.UPF O.pbe-n-kjpaw_psl.0.1.UPF P.pbe-n-kjpaw_psl.1.0.0.UPF)
ts(){ date '+%m-%d %H:%M:%S'; }
fail=0; no(){ echo "  ⛔ $*"; fail=1; }; ok(){ echo "  ✓ $*"; }

echo "[$(ts)] ① 점검 — W=$W · R=$R"
[ -x "$PW" ] && ok "pw.x $PW" || no "pw.x 가 없다: $PW"
[ -x "$DOSX" ] && ok "dos.x" || no "dos.x 없음 ($DOSX)"
[ -x "$PROJ" ] && ok "projwfc.x" || echo "  ⚠ projwfc.x 없음 ($PROJ) — PDOS 만 빠진다"
envline=$(QE_FROM_LDD=1 PW="$PW" bash -c ". '$W/tools/sei/qe_env.sh' _sourced >/dev/null 2>&1; echo \"\${QE_ENV_ERROR:-OK}|\$MPIRUN|\${QE_LDD_MPI:-}\"")
case "$envline" in OK\|*) ok "MPI (ldd) ${envline#OK|}";; *) no "QE 환경: ${envline%%|*}";; esac
"$PY" -c "import ase, numpy" 2>/dev/null && ok "PY $PY (ase · numpy)" || no "PY 에 ase/numpy 가 없다: $PY"
for f in "${PPS[@]}"; do
  want=$(grep -a " $f\$" "$MD5_CEI" | cut -d' ' -f1)
  got=$(md5sum < "$PP_CEI/$f" 2>/dev/null | cut -d' ' -f1)
  [ -n "$want" ] && [ "$got" = "$want" ] && ok "$f md5 = CEI 세트" || no "$f md5 불일치 · 없음 ($PP_CEI)"
done
zg=$(md5sum < "$R/pseudo/$ZR" 2>/dev/null | cut -d' ' -f1)
[ "$zg" = "$ZR_MD5" ] && ok "$ZR md5 = gabia 검사값" || no "$R/pseudo/$ZR 가 없거나 md5 ($zg) ≠ $ZR_MD5 — gabia 에서 scp"
grep -aqi "<PP_CHI" "$R/pseudo/$ZR" 2>/dev/null && ok "Zr PP 원자 파동함수 있음 (PDOS)" || echo "  ⚠ Zr PP 에 PP_CHI 가 없다 — Zr PDOS 가 빠질 수 있다"
[ -f "$STRUCT" ] && ok "구조 $(basename "$STRUCT")" || no "구조 없음: $STRUCT"
[ -f "$CTRL_SRC/02_scf.in" ] && ok "대조 잡 입력 $CTRL" || no "대조 잡 입력 없음: $CTRL_SRC"
st=$(python3 - "$W/db/governance/decisions.json" "$EXTRA_DECISION" <<'PY'
import json, sys
d = {x["id"]: x for x in json.load(open(sys.argv[1]))["decisions"]}
a = d.get("D-2026-11-16-hyeokju-lzo-stage2a-li2zro3-gap", {}).get("decision_state")
b = d.get("D-2026-11-16-hyeokju-lzo-stage2a-li2zro3-gap-amend1", {}).get("decision_state")
c = d.get(sys.argv[2], {}).get("decision_state") if sys.argv[2] else "-"
print(f"{a}|{b}|{c}")
PY
)
case "$st" in
  active\|active\|-) ok "결정 active · 개정 1 active";;
  active\|active\|active) ok "결정 active · 개정 1 active · $EXTRA_DECISION active";;
  active\|active\|proposed) echo "  ⚠ $EXTRA_DECISION 은 proposed — **잠정 실행** (사용자 비준 대기 · 결과는 비준 뒤 판독)";;
  active\|proposed\|-) echo "  ⚠ 개정 1 은 proposed — **잠정 실행** (사용자 비준 대기 · 결과는 비준 뒤 판독)";;
  *) no "결정 상태 $st — 본 결정 · 개정 1 이 active 여야 하고, EXTRA_DECISION 을 줬으면 그것도 원장에 있어야 시작한다";;
esac
python3 - "$W/db/properties/sei_electronic_class.json" "$REGKEY" <<'PY' && ok "레지스트리 $REGKEY = insulator" || no "레지스트리에 $REGKEY insulator 가 없다 — 갭 단계가 안 만들어진다"
import json, sys
r = json.load(open(sys.argv[1]))["results"].get(sys.argv[2], {})
sys.exit(0 if r.get("class") == "insulator" else 1)
PY
bash "$W/tools/sei/run_sei_dft.sh" --selftest >/dev/null 2>&1 && ok "run_sei_dft.sh selftest" || no "run_sei_dft.sh selftest 실패"
python3 "$W/tools/sei/extract_gap.py" --selftest >/dev/null 2>&1 && ok "extract_gap.py selftest" || no "extract_gap.py selftest 실패"
tmux has-session -t "$TMUX_NAME" 2>/dev/null && no "tmux $TMUX_NAME 가 이미 있다"
command -v nvidia-smi >/dev/null 2>&1 && echo "  GPU $(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader 2>/dev/null | head -1) · 문턱 여유 ${MINF} MiB"
[ "$fail" = 0 ] || { echo "[$(ts)] ⛔ 점검 실패 — 시작하지 않는다"; exit 2; }
[ "${DRY_RUN:-0}" = 1 ] && { echo "[$(ts)] DRY_RUN — 계산은 하지 않았다"; exit 0; }

echo "[$(ts)] ② 입력"
mkdir -p "$R/pseudo" "$R/struct" "$R/main" "$R/ecut90" || exit 2
for f in "${PPS[@]}"; do cp -n "$PP_CEI/$f" "$R/pseudo/"; done
cp -n "$STRUCT" "$R/struct/$TAG.vasp" && cmp -s "$STRUCT" "$R/struct/$TAG.vasp" || { echo "  ⛔ $R/struct/$TAG.vasp 가 저장소 구조와 다르다"; exit 2; }
for spec in "main|" "ecut90|--ecut_min Zr=90,720"; do
  sub=${spec%%|*}; extra=${spec#*|}
  if [ -d "$R/$sub/$TAG" ]; then echo "  ↺ $sub/$TAG 있음 — 안 덮는다"; continue; fi
  "$PY" "$W/tools/sei/build_dft_inputs.py" --pattern "$R/struct/$TAG.vasp" --pseudo_dir "$R/pseudo" \
        --work "$R/$sub" --hubbard none $extra > "$R/build_$sub.log" 2>&1
  [ -f "$R/$sub/$TAG/03_nscf_gap.in" ] && ok "입력 $sub/$TAG (갭 단계 있음 · $(grep -aoiE 'ecutwfc *= *[0-9.]+' "$R/$sub/$TAG/02_scf.in" | head -1))" \
    || { echo "  ⛔ $sub/$TAG 의 갭 단계 입력이 없다 — $R/build_$sub.log"; tail -5 "$R/build_$sub.log"; exit 2; }
done
if [ -d "$R/main/$CTRL" ]; then echo "  ↺ main/$CTRL 있음 — 안 덮는다"; else
  cp -r "$CTRL_SRC" "$R/main/$CTRL" && sed -i "s#pseudo_dir *= *'[^']*'#pseudo_dir = '$R/pseudo'#" "$R/main/$CTRL"/*.in
  grep -aq "pseudo_dir = '$R/pseudo'" "$R/main/$CTRL/02_scf.in" && ok "대조 잡 입력 · pseudo_dir → $R/pseudo" || { echo "  ⛔ 대조 잡 pseudo_dir 바꾸기 실패"; exit 2; }
fi
git -C "$W" rev-parse HEAD > "$R/SOURCE_COMMIT"

cat > "$R/driver.sh" <<DRV
#!/usr/bin/env bash
set -uo pipefail
cd "$R" || exit 2
echo "[\$(date '+%m-%d %H:%M:%S')] 시작 · commit \$(cat SOURCE_COMMIT)"
export QE_FROM_LDD=1 PW="$PW" QE="$PW" DOSX="$DOSX" PROJ="$PROJ" SEI_MIN_FREE_MIB="$MINF"
WORK="$R/main" bash "$W/tools/sei/run_sei_dft.sh" $CTRL
python3 "$W/tools/sei/extract_gap.py" --control_gate "$CARD_CEI" --work "$R/main" \\
  || { echo "⛔ 대조 잡 실패 — Li2ZrO3 를 돌리지 않는다 (main/control_gate.json)"; exit 3; }
WORK="$R/main" bash "$W/tools/sei/run_sei_dft.sh" $TAG
WORK="$R/ecut90" bash "$W/tools/sei/run_sei_dft.sh" $TAG
echo "[\$(date '+%m-%d %H:%M:%S')] 끝"
DRV
chmod +x "$R/driver.sh"
tmux new-session -d -s "$TMUX_NAME" "bash '$R/driver.sh' >> '$R/run.log' 2>&1" \
  && echo "[$(ts)] ③ tmux $TMUX_NAME 시작 → $R/run.log" || { echo "⛔ tmux 시작 실패"; exit 2; }
