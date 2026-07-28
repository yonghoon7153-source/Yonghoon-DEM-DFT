# Highly reliable and large-scale simulations of promising argyrodite solid-state electrolytes using a machine-learned moment tensor potential — Kim et al. (Nano Energy 2024)

> slug `kim2024_mtp_argyrodite_disorder_gb` · DOI `10.1016/j.nanoen.2024.109436` · type `MLIP(MTP)-MD + DFT/AIMD` · PDF 본문 `82ea256b/9a0b0c9b-35._Highlyential.pdf` + SI `82ea256b/cacf7ea8-35._Sup_Hiential.pdf` (**inbox #35 쌍**, 본문 10 pp + SI 28 pp 전부 정독) · digested `2026-07-28` · status ✅
> elements: Li, P, S, Cl, Br, I
> methods: DFT, AIMD, MD, MLIP
> **저자**: Ji Hoon Kim (성균관대 화공), Byeongsun Jun·Yong Jun Jang·Sun Ho Choi·Seong Hyeon Choi·Sung Man Cho·Yong-Gu Kim (**현대자동차**), **Byung-Hyun Kim (한양대 ERICA 안산, 응용화학)**, **Sang Uck Lee*** (성균관대) — Nano Energy 124 (2024) 109436 (2023-09-29 접수, 2024-03-02 온라인). ⚠ 한양대 공저자가 있으나 **[우리 그룹] 아님**(ERICA 응용화학·이상억 그룹 라인).

---

## 0. 이 digest를 읽는 법
이 논문은 **"argyrodite의 6가지 4a/4c 음이온 무질서 배열을 전부 AIMD로 돌리는 건 너무 비싸다 → MTP(moment tensor potential) MLIP로 대체하되, 어느 DFT functional로 학습해야 맞는 물리가 나오나"** 를 판정하고(답: **optB88-vdw**), 그 MTP로 (1) 6배열 전수 σ, (2) 27셀 Boltzmann-가중 **"random structure"** 대형셀 σ, (3) **>13,860원자 Σ5[100](021) 입계(GB)** MD까지 올라간다. 우리 캠페인과의 접점은 세 개: **무질서→σ 지배**(우리 disorder_ensemble·comp1→modelc), **MD σ의 방법 의존성**(우리 UMA 규율), **GB=σ 병목**(우리가 못 보는 축).
> ⚠ 표기: 이 논문은 halide/S²⁻ 자리를 **4a/4c**로 부른다 — 우리 다른 digest([Bai]·[Liu] 등)의 **4a/4d**와 같은 자리(F-43m 원점 선택 차이). "X% = 4c의 X⁻ 점유율".

## 1. 한 줄 요약
optB88-vdw로 학습한 MTP만이 AIMD·실험의 site-disorder 의존성(ordered 느림/disordered 빠름)을 재현하며(PBE·PBE-D3(BJ) 학습 MTP는 실패), 이 MTP로 6배열 무질서를 담은 3×3×3 "random structure"에서 **σ80% 2.3 mS/cm(실험 2.3–2.5 일치; 원값 σ100%=11.5)** 를 얻고, **PS₄ 회전·진동이 Li 확산을 돕고**(고정 시 disordered −50%), **GB는 Li이 정전기적으로 축적**되어 D를 **0.3×**(5.4e-8 vs bulk 1.8e-7 cm²/s @350 K)로 깎으며 그 영향이 계면에서 **10–20 Å**까지 미침을 보였다.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 시스템 | Li₆PS₅X (X = Cl, Br, I) — 6가지 4a/4c site-disorder 배열 + random supercell + Σ5[100](021) GB |
| 질문 | ① AIMD의 한계(≈10 Å·100 ps·고온)를 MTP로 넘을 수 있나 ② 어떤 functional 학습이 맞나 ③ 무질서 전수 대신 random 대형셀 하나로 되나 ④ GB가 σ를 왜 깎나 |
| 선행(같은 그룹) | ref [36] Jun & S.U. Lee JMCA 2022: 6배열 + 열역학·동역학 가중 σbulk 방법 + ion-cage size descriptor (AIMD 기반) — 이 논문은 그 방법의 **MTP 가속판** |
| 방법 계보 | MTP 자체는 Shapeev 2016 + MLIP 패키지; "simulated vs experimental σ gap" 프레임은 Ong 그룹 [37] Qi 2021 Mater. Today Phys. |
| 도구 스택 | VASP 5.4.4 + LAMMPS + MLIP/MAML + pymatgen(+GrainBoundaryGenerator) + enumlib + OVITO + **CCpy**(github.com/91bsjun/CCpy, 공저자 Jun의 자동화) |

## 3. 구조 모델 & 무질서 처리 ★
- **출처**: ICSD/Rietveld 직접 인용이 아니라 **enumlib로 생성한 "fully occupied" 6배열** (부분점유 불가한 DFT용 정수 점유 모델). Li 자리 배열 enumlib 생성 → 단위셀 내 단일음이온 8개(S²⁻ 4 + X⁻ 4)를 4a/4c에 배치.
- **6배열** (X⁻@4c 점유율·공간군): **0% (F-43m)** = X 전부 4a / **25% (R3m)** / **50% (P2₁22)** / **50% (P2mm)** (같은 50%인데 배치 다른 2종) / **75% (R3m)** / **100% (F-43m)** = X 전부 4c. 0%·100% = "ordered", 25/50/75% = "disordered".
- **무질서 처리 분류: enumerate(6 특성배열) + Boltzmann-가중 random supercell** — SQS 아님, 단일배열 아님. 3×3×3(27 unit cell)에 각 배열을 Pi(E)∝exp(−E_rel/kT) 비례로 **개수 할당**(Eq. S12; E_rel은 meV/atom을 kT(300 K)=25.85 meV와 직접 비교 — 차원상 heuristic) 후 무작위 배치.
- **Pi(E)와 셀 할당** (Table S2): Cl → 0%:3 / 25%:7 / 50%(P2₁22):7 / 50%(P2mm):5 / 75%:5 / 100%:0. Br → 4/11/7/2/3/0. I → **14**/6/3/2/2/0 (I는 0%=all-4a가 최안정 E_rel=0 → random에도 ordered 지배).
- **실험 점유율**(SI 인용, Rayavarapu 2012): 4a:4c = Cl 3:7, Br 6:4, I 1:0. **우리 산수**로 random 셀의 평균 4c-X 점유율 = Cl **42.6%** / Br 35.2% / I 20.4% → **Br은 실험(40%)과 근접, Cl은 실험(70%) 대비 과소, I는 실험(0%) 대비 과대** — 논문은 이 비교를 하지 않음(§12).
- **E_rel** (meV/atom, DFT-PBE): Cl 23/4/**0**/11/13/**206** · Br 23/**0**/11/39/33/**251** · I **0**/22/37/47/49/**284** — **100%(전부 4c)는 세 조성 모두 극도로 불안정**; I만 0%(전부 4a)가 최안정 = [Rao] 2025의 "I 4a 강선호"와 정합.
- **supercell·nat**: 단위셀 52원자(Li₂₄P₄S₂₀X₄) → MD용 3×3×3 = **1404원자**(본문 표기 ">1000 s atoms"는 오타, thousands). GB 학습모델 ~500원자(a 10.2795/b 22.9857/c 45.9713 Å), GB 프로덕션 **>13,860원자**(a 30/b 68/c 135 Å).
- Fig S1 구조 서술: PS₄=4b, Li=48h+24g cage("Li fully occupies 24g and partially 48h"라 쓰였는데 통상 서술(48h 주점유)과 뒤집힌 표현 — 원문 그대로 기록), 단일음이온=4a/4c.

## 4. 핵심 수치 (전량)

### 4.1 Li₆PS₅Cl 6배열 (Table 1) — E_rel(meV/atom) / Ea(meV) / σRT(mS/cm)
| X⁻@4c | AIMD_PBE | MTP_PBE | MTP_PBE-D3(BJ) | MTP_optB88-vdw |
|---|---|---|---|---|
| 0% (F-43m) | 23 / 452 / 0.0033 | 23 / 529 / 0.007 | 23 / 997 / "Too low" | 23 / 502 / 0.008 |
| 25% (R3m) | 4 / 193 / 9.1 | 4 / 219 / 25.1 | 4 / 286 / 3.6 | 4 / 220 / **19.2** |
| 50% (P2₁22) | 0 / 160 / 23.3 | 0 / 217 / 34.2 | 0 / 290 / 2.7 | 0 / 256 / 12.7 |
| 50% (P2mm) | 11 / 151 / **37.1** | 11 / 209 / **41.9** | 11 / 290 / 4.4 | 11 / 246 / 15.7 |
| 75% (R3m) | 13 / 184 / 12.1 | 13 / 239 / 23.4 | 13 / 337 / 1.9 | 13 / 250 / 13.3 |
| 100% (F-43m) | 206 / 339 / 0.12 | 206 / 249 / **3.7 ⚠** | 206 / 271 / **3.7 ⚠** | 206 / 406 / 0.01 |
| **σ80%bulk** | **3.82** | 4.19 | 0.55 | **2.46** (σExp 2.3–2.5) |

🔑 판독: ① **ordered(0/100%) ↔ disordered(25–75%) 사이 σ 3–4자릿수 갭** (Ea 340–530 vs 150–260 meV). ② MTP_PBE·PBE-D3는 **100% ordered를 비정상적으로 빠르게**(3.7 mS/cm) 내놓아 무질서 의존성 재현 실패; PBE-D3는 전반적으로 Ea 과대(~290–340). ③ optB88-vdw만 AIMD 순서·실험 σ80%를 동시 재현 → **선택**.

### 4.2 Li₆PS₅Br / Li₆PS₅I 6배열 (Table S1; AIMD_PBE vs MTP_optB88-vdw)
| X⁻@4c | Br AIMD | Br MTP | I AIMD | I MTP |
|---|---|---|---|---|
| 0% | 23 / 557 / 9.8e-5 | 23 / 467 / 0.01 | 0 / 695 / 6.9e-7 | 0 / 695 / 1e-6 |
| 25% | 0 / 219 / 3.2 | 0 / 219 / 12.9 | 22 / 255 / 1.0 | 22 / 255 / 8.3 |
| 50% (P2₁22) | 11 / 194 / 8.5 | 11 / 288 / 7.7 | 37 / 202 / 6.1 | 37 / 202 / 15.6 |
| 50% (P2mm) | 39 / 196 / 10.5 | 39 / 256 / 12.4 | 47 / 227 / 3.4 | 47 / 227 / 17.8 |
| 75% | 33 / 188 / 10.4 | 33 / 300 / 5.7 | 49 / 221 / 3.4 | 49 / 221 / 7.1 |
| 100% | 251 / 401 / 1.7e-2 | 251 / 447 / 0.05 | 284 / 531 / 2.6e-4 | 284 / 531 / 0.001 |
| σ80% | 3.12 | 1.59 (exp 1.0) | 0.84 | 0.85 (exp 0.004) |

⚠ **I의 Ea 열이 AIMD와 MTP에서 6배열 전부 동일**(695/255/202/227/221/531) — σRT는 다른데 Ea만 복제된 표 오류 가능성 큼(§12).

### 4.3 Random structure (3×3×3, MTP_optB88-vdw; Table 2)
| 조성 | σ100%bulk (원값) | σ80%bulk (χc=0.8 보정) | σExp |
|---|---|---|---|
| Li₆PS₅Cl | **11.5** | **2.3** | 2.3–2.5 |
| Li₆PS₅Br | 8.8 | 1.8 | 1.0 |
| Li₆PS₅I | 2.6 | 0.5 | 0.004 (본문엔 0.002도 인용) |

- 보정식: **σ_exp = σ_calc · χc^7.14** (χc=결정화도; 문헌 σ 대부분 χc 70–80%에 대응한다는 자기들 회귀 [36]) → χc=0.8 채택.
- random의 Arrhenius(Fig 3b)는 **ordered와 disordered 사이, disordered 쪽에 근접**. I는 σ80% 0.5로 실험(0.004) 대비 큰데, I가 실제론 fully-ordered 선호라서 **ordered 배열의 σ80%=0.001이 실험 0.002에 더 가깝다**고 자체 해명.

### 4.4 PS₄ 회전/진동 기여 (600 K, 3×3×3, Fig S7–S8)
- S 궤적 추적: PS₄ **회전 + 열진동** 존재(disordered에서 더 큼).
- **PS₄ 고정 MD**: D600K(×10⁻⁶ cm²/s) ordered 2.1→1.8 (**−18%**), disordered 7.7→3.9 (**−50%**) → **음이온 동역학이 Li 확산을 실질 부양**, disordered가 더 민감; 단 고정해도 disordered(3.9) > ordered(1.8) 2배 유지 → **주인은 여전히 inter-cage 연결(배열)**, PS₄ 운동은 증폭기.

### 4.5 GB (Σ5[100](021), MTP_optB88-vdw + active learning)
| 항목 | 값 |
|---|---|
| GB 후보 안정성 γ_GB (Fig S9, figure-read) | **tilt Σ5[100](021) ≈1.35 J/m² 최저(선택)** < twist Σ3[110](110) ≈1.4 ≈ tilt Σ5[010](001) ≈1.45 < tilt Σ3[110](1-11) ≈1.5 < twist Σ5[100](100) ≈2.0 < twist Σ3[111](111) ≈3.1 — **tilt가 twist보다 안정** |
| 표면에너지 순서 (ref [84] 인용) | (111) < (021) < (001) < (011) |
| 프로덕션 셀 | random 기반, >13,860원자, NPT 350 K, 10 ns |
| **D(350 K)** | bulk **1.8×10⁻⁷** vs GB core **5.4×10⁻⁸ cm²/s (≈0.3×)** — 실험 보고(GB 저항) 방향 재현 |
| 공간 범위 | 10 Å 두께 bin으로 GB/Near_GB/Far_GB/Bulk 분해 → GB 영향 **10–20 Å** 침투(Far_GB에서 bulk 수렴) |
| 방향성 | 모든 축(a/b/c) D 감소 (Fig S11) |
| **Li 축적** | MD 진행하며 bulk→Far→Near→GB로 Li 순차 이동·축적(Fig 5d, 5 ns 색 변화); Li–Li RDF 첫 피크 10 ns에서 단축(Fig S13) |
| 시간 의존 | GB 구조의 bulk 영역 D: 100 ps **3.4e-7** → 10 ns **1.6e-7** (Table S3) — **짧은 MD는 D 2× 과대** |
| 기전 | GB 계면에 PS₄³⁻·S²⁻가 인접 배치 → **국소 강한 음전하 → 정전기적 Li 트랩** (실험의 cation vacancy 관측[65]과 연결) |
| 처방(제안) | **solid-electrolyte inductive effect**: 고산화수 원소 도핑 → S–Li 상호작용 약화·S 전하 감소 → GB Li 축적 억제 [86,87] |

## 5. DFT/계산 방법 ★
- **code**: VASP 5.4.4 (DFT/AIMD) + LAMMPS (MTP-MD). PAW.
- **functional**: 구조최적화 **PBE**; 학습 single-point는 **PBE vs PBE-D3(BJ) vs optB88-vdw 3종 비교** → optB88-vdw 채택.
- **k/ecut/수렴**: MP **2×2×2**(단위셀), ecut **500 eV**, 힘수렴 **0.04 eV/Å**(격자+내부 full relax; 다소 느슨).
- **훈련셋 구축**(Fig 1): ① 6배열 PBE 최적화 → ② ±5% 격자 strain(3구조) → ③ 각 배열·각 strain에 **AIMD NVT(Nosé-Hoover) 300/600/900/1200 K × 10 ps(2 fs)**, 궤적당 100 스냅샷 → 배열당 1200개, **총 7200 스냅샷** → ④ 3 functional로 single-point E/F.
- **MTP**: R_cut **5 Å**, lev_max **8** (최고정확은 6 Å/16이지만 **10× 비용**; lev 8=1일, 12=3.5일, 16=9일), 가중 E:F=**100:1**, train:valid=9:1. 최종 MAE(Fig S3): **Cl E 2.88 meV/atom·F 0.073 eV/Å**, Br 2.92/0.075, I 2.51/0.066 (그림 축 "meV/Å"는 eV/Å 오기; 본문 "0.02 eV/Å 미만" 주장과 불일치 — §12). 같은 조성이면 어떤 배열에도 동일 MTP 적용 가능.
- **MTP-MD(σ)**: 3×3×3(1404원자). **NVT 승온 100 ps(10 K 스텝) → NPT 10 ns** at 목표 T. **350–500 K, 25 K 간격 7개 온도 × 2회 반복**(ensemble avg; Fig 2 캡션은 350–700 K 표기 — §12). MSD→D(식 S5, 피팅창 미명시)→Arrhenius(식 S6)→**Nernst–Einstein(식 S7, Haven 보정 없음)** 으로 σRT(300 K 외삽).
- **AIMD 레퍼런스**: 600–1200 K(Fig 2a), 셀 크기 미명시(선행 [36] 프로토콜; ~10 Å·~100 ps 규모라고 서론에서 자인).
- **GB MTP(active learning)**: passive(위 7200, optB88) + **(021) surface 2구조(0%·50%)·±5% strain·AIMD 900/1200 K 10 ps → 1200 스냅샷** 추가 → active learning: **NPT 300/500/700/900 K, γ_select=5, γ_break=20**, 불확실 구조 선별→optB88 single-point→재학습 반복; E:F:S 가중 **100:1:0.01(본문) vs 100:1:0.001(Fig 4)** 표기 불일치. slab 진공 15 Å(Fig S10).
- **무질서 처리**: §3 (enumerate 6배열 + Boltzmann random supercell).

## 6. 결과 상세 (논문 순서)

### 6.1 MTP 검증 — functional이 물리를 가른다 (Table 1, Fig 2)
- 세 MTP 모두 회귀오차(MAE)는 훌륭하지만, **σ의 site-disorder 의존성은 optB88-vdw만 재현**: MTP_PBE·PBE-D3는 100% ordered에서 σ 3.7 mS/cm(비정상 고전도), PBE-D3는 σ80% 0.55로 과소.
- **σ80%bulk**: AIMD_PBE 3.82 / MTP_PBE 4.19 / MTP_PBE-D3 0.55 / **MTP_optB88 2.46** vs 실험 2.3–2.5 → optB88 채택. Br·I도 동일 검증(Table S1·Fig S5).
- 시사: **훈련 데이터의 functional(=PES의 vdW 처리)이 MLIP-MD σ의 자릿수를 바꾼다** — "MLIP σ 절대값은 방법 각인"의 정면 증거.

### 6.2 Random structure — 무질서 전수를 셀 하나로 (Fig 3, Table 2)
- 27셀에 6배열을 열역학 가중으로 섞은 "random structure"의 D(T)가 ordered/disordered 사이·disordered 근접 → **대표성 확인**. σ80%: Cl 2.3(실험 일치)·Br 1.8·I 0.5.
- 궤적(Fig 3c·S6): ordered = cage 고립(inter-cage 연결 없음, MSD 포화 "caged", Fig S4a), disordered/random = **inter-cage 연결 활성**(MSD 선형 "free", 10 ns에 ~200 Å²). I는 가장 국소화(σ 최저 정합).
- 결론: **배열 전수 계산 없이 random 셀 + σ80% 보정으로 신속 스크리닝 가능**.

### 6.3 PS₄ 동역학 (Fig S7–S8)
- 600 K에서 PS₄ 회전 관측 → **고정 시 D −18%(ordered)/−50%(disordered)** → 회전·진동이 Li 확산 보조(§4.4). 단 순위는 배열이 결정.

### 6.4 GB — Li 축적이 σ 지연의 기원 (Fig 4–5, S9–S13)
- 안정 GB 선정(tilt Σ5[100](021), γ≈1.35 J/m²) → active-learning MTP → >13,860원자·10 ns NPT.
- **D_GB=5.4e-8 vs bulk 1.8e-7 (0.3×)**, 영향권 10–20 Å, 전 방향 감소.
- 구조는 유지(PS₄·단일음이온 골격 보존; S²⁻/Cl⁻만 GB서 유동 — Fig S12) → 구조붕괴가 아니라 **정전기 트랩**: GB에 PS₄³⁻+S²⁻ 인접 → 음전하 웅덩이 → Li 순차 유입·축적(Fig 5d) → Li–Li 거리 단축(RDF) → D 추가 하락(100 ps 3.4e-7 → 10 ns 1.6e-7).
- 처방: **고산화수 도핑으로 S 전하↓(inductive effect)** → Li 트랩 완화 제안(계산으로 검증은 안 함).

## 7. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | MTP 개발 6단계 워크플로 + coordinate-space 훈련영역 개념도 | MLIP 훈련셋 설계(평형+strain+고온 AIMD 스냅샷) 표준 그림; 우리 UMA(사전학습)와 대비되는 "자체학습 MLIP" 파이프라인 |
| 2 | 6배열 Arrhenius D — (a) AIMD_PBE (b) MTP_PBE (c) MTP_PBE-D3 (d) MTP_optB88 | **functional별 실패양상 비교 그림** — 우리 "σ 절대값 방법 각인" 슬라이드에 인용 |
| 3 | (a) random 27셀 구성 (b) random vs ordered/disordered Arrhenius (c) Li 궤적 3종 | 무질서 대표셀 아이디어; 궤적 그림은 [GG]/[Liu] 확률밀도와 같은 문법 |
| 4 | GB용 MTP passive+active learning 워크플로 | active learning(γ_select/γ_break) 절차 — 우리가 MLIP 자체학습으로 갈 때 템플릿 |
| 5 | (a) GB 학습모델 (b) random GB >13,860원자 (c) **D vs GB거리**(10 Å bin) (d) **Li count 시간지도** | (c)(d)가 핵심 — "GB Li 축적" 정량화 방식(영역분해 MSD + 정규화 Li 수) 차용 가능 |
| S1 | 구조 + 6배열 도해 | 4a/4c(=우리 4a/4d) 배열 시각화 |
| S2 | 하이퍼파라미터(R_cut·lev_max vs MAE·비용) | MLIP 비용-정확도 트레이드오프 수치(1일/3.5일/9일) |
| S3 | MTP vs DFT E/F 회귀(조성별 MAE) | MAE 보고 관례(에너지 meV/atom·힘 eV/Å) — 축 라벨 오기 반면교사 |
| S4 | MSD 350 K: ordered 포화("caged") vs disordered 선형("free") | **우리 disorder_ensemble의 'ordered frozen' 관측과 동일 그림** |
| S5–S6 | Br·I Arrhenius + 궤적 | 할라이드 일반화 |
| S7–S8 | S 궤적(PS₄ 회전) + PS₄ 고정 D 비교 | **paddle-wheel류 분석의 간단 구현**(궤적+구속 MD) — 우리 UMA 궤적에 그대로 적용 가능 |
| S9 | GB 6종 γ_GB (tilt vs twist) | GB 모델 선정 근거; γ 정의식 |
| S10 | (021) slab (진공 15 Å) | 표면 훈련셋 |
| S11 | GB vs bulk MSD·방향별 D | 영역분해 D 산출법 |
| S12 | 원소별 궤적 at GB | "구조 유지 + Li만 제한" 판별법 |
| S13 | Li–Li RDF 100 ps vs 10 ns | **축적의 RDF 시그니처**(첫 피크 단축) |

## 8. Post-processing ★
- **MSD→D→Arrhenius→NE σ**: D=MSD/(2d·t)(식 S5), ln D vs 1/T(식 S6), σ_T=ρz²F²D_T/(RT)(식 S7, **Haven=1 암묵**). 300 K는 외삽.
- **σbulk 가중평균**: P_i = P_i(E)·P_i(σ), P_i(E)∝exp(−ΔE/kT), **P_i(σ)∝exp(−Δσ/kT)** (σ를 Boltzmann 인자에 넣는 heuristic — 차원 무의미, §12) → σbulk=Σ P_i σ_i (식 S8–S10).
- **결정화도 보정**: σ_exp=σ_calc·χc^7.14, χc=0.8 → "σ80%" (자기들 선행 회귀; 지수 7.14는 경험값).
- **random supercell 구성**: 자리수 할당식 S12 (P_i(E)·27, 반올림 보정).
- **궤적 분석**: OVITO 시각화, Li/S/P/Cl 궤적 겹치기(사이트 점유 시각화), **S 궤적으로 PS₄ 회전 판별**, **PS₄ 고정(constrained) MD**로 기여 정량.
- **GB 분석**: 10 Å bin 영역분해 MSD/D, 정규화 Li count(공간×시간 열지도), Li–Li RDF(축적), γ_GB=(E_GB−n_GB·E_bulk)/(2A_GB).
- **도구**: pymatgen(스냅샷·GrainBoundaryGenerator), MLIP+MAML(학습), enumlib(배열), CCpy(작업관리).

## 9. 우리 DFT/MD 대비 (comp1/modelc) → `../our_dft_baseline.md`, `db/properties/li_transport.json`
| 항목 | 이 논문 (MTP_optB88 기준) | 우리 (UMA-s-1p1 MLIP-MD) | 판정 / 이유 |
|---|---|---|---|
| 무질서→σ·Ea 방향 | disordered Ea 151–256 meV·σ 13–42 vs ordered 339–529 meV·σ ≤0.12 (3–4자릿수) | comp1(준질서) 0.253 → modelc(Cl-rich·anti-site) 0.224 eV·D 2.6×; **disorder_ensemble: disordered 0.177±0.027 eV, ordered는 600–800 K frozen**(Ea 1.17=저T 표본화 artifact) | **✓✓ 방향 완전 일치** — "무질서=빠름, 질서=사실상 부도체". 그들의 ordered "caged MSD"(Fig S4a)가 우리 frozen 관측의 10 ns 확장판 |
| 엄밀-ordered Ea 절대값 | 0%: AIMD 452 / MTP 502 meV (10 ns 표본화로 유한값 확보) | comp1 4fu(자연셀·질서) **253 meV** | **✗ 2× 갭 = 방법 각인**: UMA의 D 과대(3–5×) + 우리 고온창(600–1000 K) vs 그들 350–500(700) K + 셀·배열 차이. **주의**: 우리 0.253은 "실험 LPSCl(내재 무질서 60–70%)"과 맞는 값이지 "모델 완전질서"값이 아님 — 이 논문이 그 구분을 정량화해 줌 |
| 절대 σ(300 K, bulk) | random σ100% **11.5** mS/cm → χ^7.14 보정 2.3 | modelc σ_NE ~14 mS/cm(H=1, 절대값 인용 금지 규율) | **같은 병(원값 4–5× 과대), 다른 약**: 그들=경험적 결정화도 보정, 우리=절대값 불인용+비율만. χ^7.14는 회귀식이라 이식 금지 |
| functional 의존성 | 같은 데이터, functional만 바꿔 σ80% **4.19/0.55/2.46**(PBE/D3/optB88) | UMA(omat)로 통일, 절대 σ 3–5× 과대 명시 | **✓ 우리 규율의 외부 증거** — "MLIP-MD σ는 훈련 PES가 각인" (우리 'σ 절대값 금지·Ea/비율만' 정당화) |
| Ea(disordered, 방법간) | 151–256 meV (배열 따라) | modelc 224 · disorder-ens 177±27 meV | **✓ 같은 범위** — Ea는 σ보다 강건(양쪽 공통 결론) |
| PS₄ 회전 기여 | 고정 시 D −50%(disordered)/−18%(ordered) | framework-immobile 확인은 **병진**만(D_framework≈D_Li/40–60); 회전은 미분석 | **○ 상보** — 모순 아님(회전≠병진). 우리 UMA 궤적에 S-궤적/PS₄ 각도 분석 추가하면 같은 검증 가능(도구 아이디어) |
| GB | D_GB 0.3×·10–20 Å·Li 정전기 축적·처방=고산화수 도핑(S 전하↓) | **GB 계산 없음**(bulk 전용) — [KimICCF] "σ 병목=미세구조" 실험 서사와 정합 | **✗ 우리 공백 축** — 단 처방(고산화수→S 전하↓)은 우리 cascade의 inductive-effect 언어와 연결 |
| 무질서 처리 방식 | enumerate 6배열 + Boltzmann random supercell(27셀) | 단일배열(comp1 4fu/modelc 5fu) + 별도 disorder_ensemble(3 level×configs) | 철학 유사(전수 아닌 대표배열), 그들이 가중평균·대형셀로 한 단계 위; SQS는 양쪽 다 아님 |
| NE/Haven | Haven=1 암묵 | Haven=1 명시(+H_R<1이면 진짜 σ 더 큼 caveat) | 동일 관례, 우리 문서화가 더 정직 |
| ⚠ Schlem 앵커 관련 | (Schlem 2020 아님 — 이 논문은 그 위시리스트와 별개) | li_transport.json이 "comp1 0.2532 = Schlem ordered 0.25 EXACT" 앵커 유지 중 | 이 논문 기준 **모델 완전질서 Ea는 0.45–0.53 eV** → "Schlem ordered 0.25"는 완전질서 모델값일 수 없고 실험 LPSCl(내재 무질서)값일 가능성 — **Schlem 원문 digest 필요(위시리스트 유지)** |

## 10. 적용 인사이트
1. **"σ 절대값은 방법 각인" 슬라이드의 정면 증거 확보**: 같은 7200 스냅샷에서 functional만 바꿔 σ80%가 0.55↔4.19로 8배 갈림(Table 1) — 우리 UMA 절대 σ 불인용 규율을 외부 논문으로 방어.
2. **ordered vs disordered 이분법 정량화**: 우리 disorder_ensemble(frozen ordered / 0.177 disordered)이 이 논문의 6배열 전수(0.34–0.53 vs 0.15–0.26 eV)와 같은 그림 — 우리 결과 서술 시 "Kim 2024 MTP 전수계산과 방향 일치"로 인용 가능. 또한 **comp1 0.253을 '완전질서 모델값'처럼 쓰지 말 것**(완전질서는 0.45+).
3. **PS₄ 회전 분석 차용**: S-궤적 시각화 + PS₄-고정 MD 두 개면 됨 — 우리 UMA 600 K 궤적(이미 보유)에 그대로 적용해 "회전 기여 −X%"를 우리 수치로 만들 수 있음(rotation≠translation이므로 framework-immobile과 별개 축).
4. **GB 축은 우리 공백**: >10⁴원자 GB는 UMA로도 비싸지만 가능 범위 — 하되 이 논문의 결론(정전기 Li 트랩, 10–20 Å)과 처방(고산화수 도핑=S 전하↓)이 이미 우리 cascade 언어(ICOHP·Bader 전하)와 접속됨. GB 안 하더라도 "우리 도핑이 GB Li-축적 완화에도 유리할 수 있다"는 문헌 근거로 인용.
5. **σ80%(χ^7.14) 같은 경험 보정은 도입하지 말 것** — 우리는 비율·Ea만 인용하는 편이 더 방어적. 대신 "계산-실험 gap의 원인 분해(결정화도·GB·MLIP 과대)" 논의에 이 논문 인용.
6. **random supercell(열역학 가중) 아이디어**: 우리 modelc 후속(무질서 민감도)에서 SQS 대신 "가중 배열 혼합 대형셀"이 현실적 대안 — 단 가중이 0 K E_rel 기반이라 실험 점유율과 어긋날 수 있음(§12 Cl 43% vs 70%)을 명시하고 쓸 것.

## 11. 인용 가능 문장 (deck/paper용)
- "Kim et al. (Nano Energy 2024) showed with moment-tensor-potential MD that strictly anion-ordered Li₆PS₅Cl is essentially non-conducting (Ea 0.45–0.5 eV, σRT ≤0.01 mS/cm) while 4a/4c-disordered arrangements reach 13–42 mS/cm with Ea 0.15–0.26 eV — the same ordered-frozen vs disordered-fast dichotomy we observe in our disorder-ensemble MLIP-MD."
- "The same training snapshots fitted at PBE, PBE-D3(BJ), and optB88-vdW levels give bulk conductivities differing by ~8× (0.55–4.19 mS/cm), underscoring that absolute MLIP-MD conductivities are imprinted by the training functional; we therefore quote only activation energies and ratios."
- "MTP-MD of a >13,000-atom Σ5[100](021) grain boundary shows Li⁺ accumulating electrostatically at the boundary (D_GB ≈ 0.3 × D_bulk, affected zone 10–20 Å), supporting the view that device-level σ is limited by microstructure rather than bulk chemistry."

## 12. 주의/한계 (critical)
- **P_i(σ)∝exp(−Δσ/kT)**: 전도도를 Boltzmann 인자에 넣는 차원 무의미 heuristic — σbulk 가중은 "그럴듯한 내삽"이지 통계역학 아님. σ80%도 경험 회귀(χ^7.14). **수치 이식 금지, 개념만**.
- **P_i(E)도 meV/atom을 kT와 직접 비교**(셀 크기 임의성) — 열역학 가중의 근거 약함. 그 결과 random 셀의 4c-Cl 평균 점유 **42.6% vs 실험 70%**(Rayavarapu) 불일치를 논문이 점검하지 않음(Br만 우연히 근접).
- **힘 정확도 표기 혼란**: 본문 "MAE <10 meV/atom·<0.02 eV/Å" vs Fig S3 실측 0.066–0.075 (축 라벨은 meV/Å 오기) — 실제 힘 MAE는 0.07 eV/Å급으로 봐야 함(그래도 MLIP 통상 수준). Fig S2 축도 동일 오기. GB 가중치도 본문 0.01 vs Fig 4 0.001 불일치.
- **Table S1 I조성 Ea 복제 의심**: AIMD와 MTP의 Ea가 6배열 전부 동일 — 편집 오류 가능성. I의 MTP Ea는 인용하지 말 것.
- **온도창 표기 불일치**: §2.6 "350–500 K 7점×2회" vs Fig 2 캡션 "350–700 K". MSD 피팅창·NPT barostat 파라미터 미명시.
- **AIMD 레퍼런스 셀 미명시**(선행 [36] 의존) + AIMD는 600–1200 K 고온 외삽 — AIMD_PBE σRT 절대값도 외삽 부담.
- **Haven=1** 암묵(우리와 동일하나 명시 없음); NE σ는 tracer-D 기반.
- **힘수렴 0.04 eV/Å**의 느슨한 relax; E_rel(meV/atom)은 그 위에서의 값.
- **100% 배열 E_rel 206–284 meV/atom**: "전부 4c" 모델은 실험적으로 접근 불가한 고에너지 구성 — ordered 한계의 σ·Ea는 모델 극한값이지 실측 대상 아님.
- **GB는 Σ5[100](021) 단일 모델** — 다결정 평균 아님; γ 값들은 figure-read(표 없음). Li 축적은 10 ns에서도 미수렴(더 돌리면 D 더 감소한다고 자인) → GB D 절대값은 하한 아님.
- 실험 없음(순수 계산) — σExp는 전부 문헌 소환(Adeli/Jung/Deiseroth).

## 13. 기법 용어 미니사전
- **MTP (moment tensor potential)**: 국소환경을 moment tensor 기저(레벨 lev_max로 복잡도 제어)로 전개하는 선형 MLIP — 학습 빠르고 저비용(Shapeev 2016; MLIP 패키지).
- **lev_max / R_cut**: 기저 복잡도(2+4μ+ν)와 근접반경 — 정확도·비용 트레이드오프의 두 손잡이.
- **passive vs active learning**: 미리 만든 훈련셋으로 한 번 학습(passive) vs MD 중 **외삽등급(γ)** 이 높은 구조만 골라 DFT 라벨링→재학습 반복(active; γ_select 초과 선별·γ_break 초과 중단).
- **Σ5[100](021) tilt GB**: [100] 축 회전으로 만든 coincidence-site-lattice Σ5 경계, 경계면 (021); tilt=회전축이 경계면 내, twist=경계면 수직.
- **random structure**: 6배열을 열역학 가중 개수로 27 unit cell에 무작위 배치한 대표 무질서 supercell.
- **σ80% (χc 보정)**: σ_exp=σ_calc·χc^7.14 회귀에 χc=0.8을 넣은 "실험 결정화도 보정" 전도도 — 경험식.
- **caged vs free Li (MSD)**: MSD 포화=케이지 내 왕복(전도 없음), 선형=장거리 확산 — ordered/disordered 판별 시그니처.
- **solid-electrolyte inductive effect**: 고산화수 치환이 S 전하를 끌어 S–Li 상호작용을 약화 → Li 이동 촉진(Culver/Zeier) — 여기선 GB Li-트랩 완화 처방으로 소환.
