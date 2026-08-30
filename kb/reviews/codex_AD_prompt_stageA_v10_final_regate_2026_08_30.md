---
title: "회신 AD 요청 — Stage A v10 최종 재게이트 (P0 8건 처리 후)"
date: 2026-08-30
updated: 2026-08-30
tags: [review, codex, sdcp, stage-a, release-gate, vasp]
status: 발송전
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

# 회신 AD — 최종 재게이트 요청

회신 AB 가 *"다음 한 번의 release gate 를 최종선으로 권한다"* 고 했다. 그 한 번이다.

## 0. AB 의 P0 8건 — 무엇을 어떻게 했나

| P0 | 무엇이었나 | 처리 |
|---|---|---|
| **1** | 36/40잡이 결과와 무관하게 차단 (`SOURCE_ROLE_MISMATCH` 24 · `SOURCE_TOPOLOGY_UNVERIFIED` 12) | `role` 이 **분석 역할(calibration)과 등록 역할(Li/Ni)** 두 뜻으로 쓰였다. `registry_role` 을 분리하고, basin 자세는 `registry_role: None` 을 **선언**한다(비우면 `role` 이 그 자리로 읽힌다). 기체 기준계에 `mol_graph_canonical` 을 실제로 기록. ★ **배포 전 입력 preflight** 를 `verify_bundle` 에 추가 — 실물 v9 에 걸어 **36건** 재현(당신이 센 수와 일치), 새 번들에서 0건 |
| **2** | D3-off 16잡의 `incar_expected.IVDW` 불일치 | **소멸** — Q6 권고를 받아 D3-off 를 제거했다 (§1) |
| **3** | C3 부호가 물리적으로 반대 | **당신이 옳았다.** 봉인값 0.90 eV 의 정본 필드명이 `오프셋_UMA_빼기_DFT_eV` 였다 (SDCP 1.0728/1.0667 · c10 0.1855/0.1484 ⇒ +0.9028). D3 는 additive 라 `offset ≈ −δ` 이므로 비교량을 `predicted_offset_gap = −D` 로 **이름부터** 고쳤다. ⚠ selftest 두 건이 **같은 틀린 규약을 인코딩**하고 있어 코드와 시험이 서로 동의하며 둘 다 틀렸다 |
| **4** | basin 크기 기준이 production 에서 죽어 있음 | `basin_distance()` 가 selftest 밖에서 **한 번도 호출되지 않았다**. `same_basin()` 을 만들어 C1 이 쓴다 — 해시가 같아도 상세 지문으로 다시 보고, **상세가 없으면 통과가 아니다**. 그리고 당신의 후단 지적 수용: `S_f` 에서 슬랩·분자가 소거되므로 **네 자세 상호** 동질성만 요구하고 clean-slab 일치는 절대 E_ads 쪽으로 옮겼다 |
| **5** | `_spin_setup_ok()` 이 실제로 안 돎 | 키 넷을 `AUDIT_KEYS_RUNTIME` 에 추가. ★ 그러자 **잠복 버그가 드러났다** — `str(None)=="NONE"` 이라 미출력이 곧 "스핀 제약 있음" 이 되어 전 잡이 `BASIN_UNRESOLVED` 였다. VASP 는 기본값이면 안 찍으므로 None 은 기본값(꺼짐)으로 읽는다. 시험도 production 과 **같은 식**(`{k: _echo_val(t,k) for k in AUDIT_KEYS_RUNTIME}`)으로 바꿨다 |
| **6** | `planned` 24 ≠ 실제 40 → completeness fail-open | 실측 일치: v10 `planned 24 = disk 24`, holdout `18 = 18`, 차집합 **공집합** |
| **7** | C2 가 네 자세 완비성을 요구 안 함 | 기대 자세 수를 동결 manifest 에서 세고 **그 수만큼 두 seed 가 모두 유효할 때만** J_f 를 낸다. "seed-insensitive" → *"시험한 N자세 안에서 seed×pose interaction range 가 작았다"* |
| **8** | POTCAR allowlist 우회 | 조립기: `POTCAR.tmp` 에 조립·검증 → 통과 시에만 원자적 `mv`, 실패하면 trap 이 전부 삭제, `set -euo pipefail`, **면제 폐지**. 러너: provenance 존재·비면제·**현재 POTCAR sha 일치** 요구 |

selftest **348건** · convention_check 0 위반.

## 1. 번들 구성이 바뀌었다 (Q6 권고 채택)

D3-off 16잡을 **버렸다.** 절충이 아니라 정보가 0이라서다 — D3(IVDW=11)는 SCF 에 안 들어가는
additive 항이라 고정기하에서 `E_on − E_off = Edisp` 가 **항등식**이고, VASP 가 그 `Edisp` 를
OUTCAR 에 직접 찍는다. repo 의 phaseB OUTCAR(같은 IVDW=11)로 확인: slab −27.49493 ·
mol −0.71798 · complex −28.58614 ⇒ δ = **−0.373230 eV**. 쌍둥이가 남아 있는 번들이면
버리지 않고 `|(E_on−E_off) − Edisp| ≤ 1 meV` 로 **교차검증**한다.

