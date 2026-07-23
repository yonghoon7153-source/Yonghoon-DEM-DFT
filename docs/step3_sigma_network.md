# STEP3 v1 — 전자전도 voxel 저항망 (σ_e_eff + 입자별 전류밀도)

**목적**: econn(binary 연결성)이 표현 못 하는 "얼마나 잘 통하나"를 숫자로 — SBE vs DBE처럼 **둘 다
연결된** 전극의 σ_e 차이 + slide-20 문법의 입자별 전류밀도 색칠.
**코드**: `scripts/step3_sigma.py` (해석해 selftest 내장) + `scripts/mpm_webapp_payload.py --step3`
(기본 ON, kgy step2에서 풀해상도 실행) + viewer "전류밀도 — STEP3" 모드.

## 물리 설계
- **이산화**: 전도상 voxel 유한체적, ∇·(σ∇φ)=0, 면 전도도 = 조화평균(상 경계 자동), 아래판 φ=1 /
  윗판 φ=0, 측면 Neumann (RVE는 주기지만 v1은 비교런 간 동일 조건이라 상대차에 1차 무영향 — 문서화).
  Bazzoun 2026의 RNM/FEM과 같은 계열 (voxel = mini-FEM).
- **전도상**: AM(σ_S/σ_P) + VGCF/SuperP/SDCP. **SE·PTFE = 전자 절연 (0)**. SDCP는 사용자 확정 원칙대로
  전자 percolation에 참여 (이온 σ는 v2).
- **σ 표 (S/cm, 전부 플래그로 override; metrics.step3.sigma_table로 기록되어 런 간 비교 가능)**
  | 상 | σ | 상태 |
  |---|---|---|
  | AM_S | 0.010 | ✅ A1-locked (Trevisanello 10 mS/cm) |
  | AM_P | 0.005 | ✅ A1-locked (5 mS/cm) |
  | VGCF | 100 | ⚠ §F1 자릿수 hook (graphitic fibre 문헌 10²-10³) |
  | SuperP | 10 | ⚠ §F1 자릿수 hook (CB compact 1-50) |
  | SDCP | **250** | **사용자 지정 앵커 (2026-07-16; interim 150 대체)** — 진성호계 S-PEDOT 자릿수.
      (⚠pellet ×5.1은 composite-수준 — phase σ 아님, +52% σ_e는 network solve EMERGENT; doped/neutral 분리는 후속) |

## 신뢰 모델 (정직)
- **v1 신뢰 단위 = 상대 비교** (σ표+vox 동일 세팅의 런끼리). 절대 σ_e는 sub-voxel constriction
  (Holm 목 면적)이 voxel 면적으로 양자화되는 한계 + σ hook 때문에 DEM Stage-E와의 교차 캘리브레이션
  전까지 절대값 주장 금지.
- AM-AM 접촉 목은 **econn과 같은 규칙(gap ≤ 0.1µm)의 1-voxel 다리**로 보존 — DEM 접촉망 충실.
  목 면적 ~vox²로 과대 (비교런 공통 → 상대차 보존).

## 물리 리뷰 반영 (2026-07-10, 2-agent 적대 리뷰 — 코드/물리 각 1명)
- **F1 판-운(MAJOR) 해결**: 윗판이 "최상 AM 한 층"에만 결합 → sub-voxel 베드 이동에 σ가 **×7.7**
  요동 (리뷰어 프로브) = 스캐폴드 다른 런끼리 비교가 판-운에 노출.  ⇒ 판을 **연속 평면(바닥=collector
  z=0, 상단=두께) + 컬럼당 표면 voxel 1개 접촉 + 거리-가중 g = σ·vox²/max(dist, vox/2), 밴드
  vox+0.1µm**로 재정식화.  베드-고정 phase 프로브에서 σ 완전 안정; 잔여 ±~2×는 **crown-희소 프레임
  (부유 베드)**에만 남는 quantization 항 — production은 프레스가 상단을 눌러 접촉이 풍부(수백 컬럼)
  → 안정.  trust 문구를 "pressed-to-plate 베드"로 좁힘.
