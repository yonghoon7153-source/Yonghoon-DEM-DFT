# ⏳ pending — `lomeli2024_predicting_reactivity_passivation_ssb_interfaces` 의 INDEX / comparison 반영분

> ⛔⛔ **번호 충돌 — 2026-09-22 정정.** 이 파일은 `§J-37` 을 잡았는데, 고른 직후
> **`chaney2024` 가 J-37 로 먼저 병합됐다**(커밋 `4a5b3faea`). 그래서 본문의 번호를
> `J-〈병합자 배정〉` 으로 비워 뒀다.
> **병합자는 `comparison_vs_ours.md` 에서 마지막 번호를 직접 확인하고 배정해라.**
> ⚠ 같은 시각에 `schwietert2021`·halide Na·antiperovskite 대기 파일도 번호를 고르고
> 있다 — **넣기 직전에 한 번 더 본다.** (이번 라운드에 번호 충돌이 **두 번** 났다:
> morgan2021 J-29→J-33, 그리고 이 건. 대기 파일이 여럿이면 선점이 어긋난다.)

> 2026-09-22, litdb-curator. **이번 세션은 `INDEX.md` · `comparison_vs_ours.md` · `db/literature/refs.json` 직접 수정 금지 + 커밋 금지** 지시라
> 아래 블록만 만들어 둔다. **조율 세션이 그대로 옮겨 붙이면 된다.**
> digest 본체: `litdb/papers/lomeli2024_predicting_reactivity_passivation_ssb_interfaces.md`
> 그림: `litdb/figures/lomeli2024_predicting_reactivity_passivation_ssb_interfaces/` (**PNG 14장** = 본문 `Fig. 1`–`4` + `Table 1`·`Table 2` + SI `Fig. S1`–`S7`)
>
> ## 📌 §J 번호 배정 — **J-〈병합자 배정〉**
> `comparison_vs_ours.md` 를 직접 열어 확인했다: 마지막 번호는 **J-36** (`[Wang22Res]`, line 5270).
> J-33 morgan2021 · J-34 haruyama2014 · J-35 okuno2020 · J-36 wang2022 가 이미 차 있다.
> ⇒ **이 논문은 `J-〈병합자 배정〉` 로 잡았다.** 같은 라운드의 다른 에이전트(논문 7·8)와 충돌하면 조율 세션이 재배정해 주기 바란다
> (블록 제목과 상호참조 두 곳만 고치면 된다).
>
> ## ✅ 사전 점검 결과
> - **🎤 talk 역링크**: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `lee2026_skku_mlip_materials_design.md` 하나뿐이고,
>   그 대기열(MTP/SevenNet/GNoME/cryoTEM/BH₄/hydrolysis 계열 6건)에 **이 논문은 없다**. 또 `litdb/talks/` 전체에
>   `lomeli`·`Predicting Reactivity`·`passivation of solid` 검색 **0건**. ⇒ **역링크 작업 없음.**
> - **`litdb/properties/` 디렉터리가 존재하지 않는다** ⇒ properties 갱신 대상 없음.
> - **`--clean` 금지 지시를 지켰다.** 기존 `figures/<slug>/` 14장을 그대로 쓰고 재추출하지 않았다.
>   🔧 다만 결함 1건을 기록해 둔다 — **`fig_S2.png` 와 `fig_S3.png` 가 바이트 동일**(md5 `599b637dca29cc505ae4e09ee051b066`).
>   SI 4쪽에 `Fig. S2`(산점)와 `Fig. S3`(pDOS 10패널)가 같이 있는데 추출기가 같은 bbox 를 두 번 썼다.
>   ⇒ **SI 4쪽을 통째로 재렌더해 둘 다 실독**했고, 파일은 지시대로 건드리지 않았다. 다음 재추출 때 고칠 자리다.
> - **SI2 xlsx 를 실제로 열었다** — `openpyxl` 은 **strict OOXML** 이라 `sheetnames == []` 를 준다.
>   `zipfile` + `xml.etree.ElementTree` 로 직접 파싱했다. 결과는 digest §3f·§3g 전수.

---

## ① `litdb/INDEX.md` — **`## ✅ Digest 완료 (paper-level)`** 표에 추가할 행

> 표 머리 확인함: **`| slug | 논문 | 축 |`** (3칸, line 18–19). 아래 행도 **정확히 3칸**이다.

