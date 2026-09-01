# 진행 중 — litdb 정본 4편 작업 (2026-08-19, 압축 대비 스냅샷)

⚠ **커밋 안 된 상태**.  정본 워크트리에서 에이전트들이 쓰는 중이다.

## 워크트리

```
/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/litdb-canon
  = origin/claude/friendly-meitner-lldvar  (로컬 브랜치 tmp-litdb-58, 정본 168편)
```
**커밋·푸시는 `claude/friendly-meitner-lldvar` 로만** (litdb 단일 서랍 규약).  이 리포 `litdb/` 는 동결 스냅샷.
webapp 은 `scripts/litdb_sync.py` 가 `origin/<branch>` 를 **직접 읽으므로 푸시 = 반영**.

## 상태

| | 논문 | 상태 |
|---|---|---|
| A | Wang & Wang, JMCA 2026 (건식 후막 NCM94 실패기전) | ✅ **완료** `litdb/papers/wang2026_dryprocess_thick_cathode_failure_ncm94.md` (824줄) |
| B | Weitze/Franco, ESM 2024 (습식 resolved-AM) | 진행 중 — **기존 카드 심화** (`wet_processing_resolved_am_ssb_cathode_manufacturing.md`) |
| C | Alabdali/Franco, JPS 2023 (3D 습식 제조) | 진행 중 — 신규 |
| D | Joule (후막 열화 multiscale imaging + 모델) | 진행 중 — 신규 |

A 가 건드린 파일: 위 카드 · `INDEX.md`(신설 섹션) · `comparison_vs_ours_DEM.md`(+147줄, 6축) · `comparison_vs_ours.md`(+2줄).
⚠ slug 에 `dryprocess` 를 넣어야 webapp `literature_track()` 이 **dem** 으로 분류한다 (없으면 dft 로 오분류).

## A 편 — 살릴 수치 (전부 stated, 논문 실측)

| 값 | 우리 축 |
|---|---|
| **AFM Young's modulus 3.056 / 2.248 / 1.263 GPa** (건식 복합막 3점, Fig S3) | ★ E_eff 방어선 |
| R_s 9.4→8.6 · R_ct1 12.5→**55.4** · R_ct2 83.8→**939.7 Ω cm²** (50 cyc @0.1C) | R_int(N) |
| DRT τ 창: **D1 10⁻⁶–10⁻⁵ = 입자 간 고체-고체 접촉** / D2 10⁻⁵–10⁻² 계면상 이온 / D3·D4 전하이동 | ★ 접촉망 |
| in-situ 스택압 −1.95 MPa (ΔP/P₀ **1.81 %**), 비가역 **1.20 %**, 래칫 **−0.30 MPa/cyc** | A10 |
| 두께 177.3 µm → 127.1–138.9 (300 cyc) = **−21.7 … −28.3 %** | — |
| I(003)/I(104) 1.99 → 1.40 | 벌크 열화 |
| 0.1C 50 cyc **87.1 %** vs 0.5C 50 cyc **98.3 %** (3.5 V) | 시간구동 열화 |

레시피: NCM94(SC 2–4 µm) : **Li₅.₄PS₄.₄Cl₁.₆** : VGCF : PTFE = **80:18:1:1**, 177.3 µm, **6.5 mAh/cm²**, 운전압 110/200 MPa.

## ⛔ A 편이 **못 채운 것** (요청 축 기준 — 중요)

- **σ_e/σ_ion 절대값 = n/a** (복합체 전도도 실측 0건).  ⇒ 우리 SBE 73 / 54.6 mS/cm 는 **검증도 반박도 안 됐다**.
  문헌 밴드 **Lee 2025 34 · Kim 2024 38.6–65.2 그대로 유지**.
- **PTFE ↔ 전도도 = n/a** (1 wt% 한 점).  **Lee 2025 SI Fig 5 가 여전히 유일 곡선.**
- 집전체 계면 = n/a (R_s 에 섞임).  `nam2026_primer_layer` 가 계속 정본.
- porosity·다압력/Heckel·packing/bimodal·G_c/K_IC — 전부 없음.

