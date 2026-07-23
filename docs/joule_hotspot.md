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

→ v1 = **발열이 어디 몰리나(위치)**까지 정직 산출.  절대 K·R(N) 가속은 Eₐ digitize 후 v2.

## 이중계산 가드 (v1)
Joule q 는 σ_e solve와 **같은 σ 테이블** 사용(독립 σ 없음) → σ 이중계산 없음.  기존 `solve_thermal`
k_eff(외부-flux 전도, source 無)와 **직교** — 절대 합산 금지(v2에서 conduction k_eff vs self-heating
ΔT 별도 필드).
