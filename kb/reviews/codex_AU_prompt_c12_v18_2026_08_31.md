---
title: "리뷰 요청 AU — C-12 v18 (회신 AT P0 5건 + 해제조건 9 이행)"
date: 2026-08-31
updated: 2026-08-31
tags: [review, codex, sdcp, c12, vasp, handoff, prompt]
status: 발송 대기
kind: review-request
system: sdcp
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 AU — `sdcp_c12_v18.zip`

> 이전 회신: `kb/reviews/codex_AT_reply_c12_v17_2026_08_31.md` (NO-GO · P0 5건 · 해제조건 9)
> **VASP 는 아직 한 잡도 돌리지 않았습니다.**

```
ZIP      b094a899cf08919b1be7285fb51715aa7ca8e8ef83687ae4eecd33e0f002529c
MANIFEST d6ce4d943eee842f1307c0ff1b1a253ca93e535a24a57b25a83241dcb1478f00
```

생성 인자는 v17 의 `generated_argv` 를 **그대로** 썼습니다 — 같은 입력이어야
v17↔v18 차이가 "고친 것" 만이 됩니다.

## 1. P0 5건 — 무엇이 문제였고 무엇으로 막는가

### P0-1 SDCP 기체 3잡이 계산 전부터 영구 게이트 — **확인했고 고쳤습니다**

지적이 정확합니다. 기체 잡의 POSCAR 는 원소별로 묶어(`idx`) 쓰는데
`mol_graph_canonical` 은 **항등 순서**로 만들어 실었습니다. 주석에 "슬랩이 없으니
POSCAR 순서가 곧 원자 순서다" 라고 적어 놓고 세 줄 위에서 원소별로 묶고 있었습니다.
복합체 잡은 `pos["order"]` 를 넘기고 있었으므로 **기체만** 어긋났습니다.

원소가 섞인 10원자 분자로 축소 재현했습니다:

| | POSCAR 원소순 | 정본 | 끊김 | 생성 |
|---|---|---:|---:|---:|
| v17 (항등 순서) | `COHCOHSCHO → OOOSCCCHHH` | 10 | **6** | **6** |
| v18 (`idx`) | 같음 | 10 | 0 | 0 |

**왜 selftest 가 못 잡았나**: 기존 검사가 `set(e) <= set(mol_poscar_idx)` 였습니다 —
**어떤 순열이든 통과**합니다. 그리고 검사 대상으로 고른 잡이 복합체였습니다.

고친 것 셋:
1. `_mol_graph_canon(at, 0, idx)` — 복합체와 같은 규약
2. **빌드 preflight 에 배포 POSCAR 되읽기 대조** — 분자를 든 모든 잡에 대해 POSCAR 를
   다시 읽어 같은 규약으로 그래프를 만들고 정본과 대조합니다. 귀하가 하신 일을
   빌드가 스스로 합니다.
3. selftest 회귀 3건 — 그중 하나가 **음성**: "항등 순서로 만들면 반드시 어긋나야 한다".
   그것이 없으면 2번이 헛돕니다.

### P0-2 dense 의 INCAR·k 감사 fail-open

`incar_expected.dense` 를 추가했습니다. 그리고 k 검사를 **정확 대조**로 바꿨습니다 —
종전 `NKPTS ≤ 격자곱` 은 coarse(3 4 1 = 12) OUTCAR 를 dense(4 6 1 = 24) 폴더에 넣어도
12 ≤ 24 라 통과했습니다.

KPOINTS 제목 줄에 `phase=dense k=4 6 1 shift=0 0 0` 을 싣고, VASP 가 그 줄을
OUTCAR 에 ` KPOINTS:` 로 되울리는 것을 **정확히** 대조합니다. 되울림이 없으면
`KPOINTS_TITLE_UNVERIFIED` — 확인 못 한 것은 통과가 아닙니다.
`kpoints_expected`/`incar_expected` 가 없는 구판 dense 는 막습니다.

### P0-3 POTCAR/provenance 를 독립 검증 없이 신뢰

종전엔 기존 provenance 의 `allowlist_sha256` 만 맞으면 `continue` 로 재조립을
건너뛰었습니다. **있으면 믿는 검사는 검사가 아닙니다.**

- 기존 POTCAR/provenance 를 **치우고 매번 PP 원본에서 다시 조립**합니다.
  이전과 SHA 가 다르면 조용히 고치지 않고 화면에 말합니다.
- `PP` 트리가 없으면 즉시 거부합니다.
- 잡마다 PP **원본 파일 자체**를 독립 재계산: variant 별 SHA256 · TITEL 토큰 ·
  allowlist 결박. allowlist 는 `sha256 <경로>/<variant>/POTCAR` 형식이므로
  **해시와 variant 가 한 줄에 묶여** 있는지 봅니다 (해시만 맞고 이름이 다르면
  다른 PP 입니다).

