---
title: "리뷰 요청 BA — C-12 v21 (회신 AZ P0 7건 + P1 전건 이행)"
date: 2026-09-02
updated: 2026-09-02
tags: [review, codex, sdcp, c12, vasp, handoff, prompt]
status: 발송 대기
kind: review-request
system: sdcp
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 BA — `sdcp_c12_v21.zip`

> 이전 회신: 회신 AZ (NO-GO · P0 7건 · P1 5건 · Q1–Q6)
> **VASP 는 여전히 한 잡도 돌리지 않았습니다.**

```
ZIP      c9950d4a98506a9d6b6e02200c358a7c85ab716a3aa07a76b3d2f1384ee38e09
MANIFEST bbbdb3cd9e5776421343878475e3f9c6532185b2f7dba9dec517472e0d00fcaf
생성기   68412a416df4c0be14bac5ae1935db638532c8ce6df0261016c3f65fdf96531e
배포 분석기 28b13b061b064e63d2dd601bf34f167ed79bc296fc8968859071b9c68dd49a48
커밋     69844dc8d34d2e3314b0961175eed193f45e89d4   ·   git_dirty false
```

⚠ 번들 안에는 `git_branch: b2o3run` 으로 찍힙니다 — 생성 기계의 로컬 브랜치 이름입니다.
**커밋 해시가 같으므로 내용은 동일**하고, `claude/friendly-meitner-lldvar` 의 69844dc8 을
받으셔도 바이트가 같습니다.

생성 인자는 v20 과 같고 `--potcar_identity post_hoc` 만 **명시적으로** 추가했습니다
(기본값과 같은 값이지만 정책이 산출물에 남게 하려고 적습니다). 잡은 **16개 그대로** —
회신 AZ Q6 그대로 늘리지도 줄이지도 않았습니다.

## 0. 먼저 — 지적하신 P0-1 은 저희가 리뷰에 쓴 문장이 거짓이었던 건입니다

회신 AZ 프롬프트(요청 AZ)에 저희는 *"러너는 **PATH 조회를 폐기**하고 봉인된 절대경로만
씁니다"* 라고 적었습니다. **run_job.sh 쪽만 그랬고 봉인을 만드는 run_staged.sh 는
그대로였습니다.** 그리고 그 run_job.sh 패치조차 봉인 파일 경로를 틀리게 적어
(`POTCAR_ROOT_SEAL.json` ← 실물은 `../../…`) **16잡이 전부 첫 줄에서 죽는** 상태였습니다.

selftest 300건이 통과한 이유는 명확합니다 — **기존 러너 회귀가 정상 실행 경로를 한 번도
지나지 않았습니다.** 언제나 `.SELFTEST_FIXTURE`(봉인 조회 블록 통째로 건너뜀) +
`VASP_LAUNCHER_KIND=none`(mpirun 분기 통째로 건너뜀) 이었습니다.

## 1. P0 7건

### P0-1 실행 경로 — 경로 일원화 + **정상 경로 e2e 회귀 신설**

- 봉인 경로를 `_SEAL` 변수 **하나**로 묶었습니다 (두 벌이면 또 갈라집니다).
- `_runner_launcher_regression` 신설: **픽스처 표시 없이**, 실제 봉인 파일을 놓고,
  `KIND=mpirun` 으로 `run_job.sh` 를 **끝까지 돌립니다**. 영수증이 8열로 실제로 쓰이고
  kind·launcher 경로·해시가 봉인과 같은지까지 봅니다.
- 음성 4: 봉인에 launcher 없음 · 봉인 파일 없음 · `LAUNCHER_BIN` 이 봉인과 다름 ·
  launcher 를 **도중에 교체**(상 직전 재해시가 잡는지).
- ⭐ 원래 오타를 되돌리면 이 시험이 `rc=1 · 상 []` 로 잡는 것을 확인했습니다.

### P0-2 봉인 시점 PATH 우회 — 세 곳 전부

