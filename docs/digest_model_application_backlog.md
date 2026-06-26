# Digest → MODEL APPLICATION backlog (안 적용한 것 추적, LIVING)

논문 digest에서 "모델에 적용하자"로 식별했으나 **아직 코드/모델에 반영 안 한** 항목 추적.  digest는 끝나도
**적용은 별개** — 이 표가 그 잔여작업.  (출처: stage2_model_audit_vs_literature.md E2/E3/E4 + 각 lit_*.md +
사용자 enhancement 리스트 "σ_e 방향 + Phase5 graded-z + MPM --coh E3 + dispersion CV E2 + pore-τ DiffuDict".)
상태: ⛔ TODO · 🔶 IN-PROGRESS · ✅ DONE.

## A. 우선순위 (사용자 plan + 새 발견)

| # | 항목 | 출처 digest | 대상 코드 | 상태 | 노트 |
|---|---|---|---|---|---|
| A1 | **σ_e 조성방향 수정** — σ_S/σ_P를 LOCKED "single>poly"에서 **재료별 INPUT**으로; Trevisanello 인용 제거/교체 | Trevisanello 2021 (#11 mis-attribution), Oh #266 (poly>single 반대) | generate_comparison_plots.py `_SIGMA_S/P_LOCKED`, network_conductivity NCM(r) | ⛔ | ★ Phase-3 전 필수.  finalized form 변경이라 신중(사용자 합의 후).  Trevisanello엔 전자σ 없음(확산/표면적만) — 값·출처 둘 다 오배선 |
| A2 | **wallP 조건부 (skeleton-spring) production 채택** | (자체 MPM 작업) | mpm3d_compaction `--floor-porosity`, mpm_input_from_case 자동주입 | 🔶 | sweep 단조 ✅; real14 trust test(불변) 통과하면 채택.  +CBD도 적용됨(Q1) |
| A3 | **E3 MPM `--coh` distribution-aware (binder 양역할)** — 과잉=σ차단/전해질차단, 부재=delamination; SAICAS adhesion↔binder | #271 Hong(PTFE void↓6.4%p), #264(cross-link modulus), #17 Song(Perzyna-Ludwick 점소성), #20 Bak(binder-z adhesion), #08 Bielefeld2020(binder σ-block), #285(spring-back) | mpm3d_compaction `--coh`(현 상수) | ⛔ | binder modulus(MPa)는 SE E_eff(1.53GPa)와 별개 항; 비단조 cap(과가교↓) |
| A4 | **E4 `se_coating_interface` carbon 옵션** — additives.py가 carbon을 bulk 간극에만 seed → CAM-표면-film carbon(SuperP coating 차단) 표현 못 함 | #19 Kim(SE-coating SuperP σ_e 3자리 붕괴) | additives.py (seed 위치) | ⛔ | 현 SuperP>VGCF는 bulk-corner 한정; coating regime은 VGCF승 |
| A5 | **E2 dispersion CV** — 첨가제/입자 분산 불균일도 | #284 SiOx | additives.py / 합성 | ⛔ | |
| A6 | **pore-τ DiffuDict (유효-D voxel)** — pore network 유효확산 | #281 A3D | voxel_conductivity (D 채널) | ⛔ | |
| A7 | **Phase-5 graded-z** — z-band별 porosity(#286)+carbon:binder(#20) 2축 | #286 Yoo, #20 Bak | extract_2d_microstructure K=8 z-band | ⛔ | optimum 재료의존(#286 gradient vs #20 uniform) → 둘 다 비교 |

## B. 검증/교차대조 (모델 값 확인·정당화 — 적용은 선택)

| # | 항목 | 출처 | 상태 | 노트 |
|---|---|---|---|---|
| B1 | **σ_ionic 절대 검증점 채택** — exp σ_eff,ion을 우리 σ_ionic anchor로 (vol% CAM:SE→φ_SE 매핑 후) | Bazzoun 2026(EIS 0.065-0.137), Minnmann 2021(0.17@42vol%), Oh#266(0.034-0.055), Hong#271 | ⛔ | 우리가 부족했던 외부 실험앵커 |
| B2 | **RNM(constriction) vs 우리 Stage-E(plastic-area)** 같은 구조서 대조 → Stage-E 기여 정량 | Bazzoun 2026, Bielefeld 2020(σ_eff continuum, constriction 없음) | ⛔ | Bielefeld 2020 high-CAM서 RNM 과소예측 → Stage-E가 보정? |
| B3 | **percolation 지수 정당화** — 우리 √(φ−φc)·CN² 등 vs β=0.41(3D site), p_c=7.83·ln d+36.67 | Bielefeld 2019 | ⛔ | 우리 exponents의 universality-class 근거 |
| B4 | **multi-contact coupling** = 18× softening 대안(밀집 과강성) 비교연구 | Varkey 2026 | ⛔ | 우리 경험적 softening의 물리적 대안 |
| B5 | **σ_grain 이중계상 재점검** — pellet(1.02-1.6) vs Cronau single(3.0) + Cronau(r_SE) GB factor | Bazzoun, Cronau, Minnmann(bulk 1.6) | ⛔ | bulk spread {3.0/2.19/1.6/1.02} |
| B6 | **operating-pressure σ-degradation** (void-vs-P 시간축) — 정적 모델에 없는 축 | Lee 2025 co-rolling, Doux 2020 | ⛔ | future: P sweep→void→σ↓ |

## C. paper-build (refs.bib / main.tex 정정 — 출판 전)

| # | 항목 | 상태 |
|---|---|---|
| C1 | refs.bib `@Minnmann2021bottleneck`(040537) **추가됨** ✅ — anchor 인용을 그쪽으로 배선(main.tex) | 🔶 |
| C2 | main.tex Sakuda "87%@300" → ">90%@>350 stated; ~87%@~300 digitized trend; glass≠LPSCl" softening | ⛔ |
| C3 | refs.bib `@Wang2022`(κ) = phantom → 일반 GB-phonon refs로 교체 + main.tex κ 인용 정정 | ⛔ |
| C4 | Cronau 라벨 정정(연도 2021, Br not Cl, GB-pellet not single-crystal) | ⛔ |

## 진행 메모
- 2026-06-26 작성.  논문 digest batch(Trevisanello/Cronau/Minnmann/Doux/Sakuda/co-rolling/Bielefeld19+20 등)
  완료 → **적용은 이 backlog가 추적**.  사용자 plan대로 논문작업 종료 후 A1(σ_e 방향)부터 진행.
- A2(wallP 조건부)는 자체 작업으로 거의 완료(trust test만).  나머지 A3-A7/B/C는 미착수.