```markdown
| `papers/lomeli2024_predicting_reactivity_passivation_ssb_interfaces.md` **(본문 11 pp + SI 8 pp + SI2 xlsx 3535행 통합)** | **[외부·음극(Li 금속)측 스크리너·🟡선점 = 인접 · ⛔⛔ 아르지로다이트 0회 → A–D 물성 4축 진입 금지 · ★★ "부동태화를 무엇으로 판정하나" 의 실패 사례이자 이식 가능한 기법 원전]** **Eder G. Lomeli\***/B. Ransom/A. Ramdas/D. Jost/B. Moritz/**Austin D. Sendek\***/**Evan J. Reed**(2022-03 별세)/**Thomas P. Devereaux\*** (**Stanford MSE + SLAC SIMES + Geballe Lab**), "**Predicting Reactivity and Passivation of Solid-State Battery Interfaces**" (***ACS Appl. Mater. Interfaces* 2024, 16, 51584–51594**, DOI `10.1021/acsami.4c06095`; **CC-BY-NC-ND 4.0**; DOE-BES; Sherlock + NERSC BES-ERCAP0027203; `Fig. 1`–`4` + `Table 1`–`2` + `Fig. S1`–`S7` + `Table S1`–`S2` + **SI2 xlsx**). **구조 = ① Li 금속‖SSE 계면 67종 AIMD(550 K · 40–60 ps · <150원자 · Γ-only · 계당 1회) → ② 눈으로 `stable/passivating/reactive` 3분류 → ③ 로지스틱 회귀 2개(SM·RM, Sendek 22 서술자) → ④ MP 3535 구조 외삽.** 결과 **stable 533 · passivating 788 · reactive 2214** (기존 `|ΔE_rxn|<100 meV/atom` 기준은 **229**). **★ 보고량 = `Norm. MSD`** = 계면수직 1D MSD 를 *원래 계면평면을 넘은 sublattice(비-Li) 원자*에 대해 평균하고 **SE 두께로 나눈 것 (단위 Å)** — 문턱은 stable **<0.05**(근거 문장 없음) · 원자 반응판정 **0.5 Å²**(= **1937년 Zn X선 논문** ref 19 의 열진동 0.1 Å² 의 5배) · **passivating↔reactive 경계는 숫자가 없고 `Fig. 1` 캡션이 *"by inspection of the simulation cells"* 라 적는다**(`figure-read ≈0.31`). **⛔⛔ `Li₆PS₅Cl` 은 훈련셋·검증셋·3535 목록 **어디에도 없다** — `argyrodite` **0회** · `Li6PS5` **0회**.** 가장 가까운 대리값: **`Li₆PS₅I` mp-950995/mp-985582 reactive(예측)** · **`Li₅P(S₂Cl)₂` mp-1040450 reactive(예측)** · **`Li₇PS₆` mp-1211324 reactive(예측)** · **`Li₃PS₄` `Norm.MSD` 0.819 / `Li₇P₃S₁₁` 0.911 / `Li₁₀GeP₂S₁₂` 0.552 = 전부 AIMD reactive**. **⭐⭐ 우리 0 V 분해산물이 전부 "Li 금속에 stable"**: `Li₂S`·`Li₃P` **AIMD 직접 확인**, `LiCl`·`Li₂O` 예측, +`Li₃N` AIMD — **[Wang22Res] 와 정확히 짝**(*산물은 더 반응하진 않지만 붙지도 통하지도 않는다*). **⭐ B₂O₃ 축 참조값**: `Li₃BO₃` mp-27275 **stable** · `Li₆B₄O₉` **stable** · `LiBO₂`×2 · `Li₂B₄O₇` · `LiB₃O₅`×2 **passivating**. **⭐ 코팅 축**: `Li₂ZrO₃`·`LiAlO₂`×2 **stable**, `LiNbO₃` 는 🔴 **stable 1 + passivating 8**(다형별로 갈림), `Li₃PO₄` 는 🔴 **mp-13725 stable / mp-2878 passivating (둘 다 orthorhombic)**. **★★ 이 digest 의 자체 생산물 3건**: ⓐ **훈련셋 50종 `Norm. MSD` 전수 복원**(논문·SI·xlsx 어디에도 숫자가 없다 — `Fig. 1` 막대 + `Fig. S2` 산점 축보정 픽셀판독, 두 그림 ±0.005 일치로 검증) ⓑ **`Fig. 1` y축이 1.0 에서 잘렸고 상위 3계 진값이 `LiBiF₄` 1.058 · `Li₂GePbS₄` 1.118 · `LiGaCl₃` **1.547** 임을 `Fig. S2` 로 복원**(논문 미고지, `LiGaCl₃` 는 55 % 가 잘렸다) ⓒ **xlsx 3535행 직접 파싱**(openpyxl 불가 — strict OOXML ⇒ zipfile+ElementTree). **🔴 핵심 비판 8건**: ① **CV 6–8 % 는 성능이 아니라 선택된 최솟값** — 22특징 × N=1..10 전수조합 = ✎ **1 744 435 개 모델**을 **50점** 위에서 채점하고 최솟값 보고(50점에서 CV 양자 = 1/50 = 0.02), 증거는 `Fig. 2b` 의 N=3–6 평평 0.08 → N=7 0.06 → N=8–9 다시 0.08(**훈련점 1개 진동**)과 `Table S2` 의 **SPF 계수 0.042 = ΔE_rxn 의 1/51 인 특징이 "최적 7개"에 포함**. **정직한 숫자는 홀드아웃 35.3 % 하나** ② **`L_SSE` 정규화가 부동태 지표로 방향이 반대** — 반응전선이 고정깊이에서 멈추면 분모만 커져 **SE 를 두껍게 할수록 reactive→passivating** 으로 이동(저자도 *"큰 셀에서는 passivating 일 수 있는데 셀이 작아 reactive 로 찍는다"* 고 자인하나 원인을 자기 정규화로 짚지 않는다) ③ **`NaLiSe` 가 `Table 1`=passivating 인데 `Fig. 1`·`Fig. S2` 색은 navy=reactive**(훈련 구성이 19/10/21 인지 19/9/22 인지 불명) ④ **검증셋이 무작위가 아니다**(*"we chose materials predicted to be good Li ion conductors"*, 10/17 별표) + **`ΔE_rxn` 단독 기준선을 그 홀드아웃에서 재보지 않았다** ⇒ *"3–4배 개선"* 은 **CV 대 CV** 뿐 ⑤ **오류 6건 중 3건을 "그래도 쓸 만"으로 사후 재분류해 17.6 % 로 다시 적는다**(결과 보고 채점표 수정) ⑥ **상태 선택 규칙 0** — `Li₆FeCl₈`(논문 스스로 *"Fe states at E_F"*)·LiMnPO₄·Li₃Fe₂(PO₄)₃ 등 **열린 껍질·산화환원 활성** 계인데 **스핀·자화·NUPDOWN 선언 0**("+U 를 켰다"는 상태선언이 아니다) ⑦ **다형 집계 규칙 0** — ✎ **87개 조성이 다형에 따라 반대 라벨** ⑧ **본문 히스토그램 서술이 xlsx 원자료와 100–125 meV/atom 어긋난다**(본문 *"300 / 750"* vs ✎ 실제 최빈 **400 / 625**). **서지·표기 오류 10건**: ref 40 PBE 를 **exchange-correlation *hole*** 논문(Perdew–Burke–**Wang** PRB 54, 16533)으로 인용 · **ref 8 ≡ ref 35 중복** · *"100 **eV**/atom"* · *"**Li₆WN₂**"*(실제 Li₆WN₄) · `Table 2` 각주 *"10⁻⁴ **mS/cm**"*(S/cm, 1000배) · *"LiB₁₂**CP**"* ↔ *"LiB₁₂PC"* · `Fig. S6` 캡션이 **존재하지 않는 "Figure 5d"** 를 가리킴 · `Fig. S2` 캡션 *"ΔE_formation"*(축·본문은 ΔE_rxn) · 후보 필터가 **50 / 100 / 100 meV/atom 세 번 다름** · **SM/RM 약어 의미가 Results 와 Methods/Conclusion 에서 뒤바뀌고 `Table S2` 는 세 번째 이름("Passivating Model")** · `Fig. 3` 에서 **(a,b) 와 (c,d) 의 teal/gold 색 규약이 뒤집힘**. **⛔ 0회 목록**: 양극 계면(`cathode` 1회 = 향후과제) · 두께 · self-limiting · 전자전도도 수치 · ASR/impedance/SEI/interphase · grand-potential/ESW · NEB/Bader/COHP/ELF/phonon/탄성/BVSE · 접합일·표면에너지 · 무질서/SQS · 시드/오차막대/불확실도. **🔑 우리 접점 4**: (i) **반응영역 분리 기법**(양쪽 계면 주기셀 + 중간면 정의 + 계면수직 MSD + **sublattice 만 세기** + unstable 이면 넘어온 Li 포함)은 **그대로 이식 가치 — 단 `L_SSE` 정규화를 버리고 `L_reacted(t)` [Å] 로 바꾸고, 시간점 ≥3 · SE 두께수렴 · 상별 PDOS 공간투영을 붙여야** 진짜 부동태 지표가 된다 (ii) **xlsx 3535행이 우리 산물·코팅·도펀트의 Li-금속 반응성 외부 참조표** (iii) **`Li₃P`·`Li₃N` 이 `E_G > 1.5 eV` 필터에서 탈락한 것이 우리 `sei_electronic.json` 서열(Li₃P 0.7092 eV = conductor-LEAK)의 외부 방증**(절대값 방증 아님) (iv) **Sendek 22 서술자가 [Zhao21HECS](J-17) 와 같은 표현 계열** — 같은 표현으로 타깃 둘(BVSE Ea / 계면 반응성)을 다룬 실증. **🔴 우리에게 불리한 결론 3**: ① 우리 모체 계열이 AIMD reactive 상위권(`Li₃PS₄` 45/50 · `Li₇P₃S₁₁` 47/50) + ✎ **황화물 169종 중 stable 5종(3.0 %) = 기저율 15.1 % 의 1/5** ② **그들 안정성 서술자(작은 AAV · 높은 sublattice 이온성 · 좁은 SLPW)가 우리가 σ 를 위해 고르는 방향과 정확히 반대**이고 논문이 그 트레이드오프를 직접 적는다 ③ ✎ **염화물 120종 stable 11.7 % / reactive 78.3 %** (질화물은 stable 49.7 % = 기저 3.3배) — ⛔ MP 후보 편향이라 경향만. **그림 14장 중 7장 실독**(`Fig. 1`(+좌/우 2배 확대 재렌더)·`Fig. 2`·`Fig. 3`·`Fig. S2`·`Fig. S3`·`Fig. S4`·`Table 2`(이미지 표 → 전사, 같은 크롭에 `Fig. 4` 동봉)); **안 본 것 = `Fig. 4`(tab_2 안에서 봄)·`Fig. S1`·`Fig. S5`·`Fig. S6`(xlsx 직접계산이 더 정확)·`Fig. S7`·`Table 1`(PDF 텍스트 전사)**. 🔧 도구 결함 1건: `fig_S2.png` ≡ `fig_S3.png` 바이트 동일(추출기 bbox 중복) → SI 4쪽 재렌더로 우회, `--clean` 금지라 파일은 그대로 둠 | **🟡 선점 = 인접(음극측 스크리너 · 우리 4축과 중복 0) · ⛔ A–D 물성 4축 진입 금지 · 판정은 §E 2행 + §H 1행 + §J-〈병합자 배정〉** — **부동태화 조작적 정의의 (실패한) 원전이자 이식 가능한 기법 원전** |
```

