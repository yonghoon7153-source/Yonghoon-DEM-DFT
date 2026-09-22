# ⏸ 병합 대기 — `schwietert2020_redox_activity_vs_electrochemical_stability`

> 2026-09-22 · litdb-curator **동시 실행**으로 `INDEX.md`·`comparison_vs_ours.md` 직접 수정 금지를
> 받아, 넣어야 할 내용을 여기 적어 둔다. 충돌이 풀리면 **아래 블록들을 그대로 옮기고 이 파일을 지운다.**
>
> 🔴 **이 편은 물성 4축에 *들어간다*.** `Li₆PS₅Cl` 이 주인공이고 우리 §B①(산화 onset)·§E(환원)와
> **같은 반응식**을 쓴다 ⇒ `🔧 방법 원전` 이 아니라 **본 표에 행을 만든다**.
> 단 **추정량 라벨(층①/층②)을 반드시 붙인다** — 안 붙이면 2.24 V 와 2.256 V 가 "일치"로 읽힌다.
>
> 🎤 talk 역링크 **해당 없음** — `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → 1건
> (`lee2026_skku_mlip_materials_design.md` §99-10, MLIP 축 6건)이고 이 논문은 그 표에 없다 (grep 실측 0건).
>
> ⛔ **커밋 안 함** (요청). 그림은 `litdb/figures/schwietert2020_redox_activity_vs_electrochemical_stability/`
> 에 재추출·수기보정 완료 (digest §16 에 도구 문제 3건 보고).

---

## ① `INDEX.md` 에 추가할 행

| `papers/schwietert2020_redox_activity_vs_electrochemical_stability.md` **(본문 12 pp = 기사 8 + Methods 2 + Extended Data 2 · SI 19 pp · 그림 19장 중 9장 실독)** | **[외부·🔴🔴 우리 §B 최대 반론의 *원전* · 아지로다이트 정면 · `[Dutra25Rev]` ref 211]** **Tammo K. Schwietert**·**Violetta A. Arszelewska**(공동1)/Chao Wang/Chuang Yu/Alexandros Vasileiadis/**Niek J. J. de Klerk**/Jart Hageman/Thomas Hupfer/Ingo Kerkamm/Yaolin Xu/Eveline van der Maas/Erik M. Kelder/**Swapna Ganapathy\***/**Marnix Wagemaker\*** (**TU Delft** Storage of Electrochemical Energy + **Robert Bosch GmbH** Renningen), "**Clarifying the relationship between redox activity and electrochemical stability in solid electrolytes**" (***Nat. Mater.* 19, 428–435 (April 2020)**, DOI `10.1038/s41563-019-0576-0` · 투고 2019-06-03 / 수락 2019-11-28 / 온라인 2020-01-13 · NWO VICI 16122 + eScience 680.91.087 + ADEM · ⛔ **데이터 리포지터리 없음**) — ✅ **서지 PDF 직독 확인: 우리 기록 "Nat. Mater. 19, 428 (2020)" 이 맞다.** **★★★ 주장**: SE 는 분해되기 *전에* 자기 자신이 산화·환원된다 — `Li₆PS₅Cl` 이 **2.24 V 에서 골격 유지 탈리튬화 → `Li₄PS₅Cl`(S²⁻→S⁰)**, **1.08 V 에서 리튬화 → `Li₁₁PS₅Cl`(P⁵⁺→P⁰)**, 그 **준안정 중간상이 곧바로 무너져** 최종 산물이 된다 ⇒ **간접(indirect) 경로**. 창 = **1.16 V** (직접 예측 **≈0.3 V**, `[Zhu15]` **1.71–2.01 V**; 실측 **1.25 V**). **일반성**: garnet `LLZO` 산화 **2.91 → 3.54 V (+0.63)** · NASICON `LAGP` **환원** **2.70 → 2.31 V (−0.39)** — ⚠ 본문은 LAGP 를 "oxidation" 이라 적지만 Methods·`Fig. 6f`·`Supplementary Fig. 8b` 전부 **reduction**(오기), 그리고 **반쪽창 6개 중 2개(LLZO 환원·LAGP 산화)는 간접·직접이 같은 전압이라 판별불가**. **🔑🔑 우리와의 관계 = "반론" 이 아니라 "다른 층"**: 저들 **2.24 V 는 골격 유지(topotactic) 전압 = `[Xiao20Rev]` 층②**, 우리 **2.256 V 는 분해 onset = 층①** ⇒ **같은 표에 놓으면 안 된다**(0.016 V 차는 서로 다른 추정량의 수치적 우연). ✅ **반응식은 글자 그대로 같다** — 순산화 `Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li`(우리 2.256 V 식) · 순환원 `Li₆PS₅Cl + 5Li → 5Li₂S + LiCl + P`(우리 1.242 V 식) · Li 교환 없는 자기분해 `→ Li₃PS₄ + Li₂S + LiCl`(우리 OCV 1.717 V 식 = `Fig. 2a` 의 x=6 흑색 ✕). **★ 간접 보정의 크기(우리 유도)**: 산화 **저들 2.24 vs 우리 2.256 = −0.016 V(≈0)** · 환원 **1.08 vs 1.242 = −0.162 V(실제로 넓어짐)** · 저들 +0.23 V 는 전적으로 **`[Zhu15]` 2.01 V 에 대한 보정**이다. **🔥 그리고 그 +0.23 V 가 크지 않다는 근거가 논문 *안*에 있다** — `Supplementary Fig. 2` 의 **저자 자신의 "Therm. equilibrium" 곡선이 ≈2.32 V**(figure-read; 1≲x≲11 전체가 단일 `Li₂S`/S 전환 평탄, 10 Li)라 `Fig. 2b` 의 Zhu ✕ **2.01 V** 와 **0.31 V 다르다**; 저자 평형곡선 기준이면 간접 2.24 V 는 오히려 **0.07 V 낮다**(= *"넓어짐" 이 성립 안 함*, 논문이 이 불일치를 언급 안 함). 같은 크기의 세 번째 눈금: `Table S1`(MP≈2019) vs 우리 사다리(MP2026)의 **Li–P 이원계 상 순서는 완전 동일**한데 전압이 **0.07–0.24 V** 다르다(`LiP₇` 1.27↔1.177 · `Li₃P₇` 1.17↔0.932 · `LiP` 0.94↔0.87). ⇒ **간접 보정 ≈ MP 판본 드리프트 ≈ 논문 내부 직접값 흩어짐, 셋이 같은 자릿수**. **★ 우리가 이기는 지점 1건**: 저자는 *"직접 예측은 2.3 V `P₂S₅`, 실측은 2.9 V `P₂S₇⁴⁻` ⇒ 우리 식 분석이 필요하다"* 고 쓰는데, **우리 2026 사다리는 2.385 V 에 `P₂S₇` 를 낸다**(종 ✅, 전압 0.5 V 낮음) ⇒ **그 진단은 2015 상집합 한정**. **실험**(LPSC 를 활물질로 쓰고 산화셀·환원셀을 따로 조립, CV 가 아니라 **느린 정전류 dC/dV**): 창 **1.25 V**(활성 <1.25 V·>2.50 V; ⚠ `Fig. 2c` 캡션은 2.30 V, figure-read 는 **≈2.43 V** — **셋이 다르다**), 용량 **264**(→3.63 V, CE 70 %)/**405**(→0.63 V, CE 40 %)/한 물질 전지 **270→107 mAh g⁻¹**; **XRD 격자 9.8693 → 9.7620 Å (−1.09 %)** ↔ DFT x=6→4 **−1.0 %** = **탈리튬화 아지로다이트의 직접 구조 증거**(⚠ 리튬화 쪽 +6.6 % 팽창은 **XRD 에 안 보인다** — 증거 비대칭); ssNMR **`P₂S₇⁴⁻` 95 ppm**·**`Li₃P` −220 ppm**·`LiCl` −1.1·`Li₃PS₄` 0.44·`Li₂S` 2.3 ppm; NCM622 조합 **`Ni₃S₄`**(50사이클). **DFT**: VASP·PBE(⚠ ref 46 이 PBE 가 아니라 Perdew–Burke–**Wang** PRB 54, 16533 — 서지 오기)·PAW·**ecut 280 eV**(=VASP 기본 ENMAX, 여유 0·수렴시험 0건)·k **4×4×4**(LLZO Γ점만 @500 eV·LAGP 3×3×1 @500 eV)·**전하중성 셀만**(명시)·단위포 1개(**52원자**)·0 K·U 없음·vdW 없음·스핀 미언급; **🔴 무질서 = S/Cl 배열 *하나* 고정**(ref 44 de Klerk 2016 최안정 배열, *"thus the … voltages were not affected"* = **단언, 시험 0**); Li 배열은 **랜덤 1만 개 → 정전기 에너지로 선별 → 상위 20개만 VASP**; 전압은 **Aydinol 평균 인터칼레이션 식**(식 3); 분해산물 에너지는 **MP 에서 가져옴**(⇒ 판본 드리프트가 그대로 들어온다). **AIMD**: NVT **velocity-rescaling**(1000스텝마다)·dt 2 fs·**100 ps**·Γ점·**400 K**·x=4/6/11, **단일 궤적**. **🔴🔴 최대 비판 = 중심 주장이 측정되지 않았다** — *"간접 경로의 **활성화 장벽이 낮다**"* 가 논지의 축인데 **NEB 0회·전이상태 0회·eV 단위 장벽 0개**, 근거는 RDF 뿐이고 저자도 캡션에 *"느린 변환은 범위 밖"* 이라 적는다 ⇒ ⛔ *"장벽이 낮음을 계산으로 보였다"* 인용 금지. **판정 🟡 범위 선언 필요**(🟢도 🔴도 아님): 우리 *"2.256 V = worst-case 하한"* 은 **살아 있다**(① `[Xiao20Rev]` 4층 위계가 층②를 이미 "best case" 로 갖고 있다 ② 저자 자신이 *"Which stability window applies **depends on the activation barriers**"* 라고 쓴다 = 운동학 선택) — 다만 **추정량 라벨 3문장**을 원장에 넣어야 한다. **🔴 이 digest 가 여는 감사 2건**: 우리 창 **1.242–2.256 = 1.014 V** vs `[Zhu15]` **0.30 V**(같은 방법 계열인데 **3.4×**, 원인 미설명) · 우리 OCV **1.717** vs `[Zhu15]` 환원한계 **1.71 V**(**0.007 V** 차 — 같은 양인지 확인 안 됨) ⇒ **닫기 전에는 "우리 창이 실험 1.25 V 와 잘 맞는다" 고 쓰지 않는다**. **그림 19장 중 9장 실독**(`Fig. 1`·`2`(+2b 확대)·`3`·`5`·`6`·Extended Data `Fig. 1`·Supp `Fig. 3`·`Fig. 9`·**Supp `Fig. 2`(도구가 못 잘라 별도 렌더)**), **미열람 5장**(`Fig. 4` 31P NMR·Ext `Fig. 2`·Supp `Fig. 4`·`6`·`7`), 표 6장은 PDF 텍스트로. **📌 도구 문제 3건 보고**(digest §16): ① 최초 추출이 inbox 의 **같은 번호 접두사 다른 논문**(`6. Model-informed design…`)을 본문으로 집었다 ② **Extended Data ↔ Supplementary 번호 충돌**로 Supplementary Fig. 1·2 가 "중복" 으로 버려짐(현 `fig_S1/S2` 는 **Extended Data** 다) ③ **캡션이 그림 아래에 오는 Nature 배치**를 못 잡아 본문 `Fig. 1·3·4·6` 전부 탈락(수기 크롭). | **🔴 §B①(산화 onset)·§E(환원) 본표 편입 — 단 층①/층② 라벨 필수**; §A/§C/§D 는 값 0건 |

---

## ② `comparison_vs_ours.md` **§B (산화안정성 4축)** 에 추가할 행

| **B① 🔴🔴 🆕 *간접(indirect) 분해* — 우리 hull ESW 에 대한 가장 강한 외부 반론의 **원전**, 그리고 그것이 왜 우리 값을 무효화하지 않는가** (2026-09-22 신설) | (우위 아님 — **추정량이 다르다**) | **[Schw20]** `schwietert2020_redox_activity_vs_electrochemical_stability` · ***Nat. Mater.* 19, 428 (2020)** · `Fig. 2a–c`+`Fig. 5`+`Extended Data Fig. 1`. `Li₆PS₅Cl` 이 **2.24 V 에서 골격을 유지한 채 탈리튬화**(→`Li₄PS₅Cl`, S²⁻→S⁰)하고 **1.08 V 에서 리튬화**(→`Li₁₁PS₅Cl`, P⁵⁺→P⁰)한 뒤 **그 준안정 중간상이 무너져** 최종 산물이 된다 ⇒ 창 **1.16 V**(직접 **≈0.3 V** = `[Zhu15]` 1.71–2.01, 실측 **1.25 V**). 저자 문장: *"**Which stability window applies depends on the activation barriers** to these decomposition routes"* | comp1/modelc **2.256 V** (0 K grand-potential, LiS₄ 제외) · 환원 **1.242 V** · OCV **1.717 V** ⇒ 🔑🔑 **"반론" 이 아니라 "다른 층" 이다**: 저들 2.24 V = **골격 유지(topotactic) 전압 = `[Xiao20Rev]` 층②**, 우리 2.256 V = **분해 onset = 층①**. ⛔ **0.016 V 차를 "일치" 로 쓰지 마라 — 서로 다른 추정량의 수치적 우연이다.** ✅ **반응식은 글자 그대로 같다**(순산화 `Li₆PS₅Cl → Li₃PS₄+LiCl+S+2Li` · 순환원 `+5Li → 5Li₂S+LiCl+P` · 자기분해 `→ Li₃PS₄+Li₂S+LiCl`) ⇒ **화학은 이견 0, 이견은 "어느 단계를 onset 이라 부르나" 하나뿐**. 🟡 **조치 = 범위 선언 3문장**(digest §7-9), 🔴 재계산 아님 |
| **B① 🆕 그 간접 보정이 *얼마나 큰가* — 세 눈금이 전부 같은 자릿수** (2026-09-22 신설) | (우위 아님 — **크기 재기**) | **[Schw20]** ① `Fig. 2b` 기준 산화 보정 **2.01 → 2.24 V = +0.23 V** ② **`Supplementary Fig. 2` 의 저자 자신의 "Therm. equilibrium" 곡선 ≈2.32 V**(figure-read; 1≲x≲11 전체가 **단일 `Li₂S`/S 전환 평탄**, 10 Li) — `Fig. 2b` 의 Zhu ✕ 2.01 V 와 **0.31 V 차**, 그 기준이면 간접 2.24 V 가 **0.07 V 더 낮다**(논문이 이 불일치를 **언급 안 함**) ③ `Table S1`(MP≈2019) 의 Li–P 사다리 **1.27/1.17/0.94/0.87 V** | 우리 사다리(MP2026) **1.177/0.932/0.87/(0.0 바닥)** ⇒ **상 순서 완전 동일, 전압만 0.07–0.24 V 차** = MP 판본 드리프트의 눈금(우리 유도). 🔑 **①≈②≈③ (0.23 / 0.31 / ≤0.24 V)** ⇒ **"간접 경로 때문에 우리 2.256 V 를 못 쓴다" 는 성립하지 않는다.** ⚠ ①은 저들 VASP·우리 MP 를 섞으므로 **부등호와 규모까지만** 쓴다 |
| **B① 🆕 `[Xiao20Rev]` worst-case 프레임 **안인가 밖인가** → ✅ 안이다** (2026-09-22 신설) | ✅ **우리 프레임이 살았다** | **[Schw20]** + **[Xiao20Rev]** 4층 위계(① ESW=worst / ② **topotactic=best** / ③ pseudo-binary / ④ explicit·AIMD) | **[Schw20]** 의 2.24 V 는 **정확히 층②의 양**이다 ⇒ 프레임이 이미 칸을 갖고 있다. **근거 ②**: 저자 자신이 **경로 선택을 운동학에 맡긴다**(위 인용문) ⇒ *"no kinetic stabilization 을 가정한 worst case"* 와 **모순 없음**. ⚠ **정밀화 1건**: `[Xiao20Rev]` 층② 는 *"SE 가 안 망가진다"* 는 **best case** 인데 **[Schw20]** 의 중간상은 **곧 무너진다** ⇒ 그 2.24 V 는 **"관문(gateway) 전압"** = 숫자는 층② 자리, 의미는 *"여기부터 비가역 열화 시작"*. **층①과 ② 사이의 새 칸**으로 부르는 게 정확하다. 🔑 **우리 §H 의 *"층② 없음 — 상한이 없다"* 항목에 이제 외부 수치가 붙는다**(우리 조성은 여전히 미계산) |
| **B② 🆕 2차 산화 종 — 우리 `P₂S₇` 예측이 살아 있다 (우리가 이기는 지점)** (2026-09-22 신설) | 🟢 **우리 우위** | **[Schw20]** p.432: 직접 예측(ref 14, MP2015)은 **2.3 V `P₂S₅`** 인데 실측(`Fig. 1d` 주봉 **2.93 V**, ³¹P **95 ppm** = `P₂S₇⁴⁻`, ref 32 Hakari)과 안 맞는다 ⇒ 저자 결론 *"…requires a **comprehensive DFT redox activity analysis** as done here"* | `esw_lis4excluded.json` comp1 **2.385 V**: `Li₆PS₅Cl → 0.5 **P₂S₇** + LiCl + 1.5 S + 5 Li` ⇒ 🔑 **"직접 방법으로는 `P₂S₇⁴⁻` 를 못 낸다" 는 진단은 2015 상집합 한정이고 2026 상집합에서는 틀렸다.** **종 ✅, 전압은 실측보다 0.5 V 낮다**(= 과전압 + 간접 몫 = 우리 하한 프레임 그대로). ⚠ 우리 2.385 V 는 **SE 자기분해**, 저들 2.9 V 는 **`Li₃PS₄` 의 산화** ⇒ **종 일치까지만** 쓴다 |

## ②b `comparison_vs_ours.md` **§E (환원/음극)** 에 추가할 행

| **E 🆕 환원 쪽에서는 간접 보정이 *실제로* 있다 — 우리 1.242 V 가 0.162 V 좁다** (2026-09-22 신설) | 🔴 **저들 쪽이 넓다** | **[Schw20]** 간접 환원 onset **1.08 V** (`Li₆PS₅Cl → Li₁₁PS₅Cl`, P⁵⁺→P⁰). 2차 환원 사다리 **1.3 V → ≈0.87 V**(`LiP`→`Li₃P` 가 환원용량의 **67 %**), 실측 봉우리 figure-read **1.15 / 0.85 / 0.72 V** | 우리 `reduction_V = **1.242 V**`, 반응식 `Li₆PS₅Cl + 5 Li → 5 Li₂S + LiCl + P` = **저들 `Li₁₁PS₅Cl → P + 5Li₂S + LiCl` 과 원자 하나까지 동일** ⇒ **차 −0.162 V (우리 유도, 논문 미보고)**. 🔑 **산화 쪽과 달리 여기서는 간접 경로가 창을 실제로 넓힌다** ⇒ **우리 §E 서술은 이 방향의 보정을 인정해야 한다**. ⚠ 저들 1.08 V 는 층②, 우리 1.242 V 는 층① — **라벨 필수** |

## ②c `comparison_vs_ours.md` **§H (우리가 아직 못 하는 것)** 갱신

기존 *"우리에게 층②(topotactic, 식 3)가 없다 — 상한이 없다"* 항목에 한 줄 추가:

> 🆕 2026-09-22 — **[Schw20]** 이 `Li₆PS₅Cl` 의 층② 값을 **2.24 V**(산화)·**1.08 V**(환원)로 준다.
> **우리 조성(comp1·modelc)의 층② 는 여전히 0 건이다.** 계산한다면 보고량 카드
> (`kb/templates/estimand_card.md`) 를 **먼저** 채운다 — **[Schw20]** 이 S/Cl 무질서를 **배열 하나**로
> 고정하고 *"따라서 전압은 영향받지 않았다"* 고 **단언**했기 때문에(시험 0), 우리 계에서는
> **무질서 처리 자체가 admissibility 문제**가 된다.

## ②d `comparison_vs_ours.md` **§J-24 (`[Dutra25Rev]` 방법 원전)** 갱신

`③ 간접 경로 (ref 211 = Schwietert, Nat. Mater. 19, 428 (2020))` 줄에:

> ✅ **원전 확보 2026-09-22** → `papers/schwietert2020_redox_activity_vs_electrochemical_stability.md`.
> ⚠ **리뷰의 요약 한 줄(*"the ESW is usually wider"*)만 인용하지 마라** — 원전에서 실제로 잰 것은
> **반쪽창 6개 중 4개**(LPSC 산화 **+0.23** · LPSC 환원 **−0.63** · LLZO 산화 **+0.63** · LAGP 환원 **−0.39 V**)
> 이고 **2개는 간접·직접이 같은 전압이라 판별불가**다. 그리고 **산화 쪽 +0.23 V 는 `[Zhu15]` 2.01 V 에
> 대한 보정**이라, 우리 2.256 V 에 그대로 더할 수 있는 값이 **아니다**.

---

## ③ 정정 (기존 행 수정) — `comparison_vs_ours.md`

| 위치 | 현재 | 고칠 것 |
|---|---|---|
| **514행 `[Rupp]` B① 방법: indirect (de)lithiation** | *"LPSCl→**`Li₄PS₄Cl`**/`Li₁₁PS₅Cl` 중간상"* | 🔴 **조성 오기** — 원전 확인 결과 **`Li₄PS₅Cl`** 이다(S 개수 5 유지). 그리고 *"(우리 못 봄)"* 을 **원전 digest 링크**로 교체 |
| **20행 `[Du22LMR]` 꼬리** | *"(계산 인용 2건 = `[Zhu15]`·Schwietert 2020)"* | ✅ 그대로 두되 **Schwietert 2020 을 digest 링크로** |

---

## ④ 🔴 감사 항목 신설 (§H 또는 `kb/open_items.md` ⏭)

> **우리 grand-potential 창이 `[Zhu15]` 보다 3.4× 넓은 이유를 우리가 설명하지 못한다.**
>
> | | 값 |
> |---|---|
> | `[Zhu15]` `Li₆PS₅Cl` 창 | **1.71 – 2.01 V = 0.30 V** |
> | 우리 (`esw_lis4excluded.json`, LiS₄ 제외) | **1.242 – 2.256 V = 1.014 V** (우리 유도) |
> | 우리 OCV | **1.717 V** ↔ `[Zhu15]` 환원한계 **1.71 V** — **0.007 V** 차 |
>
> **질문 2개**: ① 우리 `reduction_V = 1.242` 와 `[Zhu15]` 의 `red = 최고 lithiation plateau (1.71)` 이
> 같은 규약인가? ② 우리 `ocv_V = 1.717` 이 규약상 `[Zhu15]` 의 환원한계와 같은 양은 아닌가?
> (대조 파일: `db/properties/esw_lpscl_hull.json` = `energy_mode: "hull"`·`e_above_hull_0V = 0.0` 규약 vs
> `db/properties/esw_lis4excluded.json` = 사다리 9단계.)
>
> ⛔ **이 둘이 정리되기 전에는 "우리 창이 실험(1.25 V)과 잘 맞는다" 고 쓰지 않는다.**
> 우리 1.014 V 가 실측 1.25 V·**[Schw20]** 간접 1.16 V 에 가까운 것은 **매력적이지만 검증 전이다.**

---

## ⑤ 📌 도구 이슈 (`tools/litdb/extract_figures.py`) — 별도 처리 필요

digest §16 에 상세. 요약:
1. **🔴 최초 추출이 다른 논문 그림을 넣었다** — inbox 번호 접두사(`6. `)가 같은
   `6. Model-informed design of microcrack-tolerant cathodes…pdf` 를 본문으로 집었다.
   ⇒ **`--audit-src` 를 기본 경로에 편입** 제안.
2. **🔴 `Extended Data Fig. N` ↔ `Supplementary Figure N` 번호 충돌** — 둘 다 `S{N}` 이 되어
   뒤에 온 Supplementary 가 "중복(작은 쪽)" 으로 **버려진다**. 현 폴더의 `fig_S1/S2` 는 **Extended Data** 다.
3. **⚠ 캡션이 그림 *아래* 인 Nature 배치를 못 잡는다** — 본문 `Fig. 1·3·4·6` 전부 탈락,
   `Fig. 5` 는 상단 잘림. 이번엔 손으로 크롭해 `figures.json` 에 `manual_additions`/`note` 로 남겼다.

---

## ⑥ `litdb/our_dft_baseline.md` 에 넣을 한 줄 (§비교 시 주의)

> 🆕 2026-09-22 — **ESW 산화 onset 은 "층①(분해 onset)" 이다.** `[Schw20]`(*Nat. Mater.* 19, 428)
> 이 같은 물질에 대해 보고한 **2.24 V** 는 **층②(골격 유지 탈리튬화)** 라 **다른 양**이다.
> **0.016 V 차를 일치로 쓰지 않는다.** 우리에게는 층② 값이 **없다** = 창의 하한만 있고 상한이 없다.
