# 📥 PENDING — `maginn2019_best_practices_transport_selfdiffusivity_viscosity` 인덱스/비교 반영 대기
> ✅ **①②③ 병합 완료 2026-09-13** (조율 세션) — INDEX.md: ① 병합됨 · comparison_vs_ours.md: 2-a → Reference key · 2-b → J-7 · 2-c → §H 행 3 · 2-d → **J-18** 머리 선언. ⏳ **남은 것**: 3. properties 갱신 **미처리** (db 규율) · 4. talk.

> 작성 2026-09-09 · litdb-curator (동시 다중 실행 중이라 `INDEX.md`·`comparison_vs_ours.md` 직접 편집 금지)
> **사람이 확인한 뒤 아래 3덩이를 각각 옮겨 붙이고, 이 파일을 지운다.**
>
> ⚠ **형제 4편과 같은 다발이되 반대쪽 절반이다.** 오늘 들어온 MLIP 불확실도 4편 —
> `#78 imbalzano2021` · `#79 carrete2023` · `#80 kurniawan2025` · `#81 grasselli2025` — 은 전부
> **모델(epistemic) 불확실도**를 다룬다. **이 편(#82)은 그 넷이 다루지 않는 나머지 절반,
> 즉 궤적 유한성에서 오는 *통계(random)* 불확실도의 정본**이다.
> ⇒ 병합하는 사람에게: **`J-11` 을 만든다면 이 편이 그 절의 "통계 축" 이고 넷이 "모델 축" 이다.**
> 두 축을 한 표에 섞지 말 것 — 재는 양이 다르다 (`Ea 0.197 ± 0.032 eV` 의 ±0.032 는 통계 축이다).
>
> ⛔ **물성값 0건** — σ·Ea·D·ESW·탄성·gap 어느 것도 없다. **물성 4축(A–I) 표에 넣지 말 것.**
> 갈 곳은 `J-7. 🔧 방법 원전` 블록이다.

---

## 1. `INDEX.md` — 붙일 위치: `## 🤖 MLIP 방법론 — **우리 UMA 스택을 재는 축**` 표 (line ~383 이하)

| `papers/maginn2019_best_practices_transport_selfdiffusivity_viscosity.md` | **[외부·methods·고전MD 규약 원전·⛔물성 4축 아님·★★MD 통계 불확실도 축의 정본]** **Edward J. Maginn\*** (Notre Dame) / **Richard A. Messerly\*** (NIST) / Daniel J. Carlson (BYU) / Daniel R. Roe (NIH) / **J. Richard Elliott** (Akron), "**Best Practices for Computing Transport Properties 1. Self-Diffusivity and Viscosity from Equilibrium Molecular Dynamics**" (***Living J. Comp. Mol. Sci.* 2019, 1(1), 6324**, DOI 10.33011/livecoms.1.1.6324, **[Article v1.0], 판본일 2019-01-06**, living document — 관리처 `github.com/ejmaginn/TransportCheckList`; 20 pp · Fig 13 · Table 1 · ref 61 · SI 없음). ⚠ **서지 정정: 5저자는 Anderson 이 아니라 Elliott 이다.** **질문**: EMD 로 뽑은 D·η 가 "힘장을 제대로 대표하는가(reliable)" 와 "남이 재현하는가(reproducible)" 를 실험 정확도와 분리해 어떻게 보장하나. **답 = 체크리스트 + 부트스트랩.** ★★ **우리 규약에 직접 걸리는 수치 5개**: ① **부트스트랩은 N_reps ≥ 20 에서 가장 신뢰**(§4.2.3), SEM ∝ 1/√N_reps, 복원추출 N_boots=N_reps, 수백 회 반복, **α=0.05 two-sided → 95 % CI**; ② **확산영역 게이트 = log-log MSD 기울기 ≈ 1** + **√MSD > r_G(하한) · > L/2(상한)**(§5.2.2) — ⚠ 저자는 "ergodicity" 라는 단어를 **한 번도 안 쓴다**(전문 0회); ③ **MSD 적합 구간은 "middle"** 이되 *"we are unaware of an objective approach for defining the 'middle' region"* — **수치 기준 없음**, 대신 **보고 3종 의무**(구간 선택법 · 그 선택이 만드는 D 변동폭 · 기울기 적합 불확실도, §5.2.3); ④ **유한크기 효과 유의** — CO₂ 에서 크기 따라 ≈10 %, 처리 = D vs N^(−1/3) 외삽 **또는** **Yeh–Hummer `D∞ = D(L) + k_BTξ/(6πηL)`, ξ = 2.837298**(입방 상자 + η 별도 계산 전제, 비입방은 다른 보정); ⑤ 복제 수 문헌값 **10개 ≈ 단일 장기런**(Ref 29) · **30–40 ≡ 100**(Zhang et al.) — ⚠ **셋 다 점도 맥락이고 D 에 대한 정량 N_reps 권고는 이 논문에 없다**. ⛔⛔ **§4.1.1 이 우리 Langevin 을 이름을 대서 경고**: 속도 스케일링 thermostat(Berendsen·stochastic rescaling·Nosé-Hoover)은 결합시간 0.1/1/10 ps 전 범위에서 NVE 와 구분 불가지만, **속도 무작위화 계열(Andersen, Langevin)은 강한 결합(τ = 0.1 및 1 ps)에서 D 를 극적으로 낮추고 η 를 높인다**(Basconi & Shirts). 권장 = **NVE > NVT ≫ NPT(강한 비권장)**. 기타 규약: Einstein D 는 생산런에 **≈1000 배치** 저장 · GK 는 속도 **4–5 fs** · 응력텐서 **5–10 fs** · **unwrapped 좌표 필수**(아니면 D 과소) · 원자좌표보다 **분자 COM** 권장 · η 는 D 보다 **10배 데이터** 필요 · 필요 런 길이 ≈ plateau time × 10 · EMD 적용한계 η < 20×10⁻³ Pa·s. **🔑 우리 figure-read 5장**(`Fig. 1`·`2`·`3`·`9`·`13`, 나머지 8장은 점도 전용이라 미열람): ★ `Fig. 13` = **Einstein η 의 (시작,끝) 창 히트맵** — **N_reps=1 이면 컬러바가 −0.2 ~ 0.6 ×10⁻³ Pa·s(음의 점도까지!) 인데 N_reps=30 이면 0.31 ~ 0.37** ⇒ **창 민감도가 ≈13배 축소**. **"창을 어떻게 고르나" 는 "복제를 몇 개 돌리나" 와 분리된 질문이 아니다** — 이 논문에서 우리에게 가장 이식 가치 높은 한 문장; `Fig. 3`(하) **N=10 에서 궤적길이 4종이 1.20–1.33 로 갈리고 N=20 에서 넷이 동시에 1.43–1.47 로 튄다** ⇒ **작은 N 의 "수렴처럼 보이는 공통 인공물"**; `Fig. 9` 단일런들이 250 ps 에서 **≈46 ~ >100 로 2배 이상** 벌어지고 30복제 평균만 직선. **⛔ 본문 서술과 어긋난 그림 2장**: `Fig. 1` — 본문 "≈10 %" 는 계산한 크기들 사이 산포일 뿐이고 **가장 작은 셀 vs D∞ 는 ≈15 %**(18.85 vs 22.2, figure-read), 게다가 **가장 작은 셀에서 YH 가 과보정**(22.85 > 평균선 22.25)하는데 본문은 "similar results" 로 뭉갠다; `Fig. 2` — 본문이 0→100 ps 를 *"ballistic"* 이라 부르지만 진짜 탄도영역은 sub-ps 이고 그림에 보이는 건 **케이지/아확산**이다 (**용어 오용**). **⛔ 범위 밖 4가지**: **힘장(모델) 오차 명시적 제외**(§4.2.3: *"we limit our discussion to random uncertainties"*) · **MLIP 특유 문제 전무**(2019년 고전 force field) · **이온전도도 σ 는 이 편에 없다**(Abstract 가 후속편 예고) · **결정 고체 이온전도체 예제 0건**(CO₂·ethanol·ethane·glyme·이온성액체·물·LJ 유체뿐) | **★★ 우리 MD 통계 불확실도 축의 정본 — 단 "통계"만.** 우리 규약 항목별 판정: **✅ 자유절편 OLS**(`Table 1` Einstein 식이 **미분형**이라 절편을 안 본다 — 원점강제가 오히려 위반) · **🟡 MSD 창 2–50 ps**(논문에 판정 수치가 없어 **정당화도 반박도 못 한다**. 요구되는 건 보고 3종인데 우리는 2개를 안 한다 — 특히 **창 효과 Ea 242 meV > 주장 효과 90 meV** 를 알면서 불확실도로 보고 안 하고 "규약 고정"으로 처리) · **⛔ 시드 3**(부트스트랩 문턱 ≥20 미달. **결정타: 시드 3의 복원추출 다중집합은 10가지뿐** ⇒ 수백 회 반복해도 이산 점 10개, CI 가 무의미) · **⛔ 확산영역 게이트 없음**(β 폐기 후 공백 — log-log 기울기 게이트는 **비용 0**, 기존 `msd_diffusive_check.py` 확장으로 즉시 가능) · **⛔ 유한크기 미점검**(단 **YH 식 직접이식 금지** — η 를 요구하고 유체역학 backflow 전제라 고체 골격계에 안 온다. 대신 **D vs N^(−1/3) 실측**은 그대로 유효) · **⛔⛔ Langevin τ ≈ 0.51 ps**(우리 `aimd_mlip.py:190` 이 `friction=0.02` 를 ASE 단위로 넘김 ⇒ γ ≈ 1.96×10⁻³ fs⁻¹ ⇒ **저자가 경고한 0.1–1 ps 대역 한복판**). ⚠ **비(ratio) 불확실도는 이 논문이 다루지 않는다** — digest §9 의 paired bootstrap 은 **우리 확장**임을 명시할 것. ⛔ **인용 금지 문장 2개**: *"Maginn et al. 이 2–50 ps 창을 권고한다"* / *"우리 창은 Maginn 규약을 따른다"* — 논문은 창 수치를 주지 않는다. §6.3.1 의 *"5 to 50 ps"* 는 **점도(Einstein η)** 얘기이고 저자 스스로 *"less theoretically rigorous"* 라 깎은 대목이라 **숫자 일치는 물리적 관련이 없다** ⛔ 물성 A–I 축 해당 없음 |

---

## 2. `comparison_vs_ours.md` — 절 초안

### 2-a. `## 📑 Reference key` 표에 추가할 행

| **[Maginn19MD]** ★★ | **E. J. Maginn\***/**R. A. Messerly\***/D. J. Carlson/D. R. Roe/**J. R. Elliott** 2019 ***Living J. Comp. Mol. Sci.* 1(1), 6324** (Notre Dame + **NIST** + BYU + NIH + Akron; DOI 10.33011/livecoms.1.1.6324; **[Article v1.0], 2019-01-06**; LiveCoMS **living document** — 인용 시 버전 필수) — "**Best Practices for Computing Transport Properties 1. Self-Diffusivity and Viscosity from Equilibrium MD**". **EMD 로 D·η 를 뽑을 때의 체크리스트 원전.** 우리에게 걸리는 축 = **MSD 적합 구간 · 독립 복제 수 · 부트스트랩 CI · 확산영역 게이트 · 유한크기 · thermostat 선택**. ⛔ **고전 force field 기준 · 분자 액체 예제만 · 힘장 오차는 명시적 범위 밖 · 이온전도도는 후속편 예고** | ✅ `papers/maginn2019_best_practices_transport_selfdiffusivity_viscosity.md` | **규약 원전 (물성값 0건) — 방법 원전 전용, 축 A–I 제외** |

### 2-b. `### J-7. 🔧 방법 원전` 블록에 추가

**[Maginn19MD] `maginn2019_best_practices_transport_selfdiffusivity_viscosity` — 우리 D 의 *통계* 불확실도를 정의하는 원본**

> ⛔ **σ·Ea·D·ESW·탄성·gap 0건.** 여기 있는 것은 우리 `Ea 0.197 ± 0.032 eV` 의 **±0.032 가 무엇인가**를 정의하는 원본이다.
> ⛔ **형제 4편(#78–81)과 재는 양이 다르다**: 저 넷은 **모델(epistemic)** 분산, 이 편은 **궤적 유한성(random)** 분산.
> **복제를 무한히 늘려도 모델 편향은 안 줄어든다** — 논문 §4.2.3 첫 문단이 힘장에 대해 직접 그렇게 쓴다.

| 항목 | [Maginn19MD] | 우리 | 판정 |
|---|---|---|---|
| **MSD 적합 구간** | *"only the **middle**"* · 단시간(케이지)·장시간(잡음) 배제. **⛔ 수치 기준 없음** — *"we are unaware of an objective approach"*. 대신 **보고 3종**: 선택법 · **그 선택이 만드는 D 변동폭** · 기울기 적합 불확실도 | **2–50 ps 고정 · 자유절편 OLS** | 🟡 **절반**. 취지 일치·자유절편 ✅. 그러나 **변동폭을 안 보고한다** — 우리는 그 값을 이미 안다(**창 효과 Ea 242 meV**, `tools/convention_check.py` · `kb/concepts/msd_reading.md`) ⇒ **242 meV > 주장 효과 90 meV** 인데 규약 고정으로 처리했다. ⛔ **논문을 우리 창의 근거로 인용하면 오독** |
| **자유절편 vs 원점강제** | `Table 1`: `D = (1/2d_α) lim (d/dt)⟨MSD⟩` — **미분형** | 자유절편 OLS `MSD = c + 6Dt` | ✅ **직접 방어된다.** 도함수는 절편을 안 본다 ⇒ `MSD/(6t)` 원점강제가 규약 위반 (2026-08-11 β 게이트 사태의 뿌리와 같은 병) |
| **독립 복제 수** | 부트스트랩 **N_reps ≥ 20** 에서 최신뢰 · SEM ∝ 1/√N · **10 ≈ 단일 장기런** · **30–40 ≡ 100**(점도) | **시드 3** | ⛔ **미달.** 산술 결정타: **시드 3 → 복원추출 다중집합 10가지** ⇒ "수백 회 반복" 해도 분포가 아니라 이산 점 10개. **논문식 복제 부트스트랩은 시드 3에서 실행 불가.** ⚠ 완화: 저자가 *"even if only a few"* 를 허용(단 *rough estimate* 로 부를 것) + D 는 **N 분자 평균**이 가능해 η 보다 정밀(§4.2.1) — ⛔ 그래도 **분자 평균은 복제를 대체 못 한다**(같은 궤적·같은 열욕·같은 무질서 배열 = 독립 표본 아님) |
| **확산영역 진입 판정** | ① **log-log MSD 기울기 ≈ 1** ② **√MSD > r_G(하한) · > L/2(상한)** (⚠ 문서 내 세 곳이 L/2 · "~L" 로 불일치) ③ 점점 긴 런 계열로 D 변화 확인. **"ergodicity" 단어 0회** | **β 게이트 폐기 후 공백** | ⛔ **가장 큰 구멍이자 가장 싼 수리.** ①은 **비용 0** — 기존 MSD 로그에서 계산. ⭕ **처방(T1)**: `tools/ionic/msd_diffusive_check.py` 에 `slope_2_50ps` 한 열 추가 (**새 파일 금지** — 기존 도구 확장). ②는 r_G 가 단원자 Li 에 없어 **그대로 못 온다** → 하한을 Li–Li 최근접/점프거리로, 상한을 L/2 로 치환 ⚠ **이 치환은 우리 판단이지 논문 권고가 아니다** |
| **유한크기 효과** | **"significant … must be accounted for"**. CO₂ ≈10 %. ① D vs N^(−1/3) 외삽 ② **YH `D∞ = D(L)+k_BTξ/(6πηL)`, ξ=2.837298** (입방 + η 별도) | **점검 0회** | ⛔ **명시적 결손.** 단 **YH 직접이식 ❌**: 식이 η 를 요구하는데 결정성 SE 의 "전단점도" 는 잘 정의되지 않고, 보정의 물리가 **유체역학 backflow** 라 골격이 운동량을 흡수하는 우리 계에 전제가 안 선다. ⭕ **처방(T2)**: 600 K 에서 host·design 각각 **2×2×2 / 3×3×3** 두 크기만 → 목표는 D∞ 가 아니라 **D_rel 이 크기에 둔감한지** 확인 |
| **thermostat** | **NVE > NVT ≫ NPT.** 속도 스케일링(Berendsen·SR·NH)은 τ 0.1/1/10 ps 전 범위에서 NVE 와 구분 불가. ⛔ **속도 무작위화(Andersen·Langevin) + 강결합(τ = 0.1 및 1 ps) → D 극적 감소·η 증가** | **Langevin NVT, `friction=0.02`(ASE 단위) ⇒ τ ≈ 0.51 ps** | ⛔⛔ **이름을 대서 경고받은 조합.** ⚠ 근거는 **분자 액체** 기준이라 고체 hopping 으로의 전이는 미검증. ⚠ 우리 보고량이 **비**라 곱셈 편향이 상쇄될 여지가 있으나 **증명된 적 없다**. ⭕ **처방(T3, 최저비용)**: 600 K 에서 γ = 0.002/0.02/0.2 **대조 잡** — D 는 움직이는데 **D_rel 이 안 움직이면** 상쇄 가정이 실측으로 뒷받침된다 |
| **런 길이** | §4.3: **점점 긴 런의 계열**로 D 가 변하는지 본다. `Fig. 4`: **느린(저온) 계일수록 창을 늘려야** | prod 200 ps(600 K) / 100 ps(800·1000 K), 창은 **양쪽 다 2–50 ps** | 🟡 **판정 불가 — 점검을 안 했다.** ⚠ 800/1000 K 에서 상한 50 ps 는 **런의 T/2** (⚠ `lag ≤ T/4` 는 **우리 kb 관례**이지 이 논문 규칙이 아니다 — 논문의 "절반 이하"는 §5.3.2 의 *GK 시간원점 lag* 얘기다) |
| **시간원점 다중화** | 식 정의의 일부(`⟨…⟩_{t₀}`). 전제: **δt₀ > 상관시간** | 하고 있다 (`msd_origin.py`) | ✅ 축은 있다. ⚠ **δt₀ > 상관시간 확인 기록이 없다** |
| **3차원 평균의 덤 진단** | `D = ⅓(D_xx+D_yy+D_zz)`, **세 성분 산포 = crude 불확실도**, 비대각 ≈ 0 확인 | 평균은 하되 **산포를 안 본다** | ⭕ **공짜 진단 미수확 (T0)** — 후처리만으로 시드 3에서도 즉시 얻는 불확실도 하한 |
| **비(ratio) 의 불확실도** | ⛔ **다루지 않는다** (비·상대확산 언급 0건) | 보고량 = `D_rel = D*(design)/D*(host)` @600 K | ⚪ **논문 밖.** digest §9 의 **paired bootstrap**(design·host 에 같은 시드 집합 `S_b` 를 적용해 매 반복 `R_b` 를 만들고 2.5/97.5 백분위) 은 **§4.2.3+§6.3.1 의 우리 확장**이며 그렇게 표기해야 한다. 독립 가정 오차전파는 **공통 성분을 두 번 세어 CI 를 과대추정**한다. ⚠ 짝짓기 전제 = design 시드 k ↔ host 시드 k 대응 (`aimd_mlip.py` 는 `seed = args.seed + T_K` — 같은 `--seed` 로 돌렸는지 **미확인**) |
| **창 민감도 × 복제 수** | `Fig. 13` figure-read: N_reps 1 → 30 에서 **창이 만드는 산포 ≈0.8 → ≈0.06 ×10⁻³ Pa·s (≈13배 축소)**. 단일런에서는 **음의 점도**까지 나온다 | 창 고정 + 시드 3 | ★★ **이 논문의 최대 소득.** *"창을 어떻게 고르나"* 와 *"복제를 몇 개 돌리나"* 는 **한 질문**이다. ⭕ **처방(T4)**: 창 자체는 두고 **시간구간 부트스트랩**(§6.3.1) 을 MSD 에 이식 — start ∈ [1,10] ps, end ∈ [30,60] ps 를 수백 회 무작위 추출해 **D_rel 분포**를 내고 2.5/97.5 백분위 보고. **새 MD 0회, 후처리만.** ⚠ 그 CI 는 "통계 + 창 선택" 합산폭이므로 그렇게 이름 붙일 것 |

**⛔ 이 축에서 인용하면 안 되는 것 (`J-6` 에도 반영 권장)**
- *"Maginn et al. 이 2–50 ps 창을 권고한다"* / *"우리 창은 Maginn 규약을 따른다"* — **거짓.** 논문은 창 수치를 주지 않는다.
- §6.3.1 의 *"5 to 50 ps"* 를 우리 2–50 ps 의 방증으로 쓰기 — **점도(Einstein η)** 얘기이고 저자가 *"less theoretically rigorous"* 라 깎은 관행이다. 숫자 일치는 물리적 관련이 없다.
- *"YH 보정을 적용했다"* — 우리 계에 적용 불가(위 표 참조).
- *"Maginn 규약대로 σ 를 냈다"* — **이온전도도는 이 편에 없다** (후속편 예고만).
- 시드를 늘려 CI 가 좁아진 것을 *"D 가 정확해졌다"* 로 쓰기 — 좁아지는 건 **통계 축뿐**이다.

### 2-c. `## H. ⚠️ 우리가 아직 못 하는 것 (정직 목록 → 향후)` 에 추가할 행 3개

| gap | 누가 필요로 함 | 보강책 |
|---|---|---|
| **⭐ D 의 확산영역 게이트가 없다** (β 폐기 후 공백) | **[Maginn19MD]** §5.2.2 — **log-log MSD 기울기 ≈ 1** 과 **√MSD > L/2** 를 확산영역 판정의 조건으로 요구 | **비용 0.** 기존 `tools/ionic/msd_diffusive_check.py` 에 `slope_2_50ps` 한 열 추가(새 파일 금지). 이게 없으면 "2–50 ps 가 확산영역이다" 라는 **전제 자체가 미검증**이고, 그 위의 Ea·D_rel 은 전부 그 전제에 얹혀 있다 |
| **⭐ MSD 창 선택이 만드는 D_rel 변동폭을 보고하지 않는다** | **[Maginn19MD]** §4.2.2·§5.2.3 — *"critical to quantify the degree of variability … that arises from assumptions in the data analysis, e.g., the time interval over which the Einstein slope is computed"* | 우리는 **절대 Ea 의 창 효과 242 meV** 를 안다(원장). **그런데 보고량인 `D_rel` 의 창 민감도는 잰 적이 없다** — 242 meV 는 D_rel 에 그대로 옮겨오지 않는다(비에서 상쇄될 수 있다). ⇒ **시간구간 부트스트랩(§6.3.1 이식)으로 `D_rel` 의 창 CI 를 내는 것이 최우선**. 새 MD 0회 |
| **⭐ D 의 유한크기 의존을 한 번도 안 봤다** | **[Maginn19MD]** §5.1.2 — D 의 크기 효과는 **"significant … must be accounted for"**, CO₂ 에서 ≈10 %(figure-read 로는 최소 셀이 D∞ 를 **≈15 % 과소**) | ⛔ **YH 식 이식 금지**(η 요구 + 유체역학 backflow 전제 → 고체 골격계에 전제 불성립). ⭕ 논문의 **첫 번째 방법**은 그대로 유효: 600 K 에서 host·design 을 **2×2×2 / 3×3×3** 두 크기로. 목표는 D∞ 가 아니라 **`D_rel` 이 크기에 둔감함을 보이는 것** — 그것만 보이면 우리 보고량이 방어된다 |

### 2-d. (선택) `J-11` 을 신설한다면

형제 4편 pending 이 이미 제안한 대로 `J-11. 불확실도` 를 만든다면, 절 머리에 **두 축 분리 선언**을 박아 둘 것:

> **J-11 은 두 축이다. 섞으면 틀린다.**
> · **통계(random) 축** — 궤적이 유한해서 생기는 요동. 정본 = **[Maginn19MD]**. **복제·시간원점·창 선택**으로 줄어든다.
> · **모델(epistemic) 축** — MLIP 가 틀려서 생기는 편향. 정본 = **[Imbalzano21] · [Carrete23UQ] · [Kurniawan25] · [Grasselli25]**. **복제로는 안 줄어든다.**
> 우리 `Ea 0.197 ± 0.032 eV`(modelc 600 K 3-seed) 의 **±0.032 는 통계 축이고, 모델 축 추정치는 우리에게 아예 없다.**

---

## 3. `properties/` 갱신

해당 없음 — 이 논문은 물성값을 만들지 않는다. **`db/` 는 이번 실행에서 건드리지 않았다.**

---

## 4. 🎤 talk 역링크

**해당 없음** — `litdb/talks/*.md` 의 인입 대기열(`lee2026_skku_mlip_materials_design.md`)에서 이 논문을 찾지 못했다 (`grep -i "maginn|best practices|livecoms"` 0건).
