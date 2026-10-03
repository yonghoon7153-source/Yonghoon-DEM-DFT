<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · τ 묶음 형식 기준 = tjaden2018_… · taufactor_… · landesfeind2016_… · 같은 날 앞 묶음 (siroma2015_… · nguyen2020_… 등).
     이 논문은 수치 방법 논문이다 (주파수 영역 유한차분 확산 임피던스 · TauFactor 통합).  그래서 §4 = 지배식 · 경계 · 정규화의 사슬 (원문 번호 그대로),
     §8 맨 앞 = "망 임피던스 (τ_e) 구현 참고" (이 카드를 연 이유 · 판단 메모 v2 §7 최소안 · §8-2).
     쪽 표기 = 학술지 인쇄 쪽 (PDF n 쪽 = 인쇄 680 + n 쪽; 범위 681–689).  식 · 그림 번호 = 원문 번호.  본문 표 없음 (그림 6 안에 인쇄된 작은 표 하나).
     SI 없음 — 본문이 SI 를 인용하지도 않는다.  수식 · 그림은 PDF 를 고배율로 렌더해 읽었고, 그림 수치는 PDF 벡터 경로 좌표로 판독했다 (방법 = "원문 대조 기록").
     값 표지: stated = 본문 · 캡션 / stated(그림) = 그림 안에 인쇄된 숫자 / 판독 = 그림 좌표에서 읽은 값 (≈ · 추세 전용) /
     우리 유도 = 카드 작성자가 원문 식에서 끌어낸 관계 (원문에 그 문장은 없다) / 우리 재계산 = 원문 값 · 식으로 다시 계산한 값. -->
# 다공 미세구조 확산 임피던스의 주파수 영역 유한차분 직접 모사 — 개방계 저주파 절편 = τ/ε · 같은 τ·ε 라도 스펙트럼은 다르다 · 다공도 구배의 순수 확산 이중 피크 (DRT 오독 경고) · TauFactor 확산 임피던스 모드의 원전 — Cooper (Electrochim. Acta 2017)

> slug `cooper2017_simulated_impedance_diffusion_porous_media` · DOI `10.1016/j.electacta.2017.07.152` · type `computational (frequency-domain finite-difference diffusion impedance on segmented voxel geometries — TauFactor · open/closed boundaries · pseudo-3D vs 3D · DRT) — method` · PDF `25. Simulated impedance of diffusion in porous media.pdf` · digested `2026-10-03` · status ✅
>
> inbox τ 문헌 묶음 3 #25 · 9 쪽 전부 읽음 (본문 + 부록 A + 참고문헌 60 편) · SI 없음 · 그림 크롭은 메인 몫 (§5 에 크롭 권고 — 정본 `figures/cooper2017_simulated_impedance_diffusion_porous_media/` 에 자동 추출 6 장이 있다, 캡션 대조는 메인).
> ★ **이 카드의 결론 한 줄** — 이 논문은 TauFactor 의 정상상태 Laplace 솔버를 **주파수 영역 확산 방정식** ∇²Ĉ − (iω/D)Ĉ = 0 (식 1) 으로 바꿔
> 복셀 미세구조의 확산 임피던스를 직접 푼다.  τ 와의 연결은 한 문장이다 — *"the low frequency intercept of open systems is equal to τ/ε"* (p.683,
> 정규화 Z̃ = Z·A·D/L, A = CV 전체 단면) ⇒ 이 τ 는 TauFactor τ = ε·D/D_eff = 우리 **tau2** 이고, Z̃(0) = 1/f 다 (우리 유도).
> ⚠ 그러나 **τ_e 의 물리는 이 논문 3D 솔버에 없다**: 저장 (축전) 항이 기공 **부피**에 있고 (식 1 · p.685), 이중층 · 전하전달 · 이동은 빠져 있다 (p.683).
> 표면 축전 (de Levie · Keiser · Eloot = TLM · eSCM 계열) 은 부록 A 의 pseudo-3D 비교에만 나오고, 두 물리는 **단면이 일정할 때만** 같다 (1/r̃ 항, p.687).
> ⇒ 우리 τ_e 구현에는 **수치 틀 · 경계 어휘 (open/closed) · 정규화 · 진단**의 참고이지 지배식의 원전이 아니다 (지배식 원전 = Nguyen 2020 eSCM).
> 형제 카드: `taufactor_tortuosity_factor_tomography_tool` (이 솔버가 들어간 툴 · 1.424.0 모드 목록) · `nguyen2020_electrode_tortuosity_factor` (이 틀에 표면 축전 경계를 얹은 τ_e — ref 42 로 이 논문 인용)
> · `siroma2015_transmission_line_model_porous_electrode_impedance` (TLM 해석해 · R/3) · `landesfeind2016_tortuosity_eis_electrodes_separators` · `tjaden2018_tortuosity_review_calculation_approaches` (명명 정본).

---

## 0. 결론 먼저 (닫는 것 + 판정)

| # | 결론 | 근거 (인쇄 쪽 · 식) |
|---|---|---|
| ① | **τ 정의 = TauFactor τ = 우리 tau2.**  개방계 정규화 임피던스 Z̃ = Z·A·D/L (A = 흐름 방향에 수직인 CV 경계 **전체** 면적) 의 저주파 절편이 τ/ε 다.  정상상태 flux 를 D_eff (전체 단면 기준) 로 쓰면 Z̃(0) = D/D_eff ⇒ **τ = ε·D/D_eff** (우리 유도) — TauFactor [24] 정의와 같은 꼴이고 Z̃(0) = τ/ε = **1/f** 다.  ε 는 **고립 기공 부피까지 포함한** 수송상 분율이다 (그림 2 기하 1) | 식 3 (p.682) · p.683 첫 문장 · p.684 ("geometry 1 … same tortuosity factor … due to the region of isolated pore volume") |
| ② | **물리 = 부피 저장 Fick 확산.**  저장 항 −(iω/D)Ĉ 가 Ω 의 모든 점에 있다 = *"the capacitance scales with the pore volume"*.  대류 · 전기 이동 · 이중층 · 농축용액 효과는 **없다** (PNP 가 필요하다고 스스로 적음).  표면 축전 (TLM) 은 부록 A.3–A.4 의 pseudo-3D 비교뿐이고, 일정 단면이면 두 계가 같은 Warburg 를 낸다 — 단면이 변하면 1/r̃ 만큼 다르다 | 식 1 (p.682) · p.683 (§2.1 끝) · p.685 · 식 (A.2) ↔ (A.4) (p.687) |
| ③ | **같은 τ · ε → 다른 스펙트럼.**  ε 0.5 · τ 1.57 로 맞춘 2D 개방 기하 7 개가 양 끝 (고주파 · 저주파) 에서만 만나고 중고주파 모양 · 특성주파수가 다르다.  입구에서 멀어질수록 **좁아지면 위상 > 45°**, **넓어지면 < 45°**.  어디서 바뀌는지는 침투 깊이 l_δ = √(D/ω) (식 4) 가 주파수로 옮긴다 | p.683 (§2.2) · 그림 2 (p.684) · p.685–686 · 식 4 (p.685) |
| ④ | **구배 구조 = 순수 확산만으로 두 봉우리.**  선형 다공도 구배 구 충전 (입구 쪽이 좁고 안쪽으로 넓어지는 증가형, 개방) 이 Nyquist 두 호 · DRT 2차 봉우리를 낸다 — *"both from a purely diffusive process"* — 실험 DRT 에서 **추가 전기화학 과정으로 오독**될 수 있다.  같은 충전을 뒤집으면 개방 절편은 그대로 (≈ 4.1–4.2) 인데 **폐쇄계 저주파 실수부는 ≈ 0.74 ↔ 2.27 (×3.1)** 로 갈린다 (판독) = 차단형 저항의 **방향 의존** · 관통형의 방향 맹 | 그림 5 (p.685) · p.686 |
| ⑤ | **pseudo-3D (1D 균질화) 는 3D 보다 저항을 과소 · 주파수 의존을 고주파로 민다.**  그림 6 표: Z̃'(ω = 0) pseudo-3D/3D = 14.0/17.3 (A_T/A_B 0.01) · 3.0/3.0 (1) · 1.7/2.2 (3) → −19 % · 0 · −23 % (우리 재계산).  이유 = 등농도면이 흐름 방향에 수직이라는 가정 (가로 확산 무한대) | 그림 6 (p.687, stated(그림)) · p.685 · p.687–688 |
| ⑥ | **원문 내부 불일치 둘**: p.685 *"Z̃'' goes to −1/√(2ω) and the phase approaches 90°"* — −1/√(2ω) 는 **고주파 45°** 점근 (ωc = 1) 이고, 차단 끝의 저주파 극한은 Z̃' → 1/3 · Z̃'' → −ωc/ω (우리 재계산).  p.686 단위 *"D = 10⁻⁹ m s⁻²"* (→ m² s⁻¹) · ω 를 "Hz" 로 표기 (값은 D/l_δ² = s⁻¹) | §10 오식 표 · "원문 대조 기록" |
| ⑦ | **우리 τ_e 에 필요한 최소 요구** (Cooper 밖): ⓐ sink 를 **AM–SE 계면 면적**에 (SE 부피 아님) ⓑ 집전체 쪽 **이온 차단** (= Cooper 의 closed) ⓒ 전자 쪽 (AM 등전위 또는 전자망) ⓓ 추출 규칙 (R_ion ← TLM · 저주파 R/3).  ω → 0 만 쓰면 **실수 솔브 한 번**으로 충분 (메모 v2 §7) — Cooper 의 주파수 기계는 스펙트럼 · 진단을 원할 때만.  **결정 13 · 11 · 5 권고 변경 없음** (§8) | §8-1 · §8-2 · §8-3 · §8-4 |

## 1. 한 줄 요약
등가회로의 Warburg 요소는 1D 확산을 가정해 3D 미세구조를 기공률 · tortuosity factor 두 숫자로 줄인다.  이 논문은 TauFactor 의 유한차분 · 과완화 솔버를
**주파수 영역**으로 옮겨 (복소 농도 Ĉ, 식 1) 분할된 2D/3D 복셀 구조 위에서 확산 임피던스 스펙트럼을 직접 계산하고, 개방계 (저장소 끝 = FLW 기준) ·
폐쇄계 (차단 끝 = FSW 기준) 로 Keiser 1976 기공 · 같은 τ·ε 의 개방 기하 7 개 · 프랙탈 · 다공도 구배 구 충전 · Celgard 분리막 단층 영상 두 개를 풀었다.
결론: 스펙트럼은 Warburg 에서 크게 벗어날 수 있고 (특히 구배 · 프랙탈), **순수 확산만으로 여러 봉우리**가 나와 별개 전기화학 과정으로 오독될 수 있다.
도구는 TauFactor 의 공개 MATLAB 앱으로 배포됐다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재계 | 연구유형 |
|---|---|---|---|---|
| **Samuel J. Cooper**(a, 교신) · Antonio Bertei(b) · Donal P. Finegan(c,d) · Nigel P. Brandon(b) | **Electrochimica Acta 251 (2017) 681–689** | **10.1016/j.electacta.2017.07.152** | 일반 확산종 (고유 D = 1, 무차원).  예시 구조: 2D 그림 기하 (MS Paint) · 프랙탈 · Monte-Carlo 구 충전 (SOFC 맥락) · **Celgard 2325 / 2500 분리막** 단층 영상 [43] | **계산 (방법)** — 주파수 영역 유한차분 (TauFactor) · 실험 없음 (실측 EIS 대조는 후속으로 미룸, p.686) |

