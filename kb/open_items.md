# 미결 리스트 (Open Items)

> 세션이 바뀌어도 유지되는 미결 사항 추적. 닫을 때 날짜+근거를 남기고 ✅로 옮긴다.
> 등록: 2026-07-27 (MAX 감사 후속).

## 🔴 판정 대기

### 1. 🔴 modelc MD Ea 정본 — **닫는 방법이 무효화됐다 (2026-08-01)**
- **원래 계획**: comp1 멀티시드 보강 → 전 조성 3-seed 통일 → modelc 0.197±0.032 정본 확정.
- **실행함**: kgy 에서 comp1 seed 2/3 완주(6런). 3-seed Ea = 0.2681 ± 0.0576 까지 나왔다.
- **⛔ 그런데 그 값을 쓸 수 없다.** 확산영역 게이트에서 **6/6 전부 케이지**로 판정됐다
  (β 0.17–0.79). 창을 2-50 → 100-200 으로 옮겨도, 시드 MSD 를 평균해도 β 가 0.8 을
  못 넘는다. s3 의 `D(600) 1.36e-06 ≈ D(800) 1.37e-06`(비 1.007) 이 그 증상이었다.
- **따라서 #1 은 '시드를 더 돌면 닫히는' 항목이 아니다.** 저이동도 계에서 200 ps 가
  부족한 게 근본 원인이라, **셀 확대(2×2×2, Li 24→192) 또는 시간 연장** 후에야 닫힌다.
- ~~⚠ 비교 상대인 modelc 0.197±0.032 · b2o3 · LPSOCl 도 **같은 프로토콜**이다(미검사).~~
  → **2026-08-04 일부 판정**: LPSOCl 첫 게이트 검사 — **600 K 이 4시드 앙상블 평균에서
  탈락** (β 0.61, MSD 는 97 Å²@200 ps 로 충분 = 홉 통계 문제; 시드별 0.52~0.98 갈림).
  800 K 0.86 / 1000 K 1.02 통과. → **Ea 0.287±0.024 는 케이지 오염된 600 K 점을 포함** —
  재검토 필요 (paper_first_author_requests_2026_08.md §4 의 선택지 3안).
  **modelc·b2o3 3시드 평균 검사 완료 (v2)**: modelc 0.87/0.93/0.92 · b2o3 0.81/0.83/0.97
  전부 통과 — 단일시드 '아슬' 해소. b2o3 600 K 3시드 D 가 등록 D_600_mean 을 재현(1.039 vs
  1.041e-5). **잔여 이슈는 LPSOCl 600 K 하나** — 30런(lpsocl 600 재실행 포함, 2026-08-04 결정) MTO-β 로 1차 판정, 안 되면 1600 ps 프로브.
  게이트 통과 전까지 전부 인용 보류.
- 근거: `kb/results/mlip_md_diffusive_gate_2026_08_01.md` ·
  `tools/ionic/msd_diffusive_check.py`

### 2. 🟡 comp2 disorder ensemble — **d=0.5 판정 완료 / d=1.0 측정 실패 (2026-08-01)**
- **d=0.50 ✅ 인용 가능**: Ea **0.151 ± 0.068 eV** (config 3개). 확산영역 게이트를
  개별 9/9(β 0.81–1.12) + 온도별 평균 3/3(β 0.92/1.00/0.97) 로 **완전히 통과**.
  MSD 45–280 Å² 로 통계도 충분하다.
  ⚠ 다만 **config 산포가 45%** 다 — "ordered(0.276)보다 낮다"까지만 말하고
  값 자체를 정밀 인용하지 말 것. cfg0 의 0.087 은 아티팩트가 아니라 **실제 산포**였다.
- **d=1.00 ⛔ 측정 실패**: 개별 8/9 케이지(β 0.11–0.93), 평균도 0.27/0.46/0.78.
  겉보기 Ea 0.378 은 케이지 진동을 맞춘 값이라 의미가 없다.
  → **"disorder 를 더 늘리면 Ea 가 다시 오른다"는 비단조성을 주장하면 안 된다.**
- **남은 것**: d=1.0 을 셀 확대/시간 연장으로 다시 재야 추세(0 → 0.5 → 1.0)가 완성된다.
- 등록: `db/properties/comp2_disorder_ensemble.json`

### 3. ~~VGCF 2×2 barrier 행렬 + 기전 판정~~ → ✅ **완료 (2026-07-30)**
- **2×2 행렬**: 1L|1L 0.3567 · 2L|1L(VGCF 2층) 0.1495 · 1L|2L(h-BN 2층) 0.3802 · 2L|2L 0.1473 eV.
  → 209 meV 는 거의 전부 VGCF 쪽 (**−207.2 meV = 98.9%**), h-BN 만 두껍게 하면 **+23.5 meV 악화**.
- **기전 = CONFINEMENT.** 표면 대조군 `Li_on_graphene_2L` = **0.2848 eV** 가 나왔다.
  같은 그래핀 1L→2L 변화가 자유 표면에서는 **+11.9 meV**(NEB 허용오차 ~20 meV 안 → **0**),
  갤러리 안에서는 **−207.2 meV**. 17배 차이 + 부호 반대.
  ⚠ +11.9 meV 를 '약간 악화'로 인용하면 안 된다 — 0 과 구별 안 되는 값이다.
- **논문 문장 확정**: "이중층 탄소 기판이 유리하다"(일반화) ❌ →
  "**갇힌 Li 에 대해** 벽 두께가 유리하다"(VGCF 다발 구조 특화) ✅
- 등록: `db/properties/vgcf_hbn_neb.json` `mechanism_verdict_2026_07_30` ·
  `vgcf_mechanism_origin.csv` · 그림 `docs/figures/vgcf_hbn/vgcf_mechanism.png` ·
  정리 `kb/results/vgcf_hbn_gallery_mechanism_2026_07_30.md`
- **남은 것(별도 항목 아님, 인용 규율)**: 3L 포화 미확인 → 0.147 eV 는 '수렴값'이 아니라
  **2L 값**으로만 인용. h-BN 굴곡은 #5 로 계속.