⇒ 그 예산으로 **층화 홀드아웃**을 넣었다 (당신 권고대로).

| 번들 | 잡 | 구성 |
|---|---:|---|
| `sdcp_stageA_v10` | **24** | 2조각 × 4자세 × {pm1, net4} = 16 · refs 8 |
| `sdcp_stageA_holdout_v1` | **18** | 2조각 × 8자세 × pm1 = 16 · **controls/clean_slab 2** |
| | **42** | |

**홀드아웃 층화 (결과 보기 전 동결, `3e3ce4820c4df3ec`)**: UMA 사분위 4 × 사분위 안에서
**표면 anchor 원소가 서로 다른 2개**. ⚠ 처음엔 `sulfonate/backbone`·`terminus/midchain` 으로
적었는데 동결 manifest 로 **계산 불가**였다(원소기호까지만 있어 술폰산 O 와 에터 O 를 못 가른다).
게다가 분자쪽 anchor 는 축이 안 된다 — `sdcp_neutral` H 94 / O 7, `ptfe_c10` **96개 전부 F**.
런 전에 표면쪽 anchor 로 교체했다.

## 2. 판정해 달라 — 여섯

### Q1. P0 8건이 실제로 닫혔나
문서가 아니라 **코드와 산출물**로 판단해 달라. 특히 P0-1: 입력 preflight 가 v9 에서 36건을
재현하고 새 번들에서 0건인 것이 *"OUTCAR 가 와도 안 막힌다"* 를 보증하나, 아니면 여전히
결과가 와야 알 수 있는 자리가 남아 있나?

### Q2. C3 부호 정정이 옳은가
`predicted_offset_gap = −D` 를 `+0.9028` 과 비교한다. 그리고 **조각내 일관성**을 필수로 넣었다 —
사전등록 문서의 `⛔_분산_귀속_철회` 절이 *"D3 는 기하 의존이라 자세마다 달라야 하는데 관측
오프셋은 조각 안에서 상수(SDCP 6 meV · c10 37 meV)였다"* 고 적었으므로, δ 의 조각내 range 가
관측 상수성의 **5배**를 넘으면 평균이 맞아도 미해결이다. **이 추가가 옳나, 여유배수 5 가 맞나?**

### Q3. 42잡이 맞는 수인가
40 은 옛 구성(24 + 16 twin)의 산술이었고 그 16 을 지웠으므로 함께 사라졌다고 본다. 홀드아웃의
`controls/clean_slab` 2잡은 **여분이 아니라** 그 tranche 의 basin 판정 기준이다 — 빼면 판정이
사라지는 게 아니라 전 잡에서 **'보류' 로 조용히 통과**한다(생성기 도움말이 그렇게 적는다).
게이트 조건 ③은 숫자가 아니라 **등식**이라고 읽었다. **이 독법이 맞나?**

### Q4. 홀드아웃이 primary 를 오염시키지 않나
`candidate_set = holdout_stratified` → 분석기가 `HOLDOUT_TRANCHE` 로 primary 를 막고,
`--roles holdout` 은 **단독 강제**다. 홀드아웃이 더 낮게 나오면 primary 의 min 후보가 아니라
**재개 조건 발동**으로 처리한다. estimand 카드:
`kb/questions/sdcp_stageA_holdout_selector_2026_08_30.md` (H1 문턱 30 meV · H2 Spearman ρ 0.70/0.30).
**이 설계가 selector 가정을 실제로 시험하나?**

### Q5. 당신의 release gate 6조건
① 최종 ZIP·MANIFEST hash — 재생성 후 확정 예정
② production `main()` 합성 완주 exit 0 — e2e selftest 12/12
③ required inventory = 디스크 = census — 실측 일치 (24=24, 18=18)
④ C1/C2/C3 cohort 수 정확 — C1·C2 는 manifest 기대수 강제, C3 도 동일
⑤ 승인 PP 로 한 잡 site dry-run — **외주처에서만 가능** (우리가 PP 를 못 가진다)
⑥ clean source 또는 정확한 snapshot — MANIFEST 가 이제 자기 `argv` 와 유효 플래그를 적는다
**⑤를 우리가 못 하는데, 그것이 GO 를 막나? 대체 조건이 있나?**

### Q6. 우리가 여전히 못 본 것
AB 가 세 개를 새로 잡았다. **또 있나?** 특히 P0-5 처럼 *"검사가 존재하는데 실제로는 안 도는"*
부류를 찾아 달라 — 이 캠페인이 반복해서 밟는 자리다.

## 3. 형식

Q1–Q6 각각에 **P0/P1/P2 + 한 줄 판정 + 근거**. 마지막에 **GO / NO-GO** 하나.
NO-GO 면 해제조건을 번호로 달라. GO 면 그대로 제출한다 (외주 42잡, 동시 8잡에 약 3.8일).