---

## ② `litdb/comparison_vs_ours.md` — **📑 Reference key** 표에 추가할 행

> 표 머리 확인함: **`| 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |`** (4칸, line 13–14).

```markdown
| **[Lomeli24]** 🟡 **선점 = 인접** · ⛔⛔ **아르지로다이트 0회 · `Li₆PS₅Cl` 이 3535 목록에 없다 → A–D 물성 4축 진입 금지** · ★★ **"부동태화를 무엇으로 판정하나" 의 유일한 정면 시도(그리고 그 실패 기록)** | **Eder G. Lomeli\***/B. Ransom/A. Ramdas/D. Jost/B. Moritz/**Austin D. Sendek\***/**Evan J. Reed**/**Thomas P. Devereaux\*** (**Stanford MSE + SLAC SIMES + Geballe Lab**) 2024 ***ACS Appl. Mater. Interfaces* 16, 51584–51594** (DOI `10.1021/acsami.4c06095`; 접수 2024-04-14 / 수정 2024-09-01 / 수락 2024-09-03 / 게재 2024-09-15; **CC-BY-NC-ND 4.0**; **DOE-BES**; Sherlock(Stanford) + **NERSC BES-ERCAP0027203**; 본문 11 pp · SI 8 pp · **SI2 xlsx 3535행** · refs 44 · 본문 그림 4 + 표 2 · SI 그림 7 + 표 2) — "**Predicting Reactivity and Passivation of Solid-State Battery Interfaces**". **음극(Li 금속)측 고속 스크리너**: Li‖SSE 계면 **67종 AIMD**(VASP·PBE·**+U(TM만)**·**500 eV**·**Γ-only**·NVT Nosé–Hoover·**550 K**(녹으면 400 K, 대상 미공개)·**dt 2 fs**·**40–60 ps**·**<150 원자**·≈8×8×40 Å³·**계당 1회·시드 0·오차막대 0**) → 눈으로 3분류 → **로지스틱 회귀 2개**(scikit-learn L2/LBFGS, Sendek 22 서술자, 5-fold Stratified CV, **N=1..10 전수조합**) → **MP 3535 구조** 외삽. **보고량 = `Norm. MSD`**(계면수직 1D MSD / 계면교차 sublattice 원자 평균 / **SE 두께로 정규화**, 단위 **Å**). 소환값: **stable 533 · passivating 788 · reactive 2214** (기존 `\|ΔE_rxn\|<100 meV/atom` = **229**; ✎ 우리 검산 `\|E_rxn\|<0.1` 이 **180+31+18 = 229** 로 정확 일치 ✓) · 홀드아웃 17종 **오분류 35.3 %**(random 63.7 · baseline 58.2) · CV **SM 8 % / RM 6 %** · `ΔE_rxn` 단독 CV **22 % / 26 %** · 붕소화물 **LiB₁₃C₂ D_vac 8.19e−5 → σ 1.30e−3 S/cm** · **LiB₁₂PC 2.69e−5 → 4.43e−4 S/cm**(**둘 다 c_vac = 0.05 % *가정*, 300 K 외삽**). ⛔ **ESW·grand-potential·NEB·Bader·COHP·ELF·포논·탄성·BVSE·접합일·표면에너지·두께·전자전도도 수치·ASR — 전부 0회.** 🔴 **비판**: **CV 6–8 % 는 ✎ 1 744 435 조합 × 50점에서 고른 최솟값**(CV 양자 1/50 = 0.02; `Table S2` 의 SPF 계수 **0.042**가 "최적 7개"에 포함) · **`L_SSE` 정규화가 부동태 지표로 방향이 반대**(SE 를 두껍게 하면 reactive→passivating) · **`Fig. 1` y축 1.0 클리핑**(✎ 진값 1.058/1.118/**1.547**) · **`NaLiSe` 라벨이 표↔그림 불일치** · **검증셋이 다른 모델 예측으로 편향 선택** · **오류 3건 사후 재분류로 17.6 % 재보고** · **스핀·다형 집계 규칙 0** · 서지·표기 오류 10건 | ✅ `papers/lomeli2024_predicting_reactivity_passivation_ssb_interfaces.md` (2026-09-22; **그림 14장 중 7장 실독** + `Fig. 1` 좌/우 2배 확대 재렌더 + `Table 2` 이미지표 전사 + **SI2 xlsx 3535행 직접 파싱**). 판정은 **§E 2행 + §H 1행 + §J-〈병합자 배정〉**. ⛔ A–D 4축 진입 없음 | **계산 100 %** (AIMD 67계 + 로지스틱 회귀 스크리너 · 실험 0 · **아르지로다이트 0**) · 외부 |
```