- **F2 수렴 침묵**: info≠0 또는 resid>1e-6 → ⚠ 출력 + metrics trust에 `⚠UNCONVERGED` 플래그;
  maxiter 30k.  **F3 다리 σ-id 역전**: 수정(혼합 접촉 = AM_P 하위-σ).  **F4 share 오분배**: 혼합 면의
  발열을 반반이 아니라 **반대편 σ 가중**(1e4 대비 면에서 탄소 몫 50%→~0%)으로; 라벨 "전류 경로"→
  **"손실(발열) 분담"** (전류 아님 — 탄소는 전류는 많이 나르고 발열은 거의 없음).
- 기타: je = |J_z| proxy 라벨 정정 / vox 민감도 실측 **0.4→0.3µm에서 σ ×0.46** (vox는 절대 튜닝 노브
  아님 — 비교런 간 고정 필수) / 1.6M dof 실측 ~8분 (문서의 "수 분" 정정) / PTFE가 접촉 틈에 있어도
  AM-AM 다리는 스탬프됨(econn과 같은 한계 — binder-rich계 과대 카운트 1줄 명시) /
  `--integration` 모드 커밋 (real14+합성 VGCF 재현: AM-only 1.474e-4 → +VGCF 2.849e-4, ×1.93 단조).

## 검증 (2026-07-10, 전부 통과)
1. **해석해 5종**: 균질블록=σ 정확 / 직렬 라미네이트=조화평균 / 병렬=산술평균 / 절단층=0 /
   단면 1/36 기둥=σ/36 — 조립·BC·단위 고정.
2. **통합 테스트 (real14 스캐폴드 + 합성 VGCF 300개, 0.4µm)**:
   AM-only σ=1.49e-4 → +VGCF **2.89e-4 S/cm (×1.94)** — 도체 추가 단조성 ✓, CG resid 1e-8,
   700k dof 26-88s (production 2-4M dof ≈ 수 분).
3. **통합 테스트가 잡아서 고친 버그 3건** (이력 보존):
   - 부유 전도 섬 → 특이행렬 NaN ⇒ 판-연결 성분만 풀기 (물리: 부유 섬 전류 0)
   - 접선 접촉의 voxel-center 미도달 ⇒ 판을 grid 끝이 아닌 **점유 최하층/AM 최상층**에 결합
     (구가 판에 접해도 그 층 voxel 중심엔 못 닿음 → 모든 런 σ=0이 되는 버그였음)
   - 돌출 fibre 끝이 윗판을 끌어올려 깔때기 ⇒ **윗판 = AM 존재 최상층** (+ z_top=두께로 클립);
     탄소 한 가닥은 판을 만들 수 없음 (이 버그는 "탄소 추가가 σ를 ×24 낮추는" 비물리로 발현)
4. DEM 불필요 — 전부 MPM 구조(se_dump/phase/scaffold) 위 계산.

## 산출물
- `mpm_metrics.step3`: sigma_e_eff_S_cm, sigma_table, dissipation_share(상별 손실(발열) 분담 — 전류 아님),
  vox_um, n_dof, k_plates, n_floating_dropped, cg_resid, trust 문자열
- `payload particles[].je`: 입자별 평균 |J_z| → viewer "전류밀도 — STEP3 σ_e (slide-20)" 모드
  (p5-p95 정규화, 빨강=hot path)
- 로그 한 줄: σ_e_eff + 상별 분담

