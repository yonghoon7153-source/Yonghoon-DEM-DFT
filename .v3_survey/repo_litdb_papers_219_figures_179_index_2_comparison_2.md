# repo — litdb (문헌 지식베이스: papers 219 · figures 179 · INDEX 2종 · comparison 2종)

## 지금 무엇인가
litdb 는 논문 digest 219개(_TEMPLATE 제외 218, 세미나 대본 3편 빼면 실 digest 215)와 크로핑 그림 2,764장(179 slug, 1.0 GB)을 담은 문헌 단일 시스템이고, 축이 SE(argyrodite)와 DEM/MPM 둘로 갈려 인덱스도 비교문서도 각각 두 벌이다. 웹앱은 papers/ 디렉터리를 직접 읽으므로 INDEX.md·comparison_vs_ours*.md·our_dft_baseline.md 는 **화면에 한 번도 렌더되지 않고** 오직 repo 를 읽는 사람/LLM 만 본다 — 즉 결속·lint 어느 것도 이 파일들을 안 본다. **내가 실제로 본 것**: README·our_dft_baseline·_INDEX_proposals 전문, INDEX.md 부분(1–10·130–216·272–280 + 21개 절 행수 전수), INDEX_DEM.md 앞 40줄, comparison_vs_ours.md 부분(1–30·115·222·430–470·1346–1412 + 제목 전수), comparison_vs_ours_DEM.md 앞 20줄과 제목만, talks/README 앞 20줄, surveys 1편 앞 25줄, digest 12편(스켈레톤 5·han2025 2·세미나 3·묘비 1·기타). **못 본 것**: comparison_vs_ours_DEM.md 본문 3,190줄, digest 약 205편의 본문(기계 스캔만), positioning_vs_geodict.md·yonsei triage 본문·concepts 1편·talks 9편 본문, 그리고 **크로핑 PNG 는 한 장도 안 봤다**(CLAUDE.md 의 "litdb 볼 때 그림을 같이 본다" 규율은 이번 구조 조사에서 지키지 않았다).

## 처음 오는 사람
README.md 를 열면 "Argyrodite SE 문헌 단일 시스템" 이라고 자기소개하는데, 실제 digest 215편 중 117편(54%)이 DEM/MPM 축이다. README 의 폴더 구조표 6줄에는 `INDEX_DEM.md`·`comparison_vs_ours_DEM.md`·`talks/`·`surveys/`·`topics.json`·`_INDEX_proposals.md` 가 **하나도 없고**, 대신 존재하지 않는 `properties/*.md` 를 두 번 가리킨다. 그래서 처음 온 사람은 "SE 논문 모아둔 폴더" 로 오해한 채 litdb 절반을 못 찾는다. 다음으로 INDEX.md 를 열면 150 KB / 평균 972자·최대 15,710자짜리 한 줄 표라서 사람은 스크롤로, LLM 은 약 40k 토큰으로 읽어야 하고, 맨 위 3분의 1은 2026-06-23 Excel 덤프(잘린 셀·빈 행)와 사라진 업로드 id 목록이며 2026-08~09 에 새로 판 축 8개는 전부 맨 아래에 붙어 있다. 결정적으로 DEM 쪽 digest 84편이 "우리 대비" 절에서 가리키는 `our_dem_baseline.md` 는 **이 브랜치에 없다** — DEM 트랙에는 기준점이 아예 없다. 막히는 지점 순서: ① README 가 절반을 안 알려준다 → ② INDEX.md 가 너무 비싸다 → ③ DEM 기준값이 없다 → ④ 어느 숫자가 아직 살아 있는지(철회/비인용) 판단할 근거가 litdb 안에 없고 db/properties 원장을 따로 열어야 한다.

