# ⏸ 병합 대기 — `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`

> 2026-09-22 · 1저자 지시로 `INDEX.md`·`comparison_vs_ours.md` **직접 수정 금지**. 넣을 내용을 여기 둔다.
> 충돌이 풀리면 **아래 블록을 그대로 옮기고 이 파일을 지운다.** (⛔ 이 작업은 **커밋하지 않았다.**)
>
> ⭐ **digest 본체**: `litdb/papers/haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md`
> ⭐ **그림**: `litdb/figures/haruyama2014_space_charge_layer_oxide_cathode_sulfide_se/` (그림 12 + 표 5, **그림 9장 실독**)
>
> ⛔ **이 편의 물성값은 LCO / β-Li₃PS₄ / LiNbO₃ 계다 — 아르지로다이트 0회 · Cl 0회 · MLIP 0회 ·
> MD 0회 · NEB 0회 · ESW 0회 · 탄성 0회.** ⇒ **A/B/C/D 물성 4축 표에 수치로 넣지 않는다.**
> 선례 = 같은 그룹 `[Haru17]` 행의 명시적 규정(*"β-Li₃PS₄ 계 — A–D 물성 4축에 수치로 넣지 않는다"*).
> 둘 곳 = **`🔧 방법 원전` 블록** + **§H(정직 목록) 1행**.
>
> ⚠ **§J 번호를 비워 뒀다** — 최근 충돌이 반복됐다. **병합자가 비어 있는 다음 번호를 배정**한다.
>
> 🎤 **talk 역링크 해당 없음** — `talks/lee2026_skku_mlip_materials_design.md` §99-10 인입 대기열(6건)에
> 이 논문 **없음**(`grep -in haruyama litdb/talks/` 무결과). 덱과 어긋나는 것도 없다(덱은 MLIP 아키텍처 축).
>
> 🔴 **병합자에게 별도 요청 1건 (§④ 참조)** — `db/literature/refs.json[37]` 의 주석 한 줄이
> **방법 축을 통제하지 않은 귀속**을 하고 있다. digest §11-② 에 근거를 적었다.

---

## ① `INDEX.md` 에 추가할 행