- `VASP_EXE`·`LAUNCHER_BIN` 을 **절대경로로만** 받습니다. PATH 에서 찾아 주지 않습니다.
- SEAL 재대조 **불변량**에 `launcher_kind`/`launcher_path`/`launcher_sha256` 를 넣었습니다
  — 종전엔 봉인에 **쓰기만** 하고 대조 목록엔 없어서, 지적하신 대로 seal 이 `mpirun` 인데
  다음 단계가 `kind=none` 이어도 통과했습니다.
- 분석기가 receipt 의 **kind·path** 를 봉인과 대조합니다. kind 를 바꿔 launcher 해시
  검사를 통째로 건너뛰던 경로를 닫았습니다.

### P0-3 진공 판정 — MANIFEST 를 코드에 맞췄습니다

hard gate 는 `|Δ_vac| ≤ 5 meV` **하나**입니다. `same_rounded` 는 표시 안정성 정보로
분리했습니다. (AY P0-3 에서 docstring 만 고치고 이 문자열을 놓쳤습니다.)

### P0-4 `E_ads` — 성분 균형 정정

주신 형태로 닫았습니다.

```
E_ads(f)  = E_C(f) − E_S − E_G(f)      [정의 — 이 묶음은 산출하지 않습니다]
ΔE_ads    = [E_C(sdcp) − E_G(sdcp)] − [E_C(ptfe) − E_G(ptfe)]   [이것만 보고합니다]
```

공통 `E_S` 가 ΔE_ads 에서 소거되므로 **clean-slab 추가 잡은 불필요**합니다(잡 수 불변).
보고량 이름을 **ΔE_ads** 로 바꿔 개별값이 산출물처럼 읽히던 내부 모순도 닫았습니다.

### P0-5 `overall_citable=None` 우회

- `reported_X_eV` → **`rounded_value_under_tested_axes_eV`** (범위를 필드명에 박음)
- `reported_X_eV` 는 `overall_citable_at_0.01eV is True` 일 때만 값이 나옵니다 —
  지금은 언제나 `None` 입니다.
- 방향 판정도 **`보고 가능 (시험한 축 조건부)`** 로 바꾸고 `verdict_scope` 를 붙였습니다.

### P0-6 거버넌스 — 간선 제거 · 원장 fail-closed · 🔴 **비준은 아직**

- 좁은 C-12 estimand 노드가 전역 마감정책을 supersede 하던 **간선을 제거**했습니다.
- ⚠ 되돌려 보니 그 전역 정책은 **사람 승인 기록이 한 번도 없었습니다.** `superseded`
  상태가 그 사실을 가리고 있었습니다. 그래서 `active` 가 아니라 **`proposed`** 로 뒀습니다.
- 원장 fail-closed 신설: 상태 enum · 필드 타입 · 중복 id · 적재 누락 ·
  **좁은 노드→전역 정책 supersede 금지** · **non-policy→policy supersede 금지**. 음성 5건.
- 🔴 **비준 자체는 아직입니다.** 지적하신 대로 비용 발생 전에 닫는 것이 맞다고 보고,
  1저자 비준 전에는 발송하지 않습니다.

### P0-7 POTCAR — 🔴 **1저자가 판정을 알고 `post_hoc` 을 선택했습니다**

주신 두 길(pin / 생산 전 attestation 필수) 대신 **README 권고**로 가기로 1저자가
두 번 재확인해 결정했습니다. 저희가 판정을 전달하지 않아서가 아니라, 전달한 뒤의
결정입니다. 기계는 두 길 모두 준비돼 있습니다(`--potcar_pin`, `--potcar_identity
require_attestation`) — 지시가 오면 인자만 바꾸면 됩니다.

그 선택의 **대가를 산출물이 집니다**:
- `potcar_identity_policy.manuscript_citable = false`
- `현재_판정: ⛔ **탐색용** — 원고 인용 불가 (승인 dataset 확인 없음)`
- Methods 필수문장(ko/en): *"…해당 트리의 공식 배포판 여부는 본 연구에서 독립 확인하지
  않았다."*
- `1저자_결정_2026_09_01` 에 **리뷰어 판정을 알고 고른 것**임을 기록 — 누락과 결정을
  산출물에서 구분할 수 있어야 한다고 봤습니다.
