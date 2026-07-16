---
title: "SDCP 종합 정리 — 오비탈 · 작용기 · DFT (마스터)"
tags: [project/sdcp-linio2, results, orbitals, doping, dft, binder]
date: 2026-07-16
status: phaseB-4of5-done_verdict-imminent
supersedes-headline-of: sdcp_linio2_binding_report.md (2026-06-01, UMA 시대)
---

# SDCP 종합 정리 (2026-07-16) — 오비탈 · 작용기 · DFT

> [!success] 지금까지의 헤드라인 4개
> 1. **폴라론 백본화 크로스오버**: 도핑 스핀의 백본 π 지분이 n=1 35% → n=2 32.6% → n=3(내부) **50.1%** — 사슬이 자랄수록 hole이 SO₃ 라디칼에서 백본 π로 이동.
> 2. **폴라론은 사슬 내부를 선호**: E(mid) − E(end) = **−70.9 meV** → 실제 고분자에서 polaron은 사슬 끝을 피해 앉는다.
> 3. **자기도핑은 사슬이 길수록 쉬워진다**: H-제거 비용 dimer 대비 trimer-mid **−213 meV**.
> 4. **DFT 앵커링(잠정)**: LiNiO₂(104) 위 doped SDCP E_bind = **−1.52 eV** (Phase-B DFT+U; neutral 수렴 임박 → Δ VERDICT 곧 확정).

## 0. 문서 계보
- 6월 보고서 `sdcp_linio2_binding_report.md` = Phase A–C **UMA(MLIP)** 시대. 거기의 절대값(-18.2/-6.3 eV, v1 분자 세대)은 이후 v7c Phase-A 재실행으로 대체(-5.20/-2.73, db/properties/sdcp_linio2_binding_phaseA.csv)됐고, 어느 쪽이든 **사이트 랭킹·방향성 지표**였으며, 절대 스케일은 본 문서의 DFT 값으로 대체 중.
- 본 문서 = 오비탈(n-시리즈) + 도핑 부기 + 작용기 + Phase-B DFT + PTFE 벤치마크의 단일 최신 정리.

## 1. 시스템 한 장
- **SDCP** = self-doped conducting polymer (PEDOT-S 계열): thiophene 고리 + 알킬 스페이서 + 말단 **SO₃H** (자기도핑 시 SO₃⁻).
- v7c 구조 세대. 조성/원자수:
  | n | neutral | doped(라디칼, 알짜중성 doublet) |
  |---|---|---|
  | 1 (monomer) | C₁₁H₁₆O₅S₂, 34 at | C₁₁H₁₅O₅S₂•, 33 at |
  | 2 (dimer, α–α, 이면각 60°) | 68 at, E=−3351.335544 Eh | 67 at, E=−3350.681182 Eh |
  | 3 (trimer, 이면각 130°) | 101 at, E=−5026.422091 Eh | mid 100 at −5025.775556 / end 100 at −5025.772950 Eh |
- 분자 방법: **ORCA r2SCAN-3c Opt** (desktop WSL, 전부 bfgs 수렴), Loewdin 그룹 스핀 분해.
- 표면 방법: **QE PBE+U(AFM, U_Ni=6.2) LiNiO₂(104)** 96원자 슬랩, gabia A6000 (Phase-B).

## 2. 도핑 부기 — 가장 많이 헷갈렸던 것들의 최종 정리
- 산화적 축합/산화제 도핑 = **분자 전체 HOMO에서 전자 1개 제거 + SO₃H의 산성 H 제거**. "thiophene P오비탈 5개에 전자 6개에서 하나 잃음" 그림은 국소 오해 — 전자는 특정 고리가 아니라 **전분자 HOMO**에서 빠진다.
- 떼어진 H의 행선지: 산화제/짝염기 (H⁺ + e⁻ 부기). 검산: E(neutral)−E(doped) = 0.654 Eh ≈ H 원자(0.500 Eh) + O–H BDE(~4.2 eV) ✓.
- **중성 사슬에는 캐리어가 없다.** 도핑이 만든 hole(=SOMO)이 캐리어다. SO₃⁻는 그 hole의 짝(고정 음이온)으로 사슬에 붙어 있어 "자기"도핑.
- 교육 그림: `sdcp_monomer_MO_scheme.png` (모노머 전체 MO 사다리 + HOMO에서 전자 빠지는 위치).

## 3. 오비탈/스핀 n-시리즈 (핵심 데이터)
도핑 상태(doublet)의 Loewdin 스핀 분포, SO₃(라디칼) : 백본 π 지분:

| n | 도핑 자리 | SO₃ % | 백본 π % | 고리별 분해 |
|---|---|---|---|---|
| 1 | – | ~65 | ~35 | O 론페어 우세 |
| 2 | A-ring | 62.3 | 32.6 | A 17.4 / B 15.2 — **고리 2개에 거의 균등**(비편재 시작) |
| 3 | end(A) | 54.6 | 39.8 | 이웃 B 15.3 > 호스트 A 13.9 > 원거리 C 10.6 |
| 3 | **mid(B)** | 42.3 | **50.1** | A 14.0 / B 21.3 / C 14.9 — 대칭 날개 |