## 건드리면 안 되는 것
- **INDEX.md 의 손으로 쓴 분석 산문** — MUST-READ(:15 fan2026 리뷰 판정), ✅ Digest 완료 66행, 2026-08/09 신설 축 8개. 자동 생성으로 못 만드는 것이고 _INDEX_proposals.md 머리말이 이유를 못박아 뒀다("INDEX 항목은 손으로 쓴 분석 산문이라 자동 append 하면 오염된다"). 재편은 **순서와 접힘**만 바꾸고 문장은 건드리지 않는다.
- **comparison_vs_ours.md §I(출처 재귀속) · §J-6(이 축에서 인용하면 안 되는 것) · §J-8(CV 규약 판정) · §L(자기감사)** — litdb 에서 가장 비싼 자산이고 대부분 다른 곳에 사본이 없다. §L 은 **원장으로 옮긴 뒤에** 링크로 축소해야지, 먼저 지우면 투고 중 원고의 P0 두 건이 사라진다.
- **litdb/talks/README.md 의 3단 인용 규율** — "덱 수치는 발표 소환값 … papers/ 소환값보다도 낮은 등급", "'저 그룹은 ~을 안 한다'는 서술 금지 … 부재의 증거가 아니다", 내부 BML 세미나 외부 인용 금지. 이 등급 체계가 무너지면 comparison_vs_ours.md 의 소환값 규율 전체가 같이 무너진다.
- **digest 본문의 ⛔/⚠ 금지·단서 문장** — 예: 'σ·D 절대값은 소환값, 계산 σ 는 인용 금지'([Shin26]), 'ε_p 0.51 eV 정량 인용 금지'([Liu24SbO]), '우리 v2/li2s 와 값 대 값 비교 금지'([Lai20]). digest 를 요약·압축할 때 제일 먼저 잘려 나가는 부분인데, 이게 잘리면 남는 건 출처 없는 숫자다.
- **철회값을 이름 대는 문장** — comparison_vs_ours.md:115 의 "단일시드 1.33× 철회, SEMIFINAL 07-09" 같은 표기. 그 줄의 σ 동등 주장은 고쳐야 하지만, **철회 사실을 명명하는 절반은 남긴다** (claim 결속 규율).
- **SE / DEM 두 트랙 분리 자체와 그 근거 문장** — INDEX_DEM.md:7-10 "한때 64편이 어느 인덱스에도 없었다(open_items #7)", comparison_vs_ours.md:8 "두 문서를 한 분모로 세면 '159편 중 98편 미언급' 같은 가짜 미결이 나온다". 통합하고 싶은 유혹이 있겠지만 분리는 실측 근거가 있는 결정이다.
- **litdb/figures/ 의 크로핑 PNG 2,764장 + 각 폴더 figures.json + _sources.json** — 원본 PDF 는 .gitignore 라 repo 에 없다. 용량 때문에 PNG 를 .gitignore 로 돌리는 결정은 할 수 있지만, **figures.json 과 _sources.json 은 절대 지우지 않는다** — 복원 경로가 이 둘뿐이다. 그리고 README:105-114 의 '실제로 돌려보고서야 드러난 버그 6개' 목록도 남긴다(같은 실수 반복 방지).
- **INDEX_DEM.md 는 생성물** — 손편집 금지(:3 이 그렇게 적혀 있다). 고칠 것이 있으면 build_index.py 를 고치고 재생성한다.
- **litdb/README.md 의 그림 추출 사용법(§🖼, :43-129)** — 낡은 것은 '현황' 숫자 3줄과 용량 예고뿐이고, venv 설치·litfig --inbox/--refresh/--audit/--why·pdf_map.tsv 예외 규칙·'못 하는 것(원고형 PDF·깨진 OCR)' 은 지금도 정확하다.
- **papers/_TEMPLATE.md 와 스켈레톤 헤더의 '⏳ 문서 대기 가 하나라도 남아 있으면 이 카드를 인용하지 않는다'** — 빈 카드가 인용되는 걸 막는 유일한 장치다. evidence_level 만 고치고 이 문장은 그대로 둔다.

## 발견

### [P0·wrong] sigma-equivalence-claim
- **어디**: `litdb/comparison_vs_ours.md:115`
- **근거**: 본문 축자: "우리 **BVSE Li-채널 부피 3.32/4.74/6.73 %… · UMA-MD σ300 b2o3/modelc **동등**(멀티시드 1.08/0.82/1.15; 단일시드 1.33× 철회, SEMIFINAL 07-09)** — **B₂O₃ = σ를 깎지 않는(보존) 안정화 도핑**". 그런데 db/properties/canonical_registry.json 의 MD_sigma_ratio_600K/800K/1000K(b2o3_vs_modelc, updated 2026-09-07, Codex BH P0-1)는 status=source_pending · citable=false · comparison_group="md-sigma-ratio-v1__NON_CITABLE" 이고 prohibitions 에 "statistically_equivalent_transport", "conductivity_preserved", "equivalent_sigma", "any_ranking_claim", "any_mechanism_claim", "absolute_sigma", "RT_extrapolation" 이 명시돼 있다. gate_detail 은 "미평가 쌍의 '같음' 은 동등이 아니라 **구분 실패**다" 라고 축자로 적는다. 한 문장이 금지 4개(동등·보존·기전/순위·RT 외삽)를 동시에 범한다. 게다가 1.08/0.82/1.15 는 db/properties/b2o3_vs_lpscl16_conductivity.csv 의 sig600/sig800/sig1000 비이지 300 K 값이 아니다 — "σ300" 은 온도 오표기다. CSV 헤더는 "PROTOCOL GENERATION: gen0_pre_gate … Gates G1(MTO)=NO, G2(traj retained)=NO -> G3 … G4 … are NOT ASSESSED (that is not a pass)". 이 줄은 2026-07-28(e79640517) 이후 손대지 않아 09-07 판정을 모른다.
- **고치는 법**: 레지스트리의 allowed_sentence 를 축자로 갈아끼운다 — "같은 3시드×3온도 집계에서 ΔEa 는 +0.002 eV 였고, 시드조합 산포 ±0.047 eV 가 두 추정치를 구분하지 못했다. 고온 원궤적이 보존되지 않아 비-Li 구조 상태는 평가되지 않았다." 그리고 "σ300"·"동등"·"보존"·"실현 사례로 포지셔닝" 을 지운다. 구조적으로는 citation_hazards.json 에 id=HZ-sigma-ratio-noncitable + forbidden_phrases("σ를 깎지 않는", "보존", "σ300", "동등")를 신설해 hazard_claims() 스캐너에 태운다 — 지금은 값이 null 이라 bound_claims(수치 결속)도, forbidden_phrases 도 이 주장을 못 잡는다.
- codex 필요: False