- README 에 권고를 넣되 **막지 않습니다**: 왜 부탁하는지와 안 하면 어떻게 되는지를
  같이 적었습니다.

## 2. P1 전건

- `ALLOW_RESUME=1` 이 receipt 를 **새 헤더로 덮어써** 완료 상의 행이 사라지고 결국
  `RECEIPT_PHASE_MISSING` 이 났습니다 — 정직하게 이어 돌린 사람이 "러너 밖에서 돌렸다"
  판정을 받는 구조였습니다. 재개는 **이어 쓰고** `_runner_resume` 으로 구분합니다
  (`_runner_start` 는 여전히 정확히 하나). 재개 시 실행파일·kind 가 봉인과 같은지도 봅니다.
- `_runner_start` 헤더의 **내용**(시각 형식·exe·kind)도 검증합니다. 종전엔 개수만 셌습니다.
- 같은 상이 두 번 찍히면 `RECEIPT_PHASE_DUPLICATE`.
- attestation 안내 파일명 대소문자 정정.
- **"두 complex 의 슬랩 조성이 다르다" 는 거짓**이었습니다 — 둘 다 `Li48 Ni48 O96`,
  192원자로 같습니다. 결론(주기영상 소거 미주장)은 유지하고 **이유를 정정**했습니다:
  비소거 위험은 복합체 **전체 조성·기하와 주기영상 항이 조각마다 다른** 데서 옵니다.
- D3 단서를 코드 주석뿐 아니라 **결과 객체**에 실었습니다 (`closure_C3.⚠_C3_가_무엇인가`,
  ko/en + VASP IVDW 문서 링크). C3 는 **exact-cell Δ 에 대한 전체 D3 기여**이지
  fragment–slab pair 분해가 아니라는 문구입니다.

## 3. 검증

```
verify_zip        PASS · rc 0
배포본 selftest   301/301 PASS      (v20 300 · v19 294)
신설 e2e          정상 launcher 경로 (양성 1 + 음성 4) — 이 시험이 P0-1 을 잡는다
webapp            141 passed · 원장 위반 0
```

## 4. 여쭙는 것

**Q1.** P0-1 이 이번엔 실제로 닫혔습니까? 정상 경로 e2e 를 넣었지만, 그 시험이 여전히
**저희가 상상한 경로**만 지날 수 있습니다. 실행 경로에서 아직 시험이 안 닿는 곳이 보이십니까?

**Q2.** P0-2 에서 "가짜를 최초 봉인" 경로는 절대경로 강제로 좁혔지만, 봉인을 **외주처가
만드는** 구조 자체는 그대로입니다. 이것은 위협모델 밖입니까, 아니면 사전 승인된 launcher
지문이 필요합니까? (회신 AZ Q1 의 재확인입니다.)

**Q3.** P0-4 의 ΔE_ads 정의와 "개별 E_ads 미산출" 이 원고용으로 닫혔습니까?
`E_S` 소거 논증을 MANIFEST 에 적었는데, 그 논증 자체에 구멍이 있습니까?

**Q4.** P0-5 에서 `reported_X_eV` 를 **overall True 일 때만** 내도록 했습니다. 지금은
영영 `None` 이므로 사실상 그 필드가 죽은 셈인데, 아예 **제거**하는 편이 낫습니까?
(남겨 두면 나중에 되살아날 자리가 됩니다.)

**Q5.** P0-7 의 1저자 결정(post_hoc + README 권고)이 **탐색용 번들로서는** 성립합니까?
저희가 붙인 라벨(`manuscript_citable=false` · Methods 필수문장)로 충분합니까,
아니면 탐색용조차 막아야 할 이유가 있습니까?

**Q6.** 거버넌스 비준 전에는 발송하지 않을 계획입니다. 비준 **외에** 발송 전 닫아야 할
것이 더 있습니까?

**Q7.** 이번에도 결과를 보기 전에 더 넣거나 뺄 잡이 있습니까?

파일은 수정하지 않으셔도 됩니다 — **GO/NO-GO 와 P0/P1** 판정만 주십시오.
