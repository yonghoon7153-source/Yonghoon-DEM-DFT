# 끝 보고 — kazyak2020_li_penetration_ceramic_se_operando_microscopy (2026-11-24)

결과물 (내가 쓴 파일 셋뿐)
- digest `litdb/papers/kazyak2020_li_penetration_ceramic_se_operando_microscopy.md` (479 줄 · §0–§15)
- 그림 `litdb/figures/kazyak2020_li_penetration_ceramic_se_operando_microscopy/` (PNG 25 + figures.json)
- 이 보고 파일
- 공유 파일 · git 작업은 안 했다. `build_index.py --check` 만 돌렸다 — 이 slug 는 '어느 인덱스에도 없음' (합치기 전이라 정상) · 분류기가 **[dem]** 트랙으로 넣어 `comparison_vs_ours_DEM.md` 미편입 목록에도 뜬다.

논문 한 줄 — Al-LLZO 연마면에 Li 전극 두 개를 나란히 증착한 in-plane operando 광학 셀 (녹인 Li · 무압력 · 계면 < 5 Ω cm²) 로 침투를 찍었다. 형태 넷 (straight · branching · spalling · diffuse) · 침투 Li 가역 (dead Li · 끝 먼저 탈리 / 밑동 먼저 도금) · 성장 속도 ∝ 전류 (균열 하나 604 µm s⁻¹ mA⁻¹ · 문턱 · 전류를 끊으면 ≈3 µm 되밀림 = Li 크리프 → '기계적 균열 열림') · 깊은 방전 공극 (커패시턴스가 저항보다 먼저 꺾임) · 유리 Li₃PS₄ 도 straight · spalling (branching 없음). 원자 계산 0.

---

## (a) `litdb/INDEX.md` 에 넣을 행

넣을 절 — `## ✅ Digest 완료 (paper-level)` 표 맨 위 (최신 행이 위). 3 칸 표다.

```
| `papers/kazyak2020_li_penetration_ceramic_se_operando_microscopy.md` **(본문 25 pp + SI 21 pp · 크롭 25장 (도구 24 + 손 크롭 1 = Table S1 · 이미지로 박힌 표) · 실독 22 (본문 12/12 · SI 9/12 · Table S1 — 안 본 것 S4 · S8 · S10) · 2026-11-24)** | 🏷 **Jeff Sakamoto 공저** · **[외부·exp·⚠ 우리 계 아님 — 산화물 Al-LLZO 주 · 유리 Li₃PS₄ 한 셀 · 원자 계산 0 · COMSOL FEM 보조]** ✅ **Eric Kazyak**/R. Garcia-Mendez/W. S. LePage/A. Sharafi/A. L. Davis/A. J. Sanchez/K.-H. Chen/C. Haslam/**Jeff Sakamoto**/**Neil P. Dasgupta\*** (Univ. Michigan ME + MSE), "**Li Penetration in Ceramic Solid Electrolytes: Operando Microscopy Analysis of Morphology, Propagation, and Reversibility**" — ***Matter* 2, 1025–1048 (2020)**, DOI `10.1016/j.matt.2020.02.008` (OA). 같은 면에 Li 두 개를 증착한 in-plane operando 광학 셀 (녹인 Li · 무압력 · 계면 < 5 Ω cm² · 공칭 1–5 mA/cm² 침투 없음) → 침투 형태 넷 (straight · branching · spalling · diffuse) · 침투 Li 가역 (dead Li · 끝 먼저 탈리 / 밑동 먼저 도금 = 남은 균열 벽 비전도) · 성장 속도 ∝ 전류 (균열 하나 604 µm s⁻¹ mA⁻¹ · R² 0.95 · 문턱 · 되밀림 ≈3 µm = Li 크리프 → '기계적 균열 열림') · 깊은 방전 공극 (커패시턴스 급락 0.5–0.8 mAh/cm² 이 계면저항 상승보다 먼저) · 유리 Li₃PS₄ 도 straight · spalling (branching 없음). ⛔ 산화물 값 (CCD · 성장 속도 · ASR) 을 우리 LPSCl 값 옆에 두지 않는다 · 비판 11 (SI 조성 오기 25Li₂S–75P₂S₅ · 형태–전류 교락 · 커패시턴스 크기 · n = 1) | **Li 침투 = Li 찬 균열의 기계적 열림 · 방전 공극 · 침투 Li 가역 (E 축 · DEM/연속체 균열 · W_ad 보고서 §7)** (exp, 외부) |
```

