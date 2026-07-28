# 미결 리스트 (Open Items)

> 세션이 바뀌어도 유지되는 미결 사항 추적. 닫을 때 날짜+근거를 남기고 ✅로 옮긴다.
> 등록: 2026-07-27 (MAX 감사 후속).

## 🔴 판정 대기

### 1. modelc(LPSCl1.6) MD Ea 정본 — 0.2235(단일 deck) vs 0.197±0.032(3-seed)
- **상태**: OPEN. 양쪽 파일(comp2_md_arrhenius.json ↔ b2o3_vs_lpscl16_conductivity.csv)에
  충돌 블록 + "확정 인용 금지" 표기됨 (MAX 감사 discipline-6).
- **통계적 사실**: 0.2235 ∈ [0.165, 0.229] = 3-seed 1σ 구간 안 — **물리적 모순이 아니라
  '어느 프로토콜 값을 인용하나'의 충돌**이다. 임시 규칙: 조성 간 비교는 같은 시드
  프로토콜끼리만 (단일 deck: comp1 0.253 ↔ modelc 0.2235 / 멀티시드: modelc 0.197±0.032
  ↔ b2o3 0.199±0.034 ↔ LPSOCl 0.271±0.033).
- **닫는 방법 (판정 2026-07-27): AIMD 불필요.** 이유:
  1. 충돌이 UMA 내부(시드 통계) 문제라 AIMD는 질문이 다르다 — AIMD 1궤적을 추가하면
     같은 ~15% 시드 잡음을 가진 **제3의 값**이 하나 늘 뿐, 통계 충돌은 그대로다.
  2. 비용 비대칭: AIMD 3-T Arrhenius(52at, 각 ≥100 ps)는 주 단위 / UMA 시드 추가는 시간 단위.
  3. 우리 규율상 MLIP 절대값은 어차피 인용 금지 — 절대 정확도가 걸린 항목이 아니다.
  → **정공법 = comp1 멀티시드 보강**: comp1 600/800/1000 K × 추가 2 seed (6 run,
  ~15 h GPU, gabia disorder 캠페인 종료 후). 전 조성이 멀티시드로 통일되면
  0.197±0.032를 modelc 정본으로 확정하고 단일 deck 앵커는 SUPERSEDED 처리.
  UMA 자체 검증이 필요해지면(리뷰어 요구 시) full AIMD가 아니라 **UMA 궤적 스냅샷
  DFT single-point 스팟체크**(힘/에너지 상관)로 족하다.

### 2. comp2 disorder ensemble — Ea 0.087(cfg0) 아티팩트 여부
- cfg0 600 K MSD가 확산 영역인지 log-log 기울기(≈1) 확인 전까지 **인용 금지**.
  600→1000 K에서 D 2.0×(0.276 eV라면 8.5× 기대)라 케이지 잔류 의심.
- cfg1/cfg2 완료 후 config 산포로 판정 (단일 config 판정 금지 규율).

### 3. VGCF 2×2 barrier 행렬 — kgy NEB 체인
- Li_in_gallery_gr2L(2L|1L) → Li_in_gallery_2L(1L|2L) → Li_on_graphene_2L 진행 중.
- 완료 시: 209 meV 층수 효과의 VGCF/h-BN 몫 분해 + 2L 수렴 판정 + 기준선 층수 정합.
  결과에 따라 "gallery가 표면보다 ~2× 빠름" 문구의 배수 재계산.

### 4. SDCP complex_doped_v2 DFT relax — k 2×2×1 재실행 수렴 여부
- k 1×1×1 정체(150 iter, 0.0837 Ry) → 2×2×1로 재시작. accuracy가 0.08을 뚫고
  내려가는지 확인 필요. VRAM 46.9/48 GB로 임계 (OOM 시 diago_david_ndim=2).
- reference_dft(절대 binding 기준)는 0 ionic step이라 from-scratch 별도 결정 필요.

### 5. h-BN 시트 굴곡 0.27–0.37 Å (vgcf_hbn_neb.json flag_hbn_corrugation)
- 자유 h-BN 단층은 <0.01 Å 평면이어야 정상. Li-유도 pucker인지 4×4 셀 리플인지
  relax 미완인지 미해결 — h-BN 표면 수치(7 meV) 정량 인용 전 확인.

## 📄 PDF 확보 대기 (원전 미보유 — 웹/재인용 딱지 상태)