### P0-4 seal/attestation fail-open

전부 **타입 문제**였습니다. `sealed_before_production` 이 문자열 `"true"` 여도
파이썬에선 참이라 통과했고, `schema` 는 검사 목록에 아예 없었습니다.

- 봉인 재검사: `schema` 정확 대조 · `sealed_before_production is True` ·
  evidence 가 이 도구의 문구와 같은지 · `sealed_at_utc` 형식과 **미래 금지**
- attestation: 필수 목록에 `schema` 추가 + 값 대조 ·
  `made_before_production is True` · `created_utc` 형식
- 🔴 **root seal 이 없으면 attestation 을 못 씁니다.** 종전엔 variant 집합 대조가
  `if _seal and …` 이라 봉인이 없으면 통째로 건너뛰었고, 임의 release label 의
  attestation 이 `usable=true` 로 갔습니다.

### P0-5 실행 경로와 문서의 모순 + launcher 우회

`VASP_LAUNCHER='mpirun -np 48 /other/vasp'` 로 주면 최종 명령이
`mpirun -np 48 /other/vasp /sealed/vasp_std` 가 되어 mpirun 은 **앞의 것**을 돕니다.
봉인은 뒤의 것을 해시했으므로 봉인 전체가 무의미해집니다.

- 셸 메타문자 거부 · 첫 토큰은 허용 목록(mpirun/mpiexec/srun/aprun/jsrun/ibrun/env)
  · 그 뒤 토큰이 **실행 가능한 파일**이면 거부
- 잡 실행 **직전** `EXECUTABLE_RECEIPT.tsv` (시각·sha256·경로·launcher)
- **INT/TERM trap** 이 종전엔 lock 만 지우고 러너는 계속 돌았습니다 (bash 는 핸들러
  뒤에 하던 일을 이어갑니다). 이제 프로세스 그룹을 죽이고 130/143 으로 나갑니다.
- `SEAL_POTCAR_ROOT.sh` · `MAKE_POTCAR_ATTESTATION.sh` 도 같은 `.lock_bundle` 참여
- 문서: `VASP_CMD=` **대입문 삭제**(경고 문장은 남김) · 수동 `run_job.sh` 경로 삭제 ·
  `sbatch --array` 예시 삭제 · `EXPECT_ZIP_SHA256`/`EXPECT_MANIFEST_SHA256` 을
  **둘 다 필수**로 명시

## 2. Q 답변 — 받아들인 것과 우리 판단

**Q1 셀 한정 · D3-off 반대 — 전부 수용.**
`molecule_image_min_distance_A` 가 조각별 **최솟값 하나**여서, sdcp 4.613 Å(대안
자세 b12 의 worst case)이 primary 값처럼 보고됐습니다. 정정합니다:

| 조각 | primary b00 | 대안 자세 |
|---|---:|---:|
| sdcp_neutral | **4.894** | 4.613 (b12 stress_sensitivity) |
| ptfe_c10 | **5.646** | 6.05 (b52 sensitivity) |

"공통 주기영상 항이 상당 부분 소거된다" 는 **삭제**했습니다 (슬랩 원자 48/192 ·
최대 변위 0.296 Å). D3-off 잡은 만들지 않습니다 — 기존 OUTCAR 의 Edisp 로 D 의 총
D3 기여를 계산합니다. **v18 의 D3-off 쌍둥이 0개**입니다.

**Q2 합산 오차예산 — 수용.** `B_num = |Δ_vac| + |δ_gas| + |δ_k| ≤ 5 meV`,
RSS 금지 사유를 산출물에 적습니다. 넘으면 **값을 버리지 않고** 0.01 eV 안정성 주장을
하지 않습니다. 축이 하나라도 없으면 `NUMERIC_BUDGET_INCOMPLETE`.
selftest: 축별 2 meV 는 각각 통과하지만 합 6 meV 는 넘습니다 (RSS 면 3.46 이라 통과).

**Q3 병렬도 — 수용.** 기본 병렬도를 낮추고 `NPAR` 로만 조절합니다. 배열 제출 예시를
문서에서 뺐습니다. 봉인기·attestation 생성기·러너가 같은 lock 에 참여합니다.

**Q4 서명된 외부 checksum — 동의하나 이번 판에는 없습니다.** 지금은 메일 본문의 해시를
사람이 붙여넣는 단계가 남아 있습니다. detached-signed SHA256SUMS 나 signed git tag 로
가려면 양측 키 교환이 필요해 이번 라운드 범위 밖으로 두었습니다. **이 상태로 시작해도
되는지** 판정해 주십시오.