- 소속 (p.681): (a) Dyson School of Design Engineering, Imperial College London · (b) Electrochemical Science and Engineering, Earth Science and Engineering, Imperial College London · (c) Electrochemical Innovation Lab, Department of Chemical Engineering, University College London · (d) National Renewable Energy Laboratory, Golden, CO.
- 이력: 접수 2017-04-28 · 수정본 2017-07-24 · 수리 2017-07-25 · 온라인 2017-07-27 (p.681).  **CC BY 4.0** 오픈액세스 (p.681).
- 키워드: Impedance · Microstructure · Diffusion · Tomography · EIS · Warburg · TauFactor (p.681).
- 지원: EU Horizon 2020 Marie-Skłodowska-Curie grant No 654915 · EPSRC EP/M014045/1 · EP/K002252/1 (p.687).  사의: G. Reade · V. Yufit · A. Kucernak · A. Atkinson (EIS 논의) · P. Shearing (단층 영상 데이터) (p.687).
- 코드: *"This simulation tool is provided as an open-source MatLab application and is freely available online as part of the TauFactor platform"* (초록 p.681) · *"The simulation tool has been integrated into the TauFactor platform"* (p.687).  **판 번호 · URL · 저장소 ID 는 이 논문에 없다** [미확인] — §4-9.
- 참고문헌 60 편 (p.688–689).

## 3. 핵심 수치 ★ (stated / stated(그림) / 판독 구분)

### 3-1. 정의 · 정규화 (stated)
| 양 | 값 · 식 | 쪽 |
|---|---|---|
| 지배식 | ∇²Ĉ − (iω/D)Ĉ = 0 in Ω · Ĉ = 0 on T · ∇Ĉ·n = 0 on I · Ĉ = 1 on B (식 1) | p.682 |
| 고유 확산도 | **D = 1** (모든 경우) | p.682 |
| 자극 진폭 | 1 (모든 경우) · Z = 진폭 ÷ 입구 (B) 복소 확산 flux | p.682 |
| 특성주파수 | **ωc = D/L²** (식 2) · 개방계 L = CV 두께 (자극면 수직) · 폐쇄계 L = 자극면에서 가장 긴 기공 끝까지의 **최대 침투 거리** | p.682 |
| 주파수 창 | **[ωc·2⁻⁴, ωc·2¹¹]** — 15 옥타브 ≈ 4.5 decade (우리 산술) | p.682 |
| 정규화 | **Z̃ = Z·A·D/L** (식 3) · 개방계 A = 흐름 방향 수직 CV 경계 **전체** 면적 · 폐쇄계 A = **"mean accessible area"** (각 깊이에서 확산이 닿을 수 있는 면적의 산술 평균) | p.682–683 |
| 개방계 저주파 절편 | **= τ/ε** (*"a useful characteristic feature for comparison between structures"*) | p.683 |
| 침투 깊이 | l_δ = √(D/ω) (식 4) | p.685 |
| 초기화 | 개방계 = 정상상태 시간영역 해 (ω = 0 절편으로도 사용) · 폐쇄계 = Ω 전체 Ĉ = 1 + 0i | p.683 |
| 수렴 | 자극면 B 에서 잰 복소 임피던스의 안정 | p.682 |

### 3-2. 구조 세트와 격자 (stated)
| 세트 | 경계 | 격자 · 크기 | 쪽 |
|---|---|---|---|
| Keiser 1976 의 폐쇄 기공 5 개 (Keiser 그림 4 를 MS Paint 로 근사 재현) — 2D (prismatic) · 3D (축대칭 회전) | 폐쇄 (FSW 기준) | 거울 대칭으로 2D **절반 128 × 128**, 3D **4 분의 1 128 × 128 × 128** voxel | p.683 |
| 개방 2D 기하 7 개 (기하 1 + 시행착오로 만든 새 6 개) — 흰 상 수직 방향 **ε = 0.5 · τ = 1.57** | 개방 (FLW 기준) | 격자 크기 원문 없음 [미확인] | p.683–684 |
| Sierpinski carpet 1–6 차 | 개방 | 가장 작은 정사각 = **5 × 5 voxel** (격자 무관 해를 위해) → 6 차 = **3645 × 3645** (= 5·3⁶, 우리 확인) · 절반 모사 | p.683 |
| Pythagoras tree 0–5 차 | 폐쇄 | **250 × 250 pixel** · 절반 모사 | p.683 |
| 3D 의사 무작위 구 충전 (Monte-Carlo [44]) — 자극면 수직으로 **선형 다공도 구배**, 뒤집어 증가/감소 × 위 끝 개방/폐쇄 = 4 런 | 둘 다 | 크기 · 입경 · 다공도 범위 원문 없음 [미확인] | p.683–684 |
| Celgard 2325 · Celgard 2500 단층 영상 [43] (두께 방향 다공도 변화가 뚜렷하게 제조) | 개방 | voxel 크기 · 부피 원문 없음 [미확인] · 샘플당 스펙트럼 2 개 (결론의 *"depending on the direction analysed"* (p.687) 로 보아 두 방향 — 색 ↔ 방향 대응 미표기) | p.683–684 |

### 3-3. 그림 6 의 인쇄 표 — pseudo-3D vs 3D (stated(그림), p.687) + 우리 재계산
| A_T/A_B (위/아래 단면비) | Z̃'(ω=0) pseudo-3D | Z̃'(ω=0) 3D | pseudo-3D/3D (우리 재계산) |
|---|---|---|---|
| 0.01 (입구에서 멀어지며 좁아짐) | 14.0 | 17.3 | 0.809 (**−19 %**) |
| 1 (일정 단면) | 3.0 | 3.0 | 1.000 |
| 3 (넓어짐) | 1.7 | 2.2 | 0.773 (**−23 %**) |
- ⚠ 그림 6 의 Z̃ 정규화 (어느 A · 어느 L) 는 본문 · 부록에 적혀 있지 않다 [미확인] — A_T/A_B = 1 에서 3.0 이 나오는 이유 (종횡비 등) 를 원문으로 확인할 수 없다.  **비 (pseudo-3D/3D) 만** 쓴다.

### 3-4. 그림 판독 (PDF 벡터 좌표 · ≈ · 추세 전용)
| 그림 | 양 | 판독값 | 비고 |
|---|---|---|---|
| 2 | 7 기하 공통 저주파 절편 (τ/ε 표지 *) | **≈ 3.10** | 명시값 τ/ε = 1.57/0.5 = 3.14 (우리 재계산) 과 −1.3 % — 설계가 "trial and error" (p.683) 라 이 정도 어긋남은 판정 불가 |
| 3a | Sierpinski 1–6 차 τ/ε | ≈ 1.29 · 1.63 · 2.03 · 2.55 · 3.20 · 4.00 | 차수당 ≈ ×1.25 (판독 비 1.25–1.27).  carpet 의 ε 미보고 → τ 역산 안 함 |
| 3a | ω = ωc 원의 Z̃'/Z̃'(0) | 0.84 · 0.81 · 0.78 · 0.74 · 0.70 · 0.65 (1→6 차) | FLW 해석해 0.886 (우리 재계산) — 차수가 오를수록 특성주파수가 FLW 에서 더 멀어진다 |
| 3b | Pythagoras 0–5 차 폐쇄계 저주파 수직선 Z̃' | ≈ 0.33 · 0.39 · 0.37 · 0.44 · 0.47 · 0.54 | 0 차 (곧은 기공) 0.330 = FSW 해석해 1/3 (우리 재계산) · 1 ↔ 2 차 비단조 |
| 4 | τ/ε — Celgard 2500 (위 축) · 2325 (아래 축) | **≈ 2.65 · ≈ 6.38** (비 ≈ 2.40) | 본문에 τ · ε 값 없음 → τ 역산 안 함 |
| 4 | ω = ωc 점 (빨간 원) 의 Z̃'/Z̃'(0) | 2500 ≈ 0.79–0.82 · 2325 ≈ 0.60–0.61 | FLW 회색 원 0.885 = 해석해 0.8855 와 일치 (판독법 검증) — 2325 의 이동이 크다 = *"more convoluted flow paths"* (p.686) |
| 5 | 개방계 저주파 끝 (같은 충전 뒤집기) | 증가형 ≈ 4.14 · 감소형 ≈ 4.10 (마지막 계산점, −Z̃'' 0.10 / 0.39) → 절편 ≈ 4.1–4.2 | 같은 τ/ε 여야 한다 — 일치 |
| 5 | 폐쇄계 저주파 수직선 Z̃' | 증가형 (입구 좁음) **≈ 2.27** · 감소형 (입구 넓음) **≈ 0.74** → **×3.1** | 같은 충전 · 같은 정규화 (평균 접근 면적 · 최대 침투 깊이 — 완전 연결 가정) 라 비는 정규화 무관 |
| 5 | DRT 봉우리 log₁₀(ω⁻¹) (γ) | 증가형 ≈ 3.7 (4.5) + ≈ 2.5 (1.2) · 감소형 ≈ 4.1 (16) + ≈ 2.9 (0.5) | x 축 단위 미표기 [미확인] · 증가형 두 봉우리 간격 ≈ 1.2 decade |
| 6 | 위상 −φ 최댓값 | A_T/A_B 0.01 ≈ 66–67° · 1 ≈ 46° (약간 넘친 뒤 45°) · 3 = 45° 아래 어깨 (≈ 37–42°) | 고주파에서 셋 다 45° 로 수렴 |

### 3-5. 침투 깊이 ↔ 주파수 (p.686 stated + 우리 재계산)
| l_δ (기공 입구에서의 거리) | 액체 (D = 10⁻⁹) | 기체 (D = 10⁻⁵) |
|---|---|---|
| 1 µm | ω ≈ 10³ | ω ≈ 10⁷ |
| 10 µm | ω ≈ 10 | ω ≈ 10⁵ |
| 1000 µm | ω ≈ 10⁻³ | ω ≈ 10 |
- 우리 재계산 ω = D/l_δ² 가 표 값을 그대로 낸다 (단위 s⁻¹ = rad s⁻¹).  원문 인쇄 단위는 D "m s⁻²" · ω "Hz" — 둘 다 오식 후보 (§10).  "Hz" 를 f 로 읽으면 실제 주파수는 2π 배 작다.