## 세 판단 (에이전트 질의에 대한 내 답 — 원장에 넣기 전 초안)

1. **AFM 1.3–3.1 GPa 를 E_eff 서사에 어디까지?** → 에이전트가 그은 선(**자릿수 진술만**)이 **맞다, 보수적이지 않다**.
   막 압입 모듈러스와 우리 E_eff(입자 접촉강성 입력, frame[2] lumping)는 **범주가 다르다** — σ_VGCF 에서
   방금 겪은 분말↔단섬유 범주오류(CL-47)와 같은 형태다.  ⇒ "18× 연화가 자의적" 이라는 비판의 **방어선**으로만
   쓰고 **"일치/검증" 금지**.
2. **−1.95 MPa 를 스택강성 없이 A10 에 어떻게?** → **무차원·강성무관 3개만**: ΔP/P₀ 1.81 % · 비가역 1.20 % ·
   래칫 −0.30 MPa/cyc.  Δ부피 환산 금지.  **방향 앵커**(SC 는 충전에 수축)로 등록하고 크기는 안 쓴다 —
   A10 `--poly-mode` 분기(SC=계면 debond / poly=내부 void)를 **셀 레벨에서 지지**하는 것이 값어치다.
3. **시간구동 열화(0.1C 87.1 % vs 0.5C 98.3 %)를 STEP5 에?** → **값어치 있다**.  같은 사이클 수에서
   저율이 더 나쁘면 열화가 **사이클 구동이 아니라 시간(캘린더) 구동**이라는 뜻이고, 그건 STEP5 rate law 의
   **형태**를 바꾼다.  ⚠ 단 1편·1조건이므로 **가설 등록**으로만.

## 다음

1. B·C·D 완료 대기 → 4편 한 번에 검토
2. `claude/friendly-meitner-lldvar` 로 커밋·푸시 → webapp 자동 반영
3. worktree 제거 (`git worktree remove`, 브랜치 `tmp-litdb-58` 삭제)
4. 위 세 판단을 원장(claims.json)에 반영할지 결정

## 병행 — kgy STEP 4 (별개)

vox 0.125 CL-41, 11/16 팔 시점 5쌍 평균 ~~R = 1.14508~~ (SE 0.107 %p) — **폐기된 중간값**.
8팔 완주 확정값은 **R = 1.143817** (CL-41).  중간값은 인용하지 않는다.
`python3 ~/dem-sk/scripts/sdcp_gain_verdict.py --dir prereg_v2_vox0125_sph_b048_lean2 --collect-only`

---

# B편 완료 (2026-08-19) — Weitze/Franco 카드 심화 288 → **528줄**

수정 파일: `litdb/papers/wet_processing_resolved_am_ssb_cathode_manufacturing.md` (신규 절 + 본문 26곳 `⚠정정2026-08-19`) ·
`comparison_vs_ours_DEM.md` (+230줄, 축 A/B/C/F).  `INDEX_DEM.md` 는 **자동생성**이라 미수정 (헤더가 손대지 말라고 명시).

## ★★ 옛 카드 정정 7건 — 하나는 우리 쪽 **근거 없는 서술**

| # | 초판 | 정정 |
|---|---|---|
| C1 | AM = NMC622 75 wt% | **반전 오독** — NMC622 는 nano-CT **형상 공여체**, 슬러리 AM 은 다른 Ni-rich |
| C2 | 슬러리 22 → 건조 110 → 압연 40 µm | 110 은 **슬러리 기둥 높이**, 40 이 건조 전극.  110→40 = 건조 수축 2.75배.  stated → **digitized(Fig 4)** |
| C3 | "연속체 → σ_eff **상한**" (6곳) | **갈라야 한다** — 방법 수준(접촉·계면 저항 항 부재)에서는 상한, **결과 수준에서는 실험의 1/10** |
| C4 | "무차원 → 절대 비교 불가" | **형성인자 F 축에서는 직접 비교됨**(순수 기하량).  전자만 불가 |
| C5 | AM PSD "명시 없음" | SI 에 있음 — Gaussian 4.5±0.79 µm [3,6] 절단, SE 단분산 **Ø1.0 µm** |
| C6 | Fig 7 AM–SE "거의 일정" | **1.08 → 1.25 (+16 %)** = 유일하게 오르는 상-상 계면 |
| **C7** ⚠⚠ | "그들조차 future work 로 **constriction/contact 저항**을 시사" | **근거 없음.**  본문·SI 에 "constriction"·"Greenwood" **0회**.  그들 향후과제는 porosity-vs-압력·전도도·cracking 뿐 → **인용 금지** |