- talk 인입 대기열 — 걸린 것 없음 (`grep` 으로 확인 · 🎤 역링크 불필요).

## (b) `comparison_vs_ours.md` 에 넣을 줄

① 📑 Reference key 표 (12 행 근처 · 약칭 새로)

```
| **[Kazyak20Op]** 🔧 **Li 침투 = Li 로 찬 균열의 기계적 열림 (Al-LLZO · in-plane operando 광학 · 무압력 · 녹인 Li) · 형태 넷 · 침투 Li 가역 · 방전 공극 (커패시턴스가 저항보다 먼저) · 유리 Li₃PS₄ 도 straight · spalling** · ⛔ **원자 계산 0 · 산화물 수치 (CCD · 성장 속도 · ASR) 를 우리 LPSCl 값 옆에 같은 양으로 두지 않는다 — A–D 물성 4축에 값 행을 만들지 않는다** (§E 행만) | **Eric Kazyak**/R. Garcia-Mendez/W. S. LePage/A. Sharafi/A. L. Davis/A. J. Sanchez/K.-H. Chen/C. Haslam/**Jeff Sakamoto**/**Neil P. Dasgupta\*** (Univ. Michigan) 2020 ***Matter* 2, 1025–1048** (DOI 10.1016/j.matt.2020.02.008 · OA CC BY-NC-ND) — "**Li Penetration in Ceramic Solid Electrolytes: Operando Microscopy Analysis of Morphology, Propagation, and Reversibility**" | ✅ `papers/kazyak2020_li_penetration_ceramic_se_operando_microscopy.md` (2026-11-24 · 크롭 25 장 중 22 장 실독) | exp (외부) · 원자 계산 0 · COMSOL FEM 보조 |
```

② `## E. 환원 / 음극(Li 금속) 계면` 표 맨 위 (4 칸 — 주장 | 출처 | 우리 | 일치)

```
| **🆕 (2026-11-24) Li 침투는 Li 로 찬 균열이 '기계적으로 열리며' 자란다 (Al-LLZO) — 성장 속도 ∝ 전류 (균열 하나 604 µm s⁻¹ mA⁻¹ · R² 0.95 · x 절편 ≠ 0 = 문턱) · 전류를 끊으면 ≈3 µm 되밀림 (Li 크리프) · 침투 Li 는 끝부터 빠지고 밑동부터 다시 찬다 (남은 균열 벽은 전자 비전도) · 유리 Li₃PS₄ 도 straight · spalling (branching 없음)** | **[Kazyak20Op]** `Fig. 8E,G` · `Fig. 9` · `Fig. 7H–L` · `Fig. 12` (실독) · p. 1038 (Li 와 반응해 전도성 계면상을 만드는 SE (LGPS · ref 47) 는 다를 수 있다는 저자 단서) | 우리 DFT 는 균열 · 크리프를 재지 않는다 — 걸리는 곳 둘: ① LPSCl 은 Li 에서 환원 분해 (Li₂S · Li₃P · LiCl · 이 절의 'Li₃P 딜레마') → '균열 벽 비전도' 가 LPSCl 에선 열린 질문 ② Li\|X 점착 · 젖음 = W_ad 보고서 §7 제안 (값 미계산 · 위치 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §7) | △ 정성 — 재료가 다르다 (산화물 · 유리 황화물 ↔ 결정 argyrodite) · 숫자 비교 없음 |
```

③ (선택) 분류기가 [dem] 으로 넣었으니 `comparison_vs_ours_DEM.md` 에도 한 덩이를 원하면 — `## C. 역학 / morphology` 또는 `## F. 우리가 아직 못 하는 것` 에:

```
> 🆕 (2026-11-24) **[Kazyak20Op] — 'Li 로 찬 균열' 의 operando 표적** (`papers/kazyak2020_li_penetration_ceramic_se_operando_microscopy.md` §6 · §11): 성장 속도 ∝ 전류 (균열 하나) · 문턱 · 되밀림 ≈3 µm · 같은 전하에 전진량 ≈1–27 µm (전류 분배 ≈15–35 % — digest 우리 산수) · spalling = 휘어 닫히면 들림으로 정지 · 분기 = 불순물 입자 · 균열 기하 = 표면 아래 얕게 누운 면 (가로 ≈450 · 깊이 ≲75 µm · figure-read). ⛔ 산화물 · 무압력 · 공칭 전류 — 값을 맞추지 않고 꼴만 재현 표적으로.
```

