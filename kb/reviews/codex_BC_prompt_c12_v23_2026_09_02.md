---
title: "리뷰 요청 BC — C-12 v23 (회신 BB P0 6건 + P1 6건 이행 · clean tree 재생성)"
date: 2026-09-02
updated: 2026-09-02
tags: [review, codex, sdcp, c12, vasp, prompt]
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

# 리뷰 요청 BC — C-12 v23

> 이전 회신: 회신 BB (NO-GO · P0 6건 · P1 6건 · Q1–Q6)
> **VASP 는 여전히 0잡입니다.**

```
sdcp_c12_v23.zip                                     e3b2cafbf1049a24d44dfccb74f7951c7b56389487caa2e580cca36f32463591
MANIFEST.json                                        d874583a3d1c6fb59b9d55a434e84bde288587a09f8119d1518024a4713a3e0f
analyze_results.py (번들 안)                          69c46cfaf09d6cc34dd5b00cb11a269662a60f3e9becc9d2bf91782e5d8b81af

tools/sdcp/vasp_handoff_bundle.py                    896a38060404c035441f619a2a9180995c2722ddf0c1bd88be1d069da634e5d9
db/properties/sdcp_c12_claim_prereg_2026_08_31.json  5bc7afbcc45eedc7e94ecd4070c4ace08c8b3aa86ccdd3d629e538be008a6aa3
db/properties/sdcp_c12_protocol_2026_08_30.json      0b1c0a9893b96f17577ba2328648de89e60e94267ebcf9dbe68e2ac7c7882109
db/properties/c12_poses_2026_08_30.json              547544cc8b84b188100495f67f85b5565a3594f81afa0ce03a527e1f57a29df8
커밋                                                  ac06a675340a4aad4b6b69ebee7389aca4a4dee4   (원격 있음)
selftest                                             559건 PASS   (BB 시점 310)
verify_zip                                           PASS · rc 0 · 잡 16
```

repo 해시는 `tools/review_manifest.py --require_pushed` 가 **커밋된 트리에서만** 낸
것이고, 생성기 SHA 는 생성 기계에서 실측한 값(`896a3806…`)과 일치합니다.

## 0. Q5 대로 **clean tree 에서 재생성**했습니다

P0-5 판정("범위를 증명하지 못해도 clean tree 재생성이 안전하다")을 그대로 따랐습니다.

- 생성 기계의 작업 repo 는 브랜치 `b2o3run` · **dirty 534건** 이었습니다. v22 가
  거기서 나왔으므로, 말씀대로 **v22 는 폐기**합니다.
- v23 은 그 repo 를 건드리지 않고 `git worktree add --detach` 로 커밋 `ac06a675`
  의 **분리된 clean 트리**를 만들어 거기서 생성했습니다
  (`git status --porcelain` = 0). attestation 의 `git_dirty: false` 가 그 사실입니다.
- 그 위에 **번들이 스스로 계보를 담습니다** — 아래 P0-5.

## 1. P0 이행

### P0-1 — 완주하면 반드시 NameError 였다

지적이 정확했습니다. `res["citation_status"]` 의 `res` 는 그 스코프에 없습니다.
그리고 지적하신 두 번째 층이 더 중요했습니다: **RESULTS.json 을 그 앞에서 저장**
하므로 이름만 고쳐도 판정이 파일에 안 남고, 중간 `return 2` 경로가 여럿이라
그 경우에도 안 남았습니다.

⇒ 판정을 **저장 전으로** 옮기고, 뒤쪽은 출력·종료코드만 합니다.

⇒ **완주 e2e 를 신설했습니다.** 기존 e2e 는 **언제나** 음성을 심고 돌려
`required_missing` 에서 `exit 2` 로 빠졌습니다. 그래서 selftest 310건이 main() 의
마지막 구간을 **한 번도** 지나지 않았습니다. 이제 음성을 심기 **전** 스냅샷으로
끝까지 돌려 ⓐ 예외 없음 ⓑ `citation_status` 가 RESULTS.json 에 있음
ⓒ post_hoc 이라 `manuscript_citable=false` ⓓ 화면에 인용 자격 절이 찍힘 을 봅니다.

(회신 AZ P0-1 과 같은 형태입니다 — 정상 경로를 시험이 지나지 않으면 통과 개수는
아무것도 보증하지 않습니다. 두 번째입니다.)

