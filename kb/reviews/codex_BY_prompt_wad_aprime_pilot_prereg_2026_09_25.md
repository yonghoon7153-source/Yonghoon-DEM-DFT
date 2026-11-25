---
title: "리뷰 BY 프롬프트 — A′ 파일럿 사전등록 카드 (LPSCl | Ag · 흑연 점착일): 봉인 전 설계 검토"
date: 2026-09-25
updated: 2026-09-25
tags: [review, codex, adhesion, wad, prereg, estimand, lpscl, silver, graphite, uma, d3, pilot]
status: 발송 완료 · 회신 수령 2026-09-25 **NO-GO** (`codex_BY_reply_…`) → 카드 v2 로 대응 (`wad_aprime_pilot_prereg_v2_2026_09_25.json`) · 재심 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 BY — A′ 파일럿 사전등록 카드: 봉인 전 설계 검토

> 앞 리뷰: **BW** (A′ 경로 권고 · 제한 파일럿 조건부 GO) → **BX** (SE|SE 4층 경보 · 원인 진단 조건부 GO · '방법 검증 완료' NO-GO · P0 완료 판정기 · 라벨 정책).
> BX 뒤 파이프라인 v4 (`D-2026-09-25-wad-reference-state-policy`) 의 ③ 이 이 카드다. 트랙 = W_ad (우리 DFT) → 1저자 = 사용자. 정본 브랜치 `claude/friendly-meitner-lldvar`.
> **카드**: `db/properties/wad_aprime_pilot_prereg_2026_09_25.json` (draft · content_digest 없음 · 계산 0). 이 리뷰 뒤 1저자 비준 → 봉인 → 그 다음에야 던진다.

## §0. BX 뒤 한 것 (전부 계산 결과 보기 전 규칙 또는 진단)

| BX 항목 | 한 것 | 근거 |
|---|---|---|
| P0 완료 판정기 | 러너·집계기 둘 다 '마지막 실행 · `bfgs converged` 명시 · 실패 문구 거부' · 음성 5 · 원출력 네 잡 확인 (헤더 1 · 실패 0 · 성분별 힘 < 1e-3) | `tools/wad/run_sese_gpu.sh` · `se_sym_slab.py` · `db/raw/wad_sese_4L_2026_09_25/lastrun_check_2026_09_25.txt` |
| P1 문구 정정 7 | 4층 값 = 참조에 대한 슬랩 쌍 초과에너지 · ±0.16 귀속 철회 · '원자 극소' → 힘 기준 만족 · +0.0775 = 참조 변경 효과 · Pulay 등방 보장 아님 · 절반 전단 ≠ 미수렴 · epitaxial 참조의 뜻 | `wad_sese_4L_result_2026_09_25.json` `⛔_정정_회신BX` |
| 권고 3 벌크 수치 민감도 | 7 SCF (cubic/epi × 52·70 Ry × k3·k4 + 내장 대조) — σ_yz 10.8 kbar · ΔW′ 0.0775 네 설정 동일 · 70/k4 대비 −0.16 meV/atom | 같은 기록 `점검_C` · `--bulk_sens` |
| Q3″ | 끝점 동일 ✅ · 같은 기판 상태 → 정합 규칙 **(a)** 결정 (`D-2026-09-25-wad-lattice-matching-rule-a`) · 잔류 응력은 조건으로 명시 · comp1 V0 정본 불변 | 결정 원장 |
| Q6 | DEM 회신에 허용 서술 그대로 (부록) | `kb/projects/wad_dem_reply_draft_2026_09_23.md` §회신 3 |

## §1. 카드 요지 (자세한 것은 카드 파일)

