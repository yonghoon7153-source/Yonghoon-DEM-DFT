# ⏳ pending — `jeon2026_concerted_li_motion_argyrodite_assi` 의 INDEX / comparison 반영분
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09, litdb-curator. **동시작업 충돌 회피**(curator 다중 실행)로 `INDEX.md` · `comparison_vs_ours.md` 를 직접 안 고쳤다.
> 아래 블록을 **사람이(또는 조율 담당 세션이) 그대로 옮겨 붙이면 된다.**
> digest 본체: `litdb/papers/jeon2026_concerted_li_motion_argyrodite_assi.md`
> 그림: `litdb/figures/jeon2026_concerted_li_motion_argyrodite_assi/` (**PNG 35장** = 본문 그림 8 + SI 그림 14 + 표 13)
>
> ✅ **talk 역링크 점검함**: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` →
> `litdb/talks/lee2026_skku_mlip_materials_design.md` 하나뿐이고, **이 논문은 그 대기열 9건에 없다**
> (그 큐는 MTP/SevenNet/SKKU·이상욱 랩 계열). ⇒ **역링크 작업 없음.**
>
> ⚠ **서지 정정 1건**: 소속이 **한양대가 아니라 부경대(Pukyong National University)** 다 (PDF 표지 확인).
> 저자 4인·순서·저널(*J. Mater. Chem. A* 2026)·조성(Li₆₊ₓAs₁₋ₓSiₓS₅I)은 1저자 기억과 일치.

---

## ① `litdb/INDEX.md` — **`## ✅ Digest 완료 (paper-level)`** 표에 추가할 행