### P0-2 — SHA 를 적은 것은 비준의 증거가 아니다

맞습니다. decision 두 건만 세어 `all_ratified=true` 였고, 정작 주장을 정의하는
문서는 그 집합 밖이었습니다 — claim prereg 는 `proposed`, protocol 은 **status 필드
자체가 없었습니다**(`지위` 칸에만 적혀 있어 한 칸만 읽으면 놓칩니다).

⇒ `reference_files_state` 를 싣고 종합 판정에 넣습니다. 상태 칸은 `status` 와
`지위` 둘 다 봅니다.

⇒ **1저자가 두 문서를 비준했습니다** (2026-09-02, DFT 0잡 시점).
`ratification.content_digest` = `ratification` 을 뺀 내용의 sha256 이라, 이후 한
글자라도 바뀌면 게이트가 재승인을 요구합니다.

⚠ **한 건은 비준하지 않았습니다.** `c12_poses_2026_08_30.json` 은 자세 집합
**데이터**(`freeze_sha256` 로 동결)이지 주장 문서가 아닙니다. 데이터 파일에 비준을
요구하면 고무도장이 되고, 그러면 "비준" 이라는 말이 아무것도 뜻하지 않게 됩니다.
⇒ 참조를 `claim`(사람 비준 필요) / `frozen_input`(내용 결박만) 으로 갈랐습니다.
**이 구분이 타당한지 Q2 에서 여쭙니다.**

### P0-3 — 요약 불리언을 믿어 fail-open

재현하신 그대로였습니다. 이제 항목마다 `state`·`ratified`·`digest`·`digest_matches`
를 직접 보고, **요약이 개별 항목과 어긋나면 그 자체가 차단 사유**입니다(요약만
고쳐 놓는 경로를 닫습니다). 음성 6건 — state=proposed · ratified=false ·
digest=BROKEN · 비준 후 내용 변경 · 요약 불일치 · decisions 를 비우면 통과하던
`all(빈 것)=True`.

base_commit 과 내용 앵커도 갈랐습니다. 비준의 `commit` 은 **비준을 누른 시점의
HEAD** 이지 그 digest 가 가리키는 내용이 있는 커밋이 아닙니다(실측: 두 비준 모두
`2f96eeb…` 인데 active 내용은 `97cb2d4…` 에 있었습니다). 이제
`ratification_base_commit` / `recorded_digest` / `digest_matches` 로 나눠 싣고,
"base_commit 은 내용 앵커가 아니다" 를 산출물에 적었습니다.

### P0-4 — provenance 가 폐기된 사전등록을 가리켰다

`prereg_closure.prereg_doc` 이 `prereg_sdcp_neutral_contrast_2026_08_29.json` 을
가리키고 있었습니다. 그 문서는 스스로 `지위: ⛔ SUPERSEDED` 라고 적혀 있습니다.

⇒ C-12 정본 두 건(claim prereg + protocol §2b)을 가리킵니다. 계보는
`superseded_origin` 으로 남깁니다 — 그 문서의 **실측 기록**(UMA–DFT 오프셋 등)은
여전히 유효하고 폐기된 것은 estimand 이지 관측이 아니기 때문입니다.

⇒ 참조 문서 판독이 SUPERSEDED/철회/폐기 문자열을 `status` 뿐 아니라 `지위` 같은
다른 칸에서도 찾습니다(이 파일은 `status` 에 없었습니다). 폐기 문서는 **비준해도**
인용 자격을 주지 않으며, 미비준과 **다른 사유**로 말합니다.

### P0-5 — 생성 계보가 번들 안에서 닫히지 않았다

MANIFEST 에는 실행한 생성기의 SHA 조차 없었습니다(검증 attestation 에만).

⇒ `provenance_closure()` 를 만들어 MANIFEST 에 싣습니다: 실행 중인 생성기 +
repo 안에서 import 된 모든 모듈 + 등록된 입력의 sha256 과 **git 추적 상태**.
dirty 나 `unknown` 이 하나라도 있으면 `clean=false` 이고 **분석기가 인용을
막습니다**. `provenance` 가 **없는** 구판 번들도 막습니다(v22 가 그 상태입니다).
`unknown` 을 clean 으로 세지 않습니다 — 모르는 것을 통과시키면 그게 fail-open 입니다.

v23 실측: `clean=True · 파일 4 · dirty 0 · 미상 0`.