## ① 그들이 solid-state 를 구현한 방식 (핵심만)

- **AM 만 resolved**: nano-CT 형상 → Ø0.97 µm 1차 구 ~50개 + **harmonic bond κ=1e6 로 강체 고정** (multisphere)
- **SE 는 단분산 Ø1.0 µm 완전 구** — nano-CT 가 SE/carbon/binder 를 gray 로 구별 못 해 **원리적으로 resolved 불가**라고 저자가 명시.
  ⇒ **이온수송의 주역 상은 그들도 우리와 같은 구다.**  (그리고 Ø1.0 µm = 우리 r_SE 0.5 µm 와 정확히 일치)
- 접촉 = **JKR (탄성+점착, 항복캡 0)**.  SI: 쌍-유효 **E = 135 GPa** (실물 LPSCl 22–24, 우리 E_eff 1.35),
  **γ ≈ 1000 J/m²** (Bucci G_c 2.8 의 ~350배 = 수치 응집항)
- **소성 전무** — 본문에 "plastic/plasticity" **0회**, 절대압(MPa) **0회**.  결론에서 *"겹침을 크게 허용하지 않는
  force field 는 setback"* 이라 **자인**하고 *"porosity as a function of applied pressure 로 보정하라"*
  (= 정확히 우리가 이미 하는 것) 를 향후과제로 단다.
  ★ 우리 산술: 그 강성에서 LPSCl 은 **δ ≈ 2 pm 에서 이미 항복** (δ=10 nm 면 p̄ ≈ 11.6 GPa)
- LJ ε 가 단계마다 **15.1 → 150,000 → 75,000 (10⁴배)** = fit 노브.  건조는 CBD Ø2.438 → 0.7 µm (부피 42배) 축소
- 실험 앵커 **2점뿐**(슬러리 밀도 1.353±0.001 · 건조 porosity 0.53±0.03)이고 **둘 다 보정에 소비 = held-out 0**.
  압연 단계 force field 는 앵커가 **아예 없다**
- GeoDict: DiffuDict(Δc=1 mM)/ConductoDict(ΔV=1 V), 상 벌크 σ=1 정규화.
  **상별 σ 입력값·voxel 크기·τ 계산값 전부 미보고**, 접촉/계면 저항 항 **없음**

## ② 결과 수준 — 그들 이온 전달이 실험의 1/10 이다

| | 형성인자 F_ion | N_M |
|---|---|---|
| 그들 (GeoDict) | **1.35×10⁻²** | 74 |
| Bazzoun **실험** | 0.134 | 7.5 |
| 우리 STEP3 | 0.052–0.166 | 19–6 |

조성 탓이 아니다 (그들 SE/solid 28 % ≈ 우리 26–27 %).  원인은 **φ_SE ≈ 0.15–0.18 이 문헌 이온-percolation
문턱 25 % 아래**라 τ_SE 가 375 → 13 (Bruggeman 의 5.6–145배 나쁨) + 계면이 압밀에 반응 안 해 목이 얼어붙음.
⚠ **voxel 크기를 안 밝혀 그 목을 감사할 수조차 없다** — 우리가 CL-25 로 그 노브의 18배 변동을 실측한 것이
진짜 방법론적 우위.

## ③ 당장 쓸 수 있는 앵커 (10건 중 핵심 5)

