---
title: "CY 프롬프트 — W_ad 외주 2차 설계 리뷰: 탄소 작은 모델 (P2′) 보고량 카드 + V5 은 쪽 ENCUT 짝 재시도 (개정 4) + 러너 고칠 점 · 빌드 전 · 범위·수렴·문턱부터"
tags: [review, wad, adhesion, vasp, outsourcing, graphite, dipole, scf, estimand, codex, prompt, letter]
letter: CY
date: 2026-10-15
track: wad
channel: codex
kind: prompt
status: 초안 (2026-10-15) — 사용자 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). 이 편지는 **빌드 전 설계 리뷰**다 — 구조·묶음·코드는 아직 없다. GO 가 나면 빌드하고, 묶음 (코드·MANIFEST·러너) 은 다음 편지 CZ 에서 따로 본다.
> ⛔ 점착 W 값은 kb 문서에 싣지 않는다 (repo 규율) — 이 편지에도 W 숫자를 쓰지 않는다. 문턱·비율·벽시계만 쓴다. 값은 아래 파일에서 직접 읽어 주길 바란다.
> 기준 커밋 `d789d8f`. ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_CY_reply_…` 로 원문 보존.

---

**[W_ad · 외주 2차] 설계 리뷰 요청 — 탄소 작은 모델 (P2′) 카드 · V5 은 쪽 ENCUT 짝 재시도 (개정 4) · 러너 고칠 점 (빌드 전)**

## 0. 이번 리뷰를 왜 이렇게 묻나

지난 V5 외주 (LPSCl|Ag 작은 모델 · VASP 18 잡) 는 리뷰를 다섯 번 거쳤다 (CE → CF → CG → CI → CJ → CK GO). 그 리뷰들은 전부 **포장·무결성** (POTCAR 유출 · MANIFEST · 종료 코드 · 증거 모순) 을 봤고 다 고쳤다. 그런데 반송된 결과에서 터진 것은 거기가 아니었다:

1. **범위** — LPSCl 은 Ag–C 층의 Ag 와 **탄소 둘 다**에 닿는데, DFT 확인 대상을 은 쪽 하나로만 잡았다. 탄소 쪽 (LPSCl|흑연) 은 UMA+D3 예측뿐이고 확인 경로가 없다.
2. **수렴** — 금속 슬랩 + 쌍극 보정 (LDIPOL) 의 분리 끝점 셋이 SCF 수백 스텝 동안 |dE| 1e-4–1e-3 eV 에서 맴돌았다. 사전등록 재시도 (혼합만 변경) 는 듣지 않았고, ENCUT 650 짝은 값 없음으로 끝났다 → G4 INCOMPLETE → G5 판정 불가.
3. **러너** — 수렴을 OUTCAR 의 'EDIFF is reached' 문구로 판정했는데, VASP 5.4.4 는 NELM 소진에도 그 문구를 찍는다 → 자동 재시도가 안 돌아 손으로 다시 맡겼다.

그래서 이번엔 **"범위가 맞나 · 수렴이 될까 · 문턱이 의미가 있나"** 를 먼저 물어 주길 바란다. 무결성은 CZ 에서 본다.

## 1. 지금 상태 (사실)

- V5 반송 (10-15): 17/18 잡 OK (OSZICAR 마지막 스텝 기준) · G3 끝점 PASS (두 검사 모두 문턱 0.01 안 · 직접 8→10 Å 쪽은 문턱의 92 %) · G4 k·σ PASS · **ENCUT 650 far 값 없음** → G4 INCOMPLETE. 기록 `db/properties/wad_aprime_v5_vasp_result_2026_10_15.json` · 원자료 `db/raw/wad_aprime_v5_vasp_2026_09_27/final_return_2026_10_15/` (레포 묶음으로 다시 낸 집계가 처음 집계와 바이트 일치).
- UMA 단일점 (G5 용 · 12 구조) 은 올라왔지만 (`db/raw/wad_aprime_v5_vasp_2026_09_27/uma_energies_v5_2026_10_15/`) **G5 는 아무도 집계하지 않았다** — 재개 결정을 G5 를 보기 전에 하려고.
- 사용자 결정 (10-15): ENCUT 짝을 지금 다시 연다 (이유 = LPSCl|Ag 가 DEM 박리의 실제 접촉 쌍 · G5 와 무관) · 탄소 작은 모델 카드를 쓰고 **한 번에 묶어** 외주 · 빌드 → 리뷰 → 발송.

## 2. 리뷰할 문서 (둘 다 초안 · 결과 전)

- **탄소 카드** `db/properties/wad_p2small_vasp_card_2026_10_15.json` — §1 무엇을 · §1b 설계 · §1c 답하지 않는 것 · §2 식 (Δ_C · δ_vdW · ②′ C–C) · §3 잘 정의되나 · 표본_계획 · §4 게이트 · §4b 재시도 사다리 · §4c 비용 · §5 서술.
- **개정 4** `db/properties/wad_aprime_pilot_prereg_v5_amendment_4_e70_rerun_2026_10_15.json` — 왜 다시 여나 · 두 단계 절차 (a4) · 검사기·집계기 고칠 것 · 러너 고칠 것 (탄소 묶음과 공통).
- 참고: A′ 카드 `db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json` · 개정 3 `…_amendment_3_vasp_v5_2026_09_27.json` · SE 쌍 카드 `db/properties/wad_se_pairs_uma_prediction_card_2026_10_01.json` · C–C 결과 `db/properties/wad_cc_graphite_result_2026_09_30.json` · CE 회신 (재시도 정책) `kb/reviews/codex_CE_reply_wad_aprime_v5_vasp_outsourcing_2026_09_27.md` · V5 도구 `tools/wad/build_v5_vasp_package.py` · 빌더 `tools/wad/build_aprime_interfaces.py`.

## 3. 확인 요청 (질문마다 GO / 조건부 / NO-GO 와 P0·P1·P2 로)

- **Q-CY-1 (범위)** — 탄소 쪽을 ① 같은 봉인 좌표의 UMA+D3 vs PBE+D3(BJ) (Δ_C · D3 가 지워져 짧은 거리 부분만 본다) 와 ② 같은 좌표에서 분산 처리를 바꾼 민감도 (δ_vdW · optB88-vdW) 로 재는 설계가, DEM 이 SE/Ag–C 계면 박리에 쓸 LPSCl|흑연 W 의 불확실성을 실제로 줄이는가? ②′ (같은 두 방법으로 흑연 C–C 대조점 — 우리 QE PBE+D3(BJ) 는 실험보다 약 10 % 낮았다) 은 넣을 가치가 있는가? 넣어야 하는데 빠진 것, 또는 넣지 말고 '답하지 않는 것' 에 적어야 할 것이 있는가?
- **Q-CY-2 (문턱)** — 탄소 G5_C (표본 |Δ_C| ≤ 0.03 · 종결별 평균 ≤ 0.02 J/m²) · G3 (≤ 0.01 · 발송 전 D3 만 예측이 문턱의 80 % 를 넘으면 끝점 재설계) · G4 (≤ 0.01) · δ_vdW 라벨 (20 %) 이 서로 맞고, **예측되는 실패나 공짜 통과**가 없는가? (G3 를 처음 0.005 로 적었다가, P2 전체 계면 UMA 에서 10 → 12 Å 변화가 이미 그만큼이라 결과 전에 고쳤다.) 절대 문턱이 맞나, 상대 문턱이 맞나?
- **Q-CY-3 (모델·표본)** — SE 2층 (V5 절단) 1×3 + 흑연 AB 2층 · 변형 2 % 미만 · 직접 분리 10 Å · registry A 만 (P2 에서 A·B 차가 아주 작았다) + 계면 +0.5 Å 벌린 표본 · 분모 4. 흑연 1층 (값싼 대안) 이나 3층과 견주어 이 선택이 맞나? 표본 넷이 '방법 오차' 를 말하기에 충분한가?
- **Q-CY-4 (수치 점검 집합)** — G4 를 ENCUT 650 · k 4×3×1 둘만 두고 σ ½ 을 빼는 것 (V5 금속에서도 σ ½ 효과가 문턱의 2 %) 이 정당한가? 흑연 반금속에 기본 k Γ 3×2×1 이 충분한가 (흑연 4×7√3 직사각 셀의 K 점 접힘 포함)?
- **Q-CY-5 (분산 대안)** — VASP 5.4.4 에서 고정기하 민감도용으로 optB88-vdW 가 맞는 선택인가 (rev-vdW-DF2 · D3 zero · MBD · TS 와 견주어)? PAW 와 vdW-DF · vdw_kernel.bindat · GGA = BO 매개변수 · LASPH 등 함정은?
- **Q-CY-6 (두 단계 쌍극 보정)** — ⓐ LDIPOL = .FALSE. (IDIPOL · DIPOL 유지) 로 먼저 돌린 WAVECAR 에서 ⓑ LDIPOL = .TRUE. · ISTART = 1 · ICHARG = 0 으로 이어 수렴시키는 절차가 맞나? ⓑ 의 최종 에너지가 처음부터 수렴한 것과 같은 바닥상태라고 봐도 되나? 사다리 순서 (r1 두 단계 → r2 두 단계 + 혼합 변경) 대신 AMIN 0.01 등을 먼저 둬야 하나? (VASP 설명서는 이 환경에서 접속이 막혀 원문을 확인하지 못했다.)
- **Q-CY-7 (은 쪽 재개의 정당성)** — G5 를 보기 전에 '물리적 관련성' 을 이유로 ENCUT 짝 한 잡을 개정 4 로 다시 여는 것이 사전등록 규율상 정당한가? 은 쪽 G5 와 크기 효과를 a4 반송 뒤로 미루는 것이 맞나? a4 의 자격·채택 규칙 (첫 시도와 r1 이 모두 실행·미수렴일 때만 · a4 가 마지막) 에 빈틈은?
- **Q-CY-8 (비용)** — V5 실측 장부 (같은 업체 · 같은 빌드 · 잡당 중앙 10.4 h) 를 크기 비율로 늘린 어림 (탄소 잡당 약 23 h · 17 잡 약 16 노드-일 · 흑연 1층이면 약 9 일) 이 타당한가? 질문에 답하는 **최소 집합**은? 파일럿을 '가장 어려운 잡부터' (은 a4 · 탄소 S_A far · 탄소 ENCUT 650 far) 로 두는 것이 맞나?
- **Q-CY-9 (러너·검사기)** — OSZICAR 마지막 스텝 판정 · 자동 사다리 · 120 스텝 조기 경보 · 0 스텝 중단 폴더 규칙 · stageA 반송 — V5 교훈에서 빠진 것은? 검사기가 **조용히 틀린 데이터를 받아들일** 길 (예: ⓑ 가 WAVECAR 를 못 읽고 무작위로 시작했는데 수렴해서 통과 — 문제인가) 이 있는가?
- **Q-CY-10 (메타)** — 이번에도 '제대로 돌렸나' 만 묻고 '맞는 양을 재나' 를 놓치는 곳이 있는가? 우리가 묻지 않은 질문 중 물어야 할 것은?

## 4. 다음

GO (또는 조건부 GO 를 반영한 개정) → 빌드 (작은 탄소 모델 구조 · UMA+D3 이완 · 봉인 · VASP 묶음 · 검사기·집계기 확장 · selftest + 일부러 깨기) → **CZ (묶음 리뷰)** → 사용자 발송. 은 쪽 DEM 편지 (라벨 · Ag–C 정정 두 문장) 는 외주 결과가 온 뒤 한 번에 보낸다.
