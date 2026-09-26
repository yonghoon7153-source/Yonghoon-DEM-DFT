# 감사 A — 고체전해질(LPSCl) 물성 인용의 뿌리 (2026-09-25)

> ⛔ **기록 사본** — 2026-09-25 읽기 전용 감사 에이전트 보고 원문 (scratchpad → 리포 이전 09-26).  판정의 정본은 원장 `docs/reviews/claims.json` (`CL-90` · `CL-91`) 과 `findings.json` `SELF-51` 이다.  인용 금지 등록부의 문자열은 `⟦CL-xx …⟧` 로 바꿔 적었다.  file:line 은 감사 기준 커밋 기준이라 지금 줄 번호와 다를 수 있다.  종합 = `docs/reviews/citation_root_audit_20260925.md`.


## 0. 범위 · 기준 · 판정 기호

- **기준 커밋**: stoic-knuth `b037d765c` (09-25 15:35).  감사 도중 HEAD 가 `bd6d5efa2` → `171934433` → `b037d765c` 로 움직였다 (주 세션의 SELF-51 1·2단계 정정).  아래 "잔존" 수는 `b037d765c` 기준이고, 기록 파일 (`claims.json`·`findings.json`·`docs/data/audit_*`·`litdb/`) 은 세지 않았다.  리포는 읽기만 했다.
- **정본 카드**: `origin/claude/friendly-meitner-lldvar` (감사 중 `f9f834cd0` → `d95bda929`; 차이는 cronau2021 카드 한 줄 정정뿐).
- **추가로 본 1차 자료**: 리포 안 PDF (`docs/literature_coverage/pdfs/`) 를 pypdf 로 추출 — So 2021 JPS · So 2022 JPS · Kang 2025 ACS AMI · Bazzoun 2026 JPS 의 표·참고문헌.  사용자가 준 **Cronau 2021 SI** (`scratchpad/cronau2021_SI.txt`, `cronauSI_p4.png`, `cronauSI_p5.png`) — 추출 텍스트와 Fig. S1·S2 렌더를 직접 봤다.
- **판정 기호**
  - **V** 정본 카드 (PDF digest) 에 그 소재·그 조건의 그 값이 있다
  - **P** 1차 원문 (SI) 그림에서 읽어 지지됨 (디지타이즈) — 정본 카드는 아직 반영 안 됨 (조정자 지시로 추가한 기호)
  - **M** 논문은 있으나 그 값을 주지 않거나, 다른 소재·조건의 값이다 (서지 필드 오류는 M(서지))
  - **B** 서지는 검색으로 확인, 값은 원문 미확인
  - **F** 제목·저자·저널 검색으로 찾을 수 없음 → 지어진 것으로 보임
  - **C** 방법·법칙 인용 (수치 아님)  ·  **U** 판정 불가
  - 검색 결과 요약에만 보인 숫자는 "검색 요약 — 미확인" 으로 적었다.

---

## 1. 판정표

### 1-1. Cronau (2021 ACS Energy Lett. 6, 3072 · 2022 Batteries & Supercaps 5, e202200041)