### 4. SDCP complex_doped_v2 DFT relax — k 2×2×1 재실행 수렴 여부
- k 1×1×1 정체(150 iter, 0.0837 Ry) → 2×2×1로 재시작. accuracy가 0.08을 뚫고
  내려가는지 확인 필요. VRAM 46.9/48 GB로 임계 (OOM 시 diago_david_ndim=2).
- reference_dft(절대 binding 기준)는 0 ionic step이라 from-scratch 별도 결정 필요.

### 5. h-BN 시트 굴곡 0.27–0.37 Å (vgcf_hbn_neb.json flag_hbn_corrugation)
- 자유 h-BN 단층은 <0.01 Å 평면이어야 정상. Li-유도 pucker인지 4×4 셀 리플인지
  relax 미완인지 미해결 — h-BN 표면 수치(7 meV) 정량 인용 전 확인.

### 6. ~~LPSOCl COHP 곡선 원자료 회수~~ → ✅ **완료 (2026-07-29)**
- 회수 성공(md5 대조 일치). N 이 `lpsocl_icohp.json` 과 정확히 일치:
  P-S 19 · P-O 1 · Li-S 106 · Li-Cl 42 · Li-O 5 · S-S 54.
  산출: `db/properties/lpsocl_cohp_curves_origin.csv` ·
  `docs/figures/icohp/lpsocl_COHP_curves.png` · webapp Bonding 탭 실시간 렌더.
- **읽을 때 남는 제약(⚠ 인용 전 필독)**: COHPCAR 격자가 −15.03 eV 에서 시작해서
  **곡선 면적 ≠ ICOHP** 다. 창 안 비율 — P-O **30%** · Li-Cl 45% · Li-O 47% ·
  P-S 81% · Li-S 89%. 곡선은 "어느 에너지에서 결합/반결합인가"만 말하고,
  세기는 ICOHP 표(적분값)에서 인용한다. 그림·사이트 모두 이 커버리지를 표기한다.
  더 넓은 창이 필요하면 **LOBSTER 재실행**(COHPstartEnergy 확대)이 필요하다.
- 물리 판독: 모든 패널에서 반결합 상태가 E_F 위(비점유) — host 결합이 깨끗하다.
  P-O σ* 는 +3.5 eV. Li-Cl 은 −4.3 eV 한 봉우리에 몰려 있고 Li-S 는 −2~−9 eV 에
  넓게 퍼진다(같은 세기대, 다른 성격).

### 6b. ⏳ 예전 항목 원문 (참고용 — 회수 절차)
- `COHPCAR.lobster` 가 gabia
  `/data/work/runs/lpsocl_dft/lobster_ext/` 에만 있고 수십 MB라 repo 로 못 옮긴다.
- **회수 경로**: gabia 에서 `tools/figures/extract_cohp_curves.py` 로 패널 곡선만
  압축 CSV(~20 KB)로 뽑아 gzip+base64 전송 → `db/properties/lpsocl_cohp_curves_origin.csv`.
  그러면 webapp Bonding 탭이 자동으로 그리고,
  `tools/figures/fig_lpsocl_cohp_curves.py` 가 논문용 PNG 를 낸다.
- **⚠ 정규화 규약 주의**: 신규 추출기는 **결합당 평균**(∫|E_F = −ICOHP/bond, 자기일관),
  구형 `docs/figures/icohp/*_COHP_curves.csv`(modelc·nd·b2o3)는 **합(sum)** 이다.
  둘을 같은 그림/표에서 높이 비교하면 안 된다 (사이트는 '구형 CSV' 배지로 구분 표시).
- **회수 후 확인**: 추출기가 찍는 N 이 `lpsocl_icohp.json` 의 N(P-S 19 · Li-S 106 ·
  Li-Cl 42 · Li-O 5 · S-S 54 · P-O 1)과 일치해야 한다. 어긋나면 P–S dmax(기본 2.6 Å)를
  조정해야 하는 신호다.

### 7. litdb 인덱스 정합 — digest 156편 중 **67편이 INDEX 어디에도 없다** (2026-07-29 감사)
- **사이트·db 는 멀쩡하다.** webapp `list_papers()` 는 디렉터리를 직접 읽어 156편 전부 잡는다
  (파일 수 = 사이트 수 = 156). 문제는 **마크다운 인덱스 두 개만** 뒤처져 있다는 것.
- `litdb/INDEX.md` (갱신 2026-06-23 표기, 파일 mtime 07-28): **67편 미등재**.
  `litdb/INDEX_DEM_snapshot_2026-07-16.md` 도 그 67편을 담지 않는다.
- `litdb/comparison_vs_ours.md`: **98편 미언급** (우리 값 대비가 없는 digest).
- 미등재 67편의 대부분(≈63)은 **DEM·기계·건식전극 클러스터** — SE 캠페인과 축이 달라
  argyrodite 전용 INDEX 에 안 들어간 것이 설계상 자연스럽다. 다만 **SE 축 4편은 진짜 누락**:
  `huang2022_li2sis3_anomalous_conductivity_bvse` ·
  ~~`lee2024_multicomponent_argyrodite_mixed_oxidation_mtp`~~ **✅ 해소 2026-08-04** (INDEX 행 + comparison `[Lee24MO]` 키
  + 축 A 4행 신설; 본문 실물 독립 검증 §11 = 교정 6·신규 16) ·
  ~~`kim2026_hts_li3sc2po43_coating_midni_ncm`~~ **✅ 해소 2026-08-03** ·
  `yun2023_deciphering_degradation_halide_vs_sulfide`
  — 앞 3편은 2026-07-28 캠페인에서 우리가 직접 먹인 것들이다. **남은 진짜 누락 2편: huang2022 · yun2023.**
- **판정**: 급하지 않다(사이트가 정본). 다만 논문 에이전트가 digest 를 쓸 때
  **INDEX 갱신을 같이 하도록 되어 있는데 그게 최근 3건에서 안 됐다** — 에이전트 지침 점검 필요.
  DEM 클러스터는 별도 인덱스로 분리 유지가 맞다(축이 다름).

