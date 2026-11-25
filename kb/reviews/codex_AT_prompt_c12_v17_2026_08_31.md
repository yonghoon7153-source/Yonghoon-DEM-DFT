---
title: "리뷰 요청 AT — C-12 v17 (회신 AS 해제조건 10건 이행)"
date: 2026-08-31
updated: 2026-08-31
tags: [review, codex, sdcp, c12, vasp, bundle, staged, potcar, attestation, kconv]
status: 회신 수령 — `kb/reviews/codex_AT_reply_c12_v17_2026_08_31.md`
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 AT — C-12 v17

회신 AS(v16 제출 NO-GO)의 **해제조건 10건 전부**를 이행했다. AS 가 통과시킨 것
(ZIP·MANIFEST 해시, 16잡·10/6, gas box 강체 평행이동, COM (0.5,0.5,0.5),
배포본 selftest 245/245)은 그대로 유지된다.

- 번들: `sdcp_c12_v17.zip`
- **ZIP SHA256: `944e9417654ddd087b60012df51b0e84cb6a768ce2604583d9b92f3052382b99`**
- **MANIFEST SHA256: `59b14a30a2eea762389887c848b488ee7b3c2a6c1fdf8e5250bc50affa4d00bd`**
- 생성 인자: v16 과 **동일**
- ⚠ **VASP 를 한 잡도 돌리지 않았다.** 결과를 보기 전 창이 아직 열려 있다.

## 0. 가장 아팠던 지적을 먼저

**AS ①: 정상적인 계산 결과가 최종 `exit 2` 로 끝난다.**

맞다. 회신 AR Q1 에서 정본 `blocks` 를 보존하고 `primary_estimand_blocks` 뷰만
강등하게 고쳤는데, **최종 종료 판정이 여전히 정본을 읽고 있었다.** 정본에는
설계상 `BASIN_HETEROGENEOUS` 가 남고 pm1/net4 는 **의도적으로 다른 magnetic
topology** 라, 둘 다 정상 수렴해도 그것이 뜬다. 즉 이 번들은 **성공할 수 없었다** —
외주가 16잡을 다 돌린 뒤에야 알았을 결함이다.

⇒ 판정을 `_final_verdict(cl, vc)` 로 빼서 **primary 뷰 하나만** 읽게 하고,
정상 pm1/net4 가 `exit 0` 인지 회귀시험으로 고정했다. 구판 결과(강등 뷰가 없는)는
정본으로 되돌아가 여전히 막힌다.

## 1. 조건별 이행

**② canary 부모 결측을 구조화 block 으로.**
box24 부모가 실패하고 nzmag canary 만 회수되면 `e1 - None` 으로 TypeError 였다.
`MOLECULAR_SPIN_CONTROL_PARENT_MISSING` 로 막고 차 계산을 건너뛴다.

**③ pooled 완전성 검사 + sensitivity 상태 단일화.**
지적대로 `not jr.get("ok")` 로 **먼저** 건너뛰어서 실제로 게이트된 잡이
`GATED_POSE` 에 **도달조차 못 했다**. net4 가 전부 게이트돼도 pm1 만으로
`secondary_G_citable=true` 가 됐다.
⇒ pool 을 `man["planned"]` 에서 세고, 결측·게이트·미해결이 하나라도 있으면
`pool_completeness.ok=False` 로 **pooled 값 전체를 비인용**으로 한다.
계획엔 있는데 회수 안 된 잡이 `_is()` 에서 조용히 새던 경로도 막았다.

**④ root seal·attestation 을 값까지 재계산 대조.**
· `SEAL_POTCAR_ROOT.sh` 의 기존-봉인 재대조가 source 집합과 allowlist 만 봤다.
  조립본 해시·MANIFEST·ZIP·VASP 신원이 바뀌어도 "대조 통과" 가 찍혔다 →
  **모든 불변량**을 다시 확인하고, 필드가 없으면 "반쪽 봉인" 으로 거부한다.