---

## ③ `litdb/comparison_vs_ours.md` — 본문 블록 3개

### ③-1. **§E. 환원 / 음극(Li 금속) 계면** 표에 추가할 **2행**

> 표 머리 확인함: **`| 주장 | 출처 | 우리 | 일치 |`** (4칸, line 858–859).

```markdown
| **⭐⭐ 🆕 아르지로다이트의 0 V 분해산물 3형제가 *Li 금속과 더 반응하지는 않는다* — 독립 AIMD 확인** (2026-09-22 신설) — 550 K·40 ps Li‖SSE AIMD 에서 **`Li₂S` 와 `Li₃P` 가 `stable`**(`Fig. 1` 의 cyan 막대, `Norm. MSD` figure-read ≈**0.03**, 문턱 0.05), **`Li₃N` 도 stable**; `LiCl`(mp-22905/mp-1185319)·`Li₂O`(mp-1960) 는 스크린 **stable 예측**. 세 계의 `ΔE_rxn` = **0.000 / 0.000 / −0.0205** | **[Lomeli24]** `Table 1`·`Fig. 1`·SI2 xlsx `stable_materials` 시트 (VASP·PBE·+U(TM만)·**Γ-only**·**<150 원자**·**계당 1회**) | `db/properties/sei_products.json` / `anode_interface_b2o3.json` 는 **어떤 상이 생기나**까지만 답한다 — *"그 상이 Li 금속과 더 반응하나"* 칸이 **비어 있었다** | ⭕⭕ **칸이 채워진다 + [Wang22Res] 와 짝이 맞는다.** 쓸 수 있는 문장: ***"아르지로다이트의 분해산물은 Li 금속과 더 반응하지는 않는다([Lomeli24] AIMD). 문제는 그 산물이 Li 금속에 붙지 않고(W_adh 0.045–0.675 J m⁻², 두 문턱 다 미달) Li⁺ 를 통과시키지 않는다는 것이다([Wang22Res] 400 K D\* 1.8e−9 ~ 3.0e−6 cm²/s)."*** — **서로 다른 두 그룹의 독립 계산**이다. ⚠ **`Li₃P` 에 축 이름을 반드시 붙인다**: 우리 `sei_products.json` 의 `conductor-LEAK`(갭 0.7092 eV)는 **전자누설 축**이고 여기 `stable` 은 **화학반응성 축**이다 — **모순이 아니라 다른 양**이고, 축 없이 같은 문장에 쓰면 독자가 뒤집어 읽는다 |
| **🔴 🆕 우리 모체 계열(황화물)이 이 스크리너에서 *부동태화조차 못 받고* 반응성 상위권이다 — 그리고 `Li₆PS₅Cl` 은 목록에 아예 없다** (2026-09-22 신설) — 550 K AIMD `Norm. MSD`(figure-read, 50종 중 순위): **`Li₃PS₄` 0.819 (45위)** · **`Li₇P₃S₁₁` 0.911 (47위)** · **`Li₁₀GeP₂S₁₂` 0.552 (37위)** — 셋 다 `reactive`. 스크린 예측: **`Li₆PS₅I` reactive**(mp-950995 −0.5486 / mp-985582 −0.5653) · **`Li₅P(S₂Cl)₂` reactive**(mp-1040450 −0.5966, **전 목록에서 유일한 Li–P–S–Cl 항목**) · **`Li₇PS₆` reactive**(mp-1211324 −0.5562). ✎ 화학군 통계: **황화물(S 포함·O 없음) 169종 중 stable 5종(3.0 %)** vs 기저율 15.1 % = **1/5** | **[Lomeli24]** `Fig. 1`(막대 픽셀판독)·`Table 1`·SI2 xlsx 전수 (⛔ **소환값**, 계당 AIMD 1회·시드 0·오차막대 0) | 우리 축 A 는 **벌크 σ·Ea** 이고 음극 계면 반응성 라벨은 **없다**. `db/properties/` 에 대응 항목 없음 | 🔴 **불리한 방향.** ⛔⛔ ***"이 논문이 `Li₆PS₅Cl` 을 reactive 로 분류했다" 고 쓰면 안 된다*** — **훈련셋·검증셋·3535 스크린 어디에도 없다**(`argyrodite` 0회·`Li6PS5` 0회). `Li₆PS₅I` 는 **두 다형 다 들어 있으므로 구조형 배제는 아니고**, 필터(`E_hull ≤ 100 meV/atom`, `E_G > 1.5 eV`) 중 하나에 걸렸거나 당시 MP 에 Cl 정렬항목이 없었던 것으로 보이는데 **논문이 이유를 안 밝혀 확인 불가**. ⚠ 그리고 더 불리한 것은 순위가 아니라 **서술자 방향**이다 — 그들 안정성 상관은 **작은 AAV(+0.616) · 높은 sublattice bond ionicity(−0.791) · 좁은 직선경로 SLPW(+0.621)** 이고, 이는 **우리가 σ 를 위해 고르는 것(열린 골격·넓은 채널·황화물)과 정확히 반대**다. 논문이 직접 적는다: *"a high packing fraction could lead to smaller and less accessible Li diffusion pathways … optimizing for both stability and conductivity will be key."* ⇒ **§A 의 "Cl-rich 가 빠르다" 를 음극 안정성 근거로 전용할 수 없다** |
```