## (c) `pdf_map.tsv`

필요 없음 — `extract_figures.py --inbox --only kazyak2020` (매칭표만) 에서 본문 · SI 가 '제목 100%' 로 자동 매칭된다.

## (d) 추가로 먹일 만한 논문 (8 편 · 최근 순)

⚠ 2024–2026 이고 서지를 확신하는 후속은 Sandoval 2025 *Nat. Mater.* (Perspective — 이미 이번 배치에 digest `sandoval2025_electro_chemo_mechanics_anode_free_ssb` 있음) · Liao 2025 *Adv. Mater.* (litdb ✅) 뿐이다. 다른 최근 편은 서지를 지어내지 않으려고 넣지 않았다. 이번 배치에 이미 있는 이웃 (lee2022 · seymour2021 · sharafi2017 · wang2019 · masias2019 · chatterjee2025 · kim2026 공극 임피던스 · yang2021 둘 · shi2026 · cicvaric2026 · lu2026 · metzler 둘) 도 뺐다. litdb/papers 에는 아래 8 편 모두 **없다** (grep 확인).

| # | 논문 | 왜 (주제) | 서지 확인 |
|---|---|---|---|
| 1 | Ning et al., "Dendrite initiation and propagation in lithium metal solid-state batteries", *Nature* 618, 287–293 (2023) | **황화물 (Li₆PS₅Cl) 판 '균열 열림'** — 표면 아래 spallation 균열에서 시작, 횡단 균열이 Li 보다 먼저 열리고 Li 가 뒤에서 채운다 (operando XCT). 이 논문의 LLZO 결론을 우리 계로 옮기는 가장 직접적인 편 · 균열 → 침투 · 황화물 침투 | 내 기억 (DOI 미확인) |
| 2 | McConohy et al., "Mechanical regulation of lithium intrusion probability in garnet solid electrolytes", *Nat. Energy* 8, 241–250 (2023) | 국소 응력이 Li 침투 확률을 바꾼다 (LLZO) — 연속체 균열 모형의 응력 입력 · 균열 → 침투 | 내 기억 (DOI 미확인) |
| 3 | Kazyak et al., "Understanding the electro-chemo-mechanics of Li plating in anode-free solid-state batteries with operando 3D microscopy", *Matter* 5, 3912–3934 (2022) | 같은 Dasgupta 그룹 후속 — 무음극 첫 석출 · 3D operando · Li\|기판 (집전체) 접촉 | 내 기억 (권 · 쪽 미확인) |
| 4 | Fincher et al., "Controlling dendrite propagation in solid-state batteries with engineered stress", *Joule* 6, 2794–2809 (2022) | 외부 응력으로 침투 경로를 꺾는다 (LLZO) — '기계적 구동' 의 역검증 · 균열 경로 | 내 기억 (DOI 미확인) |
| 5 | Ning et al., "Visualizing plating-induced cracking in lithium-anode solid-electrolyte cells", *Nat. Mater.* 20, 1121–1129 (2021) | Li₆PS₅Cl · XCT · spallation + 횡단 균열 · 균열이 Li 보다 앞선다 — 황화물 침투 | 내 기억 (DOI 미확인) |
| 6 | Lewis et al., "Linking void and interphase evolution to electrochemistry in solid-state batteries using operando X-ray tomography", *Nat. Mater.* 20, 503–510 (2021) | Li\|Li₁₀SnP₂S₁₂ — 방전 공극이 계면상보다 저항을 지배 · **황화물 방전 공극** | 내 기억 (DOI 미확인) |
| 7 | Kasemchainan et al., "Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells", *Nat. Mater.* 18, 1105–1111 (2019) | Li₆PS₅Cl — 탈리 공극 → 다음 도금에서 덴드라이트 (이 논문 §5.6 공극과 같은 줄기 · 황화물) | ✅ lee2022 PDF 참고문헌 25 로 확인 |
| 8 | Porz et al., "Mechanism of lithium metal penetration through inorganic solid electrolytes", *Adv. Energy Mater.* 7, 1701003 (2017) | 이 논문 ref 6 — 과전압 ↔ Li 찬 균열 압력 ↔ 임계 결함 크기 모델 (단결정 LLZO · **유리 LPS**) · 균열 열림 기전의 원전 | ✅ 이 논문 참고문헌으로 확인 |