### [P0·missing] dem-baseline-missing
- **어디**: `litdb/our_dem_baseline.md (부재) — 참조 98곳 / 84개 파일`
- **근거**: litdb/comparison_vs_ours_DEM.md:3 "기준값: `our_dem_baseline.md`. 각 축마다 …" · :1019 "`our_dem_baseline.md §4` 와 σ_e 문서에 못박을 것" · :2495 "`our_dem_baseline.md §0`에 NCA 행 추가" · papers/kang2025_toughened_bimodal_nca_lzo.md:242 "## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`" 외 84개 파일 98회. `ls litdb/our_dem_baseline.md` = No such file. git 이력상 이 파일(55줄)은 origin/claude/solid-state-cathode-improvement-hevry0 에만 있고(e7b668377, 2026-06-26) HEAD 의 조상이 아니다 — 2026-07-16 "stoic-knuth 브랜치에서 통합" 때 digest 는 왔는데 기준값 파일은 안 왔다. SE 트랙에는 our_dft_baseline.md 가 있어 대칭이 깨져 있다.
- **고치는 법**: 타 브랜치의 `litdb/our_dem_baseline.md`(E_SE 22–24 GPa / DEM effective 1.35 / MPM 1.53·σ_y 0.15·0.30 / E_CAM 140 / σ_grain 3.0 mS/cm / porosity·Heckel·Furnas 표)를 정본 승격한다 — positioning_vs_geodict.md 가 2026-07-28 에 같은 절차를 밟은 선례가 있다. 다만 그 파일은 2026-07-15 판이고 DEM digest 는 2026-09-04 까지 늘었으므로, 옮기기 전에 각 행이 지금도 정본인지 확인이 필요하다.
- codex 필요: True

### [P1·wrong] beta-hard-gate-live
- **어디**: `litdb/comparison_vs_ours.md:222 · litdb/papers/wu2026_ta_argyrodite_selfpassivating.md:143,595`
- **근거**: comparison_vs_ours.md:222 오른쪽 칸: "우리 규약 **600/800/1000 K · prod 200 ps · MSD 창 2–50 ps · MTO 정본 · 3시드 · β̄ ≥ 0.80** (`db/properties/lpsocl_beta_registry.json`)". wu2026 digest 는 표로 두 번 반복한다 — "| **β (확산 지수) 게이트** | ⛔ | β̄ ≥ 0.80 (MTO) | ⛔ |". 그런데 db/properties/citation_hazards.json 의 id=HZ-beta-hard-gate 는 level=SUPERSEDED, forbidden_phrases=["β ≥ 0.80", "베타 하드게이트", "β 하드게이트"], why="kb/concepts/beta-gate.md §7-5(2026-08-26)·§7-8b(회신 F, 2026-08-27)에서 폐기. 우리 운영점에서 고정문턱 0.8 은 거짓탈락률 50 %". 즉 폐기된 문턱을 문헌 반박의 근거("우리 규약")로 세 곳에서 여전히 쓴다. 2026-09-08 결속 이주(12e6d0c9b)가 이 문구를 잡도록 forbidden_phrases 를 신설했지만, litdb 의 이 두 파일은 comparison_vs_ours.md(렌더 안 됨)와 digest 본문이라 실제로 걸리는 건 digest 쪽뿐이다.
- **고치는 법**: 세 자리 모두 판정축을 현행으로 교체 — "D_inc plateau · 창 안정성 · 홉 수"(citation_hazards fix 필드 축자). comparison_vs_ours.md 는 어느 화면에도 렌더되지 않아 결속 스캐너 밖이므로, 손으로 고치고 tools 쪽에 litdb 상위 md 를 forbidden_phrases 로 훑는 점검을 하나 붙인다.
- codex 필요: False

### [P1·wrong] gap-2098-drift
- **어디**: `litdb/comparison_vs_ours.md:436,437,441,442,452 (5행) · litdb/INDEX.md:194`
- **근거**: §D 안에서 우리 값이 두 갈래다. 새 행들은 "comp1 **2.066** / modelc **2.099** / +B₂O₃ **1.9671** / LPSOCl **2.2309** eV (fixed-occ nscf 고유값)" 로 정본을 쓰는데, 옛 행 5개는 "comp1 2.066 / modelc **2.098** (PBE)" 라고 쓴다(436 [Lu], 437 [Sundar], 441 [Li25], 442 [Rao], 452 [Rupp]). litdb/our_dft_baseline.md 헤더가 직접 금지한다 — "gap 2.099 는 fixed-occ nscf 고유값(canonical). **2.098 은 lobster_nscf 교차검증값이라 헤드라인에 쓰지 않는다.**" canonical_registry 에도 gap_eV/modelc = 2.099(canonical) 뿐이다. INDEX.md:194 도 같은 값을 쓴다.
- **고치는 법**: 5행 + INDEX.md:194 를 2.099 로 통일한다. 표 안에서 같은 물리량이 두 값으로 나오는 것 자체가 나중의 LLM 에게 "어느 쪽이 정본인지" 를 다시 논증하게 만든다.
- codex 필요: False

