# 🎤 Research Seminar spec — DFT-based screening cascade for sulfide SEs

> **발표자** 안용훈 (Yonghoon An) · Division of Materials Science & Engineering, Hanyang University
> **형식** 이가형 연구세미나 템플릿 승계 — 4:3 · 표지 "Research Seminar" · `Part N` 구분 ·
> 섹션 헤더(navy bold) · `■` 대제목 / `·` 소제목 · 우상단 약어정의 + 참고문헌(이탤릭) ·
> 하단 HANYANG UNIVERSITY / Battery Materials Lab. / 페이지번호
> **분량** 본문 18 + Appendix 6 = 24
>
> **청중** 대학원생 수준 · **처음 보는 사람 다수** → ① 모르는 사람 기준으로 깔고
> ② 모든 수치에 "어떻게 얻었나"를 붙이고 ③ **defense 를 appendix 에 두껍게**.
>
> ⚠⚠ **수치 규율** — 이 spec 의 모든 값은 `db/properties/` canonical 기준이다.
> 2026-06-15 덱의 일부 값은 **그 후 철회·갱신**됐다(§What we got wrong 참조).
> 용어는 `kb/methodology/terminology_register.md` 를 따른다.

---

## Part 1 — Why compute? (Motivation)

### S1. 문제 정의 — 후보는 많고 실험은 느리다
- `■` The screening problem in sulfide solid electrolytes
- `·` 조성 공간이 조합적으로 커진다 — 아지로다이트 하나만 해도 halogen 종·비율·도펀트
- `·` 실험 1점 = 합성 + XRD + EIS + 셀조립 ≈ **수 주**. 계산 1점 = **수 시간~수 일**
- `·` 그래서 **계산은 실험을 대체하는 게 아니라 실험이 갈 곳을 좁힌다**
- 🖼 왼쪽: 조성공간 팬아웃 도식 / 오른쪽: 우리 cascade 47종 funnel 미리보기
- 📚 `sendek2017_ml_screening_12k_conductors` (EES 2017) — 12,000종 스크리닝의 선례

### S2. 그런데 계산도 틀린다 — 이 발표의 두 번째 주제
- `■` Screening is only as good as its gates
- `·` 이 발표는 **성공 사례집이 아니다.** 우리가 낸 판정 중 **철회한 것들**을 같이 보여준다
- `·` 스크리닝의 가치는 **후보를 고르는 능력**이 아니라 **틀린 후보를 걸러내는 게이트**에 있다
- → 이 발표의 구조: ① DFT 가 무엇을 주나 → ② 우리가 돌린 계산들 → ③ LPSCl 결과와 착상 →
  ④ cascade 방법론 → ⑤ **무엇을 틀렸나** → ⑥ 앞으로

---

## Part 2 — DFT: 무엇을 계산하고 무엇을 못 하나

### S3. 왜 슈뢰딩거 방정식을 못 푸나
- `■` The many-electron problem
- `·` N 전자 파동함수 Ψ(r₁…r_N) 는 **3N 차원** — 전자 100개면 300차원. 저장 자체가 불가능
- `·` **Hohenberg–Kohn**: 바닥상태 성질은 **전자밀도 n(r) (3차원)** 만으로 결정된다
- `·` **Kohn–Sham**: 상호작용하는 실제 계를 **같은 밀도를 주는 가상의 비상호작용 계**로 치환
- `·` 모르는 것을 전부 **교환–상관 범함수 E_xc[n]** 에 몰아넣었다 → **여기가 근사가 들어가는 유일한 곳**
- 🖼 3N 차원 → 3차원 축소 도식
- 📚 Hohenberg & Kohn (1964) · Kohn & Sham (1965) ⚠ 원전 미보유 — PDF 확보 필요

### S4. XC 근사와 그 대가
- `■` Exchange–correlation approximations: what they cost us
- `·` LDA → GGA(PBE) → meta-GGA → hybrid. 정확도와 비용이 같이 오른다
- `·` ⚠ **semi-local 범함수는 밴드갭을 과소평가**한다 — "PBE 라서" 가 아니라
  **미분 불연속(derivative discontinuity)이 없어서**다
- `·` **DFT+U**: 국재된 d/f 전자(우리 계의 Ni 3d)에 on-site 반발을 넣어 자기상호작용 오차를 완화
- `·` ⚠ U 는 **경험 파라미터**다. 어느 원자·어느 오비탈에 얼마를 걸었는지 반드시 밝힌다 (우리: Ni 3d, U = 6.2 eV)
- 📚 `he2019_dft_for_battery_materials_review` (EEM 2019)

