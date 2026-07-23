# #29 — Cycle Joule I²R 발열 hot-spot

**질문:** "사이클 돌 때 어디서 발열이 몰리는지."

**답 (v1, 구현):** 전자망 전류가 구속(소수 percolating neck)에 몰리고 σ 낮은 곳에서 발열밀도
q ∝ ∣J∣²/σ 가 최대 → **발열 hot-spot 위치 맵**.

## v1 — 발열 생성분포 (구현, 기본 OFF)

- **STEP3** `step3_sigma.joule_hotspot(res, sid, σ, vox, sel_sids)`: 전자 solve의 (φ,cond) 재사용
  → per-voxel ∣J∣(`_voxel_jmag`, field_point_cloud와 **공유** = 단일 소스) → q=∣J∣²/σ.  순수
  readout(재솔브 없음·σ 불변).  반환: 점군 + `hot_frac_50`(q 총합 50% 담는 상위복셀 분율, 작을수록
  집중) + `conc_ratio`(max/mean).  검증: 1-voxel neck 구조 → hot_frac_50 0.32·conc 2.0×.
- **payload** `--joule-heat`(기본 OFF): `step3['joule']`{hot_frac_50, conc_ratio, n_pts} +
  `joule_field`[x,y,z,q₀₋₁] (p99.8-norm, 전자/이온/열 필드와 동일 문법).  전자망 percolation 필요
  (SE-only 베드는 σ_e=0 → 발열 없음 → joule_field=None, 정상).
- **뷰어** `jt_field` 모드(🔥 Joule 발열): je_field 경로 재사용(발열=전자망 AM+carbon), 색=발열 hot-spot,
  범례 hot_frac_50·conc.  select 옵션 + kt_field 옆.

## v2 — 절대 ΔT(K) + STEP5 연동 (⚠ 앵커 대기, 미구현)

정직하게 **아직 못 채움**:
- **절대 온도상승 ΔT(K):** Poisson 열확산 ∇·(k∇ΔT)=−q + 등온 plate BC + 실전류 스케일 필요.
  (solve_sigma_z 에 `source=` kwarg 추가 → Laplace/Poisson 공유 assembler로 구현 가능 — 인프라 준비됨.)
- **STEP5 R(N) 연동:** hotter → faster 열화 = Arrhenius 가속.  **LPSCl 분해 활성화에너지 Eₐ 앵커가
  litdb에 없음**(리서치 확인) → 값 날조 금지(F1 규약).  또 이중계산 가드: cho2024/yun2023 끝점은
  실측 셀의 자기발열을 이미 포함 → Joule→R 연동은 **끝점 보존 공간 재분배기**(hot 복셀 빠르게·cold
  느리게, Σ 앵커 보존)여야지 Arrhenius 곱을 끝점 위에 얹으면 안 됨.

→ v1 = **발열이 어디 몰리나(위치)**까지 정직 산출.

## 문헌 조사 결과 (2026-07-23, Eₐ 앵커 탐색)

**TARGET 1 (분해-율 Eₐ): 문헌 침묵 — 존재하지 않음.**  LPSCl 분해/CEI-성장 *율*의 Arrhenius Eₐ는
출판된 값이 없음(우리 digitize gap 아니라 **문헌 자체의 gap**).  존재하는 T-분해 Eₐ는 전부 **틀린 양**:
- 이온 전도 Eₐ 0.16–0.36 eV (Boulineau/Yu — σ_ion, 분해 아님).
- kim2025 계면 R_ct(T) → 전달 Eₐ ~0.40 eV (R_ct는 T↑에 *감소* = 부호 반대, 분해율 아님).
분해는 **열역학**(안정창·DFT ΔG)이나 **압력-의존 √t Wagner 율상수**로만 특성화 — T/Arrhenius 아님.
→ **절대 Arrhenius 곱은 앵커 불가·날조 금지(F1).**  불가피 시 라벨된-ASSUMED 스윕 Eₐ∈0.4–0.9 eV만.

**TARGET 2 (자기발열 크기): 물리적으로 유의 (~5–30 K, ~1 K 아님).**  Ayyaswamy AEM 2026
(10.1002/aenm.70978): SSB 자기발열·미세구조 열구배 설계-유의, 작은 SE→큰 구배, 2C서 +40 Wh/kg
"온도상승만으로".  낮은 복합 k(0.08–1 W/m·K)가 국소 hot-spot 증폭.  → 발열-열화 커플링은 물리적 정당.

## v2 — 끝점-보존 공간 재분배기 (구현됨, `scripts/joule_redistribute.py`)

문헌조사가 Eₐ 부재를 확인 → **절대 Arrhenius 곱 대신 재분배**로 정직하게 구현:

  **ΔR_local = ΔR_total · q^p / Σ(q^p)**   (Σ ΔR_local = ΔR_total = 앵커 끝점 보존)

- ΔR_total = STEP5 스칼라 총 열화 증분(이미 cho2024/yun2023 실측 끝점 앵커, **실셀 자기발열 포함**).
- q = #29 v1 `joule_hotspot` 발열밀도.  p = 집중 지수(**p=1 자연=열화∝국소발열** / p>1 = ASSUMED 스윕).
- ★Arrhenius 곱을 끝점 위에 얹지 **않음** → 이중계산 회피(끝점이 자기발열 이미 포함).  = 절대 K·Eₐ 없이
  "발열 몰린 곳이 더 빨리 열화(공간)"를 정직 표현.  **공간 패턴 = Joule hot-spot 맵(joule_field)과 동일**,
  절대 스케일만 ΔR_total 로 보존-정규화.
- 검증(selftest 7/7): Σ 보존(p=1·2 불변)·p>1 집중↑(3.8→6.7×)·q≤0 안전·균일 q 균등분배.
- 대안(절대 K 필요 시): ASSUMED 스윕 Eₐ∈0.4–0.9 eV 게이트(kim2025 전달 하한→liquid-LIB SEI 유사).

★남은 절대 ΔT(K) 정밀값: Ayyaswamy AEM2026 PDF digitize(egress 제한서 재시도) — 재분배기는 절대 K 불요.
- 대안: ASSUMED 스윕 Eₐ∈0.4–0.9 eV 게이트 뒤 (kim2025 전달 하한 → liquid-LIB SEI 유사).
- PDF 타깃(egress 제한서 재시도): Chem.Eng.J. 2024 S1385894724063940(고온저장 열화)·Ayyaswamy ΔT digit.

## 이중계산 가드 (v1)
Joule q 는 σ_e solve와 **같은 σ 테이블** 사용(독립 σ 없음) → σ 이중계산 없음.  기존 `solve_thermal`
k_eff(외부-flux 전도, source 無)와 **직교** — 절대 합산 금지(v2에서 conduction k_eff vs self-heating
ΔT 별도 필드).
