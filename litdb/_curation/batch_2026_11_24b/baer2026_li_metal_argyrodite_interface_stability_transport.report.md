# 끝 보고 — baer2026_li_metal_argyrodite_interface_stability_transport (배치 2026-11-24b · #1)

- digest: `litdb/papers/baer2026_li_metal_argyrodite_interface_stability_transport.md` (새 파일 · 592 줄 · 한국어 standalone · §0–§16 + Post-processing 표)
- 그림: `litdb/figures/baer2026_li_metal_argyrodite_interface_stability_transport/` — 크롭 50 장 (본문 그림 13 · SI 그림 29 · 본문 표 6 · SI 표 2) 전부 도구 (`--pdf 본문 SI --clean`) · 손 크롭 0 · 번호 공백 0 (`missing_labels` = []). `figures.json` 에 전 항목 `viewed` / `viewed_how` 를 달았고, 캡션은 추출 잔재만 고쳤어요 (합자 ﬂ · ﬀ · ﬃ · 잃어버린 그리스 문자 γsurf · γinter · σ · 화살표 L → R · 줄바꿈 하이픈 · 표 캡션 뒤에 붙은 뒤섞인 표 본문 삭제 — 원문은 `caption_raw` 에 남김).
- 저장소: `/home/user/bkarasulu/li-argyrodite-interface` @`3f67da9` 읽기만 — 구조 파일 46 개를 ASE 로 읽어 셀 · 원자 수 · 조성 · 층 · 종결 · P–S 결합을 대조했어요. MACE 모델 3 개는 **안 돌렸고 안 열었어요** (zip 목록 · 크기 · sha256 만 · 안에 pickle 이 있어요).
- 공유 파일은 안 건드렸어요. `litdb/figures/_sources.json` 은 추출 도구가 이 slug 항목을 더해 다시 썼어요 (손 안 댐). git 작업 없음 — 메인 세션 checkpoint 커밋 `6e34402e` 에 크롭 50 장 + 원래 `figures.json` 이 이미 들어가 있고, 지금 `figures.json` 은 수정 (viewed · 캡션) 상태 · digest 는 미추적 상태예요.
- 점검 (읽기만): `build_index.py --check` → 이 digest 는 "어느 인덱스에도 없음 [dft]" + "comparison_vs_ours 미편입" (아래 (a) · (b) 를 넣으면 풀려요) · `extract_figures.py --inbox --only baer2026` (매칭표만) → 본문 + SI 자동 매칭 `[제목 72%]` · 웹앱 `/paper/<slug>` 200 · `paper_figures` 50 · `paper_figure_notes` 50/50 · `_paper_pis` = [] · 원소 페이지 Li · P · S · Cl 연결 ✓ · 기법 페이지 dft · md · mlip 연결 ✓ (AIMD 는 용어 사전에 항목이 없어 안 붙어요) · 시험: `test_v3_literature` + `test_v3_markdown` 43 개 중 42 통과 · 1 실패 = `test_todo_page_folds_every_ledger_fold` (`/todo` 가 `kb/open_items.md` 의 `<!-- … -->` 글자를 그대로 보여 줌 — 이 digest 와 무관 · 원래 있던 실패로 보여요) · `test_webapp -k "sakamoto or litdb_figure or recent_digests or digest_date or element_papers or glossary_papers or figure_comment"` 7 통과 1 실패 = `test_recent_digests_are_on_every_litdb_surface` (INDEX · comparison 미편입 — 합치면 풀려요).

⚠ **메인에 알릴 것**
1. **이 논문엔 W_ad · W_sep · γ_Li 가 없어요.** 있는 건 γ_surf (종결 28) · γ_inter (계면 3 · 두 벌크 기준) · E_str 뿐이고, γ_inter 는 0 K DFT 이완 중 일어난 반응 (잘린 PS₄ 의 P 가 S 를 다 잃음 · 저장소로 확인) 이 들어간 값이라 우리 W 와 같은 줄에 못 놓아요.
2. **최저 종결 셋은 셋 다 PS₄ 를 잘라 P 를 맨 바깥에 내놓은 '전하 있는' 판이에요** (+10 · +1 · +12). 우리 두 종결 (S 바깥 · Li·PS₄ 바깥) 은 이 논문 표에 없어요 — 면적비 · 안정성 순위 근거로 못 써요.
3. **선행 연구 숫자 불일치**: 본문이 Chaney · Ding 을 묶어 "up to 35 ns for a 21 120 atom cell" 이라고 썼는데, 우리 `chaney2024_…` digest 의 Chaney 셀은 7,956 · 31,824 원자 · 10 ns 예요. Ding (arXiv 2506.10944 · litdb 없음) 을 먹일 때 그쪽 숫자인지 확인해 주세요.
4. **`yuan2026_percolating_li2s_interphase_efield_md` 가 이 논문을 인용해요** (그 digest 63 행: 서론 refs 40–42 에 "Baer 2026 *J. Mater. Chem. A*"). 역링크를 달지는 메인이 정해 주세요 (남의 digest 라 안 건드렸어요).
5. **논문 자체의 그림 · 표 오류** (픽셀 · 산수로 잡은 것): `Fig. S6` D 라벨이 한 온도씩 밀림 (기울기로 읽으면 보고 Ea 0.18 · D300 5.8 × 10⁻⁷ 재현) · `Fig. S6` · `S7` 시간축 fs → ps · `Table S2` (100)/(010) 400 K 전극 53.4 대 그림 ≈530 (10 배) · `Table S2` (011)/(011) 400 K 전해질 L→R / R→L 뒤바뀜 · `Table 2` 전하 열 3 칸 · "426 atoms" (✎ 416) · 결론 "세 계면 모두 5 ns 안에 완전 분해" 대 `Table 5` > 5 ns. 인용 금지 규칙은 digest §14 에 걸었어요.
6. W_ad 보고서 INDEX 절 머리가 "18 편 한 묶음" 이라 이 배치 (11-24b) 를 넣으면 머리 문구도 같이 고쳐야 할 거예요.
7. 발견 검색 (최근 2 년 먼저): Crossref 주제어 검색 4 번 + DOI 확인 1 번 (일반 UA · 개인정보 없음). 넷째 주제어 검색은 HTTP 오류로 끊겼고 다시 안 쳤어요. 건진 것 2 편 (Kotakadi 2025 ChemRxiv · Westover 2025 JMCA) 은 (d) 에 넣었어요.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` — 행 순서상 **'계면 원자 모형 (DFT · MD)' 묶음 끝** (`cicvaric2026_…` 행 다음). 같은 Li | LPSCl SEI 이웃 (`chaney2024_…` · `wang2022_resistive_…` · `kim2026_li_argyrodite_sei_reactive_md` · `yuan2026_…` · `lai2025_…`) 은 `## ✅ Digest 완료` 절에 있어요 — 행 끝에 그 slug 들을 이웃으로 적었어요.