### ③-2. **§H. ⚠️ 우리가 아직 못 하는 것** 표에 추가할 **1행**

> 표 머리 확인함: **`| gap | 누가 필요로 함 | 보강책 |`** (3칸, line 1002–1003).

```markdown
| **🔴🔴 ⭐⭐ 부동태화(passivation) 를 *조작적으로 정의한 적이 없다* — 그리고 이 논문으로도 안 메워진다** (2026-09-22 신설) | **[Lomeli24]** 가 이 질문을 **정면으로 시도한 유일한 편**이고 **부분적으로 실패했다**. 그들의 정의는 *"550 K·40 ps AIMD 후에도 SSE sublattice 골격이 유지되고 재배치가 **원래 계면 근처에만** 머무는 것"* = **공간적 국소성 하나**다. 그런데 ① **두께 0**(`thickness` 0회) ② **성장속도 0**(t=0 과 t=40 ps 두 점뿐) ③ **자기제한 0**(`self-limit` 0회) ④ **이온/전자 수송비 0** ⑤ **전자절연 기준은 시도했다가 포기** — `Fig. S3`(passivating 10) · `Fig. S4`(reactive 21) **전 패널이 E_F 에 유한 DOS** 이고 본문이 자인한다 *"all calculations depict an electronically conductive system, arising from **amorphous Li** in the high temperature computational cell."* ⑥ 결정적으로 **경계를 셀 크기가 정한다** — *"due to our **limited computational cell size** … we do not capture a passivating behavior that may be present at larger computational cell sizes. Hence we decide to predict these materials as **reactive out of caution**."* 우리 쪽 공백은 그대로다: `anode_interface_b2o3.json`·`sei_products.json` 은 **0 K 열역학 산물표**이고 **성장 동역학·두께·자기제한 판정이 없다** | **① 기법은 빌리고 정규화는 버린다.** 이식할 것 = **양쪽 계면 주기셀 + "원래 계면평면"=(바깥 SSE 원자 ↔ 금속 원자 중간면) + 계면수직 MSD + ⭐`sublattice(비-Li)` 원자만 세기 + unstable 이면 넘어온 Li 포함**. ⛔ **버릴 것 = `L_SSE` 정규화** — 반응전선이 고정깊이에서 멈추면(진짜 부동태) 분자는 상수인데 분모만 커져 **SE 를 두껍게 할수록 reactive→passivating 으로 이동한다**(저자가 인정한 셀크기 의존의 실제 원인이 이것이다). ⇒ **`L_reacted(t)` 를 Å 로 직접 보고.** **② 시간점 ≥3** — 부동태화의 정의는 `dL_reacted/dt → 0` 이고 두 점으로는 원리적으로 판정 불가. **③ SE 두께 수렴 시험**([Wang22Res] `Fig. S10` 형식) — *"전선이 셀을 다 먹었다"* 와 *"정말 반응성"* 을 가르는 유일한 방법. **④ 전자 기준은 *반응층에만* 공간투영** — 그들의 실패는 고칠 수 있다(셀 전체 DOS 대신 계면상 슬랩 PDOS, 또는 액체 Li 영역 배제). 우리는 이미 `sei_electronic.json` 에 산물별 갭이 있으므로 **상별 갭 + 연속성** 두 축으로 갈 수 있다. **⑤ 보고량 카드 먼저** (`kb/templates/estimand_card.md`) — 시드 집계·종단 선택·다형 집계 규칙을 **결과 보기 전에** 선언한다([Lomeli24] 가 셋 다 빠뜨렸다) |
```

### ③-3. **§J 새 블록 — `J-〈병합자 배정〉`** (⛔ A–D 물성 4축 표 아님)