| `papers/haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md` **(본문 8 pp + SI 10 pp · 크롭 17장 중 그림 9장 실독 — 본문 `Fig. 1`–`5` 전부 + SI `Fig. S2`·`S4`·`S6`·`S7`; 표 5장은 의도적으로 텍스트 전사)** | **[외부·methods·★★★ 우리 v5 계면 기하의 *원전* · `db/literature/refs.json[37]` = method-anchor-PRIMARY 의 원문 검증 · ⛔ A–D 물성 4축 금지]** **Jun Haruyama**, **Keitaro Sodeyama**, **Liyuan Han**, **Kazunori Takada**, **Yoshitaka Tateyama\*** (NIMS MANA/GREEN + 京都大 ESICB + JST PRESTO/CREST), "**Space−Charge Layer Effect at Interface between Oxide Cathode and Sulfide Electrolyte in All-Solid-State Lithium-Ion Battery**" (***Chem. Mater.* 26, 4248–4255 (2014)**, DOI `10.1021/cm5016959` · 접수 2014-05-11 / 개정 2014-06-16 / 게재 2014-07-03, **ASAP 재게재 2014-07-09 — `Figure 1` 오류 + SI 파일 교체** · KAKENHI 23340089 · SPIRE(MEXT)+CMSI · 계산 NIMS·九州大·ISSP·東大 Oakleaf-FX · refs 55+11) — **산화물 양극|황화물 전해질 계면의 첫 DFT 논문**(저자 자칭), 그리고 **[Haru17] 이 그대로 물려받는 계면 3종을 만든 편**. **계 = LCO(110)\|β-Li₃PS₄(010)** + 버퍼 **LCO(110)\|LiNbO₃(1̄0)**, **LCO(110)\|LNO(110)**, **LNO(1̄0)\|LPS(010)**. **방법 = 정적 DFT+U 슬랩** (QE · PBE · **spin-unpolarized** · **USPP 40/320 Ry** · **U(Co 3d)=5.9 eV**(Nb 에는 없음) · **계면 Γ-only**(PDOS 만 2×1×1 / 2×2×1 nscf) · 힘 **0.001 Ry/bohr** · 응력 **0.5 kbar** · **중성셀** · Gaussian **0.001 Ry** · **ESM 은 점검만**(PBC 대비 총/형성E 차 0.1 / 0.01 eV) · 진공 **≈1.5 nm** · 슬랩 **1–2 nm** · **무질서 = Lepley 의 `β-Li₃PS₄-b` 정렬모형 단일배열**(4c Li 제거, SQS 아님)). ⭐⭐ **기하 원전으로서의 소득 — 4단계 절차가 전부 활자로 있다**: ①벌크 DFT+U(격자 오차 **±1.3 % 이내**) ②**화학양론 종단** 슬랩 + 전원자 이완(LNO 종단만 활자: **`−Li₂−Nb₂−O₆`**(1̄0) · **`Li₆Nb₆−O₉`**(110); **LCO·LPS 종단은 미기재**) ③**탄성계수 큰 쪽(LCO)에 격자를 맞춘다**(LNO/LPS 만 두 벌크의 평균) ④**계통적 횡방향 미끄럼 16/4/9 표본 전부 이완 후 최저 채택**. **`Table S3` 전수**: μ(**면적** 정의) 3.4 / 5.2 / **3.7** / 3.6 % · 계면셀 (14.32, 9.98, 89.8°) / (14.05, 9.63, 88.6°) / (**13.94, 24.46, 87.4°**) / (12.79, 31.15, 90.0°) · **W_ad 10.6 / 6.1 / 4.3 / 3.8 eV/nm² = 1.698 / 0.977 / 0.689 / 0.609 J/m²**(*환산은 우리 산수*). **`Table S2`**: W_surf **LCO(110) 14.08**(2.256 J/m²) · LNO(1̄0) 5.63 · LNO(110) 6.45 · **LPS(010) 1.94**(0.311 J/m²), 슬랩 갭 0.70 / 3.0 / 3.1 / 2.6 eV. **`Table S1`** 벌크: LCO a 2.835 c 14.04 **E_g 2.2** · LNO a 5.183 c 13.96 **3.6** · **LPS a 13.13 b 8.062 c 6.178 E_g 2.8 eV**. ★ **핵심 기전 = "산소 능선(ridge) vs 꼭짓점 산소(apical)"**: LCO(110)은 CoO₆ 를 옆으로 잘라 **두 O 를 잇는 능선**을 내밀고 거기에 **LPS 쪽 Li 이 흡착**한다 → **LPS 슬랩이 결정 질서를 잃고**(`Fig. 2`c 실독: PS₄ 방향 제각각) **`CoO₄S` 오면체**가 부분 형성 → **`Table 1`**: LCO\|LPS 의 **LP2 자리 E_v = 1.44 eV**(벌크 LPS **3.2** 대비 **−1.76**), 흡착 Li(LP1·LP4) 은 오히려 **3.27 / 2.90**, LCO 쪽 3.18–3.98; **LP2 → LCO 흡착자리 전달에너지 −1.6 eV**. **버퍼를 끼우면**: Nb–S 결합 없음 · Li 흡착자리 없음 · 두 슬랩 결정성 유지 · LPS 쪽 E_v **2.42–3.18 로 벌크 근처 복귀**(LP2→빈공간 전달 이득 **0.3 eV** 뿐). ★ ***우리 산수* 로 버퍼 효과를 수로 옮기면**: LPS 쪽 6자리 **최저 낙폭 −1.76 → −0.78 eV(회복 +0.98)** · **평균 낙폭 −0.54 → −0.25(54 % 감소)** · **자리 간 편차 1.83 → 0.76 eV(58 % 감소)** — **편차가 곧 "충전 초기 전압 기울기의 폭"** 이다(논문 미보고). **전자구조**: LNO 점유준위가 LCO VBM 보다 `figure-read ≈ −0.9 eV`(본문 "about 1 eV"), LNO\|LPS 는 **LPS 가 LNO 보다 `figure-read ≈ +1.6 eV`**(본문은 부호만) ⇒ **LNO 가 양쪽 모두에 전자 장벽**; 반면 **LCO\|LPS 는 갭 안에 계면 Co 3d 가 들어앉고**(`Fig. 3`b 점선이 `figure-read ≈ +0.55–0.95 eV` 에서 솟음 — (a)에서는 0) **`Fig. S7` 실독: VBM·CBM 둘 다 계면 Co 에 국소화**, 총 DOS 가 0 인 창이 `figure-read ≈ 0.05–0.35 eV` 뿐(실효갭 붕괴). ⛔ **NEB·AIMD·MD·MLIP·COHP·Bader·ELF·BVSE·grand-potential 전부 0회 — 후처리는 PDOS + E_v + W_ad + W_surf 뿐.** 🔴 **비판 6건**: ① **제목이 SCL 인데 SCL 이 한 번도 정량 안 된다** — 두께(nm)·전위(V)·층별 전하·Debye 길이 전부 0, **`Fig. 5` 는 축 라벨·눈금·단위가 하나도 없는 손그림**(실독 확인), 저자도 장거리 정전기 부재를 자인 ② **정량 클라이맥스인 "1.44 eV ↔ 실험 충전 개시 전압 일치" 에 그 실험 전압이 안 적혀 있다**(refs 5,8–10,13,14 뭉침) ③ **LCO 면이 (110) 하나인데 저자 스스로 (104)가 더 안정하다고 인용**(ref 26 Kramer&Ceder) — 핵심 기전(산소 능선)이 **(110) 전용 기하**인데 결론은 LiMn₂O₄·LiFePO₄ 로 일반화 ④ **결론이 걸린 계면의 표본이 가장 적다** — LCO/LNO 16개 vs **LCO/LPS 4개**, **LNO/LPS 는 9개 중 3개만**(건너뛴 기준이 *"이완 전 초기 에너지가 높아서"*), 표본 폭은 **6.19–9.07 eV** ⑤ **spin-unpolarized 인데 기전 주체가 Co 3d 국소준위**(면제 근거 0.2 eV 는 *LCO(110) 표면 Li passivation* 에서 잰 것이라 갭 안 준위에 적용되지 않는다) ⑥ **W_ad 의 변형 상쇄 불명 + 실제 선형변형이 "미스핏" 보다 크다** — *우리 산수* 로 `Table S2`↔`S3` 를 나누면 **LCO/LPS 의 LPS 가 한 축 +6.2 %**, **LNO/LPS 의 LNO 가 −8.4 %**(그리고 그 a=12.79 Å 은 논문이 밝힌 초기값 = 두 벌크 평균 13.545 Å 보다 **5.6 % 작다**, 설명 없음). 추가 ⚠ **LCO(110)/LNO(110) 계면 PDOS 는 논문 어디에도 없는데 "거의 같다" 고 단언** · **초록의 "Li migration" 은 NEB 가 아니라 끝점 에너지차 2개** · **총 원자수·슬랩 층수·법선 셀 길이·좌표·원시 총에너지 전부 미기재 ⇒ 재현 불가**(2017 편은 `Table S3` 로 총에너지를 공개했는데 2014 편은 없다). 🔧 ***우리 산수* 재현 추정**(⛔ 논문 값 아님): `Fig. S3` 캡션의 *"1st and 8th layer"* + `d₁₁₀ = a_hex/2 = 1.4175 Å` + `Fig. S6`c 2배 확대 실측(진공 1.5 nm 를 자로) ⇒ **LCO 8층 ≈11.5 Å · LPS ≈2 셀 16.7 Å · 법선 셀 전장 ≈43 Å · 정합 LCO 5×1 : LPS 1×4 · nat ≈ 480 + 256 = 736**(±15 %). ⭐ **우리 v5 의 근거 문장 원문 확보**: *"**Without this vacuum, the supercell approach always involves two interfaces, which are atomically different in most cases. Besides, artificial interaction between the two interfacial polarizations may arise … Therefore, the presence of the vacuum region is quite crucial.**"* ⇒ **anti-sandwich 논거 원문 검증 완료**. ⛔ **A–D 물성 4축 금지** → `comparison_vs_ours.md` **§J-(배정) `🔧 방법 원전`** + **§H 1행**. 🔴 **`refs.json[37]` 주석 정정 후보 1건**(아래 ④). 🎤 talk 역링크 해당 없음. | **우리 v5 계면 기하·anti-sandwich 논거의 원전 + SCL 서사의 현상 원전 (⛔ SCL *정량* 원전 아님)** — 물성값은 LCO/β-LPS/LNO 의 W_ad·γ·E_v·벌크갭 뿐, 아르지로다이트 0회 |