| `papers/baer2026_li_metal_argyrodite_interface_stability_transport.md` **(본문 16 pp + SI 18 pp · 크롭 50 장 (그림 42 + 표 8 · 전부 도구 · 번호 공백 0) · 그림 42 장 전부 봄 — 26 장 원해상도 · 16 장 축소 대조표 · 표 3 장 이미지 대조 · 저자 저장소 @3f67da9 구조 46 개 ASE 대조 · 2026-11-24)** | **[외부·DFT(VASP-PBE · vdW 없음)+AIMD+MLIP-MD(계면별 미세조정 MACE · 2220–2596 원자 · 300/400 K · 5–10 ns)·⭐⭐ 우리 W_ad 와 같은 Li \| Li₆PS₅Cl 계면 · ⛔ W_ad · W_sep · γ_Li 0 — γ_inter 는 0 K 이완 중 반응이 든 값 · 우리 W 와 같은 줄 금지]** ✅ **Chantal M. I. Baer\***/Roman Shantsila/Łukasz Figiel/**Bora Karasulu\*** (Warwick · WMG + Chemistry), "**Atomistic insights into the chemical stability and ionic transport at Li-metal/Li-argyrodite interfaces**" — ***J. Mater. Chem. A* 14, 20245–20260 (2026)**, DOI `10.1039/D6TA00922K` (CC-BY 4.0 · 저장소 `bkarasulu/li-argyrodite-interface` 는 LICENSE 없음). 대칭 비화학량 판 28 개 (6 면 · 환원 끝점 μ) γ_surf → 최저 (100) Li–P–S–Cl **1.006** · (011) Li–P–S–Cl **1.168** · (010) Li–P–Cl **1.225** eV nm⁻² (형식 전하 +10 · +1 · +12 · ✎ 셋 다 PS₄ 를 잘라 P 노출) — 우리 S 바깥 · Li·PS₄ 바깥은 표에 없음. 전하 맞춤 뒤 γ_surf 3.039 · 2.834 · 1.261 · γ_inter **−7.807 · −8.584 · −12.947** eV nm⁻² (✎ 완전 환원 P 는 전부 잘린 조각). MLMD: 세 계면 모두 전해질 판 전체가 0.35–0.57 ns (400 K) 에 비정질 Li₃P/Li₂S/LiCl → antifluorite **Li₂S₀.₇₂P₀.₁₄Cl₀.₁₄** (✎ = Li₁₄PS₅Cl = 7 Li₂X · [Chaney24SEI] 와 같은 산물) · c −14 ~ −21 % · 300 K (100)/(100) · (011)/(011) 5 ns 결정 없음 (관측창 ✎ 0.28 / 0.25 eV · n = 1). 3 Å 막 플럭스 400 K 1 ns: 벌크 35–37 · 계면 65–80 · 비정질 6.8–18.2 · 결정 SEI **0–0.93** atoms nm⁻² ns⁻¹ (✎ 사건 0–8 개 · 창 해상도가 1 mA cm⁻² 보다 6–7 자릿수 큼). 벌크 Ea(D*) 0.18 · Ea(σ) 0.12 eV (✎ 차 = σ 대 σT 의 kT̄) · σ300 0.139 S cm⁻¹. 🔴 `Fig. S6` 라벨 밀림 · `Table S2` 두 칸 · `Table 2` 전하 3 칸 · MACE S–P RDF 400 K ≈ AIMD 절반 (figure-read) · 최종 모델 test 오차 > AL 6 회째 · "426 atoms" (416) · 선행 Chaney 숫자 불일치 · 실험 0 | 점착 트랙: Li \| LPSCl 의 '젖음' 은 Li \| SEI (antifluorite) 문제 (W_ad 보고서 7 · 8 절) · 반응 부피 수축 ✎ −21 % (DEM 시나리오 후보) · UMA 반응 계면 검증용 공개 test 1500 프레임 · ⛔ 우리 W · MLIP Ea 와 같은 줄 금지 · 이웃 `chaney2024_…` · `wang2022_resistive_…` · `kim2026_li_argyrodite_sei_reactive_md` · `yuan2026_…` (이 논문 인용) · `lai2025_…` |

---

## (b) `comparison_vs_ours.md` 에 넣을 줄

**A–D 물성 4축: 본 자리는 없어요** (계면 · 음극 논문). 벌크 MLIP Ea 가 있어서 A 축 방향 행 하나는 선택으로 적었어요 (b-5).

### b-1. `📑 Reference key` 표에 한 행 (4 칸: 약칭 | 논문 | digest/status | 유형)

| **[Baer26LiArg]** 🔧 **Li 금속 \| Li₆PS₅Cl 계면 — 종결 28 훑기 (대칭 비화학량 · 전하 있는 판) + 계면별 MACE MLMD (5–10 ns) + 막 플럭스** · ⛔ **W_ad · W_sep · γ_Li 0 — γ_inter 는 반응 포함 · 우리 W 와 같은 줄 금지** · ⛔ **A–D 4축 진입 금지 (벌크 Ea 는 A 방향 행만)** | Chantal M. I. Baer\*/Roman Shantsila/Łukasz Figiel/Bora Karasulu\* (Warwick) 2026 ***J. Mater. Chem. A* 14, 20245–20260** (DOI 10.1039/D6TA00922K · CC-BY 4.0) — "Atomistic insights into the chemical stability and ionic transport at Li-metal/Li-argyrodite interfaces" | ✅ `papers/baer2026_li_metal_argyrodite_interface_stability_transport.md` — 판정은 §E 2 행 + §J (방법) + (선택) A 방향 행 | DFT (VASP-PBE) + AIMD + MLIP-MD (MACE) · 실험 0 |