### [P1·wrong] index-aimd-mislabel
- **어디**: `litdb/INDEX.md:193-194`
- **근거**: "| 0-1 | [본 연구] Stoichiometric argyrodite | - | - | Li6PS5Cl **DFT AIMD** 종합 GAP=2.0656 eV …" / "| 0-2 | [본 연구] Cl-rich argyrodite | - | - | Li5.4PS4.4Cl1.6 **DFT AIMD** 종합 밴드갭 2.098 eV …". litdb/our_dft_baseline.md 가 2026-07-27 에 정정한 바로 그것이다 — "⚠ **방법 라벨 주의 (2026-07-27 정정)**: 우리 Ea·D 는 **AIMD 가 아니라 MLIP-MD**(UMA-s-1p1, omat)다. 진짜 AIMD 논문과 대조할 땐 '둘 다 AIMD라 직접 비교' 식으로 쓰지 말 것 — 힘 계산 축이 다르다." 정정이 baseline 에만 반영되고 INDEX.md 의 [본 연구] 두 행에는 14개월 전 Excel 문구 그대로 남았다.
- **고치는 법**: 두 행의 "DFT AIMD 종합" → "DFT(정적) + MLIP-MD(UMA-s-1p1)" 로 바꾸고 gap 을 2.066/2.099 로 맞춘다. 더 나은 쪽은 [본 연구] 두 행을 INDEX 에서 빼고 our_dft_baseline.md 링크 한 줄로 대체하는 것 — 우리 값이 문헌 인덱스 안에 사본으로 존재하는 게 drift 의 원인이다.
- codex 필요: False

### [P1·stale] index-selfreport-stale
- **어디**: `litdb/INDEX.md:6,8`
- **근거**: :6 "두 인덱스 어디에도 없는 digest 는 `python3 tools/litdb/build_index.py --check` 로 잡는다 **(2026-08-06 기준 0편 — open_items #7 해결)**" — 지금 그 명령을 돌리면 "어느 인덱스에도 없는 것 **5편**" 이 나온다. :8 "자동 생성 from Excel (`dbce603a`). **갱신: 2026-06-23.**" — 파일 자체는 2026-09-08(66d5a3f3f)에 커밋됐고 본문에 2026-09-03 신설 절이 4개 있다. 즉 자기 날짜와 자기 상태를 둘 다 틀리게 말한다.
- **고치는 법**: 헤더의 "0편" 을 지우고 "현재값은 --check 로 확인" 으로 바꾼다(수를 박으면 또 밀린다). "갱신: 2026-06-23" 은 "Excel 초판 2026-06-23 · 이후 손 큐레이션" 으로.
- codex 필요: False

### [P1·stale] comparison-coverage-stale
- **어디**: `litdb/comparison_vs_ours.md:10`
- **근거**: 축자: "> **현재: DFT 트랙 64/64 편입 (2026-08-06).**" 실측(build_index.py --check): "DFT  94/98  → comparison_vs_ours.md   미편입 4편", "DEM  46/117 → comparison_vs_ours_DEM.md   미편입 71편". 분모도 분자도 틀렸고, 무엇보다 DEM 트랙이 39% 편입이라는 사실이 이 줄에도 DEM 문서에도 안 적혀 있다.
- **고치는 법**: 고정 숫자를 지우고 --check 출력 인용으로 바꾼다. DEM 미편입 71편은 별도 항목으로 드러내야 한다 — 지금은 아무 문서도 그 구멍을 말하지 않는다.
- codex 필요: False

### [P1·stale] readme-status-stale
- **어디**: `litdb/README.md:90-92,128`
- **근거**: :90-92 "**현황 (2026-08-06)**: 논문 **112편 / 그림 1,593장** (본문 882 + SI 472 + 표 239), audit 깨끗 86편. digest 159편 중 112편(70%)에 그림이 붙었다 … 작업트리 **432 MB**." 실측: 그림 폴더 179개 · PNG 2,764장(fig_ 2,376 + tab_ 382) · digest 215편 · litdb/figures 1,020 MB. :128 "(지금 112편 432 MB · .git 은 재생성 이력 때문에 **1 GB 대**) PNG 만 .gitignore 하고 figures.json 만 추적하는 쪽으로 바꾼다" — 실측 .git = **4.4 GB**, 작업트리 1.3 GB 중 litdb 가 1.1 GB(85%). README 자신이 적어둔 전환 조건("규모가 커지면")이 이미 4배 초과된 채 방치돼 있다.
- **고치는 법**: 숫자를 손으로 적지 말고 `litfig --audit` 요약이나 build_index 출력에서 받아 쓰게 한다. 그리고 PNG .gitignore 전환은 README 가 스스로 예고한 조치이므로 1저자 결정 안건으로 올린다(figures/_sources.json 179 항목이 있어 `--inbox --run` 복원 경로는 이미 있다).
- codex 필요: False