### S5. DFT 가 주는 것 — 관측량 사다리
- `■` From total energy to observables
- 표 (왼쪽 = 계산량, 오른쪽 = 무엇을 판정하나):

| 계산량 | 나오는 것 | 우리가 판정하는 것 |
|---|---|---|
| E(V) 곡선 | **BM3 EOS → B₀** | 압축 강성 |
| 유한변형 응력 | **C_ij → VRH (E, G, B)** | 탄성·이방성 |
| 고유값 (fixed-occ nscf) | **fundamental gap (VBM–CBM)** | 전자 절연 |
| 파동함수 투영 | **DOS / PDOS** | 어느 오비탈이 밴드끝인가 |
| COHP | **−ICOHP** | 결합별 세기 |
| grand potential | **ESW** | 전기화학 안정창 |
| MD 궤적 | **MSD → D → Ea** | 이온 수송 |

- ⚠ **못 하는 것도 같이 적는다** — 파괴인성 K_IC(시편 물성), μm 입자 역학, 공간전하층 정량
- 📚 `famprikis2019_fundamentals_inorganic_sse` (Nat. Mater. 2019)

### S6. MLIP — 왜 필요하고 어디까지 믿나
- `■` Machine-learned interatomic potentials
- `·` DFT 는 계 크기 N 에 대해 **O(N³)**. 62원자 200 ps MD 를 DFT 로는 못 돈다
- `·` MLIP = **DFT 에너지·힘의 회귀 대체 모델**. 정확도를 DFT 에서 물려받고 속도는 고전 퍼텐셜급
- `·` ⚠ **"AI 계산" 이라고 부르지 않는다** — 대체 모델이지 추론 엔진이 아니다
- `·` ⚠ 한계: **전하 상태·산화수를 명시적으로 안 다룬다.** 우리 계에서 실제로 걸렸다(S16)
- 우리 표준: **UMA-s-1p1 (task=omat)** · Langevin NVT · dt 2 fs · MSD 창 2–50 ps
- 📚 `kahle2020_ht_aimd_screening` (EES 2020)

---

## Part 3 — 내가 돌린 계산들 (variation)

### S7. 3-tier pipeline
- `■` MLIP screening → DFT validation → post-processing
- 3열 박스 (2026-06 덱 계승, 내용 갱신):
  - **MLIP screening**: halogen enumerate → Li sublattice screen → 500 K Langevin anneal
  - **DFT validation**: MLIP EOS pre-scan → BM3 EOS 11 volumes → V₀ 확인(BFGS) → k-mesh 수렴
  - **Post-processing**: 구조(Voronoi·BVSE) / 전자(DOS·ELF) / 결합(Bader·ICOHP) /
    수송(MLIP MD) / 역학(C_ij) / 전기화학(ESW)
- `·` **같은 프로토콜을 모든 조성에 적용** — 그래야 조성 간 비교가 성립한다

### S8. 문제 유형 4가지 — 같은 도구, 다른 셋업
- `■` Four problem classes I have run
- 2×2 그리드:
  1. **Bulk periodic** (LPSCl 계열) — 절대값 비교 가능, 축만 맞추면
  2. **Doped supercell** (47종 cascade) — Δe·ox_V·BVS proxy. 상대 비교 전용
  3. **Slab + adsorbate** (SDCP × LiNiO₂(104)) — 진공·구속·좌표일치가 추가 변수
  4. **Isolated molecule** (SDCP 계열, ORCA r²SCAN-3c) — 평면파 부적합, 국소기저로
- `·` ⚠ 유형이 다르면 **에너지를 직접 못 비교**한다. 각 유형 안에서만

### S9. 비교가 성립하려면 — 일관성 축
- `■` What must match before you tabulate absolute values
- 표: 물성 × "맞춰야 할 축" (`kb/methodology/computational_methods_canonical.md` §1)

| 물성 | 맞춰야 할 축 | pseudo 민감 |
|---|---|---|
| Elastic C_ij | pseudo · ecut · k-density · **셀타입** · strain · **clamped/relaxed** | 예 |
| EOS B₀ | pseudo · ecut · k · 조성 | 예 |
| Band gap | pseudo · ecut · k · **판독법(eigenvalue)** | 예 |
| ICOHP | **all-PAW 필수** · basis · nbnd | 예 |
| MD (Ea) | UMA버전 · MD프로토콜 · **멀티시드** | 아니오 |