| 값 | 우리 축 |
|---|---|
| **건조(미압연) porosity 0.53±0.03** (stated 실험) | 압밀 시작점 |
| **springback = 압축량의 10–15 %** (우리 산출; relaxed 23.8–24.6 µm ↔ Fig 5 종단 ≈24 µm 자기일관 ✓) | ★ **MPM unload 검증 타깃** |
| **F_ion/F_e 9점** | 형성인자 대조 |
| **유도 AM 표면 SE-피복률 14.4 → 20.9 %** | 우리 Hertz 16–18 %·MPM 기하 16 % 와 **같은 밴드** (Tabor 48–52 와는 다른 밴드) |
| SE **Ø1.0 µm** = 우리 r_SE 0.5 µm 와 일치 | 규약 대조 |

⛔ **σ_e 밴드 배치 불가** — σ_e = 1.13e-3 × σ_CBD,bulk 인데 **σ_CBD,bulk 가 논문·SI 어디에도 없다(n/a)**.
역산하면 우리 밴드에 앉으려면 σ_CBD ≈ 30–65 S/cm 여야 하고 우리 탄소 규약(100, 분말 83)과 자릿수는 같지만
**가정 위의 숫자라 원고에 "밴드 안" 이라고 쓰면 안 된다.**  ⇒ 이온 축은 밴드 **밖**(더 저항적)에 명확히 앉는다.

⚠ 추가 완화 2건: porosity floor 29 % 를 강성에 귀속 금지 (같은 SI 가 CBD E = 1–20 kPa 초연질을 주고 압력 축이 없음) ·
논문 자체 오류 1건 (Fig 7 서열을 "SE 부피 최대" 로 설명하나 자기 Fig 5 가 φ_AM > φ_SE — 실제 이유는 비표면적)

---

# ⚠⚠ 정정 2건 (2026-08-19) — 코팅 논의에서 내가 틀린 것

## 정정 ① "So 2022 JPS coated-particle DEM 을 digest 해야 한다" → **이미 정본에 있다**

`litdb/papers/so2022_dem_compaction_coated_particles_assb.md` (236줄, digested 2026-06-26,
DOI 10.1016/j.jpowsour.2022.231279).  `so2022_dem_contact_model_assb_compaction_sintering`
(MethodsX = 방법) 과 **한 쌍**이고 데이터 CSV `docs/data/so2022_coated_particles.csv` 까지 있다.
⇒ **웹서치 결과만 보고 "신규 digest 후보 1순위" 라고 한 것은 틀렸다.**  litdb 를 먼저 봤어야 했다
(CLAUDE.md 규율: "카드 만들기 전 정본 INDEX 먼저 확인").

## 정정 ② "코팅은 sub-voxel 이라 부피로 못 그린다" → **SE 코팅에는 해당 없다**

사용자가 뜻한 코팅은 **NCM 에 LPSCl + dopant** 다.  LNO/LZO 산화물 나노코팅(5–20 nm)을 전제로
S/N 표를 짰던 것이고, **SE 코팅은 µm 급**이라 DEM·복셀 **둘 다 해상 가능**하다.
So 2022 규약: AM 1 µm primary → **5 µm 응집체** · SE 0.5 µm primary → **1.5 µm 응집체**
⇒ 내 S/N 표의 **t ~ 500 nm, S/N 116 ✅ "확실히 보인다"** 밴드.

## So 2022 (JPS 530, 231279) 가 이미 낸 결과 — 우리가 하려던 것의 선행

| | 입자 혼합 | **SE 코팅(core-shell)** |
|---|---|---|
| SE percolation > 90 % 도달 압력 | **360 MPa** | **25 MPa** |
| AM percolation @25 MPa | ~1.0 | **~0.3** ⚠ |
| τ_SE (50 → 500 MPa) | 36 → 6 | **10 → 4** |
| porosity @360 MPa | ~17 % | ~16 % |
| AM 손상 @500 MPa | ~12 % | ~12 % (같음) |

