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