### b-2. §E 표에 두 행 (4 칸: 주장 | 출처 | 우리 | 일치)

| **🆕 (2026-11-24) Li \| Li₆PS₅Cl 세 종결 모두 0 K DFT 이완에서 이미 반응 (γ_inter 셋 다 음수) · MACE MLMD 300 / 400 K 에서 전해질 판 전체가 비정질 Li₃P/Li₂S/LiCl → antifluorite Li₂S₀.₇₂P₀.₁₄Cl₀.₁₄ (✎ = Li₁₄PS₅Cl = 7 Li₂X) · 종결은 분해 · 결정화 속도만 바꾼다** — ⚠ 0 K 에서 완전 환원된 P 는 전부 종결이 이미 자른 PS₂ · PS₃ 조각 (✎ 저장소 P 추적) · 종결 효과와 전하 맞춤 효과가 안 갈림 (지울 P 만 바꿔도 결정화 시작 0.23–0.41 ns · 대칭 맞춤 4.73 ns) | **[Baer26LiArg]** `Table 4` · `Table 5` · `Table S1` · `Fig. 6`–`Fig. 11` · `Fig. S14`–`S26` (VASP PBE · vdW 없음 · 셀까지 이완 / MACE · LAMMPS NPT · 2220–2596 원자) | 우리 0 V 산물표 반응식 (`anode_interface_b2o3.json` · **BLOCKED** `HZ-anode-b2o3-reaction-direction`) · 산물 종류 Li₂S · Li₃P · LiCl 은 같다 · 음극 계면 MD 0 | ✅ **[Chaney24SEI] 와 같은 산물 · 같은 조성 (다른 MLIP: MACE 대 MTP)** · 🔴 우리 반응식 방향 오류 재확인 (새 판정 아님) · ⛔ 분해 · 결정화 시간 (`Table 5`) 을 실제 SEI 성장 속도로 인용 금지 — 전해질 판이 0.4–0.6 ns 에 통째로 바뀜 = 반응물 소진 · 부동태 없음 (중성 Li 확산) · MACE S–P 결합 약화 의심 (`Fig. S4` figure-read) |
| **🆕 (2026-11-24) "결정 SEI 가 Li 수송 병목" — 400 K · 1 ns 3 Å 막 통과: 벌크 Li₆PS₅Cl 35.1 / 37.0 · 계면 65–80 · 비정질 SEI 6.8–18.2 · 결정 SEI 0–0.93 atoms nm⁻² ns⁻¹** — ✎ 결정 SEI = 4.2–6.0 nm² × 1 ns 에서 사건 0–8 개 · 관측창 (400 K · 1 ns · n ≈ 55): 기대 사건 1 ≈ 0.46 eV (검출 63 %) · 95 % 검출 ≈ 0.42 eV · 창 최소 교환율 ≈ 2.4 × 10⁸ nm⁻² s⁻¹ 대 1 mA cm⁻² = 62 Li nm⁻² s⁻¹ | **[Baer26LiArg]** `Table 6` · `Table S2` · `Fig. 12` · `Fig. 13` · `Fig. S27`–`S29` | 음극 계면 수송 계산 없음 · 우리 MLIP-MD 는 벌크만 (`litdb/our_dft_baseline.md` 축 A · 상대차 정책) | ⚠ **셀 저항 · 상온 σ 근거로 인용 금지** — ns 창에서 '교환이 드물다' 까지만 · 🔀 [Wang22Res] (Li₃P 쪽 통로) · [Yuan26Perc] (Li₂S 계면상 수송 · 장 구동) 와 정의 · 방법이 달라 같은 줄 금지 · (우리 가설) P : Cl = 1 : 1 이 틈새 Li 와 Li 빈자리를 상쇄해 운반자가 적다 — 시험 안 됨 |