⚠ **한계를 숨기지 않겠습니다.** 폐포에 잡힌 4개는 생성기와 import 된 repo 모듈뿐
입니다. `_prov_note()` 훅은 만들었지만 생성기가 아직 **입력을 등록하지 않습니다**.
즉 입력 구조 파일은 이 폐포 안에 없습니다. 지금 입력을 덮는 것은 두 가지입니다:
ⓐ `governance_binding.reference_files_sha256` (자세 집합 등 참조 문서)
ⓑ **트리 전체가 clean 이었다는 사실** (`git status --porcelain` = 0 ·
attestation `git_dirty: false`). ⓑ가 더 강한 진술이라고 보지만, 번들 **내부**
에서 닫힌 것은 아닙니다. **Q1 에서 여쭙니다.**

### P0-6 — 바이트 앵커는 이름을 인증하지 않는다 · 증서 검증이 생산 후였다

두 지적 모두 맞습니다.

**이름**: BA P0-3 에서 `potcar_pin.source_sha256` 만 있으면 `paw_release_attested`
로 올렸는데, 그 pin 은 *우리가* 적어 둔 바이트 지문이라 "이 바이트가
potpaw_PBE.54 다" 는 말하지 못합니다. Q4 대로 고쳤습니다 — pin 이 label 을 함께
담고, 그것이 현장 신고와 같고, pin 의 SHA map 이 attestation variant 를 **전부**
덮을 때만 이름을 주장합니다. 아니면 이름은 `site_reported_release_label`
메타데이터로만 남습니다. 판정 근거는 `release_label_anchor_detail` 에 적습니다.

