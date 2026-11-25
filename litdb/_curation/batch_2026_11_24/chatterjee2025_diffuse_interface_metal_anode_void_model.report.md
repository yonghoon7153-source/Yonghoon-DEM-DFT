# 끝 보고 — chatterjee2025_diffuse_interface_metal_anode_void_model (2026-11-24 · litdb-curator)

쓴 파일: `litdb/papers/chatterjee2025_diffuse_interface_metal_anode_void_model.md` (635 줄 · 표 17 개 · 칸수 검사 0 건) · `litdb/figures/chatterjee2025_diffuse_interface_metal_anode_void_model/` (PNG 31 + figures.json) · 이 보고 파일. 공유 파일 · git · 코드 폴더는 안 건드렸다 (메인 체크포인트 커밋에 digest 앞판이 이미 들어가 있어서 지금 ` M` 로 보인다).
웹앱 확인 (읽기만): track **dem** · digested 2026-11-24 · `pis` = `[]` · 원소 태그 `Na` · methods 태그 없음 (`> methods: —`) · 그림 주석 f1–f17 · fS1–fS10 · t1 · t2 · tS1 연결됨.
⚠ slug 의 `li_anode` 는 지시대로 고정했지만 **논문이 푼 계는 Na 금속 | Na-β″-alumina** 다 (Li 계산 0). 바꿀지는 메인이 정한다 (바꾸면 figures 폴더 · figures.json 의 slug 도 같이).
서지: *J. Electrochem. Soc.* **172**, 070522 (2025) · DOI 10.1149/1945-7111/aded38 · 투고 2024-12-22 · 게재 2025-07-23 · 저자 Sourav Chatterjee (UF · LLNL) · Michael Tonks (UF) · William Gardner · Marina Sessim (QuantumScape) · 코드 souravmat-git/MOOSE-BatModelling @ 3e44674.

## (a) 인덱스

- **축 = DEM** (`webapp/data.py::literature_track` 점수 dem 3 : dft 1 — dem 은 type 문자열의 `fem` · ` continuum` · `multiphysics`, dft 1 은 제목 "Homogeneous" 의 `homo`). 제목을 고치면 뒤집힐 수 있으니 굳히려면 (메인 몫 · litdb 밖) `LIT_TRACK_OVERRIDE` 에 `"chatterjee2025_diffuse_interface_metal_anode_void_model": "dem",` 한 줄.
- **`INDEX_DEM.md`**: `python3 tools/litdb/build_index.py` 재생성에 맡긴다 → 묶음 = **"화학-기계 열화 · 계면"** (`group_of` 가 slug 의 `interfac` 로 잡음 · 확인함). 지금 `--check` 는 이 slug 를 "어느 인덱스에도 없음 [dem]" · "DEM 비교문서 미편입" 두 곳에만 띄운다 → (a) · (b) 로 풀린다.
- `INDEX.md`: **권고 안 함** (argyrodite 축 아님 · LPSCl 계면 실측 아님 · Jeff Sakamoto 공저 아님). 이 배치 (Li | SE 공극 · 점착) 를 `## 🧲 계면 점착 · 인터레이어 트랙` 표에 같이 모으기로 하면 아래 행 (3 칸):

```
| `papers/chatterjee2025_diffuse_interface_metal_anode_void_model.md` **(본문 25 pp + SI 17 pp · 크롭 31장 (도구 27 + 손 4) · 공개 코드 3e44674 줄 단위 대조)** | **[외부·계산(연속체 상장 · MOOSE)·🔧 방법 원전 — 물성 4축 비교 없음]** ✅ Sourav Chatterjee/Michael Tonks/William Gardner/Marina Sessim (UF · LLNL · **QuantumScape**), "A Diffuse-Interface Model for Predicting the Evolution of Metallic Negative Electrodes and Interfacial Voids in Solid-State Batteries with Homogeneous and Polycrystalline Solid Electrolyte Separators", *J. Electrochem. Soc.* 172, 070522 (2025) — **Na \| Na-β″-alumina** 2D 공극 상장: 계면 에너지 입력은 γ = 0.22 J m⁻² 하나 · 금속 \| SE 경계에 W · 접촉각 칸 없음 (상장 자연 경계 → θ 90° = 암묵 W = γ · 우리 추론) · l_w 0.5→0.7 µm 에 반공극 −13 % > GB 효과 ≤ 10 % · ⚠ 출판본 Fig. 10 = Fig. 12 같은 이미지 · 코드 저전도 κ_gb/κ_g 1.7×10⁻³ ≠ 본문 0.067 | W_ad (DEM-DFT) 공극 모델 자리 · 🔧 방법 원전 |
```