| # | 인용 → 값/주장 | 사용처 (대표 file:line · 잔존 규모) | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|
| CR-1 | **Cronau 2022** → σ_grain = 3.0 mS/cm "Li₆PS₅Cl single-crystal" (HIGH) | `scripts/voxel_conductivity.py:92` ("✅ literature") · `webapp/templates/group.html:1287,1298` (화면) · `docs/pipeline_step1_to_step5_guide.md:530` · `docs/reviews/codex_review_request_sulfide_doping_20260819.md:22,174` — CLAUDE.md·final_form_status·final_pushes·generate_fitting_report·se_material 는 `b037d765c` 에서 정정됨 | **M** | Cronau 2022 는 실재하지만 소재가 Li₅.₅PS₄.₅Cl₁.₅ 볼밀 분말 연구 (검색: Wiley 초록 — 밀링 시간↑ → 입도↓·σ↓, ~2 h 최적).  단결정 측정은 두 논문 어디에도 없다.  **값 3.0 자체는 Cronau 2021 SI 에서 지지됨 (CR-4)** — 틀린 것은 연도(논문)와 "단결정" 라벨 | 값: import 이전부터 무출처 (`660600a44`, 근거는 자체 MLIP-MD) · "Cronau 2022 … single-crystal": 05-28 `38931e3e7` · `4495bb932` · `b20930e74` |
| CR-2 | Cronau 2021/2022 → 3.0 "단결정" (06-25 카드가 이미 오귀속 판정한 **뒤** 재도입) | `docs/voxel_contact_free_gap.md:60` (CL-81 정본 문서) · (`scripts/se_material.py` 는 `b037d765c` 에서 정정) | **M**(라벨) / 값 P | CR-1 과 같음 | 07-28 `d66fd1448` (se_material) · 09-08 `066fb9628` |
| CR-3 | "펠릿 1.02 < **Cronau ⟦CL-91 단결정 라벨⟧ 3.0** → 입계 때문, 일관" 식의 비교 서사 | `CLAUDE.md:1547,1562` · `docs/data/bazzoun2026_sigma_ionic.csv:8` · `docs/data/hong2026_sigma_ionic.csv:6` · `docs/data/lee2025_transport_anchors.csv:13` · lit 요약 8편 (bazzoun·hong2026·minnmann2021·minnmann2022·oh2026·park2026·sakuda2013·yonsei) · `docs/paper/main.tex:849` · `docs/pipeline_step1_to_step5_guide.md:289` · `docs/reviews/week_plan_manuscript_20260825.md:68` · `ms_si_v7_edit_sheet_20260901.md:384` — 약 30줄/22파일 | **M**(라벨) / 값 P | SI Fig. S2c 의 3.0–3.5 는 **고 스택압 아래 펠릿 총전도도**이지 단결정·grain-interior 가 아니다 ⇒ "펠릿 < 단결정 = 입계" 라는 논거 자체가 성립하지 않는다 (둘 다 펠릿, 압력 조건 차) | 06-23 `5bb684d61` |
| CR-4 | **Cronau 2021 → LPSCl σ ≈ 3.0 mS/cm** (원고 SI Table S2 `Ref. S5`, 세미나 용어집) | 원고 docx Table S2 (생성기 `docs/manuscript_draft/build.js:277` [S8]) · `docs/seminar_20260806_glossary.md:217` · `docs/data/lpscl_electrolyte_params.md:11` | **P** | SI Fig. S2c (µC-Li₆PS₅Cl, 550 °C 10 h 어닐 분말, 제조압 97–487 MPa): 스택압 ≥150 MPa 에서 평탄 — 제조 292 MPa ≈3.0, 389 MPa ≈3.3–3.45, 487 MPa ≈3.0–3.25 ×10⁻³ S cm⁻¹ (그림 판독).  Fig. S1e (GC-Li₆PS₅Cl) 평탄 ≈0.5–1.05 ×10⁻³.  ⚠ 라벨은 "고 스택압 펠릿, 디지타이즈" 여야 한다 — 단결정 아님.  SI 의 압력의존 측정 방법에는 온도가 적혀 있지 않다 | 06-30 `b1ab279c5` (bib 재배선) |
| CR-5 | **거짓 음성** — "Cronau 2021 에는 3.0 이 없다 · Li₆PS₅Cl 은 측정 안 했다 · argyrodite 는 Br 뿐" | 정본 카드 §0(A) (+ 리포 사본 `docs/lit_cronau2021_…md:32–36,53–57`) · `CLAUDE.md:430` (규율 ⑥) · `CLAUDE.md:545–546` · `scripts/se_material.py:46–48` · `scripts/generate_fitting_report.py:483` · `docs/reviews/si_table_response_20260925.md:231` · `docs/manuscript_draft/build.js:414` · `docs/paper/refs.bib:48` · `docs/digest_model_application_backlog.md:50` · `findings.json` SELF-51 제목·note | **M** (부정 주장) | SI Fig. S1e = GC-Li₆PS₅Cl, Fig. S2c = µC-Li₆PS₅Cl, Fig. S6e,f (XRD)·S7e,f (SEM) 도 Li₆PS₅Cl.  카드 스스로 "SI 미업로드 … 본문 6쪽 기준" 이라 적어 놓고 "어디에도 없다" 고 판정했다.  단 "단결정 측정 없음" 부분은 맞다 | 06-25 `d47ac4afa` → 06-30 `b1ab279c5` → 09-25 `171934433`·`b037d765c` · 정본 `d95bda929` 가 "나머지 판정은 그대로" 라며 재확인 |
| CR-6 | Cronau 2022 → SE 크기 계수 Cronau(r_SE): ≥0.5 µm 1.00 · 0.3 0.90 · 0.1 0.65 · ≤30 nm 0.33, "extended ball-milling 1/3 감소", 3-시그모이드 "HIGH literature" | `scripts/run_network_full_corrections.py:12,88–124,1195` · `scripts/generate_comparison_plots.py:4343` · `scripts/nested_cv_sat.py:211` · `webapp/app.py:1263–1264,2141` · `webapp/templates/single.html:2402–2422` · `STAGE_E_ASR_GUIDE.md:110–125` · `docs/sigma_ionic_physics_derivation.md:403` ("HIGH — Cronau 2022 literature") · `docs/paper_brittle_caveat.md:925,1123,1343,1528` · `docs/Reviewer_Defence_Notes.md:134` (≥0.3 µm — 코드는 ≥0.5, 불일치) | **B** | 논문 실재 (Batteries & Supercaps 5 (2022), DOI 10.1002/batt.202200041; 검색 요약: 밀링↑ → 입도↓·σ↓).  절단점·계수값은 원문 미확인.  ⚠ 04-30 **같은 날 값이 두 번 바뀌었다** (`ceee1d812`: 1.5 µm 1.00/1.0 0.92/0.5 0.85/<0.3 0.50 → `f2f214d54`: 1.00/0.90/0.65/0.33) — 원문에서 읽은 값이 아니라는 정황 | 04-30 `ceee1d812` |
| CR-7 | **Cronau 2021** → 입자크기(비정질화) 계수 f_Cronau(r_SE) | `docs/paper/main.tex:73,201,320,833` | **M** | 정본 카드 §0(B): "입자 반경 r 의 함수로 σ 를 측정하지 않았다 … breakpoint 는 논문에 존재하지 않는다".  SI 도 입도 스윕 없음 (Fig. S3 밀도, S4 제조압) | 06-30 `b1ab279c5` (@Cronau2022→@Cronau2021 재배선이 크기계수 인용까지 옮김) |
| CR-8 | Cronau 2022 서지 "*Adv. Energy Mater.*" | `STAGE_E_ASR_GUIDE.md:119` | **M**(서지) | 실제 저널 = Batteries & Supercaps (검색) | 05-08 `84573970d` |
| CR-9 | refs.bib `@Cronau2022` = 2021 논문 **제목** + "ACS Energy Lett. 7, 1843–1851, doi 10.1021/acsenergylett.2c00688" | 제거됨 (06-30) | **F**(서지 필드) | 권·쪽·DOI 가 어느 Cronau 논문과도 맞지 않음; 2c00688 은 검색으로 특정 논문에 해석되지 않음 | 05-08 `c66f9ae94` |
| CR-10 | "**Cronau, Szczuka, Janek, J. Phys. Chem. Lett. 2022, doi 10.1021/acs.jpclett.2c00203**" = σ_grain 3.0 "Li₆PS₅Cl single-crystal bulk" 의 원출처 | `docs/sigma_ionic_physics_derivation.md:56–59` (**살아 있음**, σ_ionic 유도 정본 문서) | **F** | 그 DOI 는 검색상 Mattes *et al.*, "Observation of Oligomeric States Indicates a High Structural Flexibility Required for the Onset of Polyglutamine Fibrillization" (JPCL) — 전혀 다른 논문.  저자 조합으로도 검색 안 됨 | 05-28 `4395b742d` |
| CR-11 | Cronau → SE overlap "floor 5–10 % @380 MPa", "pure-SE **Cronau overlap 11–12 %**" (실험 보정 앵커로) | `CLAUDE.md:471` (frame[2] "Calibration anchors (experiment)") · `CLAUDE.md:974–978,1003,1028` · `docs/esse_calibration_2mAh_real_9.md:60–74` · `webapp/templates/single.html:21` · `group.html:180` · `scripts/seminar_deck/build.js:637` (발표 덱) · `wiki/concepts/ese-softening-18x.md:26` · `docs/pipeline_step1_to_step5_guide.md:525` — 18줄/11파일 | **M** | Cronau 2021 은 σ-vs-압력만 잰다 (카드·SI 어디에도 DEM·접촉 overlap 없음).  11–12 % 는 **우리 pure-SE DEM 결과** (`esse_calibration…`: SE 20 vol% 12.13 / 25 wt% 11.44).  원고 생성기 (`build.js:148`) 는 이미 "simulation consistency result" 로 적는다 | 06-03 `a58e1b7c9` (UI "Cronau floor 5–10%", 출처 없음) → 06-06 `1eb6f6500` |
| CR-12 | Cronau 2021 → 신뢰할 σ 측정엔 스택압 >~50 MPa · 연구실 간 ~10배 산포 | `docs/data/lpscl_electrolyte_params.md:15` 등 | **V** | 카드 §4 "AM·GC: stack > ~50 MPa 면 plateau", µC 는 200–250 MPa; SI Table S1 권장 최소 스택압 = GC/µC 100 MPa (스퍼터 없음), µC 250 MPa | — |
| CR-13 | Cronau 2021 → 스택 50 MPa 고정, 제조 98→392 MPa 에서 σ 0.30→0.85 mS/cm (GC-Li₆PS₅Br) | `docs/temp_pressure_capability.md:381` | **V**(판독) | 카드 §5(a) "~3×10⁻⁴ → ~9×10⁻⁴" (⚠ 카드 본문 단위 표기가 문맥과 안 맞음 — PDF 대조 권장) | — |