```markdown
| `papers/jeon2026_concerted_li_motion_argyrodite_assi.md` | **[외부·AIMD·★★Haven 묶음 3편 중 유일한 argyrodite 계산본 · ⛔우리 계와 양·음이온 모두 다름]** **Taegon Jeon**, Dong Hun Shin, Jueun Park, **Sung Chul Jung\*** (**부경대** 물리학과 + SEED 연구소, 부산 — ⚠ 한양대 아님), "**Unraveling the concerted motion of Li ions in argyrodite Li₆₊ₓAs₁₋ₓSiₓS₅I solid electrolytes**" (***J. Mater. Chem. A* 2026**, DOI `10.1039/d6ta04898f`, 접수 2026-06-10/수락 2026-08-28 · 본문 13 pp + SI 44 pp · Fig 8 + S1–S14 · Table 4 + S1–S10 · refs 58). **실험 0 · 순수 계산.** 같은 그룹 argyrodite AIMD 3부작의 마지막(ref 49 Li₆PS₅Cl JMCA2024, ref 50 Li₅.₇₅PS₄.₇₅ClBr₀.₂₅ JMCA2024, ref 40 Li₆₊ₓSb₁₋ₓSiₓS₅I JMCA2025). **방법**: VASP PBE·PAW·**vdW 없음·+U 없음**, ecut 520 eV/k 2×2×2(정적) → **AIMD 258.7 eV·Γ점**, **NVT Nosé–Hoover, dt 1 fs, 500 ps × 700/800/900/1000 K**, 셀 = **1×1×1 단위셀 52–55 원자(Li 24–27)** ⚠ 유한크기 검증 없음, **시드 1개·평형화 미기재**, D = **MSD(t)/6t 의 현(chord)** ⚠우리 자유절편 2–50 ps 와 다른 추정자, σ = **NE·캐리어 = 전 Li**(우리 규약과 동일). **무질서**: Li 배열 1,800 구조(Ewald 16,000 선별) 중 **조성당 최저 1개만** AIMD · As/Si **단일 균일배열** · **S/I 음이온 무질서는 0.85 eV/cell 불리 ⇒ anion-ordered** (⛔ 우리 LPSCl 무질서 기전이 이 계엔 없다). **핵심 물성**: σ(300 K) **6.0×10⁻³ → 0.9 → 8.1 → 12.9 mS/cm** (x = 0/0.25/0.5/0.75), Ea **0.433/0.288/0.223/0.219 eV**, E_hull 0–11.91 meV/atom. **★★ 핵심 발견**: 총 Li 점프 수는 x=0 과 0.75 가 **거의 같은데**(`Fig. 6b` figure-read 60 vs 65 Å⁻³ns⁻¹) σ 는 2×10³ 배 다르다 — **케이지간(intercage) 점프 빈도만 2×10⁶ 배** 바뀐다(`Table 4`). 그 점프는 조성 무관하게 **2–6개 Li 가 0.03–3.40 ps 동안 도미노처럼 협동**(`Table S8/S9`)하고, **성공률만 10 %(x=0) → 37.4–41.9 %(x>0)** 로 오른다. 기전 = Si 가 SiS₄ 의 S₁₆ₑ 를 **−0.93 → −1.45 e** 로 전자 부화(`Fig. 2a`)해 확산 경로 Li 를 정전 안정화(경로 주변 S 가 0.49–0.62 e 더 전자 보유). **★★★ Haven 비(`Table S10`, 우리 묶음의 목표물)**: multi-time-origin MSD 로 tracer/charge D 를 **궤적에서 직접** 분리 → **H = D_tr/D_σ = 1.83(x=0) · 0.53 · 0.64 · 0.77** ⇒ **부호가 조성 안에서 뒤집힌다**(x=0 은 NE 과대, Si 치환계는 NE 과소). **🔑 `adeli2019` 와 달리 캐리어 수 규약이 원천적으로 없다**(H 에서 n 약분) ⇒ **우리 UMA 궤적에 그대로 이식 가능한 유일한 정의**. **⛔ 그러나 H 를 인용하면 안 되는 이유 5**: ① **1000 K 한 점**만(조성×온도 표 없음) ② **오차막대 0**(SI 유일) ③ **`Fig. S14` 에서 x=0 의 charge MSD 가 150 ps 이후 포화 = 확산이 아님** — H>1 을 만드는 유일한 점이 그것 ④ **단일 궤적·Li 24–27개**(집단항은 계 전체가 표본 1개) ⑤ **계산한 H 를 자기 300 K σ 에 반영 안 함**(digest 계산: 반영하면 12.9→16.8 로 실험 8.1–10.4 에서 **멀어진다**). **⛔ 그 밖의 한계(우리 지적)**: `Fig. S5` 에서 **x=0 의 Ea 가 500 ps 까지 계속 상승 중**인데 본문은 "sufficiently converged" · **300 K 외삽 거리가 Arrhenius 적합폭의 4.4배**이고 `Fig. S3` 로 보면 x=0 의 700·800 K MSD 는 사실상 비확산 · σ 오차구간이 x=0.5 [2.8, 23.5]·x=0.75 [7.1, 23.5] 로 **3–8배 폭** ⇒ "실험과 잘 맞는다"가 그 안의 이야기 · `Table S7` 의 x=0.75 두 점프유형 구간이 **[2.1e-3, 4.2e-3] 에서 겹쳐** "T2→T2 가 지배적" 이 통계적으로 미성립(게다가 `Table S2` 에서 컷오프만 바꿔도 140:155 → 180:125 로 대소가 뒤집힘) · **digest 환산: x=0 의 협동 통계(`Table S8/S9` x=0 행)는 사건 2개씩에서 나왔다**(`Table S2` 로 교차확인) — 논문 미기재 · **협동 사건의 그룹화 문턱(몇 Li 를 한 사건으로 묶는지)이 SI 어디에도 없다** ⇒ 초록 헤드라인 "2–6 Li·0.03–3.40 ps" 가 **재현 불가** · **NEB 없음** ⇒ "Si 가 장벽을 X eV 낮춘다" 인용 금지(본문도 전부 *appears/probably*) · `Fig. 5d` figure-read 로 x=0.25 계산 0.9 vs 실험 ≈0.03 = **30배**인데 본문은 "somewhat higher". **부수 축(수분)**: H₂S 생성 E_f(자리 최저값 규약) **Li₆PS₅Cl −0.60 < Li₆PS₅Br −0.40 < Li₆PS₅I −0.24 < Li₆AsS₅I +0.37 < Li₆SbS₅I +0.43 eV**, Si 치환은 −0.27 로 이점 잠식. `Fig. 4` figure-read 추가: **S₄d 자리 O 교환은 전 계에서 +0.8~+1.4 eV 로 항상 불가 ⇒ 가수분해는 폴리음이온을 친다**; LPSCl 은 같은 결정 안 자리별 산포가 **0.38 eV** 로 할로겐 종간 차이(0.36 eV)와 같은 크기. **⛔ 값 이식 전면 금지**: 양이온(As/Si vs P)·음이온(I vs Cl)·무질서 상태(정렬 vs 무질서)가 전부 다르다. Ea 0.219 eV 가 우리 modelc 0.224 와 비슷한 것은 **우연**이며 방법(PBE-AIMD·현 추정 vs UMA·자유절편 2–50 ps)이 다르다 | **축 A(이온전도) 기전·협동 이동 관측량 · ★★Haven 비 방법 원전(J-7)** — σ·D 절대값 이식 금지 |
```

