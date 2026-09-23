# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, verify, archive, delete

## [2026-07-30] create | Wiki initialized
- Scaffolded from llm-wiki harness (tools + commands + hooks + CI).
- Domain: 이 저장소의 도메인을 한 문장으로 적는다 (무엇에 관한 자료를 모아 무엇에 재사용하는가).

## [2026-07-30] create | Mothership 변환 + 킥오프 가이드
- SCHEMA/CLAUDE/AGENTS 에 Mothership 특칙 추가 (satellite entity 등록, living reference, transcripts).
- guides/new-project-kickoff.md 추가 — `<MOTHERSHIP>` placeholder, 배치 후 실제 경로로 치환.

## [2026-08-06] update | 하네스 v1.8~v1.10 채택 (원본 위키에서 전파)
- frontmatter: `model`/`effort` provenance + `claimType`/`evidenceScope` (single-source→confidence high 금지), 타입 2종 신설 (`questions/` research-question · `syntheses/` synthesis).
- Paper Ingest Mode opt-in 특칙 + guide [[paper-ingest-mode]] + raw changelog. SCHEMA/CLAUDE/AGENTS(parity)/tools/hook/ingest 커맨드/init-wiki.sh 갱신, lint 검사 12~15 추가.

## [2026-08-11] create | Yonghoon-DEM-DFT mothership 이식·적응
- llm-wiki-kit_260730 을 repo root `wiki/` 로 이식. 적응: `wiki-` 접두 커맨드(root `.claude/commands/`), hook 를 `wiki/tools/hooks/` + root settings.json 으로, cross-vault 참조를 repo-root 상대 경로로, 커밋 prefix `<action>(wiki):`, wiki-lint CI (`wiki/**` path filter). 근거: 강의 전사 + 킷 (아래 ingest).
- 연구 파이프라인 경계 명시: `wiki/` 는 degradation-degeneracy 의 code identity(`source_digest`) 밖 — 게이트 리뷰 대상 코드 불변.

## [2026-08-11] ingest | LLM Wiki 강의 (KIST, 커맨드스페이스 구요한)
- raw/transcripts/2026-08-11-llm-wiki-lecture-kist.md (유튜브 자동 전사, 수집 목적: 이 위키 구축의 근거). 컴파일: [[llm-wiki-pattern]].

## [2026-08-11] create | 프로젝트 지식 분류 — satellite 등록 + 개념/가이드/질문 카드
- raw/repositories/degradation-degeneracy-audit.md (기존 프로젝트 감사 스냅샷, HEAD c9970ebc).
- 페이지 5: [[degradation-degeneracy]](entity) · [[fitting-degeneracy]] · [[provenance-fail-closed-verification]] · [[gate-review-loop]] · [[22p-physics-or-degeneracy]](research-question, active).
- 원칙 준수: 수치·발견 상세는 위키로 복사하지 않음 (정본 = artifact·docs, living reference).

## [2026-08-11] ingest | 에이전트 하네스 3종 (ponytail · caveman · superpowers)
- raw/repositories/2026-08-11-agent-harness-repos.md (WebFetch 요약, 원문 아님 — sha256 봉인).
- 컴파일: [[agent-harness-patterns]] — 채택/각색/기각 판단표와 근거.

## [2026-08-11] create | 작업 규율 이식 — 루트 CLAUDE.md + 커맨드 4종
- 루트 `CLAUDE.md` 신설 (저장소 지도, 하드룰, 작업 규율 4항, RUN_SCOPE 경계).
- `.claude/commands/`: /finding(RED-first + fixture 감사) · /lean-review(사다리, 검증 carve-out) · /self-review(다각 렌즈) · /gate-request(기계용 밀도).
- 플러그인 통째 설치는 기각 — 전역 훅이 게이트 리뷰 중인 저장소 행동을 바꾼다.

## [2026-08-11] query | /lean-review 첫 실행 — 중복 후보 원장화
- env 결정축 비교가 baseline.py·halfcell.py 3곳 중복 + _ENV_KEYS 레이어링 어긋남 확인.
- **실행 보류**: 13차 리뷰가 c9970ebc 대상으로 열려 있어 source_digest 변경 금지. [[lean-review-backlog]] 에 원장화.

## [2026-08-20] lint | 브랜치 이름 drift 차단 + 죽은 study-path 검사 제거
- 브랜치 통독 중 발견: 위키 5개 파일(SCHEMA/CLAUDE/AGENTS/README/[[degradation-degeneracy]])과 위키 밖 3곳이 **이미 흡수된 브랜치**를 작업 브랜치로 지목하고 있었다. 브랜치 이름의 정본을 루트 `CLAUDE.md` 하드룰 1 하나로 모으고, 위키는 그것을 참조하게 바꿨다.
- `tools/lint.py` 검사 15 신설 — 위키 파일이 브랜치 이름을 하드코딩하면 error. `raw/` 면제(봉인 스냅샷), `.claude/`·`.github/` 경로는 오탐 안 함. 변이 3종으로 확인(주입 시 검출 / 경로 오탐 없음 / raw 면제).
- 킷의 study-path 커버리지 검사와 status 진도 바 제거 — `guides/llm-wiki-study-path.md` 가 없어 **한 번도 실행된 적이 없는** 검사였다. 조용히 통과하는 검사는 커버리지로 오독된다.

## [2026-08-20] update | 본 실행 결과를 satellite·질문 카드에 반영
- [[degradation-degeneracy]]: 13차 대기 → 19차 완료·본 실행 완료로 갱신. 결론 1 철회 / 2 한정 / 3 축소를 상태에 기록(수치는 옮기지 않음 — 정본은 artifact + docs/RESULTS*.md). 한계 절에 남아 있던 모집단 숫자 사본을 참조로 교체.
- [[22p-physics-or-degeneracy]]: 실행 후 Evidence 갱신 — dQ/dV 이점 근거는 **철회**(paired 정본에서 모든 noise 층에 걸쳐 열세), 좌표 원점·restart 예산 축을 새 근거로 추가. status 는 `active` 유지: 질문이 "물리인가"에서 "어떤 모델 정확도·최적화 예산에서 의미를 갖는가"로 좁혀졌다.
- [[lean-review-backlog]]: 보류 사유를 닫힌 13차 리뷰에서 진행 중인 민감도 스윕으로 갱신(영구 부채화 방지).
- 루트 `BRANCHES.md` 신설 — 38개 브랜치의 계열·흡수 관계 지도. degradation-degeneracy 는 갈라져 있지 않음을 실측으로 고정.
- 21차 게이트 리뷰 회답(문서 라운드): [[22p-physics-or-degeneracy]] 의 "모든 noise 층에서 열세" 를 `warm_start=False` protocol 조건부로 재정정 — warm 을 켜면 한 층에서 방향이 뒤집힌다. `wiki/tools/{status,lint}.py` 의 stdout 을 UTF-8 로 재구성(CP949 콘솔에서 status.py 가 죽던 것을 실측 후 수정). `BRANCHES.md` 의 `main` 고립 주장 정정 — shallow clone 산물이었고 full clone 에서는 37/37 브랜치의 공통 조상이다.

## [2026-09-03] ingest | 2026-09-02 BML 세미나 (김시원) — degradation mode ML 프레임워크
- raw 2건 봉인: `raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md` (PDF 15쪽 **페이지별 해체분석** — `[인쇄]`/`[도표]`/`[해석]` 3구분으로 원문 주장과 우리 판단을 분리), `raw/transcripts/2026-09-03-voice-memo-007-degradation-mode-ml.md` (구술 메모 전문 + 전사 오인식 대조표 30여 항 + 슬라이드에 없고 구술에만 있는 7가지). 구술은 **09:15 에서 끊겨** p.12~15 가 녹음에 없다 — 그 한계를 파일 머리에 적었다.
- 컴파일 2건: [[pvs-sev-degradation-mode-features]] (concept — PVS/SEV 정의·물리 귀속·모드별 부호표), [[pvs-sev-lli-lampe-separability]] (research-question, status open).
- 발견의 요지: 두 feature 의 **모드별 부호 패턴이 동일**하다 ({LLI, LAM_PE} ↑ vs {LAM_NE} ↓). 부호가 같다고 벡터가 평행한 것은 아니므로 확정은 아니지만, 확정되면 LLI↔LAM_PE 방향에 새 정보가 없다는 뜻이 된다. 원문 p.13 permutation importance 에서 PVS 가 네 target 모두 최하위권이고 LAM_PE 예측을 SOH+프로토콜 식별자가 지배하는 것이 같은 방향의 정황.
- [[22p-physics-or-degeneracy]] 에 분기 기록 추가 (status 는 `active` 유지 — 새 근거 없이 갈라진 질문만 등록).
- 이 커밋은 `wiki/` 만 건드리므로 degradation-degeneracy 의 `source_digest` 를 바꾸지 않는다 (진행 중인 57차 게이트 대상 커밋과 무관).

## [2026-09-03] create | 논문 에이전트 이식 + satellite mode-observability 개설
- **논문 에이전트**: DFT/argyrodite 계열 브랜치(루트 `BRANCHES.md` 지도 참조, e80dd480)의 litdb-curator 를 이 브랜치 위키 구조로 이식 — `.claude/agents/paper-curator.md` (digest 는 `wiki/raw/papers/` sha256 봉인 + 컴파일 페이지 연결, 축은 argyrodite/DFT → 열화 모드 식별 가능성으로 교체). figure 크로퍼 `wiki/tools/extract_figures.py` 는 같은 코드의 경로 이식본 (캡션 앵커·기하 검증 로직 원본 유지, pymupdf 필요).
- 크로퍼 실측: 2026-09-02 세미나 덱 15쪽을 `--slides` 로 잘라 `wiki/raw/figures/2026-09-02-siwon-kim-degradation-mode-ml-seminar/` 에 15장 + figures.json 등록 (전체 4.3 MB).
- **[[mode-observability]]** (둘째 satellite, repo root `mode-observability/`) 개설: "관측을 늘리면 갈리는가" — Phase 1 PVS Jacobian · Phase 2 SEV P2D · Phase 3 ML 라벨 degeneracy 전파. 셋 다 미착수. [[pvs-sev-lli-lampe-separability]] 의 feedsInto 를 이 satellite 로 연결.

## [2026-09-03] update | mode-observability Phase 1 첫 실측 (PVS 모드 감도)
- 합성 truth 격자(noise=0, 1023 조건)에서 PVS 계산 + 유한차분 감도. 22p 동작점 근방에서 세 모드 감도 동부호(PVS 단독으로 LLI↔LAM_PE 안 갈림, H1 쪽), pristine 에서는 세미나와 부호가 다름(검증 전 인용 금지 — LLI 스윕 비단조, feature tracking 의심). valley 정의 민감성(−20.0 vs −11.3)이 세미나 discussion point 3 을 실측으로 확인. [[pvs-sev-lli-lampe-separability]] Status Log 에 등재, 정본은 satellite 의 pvs.csv + PHASE1_NOTES.md.

## [2026-09-03] ingest | Birkl et al. 2017 — 우리가 판정 대상으로 삼는 OCV fitting 절차의 원전
- raw 1건 봉인: `raw/papers/birkl2017_degradation-diagnostics-ocv.md` (*J. Power Sources* **341** (2017) 373–386, doi:10.1016/j.jpowsour.2016.12.011, CC BY — 게재본 14쪽 **절별 해체분석**, `[인쇄]`/`[도표]`/`[해석]` 3구분). 그림 크로핑 14장(fig 8 + tab 6) → `raw/figures/birkl2017_degradation-diagnostics-ocv/`; 그중 fig 3·4·5·6·7·8 과 tab 2 를 **실제로 열어 보고** digest 를 썼다 (fig 1·2 는 우리 축에 안 걸려 생략 — digest §12 에 명시).
- 컴파일 1건: [[birkl-ocv-degradation-diagnostic]] (concept — 3단계 절차·자유도·컷오프 등식·저자 진술 축퇴·인용 금지 문장).
- **핵심 발견 셋**:
  1. **저자들은 식별 가능성에 침묵하지 않는다.** §4.2 가 `pure-LLI + LAM_de ↔ LAM_li` 축퇴를 명시하고, 3-파라미터 출력이 그 **동치류 좌표**임을 알고리즘 설계 이유로 적는다. 즉 이 계열의 LAM 은 총량이고 LLI 는 total 이다 — 하위 귀속을 주장하는 후속 인용은 원전이 허용하지 않는다. 다만 3-파라미터 **공간 안에서의** 식별 진단(상관·Hessian·신뢰구간·노이즈 스윕)은 전무하다.
  2. **★ 우리가 재는 절차가 원전과 같지 않다.** 원안은 자유 파라미터 **3개**이고 `Δx_EoC`/`Δx_EoD` 를 컷오프 전압 등식으로 **소거**한다 (우리 문서의 창 모델 α/β 4개에는 그 제약이 없다). 우리가 본 degeneracy 의 일부가 원전에 없는 자유도에서 올 수 있다 — 검증 가능한 가설.
  3. **검증 구조**: 합성 3점은 **inverse crime**(생성=적합 모델, 노이즈 0, RMSE 0.0 mV)이고, 실험 검증은 제작 코인셀 6종(정답 = 제작 설계값, **해체 대조 없음**). 오차 막대 5.4% 는 **제작 재현성**이지 추정 불확실성이 아니다 (논문이 §4.3 에서 명시).
- 원문 결함 기록: Table 2 의 LLI 셀 전극 지름 20 mm 가 본문·Fig. 4 의 15 mm 와 모순(조판 오식으로 보임), p.381 "solving Equation (2)" 는 Eq. (4) 여야 함. **본문 서술이 그림보다 관대한 곳 2건** (Fig. 8 패널 d 의 "negligible within the margin of error" — 그림의 LAM_PE ≈6.5% 는 5.4% margin 밖 / 패널 j 의 "correct amounts" — 그림은 둘 다 ~5.5–6%p 과소추정).
- 질문 카드 2건 갱신: [[22p-physics-or-degeneracy]] (Evidence For 2건 + Against 2건 + Status Log — status `active` 유지), [[pvs-sev-lli-lampe-separability]] (Gap 2건의 출처 확정 + "관측 추가 대신 **제약 추가**" 라는 셋째 경로 등재 — status `open` 유지).
- 후속 확인 항목 1건 열림: `degradation-degeneracy/docs/02_CODE_AUDIT.md`·`docs/04_PROMPTS.md` 의 `LLI = (1−α_PE) + (β_PE − β_NE)` 에 붙은 "Birkl 2017 부호 규약" 주석이 **이 논문 본문으로 확인되지 않는다** (본문에 α·β 창 파라미터가 없다). 읽기만 하고 고치지 않았다.
- 이 커밋은 `wiki/` 만 건드리므로 degradation-degeneracy 의 `source_digest` 를 바꾸지 않는다.

## [2026-09-03] ingest | Wang et al. 2025 — interpretable ML for battery prognosis (분야 리뷰)
- raw 1건 봉인: `raw/papers/wang2025_interpretable-ml-battery-prognosis.md` (*Adv. Energy Mater.* **2025**, **15**, **e03067**, doi:10.1002/aenm.202503067, 20쪽 REVIEW — **절별 해체분석**, `[인쇄]`/`[도표]`/`[해석]` 3구분). 그림 크로핑 9장(fig 8 + tab 1) → `raw/figures/wang2025_interpretable-ml-battery-prognosis/`; **fig 1~8 여덟 장을 전부 실제로 열어 보고** digest 를 썼다 (tab_1 은 PDF 텍스트가 정확하므로 이미지 판독 생략 — digest §12 에 명시).
- **서지 확인**: 2026-09-02 세미나 p.4 가 인용한 `Adv. Energy Mater., 2025, 15, e03067` 과 **일치** (권·article number·연도 모두). 같은 줄의 둘째 인용 `Joule, 2025, 9, 101884` 는 이 리뷰의 참고문헌 [113] (Rhyu et al.) 과 일치 — 세미나 p.4 의 두 인용은 "리뷰 + 그 리뷰가 인용하는 원전" 조합이다.
- 컴파일 1건: [[interpretable-ml-battery-prognosis-taxonomy]] (concept — 4분류, PVS·SEV 가 앉는 자리, 그리고 그 분류가 묻지 않는 것의 전수 확인표).
- **핵심 발견 셋**:
  1. **★ 이 리뷰는 우리 축의 어휘를 갖고 있지 않다.** 본문(참고문헌 제외) 전수 검색: `identifiab` `degenerat` `uncertain` `noise` `error bar` `confidence interval` `Bayesian` `cross-valid` `OCV` `half-cell` `post-mortem` 이 **각 0회**. `collinear` 는 1회(SHAP 한계), `highly correlated` 1회(PDP 한계), `ground truth` 1회(**feature importance** 에 대한 것) — 셋 다 **사후 해석 도구의 신뢰도** 문제이지 역문제의 적절성이 아니다. Fig. 4b 에 `Parameter identification` 상자를 실으면서 `identifiability` 는 한 번도 쓰지 않는다. (검색 시 **합자 정규화 필수** — `ﬁ` 때문에 정규화 없이는 `identifiab`/`confiden`/`overfit` 이 전부 0 으로 잘못 나온다. 첫 시도에서 실제로 그랬다.)
  2. **전극 수준(LLI/LAM)을 예측 target 으로 삼는 사례가 하나도 없다.** Fig. 1 의 conventional/interpretable 두 패널 모두 Targets = `SOH, RUL, SOC…` 로 동일하다 — 이 리뷰가 말하는 해석 가능성은 **출력을 바꾸는 것이 아니라 경로를 투명하게 하는 것**이다. LLI/LAM 은 본문 6회 등장하며 전부 feature 의 사후 물리 설명이고, 유일한 예외가 Navidi et al. 2024 의 손실함수("true values of … lithium inventory") 인데 그 참값의 출처를 리뷰가 적지 않는다.
  3. **PVS 의 문헌적 선례와 물리 귀속 충돌.** Fig. 5c 를 직접 보면 Kim et al. 2023 의 "DV peak intensity" 는 실제로 **peak−valley 진폭**이며(캡션만으로는 알 수 없다), 그 물리 귀속이 **흑연 음극 단일**(리튬 삽입 불균일성)이다. 세미나의 PVS 는 같은 형태의 양을 양극 peak vs 음극 valley 의 **대비**로 읽는다 — 같은 기하량에 두 개의 다른 물리 이야기.
- 원문 결함 기록: **Fig. 3c 캡션의 상관계수 `−0.93` 과 재수록 그림 안의 `ρ = −0.92` 가 불일치** (400 dpi 재확대로 확인 — 이 리뷰를 인용해 숫자를 옮길 때 걸리는 유일한 함정). 그 외 캡션/그림 표기 불일치 5건과 조판 오식 다수(`intrisic`, `Impedence`, `Opportunies`, `Onset temperatrue`, `Differential Volatge`, `LPR`↔`LRP` 혼용, p.8 문장 중복, 참고문헌 [170] DOI 절단)를 digest §12·§13 에 기록.
- 질문 카드 1건 갱신: [[pvs-sev-lli-lampe-separability]] — Evidence For 1건(SEV 축: "LLI 와 LAM 이 **함께** R_ct 를 올린다" 는 DRT 관찰), Gap 2건(PVS 물리 귀속 충돌 / 라벨 불확실성 공백이 **ML 분야 리뷰에도** 있다는 전수 확인), Status Log 에 "이 리뷰가 다루지 **않는** 것" 명시. status `open` 유지 — 이 리뷰는 답이 아니라 **좌표계와 공백**을 준다.
- [[pvs-sev-degradation-mode-features]] 에 "문헌에서의 자리" 절 추가 (PVS = §4.2 IC/DV 계열의 변형, SEV = 분류상 새 자리, ΔE/η 분해가 선행 프레임).
- **다음 흡수 후보 5편** 을 digest §14 에 우선순위와 이유 한 줄로 고정 (Navidi 2024 · Kim 2023 · Tao 2025 · Rhyu 2025 · Su 2024).
- 이 커밋은 `wiki/` 만 건드리므로 degradation-degeneracy 의 `source_digest` 를 바꾸지 않는다 (진행 중인 57차 게이트 P0-1 작업과 무관 — `git add wiki/` 만 했다).

## [2026-09-03] ingest | Dubarry 2012 "Synthesize battery degradation modes" (JPS 219:204–216)
- raw: `raw/papers/dubarry2012_synthesize-degradation-modes.md` (절별 해체분석, 16절). 크로핑 15장 중 **8장을 직접 봄** (Fig. 1,4,6,7,11,13,14,17); Fig. 3·12 는 크로핑 실패, 나머지 5장 미열람 — digest §16 에 명시.
- 신규 개념: [[dubarry-mechanistic-mode-synthesis]] — **판정 (c) 부분적으로 맞다**. α·β 창 좌표계 `(LR, OFS)`·LAM↔scaling 식 (5)·li/de 4분류는 **여기가 출처**(Birkl 이 [19] 로 물려받음). 그러나 `LLI = (1−α_PE)+(β_PE−β_NE)` 는 **두 원전 어디에도 없고** Dubarry 식 (8') 과 부호·전극·연산이 어긋난다.
- [[birkl-ocv-degradation-diagnostic]]: "계보" 절 신설, li/de 용어 출처 정정, "인용 확인" 항목 **종결**, evidenceScope → multi-source-primary.
- [[22p-physics-or-degeneracy]]: status log 추가 (status `active` 유지). 식별 가능성 어휘 전수 0회 확인 + **축퇴가 식 (5)+(8') 로 해석적으로 예측된다**(`{LAM_liNE=x} ≡ {LAM_deNE=x, LLI=LR·x}`) + 자유도 계보 2→3→4.
- [[degradation-degeneracy]]: "선행 연구 인정" 절 추가 — 정방향 합성은 Dubarry 2012 가 13년 앞선다. 우리 기여는 역방향 판정·격자·noise 층.

## [2026-09-03] ingest | Kim et al. 2023 — DV peak intensity 로 흑연 불균일성·수명 예측 (ACS Energy Lett. 8, 2946)
- raw/papers/kim2023_graphite-heterogeneity-lifetime.md (본문 8쪽 + SI 24쪽, DOI 10.1021/acsenergylett.3c00695). 크로핑 24장 중 **10장을 실제로 Read**.
- **판정 (이번 흡수의 목적)**: 리뷰가 PVS 의 선례로 든 "DV peak intensity" 는 **peak−valley 진폭이 아니라 ridge 의 절대 높이**다 (SI 인쇄: "the absolute value at the ridge"). 진폭 변형(ΔPeak_S2)은 valley 노이즈 때문에 폐기됐다 (ρ 0.75 → 0.82). 셀은 **LFP‖Gr**(2상 평탄 OCP) 이라 음극 단일 귀속이 화학에 의해 강제된다. `dQ/dV = 1/(dV/dQ)` 로 좌표를 맞추면 그 descriptor 는 세미나의 **Valley2**(음극)에 대응해 **오히려 일치**한다.
- 컴파일: [[dv-peak-heterogeneity-descriptor]] 신설 · [[pvs-sev-degradation-mode-features]] "문헌에서의 자리" 정정 · [[pvs-sev-lli-lampe-separability]] Gap 1건 닫고 2건 신설 (DV 진폭이 모드 이외 상태변수를 싣는다 / valley 노이즈 취약성의 문헌 전례).
- 물리 귀속의 근거는 half-cell·시뮬레이션이 아니라 선행문헌(Lewerenz/Sauer 2017) + 기구론 도식 + n=2 XRM + 조건 경향이다. 식별 가능성·불확실성 어휘는 본문·SI 통틀어 0회 (이 계보 네 편 연속).

## [2026-09-03] ingest | Su et al. 2024 — DRT 유래 health feature 와 GPR SOH 추정 (J. Energy Storage 90, 111770)
- raw/papers/su2024_drt-soh-health-features.md (DOI 10.1016/j.est.2024.111770). 크로핑 12장.
- **판정 ① (리뷰 §4.4 의 "LLI 와 LAM 이 함께 R_ct 를 올린다" 검증)**: 그 문장은 **Su 의 관찰이 아니다**. 원문 `[인쇄, p.6]` 은 "These trends are **in line with the fact that** … **[20]**" 이고 [20] = Jiang et al., *Appl. Energy* 322 (2022) 119502 — **상속된 인용**이다. 게다가 (a) Su 는 LLI 도 LAM 도 **한 번도 재지 않는다** (두 약어 4회, 전부 수치 없는 서술; half-cell OCP fitting·ICA/DVA·해체분석 전무), (b) Su 가 "charge transfer" 로 이름 붙인 p₂ 는 5셀 중 **4셀에서 노화와 함께 감소**한다 (Fig. 5·7) — **원전 안에서 어긋난다**. 리뷰는 증거 등급을 한 단계 올려 옮겼다(상속된 해석 → 저자의 관찰).
- **컴파일**: [[interpretable-ml-battery-prognosis-taxonomy]] 에 "이 리뷰의 요약에 붙는 정정" 절 신설 (raw 는 불변층이므로 정정은 컴파일 페이지가 보유). [[pvs-sev-lli-lampe-separability]] 의 H1 반대 근거 항목 **철회** — SEV 설계에 불리하다던 문헌 근거가 원전에서 성립하지 않는다.
- **판정 ② (우리가 쓰는 EIS 데이터의 출처)**: **재사용이다.** Su 원문 Data availability `[인쇄]`: "We used an **open dataset** at doi:…/zenodo.3633835, reference number [32]." 원 출처는 **Zhang et al., Nat. Commun. 11 (2020)**, DOI 10.1038/s41467-020-15235-7 / Zenodo 10.5281/zenodo.3633835. `mode-observability/manifests/README.md` 의 출처 유보 **해제**, 1차 인용을 Zhang 2020 으로 전환.
- 신규 개념: [[zhang2020-eis-aging-dataset]] — 그 데이터셋의 좌표계. **`state I~IX` 는 열화 단계가 아니라 한 충방전 사이클 안의 아홉 측정 시점**이고 열화 축은 파일 안의 `cycle number` 열이다 (두 축 직교). 따라서 (a) state 고정 → cycle 스윕 = 노화 추적(Su 가 한 것, state V 하나) 과 (b) cycle 고정 → state 스윕 = **SOC 의존성 추적(아무도 안 했다)** 이 갈린다. SEV 가 R_ct 의 stoichiometry 의존성을 읽는 feature 이므로 (b) 가 SEV 의 실측 대응물에 가깝다.
- **경계**: 이 데이터셋에는 LLI/LAM 라벨이 **없다**. "SEV 가 모드를 가르는가" 는 이것으로 못 묻고 "SEV 축이 셀 간에 재현되는가" 만 물을 수 있다 — 그 구분을 흐리지 않는다.

## [2026-09-03] ingest | Rhyu et al. 2025 — 형성 데이터로 cycle life 예측하는 체계적 feature 설계 (Joule 9, 101884)
- raw 1건 봉인: `raw/papers/rhyu2025_systematic-feature-design-formation.md` (본문 15쪽 + SI 19쪽, DOI 10.1016/j.joule.2025.101884). **절별 해체분석 + `[인쇄]`/`[도표]`/`[해석]` 3구분**. 함께 올라온 `mmc2.pdf`(34쪽)는 열어서 **본문 15쪽 + SI 19쪽의 재수록본**임을 확인하고 무시했다 (digest §0 에 기록).
- 그림 크로핑 23장(그림 15 + 표 8) → `raw/figures/rhyu2025_systematic-feature-design-formation/`. 캡션 오탐 방지로 제외된 **Figure 2·6 은 해당 쪽 전체를 170 dpi 로 따로 렌더**해 확보(`fig_2_fullpage-p5.png`, `fig_6_fullpage-p11.png`). **11장을 실제로 Read** 했고 무엇을 안 봤는지 digest §15 에 명시. 표 이미지 8장은 PDF 텍스트가 정확하므로 판독 생략.
- **우선 질문 ① "systematic feature design 이 정확히 무엇인가" → 데이터 우선 파이프라인이고 물리는 두 지점에서만 들어온다.** 앞에서는 **후보를 지우는 가위**(입력 후보 6종으로 축소), 뒤에서는 **사후 설명**(반응입자 앙상블 모형). feature 의 **형태를 만드는 것은 선형대수**다 — β 가 구간 안에서 평평 → Q̃(V) 직선근사 → `[인쇄]` "only two features are needed to describe each section: Q^B(V₂)−Q^B(V₁) and mean(Q^B(V₁–V₂))". 저자들이 대체 대상으로 지목하는 것이 `[인쇄]` "**handcrafted features** that are limited by the many unknown aspects of the underlying physics" 이므로, **PVS·SEV 는 이 프레임의 선례가 아니라 대척점**이다 — 절차 안에 유도 스칼라를 넣을 문이 없다 (근거 등급 B).
- **우선 질문 ② 어휘 전수 → "연속 0회" 는 형식상 깨지지만 결정적으로 약하게 깨진다.** 합자 정규화 후 본문 15쪽 + SI 19쪽: `degenerac*` **0** · `uncertain*` **0** · `identifiab*` **1** — 그 1회는 **참고문헌 [30] 의 제목 안**(Lin & Khoo 2024, "Identifiability study … degradation mode sensitivity …")이고 본문에서 그 문헌은 **DVF 기법 4연속 인용의 넷째**로만 쓰인다. `nullspace` 1회도 참고문헌 [13] 제목 안이며, 그것은 **저자 그룹 자신의 논문**(공저자 4명 겹침)인데 "β 는 해석을 준다" 는 **긍정 근거로만** 인용된다. 가장 UQ 에 가까운 것은 `error bar` 2회 — 그러나 그것은 **형제 셀 2~3개 예측값의 min–max 폭**이고, 저자들은 그것을 `[인쇄]` "may not be **trustworthy**" 의 신호로 쓴다 (이 계보 최초의 신뢰도 문제의식).
- **우선 질문 ③ feature ↔ 예측 대상 → 두 과제가 같은 feature 를 쓸 수 있다는 근거는 원문에 없고, 원문 안에 반대 증거가 있다.** `LLI`·`LAM` 약어 **0회**, `degradation mode` 2회는 둘 다 참고문헌 제목 안. 대신 SI Note S11 이 **4-파라미터 전극 이용상태**(β_c, β_a, Q_rem, V_shift)를 실제로 적합하고 Table S9 에 점추정을 싣는다 — 우리 축과 좌표가 대응하는데 **오차 막대 0**, 그런데 `[인쇄]` "the effective capacity lost at each electrode is **greater than** the lithium inventory lost" 라는 물리 결론을 뽑는다. 그리고 결정적으로: 느린 형성 32셀에서 형성 후 C/20 RPT 신호가 `[인쇄]` "**nearly indistinguishable**" 인데 cycle life 는 다르다 → **그 데이터에서 수명을 예측하는 정보는 열역학적 모드 좌표 밖**(저자 귀속: 미시 입자 저항 불균일성 = 동역학)에 있다.
- **데이터 포털 (요청 항목) → zip 파일 이름·내용은 원문 미제시.** `Data and code availability` 전문은 raw §11 에 그대로. 문자열 `zip`·`Framework_Formation`·`tsfresh_autoML`·`fulllist`·`GitHub`·`repository` 가 본문+SI 통틀어 **각 0회**. 원문이 말하는 것은 역할 구분뿐이다 — **data.matr.io/8/ = 원시 데이터(Cui et al. 2024 이 생성)**, **Zenodo 10.5281/zenodo.14916092 = 코드 + 가공 데이터**. 파일명 어의로 추정하는 것은 논문 인용이 아니라 데이터셋 관찰 등급으로 다뤄야 한다고 명시했다.
- 컴파일 1건: [[fused-lasso-feature-design-framework]] (concept — 7단계 절차표, 물리가 들어오는 두 지점, agnostic 기준선 패턴, 이 프레임이 말하지 않는 것).
- **★ 이 계보에서 검증 설계가 가장 엄격한 논문이다** — group = 형성 프로토콜 · feature 설계가 outer training set **안에서** 일어남 · feature 설계용 inner 분할과 하이퍼파라미터용 inner 분할을 `[인쇄]` "**intentionally differentiated** … to avoid information leakage" · 선행 연구(Weng 2021)의 leakage 를 **각주 49 로 못 박음**. 그리고 프로토콜 파라미터만 쓰는 **agnostic 기준선 52개**를 별도로 세워 물리 feature 가 그것을 이기는지로 판정한다 — 우리가 이 계보에서 반복 지적해 온 "프로토콜 식별자가 입력에 섞였는가" 를 저자들이 먼저 분리해 놓았다.
- 질문 카드 2건 갱신: [[pvs-sev-lli-lampe-separability]] (Evidence Against 1건 + Gap 3건 + Status Log — status `open` 유지), [[22p-physics-or-degeneracy]] (Status Log — status `active` 유지, 22p 수치에 직접 닿는 근거는 **없다**고 명시). 개념 2건 갱신: [[interpretable-ml-battery-prognosis-taxonomy]] (**정정 2** 신설 — 리뷰의 "dQ/dV·d²Q/dV² feature 자동 생성 / MAPE 9.2%" 는 둘 다 부정확하다: 설계 feature 는 **용량 차분**이고 원문은 미분용량 곡선과의 직접 대응을 **부정**하며, 9.2 는 5 fold **중앙값**이고 대표값은 9.87/9.84, **최악 fold 11.93 은 세 접근 중 가장 나쁘다**), [[pvs-sev-degradation-mode-features]] ("문헌에서의 자리" 에 대척점 항목 추가).
- 원문 결함 기록 (digest §13): 초록 **9.87%** vs Table 6 mean **9.84** 불일치(근거 미제시) · SI Fig. S12 캡션의 "Table 6" 은 **Table 4** 여야 함 · Table 6 각주 a/b/c 가 표 대신 본문 참고문헌 49/62/74 의 내용 · `robustness` 가 두 뜻으로 쓰임 · Fig. S4 에 범주가 다른 "Designed (best)" 가 섞여 있음.
- **본문이 그림보다 관대한 곳 2건**: (i) "robustness of β" 서술 vs **SI Fig. S5e 의 fold 간 부호 뒤집힘**(3.45–3.60 V 에서 β^(2) ≈ −0.70 vs β^(5) ≈ +0.37, 직접 봄 — 하필 설계 feature 가 사는 구간이다), (ii) Highlights 3번의 단정적 어조 vs Fig. 6 의 진폭 불일치(실측 ±30 vs 시뮬 ±60 스케일).
- 다음 흡수 최우선 후보 확정: **Lin, J. & Khoo, E. (2024), *J. Power Sources* 605, 234446** — 이 계보에서 제목에 identifiability 가 있는 유일한 문헌.
- 이 커밋은 `wiki/` 만 건드리므로 degradation-degeneracy 의 `source_digest` 를 바꾸지 않는다 (`git add wiki/` 만 했다 — webapp/ 과 degradation-degeneracy/ 는 손대지 않았다).

## [2026-09-03] ingest | Zhang et al. 2020 — EIS + GPR 로 용량·RUL 예측 (Nat. Commun. 11:1706): 우리 EIS 데이터셋의 **원전**
- raw 1건 봉인: `raw/papers/zhang2020_eis-gpr-capacity-rul.md` (본문 6쪽 + SI 6쪽, DOI 10.1038/s41467-020-15235-7 / Zenodo 10.5281/zenodo.3633835). 서지는 사용자 추정대로 전부 맞았고 논문번호 **1706** 을 보탰다. `[인쇄]`/`[도표]`/`[코드]`/`[해석]` **4구분** (공개 저장소 파일에서 확인한 것을 `[코드]` 로 따로 뒀다).
- 그림 크로핑 8장(본문 4 + SI 4) → `raw/figures/zhang2020_eis-gpr-capacity-rul/`. **8장 전부 Read 로 실제로 봤다.** 자동 크롭이 "거의 백지" 로 오판해 제외한 **SI Table 1** 은 SI 6쪽을 200 dpi 로 직접 렌더해 읽고 digest §2.4 에 전사.
- **★ 최우선 과제 — [[zhang2020-eis-aging-dataset]] 의 "미확인 항목" 6개 판정: 4 닫힘 / 1 부분 닫힘 / 1 원문 미제시.** ① 셀 형태 **닫힘** = `[인쇄]` "12 commercially available 45 mAh **Eunicell LR2032** Li-ion **coin cells**" (우리 추정 LIR2032 급, 규격까지 맞음). ② 셀 목록 **닫힘** = Su 의 12셀 열거가 맞다 (Methods `[인쇄]` + SI Fig. 4 범례 `[도표]` 로 교차확인, "온도별 01–08" 가설 폐기). ③ 파일 수 176 **원문 미제시** — 논문은 Zenodo 파일 구성을 한 글자도 적지 않는다. 다만 설계상 정본 개수 **108 EIS + 12 capacity = 120** 과 "한 파일 = 한 (셀,state)" 구조는 확정 → **56파일이 설계 밖**. Zenodo·doi.org 는 이번 세션 egress proxy 가 **403 으로 차단**(미해결). ④ `EIS_state_VI_25C42.txt` **부분 닫힘** — **셀 42 는 이 연구에 존재하지 않는다**(명부가 두 곳에서 exhaustive). 조치: 13번째 셀로 취급하지 않고 **격리**. ⑤ 프로토콜 **닫힘** = `[인쇄]` **1C(45 mA) CC–CV 4.2 V / 2C(90 mA) CC 3.0 V**, EIS 짝수·용량 홀수 사이클, 전 셀 25 °C 30사이클 선행, EoL = 그 후 80 %. ⑥ `state I~IX` **아홉 개 전부 닫힘** (SI Fig. 1 캡션 `[인쇄]`).
- **★ ⑥ 이 Phase 2 설계를 바꾼다**: SI Fig. 1 의 적·녹 점이 **DC 전류 유무**까지 준다 — **II·III·VI·VII 은 전류가 흐르는 중에 측정**된다. 따라서 평형 임피던스로 쓸 수 있는 SOC 는 **0 %(I·VIII·IX) 와 100 %(IV·V) 두 점뿐**이고 중간 SOC(III ≈40 %, VII ≈57 %)는 DC 바이어스 상태다. **"state I~IX 스윕 = SOC 곡선" 이라는 우리 읽기는 절반만 맞았다** → Phase 2 는 **양 끝점 2점 대비**로 축소. 대신 `IV vs V`·`VIII vs IX` = **같은 SOC, 휴지 전/후** 라는 **완화 시간 대비** 축이 새로 보인다 (아무도 안 썼다).
- **정정 1건**: 이전 항목의 "(b) cycle 고정 → state 스윕 = **아무도 안 했다**" 는 **틀렸다**. Zhang 은 state 축을 **복제 축**으로 썼다 — SI Fig. 2 가 **state 마다 독립 GPR 아홉 개**의 R² 를 싣는다 (V **0.88** · VII 0.86 · IX 0.81 · VIII 0.68 · II 0.66 · I 0.61 · IV 0.60 · III 0.53 · **VI 0.28**). 여전히 미개척인 것은 **state 간 대비를 feature 로 쓰는 것**. 부수 소득: **state VI 는 쓰지 않는다**는 공짜 사전정보.
- **판정 (②의 축)**: 이 논문은 **모드 식별 논문이 아니다.** 라벨은 **용량(측정)** 과 **RUL(= EoL − cycle)** 둘뿐이고 `LLI`·`LAM`·`lithium inventory`·`half-cell` 이 본문·SI 에 **각 0회**, 모드를 재는 절차가 전무하며 Introduction 이 미시 기구 모델링을 `[인쇄]` "unscalable" 하다며 명시적으로 포기한다. 제목의 "degradation **patterns**" 는 본문 용례 2회(제목 + Discussion)로 보아 **셀마다 다른 감쇠 궤적**이다. → **"이 데이터셋에 LLI/LAM 라벨이 없다" 가 원전에서 확정됐다.**
- **어휘 전수 (이 계보 여덟 편째)**: `degenerac*` **0** · `identifiab*` **0** · `uncertaint*` **1**(식 (3) 뒤 "a measure of uncertainty") · `calibrat*` **0** · `cross-valid*` **0**. 다만 **`non-unique` 1회** — `[인쇄]` "the fit is often non-unique" 는 **등가회로 fitting(경쟁 방법)** 을 향하며 그것을 **자기 방법의 정당화**로 쓴다. 심사자는 `[인쇄]` **Richard Braatz**.
- **★ 저자들의 공개 코드를 실제로 clone 해 확인** (`github.com/YunweiZhang/ML-identify-battery-degradation`, MATLAB 3 스크립트 + GPML + 가공 행렬; **전처리 코드는 없다**). 코드가 준 것 넷: (a) 입력 120 = **60 주파수 × (실,허)** 확정(`log(ones(121,1))`) → 본문 Fig. 1c 캡션의 "120 **frequencies**" 는 오기, (b) 주파수 격자 역산으로 **예측자 91 = Im Z(17.80 Hz), 100 = Im Z(2.16 Hz)** 확정, (c) ARD 가중치 코드가 논문 식 `exp(−σm)` 이 아니라 `exp(−10^log ℓ)` → 순위는 같지만 **"나머지 119개가 정확히 0" 은 변환이 만든 인상**, (d) **md5 로 확인**: `EIS_data_35.txt` ≡ `EIS_data_35C02.txt` (바이트 동일) — `Readme.txt` 대로면 **Fig. 3(c) 의 ARD 는 시험 셀 35C02 한 셀에 in-sample 적합**된다. 다온도 용량 모델은 ARD 가 아니라 `covSEiso` 다 (본문 서술과 불일치).
- **★ 새 Gap (SEV 축에 직접 걸린다)**: 저자들의 공개 데이터로 우리가 직접 계산 — 120 예측자 중 **52개**가 단독으로 |r(용량)| > 0.95 이고 91번↔92번 상관이 **0.998**, |r| > 0.99 인 5개(Im Z at 22.5/17.8/14.1/11.1/8.8 Hz)의 |r| 은 0.9920~0.9941. **ARD 가 고른 것은 주파수가 아니라 공선 대역**이며 그 안의 선택은 데이터가 정하지 않는다 → [[fitting-degeneracy]] 의 EIS 판. 논문은 17.80 Hz 에 물리적 의미(계면 물성)를 부여한다.
- **불확실성**: 이 계보에서 **처음으로 예측 구간을 그린 논문**(GPR 사후분산 ±1 s.d., Fig. 1a·2·3a,b·4). 그러나 그것은 **가정 관측잡음 + 커널 함수 불확실성**일 뿐 라벨·셀 간 변동이 아니고 **보정 검사가 없다** — `[도표]` Fig. 3a/3b 에서 측정 곡선이 음영 **밖에 연속 100 사이클 이상**(계통 편의). 교훈: **구간을 그리면 coverage 도 같이 보고한다.**
- **인용 금지 표시**: SI Table 1 의 기준선 비교(방전곡선 feature)는 **쓰지 않는다** — 25C08 의 RUL 범위가 0–38 인데 기준선 RMSE 가 **73.20**(범위의 1.9배)이고 feature 목록이 인쇄되지 않아 재현 불가. 망가진 기준선이다.
- 그 밖의 원문 결함 (digest §3): 본문 "results at other states are **similarly positive**" vs SI Fig. 2 의 R² 0.28~0.86 · SI Fig. 2 캡션은 "**25C02**"(훈련 셀)인데 본문 흐름은 25C05 · Fig. 1c 캡션의 "120 frequencies" · SI Fig. 4 y축 단위 `mA/h` · `[도표]` **고온 셀이 더 오래 살고 초기용량도 높다**(45 °C 40.5–42 mAh vs 25 °C 34–36 mAh)는데 논문이 언급하지 않는다(온도 ↔ 배치 교락) · 25 °C 코인셀 8개의 EoL 이 **12~234 사이클, 20배**로 흩어진다.
- 컴파일: [[zhang2020-eis-aging-dataset]] 대폭 갱신 (좌표계를 Su 전언 → **원전 인쇄** 로 교체, state 9개 표 신설, 미확인 6항목에 **닫힘 표시 + 근거**, confidence medium → **high** + verified, 반대해석 1줄 기록). [[pvs-sev-lli-lampe-separability]] Gap 2건 + Status Log (8) 추가 (status `open` 유지). `mode-observability/` 의 README·manifests 도 같은 판정으로 갱신.
- **이 세션은 git 명령을 하나도 실행하지 않았다** (게이트 증거 재생 중 — HEAD 이동 금지). 파일만 만들어 두었고 커밋은 사용자가 한다.

## [2026-09-03] ingest | Tao et al. 2025 — 비파괴 열화 패턴 decoupling 과 조기 궤적 예측 (Energy Environ. Sci. 18, 1544)
- raw 1건 봉인: `raw/papers/tao2025_nondestructive-degradation-decoupling.md` (본문 16쪽 + SI 75쪽, DOI 10.1039/d4ee03839h, EES 18호 **표지 논문**). `[인쇄]`/`[도표]`/`[코드]`/`[데이터]`/`[해석]` **5구분** (저자 공개 저장소에서 확인한 것과 그 데이터로 우리가 계산한 것을 따로 뒀다).
- 그림 크로핑 22장(fig 20 + tab 2) → `raw/figures/tao2025_nondestructive-degradation-decoupling/`. **7장을 실제로 Read** 했고 안 본 13장을 digest §14 에 명시. 자동 추출기가 캡션을 놓친 **본문 Fig. 4** 는 p.8 이미지 bbox 를 직접 잘라 `fig_4.png` 로 넣고 `figures.json` 에 `note` 를 달았다.
- **★ 최우선 질문 ① "이 논문의 decoupling 이 우리 모드 분리와 같은 것인가" → 다르다. 우리 문제가 이 논문의 한 칸 안에 통째로 들어 있다.** 미지수가 **2개**(열역학 ΔE / 동역학 η)이고, 논문 자신의 Fig. 5b 가 **LAM 과 LLI 두 상자를 한 화살표로 묶어** "Thermodynamics ΔE" 로 보내며 그 옆에 굵은 글씨로 `[인쇄]` **"Hard to decouple"** 을 인쇄한다. Fig. 5e 범례는 `[인쇄]` "Thermodynamic loss (**LAM&LLI**)", SI Fig. 25 캡션은 `[인쇄]` "Thermodynamic loss can be related to … **LAM at the cathode, LAM at the anode, and loss of lithium inventory (LLI)**". 즉 **LLI·LAM_PE·LAM_NE 가 전부 ΔE 안**이고, 가르는 수단은 곡선 형상이 아니라 **인가 전류 크기**(0.33C 두 단 vs 1.4–3C 일곱 단)다. 신규 개념 [[thermo-kinetic-loss-partition]] 에 좌표계를 고정했다.
- **★ 최우선 질문 ② "physics-informed 가 어디에 들어가는가" → 손실항에는 0, feature 선정·구조·사후해석에만.** 손실은 MSE + L1 뿐이고 물리 항이 하나도 없다 (PINN 이 아니다). 구조 쪽 물리는 Arrhenius AT score 인데 `[인쇄]` "**Since the dominating aging mechanism is unknown (characterized by E_a) as a posterior, we alternatively determine the aging rate by calculating the first derivative** …" — **논문 스스로 식 (6)의 Arrhenius 를 식 (7)–(8)에서 폐기**하고 초기 사이클 기울기 비로 대체한다. `[코드]` 공개 코드는 더 멀리 갔다: 구현된 AT 는 **기울기의 로그들의 비**(`np.log(abs(grad/rang))` 의 나눗셈)이고, 온도는 **하드코딩된 전압 척도 상수 10개**(예 T35: −12.97, −11.08, …)로만 들어온다.
- **★ 최우선 질문 ③ "identifiability/degeneracy 를 말하는가" → 어휘는 0회, 그러나 개념은 한 번 인정하고 넘어간다.** 본문 16쪽 + SI 75쪽 전수: `identifiab*` **0** · `degenerac*` **0** · `ill-posed` **0** · `non-unique`/`uniqueness` **0** · `cross-valid*` **0** · `error bar`/`confidence interval` **0** · `collinear*` **0** · `half-cell` **0**. 그런데 `[인쇄]` "fully separating the degradation … remains complex due to the dynamic interactions among degradation mechanisms" · "**The challenge of distinctly identifying these mechanisms persists, even with advanced diagnostics**" 라고 적은 **뒤에** 제목에 "decoupling" 을 쓴다. 여덟 편의 "어휘가 없다" 와 다른 **아홉 편째의 새 형태 — 어휘 없이 개념을 인정하고 넘어간다.**
- **★ 저장소 대조 감사 (사용자 요청) — 데이터는 맞고 코드는 여러 곳이 어긋난다.**
  - **데이터 저장소는 대체로 일치**: 32셀 9/9/7/7 (시트 이름으로 확인) · feature 52열의 이름·순서가 SI Note 2 ID 순서와 정확히 일치 · 9단 프로토콜 표 일치 · `[데이터]` EOL80 수명 **481–1025, 평균 775.9, 표준편차 175.4** = 본문 "480–1025, 775 ± 175" 와 일치 · 종료 SOH 0.589–0.731 = `[인쇄]` "from 73% to 59%" 와 일치.
  - **어긋나는 것 3건**: (a) SI Fig. 2e 의 전체 평균 **779** vs 본문 **775** vs 계산 **775.9** (SI 내부 불일치), (b) **Fig. 2g 의 25 °C EOL73 평균 1218 을 공개 라벨로 재현할 수 없다** — 25 °C 셀 9개 중 **B8T25 가 EOL73 문턱(0.803 Ah)에 끝까지 도달하지 않는데**(마지막 0.8039) violin 에는 점이 9개다. 도달한 8개의 평균은 1197.5 이고 표준편차 61.0 은 그림의 60 과 맞는다 — **평균만 어긋난다**(외삽으로 보이나 설명 없음). 35/45/55 는 0.80 Ah 문턱으로 ±2 사이클 안에 재현된다. (c) 데이터 README 는 "Steps **2** to 14 repeated 3 times", Table S1 은 "Steps **3** to 14" — 1단 차이.
  - **코드 저장소 ↔ 논문 불일치 15건** (digest §10.2 표): Leaky ReLU 라 적고 `torch.relu` 사용 · 손실 L1 대상이 **잔차가 아니라 가중치** · "75/25 분할" 이라 적었지만 실제는 **35/45 °C 셀의 첫 200 사이클을 학습에 넣고 같은 셀의 나머지를 시험** (셀 단위 hold-out 아님) · epoch/lr 불일치 · **시험 손실로 best epoch 선택**(valid 셋이 학습셋 복사본) · AT 정의 불일치 · **다중 source 앙상블이 실제로는 55 °C 단일 source** (25 °C 항 `step1` 과 `w_at_25` 가 계산만 되고 미사용) · 예측에 **하드코딩 −0.03 Ah 오프셋** · MAPE 정답이 **평활된 `filter_cap`** · 35 °C 는 9셀 중 **7셀만 평가**(`battery_dict["T35"]` 항목 7개) · `MyNetwork3` 의 `super(MyNetwork1, self)` 버그 + 데이터로더 튜플 개수 불일치로 **공개 코드가 그대로는 실행 불가**(학습 csv·체크포인트도 미공개).
  - `[데이터]` **U1–U9 는 셀마다 전 사이클에 걸쳐 정확히 상수**(표준편차 ~1e-16). 즉 1단계 모델의 입력 `(T, U1…U9, cyc)` 에서 U 벡터는 **셀 식별자**로 기능하고, 3단계 궤적 모델 입력 53차원에는 **사이클 번호와 온도가 직접** 들어간다. `cyc` 는 온도군별 기록 길이(1299/1099/899)로 정규화된다.
- **★ 값싼 대조 기준선 (우리 계산, digest §10.4)**: 대상 셀 **자신의 사이클 100–200 용량에 직선을 맞춰 끝까지 외삽**한 전 궤적 MAPE = **35 °C 1.45 % · 45 °C 1.25 %**. 논문의 headline(다중 source + 조기 20 %)은 1.4 % · 0.6 %. **35 °C 에서는 3단 파이프라인이 자(ruler)와 동률이다.** 반대로 초조기(25 사이클) 영역에서는 자가 13–20 % 로 무너지고 논문 방법(1.27–2.52 %)이 확실히 이긴다 → **이 방법의 실질 가치는 초조기 영역에 있고, Fig. 4a/b 의 대표 수치는 그 가치를 보여 주는 자리가 아니다.** 논문은 단조 외삽 기준선을 두지 않는다 (LSTM 기준선은 Table S4 에서 MAPE **67.75–89.78 %** 로 발산).
- **봉인된 digest 에 대한 정오 1건** (raw 는 불변층이므로 정정은 여기가 보유): digest §6.2 표의 "Table S4 에서 MAPE **67 ~ 88 %**" 는 반올림이 부정확하다 — 정확한 범위는 **67.75 ~ 89.78 %** (Table S4 의 Model1 여섯 칸). 결론(발산한 기준선)은 바뀌지 않는다.
- **★ "열역학 79 % / 85 %" 의 정체**: SI Note 8 을 따라가면 79 % = `Σ|SAGE(Q1,Q9)| / Σ|SAGE(Q1..Q9)|`, 검증 기준으로 제시된 85 % = 같은 9개 feature 의 **1↔800 사이클 변화량 비**(`[인쇄]` "regarded as the truth by manipulating the raw data"). **같은 아홉 숫자에서 나온 두 요약**이므로 독립 검증이 아니다. 게다가 어느 쪽도 LLI·LAM·임피던스를 **측정한 값이 아니다**. `[도표]` Fig. 4h 에서 RL 계열 SAGE 가 **음수**인데 배분식은 절댓값을 쓴다.
- **★ FEA 의 인과 방향**: `[인쇄]` SI Note 7 "**according to insights gained from machine learning** … **By adjusting the stoichiometric coefficient of LLI** … **we achieve control of the proportion of thermodynamic and kinetic loss** … thus aligning with the insights derived from machine learning." → **시뮬레이션은 ML 결과를 검증한 것이 아니라 그것에 맞춘 것이다.** 따라서 열역학 85 % 를 뒷받침하는 독립 측정은 이 논문에 없다.
- 원문 내부 불일치 (digest §11): **초록의 headline 95.1 % 정확도(= MAPE 4.9 %)를 본문이 근거로 지목한 Table S4 에서 재현할 수 없다** — 같은 설정 값 평균은 **1.91 %** 다 (인용 시 95.1 % 를 쓰지 않는다) · model 2(No-IMV)를 "온도를 고려하지 않는 모델" 이라 쓰고(그것은 model 3) 같은 문단에서 후기 MAPE 를 5.82 %/5.62 % 로 두 번 다르게 인쇄 · EOL 정의가 **EOL80/EOL73/EOL75 세 개** · SI Note 3 은 SOC 고정으로 feature 를 정의하는데 Table S1 은 전압 cut-off 고정 운전 · Fig. 5f 축 이름이 "correlation" 인데 Methods 정의는 **2차 Wasserstein 거리** · SI Fig. 26–28 캡션의 상호 참조가 Fig. S25 → S24 로 하나씩 밀림.
- 컴파일 1건: [[thermo-kinetic-loss-partition]] (concept — ΔE/η 정의, 우리 3모드 좌표와의 대조표, 관측 채널로서의 가능성, 이 분해를 쓸 때의 함정 4가지). [[fitting-degeneracy]] 에 "인접하지만 다른 분해" 절 추가 (혼동 방지 역링크).
- 질문 카드 2건 갱신: [[pvs-sev-lli-lampe-separability]] (**후보 관측 1건 추가 — 전류 축** + Status Log (9), status `open` 유지, Evidence 는 아님을 명시), [[22p-physics-or-degeneracy]] (Status Log (9) — **직접 닿는 근거 없음**과 그 이유 3가지를 명시, status `active` 유지).
- **이 세션은 git 명령을 하나도 실행하지 않았다** (사용자 지시). 파일만 만들어 두었고 커밋은 사용자가 한다. 변경은 전부 `wiki/` 안이므로 degradation-degeneracy 의 `source_digest` 를 바꾸지 않는다.

## [2026-09-03] ingest | Lin & Khoo 2024 — Identifiability study of Li-ion capacity fade using degradation mode sensitivity (J. Power Sources 605, 234446)
- raw 1건 봉인: `raw/papers/lin2024_ocv-degradation-mode-identifiability.md` (본문 18쪽, SI 없음, DOI 10.1016/j.jpowsour.2024.234446). `[인쇄]`/`[도표]`/`[해석]` 3구분.
- **이 위키가 직접 예약해 둔 문헌이다.** 2026-09-03 (7) 라운드에서 Rhyu 2025 의 참고문헌 [30] 제목 안에서 발견하고 "이 계보에서 제목에 identifiability 가 있는 **유일한** 문헌 · 우리 프로젝트의 정확한 선행 연구 · 다음 흡수 1순위" 로 못 박았던 그것 ([[22p-physics-or-degeneracy]] Status Log (4), [[pvs-sev-lli-lampe-separability]] Status Log (7)).
- 그림 크로핑 14장(fig 9 + tab 5) → `raw/figures/lin2024_ocv-degradation-mode-identifiability/`. **본문 그림 9장 전부를 실제로 Read** 했다 (표 5장은 PDF 텍스트가 정확해 이미지로 읽지 않음). 본문 서술과 어긋난 그림은 없다.
- **★ Q1 "identifiability 를 어떤 의미로 쓰는가" → 국소 + 실용. 도구는 Fisher 정보행렬(해석적 gradient 로 구성) → 역행렬 = Cramér–Rao 하한.** 프로파일 우도·Hessian·특이값·조건수는 **쓰지 않는다**(각 0회). 저자들이 세 곳에서 반복해 못 박는다: `[인쇄]` "any statements based on sensitivity gradients are **only valid locally**" · "To quantify **global identifiability** … Bayesian inversion **are needed**" · "we will report our findings in **future work**". **예외 하나** — §2.3 의 자유도 논증은 국소가 아니라 **구조적**이다.
- **★ Q2 "미지수가 몇 개인가" → 좌표에 따라 2 또는 3.** SOC 정규화 곡선 `U_OCV(z)` 의 **형상**은 `r_N/P = Q̂⁻/Q̂⁺` 와 `z₀⁺ = Q̂^Li/Q̂⁺` **단 둘**로 결정된다. Ah 축 `U_OCV(Q̂)` 는 `(Q̂^Li, Q̂⁻, Q̂⁺)` **셋**. 제목의 "minimally parametrized" 가 줄인 것은 **반쪽전지 OCP 가 아니라 둘을 붙이는 방식**이다 — Birkl 의 전극 SOC 한계 4개 + 컷오프 제약 2개, Mohtat 의 4개 + 제약 1개를 **제약 0개인 직선 하나(기울기·절편)** 로 대체한다. `[인쇄]` 비판: 제약된 매개화는 "non-independent parameters, of which the **redundancy** complicates their estimation". 그리고 **LLI/LAM 퍼센트로 매개화하지 말라고 명시**한다 (pristine 값에 의존해 "irrelevant to the current SOH and could be arbitrary").
- **★★ Q3 "degeneracy 를 발견했는가" → 어휘로는 0회. 실질은 두 종류를 모두 인쇄한다.**
  - **(a) 구조적 축퇴, 닫힌 형태**: `[인쇄, §2.3]` "a certain ratio LLI ∶ LAM⁻ ∶ LAM⁺ **does not correspond to a unique shape of OCV** … it is the ratio (1−LLI) ∶ (1−LAM⁻) ∶ (1−LAM⁺) … which will uniquely determine the OCV shape." → **정확한 null 방향**: `(1−LLI, 1−LAM_NE, 1−LAM_PE)` 를 공통 인자로 스케일하면 곡선 형상이 **불변**. 특히 pristine 에서 **`LLI = LAM_PE = LAM_NE = x` 는 곡선을 전혀 바꾸지 않는다**(총용량만 `1−x` 배). 지금까지 우리가 **수치로 찾던** flat 방향의 **해석해**이며 격자에 직접 심어 시험할 수 있다.
  - **(b) 국소 flat valley, 그림에만**: `[도표]` Fig. 2(b) LFP 의 MaxE·RMSE 지도에 **Li/P ≈ 1.0 을 따라 N/P 0.7→1.5 전 구간을 가로지르는 거의 흰 능선**이 있다 — N/P 를 두 배 넘게 바꿔도 전체 곡선이 사실상 같다. Fig. 5(b) 는 N/P 0.6~1.4 다섯 곡선이 육안으로 겹치고, Fig. 1(d) 는 `(N/P,Li/P)` 가 (1,1)/(1,1.2)/(1.4,1.2)/(0.7,0.8)/(1,0.8) 인 다섯 셀이 구별되지 않는다. **논문은 이것을 "sensitivity" 라고만 부른다.**
  - **갈리는 조건 (표는 digest §2 Q3)**: ① 화학이 지배 — `[인쇄]` LFP 60–100 mV vs NMC 200–400 mV 변동, "identifiability is **significantly higher for NMC than for LFP**", "the active material of **LFP tends to be hard to identify**". ② `(Li/P, Li/N)` 의 4-regime (Highlight 4). ③ SOC 창 — `[인쇄]` "estimating **𝑟_N/P is harder than 𝑧₀⁺**", "OCV values at **lower SOC** are overall more informative". ④ 노이즈는 **스윕하지 않는다** (σ_U = 5 mV 고정), C-rate·온도는 **변수가 아니다** (전류 없음, 25 °C).
  - `[도표]` **Fig. 9 (핵심)**: LFP regime Ⅲ(`r=0.7,z₀=0.8`)에서 `Q̂^Li` 와 `Q̂⁺` 는 **모든 SOC 창에서 오차 ≥ 100 mAh** (= 참값의 10 % 이상, 사실상 불가)이고 `Q̂⁻` 만 식별된다. 이상적 5 mV·완전 모델·국소 선형화라는 최상의 조건에서다. NMC 는 훨씬 낫다.
- **★ Q4 "truth 가 무엇인가" → 실측 0. 100 % 해석식 + Python 계산.** OCP 는 Plett 교재의 LFP·NMC111·MCMB 적합식(25 °C), 셀은 두 화학, 노이즈는 **가정만**(난수 실현 없음), **추정기를 한 번도 돌리지 않는다** (Fig. 8·9 는 참값에서 평가한 CRLB 이지 복원 결과가 아니다). 코드·데이터 미공개.
- **★ Q5 "충돌하는가" → 정면 충돌은 없다. 대신 이 논문이 우리 방법의 약점을 이름 붙여 지목한다.** `[인쇄, §3]` "A straightforward approach is to devise an estimator and calibrate the estimation error by feeding measurements coming from a known ground truth **[3,19]**. The drawback … it **entangles the identifiability intrinsic to the problem with the error incurred by the estimator itself**." — `[3]` 이 Birkl 2017 이고 우리 파이프라인이 그 계열이다. **다만 우리는 그 얽힘을 알고 설계했다** — flat valley ↔ multimodal 구분이 정확히 그것을 분해하려는 장치다. 그들은 **회피**했고 우리는 **분해**한다.
- **★ 어휘 전수 (이 계보 열 편째) — 연속 0회가 처음으로 깨졌다, 그러나 반쪽만.** 합자 정규화 후 본문 77,217자: `identifiab*` **26** · `sensitivit*` 46 · `Fisher` 12 · `error covariance` 4 · `local` 6(전부 한정) · `global` 2(둘 다 "안 했다"). 그런데 `degenerac*` **0** · `non-unique` **0** · `collinear*` **0** · `confound*` **0** · `ill-posed` **0** · `nullspace` **0** · `Hessian` **0** · `singular value` **0** · `condition number` **0** · `profile likelihood` **0** · **`noise` 0**(σ_U 를 "standard error" 로만 부른다) · `error bar` **0** · `cross-valid*` **0** · **파라미터 상관 언급 0**. `uniqu*` 4회 중 **부정형은 단 하나**이고 그것이 우리 축의 축퇴다. `[해석]` **추정 정밀도 어휘는 갖췄고 비유일성 어휘는 없다 — 개념을 절반만 자기 쪽으로 돌린다.**
- **★ 비판 (digest §15) — 가장 큰 것 셋**: (1) **오차공분산 `C_θ` 를 계산해 놓고 `sqrt(diag)` 만 그린다** (`[인쇄]` "the square root of **diag(𝑪_𝜽)**") — 축퇴의 **방향**(비대각·최소 고유벡터)을 손에 쥔 채 한 번도 표시하지 않는다. (2) **추정기를 안 돌린다** — CRLB 는 **불편 추정량**의 하한인데 저자 스스로 MLE 가 `[인쇄]` "not necessarily unbiased" 라 적고 "semi-heuristic" 으로 쓴다. (3) **네 평가점 중 셋을 논문 스스로 "비전형" 이라 부른다** (`[인쇄]` Li 과잉은 "a normal cell **rarely falls into this regime**", N/P<1 도 비전형) — 실제 노화 셀이 가는 regime Ⅳ 는 (d)/(h) 하나뿐인데 여덟 패널이 동등하게 나열된다. 부수: **Table 4 캡션의 "only identifiable" 이 본문 §2.7 에서는 "highly identifiable"** 로 완화돼 있다(같은 세 문장) — 캡션을 인용하면 과장이 전파된다. **그럼에도 이 논문은 이 계보 열 편 중 방법론적으로 가장 정직하다** (유효 범위를 세 곳에서 반복 명시).
- **★ 우리 저장소와의 접점 (읽기만 함, 아무것도 고치지 않음)**:
  - **좌표계가 일치한다.** Lin 식 (15) `LLI = 1 − Q̂^Li/Q̂^Li_ini`, `LAM± = 1 − Q̂±/Q̂±_ini` 는 `degradation-degeneracy/docs/07_LAM_LLI.md` 의 정의와 같은 형태다. 우리 격자가 `de` 전용이라 세 파라미터가 실제로 독립인 것도 Lin 의 전제와 맞는다.
  - **점검 B1 (새로 열림)**: 우리 목적함수의 x축이 `[코드 주석]` "각 셀 자기 용량" 정규화이므로 (`src/fitting.py` 헤더) pOCV 항은 Lin 의 `U_OCV(z)` 이고 **형상 자유도가 2개뿐**인데 우리는 **4개**(α_PE,β_PE,α_NE,β_NE)를 맞춘다. 재구성이 양 끝 컷오프를 근사적으로 맞추면 제약 2개가 소모돼 유효 자유도가 2로 떨어진다 — **Lin 이 Birkl/Mohtat 을 비판한 바로 그 구조**. 2026-09-03 (2) 에서 열어 둔 "우리 degeneracy 의 일부가 원전에 없는 자유도에서 온다" 가설의 **정확한 좌표**다. 사영: `z₀⁺ ↔ (β_NE−β_PE)/α_PE`, `r_N/P ↔ α_NE/α_PE`. **미검증.**
  - **점검 B2 (새로 열림)**: **dQ/dV 를 더해도 개선이 없었던 2026-08-20 결과가 구조적 필연일 수 있다.** dQ/dV 는 같은 정규화 곡선의 함수이므로 rank 를 늘릴 수 없고 국소 null 방향은 재가중에 불변이다. 값싸게 확인 가능. **미검증.**
  - **경험적 결론 하나가 해석식과 만났다**: `docs/07_LAM_LLI.md` 의 "**양극 활물질이 조금 줄어도 전체 용량은 거의 안 변하므로 LAM_PE는 full-cell 곡선에 흔적을 거의 남기지 않는다**" 는 Lin 식 (47) `∂Q̂max/∂Q̂⁺ = z⁺_max λ⁺_l − z⁺_min λ⁺_u` 의 `λ⁺_l → 0` 극한이다. **그리고 `λ⁺_l` 은 SOH 에 따라 움직인다** — "LAM_PE 가 안 보인다" 는 고정된 성질이 아니라 `(r_N/P, z₀⁺)` 위치에 따라 켜지고 꺼진다. 우리 격자 안에서 그 전환이 일어나는지 미확인.
  - **22p 삼중항의 좌표 환산**: 세미나 22p (LAM_PE≈LAM_NE≈13 %, LLI≈17 %) → `r_N/P/r_ini = **1.000**`, `z₀⁺/z₀,ini = **0.954**`. `[해석]` **세 숫자가 담은 곡선 형상 정보는 스칼라 하나이고 N/P 는 pristine 에서 한 발짝도 안 움직였다.** (우리 파이프라인 수치의 정본은 artifact + `docs/RESULTS*.md`. 여기서는 환산만.)
- **다음 흡수 후보 2건 확정**: `[11]` **Mohtat et al. 2019** (*J. Power Sources* 427, 101–111) · `[15]` **Lee et al. 2020** (*IEEE TII* 16(5), 3376). `[인쇄]` "They also derive the gradient … and **use Fisher information to quantify the parametric identifiability**" — 즉 **Fisher 를 이 문제에 처음 쓴 것은 Lin & Khoo 가 아니다.** 게다가 그 모델이 `[인쇄]` "**has been incorporated in PyBaMM**" 이라 우리 도구와 직접 닿는다.
- 컴파일 1건: [[np-lip-ocv-reparametrization]] (concept — `(N/P, Li/P)` 최소 매개화 · **2 자유도 정리와 닫힌 형태 null 방향** · 전극 DV fraction `λ±` · 네 regime 표와 그 표를 식별 가능성 지도로 오독하지 말라는 인용 주의). [[fitting-degeneracy]] 에 "닫힌 형태로 알려진 null 방향" 절 추가.
- 질문 카드 2건 갱신: [[22p-physics-or-degeneracy]] (**Evidence For 2건 추가** + Status Log (10), status `active` 유지), [[pvs-sev-lli-lampe-separability]] (**Evidence For 1건 + Evidence Against 1건 + 판정 절차 정정 + 새 Gap 1건** + Status Log (10), status `open` 유지). ★ 그 카드의 **전제 하나가 갈라졌다** — 2 자유도 정리의 따름정리상 **PVS 는 새 관측 채널이 아니라 같은 곡선의 재가중**이고, **SEV 만이 이 정리의 사정권 밖**(동역학)이다. 반대로 구조적으로 잃는 방향은 **LLI↔LAM_PE 가 아니라 세 모드 공통 스케일** 방향이므로, H1 이 참이라면 그 이유는 구조가 아니라 **조건수**다 — 논쟁 무대가 옮겨졌다.
- **이 세션은 git 명령을 하나도 실행하지 않았다** (사용자 지시). 파일만 만들어 두었고 커밋은 사용자가 한다. 변경은 전부 `wiki/` 안이므로 degradation-degeneracy 의 `source_digest` 를 바꾸지 않는다.

## [2026-09-03] ingest | Schaeffer et al. 2024 — 고차원 선형회귀의 nullspace 와 정칙화 (Comput. Chem. Eng. 180, 108471)
- 원문: 본문 9쪽 + SI 4쪽 + **저자 공개 저장소 `HDRegAnalytics`** (읽기 전용 참조, 이 저장소에 복사하지 않음). raw digest: `raw/papers/schaeffer2024_nullspace-regularization-interpretation.md` (sha256 봉인, 그림 11장 크로핑 후 **9장을 직접 열어 봄**).
- **흡수 이유**: 이 위키가 두 번 지목해 둔 문헌이다. (a) [[fused-lasso-feature-design-framework]] 의 참고문헌 `[13]` — "저자 그룹 자신의 nullspace 논문인데 본문에서 **긍정 근거로만** 인용된다" 고 2026-09-03 (7) 에 적어 두었다. (b) 직전 라운드([[np-lip-ocv-reparametrization]])의 결론이 "Lin 은 `C_θ` 를 손에 쥐고 **축퇴의 방향을 한 번도 그리지 않는다 — 그 그림이 우리가 공급할 것**" 이었고, 이 논문 제목에 `nullspace` 가 있다.
- **★ 다섯 질문에 대한 답 (요지)**:
  1. **무엇의 nullspace 인가** → `[인쇄]` "The data's nullspace contains all coefficients that satisfy **𝐗𝐰 = 𝟎**" — **설계행렬 `X`** 다. Fisher/Hessian 이 아니다. `[해석]` **그러나 이 모형에서는 같은 것이다**: 선형 최소제곱의 Hessian 이 정확히 `2XᵀX` 이고 `𝒩(X)=𝒩(XᵀX)` 이며 등분산 가우시안이면 Fisher 가 `XᵀX/σ²` 다. 우리 비선형 문제로는 `X → Jacobian J(θ)` 로 옮기면 되고, 그때 `𝒩(J)` 는 **국소**가 된다 (Lin 이 자기 감도에 붙인 것과 같은 한계).
  2. **정칙화가 하는 일** → `[인쇄]` "The vectors in the nullspace **affect only the regularization term**". 즉 **데이터는 계수를 부분공간 하나만큼 결정하지 못하고 그 안의 점은 오직 정칙화가 고른다.** 방법이 두 부류로 갈린다 — RR·PCR·PLS·최소노름해는 그 성분을 **정확히 0** 으로 두고(SI §S2 증명 3건), lasso·EN·**fused lasso** 는 L1 때문에 **0 이 아니다**. **물리적 의미 주장은 조건부**다: `[인쇄]` "**if chosen corresponding to prior physical knowledge**, lead to interpretable regression results. **Otherwise** … can make it **impossible** to obtain regression coefficients close to the true coefficients." 그리고 그 조건이 맞는지는 데이터로 확인 불가라고 못 박는다 — `[인쇄]` "**From the data alone, it is not possible to state whether 𝐲 was constructed from constant or parabolic coefficients.**" 요컨대 **넣은 사전지식만큼만 나온다.**
  3. **무엇을 금지하는가** → `[인쇄]` §1: 계수를 "in terms of shape (e.g., **peaks, plateaus, slopes**)" 로 읽는 것이 "often done implicitly by engineers" 이지만 "**such an interpretation can lead to misleading conclusions**". `[인쇄]` §4.2.2: 직교 성분은 "**less interpretable while making identical predictions**". **"크기 = 중요도" 의 그림판 반증**은 `[도표]` Fig. 4a — 참계수가 전 구간 **상수 0.001** 인데 PLS 계수는 **3.2 V 위에서 ≈ 0 으로 붕괴**하고 nullspace 보정하면 **≈ 0.0009 로 돌아온다**. 덤으로 `[도표]` Fig. 4b 범례에서 **참계수의 학습 NRMSE(0.127 %)가 적합 계수(0.108 %)보다 나쁘다** — "낮은 잔차 ⇒ 참에 가깝다" 도 깨진다. ARD 가중치·permutation importance 함정과 **같은 계열이되 더 근본적**이다 (사후 귀속이 아니라 모형 자신의 계수가 자유롭다).
  4. **★★ 우리가 그대로 쓸 도구 (이번 흡수의 최대 소득)** → **있다.** `src/nullspace.py:390 nullspace_calc`, 핵심 한 줄이 `:429` `v_[i,:] = -linalg.inv(g*self.XtX + I_) @ self.w` = 논문 식 (19). **`XtX → JᵀJ`, `w → θ_A−θ_B` 로 바꾸면 우리 것**이고 `XXᵀ` 역행렬을 피한다. 그리는 함수는 `src/plotting_utils.py:298 plot_nullspace_analysis` (세 곡선 + NRMSE 범례), valley 폭을 재는 것은 `src/nullspace.py:199 objective_function_trajectory` (`γ` 로그 스윕 → ΔNRMSE·‖Xv‖ 이중축; **논문에는 안 실렸고 코드에만 있다**). 부수로 `src/utils.py:517/523` 사영자 2종, `src/hd_data.py:144 analyze_snr_by_splines` (좌표별 SNR).
  - **★ null 방향을 그린 그림은 논문에 없다 — 그러나 저자가 시도했다가 포기한 자리가 저장소에 있다.** 노트북 cell 36–37 이 `scipy.linalg.null_space(X)` 로 기저를 뽑아 그리고, 바로 아래 저자 주석이 `[인쇄]` "It's **difficult to interpret when visualized this way** … orthogonal unit vectors which can be difficult to visualize (and interpret)". **실패 원인은 차원(`[재현]` 959)이지 발상이 아니다.** 우리 null 방향은 **1차원이고 닫힌 형태로 알려져 있으므로 그 장애가 없다.** 논문이 실제로 실은 것은 Fig. 8 (`β_FL` vs 그 직교 성분) 이며, 두 곡선의 **차이**가 곧 nullspace 벡터다.
  5. **데이터** → `data/lfp_slim.csv` **124행 × 1004열** (전압 2.0–3.5 V 1000점의 `ΔQ_{100−10}`(Ah) + cycle life + 충전 프로토콜 class + Severson 분할). `[재현]` split 0/1/2 = **41/43/40**, cycle life 148~2237. **"small subset" 은 셀 수가 아니라 셀당 데이터를 줄인 것** (124셀 전부 있다). CC-BY 4.0 이라 재사용 가능하고 실제로 돌려 봤다. **단 LLI/LAM 라벨이 없다** — 방법론 검증용이지 우리 축 질문에 직접 답하지 못한다.
- **`[재현]` 우리가 직접 계산한 것** (인용 금지 등급, 원문 미인쇄): `dim 𝒩(X_train) = 959` (평균중심 후 960) · 평균중심 후 `cond(XXᵀ) ≈ 2.1e17` (→ **논문 식 (14) 의 가역 전제가 논문 자신의 전처리로 깨진다**; 식 (19) 를 써야 한다) · fused lasso 계수 **노름의 36.5 % 가 nullspace 안**이고 그것을 지워도 학습 예측 차이가 **1.3e−15** · 점별로는 계수가 **2.09** 움직여도 예측 불변 (그 지점 최대 계수 3.18) · **그 자유도가 3.0–3.3 V 에 집중**되는데 **논문이 상전이 물리로 가장 조밀하게 해석한 구간이 바로 거기다** (논문은 두 사실을 같은 쪽에 인쇄해 놓고 연결하지 않는다).
- **어휘 전수 (이 계보 열한 편째) — 새 형태**: `nullspace` **69**(본문)/**9**(SI) 로 비유일성을 **논문 전체의 주제**로 다루면서 `identifiab*` **0** · `degenerac*` **0** · `unique`/`non-unique`/`uniqueness` **0** · `ill-posed` **0** · `Hessian` **0** · `Fisher` **0** · `uncertaint*` **0** · `confidence` **0** · `error bar` **0** · `LLI`/`LAM`/`half-cell` **0**. `[해석]` 아홉 편의 "어휘가 없다", 열 편째의 "절반만 자기 쪽으로 돌린다" 와 또 다르다 — **개념을 정면으로 다루되 자기 어휘를 새로 만들고 표준 어휘를 안 쓴다.** 그 결과 Lin & Khoo 2024(`identifiab*` 26 / `nullspace` 0)와 이 논문은 같은 수학적 대상을 다루면서 **서로를 인용하지 않는다.**
- **비판 (digest §15) — 큰 것 넷**: (1) **`γ` 를 손으로 골랐다** (`[인쇄]` "We **hand-selected** γ = 10") 고 결론의 진폭이 거기에 달려 있는데 민감도 분석이 없다 (도구는 코드에 있다). (2) **경고해 놓고 스스로 그 함정에 들어간다** — "데이터만으로는 참계수 모양을 말할 수 없다" 고 적은 뒤 **참계수를 모르는** 실측 응답의 계수 봉우리에 철 반사이트 결함 형성에너지 **0.55 eV** 까지 붙인다. (3) **비교가 불공평하다** — cycle life 절에서만 1-SE 규칙을 버려(각주 3) PLS 정칙화를 약하게 만든 뒤 "PLS 는 부호가 자주 바뀌어 해석하기 어렵다" 고 결론짓는다. (4) **일차 시험셋에서 셀 하나를 빼고 본문에 안 적었다** — 흔적은 Table 1 의 `Test 1 (**42**)` 뿐이고(원 분할 43), 사유는 코드 주석 `[인쇄]` "Very different shape and a lot lower cycle life … **Degradation is not linear**" (`[재현]` cycle life 148 인 셀). **잘한 점도 적었다**: 코드·데이터 완전 공개로 이 계보 열한 편 중 재현성이 가장 좋고, 못 실은 실패를 코드 주석에 남겼으며, 참계수를 아는 합성 응답으로 "예측이 맞는가" 와 "계수를 되찾았는가" 를 분리했다.
- **컴파일 1건**: [[nullspace-coefficient-interpretation]] (concept — nullspace 정의와 우리 Jacobian 으로의 사전(辭典), 정칙화 두 부류 표, 금지되는 독법 3가지, 파일·함수 단위 도구 목록, 재현 수치).
- **기존 페이지 4건 갱신**: [[fitting-degeneracy]] 에 **"★ 그 방향을 그리는 법"** 절 신설 (식 19·23 을 우리 좌표로 옮긴 5단계 절차 + 왜 정확 사영이 아니라 완화판인지 + 국소 한계). [[np-lip-ocv-reparametrization]] 에 "이 방향을 그리는 법은 다른 문헌에 있다" 절 (**두 페이지가 짝** — 여기가 *무엇을*, 저기가 *어떻게*).
- **질문 카드 2건 갱신 (Evidence 귀속 명시)**: [[22p-physics-or-degeneracy]] — **Evidence For 2건 추가** (축퇴 방향 위의 값은 데이터가 아니라 추정기가 정한다 · "낮은 잔차 ⇒ 참" 반증), **Evidence Against 0건** (이 논문은 22p 가 물리라는 근거를 주지 않는다 — 열화 모드를 재지 않으므로). Status Log (11), status `active` 유지. [[pvs-sev-lli-lampe-separability]] — **Evidence Against 1건 추가** (= H1 반대쪽; 낮은 permutation importance 를 "정보 없음" 으로 읽는 Evidence For 2번의 **등급을 낮춘다**), **Evidence For 0건**. Status Log (11), status `open` 유지.
- **다음 흡수 후보 1건 추가**: `[인쇄]` §4.2.2 가 데이터 누수 회피 근거로 인용하는 **Geslin et al. 2023**, "Selecting the appropriate features in battery lifetime predictions", *Joule* **7**, 1956–1965.
- **그림 정직성**: 크로핑 11장 중 **9장을 직접 열어 봄** (fig 1·2·3·4·5·6·7·8 + SI S2). **안 본 것**: SI Fig. S1(예측 산점도 — 본문·SI 텍스트에 같은 값이 인쇄됨), Table 1(추출기 안내대로 이미지 대신 PDF 텍스트에서 옮김). SI Fig. S3 은 **추출기가 영역을 못 찾아 크롭이 없다**. **본문 서술과 어긋난 그림 1건(사소)**: SI Fig. S2b 의 평균 `X̄` 가 **양수**로 그려져 있으나 `[재현]` 실제 데이터 평균은 같은 크기의 **음수**다 (2.0 V −0.0111 / 2.9 V −0.0467, 소수 넷째 자리까지 일치). Fig. 3a 는 음수로 올바르다. **크롭 품질 주의**: fig_6·fig_7 은 왼쪽 y축 눈금값이 잘려 **수치를 읽지 않고 모양만** 기술했다.
- **이 세션은 git 명령을 하나도 실행하지 않았다** (사용자 지시). 파일만 만들어 두었고 커밋은 사용자가 한다. 변경은 전부 `wiki/` 안이므로 degradation-degeneracy 의 `source_digest` 를 바꾸지 않는다.

## [2026-09-03] ingest | Cui et al. 2024 — 형성이 전극 이용상태를 정해 수명을 바꾼다 (Joule 8, 3072–3087) — 이 계열 13번째·마지막
- 원문: 본문 17쪽 + SI 19쪽 (pdftoppm 미설치로 pymupdf 텍스트 추출 + get_pixmap 렌더 병행). raw digest:
  `raw/papers/cui2024_electrode-utilization-formation-cycle-life.md` (sha256 봉인, 그림 37장 크로핑 후 **11장을 직접 열어 봄**).
- **★ 이 논문의 정체**: [[fused-lasso-feature-design-framework]] (Rhyu et al. 2025, Joule 9)
  가 참고문헌 [47] 로 인용하는 **바로 그 186셀·62프로토콜 데이터셋
  (`data.matr.io/8/`) 을 만들고 처음 분석한 원전**이다. 즉 이번 흡수는 새
  데이터셋이 아니라 같은 데이터의 다른 저자·다른 방법(수작업 DVA 물리
  feature "electrode utilization" vs 자동 fused-lasso 설계 feature) 판이다
  (raw digest §0 전수 대조).
- **★ 사용자가 지정한 6개 질문에 대한 판정 (근거 등급은 raw digest §2)**:
  1. **"electrode utilization" 정의**: `[인쇄]` "the utilization range of an
     electrode is determined by its SOC at full-cell top of charge (4.4 V) and
     bottom of discharge (3 V)" — [[np-lip-ocv-reparametrization]] 의
     `z⁺(z⁻) = z₀⁺ − r_N/P·z⁻` 를 컷오프 두 점에서 평가한 값과 **같은 대상**
     (실측 vs 모델의 차이). 우리 `(LLI, LAM_PE, LAM_NE)` 와는 정의만 대응하고
     **정량 환산은 안 된다**(비교 기준=pristine 이 원문에 없음).
  2. **인과 강도**: **진짜 개입 실험**(LHS 로 6개 형성 파라미터를 실험자가
     직접 설정, 모든 셀이 동일 aging 프로토콜). 다만 추가 36셀은 결과를 본
     뒤 표적 증강(사전 등록 아님), 무작위 실행순서 미기재.
  3. **Rhyu 2025 와의 관계**: 같은 데이터, 다른 부분집합(Cui=전체 178~186셀,
     Rhyu=느린 형성 32셀 물리검증), 다른 메커니즘(Cui=전극 이용상태 이동/
     열역학, Rhyu=입자 저항 불균일성/동역학). **충돌이 아니라 상보적** —
     전극 이용상태 축은 **그룹 간**(fast vs slow) 변이를 지배하고, Rhyu 가
     보는 **그룹 내** 변이는 다른 축(동역학)이 설명한다. 약한 불일치 1건:
     Cui 본문 "70% 증가"(Conclusions) vs Rhyu 가 인용한 "2배" — 원문 대조로
     확인, Cui 원문에 "2×"·"double" 표현 없음.
  4. **우리 격자의 시작점**: N/P = 1.16 **고정**(Table 1, 셀 설계), 형성이
     움직이는 것은 `Q_Li`(∝ Li/P = Lin 의 z₀⁺) **하나뿐**. → 형성 직후 상태는
     `(1,1,1)` null 방향이 아니라 **z₀⁺(LLI) 축 위**에 있을 개연성 — 검증
     미실행, 값싸게 확인 가능.
  5. **잡음 문턱**: `[인쇄]` DVA 적합 RMSE **< 6 mV**(SI Fig. S15 캡션) — 우리
     σ=5 mV 문턱과 같은 자릿수(상한으로만 씀). SI Table S3(반쪽전지 반복측정,
     원문 표에서 우리가 직접 계산) — **PE 전압 재현성 1–12 mV, NE 전압
     재현성 8–93 mV**(전극·SOC 위치에 따라 8배 이상 차이) — Phase 1c/1d 의
     "균일 σ" 가정이 단순화일 수 있다는 첫 실측 근거.
  6. **해석 가능성 함정 6종 점검**: ①(중요도→물리) **완화**(SHAP-선별 후
     통제비교의 2단 구조) · ②(시뮬레이션 자기검증) **해당없음**(시뮬레이션
     자체가 없음, 대신 반쪽전지 독립 실측 Table S3 로 DVA 방향과 교차검증) ·
     ③(외삽 기준선 없음) **있음** · ④(셀 단위 분할 아님) **회피**(그룹=
     프로토콜) · ⑤(예측구간 미보정) **있음** · ⑥(라벨 불확실성 부재) **있음**
     (Rhyu SI Note S11·Birkl 2017·Dubarry 2012 와 같은 패턴의 네 번째 사례).
- **어휘 전수 (열세 편째, 새 형태)**: `identifiab*`·`degenerac*`·`nullspace`·
  `uncertain*`·`error bar`·`confidence interval` 전부 **0**. **`LLI`·`LAM`
  약어 자체가 대소문자 정확 일치 검색으로 0회** — 케이스-무시 검색은
  "Shijing"·"filling" 등에서 오탐. 즉 이 논문은 식별 가능성 언어가 없는
  것을 넘어 **모드 분류 언어(LLI/LAM) 자체를 안 쓴다** — `Q_PE, Q_NE, Q_Li,
  SOC_PE,·, SOC_NE,·` 라는 병행 표기 전통(Chueh/Bazant 그룹)을 쓰면서도 DVA
  방법 원전은 Dubarry 2012 를 그대로 인용한다(방법 계보는 공유, 어휘는 분리).
- **컴파일 반영 (Evidence For/Against 귀속 명시)**:
  [[22p-physics-or-degeneracy]] — Status Log (13) 추가, **Evidence 어느 쪽도
  아님**(새 근거는 잡음 문턱 정박점 + 방법론 패턴 확인이지 22p 수치 자체에
  대한 직접 증거가 아님), status `active` 유지, `sources` 에 raw 추가.
  [[np-lip-ocv-reparametrization]] — "전극 이용범위 = 이 직선을 컷오프에서
  잰 값" 절 신설, N/P 고정·Li/P 만 이동 실측 사례 등재, `sources` 갱신.
- **그림 정직성**: 37장(그림 33+표 4) 중 **11장을 직접 열어 봄**(fig 1·2·3·4·
  5·6·8·S12·S13·S16·S17). 안 본 것 15장은 본문/SI 텍스트가 핵심 수치(상관·
  RMSE·%)를 이미 인쇄해 생략(raw digest §12). **본문이 그림보다 정성적인
  곳 1건**: "PE SOCs ... up to 8% lower"(정성)만 인쇄되고 Fig. 4D 를 직접
  봐야 ρ=−0.82·fast/others 군집 분리 형태를 확인할 수 있었다.
- **이 세션은 git 명령을 하나도 실행하지 않았다** (사용자 지시). 파일만
  만들어 두었고 커밋은 사용자가 한다. 변경은 전부 `wiki/` 안이므로
  degradation-degeneracy 의 `source_digest` 를 바꾸지 않는다.

## [2026-09-03] ingest | Navidi et al. 2024 — 열화 진단용 PIML 네 방법 비교 (ESM 68, 103343)

**누락분 흡수** (사용자가 준 13편 중 digest 없이 빠져 있던 5번). raw:
`raw/papers/navidi2024_piml-degradation-diagnostics-comparison.md`
(sha256 `d71f0cb9…`, 본문 38,963자). 그림 25장 크로핑
(`raw/figures/navidi2024_piml-degradation-diagnostics-comparison/`).

- **제목이 약속하는 것보다 좁다**: "comparison of state-of-the-art methods" 는
  **열화 진단 방법의 비교가 아니라, 하나의 진단 모델(4-파라미터 반쪽전지 창
  적합)을 흉내 내는 ML 배관 네 개의 비교**다 (PINN · co-kriging · delta
  learning(elastic net) · data augmentation). EIS/DRT·전기화학 모델 역산·
  ICA 봉우리 진단은 도입부 열거뿐이고 실험에 오르지 않는다. 네 방법은
  입력(dQ/dV 100점)·물리 모델·**정답(사람의 수동 적합)** 을 전부 공유한다.
- **★★ 우리 fitting 모델과 좌표가 글자 그대로 같은 첫 문헌**:
  `V_c(Q) = V_p((Q−δ_p)/m_p) − V_n((Q−δ_n)/m_n)`, 자유 파라미터 **4개**,
  **컷오프 등식 제약 없음**. `m_p ↔ α_PE · δ_p ↔ β_PE · m_n ↔ α_NE ·
  δ_n ↔ β_NE`. `LII = Q_p − (δ_p − δ_n)` 이 우리 legacy LLI 식과 구조가
  같다 (인용 경로의 증거는 **아니다** — 후속 확인 항목으로만 등재).
- **★ 우리 파이프라인이 이 논문에서 시험대에 올라 기각된다** (부록 A2):
  자동(비선형 최적화) 적합이 `[인쇄]` "multiple local minima, leading to
  run-to-run variability … depending on the initial guess" 이라며 **사람의
  수동 적합**을 정답으로 채택. 5회 다중시작 산포는 `[도표, Fig. 15]`
  **±1.5–11 %p**(우리 `tol = 2 %p` 의 1~5배). **그러나 목적함수 값을
  보고하지 않아 flat valley ↔ multimodal 를 구별하지 않은 채 기각했다.**
- **★ 새 경고 1건**: 같은 그림의 해체 실측 대조에서 **다중시작 산포가 실제
  오차의 하한조차 아니다** (G2C1 `m_p`: 5개 해 전부 0.835–0.935, 참값 0.63).
- **본문에 성능 수치가 하나도 인쇄돼 있지 않다** (`mV` 0회, RMSPE 표 없음).
  모든 비교 주장이 그림 판독으로만 검증되며, **본문이 자기 그림보다 낙관적인
  곳이 한 방향으로 5건**(raw §7 I3–I7). 인용 금지 4건 확정.
- **어휘 전수 (열두 편째) — 새 형태**: `identifiab*`·`degenerac*`·
  `nullspace`·`non-unique`·`collinear*`·`Hessian`·`Fisher`·`mV` **각 0**,
  그런데 `uncertaint*` **21회로 계보 최다**이고 **21회 전부 예측
  불확실성**이다(라벨·파라미터 불확실성 0회). 비교 논문인데도 Table 5 의
  열 개 등급 축에 **"비유일성에 대한 강건성" 이 없다** — 개별 논문의 침묵과
  달리 그 축이 **선택지 목록 자체에 없었다**는 뜻.
- **신설**: [[piml-physics-injection-points]] — 물리가 ML 파이프라인에
  들어가는 **여섯** 자리 (표준 4분류 + **학습 데이터** + **라벨 그 자체**),
  그리고 Fig. 13 ablation 이 준 첫 실측 순위 **손실항 55–70 % ≫ 학습 데이터
  10–23 %**. 여섯째 자리는 **방법 간 비교로는 원리적으로 검출되지 않는다**
  (축퇴가 공통 인자라 차이에서 소거된다).
- **컴파일 반영 (Evidence For/Against 귀속 명시)**:
  [[22p-physics-or-degeneracy]] — Status Log (14) 추가, **Evidence 어느
  쪽도 아님 = 경계 확정**(좌표 일치 + 방법론 정박점이지 22p 수치에 대한
  직접 증거가 아니다), status `active` 유지.
  [[pvs-sev-lli-lampe-separability]] — **Evidence For 에 약한 근거 1건**
  (관측을 곡선 100점까지 늘려도 전극별 분해만 3.7–9.9 % 로 남는다),
  Evidence Against 에는 없음, status `open` 유지.
  [[fitting-degeneracy]] — multimodal 가지에 **야생 실측 1건** + "산포는
  오차의 하한이 아니다" 경고 신설.
  [[interpretable-ml-battery-prognosis-taxonomy]] — 4분류에 칸 두 개가
  모자란다는 절 신설, 새 개념 페이지로 분리.
- **그림 정직성**: 25장(그림 20 + 표 5) 중 **7장을 직접 열어 봄**
  (fig 2·3·6·7·8·12·13·15 — 여덟이 아니라 fig_15 를 4분면으로 확대해 본 것
  포함하면 실질 8장이고, Fig. 12 범례는 PDF 14쪽 재렌더로 확인).
  안 본 것 13장(fig 1·4·5·9·10·11·14·16–19·20)은 도식이거나 §3.1 표를
  넘어서는 수치를 주지 않아 생략. 표 5장은 이미지로 안 읽음(PDF 텍스트가
  정확). **본문과 어긋난 그림 4건**(Fig. 8 ×3, Fig. 15 ×1) + **원문 내부
  표기 불일치 3건**(Fig. 15 의 셀 번호·날짜·온도가 §3.1·Table 1 과 어긋남).
- **이 세션은 git 명령을 하나도 실행하지 않았다** (사용자 지시). 변경은
  전부 `wiki/` 안이므로 degradation-degeneracy 의 `source_digest` 불변.
  `python3 wiki/tools/lint.py` → **0 errors / 0 warnings** (23 pages).

## [2026-09-03] ingest | Marongiu et al. 2016 — On-board capacity estimation of LFP batteries by means of half-cell curves (JPS 324)

- **사용자가 준 13편의 마지막 누락분.** raw:
  `raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md` (sha256 봉인).
  제목에 **half-cell curves** 가 들어간 유일한 편이고, 22p 카드가 legacy LLI
  식의 출처 후보로 지목해 둔 **Birkl 참고문헌 [26]** 이 이것이었다.
- **최대 산출물 — 이 계보의 축퇴를 처음으로 닫힌 형태로 풀었다.** 원전 식
  (2)–(5) 가 **모드 5개 → 창 좌표 4개** 사상을 등식 제약 **0개**로 인쇄한다.
  거기서 나오는 정확한 null 2차원 `n₁ = (−N,0,0,+1,−1)`,
  `n₂ = (+1,−1,+1,0,0)` 이 네 창 좌표·세 관측·총용량을 **정확히 불변**으로
  두고(수치 확인), 그 몫공간이 **Birkl 2017 의 `[total-LLI, LAM_PE, LAM_NE]`
  와 정확히 같다**. 산문으로만 있던 진술이 수식이 됐다.
- 새 페이지 1: [[halfcell-window-parametrization-lineage]] (comparisons/ 첫
  페이지) — 같은 4개 창 좌표를 무엇으로 매개화하고 여분을 어떻게 죽이는가:
  **등식(Birkl·Mohtat) / 0-고정(Marongiu) / 애초에 안 만들기(Lin·Navidi·우리)**
  셋뿐임을 정리.
- 갱신: [[fitting-degeneracy]] — 닫힌 형태 null 방향 **둘** + **세 번째 실패
  모드 후보**(중복 관측이 최적화를 방해한다) + 초기값 통제 대조군 실측.
  [[np-lip-ocv-reparametrization]] — Lin 이 비판한 "redundancy" 의 가장 극단
  사례(제약 0, 여분 2) 등재. [[birkl-ocv-degradation-diagnostic]] — 3-파라미터
  좌표가 어느 공간의 몫공간인지 확정.
  [[22p-physics-or-degeneracy]] — Status Log (15), **Evidence 어느 쪽도 아님
  = 경계 확정**, status `active` 유지. 인용 계보 항목 종결(legacy 식은 이
  논문에도 없다 — `docs/02_CODE_AUDIT.md` 의 정정이 옳다).
  [[pvs-sev-lli-lampe-separability]] — Evidence For 2건(중복 관측을 더했더니
  **나빠진** 대조군 · 초기값 지배), status `open` 유지.
- **어휘 전수 (열세 편째)**: `identifiab*` `degenerac*` `uniqu*` `nullspace`
  `uncertaint*` `error bar` `cross-valid*` `sensitivit*` `Fisher` `Hessian`
  **각 0** · `mV` **1**. 그런데 `[인쇄]` "The correct determination of all the
  degradation mechanisms … **is out of the goal of this work**" — **어휘가
  없는 것과 주장을 절제하는 것은 다른 축**임을 보여 주는 첫 편.
- **그림 정직성**: 13장(그림 8 + 표 5) 중 **그림 8장 전부를 직접 열어 봄**
  (fig 1–8). 추가로 저널 조판본 p.160 을 400 dpi 로 재렌더링해 **식 (2)–(5)
  의 마이너스 부호를 눈으로 확인**했다 (축퇴 계산이 부호에 전적으로 의존).
  표 5장은 이미지로 안 읽음(PDF 텍스트가 정확, Table 1–5 를 digest 에 전재).
  **원문 내부 불일치 7건** 기록 — 특히 목적함수가 본문 식 (9)=`max` 와
  Fig. 3=`Σ` 로 다르고, **Fig. 6 의 숫자가 합 쪽을 지지한다.**
- **이 세션은 git 명령을 하나도 실행하지 않았다** (사용자 지시). 변경은 전부
  `wiki/` 안이므로 degradation-degeneracy 의 `source_digest` 불변.
  `degradation-degeneracy/` 와 `mode-observability/` 는 **읽기만** 했다.

## [2026-09-03] create | Mode Identifiability Unmeasured Lineage (synthesis)

사용자가 준 논문 **13편이 전부 흡수 완료**된 뒤, 그 13편을 가로지르는 **논지 하나**를
`syntheses/` 첫 페이지로 세웠다 (SCHEMA 의 synthesis 규약: Thesis 한 문장 →
Argument → Counter-arguments **보존** → Gap).

**Thesis**: 13편은 LLI/LAM 분해를 **보고**하지만 그 분해가 **유일한지**를 잰 편이
하나도 없고, **그것을 잴 도구는 이미 그 13편 안에 흩어져 있다** — 빠진 것은 도구가
아니라 그 도구를 자기 결과에 겨누는 한 걸음이다.

근거 여섯:

1. **침묵의 형태가 매번 다르다** — 13편 어휘 전수표. 식 안에 넣어 두기(Dubarry) ·
   근거로 쓰면서 이름 안 붙이기(Marongiu) · 산문 진술(Birkl) · 어휘 자체 없음(4편) ·
   비교 논문인데 0(Navidi) · 약어조차 안 씀(Cui) · 한 번 인정하고 치환(Tao) ·
   절반만 자기 쪽으로(Lin) · 자기 어휘를 새로 만들기(Schaeffer).
2. **축퇴가 세 번 인쇄됐고 세 번 다 계산되지 않았다** — 그 null 을
   [[halfcell-window-parametrization-lineage]] 이 풀었고 독립 검산했다.
3. **Lin 이 네 번째 null 을 인쇄했지만** `C_θ` 를 쥐고 `sqrt(diag)` 만 그렸다.
4. **그리는 기계는 Schaeffer 에 있고**, 저자가 959차원에서 포기한 주석까지 남아 있다.
5. **우리 Phase 1c·1d 가 겨눈 결과** — 12.04° 일치, 그러나 조건수 18.2 (평평하지만
   0 이 아니다) → 방어할 문장은 "구조적 불가" 가 아니라 **"우리 잡음 수준에서 불가"**.
6. **재지 않은 대가의 야생 실측** — Marongiu 가 초기값만 10 % → 0 % 로 바꿔 오차
   6.38 → 14.46 %. 동시에 총용량은 null 위에서 불변이므로 **"용량이 맞으니 방법이
   옳다" 는 추론이 원리적으로 성립하지 않는다.**

**Counter-arguments 다섯을 보존**했다 — (a) Cui 는 독립 half-cell 로 교차검증하므로
"하나도 없다" 를 문자 그대로 쓸 수 없다(논지를 **유일성**으로 좁혔다) · (b) Lin 은
자기 범위를 명시 한정했다(논지는 "게을렀다" 가 아니라 **어휘 분단**) · (c) 목적이
예측이면 유일성은 무관할 수 있다(사정권은 **분해를 물리로 읽는 문장**) ·
(d) **우리 Phase 1d 가 Lin 의 redundancy 지적을 반증했다**(rank 2 가 아니라 4) ·
(e) 관측을 늘리면 갈린다는 반론은 두 방향에서 약해졌지만 **SEV 는 열려 있다**.

**Bias Check 넷**도 적었다 — 13편은 우리가 고른 게 아니라 **주어진** 것이고
(Mohtat 2019 는 아직 안 읽었다) · 어휘 전수는 문자열 검사라 **다른 이름으로 다루는
편을 0 으로 셀 수 있고**(Cui 가 실제 사례) · 우리 실측은 **한 동작점·한 화학**이며 ·
**논지가 우리에게 유리한 방향**이라 반대 증거를 덜 찾았을 수 있다.

역링크 셋: [[22p-physics-or-degeneracy]] · [[pvs-sev-lli-lampe-separability]] ·
[[fitting-degeneracy]]. index 전체 페이지 24 → 25.

## [2026-09-03] update | Phase 1e — 컷오프 제약 판정으로 Gap 5 를 닫는다

`syntheses/mode-identifiability-unmeasured-lineage.md` 의 **Gap 5** 를 닫고 그
결과를 **Counter-argument (d)** 에 접었다. 정본은
`mode-observability/results/phase1e/` CSV.

**물음**: Lin 이 지적한 `redundancy` 를 컷오프 등식으로 지우면 우리 좌표에서
무엇이 사라지는가 — σ3·σ4(여분)인가 σ1·σ2(정보)인가.

**실측**: 제약 gradient 가 **강한 쌍과 1.5°·2.0°** 로 거의 겹치고 약한 쌍과는
65°·16° 로 멀다. 제약 접공간에 `J` 를 제한하면 남는 감도가 원래 최강 방향의
**0.13~0.49 배**로 떨어진다. → **우리 좌표에서 그 제약은 여분이 아니라 정보를
지운다.** "Lin 이 지적했으니 우리도 제약을 걸자" 는 처방은 적용하면 안 된다.

**덤**: 가장 약한 방향의 모양이 두 동작점에서 거의 같다 — `Δα_NE ≈ −Δβ_NE`,
즉 **음극 창의 오른쪽 끝은 두고 왼쪽 끝만 미는** 변형.

**경계 넷을 함께 적었다** — Birkl 이 틀렸다는 말이 아니고(시작 매개화가 다르다) ·
우리 `g₁·g₂` 는 **대리물**이며 · 국소·두 동작점·한 화학이고 · "제약을 걸면 안
된다" 가 아니라 "이 제약은 여분 제거가 아니다" 이다.

새로 열린 것 둘: Birkl 등식을 우리 좌표로 정확히 옮기기 · `v₄` 의 "음극 창 왼쪽
끝" 이 Phase 1c 잔차가 몰린 `x_norm = 0.839` 와 같은 자리인지.

## [2026-09-04] update | Phase 1g — 12.04° 는 동역학 산물이 아니다 (Gap 2 절반)

정본은 `mode-observability/results/phase1g/`.

세 판을 나란히 놓아 몫을 나눴다. **A 판이 Phase 1c 를 소수점까지 재현**한다
(12.04° · cos 0.977999 · 조건수 18.24) — 처음엔 10.92° 가 나왔는데 Phase 1c 의
`LO, HI = 0.02, 0.98` 절단을 안 맞춘 탓이었고, 맞추자 일치했다. 이 검산이
없었으면 비교 전체가 헛것이 될 뻔했다.

- **A → B** (시뮬 → **순수 창 대수**) : 12.04° → 10.56°, **Δ −1.48°**
- **B → C** (참조곡선을 평형 OCP 로)  : 10.56° → 39.03°, Δ +28.47°

**판정**: B 의 변환은 `windowed_curve` 두 번과 뺄셈뿐이라 모드→곡선 경로에
동역학이 없다. 그런데 null 방향이 거의 같은 자리다 → **12° 는 동역학 산물이
아니라 창 모델의 구조에서 온다.**

**C 판은 기각했다.** `"halfcell"` 정규화는 **전극 전체**, `"grid"` 는 **셀 창**
기준이라 B→C 가 "전류를 뺐다" 가 아니라 "좌표계를 바꿨다" 이기도 하다. 증거가
열 노름에 있다 — `LAM_PE` 가 8.38 → **50.17 V/단위**로 6배. **Phase 1f 가 막힌
자리와 같은 문제**(두 `x` 정규화 사이 환산 부재)이고, 그래서 두 Phase 가 하나의
미제로 수렴했다.

정직 항목: B 판에도 **reference 곡선 자체의** 동역학은 남아 있다. 정확한 문장은
"12° 가 전류와 무관" 이 아니라 **"모드→곡선 경로의 동역학과 무관"** 이다.

## [2026-09-04] update | Mohtat 2019 을 **구현본으로** 흡수 — 컷오프 등식은 우리 null 을 못 본다 (Phase 1h)

정본은 `mode-observability/results/phase1h/` CSV · 판정문은
`mode-observability/docs/PHASE1H_NOTES.md`. `degradation-degeneracy/` 는 읽기만 했다.

**먼저 정직 항목 — 원전을 못 읽었다.** `[11] Mohtat et al. 2019` (*J. Power
Sources* 427, 101–111) 은 Elsevier 유료이고 이 실행 환경의 egress 정책이
`api.semanticscholar.org`·`docs.pybamm.org` 를 막는다 (실측 CONNECT 403 ·
`EGRESS_BLOCKED`). 그래서 흡수한 것은 **그 모델의 구현본**이다 — PyBaMM 26.7.1.0
`models/full_battery_models/lithium_ion/electrode_soh.py` 의 `_ElectrodeSOH`
(`pybamm.citations.register("Mohtat2019")`), docstring 이 다섯 식을 인쇄한다.
**Lin 이 선행자로 지목한 근거인 Fisher 식별가능성 분석 자체는 여전히 미독**이고,
그래서 통합 논지의 Bias Check 1 은 **닫히지 않았다**.

**사전(dictionary) 을 확정했다.** `windowed_curve` 정의에서 Mohtat 좌표
`(x_100, y_100, x_0, y_0)` ↔ 우리 `[α_PE, β_PE, α_NE, β_NE]` 가 일대일이고,
Mohtat 의 두 전압 등식은 우리 x 축에서 글자 그대로 `U_full(0)=V_max`,
`U_full(1)=V_min` 이다. 그리고 `Q_Li = y_100·Q_p + x_100·Q_n` 이 **`src/inventory.py`
의 LLI 유도 그 자체**다 — 거기 나오는 `(w_PE, w_NE, κ)` 가 "전극 전체" 와 "셀 창"
두 정규화를 잇는 상수이고, `reference_inventory()` 가 그것을 셀 기하에서 직접
계산한다. **Phase 1f·1g 가 막힌 환산의 절반이 이미 코드 안에 있었다**
(다만 그것은 `c_init`, 필요한 것은 `c_max` — 아직 안 쟀다).

**실측 넷**

1. **컷오프 등식은 우리 참값에서 성립하지 않는다.** 1023 조건에서 끝점 전압이
   `U_full(0)` **127.0 mV**, `U_full(1)` **53.6 mV** 폭으로 흔들린다 (설정 컷오프는
   4.2 / 2.5 V, 차이는 유한 전류 과전압). 등식으로 얹으면 그만큼이 모델 오차다.
2. **Lin 의 예언이 pristine 에서 맞는다.** `LLI=LAM_PE=LAM_NE=x` 위에서 SOC 정규화
   곡선이 통째로 불변이므로 이상적 셀이면 `∇g ⟂ (1,1,1)`. 실측 **83.95°·83.59°** —
   90° 에서 6° 남짓이고 그 6° 가 유한 전류 + 복합 음극의 몫이다.
   **22p 에서는 깨진다** (`g₂` 가 **44.16°**).
3. **그래도 판정은 안 바뀐다.** 끝점 2개를 관측에 얹으면 σ_min 이 **+3.16 %**
   (pristine) / **+5.95 %** (22p), 조건수 18.24→17.76 / 16.31→15.40. 게다가 그
   두 점은 새 관측이 아니라 **이미 맞추는 곡선의 양 끝**이다. → Birkl·Mohtat 계열의
   "등식으로 여분을 죽인다" 처방은 **창 좌표(Phase 1e)와 모드 좌표(Phase 1h)
   양쪽에서** 우리 문제를 개선하지 않는다.
4. **★ 22p 동작점에서 `u_min` 이 Lin 의 `(1,1,1)/√3` 와 4.61°** (pristine 12.04°
   보다 가깝다). `u_min = [0.5686, 0.5225, 0.6354]`, 조건수 16.31.
   **Phase 1c 의 한계 (a)("22p 에서 방향이 회전할 수 있다")가 닫혔다** — 회전하고,
   **Lin 쪽으로** 회전한다. **22p 의 축퇴는 Lin 의 닫힌 형태 축퇴와 사실상 같은
   방향이다.**

**자기 정정 — "12.04°" 는 점이 아니라 띠다.** 동작점 8개 × 전방차분 스텝 2개에서
각이 **4.61° ~ 21.89°** 에 흩어지고, 같은 pristine 에서 스텝만 0.02 → 0.04 로
바꿔도 **12.04° → 18.62°** 다 (격자 간격 0.02 라 더 작은 스텝은 이 자료로 못 잡는다).
Phase 1c 는 이 스텝 의존성을 신고하지 않았다. 앞으로 쓸 문장은 **"이 측정의
분해능 안에서 Lin 의 방향과 같다"** 이다.

갱신: `comparisons/halfcell-window-parametrization-lineage.md` (Mohtat 행을 구현본·
Lin 전언 두 줄로 분리 + 처방 1 에 실측 부착) · `syntheses/mode-identifiability-
unmeasured-lineage.md` (§5 정정 · Gap 2 단서 · Gap 6 신설 · Bias Check 1 갱신) ·
`questions/22p-physics-or-degeneracy.md` (2026-09-04 항목 4건).

## [2026-09-04] ingest | Mohtat 2019 원전 — 제약 CRB 로 **전극 창**은 쟀고 **모드**는 안 쟀다

raw: `raw/papers/mohtat2019_electrode-soh-estimability-expansion.md` (Elsevier
**조판본 11쪽**, *J. Power Sources* 427 (2019) 101–111, DOI
`10.1016/j.jpowsour.2019.03.104` — **p.1 에 인쇄돼 있어 대조 완료**).
2026-09-04 오전에 "구현본만 읽고 대리 흡수" 로 남겨 둔 자리를 **원전으로 대체**했다.
그림 9장 크로핑 → **6장 정독** (`fig_8` 핵심, `fig_1·2·3·4·7`), 2장 미열람
(`fig_5` 결정구조, `fig_6` 팽창 구간선형), 표 이미지 1장은 텍스트가 정본.
쪽 인용 규약: **PDF 인덱스 1–11** = 인쇄 쪽 101–111 (i ↔ 100+i).

**세 질문에 대한 답**

1. **Fisher 를 무엇에 세웠나.** 파라미터 `θ = [x₁₀₀, y₁₀₀, C_n, C_p]` (4개),
   관측 `Y = [OCV, Δt_c]` — **전압만이 아니라 셀 팽창(μm)까지**. 두 시나리오는
   이 벡터의 둘째 성분을 켜고 끄는 것이다. `𝓘_f = SᵀE⁻¹S` (식 29),
   `S = ∂Y/∂θ|_θ*` **참값에서 평가**. 스칼라 지표는 **D-최적성도 trace 도
   조건수도 아니고** `σ_θ = sqrt(diag[Σ])` (식 33) 를 참값으로 나눈 **백분율**
   (식 34). 제약 처리는 Stoica–Ng 1998: `Σ ≥ 𝒪(𝒪ᵀ𝓘_f𝒪)⁻¹𝒪ᵀ` (식 32), `𝒪` 는
   제약 gradient nullspace 정규직교기저 (식 31). 판정 기준이 **이분법**으로
   인쇄된다 — `[인쇄, p.7]` "If 𝒪ᵀ𝓘_f𝒪 is **nonsingular**, then the constrained
   problem is **identifiable**".
2. **결론이 무엇인가.** `[인쇄]` "with the addition of the expansion, the
   parameters are **estimable without the need to discharge the battery to a high
   Depth of Discharge (>70%)**" (Abstract) · "**DOD required for observability is
   reduced to 30%**" (Highlights) · "**a threshold of 5% is selected** … the
   estimation is feasible at **about 30% DOD**" (§6.3).
   **★ 그러나 "전압만으로는 못 가른다" 는 판정은 인쇄돼 있지 않다.** 결론절이
   정확히 반대로 적는다 — `[인쇄, §7]` "for the **voltage only** case … the
   measurements should be taken at a **wider range of SOC spanning at least two
   phase transitions**, in order to make **all the parameters identifiable**."
   즉 판정 변수는 **관측 종류가 아니라 데이터 창의 폭**이고, 팽창은 같은
   정밀도를 **더 얕은 창에서 사게 해 주는 수단**이다.
3. **매개화 장부.** **"4개 + 등식 1개" 가 Mohtat 자신의 표기다** (문제 (P) 를
   렌더링해 눈으로 대조: `θ = [x₁₀₀,y₁₀₀,C_n,C_p]`, `subject to,
   U_p(y₁₀₀) − U_n(x₁₀₀) = V_max`). 최소 전압 등식은 제약이 아니라 **사후에
   셀 용량 C 를 푸는 식 (27)** 로 쓰인다 — `[인쇄]` "the capacity is not included
   in the above formulation. Hence, **only the maximum voltage limit is used in
   the estimation problem**." → 구현본의 "5 − 2" 와 Mohtat 의 "4 − 1 (+C 사후)"
   은 **같은 문제의 두 장부**이고 둘 다 Ah 축 자유도 3.
   `[해석]` 다만 위키 비교표의 "Lin 이 전하는 표기" 행이 4개를 "전극 SOC 한계
   4개" 로 적어 둔 것은 부정확하다 — SOC 한계 **2개**(`x₁₀₀,y₁₀₀`) + 전극
   **용량 2개**(`C_n,C_p`) 다. 개수·자유도는 맞고 **구성이 다르다**.

**★ 통합 논지에 미치는 영향 (좁혀야 한다)**

| 논지 성분 | 이 논문이 깬 것 | 못 깬 것 |
|---|---|---|
| "식별 가능성을 정량한 편이 없다" | **깨진다** (제약 CRB + 판정선) | — |
| "축퇴를 지목한 편이 없다" | **깨진다 (1회)** — `[인쇄, p.8]` "the first and second columns … become **linearly dependent** … rank deficient … **unidentifiable**" | 그 축퇴를 **수치로 재지 않는다** |
| "**LLI/LAM 분해**의 유일성을 잰 편이 없다" | — | **못 깬다.** LLI·LAM 은 식 (16)·(20) 으로 정의만 하고 §5 이후 **어휘 전수 0회** |
| "축퇴의 **방향**을 보고한 편이 없다" | — | **못 깬다.** `Σ` 를 구하고 즉시 `diag` (식 33). 파라미터 `correlat*` 0회 |
| "추정기로 복원을 검증한 편이 없다" | — | **못 깬다.** 노이즈 실현·복원 오차 전무 |
| "전역 식별 가능성을 다룬 편이 없다" | — | **못 깬다.** `global` **0회** — Lin 은 최소한 "우리는 국소만" 이라고 인쇄한다 |

`[해석]` 한 문장: **"아무도 재지 않았다" 는 틀렸고, "아무도 모드 좌표에서,
방향까지, 추정기로 재지 않았다" 는 여전히 옳다.**
`[해석]` 특히 아픈 지점 — 이 논문은 `Σ` 와 모드 사상(식 16·20)을 **둘 다 손에
쥐고 있다**. `LAM_ne`·`LAM_pe` 는 `Σ` 의 대각선 하나로, `LLI` 는
`y₁₀₀C_p + x₁₀₀C_n` 이라 **비대각 성분으로** 곧바로 오차막대가 나온다.
**계산하지 않는다.** 우리가 채울 칸이 정확히 여기다.

**어휘 전수 (열네 편째)** — `identifiab*` **23**(본문 22) · `observab*` **11** ·
`unidentifiab*` **1** · `unobservab*` **1** · `CRB` **7** · `Cramer/Cramér` **5** ·
`Fisher` **3** · `sensitivit*` **13** · `covarianc*` **4**(전부 p.7) ·
`rank deficient` **1** · `linearly dependent` **1** · `nullspace` **1** ·
`expansion` **87** · `LLI` **7**(p.2·3·5·6 뿐) · `LAM` **13**(p.3·4·5 뿐) —
그리고 **`degenerac*` 0 · `uniqu*` 0 · `redundan*` 0 · `collinear*` 0 ·
`confound*` 0 · `global` 0 · `Bayes*` 0 · `uncertaint*` 0 ·
`Hessian`/`singular value`/`eigen*`/`condition number` 각 0 ·
파라미터 `correlat*` 0** (유일한 `correlat*` 1회는 p.3 "inter-correlations of
these degradation **mechanisms**" — 물리 기작).
`Fisher` 3회의 자리: p.2 §1 끝 · p.7 §5.2 첫 문장 · p.11 참고문헌 [28] Jauffret.
`Cramér`(악센트)는 **참고문헌 [27] Stoica & Ng 안에서만** 1회.

**어휘 전수 방법론 정정 (앞선 열세 편에 소급 점검 필요)** — `unobservab*` 는
문자열 검사로 **0회**로 나온다. 원인은 조판 줄바꿈 하이픈 `un-\nobservable` 이다.
하이픈 결합을 전처리에 넣으면 1회이고, 같은 이유로 `identifiab*` 22→**23**,
`observab*` 10→**11**, `expansion` 81→**87** 로 바뀐다. 독립으로 돌린 pypdf 셈과
**결합 전 아홉 항목이 정확히 일치**했으므로 추출기 차이는 아니고 **전처리 차이**다.
또한 **그림 속 글자는 세어지지 않는다** — Fig. 8(a) 에 `Unobservable` 라벨이
그려져 있으나(직접 봄) 래스터라 텍스트 층에 없다.

**논문 자신이 남긴 큰 구멍 (요약)** — (a) **`n_c`(적층 수) 값이 어디에도
인쇄되지 않는다**. 팽창 감도 스케일 `w_i = n_c t_i⁰ ξ_i` 가 여기 비례하므로
`σ_t = 5 μm` 의 상대 세기를 알 수 없고 Fig. 8 은 **재현 불가**. (b) 노이즈
`σ_V=10 mV, σ_t=5 μm` **한 점 고정**, 스윕 없음. (c) CRB 는 **fresh 1점**에서만
평가 — 열화 상태를 스윕하지 않는다. (d) 판정선 5 % 에 근거 없음. (e) 목적함수
(P) 는 mV 와 μm 를 **무가중**으로 더하고 CRB 는 `E⁻¹` 로 가중 — **가중이 서로
다르다**. (f) 저자 자신이 결론의 모형 의존성을 인정한다 — `[인쇄, p.10]`
"in practice … more non-linearities near the low DODs which results in
**better-conditioned** sensitivity matrices. Hence, the observability of the
parameters **should enhance in practice**."

**★ 그림에서만 확인한 어긋남 하나** — `[도표]` Fig. 8(d): `C_p` 는 **전압만**
시나리오에서 DOD ≈8 % 부터 **≈5.1 %** 로 5 % 판정선 **바로 위에** 붙어 ≈98 %
까지 유지된다. 본문 §6.1 이 그 98 % 를 인쇄해 놓고도 Abstract 는 ">70 %" 라고만
쓴다. **전압+팽창**에서도 `C_p` 는 DOD 0–40 % 에서 ≈5.0 % 로 판정선에 얹혀 있다.
`[해석]` 즉 헤드라인 숫자 **30 % / >70 % 는 네 파라미터 전부가 아니라 음극
파라미터(`x₁₀₀`, `C_n`)가 정하는 값**이다. Highlights 가 "graphite lithiation
state" 라고 대상을 좁혀 말한 것이 오히려 정확하고 Abstract 의 "the parameters"
가 넓다.

신설: `concepts/constrained-crb-identifiability.md` — 제약 CRB 기계(식 28–34)와,
이 계보가 `Σ` 를 구해 놓고 **대각선만 보고하는 공통 습관**, 그리고
**제약 추가(모르는 방향을 줄임) ≠ 관측 추가(정보를 늘림)** 의 구분.
갱신: `questions/pvs-sev-lli-lampe-separability.md` (Evidence For 1건 +
Status Log 2026-09-04 + sources) · `index.md`.
**건드리지 않은 것** (사용자가 이어서 고침): `syntheses/mode-identifiability-
unmeasured-lineage.md` · `comparisons/halfcell-window-parametrization-lineage.md` ·
`questions/22p-physics-or-degeneracy.md`.

## [2026-09-04] update | Mohtat 2019 원전을 읽고 **통합 논지의 Thesis 를 좁혔다**

사용자가 조판본을 주어 `[11] Mohtat et al. 2019` (*J. Power Sources* **427**,
101–111, DOI `10.1016/j.jpowsour.2019.03.104` — 1쪽 좌하단 인쇄값으로 대조)을
읽었다. digest 는 논문 에이전트가 만들었고(`raw/papers/mohtat2019_electrode-soh-
estimability-expansion.md` + 그림 9장 + 새 개념 `constrained-crb-identifiability`),
**아래 판정에 쓰인 근거는 이 위키가 원문에서 독립으로 재확인한 것**이다.

**★ 논지가 좁혀졌다.** 원래 Thesis 는 "흡수한 13편 중 그 분해가 **유일한지**를 잰
논문은 하나도 없다" 였다. **거짓이다.** Mohtat 은
- 제약 Cramér–Rao 하한을 세운다 (`𝓘_f = SᵀE⁻¹S` 식 29 · `Σ ≥ 𝒪(𝒪ᵀ𝓘_f𝒪)⁻¹𝒪ᵀ` 식 32,
  Stoica & Ng 1998),
- 구조 판정을 인쇄한다 (`[인쇄]` "If 𝒪ᵀ𝓘_f𝒪 is nonsingular, then the constrained
  problem is identifiable"),
- **축퇴를 방향까지 지목한다** — `[인쇄]` "the **first and second columns** in the
  sensitivity matrix … become **linearly dependent** … the sensitivity matrix is
  **rank deficient and the problem is unidentifiable**". 이 계보에서 축퇴의 방향을
  글자로 지목한 **유일한** 문장이다.
- 수로 낸다 — `[인쇄]` "a **threshold of 5%** is selected … feasible at about **30% DOD**".

**무너진 성분 둘 / 남은 성분 넷** (Counter-argument (f) 의 표):
거짓 = "식별 가능성을 정량한 편이 없다" · "축퇴를 지목한 편이 없다".
참 = "**LLI/LAM 좌표에서** 잰 편이 없다"(`LLI` 6회·`LAM` 13회가 전부 2–5쪽,
§5·§6·§7 에 **0회** — 파라미터는 `θ = [x₁₀₀, y₁₀₀, C_n, C_p]`) · "축퇴의 **방향을
수로** 보고한 편이 없다"(`Σ` 를 구하고 곧바로 `sqrt(diag)` 만) · "**추정기로 복원**을
검증한 편이 없다" · "**전역** 식별 가능성"(`global` **0회**).
→ 새 Thesis: **"아무도 안 쟀다" 는 틀렸고, "아무도 모드 좌표에서, 방향까지,
추정기로 재지 않았다" 는 옳다.**

**처방의 축이 다르다.** Birkl·Lin 은 "제약을 걸어라", Marongiu 는 "믿음으로
못 박아라" 인데 Mohtat 은 **"센서를 하나 더 달아라"** 다 — 전압에 셀 팽창(μm)을
둘째 채널로 더한다 (`expansion` 87회). Phase 1e·1h 가 앞의 처방을 우리 격자에서
기각했으므로 **남은 처방은 그의 것이다.** 다만 그 자신의 결론도 "팽창이 있어야
가능" 이 아니라 `[인쇄, §7]` **"전압만이면 상전이 두 개를 걸치는 넓은 SOC 구간이
필요하고, 팽창을 더하면 더 얕은 방전심도에서 가능"** 이다 — 판정 변수는 관측
종류가 아니라 **데이터 창의 폭**이다.

**매개화 장부 판정**: **Lin 이 전한 쪽이 Mohtat 자신의 표기**다. 문제 (P) 가
`θ = [x₁₀₀, y₁₀₀, C_n, C_p]` 에 `subject to, U_p(y₁₀₀) − U_n(x₁₀₀) = V_max`
**하나만** 걸고, 셀 용량은 `[인쇄]` "only the maximum voltage limit is used in the
estimation problem" 이라 **추정 후** 식 (27) 로 푼다. PyBaMM 구현본의 "양 5개 −
등식 2개" 는 같은 문제의 다른 장부. **그리고 비교표의 정정 하나** — 그 4개를
"전극 SOC 한계 4개" 로 적어 온 것은 부정확했다: SOC 한계 **2개** + 전극 용량
**2개**(Ah)다.

**★ 방법론 결함 하나 발견 — 어휘 전수의 소급 감사가 필요하다.** 조판 PDF 의
줄바꿈 하이픈을 잇지 않으면 낱말이 통째로 사라진다. 실측: `identifiab*` 22 → **23**,
`observab*` 10 → **11**, **`unobservab*` 0 → 1** (10쪽 `[인쇄]` "the parameters are
**unobservable** at low DOD regions"). 게다가 **그림 속 글자는 애초에 안 세어진다**
(Fig. 8(a) 의 `Unobservable` 라벨). **앞선 13편의 "0회" 판정은 이 두 함정을
통과했는지 확인되지 않았고**, 당시 원본 PDF 가 이 세션에 없어 재검이 불가능하다.
통합 논지 Bias Check 5 로 신설했다 — "0회" 를 "그 개념이 없다" 로 읽으면 안 되고,
논지에서 실제로 일하는 것은 개수가 아니라 본문을 읽고 적은 **"형태" 열**이다.

**새 Gap 둘**: (7) `Σ` → 모드 좌표 전파 `σ²_LLI = ∇gᵀΣ∇g` — Mohtat 이 `Σ` 와 모드
사상을 **둘 다 손에 쥐고** 계산하지 않은 한 줄이고, 우리 격자에서 바로 잴 수 있으며
Gap 4(모드 오차막대)를 닫는 길이다. (8) 팽창(부피) 축을 우리는 한 번도 안 쟀다.

갱신: `syntheses/mode-identifiability-unmeasured-lineage.md` (Thesis · §1 표에 Mohtat
행 + 하이픈 경고 · **Counter-argument (f) 신설** · Bias Check 1 닫고 2·4 보강 · **5 신설** ·
Gap 7·8 신설 · title/description) · `comparisons/halfcell-window-parametrization-lineage.md`
(Mohtat 두 행을 원전/구현본으로 재작성 + 구성 정정 + 관측 축 예외) ·
`questions/22p-physics-or-degeneracy.md` (2026-09-04 (2) 항목 4건).
lint 0 errors.

## [2026-09-04] update | Phase 1i — 22p 오차막대를 냈고, **세 막대가 하나임**을 보였다

정본 `mode-observability/results/phase1i/` · 판정문 `docs/PHASE1I_NOTES.md`.
새 시뮬레이션 없이 Phase 1c/1h 의 `J` 만 썼다. `degradation-degeneracy/` 는 읽기만.

바로 위 항목에서 연 **Gap 7**("Mohtat 이 `Σ` 와 모드 사상을 둘 다 쥐고 하지 않은
곱셈")을 우리 격자에서 했다. 우리 좌표는 모드가 파라미터 자리에 직접 있어
전파식조차 필요 없다 — `Σ = σ²(JᵀJ)⁻¹` 로 끝난다. **그것이 우리 매개화가 이
물음에 곧바로 닿는 이유**이고, Mohtat 에게는 한 줄이 더 필요했으며 그 한 줄이
인쇄되지 않았다.

**① 22p 삼중항의 오차막대 (처음)** — σ = 5 mV, CRB 하한, %p 1σ:
`LLI ±0.440 · LAM_PE ±0.401 · LAM_NE ±0.498` (σ = 1 mV 면 ±0.088/±0.080/±0.100).
**Gap 4 를 우리 쪽에서 닫는다** (논문 쪽은 여전히 안 닫혔다).

**② ★ 그런데 셋을 따로 인용하면 안 된다.** 상관이
`ρ(LLI,LAM_PE) = +0.986003 · ρ(LLI,LAM_NE) = +0.883108 · ρ(LAM_PE,LAM_NE) = +0.907473`
이고, 오차 타원체 축이 `0.755 / 0.174 / 0.046 %p` — **총 분산의 94.64 % 가 최장축
하나**에 있다. 그 축은 `(1,1,1)` 과 **4.61°**, 곧 Lin 의 null 이다.
`[해석]` **세 막대는 한 방향의 그림자 셋이다.** 그리고 이것이 `sqrt(diag)` 만
인쇄하는 관습이 가리는 것 — Mohtat 식 (33), Lin 의 `C_θ` 가 정확히 거기서 멈춘다.
**오차막대를 안 내는 것보다 더 나쁜 실패 방식이 따로 있다: 세 개를 내고 독립한
셋처럼 읽는 것.**

**③ ★ 제약 처방의 대가를 처음 수로 냈다.** 컷오프 등식을 제약으로 걸면 σ_LLI 가
0.440 → **0.051 %p** (−88 %) 로 좁아진다. 그런데 Phase 1h 가 그 등식이 참값에서
성립하지 않음을 이미 쟀다. 컷오프 상수를 pristine 에서 잡고 22p 에 얹으면 잔차
`+11.4 mV · +27.3 mV` 가 남고 제약 추정기가 그것을 모드로 떠넘긴다 (최소노름
`Δθ = G⁺r`): **`[+0.69, −8.24, −3.24] %p`, `‖Δθ‖ = 8.884 %p` — 최대 σ 의 173배**
(σ = 1 mV 면 865배). **`LAM_PE` 가 참값 12 %p 에서 −8.24 %p 어긋나고 그 값에 붙는
막대는 0.013 %p 다.** 틀린 값을 아주 좁은 막대와 함께 보고하게 된다.
Phase 1e 경계 ④ 를 수로 만든 것이고, Marongiu 가 초기값 하나로 6.38 → 14.46 % 를
겪은 것과 같은 형태의 사건이다. **Phase 1e(창 좌표)·1h(모드 좌표)에 이어 세 번째
각도에서 같은 기각.**

**④ 관측추가(Mohtat 식)는 −5 % 에 그친다** — 단 그가 실제로 더한 것은 끝점이
아니라 **셀 팽창**이고 그 축은 아직 안 쟀다 (Gap 8).

**자기 점검 하나**: 두 동작점의 `ρ(LLI,LAM_PE)` 가 소수 4자리까지 같아
(0.9860/0.9860) 캐시 오염을 의심했다. 12자리로 재확인하니 `0.986027709` vs
`0.986003353` 로 5자리에서 갈리고 열 노름도 `[9.32,8.13,3.64]` vs
`[6.91,8.48,2.43]` 로 분명히 다르다 — **우연이었다.** 출력 자릿수를 6자리로
바꿔 같은 오해가 재발하지 않게 했다.

**경계 (문서에 그대로)**: 이것은 **하한**이지 추정기 성능이 아니고
`degradation-degeneracy` 복원 결과와 섞어 인용하면 안 된다 · 등분산 가우시안
가정이다 (Cui 실측은 PE 1–12 mV / NE 8–93 mV 로 8배 비균일 — Gap 1) · 스텝 0.02
국소 선형화라 자릿수가 아니라 크기의 자리만 읽는다 · 두 동작점·한 화학.

갱신: `syntheses/...` (Gap 4 닫음 · Gap 7 결과 부착) ·
`questions/22p-physics-or-degeneracy.md` (2026-09-04 (3)) · `mode-observability/README.md`.

## [2026-09-04] update | Phase 1j — 두 정규화 환산을 세웠다. **12° 는 전류와 무관하다**

정본 `mode-observability/results/phase1j/` · 판정문 `docs/PHASE1J_NOTES.md`.
`degradation-degeneracy/` 는 읽기만 했다 (봉인 캐시 두 개를 fail-closed 로 확인).

Phase 1f·1g 가 수렴했던 **하나의 미제**(두 `x` 정규화 사이 환산 부재) 중
**1g 쪽을 닫았다.** 환산은 `src/inventory.py` 보다 곧바른 자리에 있었다 — 셀의
화학량론 창을 **봉인된 두 캐시가 양 끝에서 못 박고 있다**: 완충은
`configs/base.yaml` 의 `baseline.*_init_conc`, 완방은
`.cache/discharged_state/a8e262f7d6aa4beb.json`. 각 전극 `*_max_conc` 로 나누면 된다
(NE 는 복합이라 `src/halfcell.py:143` 과 같은 용량 가중 평균).

**환산 (전극 전체 좌표에서 본 셀의 창)**
```
PE  y₁₀₀ = 0.269999  y₀ = 0.926088  →  전극의 65.61 % 만 쓴다
NE  z₁₀₀ = 0.970083  z₀ = 0.003112  →  전극의 96.70 % 만 쓴다
```
**이 비대칭 하나가 Phase 1g 의 C 판이 왜 튀었는지를 설명한다** — 양극만 전극의
2/3 를 쓰는데 `"halfcell"` 정규화는 전체를 [0,1] 로 눌러 넣어 `LAM_PE` 감도를
1/0.656 ≈ 1.52 배로 부풀리고, 셀이 안 가는 34 %(`u_pe` 가 5.68 V 까지)를 평가한다.
음극은 96.7 % 라 거의 온전하다. 1g 가 "`LAM_PE` 열만 8.38 → 50.17 로 6배" 라고
적은 것과 방향이 맞는다 (6배 중 1.52배 말고 나머지는 정량으로 안 쪼갰다).

**검산 — pristine 재구성 vs 실제 reference 곡선 (288점)**
| reference | 평균\|Δ\| | 최대\|Δ\| | 양수 비율 |
|---|---:|---:|---:|
| `halfcell` (1g 의 C, 기각된 판) | 175.3 mV | 475.2 mV | 95 % |
| **셀 창 재정규화 (이번 판)** | **18.7 mV** | **53.9 mV** | **100 %** |

**"100 %" 가 판정이다.** 288점 전부에서 재구성한 무전류 OCV 가 측정 pOCV 보다
위에 있다 — 0.05 C 방전의 **과전압 서명**이고, 크기 18.7 mV 도 그 C-rate 에 맞다.
남은 차이는 좌표 오차가 아니라 물리다. (기각된 판은 175/475 mV 에 부호도 섞여 있다.)

**★ null 방향 — Phase 1g 의 자기 경계 ①을 철회한다**
```
A  PyBaMM 전 시뮬 · 유한 전류         12.04°
B  순수 창 대수 · 유한전류 reference   10.56°   (A→B −1.48°)
D  순수 창 대수 · **무전류** reference 12.54°   (B→D +1.98°)     A→D 순변화 +0.50°
```
1g 는 `[인용]` "B 판에도 동역학이 남아 있다 … 그래서 '12° 가 전류와 무관' 이
아니라 '모드→곡선 경로의 동역학과 무관' 이 정확한 문장이다" 라고 신고했었다.
D 판의 reference 에는 전류가 **어디에도 없고** 각이 12.54° 다. **그러므로 이제
"12° 는 전류와 무관하다. 창 모델의 구조에서 온다" 가 맞는 문장이다.**
Phase 1f 가 1e 의 한계 ②를 철회했던 것과 같은 형태의 **한계 철회**이고,
C 판의 기각은 **유지된다** (기각이 옳았고 D 가 그 자리를 대신한다).

**남은 물음**: 음극 제한과 "양극이 전극의 2/3 만 쓴다" 는 비대칭 중 어느 쪽 몫인가.
`u_min` 이 `LAM_PE` 쪽으로 가장 작게 기운 것(0.418)이 후자를 가리키지만 안 갈랐다.

**Phase 1f 는 이것으로 안 열린다** — 여기 세운 환산은 **우리 셀의** 것이고 Birkl 이
필요로 하는 것은 **그의 셀의** 창 상수다 (계속 참고문헌 [33] 필요). 다만 우회로가
생겼다: 그의 *상수* 대신 *구조*(식 7–10 의 형태)를 우리 환산으로 우리 좌표에 얹기.

**경계**: 18.7 mV 를 과전압이라 부른 것은 부호·크기 근거이지 과전압 모형으로
맞춘 것이 아니다 · 한 동작점·한 스텝·한 화학 · Phase 1h 가 잰 스텝 산포
(4.61°~21.89°)가 여기도 걸리므로 **+0.50° 자체는 의미를 못 준다**; 주장하는 것은
"전류를 빼도 각이 산포 안에서 안 움직인다" 쪽뿐이다 · 완방 캐시의 실측값을 읽었고
`_original_hardcoded_do_not_use` 는 쓰지 않았다.

같이 고친 것 — **webapp `phase_rail()` 버그**: Phase 번호를 `(\d+)` 로만 읽어
**1b~1i 여덟 개가 "Phase 1" 한 줄로 뭉개져** 있었고 README 의 `| **1e** |` 행은
아예 파싱되지 않았다. 문자열 키 + `\d+[a-z]?` 로 고쳐 11줄이 각자 산출물을 단다
(Playwright 실측, 콘솔 오류 0). Phase 1f 가 `partial`("노트만 있음")로 뜨는 것이
맞다 — 그 스크립트는 일부러 실패한 채 남긴 것이고 결과 CSV 가 없다.

갱신: `syntheses/...` Gap 2 닫음 · `mode-observability/README.md` (1j 행) ·
`docs/PHASE1G_NOTES.md` (경계 ① 철회 배너) · `docs/PHASE1F_NOTES.md` (안 열린다는 명시).

## [2026-09-04] update | Phase 1k — 축퇴는 **모드→창 층**에 있고, 그 층은 우리 것이 아니다

정본 `mode-observability/results/phase1k/` · 판정문 `docs/PHASE1K_NOTES.md`.

Phase 1j 가 남긴 물음("12° 가 창 모델의 **어느 층**에서 오나")을 `J = W·M` 으로
쪼갰다. 동작점을 **22p 근방**으로 옮겨 J·M·W 를 **셋 다 중심차분**으로 맞췄다 —
pristine 은 `−H` 조건이 없어 전방/중심이 섞이고 그 불일치가 그대로 검산 잔차로
나온다(첫 시도 0.184). 22p 에서 잔차가 0.138(스텝 0.04) → **0.068**(0.02),
비 **2.04** 로 **1차 수렴** → 잔차는 이산화 오차이고 합성은 성립한다.

**① 축퇴는 압도적으로 M 쪽이다**
```
M (모드→창)   특이값 3.2988 · 1.2276 · 0.001412   조건수 **2337.0**
W (창→곡선)   특이값 19.04 · 10.56 · 1.704 · 0.6042   조건수  31.5
J (합성·실측)  특이값 24.61 · 6.151 · 0.5103          조건수  48.2
```
곡선이 창을 못 보는 것이 아니라 **모드 셋이 창 넷으로 갈 때 이미 한 방향이 거의
죽는다.** `M` 의 넷째 행은 통째로 0 이다 (`modes_to_params` 가 `β_NE` 를 항상 0 으로
돌려준다) — 상이 창 4차원 중 3차원 부분공간이고 그 안에서 다시 2차원으로 눌린다.

**② 내가 처음에 틀린 자리 — 근사 null 뒤의 방향 비교는 하면 안 된다**
`d = M·(1,1,1)` 을 정규화해 `W` 의 약한 쌍과의 각을 재려 했는데,
`‖M·(1,1,1)‖` 은 `σ_min(M)` 의 48.6배, `‖M·u_min‖` 은 **3.0배**로 **둘 다 거의
상쇄돼 사라진다.** 그래서 그 상을 정규화한 방향은 **잔여가 정하는 잡음**이다 —
`u_min` 과 `(1,1,1)` 이 모드 좌표에서 **1.22°** 인데 상은 **82.4°** 떨어진다.
그대로 실었으면 "약한 쌍과 32.8°" 같은 **숫자처럼 보이는 잡음**을 발표할 뻔했다.

**③ 반사실 — PE 창 비대칭 가설 기각.** 평형 OCP 를 더 넓은 가짜 창으로 재정규화
(⚠ **완방 끝 `y₀` 고정 후 뒤로** 넓힌다 — 앞으로 넓히면 `y > 1` 로 표 밖에 나가
보간자가 포화된다. 첫 시도가 그래서 69° 라는 artifact 를 냈다):
`65.61 % → 1.22°` · `75 % → 1.17°` · `90 % → 1.19°`. **각이 0.05° 안에서 안 움직인다.**
(조건수는 48 → 57 로 움직이니 아무 효과도 없는 건 아니고, null 의 **방향**에만 무관하다.)

**④ 각의 띠가 또 넓어졌다.** 22p·중심차분·무전류 대수 판에서 **1.22°**.
Phase 1h 는 같은 동작점을 전방차분·시뮬 곡선으로 4.61° 로 쟀다. 판이 둘 다 다르므로
빼서 하나를 탓할 수 없지만, 관측된 산포는 **1.2°~21.9°** 로 넓어진다.

**★ 소급 경고 — 앞선 라운드에 붙는다.** 창 대수로 지은 판은 전부
`modes_to_params()` 를 통과하는데, 그 함수는 `src/fitting.py` 헤더가
**"역함수 — 테스트·진단용, 'paper' 규약"** 이라 못 박은 것이다 (그 규약 평균
|오차| **0.128**, production 의 `"derived"` 는 **0.012**). 게다가 **production 에는
모드→창 사상이 아예 없다** — 창 좌표를 직접 맞추고 모드는 사후 변환으로 얻는다.
그러므로 **Phase 1g B·C, 1j D, 1k 의 절대 각도에는 그 규약의 몫이 섞여 있고,
1g·1j 는 그것을 신고하지 않았다.** 두 문서에 배너를 달았다.
**비교는 살아남는다** — 1j 의 핵심 `B → D` 는 같은 규약·같은 스텝에서 reference 만
바꾼 짝이라 규약의 몫이 약분된다. 약해지는 것은 층을 건너는 비교(시뮬 A ↔ 대수 D)다.
그리고 `cond(M) = 2337` 을 **"우리 파이프라인이 병들었다" 로 읽으면 틀린다** —
그것은 진단용 허구의 성질이다.

갱신: `mode-observability/README.md` (1k 행) · `docs/PHASE1G_NOTES.md`·
`docs/PHASE1J_NOTES.md` (소급 경고 배너).

## [2026-09-04] update | Phase 1l — **팽창 축은 통한다.** 그리고 왜 통하는지도 나왔다

정본 `mode-observability/results/phase1l/` · 판정문 `docs/PHASE1L_NOTES.md`.

통합 논지 **Gap 8** 을 닫는다. 이 계보의 축퇴 처방 셋 중 둘(등식·0-고정)은 우리
격자에서 이미 기각됐고(Phase 1e·1h·1i / Marongiu 자신의 실측), **남은 하나가
Mohtat 의 "센서를 하나 더 달아라" 다.**

**막힌 자리와 우회**: `Chen2020_composite` 에 **전극 팽창 파라미터가 없다**
(실측 — `partial molar volume` 은 SEI 것뿐, `Cell thermal expansion coefficient`
는 열팽창). 그래서 그의 팽창 채널을 우리 셀로 **교정할 수 없다.** 그런데 교정
없이 판정하는 길이 있었다 — Mohtat 식 (39) 계열은 전부 **전극 화학량론의 고정
선형범함수**이므로, 궤적 자체의 Jacobian 을 재면 **모형 하나가 아니라 모형 족
전체**에 답한다. 화학량론은 격자의 `v_pe`·`v_ne` 를 봉인 평형 OCP 표로 역보간해
얻었다 (단조성 확인). **`modes_to_params` 를 안 거치므로 Phase 1k 의 규약 경고가
여기엔 안 걸린다.**

**★ 실측 — 채널마다 `(1,1,1)` 을 보는 정도가 완전히 다르다** (∠ 가 **작을수록 못 본다**):

| 관측 | pristine | 22p |
|---|---:|---:|
| 전압 `U_full(x)` | 12.04° | **4.61°** (거의 최약축 = 못 본다) |
| PE 화학량론 `y(x)` | 13.93° | 25.61° (자기 조건수 1726) |
| **NE 화학량론 `z(x)`** | **77.45°** | **70.53°** ← **본다** |
| `[y;z]` 통째 | 8.49° | 4.20° (**상쇄돼 다시 눈이 먼다**) |

`(1,1,1)` 방향 미분 (22p): 전압 0.826(자기 최소의 **1.25배**) · y 0.335(39.8배) ·
**z 2.015(4.73배)**.

**스칼라 팽창 `E = cosθ·y + sinθ·z` 훑기 (22p)**: θ=0° 25.61°/+11.8 % ·
30° **0.83°**/+35.2 % · 45° **1.27°**/+53.4 % · 60° 3.03°/+70.9 % ·
75° 24.50°/+87.7 % · **90°(순수 NE) 70.53°/+103.7 %**.
**균형 혼합이 가장 나쁘고 순수 NE 가 가장 좋다.** 그리고 물리가 그쪽이다 —
Gr+Si 음극은 Si ~300 %·흑연 ~10 % vs NMC 수 % 라 팽창이 **압도적으로 음극 지배**다.

**판정**: 팽창 축은 통한다. σ_min **+103.7 %** 대 컷오프 등식의 **+3~6 %**(Phase 1h)
— **20배 이상**. `[해석]` **왜 통하는지도 나왔다**: 전압은 음극의 `(1,1,1)` 응답을
**양극의 반대 응답으로 거의 상쇄**해 못 보고, 팽창은 음극만 크게 반영해 그 상쇄를
깬다. `[y;z]` 를 균형 있게 섞으면 각이 4.20° 로 다시 눈머는 것이 그 증거다.

**경계**: 이득 +103.7 % 는 **가중에 매인 수**다 (`σ_팽창` 을 모른다 — Mohtat 도 `n_c`
를 인쇄하지 않아 그의 Fig. 8 이 재현 불가다). 가중 무관한 수는 **각**이므로 그것을
인용한다 · `z` 를 직접 재는 것이 아니라 시뮬 `v_ne` 역보간이다 (실셀은 기준전극이
필요하고, **팽창의 값어치가 바로 그것 없이 그 정보에 닿는다는 데 있다**) ·
0.05 C 유한 전류라 **겉보기 화학량론**이다 · **선형 팽창 모형 족**에 한정 (Si 의 큰
이력은 사정권 밖) · 두 동작점·한 화학.

**논지에 미치는 것**: Gap 8 을 닫고 **Gap 9 를 신설**했다 — 세 처방 중 둘이
기각되고 하나가 통한다는 것이 이 논지의 실무적 결론으로 모인다. "아무도 모드
좌표에서 재지 않았다" 는 침묵의 대가가 바로 여기다: **재 보지 않으면 셋 중 어느
것이 통하는지 고를 수 없다.**

갱신: `mode-observability/README.md` (1l 행) · `syntheses/...` (Gap 8 닫음 · Gap 9 신설).

## [2026-09-04] update | Phase 1m — `n₁` 은 맞다. **계수가 틀렸다** (프레임이 정한다)

정본 `mode-observability/results/phase1m/` · 판정문 `docs/PHASE1M_NOTES.md`.
통합 논지 **Gap 3** 과 `mode-observability/README.md` 의 예고 실험 **6번**을 닫는다.

이 계보가 세 번 진술한 축퇴(`[인쇄]` Dubarry 식 (8') · Birkl §4.2 산문 · Marongiu 가
파라미터를 죽인 근거)를 **처음으로 시뮬로** 시험했다. `src/modes.py` 가 이미
`lam_ne_type="li"` 를 지원해서 (우리가 안 돌렸을 뿐) `degradation-degeneracy/` 를
**import 만** 하고 잴 수 있었다. 한 조건 ~2 s.

**① 예측대로 하면 틀린다.** `N = Q_NE/Q_PE = 0.678500` (셀 기하 계산 — 원전들은
인쇄하지 않았다. `[해석]` **1보다 작다** — 우리 셀이 음극 제한이라 모순은 아니지만
Marongiu 의 `[인쇄]` "normally bigger than one" 과 다른 영역이다).
`{LAM_Ne,li=δ}` vs `{LAM_Ne,de=δ, LLI=N·δ}` 를 돌리니 δ=0.12 에서 **평균 67.8 mV ·
최대 102.1 mV** 차이다. **대조군이 방향을 뒤집는다**:
`LLI=0` → **0.254 mV** · `0.5·N·δ` → 37.6 mV · `N·δ` → 67.8 mV.
**보정을 안 한 쪽이 가장 가깝고 보정을 키울수록 단조롭게 나빠진다.**

**② 계수를 프레임에서 다시 유도하면 맞는다.** `li` 가 `de` 보다 더 빼는 리튬은
**재료가 제거되는 프레임에서 그 재료가 쥐고 있던 양**이다. 우리 파이프라인은
열화를 **완방 프레임**에서 적용하고 (`build_overrides` 의 `[코드]` "charge_first /
완방 프레임 통일"), 그 프레임에서 음극은 거의 비어 있다 (`z_gr` = 0.001277 ·
`z_si` = 0.012396; 음극이 쥔 Li 0.0184 Ah = 총 재고 8.1053 Ah 의 0.23 %).
올바른 계수로 재면 `N·δ` 의 **1/298**, 그 값으로 다시 재면 **평균 0.048 mV** —
Dubarry 계수의 1400분의 1이고 보정 없음의 5분의 1이다.

**③ 판정**: `n₁` 의 **구조는 성립하고 계수는 프레임이 정한다.**
따라오는 것 둘 —
(a) **우리 격자에서 `lam_ne_type` 은 사실상 무효 노브다** (`de` ↔ `li` 가 0.25 mV,
우리 잡음층 1·5 mV 아래). 격자가 `de` 만 돌린 것은 **NE 에 관한 한 손해가 아니었다.**
(b) **계보에 대한 지적**: Dubarry 식 (8') 의 `LR` 은 "재료가 완전 리튬화 상태에서
제거된다" 는 **암묵 가정** 위에 있고, 그 축퇴를 진술한 세 편 중 **프레임을 명시한
편이 없다.** 프레임이 다르면 계수가 **300배** 틀린다.

**경계**: `n₂`(PE 쪽)는 **안 쟀다** — 완방 프레임에서 양극은 `y₀ = 0.926` 으로 거의
차 있으므로 **결과가 다를 것으로 예상되지만 재지 않았다.** 그러므로 (a) 를 PE 로
옮겨 읽으면 안 된다 · 한 프레임·한 화학·δ 3개 · 0.048 mV 는 `extract_curves` 의
보간 오차와 같은 자릿수일 수 있어 **"0 과 구별되지 않는다" 까지가 주장이다.**

갱신: `mode-observability/README.md` (1m 행 + 예고 실험 6 닫음) ·
`comparisons/halfcell-window-parametrization-lineage.md` (Phase 1m 배너 + `LR=N`
확인 문장 정정 + `N` 수치와 <1 사실) · `syntheses/...` (Gap 3 닫음).

## [2026-09-04] update | Phase 1m 후속 — `n₂`(PE)가 **프레임 이론의 예측을 맞혔다**

바로 위 항목의 "계수는 프레임이 정한다" 가 **반증 가능한 예측**을 낳는다:
`n₂` 는 `{LAM_Pe,li = ε} ≡ {LAM_Pe,de = ε, LLI = ε}` 이고 Dubarry 의 계수는 **1** 인데,
완방 프레임에서 **양극은 거의 차 있으므로**(`y₀ = 0.926088`, 양극이 쥔 Li
8.0869 Ah / 총 재고 8.1053 Ah) 예측 계수가 **0.997725** 다 — **NE 의 ~0 과 정반대.**

**시험 결과 (평균 |ΔV|)**: ε=0.04 → 보정 없음 **19.653 mV** · **프레임 예측 0.008 mV**
· Dubarry 계수 1 은 0.054 mV. ε=0.08 → 0.032 vs 0.058. ε=0.12 → 0.067 vs 0.152.

**예측이 맞았고, 인쇄된 계수보다 낫다** — 프레임 보정값이 정확한 1 보다 **2~7배**
더 잘 맞고, 그 차이가 곧 `y₀ = 0.9261 ≠ 1` 의 몫이다.
`[해석]` **두 전극이 정반대이고 그 차이를 프레임 점유율이 정확히 예언한다.**
이것이 "계수는 프레임이 정한다" 를 사후 설명이 아니라 **예측력 있는 진술**로 만든다.

**덤**: `ε ≥ 0.08` 에서 보정 없는 짝은 **infeasible** 이다 — `[코드]` "PE 초기농도
63522 > c_max 63104 (줄어든 PE가 완방 재고를 수용 불가 — PE-limited 영역)".
**보정 없이는 조건 자체가 물리적으로 성립하지 않는다** — `n₂` 는 선택이 아니라 필연이다.

이로써 **#120(`n₁·n₂` 를 격자에 심는다)이 닫혔다.**
(이 항목은 커밋 `b2de0763` 에서 경로 실수로 빠졌던 것을 보충한 것이다.)

## [2026-09-04] update | Birkl 매개화를 우리 셀에 이식 (Phase 1n) — 분할 판정

[[halfcell-window-parametrization-lineage]] 와
[[mode-identifiability-unmeasured-lineage]] 에 Phase 1n 실측을 반영했다.
사용자가 내 거절("[33] 없이는 계수를 지어 넣게 된다")을 반려한 데서 시작했고,
**그 반려가 옳았다** — 계수를 지어 넣지 않는 길이 있었다.

**① [[birkl-ocv-degradation-diagnostic]] 전사에 대한 정정.** 규약 16가지를
전수(PE 방향 × NE 방향 × 식 (8) `+1` 위치)하니 **4개 통과**. 전사대로도 근이
**있다**(`Δx_EoD = +1.0`) — `mode-observability/docs/PHASE1F_NOTES.md` 의
"근이 없다" 는 **탐색 구간 artifact** 였고 철회했다. 다만 그 근은 PE 창을
**폭 2** 로 만들고, 원인은 두 정규화 사이 환산도 NE 축 방향도 아니라
**식 (8) 의 `+1` 이 식 (10) 에 짝이 없는 비대칭**이다. 대칭이면 두 창이 정확히
`[0,1]` 이다. **참고문헌 [33] 은 필요 없었다.**

**② 축퇴에 대한 실측.** 그 매개화의 3-모드 Jacobian 에서 가장 안 보이는 방향이
**(1,1,1) 에서 86.13°** — 우리 자유 창 좌표(10.56°)와 정반대이고, 심판으로 쓴
**실제 시뮬 Jacobian 은 11.36°** 다. `[해석]` **매개화가 축퇴를 보이거나 감춘다.**
이것이 "축퇴가 세 번 인쇄되고 세 번 계산되지 않았다" 에 기전 후보를 준다 —
계산하지 않은 것이 게으름이 아니라 **좌표의 성질**일 수 있다 (후보이지 증명 아님).

**③ 분할 판정 — 그가 이기는 축이 있다.** 열별로 시뮬과 대조하면 Birkl 의
`LAM_PE` 열은 **cos +0.969** 로 거의 완벽하고, 같은 열에서 우리
`modes_to_params` 는 **−0.492** 로 반대로 움직인다. "누가 맞았나" 가 아니라
**"어느 축에서 맞았나"** 가 옳은 질문이다.

**④ 이 실험이 스스로 신고한 것.** 두 매개화 모두 시뮬 Jacobian 과 열 상대오차
190~220 %(최적 배율을 빼도 잔차 97 %)이고, 내가 고른 이식 검산 문턱(60 mV)이
미분되는 신호(7.66 mV)보다 8배 컸다 — **게이트 구실을 못 했다.** 그러므로 ②가
지지하는 것은 **"u_min 이 (1,1,1) 근방인가" 라는 이분법뿐**이다.
[[dubarry-mechanistic-mode-synthesis]] 쪽 `n₁·n₂` 결론(Phase 1m)은 영향받지 않는다.

정본 `mode-observability/results/phase1n/` · `docs/PHASE1N_NOTES.md`.

## [2026-09-04] ingest | Lee et al. 2020 — Estimation Error Bound of Battery Electrode Parameters With Limited Data Window (IEEE TII 16(5) 3376–3386)

Lin & Khoo 2024 가 `[15]` 로 지목한 "Fisher 로 식별 가능성을 정량한 선행자" 의
나머지 한 편. Mohtat 2019 `[16]` 의 자매편이며 **Mohtat 이 공저자**, 같은 UMich
그룹 + Samsung SDI 공동연구. digest:
`raw/papers/lee2020_estimation-error-bound-limited-data-window.md` (821줄).
그림 10장 크롭 중 8장(Fig. 1–7, 10)을 직접 봤고 Table I–IV 는 래스터라
쪽 렌더(p.4·7·9)로 읽었다. Fig. 8 은 안 봤다.

**판정 1 (좌표)**: `θ = [y₁₀₀, C_p, x₁₀₀, C_n]` — **전극 파라미터 좌표.
모드 좌표 아님.** Table II–IV 열 머리가 그대로 이 넷이다. 식 (10)–(12) 로
`LLI`·`LAM_PE`·`LAM_NE` 사상을 **정식으로 인쇄해 놓고**, 그 좌표의 오차막대는
논문 전체에 **0개**다.

**판정 2 (비대각)**: **이 계보 최초로 부분 예.** Fig. 7 이 4개 파라미터의
**6개 쌍 전부에 95 % 오차 타원**(제약 유/무 2종)을 그리고, p.8 이 산문으로
`[인쇄]` "a **strong correlation** … among the parameters from the same
electrode … the parameters from the different electrodes do not show any
correlation" 이라 적으며, 식 (26) `σ_y α = σ_x β` 로 두 막대의 비를 닫는다.
**단** 수치 ρ 0회 · 창은 DW-deep 하나뿐(가장 좋은 창) · **모드 좌표 전파 없음**.
→ 위키 문장 정정: "대각선만 인쇄한다" → **"그림으로 한 번 보였으나 수치로
인쇄한 적 없고 모드 좌표로 전파한 적 없다"**.
**본문↔그림 어긋남 1건**: `(e_Cp, e_x₁₀₀)`(다른 전극 쌍) 타원이 축 정렬이
아니다(`[도표]`, 부호 −) — 본문의 단언은 4개 다른-전극 쌍 중 둘만 보고 한 것.

**판정 3 (창)**: **DOD 구간** `DW = [Q_s, Q_e]`, `Q` = 완충에서의 방전 Ah.
네 창 `[인쇄, Table IV]` shallow `[0.0,0.2]` · medium `[0.3,0.7]` ·
non-full `[0.1,0.5]` · deep `[0.0,0.9]`. 처방 `[인쇄, p.10]` σ̂ = 10 mV,
목표 10 %, 95 % → **DOD = [0.35, 0.73]** (Mohtat 의 "DOD 30 %" 는 폭만, 이 편은
폭+위치).

**판정 4 (어휘 전수, 본문 p.1–10)**: `identifiab*` **16** · `estimab*` **0** ·
`degenerac*` 0 · `Fisher` 3 · `observab*` **1**(LFP 가정 문장뿐) ·
`unobservab*` 0 · `uniqu*` 2 · `redundan*` 1 · `ill-condition*` 0 ·
`condition number` 0 · `sensitivit*` 4 · `Cramer` 3(본문은 악센트 없음) ·
`covarianc*` 2 · **`correlat*` 3** · `global` **0** · `LLI` 6 · `LAM` 8 ·
`expansion` 1(Taylor 전개, 셀 팽창 아님).
**⚠ 새 조판 함정 실측**: IEEE 조판의 `ﬁ` 합자 때문에 정규화 없이 세면
`identifiab*` 이 **16 → 0** 이 된다 (Mohtat 의 하이픈 함정의 사촌). 두 정규화를
모두 걸어야 한다.

**판정 5 (LLI·LAM 위치)**: **p.1(인쇄 3376) 서론 각 1회 + p.3(인쇄 3378)
§III-A 에 LLI 5·LAM 7. 끝.** §IV 결과·§V 검증·§VI 지침·§VII 결론에 **0회**,
그림·표 라벨에도 0회.

**덤으로 건진 것**: (a) `[인쇄, p.3]` "out of 100 randomly generated start
points … **55** converged to the same solution" → **다봉성 45 %의 야생 실측**.
(b) `[인쇄, Table II↔III]` `V_max` 등식은 `y₁₀₀` 를 2.5 → **0.030 %** 로 83배
줄이는데 **`x₁₀₀` 3.0 → 3.0, `C_n` 3.9 → 3.9 로 NE 는 전혀 안 줄인다** —
"제약은 정보를 만들지 않는다" 의 깨끗한 수치. (c) `[인쇄, Fig. 9 라벨]`
DW-shallow 에서 `C_n` 막대 **5e3 %**.

갱신: `concepts/constrained-crb-identifiability.md` (Lee 2020 행 추가 +
"대각선만" 일반화 정정 + 제약 비대칭 수치 + 창 이동 행) ·
**신규** `concepts/data-window-identifiability.md` (제약 추가·관측 추가와
구분되는 셋째 조작) · `index.md`.

## [2026-09-04] update | Lee 2020 을 논지·비교·22p 카드에 반영 (에이전트 보고를 독립 검증한 뒤)

paper-curator 가 digest 를 만들었고, 이 항목은 **그 보고를 원문으로 다시 확인한
뒤** 금지 파일 3종(syntheses · comparisons · questions)에 반영한 기록이다.
에이전트 보고를 그대로 옮기지 않았다.

**독립 검증한 것** (`[재현]`):
- 어휘 census 를 원문에서 다시 셌다 — 18개 항목 전부 일치. 본문 `identifiab*`
  **16** · `estimab*` 0 · `degenerac*` 0 · `global` 0 · `correlat*` 3 ·
  `LLI` 6 · `LAM` 8. (내 첫 집계는 17이었는데 1건이 저자 약력 p.11 의 것이라
  본문 기준 16이 맞다.)
- **합자 함정 확인** — 정규화 없이 `identifiab` **0회**, 합자(U+FB01)를 풀면 16회.
  그 PDF 한 편에 U+FB01 이 **104회**. 하이픈 함정보다 심하다(전량 소실).
- 쪽 대응 PDF p.i ↔ 인쇄 3375+i **11쪽 전부 확인**.
- **Table II·III·IV 를 직접 읽었다** (텍스트층에 없다 — 래스터라 230 dpi 렌더).
  `y₁₀₀` 2.5 → **0.030 %** 인데 `x₁₀₀` 3.0 → 3.0, `C_n` 3.9 → 3.9 **불변**.
  Table IV 네 창의 범위·오차 12개 값 전부 일치.
- 인용 문장 8개 원문 대조 — 55/100 다봉성, DOD [0.35,0.73] 포함 전부 확인.
- **Fig. 7 의 어긋남을 직접 재현했다.** 다른 전극 쌍 `(e_Cp, e_x₁₀₀)` 패널의
  타원이 축 정렬이 아니고 부호가 **음**이다 — 확대 육안 + 화소 공분산 2개 분할
  (`−0.128`, `−0.171`)이 일치. 대조군도 맞는다(같은 전극 `+0.589`, 다른 전극
  `+0.011`). **경계**: 그려진 등고선의 화소 공분산이지 추정량 `ρ` 가 아니다 —
  부호와 비영까지만 주장한다.
  (내 첫 k-means 분할은 타원 하나를 두 군집으로 쪼개 부호가 뒤집혔다. 폐기했다.)

**반영**:
- [[mode-identifiability-unmeasured-lineage]] — Thesis 두 번째 좁힘 배너,
  §1 표에 Lee 2020 행, **합자 함정 경고**(하이픈 경고 옆), **반론 (g)** 신설,
  (f) 표 4행 정정. `[해석]` 두 반례가 같은 방향으로 민다 — Thesis 를 무너뜨리는
  게 아니라 **"모드 좌표에서" 라는 정어에 무게를 몰아준다.**
- [[halfcell-window-parametrization-lineage]] — 비교표에 Lee 2020 행,
  **"네 번째 축: 관측 창의 위치"** 절 신설. 폭이 같은 두 창에서 NE 오차가
  2배 차이다 (Table IV).
- [[22p-physics-or-degeneracy]] — **다봉성 야생 실측**(45 %가 다른 해)과
  CRB 가 국소 도구라 그 45 %를 못 담는다는 함의. 경계도 같이 적었다.

정본은 원전 PDF 와 `wiki/raw/papers/lee2020_…md`. lint 0 errors.

## [2026-09-04] update | 정정 — Fig. 7 "본문-그림 어긋남" 을 철회하고 진짜 발견으로 바꿈

**앞 항목(같은 날)에서 내가 올린 발견 하나가 틀렸다. 철회한다. 원전이 옳다.**

**틀린 주장**: [[data-window-identifiability]] Fig. 7 의 `(e_Cp, e_x₁₀₀)` 패널이
다른 전극 쌍인데도 타원이 기울어 있으므로 본문("다른 전극끼리는 상관 없음")이
자기 그림에 반박당한다 — 고 적었다.

**왜 틀렸나**: 그 패널에서 **무제약(파랑) 타원과 제약(노랑) 타원이 거의 겹친다.**
확대해 본 기울기는 **노랑(제약)** 것이었고 파랑은 노랑에 가려 조각나 있었다.
근거로 든 화소 공분산(−0.128 · −0.171)은 **가려진 조각의 통계**였고, 그 방법
자체도 편향돼 있었다 — 그려진 곡선을 호길이로 표집하면 평탄한 부분이 과대표집된다.

**제대로 다시 잼**: 신뢰타원의 세로 현 중점이 직선 `y = (ρ·σ_y/σ_x)x` 위에 있음을
이용해 `ρ = m·(h_x/h_y)` 로 냈다 (축 눈금 환산이 소거되고 표집 편향에 강하다).
가림 검사(행마다 두 갈래가 있는 비율)도 붙였다. **무제약 결과**: 같은 전극 PE
**+0.644**, 다른 전극 네 쌍 **+0.013 / −0.075 / +0.060 / −0.039** — 전부 |ρ|<0.08.
`[인쇄]` "the parameters from the different electrodes do not show any
correlation" 은 **맞는 문장이었다.**

**대신 같은 방법이 진짜 발견을 줬다 — 제약이 만드는 축퇴가 그림에 있다.**
노랑(제약) 타원: `(e_Cp, e_x₁₀₀)` **−0.469** · `(e_Cp, e_Cn)` **+0.350** ·
`(e_x₁₀₀, e_Cn)` **−0.953**. 무제약에서 0 이던 전극 간 상관이 제약을 걸면
살아난다 — 원전이 식 (26) 과 p.7 산문으로 **예고한** 바이나 **크기를 인쇄하지는
않는다.** 그리고 `−0.953` 은 이 계보에서 가장 선명한 축퇴 서명이고, Table II→III
에서 `x₁₀₀` 3.0→3.0 · `C_n` 3.9→3.9 로 **전혀 안 줄어드는 이유**를 그림으로
설명한다 (제약이 PE 를 못 박고 NE 쌍은 1차원 골짜기를 따라 미끄러진다).

**Fig. 8 도 마저 봤다** (앞 항목에서 에이전트가 캡션으로만 기록한 그림).
`[도표]` (a) 의 적합 잔차가 **백색도 등분산도 아니다** — 매끈한 혹 서너 개의
구조적 곡선(−0.007…+0.006 V)이고 방전 끝에서 **−0.019 V** 까지 부푼다.
원전의 오차한계 전체가 `σ̂ = 10 mV` 등분산 백색 가정 위에 있으므로,
**Gap 1 이 "σ 값을 모른다" 에서 "σ 가 상수라는 형태가 틀렸을 수 있다" 로 격상**됐다.

**Bias Check 6 신설** — 실패의 구조를 남겼다. "독립 검증했다" 고 적었지만 실제로는
**같은 결론을 더 나쁜 방법으로 재확인**한 것이었고, 두 관측이 **같은 실패모드**
(파랑/노랑 미구분)를 공유했다. 규칙 셋을 명시했다: 가림 검사 필수 · 방법이 다를
때만 독립으로 셈 · **원전이 스스로 예고한 것을 원전에 대한 반증으로 쓰지 않는다.**

**측정 못 한 것**: 무제약 NE 쌍 `(e_x₁₀₀, e_Cn)` 은 노랑에 완전히 가려 불가.
Fig. 8(b) 의 전극 이용률(우리 Phase 1j 의 65.61 %/96.70 % 대응물)은 범례 색
견본과 점선 끝점이 섞여 **신뢰할 수치가 안 나와 적지 않았다.**

## [2026-09-10] ingest | Schmitt et al. 2022 — Si/graphite half-cell OCP 형상 변화와 열화 모드 (JPS 532, 231296)

사용자가 **MATLAB electrode balancing 코드(5-파라미터 `[a_PE, b_PE, a_NE, b_NE,
γ_Si]`)의 α·β 검증**을 준비하며 지목한 논문. 이 논문의 모델이 정확히 그
5-파라미터다 — 그래서 digest 의 무게중심을 "무엇을 발견했나" 가 아니라
**"우리 코드가 깔고 있는 전제가 어디서 깨지는가"** 에 뒀다.

**raw**: `raw/papers/schmitt2022_sic-ocp-shape-change-degradation-modes.md`
(sha256 봉인, 페이지·절별 STANDALONE 해체분석 16절). 크로핑
`raw/figures/schmitt2022_sic-ocp-shape-change-degradation-modes/` — **fig 1–8
전부를 Read 로 직접 보고** 썼다 (표 1장만 PDF 텍스트로).

**핵심 (사용자 4문항)**:
1. **전제가 깨지는 지점** = 음극이 **blend(Si/graphite)** 일 때. Si 가 graphite
   보다 빨리 죽으면 `γ_Si` 가 바뀌고 blend OCP 는 두 성분 곡선의 **역함수
   합성**이라 **모양 자체**가 변한다 — α·β 아핀 변환으로는 표현 불가.
   정량 지표는 곡선 오차가 아니라 **`γ_Si` 9.52 % → 5.55 %** (초기의 58 %).
2. **처방** = 곡선을 다시 재는 게 아니라 **`γ_Si` 를 다섯 번째 자유 파라미터로**
   두고 4개 정렬 파라미터와 동시 최적화. 대가: 자유도 4→5 + 저자 스스로
   "같은 서명" 이라 인정한 `(α_an, γ_Si)` 축퇴를 **재지 않음**.
3. **정의식·좌표 규약**을 전부 옮겨 적고 **수치로 검산**했다 —
   `C_lit = (α_cat + β_cat − β_an)·C_full` (★ LLI 는 `α_an` 에 **무관**),
   `LAM = 1 − α·C_full/(α_ini·C_full,ini)` (★ `C_full` 이 반드시 들어간다).
   이 두 식으로 논문 Fig. 8 수치가 재현된다 (digest §11.3).
4. **검증**: 모드의 ground truth **없음**. 있는 것은 OCV RMSE < 12 mV,
   half-cell RMSE < 6.9 mV, `γ_Si` 두 경로 교차일치 < 0.8 pp(단 7/7 점 계통
   편향), 질량 정합 < 6 %. **오차막대 0개, aging state 당 셀 1개.**

**★ 이 저장소에 가장 날카로운 것**: 같은 데이터·같은 추정기에 **음극 곡선만**
바꾸면 LAM_an 15.5 ↔ 13.1 %, LAM_cat ≈2.3 ↔ ≈6.5 %, LLI ≈13.2 ↔ ≈14.2 % 로
갈리는데 **OCV RMSE 는 9.9 ↔ 8.2 mV** 다. "충전 종료를 제한하는 전극" 이라는
정성 결론까지 뒤집힌다. 원전은 `identifiability`·`degeneracy` 를 **한 번도 쓰지
않는다**.

**본문↔그림 불일치 1건 발견**: §4.5 의 "aged anode curves … 15.5 % LAM_an"
문장이 Fig. 8(a)(≈13 %) 및 같은 절 앞부분(13.1 %)과 모순 — pristine 값을 잘못
옮긴 것으로 보인다. 그 문장만 인용하면 논문의 논지와 **정반대** 값을 인용하게
된다 (digest §11.1).

**컴파일**:
- 신규 concept [[halfcell-ocp-shape-invariance]] (index 등록).
- [[halfcell-window-parametrization-lineage]] — Schmitt 행 추가 + 새 절
  "**다섯 번째 축 — 반쪽전지 곡선 자체를 매개화한다**" (앞의 세 처방은 자유도를
  줄이고 이것은 늘린다).
- [[22p-physics-or-degeneracy]] — Evidence For 1건 + Status Log 1건.
  ★ 카드에 새 축을 달았다: **좌표의 불완전성**. 우리 합성 truth 는 생성·적합이
  같은 OCP 함수를 쓰므로 형상 불변이 **정의상 참** → **우리가 재는 축퇴는
  이상적 조건의 하한**이고 실셀에선 형상 오설정 편향이 더해진다.
- [[mode-identifiability-unmeasured-lineage]] — §8 신설(모드 좌표에서의 두 번째
  "재지 않은 대가" 실측), 계보 14편 → **15편**.

`python3 wiki/tools/lint.py` → **0 errors** 확인.

## [2026-09-10] ingest | Natterer et al. 2026 — 기준전극 half-cell 분해 측정과 anode 전위 (JPS 678, 240036)

PDF 16쪽 전문 + 그림 10장(부록 2장 포함)을 **전부 직접 판독**하고 페이지/절별
STANDALONE digest 를 봉인했다 (`raw/papers/natterer2026_re-halfcell-anode-potential-aging.md`,
sha256 `6a1ae22e…`). 크로핑: `raw/figures/natterer2026_re-halfcell-anode-potential-aging/`
(도구가 fig 8 + tab 1, **부록 `Fig. A.1`/`A.2` 는 캡션 정규식이 못 잡아 이 세션에서
따로 잘라 `fig_A1.png`/`fig_A2.png` 로 추가** — `figures.json` 은 불변층이라
덧쓰지 않았고 A1/A2 항목이 없다).

**왜 이 논문인가**: 우리가 찾던 "손으로 맞춘 α·β 를 검증할 독립 근거" 의 **형태**가
여기 있다 — LTO 기준전극으로 1000 사이클 in-situ half-cell 전위를 찍고,
**수치 최적화 없이** DVA 특징점 산술(식 1–4)만으로 LLI·LAM_neg·LAM_pos 를 낸다
(`[인쇄, §3.1]` "eliminates numerical fitting procedures"). 새 개념 페이지
[[reference-electrode-halfcell-dma]] 에 절차·대가 6개·심사 기준 2개를 고정했다.

**가장 무거운 발견** `[재현]`: 500 EFC 실측 삼중항 `(LLI, LAM_pos, LAM_neg) ≈
(9.3, 8.1, 8.2) %` 를 [[np-lip-ocv-reparametrization]] 좌표로 옮기면 `r_N/P` 0.11 %,
`z₀⁺` 1.31 % 이동뿐 — **1년치 열화가 full-cell OCV 형상이 거의 못 보는 방향을 따라
갔는데 half-cell 채널은 그것을 갈라서 보고한다.** [[22p-physics-or-degeneracy]] 의
Evidence Against 에 넣었다 (오차 막대 없음·셀 1개·화학 상이·반사실 대조군 부재의
범위 한정 4개와 함께).

**인용 가치 최상의 저자 진술** `[인쇄, §3.3.2]`: "as of today, **no such parametric
analyses exist for the presented model or comparable ones in the literature**" —
이 계보에 민감도·식별 가능성 분석이 없다는 것을 2026년 4월 게재 논문이 스스로
확인한다. 저자들은 "compensating parameters" 라는 말도 쓰고 "sensitivity results
inform but do not fully resolve identifiability" 로 둘을 구분한다.

[[pvs-sev-lli-lampe-separability]]: Evidence Against 1건(부호가 아니라 **모양**이
다른 관측 쌍 — LAM 은 수직 평행이동, 양극 저항은 창 절단) + Gap 2건(기준전극
**위치**가 20 mV 를 흔든다 · 한 셀 안에서 두 전극 저항 변화의 **부호가 반대**:
양극 +52 %, 음극 −26 %).

**본문 서술과 그림이 어긋난 것 2건** (digest §11-8 에 기록):
(a) Fig. A.2 의 음극 DC 저항은 본문의 "relatively constant" 가 아니라 **−26 % 단조 감소**,
(b) Fig. A.1 의 "good agreement" 는 전위 곡선에서만 성립하고 **양극·full-cell DVA
에서는 어긋난다** — 판정하려던 대상(노화된 NMC-811 OCP 형상 변화)이 바로 미분
축에서만 보이는 성질이다. 이 두 번째 건은 같은 날 흡수된
[[halfcell-ocp-shape-invariance]] 와 직접 맞물린다 (그쪽은 Si/Gr blend 음극,
이쪽은 Ni-rich 양극).

**미실행 후속 (값싸다)**: 같은 PyBaMM 모델에서 **half-cell 항만 뺀 적합**을 돌려
원문의 가장 강한 반사실 주장("RE 없었으면 양극 저항 증가가 음극에 오귀속됐을 것")을
정량화하는 것 — 원문에 대조군이 없다.

`python3 wiki/tools/lint.py` → **0 errors** 확인.

## [2026-09-11] ingest | Wang (Xiong) et al. 2025 — Aging-induced, rate-independent lithium plating: a complete mechanism analysis throughout the battery lifecycle (Applied Energy 393, 126094)

사용자가 올린 세 편(16·19·20) 중 **19번**. `bms-balancing/` 의 새 독자 모델 요구서
(관측 → 후보 원인 → 구분 시험 → 채택 기준 → 한계)를 쓰는 단계라, digest 의 무게중심을
"도금의 기전" 이 아니라 **"아핀 α·β 적합이 못 맞추는 잔차가 나오면 무엇을 의심하고
어떻게 가를 것인가"** 에 뒀다.

**raw**: `raw/papers/wang2025_aging-induced-rate-independent-li-plating.md` (sha256
봉인, 절별 STANDALONE 해체분석 13절 + 공백 G1–G13). 크로핑
`raw/figures/wang2025_aging-induced-rate-independent-li-plating/` (fig 12 + tab 3) —
**Fig. 2, 4, 5, 6, 7, 9, 10, 11, 12 의 9장을 Read 로 직접 보고** 썼다 (Fig. 1·3·8 은
도식·SEM 이라 안 봤고, 표 3장은 PDF 텍스트로).

**논문이 한 것**: 1.1 Ah LFP/graphite 17 셀·6 조건 사이클 중 **10 셀(58.8 %)** 에서
노화 후반 0.05 C 의사-OCV 의 **충전 말단에 새 평탄역**(`[도표]` ≈3.46 V), **방전
시작에 짝 평탄역**(≈3.40 V), dV/dQ 에 **원래 없던 봉우리**가 생긴다. 분해한 음극
반쪽전지를 0 V 아래로 6 h 과방전시켜 도금 구간 전위(≈−0.015 V)를 직접 재고, 원인을
과전위가 아니라 **`Q_NE < Q_Li`** (LAM_NE 가 리튬 재고를 밑돎) 로 확정 — 그래서
"rate-independent". 아핀 4-창 적합이 이 어깨를 못 맞추자(Fig. 4b) 음극 곡선을 DV
극값 4개로 5 구간으로 잘라 **구간별 스케일**(자유도 4 → 8, GA) 을 두고 RMSE 2.7–9.1
mV 를 얻는다. 모드 궤적(Fig. 12)에서 `Q_NE` 가 `Q_Li` 를 가로지르는 곳이 용량
변곡점과 겹친다.

**우리 축에 걸린 것 셋**:
1. **모드 3개 밖의 네 번째 칸.** 원전 정의(식 3·6·7)로 회계를 재구성하면 가역 도금은
   **LLI 도 LAM 도 아니다** (용량에는 들어가고 `Q_NE` 에는 안 들어간다); 원인만
   LAM_NE, 비가역분만 LLI. 4-창 모델에는 이 칸이 없다.
2. **좌표의 불완전성 두 번째 야생 사례** (첫째는 2026-09-10 Schmitt, blend). 순수
   graphite 에서도 도금이 생기면 아핀 변환 밖으로 나간다. 처방은 또 "늘리고 안
   잰다" — `identifiab*`·`uniqu*`·`uncertaint*`·`error bar` **전부 0회**.
3. **식별 국면 전환의 야생 궤적** `[도표]`: 음극 0 V 교차점이 SOH 100 → 57.1 % 에
   걸쳐 full-cell SOC **1.08 → 0.88** 로 창 밖에서 안으로 들어오고, 그 경계에서 추정
   `Q_NE` 가 100–300 사이클에 ≈0.1 Ah **계단**으로 떨어진다. 원전은 물리로만 읽지만
   "창 밖 가장자리의 약한 식별 → 안으로 들어오며 강한 식별" 로도 읽힌다
   ([[data-window-identifiability]] 의 기제, 전극 창이 움직인 판).

**원문 안의 불일치 2건** (digest §9.5): (a) §4.3 "decreasing ratio of lithium
inventory-to-anode capacity" 인데 Table 3 의 `Q_Li/Q_NE` 는 `[재현]` 0.941 → 1.085 →
1.109 → 1.165 로 **증가** (도금 조건이 바로 이 비가 1 을 넘는 것); (b) Fig. 4(a) 의
`Q_NE/Q_Li ≈ 1.25` vs Table 3 의 1.063 — 셀 미표기. 그리고 식 (6) `K_NE =
max(SOC′(SOC′ ≥ 0))` 는 인쇄된 대로는 뜻이 안 통한다 (G3).

**LFP 경계**: 평탄 양극은 창 상단을 컷오프에 고정하고 하단을 창 밖에 둔다 →
`Q_Li = (1 − S_NE)·Q_Full` 로 `Q_Li` 는 식별되지만 **`Q_PE` 는 구조적으로 비식별** —
원전이 `Q_PE` 를 어디에도 인쇄하지 않는 것과 정합. NMC 로 옮기면 사라지는 축퇴라
22p 에 직접 대지 않는다.

**컴파일**:
- 신규 concept [[rate-independent-li-plating-signature]] — 서명 S1–S7, 모드 회계,
  요구서용 구분 시험 T1–T5 와 채택 기준 (index 등록, 30 페이지).
- [[halfcell-window-parametrization-lineage]] — Wang (Xiong) 2025 행(8, 제약 0) +
  새 절 "**여섯 번째 축 — 반쪽전지 곡선을 구간별로 매개화한다**".
- [[mode-identifiability-unmeasured-lineage]] — 표에 행 추가, 계보 15 → **16편**.
- [[22p-physics-or-degeneracy]] — Evidence For 1건(창 밖 가장자리의 약한 식별과
  계단, 범위 한정 3개) + Status Log.
- [[pvs-sev-lli-lampe-separability]] — Gap 1건(새 봉우리 출현이 순서 기반 feature 를
  깨고, 2 mV 동역학 하강이 SEV 축에 걸린다) + Status Log.

**미실행 후속 (값싸다)**: 합성 truth 에서 `a_NE` 를 창 밖 → 안으로 움직이며
4-파라미터 적합의 `a_NE` 오차막대가 **불연속으로 줄어드는 지점**이 있는지; 8-파라미터
구간 스케일링의 `JᵀJ` 조건수·null 방향.

`python3 wiki/tools/lint.py` → **0 errors, 0 warnings** 확인 (pages 30, raw files 25).

## [2026-09-11] ingest | Cui et al. 2026 — A direct diagnosis method for degradation modes of LiFePO4 batteries based on mechanism analysis (Applied Energy 426, 128689)

사용자가 올린 세 편 중 **20번**. 같은 제1저자의 `cui2024_electrode-utilization-…` 과는
다른 논문 (Jiangsu Univ., L. Wang 그룹). digest 의 무게중심은 두 가지 — **(a) "direct"
가 적합 없이 무엇을 재는가와 그것이 LFP 에서만 되는 이유, (b) 정답 라벨이 measured
인가 fitted 인가.**

**raw**: `raw/papers/cui2026_direct-diagnosis-lfp-degradation-modes.md` (sha256 봉인,
절별 STANDALONE 해체분석 15절 + 공백 G1–G16). 크로핑
`raw/figures/cui2026_direct-diagnosis-lfp-degradation-modes/` (fig 17 + tab 6; **도구가
Fig. 6 과 Fig. 7 을 한 장으로 잘랐다** — `figures.json` 에 `f7` 없음, 불변층이라
덧쓰지 않음). **Fig. 3, 4, 6(+7), 8, 9, 10, 11, 12, 14, 15, 17, 18 의 12장을 Read 로 직접
보고** 썼다 (Fig. 1·2·5·13·16 은 사진·도식·XRD 패턴·중복 통계·순서도라 안 봤다).

**논문이 한 것**: 20 Ah 각형 LFP/graphite 10 셀(8 노화 + 2 기준). (i) C/25 방전
의사-OCV 를 `X1–X4`(양극 가용 용량 · 음극 가용 용량 · 오프셋 `LAM_liNE − LAM_dePE +
LLI` · 방전 종료 음극 리튬화도) 로 PSO 적합 → 파괴 확률 균일 가정(식 9)으로 다섯 모드로
되풀기 (LAM_PE ≈ 0, LAM_NE 최대 2.83 Ah, LLI 3.40 Ah). (ii) **재료 라벨**: 코인 반쪽전지
용량(LAM_NE, 4 셀, 최대 편차 1.35 %) · XRD LiC₆/LiC₁₂ 세기비(LLI, 4 셀, 1.68 %). (iii) OCV
적합값을 참조로 만든 가상 배터리 스윕에서 **Peak B 면적은 LLI 불변·LAM_NE 감소, Peak C
면적은 LLI 지배** → 적합 없는 직접 진단식 `LAM_NE = ΔArea_B/Area_B`, `LLI′ = ΔArea_C/
Q_fresh` (OCV 적합 대비 1.79 / 1.62 %). (iv) C-rate(계수 1/1.19/1.26/1.47)·온도(0–55 °C)·
18650 적응성.

**우리 축에 걸린 것 넷**:
1. **왜 LFP 에서만 되는가** `[해석]`: 평탄 양극 → full-cell dQ/dV 봉우리 = 음극 stage
   용량 그대로 → **Peak C 절대 면적 감소(Ah) = LLI(Ah)** 항등식 (원문의 식 21 → 23
   "보정" 이 바로 이것). NMC 에서는 봉우리가 양극·음극 합성이라 깨지고, Si/Gr 은 위치
   불변이 깨지며, 무릎 이후는 새 봉우리(19번 논문)가 생긴다.
2. **평탄 양극이 만드는 `(X1, X3)` = LAM_PE ↔ LLI 축퇴** `[해석]` (원문 식 1·5·20 에서
   유도): 관측이 구속하는 것은 `X1 − X3 = Q_EOC` 뿐. Fig. 3(a) 의 `X1` 이 8개 SOH 에서
   `[도표]` 정확히 같은 높이 = PSO tie-break 의 징후. 그런데도 LLI 가 XRD 와 맞은 이유는
   **코인셀·XRD 가 LAM_PE ≈ 0 을 독립으로 확인**했기 때문 — 이 논지의 처방("관측을
   늘려라")이 작동한 형태이며 저자는 그 구조를 모른다.
3. **줄였다가 늘린다**: 비유일성을 인쇄하고(`[인쇄]` "To obtain unique parameter
   results … recombined") 7 → 4 로 줄인 뒤 **사전믿음 등식**으로 li/de 를 다시 가른다 —
   `LAM_liNE/LAM_NE ≈ 0.36` 은 `[재현]` 순환 구간 중점 0.39 의 구성. XRD 검증은 총량뿐이라
   분할은 검증되지 않았다. 창 매개화 계보에 "등식의 새 변종".
4. **정답 축의 층위**: OCV 법 ← 재료 라벨(4+4 셀, XRD 보정용 LAM_NE 는 **다른 셀**
   코인셀의 선형 보간, 오차 막대 0, 기준 셀 둘) · IC 법 ← **OCV 적합값** · 18650 ← 각형
   OCV 적합값의 SOH 보간. "1.79 %" 를 인용할 때 축을 반드시 붙인다.

**본문 서술과 그림이 어긋난 것 3건** (digest §11.4): (a) 결론 "LAM_NE is insensitive
to the C-rate" 인데 Fig. 15(a) `[도표]` SOH 79.4 % 에서 C/3 ≈18 % vs C/25 ≈11.7 %
(≈6 pp, LLI 의 율 편차 6.07 % 와 같은 크기); (b) Fig. 9 와 Fig. 11 의 봉우리 전압이
≈40 mV 다르고 충/방전 미표기; (c) 18650 SOH 본문 79.72 vs 범례 79.76. 그리고 "Peak C
에서 de·li 가 상쇄" 는 가상 배터리를 **de:li = 1:1** 로 만든 산물인데 같은 논문의 진단은
≈1.75:1 이다 (G10).

**컴파일**:
- 신규 concept [[ic-peak-area-direct-mode-readout-lfp]] (index 등록, 31 페이지).
- [[halfcell-window-parametrization-lineage]] — Cui 2026 행(4, 재조합 7 → 4, 사전믿음
  등식으로 다시 7) + 새 절 "**등식의 새 변종 — 사전믿음 등식으로 다시 가른다**".
- [[mode-identifiability-unmeasured-lineage]] — 표에 행 추가 + §9 신설("다섯 번째 인쇄 —
  줄였다가 사전믿음으로 늘리고, 축퇴는 재료 측정이 대신 풀었다"), 계보 16 → **17편**.
- [[22p-physics-or-degeneracy]] — Evidence For 1건(적합의 "깨끗한 상수" 가 tie-break
  였고 데이터 밖 측정이 판정) + Status Log.
- [[pvs-sev-lli-lampe-separability]] — Evidence Against 1건(LFP·양극 제한 regime 에서
  LLI ↔ LAM_liPE 가 OCV·IC 어느 관측에서도 같은 자리) + Gap 1건(부호표에 LAM_PE 열
  부재, 정답 축 적합값) + Status Log.
- [[rate-independent-li-plating-signature]] — 관련 항목에 상호 링크 (같은 화학의 무릎
  앞/뒤).

**미실행 후속 (값싸다)**: LFP 합성 truth 에서 `(X1, X3)` 방향 `JᵀJ` 조건수; LAM_PE
0 → 10 % 에서 OCV 적합과 Peak C 면적법의 LLI 오귀속량 동시 계산; de:li 비(1:1 / 1.75:1 /
3:1)에 따른 Peak C 편향.

`python3 wiki/tools/lint.py` → **0 errors, 0 warnings** 확인 (pages 31, raw files 26).

## [2026-09-14] create | 근최적 집합 폭 측정법 + 서브 브랜치 인수인계 3건 반영
- 서브 브랜치(`bms-balancing/`)가 `HANDOFF_TO_GATE.md` §3 에서 "위키에 올릴 후보"
  로 넘긴 세 건을 본체가 채택해 반영. 원문은 `raw/transcripts/2026-09-14-bms-handoff-width-and-wiki-candidates.md`
  에 보존 (§2 폭 측정법 · §3 위키 후보, sha256 봉인).
- 새 페이지 [[near-optimal-set-width-measurement]] — 등방 표집이 참 폭 40 %p 를
  0.00 %p 로 보고한 반례, Hessian 의 같은 국소성 한계, 제약 최적화 + mode 등식
  프로파일의 합집합, 한계 넷. 본체 적용 여부는 **미정**으로 명시.
- [[halfcell-ocp-shape-invariance]] — Schmitt 2022 가 재지 않은 자리의 첫 숫자
  (12 mV 문턱 안 LAM_NE 17.4 %p · LLI 1.14 %p) 와 문턱 의존성 경고 추가.
- [[halfcell-window-parametrization-lineage]] — 규진팀 MATLAB 의 chain rule
  결함(dV/dQ 에 `1/α` 누락, 7~15 % 계통 오차) 기록. **본체에는 없음을 오늘
  실측으로 확인** (수치미분 경로라 `1/α` 가 자동으로 들어간다; α=0.80 대조에서
  오차 6.4e-06 vs 7.9e-01). 닫힌 신고.
- lint 0 errors / 0 warnings.

## [2026-09-16] ingest | Bielefeld, Weber, Janek 2019 — Microstructural Modeling of Composite Cathodes for ASSBs (`assb` 섹션 1호)
- raw: `raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md`
  (J. Phys. Chem. C 2019, 123, 1626−1634, 9쪽, sha256 봉인). **액체셀 계열 20편과 분리**
  — `assb` 태그, 닻은 [[assb-contact-loss-vs-lampe]].
- 그림: `raw/figures/bielefeld2019_.../` (fig 10 + tab 1). **본문 그림 10장 전부 Read 로 직접 봤다**
  (Fig. 1–10). SI 없음. 표 1장은 PDF 텍스트로.
- 컴파일: [[composite-cathode-percolation-utilization]] (concept, `assb` 축 첫 개념).
  닻 카드에 Q1~Q8 채움표 + Evidence For/Against + Status Log 추가, sources·updated 갱신.
- 핵심 수확: 접촉 손실의 **형태**가 정해졌다 — 이용률 `θ = V_c/V_ν` 가 용량 축 스케일에
  **곱**으로 들어간다. 그리고 **라벨 자체가 폭을 갖는다**(무작위 충전만으로 `θ_AM`
  ≈30 % ↔ ≈70 % 이봉; 임계 바로 위 `A_spec` σ ≈ ±32 %) → DEM 독립 라벨 계획의 선행 조건
  두 개(폭 보고 · 도메인 크기 수렴)가 여기서 나왔다.
- 비판 기록: **유효 전도도(S/cm)가 한 번도 계산되지 않았는데 초록이 그 결과를 주장**하고,
  본문이 **유한 크기 인공물**이라 적은 것을 초록이 **"유리한 전극 특성"** 으로 뒤집는다
  (digest §10 불일치 1). 어긋남 원장 8건. Q1~Q8 중 실질 충족 1.5/8 — **Q6(압력) `pressure` 0회**.
- lint 0 errors / 0 warnings.

## [2026-09-16] ingest | Clausnitzer et al. 2023 — Optimizing the Composite Cathode Microstructure in ASSBs by Structure-Resolved Simulations (`assb` 섹션 2호)
- raw: `raw/papers/clausnitzer2023_optimizing-composite-cathode-structure-resolved.md`
  (*Batteries & Supercaps* 2023, 6, e202300167; 본문 16쪽 + **SI 10쪽**, 둘 다 sha256 봉인).
  `assb` 태그, 닻은 [[assb-contact-loss-vs-lampe]]. 액체셀 계열 20편과 분리 유지.
- 그림: `raw/figures/clausnitzer2023_.../` (fig 11 + SI fig 7 + tab 6 = **24장 크로핑**).
  **직접 Read 로 본 것 15장** — Fig. 1–11 전부 + Fig. S1·S3·S4·S5·S7.
  **안 본 것 3장** — Fig. S2(도메인 모식도)·S6(면적당 용량, 본문이 Fig. 4 와 같은 상관이라
  명시)·표 6장은 PDF 텍스트로 읽음.
- 컴파일: 새 개념 [[assb-apparent-capacity-decomposition]] (concept, `assb` 축 둘째) +
  [[composite-cathode-percolation-utilization]] 갱신(좌표 변환표 · 반례 · 산포 후퇴 ·
  evidenceScope → multi-source-primary). 닻 카드에 Q1~Q8 행 추가 + Evidence For/Against
  보강 + Status Log, sources·updated 갱신.
- **1호 대비 셋 중 하나만 들어왔다**:
  **전압축 ★있다** (`U₀ = 4.2 V` 함수형 · `U_cut = 3.4 V` · Fig. S5 `V`–`Q` 방전 곡선 ·
  `Wh/kg_cell` 식 (9)) — `assb` 계보 최초.
  **동역학(시간축) 없다** (방전 1회, 사이클 0, 역학 0 — `[인쇄]` "beyond the scope").
  **시드 산포 없다** (오차막대 0, 점당 구조 1개; 도메인이 1호의 `[재현]` 1/28.7 부피 —
  **1호보다 후퇴**).
- 핵심 수확: **1호의 곱셈 `Q_apparent = θ_AM·Q_material` 이 충분하지 않다는 논문 내부
  반례** (CAM 연결성 ≈100 % 인데 정규화 용량 ≈0.10) → 3항 분해
  `θ_AM · η(i) · Q_material`. 그리고 **율(rate)이 셋 중 동역학만 지운다**는 분리 시험
  (논문의 두 인쇄 문장에서 추론 — 논문은 단일 율로만 돌았다).
  `[도표]` 재료·기하 동일·입계 저항만 0 → 3.6 Ω cm²: 1.37 → 0.385 mAh/cm² =
  **겉보기 `LAM_PE` 72 %**, 그 곡선은 **아핀 스케일링이 아니다**(시작 전압 −175 mV).
- 좌표 확정: **`θ`(1호) ≡ `Connectivity`(2호)** — 변환 불필요. `ρ_S = 1 − φ`,
  `SVF_CAM ≡ g^S_AM`, `1 m²/m³ = 10⁻² 1/cm`. ⚠ 1호의 닫힌 형태(식 7·8)는 **적용 불가**
  (2호 구조는 다분산 육각판+구, Voronoi 소결).
- 비판 기록: 어긋남 **14건**. 최악은 본문 "electronic conductivity … orders of magnitude
  higher than ionic" 가 **자기 Fig. S4 에 반증**되는 것(`SVF ≤ 60 %`, `c_Li,max` 에서 전자가
  더 낮다) — 그 문장이 "kinetic limitations are mainly due to ion conduction" 을 떠받친다.
  그 밖: 격자 밖 결론("20 vol% for both" 의 CAM 쪽 · "`SVF=30 %` 최적" · "optimal … thickness"),
  조판 오류 5건(식 (1)·(6)·Table S3·캡션 3건). 미해결 좌표 G1 — **`C_norm` 이 `θ_AM` 을
  포함하는지 원문에 없다.**
- Q1~Q8: 2호 단독 ≈2.5/8, 2편 누적 합집합도 ≈2.5/8. **Q4(유일성)·Q5(Li-In)·Q6(압력)·
  Q7(dead Li) 은 여전히 0편** — Q6 은 `assb` **2/2 편이 `pressure` 0회**, Q4 는 두 편 모두
  forward 전용이라 원리적으로 못 채운다.
- lint 0 errors / 0 warnings.

## [2026-09-16] ingest | Liu · Roters · Raabe 2024 — Role of grain-level chemo-mechanics in composite cathode degradation of solid-state lithium batteries (Nat. Commun. 15, 7970) — `assb` 3호

- raw: `raw/papers/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation.md`
  (절별 해체분석 · 본문 18쪽 sha256 `0835168b…` + SI 10쪽 sha256 `46b8d56f…` **둘 다 봉인**).
  그림: `raw/figures/liu2024_…/` — 자동 크롭 6장(Fig. 1·2·3·5·6 + Table S1) + **캡션
  검출이 놓친 Fig. 4·7 과 SI 전체(`Fig. S.1` 처럼 번호에 점)를 쪽 렌더로 보강**.
  **실제로 본 것: Fig. 3(전문+3c 확대) · 4(전문+4a 확대) · 5(전문+5d–f 확대) ·
  6(쪽 렌더+6h 확대) · 7 · S1 · S2 · S3 · S4 · S5 · S8.**
  안 본 것: Fig. 1·2(개념도) · Fig. S6·S7(4d,4e 의 3D 판). Table S1 은 PDF 텍스트로.
- 컴파일: **새 개념 페이지 없음** (SCHEMA Page Thresholds 판단 — 이 논문의 좌표는 `θ` 로
  변환되지 않아 기존 두 개념에 **제약**으로 붙는 편이 정확하다). 대신
  [[assb-apparent-capacity-decomposition]] 갱신(율 극한 확인 + `Q_material` 율 의존 +
  주장하지 않는 것 3항) · [[composite-cathode-percolation-utilization]] 갱신(§"3호는 이
  `θ` 와 변환되지 않는다" 신설 + 원장 확장) · 닻 [[assb-contact-loss-vs-lampe]]
  (Q1~Q8 행 추가 · Evidence For 보강 · 새 제약 5항 · Status Log) · index.md 3줄.
- **물은 세 가지에 대한 답**:
  **`θ(N)` 시간축 — 없다.** 방전 1회(+ 충전 1회), 사이클 축 그림 0장. 결정적으로
  **파괴·디본딩 모형이 없다** (`[인쇄]` "does not explicitly account for mechanical
  fracture"). 있는 것은 **계면 최대주응력**(GPa)뿐 — **`θ` 로 변환 불가**.
  `assb` **3/3 편이 시간축을 안 줬고, 이제 공통 원인이 보인다**(cohesive zone /
  phase-field damage 가 3편 모두에 없다).
  **실험 — 없다.** 자기 실험 0 (3/3 편 공통). 대조 자료는 전부 인용이고 **모집단이
  어긋난다**: Fig. 4a 방전곡선은 **Si 음극 + 황화물 SE** 셀(ref 62), Fig. 5e 활물질
  손실 실측은 **전부 액체 전해질 Li-ion 셀**(refs 67–71), Fig. 5c 산소결핍은
  **Li-rich** 산화물(ref 5).
  **시드 산포 — 없다.** 구조 실현 **1개**. 본문은 `[인쇄]` "the **random arrangement**
  of primary particles … play a critical role" 라고 적고도 실현을 안 늘렸다.
  Fig. 3j·4e 의 "statistical variability" 는 **한 구조 안의 공간 분포**다.
- **새로 들어온 것 둘 (`assb` 계보 최초)**: ★ **OCV 곡선** (SI Fig. S2, GITT, `1−θ` 0→1
  에서 ≈3.0 → 4.4 V vs Li/Li⁺, 전 구간 기울기) — 2호가 남긴 "OCV 0편" 단서를 닫았다.
  ★ **율 스윕** (SI Fig. S4, 0.25–5C × 4 크기 = 20 곡선): `i→0` 에서 전 크기가 ≈1 로
  수렴 → 3항 분해의 **`η(i)→1` 이 독립 모델에서 확인**됐다 (그 모델은 `θ_AM ≡ 1`).
- **가장 무거운 수확 둘**: ① `[인쇄]` **"실험의 활물질 손실은 rock-salt 형성 + 입계
  파괴로 고립된 활물질을 둘 다 포함한다"** — 닻 질문의 축퇴가 **문헌 문장으로 확인**된
  첫 사례. ② **`Q_material` 이 율 의존**(12 µm: 0.25C 0.093 → 5C 0.185) → 우리 율 스윕
  분리 시험이 좁아졌다 (저율 쌍 또는 **왕복 이력**으로).
- 비판 기록: 어긋남 **18건** (1호 8 · 2호 14 · 3호 18). 무거운 묶음 **D3·D4·D5·D6** —
  초록이 "contact loss **is caused by**" 라고 단정하는데 모델에 접촉 손실 변수가 없고(D3),
  Fig. 5 의 손실 기준이 자기 방전곡선과 화해되지 않으며(D4, 12 µm·1C: 0.235 vs 0.31),
  "kinetically induced capacity loss" 가 **세 곳에서 다른 뜻**이고(D5),
  Fig. 7 의 "Operating window, ≥90 % usable capacity" 라벨이 **자기 Fig. 5d 와 모순**(D6,
  두 손실이 가법인데 패널마다 한 성분만 10 %로 자른다). **2호와 같은 형태** — 결론을
  떠받치는 문장이 자기 그림과 충돌한다.
  그 밖: **Fig. 3c 범례 색이 Table S1 과 뒤바뀜**(D1, 5쌍 중 4쌍; Fig. 6a 로 독립 확인),
  출처 없는 초록 수치 `393 Wh kg⁻¹`(D2), 본문 "+20 % 용량" vs 도표 +25 %p(D7),
  서론 "7.8 % 부피변화" vs 자기 Fig. 3b `[재현]` 6.3 %(D8), 단위 오식 2건(D13).
- **재현 가능성 원장 신규 항목**(D16): Code Availability 가 가리키는 공개 DAMASK v2.0.2 는
  **이 연구가 쓴 코드가 아니다** — 실제 코드는 `git.damask-multiphysics.org` 의
  `plasticity_chemo_mechanics` 브랜치(커밋 `a987e05f…`)이고 **MPIE 허가 + CLA 승인**이
  필요하다. 인계받은 확인: 공개본(2018-05-22, 71파일·50,208줄 Fortran)에 `lithium`·
  `intercalat` **0건**, 논문이 "developed" 라고 적은 **독립 FEM 솔버도 없다**(spectral +
  Marc/Abaqus 인터페이스뿐), 라이선스 GPL.
- Q1~Q8: 3호가 새로 채운 칸은 **Q8 하나**, **Q3 에 새 층위**(fitted 문턱 12 %, 타 화학에
  적합). **3편 누적 ≈3.0/8.** Q4(유일성)·Q5(Li-In)·Q6(압력)·Q7(dead Li) 은 **3/3 편 0** —
  특히 Q6 은 **접촉 역학이 본체인 논문이 `pressure` 0회**다.
- 후속 후보: 1순위 **Koerver 2017** (`Chem. Mater.` 29, 5574 — 3편이 모두 인용, 접촉
  손실의 실험 원전 + 용량축 + 사이클; **`θ(N)` 은 실험 쪽에서만 나온다**),
  2순위 **Shin 2023** (`Adv. Energy Mater.` 13, 2301220 — 저압 조건, **Q6 첫 후보**).
- lint 0 errors / 0 warnings.

## [2026-09-16] ingest | Shi 2020 — Characterization of mechanical degradation in an all-solid-state battery cathode (`assb` 4호, 첫 실험 논문)

- 원본: `raw/papers/shi2020_mechanical-degradation-assb-cathode.md` — Shi, Zhang, Tu,
  Wang, Scott, Ceder, *J. Mater. Chem. A* **8** (2020) 17399–17404,
  doi `10.1039/d0ta06985j`. 본문 6쪽 + ESI 7쪽, **둘 다 sha256 봉인**.
  ⚠ **업로드 파일명이 서로 바뀌어 있었다** — `Sup_` 이 붙은 쪽(6쪽)이 본문, 안 붙은
  쪽(7쪽)이 ESI 다. 해시는 **내용 기준**으로 붙였다.
- 그림: `wiki/tools/extract_figures.py` 로 **6 장 크로핑, 6 장 전부 열람**
  (`wiki/raw/figures/shi2020_mechanical-degradation-assb-cathode/`).
  ⚠ ESI **Fig. S3** 은 캡션이 PDF 안에서 `Fi`/`gure S3.` 로 끊겨 탐지되지 않아
  **크로핑되지 않았고 보지 못했다** (Weka 분할 워크플로 — 정확도 수치 없음).
  본문에 없고 **그림에만 있는 수**를 여럿 건졌다: `R_LF` ≈110 → ≈39 kΩ ·
  반원 경계 50 kHz / 6 Hz · void 부피분율 라벨 · 재구성 부피 3 개 ·
  사이클별 방전 시작 전압 · 충전 전압 비단조 진동.
- ★★ **이 계보 첫 실험 논문이고, 한 편에서 세 칸을 깼다.**
  **Q2(자기 실험 — `assb` 3/3 편 연속 0)** · **Q6(압력 — 3/3 편 `pressure` 0 회)** ·
  **Q8(실측 사이클별 V–Q — 3호의 OCV 는 타 논문 액체 반쪽전지 GITT 였다)**.
  Q1 을 **무차원 분율 + 시간축**으로, Q5 를 **부분**으로 열었다.
  Q1~Q8 채움표 **4편 누적 ≈5.5/8**. **남은 0: Q4(유일성) · Q7(dead Li).**
- 핵심 수치 (정본은 원문 PDF — 아래는 사본):
  `[인쇄]` 첫 방전 **129 mAh g⁻¹** → 26 사이클에 102 (≈1 mAh g⁻¹/cycle) →
  30–40 사이클에 급락 → `[도표]` 사이클 46–50 **≈2 mAh g⁻¹** (본문은 "<20") →
  **50 사이클 후 300 MPa 재가압** → `[인쇄]` **80 mAh g⁻¹** (`[재현]` **+60.5 %p**).
  `[인쇄]` 접촉 손실 **면적 10.4 %** · `[도표]` void **2.87 / 3.23 / 9.50 vol%**
  (사이클 0/10/50) · `[인쇄]` `R_MF` **954 → 1241 → 3283 → 2755 Ω** ·
  `[도표]` `R_LF` **≈0.7 → ≈110 → ≈39 kΩ**.
  압력: 제작 **100 / 300 / 100 MPa**, 사이클 **~2 MPa 스프링**, 재가압 **300 MPa**
  (⚠ **전부 ESI 에만**). 율 `[재현]` **≈C/15**.
- 컴파일:
  - **새 개념 1**: `concepts/assb-pressure-reapplication-separation-test.md` —
    **두 번째 분리 연산자**. 율이 `η(i)` 를 지우듯 **압력이 `θ_AM` 을 되돌린다**.
    `ΔQ_mech ≡ Q(P_high) − Q(P_low)` = 기하 접촉 손실의 **상한** → 진짜 `LAM_PE` 의
    **하한**. ★ **OCV 밖의 축이 열린다.** `confidence: low` (사례 1 편·1 셀·압력 1 점).
  - `concepts/composite-cathode-percolation-utilization.md` 갱신 — 4호의 **면적
    분율 ↔ `θ`(부피 분율)** 좌표 대조표, **6 배 간극**, 시간축 도착과 그 계단 모양,
    실측 라벨에도 폭이 없다는 기록, "모두가 안 잰 것" 원장에서 **압력 항목 해소**.
  - `concepts/assb-apparent-capacity-decomposition.md` 갱신 — **율 극한 논증의
    실험 간접 검증**(≈C/15 셀), 곱셈 형태의 실측 반례, 회복분 귀속 경고.
  - `questions/assb-contact-loss-vs-lampe.md` 갱신 — Q1~Q8 채움표 4호 행,
    미결 항목 1·2·4 갱신, Evidence 에 **실측 반례** + **압력 개입** + **율 극한
    간접 검증** + **충전 전압 비단조 진동(새 feature 후보)**, 새 제약 7 항, Status Log.
- 최대 수확 셋:
  ① ★★ **분리 연산자가 하나 더 생겼다** (300 MPa 재가압, +60.5 %p 회복).
  ② ★★ **곱셈 형태의 실측 반례** — 접촉 손실 면적 **10.4 %** 인데 압력 가역분이
  **60 %p**. **≈6 배.** 논문은 두 수를 **한 번도 비교하지 않는다**.
  → **`θ` 를 스칼라 곱셈 인자로 쓰는 모형은 실측과 6 배 틀린다.** DEM 이 주는 것도
  **접촉 수·면적**이므로 이 제약이 우리 계획에 직접 걸린다.
  ③ ★★ **논문의 인과가 자기 EIS 와 충돌한다** — `[도표]` 50 사이클에서 음극 쪽
  `R_LF ≈110 kΩ` 가 전체 저항의 **≈93 %**(양극 `R_MF` ≈3.3 kΩ, **33 배**),
  재가압 회복률도 **LF 65 % vs MF 23 %**. 그런데 초록·결론은 **양극 접촉 손실**로
  돌린다. → **Q5(In 기준극 안정성)가 채워지면서 동시에 문제로 드러났다.**
- 어긋남 원장 **18 건**(1호 8 · 2호 14 · 3호 18 · 4호 18). 무거운 묶음
  **D8·D9·D10·D12**: 초록·결론의 인과 ↔ 자기 Fig. 1(c) · 10.4 %와 60 %p 무비교 ·
  **라벨과 관측이 다른 셀**(토모그래피 3 셀의 용량이 한 번도 없다) ·
  **검출 한계가 "후기에 몰린다" 결론을 만들었을 수 있다**(같은 논문이 "very small
  microfractures … undetectable by the tomography" 라고 적는다).
  그 밖: 전압창 본문 `1.4–3.7 V vs In` ↔ ESI `2–3.7 V vs In`(D1, 그림이 본문 편) ·
  본문이 Fig. 1 (c)/(d) 를 바꿔 씀(D2) · "<20 mAh g⁻¹" 인데 실제 ≈2(D3) ·
  재구성 부피가 캡션 "all 60×40×30 µm³" 와 하나도 안 맞고 pristine 이 0.62 배(D4) ·
  재가압 후 **재감쇠(80→≈64) 무언급**(D17) · 압력값이 전부 ESI 에만(D16).
- 산포 규율: `error bar`·`standard deviation`·`uncertain*`·`replicate`·`seed`
  **전부 0 회**(본문+ESI), 조건당 **셀 1 개**, 분할 정확도 수치 **없음** —
  `assb` **4/4 편 연속** (1호만 실현 간 폭을 쟀다).
- 후속 후보: 1 순위 **Koerver 2017** (`Chem. Mater.` 29, 5574 — `assb` 4 편 전부 인용;
  4호가 `θ(N)` 3 점을 줬지만 **용량과 같은 셀에서** 주지 못했다), 2 순위
  **Koerver 2018** (`EES` 11, 2142 — **스택 압력 스윕**, Q6 을 스윕으로), 3 순위
  **Neumann/Danner/Latz 2020** (`ACS AMI` 12, 9277 — 4호 실측 기하를 2호 계보 전방
  모형에 꽂는 다리), 4 순위 **Zhang/Scott/Ceder 2020** (`AEM` 1903778 — LZO 코팅
  불안정성, 4호가 정량 없이 남긴 화학 열화 몫).
- lint 0 errors / 0 warnings.

## [2026-09-16] ingest | Doux et al. 2020 — Stack Pressure Considerations for Room-Temperature All-Solid-State Lithium Metal Batteries (Adv. Energy Mater. 10, 1903253) — `assb` 5호

- raw: `raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md`
  (본문 6 쪽 + SI 8 쪽, **둘 다 sha256 봉인**; doi `10.1002/aenm.201903253`, UCSD /
  Y. S. Meng). ✅ 업로드 파일명이 **내용과 일치**한다 — 4호의 본문/SI 뒤바뀜 사고
  재발 없음 (쪽수 + 1 쪽 첫 줄로 확인).
- 그림: 크로핑 13 장(그림 11 + 표 2) 중 **그림 11 장 전부 열람**. 표 2 장은 도구
  권고대로 PDF 텍스트로 읽었다 (`raw/figures/doux2020_stack-pressure-room-temperature-assb-li-metal/`).
- 컴파일: **새 개념 1** — `concepts/assb-stack-pressure-operating-window.md`
  (압력의 2 측 구속: 아래는 접촉 손실, 위는 Li 크리프 단락).
  갱신 — `concepts/assb-pressure-reapplication-separation-test.md`(경고 4 부분 해소 +
  상한·전극 귀속·이력·비직교성 5 항 추가), `questions/assb-contact-loss-vs-lampe.md`
  (Q1~Q8 행 추가, 미결 3·4 갱신, Evidence 반례 + 새 제약 + status log).
  ⚠ `concepts/composite-cathode-percolation-utilization.md` 는 **일부러 안 건드렸다**
  — 이 논문은 음극 축이고 그 페이지는 이미 **320 줄**(SCHEMA 200 줄 권고 초과).
  **분할 제안은 사용자 판단 대기.**
- ★★ 이 편이 한 일: 4호가 **점**으로 준 압력을 **곡선**으로 바꿨다 —
  **P→임피던스 6 점**(1 MPa >500 Ω → 25 MPa 32 Ω, +이력 1 점) ·
  **P→단락시간 6 점**(75 MPa 0 h · 25 MPa 48 h · 20 MPa 190 h · 15 MPa 272 h ·
  10 MPa 474 h · 5 MPa >1000 h) · **P→과전압 5 점**(+본문에 없는 2 MPa 1 점).
  압력을 **로드셀로 실계측**한 첫 편(0–220 MPa, Instron 교정).
- 최대 수확 넷: ① **상한**(4호의 300 MPa 는 이 상한의 4 배 — 단 모집단이 In 음극 ↔
  Li 금속으로 다르다) ② **전극 귀속**(양극 없는 대칭셀에서 압력이 임피던스를
  >15 배 움직인다 → `ΔQ_mech` 를 양극으로 읽으면 과대) ③ **이력**(계면 과잉의
  77 % 영구 제거 → `θ(P)` 는 경로 의존 상태) ④ **Q7 절반 해소**(SEI 는 상으로 검출,
  dead Li 는 검출 수단 없음). Q1~Q8 **5편 누적 ≈6.5/8**, 남은 0 은 **Q4 하나**.
- 어긋남 원장 **20 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · 5호 20). 무거운 묶음
  **D1–D6**: "과전압이 전 과정 일정했다 → 계면 안정" 이 **자기 SI Fig. S4 다섯 패널
  전부에서 8–28 % 증가**로 반증(D1) · 본문이 **Fig. S5 를 "1000 h" 근거로 인용하는데
  Fig. S5 는 92 h**(D2) · **Fig. S2·S3·S4 를 본문이 한 번도 인용하지 않음**(D3) ·
  그중 **S3 은 Methods 에도 없는 2 MPa 조건**이라 "optimal 5 MPa" 에 하한 탐색이
  없다(D4) · **S2 는 단락 28 h 전 임피던스 −16 % 전조**인데 해석 0(D5) ·
  **"덴드라이트" 동정에 독립 근거 없음**(D6 — Li 는 XRD 로 안 보이고 같은 저밀도
  대비를 Fig. S6 에서는 "severe cracking" 이라 부른다).
  → **새 변종: 인용조차 되지 않은 SI 가 본문을 반증한다.**
- 산포: `error bar`·`standard deviation`·`uncertain*`·`replicate`·`seed` 전부 0 회,
  조건당 셀 1 개. ★ **단 하나의 예외** — Table S2 가 펠릿 **4 개**의 상대밀도를
  인쇄한다(80.2/84.9/80.3/83.0 %, `[재현]` s ≈2.3 %p → 공극률 15.1–19.8 %):
  **`assb` 5 편 중 첫 반복 측정**이고, 그 폭이 단락 기구(기공 퍼콜레이션)의 입력이다.
- 후속 후보: 1 순위 **Koerver 2017**(`Chem. Mater.` 29, 5574), 2 순위 **inbox 15번**
  (*Elucidating the Influence of Stack Pressure on Anode and Cathode Impedance …
  via Three-Electrode Measurements* — 이 ingest 가 남긴 **전극 분해 + 압력** 공백
  정조준), 3 순위 **inbox 24번**(*… Long Cycle Life at **Low Pressure*** — 창의 아래 벽),
  4 순위 **Kasemchainan 2019**(`Nat. Mater.` 18, 1105 — 5호가 반박한 탈리 void 원전).
- lint 0 errors / 0 warnings.

## [2026-09-16] ingest | Lee 2020 — High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes (`assb` 6호)

- `raw/papers/lee2020_ag-c-anode-free-assb.md` (*Nature Energy* **5** (2020) 299–308,
  doi `10.1038/s41560-020-0575-z`, **SAIT + Samsung R&D Japan**, 저자 16 명 전원 삼성).
  본문 10 쪽 + SI 18 쪽, **둘 다 sha256 봉인**. ✅ 파일명 ↔ 내용 일치 (4호의 뒤바뀜
  재발 없음 — 쪽수와 첫 쪽 텍스트로 확인).
- ★★ **계보에서 처음인 것 셋**: **무음극(anode-free)** · **산업체 논문** ·
  **Ah 급 파우치 셀**.
- 컴파일: **새 개념 1** — `concepts/anode-free-li-inventory-accounting.md`
  (무음극 `LLI` 의 계정) + `concepts/assb-stack-pressure-operating-window.md` ·
  `concepts/assb-apparent-capacity-decomposition.md` ·
  `concepts/assb-pressure-reapplication-separation-test.md` 갱신 +
  닻 `questions/assb-contact-loss-vs-lampe.md` Q1~Q8 행 추가.
  ⚠ `composite-cathode-percolation-utilization.md` 는 **일부러 건드리지 않았다**
  (이미 320 줄; 그리고 이 논문은 양극 `θ` 에 대해 아무것도 주지 않는다).
- 최대 수확 넷:
  ① ★★★ **`LLI` 추정자의 분해능이 새 전선** — 같은 논문 안에서 20 mAh 셀은
  CE(99.97 %)↔유지율(92.5 %@300)이 맞고 **0.6 Ah 셀은 10 배 어긋난다**
  (CE `[도표]` 99.89 % ⇒ 누적 결손 `[재현]` **161 mAh g⁻¹** ↔ 실측 손실 **16**,
  양극 재고 **215**). **CE 축 눈금조차 다르다**(95–101 vs 99.4–100.0). 논문은
  두 셀을 **한 번도 비교하지 않는다.**
  ② ★★★ **압력이 두 축으로 갈렸다** — **제작 490 MPa 등방(WIP, 비가역: Table S2)**
  vs **운전 2 MPa**, 그리고 **무압 0.1 C 가 2 MPa 와 구별 안 된다.** 5호와 모순이
  아니라 **제작 압력 이력이 다르다**. ⚠ 운전 상한 ">4 MPa 단락" 은 **데이터 0**.
  ③ ★★ **Q7 채널 둘 추가, 정량 0** — **EELS Li 맵**(방전 후·100 사이클 후에도 Li 망
  잔존)과 **XRD 의 Li₉Ag₄**(Li 저장 상 동정). **dead Li 만 여전히 수단 없음.**
  ④ ★★ **"무음극은 OCP 평탄" 이 앞 10–17 % 구간에서 거짓** (Fig. 4a + SI Fig. 4c).
- Q1~Q8 **6편 누적 ≈7.0/8**. **남은 0: Q1(양극 접촉 손실 정량) · Q4(유일성).**
- 어긋남 원장 **14 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · 5호 20 · **6호 14**).
  ⚠ **2–5 호보다 적고 가볍다** — *Nature Energy* 의 편집 품질이 보이고, 5호의 변종
  (인용조차 안 된 SI 가 본문을 반증)은 **여기 없다**. 무거운 넷: **D2**(CE↔유지율
  10 배) · **D1**(">99.8 % CE" ↔ `[도표]` 900–1000 사이클 중앙값 **99.21 %**·최저
  **97.42 %**, 언급 0) · **D3**(">4 MPa 단락" 데이터 0) · **D6**("no residual Li
  deposits" ↔ EELS Li 망 잔존).
- 산포: `n =`·`N =`·`error bar`·`standard deviation`·`replicate`·`uncertain*` 이
  **본문+SI 전수 0 회**. ★ 유일한 예외 **Table S2 ±2.2–2.9 µm**(정의·n 없음) —
  5호 Table S2 에 이어 **두 번째이고 둘 다 기하다.** **파우치 스케일업 논문인데
  통계가 오지 않았다.**
- 그림: 크로핑 **26 장** 중 **그림 12 장 열람**, 표 3 장은 PDF 텍스트로.
  ⚠ **Fig. 6 은 크로퍼가 제외**해 `pymupdf` 로 8 쪽 직접 렌더, **Fig. S10 은 제외된
  채 열지 않았다**(Q1 판정은 Table S2 + 본문 서술에만 근거).
  ★ Fig. 6g·SI Fig. 16 은 **PDF 축 눈금 좌표로 교정 후 화소 판독**, 교정을
  인쇄값(600 사이클 95 % · 1000 사이클 89 %)으로 검증.
- 후속 후보: 1 순위 **Koerver 2017**(`Chem. Mater.` 29, 5574 — 여섯 편이 모두 인용하고
  여섯 편이 모두 안 준 Q1 의 실험 원전), 2 순위 **inbox 15번**(3전극 + 압력),
  3 순위 **Genovese/Dahn 2018**(`JES` 165, A3321 — **무음극 CE 측정법 그 자체**),
  4 순위 **Zhang 2017**(`JMCA` 5, 9929 — 운전 중 압력 변화 실측).
- lint 0 errors / 0 warnings.

## [2026-09-16] ingest | assb 7호 — Spencer-Jolly 2023, Ag–흑연 무음극 중간층의 operando 구조 변화 (Joule 7, 503–514)

- `raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md` 신설.
  Spencer-Jolly, Agarwal, Doerrer, Hu, Zhang, Melvin, Gao, Gao, Adamson, Magdysyuk,
  Grant, House, **Bruce** — *Joule* **7** (2023) 503–514,
  doi `10.1016/j.joule.2023.02.001`, **University of Oxford + Diamond Light Source**.
  본문 13 쪽 + SI 6 쪽, **둘 다 sha256 봉인**(업로드 파일을 직접 해시).
  ✅ 파일명이 내용과 맞다(쪽수·1 쪽 텍스트로 확인). ⚠ 같은 업로드의 `Sup1_`(2 쪽,
  *Standardized data reporting for batteries* **제출 양식**)은 사용자 지시대로
  **읽지 않았고 근거에 없다.**
- 컴파일: **새 개념 1** — [[ag-c-interlayer-lithium-phase-path]] (`assb` 축 여섯째).
  갱신 — [[anode-free-li-inventory-accounting]] · [[assb-apparent-capacity-decomposition]] ·
  [[assb-stack-pressure-operating-window]] · [[halfcell-ocp-shape-invariance]] ·
  닻 [[assb-contact-loss-vs-lampe]].
  ⚠ [[composite-cathode-percolation-utilization]] 은 **일부러 안 건드렸다**(339 줄,
  그리고 이 논문은 양극에 아무것도 주지 않는다).
- ★★ **계보에서 처음인 것 셋**: **operando 회절**(실험실 Cu Kα + 싱크로트론 56 keV) ·
  **6호(삼성)의 외부 검증** · **원자료 공개**(Oxford Research Archive,
  DOI 10.5287/bodleian:kKBPZ282m).
- 최대 수확 넷:
  ① ★★★ **dead Li 가 처음으로 숫자가 될 수 있게 됐다** — `[도표]` 충전 67.6 h ·
  방전 35.0 h(둘 다 30 µA cm⁻²) ⇒ `[재현]` **2.03 ↔ 1.05 mAh cm⁻², 첫 사이클 효율
  ≈52 %**, SEI 구간 0.19 를 빼면 **≈0.79 mAh cm⁻² = 통과 전하의 39 %** 가 설명되지
  않는다(방전 종료 회절에 `[인쇄]` "only graphite and Ag" 만 남는다).
  ⚠ **논문은 이 뺄셈을 하지 않는다** (`Coulombic`·`efficiency`·`dead`·`isolated`
  본문+SI **전수 0 회**). ⚠ **SEI ↔ dead Li 는 여전히 안 갈린다.**
  ② ★★★ **음극 OCP 가 충전과 방전에서 다른 곡선이다** — 충전 경로에 없는 상
  (**LiAg 의 UPb 다형**)이 방전에 나타나고 논문이 **열역학적 안정성**으로 설명한다.
  율 ≈**C/68** · 상온 → **`i→0` 으로 지울 수 없는 이력**.
  ③ ★★ **6호의 "Ag 는 돌아오지 않는다" 에 대한 답** — 충전에 Ag 가 층 밖으로 나가
  집전체 계면의 **균일막**, 방전에 **다시 층 안 불연속 군집**. **모순이 아니라
  시간척도가 다르다**(1 사이클 ↔ 100 사이클). **사이클당 잔류는 아무도 안 쟀다.**
  ④ ★★ **Ag 는 임계전류를 못 올린다** — 흑연 단독과 **같은 failure point**
  (2.0 안정 / **2.5 mA cm⁻² 단락**). ⚠ **흑연 계의 판정**이다.
- Q1~Q8 **7편 누적 ≈7.0/8 — 칸은 안 늘었다.** 남은 0: **Q1(양극 접촉 손실 정량) ·
  Q4(유일성)**. **Q6 은 6호 대비 후퇴**(스윕 0 · 계측 0 · 무압 대조 0).
  ★ **모집단 경계 넷**(탄소 카본블랙↔흑연 · 완전지↔반쪽전지 · 1000↔1 사이클 ·
  등방 490 MPa↔일축 400 MPa)을 digest §15 에 표로 박았다.
- 어긋남 원장 **13 건**(1호 8 · 2호 14 · 3호 18 · 4호 18 · 5호 20 · 6호 14 · **7호 13**).
  ★ **이 계보 최소다** — 1 사이클·반쪽전지라 주장 표면적이 작고 **초록이 자기 결과보다
  세게 말하지 않는다**(2–5 호의 지배 패턴이 없다). 억지로 늘리지 않았다.
  무거운 넷: **D2**(`[인쇄]` Ag 합금 예산 **0.60 mAh cm⁻²** ↔ `[재현]` 자기 조성 +
  Li₁₀Ag₃ 화학량론으로 **0.25**, ≈2.4 배 — Ag 당 Li 8.3 개가 필요한데 상평형 최대가
  3.33 이다) · **D3**(첫 사이클 효율을 한 번도 안 적는다) · **D4**(비가역분 39 % 의
  행방을 계산하지 않으면서 결론에서는 "Li 가 남는다" 고 적는다) · **D8**(Fig. 6
  (0.1 mA cm⁻²·60 °C)의 Ag 를 Fig. 1(30 µA cm⁻²·상온)의 상으로 귀속 — 같은 논문이
  "율이 오르면 Li–Ag 반응이 뒤처진다" 를 보였는데도; Fig. 6 의 조건은 **Methods
  두 범주 어디에도 없다**).
- 산포: `n =`·`N =`·`error bar`·`standard deviation`·`replicate`·`uncertain*` 가
  **본문 13 쪽 + SI 6 쪽 전수 0 회** — **7/7 편 연속**.
  ★ 단 **원자료가 공개돼 있다** — 우리가 산포·검출한계를 직접 잴 수 있는 첫 자리.
- 그림: 크로핑 **11 장 전부 열람**(본문 6 + SI 5). ✅ **6호의 "크로퍼가 핵심 그림
  제외" 사고 없음** — 제외 0 장.
  ★ Fig. 1·3 의 상 막대/시간축과 Fig. 4 의 전압축은 **400 dpi 재렌더 + 화소 좌표
  판독**, 시간축 교정을 **인쇄값(2 mA h cm⁻²)으로 검증**했다.
  ⚠ **Methods 는 260 dpi 로 직접 렌더해 읽었다** — 본문 PDF 폰트가 **µ 를 전부
  떨어뜨려**(`30 µA cm⁻²`→`30 mA cm⁻²`, `5 µm`→`5 mm`) 텍스트 추출값을 그대로 쓰면
  **단위를 세 자리 틀린다.** 이 digest 의 모든 µ/m 는 렌더 이미지 또는 SI 로 교차 확인.
- 후속 후보: 1 순위 **Koerver 2017**(`Chem. Mater.` 29, 5574 — 일곱 편이 모두 안 준
  Q1 의 실험 원전), 2 순위 **Gao/…/Bruce 2022**(`Joule` 6, 636 — 7호 ref 44,
  **같은 그룹의 "저압에서 작동하는 복합양극"**; Q1 과 Q6 을 동시에 칠 수 있다),
  3 순위 **inbox 15번**(3전극 + 압력 — 전극 귀속 공백), 4 순위 **Kasemchainan 2019**
  (`Nat. Mater.` 18, 1105 — 7호 ref 49, 상대극 void; §7 전하 수지의 상대극 쪽 오차원).
- lint 0 errors / 0 warnings.

## [2026-09-22] ingest | `assb` 8호 — Li et al. 2026, safety-aware BMS (Front. Chem. 14, 1960882) ⚠ Mini Review
- 대상: `wiki/raw/papers/li2026_safety-aware-bms-active-intelligence.md` (본문 12쪽, SI 없음, sha256 봉인, PDF `a54b551671eea230…`, doi `10.3389/fchem.2026.1960882`).
- ★★ **ASSB 수집 큐에서 처음으로 성격이 다른 자료다** — 1–7호는 ASSB 미세구조·계면·전극 논문(시뮬레이션 3 + 실험 4), 8호는 **BMS·진단 종설**이고 **ASSB 는 12쪽 중 한 문단(§6.1)** 뿐이다.
- ⚠⚠ **Mini Review 다 — 1차 측정 0, 모든 수치가 재인용.** digest 머리·채움표 행·Evidence 절에 그 사실을 박았다. 근거로 쓰려면 원 논문 필요.
- 그림: 크로핑 **6장**(fig 2 + tab 4) 중 **fig 2장 전부 열람**(Table 3 은 fig_2 크롭에 함께 들어와 이미지로도 이중 확인), 표 4장은 도구 권고대로 PDF 텍스트. ✅ **크로퍼 누락 0** (pymupdf 내장 이미지 2개와 일치). ✅ µ 탈락 위험 없음 (이 PDF 에 µ 필요 수치 0).
- 컴파일: **새 개념 페이지 없음** (1차 근거가 없어 개념을 세울 재료가 안 된다). [[assb-contact-loss-vs-lampe]] 에 Q1~Q8 채움표 행 + Evidence 1절 + 새 제약 1절 + Status Log, [[assb-stack-pressure-operating-window]] 에 산업 요구치 절. ⚠ [[composite-cathode-percolation-utilization]] 은 건드리지 않았다 (339줄 분할 대기 + 내용상 `θ` 에 아무것도 안 준다).
- Q1~Q8: **8편 누적 ≈7.0/8 — 칸은 안 늘었다.** 남은 0 은 **Q1(양극 접촉 손실 정량) · Q4(유일성)**.
- 최대 수확 넷: ① **이 카드의 질문이 BMS 요구 사항으로 인쇄됐다** (`[인쇄]` "diagnostics capable of distinguishing contact loss from ordinary electrochemical aging") ② **Q4 의 성질 변화** — `identifiab*` 5회(1–7호 0회) + Table 4 중기 실패 모드 "Unidentifiable pulse response" (⚠ 측정은 0, 8/8편) ③ **보정된 불확실성 0/8** — 액체셀 17/17·`assb` 7/7 에 이은 **세 번째 비어 있음 원장** ④ **산업 압력 요구치 `<≈1 MPa`** — 실험실 창 2–490 MPa 전체가 그 위.
- 어긋남 **10건** (형태가 다르다 — 자기 실험 0 이라 **인용 어긋남**이 주종): D1 ★★★ 재인용이 원전을 넘어선 것을 **우리 위키로 검증**(`≤0.873 %` ↔ `raw/papers/su2024_drt-soh-health-features.md` 의 5셀 평균·cell5 1.607 %·자기 대조군에 패배) · D2 `poorly identifiable` 인용이 **Si–C 음극 소재 종설** · D3 Fig. 2 가 "lexicographic" 이라 적고 **`min()`** 을 계산 · D4 본문이 **Figure 1 에 없는** safety supervisor 를 Figure 1 의 것이라 부름 · D5 심사 응답 문장이 게재본에 잔존 + Figure 1 은 생성형 AI 제작 + 접수→게재 39일 · D6 PyBaMM 인용 서지가 DOI 와 불일치 · D8 Birkl 2017 이 EIS/DRT 표에 붙어 있고 이 리뷰는 열화 모드를 한 번도 안 씀(`LLI`·`LAM` 전수 0회).
- ★★★ **이 편의 실익은 수치가 아니라 원 논문 지도다** (digest §15, 7편): Xu 2024 (*AEM* 14, 2303539) · Zhang 2025 (*Adv. Mater.* 37, 2413499) · Biçer 2025 (*Batteries* 11, 212) · Liang 2026 (*npj Clean Energy* 2, 16) · LeBel 2022 (*JES* 54, 105303) · Roman 2021 (*NMI* 3, 447) · Thelen 2024 (*npj Mater. Sustain.* 2, 14). ⚠ 1–3순위가 전부 종설이고, 닻의 오랜 1순위 **Koerver 2017 은 이 리뷰가 인용조차 하지 않는다**(참고문헌 48편에 0회).
- lint: 0 errors.

## [2026-09-22] ingest | `assb` 9호 — Huo et al. 2025, sulfide ASSB 양극 열화 + 결합 전기화학-노화 모델 (*JPS* 627, 235830)
- 대상: `wiki/raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md` (본문 11쪽 + **SI(.docx)**, sha256 봉인, PDF `9f2496907f7e65a0…`). SI 는 `zipfile` 로 `word/document.xml` 을 풀어 읽었다 (pymupdf 로 안 열린다).
- ★★★ **큐에서 우리 문제와 가장 가까운 편이다.** 이 계보 최초로 **실험과 파라미터 식별을 한 논문 안에서 잇고**, 그래서 처음으로 **열화 모드의 지분 자체를 적합으로 정한다** (`ε_p` 하나를 푼다). 하이라이트가 `[인쇄]` "The loss of positive active material is identified as the main aging mechanism" + 키워드에 "Parameter identification" + "SOH 평균 오차 1 % 이내".
- 다섯 축으로 캐물은 답: ① 식별 절차 = **1-파라미터 PSO**, 정답축이 **자기 자신의 방전곡선** ② 유일성 증거 **0** (`uncertaint*`·`identifiab*`·`sensitiv*`·`Fisher`·`condition number`·`bootstrap`·`multi-start`·`error bar`·`regulariz*`·`objective function` 전수 0회) ③ **여러 모드를 같이 놓고 지분을 비교한 적이 없다** — `LLI`·`LAM_NE` 는 모델에 **좌표가 없고**(`ε_n` 이라는 파라미터가 아예 없다) `ε_p` 하나만 푸므로 **잔차가 갈 곳이 하나다** ④ fitting 밖의 독립 관측 **0건** ⑤ "1 % 이내" 는 **훈련 잔차**이고 예측 오차가 아니다 — 대조군 **0건**.
- Q1~Q8: **8편 ≈7.0 → 9편 누적 ≈7.5 칸.** 늘어난 것은 **Q6**(압력이 "점·스윕" → **연속 힘 시계열**, `[재현]` 평균 ≈36.9 MPa · 주기 변조 ≈0.32 MPa) 반 칸과 **Q3 의 새 층위**(`fitted-single-parameter`). **Q1·Q4 의 0 은 못 깼다** — 그러나 **Q4 의 성질이 세 번째로 바뀌었다**: 안 쟀다 → 이름이 목록에 올랐다 → **지문이 자기 표 안에 있고 다르게 불린다**.
- 컴파일: **새 개념 페이지** [[assb-lampe-contact-product-degeneracy]] (160줄) — 출판된 P2D 모델의 BV 분모가 **`A^p_eff · ε_p / R_s` 한 조합만** 본다는 것을 **인쇄된 식에서 손으로 유도**했다. 앞의 여섯 개념이 *현상*을 다룬 데 반해 이것은 **역문제**를 다루는 첫 페이지다. [[assb-contact-loss-vs-lampe]] 에 채움표 행 + Evidence 여섯 번째 절 + 새 제약 5개 + Status Log. ⚠ [[composite-cathode-percolation-utilization]] 은 건드리지 않았다 (분할 대기).
- ★★ 가장 단단한 결과 둘: (a) **곱 축퇴** — 자기 SEM 의 입자 반경(≈1.05 µm)을 쓰면 `A_eff` 가 `[인쇄]` 0.4938 → `[재현]` **0.055** 로 **9 배** 움직인다 (b) `[인쇄]` **"파라미터가 흔들려도 적합이 잘 되니 괜찮다" 가 문자로 인쇄되어 있고**("these values are **not disclosed**" + "robustness … remain unaffected, as confirmed by our experimental results"), 같은 논문이 그 명제의 **반례 셋**을 자기 지면에 남긴다 — `R_SEI` 분해가 동일 공정 두 셀에서 **+37 % / −80 %** · 곱 축퇴 · `k_LAM` 셀 간 **2.15 배 vs 보고된 "1 % 이내"**.
- 새 제약 5개: ① **"평탄 상대극 → 5→3 붕괴" 가 모든 ASSB 에 성립하지 않는다** — Li-Si 합금 음극이고 `[재현]` N/P ≈ 3.14 ⇒ 음극 스윙 31.8 %, **합금 계열은 5 파라미터가 그대로 필요하다** ② `θ_AM` 과 `η(i)` 가 한 파라미터에 묶인 실제 사례 (`[재현]` 증폭 1.60/1.32 ⇒ "활물질 손실" 의 ≈37 % 는 모델 안에서조차 활물질 손실이 아니다, **증폭이 상수가 아니라 사후 보정 불가**) ③ 압력을 측정해 놓고 모델에 안 넣는다 ④ **"LLI 없음" 이 관측이 아니라 파라미터 동결의 결과** (`cp0`·`cn0` 고정 + 비공개 + SI 가 CE 제출 거부) ⑤ 우리 폭 측정기가 이 논문에 공급할 것이 있다 (`A_eff·ε_p/R_s` 의 근최적 폭; 필요한 입력은 반쪽전지 OCP 두 곡선 + 비공개 6개 파라미터).
- 어긋남 **9건**(D1~D9) + 공백 12건. ⚠ **크로퍼가 Fig. A.1(부록 DVA)을 빠뜨려 수동으로 뽑았다** — 06호식 누락의 재발(`fig_a1_manual.png`). 그 그림이 논문의 DVA 논거를 담고 있어 빠지면 §6.4 를 못 썼다.
- 후속 후보: 1순위 원전 **ref [27]**(같은 연구실 *eTransportation* 20, 100315 — 모델·PSO·`A_eff` 정의를 전부 위임한 곳) · 2순위 **ref [30] Conforto 2021**(9호가 "정량한 몇 안 되는 문헌" 으로 지목하고 "오차가 비교적 크다" 로 기각 — **relaxed OCP + EIS-PSD** 라 우리 축과 직결) · 3순위 **ref [21] Yu 2024 DRT**(병합 원호를 가르는 도구, 8호의 DRT 처방과 이어진다).
- ⚠ 이 흡수는 에이전트가 API 오류(529·500)로 두 번 끊겨 **닻·index·log 연결은 본 세션이 직접 마무리**했다.
- lint: 0 errors.

## [2026-09-22] ingest | `assb` 10호 — Vadhva, Hu, Johnson 외 2021, EIS for All-Solid-State Batteries: Theory, Methods and Future Outlook (*ChemElectroChem* 8, 1930–1947) ⚠ Review
- 대상: `wiki/raw/papers/vadhva2021_eis-for-assb-theory-methods.md` (본문 **18쪽**, **SI 없음** — 업로드 큐에 `10._Sup_*` 부재 + 본문에 supporting/supplementary **0회**, Reviews 형식이라 원래 없다; sha256 봉인, PDF `537a508716afd2b3…`, doi `10.1002/celc.202100108`, **CC-BY open access**).
- 저자·소속 확인: **Vadhva⁺ · Hu⁺ · Johnson⁺** (⁺ 공동 1저자, `[인쇄]` "These authors contributed equally") + Stocker · Braglia (**HORIBA MIRA Ltd., 기업 — 확인 완료**) + Brett + **Rettie**(교신). UCL Electrochemical Innovation Lab + **The Faraday Institution**. 자금 **LiSTAR** + **HORIBA-MIRA/UCL/EPSRC CASE studentship**.
- ⚠ **Review 다 — 1차 측정 0, 그림 14장 중 12장이 재수록.** 8호 규율을 적용하되 **층위를 갈랐다**: 수치는 `[재인용]` 이고, **"이 방법은 이런 조건에서 이런 한계가 있다" 는 저자들의 1차 방법론적 주장**이다 (digest §12). 이 구분이 이 흡수의 핵심이다.
- 그림: 크로핑 **15장 = Fig. 1–14 + Table 1, 누락 0** (논문의 도표가 그것뿐 — 본문의 "Table 3" 은 `[인쇄]` "cf Table 3 in **Ref. [129]**" 로 남의 표). ⚠ `fig_7.png`/`fig_8.png` 가 같은 두 단 영역을 **중복** 크롭(누락 아님). **실제로 열어 본 것 8장 — Fig. 2·5·6·7·8·9·11·12.** 안 본 것 6장(Fig. 1·3·4·10·13·14 — 정현파 모식도·4단자 기하·3전극 모식도·LLZO 입계·폴리머 대칭셀·폴리머 완전지, 우리 축에 안 걸린다). Table 1 은 도구 권고대로 PDF 텍스트로 전사. 추가로 **본문 4곳을 페이지 렌더로 확인**(Eq. 3 · Eq. 5 · "~10⁹ orders of magnitude" · `μAh`). ✅ **µ 탈락 없음** — 이 PDF 는 `μAh`·`μm` 를 정상 추출하고 렌더로 재확인했다.
- Q1~Q8: **9편 ≈7.5 → 10편 누적 ≈8.0 칸.** ★★★ **`Q4` 의 0 이 처음으로 깨졌다.** 깬 방식을 정확히: **"우리 대신 쟀다" 가 아니다** — `identifiab*`·`uncertaint*`·`confidence`·`condition number`·`error bar` **전수 0회**, 조건수·프로파일 가능도·근최적 폭·Fisher/CRB 전부 0, **유일성을 수치로 잰 `assb` 논문은 10/10 편 중 0편**. 깬 것은 **"축퇴가 일반 현상임을 방법론으로 인쇄했다"** 이다: `[인쇄]` "**As no solution to an EIS spectrum is unique**" · "**the inclusion of more elements will tend to improve the fit**" · "how many time constants … **highly subjective**" · DRT 는 **`ill-posed`, regularization 필요** · 모델 선택을 **AIC**(Akaike)로 명명하고 `[인쇄]` "thorough validation against experiment in the context of ASBs is **desirable**" 로 **열린 문제 등록**. ⇒ Q4 의 성질이 **네 번째로** 바뀌었다 (안 쟀다 → 이름이 로드맵에 → 지문이 자기 표에 → **방법 자체가 비유일하다는 것이 분야의 공식 문장**). ⚠ **`Q1` 은 10/10 편 여전히 0.**
- ★★★ **9호 §5.1("하나의 원호에서 두 시상수")에 정식 근거를 준다** — 판정 5문장(위) + 처방 5개: **K–K / Lin-KK 사전 검증**(ref. 41–43, Schönleber 소프트웨어) · **DRT 로 시상수 개수를 먼저 정한다**(ref. 62 Pang — `[인쇄]` "unambiguously identified three semicircles") · **조건을 바꿔 시상수를 벌린 뒤 구속으로 되가져온다**(ref. 82 Bron: −130 °C 에서 `R_gb` 동정 → 실온 추적 / ref. 28 Krauskopf: 400 MPa 로 `R_int` 제거 → GB 노출) · **상보 대칭셀 쌍**(ref. 70·126·161) · **AIC**(ref. 51·52). **9호는 그중 하나도 쓰지 않았다** (`Kramers`·`Kronig`·`DRT`·`symmetric cell`·`AIC` 전수 0회). `[재현]` 9호 회로의 자유 파라미터는 **9개**(`R_b`1 + RQ3 + RQ3 + W2)인데 **분해 가능한 원호는 1개**다.
- ★★★★ **가장 단단한 그림 두 장** (둘 다 열어서 봤다): (a) **Fig. 5** — (a)패널의 **물리적으로 구별되는 9개 층 회로**가 (b)패널에서 **`R_b` + (R_SEI∥CPE) + (R_ct+W ∥ CPE)** 로 접힌다. `[인쇄]` "many physical elements may be **negligible or convoluted**". **그 접힌 회로가 9호의 회로와 글자 그대로 같고, 리뷰는 그것을 물리 분해가 아니라 "9개가 접힌 결과" 로 소개한다.** 게다가 **(b)의 Nyquist 에는 원호가 실제로 둘 보인다**(`[도표]` R_b≈18 · R_SEI 18→70 · R_ct 70→178 Ω). (b) **Fig. 8** — 같은 황화물족 **5개 중 3개만** 입계가 분해된다(같은 −130 °C, 입계는 5개 모두에 물리적으로 존재).
- ★★ **DRT 를 다룬다 — 그리고 비판적으로**(`DRT` 13회). 8호의 "Ill-posed inversion needs regularization" 처방이 EIS 쪽 1차 진술로 확인되고, 개선 경로 3개 + 원전이 붙는다: **일반화 DRT**(Danzer 2019, 저항-유도성 원소 + 전처리 제거) · **Bayesian DRT**(Huang 2020) · **2D DRT**(Mertens 2017). ⚠ 자기 DRT 계산은 0(Fig. 6d 는 재인용).
- ★ **새 명제 하나 — 리뷰가 다섯 곳에 흩어 놓은 것을 우리가 모았다: "분해 가능한 RC 의 개수는 실험 조건의 함수다"**: 황화물 5중 3만 입계 분해 · `[도표]` LGPS 는 **실온에서 원호 0개**(그런데 σ=12 mS cm⁻¹ 가 그 절편에서 나온다) · `[도표]` 400 MPa 에서 `R_int` 가 사라져야 GB 등장 · 폴리머는 60 °C 위에서 상경계 소멸 · ★★ `[인쇄]` **LiPON 박막의 노화가 RQ 를 3→4개로 바꾸고 새 RQ 의 귀속이 "Li|LiPON interface **and/or** in the LCO bulk"** (Larfaillou 2016) ⇒ **모델 차수가 상태변수**이고 **저항 하나가 어느 전극 것인지 모르는 채 열화 서사에 들어간다**.
- ★ **이 카드 Q2 직격**: `[인쇄]` In|LGPS|LCO 의 중주파 양극 계면 저항 증가가 "**loss of interfacial contact in the composite cathode due to volumetric expansion** **and** the **formation of a decomposition layer on exposed LCO**" — **접촉 손실과 계면상 성장이 한 `R_MF` 에 함께 귀속**되고 가르는 관측은 없다. ⇒ **EIS 는 곱 축퇴를 깨는 대가로 새 축퇴를 들여온다.**
- ★ **Q5 새 경고 둘**: ① `[인쇄]` **In 음극 계면 저항이 한 번의 방전 안에서도 리튬화도(In-rich 화)로 크게 증가** ⇒ 4호의 `[도표]` `R_LF` ≈157배에서 **노화분과 SoC 분이 안 갈린다** ② `[인쇄]` **In–Li 음극 셀은 LMA 셀과 전극↔주파수 귀속이 반대** ⇒ **"저주파=양극" 같은 보편 규칙이 없다**, 9호의 `R_SEI`/`R_ct` 귀속은 무보증.
- ★ **Q6**: `[인쇄]` ~120 MPa(σ 포화, 단 인가 최대압) · ~400 MPa(Li₆PS₅Cl, ref. 84 = **Doux JMCA 2020 — 우리 5호의 자매 논문**) · `[도표]` 400 MPa. **개념 기여가 값보다 크다**: 이력의 **산화물 독립 재현**(`[인쇄]` "<1 Ω cm², remained after the pressure was removed") + **압력이 관측 분해능 연산자**.
- 컴파일: **새 개념 페이지 없음** (이 논문의 명제는 기존 두 페이지의 같은 축이고, 만들면 "EIS 일반 설명" 으로 흐른다 — SCHEMA Page Thresholds + 이 세션 지침). 대신 [[assb-contact-loss-vs-lampe]] (채움표 행 + Evidence 일곱 번째 절 + 새 제약 7개 + Status Log) · [[assb-lampe-contact-product-degeneracy]] ("EIS 는 대가를 받는다" 절) · [[assb-stack-pressure-operating-window]] (이력 재현 + 분해능 연산자 절) · [[fitting-degeneracy]] ("같은 축퇴가 다른 관측 영역에서는 공식 문장" 절). ⚠ [[composite-cathode-percolation-utilization]] 은 건드리지 않았다 (분할 대기). **기존 EIS 페이지 중복 확인**: [[zhang2020-eis-aging-dataset]] 는 **액체셀 데이터셋 전용**이라 겹치지 않는다 — 오히려 ★ **이 리뷰가 ML+EIS 의 예로 드는 ref. 174 가 바로 그 논문**이고, **우리 위키가 리뷰보다 한 칸 앞서 있다**(`state I~IX` 중 넷이 DC 전류 중 = 리뷰 자신의 `stability` 요건 위반, 모드 라벨 0, ARD 두 주파수 비식별).
- 어긋남 **6건** — **방법론적 주장 자체에는 어긋남을 못 찾았다**: **D1 ★ Eq. (5) 위상각이 `tan⁻¹(Re/Im)` 으로 뒤집혀 있다**(표준은 `Im/Re`; EIS 방법론 리뷰의 이론 절, 220 dpi 렌더로 확인) · **D2 Eq. (3) 차원 불일치**(`sin(ωt+Δt)` 이고 본문이 "(ωt+Δt) is the phase angle" — Fig. 1 은 Δt 를 시간 축에 그린다) · **D3 "spans ~10⁹ orders of magnitude … (mHz to MHz)"** (9자릿수다) · **D4 본문↔캡션 패널 글자 한 칸 어긋남**(본문 "Figure 6a = Pt|LiPON|Pt" ↔ 캡션/그림 "6a = SEM, 6b = Pt|LiPON|Pt") · **D5 라운드로빈 인용 번호 오류** — `[인쇄]` "Ohno et al.**[85]**" 인데 ref.[85] 는 Kraft *JACS* 2018 이고 라운드로빈은 **ref.[191] Ohno *ACS Energy Lett.* 2020**(같은 논문 p.1944 는 [191] 로 올바르게 인용) · **D6 저주파 인덕턴스에 두 이름** (Table 1 = "degradation processes" ↔ §7 = "measurement artefact, due to the violation of the QSS condition"). 공백 8건(G1~G8).
- ⚠ **재인용 수치는 이 위키의 근거로 쓰지 않는다**: `22 % / ~10 %`(라운드로빈) · `~120 / ~400 MPa` · `<1 Ω cm²` 전부. 특히 라운드로빈은 **인용 번호마저 틀렸다**(D5).
- 후속 후보 9편 + 도구 1: 1순위 **Ingdal, Johnsen, Harrington** *Electrochim. Acta* 2019, 317, 648 (**AIC 로 등가회로 순위 — Q4 의 계산기**) · 2순위 **Ohno et al.** *ACS Energy Lett.* 2020 (라운드로빈 원전, **Q3**) · 3순위 **Bron, Dehnen, Roling** *JPS* 2016, 329, 530 (**저온으로 축퇴 깨기의 실물**) · 4순위 **Zhang, Weber, …, Zeier, Janek** *ACS AMI* 2017, 9, 17835 (**In|LGPS|LCO — 접촉 손실 + 분해층이 한 저항에 묶인 원전**, 4호 검증용) · 5순위 **Krauskopf et al.** *ACS AMI* 2019, 11, 14463 (**Q6** 압력 이력의 산화물 판) · 6순위 **Doux et al.** *JMCA* 2020, 8, 5049 (5호의 자매) · 7순위 **Kaiser et al.** *JPS* 2018, 396, 175 (**TLM 으로 복합전극 이온 굴곡도 정량 — `θ_AM` 에 가장 가까운 실측 채널**) · 8순위 **Huang, Papac, O'Hayre** *Electrochim. Acta* 2020, 367 (**Bayesian DRT** — 8호의 "calibrated uncertainty" 와 직결) · 9순위 **Larfaillou et al.** *JPS* 2016, 319, 139 (**모델 차수가 상태변수**의 원전). 도구: **Schönleber Lin-KK**(KIT 2015). ⚠ 정정: ref.[190] **Bielefeld 2020 *ACS AMI*** 는 우리 1호(Bielefeld 2019 *JPCC*)와 **다른 논문**이다.
- lint: 0 errors.

## [2026-09-22] ingest | Yu et al. 2024 — 황화물 ASSB 완전지의 시간분해 EIS–DRT 노화 분석 (`assb` 11호, 큐 38번을 당겨서)

- raw: `raw/papers/yu2024_drt-time-resolved-aging-sulfide-assb-fullcell.md` (본문 8쪽 + **SI `.docx` 7,607자 + 그림 S1–S5**, 둘 다 sha256 봉인). *J. Power Sources* **597** (2024) 234116 · **Schaeffler Transmission Systems LLC**(산업체) + **Ohio State University** · `[인쇄]` "0378-7753/© 2024 Elsevier B.V. **All rights reserved**" (open access 아님) · `[인쇄]` 자금 "**internally funded by the Schaeffler group**".
- **순서를 당긴 이유 (사용자 결정)**: 10호(Vadhva 2021)가 DRT 를 `[인쇄]` "ill-posed … requiring regularization" 으로 판정하고 **λ 선택 규칙을 공백(G4)으로 남겼는데**, 38호가 **그 DRT 를 실제로 돌린 첫 `assb` 논문**이다. 짝으로 읽는 값이 컸다.
- **그림 14장 등록 · 12장 열람**: 본문 Fig. 1–8 + Table 1(크로퍼 9장, 논문 도표와 **누락 0**) + ★ **SI 가 `.docx` 라 크로퍼가 못 읽어 `zipfile` 로 `word/media/image1–5.png` 를 직접 꺼내 `fig_s1–s5.png` 로 등록**. 실제로 연 것은 Fig. 1·2·3·4·5·6·7·8 + S1·S2·S3·S4·S5 (Table 1 은 텍스트). **텍스트만 긁었으면 §10·§12·§13 세 절을 통째로 놓쳤다.**
- ★★★ **9호(Huo 2025) §5.1 에 대한 답 셋**: ① DRT 는 같은 화학의 완전지에서 `[인쇄]` **P1–P5 다섯 개**(Fig. 8 지도로는 P1′ 포함 **여섯 + W**)를 주장하고 `[도표]` 실측 국소 극대는 48 사이클에 **5개** ⇒ **9호의 RC 2개는 2–3배 차수 미달**. ② ★★ **그러나 38호의 개수도 절대 기준이 아니다** — 개수가 **사이클(↑)·조작(↓)·배선**의 함수다. ⇒ 9호의 문제는 "2개 대신 5개" 가 아니라 **"개수를 고르는 규칙이 문헌에 없다"** 이고, 후보(AIC)를 10호가 열어 뒀는데 **38호도 안 쓴다**(`AIC`·`Akaike` 0회). ③ 9호의 `R_SEI` **+37 % / −80 %** 와 같은 자릿수의 변동이 38호 SI 에 **셀을 건드리지 않고** 나타난다(아래).
- ★★★★ **10호의 λ 공백은 메워지지 않았다 — 더 깊어졌다.** `regulariz*`·`lambda`/`λ`·`L-curve`·`GCV`·`cross-valid*`·RBF shape factor·`Kramers`·`Kronig`·`uniqu*`·`ill-posed`·`uncertaint*`·`confidence`·`error bar`·`identifiab*`·`condition number`·`Fisher`·`Bayes*`·`overfit*`·`degenerac*` — **본문 8쪽 + SI 전수 0회.** 유일한 방법 서술이 `[인쇄]` "MATLAB-based DRT calculation code developed by **T.H. Wan et al. [16]**" 한 줄이고, SI 는 DRT 를 **보통의 적합 문제**로 소개하며 `[인쇄]` **"The well-fitted `Z_DRT` can represent the actual physics in the system"** 이라고 쓴다 — 10호의 정반대 진술. `[재현]` 10호 처방 **14항목 채점: ✅ 2 · ⚠ 5 · ❌ 7**.
- ★★★★★ **이 흡수의 최대 수확 — SI Fig. S3.** 같은 셀(로 보이는 것)을 **배선만 바꿔** 잰 두 DRT 가 `[도표]` ≈3.5×10⁵ Hz **117 → 105 (−10 %)** · ≈3×10³ Hz **78 → 66 (−15 %)** · ≈3×10⁻² Hz **45 → 76 (+69 %)** 이고, **≈2×10⁴ Hz 의 분해된 어깨가 한쪽에만 있다**. 그런데 **본문의 재가압 효과가 P1 −11 % · P2 −10 % · P3 −16 % · P4 −25 %** 로 **전부 그 폭 안**이다. **논문은 두 숫자를 나란히 놓지 않는다.** ⚠ 단서 셋(배선 변화의 일부는 진짜 물리 · 두 측정 대역 1 MHz ↔ 2 MHz · SI 가 "같은 셀" 을 명시 안 함) → **69 % 는 상한**.
- ★★★★ **두 번째 폭 재료 — 이름표의 불확정성이 이름표 간격보다 크다.** `[재현]` P3 의 보고 위치가 한 논문 안에서 **500 Hz – 10 kHz = 1.3 자릿수**(본문 4곳 + Table 1 + 그림 3곳)인데 **P2↔P3 간격은 0.8 자릿수**(`log₁₀(6000/900)=0.82`). Table 1 이 **P2 = 화학 접촉 · P3 = 기계 접촉**이므로 **화학/기계 분리가 그 자리에서 무너진다.**
- ★★★ **"모델 차수는 상태변수" 가 1차 데이터로 네 번 확인됐다** (10호가 Larfaillou 2016 재인용으로만 전한 것): `[도표]` 완전지 국소 극대 **2–3(4cy) → 5(48cy)** · micro-SE 반쪽 **1 → 2** · graphite 반쪽 **P4 가 없던 평탄에서 생긴다** · **재가압 후 완전지 4 → 3**. ⚠ **논문은 세 번 다 "봉우리가 커졌다" 고 적고 "생겼다" 고 적지 않는다.**
- ★★★ **논문 자신의 결론 지도(Fig. 8)가 축퇴를 그림으로 인쇄한다**: **P2·P3 에 `Cathode`+`Anode` 를 둘 다 찍고**, **P4(음극 CT)와 P5(양극 CT)를 ≈10 Hz 에서 겹쳐 그리며**, **(P1′) 은 측정 대역(2 MHz) 위라 회색 점선**이다(= 못 본 봉우리를 지도에 그려 넣었다).
- Q1~Q8: **11편 누적 ≈8.5/8.** ✅ **Q1 반쯤 깨짐**(P3 봉우리 높이 = 주파수로 국소화 + 시계열 + 조작으로 되돌려지는 첫 대리량; ⚠ 무차원 아님·전극 안 갈림) · ✅✅ **Q6 의 마지막 빈칸 `압력 → 용량` 채워짐**(반쪽 3점 `[인쇄]` 165.0/166.9/**173.1**, 완전지 2점 169.9/171.7 — 10/10편이 못 주던 것) · ★★★ **Q8 이 이 카드의 출발 전제를 깸**(**계보 최초 graphite 음극 완전지** ⇒ "전고체 음극은 평탄 → 5→3 붕괴" 불성립; 9호 Li-Si 에 이은 두 번째 반례, 이쪽은 **상용 흑연**) · ⚠ **Q3 후퇴**(`[인쇄]` "The authors do not have permission to share data", **파라미터 표 자체가 없다** — 9호는 "not disclosed" 를 찍기라도 했다; **어느 셀이 Cl 이고 어느 셀이 Br 인지도 안 밝힌다**) · **Q4 는 0 / 11** (성질만 다섯 번째로 바뀜).
- ⚠ **압력 연산자의 비직교성 반례**: 재가압(>500 MPa)이 P1 −11 % · P2(**화학**) −10 % · P3 −16 % · P4(**전하이동**) −25 % · 무표기 0.03 Hz **−27 %** 를 **전부** 줄인다 ⇒ [[assb-pressure-reapplication-separation-test]] 의 `P` 가 `θ_AM` 에만 들어간다는 분해에 반례. **`confidence: low` 유지.** 그리고 **회복 크기가 4호의 1/12**(`[재현]` +4.91 % vs +60.5 %p)인데 `[인쇄]` "agree with previous report by Ceder et al. [21]"(= 우리 4호) 로만 적고 **크기를 비교하지 않는다**.
- 컴파일: **새 개념 1** [[drt-peak-count-nonidentifiability]] (**C1–C5 체크리스트** · λ 격자로 [[near-optimal-set-width-measurement]] 이식 설계 · 새 provenance 층위 **`inverted-nonunique`**; 200줄 안) + [[assb-contact-loss-vs-lampe]] (채움표 11행 + Evidence 여덟 번째 절 + 새 제약 5개 + Status Log + "주장하지 않는 것" 4항) + [[fitting-degeneracy]] (Q4 계보 다섯 번째 형태) + [[assb-pressure-reapplication-separation-test]] (11호 반례 절) + `index.md` 등록. ⚠ [[composite-cathode-percolation-utilization]] 은 건드리지 않았다 (분할 대기). **중복 확인**: `raw/papers/su2024_drt-soh-health-features.md` 는 **액체셀 DRT feature + GPR** 이라 겹치지 않고, 새 개념 페이지의 source 로만 넣었다.
- 어긋남 **18건** (10호 6 · 7호 13 · 8호 10 보다 많다). 주장을 직접 약화시키는 것 6개: **D1** DRT 전처리가 두 가지로 서술되고 그림마다 다르게 적용(Fig. 2 캡션 "**simulated** Nyquist curves 위에서" ↔ SI "**measurement data** 에서 뺀다") · **D2** P1 주파수가 Table 1/Fig. 8 `>10⁶ Hz` ↔ 본문 1.2×10⁵ / 160 kHz / ~10 kHz ↔ `[도표]` 8×10⁴–1.6×10⁵ (**최대 2자릿수**) · **D3** `[인쇄]` "P3 만 줄었다" 가 그림에 없다(전부 줄고 최대는 무표기 봉우리) · **D10** 본문이 자기 Fig. 1 을 "a single flattened semi-circle" 이라 묘사하는데 `[도표]` **원호 2개 + 꼬리**다 · ★ **D11 Fig. 1 은 "Illustration" 이 아니라 Fig. S3 하단의 실측**(7개 특징이 판독 오차 안에서 일치) · **D13** DRT 가 측정 하한(0.1 Hz) 밖 ≈2–3×10⁻² Hz 에 **두 번째로 큰 봉우리**를 놓는다. 나머지 12건은 편집 수준(D5 축 기호 `g(τ)`↔`γ(τ)`·정규화 질량 미공개 · D7 Table 1 증거 칸 오기 2건 · D12 봉우리 명명 체계 3벌 · D15 `Z_imag` 눈금 없는 Nyquist 3장 …). 공백 9건(G1~G9).
- 후속 후보: 1순위 ★★★ **Wan, Saccoccio, Chen, Ciucci, DRTtools** *Electrochim. Acta* 184 (2015) 483 (**38호의 DRT 가 전부 이 코드**이고 λ·RBF shape factor 가 이 논문의 인터페이스 — **G1 을 닫는 유일한 경로**) · 2순위 ★★★ **Hori, Kanno, …, Ivers-Tiffée** *JPS* 556 (2023) 232450 (같은 재료계 EIS–DRT, **봉우리 귀속의 외부 검증**) · 3순위 ★★★ **Danzer, generalized DRT** *Batteries* 5 (2019) 53 (10호가 지목, **38호가 인용만 하고 안 쓴다** — 케이블 인공물 문장에 매달았다) · 4순위 **Ciucci 2019 + Huang/Papac/O'Hayre Bayesian DRT 2020** · 5순위 **Pan, Zou, Canova, Zhu, Kim** *JPS* 479 (2020) 229083 (38호 교신저자의 선행 DRT, 케이블 인공물의 1차 근거, **Si 음극이라 `pvs-sev` 계열과도 겹친다**) · 6순위 ★ **Illig 2012 (JES 159 A952) + Schmidt 2011 (JPS 196 5342)** (**P3 = "solid-solid contact impedance" 귀속의 원전** — 액체셀 LFP/Al 집전체의 주파수대를 황화물 복합양극에 이식한 것이 정당한지 확인해야 한다) · 7순위 **Minnmann 2022** *AEM* 12 2201425 · 8순위 **Gaberšček** *Nat. Commun.* 12 (2021) 6513 · 9순위 **Höltschi 2021** *Electrochim. Acta* 389 138735 (graphite 음극 ASSB 열화 — Q8 이 연 새 축).
- lint: 0 errors.

## [2026-09-22] ingest | `pack-fault` 1호 — Lai, Ke, Tang, Zheng 2025, Balanced capacity-based quantitative method for detecting ISC in Li-ion battery modules (*J. Energy Storage* 123, 116622) ⚠ assb 아님 — 새 섹션 개설
- 큐 39번. **`assb` 가 아니다** — 액체셀 6S2P SONY US18650VTC5 모듈의 ISC 검출·정량. 2026-09-22 사용자 결정으로 **`pack-fault` 섹션을 새로 열었다** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-f-1 설계 그대로): SCHEMA Tag Taxonomy 시드 + 경계 둘(① `assb` 병기 금지 ② LLI/LAM 페이지에 부착 금지) · 닻 [[isc-detection-vs-balancing-masking]] (자기 물음 P1~P6, `assb` Q1~Q8 미사용) · 데이터셋 entity [[isc-balancing-dataset-est-d-24-12331]]. **태그 승격 3 페이지 판단**: 닻 + digest + entity — entity 는 억지가 아니라 **논문에도 digest 에도 없는 독립 내용**(열↔그림 사상 `[재현]`, 재현 불가 원장, 상태 추적)을 담으므로 정당하다고 판단했다.
- raw: `raw/papers/lai2025_balanced-capacity-isc-detection-modules.md` (sha256 봉인). 크로퍼 **15 장**(Fig. 1–8 + Table 1–7); **Fig. A.1/A.2 누락** → p.7 렌더로 읽음. **실제로 본 것: Fig. 1–8 전부 + A.1/A.2.** Fig. 5(a) 크롭의 y 라벨 잘림 표시. µ 탈락 없음(누설 mA · 균등화 A 급).
- ★ `ISC_LEAKAGE_DATASET.md` §5 의 7 물음: ① 셀 #1 — `[인쇄]` "the weakest battery, say, #1, is paralleled with an accurate external short circuit resistance" ② Ω · 2.5 Ah · 6S2P · 25±2 °C · "NCM" ③ **17 열 — 논문 무언급 (미해결)**, `[재현]` 파일 내 카운터, 파일 간 불연속 ④ **165 = Test 5 = 설계**(충·방전 반복 프로파일, 능동 ≈870 min = 522,000 행 × 0.1 s 정확 일치; 수동 ≈720 min → 깨진 파일) → **재현 불가 원장**: Table 3 Test 5 · **Table 6 수동(추정 SoH 의 유일한 수동 숫자)** · Fig. 2(b)(d) · 5(b) · 8(b) ⑤ **검출 + 정량(식 12 닫힌 형태), 폭 0** — `identifiab*`·`uniqu*`·`confidence interval`·`uncertaint*`·`error bar`·`condition number`·`Fisher`·`regulariz*` 전수 0 (재집계 일치), 조건당 1 회; 용량 편차만 칸(SoH 정규화), **자기방전은 정의로 배제**(각주 2), 온도 고정, 다중 셀 배제 ⑥ 논문 "less influenced by the balancing method" ↔ `[도표]` 서명 부호 반대(Fig. 3 능동 +0.23 / Fig. 4 수동 −0.08 Ah) + Test 5 SoH 민감도 **능동 0.13 ↔ 수동 6 %/%** (프로토콜 혼입) ⑦ **누설 = derived** (`[인쇄]` "dividing the average battery voltage by the short-circuit resistance"), 저항 허용오차 없음; 수동 균등화 전류도 식 (4) 계산값.
- ★★ **공개 데이터 대조** (`55_passive`·`55_active` 전수): 열 14 인덱스 0 = 셀 #1; 열 12 의 대상별 적분 = Fig. 4 (−0.088/−0.49/−0.566/−0.687/−0.853/−0.861 Ah, 0.01 Ah 안); 능동은 **+ 열 13 환류 0.714 Ah(6 셀 공통)** = Fig. 3 (+0.229/−0.225/…). → §3 의 "177 배" 는 환류 항의 유무. `max|열 12|` 1.566 A ≈ V/2.5 Ω · 2.786 A ≈ "about 2.7 A". ⚠ 끝 행 환경 온도 27.53 °C (25±2 상한 초과, 두 행 표본).
- ★ **유일성 구조** (`[해석]`): 주어진 `(l, SoH)` 아래 `i_L` 유일 → 그 조건을 풀면 `(i_L, SoH_l)` 에 flat valley (Fig. 7: 330 Ω ±2 % → >100 %) · **자기방전 방향은 정확 null** · 식 (10) 15 쌍 절댓값 합 ↔ 식 (12) max−min 한 쌍 불일치. 구분 시험 후보: **부하 방향 반전**(Fig. 5(b) 에서 누설 셀이 최소 방전 셀이 아니다).
- 어긋남 **14 건**, 주장 약화 5: **D3** "not rely on specific load profiles" ↔ ">10 h" 권고 · **D5** Table 7 이 `R_isc %` 와 `I_leak mA` 를 섞고 "superiority" (`[재현]` 330 Ω 상대 오차 −7 %) · **D7** Test 5 능동/수동 프로토콜 다름(5 사이클 ↔ 2 사이클) · **D8** Fig. 5(b) 무언급 반전 · **D9** 수동 Test 5 에서 **틀린 SoH 가 오차를 0.84 → 0.31 mA 로 개선**(상쇄). 편집급: D10 Appendix B `a=3.01, b=−0.10` 단위 불일치(`s≈0.1 V` → SoH ≈0.2 %) 등. 공백 12 건(G1~G12).
- 컴파일: [[fitting-degeneracy]] 에 **관계 절 한 개(링크만, 태그 없음)** · `index.md` 2 건 등록(43 페이지) · SCHEMA 시드. `assb-contact-loss-vs-lampe.md` 는 **건드리지 않았다.**
- 후속 후보: ★★★ **Tang 2023 *CEJ* 476 146467** (`R_isc` 2 %, aging-insensitive — 정규화 물음의 원전) · ★★★ **Lai 2023 *JPS* 573 233109** (±1 mA float-charging 원전) · ★★ **Kong 2018 *JPS* 395 358** (Table 7 "Sensitive to balancing" — 닻 물음이 문헌에 처음 인쇄된 자리 후보) · ★★ **Tang 2022 *IEEE TIE* 69 8055** (균등화 전류로 SoH — 순환 우려의 원전) · ★★ Shen 2023 *GEITS* · ★ Lai 2018 *EA* 278 (시불변 가정 근거) · ★ Liu 2020 *Appl. Energy* 259 (병렬 저항 대리 타당성) · ★ Song 2023 · ★ Lai 2023 *Energy* 282 + Tang 2021 *iScience* (Appendix B·플랫폼 원전).
- lint: **0 errors · 0 warnings** (43 pages, 39 raw).

## [2026-09-22] ingest | `assb` 12호 — Sadegh Kouhestani, Yi, Qi, Liu, Wang, Gao, Yu, Liu 2022, Prognosis and Health Management (PHM) of Solid-State Batteries: Perspectives, Challenges, and Opportunities (*Energies* 15, 6599) ⚠ Review
- 큐 **11번** — 38·39 를 당겨 끝낸 뒤 **큐 순서로 복귀한 첫 편**. raw: `raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md` (본문 **26쪽** = 텍스트 21 + 참고문헌 131편 5쪽, **SI 없음** — 업로드 큐에 `11._Sup_*` 부재 + 본문 `supplement*`·`Appendix` **0회**; sha256 봉인, PDF `912b3d1df0233ba4…` 실측 일치, doi `10.3390/en15186599`, MDPI **CC BY**). 소속 Kansas(ME) + USTB + North Minzu ×2, 교신 Lin Liu. 접수 2022-08-24 → 승인 **09-02 (9일)**.
- ⚠ **Review — 1차 측정 0. 그림 7장 전부 타 논문 재수록**(`[인쇄]` "Adapted with permission" refs 15/30/31/31/40/41/29): **LIB 그림 6장 + Palacín 2009 모식도 1장** ⇒ **이 논문에 SSB 데이터 그림은 0장**이다. `[인쇄]` 는 10호·8호 규율대로 "이 지면에 이렇게 적혀 있다" 의 뜻. 크로핑 **8장(Fig. 1–7 + Table 1), 누락 0. 실제로 열어 본 것: Fig. 1·2·3·4·5·6·7 전부**(Table 1 은 텍스트 전사). ⚠ 텍스트 추출이 `ﬁ` 합자를 보존해 첫 키워드 집계에서 `identif*` 가 0 으로 나왔다 — **합자 정규화 후 재집계**(`identification` 5회 · `identifiab*` 0회). 앞으로 pymupdf 텍스트는 합자를 먼저 푼다.
- Q1~Q8: **12편 누적 ≈8.5/8 유지 — 새 칸 0.** Q1 없다(`contact loss` 0, `contact area` 3회 전부 재인용·값 0) · Q2 없다(리뷰) · Q3 해당 없음(SOH 스칼라 식 (6), 모드 라벨 0, Table 1 열 둘뿐, `Data Availability: Not applicable`) · **Q4 0/12** · Q5 0 · Q6 재인용 1값(`0.4–1 MPa`, 출처 미확정) · Q7 0 · Q8 없다(V–Q·OCP 0장).
- ★★★ **판정 한 줄 (Q3·Q4)**: **12호는 채움표에 칸이 아니라 날짜를 더한다.** ① `[인쇄]` §2.2 "**The loss of active materials mainly stems from the electrical contact loss** that is caused by graphite spalling, adhesive decomposition, collector corrosion, and electrode particle cracking" ⇒ 2022년 PHM 어휘에서 **`LAM ⊃ 접촉 손실`** — 이 카드의 분리 물음이 **정의 차원에서 없는** 분류 체계. 기구 목록은 **전부 액체셀**, `[도표]` Fig. 6 의 "Contact Loss" 두 자리도 **Cu/Al 집전체**. ② Q4 성질은 **8호 이전(1–7호 "안 쟀다")으로** — `identifiab*` **0**(8호 5), 가장 가까운 어휘 "difficult parameter identification"(실무 곤란), 그리고 **같은 논문이 모델 차수에 대해 정반대 두 문장**(§3.1.2 "inevitable errors in each parameter" ↔ §3.1.3 "the more parameters … the higher the accuracy"). ⇒ **2022 → 2026 사이 PHM 문헌은 "identifiability" 라는 이름을 얻었고(0 → 5회) 여전히 재지 않았다.**
- ★★ **`A_eff` 형 접촉 파라미터의 계보 입구**: `[인쇄]` §3.1.1 "Tian et al. [60] and Shao et al. [60] introduced **a parameter to describe the contact area, which adjusts the current density in the 1-D Newman model** … capacity drop was correlated with the loss of contact area … medium compressive pressures (0.4–1 MPa)" = 9호(Huo 2025) `A^p_eff`(BV 분모)와 **같은 형태** ⇒ [[assb-lampe-contact-product-degeneracy]] 의 곱 축퇴가 **2017년 모델 형태(Tian & Qi *JES* 164, E3512)부터** 있을 가능성; Shao 2022 (*Energy* 239, 121929)는 거기에 **압력 의존**을 얹은 후보. ⚠ **두 저자에 같은 번호 [60]**(D4) → `0.4–1 MPa` 출처 확정 불가. 9호가 Tian & Qi 를 인용하는지는 **확인 안 함**.
- ★ **"모델 차수는 상태변수" 세 번째 독립 인쇄** (액체셀 ECM, 재인용 [84] Cho 2012): `[인쇄]` "change **from a single impedance arc to a double impedance arc**" — 10호(Larfaillou 재인용) · 11호(1차 DRT)에 이어. 단 종설은 이것을 "1차 RC 정확도 저하" 로만 읽는다 → [[drt-peak-count-nonidentifiability]] 층 1 이웃 절.
- ★ **Table 1 ("Summary of PHM techniques for solid-state batteries") 28 슬롯 전수 대조** `[재현]`: SSB 논문 13(순방향 물리 모델 10 + 전해질 재료 ML 3) · LIB PHM 4 · **납축전지 ECM [85] · 전방십자인대 재건 예후 [111] · 1976 kNN [108] · 1999 LS-SVM [113] · QSAR RF [109] · 정보학 종설을 "PF" 로 [87]** ⇒ **SSB 실측 열화 데이터로 SOH/RUL 을 추정한 항목 0/28**. 논문 자신의 결론 (1) `[인쇄]` "primarily used to estimate the **SOC** of SSBs" · (2) "very few studies … lack of accurate data" · §4 "**most PHM techniques are based on simulation results and not experimental**" 과 일치. ★ `[인쇄]` "very few instances where a battery can be completely exhausted or fully charged at the pack level"(재인용) = 8호 "no direct capacity labels" 의 **2022년 판**.
- **8호(Li 2026)와 대조**: 둘 다 종설·SOH 스칼라·모드 라벨 0. 다른 점 — `identifiab*` 0 ↔ 5, 표의 열(Categories·Technique ↔ Training boundary·Validation·Uncertainty), 압력 재인용(`0.4–1 MPa` 모델 최적 ↔ `<≈1 MPa` 산업 요구 — **다른 원전, 같은 자릿수**). **공통 원전 0건**이라 "같은 원전을 두 리뷰가 다르게 적었는가"(8호에서 Su 2024 로 실측한 것)는 이 쌍에서 **수행 불가**.
- 어긋남 **21건**, 주장 약화 ★ 8: **D4** 중복 [60] · **D5** Deng [79] 가 §3.1.1 Padé 축소 / §3.3.3 eSNAP 퍼텐셜 이중 용도(제목은 후자) · **D6** "Song et al. [29]" LS-SVM+UPF "SSBs and LIBs" — [29] 는 Tian **종설**(유일한 SSB 하이브리드 사례 주장의 출처 없음) · **D7 §3.3.1 "Anode Materials" 내용 = 양극 / §3.3.2 "Cathode Materials" 내용 = 음극 (제목 뒤바뀜)** · **D8 Table 1** · **D9** ECM 식별법 인용 [86–89] 넷 다 무관(Bayesian opt. arXiv · 정보학 종설 · NCA DFT · 클러스터 전개) · **D13 모델 차수 두 명제 충돌** · **D20 `[도표]` Fig. 5 `SOH = {FOI₁…FOIₙ}` 벡터 ↔ 식 (6) 스칼라, 언급 없음**. 편집급: D1 "LiCoO₂ **or LTO**"(LTO 는 음극) · D2 §2 "Li metal anode" ↔ 식 (2) 흑연 + 식 (3) 오타 `LiCoC₂`/`Li₁×x` · D3 Fig. 2 캡션 "blue line … blue line"(그림엔 자홍 실선 + 청록 점선) · D11 ref [21](LIB 이차입자 균열) 세 용도 · D12 Li plating → Fabre SSB 모델 [42], 접촉손실 기구 → Remmlinger R 추정 [43] · D15 "equivalent **circle** life" · D16 SE 유형에 "LiTFSI"(염), 음극에 "graphene [69]"(= Safari LFP) · D18 외부 인자 본문 4 ↔ Fig. 7 5(SOC) · D21 초록의 "ML … anode, cathode, electrolyte materials" = §3.3 은 PHM 이 아니라 **재료 설계**(NN potential·형성에너지). 공백 10건(G1~G10; G7 = 저자 자신의 DDP 에 데이터·지표 0, 인용이 **전방십자인대 예후 + 학회 요약문 자기인용**).
- 컴파일: **새 개념 페이지 없음**(1차 내용 0 · 명제 전부 기존 축 — SCHEMA Page Thresholds). [[assb-contact-loss-vs-lampe]] (채움표 12행 + Evidence **아홉 번째** 절 "반례도 근거도 아닌 계보의 출발점" + 새 제약 4개 + Status Log + "주장하지 않는 것" 1항) · [[assb-lampe-contact-product-degeneracy]] (`A_eff` 계보 절, `single-source` 유지) · [[drt-peak-count-nonidentifiability]] (층 1 이웃) · [[fitting-degeneracy]] (Q4 계보 2022년 표본). ⚠ [[composite-cathode-percolation-utilization]] 은 건드리지 않았다 (분할 대기). `index.md` 변경 없음(새 컴파일 페이지 0).
- ⚠ **규율 강화**: 인용 위생이 21건 무너진 종설이라 **재인용 수치를 방향으로도 옮기지 않는다** — "이 지면에 이렇게 적혀 있다" 까지만.
- 후속 후보 (원전 우선; 큐 12~37 과 겹침 검색 0건 — Tian·Shao·Kim·Fathiannasab·Schmidt·Pastor·Hu 2020·Cho 로 `ASSB_TRANSFER_NOTE.md` 검색): ★★★ 1 **Tian & Qi, *J. Electrochem. Soc.* 2017, 164, E3512** ("Simulation of the effect of contact area loss in ASSB" — `A_eff` 원전 후보) · ★★★ 2 **Shao et al., *Energy* 2022, 239, 121929** (접촉 면적 손실 **+ 압력** — Q1·Q6 동시, `0.4–1 MPa` 진짜 출처) · ★★ 3 **Kim, Lin, Abbasalinejad, Kim, Chung, *Electrochim. Acta* 2019, 317, 663** ("On state estimation of all solid-state batteries" — Table 1 유일의 SSB 상태추정; ⚠ 10호 후속 1순위 Ingdal 2019 와 **같은 권 317**) · ★★ 4 **Schmidt, Bitzer, Imre, Guzzella, *JPS* 2010, 195, 7634** (용량 손실 ↔ 율 특성 저하의 모델 기반 구분 — 3항 분해 `θ_AM·Q_material ↔ η(i)` 의 액체셀 원형; `assb` 태그 아님) · ★★ 5 **Fathiannasab, Zhu, Chen, *JPS* 2021, 483, 229028** (싱크로트론 TXM 토모 → SSB 응력 모델; 2호·3호의 실측 형태 입력 판) · ★ 6 **Pastor-Fernández 2017 *JPS* 360, 301** (EIS vs IC-DV 모드 정량 — 이 종설이 "CL" 각주로만 쓴 원전, 액체셀) · ★ 7 **Hu, Xu, Lin, Pecht, *Joule* 2020, 4, 310** (Fig. 6 + "LAM ⊃ contact loss" 정의의 원전) · ★ 8 **Cho 2012 *Comput. Chem. Eng.* 41, 1** ("원호 1→2" 재인용의 원전).
- lint: **0 errors · 0 warnings** (43 pages, 40 raw).

## [2026-09-22] ingest | 세미나 — BML 주간 보고 (김시원, 2026-09-21, 8쪽): Si-graphite ‖ NCM811 ICA 모델링 — LAM_Si 도입 · Si OCP 방향 의존 · Euclidean loss · 0.5C PVS
- 09-02 덱(`raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md`)의 **직접 후속** — 그 덱 p.15 discussion point 3개(① fitting quality ② LAM_NE → Si/Gr ③ dQ/dV → PVS)가 **전부 착수**된 첫 보고. raw: `raw/papers/2026-09-21-siwon-kim-si-gr-ica-lam-si-gitt-ocp.md` (sha256 봉인, `pdf_sha256 717952aecc84ea34…` 실측 일치). 크로핑 `--slides` **8장, 전부 직접 봄**. 셀 화학·모델명·셀 수가 덱에 **미인쇄**(09-02 MJ1 연속선상으로 추정, `[해석]`).
- ★★ **p.4 — Si OCP 가 방향 의존이다**: `[인쇄]` "충/방전 GITT-OCV 의 최적 fit OCP 가 다름" — `[도표-인쇄]` 방전 데이터에 **Li OCP γ_Si 25.7 % / RMSE 15.23 mV** ↔ **Lu OCP 30.5 % / 20.36 mV ("Lithiation fitting 시 최적")**. 라벨이 OCP 출처에 **≈5 %p 민감**. p.3 문헌 Si OCP 8종(Bagetto·Friedrich·Jiang·Kunz·Li·Lu·Sethuraman·Wetjen, 성만) **전부 닫힌 이력 루프**(가지 간격 ≈0.1–0.3 V). → [[halfcell-ocp-shape-invariance]] **세 번째 파괴 방식**(액체셀 Si, 한 사이클 안, 준평형) — Spencer-Jolly 7호의 액체셀 판. 덱은 full-cell 적합에 어느 방향 OCP 를 넣었는지 적지 않는다.
- ★★ **p.6 — LAM_Si 첫 궤적이 음수를 포함한다**: `[도표]` knee 이후 셀 1개, `LAM_Si` **0 → −20.5 → −23 → −9 → +50 %**, `γ_Si` 20.5 → 25.3 → 11.4 %, `LAM_Gr` +6 → −0.5 %, `LAM_PE` 한 점 −0.2 %, `LLI` → 26.8 %. 덱 문장은 "정량화 결과가 LAM_Si 반영", 음수 무언급, 오차 막대 0. `[해석]` Schmitt 2022 처방 ③(γ_Si 자유)의 미검사 대가 `(γ_Si, α_NE)` 축퇴의 야생 징후로 읽힘 — 가설. **이 5곡선이 차주 랜덤 포레스트의 정답 축**(p.1).
- ★ **p.7 — Euclidean distance loss 식 인쇄**: `L_euc = (1/N) Σ min_j sqrt((Q_i−Q̂_j)² + ((V_i−V̂_j)/s)²)` + dV/dQ 판 + `θ* = argmin[w_pOCV L_pOCV + w_dV/dQ L_dV/dQ]`. `s`·`w`·ub/lb 값 없음. ⚠ **상위 메모의 "비교 그림 6장" 은 없다 — 모식도 1장 + 식 5개**, MSE 대비 수치 0. `[해석]` 가로 어긋남을 싸게 하는 손실 = 특징점 가로 위치(모드 신호)에 무뎌짐 → 곡선 일치 ↑ 와 근최적 폭 ↑ 가 같은 변경의 두 얼굴 — 우리 격자에서 paired 검증 후보 ([[22p-physics-or-degeneracy]] Status Log).
- ★ **p.8 — 0.5C dQ/dV PVS "열화모드와 선형성 X"**: 상관 그림 **없음**, dQ/dV 겹침(셀 #8, rpt 0–700)만. `[도표]` rpt 0 만 형상이 다르고(3.63 V 봉우리 4.8 → 3.3 Ah/V, 3.9 V 둔덕 소멸) 이후 14곡선 촘촘; **4.23 V 컷오프 스파이크에 peak 마커 세로 줄** (검출기 오검출). **판정: [[pvs-sev-lli-lampe-separability]] Evidence For/Against 어느 쪽도 아님 → Gap** (feature 비선형 vs 라벨 잡음 분리 불가 — 라벨 불확실성이 실무에서 처음 필요해진 자리). **Gap 1건 닫힘**: PVS 는 두 덱 모두 **Ah 축**(`Ah/V`)에서 계산 → Lin 따름정리 엄밀형 미적용, 총용량 정보(= 입력 SOH)가 섞인다. SEV 는 덱에 0회.
- **사용자 메모 ↔ 덱 어긋남**: 메모의 "**fmincon 외 PSO/GA 적용 예정**" 은 **덱에 없음(구술 전용)** — optimizer 가 fmincon 이라는 사실도 여기서만; 메모의 "SOH 상관" 도 덱에 없음; 반대로 덱의 **LAM_Si 도입 · Euclidean loss · Si OCP 8종 · 딥러닝** 이 메모에 없음. "Fitting 성능 개선 확인" 은 덱에 근거 그림 없음.
- 컴파일 (새 페이지 0 — 전부 기존 축): [[pvs-sev-lli-lampe-separability]] (Gap 2 추가 · Gap 1 닫힘 · Status Log) · [[pvs-sev-degradation-mode-features]] (0.5C 절 신설) · [[halfcell-ocp-shape-invariance]] (세 번째 파괴 방식 + 처방 ③ 야생 실행) · [[22p-physics-or-degeneracy]] (Status Log — `(γ_Si, α_NE)` 축퇴 지도 실행 동기 · `L_euc` 대조군 · 유효범위 "단일 방향 OCP 가정 하"). `index.md` 변경 없음.
- 공백 14건 (raw digest 머리): 셀 식별 · fmincon 설정 · `s`/`w` · Euclidean vs MSE 비교 수치 · LAM_Si 정의식 · p.6 x축 단위 · 음의 LAM_Si 무언급 · 0.5C PVS 정의/상관 그림 · Si OCP 8종 서지 · GITT 프로토콜 · **γ_Si 불일치(half-cell 25.7–30.5 ↔ full-cell 20.5 ↔ Schmitt MJ1 9.52 %)** · 딥러닝 정체 · 이력 처리 방침 · 라벨 불확실성 0.
- 되돌려 줄 것: ① `(γ_Si, α_NE)` 근최적 폭(우리 격자, 값 싸다) ② 방향 의존 OCP 아래에서 우리 하한 진술의 유효범위 ③ `L_euc` 의 곡선 일치 vs 폭 paired 비교. 후속 후보: Si OCP 8종 서지 확정(특히 Li = Li & Dahn 2007?, Lu) · Si 이력의 열역학/동역학 귀속 문헌.

## [2026-09-22] ingest | `assb` 13호 — Zheng, Xie, Zhang, Yang, Zhou, Zhu 2026, All-solid-state batteries for the grid: A realistic appraisal of challenges and opportunities (*Energy* 345, 140229) ⚠ Perspective
- 큐 **12번**. raw: `raw/papers/zheng2026_assb-grid-realistic-appraisal.md` (본문 **10쪽** = 텍스트 8 + 참고문헌 56편 2쪽, **SI 없음** — 업로드 큐에 `12._Sup_*` 부재 + 본문 `supplement*`·`Supporting`·`Appendix` **0회**; sha256 봉인, PDF `496f3b4580a81b9b…` 실측 일치, doi `10.1016/j.energy.2026.140229`, Elsevier 유보 저작권). 큐 문서의 "Energy 2026" 은 지면과 일치(권 345). 소속 Nanjing Tech + **Huadian 전력연구원 + Shuangdeng 전지 제조사**(제1저자 겸직) — 수요 측 저자. 접수 2025-12-07 → 승인 **2026-01-27 (51일)**. 자기 인용 **6/56**(권장 복합전해질의 유일한 수치 예 0.826 mS cm⁻¹ = 자기 논문 [29]).
- ⚠ **Perspective — 1차 측정 0. `[인쇄]` "Data availability: No data was used".** 그림 5장 **전부 모식도/레이더**(데이터 그림 0). `[인쇄]` 는 12호·10호·8호 규율대로 "이 지면에 이렇게 적혀 있다". 수치 세 층위(저자 1차 추정 / 재인용 / 투영)를 digest 에서 구분. 크로핑 **7장(Fig. 1–5 + Table 1–2), 누락 0. 실제로 열어 본 것: Fig. 1·2·3·4·5 전부**(표 2장은 텍스트 전사). 합자: NFKC 정규화 후 `ﬁ`/`ﬂ` 잔존 0 → 집계 신뢰 (`identifiab*` 0 · `identification` 0 · `contact loss` 1 · `MPa` 본문 2 — ⚠ 첫 집계에서 대소문자 무시로 `LAM`→"fl**am**mable"·`MPa`→"co**mpa**tible" 이 잡혔다, 약어는 대소문자 구분 재집계).
- **큐 등록 축 Q3·Q4 → 실제 접점 Q6·Q8 로 판정.** Q1~Q8: **새 칸 0 (13편 누적 ≈8.5/8 유지, Q4 0/13).** Q1 없다(`contact loss` 1, 정량 0 — 단 대리량으로 **"interfacial contact pressure 감쇠"** 지목) · Q2 없다(처방 셋: 압력 센서·EIS proxy·음향) · Q3 해당 없음(투영 + LCOS 입력 미공개) **+ 라벨 정의 인쇄** · **Q4 0/13** · Q5 0 · **Q6 ★★ 본체**(`<5 MPa` 1차 주장 ×2 + `[도표]` Fig. 2 클래스 창 5 값 + 피로형 상한 + 능동 응력 관리 정책) · Q7 0 · **Q8 ★ 부분**(LFP 권장 + `[인쇄]` "20–80 % SOC … impossible to obtain a full OCV curve" + 응력 이력 + Si 음극 권장).
- ★★★ **판정 한 줄**: **13호는 채움표에 칸이 아니라 "운전 조건" 과 "분류 체계 셋째" 를 더한다.** ① `[인쇄]` SOH 가 갈라야 할 것 = "**true active material loss**" ↔ "**reduction in usable capacity caused by rising impedance or increasing overpotentials**" — **2항**, 같은 절이 지배 실패 모드 1번으로 꼽은 **접촉 손실의 소속 미배정**(`θ_AM` 이 요구서에서 사라짐). 12호 `LAM ⊃ 접촉 손실`(흡수) · 13호 누락 · 우리 3항 — **분류 셋이 전부 다르다.** ② **운전 창이 OCV 채널을 설계상 닫는다**: 20–80 % SOC + LFP 평탄 + "voltage hysteresis arising from mechanical stresses"(인용 0) ⇒ 닻의 답에 **"완전 OCV 곡선 조건"** 을 붙이고 부분 창 폭을 별도 산출(새 제약 1). ③ **Q4 성질 — 이름 없이 역문제를 처방**: `[인쇄]` "inversely estimate the current state of interfacial contact **and** material properties" — 9호 곱 축퇴 `A_eff·ε_p/R_s` 가 정확히 그 사이에 있는데 모른다. 8호(`identifiab*` 5)와 **같은 해** ⇒ "2026년 문헌은 안다" 는 8호 한 편의 일.
- ★★ **Q6 — 요구치 세 번째 독립 인쇄 + 위 벽의 두 번째 형태**: 8호 `<≈1`(Xu 2024) · 12호 `0.4–1`(Tian/Shao) · 13호 `<5`(Si 근거 [35]/[45], "5" 출처 미명시 G3) — **원전 셋 다 다르고 자릿수 같음**, 실험실 창 2–490 MPa 은 셋 다의 위. `[인쇄]` 고정 고압 → "creep and stress relaxation … fatigue-driven micro-crack initiation"(**피로**, ~년) = 5호 단락 상한(~h)과 다른 축 → 한 숫자로 안 합침(새 제약 2). `[인쇄]` 능동 응력 관리 정책(율↑→P↑, 휴지/노화→P↓) = 8호 "coupled state/control variable" + 정책 — ⚠ 5호의 `θ(P)` 이력과 정면 충돌(제어가 상태를 매번 다른 가지에 올린다). 인과 `압력 감쇠 → 임피던스 ↑` 명시. **압력→용량 0 (12/12 데이터 편 기준 유지)**.
- **8호·10호·12호와 대조**: 12호 ↔ 13호 **공통 원전 0건**(Tian·Shao·Hu·Fathiannasab ↔ Schmaltz·Albertus·Li Qianya·Gu·Pang 2021). 10호 ↔ 13호 = **같은 그룹(Offer/Marinescu)의 다른 논문**(Pang 2019 *PCCP* ↔ Pang 2021 *Mater. Today* [51]) — 공통 원전 아님. 8호 ↔ 13호 압력 요구치 원전 다름(Xu 2024 ↔ [23]/[35]/[45]). ⇒ "같은 원전을 두 리뷰가 다르게 적었는가" 는 이 쌍에서도 **수행 불가**; 실측은 **≈1–5 MPa 의 독립 수렴**.
- 어긋남 **12건**: **D2** "~45–55 % LCOS reduction" ↔ 표 끝점 짝 `[재현]` 45.5/50 % · **D3 `[도표]` Fig. 1 그리드 삼각에 숫자 0**, EV 원 ">1500 cycles · >99.98 % CE" — `[재현]` 그 CE 로 10000 사이클이면 잔존 ≈13.5 % (그리드 CE 문턱 미제시) · **D4 본문 `<5 MPa` ↔ `[도표]` Fig. 2 권장 클래스(Halides 2–10 · Composites 1–10) 상단 = 문턱 2배** · **D5 `[도표]` Fig. 3 SSB BMS 입력에 온도 없음 ↔ §4 "thermal management remains a critical function … 30–50 °C"** · D6 `j ≈ 5 mA cm⁻²` = 0.5P ⇒ `[재현]` 로딩 ≈10 mAh cm⁻² 함의, 미기재 · D7 Table 2 "Dominant Degradation Modes" = 액체셀 어휘(Li plating·electrolyte decomposition), §4 의 접촉 손실·균열 부재 · D8 Fig. 2 캡션이 **수명 축을 제외**(논지는 lifetime-first) · D9 음향 진단 인용 [41] = 저온 시험 논문 · D10 "dominant failure modes [38]" = 종설 인용 종설 · D11 수명비 "2–3×" ↔ `[재현]` 1.67–3.75× · **D12 ASSB 10000–15000 cycles 무인용** (LCOS 최대 구동 입력). 공백 12건(G1 LCOS 입력 `d`·`P_charge`·`C_deg` 미공개 → `$0.08–0.12/kWh` 재현 불가 · G3 · G5 역추정 모델/관측/유일성 0 · G6 응력 이력 인용·크기 0 · G7 로딩 · G10 **Si 음극 권장하면서 Si OCP 이력 논의 0** · G12 `[재현]` 20 y × 2 cycle/day = **14,600 cycles** — ASSB 목표 10000–15000 의 상단만 넘는다, 논문 무언급).
- 컴파일: **새 개념 페이지 없음**(1차 내용 0 · 명제 전부 기존 축 — SCHEMA Page Thresholds). [[assb-contact-loss-vs-lampe]] (채움표 13행 + Evidence **열 번째** 절 "운전 조건이 OCV 채널을 설계상 닫는다" + 새 제약 5개 + Status Log + "주장하지 않는 것" 1항) · [[assb-stack-pressure-operating-window]] (요구치 계보 표 + 피로형 위 벽 + 제어변수·정책 ↔ 이력 충돌) · [[assb-apparent-capacity-decomposition]] (수요 측 2항 요구서에서 `θ_AM` 이 빠진 자리 + 그리드 창에서 `Q_material` 이 가장 안 보이는 항) · [[fitting-degeneracy]] (Q4 계보 2026년 두 번째 표본). `index.md` 변경 없음(새 컴파일 페이지 0).
- ⚠ **규율**: 13호의 수치를 근거로 옮기지 않는다 — Table 1 ASSB 열은 투영(무인용 5), LCOS 입력 미공개, `<5 MPa` 출처 미명시, Fig. 2 다섯 창은 `[도표]`·산정 규칙 0. "LFP + Si 가 그리드 ASSB" 는 수요 측 **권장**(자기 논문 근거)이지 사실이 아니다.
- 후속 후보 (원전 우선; 큐 13~37 겹침 검색 **0건** — Li Qianya·Zhang·Li Menglin·Oh·Gu·Pang·Kohtz·Schmidt/Staffell 로 `ASSB_TRANSFER_NOTE.md` 검색): ★★★ 1 **Li Qianya et al., *Nat. Energy* 2025, 10, 1064** ("The critical importance of stack pressure in batteries" [23] — Q6 요구 창의 정본 후보, 8호 Xu 2024·12호 Tian/Shao 와 삼각 대조) · ★★★ 2 **Zhang et al., *Nat. Commun.* 2025, 16, 1013** (무외압 Si ASSB [45] — 압력 0 에서의 접촉 손실 시계열이 있는지, Q1·Q6) · ★★ 3 **Li Menglin et al., *AFM* 2025, 35, 2415696** (압력 → Si 파괴 크기 문턱 [35] — `<5 MPa` 근거 후보) · ★★ 4 **Oh Jihoon et al., *AEM* 2025, 15, 2404817** (저 N/P·저압 운전 실셀 [34]) · ★★ 5 **Gu, Liang, Shi, Yang, *AEM* 2023, 13, 2203153** (황화물 ASSB 응력 측정 종설 [38] — 9호 힘 시계열 측정법 계보 + "지배 실패 모드" 정의 원전) · ★ 6 **Pang et al., *Mater. Today* 2021, 49, 145** ([51] — 10호 Pang 2019 의 자매, multi-physics 결합에서 접촉 손실 항 형태) · ★ 7 **Kohtz, Xu, Zheng, Wang, *MSSP* 2022, 172, 109002** ([40] — 13호 SOH 이분법 문장의 자기 공저 원전, 부분 충전 구간 라벨 정의) · ★ 8 **Schmidt, Melchior, Hawkes, Staffell, *Joule* 2019, 3, 81** ([18] — LCOS 식 원전, 열화율 `d` 취급).
- lint: **0 errors · 0 warnings** (43 pages, 42 raw).

## [2026-09-22] ingest | `assb` 14호 — Oh, Kim, Kim, An, Kwon, Choi 2025, Maxwell Protocol for Non-Destructive Health Diagnosis of All-Solid-State Batteries (*Angew. Chem. Int. Ed.* 64, e202514910) Hot Paper · 실험 + 진짜 SI
- 큐 **13번** — "**OCV 경쟁 접근**" 으로 등록된 편. raw: `raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md` (본문 **9쪽** = 텍스트 8 + 참고문헌 74편, **SI .docx** = Experimental 3절 + Note S1 + Fig. S1–S16, **표 0**; sha256 봉인, PDF `fa35a5cdd5d3fcec…` · SI `ce0b9a35c96ef99c…` 실측 일치, doi `10.1002/anie.202514910`, **CC BY-NC-ND**). ⚠ 지면은 *Angew. Chem.* 독일어판 조판("Forschungsartikel")이지만 **본문 영어**. 서울대 + **HMG-SNU JBRC(현대차)**, 교신 Choi Jang Wook. 접수→승인 **35일**. 자기 인용 **21/74**. SI 는 `zipfile` 로 `document.xml` + `media/image3–18`(= S1–S16) 추출, TIFF 는 투명 배경을 흰색으로 합성해 봤다.
- **실험 논문** (엔트로피메트리 3셀 · volumetry 3+1셀 · XRM 4 · SEM). 크로핑 본문 **6장 전부 봄**, SI 16장 중 **11장 봄**(S1·S2·S3·S4·S7·S8·S9·S12·S13·S14·S16) — 안 본 것 **S5·S6·S10·S11·S15**(SEM-EDS·XRM 원영상). 합자 잔존 0; ⚠ 대소문자 무시 집계의 `SOH` 5회는 전부 저자 "**Soh**n"(13호 "fl**am**mable" 교훈 재현) — 약어 재집계(`LAM`·`LLI`·`SOH` 0).
- ★★★ **판정 한 줄**: **"OCV 경쟁" 이 아니라 "OCV 의 관측 추가"** — `E(x)` 를 적합하지 않고 같은 상태함수 `E(x,T,P)` 의 두 편미분 `−F(∂E/∂T)_P = ΔS`(엔트로피메트리 → "탈리튬화 비균질") · `F(∂E/∂P)_T = ΔV`(volumetry → "void") 를 잰다. "Maxwell" = `dG = VdP − SdT` 의 혼합 2계 편미분 대칭성을 `x` 축에 확장(Yazami 계보 표준 유도, 새 물리 아님). 분리 주장은 `[인쇄]` "distinguish between **mechanical and chemical** degradation" — **`LAM_PE` ↔ 접촉 손실은 물음 자체가 없고**, ΔS 는 `[인쇄]` "contact loss **as well as** … interfacial resistance" 를 **한 신호로** 받는다고 스스로 정의. 교차 실험 0((ΔS, ¬ΔV) 칸 없음).
- Q1~Q8: **14편 누적 ≈8.5/8 유지 — 새 칸 0, 층 셋.** Q1 ★ 비파괴 대리량 `F(dE/dP)` `[인쇄]` 42.7 → 34.7 µJ mol⁻¹ Pa⁻¹(−18 %, 3셀 18–20 %) + XRM 공극률 4.5 → 9.8 %(4호 void 9.50 % 와 같은 자릿수) · Q2 ★★ 셋(가르는 쌍이 다름) · Q3 measured-morphological + measured-thermodynamic, **등급 문턱값 0 · 오차 0** · **Q4 0/14 — 일곱 번째 성질: 역문제가 없어 조건수가 정의될 자리가 없고 귀속 유일성은 안 쟀다** · Q5 해당 없음(Li 금속)이나 음극 상수항(`V_m(Li)` 13 cm³ mol⁻¹ = `[재현]` 실측 2.2 mV 의 30 %) 미검토 · **Q6 ★★★ 압력이 관측 변수 — 계보 최초 `E(P)`** `[인쇄]` 2.2 mV/5 MPa ↔ 2.3 mV/10 MPa(신품끼리) = `[재현]` **0.44 ↔ 0.23 mV/MPa, 2배 비선형**(논문 무언급) + 압력→용량 2점(86.0/84.0 %, **역상관**) · Q7 해당 없음 · **Q8 ★★★ OCV 축 위 열역학 도함수** ≈28점 × 3셀 × 전·후 + dQ/dV 봉우리 3.60/3.73(H1→M)/4.00/4.18 V(SOC 축 없음). 접촉 손실 = LAM 안/밖: **미언급**.
- ★★★ **우리 축에 준 실측**: `[인쇄]` **void 2배 셀(86.0 %)과 +0.9 %p 셀(84.0 %)의 용량이 같다** — 접촉 손실 → 용량 사상이 **문턱형**(4호 60 %p 의 반대쪽 끝), 문턱 아래에서 OCV 적합은 `LAM_PE ≈ 0` 을 정확히 보고하며 void 성장을 **놓친다**(오독이 아니라 무감). `[해석]` 우리 쌍에 대한 새 감도 행 부호: 균일 `LAM_PE`·완전 고립 접촉 손실은 둘 다 아핀 → **ΔS 행 = 0**; void → **`dE/dP` 행 ≠ 0** ⇒ 분리 후보는 **volumetry**, 엔트로피메트리 아님(논문은 반대). 실측 0.
- 어긋남 **15건**: **D1** Fig. 3a 기준선 이탈 ≈2–4 mV ↔ ΔS ≈ +3 이 함의하는 `[재현]` 0.47 mV · **D2 Fig. 3c "after 100 cycles" 끝점(+1 @4.25 V) 이 Fig. S2 세 셀(−2.3/−4.5/−5) 어느 것도 아님** · D3 SI "OCV 4.5 V" ↔ 그림 4.25 V · **D4 신품 volumetry 42.5(ΔP 5) ↔ 22.2(ΔP 10) — 압력 구간 2배, Fig. 5e/f 눈금 달라 가려짐** · D5 본문 42.7 ↔ `[재현]` 42.45 · **D6 Fig. 6 "Recycle (ΔS signal)" ↔ 본문 "heterogeneous along with significant void"** · **D7 전·후 volumetry OCV 3.532 ↔ 3.703 V(171 mV) — 캡션은 둘 다 "after discharge at 2.5 V"** · D8 SI "TPU-080 … Figure S7" ↔ S8 사진 TPU-040N · D9 "real time" ↔ `[재현]` 1 프로파일 ≈140 h · D10 "quantitatively" ↔ 사상 2점 · **D11 "distinguish mechanical and chemical" ↔ 화학 단독 대조군 0** · **D12 "similar" 로 덮인 역상관** · D13 음극 "constant" ↔ 식 (6)(10) 상수항 ≠ 0 · D14 신품 공극률 4.5 ↔ 4.4(다른 셀) · D15 "without perturbing" ↔ ≈140 h 정지. 공백 14건(G1 등급 문턱 0 · G3 `dE` 판독 규칙 0(S16 재가압 뒤 +0.4 mV 오프셋·+0.5 mV 표류 = 노화 신호 크기) · G7 SOC 축 0 · **G8 sum rule** — ΔS SOC 축 적분 ≈ −3.5 → +1.5 부호 반전은 비균질만으로 안 나온다 · G9 로딩 0 · G10 XRM 복셀 "0.7 pixels per unit"(sic) · G11 >300 MPa recondition 미수행·4호 미인용 · G12 (1,0) 칸 없음).
- 이웃: 5호 Doux = **ref [35]**(`Z(P)` ↔ 이 편 `E(P)`; Li 금속 20 MPa 단락 190 h ↔ 이 편 20 MPa `[재현]` ≈225 h 단락 보고 0, 설계 다름) · 4호 Shi **미인용**(같은 300 MPa 숫자) · 1호 Bielefeld 2019 대신 **Bielefeld 2022 *JES* = ref [69]**(pore 문턱 → 저항 급증) · 9호와 반대 형태(적합 없음) · 10·11호 EIS 를 `[인쇄]` "limited … underlying degradation mechanism" 으로 밀어냄 · **13호 후속 4순위 Oh *AEM* 2025 = 이 편 ref [10], 같은 저자·연구실 → 1순위 승격**.
- 컴파일: **새 개념 페이지 1** [[assb-maxwell-ocv-derivative-channels]] (`assb` 아홉째 — 관측 축이 새롭고 닻·CRB·압력·3항 페이지 넷에서 참조; `single-source`, `confidence: low`). [[assb-contact-loss-vs-lampe]] (채움표 14행 + Evidence **열한 번째** 절 + 새 제약 5개 + Status Log + "주장하지 않는 것" 1항) · [[assb-pressure-reapplication-separation-test]] (**소신호 판** — 적용 순서 ①율 ②ΔP ③P↑) · [[assb-stack-pressure-operating-window]] (계보 최초 `E(P)` + 압력→용량 2점 + 위 벽 세 번째 표본) · [[assb-apparent-capacity-decomposition]] (**`θ_AM` 은 void 의 함수가 아니라 퍼콜레이션의 함수** — 문턱형 사상의 양 끝) · [[constrained-crb-identifiability]] (관측 추가 행의 ASSB 표본 + 부호표) · [[fitting-degeneracy]] (Q4 계보 — 역문제 부재형) · [[halfcell-ocp-shape-invariance]] (ΔS(x) 두 번째 상태함수 검사 + sum rule). `index.md` **+1 (44 페이지)**.
- ⚠ **규율**: 42.7 µJ mol⁻¹ Pa⁻¹ 를 "ΔV" 상수로 옮기지 않는다(압력 구간 2배·SOC 171 mV 차); "void 는 용량에 안 보인다" 는 50 cy·2점·셀 각 1 의 것; volumetry 분리 후보는 우리 `[해석]` 이지 논문 주장 아님; Q4 는 여전히 0/14.
- 후속 후보 (원전 우선; 큐 14~37 겹침 **0건** — Bielefeld 는 2019 편만 큐에 있음): ★★★ 1 **Oh, Kwon, Choi, …, Choi, *AEM* 2025, 15, 2404817** (ref [10] — 저압 실셀, Q6; 13호 4순위 승격) · ★★★ 2 **Bielefeld, Weber, Rueß, Glavas, Janek, *JES* 2022, 169, 020539** (ref [69] — pore 문턱 → 저항 급증, 1호 `p_c` 의 실험판, Q1) · ★★ 3 **Kim, Kim, Kim, Chang, Choi, *PNAS* 2022, 119, e2211436119** (ref [56] — 이 연구실 엔트로피메트리 원전; SOC 축·sum rule·오차 처리) · ★★ 4 **Kim … Yazami, Choi, *EES* 2020, 13, 286** (ref [57] — `dE/dT` 정밀도·이완 기준선) · ★★ 5 **LePage et al., *JES* 2019, 166, A89** (ref [70] — "10 MPa Li creep" 근거) · ★ 6 **Lewis 2021 *Nat. Mater.* 20, 503 / Lu 2022 *Sci. Adv.* 8, eadd0510** (refs [73][74] — "void 가 초기 성능에 안 보인다" 원전) · ★ 7 **Lee, Han, Lewis, …, McDowell, *ACS Energy Lett.* 2021, 6, 3261** (ref [34] — 해체 시 압력 해제가 상태를 바꾼다, post-mortem 라벨 신뢰성).

## [2026-09-22] ingest | `assb` 15호 — Rahman & Lu 2024, SSB 의 RUL 을 위한 스마트 BMS 전략 (IISE 회의록 6쪽)
- raw: `raw/papers/rahman2024_sbms-rul-solid-state-batteries.md` (*Proc. IISE Annual Conference & Expo 2024*, Abstract ID 8085; 6쪽, **SI 없음**, PDF sha256 `0d99b00e…`, 본문 sha256 봉인). 크로핑: `raw/figures/rahman2024_sbms-rul-solid-state-batteries/` — ⚠ 캡션 크로퍼가 0개를 뽑아(`Figure 1-` 에 공백이 없어 정규식 불일치) `--slides` 로 페이지 전면 6장 + **본문 유일 그림 400 dpi 직접 크롭 1장**(`p2_figure1_ann_pipeline_400dpi.png`). **실제로 본 것: 그 1장**(400 dpi 전체 + 좌반부 500 dpi). 안 본 것: 텍스트 페이지 렌더 5장 — `get_images()`/`get_drawings()` 전수로 **그래픽 0**임을 기계 확인.
- ⚠⚠ **이 계보에서 심사 강도가 가장 낮은 표본**이다 (DOI·접수/게재일·심사 기록 없음). 그리고 **1차 측정 0 을 넘어 재인용 수치도 0**: `[재현]` 본문 2,331단어에서 인용 괄호·절 번호를 빼면 남는 숫자가 **2024 · 8085 · 19 · 2021 · 2026** 뿐이고 `capacity`·`experiment*`·`measur*`·`contact`·`pressure` 가 **전부 0회**. 본문 그림 1장(액체셀 종설 재수록) · 표 0 · 식 0.
- ★★ **최대 수확은 논문의 내용이 아니라 인용 관계 둘이다 — 이 위키 최초로 "우리가 이미 읽은 원전을 인용하는 편"이 들어왔다.**
  ① **ref [5] = `assb` 1호(Bielefeld 2019), 어긋난다** — 기하 모형 논문이 `[인쇄]` "load balancing, state-of-charge estimation, and overall battery health monitoring" 의 근거로 배치된다. 우리 1호 digest 는 그 논문에 `[인쇄]` "셀 실험 0, 사이클링·전압·용량 없다" · `voltage` 1회(참고문헌 제목) · 음극 없음을 전수 계수로 기록해 뒀다. 서지도 **연도 2018 오기**(원전 2019).
  ② **ref [21] = `assb` 12호(Kouhestani 2022), 어긋나지 않지만 껍데기만 간다** — FNN/RNN 교과서 정의 한 문장만 가져가고, 12호의 자기 결론(`[재현]` **SSB 실측 열화 라벨 0/28** · `[인쇄]` "most PHM techniques are based on **simulation** … not experimental")은 옮기지 않는다. **12호(2022)가 감사로 적은 공백을 15호(2024)가 12호를 인용하면서 재생산한다.**
- ★ **분류 체계 세 번째 표본 = "어휘 미도입"** (12호 `LAM ⊃ 접촉 손실` 병합 · 13호 미배정 · **15호 미도입**, `contact` 0회). 셋 다 종설/전망/회의록이고, **1차 측정이 있는 편(4·5·6·7·9·11·14호)은 전부 접촉 축을 갖는다** → `[해석]` 접촉 구분은 **실험 층위에서 강제되고 종합 층위에서 소실된다** (표본 3, 잠정).
- **Q1~Q8 채움표 15호 행 추가 — 누적 ≈8.5/8 유지, 새 칸 0.** Q4 **여덟 번째 성질, 계보에서 가장 얕은 0**: 14호는 "역문제가 없어 조건수 자리가 없음", **15호는 추정기 자체가 없어 역문제를 말할 대상이 없다** (`identifiab*` 0회 · `accuracy` **7회** : 정확도 수치 **0** : 불확실성 표기 **0**). **여전히 0/15.**
- 참고문헌 33편 전수 분류(`[재현]`): **SSB 15 · 액체 LIB/EV 14 · 배터리가 아닌 것 2**([27] 람부탄 껍질 바이오차 Cu(II) 흡착 — **결론의 "as evidenced by" 근거** · [31] 멕시코 COVID-19 시계열). **두 집합이 교차하지 않아 "SSB 데이터에 ML 을 돌려 RUL 을 낸" 인용이 0편**이다.
- 어긋남 원장 **11건** (원전 대조로 확인 2 · 제목 기준 판단 3 · 나머지 내부 정합). 무거운 셋: **D1** 제목의 중심량 RUL 이 §2–§5 에 **0회**(초록·키워드·서론뿐, 정의·문턱·추정기·지표 전부 0) · **D2** 1호 오인용 · **D4** 결론 근거가 흡착 논문. ★ 억지로 늘리지 않으려 **인용 위생이 지켜진 자리 1건**도 함께 적었다([31] 은 `[인쇄]` "could be insightful" 로 유추임을 밝힌다).
- 컴파일: **새 개념 0** (6쪽 회의록에 새 축이 없다 — 기존 페이지에 절을 더하는 쪽을 택했다). 갱신 — 닻 [[assb-contact-loss-vs-lampe]] (채움표 15호 행 · Evidence 열두 번째 · 수집현황 항목 · Status Log · 주장하지 않는 것) · [[composite-cathode-percolation-utilization]] (★ "이 `θ` 가 야생에서 어떻게 인용되는가 — 첫 실측" 절 신설). **`index.md` 변동 없음** (새 컴파일 페이지 0).
- 후속 후보: 1순위 **Asheri et al., *Comput. Mater. Sci.* 226, 112186 (2023)**(ref [22] — 이 편이 아는 **유일한 SSB-ML** 이고 `[인쇄]` "interface damage" 를 다룬다; **12호의 28 슬롯에도 없던 좌표**) · 2순위 **Bielefeld et al., *ACS AMI* 12, 12821 (2020)**(ref [28] — 1호의 직계 속편, 1호 모집단 경고 "탄소·바인더 없는 2성분" 의 바인더 축) · 3순위 Zou et al., *JES* 73, 109069 (2023)(ref [16], Figure 1 의 원전; ⚠ 액체셀 — `assb` 태그 금지) · 4순위 Lipu et al., *JES* 55, 105752 (2022)(ref [33] — 이 편 참고문헌 중 제목에 RUL 이 있는 유일한 편인데 15호가 RUL 을 안 가져왔다; ⚠ 액체셀).

## [2026-09-22] ingest | `assb` 16호 — Ramanayagam, Miß, Leier, Duncker, Kirczek, Roling 2026, Elucidating the Influence of Stack Pressure on Anode and Cathode Impedance of ASSBs via Three-Electrode Measurements (*Batteries & Supercaps* 9, e70315) 실험 + 3전극 + SI

- raw: `raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md` (doi `10.1002/batt.70315`, **CC BY**, Univ. Marburg / mar.quest, DFG Ro1213/20-1; 본문 10쪽 + **SI 6쪽**, PDF sha256 `5ce9a4259bdf46d0…` / SI `4b6180aacf267b3e…`, 본문 sha256 봉인). 큐 **15번**, 이 큐 **3전극 실측 5편(15·16·18·19·20)의 첫 편**. ⚠ **연도는 2026** — 접수 2025-12-11 → 승인 2026-04-21, 지면 *Batteries & Supercaps* 2026, 9, e70315 (slug 를 `ramanayagam2026_` 로 잡은 근거).
- 크로핑: `raw/figures/ramanayagam2026_stack-pressure-three-electrode-assb-impedance/` **19장**(본문 그림 7 + SI 그림 8 + 표 4). **실제로 본 것 11개 파일** = 본문 Fig. 1–7 전부 + SI Fig. S1·S2·S3·S4 (+ Fig. 3 의 (b)(d) 확대 · S2 양 패널 확대 · S3 하단 확대). **안 본 것**: SI Fig. S5·S6(Bode 적합) · S7(XRD) · S8(Arrhenius), 표 크롭 4장(PDF 텍스트 사용).
- **셀**: NMC83|6|11(단결정 3–6 µm, LiNbO₃ 1 wt%) : Li₅.₃PS₄.₃ClBr₀.₇ = **70:30** ‖ SE 분리막 ‖ **In 박**(∅12 mm), A = 1.13 cm². **제작 389 MPa/3 min**(분리막 선압축 97 MPa/3 min), 측정 **97 또는 389 MPa**, 0.1 C, **2.7–3.7 V**, **SOC50 · 2 번째 사이클**. **셀 12 개**(두께 5 × 압력 2 × 2E + 3E 2) — **조건당 n = 1, 오차막대 0**.
- ★★★ **계보 최초 3 건**: ① **3전극 전극 분해**(리튬화 **Au/W μ-RE ∅25 µm**, 5 µA/30 min) + `[인쇄]` **2E = 3E 합(10 kHz 아래)** 자기 검증 ② **압력을 본체로 삼은 1차 측정**(`pressure` **49 회** — 13호 24 를 넘는 계보 최대) ③ **DRT 정규화 λ = 0.05 를 인쇄**([[drt-peak-count-nonidentifiability]] 체크리스트 **C1 최초 ✅**, C2–C5 전부 ❌).
- ⚠⚠ **열화가 없는 편이다**: `degrad*`·`aging`·`SOH`·`LAM`·`LLI`·`contact loss`·`percolat*`·`θ`·`void`·`hysteres*` **전수 0 회**. `capacity` **본문 1 회**(서론의 "energy storage capacity"). 그래서 닻에 주는 것은 **열화 라벨이 아니라 역문제의 구조**다.
- ★★★ **최대 수확 — 곱 축퇴의 실측 표본, 그리고 배정이 결론을 뒤집는다.** `[인쇄]` 식 (4)가 "**the area of the CAM particles in contact with the SE**" 라 이름 붙인 양을 **완전구 기하 면적** `a_V = 3ε_CAM/r_CAM`(접촉 분율 인자 **없음**)으로 계산 ⇒ `[해석]` 얇은 전극 극한 `R_semicircle = R_CT/(a_V d)` 가 보는 것은 **`j₀ · ε_CAM / r_CAM` 한 조합**(9호 `A_eff·ε_p/R_s` 와 **같은 자리**). 논문은 뒤 둘을 고정해 **전부 `j₀` 로 읽는다**(0.74 → 1.33 A m⁻², **1.80 배**). **그런데 같은 Table 2 의 `Q_DL` 이 0.18 → 0.54 (3.0 배)** — 이중층 용량은 **면적 비례**다. 면적으로 읽으면 `[재현]` **`θ` 3 배 + `j₀` 0.60 배(감소)** ⇒ **같은 데이터, 반대 결론.** 그리고 **논문의 문장은 둘째 배정**(`[인쇄]` "pressure improves the interfacial contacts … considerably"), **숫자는 첫째 배정**이다. ⚠ `β` 0.89↔0.81 로 두 `Q` 는 차원이 다르고, `[재현]` Brug 변환하면 비가 **3.0 → ≈5.6 으로 커진다**(방향 유지).
- ★★ **그래서 처방이 하나 생겼다 — `R_CT·C_dl` 채널**: `R_CT^meas·C^meas` 에서 **접촉 분율이 소거**되고(고유 시상수), `C^meas` **단독은 면적에 비례** ⇒ **둘을 같이 보고하면 `θ` 와 `j₀` 가 갈린다**. **16호는 두 값을 다 인쇄해 놓고 조합을 만들지 않는다.** `[재현]` 만들어 보면 `R_CT·Q` 가 두 압력에서 **1.7 배**(유효용량 3.1 배) 달라 **순수 면적 효과만으로도 설명되지 않는다** — 채널에 정보가 있다. ⚠ 우리도 아직 안 쟀다(설계).
- ★★ **Q5 가 네 겹으로 채워졌다**: ① 기준극이 **Li–In 이 아니라** 리튬화 Au/W ② **안정성을 인용으로 가정** (`stable` 3 회 중 **2 가 남의 논문** — Zhang LTO-RE 1.57 V · Hertle μ-RE 0 V; 자기 셀 검증 **0**) ③ `[도표]` **Fig. S1 리튬화 곡선에 평탄부가 없다**(2.5 µAh 에 **560 mV 표류**) ④ ★★★ `[도표]` **Fig. S3 의 In–Li 평탄 전위가 두 셀에서 0.58 ↔ 0.47 V, ≈0.11 V 어긋난 채** 같은 "vs Li/Li⁺" 축에 그려진다(둘 다 2상역 `x_Li` 0.18/0.14, `[재현]` 과전압 ≈5 mV 로 설명 불가, **논문 무언급**). `[해석]` **밀린 양의 셀 간 재현성이 0.1 V 자릿수면 그것은 `LLI` 로 오독될 크기다.**
- ★★★ **평탄 OCP 가 숨기는 양이 처음으로 숫자가 됐다**: `[재현]` `x_Li` 0.05–0.28 은 **In+InLi 2상 공존역 안**(우리가 SI 의 방전용량으로 정의를 역산해 확인 — 26 µm 셀 0.057 ≈ 인쇄 0.06, 207 µm 셀 0.28 ✓)이고 음극 전위는 **완전 평탄**인데, **바로 그 구간에서** `[도표]` 음극 DRT 봉우리가 **18.6 → 1.2 (≈15 배, 97 MPa)** 움직인다(389 MPa 에서는 1.6 → 0.30, 5 배). ⇒ **"음극이 평탄하다" ≠ "음극이 조용하다".**
- **Q6**: 운전 **97 / 389 MPa** = **계보 운전 압력 최댓값**(5호 Li 금속 상한 75 MPa 의 **5.2 배**, ⚠ In 음극이라 화학이 다르다) · ★ **제작 = 운전인 첫 표본**(6호가 쪼갠 두 축을 붙인다) · 압력 → 임피던스 1차(완전지 반원합 `[인쇄]` **23→11**(389) / **85→23 Ωcm²**(97), 3E 양극 **10↔20**, 음극 **4↔9 Ωcm²** — `[재현]` 양극 2.0 배 ↔ 음극 2.25 배로 **거의 같은 배율**) · 압력 → 공극률 `[인쇄]` **11.2 ↔ 12.9 %**(4 배 가압에 1.7 %p) · ★★ 압력 → 용량이 **SI 그림에만** `[도표]` 1 사이클 방전 **+9 … +59 %**(6호 1.5 %p · 14호 2 %p 에 이은 **세 번째, 폭이 압도적**). ⚠ **스윕 아님(2 점) · 이력 0 · 두 압력이 다른 셀 · 로드셀 시계열 0**.
- ★ **5호(Doux)의 `θ(P)` 이력 물음에는 답하지 않는다 — 그리고 그 물음이 왜 중요한지를 보여 준다**: 두 압력이 **다른 셀**이고 **둘 다 389 MPa 제작을 거친다** ⇒ `[해석]` **97 MPa 데이터는 필연적으로 하강 분기**인데 논문은 두 압력을 **대칭적 두 조건**처럼 비교한다.
- ★★ **DRT 가법성 파탄 — 새 경보**: `[도표]` Fig. 3(b)에서 ① **완전지의 τ≈10⁻⁴ 봉우리(γ≈1.55)가 양극·음극 어느 스펙트럼에도 없다**(본문은 "작은 시상수 2 개 = 양극", Fig. 4 는 집전체 귀속) ② **부분(양극 4.6)이 전체(완전지 3.1)보다 크다** — Nyquist 에서는 합이 맞는데 ③ 봉우리가 **τ 8·10⁻³ ↔ 4·10⁻³ 로 2 배 이동**. Fig. 3(d)에서는 **양극의 τ≈2 s 봉우리가 완전지에 없고** 논문은 **음극 사례만** 적는다. `[해석]` **전기화학적 분해(3전극) 뒤에도 수학적 분해(DRT)가 그것을 보존하지 않는다.**
- **어긋남 원장 12건**: **D1 본문 `[인쇄]` "In 박 두께는 모든 ASSB 에서 identical" ↔ SI 67–109 µm(질량 28.3–53.3 mg)** — 음극 결론의 논증 전제 · **D3 `[인쇄]` "R_CT 가 2 배 넘게 높다" ↔ `[재현]` 1.797** · D2 고주파 반원 "압력 무관" ↔ DRT 높이 3 배 · D4 Fig. S4 −3.5/−3.4 ↔ Table 1 −3.48 하나 · D5 양극 반원 압력비가 **세 곳에서 2.0 / 1.80 / 1.45** · D6·D7·D8 DRT 가법성 · D9 서론이 3E 의 명분으로 SOC 의존을 들고 **SOC 한 점만** 잰다 · D10 Table S2 캡션만 "98 MPa" · D12 Table 2 `D_CAM` 조판 파손("6.6 \*0−15").
- **공백 원장 16건**: G1 n=1·오차 0 · **G3 `D_CAM` 이 압력에 3.1 배 움직이는데 본문 언급 0**(재료 물성이다 → 적합 파라미터 교환의 신호) · G4 `Q_DL` 3 배 언급 0 · **G5 분리막 저항 비공개**(`[재현]` 2E ≈12 · 3E ≈35 Ωcm² — 보고된 모든 반원과 같은 자릿수 이상) · G9 `x_Li` 와 두께가 **완전 공선**(두께 고정 셀 0) · G10 **σ 를 97 MPa 에서만 재고 389 MPa 에 그대로 쓴다**(τ 8.8→7.7 이 σ(P) 일 수 있다) · G11 ε_SE+ε_CAM=1.000 인데 공극률 11–13 %(`[재현]` 전극 부피 기준 보정해도 비는 1.12 — **공극률 차이는 τ 차이를 설명 못 한다**) · G12 용량 미논의 · G13 207 µm 적합 실패 셀을 동시 적합에서 안 뺀다(공유 5 파라미터를 끌어당긴다) · G16 데이터 on request.
- **컴파일**: 닻 `questions/assb-contact-loss-vs-lampe.md` — **Q1~Q8 채움표 16호 행 + 누적 ≈8.5 → ≈9.5**(Q2 +0.5 전극 분해 관측 · Q5 +0.5 기준극 실측; **14편 만에 칸이 움직였다**), Evidence For **열세 번째** + Evidence Against 에 **`R_CT·C_dl` 채널** 신설, status log, "주장하지 않는 것" 5항. **Q4 아홉 번째 성질 = "밟고 지나갔다" — 여전히 0/16.**
  [[assb-lampe-contact-product-degeneracy]] — **§"두 번째 출처, 그리고 실측 판"** 신설 + 처방표 새 행 + **`evidenceScope: single-source → multi-source-primary`**(9호 P2D 식 + 16호 TLM/EIS 식; `confidence` 는 **medium 유지** — 두 편 다 축퇴를 **재지는** 않았다).
  [[assb-stack-pressure-operating-window]] — **§16호**(제작=운전 첫 표본 · 압력→임피던스 표 · 압력→용량 세 번째 표본 · 압력→공극률) + 압력 역할표에 16호 행.
  [[drt-peak-count-nonidentifiability]] — **C1 최초 ✅ 표** + **§"세 번째 경보: 부분의 합이 전체가 아니다"** + 폭 측정기가 붙는 두 번째 자리(`D(λ) ≡ ‖DRT(양극)+DRT(음극)−DRT(완전지)‖`).
  **새 개념 페이지는 만들지 않았다** — 위 세 페이지가 이미 이 편의 세 축을 담고 있고, 16호가 더한 것은 각 축의 **새 층**이지 새 대상이 아니다. `index.md` 변경 없음(새 컴파일 페이지 0).
- **후속 후보** (큐 대조 포함): 1순위 ★ **Miß, Ramanayagam, Roling, *ACS AMI* 14 (2022) 38246**(ref [30] — 이 편 **TLM 방법의 원본**, `r_CAM`·초기값·비교 `j₀` 의 출처) · 2순위 **König, Ramanayagam, Kraus, Roling, *Batteries & Supercaps* 7 (2024) e202300578**(ref [31] — 음극 heterogeneous interphase 모형의 원본) · 3순위 **Hertle et al., *JES* 170 (2023) 40519**(ref [24] — μ-RE 원본, "0 V vs Li⁺/Li 안정" 의 **유일한 근거**; Q5 의 G6 이 여기서 닫힌다) · 4순위 ★ **Fukunishi et al., *J. Power Sources* 564 (2023) 232864**(ref [39] — **큐 17번과 같은 논문**, 이 편의 유일한 외부 실측 대조군이고 **열화를 다룬다**) · 5순위 Roling et al., chemRxiv 2025 `10.26434/chemrxiv-2025-qj66b`(ref [34] — 공극률–압력의 출처, ⚠ 심사 전 프리프린트인데 이 편의 두께 전부가 걸려 있다).
- lint: **0 errors** (pages 44 · raw files 45).

## [2026-09-22] ingest | `assb` 17호 — Yanev, Heubner, Nikolowski, Partsch, Auer, Michaelis 2024, Editors' Choice: Alleviating the Kinetic Limitations of the Li-In Alloy Anode in All-Solid-State Batteries (*J. Electrochem. Soc.* 171, 020512) 실험 + 3전극 + SI

- raw: `raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md` (doi `10.1149/1945-7111/ad2594`, **CC BY 4.0 · Editors' Choice**, Fraunhofer IKTS Dresden + TU Dresden; 본문 8쪽 + **SI 2쪽**, PDF sha256 `8fb10ec47e613614…` / SI `5e3fdd576b865b2d…`, 본문 sha256 봉인). 큐 **16번**. 접수 2023-11-29 → 게재 2024-02-12.
- 크로핑: `raw/figures/yanev2024_li-in-alloy-anode-kinetic-limitations/` **6장**(본문 Fig. 1/3/4/5 + SI Fig. S1/S2). **실제로 본 것: 6장 전부 + Figure 2**. ⚠ **캡션 크로퍼가 Figure 2(사진 2장)를 놓쳤다** — 임베디드 JPEG 라 기하 검증에 안 걸렸다. `page.get_image_rects('Im3')` 로 직접 렌더해 열람. 그 위에 Fig. 1(g–i · d–f · a–c) · Fig. 4(a · c · d) · Fig. 5(a · b) 를 **500–1100 dpi 로 재크롭**해 수치 판독. **안 본 것 0.**
- **셀**: 단결정 **NCM811** : Li₆PS₅Cl : VGCF = **73.2:24.0:2.8 wt%** ‖ LPSCl 분리막 ‖ **Li-In(제조법 3종 × 조성 스윕)**. `[재현]` **19.1 mg cm⁻² · 2.80 mAh cm⁻² · 공칭 200 mAh g⁻¹**(역산 정합 ✔, 1 C = 2.80 mA cm⁻²). 2전극 ∅10 mm/**30 °C** · 3전극 ∅12 mm/**실온**, **둘 다 운전 50 MPa**, 제작 500 MPa. **셀 12개 · 조건당 n = 1 · 최대 5 사이클**(형성 2 + CA 율시험 3). ⚠ **열화가 없는 편이다** — `LAM`·`LLI`·`SOH`·`aging`·`cycle life` **전수 0회**.
- ★★★★ **최대 수확 — 이 닻 카드의 물음이 한 셀 안에서, 전극 분해로 실증된다. 그리고 경로가 새롭다**: 1–16호의 For 근거는 **양극 안**의 혼동(접촉 손실 ↔ 진짜 활물질 손실)이었는데, **17호는 양극 밖의 경로를 연다 — 양극은 멀쩡한데 상대극 때문에 줄어 보인다.** 같은 양극·같은 프로토콜·**0.1 C** 에서 2전극이 보는 것은 `[도표]` **방전 용량 198 → 185 mAh g⁻¹ (−6.6 %) + 곡선의 끝이 잘림**(= `LAM_PE` 의 서명)인데, 3전극이 말하는 것은 `[재현]` **양극 임피던스가 동일**(≈31 ↔ ≈32.5 Ω, 5 % 차)이고 `[도표]` **`E_CE` 가 방전 끝에 0.62 → ≈1.0 V** 로 올라 `E_cell` 하한 2.38 V 에 조기 도달 ⇒ `[재현]` **양극이 3.0 V 대신 ≈3.4 V 에서 멈춘다.** **활물질은 그대로다.** 반대 방향의 짝도 같은 논문 안에: `[인쇄]` 과리튬화(foil 50 at%)로 기준이 **−0.2 V** → `[인쇄]` **컷오프 4.3 → 4.1 V** → 충전 용량 40 mAh g⁻¹ 감소(= **`LLI` 흉내**). ⇒ **한 논문 안에서 `LAM_PE` 흉내와 `LLI` 흉내가 둘 다 나온다.**
- ★★★★ **Q5(Li-In 기준 전위)의 실제 폭이 처음으로 숫자가 됐다 → 새 개념 페이지** [[assb-li-in-reference-potential-window]] (`assb` **열째**). 세 가지를 갈라 부른다: **① 열역학 평탄 ±10 mV 안**(그보다 좁게 잰 편이 없다) · **② Li-rich 이탈 `[인쇄]` −0.2 V**(충전 중, 전극 전체) · **③ In-rich 국소 고갈 `[인쇄]` +0.68 … +0.78 V**(방전 중, 계면). **전체 폭 0.42 → 1.40 V ≈ 0.98 V**, 그리고 **양 끝이 모두 "Li-In 음극" 이라 불린 셀**이다.
- ★★★ **우리가 한 옴 분리**(논문이 하지 않은 연결 — Fig. 5 의 CE/RE 고주파 절편 `[도표]` foil ≈28.7 Ω 을 `E_CE` 편차에서 뺀다; A = 1.131 cm², 공칭 3.167 mAh): `[재현]` **0.1 C → 9.1 mV = 관측 편차의 ≈100 %** · **CA 초기(≈18 mA) → 0.52 V = 76 %** · **CA 정상(≤0.063 mA) → ≈1.8 mV = 0.2 %**. ⇒ ★★★★ **전류가 종료 기준(0.02 C)까지 떨어진 뒤에도 foil 의 `E_CE` 가 ≈1.35 V 에 6 h 이상 머문다 — 과전압이 아니다.** ⚠ "평형 전위" 는 `[해석]` 이다: **CA 후 이완 곡선을 재지 않았다**(G2). 그리고 **0.1 C 의 "음극 과전압 ≈10 mV" 는 옴과 구별되지 않는다** ⇒ **이 편이 "평탄하다" 고 확인한 쪽의 분해능도 ±10 mV 가 바닥이다.**
- ★★★ **대표 숫자**: **같은 프로토콜 · 전류 ≈0 · 같은 공칭 조성(40 at% Li) 의 두 Li-In 음극이 `E_CE` = 0.61 V ↔ 1.35 V, ≈0.74 V 갈린다. 차이는 제조법뿐이다**(Li·In 박 압착 ↔ Li-In+SE 분말 복합).
- ★★★ **곱 축퇴 검사(16호 처방)의 첫 적용은 "적용 불가" — 그리고 그 이유가 정보다.** `R_CT`·`C_dl`/`Q_DL`·`CPE`·`capacitance`·`equivalent circuit`·`ECM`·`DRT`·**`fit*` 전수 0회**, `[인쇄]` "Detailed quantitative analyses and **modelling of the impedance spectra are beyond the scope of this study**". **세 편의 실패 양식이 다르다: 9호 = 곱을 적합했다 · 16호 = 곱 위에 서서 한쪽 끝을 골랐다(`θ≡1`) · 17호 = 곱을 만들지 않았다.** `[해석]` **역설적으로 17호가 가장 안전하다**(배정하지 않았으므로 잘못 배정할 수 없다) — 대신 **가져갈 숫자도 0**.
- ★★ **그래도 곱 축퇴가 다른 자리에 있다 — 문장으로.** SE 분말을 넣는 조작 **하나**가 (i) LiIn↔SE **접촉 면적**(`[인쇄]` "high effective **contact area**")과 (ii) 음극 **유효 이온전도도**(`[인쇄]` "confirms that the **effective ionic conductivity** … plays an important role")를 동시에 올리고 **둘을 따로 움직인 실험이 없다**. `[재현]` 그리고 배정이 숫자로도 안 받쳐진다 — 2전극 총 임피던스 SE **20 % ≈36 Ω → 40 % ≈27 Ω (Δ ≈9 Ω)** 인데 `[도표]` **복합 음극 전체가 ≈6 Ω** 이고 **3전극은 40 % 쪽만 쟀다** ⇒ Δ 를 음극에 다 줄 수 없다.
- **Q4 열 번째 성질 = "인쇄로 사양했다"**: `identifiab*`·`uniqu*`·`uncertaint*`·`condition number`·`error bar`·`confidence`·`n =`·`fit*` **전수 0회**(NFKC · 대소문자 구분 · 표지 제외; `flam*`·`Soh` 오검출 0 확인). 계보: 안 쟀다(1–7) → 이름만(8) → 지문이 자기 표에(9) → 분야가 명제로(10) → 재료만(11) → 0(12·13) → 역문제 없음(14) → 추정기 없음(15) → 밟고 지나갔다(16) → **17호: 역문제가 눈앞에 있는데 지면이 명시적으로 사양했다.** ★ **그 사양이 결론을 방어한다** — 결론이 적합의 출력이 아니라 **전압계 판독**이라 축퇴할 자리가 없다(14호는 귀속이 **가정**, 17호는 **배선**). ⚠ 단 그 배선에도 오염원 둘(옴 · RE 안정성)이 있고 논문은 둘 다 안 다룬다. **여전히 0/17.**
- **Q1~Q8: 16편 ≈9.5 → 17편 ≈10.0 — 두 편 연속으로 칸이 움직였다** (**Q5 +0.5**; 16호가 기준극을 *설치*한 편이었다면 17호는 **기준 전위 자체를 재고 그 폭을 주제로 삼은 첫 편**). **Q1·Q4 그대로 0.** Q2 ★★★(계보 두 번째 전극 분해, **첫 전위 채널**) · Q3 ★★ **새 층위 `measured-potentiometric`**(적합도 형태학도 도함수도 역변환도 아닌 **전압계 판독**) · Q6 **한 점(50 MPa)** · Q7 해당 없음 · Q8 ★ **V–Q 곡선 11장**(10·11호가 0장이던 칸, ⚠ `OCV`·`GITT` 0회).
- ★ **우리가 한 자기 검증 둘** (논문이 하지 않는다): ① `[재현]` `Z_WE/CE ≈ Z_WE/RE + Z_CE/RE` 가 **2 Hz 에서 두 셀 다 1 % 안**(foil 고주파 절편만 7 % 어긋남 — 음극 임피던스가 거대할수록 3전극 아티팩트가 크다) ② `[재현]` **RE 표류 상한 ≈20 mV / 20 h**(복합 셀 `E_CE` 가 0.61–0.63 밖으로 안 나감) = **계보 최초의 기준극 표류 상한**, ⚠ 엄밀히는 (RE 표류 + 음극 과전압 + 옴) **합의 상한**.
- 어긋남 원장 **15건**: **D3** `[인쇄]` In 75 mg + Li 3.6–4.4 mg ⇒ `[재현]` **44.3–49.3 at%** ↔ 라벨 **45–50 at%**(50 at% 엔 4.53 mg 필요; 논문 스스로 "2 at% 가 결정적" 이라 쓰므로 **그 단차의 35 %**) · **D4** 2전극 **30 °C** ↔ 3전극 **"room temperature"** 인데 목적이 `[인쇄]` "to **reproduce** the two-electrode cell experiments"(`[재현]` 면적 정규화 HF 저항 **≈29 ↔ ≈47 Ω cm² = 1.6배**, LPSCl `E_a≈0.35 eV` 가정 시 온도만으로 1.4배) · **D5** 3전극 분리막은 **375 MPa**, 2전극은 500 · **D6** ★★★ **3전극 foil 셀은 40 at% — 2전극에서 시험한 어떤 foil 셀(45/47/49/50)도 아니고, 논문이 찾은 sweet spot 49 at% 는 전극 분해로 검증된 적이 없다** · **D7** **Fig. 2 의 시편은 "10 mm 를 13 mm 다이에"** 눌러 **측면 유동이 허용된 기하**인데 실제 셀은 구속돼 있다(무언급) · **D8** "ca. 50 % SOC" 자기 모순(충전은 "실험 용량의 절반" = 셀마다 다름 ↔ 캡션은 공통 라벨, 그리고 고주파 산포를 "SOC 민감도" 로 넘긴다) · **D11** **Table S1 "추세"(foil 45→49 at% 0.5 %p)가 유일한 산포 대용(같은 40 at% 복합 두 셀 2.2 %p)의 1/4.4** — 반복 0 이라 오차 바닥이 없는데 그 위에 "Li-rich 일수록 SE 분해" 기구 주장이 얹힌다(독립 관측 0) · **D12** **ref 32 = 우리 10호 Vadhva 2021**, 원전은 `[인쇄]` "In–Li 셀은 LMA 셀과 귀속이 **반대** … **system-by-system basis**" 인데 17호는 `[인쇄]` "have **established**" 로 옮긴다(⚠ **자기 화학에 대해서는 정합**이고 Fig. 5 가 실증한다; **우리 위키의 원전 대조 두 번째 사례**) · **D14** **EIS 를 충전 상태 + 5 h 이완에서 쟀는데 foil 음극이 100 mHz 에서도 안 닫힌다**(실축 ≥58 Ω) ⇒ `[해석]` 고갈층이 다음 충전·이완으로 안 돌아온다(또는 5사이클 계면 열화 — **가르는 관측 0**) · **D15** **RE 도금 전하가 음극에서 나오는데 조성은 "40 at% 고정"**(`[재현]` 셀 면적 기준 1.87 mAh ⇒ foil −2.8 at% · 복합 −4.5 at%; ⚠ **110 µA cm⁻² 의 기준 면적 미명시**). 그 밖 **D1** 그림 번호 오기(분말 임피던스를 "Fig. 1f" 로 — 실제는 1h) · **D2** 부등호 반전("very low frequencies **>**0.3 Hz") · **D9** 50 at% 셀만 기준축이 0.2 V 다른데 Fig. 1g 에서는 그 계산을 안 한다 · **D10** 균질성 비교에 공통 척도 없음(광학 사진 ↔ BSE-SEM) · **D13** Fig. 3 이 In-rich 층의 **제조 기원 ↔ 방전 기원**을 합친다(가르는 실험 0).
- 공백 원장 **12건**: **G1 ★★★ 개방회로 `E_CE` 가 한 번도 인쇄되지 않는다**(셀 안에 Li RE 가 있고 4 h·5 h 이완이 프로토콜에 있는데 — **0.62 V 는 끝까지 인용값**) · **G2 ★★★ CA 후 이완 곡선 0**(과전압 ↔ 기준 이동을 가르는 유일한 측정) · G3 반복 0·`n =` 0 · G4 적합 0 · G5 접촉 면적 값 0 · G6 SE 20 %↔40 % 를 전극 분해로 안 쟀다 · **G7 화학·단면 분석 전수 0**(XRD·EDS·XPS·단면 SEM·post-mortem — **중심 기구인 In-rich 층이 직접 관찰된 적이 없다**) · G8 압력 한 점 + Wang 과의 불일치를 압력으로 넘기며 상대 압력값 0 · G9 사이클 수명 0 · G10 도금 전류밀도 기준 면적 미상 · G11 "experimental capacity" 정의 미상 · G12 데이터 가용성 문장 0.
- ★★★ **문헌 쪽에서 온 두 번째 "인쇄된 요구"**: `[인쇄]` "prevent the possibility of **misinterpretation of anodic effects as cathodic effects** in typical half cells" + `[인쇄]` "**the deconvolution of half-cell impedance spectra** … could be **severely complicated by overlapping anode impedance**" + `[인쇄]` "**Insufficient reproducibility, which is hardly reported in ASSB half-cell studies, at moderate C-rates can be easily explained by anode dominated data**". 8호(Li 2026)의 "distinguishing contact loss from ordinary electrochemical aging" 에 이은 두 번째이고 **이쪽은 1차 측정을 동반한다.**
- ★★ **16호와의 대질(`[해석]`, 미검증)**: 16호 음극은 **순수 In 박**이라 Li 가 **분리막 쪽에서** 들어와 **LiIn 이 필요한 자리에 생기고**, 17호 foil 은 Li 박을 **집전체 쪽에서 기계적으로** 눌러 `[인쇄]` "do not reach the separator side" 다. ⇒ 16호가 `x_Li` **0.05–0.28**(훨씬 Li-poor)인데도 음극 임피던스가 `[인쇄]` **4–9 Ω cm²** 인 것이 설명된다(17호 foil 은 `[재현]` **≥66 Ω cm², 미폐**). ⚠⚠ **압력이 2–8배 다르고**(50 ↔ 97/389 MPa) SE·조성·전류·SOC 가 전부 다르다 — **두 편을 가로지르는 가설이지 어느 편의 결론도 아니다.** 검증 실험은 17호 자신이 인용한다(ref 21 Sedlmeier — Li 쪽을 분리막으로 돌리면 **저장고는 커지고 SE 계면 안정성은 나빠진다**).
- 컴파일: **새 개념 페이지 1** [[assb-li-in-reference-potential-window]] (`assb` 열째 — Q5 축이 반복 참조될 것이 확실하다: 큐 **17**(Fukunishi 2023)·**19**(embedded indium RE)·**20**(μ-RE, Indium-Lithium anodes)가 전부 이 축이고, 4·10·16·17호가 이미 걸린다. `evidenceScope: multi-source-primary`, `confidence: medium`). 갱신 — [[assb-contact-loss-vs-lampe]] (채움표 **17행** + **17호 절 9항** + Evidence For **열네 번째** + Against 에 "세 번째 전극(전위 채널)" 항 + "아직 모르는 것 2" 갱신 + Status Log + "주장하지 않는 것" 6항) · [[assb-lampe-contact-product-degeneracy]] (**§"처방의 첫 적용 — 적용 불가"** + 면적↔전도도 공변 + **§"음극 오염"** 이 처방표에 한 줄 추가: 다중 SOC EIS 는 3전극/대칭셀과 짝지어야 한다 — **16호는 3전극이었고 9호는 2전극이었다**) · [[assb-apparent-capacity-decomposition]] (**§"네 번째 항" — `E_cut^eff = E_cell,min + E_CE(i, x_Li, 제조법)`**; ★ **율 스윕 분리 시험이 이 항을 못 지운다**, `η` 가 아니라 축의 원점) · [[assb-stack-pressure-operating-window]] (**§17호 — 한 점, 그리고 압력이 데이터 없이 설명 변수로 쓰인 첫 사례**; 새 빈칸 `Z_anode(P)` 를 제조법 고정하고 재는 편 0). **`index.md` +1 (45 페이지).**
- ⚠ **규율**: 0.98 V 를 **Li-In 물질의 성질로 옮기지 않는다**(조성 × 제조법 × 율 의 폭이다) · "기준 전위가 1.35 V 로 옮겨 갔다" 고 **단정하지 않는다**(확실한 것은 "옴이 아니다" 까지, G2) · **Table S1 의 CE 를 `LLI` 대리로 쓰지 않는다**(D11) · 압력을 결론에 넣지 않는다(한 점) · **`E_CE(N)`·`E_CE(P)` 는 여전히 0편** · **Q4 는 0/17**.
- 후속 후보 (원전 우선): ★★★ 1 **Santhosha, Medenbach, Buchheim, Adelhelm, *Batteries & Supercaps* 2019** (ref 26 — **0.62 V 가 태어난 자리**, 쿨로메트릭 적정 + `[인쇄]` "Li-richer phases … strongly dependent on small lithiation changes". 우리 Q5 의 열역학 바닥이고 16호(0.58↔0.47 V)·17호(±10 mV)의 산포를 대조할 유일한 기준. ⚠ 서지가 `[인쇄]` "414, 359 (2019)" 로 권호가 이상하다) · ★★★ 2 **Nam, Park, Oh, An, Jung, *J. Mater. Chem. A* 2018, 6, 14867** (ref 20 — **Li-In-SE 복합 음극의 원전**이자 "Li-depleted In-rich layers" 의 원전; 17호의 처방과 기구 설명이 전부 여기서 온다) · ★★★ 3 **Sedlmeier, Schuster, Schramm, Gasteiger, *JES* 2023, 170, 030536** (ref 21 — **Li 박 방향 뒤집기 실험이 이미 여기 있다** = 16호↔17호 대질의 검증 실험) · ★★ 4 **Ikezawa, Fukunishi, …, Kanno, Arai, *Electrochem. Commun.* 2020, 116, 106743** (ref 16 — ⚠ **큐 17번(Fukunishi 2023)과 같은 그룹**이고 16호의 유일한 외부 실측 대조군이었다; **큐 17번을 먼저 읽는 것이 경제적일 수 있다**) · ★★ 5 **Yanev et al., *JES* 2022, 169, 090519** (ref 29 — 이 편의 CA 율시험 방법 원전; "저율 평탄 + 급락 = 양극 제한" 형태 기준의 문턱이 거기 있어야 한다) · ★ 6 **Wang, Zhao, …, Huang, *eScience* 2023, 3, 100087** (ref 28 — 17호와 **정면 충돌**, `[인쇄]` 14.3 at% Li 가 최적; Q5·Q6 양쪽) · ★ 7 **Krauskopf, Mogwitz, …, Janek, *AEM* 2019, 9, 1902568** (ref 14 — 합금 음극 확산 한계; `D_Li(In)` 이 있으면 "6 h 에 안 돌아온다" 를 시간 척도로 검증할 수 있다). ⚠ **큐 대조: 1·2·3 순위는 큐에 없다.**
- lint: **0 errors** (pages 45 · raw files 46).

## [2026-09-22] ingest | `assb` 18호 — Fukunishi, Tabuchi, Ikezawa, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai 2023, AC impedance analysis of NCM523 composite electrodes in all-solid-state three electrode cells and their degradation behavior (*J. Power Sources* 564, 232864) 실험 + 3전극 + 열화 + SI

- raw: `raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md` (doi `10.1016/j.jpowsour.2023.232864`, © 2023 Elsevier — 오픈액세스 아님, Tokyo Institute of Technology + All-Solid-State Battery Center, NEDO **SOLiD-EV** P18003; 본문 10쪽 + **SI 6쪽**, PDF sha256 `c0798ee510063429…` / SI `773e6fbca1d7b938…`, 본문 sha256 봉인). 큐 **17번**. 접수 2022-11-07 → 승인 2023-02-20 → 온라인 2023-03-03.
- 크로핑: `raw/figures/fukunishi2023_ncm523-three-electrode-impedance-degradation/` **13장**(본문 Fig. 1–7 + SI Fig. S1–S4 + 표 2). **실제로 본 것: 그림 11장 전부** + 캡션이 없어 크로퍼가 놓친 **1쪽 Graphical Abstract 를 직접 렌더**해 열람(+ Fig. 5c 는 500 % 확대 재판독). 안 본 것: 표 크롭 2장(PDF 텍스트가 정확). **누락 기계 확인** — `get_images()`/`get_drawings()` 페이지별 계수(p1 4img · p3 2 · p4 1 · p6 2 · p7 1 · p8 1)로 **캡션 앵커가 본문 그림 7장을 전부 잡았고 놓친 그래픽은 무캡션 도판 1건뿐**임을 확인.
- **셀**: **LiNbO₃ 코팅 NCM523**(D50 **5.0** / 11.2 µm, 다결정) ‖ **LPSI**(glass-ceramic Li₂S-P₂S₅-LiI, 2.6 mS cm⁻¹) 또는 **LPSCl**(argyrodite, 1.8 mS cm⁻¹) ‖ **Li-In**, 기준극 = **R-LTO 메시**(부분환원 Li₄Ti₅O₁₂, φ9 mm Ni 메시). PET 관 φ10 mm, SE 층 **1.3 mm(상대극 쪽) / 1.0 mm(작업전극 쪽)**, **110 MPa 압착**. 양극 **6.0 mg · 7.6 mg cm⁻²** ⇒ `[재현]` 활물질 **3.7–5.2 mg cm⁻²**(계보 최박). ⚠⚠ **두 계의 복합양극 조성이 다르다** — `[인쇄]` **49:43:8.0** ↔ **69:26:5.0 wt%**, 근거는 "preliminary tests" 뿐(**교락**). 내구 시험 **1.0 C × 50 사이클 × 333 K**, RPT **0.1 C × 298 K** 전후. **조건당 n 미상**(`n =` 0회).
- ★★★★ **최대 수확 ① — 이 닻 카드의 물음이 지면에 문장으로 인쇄되고, 갈리지 않는다.** `[인쇄]` "R3 drastically increased (6 times larger) … These results suggest that the **chemical composition at the interface or the contact area** between the NCM523 and electrolyte particles changed." 그리고 같은 절이 **`θ_AM` 의 기구를 서술한다**: `[인쇄]` "if insulative layers **completely cover** the active material to make the particle **inactive**, such **dead particles** probably have no contribution to the charge transfer process. This could explain the **large capacity decrease**." **값 0.**
- ★★★★ **최대 수확 ② — 16호 처방(`R_CT·C_dl`)의 첫 성공. 저자의 표로 저자의 "or" 를 갈랐다.** 면적만 잃으면 `C` 비 = 1/(R 비), 동역학만 나빠지면 1.00. `[재현]` (Fig. 5 로그 막대 판독, `C ≡ τ/R`, ±18 %): **LPSI R3 → C 비 0.37 ± 0.07**(R ×6.5, τ ×2.4) = **유효 면적 ≈2.7배 감소 + 고유 `R_ct` ≈2.4배 증가** · **LPSCl R3 → C 비 1.07 ± 0.19**(R ×7.4, τ ×7.9) = **면적 손실 없음, 전부 고유 동역학**. ★ **그리고 그 분해가 같은 논문의 SEM 과 독립으로 일치한다** — `[인쇄]` **LPSI 에만** 2차 입자를 두르는 **O·P 퇴적층(2 µm)**, LPSCl 은 "not apparent". ⚠ **측정이 아니라 지면 두 열의 조합**이다(노화 후 `p` 미공개 · `C∝θ` 가정 · 셀 1개).
- ★★★ **처방이 정련된다 — 검사 A(신품 입자크기 축)가 처방의 전제를 흔든다.** 논문의 논증은 `R3` 비 0.5 = 접촉 면적 비 2.0–2.4 의 역수 ⇒ `[인쇄]` "uniform physical contact". 그런데 `[재현]` `C_eff = Q^{1/p}R^{(1-p)/p}` 비는 **`p` 가 같은 두 온도에서 0.68(293 K) / 1.10(303 K)** — **예측 2.0–2.4 와 2–3배 어긋난다**(맞는 유일한 온도 283 K 는 `p` 가 0.57↔0.76 으로 달라 두 `Q` 의 차원이 애초에 다르다). ⚠ **반증으로 적지 않는 이유**: 같은 계면의 `C_eff` 가 **283/293/303 K 에서 4.4배** 움직인다 ⇒ `Q` 자체가 잘 안 정해지고, **Table S1 에서 ± 가 빠진 유일한 열이 `CPE2-C`·`τ3`** 다. ⇒ 처방이 **"두 값을 보고하라" → "두 값 + 면적을 아는 대조군을 같이 보고하라"** 로 바뀐다.
- ★★★★ **17호가 연 오염 경로가 18호에서는 설계상 닫혀 있다.** `[인쇄]` **컷오프가 작업전극 전위**(0.85–2.65 V = 2.40–4.20 V vs Li)이고 `[도표]` **Fig. 1(b)(d) 가 상대극이 전 구간 평탄(≈0.60 V)임을 보인다** ⇒ `[인쇄]` "the amount of **effective active material** decreased **only in the LPSI system**" 은 **상대극 오염 없이 말해진 이 계보 첫 양극 활물질 손실 문장**이다(⚠ 값 0 — 그래서 반 칸).
- ★★★★ **16호와의 3전극 배정 대질(이번 흡수의 1순위)**: **고주파(≈1 MHz, 집전체 전자 접촉)와 중주파(전하이동)는 같다** — 그리고 18호 쪽에 **대칭셀 독립 근거**가 있다(16호는 문헌 인용). **저주파가 다르다**: **다결정 NCM523 은 `R4`(~1 Hz, 2차 입자 내 1차 입자 간 전하이동)를 저주파에 하나 더 놓고 그것이 음극 기여와 겹친다**. 16호는 **단결정**이라 없다 — **두 편이 서로 인용하며 동의한다**. ⇒ ★ **"저주파 = 음극" 규칙은 화학뿐 아니라 양극 미세구조의 함수다** (10호 화학 → 11호 상태·배선 → 16호 부분의 합 ≠ 전체 → **18호 미세구조**). 그리고 `[인쇄]` 18호 자신이 "The existence of **R4 is apparent when the three-electrode cell is applied to separate the Li-In component**" 라고 적는다 — **3전극이 없었으면 `R4` 는 "음극 열화" 로 읽혔을 것**이다.
- ★★★ **DRT — λ 가 봉우리 개수를 정하는 사슬이 지면에 그대로 있다.** `[인쇄]` "First, the **time constants obtained from the DRT analysis were fixed** and the other parameters were refined" ⇒ **λ → 봉우리 개수 → 회로 차수 → `R3`/`R4` → "열화의 주 원인"**. 그리고 `[인쇄]` "the independent components of R2 to R4 are **confirmed by using λ = 8.5×10⁻⁴**" — **개수가 λ 의 출력이 아니라 λ 선택의 목표다.** ⚠⚠ **두 λ 가 70배 다르고**(LPSI **6.0×10⁻²** ↔ LPSCl **8.5×10⁻⁴**) **봉우리 개수도 3 ↔ 4** 인데, 논문은 그 차이를 **재료 탓**(LPSCl 의 낮은 Young 계수 → void)으로 돌리고 **λ 를 같게 둔 비교 그림이 없다**. ★ 반면 **C2(K–K / Lin-KK)는 이 계보 최초로 통과** — ⚠ 그 잔차를 `[인쇄]` **"기준극의 안정성"** 근거로 쓰는 것은 **범주 오류**이고, 잔차 축이 `[도표]` **무차원 ±0.6 스케일에 0.2–0.4** 까지 간다.
- ★★★ **Q5 — 17호와 모순이 아니라 반대편 끝.** `[재현]` Li-In 상대극 **`x_Li` 37.7 → 40.0 at%**(2상역 한복판), **Li 재고 / 이동 전하 = 9.5배**, **0.1 C = 0.054 mA cm⁻²** = 17호 0.1 C 의 **1/5** · 17호 CA 의 **1/300** ⇒ **17호가 본 고갈(+0.7 V)이 일어날 수 없는 설계**다. 두 편을 겹쳐 **경계 조건 여섯**이 생긴다(조성·LiIn 위치·율·옴 + **재고비 ≥ 한 자릿수**·**전류밀도 ≲0.1 mA cm⁻²**). ⚠ **셋 중 무엇이 지배적인지 가른 실험은 0편.** ★ 그리고 **"기준을 Li-In 에서 빼는 길"**(제3물질 기준극 R-LTO)이 처음 보이지만 **가정이 옮겨갈 뿐 사라지지 않는다** — `[인쇄]` "**Assuming** … **1.55 V**", 자기 셀 검증 0, 순환 논증(가정값으로 얻은 평탄값이 문헌과 맞으니 가정이 맞다). ★ 부수 확인: 18호의 **Santhosha 2019 서지가 정상**("2 (2019) 524–529") ⇒ **17호의 "414, 359 (2019)" 가 오기임이 확인된다.**
- **Q4 열한 번째 성질 = "갈림을 인쇄하고 가르지 않았다"**: `identifiab*`·`uniqu*`·`uncertaint*`·`degenerac*`·`condition number`·`error bar`·`n =` **전수 0회**(NFKC·대소문자 구분; `flam*`·`Soh`·`[Ll]am[a-z]` 오검출 0 확인). ★ **그러나 계보 최초로 ± 를 인쇄한다**(Table 1 의 Ea 16개, Table S1 의 `R3`·`p`) — ⚠ **자기 ± 를 결론에 쓰지 않는다**(D5). 계보: 안 쟀다(1–7) → 이름만(8) → 지문이 자기 표에(9) → 분야가 명제로(10) → 재료만(11) → 0(12·13) → 역문제 없음(14) → 추정기 없음(15) → 밟고 지나갔다(16) → 인쇄로 사양(17) → **18호: 갈림을 인쇄하고 다음 문단으로 간다. 그리고 가를 입력이 자기 표에 있다** (9호가 "지문이 자기 표에" 였다면 **18호는 "해답이 자기 표에"**). **0/18.**
- **Q1~Q8: 17편 ≈10.0 → 18편 ≈10.5 — 세 편 연속으로 칸이 움직였다** (**Q1 +0.5** — `[인쇄]` **Image-J 로 SE|활물질 접촉 면적을 실제로 쟀다**, 계보 최초의 이미지 기반 접촉 면적 측정. **반 칸인 이유**: 나온 것이 **비 2.0** 하나뿐이고 절대 분율·오차 0, **노화 축 `θ(N)` 은 여전히 0** — 이번에는 **도구와 시편이 둘 다 지면에 있었는데도**). **Q4 그대로 0.** Q2 ★★★(계보 세 번째 전극 분해, **열화를 동반한 첫 편**, 관측 7종) · Q3 fitted(**+ 계보 최초의 ±**, 단 용량 축은 실측) · Q6 **`pressure` 0회** · Q7 해당 없음(⚠ `dead` 1회는 **양극**) · Q8 ★★(V–Q 6장 + **`R3(SoC)` 5점**).
- ⚠⚠ **Q6 — 압력이라는 낱말이 없는 열화 논문.** `pressure`·`stack pressure`·`hysteres*` **본문 0회**, `MPa` 2회(**110 MPa** 셀 · **150 MPa** 대칭셀), **운전 압력은 값도 장치도 문장도 없다**(PET 관 → Ar 폴리스티렌 용기). 그런데 **두 열화 기구 중 하나가 `void formation`**(`void` **7회**, 실측 편 최다)이고 LPSCl 의 추가 반원도 void 로 설명된다 ⇒ **압력에 가장 민감한 양을 주인공으로 삼으면서 압력을 통제하지 않은 첫 실측 편**(16호 49회 · 17호 7회 · **18호 0회**).
- 어긋남 원장 **17건**: **D1 ★★★ Fig. 3 캡션 "(b),(c) ×2500" ↔ 스탬프 2500x/1000x**(스케일바 10↔20 µm, HV 15↔10 kV, EDX 채널 10↔7종) — **유일한 접촉 면적 측정의 원자료다** · **D2 ★★ Table S1 의 τ3 6개 중 3개가 `(R·Q)^{1/p}` 와 정확히 10배 어긋난다**(303 K 의 둘은 **방향이 반대**) · **D3 ★★★ "the time constants are nearly unchanged" 가 인쇄된 표(비 8.2/2.9/0.018)로도 우리 재계산(1.20/0.33/0.54)으로도 성립하지 않는다** · **D5 ★★ "Ea(R2) remained almost unchanged" ↔ Table 1 의 LPSI 70±20 → 41±8(구간 불일치)**, 반대로 "Ea(R3) increased" 는 LPSI 에서 49±6 → 54±1 로 **구간이 거의 포개진다** · **D6 ★★ LPSCl 의 R2(집전체 전자 접촉)가 `[도표]` 6.9배 자라는데 무언급** · **D8 ★★★ 자기 조건문의 귀결이 자기 데이터와 반대다**("퇴적층이 저항성 화합물이면 R3 증가가 LPSI 에서 더 클 것" ↔ 같은 절 "R3 증가는 두 계가 같다") · **D9 ★★ 결론 "주 원인은 R3" ↔ R3 는 두 계에서 같이 자라는데 용량 손실은 LPSI 에만** · **D10 ★★ Fig. S3(a)(d) 에서 3전극 합 ↔ 2전극이 중주파에서 ≈13 %·≈60 Ω 어긋난다** ↔ 본문 "agree well" · **D14 ★★ Fig. 7 before 가 5 kV, after 가 15 kV** — "LPSCl 엔 퇴적층 없음" 이 그 위에 있다 · **D17 ⚠ 같은 이름표의 `R3` 가 55/60/79 Ω 로 1.45배**(= 우리가 만든 유일한 셀 간 산포 추정 **≈±20 %**; 노화 6.5배는 그 위에 안전, **입자 크기 2.0배는 여유가 훨씬 적다**). 그 밖 D4(2.4 ↔ 반경비 2.24) · D7(K–K 잔차 축 무차원) · D11(SI 캡션 "(d-e)" ↔ 패널 셋, S2(d)만 축이 잘림) · D12(반원 둘은 93.5 mg 뿐) · D13(Fig. 5c 라벨 `R1′+R2′` — 본문·회로도에 `R2′` 없음) · D15(7.9 ↔ 8.011 Ω) · D16(ref 33 연도 "(2022)" ↔ 실제 1995).
- 공백 원장 **16건**: **G1 셀 개수 0** · **G2 운전 압력 0** · **G3 두 계의 양극 조성이 다르다(교락)** · **G4 R-LTO 1.55 V 가정** · **G5 K–K 로 기준극 안정성을 주장(범주 오류)** · **G6 접촉 면적 절대값·노화 축 0 — 도구와 시편이 지면에 있는데도** · **G7 `CPE2-C` 에만 ± 없음** · **G8 노화 후 파라미터 표 없음(`p` 미공개)** · **G9 `Wo` 값 0**(가장 크게 자라는 성분인데) · **G10 λ 선택 규칙 0** · G11(Young 계수 단위 없음, 계산값 ↔ glass-ceramic) · G12(SoC 정의) · G13(대칭셀 2점 외삽을 4유효숫자로) · G14(Fig. 5 조건 미표기) · G15(데이터 on request) · G16(`LAM`/`LLI`/`SOH` 0, "effective active material" 1회에 값 0).
- 컴파일: **새 개념 페이지 0** (SCHEMA Page Thresholds — 새 축이 아니라 기존 네 축이 전부 굵어졌다). 갱신 — [[assb-contact-loss-vs-lampe]] (채움표 **18호 행** + **18호 절 9항** + Evidence For **열다섯 번째** + "모르는 것 1·2" 갱신 + Status Log + "주장하지 않는 것" 6항) · [[assb-lampe-contact-product-degeneracy]] (**§"처방의 두 번째 적용 — 첫 성공, 그리고 전제의 발견"**: 검사 A/B 표 + 처방 정련 + 처방표 행 갱신 + evidenceScope 근거 2편 → **3편**) · [[drt-peak-count-nonidentifiability]] (**C1·C2 18호 열** + "개수가 λ 의 목표다" + **§네 번째 경보 "주파수 → 전극 규칙은 양극 미세구조의 함수다"**) · [[assb-li-in-reference-potential-window]] (**§18호 5항** + 평탄 조건 **(5)(6)** + 처방 **P6·P7**) · [[assb-stack-pressure-operating-window]] (**§"압력이라는 낱말이 없는 열화 논문"**). **`index.md` 변화 없음** (컴파일 페이지 45 유지).
- ⚠ **규율**: **`C` 비 분해를 측정값으로 쓰지 않는다**(로그 막대 판독 · `p` 미공개 · `C∝θ` 가정 · 셀 1) · **"활성 접촉 ≈2 %" 를 인용하지 않는다**(비용량 10 µF cm⁻² 는 우리 가정, `C_eff` 가 4.4배 흔들린다) · **LPSI ↔ LPSCl 차이를 전해질의 성질로 옮기지 않는다**(조성 교락) · **열화 값을 다른 셀로 옮기지 않는다**(3.7–5.2 mg cm⁻², 0.54 mA cm⁻², 333 K, 압력 미상) · **압력에 대해 아무것도 주장하지 않는다** · **Q4 0/18**.
- 후속 후보: ★★★★ 1 **Ikezawa, Fukunishi, …, Kanno, Arai, *Electrochem. Commun.* 116 (2020) 106743**(ref 27 — **R-LTO 기준극과 이 편 방법의 원전**; 1.55 V 의 근거·안정성·"Li-In 상대극의 영향이 유의하다" 가 전부 거기 있다. ⚠ **16·17·18호 세 편이 전부 이 한 편을 가리키는데 큐에 없다**) · ★★★ 2 **Illig, Ender, …, Ivers-Tiffée, *JES* 159 (2012) A952**(ref 29 — 제목이 곧 우리 물음: "**Separation of charge transfer and contact resistance**"; 18호는 DRT 참고문헌으로만 쓴다) · ★★★ 3 **Koerver, …, Janek, *Chem. Mater.* 29 (2017) 5574**(ref 23 — **큐 22번과 같은 편**, 순서만 당기면 된다) · ★★ 4 **Ruess, …, Janek, *JES* 167 (2022) 100532**(ref 19 — `R4` 귀속의 원전, 입자 균열이 액체/고체에서 다르게 보이는가) · ★★ 5 **Schönleber, Klotz, Ivers-Tiffée, *Electrochim. Acta* 131 (2014) 20**(ref 30 — **Lin-KK 원전**, D7 을 푸는 유일한 길이자 DRT 체크리스트 **C2 의 정본**) · ★ 6 **Deng, …, Ong, *JES* 163 (2016) A67**(ref 42 — Young 계수 22.1/30 의 출처, G11).
- lint: **0 errors**.

## [2026-09-22] ingest | `assb` 19호 — Yoshida 2024 전고체 **4전극** 셀 (황화물 SE|SE 계면): 기준 전위를 **소거**하는 설계 · 상대극이 관심 대역을 통째로 덮는다 · 곱 축퇴 처방 세 번째 적용
- 큐 **18번**. `raw/papers/yoshida2024_four-electrode-assb-cell-li-transport.md` (sha256 봉인; `pdf_sha256 a991f5351cb61a20…` · `si_sha256 774a121241a8d2dc…` 실측 일치). Yoshida, Ikezawa, Okajima, Arai, *Electrochim. Acta* **497** (2024) 144523, **CC BY**. 본문 9쪽 + SI 9쪽. 닻은 `questions/assb-contact-loss-vs-lampe.md`.
- **크로핑 17장 중 그림 9장을 직접 봤다** — Fig. 1/2/3/4/5/6/7/8 + Fig. S1 + Fig. S4 + Fig. S6, 그리고 **캡션이 "Figure S 5" 로 띄어져 크로퍼가 놓친 Fig. S5 를 SI p.6 직접 렌더로 열람**(18호의 Graphical Abstract 누락과 같은 유형). Table 2 는 **지수 부호 오타 확인을 위해 크롭도 직접 봤다**. 안 본 것: Fig. S2(전도도 셀 도식) · S3(XRD) · S7 · S8. 누락은 `get_images()`/`get_drawings()` 페이지별 계수로 기계 확인.
- ★ **18호와 같은 연구실의 같은 계보**다 (Ikezawa·Okajima·Arai 겹침; 감사문이 **18호 제1저자 Goro Fukunishi** 에게 기술 자문을 사례). 그리고 **큐가 확인하라던 Ikezawa 2020 (*Electrochem. Commun.* 116, 106743)이 여기서도 인용된다 — ref [18]**. 18호는 ref [20], 새로 보이는 자매편(**흑연 복합전극 3전극 + cyclability**, *ACS Appl. Energy Mater.* 6 (2023) 10908)은 ref [19].
- ⚠ **먼저 경계**: 이 편에는 **전극이 없다** — 활물질·용량·사이클 0, `degrad*`·`capacity`·`OCV`·`GITT` 전수 0회. 잰 것은 **황화물 SE 펠릿 두 장을 포개 만든 계면 하나의 Li⁺ 수송 저항**뿐이다. Q1·Q2·Q3(라벨)·Q7·Q8 에 구조적으로 기여할 수 없다.
- ★★★★ **Q5 — 계보 다섯 번째 형태: 재지도 가정하지도 않고 소거한다.** 4전극의 측정량이 `[인쇄]` **RE₂ − RE₁** 이라 R-LTO 의 절대 전위가 상쇄된다 ⇒ `assum*` **0회**, "**1.55**" **0회**(18호의 "Assuming 1.55 V" 공백이 생기지 않는다). **대신 새 바닥이 인쇄된다**: RE–RE 개방회로 **−4 / −5 / +25 mV**, `[인쇄]` "within the **reproducibility of the reference electrode potentials (ca. ±30 mV)**" = **계보 최초의 기준극 재현성 숫자이자 검출 하한**(⚠ **근거 미제시**). ★ **R-LTO 조성도 처음 인쇄**: **Li₇Ti₅O₁₂ : Li₄Ti₅O₁₂ = 67 : 33 mol%**(2상 한복판) ⇒ 18호의 "partially reduced" 공백 절반 해소.
- ★★★★ **큐 메모("상대극 전위 변화가 선형이 아니다")의 출처를 확정했다 — 메모는 맞다.** §3.2 마지막 문단, `[인쇄]` "The potential change in the counter electrode is **not linear**, and the voltammogram of the counter electrode is **asymmetric**, especially in the case of the LGPS | LPSCl cell." 근거 그림은 **Fig. S4**. `[도표]` 200 s·≤0.7 mA CV 한 번에 `E_CE` 가 **42 / 126 / 75 mV** 움직이고(극값이 CV 반전보다 **27 초 앞선다**), `[재현]` `ΔE/ΔI` = **44 / 221 / 83 Ω = 같은 셀 계면 저항(21.5 / 12 / 29.3 Ω)의 2–18 배** ⇒ **"4전극이 3전극보다 무엇을 더 재는가" 의 정량 답**. `[재현]` 이것은 **가역 분극**이다(통과 전하가 Li 재고의 0.39 %, 200 s 뒤 복귀).
- ★★★★ **Q5 경계 조건에서 (ㄷ)만 깬 첫 표본**: (ㄱ) `x_Li` **25 at%**(17·18호와 다른 세 번째 조성) ✅ · (ㄴ) 재고 여유 **≈260 배** ✅✅ · (ㄷ) **0.41–1.07 mA cm⁻²** ❌ ⇒ 관측 이동 **42–126 mV**. `[해석]` **재고 여유가 충분하면 전류밀도를 20 배 올려도 이동은 10⁻¹ V 에 못 미친다 — 17호의 0.7 V 는 고갈의 산물이다.** ⚠ 네 편을 가로지르는 추론이고 통제 실험이 아니다.
- ★★★★ **Q2 — 비분리를 자기 데이터로 증명한 첫 편.** `[인쇄]` Li-In 전극 반원이 **P1(>1 kHz)·P2(1 kHz–0.1 Hz) 둘 다와 겹쳐** "**P1 and P2 are difficult to extract** from the impedance measured with the two-electrode system". `[도표]` 같은 공칭 Li-In 박의 전극 저항 **39 / 172 / 54 Ω = 4.4 배 (n=3)**. ⇒ **10·11·16·18호 계보의 다섯 번째이자 가장 아래 층 — 양극을 바꿔도 음극은 거기 있다.** 해법이 알고리즘이 아니라 **배선**이다.
- ★★★★ **곱 축퇴 처방의 세 번째 적용 = 부분 적용 + 전제 반증 + 대체 채널 획득.** 입력은 **처음으로 완비**(Table 2 가 `R`·`Q`·`p`·`C`·`τ` 전수, `C` 는 저자가 Brug 식으로 계산 — `[재현]` 검산 일치)이고 면적 조작도 셋(압력 2점·단면적 3점·계면 유무 대조)인데: **검사 A** `[재현]` `P2` 의 `C` 가 기하 면적 기준 **2.0–4.8 mF cm⁻² = 이중층(10 µF cm⁻²)의 200–480 배** ⇒ **물리 상한 2–3 자릿수 초과, 전제 `C ∝ θ` 두 번째 반증**(18호는 "2–3 배 빗나감"이었다). **검사 B** `[재현]` `τ₂` 가 36–46 ms(±13 %) 로 "면적만 다르다"(2.4 배)를 말하는데 `Ea(R₂)` 는 **27 / 41 / 42 kJ mol⁻¹** 이라 전지수 인자 **158–174 배** 보상이 필요하다 ⇒ **두 채널이 70 배 충돌**(⚠ 세 계면은 물리적으로 다른 계면이라 18호 검사 B 와 성질이 다르다). **검사 C** 압력 축에 `C` 가 인쇄되지 않았다 — **18호와 정반대의 결손**.
- ★★★★ **대신 얻은 것 — 면적-불변 채널 `Ea`.** `[도표]` 560→840 kPa 에서 `R₁` −6.5 % · `R₂` **−26 %** 인데 `[인쇄]` "the **physical state of the interface does not affect the Ea** but the resistance values … **Ea as the essential parameter**". ⇒ `R(T) = A(θ)·exp(Ea/RT)` 에서 **`Ea` 는 `θ` 와 직교**하고 **`C_dl ∝ θ` 전제를 쓰지 않는다**. ★ **18호가 `Ea(노화 전후)` 를 쟀다면 검사 B 가 `C` 없이 독립 확인됐을 것이다** — 처방에 줄로 등록. ⚠ 충분조건은 아니고(검사 B 가 반례), 근거도 **2점·n=1·범위 1.5 배**다.
- ★★★★ **산포 하한**: `[도표]` LPSCl|LPSCl 셀의 `Ea(R₁)` = **45.5 ± 0.1** kJ mol⁻¹ ↔ 같은 물질 Table 1 벌크 **40.5 ± 0.3** (`R₁` 은 정의상 벌크뿐) ⇒ **5.0 kJ mol⁻¹ = 인쇄된 ± 의 12–50 배, 논문 무언급**. `[인쇄]` 저자 스스로 **성형법(냉간↔열간)이 `Ea` 를 11 kJ mol⁻¹ 움직인다**고 적는다. 다른 둘: **Li-In 임피던스 4.4 배** · `P3` **7 배**(4.8 Ω ↔ `[도표]` ≈35 Ω).
- ⚠⚠ **중심 배정(P2 = 계면)이 4점·이상치 1개에 걸려 있다.** 단면적 `S` 축은 **벌크도 계면도 `1/S` 로 스케일**해 판별력이 없고(논문도 `[인쇄]` "pellets **or** at the interface"), 결정적인 `d` 축의 `[도표]` `R₂/d` = **17.0 / 3.3 / 3.0 / 3.2 Ω mm⁻¹** — **이상치를 빼면 `R₁`(1.12×)만큼 깨끗이 `d` 에 비례(1.10×)해 결론이 뒤집힌다**. ★ 다만 같은 지면의 **Fig. 7(계면 유무 대조: LPSCl 펠릿 1장엔 `P2` 없음 → 2장 적층엔 `P2` 생김, `[도표]` ≈8 Ω)** 이 훨씬 강하게 지지하는데 **"consistent with" 로 뒤에 놓인다 — 논증 순서가 거꾸로다.** 우리에게는 그 대조군이 **접촉을 아는 대조군의 교과서적 형태**다.
- **Q6**: 운전 **ca. 420 / 560 / 840 kPa = 계보 최저 대역**이고 **8호가 인쇄한 산업 요구치 <≈1 MPa 안에 들어온 첫 편**(16호 97/389 · 17호 50 · 18호 미보고 MPa). ⚠ 2점·n=1·범위 1.5 배, `[재현]` **420 kPa 의 `R₂`(21.5 Ω)가 560 kPa(≈24.7 Ω)보다 작아 추세와 반대**.
- ⚠ **`θ` 는 또 0 — 19/19.** `contact area` 2회가 전부이고 압력 효과의 설명(`[인쇄]` "possibly due to the **increases in the contact areas**")에 **값이 없다**. `R(P)` 는 있고 `θ(P)` 는 없다.
- **어긋남 16건**: **D10** `Ea` 자기 불일치(45.5 ↔ 40.5) · **D5** 율결정 단계 지표가 본문 "(ii)" ↔ Fig. 6 은 "Slow" 를 **(iii) 위치**에 그린다 · **D6** `R₂`–`d` 이상치 · **D9** LGPS|LPSCl 의 **CV 기울기 ≈114 Ω ↔ Nyquist 총합 183 Ω (1.6 배)**, 다른 두 셀은 5 % 안 · **D3** Table 2 특성 주파수 **세 칸의 지수 부호 오타**(2.4×10⁻⁷ Hz = 48일에 한 주기), 정정하면 **`P1` 꼭짓점이 측정 상한 7 MHz 밖** ⇒ `R₁` 은 외삽값(한 셀은 원호의 26 %만 측정) · **D1** Fig. S5 패널 배정이 본문 ↔ SI 캡션에서 다르다 · **D14** "RE artifact 아님" 의 근거가 **진폭 비의존성**(18호의 K–K 잔차와 **같은 구조의 범주 오류**).
- 컴파일: 닻 채움표 **19호 행 + 새 절(10 항) + Evidence 열여섯 번째 + Against 2항 + Status Log** · [[assb-li-in-reference-potential-window]] (**4전극 층 + 처방 P8·P9**) · [[assb-lampe-contact-product-degeneracy]] (**처방 세 번째 적용 + `Ea` 채널 줄 신설**) · [[drt-peak-count-nonidentifiability]] (**다섯 번째 경보**). `index.md` 닻 항목 갱신. **채움표 누적 ≈10.5 → ≈11.0 (Q5 +0.5)**, **Q4 0/19**.
- 후속 후보: ★★★★ 1 **Ikezawa, Fukunishi, …, Arai, *Electrochem. Commun.* 116 (2020) 106743** (ref 18 — **세 번째 지목**; 16·17·18·19호 **네 편**이 가리키고 **±30 mV 와 1.55 V 의 근거가 둘 다 거기 있어야 한다**) · ★★★ 2 **Fukunishi, Ikezawa, …, Arai, *ACS Appl. Energy Mater.* 6 (2023) 10908** (ref 19 — **흑연 복합전극 3전극 + cyclability**, `θ(N)`·`Ea(N)` 가 있을 가능성이 계보 최고) · ★★★ 3 **Abe, Sagane, Ohtsuka, Iriyama, Ogumi, *JES* 152 (2005) A2151** (ref 14 — `Ea` 로 율결정 단계를 정한 **논증 틀의 원전**) · ★★ 4 **Brug 1984** (ref 27 — 식 (1)의 원전, `p` = 0.55–0.61 에서 유효 용량이 물리 용량인가) · ★★ 5 **Lewis, …, McDowell, *Nat. Mater.* 20 (2021) 503** (ref 8 — operando 토모로 void↔interphase, 5호의 형제) · ★ 6 **Rosenbach 2022** (ref 21) · ★ 7 **Shi/Ceder 2020** (ref 4, **큐 21번 계열**). ⚠ **1–6 은 큐에 없다.**
- lint: **0 errors · 0 warnings** (45 pages, 48 raw).

## [2026-09-22] ingest | `assb` 20호 — Chang, Choi, Kang, Park, Lim 2020, Characterization of limiting factors of an all-solid-state Li-ion battery using an embedded indium reference electrode (*Ionics* 26, 1555–1561, Short Communication 7쪽, SI 없음) 실험 + 3전극 매립 In

- `raw/papers/chang2020_embedded-in-reference-electrode-assb-limiting-factors.md` (sha256 봉인). 큐 **19번**. 창원대 + **RIST** + 세종대. 그림 4 + 표 1 이 전부이고 **전부 직접 봤다** — 크로퍼는 2장만 잡았다(Fig. 1–3 캡션이 `Fig. 1 a A schematic…` 이라 구두점 규칙 탈락) ⇒ p.2·p.3 전면 렌더 + 400–600 dpi 수동 크롭 3장 보관. **안 본 그림 0장.**
- ★★★★ **계보 판정 — Ikezawa 2020 을 가리키지 않고 가리킬 수 없다** (접수 2019-08-06 · 게재 2019-12-23). 16·17·18·19호가 전부 가리킨 그 논문의 **다섯 번째가 아니라 그 앞**이다. 대신 **ref [10] Nam 2018 *JMCA*** 와 **ref [19] Santhosha 2019** 를 가리키는데 **둘 다 17호가 이미 지목한 후속 후보**다 ⇒ **Q5 계보가 둘이다**: R-LTO 가지(4편 → Ikezawa 2020) / **In 가지(17·20호 → Nam·Santhosha)**.
- ★★★★ **17호 함정("겉보기 `LAM_PE` 가 사실은 상대극")을 5년 먼저, 명시적으로 피했다.** 첫 충전 **122 mAh g⁻¹(54 %)** 손실을 3전극이 **음극**에 배정하고 `[인쇄]` "the cause of the capacity fade … **could not have been elucidated without the three-electrode setup**". `[도표]` **1·2차 충전이 둘 다 음극 전위 ≈0.019 / 0.043 V vs Li/Li⁺ 에서 끝나고 양극은 2.40 V**(신품 2.52–2.58) ⇒ 충전을 끊는 것은 음극이다 — **저자가 안 적은 수치**. ⚠ 반대로 `[재현]` **저자 논거(음극 저항 증가 275 Ω = 55 mV)는 격차의 12 %(≈15 mAh g⁻¹)만 설명한다** ⇒ **결론은 옳고 논거는 다른 데 있다**.
- ★★★★ **Q5 — 다섯 번째 형태: 가정하되 가정이 깨지는 모습을 남겼다.** `assum*` **0회** · `0.62` **2회** — ★ **가정이 문장이 아니라 그림의 두 번째 축("V vs. Li/Li⁺" = 왼쪽 + 0.62 V)으로 인쇄되기 때문**이고 **낱말 지문으로는 안 잡힌다**. `[재현]` Fig. 2a 디지타이즈(인쇄값과 2–5 mV 일치로 보정 검증): **비리튬화 In 에서 `V₁ = V₂−V₃` 가 159 mV 깨지고 리튬화 뒤 5 mV 로 닫힌다** ⇒ **신품 In 부유 전위 1.77–1.93 V = 짝(0.62)보다 1.15–1.31 V 높다**(16호의 "설치·미검증" 위험의 크기) ⇒ **정정된 명제: 이 검사는 기준극의 *접촉*을 보지 *전위*를 보지 않는다**. 범주 오류 **세 번째**(18호 K–K · 19호 진폭 비의존 · 20호 키르히호프 항등식) — **단 유일하게 판별력 ≠ 0**, 그리고 같은 논문 안에서 **두 번** 쓰인다(Table 1 의 "Cathode R + Anode R ≈ Cell R" 도 같은 항등식의 시간 미분).
- ★★★★ **새 축 — 기준극의 재고 예산, 그리고 3전극의 원리적 사각.** `[재현]` 리튬화 20 µA×1 h = 0.020 mAh ⇒ **x̄ = 0.0053**, 셀 용량 대비 **1/675**; 190 h 실험에서 재고 90 % 유지에 **누설 < 10 nA** 필요. 그리고 **기준극 표류는 `V₂`·`V₃` 에 공통 모드로 들어가 `V₁` 에서 상쇄되므로 3전극은 자기 표류를 원리적으로 못 본다** ⇒ **19호 차분 설계의 물리적 근거가 20호 데이터 안에 있다.** **20/20 편이 누설을 안 쟀다.** ⚠ `[도표]` XRD 가 동정한 상은 **In₁.₇Li₀.₃ = Li₀.₁₈In**(본문은 "Li-In")이라 0.62 V 의 근거인 In/LiIn 2상과 같지 않다 — `[재현]` 전하 수지와 맞추면 리튬화가 **≈3.3 µm 표면층**에 갇힌 **구배 전극**이다.
- ★★★★ **곱 축퇴 처방 — 1·2단계 적용 불가, 3단계를 시간 영역으로 번역하면 적용되고 즉시 실패한다.** `equivalent circuit`·`capacitance`·`C_dl`·`Ea`·`fit*`·본문 `impedance` **전수 0회**(주파수 영역이 통째로 없다). 그러나 펄스 분해의 **비선형 구간 지속 = 시상수**이므로 `[재현]` τ ≈ 10³ s ⇒ **`C = τ/R_ct` ≈ 1 F cm⁻² = 이중층 상한의 10²–10³ 배**(19호 200–480 배) ⇒ **`R_ct` 라 부른 성분은 전하이동이 아니다.** ⇒ **처방 4단계 신설**: "시간 영역 분해에도 같은 상한 검사를 건다."
- ★★★ **음극 판 곱 축퇴 — 방정식 없이, 진단 → 처방 사이에서.** 진단은 **동역학**(`[인쇄]` "sluggish alloying")인데 처방은 **면적**(`[인쇄]` "for **larger interface areas**"). `[재현]` 음극은 **8.4배 과잉**이고 DOD 11.2 % 인데 그 구간에서 음극 전위가 0.29 V 움직여 충전을 끊는다 ⇒ **(a) 극심한 분극** ↔ **(b) 접근 가능 분율 ≈1/9 이하**를 `R₀`·`R_ct`·`R_p` 로 가를 수 없다.
- ★★★ **`i → 0` 처방의 반례.** `[재현]` 면적용량 **9.3 mAh cm⁻²**, 200 µA = **C/72** — 극저율에서도 54 % 가 날아간다. 그리고 `[재현]` **1일 휴지 뒤 `V₁` = 2.095 V 로 컷오프(2.4 V)보다 310 mV 아래** ⇒ **손실의 일부는 CC 전용 프로토콜의 산물**이다.
- ⚠⚠⚠ **설계에 2요인 교락**: `[재현]` 방전 펄스는 **t=2.35 h(양극 x≈0.03, 음극 Li-rich 끝)**, 충전 펄스는 **t=70 h(양극 x≈0.95, 음극 Li-poor 끝)** ⇒ **방향 ⊗ 조성 완전 교락**, 셀 1개 ⇒ `[인쇄]` "탈합금화가 합금화보다 빠르다" 는 **이 설계로 분리되지 않는다**. ⚠ 그리고 `[재현]` **"접촉 저항 362 Ω"** 은 `R₀ − L/(σA)` 의 잔차인데 **복합전극 내부 이온 경로만으로 ≈350 Ω**(ε=0.4·τ=2 가정)이 나와 **이름표가 데이터에 요구되지 않는다**.
- **채움표 20호 행 — 누적 ≈11.0 → ≈12.5** (**Q2 +0.5** 계보 최초의 전극별 용량 손실 귀속 · **Q5 +0.5** · **Q8 +0.5** 새 화학 **TiS₂** + 두 전극 전위 궤적 동시 인쇄). **안 움직인 칸: Q1 0/20 · Q4 0/20 · Q6 0**(`pressure`·`MPa`·`kPa` 전수 0회 = **두 번째 완전 미보고**). **Q4 열세 번째 성질 = "분해가 적합조차 아니다 — 작도다"**(`fit*` 0회, 잔차·공분산 없음, `[재현]` 음극 `R_p` 12 mV = 패널 y 전폭의 **1.2 %** 에서 판독, 오차 표기 0).
- 컴파일: **새 개념 0**. 갱신 — 닻 [[assb-contact-loss-vs-lampe]] (채움표 20호 행 + Evidence For **열일곱 번째** + 새 제약 6개 + Status Log) · [[assb-lampe-contact-product-degeneracy]] (**처방 네 번째 적용 + 4단계 신설 + 음극 판**) · [[assb-li-in-reference-potential-window]] (**다섯 번째 형태** + 조건 (5′)(누설 분모)·(7)(프로브 리튬화) + 처방 **P10**).
- 후속 후보: ★★★★ 1 **Nam, Park, Oh, An, Jung 2018, *J. Mater. Chem. A* 6, 14867** (17호·20호 **동시 지목**, 제목이 곧 failure modes) · ★★★★ 2 **Santhosha, Medenbach, Buchheim, Adelhelm 2019, *Batteries & Supercaps* 2** (**0.62 V 의 출생지**, 두 번째 지목) · ★★★ 3 **Jin, Park, Park, Lim 2015, *Electrochim. Acta* 185, 242** (이 편의 셀 원전 — 공백 G1·G2·G3) · ★★ 4 **Barai, Uddin, Widanage, McGordon, Jennings 2018, *Sci. Rep.* 8, 21** (`R₀`/`R_ct`/`R_p` 작도법 원전, 제목이 **measurement timescale**). ⚠ **1–4 전부 큐에 없다.**
- lint: **0 errors · 0 warnings**.

## [2026-09-23] ingest | `assb` 21호 — Sedlmeier, Schuster, Schramm, Gasteiger 2023, A Micro-Reference Electrode for Electrode-Resolved Impedance and Potential Measurements in All-Solid-State Battery Pouch Cells and Its Application to the Study of Indium-Lithium Anodes (*J. Electrochem. Soc.* 170, 030536, CC BY, 13쪽, SI 없음) 실험 + 미세 기준극 3전극 파우치

- `raw/papers/sedlmeier2023_micro-reference-electrode-assb-pouch-inli-anode.md` (sha256 봉인). 큐 **20번**. TUM Gasteiger. 크로퍼가 본문 그림 **9장**을 잡고 **부록 Fig. A·1 을 놓쳐** p.12 를 400 dpi 수동 크롭(`fig_A1_manual_p12.png`, `figures.json` 에 `manual` 등록) ⇒ **10장 전부 직접 봤다 — 안 본 그림 0장**(Fig. 7b 는 확대 재확인).
- ★★★★ **계보의 자리**: **17호가 지목한 후속(ref 21)이자 개념 페이지 처방 P4(Li 박 방향 뒤집기) 의 통제 실험.** 그리고 **두 Q5 가지의 뿌리를 함께 인용하는 첫 편** — Ikezawa 2020(ref 18, **다섯 번째 지목**) · Nam 2018(ref 13, 세 번째) · Santhosha 2019(ref 28, 세 번째) · 20호 Chang 2020(ref 12) · 큐 22번 Koerver 2017(ref 29). 자기 기준극은 **리튬화 금선(LixAu 0.31 V)** — 재료로는 **Au 가지(16·21호)**.
- ★★★★ **"0.62 V ✓ ≠ 재고 ✓"**: 같은 InLi 박(≈24 at%, 공칭 ≈14 mAh cm⁻²)을 방향만 바꿔 n = 3 씩 — InLi-(In)(Li 박 뒷면 = 17호 foil) 은 28 일 **0.62 V(< 3 mV)** 인데 0.2 mA cm⁻² 에서 **9 초 · 0.39 ± 0.21 µAh cm⁻²**, InLi-(Li) 는 **15 h · 3.0 mAh cm⁻²**. 순수 In(= 16호)은 전기화학 리튬화 뒤 임피던스가 Li 쪽 부류로. ⇒ **16↔17호 대질 가설 지지**(한 변수만 바꾼 첫 데이터). 이 카드 물음의 **음극 판 실측**(OCV 는 "있음 ↔ 접근 가능" 을 못 가른다) = Evidence For **열여덟 번째**.
- ★★★★ `[인쇄]` **"cannot be assumed to stay invariant at 0.62 V"** (NCM|In 방전 끝, `LLI` 의존) — 17호 함정의 **원인 쪽(`LLI` → 상대극 → 끝 절단)** 이 17호보다 앞서 문장으로.
- ★★★ **Q5 여섯 번째 형태 = 교정 이식**: GWRE 0.31 V 를 Li|Li 교정 셀(3 MPa, 2 h)에서 재고 InLi 셀(20 MPa)로 옮긴다. `assum*` 4 회(기준 전위엔 **0**) · `0.62` 18 · `0.31` 7 — 가정이 **"calculated based on"** 으로 · Fig. 4 두 번째 축으로 · Fig. 6·8 은 환산 축만으로. ★★ **Fig. A·1 은 축 이름("vs. InLi-(Li) CE")과 숫자(+0.31 V)가 정확히 0.62 V 어긋난다** ⇒ 유력한 읽기면 **순환이 두 그림에**(A·1 은 InLi = 0.62 가정 → GWRE 0.31, Fig. 4 는 반대).
- ★★★ **기준극 표류 < 3 mV / 28 일** — 두 전극이 2상 평탄에 고정돼 공통 모드가 보인다 ⇒ 20호 "3전극은 자기 표류를 못 본다" → **"고정 전극이 없으면"**. `[재현]` 재고 3 µAh(셀의 1/4,000–1/21,000)로 ≈703 h ⇒ **누설 < ≈4.3 nA**(간접; 직접 측정 **21/21 편 0**).
- ★★★ **③ 국소 고갈이 둘로**: ③-a 뒤에 재고(InLi-(In)) → **≈0.1 h 안에 0.62 V 복귀**(농도 과전압) · ③-b 재고 없음(탈리튬 순수 In) → **≈0.96 V 잔류**. **(5) 재고비 가설 약화** — InLi-(Li) 는 재고비 4.2–5.2(17호 foil ≈5)로 평탄 ⇒ 17호를 깬 것은 (2).
- ★★★ **곱 축퇴 처방 다섯 번째 적용**: 1단계 **τ 형**(꼭짓점 주파수) — Li|Li 쌍 **면적 서명 통과**, InLi 쌍 **정렬 어긋남 기각**(`[재현]` C 비 ≳1.4 ↔ 0.28); 3단계-b **저주파 "전하이동" 호 C ≈0.50 / ≳0.64 mF cm⁻² = 이중층 비용량 10 µF cm⁻² 의 ≈50–64 배**(세 번째 실패) — ⚠ 페이지의 **두 기준값(10 µF ↔ 10⁻² F)이 10³ 배 다른 부채**를 정리(관대한 기준으로는 통과); 4단계 **"이중층 충전" 10²–10³ 배 실패**; AC = DC 3–6 % 일치는 **값이지 배정이 아니다**.
- ⚠⚠ `[재현]` **저자의 D ≥ 4.4×10⁻⁸ cm² s⁻¹ 와 1 at% 고용체는 9 초와 양립하지 않는다** — Sand ≈54 분 · ≈181 µAh cm⁻²(≈360–465 배), OCV(< 3 mV)가 c 를 1 at% 근처로 묶으므로 **틀린 쪽은 D**. ⚠ `[재현]` "과전압" 375 / 750 Ω cm² 중 **≈245 Ω cm²(33–65 %) 가 분리막 절반**. 어긋남 **14 건**(D1 순수 In **38 ± 0.8 → ±10** · D2 A·1 · D5 압착 60 ↔ 70 MPa · D14 "Warburg ⇒ 전하이동 없음").
- **채움표 21호 행 — 누적 ≈12.5 → ≈13.5** (**Q2 +0.5** "있음 ↔ 접근 가능" 을 독립 관측 둘로, 반 칸 = 음극 재고·제조 상태 · **Q5 +0.5**). **안 움직인 칸: Q1 0/21**(접촉을 이름 붙여 SEI 와 한 반원에 합치고 압력 가설로 넘겼다) · **Q4 0/21**(열네 번째 성질 = **"값의 정확도를 검사하고 배정의 유일성으로 읽었다"**) · **Q6 칸 이동 없음**(보고·통제, 스윕 0) · **Q7·Q8 해당 없음**. Q3 은 층 하나(계보 최초 동일 조건 셀 간 ± n = 3).
- 컴파일: **새 개념 0**. 갱신 — 닻 [[assb-contact-loss-vs-lampe]] (채움표 21호 행 + 누적 줄(20편 줄 보충) + Evidence For **열여덟 번째** + 새 제약 5개 + Status Log + 주장하지 않는 것) · [[assb-li-in-reference-potential-window]] (21호 절 · ③-a/③-b · 조건 (8) + (5) 약화 · **P4 ✅** · **P11·P12** 신설 · 16↔17호 대질 판정) · [[assb-lampe-contact-product-degeneracy]] (**다섯 번째 적용** + 기준값 정리). `index.md` 세 항목 갱신.
- 후속 후보: ★★★★ 1 **Ikezawa 2020 *Electrochem. Commun.* 116, 106743** (다섯 번째 지목 — 21호가 InLi-(In) 조립의 예로도 인용) · ★★★★ 2 **Nam 2018 *JMCA* 6, 14867** (세 번째 — 탈리튬 후 계면 고갈의 원전) · ★★★ 3 **Santhosha 2019 *Batteries & Supercaps* 2, 524** (세 번째) · ★★★ 4 **Solchenbach 2016 *JES* 163, A2265** (GWRE · 0.31 V 원전) — **넷 다 큐에 없다.**
- lint: **0 errors · 0 warnings**.


## [2026-09-23] ingest | `assb` 22호 — Strauss, Bartsch, de Biasi, Kim, Janek, Hartmann, Brezesinski 2018, Impact of Cathode Material Particle Size on the Capacity of Bulk-Type All-Solid-State Batteries (*ACS Energy Lett.* 3, 992−996)

- `raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md` (sha256 봉인). 큐 **21번**. KIT BELLA + JLU Giessen + BASF — **1호(Bielefeld 2019)의 ref 13**. 크로퍼가 본문 그림 4 + SI 그림 7 + SI 표 1 을 전부 잡았고 **그림 11장 전부 직접 봤다 — 안 본 것 0장**(표 S1 은 텍스트).
- ★★★★ **Q1 이 `θ` 축에서 처음 움직였다**: ex situ XRD 2상 Rietveld 의 불활성 CAM 분율 **2 / 27 / 31 %**(d₅₀ 4.0 / 8.3 / 15.6 µm)는 **회절 상 분율의 측정**이고 용량은 독립 대조(±7 %)로만 쓰인다 ⇒ **역산이 아니다.** 그러나 등호도 아니다 — `1 − θ_AM` 의 **합집합 상한** · `[재현]` Cu Kα 반사 정보 깊이 ≈3–15 µm = **집전체 면 표층** · 신품 C/10 한 점 · n 미기재.
- ★★★ **3항 분해의 첫 실측 분리**: `[재현]` NCM-L θ ≈0.69 · η ≈0.69 — 결손의 절반은 활성 입자의 덜 충전. 불활성 상 격자 = pristine ⇒ `Q_material` 그대로.
- ★★★★ **1호 대질**: 인용 네 가지는 원문과 맞다(`poros*` 0 회). 그러나 `[재현]` **무공극 상한에서 1호 식 (8) 은 불활성 ≈23–40 / ≈95 / ≈95–97 % 를 예측** — 측정 2 / 27 / 31 %, 용량만의 상한 ≤3 / ≤39 / ≤44 % ⇒ "correlate well" 은 순위만 맞다.
- ⚠⚠ **원인 배정("lack of electronic contact")은 병치**: `[도표]` σ_e/σ_ion ≈550 / ≈50 / ≈1.5, 불활성 M ≈ L; Fig. 4 두 y 축 자릿수 간격 불일치로 L 의 σ_e ≥ σ_ion 이 반대로 보인다.
- ★★★ **곱 축퇴 처방 여섯 번째 적용**: 1·3단계 ❌ · 2단계 ⚠ · 4단계 ✅(DC 분극 과도 C ≈0.4–0.8 F cm⁻² = 화학량 분극 ⇒ σ_ion 상한). **처방 표에 새 줄 "SOC 추종 상 분율"** — `θ·ε_p` 를 뗀다, `A_eff·j₀` 는 남는다.
- **17호 함정**: 주 주장(XRD)은 설계상 면제(양극을 전위 없이 읽은 첫 편), 용량·CE 축은 노출. **Q5 일곱 번째 형태** = "가정이 대조군 전압창을 정한다"(0.6 V, `[도표]` ±30 mV 정합).
- **Q4 0/22** — 열다섯 번째 성질 "측정이 분할을 대신했고 원인은 병치됐다" + c(x) 가지 선택을 밟고 지나감.
- **채움표 22호 행 — 누적 ≈13.5 → ≈14.5** (**Q1 +0.5 · Q2 +0.5**). 안 움직인 칸: Q4 · Q5 · Q6 · Q8(칸 이동 없음) · Q7(해당 없음). Q3 층 하나(방법 오차 예산을 인쇄한 첫 편).
- 컴파일: **새 개념 0**. 갱신 — 닻 [[assb-contact-loss-vs-lampe]] (채움표 22호 행 + 누적 줄 + Against 새 첫 항목 + 새 제약 5개 + Status Log + 주장하지 않는 것) · [[composite-cathode-percolation-utilization]] (measured 라벨 + 1호 식 (8) 대질) · [[assb-apparent-capacity-decomposition]] (θ·η 첫 실측 분리) · [[assb-lampe-contact-product-degeneracy]] (여섯 번째 적용 + 처방 표 새 줄).
- 후속 후보: ★★★★ 1 **Koerver 2017 *Chem. Mater.* 29, 5574** (큐 22, 이 편 ref 9, 본문 4 회) · ★★★ 2 **Zhang 2017 *JMCA* 5, 9929** (ref 18, 셀 장치·부피 수축→접촉 감소) · ★★★ 3 **Zhang 2017 *ACS AMI* 9, 17835** (ref 16, 같은 연구망 복합체 토모그래피 — 공극률 후보) · ★★ 4 **Nam, Oh, Jung, Jung 2018 *JPS* 375, 93** (ref 17, 건식/슬러리 혼합 — 원장의 Nam 2018 *JMCA* 와 다른 논문).

## [2026-09-23] ingest | `assb` 23호 — Koerver, Aygün, Leichtweiß, Dietrich, Zhang, Binder, Hartmann, Zeier, Janek 2017, Capacity Fade in Solid-State Batteries: Interphase Formation and Chemomechanical Processes in Nickel-Rich Layered Oxide Cathodes and Lithium Thiophosphate Solid Electrolytes (*Chem. Mater.* 29, 5574−5582) + SI

- `raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md` (sha256 봉인). 큐 **22번**. JLU Giessen + KIT BELLA + BASF — **1호 ref 7 · 22호 ref 9 · 21호 ref 29 · 18호 [23] · 9호 [17]**. 크로퍼가 본문 그림 6 + SI 그림 8 을 전부 잡았고 **14장 전부 직접 봤다 — 안 본 것 0장** (+ Fig. 6 원본 SEM 픽셀 계측).
- ★★★★ **원전은 계면층 ↔ 접촉 손실을 가르지 않는다** — XPS ↔ SEM 채널 분담으로 **존재**만 보이고 몫은 시간 분할(첫 사이클 "combination" · 이후 CEI 소거법)로 배정; 초록 ↔ 결론이 `ΔR` 을 다르게 배정.
- ★★★★ **SI 가 가른다(우리 조합)**: `R_SE/Cathode` ×1.5–2.45 동안 `C_SE/Cathode` ×0.96–1.05 (면적 가설 ×0.41–0.66) — 두 셀(In · LTO) 다섯 구간 ⇒ `R` 증가분은 **화학 형**. S3 무전류 이완이 전제 `C ∝ 면적` 의 부분 양성 대조(한 호 `R·C` +5 %).
- ★★★ `[재현]` **손실 예산**: 계면층 패러데이 ≈4 % + 옴 ≲3 % ⇒ 첫 사이클 손실 52 mAh g⁻¹ 의 **≳85 % 미배정**(`θ` · `η(i)` · 상대극).
- ★★★★ **17호 함정 노출 + 대조군 공유**: 두 상대극 모두 무 Li 조립, 방전 끝 `C_anode` ≈90–100 배 붕괴(평탄 이탈 서명), 재고비 ≈1.4. **Q5 여덟 번째 형태** = "가정 명시 + 깨지는 곳을 '활성화'·'음극 동역학' 으로 덮음"; 1.55 V(LTO) 가정이 18호보다 6 년 이르다.
- ★★★ **인용 대질**: 숫자 오기 0. 22호 ref 9 네 문장 · 21호 ref 29 두 문장은 원문과 맞다. **18호 [23] "space charge layer" — 원전에 0 회(기구 치환)** · 1호 "throughout"(강도 과장) · 1호 탄소 분해(원전은 회피) · 9호 초록 채택.
- **채움표 23호 행 — 누적 ≈14.5 → ≈15.0** (**Q2 +0.5**). 안 움직인 칸: Q1(이름표 + 정성, `θ(N)` 측정량 0/23 — 대리량 N = 1→2 불변이 첫 입력) · Q4 0/23(열여섯 번째 성질 "채널 분담 + 시간 분할 배정") · Q5 · Q6 · Q8 · Q7(해당 없음). Q3 층 하나.
- 컴파일: **새 개념 [[assb-interphase-vs-contact-loss-attribution]]**. 갱신 — 닻 [[assb-contact-loss-vs-lampe]] (채움표 23호 행 + 누적 줄 + For 열아홉 번째 + Against 새 첫 항목 + 새 제약 5개 + Status Log + 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]] (일곱 번째 적용 + 처방 표 두 줄) · [[assb-apparent-capacity-decomposition]] (손실 예산) · [[assb-li-in-reference-potential-window]] (여덟 번째 형태 + P13). index 에 새 개념 등록.
- 후속 후보: ★★★★ 1 **Zhang 2017 *ACS AMI* 9, 17835** (ref 29, 본문 8 회 — 방법 원전) · ★★★★ 2 **Kondrakov 2017 *JPCC* 121, 3286** (ref 41, NCM811 ΔV) · ★★★ 3 **Ishidzu 2016 *SSI* 288, 176** (ref 48) · ★★★ 4 **Zhang 2017 *JMCA* 5, 9929** (ref 40).

## [2026-09-23] ingest | `assb` 24호 — Stavola, Sun, Guida, Bruck, Cao, Okasinski, Chuang, Zhu, Gallaway 2023, Lithiation Gradients and Tortuosity Factors in Thick NMC111-Argyrodite Solid-State Cathodes (*ACS Energy Lett.* 8, 1273−1280, CC-BY 4.0)

- `raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md` (sha256 봉인). 큐 **23번**. Northeastern + Argonne APS 6-BM. 크로퍼가 본문 그림 6 + SI 그림 17 + SI 표 9 를 잡고 **초록(TOC) 그래픽을 놓쳐** p1 을 400 dpi 수동 크롭(`fig_TOC_manual_p1.png`, `figures.json` 에 `manual` 등록) ⇒ **그림 24장 전부 봤다, 안 본 것 0장.** 식 (2)–(4)·S4–S7 은 페이지 렌더로 읽었다.
- ★★★ **01 대질 — 반박도 지지도 아니다, 다른 기구다**: 01 의 "finite size effect" 는 모델 체적을 자를 때 전자 클러스터 소속이 부푸는 것이고, 01 은 `[인쇄]` "tortuosity, and resulting effective conductivities … not explicitly treated" 로 이 편이 재는 항을 뺐다. 이 편은 두께를 스윕하지 않고(110 · 155 µm 조성 교락, 50 µm 한 셀) 1호를 인용하지도 않는다(ref 41 = Bielefeld 2020).
- ★★★★ **리튬화 구배 = `η(z)` 몸통 + `θ` 형 모집단**: 반응파·전류 역전(40 % 분리막 조각 1.2 h)·방전 끝 완화는 `η(z)`; `[도표]` 80 % 집전체 쪽 조각 6 의 (003) 한 봉우리가 충전 1 내내 pristine 근처 = 22호의 "불활성". 측정 원리(식 S14 높이 가중평균)가 둘을 합치고, 전제 "same area" 는 Fig. S6 에서 깨진다. 22호 표층 편향 크기 `[도표]` ±0.08 `(1−x)`, 부호 = σ_el/σ_ion.
- ★★★ `[재현]` **첫 사이클 비가역 ≈0.2 Δx 가 깊이 균일** ⇒ 두께 수송 아님; **코팅 쌍(계보 첫 통제 쌍)** 이 그것을 ≈14 % 만 줄임 — 23호 손실 예산과 같은 방향.
- ★★★★ **굴곡도는 측정이 아니라 분할**: `σ_eff = σ_bulk·ε/τ²` 에서 `ε` 는 가정(14 %; `[재현]` 두께 함의 21–38 %). **D1 — 이온 쪽 `τ²` 4 값이 ε_CAM 으로 계산**(4/4 ≤2 %) ⇒ "tipping point" ×1.6 ↔ 바른 ε ×0.92. σ_eff 로 비교하면 "굴곡도 진화" 는 **80 % 셀 ≈3 배 하나**(LPSC COMSOL/EIS 0.93 · 0.34) — 압력(50/150 ↔ 100 MPa)·ε·모델(OCP 없음)·접촉 어느 쪽에도 배정.
- ★★★ **곱 축퇴 처방 여덟 번째 적용**: 1단계 ❌(상태축 0) · 2단계 ⚠(코팅 쌍 = 화학 대조) · 3-a/3-b ❌ · **4단계 ✅ 70 % 통과 · 80 % 실패**. 처방 표에 두 줄(코팅 유무 쌍 · 두 영역 대조의 시편 조건). 23호의 "R·C 같은 상태축" 은 적용 불가 — 같은 분류 문제가 봉우리 이봉(`j₀` ↔ `A_eff` ↔ 자촉매)으로 나타나고 코팅 쌍이 화학 몫을 뗀다.
- **17호 함정**: 주 주장(깊이 `(1−x)`)은 면제, 방전 끝 바닥 ≈0.80 은 노출(In–Li 조성 미기재). **Q5 아홉 번째 형태 = "기준을 말하지 않는다"** — 그림 축 기준 0, `vs Li−In` SI 1 회, 모델 CE 임의 0 V + OCP 없음.
- **Q4 0/24 — 열일곱 번째 성질 "비식별을 물리로 읽었다"** (i₀ 평탄 → "not kinetically limited" · 두 경로 불일치 → "evolved" · 둔감 파라미터를 7 자리로, 같은 저항 두 적합 1.35–2700 배 · 가정 분할 → "tipping point"). Q4 의 첫 **재료**(ε 규약 반전 표 · 세 `τ²` 병치).
- **채움표 24호 행 — 누적 ≈15.0 → ≈15.0 (새 칸 0).** 안 움직인 칸: Q1(`θ(N)` 0/24) · Q2(층: `η(z)` 공간 연산자) · Q4 · Q5 · Q6(제조 압력 교락) · Q8(NMC111 첫, OCP 0) · Q7(해당 없음). Q3 층 하나(같은 양의 세 추정 병치, 계보 첫).
- 컴파일: **새 개념 [[assb-tortuosity-factor-effective-conductivity-split]]**. 갱신 — 닻 [[assb-contact-loss-vs-lampe]] (채움표 24호 행 + 누적 줄 + For 스무 번째 + Against 새 첫 항목 + 새 제약 5개 + Status Log + 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]] (여덟 번째 적용 + 처방 표 두 줄) · [[assb-apparent-capacity-decomposition]] (`η(z)` · 관측 연산자 · 비가역 깊이 균일) · [[assb-interphase-vs-contact-loss-attribution]] (코팅 쌍 첫 표본 · 채널 두 줄 · 계보 행) · [[composite-cathode-percolation-utilization]] (01 대질).
- ⚠ 어긋남 17 건(D1 ε 규약 · D2 가중 전제 · D3 "<0.02" ↔ ≈0.04–0.07 · D4 Δx 인쇄 ↔ 그림 · D5 Li 함량 >1 · D9 모델 10 h ↔ 실험 6.6/7.5 h · D11 얇은 셀 두께 · D13 void 14 % 출처 · D17 코팅 행 불일치).
- 후속 후보: ★★★★ 1 **Bielefeld 2020 *ACS AMI* 12, 12821** (ref 41 · SI 5, 원장에 있음) · ★★★★ 2 **Minnmann 2021 *JES* 168, 040537** (ref 42 · SI 18, 원장에 있음) · ★★★ 3 **Davis 2021 *ACS Energy Lett.* 6, 2993** (ref 39) · ★★★ 4 **Park 2021 *Nat. Mater.* 20, 991** (ref 51 · SI 12) · ★★★ 5 **Naik 2022 *ACS AMI* 14, 29754** (ref 54).
- lint: **0 errors · 0 warnings**.

## [2026-09-23] ingest | `assb` 25호 — Zhou, Lu, Mish, Chen, Feng, Kim, Song, Kim, Liu 2025, Tailored Cathode Composite Microstructure Enables Long Cycle Life at Low Pressure for All-Solid-State Batteries (*ACS Energy Lett.* 10, 966−974)

- `raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md` (sha256 봉인). 큐 **24번**. UCSD + LG Energy Solution. 크로퍼가 본문 그림 4 + SI 그림 21 + 표 2 를 잡고 **초록(TOC) 그래픽을 놓쳐** p1 을 400 dpi 수동 크롭(`fig_TOC_manual_p1.png`, figures.json 에 `manual: true`). **Fig. 2 · Fig. 3 은 PDF 벡터 경로에서 좌표를 추출**했다. **26장 전부 봤다, 안 본 것 0장.** DEM 브랜치 앵커 CSV 는 읽지 않았다(하드룰 1).
- ★★★★ **압력 × 미세구조 요인 설계(운전 30 · 10 · 2 MPa × SE 입도 2)** — `[재현]` 초기 압력 손해는 공통 모드(c2 −26.5 ↔ −30.7 mAh g⁻¹), 미세구조는 감쇠의 압력 의존만 바꾼다(fine −26/−27/−22 ↔ coarse −33/−38/−64). 1 사이클 뒤 `R_NCM`·`R_anode` 도 두 조성 같이 ×1.7–1.9.
- ★★★★ **DEM `θ`(LAMMPS Hertz)는 겹침 기준 0–10 % 에서 94 → 20 %** — 원전은 2 % 를 골라 "83 % ↔ ≈85 %" 로 맞춤. `[재현]` 30/10 MPa 첫 충전 비 coarse/fine **1.03** ⇒ "17 % 불활성" 과 모순; 데이터는 0 % 쪽.
- ★★★★ **그림 무결성**: Fig. 3 DRT 12 곡선 중 5 개가 2 개(≤0.21 Ω) · Nyquist "2 MPa 1 뒤" = "30 MPa 100 뒤"(≤0.8 Ω) · S15 굴곡도 히스토그램 제목 반전 · 인쇄 유지율 6 중 2 만 재현 · 18/20/22 는 V–Q 판에서만(2 MPa 는 coarse 2 사이클 ↔ fine 1 사이클) · fine 30 ↔ 10 MPa 라벨이 그림마다 다름. DRT 면적 +8/+26/+115 % ↔ 판독 0/+57/+171 %.
- ★★★★ **17호 함정 노출** — S19 에서 `R_SSE/anode` 가 모든 조건에서 가장 큰 항, 2 MPa coarse `[재현]` 방전 전압 하강 ≈0.30–0.37 V 의 ≈80 % 가 Li 계면. **Q5 열 번째 형태** = "Li 금속이라 기준을 문제 삼지 않는다 — 자기 적합이 상대극을 가장 큰 항으로 인쇄".
- ★★★ **5호 Doux 대질** — 같은 UCSD, 인용 0. 음극 계면 저항의 압력 방향은 같다; **위 벽 반례 후보**(Li 금속 30 MPa ≈1500–1700 h, 5호 25 MPa ≈48 h 단락); 모든 셀이 하강 분기(375/30 MPa 제조).
- ★★★ **곱 축퇴 처방 아홉 번째 적용**: 1단계 ❌(`C` 미인쇄, τ 대리는 겹침·범례에 걸려 `C` ×0.77 ↔ ×1.20) · **2단계 ✅(부분) SE 입도 쌍 + BET — C 비 1.7–2.5 ↔ 면적 예측 1.75 · BET 1.53** · 3-a ❌ · 3-b ✅ · 4단계 ❌. 저자가 `C ∝ 면적` 을 스스로 인쇄한 첫 편 — P1(입계)에 걸어 벽돌층 모형과 방향 반대(`[추론]`). 처방 표에 한 줄.
- **Q4 0/25 — 열여덟 번째 성질 "민감도를 인쇄하고 그 손잡이로 검증을 맞췄다".**
- **채움표 25호 행 — 누적 ≈15.0 → ≈15.5 (Q6 +0.5).** 안 움직인 칸: Q1(측정 0 · 계산 `θ` 손잡이 · `θ(N)` 0/25 · 23호 대리량 적용 불가) · Q2(층) · Q4 · Q5 · Q8 · Q7(해당 없음). Q3 층 둘(그림 자료 정체 불확실 · 암묵적 반복 ≈20 %).
- 컴파일: **새 개념 0**. 갱신 — 닻 [[assb-contact-loss-vs-lampe]] (채움표 25호 행 + 누적 줄 + For 스물한 번째 + Against 새 첫 두 항목 + 새 제약 5개 + Status Log + 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]] (아홉 번째 적용 + 처방 표 한 줄) · [[assb-stack-pressure-operating-window]] (요인 설계 · 5호 대질 · 요구치) · [[composite-cathode-percolation-utilization]] (계산 `θ` 손잡이 · 첫 충전 시험) · [[assb-apparent-capacity-decomposition]] (충전 ↔ 방전 · 율 극한 · 공통 모드) · [[assb-tortuosity-factor-effective-conductivity-split]] (기하 τ, `σ_eff` 미측정).
- ⚠ 어긋남 22 건(D1–D3 그림 겹침·제목 반전 · D4–D7 인쇄 ↔ 그림 · D9 온도 30 ↔ 23–25 °C · D11 σ "very close" ↔ ×0.66 · D16 음극 없는 셀의 "음극" 봉우리 · D17 이용률 정의 둘 · D19 "Tan et al." = Shi, T. · D20 이론밀도 1.64 ↔ 1.86).
- 후속 후보: ★★★★ 1 **Sakka 2022 *JMCA* 10, 16602** (ref 12, CT 압력별 접촉 면적 분율) · ★★★★ 2 **Shi 2020 *AEM* 10, 1902881** (ref 14, DEM 이용률 방법 원전, 원장에 있음) · ★★★ 3 **Xu 2024 *AEM* 14, 2303539** (ref 11, 요구치) · ★★★ 4 **Schlautmann 2023 *AEM* 13, 2302309** (ref 13, SE 입도 분포) · ★★★ 5 **Jiao 2023 *ESM* 61, 102864** (SI ref 3, DEM 연결성 후처리) · 큐 **32번**(저압 종설)과 짝.

## [2026-09-23] ingest | `assb` 26호 — Iwakiri, Delgado, Nogueira 2024, Introducing a new model for solid-state batteries: Parameter estimation and sensitivity analysis on diffusion, concentration, and electrochemical kinetics (*Electrochim. Acta* 508, 145202, CC BY)

- `raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md` (sha256 봉인). 큐 **25번**("Q4 확인용"). NTNU + Simoldes Plásticos. **모델 편** — 데이터는 Raijmakers 2020 박막 Li/LiPON/LCO 4 율 방전곡선(98 점)을 빌림, 열화 0. 크로퍼가 본문 그림 21 + 표 3 을 잡았다(SI 없음); Table 3 은 p7 300 dpi 수동 렌더로 `D_e⁻` 지수 확인.
- 큐 표 낱말 지문 재집계 — 같다(`identifiab` 0 · `uniqu` 0 · `sensitiv` 3 · `OCV` 0); `sensitiv` 3 = 제목 · Table 1 열 머리 · "less sensitive to air". 본문 이름은 "parametric study"(16 회).
- ★★★★ **Q4 0/26 — 움직이지 않는다.** "sensitivity analysis" = 1C 전방 모델의 OAT 대역 스윕(×0.1–500 · 동역학 ×5e-7–1e5) + 설계 KPI. FIM · 조건수 · 프로파일 · CI 전수 0, Nelder–Mead 점추정.
- ★★★★ **그러나 추정 + 스윕이 같은 지면인 계보 첫 편** — 저자 그림에 비식별 방향 셋: Fig. 5a(`D_e⁻` 0 열) · Fig. 12a≡b(`k₁`↔`k₂`) · Fig. 3≡15(`D_M⊕`↔`a_max`, `[재현]` `x` 좌표 스케일 대칭). `[인쇄]` Table 3 `D_e⁻` 5.24e-3 ↔ 문헌 5.06e-13(10 자릿수); `[재현]` 식 (30) 으로 문헌값이면 Fig. 5a·5b 가 성립 안 함 ⇒ 스윕은 표류한 적합점에서 돌았고 그 둔감이 결론의 "느린 종 지배" 가 됐다.
- ★★★ `[재현]` 적합 변수 10 중 **7 이 정확히 문헌 ×1.0500** ↔ `[인쇄]` "not fed into the optimization algorithm"; 문헌값의 출처 = 데이터 출처(ref 10). ★★ 모델 1C = 1.23 mA(Fig. 4·9·13 검산) ↔ 셀 0.7 mAh.
- **Q4 열아홉 번째 성질 = "평탄을 스스로 계산해 놓고, 평탄 위의 점을 값으로 인쇄하고, 그 점에서 본 둔감을 물리로 읽었다"** — 반 칸 검토 후 접음(보인 것은 우리 `[재현]`).
- **곱 축퇴 처방 열 번째 적용** — 1–4단계 전부 ❌(이중층 가정 배제 · EIS 0 · 한 온도 · 펄스 0). 처방 표에 한 줄("추정 논문의 스윕 그림 겹치기 = 공짜 `J^T J`").
- **채움표 26호 행 — 누적 ≈15.5 → ≈15.5 (새 칸 0).** 안 움직인 칸: 전부. Q3 층 하나(문헌 대조의 순환).
- 컴파일: **새 개념 [[assb-sensitivity-sweep-vs-identifiability]]**. 갱신 — 닻 [[assb-contact-loss-vs-lampe]] (채움표 26호 행 + 누적 줄 + For 스물두 번째 + 새 제약 4개 + Status Log + 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]] (열 번째 적용 + 처방 표 한 줄) · `index.md` 등록.
- ⚠ 어긋남 14 건(D1 `D_e⁻` · D2 ×1.0500 · D3 식 36 부피 누락 · D4 0.7 ↔ 1.23 mAh · D5 Fig. 5 ↔ 식 30 · D6–D7 캡션 ↔ 본문 · D8 Fig. 16 ↔ 15 · D9 Fig. 21 "Case 1.0" = Case 1.5).
- 그림: **21장 전부 봤다, 안 본 것 0장.**
- 후속 후보: ★★★★ 1 **Raijmakers 2020 *Electrochim. Acta* 330, 135147** (ref 10) · ★★★ 2 **Firouz 2020 *J. Energy Storage* 28, 101184** (ref 17, "system identification") · ★★★ 3 **Deng 2021 *IEEE TTE* 7, 464** (ref 16) · ★★★ 4 **Danilov 2011 *JES* 158, A215** (ref 15). Bizeray 2019(큐 27) 인용 0.
- lint: **0 errors · 0 warnings**.

## [2026-09-23] ingest | `assb` 27호 — Sinzig, Schmidt, Wall 2024, Analysis of the Validity of P2D Models for Solid-State Batteries in a Large Parameter Range (J. Electrochem. Soc. 171, 120519)

- `raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md` (sha256 봉인). 큐 **26번**("Q4 확인용"). TUM 계산역학 + TUMint.Energy. **모델 편** — 3D 입자 분해 FEM ↔ 균질화 P2D (NMC622/LPS/Li), 실험 0 · 빌린 데이터 0 · 열화 0.
- 큐 표 낱말 지문 재집계 — 합자 그대로는 같다(`identifiab` 0 · `sensitiv` 26 · `Sobol` 29 · `OCV` 0). **NFKC 정규화 뒤 `identifiab` 1**("phenomena … identifiable", 파라미터 뜻 아님) — 지문 도구 맹점 = `ﬁ` 합자.
- ★★★★ **Q4 0/27 — 움직이지 않는다.** 전역 민감도는 제대로(Sobol 1·2·전차 + 95 % CI · GP 대리 · 150 표본 · 2¹⁴ MC) — 그러나 출력은 설계 KPI `SOC_end` 하나, 데이터 0. 26호 표로 **첫 줄의 전역판** + 새 줄 "모델 불일치 민감도" `|∇d_SOC|`. 묻는 것은 **모델 적합성**.
- ★★★★ 비식별 재료 셋(`S_T(D │ P2D) ≈ 0` · 두 모델 일치 영역 · `[인쇄]` "a constant difference could still be corrected by an update of the homogenization parameters")을 저자는 전부 적합성으로 읽었다.
- ★★★★ `[재현]` 벡터 좌표 — 그 상수(큰 `κ` 오프셋 0.068 · Fig. 7 150 점 평균 차 0.072)는 **비연결 몫 `1 − u` = 0.07**(접촉 손실). 저자 배정은 "insufficient homogenization strategy"; `u` 처방은 `A_el-c` 로 용량 깎기; 그 곡선(Fig. 3b "dashed line")은 **그림에 없다**.
- **Q4 스무 번째 성질 = "적합성을 전역으로 재고, 그 안의 비식별 재료 셋을 전부 모델 적합성으로만 읽었다. 그리고 상수의 정체는 접촉 손실이었다"** — 반 칸 검토 후 접음.
- **곱 축퇴 처방 — 적용 대상 아님(모델 편).** 모델 쪽 세 번째 표본: `A_el-c` 가 면적 · 용량 · 연결 분율을 함께 진다(`[재현]` 실제 비표면적의 ≈1.5 배). `τ` = 24호의 `τ²`(이름 충돌). `D/d²`: `d̄` 개수 평균 ↔ `d₄₃` (시간척도 ≈3.5 배).
- **채움표 27호 행 — 누적 ≈15.5 → ≈15.5 (새 칸 0).** 안 움직인 칸: 전부. Q3 층 하나(모델 대 모델 참값 + CI 붙은 민감도).
- 컴파일: 새 개념 0. 갱신 — 닻 [[assb-contact-loss-vs-lampe]] (채움표 27호 행 + 누적 줄 + For 스물세 번째 + 새 제약 6개 + Status Log + 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]] (전역판 · 모델 불일치 민감도 줄 · 적합성 ≠ 식별성 · 처방 5–6) · [[assb-lampe-contact-product-degeneracy]] (27호 절) · [[assb-tortuosity-factor-effective-conductivity-split]] (이름 충돌 절) · index 개념 줄.
- ⚠ 어긋남 15 건(**D1 Fig. 3b 점선 없음** · **D2 Fig. 13 ≈0 영역의 `D` 방향** · D3 `m_SOC` 선형 ↔ `lg` · D4–D6 Sobol 서술 ↔ 그림 · **D7 Fig. 14a 점선 색 뒤바뀜** · D8 · D9 AM 비 0.4 ↔ 0.47 · D15 "factor five" ↔ 6.4).
- 그림: **15장 전부 봤다, 안 본 것 0장** (+ 쪽 렌더 26장 · 벡터 추출 Fig. 3b·7·9a·11a·14b).
- 후속 후보: ★★★★ 1 **Khalik 2021 *J. Power Sources* 499, 229901** (ref 27) · ★★★★ 2 **Lu, Trimboli, Fan, Wang, Plett 2022 *JES* 169, 080504** (ref 28) · ★★★ 3 **Schmidt, Sinzig, Wall 2024 *JES* 171, 100502** (ref 18, 박리).
- lint: **0 errors · 0 warnings**.

## [2026-09-23] ingest | `assb` 28호 — Bizeray, Kim, Duncan, Howey 2019, Identifiability and Parameter Estimation of the Single Particle Lithium-Ion Battery Model (IEEE TCST 27(5), 1862) — ⚠ 액체셀

- `raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md` (sha256 봉인). 큐 **27번**("방법론 원전 (액체셀)"). Oxford + SAIT. 선형화 SPM 의 구조적(전달함수 유일성) · 실제적(손실 등고선) 식별성, 합성 LCO + 실험 Kokam NMC 740 mAh EIS. ASSB 아님 — Q4 방법 원전이라 `assb` 번호.
- 큐 표 낱말 지문 재집계 — `identifiab` 추출 그대로 9 는 **전부 대문자 쪽 머리글**, **NFKC 뒤 54**(본문 42 · 머리글 9 · 참고문헌 3). `ﬁ` 182 · `ﬂ` 16. `OCV` 67 · `GITT` 2 · `sensitiv` 7 · `Sobol` 0 · `fit` 0 → 14. **합자 맹점이 IEEE 에도 있다.**
- ★★★★ **Q4 ASSB 0/28 — 도구 칸만.** 계보 첫 셋째 줄(식별성)이지만 식별 집합 `(τ_d⁺, τ_d⁻, R_ct)` 에 용량이 없다 — `Q_th` 는 `β = dU/dQ`(기준극 입력)로, `x⁰` 는 가정. 보편 범위 명제("any lithium-ion battery model … flat OCV")는 동역학 파라미터 ⇒ 반 칸 검토 후 접음. **스물한 번째 성질 "도구는 있고 대상이 없다".**
- ★★★ `[해석]` 묶음 대조 — 26호 `k₁≡k₂` = 식 50 같은 구조 · `D_e⁻` 0 열 = 예외 1(`β = 0`) 같은 부류 · 다른 기구 · 27호 `1 − u` = `Q_th` 손잡이. **SPM 에서 입자 통째 비연결 ≡ LAM**(ε 는 `Q_th` 에만 있다), 표면 일부 접촉은 `R0` 로 사라진다.
- ★★★ `[재현]` Fig. 9 벡터: "max 20 mV" 는 양의 최대 — 적색 최소 −42.9 mV, RMS 10.3 ✓, 순 방전 72.5 mAh(9.8 %) ✓. ×0.78 사후 보정(양극 OCV 기울기 ≡ `Q_th⁺` ×1.28)은 검증과 같은 데이터. Table I `D₊` 는 그림과 10³ 불일치(Fig. 1 저주파 점근선으로 판정).
- **곱 축퇴 처방 열한 번째 적용** — 1–4단계 전부 ❌(고주파 반원을 설계상 버림). 곱의 액체 SPM 원형(식 18 · 26)은 있다.
- **채움표 28호 행 — 누적 ≈15.5 → ≈15.5 (새 칸 0).** Q3 층 하나(합성 참값 복원 — 같은 모델 · 무잡음).
- 컴파일: **새 개념 [[spm-grouped-parameter-identifiability]]**(도구 페이지, `assb` 태그 없음) · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · For 스물네 번째 · 새 제약 6 · Status Log · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](28호 절 · 처방 7) · [[assb-lampe-contact-product-degeneracy]](열한 번째 적용) · [[22p-physics-or-degeneracy]](전극 맞바꿈 대칭, 형식 유비) · `index.md` 등록.
- ⚠ 어긋남 8 건(D1 `D₊` ×10³ · D2 `τ_d⁻` 2841 ↔ ≈4000 · D3 `A` 이름·단위 · D4 max 20 ↔ −42.9 mV · D5 60000 ↔ 50 147 s · D6 둘째 최소 확인 불가 · D7 비독립 검증 · D8 `R_ct(DoD)` 를 비용으로 읽음).
- 그림: **9 장 전부 봤다, 안 본 것 0 장** (+ Table II 쪽 렌더 · Fig. 9 벡터 추출).
- 후속 후보: ★★★★ 1 **Forman 2012 *J. Power Sources* 210, 263** (ref 18, DFN Fisher 식별성) · ★★★ 2 **Alavi 2016 arXiv 1505.00153** (ref 33, Randles 회로 식별성) · ★★★ 3 **Santhanagopalan 2007 *JES* 154, A198** (ref 30, 모델 판별). 26·27호 모두 이 편 인용 0.


## [2026-09-23] ingest | assb 29호 — Yanev et al. 2024, Quantifying Resistive and Diffusive Kinetic Limitations of Thiophosphate Composite Cathodes (J. Electrochem. Soc. 171, 050530)

- `raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md` (sha256 봉인). 큐 **28번**("`η(i)` 항 그 자체 + OCV 곡선 최유력"). Fraunhofer IKTS — 17호와 같은 연구실(17호 = ref 21). 14 복합체 CA + 대칭 셀 EIS/TLM + GITT, 신품, 2전극 Li-In. **SI 미열람**(업로드 없음, IOP 접근 정책상 차단).
- 큐 낱말 지문 재집계(NFKC 전/후) — `identifiab` 0/0 · `uniqu` 0/0 · `GITT` 20/20 · `OCV` 0/0: **큐 지문이 정규화 전후 모두 맞다.** 정규화가 바꾼 것 `fit` 0 → 20 · `identif*` 1 → 4. `ﬁ` 99 · `ﬂ` 17. 식별성 신호는 지문 열 밖 `dependenc*` 2.
- ★★★★ **Q4 +0.5 — ASSB 계보 첫.** `Q(R) = Q_M/(1+2(Rα)ⁿ)` 적합에서 `[인쇄]` sc90 `Q_M`·`α` "high dependencies close to unity in Table S2" = 저자의 공분산 진단 + 비식별 명제, 식별 집합에 용량 스케일 포함. `[재현]` 고율 극한이 `Q_M·α⁻ⁿ` 한 조합 — 정합. 반 칸: SI 미열람 · 국소 · 축이 정적↔동적 · 진단 미전파(sc84 외삽 ≈236 이 "LIB 초과 이용률" 결론).
- ★★★ `[재현]` GITT `D_app` = `D·(A_eff/V)²` = 28호 `τ_d` 묶음 — "확산성 한계" 와 "작은 접촉 면적(φ)" 은 같은 숫자 · `σ_eff`–`D` Spearman 0.94 · Table I `ε` 역산 = 공칭 · sc73-BM 행 전사 오류 둘. `[해석]` `n` = CA 누적 전하 시간 지수 → TLM √t 대안(판별 안 함).
- **곱 축퇴 처방 열두 번째 적용** — 2단계 부분 ✅ · 4단계 자릿수 양립 · 1·3단계 ❌. 처방 첫 줄(율 스윕 `i → 0`)의 계보 첫 실적용 + 실패 조건.
- **채움표 29호 행 — 누적 ≈15.5 → ≈16.0 (Q4 +0.5).** Q1 이동 없음(역산 둘, `θ(N)` 0/29) · Q2 반 칸 검토 후 접음 · Q5 열한 번째 형태 "검증 이식" · Q3 층 둘.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · For 스물다섯 번째 · Against 단서 · 새 제약 7 · Status Log) · [[assb-sensitivity-sweep-vs-identifiability]](29호 절 · 처방 8) · [[spm-grouped-parameter-identifiability]](29호 세 줄) · [[assb-lampe-contact-product-degeneracy]](열두 번째 적용 · 새 줄 둘) · [[assb-tortuosity-factor-effective-conductivity-split]](네 번째 표본) · [[assb-apparent-capacity-decomposition]](29호 절).
- ⚠ 어긋남 15 건(D1 "175 and 195" 순서 반대 · D3 sc84 `D` 표↔그림 · D4 sc73-BM 두 칸 · D6 `Q_M` < 실측 저율 · D7 sc84 외삽 해석 · D9 sc90 무표시 작도 외).
- 그림: **7 장 전부 봤다, 안 본 것 0 장** (+ 식 1–5 렌더 · Fig. 2c/2d 확대). SI 그림 8 · 표 2 못 봄.
- 후속 후보: ★★★★ 1 **Tian 2020 *J. Power Sources* 468, 228220** (ref 19, 식 (2) · `n` 배정 원전) · ★★★ 2 **Yanev 2022 *JES* 169, 090519** (ref 20) · ★★★ 3 **이 편의 SI** (Table S2) · ★★ 4 **Kaiser 2018 *JPS* 396, 175** (ref 22).

## [2026-09-23] ingest | assb 30호 — Park 2024, Unraveling Asymmetric Electrochemical Kinetics in Low-Mass-Loading NMC111 Li-Metal All-Solid-State Batteries (Materials 17, 5014)

- `raw/papers/park2024_asymmetric-kinetics-low-mass-loading-nmc111-latp-li-metal.md` (sha256 봉인). 큐 **29번**("Q8 보조"). 홍익대 단독 저자, CC BY, SI 없음. Li \| 소결 LATP 펠릿(150 µm) \| NMC111 슬러리 전극(0.57 mg cm⁻², **SE 없음**) 2전극 CR2032 + 액체 대조(표만). 주사율 CV(b · Randles–Ševčík · Dunn) + 율 스윕.
- 큐 낱말 지문 재집계(NFKC 전/후) — `identifiab` 0/0 · `uniqu` 1/1 · `sensitiv` 1/1 · `GITT` 0/0 · `OCV` 0/0: **큐 지문이 정규화 전후 모두 맞다.** 합자 0, 정규화가 바꾼 문자 `µ` → `μ` 3 개. ⚠ 대소문자 무시 오검출 `ICI` 21 · `MPa` 20 · `LLI` 2.
- ★★★★ **Q4 0 (ASSB 누적 0.5 유지) — 스물두 번째 성질 "라벨이 자기 그림을 거스른다"**: `[재현]` Fig. 3 교차 판독 b 산화 ≈0.58 · 환원 ≈0.73 ↔ 인쇄 0.76 · 0.58. 전제가 배타인 두 모형 병치.
- ★★★★ **Q5 열두 번째 형태 "방향 비대칭의 일방 배정"**: Li 금속 "reference and counter", 상대극 석출/박리 언급 0, Li/LATP/Li 대칭셀은 σ 한 값으로 소진. `[재현]` σ 는 호 포함 · 직렬 ≈0.5–0.86 kΩ ↔ CV 봉우리 이동 ≈0.54–0.65 kΩ.
- ★★★ `[재현]` Table 1 "고체" 용량 행 ≠ Fig. 2a = "액체" 행 · 액체/고체 `D` 10.9 = 유효 면적 ≈3.3 배로도 설명(29호와 반대 배정) · 29호 식 적용 `Q_M` ≈63 은 −26 % 표류 뒤 값(율 스윕 두 번째 실패 조건).
- **채움표 30호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q1 `θ(N)` 0/30 · Q3 층 둘(label-contradicts-own-figure · textbook-equation-with-unprinted-inputs).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · For 스물여섯 번째 · 새 제약 6 · Status Log) · [[assb-lampe-contact-product-degeneracy]](열세 번째 적용 · 처방 표 3 행) · [[spm-grouped-parameter-identifiability]](Randles–Ševčík · Dunn 행) · [[assb-sensitivity-sweep-vs-identifiability]](세 줄 밖 표본 · 처방 9).
- ⚠ 어긋남 17 건(D1 b 배정 반대 · D2 Table 1 용량 행 · D5 "activation" ↔ 봉우리 −62 % · D6 dQ/dV 손실 전 · D7 고율 귀속 · D9 전제 위반 · D11 σ 인용 없음 외).
- 그림: **크로퍼 4 장 전부 봤다, 안 본 것 0 장** (+ Fig. 2a 확대 · Table 1 쪽 렌더).
- 후속 후보: 1 **큐 30 ICI (*Nat. Commun.* 2023)** · 2 **Nomura 2019 *Angew. Chem.* 131, 5346** (ref 33) · 3 **Yu … Wagemaker 2017 *Nat. Commun.* 8, 1086** (ref 6).

## [2026-09-23] ingest | assb 31호 — Chien et al. 2023, Rapid determination of solid-state diffusion coefficients in Li-based batteries via intermittent current interruption method (Nat. Commun. 14, 2289)

- `raw/papers/chien2023_ici-rapid-solid-state-diffusion-coefficient.md` (sha256 봉인, 본문 9 쪽 + SI 26 쪽). 큐 **30번**("이 곡선이 얼마나 평형인가"). Uppsala + Scania, CC BY, zenodo 원자료 공개(미열람). ⚠ **액체셀** — NMC811 | Li 링 기준극 | Li, 1 M LiPF₆ 3전극 파우치 ×2. 수정 GITT 로 GITT ↔ ICI ↔ EIS 대조 + 표준 ICI 55 사이클 + operando XRD.
- 큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말): `GITT` 94 → **92**(부분문자열 `GITTin`·`GITT5`) · `ICI` 100 → **99**(대소문자 무시였다) · `open circuit` 5 ✓ · `equilibri*` 4 ✓. ★ 대소문자 무시 `ici` 는 NFKC 뒤 **162** — 합자가 `coefficient` 오검출 62 를 가리고 있었다(27·28호와 반대 방향).
- ★★★★ **핵심 판정 — ICI 는 곱 `D·(A/V)²` 을 가르지 않는다**: 식 19 에 `A` 제곱 입력, `A` = BET 상수 → 전부 `D` = **세 번째 배정, 첫 고지된 배정**(`[인쇄]` "BET-surface area may differ from the electrochemically active surface area … both … equally affected"). 비교는 봉인, 사이클 · operando 절대 주장에서 봉인 해제.
- ★★★ `[해석]` `D_app` 은 입자 통째 비연결(`u`)에 불변 · 표면 피복에 `φ²` — 두 접촉 손실이 다른 축으로 간다 · ICI `R/k` 는 면적 소거 조합(처방 새 줄 **후보**, 지면에 사이클별 `k` 없음).
- ★★★ `[재현]` SI Note 1·2 한계 37.7 · 26.8 · 12.8 s 재현 · BET ↔ D50 구 선택만으로 `D` ×2.52 > 방법 간 SD 0.56 · SD 0.56 = 2·√(0.26²+0.076²) · 신품 4.18 V `D` 골은 OCP 기울기(×0.36)가 만들고 `k` 는 준다 · operando `D` 급락 구간 = 상속 가정 "single-phase" 가 자기 XRD 로 깨진 곳.
- **채움표 31호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q4 ASSB 0 — 스물세 번째 성질 "공통 인자로 비교를 봉인하고, 절대 주장에서 봉인을 뗐다" · Q1 `θ(N)` 0/31 · Q3 층 둘(measured-bundle-with-declared-constant · regression-SD-only error bars).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · For 스물일곱 번째 · 제약 4 · Status Log) · [[assb-lampe-contact-product-degeneracy]](열네 번째 적용 · 처방 표 2 행) · [[spm-grouped-parameter-identifiability]](ICI 3 행) · [[assb-sensitivity-sweep-vs-identifiability]](방법 간 일치 ≠ 인자 식별).
- ⚠ 어긋남 20 건(D1·D3·D4 SI 그림 번호 오지시 · D2 SD 0.086 ↔ 0.076 · D8 체계 편차 · D9 Fig. 1 (c)↔(e) · D12 극값 시각 · D13 "uniformly" · D15 표준 ICI 무대조 · D19 단상 가정 ↔ 두 상 외).
- 그림: 크로퍼 26 장 — **15 장 직접 봤다**(본문 8 전부 + SI 8·10·12·13·15·16·18), **안 본 것 11 장**(SI 1–7 · 9 · 11 · 14 · 17).
- 후속 후보: 1 **Geng … Brandell 2022 *Electrochim. Acta* 404, 139727** (ref 19) · 2 **Chouchane 2020 *JPCL* 11, 2775** (ref 24) · 3 **zenodo 원자료로 `R/k`** · 4 **Xu 2021 *Nat. Mater.* 20, 84** (ref 31).

## [2026-09-23] ingest | assb 32호 — Biçer et al. 2025, Solid-State Batteries: Chemistry, Battery, and Thermal Management System, Battery Assembly, and Applications — A Critical Review (Batteries 11, 212)

- `raw/papers/bicer2025_ssb-chemistry-bms-thermal-assembly-critical-review.md` (sha256 봉인, 49 쪽 = 본문 42 + 참고문헌 160 편, SI 없음). 큐 **31번**("08 의 '접촉 손실 ↔ 보통 노화 분리 진단' 요구가 매단 유일한 인용"). Sivas + Kayseri + Siro(셀 제조사) + Bozankaya + TechConcepts + INEGI, EU Horizon "EXTENDED", CC BY. ⚠ **Review — 전기화학 1차 측정 0**.
- 큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말): **11 열 전부 일치**. NFKC 변경 31 자(터키어 결합 부호 · `µ`), 합자 0 → 정규화 전후 수 동일. 대소문자 무시 오검출 `LLI` 42 · `LAM` 28 · `MPa` 142.
- ★★★ **8호 인용 대조**: 8호 §6.1 이 이 편에 매단 3 요소 중 압력 센서 ✅ · 압력 의존 임피던스 ⚠ 절반 · **"contact loss ↔ ordinary aging 진단" ❌ 없음** — 요구 명제의 첫 인쇄는 8호 자신.
- ★★ 축 판정: (a) BMS — 관측 V·I·T + 권고(압력 센서 · EIS · 서브셀), **구별 0**, 접촉 = 임피던스(용량 몫 없음; 분류 체계 네 번째 표본) · (b) 온도 — **0**(`Arrhenius` 0, 열관리 = 열폭주 안전) · (c) 압력 — `MPa` 0, 제조 ↔ 운전 미구분.
- ★★ `[해석]` BMS 어휘의 전제: OCV–SoC "well-established linear"(p.23, p.24 "nonlinear" 와 모순) · SoC 분모 = 정격 용량 · SEI = interface 재정의 · Fig. 3 bipolar 스택이 셀별 OCV 관측 가능성을 지운다.
- **채움표 32호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q4 ASSB 0 — 스물네 번째 성질 "선형 OCV 전제가 물음을 지운다" · Q1 `θ(N)` 0/32 · Q3 층 하나(정의 없는 SoH + 정격 분모 SoC).
- 곱 축퇴 처방 **열다섯 번째 적용 — 대상 없음**, 대신 BMS 센서 ↔ 처방 단계 대응표(우리 번역).
- ⚠ 어긋남 13 건 + 사소: **D2 Fig. 6B 5.473 kJ/g → 본문 5473 kJ g⁻¹(×1000)** · D3 OCV 선형/비선형 · D4 산화물 전도도 · **D6 "replacing SSEs with organic liquid electrolytes"** · **D8 인용 불일치 12 건(제목 기준)** 외.
- 그림: 크로퍼 20 장 — **4 장 봤다(Fig. 1 · 3 · 4 · 6), 그중 3 장이 본문과 어긋남**; 안 본 것 Fig. 2 · 5 · 7–12, 표 8 장은 텍스트 대조.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 스물여덟 번째 · 제약 5 · Status Log) · [[assb-lampe-contact-product-degeneracy]](열다섯 번째 적용).
- 후속: 160 편 중 Q1 · Q4 · 곱 분리 · 기준극 누설 1차 후보 **0**(제목 기준). 약한 후보 Celen 2021 IEEE SysCon (ref 11, ASSB-ECM) · Kan 2024 *ESM* 68 (ref 124, 온도). 압력 값은 큐 32.

## [2026-09-23] ingest | assb 33호 — Zhang et al. 2025, Challenges and Strategies of Low-Pressure All-Solid-State Batteries (Adv. Mater. 37, 2413499)
- raw: `raw/papers/zhang2025_low-pressure-assb-challenges-strategies-review.md` (sha256 봉인) · 그림 `raw/figures/zhang2025_low-pressure-assb-challenges-strategies-review/` 9 장. 큐 **32번**("Q6 주축 · 24 번과 짝"). EIT Ningbo + USTC + UWO, CC BY-NC-ND. ⚠ **Review — 1차 측정 0**, 그림 8 장 전부 모식 · 재수록.
- 큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말): **11 열 전부 일치**(`contact loss` 4 · `MPa` 50). NFKC 변경 204 자(합자 193) — 지문 열은 전후 동일, 열 밖에서 `effect` 0 → 30 · `identif` 0 → 2(식별성과 무관).
- ★★★ **판정**: Q6 · Q1 칸 이동 없음 — 압력 수치 50 개 중 압력의 **함수** 0, `θ(N)` 0/33 · `θ(P)` 0. **Sakka 2022 = [120] 인용, 단 "3D 접촉 · 압력 방향" 명제에 · 수치 0** · **Xu 2024 = [11] 인용, 단 "hundreds of MPa" 에만 · "<≈1 MPa" 없음**. 제조 ↔ 운전 압력 명시 분리 ✅(종설 계보 첫).
- ★★★ **귀속 검사**: 8호 "pressure reduction = commercialization problem" ✅ 선다 · 25호 "짝, 인용 아님" ✅(양방향 시점상 불가) · 25호 "≤5 MPa" 는 이 편에서 오지 않음 · 요구치 계보 **다섯 번째 값 < 2 / ≤ 2 MPa, 출처 없음**(5 편 · 4 값 · 원전 0).
- ★★★ **23호 대조 ❌**: 유일한 양극 접촉 손실 문단이 Koerver 2017 의 "첫 충전 = 접촉 / 이후 = 계면상" 배정을 뒤집고, "압력으로 재활성" 은 인용 번호 없이 인쇄(D1 · G4) — 분류 체계 다섯 번째 표본.
- **채움표 33호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q4 ASSB 0 — 스물다섯 번째 성질 "용량은 전략의 성적표" · Q3 층(재수록 그림 출처 갈림 3/8) · Q6 층 둘 · Q8 입력 하나(Fig. 3A/B 부피 곡선).
- 곱 축퇴 처방 **열여섯 번째 적용 — 대상 없음**. `[해석]` 재수록 상대극 압력 진동 0.7–2.3 MPa/사이클 ≈ 산업 운전 압력(양극만 ≈0.05–0.07).
- ⚠ 어긋남 12 건: D1 23호 배정 뒤집음 · D2 Fig. 3I 출처 [63] ↔ [78] · D3 Fig. 2D 본문 ↔ 그림 · D4 "most labs 50–600 MPa" 출처 0 · D5 Fig. 5 A/B 뒤바뀜 외.
- 그림: 크로퍼 9 장 — **6 장 봤다(Fig. 1 · 2 · 3 · 4 · 5 · 7), 그중 4 장이 본문과 어긋남**; 안 본 것 Fig. 6 · 8, Table 1 은 텍스트 전사.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 스물아홉 번째 · 제약 5 · Status Log) · [[assb-lampe-contact-product-degeneracy]](열여섯 번째 적용) · [[assb-stack-pressure-operating-window]](제조/운전 분리 · 요구치 다섯 번째 · 압력 진동).
- 후속: Sakka 2022(지목 2 회) · Xu 2024(승격 제안) · Koerver 2018 *EES*(지목 2 회) · Gao 2022 *Joule* · Cronau 2021(DEM SE 압분) · Zhang 2017 *JMCA*(지목 3 회). Q1 · Q4 · 곱 분리 · 기준극 누설 1차 후보 0.

## [2026-09-23] ingest | assb 34호 — Liang et al. 2026, Pulse excitation for active battery management systems (npj Clean Energy 2, 16)
- raw: `raw/papers/liang2026_pulse-excitation-active-bms-comment.md` (sha256 봉인) · 그림 `raw/figures/liang2026_pulse-excitation-active-bms-comment/` 1 장(크로퍼 0 장 — 벡터 그림, 300 dpi 수동 크롭). 큐 **33번**("Q4 설계 축 — 우리 폭 측정기의 역방향"). UNSW + Chalmers + UTS, CC BY-NC-ND. ⚠ **Comment 5 쪽 — 1차 측정 0 · 데이터 0 · ASSB 0**(도구 칸).
- 큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말): **11 열 중 9 열 일치, 2 열 불일치** — `identifiab` 0 → **3** · `confidence interval` 0 → **1**, 둘 다 정규화 전 0(합자 `ﬁ` 67 자). 같은 검사로 큐 35 번 `confidence interval` 0 → 6. 텍스트 층이 `10⁻¹ Hz` 의 음부호를 잃는다(렌더로 확인).
- ★★★ **판정**: 펄스가 곱 축퇴 처방의 **어느 단계도 명제로 실현하지 않는다** — 세 대역 이름(옴 > 10³ · 계면 분극 10⁰–10³ · 확산 개시 < 10⁻¹ Hz) + 신경망 재구성, `capacitan*` · `time constant` · `relaxation` 0(31호 `R_ICI` 보다 한 층 아래). `[해석]` 한 펄스 이완 = 1단계 τ 형 · 4단계 · `R/k` 의 공통 입력(kHz 급 샘플링 · 2전극 합 · `C ∝ A` 전제 · √t 창 조건). OCV 분해는 **대체 쪽**(IC/DV "정보 밀도 부족" → 재구성) + 불변량 "active material stoichiometric limits"(α·β 의 양, 근거 0).
- **채움표 34호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q4 ASSB 0 — 스물여섯 번째 성질 "식별성을 입력 설계로 살 수 있는 자원으로 인쇄했다"(FIM · CRLB · D-optimality · PE 처방, 계산 0, 구조적 ↔ 실제적 구분 0) · Q3 층 하나(learned-reconstruction features, 제안형).
- 곱 축퇴 처방 **열일곱 번째 적용 — 적용 불가 · 온보드 번역 한 줄**(한 펄스 이완 = 처방 공통 입력; 재구성 · 온도 불변 학습은 그 입력을 지우는 방향). `[해석]` D-optimality 는 구조적 곱 축퇴에 0 — OED 는 우리 폭 측정기의 짝이되 사후 전역 검증이 필요.
- ⚠ 어긋남 8 건: D1 반복 문장 셋 · D2 확산 대역 ↔ "ms–s" 창 · D3 화학량론 "불변" ↔ Fig. 1b 열화 도메인 · D4 그림 ↔ 캡션 라벨 · D5 "CRLB = FIM⁻¹" · D6 ref 28 문맥 · D7 기간 표기 · D8 OED 시제.
- 그림: **1/1 장 봤다**(Fig. 1, 수동 크롭). 본문과 어긋난 것: 라벨 2(D4) · 기간(D7).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 서른 번째 · 제약 5 · Status Log) · [[assb-lampe-contact-product-degeneracy]](열일곱 번째 적용 · 처방 표 온보드 줄) · [[assb-sensitivity-sweep-vs-identifiability]](입력 설계판 줄).
- 후속(제목 기준): Jiang·Tao·Lee·Moura 2026 *Joule*(ref 19, CRLB 한계) · Li·West·Preindl 2023 *JPS*(ref 24, 펄스 열화 특성화) · Tang 2023 *iScience*(ref 21, 10 Hz 재구성 EIS) · Yang 2024 *Science*(ref 29, 접촉 복원 펄스). 큐 34 · 35 는 인용되지 않는다.

## [2026-09-23] ingest | assb 35호 — Roman et al. 2021, Machine learning pipeline for battery state-of-health estimation (Nat. Mach. Intell. 3, 447–456)
- raw: `raw/papers/roman2021_ml-pipeline-soh-estimation-uncertainty.md` (sha256 봉인; 본문 + SI 두 PDF 해시) · 그림 `raw/figures/roman2021_ml-pipeline-soh-estimation-uncertainty/` (크로퍼 그림 18 + 표 11, 본문 Fig. 2 · 4 · 5 수동 크롭 + Fig. 1 재크롭). 큐 **34번**("Q3 — 08 Table 2 에서 유일하게 신뢰구간 보고"). Heriot-Watt + CALCE + TU Delft. ⚠ ML 방법 논문 — 1차 실험 0, 공개 액체 셀 179 개.
- 큐 낱말 지문 재집계(NFKC 뒤 · 대소문자 구분 · 낱말): **11 열 중 10 열 일치, 합자 가림 0** — `calibrat` 39 는 대소문자 무시 수(규칙대로 36). **큐 35 번 `confidence interval` 0 → 6 을 35 번 원본에서 직접 확인**(여섯 개 전부 합자 `ﬁ`, pp. 18–19).
- ★★★ **판정**: (a) 용량(Ah) 스칼라 하나 — 모드 분할 0(차원 1 ↔ ≥3) · (b) 특징 = 충전 상단 0.3 V 창 + CV 꼬리의 범함수 → `[해석]` α·β 의 함수, 특징 공간 LLI ↔ LAM 축퇴는 다루지 않음 · (c) 불확실성 = 예측 오차 보정(isotonic + 보정 전용 셀 + 90 % 적중률), 식별성 아님 · (d) 전부 실측, 역범죄 없음 — 대신 데이터셋 표지(`Nominal Capacity` · `Charge Current`)와 과거 라벨 합(`Lagged Cumulated Discharge Capacity`)이 선택된 입력. ASSB 0 → 도구 칸.
- **채움표 35호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q4 ASSB 0 — 스물일곱 번째 성질 "불확실성을 보정했다 — 분해가 없는 스칼라 위에서" · Q3 층 하나(measured scalar label + held-out-recalibrated predictive interval).
- ★★ **8호 원장 정정 둘**: "보정된 불확실성 0/8" → **1/8** · "RMSE 0.45 % (best)" → dNNe RMSPE, 최저는 RF 0.14 %.
- 곱 축퇴 처방 **열여덟 번째 적용 — 적용 불가**, 경고 한 줄: 목표 주도 특징 선택은 분리 채널을 버린다(유일한 저항 채널이 세 그룹 모두 탈락).
- ⚠ 어긋남 21 건: D1 그룹 ↔ 프로토콜 · D2 초록 "best 0.45 %" · D3 RMSPE 0.97 = 합 ÷ 2 · D4 Group I 분할 23/10/5/19 ↔ `[재현]` 24/11/5/18 · D5 셀 38 정체 · D6 PEP 97.71 ↔ Fig. 2d · D12 Fig. 1c 창 ≈0.09 V ↔ 0.3 V · D14 SI Fig. 10 캡션 a/b 외.
- 그림: **9 장 봤다**(본문 Fig. 1–5 · SI Fig. 4 · 8 · 10 · SI Table 2 쪽); 안 본 것 SI Fig. 1 · 2 · 5 · 6 · 7 · 9 · 11 · 12 · 14 · 15 · 17 · 18.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 서른한 번째 · 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](열여덟 번째 적용 · 처방 표 경고 줄) · [[assb-sensitivity-sweep-vs-identifiability]](예측 보정 줄 · 처방 10).
- 후속(제목 기준): Kuleshov 2018 (ref 62) · Richardson 2018 *IEEE TII* (ref 32) · Birkl 2017 박사논문 (SI ref 22) · Saxena 2008 (ref 64). Q1 · Q4 · 곱 분리 1차 후보 0.

## [2026-09-23] ingest | assb 36호 — Thelen et al. 2024, Probabilistic machine learning for battery health diagnostics and prognostics — review and perspectives (npj Mater. Sustain. 2, 14)
- raw: `raw/papers/thelen2024_probabilistic-ml-battery-health-review.md` (sha256 봉인) · 그림 `raw/figures/thelen2024_probabilistic-ml-battery-health-review/` (크로퍼 18 장, Fig. 2 · 9 제외; Fig. 3 · 4 전체 수동 재렌더). 큐 **35번**("Q3·Q4 — 불확실성 보정"). Review 33 쪽, CC BY, 1차 측정 0, ASSB 0.
- ★★★ **판정**: (a) aleatory/epistemic(→ model-form · parameter) 은 가르고 식별성은 없다 — 사후 폭 = 예측 분포 또는 ML 가중치, 근최적 폭과 다른 대상 · (b) **확률적 모드 진단 1차 원전 0/13** — Fig. 4 도 Problem 4 만 점, 사후 상관에 가장 가까운 것은 Ruan 2022 의 "상관된 모드"(학습 사전) · (c) CI ⊂ PI ⊂ TI 정의(35호 `μ ± 2σ` = PI) · (d) ASSB 0 → 도구 칸.
- **채움표 36호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q4 ASSB 0 — 스물여덟 번째 성질 "불확실성의 분류학을 세웠는데, 데이터를 더 모아도 줄지 않는 파라미터 불확실성의 칸이 없다" · Q3 층 하나 · Q1 분류 체계 여섯 번째 표본(Fig. 3 재작도가 접촉 손실의 모드 연결을 지웠다).
- 큐 낱말 지문 재집계(NFKC · 대소문자 구분 · 낱말 경계): NFKC 변경 684 자(`ﬁ` 481). 정정 — `uncertaint` 205 → 180 · `Bayes` 53 → 35 · `posterior` 28 → 26 · `calibrat` 8 → 7(큐 값 = 공백 소실로 붙은 낱말 포함 부분문자열 · 문서 전체) · `confidence interval` 6 확인 · `LAM` 5 는 가림(`LAMPE`/`LAMNE` 13).
- 곱 축퇴 처방 **열아홉 번째 적용 — 대상 없음**, 경고: 확률적 추정이 곱을 가리는 세 번째 경로(평균장 VI · 상관된 학습 사전).
- ⚠ 어긋남 12 건: D1 Fig. 3 캡션 "connections" ↔ 연결선 0 · D2 Severson 2021 ↔ 2019 · D3 절 교차참조 5 곳 · D7 Roman "RF lowest accuracy" 그룹 의존 · D8 CI 문단 내부 긴장 · D9 부트스트랩 반복 수 외.
- 그림: **5 장 봤다(Fig. 3 · 4 · 7 · 13 · 15)**; 어긋난 것 Fig. 3 · Fig. 7. 안 본 것 Fig. 1 · 2 · 5 · 6 · 8 · 9 · 10 · 11 · 12 · 14 · 16–20.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 서른두 번째 · 제약 6 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](열아홉 번째 적용) · [[assb-sensitivity-sweep-vs-identifiability]](불확실성 분류 ≠ 식별성 줄 · 처방 11).
- 후속(제목 기준): Gasper 2021 *JES* 168 (ref 52) · Gasper 2022 (ref 169) · Thelen 2022 *ESM* 50 (ref 81) · Ruan 2022 *Energy AI* 9 (ref 196) · Schmitt 2023 (ref 192). 확률적 모드 진단 · Q1 · 곱 분리 1차 후보 0. 큐 36 · 37 인용 0.

## [2026-09-23] ingest | assb 37호 — Li et al. 2024, Modeling of an all-solid-state battery with a composite positive electrode (eTransportation 20, 100315)
- raw: `raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md` (sha256 봉인 — 본문 PDF · SI .docx 해시 각각 frontmatter) · 그림 `raw/figures/li2024_assb-composite-cathode-model-contact-area-edl/` (크로퍼 13 + SI SEM `fig_s1.png` zipfile 추출). 큐 **36번**("9호가 모델 · PSO · `A_eff` 정의를 위임한 곳"). 모델 + 신품 실험, 노화 0.
- ★★★★ **판정**: (a) 표면 접촉 손실 `A_eff` 는 `LAM_PE` 와 다른 손잡이 — 용량 · 확산에 없고 BV 분모에서 `k_p` 와 **정확한 곱**(접촉 ↔ 계면 화학 항등); 입자 통째 비연결의 자리는 `ε_p`(= `LAM_PE`) 뿐 · (b) Table 1 각주 5 종, `A_eff` · `ε_p` · `c_dl` 무표기, **`A_eff` 두 값이 9호와 네 자리 같다(상속)**, `k_p` 인쇄값은 측정 범위 밖 · (c) 식별성 명제 0, "sensitivity" = 0.4 C OAT · (d) 합성 truth 로 쓰면 두 갈래 동어반복(`A_eff(N)` → OCV 에 안 보임 · `k` 와 같음 / `ε_p(N)` → 정의상 `LAM_PE`).
- **채움표 37호 행 — 누적 ≈16.0 → ≈16.0 (새 칸 0).** Q1 `θ(N)` 0/37 · Q4 ASSB 0 스물아홉 번째 성질 · Q3 층 하나(footnote-typed table — the contact knob is the unmarked row) · Q5 열세 번째 형태 "차감 흡수".
- 곱 축퇴 처방 **스무 번째 적용 — 원천 모델에 건다**: 처방 표 새 줄 둘(`A_eff ↔ k` 항등 · 율 스윕 줄 세 번째 실패 조건 = 율별 재적합 `D_p,ref`).
- ⚠ 어긋남 14 건: D1 `R_s` 9.315 µm ↔ SI SEM ≈0.5–1.5 µm(9호 "9 배" 의 원천) · D2 `A_eff` 상속 · D3 `k_p` 범위 밖 · D6 "minimal" ↔ ±40–60 mV · D7 이완 ≈10² s ↔ `R·C` 1.5–7 ms 외.
- 낱말 지문(NFKC · 대소문자 구분 · 낱말 경계 · 본문): `identifiab` 0 · `LAM` 0(접두 포함) · `contact loss` 0 · `MPa` 0(SI 1). NFKC 변경 8 자(`´`) — 열 변화 0. 소프트 하이픈 81 은 NFKC 가 안 지운다.
- 그림: **8 장 + 표 1 봤다(Fig. 2 · 4 · 5 · 6 · 8 · 9 · 11 · S1 + Table 1 상단)**; 어긋난 것 Fig. 4b · 5c · 5d · 8a · 9c/f · 11b/e · 11f · S1. 안 본 것 Fig. 1 · 3 · 7 · 10 · Table 2 이미지 · SI 수식 WMF.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 서른세 번째 · 새 제약 5 · Status Log) · [[assb-lampe-contact-product-degeneracy]](스무 번째 적용 · 9호 `A_eff` 정정 · 표 두 줄) · [[assb-sensitivity-sweep-vs-identifiability]](37호 절 · 처방 12) · [[spm-grouped-parameter-identifiability]](37호 두 행).
- 후속(제목 기준): Raijmakers 2020 *Electrochim. Acta* 330 (ref 14) · Deng 2021 *IEEE TTE* 7 (ref 29) · Kim 2019 *Electrochim. Acta* 317 (ref 21) · Froboese 2019 *JES* 166 (ref 30). 큐 37 · 38 인용 0.

## [2026-09-23] ingest | assb 38호 — Conforto et al. 2021, Quantification of the Impact of Chemo-Mechanical Degradation on NCM-Based Cathodes in Solid-State Li-Ion Batteries (J. Electrochem. Soc. 168, 070546)
- raw: `raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd.md` (sha256 봉인 — PDF 해시 frontmatter) · 그림 `raw/figures/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd/` (크로퍼 9). 큐 **37번**("Q1 을 깰 1 순위") — **큐의 마지막 편**. OA CC BY, SI 미수령.
- ★★★★ **판정**: (a) 사이클마다 **이완 OCP 두 점 → 활성 질량**(식 7) · **저주파 EIS → 확산 경로 분포**(EIS-PSD) — 활성 질량은 `θ·ε_p` 합, 용량 역산, 전부를 "We suggest" 로 접촉 손실에 배정(합 측정 + 이름 붙이기) · (b) 접촉 ↔ `LAM_PE` 실험 분리 0(보유 리튬 0 자 · 재가압 0 · LLI 는 Li 과잉 ×2.75 로 설계상 안 보임) · (c) SC ↔ PC(입도 · 재소성 교락) · (d) 전자 비연결 → `C_diff` 질량(= `ε_p`), SE 접촉 · 균열 → `L_diff`; 반무한 꼬리는 `L/(C_diff√D̃)` 곱.
- **채움표 38호 행 — 누적 ≈16.0 → ≈16.5 (Q2 +0.5).** Q1 `θ(N)` 0/38(첫 `θ·(1−LAM)` 합 계열 1/38) · Q4 0/38 서른 번째 성질("식별 한계를 식으로 인쇄하고, 결론의 수를 그 한계 밖에 두었다") · Q5 열네 번째 형태("고정 전위가 게이지의 영점이다").
- ★★★ 9호 기각("error … relatively large") ↔ 본문 "good agreement for all" ↔ `[도표]` Fig. 9 (a) +12…+27 · (d) −14…−28 mAh g⁻¹ — 9호가 그림에 맞다.
- 곱 축퇴 처방 **스물한 번째 적용**: 표 새 줄 "이완 OCP 두 점 = 연결 질량" + 경고 줄 "반무한 꼬리 곱 `L/(C_diff√D̃)`".
- ⚠ 어긋남 11 건: D1 닫힘 · D2 Fig. 9 가는 선 ↔ Fig. 6 · D3 SC "<2" ↔ 2.0 · D4 Fig. 5d ↔ 9a 같은 조건 ≈37 mAh g⁻¹ · D6 `C_diff/m` ×0.72 · D7 질량 > 1 외.
- 낱말 지문(NFKC · 대소문자 구분 · 낱말 경계 · 본문): `identifiab` 0 · `uncertaint` 2 · `LLI` 0 · `LAM` 0 · `degradation mode` 0 · `contact loss` 13 · `MPa` 2. NFKC 변경 121 자 — 열 변화 0. 소프트 하이픈 0.
- 그림: **6 장 봤다(Fig. 4 · 5 · 6 · 7 · 8 · 9, Fig. 9 패널 확대)**; 안 본 것 Fig. 1 · 2 · 3(모식 · 모사).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 서른네 번째 · Against 단서 · 새 제약 7 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](스물한 번째 적용 · 표 두 줄) · [[spm-grouped-parameter-identifiability]](38호 두 행) · [[assb-li-in-reference-potential-window]](열네 번째 형태).
- 후속(제목 기준, 큐 밖): Bartsch 2019 *Chem. Commun.* 55, 11223 (ref 47, operando XRD 활성 질량) · Ruess 2020 *JES* 167, 100532 (ref 19) · Fantin 2021 *Chem. Mater.* 33, 2624 (ref 41) · Lin 2014 *Nat. Commun.* 5, 3529 (ref 14) · Schönleber 2015/2017 (refs 32 · 31).

## [2026-09-23] ingest | assb 39호 — Sakka et al. 2022, Pressure dependence on the three-dimensional structure of a composite electrode in an all-solid-state battery (J. Mater. Chem. A 10, 16602)
- raw: `raw/papers/sakka2022_pressure-3d-structure-composite-cathode-xct.md` (sha256 봉인 — 본문 · SI PDF 해시 frontmatter) · 그림 `raw/figures/sakka2022_pressure-3d-structure-composite-cathode-xct/` (크로퍼 23). 큐 **40번** — **2차 묶음 40~59 의 첫 편**(원장 최상위). CC-BY 4.0, SI 16 쪽.
- ★★★★ **판정**: (a) X선 CT(SPring-8, 화소 0.5 µm)로 **접촉 면적 분율을 쟀다 — 표면 피복 `φ`**(NCM 표면 중 LGPS 와 닿은 몫), `θ` · `u` 아님 → 37호 기준 **`A_eff` 쪽 손잡이** · (b) 압력 축뿐(0 · 6 · 12 · 50 · 100 MPa, 신품) — **`θ(N)` 0/39**, `φ(P)` 는 **제조 압력**의 함수 · (c) 분할 문턱 미인쇄 · `[재현]` 분할이 고정 혼합물의 NCM/LGPS 부피비를 0.47 → 0.97 로 흔든다 · (d) `R_ct` ×14 ↔ `φ` ×1.10 ⇒ `R_ct·φ` ×13.
- **채움표 39호 행 — 누적 ≈16.5 → ≈17.5 (Q1 +0.5 · Q6 +0.5).** Q2 반 칸 검토 후 접음(신품) · Q4 0/39 서른한 번째 성질 · Q5 열다섯 번째 형태("상대극 계면을 양극 접촉 면적에 흡수한다").
- ★★★ **25호 ↔ 33호 인용 판정**: 둘 다 선다(결과 ↔ 제언). ⚠ 25호 digest 의 "모델상 25 MPa 면 안정" 은 Sakka 에 없다 — Zhou 원문의 무인용 인접 문장(우리 오귀속, 컴파일 페이지에서 정정).
- ★★★ DEM 보정 목표: 조건부 — 1순위 복합층 공극률(P) 5 점 · `φ(P)` 는 해상도 판정의 범위 제약으로만. DEM/MPM 파일 손대지 않음.
- 곱 축퇴 처방 **스물두 번째 적용**: 표 새 줄 "영상 면적 → `R·φ` 검사" — 2단계를 측정된 면적으로 건 첫 표본, 면적 가설이 CT 척도에서 기각.
- ⚠ 어긋남 12 건: D3 결론 방향 어휘 반전 · D4 "≈10 %" ↔ 비단조 · D6 질량수지 · D7 S3 절대 ↔ 정규화 · D8 고압 `R_ct` ↔ Nyquist ×2–3 · D11 ref 23 = 41 외.
- 낱말 지문(NFKC · 대소문자 구분 · 낱말 경계 · 본문): 11 열 중 `MPa` 30 외 전부 0(`contact loss` 0 · `contact area` 13). NFKC 변경 38 자 — 열 변화 0. `fi` · `µ` 글리프 추출 소실(단위는 렌더링으로 확인).
- 그림: **15 장 봤다(Fig. 1–6 · S1–S4 · S7 · S13–S16)**; 안 본 것 Fig. 7 · S5 · S6 · S8–S12.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 서른다섯 번째 · Against 단서 · 새 제약 6 · Status Log) · [[assb-lampe-contact-product-degeneracy]](스물두 번째 적용 · 표 한 줄) · [[assb-stack-pressure-operating-window]](39호 절 · 요구치 여섯 번째 인쇄 · 25호 오귀속 정정) · [[assb-pressure-reapplication-separation-test]](39호 절). 큐 `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g 신설(40 행).
- 후속(서지 기준, 큐 41–59 에 없음): Wang · Kazyak · Dasgupta · Sakamoto 2021 *Joule* 5, 1371 (ref 22, "1 MPa practically") · Ohashi … Hirai 2020 *JPS* 470, 228437 (ref 24) · Ohashi … Hirai 2021 *JPS* 483, 229212 (ref 25) · Fathiannasab 2021 *JPS* 483, 229028 (ref 18) · Doux 2020 *JMCA* 8, 5049 (ref 15).

## [2026-09-23] ingest | assb 40호 — Ikezawa et al. 2020, Performance of Li4Ti5O12-based reference electrode for the electrochemical analysis of all-solid-state lithium-ion batteries (Electrochem. Commun. 116, 106743)
- raw: `raw/papers/ikezawa2020_lto-reference-electrode-assb-three-electrode-eis.md` (sha256 봉인 — PDF 해시 frontmatter) · 그림 `raw/figures/ikezawa2020_lto-reference-electrode-assb-three-electrode-eis/` (크로퍼 3). 큐 **41번** — 2차 묶음 둘째 편, 지목 5 회(16 · 17 · 18 · 19 · 21호). CC BY, SI 없음.
- ★★★★ **Q5 판정**: (a) R-LTO 전위의 **누설 · 드리프트 · 안정성을 재지 않았다**(`leak` · `drift` · `assum*` 0) — 원장 구조적 공백 3 그대로, 누설 직접 측정 0/40 · (b) 1.55 V = ref [11] Costard 2017(액체셀) 수입, 검증은 환산한 두 평탄 ↔ 문헌 [5,17] "coincident" = P6 순환의 원전 확인 · (c) 19호 ±30 mV 의 근거 없음 · (d) 두 가지가 만난다 — 인용([5] Nam 2018 · [6] = 20호 Chang) · 기각(Li-In 은 기준극 부적합) · 한 셀(Li-In 문헌값이 증인) ⇒ **열여섯 번째 형태 "상호 증언"** · (e) `[재현]` 증인 0.62 V 면 R-LTO 1.5745 V — 1.55 ↔ 1.57 불가분 · (f) 부호 오기 "−0.60 V vs Li".
- **채움표 40호 행 — 누적 ≈17.5 → ≈17.5 (새 칸 0).** Q5 · Q2 반 칸 검토 후 접음 · Q4 0/40 서른두 번째 성질 "통과가 보장된 검사로 분리를 검증했다" · Q3 층 하나(같은 상태 R3 세 값 ×1.49).
- ★★★ 다른 편의 인용 교정: 21호 `[인쇄]` "∼40 mV ∼110 Ω cm²" → 원전 인쇄 0, `[도표]` C/2 충–방 폭 42.8 mV; 탈리튬만 21–23 mV ⇒ `[재현]` ≈58–63 Ω cm² · 20호 "뿌리 둘" → R-LTO 원전이 In 가지의 두 뿌리를 인용 · 17호 요약 "Li-In 병목" → 원문 "relatively large overpotential at the end of the discharges".
- 곱 축퇴 처방 **스물세 번째 적용**: 3-a ✅(재료만, `[재현]` 55.4 · 37.2) · 3-b R2 귀속 긴장(`C₂` ≈23 nF) · 4단계 ✅(Li-In DC ↔ EIS) · 표 새 줄 "3전극 옴 몫은 기준극 위치가 정한다".
- ⚠ 어긋남 6 건: D1 부호 · D2 [6] 은 LTO 를 안 쓴다 · **D3 R3 세 값** · D4 "Li₁₀GeP₂S₅" · D5 서지 · D6 "직선 이탈".
- 낱말 지문(NFKC · 대소문자 구분 · 낱말 경계 · 본문): 11 열 중 `MPa` 1 외 전부 0. NFKC 변경 0 · 줄끝 하이픈 이음 열 변화 0. 보조 `leak` 0 · `drift` 0 · `1.55` 1 · `30 mV` 0.
- 그림: **3 장 다 봤다**(Fig. 1–3, 화소 판독 1c · 1d · 2a · 2d · 3b · 3d).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 서른여섯 번째 · Status Log) · [[assb-li-in-reference-potential-window]](40호 절 · P6 원전 판정 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](스물세 번째 적용 · 표 한 줄). 큐 `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g 41 행 · 지문 행.
- 후속: Costard · Ender · Weiss · Ivers-Tiffée 2017 *JES* 164, A80 (ref 11 — 1.55 V 의 유일한 근거, 큐 없음) · Nam 2018 *JMCA* 6, 14867 (ref 5 — 큐 42) · Ender · Illig · Ivers-Tiffée 2017 *JES* 164, A71 (ref 10) · Braun 2018 *JPS* 393, 119 (ref 28).

## [2026-09-23] update | assb 40호 흡수 커밋 추적 — 내용은 `804cf4cf` 에 들어갔다
- assb 40호(Ikezawa 2020) ingest 의 스테이징된 변경 전부(digest · 그림 3 · 채움표 · 개념 2 · 큐 41 행 · log)가 **동시 세션의 커밋 `804cf4cf`**("docs(bms): MSC 세미나 적용 — 절 번호 바뀐 뒤 남은 교차참조(§5→§4) 수정")에 함께 들어갔다. 그 커밋은 이미 origin 에 있어 이력을 고치지 않는다. 이 항목과 큐 §6-3-g 41 행의 SHA 표기가 추적 기록이다.
- digest 봉인은 그대로다(`sha256 182057355a5b3762…` — 커밋된 파일에서 재계산 일치).

## [2026-09-23] ingest | assb 41호 — Nam et al. 2018, Diagnosis of failure modes for all-solid-state Li-ion batteries enabled by three-electrode cells (J. Mater. Chem. A 6, 14867)
- raw: `raw/papers/nam2018_three-electrode-assb-failure-modes-li-in-depletion.md` (sha256 봉인 — 본문 · SI PDF 해시 frontmatter `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/nam2018_three-electrode-assb-failure-modes-li-in-depletion/` (크로퍼 20, S8 누락). 큐 **42번** — 2차 묶음 셋째 편, 지목 4 회(17 · 20 · 21 · 40호). **In 가지에서 가장 이른 편(2018-07).**
- ★★★★ **Q5 판정**: (a) 본문 0.62 V = ref 33 Jung 2008 *AFM* 18, 3010 수입(Santhosha 2019 이전 경로) · (b) **SI Fig. S2 = 같은 설계 셀의 기준극 재료 교체(Li₀.₅In ↔ Li 금속)**, `[인쇄]` "marginal difference", `[도표]` Li 대비 CE 중점 ≈0.621 V · 두 셀 차 ≈2 mV — **P8 재료 축의 원전 실행, 수 미인쇄** · (c) 40호 "상호 증언" 의 In 쪽 끝 — 순환 밖 고리가 SI 에 하나 · (d) **열일곱 번째 형태 "기준극 교체 대조"**.
- ★★★★ **고갈층**: TOF-SIMS Li⁺ 단면 지도로 봤다(정성) — 반값 깊이 ≈49 µm(인쇄 "≈50 µm") · 대조군 0 · 정량 0 · `In-rich` 0 회 · "insulating" 측정 0. 21호 인용 선다, 조립 방향은 미시험(분말 CE).
- **채움표 41호 행 — 누적 ≈17.5 → ≈18.0 (Q5 +0.5).** Q2 반 칸 검토 후 접음 · Q4 0/41 서른세 번째 성질 "전극 분해를 '진단' 으로 인쇄했다 — 분해가 분리막 옴을 어느 전극 채널에 싣는지 묻지 않고" · Q3 층 하나(cutoff-identity terminal value).
- ★★★ `[재현]` 배면형 RE → 분리막 옴 전부가 CE(파생) 채널: "Gr < 0 V" 1 C ≈−0.02 ↔ 반전 계단 절반 ≈0.10 V · 2 C(730 µm) ≈−0.15 ↔ ≈0.20 V. Fig. 3c CE 종단 전위 = WE 종단 + 0.62 V 항등식.
- 곱 축퇴 처방 **스물네 번째 적용**: 1–3단계 ❌(EIS 0) · 새 줄 "배면형 기준극은 분리막 옴 전부를 상대극 채널에 싣는다".
- 카드 새 제약 5(측정 ↔ 파생 채널 · 컷오프 항등식 · 쿨롱 효율의 연성 단락 오염 · 기준 전위는 수를 인쇄 · 방전 끝을 양극이 낼 수 있다).
- ⚠ 어긋남 10 건: D1 Table 1 행 이름 뒤바뀜 · D2 컷오프 부호 · D3 Mo ↔ Ti · D4 항등식 · D5 계단 · D6 CE 양 · D7 ref 35/36 · D8–D10 교차 편.
- 낱말 지문(NFKC · 대소문자 구분 · 낱말 경계 · 본문): `calibrat` 1(Q5 문장) · `MPa` 6(SI 0) 외 전부 0. NFKC 변경 57 자 — 열 변화 0 · 줄끝 하이픈 53 곳 이음 열 변화 0.
- 그림: **8 장 봤다(Fig. 2–6 · S2 · S4 · S10)**, 화소 판독 S2 인셋 · 4a · 5b · S10b; 안 본 것 Fig. 1 · S1 · S3 · S5–S7 · S9 · S11–S14.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 서른일곱 번째 · 새 제약 · Status Log) · [[assb-li-in-reference-potential-window]](41호 절 · P8 원전 실행 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](스물네 번째 적용). 큐 §6-3-g 42 행 · 지문 표 · 각주 ⁷.
- 후속(서지 기준, 미열람 — 큐 43–59 인용 0): Jung, Lee, Kim, Kwon, Oh 2008 *AFM* 18, 3010 (ref 33) · Jung, Oh, Nam, Park 2015 *Isr. J. Chem.* 55, 472 (ref 9) · Zhang … Janek 2017 *ACS AMI* 9, 17835 (ref 34) · Yu, Bates, Jellison, Hart 1997 *JES* 144, 524 (ref 37).

## [2026-09-23] ingest | assb 42호 — Santhosha et al. 2019, The Indium–Lithium Electrode in Solid-State Lithium-Ion Batteries: Phase Formation, Redox Potentials, and Interface Stability (Batteries & Supercaps 2, 524)
- raw: `raw/papers/santhosha2019_indium-lithium-electrode-phase-formation-redox-potential.md` (sha256 봉인 — 본문 · SI PDF 해시 frontmatter `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/santhosha2019_indium-lithium-electrode-phase-formation-redox-potential/` (크로퍼 9 = 그림 6 · 표 3). 큐 **43번** — 2차 묶음 넷째 편, 지목 3 회(17 · 20 · 21호), 인용 6 편.
- ★★★★ **Q5 판정**: Li 금속 대비로 쟀다 — **액체셀**(1 M LiTFSI DOL/DME, Swagelok 3전극, 1 h 펄스 + 0.5 h 이완, 실온, 곡선 1 개, "experimental data scatters"). ASSB 안 Li 대비 0. 평탄 0.622 V · `[도표]` ≈1–47 at% · 평탄 안 ≈15 mV 처짐 · InLi 단상 1.9 at% / −280 mV · 0.339 · 0.122 V. **열여덟 번째 형태 "다른 전해질의 원전"** — 두 가지 영점(R-LTO · In)이 둘 다 액체셀 측정.
- ★★★★ **21호 어긋남**: 대칭셀은 InLi-(In) 조립 · 1 mAh cm⁻² 반주기 × 100 — `[재현]` 셀 12 Ω cm² 가 SE 벌크 옴 ≈400–570 Ω cm² 의 1/25–1/47(이온 경로 미입증; creep 강한 판과 양립) · 전기화학 리튬화분 대안은 첫 반주기에 적용 불가(그림은 ≈7 h 부터).
- **채움표 42호 행 — 누적 ≈18.0 → ≈18.5 (Q5 +0.5).** Q2 반 칸 검토 후 접음 · Q4 0/42 서른네 번째 성질 "산포를 문장으로 인정하고 대표값을 세 자리로 인쇄했다" · Q3 층 하나(charge-derived composition axis).
- 곱 축퇴 처방 **스물다섯 번째 적용**: 액체 EIS R·C 가 저자 면적 설명을 ≈20 % 만 받침 · 새 줄 "4단계를 SE 벌크 옴 하한과 먼저 대조한다".
- 카드 새 제약 6(원전 전해질 · 이완 · 창을 같이 인용 · 공칭 창은 필요조건 · 조성 질량 ↔ 치수 검산 · SE 옴 하한 · 같은 축 이름 다른 기준 · 상대극의 곱).
- ⚠ 어긋남 13 건: D1 전류 세 값 · D2 대칭셀 < SE 옴 · D3 SI 비 뒤집힘 · D4 CPE_SL 동일 · D5 ΔrG · D6 질량 ↔ 치수(44.1 ↔ 49.6 at%) · D7 상도 참조 · D8 SI · D9 12 mV · D10 CuS 창 · D11–D13 교차 편.
- 낱말 지문(NFKC · 대소문자 구분 · 낱말 경계 · 본문): 11 열 전부 0(`MPa` 0, SI 0). NFKC 변경 4 자 — 열 변화 0 · `µ` · 반각 대시 · 음수 부호 추출 소실 · 줄끝 하이픈 34 곳 이음 열 변화 0.
- 그림: **6 장 전부 봤다(Fig. 1–3 · S1–S3)**, 원본 래스터 화소 판독 Fig. 1 · 2a · 3; 표 3 장은 텍스트로.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 서른여덟 번째 · 새 제약 · Status Log) · [[assb-li-in-reference-potential-window]](42호 절 · 정의표 ② · 조건 (1) · P11 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](스물다섯 번째 적용). 큐 §6-3-g 43 행 · 지문 표 · 각주 ⁸.
- 후속(서지 기준, 미열람 — 큐 44–59 인용 0): Takada, Aotani, Iwamoto, Kondo 1996 *SSI* 86–88, 877 (ref 18) · Wen, Huggins 1980 *Mater. Res. Bull.* 15, 1225 (ref 17) · Webb, Baggetto, Bridges, Veith 2014 *JPS* 248, 1105 (ref 19) · Sangster, Pelton 1991 *J. Phase Equilib.* 12, 37 (ref 12a).

## [2026-09-23] ingest | assb 43호 — Fukunishi et al. 2023, Impedance Analysis and Cyclability Evaluation of Graphite Composite Electrodes with All-Solid-State Three-Electrode Cells (ACS Appl. Energy Mater. 6, 10908)
- raw: `raw/papers/fukunishi2023_graphite-three-electrode-impedance-cyclability.md` (sha256 봉인 — 본문 · SI PDF 해시 frontmatter `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/fukunishi2023_graphite-three-electrode-impedance-cyclability/` (16 장). 큐 44번(2차 묶음 다섯째 편). ⚠ 18호(NCM523 *JPS*)와 다른 논문 — 같은 연구실의 흑연 음극 판.
- ★★★★ **음극 열화 배정**: 저항 분해 = 측정(Table 3 `R` · CPE-T · CPE-P 노화 전후 ± · Table 2 `Ea` 전후) · 용량 → `LAM` = 해석(dQ/dV 높이 한 문장). 반쪽전지라 `LLI` 가 WE 용량에 없다 ⇒ 음극 곱 `(1−LAM_NE)(1−u)` 순수. `[재현]` `R_CT` 면적 서명(`C` ×0.43 ≈ 1/`R` ×0.47) > 용량 손실(`[도표]` ×0.75–0.78) · 3-a 는 반대(`Ea` 22 → 27.5) · 노화 뒤 세 `Ea` 27.5 수렴.
- ★★★ **Q5 판정**: 1.55 V 또 인용("Suppose" + Colbow · Ohzuku) · 증인 = 흑연 GITT 평탄 셋 + Li-In "0.60"(원전 0.62) · **R-LTO 가지 첫 표류 값 ≈10 mV(인쇄) / 공통 모드 ≈−14 · −16 mV(`[도표]`)** · 안정성은 합 일치로 "proves"(범주 오류) · `[재현]` R-LTO ≈1.568.
- **채움표 43호 행 — 누적 ≈18.5 → ≈19.0 (Q5 +0.5, 열아홉 번째 형태 "공통 모드 표류 판독").** Q2 반 칸 검토 후 접음 · Q4 0/43 서른다섯 번째 성질 "채널별 명명" · Q3 층 하나.
- 곱 축퇴 처방 **스물여섯 번째 적용(음극 첫)**: 1단계 완비 · 3-a 충돌 · 3-b ❌(×270–3,200) · 4단계 ✅(복합체 질량 읽기) · 새 줄 "면적 서명 ↔ 저율 용량 비 대조(반쪽전지 음극)".
- 카드: Evidence 서른아홉 번째 절 · 새 제약 6.
- ⚠ 어긋남 15 건(D4 CPE_X-T "decrease" ↔ ×5.2 · D5 `Ea` "nearly unchanged" · D7 컷오프 부호 · D10 RT 1 C −21 % · D11 0.21 V 봉우리 ×1.03 · D13 0.60 ↔ 0.62 외).
- 낱말 지문: `MPa` 2(SI 0) 외 11 열 전부 0 · `LAM` 0 이지만 구절 "loss of the active material" 1 · `Suppos*` 1 · `drift` · `leak` 0.
- 그림: **13 장 중 9 장 봤다(Fig. 1 · 2 · 4 · 5 · S2 · S4 · S5 · S7 · S8)**, 화소 판독 1b · 4a · 4b · 4d · S7a; fig_S7 은 크로퍼가 띠만 잘라 SI 8 쪽을 따로 렌더. 안 본 것 Fig. 3 · S1 · S3 · S6.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 누적 · 서른아홉 번째 · 새 제약 · Status Log) · [[assb-li-in-reference-potential-window]](43호 절) · [[assb-lampe-contact-product-degeneracy]](스물여섯 번째 적용 · 처방 표 새 줄 · 주장하지 않는 것). 큐 문서 §6-3-g 44 행 · 지문 행 · 각주 ⁹.
- 후속(서지 기준, 미열람 — 큐 45–59 인용 0): Kuratani … Kobayashi 2020 *ACS AEM* 3, 5472 (ref 24) · Otoyama … Tatsumisago 2018 *SSI* 323, 123 (ref 25) · Lee … Ahn 2022 *ACS AEM* 5, 5227 (ref 26) · Höltschi … Novák 2020 *JES* 167, 110558 (ref 27) · Yu … Fukutsuka 2022 *Electrochemistry* 90, 037003 (ref 30).

## [2026-09-23] ingest | assb 44호 — Jin et al. 2015, Effect of electrode design on electrochemical performance of all-solid-state lithium secondary batteries using lithium-silicide anodes (Electrochim. Acta 185, 242)
- raw: `raw/papers/jin2015_lithium-silicide-anode-electrode-design-assb.md` (sha256 봉인 — 본문 PDF 해시 frontmatter `pdf_sha256`) · 그림 `raw/figures/jin2015_lithium-silicide-anode-electrode-design-assb/` (12 장). 큐 45번(2차 묶음 여섯째 편) — 원장 "20호 셀의 원전"(20호 ref [12]).
- ★★★★ **20호 공백 대조**: G1 ✅ 양극 TiS₂ : SE : 탄소 = 50 : 50 : 0 wt%, `0.06 g` = 활물질(20호 N/P 8.4 선다) · G2 ✅ σ 1.8 × 10⁻⁴ = 30 MPa 펠릿 · SS 차단 · 1 kHz–7 MHz · 실온 · 절편 판독(두께 · 온도 · n 미인쇄) · G3 ⚠ 제조 30 MPa 인쇄, 운전은 Fig. 1 그림에만. **같은 셀 아님 — 같은 레시피**(SE 0.36 ↔ 1240 µm, 기준극 없음). `[재현]` 20호 음극 = 단층 Li-Si · 20호 R17 → 362 Ω 의 46–69 %.
- ★★★★ GITT "effective contact area" = `√D·S/θ` 곱을 대조 셀 가정으로 쪼갬(Case 2 도 전해질 없음) · 인쇄값 = 셋째 계단 · BET ×8.7 ↔ ×2.07 · Table 2 `ΔE_t` ↔ Fig. 6 ×≈2. `[재현]` **Li 재고 수지 위반**(Case 6 x ≈1.37) — "탈합금화가 빠르다" 와 모순.
- **채움표 44호 행 — 누적 ≈19.0 → ≈19.0 (새 칸 0).** Q4 0/44 서른여섯 번째 성질 "대조 셀 가정으로 곱을 쪼갰다" · Q5 스무 번째 형태 "GITT `ΔE_s` 안의 상대극 평탄 가정"(우리 판독) · Q3 층 하나.
- 곱 축퇴 처방 **스물일곱 번째 적용**: 2단계 ✅ 부분(계보 가장 이른 면적 대조군 + BET, 면적 가설 반증) · 새 줄 "외부 기준 네 번째 배정 — 같은 계의 면적 기지 대조 셀(GITT)".
- 카드: Evidence 마흔 번째 절 · 새 제약 5 · Status Log.
- 낱말 지문: `MPa` 2 외 10 열 전부 0 · `0.62` · `assum*` · `leak` · `drift` 0.
- 그림: **11 장 전부 봤다**, 화소 판독 Fig. 6 인셋.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]] · [[assb-lampe-contact-product-degeneracy]] · [[assb-li-in-reference-potential-window]] · 큐 문서 §6-3-g 45 행 + 지문 ¹⁰.
- 후속(서지 기준, 미열람 — 큐 46–59 인용 0): Park … Lim 2014 *JJAP* 53, 08NK02 (ref 20) · Liu … Wu 2005 *JPS* 140, 149 (ref 30) · Shen … 2013 *JES* 160, A1842 (ref 29) · Hayashi … Minami 2001 *J. Am. Ceram. Soc.* 84, 477 (ref 28) · Asl … Kim 2012 *Electrochim. Acta* 79, 8 (ref 17).

## [2026-09-23] ingest | assb 45호 — Hertle et al. 2023, Miniaturization of Reference Electrodes for Solid-State Lithium-Ion Batteries (J. Electrochem. Soc. 170, 040519)
- raw: `raw/papers/hertle2023_micro-reference-electrode-lithiated-gold-wire-assb.md` (sha256 봉인 — 본문 · SI PDF 해시 frontmatter `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/hertle2023_micro-reference-electrode-lithiated-gold-wire-assb/` (21 장). 큐 46번(2차 묶음 일곱째 편) — 원장 ★★★ "μ-RE 원본, Q5 최대 공백" · 16 · 21호 지목. JLU Giessen(Janek) + BASF.
- ★★★★ **Q5 판정**: 0 V = **도금 Li 상 정체**(Li 금속 대조 셀 없음) · Fig. 7 측정 축 −618 mV vs In/InLi(계보 첫 ASSB 안 인쇄 수) · `[도표]` 사다리 AuLi/AuLi₃ 개방회로 −0.485 ↔ 도금 −0.618 ⇒ 0.133 ↔ 문헌 0.134 V · 안정성 "≥8 일"(그림 · mV 0) · 점검 = 실험 사이 In/InLi 대비 + "refresh" · 누설 0/45 · `[재현]` 소진 가정 소비 ≈39 nA → (5′) ≥10 은 ≤ ≈19 h. **스물한 번째 형태 "셀 안 도금 Li — 영점을 상 정체로, 기준극을 소모품으로"**.
- ★★★★ **16호 이식 = 조건 밖**(∅25 ↔ 10 µm · 면적당 0.27 ↔ 2.55 mAh cm⁻² · NMC 상대 · 평탄 무) · `[해석]` 16호 0.11 V 새 후보 = AuLi/AuLi₃ 칸(+0.133 V)으로의 계단 이동.
- ★★★ 합 일치(3E 합 ≈ 2E) = 범주 오류 계열 — DC · 위치 artifact 둘 다 합에서 상쇄 · >10 kHz 원인 원문 0 · 검증 셀 ≠ 분석 셀(`[재현]`). 2E 적합 비유일성 인쇄(`R_Anode` 14 ↔ 3.9) → S7 이 Fit 1(우리 판독). 율 시험: 2E 방전 부족 = LTO 상대극 Li 소진(0.1 C 165 ↔ 193).
- **채움표 45호 행 — 누적 ≈19.0 → ≈19.5 (Q5 +0.5).** Q2 반 칸 검토 후 접음 · Q4 0/45 서른일곱 번째 성질 · Q3 층 하나.
- 곱 축퇴 처방 **스물여덟 번째 적용**: 3-b ✅ 호 #1 "SE separator" 배정 실패(≈10 nF ↔ 10–100 pF) · 새 줄 "합 일치는 분배를 검증하지 않는다".
- 카드: Evidence 마흔한 번째 절 · 새 제약 5 · Status Log.
- ⚠ 어긋남 19 건(D1 방전 순서 · D2 컷오프 · D3 Li 두께 · D5 Chang ×10 · D11 SE ×3.3 · D12 검증 셀 ≠ 분석 셀 외). 21호 `[추론]` "Schlenker → Hertle" 계보는 인용 목록에서 지지 안 됨.
- 낱말 지문: `MPa` 7(SI 0) 외 10 열 전부 0 · `leak` · `drift` · `calibrat` · `0.62` 0 · `stable` 16(μ-RE 11, 수치 판정 0).
- 그림: **20 장 중 15 장 봤다**(Fig. 1 · 3–13 · S1 · S5 · S7), 화소 판독 Fig. 7 · 10 · 13. 안 본 것 Fig. 2 · S2 · S3 · S4 · S6.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]] · [[assb-li-in-reference-potential-window]](45호 절 · 조건 (9) · P10 · P11) · [[assb-lampe-contact-product-degeneracy]](스물여덟 번째 적용 · 처방 표 새 줄) · 큐 문서 §6-3-g 46 행 + 지문 ¹¹.
- 후속(서지 기준, 미열람 — 큐 47–59 인용은 48 하나): Solchenbach … Gasteiger 2016 *JES* 163, A2265 (ref 20, 큐 48) · Bach … Renner 2015 *Electrochim. Acta* 164, 81 (ref 33) · Braun … Ivers-Tiffée 2018 *JPS* 393, 119 (ref 38) · Klink … La Mantia 2012 *Electrochem. Commun.* 22, 120 (ref 19).

## [2026-09-23] ingest | assb 46호 — Schlenker et al. 2020, Understanding the Lifetime of Battery Cells Based on Solid-State Li6PS5Cl Electrolyte Paired with Lithium Metal Electrode (ACS Appl. Mater. Interfaces 12, 20012)
- raw: `raw/papers/schlenker2020_li6ps5cl-li-metal-lifetime-three-electrode.md` (sha256 봉인 — 본문 PDF 해시 frontmatter `pdf_sha256`, SI 없음) · 그림 `raw/figures/schlenker2020_li6ps5cl-li-metal-lifetime-three-electrode/` (11 장). 큐 47번(2차 묶음 여덟째 편) — 21호 ref 17, 원장 Hertle 행 병합("'0 V 리튬화 금선' 관례의 출처" 후보). KIT IAM + Bosch + Marburg(Roling · Miß — 16호 공저자).
- ★★★★ **Q5 판정**: Au 도금 W 선 매립 기준극을 **썼다**(Li\|Li₆PS₅Cl\|Li 대칭셀 EIS 분할 전용) · 영점 · 리튬화 전하 · 선 지름 · 검증 · 표류 · 누설 전부 0 — 스물두 번째 형태 "영점이 들어가지 않는 자리". **계보 최종 판정**: 21호 "Schlenker → Hertle → 16호" = 하드웨어 · 저자 줄(Marburg) + 영점 줄(Giessen, Hertle → 16호 [24]) 의 16호 합류 — 이 편은 0 V 의 출처가 아니다.
- ★★★★ **Q7 판정**: 저자 기구 = 계면 면적 손실(void · Li 공공 확산) + 씨앗형 도금 → 국소 전류 → 덴드라이트, SEI 보류(XPS S 2p ≤6 at%), Li 소모 무관(`[재현]` ≤3 %). 단락 = "sudden voltage drop" 한 기준 · `[도표]` 붕괴 여러 계단 · 단락 전 계단 ×≈0.7 — 연성 단락 배제 0, 대칭셀은 OCV ≡ 0 이라 개방회로 서명 없음 · CE 통로 없음.
- **채움표 46호 행 — 누적 ≈19.5 → ≈19.5 (새 칸 0).** Q5 · Q2 반 칸 검토 후 접음 · Q4 0/46 서른여덟 번째 성질 · Q6 층 하나(감압 이력) · Q3 층 하나.
- 곱 축퇴 처방 **스물아홉 번째 적용**(Li 음극 계면): 4단계 ✅ 부분(`[재현]` DC 77–117 ↔ EIS 합 ≈24 Ω cm²) · 새 줄 후보 "역방향 반쪽 짝".
- 카드: Evidence 마흔두 번째 절 · 새 제약 4 · Status Log.
- ⚠ 어긋남 16 건(D1 Fig. 1 J·t 본문 ↔ 캡션 · D2 Fig. 4b 축 "µm" = 분 · D3 Li 면적 ≈0.16 cm² · D4 "10^10 F/cm²" · D6 Fig. 1e ↔ Fig. 8 · D9 Fig. 6 외).
- 낱말 지문: `contact loss` 1(Li 음극) · `MPa` 14 외 9 열 전부 0 · `leak` · `drift` · `calibrat` · `Coulomb*` · `soft` 0.
- 그림: **11 장 중 7 장 봤다**(Fig. 1 · 2 · 3 · 4 · 6 · 7 · 8), 안 본 것 Fig. 5 · 9 · 10 · 11.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]] · [[assb-li-in-reference-potential-window]](46호 절 · 계보 판정) · [[assb-lampe-contact-product-degeneracy]](스물아홉 번째 적용 · 처방 표 새 줄) · 큐 문서 §6-3-g 47 행 + 지문 ¹².
- 후속(서지 기준, 미열람 — 큐 48–59 인용 0): Kasemchainan … Bruce 2019 *Nat. Mater.* 18, 1105 (ref 13) · Krauskopf … Janek 2019 *ACS AMI* 11, 14463 (ref 14) · Bron, Roling, Dehnen 2017 *JPS* 352, 127 (ref 45) · Wenzel … Janek 2018 *SSI* 318, 102 (ref 38) · Wang, Sakamoto 2018 *JPS* 377, 7 (ref 51) · Xu … Greer 2017 *PNAS* 114, 57 (ref 54).

## [2026-09-23] ingest | assb 47호 — Solchenbach et al. 2016, A Gold Micro-Reference Electrode for Impedance and Potential Measurements in Lithium Ion Batteries (J. Electrochem. Soc. 163, A2265)
- raw: `raw/papers/solchenbach2016_gold-wire-micro-reference-electrode-liquid-t-cell.md` (sha256 봉인 — 본문 PDF 해시 frontmatter `pdf_sha256`, SI 없음) · 그림 `raw/figures/solchenbach2016_gold-wire-micro-reference-electrode-liquid-t-cell/` (8 장). 큐 48번(2차 묶음 아홉째 편) — 21호 ref 11 · 45호 ref [20]. ⚠ **액체셀**(LP57, Swagelok T-셀).
- ★★★ **Q5 판정**: 0.311 V = **Li 금속 대비 측정**(액체 Li\|Li) · LixAu(0 < x < ∼1.2) 첫 단 OCV · 150 nAh 절단면 리튬화 · >500 h 추적 `[도표]` 20 h 뒤 ≈3 mV(인쇄 < 2 mV) · 40 °C 리튬화 −1–2 mV · 25 → 40 °C ≈60 h 이탈 · 재리튬화 복원 · 누설 0/47(`[재현]` < ≈0.27 nA) — 스물세 번째 형태 "원전 측정 + 영점 사용 조건". 칸 반 칸 검토 후 접음(액체).
- ★★★★ **0.31 V ↔ 0 V = 같은 선의 맨 위 · 맨 아래 칸.** 45호 "21호 0.31 V 는 어느 칸도 아니다" 는 원전 사다리로 풀림. 45호가 [20] 에 단 134 / 215 mV 는 지면에 없음 — 칸 값 표가 둘(0.3 / 0.2 ↔ 0.215 / 0.134 V).
- ★★★★ **21호 교정 이식**: 가져간 것 = 값(두 자리) + 절차, 원전 조건 둘(노출 ×40 · 2 h 판독 = 초기 창 안) 이탈, 장기 안정성은 21호 자기 측정. 원장 "액체 값 → ASSB" 표현은 정밀하지 않음(21호 이식은 ASSB 안). "CE 거칠어짐" = "We believe"(셀 1, `[재현]` 0.77 nm).
- ★★ 3전극 아티팩트: 원전 기구 = 표류(≲1 Hz, PEIS 에서 완전지까지) + 위치 — 45호 >10 kHz 원인 후보 추가 0.
- **채움표 47호 행 — 누적 ≈19.5 → ≈19.5 (새 칸 0).** Q4 0/47 서른아홉 번째 성질 · Q3 층 하나 · Q2 해당 없음(도구 칸).
- 곱 축퇴 처방 **서른 번째 적용**(액체, 도구 칸): 1단계 τ 형 면적 서명 · 3-b "전하이동" ×700–1000(다섯 번째, 첫 액체) · 새 줄 "외부 기준 줄의 다섯 번째 배정 — 연구 간 비교".
- 카드: 채움표 행 · 47편 문단 · Evidence 마흔세 번째 절 · 새 제약 4 · Status Log.
- ⚠ 어긋남 12 건(D1 20 h ↔ ≈3 mV · D2 "quickly" · D4 대칭셀 −9/−21 % · D5 같은 상태 흑연 호 ×0.63 · D6 134/215 교차 편 · D7 "∼5-fold" ↔ 4.2 · D11 x ≤ 1.2 ↔ 축 확산 외).
- 낱말 지문: `MPa` 1(압연) 외 10 열 전부 0 · `calibrat` · `leak` · `pressure` 0 · `drift` 11.
- 그림: **8 장 다 봤다**, 화소 판독 Fig. 2b · 2c · 5 · 6a.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]] · [[assb-li-in-reference-potential-window]](47호 절 · 조건 (10)) · [[assb-lampe-contact-product-degeneracy]](서른 번째 적용 · 처방 표 새 줄) · 큐 문서 §6-3-g 48 행 + 지문 ¹³.
- 후속(서지 기준, 미열람 — 큐 49–59 인용은 52 Illig 2012 하나): Bach … Renner 2015 *Electrochim. Acta* 164, 81 (ref 25) · Bach … Renner 2016 *Chem. Mater.* 28, 2941 (ref 30) · Ender, Weber, Ivers-Tiffée 2012 *JES* 159, A128 (ref 14) · Dees, Jansen, Abraham 2007 *JPS* 174, 1001 (ref 15) · Victoria, Ramanathan 2011 *Electrochim. Acta* 56, 2606 (ref 17).

## [2026-09-23] ingest | assb 48호 — Dugas et al. 2021, Engineered Three-Electrode Cells for Improving Solid State Batteries (J. Electrochem. Soc. 168, 090508)
- raw: `raw/papers/dugas2021_engineered-three-electrode-cell-assb-li-in-reference-layer.md` (sha256 봉인 — 본문 PDF 해시 frontmatter `pdf_sha256`, SI 없음) · 그림 `raw/figures/dugas2021_engineered-three-electrode-cell-assb-li-in-reference-layer/` (10 장). 큐 49번(2차 묶음 열째 편) — 21호 ref 16.
- ★★★★ **기하 정정**: 기준극은 링이 아니라 **WE 와 CE 사이 단면 전체를 덮는 Li₀.₅In : SE 60 : 40 복합층** — 링은 15 µm Al 집전체. 21호 "circular … around the outer perimeter" · 원장 "원형 InLi 기준극" 은 집전체를 읽었다. `[해석]` 기준극이 전류 경로 안 → 쌍극 교환 가능성(조건 (11), 크기 C/20 급 mV 이하 추정).
- ★★★ **Q5 판정 — 스물네 번째 형태**: 영점 = 인용 622 mV(42호)를 2전극 귀속 전제로 한 번 · 3전극 축은 끝까지 "vs LiIn/In"(환산 0) · 기준극 33.3 at%(창 안) · `[인쇄]` CE 창 ±160 → ±20 mV + "20 mV ↔ ⩽2 mA h g⁻¹ … 2 electrodes … can safely be employed" = 계보 첫 "상대극 창 → 용량 오차 → 2전극 허용" 규칙 · 안정성 "hundreds of hours"(수 0) · 누설 0/48 · `[도표]` Fig. 10a Li 박 상대극 휴지 끝 −0.62 ± ≈0.01 V vs LiIn/In(우리 판독, 본문 미판독).
- ★★★ **21호 인용 셋**: 기하 ❌ · 저주파 변화 "expected" ⚠ 약한 판(Li-In = 시간 단조 성장, 방향 의존은 Li 금속) · 음극 저주파 호 = 전하이동 ❌.
- ★★★ **2전극 재구성 = 비식별성 시연**(WE 모형이 합을 "satisfactory" 적합, 중간 호 139 → 307 Ω cm², "cannot be decorrelated") · 호 제거 검정 문장. 검증은 양의 Im 호 부재 한 기준, 기준극 없는 셀 EIS 대조 0.
- **채움표 48호 행 — 누적 ≈19.5 → ≈20.0 (Q5 +0.5).** Q4 0/48 마흔 번째 성질 · Q3 층 하나 · Q6 층 하나 · Q1 `θ(N)` 0/48.
- **곱 축퇴 처방 서른한 번째 적용**: 3-b 느린 "전하이동" 두 호 실패(여섯 번째 계열) · 4단계 부분(Li CE) · 새 줄 "호 제거 검정 + 2전극 합 재구성".
- ⚠ 어긋남 15 건(D1 1.9 ↔ ≈0.2 mS cm⁻¹ · D2 33 ↔ 23 % · D4 Fig. 6c = 8c · D7 540 ↔ 670 mHz · D8 압력 단정 교락 · D9 겹침 ↔ 다른 패널 · D12–D15 교차 편 외).
- 낱말 지문: `calibrat` 1(토크 ↔ 압력) 외 10 열 0 · `leak` · `drift` · `assum*` 0 · `expect*` 4 · `622` 1.
- 그림: **10 장 다 봤다**, 화소 판독 Fig. 3a · 5c · 7 · 9a · 10a.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]] · [[assb-li-in-reference-potential-window]](48호 절 · 조건 (11) · P8 · P11) · [[assb-lampe-contact-product-degeneracy]](서른한 번째 적용 · 처방 표 새 줄) · 큐 문서 §6-3-g 49 행 + 지문 ¹⁴.
- 후속(서지 기준, 미열람 — 큐 50–59 인용 0): Costard … Ivers-Tiffée 2017 *JES* 164, A80 (ref 15, 두 번째 지목) · Ender, Illig, Ivers-Tiffée 2017 *JES* 164, A71 (ref 6) · Kasemchainan … Bruce 2019 *Nat. Mater.* 18, 1105 (ref 8) · Marchini … Tarascon 2020 *ACS AMI* 12, 15145 (ref 18) · Kaiser … Roling 2018 *JPS* 396, 175 (ref 23).

## [2026-09-23] ingest | assb 49호 — Barai et al. 2018, A study of the influence of measurement timescale on internal resistance characterisation methodologies for lithium-ion cells (Sci. Rep. 8, 21)
- raw: `raw/papers/barai2018_measurement-timescale-internal-resistance-methods.md` (sha256 봉인 — PDF 해시 frontmatter `pdf_sha256`, SI 없음) · 그림 `raw/figures/barai2018_measurement-timescale-internal-resistance-methods/` (7 장). 큐 50번(2차 묶음 열한째 편) — 20호 ref [24]. ⚠ 액체셀(상용 20 Ah LFP/흑연 파우치) — 도구 칸.
- ★★★★ **판정**: 총량은 **같은 양의 다른 창**(`[재현]` 5 C 펄스 ↔ EIS |Z|(t = 1/f) −6 … +11 %) · 성분 이름(`R₀`/`R_CT`/`R_p`)은 **창 경계의 규약**(방법 간 ×2.0 · ×2.9 · ×13, EIS `R_p` 경계만 ×3.9) · 옳은 창은 `R₀` 에만("after 4ms") · 10 Hz 장비 `R₀` +43 % = |Z|(10 Hz).
- ★★★ **식별**: 비유일성 두 곳(ECM · DC 분해) 인쇄 → 결론이 지움 — Q4 마흔한 번째 성질. `[해석]` 적합된 직렬 R = 여기 대역 위쪽 끝의 |Z|.
- ★★★ **20호 대조**: 모양 규칙(원전 Fig. 1 모식의 선형 외삽 · "shallow, linear")은 가져갔고 시간 규약(0.1 · 2 · 10 s, 5 C, 50 % SoC, 4 h 휴지)은 두고 왔다 — `R_CT` 창 ×10³, 원전 규약으로 ≈0.28 mHz. "작도다" 판정은 원전에서도 선다. 규약 출처 = 원전 ref 8 Waag 2013(20호 [25]).
- ⚠ 결론 긴장: "not the non-linearity" ↔ 10 s 창 진폭 ×1.46 · 대진폭 다중사인 −24 % @ ≈0.017 Hz · 다중사인 총 2.83 = ω→0 외삽.
- **채움표 49호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q4 0/49 마흔한 번째 성질 · Q3 층 둘 · Q2 해당 없음(도구 칸).
- **곱 축퇴 처방 서른두 번째 적용**: 4단계 ✅ 총량 · 3-b 판정 불가 · 새 줄 "창 규약".
- ⚠ 어긋남 15 건(D4 Re ↔ |Z| 혼용 · D5 결론 "separation and identification" ↔ "not well-defined" · D6 진폭 · D10 0.01 ↔ ≈0.017 Hz 외).
- 낱말 지문: `identifiab` 3(파라미터 뜻 2) · `uncertaint` 1 · 나머지 9 열 0 · `timescale` 20 · `window` 0.
- 그림: **7 장 다 봤다**, 화소 판독 Fig. 5a · 5b · 6a · 7b.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]] · [[assb-lampe-contact-product-degeneracy]](서른두 번째 적용 · 처방 표 새 줄) · [[assb-sensitivity-sweep-vs-identifiability]](49호 절 · 처방 13) · 큐 문서 §6-3-g 50 행 + 지문 ¹⁵.
- 후속(서지 기준, 미열람 — 큐 51–59 인용 0): **Waag, Käbitz, Sauer 2013 *Applied Energy* 102, 885** (ref 8, 두 번째 지목) · Schweiger et al. 2010 *Sensors* 10, 5604 (ref 22) · Widanage et al. 2016 *JPS* 324, 61 · 70 (refs 21 · 20) · Barai et al. 2015 *JPS* 280, 74 (ref 18) · Smith & Wang 2006 *JPS* 161, 628 (ref 28).

## [2026-09-23] ingest | assb 50호 — Miß, Ramanayagam, Roling 2022, Which Exchange Current Densities Can Be Achieved in Composite Cathodes of Bulk-Type All-Solid-State Batteries? A Comparative Case Study (ACS Appl. Mater. Interfaces 14, 38246)
- raw: `raw/papers/miss2022_exchange-current-density-tlm-thickness-lco-nmc-assb.md` (sha256 봉인 — 본문 `pdf_sha256` · SI `si_sha256`) · 그림 `raw/figures/miss2022_exchange-current-density-tlm-thickness-lco-nmc-assb/` (15 장 + 표 4). 큐 51번(2차 묶음 열두째 편) — 16호 ref [30], 16호 TLM 방법의 원본.
- ★★★★ **판정**: 면적 = 완전구 기하 `a_v = 3ε/r`(`[인쇄]` "in contact to SE" — 16호 문장의 출생지, `r_CAM` 2.5 µm 는 SEM 공칭 확인) — **`j₀` 와 면적을 가르지 않았다**. 두께 가변은 `R_ion` ↔ `R_CT/(a_v d)` 만(NMC 전이 통과 · LCO 전부 두꺼운 극한). `[재현]` 수정 (ii) `a_v·τd → a_v·d` = `j₀` ×τ 정확한 재척도(식 1 이면 LCO 25.8 → 4.2 · NMC 0.11 → 0.016 A m⁻²).
- ★★★ **비교**: 같은 지면 LCO ↔ NMC τ_CT ×106(면적 서명 아님 — 견딘다) · 16호 ↔ 이 편 NMC τ ×1.28(면적 서명 — 16호 SE 전도도 서사가 곱을 안 가름) · 3-b ✅ 4.4 · 2.0 µF cm⁻².
- ★★★ **16호 대조**: `r_CAM` 공칭 확인 · 초기값 문헌(Kaiser 2018 τ) + 1/30 C · `ε` 0.505/0.495 = 이 편 LCO 칸 · "기공 구조" 이유는 16호의 것 · 비교 대상 `j₀` = 0.11.
- **채움표 50호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q4 0/50 마흔두 번째 성질 "면적 규약을 적합 개선으로 골랐다" · Q5 스물다섯 번째 형태 "대칭셀 반 빼기"(반 칸 검토 후 접음) · Q3 simulation-matched.
- **곱 축퇴 처방 서른세 번째 적용**: 1단계 ✅(같은 지면 · 편 간) · 3-b ✅ · 새 줄 "면적 정규화 규약".
- ⚠ 어긋남 14 건(D1 첫 방전 ≈170 ↔ "180−200" · D6 SI σ_ion ⇒ τ ≈3.0 ↔ 6.8 · D7 Fig. 5a 과차감 · D9 LCO 모형 두께 추세 "unclear" · D13 refs 30 = 33 외).
- 낱말 지문: 11 열 중 `MPa` 8(SI 1) 외 0 · `simulat*` 19 · `fit*` 4(`j₀` 밖).
- 그림: 15 장 중 **12 장 봤다**(Fig. 2–8 · S2 · S3 · S5 · S6 · S7), 안 본 것 Fig. 1 · S1 · S4 · 식은 쪽 렌더.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]] · [[assb-lampe-contact-product-degeneracy]](서른세 번째 적용 · 처방 표 새 줄) · [[spm-grouped-parameter-identifiability]](50호 두 행) · 큐 문서 §6-3-g 51 행 + 지문 ¹⁶.
- 후속(서지 기준, 미열람 — 큐 52–59 인용: 57 Bielefeld 2022 만): Kaiser … Roling 2018 *JPS* 396, 175 (ref 24) · Cronau … Roling 2020 *Batter. Supercaps* 3, 611 (ref 36) · Hess … Cuniberti 2015 *JPS* 299, 156 (ref 31) · Minnmann … Janek 2021 *JES* 168, 040537 (SI ref 4) · Morasch … Suthar 2021 *JES* 168, 080519 (ref 34).

## [2026-09-23] ingest | assb 51호 — Illig, Ender, Chrobak, Schmidt, Klotz, Ivers-Tiffée 2012, Separation of Charge Transfer and Contact Resistance in LiFePO4-Cathodes by Impedance Modeling (J. Electrochem. Soc. 159, A952)
- raw: `raw/papers/illig2012_charge-transfer-contact-resistance-lfp-drt-ecm.md` (sha256 봉인 — `pdf_sha256`) · 그림 `raw/figures/illig2012_charge-transfer-contact-resistance-lfp-drt-ecm/` (자동 9 + 수동 7 + 표 2). 큐 52번(2차 묶음 열셋째 편) — 18호 [29] · 11호 [9] · 47호 [35]. ⚠ 액체셀(도구 칸).
- ★★★★ **판정**: "접촉 저항" = 양극층 | Al 집전체(전자 접촉) — 카드의 CAM|SE `θ` 와 다른 물리. 가른 것은 한 호 안의 곱이 아니라 **직렬 두 호(P1C ↔ P2C)의 이름**: DRT 대역 · 대칭셀 · `Ea` 0.45 ↔ 0.06 eV(주 판별자) · SOC = 측정, 이름 = 가정("always temperature activated") + 소거 + 문헌. 캘린더링 한 쌍은 방향만(네 원인 동시).
- ★★★ `[재현]` Table I → `C` P2C ≈1 µF · P1C ≈3 mF cm⁻²(×≈3,000; 표 주파수 열 순서 뒤집어야, D1) · `[도표]` 캘린더링 τ P1C ×≈3.5 · P2C ×≈1/6 · Fig. 15 도식 P2C CPE → 비접촉 집전체 ⇒ 전자 접촉 호의 `C` 는 여집합(1단계 전제 부호 반전).
- ★★★ **ASSB 이식**: 방법 형태 ✅ · 판별값 ❌ — 18호 R2(Al|복합체) `Ea` 41–70 kJ mol⁻¹ ↔ R3 49–63 겹침. **가져간 것**: 18호 DRT 참고문헌만 · 11호 대역만(정체 근거인 온도는 두고 옴) · 47호 R‖CPE 하나로 두 호를 다시 합침.
- **채움표 51호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q4 0/51 마흔세 번째 성질 · Q3 DRT-seeded ECM.
- **곱 축퇴 처방 서른네 번째 적용**: 1단계 부분 · 3-a ✅ · 3-b ✅ · 새 줄 "`C` 의 자리 · `Ea` 판별값은 계 고유".
- ⚠ 어긋남 11 건(D1 F_R 순서 · D2 Pdiff `Ea` 미인쇄 · D3 "± 50" = 범위 · D4 질량수지 ×0.83 · D7 "without any a priori settings" · D9 DRT 정규화 외).
- 낱말 지문: 11 열 전부 0 · `contact` 20(전부 집전체) · `capacit*` 21(RQ 커패시턴스 0) · `double layer` 0.
- 그림: 크롭 Read 8 장(Fig. 9 · 10 · 12 · 13 · 14 · 15 · 16 · Table I), 쪽 미리보기만 Fig. 5–8 · Table II, 안 봄 Fig. 1–4 · 11.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]] · [[assb-lampe-contact-product-degeneracy]](서른네 번째 적용 · 처방 표 새 줄) · 큐 문서 §6-3-g 52 행 + 지문 ¹⁷.
- 후속(서지 기준, 미열람 — 큐 53–59 인용 0): **Gaberscek … Jamnik 2008 *ESSL* 11, A170** (ref 11) · Schmidt … Ivers-Tiffée *JPS* 196, 5342 (ref 19) · Illig … Ivers-Tiffée 2010 *ECS Trans.* 28(30), 3 (ref 17) · Levi & Aurbach 1997 *J. Phys. Chem. B* 101, 4630 (ref 23).

## [2026-09-23] ingest | assb 52호 — Oh, Kwon, Choi, Lee, Sohn, Lee, Lee, Kim, Bae, Choi 2025, All-Solid-State Batteries with Extremely Low N/P Ratio Operating at Low Stack Pressure (Adv. Energy Mater. 15, 2404817)
- raw: `raw/papers/oh2025_mgsigr-overcharge-low-np-ratio-low-pressure-assb.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/oh2025_mgsigr-overcharge-low-np-ratio-low-pressure-assb/` (본문 7 + SI 25 + 표 2). 큐 53번(2차 묶음 열넷째 편) — 13호 [34] · 14호 [10], 14호와 같은 연구실(서울대 + HMG-SNU JBRC + 현대차).
- ★★★★ **Q6 판정**: 운전 20 · 3 MPa(스프링, 상수 · 계측 0) · 파우치 3 MPa(볼트 3.5 N·m, 변환 0) ↔ 제조 150 · 380 · WIP 450 MPa 명시 — **압력 비교 없음**: 두 점이 양극 적재 20 ↔ 6 mg cm⁻² · N/P 0.15 ↔ 0.66 과 교락, 반쪽 압력 미인쇄. 저압 "most critical factor"(음극 계면)는 3 MPa 고정 음극 교체로만, MgSiGr 저압 감쇠 원인은 해석 한 줄, 양극 관측 0. 제목의 두 조건은 한 셀에서 안 만난다.
- ★★★★ **용량 제한 전극 · 배정 없음**(2전극, `LLI` · `LAM` 0, 방전 끝 판정 불가). `[재현]` **CE ≠ `LLI`**: 20 MPa 평균 99.2 % ↔ 83.7 %(결손 ≈95 ↔ 손실 ≈27) · 3 MPa `[도표]` CE ≈85–97 %(본문 0), 누적 결손 ≈575 mAh g⁻¹ > NCM811 재고 ≈275 · 면적당 ×≈1.8.
- **채움표 52호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q6 반 칸 검토 후 접음 · Q4 0/52 마흔네 번째 성질 · Q3 층 하나.
- **곱 축퇴 처방 서른다섯 번째 적용**: 1–4단계 ❌ · 새 줄 "누적 충–방 결손 ↔ Li 재고 상한".
- ⚠ 어긋남 14 건(D1 제목 두 조건 · D2 완전지 N/P 재현 불가 · D3 `R_B` "tolerance" · D5 3 MPa CE · D6 99.2 ↔ 83.7 · D8 압력 제어 근거 0 외).
- 낱말 지문: `LLI` · `LAM` · `identifiab` · `calibrat` 0 · `contact loss` 1(음극) · `MPa` 13(SI 2) · `dead` · `reservoir` · `leak` 0.
- 그림: 34 장 중 14 장 Read(Fig. 1–6 · S11 · S15 · S17 · S19 · S23 · S25 · 표 S1 · S2), 화소 판독 Fig. 4D · 6D, 안 봄 20 장.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 52편 · Evidence 마흔일곱 번째 · 새 제약 · Status Log) · [[assb-lampe-contact-product-degeneracy]](서른다섯 번째 적용 · 처방 표 새 줄) · [[assb-stack-pressure-operating-window]](52호 절) · [[anode-free-li-inventory-accounting]](52호 절) · 큐 문서 §6-3-g 53 행 + 지문 ¹⁸.
- 후속(서지 기준, 미열람 — 큐 54–59 인용 0): Oh … Choi 2024 *ESM* 71, 103606 (ref 12b) · Oh … Choi 2023 *AEM* 13, 2301508 (ref 12c) · Menkin … Grey 2024 *Faraday Discuss.* 248, 277 (ref 23) · Chen … Li 2021 *ACS AEM* 4, 4879 (ref 16a) · Yan … Chen 2022 *AEM* 12, 2102283 (ref 16b).

## [2026-09-23] ingest | assb 53호 — Ren, Danner, Moy, Finsterbusch, … Latz, Srinivasan, Janek, Sakamoto, Wachsman, Fattakhova-Rohlfing 2023, Oxide-Based Solid-State Batteries: A Perspective on Composite Cathode Architecture (Adv. Energy Mater. 13, 2201939)
- raw: `raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/ren2023_oxide-ssb-composite-cathode-architecture-perspective/` (크로퍼 13 + 수동 SI-1 · SI-2). 큐 54번(2차 묶음 열다섯째 편) — 02호 ref 17. ⚠ Perspective, 1차 기여는 P2D 사례 계산 하나.
- ★★★★ **Q1 판정**: `θ(N)` 0/53 — 자기 P2D `θ ≡ 1`(퍼콜레이션 · 치밀 · 열화 무시 인쇄) · 공백을 인쇄("There is yet no experimental study that incorporates percolation theory and its influence on mechanical degradation"). "시간축의 입구" 뒤 = Barai 2021 [127] 사이클 축 박리 모델 하나 + 산화물 용량 곡선 재인용 넷(접촉 분율 0).
- ★★★★ **산화물 시점**: 제조(냉각 응력 모의 ≈1 GPa ↔ LLZO 100–150 MPa, "possible") → `θ₀` 공정 변수 · 운전("fatigue", 인용 0). ★★★ 시간 배정 역전(인용 [103] = 23호 반대) — 33호에 앞선 첫 역전. [105] FAST/SPS 치밀 셀 = 기계 기구 배제 대조(재인용).
- ★★★ **모델 대조(37호)**: `a` 미정의 · `ε_CAM` 고정 · 접촉 자리 = `a·i₀₀` + `a/R_SP`(세 번째 곱). `[재현]` improved 체제에서 면적형 접촉 손실 전압 비가시(≈0.7 mV).
- **채움표 53호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q4 0/53 마흔다섯 번째 성질 · Q3 층 하나(계 간 이식) · Q2 반 칸 검토 후 접음.
- **곱 축퇴 처방 서른여섯 번째 적용**: 1–4단계 ❌ · 새 줄 "전류 진폭 — 직렬 `R_SP` ↔ `R_CT`".
- ⚠ 어긋남 15 건(D1 state-of-the-art 24 · 15 ↔ 그림 ≈120 · ≈115 ↔ SI ≈112 · D2 시간 배정 · D4 Fig. 7d 사이클 0 · D8 In-Li ↔ Li · D9 κ_eff ×10 · D14 결론 "cracks" 외).
- 낱말 지문: 11 열 중 `contact loss` 5(황화물 4) · `MPa` 7(응력 6) 외 0.
- 그림: 15 장 중 Read 7(Fig. 1 · 4 · 5 · 7 · 9 · SI-1 · SI-2), 안 봄 Fig. 2 · 3 · 6 · 8, 표는 텍스트.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 53편 · Evidence 마흔여덟 번째 · 새 제약 · Status Log) · [[assb-lampe-contact-product-degeneracy]](서른여섯 번째 적용 · 처방 표 새 줄) · [[assb-interphase-vs-contact-loss-attribution]](계보 표 53호 행) · [[assb-sensitivity-sweep-vs-identifiability]](53호 절) · 큐 문서 §6-3-g 54 행 + 지문 ¹⁹.
- 후속(서지 기준, 미열람 — 큐 55 · 57 · 58 인용, 56 · 59 0): Barai … Srinivasan 2021 *Chem. Mater.* 33, 5527 ([127]) · Ihrig … Guillon 2021 *JPS* 482, 228905 ([105]) · Tsai … Guillon 2019 *Sustain. Energy Fuels* 3, 280 ([83]) · Neumann … Latz 2020 *ACS AMI* 12, 9277 ([32]) · Finsterbusch, Danner … 2018 *ACS AMI* 10, 22329 ([12]).

## [2026-09-23] ingest | assb 54호 — Neumann, Hamann, Danner, Hein, Becker-Steinberger, Wachsman, Latz 2021, Effect of the 3D Structure and Grain Boundaries on Lithium Transport in Garnet Solid Electrolytes (ACS Appl. Energy Mater. 4, 4786)
- raw: `raw/papers/neumann2021_garnet-3d-structure-grain-boundary-transport.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/neumann2021_garnet-3d-structure-grain-boundary-transport/` (본문 12 + 표 1 + SI 9 + 표 5). 큐 55번(2차 묶음 열여섯째 편) — 지목 3 회(02호 ref 38 · 27호 ref 14 · 53호 [27]). ⚠ 양극 없음 — LLCZNO SE 자체, 모델(BEST) + 재사용 자료. ⚠ Neumann 2020 *ACS AMI* 와 다른 편.
- ★★★★ **판정**: 굴곡도 = FIB-SEM 구조 계산(곱 `σ⁰·ε/τ²` 풀림) · 벌크 `σ⁰` = 외부 입력(벌크 절편 대역 밖, `f_C,B` 1.40e7 ↔ 상한 1.5e7) · 입계 `i₀₀^GB` · `C_DL^GB` = 재사용 치밀 펠릿 한 스펙트럼 위 손 보정(가정 입도 15 ± 6 µm). 남은 합 벌크 ↔ 입계는 원문이 "exact deconvolution … unfeasible" 두 번 인쇄.
- ★★★★ **원장 "measured 라벨" ❌** — Table S4 범례 "measured by the authors [°]" 표시 0 개, 전부 "calculated". ★★★ 53호 `β_tort` 2.31 · `β_GB` 1.39 는 이 편에 없음 — `[재현]` 2.31 = 56 % 한 점, 1.39 는 치밀 정규화에서만 근처 → 53호 `σ⁰` 뜻 어긋남(×≈0.27).
- **채움표 54호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q3 새 층(재사용 스펙트럼 위 손 보정) · Q4 0/54 마흔여섯 번째 성질.
- **곱 축퇴 처방 서른일곱 번째 적용**: 1단계 `C` 두께 불가(`[재현]` 등가 ≈6.8 µm) · 3-a ❌ · 4단계 모델에만(ASR 1064 → 655) · 새 줄 "벌크 특성 주파수 ↔ 측정 대역 상한".
- ⚠ 어긋남 20 건(D3 [°] 0 · D2 `R` = 뤼드베리 상수 · D1 "β-LPS" · D6 "25%" ↔ +33 % · D7 7.56e-5 ↔ 1.1e-4 · D15 `C` 단위 비교 · D19 "fluctuates" ↔ 단조 감소 외).
- 낱말 지문: 11 열 중 `MPa` 1(문헌 Li 음극) 외 0 · `deconvol*` 1/1 · `unfeasible` 1/1 · `activation` · `Arrhenius` 0.
- 그림: 27 장 중 Read 9(Fig. 4 · 5 · 6 · 7 · 8 · S1 · S4 · S5 + 표 S4), 안 봄 Fig. 1–3 · 9–12 · S2 · S3 · S6–S9, 나머지 표는 텍스트.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 54편 · Evidence 마흔아홉 번째 · 새 제약 · Status Log) · [[assb-lampe-contact-product-degeneracy]](서른일곱 번째 적용 · 처방 표 새 줄) · [[assb-tortuosity-factor-effective-conductivity-split]](다섯 번째 표본) · [[assb-sensitivity-sweep-vs-identifiability]](54호 절 · 처방 14) · 큐 문서 §6-3-g 55 행 + 지문 ²⁰.
- 후속(서지 기준, 미열람 — 큐 56–59 인용 0): Hamann … Wachsman 2020 *Adv. Funct. Mater.* 30, 1910362 ([30]) · Han … Hu 2016 *Nat. Mater.* 16, 572 ([9]) · Fleig & Maier 1999 *J. Eur. Ceram. Soc.* 19, 693 ([63]) · Irvine 1990 *Adv. Mater.* 2, 132 ([61]) · Hein … Latz 2020 *JES* 167, 013546 ([34]).

## [2026-09-23] ingest | assb 55호 — Hlushkou, Reising, Kaiser, Spannenberger, Schlabach, Kato, Roling, Tallarek 2018, The influence of void space on ion transport in a composite cathode for all-solid-state batteries (J. Power Sources 396, 363)
- raw: `raw/papers/hlushkou2018_void-space-ion-transport-composite-cathode.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/hlushkou2018_void-space-ion-transport-composite-cathode/` (자동 8 + 측면 캡션 수동 3). 큐 56번(2차 묶음 열일곱째 편) — 01호 ref 16 지목. LCO(LiNbO₃)/비정질 LPSI, 탄소 없음 · Marburg(Roling · Tallarek) + KIT KNMF + Toyota.
- ★★★★ **판정**: 부피분율 측정(FIB-SEM 35.6 nm × 100 nm — LCO 33.1 · SE 53.7 · void 13.2 %, ⚠ void = 수지 + 잔류 void) · 연결성 · 접촉 면적 0(`θ` · `φ` · `u` 아님) · void 의 경로 효과만 가상 치환으로 계산(`τ` 1.74 → 1.27, `[재현]` `ε/τ` ×1.71, 로그 몫 `τ` 59 %).
- ★★★★ **실측 대조는 `τ` 로** — `τ_cond` 1.6 ± 0.1 ↔ `τ_diff` 1.74 "close"; EIS 쪽 `ε` 미인쇄, `[재현]` 관측 곱 0.406 ↔ 모의 0.309(×1.31), EIS 시편 void 미측정 · 시편 차 넷 중 "수지" 하나에 배정 ⇒ 구조가 곱을 푸는 것은 같은 시편일 때. 01호 기대 절반(같은 양 대조 불가).
- **채움표 55호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q3 층 하나 · Q4 0/55 마흔일곱 번째 성질.
- **곱 축퇴 처방 서른여덟 번째 적용**: 2단계 부분(디지털 치환 = 대조군의 계산판, 수송만) · 4단계 ❌ · 새 줄 "두 경로 대조는 관측 곱 `σ_eff/σ⁰` 로, 같은 시편 · 같은 `ε` 로".
- ⚠ 어긋남 9 건(D5 `τ_cond` ↔ `[재현]` 1.53 · D7 "void" = 수지 + void · D2 "relative 13%" ↔ +24.6 % · D3 Bruggeman 1.34 ↔ 1.365 · D6 유한 크기 "all phases" ↔ SI 예외 외).
- 낱말 지문: 11 열 중 `MPa` 1(SE 펠릿) 외 0 · `void*` 43/6 · `percolat*` · `connect*` · `surface area` 0 · `manual*` 0/3(SI 만).
- 그림: 그림 8 장 전부 Read(Fig. 1 은 쪽 렌더), 표는 텍스트.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 55편 · Evidence 쉰 번째 · 새 제약 · Status Log · 비주장) · [[assb-lampe-contact-product-degeneracy]](서른여덟 번째 적용 · 처방 표 새 줄) · [[assb-tortuosity-factor-effective-conductivity-split]](여섯 번째 표본) · [[composite-cathode-percolation-utilization]](1호 ref 16 기대 판정) · 큐 문서 §6-3-g 56 행 + 지문 ²¹.
- 후속(서지 기준, 미열람 — 큐 57–59 는 이 편보다 늦어 인용 0): Thorat … Wheeler 2009 *JPS* 188, 592 ([22]) · Landesfeind … Gasteiger 2016 *JES* 163, A1373 ([13]) · Siroma … Ioroi 2016 *JPS* 316, 215 ([19]) · Asano … Tatsumisago 2017 *JES* 164, A3960 ([20]) · Müllner … Tallarek 2014 *Mater. Today* 17, 404 ([31]) · 같은 권 Kaiser … Roling 2018 *JPS* 396, 175 (인용 0).