### 1-2. Sakuda 2013 (Sci. Rep. 3, 2261 — 75Li₂S·25P₂S₅ **유리**)

| # | 인용 → 값/주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|
| SA-1 | E = 24 GPa, **75Li₂S·25P₂S₅ 유리**로 표기 | `docs/Tabor_framework_reference.md:102` · `scripts/analyze_tabor_regime.py:16` · `webapp/templates/single.html:25` · `docs/Reviewer_Defence_Notes.md:79,90` · `docs/paper_brittle_caveat.md:2290,2332` | **V** | 카드 §3: "E (75Li₂S·25P₂S₅) 24 GPa — stated (초음파, 열간프레스 고밀도 펠릿)" | (09-25 정정본) |
| SA-2 | E = 24 GPa 를 **LPSCl 값**으로 ("LAB VALUE", "experimental consensus", "단결정 reference", "dense-material value", "실 bulk (LPSCl 단결정)") | `scripts/plastic_coverage.py:34,336` · `docs/literature_coverage/README.md:632` · `docs/paper_brittle_caveat.md:27,71` · `docs/sulfide_se_mechanical_anchors.md:42` · **원고** `docs/manuscript_draft/build.js:145–146` ([34]) · `docs/manuscript/methods_simulation_v7_draft.md:99` · `scripts/build_methods_docx.py:103` — 12줄/10파일 | **M** | 카드 §12: "소재가 LPSCl argyrodite 아님"; E 는 열간프레스 유리 펠릿 초음파값 (단결정 아님) | import `660600a44` (plastic_coverage "LAB VALUE") · 04-29 `750e23b7d` ("single-crystal reference value") · 05-18 `296711edc` · 08-05 `d495a0035` · 08-23 `c2670de6e` (원고) |
| SA-3 | 경도 H = 0.85 GPa / 0.7–1.0 GPa "**LPSCl (Vickers) hardness**" | `scripts/analyze_tabor_regime.py:20` · `scripts/build_literature_reference.py:109` · `docs/literature_coverage/README.md:633` · `scripts/plastic_coverage.py:337` · `docs/literature_coverage/contact_mechanics_db.json:386–389` | **M** | 카드 §3 "전부 추출" 표에 경도 없음, §6 "직접 수치는 밀도-vs-P + E + σ 뿐".  리포 자체 기록상 0.85 = **2.8 × σ_y 0.30** (Tabor 산식; `contact_mechanics_db.json`) — 측정값이 아니다 | import `660600a44` ("sulfide glass range 0.5–1.0 per Sakuda") · 04-29 `0a040f2b0` · 05-04 `380c2a723` ("LPSCl Vickers, Sakuda 2013") |
| SA-4 | H ≈ 0.6 GPa "**나노압입**, 비정질 분말" | `docs/Reviewer_Defence_Notes.md:20,27,37` · `docs/Tabor_framework_reference.md:111,192,274` · `docs/paper_brittle_caveat.md:2357` — 6줄/3파일 | **M** | 경도·나노압입 없음 (E 는 초음파) | 05-04 `380c2a723` · `bd4d6fe0b` |
| SA-5 | σ_y(LPSCl) ≈ 0.30 GPa "(Sakuda 2013 indentation)" | `docs/literature_coverage/contact_mechanics_db.json:388` | **M** | 카드에 σ_y·압입 없음.  ⇒ H 0.85 = 2.8×0.30 과 σ_y 0.30 = H/2.8 이 서로를 근거로 삼는 **순환** | import |
| SA-6 | "**Li₆PS₅Cl single-crystal ultrasonic** σ 2.5–3.5 mS/cm (default 3.0)" · σ_disk "Sakuda single-crystal (3.0) vs pellet (0.31)" | `scripts/build_literature_reference.py:99–102` · `scripts/network_conductivity.py:140–141` | **M** | 카드: σ 는 0.31 (냉간)/0.34 (열간) mS/cm, 소재 유리; 단결정 없음; 초음파는 E 측정 | 04-29 `0a040f2b0` · `f68b9a1ff` |
| SA-7 | 냉간 펠릿 σ 0.25–0.40 / 0.31 mS/cm 를 "**Li₆PS₅Cl** pellet" 로 | `scripts/build_literature_reference.py:104–106` · `scripts/network_conductivity.py:141` · `docs/paper/main.tex:843` | **M**(소재) | 값 0.31 은 V (75Li₂S·25P₂S₅ 유리, 360 MPa) — LPSCl 아님 | 04-29 `0a040f2b0` |
| SA-8 | 상대밀도 ~87 % @300 MPa (공극 ~13 %) | `docs/literature_coverage/README.md:389` · `docs/paper/main.tex:823` 등 | **V**(추세) | 카드 §11: Fig 2a 판독 85–88 %; stated 는 ">90 % @ >350 MPa" 뿐 | import |
| SA-9 | "순수 LPSCl 300 MPa ε≈10 % (**EXPERIMENTAL**, Sakuda 2013, Tran 2025)" · `HECKEL_DELTA` 26 %p "(Sakuda 2013, 300 MPa)" · "σ_y 100–200 MPa (Sakuda)" | `scripts/predict_porosity_real_physics.py:7,23,48,179` · `scripts/predict_porosity_strict_physics.py:15,163` · `scripts/fit_porosity_physics_decomposition.py:7,100,172` — 9줄/3파일 | **M** | 카드: 300 MPa 는 ~87 % (판독, 공극 ~13 %), 소재 유리; σ_y·Heckel 적합 수치 없음 | 05-13 `97cc1eac0` · `288d7b27c` · 05-19 `66cc30290` |
| SA-10 | 최소 소성막 h_film = 5 nm "(Sakuda discussion / ~5 nm residual interface)" | `scripts/plastic_coverage.py:48` · `webapp/templates/single.html:1944` · `contact_mechanics_db.json:393` | **M** | 카드에 막 두께 없음 (원장 `L1-08` open, Codex L1 판정과 같음) | import |
| SA-11 | SE 형상계수 1.05 "quenched glass, near-spherical (Sakuda 2013)" | `scripts/dem_analysis_core.py:25–30` | **M**(정성) | 카드 §4: 분말은 유성볼밀 기계화학 합성 유리 (quenched 아님), 구형도·거칠기 수치 없음 | 04-29 `00368b5ea` |
| SA-12 | 상온 가압소결 · 360 MPa 에서 입계 소멸 (유리) | `docs/paper/main.tex:831` 등 | **V** | 카드 §5 Fig 3 | — |

### 1-3. Wang 2020 · Cheng 2017 · McGrogan 2017 (경도·영률)