**⚠ INDEX 행에 같이 반영할 것 — 묶음 상호참조**
- Haven 묶음 3편의 층위를 INDEX 에서 서로 가리키게 한다:
  - **`adeli2019`** = *실험* (PFG-NMR D* + EIS σ 역산). ⚠ 캐리어 규약 **c = 4 Li/cell 하한**
  - **`zaby2026`** = *계산 방법론* (액체, EH/GK, ionicity = H⁻¹). 계가 액체라 값 이식 0
  - **`jeon2026`(이 편)** = *계산 + 우리 골격(argyrodite)*. **규약 자유**, 대신 통계가 얇다
- **확보 후보 2건** (이 논문의 참고문헌, 우리 미보유):
  - ref **40** — S. Yi, T. Jeon, J.-H. Lee, Y.-K. Han, S. C. Jung, *JMCA* **13**, 36597–36608 (2025), **Li₆₊ₓSb₁₋ₓSiₓS₅I**. 자매편이고 **단일이온 vs 협동 확산의 NEB 장벽 비교**가 거기 있다 → 우리 NEB 축과 직접 연결
  - ref **53** — C. López, R. Rurali, C. Cazorla, *JACS* **146**, 8269–8279 (2024). **"상관 이온 10 ± 5"** 의 원전. **협동 이동의 정량 문턱**이 여기 있을 가능성 → 이 논문의 정의 공백(§10.2-3)을 메울 후보

---

## ② `litdb/comparison_vs_ours.md` — **§📑 Reference key** 에 추가할 줄

```markdown
| **[Jeon26Con]** | `jeon2026_concerted_li_motion_argyrodite_assi` — **argyrodite 협동 이동 + tracer/charge D 분리** (*JMCA* 2026, DOI 10.1039/d6ta04898f). 계 = **Li₆₊ₓAs₁₋ₓSiₓS₅I (As/Si + I, anion-ordered)** ⇒ 우리 comp1/modelc 와 **양이온·음이온·무질서 상태가 전부 다르다**. **값 이식 금지, 기전·방법만.** Haven 비는 **§J-7 방법 원전** 으로 간다 |
```

---

## ③ `litdb/comparison_vs_ours.md` — **§A. 이온전도도** 표에 추가할 줄 **2개**

```markdown
| **★★ "Li 가 많이 움직인다" 는 σ 의 대리지표가 아니다 — 총 점프 수는 그대로인데 σ 가 2×10³ 배 달라진다** — AIMD 700 K 기준 총 기본점프 수가 x=0 (≈60) 과 x=0.75 (≈65 Å⁻³ns⁻¹, `Fig. 6b` figure-read) 로 거의 같고, 케이지 **안** 점프(T5↔T5·T5↔T2)가 x=0 에서 전체의 **>98 %** 다. σ 를 만드는 것은 **케이지 경계를 넘는 극소수 점프**뿐이며 그 300 K 빈도만 **2.0×10⁶ 배**(digest 검산 ✓) 바뀐다 | **[Jeon26Con]** `Fig. 6a–c` · `Table 4` · `Table S7` | 우리 표준 보고는 **MSD·D·Ea** 뿐이지만, 도구는 이미 있다 — `tools/ionic/aimd_jump_stats.py` 가 **케이지 중심(자유 음이온) 기준 inter-cage hop 율**과 van Hove Gs(r,Δt) 를, `cage_jump_descriptors.py` 가 intra/inter-cage 48h–48h 거리를 낸다. ⚠ 다만 **"총 점프 수 대비 케이지간 비율" 로 묶어서 보고한 적이 없고**, BVSE 채널%(`tools/comp1_v3/`)와 **짝지어진 적도 없다** | 🔑 **규율로 채택 후보.** MSD 총량·확률밀도 부피·BVSE above-min 부피는 **연결성(percolation) 지표가 아니다.** `Fig. 6a` 의 "끊어진 케이지 → 연결된 3D 망" 이 그 시각화 — 우리 BVSE 그림과 같은 메시지의 MD 판 |
| **★ 협동 이동은 "빈도"만 도펀트로 조절되고 "성질"은 안 바뀐다 (⇒ cascade 축이 하나 생긴다)** — 700 K, x = 0→0.75 전 구간에서 참여 Li 수 **2–6**(평균 3.31–4.50)·지속시간 **0.03–3.40 ps** 가 x 에 **거의 무관**하고, 바뀌는 것은 **사건 빈도**(T5→T4→T5 3.7×10⁻³ → 0.25 Å⁻³ns⁻¹)와 **성공률(10 % → 37.4–41.9 %)** 이다. 지렛대는 **국소 음이온 전하**(S₁₆ₑ −0.93 → −1.45 e; 확산 경로 주변 S 가 0.49–0.62 e 더 보유) | **[Jeon26Con]** `Table S8` · `Table S9` · `Fig. 2a` · `Fig. S10/S11`(본문 인용) | 우리 도핑 캠페인(Nd/O·B₂O₃ 등)은 **Ea·D 만 본다** — "성공률"·"협동 사건 빈도" 를 관측량으로 쓴 적 없다. Bader·ICOHP 는 이미 낸다 | 🔶 **방향만 이식.** 값은 As/Si+I 계라 금지. 우리 쪽 번역 = *"도펀트는 협동을 만들지 않는다 — 이미 있는 협동 사건의 성공률을 올린다"* ⛔ 단, 이 논문의 참여 Li 수·지속시간은 **그룹화 문턱이 SI 에 없어 재현 불가** ⇒ 관측량으로 채택하려면 **우리가 문턱을 정의해야 한다** |
```

