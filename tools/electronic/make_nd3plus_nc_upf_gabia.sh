#!/usr/bin/env bash
# =============================================================================
# make_nd3plus_nc_upf_gabia.sh — 4f 를 core 에 둔 NC Nd (PseudoDojo Nd3+_f-in-core) 를 QE 가 읽는 UPF 로 · gabia
#   Nd Q3 ELF 의 NC 규약 (사용자 10-19 '권고대로 해' · runlog nd_q3_bader_elf_runlog_2026_10_19.json).
#
# 왜 이렇게 하나
#   PseudoDojo (ONCVPSP-PBE-PDv0.4/Nd/Nd3+_f-in-core · ONCVPSP 3.2.3.1 · 가전자 5s²5p⁶5d¹6s² = 11 · 표준 표 밖) 는 psp8 만 배포한다.
#   UPF 를 손으로 변환하지 않는다 — ONCVPSP 를 빌드해 **같은 입력**으로 psfile 'both' 를 돌리면 한 실행에서 psp8 · UPF 가 같이 나온다.
#   그 psp8 을 배포본과 열마다 대조해 차이를 잰다 (tools/electronic/oncv_regen_check.py).
#   ⚠ GitHub oncvpsp 에는 3.2.3 소스가 없다 (태그는 4.0.1 · master 에 옛 optimize 도 없다) — 4.0.1 은 3.3.0 의 optimize 수정 ·
#     4.0.1 의 modcore 도함수 잡음 제거가 들어 있어 숫자가 조금 다를 수 있다. 이 러너는 **재고 기록만** 한다 — UPF 를
#     pseudo 폴더에 넣지 않는다 (차이를 보고 사용자와 정한다 · 필요하면 같은 실행의 psp8+UPF 짝으로 변환기를 검증해 배포본에 쓴다).
#
# 쓰는 법 (worktree 뿌리에서 · CPU 몇 분 — QE 계산 아님 · ONCVPSP 원자 계산은 수 초)
#   bash tools/electronic/make_nd3plus_nc_upf_gabia.sh
#
# 순서: ① PseudoDojo 원본 넷 (.in · .psp8 · .djrepo · .out) 받기 + md5 (djrepo 의 md5 = 474ce0fc…)
#       ② 도구 확인 (gfortran · cmake · LAPACK) — 없으면 멈추고 conda 안내
#       ③ ONCVPSP 4.0.1 받기 · 빌드 (Libxc · TOML 끔 — iexc 4 = 내장 PBE) · 커밋 기록
#       ④ 입력 psfile → both · 실행 · ERROR 줄 검사
#       ⑤ psp8 · UPF 뽑기 · 배포본 psp8 과 열마다 대조 (tol 1e-3 · 넘어도 기록하고 끝 코드 0 — '같다/다르다' 는 기록이 말한다)
#       ⑥ 기록 JSON + SHA256SUMS
# 종료: 0 끝 (대조 결과는 nd3plus_regen_record.json) · 3 원본 받기·md5 실패 · 5 도구 없음 · 6 ONCVPSP 빌드·실행 실패
# ⛔ 못 하는 것: pseudo 의 전이성 검증 (PseudoDojo 기록을 믿는다) · UPF 설치 · QE 계산
# =============================================================================
set -u; set +H
REPO=$(cd "$(dirname "$0")/../.." && pwd)
P=${P:-/data/work/pseudo_nc_nd3plus_2026_10_19}
PY=${PY:-python3}
RAW=${RAW:-https://raw.githubusercontent.com/PseudoDojo/ONCVPSP-PBE-PDv0.4/master/Nd}
MD5=474ce0fc5175ff9ddf2621f906febf65
ONCV_GIT=${ONCV_GIT:-https://github.com/oncvpsp/oncvpsp.git}
ONCV_REF=${ONCV_REF:-4.0.1}
NJ=${NJ:-4}
FC=${FC:-gfortran}; CMAKE=${CMAKE:-cmake}     # 시험에서 없는 이름을 주면 ② 가 멈춰야 한다
CHK=$REPO/tools/electronic/oncv_regen_check.py
mkdir -p "$P/dojo" "$P/run"
LOG=$P/make.log
say(){ echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
exec 9>"$P/.lock"; flock -n 9 || { say "⛔ 이미 실행 중"; exit 6; }
say "════ Nd3+ NC → UPF (ONCVPSP 다시 생성) · HEAD $(git -C "$REPO" rev-parse --short HEAD 2>/dev/null) · $P ════"

# ① 원본 + md5 ────────────────────────────────────────────────────────────────
for e in in psp8 djrepo out; do
  f="$P/dojo/Nd3+_f-in-core.$e"
  [ -s "$f" ] || curl -fsS --max-time 60 "$RAW/Nd3%2B_f-in-core.$e" -o "$f" || { say "⛔ 받기 실패 $e ($RAW)"; exit 3; }
done
"$PY" "$CHK" --md5 "$P/dojo/Nd3+_f-in-core.psp8" "$MD5" | tee -a "$LOG"
[ "${PIPESTATUS[0]}" = 0 ] || { say "⛔ psp8 md5 ≠ PseudoDojo 기록"; exit 3; }
"$PY" -c "import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d.get('md5')==sys.argv[2] else 1)" "$P/dojo/Nd3+_f-in-core.djrepo" "$MD5" \
  || { say "⛔ djrepo 의 md5 가 기대와 다르다"; exit 3; }
say "원본 ✓ md5 $MD5 (psp8 = djrepo)"

# ② 도구 ───────────────────────────────────────────────────────────────────
miss=""
command -v "$FC" >/dev/null || miss="$miss $FC"
command -v "$CMAKE" >/dev/null || miss="$miss $CMAKE"
# LAPACK — 시스템 (ldconfig) 이나 LAPACK_ROOT (conda env 처럼 ldconfig 에 안 보이는 곳) 둘 중 하나면 된다
if [ -n "${LAPACK_ROOT:-}" ]; then ls "$LAPACK_ROOT"/lib/ 2>/dev/null | grep -qE "^lib(lapack|openblas)\." || miss="$miss LAPACK(LAPACK_ROOT=$LAPACK_ROOT)"
else ldconfig -p 2>/dev/null | grep -qE "liblapack\.so|libopenblas\.so" || miss="$miss LAPACK"; fi
if [ -n "$miss" ]; then
  say "⛔ 도구 없음:$miss — 예: /data/apps/miniforge3/bin/conda create -y -p /data/work/envs/oncv -c conda-forge gfortran cmake make liblapack libblas"
  say "   그 뒤 PATH=/data/work/envs/oncv/bin:\$PATH 로 다시 (LAPACK_ROOT=/data/work/envs/oncv)"
  exit 5
fi
say "도구 ✓ $("$FC" --version | head -1) · $("$CMAKE" --version | head -1)"

# ③ ONCVPSP 4.0.1 ──────────────────────────────────────────────────────────
S=$P/oncvpsp
if [ ! -x "$S/build/oncvpsp.x" ] && [ ! -x "$S/build/src/oncvpsp.x" ]; then
  [ -d "$S/.git" ] || git clone --depth 1 --branch "$ONCV_REF" "$ONCV_GIT" "$S" >> "$LOG" 2>&1 || { say "⛔ git clone 실패 ($ONCV_GIT $ONCV_REF)"; exit 6; }
  ( cd "$S" && FC="$FC" "$CMAKE" -S . -B build -DONCVPSP_WITH_Libxc=OFF -DONCVPSP_WITH_TOML=OFF ${LAPACK_ROOT:+-DLAPACK_ROOT=$LAPACK_ROOT} \
      && "$CMAKE" --build build --parallel "$NJ" ) >> "$LOG" 2>&1 || { say "⛔ ONCVPSP 빌드 실패 — $LOG"; exit 6; }
fi
X=$(ls "$S"/build/oncvpsp.x "$S"/build/src/oncvpsp.x "$S"/build/bin/oncvpsp.x 2>/dev/null | head -1)
[ -x "$X" ] || { say "⛔ oncvpsp.x 를 못 찾았다 (build 아래)"; exit 6; }
ONCV_COMMIT=$(git -C "$S" rev-parse HEAD 2>/dev/null)
say "ONCVPSP ✓ $X · ref $ONCV_REF · commit ${ONCV_COMMIT:0:12}"

# ④ 실행 ───────────────────────────────────────────────────────────────────
cd "$P/run" || exit 6
"$PY" "$CHK" --set_psfile "$P/dojo/Nd3+_f-in-core.in" both --dest Nd3+_both.dat >> "$LOG" 2>&1 || { say "⛔ psfile 바꾸기 실패"; exit 6; }
"$X" < Nd3+_both.dat > Nd3+_both.out 2>&1
rc=$?
grep -a "ERROR" Nd3+_both.out | head -3 | tee -a "$LOG"
[ "$rc" = 0 ] && ! grep -aq "ERROR" Nd3+_both.out || { say "⛔ ONCVPSP rc=$rc 또는 ERROR — Nd3+_both.out"; exit 6; }
say "ONCVPSP 실행 ✓ $(head -2 Nd3+_both.out | tail -1 | tr -s ' ')"

# ⑤ 뽑기 · 대조 ─────────────────────────────────────────────────────────────
"$PY" "$CHK" --extract Nd3+_both.out --kind psp8 --dest Nd3+_regen.psp8 >> "$LOG" 2>&1 || { say "⛔ psp8 뽑기 실패"; exit 6; }
"$PY" "$CHK" --extract Nd3+_both.out --kind upf --dest Nd3+_f-in-core.oncvpsp401.upf >> "$LOG" 2>&1 || { say "⛔ UPF 뽑기 실패"; exit 6; }
"$PY" "$CHK" --compare "$P/dojo/Nd3+_f-in-core.psp8" Nd3+_regen.psp8 --tol 1e-3 --json compare_vs_dojo.json 2>&1 | tee -a "$LOG"
CMP=${PIPESTATUS[0]}
ZV=$(grep -aoE 'z_valence="[^"]*"' Nd3+_f-in-core.oncvpsp401.upf | head -1)
say "UPF ✓ $(wc -c < Nd3+_f-in-core.oncvpsp401.upf) B · $ZV · 대조 $([ "$CMP" = 0 ] && echo '상대 ≤ 1e-3' || echo '상대 > 1e-3 (기록 참조)')"

# ⑥ 기록 ───────────────────────────────────────────────────────────────────
"$PY" - "$P" "$MD5" "$ONCV_REF" "$ONCV_COMMIT" "$CMP" "$ZV" <<'PY'
import json, sys, hashlib, os
P, md5, ref, commit, cmp_rc, zv = sys.argv[1:7]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
run = os.path.join(P, "run")
cmp = json.load(open(os.path.join(run, "compare_vs_dojo.json")))
rec = {"schema": "nd3plus_nc_regen/v1", "source": "PseudoDojo ONCVPSP-PBE-PDv0.4/Nd/Nd3+_f-in-core (ONCVPSP 3.2.3.1)",
       "dojo_md5": md5, "dojo_psp8_sha256": sha(os.path.join(P, "dojo", "Nd3+_f-in-core.psp8")),
       "oncvpsp_ref": ref, "oncvpsp_commit": commit, "upf": "run/Nd3+_f-in-core.oncvpsp401.upf",
       "upf_sha256": sha(os.path.join(run, "Nd3+_f-in-core.oncvpsp401.upf")), "upf_z_valence": zv,
       "compare_ok_tol_1e-3": cmp_rc == "0",
       "compare_worst": {k: {"rel": v.get("rel"), "worst_col": v.get("worst_col")} for k, v in cmp["blocks"].items()},
       "ekb_rel": {k: v["rel"] for k, v in cmp["ekb"].items()},
       "installed": False, "note": "UPF 는 설치하지 않았다 — 차이를 보고 정한다 (러너 머리 주석)"}
open(os.path.join(P, "nd3plus_regen_record.json"), "w").write(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
print("→ nd3plus_regen_record.json")
PY
say "■ 끝 · 끝 코드 0"
( cd "$P" && find dojo run nd3plus_regen_record.json make.log -type f -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS )
exit 0