| # | 인용 → 값/주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|
| WA-1 | "Wang 2020, *J. Power Sources* 470, ⟦CL-90 기사번호⟧" (+ 지어진 제목 "⟦CL-90 지어진 제목⟧") → NCM 경도 · NCM E 140 GPa · **LPSCl E 24 GPa "nanoindentation"** | `171934433` 에서 9곳 정정 — 금지 표지만 남음 (`CLAUDE.md:428` · `build_literature_reference.py:78`) | **F** | 제목 검색 결과 없음.  DOI 10.1016/j.jpowsour.2020.⟦CL-90 기사번호⟧ 은 검색으로 특정 논문에 해석되지 않음.  한 논문이 세 값 = 지어진 신호 (원장 `CL-90`) | 04-29 `b1c8262fe`·`0a040f2b0` (NCM 경도) → 05-04 `bd4d6fe0b` (NCM E 140) · `23d35991a`/`380c2a723` (LPSCl E 24) → 08-23 `c2670de6e` (SI [36]) → 08-24 `9aa882135` (제목 부착) |
| CH-1 | "**Cheng et al. 2017 — *Nano Lett.* 17: 7396**" → dense LPSCl 나노압입 H 0.7–0.9 GPa (→ 0.85) · ν≈0.30 | `docs/Reviewer_Defence_Notes.md:29,33,37,113,297,678` (반박 대응 원고) · `docs/Tabor_framework_reference.md:110` · `docs/paper_brittle_caveat.md:2330` — 9줄/4파일 | **F** | Nano Lett. 17 권 7396 쪽 시작 논문을 찾을 수 없고, Cheng 2017 LPSCl 경도 논문도 없다 (검색 2회).  실재하는 Cheng 2017 은 E.J. Cheng *et al.*, *J. Eur. Ceram. Soc.* **37**, 3213 = **NMC** — 리포 PDF So 2022 표 1: E_AM 199 · H_AM 11.2 GPa · ν_AM 0.25 [37] | 05-04 `380c2a723` ("Cheng 2017 range") · `148d0f5fb` (Nano Lett 서지·"LPSCl dense pellet") |
| CH-2 | Cheng 2017 (JECS/JACS) → NMC111 E 199 ± 12 · LCO 191 GPa | `docs/nca_material_preset.md:18,30` | **B** | 서지는 리포 PDF So 2022 참고문헌 [37] 로 확인, 값은 원문 미확인 | 07-21 `a55c5db24` |
| MG-1 | McGrogan 2017 → Li₂S–P₂S₅ (LPS) 경도 1.9 GPa | `docs/literature_coverage/README.md:633` | **B** (2차 일치) | 실재 (검색; *Adv. Energy Mater.* 7, 1602011).  리포 PDF So 2021 JPS 표 1: "H 1.9 GPa Hardness of SE (LPS) McGrogan et al. [8]"; 정본 카드 so2021·so2022 동일 — McGrogan 원문 카드는 없음 | 05-18 `296711edc` |
| MG-2 | McGrogan 2017 → "**LPSCl** as-synthesized H 0.5–0.7 GPa", "LPSCl mechanical properties" | `docs/Reviewer_Defence_Notes.md:20,28` · `docs/Tabor_framework_reference.md:193,275` · `docs/paper_brittle_caveat.md:2358` | **M** | 제목부터 "Li₂S–P₂S₅" (So 2021 PDF 참고문헌 [8]); 2차 카드들은 H 1.9 · E 18.5 ± 0.9 로 인용 — LPSCl 아님, 0.5–0.7 아님 | 05-04 `148d0f5fb` · `bd4d6fe0b` |
| MG-3 | McGrogan 2017 → E_SE **24 GPa** 의 공동 출처 | `scripts/analyze_tabor_regime.py:16–17` · `docs/Tabor_framework_reference.md:103` | **M** | 정본 song2025·bucci2017 카드 (2차): McGrogan E = 18.5 ± 0.9 GPa (70Li₂S–30P₂S₅ 유리, 나노압입); famprikis2019·du2022: ≈20 GPa | 05-04 `380c2a723` ("Wang 2020, McGrogan 2017") → ⚠ **09-25 `171934433` 정정이 McGrogan 을 24 GPa 출처로 남겼다** |

### 1-4. Koerver 2018 (*EES* 11, 2142) · Koerver 2017 (*Chem. Mater.* 29, 5574)

| # | 인용 → 값/주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|
| KO-1 | Koerver 2018 → H = 0.85 GPa "**LPSCl Tabor hardness**" | `webapp/templates/single.html:1944` (사용자 화면) | **B** ⚠ | 서지 실재 (검색), 값 원문 미확인.  단 리포 기록상 0.85 = 2.8×0.30 산식값 (SA-3·SA-5) 이고, 리포 옛 요약 (`docs/literature_coverage/README.md` §12) 의 Table 1 에도 경도 열이 없다 — Koerver 에서 읽은 흔적이 없다 | import |
| KO-2 | Koerver 2018 Table 1 → Li₆PS₅X E 22–30 · ν 0.33–0.37 · G 8–11 · K 28–30, LLZO 150; 조립 445 · 작동 70 MPa | `docs/literature_coverage/README.md:394–466` · `scripts/plastic_coverage.py:335` ("Koerver 2018 Table 1 #12") | **B** | 정본 카드 없음 (비정본 요약만) | import |
| KO-3 | Koerver 2018 → E_LPSCl 22.1 (및 E_NCA 175) — Kang 2025 의 인용 [42] 기록 | `docs/nca_material_preset.md:10,30` | **B** (Kang 쪽 인용 자체는 V) | Kang 2025 PDF (리포): "The elastic moduli of NCA and LPSCl were assumed to be 175 and 22.1 GPa, respectively.⁴²".  22.1 이라는 수의 원출처 = Deng 2016 Li₆PS₅Cl PBEsol (DE-1) | 07-21 `a55c5db24` |
| KO-4 | Koerver 2018 → NCM ΔV 2.4 % → 8.0 % | `docs/a10_cycle_chemomech_design.md:22` ("web_abstract") | **B** | — | 07-21 `0822e6adf` |
| KO-5 | Koerver 2017 → 작동압 64 MPa · 계면상은 첫 충전에 대부분 형성 | `docs/literature_coverage/README.md:466` · `docs/a10_cycle_chemomech_design.md:49` · `docs/rint_*` | **B** | 서지 실재 (검색) | import / 07-20~21 |

### 1-5. Kraft 2017 (*JACS* 139, 10909) · Ketter 2025 (*Nat. Commun.* 16, 1411)

