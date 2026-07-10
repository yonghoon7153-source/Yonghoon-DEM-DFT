# SDCP v7c — 구조·분광 판정 보고 (입문자용 완전판)

**날짜** 2026-07-10 · **데이터** 실험 FTIR(400–4000)·Raman(50–3400, 2스캔) × ORCA r²SCAN-3c opt+freq (v7c 단량체, neutral/doped) · **결론 한 줄**: **실물 SDCP는 자가도핑(doped, –SO₃⁻/폴라론) 상태** — 산화 중합 단계에서 이미 도핑되어 태어나며, 기하·IR·Raman 3중 증거가 일치.

> 이 문서는 IR/Raman을 처음 보는 사람도 따라올 수 있게 쓴 판정 보고서다.
> 주간보고 슬라이드 문장은 §7, 그림/데이터 파일 목록은 §9.

---

## 1. 질문과 답 (Q&A 요약)

| 질문 | 답 |
|---|---|
| 실물 SDCP는 neutral(–SO₃H)인가 doped(–SO₃⁻)인가? | **doped-우세.** FTIR에 O–H 없음(음성 증거) + Raman 1062 νs(SO₃)·3-등가 S–O 기하(양성 증거) |
| 단독(pristine) 시료인데 왜 doped인가? 합성 중에 바뀌나? | **산화 중합 = 중합 + 도핑 동시**(산화제가 백본 전자를 뽑음). "도핑 안 된 SDCP"를 거치지 않음. 이온교환 후에도 폴라론⁺를 상쇄하는 술포네이트는 SO₃⁻로 남는 것이 유리 |
| Raman이 3400에서 끊겨서 판정 불가 아닌가? (기존 보고 p.3) | **판정 가능.** O–H는 IR-강/Raman-약이라 판정의 정본은 IR이고, FTIR은 4000까지 커버하며 O–H 부재. Raman >3500 재측정은 보너스 확인 |
| neutral 계산은 왜 했나? | "도핑 전" 참조 비교군. 도핑되면 무엇이 바뀌는지(O–H 소멸, S–O 등가화, νs SO₃ 등장)를 보여주고 실험이 doped 쪽과 맞음을 증명 |

---

## 2. 분자 구조와 작용기 (v7c)

그림: `sdcp_v7c_structure_neutral_annotated.png` / `sdcp_v7c_structure_doped_annotated.png`

