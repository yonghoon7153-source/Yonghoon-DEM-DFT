# 📥 PENDING — `fang2022_argyrodite_transport_beyond_paddlewheel` 인덱스/비교 반영 대기
> ✅ **①②③ 병합 완료 2026-09-13** (조율 세션) — INDEX.md: ① 병합됨 · comparison_vs_ours.md: 2 → Reference key(3·4열 병합자 기입) · 3 → **J9-e′ 개정 행**(J9-e 원문 보존) · 4 → §A 행 3 · 5 → §A 끝 주석. ⏳ **남은 것**: 6. 규율 3줄은 사람 확인.

> 작성 2026-09-09 · litdb-curator (동시 다중 실행 중이라 `INDEX.md`·`comparison_vs_ours.md` 직접 편집 금지)
> **사람이 확인한 뒤 아래 4덩이를 각각 옮겨 붙이고, 이 파일을 지운다.**
>
> ⚠ **이 편은 물성값이 *있다*** (σ·Ea·D). 그러니 `J-7. 🔧 방법 원전` 이 아니라 **축 A(이온전도)** 에 행이 간다.
> **다만 Haven 규약 쪽은 §J-9 의 기존 판정(J9-e)을 *고쳐야* 한다** — 4번째 데이터점이 **반대 방향**이다. §3 참조.
>
> ⛔ **조성 방향 주의**: 이 논문의 argyrodite 기준계는 **Li₆.₂₅PS₅.₂₅Cl₀.₇₅ = S-rich(Cl 0.75)** 다.
> 우리 modelc(**Li₅.₄PS₄.₄Cl₁.₆ = Cl-rich**)와 **치환 방향이 반대**다. 값 이식 금지, 방향·방법만.
>
> ⛔ **talks 역링크 없음**: `litdb/talks/lee2026_skku_mlip_materials_design.md` 의 인입 대기열 6건에 **이 논문은 없다**
> (대기열 #8 은 같은 주제의 다른 논문 `shin2026_bh4_reorientation…` 이고 이미 ✅ 완료). 역링크 작업 불필요.

---

## 1. `INDEX.md` — 붙일 위치: `## ✅ Digest 완료 (paper-level)` (line 22 이하)

| `papers/fang2022_argyrodite_transport_beyond_paddlewheel.md` | **[외부·순수계산(실험 0)·★★Haven 규약 외부앵커·⚠조성 방향 반대]** **Hong Fang\* & Puru Jena\*** (Virginia Commonwealth Univ. 물리, **2인 단일기관**), "**Argyrodite-type advanced lithium conductors and transport mechanisms beyond paddle-wheel effect**" (***Nat. Commun.* 13, 2078 (2022)**, DOI `10.1038/s41467-022-29769-5`; 본문 11 pp + SI 22 pp + **Supplementary Videos 1–3 (mp4, ✅ 시청 완료)**) — argyrodite 할로겐 자리에 **가벼운 1가 클러스터 음이온**(SH⁻·BH₄⁻)을 넣은 **가상** 초이온전도체 2종(**Li₆POS₄(SH)** σ₃₀₀K **82(9) mS/cm**·Ea **0.166 eV** / **Li₆.₂₅PS₅.₂₅(BH₄)₀.₇₅** **177(41) mS/cm**·**0.108 eV**) 제안 + **전도 기전의 재해석**. 기준계 **Li₆.₂₅PS₅.₂₅Cl₀.₇₅ = 14 mS/cm·0.210 eV** (`Fig. 1C`), **figure-read D(600 K) ≈ 5×10⁻⁶ cm²/s**. **🔑 우리 소득 3**: (i) ★★ **Haven 비를 우리와 *같은 규약*(H_R ≡ D\*/D_σ, 캐리어=셀 내 전 Li)으로 낸 유일한 argyrodite-계 AIMD** — 본문 *"inverse Haven ratios … are **1.3 and 1.5**"* ⇒ **H_R = 0.769 / 0.667**(digest 계산), 즉 **σ_NE 는 1.3–1.5배 과소**. 우리 자체 측정 **0.84 ± 0.06**(`db/properties/haven_ratio_measured_2026_09_07.json`, ⚠`citable:false`)과 **같은 대역** ⇒ **인용 가능한 외부 앵커 확보**. ⛔ 단 **Cl 계의 H_R 은 보고 안 됨** — "argyrodite H_R = 0.67–0.77" 일반화 금지; (ii) **`Fig. 6` (F)/(M)/(PM) 3조건 NEB 설계 + 대조경로 P3** = 도펀트 효과를 "격자를 열어 주는 기여 vs 정적 사이트 기여"로 분해하는 틀 (P1 장벽 0.81→**0.06** eV, P3(클러스터 무관)은 **0.90→0.88 = 불변**, figure-read); (iii) **`Fig. S13` inset** — 같은 250 ps 궤적을 4등분하니 50 ps MSD 가 **3.6/5.7/5.9/9.9 Å² = 2.75배** 산포 ⇒ **우리 3-시드 규율의 최상급 문헌 근거**. **★ paddle-wheel 재해석**: 회전은 Li 를 끌고 가는 원인이 아니라 **반응(responsive, 항상 장벽↓ 최대 80 %)** 이고, 열적 자발회전(**active**)은 경로·각도에 따라 **올리기도 내리기도**(`Fig. 6C` P1 −73 %~+40 %). 대신 **'billiard-ball'**(Li–Li 반발 릴레이)·**'revolving-door'**·**'docking–undocking'** 3기전 제안, **Cl 계에서도 billiard-ball 성립**(`Fig. S11`, 500 K, 트리거는 항상 **S_d = 할로겐 자리의 S²⁻**). **⚠ 한계 다층**: 독립시드 0 · 유한크기 보정 0 · 무질서 단일배열(SQS 아님) · **Haven 에 온도·오차·수렴검사 전무** · paddle-wheel 부정의 증거가 **눈으로 본 시계열**(상호상관·lag 분석 없음, `Fig. 4B` 는 회전이 선행하는 **반례**, `Fig. 5A,D` 는 각도 포화로 판별 불가) · **개입실험 없음**(회전 구속 MD 미실시 — 그것을 한 **`shin2026`** 은 **반대 결론**, §12.4). **본문↔그림 불일치 5건 적발**(4자릿수/3.85자릿수, "10 meV" vs 판독 50–150 meV, +80 % vs 판독 +40 %, 범례 오타 `Li₆POS₄P(SH)`, **MOESM3 Video 1 의 "OH" 오기**). **탄성·ESW·COHP·DOS 0건.** 판독: 본문 11 pp + SI 22 pp 전수, 그림 22장 크로핑, **본문 Fig 1–6 + Fig S4·S5·S11·S13 실물 판독**, **동영상 3편 전부 프레임 추출 시청**(각 18프레임) | ✅ |

---

## 2. `comparison_vs_ours.md` — §2-a Reference key 에 추가할 행 (line 12 이하 표)

| **[Fang22PW]** ★★Haven 외부앵커·⚠조성 반대 | **Hong Fang\*** & **Puru Jena\*** 2022 ***Nat. Commun.* 13, 2078** (Virginia Commonwealth Univ. 물리, 2인) — "Argyrodite-type advanced lithium conductors and transport mechanisms **beyond paddle-wheel effect**", DOI `10.1038/s41467-022-29769-5`. **순수 계산**(CALYPSO PSO + VASP PBE/HSE06 + AIMD + NEB, 실험 0). 계: **Li₆POS₄(SH)** · **Li₆PS₅(BH₄)** · **Li₆.₂₅PS₅.₂₅(BH₄)₀.₇₅** · 기준 **Li₆.₂₅PS₅.₂₅Cl₀.₇₅**. digest `papers/fang2022_argyrodite_transport_beyond_paddlewheel.md` |

---

## 3. 🔴 `comparison_vs_ours.md` §J-9 — **기존 판정 J9-e 를 고쳐야 한다** (line ~1319)

**현재 문장**:
> | **J9-e** | **Haven=1 라벨링** — Dai2022 `H_R 0.1–0.4` + Gigli2024 `NE 가 σ 를 2배 넘게 과소평가` + adeli2019 `H_R 0.235–0.315` **3중 반증**. 규약을 바꾸는 게 아니라 … |

**문제**: 세 소환값이 **전부 H_R ≪ 1 쪽**이라 "NE 가 3–4배 과소" 로 읽히기 쉽다.
그런데 **우리 자체 측정(2026-09-07)은 0.84 ± 0.06 = 보정 19 %** 였고, 이제 **네 번째 문헌점이 그 편에 선다**.

**추가/정정 제안 (J9-e 아래 붙일 행)**:

| **J9-e′** 🆕 | **★★ Haven 문헌이 갈리는 것은 *규약*이지 물리가 아니다 (2026-09-09, [Fang22PW] 로 판정 보강)** — **[Fang22PW]** 는 **우리와 동일 규약**(H_R ≡ D\*/D_σ, D_σ = 집단좌표, **캐리어 = 셀 내 전 Li**)의 AIMD 로 **1/H_R = 1.3·1.5 ⇒ H_R = 0.77·0.67** 을 보고한다 (본문 4쪽 한 문장). **우리 gen1 실측 0.84 ± 0.06 과 같은 대역**이다. 반면 **[Adeli] 의 0.23–0.3 은 캐리어를 c = 4 Li/셀(저자가 "하한"이라 명시)로 잡은 값**이고, Li₆PS₅Cl 관용셀의 Li 는 **24개**다 — `D_σ = k_BT σ/(c q²)` 이므로 **c 규약 하나로 H_R 이 6배 움직인다**(digest 계산: 0.23 → ~1.4). ⇒ **[Adeli] 0.23 과 [Fang22PW] 0.67–0.77 을 "문헌이 갈린다" 로 병치하면 안 된다 — 비교 자체가 성립하지 않는다.** ⇒ **MD 규약(캐리어=전 Li)으로 좁히면 문헌·우리 실측이 모두 H_R ≈ 0.7–0.85, 즉 보정 20–50 %** 이고, 이는 **300 K 외삽 밴드(6–14배)·펠릿 GB(1.3–3배)보다 훨씬 작다**. ⛔ 그래도 **"H_R=1 이라서 상한" 은 여전히 틀렸다** — 방향은 **과소** 쪽이다 (2026-09-07 부호 정정 유지). ⛔ **σ_NE 에 1/H_R 을 곱해 "보정된 σ" 를 만들지 않는다** (σ 절대값 인용 금지 불변) |

**⇒ 이 정정의 실무 이득**: 우리 `haven_ratio_measured_2026_09_07.json` 은 `citable:false` 라 **원고에 못 쓴다.**
**[Fang22PW] 의 1.3–1.5 는 남의 출판값이라 인용할 수 있다** ⇒ *"Haven 보정은 자릿수를 바꾸지 않는다"* 를 **인용 가능한 문장**으로 말할 수 있게 됐다.
원고 문구 초안은 digest §13.2.

---

## 4. `comparison_vs_ours.md` §A(이온전도도) 에 추가할 행 3개

| **★★ 우리와 *같은 규약*의 Haven 비를 낸 유일한 argyrodite-계 AIMD — 그리고 저자도 그 보정을 σ 에 적용하지 않았다** — 본문 *"The inverse of Haven ratios … are **1.3 and 1.5**"* (Li₆POS₄(SH) / Li₆.₂₅PS₅.₂₅(BH₄)₀.₇₅) ⇒ **H_R = 0.769 / 0.667**, **σ_true = 1.30× / 1.50× σ_NE** (digest 계산). Methods 의 σ 식은 **tracer D 를 그대로** NE 에 넣는다 = **H_R = 1 규약**. ⛔ **Li₆.₂₅PS₅.₂₅Cl₀.₇₅ 의 H_R 은 보고 안 됨** ⇒ *"우리 계에서 σ 가 몇 배 틀리나"* 는 **이 논문으로 답할 수 없다** | **[Fang22PW]** 본문 p4 + Methods (`D_c` 정의식) | 우리 **NE, H_R = 1 고정** · 자체 실측 **0.84 ± 0.06**(⚠`citable:false`) | **✓ 규약 동일 · 값 같은 대역** |
| **⚠ Ea·D 대비 — real difference 아님(조성 *방향*·힘계산 둘 다 다름)** — [Fang22PW] **Li₆.₂₅PS₅.₂₅Cl₀.₇₅ (S-rich, Cl 0.75)**: Ea **0.210 eV**(700/600/500 K **3점**), σ₃₀₀K **14 mS/cm**(3점 외삽), **figure-read D(600 K) ≈ 5×10⁻⁶ cm²/s**. 그들은 **AIMD(VASP PBE)**, 우리는 **MLIP-MD(UMA-s-1p1)** | **[Fang22PW]** `Fig. 1C` (표 + Arrhenius, figure-read) | 우리 comp1 **0.253 eV / 3.09×10⁻⁶** · modelc **0.224 eV(단일궤적) / 0.197±0.032(3-seed) / 7.90×10⁻⁶** cm²/s | **~ 자릿수 일치, 일치 주장 금지** |
| **★ "billiard-ball" — 국소(intra-cage) 확산이 Li–Li 반발로 릴레이돼 장거리 전도를 만든다. 클러스터 없이 *할로겐 argyrodite 에서도* 성립** — `Fig. S11`(Li₆.₂₅PS₅.₂₅Cl₀.₇₅ @500 K) 결합 Event 3개가 **전부 S_d(할로겐 자리의 S²⁻) 주변**에서 발생, 연쇄 간격 **~0.6–3 ps**. ⛔ **트리거가 S_d 라는 점이 우리와 반대다** — modelc 는 Cl 을 S 자리에 넣은 계라 **S_d 가 원리적으로 없다**. 기전 자체(Li–Li 반발 릴레이)는 도관 종류와 무관하므로 **우리 궤적에서 따로 확인할 문제** | **[Fang22PW]** `Fig. S11` + Discussion 4요인 | 우리 `aimd_jump_stats.py`·`cage_jump_descriptors.py` 로 확장 검출 가능 (Eq.(1) 3-파라미터 필터 미구현) | **미검증 (우리 축으로 안 재봄)** |

---

## 5. (선택) `comparison_vs_ours.md` §A 의 BH₄ 계열 행과 **묶어 읽으라는 주석**

§A 에는 이미 `shin2026` 발(**BH₄⁻ 회전이 Li 수송에 기여**, 회전구속 MD 에서 **D 2.0–3.0배 감소**, 31 hop 중 28개가 ±0.2 ps 동반) 행들이 있다.
그 옆에 다음 주석을 붙이면 좋다:

> 🧭 **paddle-wheel 축은 우리 litdb 안에서 갈려 있다 (2026-09-09).**
> **[Fang22PW]**(AIMD, 관찰) = *"회전은 Li 운동의 **반응**이지 원인이 아니다"* ↔ **`shin2026`**(NMR + AIMD, **개입**) = *"회전이 hop 과 인과적으로 맞물린다"*.
> **개입 실험을 한 쪽(shin)의 증거가 더 강하다** (digest §12.4 우리 평가).
> 단 **두 결론이 반드시 모순은 아니다** — Fang 의 *responsive* 성분(Li 통과 시 클러스터가 비켜 주며 장벽↓)은
> **회전을 구속하면 사라지므로** shin 의 "구속 시 D 2–3배 감소" 를 그대로 설명한다.
> 진짜 쟁점은 *"회전이 있어야 빠른가"*(둘 다 예)가 아니라 **"회전이 hop 을 *개시*하는가"** 다.
> ⚠ 서지 확인 필요: `shin2026` digest §2.2 참조표의 **"[50] Fang & Jena 2020 Nat. Commun."** 은
> 제목 서술이 이 논문(**2022**)과 정확히 일치한다 — **연도가 어긋났을 가능성**.

---

## 6. 병합하는 사람에게 — 이 편을 넣을 때의 규율 3줄

1. ⛔ **σ 절대값(14 / 82 / 177 mS/cm)을 우리 표에 값으로 옮기지 않는다.** 전부 **소환값**이고 우리는 σ 절대값 인용 금지다.
2. ⛔ **H_R = 0.67–0.77 을 "argyrodite 값" 으로 일반화하지 않는다.** 저자는 **클러스터 계 2종만** 냈고 **Cl 계는 안 냈다.**
3. ✅ **가져올 것은 방법 3개**: (a) Haven 규약 문장(§3), (b) `Fig. 6` (F)/(M)/(PM)+대조경로 NEB 설계, (c) `Fig. S13` 적합창 결정 절차.
   추가로 **T16(`tools/ionic/anion_rotation_acf.py`)을 돌릴 근거**가 생겼다 — 목표 그림(`Fig. S5`)과 기대결과("PS₄³⁻ 는 안 돈다")가 문헌에 있다.