> **왜 4축 표가 아닌가**: 이 논문의 "물성값" 은 **3분류 라벨**과 **붕소화물 2종의 σ**뿐이다.
> σ·ESW·탄성·gap 은 우리 계에 대해 **0건**이고, 가장 가까운 계(`Li₆PS₅Cl`)는 **목록에 아예 없다**.
> 행을 만들면 전부 `n/a` 다. ⇒ **`🔧 방법 원전` 블록**으로 둔다. 물성 판정은 **§E 2행**에서 한다.

```markdown
### J-〈병합자 배정〉. 🔧 **방법 원전 — [Lomeli24] "부동태화를 무엇으로 판정하나" 의 정면 시도와 그 실패 · 반응영역 분리 기법 · 스크리너 통계의 함정** (2026-09-22 신설)

📎 **출처**: `papers/lomeli2024_predicting_reactivity_passivation_ssb_interfaces.md` · 초안 `_pending_index_lomeli2024_predicting_reactivity_passivation_ssb_interfaces.md`

⛔ **A–D 물성 4축 표에 행을 만들지 않는다** — 자체 물성값은 **3분류 라벨**과 **붕소화물 2종 σ**(공공농도 0.05 % **가정**)뿐이고, **아르지로다이트 0회 · `Li₆PS₅Cl` 이 3535 목록에 없다 · ESW/탄성/gap/W_ad 0회**다. 물성 판정은 **§E 2행**, 공백 판정은 **§H 1행**.

**[Lomeli24] `lomeli2024_predicting_reactivity_passivation_ssb_interfaces` — 음극측 계면 반응성을 "AIMD 로 라벨 → 구조 서술자로 배워 → 3535개에 외삽" 한 편**
(⛔ 전부 **소환값**. 550 K·40 ps·<150원자·Γ-only·**계당 1회** AIMD 의 값이다. 우리 `db/properties/` 절대값과 섞지 않는다.)

| 항목 | [Lomeli24] 가 보이는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| **★★ 부동태화의 조작적 정의** | *"반응이 **원래 계면 근처에만** 머무르나"* — **공간적 국소성 하나**. 전자절연·두께·성장속도·수송비 **전부 아니다** | **정의 자체가 없다** (열역학 산물표만) | 🔵 **이식하되 고쳐서.** 정의의 뼈대는 쓸 만하다 — 고칠 곳은 **정규화·시간점·두께수렴·전자기준 공간투영** 넷(§H 1행) |
| **★★ 반응영역 분리 기법** | **양쪽 계면 주기셀**(PBC 로 계면 2개, 둘 다 센다) + **"원래 계면평면" = 바깥 SSE 원자 ↔ 금속 원자의 중간면** + **계면수직(z) 1D MSD** + **평면교차 필터** + ⭐ **sublattice(비-Li) 원자만 평균** + *unstable 이면 넘어온 Li 도 포함* | 우리 MD 는 **벌크 전용** — 계면 반응을 벌크 확산과 분리하는 장치가 없다 | 🔵🔵 **채택 권고.** ⭐ **`sublattice 만 세기` 한 수가 이 논문에서 제일 영리하다** — Li 의 정상 확산이 반응 신호를 가리는 것을 원천 차단한다. 우리 MSD 창 규약(2–50 ps, 3D)과 **충돌하지 않는다**(다른 양이므로 따로 둔다) |
| 🔴 **정규화의 함정** | `Norm. MSD = ⟨MSD_⊥⟩ / L_SSE` (단위 **Å**, 논문은 단위를 한 번도 안 쓴다) | — | ⛔ **채택 금지.** 반응전선이 고정깊이에서 멈추면 분모만 커져 **SE 를 두껍게 할수록 "부동태화" 로 보인다.** 저자가 셀크기 의존을 인정하면서 **원인이 자기 정규화임을 짚지 못한다** ⇒ 우리는 **`L_reacted(t)` [Å]** 로 보고 |
| 🔴 **전자적 부동태 판정** | **시도했고 실패했다** — `Fig. S3`(10계)·`Fig. S4`(21계) **전 패널 E_F 에 유한 DOS**. 원인은 **액체 Li**(550 K > Li 융점 454 K) | `sei_electronic.json` 은 **상별 벌크 갭**(fixed-occ nscf) — 계면 셀 DOS 가 아니다 | 🔵 **교훈 + 처방.** ⛔ **액체 금속을 포함한 계면 셀의 전체 DOS 는 부동태 판정에 못 쓴다.** ⇒ 우리가 음극 계면 DOS 를 계획하면 **반응층에만 공간투영**하거나 **상별 갭 + 연속성**으로 간다. ⭐ 우리 쪽이 이미 유리한 자리 |
| **★ 문턱의 근거** | stable **<0.05**(근거 문장 없음) · 원자 반응판정 **0.5 Å²**(= **1937년 Zn X선 논문** ref 19 의 0.1 Å² 의 **5배**, 배수 근거 없음) · **passivating↔reactive 는 숫자 자체가 없고 눈으로 판정**(`Fig. 1` 캡션 *"by inspection of the simulation cells"*) | 우리 규약은 `kb/` 카드에 근거를 적는다 | ⚠ **반면교사.** *"임의 문턱 하나(100 meV/atom)"* 를 공격하면서 **근거 없는 문턱 둘 + 숫자 없는 문턱 하나 + 사람 눈**으로 대체한다 |
| **🔴🔴 보고량 규율 대조** | **선언된 것**: 구조 선택 = *"변형 최소 · 셀 최소"*(= **비용 규칙, 물리 규칙이 아니다**). **선언 안 된 것**: 궤적 집계(**시드 1개**) · 다형 집계(✎ **87개 조성이 반대 라벨**) · 상태 선택(`Li₆FeCl₈` 등 **열린 껍질·산화환원 활성인데 스핀·자화·NUPDOWN 0회**) · 온도(550 K vs 400 K, **대상 미공개**) · 초기 간극(1.8–3.0 Å **물질별 값 미공개**) | `kb/templates/estimand_card.md` — 보고량 카드를 **던지기 전에** 채운다 | ⛔⛔ **우리 기준으로 이 스칼라는 정의되지 않았다.** ⭐ **`Li₆FeCl₈` 는 `kb/methodology/estimand_before_running_2026_08_28.md` §2.1 의 교과서 사례**(열린 껍질 + 자성 + 산화환원 활성 + 상태 선언 0) — 우리 SDCP 8회 반려와 **같은 층위**. *"+U 를 켰다"는 상태 선언이 아니다* |
| **🔴🔴 스크리너 통계의 함정** | **CV 6–8 %** 는 ✎ **1 744 435 개 특징조합**(22 특징 × N=1..10 전수)을 **50점** 위에서 5-fold CV 로 채점하고 **최솟값을 보고**한 것. 50점에서 **CV 양자 = 1/50 = 0.02**. 증거 둘: `Fig. 2b` 의 N=3–6 평평 0.08 → N=7 **0.06** → N=8–9 **다시 0.08**(= 훈련점 1개 진동) · `Table S2` 의 **SPF 계수 0.042 = ΔE_rxn(−2.145)의 1/51** 인 특징이 "최적 7개"에 포함 | 우리 실측(J-17): 쌍 LOOCV 0.0892 → **LODO −0.1805 → L2DO −0.2548**(group-out 낙차 0.27) | ⚠⚠ **반면교사 — [Zhao21HECS] R²=0.820 과 같은 계열의 2호 사례.** **정직한 숫자는 홀드아웃 35.3 % 하나**다. 우리가 이 편을 인용할 때는 **CV 값만 쓰면 그 편향을 승인하는 셈**이라 **반드시 35.3 % 를 같이 쓴다** |
| **🔴 검증셋 설계** | *"we **chose materials predicted to be good Li ion conductors**"* — **다른 모델(Sendek σ)의 예측으로 고른 17종**(10/17 별표). 그리고 **`ΔE_rxn` 단독 기준선을 그 홀드아웃에서 재보지 않았다** | 우리 group-out 규율 | ⚠ **반면교사 2.** *"3–4배 개선"* 은 **CV 대 CV** 비교일 뿐이고, **홀드아웃에서의 개선은 한 번도 보이지 않았다** ⇒ 우리 비교표에서는 **기준선을 같은 분할에서 재는 것**을 규칙으로 둔다 |
| **🔴 사후 재채점** | 오류 6/17(35.3 %) 중 **3건(stable→passivating)을 "그래도 쓸 만"이라며 빼고 17.6 % 로 다시 적는다** | *"검증 게이트를 결과 보기 전에 정한다"* (CLAUDE.md 계산 규율) | ⛔ **정면 위반 사례.** 우리 게이트 규율의 외부 반례로 인용 가치 있음 |
| **★ 서술자 표현(representation)** | **Sendek et al. 22 특징**(AASD·AAV·AFC·ENS·LASD·LBI·LLB·LLSD·LNC·PF·RBI·RNC·SBI·SDLC·SDLI·SLPE·SLPW·SNC·SPF·VPA·ΔE_form·ΔE_rxn). 정규화 계수 전수는 digest §3d | cascade descriptor v0 (**J-17 `[Zhao21HECS]`** 가 HECS 골격) | ⭕ **접속점.** 두 편이 **같은 표현 계열로 서로 다른 타깃**(BVSE Ea / 계면 반응성 라벨)을 다룬다 ⇒ **하나의 표현으로 두 타깃** 실증. `AAV·PF·SBI·LBI·LLB·SLPW·SLPE` 를 v0 후보에 올릴 근거 |
| ⚠ **계수 해석의 함정** | **부호 앵커는 본문이 준다**(SBI 음수 = stable 방향). 그런데 🔴 **AASD(−0.301, "멀수록 안정")가 AAV(+0.616)·SLPW(+0.621) 의 밀도 서사와 반대 부호**이고, 🔴 **SBI(−0.791, SM)와 LBI(+0.657, RM)가 반대 부호**다 | — | ⚠ **다중공선 특징에서의 전형적 부호 뒤집힘.** 논문은 자기 서사에 맞는 계수만 해설하고 반대 부호는 언급하지 않는다 ⇒ **우리가 계수로 물리를 말할 때 전 계수를 다 보여 주는 것**을 규칙으로 |
| **★ ΔE_rxn 규약** | MP API 상도에서 가져온 값. 🔴 **혼합분율 규약(min over x? x=0.5?)·open/closed 규약·MP 세대 전부 미기재** | `interface_reactivity` / ΔH_D (예 −0.3227 eV/atom, 정의·부호·혼합분율 최소화가 **선언돼 있다**) | ⛔ **값 대조 금지.** 자릿수가 비슷해 보여도 **정의가 확인되지 않는다.** ⭕ 우리 쪽이 낫다 — 이 대비가 우리 원장 규율의 값어치를 보여 준다 |
| **★ 공개 자산** | **SI2 xlsx 3535행**(`stable_materials` 533 / `passivating_materials` 788 / `reactive_materials` 2214 · 열 `Material·MP-ID·crystal_system·E_rxn`). ⚠ **`openpyxl` 로는 못 연다 — strict OOXML** ⇒ `zipfile`+`ElementTree` 직접 파싱. ⛔ **`Norm. MSD` 원자료 67개·코드·궤적·시드는 미공개** | — | 🔎 **확보 완료.** 우리 산물·코팅·도펀트 후보의 **Li-금속 반응성 외부 참조표**로 바로 쓴다(digest §3g 전수) |
| **★ 외부 방증 1건** | `Li₃P`·`Li₃N` 이 3535 스크린에서 빠진 이유가 **`E_G > 1.5 eV` 필터**다 | `sei_electronic.json` fixed-occ nscf: **Li₃P 0.7092** · Li₂S 3.4379 · Li₂O 4.986 · LiCl 6.2603 eV | ✅ **서열의 외부 방증**(절대값 방증 아님). *"우리가 전자누설 산물이라 부른 두 상이, 남의 독립 스크리너에서도 '전해질로 쓸 수 없는 갭'으로 걸러졌다"* |

**상호참조**: **§J-36 `[Wang22Res]`** 와 **짝 블록**이다 — 이 편은 *"분해가 시작되는 순간"*, J-36 은 *"분해가 끝난 뒤"*. **둘 다 음극측이고 둘 다 아르지로다이트를 한 번도 계산하지 않는다.** 두 편을 합친 문장은 **§E** 에 있다. 표현(descriptor) 쪽 짝 블록은 **§J-17 `[Zhao21HECS]`**.

---
```