### b-3. §J 끝에 블록 (지금 J-91 · **J-92** 제안 · 번호는 메인이 정해 주세요)

### J-92. 🔧 **방법 원전 — [Baer26LiArg] Li \| Li₆PS₅Cl 계면: 종결 28 훑기 (대칭 비화학량 판 · 환원 끝점 μ) · γ_inter (두 벌크 기준 · 반응 포함) · 계면별 MACE · 3 Å 막 플럭스 — 우리 W_ad 의 종결 · 정의 · 검증과 대조** (2026-11-24 신설)

📎 **출처**: `papers/baer2026_li_metal_argyrodite_interface_stability_transport.md` (그림 42/42 · 26 장 원해상도 · `Fig. S6` · `S7` 기울기 판독 · 저자 저장소 @3f67da9 구조 46 개 대조)

⛔ **A–D 물성 4축 표에 행을 만들지 않는다** (벌크 Ea 는 선택 A 방향 행만) — 판정은 **§E 2 행**. 우리 W 값은 위치만 (`db/properties/adhesion.json` · `db/properties/wad_*`).

| 항목 | [Baer26LiArg] 가 보이는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| 종결 만들기 | pymatgen 대칭 비화학량 판 28 (6 면 · (111) 없음) · PS₄ 를 자르는 틈 포함 · 형식 전하 −12 ~ +12 (중성은 (110) Li–S 하나) | 입방 (001) 을 PS₄ 안 끊는 두 틈에서 → 화학량 비대칭 판 둘 (S 바깥 · Li·PS₄ 바깥) | 🟡 **대응 없음** — 최저 셋은 'P 노출' 셋째 꼴 (✎ 바깥 1 Å 안 P 0.95–1.34 · Cl 0.95–2.01 nm⁻²) |
| 순위의 강건성 | 전하 있는 판 순위 · 전하 맞춤하면 (100) 1.006 → 3.039 · (010) 1.225 → 2.834 (중성 (110) Li–S 2.053 보다 높아짐) · 나머지 25 판 중성화 안 함 | 순위 안 냄 (시나리오 양 끝) | ✅ 우리 '비율은 계산이 모름' 유지 |
| 계면 에너지 | γ_inter 식 (9) — 두 **벌크** 기준 · 셀까지 이완 · 이완 중 P 환원 · 중성 −7.8 ~ −12.9 eV nm⁻² · γ_inter^min 정의만 (값 없음) | 고정 기하 W_sep · registry 평균 · UMA+D3 | ⛔ **같은 표 금지** · ✎ Dupré 역산 하한 1.74–2.28 J m⁻² 는 반응 에너지 (인용 금지 · 설명용) |
| Li 쪽 | Li bcc (100) 12 층 · (100) sym 11 층 · (110) 6 층 · E_str 만 · γ_Li 0 · ✎ (100) sym 이완 판은 bct (c/a ≈ 1.24 · CN 12) 로 변함 | 7 절 제안 (같은 방법 · 같은 Li 면의 γ_Li) | 🔑 Li 슬랩은 **bcc 가 유지되는지** 이완 뒤 CN 으로 확인 |
| MLIP 검증 | E · F RMSE (계면 AIMD 500 · 벌크 400) + RDF · S–P 첫 봉우리 400 K MACE ≈ AIMD 절반 (figure-read) · 최종 모델이 AL 6 회째보다 나쁨 · 보고량 (분해 시간 · 플럭스) DFT 대조 0 | 보고량 W 자체를 같은 배치 · 같은 끝점 · 같은 D3 로 DFT 대조 | ✅ 우리 방식이 더 엄격 · 🔑 반응 계면이면 결합 끊김 통계 (CN · RDF) 를 더한다 |
| 수송 | 3 Å 막 양방향 통과 횟수 (교환 빈도 · 순 수송 아님) · 포아송 오차 없음 | 벌크 MSD 2–50 ps · NE Haven = 1 | ⚠ 막 플럭스는 σ 와 같은 양이 아니다 |

**인용 위생**: `Fig. S6` 라벨 · `Table S2` (100)/(010) 400 K 전극 · (011)/(011) 400 K 전해질 칸 · `Table 2` 전하 3 칸 인용 금지 · 벌크 Ea 0.18 / 0.12 차를 '불확도' 로 인용 금지 (✎ σ 대 σT) · 불확도 ±5 × 10⁻⁶ eV 류 인용 금지 · 장벽 0.18 eV 는 300 K 홉 대기 ≈0.11 ns (ν₀ 10¹³ s⁻¹ 가정) — 서술과 맞음.

### b-4. (권장 · 점착 트랙의 실제 집) `comparison_vs_ours_DEM.md` §I 에 블록 (지금 I-22 · **I-23** 제안)