**Q5 pooled 엄격화 — 권장안 (a) 채택.** pooled 최솟값과 secondary_G 를 **영구
비인용**으로 고정했습니다 (추가 잡 0). 값은 `secondary_G_eV_diagnostic` 에 남깁니다.

⚠ **여기에 귀하가 쓰지 않은 논거를 하나 더 달았습니다 — 확인 부탁드립니다.**
+2 잡(net4 dense)으로는 k 미검증 문제만 닫히고 **basin 혼합은 그대로**라고 판단했습니다.
`secondary_G_citable` 이 `nonprimary_notes` 가 비어 있을 것을 요구하는데, 거기에
`BASIN_HETEROGENEOUS` 가 들어가고, pm1/net4 는 애초에 서로 다른 자기상태로 수렴하라고
넣은 seed 이므로 사실상 상시 뜹니다. 그렇다면 인용가능 pool 은 잡 두 개가 아니라
**설계 변경**(basin 별 pool 분할 + pooled min 재정의)이 필요합니다.
**이 판단이 맞습니까?**

**Q6 좁은 estimand 문구 — 그대로 채택.** 사전등록 문서 §2 에 조건절까지 넣어
고정했습니다 (`db/properties/sdcp_c12_claim_prereg_2026_08_31.json`).

## 3. 이번에 드러난 것 — 우리 쪽 자기점검

이 라운드에서 고친 회귀 중 **우리가 만든 것**이 셋 있습니다. 기록해 둡니다:

1. 새 k 정확대조 게이트가 selftest 픽스처의 **정상 잡까지 막았습니다.** 픽스처 OUTCAR 에
   ` KPOINTS:` 되울림이 없었고, dense 픽스처가 static OUTCAR 를 베껴 만들어 제목이
   static 인 채였습니다. **게이트는 맞게 동작했고 픽스처가 실물과 달랐습니다.**
2. 문서 블록의 `%` 인자 개수가 어긋나 빌드가 `TypeError` 로 죽었습니다.
3. AT P0-2 시험을 처음에 **생성기 selftest** 에 넣었다가 `NameError` 가 났습니다 —
   `phase_gates` 는 배포본 분석기의 함수입니다. 배포본 안(`_selftest_closure`)으로
   옮겼고, 그래서 이제 생성기와 배포본 양쪽에서 같은 시험이 돕니다.

## 4. 확인 방법

```bash
python3 tools/sdcp/vasp_handoff_bundle.py --selftest
python3 tools/sdcp/vasp_handoff_bundle.py --verify_zip sdcp_c12_v18.zip --expect_jobs 16
cd <풀린 번들> && env -u PYTHONIOENCODING LC_ALL=C PYTHONUTF8=0 python3 analyze_results.py --selftest
```

배포본 selftest **274/274 PASS** (v17 은 257). estimand 판정 검사 87건이 배포본
안에서 돕니다. 공격 fixture(가짜 POTCAR + 자기일관 provenance · PP 부재 · variant 삭제 ·
위조 seal schema · 문자열 불리언 · 손으로 쓴 근거 · 미래 시각 · launcher 우회 3종 ·
남의 lock)는 **실제로 `run_staged.sh` 를 돌려** rc≠0 을 확인합니다.

## 5. 여쭙는 것

**Q1.** P0-1 과 같은 종류 — **결과가 오기 전에 이미 막히는** 잡이 v18 에 또 있습니까?
빌드 preflight 를 넣었지만, 그것이 보는 것은 우리가 생각한 축뿐입니다.

**Q2.** Q5 의 우리 판단(§2)이 맞습니까 — pooled 를 인용가능하게 하려면 +2 잡이 아니라
설계 변경이 필요합니까?

**Q3.** `B_num ≤ 5 meV` 를 **넘었을 때의 처방**이 맞습니까? 지금은 "0.01 eV 주장 안 함 +
해상도 낮춤 + 축별 민감도" 입니다. 값 자체를 버려야 하는 경우가 있습니까?

**Q4.** Q4(서명된 checksum)를 이번 판에 넣지 않고 시작해도 됩니까? 아니면 그것이
선행조건입니까?

**Q5.** launcher 허용 목록(mpirun/mpiexec/srun/aprun/jsrun/ibrun/env)이 현장에서
지나치게 좁습니까? 넓히면 P0-5 의 우회가 다시 열립니까?

**Q6.** 이번에도 **결과를 보기 전에** 더 넣거나 빼야 할 잡이 있습니까?

파일은 수정하지 않으셔도 됩니다 — 판정만 주십시오.