| # | 인용 → 값/주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|
| KR-1 | σ·T = σ₀·exp(−Eₐ/k_BT) 규약 (eq 5) | `scripts/se_material.py:34,113,122` · `webapp/predictor_engine.py:782` · `single.html:785` | **V** | 카드 §4 "σT=σ₀exp(−E_A/k_BT) (eq 5)" | — |
| KR-2 | Eₐ 0.46 eV (밴드 상한) | `scripts/se_material.py:59` · `webapp/templates/predictor.html:239` | **V**(판독) | 카드 §3c Cl "~0.44–0.46" (Fig 6b, 총 임피던스) | — |
| KR-3 | "Li₆PS₅Cl σ_grain = 3.0 mS/cm **[Kraft 2017]**" | `docs/References_and_Methodology.md:118,177` | **M** | 카드 §3c: σ_RT(Cl) ~1.3×10⁻³ S/cm (판독), 최대는 Cl₀.₅Br₀.₅ ~2 mS/cm | import |
| KR-4 | 서지 저자 "Caldwell, M." | `docs/References_and_Methodology.md:117` | **M**(서지) | 카드 저자: Mario **Calderon** | import |
| KE-1 | **K_SE = 0.7 W/(m·K) "LPSCl (Ketter 2025)"** · "SE=문헌앵커, AM 은 Ketter 아님" | `scripts/network_conductivity.py:132` · `scripts/step3_sigma.py:1035–1039,1052–1054` · `scripts/audit_transport_cap_equivalence.py:399` · `scripts/mpm_webapp_payload.py:2580` — 코드 4파일 | **M** | 논문 실재 (Ketter, Greb, Bernges, Zeier, *Nat. Commun.* 16, 1411 (2025), 10.1038/s41467-025-56514-5).  정본 브랜치 `research-agent/vault` 노트 (evidence_level fulltext — **litdb 카드 아님**): "열전도도는 **LPSCl 0.32 ± 0.02, NCM83 0.71 ± 0.04** W m⁻¹ K⁻¹" ⇒ 0.7 은 NCM83 값과 겹치고 LPSCl 값이 아니다 (검색 요약도 같은 수치 — 질의에 수치를 넣었으므로 독립 증거로 치지 않음).  PDF 대조 후 카드화 필요 | import |
| KE-2 | 서지 "**Ketter, F. et al. (2025). Thermal conductivity of LPSCl argyrodite.**" | `GB_correction_fitting_report.md:1070` · `docs/thermal_conductivity_derivation.md:298` | **F** | 그 제목은 검색에 없다.  실제 제1저자는 Lukas Ketter, 제목은 "Using resistor network models to predict the transport properties of solid-state battery composites" — 같은 보고서 880행은 올바른 서지를 따로 갖고 있다 | import |
| KE-3 | Ketter 2025 → voxel 저항망 (2 µm voxel, 협착 없음) 비교 | `GB_correction_fitting_report.md:376,542–550` | **B** | vault 노트 요약 (300³, 2 µm) 과 일치 — litdb 카드 없음 | import |

### 1-6. Minnmann 2021 (*JES* 168, 040537) · Doux 2020 (*AEM* 10, 1903253)

| # | 인용 → 값/주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|
| MI-1 | 복합 양극 공극 14 % (13–17 %) @380 MPa · σ_ion,eff 0.17 mS/cm @42 vol% · τ_ion 2.07 (τ² 4.3) · LPSCl bulk 1.6 mS/cm @25 °C · 측정압 ~40 MPa | 다수 | **V** | 카드 §0 표 "✅ stated" · §2 | — |
| MI-2 | "**pure-SE porosity ≈ 10 % @300 MPa (Minnmann et al., LPSCl cold-press)**" | `CLAUDE.md:445` (frame[1]) · `CLAUDE.md:1084,1271,1286,1317` · `docs/mpm3d_calibration.md:74,180` · `docs/pipeline_step1_to_step5_guide.md:262,524,526` · `docs/data/heckel_pure_se_dem.csv:11,16` · `scripts/mpm_dem_match.py:369,393` · `scripts/dem3d_calib.sh:4` · `wiki/concepts/frame4-independent-calibration.md:44` — 33줄/22파일 | **M** | 카드 §3: "이 논문은 pure-SE porosity를 별도 측정하지 않는다 — 14 %는 복합 양극 값"; minnmann2022 카드: "pure-SE 10 %는 우리 MPM/DEM 보정 표적".  09-09 감사 P0 (`residual_buckets.json`) 로 지적됐으나 원장 미등재 | 06-07 `2d0ce2a61` (그 전 같은 10 % 가 import 에선 **Doux 2020**, 05-13 에선 **Sakuda 2013** 에 붙어 있었다) |
| MI-3 | Minnmann 2021 → "*Adv. Energy Mater.* 11 — DEM with relaxation, max overlap 0.06–0.10" · "DEM values 0.05–0.15 (Wang 2023; Minnmann 2021)" | `scripts/build_literature_reference.py:20,91` · `docs/paper_brittle_caveat.md:44,87` | **M** | 카드: JES 실험 논문 (EIS-TLM), DEM 없음 | 04-29 `0a040f2b0` · `750e23b7d` |
| MI-4 | Minnmann 2021 → "wet-coated catholyte" ASR 50–200 Ω·cm² | `STAGE_E_ASR_GUIDE.md:364` · `webapp/templates/single.html:2453` | **M** | 카드: 건식 혼합 + 380 MPa; Ω·cm² ASR 없음 (R_el 107 Ω · R_ion 360 Ω 만) | 05-06 `19e03e9fb` |
| MI-5 | Minnmann 2021 → "실험 coverage 40–65 %" | `webapp/templates/single.html:1735,2128` | **M** | 카드에 coverage 측정 없음 (§7 은 utilization 개념뿐) | 04-30 `573a07187` · 05-06 `716f98e81` |
| MI-6 | "Minnmann et al. (2021, 2024)" → 복합 σ_el ≈ 10–15 mS/cm | `docs/electronic_conductivity_derivation.md:298` | **M**(2021분) | 2021 카드: 42 vol% σ_el,eff 0.56 mS/cm, 61 vol% ~1 mS/cm.  10–15 는 **Minnmann 2024** 카드 값 (70 wt% CAM, 판독 15/10/10) | import |
| MI-7 | (관련) Minnmann 2022 = 원고 [9] → "~10 % target … 11–12 % overlap" 의 근거, 저자 "T. Minnmann" | `docs/manuscript_draft/build.js:146–148,270` | **M** | minnmann2022 카드: "이 논문엔 porosity 숫자가 단 하나도 없다"; 제1저자 P. Minnmann | 08-23 `c2670de6e` |
| MI-8 | k_spread 1.65 = "Minnmann 2021 match" | `scripts/plastic_coverage.py:287` | **U** | 무엇을 맞췄는지 기록 없음 | import |
| DO-1 | Doux 2020 → LPSCl 펠릿 공극 18 % @370 MPa · 5 MPa 최적/≥25 MPa 단락 · §8 (370 MPa 펠릿은 5–75 MPa 스택에 더 안 눌림) | `docs/temp_pressure_capability.md:319` · `single.html:292,670,832` · `literature_review_dem_mpm_assb.md:54` | **V** | 카드 §6 Table S2 상대밀도 82.1 %, §8 | — |
| DO-2 | Doux 2020 → "SE-only 펠릿 **~10 % @300 MPa**, 250–400 MPa 5–15 % — 우리 calibration reference" · "E_eff 1.35 가 ~10 % (Doux 2020) 재현" | `docs/References_and_Methodology.md:7,113–115,194,208,270` · `scripts/cap_compaction_heckel.py:17–18,30,36,79,91` | **M** | 카드: 300 MPa 데이터 없음, 370 MPa 에서 18 % | import · 06-07 `4706f7665` |

### 1-7. 나머지 키