---

## ② `comparison_vs_ours.md` §📑 Reference key 에 추가할 행

| **[Haru14]** ⭐⭐⭐ **우리 v5 single-interface + vacuum 기하의 *원전* (= `db/literature/refs.json[37]`, method-anchor-PRIMARY)** · **[Haru17] 의 직계 선행 — 계면 3종을 만든 편** · ⛔ **LCO/β-Li₃PS₄/LiNbO₃ 계 — A–D 물성 4축에 *수치로* 넣지 않는다** | **Jun Haruyama**/**Keitaro Sodeyama**/**Liyuan Han**/**Kazunori Takada**/**Yoshitaka Tateyama\*** (NIMS MANA·GREEN + 京都大 ESICB + JST) 2014 ***Chem. Mater.* 26, 4248–4255** (DOI 10.1021/cm5016959; 접수 2014-05-11 / 게재 2014-07-03, **ASAP 재게재 07-09**; KAKENHI 23340089 · SPIRE+CMSI; 본문 8 pp · **SI 10 pp 보유** · refs 55+11 · 본문 그림 5 + 표 1 · SI 그림 7 + 표 4) — "**Space−Charge Layer Effect at Interface between Oxide Cathode and Sulfide Electrolyte in All-Solid-State Lithium-Ion Battery**". **계 = LCO(110)\|β-Li₃PS₄(010)** ± 버퍼 **LiNbO₃(1̄0)/(110)**. **방법 = 정적 DFT+U 슬랩**(QE · PBE · **spin-unpolarized** · USPP **40/320 Ry** · **U(Co 3d)=5.9 eV** · **계면 Γ-only** · 힘 0.001 Ry/bohr · 응력 0.5 kbar · 중성셀 · Gaussian **0.001 Ry** · ESM 점검만 · **진공 ≈1.5 nm** · 슬랩 1–2 nm · **무질서 = `β-Li₃PS₄-b` 정렬 단일배열**). **보고량 4종**: `W_surf=(E_slab−nE_bulk)/2S` · `W_ad=(E_A+E_B−E_AB)/S` · `μ=1−2S_{A∩B}/(S_A+S_B)`(**면적** 정의) · `E_v(Li_i)={E_tot(무Li)+μ_Li}−E_tot`(**μ_Li = Li 금속** ⇒ eV = V vs Li/Li⁺). 소환값: **W_ad 10.6 / 6.1 / 4.3 / 3.8 eV/nm²** · **W_surf LCO(110) 14.08 · LPS(010) 1.94 eV/nm²** · **벌크 E_v LCO 4.0 / LNO 5.1 / LPS 3.2 eV** · **계면 E_v 21개**(최저 **LP2 = 1.44 eV** @LCO\|LPS, **2.42** @LNO\|LPS) · **전달에너지 −1.6 eV / −0.3 eV** · 벌크갭 LCO 2.2 / LNO 3.6 / **LPS 2.8 eV**. ⛔ **NEB·MD·AIMD·MLIP·COHP·Bader·ELF·ESW·탄성 전부 0회.** 🔴 **핵심 비판**: ① **SCL 을 한 번도 정량하지 않는다**(두께·전위·Debye 0, `Fig. 5` 는 축 없는 손그림) ② **"1.44 eV ↔ 실험 충전 개시 전압" 의 실험값 미기재** ③ **(110) 한 면 · 표본 4개(폭 6.19 eV)** ④ **spin-unpolarized 로 Co 3d 갭준위를 논함** ⑤ **W_ad 변형 상쇄 불명 — 실제 선형변형 LPS +6.2 % / LNO −8.4 %**(*우리 산수*) ⑥ **nat·층수·법선 셀길이·원시에너지 전부 미기재 ⇒ 재현 불가**. ✅ **우리에게 주는 것**: **기하 프로토콜 + anti-sandwich 원문 + SCL 현상 서사 + "능선 O vs 꼭짓점 O" 판정 기준**. | `papers/haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md` |