---

## ④ 정정 제안 문구 (조율 세션이 판단할 것)

> 아래는 **제안**이다. 내가 직접 고치지 않았다.

### ④-1. 🔴 기존 서술에 조건절이 필요한 곳 — `Li₃P`

우리 여러 표면에 *"`Li₃P` 는 전자를 샌다(`conductor-LEAK`, gap 0.7092 eV)"* 가 조건절 없이 쓰여 있다.
[Lomeli24] 는 같은 상을 **"Li 금속에 chemically stable"** 이라 부른다(AIMD 직접 확인).
**모순이 아니라 다른 축**인데, 축 이름 없이 병치되면 다음 사람이 둘 중 하나를 틀렸다고 읽는다.

> **제안 문구**
> *"`Li₃P` 는 **전자누설 축에서** 문제다(fixed-occ nscf gap 0.7092 eV = `conductor-LEAK`). **화학반응성 축에서는** 오히려 Li 금속에 안정하다는 외부 AIMD 근거가 있다([Lomeli24] 550 K·40 ps, `Norm. MSD` figure-read ≈0.03 < 문턱 0.05). **두 축을 같이 적지 않으면 서술이 뒤집혀 읽힌다.**"*

(이미 §E 에 *"[Xiao20Rev] 와 정면 충돌 — 조건절을 달아야 한다"* 행이 있다. **이 논문이 그 조건절에 세 번째 독립 근거를 더한다** — 그 행 꼬리에 붙이는 것도 방법이다.)