## 이온망 (v2-lite, 2026-07-10 — 같은 그리드, σ표만 교체)
같은 voxel 그리드에 SE(sid 6, 최저 우선순위 스탬프)를 추가하고 **이온 σ표로 한 번 더 풀기**:
SE = 3.0 mS/cm (Cronau σ_grain ✅) + **SDCP = 1.0 mS/cm (⚠F1 hook — 사용자 원칙 '이온 절연 아님',
pellet ×0.80 방향; Li⁺ DFT 패키지가 앵커 예정)**; AM/VGCF/SuperP/PTFE = 이온 차단.
→ `metrics.step3.sigma_ion_eff_S_cm` + `ion_dissipation_share` (SE vs SDCP 경로 분담).
GeoDict-계 논문의 Fig-2(d)/(f) 축과 방법론 동급 (voxel FV) — 단 우리는 **상 분해** 유지.
스모크: 전자 2.19e-4 / 이온 3.69e-4 S/cm, 이온 분담 SE 97.6% + SDCP 2.4% (기계 검증).

## 집전체 축 (C-SUS/primer, 2026-07-10)
- **R_int 직렬 (후처리, 재-솔브 불필요)**: σ_apparent = L/(L/σ_bulk + R_int).  앵커 = manuscript
  Fig6e **사이클 후** R_int: bare-Al SBE 110 / DBE 46 / C-SUS primer 30 Ω·cm² (S14: primer 1.3e4
  S/cm, 200nm).  벌크 R ~0.002 Ω·cm² ≪ R_int → **계면이 병목, primer가 그걸 ×3.7 연다**.
- **문헌 검증 (2026-07-10 WebSearch)**: ① 액체 LIB의 carbon-coated Al 계면 ASR은 0.014–0.03
  Ω·cm² (코팅 후) — 우리 값보다 3-4자릿수 작음 = **액체계 잣대는 부적용**.  ② 고체계 계면은
  수십~수백 Ω·cm²가 정상 스케일 (garnet/Li 950→75 표면처리; Bazzoun 우리-동일계 R_ele 59.7→48.5
  Ω·cm²) → **manuscript 30-110은 sulfide-ASSB EIS 계면저항 자릿수에 정합** ✓.  ③ dry-공정 ASSB
  carbon-coated Al: R_int **5-10× 감소** 보고 — manuscript의 110→30 (×3.7)과 방향·자릿수 일치 ✓.
  ⚠ 명시: Fig6e는 **사이클 후**(열화 포함) 값 — pristine 계면은 더 낮음; "primer = 열화 억제"
  성분이 큼 (조건 라벨 유지).
- **기하 접촉 모드 (v2)**: bottom 접촉 밴드 wetted(vox+0.1 — 200nm film reach) vs **bare(0.5vox+0.1
  — crown 접점만)** 두 번 풀어 σ_wetted/σ_bare + 접점 수 + **입자별 je(wetted)·jb(bare)** 를 payload에
  기록 — bare의 "몇 개 crown으로 전류가 몰리는" 국소 그림이 viewer 'je_bare' 모드에서 3D로 보임
  (primer-논문 Fig4d red-box 문법).  접촉 집합에 ±half-voxel 양자화 blur (방향 강건, 문서화).
- webapp: 첨가제 패널 **집전체 드롭다운** (C-SUS 30 기본/DBE 46/bare 110/이상 0) → zip에
  --collector-rint 베이킹 → metrics.step3.collector.selected 강조 (모든 프리셋은 항상 병기).

## 한계 (v1, 문서화)
- sub-voxel constriction 미모델 (목 면적 voxel-양자화) / 측면 Neumann (주기 아님) /
  σ_ion 망 미구현 (v2: SE+SDCP, SDCP σ_ion>0 — 사용자 원칙) / 절대값 캘리브레이션 미완.
- Li 농도(slide-21/22)는 시간-의존 전기화학 — STEP3 전류의 ∫I·dt proxy가 다음 단계 후보.

## 실행 (kgy)
step2가 자동 포함 (`run_mpm.sh` 재실행이면 충분; payload만 다시 = 케이스 폴더에서 run_mpm.sh의
mpm_webapp_payload 명령 재실행). 끄기: `--no-step3`. 해상도: `--step3-vox 0.4`(기본).