- **π-허브 효과**: 컨쥬게이션 이웃이 둘인 가운데 고리가 스핀을 우선 수용 (end-doping에서 이웃>호스트 역전; mid-doping에서 B가 최대). 단순 거리감쇠는 허브 너머에서만 성립.
- **크로스오버**: n=3 내부 도핑에서 백본 지분이 50%를 넘음 → 폴라론이 "SO₃ 라디칼"에서 "백본 π 폴라론"으로 성격 전환. n↑ 외삽 시 백본 지배 예상.
- **자리 선호**: E(mid)−E(end) = −2.606 mEh = **−70.9 meV** → 내부 자리 선호.
- **자기도핑 용이화**: H-제거 비용 0.65436(dimer) → 0.64914(trimer-end, −142 meV) → 0.64654 Eh(trimer-mid, −213 meV) — 비편재 안정화 때문.

## 4. 작용기별 역할 정리
| 작용기 | 역할 | 근거 |
|---|---|---|
| **SO₃⁻** (탈양성자) | 자기도핑 소스 + **표면 앵커** | 도핑 스핀의 주 서식지(n 작을 때); Phase-A 스캔의 결합 그룹 |
| **SO₃H** (중성) | 수소결합형 얕은 흡착 | UMA neutral −2.73 eV (v7c Phase-A 정본; 방향성) |
| thiophene π 백본 | 전도 경로·폴라론 수용체 | n-시리즈 백본 지분 성장, π-허브 |
| 알킬 스페이서 | 측쇄-백본 전자 절연 | 스핀 "rest" 5.0–7.6%뿐 |

## 5. LiNiO₂(104) 앵커링 — UMA(6월) → DFT(7월)
### Phase A–C (UMA oc20, 2026-06-01 보고서)
- v7c 정본(phaseA csv): doped chelation_r90 **−5.196 eV** (CHAMPION) vs neutral chelation_r0 **−2.733 eV** → Δ 2.46 eV, "자기도핑이 앵커링 강화" 방향성. (v1 세대의 −18.2/−6.3은 구버전 — 6월 보고서 참조용.)
- 주의: omat은 슬랩 붕괴 → oc20 + unrelaxed 슬랩 사용; **절대값은 과대**(doped −5.20 vs DFT −1.52 ≈ 3.4×) — 랭킹용으로만 인용.

### Phase B (QE PBE+U, gabia, 2026-07-13~) — 진행 4/5
| job | E (Ry) | 상태 |
|---|---|---|
| slab | −10563.22819091 | PLATEAU(±0.10 eV; 계통오차는 Δ에서 부분상쇄) |
| mol_doped | −518.39271245 | 수렴 |
| mol_neutral | −519.68310300 | 수렴 |
| complex_doped | −11081.73293860 | DONE (PLATEAU ±0.004 Ry) |
| complex_neutral | (iter 272, acc 7.6e-6 — 수렴 임박) | 러닝 |

- **E_bind(doped, DFT) = complex − slab − mol = −0.11204 Ry = −1.524 eV** (잠정; favorable).
- **★VERDICT = E_bind(doped) − E_bind(neutral)** — complex_neutral 완료 시 watch가 자동 계산. 질문 스케일(UMA Δ 기준 ~2.4 eV) 대비 슬랩 오차 ±0.10 eV → S/N 양호.

## 6. PTFE 벤치마크 (비교군 — "SDCP가 돋보여야")
- 목적: 기존 vdW 바인더 PTFE 대비 SDCP 결합 우위의 정량.
- fragment 확정: **C₄F₈H₂** (문헌 'PTFE dimer' 표기 스타일; H-말단 인공성 인지하고 사용) 대표 + **C₁₀F₂₂**(CF₃-capped parity) 백업. 둘 다 r2SCAN-3c 이완 완료, 나선 이면각 ~162° 재현.
- step 2 (Phase-B 종료 후 gabia): mol γ-box 2종 + Phase-B 슬랩 위 complex + **D3 후보정 일괄 적용** — Phase-B 레시피에 vdw_corr 없음을 확인했고 PTFE는 vdW 결합이라 필수. SDCP 세트에도 같은 D3를 적용해 공정 비교.

## 7. 산출물 인덱스 (repo)
- 구조: `db/structures/sdcp_v7c_dimer_{neutral,doped}.xyz`, `sdcp_v7c_trimer_{neutral,doped_mid,doped_end}.xyz`, `ptfe_dimer_c4h2f8_r2scan3c.xyz`, `ptfe_c10f22_r2scan3c.xyz`
- 데이터: `db/properties/sdcp_v7c_dimer_spin.csv`, `sdcp_v7c_trimer_spin.csv`(n-시리즈 주석 포함), `sdcp_v7c_phaseB_energies.csv`, `sdcp_linio2_binding_phaseA.csv`, `sdcp_v7c_li_binding.csv`, `sdcp_v7c_surface_hbond_screens.csv`
- 도구: `tools/sdcp/`(v7c 빌더·trimer 빌더·PTFE 빌더·phaseB 러너·gabia watch), `tools/sdcp_binding/`(6월 UMA 스택)
- 그림: MO scheme(스크래치), Phase-A heatmap 3종(6월)

## 8. 남은 일
1. **complex_neutral 수렴 → ★VERDICT 등록** (phaseB csv·본 문서 헤드라인 확정)
2. PTFE step 2 + D3 패스 (SDCP/PTFE 공정 비교)
3. (옵션) n=4 외삽으로 백본 지분 포화 확인 / polaron 준위 도식