### 8. lpscl16 PDOS 의 VB-top DOS 가 비정상적으로 작다 (2026-08-04 발견 · 판별 대기)
- gap 정합 검사 중 발견: lpscl16 DOS/PDOS 파일의 **CB 에지는 정본 2.099 와 정합**하는데,
  **E=0(VBM) 에서 DOS 가 0.019 states/eV** — lpsocl(1.59)·b2o3(2.82)의 **1/80~1/150**.
  원소투영·총DOS 모두 동일 → 투영 문제 아님.
- 두 가설: (a) modelc VB top 이 실제로 뾰족한 단일 밴드 꼭대기(분산 큰 밴드, 물리) —
  anti-site 배치 차이로 가능 (b) VBM 정렬 기준이 이 DOS 런과 다른 런에서 옴(아티팩트).
- **판별**: 서버의 modelc nscf 고유값에서 VBM k-점 근방 밴드 분산 확인, 또는 dos 재생성
  시 자체 고유값 VBM 으로 재정렬. 판별 전까지 **lpscl16 VB-top DOS '모양' 인용 보류**
  (gap·적분량 인용은 무관).
- 맥락: 세 PDOS 파일의 gap 인코딩 자체는 셋 다 정본과 정합 ✅ (2026-08-04 검사).

## 📄 PDF 확보 대기 (원전 미보유 — 웹/재인용 딱지 상태)

| # | 서지 | DOI | 왜 필요한가 |
|---|---|---|---|
| ~~1~~ | ✅ **확보·다이제스트 완료 (2026-07-28)** de Klerk et al. | 10.1021/acs.chemmater.6b03630 | digest: deklerk2016_diffusion_site_disorder_argyrodite.md — 75%는 min-rate 지표·비단조·단일 배열이었음이 판명. ✅ SI 통합 완료(2026-07-28) — Tables S1-S3 전표 수록, figure-read 값 SI 정밀값으로 교정(75/50 비 1.99x 확정, 300K σ* Cl 최대 교정) |
| 2 | Adeli et al., Angew. Chem. Int. Ed. 58, 8681 (2019) | 10.1002/anie.201814222 | Li5.5PS4.5Cl1.5 실험 원전 (9.4 mS/cm) — modelc Cl-rich Rietveld 점유율 ground truth |
| 3 | Deng, Wang, Chu, Luo, Ong, J. Electrochem. Soc. 163, A67 (2016) | 10.1149/2.0061602jes | SQS 반례 원전 (A=0.92) — ordered_vs_disordered 문서 '경계 사례' 논증의 원본 |
| ~~4~~ | ✅ **확보·다이제스트 완료 (2026-07-28)** Kim et al., Nano Energy 124, 109436 | 10.1016/j.nanoen.2024.109436 | **신규성 판정 완료**: enumerate 6 특성배열+단일 random supercell, config-분산 오차막대 **없음** → 우리 다중 config×멀티시드 산포 보고는 신규 기여로 원고 기재 가능 (digest: kim2024_mtp_argyrodite_disorder_gb.md) |
| ~~5~~ | ✅ **확보·다이제스트 완료 (2026-07-28) — 단 귀속 오류 판명** Schlem et al. AEM 1903719 | 10.1002/aenm.201903719 | 실물 = **Li3MCl6(Y,Er) 기계화학 논문, LPSCl 데이터 0건** → 'ordered 0.25' 앵커 철회, li_transport 정정 완료. '무질서=공정변수'의 최정밀 외부 실증(Er 무질서 88→2.5% 연속 조절)으로 가치 전환. **신규 미결: LPSCl 0.25/0.22의 진짜 원전 추적** (후보: Schlem 2019 계열 argyrodite 논문 — 서지 확인 필요) |
| (6) | Kim rapid-thermal (10.2 mS/cm, liu2022 재인용) | liu2022 참고문헌에서 확인 | 공정–무질서 관계 보강 (우선순위 낮음) |
| 7 | **Chouchane, Yao, Cronk, Zhang, Meng**, "Improved Rate Capability for Dry Thick Electrodes through Finite Elements Method and Machine Learning Coupling", *ACS Energy Lett.* **2024, 9, 4** | (미확인) | **DEM/미세구조 트랙 직접 선행** — `Library of Real Particles → Stochastic Generation → FEM → 입자별 평균 SOD → Random Forest` 워크플로. Chouchane 은 ARTISTIC(Franco) → Meng 계보. `talks/moon2026_cau_...` 슬 32가 "Reference Work"로 인용. 2026-08-03 덱 재판독으로 발견 |

확보 시 "논문 에이전트"(litdb-curator)로 다이제스트 → 서베이 ⚠딱지 승격.
진행: #1 de Klerk·#2 Adeli·#3 Deng·#35쌍·#36쌍(Schlem 추정) — 2026-07-28 큐레이터 5기 가동.

### 스크리닝 방법론 논문 위시리스트 (지도 피드백 "co-doping screening develop" 지원)