---

## ③ `comparison_vs_ours.md` §J-(병합자가 배정) `🔧 방법 원전` 에 추가할 블록

### J-(배정). 🔧 **방법 원전 — [Haru14] 우리 v5 계면 기하의 *원전*, 그리고 그 원전이 *주지 않는 것*** (2026-09-22 신설)

**[Haru14] `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` — 산화물 양극|황화물 전해질 계면의 첫 DFT 편**
(⛔ 물성값은 **LCO / β-Li₃PS₄ / LiNbO₃** 의 W_ad·γ·E_v·벌크갭뿐. **아르지로다이트 0회 · Cl 0회 · MLIP 0회 · MD 0회 · NEB 0회.**
A–D 4축 행 금지. 아래는 **기하 대조표**와 **판정**뿐이다. ⚠ 전부 **소환값** — 우리 `db/properties/` 절대값과 섞지 않는다.)

#### (1) 기하 대조 — *판정하지 않고 나란히만 둔다* (판정은 1저자 몫)

| # | 항목 | **[Haru14] 원문** | **우리 v5 (현재 기록)** | 출처 |
|---|---|---|---|---|
| 1 | 계면 형식 | **단일 계면 + 진공** (샌드위치 명시적 반대) | **단일 계면 + 진공** | `refs.json[37]` |
| 2 | 진공 두께 | **≈1.5 nm** | **30 Å** (60 Å 에서 UMA W_ad 10× 폭주) | `kb/results/adhesion_v5_full_report.md` |
| 3 | 산화물 면지수 | **LCO (110)** (저자 스스로 (104)가 더 안정하다고 인용) | ⚠ **v5 보고서에 미기재**. v26/v27 은 LiNiO₂ (003)/(110)/(012)/**(104)** | `adhesion.json` |
| 4 | SE 면지수 | **β-Li₃PS₄ (010)** (Li 전도축 b 가 법선) | ⚠ **미기재** (LPSCl cubic 2×2×3) | — |
| 5 | 종단 | **화학양론**. LNO 만 활자(`−Li₂−Nb₂−O₆` / `Li₆Nb₆−O₉`), **LCO·LPS 미기재** | ⚠ **기술 없음** | — |
| 6 | 정합 방향 | **탄성계수 큰 쪽(LCO)에 맞춘다**; LNO/LPS 만 **두 벌크의 평균** | **SE 를 NCM 에 맞춘다** | v5 §2 |
| 7 | 정합 배수 | **LCO 5×1 : LPS 1×4** (*우리 산수*) | **SE 2×2×3(624) + NCM 7×7×1(196)** | v5 §2 |
| 8 | 미스핏/변형 | μ **3.7 %**(면적 정의) · **실제 선형 LPS +6.2 %**(*우리 산수*) | **strain +0.2 %**(Li6) / **+1.1 %**(Li5.4) | v5 §2 |
| 9 | 슬랩 두께 | **각 1–2 nm**; LCO ≈**8층/1.13 nm**, LPS ≈**2셀/1.66 nm**(*우리 산수*) | SE **30 Å**, NCM 미기재 | — |
| 10 | **총 원자 수** | ⛔ **미기재** (*우리 산수* ≈ **736**) | **820** (624+196) | — |
| 11 | 법선 셀 길이 | ⛔ **미기재** (*우리 산수* ≈ **43 Å**) | `cell_z = atoms_max + 30 Å` | — |
| 12 | 횡방향 샘플링 | **계통적 lateral slide 16 / 4 / 9**, 전부 이완 후 최저 채택. 표본 폭 **최대 9.07 eV** | **xy-shift 샘플링**(z-shift 는 슬랩 절단으로 폐기) | ✅ **발상 동일** |
| 13 | 이완 자유도 | **전 원자 + 횡방향 셀 자유. FixAtoms 없음** | **하단 33 % FixAtoms** (UMA 안정화) | `refs.json[37]` 이 이미 "우리만의 추가" 로 기록 |
| 14 | 초기 간격 | ⛔ 미기재 | **gap 2.5 Å** | v5 §4 |
| 15 | 힘 수렴 | **0.001 Ry/bohr = 0.0257 eV/Å** | **fmax 0.01 eV/Å** | — |
| 16 | **힘 계산기** | **DFT+U** (QE·PBE·USPP·U=5.9 eV·**Γ-only**) | **UMA-s-1p1 (MLIP)** | 🔴 **여기가 최대 차이** |
| 17 | W_ad 식 | `(E_A+E_B−E_AB)/S` | **동일** | ✅ |
| 18 | W_ad 값 | LCO\|LPS **0.689 J/m²** · LNO\|LPS 0.609 · LCO\|LNO(1̄0) **1.698** | comp1 LiNiO₂\|LPSCl **≈1.25 J/m²** | ⚠ 물질·방법 둘 다 다름 |
| 19 | γ | LPS(010) **0.311 J/m²** · LCO(110) **2.256** (DFT+U) | comp1 γ_SE **1.211 J/m²** (UMA, **정본 등록 없음**) | `adhesion.json` |
| 20 | 변형에너지 상쇄 | ⛔ **불명** — `E_A`·`E_B` 가 변형 셀인지 원래 셀인지 안 밝힘 | ✅ **우리는 이 함정을 스스로 기록**("STRAIN ARTIFACT ~30 eV", method_A) | v5 §4 |
| 21 | **SCL 정량** | ⛔ **없음**(두께·전위·Debye 전부) | ⛔ **없음** — `computational_methods_canonical.md` §2 가 **경계로 선언** | ✅ **아래 (2)** |

#### (2) ✅ **판정 1 — 우리 경계 선언이 문헌으로 지지된다**

`kb/methodology/computational_methods_canonical.md` §2 말미가 **"공간전하층 정량(두께·전위·Debye 길이) — 문헌도 정성뿐이라 '계산했다'고 말할 수 없다"** 를 우리 경계로 선언해 뒀다.
**[Haru14] 가 그 선언의 실물 증거다.** SCL 을 최초로 원자단위 계산했고 10년 넘게 인용되는 이 논문이, **두께도 전위도 Debye 길이도 한 번도 내지 않는다.** `Fig. 5` 는 **축 라벨·눈금·단위가 전혀 없는 손그림**이고, 저자들도 *"long-range variation … needs to be analyzed by methods involving the long-range electrostatic interaction"* 라고 자인한다.
⇒ *"문헌도 정성뿐"* 을 **추측이 아니라 확인된 사실**로 격상할 수 있다.

#### (3) 🔴 **판정 2 — "v5 는 Haruyama 를 따랐다" 라고 쓸 수 있는 범위**

| 쓸 수 있다 | 쓸 수 없다 |
|---|---|
| ✅ **프로토콜**: 단일 계면 + 진공, `W_ad=(E_A+E_B−E_AB)/S`, 계통적 횡방향 registry 탐색, 비대칭 이종계면에 샌드위치를 쓰지 않는다는 논거 | ⛔ **셀 크기·슬랩 두께·정합 수치를 "따랐다"** — 논문에 **총 원자수·층수·법선 셀 길이·좌표·원시 에너지가 없다** |
| ✅ **원문 인용**: *"the presence of the vacuum region is quite crucial"* (anti-sandwich) | ⛔ **W_ad 절대값을 나란히 놓고 "일치/불일치"** — 저쪽 DFT+U, 우리 UMA. **물질 차이와 방법 차이가 분리되지 않는다** |
| ✅ **SCL 서사**: "계면에 Li 흡착층 + 황화물 차표면 고갈" 이 제안됐다 | ⛔ **SCL 두께·전위·저항 수치** — 이 논문에 하나도 없다 |
| ✅ **"능선 O vs 꼭짓점 O"** 기하 판정 기준 | ⛔ **우리 계면에 그대로 적용** — 우리 NCM 면지수가 기록돼 있지 않다 |

#### (4) ⭐ **우리가 안 가진 축이 여기서 이름을 얻는다** → §H 후보 (아래 ③-b)

이 논문의 정량 지표는 **자리별 Li 공공 형성에너지 `E_v` 하나**인데, 그것만으로 SCL 서사 전체를 떠받친다.
**우리는 계면 Li 자리 E_v 를 한 번도 낸 적이 없다.** v5 구조가 이미 있으므로 **가장 싼 공백 메우기**다.
⚠ 다만 아지로다이트는 **무질서 배열 + free S²⁻ + Cl⁻** 라 **"자리" 가 유일하지 않다** ⇒ 우리 보고량 규율상 **스칼라 보고량이 정의되지 않는다**. **분포로 보고**하는 설계가 맞고, **중성 셀이면 전자가 어디 앉느냐(밴드정렬)가 값을 정한다**는 것을 [Haru14] 자신이 LNO 에서 보였다(벌크 5.1 → 계면 3.13–3.86 eV).

#### (5) *우리 산수* — 논문에 없는 정량 (병합 시 그대로 옮겨도 된다)

| 지표 (LPS 쪽 6자리) | **LCO\|LPS** | **LNO\|LPS** (버퍼) | 버퍼 효과 |
|---|---|---|---|
| 최저 `E_v` | **1.44** eV (벌크 3.2 대비 **−1.76**) | **2.42** eV (**−0.78**) | **+0.98 eV 회복** |
| 평균 `E_v` (LP1–6) | **2.662** eV (**−0.54**) | **2.950** eV (**−0.25**) | 낙폭 **54 % 감소** |
| 자리 간 편차 (max−min) | **1.83** eV | **0.76** eV | **58 % 감소** ← *"전압 기울기의 폭"* |
| 골격자리 LP4–6 낙폭 | −0.30 / −0.49 / −0.58 | −0.21 / −0.13 / **−0.06** | 거의 벌크 |

⚠ LNO **자신의** E_v 낙폭(−1.2 ~ −2.0 eV)은 **SCL 이 아니라 밴드정렬 인공물**이다(저자 자인). 혼동 금지.

---

## ③-b `comparison_vs_ours.md` §H(⚠️ 우리가 아직 못 하는 것 — 정직 목록) 에 추가할 1행

| **계면 Li 자리별 공공 형성에너지 `E_v`** (= 계면 Li 화학퍼텐셜 지도) | ⛔ **우리 원장에 0건.** v5 계면 구조는 있으나 자리별 E_v 를 낸 적이 없다 | **[Haru14]** 가 이 지표 **하나로** SCL 서사 전체를 세웠다 (`Table 1`, 21개 자리). 벌크 기준 LCO 4.0 / LNO 5.1 / **LPS 3.2 eV** | **가능하다** — QE 중성 셀 + μ_Li = Li 금속. ⚠ 단 아지로다이트는 **무질서 + free S²⁻ + Cl⁻** 라 "자리" 가 유일하지 않다 ⇒ **보고량 카드에 자리선택·집계규칙을 먼저 선언**하고 **분포로 보고**. 중성 셀이면 **밴드정렬이 값의 일부를 정한다**(Haru14 가 LNO 에서 실증) |

---

## ④ 🔴 병합자에게 — `db/literature/refs.json[37]` 주석 정정 요청 (⛔ 내가 고치지 않았다)

현재 `references[37].key_results.adhesion_energies_eVnm2._relative_to_us` 가 이렇게 적혀 있다:

> *"Our paper #1 v5 LiNiO2/LPSCl comp1 = 1.28 J/m² is ~2× their LCO/LPS = 0.69 J/m². **Reasonable: LiNiO2 more reactive than LCO per Komatsu (-424 vs -321 meV/atom).**"*

🔴 **이 귀속은 방법 축을 통제하지 않았다.** 저쪽은 **DFT+U (QE·PBE·USPP·U(Co 3d)=5.9 eV·Γ-only·전원자 자유이완)**, 우리는 **UMA-s-1p1 MLIP (FixAtoms 하단 33 %·vacuum 30 Å)** 다. **1.86× 비율이 물질 차이(Ni vs Co)인지 방법 차이(DFT vs MLIP)인지 이 자료로는 가를 수 없다.**
제안 문구 (한 줄 추가):
> *"⚠ 이 비율은 **방법 축이 통제되지 않았다** — Haruyama 는 DFT+U(전원자 자유이완), 우리는 UMA MLIP(FixAtoms 33 %). 물질 차이로 귀속하려면 **같은 계산기에서 LCO|β-LPS 를 한 번 재현**해야 한다."*

같은 항목의 `v5_method_vs_haruyama.verdict` (*"v5 = Haruyama method + UMA stability hack. STRONGEST literature backing for v5."*) 는 **프로토콜 수준에서는 원문과 맞다**(digest §3c-1 에서 4단계 전수 확인). 다만 *"기하를 따랐다"* 로 읽히지 않도록 **"프로토콜을 따랐다(셀 수치는 논문에 없다)"** 로 한정하는 것이 정확하다.

---

## ⑤ 실행 기록 (재현용)

- **그림 크로핑**: 재실행하지 **않았다**. `litdb/figures/haruyama2014_space_charge_layer_oxide_cathode_sulfide_se/figures.json` 의 `sources` 가 **정확히 지정된 두 PDF**(`11. ChemMater_2014_…_MAIN.pdf` + `11. Sup) …_SI.pdf`)로 이미 생성돼 있었고(2026-09-22 06:36), 본문 `Fig. 1`–`5` + `Table 1`, SI `Fig. S1`–`S7` + `Table S1`–`S4` **전 17장이 빠짐없이** 들어 있었다. **`--clean` 도 `--force_clean` 도 쓰지 않았다.**
- **글롭 사고 방지**: 파일명을 **전체 경로 문자열로만** 다뤘다. `11. *` 글롭은 한 번도 쓰지 않았다 (`11._Investigation_of_delamination…LLZO…` 와 섞일 위험).
- **본 그림 9장**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. S2` `Fig. S4` `Fig. S6` `Fig. S7` (+ `Fig. S6`(c) 2배 확대 크롭 1장).
- **안 본 것**: `Fig. S1` `Fig. S3` `Fig. S5` (근거는 digest 머리에) · `Table 1` `Table S1`–`S4` (표 = PDF 텍스트가 정확, **전량 전사**).
- **커밋 안 했다** (1저자 지시).
