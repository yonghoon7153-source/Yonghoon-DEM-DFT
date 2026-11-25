#!/usr/bin/env bash
# =============================================================================
# v5_rerun_r1.sh JOB — A′ V5 VASP: 사전등록 재시도 r1 을 **한 잡에 한 번만** 수동으로 돌린다 (2026-10-08)
#
# 왜: run_all.sh (v6) 의 수렴 판정은 OUTCAR 'aborting loop because EDIFF is reached' 문구를 본다. VASP 5.4.4 는 NELM 을 다
#     써서 끝나도 이 문구를 찍어서, NELM 소진 (예: V5_s_outer_A_G3_c2_far_i · 200 스텝 · 마지막 |dE| 2.3e-3) 을 수렴으로 읽고
#     사전등록 재시도 (INCAR.r1 · AMIX 0.1 · BMIX 0.01 · NELM 300) 를 건너뛰었다. 이 스크립트는 그 재시도를 **러너와 같은 함수**
#     (run_all.sh 의 h · run_one 을 그대로 꺼내 쓴다) 로 돌린다 → run/<JOB>_r1 · attempt.json · status.tsv 줄 형식이 같다.
#
# 쓰는 법 (패키지 폴더 = run_all.sh 옆에 이 파일을 두고 · 본 러너가 끝난 뒤 권장 — 같은 노드 자원을 나눠 쓰지 않게):
#   VASP_CMD="mpirun -np 128 vasp_std" POTCAR_DIR=/path/to/PAW_PBE bash v5_rerun_r1.sh V5_s_outer_A_G3_c2_far_i
#   그 뒤 PACK_ONLY=1 bash run_all.sh   (반송 묶음 다시 만들기 · r1 폴더가 같이 들어간다) → sha256sum -c V5_vasp_return.tgz.sha256
#
# 지키는 것: MANIFEST 검사 · 첫 시도 폴더가 있어야 함 · r1 폴더가 이미 있으면 안 돎 (원자적 mkdir) · 성능 태그는 첫 실행과 같게
#   (run/env.txt 의 PERF_TAGS 줄에서 복원) · 첫 시도 OSZICAR 마지막 스텝이 이미 수렴(|dE|·|d eps| ≤ 1e-6)이면 안 돎 (재시도 자격 없음) ·
#   끝난 뒤 r1 의 OSZICAR 마지막 스텝으로 **진짜** 수렴을 다시 본다 (run_one 의 판정은 같은 VASP 5.x 함정이 있다).
# ⛔ 못 하는 것: 두 번째 재시도 · 다른 설정 · 첫 시도 폴더 수정. r1 도 미수렴이면 그 잡은 '값 없음' 으로 반송한다.
#   최종 판정은 반송 뒤 우리 쪽 --collect 가 한다 (OSZICAR 마지막 스텝 검사 포함 · tools/wad/build_v5_vasp_package.py).
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
JOB=${1:-}; [ -n "$JOB" ] || { echo "사용법: bash v5_rerun_r1.sh <잡>"; exit 2; }
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다"; exit 2; }
{ [ -d "jobs/$JOB" ] && [ -f "jobs/$JOB/INCAR.r1" ]; } || { echo "⛔ 모르는 잡 또는 INCAR.r1 없음: $JOB"; exit 2; }
[ -d "run/$JOB" ] || { echo "⛔ 첫 시도 폴더 run/$JOB 이 없다 — 재시도 대상이 아니다"; exit 2; }
[ -e "run/${JOB}_r1" ] && { echo "⛔ run/${JOB}_r1 이 이미 있다 — 재시도는 한 번뿐"; exit 2; }
: "${VASP_CMD:?VASP_CMD 가 필요하다}" "${POTCAR_DIR:?POTCAR_DIR 가 필요하다}"
lastline(){ grep -E "^[[:space:]]*(DAV|RMM|CG|SDA):" "$1" 2>/dev/null | tail -1; }
is_conv(){ [ -n "$1" ] && echo "$1" | awk '{d=$4+0; e=$5+0; if (d<0) d=-d; if (e<0) e=-e; exit !(NF>=5 && d<=1e-6 && e<=1e-6)}'; }
last=$(lastline "run/$JOB/OSZICAR")
if is_conv "$last"; then echo "⛔ run/$JOB 의 OSZICAR 마지막 스텝이 이미 수렴이다 ($last) — 재시도 자격 없음"; exit 2; fi
echo "첫 시도 마지막 전자 스텝: ${last:-(못 읽음)}"
PERF_LINES=$(grep -m1 '^PERF_TAGS ' run/env.txt 2>/dev/null | sed 's/^PERF_TAGS //' | tr ';' '\n' | sed '/^$/d')
[ -n "$PERF_LINES" ] && PERF_LINES="$PERF_LINES"$'\n'
echo "성능 태그 (첫 실행과 같게): $(printf '%s' "$PERF_LINES" | tr '\n' ' ')"
eval "$(sed -n '/^h(){/,/^}$/p' run_all.sh)"
{ declare -F run_one >/dev/null && declare -F h >/dev/null; } || { echo "⛔ run_all.sh 에서 run_one·h 를 못 꺼냈다"; exit 2; }
echo "manual_r1 $JOB $(date -u +%FT%TZ) — VASP 5.x NELM 소진을 러너가 수렴으로 읽음 · 사전등록 재시도 수동 실행 (1저자 승인)" >> run/env.txt
run_one "$JOB" r1 INCAR.r1; s=$?
lr=$(lastline "run/${JOB}_r1/OSZICAR")
if [ "$s" = 0 ] && is_conv "$lr"; then echo "✓ $JOB (r1) 수렴 — 마지막 스텝: $lr · 이제 PACK_ONLY=1 bash run_all.sh"; exit 0; fi
echo "⛔ $JOB r1 도 실패·미수렴 (러너 판정 $s · 마지막 스텝: ${lr:-못 읽음}) — 값 없음으로 반송 (더 돌리지 않는다) · PACK_ONLY=1 bash run_all.sh"; exit 1