---

## ④ `litdb/comparison_vs_ours.md` — **§J-7 `🔧 방법 원전`** 에 추가할 블록 ★ (여기가 본체)

> ⚠ **왜 물성 4축(A–D)이 아니라 J-7 인가**: Haven 비는 **우리 계의 물성값이 아니라 우리 σ 규약의 오차**다.
> 그리고 이 논문의 σ·D·Ea 절대값은 As/Si+I 계라 A 축에 못 올린다. **A 축에는 위 ③ 의 두 줄(기전)만** 간다.

```markdown
#### J-7-N. ★★★ **[Jeon26Con] — Haven 비를 궤적에서 직접 재는 법 (규약 자유) + 묶음 3편 재정렬** (2026-09-09 신설)

**(a) 이 편이 채우는 빈칸**
우리 σ 는 **NE, Haven H_R = 1 고정**이다. 그 오차를 재려고 모은 3편 중 **유일하게 (i) 우리와 같은 argyrodite 골격이고
(ii) tracer 와 charge D 를 *같은 궤적에서 직접* 분리**한 편이다.

| 출처 | 계 | 방법 | 원 보고 H_R | 캐리어 수 규약 |
|---|---|---|---|---|
| **[Adeli19]** | Li₆₋ₓPS₅₋ₓCl₁₊ₓ | 실험 PFG-NMR + EIS 역산 | 0.23–0.3 | ⚠ **c = 4 Li/cell (저자 명시 하한)** |
| **[Zaby26σ]** | IL·LiFSI 액체 | 고전 MD (EH·GK) | 1.3–2.1 | 전 이온 (모호성 없음) |
| **[Jeon26Con]** | Li₆₊ₓAs₁₋ₓSiₓS₅I | **AIMD, 집단 MSD 직접** | **1.83 / 0.53 / 0.64 / 0.77** | **없음 (H 에서 n 약분)** |

**(b) 재현에 필요한 규격 전부** (`Table S10` · SI "Tracer and collective diffusion")
- `MSD_σ(τ) = 1/[N(N_t−n)] · Σ_j |Σ_i (r_i(t_j+τ) − r_i(t_j))|²` — **합을 먼저, 제곱을 나중에.** 정규화는 **1/N** (1/N² 아님)
- `MSD_tr` 도 **같은 multi-time-origin** 으로 다시 계산 (본문 `Fig. 5`/`Table 3` 의 단일 origin 값과 다르다)
- `D = MSD(τ)/6τ` — **원점 통과 현(chord)**. ⚠ **우리는 자유절편 기울기 2–50 ps** ⇒ **추정자가 다르다**
- `τ_max = 총 시뮬 시간의 1/2` (여기선 250 ps / 500 ps)
- **unwrapped 좌표 필수** (wrap 되면 벡터합이 깨진다)
- 도구 `pymatgen-analysis-diffusion` (ref 48 Deng 2017) · multi-origin 근거 ref 58 (He/Mo 2018)
- `H = D_tr/D_σ = σ_NE/σ_col`, `σ_col = n q² D_σ/(k_B T)`

**(c) ★★ digest 계산 — 규약을 맞추면 묶음의 그림이 바뀐다** *(원논문 미보고 · 우리 대조)*
[Adeli19] 는 `D_σ = k_B T·σ/(c q²)` 이므로 `H_R ∝ c`. c: 4 → 전 Li(22–24/cell) 로 옮기면 **H_R 이 5.5–6배**:

| | 원 보고 | **전-Li 규약 환산** | NE 는 |
|---|---|---|---|
| [Adeli19] x=0 (Li₆PS₅Cl) | ~0.3 | **≈1.8** | 과대 |
| [Adeli19] x=0.5 | 0.23 | **≈1.3** | 과대 |
| [Zaby26σ] | 1.3–2.1 | 1.3–2.1 | 과대 |
| [Jeon26Con] x=0 | 1.83 | 1.83 | 과대 |
| **[Jeon26Con] x=0.25–0.75** | **0.53–0.77** | 0.53–0.77 | **과소** |

⇒ **규약을 맞추면 4개 중 3개가 H_R ≈ 1.3–2.1 (NE 과대) 로 모이고**, 유일한 이탈자가 [Jeon26Con] 의 Si-치환 조성인데
그것이 하필 **집단 MSD 통계가 가장 미심쩍은 값들**이다.

⚠⚠ **과신 금지 3**: ① [Adeli19] σ 는 cold-press **total** 이라 GB 가 σ 를 깎으면 H_R 이 **부풀려진다** ⇒ 진짜 bulk 는 1.3–1.8 **미만**
(다만 Ea(EIS)≈Ea(PFG) 이므로 GB 가 *장벽*은 안 건드린다 — 앞지수만) ② [Adeli19] 의 c=4 는 임의값이 아니라 저자의 물리 논거
(케이지간 점프가 장거리 수송을 지배) ⇒ 전-Li 가 **더 옳다는 뜻이 아니라 같은 자를 써야 한다는 뜻** ③ 온도가 다르다(1000 K vs 270–340 K).

**⇒ 판정 (변경 없음)**: **"H_R = 1 은 근사가 아니라 미측정이고, 오차의 부호조차 우리 계에서 확정돼 있지 않다."**
다만 **약한 사전(prior)** 이 생겼다 — *규약을 맞추면 argyrodite 에서도 H_R > 1 쪽 증거가 더 많다*. **인용할 결론이 아니라 직접 잴 이유다.**

**(d) ⛔ [Jeon26Con] 에서 인용 금지**
- "argyrodite 의 Haven 비는 0.53–0.77 이다" — **1000 K 1점 · 오차막대 0 · 단일 궤적 · Li 24–27개**
- `Fig. S14` 에서 **x=0 의 charge MSD 는 150 ps 이후 포화**(확산 아님)한데, **H>1 을 만드는 유일한 점이 그것**
- 저자 자신이 **계산한 H 를 300 K σ 에 반영하지 않았다** (digest 계산: 반영 시 12.9 → 16.8 mS/cm 로 실험 8.1–10.4 에서 **멀어진다**)
- σ·D·Ea **절대값 전부** (As/Si+I·anion-ordered 계). ⚠ Ea 0.219 eV 가 우리 modelc 0.224 와 가까운 것은 **우연** — 방법도 계도 다르다

**(e) ✅ 우리가 할 것 — 도구가 이미 거의 다 있다 (digest §12 와 동일)**
> 🔎 **기존 도구 조사 결과 (CLAUDE.md 코드 규율 사다리 ②)**: `tools/ionic/` 에 이미 있다 —
> `msd_origin.py`(MSD→Arrhenius, **최소상 언랩 `df -= np.round(df)` 내장**, `T*/traj.xyz` 를 직접 읽음) ·
> `msd_diffusive_check.py`(**확산영역 인용 게이트**, `no-value`/`HOLD` 2층 판정) ·
> `msd_refit_window.py`(재계산 없이 창 스윕) · `aimd_jump_stats.py`(**케이지 중심 기준 inter-cage hop 율** + van Hove Gs) ·
> `cage_jump_descriptors.py`(intra/inter-cage 48h–48h 거리). ⇒ **새 파일을 만들 이유가 없다.**

1. **보고량 카드 먼저** (`kb/templates/estimand_card.md`): 추정자(현 vs 자유절편)·τ 창·시드 집계·**폐기 기준**을 **결과 보기 전에** 못박는다.
   폐기 기준은 새로 정의할 필요 없다 — **`msd_diffusive_check.py` 의 `no-value`/`HOLD` 2층 판정을 MSD_σ 에 그대로 적용**한다.
   (**[Jeon26Con] `Fig. S14` 의 x=0 곡선이 정확히 그 도구의 `no-value` 사례다** — 좋은 시험 표본)
2. **`tools/ionic/msd_origin.py` 에 `--collective` 플래그** 추가 (MSD_σ = (1/N)⟨\|ΣΔr\|²⟩, multi-origin, τ_max = T/2).
   ⚠ **`msd.json` 으로는 안 된다** — 거기엔 tracer MSD 시계열만 있고 좌표가 없다. **집단 MSD 는 반드시 `T*/traj.xyz` 에서.**
3. 파일럿(무료): 기존 comp1·modelc **1000 K 궤적**으로 MSD_σ 를 그려 `Fig. S14` 식 포화가 나오는지 본다 → 나오면 1번 게이트 발동
4. 추정자 두 벌(현 / 자유절편 2–50 ps)로 H 를 다 내서 **추정자 의존성**부터 보고
5. 본계산: **배열 시드 + 속도 시드 8–16개 × 500 ps–1 ns**. ⚠ 우리 현행 3-seed 는 **속도 시드만·배열 고정**이라 집단항엔 부족
   🔑 **H_R 의 병목은 힘 정확도가 아니라 독립 궤적 수다 ⇒ 이 논문이 AIMD 로 못 한 것(조성당 500 ps × 1개)을 UMA 로 살 수 있다**
6. (별건, 값싸다) **§A 의 "총 점프 수는 그대로, 케이지간만 바뀐다"를 우리 계에서 재현** — `aimd_jump_stats.py` 가 이미 inter-cage hop 율을 낸다
7. (사용자 승인 후) `adeli2019` digest §3c 에 **전-Li 규약 환산 ≈1.3–1.8** 을 각주로 추가
```

