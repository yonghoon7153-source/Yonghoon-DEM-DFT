---
title: "리뷰 요청 BB — C-12 v22 (회신 BA 해제조건 8건 + 거버넌스 비준)"
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

# 리뷰 요청 BB — `sdcp_c12_v22.zip`

> 이전 회신: 회신 BA (NO-GO · P0 4건 · P1 7건 · GO 해제조건 8건)
> **VASP 는 여전히 한 잡도 돌리지 않았습니다.**

## 0. 해시

배포물 (생성 기계에서 직접 계산):
```
ZIP      90b7596c02c8f65895faafb96ef37dda23aef8ed5a37ba50b7488374c87476a9
MANIFEST 7684207e459fa66e6b8c5e33d5526ecc7b5cb0e7265b214c3fd70521671b07c4
분석기   d1986efe6928fbf99493f42716947109441d169167d6e370825ac73e3fdf25bb
```

repo 파일 (**커밋된 트리에서** — `tools/review_manifest.py` 가 `git show <commit>:<path>` 로 계산):
```
tools/sdcp/vasp_handoff_bundle.py                    d7b55c6c4b60c0a611a1dd601f075d316300a568458ce72f7602646de712297a
db/properties/sdcp_c12_claim_prereg_2026_08_31.json  9659c0c92ae55306711d8b974ede6ef34302f66a94a3eb7373720a5029088b9e
db/properties/sdcp_c12_protocol_2026_08_30.json      8cb150221235a605be015af26f4f6e1952820ab7a0dd20c3fc83da270e39bf39
db/governance/decisions.json                         90632dbe35c78b29416f74e93ccb439f026bde528d64e3a5675364b007b16458
커밋                                                   97cb2d4d3bcd73b96d6168cc977c8ea8e624b761   (원격에 있음)
```

### 🔴 먼저 말씀드릴 것 — 생성 기계의 작업 트리가 dirty 였습니다

회신 V P0-1 이후 저희는 리뷰 해시를 **커밋된 트리에서만** 뽑는 도구
(`tools/review_manifest.py`)를 만들었고, 그 도구가 **이번에 생성 기계에서 거부했습니다**:
작업 트리가 dirty 라 재현되지 않는 표가 나올 상황이었습니다.

- 확인된 것: 생성 기계가 보고한 prereg·protocol SHA(`9659c0c9…`·`8cb15022…`)가
  커밋 `97cb2d4d` 의 값과 **정확히 같습니다** ⇒ 그 두 파일은 커밋본과 동일합니다.
- 아직 모르는 것: 생성 기계의 **생성기 SHA** 가 커밋본 `d7b55c6c…` 와 같은지,
  그리고 무엇이 dirty 인지 (추적 파일인지 untracked 인지).

⇒ **추적 파일이 수정돼 있었다면 이 v22 는 폐기하고 v23 으로 다시 만듭니다.**
그 확인 전에는 이 묶음을 외주처로 보내지 않습니다. 위 표에서 배포물 세 해시는
실물에서 잰 값이고, repo 네 해시는 커밋에서 잰 값입니다 — 둘을 잇는 고리가
생성기 SHA 하나이고 그것이 지금 미확인입니다. 숨기지 않고 적습니다.

## 1. 해제조건 8건

| # | 조건 | 처리 |
|---|---|---|
| 1 | ZIP 밖 SHA 대조 + 배포 스크립트보다 먼저 추출 파일 검증 | census 를 SEAL **앞으로**. 봉인 검사만 뒤(`RECHECK_SEAL=1`). README 0단계 신설 |
| 2 | prereg·protocol 을 ΔE_ads 정의로 정정 | 둘 다 `E_C − E_S − E_G`, 개별값 미산출 명시 |
| 3 | decision 비준 + 참조 SHA·digest 결박 | `governance_binding` 신설 · **1저자 비준 완료** |
| 4 | `manuscript_citable=false` 기계 집행 | `citation_status()` 신설 · README 문구 삭제 |
| 5 | 범위 없는 숫자 필드 제거 | `diagnostic_only` 로 이동 · `reported_X_eV` 제거 |
| 6 | J_f 코호트 수정 | 고르는 술어 = 세는 술어 |
| 7 | 재개 계약 통과 가능하게 or 폐지 | **폐지** · dense 승격만 분리 |
| 8 | attestation 스키마·절대경로·release 앵커 | 스키마 일치 · PATH 폐기 · 자기선언 label 승격 차단 |

### ① 실행 순서 — 지적이 정확했습니다

`run_staged.sh` 가 SEAL 을 먼저 부르고 SEAL 이 16개 `POTCAR_ASSEMBLE.sh` 를 실행하는데
`EXPECT_*`·`files_sha256` 검사는 그 **뒤**였습니다. 변조 assembler 가 무결성 검사 **전에**
실행되는 구조였습니다.

census 를 SEAL 앞으로 옮기고, 봉인 검사만 SEAL 뒤 두 번째 census 로 미뤘습니다
(`RECHECK_SEAL=1` 로 **같은 코드**를 두 번 돌립니다 — 검사 로직이 갈라지지 않습니다).
README 에 0단계를 신설해 **ZIP 을 풀기 전에 ZIP 밖에서 SHA 를 대조**하도록 적었습니다.