- `·` **황금률**: 하나라도 다르면 절대값 표를 만들지 않는다 → "순위/방향 + 각주"
- ★ 실측 사례: **clamped-ion 은 아지로다이트 탄성을 실험의 ~2.3배로 부풀린다**
  (comp1 clamped E_VRH **52.31** vs relaxed **22.06**, 실험 ~23)
  📚 `deng2016_elastic_superionic_electrolytes_dft` · `famprikis2019_…` (glass 실측 E≈20/G≈7)

---

## Part 4 — Results: LPSCl vs LPSCl₁.₆, 그리고 착상

### S10. 두 아지로다이트 — 같은 원소, 다른 비율
- `■` Li₆PS₅Cl vs Li₅.₄PS₄.₄Cl₁.₆
- `·` 5 f.u. 기준 **Li −3 · S −3 · Cl +3** — 원소는 같고 비율만 이동
- `·` 실험: Cl-rich 가 **σ 더 높고 더 단단**하다고 보고
- `·` **질문: 그 이득의 구조적 기원은 무엇인가?**
- 🖼 조성 변환 도식 + 두 champion 셀 (cubic-52 / rhombo-62)

### S11. M1 — 전자구조는 거의 같다
- `■` The electronic structure is nearly invariant
- `·` **fundamental gap 2.066 vs 2.099 eV** (Δ = 0.033) — fixed-occupation nscf 고유값
- `·` ⚠ **DOS-threshold 판독 금지** — 그 방식은 ~0.3 eV 과소평가한다(우리 규율)
- `·` VBM = S 3p 지배, CBM = Li 2s + P 3s — **성격도 같다**
- → **σ 2배 이상 차이를 전자구조로는 설명 못 한다.** 원인은 구조 쪽에 있다
- 🖼 DOS 겹쳐 그리기 + gap 표

### S12. M2 — 수송 이득은 장벽 + 캐리어 둘 다
- `■` Two mechanisms, both operative
- `·` **Ea (멀티시드)**: modelc **0.197 ± 0.032 eV** (3-seed, 확산영역 게이트 통과)
- `·` ⛔ **comp1 은 현재 인용 가능한 Ea 가 없다** — 200 ps 게이트 0/6, 1600 ps 로도 1/3 통과
- `·` D₀ prefactor: Cl-rich 가 더 큼 = **공공 캐리어 증가**
- `·` ⚠ **σ 절대값은 인용하지 않는다** (§S16)
- 🖼 아레니우스 플롯 + MSD 곡선(β 표시)
- 📚 `kahle2020_…` (diffusive-regime criterion)

### S13. M3 — Li–anion 이온결합이 강해진다
- `■` Li–anion bonds strengthen; the PS₄ framework does not change
- `·` **P–S 5.94 → 6.00 (+1 %)** — 골격은 그대로
- `·` **Li–Cl 1.86 → 2.10 (+13 %)** · **Li–S 1.59 → 1.72 (+8 %)** (|ICOHP| eV/bond)
- `·` 분해: **vacancy field 69 %** (4a 자리, Cl 의 90 %) + **4d anti-site 31 %**
  (4 bonds, −2.836 eV/bond = 4a 대비 +40 %)
- → **소수의 anti-site 가 불균형하게 큰 기여**를 한다
- 🖼 막대(결합별 ICOHP) + per-site 분해표

### S14. ★ 착상 — 치환은 전자구조가 아니라 무질서를 바꾼다
- `■` The screening axis should be structural, not electronic
- `·` M1(전자 불변) + M2(수송 이득) + M3(이온결합 강화)를 합치면:
  **halogen 치환의 효과는 전자구조 재편이 아니라 Li 공공 + anion anti-site 라는 무질서 생성**
- `·` → 그러면 **스크리닝 기술자도 전자적인 것이 아니라 구조적인 것이어야** 한다
- `·` 그것이 우리 cascade 의 축 선택 근거다: Δe(구조 안정) · BVS proxy(채널) ·
  disorder std(무질서 유도) · C_ij(역학) — **전자 축은 절연 확인용으로만**
- 🖼 M1/M2/M3 → 착상 → cascade 축 매핑 화살표

---

## Part 5 — Cascade: 방법론과 검증

### S15. 필드는 어떻게 스크리닝하나
- `■` How the field screens
- 3 사례 (전부 우리 litdb 보유):
  - **`sendek2017`** (EES 2017) — 12,000종 → ML 분류기 → 소수 후보. **값싼 기술자 → 비싼 검증**
  - **`xiao2019`** (2019) — CAM 코팅 스크리닝. MP 기반 열역학 필터
  - **`richards2016`** (Chem. Mater. 2016) — **pseudo-binary 계면 반응에너지**로 계면 안정성