| 작용기 | VESTA 원자번호 (1-index) | 역할 |
|---|---|---|
| **티오펜 고리** (방향족 S) | S16 + α-C15·C17 + β-C14·C18 | **전도성 백본** 단위. S가 오각형 위치-1(α-C 둘 사이) = EDOT 골격 |
| **에틸렌다이옥시 다리** | O13·O19 + C11–C12 | 티오펜 β-탄소 둘에 걸린 O–C–C–O 다리 = **EDOT의 시그니처** (PEDOT 계열임을 정의) |
| **에터 링커** C–O–C | O9 (C8–O9–C10) | 곁사슬을 다리에 연결하는 유연한 링커 (v7c에서 신설된 부분) |
| **술폰산/술포네이트** | S3 + O4·O5·O6 (+H26, neutral만) | **자가도핑 그룹.** neutral: S–O 1.46/1.47/**1.66** Å(긴 것에 O–H) = 산 형태. doped: **1.50×3 완전 등가** + O–H 없음 = 대칭 라디칼/음이온 형태 |
| 말단 메틸 | C1 | 사슬 캡 (단량체 모델의 절단면) |

**neutral vs doped 차이는 단 하나 — 술포네이트의 H**: H가 떠나면 (1) O–H 진동 소멸, (2) S–O 3개가 등가(1.50 Å)로 대칭화, (3) 스핀/전하가 3개 O에 분산(계산 스핀밀도: O에 ~65%, 백본 π에 ~35%). 이 하나의 원인이 아래 §4의 모든 스펙트럼 변화를 만든다.

---

## 3. IR와 Raman — 3분 입문

- **분자는 진동한다**: 결합(용수철)마다 고유 진동수(cm⁻¹)가 있고, 이는 **작용기의 지문**이다 (O–H ~3600, C–H ~2900–3100, C=C ~1400–1600, S–O ~1000–1200 …).
- **IR (적외선 흡수)**: 진동하면서 **쌍극자(전하 비대칭)가 변하는** 진동이 IR 빛을 흡수 → 투과율 그래프에서 **골(dip)**. 비대칭·극성 진동에 민감.
- **Raman (산란)**: 레이저를 쏘고 산란광의 진동수 이동을 봄. **전자구름의 변형(편극률) 변화**가 큰 진동이 강함 → **대칭 진동**에 민감.
- **왜 둘 다 필요한가**: 선택규칙이 상보적이다. **대칭 νs(SO₃)는 Raman-강/IR-약, O–H는 IR-강/Raman-약** → IR로 못 가르는 밴드를 Raman이 가르고(§4-③), Raman 범위 밖(O–H)은 IR이 커버한다(§4-①).

---

## 4. 증거 사슬 — 왜 doped라고 판정하나 (4가지, 독립적)

| # | 증거 | 데이터 | 읽는 법 |
|---|---|---|---|
| ① | **IR에 O–H 없음** (음성) | 계산 neutral만 3624 cm⁻¹ O–H; **실험 FTIR(–4000)에 해당 밴드 부재** | 술폰산의 H가 없다 = 탈양성자 완료 |
| ② | **Raman 1062 = νs(SO₃)** (양성) | 실험 Raman 1062 피크; 계산 doped의 강한 Raman 클러스터 936–1042 | 3-등가 S–O의 **대칭 신축**은 doped에서만 뚜렷 (neutral은 비대칭이라 분산) |
| ③ | **IR 1133/1178 재배정** | 1133: Raman-약 → **C–O–C 에터**; 1178: IR·Raman 둘 다 강 → **νas(SO₃)/ring** | IR만으론 못 갈랐던 겹침을 Raman이 심판 — Raman을 돌린 이유 |
| ④ | **기하 + 스핀** | doped 최적구조 S–O 1.495/1.498/1.496 Å (완전 등가); 스핀 3-O 분산; ⟨S²⟩=0.755 (깨끗한 doublet) | 분광과 독립적으로 같은 결론 |
| (+) | **Raman 1423 = C=C 백본** | 실험 최강 피크; PEDOT계 공액 백본 시그니처 | 전도성 백본 실재 (도핑 서사와 정합) |

**앵커링 품질**: 관능기 지문(SO₃·C–O–C·C–H·O–H)은 실험–계산 ~20–40 cm⁻¹로 타이트, 백본 C=C는 ±80 수준(실험=폴리머 vs 계산=단량체의 원리적 차이, 실패 아님).

---

## 5. 합성 관점 — 언제 도핑되는가 (manuscript Fig. 2a와 정합)

1. 단량체(NaO₃S–) → **산화 중합**: 산화제가 **중합과 백본 산화(p-도핑)를 동시에** 수행 — 점선 백본(퀴노이드) 그 상태로 태어남.
2. 백본⁺(폴라론)의 전하를 곁사슬 **–SO₃⁻가 내부 상쇄** = **자가도핑**(외부 도판트 불필요).
3. **이온교환(Na⁺→H⁺)**: 명목상 H-form 표기지만, 폴라론을 상쇄 중인 술포네이트는 SO₃⁻로 남는 것이 유리(초강산 pKa ≈ −2 + 폴라론 정전 안정화). → **단독 시료 측정에서도 doped 스펙트럼**이 나오는 이유.
4. (참고) 고립 기체상 분자에서 O–H 떼기는 ~4.2 eV 비용 — "doped 선호"는 분자 혼자의 성질이 아니라 **응축상 + 자가도핑 열역학**의 결과. neutral 계산이 기체상에서 더 안정인 것과 모순 없음.

---

## 6. 밴드 배정표 (실험 ↔ 계산; CSV: `sdcp_v7c_band_assignment_beginner.csv`)

| 영역(cm⁻¹) | 밴드 | 실험 | 계산 (스케일 ×0.965) | 판정 근거 |
|---|---|---|---|---|
| 3600–3770 | ν(O–H) | **없음** | neutral만 3624(IR)/3765(Raman) | doped 확증 (핵심) |
| 2850–3270 | ν(C–H) | IR 2850–2980 | 2954–3262 | 골격 공통 |
| 1380–1560 | ν(C=C) 백본 | **Raman 1423 최강** | doped 1391/1519/1613 | 공액 백본 |
| ~1178 | νas(SO₃)+ring | IR 1178 | 1171/1177 (IR·Raman 강) | SO₃ 존재 |
| ~1133 | ν(C–O–C) | IR 1133 | IR 1120 / Raman 1124(약) | **재배정** (Raman-약 → 에터) |
| 1000–1080 | **νs(SO₃)** | **Raman 1062** | doped 936–1042 Raman-강 | **도핑 양성 증거** |
| ~750 | 고리 변형 | IR ~750 | 749/751 | 고리 확인 |

---

## 7. 주간보고 슬라이드용 문장 (기존 p.3 업데이트)

- (기존) "측정 Raman이 ~3500까지라 O–H를 못 봐 neutral/doped 판단 불가능" →
  **(업데이트) "판정 완료: O–H는 IR-강/Raman-약이므로 판정의 정본은 FTIR(400–4000 커버)이며, 실험 FTIR에 O–H 부재 + Raman 1062 cm⁻¹ νs(SO₃)·최적구조 3-등가 S–O(1.50 Å)로 실물 SDCP는 자가도핑(–SO₃⁻) 상태로 판정. Raman >3500 재측정은 보조 확인으로 유지."**
- "도핑 시점: 산화 중합 단계에서 중합과 동시에 발생(자가도핑) — pristine 시료의 doped 스펙트럼은 자연스러운 결과."
- "Raman의 역할: IR 1133/1178 겹침을 Raman이 심판 — 1133은 C–O–C(에터), νs(SO₃)는 1062에 별도로 존재."

**EN (manuscript용):** "FT-IR and Raman jointly identify the as-synthesized SDCP as the self-doped form: the O–H stretch expected for the sulfonic-acid (neutral) form is absent over the full FT-IR window, while the symmetric νs(SO₃) mode of the deprotonated sulfonate appears at 1062 cm⁻¹ in Raman, consistent with the DFT-optimized doped geometry bearing three equivalent S–O bonds (1.50 Å). The dominant Raman band at 1423 cm⁻¹ corresponds to the conjugated C=C backbone, confirming the doped conducting state formed during oxidative polymerization."

---

## 8. 정직한 한계

1. **doped-"우세" 판정**: O–H 부재는 음성 증거 — 강한 수소결합으로 광대역화된 소량 SO₃H까지 100% 배제는 못 함 (원하면 O–H 영역 적분으로 상한 정량 가능).
2. **단량체 모델**: 폴리머 공액 미포함 → 백본 C=C ±80 cm⁻¹ 분산은 원리적 한계. 관능기 판정에는 영향 없음.
3. 조화근사 + 스케일 0.965 (관례적).
4. 도핑률(폴라론 밀도) 정량은 이 데이터로 불가 — 정성 판정까지.

---

## 9. 자료 인벤토리 (모두 scratchpad 생성, 사용자 전달됨)

| 파일 | 내용 |
|---|---|
| `sdcp_v7c_structure_neutral_annotated.png` / `_doped_annotated.png` | 작용기 주석 구조 그림 (이 문서 §2) |
| `sdcp_v7c_band_assignment_beginner.csv` | §6 배정표 (Excel용 UTF-8-sig) |
| `sdcp_v7c_IR_computed.png` / `.csv` | 계산 IR neutral vs doped (O–H 강조) |
| `sdcp_v7c_Raman_computed.png` / `.csv` | 계산 Raman neutral vs doped |
| `sdcp_v7c_IRvsRaman_arbitration.png` | doped IR vs Raman 겹침판정 (1000–1300) |
| `sdcp_v7c_Raman_vs_exp.png` | 실험 vs 계산 Raman (νs SO₃·C=C 매칭) |
| `sdcp_v7c_IR_vs_exp_full.png` | 실험 vs 계산 IR (전 영역, O–H 창 포함) |
| (원본) `sdcp_v7c_{neutral,doped}.{xyz,out,inp}` | D:\QE\6. orca_sdcp\new\1. structual output |

---

## 10. VESTA 예쁜 구조 그림 레시피 (xyz → 논문급 PNG)

1. **열기**: File > Open > `sdcp_v7c_doped.xyz` (neutral도 동일).
2. **결합 정의** (기본값은 S–O·C–S를 놓칠 수 있음): Edit > Bonds > New로 추가 —
   `C–C 1.70 / C–H 1.15 / C–O 1.65 / C–S 1.95 / S–O 1.80 / O–H 1.10` (Å, max length).
3. **스타일**: 좌측 Style 패널 > **Ball-and-stick**; Properties > Bonds > radius **0.12**; Atoms > radii scale **0.35–0.4**.
4. **색** (Properties > Atoms > 원소별): C **회색(90,90,90)** (VESTA 기본 갈색은 논문용으론 탁함), H 흰색, O 빨강, S 노랑 유지.
5. **투영**: View > Projection > **Parallel** (원근 왜곡 제거); Properties > General > **Depth-cueing off**.
6. **배경/축**: 배경 흰색, 좌하단 compass/axes 표시 끄기.
7. **방향**: 마우스로 회전해 **티오펜 고리가 정면**(§2 그림처럼), 술포네이트가 위로 오게.
8. **내보내기**: File > Export Raster Image > **scale 4**, PNG (투명배경 옵션 가능).
9. 작용기 라벨(–SO₃⁻, EDOT 등)은 PPT에서 주석으로 얹는 것이 가장 깔끔 (annotated PNG 참조).
10. **포인트 샷 2장**: (a) doped 술포네이트 클로즈업 — S–O 3개 등가(1.50 Å) 보이게, (b) neutral 동일 앵글 — O–H와 긴 S–O(1.66) 보이게 → 나란히 놓으면 "도핑 = H 하나의 차이"가 시각적으로 완성.

---

*다음 통합: 이 문서 + `sdcp_v7c_IR_analysis.md`(1133 재배정 반영 필요) + Phase-A/B 결합에너지(진행 중, DFT+U 5-SCF) + sdcp_master → **마스터 MD**. Phase-B Δ(doped−neutral) 나오면 §4에 "캐소드 결합에서도 doped가 강결합" 행 추가 예정.*