### 3-6. 1D 해석해 극한 (우리 재계산 · 이 논문 정규화 · ωc = 1)
| 계 | Z̃(ω) | ω → 0 | ω → ∞ | ω = ωc |
|---|---|---|---|---|
| 개방 곧은 기공 (FLW) | tanh(s)/s, s = √(iω/ωc) | 1 (CV 를 꽉 채운 기공) · 일반 구조는 τ/ε | (1 − i)/√(2ω/ωc) — 45° | 0.886 − 0.287i |
| 폐쇄 곧은 기공 (FSW) | coth(s)/s | **1/3 − i·ωc/ω** (−φ → 90°) | 같은 45° 꼴 | 0.331 − 1.022i |
- FLW 호의 최대 −Z̃'' = 0.417 (ω/ωc ≈ 2.54, Z̃' 0.58).  그림 1 주축 · 그림 3b 의 곧은 기공 수직선 ≈ 0.33 (판독) 이 FSW 1/3 과 맞는다.

- σ_ionic · E_SE · porosity@P · coverage · Z (배위수) · Heckel: **n/a** (압밀 · 재료 물성 논문 아님).

## 4. ★ 방법 — 지배식 · 경계 · 정규화의 사슬 (원문 번호 그대로)

### 4-1. 지배식 (식 1, p.682)
- 영역: Q = (0, L_x) × (0, L_y) × (0, L_z) ⊂ ℝ³ (직육면체) · **Ω ⊂ Q = 확산이 일어나는 다공 매질 영역** · ∂Ω = T ∪ I ∪ B ·
  ∂Ω|_{z=L_z} = B (Bottom) · ∂Ω|_{z=0} = T (Top) · ∂Ω|_{0<z<L_z} = I (Interfacial) — 집합 정의상 I 는 기공벽과 측면 CV 경계를 함께 담는다 (우리 읽기 · 측면 거울 대칭 사용과 정합, p.683).
- **∇²Ĉ − (iω/D)Ĉ = 0 in Ω** · **Ĉ = 0 on T** · **∇Ĉ·n = 0 on I** · **Ĉ = 1 on B** (n = Ω 의 바깥 단위법선 · Ĉ = 복소 농도 · i = 허수 단위 · D = 수송상 고유 확산도 = 1 · ω = 자극 주파수).
- 폐쇄계: T 의 조건이 I 와 같아진다 (no-flux) (p.682).
- 시간영역 정현 자극도 원리상 가능하지만 계산비가 금지적이라 주파수 영역으로 옮겼다 — 자극은 다시 Dirichlet 조건 (p.682).  (식 1 은 Fick 2법칙 ∂C/∂t = D∇²C 에 C = Ĉe^{iωt} 를 넣은 꼴 — 우리 해석.)
- ★ **저장 항의 자리** — −(iω/D)Ĉ 는 Ω 의 **모든 점**에 있다 = 질량 축전이 **부피**에 비례 (p.685).  벽 I 는 no-flux 라 표면 축전 · 반응 · 계면 저항이 들어갈 자리가 **없다** (§8-7).

### 4-2. 개방계 · 폐쇄계 (p.682–685)
| | **개방계 (open)** | **폐쇄계 (closed)** |
|---|---|---|
| 끝 T 의 조건 | Ĉ = 0 (이상 저장소) | ∇Ĉ·n = 0 (차단) |
| 해석 기준 (곧은 기공) | Finite Length Warburg (FLW) | Finite Space Warburg (FSW) (p.683) |
| 저주파 | 유한 실수값 · 위상 0 (p.685) — 절편 = τ/ε (p.683) | 수직 점근 (축전) · 위상 → 90° (p.685, Song & Bazant [41] 인용) |
| 정규화 A · L | CV 전체 단면 · CV 두께 | 평균 접근 면적 · 최대 침투 거리 (p.682) |
| 초기값 | 정상상태 해 | Ĉ = 1 + 0i |
| 그림 | 2 · 3a · 4 · 5 (실선) | 1 · 3b · 5 (점선) |
- ⚠ **두 계의 단면 장부가 다르다** — 개방계는 CV 전체 면적, 폐쇄계는 기공 (접근 가능) 면적.  개방 Z̃ 와 폐쇄 Z̃ 의 절대값을 한 축에서 비교하지 않는다 (우리 해석).
- 풀이 영역: 입구 B 와 이어진 수송상.  폐쇄 기공 (그림 1 · 3b) 은 정의상 전부 dead-end 다.  그림 2 기하 1 의 고립 부피에 대해 원문은 *"simply has the effect of linearly scaling the spectra, so it will still be the same shape as the FLW solution"* (p.684) — 모양은 FLW 그대로이고 배율만 바뀐다.
  물리적으로는 고립 부피 자체는 전류를 나르지 않으므로 Z (따라서 Z̃) 는 관통 채널의 단면만으로 정해지고, 고립 부피는 ε (그래서 τ) 에만 들어간다 — 같은 ε 에서 고립 부피를 늘리면 채널이 좁아져 배율이 커지는 것이다 (우리 해석).

### 4-3. 정규화 사슬 (식 2–3) — τ/ε 가 나오는 이유 (우리 유도)
1. Z = (자극 진폭 1) ÷ (입구 복소 flux) (p.682).
2. ω → 0 개방계: flux = D_eff·A·ΔC/L (D_eff 를 **CV 전체 단면 A** 로 정의) → Z(0) = L/(D_eff·A).
3. Z̃(0) = Z(0)·A·D/L = **D/D_eff**.  원문: Z̃(0) = τ/ε (p.683).  ⇒ **D_eff = ε·D/τ ⇔ τ = ε·D/D_eff** — TauFactor [24] 의 τ 정의 (`taufactor_…` 카드 Eq 1 · `TauFactor.m:3495–3496`) 와 같은 꼴.
4. ⇒ Z̃_open(0) = τ/ε = D/D_eff = **1/f** (우리 f = σ_eff/σ₀ 의 역수 = MacMullin 수 — 원문은 이 이름을 쓰지 않는다).
5. 그림 2 · 3 · 4 의 원 (○) = ω = D/L²_CV 인 점 (*"Circles have been used to highlight the characteristic frequency of each spectrum"*, p.684).  FLW 의 그 점은 Z̃'/Z̃'(0) = 0.886 (우리 재계산) — 시뮬 원이 이보다 왼쪽이면 "전 두께가 탐색되는 주파수가 ωc 보다 낮다" (p.686).

### 4-4. 수치 (p.682–683)
- TauFactor [24] 의 유한차분 · 최적화 (**과완화 · 체커보드 · 벡터화**) 를 그대로 주파수 영역에 씀 — *"massively accelerating convergence"* (p.682).  주파수마다 따로 푼다 (스펙트럼의 각 점, p.682).
- 원문에 없는 것 [미확인]: 복소 항의 이산식 · 이완 계수 · 스펙트럼당 주파수 점 수 · 계산 시간 · 격자 수렴 자료 (Sierpinski 의 "5 × 5 voxel" 규칙만 문장으로 있다).
- 참고 (툴 카드 기록): TauFactor 1.424.0 의 정상상태 모드 1 은 6-이웃 · 반 voxel 경계 · red-black SOR (w = 2 − π/(1.5a)) 이고, 모드 5 (Nguyen eSCM 복소 문제) 는 이완 0.85 고정이다.  **모드 4 (이 논문) 의 내부는 이 카드에서 코드로 확인하지 않았다.**

### 4-5. 구조 생성 (p.683)
- Keiser 기공: MS Paint 2D 틀 → 단순 회전 알고리즘으로 축대칭 voxel 부피.  곧은 (prismatic) 폐쇄 기공은 FSW, 곧은 개방 기공은 FLW 를 되찾아야 한다 (자기 검증 기준).
- 개방 7 기하: 시행착오로 같은 ε · τ — *"based on current electrode equivalent circuit models, they would each be treated identically in terms of transport"* (p.684).  기하 1 = 곧은 경로 + 고립 기공 (τ 를 맞추려고 고립 부피를 붙임) · 나머지 여섯의 같은 τ 는 *"a variety of combinations of constriction and path length convolution"* 에서 온다 (p.684).
- 프랙탈: rough · multi-lengthscale 계의 문헌 모델 [31–37] (p.683).
- 구 충전: 배터리 · 연료전지 전극의 흔한 모델계 [38] · 1D 균질화 [39, 40, 30] 를 3D 로 넓혀 면내 비균질까지 · 실제 배터리 확산 임피던스는 보통 **입자 내부 반경 방향 고상 확산** [41, 42] 이지 기공망이 아니다 — 다만 연료극 지지형 SOFC 는 기상의 긴 경로 손실이 있다 (p.683).
- 분리막: 저자들의 선행 연구 [43] 의 단층 영상 (Celgard 2325 · 2500).

### 4-6. 부록 A — pseudo-3D 와 축전 벽 기공의 수학 대응 (p.687–688)
| 식 | 원문 | 뜻 |
|---|---|---|
| (A.1) | iωĈπr²dx = −d/dx(−D dĈ/dx πr²)dx (0 < x < L) · Ĉ = 1 (x = 0) · FLW: Ĉ = 0 / FSW: −D dĈ/dx = 0 (x = L) | 축대칭 기공 (국소 반지름 r(x)) · 등농도면 ⊥ x 가정의 확산 |
| (A.2) | d²Ĉ/dx̃² + (2/r̃)(dr̃/dx̃)(dĈ/dx̃) − i(ω/ωc)Ĉ = 0 · x̃ = x/L · r̃ = r/r₀ (r₀ = x = 0 반지름) · **ωc = D/L²** | (A.1) 무차원 |
| (A.3) | iωcV̂·2πr dx = −d/dx(−σ dV̂/dx πr²)dx · 같은 경계 (V̂ 로) | **전해질 (전도도 σ) 로 찬 기공 + 비표면 축전 c 의 전극 벽** = Keiser · Eloot 의 물리 · V̂ = 복소 전위 |
| (A.4) | d²V̂/dx̃² + (2/r̃)(dr̃/dx̃)(dV̂/dx̃) − i(ω/ωc)(V̂/**r̃**) = 0 · **ωc = σr₀/(2cL²)** | (A.3) 무차원 — (A.2) 와 **1/r̃ 하나만** 다르다 |
- 원문 해석 (p.687): V̂ = Ĉ · σ = D · 2c/r₀ = 1 로 두면 같은 꼴.  1/r̃ 는 *"in this system the capacitance scales with the pore surface while in the diffusion problem the mass-capacitance scales with the pore volume"* 에서 온다.  **r̃ = 1 (일정 반지름) 이면 (A.2) ≡ (A.4)** → 물리가 달라도 같은 Warburg (차원 배율만 다름).  본문 p.685: 곧은 원통 기공이면 *"identical Warburg impedance spectra [3, 46]"*, 단면이 변하면 *"minor differences"*.
- pseudo-3D 의 한계 (p.685 · p.687–688): 등농도면의 곡률을 무시 = 가로 방향 확산 무한대 가정.  A_T/A_B 가 1 에서 멀면 (i) Z′(ω = 0) **과소** (ii) 주파수 의존 **과대** (φ(ω) 가 고주파 쪽으로 약간 이동) — 3D 에서는 가로 flux 가 유한해 저항 · 시간척도가 더 크다.  Keiser 결과는 이 논문의 2D 와 3D **사이**에 놓인다 (p.685).

### 4-7. 가정 목록 (원문 근거)
| 가정 | 근거 |
|---|---|
| 무한희석 Fick 확산만 — 대류 · 전기 이동 · 전하 분리 (이중층) · 농축용액 효과 없음 (그건 PNP 모델 [29] 필요) | p.683 |
| *"these are the exact assumptions used in the standard Warburg model [30]"* — 이 단순함 덕에 단층 영상 voxel 을 그대로 노드로 빠르게 푼다 | p.683 |
| 단일 수송상 · 균일 D (= 1) · 이진 voxel | p.682 |
| 선형 소신호 (주파수 영역 변환) · 정현 Dirichlet 자극 진폭 1 | p.682 |
| 벽 · 측면 no-flux (측면 거울 대칭으로 절반 · 4 분의 1 만 모사) | 식 1 · p.683 |
| 격자 무관: 가장 작은 특징 = 5 × 5 voxel (Sierpinski) — 수렴 자료 없음 | p.683 |

### 4-8. 입자 처리 ★
- **입자 물리 없음.**  구조는 기하 voxel 상이다 — MS Paint 그림 · 회전체 · 프랙탈 · Monte-Carlo 구 충전 (강체 기하; 겹침 · 접촉 규칙 원문 없음 [미확인]) · 실제 고분자 분리막 단층 영상.
- 접촉법칙 · 압밀 · 소성 · 입자 번호 · 계면 저항 **모두 없다**.  수송상 = 흰 상 (그림 2 캡션 · 그림 5 단면도 흰 바탕 검은 입자) 이 연속 복셀로 이어진다.  ⇒ 우리 MPM STEP3 복셀 σ 와 같은 범주 (접촉망의 CONTACT_FREE 가지 쪽 — CL-81 구조 결론과 같은 자리).

### 4-9. 공개 코드 서지 (특히 확인)
| 무엇 | 내용 | 출처 |
|---|---|---|
| 논문 안의 문장 | open-source MatLab application · TauFactor platform 의 일부로 공개 (초록) · TauFactor 에 통합 (결론) | p.681 · p.687 |
| 플랫폼 서지 (원문 목록 그대로) | [24] S.J. Cooper, A. Bertei, P.R. Shearing, J.A. Kilner, N.P. Brandon, TauFactor: An open-source application for calculating tortuosity factors from tomographic data, SoftwareX 5 (2016) 203–210. | p.688 — 정본 카드 `taufactor_tortuosity_factor_tomography_tool` |
| 판 · URL · ID | **이 논문에 없음** [미확인] | — |
| 다른 카드의 기록 | Nguyen 2020 의 Code availability: MathWorks File Exchange 57956-taufactor · SourceForge (nguyen 카드 §2) · TauFactor **1.424.0** GUI 모드 `4. Diffusion Impedance Spectrum w/ Mirror` ↔ 이 논문 (툴 카드 모드 목록 — 라벨 대응은 툴 카드의 판단, 모드 4 내부 코드는 미기록) | 형제 카드 |
| Python 판 (`tldr-group/taufactor`) | 임피던스 기능 유무 [미확인] — J 절은 classic 정상상태 솔버만 기록 | `comparison_vs_ours_DEM.md` §J |

### 4-10. 기법 미니 용어집
| 용어 | 뜻 |
|---|---|
| FLW (Finite Length Warburg) | 끝이 이상 저장소 (Ĉ = 0) 인 1D 확산 — Z̃ = tanh(s)/s · 저주파 실수 절편 (투과형) |
| FSW (Finite Space Warburg) | 끝이 차단 (no-flux) 인 1D 확산 — Z̃ = coth(s)/s · 저주파 축전 수직선 (반사형) |
| open / closed system | 이 논문의 경계 이름: 위 끝 T 가 저장소 (FLW 계열) / 차단 (FSW 계열).  ⚠ 회로 소자 이름 "Wo" ('open' 끝단 = 개방 회로) 는 coth 꼴 = 이 논문의 **closed** 다 — 낱말 "open" 이 반대 뜻 (§8-6) |
| penetration depth l_δ | √(D/ω) — 교류 신호가 입구에서 탐색하는 깊이.  l_δ ≈ L 이면 끝 경계가 임피던스에 걸린다 (p.685) |
| characteristic frequency ωc | D/L² (개방: L = CV 두께 · 폐쇄: 최대 침투 거리) |
| mean accessible area | 폐쇄계 정규화 면적 — 각 깊이에서 확산이 닿는 면적의 산술 평균 (p.682) |
| pseudo-3D | 축대칭 단면 변화를 1D 식에 넣은 Keiser · Eloot · de Levie 계 (등농도면 ⊥ x) |
| prismatic 2D / 축대칭 3D | 같은 2D 틀을 기둥으로 / 회전체로 만든 두 판 (그림 1) |
| DRT | distribution of relaxation times — 이 논문은 DRTtools [45] (Wan · Saccoccio · Chen · Ciucci 2015) 사용 |
| electrochemical porosimetry | 임피던스로 기공 구조를 역추정 (Song 등 [59, 60]) — 이 논문은 "가능하나 제한적" (p.686) |

## 5. Figure set ★ (크롭 권고 = ★)
| Fig (쪽) | 내용 (무엇을 보여주나) | 우리가 참고할 점 | 크롭 |
|---|---|---|---|
| 1 (p.683) | Keiser 폐쇄 기공 5 개의 2D (왼) · 3D (오) 스펙트럼.  inset = 식 3 정규화, 주축 = 곧은 기공 (1) 과 같은 값으로 모이게 한 **두 번째 정규화** (Ẑ — 식 정의 없음).  입구에서 좁아지는 쐐기 (5) 는 45° 위, 입구 뒤에서 넓어지는 (2)–(4) 는 45° 아래 고원 (판독 · 형상 이름은 그림 모식에서 읽음) · 3D 가 2D 보다 형상 효과가 크다 (3D (4) 는 수직선 직전에 −Z̃'' 가 다시 내려가는 갈고리) | 폐쇄계 (차단형) 에서 형상이 중고주파를 바꾼다 · 곧은 기공 수직선 ≈ 0.33 = FSW 1/3 | ★ |
| 2 (p.684) | **ε 0.5 · τ 1.57 동일한 개방 기하 7 개** — 양 끝에서만 만나고 (τ/ε 표지 ≈ 3.10) 중고주파 모양 · ω = D/L²_CV 원 위치가 다르다.  (6) 좁아짐 = 45° 위 · (7) 넓어짐 = 45° 아래 고원 | ★★ "같은 tau2 · 같은 φ ≠ 같은 수송 응답" 의 가장 깨끗한 그림 — 결정 11 (복셀 ↔ 망 대조를 DC tau2 하나로 끝내지 말 것) | ★★ |
| 3 (p.684) | (a) Sierpinski 개방 1–6 차 — 절편 ≈ 1.29 → 4.00 · inset 고주파 (1 차는 45° 아래, 6 차는 위로 가파름) (b) Pythagoras 폐쇄 0–5 차 — 차수↑ 일수록 중고주파가 45° 아래에 오래 머묾 (깊이당 면적 증가) | 계층 · 분포 기공의 눌린 호 [31, 48, 36, 37] 와 정성 일치 | ★ |
| 4 (p.685) | Celgard 2500 · 2325 단층 영상 스펙트럼 (샘플당 2 개) + 같은 절편의 FLW · τ/ε * · ωc 원.  두 판의 축은 절편이 맞게 배율 | 실재 균질 재료에서도 작은 왜곡 · 특성주파수 이동 (2325 가 큼).  "Warburg 이탈인데 다공도 변화를 기대할 이유가 없으면 → RVE 부족" (p.686) | ★ |
| 5 (p.685) | **선형 다공도 구배 구 충전** — 증가형 (청) · 감소형 (적) × 개방 (실선) · 폐쇄 (점선) + 개방 두 경우의 DRT inset + 3D 렌더 | ★★ 증가형 개방 = 두 호 · DRT 2차 봉우리 (순수 확산) · 뒤집기: 개방 절편 같음 ↔ 폐쇄 수직선 ×3.1 (방향 의존) — 결정 13 · graded-z (A7) | ★★ |
| 6 (p.687) | A_T/A_B = 0.01 · 1 · 3 의 위상 vs log ω — pseudo-3D (실선) vs 3D (점선) + Z̃'(ω=0) 인쇄 표 + 농도장 색 그림 | ★ 1D 균질화 (TLM 계열) 의 저항 과소 −19 / −23 % — R_ion 환산 · TLM 적합의 오차원 | ★★ |

- 크롭 우선순위: **2 · 5 · 6** (결정 11 · 13 근거) → 4 → 1 → 3.  그림 6 은 인쇄 표가 그림 안에 있으니 표가 잘리지 않게.

## 6. Post-processing ★
- **무엇**: Nyquist (−Z̃'' vs Z̃') 정규화 플롯 · 폐쇄 기공 비교용 두 번째 정규화 (곧은 기공 값으로 모음, 그림 1) · τ/ε 와 ω = D/L²_CV 표지 · 같은 절편의 FLW 해석해 겹쳐 그리기 (그림 4) · 개방계 DRT (DRTtools [45], 그림 5 inset) · 위상 vs log ω (그림 6).
- **도구**: TauFactor (MATLAB, 주파수 영역 FD) · MS Paint (2D 틀) · 회전 알고리즘 (축대칭 3D) · Monte-Carlo 충전 생성기 [44] · DRTtools [45].
- **읽는 법 (원문 규칙)**: ① 중고주파 위상 > 45° = 입구에서 멀어지며 좁아지는 단면 (차단벽을 닮음) · < 45° = 넓어지는 단면 (저장소를 닮음) (p.686) ② 형상 변화의 거리 ↔ 주파수 = 식 4 ③ 이질성은 **입구 가까이 · 고주파 (ω > ωc)** 에서 잘 보이고 ω < ωc 에서는 정보 질이 급락 (p.686) ④ 같은 확산 임피던스 지문을 다른 구조 족이 낼 수 있다 → **역추정은 유일하지 않다** — 단면 좁아짐/넓어짐 · 다공도 감소/증가 같은 지표는 구분된다 (p.686) ⑤ 미세구조를 알면 확산 임피던스를 계산해 실측에서 **빼고** 다른 과정에 집중할 수 있다 (p.686).

### 6-bis. 절별 결과 흐름 (논증 순서)
1. **서론 (p.681–682)** — 등가회로의 Warburg 는 1D 라 3D 구조를 기공률 · tortuosity factor 몇 숫자로 줄인다.  *"structures with very different morphologies can have identical tortuosity factors and porosities"* — 주파수 분석이 정상상태 분석에 더해 성능 관련 특징을 줄 수 있다.  Keiser 1976 [6] (de Levie [7] 의 TLM 위 pseudo-3D) 이후 40 년간 많은 논문 (Lasia [10–12] · Malko [13] · Noack [14] · González-Buch [15] · Cericola & Spahr [16] · Radvanyi [17] · Wu [18] · Hitz & Lasia [11] · Zhang [19]) 이 왜곡 설명에 Keiser 를 인용했지만 *"unable to find an instance where the numerical results were directly used in the analysis of an EIS spectrum"* (p.682).  CT [20–23] 로 3D 구조를 얻게 됐다.
2. **방법 (p.682–683)** — 식 1–3 · 초기화 · 물리 범위 (Warburg 와 같은 가정).
3. **폐쇄 기공 (그림 1)** — Keiser 와 같은 일반 추세 (물리가 달라도) · 3D 가 2D 보다 강함 · Keiser 는 그 사이 (p.684–685).
4. **개방 기하 7 개 (그림 2)** — 같은 τ · ε 인데 중고주파 모양 · 특성주파수 이동이 다르다.  좁아짐 > 45° · 넓어짐 < 45° · 넓어지는 위치가 입구에 가까울수록 (사례 7) 높은 주파수에서 이탈 (사례 4 · 5 는 더 낮은 주파수) (p.685–686).
5. **프랙탈 (그림 3)** — 개방 carpet: 차수↑ → 저항↑ (절편) + 고주파가 45° 로 더 가파르게 (입구 근처 좁아짐) · 폐쇄 tree: 차수↑ → 깊이당 면적↑ → 45° 아래 오래 (p.686).
6. **실제 분리막 (그림 4)** — 균질한 편인 실재 재료에서도 왜곡이 보인다 (Candy [49] 의 균질 구 충전 결과와 정합).  가장 큰 차이는 FLW 대비 특성주파수 위치 — 후보 설명 = 관측 tortuosity factor 안에서 **경로 연장 vs 경로 협착**의 상대 기여 (가설, p.686).  Warburg 이탈인데 다공도 변화를 기대할 이유가 없으면 → 부피가 작아 대표성이 없다 (TauFactor 의 RVE 도구, p.686).
7. **구배 충전 (그림 5)** — 강한 왜곡 · 증가형 개방 = 두 봉우리 (두 시간상수) · 전기화학 없음 · DRT 2차 봉우리 → 추가 회로 요소 오용 위험 (Bertei [58]) (p.686).
8. **역이용 · 한계 (p.686)** — 확산이 주 현상이면 임피던스로 미세구조를 추정 (electrochemical porosimetry [59, 60] 유사) — 다만 비유일 · 깊을수록 신호가 뒤섞임.  실측 EIS 대조는 후속.
9. **부록 (p.687–688)** — pseudo-3D 식 · 축전 벽 기공과 1/r̃ 차 · 그림 6.

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 이 파일은 값 0 개 자리표시 — 비교는 판단 메모 v2 의 정의 · 코드 줄 기준; 코드 줄은 메모 v2 · 형제 카드 기록과 이 카드의 읽기 전용 grep)
| 항목 | 이 논문 | 우리 | 같음/다름 · 이유 |
|---|---|---|---|
| 역할 (frame[5]) | **수송 절반의 방법 논문** (확산 임피던스) · 기계 · 입자 없음 | DEM 접촉망 σ (DC 관통) · MPM STEP3 복셀 σ (DC 관통) | 경쟁자가 아니라 **임피던스 쪽 도구 · 진단의 참고**.  기계 · 형상 절반은 없다 |
| frame[4] | 실험 없음 (수치 ↔ 해석해 · Keiser) | 각 모델을 실험에 따로 보정 | 이 논문의 "일치" 는 수치 자기검증 — 실험 검증 아님 |
| 주파수 | 전 영역 (4.5 decade 창) | **DC 하나** — `network_conductivity.py` · `step3_sigma.py` · `voxel_conductivity.py` 에 복소 · 주파수 경로 0 건 (읽기 전용 grep) | 대응하는 것은 **개방계 ω → 0 극한 하나** = 우리 1/f |
| 이산화 | 복셀 FD · 단일 수송상 D = 1 (이진) | 접촉망 (SE 노드 + Holm 간선) · 복셀 FV (다상 σ, 조화평균) | Cooper ≈ STEP3 범주 (연속체 · 비기하 계면 항 0).  접촉망과는 다른 이산화 |
| 경계 | 개방: Dirichlet 1/0 · 측면 거울 / 폐쇄: 끝 차단 | 접촉망: 두 띠 Dirichlet (`network_conductivity.py:225–249 · 590–593`) · 측면 주기 / STEP3: 판 Dirichlet + 측면 Neumann (`step3_sigma.py:835–840`) | **개방계 DC = 우리 BC 부류** (관통) · 폐쇄 (차단) 대응은 우리에게 **없다** (τ_e 공백, 메모 v2 §7) |
| 정규화 | Z̃ = Z·A·D/L, A = CV 전체 | σ_ratio = G·T/A_box 전체 단면 (`network_conductivity.py:857`) | **같은 관례** → Z̃_open(0) ≡ 1/f 를 그대로 대조할 수 있다 |
| ε 장부 | 고립 기공 포함 전체 (그림 2 기하 1) | φ_SE = 모든 SE 구 부피 합 (비관통 포함 · 겹침 이중계상) | 같은 "전체 상" 규약 · 겹침만 다르다 (J 절과 같은 판정) |
| 저장 (축전) 항 | 부피 (iω/D)Ĉ | 없음 (DC) | τ_e 에는 **표면** (AM–SE 접촉) 이 필요 — 이 논문 3D 솔버의 물리가 아니다 (§8-1) |
| 계면 저항 | 없음 (벽 no-flux · 입자 번호 없음) | 접촉망 FULL = Holm 직렬 · CF = 0 · STEP3 계면 저항 항 (CL-81 ①, `--step3-rint A\|B=VAL` Ω·cm², 기본 OFF) | Cooper = CF 쪽.  r_int 자리는 이 틀에 없다 (§8-7) |
| 입자 | 기하 voxel (그림 · 회전체 · MC 구 충전 · 분리막 영상) | DEM 강체구 + 연화 E_eff (접촉 소성 대리) · MPM 소성 형상 | 입자 물리 0 — 강체구 ↔ 소성 · halide ↔ LPSCl 주의가 **직접 걸리지 않는다** |
| 액체/기체 vs 고체 | 확산종 (액체 10⁻⁹ · 기체 10⁻⁵ 예시) | ASSB SE = 단일 이온 전도체 (이온 DC 에 부피 저장 없음 — 우리 해석) | 이 논문의 확산 임피던스는 **SE 이온 임피던스의 물리가 아니다**.  AM 입자 내부 고상 확산에는 같은 꼴이 맞다 (p.683 · [41, 42]) |
| 2D/3D | 둘 다 · 2D (prismatic) 와 3D (축대칭) 가 다르다 (그림 1) | 3D | 2D 사례는 개념 증명 — 절대 크기 전이 금지 |
| RVE · 해상도 | 최소 특징 5 × 5 voxel · Warburg 이탈 = RVE 부족 진단 (p.686) | d_h/dx ≥ 3.5 · RVE ≥ 7.5× 최대 입자 | 같은 철학 · 임피던스 기반 RVE 진단은 우리에게 없다 |
| 고주파 해상도 | 창 상한 ωc·2¹¹ 에서 l_δ = L/√2048 ≈ L/45 (우리 산술) — L = 128 voxel 이면 ≈ 2.8 voxel | — | 고주파 끝이 해상도 한계 근처일 수 있다 (원문 수렴 자료 없음) · 접촉망은 입자 하나 = 노드 하나라 **l_δ < 입자 크기** 영역을 원리적으로 못 그린다 (우리 해석) |

- ⚠ 걸리는 차이는 셋이다: ① 부피 축전 ↔ τ_e 의 표면 축전 ② 액체 · 기체 확산종 ↔ 고체 단일 이온 전도 ③ 연속 voxel (협착 0) ↔ Holm 접촉망.  이 카드의 어떤 수치도 우리 tau2 의 "일치/불일치" 근거로 쓰지 않는다 — 정의 · 경계 · 진단만 쓴다.

## § τ 정의 대조 — 우리 규약 매핑
> 우리 규약 (CLAUDE.md τ 명명 규약 · 1저자 비준 10-03): f = σ_eff/σ₀ · **tau2** = φσ₀/σ_eff = φ/f (= **tortuosity factor**) · tau = √tau2 ·
> τ_geo = 최단 경로/두께 · τ_e = electrode tortuosity factor (우리 없음).  'tortuosity factor' 는 tau2 에만 쓴다.

**(a) 이 논문의 양 → 우리 다섯 양**

| 이 논문 (쪽) | 정의 · 정규화 (부피 · 단면 · σ₀) | 우리 양 (키) | 판정 |
|---|---|---|---|
| **τ "tortuosity factor"** (p.681 이름 · Epstein [4]: *"a measure of the resistance to diffusive transport caused by convolutions in the flow paths"* · p.683 τ/ε 절편) | 개방계 Z̃(0) = τ/ε · Z̃ = Z·A·D/L · A = CV **전체** 단면 · ε = 수송상 **전체** 분율 (고립 포함) · D = 고유 입력값 → **τ = ε·D/D_eff** (우리 유도) | **tau2** (`tau2_ion_<mode>`) | **같은 양 (정의식)** — TauFactor τ (p.682 "TauFactor … quantifying diffusive tortuosity factors … between a pair of parallel Dirichlet boundaries") · 원문은 τ² · κ 기호를 쓰지 않는다 |
| Z̃_open(ω → 0) = τ/ε (p.683) | D/D_eff · 고립 부피는 전류를 안 나르므로 Z̃ 는 관통 채널만으로 정해진다 (우리 해석 — 원문은 기하 1 을 "FLW 의 선형 배율" 로 적음, p.684) | **1/f** (`f_ion_<mode>` 의 역수) | 같은 양 · **ε 장부와 무관** (메모 v2 의 "f 는 φ 장부 무관" 과 같은 자리) |
| 폐쇄계 Z̃ (평균 접근 면적 · 최대 침투 거리 정규화, p.682) — 곧은 기공 저주파 실수부 1/3 (우리 재계산 · 그림 판독 0.33) | 차단 끝 + **부피** 축전 · τ 를 정의하지 **않는다** | — (τ_e 아님) | R/3 형 (de Levie · Nguyen Eq 5) 의 **확산 유사물**이지만 저장이 부피 → Nguyen τ_e (표면 축전) 와 **다른 양**.  단면 장부도 개방계와 다르다 |
| "path length" · "geometric" | 기하 1 = 곧은 경로인데 τ = 1.57 (p.684) · 같은 τ 가 *"combinations of constriction and path length convolution"* 에서 온다 (p.684) | `tau_geo_SE_dij` | **대응 없음** — 이 논문은 경로 길이 τ 를 쓰지 않고, 그것이 tortuosity factor 와 다르다는 예를 준다 |
| √ 값 | 없음 | `tau_ion_<mode>` | 대응 없음 |
| τ_e | 없음 (차단형 스펙트럼은 계산하지만 τ 로 바꾸지 않는다) | — | τ_e 원전은 Nguyen 2020 (이 틀에 표면 축전 경계를 얹음) |

- **σ₀ 기준**: **입력값** — 수송상 고유 확산도 D = 1 (무차원).  펠릿 · 벌크 측정이 아니고 접촉 저항 · 입계도 없다 (연속 voxel).  ⇒ 메모 v2 부록 (lit10) ② 의 세 기준 상태 중 **"치밀 고유 입력값 ≡ 1"** 부류 (Park 2019 · 2020 과 같은 쪽).  우리 tau2 는 간선 재료 σ₀ 3.0 mS/cm (펠릿값, CL-91) 위에 SE–SE Holm 을 직렬로 더한 **모델 T** 라 기준 상태가 다르다 — 우리 T 에서 σ₀ 는 약분되지만 협착이 T 안에 남는다.
- **정규화 길이 · 면적**: 개방계 L = CV 두께 · A = CV 전체 단면 ↔ 우리 σ_ratio = G·T/A_box (전체 단면) — **같은 관례**.  폐쇄계는 기공 면적 · 최대 침투 거리 — 우리 쪽 대응 없음.
- **연속체 tau2 ≥ 1**: 명시값 τ = 1.57 (> 1).  부록 (lit10) ③ "연속체는 모두 tau2 ≥ 1" 과 모순 없음 (carpet 은 ε 미보고라 τ 확인 불가).

**(b) J 절 한 줄** — Cooper 2017 τ ("tortuosity factor", Epstein) 는 개방계 정규화 임피던스 Z̃ = Z·A·D/L (A = CV 전체 단면) 의 저주파 절편 τ/ε 로 정의된다 → **τ = ε·D/D_eff = tau2** (TauFactor 와 같은 양) · Z̃(0) = τ/ε = **1/f** · ε = 고립 기공 포함 전체 분율 · σ₀ ↔ D = 수송상 고유 입력값 1 (펠릿 아님 · 협착 없음) · 폐쇄계 (차단) 임피던스에는 τ 를 정의하지 않는다 (부피 축전 → τ_e 아님).

## 8. 적용 인사이트 (내 연구에 어떻게)

### 8-1. 망 임피던스 (τ_e) 구현 참고 — 이 카드를 연 이유 (판단 메모 v2 §7 최소안 · §8-2)

**(a) 이 논문이 주는 것 (구현 재료)**
| 재료 | 내용 | 쪽 |
|---|---|---|
| 주파수 영역 틀 | 정상상태 솔버 (과완화 · 체커보드 · 벡터화) 를 그대로 복소 문제로 · 주파수마다 한 번 풂 | p.682 |
| 경계 어휘 | 개방 (끝 저장소, FLW) / 폐쇄 (끝 차단, FSW) — **폐쇄 = 우리 집전체 쪽 이온 차단**의 확산판 | 식 1 · p.682–683 |
| 정규화 | Z̃ = Z·A·D/L — 개방 DC 절편 = τ/ε (= 우리 1/f) → **DC 관문** (구현한 임피던스의 ω → 0 이 기존 f 를 재현해야 한다) | 식 3 · p.683 |
| 주파수 창 | ωc = D/L² 를 중심으로 [ωc·2⁻⁴, ωc·2¹¹] | 식 2 · p.682 |
| 초기화 · 수렴 | 개방 = 정상상태 해에서 출발 · 폐쇄 = Ĉ = 1 + 0i (저주파 극한 상태) · 수렴 = 자극면 임피던스 안정 | p.682–683 |
| 진단 | Warburg/TLM 이탈의 읽기 (좁아짐 · 넓어짐 · 침투 깊이) · RVE 부족 신호 · 다중 봉우리 오독 경고 · 1D 균질화 과소 (그림 6) | p.685–688 |

**(b) 이 논문에 없는 것 (τ_e 에 필요한데)**
- **표면 축전** (고/전해질 계면의 이중층) — 3D 솔버에는 없고 부록 (A.3)–(A.4) pseudo-3D 식에만 있다 (p.687).  이중층 · 전하전달 · 이동은 명시적으로 범위 밖 (p.683).
- **두 상 결합** (전자 레일 · AM 등전위) — 단일 수송상만.
- **τ_e 정의 · 추출** (TLM 적합 · R/3 → R_ion → τ_e) — 이 논문은 개방 DC 절편 τ/ε 말고 τ 를 뽑지 않는다.
- **계면 저항 항** — 벽 I 는 no-flux · 입자 번호 없음.
- **실측 대조** — 후속 연구로 미룸 (p.686).

**(c) 우리 STEP3 복셀 · 접촉망에 τ_e 를 붙일 때의 최소 요구**
| # | 요구 | Cooper 2017 이 주는 것 | STEP3 복셀 (지금) | DEM 접촉망 (지금) |
|---|---|---|---|---|
| 1 | 축전 sink 의 **자리 = AM–SE 계면 (표면)**, SE 부피 아님 | ✗ — 부피 (식 1).  표면은 부록 pseudo-3D 비교뿐 · 차이 = 1/r̃ (p.687) | 상 격자 (sid) 로 AM–SE 면을 가를 수 있다 — CL-81 ① 이 이미 "다른 sid 면" 분류를 쓴다 (`step3_sigma.py` `parse_rint_table` · 직렬 r, 기본 OFF) — 축전 결합은 없음 | AM–SE 접촉 목록 · 면적 있음 (hertz = c_cpl[22] 교차 원판).  physics 면적은 **LHS-25 뒤** (메모 결정 3 · 9) |
| 2 | 경계: 분리막 쪽 Dirichlet + **집전체 쪽 이온 차단** | ✓ 개방/폐쇄 (∇Ĉ·n = 0 on T) | 양 끝 Dirichlet 만 (관통) → 차단 경계 추가 필요 | 두 띠 Dirichlet 만 → 차단 경계 추가 필요 |
| 3 | 전자 쪽 (AM 등전위 또는 전자망 결합) | ✗ (단일 상) | 전자 채널은 따로 솔브 (이온과 결합 없음) | 전자망 따로 (σ_e 채널) · 결합 없음 — AM 등전위 가정은 저 CAM 에서 깨짐 (메모 §7 · Minnmann τ_el² 120 @25 vol%) |
| 4 | 풀이: ω → 0 극한 **실수 솔브 1 회** (접촉 면적 비례 균일 sink) 또는 주파수 sweep (복소) | ✓ 복소 sweep 틀 · 폐쇄 초기값 Ĉ = 1 + 0i 가 ω → 0 상태 | 실수 정상상태만 (복소 0 건) | 실수 Kirchhoff 만 (복소 0 건) |
| 5 | 정규화: A = 전체 단면 · L = 두께 · σ₀ 짝 | ✓ 식 3 (개방 = 전체 단면) | 전체 단면 (TauFactor 모드 1 짝) | 전체 단면 (`network_conductivity.py:857`) |
| 6 | 추출: Re Z(ω → 0) = R_ion/3 (균일일 때만) 또는 TLM 적합 → τ_e = ε·R_ion·A·σ₀/L | ✗ (곧은 FSW 의 1/3 이 그 확산판 — 우리 재계산) · 1D 균질화 과소 −19/−23 % 경고 (그림 6) | — | — |
| 7 | 진단: TLM/Warburg 이탈 · 다중 봉우리 · RVE · 방향 | ✓ (§6) | — | — |
| 8 | 해상도: 고주파 l_δ ≫ dx (스펙트럼을 원할 때) | 5 voxel/최소 특징 · 창 상한 l_δ ≈ L/45 (우리 산술) | d_h/dx ≥ 3.5 규칙 | 노드 = 입자 → l_δ < 입자 크기는 원리상 불가 (ω → 0 만 쓰면 무관) |

**(d) 판정** — Cooper 2017 = **수치 틀 · 경계 어휘 · 정규화 · DC 관문 · 진단**의 참고.  **τ_e 의 물리 (표면 sink) 는 주지 않는다** (지배식 원전 = Nguyen eSCM, TauFactor 모드 5–6).
메모 v2 §7 최소안 (ω → 0 · 접촉 면적 비례 균일 sink · AM 등전위 · 분리막 쪽 Dirichlet · 집전체 쪽 차단 · R_ion = 3·R_eff) 은 요구 1–6 중 **1 · 2 · 3 · 6** 만 있으면 되고 **복소 산술이 필요 없다** — Cooper 의 주파수 기계는 스펙트럼 (TLM 적합 · 다중 봉우리 · RVE 진단) 을 원할 때 들어온다.
⚠ **구현 함정 하나**: Cooper 식 1 을 그대로 망에 옮겨 **각 SE 노드에 부피 비례 축전**을 주면 확산 임피던스가 나오고 τ_e 가 아니다 — sink 가중은 **접촉 면적**이어야 한다 (부록 1/r̃).  원문의 "minor differences" (p.685) 는 **모든 벽이 축전인** 액체 기공 이야기라, AM–SE 벽만 축전인 ASSB 로 옮기지 않는다 (우리 해석).

### 8-2. 결정 13 (τ_e) — 권고 유지 · 한정어 · 진단 보강
- **권고 변경 없음** ("인계 비차단" 은 ML 기술자 문장으로만 · P2D/COMSOL 입력 열 보류 · "부호 불정").
- 보강 ① **방향 의존의 두 번째 독립 사례** — 그림 5: 같은 충전을 뒤집으면 개방 (관통) 절편은 같고 (≈ 4.1–4.2) 폐쇄 (차단) 저주파 실수부는 ≈ 0.74 ↔ 2.27 (**×3.1**, 판독).  Nguyen 그림 6 (τ_e 4.0 ↔ 11.9 = ×2.98 · τ 7.4 하나) 과 **같은 꼴**이 부피 축전 확산에서도 나온다 — 구조가 달라 숫자 일치는 우연 (비교 금지).  ⇒ "우리 T 는 방향 맹" (nguyen 카드 ④) 의 근거가 하나 더.
- 보강 ② **입구 좁음 = 큰 차단 저항** — 충전 전류 전체가 입구 병목을 지난다 (증가형 2.27 > 감소형 0.74 · 기전 설명은 우리 해석).  메모 v2 의 진단 "z 단면별 SE 컨덕턴스" 를 **분리막 쪽에서 본 좁아짐/넓어짐** 으로 읽으면 Cooper 의 분류 (위상 > 45° / < 45°, p.686) 와 차단 저항 방향이 바로 따라온다.
- 보강 ③ **"R_ion = 3·R_eff" 의 다른 오차원** — 그림 6: 1D (pseudo-3D) 는 단면비 0.01 · 3 에서 3D 대비 저항 −19 / −23 % · 위상 곡선을 고주파로 민다.  부록 (lit10) 의 한정어 (균일 r · c · z_C = 0 · β 보정) 에 "**1D 균질화 자체의 과소**" 를 덧붙인다.  우리 최소안은 3D 망을 직접 푸니 R_eff 는 3D 값이고, **환산 (R_eff → R_ion)** 단계에서만 1D 가정이 들어간다.
- 보강 ④ **다중 봉우리** — 우리 침대의 판 근처 층 · graded-z (A7) 같은 z 구배는 전기화학 없이 두 번째 호를 만들 수 있다 — τ_e 스펙트럼을 실측 (Kim 2025 · Islam 2026 · Bazzoun) 과 대조할 때 "두 번째 호 = 계면 과정" 으로 읽지 않는다.

### 8-3. 결정 11 (복셀 ÷ 접촉망 대조 · CF 지위) — 권고 유지 · 사전등록 후보 셋
- **권고 변경 없음.**  Cooper 의 복셀 솔버도 비기하 계면 항이 0 (벽 no-flux · 이진 D) → CL-81 의 "복셀 σ 는 CF 가지 위" 구조 결론과 같은 자리.
- 사전등록 후보 ⓐ **해상도 규칙**: 최소 특징 ≥ 5 voxel (p.683 — 수렴 자료 없는 원문 규칙) ↔ 우리 d_h/dx ≥ 3.5.  부록 (lit10) 결정 11 ⓐ (격자 수렴 조건) 에 문헌 기준점으로 병기.
- 사전등록 후보 ⓑ **DC 관문**: 두 이산화에 임피던스를 붙이면 각자의 개방 ω → 0 이 각자의 1/f 를 재현해야 한다 (Cooper 가 개방계를 정상상태 해로 시작하는 것과 같은 논리, p.683).
- 아이디어 ⓒ (미검증 · 등록 아님): 그림 2 — **같은 DC tau2 에서도 스펙트럼 모양이 갈린다**.  Cooper 는 특성주파수 이동을 *"the relative contribution of extended path length and path constriction in the observed tortuosity factor"* 로 설명할 **가설**을 낸다 (p.686).  같은 침대의 복셀 (CF) 과 접촉망 (FULL — Holm 협착이 목에 집중) 은 DC 가 달라도 · 같아도 고주파 위상에서 협착 위치를 드러낼 수 있다.  다만 망에는 부피 저장을 어디에 둘지부터 정해야 하고 (노드 = 입자 부피?), l_δ < 입자 크기는 못 그린다 → 지금은 **아이디어로만**.

### 8-4. 결정 5 (COMSOL/EIS 표기) — "EIS τ" 는 경계형을 적어야 한다
- 같은 확산 임피던스 시뮬레이션이 **개방 (관통)** 이면 DC 절편 τ/ε = conventional (tau2/φ = 1/f), **폐쇄 (차단)** 이면 DC 저항이 없다 (축전 수직선 · R/3 형).  ⇒ 부록 (lit10) 결정 5 한정어 ("tau2 에 'EIS' 를 붙일 때 연결형 병기 — T형 open–open = 관통 tau2 부류 · Z/E형 = τ_e 부류") 를 지지.  **권고 변경 없음.**

### 8-5. graded-z (A7) · 판 근처 밀도 구배
- A7 (`--poro-grad`) 이나 판 근처 조밀층은 그림 5 의 구배 충전과 같은 범주다.  T (tau2) 는 위아래를 뒤집어도 같지만, 차단형 응답은 ×3 급으로 갈릴 수 있다 (그림 5 판독 — 크기는 이 충전 하나의 값, 전이 금지).  구배 설계를 T 로 순위 매기지 않는다 (nguyen 카드 ⑤ 와 같은 결론).

### 8-6. 우리 STEP4 EIS (`eis_drt_ica.py`) — 이름 함정 · DRT 해석
- 우리 회로 Z(ω) = R0 + R_ct/(1 + jωR_ctC_dl) + Z_Wo(ω) (+ 선택 R_int‖C_int 계면 호, 42 행), Z_Wo = R_w·coth(√(jωτ))/√(jωτ) · τ = r_p²/D_s (구형 고상 확산) — 파일 머리말 · `warburg_open` (`eis_drt_ica.py:6–19 · 32–34 · 42–47`, 읽기 전용 확인).  docstring 이 스스로 *"유한-공간(반사경계=삽입입자) Warburg 'Wo'"* 라 적는다 = Cooper 의 **closed (FSW)**.  ⚠ 소자 이름의 "o (open)" 와 Cooper 의 "open system" 은 **반대 경계**다 — 문서 · 그림에서 섞지 않는다.
- Cooper 경고 둘이 직접 걸린다: ① FLW 의 DRT 도 원래 봉우리가 여럿이다 (p.686) ② 비균질 (구배) 구조는 순수 확산만으로 2차 봉우리를 키운다.  우리 DRT 가 "R_ct / C_dl / Warburg / GB 시상수를 모델-자유로 분리" 한다고 쓸 때 (`eis_drt_ica.py:19`) — 봉우리 수를 과정 수로 읽는 데 한정어가 필요하다.
- 우리 Wo 는 1D (구형 반경) 소자라 Cooper 가 보인 형상 효과 (단면 변화 · 2D/3D 차) 를 담지 못한다 — 고상 확산은 입자 내부 문제라 AM 형상이 구이면 맞고, MPM 이 AM 형상을 바꾸지 않으므로 지금은 무해 (우리 해석).

### 8-7. 계면 저항 항 (CL-81 ① r_int) 이 들어갈 자리
- **이 논문 틀에는 자리가 없다** — Ω 는 입자 번호 없는 단일 연속상이고, 벽 I 는 no-flux 다.
- 들어갈 수 있는 자리는 둘이고 **물리가 다르다**: (가) 벽 I 의 Robin 조건 = **계면 임피던스** (τ_e 의 이중층 축전 · 비차단이면 R_ct 병렬) — Nguyen eSCM 이 이 자리를 쓴다 / (나) 같은 수송상 **내부 면의 직렬 저항** (서로 다른 입자 사이 = SE–SE 입계 · 접촉) — 입자 번호가 필요하고, STEP3 의 CL-81 ① 이 다른 sid (또는 같은 sid · 다른 입자 번호) 면에 r [Ω·cm²] 를 직렬로 넣는 기구가 바로 이것이다 (기본 OFF).
- ⇒ τ_e 스펙트럼 (가) 와 r_int (나) 는 **같은 코드 자리를 다투지 않는다** — 하나는 AM–SE 면의 병렬 (축전) 결합, 하나는 SE–SE 면의 직렬 저항.  면 분류 기반 (sid · pid) 은 공유할 수 있다 (우리 해석 · 미구현).

## 9. 인용 가능 문장 (deck/paper용)
- "In the frequency-domain finite-difference scheme of Cooper et al. (2017), the low-frequency intercept of the normalised diffusion impedance of an open (through-plane) system equals τ/ε, so its ω → 0 limit reproduces the steady-state (TauFactor-type) tortuosity factor; with the same full-cross-section normalisation this intercept is the inverse of our f = σ_eff/σ₀ [identity derived from their Eq. 3]."
- "Cooper et al. constructed seven 2D pore geometries with identical porosity (0.5) and tortuosity factor (1.57) whose diffusion-impedance spectra nevertheless differ at medium-to-high frequency, so agreement in the steady-state tortuosity factor does not imply agreement in frequency response."
- "In their simulations a packing with linearly graded porosity produced two arcs and a pronounced secondary DRT peak from purely diffusive transport, which the authors warn could be misinterpreted as an additional electrochemical process."
- "Their solver stores mass in the pore volume, whereas transmission-line (de Levie/Keiser) models store charge on the pore surface; the two descriptions coincide only for a uniform cross-section (their Appendix A), so the scheme is a numerical template rather than the physics of an electrode tortuosity factor."

## 10. 주의/한계 (over-claim 방지)
- **수치 방법 논문이다** — 실험 검증이 없다 (실측 EIS 대조는 후속, p.686).  인용 쓸모는 **정의 · 경계 · 진단**이고, 우리 수치와의 "일치" 근거로 쓰지 않는다.
- **물리가 다르다** — 부피 축전 Fick 확산 (액체 · 기체 확산종 예시).  ASSB SE 의 이온 전도 (단일 이온 · 이온 DC 에 부피 저장 없음) 나 τ_e (표면 이중층) 와 같은 물리가 아니다 — 일정 단면에서만 수학이 같다 (부록 A).
- **2D 사례가 대부분** (그림 1–3 · 6) — 개념 증명.  3D 는 Keiser 회전체 · 구배 구 충전 하나 · 분리막 영상 둘.  반복 실현 · 시드 통계 없음.
- **같은 τ·ε 7 기하의 "같음"** 은 시행착오 설계값 (τ 1.57 두 자리) — 판독 절편 ≈ 3.10 ↔ 계산 3.14 (−1.3 %).
- **그림 판독값** (§3-4) 은 벡터 좌표로 읽어 정밀도는 높지만 원문 명시값이 아니다 — 추세 · 비율로만 쓴다.  그림 5 의 ×3.1 비는 같은 충전 · 같은 정규화라는 전제 (완전 연결) 위에 있다.
- **그림 6 정규화 미기재** — 표의 비만 쓴다 (§3-3).
- **"경로 연장 vs 협착" 으로 특성주파수 이동을 설명하는 것은 원문의 가설**이다 (*"One potential explanation"*, p.686) — 검증 아님.
- **공개 코드의 판 · 위치는 이 논문에 없다** — 모드 4 ↔ 이 논문 대응은 툴 카드의 GUI 라벨 판단 · 모드 4 내부는 미확인.

**원문 오식 · 내부 불일치 (우리 확인)**
| # | 자리 (쪽) | 인쇄 | 맞는 것 (우리 확인) | 근거 |
|---|---|---|---|---|
| 1 | §4.2 (p.685) | 차단 끝이면 *"the imaginary component of the impedance Z̃'' goes to −1/√(2ω) and the phase approaches 90°"* | −1/√(2ω) (ωc = 1) 는 **고주파 반무한 Warburg (45°)** 의 허수부다.  차단 끝 저주파 극한은 **Z̃' → 1/3 · Z̃'' → −ωc/ω** (−φ → 90°) | 우리 재계산 (FSW = coth(s)/s): ω/ωc = 10⁻³ → Re 0.33333 · −Im·ω 1.0000 · 89.98° / ω/ωc = 10²–10⁴ → Im = −1/√(2ω) 정확 · 45.00°.  그림 1 · 3b 곧은 기공 수직선 ≈ 0.33 (판독) 이 1/3 과 맞는다 |
| 2 | §4.2 (p.686) | *"D = 10⁻⁹ m s⁻²"* · *"D = 10⁻⁵ m s⁻²"* | **m² s⁻¹** | 확산도 차원 |
| 3 | §4.2 (p.686) | ω ≈ 10³ · 10 · 10⁻³ **Hz** (액체) · 10⁷ · 10⁵ · 10 **Hz** (기체) | 값 = D/l_δ² (식 4) = **s⁻¹ (각주파수)**.  Hz (f) 로 읽으면 실제 주파수는 2π 배 작다 | 우리 재계산 — 여섯 값 전부 D/l_δ² 와 같다 |
| 4 | 그림 1 (p.683) | 주축 기호 Ẑ (hat) — "두 번째 정규화" | 식 정의 없음 (곧은 기공 값으로 모이게 했다는 문장만) | 캡션 |
| 5 | 그림 6 (p.687) | Z̃'(ω=0) 표 | 정규화 (A · L) 미기재 → 절대값 해석 불가 | §3-3 |
| 6 | §2.2 · §3 (p.683) | "a set of 6 new idealised 2D geometries" ↔ "the seven 2D open-systems" | 오류 아님 — 기하 1 (기준) + 새 6 (p.684 "the other six geometries") | 확인만 |
| 7 | 잔 오식 | "semi-cricle" (p.682) · "The separators where imaged" (p.684) · "These structures where chosen" (p.683) | circle · were · were | 뜻 무영향 |

**이 논문을 인용하는 기존 카드와의 대조** (그 카드는 고치지 않음 — 메인 판단)
| 카드 · 자리 | 카드 서술 | 원문 대조 |
|---|---|---|
| `nguyen2020_electrode_tortuosity_factor` §11 ref 42 행 | "TauFactor mode 4 (확산 임피던스) 의 근거 + **부록에 eSCM 과의 수학 대응 (p10)** — 접촉망 임피던스 구현 시 참고" | ⚠ 부분 일치.  Cooper 부록 A 는 **Keiser · Eloot (de Levie 계) 축전 벽 기공 ↔ 확산 기공**의 pseudo-3D 대응이다 (A.1–A.4, p.687).  "eSCM" · 대칭셀 · τ_e 낱말은 Cooper 원문에 **없다** (텍스트 검색 0 회) — eSCM 은 Nguyen 의 이름.  대응은 **일정 단면에서만 동일** (1/r̃) 이라는 한정어가 필요.  "(p10)" 은 Nguyen 쪽 번호로 읽힌다 (Cooper 는 681–689) — Nguyen p10 원문은 이 카드에서 재확인 안 함 [미확인] |
| `taufactor_tortuosity_factor_tomography_tool` 모드 목록 (모드 4) | "`4. Diffusion Impedance Spectrum w/ Mirror` — Cooper 2017 (Electrochim. Acta 251) 확산 임피던스" | ✅ 정합 — TauFactor 통합 (p.681 · p.687) · 거울 대칭 이용 (p.683).  원문은 "mode 4" 라는 이름을 쓰지 않는다 (대응은 툴 카드 판단) |
| `tjaden2018_tortuosity_review_calculation_approaches` | 이 논문 제목 · DOI 없음 (grep 0 건) | 인용 목록에 이름이 올랐다면 원 리뷰 참고문헌에 있을 수 있다 — 이 카드에서 Tjaden 원문 미확인 [미확인] |
| `kim2025_impedance_decoupling_tlm_assb` (`figures.json`) | Fig 6 캡션 "(e) Simulated impedance spectra with varied Rint/Ri values" | Kim 자체 TLM 모사 그림이다 — 카드 · figures.json 어디에도 Cooper 서지 없음 (grep 0) → **검색 오탐**으로 보인다 |

**메모 v2 정정 후보** (`docs/reviews/tau_conventions_judgment_v2_20261003.md`)
| # | 메모 자리 | 현재 문장 | 원문 근거 | 제안 |
|---|---|---|---|---|
| A | §8-2 Cooper 행 "왜" | "망 임피던스 (τ_e) 구현 참고" (닫는 항목 §7 최소안) | 식 1 = 부피 저장 확산 (p.682) · *"does not reflect … charge separation (i.e., double layers)"* (p.683) · 표면 축전은 부록 (A.3)–(A.4) pseudo-3D 비교뿐 · 일정 단면에서만 동일 (p.685 · p.687) | **정밀화**: "주파수 영역 FD 틀 · open/closed 경계 · Z̃ 정규화 (개방 DC = τ/ε = conventional) · DC 관문 · 진단 (Warburg 이탈 · 다중 봉우리 · RVE · 1D 과소) 참고 — **τ_e 지배식의 원전 아님** (원전 = Nguyen eSCM · TauFactor 모드 5–6)" |
| B (보강) | §7 최소안 "SE 망 + AM–SE 접촉을 축전 sink 로 (ω → 0 극한 = 접촉 면적 비례 균일 sink)" | (맞다) | *"capacitance scales with the pore surface … with the pore volume"* (p.685) · 1/r̃ (p.687) | 정정 아님 — 한정어 후보: "sink 를 SE **부피**에 두면 (Cooper 식 1 꼴) τ_e 가 아니라 확산 임피던스다 → 면적 가중을 시험으로 고정".  Cooper 의 "minor differences" (p.685) 는 모든 벽이 축전인 액체 기공 — ASSB 전이 금지 (우리 해석) |
| C (보강) | §7 최소안 "R_ion = 3·R_eff (Nguyen Eq 5)" | 균일 조건 한정어 (부록 lit10 §1 결정 13 ⓑ) | 그림 6 표 (p.687): pseudo-3D (1D) 가 3D 대비 Z′(0) −19 % (A_T/A_B 0.01) · −23 % (3) · φ(ω) 고주파 쪽 이동 (p.687–688) | 한정어에 "1D 균질화 자체의 과소" 추가 — 단면 변화가 큰 침대에서는 환산 R_eff → R_ion 을 3D 해로 검증 |
| D (보강) | §7 · nguyen ④ "T 는 방향 맹" · 결정 13 진단 | — | 그림 5 (p.685): 같은 충전 뒤집기 — 개방 절편 같음 (≈ 4.1–4.2) · 폐쇄 저주파 실수부 ≈ 0.74 ↔ 2.27 (×3.1, 판독) | 차단형 = 방향 의존 · 관통형 = 방향 맹의 **두 번째 독립 사례** (부피 축전 확산) — 근거 문장에 병기 후보 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
- **렌더**: 9 쪽 전부 2 배 렌더 + 식 (1)–(3) · (A.1)–(A.4) · p.683 τ/ε 문장 · p.685 차단 극한 문장 · 그림 1 · 2 · 3 · 4 · 5 · 6 (inset 표 포함) 을 3.5–6 배로 다시 읽었다.
- **그림 판독법**: 그림이 벡터 경로라서 PDF 의 경로 좌표를 직접 읽었다 (pymupdf `get_drawings`).  축 보정 = 눈금 라벨 글리프 · 눈금선의 위치 (예: 그림 4 아래 축 0 · 2 · 4 · 6 = 24.53 pt/단위, 위 축 0–3 = 59.0 pt/단위).  표지 = 빨간/검은 * · ○ 중심.  **판독법 검증**: 그림 4 의 FLW 회색 원 (ω = ωc) 이 Z̃'/Z̃'(0) = 0.885 (두 판 모두) — 해석해 FLW(ω = ωc) = 0.8855 와 일치.  그림 3b 0 차 수직선 0.330 = FSW 1/3.
- **검산 1 — 해석해 극한** (§3-6 · 오식 1): FLW = tanh(s)/s · FSW = coth(s)/s (s = √(iω/ωc)) 를 복소수로 계산 — FSW 저주파 Re → 0.33333 · −Im·ω → 1.0000 · 위상 → 89.98° (ω/ωc 10⁻³) · 고주파 Im = −1/√(2ω) · 45.00° (10²–10⁴) · FLW 저주파 Re → 1.
- **검산 2 — 원문 산술**: 1.57/0.5 = 3.14 · 5·3⁶ = 3645 · 창 2¹⁵ = 4.5 decade · 그림 6 비 0.809 · 0.773 · p.686 표 여섯 값 = D/l_δ² · 창 상한 l_δ = L/√2048 = 0.0221 L.
- **텍스트 검색** (본문 p.681–687): "tortuosity factor" 10 회 · "Warburg" 17 회 · "capacitance" 5 회 · "constriction" 2 회 · "representative" 4 회 · "double layers" 1 회 (범위 밖 물리로) · "migration" 1 회 · **"eSCM" · "charge transfer" · "Faradaic" · "MacMullin" · "Bruggeman" · "dead" · "percolat" 0 회** · "symmetric" 은 axisymmetric · axi-symmetric 뿐 (대칭셀 아님).
- **우리 리포 (읽기 전용 grep)**: `network_conductivity.py` · `step3_sigma.py` · `voxel_conductivity.py` 에 복소 · 주파수 표현 0 건 · `eis_drt_ica.py` 의 Wo = coth 꼴 (6–19 · 32–34 행) · `step3_sigma.py` 의 `parse_rint_table` (`--step3-rint`, Ω·cm², 기본 OFF).
- **중복 확인 (10-03)**: 정본 `litdb/papers/` 파일 목록 365 항목에 이 slug 없음 · `git grep` DOI (`10.1016/j.electacta.2017.07.152` · `electacta.2017.07.152`) 0 건 · 제목 낱말 grep 은 `nguyen2020_electrode_tortuosity_factor` (ref 42 인용) 한 곳 · "Cooper" + 2017/impedance 는 nguyen · taufactor 카드의 **인용**뿐.

## 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 원문 번호 · 서지 (p.688–689) | 왜 |
|---|---|
| [3] U. Tröltzsch, O. Kanoun, Generalization of transmission line models for deriving the impedance of diffusion and porous media, Electrochimica Acta 75 (2012) 347–356. | 확산 ↔ TLM 의 수학 동일성 일반화 (곧은 기공이면 같은 Warburg — p.685 인용) · siroma · pouraghajan 카드도 인용 |
| [6] H. Keiser, K.D. Beccu, M.A. Gutjahr, Abschätzung der porenstruktur poröser elektroden aus impedanzmessungen, Electrochimica Acta 21 (1976) 539–543. | 기공 형상 → 임피던스의 원조 (독일어) — 이 논문 그림 1 의 원본 |
| [7] R. de Levie, On porous electrodes in electrolyte solutions: I. Capacitance effects, Electrochimica Acta 8 (1963) 751–780. | TLM 원조 · 표면 축전 (τ_e 물리) 의 출발 — siroma 카드 [1] 과 같은 논문 |
| [9] K. Eloot, F. Debuyck, M. Moors, A.P. Van Peteghem, Calculation of the impedance of noncylindrical pores Part I: Introduction of a matrix calculation method, Journal of Applied Electrochemistry 25 (1995) 326–333. | 비원통 기공의 표면 축전 임피던스 (부록 A.3 의 물리) |
| [29] J.R. Macdonald, Utility and Importance of Poisson-Nernst-Planck Immittance-Spectroscopy Fitting Models, The Journal of Physical Chemistry C 117 (2013) 23433–23450. | 이동 · 이중층을 넣을 때의 일반 틀 (이 논문 범위 밖이라 적은 것) |
| [41] J. Song, M.Z. Bazant, Effects of Nanoparticle Geometry and Size Distribution on Diffusion Impedance of Battery Electrodes, Journal of The Electrochemical Society 160 (2013) A15–A24. | 입자 내부 고상 확산 임피던스 (실제 배터리의 확산 임피던스, p.683) · 차단 극한 문장의 인용원 (p.685) — 우리 STEP4 Wo 와 같은 자리 |
| [43] D.P. Finegan, S.J. Cooper, B. Tjaden, O.O. Taiwo, J. Gelb, G. Hinds, D.J.L. Brett, P.R. Shearing, Characterising the structural properties of polymer separators for lithium-ion batteries in 3D using phase contrast X-ray microscopy, Journal of Power Sources 333 (2016) 184–192. | 그림 4 분리막의 τ · ε 원값 (이 논문엔 없음) — τ 역산 · 판독 검증 |
| [44] C. Chueh, A. Bertei, J. Pharoah, C. Nicolella, Effective conductivity in random porous media with convex and non-convex porosity, International Journal of Heat and Mass Transfer 71 (2014) 183–188. | 그림 5 충전 생성기 · 무작위 다공 매질 유효 전도도 (Bruggeman 류 관계의 비교점) |
| [45] T.H. Wan, M. Saccoccio, C. Chen, F. Ciucci, Influence of the Discretization Methods on the Distribution of Relaxation Times Deconvolution: Implementing Radial Basis Functions with DRTtools, Electrochimica Acta 184 (2015) 483–499. | DRT 도구 — 우리 `eis_drt_ica.py` Tikhonov DRT 의 비교 기준 |
| [47] J. Gunning, The exact impedance of the de Levie grooved electrode, Journal of Electroanalytical Chemistry 392 (1995) 1–11. | pseudo-3D (등농도면 ⊥) 의 한계 — 1D 과소의 해석적 근거 |
| [48] M. Musiani, M. Orazem, B. Tribollet, V. Vivier, Impedance of blocking electrodes having parallel cylindrical pores with distributed radii, Electrochimica Acta 56 (2011) 8014–8022. | 기공 반지름 분포 → 눌린 호 (차단 전극) |
| [49] J.-P. Candy, P. Fouilloux, M. Keddam, H. Takenouti, The characterization of porous electrodes by impedance measurements, Electrochimica Acta 26 (1981) 1029–1034. | 균질 구 충전의 작은 왜곡 (그림 4 정합 근거) |
| [58] A. Bertei, G. Arcolini, C. Nicolella, P. Piccardo, Effect of Non-Uniform Electrode Microstructure in Gas Diffusion Impedance, ECS Transactions 68 (2015) 2897–2905. | 비균질 미세구조 → 추가 회로 요소 오용 (다중 봉우리 경고의 선행) |
| [59] H.-K. Song, Y.-H. Jung, K.-H. Lee, L.H. Dao, Electrochemical impedance spectroscopy of porous electrodes: the effect of pore size distribution, Electrochimica Acta 44 (1999) 3513–3519. · [60] H.-K. Song, J.-H. Sung, Y.-H. Jung, K.-H. Lee, L.H. Dao, M.-H. Kim, H.-N. Kim, Electrochemical Porosimetry, Journal of The Electrochemical Society 151 (2004) E102. | 임피던스 → 기공 구조 역추정 (이 논문의 "역이용" 비교점) |
| [24] (TauFactor, SoftwareX 2016) | 정본 카드 있음 — `taufactor_tortuosity_factor_tomography_tool` |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