### I-23. `baer2026_li_metal_argyrodite_interface_stability_transport` — ★★ (DFT · MLIP · ⛔ W 아님) **Li \| Li₆PS₅Cl 은 닿는 순간 반응한다 — 젖음 · 공극 판정의 상대는 SEI (antifluorite Li₂X)** · 반응 부피 수축 ✎ −21 %

- **무엇**: 종결 셋 모두 0 K DFT 이완에서 노출 P 가 환원되고 (γ_inter < 0), MLMD 에서 전해질 판 전체가 antifluorite Li₂S₀.₇₂P₀.₁₄Cl₀.₁₄ 로 바뀐다. 결정 SEI 를 지나는 Li 통과는 1 ns 에 0–8 번.
- **점착 트랙에 주는 것 셋**: ① W_ad 보고서 7 절의 Li \| 재료 W 에 Li \| LPSCl 을 넣는다면 **"반응 전 고정 기하" 인지 "반응 뒤 산물 계면" 인지 상태를 선언**해야 W 가 정의된다 — 실제 접촉은 곧 Li \| SEI 다 ② 문헌 Li \| Li₂S W (`wang2022_…` · `seymour2021_…` · 소환값) 는 2γ_Li 문턱 아래라 "SEI 가 생긴 Li \| LPSCl 은 소Li 쪽" 서술이 가능 — 순서만 ③ 이 논문의 종결 순위는 우리 두 종결의 면적비 근거가 아니다.
- **DEM 쪽 쓰임**: 반응 부피 수축 — ✎ Li₆PS₅Cl + 8 Li → Li₃P + 5 Li₂S + LiCl 은 반응물 부피의 약 −21 % (저장소 PBE 이완 LPSCl 248.2 Å³ f.u.⁻¹ + bcc Li 20.34 Å³ × 8 → `wang2022_resistive_…` digest 의 PBE 산물 부피 합 325.3 Å³) · MLMD c 길이 −14 ~ −21 % (면적 불변 가정 ✎ f.u. 당 −91 ~ −112 Å³). '계면 반응 = 국부 수축 → 접촉 감소' 시나리오 입력 후보 (속도는 이 논문에서 안 가져온다).
- **금지**: γ_inter · γ_surf 를 우리 W · γ 와 같은 줄 · `Table 5` 시간을 SEI 성장 속도로 · "결정 SEI 가 Li 를 막는다" 를 셀 저항 근거로.

### b-5. (선택) A 축 방향 행 (4 칸)

| **🆕 (2026-11-24) [Baer26LiArg] 무질서 Li₆PS₅Cl (4a/4c 50 : 50 · 단일 배치) MACE MLMD 2 × 2 × 2 · NPT 1 ns · 400–1000 K — Ea(D*) 0.18 eV · D*(300 K) 5.8 × 10⁻⁷ cm² s⁻¹ · σ(300 K) 0.139 S cm⁻¹ (MSTD 기반 D_σ · Ea(σ) 0.12 eV)** — ✎ Haven 0.72–0.88 · ✎ Ea 두 값의 차 ≈ kT̄ (σ 대 σT) · 600 K 40 ps AIMD 에서 질서 구조는 cage 안만 | **[Baer26LiArg]** `Fig. 4` · `Fig. 5` · `Fig. S6` · `Fig. S7` (⚠ `Fig. S6` 라벨 한 칸 밀림 — 기울기 판독값으로 재현) | 우리 UMA MLIP-MD (`litdb/our_dft_baseline.md` 축 A · 상대차 정책) — 모델 · 앙상블 · MSD 창 · 온도 점 · Haven 처리 다름 | 🟡 **방향만 같음** (무질서가 장거리 확산을 연다) · ⛔ 같은 줄 금지 · σ 0.139 는 실험의 수십 배 (저자: 결함 · 입계 없음) · 홉 수 검산 (ν₀ 10¹³ s⁻¹ 가정 · 300 K): Γ ≈ 9.5 × 10⁹ s⁻¹ · 1/Γ ≈ 0.11 ns |

---

## (c) `pdf_map.tsv`

**필요 없어요** — digest 를 쓴 뒤 `extract_figures.py --inbox --only baer2026` (매칭표만) 가 본문 + SI 둘을 자동으로 붙였어요 (`[제목 72%]`). 굳히고 싶으면 한 줄:

```
baer2026_li_metal_argyrodite_interface_stability_transport	baer2026_li_argyrodite_interface
```

---

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

> litdb 에 이미 있는 이 논문의 참고문헌 · 이웃 (세지 않음): ref 1 `famprikis2019_…` · ref 10 `deklerk2016_…` · ref 13 `morgan2021_…` · ref 15 `damore2022_…` · ref 19 `wang2022_resistive_…` · ref 20 `chaney2024_…` · ref 45 `mccluskey2025_…` · ref 46 `marcolongo_…` · ref 47 `he2018_…` · 이 논문을 인용한 `yuan2026_…`.
> 대조: `litdb/papers` 파일 이름 + digest 본문 grep · `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md` grep. 참고문헌 목록엔 제목이 없어서 1 · 2 · 3 만 제목을 적었어요.