## (b) comparison

- `comparison_vs_ours.md` (DFT 축): **없음** (같은 계 · 같은 양 없음).
- `comparison_vs_ours_DEM.md` **§I 끝** (`### I-10` 블록과 그 아래 "2026-… 추가" 줄들 뒤 · `## J.` 앞) 에 한 줄 (물성 행이 아니라 🔧 방법 원전):

```
> 2026-11-24 추가 — 🔧 방법 원전 · `chatterjee2025_diffuse_interface_metal_anode_void_model` — Na | Na-β″-alumina 2D grand-potential 공극 상장 (MOOSE · 코드 공개 3e44674): 계면 에너지 입력은 **γ = 0.22 J m⁻² 하나** (Materials Project 인용 · aux/금속 · 공극/금속 · aux/공극 공통) 이고 **금속 | SE 경계는 상장 밖의 날카로운 고정 경계라 W · 접촉각 칸이 없다** — 공개 입력의 `[BCs]` 에 상장 변수 조건이 없어 자연 경계 → θ = 90° → 암묵 W = γ (우리 추론). 우리 W 를 쓰려면 젖음 경계조건 (Δγ_w = W − γ · 지금 모델 = 0) 을 코드에 넣고 γ 를 **같은 틀 · 같은 금속 면**으로 다시 내야 한다 (MP γ = PBE · 우리 W = PBE+D3 섞지 않음). 민감도: γ · W 시험 없음 · l_w 0.5 → 0.7 µm 에 반공극 −13 % (> GB 전도도 ≤ 10 %) · 우리 차수 어림 (모세관 / 전류 구동 Δμ @ 0.5 mA cm⁻²) 공극 규모 ≈0.4 % · 가장자리 ≈5–20 % → W 는 전체 성장 속도보다 가장자리 기하에 들어간다. 이 γ 는 W_ad 쪽 양이지 G_c 가 아니다 (I 축 규약 그대로) · 값 비교 행 없음.
```

## (c) pdf_map.tsv

**필수 아님** — digest 를 쓴 뒤 `extract_figures.py --inbox --only chatterjee2025` (드라이) 가 본문 · SI 를 **제목 49 %** 로 자동 매칭한다. 굳히고 싶으면 (손 크롭 경고 포함):

```
# ── Na | Na-β″-alumina 확산 계면 공극 상장 (Chatterjee … Sessim · J. Electrochem. Soc. 172 (2025) 070522 · 본문 25 쪽 + SI 17 쪽) — litdb 2026-11-24 · 파일 이름 'difint2025' 가 slug 와 안 겹쳐 제목 매칭 (49 %) 에만 기대고 있다
#   ⚠ 크롭 31 장 중 손작업 4 장 (tab_1 · tab_2 · tab_S1 · fig_A1 — manual_crop) · 다시 뽑을 때 --force_clean 쓰지 말 것
chatterjee2025_diffuse_interface_metal_anode_void_model	difint2025_void_diffuse_interface
```

## (d) 추가로 먹일 만한 논문 (8 편 · 전부 이 논문 참고문헌에서 서지 확인 · 최근 순 · litdb 에 **digest 없음** 8/8)

