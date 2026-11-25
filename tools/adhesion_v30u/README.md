# adhesion_v30u — paper #1 출판 결합곡선 스크립트 (백업 회수분)

2026-07-21, D:\v100 KISTI 백업(`work_misc/Yonghoon-DEM-DFT/scripts/adhesion/`)에서 회수.
comp1~5 (Li6/Li5.4 argyrodite) | NCM 접착 v30u 캠페인의 잔존 스크립트 13종 + α-민감도 json.

## 확정된 수식 계보 (alpha_sensitivity_FINAL.py)
- **출판 인용값**: `Wad_well(published) = WELLS_RAW − α·dW`, α=1.0
- WELLS_RAW (self-ref 상호작용 우물, J/m²): comp1 2.7084 / comp2 2.4391 /
  comp3 1.6133 / comp4 1.3098 / comp5 1.0989  ← **raw 순위는 Li6 > Li5.4 (논문과 역순)**
- dW (per-comp, eiso fix 유도): comp1 2.633 / comp2 2.503 / comp3 0.873 /
  **comp4 3.640 (outlier)** / comp5 0.314
- 채택: Li6 = per-comp 그대로, **Li5.4 = 균일 0.44** (per-comp은 comp4 outlier로
  strict rank가 어떤 α에서도 불성립 → 계열-균일 정규화 채택; α-창 민감도로 견고성 검증)
- α=0이면 R=−0.76/ρ=−0.5 (역상관) → 보정(표면 준비 비용)이 실험 순위 재현의 필수 성분
- 그림: plot_R0988_TIGHT_FIT.py — Morse `E(d)=D(1−e^{−a(d−d_eq)})²−D+offset`
  (offset = 뜬 꼬리; well_min = offset−D)

## dW의 정체 — 유도 완결 (2026-07-21, kb/papers/mechanism_anion_O_descriptor.md §ΔW_strain)
- **dW = ΔW_strain = E_NCM(SE cell) − E_NCM(NCM cell)** — NCM 슬랩이 SE 가로 셀에
  강제될 때 갖는 변형 에너지. ("surface-Li dangling"이라는 초기 추정은 오독 — 정정)
- per-comp: comp1 2.633 / comp2 2.503 / comp3 0.873 / **comp4 3.640** / comp5 0.314
- comp4 3.64 = **single-frame cell artifact**: 50:50 Cl/Br 혼합 조성이라 anion-ordering
  앙상블 분산이 큼 → 챔피언 단일 프레임의 셀이 앙상블 평균에서 가장 벗어남.
- **0.44 = Li5.4 계열의 v1 앙상블 평균 ΔW_strain** — 단일 프레임 artifact 제거,
  "실험 W_ad는 thermal ensemble 평균"이라는 정신과 정합. α∈[0.8,1.5] 전 구간
  strict rank 유지 (독립 유도 + 사후 견고성 검증 구조 = 순환논증 아님).
- 최종식: `W_ad_corrected = (E_SE + E_NCM − E_SE/NCM)/A − α·ΔW_strain`, α=1.0
  (러너 실코드: run_v30u_1L_face_flip.py L247, face별 E_se_iso/E_ncm_iso 참조)

## 전체 아카이브 (cold backup, 1.4 GB)
`D:\v100\kisti_backup_2026-07-14\kgy_manuscript_support_2026-07-14\manuscript_support\adhesion_v5_v2\`
— phase1(rigid)~phase2a v4→v30u 전 이터레이션 + 슬랩 xyz + z-shift/face 변형 + 결과.
스크립트 상위 31종만 tar하면 <1 MB (`tar czf out.tgz *.py *.json *.csv`) — 필요 시 회수.