- `·` 공통 구조: **funnel** — 넓게 시작해 각 단계에서 물리적 게이트로 좁힌다
- `·` ⚠ 공통 약점: **게이트의 실패율을 보고하지 않는다**

### S16. 우리 cascade — 47종 × 14 테마
- `■` Our cascade: 47 dopants, 14 design axes
- `·` 축: 산화안정 · 환원안정 · 전자절연 · Li수송 · 무질서유도 · 농도내성 · 경량 · 저비용 ·
  연질 · 연성 · **공기내성(정성)** · **공기내성(문헌 ΔG_hyd)** · 구조안정 · 종합
- `·` 임의 축 조합은 **기하평균**으로 — 한 축이라도 바닥이면 종합도 바닥(AND 의미)
- `·` ⚠ **데이터 없음 ≠ 나쁨** — 결측 축이 있는 후보는 0 으로 깔지 않고 **랭킹에서 제외**하고 명시
- 🖼 funnel + 테마 그리드 스크린샷 (webapp `/cascade`)

### S17. ★ What we got wrong — 철회한 판정들
- `■` Retracted verdicts, and the gates that caught them
- 표:

| 철회한 판정 | 무엇이 문제였나 | 잡아낸 게이트 |
|---|---|---|
| σ 비율 1.33× (단일시드) | 시드 하나로 낸 비율 | **멀티시드 요구** (2026-07-09) |
| comp1 Ea 0.253 eV | MSD 가 확산영역에 없었다 | **β 게이트** (0/6 실패) |
| gap DOS-threshold 판독 | ~0.3 eV 과소 | **fixed-occ eigenvalue 규약** |
| `air_hsab` 등급 | 실제 구동변수는 softness 가 아니라 **oxophilicity** | **[Zhu20] SI 대조** — 35종 중 **9종 어긋남, 전부 과소평가** |
| SDCP E_ads −0.26 eV | 슬랩을 얼려서 표면 이완을 막았다 | **구속 완화 대조** — −1.465 로 4× |

- ★ 마지막 줄이 이 발표의 핵심 메시지: **제약 조건 하나가 결론을 바꾼다**
- 그리고 그 −1.465 조차 흡착이 아니라 **표면 Li⁺ 추출**이었다(구조 검증에서 드러남)

### S18. 검증 전략 — 무엇으로 걸러내나
- `■` Validation strategy
- `·` **확산영역 게이트** β = d log⟨r²⟩/d log t ∈ [0.8, 1.2] — 없으면 케이지 기울기를 D 로 착각
- `·` **멀티시드** — 단일시드 판정 금지. 앙상블 평균 MSD 의 β 로 판정(시드별 β 평균이 아니다)
- `·` **문헌 대조** — [Zhu20] SI 전수 전사(99행)와 우리 정성 등급을 산화수까지 맞춰 대조:
  **일치 26 / 어긋남 9 / 문헌 없음 12**
- `·` **구조 검증** — 에너지가 깊어졌다고 결합이 아니다. 분자 무손상 · 접촉거리 · **원자 이탈** 확인
- `·` ⚠ **못 하는 것을 먼저 말한다** — K_IC, μm 입자 역학, 공간전하층 정량
- 📚 `zhu2020_air_stable_se_design_principles` (Angew. 2020)

---

## Part 6 — 결론과 계획

### S19. Conclusions
- `·` LPSCl₁.₆ 의 이득은 **전자구조가 아니라 무질서**(Li 공공 + 4d-Cl anti-site)에서 온다
- `·` 그래서 스크리닝 축을 **구조적 기술자**로 세웠고, 47종 × 14 축 cascade 로 구현했다
- `·` 게이트가 실제로 작동한다 — **자체 판정 5건을 철회**시켰다
- `·` 문헌 대조에서 우리 정성 축의 **체계적 편향(9/35, 전부 과소평가)** 을 찾았다

### S20. Future plan
- `·` **단기** — comp1 셀 확대(게이트 통과), 6점 아레니우스(500–1000 K), SDCP Phase-B DFT+U
- `·` **중기** — ΔG_hyd 직접 계산으로 정성 등급 **대체** · ΔV_rxn × C_ij 로 화학–역학 다리
- `·` **장기** — 원자 스케일(DFT/MLIP) → **입자 스케일(DEM)** 연결.
  우리가 재료 상수(E·G·γ·ΔV)를 대고 DEM 이 접촉면적·굴곡도·유효 σ 를 낸다
