# STEP4-v1 — 저율 충전 반응전류 분포 (랩 slide-20 물리판)

2026-07-14.  요청: "랩 슬라이드 20(0.1C 충전 시 입자별 전류밀도)을 우리 프레임으로" —
STEP3의 DC 전도 지도(je)가 아니라 **충전 구동 반응전류** i_n을 계산한다.

## 모델 (v1 = 선형·준정적)

같은 STEP3 복셀 격자 위 **두 네트워크를 반응 계면에서만 결합**한 단일 SPD Kirchhoff 시스템:

- **전자망** (σ_e 테이블: AM 10/5 mS/cm + VGCF/SuperP/SDCP) ← 집전체 plate (bottom, φ_e=1 소스)
- **이온망** (σ_i 테이블: SE 3.0 + SDCP 1.0 mS/cm) ← 분리막 plate (top, φ_i=0 싱크)
- **BV faces**: AM(sid 1,2) ↔ 이온전도상(sid 5,6) 인접 복셀면마다 선형화 Butler-Volmer 컨덕턴스
  g_ct = (i0·F/RT)·A_face.  Li는 이 면으로만 두 망을 건넌다 → **반응 면적이 rasterized 접촉
  (=coverage)에서 자연히 나온다** (별도 coverage 입력 불필요).
- 입자별 반응전류 i_n = Σ_faces g_ct·(φ_e − φ_i).  출력은 **RELATIVE i/ī** (linear라 C-rate와
  무관한 분포; 절대 A/m²·SOC 의존은 v2).

가정 (정직):
- **선형화 BV** (과전압 ≪ RT/F ≈ 26 mV) = 저율 전용.  충·방전 = 부호 반전만.
- **균일 SOC** → OCV 상수항이 전위 기준으로 소거 (충전 초기 상태).
- i0 = 2 A/m² 기본 (**⚠F1 hook**, Newman-typical 1–5 A/m²; `--i0-a-m2`).  i0는 Wagner 수를 통해
  분포의 network-지배 ↔ 계면-지배 정도를 정한다 — 민감도 스윕 대상.
- SDCP는 혼성전도라 **두 망 모두에 노드**를 갖지만 자기-BV는 없음(인터칼레이션 전극이 아님) —
  기여는 이온/전자 '배달'로만 (STEP3 이중전도 서사와 연속).  AM|SDCP 면은 반응면으로 포함
  (SDCP가 Li를 AM에 배달 → SDCP의 반응-접근성 기여가 자연히 계산됨).

## 구현

- `scripts/step3_sigma.py :: solve_reaction_current()` — 어셈블리는 solve_sigma_z 미러
  (harmonic face-g, per-column distance-aware plate, union-라벨 anchored-component 필터,
  ε-diag 가드).  GPU_SOLVE(CuPy) 공용.
- `scripts/mpm_webapp_payload.py` — 기본 ON (`--no-step4`), `--i0-a-m2`.  입자별 `jrxn`(i/ī)
  + `step3.rxn{i0, g″, n_bv_faces, active_am_pct, kcl_err, resid, trust}`.
- 뷰어: 메인 `🔋 반응 전류밀도` 모드 + 비교 팝업 `jrxn` 옵션 (je 기계 재사용, jet+감마).

## 검증

- **analytic sandwich selftest** (`--selftest-rxn`): AM slab | BV | SE slab 직렬저항 —
  I_tot가 해석해와 1e-3 이내 일치(실측 1e-7), **KCL**(plate 유입 = ΣBV 통과) 1.3e-9,
  입자합 = 총전류.  PASS (2026-07-14).
- 기대 물리 체크리스트 (payload 첫 런에서 확인): ① 저율·i0=2에서 계면-지배 경향 → i_n이
  대체로 반응면적(coverage) 비례 + 두께방향 완만한 구배, ② 분리막/집전체 근처 편중은 σ_i/σ_e
  비대칭을 따름 (slide-20의 바닥 편중과 문법 비교), ③ SBE↔DBE: SDCP가 이온 배달로 i_n
  불균일도를 낮추는지 (신규 결과 — SDCP 서사 확장).

## Trust

RELATIVE 분포 지도 (동일 세팅 비교용).  절대 반응전류/과전압/농도(slide-21·22)는 STEP4-v2
(시간적분 + 구형확산 + 비선형 BV) — pybamm 대조 앵커 예정 (docs/stage4_electrochem_research.md).