| # | 서지 | DOI | 왜 필요한가 |
|---|---|---|---|
| 1 | de Klerk & Wagemaker, Chem. Mater. 28, 7955 (2016) | 10.1021/acs.chemmater.6b03630 | 무질서%–σ 원전 (75% 최적). AIMD 4a/4d decorate 방법 — disorder ensemble 직접 앵커 |
| 2 | Adeli et al., Angew. Chem. Int. Ed. 58, 8681 (2019) | 10.1002/anie.201814222 | Li5.5PS4.5Cl1.5 실험 원전 (9.4 mS/cm) — modelc Cl-rich Rietveld 점유율 ground truth |
| 3 | Deng, Wang, Chu, Luo, Ong, J. Electrochem. Soc. 163, A67 (2016) | 10.1149/2.0061602jes | SQS 반례 원전 (A=0.92) — ordered_vs_disordered 문서 '경계 사례' 논증의 원본 |
| 4 | Kim et al., Nano Energy 124, 109436 (2024) | (SD 링크는 서베이 §1c) | **config-앙상블 신규성 주장의 선행조건** — 6-config 표본화가 분산을 오차막대로 보고했는지 확인 전까지 원고에 신규성 기재 금지 (서베이 §4-3, §5) |
| 5 | Schlem et al., Adv. Energy Mater. 10, 1903719 (2020) | 10.1002/aenm.201903719 | ordered Ea 0.25 eV — li_transport.json 비교 기준의 원전 |
| (6) | Kim rapid-thermal (10.2 mS/cm, liu2022 재인용) | liu2022 참고문헌에서 확인 | 공정–무질서 관계 보강 (우선순위 낮음) |

확보 시 "논문 에이전트"(litdb-curator)로 다이제스트 → 서베이 ⚠딱지 승격.

## 🧠 ML 후속 (트리거 대기 — 데이터 나오면 전체 진행)

> 랩 PPT(TabPFN) 판독에서 나온 계획: kb/projects/ml_opportunities_from_lab_ppt_2026_07.md.
> 각 항목은 **트리거 조건**이 충족되면 착수한다.

### M1. TabPFN 벤치 — codoping 비선형 타깃
- **트리거**: 없음 (지금 가능 — 로컬 WSL/kgy GPU 반나절).
- 내용: champions Δe_post_anneal · litransport bvs proxy를 조성 특징에서 TabPFN으로
  예측, 현행 numpy ridge와 LOOCV 성능표 비교 → 사이트 ML 탭에 병기.
  근거: litdb hollmann2025 (≤10k행/500특징 스윗스팟, 튜닝 0).

### M2. pair CV를 leave-one-dopant-out으로 (codoping_ml v2.1)
- **트리거**: 없음 (코드 수정만).
- 내용: 같은 도펀트를 공유하는 쌍(A–B, A–C)은 비독립 — pair 단위 CV는 누수.
  랩 PPT의 Group-CV 관행 대조에서 발견한 우리 구멍.

### M3. TabPFN 역설계 루프 1회전 → 첫 실측 라벨
- **트리거**: M1 완료 + gabia GPU 여유 (comp1 seeds 종료 후).
- 내용: 가상 후보(1081쌍 × 농도축) TabPFN 스코어링 → 불확실성 페널티로 상위 5쌍
  선별(winner's curse 완화) → UMA 공동치환 슈퍼셀 검증 = codoping 첫 라벨.
  mlip_next_campaigns ①(Li|SE 계면)과 후보 공유.

### M4. disorder 서러게이트 (active learning)
- **트리거**: disorder ensemble d×cfg 표본 ≥ 9 (현재 3) + Kim 2024 PDF 확보.
- 내용: 배열 기술자(anti-site 분포·Ewald·BVS 채널%) → D 예측, 다음 cfg 선택에 사용.

### M5. P2D 물성 export 인터페이스 (랩 P2D 데이터셋과 동기화)
- **트리거**: 랩 후막 전고체 P2D 데이터셋 스키마 확정 (다음주 랩 계획).
- 내용: db/properties(σ·E·ESW)를 P2D 입력 파라미터 포맷으로 내보내는 export —
  DFT(우리)→P2D(랩)→TabPFN 멀티스케일 연결. ⚠ σ는 MLIP 상한임을 명시 필수.

## ✅ 닫힌 항목
- (여기로 이동)