⚠ 종전 시험은 **이 구멍을 통과 조건으로 박아** 두고 있었습니다("앵커가 있어도
label 은 검증 못 한다"). 시험을 뒤집었고, 같은 `FAKE_RELEASE` 재현이 이제
차단됩니다.

**순서**: `run_staged.sh` 는 `made_before_production` 과 SHA map 둘만 봤고 나머지는
분석 단계에 가서야 봤습니다. 검사 **사본**을 걷고 정본
(`analyze_results.py --check_attestation`)을 부릅니다 — 사본은 언젠가 정본과
갈립니다(BA 해제조건 8 이 그 사고였습니다: 사본이 없는 키
`sealed_before_production` 을 요구해 정상 증서를 거부했습니다).
⚠ 그 사본을 지키던 시험은 **주석 문자열**을 잡고 있었습니다 — 행동을 보게 바꿨습니다.

## 2. P1 이행

- **J_f** — 지적대로 고르는 술어와 세는 술어가 달랐습니다. **세 자리**였습니다:
  ⓐ J_f(`pose_basin_interaction`)는 선택이 `ALT_ROLES` 를 빼는데 기대는 잡 키를
  `split("__")[1]` 로 파싱해 대안 자세까지 셌습니다(정상 2자세×2seed 에서도
  `used=1/required=2`). ⓑ C3(Edisp)는 `startswith("prospective/")` 이름 파싱에
  d3-off 쌍둥이를 기대에만 넣었습니다. ⓒ C1 은 BA P1 에서 이미 고쳤습니다.
  ⇒ `_expected_pose_keys()` **helper 하나**로 합치고, 어긋나면 **어느 자세가**
  어긋났는지 남깁니다(required/used/누락/예상밖).
- **README** — `ALLOW_RESUME=1` 지시를 걷었습니다(러너는 거부합니다). 실패 잡은
  **별도 rescue 묶음**(parent/supersedes 명시)으로 처리한다고 적었습니다(Q3).
  실행 순서도 실물대로 정정: census → 조립+봉인 → 봉인 census → 단계.
- **census 사본 두 벌** — 바이트가 같은 122줄이 두 벌이었습니다. 번들에
  `census.py` **하나**를 넣고 러너가 두 번 부릅니다(`RECHECK_SEAL=1` 로 구분).
  그 파일 SHA 는 `files_sha256` 에 있어 무결성 검사가 변조를 잡습니다.
- **DENSE_PLAN** — 존재 여부만 보던 것을 계약대로 바꿨습니다: ① 이 잡이 promote
  목록에 있는가 ② dense 가 아직 안 돌았는가 ③ 실제로 도는 상이 dense 하나뿐인가.
  완료 상 건너뛰기도 계획된 이어달리기에서만 허용합니다(종전엔 무조건이었습니다).
  ⚠ 옛 픽스처가 `{"planned": true}` 라 **"파일만 있으면 통과" 계약을 시험이
  굳히고** 있었습니다.
- **잡 수·census 분류** — census 가 **잡 키 접두어**로 나눠 vacconv 가 references
  로 세어졌습니다. `meta.kind`·`meta.vacconv` 로 셋을 갈랐고, meta 가 없으면
  **모른다**로 셉니다(추측이 통계가 되지 않게). v23 실측:
  **refs 6 · vacconv 2 · 자세 8 · 미상 0 = 16**.
  protocol 의 12·19 는 `⛔_잡수_정정_2026_09_02` 한 칸에 정정했습니다 — 원안
  숫자는 지우지 않습니다(그때의 계획이라 이력이고, 지우면 왜 16이 됐는지가
  사라집니다).
- **300 h · 재개 폐지** (Q3) — rescue 묶음 경로를 README 에 적었습니다. 다만
  **아직 생성기에 구현하지 않았습니다** (parent/supersedes 필드를 포함한 rescue
  번들 모드). 실패가 나기 전에 만들어야 하는지 Q4 에서 여쭙니다.

## 3. 아직 **안** 한 것

1. **입력을 폐포에 등록하지 않았습니다** (`_prov_note` 훅만 있습니다) — 위 P0-5.
2. **rescue 번들 모드 미구현** — README 에 약속만 적혀 있습니다.
3. **VASP 0잡** — 이 번들로 아무것도 돌리지 않았습니다.
4. POTCAR 는 여전히 `post_hoc` 입니다(1저자가 세 번 재확인). 따라서 이 묶음의
   결과는 **영구 탐색용**이고 `manuscript_citable=false` 입니다. 그 선택과 대가가
   산출물에 같이 남습니다.

## 4. 여쭙는 것

**Q1.** P0-5 의 남은 반쪽입니다. 지금 입력을 덮는 것은 ⓐ governance_binding 의
참조 문서 SHA ⓑ 생성 시 트리 전체가 clean 이었다는 사실뿐이고, **번들 내부의**
폐포에는 입력이 없습니다. ⓑ("clean 트리에서 만들었다")로 충분합니까, 아니면
`_prov_note` 를 실제로 걸어 입력 파일까지 폐포에 넣어야 v23 이 유효합니까?
후자면 v24 를 만들겠습니다.

**Q2.** 참조를 `claim`(사람 비준) / `frozen_input`(내용 결박만) 으로 가른 것이
타당합니까? 저희 논거는 "데이터 파일에 비준을 요구하면 고무도장이 되어 비준이
아무것도 뜻하지 않게 된다" 입니다만, 반대로 **자세 집합이야말로 estimand 를
정의하므로 비준 대상**이라는 읽기도 가능하다고 봅니다.

**Q3.** P0-1 과 AZ P0-1 은 같은 형태였습니다 — *"정상 경로를 시험이 지나지
않는다."* 이번에 완주 e2e 를 넣었지만, **아직 안 태워 본 경로**가 또 있다고
보십니까? 저희가 아는 것: `run_staged.sh` 2단계 전체 · `--check_attestation` 의
require_attestation 분기(현재 정책이 post_hoc 이라 안 탑니다) · rescue 경로(미구현).

**Q4.** Q3 답변(재개 폐지는 허용하되 rescue 묶음이 필요)을 README 문구로만
이행했습니다. **300 h 잡을 던지기 전에** rescue 번들 모드를 구현해야 합니까,
아니면 실패가 실제로 났을 때 만들어도 됩니까? 저희는 후자가 낫다고 보는데
(실패 형태를 보고 만드는 편이 정확하므로) 그때는 이미 시간이 없다는 반론도 압니다.

**Q5.** Q6 에서 "잡은 추가·삭제하지 마십시오" 라고 하셨습니다. v23 은 v22 와
**같은 16잡**이고 argv 도 같습니다(`--potcar_identity post_hoc` 포함). 바뀐 것은
코드·문서·거버넌스뿐입니다. 이 이해가 맞습니까?

**Q6.** 이 번들로 **생산을 시작해도 됩니까?** 시작해도 된다면 1단계(10잡)까지
입니까, 아니면 그 앞에 더 볼 것이 있습니까?

파일은 수정하지 않으셔도 됩니다 — **GO/NO-GO 와 P0/P1** 판정만 주십시오.