| # | 문헌 | 왜 (우리 축) | litdb | 목록 |
|---|---|---|---|---|
| 1 | Kotakadi, Aspinall, Burton, Liang, Aihara, Pasta · ChemRxiv (2025-08-28) — *"Impact of metallic interlayers at the lithium – Li6PS5Cl solid electrolyte interface"* · DOI 10.26434/chemrxiv-2025-bfts2 (Crossref 확인 · **미심사**) | W_ad 7 절 금속 인터레이어를 Li \| LPSCl 에서 직접 — 점착 트랙 정조준 | 없음 | 없음 |
| 2 | Westover, Browning, Cannavó, Gilles, Vacik, … · *J. Mater. Chem. A* 13, 35435 (2025) — *"Measuring the buried interphase between solid electrolytes and lithium metal using neutrons"* · DOI 10.1039/d5ta05758b (Crossref 확인) | 실험 계면상 두께 — MLMD 'SEI 64 Å · ns 성장' 과 대볼 실측 | 없음 | 없음 |
| 3 | Ding, Zichi, Carli, Wang, Musaelian, Xie, Kozinsky · arXiv:2506.10944 (2025) — *"Coupled reaction and diffusion governing interface evolution in solid-state batteries"* (ref 21 · 미심사) | 같은 계 최대 300 만 원자 · SEI 두께 정의 원전 · 메인 알림 3 (Chaney 숫자) 확인처 | 없음 | **목록에 있음** ('그 밖' · 저널판 미확인) |
| 4 | Sen & Karasulu · *J. Mater. Chem. A* 13, 19878 (2025) (ref 55) | 막 플럭스법 · E_str 식 · Li₃P–Li₂S 고용체 수송 — 이 논문 방법의 원전 | 없음 | 없음 |
| 5 | Shantsila, Baer, Bartók-Pártay, Karasulu · ChemRxiv (2026) · DOI 10.26434/chemrxiv.15001544/v1 (ref 31 · 미심사) | STING 능동학습 — 반응 계면 MLIP 학습 흐름 (우리 UMA 미세조정 판단용) | 없음 | 없음 |
| 6 | Szczuka, Karasulu, … Grey · *J. Am. Chem. Soc.* 144, 16350 (2022) (ref 60) | Li₃P–Li₂S 고용체 전도 — '결정 SEI 막힘' 주장과 갈라 볼 자료 (같은 antifluorite) | 없음 | 없음 |
| 7 | Golov & Carrasco · *ACS Appl. Mater. Interfaces* 13, 43734 (2021) (ref 17) | Li \| LPSCl 계면 4 종의 Li 이동 장벽 (DFT) — 이 논문에 없는 계면 장벽 (Q4) | 없음 (다른 digest 에 인용만) | 없음 |
| 8 | Cheng, Merinov, Morozov, Goddard · *ACS Energy Lett.* 2, 1454 (2017) (ref 18) | Li(100)/LPSCl(100) AIMD 분해 — 0 K 분해 서술의 원형 | 없음 | 없음 |