· 분석기가 `assembled_sha256_by_job` 의 **키만** 봤다 → 잡별 조립본 해시를
  **반송 provenance 의 실제 값**과 대조한다(`ROOT_SEAL_ASSEMBLED_MISMATCH`).
  반송에 그 값이 없으면 `..._UNVERIFIED` 로 막는다.

**⑤ 봉인한 절대 VASP executable 만 실행.**
봉인은 `VASP_EXE` 를 해시하는데 러너는 임의 `VASP_CMD` 를 실행했다.
⇒ launcher/executable 을 분리(`VASP_LAUNCHER` + `VASP_EXE`)하고 `VASP_CMD` 만
주면 **거부**한다. 실행파일을 절대경로로 해석하고, **잡 실행 직전에 다시 해시**해
봉인의 경로·해시와 대조한다.

**⑥ bundle-global lock · 실행 전 `files_sha256` 전수.**
lock 이 단계별이라 1·2 단계를 동시에 던질 수 있었다 → `.lock_bundle` 로 전역화
(RUNID 에 단계 기록). 그리고 실행 전에 배포 파일 **110개 전수**를 해시 대조한다 —
종전엔 잡 집합만 세어 INCAR 한 줄이 바뀌어도 통과했다.

**⑦ 외부 ZIP/MANIFEST digest anchor 강제.**
지적대로 ZIP 안의 해시는 자기 자신을 증명하지 못한다.
`EXPECT_MANIFEST_SHA256` · `EXPECT_ZIP_SHA256` 을 **선택에서 필수로** 바꾸고
`[0-9a-f]{64}` 형식을 강제하며, 현장이 계산한 `BUNDLE_ZIP_SHA256` 과 대조한다.
위 두 해시가 그 외부 anchor 다.

**⑧ 보고량 명칭·gas conformer provenance·낡은 claim 정리.**
manifest 에 `reported_quantity` 신설:
- name = **"fixed-geometry differential complex–gas reference energy"** (AS Q2 문구)
- 금지 이름 목록에 `adsorption energy` · `binding/free energy` · 옛 `E_ads`/`dE_site`
- 포함되는 것(조각·표면 변형, 고정 conformer 선택 효과)·제외되는 것
- `gas_conformer_provenance` — MLIP 로 고른 conformer 하나를 모든 자세에 공통 사용,
  선택 규칙, **평형 분자가 아니다**

**⑨ dense k 쌍 추가 + 셀 한정 사전등록.**
AS Q7 의 두 선택지 중 **lateral 대조가 아니라 셀 한정**을 택했다(옵션 b).
근거: 보고하는 것이 두 조각의 **차**이고 둘이 같은 셀·같은 피복률에 있으므로 공통
주기영상 항이 상당 부분 소거된다. lateral 확장은 원자수 2배(비용 ~4배·잡당 ~9일)라
이 단계 질문에 비해 과하다. **다만 말로만 두지 않고 수치를 실물에서 계산해 실었다**:

| 항목 | 값 |
|---|---:|
| lateral 면적 | 199.643 Å² |
| 피복률 | 0.5009 분자/nm² |
| 격자벡터(짧은 쪽) | 11.512 Å |
| **분자–주기이미지 최단** | **ptfe_c10 5.646 · sdcp_neutral 4.613 Å** |

⚠ **자체 정정**: v17 첫 생성에서 `min_image_distance_A` 로 11.512 Å 를 찍고 있었다 —
그건 **격자벡터 길이**이고, 회신 AS 가 준 4.89/5.65 Å 는 **분자–이미지 실제 최단
거리**다. 이름은 같은데 다른 양이고, 그대로 실었으면 리뷰 수치를 반박하는 것처럼
보였을 뿐 아니라 실제보다 여유가 있어 보여 한정의 근거를 약하게 만들었다.
둘을 분리하고 후자를 **복합체 POSCAR 에서 직접 계산**한다(8개 횡방향 이미지).
지금 값이 리뷰가 준 5.65 와 일치하고 SDCP 는 4.61 로 약간 다르다 —
어느 자세를 재셨는지 알려 주시면 대조하겠다.

