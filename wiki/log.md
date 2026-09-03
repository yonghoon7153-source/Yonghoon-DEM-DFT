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