## (e) DEM-DFT 보고서에 쓸 거리 (W_ad 보고서 §7 · 연속체 / DEM)

쪽 = 인쇄 쪽 · '봄' = 내가 직접 본 그림 · [산화물] LLZO / [황화물] 유리 Li₃PS₄. 우리 W 값은 digest 에 싣지 않았다 (위치만). 자세한 판은 digest §11.

Li 친화성 · 젖음 (§7)
- [산화물] Li 를 녹여 (250 °C · 5 min · 무압력) 계면 < 5 Ω cm² · 안 녹이면 둘째 반원 — p. 1031 · `Fig. 2F` (봄) · `Fig. S5` (봄). '녹은 Li 젖음' 은 §7 의 0 K 고체 Li W/γ_Li 젖음각과 같은 양이 아니다 — 순서 비교용.
- [산화물] 새 균열 속 Li/LLZO 계면이 증착 계면보다 빠르다 (선호 도금 · 탈리) — p. 1036–1037 · `Fig. 6` (봄) — 깨끗한 표면 W 를 '균열 벽 계면' 으로 쓸 근거 (저자 가설).

점착 · 공극
- [산화물] 탈리 쪽 공극 · 도금 쪽 밀착 (FIB) — p. 1044 · `Fig. 11` (봄).
- [산화물] 공극의 선행 지표 = 커패시턴스 급락 0.5–0.8 mAh/cm² (4 mA/cm² · 8 µm Li · 무압력 · 방전 깊이 30–50 % 우리 산수) · 계면 ASR 은 ≥ 0.93 에서 상승 — p. 1043 · `Fig. 10E,F` (봄) · 커패시턴스 절대값은 쓰지 말 것 (≈50 mF/cm² 급 — Q→C 미기재).
- [산화물] 공공 확산 < 탈리 → 공극 → 접촉점 전류 집중 되먹임 — `Fig. 10G` (봄) · 연속체 공극 모형의 정성 틀.
- [산화물] 균열 밑동 공극 → 그 균열로 재도금 안 됨 (가설) — p. 1038 · `Fig. 5E` (봄).
- [황화물] CCD 의 전압 급상승을 공극으로 귀속 (LPS 사후 단면 없음) — p. 1045 · `Fig. 12E` (봄).
- 이 논문은 점착 에너지를 재지 않는다.

침투 (균열 열림 · 경로) — 연속체 · DEM
- [산화물] 성장 속도 ∝ 전류 · 문턱 (≈0.4 mA/cm² 공칭 · 우리 산수) · 되밀림 ≈3 µm — p. 1039–1041 · `Fig. 8` (봄) — '압력 받는 Li 찬 균열' 모형의 검증 표적 (꼴만). 같은 전하인데 전진 ≈1 · 14 · 24 · 27 µm → 전류 분배가 핵심 미지수 (균열 단면 상한 223 µm² · 전진에 쓰인 전류 ≈15–35 % 우리 산수).
- [산화물] straight 균열 기하 = 표면 아래 얕게 누운 면 (가로 ≈450 · 깊이 ≲75 µm) — `Fig. S7C` (봄) · 벌어짐 0.5–1 µm (`Fig. S7B` 봄) · 교차각 제각각 (`Fig. 3C` 봄).
- [산화물] 형태 넷 어휘 — p. 1031–1036 · `Fig. 3` (봄) · 분기 = 불순물 입자 (1.1 % 리튬 지르코늄 산화물 + 0.1 %) 에서 굴절 — p. 1034 · `Fig. 4` (봄) — DEM 결합 입자의 이종 입자 자리 · spalling = 휘어 닫히면 들림으로 정지 · 고립 영역 분쇄 — `Fig. 5` (봄) — DEM 파편화 형상 · 입자 관통 경로 — p. 1041 · `Fig. 9C,D` (봄) — '입계 전용' 가정의 반례.
- [산화물] 침투 Li 가역 · dead Li · 끝 먼저 탈리 / 밑동 먼저 도금 (벽 비전도) — p. 1036–1038 · `Fig. 6`, `Fig. 7` (봄). LPSCl 은 Li 에서 Li₂S · Li₃P · LiCl 로 분해 (Li₃P 전자누설) → 균열 벽이 전도성이 되면 도금 위치가 바뀔 수 있다 — 우리 DFT 쪽 새 질문 (Li\|Li₃P · Li\|Li₂S 띠 정렬 · W).
- [황화물] 유리 Li₃PS₄ 도 straight · spalling (branching 없음) — p. 1045 · `Fig. 12` (봄) · 한 셀 · 열간 가압 유리라 냉간 가압 결정 LPSCl 로 옮길 땐 단서.
- [산화물 · 모델] 공칭 → 국소 전류 ≈2.5–3 배 · 100 µm 막은 안쪽 가장자리 ≈6 mA/cm² — `Fig. S3` (봄) · 전기장 선 평행 — `Fig. S2` (봄) · COMSOL 매개변수 `Table S1` (봄 · σ_NE ≈0.21 mS/cm 우리 산수).
- Ag–C 인터레이어 crack 보고 (`docs/collab/agc_interlayer_crack_calc_2026_11_16.html` §1 — Ag 가 crack 을 따라 SE 안으로 · 일부 crack 엔 Li 흔적만) 와 기하가 닮았다 — 그 crack 속 Li 를 '압력 받는 Li 찬 균열' 로 볼 틀 (산화물 근거).