| # | 서지 | DOI | 왜 |
|---|---|---|---|
| S1 | Xiao, Wang, Ceder et al., *Joule* 3, 1252 (2019) "Computational screening of cathode coatings" | 10.1016/j.joule.2019.02.006 | **cascade의 직계 조상** — 양극 코팅 HT 스크리닝의 표준 프레임 (안정성+ESW+수송 게이트) |
| S2 | Zhu, He, Mo, *ACS Appl. Mater. Interfaces* 7, 23685 (2015) | 10.1021/acsami.5b07517 (구기재 5b01004는 오기 — PDF 실물 확인) | **grand-potential ESW 방법 원전** — 우리 oxidation CSV가 쓰는 바로 그 방법 |
| S3 | Richards, Ong, Ceder et al., *Chem. Mater.* 28, 266 (2016) "Interface stability" | 10.1021/acs.chemmater.5b04082 | pseudo-binary 계면 반응성 — MLIP 캠페인 ①(Li\|SE)의 열역학 짝 |
| S4 | Sendek et al., *Energy Environ. Sci.* 10, 306 (2017) "12k candidates" | 10.1039/C6EE02697D | **ML 스크리닝 대표작** — TabPFN 노선의 선행, 발표 인용 앵커 |
| S5 | Kahle, Marcolongo, Marzari, *EES* 13, 928 (2020) HT-AIMD 스크리닝 | 10.1039/C9EE02457C | AIMD 기반 HT의 방법 규율 (수렴·통계) — 우리 MD 규율과 대조 |
| S6 | Fujimura et al., *Adv. Energy Mater.* 3, 980 (2013) | 10.1002/aenm.201300060 | ML×전도도 예측의 원조 — 역사 앵커 |
| S7 | Ong et al., *EES* 6, 148 (2013) Li₁₀±₁MP₂X₁₂ family | 10.1039/C2EE23355J | 조성족 치환 스크리닝 원형 (LGPS M/X 스캔) |

## 🧠 ML 후속 (트리거 대기 — 데이터 나오면 전체 진행)

> 랩 PPT(TabPFN) 판독에서 나온 계획: kb/projects/ml_opportunities_from_lab_ppt_2026_07.md.
> 각 항목은 **트리거 조건**이 충족되면 착수한다.

### M1. TabPFN 벤치 — codoping 비선형 타깃
- **트리거**: 없음 (지금 가능 — 로컬 WSL/kgy GPU 반나절).
- 내용: champions Δe_post_anneal · litransport bvs proxy를 조성 특징에서 TabPFN으로
  예측, 현행 numpy ridge와 LOOCV 성능표 비교 → 사이트 ML 탭에 병기.
  근거: litdb hollmann2025 (≤10k행/500특징 스윗스팟, 튜닝 0).
  + [Sendek17 선례 이식] X-randomization(랜덤 대비 농축배수로 보고) + cR²_p
  유의성 — 소표본(그들 40 ≈ 우리 47) 정직성 지표의 인용 선례 확보.

### M2. pair CV를 leave-one-dopant-out으로 (codoping_ml v2.1)
- **트리거**: 없음 (코드 수정만).
- 내용: 같은 도펀트를 공유하는 쌍(A–B, A–C)은 비독립 — pair 단위 CV는 누수.
  랩 PPT의 Group-CV 관행 대조에서 발견한 우리 구멍.

### M3. TabPFN 역설계 루프 1회전 → 첫 실측 라벨
- **트리거**: M1 완료 + gabia GPU 여유 (comp1 seeds 종료 후).
- 내용: 가상 후보(1081쌍 × 농도축) TabPFN 스코어링 → 불확실성 페널티로 상위 5쌍
  선별(winner's curse 완화 — [Sendek17]의 적용영역 d/ε/A 3지표가 기성 구현체,
  P_LR vs d 그림 양식 그대로 이식) → UMA 공동치환 슈퍼셀 검증 = codoping 첫 라벨.
  mlip_next_campaigns ①(Li|SE 계면)과 후보 공유.

### M4. disorder 서러게이트 (active learning)
- **트리거**: disorder ensemble d×cfg 표본 ≥ 9 (현재 3). ~~Kim 2024 PDF~~ ✅ 확보 완료(2026-07-28) — 기술자 설계 시 그들 E_rel·Boltzmann 가중 방식 참조 가능.
- 내용: 배열 기술자(anti-site 분포·Ewald·BVS 채널%) → D 예측, 다음 cfg 선택에 사용.

### M7. MD 프로토콜 업그레이드 2건 (Kahle 2020 이식)
- **트리거**: comp1 멀티시드 수확 시 함께 적용 (코드 반나절).
- 내용: ① MSD 피팅창 t'-스캔 1회 검증(우리 2-50 ps 고정창이 창 길이에 둔감함을
  데이터로 입증 — Kahle Fig S3 양식) ② Ea에 Bayesian 오차 전파(현행 시드 std 보완).
  근거: kahle2020 digest §3 — per-material 자동 수렴판정·블록 분산 SE의 원전.

### ~~M6~~. ✅ cascade 양극 반응성 게이트 (2026-07-28 완료 — 결과 회수 대기)
- **검증 통과**: 닫힌계 pseudo-binary ΔE_rxt로 LPSCl/LCO **만충 −322.7 (Xiao −339, 0.95×) /
  반충 −454.9 (−493, 0.92×)**, 리튬화 순서(반충이 더 발열)까지 재현.
  반응식도 `Li₂S + Li₃PO₄ + Co₉S₈` 로 물리적으로 타당.
- **교훈(기록용)**: 초판을 개방계 `GrandPotentialInterfacialReactivity` + 전위 스캔으로 짰다가
  −810~−1544 meV/atom 이 나왔고, V=4.30 반응식이 `Li6PS5Cl -> 6 Li + SCl + 0.5 P2S7 + 0.5 S` 로
  **양극이 아예 빠진 자체분해**였다. Li 저장소를 열면 코팅 탈리튬 분해가 상호반응을 압도한다.
  xiao2019 digest 227번 줄이 ΔE_rxt를 "**닫힌계**"로, 222번 줄이 만충/반충을 **조성 축**으로
  명시하고 있었다. → **개방계는 Li 음극 쪽 도구, 양극 F4 게이트는 닫힌계**.