| # | 인용 → 값/주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|
| JA-1 | Janek (& Zeier) 2023 → 황화물 복합 σ_ion 0.1–0.5 mS/cm · ≥500 mAh/cc · AM 75–90 % (76–88 wt%) 상용 창 | `scripts/grade_engine.py:343,401,409` · `docs/GRADING_STORY.md:42,188` | **B** | 서지 실재 (검색: *Nat. Energy* 8, 230–240, Janek & Zeier); 카드 없음 | 05-20 `41f3a9d9a` · 05-22 `06aece281` |
| RE-1 | Reisacher 2023 → Eₐ 0.41 eV · 375 MPa 분리막 · σ 0.43 mS/cm · p_c ≈4 wt% C65 · 5 wt% 102 mS/cm | `scripts/se_material.py:90` · `predictor.html:211,236,251` 등 | **V** | 카드 §3 (stated) | — |
| BA-1 | Bazzoun 2026 → σ_eff,ion 0.137/0.101/0.065 · 펠릿 1.02 · E_SE 22.1 · ν 0.37 · E_CAM 161.5 · RNM 0.068→0.135 · RNM 32–98× | 다수 | **V** | 카드 §3 · 리포 PDF 표.  ⚠ **E_SE 22.1 은 Bazzoun 이 Deng 2016 [55] 에서 가져온 DFT 입력값** (리포 PDF 표) — `sulfide_se_mechanical_anchors.md:43` ("같은 재료") · sakuda 카드 §10 ("양쪽에서 고정") 처럼 독립 앵커로 세면 Deng 과 이중계상 | — |
| DE-1 | Deng 2016 → Li₆PS₅Cl E 22.1 · G 8.1 · B 28.7 GPa · ν 0.37 (PBEsol, 24g 질서 모델) / 본문의 "LPSCl DFT ≈ 22 GPa" | `single.html:25` · `Reviewer_Defence_Notes.md:79` (이름 없이) | **V** | 카드 Table III.  Cronau 2021 SI 도 참고문헌 S4 로 Deng 을 들어 "Young's and bulk moduli 20–35 GPa" 라 적는다 | — |
| NI-1 | Ning 2023 | 리포 (litdb 제외) **0건** | — | 정본 song2025 카드가 2차로 "Ning *et al.*, *Nature* 2023: 나노압입 E 28.0 ± 1.8 GPa · K_Ic 0.69 ± 0.12" 인용 | — |
| BO-1 | Boulineau 2012 → 냉간 펠릿 1.33 mS/cm · Eₐ ~0.33 eV | `docs/data/lpscl_electrolyte_params.md:12,29` | **B** | 서지 실재 (*Solid State Ionics* 221, 1–5, 10.1016/j.ssi.2012.06.008).  문서 스스로 "values from search snippets" 라 적음 | 06-24 `268dcd057` |
| YU-1 | Yu 2018 → 3.15→4.96 mS/cm · Eₐ 0.32–0.36 · **이론밀도 1.64 g/cm³** | `docs/data/lpscl_electrolyte_params.md:13,19,29` | **B** ⚠ | 서지 실재 (*ACS AMI* 10, 33296, 10.1021/acsami.8b07476).  ⚠ 1.64 는 정본 doux2020 "이론밀도 1.860", reisacher2023 "1.83 g/cm³" 와 어긋난다 (1.64 는 Bazzoun 의 DEM ρ_SE 와 같은 수) | 06-24 `268dcd057` |
| ZH-1 | Zhou 2020 → 6.11 mS/cm | `docs/data/lpscl_electrolyte_params.md:13` | **B** | 서지 실재 (*Nano Lett.*, "Densified Li6PS5Cl Nanorods …", 10.1021/acs.nanolett.0c02489) | 06-24 `268dcd057` |

**판정 집계 (60 행)**: V 12 · P 1 · M 28 · B 13 · F 5 · C 0 · U 1  (NI-1 은 0건이라 제외).

---

## 2. 뿌리 — 확인 없이 들어간 짝이 처음 생긴 커밋

모든 뿌리 커밋의 작성자는 `Claude` (자동 작성) 다.

**① 04-24 import `660600a44`** (claude/add-metric-cards-0a3n0 에서 들여옴 — 그 전 이력은 이 리포에 없다)
- σ_grain = 3.0: 코드엔 출처 없이 `SIGMA_BULK_DEFAULT = 3.0e-3 # grain interior`; 보고서 근거는 **자체 MLIP-MD (UMA) σ₃₀₀K = 3.0 mS/cm** + 펠릿 문헌값; `References_and_Methodology.md` 는 **[Kraft 2017]** 로 적음 (KR-3, KR-4).
- Doux 2020 → "300 MPa ~10 %, 250–400 MPa 5–15 %, 우리 calibration reference" (DO-2).
- LPSCl E 24 "LAB VALUE / experimental consensus" (SA-2), H 0.85 = 2.8×σ_y 0.30 을 "Sakuda indentation"·"Sakuda glass 0.5–1.0"·"**Koerver 2018**" 에 붙임 (SA-3, SA-5, KO-1), h_film 5 nm "Sakuda" (SA-10).
- K_SE 0.7 W/mK "**Ketter 2025**" + 지어진 서지 "Ketter, F. … Thermal conductivity of LPSCl argyrodite" (KE-1, KE-2).
- Minnmann (2021, 2024) σ_el 10–15 (MI-6), Koerver 2017/2018 수치 (KO-2, KO-5).

**② 04-29 균열 모듈·문헌표** `b1c8262fe` · `0a040f2b0` · `f68b9a1ff` · `00368b5ea` · `750e23b7d`
- Wang 2020 JPS 470 ⟦CL-90 기사번호⟧ (F, WA-1).  Sakuda 2013 → "**Li₆PS₅Cl single-crystal** ultrasonic 2.5–3.5 (3.0)" · "Li₆PS₅Cl pellet 0.25–0.40" · "Li₆PS₅Cl hardness 0.7–1.0 (0.85)" (SA-3/6/7) — **"단결정" 라벨이 처음 붙은 곳은 Cronau 가 아니라 Sakuda 였다**.  Minnmann 2021 → "AEM 11 DEM overlap" (MI-3).  σ_disk "Sakuda single-crystal vs pellet" · SHAPE_FACTOR "quenched glass" · 원고 초안 "single-crystal reference E 24".

**③ 04-30 Stage-E** `ceee1d812` · `f2f214d54` · `573a07187`
- Cronau 2022 크기계수 도입 — 같은 날 값 두 번 교체 (CR-6).  Minnmann coverage 40–65 % (MI-5).

**④ 05-04 Tabor 상수·반박 노트** `380c2a723` · `23d35991a` · `bd4d6fe0b` · `148d0f5fb`
- E 24 = "Wang 2020 nanoindentation, McGrogan 2017" · H 0.85 = "LPSCl Vickers, Sakuda 2013" · **Cheng 2017 *Nano Lett.* 17:7396 (F)** · McGrogan "LPSCl 0.5–0.7" · Sakuda "0.6 GPa 나노압입" (WA-1, CH-1, MG-2/3, SA-3/4).  ⇒ **한 값 (0.85) 이 세 논문 (Sakuda·Koerver·Cheng) 을 출처로 달고 있다 — Wang 2020 과 같은 신호**.