## (f) 그림 크롭 요약

- 도구 24 장 (본문 12 · SI 12) + 손 크롭 1 장 = **25 장**. 손 크롭 = `Table S1` (SI p. 4 · 이미지로 박힌 표라 캡션 앵커가 못 잡아 `missing_labels` 에 떴다) — 캡션 줄 + 이미지 bbox + 2 pt · 300 dpi · figures.json 에 `manual_crop` 사유 · `missing_labels` 비움. 캡션은 이미지라 내가 옮겨 적었는데, 첫 옮김에서 D_n 을 10⁻¹⁶ 으로 잘못 읽어 300 dpi 크롭과 대조해 **2×10⁻¹⁵** 로 고쳤다.
- 제외 1 건 'f10 p20 영역 없음' 은 정상 — PDF 20 쪽 (p. 1043) 은 'Figure 10. Continued' 캡션만 있고 패널 A–H 는 전부 19 쪽 `fig_10.png` 에 들어 있다 (직접 확인). 오탐 0 · 놓친 그림 0.
- 실독 22 장 (본문 12/12 · SI S1 S2 S3 S5 S6 S7 S9 S11 S12 · Table S1) · 안 본 것 S4 · S8 · S10 (값은 본문 · SI 텍스트로) · figures.json 에 `viewed` 표시.
- 그림이 본문과 어긋난 것 — `Fig. 10E` (계면 몫 ≈70 % vs '거의 전부') · `Fig. 10E,F` (저항 상승이 커패시턴스보다 ≈0.3 mAh/cm² 늦음 — 본문은 같은 구간이라 씀) · `Fig. S9` (점 13 vs 본문 18 셀 · 본문은 'S7' 로 가리킴) · `Fig. 8E,G` (같은 전류에서 세트 간 최대 4 배 · 같은 전하에 전진량 1–27 µm) · SI 표기 (25Li₂S–75P₂S₅ · 방전 '10 회' · 'Fig. X' · ref 5) — digest §10.
- scratchpad 충돌 대조 (한 줄) — 처음 공용 이름 `main.txt` 로 뽑았다가 7 쪽 이후가 다른 논문 (Lee 2022 *Joule*) 글자로 덮인 것을 발견해 slug 폴더로 다시 뽑았고, 공용 파일에서 읽은 PDF 6–12 쪽은 PDF 에서 다시 뽑아 대조했다 — 꼬리말 *Matter* p. 1029–1035 · digest 에 쓴 사실 15 개 전부 일치 · 'Joule' 0 회 → **오염 없음** (1–6 쪽은 처음부터 PDF 쪽 렌더 · 13–25 쪽 · SI 는 slug 폴더 텍스트로만 씀).

## (g) Jeff Sakamoto 저자 여부

**예 — 공저** (소속 ¹ U-M Mechanical Engineering · ² U-M Materials Science and Engineering · 자금 · 지도 · 착상 · 검토). 교신 (lead contact) 은 Neil P. Dasgupta. digest 저자 줄에 'Jeff Sakamoto' 로 적었다 (웹앱 배지) · (a) 행 둘째 칸 앞에 🏷 표시. 이해관계: 가특허 출원 · Zakuro Inc. CTO.