### [P1·missing] readme-front-door-half
- **어디**: `litdb/README.md:1-13,25,32`
- **근거**: :1 "# 📚 LITDB — Argyrodite SE 문헌 단일 시스템" 인데 digest 215편 중 DEM 트랙이 117편이다. :6-13 폴더 구조표 6행이 언급하는 것은 INDEX.md · papers/ · our_dft_baseline.md · comparison_vs_ours.md · properties/*.md · figures/ 뿐. **`properties/` 는 존재하지 않는다**(:12 와 :32 두 번 가리킴, `ls litdb/properties` = No such file). 반대로 실재하는 INDEX_DEM.md(117편)·comparison_vs_ours_DEM.md(3,210줄)·talks/(9편+README)·surveys/(2편)·topics.json·pdf_map.tsv 일부·_INDEX_proposals.md·positioning_vs_geodict.md·yonsei_dtbl_lab_triage_2026.md 는 README 에 한 글자도 없다.
- **고치는 법**: 구조표를 실물에 맞춰 다시 쓰고 맨 앞에 '두 트랙(SE/DEM)' 을 명시한다 — 왜 나눴는지는 INDEX_DEM.md:7-10 에 이미 잘 적혀 있으니 그 문장을 README 로 올린다. 죽은 `properties/*.md` 2곳은 지우거나 db/properties/ 로 정정한다.
- codex 필요: False

### [P1·duplicate] han2025-double-index
- **어디**: `litdb/papers/han2025_icep_conductive_elastic_binder.md ↔ litdb/papers/han2025_icep_binder_ultrahigh_loading_ncm811.md`
- **근거**: 같은 논문이다 — 둘 다 DOI `10.1002/adma.202506266` (Adv. Mater. 2025, 37, 2506266). 그런데 서로를 한 번도 언급하지 않는다(상호 참조 grep 0/0). 더 나쁜 건 **두 트랙에 따로 등재돼 있다**: `han2025_icep_conductive_elastic_binder` 는 INDEX_DEM.md 1회 + comparison_vs_ours_DEM.md 3회, `han2025_icep_binder_ultrahigh_loading_ncm811` 은 INDEX.md 1회 + comparison_vs_ours.md 2회. 수치는 같지만(둘 다 ICEP_AMPS −1.819 / (−H) −2.243 eV) 서술 깊이가 다르다 — 구판(181줄, 2026-08-06)은 "| ICEP_AMPS(-H) | **−2.243 eV** | 설폰산–표면 O 수소결합 |" 이라고 단서 없이 표에 넣고, 신판(831줄, 2026-08-29)은 §4.3 에서 전하상태·state-selection policy 부재를 확정 판정한다. DEM 쪽에서 들어온 독자는 단서 없는 값을 본다.
- **고치는 법**: 신판(831줄)을 정본으로 두고 구판을 bzox 방식의 3줄 묘비 스텁으로 바꾼다(선례: papers/bzox_dry_zro2x_nmc_shell_coating_sulfide_assb.md). INDEX_DEM·comparison_vs_ours_DEM 의 4개 참조를 신판 slug 로 바꾸고, 트랙 카운트 중복(215 에 1 과다)도 같이 해소된다.
- codex 필요: False

### [P1·wrong] skeleton-evidence-level
- **어디**: `litdb/papers/{ketter2025_resistor_network_models_predict_transport_properties, kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable, liu2026_planar_li_deposition_dissolution_enable_practical, wang2026_domain_oriented_universal_machine_learning_potential}.md:8`
- **근거**: 네 스켈레톤 모두 헤더 8행에 "> · evidence_level `fulltext`" 라고 적으면서 같은 카드 5행에 "· PDF `⏳ 미확보` · status `🌱 skeleton (문서 대기)`" 라고 적고, 63행 체크리스트에는 아직 할 일로 "- [ ] `status` 를 `✅` 로, `evidence_level` 을 `fulltext` 로" 가 남아 있다. 즉 아직 해야 할 일이 이미 된 것처럼 헤더에 박혀 있다. CLAUDE.md 절대 규칙 위반이다 — "초록/전문이 없으면 `evidence_level`을 `snippet`/`title`로 적고 `follow_up`에 '전문 확보' 를 남긴다". 실제 피해 경로도 있다: 같은 CLAUDE.md 의 충돌 규칙이 "같은 논문에 분석이 둘이면 `evidence_level`이 높은 쪽(fulltext > abstract > snippet > title)을 남긴다" 이므로, 나중에 진짜 초록 기반 분석이 들어와도 이 빈 카드가 이긴다. (다섯 번째 unknown2025 는 `snippet` 으로 올바르다.)
- **고치는 법**: 네 파일의 8행을 `title`(또는 초록 확보분은 `snippet`)로 내린다. 생성기(research-agent/research_agent/exporters/litdb.py) 쪽에서 skeleton 을 만들 때 evidence_level 을 fulltext 로 찍지 않게 막는 게 근본 수정이다.
- codex 필요: False

### [P1·broken] check-ignores-proposals
- **어디**: `tools/litdb/build_index.py:190-197 (check())`
- **근거**: check() 는 `missing = [p for p in papers if p["id"] not in se and p["id"] not in dem]` 로 INDEX.md·INDEX_DEM.md 두 파일만 본다. 그런데 그 5편은 전부 litdb/_INDEX_proposals.md 에 이미 적혀 있고, 그 파일 머리말이 그렇게 하라고 못박는다 — "⛔ **여기서 INDEX.md 로 옮기는 것은 사람이 한다.** INDEX 항목은 손으로 쓴 분석 산문이라 자동 append 하면 오염된다." 즉 규율대로 대기 중인 카드를 도구가 매번 결함으로 보고한다. 결과: --check 가 상시 5 를 찍어 '0 = 깨끗' 신호가 죽었고, 진짜 미등재가 생겨도 안 보인다. (부수적으로 판정이 substring 이라 slug 가 다른 slug 의 부분문자열이면 조용히 통과한다.)
- **고치는 법**: check() 가 _INDEX_proposals.md 를 세 번째 장부로 읽고, `🌱 skeleton` 상태인 digest 는 "대기(사람 승인 필요) n편" 으로 **분리 집계**한다. 그러면 0 이 다시 의미를 갖는다.
- codex 필요: False

### [P1·stale] index-dem-not-regenerated
- **어디**: `litdb/INDEX_DEM.md:5`
- **근거**: "> digest **114편** · 생성 2026-09-03" 인데 실제 표 행은 115개이고 build_index.py --check 는 DEM 트랙을 **117편**으로 센다. 이 파일은 손으로 고치면 안 되는 생성물인데(:3 "이 파일은 `tools/litdb/build_index.py` 가 생성한다 — 손으로 고치지 말 것.") 09-03 이후 digest 가 늘었는데도 재생성이 안 돌았다. 같은 도구 docstring 도 "digest 159편 중 64편이 어느 인덱스에도 없었다" 로 2026-08-06 시점에 멈춰 있다(현재 215편).
- **고치는 법**: `python3 tools/litdb/build_index.py` 한 번. 그리고 digest 추가 시 자동으로 돌게 걸어 둔다(litdb-curator 마무리 단계 또는 pre-commit) — 손으로 기억하는 한 또 밀린다.
- codex 필요: False

### [P1·broken] lit-prefix-dead-links
- **어디**: `litdb/yonsei_dtbl_lab_triage_2026.md (lit_ 등장 45회 · 고유 파일명 22개)`
- **근거**: 합병 전 브랜치의 파일명 규약이 그대로 남았다 — 예: :889 "✅ 풀 디제스트 (`lit_lim2025_virtual_calendering_framework.md`)", :900 "(`lit_choi2024_digital_twin_review_echem.md`)". 22개 중 **21개는 `lit_` 접두만 떼면 papers/ 에 실재**하고(lim2025_virtual_calendering_framework, choi2024_digital_twin_review_echem, oh2026_bimodal_composite_cathode, nam2026_dpe_microstructure_review …), 1개는 이름까지 바뀌었다 — :550 "`docs/lit_kim2025_conductive_agent_se_coating_assb.md`" 의 실물은 `litdb/papers/kim2025_conductive_agent_se_coating_cathode.md` 다. 22개 전부 지금은 클릭도 grep 도 안 걸린다.
- **고치는 법**: `lit_` 접두 일괄 제거 + kim2025 한 건은 `_cathode` 로 이름 수정. 같은 종류로 comparison_vs_ours_DEM.md:271,2536 의 `papers/li2026_sulfide_stability_review_ecer.md` 도 실물이 `papers/fan2026_sulfide_assb_stability_review_ECERD2600097.md` 다.
- codex 필요: False

### [P1·buried] l3-db-split-unregistered
- **어디**: `litdb/comparison_vs_ours.md:1393-1410 (§L-3)`
- **근거**: §L-3 이 우리 db 내부 분열을 잡아냈다 — "스플라인 최대 **0.28968 eV @ xi = 0.4100** ← 원고의 0.290 / 실제 최고 계산점 **img3 = 0.2866 eV** / `diffusion.json` 헤드라인 **0.287**" → "**우리 db 안에서 값이 갈라져 있다**(0.287 vs 0.28968) — 이건 **db 쪽을 정리해야 하는 예외**다". 그런데 db/properties/citation_hazards.json 에도 db/governance/decisions.json 에도 이 건은 없다(0.28968 grep 은 원자료 CSV 2건과 kb/syntheses 1건만). 투고 중 원고의 P0 두 건(§L-2 Fig.5d 실선·Methods §4.6 QE 단계 누락)도 마찬가지로 여기 1,346행 아래에만 있고 1,480줄 문서의 맨 끝, 축 12개 중 11번째다.
- **고치는 법**: §L 의 P0/P1 세 건을 db/governance/decisions.json 또는 citation_hazards.json 에 항목으로 올리고(0.287 로 통일 권고 포함), comparison_vs_ours.md 에서는 원장을 가리키게 한다. 자기 원고 감사는 문헌 비교 문서의 12번째 절이 있을 자리가 아니다 — 애초에 §L-0 이 "⛔ '문헌 vs 우리' 가 아니다" 라고 자인한다.
- codex 필요: False

### [P2·useless] index-legacy-excel-sheets
- **어디**: `litdb/INDEX.md:136-207 (시트 실험값 25행 · 계산값 18행 · DFT 관련 14행)`
- **근거**: 2026-06-23 Excel 자동 덤프가 그대로 있다. 제목이 잘려 있고("Superionic Halogen-Rich Li-Argyrodites Using In Situ Nanocrystal Nucle"), DOI 자리에 잘린 URL 이 들어가 있고("https://pubs.acs.org/doi/full/10.1021/acs.nan"), 빈 행이 있고("| 17.0 |  |  |  | L6.16P0.92In0.08SCl … |"), 셀 안에 점만 남은 것도 있다("…3.48 V; .0.........................................................."). 세 시트 57행 전부 status 가 📄(Excel만) 이고, Adeli 2019 처럼 이미 ✅ digest 가 있는 논문이 시트에도 중복으로 앉아 있다. 절 제목의 개수(21/18/14)와 실제 행수(25/18/14)도 안 맞는다.
- **고치는 법**: digest 가 있는 행은 지우고, 아직 digest 가 없는 행만 남겨 이름을 '미digest 후보(Excel 유래)' 로 바꾼 뒤 INDEX 맨 아래 접힘 구역으로 내린다. 잘린 셀은 근거로 못 쓰므로 값이 필요하면 원 Excel 이나 논문에서 다시 받는다.
- codex 필요: False

### [P2·duplicate] index-pdf-inventory-duplicate
- **어디**: `litdb/INDEX.md:209-277 (51행)`
- **근거**: 절 제목이 "## 📂 보유 PDF (지금까지 \"먹인\" 논문 — **28개**, ~25 unique)" 인데 표는 51행이고, 항목의 키가 세션 한정 업로드 id 다 — "| 1 | d0102fe3 …Zuo… (＝ 재업로드 `82ea256b/7dd4f5c1 …`)", "| 39 | 82ea256b/bd05d979 (…firstprinciples…2dhbn…)". 그 id 는 지금 아무 데서도 안 풀린다. 게다가 미해결 메모가 붙어 있다 — "*(#9–22 일부는 제목 미확인 — digest 시 curator가 PDF 첫 페이지에서 확정. #19 `High_perfo…eries`는 Kraft2017(inbox #31)과 동일 논문일 가능성 — upload-id 다름, 미…". 같은 정보의 기계 정본이 이미 있다: litdb/figures/_sources.json 이 slug → 원본 PDF 상대경로를 179개 담고 있고 generated 날짜가 2026-09-07 까지 온다.
- **고치는 법**: 절 전체를 지우고 "slug↔PDF 대응은 `litdb/figures/_sources.json` (179편, 자동 갱신)" 한 줄로 대체한다. 아직 digest 가 없는 PDF 만 남기려면 그 목록도 _sources.json 과 papers/ 차집합으로 뽑는 게 맞다.
- codex 필요: False

### [P2·ia] index-append-only-order
- **어디**: `litdb/INDEX.md (21개 절, 특히 :136-277 vs :419-481)`
- **근거**: 절 순서가 시간이 아니라 붙인 순서다. 위쪽 절반은 MUST-READ(1행) → Digest 완료(66행) → talks(5행) → EXTERNAL(10행) → **Excel 시트 57행** → **보유 PDF 51행** 이고, 2026 하반기에 새로 판 축은 전부 아래에 붙었다 — :419 "CAM 고유 전달물성 앵커 (2026-08-25 신설)", :429 "SDCP (2026-09-03 신설)", :441 "수계 Zn 음극 (2026-09-03 신설)", :455 "Li–S 전환형 (2026-09-03 신설)", :470 "확률적 voxel 생성기 계보 (2026-09-03 신설)". 즉 가장 죽은 108행이 가운데 위, 가장 최근 5개 축이 맨 끝이다. 한 줄 평균 972자·최장 15,710자라 스크롤로도 못 훑는다.
- **고치는 법**: 순서를 ① MUST-READ ② 최근 신설 축(역순) ③ Digest 완료 ④ EXTERNAL/talks ⑤ **레거시(Excel·보유PDF) 접힘** 으로 뒤집는다. '최신·중요한 것이 앞, 옛것은 접힘' 을 이 파일에 먼저 적용하는 게 재편의 본보기가 된다.
- codex 필요: False

### [P2·ia] dem-mustread-in-blockquote
- **어디**: `litdb/comparison_vs_ours_DEM.md:5,40`
- **근거**: 가장 중요한 블록이 인용문 안 제목이라 목차·아웃라인에 안 잡힌다 — ":5 `> ## ⭐필독 / 우리-랩 — **Jong-Won Lee 그룹(Hanyang) 자매 논문 2편** = 모델이 따라가야 할 실험 trend의 기준점.`" 와 ":40 `> ## 🎤 발표 덱 (papers/ 보다 한 등급 낮음 — talks/README.md)`". `grep "^## "` 로 목차를 뽑으면 A~G 7개 축과 Q&A 만 나오고 이 둘은 사라진다 — 3,210줄 문서에서 사실상 안 보인다.
- **고치는 법**: 두 블록을 `>` 밖으로 꺼내 정식 `##` 절로 올리고 A 축 앞에 둔다. 인용 표시가 필요하면 내용만 blockquote 로 감싼다.
- codex 필요: False

### [P2·ia] curator-knows-only-se
- **어디**: `.claude/agents/litdb-curator.md:52,54,56 (마지막 커밋 2026-08-26)`
- **근거**: 인입 에이전트가 SE 트랙만 안다. :52 "**Compare vs our baseline** (`litdb/our_dft_baseline.md`): fill §7 …" — DEM 논문이 들어와도 our_dem_baseline 을 모른다(애초에 파일도 없다). :54 "`INDEX.md`: set the paper's status → ✅" — INDEX_DEM.md·_INDEX_proposals.md 를 모른다. :56 "`properties/<prop>.md` if it exists" — 없는 폴더. description 도 "Updates INDEX.md and comparison_vs_ours.md" 로 끝난다. 이게 DEM 편입률이 46/117(39%)에 머문 구조적 이유로 보인다(DFT 는 94/98).
- **고치는 법**: 에이전트에 트랙 분기를 넣는다 — track 판정 후 SE 면 INDEX.md+comparison_vs_ours.md, DEM 이면 INDEX_DEM.md 재생성+comparison_vs_ours_DEM.md, 실물 미확보면 _INDEX_proposals.md. baseline 도 트랙별로 가리키게 한다(our_dem_baseline 복원이 선행 조건).
- codex 필요: False

### [P2·missing] no-cheap-manifest-for-llm
- **어디**: `litdb/ (전체 — 기계 판독 목록 부재)`
- **근거**: 나중의 LLM 이 "litdb 에 무엇이 있나" 를 알려면 INDEX.md 150 KB(평균 972자/줄) 나 INDEX_DEM.md 를 통째로 읽어야 한다. CLAUDE.md 컨텍스트 규율은 "kb/index.md(25 KB)는 통째로 읽지 말고 grep" 이라고 하는데, litdb 에는 grep 으로 뽑을 짧은 정본 목록이 없다 — 있는 건 webapp/data.py 의 list_papers() 함수(코드)와 topics.json(태그 13편분)뿐이다. figures/_sources.json 은 PDF 경로만 담는다.
- **고치는 법**: build_index.py 에 `--manifest` 를 붙여 `litdb/MANIFEST.tsv`(slug · track · type · digested · 그림수 · 한 줄 요약, 한 줄 200자 이내)를 생성한다. 새 파일이 아니라 기존 도구의 플래그로 — 코드 규율 사다리 ③.
- codex 필요: False

### [P2·ia] seminar-and-tombstone-in-papers
- **어디**: `litdb/papers/*__seminar_5min_qa.md (3편) · litdb/papers/bzox_dry_zro2x_nmc_shell_coating_sulfide_assb.md (3줄)`
- **근거**: papers/ 에 논문이 아닌 것이 섞여 있다. 세미나 대본 3편은 "# 🎤 PS-LPSC 논문 세미나 — 5분 발표 대본 + Figure별 예상 질문" 처럼 발표물이고 webapp/data.py:3196 이 `if "__seminar" in f.stem: continue` 로 걸러낸다(2026-08-28 규약). 즉 규약은 코드에만 있고 README·talks/README 어디에도 없다 — talks/ 라는 발표물 전용 폴더가 따로 있는데도 그렇다. 묘비 스텁은 본문이 "# → superseded by `choi2026_bzox_dry_zro2x_nmc_shell_coating.md`" 3줄뿐인데 digest 로 계수되고 build_index --check 의 DEM 미편입 목록에도 이름이 오른다.
- **고치는 법**: 세미나 대본 규약(왜 papers/ 에 두는지, talks/ 와 무엇이 다른지)을 litdb/README.md 와 talks/README.md 에 한 줄씩 적는다 — 코드에만 있는 규약은 다음 세션이 못 찾는다. 묘비 스텁은 list_papers 에서 `superseded by` 헤더를 인식해 카운트·미편입 보고에서 빼면 된다.
- codex 필요: False

### [P2·buried] surveys-orphaned
- **어디**: `litdb/surveys/nd_substitution_54papers_2026-07.md · litdb/surveys/md_structure_setup_halogen_rich_2026-07.md`
- **근거**: 두 파일 모두 litdb 안 어느 md 에서도 참조되지 않는다(`grep -rn "surveys/"` 로 litdb/surveys 자신 말고 히트 0). 접근 경로는 webapp /nd-survey 라우트 하나뿐이다. 내용도 Notion 붙여넣기 상태로 남아 있다 — 첫 줄이 유령 제목 "# 재현", 다음이 "# 원소 치환 문헌 **57개** 분석"(파일명은 54papers), 본문은 `<aside>` HTML + 존댓말("…분리했습니다"). 마지막 커밋 2026-07-28 이라 2026-09-08 Nd2O3-LPSCl1.6 어닐 6셀 회수(83c868a97, 순위 distributed < free_s < bo4)와 연결이 없다.
- **고치는 법**: README 구조표에 surveys/ 를 넣고, Nd 서베이는 최근 Nd cascade·어닐 결과와의 연결 한 줄을 머리에 붙인다(문헌 수치와 우리 값은 섞지 않는 선에서). 유령 "# 재현" 제목과 57/54 불일치는 그 자리에서 정리.
- codex 필요: False