1. **P. Barai, T. Fuchs, E. Trevisanello, F. H. Richter, J. Janek, V. Srinivasan, "Study of void formation at the lithium | solid electrolyte interface", *Chem. Mater.* 36, 2245 (2024)** (ref 37) — 공극 상장 + **표면 확산** (이 모델이 빠뜨린 항 · 저자가 C_crit 차이 원인으로 듦) · Janek 그룹 실험 대조 · L_φ 를 실험으로 맞춘 선례. litdb 없음 (barai2021 은 다른 논문).
2. **S. Sinzig, C. P. Schmidt, W. A. Wall, "A conservative and efficient model for grain boundaries of solid electrolytes in a continuum model for solid-state batteries", *J. Electrochem. Soc.* 171, 040505 (2024)** (ref 81) — 다결정 SE 입계의 보존형 연속체 처리 = 이 모델의 "GB 폭 10³ 배 · 보정 안 함" 문제의 대안 (우리 SE 입계 채널 축). litdb 없음.
3. **Y. Zhao, R. Wang, E. Martínez-Pañeda, "A phase field electro-chemo-mechanical formulation for predicting void evolution at the Li–electrolyte interface in all-solid-state batteries", *J. Mech. Phys. Solids* 167, 104999 (2022)** (ref 36) — 직접 선행 공극 상장 · **크리프 · 역학 결합** (적층압 · 크리프 축) · Li/LLZO · 도금 후 가둬진 공극 (이 논문과 반대 결과). litdb 없음.
4. **J. Agier, S. Shishvan, N. Fleck, V. Deshpande, "Void growth within Li electrodes in solid electrolyte cells", *Acta Mater.* 240, 118303 (2022)** (ref 35) — 날카로운 계면 공극 성장 · 플럭스 문턱 · **C_crit = i·t_f 정의 원전** · 크리프. litdb 없음.
5. **V. Raj, V. Venturi, V. R. Kankanallu, B. Kuiri, V. Viswanathan, N. P. B. Aetukuri, "Direct correlation between void formation and lithium dendrite growth in solid-state electrolytes with interlayers", *Nat. Mater.* 21, 1050 (2022)** (ref 21) — **인터레이어** ↔ 공극 ↔ 덴드라이트 (Ag–C 점착 트랙에 바로 걸림). litdb 없음.
6. **Y. Lu, C.-Z. Zhao, … Q. Zhang, "The void formation behaviors in working solid-state Li metal batteries", *Sci. Adv.* 8, eadd0510 (2022)** (ref 30) — 이 논문이 반박한 **선형 공극 성장** 해석 모델의 원전 + 실험. litdb 없음.
7. **D. S. Jolly, Z. Ning, J. E. Darnbrough, J. Kasemchainan, G. O. Hartley, P. Adamson, D. E. Armstrong, J. Marrow, P. G. Bruce, "Sodium/Na β″ alumina interface: effect of pressure on voids", *ACS Appl. Mater. Interfaces* 12, 678 (참고문헌 표기 2019)** (ref 28) — **이 모델과 같은 계 (Na | NBA) 의 실험** · 압력 · 공극 · CCS 1.5–2.5 mA cm⁻² — 이 논문이 대조하지 않은 바로 그 실험. litdb 없음.
8. **J. Kasemchainan, S. Zekoll, D. Spencer Jolly, Z. Ning, G. O. Hartley, J. Marrow, P. G. Bruce, "Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells", *Nat. Mater.* 18, 1105 (2019)** (ref 19) — CCS/CCP 개념 원전 · 크리프 대 박리 경쟁. litdb 없음 (lee2022 · banerjee2020 digest 안에 인용으로만).
- 이미 litdb 에 있는 이웃 (같은 배치 · 병렬): `yang2021_atomistic_li_stripping_plating_interface_md` (= 이 논문 ref 33 · Mo 그룹 MD 점착 · 압력) · `yang2021_flat_li_stripping_lithiophilic_interface_design` (ref 34) · `wang2019_li_se_interface_dynamics_stack_pressure_current_density` (ref 18) · `kazyak2020_…` (ref 14) · `masias2019_…` (Li 크리프 · 참고문헌 밖) · `seymour2021_…` (점착 ↔ 공공 수송 · 참고문헌 밖).
- 참고문헌 밖 2024–2026 후보는 서지를 PDF 로 확인할 수 없어 넣지 않았다.

## (e) DEM-DFT 보고서에 쓸 거리 — 이 모델이 계면 에너지 · 점착을 어디서 어떤 꼴로 받나