k 수렴: primary pm1 두 잡에 **dense 상을 추가**했다(새 폴더가 아니라 phase —
같은 POSCAR·CHGCAR 승계라 k 외에 달라지는 것이 없다). manifest 에 `kconv_pair`
봉인, 분석기가
`δ_k = (E_sdcp,dense − coarse) − (E_ctl,dense − coarse)`, `|δ_k| ≤ 5 meV` 를 게이트한다.
결측·조각 미판별·미봉인은 전부 차단이다.

**⑩ 문서·러너·MANIFEST 숫자 정합.**
· **러너가 직렬인데 MANIFEST 는 `max_concurrency: 8`** 이라고 적고 있었다 —
  비용 추정이 그 병렬도 위에 서 있어 외주가 일정을 잘못 잡는다.
  ⇒ 러너가 실제로 병렬로 돈다(`xargs -P`). 단 canary 는 부모 최종 기하를 받으므로
  **두 물결**로 나누고, 앞 물결에 실패가 있으면 뒤 물결을 시작하지 않는다.
· stage-1 게이트를 문서가 4축으로 적고 있었다 → **8축**.
· SUBMIT 에 수치 게이트 표를 넣었다 — Δ_vac · δ_gas · δ_k 전부 5 meV 이고
  **조각별이 아니라 두 조각의 차**에 건다는 것을 같이 적었다.

## 2. 숫자

| | v16 | v17 |
|---|---:|---:|
| 잡 | 16 | 16 |
| 1단계 / 2단계 | 10 / 6 | 10 / 6 |
| **VASP 실행** | 16 | **18** (dense k 2) |
| stage-1 선결조건 | 8 | 8 |
| 배포 파일 | 106 | **110** |
| 생성기 selftest | 404 | **430** |
| 러너 실행 방식 | 직렬(문서는 동시 8) | **병렬 + 의존 물결** |

## 3. 여쭙고 싶은 것

**Q1.** 셀 한정(옵션 b)을 택했다. 분자–이미지 최단이 SDCP 4.61 Å 인데, D3 의
pairwise 항이 이 거리에서 두 조각에 **다르게** 들어올 여지가 얼마나 되나?
한정 문구만으로 충분한가, 아니면 D3 를 끈 단일점 한 쌍을 진단으로 붙여야 하나?

**Q2.** `δ_k` 문턱을 `δ_gas`·`Δ_vac` 과 같은 5 meV 로 잡았다. 세 게이트가 독립이
아니라면(같은 계·같은 조각) 각각 5 meV 를 통과해도 합이 커질 수 있다. 합에 대한
문턱을 따로 둬야 하나, 아니면 세 개를 하나의 오차 예산으로 묶어야 하나?

**Q3.** 러너 병렬화. canary 를 뒤 물결로 미는 것 말고 다른 숨은 의존성이 있나?
(dense 는 같은 잡 안에서 static 뒤라 잡 내부 직렬이다.)

**Q4.** 외부 anchor 를 필수로 만들었는데, 현장이 우리 메일의 해시를 그대로 붙여넣는
것 말고 **검증 가능한** 경로가 있나. 지금은 사람이 복사하는 단계가 남아 있다.

**Q5.** `pool_completeness` 를 도입하면서 pooled 값이 **더 자주** 비인용이 된다.
primary D(봉인된 네 잡)는 영향받지 않지만, secondary·pooled min 은 사실상 전 잡
완주를 요구한다. 이 엄격도가 맞나?

**Q6.** 이번에도 **결과를 보기 전에** 더 넣어야 할 잡이 있나. AR 의 box20,
AS 의 dense k 와 같은 종류의 판단이 남아 있는가?

## 4. 확인 방법

```bash
python3 tools/sdcp/vasp_handoff_bundle.py --selftest          # 430건
python3 tools/sdcp/vasp_handoff_bundle.py --verify_zip sdcp_c12_v17.zip --expect_jobs 16
cd <풀린 번들> && env -u PYTHONIOENCODING LC_ALL=C PYTHONUTF8=0 python3 analyze_results.py --selftest
```

파일은 수정하지 않으셔도 됩니다 — 판정만 주십시오.
