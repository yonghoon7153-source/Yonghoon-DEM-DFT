---
title: ISC × 균등화 공개 데이터셋 (xtangai/EST-D-24-12331)
description: "Public dataset behind Lai 2025 (J. Energy Storage 123, 116622): 6S2P 18650 module, designed ISC resistor on cell #1, passive/active balancing, 100 ms — one of ten files is broken in the published archive"
created: 2026-09-22
updated: 2026-09-22
type: entity
tags: [battery, research, pack-fault]
sources: [raw/papers/lai2025_balanced-capacity-isc-detection-modules.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: multi-source-mixed
---

# ISC × 균등화 공개 데이터셋 (xtangai/EST-D-24-12331)

## 개요

Lai, Ke, **Tang(교신)**, Zheng 2025 (`raw/papers/lai2025_balanced-capacity-isc-detection-modules.md`)
의 공개 데이터셋. 저장소 `https://github.com/xtangai/EST-D-24-12331` (교신저자 Xiaopeng Tang
의 계정; 이름은 *J. Energy Storage* 투고 번호). **6S2P SONY US18650VTC5 모듈**, 가장 약한
단위 **#1 에 설계된 병렬 저항(55/110/165/220/330 Ω)** 을 달아 ISC 를 모사, **수동/능동 균등화**
각각으로 **100 ms** 샘플링.

**살아 있는 조사 기록은 위키 밖에 있다** — `bms-balancing/docs/ISC_LEAKAGE_DATASET.md`
(구조·실측·재현 명령·미해결 물음; 내용을 여기 복사하지 않는다, mothership 특칙). 이 페이지는
그 문서와 **논문을 잇는 사상표**와 **재현 불가 원장**만 둔다.

## 핵심 사실

### 상태 (2026-09-22)

- ★ **공개 아카이브의 `165_passive.xlsx` 가 깨져 있다** (중앙 디렉터리에는 있고 바이트가 없다 —
  실측은 `ISC_LEAKAGE_DATASET.md` §1). 나머지 **9/10 파일**은 `zip -FF` 로 살아난다.
- 열 정의는 저장소 README 에만 있고(16 열), 파일은 **17 열**이다. **논문도 17 열을 언급하지
  않는다** — `[재현]` 파일 내 1 씩 증가하는 카운터, 파일마다 시작값이 다르고 범위가 겹친다.
- **논문 Table 2 의 SoH(용량)는 데이터셋에 없다** → 식 (12) 를 돌리려면 논문에서 옮겨 와야 한다.

### 데이터 열 ↔ 논문 사상 (`[재현]`, `55_passive`·`55_active` 전수)

| 데이터 | 논문 | 근거 |
|---|---|---|
| 열 14 대상 셀 인덱스 `0` | **셀 #1** (ISC 셀, 0-기반) | 인덱스 0 의 균등화 적분이 Fig. 3/4 의 #1 곡선과 일치 |
| 열 12 (대상 셀 균등화 전류) 를 열 14 별로 0.1 s 적분 | **Fig. 4 의 balanced capacity (수동)** | −0.088/−0.490/−0.566/−0.687/−0.853/−0.861 Ah ↔ `[도표]` ≈ −0.08/−0.49/−0.56/−0.68/−0.85/−0.85 |
| 위 + Σ열 13 (환류, **6 셀 공통 0.714 Ah**) | **Fig. 3 의 balanced capacity (능동)** | +0.229/−0.225/−0.315/−0.471/−0.634/−0.637 Ah ↔ `[도표]` ≈ +0.23/−0.23/−0.31/−0.47/−0.64/−0.64 |
| `max\|열 12\|` 수동 1.566 A · 능동 2.786 A | Appendix A **2.5 Ω 저항**(≈V/2.5) · "**about 2.7 A**" | 정합 |
| 파일 길이 150,000 / 135,000 / 522,000 행 | Fig. 3 250 min · Fig. 4 ≈225 min · Fig. 5(a) ≈870 min (=14.5 h) | 정합 — **165 조건이 긴 것은 설계**(Test 5 = 다른 프로파일) |
| 열 7–10 환경 온도 | `[인쇄]` "25 ± 2 °C" | ⚠ `55_active` 끝 행 27.53 °C (첫·끝 행만 봤다) |

→ `ISC_LEAKAGE_DATASET.md` §3 의 "수동/능동 나머지-셀 균등화 적분 **177 배**" 는 정확히
**능동 환류 항(열 13)의 유무**다.

### 재현 불가 원장 — 깨진 `165_passive` 에 걸린 논문 결과

| 논문 결과 | 재현 |
|---|---|
| Table 3 Test 5 열 (Ref 22.01 / Est 21.17 / Err 0.84 mA) | ❌ |
| **Table 6 Passive 열** (22.01 / 21.70 / 0.31 mA) — **추정 SoH 로 돌린 수동 결과의 유일한 숫자** | ❌ |
| Fig. 2(b)·(d), Fig. 5(b), Fig. 8(b) | ❌ |
| Tables 3/4 Tests 1–4 · Table 4 Test 5 · Fig. 3 · 4 · 5(a) · 6 · 7 · 8(a) | ✅ (Table 2 SoH 를 논문에서 가져오면) |

## 이 위키와의 관계

- **왜 이 데이터가 이 위키에 있는가**: [[isc-detection-vs-balancing-masking]] 섹션에서 **정답
  라벨이 설계값**인 유일한 실팩 데이터다 (`NEW_MODEL_REQUIREMENTS.md` §5 의 `measured` 급).
  ⚠ 라벨은 **ISC 저항**이고 열화 모드(LLI/LAM)가 아니다 — [[fitting-degeneracy]] 의 본진 축에는
  쓰이지 않는다.
- **수동 ↔ 능동**은 같은 결함에서 조작만 바꾼 쌍이다 — 다만 능동 환류(0.714 Ah = 단위 용량의
  ≈14 %)가 SoC 를 바꾸므로 **직교하지 않는다**.
- 데이터는 저장소에 넣지 않는다 (180 MiB, 남의 자료). 추출본은 세션 스크래치패드에만 있고
  재현 명령은 `ISC_LEAKAGE_DATASET.md` §6.

## 관련

- [[isc-detection-vs-balancing-masking]] — 이 데이터가 답해야 할 물음(P1~P6)
- [[fitting-degeneracy]] — 모양이 같은 본진 개념 (물리량은 다름)
- `bms-balancing/docs/ISC_LEAKAGE_DATASET.md` — 조사 정본 (repo-root 상대 경로)