1. **계면 에너지 = γ 하나 (0.22 J m⁻² · ref 77 Materials Project · 면 · 가중 미기재)** — 세 확산 계면 (aux/금속 · 공극/금속 · aux/공극) 공통. 꼴: `α = (3/4)γ l_w` · `m = 6γ/l_w` · 교차항 1.5 (Eq. 1 · p. 4) · `Table 1` (p. 6) · 코드 `single_void/Na_stripping_void_homogeneous_CC.i:40` (`sigma = 0.22`) · `:619–620` (α · m) · `:633` (`gab 1.5`). **직접 봄** (PDF 쪽 렌더 + 텍스트 · 코드 줄).
2. **점착 W 는 받는 칸이 없다.** 금속 | SE 경계 Γ_ed/el 은 상장 밖의 날카로운 고정 경계 (`Fig. 1a` p. 3 — **크롭 봄**, 접촉각 · 벽 에너지 표기 없음) · 경계조건 Eq. 14–18 (p. 5–6) 은 전류 · 전위 연속 + Na 플럭스 (× (1 − ξ_v)) 뿐 · 코드 `[BCs]` `:498–539` 에 상장 변수 조건 **없음** (경계 이름 `metal_sep_int` `:83–89`) — **직접 봄**. ⇒ 자연 경계 → θ = 90° → Young–Dupré 로 **암묵 W = γ** (이 해석은 **우리 추론** · 논문은 Eq. 19 가 접촉각을 무시한다고만 적음, p. 13).
3. **넣는 자리 · 꼴 (우리 추론)**: Γ_ed/el 위 ξ_v · ξ_m 에 젖음 경계조건 — 필요한 양은 차 하나 `Δγ_w = γ_SE/v − γ_SE/m = W − γ` (cos θ = W/γ − 1 · W ≥ 2γ 면 완전 적심). **지금 모델 = Δγ_w = 0 인 특수한 경우.** γ 와 W 는 같은 함수 · 같은 금속 면에서 쌍으로 (보고서 §7 규칙과 같음). 우리 쌍 (Li · Ag · C · LPSCl · NCM) 은 Na | NBA 가 아니라 그대로는 못 넣고 D · c_v^eq · κ · γ 를 Li | LPSCl 로 다시 매개변수화해야 한다. W 원장 위치 (값 안 실음): `db/properties/adhesion.json` · `db/properties/wad_*.json` · `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §2 · §7.
4. **민감도 — 논문은 γ · W 를 바꿔 보지 않았다 (n/a).** 바꿔 본 것: 계면 폭 l_w 0.5 → 0.7 µm 에 1 h 반공극 26.73 → 23.16 µm (**−13 %** · `Fig. A·1` p. 24 · **크롭 봄**) · GB 전도도 ×0.067–×10 에 반공극 최대 ≈6.4 % (`Fig. 13b` p. 17 · 크롭 봄) · ≈10 % (`Fig. 14e,f` p. 18 · 쪽 렌더만) · 다결정이면 접촉 상실이 9–12 % 늦음 (`Fig. 16c` p. 20 · 크롭 봄 · figure-read) · 전류 0.1 (외삽) → 0.6 mA cm⁻² 에 C_crit 0.78 → 0.58 mAh cm⁻² (`Fig. 15e` p. 19 · 크롭 봄).
5. **우리 차수 어림 (논문에 없음)**: 0.5 mA cm⁻² 에서 금속 안 ∇μ ≈ 5.3×10⁷ J mol⁻¹ m⁻¹ (`Fig. S8` 색막대 차수와 맞음 · 쪽 렌더) 대 Gibbs–Thomson γ v_m/r (r 4.8 µm 1.1 · r 0.5 µm 10.5 J/mol) → 모세관 비중 **공극 규모 ≈0.4 % · 가장자리 규모 ≈5–20 %** ⇒ 이 체제에서 W 는 전체 성장 속도보다 **가장자리 기하 · 국소 속도**에 들어간다. ⚠ 이 비율은 실험 근거 없는 A^m (11 f_c) 에 반비례 — 이상 희박 공공 열역학으로 읽으면 ≈11 배 커질 수 있다 (확신 낮음). W 가 더 중요해질 곳 = 저전류 · 휴지 · 핵생성 · 표면 확산 (이 모델이 안 푸는 것).
6. 보고서에 쓸 수 있는 한 문장 (외부용 · 내부 사정 없음): *"공개된 연속체 공극 모델 (J. Electrochem. Soc., 172, 070522 (2025)) 은 금속 | 고체전해질 경계에서 상장을 자연 경계로 두어 접촉각이 90° 로 고정된다 — 점착 에너지 W 를 쓰려면 젖음 경계조건을 더하고 금속 표면 에너지 γ 를 같은 방법으로 함께 내야 한다."* (뒤 절은 공개 입력 파일을 읽은 우리 판단이라고 밝힐 것.)
7. 같이 적을 경고: 전하이동 저항이 없어 공극 가장자리 전류가 1 차 분포의 특이점이고 결과가 l_w · Δx 에 묶인다 (`Fig. A·1` · `Fig. S9` 이산화 비대칭 ≤ 8 %) — W 민감도를 재려면 **l_w · 격자 수렴부터**.

## (f) 그림 크롭 요약

- `extract_figures.py --slug … --pdf <본문> <SI> --clean` → **27 장** (Fig. 1–17 · Fig. S1–S10) · 오탐 0. 손 크롭 **4 장** (300 dpi · figures.json `manual_crop` 사유): `tab_1` (Table I) · `tab_2` (Table II) · `tab_S1` (Table S.1 — 도구가 번호 공백 `tS1` 로 경고 · `missing_labels` 에 resolved 기록) · `fig_A1` (Figure A·1, 부록). **도구가 놓치고 경고도 안 낸 것**: 로마 숫자 표 (Table I · II) 와 가운뎃점 부록 그림 (Figure A·1) — 추출기 개선 후보 (메인 몫).
- 직접 본 크롭 **11 장**: Fig. 1 · 7 · 8 · 9 · 10 · 11 · 13 · 15 · 16 · S4 · A·1. 나머지 (Fig. 2–6 · 12 · 14 · 17 · S1–S3 · S5–S10) 는 PDF 쪽 렌더 (저해상도) 로만 봤다. 표 셋은 PDF 텍스트로 전사.
- **본문과 어긋난 것**: ① 출판본 **Fig. 10 = Fig. 12** (PDF 14 · 16 쪽이 같은 이미지 객체 xref 108 · 해시 동일 — 캡션의 균질 SE 도금 그림은 어디에도 없음) ② Fig. A·1 의 l_w 0.5 패널 라벨 26.73 µm 대 같은 조건 Fig. 7a(iii) 25.1 µm (색막대 최대 12.47 같음) ③ Table 2 "≲2 %" 가 0.5 mA cm⁻² 에서 3.6 % ④ Fig. 13b 저전도 곡선이 대부분 양 (+) — "느려진다" 는 국소 기울기 얘기 ⑤ Fig. 16c 에서 두 다결정 모두 접촉 상실이 늦음 (본문 미언급) ⑥ 표지 · 범례 잔실수 (Fig. 9a (i) ≈0.3 h · Fig. 15c (i) ≈0.19 h · Fig. 11b 도금인데 양 전류 · Fig. 14 "drops to 2%" 인데 그림은 −2 %).
- 코드 대조에서 나온 것 (그림 아님): 저전도 GB 입력은 Table I Arrhenius 그대로 → κ_gb/κ_g **1.7×10⁻³** (본문 · 그림은 0.067) · 저장소엔 0.5 mA cm⁻² 박리 입력만 (도금 · 순환 · 스윕 · 쌍결정 입력 없음) · 균질 단일 공극만 측정선이 계면에서 0.2 µm 안쪽.
- scratchpad 충돌 점검: **공용 이름 임시 파일 (main.txt · si.txt 등) 을 읽어 쓴 글자 없음** — PDF 는 Read 쪽 렌더와 fitz 로 `litdb/inbox/difint2025_*` 원본을 직접 읽었다. 내 임시 파일 (chk.py · extract.log · cap.py · build_index_check.log) 은 내 것임을 확인하고 `scratchpad/chatterjee2025_diffuse_interface_metal_anode_void_model/` 로 옮겼다 — 다시 대조할 것 없음.

## (g) Jeff Sakamoto

**저자 아님** — 저자 4 명 (Chatterjee · Tonks · Gardner · Sessim). 참고문헌 ref 14 · 16 · 17 · 18 · 23 에 'J. Sakamoto' 로만 나온다. 웹앱 `_paper_pis()` → `[]` 확인 · `batch.json` 의 `jeff_sakamoto: false` 와 일치 · INDEX 배지 불필요.