- 🖼 스케일 사다리 (Å → nm → μm → mm) 에 우리 도구 배치

---

## Appendix (defense)

### A1. DFT 용어 — SCF · pseudopotential · k-mesh · XC · U · smearing
### A2. 물성 용어 — EOS/BM3 · C_ij/VRH · ICOHP(부호 주의) · ELF · Bader · ESW · E_hull
### A3. 수송 용어 — MSD · β · Arrhenius · Nernst–Einstein(Haven=1 근사) · D₀ 분해
### A4. 계산 조건 전수표 — 조성별 pseudo/ecut/k/셀/시드
### A5. ★ 예상 질문 10 (아래 §Q)
### A6. References — litdb 보유 목록

---

## §Q. Defense — 예상 질문과 답

| # | 질문 | 답의 뼈대 |
|---|---|---|
| Q1 | **DFT 가 갭을 과소평가하는데 2.07 eV 를 믿나?** | 절대값은 안 믿는다. **같은 방법 안의 차이(0.033 eV)** 만 쓴다. 그리고 그 차이가 작다는 것이 결론(M1)이지 크기가 결론이 아니다 |
| Q2 | **왜 σ 를 안 보여주나?** ★최다 예상 | 그룹 간 재현성이 **1자릿수로 갈린다**(`famprikis2019`). 우리도 단일시드 1.33× 판정을 냈다가 철회했다. 그래서 σ 절대값은 인용하지 않고 비율도 멀티시드 게이트 통과분만 쓴다 |
| Q3 | **MLIP 가 DFT 를 대체하나? 오차는?** | 대체가 아니라 **스크리닝 단계용 대체 모델**이다. 챔피언은 반드시 DFT 로 재검한다. 그리고 MLIP 는 **전하 상태를 못 다룬다** — 우리 계에서 실제로 걸렸다(S17 마지막 줄) |
| Q4 | **47종이 실험으로 검증됐나?** | 아니다. **DFT 검증은 Nd₂O₃·B₂O₃ 둘뿐**이다. 나머지는 UMA 상대 순위다. 그래서 절대값 표를 안 만들고 순위+각주로만 쓴다 |
| Q5 | **cascade 순위가 방법에 얼마나 의존하나?** | 크게 의존한다. 그래서 게이트 통과/탈락을 **평탄화**해서 게이트 상태와 값이 교차하지 못하게 했고, 동점군 내 순위는 무의미하다고 명시한다 |
| Q6 | **왜 U = 6.2 인가?** | 이 계보에서 확립된 값이며 **경험 파라미터**다. U 를 바꾸면 결과가 바뀐다 — 그래서 U 를 고정하고 **같은 U 안의 차이**만 인용한다 |
| Q7 | **Γ-only k-point 로 흡착에너지를 내도 되나?** | 개별 E_ads 에는 그대로 실린다(각주 필수). 우리 결론은 **Δ(doped−neutral)** 이고 같은 셀·같은 k 라 k-오차가 대부분 상쇄된다 |
| Q8 | **왜 파괴인성을 안 다루나?** | K_IC 는 치밀도·입경·기공에 의존하는 **시편 물성**이라 원자 스케일 계산의 산출물이 아니다(`famprikis2019` 명시). 우리는 탄성상수까지만 대고 그 위는 DEM/연속체 몫이다 |
| Q9 | **문헌 ΔG_hyd 와 우리 값을 왜 같은 표에 안 넣나?** | 계산 수준이 다르다(문헌 = MP GGA-PBE + NIST-JANAF 혼합, 300 K, 특정 부분압). 소환값과 우리 값을 섞으면 둘 다 못 쓰게 된다 |
| Q10 | **슬랩을 얼린 게 결과를 바꿨다면, 다른 계산도 그런 거 아닌가?** | 정확히 그렇다. 그래서 **구속 조건을 결과와 함께 보고**하고, 중요한 판정은 **구속을 바꿔 대조**한다. 이번 사례가 그 절차의 실물이다 |

> ⚠ **인용 규율** — 위 답에서 문헌을 대는 항목(Q2·Q8)은 `litdb/papers/` 에 실물이 있는 것만이다.
> `⚠ 원전 미보유` 인 항목(Hohenberg–Kohn, Kohn–Sham, Pugh, Dronskowski, Dudarev, IUPAC)은
> **발표 전 PDF 확보**가 필요하다 — 기억으로 서지를 쓰지 않는다.