- **전수 완주**: 47 코팅 × {LiCoO₂, Li₀.₅CoO₂} = **94쌍** (gabia, 2026-07-28).
- **남은 것**: gabia의 `db/properties/cathode_reactivity_cascade.csv` 를 repo로 회수 →
  cascade 깔때기에 **G6 계면 반응성** 게이트로 조인. 판정 기준은 "몇 종이 100 meV를 통과했나"가
  아니라 **"host LPSCl(−323)보다 계면 반응성이 완화되는 코팅이 있는가"** (S1 성공조건 ②).
  ⚠ 컷 근처 ±20 meV 순위 주장 금지 (Xiao 100 meV는 관례컷 + Sundar 2025의 "분해산물 전자전도도
  미고려" 비판을 그대로 받음).

### M5. P2D 물성 export 인터페이스 (랩 P2D 데이터셋과 동기화)
- **트리거**: 랩 후막 전고체 P2D 데이터셋 스키마 확정 (다음주 랩 계획).
- 내용: db/properties(σ·E·ESW)를 P2D 입력 파라미터 포맷으로 내보내는 export —
  DFT(우리)→P2D(랩)→TabPFN 멀티스케일 연결. ⚠ σ는 MLIP 상한임을 명시 필수.

## 🎤 심포지엄 대응 (2026-07-28 신설 — T1–T8)

전지기술 심포지엄 2026 기술세션 3-3(이상욱, 성균관대) · 3-4(문장혁, 중앙대) 덱 분석에서 나온 실행 항목.
전체 근거·좌표는 **`kb/projects/symposium_2026_competitive_analysis.md`**,
digest는 `litdb/talks/`, 벤치마크 수치는 `db/properties/external_benchmarks_symposium_2026.json`.

| ID | 항목 | 왜 (우리 약점/기회) | 비용 | 우선 |
|---|---|---|---|---|
| **T1** | **UMA 외삽 대리지표 설계** (재정의 2026-07-28) | 우리 MLIP-MD는 **스냅샷 수준 외삽 판정이 전무**하다. ⚠ 이상욱 랩의 γ(=γ_select 2 / γ_break 10→5→2)는 **MTP 선형 기저 위 maxvol·D-optimality 정의라 UMA(비선형 등변 GNN)에는 정의 자체가 없다** — 숫자 이식 불가. 이식할 것은 논리뿐: ①대리지표 하나 정한다 ②**선별 문턱과 중단 문턱을 분리** ③중단 문턱을 조여 수렴 판정. 후보 대리지표: 궤적 스냅샷 UMA vs DFT 단일점 오차 분포 / 앙상블 분산 | 중 | **1** |
| **T7** | **3계층 스킬 로딩** (Level 1 YAML 메타 ~100토큰 신설) | 우리는 Level 2만 있다(CLAUDE.md + tools/). 매 세션 전체를 훑는 구조적 이유 | 소 | **1** |
| **T2** | **ICOHP 기반 P–S 약화 기술자** | `air_hsab` 정성 tier를 정량으로. 그들은 양성자화 시 ICOHP −6.43 → −4.69 eV (27% 약화) | 중 | 2 |
| **T4** | **반응좌표 기반 검증셋** | pre-mixing→reactants→TS→products 단계별 UMA vs DFT 단일점. 학습이 아니라 **검증**으로 전용 | 소 | 2 |
| **T5** | **영역분해 MSD** | 계면/벌크 구획 마스크로 D 분리. 기존 파이프라인 확장만 | 소 | 2 |
| **T3** | **Li\|LPSCl 반응 MD (UMA)** — 프로토콜 확정 | 완전 공백 축. **셀** Li(100)‖LPSCl(100) 직접접촉, 횡단면 ~3 nm², Li 6 nm ‖ LPSCl 10 nm (~7,000원자), NVT **350 K**, **≥20 ns**. ⚠ **우리 표준 200 ps로는 결정 핵생성(11 ns)을 절대 못 본다 = 결과가 없다.** 비용 초과 시 [두께 절반 + 20 ns] > [두께 유지 + 2 ns]. **1순위 관측량은 D가 아니라 잔존 PS₄ 층수 vs 시간**(z-bin + P–S 거리컷; **층 간격 ≈0.5 nm = a/2** 로 nm 환산 — 2026-08-04 검산). 착수 전 게이트: 1 ns UMA MD → 20 ps 스냅샷 → QE 단일점 대조 (UMA는 Li 금속‖황화물 반응 영역에서 검증된 적이 없다 — Li₃N 편향 전례). 벤치마크: interphase ~11 nm · Li₂S 결정화 · D비 0.36. **★ 2026-08-04 실물 검증 추가**: ① **구획 마스크를 "계면 ±d"로 잡지 말 것** — 결정 Li₂S 핵은 **계면에서 LPSC 쪽 ~3 nm 안쪽(z≈75 Å, 초기 계면 z≈105 Å)**에서 시작한다 → **LPSC 쪽 0–5 nm 를 독립 bin** ② **초기 접촉 간격·평형화 프로토콜을 명시**할 것 (원논문은 *"direct contact"* 한 마디뿐, 이완 절차 0줄 → "즉시 분해"가 초기 배치 의존일 수 있음) | 대 | **2** |
| **T8** | **P2D 파라미터 export** (=M5) | 문장혁 랩 발표로 **소비자가 특정됨**. 우리가 파라미터 생산, 그들이 셀 스케일 소비 | 중 | 3 |
| **T6** | **litdb 그래프층** | 멀티홉 가설 생성 부재. digest **위에** 얹기(대체 아님) — 방법 맥락·인용금지 규칙 보존이 조건 | 중 | 4 |

**하지 않기로 한 것**: CSP(문제설정 다름) · 자체 MLIP 학습(UMA 횡단 속도가 우리 강점) ·
셀 스케일 FEM(상하류 관계 유지).

### T9–T12 — 이상욱 랩 논문 실물에서 추가된 항목 (2026-07-28)

| ID | 항목 | 근거 (논문 실물) | 비용 | 우선 |
|---|---|---|---|---|
| ~~**T9**~~ | ✅ **완료 (2026-07-28)** — 계면 상대 5종 {양극 만충/반충, **SE(LPSCl)**, **Li 음극**, LiNbO₃ 대조} 47종 전수 | **M6의 'vacuous' 판정을 우리 데이터로 확정 반증.** 축별 탈락: 양극 만충 **2** · 반충 **3** · **SE 29** · **Li 음극 35** · LNO 4. 코어 생존자 **11 → 3종**(CaF₂·LiF·MgO). 앵커 재현도 정확 — LPSCl vs Li −541.5 (Lee 2024 Li₆PS₅I −539.2, 0.4% 차) · vs LNO −108.8 (−107.5, 1.2%). 상세: **판정 이력 V1** | — | ✅ |
| ~~**T10**~~ | ⛔ **폐기 (2026-07-28)** — E_hull 필터가 우리 풀에서 무력 | **예측이 빗나갔다.** hull ≥ 50 meV 탈락 **0종**(최대 CrO₃ 46, 나머지 ~0). 원인은 기준이 아니라 **풀**이다 — 47종이 애초에 안정한 흔한 이성분 화합물로 큐레이션돼 있어 어떤 열역학 안정성 기준도 통과한다. → 음성 결과를 `pool_provenance` 논증의 **정량 근거**로 전환. ⚠ '안정성이 안 중요하다'가 **아니다** — 발견 깔때기(Kim 2026은 ECW에서 94.3% 제거)에선 압도적으로 센 게이트고, 우리 풀은 그 단계를 이미 통과한 상태에서 시작할 뿐. 상세: **판정 이력 V2** | — | ⛔ |
| **T11** | 🔶 **부분 완료 (2026-07-28)** — pseudo-binary ΔE_H₂S 47종 계산됨 | 최악군이 전부 알칼리·알칼리토 산화물(Na₂O −192 · BaO −160 · SrO −116 · Li₂O −108 · CaO −74 meV/atom)로 화학적으로 타당. 불화물은 전부 0 근처. Li₂O·CaO는 SE 축에서도 탈락 = 두 축이 같은 화학을 다른 각도에서 본다. **⚠ 남은 것: host LPSCl 자체의 ΔE_H₂S 기준선** — 없으면 '개선인지'를 말할 수 없다. ⚠ 이상욱 랩 반응 MD(SevenNet 500 ps, ICOHP, Sn 유인)와 **같은 것이 아니다**(0 K 열역학 vs 동역학) | 소 | **1** |
| **T12** | **van Hove 상관함수** MSD 파이프라인 추가 | Lee 2024 Fig 3e: "cage에 갇힘 vs 자유 확산"을 MSD 기울기가 아니라 **거리–시간 지도**로 판별. 우리 disorder_ensemble의 "ordered frozen" 판정을 선명하게. **✅ 도구 확정 (2026-08-04 ESI): `pymatgen-diffusion`**(Note S4, Zhu 2015) · G_s/G_d 분해 eq S4 — 그들도 **G_d 결과는 미게재**라 우리가 G_d 를 그리면 그 자체로 신규. ⚠ 도입 시 **컬러 정규화 기준 명시 필수**(§11-N8). ⛔ **2026-08-04 [Jun22] 본문 실물 검증 — 판정축은 self-part 한정**: Jun 2022 Fig 4(c) 는 **σ 가 10⁴ 배 다른 세 배열의 G_d 지도가 육안 구별 불가**였다(§20.7). G_s 는 갇힘을 확실히 가르지만(⚠ 띠 중심 ~4 Å, 5 Å 은 상한) **G_d 는 전도도 판별력이 없다** → 우리 게이트 판정에는 **G_s 만** 쓰고, G_d 는 협동성의 정성 서술로만. `[Lee24MO]`·`[Kim25CSP]` 에 이어 **3건 연속 같은 방향** | 소 | 2 |
| **T14** 🆕 | **Li–(S,Cl)₄ CSM(연속대칭척도)을 기존 UMA-MD 궤적에 후처리** (2026-08-04 신설) | Kim 2025 CSP 본문 실물 검증(`kim2025_csp…` §19 N5): 그들의 인과사슬 `edge-sharing → 왜곡↑ → D↑` 에서 **첫 화살표는 Li₄SiGeS₆에서 끊기고 뒤 고리(CSM↔D)만 남는다** — Fig 5b 최고 CSM(5.5–6.0)은 edge 가 아니라 **corner rank 8·9·10** 이고, 그 셋이 Fig 3d 에서 **corner 중 유일하게 D≠0**. → **CSM 은 연결방식의 부산물이 아니라 독립 기술자**이므로, corner/edge 축이 정의되지 않는 우리 host 에서도 **의미가 있다**. 구현은 pymatgen `chemenv` 또는 SI eq 10 직접(≈30줄), **새 시뮬레이션 0**(기존 600 K 궤적 재사용). BVSE 채널 % 와 **교차검증** — 두 지표가 어긋나는 도펀트 자체가 결과. ⚠ 그들은 **같은 조성 안 폴리모프 줄세우기로만 검증** → 47종 횡단 사용은 논문 미검증 용법, "농도별 상대 지표"로만 | 소 | 2 |
| **T15** 🆕 | **순위·비율 주장에 "시뮬레이션 온도의 D" 를 의무 병기** (2026-08-04 신설) | Kim 2025 LYC 본문 실물 검증(`kim2025_li3ycl6…` §20a·N1): Fig 4 의 600 K 총 MSD 는 기보고 4골격이 **92–115 Å² = ±12 %** 인데 300 K 외삽 σ 는 **3.4–18.8 = 5.5×** 로 벌어지고, **hcp_2 는 600 K 최속인데 300 K 에선 밑에서 둘째로 순위가 뒤집힌다**. 즉 논문 제목 주장("hcp > ccp")이 전부 **외삽이 만든 것**인데 Ea 는 본문에 한 개도 없다. 같은 논문의 antisite 축도 동일(600 K 총 MSD 103 → 108 인데 σ 12.6 → 3.6). **우리도 600/800/1000 K → 300 K 외삽이라 노출이 같다.** → 규율: σ 비교표·그림에 **T_sim(600 K)의 D 열을 함께** 싣고, `D(600 K)` 서열과 `σ(300 K)` 서열이 어긋나면 **그 불일치를 결과로 기술**한다. 첫 적용 대상 = **Nd σ-drop 0.52×**(Ea 0.224≈0.227 불변 → prefactor 지배 서사가 600 K D 에서도 보이는지). 구현은 `tools/ionic/` 기존 산출물 재집계 = **새 시뮬레이션 0** | 소 | **1** |
| **T13** 🆕 | **MSD 생산길이 200 ps 의 타당성 재검토** (2026-08-04 신설) | Lee 2024 ESI 실물: 그들은 **NPT 10 ns = 우리의 50배**. 우리 창(2–50 ps)이 고정이라 길이 자체가 곧바로 치명적이진 않지만, **느린 계에서 창 안의 유효 hop 수가 충분한지** 점검이 필요. 참고로 그들 Fig S5(a) 는 10 ns 에도 MSD 26 Å²(RMS ~5 Å)에 그친다 — **길이만으로 해결되지 않는다**는 반증이기도 하다 | 중 | 3 |

> 🔑 **T9·T10·T11은 셋 다 비용이 작고 셋 다 우리 깔때기의 약점을 직접 친다.** M6 인프라를
> 그대로 재사용하므로 묶어서 한 번에 돌리는 것이 맞다.

> 🔁 **2026-08-04 · Lee 2024 ESI 29 pp 실물 검증이 T10·T11 의 성격을 바꿨다**
> (`litdb/papers/lee2024_multicomponent_argyrodite_mixed_oxidation_mtp.md` §12):
> - **T10 (E_hull)** — 이미 V2 로 폐기됐지만, **애초에 베낄 레시피 자체가 없었다**:
>   ESI 29 pp 전체에서 `hull`·`convex`·`synthesiz` 검색 **0회**. 어떤 상도표·참조 DB·functional 로
>   hull 을 잡았는지 **본문에도 ESI 에도 기술이 없다.** → 폐기 판정과 무관하게, 이 논문을
>   **E_hull 방법 출처로 인용하면 안 된다.**
> - **T11 (ΔE_H₂S)** — ⛔ **'그들 Table S4 값을 이식한다'는 선택지가 사라졌다.**
>   ESI Table S3/S4 를 85행 전수 전사해보니 **할로겐을 분해하지 못한다**: Cl↔Br 8쌍 중 **7쌍 계면
>   3값 완전동일**, D₁.₅ 혼합비 뒤집기 **7/7 완전동일**, I/Cl/Br 3종 통째 동일 골격 4개
>   (그런데 같은 묶음 σ 는 최대 **3.18×** 차). 우리 축은 **Cl-rich** 이므로 **직접 계산 필수로 승격.**
>   ✅ 다만 우리 T9 앵커 재현(−541.5 vs −539.2, −108.8 vs −107.5)은 **여전히 유효**하다 —
>   그 앵커는 **모체 Li₆PS₅I 단일 조성**이라 할로겐 분해 문제와 무관하다.
> - 전수 데이터는 `db/properties/lee2024_si_84_structures.csv`(85행), 재현 코드는
>   `tools/litdb/lee2024_si_tables_transcribe.py`.

### ⚠ σ 절대값 규율 — 근거 재정의 (2026-07-28)

지금까지 "MLIP σ 절대값 인용 금지"의 근거는 `kim2024`(훈련 functional에 따라 σ₈₀%가 **8배** 갈림)
하나였다. `lee2024` ESI Table S1이 **반대 방향의 데이터**를 준다:

| 조성 | AIMD | MTP_optB88 | 실험 |
|---|---:|---:|---:|
| Li₆PS₅I | 0.84 | **0.001** | **0.001** |
| Li₆PS₅Cl | 4.6 | **2.46** | **2.3–2.5** |
| Li₃YCl₆ | 14 | **0.56** | **0.51** |

**optB88-MTP는 8개 계에서 실험과 잘 맞고, 크게 틀리는 쪽은 AIMD다**(Li₆PS₅I에서 840배).

→ 정확한 명제: **"MLIP σ 절대값은 (a) 훈련 functional이 그 계에 맞고 (b) 같은 물질군에서
실험 검증을 거친 경우에만 신뢰할 수 있다."**
**우리 UMA는 둘 다 미충족**(OMat24 = PBE 계열이라 optB88 아님 · 우리 계 실험 대조 없음)
→ **인용 금지 규율 유지. 단 이유가 "MLIP는 원래 못 믿는다"가 아니라 "우리 설정이 검증되지
않았다"로 바뀐다.** 규율이 약해지는 게 아니라 정확해지는 것이고, **T1의 필요성이 커진다**.

### 이상욱 랩 논문 확보 위시리스트 (사용자가 탐색·제공 예정)
| 순위 | 논문 | 왜 |
|---|---|---|
| ~~1~~ ✅ | **Nano Convergence 2026, 13, 27** — 코팅 스크리닝 (**17,230 Li·O 산화물** → Li₃Sc₂(PO₄)₃) | **확보·정독 완료** (`litdb/papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md`). ⚠ 종전 표기 '17,233 Li-P-S-O'는 덱 저해상도 전사 오류 — 2026-08-03 철회 |
| 2 | **Adv. Funct. Mater.** (revision) — argyrodite 가수분해 SevenNet | T2 방법 원본 |
| ~~3~~ ✅ | ~~**Chem. Eng. J.** (under review)~~ → 실물은 **SSRN preprint 6020397 (저널명 없음)** — Li\|argyrodite 계면 MTP | **확보·정독 완료** (`litdb/papers/kim2026_li_argyrodite_sei_reactive_md.md`; **본문 실물 독립 검증 2026-08-04**, inbox #3·폴더 `이상욱`). ⚠ "Chem. Eng. J. under review"는 **덱 표기일 뿐 논문에 근거 없음** — 인용 시 "[Kim, SSRN preprint 6020397, 미심사]" 병기. **⛔ SI 미확보 확정** (프리프린트의 SI 링크가 공란 → 대안은 figshare 원자료 `10.6084/m9.figshare.30272386.v1`) |
| ~~4~~ ✅ | **JACS 2025, 147, 47381 — 준안정 3기술자** | **확보·정독 완료 + 본문 실물 독립 검증 2026-08-04** (`litdb/papers/kim2025_csp_metastable_edge_sharing_sse.md` §19). ⚠ **SI 24 pp 실물은 아직 미확보** — Table S1·S2, Fig S1–S12, eq 1–11 은 2026-07-28 판독 승계 |
| 5 | **Adv. Energy Mater.** (revision) — Dynamic properties 후속 | **Q5: config-variance 오차막대 추가됐나** — 우리 신규성 주장의 유효범위가 걸림 |
| 6 | Rare Metals 2025, 44, 2366 | CSP 보조 |
| 7 | arXiv:2601.04746 — BEARS 스킬 3계층 | T7 실측치 |

### 🔁 판정 정정 이력 (우리가 냈다가 뒤집은 판정)

웹앱 **`/benchmarks` → 판정 정정 이력**에 ①주장 →②무엇이 틀렸나 →③어떻게 알았나 →④지금 무엇을 아나
형식으로 전문 수록. 여기엔 색인만 둔다.

| ID | 무엇을 뒤집었나 | 근거 |
|---|---|---|
| **V1** | M6 계면 게이트 'vacuous' 판정 철회 — 가장 쉬운 상대(양극)만 계산한 결과였다 | Kim 2026 Table S1 + 우리 T9 전수 |
| **V2** | T10(E_hull) 예측 빗나감 — 원인은 기준이 아니라 큐레이션된 풀 | 우리 T10 전수 (음성 결과) |
| **V3** | σ 규율 근거 재정의 — kim2024만으론 절반. AIMD가 840× 틀리는 쪽이다 | lee2024 ESI Table S1 |
| **V4** | T1을 'γ 확보' → 'UMA용 대리지표 설계'로 재정의 — γ는 MTP 전용이라 정의 자체가 없다 | kim2026 SEI 실물 |

> 📌 **덱 정정 원장(외부 6건)과 나란히 둔다.** 한쪽만 있으면 정직성이 아니라 남 탓이 된다.

### 🧪 T1 진행 — 모델 위원회 (UMA + MACE-MP-0 + SevenNet-0)

- 도구 `tools/ionic/mlip_committee.py` (sample → predict×3 → analyze). **새 MD 불필요**, 기존 궤적 후처리.
- 문턱은 임의 상수를 만들지 않고 **표본 분포에서 유도**: 선별 = 중앙값×2 · 중단 = p95.
  (kim2026의 γ_select/γ_break **논리 구조만** 차용)
- 기준선 대상: `/data/work/b2o3md/modelc_full/d0.00_cfg0/T600/traj.xyz` (2000 프레임 × 62원자).
- **CPU 실행** — comp2 disorder MD가 GPU를 쓰고 있어 충돌 회피. 단일점만 하므로 CPU로 충분.
- ⛔ **이 지표는 절대 정확도를 말하지 않는다.** 세 모델이 전부 PBE 계열이라 V3의 functional 각인
  문제를 풀지 못한다 — **일치해도 절대 σ 인용 금지는 그대로**. 재는 것은 "이 배열이 훈련 분포에서
  이상한가"뿐이고, 그 목적에는 같은 functional 계열인 것이 오히려 무해하다.
- **✅ 기준선 교정 완료 (2026-07-28)** — modelc 600 K, 62원자, 200/2000 프레임, 3엔진 CPU.
  프레임 단위 중앙 **0.3175** · p95 **0.3669** eV/Å → `db/properties/mlip_committee_baseline.json`
- ⚠ **위원회 독립성이 보이는 것보다 낮다**: 쌍별 mace|sevennet **0.202** < sevennet|uma 0.215 <
  mace|uma **0.317**. **가장 잘 맞는 쌍이 훈련셋을 공유한다(MPtrj)** — UMA만 OMat24.
  불일치를 지배하는 것은 아키텍처가 아니라 **훈련 데이터**이고, 실질 **3명이 아니라 2진영**이다.
- **원소별(정규화 후)**: P 0.333 > S 0.277 > Li 0.235 > Cl 0.182.
  원시 절대값으로는 P/Cl = 5.9배였는데 정규화하면 **1.8배**로 압축된다 — 원시 순위의 대부분이
  **힘 크기**였다. 단 **순서는 살아남는다**: 모델들이 **PS₄ 골격에서 가장 덜 합의**한다.
- 🔑 **T3에 직결**: T3의 1순위 관측량이 **잔존 PS₄ 층수**인데 위원회가 가장 덜 합의하는 게 바로 그
  PS₄다. → T3 착수 게이트를 **벌크가 아니라 Li 계면 구조에서** 다시 잡아야 하고, QE 단일점 대조를
  병행해야 한다(대리지표는 DFT를 대체하지 않는다).
- 다음: ① 정적 구조(comp1 V0) 기준선 — 평형에서의 하한 ② **Li 계면 슬랩 탐지 모드** (T3 게이트)
  ③ 훈련셋이 다른 4번째 엔진 검토 ④ QE 단일점 대조 ~20 스냅샷

### ⏳ 발표 구술 txt 대기
두 발표 모두 구술 내용 txt를 받기로 함. 받으면 각 digest `§99` 를 채우고
미해결 질문(lee Q1–Q6 / **moon Q1b·Q2·Q3·Q4·Q5·Q6·Q7·Q8** — Q1은 2026-08-03 재판독으로 종결,
Q7·Q8은 재판독으로 신설)을 닫는다. **이 항목은 닫지 말 것.**

### 🆕 BEARS arXiv 확보 대기 (2026-08-03 덱 재판독 발)
`talks/moon2026_cau_...` digest Q3·Q7·Q8이 전부 BEARS/스킬 논문으로만 닫힌다:
**arXiv:2601.04748**(3계층 스킬 로딩 토큰 절감 실측치) + BEARS 본문(Validator의 **"8종 구조 검증 지표"**
목록, "40+ skills"와 에이전트별 [3]/[5]/[6]/[8] 표기의 관계). ⚠ **우리 DEM 산출 구조에도 고정 검증
세트가 없다** — 그들 8종 목록이 나오면 우리 세트 설계의 출발점으로 쓴다.

## ✅ 닫힌 항목
- (여기로 이동)
