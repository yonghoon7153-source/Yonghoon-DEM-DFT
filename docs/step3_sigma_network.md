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
  | SDCP | **150** | 🔶 **사용자 지정 INTERIM 앵커 (2026-07-10)** — S-PEDOT급 소재 전도도 자릿수.
      (pellet ×5.1은 composite-수준이라 별개; doped/neutral 분리는 후속) |

## 신뢰 모델 (정직)
- **v1 신뢰 단위 = 상대 비교** (σ표+vox 동일 세팅의 런끼리). 절대 σ_e는 sub-voxel constriction
  (Holm 목 면적)이 voxel 면적으로 양자화되는 한계 + σ hook 때문에 DEM Stage-E와의 교차 캘리브레이션
  전까지 절대값 주장 금지.
- AM-AM 접촉 목은 **econn과 같은 규칙(gap ≤ 0.1µm)의 1-voxel 다리**로 보존 — DEM 접촉망 충실.
  목 면적 ~vox²로 과대 (비교런 공통 → 상대차 보존).

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
- `mpm_metrics.step3`: sigma_e_eff_S_cm, sigma_table, dissipation_share(상별 전류경로 분담),
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

## 한계 (v1, 문서화)
- sub-voxel constriction 미모델 (목 면적 voxel-양자화) / 측면 Neumann (주기 아님) /
  σ_ion 망 미구현 (v2: SE+SDCP, SDCP σ_ion>0 — 사용자 원칙) / 절대값 캘리브레이션 미완.
- Li 농도(slide-21/22)는 시간-의존 전기화학 — STEP3 전류의 ∫I·dt proxy가 다음 단계 후보.

## 실행 (kgy)
step2가 자동 포함 (`run_mpm.sh` 재실행이면 충분; payload만 다시 = 케이스 폴더에서 run_mpm.sh의
mpm_webapp_payload 명령 재실행). 끄기: `--no-step3`. 해상도: `--step3-vox 0.4`(기본).
