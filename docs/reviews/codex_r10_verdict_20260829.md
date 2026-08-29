# Codex R10 판정 — Methods v7 · Table S3 (2026-08-29)

기준 커밋 **`b84c955d`** (URL 고정).  ⚠ 요청서 헤더의 `6ba54948` 는 오기 — 비-P provenance 정정.

## 총판정

| 용도 | 판정 |
|---|---|
| 쟁점 목록을 붙인 **공저자 내부 검토** | **조건부 GO** — 첫 페이지 `PROVISIONAL — NOT FOR SUBMISSION` |
| **완성된 Methods 교체안**으로 전달 | **NO-GO** |
| **Table S3 투고 준비** | **NO-GO** |
| centerline 을 단일 "보고 규약" 으로 지정 | **기각** |
| 방어 가능한 결론 | **한 bed pair · 채택 상전도도 아래의 조건부 모델 contrast** |

## 우리가 틀린 것 (사실 오류 — 한정어 부족이 아니다)

| # | 초안이 쓴 것 | 사실 |
|---|---|---|
| 1 | *"PTFE was **resolved** … as a blocking phase"* | **아니다.** 한 셀 폭 centerline 을 찍고 그 셀을 exact-zero 로 제거한다.  직경 인식 `capsule` 은 **미구현 예약값** ⇒ 코팅 공간범위 **과소** · 찍힌 셀 차단 **과대** |
| 2 | *"빼면 치환의 절반이 모델에서 사라진다"* | **과장.**  PTFE 의 함량·역학은 DEM–MPM 침대에 **남는다** (W2 실측: PTFE 만 E 가 바뀌어 변위가 달라짐).  사라지는 것은 **전자격자의 절연배제 채널** 하나 |
| 3 | *"additives were **then** seeded"* | **순서 오류.**  첨가제는 **MPM 점군에 포함**돼 있었다 — 위 W2 측정이 그 증거 |
| 4 | *"rigid-sphere cannot reproduce … particle **rearrangement**"* | DEM 은 재배열을 **한다.**  못 하는 것은 소성 평탄화·파쇄·입계 변형 |
| 5 | ~10 % · 11–12 % 를 *"reported/measured"* 로 | ~10 % 는 **복합체·유리 문헌에서 유도한 프로젝트 표적**, 11–12 % 는 **우리 순수-SE 시뮬레이션 결과** — 둘 다 독립 실측 아님 |
| 6 | `lower bound on that axis` | **철회.**  관측된 것은 **제한된 refinement 구간의 증가**뿐 |
| 7 | σ_ele 를 reported 로 승격 | **정본 원장이 `RAW_W4_VERIFIED_UNTRACKED · 승격 HOLD`** — 내가 쓴 헤더를 내가 어겼다 |

★ **Q1 의 핵심**: 물리적 우려는 결과 전에도 있었으나 **생산 승격은 명시적으로 보류**돼
있었고, 두 값을 본 뒤 큰 쪽으로 옮겼다 ⇒ **결과 독립이 아니다.**
그리고 `off` 가 보수적이라는 판정도 **성립하지 않는다** (더 작은 값일 뿐, 하한 입증 없음).

## 살아남는 헤드라인 (R10 제시)

> For the single paired SBE/DBE bed and the adopted phase-conductivity parameterization, DBE
> exceeded SBE under both tested PTFE representations (+12.4 % unresolved; +30.8 % exact-zero).
> The magnitude was PTFE-protocol dependent, and a registered carbon-network upper-bound
> sensitivity reversed the ordering; this is therefore a **conditional model contrast, not an
> experimentally validated or parameter-robust material claim.**

## 해제조건 8 (투고 GO 로 바꾸려면)