### ④-2. ⚠ 인용 가드 신설 제안 — **"[Lomeli24] 를 LPSCl 근거로 쓰지 말 것"**

`Li₆PS₅Cl` 이 **훈련셋·검증셋·3535 목록 어디에도 없다**. 그런데 이 논문은 제목·초록이 워낙 일반적이라
**나중에 "SSE 계면 반응성" 근거로 소환되기 쉽다.**

> **제안 (가드 문구, §E 2행 안에 이미 넣어 뒀고 별도 표면에도 필요하면)**
> ⛔ **`[Lomeli24]` 로 `Li₆PS₅Cl` 을 말할 수 없다** — 목록에 없다(`argyrodite` 0회·`Li6PS5` 0회).
> 대리값은 **`Li₆PS₅I` reactive(ML 예측)** · **`Li₅P(S₂Cl)₂` reactive(ML 예측)** · **`Li₃PS₄`·`Li₇P₃S₁₁` reactive(AIMD 직접)** 이고
> **셋의 신뢰도가 다르다**(예측 vs AIMD). 옮길 때 **어느 쪽인지 반드시 표기**.

### ④-3. ⚠ 성능 인용 규칙 제안

> **제안**: 이 논문의 분류 성능을 인용할 때는 **홀드아웃 35.3 % 오분류를 반드시 같이 적는다.**
> **CV 6–8 % 만 인용하면 ✎ 1 744 435 조합 × 50점에서 고른 최솟값을 성능으로 승인하는 셈**이 된다.
> (같은 계열 선례: **[Zhao21HECS]** 의 시험 R² 0.820 — 우리가 0.7661 로 정정한 건.)

### ④-4. 🔧 도구 제안 — `extract_figures.py` bbox 중복

`litdb/figures/lomeli2024_predicting_reactivity_passivation_ssb_interfaces/fig_S2.png` 와 `fig_S3.png` 가
**바이트 동일**(md5 `599b637dca29cc505ae4e09ee051b066`)이다. SI 4쪽에 `Fig. S2`(산점)와 `Fig. S3`(pDOS 10패널)가
**한 쪽에 같이** 있는데 추출기가 **두 캡션에 같은 bbox** 를 배정했다.

> **제안**: `--dedupe` 가 "바이트 동일 중복 크롭"을 이미 잡는다. 다만 이 경우는 **삭제가 아니라 재분할**이 맞다
> (두 그림이 실제로 존재하고 한 쪽에 위아래로 놓여 있다). **한 쪽에 캡션이 2개 이상이면 캡션 y좌표로 쪽을 분할**하는
> 규칙이 필요해 보인다. ⚠ **이번 세션은 `--clean` 금지 지시라 파일을 건드리지 않았다** — SI 4쪽을 통째로 재렌더해
> 둘 다 읽는 것으로 우회했다.

### ④-5. ⚠ INDEX 표 칸 수 / §절 헤더 순서 확인 기록

- `INDEX.md` `## ✅ Digest 완료 (paper-level)` 표 머리 = **`| slug | 논문 | 축 |`** (3칸) — ①번 행은 **3칸**으로 맞췄다.
- `comparison_vs_ours.md` **§E** 머리 = **`| 주장 | 출처 | 우리 | 일치 |`** (4칸) — ③-1 두 행 **4칸**.
- `comparison_vs_ours.md` **§H** 머리 = **`| gap | 누가 필요로 함 | 보강책 |`** (3칸) — ③-2 한 행 **3칸**.
- `comparison_vs_ours.md` **📑 Reference key** 머리 = **`| 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |`** (4칸) — ②번 행 **4칸**.
- **§A~§D 물성 4축에는 행을 만들지 않았다** (사유는 ③-3 머리).