★ **핵심 = 코팅의 σ_e 차폐**: 저압에서 SE 쉘이 **AM–AM 전자접촉을 차폐**해 전자수송이 끊기고,
**200 MPa 초과에서 차폐가 사라진다**(쉘 박리/관통 → AM–AM 접촉 형성).

⇒ ⚠ 내가 제안한 **"코팅 = 접촉당 직렬저항"** 모델은 **불충분하다**.  실제는 저압에서 **접촉 자체가
안 생기고**(위상 변화) 고압에서 쉘이 뚫려 생기는 **압력 의존 스위치**다.  직렬저항으로는 그 전이를 못 낸다.

⚠ 전이 한계: LPS(Li₂S–P₂S₅) + NCM/LiCoO₂ 이고 전달을 **σ 솔버가 아니라 TauFactor τ 로 추정**
⇒ 절대값 전이 금지, 방법·추세만.

## dopant 축 — 정본에 이미 8편+

`ma2024_sb_doping_lpsc_conductivity` · `li2025_cubr2_dualdoping_argyrodite` ·
`xu2026_ndo_codoping_argyrodite` · `wang2025_electronic_localization_yo_argyrodite` ·
`deklerk2016_diffusion_site_disorder_argyrodite` · `zhou2026_high_entropy_lgps_multicationic` ·
`schlem2020_li3mcl6_cation_site_disorder` · `torii2025_lpscl_mechanical_anisotropy_dft`

⇒ **dopant = σ_SE 값 축** (우리 파이프라인에서 `--sigma-ion-se` 한 줄) ·
   **코팅 = 그 SE 를 어디에 두느냐 위상 축** (시딩/스탬프 구조).  **완전히 분리돼 있다.**

## ⇒ 우리 자리가 바뀐다 (novelty 재조준)

"코팅을 DEM 으로 그린다" 는 **선행이 있다**.  우리 자리는 **그들이 안 한 것**:

| 그들이 한 것 | **안 한 것 = 우리 자리** |
|---|---|
| core-shell SE 코팅 DEM 압밀 | **접촉당 Holm 협착 σ** (그들은 τ 추정) |
| τ_SE / τ_AM (TauFactor) | **σ_e·σ_ion·k 절대값 삼중항** |
| percolation · damage | **MPM 소성 형태 + 복셀 FV 이중 이산화** |
| LPS + NCM/LiCoO₂ | **LPSCl + NMC811 (우리 소재계)** |
| 압력 스윕 | **dopant σ_SE 축 × 코팅 위상 축 교차** |

★ **깨끗한 검증 표적**: 그들의 "저압 σ_e 차폐 → 고압 해제" 를 **우리 σ_e 솔버(Kirchhoff)로 재현**할 수
있는가 — τ 추정이 아니라 실제로 풀어서.  이건 frame[4] 형태의 독립 재현이고, 성공하면 우리 접촉망
솔버가 그들 연속체/τ 추정보다 **무엇을 더 보는지**를 보여준다.

## 코드 리뷰 대상 (착수 전 — 사용자 지시 "다 진행해보고 하기전에 코드 리뷰 받아봐")

1. **SE 코팅 시딩** — `R+t` 가 아니라 **core-shell 다입자**(So 2022 규약: 응집체) 로 갈지.
   ⚠ DEM 덱의 `density constant 4800` 은 AM 코어 값 — 쉘 밀도가 다르면 질량 규약이 깨진다.
2. 접착·마찰 민감도 팔 (`coefficientAdhesionStiffness`·`coefficientFriction`) — 기존 노브, 안전.
3. **σ_e 차폐를 접촉망에서 재현** — 직렬저항이 아니라 **접촉 생성/소멸**로 나오는지.
4. 옴(`--coat-sigma-b`) ↔ 패러데이(R_ct) 분리 게이트.
5. 다중 seed 사전등록 (얇은 코팅이면 S/N 1.8; **SE 코팅이면 S/N 100+ 라 이 제약은 완화**).