다음 순번: Gao, Jalem, Tateyama · *ACS Appl. Mater. Interfaces* 12, 16350 (2020) (ref 53 · γ_inter 식 원전) · Wenzel et al. · *Solid State Ionics* 318, 102 (2018) (ref 59 · XPS 계면상 실측) · Camacho-Forero & Balbuena · *J. Power Sources* 396, 782 (2018) (ref 57) · Lepley & Holzwarth · *Phys. Rev. B* 92, 214201 (2015) (ref 58 · **목록에 있음** 표 2 #4) · Kasemchainan et al. *Nat. Mater.* 18, 1105 (2019) (ref 7 · **목록에 있음** 표 2 #2) · Lee Y.-G. et al. *Nat. Energy* 5, 299 (2020) (ref 51 · **목록에 있음** 표 2 #1).

---

## (e) DEM-DFT 보고서 (W_ad 보고서) 에 쓸 거리

| 보고서 항목 | 이 논문에서 쓸 점 | 위치 (쪽 · 그림 · 표) | 직접 봤나 |
|---|---|---|---|
| **1. 종결 훑기** (2-3 · 2-4 절 · 종결 둘) | 28 판 (6 면) 을 **γ_surf** (식 4 · 환원 끝점 μ · 전하 있는 판) 로 줄 세움 · 최저 셋 (100) Li–P–S–Cl 1.006 · (011) Li–P–S–Cl 1.168 · (010) Li–P–Cl 1.225 eV nm⁻² (+10 · +1 · +12) — 셋 다 PS₄ 를 잘라 P 를 맨 바깥에 냄 (✎ 저장소) · 우리 S 바깥 ≈ 이름만 S_n 가족 (그쪽은 음이온 과잉 · γ 2.4–5.7) · 우리 Li·PS₄ 바깥과 같은 판 없음 · 전하 맞춤하면 순위가 흔들림 (1.006 → 3.039) | p.20250–20251 · `Table 2` · `Table 4` · `Fig. S8`–`S10` · digest §3b · §4 바깥 층 표 · §7a | ✅ `Table 2` 이미지 · `Fig. S8`–`S10` 원해상도 · 저장소 슬랩 6 개 ASE |
| **2. W · 분리 · 계면 에너지** (머리 표 · 6 절 '고정 기하 W_sep') | **W_ad · W_sep · γ_Li 없음.** γ_inter (식 9 · 두 벌크 기준 · PBE · vdW 없음 · 셀까지 이완 · Li 면 bcc (100) · (100) sym · (110) · 이완 뒤 면내 −5.3 ~ +2.0 %) 는 0 K 이완 중 반응 포함 → **같은 줄 금지** · E_str (식 12) 은 변형 보정 정의만 · γ_inter^min 값 없음 · ✎ Dupré 역산 하한 1.74–2.28 J m⁻² = 반응 에너지 (설명용 · 인용 금지) | p.20251 · 식 (9)–(12) · `Table 3` · `Table 4` · `Fig. 6` · `Fig. S12` · digest §3c · §7b | ✅ `Fig. 6` · `Fig. S12` 원해상도 · `Table 3` · `4` 글자층 · 계면 셀 이완 전후 ASE |
| **3. 화학 안정성** (8 절 문헌 · 7 절 Li \| 재료) | 0 K DFT: 잘린 P (S 2–3) 가 S 를 다 잃고 P −2 (DDEC6) · 온전한 PS₄ 는 S 를 많아야 하나 잃음 (✎ P 추적) · MLMD (MACE · 2220–2596 원자 · 300 / 400 K · 5–10 ns · NPT): 전해질 판 전체 → 비정질 Li₃P/Li₂S/LiCl → antifluorite Li₂S₀.₇₂P₀.₁₄Cl₀.₁₄ · 400 K 분해 끝 0.35–0.57 ns · 결정화 시작 0.24–0.87 ns · 300 K 분해 1.93–> 5 ns · **관측창** "300 K 5 ns 결정 없음" (n = 1): 기대 사건 1 ≈ 0.28 eV (검출 63 %) · 95 % ≈ 0.25 eV · ⚠ 반응물 소진 · 부동태 없음 · MACE S–P 약화 의심 → 속도 인용 금지 · **보고서에 쓸 문장**: Li \| LPSCl 의 젖음은 Li \| SEI 의 문제 | p.20252–20256 · `Fig. 7` · `Fig. 8`–`11` · `Table 5` · `Fig. S4` · `Fig. S13`–`S26` · digest §3d · §3e · §7c · §10-⑦ | ✅ `Fig. 7`–`11` · `S4` · `S13` · `S22` · `S23` 원해상도 · `S14`–`S21` · `S24`–`S26` 축소 대조표 · 저장소 계면 6 + 초격자 5 ASE |
| **4. 이온 수송** (8 절 · 공극) | 계면 장벽 **없음** (NEB 0 · 원전은 Golov 2021 · (d) #7) · 막 플럭스 400 K 1 ns: 벌크 35–37 · 계면 65–80 · 비정질 6.8–18.2 · 결정 SEI 0–0.93 atoms nm⁻² ns⁻¹ · ✎ 결정 SEI = 사건 0–8 개 · **관측창** (400 K · 1 ns · n ≈ 55): 기대 사건 1 ≈ 0.46 eV · 95 % ≈ 0.42 eV · ✎ 창 최소 교환율 ≈ 2.4 × 10⁸ nm⁻² s⁻¹ 대 1 mA cm⁻² = 62 Li nm⁻² s⁻¹ (6–7 자릿수) · **홉 수 검산** (ν₀ 10¹³ s⁻¹ 가정): 벌크 Ea 0.18 eV → 300 K 1/Γ ≈ 0.11 ns · 400 K ≈ 19 ps | p.20255–20258 · `Table 6` · `Table S2` · `Fig. 12` · `Fig. 13` · `Fig. S27`–`S29` · digest §3f · §7d | ✅ `Fig. 12` · `13` · `S27`–`S29` 원해상도 · `Table 6` 이미지 |
| **5. MLIP 학습 · 검증** (3 절 '작은 모델 DFT 확인') | MACE-OMAT 기반 · STING 능동학습 6 회 · 자료 2151 (VASP PBE · 400 eV · **Γ 만**) · 계면마다 모델 하나 (따로 만든 이유는 본문에 없음 — 능동학습이 계면별 DFT 이완 구조에서 출발) · test: E 3.1–4.5 meV (원자당으로 읽음) · F 35.9–46.8 meV Å⁻¹ · RDF · **보고량 DFT 대조 0** · S–P 첫 봉우리 400 K MACE ≈ AIMD 절반 (figure-read) · 최종 모델 test 오차 > AL 6 회째 · **우리와 견줄 점**: 우리는 보고량 W 자체를 같은 배치 · 끝점 · D3 로 DFT 대조 (더 엄격) · 반응 계면이면 결합 끊김 통계 (P–S CN 감쇠 · S–P RDF) 대조를 더해야 함 · 둘 다 OMat24 계열 뿌리 | p.20247–20248 · `Fig. 1` · `Fig. 2` · `Fig. S1`–`S5` · digest §3g · §7e · §10-⑥ | ✅ `Fig. S1` · `S2` · `S4` · `S5` 원해상도 · `Fig. 1` · `2` · `S3` 축소 대조표 |
| **6. 저장소 구조** | **쓸 것** (내부 대조 · 출처 표기): `interfaces/*_cb.vasp` · `_cb_relaxed` (Li \| LPSCl 반응 전 · 0 K 반응 뒤 · 164–225 원자) · `test_sets/*.xyz` (계면마다 500 프레임 DFT E · F — UMA zero-shot 힘 RMSE 용 · Γ 점 기준이라 에너지는 조심) · `*_supercell.xyz` (2220–2596 원자 — UMA MD 모델 간 대조 시작점) · 'P 노출' 슬랩 (W 시나리오 밖 극단 대조) · **못 쓸 것**: LICENSE 없음 (공개물 재사용 불가 · 저자 확인) · MACE 모델 (pickle · 판 미기재) · 에너지 없는 구조 (γ 재계산 불가) · `Li_100_sym_relaxed` bcc 아님 · `bulk/Li6PS5Cl_supercell` 는 본문 MLMD 셀 아님 · 셀까지 이완된 구조 (우리 고정셀 + EOS 규율과 다름 — 쓰면 표기) · 학습 자료 · 입력 · 분석 코드 · sym 모형 없음 | digest §4 · §7f | ✅ 파일 50 개 목록 · 46 개 ASE · 모델은 zip 목록 · sha256 만 |

보고서 문장 후보 (공유 보고서 문체 · 출처는 랩 표준 꼴):
- *Li 금속과 Li₆PS₅Cl 은 닿는 순간 반응해 Li₂S 와 비슷한 계면상을 만든다는 계산 결과가 있어 (J. Mater. Chem. A, 14, 20245 (2026)), Li | Li₆PS₅Cl 의 젖음은 Li 와 그 계면상 사이의 점착으로 따져야 한다.*
- *같은 계산의 계면 형성 에너지는 이완 중 일어난 반응을 포함해서 점착 에너지와 같은 양이 아니다 — 이 보고의 W 와 나란히 두지 않는다.*
- *계면상이 생기면 부피가 약 20 % 줄어든다 (반응식과 결정 부피로 어림) — 접촉을 줄이는 쪽의 기전이다.*

---

## (f) 그림 크롭 요약

- **50 장** = 본문 그림 13 (`Fig. 1`–`13`) + SI 그림 29 (`Fig. S1`–`S29`) + 본문 표 6 (`Table 1`–`6`) + SI 표 2 (`Table S1`–`S2`). 전부 도구 한 번 (`--slug … --pdf 본문 SI --clean`) · 손 크롭 · 다시 자름 0 · 번호 공백 · 놓친 캡션 0 (`missing_labels` = []). 크롭 경계는 원해상도 26 장 + 축소 대조표로 확인 — 잘린 것 없음.
- **본 것: 그림 42/42** — 원해상도 26 장 (`Fig. 5`–`13` · `Fig. S1` · `S2` · `S4`–`S13` · `S22` · `S23` · `S27`–`S29`) · 축소 대조표 16 장 (`Fig. 1`–`4` · `S3` · `S14`–`S21` · `S24`–`S26`). 표는 3 장 이미지 대조 (`Table 2` · `5` · `6`) · 5 장 글자층만 (`Table 1` · `3` · `4` · `S1` · `S2`). `Fig. S6` · `S7` 은 곡선 끝값으로 기울기를 재 라벨과 대조.
- **그림이 본문 · 표와 어긋난 것**: `Fig. S6` D 라벨 한 칸 밀림 · `Fig. S6` · `S7` 시간축 fs (ps 여야) · `Fig. S1` 축 단위 eV · eV/Å (meV 규모) · `Fig. S2` E RMSE 단위 (원자당 누락) · `Fig. 11b` · `S23` · `S25b` 축 '%' 인데 분율 · `Fig. S25` 캡션 '(100)/(010)' (본문은 (100)/(100)) · `Fig. S27b` 전극 400 K 누적 ≈2650 대 `Table S2` 53.4 · `Fig. S28c` 대 `Table S2` L→R / R→L 뒤바뀜 · `Fig. S9` · `S10` 대 `Table 2` 2 칸 (0.003 · 0.03) · `Fig. S12` 대 `Table 4` 1 칸 (0.003) · `Fig. S4` S–P 봉우리 MACE ≈ AIMD 절반 (본문 "만족할 수준") · `Fig. 7b` 와 `Fig. S13b` DDEC6 라벨 숫자 동일.
- **임시 파일 점검 (병렬 충돌 주의)**: 글자 · 렌더 · 스크립트 · 대조표는 전부 `scratchpad/baer2026_li_metal_argyrodite_interface_stability_transport/` 안에 `baer2026_` 접두 이름으로만 썼어요 (공용 이름 없음). 본문 글자 파일 첫 줄 = 이 논문 표지 (*Journal of Materials Chemistry A* · 제목 · Baer) · SI 글자 파일 첫 줄 = 이 SI 표지 · PDF sha256 두 개 = `batch.json` 값과 일치 (`4590934b…` · `aabb7c91…`). 대조표 그림 내용 (Li | LPSCl 단면 · MACE 그래프) 도 이 논문 것이었어요.

---

## (g) Jeff Sakamoto 저자 여부

**아니에요** — 저자는 Chantal M. I. Baer (교신) · Roman Shantsila · Łukasz Figiel · Bora Karasulu (교신) 넷 (University of Warwick · WMG + Department of Chemistry). 참고문헌 63 편에도 Sakamoto 이름은 없어요 (본문 · SI 글자층 검색 0 건). digest 머리말 저자 줄에 그 이름을 쓰지 않았고 웹앱 `_paper_pis` = [] 예요 — INDEX 행에 `🏷 Jeff Sakamoto 공저` 를 달지 않아요.