- **보고량**: 작은 주기 모델의 **DFT(PBE+D3(BJ) 2체) 고정기하 W_sep** + 같은 표본에서 **UMA+D3 재현도** · 전체 계면(P1 ~436 · P2 ~820)은 **UMA+D3 예측**으로 따로.
- **기판**: comp1 (001) 정본 대칭 SE 슬랩 4층 두 종결 · **한 기하** (정합 규칙 (a) — 흡착층을 SE 에 맞춤) · 라벨 = 지정 comp1 셀 · 입방 고정 면내 · 잔류 응력 조건.
- **표본 V-세트**: V1 SE|SE (끝 · 대조 기록) · **V2 Ag(111)|graphene 직접 DFT** (registry ≥ 4 · E(d)) · V3 Ag₄/Ag₁₃ 조각 · V4 C₆H₆/C₂₄H₁₂ 조각 (둘 다 진단 · eV/조각) · **V5 작은 주기 계면** (SE 2층 1×2 + Ag 3층 ≈ 200 원자 — **자원 프로브 통과 시에만** · UMA 대조 5점의 표본).
- **끝점 (MoLE)**: 같은 셀·원자·제약 · far ≥ 10 Å · 진공/영상·추가 분리 ΔW ≤ 0.01 · δ_add 기록.
- **기하 생성**: UMA+D3 이완(셀 고정) → 그 좌표에서 DFT 단일점 두 끝점 (같은 기하면 DFT@UMA ≡ DFT 고정기하).
- **전자상태 정책**: 스핀 비편극 · gaussian 0.005 · 쌍극자 보정 두 끝점 동일 · −TS 기록 · **Li→Ag 침투 ≥ 1.5 Å = '반응한 계면' → 무효(세고 제외)**.
- **게이트 (결과 전)**: G1 P0 · G2 구조(PS₄·결합·침투) · G3 끝점 · G4 수치(ecut 70 단일점 ≤ 0.02) · **G5 UMA 대조 표본별 ≤ 0.10 · 평균 부호오차 ≤ 0.05** (§0′ 운영 기준 그대로) · G6 V2 registry.
- **갈래**: V5 불통과 → V5 없이 · G5 5/5 → 허용 문구 · 일부 탈락 → 나열·DEM 미전달 · 반응 계면 ≥ 절반 → 질문을 바꾼다.
- **자원**: GPU 만 (gabia 48 · V100 32) · CPU 추정 프로브 41 GB 문턱 · 총상한 제안 **140 GPU-h 벽시계**.

## §2. 질문

- **Q1 표본 설계** — V5(SE 2층 1×2 + Ag 3층)가 '전체 계면에 가장 가까운 대리' 로 적절한가? 2층 SE 는 SE|SE 4층에서 본 속층 이완(Li 자리 이동)을 담을 수 없다 — 그래도 UMA 대조 표본으로 쓸 수 있나, 아니면 V5 를 빼고 V2 + V3/V4 + 예측으로 가는 것이 정직한가?
- **Q2 G5 문턱의 출처** — 0.10 / 0.05 J/m² 는 §0′ 운영 기준(문헌 표준 아님)이다. 표본이 5점일 때 이 두 문턱이 무엇을 보증하고 무엇을 못 보증하는지, 그리고 '탈락은 세고 제외' 규칙이 G5 를 무력화하지 않는지.
- **Q3 상태 정책** — 스핀 비편극 · gaussian 0.005 Ry (Ag 금속 슬랩에 작다) · `dipfield` 두 끝점 동일 — 빠진 것은? Li→Ag 침투 1.5 Å 규칙은 '반응한 계면' 을 가르는 데 충분한가 (Li–Ag 합금화 · 전하이동)?
- **Q4 기하 생성 정책** — UMA+D3 이완 좌표에서 DFT 단일점(고정기하)만 하고 DFT 이완은 안 한다. 이 정의로 DEM 이 요구한 '고정기하 W_sep' 이 맞나? DFT 로 재이완한 값과의 차를 표본 1개에서 재야 하나 (그러면 그것도 결과 전 규칙으로)?
- **Q5 V2 Ag|graphene** — Maurer 류 셀 · registry 4 · E(d) 세 구간. 그래핀 단층 값을 P2(흑연)의 대리로 쓰는 한계를 어떻게 적나? 흑연 층간(벽개) 대조를 같은 카드에 넣어야 하나?
- **Q6 자원 규칙** — CPU 추정 41 GB 문턱 · GPU 실측 44 GB 중단 · 총상한 140 GPU-h. 빠진 위험(gabia 공존 금지 · b2o3 종료 뒤) 은?
- **Q7 봉인 형식** — 봉인 때 좌표 지문(sha)·registry 목록·PP 해시·UMA 체크포인트 sha 를 넣을 자리는 카드에 있다. 그 밖에 결과 뒤 바꿀 유혹이 생길 칸은?
- **Q8 허용 문구** — 1a 세 문장이 A′ 결정 ⑥('지정 표본에서 운영 기준 충족' 까지)을 넘지 않나? DEM 에 나가는 라벨 문장은 충분한가?

형식: 항목별 **GO / NO-GO / 조건부** + 봉인 전 필수 수정. 새 문턱을 제안하면 결과 전이므로 그대로 채택 가능하다는 점을 명시해 달라.

## 첨부 (repo 경로)

- 카드 `db/properties/wad_aprime_pilot_prereg_2026_09_25.json`
- 결정 `D-2026-09-25-wad-reference-state-policy` · `D-2026-09-25-wad-lattice-matching-rule-a` · `D-2026-09-23-wad-a-prime-scope` · `D-2026-09-23-wad-p2-lpscl-graphite-scope` (`db/governance/decisions.json`)
- 계획 `kb/projects/wad_lpscl_agc_vgcf_plan_2026_09_23.md` §0″ · §0′
- SE|SE 결과 기록 `db/properties/wad_sese_4L_result_2026_09_25.json` · 원자료 `db/raw/wad_sese_4L_2026_09_25/`
- 앞 리뷰 BW · BX 회신 (`kb/reviews/`)