**⑤ 05-06/05-08** `19e03e9fb` · `716f98e81` · `84573970d` · `c66f9ae94` — Minnmann "wet-coated ASR" (MI-4), Cronau 2022 "Adv. Energy Mater." (CR-8), refs.bib `@Cronau2022` 서지 필드 조작 (CR-9).

**⑥ 05-13/05-19 다공도 예측기** `97cc1eac0` · `288d7b27c` · `66cc30290` — "순수 LPSCl 10 % EXPERIMENTAL (Sakuda 2013)" · "σ_y 100–200 (Sakuda)" · "Heckel (Sakuda)" (SA-9).

**⑦ 05-18 / 05-20 / 05-22** `296711edc` (README: E_LPS 24→LPSCl, H_LPSCl 0.85 Sakuda) · `41f3a9d9a`·`06aece281` (Janek 2023 수치, B).

**⑧ 05-28 최종형 보고** `38931e3e7` · `4495bb932` · `b20930e74` · `4395b742d` — σ_grain 3.0 에 "**Cronau 2022 Li₆PS₅Cl single-crystal, HIGH**" (CR-1) + **지어진 서지 "Cronau, Szczuka, Janek, JPCL 2022, doi …2c00203"** (CR-10).

**⑨ 06-03 ~ 06-07 보정 앵커** `a58e1b7c9` · `1eb6f6500` · `2d0ce2a61` · `4706f7665` — "Cronau overlap floor 5–10 % / 11–12 %" (CR-11) · CLAUDE.md frame[1] "pure-SE 10 % (Minnmann)" (MI-2) · cap Heckel "Doux 300→10 %" (DO-2).

**⑩ 06-23 ~ 06-30** `5bb684d61` · `268dcd057` · `0e7c4dc0e` · `d47ac4afa` · `b1ab279c5` — "펠릿 < Cronau ⟦CL-91 단결정 라벨⟧ 3.0" 서사 (CR-3) · 검색 요약 기반 LPSCl 파라미터 (BO/YU/ZH) · voxel_conductivity "✅ literature" · **카드의 거짓 음성 (SI 안 읽고 "3.0 없음·Cl 미측정")** (CR-5) · bib 재배선이 크기계수 인용까지 Cronau 2021 로 옮김 (CR-7).

**⑪ 07-28 ~ 09-08** `d66fd1448` (se_material: 06-25 카드가 오귀속을 판정한 **뒤** "Cronau 2021/2022 단결정" 재도입) · `d495a0035` ("실 bulk LPSCl 단결정 24") · `d6dcd9358` (용어집 "σ ~3 mS/cm, Cronau 2021 [✓]" — 원문 확인 없이 [✓] 를 달았다; 값은 오늘 SI 로 사후 지지됨) · `c2670de6e` (원고: "dense-material value (24 GPa)[34]", "[9] T. Minnmann", Wang [36]) · `066fb9628` (CL-81 정본 문서 "Cronau ⟦CL-91 단결정 라벨⟧").

**⑫ 09-25 정정 커밋이 남긴 것** `171934433` · `b037d765c` · 정본 `d95bda929` — McGrogan 을 24 GPa 출처로 유지 (MG-3), 카드의 거짓 음성 (CR-5) 을 se_material·CLAUDE.md·SELF-51 에 옮겨 적음.

**값 하나에 출처가 여럿 붙은 사례 (가장 강한 신호)**
- σ_grain 3.0 mS/cm: 자체 MLIP-MD (import) → Kraft 2017 (import) → Sakuda 2013 (04-29) → Cronau 2022 (05-28) → 지어진 JPCL 2022 (05-28) → Cronau 2021 (06-30).  **실제로 ~3.0 을 보여주는 것은 Cronau 2021 SI Fig. S2c (µC-Li₆PS₅Cl 펠릿, 고 스택압) 하나뿐**이고, 그것은 오늘 SI 로 처음 확인됐다.
- H 0.85 GPa: 2.8×0.30 산식 (import) → Sakuda · Koerver 2018 · Cheng 2017 (F) · McGrogan.
- 순수-SE 10 % @300 MPa: Doux 2020 (import) → Sakuda 2013 (05-13) → Minnmann (06-07).  어느 것도 그 값을 주지 않는다.
- E 24 GPa (LPSCl 로): "LAB VALUE" (import) → Wang 2020 + McGrogan (05-04) → Sakuda 유리 + McGrogan (09-25).

---

## 3. 교체안 — 정본 카드 (V) 에 있는 것만.  없으면 "원문 필요"

| 대상 | 교체 (정본 카드) |
|---|---|
| LPSCl 영률 (E 24 "LPSCl/dense/단결정") | DFT: **deng2016** Li₆PS₅Cl E 22.1 · G 8.1 · B 28.7 GPa · ν 0.37 (PBEsol, 질서 모델; Cronau 2021 SI·Bazzoun 2026 도 이것을 인용) · **torii2025** E 27.4 (PBE-D3).  실측: **jung2026** LPSCl 나노압입 (Oliver–Pharr, ν 0.30 가정) 28.6 GPa · AFM-QNM 16.6 GPa · **song2025** 다공 13 % 펠릿 벌크 4.7 ± 1.1 GPa.  24 GPa 를 남기려면 "75Li₂S·25P₂S₅ 유리, 초음파 (sakuda2013)".  Ning 2023 (28.0 ± 1.8) 은 2차 인용 → 원문 필요 |
| LPSCl 경도 (H 0.85) | **jung2026**: LPSCl H = **1.34 GPa** (나노압입, Oliver–Pharr, 70 µN, Fig. S6d) — 정본에 있는 유일한 LPSCl 경도.  McGrogan 1.9 (유리) 는 원문 필요.  Cheng 2017 Nano Lett 인용은 삭제 |
| σ_y(LPSCl) 0.30 "Sakuda indentation", h_film 5 nm, SE 형상계수 1.05 | 원문 필요 (정본에 없음) |
| σ_ion 3.0 mS/cm | **원문 확인됨, 카드 미반영**: Cronau 2021 SI Fig. S2c — "µC-Li₆PS₅Cl 펠릿, 제조압 ≥292 MPa, 스택압 ≥150 MPa 평탄 ≈3.0–3.5 mS/cm (그림 판독)" 로 카드 갱신 후 인용.  "단결정/grain-interior" 라벨은 근거 없음.  비교용 정본 값: minnmann2021 1.6 mS/cm (25 °C, 380 MPa) · bazzoun2026 1.02 (400 MPa 펠릿) · reisacher2023 0.43 (RT, 375 MPa) · jung2026 1.63 · kraft2017 ~1.3 (판독) |
| Cronau(r_SE) 계수값 | 원문 필요 (Cronau 2022 Batteries & Supercaps PDF).  방향 (미세결정 → 접촉 불량 → σ↓) 만 cronau2021 카드가 지지 |
| κ_LPSCl 0.7 W/mK | 원문 필요 (Ketter 2025 PDF → litdb 카드화.  vault 노트는 LPSCl 0.32 ± 0.02 · NCM83 0.71 ± 0.04).  ling2026 카드는 LPSC 열확산도 α 0.174 mm²/s 만 준다 (κ 아님) |
| 순수-SE 공극 10 % @300 MPa ("Minnmann"·"Doux"·"Sakuda") | 정본에 순수 LPSCl 10 % 는 없다 → "우리 보정 표적" 라벨.  정본 순수 LPSCl 펠릿: **song2025 13 ± 2 % @360 MPa (+60 °C 2 h)** · **doux2020 18 % @370 MPa** (상대밀도 82.1 %).  복합: minnmann2021 13–17 % @380.  유리 추세: sakuda2013 >90 % @>350 (stated) / ~87 % @~300 (판독) |
| "Cronau overlap 5–10 % / 11–12 %" | 문헌 없음 → "우리 pure-SE DEM 결과" 로 |
| Minnmann 2021 → coverage 40–65 % | **minnmann2024**: CAM coverage by ISE ≈20 % → ≈50 % (70 wt% CAM, 380 MPa, 토모그래피) — 같은 양인지 확인 후 |
| Minnmann 2021 → σ_el 10–15 mS/cm | **minnmann2024** ≈15/10/10 mS/cm (판독, 70 wt%) 또는 **minnmann2021** 0.56 mS/cm @42 vol% |
| Minnmann 2021 → DEM overlap, wet-coated ASR 50–200 | 원문 필요 (Minnmann 2021 이 아님) |
| Doux 2020 → 10 % @300 | **doux2020** 18 % @370 MPa |
| Kraft 2017 → 3.0 | **kraft2017** Cl ~1.3 mS/cm (판독); 저자 Calderon |
| Ketter, F. "Thermal conductivity of LPSCl argyrodite" | 서지를 Ketter, L.; Greb; Bernges; Zeier, *Nat. Commun.* 16, 1411 (2025) 로 — 값은 원문 필요 |
| Cronau, Szczuka, Janek JPCL 2022 | 삭제.  값의 근거는 위 Cronau 2021 SI |
| Janek 2023 · Koerver 2017/2018 · Boulineau · Yu 2018 · Zhou 2020 · McGrogan | 원문 필요 (정본 카드 없음) |