### ③ 거버넌스 — 계산 전에 비준했습니다

1저자가 2026-09-02 세 건을 함께 비준했습니다:
`D-2026-08-28-closure-criteria-first` · `D-2026-08-30-sdcp-c12-path` (둘 다 → `active`),
`sdcp_polaron_pilot_prereg_S0_*.json` (→ `ratified`).

각 기록에 `actor_id`·`timestamp`·`commit`(40-hex)·**내용 digest**(= `ratification` 을 뺀
내용의 sha256)를 넣었습니다. 비준 뒤 내용을 고치면 검사가 재승인을 요구합니다.

⚠ 그 결박이 즉시 작동했습니다 — 처음에 digest 를 상태 변경 **전에** 계산했더니
검사가 두 건 다 "승인 이후에 내용이 바뀌었다" 로 잡았습니다. 순서를 바로잡아
(내용 확정 → 지문 → 비준 부착) 0 위반이 됐습니다.

번들의 `MANIFEST.governance_binding.all_ratified = True` 로 확인됩니다.

### ⑥ J_f — 우리 코드가 스스로 금지한 것을 하고 있었습니다

`_pick` 은 구조화 meta 로 고르는데 기대 수는 **잡 키 문자열**(`endswith`)로 셌습니다.
"이름 파싱 금지" 는 같은 파일의 다른 자리에 저희가 적어 둔 규칙입니다. 같은 술어로
세도록 고치고, 어긋나면 `required_keys`·`used_keys`·`예상밖`·`누락` 을 함께 냅니다.

### ⑦ 재개 — 폐지했습니다

지적하신 대로 `_runner_resume` 자체가 `RECEIPT_RESUMED` 게이트가 되고 중단 상
재실행은 `PHASE_DUPLICATE` 라 **언제나 막혔습니다** — 있으나 마나가 아니라 함정이었습니다.
attempt ID·supersedes 를 도입하는 것은 이 묶음의 질문에 비해 과하다고 보아 폐지했습니다.
dense 승격만 성격이 달라 `PLANNED_CONTINUATION` 으로 이름을 갈랐고, **DENSE_PLAN.json 을
증거로 요구**합니다.

## 2. 우리가 이번에 저지른 것 (숨기지 않습니다)

1. **직전 커밋에 회귀를 실었습니다.** 주석에 쓴 ASCII 작은따옴표가
   `xargs … sh -c '…'` 문자열을 조기 종료시켜, 잡 경로가 `_` 로 들어가고
   **영수증이 한 건도 안 써졌습니다.** selftest 는 잡아냈는데 저희가 `✗` 만 grep 하고
   **종료코드를 안 봤습니다** — 그 실패는 `⛔ ` 접두어를 씁니다. 이제 rc 로 확인합니다.
2. J_f 를 고치니 selftest 의 `planned` 가 **meta 를 안 싣는다**는 것이 드러났습니다.
   같은 파일 11345행에 "픽스처≠실물" 함정을 저희가 이미 기록해 뒀는데 또 밟았습니다.

## 3. 검증

```
verify_zip                      PASS · rc 0
생성기 selftest                 rc 0
governance_binding.all_ratified True
webapp                          141 passed
원장 위반                        0
잡                              16 (변동 없음 — 회신 BA Q7)
```

## 4. 여쭙는 것

**Q1.** 해제조건 8건이 닫혔습니까? 특히 ①(실행 순서)에서 census 를 두 번 돌리는
방식이 맞습니까, 아니면 봉인 검사를 아예 별도 스크립트로 빼야 합니까?

**Q2.** ③ 의 결박이 충분합니까? `governance_binding` 은 생성 시점의 decision digest 를
박습니다만, **회수 시점**에 원장이 바뀌었는지는 분석기가 보지 않습니다. 그 대조도
필요합니까?

**Q3.** ⑦ 에서 재개를 폐지한 판단이 적절합니까? 아니면 attempt ID 를 도입해서라도
지원해야 하는 상황이 있습니까? (16잡 · 각 수 시간이라 한 번에 완주가 현실적이라고 봅니다.)

**Q4.** ⑧ 에서 자기선언 `release_label` 을 외부 앵커 없이는 승격하지 않게 했습니다.
다만 **앵커가 있어도 label 문자열 자체는 검증하지 못합니다** — 앵커는 바이트를
결박하지 이름을 결박하지 않습니다. 그 한계를 시험으로 박아 뒀는데, 이 정도로
정직하면 됩니까, 아니면 label 필드를 아예 없애야 합니까?

**Q5.** §0 의 dirty 트리 건 — 생성기 SHA 가 커밋본과 다르면 v22 를 폐기하는 것이
맞습니까? 아니면 다른 처리가 있습니까?

**Q6.** 이번에도 결과를 보기 전에 더 넣거나 뺄 잡이 있습니까? (회신 BA Q7 은 16잡
유지를 권했고, 저희는 그대로 뒀습니다.)

파일은 수정하지 않으셔도 됩니다 — **GO/NO-GO 와 P0/P1** 판정만 주십시오.
