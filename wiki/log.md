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
