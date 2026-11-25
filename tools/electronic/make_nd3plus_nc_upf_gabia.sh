#!/usr/bin/env bash
# =============================================================================
# make_nd3plus_nc_upf_gabia.sh — 4f 를 core 에 둔 NC Nd (PseudoDojo Nd3+_f-in-core) 를 QE 가 읽는 UPF 로 · gabia (어디서든)
#   Nd Q3 ELF 의 NC 규약 (사용자 10-19 '권고대로 해' · runlog nd_q3_bader_elf_runlog_2026_10_19.json).
#
# 왜 이렇게 하나 (2026-10-19 판 · 첫 판 58dd54f1 은 CMake 를 가정해 gabia 에서 빌드가 멈췄다 — 4.0.1 은 make.inc 빌드다)
#   PseudoDojo (ONCVPSP-PBE-PDv0.4/Nd/Nd3+_f-in-core · ONCVPSP 3.2.3.1 · 가전자 11) 는 psp8 만 배포한다.
#   ONCVPSP 4.0.1 로 같은 입력을 다시 돌리면 **다른 pseudo** 가 나온다 (r_core · ekb 최대 83 % · GHOST(+) 경고) —
#   그래서 배포본 psp8 을 **그대로 UPF 로 옮긴다** (oncv_regen_check.py --to_upf · 4.0.1 upfout.f90 규약 · 보간 없음).
#   변환기 검증 (같은 4.0.1 실행의 psp8·UPF 짝 대조 · QE 대조) 은 2026-10-19 클라우드에서 했고 원자료는
#   db/raw/nd_nc_pp_conversion_2026_10_19/ 에 있다. 저장소의 UPF 는 db/inputs/nd_q3_elf_nc_2026_10_19/pseudo/ 에 있다.
#   ⇒ 이 러너의 기본 일은 **그 UPF 를 이 기계에서 원본부터 다시 만들어 해시가 같은지** 보는 것이다 (몇 초 · 컴파일 없음).
#   REGEN=1 이면 변환기 검증까지 이 기계에서 다시 한다 (ONCVPSP 4.0.1 make 빌드 · 원자 계산 수 초 — QE 계산 아님).
#
# 쓰는 법 (worktree 뿌리에서 · CPU 몇 초 · REGEN=1 이면 빌드 포함 1 분 안팎)
#   bash tools/electronic/make_nd3plus_nc_upf_gabia.sh
#   REGEN=1 bash tools/electronic/make_nd3plus_nc_upf_gabia.sh
#
# 순서: ① PseudoDojo 원본 넷 (.in · .psp8 · .djrepo · .out) 받기 + md5 (djrepo 의 md5 = 474ce0fc…)
#       ② 배포본 psp8 → UPF (--to_upf) · 저장소 UPF 와 sha256 대조
#       ③ (REGEN=1) 도구 (gfortran · make · LAPACK/BLAS) → ONCVPSP 4.0.1 받기 · make.inc (libxc 끔 — iexc 4 = 내장 PBE) · 빌드 ·
#          psfile both 실행 → psp8 · UPF 뽑기 → 재생성 psp8 대 배포본 (기록만 · 다르다고 알려져 있다) →
#          재생성 psp8 을 --to_upf 로 옮겨 같은 실행의 UPF 와 --compare_upf (통과해야 한다)
#       ④ 기록 JSON + SHA256SUMS
# 종료: 0 끝 · 3 원본 받기·md5 실패 · 4 변환 UPF ≠ 저장소 UPF (또는 저장소 UPF 없음) · 5 도구 없음 (REGEN) ·
#       6 ONCVPSP 받기·빌드·실행 실패 (REGEN) · 7 같은 실행 짝 대조 실패 (REGEN — 변환기를 믿을 수 없다)
# ⛔ 못 하는 것: pseudo 의 전이성 검증 (PseudoDojo 기록을 믿는다) · QE 계산 (그건 ELF 러너가 한다) ·
#    psp8 에 없는 PP_PSWFC · rchrg 밖 꼬리 (oncv_regen_check.py docstring — 절대 에너지가 ONCVPSP UPF 와 조금 다르다)
# =============================================================================
set -u; set +H
REPO=$(cd "$(dirname "$0")/../.." && pwd)
P=${P:-/data/work/pseudo_nc_nd3plus_2026_10_19}
PY=${PY:-python3}
RAW=${RAW:-https://raw.githubusercontent.com/PseudoDojo/ONCVPSP-PBE-PDv0.4/master/Nd}
MD5=474ce0fc5175ff9ddf2621f906febf65
REF_UPF=${REF_UPF:-$REPO/db/inputs/nd_q3_elf_nc_2026_10_19/pseudo/Nd3plus_f-in-core.dojo_psp8_conv.upf}
UPF_NAME=Nd3plus_f-in-core.dojo_psp8_conv.upf
REGEN=${REGEN:-0}
ONCV_GIT=${ONCV_GIT:-https://github.com/oncvpsp/oncvpsp.git}
ONCV_REF=${ONCV_REF:-4.0.1}
NJ=${NJ:-4}
FC=${FC:-gfortran}; MAKE=${MAKE:-make}     # 시험에서 없는 이름을 주면 ③ 이 멈춰야 한다
CHK=$REPO/tools/electronic/oncv_regen_check.py
mkdir -p "$P/dojo" "$P/run" "$P/upf"
LOG=$P/make.log
say(){ echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
exec 9>"$P/.lock"; flock -n 9 || { say "⛔ 이미 실행 중"; exit 6; }
say "════ Nd3+ NC psp8 → UPF · HEAD $(git -C "$REPO" rev-parse --short HEAD 2>/dev/null) · REGEN $REGEN · $P ════"

# ① 원본 + md5 ────────────────────────────────────────────────────────────────
for e in in psp8 djrepo out; do
  f="$P/dojo/Nd3+_f-in-core.$e"
  [ -s "$f" ] || curl -fsS --max-time 60 "$RAW/Nd3%2B_f-in-core.$e" -o "$f" || { rm -f "$f"; say "⛔ 받기 실패 $e ($RAW)"; exit 3; }
done
"$PY" "$CHK" --md5 "$P/dojo/Nd3+_f-in-core.psp8" "$MD5" | tee -a "$LOG"
[ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ psp8 md5 ≠ PseudoDojo 기록"; exit 3; }
"$PY" -c "import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d.get('md5')==sys.argv[2] else 1)" "$P/dojo/Nd3+_f-in-core.djrepo" "$MD5" \
  || { say "⛔ djrepo 의 md5 가 기대와 다르다"; exit 3; }
say "원본 ✓ md5 $MD5 (psp8 = djrepo)"

# ② 변환 · 저장소 UPF 와 대조 ─────────────────────────────────────────────────
"$PY" "$CHK" --to_upf "$P/dojo/Nd3+_f-in-core.psp8" --dest "$P/upf/$UPF_NAME" 2>&1 | tee -a "$LOG"
[ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ 변환 실패"; exit 4; }
NEW_SHA=$(sha256sum "$P/upf/$UPF_NAME" | cut -c1-64)
[ -s "$REF_UPF" ] || { say "⛔ 저장소 UPF 없음 ($REF_UPF)"; exit 4; }
REF_SHA=$(sha256sum "$REF_UPF" | cut -c1-64)
[ "$NEW_SHA" = "$REF_SHA" ] || { say "⛔ 변환 UPF sha256 ${NEW_SHA:0:16} ≠ 저장소 ${REF_SHA:0:16} — 쓰지 않는다"; exit 4; }
say "UPF ✓ 원본에서 다시 만든 것 = 저장소 UPF (sha256 ${NEW_SHA:0:16}…)"

# ③ (REGEN=1) 변환기 검증을 이 기계에서 다시 ───────────────────────────────────
PAIR=skip; CMP=skip; ONCV_COMMIT=""
if [ "$REGEN" = 1 ]; then
  miss=""
  command -v "$FC" >/dev/null || miss="$miss $FC"
  command -v "$MAKE" >/dev/null || miss="$miss $MAKE"
  # LAPACK·BLAS — 링크에는 버전 없는 .so 가 있어야 한다 (liblapack.so · libblas.so 또는 libopenblas.so)
  if [ -n "${LAPACK_ROOT:-}" ]; then LST=$(ls "$LAPACK_ROOT/lib" 2>/dev/null | sed 's/$/ /'); LDIR="-L$LAPACK_ROOT/lib -Wl,-rpath,$LAPACK_ROOT/lib"
  else LST=$(ldconfig -p 2>/dev/null | awk '{print $1" "}'); LDIR=""; fi
  if printf '%s\n' "$LST" | grep -q "^liblapack\.so $" && printf '%s\n' "$LST" | grep -q "^libblas\.so $"; then BL="-llapack -lblas"
  elif printf '%s\n' "$LST" | grep -q "^libopenblas\.so $"; then BL="-lopenblas"
  else miss="$miss LAPACK/BLAS(.so)"; fi
  if [ -n "$miss" ]; then
    say "⛔ 도구 없음:$miss — 예: /data/apps/miniforge3/bin/conda create -y -p /data/work/envs/oncv -c conda-forge gfortran make liblapack libblas"
    say "   그 뒤 PATH=/data/work/envs/oncv/bin:\$PATH LAPACK_ROOT=/data/work/envs/oncv 로 다시"
    exit 5
  fi
  say "도구 ✓ $("$FC" --version | head -1) · LIBS $LDIR $BL"
  S=$P/oncvpsp
  X=$S/src/oncvpsp.x
  if [ ! -x "$X" ]; then
    [ -d "$S/.git" ] || git clone -q --depth 1 --branch "$ONCV_REF" "$ONCV_GIT" "$S" >> "$LOG" 2>&1 || { say "⛔ git clone 실패 ($ONCV_GIT $ONCV_REF)"; exit 6; }
    # 4.0.1 은 make.inc 빌드다 (CMakeLists.txt 없음) · 배포 make.inc 는 libxc 를 켜 두었다 → 덮어쓴다
    cat > "$S/make.inc" <<EOF
F77        = $FC
F90        = $FC
CC         = gcc
FCCPP      = cpp
FLINKER    = \$(F90)
FCCPPFLAGS = -ansi -DLIBXC_VERSION=400
FFLAGS     = -O3 -ffast-math -funroll-loops
CFLAGS     = -O3
LIBS       = $LDIR $BL
OBJS_LIBXC = exc_libxc_stub.o
EOF
    "$MAKE" -C "$S/src" -j "$NJ" oncvpsp >> "$LOG" 2>&1 || { say "⛔ ONCVPSP 빌드 실패 — $LOG"; exit 6; }
  fi
  [ -x "$X" ] || { say "⛔ oncvpsp.x 를 못 찾았다 ($X)"; exit 6; }
  ONCV_COMMIT=$(git -C "$S" rev-parse HEAD 2>/dev/null)
  say "ONCVPSP ✓ ref $ONCV_REF · commit ${ONCV_COMMIT:0:12}"
  cd "$P/run" || exit 6
  "$PY" "$CHK" --set_psfile "$P/dojo/Nd3+_f-in-core.in" both --dest Nd3+_both.dat >> "$LOG" 2>&1 || { say "⛔ psfile 바꾸기 실패"; exit 6; }
  "$X" < Nd3+_both.dat > Nd3+_both.out 2>&1
  rc=$?
  [ "$rc" = 0 ] && ! grep -aq "ERROR" Nd3+_both.out || { say "⛔ ONCVPSP rc=$rc 또는 ERROR — Nd3+_both.out"; exit 6; }
  say "ONCVPSP 실행 ✓ $(head -2 Nd3+_both.out | tail -1 | tr -s ' ') · 경고 $(grep -ac WARNING Nd3+_both.out) 줄"
  "$PY" "$CHK" --extract Nd3+_both.out --kind psp8 --dest Nd3+_regen.psp8 >> "$LOG" 2>&1 || { say "⛔ psp8 뽑기 실패"; exit 6; }
  "$PY" "$CHK" --extract Nd3+_both.out --kind upf --dest Nd3+_f-in-core.oncvpsp401.upf >> "$LOG" 2>&1 || { say "⛔ UPF 뽑기 실패"; exit 6; }
  "$PY" "$CHK" --compare "$P/dojo/Nd3+_f-in-core.psp8" Nd3+_regen.psp8 --tol 1e-3 --json compare_vs_dojo.json > compare_vs_dojo.txt 2>&1
  CMP=$([ $? = 0 ] && echo same || echo differ)
  say "재생성 psp8 대 배포본: $CMP (기록만 — 4.0.1 은 다른 pseudo 를 낸다고 알려져 있다)"
  "$PY" "$CHK" --to_upf Nd3+_regen.psp8 --dest conv401.upf >> "$LOG" 2>&1 || { say "⛔ 재생성 psp8 변환 실패"; exit 7; }
  "$PY" "$CHK" --compare_upf Nd3+_f-in-core.oncvpsp401.upf conv401.upf --json cmp_conv401.json 2>&1 | tee -a "$LOG"
  [ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ 같은 실행 짝 대조 실패 — 변환기를 믿을 수 없다 (cmp_conv401.json)"; exit 7; }
  PAIR=pass
fi

# ④ 기록 ───────────────────────────────────────────────────────────────────
"$PY" - "$P" "$MD5" "$UPF_NAME" "$REF_UPF" "$REGEN" "$ONCV_REF" "$ONCV_COMMIT" "$CMP" "$PAIR" <<'PY'
import json, sys, hashlib, os
P, md5, upf, ref, regen, oref, ocommit, cmp_, pair = sys.argv[1:10]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rec = {"schema": "nd3plus_nc_upf/v2", "source": "PseudoDojo ONCVPSP-PBE-PDv0.4/Nd/Nd3+_f-in-core (ONCVPSP 3.2.3.1)",
       "dojo_md5": md5, "dojo_psp8_sha256": sha(os.path.join(P, "dojo", "Nd3+_f-in-core.psp8")),
       "upf": f"upf/{upf}", "upf_sha256": sha(os.path.join(P, "upf", upf)), "repo_upf": ref, "repo_upf_same": True,
       "conversion": "oncv_regen_check.py --to_upf (ONCVPSP 4.0.1 upfout.f90 규약 · 보간 없음 · PP_PSWFC 없음 · rchrg 밖 쿨롱)",
       "regen": {"done": regen == "1", "oncvpsp_ref": oref if regen == "1" else None, "oncvpsp_commit": ocommit or None,
                 "regen_psp8_vs_dojo": cmp_, "same_run_pair_check": pair}}
open(os.path.join(P, "nd3plus_upf_record.json"), "w").write(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
print("→ nd3plus_upf_record.json")
PY
say "■ 끝 · 끝 코드 0"
( cd "$P" && find dojo upf run nd3plus_upf_record.json make.log -type f -print0 2>/dev/null | sort -z | xargs -0 sha256sum > SHA256SUMS )
exit 0