| # | 조건 | 상태 |
|---|---|---|
| 1 | centerline 단일 primary·굵은글씨·`reported`/`resolved` 제거, 두 규약 **동등 sensitivity** | ✅ 적용 — ⚠ **1차 반영은 머리만 고치고 본문 3곳을 놓쳤다** (아래 부록 B) |
| 2 | calibration provenance · DEM/MPM 역할 · **첨가제 단계 순서** 정정 | ✅ 적용 |
| 3 | `lower bound` · "contact resistance 복원" · 무조건 SDCP 개선 주장 → 조건부 문구 | ✅ 적용 |
| 4 | **W4 원자료·receipt 를 고정 커밋에** 넣어 원장 HOLD 해제 | ⛔ 미착수 (task #10) |
| 5 | σ_ion 및 나머지 Table S3 행 **재측정 또는 명시적 제외** | ⛔ 미착수 |
| 6 | `ε_union`·thickness 의 **연산 정의** + 과압축 한계 추가 | ⛔ 미착수 |
| 7 | 수정안을 **`docs/manuscript_draft/build.js` 에 배선** + Figure 4b 재작도 | ⛔ 미착수 |
| 8 | Compact ↔ Full 한정어 **동등화** + 외부 DOCX 의 S16–S18 감사 | ⛔ 미착수 |

⚠ **7 이 새로 드러난 것**: 실제 생성 소스 `docs/manuscript_draft/build.js` 가 아직
PTFE-off · `standard error` · 옛 Table S3 골격을 쓴다.  **Markdown 수정안이 최종
전달물에 배선돼 있지 않다** — 오늘 반복해서 만난 "주 문서만 고치고 거울 방치" 그대로다.

## 부수 정정 (R10)

- **Q2**: 코드 기본값을 지금 옮기지 **않는** 판단은 맞다.  대신 ① 재현 러너에서
  `PTFE_STAMP` 필수 명시 ② `software default`·`analysis role`·`publication profile` 분리
  ③ 로그 라벨을 `explicit exact-zero sensitivity protocol` 로 중립화 ④ 두 규약 동등 보고.
- **Q4-2**: σ_VGCF 부호반전은 **본문 유지** — 단, 상한 팔이 *"더 정확한 물리가 아니라
  한 origin 의 이중 이상화 sensitivity"* 임을 함께 적을 것.
- **Q6**: Compact 에 빠진 한정 넷 — exact-zero 과차단 · 두 규약 방향/크기 · `no CI` ·
  A-track 1/5 의 PTFE-off 한정.
- **Q7**: `reconstructed` → `generated`/`packed`/`compacted` (tomography 재구성 오인 방지).
  Table S3 제목은 구조/수송을 나눠 적을 것.  S16–S18 caption 은 **리포 밖이라 미감사**.

---

## 부록 — 규율 검사 `19b` 가 **여전히 간헐 실패한다** (2026-08-29, 정정)

2026-08-29 오전에 이 검사의 간헐 실패를 `git rev-parse --short=8` 로 **고쳤다고 커밋했다**
(`abc83007`).  **그 주장은 틀렸다** — 같은 날 오후 R10 반영 커밋에서 **다시 실패했다**
(probe `8bfd3b6e`, 8자라 접두사 길이 문제도 아니다).  직후 6회 연속 재실행은 전부 통과.

⇒ **접두사 모호성이 원인이 아니었다.**  원인 미상.  관측된 것:
- probe 는 `git commit-tree HEAD^{tree}` 로 만든 **매달린 커밋**이고 SHA 는 매 실행 달라진다
- 실패는 **특정 SHA 에서만** 난다 (수동 재현에서는 "안 닿는" 이 정상 출력됐다)
- 실패율은 낮다 (오늘 ~20 회 중 2 회)

⚠ **이것은 사소하지 않다.**  이 검사는 러너의 fail-closed 게이트에 걸려 있어 거짓 빨간불이
**GPU 런을 막는다**.  그리고 더 나쁜 방향 — 간헐적으로 **통과**하는 검사는 진짜 결함도
간헐적으로 놓친다.

**후속 (미착수)**: 실패한 probe SHA 를 파일에 남겨 재현 가능하게 만들고
(`_dang` 을 로그), 그 SHA 로 `check()` 를 직접 호출해 어느 분기에서 갈리는지 본다.

---

## 부록 B — 1차 반영이 **머리만 고쳤다** (2026-08-29, 재판정 직전에 발견)

R10 반영 커밋(`6e65e28b`)은 문서 **머리**에 *"centerline 은 resolved 가 아니다 — 기각"* 을
적었으나, **본문 세 곳에 그 문장이 그대로 남아 있었다**:

| 자리 | 남아 있던 문장 |
|---|---|
| Full · Stage 3 | *"**PTFE was resolved on the conduction grid as a blocking phase** … could not represent **half of the compositional change** under study"* |
| Compact | *"PTFE was resolved as a blocking phase … omitting it would remove half of the compositional change"* |
| Table S3b 각주 | *"PTFE is **resolved in the reported configuration** …"* |

⇒ **머리와 본문이 정반대를 말하는 상태로 재판정에 낼 뻔했다.**  Codex 가 재판정을 제안한
직후, 보내기 전에 본문을 다시 읽다 발견했다.

★★ **오늘 네 번째 같은 형태이고, 이번엔 고치고 있던 파일 안에서 났다**:
① Table S3 헤더(`RAW_W4_VERIFIED`) ② §5 국문 요약 ③ A1 §4 (A3 이 대체했는데 A1 무표시)
④ **이 건**.  앞의 셋은 "다른 문서" 였는데 이번엔 **같은 문서 안**이다.

**교훈 — 문자열 치환으로 철회를 반영할 때는 `grep` 으로 잔여를 세고 0 을 확인한다.**
지금 그렇게 했다: `grep -c "PTFE was resolved\|half of the compositional"` → **0**.
⚠ 이것을 검사기로 만들 수 없는 이유: 철회 문구는 매번 다르고 `quotation_ban` 은 **수치**
등록부다.  ⇒ 절차로만 막힌다 (반영 커밋마다 잔여 grep).