---

## 4. 별도 발견 — 정본 카드의 거짓 음성 (Cronau 2021)

- 카드 §0(A) 의 세 판정 중 **둘이 틀렸다**: "3.0 mS/cm 이 논문 어디에도 없다" (SI Fig. S2c 에 있다) · "Li₆PS₅Cl 을 측정하지 않았다, argyrodite 는 Br 뿐" (SI Fig. S1e·S2c·S6e,f·S7e,f 가 Li₆PS₅Cl, S1f·S2d 가 Li₅.₅PS₄.₅Cl₁.₅).  "단결정 측정 없음" 은 맞다.
- 원인: 06-25 digest 가 "SI 미업로드 … 본문 6쪽 기준" 이라고 스스로 적고도 **본문 밖까지 부정 판정**을 냈다.  부정 판정 ("없다") 은 전문을 다 본 경우에만 쓸 수 있다.
- 퍼진 곳: 위 CR-5 칸 (CLAUDE.md 규율 ⑥ 문단 포함 약 15줄/9파일 + SELF-51 원장).  오늘 정본 `d95bda929` 가 "나머지 판정은 그대로" 라며 한 번 더 확인했다.
- 결과: 원고 SI Table S2 의 `Ref. S5` 를 "오귀속" 으로 보고 `Assumed` 로 바꾸려던 처방 (si_table_response #10, build.js:414) 은 다시 봐야 한다 — 인용은 살리고 라벨을 "펠릿, 고 스택압, 판독" 으로 고치는 것이 원문과 맞는다.
- 같은 부류 하나 더: CR-3 의 "펠릿 1.02 < Cronau ⟦CL-91 단결정 라벨⟧ 3.0 = 입계" 서사는 3.0 도 펠릿이므로 논거가 없다 (Hong 1.87 · Lee 2.19 · Minnmann 1.6 을 "그 사이 = GB 일관" 으로 읽은 lit 요약들 포함).

---

## 5. 범위 밖 부수 발견 (감사 안 함 — 다른 키 담당에게)

- `docs/GRADING_STORY.md:187` — "Liu & Yin 2025: SE percolation threshold … (https://example.org/) (placeholder)" — 자리표시 URL 이 참고문헌 목록에 있다.
- `docs/Reviewer_Defence_Notes.md` §B — "Tanaka *et al.* 2017, *J. Am. Ceram. Soc.* 100: 4053", "Bistri 2024 — MPM for sulfide cold-press (forthcoming)" 미확인.
- `scripts/build_literature_reference.py` — Wang 2023 (DEM overlap 0.05–0.15) 미확인.  Bielefeld 2020 ("*J. Electrochem. Soc.* — relaxation-included DEM, max overlap 5 %") 은 정본 카드 `bielefeld2020_effective_ionic_conductivity_binder` 와 어긋난다 — 카드는 *ACS Appl. Mater. Interfaces* 12, 12821 · GeoDict voxel 연속체 풀이 (DEM 아님).
- `scripts/predict_porosity_real_physics.py` 의 "Tran 2025", `se_material` 의 "Ma 2024 (0.29 eV)" 미확인.

---

## 6. 검색 근거 (존재 확인용; 수치는 쓰지 않음)

- Cronau 2022, Batteries & Supercaps: https://chemistry-europe.onlinelibrary.wiley.com/doi/abs/10.1002/batt.202200041
- Cronau 2021, ACS Energy Lett.: https://pubs.acs.org/doi/10.1021/acsenergylett.1c01299
- DOI 10.1021/acs.jpclett.2c00203 (다른 논문): https://pubs.acs.org/doi/10.1021/acs.jpclett.2c00203
- JPS vol 470 목차 (⟦CL-90 기사번호⟧ 미특정): https://www.sciencedirect.com/journal/journal-of-power-sources/vol/470/suppl/C
- Nano Lett. 17(12) 목차 (7396 미특정): https://pubs.acs.org/toc/nalefd/17/12
- Ketter 2025: https://www.nature.com/articles/s41467-025-56514-5 · https://pubmed.ncbi.nlm.nih.gov/39915489/
- McGrogan 2017: https://onlinelibrary.wiley.com/doi/full/10.1002/aenm.201602011
- Koerver 2018: https://pubs.rsc.org/en/content/articlelanding/2018/ee/c8ee00907d
- Koerver 2017: https://pubs.acs.org/doi/10.1021/acs.chemmater.7b00931
- Janek & Zeier 2023: https://www.nature.com/articles/s41560-023-01208-9
- Boulineau 2012: https://www.researchgate.net/publication/232162570
- Yu 2018: https://pubs.acs.org/doi/10.1021/acsami.8b07476
- Zhou 2020: https://pubs.acs.org/doi/abs/10.1021/acs.nanolett.0c02489
