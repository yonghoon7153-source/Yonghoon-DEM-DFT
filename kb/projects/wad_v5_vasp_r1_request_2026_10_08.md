---
title: "V5 VASP 외주 — far_i r1 재시도 승인 + 남은 잡 상시 승인 (VASP 5.x NELM 소진 판정 버그) · 전달 프롬프트"
tags: [wad, adhesion, v5, vasp, outsourcing, retry, nelm, letter]
date: 2026-10-08
track: wad
kind: letter
status: 발송 대기 (사용자 2026-10-08 '전달할 프롬프트 부탁' = 권고 ① 진행)
confidence: high
verificationStatus: verified
verifiedAt: 2026-10-08
verifiedBy: self
explored: false
authoredBy: agent
---

> 트랙 W_ad (1저자 = 사용자 · 승인 주체). 외주 감사 회신 (10-08 · far_i 미수렴 · 러너 파서 버그) 에 대한 답이다.
> 스크립트 원본: `tools/wad/v5_rerun_r1.sh` (커밋 3472c1a) · sha256 `8a4c48913ff2412f597f81e967a193ee2d4a360426615e7e08bde6a1c9a13fde`.
> ⬇ 아래 **보내는 글**만 전달한다.

---

**[A′ V5 VASP] far_i 재시도 승인 · 남은 잡 상시 승인 · 실행 방법**

감사 고맙습니다. 진단이 맞습니다 — **우리 패키지 쪽 버그**입니다. run_all.sh (v6) 의 수렴 판정은 OUTCAR 의 `aborting loop because EDIFF is reached` 줄을 보는데, VASP 5.4.4 는 NELM 을 다 써도 이 줄을 찍습니다 (`EDIFF was not reached` 경고는 VASP 6 부터). 그래서 `V5_s_outer_A_G3_c2_far_i` (200 스텝 = NELM · 마지막 |dE| 2.3e-3) 를 수렴으로 읽었고 사전등록 재시도가 건너뛰어졌습니다. 나머지 8 잡이 OSZICAR 기준으로 진짜 수렴이라는 확인도 받았습니다.

우리 쪽 반송 검사기는 이미 고쳤습니다 — 이제 OSZICAR 마지막 전자 스텝의 |dE|·|d eps| 가 둘 다 1e-6 이하일 때만 수렴으로 받습니다. **run_all.sh 는 고치지 마세요** (MANIFEST 로 묶여 있어서 바꾸면 승인본이 아니게 됩니다).

## 1. 승인

- **① `V5_s_outer_A_G3_c2_far_i` — 사전등록 재시도 r1 을 한 번 돌려 주세요.** INCAR.r1 (AMIX 0.1 · BMIX 0.01 · NELM 300) 그대로입니다. 새 설정이 아니라 원래 발동했어야 할 규칙의 이행입니다.
- **② 남은 잡 상시 승인** — 지금 도는 `V5_s_outer_A_G4_e70_bound` 와 아직 안 뜬 8 잡 (G4_e70_far · G4_k1 bound/far · G4_s05 bound/far · p05_bound · s_outer_B bound/far) 이 끝날 때마다 아래 §3 확인 명령으로 OSZICAR 마지막 스텝을 봐 주세요. **|dE| 또는 |d eps| 가 1e-6 을 넘으면** 같은 방식으로 r1 을 **한 번만** 돌려 주세요. 따로 묻지 않으셔도 됩니다.
- ⛔ 그 밖의 재실행 · 다른 설정 (ENCUT · 혼합 · NELM 추가 등) · 두 번째 재시도는 하지 않습니다. r1 도 미수렴이면 그 잡은 '값 없음' 으로 그대로 반송해 주세요 (실패도 기록입니다).
- ⛔ 첫 시도 폴더 (`run/V5_s_outer_A_G3_c2_far_i`) 는 지우거나 고치지 말아 주세요 — 반송 묶음에 같이 들어가야 합니다.

## 2. 실행 방법

재시도는 아래 스크립트로 돌려 주세요. run_all.sh 안의 `run_one` 함수를 그대로 꺼내 쓰기 때문에 `run/<잡>_r1` 폴더 · attempt.json · status.tsv 줄 형식이 러너와 같습니다. 한 잡에 한 번만 돌고 (r1 폴더가 이미 있으면 거부), 첫 시도가 이미 수렴이면 거부하고, 성능 태그는 run/env.txt 의 첫 실행 값 그대로 씁니다. 끝난 뒤 r1 의 OSZICAR 로 수렴을 다시 확인합니다.

① 패키지 폴더 (run_all.sh 옆) 에 아래 내용을 `v5_rerun_r1.sh` 로 저장하고 해시를 확인해 주세요:

```bash
sha256sum v5_rerun_r1.sh
# 8a4c48913ff2412f597f81e967a193ee2d4a360426615e7e08bde6a1c9a13fde  이어야 합니다
```

② **본 러너 (run_all.sh) 가 끝난 뒤** 돌려 주세요 (같은 노드 자원을 나눠 쓰지 않게). 남는 노드가 따로 있으면 먼저 돌려도 됩니다 — 그때도 r1 폴더 이름은 같습니다.

```bash
VASP_CMD="<첫 실행과 같은 명령>" POTCAR_DIR=<첫 실행과 같은 경로> bash v5_rerun_r1.sh V5_s_outer_A_G3_c2_far_i
```

NELM 300 이라 15 h 이상 걸릴 수 있습니다.

③ 재시도가 다 끝나면 반송 묶음을 다시 만들어 주세요 (계산은 다시 하지 않습니다):

```bash
PACK_ONLY=1 bash run_all.sh && sha256sum -c V5_vasp_return.tgz.sha256
```

## 3. 끝난 잡 확인 명령 (잡이 끝날 때마다)

```bash
for d in run/V5_*/; do printf '%s ' "$d"; grep -E "^[[:space:]]*(DAV|RMM):" "$d/OSZICAR" | tail -1 | awk '{print $1,$2,$4,$5}'; done
```

셋째 · 넷째 값 (dE · d eps) 의 절댓값이 둘 다 1e-6 이하면 수렴입니다. 하나라도 넘으면 §1 ② 대로 r1 한 번입니다.

## 4. 반송 때 같이 보내 주실 것

- `V5_vasp_return.tgz` + `.sha256` (PACK_ONLY 로 다시 만든 것)
- `cat run/status.tsv` 출력
- §3 확인 명령 출력 (마지막 시점)
- `v5_rerun_r1.sh` 실행 화면의 마지막 줄 (✓ 수렴 / ⛔ 미수렴)
- `grep manual_r1 run/env.txt` 출력

참고로 status.tsv 의 converged 칸은 VASP 5.x 에서 믿을 수 없으니 그대로 두셔도 됩니다 — 판정은 반송 뒤 우리 검사기가 OSZICAR 로 다시 합니다.

## 부록 — `v5_rerun_r1.sh` 전문

```bash
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
```