---

## ⑤ (선택) `litdb/comparison_vs_ours.md` — **§B. 산화안정성** 에는 넣지 **말 것**

이 논문의 안정성 축은 **가수분해(H₂O → H₂S)** 이고 우리 §B 는 **전기화학 산화(grand-potential ESW)** 다. **다른 축이다.**
다만 §B 서두의 *"축 명명 없이 말하면 틀린다"* 규율의 **새 실례**로 각주 한 줄은 가능:

```markdown
> ⚠ 새 실례 (2026-09-09): **[Jeon26Con]** 은 Li₆PS₅Cl 의 H₂S 생성 E_f = **−0.60 eV** 로 "Li₆PS₅Cl 이 가장 불안정" 이라 하지만
> 이건 **수분 축**이지 우리 onset 2.256 V(축 ① S²⁻-limited)와 아무 관계가 없다. 게다가 그 −0.60 은 **여러 S₁₆ₑ 자리 중 최저값**이고
> 같은 결정 안 산포가 **0.38 eV**(`Fig. 4b` figure-read)로 **할로겐 종간 차이(0.36 eV)와 같은 크기**다 ⇒ 인용 시 "자리 최저값 규약" 명시 필수.
> 부수 소득: **S₄d(자유 S²⁻) 자리 O 교환은 전 계에서 +0.8~+1.4 eV 로 항상 불가** ⇒ 가수분해는 **폴리음이온(PS₄/AsS₄/SiS₄)을 친다**.
```

---

## ⑥ 정리 — 이번 세션이 건드린 파일 (충돌 회피 준수)

| 파일 | 상태 |
|---|---|
| `litdb/papers/jeon2026_concerted_li_motion_argyrodite_assi.md` | ✅ 신규 작성 |
| `litdb/figures/jeon2026_concerted_li_motion_argyrodite_assi/` | ✅ 신규 (PNG 35 + figures.json) |
| `litdb/figures/_sources.json` | ✅ 도구가 자동 갱신 (194편 색인) |
| `litdb/inbox/89._*.pdf` (본문 + SI) | ✅ 업로드본 복사 |
| `litdb/_pending_index_jeon2026_…md` | ✅ 이 파일 |
| `litdb/INDEX.md` · `litdb/comparison_vs_ours.md` | ⛔ **안 건드림** (지시대로) |
| `db/` · git | ⛔ **안 건드림** (지시대로) |
