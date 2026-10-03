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

## [2026-09-23] ingest | assb 56호 — Bielefeld, Weber, Rueß, Glavas, Janek 2022, Influence of Lithium Ion Kinetics, Particle Morphology and Voids on the Electrochemical Performance of Composite Cathodes for All-Solid-State Batteries (J. Electrochem. Soc. 169, 020539)
- raw: `raw/papers/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem/` (자동 17 + SI 벡터 수동 2). 큐 57번(2차 묶음 열여덟째 편), 지목 4 회(02 · 14 · 50 · 53호). ⚠ FEM 모델 편 — 새 측정 0.
- ★★★★ **판정**: void 는 **접촉(`φ`) 자리에만**(1-입자 표면 반구, 피복률 100 → ≈52 % · 크기 비 1.2–10) — 경로 효과 구성상 0, 검증 모델은 실험 void 14 % 를 SE 로 채움 · 둘을 갈랐나 ❌ · **`θ` 는 손으로 1**(SI: 01호대로면 42 vol% 는 문턱 아래 → placeholder + "moved manually") · **"pore 문턱 → 저항 급증"(원장 · 14호 [69]) 은 이 편에 없다**(`threshold` · `surpass` 0).
- ★★★★ **`j₀` 는 입력** — Rueß 2020 `R_CT` → 식 (12), `A` 미정의 ⇒ 50호 "10⁻⁵ A cm⁻² ≈ NMC 0.11" 은 EIS ↔ EIS, 규약 판정 불가(`[재현]` ASR ≈112 ↔ ≈1520 Ω cm²). 실험 대조 = 남의 첫 충전 3 율, 오차 척도 0, 본문 "best" 는 상수 세트(결론과 어긋남).
- ★★★ **모델 명제**: 피복은 0.02 C 에서 ≤ ≈7 mV · −3 %, 0.5 C 에서 −25 % · `φ` 70 % 고정에서 크기만으로 ×2.6–4.5 · `[재현]` BV 면적 몫 ≈44 % ⇒ 37호 `A_eff ↔ k` 항등이 3D 에서 부분 파괴. `θ`-전용 조작 ❌.
- **채움표 56호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 층 하나(모델 명제) · Q3 층 하나 · Q4 0/56 마흔여덟 번째 성질 · Q8 층 하나(02호 `U₀` 경유지).
- **곱 축퇴 처방 서른아홉 번째 적용**: 2단계 모델판 둘 · 율 스윕 줄 모델 확인 · 새 줄 "`φ` 고정 분포 스윕 — 3D 모델에서 `A_eff ↔ k` 항등의 파괴 검사".
- ⚠ 어긋남 14 건(D2 "none fitted" ↔ PSD 선택 · D3 "best" ↔ "not capable" · D4 void 4 ↔ `[재현]` 5.8 µm · D5 0.5 C 점 없음 · D7 void 14 % ↔ 0 % · D12 · D13 계보 귀속 · D1 `T` 273.15 K 외).
- 낱말 지문: 11 열 중 `uncertaint` 1 · `contact loss` 5 외 0 · `Achilles` 1 · `caution` 1 · `percolat*` 2/6 · `manual*` 0/2.
- 그림: Read 11 장(Fig. 2 · 4 · 5 · 6 · 7 · 8 · 9 · 10 · S3 · S2 · S7) + S5 쪽 렌더, 안 봄 Fig. 1 · 3 · 11 · S1 · S4 · S6 · S8.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 56편 · Evidence 쉰한 번째 · 새 제약 · Status Log) · [[assb-lampe-contact-product-degeneracy]](서른아홉 번째 적용 · 처방 표 새 줄) · [[composite-cathode-percolation-utilization]](01호 `p_c` 반례 · 수작업 강제) · [[assb-apparent-capacity-decomposition]](`η(i)` 모델 표본) · 큐 문서 §6-3-g 57 행 + 지문 ²².
- 후속(서지 기준, 미열람): Ruess … Janek 2020 *JES* 167, 100532 ([10] — 모든 입력의 원전) · Bielefeld · Weber · Janek 2020 *ACS AMI* 12, 12821 ([25] = 큐 58) · Minnmann … Janek 2021 *JES* 168, 040537 ([27]) · Neumann … Latz 2020 *ACS AMI* 12, 9277 ([38]) · Trevisanello … Janek 2021 *AEM* 11, 2003400 ([11]).

## [2026-09-23] ingest | assb 57호 — Bielefeld, Weber, Janek 2020, Modeling Effective Ionic Conductivity and Binder Influence in Composite Cathodes for All-Solid-State Batteries (ACS Appl. Mater. Interfaces 12, 12821–12833)
- raw: `raw/papers/bielefeld2020_effective-ionic-conductivity-binder-composite-cathode.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/bielefeld2020_effective-ionic-conductivity-binder-composite-cathode/` (자동 13, 제외 1). 큐 58번(2차 묶음 열아홉째 편), 지목 3 회(15 · 24 · 53호) + 56호 ref 25. ⚠ 모델 편(GeoDict + EJ-heat 정상 전도) — 새 측정 0.
- ★★★★ **판정**: "pore(void) 문턱 → 저항 급증"(14호 [69] 가 56호에 붙인 문장)은 **이 편에도 없다** — void 스윕은 5 · 10 · 20 % 세 점 단조(`σ_eff` ×≈2), `threshold` 0, 급변은 AM 분율 축뿐. 01 · 56 · 58 어디에도 세 요소가 함께 없다 ⇒ **귀속 출처 불명**.
- ★★★★ **유효 전도도**: 곱 `σ⁰·ε/τ²` 는 구성상 풀림 · `τ²` = `σ⁰ε/σ_eff` 이름표 · Bruggeman ×4 과소 · 검증은 Kato 2018 한 점(void 15 % 가정, 곱 비 1.07 ↔ void 손잡이 ×2). **바인더** = `θ_AM` 불변(구성상) · `A_spec,a` ↓ 17–82 % · `σ_eff` ↓ · `θ_SE` ↓ — `A_eff·k` · `κ_eff` 두 자리를 한 손잡이로(모델 명제). **`p_c` 계보** 01 → 58(무언 재현, 49 → 50 vol%) → 56(반례 · 수작업).
- **채움표 57호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 층 하나(모델 명제) · Q3 층 하나 · Q4 0/57 마흔아홉 번째 성질.
- **곱 축퇴 처방 마흔 번째 적용**: 새 줄 "한 공정 손잡이가 두 곱을 같이 깎을 때 — 면적 비와 수송 비를 같은 모델에서 따로, GITT '면적' 은 곱으로".
- ⚠ 어긋남 13 건(D1 극한식 d → 0 = 6.40 · D3 표 1 고출력 `τ²` 1.7 ↔ 1.50 · D4 바인더 전류 규약 · D6–D8 Nam 대조 · 탄소 가정 · D10 55호 13.2 % · D12 14호 [69] · D13 24호 "14 %" · "point contacts" 외).
- 그림: Read 6 장(Fig. 1 · 2 · 4 · 5 · 6 · S4) + 5b · 5d 확대 + 극한식 쪽 렌더, 안 봄 Fig. 3 · S2 · S3 · S5.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 57편 · Evidence 쉰두 번째 · 새 제약 · Status Log) · [[assb-lampe-contact-product-degeneracy]](마흔 번째 적용 · 처방 표 새 줄) · [[assb-tortuosity-factor-effective-conductivity-split]](일곱 번째 표본) · [[composite-cathode-percolation-utilization]](`p_c` 계보 · "pore 문턱" 귀속) · 큐 문서 §6-3-g 58 행 + 지문 ²³.
- 후속(서지 기준, 미열람): Nam · Oh · Jung · Jung 2018 *JPS* 375, 93 ([25]) · Kato … Kanno 2018 *JPCL* 9, 607 ([44]) · Froboese … Kwade 2019 *JES* 166, A318 ([27]) · Shi … Ceder 2020 *AEM* 10, 1902881 ([28]) · Braun … Ivers-Tiffée 2018 *JPS* 393, 119 ([52]).

## [2026-09-23] ingest | assb 58호 — Asheri, Fathidoost, Glavas, Rezaei, Xu 2023, Data-driven multiscale simulation of solid-state batteries via machine learning (Comput. Mater. Sci. 226, 112186)
- raw: `raw/papers/asheri2023_data-driven-multiscale-ssb-delamination-surrogate.md` (sha256 봉인 — `pdf_sha256` · 코드 저장소 URL · 커밋 `4683a6f` · 파일별 sha256 표) · 그림 `raw/figures/asheri2023_data-driven-multiscale-ssb-delamination-surrogate/` (자동 16: 그림 11 · 표 5). 큐 59번(2차 묶음 스무째 · 마지막 편), 15호 ref [22] "유일한 SSB-ML 인용". ⚠ 순수 계산 편(MOOSE CZM + 신경망 대리 + FE²) — 실험 0. 코드 저장소는 실행 없이 조회(`.sav` 미로드), 라이선스 미표기라 복사 0.
- ★★★★ **판정**: 박리 `⟨d⟩` 는 `a·(1−⟨d⟩)` 로만 들어가고 미세 유입은 `d` 무관(`[코드]` `soc_dot = 2|j|` 전 12,304 행) ⇒ **결합상 `ε_p`(`LAM_PE`) 자리**, 37호 `A_eff ↔ k` 아님 · `[재현]` 저율 손실 8.9 · 3.9 % ↔ 1 C 셀 8.7 · 3.1 % · **`θ(N)` 구조적 0**(한 방전 · 출력 ReLU 충전 금지 · 이력 입력 없음) · 손상은 사실상 SOC 의 함수 · 대리 검증은 궤적 안 행 분할 + 범위 안 `G_c` 두 점, 셀 손상 기준해 0, 불확실성 0.
- ★★★ **코드 대조**: 표 4 ✅ · 표 5 R²₁ = bigJ **학습** R² · `r2_score` 인자 역순 · 벤치마크 sklearn · 출력 `identity` · L2 없음 · 플럭스 척도 D1(인쇄 = `j` × 2609.6, Fig. 8 시간은 `j` ÷ 2609.6).
- **채움표 58호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 층 하나(모델 명제) · Q3 층 하나(simulated-surrogate) · Q4 0/58 쉰 번째 성질. **2차 묶음 종료**(≈16.5 → ≈20.0, 마지막 열 편 새 칸 0).
- **곱 축퇴 처방 마흔한 번째 적용**: 새 줄 "박리 변수의 거시 자리는 미세 경계조건이 정한다 — 질량 보존 + 저율 극한 손실로 `ε_p` ↔ `A_eff·k`".
- ⚠ 어긋남 14 건(D1 플럭스 척도 · D3 벤치마크 모델 · D4 · D5 표 5 · R² 역순 · D8 식 (26) · D9 식 (45) · D10 Fig. 10 전하 축 2 C > 1 C · D11 Fig. 11 `G_c` 13.92 > 무손상 외).
- 그림: Read 6 장(Fig. 5 · 7 · 8 · 9 · 10 · 11) + Fig. 9–11 원본 래스터 픽셀 판독 + 식 (26)(32)(45) 렌더, 안 봄 Fig. 1 · 2 · 3 · 4 · 6.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 · 58편 · Evidence 쉰세 번째 · 새 제약 · Status Log) · [[assb-lampe-contact-product-degeneracy]](마흔한 번째 적용 · 처방 표 새 줄) · [[assb-sensitivity-sweep-vs-identifiability]](대리 위 OAT 두 줄) · `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g 59 행 + 지문 ²⁴.
- 후속(서지 기준, 미열람, 큐 밖): Rezaei · Asheri · Xu 2021 *JMPS* 157, 104612 ([11]) · Bai · Zhao · Liu · Xu 2019 *JPS* 422, 92 ([31]) · Sultanova & Figiel 2021 *Comput. Mater. Sci.* 186, 109990 ([19]) · Bucci … Carter 2017 *JMCA* 5, 19422 ([16]) · Fathiannasab … Chen 2020 *JES* 167, 100558 ([33]) · Wolff · Röder · Krewer 2018 *Electrochim. Acta* 284, 639 ([29]).

## [2026-09-23] decision | 2차 묶음 뒤 사용자 결정 — 보류 결정 (라)(마)(바)(사) 반영

- (마) 새 개념 [[assb-synthetic-truth-contact-loss-requirements]] — 카드 '새 제약'(37호)의 ASSB truth 5조건을 분리하고 38·39·53·55–58호 추가분을 합쳐 R1–R8. 전부 `[추론]`, 코드 검증 0. 카드에 분리 표시 링크.
- (바) [[assb-pressure-reapplication-separation-test]] 에 설계 조건 D1–D5 (사이클 해상 압력 계측 · 기준셀 이중차분 · 압력만 바꾸기 · 제조/운전 압력 분리 · 채널별 신고) — 33·39·52·11호 근거.
- (사) [[assb-li-in-reference-potential-window]] P12 를 이식판 입력 메타데이터 요구로 격상 — `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §2-1 M1–M3 (조립 방향 · 상대극 Li 재고 · 원천 역할 검사).
- (라) `ASSB_TRANSFER_NOTE.md` §2 에 A4 양극성 스택(셀별 OCV 비관측) 추가 — wiki 밖.
- 나머지 (가)(나)(다)(아)(자)(차)(타) 는 사용자 지시로 논문 추가 흡수 뒤 판단 (원장 §3-b).

## [2026-09-28] ingest | assb 59호 — Li Q., Liu H., Ye Y., Li K.J., Wu F., Li L., Chen R. 2025, The critical importance of stack pressure in batteries (Nat. Energy 10, 1064–1073)
- raw: `raw/papers/li2025_stack-pressure-critical-importance-perspective.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`(xlsx)) · 그림 `raw/figures/li2025_stack-pressure-critical-importance-perspective/` (자동 6 + 수동 3). **3차 묶음 파일 21**(3차 묶음 첫 편 — 파일 번호 21–33 은 2차 묶음 큐 번호와 별개) · 13호 [23] · 원장 "★ Li Q. 외 2025 · 지목 13호 1 회 · Q6". ⚠ Perspective, 1차 측정 0 · Source Data xlsx = Fig. 1b 원자료(시트명 'Figure 5').
- ★★★ **판정**: 13호 항의 "≈1–5 MPa 가 종설 셋에서 원전 셋으로 독립 수렴" **반박** — "정본 후보" 의 요구치는 `[인쇄]` `<0.1 MPa`(인용 0), 1–5 MPa 를 요구치로 인쇄한 문장 0(이 편 지도에서 0.1–수 MPa 는 액체 LMB 대역) ⇒ 인쇄 띠 0.1–5 MPa(×50) · 일곱 편 · 확인된 원전 0. 13호 귀속("creep, fatigue, and fracture") ✅ · 13호 `<5` 는 [35] · [45] 라 13호 오귀속 아님(정정 대상은 우리 13호 digest 대조표).
- ★★★ **CSP "empirical model"**: 주변 분포 둘(Fig. 5a/b — CE–압력 짝 그림 0, Li 범주가 액체 · 고체 합산) + 눈금 없는 곡선(Fig. 5c) · "validation" 인용 = 양극 압력 모델(Naik 2024) · Na 계(Spencer Jolly 2019) · 측정법 = 같은 셀 오름 압력 + CE 최대 — `[해석]` CE 가 `LLI` · `θ` · 누설(41 · 52호) · 기준 전위(17호)를 한 비로 합치고 이력(5호)을 지운다.
- ★★ **Source Data**: 시트 'Figure 5'(머리 셀 "Figure. 1b" — 29 값: LIB 0.01–0.1 · 액체 LMB 0.69–1.4 · 고체 LMB 5–400 MPa) · 'References'(27 편). Fig. 5 원자료 없음. `[도표]` 화소 판독한 그림 점 ≠ 원자료(액체 LMB 그림 ≈0.34–2.5 MPa).
- ★★ **위 벽 피로의 하중 형태**: 59호 "fluctuations in stack pressure at the MPa level"([39] = 5호 — 5호 digest 에 그 명제 없음) ↔ 13호 "high, constant"; 제어 방향도 반대(59호 압력 일정 + 신호로 운전 조절 ↔ 13호 압력 변조).
- **채움표 59호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다 · Q2 없다(층 — 압력 진단 처방) · Q3 층 하나(literature-aggregate, unpaired + concept curve) · Q4 0/59 **쉰한 번째 성질** · Q5 해당 없음 · Q6 층 넷 · Q7 층 하나(기저 압력 = SEI + 고립 Li, 분리 불가 인쇄) · Q8 없음.
- **곱 축퇴 처방 마흔두 번째 적용**: 적용 불가 · 대상 없음 · 처방 표 경고 행 "압력 축 벤치마크가 CE 한 스칼라일 때 — 52호 줄과 D5 가 먼저다".
- ⚠ 어긋남 14 건(D1 그림 점 ≠ 원자료 · D2 파일 이름표 · D3 경험 근거 · D4 `P/I > 25 MPa cm⁻² mA⁻¹` 단위 부호 + 목표 0.1 MPa 와 모순(허용 0.004 mA cm⁻²) · D5 Fig. 3a ↔ 3b 경계 · D6 5호 귀속 · D7 "Stack pressure minimizes this effect" 인용 0 · D8 균일도 지표(`[재현]` 한 점 +10 MPa 가 "균일") 외).
- 낱말 지문: 11 열 중 `MPa` 15(본문) · `uncertaint` 1(일반어) 외 0 — `contact loss` 0 · `pressure` 188 · `CSP*` 20 · `Coulombic efficienc*` 19 · `EIS` · `OCV` · `hysteres*` 0.
- 그림: **전부 봤다**(자동 6 + 수동 3 — 자동 크롭이 Fig. 2 d/e · Fig. 5 c · Fig. 6 제목 줄을 잘라냄), 화소 판독 Fig. 1b(점 29 + 원자료 대조) · 3a/b/c · 5a/b.
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**((차)에 정성 메모 하나 — Fig. 2d 는 통째 고립 그림).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 59호 행 · 59편 누적 · Evidence 쉰네 번째 · 새 제약 · Status Log · 주장하지 않는 것 · 13호 관련 두 곳 정정 표시) · [[assb-stack-pressure-operating-window]](59호 절 · 13호 표 정정 표시 · 주장하지 않는 것 둘) · [[assb-pressure-reapplication-separation-test]](59호 절 — CSP 측정법 D1–D5 대조) · [[assb-lampe-contact-product-degeneracy]](마흔두 번째 적용 · 처방 표 경고 행 · 주장하지 않는 것). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-g)은 손대지 않았다.
- 후속(서지 기준, 미열람): Zhang W. … Janek 2017 *JMCA* 5, 9929([23] — 지목 4 회째 · 3차 묶음 파일 24) · Chen M. … Zhang X. 2023 *Acta Mech. Solida Sin.* 36, 65([27] — 양극 계면 `P/I` 기준) · Naik … Mukherjee 2024 *AEM* 15, 2403360([44] — 양극 압력 모델) · Yamamoto … Takahashi 2020 *JPS* 473, 228595(원자료 — 압력 × 미세구조) · Feng · Yang · Qi 2022 *JES* 169, 090526([43]) · Yan 2022 *AEM* 12, 2102283([21]) · Kim 2020 *JPS* 463, 228180([31]) · Huang 2022 *Nat. Commun.* 13, 7091([32]) · Ham 2023 *ESM* 55, 455([36]).

## [2026-09-28] ingest | assb 60호 — Zhang Z., Zhang X., Liu Y., Lan C., Han X., … Wang M.-S., Chen S. 2025, Silicon-based all-solid-state batteries operating free from external pressure (Nat. Commun. 16, 1013)
- raw: `raw/papers/zhang2025_pressure-free-si-li21si5-double-layer-anode-assb.md` (sha256 봉인 — `pdf_sha256` · `zip_sha256` · `si_sha256`(SI 1 PDF) · `si2_sha256`(Source Data xlsx)) · 그림 `raw/figures/zhang2025_pressure-free-si-li21si5-double-layer-anode-assb/` (자동 26 + 수동 5 — Fig. 1 · S8 · S18 을 자동 추출이 놓치고 Fig. 3 · 5 를 잘라냄). **3차 묶음 파일 22**(둘째 편 — 2차 묶음 큐 22 = Koerver 와 별개) · 13호 [45] · 13호 후속 표 ★★★ 2 순위 · 원장 "★ Li Q. 외 2025 · Zhang 외 2025 · 지목 13호 · Q6". Article(CC BY) · 1차 측정 있음 · Source Data 14 시트(본문 그림 전부).
- ★★★ **판정**: 13호 `<5 MPa` 의 마지막 인용 다리 **❌** — 요구치 · 문턱 인쇄 0(본문 `MPa` 값 0.8 · 1.51 · 70 · 350 · 370 · 600 · 700), "5" 는 Table S2 의 **5호 Doux 2020 운전 조건** 한 칸 ⇒ [23](59호) · [45](60호) 둘 다 비었고 남은 [35] Li Menglin *AFM* 2025 는 원장 §1 에 없다. 59호 판정(13호 항 "≈1–5 MPa 독립 수렴" 반박)과 일관 — 계보 표(일곱 편 · 0.1–5 MPa · 원전 0)에 값을 더하지 않는다.
- ★★★ **"압력 0 에서의 접촉 손실 시계열" 없음** — `θ(N)` 0/60. 있는 것: 셀 분극 100 사이클(`[데이터]` Fig. 3h `V_max` 0.35 → 0.76 V ×2.2 — 본문 "100 stable cycles") · 용량 1000 사이클(`[데이터]` 1 사이클 기준 −45 %; 인쇄 "80 %@183 · 54.9 %@1000" 은 **2 사이클 112.9 mAh g⁻¹ 기준**) · EIS 2 점(`R_s` ×3.0 · `R_sei` ×4.4 · `R_ct` ×2.9 — 본문 "remained stable") · 사후 SEM 정성. 접촉 몫 0 · **압력 대조군 0**.
- ★★★ **"외압 0"** = 제조(600/370/350 MPa 냉간압착) ↔ 운전(프레임 없는 다이 셀, S1b) 명시 분리 — 그러나 운전 중 **기계 경계조건 미명시**(G1: 플런저 자유 ↔ 캡 고정). 별도 정변위 지그(S14, 예압 0.8 MPa · 공기 중 · 5 사이클): 첫 충전 **+1.51 MPa**(`[인쇄]`) · 이후 `[도표]` ≈1.2 → 1.05 MPa/사이클 · 방전 말 복귀 ⇒ "외압 0 ≠ 계면 응력 0" — 33호 §압력 진동의 Si 완전지 1 차 표본.
- ★★ **Li 과잉 상대극**: `[재현]` 음극 Li₂₁Si₅ 15 mg → Li 29.5 mAh cm⁻² = 양극 2.8 의 **10.5×** → `[데이터]` 1–1000 사이클 중 **145 사이클 CE > 100 %**(최대 107.9 %) · 누적 결손 1.39 mAh cm⁻² = 재고의 4.7 % — CE 는 `LLI` 게이지가 아니고 52호 줄은 검사력 0(M2 의 실례).
- **채움표 60호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다 · Q2 부분(음극 채널 넷 · 양극 0) · Q3 층(n = 1 · 원자료가 지면 다섯을 뒤집음) · Q4 0/60 **쉰두 번째 성질** · Q5 해당 없음 · Q6 층 다섯 · Q7 층 하나 · Q8 층 하나.
- **곱 축퇴 처방 마흔세 번째 적용**: 적용 불가(2전극 · `C` 0 · 온도 1 점 · 양극 0) · 처방 표 새 행 "상대극 Li 재고 ≫ 양극 재고인 셀에서 CE 의 방향 — 52호 줄 앞에 재고비(M2)".
- ⚠ 어긋남 21 건(D1 retention 기준 2 사이클 · D2 CE SD 0.018 ↔ `[재현]` 0.0025 · D3 캡션 2.3 ↔ 본문 0.23 mA cm⁻² · D4 저항 전사 29.1/29.7 · 36.5/35.6 · D5 PITT 비교 전압 = Si 최솟점 · D6 면저항 단위 · D7 "stable" ↔ ×2.2 · D8 "slowly increasing" ↔ ×3.2 · D9 율 복귀 61 % 미보고 · D10 "vs. Li/Li⁺" · D12 ± = 다른 적재 셀 max/min · D13 대조군 적재 · 율 불일치 · D15 Table S2 사이클 정의 · D20 "twofold" 근거 0 외).
- 낱말 지문: 11 열 중 `MPa` 15(본문) · 8(SI) 외 **전부 0** — `pressure` 32 · `external pressure` 14 · `free from external pressure` 6 · `expansion` 22 · `dendrite` 14 · `EIS` 4 · `void` · `OCV` · `hysteres*` 0.
- 그림: 자동 26 + 수동 5 중 **18 항목 봤다**(Fig. 1 · 2 · 3 · 5 · 6 · S1 · S3 · S5 · S10 · S13 · S14 · S15 · S16 · S17 · S18 · S19 · Table S1 · S2), 안 봄 11(Fig. 4 · S2 · S4 · S6 · S7 · S8 이미지 · S9 · S11 · S12 · S20 · S21). 본문과 어긋난 그림: Fig. 5e/f 라벨(기준 사이클) · Fig. 3h "stable" · S14 축 영점 · S17/S19 캡션 중복.
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**((자)에 정성 메모 — 완전지 PITT `D` 도 같은 곱).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 60호 행 · 60편 누적 · Evidence 쉰다섯 번째 · 새 제약 5 · Status Log · 주장하지 않는 것 · 13호 항 표시) · [[assb-stack-pressure-operating-window]](60호 절 · 13호 표 둘째 정정 · 주장하지 않는 것) · [[assb-pressure-reapplication-separation-test]](60호 절 — 무외압 셀 ↔ D1–D5) · [[assb-lampe-contact-product-degeneracy]](마흔세 번째 적용 · 처방 표 새 행). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — Li Menglin *AFM* 2025 등록 · Zhang 2025 흡수 표시 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 22 행)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Li Menglin … 2025 *AFM* 35, 2415696**(13호 [35] — `<5` 의 마지막 확인처) · **Zhang Z. … 2024 *EES* 17, 1061**(ref 22 — 같은 음극의 가압 판 50 MPa · 600 사이클) · **Wang C. … 2022 *Joule* 6, 1770**(ref 19 — soft short 판정 · EIS 회로 원전) · Han S.Y. … 2021 *Joule* 5, 2450(SI 15) · Chen C. … 2018 *ACS AMI* 10, 2185(SI 23 — 또 하나의 0 MPa 행) · Gao 2022 *Joule*(SI 16, 33호 후속 재지목) · Yamamoto 2020 *JPS*(SI 19, 59호 후속 재지목) · Zhang F. 2023 *eTransportation* 15, 100220(ref 14) · Jun 2024 *Small*(SI 27) · Oh 2023 *AEM* 13, 2301508(SI 21 — ≠ 53호).

## [2026-09-28] ingest | assb 61호 — Masias A., Felten N., Garcia-Mendez R., Wolfenstine J., Sakamoto J. 2019, Elastic, plastic, and creep mechanical properties of lithium metal (J. Mater. Sci. 54, 2585–2600)
- raw: `raw/papers/masias2019_elastic-plastic-creep-mechanical-properties-lithium-metal.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`(ESM PDF)) · 그림 `raw/figures/masias2019_elastic-plastic-creep-mechanical-properties-lithium-metal/` (자동 6 + 수동 9 — Fig. 1 · 2 · 3 · 5 · 6 · 7 · 8 · 9 · 10 을 자동 추출이 "그래픽 없음" 으로 전부 제외: 캡션 왼쪽 여백 · 래스터 오른쪽 배치). **3차 묶음 파일 23**(셋째 편 — 2차 묶음 큐 번호와 별개) · 21호 ref 49(후속 표 ★ 7) · 5호 ref 15 · 원장 "★ Masias 외 2019 · 지목 21호 · Q6·Q7". *J. Mater. Sci.* METALS 구독 논문 · 재료 실측(벌크 Li 원통 · 실온) · 셀 0 · 전기화학 0 · ESM Table S1 · S2.
- ★★★ **인용 귀속**: 5호 ref 15 — E 7.82 · G 2.83 GPa · ν 0.381 · 항복 0.73–0.81 · Tariq 2003 일치 ✅, **"그 위에서 creep 시작" ❌**(`[인쇄]` "Tension creep … studied at loads below the 0.8 MPa yield point between 0.2 and 0.6 MPa" — 거기서 `n` = 6.56; 5호 digest 문장 기준, Doux 원문 미열람). 21호 ref 49 — 재료 전제 ✅ · "펠릿 가장자리로 기어드는 creep" 기하 명제는 21호 것(Fig. 10a–c 모식이 최근접). 압력 개념 페이지 §정의 "항복강도를 넘어 크리프" 도 같은 정정.
- ★★★ **(a) 계보 눈금**: 띠 0.1–5 MPa 가 Li 의 눈금으로 **확산 creep(< 0.28 MPa, σ/G < 10⁻⁴) → 멱법칙 creep(0.2–0.6 측정) → 항복(0.73–0.81) → 압축 시험(0.8–2.4) → power-law breakdown(> 2.83, σ/G > 10⁻³)** 을 가로지른다 — `[재현]` 압력 ×50 = creep 속도 ×1.4×10¹¹(유효 구간 0.28–2.83 만 ×3.8×10⁶). 5호 5 MPa = breakdown · 항복 6× · 60호 예압 0.8 = 항복 자리 · 60호 첫 충전 총 ≈2.3 = 압축 상한 근처. 59호(띠 ×50 · 원전 0) · 60호(외압 0 ≠ 응력 0)와 일관 — 띠에 값을 더하지 않고 띠의 비동질성을 보인다.
- ★★★ **(b) "creep 이 계면을 채운다" 의 정량 근거 = `n` 6.56 하나** — `Qc`(온도 1 점) · 입도 `d` · `p` · 채움 실험 · 접착 · 마찰 계수 0; 압축 시간 의존 값(Table S2, 12 · 60 · 120 분)은 **응력 순서 역전**(0.8 → 2.4 MPa 에서 ×0.21 — 마찰 · 배럴링 지배, 저자 인정). 명제는 Fig. 10 모식 + "we believe".
- ★★ **(c) `θ(N)` 으로 옮길 때 빠지는 것 여덟** — 셀 · SE · 계면 0 · AR 1–4.6 ↔ 셀 Li 박 ≈10⁻⁴(`[인쇄]` 저자 추정) · 마찰 미지 · 온도 1 점 · 반복 하중 0 · 도금 Li 0 · 계면 void 경계값 문제 · 양극 0 — 우리 3 항 분해에는 음극 `η(i, P)` 의 시간 상수(σ^6.56)로만 들어간다.
- ★★ **Q6 여덟 번째 인쇄값 · 계보 최초(2018)**: `[인쇄]` "stack pressures in the 1.0 MPa range are necessary to achieve low and stable cell resistance [9, 10]" ↔ 같은 지면 "How much compressive stress is not known … We believe 1 MPa was sufficient" — 원전 [9] Sharafi … Sakamoto 2016 *JPS* 302 · [10] Wang & Sakamoto 2018 *JPS* 377(미열람; 46호는 [10] 을 "Li 항복 2 MPa" 로 전사 ↔ 이 편 0.73–0.81, 2.5×). 띠 0.1–5 · 확인된 원전 0 그대로. `[해석]` "≈1 MPa" 가닥 = Sakamoto 실험실 한 뿌리 가설(Sharafi 2016 → Wang 2018 → 이 편 → Wang 2021 *Joule* = 39호 원전).
- **채움표 61호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(셀 0) · Q2 없다(재료 채널 셋) · Q3 층(measured-mechanical · `n` 오차 0) · Q4 0/61 **쉰세 번째 성질** · Q5 해당 없음 · Q6 층 넷 · Q7 층 하나(`[인쇄]` "excess capacity … irreversible material loss … mechanical stability") · Q8 해당 없음.
- **곱 축퇴 처방 마흔네 번째 적용**: 적용 불가(대상 없음) · 처방 표 행 0 · 기록: `P↑` 연산자의 음극 쪽 시간 상수 — 재가압 뒤 초–분 회복 = Li\|SE creep, 안 돌아오는 몫 = 양극 복합체 ⇒ **회복 시간 곡선으로 전극 가르기**(제안 · 실측 0).
- ⚠ 어긋남 16 건(D1 SS/PE ↔ 0.81/0.73 본문·Table 3 반대(`[도표]` 인셋 교점 ≈0.63/≈0.76) · D2 "0.4 % 이후 감소" ↔ Fig. 2 ≈4 % 정점 0.93 MPa · D3 σ/G 저/고 뒤바뀜 · D4 Fig. 7 D 인쇄 3.1×10⁻¹ ↔ `[재현]` ≈9×10⁻¹¹ cm² s⁻¹ · D5 "1 mm/s" ↔ 1.22×10⁻³ s⁻¹(1 mm/min 이면 성립) · D7 본문 10.5–10.6 GPa 가 Table 1 에 없음 · D8 σ/G 열 G 2.81 ↔ 2.83 · D9 [33] LLZO 탄성 편을 "cycling studies" 로 인용 · D10 "necessary" ↔ "not known" · D14 Fig. 8 정하중 시작 시 ≈25–30 % 사전 변형 · D16 결론 "~1 MPa" ↔ creep 시험 0.2–0.6 외).
- 낱말 지문: `pressure` 5 · `stack pressure` 2 · `MPa` 25 · `creep` 52 · `yield` 31 · `barrel` 12 · `friction` 16 · `aspect ratio` 13 · `dislocation` 16 · `contact` 6(셀 관련 1) · `dendrit` 1 · `void` · `fatigue` · `uncertaint` · `error` · `LLI` · `LAM` · `EIS` · `OCV` **0**.
- 그림: 자동 6 + 수동 9 중 **12 항목 봤다**(Fig. 1–10 · Table S1 · S2 — SI 표는 텍스트 추출이 열을 뒤섞어 이미지로 열 대응 확정), 안 봄 3(Table 1 · 2 · 3 이미지 — 텍스트로 읽음). 본문과 어긋난 그림: Fig. 2(정점 · 인셋 교점) · Fig. 7(축값 ↔ 본문 D) · Fig. 8(사전 변형) · Fig. 9(응력 순서 역전 — 본문은 인정).
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**((차)에 정성 메모 — 압력 의존 `θ(P, t)` 를 넣는다면 음극 `R_int(P, t)` 는 별도 노브).
- 컴파일: **새 개념 1** [[li-metal-yield-creep-vs-stack-pressure]](정의 표 · 계보 눈금표 · 귀속 정정표 · 적용 5 · 어긋남 · 주장하지 않는 것; `evidenceScope: single-source` · `confidence: low`) · 갱신 [[assb-contact-loss-vs-lampe]](채움표 61호 행 · 61편 누적 · Evidence 쉰여섯 번째 · 새 제약 5 · 새 제약 3 주석 · 13호 항 주석 · Status Log · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](§정의 정정 주석 · 13호 표 셋째 주석 · 61호 절 · 주장하지 않는 것 · 관련) · [[assb-pressure-reapplication-separation-test]](61호 절 — 유지 시간 · 회복 시간 상수 · 관련) · [[assb-lampe-contact-product-degeneracy]](마흔네 번째 적용) · `index.md`(47 페이지). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — Masias 흡수 표시 · **Sharafi 2016 신규 등록** · Wang & Sakamoto 2018 지목 1 → 2 · Xu 2017 *PNAS* 지목 1 → 2 · Wang 2021 *Joule* 재지목 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 23 행)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Sharafi A., Meyer H.M., Nanda J., Wolfenstine J., Sakamoto J. 2016 *J. Power Sources* 302, 135**([9] — "1.0 MPa" 원전 · 원장에 없음) · **Wang M., Sakamoto J. 2018 *J. Power Sources* 377, 7**([10] — 지목 2 회 · "항복 2 MPa" 대조) · Wang·Kazyak·Dasgupta·Sakamoto 2021 *Joule* 5, 1371(39호 원전 재지목) · **Sargent P.M., Ashby M.F. 1984 *Scr. Metall.* 18, 145**([32] — 기구 지도 · σ/G 경계 · D 값) · LePage 2019 *JES* 166, A89(기존) · Tariq 2003 PAC([13]) · Xu … Greer 2017 *PNAS* 114, 57([30] — 지목 2 회) · Monroe & Newman 2005 *JES* 152, A396([4]).

## [2026-09-28] ingest | assb 62호 — Zhang W., Schröder D., Arlt T., Manke I., Koerver R., Pinedo R., Weber D.A., Sann J., Zeier W.G., Janek J. 2017, (Electro)chemical expansion during cycling: monitoring the pressure changes in operating solid-state lithium batteries (J. Mater. Chem. A 5, 9929–9936)
- raw: `raw/papers/zhang2017_in-situ-pressure-electrochemical-expansion-assb.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`(ESI PDF)) · 그림 `raw/figures/zhang2017_in-situ-pressure-electrochemical-expansion-assb/` (자동 12 — 본문 5 · ESI 7, 수동 0; 12 장 전부 봤고 수치는 PDF 원본 래스터에서 축 눈금 적합으로 픽셀 판독). **3차 묶음 파일 24**(넷째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★★★ Zhang·Schröder·Arlt·…·Janek 2017 · 지목 22 · 23 · 33 · 59 · Q1·Q6" · 22호 ref 18 · 23호 ref 40 · 33호 [89] · 59호 ref 23(+ 카드 6호 항 ref 46 기록). JLU Giessen + HZB · RSC(오픈액세스 표시 없음) · 1차 측정(in situ 압력 · 딜라토미터 · X-CT · XRD · EIS). ⚠ 본문 텍스트 층이 µ 를 m 으로 싣는다 — 단위는 렌더로 대조.
- ★★★ **인용 귀속**: 22호 ref 18 — 셀 장치 ⚠ 부분(`[인쇄]` ∅10 mm Macor 실린더 · In ∅8 mm → `[재현]` 0.785 cm², C/10 = 146 µA cm⁻² 정확히 재현; 장치는 [28] Busche 2016 로 다시 위임 · ESI 계산은 "cell area of 1.103 cm²") · **"volume contraction during charging → reduced contact" ❌**(양극 LCO 는 충전 팽창 · `contract` 1 회 = LCO 방전 · NCM 은 "nearly 6%" 방향 0). 23호 ref 40 "LCO 단위격자 팽창" ✅(2 % 는 [30] Reimers & Dahn 재인용). 33호 [89] — 그림 ✅(`R₁` · `R₂` 원본에 있음, 수치 0) · "causing contact loss" ⚠(원문도 추론, 외압 0 펠릿 · 충전 1 회). 59호 ref 23 "mirror" ✅(기저선을 뺀 그림에서). 6호 ref 46 — 실측 ✅ · G12 ❌. 원장 행 서술 "충전 중 부피 수축 → 접촉 감소를 압력으로 감시" ❌ — 정정 필요(wiki 밖).
- ★★★ **(a) 크기 · 부호 · 추이**: 충전 ↑ · 방전 ↓(두 전극 모두 충전 팽창) · 본문 값 `[인쇄]` "1.25 MPa" 하나(기저선 보정) · 본문 `MPa` 1 회 · `stack pressure` 0 · **운전 기저 `[도표]` ≈61.8 MPa 는 ESI S7 축에만** · 원시 첫 충전 +1.07 · 원시 표류 −1.2 MPa/110 h(시간당 ≈0.02 → 0.009) · `[도표]` 보정 진폭 1.267 → 1.152 MPa ↔ 용량 116.7 → 93.2 mAh g⁻¹ — **비 +14 %** · 원시 충전 상승 0.1 C 에서 평탄(+1.07 → +1.13 → +1.10) · LTO 셀 진폭 0.0669 → 0.0669(용량 −9 %) · 음극(In) 몫 `[재현]` ≈90–95 %.
- ★★★ **(b)** "충전 수축" 은 이 셀에 없다 · 접촉 손실(`contact` 셀 관련 9)은 전부 재인용 · 추정 · 추론 · 결론 — 추론의 두 줄기(무가압 펠릿 X-CT 휨 · 가장자리 균열 / 무가압 딜라토 셀 11.4 mAh g⁻¹)를 ≈62 MPa 구속 셀(Fig. 1)의 감쇠에 붙인다(D15) — `θ(N)` 0.
- ★★ **(c)** 60호 S14(+1.51 @ 0.8 MPa)와 같은 눈금이 아니다 — 기저 ×77 · `[재현]` ΔP/면적 용량 ≈1.0(보정) · ≈0.86(원시) ↔ ≈0.52 MPa per mAh cm⁻² · ΔP 를 셀 탄성만으로 내려면 유효 길이 ≈22–36 mm(지그 순응). 61호: 기저 = Li 항복의 ≈80× · σ/G ≈2.2×10⁻² — 이 셀은 In 이라 Li 눈금 밖; 이 편의 "Li 금속이면 2.2 µm" 는 ⅓ 규칙(평면 석출 `[재현]` 6.7–9.4 µm). **(d)** 22호 G5 에 0.785 cm² 조건부(같은 연구망 23호 역산 ∅10 mm · 8.4 mg AM 과 같다).
- **채움표 62호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다 · Q2 부분(채널 다섯 · 다섯 개의 다른 셀 · 압력 채널의 전극 분해) · Q3 층(기저선 보정본 ↔ 원시) · Q4 0/62 **쉰네 번째 성질** · Q5 층 하나(공칭 조성 계산 · Takada 1996 지목 3) · Q6 층 다섯(첫 운전 중 압력 실측 · 운전 압력 본문 0 · 요구치 0 · 기저선 · 강성) · Q7 해당 없음(층 하나 — 기저선이 재고 손실 신호를 지운다) · Q8 층 하나(NCM "nearly 6%" [31] — 23호 G1 빈칸).
- **곱 축퇴 처방 마흔다섯 번째 적용**: 적용 불가(1단계 입력 없음) · 처방 표 **경고 행** "압력 · 두께 진폭을 활성 분율(`θ·ε_p`) 대리로 쓸 때 — `k_eff(N)` · 기저선 규약 · 음극 몫이 먼저" — `[해석]` 입자 고립과 `LAM_PE` 는 둘 다 Δx 를 멈춰 같은 서명; 압력 채널은 관측 하나와 미지수(`k_eff`) 하나를 같이 더한다.
- ⚠ 어긋남 22 건(D1 기저선 규약 · D2 In 팽창 42 · 105.6 ↔ `[재현]` 50.2 % · D3 113.23 Å³ ↔ Fig. 2 치수 156.66 · D4 ESI 계산 셀(LCO 14 mg · In 89 mg · 1.53 mAh · 1.103 cm²) ↔ 본문 압력 셀 · D5 Li 2.2 µm ⅓ 규칙 · D6 기공 "light areas" ↔ 캡션 "Bright … higher material density" · D7 Fig. 5 0.1C ↔ 0.03C · D8 "before/after cycling" = 다른 두 펠릿 · D9 ESI 부피 SE +16.6 % · 음극 ×3.1 · D10 "60% … as In" ↔ 0.90 · D12 CE > 99 % "from the 2nd cycle" ↔ 98.3 % · D13 딜라토 첫 휴지 −2.6 µm ↔ "setup relaxation 배제" · D15 감쇠 배정 셋 · D16 "~1 µm" · D17 약속된 압력 추정 0 외).
- 낱말 지문(NFKC · 합자 복원): `pressure` 76 · `MPa` **1** · `stack pressure` **0** · `contact` 10(셀 관련 9) · `contract` 1 · `expan` 43 · `baseline` 4(+ ESI 9) · `confinement` 5 · `tomograph` 24 · `load cell` 0 · `uncertaint` · `error` · `±` · `LLI` · `LAM` · `OCV` · `creep` · `yield` · `fatigue` · `dendrit` **0**.
- 그림: 자동 12 · 수동 0 — **12 장 전부 봤다**(Fig. 1–5 · S1–S7). 본문과 어긋난 그림: Fig. 3 캡션("60% … as In" ↔ Fig. 1b 0.90) · Fig. 5(기공 = light ↔ 캡션 고밀도 · 0.1C ↔ 0.03C) · S3(CE > 99 % "2nd cycle" ↔ 98.3 %) · S6(첫 휴지 −2.6 µm ↔ "setup relaxation 배제") · S7(절대 압력인데 "pressure change curve"). ⚠ 부수 변경: 추출기가 `raw/figures/_sources.json` 의 61호 항 `figures` 를 6 → 15 로 바로잡았다(폴더 15 장 · figures.json 15 항목과 일치).
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**.
- 컴파일: **새 개념 1** [[assb-operando-pressure-signal-attribution]](신호 분해 `P_base + k_eff·ΣΔh_e` · 함정 다섯 · 표본 표 62 · 60 · 33 재수록 · 9호; `evidenceScope: multi-source-mixed` · `confidence: low`) · 갱신 [[assb-contact-loss-vs-lampe]](채움표 62호 행 · 62편 누적 · Evidence 쉰일곱 번째 · 새 제약 5 · Status Log · 22호 · 6호 항 주석 · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](62호 절 · §압력 진동 원형 주석 · 주장하지 않는 것 · 관련) · [[assb-pressure-reapplication-separation-test]](62호 절 — D1–D5 대조 · 원시 압력 · 기저선 · 전극 몫 · 관련) · [[assb-lampe-contact-product-degeneracy]](마흔다섯 번째 적용 · 처방 표 경고 행 · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](스물다섯 번째 형태 — 공칭 조성 계산) · `index.md`(48 페이지). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — Zhang 2017 *JMCA* 흡수 표시 · 서술 정정("충전 수축" ❌ · "셀 장치 원전" ⚠) · **Busche 2016 · Whiteley 2015 신규 등록** · Kondrakov 2017 *JPCC* 121, 3286 지목 1 → 2 · Takada 1996 지목 2 → 3 · 6호 지목 기록 · Zhang 2017 *ACS AMI* 지목 +1 후보 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 24 행)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Busche M.R., Weber D.A., Schneider Y., Dietrich C., Wenzel S., Leichtweiss T., Schröder D., Zhang W., Weigand H., Walter D., Sedlmaier S.J., Houtarde D., Nazar L.F., Janek J. 2016 *Chem. Mater.* 28, 6152**([28] — hot-press 장치 · 강성 · 조절 방식 · 원장 0) · **Zhang W. … Janek 2016 "submitted"**([27] = ESI [1] — 원장 ★★★★ *ACS AMI* 9, 17835 와 같은 편인지) · **Kondrakov … Janek 2017 *J. Phys. Chem. C* 121, 3286**([31] — NCM ≈6 % · 방향) · **Takada, Aotani, Iwamoto, Kondo 1996 *SSI***([33] — 0.62 V · 이 편 인쇄 권 "2738") · Koerver 2018 *EES*(LTO 자료 제공자 R. K. 의 후속 · 33호 [58] 재지목) · Whiteley, Kim, Kang, Cho, Oh, Lee 2015 *JES* 162, 711([19] — Sn–Li 접촉 · 외압) · Han 2021 *Joule* · Ji 2022 *ESM*(33호 [90] · [88] — 기저 본문 0 형태) · Reimers & Dahn 1992 *JES* 139, 2091([30]) · Alexander … Calvert 1976 *Can. J. Chem.* 54, 1052([32]).

## [2026-09-28] ingest | assb 63호 — Zhang W., Weber D.A., Weigand H., Arlt T., Manke I., Schröder D., Koerver R., Leichtweiss T., Hartmann P., Zeier W.G., Janek J. 2017, Interfacial Processes and Influence of Composite Cathode Microstructure Controlling the Performance of All-Solid-State Lithium Batteries (ACS Appl. Mater. Interfaces 9, 17835–17845)
- raw: `raw/papers/zhang2017_interfacial-eis-cathode-composition-lco-lgps-assb.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`(SI PDF)) · 그림 `raw/figures/zhang2017_interfacial-eis-cathode-composition-lco-lgps-assb/` (자동 26 — 본문 9 · SI 15 · 표 2 + 수동 2 — S11(벡터 그림 위쪽 · 범례를 자동 크롭이 잘랐다) · 초록 그래픽(캡션 없음); 28 항목 전부 봤고 수치는 PDF 원본 래스터 픽셀 판독 · SI 표 S1 · S2 는 텍스트 층이 없어 이미지로 읽음). **3차 묶음 파일 25**(다섯째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★★★★ Zhang·Weber·Weigand·…·Janek 2017 · 지목 22 · 23 · 24 · 39 · 41 · 42 · Q1·Q2·Q5" · 23호 방법 원전(ref 29, 본문 8 회) · 62호 [27] 확인 과제. JLU Giessen + HZB + BASF + KIT BELLA · ACS 구독 논문 · 1차 측정(SOC/SOD 해상 EIS · 조성 다섯 × 율 7 · 100 사이클 · X-CT 펠릿 1 · XPS 정성).
- ★★★ **62호 [27] = 이 편** — 62호 ESI S2 = Fig. 4a(맨 아래 곡선 마커 22 개 Re ±0.05 Ω) · 62호 ESI S3 = Fig. 9 셀 C(70:30) = 초록 그래픽(CE 사이클 3–90 ±0.02 %p · 용량 상수 차 1.4 mAh g⁻¹) · 저자 8/11 같은 순서 · [27] 에 매단 명제 전부 · 시점(이 편 접수 2017-01-23) · 이 편 [43] = 62호 역인용 ⇒ 원장 지목 **7**. ⚠ 62호 S3 셀은 이 편 방법상 **Li 박 1:60 장기 셀**(`[재현]` 재고 2.96 mAh = 양극 ×3.1) — 62호 digest 의 "무 Li In 조립 → 재고 = 양극" 은 압력 셀에만 해당(개념 페이지에 정정 주석). 62호 "standard SSB setup" · LTO "air-tight cell casing" = 이 편 S3 케이스(나사 10 N·m · 하중계 0). 62호 S1 은 이 편 S10 과 다른 그림.
- ★★★ **(a) 7:3** — `optim` 3 회 모두 일반어 · 인쇄 근거는 두 기준(100 사이클 유지 C 78.5 % ≈ B ≈79 % "comparable" · 첫 충전 뒤 계면 저항 최소 S11)의 절충. `[도표]` 0.1–1 C 최대 80:20(134.7 mAh g⁻¹ = 98 %) · 2 C 70:30 · 5–10 C 60:40 · 조성당 1 셀 · LCO:LGPS 무탄소.
- ★★★ **(b) 토모그래피** — 실험실 X-CT 6.25 µm · 냉간 압착 펠릿 1 · 분할 0 · 수치는 분리막 "∼600 μm" 하나 ⇒ 공극률 · 접촉 면적 · 입도 · 굴곡도 **0**. `[재현]` 분리막 공극률 ≈14–18 %(질량 · 지름 · 두께 · 이 편 wt→vol 에서 역산한 ρ_LGPS 2.01–2.08) · 복합체 SEM "90 μm" ↔ 무공극 36.3 µm(≈60 % — "quite dense" 와 불합).
- ★★★ **(c) 23호가 가져간 것** — 셀 절차 · PEEK ∅10 mm ✅ · 운전 구속 **나사 토크 10 N·m 뿐**(`MPa` 본문 · SI 0 — 23호 5 kN(64 MPa)/≈70 MPa 는 23호 값; `[재현]` K · d 가정 42–106 MPa) · 호 배정(HF 입계 · MF 양극 · LF In/SE) = 거동 + 인용([32] 은 LCO 절연체–금속 논문 — D11) + C 크기 · 기준극 0 · 대칭셀 S14(무 Li In = 차단) 본문 인용 0 · "kinetic hindrance" = 셀 수준 측정(방전 끝 표지 2.000 → 3.265 V, 30 분 1.27 V 회복) + 위치(In 쪽) 배정.
- ★★★ **(d) Q2 — SOC 축 1단계**(전제 `C ∝ 면적`): 첫 충전 R_MF 앞 절반(명목 SOC ≈10 → 60 %) R ×1.18 · C ×0.83 · τ 보존(면적형 −17 %) · 뒤 절반 R ×1.76 · C ×1.03 · τ ×1.82(저항형) — 저자 · 10호의 "접촉 손실 + 분해층 동시 귀속" 을 구간으로 가른다(저자가 코팅 균열을 거론한 "×2" 는 저항형). LF 방전 R ×23.8 · C ×3.5 — C 가 이중층 ×80–600 이라 전제 불성립 · 23호(방전 끝 C 붕괴)와 반대 방향. Q1 `θ(N)` 0/63(셀 D 감쇠 = "접촉 결핍 → 과충전 → 불활성" 곱 사슬 가설). Q5 스물여섯 번째 형태(창 이탈을 동역학 장애로 명명한 원전 + 장기 셀만 Li 보충; `[재현]` 무 Li 방전 끝 ≈0.8 at% · Li 박 셀 21.6 at%).
- ★★ **Fig. 8b 확산 길이** — A 53 · B 53 · C 62 · D 101 nm 는 식 (1) 기울기(h)를 s 로 넣은 값(`[재현]` ≤1 nm; D 는 그림에 없는 0.1 C 점 포함) — 교정 3.1–6.0 µm; 본문 D_Li cm² s⁻¹ ↔ 캡션 m² s⁻¹. ★ 1호 ref 12 인 이 조성 스윕에서 29 vol% 가 0.1 C 68 % — 1호 `p_c`(d 2–5 µm → 42–49 vol%)와 어긋나는 세 번째 표본(22 · 56호에 이어).
- **귀속**: 22호 ref 16 — 7:3 ⚠ 부분 · 공극률 실측 ❌ / 23호 ref 29 — 절차 ✅ · kinetic hindrance ✅(배정 위) · 70:30 "최적" ⚠ · EIS 모델 ✅(배정 근거 ⚠) / 24호 ref 20 — 조성 ✅ · 두께 ❌ / 39호 ref 12 · 42호 ref 2b — 판정 불가(전사 0) / 41호 ref 34 ✅ / 지목 밖 1호 ref 12 ✅ · 10호 [97] ✅ · 40호 [19] ✅ / 원장 행 — 7:3 ⚠ · 공극률 ❌ · 방법 원전 ✅ · [27] ✅.
- **채움표 63호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다 · Q2 부분(SOC 축 1단계 — 우리 판독) · Q3 층(적합 ± · 셀 간 산포 0) · Q4 0/63 **쉰다섯 번째 성질**("`d²/D` 의 `D` 고정 · ×60 · 배정 유일성 미질문") · Q5 층 하나(Takada 지목 4) · Q6 층 넷 · Q7 해당 없음(층 하나 — Li 박 재고) · Q8 층 하나.
- **곱 축퇴 처방 마흔여섯 번째 적용**: 부분 적용 — 1단계 SOC 축 통과(두 구간) · 코팅 쌍 화학 대조 정합 · 3단계-b LF 실패 · 처방 표 두 줄(SOC 축 1단계 · 율 스윕 `d²/D` 경고) · 마흔다섯 번째 적용 52호 줄 정정 주석.
- ⚠ 어긋남 20 건(D1 확산 길이 단위 · D2 Fig. 8a D 0.1 C 누락 · D3 R_HF "≈2 Ohms … 518 kHz" ↔ 표 S1 3.12 Ω · `[재현]` 61 kHz · D4 만충 스펙트럼 두 셀 · D5 셀 D 접촉 면적 반대 명제 · D6 셀 A "most separated" ↔ 68 % · D7 코팅 1.4 ↔ 1 wt% · D8 115 ↔ 122 µA cm⁻² · D9 "constant pressure" ↔ 운전 중 압력 변화 인용 · D10 "irreversible" ↔ 1.27 V 회복 · D11 LF 배정 인용 [32] · D12 "necks" ↔ C 크기 · D13 결론 원인 하나 · D14 80 % 기준 · D15 90 µm ↔ 36 µm · D16 Fig. 5 · 6 9 번째 점 ≈3.287 ↔ 3.267 V 외).
- 낱말 지문: `interfacial resistance` 24 · `contact` 18(측정 0) · `percolat` 10 · `diffusion length` 11 · `kinetic hindrance` 3 · `pressure` 4 · `MPa` **0** · `torque` 1 · `optim` 3(일반어) · `symmetric` 0(SI 1) · `reference electrode` · `identifiab` · `uncertaint` · `±`(텍스트 층) · `LLI` · `LAM` · `void` · `tortuos` · `reproduc` **0**.
- 그림: **28 항목 전부 봤다**(Fig. 1–9 · S1–S15 · 표 S1 · S2 · 초록 그래픽 · S11 수동). 본문과 어긋난 그림: Fig. 8(캡션 m² s⁻¹ · D 0.1 C 누락) · Fig. 9 캡션(이론 ↔ 초기) · Fig. 3 · S5 캡션(115 µA cm⁻²) · Fig. 5 · 6(9 번째 점) · Fig. 2 캡션(셀 A · 셀 D) · S5a 축 표기. ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(28)이 추가됐다.
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**((차)에 정성 메모 — SOC 구간별 면적 ↔ `j₀` 노브).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 63호 행 · 63편 누적 · Evidence 쉰여덟 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](마흔여섯 번째 적용 · 처방 표 두 줄 · 마흔다섯 번째 정정 주석 · 주장하지 않는 것) · [[assb-interphase-vs-contact-loss-attribution]](63호 행 · 처방 1 · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](스물여섯 번째 형태) · [[composite-cathode-percolation-utilization]](63호 절 — 1호 ref 12 · `p_c` 대조) · [[assb-operando-pressure-signal-attribution]](62호 LTO 케이스 · S3 셀 정정) · [[assb-stack-pressure-operating-window]](63호 절 · 주장하지 않는 것). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — 이 행 흡수 표시 · 지목 6 → 7 · 서술 정정("공극률 실측" ❌ · "7:3 근거" ⚠ · "[27] 미확인" → 확인) · Otoyama 2016 · Irvine 1990 · Okubo 2007/2008 신규 · Takada 1996 지목 3 → 4 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 25 행)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Otoyama, Ito, Hayashi, Tatsumisago 2016 *JPS* 302, 419**([35] — Raman SOC 지도 · 셀 D 가설의 유일한 근거) · **Irvine, Sinclair, West 1990 *Adv. Mater.* 2, 132**([47] — 정전용량 배정표) · **Okubo … Honma 2007 *JACS* 129, 7444 · 2008 *J. Phys. Chem. Solids* 69, 2911**([30] · [50] — 식 (1) 원전) · **Takada 1996 *SSI* 86–88, 877**([33] — 지목 4) · Weber … Zeier 2016 *Chem. Mater.* 28, 5905([16] — LGPS 10.5 GPa) · Ménétrier … Delmas 1999 *J. Mater. Chem.* 9, 1135([32]) · Webb … Veith 2014 *JPS* 248, 1105([36]) · Mizuno 2005 *JPS* 146, 711([48]) · Park … Sastry 2010 *JPS* 195, 7904([51]).

## [2026-09-28] ingest | assb 64호 — Koerver R., Walther F., Aygün I., Sann J., Dietrich C., Zeier W.G., Janek J. 2017, Redox-active cathode interphases in solid-state batteries (J. Mater. Chem. A 5, 22750–22760)
- raw: `raw/papers/koerver2017_redox-active-interphase-cutoff-voltage-ncm811-lps.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`(ESI PDF)) · 그림 `raw/figures/koerver2017_redox-active-interphase-cutoff-voltage-ncm811-lps/` (자동 14 — 본문 7 · ESI 7 + 수동 1 — Fig. 7: 8 쪽 캡션 블록이 "Fig. 7" 뒤 줄바꿈으로 시작해 자동 추출이 놓쳤다; 15 항목 전부 봤고 수치는 PDF 원본 래스터 픽셀 판독 · ESI 는 SMask 가 있어 200 dpi 렌더 · 표 S8 은 텍스트 층). **3차 묶음 파일 26**(여섯째 편 — 2차 묶음 큐 번호와 별개; 큐 22 = 23호 *Chem. Mater.* 는 다른 논문 · 같은 셀 설계) · 원장 "★★ Koerver·Walther·Aygün·…·Janek 2017 · 지목 22 · 42 · Q2 · 산화 계면층 — 곱 축퇴의 `j₀` 쪽 원전" · 22호 ref 12 · 42호 ref 2a · (지목 밖) 17호 ref 8. JLU Giessen(Zeier · Janek) · RSC 구독 논문 · 1차 측정(상한 컷오프 넷 × 25 사이클 · 충/방마다 EIS(`R` + ESI `C`) · XPS 깊이 · in situ XPS · 컷오프당 셀 2).
- ★★★ **인용 귀속**: 22호 ref 12 "탄소 첨가제 → severe degradation upon cycling" ⚠ 부분(전지 셀 무탄소 · `[인쇄]` "conductive carbon is known to promote side reactions.29,30" 로 이 편도 위임 · 탄소 증거는 in situ XPS(C65 : SE · 외압 0 · ±10 V)뿐) · 22호 후속 표 · 원장 "계면층(`j₀`) 쪽 원전" ⚠ 절반(산화 계면층 원전 ✅ · `j₀` · 면적 낱말 0 · 원전의 위치 판정은 **집전체 쪽** · `j₀` 쪽은 SI `C` 의 우리 판독이고 노화분 한정) · 42호 ref 2a 판정 불가(명제 전사 0) · 17호 ref 8 "interphase formation" ✅ · 23호는 시점상 인용 불가 — 역으로 이 편 [11] = 23호(본문 21 회): 23호가 나누지 않은 "combination" 을 "explain" 으로 받는다.
- ★★★ **(a) 화학 · 양**: 화학은 측정(S 2p PS₄³⁻ 161.4 · P–[S]n–P 162.7 · S⁰ 163.5 eV · in situ Li₂S 159.8; 표 S8 표면 at% 4.0 V 66/17/17 · 4.3 V 70/17/13 · 4.6 V 66/20/14 · 5.0 V 42/32/26) · 두께 = 식각 시간 6 · 10 · 18 · 32 분(nm 환산 0 — `[인쇄]` "not possible") · 전하 0 · 저항 = EIS 한 호(`R_cathode/SE`, 위치 미분리) · 측정 = 복합체 집전체 쪽 면 한 분화구(컷오프당 셀 1). 셀 = 23호 설계(NCM811 : β-LPS 70 : 30 12 mg · `[재현]` 0.785 cm² · 10.7 mg cm⁻² · In ∅6 mm 무 Li · 445 / "approximately 70" MPa · 0.1 C 214 µA cm⁻²).
- ★★★ **(b) 전하**: `[인쇄]` "every redox reaction of the electrolyte in the electrode will add up to the total capacity" — 수량 0. `[재현]` 상한 64 mAh g⁻¹_NCM(복합체 SE 전부 1 e⁻/PS₄) · in situ `[도표]` 적분 산화 ≈0.55 · 환원 ≈0.52 mAh — **환원이 무 Li In 재고(산화 단계가 넣은 ≈0.55 mAh)에서 끊겨** "partially reversible" 이 상대극 한계와 안 갈린다. ⇒ 카드: 겉보기 양극 용량의 **덧셈 항**(`Q_SE,rev`) · CE 결손 ≠ `LLI`(SE 산화가 Li⁺ 를 음극에 쌓는다). 첫 방전 결손의 ≈28–37 % 는 둘째 사이클에 돌아오는 `η` 형(4.0–4.6 V).
- ★★★ **(c) 곱 축퇴 — 1단계 사이클 축**(Fig. 4 + S7, 전제 `C ∝ 면적`, 원전은 `C` 해석 0): 노화분 **저항형** — 4.6 V `R` ×4.5–4.9 · `C` ×1.04 · 5.0 V `R` ×4.9–5.5 · `C` ×1.9(23 · 63호와 같은 방향); 가역 SOC 분(충 ÷ 방) 4.6 V `R` ×1.50 · `C` ×0.73–0.83 · τ ×1.10–1.24(**면적형 쪽**) · 5.0 V τ ×2.2–2.4(**저항형**) · 4.0 V `R` ×0.20(부호 반대) ⇒ 원문 "for all cells suggests redox reactions" 는 원문 SI 로 5.0 V 에서만 선다. ★ **4.0 V "양극 호" 는 `C` 0.1–0.85 mF = 다른 셀 ×250–700 = 음극 호 자릿수 · τ 7–57 Hz** — ESI S7 이 그 패널만 10⁻⁵–10⁻² F 축에 그렸다. ★ **위치** — 원전 XPS 는 분해의 주 위치를 집전체 쪽에 둔다(`[인쇄]` "The interphase formed at the CC … has a significant contribution to the cell resistance") — 집전체 \| SE 는 Li⁺ 차단 계면이라 들어간다면 전자 경로(51호 줄), `θ` 도 `A·j₀` 도 아닌 직렬 항.
- ★★ **Q5 스물일곱 번째 형태**: `[인쇄]` "(0.6 V vs. Li/Li+)25" — [25] = Zaghib 1999(23호가 LTO 1.55 V 에 단 편 · 3차 묶음 파일 32) · 음극 쪽 SE 안정의 실험 근거 [22][39] = Li₄Ti₅O₁₂ · LF 대칭셀 근거 [7] = 63호 S14(무 Li In) · 전압 그림 전부 "vs Li" 환산 축. `[재현]` In 첫 충전 끝 14.4–21.8 · 첫 방전 끝 7.5–9.9 at% · In 면 0.594 mA cm⁻².
- **채움표 64호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(4.6 V 가역 면적형 층 하나) · Q2 부분(첫 사이클 축 `R`·`C` — 우리 판독 · 호 정체 · 위치 미분리로 반 칸 검토 후 접음) · Q3 층(적합 ± 0 · n = 2 "representative" · 표 · 그림 뒤바뀜 둘) · Q4 0/64 **쉰여섯 번째 성질**("같은 이름의 호를 컷오프 넷에 걸쳐 비교하면서 그 `C` 가 ×250–700 다른 것을 묻지 않고, 부호가 뒤집히는 SOC 의존을 한 기구로 읽었다") · Q5 층 하나(스물일곱 번째 형태) · Q6 층 셋(≈70 MPa 한 값 · in situ 무가압 · 스윕 0) · Q7 해당 없음(층 하나 — SE 전하) · Q8 층 하나.
- **곱 축퇴 처방 마흔일곱 번째 적용**: 부분 적용 — 1단계 사이클 축 통과(노화분 저항형) · SOC 축 컷오프마다 갈림 · 3단계-b 4.0 V 탈락(호 정체) · 4단계 대용(평균 충전 전압 ↔ `I·ΔR` — 5.0 V ≈83 % · 4.6 V ≈31 %) 판정 불가 · 처방 표 세 줄(사이클 축 1단계 · 호 정체 검사 · 위치).
- ⚠ 어긋남 19 건(D1 하한 "2.7 V" ↔ 곡선 끝 2.57–2.62 V · D2 4.0 V 둘째 "74" ↔ 83.9 mAh g⁻¹ · D3 S5 첫 CE 4.0 ↔ 4.3 V 색 · D4 표 S8 5.0 V P–[S]n–P ↔ S⁰ · D5 4.6 V "more severe" ↔ 표면 조성 · D6 EIS "7 MHz to 1 Hz" ↔ 0.1 Hz · D7 초록 "thick" ↔ "thin" · D9 "only this thin interphase is responsible" ↔ 5.0 V 저주파 호 ≥2.5 kΩ · D10 S7 축 · D11 70 : 30 "optimal for the used material combination" ↔ 63호 LCO : LGPS · D12 LF 대칭셀 근거 [7] · D17 24 h 휴지 뒤 ×1.3–1.9 · D18 Fig. 8 S²⁻ · D19 음극 안정 근거 LTO 외).
- 낱말 지문: `redox` 26 · `interphase` 23 · `decompos` 29 · `current collector` 15 · `interfacial resistance` 11 · `capacitance` **1**(본문 — ESI 목록) · `contact` 6(측정 0) · `MPa` 2 · `optimal` 1 · `symmetric` 1 · `identifiab` · `LLI` · `LAM` · `reference electrode` · `exchange current` · `contact area` · `±` **0**.
- 그림: **15 항목 전부 봤다**(Fig. 1–8 · S1–S7; 1 쪽 래스터는 RSC 로고). 본문과 어긋난 그림: Fig. 1 캡션(2.7 V) · Fig. 2a(74 ↔ 83.9) · Fig. 3(24 h 휴지 ×1.3–1.9 · 1 Hz 뒤 자료) · Fig. 6d ↔ 표 S8 · Fig. 7c(준비 상태 Li₂S) · Fig. 8(S²⁻ 하나) · S5(첫 CE 색) · S6(0.1 Hz) · S7(a 패널 축). ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(15)이 추가됐다.
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**((차)에 정성 메모 — 두 노브 밖의 SOC 의존 가역 항 · 집전체 쪽 직렬 항).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 64호 행 · 64편 누적 · Evidence 쉰아홉 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](마흔일곱 번째 적용 · 처방 표 세 줄 · 주장하지 않는 것) · [[assb-interphase-vs-contact-loss-attribution]](정의 표 집전체 쪽 층 행 · 서명 표 두 행 · 64호 배정 행 · 처방 1 · 6–8 · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](스물일곱 번째 형태) · [[assb-apparent-capacity-decomposition]](64호 절 — 덧셈 항 · 첫 결손의 `η` 형 회복). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — 이 행 흡수 표시 · 서술 정정("`j₀` 쪽" ⚠ · 위치 집전체) · Hakari 2017 · Oh 2016 · Zhang W. 2017 *ACS AMI* 9, 35888 · Stegmaier 2017 신규 · Auvergniot 2017 지목 +1 · Zaghib 1999 지목 +1(다른 명제 — In 0.6 V) · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 26 행)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Hakari … Tatsumisago 2017 *Chem. Mater.* 29, 4768**([23] — "redox-active" 가설 원전 · 충 · 방전 양극 ex situ XPS) · **Oh, Hirayama, Kwon, Suzuki, Kanno 2016 *Chem. Mater.* 28, 2634**([37] — 운전 조성 In,LiInₓ 대칭셀 · 63호 G3 빈칸) · **Zhang W., Leichtweiss, Culver, Koerver, Das, Weber, Zeier, Janek 2017 *ACS AMI* 9, 35888**([30] — 탄소 · 22호 명제의 1차 후보) · **Stegmaier, Voss, Reuter, Luntz 2017 *Chem. Mater.* 29, 4330**([42] — 집전체 전위 강하) · Auvergniot 2017 *SSI* 300, 78([22]) · Zaghib 1999 *JPS* 81–82, 300([25] — 파일 32) · Sang … Nuzzo 2017 *Chem. Mater.* 29, 3029([44]) · Ito … Tatsumisago 2017 *JMCA* 5, 10658([29]) · Kato … Kanno 2016 *Nat. Energy* 1, 16030([6]).

## [2026-09-28] ingest | assb 29호 SI 보강 — Yanev, Auer, Pertsch, Heubner, Nikolowski, Partsch, Michaelis 2024, Supplementary data (J. Electrochem. Soc. 171, 050530)
- raw: `raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode-si.md` (sha256 봉인 · `si_sha256` · `supplements:` 원 digest · `parent_pdf_sha256` 참조) · 그림 `raw/figures/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode-si/` (자동 7 + 수동 3 — S1: 2 쪽 캡션 "Fig. S1 a) …" 누락 · Tab. S1 · Tab. S2: "Tab." 캡션 누락; 10 항목 전부 봤다). 새 호 번호 없음. **형식: 나중에 온 SI — 이 위키 첫 사례**(원 digest 불변 · 원 slug + `-si` 새 raw · 본문에 "원 digest 와 달라진 것" 표). SI 첫 쪽 제목은 투고 때 제목(PDF 생성일 = 수정본 접수일 2024-04-29) — DOI 접미 ad47d7 로 같은 편 확인.
- ★★★★ **Tab. S2**: dependency 0.95 초과는 sc90(`Q_M` 0.998 · `α` 0.998 · `n` 0.885) · sc90-BM(0.976 · 0.962 · 0.830) · **sc84(0.973 · 0.957 · 0.832)** — 본문 경고는 sc90 하나; `Q_M` ≈ `α` ≫ `n` 모양 = `Q_M`–`α` 쌍. 표준오차 · CI 0. 12 셀은 29호 Fig. 4 판독과 같고 **sc84-BM · sc90-BM 은 Tab. S2 ↔ Fig. 4 ↔ Fig. S7(적합선 재적합)이 서로 다르다**(`α` ×1.9 · 세 값).
- ★★★★ **Q4 ASSB 첫 반 칸 확정 — 반 칸 유지 · 누적 ≈20.0 그대로**: 이유 ① 해소 · ② ③ 그대로 · ④ 강화. `[재현]` dependency 순위 ↔ 창 끝 평탄 도달률 Spearman −0.991(야코비안 모사 넷에서 순위 재현 · 절대값은 못 함 — OriginPro 정의식은 프록시 차단으로 원문 미확인). `[도표]`+`[재현]` sc84 `Q_M` 236 > S6 형성 첫 CCCV 충전 ≈209 · sc90-BM 179–205 > ≈158 = 물리 상한 밖 — 진단이 옳았고 해석이 전파하지 않았다.
- ★★★ **나머지**: S1 = gran 네 셀 + TLM(계면 CPE, 값 0 → 처방 1단계 ❌ 확정) · S6 = 0.1 C CCCV "E vs Li"(OCP 0 그대로 · 조건당 셀 번호 하나) · sc90 첫 충전 ≈103 ↔ `Q_M` 60(방향 비대칭 — 비연결 아님) · Tab. S1 → `ε` = SE 부피비 × 0.85(`[인쇄]` 15 % 공극 가정 · 두께 계산값 → `τ ∝ (1−p)²`) · 공칭 200 mAh g⁻¹ · S3 입도(D50 3.3 · 10.4 µm) → BET ↔ 구 면적 ×1.65–4.3 → `D` ×2.7–18 · S8 = Table I(29호 D3 은 Fig. 6 · 7 쪽이 튄다 · D4 그대로).
- 보류 (가): 근거 있음 — 진단의 실재만, 축 문제는 그대로 — **결정 안 함**. (다) · (자) 정성 메모. 나머지 근거 0.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](Evidence 스물다섯 번째 ④ · 새 제약 4 · Status Log · 주장하지 않는 것 — **채움표 · 누적은 판정 불변이라 손대지 않음**) · [[assb-sensitivity-sweep-vs-identifiability]] · [[assb-lampe-contact-product-degeneracy]] · [[spm-grouped-parameter-identifiability]] · [[assb-apparent-capacity-decomposition]] · [[assb-tortuosity-factor-effective-conductivity-split]].
- ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 SI 항목이 추가됐다.

## [2026-09-28] ingest | assb 38호 SI 보강 — Conforto, Ruess, Schröder, Trevisanello, Fantin, Richter, Janek 2021, Supporting Information (J. Electrochem. Soc. 168, 070546)
- raw: `raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd-si.md` (sha256 봉인 · `si_sha256` · `supplements:` · `parent_pdf_sha256` 참조) · 그림 `raw/figures/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd-si/` (자동 8 + 수동 1 — S7: 선 4 개 벡터라 "그래픽 없음" 판정; 9 항목 전부 봤다 · 벡터 넷 S2 · S5 · S7 · S8 은 PDF 좌표로 읽음). 새 호 번호 없음 · 형식은 29호 SI 보강과 같다. PDF 생성일 = 수정본 날짜 2021-06-28.
- ★★★★ **S3 활성 질량 절차**: 이완 충 · 방 뒤 둘 다 1 h(38호 G2 해소) · 기준 = PC-NCM 액체 충전 가지 0.02 C 2 h / 휴지 2 h · x 0.26–0.97 · **4.19 V 에서 끝** — high-V N 1–6 이완 전위 4.191–4.219 V 는 곡선 밖. `[재현]` 세 판 → 예시 6.29 → 6.28 mg · Fig. 6 은 N ≥ 20 ±0.02 · N ≤ 10 −0.04…−0.08 · 감쇠 로그 몫 창 ≈51 % · 질량 ≈49 %. 기준 곡선 3.77 V 기울기 ≈0.53 V → `C_diff/m` 520 재현(38호 D6 바뀜 — 어긋나는 것은 본문 인용 0.38 V). 기준 전위 표류 비용(공통 모드) 10 mV ≈1–1.6 %.
- ★★★ **S8 적합 오차**: SC low-V 만(25 적합 중앙 · 최대 편차) — `L_diff,50` 1.52(1.28–1.73) → 1.89(1.53–2.32) → 2.06(1.70–3.84) µm; Fig. 8(c) 인쇄 1.3 µm 와 N = 1 부터 다르다 · PC 띠 0. **S9**: 도식뿐 — `√(t_c·D̃)` 안쪽 부피; 가는 선 · full capacity 출처 0. S8 폭을 대면 N40 닫힘 점 −15…+16 %.
- ★★★ **판정**: **38호 Q2 +0.5 선다(유지, 누적 ≈20.0 그대로)** — 결합은 한 방향 · 가름은 질량 채널 안 · EIS 채널 폭 약함. **D2 선다**(S3 재현이 셋째 크기 0.69). **D4 선다**(S2 → EIS 한 번 ≥2.5 h, 후보에 크기). S5 "very good agreement" 는 중앙값만(r90 13.6 ↔ 6.0 · 9.0 µm) · S7 `T` = 평균 `L_diff` 의 비(PC ×2.4 · 사이클 산포 6–12 % · SC low-V 38 사이클에서 끝 ↔ S6 · S8 40) · S2 SC 셀도 0.6 mHz 에서 용량성 극한 밖.
- 보류 (나): 근거 있음 — **결정 안 함**. (자) 정성 메모. 나머지 근거 0.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](Evidence 서른네 번째 ④ · 새 제약 4 · Status Log · 주장하지 않는 것 — 채움표 · 누적 불변) · [[assb-lampe-contact-product-degeneracy]] · [[spm-grouped-parameter-identifiability]] · [[assb-li-in-reference-potential-window]] · [[assb-synthetic-truth-contact-loss-requirements]].
- ⚠ 공통 모드 비용(1–1.6 %)은 raw SI digest 를 봉인한 뒤에 계산해 컴파일 페이지(Li-In 기준 전위 · 곱 축퇴 · 카드 새 제약)에만 있다 — 재료는 SI digest §2 의 S3(b) 추적 곡선.
- ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 SI 항목이 추가됐다.

## [2026-09-28] ingest | assb 65호 — Nam Y.J., Oh D.Y., Jung S.H., Jung Y.S. 2018, Toward practical all-solid-state lithium-ion batteries with high energy density and safety: Comparative study for electrodes fabricated by dry- and slurry-mixing processes (J. Power Sources 375, 93–101)
- raw: `raw/papers/nam2018_dry-vs-slurry-mixed-electrodes-binder-gitt-coverage.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/nam2018_dry-vs-slurry-mixed-electrodes-binder-gitt-coverage/` (자동 18 — 본문 8 · SI 8 · 표 2 + 수동 6 — Fig. 1 · Fig. 2: 자동 크롭이 서로 어긋남(`fig_1.png` 내용 = Fig. 2) · Table 1: 자동이 쪽 전체 · Table 2: 자동이 7 쪽 본문 문장 "…presented in Table 2. Fig. 8b shows…" 를 캡션으로 잡고 진짜 표(8 쪽)를 "중복" 으로 제외 · SI Fig. S2: 벡터 "그래픽 없음" · 초록 그래픽; 자동 항목의 잘못은 `figures.json` note 에 기록 — 24 항목 중 **22 개 열어 봤다**(안 연 2 = 쪽 전체 자동 표 크롭), 수치는 원본 래스터 · 600 dpi 벡터 렌더(Fig. 5 · 6) 픽셀 판독). **3차 묶음 파일 27**(일곱째 편 — 2차 묶음 큐 번호와 별개; 41호 Nam 2018 *JMCA* 와 다른 논문) · 원장 "★★ Nam·Oh·Jung·Jung 2018 · 지목 22 · 39 · 57 · Q1 · 건식↔슬러리 혼합 복합전극 미세구조·분리" · 22호 ref 17 · 39호 ref 13 · 57호 ref 25 · (지목 밖) 01호 ref 11 · 41호 ref 39. UNIST(Jung) · Elsevier 구독 논문 · 1차 측정(반쪽 13 전극 공정 대조 · 둘째 사이클 EIS · GITT · EDXS · 30 사이클 율 시험 · 완전지 펠릿 · 파우치). ⚠ SI PDF 메타데이터는 Word 생성 2026-09-28(출판사 SI 를 변환한 파일로 읽힌다).
- ★★★ **인용 귀속**: 22호 ref 17 "분리 · 미세구조" ⚠ 부분(윗면 · 단면 EDXS 정성 · 크기 의존 분리 없음 · 방향 "슬러리 > 건식") · 39호 ref 13 판정 불가(전사 0) · **57호 ref 25 ✅ — G8 풀림**: Fig. 5d 삼각형 넷 = `[재현]` 표 1 비 69.4 · 90.9 · 45.0 · **72.9 %(예비혼합 W85L/D85L — 바인더 함량이 아닌 공정의 점)** · "`D` 불변" = 액체셀 NCM622/Li GITT 1.72 × 10⁻¹¹ cm² s⁻¹ 고정 · "N₂ 흡착 상관" ⚠ 분모(BET 0.64) · "intermediate better contact" = 이 편 피복률 채널 단독의 이상치(같은 쌍 `R2` ×4.26 · 용량 −20 %) · 01호 ref 11 "5 성분" ✅(공극은 모식도) · 41호 ref 39 "슬러리 복합전극" ✅(41호 완전지 조성 = 이 편 파우치).
- ★★★ **(a) 미세구조**: 전부 전기화학 채널의 이름표 — `[재현]` 식 (1) ÷ BET ⇒ **피복률 = 1.2355 × ΔE_s/ΔE_t**(질량 · 통째 고립 약분 → 연결 입자의 부분 피복 `φ`, 척도는 `√D_LE` · BET · NCM111 `V_m`) · BET 등가 구 1.97 µm ↔ 2차 입자 ≈8 µm(외면 = BET 의 24.7 %) · 공극률 · 굴곡도 · 복합체 부분 전도도 0(SE 펠릿 3.2 → 자일렌 2.8 mS cm⁻¹ 뿐) · EDXS "more segregated" 정성 · N ↔ Ni µm 동시 위치(`[재현]` N ≈0.07–0.18 wt%).
- ★★★ **(c) 곱 축퇴**: 1단계 ❌(EIS 한 상태 · `R2` 만 · CPE 값 0) · **두 면적 채널 곱 `R2·φ` 2.93–11.34 Ω g %(×3.9 — 80 wt% `R2` ×4.26 ↔ `1/φ` ×1.10)** — 바인더 손잡이는 면적 하나가 아니다(57호 모델 명제의 실험판) · **첫 충전 상한** — 첫 방전 결손 중 통째 고립 몫 ≤19 · ≤21 · ≤42 % · ≈0 · ≤16 %(70L · 80L · 85L · 70H · 80H) · 예비혼합 이득 ≤29 %, 나머지는 방전 쪽 `η`(29호 SI 방향 비대칭의 공정 대조판).
- ★★ **(b) Q1**: `θ(N)` 0/65 — 사이클 축은 용량뿐: S6 0.1 C 복귀 c19 → c30 0 … −4.9 % · S8 예비혼합 −4.5 ↔ 무 −2.9 %(예비혼합이 더 빨리 준다 — 서술 0) · Fig. 8b 인셋 파우치 `[도표]` 109.9 → 102.3(12 사이클 −6.9 %, "stable").
- ★★ **(d) 셀 · Q5**: 반쪽 ∅13 mm PEEK · Li₆PS₅Cl 150 mg · Li₀.₅In 분말 · 370 MPa 동시 압착 · 적재 20 / 28 mg cm⁻²(기준 미인쇄) · **운전 압력 0**(파우치 492 MPa 제조 · 사진에 바인더 클립 둘) · **Q5 스물여덟 번째 형태** — 오프셋 값 0(`0.62` 0 회 · 전부 "vs Li/Li⁺") · Li₀.₅In 근거 [12] = Han … Hu 2017 *Nat. Mater.*(같은 편이 산화물 SE 하이브리드로 인용한 번호) · In 면 `[재현]` 0.1 C 0.24–0.49 · GITT 펄스 1.4–2.9 mA cm⁻². **(e)** M1 부분(분말 · 동시 압착 — 박의 방향 물음 없음) · M2 · M3 0.
- **채움표 65호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(신품 `θ₀` 층 둘 — GITT `φ` · 첫 충전 상한) · Q2 부분(신품 공정 대조 채널 넷 · 반 칸 검토 후 접음) · Q3 층(가져온 상수 · Ω g 정규화 · 본문 ↔ 표 어긋남) · Q4 0/65 **쉰일곱 번째 성질**("'면적' 을 가져온 상수로 척도하고 불확실성을 한 구로 닫으며, 두 면적 채널의 ×1.10 ↔ ×4.26 어긋남을 'perfectly agree' 로 읽었다") · Q5 층 하나 · Q6 층 셋(운전 0 · 바인더 클립 · 스윕 0) · Q7 해당 없음(층 하나 — N/P `[재현]` ≈0.96–1.16) · Q8 층 하나(1 C ≈175 mA g⁻¹ · QOCV).
- **곱 축퇴 처방 마흔여덟 번째 적용**: 부분 — 1단계 ❌ · 2단계 형식만 · 3-a · 3-b ❌ · 4단계 판정 불가 · 처방 표 세 줄(외부 기준 줄 여섯 번째 배정 — 액체 `D` + BET · 39호 `R·φ` 줄의 GITT 판 · 첫 충전 상한).
- ⚠ 어긋남 21 건(D1 0.1 C "0.17 mA g⁻¹"(`[재현]` ×1/100) · D2 예비혼합 92 → 129 ↔ 95 → 127 · D3 "W85L" ↔ 22 mg cm⁻² · D4 "slurry-mixed" ↔ 펠릿 양극 NBR 0 · D5 온도 뒤바뀜 · D6 4.2 ↔ 4.3 V · D7 110 ↔ 111 °C · D8 405 mAh ↔ 단층 112.9 · D9 "kg_cell" ↔ 적층 기준 · D11 [12] · D13 Fig. 3 0.1 C = 둘째 사이클 · D15 피복률 L 행 · D16 "perfectly agree" · D17 Ω g 절편 ×1.4 · D18 "dramatic" · D19 "stable" 외).
- 낱말 지문: `contact` 23 · `surface coverage` 8 · `GITT` 10 · `binder` 23 · `premix` 27 · `safety` 14 · `pressure` **0** · `MPa` 3(제조) · `porosity` **0** · `capacitance` · `CPE` **0** · `0.62` **0** · `identifiab` · `error` · `±` · `LLI` · `LAM` **0** · would/could/might 18.
- 그림: 본문과 어긋난 그림 — Fig. 1 캡션(d · e) · Fig. 3(0.1 C = 둘째 사이클) · Fig. 5(절편 질량배) · Fig. 6(범례 L/H 없음) · Fig. 7d(92 → 129 ↔ 94.8 → 126.9 · 22 mg cm⁻²) · Fig. 8b 인셋(c1 ≈110 ↔ 112 · −6.9 %) · S5(두 단면 모두 분리) · S8(예비혼합 빠른 감쇠). ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(24)이 추가됐다.
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**((자) 정성 메모 — GITT 는 √t 쪽만, `R/k` 대조 재료 없음 · (차) 정성 메모 — 바인더를 면적 + `j₀`(수송) 두 노브로 켜야 관측 쌍이 재현되는지의 짝).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 65호 행 · 65편 누적 · Evidence 예순 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](마흔여덟 번째 적용 · 처방 표 세 줄 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](65호 절 — 첫 충전 상한 · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](스물여덟 번째 형태) · [[composite-cathode-percolation-utilization]](65호 절 — 1호 ref 11 · 57호 Fig. 5d 원전 · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](65호 절 · 주장하지 않는 것). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — 이 행 흡수 표시 · 서술 정정 · Park 2016 · Kim 2017 · Choi 2017(GITT 피복률 방법 원전 셋) · Shin 2014(지목 2) 신규 · Gaberscek 2008 지목 +1 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 27 행 · §6-3-i 27 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Park … Jung 2016 *Adv. Mater.* 28, 1874**([16] — GITT 면적 식 · LiNbO₃ 코팅) · **Kim … Jung 2017 *Nano Lett.* 17, 3013**([21] — 바인더 차단 · GITT) · Choi … Jung 2017 *ChemSusChem* 10, 2605([22]) · Gaberscek 2008 *ESL* 11, A170([53] — 지목 +1) · Shin … Jung 2014 *Electrochim. Acta* 146, 395([38] — 63호 [52] 와 같은 편) · Sun … Amine 2012 *Nat. Mater.* 11, 942([55]) · Ito … Machida 2014 *JPS* 248, 943([48] — 선행 파우치).

## [2026-09-28] ingest | assb 66호 — de Biasi L., Kondrakov A.O., Geßwein H., Brezesinski T., Hartmann P., Janek J. 2017, Between Scylla and Charybdis: Balancing Among Structural Stability and Energy Density of Layered NCM Cathode Materials for Advanced Lithium-Ion Batteries (J. Phys. Chem. C 121, 26163–26171)
- raw: `raw/papers/debiasi2017_ncm-ni-content-operando-xrd-lattice-volume-energy-density.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/debiasi2017_ncm-ni-content-operando-xrd-lattice-volume-energy-density/` (자동 19 — 본문 10 · SI 7 · 표 2(Table 2 · Table S1) — **라벨 ↔ 내용 어긋남 0**, `tab_S1.png` 는 SI 6 쪽 부분(101 행 중 6 행) · Table 1 누락 · 초록 그래픽 캡션 없음 + 수동 5 — `tab_1_manual_p4` · `tab_S1_manual_p7/p8/p9` · `fig_TOC_manual_p1`; 24 항목 **전부 열어 봤다** + 대조용 22호 `fig_3` · `fig_S4`; 수치는 원본 래스터 픽셀 판독 · 표는 텍스트 층 정본). **3차 묶음 파일 28**(여덟째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★ de Biasi 외 2017 · Kondrakov 외 2017 — 지목 22 · Q8 · 격자상수 ↔ `x(Li)` 교정의 원전" — **두 편 묶음 행**(파일 29 = Kondrakov 24381 · 파일 31 = Kondrakov 3286 과 섞지 않았다) · 22호 ref 20 / SI ref 4. KIT BELLA · BASF SE · JLU Giessen · ACS 구독 · 1차 측정(액체 반쪽 · Li 금속 — **ASSB 아님**). PDF 메타데이터: 본문 = 출판사 조판(Arbortext · Distiller, 생성 2017-11-20) + 2026-09-28 내려받기 표지(iTextSharp) · SI = 저자 Word 2010(생성 2017-11-10 · author "de Biasi, Lea (INT)") + 같은 날 내려받기 표지 — 수령일 변환본 아님(65호 SI 와 다름) · SI 생성일이 본문 게재일(2017-10-31) 뒤.
- ★★★ **(a) `x(Li)` 축 = 통과 전하**: `[인쇄]` "The lithium content was calculated from the electrochemical data"(SI 캡션 넷 — 22호 교정 캡션도 같은 문장) · "we assumed that Coulombic efficiencies of less than 100% are a result of Li loss from the cathode material only" · 공칭 δ₀ 1.02 · ICP 0 — 교정 자체가 θ_ref = 1 · 부반응 0 · 결손 배정 규약을 품는다 ⇒ 22호 `f_inactive`(상 분율)는 교정 없이 서고(22호 판정 그대로), `x_active` · `η` · 용량 닫힘은 교정 셀의 전하를 빌린다. 원자료: 표 S1 — NCM 여섯 × δ 16–18 점(101 행, 넷째 충전 · 충전만) · `a` · `c` · `V` · `z` · TM–O · Li–O · U.
- ★★★ **(b) 두 교정의 x 이동** `[재현]`: 22호 교정(Fig. S4 `[도표]`)과 이 편 NCM622 가 같은 격자를 **x 로 ≈0.067 다르게 읽는다**(x 0.90–0.35 에서 0.057–0.082 로 거의 일정 — 가로 이동; 이 편 전처리 보정 0.09 와 같은 자릿수) — 22호 인쇄 오차 ±0.02 의 ×3 · 이 편 곡선이면 22호 닫힘 ±7 % → L · M +11…+16 %. `c` 최대 여섯 조성 모두 δ ≈0.45(NCM622 꼭짓점 ≈0.456 · 4.16 → 3.96 V) — 기구는 서사 + [19] 24381 위임(`Ni−O` 0 회). 22호 L ↔ M **못 가른다** — 같은 로트 원형 차(x 0.024–0.028) = 인쇄 L–M 차(0.03), 단조 채널 판정이 곡선 · 오프셋 모형에 따라 뒤집힌다. esd ≠ 산포(`V` 매끈한 곡선 잔차 ×14–37). Buchberger c/a 식(24호)은 NCM111 에 ±0.03 · NCM523 · 622 에 +0.02…+0.14(조성 특이).
- ★★ **(c) Q8 · `ΔV/V`**: 4.3 V −1.0…−5.7 % · 4.6 V + 1 h −2.3…−8.0 %(초록 "2.4 … 8.0 %") · NCM811 −4.9 / −7.35 % · −6 % ≈4.42 V(62호 "nearly 6%" 와 같은 자릿수 · 방향 = 충전 수축) · 23호 요구 중앙 8–10 % 는 범위 밖 · 23호 첫 충전을 θ = 1 로 옮기면 −1.3…−1.7 %(θ 0.8 → −4.2…−4.6 %) — 같은 용량에서 수축은 θ 에 걸린다. 3286 을 대신하지 않는다(수치 비교까지). 유지율 대조(75.1 → 98.1 %)는 Ni ↔ Umax 완전 교락 · 대조군은 Noh 2013.
- ★ **(d)** Q1 0/66 · 곱 축퇴 · 1단계 해당 없음(EIS 0 · 면적 채널 0) · **(e)** 코인 LP30 **또는** LP47 · 1C · operando 온도 · 압력 · 두께 미인쇄 · Q5 해당 없음(−100 mV 인쇄 · 근거 0).
- **채움표 66호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다 · Q2 없다(층 — 교정 원자료) · Q3 층(esd 만 · 전하 계수 축 · 외부 자료) · Q4 0/66 **쉰여덟 번째 성질**("교정 축의 가정을 방법 문장 하나로 닫고 esd 만 적었으며, 성분과 상한 전압을 한 축에 묶은 설계에서 유지율 차이를 '격자 밖 요인' 으로 돌리고, dQ/dU 와 dV/dU 가 공유하는 인자를 구조 기원의 증거로 읽었다") · Q5 해당 없음(층 하나) · Q6 없다 · Q7 해당 없음 · Q8 층 하나.
- **곱 축퇴 처방 마흔아홉 번째 적용**: 적용 불가(1단계 입력 없음) · 처방 표 경고 행 "SOC 추종 상 분율 줄의 교정 조건"(22호 줄에 붙음).
- ⚠ 어긋남 17 건(D1 원소 순서 · D2 Umax 4.4 · 4.25 ↔ Fig. 3 4.441 · 4.276 · D3 Fig. 3 ↔ 2b · D5 9b ↔ 사이클 전압 · D6 9a 정전압 제외 · D7 "about 1.5%" · D8 원형 ↔ 첫 행 `V` 부호 · D9 S5 0.94 ↔ 0.93 · D10 표 S1 오기 셋 · D11 esd ×14–37 · D12 NCM523 · 721 초반 지연 · D13 표 2 추세 · D14 Fig. 8 연쇄 법칙 · D15 설계 교락 · D16 전해질 · 1C · D17 COI ↔ BASF 외).
- 낱말 지문: `ICP` · `titration` **0** · `hysteresis` · `two-phase` · `inactive` **0** · `impedance` · `EIS` **0** · `pressure` **0** · `Ni−O` **0** · `contact` 1 · `identifiab` · `±` · `uncertain` **0** · believe · presumably · apparently · likely 11.
- 그림: 본문과 어긋난 그림 — Fig. 3 · Fig. 2b ↔ 3 · Fig. 9a · 9b · Fig. 8 · Fig. 10b · S4 · S5 · Fig. 7b. ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(24)이 추가됐다.
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**((나) 정성 메모 — 기준 곡선 축의 일정 이동은 Δx 에서 상쇄 · 모양 차는 상쇄 안 됨).
- 컴파일: **새 개념 1** [[nmc-lattice-li-content-calibration]](격자 ↔ `x` 교정의 축 규약 · 단조 채널 · 교정 간 이송 — 22 · 24 · 66호 표본 · `evidenceScope: multi-source-primary` · `confidence: low`) · 갱신 [[assb-contact-loss-vs-lampe]](채움표 66호 행 · 66편 누적 · Evidence 예순한 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](마흔아홉 번째 적용 · 처방 표 경고 행 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](66호 절 · 주장하지 않는 것 · 관련) · [[assb-operando-pressure-signal-attribution]](66호 주석 — `dV/dx` 비선형 · 관련) · `index.md`(새 개념 등록). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — 두 편 묶음 행 분리 · 이 편 흡수 표시 · 서술 정정 · Kondrakov 24381 지목 22 · 66 · Kondrakov 3286 지목 +1 · Ishidzu 2016 지목 +1 · Noh 2013 신규 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 28 행 · §6-3-i 28 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Kondrakov … Brezesinski 2017 *JPCC* 121, 24381**([19] — 파일 29 · `c` 붕괴 기구 · 22호 "Ni–O") · **Kondrakov … Janek 2017 *JPCC* 121, 3286**([15] — 파일 31 · `ΔV/V` 의 전압 · 기준 대조) · Ishidzu 2016 *SSI* 288, 176([13] — 파일 34) · Noh 2013 *JPS* 233, 121([10]) · Yang · Sun · McBreen 1999([36]) · Van der Ven 1998([38]).

## [2026-09-28] ingest | assb 67호 — Kondrakov A.O., Geßwein H., Galdina K., de Biasi L., Meded V., Filatova E.O., Schumacher G., Wenzel W., Hartmann P., Brezesinski T., Janek J. 2017, Charge-Transfer-Induced Lattice Collapse in Ni-Rich NCM Cathode Materials during Delithiation (J. Phys. Chem. C 121, 24381–24388)
- raw: `raw/papers/kondrakov2017_ncm811-charge-transfer-lattice-collapse-xrd-xas-dft.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/kondrakov2017_ncm811-charge-transfer-lattice-collapse-xrd-xas-dft/` (자동 14 — 본문 5 · SI 8 · 표 1(Table 2) — **라벨 ↔ 내용 어긋남 0**, `fig_S7.png` 는 (d) 아래 ≈12 pt 잘림 · `tab_2.png` 는 본문 ≈60 % 포함 · Table 1 누락 · 초록 그래픽 캡션 없음 + 수동 3 — `fig_S7_manual_p6` · `tab_1_manual_p3` · `fig_TOC_manual_p1`; 17 항목 **전부 열어 봤다** + 대조용 22호 `fig_S3`; 수치는 원본 래스터 · SI 600 dpi 렌더 픽셀 판독 · 표 · POSCAR 는 텍스트 층 정본). **3차 묶음 파일 29**(아홉째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★ Kondrakov 외 2017 24381 · 지목 22 · 66 · Q8·Q2 · `c` 붕괴 기구의 원전 후보 · 교정 `x` 축 규약도 확인할 곳"(66호가 묶음 행에서 분리 — 파일 31 = 3286 과 섞지 않았다) · 22호 ref 21 · 66호 [19]. KIT · BASF SE · HIU · SPbU · HZB · JLU Giessen · ACS 구독 · 1차 측정(액체 반쪽 · Li 금속 — **ASSB 아님**) + 계산(LiₓNiO₂ DFT). PDF 메타데이터: 본문 = 출판사 조판(Arbortext · Distiller, 생성 2017-11-01) + 2026-09-28 내려받기 표지(iTextSharp) · SI = Word 원고의 activePDF DocConverter 변환(생성 2017-09-07 = 수정본 접수일, title "Microsoft Word - 2517282_File000001_43888066.docx") + 같은 날 내려받기 표지 — 66호 SI(저자 Word 2010) · 65호 SI(수령일 변환)와 다르다.
- ★★★ **(a) 기구**: 현상(`c` 붕괴 · 두 슬랩 동시 감소 x < 0.45 · ΔV 의 76.8 % 가 x ≤0.5)은 측정 · "charge transfer between O 2p and partially filled Ni eg orbitals"(`[인쇄]` — 낱말 "Ni–O" 0 회) · 전자 구조 측정 둘(Ni K 연속 산화 · O K A1 증가)은 x 0.5 에서 안 꺾인다(`[도표]` Ni K 반높이 x 당 +1.4 → +4.5 → +4.4 eV) · **시점은 LiₓNiO₂ PBE(+U 0) 네 점의 Bader 꺾임 하나** — `[재현]` SI POSCAR 로 표 2 x = 1 · 0.75 · 0.5 는 재현(≤0.36 %)되나 **x = 0.25 는 안 된다**(`V` 98.63 ↔ 93.39 · `c` 13.62–13.64 ↔ 13.37) · 그 기하에 **O–O 1.331 Å 두 쌍 · Ni 둘 Li 슬랩 안(4 배위)** — 서술 0 · S8(d) −9 eV O 상태 ↔ 캡션 "Only slight changes". 22호 :168 "Ni–O 전하이동" ✅(기구) · "x ≈ 0.5" 는 축 규약 위(세 교정이 0.45 · ≈0.5 · 0.555 에 놓고 전압으로는 ≈4.0 V) · 66호 [19] "interslab 수축 → c" ⚠ 부분(`c` 감소의 절반은 TM–O 층).
- ★★★ **(b) `x(Li)` 축**: `[인쇄]` "estimated from current and charging time" · 전처리 셀(C/10 3.0–4.3 V, 횟수 미인쇄) 충전 첫 점 = **1.00**(결손 미배정) · 첫 사이클은 "first cycle irreversibilities (up to 14%) … delayed change in lattice parameters in the initial charge cycle" 때문에 피함 · 화학 분석 0 ⇒ 22호 1.02 · 66호 1.02 − 결손 · 67호 1.00 = **같은 연구망 세 규약**. `[재현]` NCM811 쌍(67 ↔ 66호): 전압 맞춤 +0.096…+0.112(= 규약 0.10) · 격자 맞춤 붕괴 구간 +0.123…+0.133(`V` · `c` 일치) → 시편 항 0 … +0.03(정전압 전하 미인쇄) · 초반 채널마다 +0.07…+0.17. NCM622 쌍(22호 첫 충전 ↔ 66호): 전압 맞춤 +0.157 → +0.033 — 분해 불가 ⇒ **66호 x 이동 ≈0.067 의 원인은 못 가른다**(NCM622 · 첫 사이클 교정 없음 · 전처리 횟수 미인쇄).
- ★★ **(c) Q8 · `ΔV/V`**(기준 = 전처리 셀 충전 첫 점): 4.6 V + 1 h −7.02 % · 4.3 V −4.9…−5.4 % · 4.2 V −2.5…−2.8 % · −6 % ≈4.4 V(62호 "nearly 6%" 와 같은 자릿수 · 66호 NCM811 −7.35/−6.95 % · −6 % ≈4.42 V) · 23호 중앙 8–10 % 는 범위 밖 · **23호 첫 충전 176 mAh g⁻¹ → 이 편 축 −4.0 % ↔ 66호 축 −1.3…−1.7 %**(축 규약만으로 ×2.4–3). 3286 을 대신하지 않는다.
- ★ **(d)** Q1 0/67 · `[인쇄]` "overpotentials arising during cycling, e.g., due to material fracture, lower the actual cell voltage"(`η` 몫에 이름, 양 0) · 곱 축퇴 · 1단계 해당 없음(EIS 0) · **(e)** 코인 EC:DMC 3:7(무게) · GF/D · Li · 25 °C · 파우치 사양 3286 위임 · scan "every 150 s" ↔ 쌍축 175.5 s/scan · hXAS P65 투과 · sXAS RGBL TEY(손 연마) · 적재 · 1C 0 · Q5 해당 없음.
- **채움표 67호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(`η` 몫 인쇄 층 하나) · Q2 없다(층 — 교정 규약 대조) · Q3 층(계산 행 재현 불가 · 상대 전하 축 · 표면 분광) · Q4 0/67 **쉰아홉 번째 성질**("전자 구조 측정 둘이 x 0.5 에서 꺾임을 보이지 않는 자리에서 격자 붕괴의 원인과 시점을 LiNiO₂ PBE 네 점의 Bader 꺾임 하나로 정하고, 그 계산의 절대 조성을 전하로 센 상대 축과 같은 눈금에 놓았으며, SI 기하가 표의 x = 0.25 행을 재현하지 않는 것을 적지 않았다") · Q5 해당 없음 · Q6 없다 · Q7 해당 없음 · Q8 층 하나.
- **곱 축퇴 처방 쉰 번째 적용**: 적용 불가(1단계 입력 없음) · 처방 표 66호 경고 행 보강("규약 항 ↔ 시편 항 — 전처리 셀끼리만").
- ⚠ 어긋남 18 건(D1 `a`(0.5) 2.8211 ↔ 2.8221 ↔ 그림 2.8207 · D3 슬랩 끝 값 항등식 13.692 ↔ 13.732 · D4 SI x = 0.25 기하 · D5 "up to 1.9%" ↔ +4.6 % · D6 부피 상쇄 · D7 scan 간격 · D8 hXAS x 범위 · D9 "nearly linearly" · D11 손실 비 · D12 두 경계 · D13 연쇄 법칙 · D14 반올림 라벨 · D18 66호 [19] 저자 누락 외).
- 낱말 지문: `Ni−O` **0** · `charge transfer` 7 · `Hubbard`/`+U` **0** · `dimer` · `migrat` **0** · `ICP` · `titration` **0** · `contact` · `pressure` · `EIS` **0** · `identifiab` · `±` · `error` **0** · indicate · suggest 21 · demonstrate · establish · inevitably 11.
- 그림: 본문과 어긋난 그림 — Fig. 2c · 3b · 2d/2e · 4 · 5 ↔ S6 · S2 · S7(d) · S8(d) · 1a ↔ 표 1. ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(17)이 추가됐다.
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**((나) 정성 메모 — 두 셀의 전하–전압 곡선은 규약만 빼면 ≈±0.01, 충전 첫머리는 모양 차).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 67호 행 · 67편 누적 · Evidence 예순두 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[nmc-lattice-li-content-calibration]](67호 절 · 표본 표 행 · 파일 29 흡수 표시 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](쉰 번째 적용 · 경고 행 보강 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](67호 절 · 주장하지 않는 것) · [[assb-operando-pressure-signal-attribution]](67호 주석) · `index.md`(개념 설명 한 줄). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — 24381 행 흡수 표시 · 서술 정정 · Kondrakov 3286 지목 +1(23 · 62 · 66 · 67) · Ishidzu 2016 지목 +1(23 · 66 · 67) · Noh 2013 지목 +1(66 · 67) · Seo 2015 · Li J. 2015 신규(☆) · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 29 행 · §6-3-i 29 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Kondrakov … Janek 2017 *JPCC* 121, 3286**([5] — 파일 31 · 첫 사이클 격자 지연의 크기 · 파우치 · 교정 절차 · `z_O`) · Ishidzu 2016 *SSI* 288, 176([4] — 파일 34) · Noh 2013 *JPS* 233, 121([2]) · Seo · Urban · Ceder 2015 *PRB* 92, 115118([17]) · Li J. … Dahn 2015 *Electrochim. Acta* 180, 234([7]) · Croguennec 2001([34]) · Petersburg 2012([14]).

## [2026-09-28] ingest | assb 68호 — Chen D., He H., Zhang D., Wang H., Ni M. 2013, Percolation Theory in Solid Oxide Fuel Cell Composite Electrodes with a Mixed Electronic and Ionic Conductor (Energies 6, 1632–1656)
- raw: `raw/papers/chen2013_sofc-miec-composite-electrode-percolation-theory.md` (sha256 봉인 — `pdf_sha256`, SI 없음) · 그림 `raw/figures/chen2013_sofc-miec-composite-electrode-percolation-theory/` (자동 13 — 본문 12 · 표 1 — **라벨 ↔ 내용 어긋남 0**, `tab_1.png` 는 14 쪽 거의 전체(과대) · `fig_12.png` 는 '5. Conclusions' 절 제목 포함(약간 과대) + 수동 1 — `tab_1_manual_p14`; 14 항목 **전부 열어 봤다**; 수치는 원본 래스터(그림 6–12 PNG) 픽셀 판독 · 식은 쪽 렌더 · 곡선 그림 일곱 장을 인쇄식으로 다시 계산). **3차 묶음 파일 30**(열째 편 — 2차 묶음 큐 번호와 별개; `ASSB_TRANSFER_NOTE.md` §6-3-c 의 "30 번 ZIP" 은 옛 큐 30 = 31호 자료) · 원장 "★ Chen·He·Zhang·Wang·Ni 2013 · 지목 22 · Q1 · 22호가 기댄 'percolation theory'(SOFC) — 01호 모델과의 관계" · 22호 ref 26. Jiangsu Univ. of Sci. & Tech. · HK PolyU · MDPI CC BY 3.0 · **SOFC(LSCF + YSZ) 해석 모형 — 실험 0 · ASSB 아님**. PDF 메타데이터: 출판사 조판 그대로(PScript5.dll 5.2.2 · Acrobat Distiller 10.1.5 · 생성 2013-03-11 18:27:53 +08:00 = 게재일, 수정 3 분 뒤) — **내려받기 표지 없음**(65–67호 ACS 파일과 다름).
- ★★★ **(a) 모형**: 좌표수 식 (2)([11] — Suzuki–Oshima 계열, `Z̄ = 6` 강체구 RCP) + 퍼콜레이션 확률 경험식 (5) `P = 1 − ((4.236 − Z)/2.472)^3.7`([31] Bertei & Nicolella 2011) + 목 `r_c = min(r) sin θ`(θ 29.5°, 출처 0) · 새로 한 것 = MIEC 배정(`P^i_LSCF = 1` · `P^e_LSCF = P_A`) · 노출 LSCF 표면 자리 식 (9)/(26) · LSCF–YSZ 입자간 전도도 `min(r)` 식 (18) · 무차원 곡선. `[재현]` `Z_NN = 6ψρ/(ψρ + 1 − ψ)`(ρ = SE/CAM Sauter 반경비 — 두 상 폭이 같으면 약분) — **CAM 만 키우면 연결 확률이 준다**(방향 ✅) · 크기는 비로만 · 연결 1 → 0 이 크기비 ×5.77 안 · 지면의 크기비는 1 · 2.5(이온 전도체가 같거나 큼)뿐.
- ★★★ **(a') 인쇄식 ↔ 그림**: 그림 6 · 8 은 인쇄 `P` 가 아니라 **`√P`**(그림 8 판독 0.806 · 1.030 · 1.228 · 1.399 ↔ `√P` 0.806 · 1.031 · 1.227 · 1.399 ↔ 인쇄 0.586 · 0.865 · 1.116 · 1.333 — 역산 지수 0.49–0.50) · 식 (24) 분자 `Z_LSCFk,YSZℓ` 오기(그대로면 문턱이 거꾸로) · 그림 7 은 식 (26) 의 `P^e P^i` 없이 · 그림 9 · 10 이름표 ↔ 곡선 값(색 규약 배정이 값을 재현) · 계산 예 r̄_YSZ 200 nm ↔ 재현 100 nm — **곡선 그림 일곱 장이 전부 인쇄식으로 재현되나 세 곳을 고쳐야 한다.**
- ★★★ **(b) 22호 정량 대조**(ψ 0.479–0.498 고상 · SE 입도 미인쇄 → 폭 · 인쇄 `P` · `√P`): 저자 배정 읽기로는 **S · M 을 맞추면(d_SE ≈4.9–6.5 µm) L 100 %**(측정 31 % · 용량 상한 44 % 초과) · 셋 최소제곱 S/M/L 0 / 2.6–3.6 / 34.8 %(측정 2 / 27 / 31) — 모형의 27 → 31 % 는 크기비 ×1.04–1.05, 22호 M → L 은 ×1.88 ⇒ **M ≈ L 평탄은 함수족 밖**(`Z̄` · 폭 · `P` 꼴 무관); 상한 읽기(`f_inactive ≥ 1 − θ^elec`)로는 모순 없는 d_SE ≥8.9–11.6 µm 에서 M 전자 비연결 ≤3 %p — M 의 27 % 는 거의 전부 전자 밖(22호 배정과 반대). 01호 SE 3 µm 를 넣으면 S 13–30 · M · L 100 %.
- ★★ **(c) SOFC ↔ ASSB**: 위상 구조(두 전도망이 한 상에서 겹침)만 닮음 · 소결 목 ↔ 압착 · `Z̄ = 6`(공극 ≈36 %) ↔ 치밀 압착 · 800 °C ↔ 25 °C · TPB ↔ 2상 CAM\|SE(짝 = Assumption 1) · 부피 변화 0 ↔ 2–8 % · **SOFC 식에는 용량 칸이 없다** · `P^i_LSCF = 1` 은 NCM 에 옮기면 안 되는 배정.
- ★★ **(d)** Q1 0/68 · 정적 `θ₀ = P^e(Z_NN)` 닫힌 식(층 하나 — 22호 대조 실패) · **곱 축퇴 기하 판**: `[재현]` Assumption 1 로 `λ^V = a_s · (Z_NS sin²θ/4) · P^e · P^i` ⇒ `A_eff ≙ φ_cov · P^e · P^i` — `j₀` 가 붙으면 한 곱; ASSB 로 옮기면 `P^e` 는 `ε_p`(= `LAM_PE`) 자리, `φ_cov` 는 `A_eff` 자리 — 합성 truth R1 · R7 의 두 변수가 한 식 안에 따로(정적). 적합 0 · 검증은 선행 편 시뮬레이션 위임.
- ★★ **(e) 01호**: 같은 양의 다른 계산(복셀 무작위 충전 · 10 배열 폭 ↔ 평균장 · 폭 0) · SE 3 µm 에서 문턱(θ/P = 0.4) d 3 → 15 µm: 01호 45 → 58 vol% ↔ 68호 35 → 73 %(인쇄 `P`) — 크기 민감도 ×3 · `[해석]` 01호 d 의존은 이산화(복셀 접촉 거리/d · 도메인/d) 가설 · 둘 다 22호 L 과대. **(f)** Q5 · Q7 해당 없음 · Q6 없다(접촉각 한 값).
- **채움표 68호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(정적 `θ₀` 층 하나) · Q2 없다 · Q3 층(computed-analytic · 검증 위임 · 인쇄식 ↔ 그림 세 곳) · Q4 0/68 **예순 번째 성질**("퍼콜레이션 확률을 평균 좌표수 하나의 결정론적 경험식으로 두고 인쇄한 식과 다른 함수(√P)로 그림을 그렸으며, 입도비 두 점 · 폭 두 점의 무차원 곡선을 '일반해' 로 내놓으면서 문턱 · 산포 · 검증 자료를 한 번도 적지 않았다") · Q5 해당 없음 · Q6 없다 · Q7 해당 없음 · Q8 해당 없음(층 하나).
- **곱 축퇴 처방 쉰한 번째 적용**: 적용 불가(입력 없음) · 해석식 안의 기하 곱 기록 — 처방 표 새 줄 없음.
- ⚠ 어긋남 17 건(D1 `P` ↔ `√P` · D2 식 (24) · D3 그림 7 · D4 그림 9 · 10 이름표 · D5 그림 11 서술 · D6 계산 예 · D7 L/r ↔ L/(2r) · D8 그림 8 캡션 · D9 전자 식 0 · D10 [4] = [26] · D11 [28] CdSe · D12 "0.3 to 1" 외).
- 낱말 지문: `threshold` **0** · `measur` · `fit` · `error` · `uncertain` · `±` **0** · `experiment` 3(서론) · `valid` 3 · `sinter` 0 · `pressure` · `battery` · `degradation` · `exchange current` · `overpotential` **0** · "sufficiently accurate" · "carefully checked" 1 씩.
- 그림: 본문과 어긋난 그림 — 그림 6 · 8(√P) · 7(P 미적용) · 9 · 10(이름표) · 11(서술) · 8(캡션 기호). ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(14)이 추가됐다.
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**((차) 정성 메모 — 면적 노브의 기하 매개화 해석식은 있으나 `j₀` 곱은 그대로).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 68호 행 · 68편 누적 · Evidence 예순세 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[composite-cathode-percolation-utilization]](68호 절 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](쉰한 번째 적용 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](68호 절) · [[assb-synthetic-truth-contact-loss-requirements]](R7 출처 · 상태) · `index.md`(개념 설명 한 줄). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — Chen 2013 행 흡수 표시 · 서술 정정 · Bertei & Nicolella 2011 신규(★) · Bertei 2012 · Chen D. 2011 · Suzuki & Oshima · Bouvard & Lange · Kenney 2009 신규(☆) · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 30 행 · §6-3-i 30 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Bertei · Nicolella 2011 *Powder Technol.* 213, 100**([31] — `P(Z)` 원전 · 인쇄식 ↔ `√P` 판정처) · Bertei · Choi · Pharoah · Nicolella 2012 *Powder Technol.* 231, 44([39]) · Chen D. et al. 2011 *JPS* 196, 3178([17] — 위임 검증) · Suzuki · Oshima 1983 · 1985([15] · [30]) · Bouvard · Lange 1991([16]) · Kenney et al. 2009 *JPS* 189, 1051([9]).

## [2026-09-28] ingest | assb 69호 — Kondrakov A.O., Schmidt A., Xu J., Geßwein H., Mönig R., Hartmann P., Sommer H., Brezesinski T., Janek J. 2017, Anisotropic Lattice Strain and Mechanical Degradation of High- and Low-Nickel NCM Cathode Materials for Li-Ion Batteries (J. Phys. Chem. C 121, 3286–3294)
- raw: `raw/papers/kondrakov2017_ncm111-ncm811-lattice-strain-particle-shrinkage-cracking.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/kondrakov2017_ncm111-ncm811-lattice-strain-particle-shrinkage-cracking/` (자동 13 — 본문 6 · SI 7 — **라벨 ↔ 내용 어긋남 0 · 잘림 0**, 캡션 필드 과대 3(`fig_1` · `fig_3` · `fig_6` 에 본문 문단) · `fig_S7` 캡션 끝 쪽 번호 " S6" · 초록 그래픽 캡션 없음 + 수동 1 — `fig_TOC_manual_p1`; 14 항목 **전부 열어 봤다**; 수치는 원본 래스터(그림 1 · 3 · 5 · 6) · SI 600 dpi 렌더(S1 · S4 · S6 · S7) 픽셀 판독 — 눈금 라벨 반올림(그림 3 · 5 · S7)은 틀 · 눈금 위치 적합으로 피함 · 자체 검사: (`a`, `c`, `z_O`) → 결합 길이 재계산이 그림과 ±0.002–0.004 Å). **3차 묶음 파일 31**(열한째 편 — 2차 묶음 큐 번호와 별개 · 파일 29 = 24381 = 67호와 다른 편) · 원장 "★★★ Kondrakov·Schmidt·Xu·…·Janek 2017 3286 · 지목 23 · 62 · 66 · 67 · Q1 · NCM811 부피 수축 %의 원전 · 첫 사이클 격자 지연의 크기를 x 로(22 ↔ 66호 NCM622 이동을 가를 열쇠)" · 23호 ref 41 · 62호 [31] · 66호 [15] · 67호 [5](본문 여덟 번). KIT BELLA · KIT IAM · HIU · BASF SE · JLU Giessen · ACS 구독 · 1차 측정(액체 반쪽 · Li 금속 — **ASSB 아님**). PDF 메타데이터: 본문 = 출판사 조판(Arbortext · Distiller 8.1.0, 생성 2017-02-08 −05:00) + 2026-09-28 내려받기 표지(iTextSharp) · SI = Word 2010 PDF(author "Kondrakov, Aleksandr (INT)" · 생성 2017-02-03 −05:00 = 게재일 뒤 · XMP 없음) + 같은 날 표지 — **SI producer 문자열이 UTF-16 BOM 뒤 1 바이트 문자 67 개**: 읽은 그대로(UTF-16 해독) 한자 · 기호가 섞인 33 자 ↔ 1 바이트 해독 "Microsoft® Word 2010; modified using iTextSharp.LGPLv2.Core 3.7.4.0" — 둘 다 raw 에 적었다.
- ★★★ **(1) `ΔV/V`** — 두 층위 · 두 조성 · 한 전압(4.3 V): 격자(in situ XRD · 신품 첫 충전 · C/10 · 4.3 V + 1 h · 원형 기준) NCM811 101.27 → 96.19 Å³(인쇄 쌍 −5.02 % · 그림 최저 −5.08 % · 초록 "around … 5.1%") · NCM111 −1.16 %("around 1.2") · 입자(광학 + DIC · 둘째 사이클 · 선형 배경 뺌) −(7.8 ± 1.5) · −(3.3 ± 2.4) % — ×1.5 · ×≈2.8. 대조: 66호 NCM811 4.3 V −4.86 / −4.45 % · 67호 −4.9…−5.4 % 와 같은 자릿수 ✅ · 62호 "nearly 6%" ❌ 이 편 값 아님(방향만) · 23호 요구 3–20 %(중앙 8–10) — `[재현]` 격자 δ 0.05–0.08 µm(낮은 끝) · 입자 0.08–0.12 µm(중앙 하단) · 23호 자기 충전량(θ = 1) −2.0…−2.4 % → 0.02–0.04 µm.
- ★★★ **(2) 첫 사이클 격자 지연**(`[재현]` 그림 3 원본 래스터 + 구간 직선 x): NCM811 첫 충전 앞머리 Δx ≈0.12–0.18 이 격자를 움직이지 않는다(3.770–3.778 V 평탄) · 같은 격자값 첫 − 둘째 충전 x: −0.07…−0.10 → 0(x ≈0.72–0.76) → +0.03…+0.09 → **x ≤0.45 에서 ±0.012** · 전압 맞춤 +0.15 → +0.005…+0.013(≥4.0 V) · NCM111 지연 없음(+0.03…+0.05 → x ≤0.6 에서 0) ⇒ **22 ↔ 66호 NCM622 ≈0.067 의 고 SOC 몫은 사이클 번호 항이 아니다**(격자 맞춤은 거의 일정 ↔ 사이클 항은 부호가 바뀌고 고 SOC 0) · 전압 맞춤 +0.157 → +0.033 의 저 SOC 모양은 사이클 항과 같다(빼면 ≥3.95 V 잔차 ≈+0.02…+0.035) · NCM622 는 이 편에 없다.
- ★★★ **(3) `x(Li)` 축**: `[인쇄]` "calculated from cycling data" · "on the basis of the integrated current" · 신품 첫 점 1.00 · 결손 이월(둘째 충전 0.894 · 0.939) · 광학 그림 ≈0.99 재설정 · 정규화 미인쇄(그림 Δx × 이론 용량 177 · 134 ↔ 인쇄 189 · 149 mAh g⁻¹) · 화학 분석 0 ⇒ **같은 연구망 네 번째 규약** · NCM811 `c` 최대 x 0.45(66) · 0.465(69) ↔ 0.555(67) — 결손 이월 여부로 정렬.
- ★★ **(a) 기계적 열화**: 부피 · 격자 측정 · 균열 정성(이온 밀링 단면 상태당 한 장 — 밀도 · 폭 · 입자 수 0) · 균열 → 용량은 두 조성 대비의 상관(초록 "establish" ↔ 본문 "a hypothesis that requires experimental proof") · 광학 균열 기여는 "linear background subtraction" 으로 뺐다 · **(a')** `[재현]` ε_c − ε_a 최대 3.4 ↔ 3.6 %p(같다) · 4.3 V 3.3 ↔ 0.8 %p — 4.3 V 에서 두 조성을 가르는 것은 부피(−1.2 ↔ −5.0 %). **(b)** Q1 0/69 · 곱 축퇴 · 1단계 해당 없음(EIS 0 · `impedance` 3 회 전부 추론). **(c)** 코인 LP57 100 µL · Celgard 2500 · 45 °C · C/2 · 파우치 4 × 2 cm² · 25 °C · C/10 · 폴리이미드 창 없음 · 75 s × 2 병합(`[재현]` 151 s/scan) · CeO₂ + pyFAI · TOPAS V5 · 중성자 HRPT(λ 1.1545 Å · FullProf · Li/Ni 4.3 · 6.8 %) · 장치는 [19] 로 재위임 · 파우치 전해질 · 분리막 · 구속 · 1C · 셀 수 미기재. **(d)** Q8 — NCM811 ΔV 의 ≈69 % 가 4.04 V 위(방전 용량 ≈25 %) · NCM111 −1.15 % · Q5 해당 없음(Li 음극 몫 인쇄) · Q6 없다 · Q7 해당 없음.
- **채움표 69호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(균열 기여 선형 배경 층 하나) · Q2 없다(층 — 입자 ↔ 격자 ×1.5) · Q3 층(단상 정련 · 결손 이월 축 · 2D 광학 · 정성 SEM) · Q4 0/69 **예순한 번째 성질**("두 조성 한 쌍의 네 관측(격자 · 입자 부피 · 균열 사진 · 용량)을 나란히 두고 인과를 초록에서 'establish' 로, 본문에서 '실험 증명이 필요한 가설' 로 적었으며, 균열이 입자 크기에 준 기여를 선형 배경으로 지운 뒤 남은 입자 수축(격자의 ×1.5)을 격자와 '직접 상관' 이라 불렀다") · Q5 해당 없음 · Q6 없다 · Q7 해당 없음 · Q8 층 하나.
- **곱 축퇴 처방 쉰두 번째 적용**: 적용 불가(1단계 입력 없음) · 처방 표 66 · 67호 경고 행 보강("첫 충전 교정을 옮길 때 사이클 번호 항을 저 SOC 값에만 따로 적는다").
- ⚠ 어긋남 25 건(D1 `V` 끝 96.19 ↔ 96.13 · D2 193 ↔ ≈178 · D3 비가역 12/14 % · D4 CE "well above 99%" · D5 "delayed change" ↔ "same behavior" · D6 `l_TM-O` 전압 · D8 x · 전압 짝 · D9 47 mAh g⁻¹ ↔ 3.5 % · D10 정규화 · D12 광학 `x` 재설정 · D13 Appendix S1 부호 · D14 ×1.5 · D15 "establish" ↔ "hypothesis" · D22 초록 그래픽 · D23 NCM111 균열 외).
- 낱말 지문: `pressure` **0** · `EIS` **0** · `ICP` · `titration` **0** · `LAM` · `inactive` · `isolat` **0** · `Ni−O` · `charge transfer` **0** · `contact` 2 · `crack` 9 · `fracture` 7 · `hypothesis` 1 · `establish` 3 · `delayed` 1 · `x(Li)` 21 · `±` 4.
- 그림: 본문과 어긋난 그림 — Fig. 1 가운데 · 위 · S4 · Fig. 3(비가역 · 결합 길이 전압 · `V` 끝) · Fig. 3 ↔ 광학 절 · Fig. 5(광학 `x` 규약 · 정전압 중 회복) · Fig. 6c · S1 · S7 · 초록 그래픽. ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(14)이 추가됐다.
- 보류 결정 (가)(나)(다)(아)(자)(차)(타): **근거 0 — 결정 안 함**((나) 정성 메모 — 기준 곡선이 첫 충전이면 3.9 V 아래 전위의 x 가 0.03–0.15 흔들린다) · (터) 근거 도착(교정 개념에 69호 절 — 유지 여부는 결정 안 함) · (저) 정성 메모(첫 충전 앞머리 격자 무응답 전하 — 상한이 느슨해지는 방향) · (하)(러) 근거 0.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 69호 행 · 69편 누적 · Evidence 예순네 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[nmc-lattice-li-content-calibration]](69호 절 · 표본 표 행 · 파일 31 흡수 표시 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](쉰두 번째 적용 · 경고 행 보강 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](69호 절) · [[assb-operando-pressure-signal-attribution]](69호 주석) · `index.md`(개념 설명 한 줄). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — 3286 행 흡수 표시 · 서술 정정 · Ishidzu 2016 지목 +1(23 · 66 · 67 · 69) · Noh 2013 재지목(행 없음) · Kasnatscheew 2016 신규(★★) · Gent 2016 신규(★) · de Biasi 2015 · Ghanty 2015 · Kim H.-R. 2016 · Kang 2008 신규(☆) · §3-b 표시 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 31 행 · §6-3-i 31 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Ishidzu · Oka · Nakamura 2016 *SSI* 288, 176**([17] — 파일 34) · **Kasnatscheew … 2016 *PCCP* 18, 3956**([31] — 첫 사이클 CE 결손의 정체) · Gent … 2016 *Adv. Mater.* 28, 6631([48]) · Kang … 2008 *Electrochim. Acta* 54, 684([30]) · de Biasi … 2015 *CrystEngComm* 17, 6163([19]) · Ghanty … 2015 *ChemElectroChem* 2, 1479([18]) · Kim H.-R. … 2016 *J. Electroanal. Chem.* 782, 168([46]) · Noh … 2013 *JPS* 233, 121([7]).

## [2026-09-28] ingest | assb 70호 — Zaghib K., Simoneau M., Armand M., Gauthier M. 1999, Electrochemical study of Li₄Ti₅O₁₂ as negative electrode for Li-ion polymer rechargeable batteries (J. Power Sources 81–82, 300–305)
- raw: `raw/papers/zaghib1999_lto-negative-electrode-spe-polymer-li-ion.md` (sha256 봉인 — `pdf_sha256`, SI 없음) · 그림 `raw/figures/zaghib1999_lto-negative-electrode-spe-polymer-li-ion/` (자동 5 — Fig. 1 · 2 · 3 · 4 · 6 — **라벨 ↔ 내용 어긋남 0**, `fig_1.png` 은 2 쪽 본문 두 단 포함(과대) · `fig_6.png` 은 5 쪽 전체라 Fig. 5(b) 포함(과대) · 캡션 필드 전부 합자 깨짐 + 수동 2 — `fig_5a_manual_p4` · `fig_5b_manual_p5`(캡션 탐지가 'Fig. 5.' · 'Fig. 5 (continued).' 를 놓침); 7 항목 **전부 열어 봤다** + 6 쪽 페이지 렌더; 수치는 PDF 원본 래스터(1 비트 스캔 ≈7000 × 4200–4600 다섯 · 8 비트 637 × 862 · 634 × 448 둘) 틀 · 눈금 적합 판독). **3차 묶음 파일 32**(열두째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★★ Zaghib·Simoneau·Armand·Gauthier 1999 · 지목 23 · 64 · Q5 · LTO 1.55 V 가정의 뿌리(액체셀) · 64호 [25] 재지목 — In 0.6 V(다른 명제) — 파일 32 에서 확인" · 23호 ref 44 · 64호 [25]. Hydro-Québec IREQ · Univ. de Montréal · Elsevier 구독 · 1차 측정 — **LTO 음극 · 무용매 SPE(POE-LiTFSI) · Li 금속 2전극 · 60/80 °C — ASSB 아님 · 원전 추적 편**. PDF 메타데이터: 헤더 `%PDF-1.7` · producer "Acrobat Distiller Command 3.01 for Solaris 2.3 and later (SPARC)" · creator · author 빈칸 · title = PII S0378-7753(99)00209-8 · 생성 1999-08-10 14:20:04 · 수정 1999-08-11 07:40:22 · XMP 0 · 단일 xref · Linearized · 조판 글꼴 · 이미지 XObject 9 — **내려받기 표지 없음**(68호 MDPI 부류). 텍스트 층 합자 깨짐(`Ž .` · `r` = `/` · `8C` = `°C`).
- ★★★ **(a) 1.55 V 의 정체**: `1.55` **0 회** — `[인쇄]` "approximately 1.5 V vs. lithium"(서론 · 인용 번호 없음) · "about 1.5 V"(결과) · "ASI at 1.6 and 1.5 V" 뿐. `[도표]` Fig. 4(C/12 · 2전극 · SPE · 60 또는 80 °C 미지정 · 1.2–2 V · 축 "V vs Li⁺/Li") 방전 평탄 중심 **1.542(20 mAh g⁻¹) → 1.504 V(110)**(−0.42 mV per mAh g⁻¹) · 충전 **1.666 → 1.600** · 차 0.09–0.13 V · 중점 ≈1.56–1.58 · 선 두께 ±0.015 · 1.2 V 도달 ≈159–162 mAh g⁻¹(인쇄 155/157) · OCV 시작 ≈2.90(인쇄 2.96) ⇒ (i) 이 편 측정 + (iii) 조건부, (ii) 인용 아님 · 1.55 는 이력 띠 안의 한 점(40호 1.575 도 안) · OCP · 3전극 LTO 전위 · dE/dT · 25 °C 전위 0(3전극 액체셀은 D 2 × 10⁻⁸ cm² s⁻¹ 에만). **23호 ref 44 ⚠ 부분**(재료 · 자릿수 ✓ · 1.55 · OCP · 25 °C ✗) · 23호 :464 "액체 전해질" ❌(SPE) · 원장 "액체셀" ❌ · 18호 [32,33] = Colbow 1989 · Ohzuku 1995(이 편 아님 — Colbow = 이 편 [1]) · 40호 인용 0(Costard 2017) ⇒ **읽은 범위에서 1.55 를 실제로 인쇄한 원전은 아직 0 편**.
- ★★★ **64호 [25] In 0.6 V**: In · indium · InLi · Li-In **0 회** · `In`(낱말) 2 = "In principle" · "In this work" · '0.6' 1 회 = 0.6 µm(1차 입자) ⇒ **이 편의 내용을 가리키지 않는다**(맞는 원전 추정 안 함).
- ★★ **(b) zero-strain**: 측정 0 — XRD 는 `[인쇄]` "before intercalation" 한 장(a 8.36 Å — `[재현]` Fig. 1 여섯 봉우리 8.359 ± 0.009 Å ✓) · "minimal dilation (<1%)" 인용 번호 없는 진술 · 참고문헌 4 편(Colbow 1989 · Zaghib 1998 · Ohzuku **1993** *JES* 140 · Nishizawa 1998)에 Ohzuku 1995 없음 · 62호 [37][39] 도 이 편 아님 ⇒ 무변형 가지의 원전이 아니라 전제로 쓴 응용 편.
- ★★ **(c) Q5 — 스물아홉 번째 형태** "하류가 '1.55 V' 로 인용한 원전에 그 숫자가 없다" · `[해석]` R-LTO 에 옮길 조건 다섯(층위 부하 ↔ OCP · 온도 dE/dT 0 · 조성 창 안 기울기 −0.04 V/90 mAh g⁻¹ · 계면 SPE ↔ 황화물 · 상대극 2전극) ⇒ "≈1.5 ± 0.05 V(부하 · 60–80 °C · SPE · vs Li 2전극)" 이상 못 좁힘 · P6 의 인용 하나 닫힘.
- ★ **(d)** Q1 0/70 · 곱 축퇴 해당 없음(LTO 음극 반쪽 · EIS 0 · ASI = DC 전류 차단 5 · 30 s) · **(e)** 4 cm² 실험 셀(Fig. 4) ↔ 사이클 셀 s852 1.75 Ah(60 °C) · s851 2.7 Ah(80 °C) 형식 미인쇄(`[재현]` 4 cm² 불가능) · SPE 조성 · 적재 · 도전재(0) · 압력 · 율 · 컷오프(사이클) · 셀 수 · 오차 0 · **사이클**(Q7/Q8 층): `[도표]` 60 °C 1.75 → 0.98 Ah/1495(−44 %) · 80 °C 2.70 → 1.53/995(−43 %) · 첫 100 사이클 −15 · −18 % · ASI ≈95–100 → 160(10) → 200(400) → 245(1000) → 270–292 Ω cm²(1490) · Effic. Ah ≈101 %(정의 미인쇄) · Wh 96 → 88 % ↔ "very stable" · "long life" · "exceptional stability" · DSC(HEBM 전구체 · 20 °C/min) 계단 440–468 °C · 바닥 −59.7 mW(포화 의심) · SEM 라벨 "lot 10 avant tt".
- **채움표 70호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나 — ASI(N) · 용량(N) 2전극) · Q2 없다 · Q3 층(셀 수 · 오차 0 · 삽입 전 XRD · 그림 0 인 D) · Q4 0/70 **예순두 번째 성질**("'zero-strain' · '<1 % dilation' · 'ASI very stable' · 'long life' 를 삽입 전 XRD 한 장 · 그림에서 ×1.7–3 오르는 ASI · −44 % 용량 위에 결론으로 적었고, 하류가 '1.55 V' 로 인용하는 값은 지면에 '약 1.5 V' 부하 전압 한 자리로만 있다") · Q5 층 하나 · Q6 없다 · Q7 해당 없음(층 하나 — CE ≈101 % ↔ −44 %) · Q8 층 하나.
- **곱 축퇴 처방 쉰세 번째 적용**: 적용 불가(1단계 입력 없음) · 처방 표 새 줄 없음.
- ⚠ 어긋남 17 건(D1 DST ↔ DSC · D2 D "more than" ↔ "about" · D3 OCV 2.96 ↔ ≈2.90 · D4 155/157 ↔ ≈159–162 · D5 ASI "very stable" ↔ ×1.7–3 · D6 "long life" ↔ −44 % · D7 4 cm² ↔ Ah 급 · D8 Fig. 2 캡션 ↔ 전구체 · D9 Fig. 3 "avant tt" · D10 311 라벨 중복 · D11 표기 · D12 "no structural change" ↔ "<1 %" · D13 Fig. 4 온도 · D14 Effic. Ah >100 % · D15 111 잘림 · D16 899–931 틈 · D17 PDF 헤더).
- 낱말 지문: `1.55` **0** · `1.5 V` 3 · `In` 2(낱말) · `indium` · `InLi` · `Li-In` **0** · `0.6` 1(µm) · `zero-strain` 5 · `plateau` · `hysteresis` · `polariz` · `ohmic` · `potential` **0** · `OCV` 1 · `ASI` 3 · `EIS` 0 · `pressure` 1(vapour) · `error` · `±` · `Table` **0** · `believe` 1 · `stab*` 6 · `long life` 4.
- 그림: 본문과 어긋난 그림 — Fig. 4 · 5(a) · 5(b) · 6 · 2 · 3 · 1. ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(7)이 추가됐다.
- 보류 결정 (가)–(로): **근거 0 — 결정 안 함**.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 70호 행 · 70편 누적 · Evidence 예순다섯 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](스물아홉 번째 형태 · 23 · 40 · 64호 절 주석 · P6 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](쉰세 번째 적용 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](70호 절) · `index.md`(개념 설명 한 줄). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — Zaghib 행 흡수 표시 · 서술 정정("액체셀" → SPE · "1.55 V 의 뿌리" → "약 1.5 V 부하 평탄, 숫자 없음" · "64호 [25] 다른 명제" → "내용 없음") · Costard 2017 행 보강 · Ohzuku 1995 · Colbow 1989 신규(★★) · Zaghib 1998 · Nishizawa 1998(☆) · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 32 행 · §6-3-i 32 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Costard · Ender · Weiss · Ivers-Tiffée 2017 *JES* 164, A80**(40호 [11] — 1.55 인쇄 후보로 남은 원전) · **Ohzuku · Ueda · Yamamoto 1995 *JES* 142, 1431**(18호 [33] · 43호 [41] · 62호 [37] — 1.55 V 와 zero-strain 의 공통 원전 후보) · **Colbow · Dahn · Haering 1989 *JPS* 26, 397**(이 편 [1] · 18호 [32] · 43호 [40]) · Zaghib · Armand · Gauthier 1998 *JES* 145, 3135([2]) · Nishizawa et al. 1998 *ESSL* 1, 10([4]).

## [2026-09-28] ingest | assb 71호 — Jung Y.S., Oh D.Y., Nam Y.J., Park K.H. 2015, Issues and Challenges for Bulk-Type All-Solid-State Rechargeable Lithium Batteries using Sulfide Solid Electrolytes (Isr. J. Chem. 55, 472–485)
- raw: `raw/papers/jung2015_sulfide-assb-bulk-type-issues-challenges-review.md` (sha256 봉인 — `pdf_sha256`, SI 없음) · 그림 `raw/figures/jung2015_sulfide-assb-bulk-type-issues-challenges-review/` (자동 17 — 그림 15 · 표 2 — **라벨 ↔ 내용 어긋남 0 · 누락 0**, 과대 7: `fig_2` · `fig_6` · `fig_10` · `fig_12` · `fig_14` 머리에 저널 로고 · `tab_1` · `tab_2` 쪽 전체; 17 항목 **전부 열어 봤다**(표 2 장은 축소본 · Fig. 5 · 8 캡션은 부분 렌더) — `figures.json` note 17; 수치는 PDF 원본 래스터(xref 99 · 108 · 119 · 127 · 148) 틀 · 눈금 적합 판독). **3차 묶음 파일 33**(열셋째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★★★ Jung·Oh·Nam·Park 2015 · 지목 23 · 41 · Q5 · In 0.6 V 가정의 인용 근거(리뷰) — Santhosha 2019 와 함께 In 가지의 원전 쌍" · 23호 ref 16 · 41호 ref 9 · (지목 밖) 62호 [3] · 63호 [10] · 65호 [6]. UNIST(Jung) · SNU · Wiley-VCH 구독 · **종설 — 1차 측정 0**(41 · 65호와 같은 연구실 · 다른 논문). 그림 1차/재인용: "Adapted with permission" 12 · 모은 도표 1(Fig. 2) · 모식도 2(Fig. 1 · 15) · 출처 표기 없는 판 1(Fig. 5c). PDF 메타데이터: 헤더 `%PDF-1.4` · creator "Arbortext Advanced Print Publisher 9.1.580/W" · producer "PDFlib PLOP 2.0.0p6 (SunOS)/OneVision PDFengine (Windows 64bit Build 25.092.S); modified using iText 4.2.0 by 1T3XT" · subject "Israel Journal of Chemistry 2015.55:472-485" · author · keywords 빈칸 · 생성 2015-05-08 11:47:12 +02:00 · 수정 2026-09-27 19:36:27 −07:00 · XMP 있음 · xref 1 · Linearized 0 — **내려받기 표지 쪽 없음 · 2–14 쪽 오른쪽 여백 세로 띠**(iText · 1 쪽 없음) — 65–67 · 69호(ACS 표지 쪽) · 68 · 70호(표지 · 띠 없음)와 다른 셋째 부류. 텍스트 층 기호 깨짐(`¢` = −, `8C` = °C).
- ★★★ **(a) In 영점의 정체**: 본문 p. 480 `[인쇄]` "a flat voltage plateau at 0.62 V (vs. Li/Li+) for the range of 0<x<1 in LixIn … [42b,62]" — **재인용**(Takada · Aotani · Iwamoto · Kondo 1996 *SSI* 86, 877 · Jung · Lee · Kim · Kwon · Oh 2008 *AFM* 18, 3010 = 41호 ref 33) · 온도 · 전해질 · 측정 0 · 옮겨 실은 이중 축 Fig. 8b([5a] Sakuda 2010 · −30 °C) · 9c([14a] Nagao 2012 · 25 °C) `[재현]` 오프셋 **0.600 ± 0.001 · ± 0.005 V** · Fig. 4 환산 축(Ti/SE/LiIn → "V vs. Li/Li⁺", 오프셋 미서술) · p. 477 "~2.3–2.4 V (vs. LiIn)" 암묵 환산(`[도표]` Fig. 6a 원 축 "Cell Voltage" · 첫 충전 ≈0.4 V 시작). `"0.6"` 전수 6 — 0.68 · **0.6 V = LGPS 구조 변화 전위**([35]) · 0.6–3.6 ×2(표 2 — `[재현]` [14a] = 0 V vs Li-In + 0.600) · 0.64 mA cm⁻² · **0.62 V(Li-In)** — "In 0.6 V" 0 · `1.55` 0.
- ★★★ **인용 사슬**: 23호 ref 16 **⚠ 부분**(자릿수 ✓ · 재인용 마디 · 무 Li In 박 ↔ "0<x<1" ✗) · "뿌리 한 가닥" → 중간 마디 · **41호 "두 번째 Jung 경로" → Jung 2008 한 뿌리로 합쳐진다** · 원장 "원전 쌍" ❌(종설 · Santhosha 와 서로 인용 0) · 42호 :177 은 인용 아님 · **64호 참고문헌에 이 편 0 회**(원문 전수 — (보) 사실 불변) ⇒ 읽은 범위에서 2019 년 이전 ASSB 편이 In 영점에 단 인용은 **Takada 1996 · Jung 2008(둘 다 미열람)로 수렴**(예외 64호 [25]).
- ★★ **같은 지면에 영점 두 관례** — 본문 0.62 ↔ 옮긴 그림 축 0.600 · 20 mV = 17호 평탄 폭 ±10 mV 의 두 배 · 48호 번역 NMC 충전 끝 ⩽2 mAh g⁻¹. ★★ **"0.6 V" = LGPS 변화 전위** — `[재현]` 두 관례로 Li-In 대비 0.00/−0.02 V = 상대극 자신의 전위(이 편은 잇지 않는다 · [35] 미열람 · `[도표]` Fig. 4a 환원 전류 0.60–0.62 V 에서 +3.5 … −6.0 · ≈0 V ≈−190 µA cm⁻²).
- ★ **(b) 카드에 닿는 명제**(거의 전부 재인용): 이 편 자신의 진술 셋(인용 0) — "morphology, percolation of SEs, and contacts" · 이상 구조(SE 균일 피복 + 탄소 배선) · LiₓMO₂ "low dimensional change" · 재인용: SE 30–65 wt% · 열간 압착 → 무공극 · 이용률 ↑ + 계면 반응 ↑([42v] · `[도표]` Fig. 13c ≈120 ↔ ≈54 mAh g⁻¹) · Li₇P₃S₁₁ 냉간 1.4 ↔ 치밀 17 mS cm⁻¹ · 코팅 기구 "either … or"(둘 다 `j₀` 쪽) · Li 공극 · 입계 성장 · **압력 값 0**(`pressure` · `MPa` 0 회) · `slurry` · `binder` · `dry` 0(65호 축 없음).
- ★ **(c) 62호 D21 확정**: *Isr. J. Chem.* 2015, 55(5), 472–485 · 접수 2014-07-20 · 수락 2014-11-14 · 온라인 2015-01-23 · "742" 지면 세 곳(우편번호 151-742 · [6b] 740–742 · [10a] A742) · "1–15" 0 · 조기 공개판 여부 확인 불가. 하류 문맥: 62호 [3] 서론 1 회 ✅ · 63호 [10] 서론 1 회("enlarge the operating voltages" ⚠ — 이 편은 황화물 창이 좁다고 인쇄) · 65호 [6] 서론 8 회(✅ 7 · 전달수 0.2–0.4 는 이 편에 없음).
- **채움표 71호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나 — 재인용 치밀화 ↔ 이용률) · Q2 없다 · Q3 층(종설 · 1차 측정 0) · Q4 0/71 **예순세 번째 성질**("계면 저항 감소의 기구를 'either … or', 열간 압착의 효과를 '이용률 ↑ · 계면 반응 ↑' 로 나란히 인쇄하고 가르지 않으며, 상대극 영점은 본문 0.62 V(재인용) · 옮겨 실은 그림 축 0.600 V 두 값으로 싣는다") · Q5 층 하나(**서른 번째 형태**) · Q6 없다 · Q7 해당 없음(층 하나) · Q8 층 하나(SE 창 재인용).
- **곱 축퇴 처방 쉰네 번째 적용**: 적용 불가(1단계 입력 없음 — 재인용 Nyquist Fig. 8a 는 판정 입력 제외) · 처방 표 새 줄 없음 · 곱 밖의 관찰 둘(재인용).
- ⚠ 어긋남 9 건(D1 0.62 ↔ 0.600 · D2 In/LiIn/Li-In · D3 "vs. LiIn" ↔ "Cell Voltage" · D4 thio-LISICON 2.2 ↔ 2.1 · D5 표 2 [14g] "0.2–0.5" · D6 Fig. 5c 출처 없음 · "30°" · D7 200 ↔ 210 °C · D8 [42b] 권 "86" · D9 Fig. 4 환산 축).
- 낱말 지문: `0.6`(부분) 6 · `0.62` 1 · `0.60` · `1.55` **0** · `In`(원소) 4 · `indium` 1 · `LiIn` 3 · `Li-In` 3 · `LixIn` 1 · `InLi` 0 · `counter/reference electrode` 1 · `pressure` · `MPa` **0** · `cold press*` 10 · `hot press*` 7 · `contact` 8 · `percolat` 1 · `tortuos` · `crack` · `impedance` · `EIS` · `LAM` · `LLI` · `identif` · `error` · `±` · `binder` · `slurry` · `dry` **0** · `Adapted with permission` 12.
- 그림: 본문과 어긋난 그림 — Fig. 8b · 9c · 6a · 8 · 4 · 5c · 13. ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(17)이 추가됐다.
- ⚠ raw 표기 결함 1: digest §(b) 표의 "첫 충전 뒤 LiCoO₂ | Li₂S·P₂S₅ 상호 확산 계면층" 행 — 칸 안 `|` 때문에 그 행만 열이 하나 밀린다(내용은 온전 · 쪽 "477" · 인용 "[5a]" · 층위 "재인용 — Fig. 7" · 축 "Q2 · 계면층 ↔ 접촉"). raw 는 한 번 쓴 불변층이라 고치지 않았다.
- ⚠ raw 판독 정정 1: digest 의 Fig. 14 절 "(g) HRTEM(Li₀.₀₈TiS₂ …)" 의 라벨은 원본 래스터(xref 164)를 2 배 확대하면 **"Li₀.₀₅TiS₂"** 로 읽힌다(digest 는 축소 크롭 판독). 우리 축 밖의 라벨이고 다른 판정에 쓰지 않았다 — raw 는 고치지 않는다.
- 보류 결정 (가)–(소): **(보) 사실 보강**(64호 참고문헌에 이 편 0) · **(차)(처) 정성 메모**(열간 압착 한 손잡이가 이용률 ↑ 와 계면 반응 ↑) · 나머지 근거 0 — **결정 안 함**.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 71호 행 · 71편 누적 · Evidence 예순여섯 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](서른 번째 형태 · 23 · 41 · 42 · 64호 절 주석 · P11 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](쉰네 번째 적용 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](71호 절) · `index.md`(개념 설명 한 줄). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — Jung 2015 행 흡수 표시 · 서술 정정 · Jung 2008 행 "두 경로" → "한 뿌리" · 지목 2 · Takada 1996 행 지목 5 · Shin 2014 행 지목 3 + 새 명제 · Sakuda 2010 · Kitaura 2011 신규 후보 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 33 행 · §6-3-i 33 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Takada · Aotani · Iwamoto · Kondo 1996 *SSI* 86–88, 877**([42b] — 지목 5) · **Jung · Lee · Kim · Kwon · Oh 2008 *AFM* 18, 3010**([62] — 지목 2) · **Shin · Nam · Oh · Kim · Kim · Jung 2014 *Electrochim. Acta* 146, 395**([35] — 지목 3 · LGPS 0.6 V) · Sakuda · Hayashi · Tatsumisago 2010 *Chem. Mater.* 22, 949([5a] — 0.600 이중 축 · −30 °C) · Kitaura · Hayashi · Ohtomo · Hama · Tatsumisago 2011 *J. Mater. Chem.* 21, 118([42v] — 열간 압착) · Nagao · Hayashi · Tatsumisago 2012 *J. Mater. Chem.* 22, 10015([14a]) · Sakuda · Hayashi · Tatsumisago 2013 *Sci. Rep.* 3, 2261([9]).

## [2026-09-28] ingest | assb 72호 — Ishidzu K., Oka Y., Nakamura T. 2016, Lattice volume change during charge/discharge reaction and cycle performance of Li[NixCoyMnz]O2 (Solid State Ionics 288, 176–179)
- raw: `raw/papers/ishidzu2016_ncm-ni-fraction-lattice-volume-change-cycle-fade.md` (sha256 봉인 — `pdf_sha256`, SI 없음) · 그림 `raw/figures/ishidzu2016_ncm-ni-fraction-lattice-volume-change-cycle-fade/` (자동 7 — 그림 5 · 표 2 — **라벨 ↔ 내용 어긋남 0 · 누락 0**, 잘림 2: `fig_1` 꼭짓점 이름 'LiCoO₂' · `fig_3` 세로축 '8.0' · '(%)' / 과대 2: `tab_1` · `tab_2` 쪽 전체 + 수동 4 — `fig_1_manual_p2` · `fig_3_manual_p3` · `tab_1_manual_p2` · `tab_2_manual_p3`; 11 항목 **전부 열어 봤다** + 네 쪽 110 dpi 렌더 · 600 dpi 부분 렌더 둘 — `figures.json` note 11; 수치는 **PDF 벡터 좌표**(그림 1–4 의 표지 원 · 틀 · 눈금 경로)에서 계산 · 그림 5 만 래스터 픽셀(5 µm = 118–119 px)). **3차 묶음 파일 34**(열넷째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★ Ishidzu·Oka·Nakamura 2016 · 지목 23 · 66 · 67 · 69 · Q1·Q8 · 조성별 격자 부피 변화 — 'Ni 가 많을수록 수축이 크다' 의 근거" · 23호 ref 48 · 66호 [13](원문 전수 **다섯 번** — 66호 digest 는 [13] 행에 둘(③ ⑤)만 배정 · ① ② 는 [15] · [19] 행에 전사 · ④ "lower redox potential of Ni than Co.13,29" 는 전사 0) · 67호 [4](한 번) · 69호 [17](네 번). Univ. of Hyogo(KIT · BASF 연구망 밖) · Elsevier 구독 · SSI-20 학회 논문집 4 쪽 · 1차 측정 — **액체 반쪽(Li 금속) · ASSB 아님 · 원전 추적 편**. PDF 메타데이터: 헤더 `%PDF-1.7` · creator "Elsevier" · producer "Acrobat Distiller 10.0.0 (Windows)" · 생성 2016-04-18 11:19:49 +08:00 · 수정 2016-04-28 10:39:32 Z · Info 의 author · subject · keywords 빈칸 · XMP 3,375 B(저자 · 키워드 · DOI · CrossMark · VoR · `prism:issueName` SSI-20 · **난독화된 71 자 이름의 빈 요소 하나** — 값은 옮기지 않았다) · `startxref` 1 · `%%EOF` 1 · Linearized · 태그 · 책갈피 7 · 글꼴 14 — **내려받기 표지 쪽 · 여백 띠 없음**(68 · 70호 부류).
- ★★★ **(a) `ΔV/V`**: 격자 층위 · 여섯 조성 · 4.5 V · 본문 수치 0 — `[도표]`(벡터) A(NCM111) **2.24** · B(Ni₀.₄₅Co₀.₁Mn₀.₄₅) **4.16** · Ni 0.5 두 점 **3.47 · 3.61**(C · D 이름표 0 — 그리기 순서로 C 3.47) · E(NCM622) **4.40** · F(NCM721) **5.76 %**. `[인쇄]` 정의 "at 2.5 and 4.5 V by normalization with the initial unit cell volume" ↔ `[재현]` 그림 2(c) **원형 첫 점 → 충전 끝 2.22 %**(그림 3 2.24 %) · 방전 끝(2.5 V) → 충전 끝 1.98 % ✗. `[재현]` 66호 SI 표 S1(원문 텍스트 층 101 행 — 4.3 V 값 재현 확인) 4.5 V 보간과 같은 조성 대조: NCM111 1.59/1.49 · 523 2.86/3.01 · 622 4.02/3.88 · 721 5.07/4.74 % ↔ 이 편 = **+0.4…+1.0 %p(×1.1–1.5)** · Li 함량 맞춤(NCM111)도 +0.24…+0.34 %p · 원형 `V` 101.24 ↔ 66 · 69호 100.50–100.53 Å³. 23호 요구치: `[재현]` δ = r[1 − (1 − ΔV/V)^{1/3}] r 3–4.5 µm — F 0.059–0.088 µm(틈 하단) · A 0.023–0.034 · 중앙(7.8–11.5 %)에 닿는 조성 0 · NCM811 없음.
- ★★★ **(b) 수준**: Ni ↑ → 수축 ↑ ✅(`[재현]` r 0.93 · B 비단조 · "guide for the eyes" 점선 넷 = 여섯 점 최소제곱선, 기울기 0.1 % 안 — 통계 인쇄 0) · → 유지율 ↓ 는 상관(r −0.88/−0.91 · `[인쇄]` "This may reflect") · **저자 배정은 계면 저항 R3 · 부반응**("The capacity fading was related to the impedance growth of the cathode/electrolyte interface") · **전기 고립은 부정**("Micro-crack formation may not generate electrically isolated particles" — 근거 = R2 가 "slightly varied", 표 2 ×2.6–3.0) · 균열 사진 두 조성 한 장씩 · 원형 0.
- ★★ **(c) `x` 축**: 정의 · 계수 · 정규화 · 사이클 번호 **인쇄 0**(가로축 이름표 = 식 "Li1-x MO2") — 그림 모양 원형 0 → 충전 끝 0.755 → 방전 끝 0.109(69호형 · 결손 이월) · **새 규약으로 세지 않음(규약 미인쇄 표본 · 연구망 밖 첫 표본)** · `[재현]` 이론 용량 277.8 mAh g⁻¹ per x 면 ≈210/≈178 mAh g⁻¹ ↔ 그림 4a 183 · NCM111 `c` 최대 Li ≈0.41 ↔ 66호 0.45 · 69호 0.53.
- ★ **(d)** Q1 0/72(층 하나 — R2 이름표 고립 배제) · 곱 축퇴: R 은 세 조성 × 여섯 점 · Q2 · Q3 적합했으나 인쇄 0 · 저자 곱 서술("When the particle fracture can simply enhance the interfacial area, the interfacial resistance should not be raised") · `[재현]` R3 ×10.6–34 · F 포화 · R3·A 227–316 Ω cm²(∅16 mm 가정) · R 합 × 0.1 C ≈52–73 mV · **(e)** ∅16 mm · 86:7:7 · ≈10 mg cm⁻² · ≈45 µm · in situ Be 창 · Cu Kα · 0.05 C · 사이클 3전극 0.5 C · 40 °C · 전후 0.1 C · 25 °C · EIS 4.5 V · 40 °C · 20 사이클마다 · 사이클 수 표 2 로 100 · 1C · 셀 수 · 기준극 · 3전극 전해질 · in situ 온도 미인쇄.
- **채움표 72호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나) · Q2 없다 · Q3 층(벡터 그림 · 축 인쇄 0 · R 만 · 두 장) · Q4 0/72 **예순네 번째 성질**("여섯 조성의 격자 부피 변화 · 용량 · 유지율을 나란히 인쇄하고 감쇠를 '부피 변화의 영향일 수 있다' 로 걸었다가 계면 저항(R3)에 배정하되, 전기 고립은 R2 이름표로 배제하고 R3 증가는 '면적만 늘면 오르지 않아야 한다' 는 곱 논증으로 부반응(`j₀`)에 돌리며, 그 곱을 가를 Q2 · Q3 는 적합하고도 인쇄하지 않았다") · Q5 해당 없음 · Q6 없다 · Q7 해당 없음 · Q8 층 하나.
- **곱 축퇴 처방 쉰다섯 번째 적용**: 적용 불가(1단계 `C` 미인쇄) · 처방 표 새 줄 없음 · 곱 안의 관찰 하나(저자 곱 서술 → `j₀` 끝을 가정으로 · `θ` 경로는 R2 이름표로 먼저 뺌).
- 귀속: 23호 ref 48 ✅ · G1 ⚠(하단 · 중앙 ✗) · 66호 [13] ①⚠ ②✅ ③✅ ④✅(재인용 마디 — Ohzuku [18,19]) ⑤✅(NCM111 추세)/⚠(고 Ni 격자 없음) · 67호 [4] ⚠ 과장("demonstrated · strongly" · 이 편은 고립 부정) · 69호 [17] ①⚠ ②✅ ③⚠(전압 · 조성 · 원형 격자 다름) ④✅.
- ⚠ 어긋남 15 건(D1 정의 ↔ 원형 쌍 · D2 Å³ · D3 부피 판 추가 점 넷 · D4 비단조 · D5 R2 "slightly" ↔ ×2.6–3.0 · D6 R3 증가율 지표 · D7 이온 반경(a 축 · Co³⁺ 0.61 ↔ 66호 0.545) ↔ c 축 수축 · D8 x 이중 · D9 초록 균열 한정 · D10 균열 표본 · D11 C · D 이름표 · D12 공칭 조성 · D13 4.5 V 두 값 · D14 오탈자 · D15 a 되오름).
- 낱말 지문: `contact` **0** · `pressure` **0** · `isolat` 2 · `crack` 9 · `fractur` 2 · `impedance` 10 · `interfac` 11 · `utiliz` 2 · `reference` **0** · `error` · `±` **0** · `Li content` **0** · `Rietveld` 0 · `least square` 2 · `capacitan` · `Nyquist` · `DRT` **0** · `LAM` · `LLI` **0** · `may` 6.
- 그림: 본문과 어긋난 그림 — Fig. 2(c)(단위 · 점 수 · 4.5 V 두 값) · Fig. 2(a)(되오름) · Fig. 3(비단조 · 정의 쌍 · 철자) · Fig. 3 · 4(C · D 이름표) · Fig. 5(표본 두 장 · A 단면 비구형). 자체 검사: 그림 2 짝 39 점 `V = (√3/2)a²c`(● −0.015 ± 0.002 Å³ · ○ −0.018 ± 0.019 — 열린 원 `a` 0.001 Å 반올림). ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(11)이 추가됐다.
- ⚠ raw 표기 느슨함 2: (i) digest 수집 목적 표의 "원문 전수 다섯 번(66호 digest 는 둘만 전사)" — 정확히는 66호 digest 가 [13] 행에 둘(③ ⑤)을 배정했고 ① ② 는 [15] · [19] 행에 문장째 전사, ④ 만 전사 0 이다. (ii) digest 판정 표 (a) 행과 Q1~Q8 표 Q3 행의 "격자 최소제곱" · "최소제곱" 은 **원형 분말 XRD(RINT-2200) 문장**("the lattice parameters were evaluated with the least square method")이다 — in situ 정련 방법은 미기재(같은 digest §2 실험 · §(c) 표에는 바르게 적었다). raw 는 한 번 쓴 불변층이라 고치지 않았고, 카드 채움표 행 · 교정 개념 표본 표 행에는 바르게 적었다.
- 보류 결정 (가)–(초): **(노) 근거 도착**(격자 층위 안의 연구실 간 폭 ×1.1–1.5 — 69호 층위 몫과 같은 크기) · **(터) 근거 도착**(연구망 밖 첫 표본 · 규약 인쇄 0 · 교정 개념에 72호 절 덧붙임 — 유지 여부는 결정 안 함) · (러) 정성 메모(반대 방향 서사 — 균열 → 고립 부정 · 근거는 이름표) · (차)(처) 정성 메모(균열 한 사건이 면적 ↑ · `j₀` ↓ 를 함께) · 나머지 근거 0 — **결정 안 함**.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 72호 행 · 72편 누적 · Evidence 예순일곱 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[nmc-lattice-li-content-calibration]](72호 절 · 표본 표 행 · 파일 34 흡수 표시 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](쉰다섯 번째 적용 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](72호 절) · [[assb-operando-pressure-signal-attribution]](72호 주석) · `index.md`(교정 개념 설명 한 줄). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — Ishidzu 행 흡수 표시 · 서술 정정 · Schmidt 2011 행 지목 +1(51 · 72) · Watanabe 2014(지목 66 · 72) · Woodford 2014 신규(★) · Nakamura T. 2013 · Muto 2009 · Shikano 2011 · Bishop 2014 · Sun 2009 신규(☆) · Noh 2013 재지목(행 없음) · §3-b (노)(터) 근거 · (러)(차)(처) 메모 표시 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 34 행 · §6-3-i 34 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Schmidt · Chrobak · Ender · Illig · Klotz · Ivers-Tiffée 2011 *JPS* 196, 5342**([21] — R2 배정 원전 · 지목 51 · 72) · **Watanabe · Kinoshita · Hosokawa · Morigaki · Nakura 2014 *JPS* 260, 50**([23] — 지목 66 · 72) · **Woodford · Carter · Chiang 2014 *JES* 161, F3005**([24] — 균열 역학) · Nakamura T. … Yamada 2013 *JPS* 244, 532([22]) · Muto … 2009 *JES* 156, A371([3]) · Shikano … 2011 *JPS* 196, 6881([4]) · Bishop … Tuller 2014 *Annu. Rev. Mater. Res.* 44, 205([14]) · Sun · Myung · Park 2009 *Nat. Mater.* 8, 320([7]) · Noh … 2013 *JPS* 233, 121([20]).

## [2026-09-28] ingest | assb 73호 — Minnmann P., Quillman L., Burkhardt S., Richter F.H., Janek J. 2021, Editors' Choice—Quantifying the Impact of Charge Transport Bottlenecks in Composite Cathodes of All-Solid-State Batteries (J. Electrochem. Soc. 168, 040537)
- raw: `raw/papers/minnmann2021_charge-transport-bottlenecks-tlm-ncm622-lpscl.md` (sha256 봉인 — `pdf_sha256`, SI 미수령 — 본문 언급 15 회) · 그림 `raw/figures/minnmann2021_charge-transport-bottlenecks-tlm-ncm622-lpscl/` (자동 6 — **누락 0 · 라벨 ↔ 내용 어긋남 0 · 잘림 0**, 캡션 문자열 넘침 3: `fig_1` · `fig_5` · `fig_6` 의 `caption` 끝에 본문이 붙었다(이미지는 온전); 6 항목 **전부 열어 봤다** + 식 1 영역 600 dpi 렌더 · 1 · 2 쪽 110 dpi 렌더 · 대조로 02호 Fig. 3 한 장 — `figures.json` note 6; 그림 여섯은 전부 JPEG 래스터 — 수치는 **PDF 원본 래스터(xref 242 · 354 · 460 · 54 · 57 · 132)의 틀 · 눈금 적합 픽셀 판독**). **3차 묶음 파일 35**(열다섯째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★★★ Minnmann·Quillman·Burkhardt·Richter·Janek 2021 · 지목 24 · 50 · 56 · Q3·Q4 · 차단 셀 + TLM 방법의 원전 — '덜 중요한 저항은 자유롭게 둔다' 관행의 출처인지" · 24호 ref 42 · SI 18 · 50호 SI 4 · 56호 ref 27 · 지목 밖 02호 ref 22 · 29호 ref 9 · 29호 SI ref 1 · 39호 ref 40(인용 digest 일곱 · 여섯 편; 27호는 인용 0 · 11 · 25호의 "Minnmann" 은 2022 종설). JLU Giessen(Janek) · ECS/IOP 오픈액세스 CC BY 4.0 · Editors' Choice 9 쪽 · 1차 측정 — **신품 · 방법 원전 추적 편**. ⚠ 2022 *AEM* 종설(파일 49)과 다른 편. 원장이 적은 다른 브랜치 앵커는 이 digest 의 입력이 아니다(읽지 않았다). PDF 메타데이터: 헤더 `%PDF-1.7` · creator "IOPP" · producer iText 5.5.13.5(IOP 판) · 생성 2021-04-24 · 수정 = 내려받기 2026-09-28 · XMP(저자 다섯 · VoR · CC BY 4.0) · EmbeddedFiles 빈 사전 · **IOP 내려받기 표지 1 쪽**(발의 IP 주소는 옮기지 않았다) · 여백 띠 없음(56호 부류).
- ★★★ **(a) 방법**: 차단 셀 두 종(이온 차단 SS \| 복합체 \| SS → σ_el · 전자 차단 In/(InLi)ₓ \| LPSCl \| 복합체 \| LPSCl \| In/(InLi)ₓ → σ_ion) + T형 TLM(식 1 인쇄 — Siroma 2015 "open-open") · 계면 비패러데이(0 % SoC) · 전자 레일 `r_el,1 + (r_el,2 ‖ CPE_el)` · 이온 레일 `r_ion` · 계면 `CPE_int` · 빼는 것 넷(고주파 오프셋 = 분리막 귀속 · In 계면 = 대칭셀 "considered" · 비패러데이 · 공극 "an average porosity of 14 % is assumed") · 회로 세부 · 적합 절차는 SI Section 1. **24호가 물은 "the less-important resistance was allowed to vary freely" · "A global model … beyond the scope" 는 본문에 없다**(`freely` · `fix` · `insensitiv` · `global` 0 회) — 관행의 구조(두 셀 · 셀마다 직류 끝 저항 하나 · 전역 적합 없음)는 Fig. 2 캡션에 있고 처리 문장은 SI — **판정 보류**. 굴곡도 규약 `[재현]` 확정 — 이온 φ_SE = 1 − Φ − 0.14(4/4 −2.9…+0.9 %) · 전자 φ_CAM = Φ(5/5 −2.5…−0.9 %) = 57호 규약 · 24호 D1 은 24호 자신의 것.
- ★★★ **(b) Q4**: 0/73 — 적합 오차 · 상관 · 파라미터 표 · EIS 시편 수 0 · 인쇄 적합값 42 vol% 한 쌍(`R_el` 107 · `R_ion` 360 Ω) · τ² 에만 정의 없는 ≈±20 % 막대. 합 셋(전자 차단 `Z(0) = 2R_In + 2R_SE + R_ion` · 고주파 오프셋 `2R_SE + R_el,1 ‖ R_ion` · 이온 차단 `R_el = L(r_el,1 + r_el,2)`) + 곱 둘(τ² · `CPE_int`). `[재현]` **두 셀 교차 대입**: 이온 차단 한 스펙트럼은 M1(이 편 — 호 = 레일 안 입자 간 전자 계면)과 M2(직렬 접촉 — 50호식)를 둘 다 맞추고(특성점 셋 = 미지수 셋), 전자 차단 저주파 호 폭(관측 ≥266 Ω · 50 mHz 미폐합)이 M1(277.5)을 고르고 M2(23.8)와 모순 — 판별값은 각 셀의 "덜 중요한 저항". 뺀 합 ≈100 Ω 은 `R_ion` 의 ≈59 %(25 vol%) → ≈1 %(61 vol%).
- ★★★ **(c) Q1 · Q3**: 조성 EIS Φ 24.6 · 32.2 · 41.6 · 52.9 · 61.1 %(`[재현]` 50 · 60 · 70 · 80 · 86 wt%) · 사이클 Φ 32.2 · 41.6 · 46.9 · 57.5 · 61.0 %(60 · 70 · 75 · ≈83.5 · 86 wt%) — 공통 셋 · 공극 14 % 인쇄(가정 · 13–17 % Table SIII · `[재현]` 42 vol% 시편 15.8 %) — **24호 "14 % void" 의 인쇄 자리 = 이 편(ref 42)** · `[도표]` σ_el 2.07e-5 → 1.44e-3 · σ_ion 4.17e-4 → 3.04e-6 S cm⁻¹ · τ²_ion 2.43 → 130 · τ²_el 121.5 → 4.34(본문 인쇄 수치 11 개와 맞고 D5 하나만 어긋남). **02호 Fig. 3** = 이 편 Fig. 2(a) ÷ 벌크(이온 5/6 — 가려진 Φ 32.2 점 없음 · 전자 6/6 · 순수 NCM 8.37e-3 기준) · 실험(공극 포함) ↔ 모의(고상) 기준 혼재(맞추면 ×1.3–1.7). **01호 `p_c(3 µm)` 45.3 vol%** ↔ 전자 σ 무릎 24.6 → 32.2 vol%(×11.5) · 32 vol% 무탄소 q_mat = VGCF 쌍의 0.87 — 같은 방향 네 번째(같은 연구실) · 68호 식은 SE 입도 미인쇄로 대입 불가(ρ_c 1.04 @Φ 24.6).
- ★ **(d) Q6**: 보고 · 통제 — 380 MPa × 3 min(이온 셀 두 번) · 분리막 100 MPa · EIS ≈40 MPa(힘 센서 + 스프링 — 이완 보상) · 사이클 ≈40 MPa(구속 형식 미인쇄) · 스윕 0. **(e)** PEEK ∅10 mm(0.785 cm² 인쇄) · NCM-622 BASF 3 µm · LPSCl NEI 1.6 mS cm⁻¹ · EIS 100 mg · 42 vol% 470 µm · VMP 300 · 10 mV · 7 MHz–50 mHz · 실온 · RelaxIS 3 · 반쪽 셀 12 mg(15.3 mg cm⁻²) · LPSCl 60 mg 분리막 · In/(InLi)ₓ 0.62 V(42호) · MACCOR · 25 °C · 200 mAh g⁻¹ 가정 · 셀 둘 · 전압 창 · 율당 사이클 수 미인쇄.
- **채움표 73호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나 — 신품 VGCF 개입 `θ₀` ≤≈13 %) · Q2 없다(반 칸 검토 후 접음 — 신품 `θ₀` ↔ `η`, `LAM` ↔ 접촉 아님) · Q3 층(fitted-EIS · 가정 공극 · 유도 τ² · 래스터 어긋남) · Q4 0/73 **예순다섯 번째 성질**("두 차단 셀로 각 운반자의 저항을 그 셀의 직류 극한에서 따로 떼는 설계를 쓰되, 다른 운반자 저항 · 분리막 · In 계면 · 공극의 처리는 SI 로 미루고, 두 셀의 교차 대입 · 전역 적합 · 적합 오차는 인쇄하지 않았으며, 굴곡도 인자에는 정의 없는 ±20 % 막대를 붙였다") · Q5 층 하나 · Q6 보고 · 통제(스윕 0) · Q7 해당 없음 · Q8 층 하나.
- **곱 축퇴 처방 쉰여섯 번째 적용**: 부분(1단계 `C` 미인쇄) · 처방 표 **후보 줄 하나 — "두 차단 셀 교차 대입"**(격상 결정 안 함) · 곱 안의 관찰(동역학 곱 `A·j₀` 은 비패러데이 가정으로 측정 밖 · 42 vol% `R_el` 의 ≈76 % 가 입자 간 전자 계면 — 점 접촉이 `τ²_el` 로).
- 귀속: 24호 ✅ 방법의 직계 · ⚠ "원전" 과장(이 편이 Siroma · Kaiser 선행을 인쇄) · ⚠ 굴곡도 규약 불일치 · 관행 문장 판정 보류 · 14 % ✅(57호 digest :328 의 물음을 닫음) · 50호 ✅ 차단 셀 발상 · ⚠ 계면 호 처리 반대 · 56호 ✅ void 14 % · ⚠ "SE 1–10 µm" 본문 0(인쇄는 "> 10 μm" · Table SV) · 02호 ✅ 옮김 · ⚠ 기준 혼재 · 29호 ✅ RelaxIS · ⚠ 회로 축약판 · 29호 SI ⚠ LPSCl 밀도 1.86 ↔ 이 편 인쇄 1.87 · ✅ 식 1 에서 (jω)^−1/2 구간(√t 논의 0) · 39호 ✅ 값 · ⚠ 양이 다름(기하 τ ↔ τ²).
- ⚠ 어긋남 21 건(D1 Fig. 6 q_mat 축 ↔ coarse 막대 = q_com · D2 53/52 vol%(실제 Φ 47) · D3 조성 집합 공통 셋 · D4 "four times" ↔ 9.4 · D5 "above eight" ↔ 7.4 · D6 47 ↔ 54.4 mS cm⁻¹ · D7 "best" 0.4 mS cm⁻¹ = 25 % 점 · D8 분리막 200–300 µm ↔ 치밀 409 µm · D9 Fig. 1 캡션 위아래 · D10 차원 문장 뒤바뀜 · D11 "214 mAh cm−2"(= 2.14 · 70 wt% 만) · D12 "x ≈0.3" ↔ 0.39 · D13 윗축 두 기준 · D14 순수 NCM 8.37e-3 ↔ 10 · D15 SI 참조 이중 · D16 고주파 오프셋 귀속 · D17 VGCF 수치 · D18 오탈자 · 서지 · D19 τ² 막대 정의 0 · D20 "improved contact" 측정 0 · D21 "slightly higher" ↔ ×2.6–5.1).
- 낱말 지문: `tortuosit` **33** · `blocking` 16 · `TLM`/`transmission line` 8 · `fit` 7 · `porosit` 13 · `void` **0** · `percolat` 8 · `isolat` 6 · `utiliz` 8 · `contact` 6 · `pressure` 8 · `MPa` 6 · `capacitance` · `CPE` **0** · `error` · `±` · `sensitiv` **0** · `freely` · `fix` · `global` **0** · `Bruggeman` 0 · `voltage` · `cut-off` **0** · `reference` **0** · `LAM` · `LLI` **0** · SI 항목 15.
- 그림: 본문과 어긋난 그림 — Fig. 1(D9) · Fig. 2(D5 · D14 · D19) · Fig. 3(D3 · D13) · Fig. 4(D17) · Fig. 5(D2) · Fig. 6(D1 · D20). 자체 검사: 특성점 판독(이온 차단 평탄 82.4 · 호 폭 24.6 · 전자 차단 ≥266)이 인쇄 쌍(107 · 360)과 맞고 · τ² 가 σ 에서 9/9 ≤3 % 로 재현 · q_com/q_mat = w 가 인쇄 밀도 + 14 % 로 Φ 위치와 ≤0.3 %p. ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(6)이 추가됐다.
- 보류 결정 (가)–(포): **(서) 번호 순서로 흡수됨** · (러) 신품 개입 표본 하나(VGCF 쌍 — 고립이 용량 스케일로) · (저) 같은 논리의 셋째 표본(충 · 방이 같이 늘면 고립 — 충전 값은 SI) · (하) 근거 하나(약 — 힘 센서 + 스프링 정하중 구속) · (너) 근거 하나(약 — PEEK ∅10 mm · 0.785 cm² 인쇄) · (오) 표본 하나(0.62 V 를 42호 인용으로 단일 표기) · (처) 정성 메모(SE 입도 한 손잡이가 σ_ion ↑ · σ_el ↓ · 접촉 서술을 함께) · 나머지 근거 0 — **결정 안 함**.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 73호 행 · 73편 누적 · Evidence 예순여덟 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-tortuosity-factor-effective-conductivity-split]](여덟 번째 표본 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](처방 표 후보 줄 · 쉰여섯 번째 적용 · 주장하지 않는 것) · [[composite-cathode-percolation-utilization]](73호 절 · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](서른한 번째 형태) · [[assb-apparent-capacity-decomposition]](73호 절) · [[assb-stack-pressure-operating-window]](73호 절 · 주장하지 않는 것) · `index.md`(굴곡도 개념 설명 한 줄). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — Minnmann 2021 행 흡수 표시 · 서술 정정 · 지목 +1(73) 열 행 · 신규 후보 셋(Siroma 2015 ★★ · Asano 2017 ★ · Amin · Chiang 2016 ☆) · 29호 SI 1.86 ↔ 1.87 · 56호 "1–10 µm" 메모 · §3-b (서) 흡수 · (러)(저) 표본 · (하)(너)(오) 근거 · (처) 메모 표시 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 35 행 · §6-3-i 35 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **이 편 SI**(Section 1 — 24호 관행의 원전 판정 · Section 3 — 14 % 도출 · Table SII–SV · Fig. S2–S4 — 오픈액세스) · **Siroma · Fujiwara · Yamazaki · Asahi · Nagai · Ioroi 2015 *Electrochim. Acta* 160, 313**([32] — 식 1 원전 · 원장 0) · Siroma … 2016 *JPS* 316, 215([26]) · Kaiser … Roling 2018 *JPS* 396, 175([25]) · Asano … Tatsumisago 2017 *JES* 164, A3960([27] · 원장 0) · Neumann … Latz 2020 *ACS AMI* 12, 9277([31]) · Bartsch … 2019 *Chem. Commun.* 55, 11223([58]) · Kato … Kanno 2018 *JPCL* 9, 607([33]) · Landesfeind … Gasteiger 2016 *JES* 163, A1373([42]) · Amin · Chiang 2016 *JES* 163, A1512([46] · 원장 0).

## [2026-09-28] ingest | assb 74호 — Park J., Zhao H., Kang S.D., Lim K., Chen C.-C., Yu Y.-S., Braatz R.D., Shapiro D.A., Hong J., Toney M.F., Bazant M.Z., Chueh W.C. 2021, Fictitious phase separation in Li layered oxides driven by electro-autocatalysis (Nat. Mater. 20, 991–999)
- raw: `raw/papers/park2021_fictitious-phase-separation-electro-autocatalysis-layered-oxides.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`, 보충 다섯의 해시는 `source_url_note`) · 그림 `raw/figures/park2021_fictitious-phase-separation-electro-autocatalysis-layered-oxides/` (자동 29 — 본문 5 · 표 1 · Extended Data 4 · SI 19 — **라벨 충돌 4**(ED 1–4 가 `fig_S1`–`S4` 로 저장돼 SI S1–S4 가 "중복(작은 쪽)" 으로 버려짐) · **누락 5**(S8 · S12 · S17 그래픽 없음 · S16 · S28 영역 없음) · **잘림 16**(크게 5 — `fig_5` 아래 1/3 만 · `fig_S7` · `fig_S20` · `fig_S21` · `fig_S24`) + 수동 25(본문 5 · SI 20); 54 항목 중 **연 것 27(자동 14 · 수동 13 — 셋은 위 띠만) · 안 연 것 27** + S26 원본 래스터 세 조각 · Source Data 로 다시 그린 Fig. 1 · ED webp 대조판 · 대조로 24호 `tab_S3.png` — `figures.json` note 54; 수치는 대부분 **PDF 벡터 좌표**(Fig. 2 · 5a · 5c · 5d · ED4 · S16 · S17) · Source Data CSV · STXM txt(`[데이터]`)). **3차 묶음 파일 36**(열여섯째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★★★ Park·Zhao·Kang·…·Chueh 2021 · 지목 24 · Q1·Q2 · 동역학이 만드는 가짜 상분리 — 24호 Fig. S17 의 θ 형 봉우리의 대안 설명이자 `i₀(x)` 의 출처" · 24호 ref 51 · SI ref 12(인용 digest 하나). Stanford(Chueh) · MIT(Bazant · Braatz) · LBNL ALS · SLAC SSRL · KIST · Springer 구독 · 보충(Source Data Fig. 1 b · c · e CSV 6 · STXM 스캔 넷 · ED webp · 영상 둘 — **판독 안 함** · 코드 `e-autocat` a75978c read-only) — **액체 반쪽(Li 금속 · LP-40) · ASSB 아님 · 원전 추적 편**. 사용자 결정(2026-09-28 "36 은 통과하자"): Fig. 1f CSV · NS_191114142 txt · Dataverse EMJFMU · AVP2I5(403) = 받은 자료에 없음 — 재요청 안 함 · 추정으로 채우지 않음. PDF 메타데이터: 본문 `%PDF-1.4` · creator "Springer" · producer 빈칸 · 생성 2021-06-22 10:58:31 +05:30 · XMP 29,084 B(VoR · `crossmark:MajorVersionDate` 2010-04-23) · 증분 갱신 1 · 내려받기 표지 · 여백 띠 · IP 표기 없음(68 · 70 · 72호 부류) / SI `%PDF-1.6` · Adobe InDesign CS6 · Adobe PDF Library 10.0.1 · 생성 2021-02-26 +05:30(수락 뒤 · 온라인 앞) · 책갈피 뿌리 "SpringerNature_NatMater_936_ESM.pdf".
- ★★★ **(a) 기구 · `j₀(x)`**: 식 S2(BV) · S3(`A = ∂J/∂c` — `[인쇄]` "a strongly concentration-dependent exchange current (large dj0/dc) can induce an autocatalytic effect … in one direction (A > 0) while being stable when the direction of reaction is reversed (A < 0)") · S4(FP) · S5(전류 제약) · 탈리튬 = 자촉매 · 리튬화 = 율과 무관하게 자억제 · 문턱 ∝ `j₀`(`[도표]` Fig. 5d 판 · 출발 1.0 → **0.231 C = 64 mA g⁻¹** · 0.95 → 0.304 · 0.90 → 0.469 · 0.88 → 0.651 C · 2.24C 이봉대 Li 0.779 → 0.675) · `[재현]` 큰 과전압 조건 `−d ln j₀/dc > (1 − α)(F/RT)|dU/dc|` 은 Li ≳0.92 에서만(우리 OCV 추정) · 온도 축 0 · 형상 둘. **네 추출**(`[도표]` Li 0.95: PITT 0.0053 · EIS 0.031 · 판 0.067 · 응집체 0.162 h⁻¹ · S17a 전압 부과 0.0034–0.0113 — **×48**; Li 0.50: 0.857 · 2.38 · 3.07 · 7.03 — ×8) — `[인쇄]` "Regardless of the scale, all curves show a similar composition dependency" · 측정량 = 용량 규격화 곱 `i₀·S/C`(식 S60 · S61) · `[재현]` `s_eff` = −(1 − c)·d ln j₀/dc 판 0.9–2.2 · EIS 3.3 → 1.4 · ED4 NMC111 Li 0.95 → 0.65 ×97 · Ni 많은 조성 ×0.11 · ×0.18. **24호 "`i₀(x)` 의 출처"**: 24호 SI 표 S3 ref 12 두 토막 식(`tab_S3.png` 열어 확인) = 판 곡선의 로그-선형 근사 **0.61–0.97 배** × 24호 면적 환산(V·ρ·m·SC/SA) — **모양 ✅ · 양 ⚠**(액체 · 규격화 · 방식 의존) · 24호 모델은 NMC 를 "one contiguous phase" 로 둬 모집단이 없다.
- ★★★ **(b) θ ↔ η 시간 궤적**: 인쇄 — 계속 충전 → 합쳐짐(Fig. 2b · `[데이터]` Source Data 과잉(Li ≥0.95, 느린 C/15 대비) 판 2.24C 최대 **+0.235**(XRD Li 0.84) → 충전 끝 +0.002 · 응집체 4C +0.213 → ≈0) · 리튬화 → 없음(빠른 방전 퍼짐 ≤ 느린) · 급랭(교환 차단) → 21 h 유지(S27 — 두 가설 모두 남긴다) · **셀 안 휴지 0**(S26 "15 min relaxation" 은 합쳐진 뒤 · Source Data 충 · 방 사이 휴지 0) · `[재현]` Python FP 이식(식 S20 `j₀` · D0 0.01 V · α 0.5): 2C 충전 뒤 휴지에서 이봉 **≈3–6 분** · 평형 ≈30 분 · 2C 역전 2.4 분 · 0.05C 감속 12 분 · **시간 ∝ 1/`j₀`**(λ = 1 · 10⁻² · 10⁻⁴ 정확히). **22호**: C/10 = 18 mA g⁻¹ = 원전 C/15(액체 단봉) · 자촉매 설명엔 ASSB `j₀(x≈1)` ≲ 액체 판의 **1/30**(`[재현]` 규모 논증) · 22호 ex situ(펠릿째 ≈5.1 h 스캔)는 **암묵적 휴지** → `θ` 쪽 조건부 근거 · 비활성 상 `c` → Li ≈0.99(M) · 0.97(L) `[재현]`(판별력 없음) · 무탄소 복합체의 **전자 접촉 옴 자촉매**(Fig. 4d "surface layers or electrical contacts")는 넷째 후보(`[해석]`). **24호 Fig. S17 조각 6**: 원전 두께 모의(S28)는 분리막 쪽(국소 2.67 C)이 가장 셈 — 방향 반대 · "방전 끝에 어디로 가는가" 는 가르지 않는다. **65호 첫 충전 상한**: 선다 · 느슨해진다(충전 쪽 자촉매 지연이 한 사이클 안에서 `θ` 와 같은 서명 · 완전 리튬화 출발에서 가장 큼) — 29호 SI 방향 비대칭에 셋째 성분.
- ★★ **(c) 곱 축퇴 · SOC 축**: 측정량이 처음부터 곱(`i₀·S/C`) · 원전은 `x` 의존을 고유(`(1 − c)ˢ`)에 배정 · `S(x)` 안 가름 · 신품 NMC111 계면 `R` Li 0.95 → 0.65 ×97–100 → 63호 SOC 축 1단계 '저항형' 이 **열화 없이** 생긴다 · ASSB 는 `S(x)` 도 움직인다(64호 가역 면적형) · 옴 접촉 `R_c(x)` 도 같은 모집단 서명(전류–과전압 모양으로 가름 — 53호 줄).
- ★ **(d) Q1 · Q2** — 둘 다 없다(반 칸 검토 후 접음) · **(e) 코드** — 식 S2 = BVSR.m:36–39 · S4 = fp_solver.m:132–142(⚠ `G` 부호: 인쇄 `J/η` ↔ 코드 `J/(−η)`) · S5 = :64–66 · :143–148 · 무유속 :141 · Fig. 5d = PS_sim.m(둘째 봉우리 두드러짐 · 최소 간격 0.1) · equilibrate_avg.m 그대로 실행 불가(:19 · :31–35) · 파라미터 · 역문제 코드 · 라이선스 0 · 이식 결과: 방향 비대칭 전 설정 · 2C 이봉 · 0.5C 는 D0 단위 · α 에 걸림(부분 재현) · **(f) 셀** — 파우치 · Li 170 µm · Celgard H2512 25 µm · LP-40 100 µL · 4 : 4 : 2 · ≈20 µm · 1 cm² · Be 판 가압(크기 0) · 형성 C/20 SOC 50 % · 방전 하한 2/2.5 V + 정전압 · 1C = 278 mAh g⁻¹ · 코인 30 °C 만 · 적재량 · 셀 수 · XRD 온도 미인쇄.
- **채움표 74호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나 — `θ` 형 서명의 비-`θ` 표본) · Q2 없다(반 칸 검토 후 접음) · Q3 층(measured-structure · measured-STXM · fitted-inverse · fitted-EIS/PITT · derived Bayes · 그림 어긋남) · Q4 0/74 **예순여섯 번째 성질**("자기 역문제(`j₀(c)` Legendre 21 계수)에 모형 선택 Bayes factor 를 임의 β 로 내고(2.4 — 두 모형의 최적 `k` 가 둘 다 사전 범위 경계), 전압 부과 · 전류 부과 두 추출이 절대값으로 ×1.2–20 갈리는 것을 그림에 두고도 모양 일치만 결론으로 삼았으며, 기각된 확산 모형에만 '비식별' 을 인쇄하고 추출 함수의 신뢰구간은 인쇄하지 않았다 — 입자 고립은 후보 목록에 없다") · Q5 해당 없음 · Q6 보고(크기 0) · Q7 해당 없음 · Q8 층 하나.
- **곱 축퇴 처방 쉰일곱 번째 적용**: 적용 불가(1단계 `C` 미인쇄) · 처방 표 **후보 줄 하나 — "SOC 축 신품 `j₀(x)` 기준선"**(격상 결정 안 함) · 곱 안의 관찰(측정량이 이미 곱 · `x` 의존 배정은 액체의 암묵 가정 위).
- 귀속: 24호 ① `i₀(x)` 식 ✅ 모양 · ⚠ 양 ② "reduced i₀ → increased bifurcation" ✅ 방향(원전은 율 문턱 명제) ③ 판별 입력 ⚠(휴지는 원전 0 · 방전 끝은 가르지 않음) ④ 대안의 원전 ✅ ⑤ ✅ · 원장 행 ✅ 흡수 · 정정 제안 넷(wiki 밖).
- ⚠ 어긋남 20 건(D1 출발 Li "0.96" ↔ 1.012 · D2 점선 평균 +0.047–0.065 · D3 ED4 ↔ 5c −1…−23 % · D4 전압 부과 ↔ 전류 부과 ×1.2–20 · D5 `G` 부호 · D6 "RT/FNt = 0.01" 단위 · D7 최적 `k` 사전 경계 · D8 5a 맨 윗칸 0 · D9 조건 이름 · D10 SI 교차 참조 · D11 오탈자 · D12 열째 사이클 · D13 ED1 셋째 · D14 [0.5, 1] 경계 쌓임 · D15 순방향 시연 `j₀` ≠ 추출값(비 ×12,350 ↔ ×154) · D16 Sup2 짝 · D17 "threshold rate" 실측 · D18 막대 정의 · D19 "unambiguous" ↔ Bayes factor 2.4 · D20 전하 ↔ XRD).
- 낱말 지문(본문 | SI): `autocatal` 26 | 22 · `fictitious` 29 | 8 · `j0` 16 | 47 · `diffusi` 45 | 64 · `relax` 6 | 11 · `quench` 7 | 12 · **`rest` 0 | 0** · **`isolat` 0 | 0** · `contact` 1 | 0 · `threshold` 12 | 1 · `pressur` 4 | 2 · `identif` 1 | 1 · `LAM` · `LLI` · `degrad` **0** · `ASSB` · `all-solid` **0**.
- 그림: 본문과 어긋난 그림 — Fig. 1(D1) · Fig. 2(D2 · D9 · D14) · Fig. 5a(D8) · 5c ↔ S17a(D4) · 5c ↔ ED4(D3) · S5(D12) · ED1(D13) · S26(휴지 띠가 합쳐진 뒤) · S28(D10). ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(자동 29 — 수동 25 는 `figures.json` 에만)이 추가됐다.
- ⚠ raw 표기 느슨함 2: (i) digest Q1~Q8 표 Q3 행("문헌 점과 ≈0.1–0.17 폭") · 보류 (터) 행("한 그림 안 출처 간 폭 ≈0.1–0.17 Li") — 정확히는 기준선 대비 −0.098 … +0.072 이고 출처 사이 폭은 **Li 0.9–0.96 에서 ≈0.04–0.05 · Li 0.6 근처 ≈0.17** 이다(카드 채움표 행 · 교정 개념 74호 절 · `index.md` 에는 바르게 적었다). (ii) digest Fig. 5d 항목의 "세로 C-rate(−1 … 2 · 음수 = 리튬화)" · "리튬화 쪽(음수)에는 음영 0" 의 '리튬화' 는 축 부호에서 읽은 `[해석]` 이다 — 그림에는 "Slow delithiation" · "Fast delithiation" 화살표만 있고 음수 구간 이름표는 없다(음영 0 은 그림대로). 판독 표의 "윗축 눈금과의 대조는 안 했다" 는 그 뒤 확인했다 — 윗축 1.0 · 0.9 · 0.8 · 0.7 · 0.6 이 누적 0 · ≈28 · ≈56 · ≈83 · ≈111 mAh g⁻¹ 에 앉아 Li = 1 − 누적/278 과 맞는다. raw 는 한 번 쓴 불변층이라 고치지 않았다.
- 보류 결정 (가)–(누): **(러)** 근거(경고 쪽 — `θ` 형 서명이 접촉 손실 없이 동역학으로) · **(저)** 근거(상한은 서되 느슨해짐 — 적용 조건) · **(차)** 근거(`j₀(x)` 모양이 노브 — PyBaMM `Chen2020` √ 꼴 `s_eff` ≈0.5 ↔ 원전 1–3 · Li 0.95 → 0.65 비 ×2.2 ↔ ×100) · **(터)** 근거 도착(교정 개념 74호 절) · (가)(다) 약 · (처) 정성 메모 · (도) 지목 +1(Gent 2016) · 나머지 근거 0 — **결정 안 함**.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 74호 행 · 74편 누적 · Evidence 예순아홉 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](처방 표 후보 줄 · 쉰일곱 번째 적용 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](74호 절 · 주장하지 않는 것) · [[nmc-lattice-li-content-calibration]](74호 절 · 표본 표 행 · 파일 36 흡수 표시 · 주장하지 않는 것) · `index.md`(교정 개념 설명 한 줄). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — Park 2021 행 흡수 표시 · 서술 정정 넷 · 지목 +1(74): Gent 2016(★ · 69) · Levi · Aurbach 1997(★ · 51) · 신규 후보 Tsai 2018 *EES* 11, 860(★★★) · Grenier 2017 *Chem. Mater.* 29, 7345(★★★) · Grenier 2020 *JACS* 142, 7001(★★) · Zhao · Bazant 2019 *PRE* 100, 012144 · Bazant 2017 *Faraday Discuss.* 199, 423 · Zhou 2016 *AEM* 6, 1600597(★) · Seidlmayer 2016 · Yin 2006 · Smith · Bazant 2017 · Fraggedakis 2020(☆) · §3-b (러)(저)(차)(터) 근거 · (가)(다) 약 · (처) 메모 · (도) 지목 표시 · 새 판단 거리 후보 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 36 행 · §6-3-i 36 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Tsai P.-C. … Chiang Y.-M. 2018 *Energy Environ. Sci.* 11, 860**([29] — 단일 입자 `j₀(x)`) · **Grenier A. … 2017 *Chem. Mater.* 29, 7345**([19] — 표면층 → 반응 이질성 · 문턱 낮춤) · **Grenier A. … 2020 *J. Am. Chem. Soc.* 142, 7001**([22] — 확산 대안의 원전) · Zhao · Bazant 2019 *Phys. Rev. E* 100, 012144([2] — `G` 부호 판정처) · Bazant 2017 *Faraday Discuss.* 199, 423([42]) · Zhou 2016 *Adv. Energy Mater.* 6, 1600597([16]) · Gent 2016 *Adv. Mater.* 28, 6631([43]).

## [2026-09-28] ingest | assb 75호 — Naik K.G., Vishnugopi B.S., Mukherjee P.P. 2022, Kinetics or Transport: Whither Goes the Solid-State Battery Cathode? (ACS Appl. Mater. Interfaces 14, 29754–29765)
- raw: `raw/papers/naik2022_kinetics-vs-transport-ssb-cathode-mesoscale-regime-map.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/naik2022_kinetics-vs-transport-ssb-cathode-mesoscale-regime-map/` (자동 19 — 본문 7 · SI 그림 7 · 표 5 — **오탐 1**(`tab_S1` = 본문 10 쪽 전체: ASSOCIATED CONTENT 목록 문장이 캡션으로 잡힘 · 진짜 SI 표 S1 은 "중복(작은 쪽)" 으로 버려짐) · **쪽 넘김 누락 1**(`tab_S2`) · **과대 2**(`fig_S4` · `fig_S7` — 그림 자체는 온전) · 잘림 0 + 수동 3(SI 표 S1 · 표 S2 연속부 · 초록 그래픽); 22 항목 **전부 열어 봤다** — `figures.json` note 22; 본문 그림은 전부 래스터라 수치는 원본 xref 픽셀 판독(판독 폭 digest §판독)). **3차 묶음 파일 37**(열일곱째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★★ Naik·Vishnugopi·Mukherjee 2022 · 지목 24 · Q4 · 24호 'not kinetically limited' 판정의 근거 — 민감도 분석이 있는지 확인 대상 (Q4 입구 후보)" · 24호 ref 54(인용 digest 하나 · 27호는 비인용 기록). Purdue(Mukherjee) · ACS 구독 · SI 13 쪽(ASSOCIATED CONTENT 목록과 하나씩 대응 — 빠진 보충 0) — **모형 편 · 자기 실험 0 · 검증은 73호 네 점**. ⚠ 같은 제1저자 Naik 2024 *AEM*(59호 [44])과 다른 편. PDF 메타데이터: 본문 `%PDF-1.3` · Arbortext Advanced Print Publisher 11.2.5208 · Acrobat Distiller 8.1.0 · iTextSharp.LGPLv2.Core 3.7.4.0 로 다시 씀(startxref 1 · 증분 갱신 0) · 생성 2022-06-27 −04:00 · XMP 3,161 B(VoR · Issue) · 여백 띠 "Downloaded from pubs.acs.org … by HANYANG UNIV user on 28 September 2026"(IP 없음 · 내려받기 표지 쪽 없음) / SI `%PDF-1.5` · Aspose.PDF for Java 19.3 · 생성 2022-05-15 −04:00(수락 전 수정본) · 같은 형식의 여백 띠.
- ★★★ **(a) 판정 기준**: 세 저항 순위(식 11–16: 두께 평균 BV `η` ÷ `I` · SE 상 강하 ÷ `I` · AM-CBD 상 강하 ÷ `I`) · 무차원수 0 · 용량 손실 분해 0 · 영역 지도(Fig. 7) 기준 · 조건 미인쇄 · `[재현]` 표 S3 여섯 점의 지도 이름표는 "큰 쪽" 과 안 맞고(60/34/6 = I 인데 `R_SE` 62 > `R_kin` 38) 절댓값 문턱(`R_kin` ≳26–38 · `R_SE` ≳62–94 Ω cm²)과만 맞는다 · 식 12 는 전류 가중이 아닌 두께 단순 평균 → 국소화가 `R_kin` 을 희석(`[재현]` 표 아홉 값의 함축 `i₀` 7.6×10⁻⁴–3.2 A m⁻² ×4,200 · `R_kin·a_s·L` 38.6–74.9) · 4 mA 의 `R_kin` 이 7 mA 보다 작다(BV 와 반대 — D4) · 표 값 시간 기준 미인쇄(S3 궤적 대조: 40 wt% = 방전 끝 값 · 80/6 `R_kin` 50 은 곡선 전 구간 아래 — D3) · 바꾼 변수 = 조성 격자 · 두께 · 전류 · σ_AM(OAT) — `k` · `c_e` · `D_s` · 입도 · 공극 · 온도 스윕 0 · 역문제 · 적합 0.
- ★★★ **(b) Q4**: 세 줄 표 첫 줄 한 칸(σ_AM OAT · 무탄소 세 조성 · 출력 끝 용량) · `identif` 4 = 전부 "identify" · 모형에서 `a_s·k·√c_e` 정확한 곱(`[재현]` `a_s` ×2 ≡ `k` ×2 ≡ `c_e` ×4) — `a_s` 만 흔들고 "point contacts or singularities" 로 이름 붙임 · σ_AM 포화를 "이온 수송 한계로의 전이" 로 읽음 — `[재현]` 40 · 60 wt% 포화는 AM 기준 209.5 · 210.5 mAh g⁻¹(AM 을 다 쓴 값) · `[재현]` 용량 축은 복합체 기준(지도 θ̄ 와 용량의 비 ∝ AM 분율) → AM 기준 끝 용량 40 → 60 wt% ±1 %(`a_s` ×2.0–3.4) — 40 wt% "동역학 한계" 의 용량 결손은 희석(`[인쇄]` "complete AM utilization") · 판정 규칙이 24호와 반대 방향(저항 크기 → 한계 ↔ 스윕 평탄 → 부재).
- ★★★ **(c) 24호 "not under kinetic limitation (Naik 2022 와 일치)"**: 결론 방향만 겹침 — 시험(`i₀` 스윕 ↔ 저항 순위) · 조건(C/10 충전 ≈0.15–0.30 mA cm⁻² ↔ 4–7 mA cm⁻² 방전 · Li₆PS₅Cl ↔ β-Li₃PS₄ κ₀ ×1/5 · 무탄소 ↔ CBD 3–6 % · ≈110–155 ↔ 70 µm · 공극 14 ↔ 5 %) 다름 · 무탄소 지도 띠에서 40 → I + III · 70 → III · 80 → II + III · `k` 2.57×10⁻¹¹ m^2.5 mol^−0.5 s⁻¹(출처 0)는 24호 SI 표 S3 일곱 식에 없음 · `c_e` 미인쇄(`[재현]` θ 0.5 `i₀` 0.065 ↔ 2.06 A m⁻²) · √ 꼴 `i₀(θ)` θ 0.65 → 0.95 ×2.19(74호 실측 ×97–100) · `[재현]` `ν²` 는 `c_e` 선택에 걸린다(1 → 전부 ≪1 · 1000 → 40 wt% 0.19–0.24 · 80 wt% 3.35–5.7).
- ★★ **(d) 모형 · 검증**: 균질 1D · 대칭 BV(α 0.5 식에 박힘) · 일정 `c_e` · 구 Fick · 기계 · 압력 · 접촉 진화 · 계면층("future study") · 이중층 · 음극 0 · 파라미터 뿌리 = 액체 LIB 편 셋(Chen 2017 · Vishnugopi 2020 · Kremer 2020) + LPS 편 하나(Garcia-Mendez 2020) — 행별 배정 0 · 검증 Fig. S5 "Experimental" = 73호 1C q_com(+0.7…+1.3)인데 **73호 조성 60 · 70 · 75 · ≈83.5 wt% 를 50 · 60 · 70 · 80 에 찍었다**(`[재현]` 73호 윗축 판독 + 반올림 경로와만 맞음) — 같은 조성끼리 대면 봉우리 60 ↔ 70 wt%.
- ★ **(e) Q1 · Q2** 0 · **(f)** 73호 τ² 가 DNS τ 의 ×1.9–5.9(방향 대조) · Bruggeman 대비 0.96 → 0.36 · 68호 "고립" 은 이름만(계산된 미이용은 율 의존 `η`) · SE 피복률 φ 모형 4.6–48 %(65호 GITT 5.8–25.2 % · 29호 3.1–85.2 %) · 63 · 64 · 74호 SOC 축 입력 0 · 27호와 같은 OCV 원전(Kremer) — `U₀` θ 0.89–0.95 비단조 +4.8 mV.
- **채움표 75호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나 — 신품 계면 면적 계산) · Q2 없다 · Q3 층(computed-DNS · computed-electrochemical · 미인쇄 기준 이름표 · 빌린 검증) · Q4 0/75 **예순일곱 번째 성질**("'kinetics ↔ transport' 를 세 저항의 순위로 가르되 영역 지도의 기준 · 조건과 저항 값의 시간 기준은 인쇄하지 않았고, 동역학 상수(`k` · `c_e`)는 한 번도 흔들지 않은 채 미세구조 활성 면적만 바꿨으며 — 모형에서 둘은 곱 `a_s·k·√c_e` 로만 들어간다 — 유일한 민감도 분석(σ_AM OAT)의 포화를 검사 없이 '이온 수송 한계로의 전이' 로 읽었다") · Q5 해당 없음 · Q6 없다 · Q7 해당 없음 · Q8 층 하나.
- **곱 축퇴 처방 쉰여덟 번째 적용**: 적용 불가(`R` · `C` 측정 0 — 모형 편) · 처방 표 새 줄 없음 · 곱 안의 관찰 둘(37호 줄의 균질판 · 57호 줄의 모형 표본 — CBD 한 손잡이가 `a_s` ↓ · τ ↑ · σ ↑).
- 귀속: 24호 ① "(Naik 2022 와 일치)" ⚠ 결론 방향만 ② G10 ✅ 공백 그대로 ③ Q4 열일곱 번째 성질 ✅ 선다 ④ 후속 표 "Q4 형 민감도 분석이 있는지" ❌ 없음 · 원장 §1 행 ✅ 흡수 · 정정 제안(wiki 밖) · 원장 §2 식별성 후보에서 제외 제안(wiki 밖).
- ⚠ 어긋남 17 건(D1 검증 이름표 · D2 캡션 표 번호 · D3 표 시간 기준 · D4 4 mA < 7 mA · D5 `R_SE` > `L/κ_eff` · D6 지도 ↔ 표 · D7 "almost identical" −21 % · D8 "115 to 50" ↔ ≈110 → ≈58 · D9 Fig. 6 어림 · D10 첫 점 σ ≈0.0019 · D11 "4-fold" ↔ ×5.1–6.1 · D12 τ 1.5 ↔ 1.69 · D13 용량 정규화 · `C₀` · D14 기호 · 교차 참조 · D15 `φ_e` 시각 · D16 밀도 4.7 ↔ 4.65 · `F` · D17 오탈자).
- 낱말 지문(본문 | SI): `kinetic` 50 | 8 · `transport` 76 | 10 · **`sensitiv` 2 | 0** · **`identif` 4 | 0** · `uniqu` · `uncertain` · `±` · `fit` · `LAM` · `LLI` · `pressur` **0** · `contact` 23 | 11 · `isolat` 5 | 0 · `percolat` 22 | 4 · `tortuos` 25 | 3 · `Bruggeman` 0 · `cutoff` 0.
- 그림: 본문과 어긋난 그림 — Fig. S5(D1 · D2) · 3a(D8) · 4f(D7) · 6a · 6c(D9 · D10) · 2b/S6a(D11) · 7(D6) · 3h(D15). ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(자동 19 — 수동 3 은 `figures.json` 에만)이 추가됐다.
- ⚠ raw 표기 느슨함 1: digest "수집 목적" 의 카드 `Naik` 적중 줄 번호(:2328 · :4988)는 **이 ingest 의 카드 편집 전** 기준이다(편집 뒤 :2331 · :5009). 그리고 같은 결의 적중 하나(편집 전 :467 — 59편 누적 문단의 "양극 압력 모델(Naik 2024)")를 목록에서 빠뜨렸다 — 셋 다 Naik 2024 *AEM* 이라 판정(이 편을 인용한 digest 는 24호 하나)은 그대로다. raw 는 한 번 쓴 불변층이라 고치지 않았다.
- 보류 결정 (가)–(수): **(차)** 근거(면적과 `j₀` 를 한 곱에 넣고 면적만 흔든 ASSB 모형 표본) · **(처)** 약(CBD 의 `j₀` 쪽을 선언적으로 뺌) · **(러)** 정성 메모(`θ` 도식 ↔ `η` 계산) · **(루)(무)** 약(√ 꼴 기본값 ×2.2 · θ → 1 소멸이 방전 끝 `R_kin` 봉우리) · **(수)** 약(무탄소 전자 한계는 SOC 상수 σ_AM — 자촉매 자리 없음) · **(호)** 약(표 S5 SE 1.5 µm 는 73호 본문에 없음 — SI 추정) · **(누)** 표본(약 — 73호 값이 남의 모형에서 이름표 이동) · (가)(다) 근거 0 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋: 24호 인용 자리 주석 표시 · "limitation 판정 기준 표기" 를 카드 수집 지침으로 격상할지(개념 처방 15 로는 붙임) · Hao · Mukherjee 2018 요청.
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 75호 행 · 75편 누적 · Evidence 일흔 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](75호 절 · 처방 15 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](쉰여덟 번째 적용 · 주장하지 않는 것) · [[assb-tortuosity-factor-effective-conductivity-split]](아홉 번째 표본 · 주장하지 않는 것) · [[composite-cathode-percolation-utilization]](75호 절 · 주장하지 않는 것) · `index.md`(민감도 개념 줄에 75호 갱신 한 구절 · 페이지 수 53 그대로). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Naik 2022 행 흡수 표시 · 서술 정정 · §2 식별성 후보 제외 제안 · 지목 +1(75) 아홉 — Shi 2020 *AEM*(4 → 5) · Koerver 2018 *EES*(3 → 4) · Barai 2021(1 → 2) · Davis 2021(1 → 2) · Zhang W. 2017 *ACS AMI* 35888(2 → 3) · Kremer 2020(1 → 2) · Kasemchainan 2019(2 → 3) · Krauskopf 2019 *ACS AMI*(1 → 2) · Bucci 2017 *JMCA*(묶음 행 1 → 2) · 신규 후보 Hao · Mukherjee 2018 *JES* 165, A1857(★★) · Mistry 2018 *ACS AMI* 10, 6317 · Vishnugopi 2020 *JES* 167, 090508 · Li M. 2021 *Adv. Mater.* 33, 2008723(★) · §3-b (차)(처)(러)(루)(무)(수)(호)(누) 표시 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 37 행 · §6-3-i 37 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Hao F. · Mukherjee P.P. 2018 *J. Electrochem. Soc.* 165, A1857**([43] — 같은 연구실 ASSB 계면 메조 모형) · Mistry 2018 *ACS AMI* 10, 6317([62] — `a_s` 방법 원전) · Vishnugopi 2020 *JES* 167, 090508([60] · SI 2) · Li M. 2021 *Adv. Mater.* 33, 2008723([58] — 무탄소 · 혼합 전도체).

## [2026-09-29] ingest | assb 76호 — Davis A.L., Goel V., Liao D.W., Main M.N., Kazyak E., Lee J., Thornton K., Dasgupta N.P. 2021, Rate Limitations in Composite Solid-State Battery Electrodes: Revealing Heterogeneity with Operando Microscopy (ACS Energy Lett. 6, 2993–3003)
- raw: `raw/papers/davis2021_operando-microscopy-graphite-lpscl-composite-current-focusing.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/davis2021_operando-microscopy-graphite-lpscl-composite-current-focusing/` (자동 25 — 본문 6 · SI 그림 18 · 표 1 — **잘림 2**(`fig_S12` 범례 · `fig_S14` A · B 패널 → 수동 크롭) · **캡션 오탐 1**(`fig_S18` — 본문 문장이 캡션 칸 · 그림은 맞음) · **과대 3**(`fig_S7` · `fig_S13` · `tab_S1` — 내용 온전) · 누락 0 + 수동 3(SI S12 · S14 전체 · 초록 그래픽); 28 항목 **전부 열어 봤다** — `figures.json` note 28; 본문 그림은 전부 래스터라 수치는 원본 xref 픽셀 판독 · S11 · S12 는 벡터 좌표 · 깊이 분포는 우리 HSV 색 분류(반정량 — 판독 폭 digest §판독)). **3차 묶음 파일 38**(열여덟째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★★ Davis·Goel·Liao·…·Dasgupta 2021 · 지목 24 · 75 · Q2 · 황화물 복합전극의 operando 광학 η(z) — EDXRD 와 독립인 깊이 채널 · 75호 [56] 재지목 — 입도 · 경로 묶음" · 24호 ref 39 · 75호 [56](인용 digest 둘). Univ. of Michigan(Dasgupta · Thornton) + Ford · ACS 구독 · SI 23 쪽 + 영상 넷(ASSOCIATED CONTENT 목록과 하나씩 대응 — 빠진 보충 0). ⚠ **흑연 \| Li₆PS₅Cl 복합 음극 · Li 금속 반쪽 — 양극 아님.** 영상(Sup2–5 · mp42 · H.264 1280 × 720 · 29.97 fps · 26.8–27.3 s)은 **컨테이너 머리만** 읽었다(사용자 지시 · 디코더 없음 · 내용 판독 0) — Sup2–5 ↔ Video S1–S4 는 순서 대응 추정 · 확인 불가. PDF 메타데이터: 본문 `%PDF-1.3` · Arbortext Advanced Print Publisher 11.2.5208 · Acrobat Distiller 8.1.0 · iTextSharp.LGPLv2.Core 3.7.4.0 로 다시 씀(startxref 1 · 증분 갱신 0) · 생성 2021-08-05 −04:00 · XMP 3,427 B(VoR · Issue) · 여백 띠 "Downloaded from pubs.acs.org … by HANYANG UNIV user on 28 September 2026"(IP 없음 · 내려받기 표지 쪽 없음) / SI `%PDF-1.3`(카탈로그 1.4) · Word → macOS Quartz PDFContext · 제목 "Microsoft Word - SSB Gr Vis Cell SI revised.docx" · 생성 2021-07-09 Z(수락 17 일 전 수정본) · 같은 형식의 여백 띠.
- ★★★ **(a) 관측**: 자유 단면(펠릿 가장자리를 깎아 낸 면)의 흑연 색을 Keyence VHX-7000 로 · 교정 = 문헌 범주 넷(회색 → 파랑 LiC₁₈ → 빨강 LiC₁₂ → 금색 LiC₆ — refs 47–50) + 46 % Gr 한 셀(실험 조성 넷에 없음 — D13)의 C/32 윗면 사진 다섯 · 색 → `x` 수치 교정 · 불확도 · 광학 분해능 · 촬영 간격 0 · `[도표]` 교정 사진 자리 ≈0 · 0.76 · 1.00 · 1.44 · 1.91 mAh cm⁻² · **금색 기준 사진은 셀 전압 0 V 아래 평탄(≈−8…−13 mV)에서 찍힘**(D14 · 저자 무언급) · 우리 색 분류로 다섯 사진의 금색 분율 0.02 · 0.01 · 0.01 · 0.13 · 0.85 — "금색" 은 `x ≳0.8–1` 의 문턱 표지. 관찰 셀 = 일반 셀과 같은 적층(집전체 \| 복합체 \| 벌크 SE ≈1 mm \| Li) · 같은 7 MPa · 60 °C · 창 없이 옆면 · 내부 대조는 S9 ex situ 한 장(캡션 "C/5.6 for 4 hr" — D4) · SOC 이름표 정의 · 셀 치수 · operando 셀 전기화학 자료 0.
- ★★★ **(b) 24호 "상대극 쪽 전류 쏠림"**: ✅ 방향은 인쇄로 선다 — "current focusing within the composite electrode occurs near the interface with the bulk SE (separator), which is intensified at high rates" · 모든 분율 · 두 율 · 두 적재 · 탈리튬(S6 — 저자 서술 0)도 분리막 쪽 먼저. ⚠ 흑연(σ_e/σ_ion `[도표]` ≈4×10³–7×10⁴)의 명제 · 원인 배정은 40–60 % SE 옴 ↔ 80–100 % 흑연 고체 확산("nearly the entire electrode acts as one large graphite region") — 방향만으로 기구가 안 갈린다. (주) 다섯 칸: ① 순위 · 문턱 0(방향 규칙 refs 52 · 53 + σ 비 + 모형 OAT 가상 실험 둘 κ ×≈11 · `D` ×10) ② 시간 기준 = SOC 사진(정의 미인쇄) ③ 조건 = 40 % Gr · 4 mAh cm⁻² · C/4 · 2D 한 미세구조 ④ 저항 정의 0 ⑤ `i₀` 0 회 — `[재현]` Wagner 형 비 Wa ≈0.008–0.1(x 0.5–0.99): 옴 지배는 입력의 귀결. NMC 로 옮길 것은 방향 규칙 하나 — 크기는 흑연 stage-1 평탄(`[재현]` ≈22 mV / 단위 `x`)이 몇 mV 강하를 Δ`x` ≈0.3 으로 증폭한 것(NMC622 ≈1.2 V / 단위 θ — ×54) · 관찰 채널 없음 · 24호 σ 비 ≈1.2 · 0.28 · 0.004(80 · 70 · 40 %)의 70 ↔ 80 "flip" 은 같은 규칙과 일치.
- ★★★ **(c) `θ` ↔ `η`**: 셀 안 휴지 **0**(`rest` · `relax` 0). 가르는 관측 — 정전압 유지 따라잡기(40 % "At the end of charging, a uniform gold color is observed in the graphite throughout the electrode" · 모형 "fully homogenized at 100% SOC due to the extended CV hold") · 끝 C/16 복귀(`[도표]` 0.967–0.982 · "permanent capacity loss does not occur") · 역방향(S6 끝 금색 분류 0.00) · 다음 사이클(같은 율 두 사이클 차 ≤0.011 mAh cm⁻²) — 넷 다 `η`. ★ `[도표]` **"100 % SOC" 프레임(Fig. 4F = S6A) 집전체 쪽 위 15 % 띠 흑연 분류 픽셀 0.44–0.68 어둠 · 0 → 100 → 0 % 내내 색이 그대로인 ≈14 µm 입자 하나** — "uniform gold" 와 다름(D6) · 정체(고립 흑연 · 미완 `η` · 비흑연) 판정 불가 · 저자 무언급 · 80 · 100 % 의 정전압 끝 상태 그림 0(영상에만). ★★ 확산 시간 창 — 80 % Gr 두께 방향 `[재현]` τ_D(75 µm) ≈20 h(문헌 `D`) – 204 h(모형 `D`) ≫ C/16 16 h(operando 20 h) → 연결된 재고가 유한 프로토콜에서 `θ` 처럼 보인다(1.87 mAh cm⁻² 셀 80 · 100 % 는 C/16 CC-CV 로도 이론의 84 · 76 %). 영역 안 구배(가장자리 금색 · 속 파랑/빨강)는 고체 확산 배정(`phase separ` 0) — 74호 자촉매(입자 간 이봉)와 무늬가 다르다.
- ★★ **(d) 모형**: 2D 해상 연속체(영상 미세구조 287 × 150 µm · 벌크 SE 1000 µm · Li 100 µm · COMSOL 5.6) · SE 옴(κ 0.88 S m⁻¹ "Experiment" — 측정법 미인쇄) · 흑연 Fick `D(x)` = **0.1 × Levi 2003**("grain boundaries" — 근거 문헌 0) · 대칭 BV(α 0.5) · √ 꼴 `i₀(x)` · `i₀,ref` 232 A m⁻²(Chen 2021 액체 · 환산 미인쇄 — D16) · Li `i₀′` 11 A m⁻²(액체 수지상 모형 둘의 "intermediate value") · `c_max` 27,800(출처 0) · 적합 0 — "qualitative insights" · 정량 대조 0. `[재현]` φ_e 색막대 윗끝 셋(−36.6 · −26.3 · −9.35 ↔ −36 · −26 · −9 mV) · 모형 전류 = C-율 × 4.0 mAh cm⁻² · 모형 적재 4.36–4.69(인쇄 "~12% higher") — 내부 정합 ✓. ⚠ 자기 측정과 어긋남: κ_eff 모형 0.14–0.27 ↔ S1 0.029 S m⁻¹(×5–9.5 — D11) · Li 두 계면 50.5 mV ↔ S3 전체 13.4 mV(≥×3.8 — D12) · S17(`D` ×10 = 문헌값)에서 두께 방향 대비도 약해짐(D7 — 일대일 배정과 긴장).
- ★ **(e)** Q1 `θ(N)` 0/76(층 하나 — `θ` 형 후보 관측) · Q2 층 하나(칸 이동 없음 — EDXRD 와 독립이나 범주형 · 표면 · 흑연 한정) · Q4 0/76 · Q6 보고 · 통제(7 MPa · 60 °C · 스윕 0 · SI "higher stack pressures may further improve …" 가설만). **(f)** 24호 방향 규칙 · 크기 옮김 불가 · `θ` 형 후보 자리(집전체 쪽) 공통 · 22호 이온 한계면 집전체 면이 마지막(22호 CC 컷오프 뒤 집전체 면 `η` 가 비활성 분율에 섞일 수 있다는 흑연 유비 — 수치 아님) · 73호 TLM 계열 · S1 ↔ S2 단위 ×10³(D5) · 75호 "kinetics" 는 어느 편에서도 계면 속도상수로 안 흔들림 · [56] "입도 조절" ❌ · 74호 셀 안 휴지 0 공통 · 정전압 유지가 넷째 연산자.
- **채움표 76호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나) · Q2 층 하나 · Q3 층(measured-optical-categorical · measured-EIS/DC · measured-electrochemical · computed-2D) · Q4 0/76 **예순여덟 번째 성질**("두 구배 형태(두께 방향 · 영역 안)를 두 원인(SE 옴 강하 · 흑연 고체 확산)에 일대일 배정하되 — 판정은 40 % Gr · C/4 한 조건의 OAT 가상 실험 둘(κ ×11 · D ×10)뿐이고, 서론이 가를 대상으로 적은 셋째 후보(계면 동역학 `i₀`)는 한 번도 흔들지 않았으며(`[재현]` 인쇄 파라미터의 Wa ≈0.008–0.1 — 옴 지배는 입력의 귀결), D ×10 은 모형 값이 문헌의 1/10 이라 사실상 '문헌값으로 되돌리기' 이고, 그 시험에서 두께 방향 구배도 함께 약해져(S17) 일대일 배정과 긴장한다") · Q5 해당 없음(층 하나 — 상대극 몫 상한 `[재현]` ≲1.4 · 5.7 · 22.8 mV) · Q6 보고 · 통제 · Q7 해당 없음 · Q8 층 하나(흑연 OCV · 평탄 ≈22 mV / 단위 `x`).
- **곱 축퇴 처방 쉰아홉 번째 적용**: 적용 불가(계면 `R` · `C` 측정 0) · 처방 표 새 줄 없음 · 곱 안의 관찰 둘(37호 줄의 해상판 — 영상 경계 × `i₀,ref` 둘 다 고정 · 옴 지배(Wa ≪ 1)면 깊이 분포가 곱 자체에 둔감 = **곱 축퇴의 영역 조건** / 2D 경계는 3D 접촉 면적의 대리 · 접촉 척도는 광학 격자 아래).
- 귀속: 24호 ① :133 "상대극 쪽 전류 쏠림" ✅ 맞다(흑연 명제 · 원인은 조성 의존) ② :611 "EDXRD 와 독립인 깊이 관측 채널" ⚠ 흑연에서만 · 범주형 사진 무늬 · 75호 [56] "입도 · 경로 묶음" ⚠ 경로 ✅ · 입도 ❌ · 원장 §1 행 ✅ 흡수 · 정정 제안(wiki 밖).
- ⚠ 어긋남 18 건(D1 "even at a C/16 … ∼1/6" ↔ 1C 값 · D2 S4B CCCV ↔ CC · D3 S12 표지 뒤바뀜 · D4 S9 C/5.6 · D5 S1 ↔ S2 단위 ×10³ · D6 "uniform gold" ↔ 위 띠 · 무변색 입자 · D7 S17 · "actual value" ↔ 1/10 · D8 퍼콜레이션 전이 60 ↔ 80 % ↔ S1 급락 40 → 60 % · D9 "only slight gradients" · D10 "attenuated" · D11 모형 κ_eff · D12 Li `i₀′` · D13 교정 46 % · D14 금색 기준 0 V 아래 · D15 "40−80%" ↔ "40−100%" · D16 `i₀,ref` 문장 · D17 "as shown in Figure S12" · D18 오탈자).
- 낱말 지문(본문 | SI): `current focusing` 11 | 0 · `kinetic` 3 | 0 · **`sensitiv` 0 | 1**(air-sensitive) · **`identif` 2 | 0**(전부 identify) · `uniqu` · `uncertain` · `±` · `error` · `n =` · `LAM` · `LLI` **0** · `fit` 0 | 3(전부 TLM) · `contact` 2 | 2 · `percolat` 4 | 0 · `tortuos` 2 | 4 · `Bruggeman` 0 · `pressur` 1 | 3 · **`rest` · `relax` 0** · `hold` 2 | 2 · `phase separ` 0 · `exchange current` 0 | 2.
- 그림: 본문과 어긋난 그림 — Fig. 4F/S6A(D6) · S17(D7) · S1(D8) · 5A(D9) · S8(D10) · 2E/S4(D1 · D2) · S12(D3) · S9(D4) · S1 ↔ S2(D5) · 3A(D13 · D14). ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(자동 25 — 수동 3 은 `figures.json` 에만)이 추가됐다.
- ⚠ raw 표기 느슨함 1: digest "보충 자료" 표 SI 행의 "그림 18 중 **17 을 열었다**" 는 초고 잔재다 — 같은 digest §그림의 "연 것 28/28 · 안 연 것 0"(SI 그림 18 장 전부)이 맞다. raw 는 한 번 쓴 불변층이라 고치지 않았다(카드 Status Log 에도 기록).
- 보류 결정 (가)–(추): **(두)** 근거(셀 안 휴지 0 · 정전압 유지 · 끝 C/16 · 역방향 · 다음 사이클 넷 다 `η` · 확산 시간 창의 수치 표본 — 조건 목록에 "정전압 유지(구동력 있음 — 휴지와 구분)" · "τ_D ↔ 창" 두 줄을 붙일 근거) · **(주)** 근거(둘째 표본 — ⑤ 동역학 손잡이가 비면 판정이 아니라 입력) · **(차)** 약(해상 모형에서도 두 노브가 곱으로 모이고 Wa ≪ 1 이면 깊이 분포에 안 찍힘 — forward 에 영역 선결 조건) · **(루)(무)** 약(√ 꼴 기본값 — 흑연판) · **(러)** 정성 메모(무변색 입자는 용량 축에서 `LAM_NE` 서명 · 정체 불명) · **(우)** 참고(24호 ref 39 옮김은 원문과 맞다 — 주석 불필요) · **(더)** 지목 +1(Otoyama 2016 [27] → 2) · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋: 76호 후속 요청(Liu 2019 *ACS AMI* 11, 18386 ★★★ · Otoyama 2020 · Yamagishi 2021 ★★ · Levi 2003 · Chen K. 2021 ★) · (차) forward 설계에 "Wa 영역 선결" 을 붙일지(설계 결정만 — 코드로 옮기면 RUN_SCOPE 가 움직이므로 별도 승인) · 영상(Video S1–S4) 판독을 할지(80 · 100 % 정전압 끝 상태 · `θ` 후보 입자가 남는지는 영상에만).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 76호 행 · 76편 누적 · Evidence 일흔한 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](76호 절 · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](76호 절 · 처방 16 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](쉰아홉 번째 적용 · 주장하지 않는 것) · [[assb-tortuosity-factor-effective-conductivity-split]](열 번째 표본 · 주장하지 않는 것) · [[composite-cathode-percolation-utilization]](76호 절 · 주장하지 않는 것) · `index.md`(3항 분해 개념 줄에 76호 갱신 한 구절 · 페이지 수 53 그대로 · 날짜 2026-09-29). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Davis 2021 행 흡수 표시 · 서술 정정("operando 광학 η(z)" → 흑연 음극 · 범주형 · 표면 · 방향 규칙 / "EDXRD 와 독립" → 흑연 한정 / "입도 · 경로 묶음" → 경로 ✅ · 입도 ❌ / Q2 → Q2 층 하나 · Q4 0/76 · `θ` ↔ `η` 연산자 · 셀 안 휴지 0) · 지목 +1(76) 일곱 — Shi 2020 *AEM* [26](5 → 6) · Kato 2018 *JPCL* [17](2 → 3) · Otoyama 2016 *JPS* [27](1 → 2) · Otoyama 2018 *SSI* [37](1 → 2) · Höltschi 2020 *JES* [34]/SI [4](1 → 2) · Uhlmann 2015 *JPS* [47](1 → 2) · Siroma 2016 *JPS* SI [6](2 → 3) · 원장 행 0 인 Yamamoto M. 2020 *JPS* SI [2] 등록 여부 · 신규 후보 Liu 2019 [52](★★★) · Otoyama 2020 [36] · Yamagishi 2021 [33](★★) · Levi 2003 SI [10] · Chen K. 2021 SI [13] · Kim J.Y. 2020 [35](★) · §3-b (두)(주)(차)(루)(무)(러)(우)(더) 표시 · 큐 문서 `ASSB_TRANSFER_NOTE.md` §6-3-h 38 행 · §6-3-i 38 행 상태)은 손대지 않았다.
- 후속(서지 기준, 미열람): **Liu H., Kazemiabnavi S., Grenier A., Vaughan G., di Michiel M., Polzin B.J., Thornton K., Chapman K.W., Chupas P.J. 2019 *ACS Appl. Mater. Interfaces* 11, 18386**([52] — 방향 규칙 "전자 한계면 집전체 쪽" 의 실측 원전 · operando XRD-CT · 같은 Thornton 연구실) · Otoyama 2020 *J. Phys. Chem. Lett.* 11, 900([36] — ASSB 흑연 operando 공초점) · Yamagishi 2021 *J. Phys. Chem. Lett.* 12, 4623([33] — 흑연 복합 음극 operando ToF-SIMS) · Levi 2003 *J. Solid State Electrochem.* 8, 40(SI [10] — `D_s(x)` 원전 · 1/10 인자 대조) · Chen K. 2021 *Adv. Energy Mater.* 11, 2003336(SI [13] — `i₀,ref` 원전).

## [2026-09-29] ingest | assb 77호 — Shi T., Tu Q., Tian Y., Xiao Y., Miara L.J., Kononova O., Ceder G. 2020, High Active Material Loading in All-Solid-State Battery Electrode via Particle Size Optimization (Adv. Energy Mater. 10, 1902881)
- raw: `raw/papers/shi2020_particle-size-ratio-cathode-utilization-assb.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`) · 그림 `raw/figures/shi2020_particle-size-ratio-cathode-utilization-assb/` (자동 9 — 본문 7 · SI 2 — **표 오탐 2**(SI "Table 1" · 표 S3 을 "거의 백지" 로 버림) · **누락 1**(표 S2 — 캡션이 셀 블록과 합쳐짐) · 캡션 텍스트 깨짐 2(`fig_1` · `fig_4` 수식 조각 — 그림은 온전) · 과대 여럿(내용 온전) · 잘림 0 + 수동 4(SI 표 셋 · §1 Hertz 식); 13 항목 **전부 열어 봤다** — `figures.json` note 13; 본문 그림은 전부 래스터(CMYK · 회색조 JPEG)라 수치는 원본 xref 픽셀 판독 · 지도는 자기 색막대 역변환(판독 폭 digest §판독)). **3차 묶음 파일 39**(열아홉째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★★★ 지목 24 · 25 · 57 · 73 · 75 · 76 · Q1 · 입도비 → 이온 수송" — 3차 묶음에서 지목이 가장 많은 편 · 지목 칸 밖 인용 4호 ref 26 · 19호 [4]. ⚠ 4호 Shi 2020 *JMCA*(기계 열화)와 다른 편. 보충: SI PDF 하나 — "Table S1" 부재는 SI 가 첫 표를 "Table 1" 로 인쇄한 표기 어긋남(D8) · 빠진 보충 0.
- ★★★ **(a) 이용률**: 모형 `θ_CAM = V_CAM^active/V_CAM` — `[인쇄]` "A CAM particle is considered to be 'active' if at least one Li percolation pathway connects it to the bulk SE layer" · "we only consider Li-ion percolation pathways through SE particles" — 부피 가중 · 입자 단위 이진 · 분리막 쪽 SE 경로 · 이온 반쪽(CNF 모형 밖) · 정적(200 MPa) · 간선 판정 미인쇄 · ≥3 배열 평균(산포 0). 실험 "이용률" = 첫 방전 ÷ 155 mAh g⁻¹(`[인쇄]` "largest experimental specific capacity observed" — `[도표]` 그려진 최대 154.1 · D10). `[재현]` 열 조건 차 평균 −5.7 · RMS 8.4 · 최대 15.8 mAh g⁻¹(70 wt%/λ 1.67 모형 0.99 ↔ 0.89 · 80 wt%/λ 3.33 0.72 ↔ 0.62) · 모형 > 실험 8/10 · 닻 근처 넷은 자동 일치. `[재현]` 셀: ∅8 mm · 복합체 ≈5 mg → 9.95 mg cm⁻² · NMC 5.97–7.96 mg cm⁻² · 0.93–1.23 mAh cm⁻² · C/18.5–C/24.7 · 두께 ≈28–43 µm(12 µm NMC 의 2.3–2.9 지름) — "고적재" 는 CAM 분율(≈50 vol%)이지 면적 용량이 아니다.
- ★★★ **정적 θ 밖의 몫**(저자 무언급): `[도표]` 첫 사이클 CE 가 λ 와 함께 0.74 → 0.50 · CV(5 h)가 충전에 더한 몫 저 θ 셀 +19–22 ↔ 고 θ 셀 +10 mAh g⁻¹ · 저 θ 셀 방전 평탄 소실(3.0 V 위 34 % · 2.0 → 1.4 V 에 10–12 %) · 12 µm 쌍은 충전 같고(186.8 ↔ 186.6) 방전 다름(127.8 ↔ 141.1) · **첫 충전 상한 위반 둘**(`θ₀ ≥ Q_ch/Q_ch,ref`: 60 wt%/λ 0.625 0.71 > 0.56 · 80 wt%/λ 1.67 0.64 > 0.48) — 25호 §4-2-3 과 같은 모양이 방법 원전에서도. `η` ↔ 동적 연결(수축) 판정 입력(셀 안 휴지 · 율 · 다음 사이클) 0.
- ★★★ **(b) 22호**: 같은 양 아님(22호 = 첫 C/10 충전의 비탈리튬 분율 · XRD · 합집합 ↔ 이 편 = 이온 연결 계산 + 방전 겉보기) · 방향 반대(CAM 크기 · 무탄소 ↔ CNF 5 wt%) · 저자 화해 "according to our model" 은 전자 연결 계산 0. `[재현]` 교차 대입: 22호 7:3(ψ 0.474 · 이 편 66.5 wt% 상당)에서 22호-S(4.0 µm · 2 %)는 이온 반쪽(Fig. 3c)이 d_SE ≲2.7 µm, 68호 전자 평균장이 ≥4.6 µm 를 요구 — **두 정적 반쪽이 한 점도 함께 못 맞춘다**(계 다름 — 방향만). (허) 값 없음 · 중요도 ↑.
- ★★★ **(c) 귀속**: **24호** "수축 → 입도비 변화 → τ↑" ❌ 인쇄 0(`tortuos` · `shrink` · `volume change` · `evolv` 0 · 사이클 0 · 최단 경로를 뽑고 τ 로 안 씀) — 24호 확장 해석(첫 사이클 비대칭과 양립). **25호** "DEM 이용률의 방법 원전" ✅ 계보 · ⚠ 옮김 셋 다름 — 가중(부피 ↔ "percentage of particles") · 기준(경로 ↔ "in contact with") · 경계(분리막 쪽 ↔ "current collector") · 겹침 손잡이는 25호가 더함. **75호** "∼30 wt %" ✅ 조건부 — 원문 "30–50 wt% typically required [5,6,9,10]" 의 좁힌 재인용(이 편 결과는 완화 쪽). 57 · 73 · 76 · 4호 ✅ · 73호 서지 "2 (2019)" 오기 확인 · 19호 [4] "접촉 면적의 배경" ⚠(면적은 향후 과제) · "큐에 이미 있다" 오기(큐 21 = 22호).
- ★★ **(d) 모형 · 지도**: LIGGGHTS · 구 · 절단 로그정규 여섯(표 S2) · 입방 상자 → 윗판 하강 200 MPa → 정지 · Hertz + 감쇠 + 마찰 항복 · 입자 그래프 최단 경로 · **복셀 없음** · 표 1 문헌 넷(McGrogan 2017 · de Vasconcelos 2016 · PAULING FILE · Zhang · Makse 2005) · 마찰계수 · k · γ_n · 입자 수 · 압착 높이 · 간선 기준 미인쇄 · `L_min ≈10 D_max` 의 D_max 는 실제로 평균 CAM 지름(D5). `[재현]` λ ↔ Sauter 비 0.96–1.06 배 · Fig. 1b 는 부피 가중 표시(개수 평균 5 µm 의 봉우리 ≈6 µm) · Fig. 7a 는 표 1 밀도 + CNF ≈1.52 g cm⁻³(맞춤)로 RMS 0.15 vol% · **Fig. 7b("vol%")는 3c 의 1.7–2.4 단위 이동판 · 윗눈금 "80"(= 90)** — 환산 아님(D3). 68호 식 SE 거울판(우리 확장): 비만 ✓(S2 ≤0.04) · 70 wt% 전이 폭 ×5 ✓ · 80 wt% 이상 과대 연결 ❌.
- ★ **(e)** Q1 `θ(N)` 0/77(층 하나 — 신품 정적 `θ₀` 계산판) · Q2 없다(SEM 분말 · SE 펠릿 σ 뿐) · Q4 0/77 · Q6 보고 · 통제(제조 100 · 200 · 200 MPa · 운전 스프링 ≈5 MPa · DEM 200 MPa 한 점 — 운전 압력 이완 0). 온도 미인쇄 · 셀 안 휴지 0 · 율 하나 · 조건당 셀 1 · 오차 0 · 60 · 80 wt% 네 셀은 Fig. 5 와 Fig. 6 에 두 번 그려짐(서로 다른 조건 10).
- **채움표 77호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나) · Q2 없다 · Q3 층(computed-geometric · measured-electrochemical · 닻 곱 · 미인쇄 입력) · Q4 0/77 **예순아홉 번째 성질**("정적 연결 모형(DEM + 입자 그래프)의 θ 를 실험 첫 방전과 대조해 '이온 퍼콜레이션이 한계' 라 하되 — 대조의 척도(155 mAh g⁻¹)는 실험 최대값을 가져온 닻이고, 관측은 CC 방전 하나(충전 · CE 0 회 · 조건당 셀 1 · 오차 0)이며, 휴지 · 율 · 다음 사이클이 없어 정적 θ 와 η 가 안 갈리고, 자기 첫 충전(5 h CV) 비가 두 저 λ 셀에서 모형 θ 를 넘는다") · Q5 없다(층 하나 — 창 "2–3.7 V versus In" ↔ 그림 1.40–3.70 V) · Q6 보고 · 통제 · Q7 해당 없음 · Q8 층 하나(첫 사이클 V–Q).
- **곱 축퇴 처방 예순 번째 적용**: 적용 불가(계면 `R` · `C` 측정 0) · 처방 표 새 줄 없음 · 곱 안의 관찰 둘(이진 연결 = 면적 노브의 0 차 극한 — 부분 접촉 손실은 0 으로 보인다 / 용량 대조 `θ × 155` 의 닻이 최선 셀의 `η·Q_material` 을 품는다).
- ⚠ raw 표기 느슨함 2: ① digest 머리 지목 표의 19호 행 "Yoshida 2024 *Electrochemistry*" 는 오기 — 19호는 *Electrochimica Acta* 497, 144523. ② §(b) 조건 표 22호 CAM 칸의 "(레이저 체적 중앙)" 은 22호 digest 에 없는 우리 추정(같은 절 "d₅₀(체적 중앙)을 개수 평균으로 옮기면" 도 그 가정 위) — `[해석]` 으로 읽는다. raw 는 한 번 쓴 불변층이라 고치지 않았다(카드 Status Log 에도 기록).
- ⚠ 어긋남 18 건(D1 3b 표지 7 ↔ 여섯 · D2 S2 60 ↔ 70 wt% · D3 7b 이동판 · 윗눈금 · D4 S1b 축 이름 · D5 L_min 의 D_max · D6 창 2 ↔ 1.40 V · D7 SI 식 δ 부호 · 접선항 · γ_t 단위 · D8 "Table 1" · D9 분쇄 조건 · D10 닻 155 · D11 "×2–3 으로 20 → 100 %" · D12 "80 wt% 초과 가능" 외삽 · D13 "over 50 vol%" · D14 50 ↔ 45 vol% · D15 색 영역 · D16 Fig. 6 축 이름 · 재사용 표시 0 · D17 "both electronic and ionic" 계산 0 · D18 S1a 축 이름표).
- 낱말 지문(본문 | SI): `utiliz` 33 | 1 · `percolat` 35 | 0 · **`tortuos` · `shrink` · `volume change` · `evolv` 0** · **`rest` · `relax` · `rate`(낱말) · `Coulombic` · `efficiency` 0** · 충전 용량 0(방전 용량 9) · `contact` 7 | 4 · **`identif` · `sensitiv` · `uncertain` · `uniqu` · `fit` 0** · `±` 0 · `temperature` · `°C` · `thickness` 0 · `LAM` · `LLI` 0.
- PDF 메타데이터: 본문 `%PDF-1.6` · InDesign CS6 (Macintosh) · Adobe PDF Library 10.0.1 · iText 4.2.0 by 1T3XT 로 다시 씀(startxref 1) · 생성 2019-12-10 +05'30' · XMP VoR · 여백 띠(2–9 쪽) "Downloaded … by Hanyang University Library … on [27/09/2026]"(IP 없음) / SI `%PDF-1.5` · pdftk 2.02 · itext-paulo-155 · 생성 = 수정 2019-12-03 +05'30' · XMP 0 · 여백 띠 0. ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(자동 9 — 수동 4 는 `figures.json` 에만)이 추가됐다.
- 보류 결정 (가)–(푸): **(러)** 근거(부피 분율 정의 → `ε_p` 자리 · 경고 쪽: 방전 하나 · 닻 · 상한 위반 둘) · **(저)** 근거(넷째 표본 — 방법 원전에 대한 부정 시험) · **(두)** 근거(휴지 0 · 율 하나 · 다음 사이클 0 · CV(충전만) ↔ CC 방전 비대칭) · **(주)** 근거(셋째 표본 — ①④⑤ 빔) · **(허)** 근거 0 + 중요도 메모 · **(수)(퍼)** 약 · **(차)(처)** 정성 메모 · **(고)** 기록(복셀 없음 · 절대 크기 무관 — DEM 은 다른 브랜치 소유) · **(머)** 지목 +1(Hakari 2017 [33] → 2) · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷(Fig. 7b 대신 3c + ψ 표기 · 합성 truth `θ₀` 세 출처 폭 · 25호 인용 자리 주석 · 77호 후속 요청).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 77호 행 · 77편 누적 · Evidence 일흔두 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[composite-cathode-percolation-utilization]](77호 절 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](77호 절 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](예순 번째 적용 · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](77호 절 · 처방 17 · 주장하지 않는 것) · [[assb-tortuosity-factor-effective-conductivity-split]](열한 번째 표본 · 주장하지 않는 것) · `index.md`(퍼콜레이션 개념 줄에 77호 갱신 한 구절 · 페이지 수 53 그대로 · 날짜 2026-09-29). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Shi 2020 *AEM* 행 흡수 표시 · 서술 정정 · 지목 칸 누락 4 · 19호 · 지목 +1(77) 넷(Ito 2014 [6] · Kato 2018 [9] · Hakari 2017 [33] · Zhang W. 2017 [34]) · §3-b 표시)는 호출자 몫.
- 후속(서지 기준, 미열람): **McGrogan F.P., Swamy T., Bishop S.R., Eggleton E., Porz L., Chen X., Chiang Y.-M., Van Vliet K.J. 2017 *Adv. Energy Mater.* 7, 1602011**(SI [1] — LPS E · σ_y — DEM 입력 원전 · 25호 G5) · **Choi S., Jeon M., Ahn J., Jung W.D., Choi S.M., Kim J., Lim J., Jang Y., Jung H., Lee J. 2018 *ACS Appl. Mater. Interfaces* 10, 23740**([29] — 공극 0.1–0.2 · LPS 소성 변형) · de Vasconcelos L.S., Xu R., Li J., Zhao K. 2016 *Extreme Mech. Lett.* 9, 495(SI [2] — NMC 물성) · Lagadec M.F., Zahn R., Müller S., Wood V. 2018 *Energy Environ. Sci.* 11, 3194([25] — SE 경로 가정 · 위상 분석).

## [2026-09-29] ingest | assb 78호 — Buchberger I., Seidlmayer S., Pokharel A., Piana M., Hattendorff J., Kudejova P., Gilles R., Gasteiger H.A. 2015, Aging Analysis of Graphite/LiNi1/3Mn1/3Co1/3O2 Cells Using XRD, PGAA, and AC Impedance (J. Electrochem. Soc. 162, A2737–A2746)
- raw: `raw/papers/buchberger2015_graphite-nmc111-aging-xrd-ca-li-loss-pgaa-impedance.md` (sha256 봉인 — `pdf_sha256` · 보충 0) · 그림 `raw/figures/buchberger2015_graphite-nmc111-aging-xrd-ca-li-loss-pgaa-impedance/` (자동 11 — 본문 그림 전부 · 라벨 어긋남 0 · 잘림 0 · 여백 과대(내용 온전) · **누락 3**(표 I · II · III — 텍스트 표) + 수동 3(표 I–III · 300 dpi); 14 항목 **전부 열어 봤다** — `figures.json` note 14; 그림은 전부 래스터(CMYK JPEG 10 · 회색조 1)라 수치는 원본 xref 픽셀 판독(판독 폭 digest §판독)). **3차 묶음 파일 40**(스무째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★ Buchberger·…·Gasteiger 2015 · 지목 24 · Q3·Q8 · c/a → x 교정식 (x < 0.5) — Li 함량이 1 을 넘는 교정 오프셋 점검용" · 24호 ref 26 · SI ref 4 · 지목 밖 사용 66호 `[재현]`(인용 0). TUM 기술전기화학 강좌(Gasteiger) + MLZ(FRM II) — 47호(Solchenbach 2016)와 같은 강좌. **액체 흑연/NMC111 풀셀 — ASSB 아님.** 보충: 없음(본문 · 캡션 · 참고문헌 언급 0 — 받을 때 대조와 같다) · 해시 호출자 명시값과 일치.
- ★★★ **(a) 교정식의 원전**: `[인쇄]`(Fig. 4 캡션) "The linear regression fit between x = 0 and 0.5 gives c/a = 0.3552∗x + 4.9722 with R2 = 0.9952"(그림 이름표는 "R=0.9952" — D4) · 본문 "A Vegard's law type linear fit is only possible in the range x = 0–0.5" — 24호 `x = (c/a − 4.9722)/0.3552, 0 < x < 0.5` 는 역함수로 **같다** ✅ · x = Li₁₋ₓNMC 의 탈리튬 분율(c/a 는 x 와 함께 증가) · 온도 "room temperature"(값 미인쇄). 교정 셀 = **Li/NMC111 in situ 반쪽 하나**(Al 창 · LP57 160 µl · 18.4 ± 1.1 mg cm⁻² · 비단색 Mo Kα 반사 · 0.1C · 3.0–4.3 V · 첫 두 사이클 · XRD 는 간헐 OCV 휴지) — **흑연 셀 아님** · x = 통과 전하 계수(`[인쇄]` "from Li1.00NMC" · x = 1 ↔ 278 mAh g⁻¹) · 적합 점 집합 · 점 수 · 휴지 길이 · esd · ICP 미인쇄. `[재현]` 그려진 파란 선 = 인쇄식(픽셀 적합 0.3549x + 4.9725) · 판독 31 점(네 가지 · x ≤0.5) 풀링 OLS **0.368x + 4.965(R² 0.984 · 인쇄선 대비 평균 잔차 −0.0036)** · 첫 충전만 0.358x + 4.9724(R² 0.991)가 인쇄에 가장 가깝다(D5) · 둘째 충전 가지는 인쇄선에서 c/a −0.004 … −0.017(x 로 −0.01 … −0.05) · 같은 c/a 의 첫 충전보다 x **+0.025…+0.040**(69호 NMC111 사이클 번호 항과 크기 같음 · 고 SOC 로 줄지 않는 점은 다름).
- ★★★ **24호 Li > 1.0 의 출처 — 교정식 절편이 아니다**: x < 0 은 c/a < 4.9722 일 때뿐인데 `[재현]` 원전 자기 원형 c/a 다섯(in situ 4.9731 · 4.9752 · 4.9765 · ex situ 4.9734 · 4.9811)이 모두 절편보다 높아 Li 0.975–0.998 · 66 · 69 · 72 · 74호 NMC111 원형도 0.987–0.995 · 24호 1.02–1.05 는 c/a 4.954–4.965 — 액체 다섯 연구실 원형(4.973–4.981)보다 **0.008–0.027 낮다** ⇒ 오프셋은 24호 측정 · 시편 쪽(EDXRD 세 봉우리 · 로트 · 가압 복합체 응력 · 조성 — 어느 것인지 24호 지면으로 못 가른다). 24호 digest 의 크기 "≥0.02–0.05" 는 서고 출처 이름이 옮겨진다.
- ★★★ **(b) 다른 교정과의 관계**: 규약 = **69호형(신품 첫 점 1.00 · 첫 사이클 결손 이월)의 인쇄판** — 새 규약으로 세지 않음 · 66호 `[재현]`(24호 전사 식 → NCM111 −0.028 … +0.007)은 식이 원전과 같아 그대로 선다 · 74호 판 입자 원형 격자를 이 식에 대면 Li 0.989 ↔ 74호 자기 첫 스캔 1.012–1.022(원형 끝 차 ≈0.02–0.03) · `c` 최대 x ≈0.59(= 72호) · `[도표]` in situ ΔV/V(4.3 V · CV 없음) −0.45 … −0.63 % ↔ 69호 −1.16 %(×1.8–2.6). **결손 배정이 66호와 반대** — `[인쇄]` ICL(0.084 · 23.4 mAh g⁻¹)은 방전 끝 느린 확산 · 3.0 → 2.0 → 1.6 V 정전압 유지(30 h)로 격자가 원형으로 돌아온다(`[도표]` ≈98 %) · 유지 중 통과 전하는 결손의 ≥129 %(전하 계정 과대). 이 편이 더하는 것 = **읽기 쪽 기준** — 노화 x 에서 뺄 영점(0.1 C ICL 0.084 · 1 C 보정 0.109)을 전하로 둔다 · 같은 교정으로 그 기준 상태를 읽으면 0.051–0.083. ASSB 옮김 조건: 조성(NMC111 전용) · 기하(반사 Kα1+2 → 투과 Kα1 → EDXRD — 원형 대조 인쇄 0 · 이 편 안 이송만으로 원형 x +0.017(캡션) · −0.005(본문) — D1) · 응력(가압 · 이방 압축률 — 위키에 물성 0) · 온도(실온 한 점) · 사이클 가지(첫 충전 쪽 선).
- ★★★ **(c) 노화 분해 — 본 프로젝트 축**: LLI 는 격자로 **적합 없이** 따로 읽었고(측정 + 교정 + 가정 기준) · LAM 은 재지 않았고(TM 용출 몫만 — PGAA 0.08 · 0.26 · 0.77 mol%) · 저항은 뺄셈 + 정성. `[인쇄]` 표 I ΔC_active-Li/ΔC_cycling: 4.2 V/25 °C 3.6/7.4 · 3.3/6.9(**48–49 %**) · 4.2 V/60 °C 57.3/62.0 · 60.9/64.5(**92–94 %**) · 4.6 V/25 °C 53.9/119.9 · 58.9/127.5(**45–46 %**) mAh g⁻¹ — `[재현]` ±0.1 · 본문 "4.2 V 는 주로 LLI" 는 60 °C 에서만(D17). 표 III XRD 열 = 표 I **+ 7.0**(영점 0.084 — 전환 인쇄 0, D6) · 1 C 보정 0.109 를 Fig. 11a 로 읽으면 0.106–0.129(D7). `[재현]` 같은 셀(4.2 V/25 ① · 용량 손실 7.4)의 LLI 가 정의에 따라 **A 3.6 · A' +4.6 … −1.9 · B 10.6 · C ≈15** — 규약 폭이 경미 셀 신호보다 크다 · 형성 결손 "큰 쪽" 규칙(Fig. 7: ICL 0.27 > SEI 0.22 mAh · 풀셀 0.28)이 흑연에 ≈4–5 mAh g⁻¹ 저장소를 남긴다(`[해석]`) · **4.6 V 격자 LLI 는 상한**(방전 끝 분극 한계 — `[해석]`) · XRD ↔ 반쪽(방 − 충) 4.2 V 넷 −3.8 … +3.4 mAh g⁻¹(같은 양의 두 읽기 — 기준 공유) · PGAA 2 e⁻/TM = 0.50 · 1.59 · 4.87 mAh g⁻¹ = B 의 2.3–8 % · 순위 반만 맞음 · `[도표]` EIS 초기 ≈27 · 4.2 V/60 ≈28 · 4.2 V/25 ≈44 · 4.6 V ≥235 Ω·cm²(2전극 · 적합 0).
- ★★ **(d)(e)(f)**: Q1 해당 없음(`θ(N)` 0/78 · 층 하나 — LAM 을 용출 몫으로만) · Q2 없다(층 하나 — LLI 채널 둘의 교차) · Q3 층 넷 · Q4 0/78 · Q8 층 하나(NMC111 구조 SOC 눈금의 원전 · OCV 표 0). 곱 축퇴 — `[인쇄]` "indicating either a substantial loss of active material or substantially increased impedance" → 용출 LAM 만 지워 "charge transfer resistance and/or surface film resistance" 로 닫음. 셀: 흑연(SGL · 95:5 · Cu 10 µm · ∅11 mm · 7.4 ± 0.2 · 9.3 ± 0.2 mg cm⁻²) \| LP57 80 µl · 유리섬유 둘 \| NMC111(96:2:2 · Al 18 µm · ∅10 mm · 15.0 ± 0.2 mg cm⁻² · ≈90 µm) · Swagelok T · 면적 용량비 1.2 · 형성 C/10 두 번(3.0–4.2 V · 25 °C) · 1C/1C CCCV(C/20) · 조건당 두 셀 · ≤300 사이클(4.6 V 232 · 228) · 스프링 압력 미인쇄 · `[재현]` NMC 11.78 mg · 2.25 mAh cm⁻² · 전극 전체 용량비 ≈1.45.
- **채움표 78호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(층 하나) · Q2 없다(층 하나 — LLI 채널 둘) · Q3 층 넷(measured-crystallographic → fitted 교정 → 가정 기준 · measured-electrochemical · measured-elemental · measured-impedance 2전극) · Q4 0/78 **일흔 번째 성질**("순환 Li 손실을 방전 끝 양극 격자로 적합 없이 읽어 용량 손실과 대조하되 — 뺄 기준 상태(0.1 C ICL 0.084 ↔ 1 C 보정 0.109 · 형성 뒤 흑연 저장소)를 전하 규약으로 두고 그 폭(7.0 mAh g⁻¹)이 경미 셀의 신호(3.3–3.6)보다 크며, LAM ↔ 임피던스를 'either … or' 로 인쇄한 뒤 한 기구(TM 용출)만 지워 닫는다") · Q5 해당 없음(층 하나 — 반쪽 율 2전극) · Q6 없다 · Q7 해당 없음(층 하나 — 형성 결손 "큰 쪽" 규칙) · Q8 층 하나.
- **곱 축퇴 처방 예순한 번째 적용**: 적용 불가(`R` · `C` 적합 0 · 2전극 원형만) · 처방 표 새 줄 없음 · 곱 안의 관찰 둘(액체 반쪽 "either … or" = 유한 율 용량 하나로는 활성 물질 양 ↔ 계면 저항이 안 갈림 / 저자 후보 "surface structural changes" = 활성 면적과 막 · 전하이동 저항을 함께 움직이는 한 사건 — 72호 정성 메모와 같은 모양).
- ⚠ raw 표기 느슨함 1(**24호** digest): :145 식 (5) 옆 "(Buchberger 2015 — 액체셀 NMC111/흑연)" — 교정 셀은 Li/NMC111 반쪽 in situ 이고 흑연/NMC111 은 같은 편의 노화 셀이다. 24호 raw 는 불변이라 고치지 않았다(개념 정의표 · 표본 표 24호 행은 정정 · 카드 Status Log 에 기록).
- ⚠ 어긋남 24 건(D1 Fig. 2 캡션 ↔ 본문 격자 · D2 캡션 격자 x ↔ 표 I · D3 ICL 넷(0.086 · 0.084 · 0.085 · ≈0.082–0.083) · D4 R ↔ R² · D5 적합 점 집합 · D6 표 III 영점 · D7 1 C 보정 근거 · D8 Fig. 11 구획 · 율 목록 · 방향 · D9 Fig. 1 캡션 · D10 4.6 V 회복 가지 · D11 Fig. 5 · D12 Fig. 6 "∼50%" ↔ ≈63–64 % · D13 8° 봉우리 · D14 결론 "full cells" · D15 "Mn2/3" · D16 초록 인과 · D17 "주로 LLI" · D18 표 II 분모 · D19 오기 · D20 색 · D21 참고문헌 형식 · D22 PageLabels · D23 OCV 3 h · D24 "almost perfectly").
- 낱말 지문(본문): `identif` · `sensitiv` · `uncertain` · `uniqu` **0** · `LAM` · `LLI` · `degradation mode` · DVA/ICA **0** · "loss of active lithium" 25 · "active lithium" 43 · `fit` 6(전부 XRD 정련 · 교정 회귀) · `equivalent circuit` 0 · `pressure` · `isolat` · `Coulombic` · `rest` · `relax` **0** · `half-cell` 35 · `PGAA` 13 · `c/a` 15 · `impedance` 30.
- PDF 메타데이터: `%PDF-1.4` · creator "LaTeX with hyperref package" · producer "Acrobat Distiller 10.1.10 (Windows); modified using iText 5.5.13.5 (IOP Publishing Ltd; licensed version)" · 생성 2015-10-20 +05'30' · 수정 2026-09-28 07:01 +01'00'(= 내려받기) · XMP 3,384 B(doi · VoR · 라이선스 필드 0) · startxref 1 · PageLabels 표지부터 2737(D22) · IOP 표지 1 쪽(내려받기 IP 옮기지 않음) · 본문 여백 띠 0. ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(자동 11 — 수동 3 은 `figures.json` 에만)이 추가됐다.
- 보류 결정 (가)–(드): **(터)** 근거 도착(원전 확인 · 원형 끝 늘 Li < 1 · 적합 점 집합 비재현 · 가지 · 사이클 항 · 읽기 쪽 영점 · `c` 최대 Li ≈0.41) · **(도)** 근거(NMC111 첫 사이클 결손 = 동역학 · 정전압으로 격자 복귀 — 요청 판단 재료) · **(노)** 약한 근거(격자 층위 연구실 간 ×1.8–2.6) · **(러)** 약한 근거(경고 쪽 — 용량 채널 하나로 LAM ↔ 저항 못 가름) · **(두)** 약한 근거(정전압 유지 연산자 둘째 표본) · **(주)** 약 · **(처)(차)** 정성 메모 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷(24호 교정 인용 자리 주석 · 교정 개념 "읽기 쪽 영점" 줄 · 실측 LLI 정의 표기 규약 A/B/C — 설계 결정만 · 78호 후속 요청).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 78호 행 · 78편 누적 · Evidence 일흔세 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[nmc-lattice-li-content-calibration]](78호 절 · 표본 표 78호 행 · 24호 행 · 정의표 정정 · 주장하지 않는 것 셋) · [[reference-electrode-halfcell-dma]](구조 채널판 절) · [[assb-apparent-capacity-decomposition]](78호 절 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](예순한 번째 적용 · 주장하지 않는 것) · `index.md`(교정 · RE DMA 개념 줄에 78호 한 구절 · 페이지 수 53 그대로 · 날짜 2026-09-29). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Buchberger 행 흡수 표시 · 서술 정정("Li 함량이 1 을 넘는 교정 오프셋" → 교정식이 아니라 측정 · 시편 쪽) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h 40 행 · §6-3-i 40 행 상태)는 호출자 몫.
- 후속(서지 기준, 미열람): **Dubarry M., Truchot C., Liaw B.Y., Gering K., Sazhin S., Jamison D., Michelbacher C. 2011 *J. Power Sources* 196, 10336**([19] — "gradual = LLI · rapid rollover = 임피던스" 두 감쇠 모양의 원전 · 위키 Dubarry 2012 와 다른 편) · **Yabuuchi N., Makimura Y., Ohzuku T. 2007 *J. Electrochem. Soc.* 154, A314**([7] — c/a 교정 방법 원전) · Kang S.-H. … 2008 *Electrochim. Acta* 54, 684 [38] · Kang S.-H. … 2008 *J. Mater. Sci.* 43, 4701 [39](ICL 동역학 · Li₂MO₂ 회복) · 화학 앵커 격자–Li 교정 Choi J., Manthiram A. 2005 *J. Electrochem. Soc.* 152, A1714 [6] · Li D.-C. … 2004 *J. Power Sources* 132, 150 [28] · Yin S.-C. … 2006 *Chem. Mater.* 18, 1901 [29] · Rodriguez A.M. … 2002 *Adv. X-Ray Anal.* 45, 182 [30] · Burns J.C. … 2013 *J. Electrochem. Soc.* 160, A1451 [20] · German F. … 2014 *J. Power Sources* 264, 100 [40].

## [2026-09-29] ingest | assb 79호 — Li Z., Yin L., Mattei G.S., Cosby M.R., Lee B.-S., Wu Z., Bak S.-M., Chapman K.W., Yang X.-Q., Liu P., Khalifah P.G. 2020, Synchrotron Operando Depth Profiling Studies of State-of-Charge Gradients in Thick Li(Ni0.8Mn0.1Co0.1)O2 Cathode Films (Chem. Mater. 32, 6358–6364)
- raw: `raw/papers/li2020_synchrotron-operando-depth-profiling-soc-gradients-thick-nmc811.md` (sha256 봉인 — `pdf_sha256` · `si_sha256` · TOPAS TXT 둘의 sha256 은 `source_url_note`) · 그림 `raw/figures/li2020_synchrotron-operando-depth-profiling-soc-gradients-thick-nmc811/` (자동 14 — 본문 그림 4 · SI 그림 8 · 표 2 · 라벨 어긋남 0 · 잘림 0 · ⚠ 표 1 자동은 5 쪽 전체(과대 영역 — 내용 온전) · **누락 1**(표 S1 — "영역 없음") + 수동 3(표 1 · 표 S1 · 초록 그래픽 — 300 dpi); 17 항목 **전부 열어 봤다** — `figures.json` note 17; Fig. 1 · 2 · S5 는 벡터라 PDF 경로 좌표로, Fig. 3 · 4 · S6 은 원본 래스터 픽셀로 읽었고 S8 교정 곡선은 Fig. 1 + 표 S1 로 재구성). **3차 묶음 파일 41**(스물한째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★ Li Z.·Yin·…·Liu P. 2020 · 지목 24 · Q2 · 액체셀 두꺼운 전극 깊이 프로파일 · 전류 역전 · 가중평균 관행의 선례" · 24호 ref 34 · SI ref 14(지목 밖 인용 0 — `Li Z.` · `Khalifah` · `6358` · `Depth Profiling` · `chemmater.0c00983` grep). Stony Brook · BNL(Khalifah · Yang · Bak) · UCSD(Liu P.) · APS(Chapman). **액체 Li/NMC811 — ASSB 아님.** 보충: SI PDF + TOPAS 입력 TXT 둘 — 본문 보충 목록과 대조해 빠진 파일 0 · 해시 넷 호출자 명시값과 일치.
- ★★★ **(a) 24호 세 명제**: ① **깊이 프로파일 ✅** — `[인쇄]` 170 µm(본문) / 172 µm(SI) · 90 : 5 : 5 · 공극 20 % · 3.27 g cm⁻³ · 50–60 mg cm⁻² · Li 250 µm · GF/B 0.68 mm · λ 0.2113 Å · 빔 20 × 250 µm · 41 높이 × 20 µm · 6 분마다 · `[재현]` 활물질 8.97 mg · ∅4.75 mm 로 50.6 mg cm⁻² · 10.1 mAh cm⁻² · 면적 전류 1.01 mA cm⁻² 는 ∅4.754 mm 와만 맞는다(본문 5 mm — D2) · **깊이 분해능은 기하가 정한다** — 기울기(SI C/10 2.9° · C/3 2.4°) × ∅4.75 mm 로 끝 주사는 표면에서 [0, t/2 + R tanα − |z|] 중첩 평균(C/10 앞 넷 0–17 · 37 · 57 · 77 µm) · |z| ≤34 · 13.5 µm 는 전 깊이 · 이 식이 S6 모의 사다리꼴(±206 · ±34 / ±185 · ±12)을 재현 · 양 끝 주사는 원판의 반대 가장자리. ② **전류 역전 ✅(인쇄)** — "the back of the cathode continues to increase its state of charge to up to two additional hours" · `[도표]` −191 0.52 → 0.72(13.9 h) · −171 0.64 → 0.84 — 단상 · 경계 층에서 격자 두 채널 일치 · ⚠ −131 · −151 은 Fig. 3 에만(Fig. 2c 가중 부피는 즉시 리튬화 쪽 — D16) · 기구 = 전해액 농도 · 1 M 부근 이동도 봉우리(정성 · ref 30). ③ **가중평균 ⚠ 형식만** — `[인쇄]` "reported parameters are the weighted average of those of the two NMC phases" 이지만 두 상은 Rietveld 로 먼저 분리(Sup3 `scale_2 = scale_1 * ratio`)하고 **첫 충전 끝 패턴의 비로 고정** · 두 상 = 기울기가 섞은 앞 · 뒤 필름(`θ` 모집단 아님) · 분율 미보고 → 모집단 분율 자리 없음 · 22호(분리 · 분율 보고) ↔ 24호(높이 가중) 사이의 중간 처리 · 이봉의 기하 기원을 인쇄한 선례 — 24호 조각 6 의 `θ` 형 해석 전에 기울기 · 깊이 혼합 배제가 필요.
- ★★★ **(b) 교정**: x 가 아닌 **자기 교정 ASOC** — `[인쇄]` "Instead of calculating the true SOC … accessible state of charge (ASOC)" · 같은 셀 맨 앞 층의 첫 방전 부피 ↔ 셀 방전 전하 보간(S8) · 0 = 첫 방전 2.8 V 유지 끝 · 1 = 첫 충전 4.4 V 유지 끝 · 원형 0.12 · 78호 식 · 다른 연구실 교정 인용 0. `[재현]` Fig. 1 벡터 + 표 S1 → S8 재구성 · 원형 **0.126** · **ΔV 의 64 % 가 방전 첫 10.7 %**(본문 "linear change in the unit cell volume" 과 다름 — D10) · 원형 0.12 의 인쇄 설명은 방향이 뒤집혔다(D9 — 원형보다 큰 것은 첫 방전 끝 부피 +0.27 Å³) · 가파른 부분 −73 Å³ per δ ↔ 66호 NCM811 최대 −24 … −30(×2.4–3.0) · 4.04 V 위 ΔV 68 % 에 셀 전하 25.4 mAh g⁻¹ ↔ 69호 ≈47(×≈1.9) — 기준 층(앞)이 셀 평균보다 앞서 방전한 몫이 교정에 들어갔다는 쪽(`[해석]`) · 두 상 조각은 평균 순서로 0.20 차 · NMC811 은 `V` 만 단조(c 최대 ≈4.04 V · a 비단조) ↔ NMC111(78호) 선형 c/a · 원형 V 101.57 Å³(66호 101.12 · 69호 101.27) · C/3 +26 척도 1 ASOC ≈246 mAh g⁻¹(정의 189.7 — 재척도 ≈0.77 · 계수 미인쇄).
- ★★★ **(c) θ ↔ η**: 뒤(집전체 쪽)가 늦다 → `[인쇄]` 이온 한계("electronic limitations would result in the lowest local capacity instead being seen at the front") — 76호 방향 규칙의 액체 · 양극 인쇄 · 판정 기준은 방향 하나(전도도 · 순위 · 문턱 0) · `[재현]` 공극 Li⁺ 재고 ≈0.092 mAh cm⁻² = C/10 5.5 분 몫. 저자 이름표 "no longer electrochemically active" 가 역방향 계속 반응(≤2 h · 충전 중 어느 때보다 빠름) · 2.8 V 유지 중 뒤층 방전 최고 속도(−0.09 … −0.15 h⁻¹ — 결론 "fastest … after the end of a discharge cycle", 결과 절 서술 0 — D15) · C/3 드리프트(−154 +0.46 / 16 h · 포화 없음 · 주기 최대 깊이 지연 0–0.5 h)로 뒤집힌다 — `θ` 형 층 0. **계획된 셀 안 휴지 0** — `[도표]` Fig. 4c 7.28–7.59 h 에 표 S2 · 본문에 없는 ≈0.3 h 무전류 구간(전압 2.8 → ≈3.7 V 직선) 하나, 그동안 ASOC 전 높이 ±0.006 · 그때 구배 ≈0.05 라 이완 판정 불가. 두 상 = 기하 혼합(H2/H3 두 상 공존 가능성 무언급) · 2.8 V 유지 끝 앞 ≤0.05 ↔ 뒤 0.18–0.22 ↔ 원형 0.12(첫 사이클 결손의 깊이 몫 — 가르지 않음). CE: C/3 과잉 충전 103.4 mAh g⁻¹ / 9 사이클 ↔ 셀 평균 드리프트가 한 척도로 맞는다(드리프트 ↔ 진폭 비) — CE 결손 ≠ LLI 후보.
- ★★ **(d) TOPAS 두 파일(읽기만)**: Sup3 = 두 상(NMC1 · NMC2) 정련 출력 · **Sup2 = Sup3 에서 둘째 상을 지운 틀** — 머리 통계(r_wp 9.25219155 · gof 4.16113294 · DW 0.0642) 바이트 동일 · 단상 파일 NMC 무게 46.010 %(= 두 상의 NMC1 · 단상이면 100) ⇒ 단상 ↔ 두 상 비교 불가. `[재현]` gof = r_wp / r_exp ✓ · V · 단위포 질량 · 무게 분율(ratio 1.16576 × M₂V₂/M₁V₁ → 46.01 : 53.99) ✓ · occLi 0.999 ± 0.100 · 0.963 ± 0.093(충전 격자에서 ≈1 — 정보 없음) · B 고정 · 반자리 0(실험 절과 다름 — D19) · z(O) 0.2422 ↔ 0.2346 · 거리 · 파장 · 영점 정련 0(높이별 재척도는 TOPAS 밖) · Fe = fcc 3.587 Å(Pawley) · Al 주석 처리(잔재 4.068) · PTFE 2.469°(d 4.904 Å) · 머리 r_wp ↔ `R_wp = Get(r_wp);:8.78771`(D18). 두 상 V 비 0.991(≈0.3 ASOC 차) · 평균 순서는 Sup3 예에서 0.02 · 한 상이 가파른 부분이면 0.2.
- ★★ **(e)(f)**: Q1 해당 없음(`θ(N)` 0/79 · 층 하나 — "불활성" → `η`) · Q2 없다(층 하나 — 격자 독립 · 눈금 전하 · 재척도 뒤 일치) · Q3 층(격자 → 두 상 고정 비 → 자기 교정 ASOC · 전기화학 · ESOC 재척도) · Q4 0/79 · Q8 층 하나(NMC811 자기 교정 눈금). 잇기: 24호(세 명제 · 조각 6 해석 조건 · 방전 끝 구배 <0.02 ↔ 이 편 ≈0.2) · 22호(같은 정련 도구 · 반대 처리) · 76호(방향 규칙 둘째 인쇄 · 연산자 둘 추가 · 휴지 여전히 0) · 78호(78호 식 미사용 · 0 점 = 첫 방전 끝 · 결손 깊이 몫이 확산 지연과 같은 방향) · 66 · 69호(기울기 대조). 셀: NMC811(Ecopro) 90 : C65 5 : PVDF-HFP 5 · Al 박 · 170/172 µm · 공극 20 % · 1 M LiPF₆ EC:DMC 1:1 wt 두 방울 · GF/B 0.68 mm · Li 250 µm ∅5.6 mm · PTFE 관 셀 · C 클램프(압력 값 0) · 2.8–4.4 V · C/10 CC-CV(2.5 h 양 끝) · C/3 CC(1C 셋 · 끝 다섯 6 분 정전압) · 율당 셀 1(세 셀 나란히 — 셋째 보고 0) · 온도 미인쇄.
- **채움표 79호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(층 하나) · Q2 없다(층 하나 — operando 깊이 회절) · Q3 층 셋 · Q4 0/79 **일흔한 번째 성질**("깊이별 구조 SOC 를 같은 셀 맨 앞 층의 부피 ↔ 셀 방전 전하로 자기 교정해 읽되 — 그 기준 층이 셀 평균보다 앞서 방전한 구간을 교정에 쓰고, 두 상 조각은 첫 충전 끝 고정 scale 비의 가중평균이라 평균 순서에 따라 같은 층의 SOC 가 0.2 · 알짜 흐름의 부호까지 바뀌며, 2.4–2.9° 기울기가 20 µm 빔을 중첩 깊이 평균으로 바꾼다 — 그리고 과잉 충전 전하의 '실재' 를 2-매개 재척도 뒤 ESOC ↔ ASOC 일치로 판정한다") · Q5 해당 없음(층 하나 — 2전극 Li 분극 · 분리막) · Q6 없다 · Q7 해당 없음 · Q8 층 하나.
- **곱 축퇴 처방 예순두 번째 적용**: 적용 불가(`R` · `C` 0) · 처방 표 새 줄 없음 · 곱 밖 관찰(연결된 전극의 겉보기 용량 부족 = `η(z)` · CV · 역방향 · 여러 주기로 돌아옴) · "SOC 추종 상 분율" 줄 경고 행에 붙일 조건(평균 순서 · 비 고정 · 기하 혼합).
- ⚠ 어긋남 23 건(D1 170 ↔ 172 µm · D2 ∅5 ↔ 4.75 mm · D3 "1.0 mAh/cm2" 단위 · D4 Fig. 3 캡션 색 ↔ 범례 · D5 S6 범례 기울기 ↔ 글 · D6 표 1 사이클 1 excess 25 ↔ 35 · D7 "about a third" ↔ 21–27 % · D8 "18 h" ↔ ≈16.3 h · D9 원형 0.12 설명 문장 · D10 "linear change in the unit cell volume" ↔ S8 · D11 "<10%" ↔ +0.10 … +0.16 · D12 Fig. 2c −171 색 · D13 Fig. 4 세 판 시간축 · D14 Fig. 4c 무전류 구간 · 단계 시간 · D15 결론 둘째 현상 서술 0 · D16 Fig. 2 ↔ 3 두 상 조각 0.20 · 흐름 방향 · D17 Sup2 = Sup3 − 둘째 상 · D18 r_wp 둘 · D19 정련 항목 · D20 S7 "near the current collector (z = −71)" · D21 PTFE d · D22 "La Jolla, XA" · D23 Fig. 3 가로축 끝).
- 낱말 지문(본문 | SI): `identif` · `sensitiv` · `uncertain` · `uniqu` 1 · 7 · 1 · 0 | 0(식별 · 민감도 · 유일성 서술 0) · `error` · `±` · `standard deviation` **0** · `OCV` · `open circuit` · `relax` **0** · `tortuos` 0 · `pressure` 2(값 0) · `LAM` · `LLI` · `degradation` · `inactive` · `isolat` **0** · "no longer electrochemically active" 1 · `weighted average` 2 · `two-phase` 2 · `tilt` 2 | 6 · `misalign` 5 | 7 · `calibrat` 4 | 2 · Li 함량 0 · `ASOC` 22 | 1.
- PDF 메타데이터: 본문 `%PDF-1.3` · title "cm0c00983 1..7" · creator "Arbortext Advanced Print Publisher 11.2.5208/W Library-x64" · producer "Acrobat Distiller 8.1.0 (Windows); modified using iTextSharp.LGPLv2.Core 3.7.4.0" · 생성 2020-08-04 16:26:57 −04'00'(호 판 — XMP versionIdentifier "Issue") · 수정 2026-09-28 06:02:07 +00'00'(= 내려받기) · XMP 3,605 B(doi · ORCID 11 · VoR · © ACS · CC 필드 0) · startxref 1 · PageLabels 1 부터 · 글꼴 27 · Fig. 1 · 2 벡터 · 여백 띠 "Downloaded from pubs.acs.org/cmatex/article-pdf/32/15/6358/13117691/cm0c00983.pdf by HANYANG UNIV user on 28 September 2026"(IP 없음 · 표지 쪽 없음) — 76호와 같은 ACS 부류 / SI `%PDF-1.5` · author "zhuo li" · creator "Acrobat PDFMaker 17 for Word" · producer "Adobe PDF Library 15.0; modified using iTextSharp.LGPLv2.Core 3.7.4.0" · 생성 2020-06-30 19:30:12 −04'00'(수정본 접수 전날) · XMP 1,852 B(uuid 둘 · pdfx:SourceModified) · 태그 PDF · 여백 띠 "…/article-supplement/1320201/pdf/cm0c00983_si_001/ …". ⚠ 부수 변경: `raw/figures/_sources.json` 에 이 편 항목(자동 14 — 수동 3 은 `figures.json` 에만)이 추가됐다.
- 보류 결정 (가)–(스): **(두)** 근거(직접 쪽 — 역방향 구동 중 계속 반응(연결의 양성 서명 · 24호 40 % 셀에 이은 둘째 표본) · 여러 주기 드리프트 두 줄 · 셀 안 휴지 칸은 여전히 빔 — 계획 밖 ≈0.3 h 한 번은 구배 작을 때) · **(터)** 근거(일곱째 교정 형태 — x 아닌 자기 교정 · 기준 층 = 셀 평균 가정 · 비선형 · 평균 순서) · **(주)** 근거(넷째 표본 — 방향만 · 분리막 · 상대극 몫 미분리) · **(노)** 근거(깊이 층위 — 같은 전극 격자 ΔV/V 앞 −7.1 ↔ 뒤 −0.9 %) · **(러)** 약한 근거(경고 쪽) · **(도)** 약한 근거(NMC811 첫 사이클 결손의 깊이 몫) · **(브)(므)** 약 · **(쿠)** 지목 +1(Liu 2019 [20] → 2) · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷(두 상 조각 평균 순서 규칙을 교정 개념 · 곱 축퇴 경고 행에 둘지 · 24호 이봉 해석 자리 주석 · CE 결손 → LLI 배정 전 구조 대조를 (브)에 붙일지 — 설계 결정만 · 79호 후속 요청(Liu 2020 *J. Appl. Cryst.* [24] 등) + 3차 묶음 파일 42(측면 구배 — 파일 이름 · 원장 행만 확인)와의 연결).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 79호 행 · 79편 누적 · Evidence 일흔네 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[nmc-lattice-li-content-calibration]](79호 절 · 표본 표 79호 행 · 흡수 표기 · 주장하지 않는 것 둘) · [[assb-apparent-capacity-decomposition]](79호 절 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](예순두 번째 적용 · 주장하지 않는 것) · `index.md`(교정 · 3 항 분해 개념 줄에 79호 한 구절 · 페이지 수 53 그대로 · 날짜 2026-09-29). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Li Z. 2020 행 흡수 표시 · 서술 정정("가중평균 관행의 선례" → 두 상 정련 뒤 고정 비 평균 · 두 상 = 기하 혼합 / "Q2" → Q2 층 하나 · Q4 0/79) · 지목 +1(79) Liu 2019 [20] · 신규 후보 · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h 41 행 · §6-3-i 41 행 상태)는 호출자 몫.
- 후속(서지 기준, 미열람): **Liu H., Li Z., Grenier A., Kamm G.E., Yin L., Mattei G.S., Cosby M.R., Khalifah P.G., Chupas P.J., Chapman K.W. 2020 *J. Appl. Crystallogr.* 53, 133**([24] — 이 편이 "elsewhere" 로 넘긴 기울기 · 기하 수차 처리) · **Liu H., Kazemiabnavi S., … Chapman K.W., Chupas P.J. 2019 *ACS Appl. Mater. Interfaces* 11, 18386**([20] = 76호 [52]) · Liu H., Allan P.K., Borkiewicz O.J., Kurtz C., Grey C.P., Chapman K.W., Chupas P.J. 2016 *J. Appl. Crystallogr.* 49, 1665([19] — RATIX) · Li W., Asl H.Y., Xie Q., Manthiram A. 2019 *J. Am. Chem. Soc.* 141, 5097([26]) · Märker K. … Grey C.P. 2019 *Chem. Mater.* 31, 2545([27] — 56호 · 3호 인용과 같은 편으로 보임) · Xu K. 2014 *Chem. Rev.* 114, 11503([30]) · Danner T. … Latz A. 2016 *J. Power Sources* 334, 191([13] = 58호 [63]).

## [2026-09-29] ingest | assb 80호 — Okasinski J.S., Shkrob I.A., Chuang A., Rodrigues M.-T.F., Raj A., Dees D.W., Abraham D.P. 2020, In situ X-ray spatial profiling reveals uneven compression of electrode assemblies and steep lateral gradients in lithium-ion coin cells (Phys. Chem. Chem. Phys. 22, 21977–21987)
- raw: `raw/papers/okasinski2020_edxrd-profiling-coin-cell-uneven-compression-lateral-gradients.md` (sha256 봉인 — `pdf_sha256` · `si_sha256`(ESI pptx) · zip 둘의 sha256 은 `source_url_note`) · 그림 `raw/figures/okasinski2020_edxrd-profiling-coin-cell-uneven-compression-lateral-gradients/` (자동 10 — 본문 그림 7 · 표 3 · 라벨 어긋남 0 · 잘림 0 · ⚠ 표 셋 자동은 쪽 전체(과대 영역 — 내용 온전) · tab_1 = tab_2 바이트 동일 · **누락 넷**(그림 2 · 4 · 6 · 표 4 — 후보로도 안 올라옴) + 수동 7(그림 2 · 4 · 6 · 표 4 · 표 1–3 — 300 dpi) + ESI 10(pptx media 원본 8 — 포스터 프레임 7 · 그림 S1 / 그림 S6 사진 둘은 슬라이드 srcRect 크롭); 27 항목 **전부 열어 봤다** — `figures.json` note 27; 본문 그림 10 장은 전부 래스터라 그림 2 · 4 · 5 · 6 · 8 · 9 는 원본 이미지 픽셀로, 3 · 7 · 10 · ESI 포스터는 눈으로 읽었다; ESI 이미지 13 장 모두 열었고 mp4 7 은 컨테이너 머리만 — 내용 판독 0). **3차 묶음 파일 42**(스물두째 편 — 2차 묶음 큐 번호와 별개) · 원장 "★ Okasinski·Shkrob·Chuang·…·Abraham 2020 · 지목 24 · Q3·Q6 · 가압 불균일과 측면 구배 — 조각 정렬 문제 점검용 · 79호 메모" · 24호 ref 36 · SI ref 16 · Argonne APS(Okasinski · Chuang — 24호 공저자 · 같은 빔라인 6-BM-A) + CSE(Shkrob · Rodrigues · Raj · Dees · Abraham) · **액체 NCM523/흑연 CR2032 코인셀 — ASSB 아님**.
- ★★★ **(a) 무엇을 쟀나**: EDXRD(굽힘 자석 백색광 · Ge 검출기 고정 2θ ≈2.287°) · 빔 2 mm × 10 µm · z 2 µm 간격 × y 10–15 위치 · 방사선 정렬 · 게이트 다항식 × 가우시안 빔 윤곽으로 hard edge(빔 폭 전역 적합 — 값 미인쇄) · **게이지 길이 미인쇄** — `[재현]` L = h_i/tan2θ + h_d/sin2θ = 0.50(수광 10 µm) … 5.26 mm(200 µm) · 같은 식에 24호 조건을 넣으면 5.58 mm(24호 "≈5.6 mm" 재현). "uneven compression" = 두 전극 hard edge ↔ y → 간극 ζ(y) → 식 (3) 판 적합 → δ — `[인쇄]` 표 1 δ 3.5–15.8 µm · `[재현]` 그림 6 적합이 δ · `±` 까지 재현(셀 1 10.86 ± 0.90 ↔ 10.8 ± 0.9 · 셀 8 3.48 ± 0.54 ↔ 3.5 ± 0.6) · **표 1 마지막 열 = δ/(ζ₀+δ)**(인쇄 서술 δ/⟨ζ⟩ 이면 셀 1 33.7 · 셀 5 · 6 56 · 51 % ↔ 인쇄 30 · 44 · 44 — D5) · 간극 가장자리 16.5–25.2 ↔ 가운데 23–36 µm(분리막 공칭 20 µm — 절대 압축은 셀 절반에서만). "steep lateral gradients" = 흑연 u₀(LiC₆ + LiC₁₂) 평탄 ↔ 바깥 ≈2 mm 띠 급락: `[도표]` 셀 1 0.644 → 0.539 · 0.564 · 셀 2 0.847 → 0.545 · 0.580 · `[재현]` 바깥 띠 = 면적 50 % · 면적 평균 0.611 · 0.779 · 충전 39.6 · 56.6 분(같은 전류 2.247 mA cm⁻² — 이름표 "1.50C" · "1.06C" = 전류 ÷ 충전량 · 1C 2.37 mA cm⁻² 로 둘 다 0.948C, D11) · 휴지 "several hours" 뒤 지도(시각 · 순서 미인쇄) · 양극 평탄.
- ★★★ **(b) 24호 G8 · G9 · 79호 교락**: G8 ✅ 검사 항목 — y 마다 경계 적합(24호는 안 씀) · 조립체 기울기 0.17–0.81 µm/mm = 0.010–0.046°(24호 가정 0.2° 의 1/4–1/20) · **곡률 δ 3.5–15.8 µm 가 주항**(20 µm 조각과 같은 크기) · x 방향 기울기는 이 편도 못 잰다. G9 ✅ 중앙 기둥 = 평탄부 · `[재현]` 중앙 ↔ 면적 평균 절대 x +0.033 · +0.068(+5.4 · +8.7 %) — 24호 쿨롱 ↔ XRD 폐합 ±7 % 가 못 가르는 크기 · ⚠ 측면 방향이 24호와 반대(가장자리 늦음 ↔ "circumference … reacted first") — 방향은 설계 의존. 79호 교락: 크기 안 줌 · 형태(가장자리 띠 반지름의 ≈30 % · 좌우 차 +0.02–0.04 · 방향 설계 의존)와 방법(측면 주사 + 경계 적합)만.
- ★★★ **(c) 압력 (Q6)**: 원인 = 오목 캔(가운데 간극 <15–30 µm · 셀 1 18 µm) 위 가장자리만 받친 바닥 스페이서의 탄성 휨 · 위 전극은 평평. 하중 `[인쇄]` 0.14 MPa(판 식) · 0.185 MPa(스프링 K ≈110 N/mm × Δ 0.27 mm) ↔ `[재현]` 인쇄 식 · 인쇄 값으로 **K = 92.0 N/mm → 0.157 MPa**(D3) · 스프링 자유 높이 1.4 mm 는 "∼16%" 와도 내부 높이 닫힘과도 안 맞고 ≈1.65 mm 에서 둘 다 맞는다(D2) · Al 0.41 mm 스페이서는 판 식 37–44 ↔ 측정 15.8 µm(캔 간극에 닿은 쪽 `[해석]`) · 구속 둘(스프링 δ 6.1 · 10.8 ↔ 스페이서 넷 3.9 · 6.2 µm · 쐐기는 스페이서 쪽). ASSB 로: 크기 ❌(운전 5–62 MPa · ×25–600) · 측정 방법 · 사슬 모양(면 압축 불균일 → 측면 저항 → 측면 `η(r)` → 가장자리 도금) ✅ · 측면 Wagner 식 ✅(`[재현]` 코인셀 w ≈5 × 10³ ↔ SE 펠릿 κ 1.9 mS cm⁻¹ · ζ 0.5–1 mm 면 w ≈24–49 · 띠 mm 급 — 흑연 액체 i₀ 를 빌린 규모 논증) · `[재현]` 분리막 옴 강하 ε 0.4 → 0.1 에서 0.79 → 6.32 Ω cm²(X선 셀 전류 1.8 ↔ 14.2 mV).
- ★★★ **(d) θ ↔ η**: **셀 안 휴지의 첫 직접 표본** — `[인쇄]` "This non-uniformity persisted even after the cells were at rest for several hours" · 방법 절 "in multiphase materials such as lithiated graphite, Li⁺ ion gradients persist almost indefinitely as phase boundaries serve as barriers" → 흑연 휴지 지속은 `θ` 의 서명이 아니다 · 양극(고용체) "varies little … suggesting smoothing … in the absence of current"(휴지 전 지도 0) · 가장자리 띠도 LiC₁₂ 까지 반응(연결) — `θ` 형 영역 0 · 셀 8(C/12.3 · x 1.0) ESI S4 포스터 y = −7 mm 에 LiC₁₂ 우세(한 프레임 — 정체 미상) · 역방향 · 다음 사이클 0 · 모형 셋은 전부 연결된 전극의 저항 분포. ⇒ 원장 (두) (i) 휴지 줄에 재료 조건("휴지 뒤 지속은 고용체 창에서만 `θ` 쪽 근거") — 74–79호 다섯 편이 비워 둔 칸을 처음 채우되 판정력 없는 재료로.
- ★★ **(e)(f)**: ESI pptx 슬라이드 10 · 이미지 13 · mp4 7(판독 안 함) — 본문 인용 자리(S1a · S1b · S2–S9) 전부 있음 · 본문 Table S2 · ESI Table S3 인용 — **지원 표 PDF 는 받은 자료에 없음**(사용자 결정 2026-09-28 · 추정 0) · ESI 어긋남(S2 = 셀 8 · "(300) 만 적분" · S4 "graphite cathode" · S7 "semi-infinite periodic" · "92 %" · S1 단위 mm). Q1 해당 없음(`θ(N)` 0/80 · 층 하나 — 측면 `η(r)`) · Q2 없다(층 하나 — 상 분율 · 기하 채널 · X선 ↔ 전하 규약 차 0.15–0.17) · Q3 층 여섯 · Q4 0/80 · Q6 층 둘 · Q8 층 하나(NCM523 `a` 시그모이드). 잇기: 24호(G8 · G9 · 같은 빔라인) · 76호(관찰 셀 가장자리 비균일 후보 ② · ④ 에 형태 · 깊이 Wa ↔ 측면 w) · 79호(측면 교락 · 휴지 칸) · 22호(암묵적 휴지 = 고용체 쪽) · 66호(α 판정) · 62 · 73 · 77호(ASSB 운전 압력 ↔ 코인셀). 셀: NCM523(Toda) 90 % · 18.6 mg cm⁻² · 71 µm · 35.4 % ‖ Celgard 2320 20 µm · 40 % ‖ 흑연 SLC1506T 91.8 % · 9.9 mg cm⁻² · 70 µm · 34.5 % · 1.2 M LiPF₆ EC:EMC 3:7 40 µL · 전극 둘 다 1.58 cm²(같은 크기) · Hohsen CR2032 · 형성 C/10 × 2 + C/25 · 3.0–4.1 V · 30 °C.
- **채움표 80호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(층 하나) · Q2 없다(층 하나 — EDXRD 프로필로메트리) · Q3 층 여섯 · Q4 0/80 **일흔두 번째 성질**("측면 구배의 원인을 분리막 기공 압축으로 배정하되 — 대안 하나(1차 전류 가장자리 효과 · Wagner 수 ≈5 × 10³)만 수치로 배제하고 전극 측면 정합 · 조직 · 휴지 중 재분배는 다루지 않으며, 채택한 원인의 크기(Ξ 0.75 → 가장자리 ε 0.1)는 측정 간극과 맞추지 않은 가정이고, 모형은 실험 율(≈0.95C)의 3–6 배에서 모양만 맞춘다") · Q5 해당 없음 · Q6 층 둘(하중 크기 · 면 분포 — 액체 코인셀) · Q7 해당 없음(층 하나 — 사후 고리) · Q8 층 하나.
- **곱 축퇴 처방 예순세 번째 적용**: 적용 불가(`R` · `C` 0) · 처방 표 새 줄 없음 · 곱 옆 관찰(측면 균일 모형으로 적합하면 가장자리 띠의 덜 쓰인 몫이 기하 면적 인자로 곱이나 `ε_p` 에 흡수 — `[재현]` 면적 평균이 중앙보다 5–8 % 낮다) · 경고 행에 교정 계수 검사 표본(α 오기 쪽).
- ⚠ 어긋남 25 건(D1 방사선 사진 판 "Fig. 1a" ↔ 1b · D2 스프링 자유 높이 · D3 스프링 상수 92 ↔ 110 · D4 판 하중 0.130 ↔ 0.14 · D5 표 1 마지막 열 정의 · D6 그림 6 캡션 "ζ₀ in Table 1" · D7 격자 α 2.5 × 10⁻³ ↔ 10⁻² · "x̌ < 0.2" 부등호 · D8 (101) d 식 a · c · D9 Legendre P2n′(1) · 2n+1 · D10 표 3 x 기준(이론 ↔ C/10 방전 용량) · D11 C-rate 이름표(같은 전류) · D12 그림 8a 양극 = 1 − x̌ · D13 표 4 창((101) 없음 · 틈 3.430–3.500 Å ↔ 방전 띠 3.456) · D14 S2 "(300) 만 적분" · D15 S2 셀 8 ↔ 그림 2 셀 1 · D16 S7 반무한 주기 · 92 % · D17 S1 mm · D18 S4 "graphite cathode" · D19 z 방향 표기 · D20 그림 9 캡션 "10% charge" · D21 S8 · S9 · D22 참고문헌 25 서지 · D23 "2 microns" 분해능 · D24 PageLabels 4–14 · D25 오기).
- 낱말 지문(본문 | ESI): `identif` · `sensitiv` · `uncertain` · `uniqu` 0 · 0 · 1 · 1 | 0(식별 · 민감도 서술 0) · `error` 0 · `±` 9(전부 δ) · `LAM` · `LLI` · `degrad` · `inactive` · `isolat` **0** · `rest` 2 · `relax` 0 · `persist` 4 · `OCV` · `open circuit` 0 · `calibrat` 0 · `tilt` 0 · `misalign` 2 · `wedg` 3 · `pressur` 3 · `compress` 14 · `spring` 21 · `deflect` 14 · `porosit` 17 · `pinch` 3 · `contact` 5(전부 기계 접촉) · `Wagner` 1 · `plating` 19 | 3 · `edge` 31 | 6 · `solid-state` · `ASSB` 0.
- PDF 메타데이터: 본문 `%PDF-1.3` · author "John S. Okasinski" · creator "Aspose Ltd." · producer "Aspose.PDF for .NET 22.3.0"(통째로 다시 씀 — startxref 1) · 생성 2020-10-04 08:03:56 +05'30' · 수정 2026-03-17 21:35:39 +00'00' · XMP 3,485 B(doi · dc:rights "This journal is © the Owner Societies 2020" · CC 필드 0) · RSC 배너 "Published on 15 September 2020 · Licence and permissions"(IP · 여백 띠 0) · PageLabels 4–14(D24) · 그림 10 장 전부 래스터(CMYK JPEG 9 · PNG 1) / pptx core creator "Shkrob" · lastModifiedBy "Abraham, Daniel" · revision 97 · 2020-05-11 → 2020-07-02 · MMClips 7 · 댓글 작성자 둘 · 댓글 파일 0 · mp4 부호화 시각 2019-12-30 … 2020-05-16. 해시 넷(본문 · ESI zip · 본문 사본 zip · pptx) 호출자 명시값과 일치 · 둘째 zip = 본문 PDF 사본(바이트 동일).
- 보류 결정 (가)–(크): **(두)** 직접 근거(첫 셀 안 휴지 — 다상이면 지속이 `θ` 아님 · 재료 조건 줄) · **(주)** 근거(다섯째 표본 — 대안 하나(1차 전류 가장자리 효과)를 Wagner 수로 수치 배제한 첫 표본 · 채택 원인 크기는 가정 · 저항 측정 0) · **(크)** 근거(파일 42 대조 수행 — 79호 교락의 형태만 · **Li W. 2019 *JACS* [18] 지목 +1(79 · 80 → 2)**) · **(하)** 근거(구속 형식 둘 대조 · 원시 하중은 두 추정뿐 · 스프링 식 비재현) · **(터)** 근거(여덟째 교정 형태 — NCM523 `a` 시그모이드 · α 오기 쪽 · (101) 식 · 부등호) · **(투)** 약한 근거(측면 Wa 의 인쇄 표본 — ASSB 로 두 자릿수 작아짐) · **(러)** 약한 근거(경고 쪽 — 측면 `η(r)` 이 부분 이용으로 보이고 휴지로도 안 풀림) · **(즈)** 약(24호 이봉의 기하 기원 후보에 측면 혼합 · 곡률 — 단 중앙 기둥은 평탄부) · **(므)** 약(흑연 쪽 — X선 − 이론 기준 0.15–0.17 · 방전 띠 3.456 Å) · **(쿠)** 근거 0(76호 [21] Mistry 2020 = 이 편 [14] — 원장 행 0 · 기록만) · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 다섯(측면 축 표기 규약 · 합성 truth 측면(반경) 축 선택지 — 코드로 옮기면 RUN_SCOPE 가 움직이므로 설계 기록만 · 휴지 연산자의 재료 조건 줄 · 24호 G8 · G9 자리 주석 · 80호 후속 요청(Yao 2019 *EES* [6] 등)).
- **봉인된 digest 에 대한 정오 2건** (raw 는 불변층이므로 정정은 여기가 보유): ① digest §판정 먼저 표 마지막 행의 "새 판단 거리 **넷**(§보류 끝)" — §보류 끝 목록은 **다섯**(1 측면 축 표기 규약 · 2 합성 truth 측면 축 · 3 휴지 재료 조건 줄 · 4 24호 G8 · G9 자리 주석 · 5 80호 후속 요청)이다. ② digest §Q1~Q8 표 Q3 칸의 "지면 어긋남 **24 건**" — §어긋남 표는 **D1–D25 = 25 건**이다(카드 · 이 로그는 25 로 적었다).
- ⚠ 부수 변경: 추출기가 `raw/figures/_sources.json` 을 다시 쓰며 이 편 항목을 더했고, `figures.json` 을 27 항목(수동 7 · ESI 10 · note 27 · `sources` 에 pptx 추가)으로 고친 뒤 색인 함수 `_write_sources_index` 를 다시 돌려 이 편 figures 27 로 맞췄다 — 같은 실행에서 **79호 항목 figures 가 14 → 17** 로 바뀌었다(79호 `figures.json` 의 수동 3 을 이제 센다 — 결정적 출력).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 80호 행 · 80편 누적 · Evidence 일흔다섯 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](80호 절 · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](80호 절 · 주장하지 않는 것 · updated) · [[assb-operando-pressure-signal-attribution]](80호 주석 · 주장하지 않는 것 · updated) · [[nmc-lattice-li-content-calibration]](80호 절 · 표본 표 80호 행 · 흡수 표기 · 주장하지 않는 것 둘) · [[assb-lampe-contact-product-degeneracy]](예순세 번째 적용 · 주장하지 않는 것) · `index.md`(3 항 분해 · 압력 창 · 압력 신호 · 교정 개념 줄에 80호 한 구절 · 페이지 수 53 그대로). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Okasinski 행 흡수 표시 · 서술 보강(가압 불균일 = 기하 측정 · 측면 방향 설계 의존 · 79호 교락은 형태만 / Q3 · Q6 → Q3 층 여섯 · Q6 층 둘 · Q4 0/80) · 지목 +1(80) Li W. 2019 [18] · 신규 후보 Yao 2019 *EES* [6](★★★) · Yao 2019 *AEM* [7] · Cannarella & Arnold 2015 [11] · Shkrob 2019 [16](★★) · [5] · [22] · [23] · [15] · [21](★) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h 42 행 · §6-3-i 42 행 상태)는 호출자 몫.
- 후속(서지 기준, 미열람): **Yao K.P.C., Okasinski J.S., Kalaga K., Shkrob I.A., Abraham D.P. 2019 *Energy Environ. Sci.* 12, 656**([6] — 같은 방법 · LiC₁₂ 산란 단면 보정의 원전 · 빠른 충전 깊이 구배) · Yao K.P.C., Okasinski J.S., Kalaga K., Almer J.D., Abraham D.P. 2019 *Adv. Energy Mater.* 9, 1803380([7]) · **Cannarella J., Arnold C.B. 2015 *J. Electrochem. Soc.* 162, A1365**([11] — 분리막 압축 → 불균일 전류 · 국소 열화) · Shkrob I.A., Rodrigues M.-T.F., Dees D.W., Abraham D.P. 2019 *J. Electrochem. Soc.* 166, A3305([16] — 전극 사양 · 삼상 흑연 모형) · Cannarella J., Liu X., Leng C.Z., Sinko P.D., Gor G.Y., Arnold C.B. 2014 *J. Electrochem. Soc.* 161, F3117([5]) · Rodrigues M.-T.F., Kalaga K., Trask S.E., Dees D.W., Shkrob I.A., Abraham D.P. 2019 *J. Electrochem. Soc.* 166, A996([22] — i₀ 40 µA cm⁻² 출처) · Tanim T.R. … Trask S.E. 2020 *Cell Rep. Phys. Sci.* 1, 100114([23]) · Harris S.J., Lu P. 2013 *J. Phys. Chem. C* 117, 6481([15]) · Wagner C. 1951 *J. Electrochem. Soc.* 98, 116([21]) · Li W., Asl H.Y., Xie Q., Manthiram A. 2019 *J. Am. Chem. Soc.* 141, 5097([18] = 79호 [26]).

## [2026-09-29] ingest | assb 81호 — Xu H., Yang S., Li B. 2024, Pressure Effects and Countermeasures in Solid-State Batteries: A Comprehensive Review (Adv. Energy Mater. 14, 2303539)
- raw: `raw/papers/xu2024_pressure-effects-countermeasures-ssb-review.md` (sha256 봉인 — `pdf_sha256` 42e87f7b…a745c26 · 12,996,527 B · 보충 자료 없음) · 그림 `raw/figures/xu2024_pressure-effects-countermeasures-ssb-review/` (자동 18 — 그림 16 · 표 2 · 라벨 전부 일치 · 누락 0 · 잘림 0 · ⚠ 표 둘 자동은 쪽 전체(과대 영역 — 내용 온전 · 바이트 동일 0) + 수동 2(표 1 · 2 촘촘 · 300 dpi) · **연 것 20/20** · `figures.json` note 20 · 그림 16 장 전부 래스터 — Fig. 1 패널 셋 · 6c2 · 7d · 8b · 8d · 14b 는 2 배 확대 + 화소 눈금).
- **3차 묶음 파일 43**(스물셋째 편; 2차 묶음 "큐 N" 과 별개 — "큐 43" 아님). 원장 "★★★ Xu·Yang·Li 2024 · 지목 25 · 32 · 33 · Q6 · 압력 종설 — 8호가 인용한 '<≈1 MPa' 의 출처로 보인다 · 확인처는 이 원문뿐". Beihang 재료과학공학부 세 저자 · Review(Editor's Choice) · **1차 측정 0** · 참고문헌 171.
- ★★★ **(a) "<≈1 MPa"**: ✅ 인쇄는 있다 — `[인쇄]` 초록 p. 1 "far exceed the current industrial requirement (< 1 MPa)" · 인용 0 · 본문 재진술 0 · `< 1 MPa` 류 전수 2(다른 하나는 Fuchs [140] 실험 조건) · 그림 속 글자는 저자 모식 다섯을 눈으로 확인해 0. 8호 귀속 ✅("approximately" 는 8호 추가) · 출처 ❌. 참고문헌에 Sharafi 2016 · Wang & Sakamoto 2018 · Wang 2021 *Joule* 0 · Sakamoto 실험실 편 여덟은 "< 1" 문장에 안 붙음. ⇒ 계보 **아홉 편(독립 인쇄 여덟 — 8호는 81호의 재인용) · 여섯 값(0.1 · 0.4–1 · < 1 · 1 · 2 · 5) · 띠 0.1–5 MPa · 확인된 원전 0 그대로** · 인용 없이 인쇄한 편 넷(25 · 33 · 59 · 81) · 빈 다리 셋(8 → 81 · 13 → 59 · 13 → 60) · 33호 가설(배경 = 자기 자료)은 지면으로 확인 안 됨.
- ★★★ **(b) 압력 지도**: 자기 서술 넷(< 1 요구 · 제조/조립 "hundreds" ↔ 운전 "dozens of MPa" · "exceeding 10 MPa" · 98 % — 표 1 요약 행까지 다섯 줄) · 재인용 70 행(표 여덟) · 표 2 "low-pressure SSBs" 0.1–4.9 MPa — `[재현]` < 1 MPa 7 행 중 0.1 여섯 · 둘은 같은 지면이 대기압 / 무가압 · 하나는 126 kPa · 고적재(≥10 mg cm⁻²) 셋은 전부 2–4 MPa · 같은 원전에 두 압력 셋(D5).
- ★★★ **(c) 창**: 모형 아래 벽(≈0.4 · 3 · 12 · 20 · 100 MPa) ↔ 실험 위 벽(7 · 7.4 · 11 · 13 · 25 · 75 MPa)이 Li 금속 쪽에서 겹침(이 편 무언급) · 처방은 "pressure-insensitive / pressure-independent" 로 창을 버림 · 세 갈래(SSE 계면 · 구조 공학 · 전극 설계) 전부 (압력 한 점, 성능 한 점) · 양극 쪽 압력 함수 0 · `[재현]` Wang [7] σ_c ∝ (j/l₀)^(1/m) — 0.1 → 4 mA cm⁻² 에 ≈0.64 → ≈1.3–1.7 MPa · l₀ ≈0.72 mm.
- ★★★ **(d) `θ(N)` · 식별성**: 양극 재인용은 [81] = 4호 한 문단 — 본문 "LF · HF remain unchanged" ↔ 자기 재수록 Fig. 7d `[도표]` LF 108.3 → 38.6 kΩ(−64 % · MF 감소의 ≈132 배) ↔ 4호 원문 "decreases after pressing" · 셀 "LLZO-based"(D1) → 33 · 59호에 이은 셋째 종설 층 표본 · 식별성 서술 0("decouple" 4 — 목표어 · 주파수 배정).
- ★★ **(e) 잇기 · 인용 대조**: 25호 ✅ · 33호 ⚠ 절반(운전 "수백 MPa" 는 이 편에 없음) · 원전이 위키에 있는 여섯 중 셋 선다(5 · 6 · 61호) · 셋 어긋난다(4 · 39 · 62호 — 전부 압력 ↔ 접촉 · 신호 귀속 자리) · 압력 신호 재수록 넷(62호 두 패널 · Lee 2021 · Ham 2023 · Liang 2021) — 본문 전사 오류 셋(D2 · D3 · D4).
- **채움표 81호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나) · Q2 없다(층 하나) · Q3 층 하나(재인용 출처 번호가 캡션 ↔ 본문 ↔ 표에서 갈림) · Q4 0/81 **일흔세 번째 성질**("'decoupling' 을 목표로 인쇄하고, 이 편의 유일한 분해 사례(재가압 EIS 주파수 배정)를 옮기며 음극 몫(LF)을 '불변' 으로 지운다") · Q5 해당 없음 · Q6 층 다섯 · Q7 해당 없음 · Q8 층 하나(양극 부피 변화 %).
- **곱 축퇴 처방 예순네 번째 적용**: 적용 불가(1차 자료 0) · 처방 표 새 줄 없음 · 곱 안 관찰(접촉 역학 식이 압력을 면적 인자에만 걸고 힘 지수 −1/2 · −1/3 · −1 이 그 가정의 검사 — 소성 지수 오기 D12 · 데이터 적합 0).
- ⚠ 어긋남 21 건(D1 4호 재가압 전사 · D2 Fig. 8d "5.2 to 2.3" = 하강 폭 · D3 Fig. 8b LTO 패널 ↔ "LCO and In-Li" · D4 Ham "cathode loading" ↔ 전류 그림 · D5 같은 원전 다른 압력 · D6 표 2 마지막 행 = Ning [104] 자료 · D7 MD "Wad < 0.25 → 100 MPa" ↔ 그림 ≈160–175 · D8 Wang ≈0.4 ↔ 교차 0.64–0.67 · D9 Fig. 14b · D10 Sakka "˂50 MPa" · D11 LGPS 476 ↔ 467 · @3MPa · D12 소성 지수 · D13 "MPa m−2" · D14 인용 번호 · D15 저자명 · D16 Fig. 1 캡션 연도 · Whiteley 출처 0 · D17 오기 · D18 five-fold ↔ 458 % · D19 표 1 97.8 % ↔ Fig. 3 ≈75 % · D20 85 % 통계 · D21 G_Li 4.8 ↔ 2.83 GPa).
- 낱말 지문(본문 | 참고문헌): `MPa` 98 | 0 · `< 1 MPa` 2 · `industr*` 4 · `requirement` 4 · `stack pressure` 56 · `contact loss` 10(양극 0) · `percolat` · `inactive` · `dead` 0 · `identif` 3 · `uniqu` 3 · `uncertain` · `error` 0 · `decoupl` 4 · `LLI` · `LAM` 0 · `re-press*` 1 · `sensor` · `load cell` 0 — 합자(ﬁ · ﬀ · ﬂ · ﬃ)가 `effect` · `significant` · `identif` 를 통째로 가린다(NFKC 뒤 셈).
- PDF 메타데이터: `%PDF-1.6` · creator "LaTeX with hyperref package" · producer "Acrobat Distiller 24.0 (Windows); modified using iText 4.2.0 by 1T3XT" · 생성 2024-04-01 +05'30' · 수정 2026-09-27 −07'00' · startxref 1 · %%EOF 1 · 암호화 · 주석 · 첨부 0 · PageLabels 1–27 · XMP 3,576 B(VoR · CC 필드 0) · 다운로드 띠(Hanyang University Library · 27/09/2026) · sha256 호출자 명시값과 일치.
- 보류 결정 (가)–(니): **(하)** 근거(재수록 · 종설 층 — Lee 2021 개방 회로 이완 · Zhang X. 유지 시간 · 62호 전극 몫 소거 · Ham 기저 ≈5 · ΔP ≈2) · **(거)** 근거(가닥 확인 — 요청 필요성 그대로) · **(주)** 약한 근거(여섯째 — 압력 판) · **(차)** 약한 근거(힘 지수) · **(노)** 약 · **(보)** 형식 참고 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(① 8호 가닥 종결 표기 ② 요구치 계보 남은 다리 요청 묶음 — Tian & Qi 2017 · Wang 2021 *Joule* · (거) 두 편(digest 는 Li Menglin 2025 도 넣었으나 이미 받음 — 아래 정오) ③ "0.1 MPa" 표기 규약 — 인가 · 대기압 · 셀 형식 하중).
- **봉인된 digest 에 대한 정오 2건** (raw 는 불변층이므로 정정은 여기와 카드 Status Log 가 보유): ① digest §보류 끝 "새 판단 거리 2" 가 Li Menglin 2025 *AFM*(13호 [35])을 요청 묶음에 넣었으나 원장 §1 · §4(2026-09-28 사용자 업로드) · `ASSB_TRANSFER_NOTE.md` §6-3-i 에 **이미 받음(3차 묶음 49-2 · ingest 대기)** 이다 — 요청 대상이 아니다. ② digest §후속 후보 마지막 행 "[76] · [74] · [8] | 81호 = 1 각" — [76] Yan … Chen *AEM* 2102283 은 52호 [16b] · 59호 [21] 도 인용해 지목 3(52 · 59 · 81) · 원장 §1 에 이미 행이 있다(지목 52). [74] · [8] 은 1 각 그대로.
- ⚠ 부수 변경: `figures.json` 에 note 20 · 수동 2 를 더한 뒤 색인 함수 `_write_sources_index`(같은 코드)를 다시 돌려 `raw/figures/_sources.json` 의 이 편 항목을 figures 20 으로 맞췄다 — 다른 편 항목 변화 0(diff 확인).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 81호 행 · 81편 누적 · Evidence 일흔여섯 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](8호 절 표지 · 13호 표 넷째 주석 · 81호 절 · 주장하지 않는 것) · [[assb-pressure-reapplication-separation-test]](81호 절 · 주장하지 않는 것 · updated) · [[assb-operando-pressure-signal-attribution]](81호 주석 · 표본 표 행 넷 · 주장하지 않는 것) · [[li-metal-yield-creep-vs-stack-pressure]](81호 주석 — 대조 넷 · 계보 줄 · updated) · [[assb-lampe-contact-product-degeneracy]](예순네 번째 적용 · 주장하지 않는 것) · `index.md`(재가압 · 압력 창 · Li 눈금 · 압력 신호 개념 줄에 81호 한 구절 · 페이지 수 53 그대로). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Xu 행 흡수 표시 · 지목 +1 · 신규 후보 · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h · §6-3-i 43 행)은 호출자 몫.
- 후속(서지 기준, 미열람): **Tian H.-K., Qi Y. 2017 *J. Electrochem. Soc.* 164, E3512**([71] — 12호 [60] 과 지목 2 · 원장 §1 에 없음) · **Lee C., Han S.Y., Lewis J.A., … McDowell M.T. 2021 *ACS Energy Lett.* 6, 3261**([45] — 14 · 59 · 81호) · **Ham S.-Y., … Meng Y.S. 2023 *Energy Storage Mater.* 55, 455**([93] — 59 · 81호) · **Ning Z., … Bruce P.G. 2023 *Nature* 618, 287**([104] — 33 · 81호) · LePage W.S., … Dasgupta N.P. 2019 *J. Electrochem. Soc.* 166, A89([66] — 5 · 14 · 81호) · Wang M.J., Choudhury R., Sakamoto J. 2019 *Joule* 3, 2165([7]) · Müller V., … Wohlfahrt-Mehrens M. 2019 *J. Electrochem. Soc.* 166, A3796([163]).

## [2026-09-29] ingest | assb 82호 — Schlautmann E., Weiß A., Maus O., Ketter L., Rana M., Puls S., Nickel V., Gabbey C., Hartnig C., Bielefeld A., Zeier W.G. 2023, Impact of the Solid Electrolyte Particle Size Distribution in Sulfide-Based Solid-State Battery Composites (Adv. Energy Mater. 13, 2302309)
- raw: `raw/papers/schlautmann2023_lpscl-particle-size-distribution-composite-transport.md` (sha256 봉인 — `pdf_sha256` 06fb3e2b…d6099649 · 2,202,178 B · `si_sha256` 3de6b636…92a4c2b0 · 5,725,633 B) · 그림 `raw/figures/schlautmann2023_lpscl-particle-size-distribution-composite-transport/` (자동 28 — 본문 6 · SI 22 · 라벨 전부 일치 · 누락 0 · 잘림 0 · ⚠ 과대 영역 넷(S2 · S5 · S7 · S9 위쪽에 앞 캡션 꼬리 — 내용 온전) · 자동 표 0("Table ST" 를 표 캡션으로 안 잡음) + 수동 4(표 ST1–ST4 · 300 dpi) · **연 것 32/32** · `figures.json` note 32 · 본문 그림 6 장 CMYK JPEG 래스터 · SI S14 만 벡터(좌표 판독)).
- **3차 묶음 파일 44**(스물넷째 편; 2차 묶음 "큐 N" 과 별개 — "큐 44" 아님). 원장 "★★ Schlautmann·Weiß·Maus·…·Bielefeld 2023 · 지목 25 · Q1·Q2 · 같은 변수(SE 입도 분포)의 독립 표본 — 25호의 셀 1개·교락을 가를 입력" · ⚠ 원장 · 25호의 끝 이름 "Bielefeld" 는 열한 명 중 열째 — 교신은 Zeier W.G. · Münster(Zeier) · JLU Giessen(Bielefeld — 모형) · FZ Jülich IEK-12 · AMG Lithium(시료 · PSD — 공저 셋 · COI 인쇄) · Research Article · CC BY · SI 19 쪽(그림 S1–S22 · 표 ST1–ST4).
- ★★★ **(a) 무엇을 바꿨나**: 시판(AMG) Li₆PS₅Cl 네 분말의 입도 분포 하나 — 만드는 법 인쇄 0 · 이름표(D50vol 4 · 11 · 20 · 40) ↔ `[도표]` 측정 D50 3.8 · 9.9 · 17.1 · 39.7 · M 부피 ≈24 % < 1.5 µm · 개수 D50 S ≈0.16 · M/L/XL ≈2.7 µm · ST2 내부 불일치(D9) · 고정: NCM811 70 : 30 · 무탄소 · 10.70 mg cm⁻² · 3 t × 3 min(≈375 / 340 MPa) · 50 MPa · 25 °C · 2.0–3.7 V vs In/LiIn · 같이 바뀐 것: void 14.1 → 24.3 % · 모형 면적 · 균질도 · σ_ion · σ_el · 반복 "triplicates" — 그러나 본문 S 값 = 셀 하나 ± 셋 SD(`[재현]` 셋 평균 178.5 ↔ "198" — D1) · 이온 DC 셀 둘.
- ★★★ **(b) 전하 수송**: 차단 셀 두 종(steel · In/LiIn \| SE) · T형 TLM(73호 회로) + DC · σ_ion,eff 0.254 · 0.199 · 0.153 · 0.165 · σ_el,eff 0.301 · 0.257 · 0.311 · 0.406 mS cm⁻¹(ST4 · AC) · `[도표·벡터]` S14 DC/AC −21.6 … +26.3 % · 본문 전자 "0.38 (±0.15) S" = DC 점 + AC 막대(D2) · κ = 24호 `τ²` · 57 · 73호 규약(`[재현]` 8/8) · ST1 분율 뒤바뀜(52.3/47.7 — D3) · 등가 Bruggeman 2.44–2.73 · 대칭 셀 455–516 ↔ 반쪽 셀 55–62 µm(`[재현]` 가정).
- ★★★ **(c) 미세구조**: 측정 = 공극(방법 재인용 · 시편 미인쇄) · SEM-EDS 표면 사진(본문 "cross-sections" — D14) · 모형 = GeoDict(57호 틀 · 56호 아님 — [9] 인용 자리 D15) · 입력 PSD ≠ 측정(S17b · `[재현]` span 을 µm 표준편차로 — CV 0.21 · 0.11 · 0.046 · fines 0 — D4) · 모양 · 복셀 · 상자 · 청소 크기(3.7 ↔ 7.4 µm)가 조건과 같이 바뀜 · 계면 면적 본문 = S22 의 ×100(D6 · 피복 φ 0.24 · 0.07 · 0.05 · 0.03).
- ★★★ **(d) 성능 · Q1 · Q2 · Q4 · Q6**: C/20 181 · 165 · 159 · 151 · 1C 100 · 84 · 71 · 54(6b) · 50 사이클 N50/N1 0.988 · 0.968 · 0.913 · 0.885 ↔ "No difference … retention"(D7) · `[재현]` 크기 검사 — C/20 옴 강하 2–4 mV · 1C 차 ≤28 mV ↔ Fig. 4b 간격 0.33–0.92 V · 율 되돌림 · 첫 충전 상한 8–17 % · Q1 `θ(N)` 0 · Q2 층 하나 · Q4 0/82 · Q6 50 MPa 한 점.
- ★★ **(e) 25호 귀속 · 교락**: "SE ≈4 µm → 전하 수송 개선"(본문 ref 13) ✅ 이온 방향(×1.54 AC · ×1.78 DC) · ⚠ 전자는 ×0.74(AC)/×1.03(DC) · 조건(50 MPa · 무탄소 · In/LiIn)이 25호(2–30 MPa · VGCF · Li 금속)와 겹치지 않음 · 교락 절반 — 벌크 σ · 측정 · 반복은 가르고 압력 · `θ(N)` · 음극 · 도전재 · 표면 화학 · 이 편 안의 교락은 못 가름.
- ★★ **(f) 잇기 · 인용 대조**: 77호 λ(같은 정의 — 대표값 선택만으로 70 wt% 지도 `θ` ≤0.37 ↔ ≈0.79 · 용량 비와는 수치 대조 안 함) · 73호(같은 방법 · 같은 규약 · 70 : 30 wt% 점 τ² 4.27 ↔ κ_ion 3.57–5.43) · 75호 φ(같은 정의 — 0.03–0.24 ↔ 0.05–0.48) · 68호 방향만 · 인용 대조 아홉 중 여섯 선다(73 · 57 · 77 · 64 · 50 · 01호 규칙) · 셋 부분(SI [1] 공극 방법 위임 · [9] 56호 · [28] 구속).
- **채움표 82호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 둘) · Q2 층 하나(두 차단 셀 × 두 방법) · Q3 층 하나(같은 이름표 아래 셀 · 방법 · 모형) · Q4 0/82 **일흔네 번째 성질**("한 손잡이가 다섯 양을 움직이는데 용량을 σ_ion/σ_el 한 축의 네 점 상관으로 귀속 — 비 > 1 표본 0") · Q5 · Q6 칸 이동 없음 · Q7 해당 없음 · Q8 층 하나(첫 CE 가 SE 입도를 따름).
- **곱 축퇴 처방 예순다섯 번째 적용**: 적용 불가(`CPE_int` 값 미인쇄 · BET 0) · 처방 표 새 줄 없음 · 곱 안 관찰(한 실험 손잡이가 면적 인자와 수송을 함께 움직임).
- ⚠ 어긋남 18 건(D1 본문 S = 셀 하나 · D2 전자 σ 방법 섞음 · D3 ST1 분율 뒤바뀜 · D4 모형 입력 PSD · D5 S15b κ_el 복제 · D6 면적 ×100 · D7 retention · D8 S3 ×6.3 · D9 ST2 · D10 CAM D 값 · D11 1C 세 그림 · D12 "keeps constant" · D13 S14 · D14 단면 ↔ 표면 · D15 [9] · D16 S12 축 이름 · D17 DC 계단 · D18 오기).
- 낱말 지문(본문 | 참고문헌 | SI): `particle size` 65 | 0 | 26 · `void` 10 · `tortuos` 2 | 0 | 3 · `homogene` 7 | 0 | 2 · `contact loss` 1(신품 대칭 셀 "ruled out") · `percolat` 0 · `isolat` 0 | 0 | 1 · `balanced` 5 · `identif` 1(ORCID) · `uniqu` 0 · `uncertain` 1(SE σ) · `MPa` 2 · `BET` · `Sauter` 0 · `LAM` · `LLI` 0 · 합자 119(NFKC 뒤 셈).
- PDF 메타데이터: 본문 `%PDF-1.6` · creator "LaTeX with hyperref package" · producer "Acrobat Distiller 11.0 (Windows); modified using iText 4.2.0 by 1T3XT" · 생성 2023-10-11 +05'30' · 수정 2026-09-27 −07'00' · startxref 1 · %%EOF 1 · 암호화 · 주석 · 첨부 0 · PageLabels 1–9 · XMP 3,576 B(VoR · CC 필드 0) · 다운로드 띠(Hanyang University Library · 27/09/2026) · SI `%PDF-1.4` · pdftk 2.02 + itext-paulo-155 · 생성 = 수정 2023-10-31 · XMP 0 · 표지 1 + A4 18 · 그림 래스터 21(PNG 17 · JPEG 4) + 벡터 1 · sha256 둘 다 호출자 명시값과 일치.
- 보류 결정 (가)–(미): **(그)** 근거(입도 대표값이 `θ₀` 폭의 넷째 원천) · **(저)** 근거(다섯째 표본 — 입도 스윕 판 · 첫 충전 상한 8–17 %) · **(두)** 근거(율 되돌림 연산자) · **(호)** 근거(공극 방법이 73호 SI 로 한 번 더 위임) · **(츠)** 약한 근거(첫 CE 가 미세구조를 따름) · **(주)** 약한 근거(일곱째 표본 — 수송 균형 판) · **(차)** 약한 근거(한 손잡이 두 노브) · **(누)** 약한 근거(같은 규약 κ 넷 — 기록만) · **(너)** 약한 근거(0.785 cm² 둘째 인쇄) · (러)(고)(후)(수)(투)(하) 약 · (허) 중요도 메모 · (느) 형식 참고 · (라)(마)(바)(사)(서) 결정 · 반영 · 해소됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(① SE 입도 값 표기 규약 ② 25호 ref 13 인용 자리 주석 ③ 모형 값 인용 규칙 — 글자는 호출자).
- ⚠ 부수 변경: `figures.json` 에 note 28 · 수동 4 를 더한 뒤 색인 함수 `_write_sources_index`(같은 코드)를 다시 돌려 `raw/figures/_sources.json` 에 이 편 항목(figures 32)을 넣었다 — 다른 편 항목 변화 0(diff 확인).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 82호 행 · 82편 누적 · Evidence 일흔일곱 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-tortuosity-factor-effective-conductivity-split]](열두 번째 표본 · 주장하지 않는 것) · [[composite-cathode-percolation-utilization]](82호 절 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](82호 절 · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](82호 절 · 처방 18 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](예순다섯 번째 적용 · 주장하지 않는 것) · `index.md` 변경 없음(새 페이지 0 · 페이지 수 53). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Schlautmann 행 흡수 표시 · 지목 · 신규 후보 · 재지목 · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h · §6-3-i 44 행)은 호출자 몫.
- 후속(서지 기준, 미열람): **Rana M., Rudel Y., Heuer P., Schlautmann E., Rosenbach C., Ali M.Y., Wiggers H., Bielefeld A., Zeier W.G. 2023 *ACS Energy Lett.* 8, 3196**([11] — 원장 없음 · CAM 쪽 입도 짝) · **Hendriks T.A., Lange M.A., Kiens E.M., Baeumer C., Zeier W.G. 2023 *Batteries Supercaps* 6, 202200544**([7] — 균형 수송 선례) · **Ohno S., … Zeier W.G. 2020 *ACS Energy Lett.* 5, 910**([13] — 10호 [191] 과 지목 2) · **Walther F., … Janek J. 2019 *Chem. Mater.* 31, 3745**([21] — 분해 계면층 배정) · Bradbury R., … Ohno S. 2023 *Adv. Energy Mater.* 13, 2203426([26]) · de Biasi L., … Ehrenberg H. 2019 *Adv. Mater.* 31, 1900985([19]) · Cheng E.J., … Sakamoto J. 2017 *J. Eur. Ceram. Soc.* 37, 3213([31]) · 재지목 Kato 2018 [6](지목 6) · Siroma 2016 [24](4) · Ruess 2020 [20](5) · Koerver 2018 *EES* [29](12).

## [2026-09-29] ingest | assb 83호 — Jiao X., Wang Y., Chen Y., Wang J., Xiong S., Song Z., Xu X., Liu Y. 2023, Insight of electro-chemo-mechanical process inside integrated configuration of composite cathode for solid-state batteries (Energy Storage Mater. 61, 102864)
- raw: `raw/papers/jiao2023_electro-chemo-mechanical-se-modulus-conductivity-intergranular-czm.md` (sha256 봉인 — `pdf_sha256` a8bc11d9…a3ba25c9 · 14,078,265 B · `si_sha256` 177dab2e…72232273 · 6,061,513 B) · 그림 `raw/figures/jiao2023_electro-chemo-mechanical-se-modulus-conductivity-intergranular-czm/` (자동 31 — 본문 7 · SI 23 · 표 1 · 라벨 전부 일치 · 누락 0 · ⚠ SI 잘림 아홉(S1 · S3 · S5 · S10 · S11 · S15 · S17 · S20 · S22 — 그림 틀이 캡션 첫 줄 상자와 ≈11 pt 겹침) · 표 S1 자동 크롭 7/13 행 · 과대 영역 넷(S3 · S8 · S9 · S22) + 수동 10(SI 그림 아홉 · 표 S1 — 300 dpi · 겹친 캡션 텍스트 블록만 지운 렌더) · **연 것 41/41** · `figures.json` note 41 · 본문 그림 7 장 RGB 래스터(1800–1925 px) — Fig. 4 · 5 는 화소 판독
- **3차 묶음 파일 45**(스물다섯째 편; 2차 묶음 "큐 N" 과 별개 — "큐 45" 아님). 원장 "★★ Jiao·Wang·Chen·…·Liu 2023 · 지목 25 · Q1 · DEM 연결성·굴곡도 후처리의 방법 원전 — DEM 브랜치에 직결" · 25호 digest 후속 ★★★(SI ref 3 — 등급 둘이 다름, 기록만) · Xi'an Jiaotong(State Key Lab for Mechanical Behavior of Materials) + Chalmers · © Elsevier(오픈액세스 아님) · SI 17 쪽(2026-09-28 Word 에서 내보낸 저자 문서 · 그림 S1–S23 · 표 S1 · SI 참고문헌 0 · pp. 2–3 노란 형광).
- ★★★ **(a) 무엇을 모형화했나**: 서로 입출력이 없는 모형 둘 — (i) 3D 복합 양극 한 번 방전(COMSOL 5.5 + MATLAB 2020b · 75 × 75 µm² · SE 30 µm · 양극 75 µm · 구형 NCM · 배치 · 입도 · 분율 생성법 인쇄 0 · `[도표·화소]` y = 37.5 µm 단면 NCM 면적 분율 0.183–0.188 · 원 29 · 지름 2.8–9.7 µm · 겹침 0 · 이원 농축 용액 SE 수송 · BV · ϕ_mech · 선형 탄성) (ii) 2D 이차 입자(∅10 µm · coarse ≈12–14 · fine ≈35–40 1차 입자) 입계 CZM(Xu–Needleman · 사이클 축 · 3 % 등방 부피 변화 · 손상 > 80 % → σ_ion 0). 스윕: E 0.1–100 GPa(9) · σ 5×10⁻⁶–5×10⁻²(12 — 이름표 넷 · 여덟 미인쇄) · CZM 2 × 2 — 서로의 고정값 미인쇄 · 조합 run 0.
- ★★★ **(b) 입력 출처**: 표 S1 13 행 출처 0/13 · 본문이 표 S1 을 한 번도 부르지 않음 · D_SE · t_Li+ · k_r · α · β · OCV · tr(ζ) · 전류 · 역학 경계 · CZM 전부 등 ≈30 미인쇄 · `[재현]` G = E/2(1+ν) 79.6 ↔ 78 ± 1 ✅ · c_max 49.3–49.8 mol L⁻¹ ↔ Fig. 3 눈금 50 ✅ · NCM D ↔ σ Nernst–Einstein ×3.1×10⁵ ❌ · 본문 "1.2% to 5.1% of NCM cathode particle" = 69호 **격자** 두 값(인용 0 · 이름표 '입자') ↔ SI 입력 3 % · 3호 입력 7.8 %(×2.6) · SE 밀도 1.0 · 초기 ≈1 mol L⁻¹(`[도표]` — 폴리머형 이원 전해질).
- ★★★ **(c) 출력 층위**: 전부 모형 출력(측정 0) · 3D 는 CAM\|SE 불파괴 가정(SI (5)) → `θ ≡ 1` 구성상 · 2D 의 "loss of contact" 는 1차 입자 사이 · 파괴 사이클 `[인쇄]` 1409 · 1545 · `[도표]` 95 · 132 · 총 균열 0.61 · 2.74 · 0.75 · 2.87(본문 ×10³ ↔ 그림 ×10⁴ — D3) · 용량 사상 0 — 카드 `θ(N)` 아님.
- ★★★ **(d) 25호 귀속 ⚠ 불성립**: `DEM` 0 · `tortuos` 0 · `percolat` 0 · `path` 0 · `connect` 본문 0(SI 1 = CAM\|SE "connection … perfect") · 연결성 양 자체가 모형에 없음 · 25호 SI 원문 대조 전(25호 PDF 미보유 · 25호 digest 도 SI 문장 미전사) · DEM 은 기록만(다른 브랜치 · 읽지 않음).
- ★★★ **(e) 결론 셋이 구조의 귀결**: "E 는 전기화학에 영향 없음" = 가정 (5) · 유일한 결합 ϕ_mech(`[재현]` 0.63–1.07 mV/100 MPa) · 역학 없는 1D EIS · DoD 100 % NCM von Mises ≈6.2 GPa 가 E 0.1–50 GPa 에서 같음(`[재현]` 고립 구 Eshelby E ≤4 GPa · ≤0.1 GPa — 미인쇄 경계가 정함) · "σ 5×10⁻⁴ 문턱" = 전류 미인쇄(`[재현]` 옴 강하 RT/F 전류 1.3–1.7 mA cm⁻² ≈ 이 형상 1C ≈1.8 · 가정) · "coarse 가 파괴를 늦춘다" ↔ 자기 수명 fine > coarse(×1.10 · ×1.39 — D1) · 모의 EIS "Rct" ×5.1 · Rs ×14(`[도표·화소]` — 계면 고정 · 수송 손잡이) · SE 고갈 0 ↔ 같은 DoD NCM 균일 리튬화(D7 · `[재현]` SE 재고 비 0.093 · 황화물 Li 41.8 mol L⁻¹).
- ★★ **(f) 잇기**: 물리 3호(SE E 스윕 — 수치 대조 안 함) · 도구 56호(COMSOL + MATLAB) · CZM 58호의 반대 계면(58 = CAM\|SE 한 방전 · 83 = 입계 사이클 — "CAM\|SE × N 축" 칸 비어 있음) · [26] = 57호 인용 자리 ⚠(57호 역학 0 — D11) · [25] = 4호 ✅ 방향 · [23] = 63호 · [13] = 원장 ★★★★ Barai 2021(공소결 예시로만) · 69호 부피 변화 · 82호 "입력 ≠ 측정" 둘째 표본(입력 자체 부재).
- **채움표 83호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다 · Q2 없다(층 하나 — 모의 "Rct" 가 수송 손잡이로) · Q3 층 하나(입력 층위가 지면에 없다) · Q4 0/83 **일흔다섯 번째 성질**("두 손잡이를 고정값 없이 따로 흔들고 조합을 지침으로 — 결론 셋이 가정 · 전류 미인쇄 · 기준 선택의 귀결") · Q5 해당 없음 · Q6 없다(층 하나) · Q7 해당 없음 · Q8 층 하나.
- **곱 축퇴 처방 예순여섯 번째 적용**: 적용 불가(측정 0 · 면적 · `j₀` 고정) · 처방 표 새 줄 없음 · 곱 안 관찰(모형판 — 수송 손잡이가 "Rct" 판독을 ×5.1).
- ⚠ 어긋남 16 건(D1 초록 ↔ 수명 순위 · D2 가정 (5) 비공개 · D3 총 균열 단위 · D4 Fig. 6 Case 4 사이클 = Case 2 · D5 SE 30 ↔ 50 µm(EIS 는 1D 다른 모형) · D6 식 (1) 1/F² · D7 SE 고갈 ↔ NCM 리튬화 · D8 부피 변화 1.2–5.1 ↔ 3 % · D9 S12 "slightly" ×2.2 · D10 S20 · S23 행 형상 뒤바뀜 · D11 [26] = 57호 · D12 DoD 정의 · D13 S21 · S22 비단조 · D14 S6 인용 행 · D15 Li 20 µm 영역 없음 · D16 오기).
- 낱말 지문(본문 | 참고문헌 | SI): `DEM` 0 · `tortuos` 0 · `percolat` 0 · `connect` 0 | 0 | 1 · `contact` 4(셋 입계) · `delamin` · `debond` 0 · `crack` 14 · `cycl` 34 | 0 | 9 · `pressure` · `MPa` 0 · `current density` 1(정의) · `C-rate` 0 · `identif` · `uniqu` · `sensitiv` · `uncertain` · `valid` 0 · `experiment` 0 | 0 | 1 · `impendence` 2 · `LAM` · `LLI` · `OCV` 0.
- PDF 메타데이터: 본문 `%PDF-1.7` · creator "Elsevier" · producer "Acrobat Distiller 8.1.0 (Windows)" · 생성 2023-08-16 17:44:49Z · 수정 2023-08-17 · 선형화 · startxref 2 · %%EOF 2 · 암호화 · 주석 · 첨부 0 · PageLabels 1–9 · XMP 5,567 B(VoR · coverDate 2023-08-01 · pdfx:robots noindex) · 글꼴 15 · 다운로드 띠 0 · SI `%PDF-1.7` · creator = producer "Microsoft® Word LTSC" · 생성 = 수정 2026-09-28 15:11:04 +09'00' · XMP 3,059 B · A4 17 쪽 · 글꼴 5(DengXian 포함) · 그림 래스터 23 · sha256 둘 다 호출자 명시값과 일치.
- 보류 결정 (가)–(이): **(이)** 근거(강 — 둘째 표본 · 입력이 지면에 없다) · **(노)** 근거(격자 값이 '입자' 이름표로 인용 없이) · **(주)** 근거(여덟째 표본 — 모형 문턱 · 전류 0) · **(차)** 약한 근거(수송 손잡이가 "Rct" 판독) · (러)(투)(그)(두)(하)(무) 약 · (느)(시) 형식 참고 · (누)(고) 기록만 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(25호 SI ref 3 인용 자리 주석 · 모형 결론 옆 배제 가정 표기 · R8 에 피로 CZM 형 N 축 메모).
- ⚠ 부수 변경: `figures.json` 에 note 31 · 수동 10 을 더한 뒤 색인 함수 `_write_sources_index`(같은 코드 · `python3 -B`)를 다시 돌려 `raw/figures/_sources.json` 의 이 편 항목을 figures 41 로 맞췄다 — 다른 편 항목 변화 0(diff 확인).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 83호 행 · 83편 누적 · Evidence 일흔여덟 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](83호 절 · 처방 19 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](예순여섯 번째 적용 · 주장하지 않는 것) · [[assb-synthetic-truth-contact-loss-requirements]](83호 표본 — "자리 없음" 참고 행 · R1 · R8 근거 열) · [[composite-cathode-percolation-utilization]](83호 절 · 주장하지 않는 것) · [[assb-tortuosity-factor-effective-conductivity-split]](83호 주석 · 주장하지 않는 것) · `index.md` 변경 없음(새 페이지 0 · 페이지 수 53). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Jiao 행 흡수 표시 · 귀속 정정 · 재지목 · 신규 후보 · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h · §6-3-i 45 행)은 호출자 몫.
- 후속(서지 기준, 미열람): **Roe K.L., Siegmund T. 2003 *Eng. Fract. Mech.* 70, 209**([36] — 비가역 CZM · 원장 없음) · **Bai Y., Zhao K., Liu Y., Stein P., Xu B.-X. 2020 *Scr. Mater.* 183, 45**([19] — 입계 CZM · 58호와 같은 연구망) · **Bistri D., Di Leo C.V. 2021 *J. Electrochem. Soc.* 168, 030515**([27] — CAM\|SE 접촉 역학) · Xiong S., … Liu Y. 2023 *Adv. Energy Mater.* 13, 2203614([33] — 같은 연구실) · Kim U.-H., … Sun Y.-K. 2020 *Nat. Energy* 5, 860([37] — 형상 출처) · Xu R., … Zhao K. 2019 *J. Mech. Phys. Solids* 129, 160([20]) · 재지목 **Barai … Srinivasan 2021 *Chem. Mater.* 33, 5527**([13] — 53 · 75 + 83 = 3) · Sultanova & Figiel 2021 *Comput. Mater. Sci.* 186, 109990([24] — 58 + 83 = 2).

## [2026-09-29] ingest | assb 84호 — Orue Mendizabal A., Cheddadi M., Tron A., Beutl A., López-Aranguren P. 2023, Understanding Interfaces at the Positive and Negative Electrodes on Sulfide-Based Solid-State Batteries (ACS Appl. Energy Mater. 6, 11030)
- raw: `raw/papers/oruemendizabal2023_multiconfiguration-geis-drt-nmc622-lpscl-li-interfaces.md` (sha256 봉인 — `pdf_sha256` badf7cbd…d12f9fde · 10,215,732 B · `si_sha256` 9be84536…f1a87882 · 587,617 B) · 그림 `raw/figures/oruemendizabal2023_multiconfiguration-geis-drt-nmc622-lpscl-li-interfaces/` (자동 13 — 본문 6 · SI 그림 4 · SI 표 3 · 라벨 전부 일치 · 누락 0 · ⚠ caption 필드 본문 섞임 다섯(f1 · f2 · f3 · f4 · f6 — 2단 조판에서 캡션 뒤 본문이 붙음 · 이미지 온전) · 과대 영역 셋(fig_S1 SI 목차 머리 · tab_S1 내려받기 띠 · tab_S3 SI 참고문헌) · 표 S2 각주 아래 절반 잘림 · 초록 그래픽 누락 + 수동 2(초록 그래픽 p. 1 · 표 S2 SI p. 8 — 300 dpi) · **연 것 15/15** · `figures.json` note 15 · 본문 그림 여섯은 PDF 안 원본 래스터(1423–2100 px) — 그림 1c · 2c · 3a · 4b · 4c · 4d · 5c · 5e · 6 · S3 는 화소 판독)
- **3차 묶음 파일 46**(스물여섯째 편; 2차 묶음 "큐 N" 과 별개 — "큐 46" 아님). 25호 digest 후속 ★★(ref 23 — "황화물 셀 양·음극 계면 EIS 배정 — `R_SSE/anode` ↔ `R_SSE/NCM` 배정의 근거") · 원장 "★★ 지목 25 · Q2·Q5 · 양극·음극 계면 EIS 배정의 근거 — 17호 함정 판정" · 원장 §3-b (차) 근거 칸 첫머리 · CIC energiGUNE(BRTA) + AIT · CC BY-NC-ND 4.0 · SI 10 쪽(Aspose.PDF 로 만든 문서 · 그림 S1–S4 · 표 S1–S3 · 식 S1–S2 · SI 참고문헌 4 — (2) Singh 2022 는 본문 참고문헌에 없음 · 본문이 부르는 SI 항목 전부 있음).
- ★★★ **(a) 셀 구성**: "multiconfigurational" = 네 구성 · 전부 2전극 — Li\|SE\|Li · Li\|SE\|In(음극 계면 셀 둘) + NMC622\|SE\|Li · NMC622\|SE\|In(완전지 둘) · 기준극 · 차단 셀 · 양극 대칭 셀 0 · EIS 는 셀 1–3(셀 4 는 용량 곡선뿐) · LPSCl : NMC622(코팅 언급 0) : C65 = 28.2 : 67.4 : 4.4 wt%(인쇄 순서 — NMC622 67.4 wt%) · 복합체 4 mg · SE 30–35 mg(∅6 mm · ≈700 µm) · 성형 100–150 → 300 · 450 · 600 MPa · **운전 압력 · 구속 형식 · 온도 · 셀 수 미인쇄** · `[재현]` 168 mAh g⁻¹ 기준 · C/20 = 0.08 mA cm⁻² · 펠릿 밀도 = 82호 ρ 의 81–95 %.
- ★★★ **(b) EIS → DRT**: GEIS(C/20 전류 인가 중) 1 MHz–0.1 Hz · 20–50 mV · Lin-KK "within the limit of 1%"(잔차 그림 0) · DRTtools(Tikhonov) — λ · 이산화 · 도함수 차수 · τ 격자 · γ 정규화 미인쇄(체크리스트 C1 ❌ · C2 ✅ 명명 · C3–C5 ❌) · 배정 연산자 넷(구성 차 · 전류 방향 · SOC · 문헌 `C` 대역) · 온도 0 · `[도표·화소]` R3\* ≈3.8 · R4\* ≈9.5 s 는 측정 창(τ_max 1.6 s — 저자 규약 f = 1/(2πτ)) 밖 · 표 S3 는 둘을 "0.1 – 0.2 Hz" 로 · 같은 이름표의 τ 띠가 그림마다 1–2 자릿수 이동 · 드리프트 조건 ">3.5 V" 뿐(SCL 배정은 <3.5 V) · `[재현]` AC 전류 = DC ×0.9–5 · γ 정규화가 그림 2e ↔ 5c 에서 한 해석으로 함께 맞지 않음.
- ★★★ **(c) 25호 귀속 ⚠ 불성립**: `[인쇄]` "The signals for both cells are within the same relaxation time for the (RQ)1, (RQ)2, and (RQ)3 processes" · "The EC model may not be accurate enough in the case of a large overlap … as is the case for R2 and R3 for the full cell" · 양극 몫 = 대칭 셀 R3(불변) 빼기 · 자기 셀 결론 "the aging of the full cell should originate exclusively from the CAM/SE interface"(25호 이름표와 반대 방향 · 이 편 Li 계면 하나 ≈25–31 ↔ 양극 R3 134–177 Ω·cm²) · 자기 `C` 기준이 R2 배정을 ×54–1000 으로 기각 · 이식 가정 넷(같은 계면 상태 · 한 ↔ 두 계면 · 압력 · 온도) 미검사 · 25호 본문 ref 23 문장 대조 전(G1). **17호 함정**: 받치지도 뒤집지도 않고 흔든다 — 용량 축 상대극 교체 대조(`[도표·화소]` 126.2 → 110.9 ↔ 122.7 → 107.8 mAh g⁻¹ · 둘 다 −12.1 % · 셀 하나씩) · 저항 축 25호 "≈80 % Li" 는 인용 근거가 분리를 인쇄하지 않은 회로 이름표 위 · 84호 "exclusively 양극" 도 역방향 함정(음극 몫을 대칭 기준선으로 작게) 미배제.
- ★★★ **(d) 사이클 · 열화**: `θ(N)` 0/84 · 완전지 R3 `[도표·화소]` 34.5 → 174.6 Ω·cm²(×5.1 · 상태 미인쇄 — 저자 배정 "interaction products … and morphological changes" 병치) · Li\|Li 27 사이클 R2 전류 방향 진동 · DC ≈ EIS · 단락 ≈1370 h · Li\|In 탈리튬 끝 급등(사전 합금 0.16 mAh cm⁻²) · **곱 1단계(표 S2 C3 × 그림 4b R3)가 이름표 해석으로 화학형(τ ×1.94) ↔ 면적형(τ ×0.85) 뒤집힘** · SEM 정성 · `[재현]` IR 예산 창 안 중간 SOC 저항 ≲15 %(용량 −15.3 mAh g⁻¹ ↔ +12.6 mV · dQ/dV 봉우리 +52 ↔ +7.7 mV).
- ★★ **(e) (차) 근거(중)**: Li\|SE 에서 면적(void) = R2 · R0 ↔ 전하이동 = R3 불변(`[인쇄]` "the charge-transfer processes are essentially not affected by the Li/SE contact area" — 대칭 R3 불변 + 떼어 낸 박 사진 한 장) · 양극은 한 R3 에 CEI + 형태 변화 병치 · forward 면적 노브의 EIS 서명 선택지(`R_ct` 배율 ↔ 별도 구속 호 — Eckhardt [48,49]).
- ★★ **(f) 잇기**: Li 쪽 순서(접촉 · SEI 중주파 → CT 저주파) = 21호(3전극)와 같은 방향 · 양극 CT 계보 30 Hz(16호) · ≈150–300 Hz(64호) · ≈500 Hz(11호) · ≈1 kHz(18 · 63호) ↔ 84호 Li void 대역(≈10³ Hz) 겹침 → 2전극 주파수 대역만의 전극 배정 불가 · 46호([39])와 같은 두 호(`C` ≈10⁻⁷ · ≈10⁻⁴–10⁻³)에 다른 이름(표 S1 행 3 "chemical capacity" ↔ 이 편 "charge transfer") · 5호 5 MPa 쪽과 같은 크기(압력 미인쇄 — 추정에 안 씀) · 11호([32] DRTtools)와 같은 도구 · 빼기 논리 · 25호 조건 겹침 0 · 42호([54]) 0.62 V · 23호([23]) CEI 인용 · 73호 TLM 혼합 가능성(`[해석]`).
- **채움표 84호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 셋) · Q2 층 하나(구성 교체) · Q3 층 하나(적합 · 역변환 라벨의 상태 이름표 교차) · Q4 0/84 **일흔여섯 번째 성질**("여러 구성의 차로 전극 몫을 정하면서 이식 가정은 검사하지 않고, 자기 `C` 기준이 R2 배정을 ×54–1000 으로 기각하는데 R 비 · DRT τ 로 배정을 유지") · Q5 층 하나(**서른두 번째 형태** "기준극 대신 구성 교체") · Q6 없다(층 하나) · Q7 해당 없음 · Q8 층 하나.
- **곱 축퇴 처방 예순일곱 번째 적용**: 부분 적용 — 1단계 입력 있음(세 상태 × `R` · `C` × 대칭 ↔ 완전지) · 판정은 이름표 모순으로 화학형 ↔ 면적형 · 3단계-b 양극 ✅ · Li `C3` 이중층의 ×100 · 4단계 대칭 ✅ · 완전지 창 밖 몫 ≈85 % · 처방 표 후보 줄 "상태 이름표 대조" · 곱 안 관찰(면적 손실이 전하이동 호 밖으로).
- ⚠ 어긋남 17 건(D1 그림 4b 줄 ↔ 2c · 4c · 6 · S3 · D2 상태 이름표 둘 · D3 자기 `C` 기준 기각 · D4 창 밖 봉우리 · D5 S3 "300 Hz" · "900 Hz" · D6 표 S3 · D7 그림 6 R3 · R2 없음 · D8 "20 → 50 %" · D9 Li\|In "3 orders" · 8th · D10 Spencer-Jolly "no EIS" · D11 표 S1 Singh 0.03 F · D12 C1 · C3 이름 · D13 DRT 오프셋 · 정규화 · D14 S1 범례 · D15 In 셀 환산 · D16 인용 자리 ↔ 제목 · D17 오기).
- 낱말 지문(본문 | 참고문헌 | SI): `reference electrode` 0 · `three-electrode` 0/1(인용 셀) · `identif` 3(과정 식별) · `uniq` 0 · `uncertain` · `error` 1(수치 0) · `λ`/`lambda` 0 · `regulariz` · `Tikhonov` · `DRTtools` 1 · `DRT` 27 | 0 | 1 · `GEIS` 10 | 0 | 5 · `contact` 25 · `void` 13 · `delamin` 4 · `crack` 4 · `constriction` 1 · `MPa` 3(전부 성형) · `pressure` 3 · `temperature` 2 · `°C` 0 · `n =` 0 · `LAM` · `LLI` · `TLM` 0.
- PDF 메타데이터: 본문 `%PDF-1.4` · title "ae3c01894 1..13"(조판 작업명) · creator "Arbortext Publishing Engine" · producer "PDFlib+PDI 9.1.2p4 (C++/Win64); modified using iTextSharp.LGPLv2.Core 3.7.4.0" · 생성 2023-11-03 · 수정 2026-09-28(내려받기 띠 삽입) · XMP 3,867 B(VoR · dc:rights CC BY-NC-ND 4.0) · 글꼴 22 · 그림 래스터 PNG · SI `%PDF-1.5` · creator "Aspose Ltd." · producer "Aspose.PDF for Java 19.3; modified using iTextSharp.LGPLv2.Core 3.7.4.0" · 생성 2023-10-11(본문 수정본 전날) · 수정 2026-09-28 · XMP 234 B(빈 기술) · 글꼴 13(Gungsuh 포함 — 쓰인 자리 미확인) · 그림 JPEG 넷 · sha256 둘 다 호출자 명시값과 일치.
- 보류 결정 (가)–(키): **(차)** 근거(중) · **(주)** 근거(아홉째 표본) · **(이)** 근거(적합판 — 셋째 표본) · **(치)** 근거(배정 가정판) · **(루)** 근거(ASSB 신품 SOC 표본 ×10–80) · (무)(오)(노)(두)(러)(하)(비)(초)(츠) 약 · (처) 정성 메모 · (사) 표본 · (느)(시)(지) 형식 참고 · (저) 근거 0 · (라)(마)(바) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(25호 ref 23 인용 자리 주석 + 17호 함정 문구 · DRT 창 밖 봉우리 표기 · 구성 교체형 전극 몫 배정 표기 — 글자는 호출자).
- ⚠ 부수 변경: `figures.json` 에 note 15 · 수동 2 를 더한 뒤 색인 함수 `_write_sources_index`(같은 코드 · `python3 -B`)를 다시 돌려 `raw/figures/_sources.json` 에 이 편 항목(figures 15)을 더했다 — 다른 편 항목 변화 0(diff 확인).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 84호 행 · 84편 누적 · Evidence 일흔아홉 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](예순일곱 번째 적용 · 17호 함정 대조 · 처방 표 후보 줄 "상태 이름표 대조" · 주장하지 않는 것 — 25호 절 본문은 손대지 않음) · [[drt-peak-count-nonidentifiability]](84호 체크리스트 · 여섯 번째 경보 · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](서른두 번째 형태 · 주장하지 않는 것) · [[assb-interphase-vs-contact-loss-attribution]](계보 84호 행 · → 84호 · 처방 9 · 편 수 · 주장하지 않는 것) · `index.md` 변경 없음(새 페이지 0 · 페이지 수 53). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Orue 행 흡수 표시 · 귀속 정정 · 신규 후보 · 재지목 · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h · §6-3-i 46 행)은 호출자 몫.
- 후속(서지 기준, 미열람): **Eckhardt J.K., Fuchs T., Burkhardt S., Klar P.J., Janek J., Heiliger C. 2022 *ACS AMI* 14, 42757**([49] — 2 + 84 = 2 · 3D 구속 · 원장 없음) · **Eckhardt J.K., Klar P.J., Janek J., Heiliger C. 2022 *ACS AMI* 14, 35545**([48]) · **Spencer-Jolly D., … Bruce P.G. 2021 *ACS AMI* 13, 22708**([30] — Li void · 3전극) · **Clematis D., … Barbucci A. 2021 *Electrochim. Acta* 391, 138916**([33] — DRT) · **Hahn M., Schindler S., Triebs L.-C., Danzer M.A. 2019 *Batteries* 5, 43**([35] — DRT 파라미터) · **Wang Z., … Huang J. 2023 *eScience* 3, 100087**([55] — 17 + 84 = 2) · Haruyama J., … Tateyama Y. 2014 *Chem. Mater.* 26, 4248([61] — 50 + 84 = 2) · Wang L., … Chen L. 2020 *Nat. Commun.* 11, 5889([62]) · Wan T.H., Saccoccio M., Chen C., Ciucci F. 2015 *Electrochim. Acta* 184, 483([32] — 11 + 84 = 2) · Narayanan S., … Pasta M. 2022 *Nat. Commun.* 13, 7237([31]) · Charbonneau V., Lasia A., Brisard G. 2020 *J. Electroanal. Chem.* 875, 113944([67]).
- 정오 (호출자 통합 때 · 2026-09-29): 위 (a) 줄의 조성비는 처음에 재료 이름이 NMC622 · LPSCl · C65 순으로 적혀 NMC622 = 28.2 wt% 로 읽혔다 — 인쇄는 "LPSCl:NMC622:C65 = 28.2:67.4:4.4"(NMC622 67.4 wt%) 라 고쳤다. 봉인 digest :58 (a') 행도 같은 나열 순서라 같은 오독이 가능하다(digest :267 은 인쇄 순서 그대로) — raw 불변이라 여기와 카드 Status Log 에 적는다.

## [2026-09-29] ingest | assb 85호 — Wang Y., Li X. 2024, Fast Kinetics Design for Solid-State Battery Device (Adv. Mater. 36, 2309306)
- raw: `raw/papers/wang2024_fast-kinetics-hierarchical-catholyte-anode-design-ssb.md` (sha256 봉인 — `pdf_sha256` f9d7520e…c3dc3c62 · 6,600,147 B · `si_sha256` 2bc92765…3ebb27c9f · 1,171,596 B) · 그림 `raw/figures/wang2024_fast-kinetics-hierarchical-catholyte-anode-design-ssb/` (자동 12 — 본문 4 · SI 그림 6 · SI 표 2 · 라벨 전부 일치 · ⚠ 그림 S5 는 벡터라 추출기가 제외 · 표 S2 는 캡션 미인식(표 S1 크롭이 쪽 전체를 덮어 S2 까지 포함 — 과대 영역) · S2 · S3 · S6 · S7 크롭 아래 축 라벨 절반 잘림(판독 영향 0) + 수동 2(그림 S5 SI p. 6 · 표 S2 SI p. 3 — 300 dpi) · **연 것 14/14** + 확대 판독 둘(S1(b) 55 °C 점 · 2g R1 절편) · `figures.json` note 14 · 본문 p. 1 그래픽 0(로고 둘) · 본문 그림은 PDF 안 래스터)
- **3차 묶음 파일 47**(스물일곱째 편; 2차 묶음 "큐 N" 과 별개 — "큐 47" 아님). 25호 digest 후속 ★★(ref 16 — "계층형 SE(작은+큰) → 낮은 굴곡도 — 25호 '굴곡도' 주장의 선행" · :104 본문 전사 있음) · 원장 "★ 지목 25 · Q1 · 계층형 SE → 낮은 굴곡도 주장의 선행"(원장 ★ ↔ 25호 ★★) · Harvard SEAS(Wang · Li) · © Wiley-VCH(CC 문장 0) · Editor's Choice · SI 9 쪽(pdftk 로 Wiley 표지 + 저자 PDF · 그림 S1–S7 · 표 S1–S3 · SI 참고문헌 5 — 본문이 부르는 SI 항목 전부 있음 · 표 S2 는 SI 안에서만).
- ★★★ **(a) 구조**: 단결정 NMC83(1–5 µm · 조성 두 판 D4) 70 : LPSCl1.5 30 wt% + PTFE 3(추가) · 무탄소 · 18 mg cm⁻²(2.7 mAh cm⁻² · 150 mAh g⁻¹ 기준) · SE 세 판 — large(합성 그대로 ≈20 µm) · small(볼밀 ≈300 nm–4 µm) · mixed(`[인쇄]` 실험 절 "20 wt% small · 10 wt% large" ↔ **그림 1b "Large 20wt% · Small 10wt%" 반대 — D3**) · 음극 Si–G\|Li(47.6:47.6:4.8 wt% · Li 박 15 µm) ↔ Si–Cl\|G\|Li(Si:LPSCly:PTFE 76.2:19:4.8) · 분리막 LPSCl1.5\|LPSCl-I\|LPSCl1.5(20 + 100 mg · 면적 · 두께 미인쇄) · 400 → 50 MPa · RT 22–30 °C 무통제 · 비교군이 다른 음극 위(율 = Si–G · EIS = Si–Cl — D17) · 셀 하나씩.
- ★★★ **(b) 굴곡도 · 수송**: `tortuos` 9 · 값 · 측정 · 모형 · σ_eff · 두께 · 면적 **0** — 근거 = EIS 두 호 순서(`[인쇄]` "R2 … conduction in the catholyte network; R3 … interface contact") + 그림 1c 모식 · `[도표]` **R1(저자 정의 "connected electrolyte network") small-only 68 ↔ large 37 ↔ mixed 27 Ω** — R2 차와 같은 크기인데 본문 미논의 · 82호식 옴 강하 검사는 면적 없어 비만(총 EIS 중 R1+R2 몫 41 · 78 · 52 · 51 %) · `[재현]` 5 C 분극 A·R_dc ≈22 Ω·cm² → 면적 함축 0.26–0.39 cm²(확정 아님).
- ★★★ **`[재현]` Ea**: 인쇄 Ea 8 중 7 = `k_B · d log₁₀(T/R)/d(1/T)`(ln 10 누락 · ±1 meV — 정의식대로면 ×2.303 = 0.45–0.62 eV) · mixed/Si–Cl R3 **284** 는 표 S1 R3 계열로 255 이고 55 °C 점을 표 S1 의 **R2 값 3.276 Ω** 으로 두면 284.1 — 그림 S1(b) 확대 `[도표]` 55 °C 점 2.00(R3 이면 1.77) · 본문 "37 · 86 · 42 meV" → **7 · 57 · 13 meV**(4 ↔ 3 점 적합 폭 ≤27) → "resistivity ↑ · area ↑↑" 분해의 정량 근거 불성립(D1 · D2) · 같은 앞인자 가정 미인쇄.
- ★★ **(c) 급속 · 수명**: C-rate = 150 mAh g⁻¹ × 적재 삼각 검사 전부 ✅(5 C 13.5 · 4 C 10.8 · 15 C 40.5 · 23 mg × 4 C 13.8 "14" · 27 × 3 C 12.15 "12") — 초록 "5–10 C ↔ 13–40 mA cm⁻²" 만 ❌(40.5 = 15 C · D6) · 그림 1a 캡션 "Critical" ↔ 축 "Charge"(D7) · 셋 셀 4275 · 2504 · 4200 사이클 유지율 `[도표]` −20 … −26 %(수치 0) · 창 2.0–4.4/4.5 V(율별 컷오프 4.1 → 4.35) · 임계 C-rate ↔ V_end 2전극 상관(표 S3 26 점 · 셀 하나씩) · "깼다" = 추세선(−17 C V⁻¹) 위 두 점(+3.7 · +2.6 C ↔ 도핑 산포 3 C) · S4 예시 셀 분리막 LGPS(D18) · 4g 세 손잡이 절제(촉매전해질 · 음극 · 중앙층 — 셀 하나씩) · 캡션 "pouch 10 MPa · 75 µm" 패널 없음(D5).
- ★★★ **(e) 25호 귀속**: :104 전사 ✅ 정확(입도 두 무리 · "low tortuosity" 낱말 그대로) · :585 "선행" ✅ 주장의 선행 · ❌ 측정의 선행 — 원전에 굴곡도 양 0 · 25호 기하 τ(DEM 1.21 ↔ 1.84)와 정의 공유 0 · 25호 :481 자기 판정과 같은 자리 → **계보 두 편 연속 측정 없는 명제**.
- ★★ **(f) 잇기**: 82호와 방향만(작은 SE → 계면 호 ↓ · 수송 ↑ — 82호는 σ_eff 측정 · 이 편은 회로 이름표) · 77호 λ = D_CAM/D_SE 로 large 판 0.05–0.25(지도 밖 · CAM 이 SE 보다 작은 반대 기하) · 73 · 75 · 68호 수치 대조 0(정의 없음 · S3a 전자 퍼콜 문턱은 68호 정성 표본 — LPSCl1.5 40 wt% 퍼콜 · LGPS 40 비퍼콜) · 76호 방향 규칙과 그림 1d 서술 같은 방향(관찰 0) · 60 · 17호 대조 0.
- **채움표 85호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 넷 — 사이클 용량 시계열 · 신품 R3 이름표 · C3 면적 대리 · 0.3 C 용량 입도 무관 ≤10 %) · Q2 층 하나(신품 구성 교체 EIS) · Q3 층 하나(적합 산술 미재현) · Q4 0/85 **일흔일곱 번째 성질**("곱 R = ρl/A 를 온도 기울기로 ρ 쪽에 배정하고 나머지를 A 에 돌리면서 A 의 독립 측정 0 · 같은 앞인자 가정 미인쇄 · Ea 차 37 meV 가 인쇄 표로 7 meV") · Q5 해당 없음(층 하나 — 2전극 V_end) · Q6 보고(50 MPa 한 점) · Q7 해당 없음(층 하나 — Li 재고 ×1.14 외부 밀도) · Q8 층 하나.
- **곱 축퇴 처방 예순여덟 번째 적용**: 부분 — 1단계 입력(R3 · C3 × 4 구성 × 4 온도 · 신품 · 구성 축) · `[재현]` τ3 = R3·C3 mixed/large ×2.2(25 °C) · small/large ×2.4 → 순수 면적형 아님(ρε ↑ — 저자 방향을 Ea 없이) · 동어반복(R · C 둘로 A · ρ 둘) · 3단계-b 면적 없어 불가 · 처방 표 후보 줄 "온도 기울기 ↔ R·C 곱 교차".
- ⚠ 어긋남 19 건(D1 Ea ln 10 · D2 55 °C 점 · D3 혼합비 반전 · D4 NMC 조성 두 판 · D5 파우치 캡션 · D6 초록 C-rate · D7 1a 캡션 ↔ 축 · D8 표 S2 ω 열 32 칸 중 8 만 Hz · D9 NP 1.6 · D10 S4 시작 율 · D11 3.15/3.16 · D12 b 0.77/0.755 · D13 CV 문단 LPSCl1.5/1.0 · D14 CPE-P > 1 · D15 R2 배정 본문 ↔ SI · D16 Si–Cl 8 µm ↔ 치밀 하한 13.5(외부 밀도) · D17 비교군 음극 · D18 S4 LGPS · D19 [6] 연도 미인쇄).
- 낱말 지문(본문 | 참고문헌 | SI · 약어 대소문자 구분): `tortuos` 9 · `percolat` 5 · `contact` 7 · `resistivity` 5 · `identif` 1(ORCID) · `uniqu` 1 · `sensitiv` · `uncertain` 0 · `error` 0 | 0 | 1 · `n =` 0 · `MPa` 3 · `pressure` 2 · `°C` 12 · `thickness` 7(분리막 · 음극) · `area` 14(셀 면적 0) · `D50` 0 · `LAM` · `LLI` · `TLM` · `OCV` · `SEI` · `CEI` · `reference electrode` 0 · `critical C-rate` 13 | 0 | 5 · `R1` 1 · `R2` 8 · `R3` 9 · `Arrhenius` · `ln` · `log` 0.
- PDF 메타데이터: 본문 `%PDF-1.6` · title "Fast Kinetics Design for Solid‐State Battery Device" · subject "Advanced Materials 2024.36:2309306" · creator "LaTeX with hyperref package" · producer "Acrobat Distiller 23.0 (Windows); modified using iText 4.2.0 by 1T3XT" · 생성 2024-03-15 · 수정 2026-09-27(내려받기 띠 Hanyang University Library) · XMP 3,576 B(doi · crossmark 2024-01-17 · jav VoR) · 글꼴 13 · 이미지 14 · SI `%PDF-1.7` · creator "pdftk 2.02" · producer "itext-paulo-155" · 생성 = 수정 2024-04-09 · **XMP 없음**(xref 0 — 앞 시도의 0 바이트 `SI_xmp.xml` 은 실제 부재) · 글꼴 9 · 이미지 6 · sha256 둘 다 호출자 명시값과 일치.
- 보류 결정 (가)–(히): **(차)** 근거(중 — 온도 기울기로 곱을 가른 첫 표본 · τ = RC 가 면적 무관 관측) · **(주)** 근거(열째 표본) · **(이)** 근거(적합판 — 넷째 표본 · 산술 미재현) · **(치)** 근거(실험판 — 앞인자 가정) · **(비)** 근거(표본 — SEM 범위 · 공칭 · 그림 ↔ 실험 절 반전) · (너)(투)(두)(저)(그)(러)(수)(하)(미)(호) 약 · (처) 정성 메모 · (느)(시)(지)(티) 형식 참고 · (라)(마)(바) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(25호 ref 16 인용 자리 주석 · 문헌 Ea 인용 규칙 · C-rate 기준 용량 표기 — 글자는 호출자).
- ⚠ 부수 변경: `figures.json` 에 note 12 · 수동 2 를 더한 뒤 색인 함수 `_write_sources_index`(같은 코드 · `python3 -B`)를 다시 돌려 `raw/figures/_sources.json` 의 이 편 항목을 figures 12 → 14 로 — 다른 편 항목 변화 0(diff 확인).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 85호 행 · 85편 누적 · Evidence 여든 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-tortuosity-factor-effective-conductivity-split]](열세 번째 표본 · 주장하지 않는 것) · [[composite-cathode-percolation-utilization]](85호 절 — 전자 퍼콜 문턱 · λ 역전 · 신품 θ₀ ≤10 % · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](85호 절 · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](85호 절 · 처방 20 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](예순여덟 번째 적용 · 후보 줄 · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](85호 절 · 주장하지 않는 것) · `index.md` 변경 없음(새 페이지 0 · 페이지 수 53). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Wang·Li 행 흡수 표시 · 등급 ★ ↔ 25호 ★★ · 신규 후보 · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h · §6-3-i 47 행)은 호출자 몫.
- 후속(서지 기준, 미열람): **Kraft M.A., Ohno S., Zinkevich T., Koerver R., Culver S.P., Fuchs T., Senyshyn A., Indris S., Morgan B.J., Zeier W.G. 2018 *JACS* 140, 16330**([19] — 85 = 1 · 82 · 25 · 5호 본문 인용 · 원장 없음 · LPSCl1.5 조성 · 벌크 Ea 원전) · **Zuo T.-T., … Janek J. 2021 *Nat. Commun.* 12, 6669**([20] — 계면 호 배정 기둥) · **Ye L., Li X. 2021 *Nature* 593, 218**([2] — 다층 분리막 · 단락 임계 정의 자기 원전) · **Wang Y., Ye L., Chen X., Li X. 2022 *JACS Au* 2, 886**([3] — LPSCl-I) · Tan D.H.S., … Meng Y.S. 2021 *Science* 373, 1494([8]) · Lee J.S., Park Y.J. 2021 *ACS AMI* 13, 38333([21]) · Lai C.-H., … Dunn B.S. 2018 *Chem. Mater.* 30, 2589([26] — b 값 방법) · Hsu C., Mansfeld F. 2001 *Corrosion* 57(SI [1]) · Morino Y., … Kanno R. 2023 *JPCC* 127, 18678(SI [2]). 지목 누락 검사: 이 편 참고문헌 중 앞 호 후속 절에 올랐으나 원장 행이 없는 편 0.

## [2026-09-29] ingest | assb 86호 — Kim J.T., Shin H.-J., Kim A.-Y., Oh H., Kim H., Yu S., Kim H., Chung K.Y., Kim J., Sun Y.-K., Jung H.-G. 2023, An argyrodite sulfide coated NCM cathode for improved interfacial contact in normal-pressure operational all-solid-state batteries (J. Mater. Chem. A 11, 20549)
- raw: `raw/papers/kim2023_argyrodite-coated-ncm-normal-pressure-assb.md` (sha256 봉인 — `pdf_sha256` c0f7667f…f33738048 · 1,404,446 B · `si_sha256` 4d48d671…423e167d86 · 2,459,689 B) · 그림 `raw/figures/kim2023_argyrodite-coated-ncm-normal-pressure-assb/` (자동 20 — 본문 6 · ESI 14 · 라벨 · 내용 · 잘림 · 과대 영역 문제 0 · 캡션 필드 온전 · 수동 0 · **연 것 20/20** + 확대 판독 19 조각(1f · 1g · 3b · 4a–c · 4e · 4f · S4a–c · S12a–b · S13a · c · S11 · S1 · S6d · 6b — 판독용 · 커밋 안 함) + 화소 판독 둘(1g 마커 · S4 V 바닥) · `figures.json` note 20 · 본문 그림은 PDF 안 래스터 · p. 1 그래픽 0)
- **3차 묶음 파일 48**(스물여덟째 편; 2차 묶음 "큐 N" 과 별개 — "큐 48" 아님). 25호 digest 후속 ★★(ref 17 — "argyrodite 코팅 NCM, 상압 운전 — 저압 대조" · :104 본문 전사 "CAM 에 SE 코팅 → 저압 개선(refs 17–19)") · 원장 "★ 지목 25 · Q6 · 상압 운전 — 저압 대조군"(원장 ★ ↔ 25호 ★★) · KIST(Jung H.-G.) + 한양대(Sun Y.-K.) · © RSC(CC 문장 0) · ESI 15 쪽(그림 S1–S14 · 표 0 · ESI 참고문헌 0 — 본문이 부르는 항목 전부 있음 · ESI 제목이 본문과 다름 D10) · 참고문헌 47(자기 인용 7).
- ★★★ **(a) "추가 외부 운전 압력 없음" 의 실체**: 2032 코인셀 안의 ∅15 mm 삼층 펠릿(SE 150 mg 370 MPa → 복합 양극 30 mg 410 MPa → Li₀.₅In 분말 100 mg 190 MPa · `[재현]` 65.4 / 72.5 / 33.6 kN) · 스프링 · 스페이서 · 집전체 · 하중 값 · 계측 **전부 0** · "normal-pressure" 는 제목(본문 · ESI)뿐 · `[재현·외부 밀도]` 펠릿 ≈0.65 mm ↔ 80호 CR2032 내부 높이 2.57 mm → 스프링 필수 → 하중은 80호 층위(0.14–0.185 MPa)의 **유추만** → (미) 표 셋째 칸 "셀 형식 하중" 표본 · 59호 "<0.1 MPa" 보다 높을 수 있다.
- ★★★ **(b) 코팅**: one-pot(ACN : DBE 8 : 2 — §3 "20 wt%" D15) LPSCl_LP2 D50 1.44 µm(BM 8.24 · LP1 3.01) · σ 4.6 mS cm⁻¹ · Ea 0.2520 eV · σₑ 3.89e-9 · 코팅 NCM523 : Li₆PS₅Cl = 95 : 5(Rietveld 95.9 : 4.1) · 두께 "≈30 nm"(STEM 입자 하나 · 그림 3b 띠 `[도표]` ≈55 nm D6) · `[재현·외부 밀도]` BET 0.762 m² g⁻¹ 위 4.1 : 95.9 균일층 = 30.0 nm ✅ · 균일도 EDS 정성 · 부산물(P₂Sₓ · Li₂Sₙ · POₓSᵧ) 신품부터 · 비교군: 복합체 70 : 27 : 3 의 SE 정체 · 코팅 셀 70 wt% 기준 · 비용량 분모 미인쇄(총 SE 27 ↔ 29.9 wt%) · NCM523_BM 셀 전기화학 0.
- ★★★ **(c) "concrete contact"**: 채널 넷 — 단면 SEM(시야 하나 · 화살표) · Rc 1st 4.79 ↔ 14.4 Ω(`[재현]` 8.5 ↔ 25.4 Ω·cm² · 100th 50.8 ↔ 316) · GITT 피복률 83.9 ↔ 19.7 %(식 (1) 에 `D` 고정 — 값 · 출처 0) · 용량 149.6 ↔ 124.5 · ICE 74.1 ↔ 61.6 · 93.7 ↔ 68.9 % · 1C 66.9 ↔ 35.7 %(각 율 첫 값 D12) — 셀 하나씩(S13 400 MPa 둘째 셀 `[도표]` LP2 142–145 ↔ 149.6 = 3–5 % · LP1 ↔ LP2 7 %) · **R_bulk 22 → 99 · 19 → 52 Ω 미논의**(D16 · LP2 100th R_bulk > Rc).
- ★★★ **`[재현]` 첫 충전 등가**: 124.5/0.616 = 202.1 ↔ 149.6/0.741 = 201.9 mAh g⁻¹(`[도표]` 겹침) → 코팅 쌍의 정적 고립 차 ≈0 ↔ "피복률 ×4.26" · Rc ×0.33 → 차는 첫 사이클 안 동역학 · 분극 · 기생(bare CE `[도표]` 2–10 사이클 93 → 99 %) 몫 · Li₀.₅In 재고 11.3 mAh = 첫 충전 ×2.7 → LLI 밖 · bare 충전 상태 ΔR +269 Ω → 0.1C +102 mV ≪ −31 % → 정적 몫 또는 방전 끝 저항(미측정).
- ★★ **`[재현]` SE**: Ea σT 규약 0.247 ↔ 인쇄 0.2520 ✅(±0.015 · 축은 σ · 규약 미인쇄 — 85호와 반대) · 그림 S4 RT/30 °C 저항 비 `[도표·화소]` 1.67 · 1.74 · 1.47 ↔ 그림 1g RT ≈ 30 °C(D2 · Ea 0.25 예측 1.17) · 펠릿 두께 미인쇄 → 이온 역산 2.5–5.7 mm ↔ 전자 1.3–1.5 mm(D3) · 0.1C = 0.214 mA cm⁻² · 1.78 mAh cm⁻² · 적재 11.4–11.9 mg cm⁻².
- ★★★ **(e) 25호 귀속**: :104 "코팅 → 저압 개선" ✅ 문구 · 대조군은 압력이 아니라 코팅 유무(운전 압력 축 0) · :586 "상압 운전 — 저압 대조" 의 "상압" = 셀 형식 하중(값 0 · 대기압 표기 0) · 25호 2 MPa fine 85.6 % ↔ 코인 LP2 93.7 % 는 층위 비교까지(0.1C · 30 °C · 100 사이클 같음 · CAM · 음극 · 적재 다름).
- ★★ **(f) 잇기**: 80호(층위 유일 근거) · 81호(표 2 "0.1" 규약의 원전 쪽 표본) · 59호("<0.1" < 코인 스프링) · 52 · 60 · 33 · 5호 수치 0 · 63 · 64 · 84호 Ω·cm² 자릿수(84호 34.5 → 175 / 10 사이클) · 64호 0.1C 전류 밀도 214 µA cm⁻² 우연 일치 · 82호 방향만 · 65 · 29호 GITT 계열 셋째 표본 · 23호(= [44]) 병치 반복.
- **채움표 86호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 넷 — Rc 세 점 · SEM · GITT 피복률 · 용량 시계열) · Q2 층 둘(코팅 쌍 · SEM 병치) · Q3 층 하나(적합 입력 부재) · Q4 0/86 **일흔여덟 번째 성질**(`D·S²` 배정 · 첫 충전 등가 미대조 · R_bulk 침묵) · Q5 층 하나(서른세 번째 형태 — Li₀.₅In 분말 · 환산 0 · 액체 대조 창 불일치) · Q6 보고(셀 형식 하중 · 값 0 · 성형 3 점) · Q7 해당 없음(층 하나 — 재고 ×2.7 · CE 결손 ≠ 용량 손실) · Q8 층 하나(QOCV 원자료 미사용).
- **곱 축퇴 처방 예순아홉 번째 적용**: 부분 — 1단계 입력 없음(R 만 · CPE 0) · GITT `D·S²` 를 `D` 고정으로 `S` 배정한 셋째 표본(65 · 29 · 86호) · (저) 첫 충전 상한 교차 → 정적 차 ≈0 · DC ↔ EIS 자릿수 정합(50 ↔ 36.9 · 24 ↔ 25.6 Ω) · 처방 표 후보 줄 "GITT 피복률 ↔ 첫 충전 상한 교차".
- ⚠ 어긋남 16 건(D1 POₓ "139.9 eV" ↔ 그림 6b 134 · D2 S4 ↔ 1g RT · D3 σ ↔ σₑ 두께 · D4 410 ↔ 400 MPa · D5 Raman 421 ↔ 424 · D6 30 ↔ 55 nm · D7 "<1 µm" ↔ 1.44 · D8 범례 NCM532 · D9 "current amplitude 100 mV" · D10 ESI 제목 · 저자 표기 · D11 70 wt% 기준 · D12 율 첫 값 · D13 피복 ×4.26 ↔ ΔV ×2.1 · D14 "410 appropriate" ↔ S13c 평탄 · D15 8 : 2 ↔ 20 wt% · D16 R_bulk 침묵).
- 낱말 지문(본문 | 참고문헌 | ESI): `pressure` 8 · `MPa` 4 · `normal-pressure` 1(제목) | 0 | 3 · 0 · 1 · `coin` 2 · `spring` · `spacer` 0 · `contact` 18 · `coverage` 1 · `void` 3 · `pore` 3 · `crack` 1 · `tortuos` · `percolat` 0 · `identif` 1(다른 뜻) · `uniqu` · `sensitiv` · `uncertain` · `error` · `n =` 0 · `GITT` 4 · `Rc` 5 · `Ra` 1 · `CPE` 0(회로 그림에만) · `reference electrode` 0 · `0.62` · `0.6 V` 0 · `Li+/Li–In` 1 · `side reaction/product/parasitic` 19 · `uniform/homogeneous/even` 23 · `liquid-phase` 22 · `dispersant` 16 · `D50` 1 · `30 nm` 3 · `°C` 11 · `LAM` · `LLI` · `OCV` 0.
- PDF 메타데이터: 본문 `%PDF-1.6` · title = 논문 제목 · author "Jun Tae Kim" · subject "… (2023), 11, 20549-20558, doi:10.1039/D3TA03283C" · creator "Aspose Ltd." · producer "Aspose.PDF for .NET 22.3.0"(XMP 안 pdf:Producer "Acrobat Distiller 8.0.0 (Windows)") · 생성 2023-09-30 · **수정 2026-03-18** · XMP 4,003 B(doi · crossmark) · 글꼴 31 · 이미지 6(그림 1–6 래스터) · 내려받기 띠 0 · ESI `%PDF-1.5` · creator "Aspose Ltd." · producer "Aspose.Pdf for .NET 9.3.0" · **author "김 준태"** · 생성 2023-05-21(투고 12 일 전) · 수정 2023-09-04(수리 이튿날) · XMP 237 B · A4 · 이미지 14 · sha256 둘 다 호출자 명시값과 일치.
- 보류 결정 (가)–(대): **(미)** 근거(중 — 셀 형식 하중 표본) · **(차)** 근거(중 — `D·S²` 배정 · 코팅 한 손잡이) · **(주)** 근거(열한째 표본) · **(이)** 근거(적합판 — 다섯째) · **(치)** 근거(실험판 — 둘째) · **(비)** 근거(표본 — 입도 이름표 셋) · **(히)** 근거(표본 — 배정 선언) · **(저)** 근거(여섯째 표본 — 첫 충전 등가) · **(어)** 근거(재지목 +1) · **(내)** 근거(둘째 표본 — 재현되는 쪽) · (두)(그)(러)(하)(너)(투) 약 · (처) 정성 메모 · (느)(시)(지)(티)(개) 형식 참고 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(25호 ref 17 인용 자리 주석 · GITT 피복률 인용 규칙 · 코인셀 무외압 하중 칸 기본값 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 86호 행 · 86편 누적 · Evidence 여든한 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](86호 절 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](예순아홉 번째 적용 · 후보 줄 · 주장하지 않는 것) · [[assb-interphase-vs-contact-loss-attribution]](계보 86호 행 · 처방 5 셋째 표본 · 실험 아홉 편 · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](서른세 번째 형태 · 주장하지 않는 것) · [[composite-cathode-percolation-utilization]](86호 절 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](86호 절 · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](86호 절 · 처방 21 · 주장하지 않는 것) · [[assb-pressure-reapplication-separation-test]](86호 절 · 주장하지 않는 것) · `index.md` 변경 없음(새 페이지 0 · 페이지 수 53). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Kim J.T. 행 흡수 표시 · 등급 ★ ↔ 25호 ★★ · 신규 후보 · 재지목 Kim 2017 *Nano Lett.* [15] · Walther 2019 [46] · Auvergniot 2017 [42] · **지목 누락 Sakuda 2013 *Sci. Rep.* [13](71호 후속 ☆ · 원장 행 0)** · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h · §6-3-i 48 행)은 호출자 몫.
- 후속(서지 기준, 미열람): **Kim D.H., Oh D.Y., Park K.H., Choi Y.E., Nam Y.J., Lee H.A., Lee S.-M., Jung Y.S. 2017 *Nano Lett.* 17, 3013**([15] — 65 · 86 = 2 · 원장 ★★★ · GITT 피복률 원전 · `D` 원전 후보) · **Sakuda A., Hayashi A., Tatsumisago M. 2013 *Sci. Rep.* 3, 2261**([13] — 71 · 86 = 2 · 원장 행 0 — 지목 누락) · **Walther F., Koerver R., Fuchs T., Ohno S., Sann J., Rohnke M., Zeier W.G., Janek J. 2019 *Chem. Mater.* 31, 3745**([46] — 82 · 86 = 2) · **Oh D.Y., Kim D.H., Jung S.H., Han J.-G., Choi N.-S., Jung Y.S. 2017 *JMCA* 5, 20771**([16] — 원장 행 0) · Auvergniot J., Cassel A., Foix D., Viallet V., Seznec V., Dedryvère R. 2017 *SSI* 300, 78([42] — 23 · 64 · 86 = 3) · Rosero-Navarro N.C., Miura A., Tadanaga K. 2018 *JPS* 396, 33([17]) · Islam A.M., Chowdhry B.Z., Snowden M.J. 1995 *Adv. Colloid Interface Sci.* 62, 109([23]) · Nikodimos Y., … Hwang B.J. 2022 *EES* 15, 991([22]) · Zhou L., … Nazar L.F. 2019 *ACS Energy Lett.* 4, 265([18]) · Yubuchi S., … Tatsumisago M. 2019 *RSC Adv.* 9, 14465([38]) · Hua W. … 2014 *Dalton Trans.* 43, 14824([30]) · Shaju K.M., Subba Rao G.V., Chowdari B.V.R. 2004 *JES* 151, A1324([31]) · Yun B.-N., … Jung H.-G. 2022 *ACS AMI* 14, 9242([14]). 지목 누락 검사: 이 편 참고문헌 47 중 앞 호 후속 절에 올랐으나 원장 §1 행이 없는 편 **1(Sakuda 2013 [13])**.

## [2026-09-29] ingest | assb 87호 — Minnmann P., Strauss F., Bielefeld A., Ruess R., Adelhelm P., Burkhardt S., Dreyer S.L., Trevisanello E., Ehrenberg H., Brezesinski T., Richter F.H., Janek J. 2022, Designing Cathodes and Cathode Active Materials for Solid-State Batteries (Adv. Energy Mater. 12, 2201425)
- raw: `raw/papers/minnmann2022_designing-cathodes-cam-ssb-perspective.md` (sha256 봉인 — `pdf_sha256` f8924cab…1c2571e09 · 2,229,784 B · 보충 자료 없음) · 그림 `raw/figures/minnmann2022_designing-cathodes-cam-ssb-perspective/` (자동 7 — 라벨 · 내용 · 잘림 · 과대 영역 문제 0 · ⚠ 캡션 필드 셋(f2 쪽 바닥글 섞임 · f3 900 자 잘림 · f6 본문 두 문단 섞임) · 수동 0 · **연 것 7/7** + 확대 판독 6 조각(3b 고체 칸 · 식 (1) 400 dpi 렌더 · 7a 두 판 · 7b 두 판 — 판독용 · 커밋 안 함) + 화소 판독 둘(그림 4 축 · 선 · 점선 · 그림 5 곡선 열하나) · `figures.json` note 7 · 재수록 = 그림 7 셋 — (a) [86] Han 2021 ©Wiley · (b) [91] = 38호 Fig. 9(a)(c) CC-BY IOP · (c) [81] Jung S.H. 2020 ©Wiley "2019" · p. 1 그래픽 초록 0).
- **3차 묶음 파일 49**(스물아홉째 편; 2차 묶음 "큐 N" 과 별개 — "큐 49" 아님). 25호 digest 후속 ★(ref 4 — 서지 구별 메모 "≠ 2021 *JES* · 종설" · 축 "—" · 명제 0) · 11호 후속 ★(ref [18] · :1192 7위) · 29호 후속 표(ref 15 · 등급 칸 없음) · 원장 "★ 지목 25 · 종설 · ⚠ Minnmann 2021 *JES*(73호)와 다른 논문"(지목 칸 11 · 29 누락) · JLU Giessen(Janek · Richter) + KIT BELLA(Brezesinski) + HU Berlin/HZB(Adelhelm) + KIT IAM(Ehrenberg) · CC BY-NC-ND(버전 미인쇄) · Perspective 18 쪽 · 그림 7 · 표 0 · 번호 식 1 · 참고문헌 158(자기 인용 50 · 31.6 %) · 공동 1저자(Minnmann · Strauss).
- ★★★ **(a) 25호 귀속**: 판정 불가 — 25호 digest 가 매단 명제 0 · §2-1 전사 refs 11–19 만 · 25호 PDF 미보유(83 · 84 · 86호와 같은 공백 — 넷째) · `[해석]` 서론 "네 한계" 자리라면 이 편은 넷 다 서술하고 [21] · [13] · [76] = 66호 · [13,14,48] · [14,86,91] 로 간다(조건부) · 11호 [18] ✅ 방향("micro-sized SE → voids" ↔ §3.1 충전 밀도 · 작은 SE[30,55,57] → 1차 근거 [30] = 77호 · 그림 6 은 작은 SE 의 대가도 적음) · 29호 [15] ✅ 주제(SC · 무탄소 >60 vol%[31,36] → [31] = 73호 · [36] = 1호).
- ★★★ **(b) 설계 규칙 · 수치의 층위**: 48 행 — 인용 27 · 모형 인용 4 · 이 편 계산 4 · 의견 13 · 측정 0 · "3–5 µm" = 1호 모형(SE 3 µm 고정)에 "experimental results indicate"(D2) · "≈50 vol%" = 관행 서술[14,31,33–35] · 기준 미인쇄(`[재현]` 73호 42 % 공극 포함 ÷ 0.86 = 48.8 % 고상 · 63호 49 vol% 고상) · "60–70 vol%" = "geometrical models"(이름표 ✅ · 1호 AM:SE 62/38 · 66/34 · 72/28) · ">60 vol% 무탄소"[31,36] ✅ 73호 61 vol% · "≥≈70 vol%" 목표(의견) · 56호 "significant increase in overvoltage"[40] 율 조건 삭제(D5).
- ★★★ **`[재현]` 식 (1)**: `L ≤ √(3D̃_Li/C-rate)` · C-rate "in units of h⁻¹" → C-rate ÷ 3600 s 로만 그림 4 선 재현(0.1 · 1 C 여덟 점 ≤2 % · 5 C 1–4 % · h⁻¹ 그대로면 ×60 — D6) · 그림 4 D̃ 띠 `[도표·화소]` NCM 4.46×10⁻¹³–1.05×10⁻¹¹ · LFP 1.28×10⁻¹³–1.96×10⁻¹² cm² s⁻¹ → NCM 5 C 0.31–1.5 · 0.1 C 2.2–10.6 µm · "83 %" 는 [69] 위임 — 우리 구 확산 산술(정전류 · 표면 포화) L = 지름 95 % · 반지름 80 %(미폐합) · 그림 4 캡션 "conversion-type" 띠 0(D7).
- ★★ **`[재현]` 그림 5 ↔ 66호**: 함축 ΔV/V(등방 (1+k)³ − 1 · 판독 폭 ±0.1 %p) NCM111 −2.10 · "NCM532" −3.25 · NCM622 −4.75 · NCM811 −6.50 · LFP −6.00 · LNMO −7.01 · LCO +2.51 % ↔ 본문 "ΔVmax/V ≈ −5% for NCM-811 at 4.3 V"[76] = 66호 표 S1 −4.86 % ✅(같은 정의) · 그림 −6.5 % 는 66호 4.3 V ↔ 4.6 V(−7.35 · 원형 −6.95) 사이 · 캡션 전압 미인쇄(D1) · 5b r₀ = 20 µm a −1.79 · c −3.82 · c(4.0 V) +1.99 · total −2.22 % · 변환형 S → Li₂S +78.7–80.9 % ↔ "78%" ✅ · FeS₂ +160.8–163.6 % ↔ "65%" ✗ ↔ p. 12 "163%" ✅(D4 · 외부 밀도) · 이론 용량 147 · 894 · 1672 ✅.
- ★★ **(c) 접촉 손실 ↔ `LAM_PE`**: `contact loss` 9 · `loss of contact` 2 · 정의 0 · 결과 배정 넷(저항 그림 3b · 굴곡도 §2.2 [13,14,48] · 용량 §2.2 · 율 의존 용량 §4.1 식 (1) [86,91]) · `loss of active material` 1(FCG [81] — 접촉 손실과 따로) · `isolat` · `LAM` · `OCV` · `OCP` 0 · 73호 θ 어휘 · 재수록 7c 원전 라벨 "Ionically loosened / isolated" 옮기지 않음 · 가르는 도구 셋([43] = 22호 · [91] = 38호 · [31] = 73호)은 인용 목록에만 · 제안 0.
- ★★ **(d) 곱 축퇴**: 그림 3b(접촉 손실 → "increased interface resistances") · §2.3(산화 계면층 → "increased interfacial resistance, thereby impeding charge transfer"[12,49,61]) · 그림 3c(점접촉 → "limit electrode kinetics") · 결합 둘(크기 손잡이 면적 × 계면층 [37,49] · 코팅 한 손잡이 셋) · 가르는 실험 제안 0 · 대조군 후보 [86] · [120] · [79](인용 목록).
- ★★ **(e) 73호와의 관계**: [31] 7 괄호 전부 정성 · 73호 수치 · TLM · 차단 셀 · 14 % 0 · 무탄소 ✅ · ≈50 ↔ 42 % 기준 차 · θ 어휘 흡수("utilization … expressed by partial effective conductivities") · (호) 약(위임 +1) · (누) 기록만.
- **채움표 87호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나 — 배정 넷) · Q2 없다(층 하나 — 도구가 인용 목록에만) · Q3 층 하나(설계 수치의 층위 · 기준) · Q4 0/87 **일흔아홉 번째 성질**(모형 값에 '실험' 이름표 · 곱 인자를 한 저항 이름에 · 가르는 도구를 묶지 않음) · Q5 해당 없음 · Q6 칸 이동 없음(층 하나 — "a few to tens of MPa"[14,60]) · Q7 해당 없음(층 하나 — "zero excess" 명칭[4]) · Q8 층 하나(부피 변화 % 두 값).
- **곱 축퇴 처방 일흔 번째 적용**: 적용 불가(1차 자료 0) · 처방 표 새 줄 없음 · 문헌 쪽 표본(세 자리 + 결합 둘) · 후보 메모 "설계 종설의 'interface resistance' 는 문장별로 곱의 인자를 가른다"(카드 새 제약 2 · (차) 근거 — 결정 안 함).
- ⚠ 어긋남 11 건(D1 본문 −5 ↔ 그림 5 −6.5 % · D2 모형 값에 "experimental" · D3 그림 7b 범례 삭제 · 캡션 "particle cracking" · D4 FeS₂ 65 ↔ 163 % · D5 56호 율 조건 삭제 · D6 식 (1) 단위 · D7 그림 4 변환형 띠 0 · D8 "Aggunda et al." ↔ [146] Santhosha · D9 "inital" · "NCM532" · D10 7c ©2019 ↔ [81] 2020 · D11 그림 1 "Cell level" 항목 0).
- 낱말 지문(본문 | 참고문헌 | 약력): `contact loss` 9 · `loss of contact` 2 · `loss of active material` 1 · `isolat` · `disconnect` · `LAM` · `LLI` · `OCV` · `OCP` 0 · `tortuos` 8 · `percolat` 15 · `partial conductiv` 4 · `pressure` 8 · `MPa` 1 · `stack pressure` 0 · `coating` 43 · `exchange current` · `EIS` 0 · `impedance` 2 · `identif` 6(식별성 뜻 0) · `uniqu` 2 · `sensitiv` · `uncertain` · `error` 0 · `Li–In`/`indium` 0 · `Supporting` 0 · 의견 표지 8 | 참고문헌 · 약력 전부 0.
- PDF 메타데이터: `%PDF-1.6` · title "Designing Cathodes and Cathode Active Materials for Solid‐State Batteries"(U+2010) · author · keywords 빈칸 · subject "Advanced Energy Materials 2022.12:2201425" · creator "Adobe InDesign CS6 (Macintosh)" · producer "Adobe PDF Library 10.0.1; modified using iText 4.2.0 by 1T3XT" · 생성 2022-08-26(온라인 29 일 뒤) · **수정 2026-09-27**(내려받기 띠 27/09/2026 과 같음) · XMP 3,576 B(doi · crossmark MajorVersionDate 2022-07-28 · VoR) · 18 쪽 · 글꼴 13 · 내장 이미지 15(그림 7 래스터 · "Check for updates" 둘 · 저자 사진 여섯) · sha256 호출자 명시값과 일치.
- 보류 결정 (가)–(배): **(차)** 근거(중 — 설계 어휘의 곱 · 크기 손잡이 결합) · **(주)** 근거(열두째 표본 — 기준을 인쇄한 쪽 · [69] 위임) · **(이)** 근거(종설판) · **(치)** 근거(종설판) · **(비)** 근거(표본) · **(노)** 근거(표본 — 한 지면 두 값) · (호)(매)(두)(러)(수)(도)(대)(저)(나)(포) 약 · (처) 정성 메모 · (누) 기록만 · (느)(시)(지)(티)(개)(래) 형식 참고 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(25호 원문 재업로드 요청 · CAM 부피 분율 기준 표기 · 종설 재수록 그림 인용 규칙 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 87호 행 · 87편 누적 · Evidence 여든두 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](일흔 번째 적용 · 주장하지 않는 것) · [[composite-cathode-percolation-utilization]](87호 절 · 주장하지 않는 것) · [[assb-interphase-vs-contact-loss-attribution]](계보 87호 주석 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](87호 절 · 주장하지 않는 것) · [[assb-tortuosity-factor-effective-conductivity-split]](열네 번째 표본 · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](87호 절 · 주장하지 않는 것) · `index.md` 변경 없음(새 페이지 0 · 페이지 수 53). wiki 밖(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 Minnmann 2022 행 흡수 표시 · 지목 칸 11 · 25 · 29 · 신규 후보 · 재지목 다섯 · 지목 누락 둘 · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h · §6-3-i 49 행)은 호출자 몫.
- 후속(서지 기준, 미열람): **Koerver R., Zhang W., de Biasi L., Schweidler S., Kondrakov A.O., Kolling S., Brezesinski T., Hartmann P., Zeier W.G., Janek J. 2018 *EES* 11, 2142**([14] — 재지목 → 12 · 원장 ★★★) · **Ruess R., Schweidler S., Hemmelmann H., Conforto G., Bielefeld A., Weber D.A., Sann J., Elm M.T., Janek J. 2020 *JES* 167, 100532**([13] — → 6 · 원장 ★★★) · **Han Y., Jung S.H., Kwak H., Jun S., Kwak H.H., Lee J.H., Hong S.-T., Jung Y.S. 2021 *AEM* 11, 2100126**([86] — 9 · 38 · 87 = 3 · 원장 행 0) · **Jung S.H., Kim U.-H., Kim J.-H., Jun S., Yoon C.S., Jung Y.S., Sun Y.-K. 2020 *AEM* 10, 1903360**([81] — 38 · 87 = 2 · 원장 행 0) · Trevisanello E., Ruess R., Conforto G., Richter F.H., Janek J. 2021 *AEM* 11, 2003400([7] — → 2) · Liu X., … Yang Y. 2021 *AEM* 11, 2003583([120] — 59 · 87 = 2 · 지목 누락) · Ohno S., Rosenbach C., Dewald G.F., Janek J., Zeier W.G. 2021 *AFM* 31, 2010620([49]) · Strauss F., de Biasi L., Kim A.-Y., Hertle J., Schweidler S., Janek J., Hartmann P., Brezesinski T. 2020 *ACS Mater. Lett.* 2, 84([79]) · Walther F., … Janek J. 2019 *Chem. Mater.* 31, 3745([11] — → 3) · Randau S., … Janek J. 2021 *Chem. Mater.* 33, 1380([58]) · Usiskin R., Maier J. 2018 *PCCP* 20, 16449([69]) · Randau S., … Janek J. 2020 *Nat. Energy* 5, 259([28] — 27 · 53 · 87 = 3 · 지목 누락) · Ohno S., … Zeier W.G. 2019 *Chem. Mater.* 31, 2930([48]) · Zhang Y.-Q., … Ceder G. 2020 *AEM* 10, 1903778([93] — 4 · 87 = 2) · Doux J.-M., … Meng Y.S. 2020 *JMCA* 8, 5049([60] — → 4) · Usiskin R., Maier J. 2020 *JES* 167, 080505([62] ☆) · Deysher G., … Meng Y.S. 2022 *Mater. Today Phys.* 24, 100679([38] ☆).

## [2026-09-29] ingest | assb 88호 — Li M., Xue D., Rong Z., Fang R., Wang B., Liang Y., Zhang X., Huang Q., Wang Z., Zhu L., Zhang L., Tang Y., Zhang S., Huang J. 2025, Stack Pressure Enhanced Size Threshold of Si Anode Fracture in All-Solid-State Batteries (Adv. Funct. Mater. 35, 2415696)
- raw: `raw/papers/li2025_si-anode-fracture-size-threshold-stack-pressure-assb.md` (sha256 봉인 — `pdf_sha256` f8d22ffa…6590e145 · 4,942,192 B · `si_sha256` cb738fb9…d7292413 · 4,784,856 B · 영상 mp4 1,515,155 B sha256 76cebd50…21c40aa1 은 본문에 · 셋 다 호출자 명시값과 일치) · 그림 `raw/figures/li2025_si-anode-fracture-size-threshold-stack-pressure-assb/` (자동 33 + 수동 4 = 37 · **연 것 37/37** · ⚠ 첫 실행은 업로드 본문 파일명의 "_Si_" 가 도구 SI 판별 정규식에 걸려 본문 그림이 SI 키로 충돌(27 항목) → 같은 바이트의 공백 이름 링크로 재추출 · `sources` · `src` 는 원 파일명으로 되돌림 · 도구 무수정 · S11 · S14 바닥 잘림 · 표 S1 · S2 미인식 → 수동 넷 · 캡션 필드 문제 다섯(f4 · fS2 · fS3 · fS19 · tS3) · 화소 판독 그림 2 · 4 · 5 · S4a · S7 · S13a · S26).
- **3차 묶음 파일 49-2**(서른째 편; 업로드 파일명의 "49." 가 87호와 겹쳐 인수인계 노트가 "49-2" 로 갈라 적음). 13호 후속 ★★(ref [35] · :349 "`<5 MPa` 의 근거 후보 — 압력 → 파괴 문턱 사상") · 60호 후속 ★★★(:629 "13호 `<5 MPa` 의 마지막 확인처") · 원장 "★★★ 지목 13 · 60 · Q6 · 마지막 확인처 · 추후 요청 후보 1 순위". 1차 측정 + 모형 — NCM811(LiNbO₃ 코팅 단결정) : LSPSCl 7 : 3 wt \| LSPSCl \| 순수 Si 분말(SE · 탄소 0) · Si 50 nm–44 µm 여섯 + 볼밀 · ∅10 mm PEEK 금형 · 명목 460 MPa · 1C 500 사이클 · 상장 파괴 모형(COMSOL 6.0 · 단일 구 · 경계 압력 0–400 MPa).
- ★★★ **(a) 13호 귀속**: ❌ — 텍스트 층(본문 · SI) "5 MPa" 0 · `requir` 0 · 저압 · 수동 케이스 · 모듈 어휘 0 · 압력은 "necessary" · "essential" 로만 · `[재현]` 이 편 그림 5 안 식에 5 MPa → 0.150 µm(점 보간 0.156 — 액체 무압 문턱과 같음 · 13호와 반대 함축). 13호 `<5` 의 인용 다리 셋([23] 59호 · [45] 60호 · [35] 88호) 모두 빔 · 계보 아홉 편 · 여섯 값 · 띠 0.1–5 MPa · 확인된 원전 0 그대로 · 빈 다리 넷(8 → 81 · 13 → 59 · 13 → 60 · 13 → 88) · 열린 다리 셋(12 · 39 · 61) · 13호 :349 의 "압력 → 파괴 문턱 사상" 은 있다(고압 쪽 · 모형).
- ★★★ **(b) 압력 정의 · 측정**: 성형 SE 380 → 양극 920 → Si 380 → 전체 460 MPa = 운전 명목(조립 마지막 압착과 같은 숫자) · `[인쇄]` "the distance between the top and bottom punches was fixed"(정변위) · 계측 0 · 사이클 중 변동은 [15] Han 2021 "within 2 MPa" 인용 · 자기 모식 S21 은 탈리튬 때 셀 안 계면 틈 h · 해체 뒤 틈(S20)은 "impossible … inside the battery" 라 저자 인쇄 · `[재현]` ∅10 mm → 460 / 200 / 764 / 1070 MPa ≙ 36.13 / 15.71 / 60.00 / 84.04 kN(둥근 kN — 명목) · 200 MPa 세트 제조 절 미인쇄(G2) · (미) 약(고압 판 표기 문제) · (배) 근거 0 · (하) 근거(중).
- ★★★ **(c) size threshold 세 층**: 실험 괄호(460: 1–5 µm · 200: 0.3–1 µm — 셀 하나씩) · 모형 점 10(`[도표·화소]`) · 그림 안 식 `p ≈ 0.35(D−D₀)^0.4`(D₀ 150 nm = 액체 문헌 [8]) — `[재현]` 식 460 → 2.13 µm(본문 ≈2 ✅) · 1 µm → 328 MPa(본문 ≈330 ✅) · 식 ↔ 점 +120 %(D 0.206) · 점 보간 460 → 2.63 µm · 그린 곡선 ≈2.18 µm · 그림 4(e) 임계 ≈325 MPa · `J_c` 9.41 ↔ 10.78(D2) · 캡션 "radius" ↔ 판 "D"(D1) · 지수 0.4 · 계수는 괄호 폭(×5 · ×3.3)으로 정해지지 않는다.
- ★★ **(d) Q1 · Q6 · Q7 · Q8(음극 판)**: Q1 없다(`θ(N)` 0/88 — 크기 효과는 CE 로만 · 용량 유지 크기 무관 표 S1 49–74 % · 파괴 Si-5 ↔ 무파괴 Si-1 `[도표·화소]` 59 · 59 % · 200 ↔ 460 MPa 무파괴 Si-0.3 44 ↔ 72 · 59 % 셀 하나) · Q6 보고(명목 · 정변위 · 계측 0 · 13호 `<5` ❌) · Q7 CE 결손 = 누설(저자 배정 미세 단락 · Si-5 4.25 V 요동 · 1070 MPa 셀 충전 376 · 407 > NCM811 275.5) · N/P 2.6 · `[재현]` Si 이용률 첫 충전 33–42 % · 가역 21–25 % → 탈리튬 고립 `θ_NE` 는 완충(`[해석]`) · Q8 부피 변화 세 층(">300%" 인용 0 ↔ 모형 ε₀ ≈0.4 → 120 / 174 % ↔ 이용률).
- ★★ **(e) 60호 · 파일 50**: 다른 연구실(Xiangtan · Yanshan · Penn State ↔ Xiamen) · 다른 Si 계열(시판 결정 Si 분말 ↔ Li₂₁Si₅ 합금 이중층) · 서로 인용 0(13호 [35] 로만 만남) — 60호 G2(가압 ↔ 무압 한 계열 대조)를 메우지 못하고 두 가압 수준(200 ↔ 460 MPa)만 준다 · G2 의 다리는 여전히 파일 50.
- ★ **(f) SI · 영상**: SI 37 쪽 전부(그림 S1–S26 · 표 S1–S3 ✅ — S1–S26 은 전부 본문에서 불림 · 표 S3 은 본문 0 회) · mp4 하나 = Movie S1 추정(SI 가 부르는 영상 하나 · 파일 안 라벨 확인 0) — `[재현]` 상자 판독 5.314 s · 1920 × 1080 · 161 프레임 · 음성 0 · Lavf58.20.100 · **미열람**(디코더 없음 · 설치 금지) · 지면은 내용을 모형 출력(1 µm · 무압 ↔ 400 MPa 경계)이라 적는다.
- ★★★ **`[재현]`**: 적재 25.49 mg cm⁻² · 1C 3.75 mA cm⁻² ✅ · N/P 2.6 ↔ 양극 ≈200–205 mAh g⁻¹(미인쇄) · Si 3579 ✅ · NCM811 275.5 · 유지율 기준 = 첫 1C(그림 2 ±2.1 %p · S7 ±1.4 %p — 표 S2 = S7) · 표 S3 λ 1.25 nm · K_Ic 1.01 / 0.65 MPa m^½(`[재현·가정]`) · 전극 두께 "35.07 µm" ↔ 치밀 Si ×2.48 · ×2.15(`[재현·외부 값]`) · CE 해상도 0.163 %/사이클 · 일정 76 · 93 일.
- **채움표 88호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(음극 판 · 층 둘) · Q2 없다(층 하나 — 손잡이 셋 · 판정량 CE · SEM) · Q3 층 하나(critical size 세 층) · Q4 0/88 **여든 번째 성질**(명목 셀 압력 = 입자 경계 압력 · 판마다 다른 `J_c` · 괄호 두 점으로 거듭제곱) · Q5 해당 없음(층 하나 — "vs Li⁺/Li" 표기) · Q6 보고(칸 이동 없음 · 13호 `<5` 마지막 다리 ❌) · Q7 해당 없음(층 하나 — CE = 누설) · Q8 층 하나(부피 변화 세 층).
- **곱 축퇴 처방 일흔한 번째 적용**: 적용 불가(음극 판 · EIS 0 · 면적 0) · 처방 표 새 줄 없음 · 음극 판 곱 문장 표본(`[인쇄]` "deterioration of interface contact increased the interfacial impedance … current focusing" — 측정 0) · 한 손잡이 여러 노브(압력 = 파괴 억제 + 접촉 + 압착 균열 · 크기 = 파괴 + 공극 + 리튬화 깊이 + 반응 면적).
- ⚠ 어긋남 18 건(D1 캡션 radius ↔ 판 D · D2 `J_c` 9.41 ↔ 10.78 · D3 식 ↔ 점 +120 % · D4 공기 노출 0 ↔ 공기 산화 동정 · D5 표 S2 "Figure S6" · D6 S5 3.3 mg · N/P 2.3 · D7 S4a 두 세트 혼합 · D8 표 S2 46 % · D9 완전지 "vs Li⁺/Li" · D10 [2f] = [12] · D11 "Li₁₅Si₄" ↔ amorphous · D12 "same mass … more active material" · D13 "nonconductive" 덴드라이트 · D14 임피던스 측정 0 · D15 부피 세 층 · D16 "Figure 2e" = S2e · D17 XRD "no side reactions" · D18 S13 "0 MPa" = 그림 2e 셀 값).
- 낱말 지문(본문 | SI): `contact` 16 | 0 · `contact loss` / `loss of contact` 0 · `isolat` · `disconnect` · `LAM` · `LLI` · `OCV` · `OCP` · `SEI` · `dead Li` 0 · `EIS` 0 · `impedance` 1 · `fractur` 53 | 8 · `crack` 38 | 21 · `pressure` 51 | 12 · `stack pressure` 30 | 2 · `MPa` 14 | 7 · `requir` 0 · "pressure-free" 2 · `short circuit` 16 | 2 · `dendrite` 30 | 3 · `coulombic efficiency` 24 | 2 · `identif` 2(식별성 뜻 0) · `uncertain` · `error` 0.
- PDF 메타데이터: 본문 `%PDF-1.6` · title U+2010 하이픈 둘 · subject "Adv Funct Materials 2025.35:2415696" · creator "LaTeX with hyperref package" · producer "Acrobat Distiller 24.0 (Windows); modified using iText 4.2.0 by 1T3XT" · 생성 2025-01-24 · **수정 2026-09-28**(내려받기 띠 28/09/2026 · pp. 2–11) · XMP 3,578 B(VoR · crossmark 2024-11-26) · SI `%PDF-1.7` · pdftk-java 3.0.9 · itext-paulo-155 · 생성 = 수정 2025-02-18 · XMP 0 · p. 1 Wiley 표지 + A4 36 쪽 · 내장 이미지 26(그림 S1–S26 하나씩).
- 보류 결정 (가)–(재): **(리)** 근거(닫힘 — 13호 [35] 가닥 ❌ · 남은 묶음 (거) + Tian·Qi 2017 + Wang 2021 *Joule*) · **(하)(대)(저)(츠)(치)** 근거(중) · **(이)** 근거(표본) · **(쿠)** 근거(재지목 — Yamamoto 2020 [6c]) · (미)(주)(차)(러)(비)(매)(도)(키)(재) 약 · (처) 정성 메모 · (디) 형식 참고 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0(**(거)** 포함 — 이 편 참고문헌에 Sharafi · Wang·Sakamoto 0) — **결정 안 함**. 새 판단 거리 셋(13호 `<5` 가닥 종결 표기 · "stack pressure" 명목 ↔ 계측 표기(고압 판 (미)) · 모형 경계 압력 ↔ 셀 압력 사상 표기 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 88호 행 · 88편 누적 · Evidence 여든세 번째 · 13호 새 제약 3 의 88호 주석 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](88호 절 · 13호 표 다섯째 주석 · 81호 계보 요약 뒤 88호 주석 · 주장하지 않는 것) · [[assb-pressure-reapplication-separation-test]](88호 절 — D1–D5 대조 · 정변위 인쇄 · 해체 뒤 틈 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](일흔한 번째 적용 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](88호 절 — 음극 판 대응 · CE 누설 · N/P 완충 · 압력 두 수준 · 주장하지 않는 것) · `index.md` 변경 없음(새 페이지 0 · 페이지 수 53).
- wiki 밖(호출자 몫): 원장 §1 Li Menglin 행 흡수 표시(88호 · ❌) · 재지목 Han 2021 [15] → 4 · Wang C. 2022 [12] = [2f] → 2 · Zhang F.Y. 2023 [11b] → 2 · Tan 2021 [3g] → 2 · **지목 누락** Yamamoto 2020 [6c](59 · 60 · 88 = 3 · 원장 행 0 · §3-b (쿠)) · 새 행 후보 · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h · §6-3-i 49-2 행 · `wiki/tools/extract_figures.py` SI 판별 정규식의 밑줄 오분류(도구 소유자 판단).
- 후속(서지 기준, 미열람): **Han S.Y., Lee C., Lewis J.A., Yeh D., Liu Y., Lee H.-W., McDowell M.T. 2021 *Joule* 5, 2450**([15] — 재지목 → 4) · **Yamamoto M., Terauchi Y., Sakuda A., Kato A., Takahashi M. 2020 *JPS* 473, 228595**([6c] — 59 · 60 · 88 = 3 · 지목 누락) · **Piper D.M., Yersak T.A., Lee S.H. 2013 *JES* 160, A77**([11a]) · **Liu X.H., Zhong L., Huang S., Mao S.X., Zhu T., Huang J.Y. 2012 *ACS Nano* 6, 1522**([8] — D₀ 원전) · **Huo H., … Janek J. 2024 *Nat. Mater.* 23, 543**([14a]) · Wang C.H., … Sun X.L. 2022 *Joule* 6, 1770([12] = [2f] — → 2) · Zhang F.Y., … Huang J.Y. 2023 *eTransportation* 15, 100220([11b] — → 2 · 자기 인용) · Sakka Y., … Orikasa Y. 2024 *JES* 171, 070536([14b]) · Tan D.H.S., … Meng Y.S. 2021 *Science* 373, 1494([3g] — → 2) · Cao D.X., … Zhu H.L. 2023 *AEM* 13, 2203969([10]) · Yang H., … Zhang S. 2014 *JMPS* 70, 349(SI [4]) · Pharr M., Suo Z., Vlassak J.J. 2013 *Nano Lett.* 13, 5570 · Kushima A., Huang J.Y., Li J. 2012 *ACS Nano* 6, 9425(SI [6]) · ☆ Trevey J.E., … Lee S.H. 2010 *ESSL* 13, A154([9]) · ☆ Liu X.H., … Zhu T. 2013 *ACS Nano* 7, 1495([16b]).

## [2026-09-29] ingest | assb 89호 — Zhang Z., Sun Z., Han X., Liu Y., Pei S., Li Y., Luo L., Su P., Lan C., Zhang Z., Xu S., Guo S., Huang W., Chen S., Wang M.-S. 2024, An all-electrochem-active silicon anode enabled by spontaneous Li–Si alloying for ultra-high performance solid-state batteries (Energy Environ. Sci. 17, 1061–1072)
- raw: `raw/papers/zhang2024_all-electrochem-active-si-li21si5-anode-assb.md` (sha256 봉인 — `pdf_sha256` 7c53d446…870e2d4e · 5,093,432 B · `si_sha256` ddf7a702…ba7cf45a · 744,000 B · 둘 다 호출자 명시값과 일치) · 그림 `raw/figures/zhang2024_all-electrochem-active-si-li21si5-anode-assb/` (자동 18 + 수동 2 = 20 · **연 것 20/20** · ⚠ 업로드 본문 파일명 "…spontaneous_Li_Si_alloying…" 의 "_Si_" 가 도구 SI 판별 정규식에 걸리는 것을 원 이름으로 먼저 확인하고 **첫 실행부터** 밑줄 → 공백 이름 링크로 추출(88호와 같은 우회 · 도구 무수정) · `sources` · `src` · `_sources.json` 은 원 파일명 · 자동 누락 그림 2 · 5(RSC 캡션 "Fig. N The …" 의 'The' 가 도구 `VERBS` 에 걸려 본문 문장으로 판정) → 수동 둘 · ESI 크롭 바닥 0.8–1.3 pt(여백) 셋 · 캡션 필드 문제 0 · 화소 판독 그림 6f · 6g · 확대 판독 그림 5e).
- **3차 묶음 파일 50**(서른한째 편 · **3차 묶음의 마지막 파일**). 60호 후속 ★★★(ref 22 · :630 "같은 음극 계열의 가압 판(Table S2: 50 MPa · 600 사이클 · 3 mA cm⁻² · 3.2 mAh cm⁻² · 55 °C) — G2 를 메울 유일한 다리 · '370 MPa' 의 출처 후보") · 원장 "★★★ 지목 60 · 추후 요청 후보 2 순위". 1차 측정 · 모형 0 — 자발 합금 Li₂₁Si₅ + Si 50 : 50 wt% 단층(10 mg · 400 MPa · 결착제 · 도전재 · SE 0 — "all-electrochem-active") | Li₆PS₅Cl | Li₃InCl₆ | LCO : Li₃InCl₆ 6 : 4 · 성형 400 / 370 / 350 MPa · 25 · 55 ℃ · ICE 97.8 % · 17.9 mAh cm⁻² · 팽창률 18.8 % · 55 ℃ 1000 사이클 66.7 %.
- ★★★ **(a) 60호 G2 다리**: ❌ 불성립 — 이 편 지면(본문 · ESI · 그림 라벨 전수)에 **운전 압력 0** · 60호 표 S2 "50 MPa" 는 같은 저자의 **사후 부여** · 두 편 사이에 음극 구조(단층 400 ↔ 이중층 600 MPa) · 온도(55 · 25 ↔ 45 ℃) · 전류 · 적재 · Si 원료(HongWu "micron" ↔ Xuzhou Jiechuang 1 µm) · 유지율 기준이 함께 다름 · 같은 셀 압력 대조 0 — 성립하는 것은 가계(같은 연구실 · 겹친 저자 11 · 같은 NSFC 두 과제 · 같은 Li₂₁Si₅ 합성 · SE · 양극 · 금형 · 창)까지 · 60호 표 S2 행: 50 MPa ❌ · 600 ⚠(80.1 %@599 = 80 % 도달 규약 · `[도표·화소]` 첫 이탈 ≈400 · ≈555–600 설명 없는 계단 꼬리) · 3 mA cm⁻² ⚠(그림 5c 22.9 mg cm⁻² 다른 셀) · 3.2 mAh cm⁻² ⚠(인쇄 0 · `[재현]` 후보 셋) · 55 ℃ ✅.
- ★★★ **(b) 압력**: 셀 형식 "ASSB mould (WuHan Chuangneng)" · 성형 음극 400 · 이중 SE 370 · 셀 350 MPa 3 min · 운전 인가 방식 · 값 · 계측 · 면적 0 · 그림 S8 라벨 "24 hours at 400 Mpa"(음극 XRD 시료 · 유지 여부 미인쇄) · 온도 25 · 55 ℃(제어 방식 미인쇄) · (캐) 셋째 형태 "미인쇄 → 후행 편 부여" · (미)(배) 근거 0 · (하) 근거(약 — 설명 없는 계단 회복).
- ★★★ **(c) "370 MPa"**: 이 편 = 이중층 SE(Li₆PS₅Cl 30 mg + Li₃InCl₆ 50 mg) 냉간압착 · 인용 0 · 요구치 · 운전 값 아님 · 음극은 400 MPa — 60호 서론 "Si … 370 MPa is required[10–13]" 의 요구치 출처 아님(확인처 60호 [13] = Huo & Janek 2022 = 이 편 [12]) · 60호 "Compared to the case of 370 MPa" 의 음극 판도 이 편에 없음.
- ★★★ **(d) all-electrochem-active · Q7**: 조성 정의("without binders and conductive agents") · Si 이용률 · 음극 비용량 · N/P · 면적 · 저장고 양 인쇄 0 · `[재현]` Li₂₁Si₅ 5 mg → 9.83 mAh · 저자 "will supplement the lithium loss of the cathode" + XPS "decomposition of Li6PS5Cl is more significant" → **ICE · CE ≠ LLI · 부반응 게이지**(60호에 이은 같은 연구실 둘째 표본) · `[재현·외부 값]` 10 mg · 56.5 µm · 17.9 mAh cm⁻² 불폐합(A ≥ 1.142 ↔ A ≤ 0.968 · 1.084 cm²).
- ★★ **(e) Q1 · Q6 · Q8**: Q1 없다(`θ(N)` 0/89 — 사후 단면 두 시야 · XPS 50 사이클 · EIS 한 점) · Q6 보고(성형만) · Q8 `[재현·외부 값]` 18.8 %(+10.6 µm) ↔ Li 부피 치밀 환산 +62 µm(순수 Si +74.4 는 양립) · Young 률 인쇄 10.0–11.6 GPa(외부 값과 한 자릿수). **(f)** 요구치 · 문턱 0 · 13호 가닥 무관 · (채) 근거 0. **(g)** 88호와 서로 인용 0 · Si 파괴 크기 문턱 인용 0 · 88호 (e) 절 "50 MPa" 는 60호 표 경유. **(h)** ESI 14 쪽 · 그림 S1–S12 · 표 S1 전부 봄 · Video S1–S3 받지 않음(본문 설명만 — 셋 다 합성 영상).
- ★★★ **`[재현]`**: 비용량 144.6 · 116.5 · 124.6 mAh g⁻¹ · 첫 충전 3.601 · 9.185 · 18.482 mAh cm⁻² · C-rate 함축 기준 131.0(1C = 3 mA cm⁻²) · 23.8("20C" = 11.5) · 26.5("60C" = 12.74) mAh g⁻¹ · "357C" → 987 mA cm⁻²(131 기준) · 팽창 117.91 · 18.76 %(초록 18.9 ❌) · 치밀 하한 A ≥ 1.142 cm²(ρ Li₂₁Si₅ 1.161 외부 값) · 60호 전사값 A ≥ 1.41 cm² · 저장고 9.833 mAh · 그림 6g 기준 121.3 → 66.9–67.6 %(66.7 ✅) · 첫 80.1 % 이탈 ≈400 · 그림 5c 기준 둘째 사이클(94.06) · S12 52.92 % ✅ · d₅₃₁ 0.3163 nm ✅ · Si XRD ✅ · 식 (1) ✅ · DC σ 비 양립 · 절대값 재현 불가 · 일정 25 · 36 · 86 일.
- **채움표 89호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(음극 판 · 층 둘) · Q2 없다(층 하나 — 함량 한 손잡이) · Q3 층 하나(조성 이름표 · 기준 미인쇄) · Q4 0/89 **여든한 번째 성질**(저장고 셀 ICE 를 저장고 없는 문헌 ICE 와 한 축에 "최고" 로 · SE 분해 ↑ 인데 부반응 억제로 · 조건 미인쇄) · Q5 해당 없음(층 하나 — "vs. Li/Li⁺") · Q6 칸 이동 없음(층 넷 · G2 다리 ❌) · Q7 해당 없음(층 하나 — 음극 저장고) · Q8 층 하나(18.8 % 불폐합).
- **곱 축퇴 처방 일흔두 번째 적용**: 적용 불가(1단계 R 하나 · C · 면적 0) · 처방 표 새 줄 없음 · 60호 M2 줄 둘째 표본 · 음극 판 곱 문장(전도 ↑ → 분해 ↑ → Li₂S SEI — 측정 0) · 한 손잡이 여러 노브(Li₂₁Si₅ 함량 = 전도 · 저장고 · 완충 · 분해 · 두께).
- ⚠ 어긋남 18 건(D1 80.1 %@599 = 계단 꼬리 · D2 C-rate 기준 셋 · "357C" · D3 음극 불폐합 · D4 18.8 % ↔ Li 부피 · D5 초록 18.9 % · D6 ESI S11 "LFP" ↔ "LCO" · D7 그림 3 "j" ↔ 패널 k · D8 S8 "24 hours at 400 Mpa" ↔ "standing" · D9 "CCD" = 최대 시험 전류 · D10 Young 률 · D11 몰비 21 : 5 ↔ 5 : 21 · D12 오기 여섯 · D13 "vs. Li/Li⁺" · D14 kg 급 · 여섯 지표 · D15 PITT 단위 · 전압 · D16 서지 · D17 60호 표 S2 ↔ 표 S1 값 불일치 · D18 97.8 % 두 셀).
- 낱말 지문(본문 | ESI): `contact` 13 | 0(전부 합성 · 제작) · `contact loss` 0(배터리 뜻) · `crack` 1 · `fractur` · `isolat` · `delaminat` 0 · `pressure` 2 | 0(합성 · 성형) · `stack pressure` 0 · `MPa`/`Mpa` 값 5 | 1(400 · 370 · 350) · `requir` 4(합성) · `threshold` 0 · `ICE` 23 | 3 · `N/P` 0 · `prelithi` · `reservoir` 0 · "lithium supplement/source/supply" 10 · `self-discharge` 5 · `LLI` · `LAM` · `OCV` · `OCP` 0 · `SEI` 1 · `identif` 1(합성) · `uncertain` · `error` 0.
- PDF 메타데이터: 본문 `%PDF-1.3` · Aspose.PDF for .NET 22.3.0 · title 의 en dash 가 "&#x2013;" 문자열 · subject "Energy & Environmental Science (2024), 17, 1061-1072, doi:10.1039/D3EE03877G" · 생성 2024-02-06 · **수정 2026-03-18** · XMP 3,759 B(dc:creator 15 · prism · crossmark 2024-02-06) · 12 쪽 595.3 × 779.5 pt · 그림 JPEG 7 · ESI `%PDF-1.7` · Aspose.Pdf for .NET 9.3.0 · author "zhang zhiyong" · 생성 2023-12-05(승인 2 일 전) · 수정 2024-01-02 · XMP 237 B(빈) · 14 쪽 A4 · 이미지 12(그림 S1–S12 하나씩).
- 보류 (가)–(히) · (개)–(패): **(대)** 근거(강) · **(캐)(츠)(도)(브)** 근거(중) · **(하)** 근거(약) · (너)(저)(므)(매)(재)(러)(비)(차)(주) 약 · (처) 정성 메모 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0(**(채)(태)(패)(쿠)(미)(배)** 포함) — **결정 안 함**. 새 판단 거리 셋(문헌 비교표 · 후행 편의 운전 압력 칸 표기 · 선리튬화 셀 ICE · CE 인용 규칙 · 유지율 · 80 % 도달 사이클 인용 규칙 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 89호 행 · 89편 누적 · Evidence 여든네 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](89호 절 · 60호 절 주석 · 주장하지 않는 것) · [[assb-pressure-reapplication-separation-test]](89호 절 — D1–D5 0/5 · 설명 없는 계단 회복 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](일흔두 번째 적용 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](89호 절 — 저장고 셀 ICE · CE · 18.8 % · 주장하지 않는 것) · `index.md` 변경 없음(새 페이지 0 · 페이지 수 53).
- wiki 밖(호출자 몫): 원장 §1 Zhang Z. 2024 행 흡수 표시(89호 · G2 다리 ❌ · 문구 "같은 음극의 가압 판 (50 MPa · 600 사이클)" 정정) · 재지목 Tan 2021 [14] → 3 · Chen C. 2018 [23] → 2 · **지목 누락** Huo & Janek 2022 *ACS Energy Lett.* 7, 4005([12] · 60 · 89 = 2 · 원장 행 0) · 새 행 후보(Yan W. 2023 [15] · Zhao J. 2014 [35]) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-h · §6-3-i 50 행 · `wiki/tools/extract_figures.py` VERBS 'The' 오판(RSC 캡션 · 도구 소유자 판단).
- 후속(서지 기준, 미열람): **Huo H., Janek J. 2022 *ACS Energy Lett.* 7, 4005**([12] — 지목 누락 · 60 · 89 = 2) · **Tan D.H.S., … Meng Y.S. 2021 *Science* 373, 1494**([14] — 재지목 → 3) · **Chen C., Li Q., Li Y., Cui Z., Guo X., Li H. 2018 *ACS AMI* 10, 2185**([23] — 재지목 → 2) · Yan W., … Wu F. 2023 *Nat. Energy* 8([15]) · Zhao J., Lu Z., Liu N., Lee H.-W., McDowell M.T., Cui Y. 2014 *Nat. Commun.* 5, 5088([35]) · ☆ Ratchford J.B., … Wolfenstine J. 2011 *JPS* 196, 7747([21]) · ☆ Shenoy V.B., Johari P., Qi Y. 2010 *JPS* 195, 6825([18]) · ☆ Huang Y., Shao B., Wang Y., Han F. 2023 *EES* 16, 1569([27]) · ☆ Xu X., … Ci L. 2023 *Small* 2302934([29]) · ☆ Lee D., Lee H., Song T., Paik U. 2022 *AEM* 12, 2200948([11]).

## [2026-10-01] ingest | GitHub 연구 브리핑 (일일 브리핑 첫 회)
- raw: `raw/articles/2026-10-01-github-research-briefing.md` (원문 + 릴리스 · PR #5755 WebFetch 1차 대조 — 원문 보장 아님 표기)
- 수집 목적 (사용자 결정 · 앞으로의 기준): 의존성 위험 감시 · 경쟁 도구 · 미세단락 도구 · 실험 아이디어
- 새 페이지 3: [[pybamm]] (영향 판정표 — #5745 · #5765 · #5694 · #5770 은 우리 경로 밖, #5755 는 x 격자 접합부 열린 물음, breaking 은 requirements 상한 부재로 간접 위험) · [[pyprobe]] (판정 대상 후보 · 미실행) · [[daily-github-briefing-triage]] (처리 기준 · RUN_SCOPE 불가침)
- 갱신: [[degradation-degeneracy]] · [[fitting-degeneracy]] 역링크 · [[22p-physics-or-degeneracy]] · [[isc-detection-vs-balancing-masking]] Status Log
- 하지 않은 것: 26.9 설치 · PyProBE 실행 · requirements 변경 (전부 별도 승인)

## [2026-10-01] ingest | 브리핑 후속 실험 2 (사용자 승인) — PyBaMM 26.8↔26.9 실측 · PyProBE 판정 대상 실험
- raw: `raw/repositories/2026-10-01-pybamm-26.8-vs-26.9-synthetic-truth.md` (드라이버 · 비교 출력 원문 임베드) · `raw/repositories/2026-10-01-pyprobe-dma-on-synthetic-truth.md` (+ `.results.json` 160 KB)
- 격리: 버리는 venv 2 (pybamm 26.9.0.0 · PyProBE 2.6.0) · `git archive 9ca6df54` 사본 · 운영 환경 · 등록부 · 산출물 불변 · 저장소 읽기만 (grid_curves_v4 parquet)
- 갱신: [[pybamm]] (#5755 열린 물음 → 실측 2.7 mV 로 닫힘 · 상한 고정 승인 후보) · [[pyprobe]] (confidence low → medium · 실측 표) · [[22p-physics-or-degeneracy]] Evidence For + Status Log · [[fitting-degeneracy]] · [[daily-github-briefing-triage]] (결과 기록 규약 · heredoc 금지) · index 2 줄
- 하지 않은 것: requirements 변경 (RUN_SCOPE) · PyProBE 형상만 시험 · 격자 수렴 물음

## [2026-10-01] ingest | PyProBE 형상만 (용량 비제공) 시험 — np-lip 2 자유도 정리의 수치 확인
- raw: `raw/repositories/2026-10-01-pyprobe-shape-only-on-synthetic-truth.md` (출력 원문 · 손계산 대조 · 추가 함수 임베드) · 버리는 venv 재설치 · 운영 환경 불변 · 12 s
- 결과: 적합 창은 용량과 무관 · 모드는 `1 − (1 − mode)/SOH` 로 되감김 · 균일 10 % 손실 조건 → 0/0/0
- 갱신: [[pyprobe]] 표 행 추가 · [[np-lip-ocv-reparametrization]] 수치 확인 절 · [[22p-physics-or-degeneracy]] Evidence For + Status Log

## [2026-10-02] ingest | Sun, Xiong, Wang, Li, Sun 2025 — A deep learning approach for enhanced degradation diagnostics of NMC lithium-ion batteries via impedance spectra (J. Energy Chem. 107, 894–907)
- **2026-10-02 논문 세미나 3번째 논문 · 사용자 공급.** 사용자의 물음 세 가지: ① 차근차근 정리하고 다 되면 브리핑 ② 우리 열화 정량화(α·β 창 맞춤 → LLI/LAM_PE/LAM_NE)에 적용 가능한가 ③ 누락된 논문이 있는가. ⚠ `assb` 아님 — 액체 NMC/graphite (셀 형식은 원문에 없음); `assb` 번호 · 태그 · 채움표 미사용.
- raw: `raw/papers/sun2025_dl-eis-degradation-mode-diagnostics.md` (sha256 봉인 `1ba7f119…789d` · `pdf_sha256` 7b80ada4…a9b64967 · 2,296,734 B · `si_sha256` 5987ae8b…1bfc90 · 515,965 B · 둘 다 호출자 명시값과 일치) · 절별 해체 20 절 + 공백 G1–G16. 그림 `raw/figures/sun2025_dl-eis-degradation-mode-diagnostics/` 자동 21 + 수동 5 (그림 3 누락 · 표 4 개 과대 영역) — **26 개 전부 봄.** 본문 그림이 벡터라 **벡터 좌표 판독**(`[도표·벡터]`)을 했고, 그 판독이 그림 8–9 산점에서 표 2 RMSE · MAX 를 0.01–0.02 안에서 재현(12 계열 중 11).
- PDF 메타데이터: 본문 creator Elsevier · producer Acrobat DC · 작성 2025-06-30 · 수정 2025-07-24 (+05'30') · author "Yue Sun"; SI Microsoft® Word LTSC · author "杜晓伟" · 작성 = 수정 **2026-10-02 20:32 +09'00'** (업로드 직전 변환판 — 출판사 원본 형식은 이 자료로 확인 불가).
- 논문이 한 것: 24 셀(3 조건 × 8, CC 1 C·25 °C / 2 C·25 °C / 2 C·35 °C) EIS 43 점 → CNN–GRU–attention DNN 으로 LLI · LAM_PE · LAM_NE 회귀. 라벨 = 신품 1/20 C 코인셀 OCP 고정 + **1–2 C 사이클 충전 곡선에 `p0, n0, Q_PE, Q_NE, R` PSO 맞춤** (적합값 — 원문의 "ground truth"). COMSOL P2D 임피던스 1,000 개(완전 요인 0–90 %) 사전학습 → 실험 자료로만 재학습. 적합 라벨 대비 RMSE LLI · LAM_PE < 3 %p · LAM_NE < 4 %p, 기준선 대비 최대오차 42.92–66.30 % 감소(`[재현]` MAX 감소율 42.94–66.31 %).
- 판정: (a) 라벨 = 적합값 · 식별성 0 (어휘 전수 0, 합자 97 개 정규화 후) · 그림 9b 라벨 간극 6.09 → 14.40 % · 세 모드 함께 30–39 % (b) "LAM ↔ 중주파" 는 물리 발견으로도 시뮬 각인으로도 확인 안 됨 — 그려진 시뮬 64 개에서 아크 −Im 폭 ≤0.10 mΩ, 꼬리만 변함; 막 저항 · 비표면적 정의 미인쇄 (c) 주의 결과 = LLI ↔ LAM_PE 한 패턴의 부호 반전(`[재현·벡터]` r = −0.962, 43 점 상보 분할), 두 LAM 같은 대역 → LLI ↔ LAM "판단 불가" · LAM_PE ↔ LAM_NE "불성립" (d) 적용 가능성 3 층 + 값싼 실험 3 건(라벨 맞춤 식별성 · `R ↔ p0 ↔ LLI` 별칭 / 라벨 상속 / 상관을 깬 EIS) — 제안만 (e) 데이터 · 코드 공개 없음 · K-K 신품만 · 15 분 휴지 (f) 불일치 17 건 — 셋째 군 율: SI 표 S1 · 그림 10 캡션 "1 C" ↔ 본문 · 표 1–2 · 그림 1b · 1f "2 C" → **35 °C@2 C 로 판정**; 그림 1f 25 °C@2C LLI 61.6 % ↔ 그림 8a 30.9 %; GRU 시퀀스 = 주파수; R² 분모; 히스토그램 막대 폭 (g) R. Xiong 9/37 · 라벨 절차 원전 [26] 이 같은 그룹 · 19 번(wang2025)과 메타휴리스틱 창 맞춤 공유 (h) 누락 논문 표 — ★★★ [26] Tian 2021 · [21] Thelen 2022 · [34] Chen B.-R. 2022.
- 컴파일: 새 개념 0 (기존 [[piml-physics-injection-points]] ⑥ 절이 "적합 라벨 상속" 을 이미 다뤄 절 추가로 충분) · 갱신 [[piml-physics-injection-points]] (⑤ + ⑥ 실셀 사례 절) · [[interpretable-ml-battery-prognosis-taxonomy]] (주의 해석 실례 절) · [[halfcell-window-parametrization-lineage]] (행 + 일곱 번째 축 절) · [[mode-identifiability-unmeasured-lineage]] (표 행 · §10 · 계보 17 → 18편) · [[22p-physics-or-degeneracy]] (Evidence For + Status Log) · [[pvs-sev-lli-lampe-separability]] (Evidence For(H1) + Status Log) · [[mode-observability]] (Phase 3 실셀 견본) · index 5 줄 메모 + 날짜.
- 하지 않은 것: 실험 실행 · 코드 변경 (RUN_SCOPE · 위성 코드 불가침) · `mode-observability/README.md` Phase 3 반영 (위키 밖 — 호출자 몫).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 56, raw files 125).

## [2026-10-02] ingest | assb 90호 — Truong T.K., Whang G., Huang J., Sandoval S.E., Zeier W.G. 2025, Probing solid-state battery aging: evaluating calendar vs. cycle aging protocols via time-resolved electrochemical impedance spectroscopy (J. Mater. Chem. A 13, 17261–17270)
- raw: `raw/papers/truong2025_calendar-vs-cycle-aging-protocols-drt-assb.md` (sha256 봉인 7a5925bd…6dbe4162 — `pdf_sha256` 585bba0d…d5aacee2 · 1,560,581 B · `si_sha256` d0b39576…c125971b · 5,612,169 B · `data_sha256` 0f792d11…415e796e · 7,671,637 B · 셋 다 호출자 명시값과 일치 · 원자료 ZIP 은 메모리에서 읽고 커밋하지 않음 — 구조 · sha256 · 재현에 쓴 파일 이름과 결과만) · 그림 `raw/figures/truong2025_calendar-vs-cycle-aging-protocols-drt-assb/` (자동 21 = 본문 7 + ESI 14 · **연 것 21/21** · 누락 0 · 화소 판독 S4 저주파 끝(판독용 · 커밋 안 함) · 자동 크롭 과대 둘(fS1 위 본문 한 줄 "the main text." · fS3 위 S2 캡션 끝 줄) · 캡션 필드 셋(f1 십자 표지 글리프 = 인라인 이미지 · f2 줄 끝 하이픈 · fS14 수식 글리프 뒤섞임 + "References") · `figures.json` notes 21 항목).
- **2026-10-02 사용자 공급 · 파일명 번호 1 · 원장 지목 0** — 사용자 "이건 assb 관련한거야. assb로 잘 분류해서 부탁할게용" · 원장 · 위키 `Truong` · `D5TA01083G` · `calendar vs` grep 0(원장 밖 · 3차 묶음 59–89호와 별개). Univ. Münster + FZ Jülich IMD-4(교신 Zeier — 23 · 62 · 63 · 64 · 82호 공저) · CC BY 4.0 · 기사 유형 띠 "REVIEW"(내용은 1차 실험 — D10). 1차 측정 · 모형 0 — In/InLi(28.42 at%) | Li₆PS₅Cl | NCM83 : Li₆PS₅Cl 7 : 3(탄소 0) 반쪽 · 컷오프 다섯(3.7–4.1 V vs In/InLi = 4.32–4.72 V vs Li⁺/Li 인쇄) × 노화 둘(48 h 정전위 유지 "calendar" ↔ ≈48 h 1C 사이클 "cycle") · 형성 · RPT 0.1C × 3 · 시간분해 EIS → DRT(hybrid-drt) · 25 ℃ · 컷오프당 셀 하나(인쇄 0). **이 편이 우리 셋을 인용** — [11] = 9호 · [27] = 23호 · [33] = 11호.
- ★★★ **(a) calendar 의 실체 · 정규화**: 개회로 보관이 아니라 상한 정전위 유지(float) 48 h · 두 프로토콜은 명목 48 h 로만 맞춤 — `[데이터]` 상한 ±1.5 mV 체류 48.00 ↔ 0.00–0.01 h · 50 mV 안 48.0–48.2 ↔ 0.9–2.5 h · ≥3.58 V 48.7–49.3 ↔ 6.4–17.8 h · 통과 전하 ≈300 ↔ 9,006–10,154 mAh g⁻¹ · 최대 탈리튬 ≈158–169(`[도표]` S12) ↔ ≈92–104(`[재현·가정]`) mAh g⁻¹ · 그림 시간 축이 30 분 휴지(≈19–20 h) · EIS 를 뺀다(D8) — "calendar 가 훨씬 나쁘다"(인쇄 Q_loss 13.09 · 32.71 · 43.56 ↔ 1.39 · 9.80 · 9.29 %)는 같은 명목 시간 · 같은 컷오프 숫자 · 셀 하나씩 조건부.
- ★★★ **(b) 전위 기준**: In/InLi 인쇄 · Li⁺/Li 환산 +0.62 V 인쇄(출처 0) · 28.42 at% ✅ · 최대 34.08 at% · 42호 이완 띠 0.622–0.625 V 안(액체 3전극 · 실온 · 0.5 h 이완 조건) · InLi-(In) 조립(21호 — 원천 역할 미검사 · M1 · M2 ✅ · M3 ✗) · 64호 축: 이 편 3.7 V ≈ 64호 3.7 V vs In(4.3 V vs Li) · 4.0 · 4.1 V ≈ 64호 4.6 V.
- ★★★ **(c) DRT 귀속**: 문헌 τ 대역[31,33,34] + 2D 연속성뿐 · λ 수동 0(hybrid-drt 계층 베이즈 MAP · 사전 미인쇄 · K–K 통과 인쇄) · `[재현]` C_eff = τ/R — calendar 지배 봉우리 1.6–2.5 µF 평탄(τ ×5.7–35 · R ×4.2–27.6 · 3.9 · 4.1 V 48 h τ 0.19 · 0.54 s = P_A 창 안) → "P_C" 조건부 성립 · cycle P_A ≈1.5–3.3 mF(이중층 ×190–520) → "음극 CT" 가정 의존 · 1C 방전 끝 상태 표류 · 그림 6 공통 기준선(신품 산포 694–1019 Ω `[도표·화소]` S4 · 자기 셀 기준 cycle 저주파 Re −40 · −30 · −4 Ω · calendar +137 · +319 · +732 Ω) · 전형 DRT 창 밖 몫 26 % · "five main peaks" 중 P_C2 는 어깨(D13).
- ★★ **(d) 분해**: ΔV(50 % SoC) · Q_loss 는 같은 곡선 쌍의 두 수 · `[재현·가정]` 균일 분극 이동이 calendar 손실의 ≈1/8–1/3(1.5 · 7.3 · 13.4 ↔ 12.0 · 31.0 · 41.8 %) · dQ/dV 세기 ↓ = 저자 "loss of lithium inventory in the CAM"[23](검사 0) · Q7 재고 ×3.31 · 접근성 미검사 → 판정 불가 · Q1 `θ(N)` 0/90.
- ★★★ **(e) 데이터 재현**: ✅ 1C = 199.6–200.6 mA g⁻¹ · ΔV 표 · 2D DRT 색 막대 여섯 · 28.42 at% · 1.783 mAh cm⁻² · S14 막대 · ❌ 그림 2 "4.1 V calendar" RPT 9,794 표본 = 3.9 V 셀 복사(D1) · ❌ Q_loss 기준(cycle 3.9 · 4.1 V 인쇄 9.80 · 9.29 % = 첫 형성 기준 9.69 · 9.32 · 지면 정의(3번째)면 2.99 · 2.83 % — D2) · 그림 2 ↔ 3 폐합 여섯 중 셋(3.7 V 두 셀 불폐합 — D15) · 사이클 수 80 · 80 ↔ 78 · 76(D7) · ZIP = 본문 그림 1–7 · 세 컷오프(3.7 · 3.9 · 4.1 V) · SI 그림 자료 0 · 저장소 DOI 10.17879/14908422666 미열람.
- ★★ **(f)**: Q4 0/90 **여든두 번째 성질** · Q5 서른네 번째 형태 · Q6 ESI 에만 "torque of 10 Nm … ~50 MPa"(토크 환산 명목 · 본문 `pressure` 0 · `[재현]` 3.93 kN · 성형 "3 tons" ≈375 MPa `[재현·가정]`) · Q8 0.1C 곡선만. **(g)** 11호와 같은 "시간분해 DRT 노화" 형식 · 다른 귀속 근거([33] τ 불일치 — D20) · [11](9호) 둘 중 하나는 "Hartel et al." 자리의 번호 오기로 읽힘(D4) · 합성 truth 요구 R_int(t, V) · SOC 의존 분극 · 준평형 RPT · M3. **(h)** ESI 12 쪽 · 그림 S1–S14 · 표 0 · 식 1 · 참고문헌 4 전부 봄 · 본문이 S1–S14 를 전부 부른다.
- **채움표 90호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나 — C_eff 판독 저항형) · Q2 없다 · Q3 층 하나(τ 창 이름표 + 연속성 · 공통 기준선) · Q4 0/90 **여든두 번째 성질**(봉우리 이름을 문헌 τ 창으로만 · 창 넘기를 연속성으로 · 다른 상태의 시간분해 · 공통 기준선으로 산포를 효과로) · Q5 층 하나(서른네 번째 형태) · Q6 보고(ESI 에만 · 토크 환산 명목) · Q7 해당 없음(층 하나 — 재고 ×3.31) · Q8 층 하나(균일 이동 1/8–1/3).
- **곱 축퇴 처방 일흔세 번째 적용**: 부분 적용 — 1단계 ✅ 우리 `[재현]`(예치 DRT · 저자 C 0) · 2 · 3-a ❌ · 3-b ✅ 우리 적용(P_A "전하 이동" 불통과) · 4 ⚠ · calendar 저항형 · cycle P_C1 면적 증가형 서명(또는 상태 표류) · P_A 는 전제 불성립 · 처방 표 후보 줄 "DRT 봉우리별 C_eff 연속성 검사"(64호 호 정체 검사 줄의 시간 축 판 — 새 줄 아님) · 곱 문장(계면층 · 균열 · 접촉 손실을 한 P_C 에).
- ⚠ 어긋남 21 건(D1 그림 2 "4.1 V calendar" RPT = 3.9 V 복사 · D2 Q_loss 기준 · D3 공통 기준 스펙트럼 · D4 Hartel ↔ [11] · D5 [7](액체) 을 황화물 산소 종 근거로 · D6 cycle Pristine ΔV 0.16 ↔ 0.177 · D7 사이클 번호 · D8 시간 축 휴지 제외 · D9 세로 어긋남 캡션 · D10 "REVIEW" 띠 · D11 "In/LiIn" · D12 오기 · D13 다섯 봉우리 ↔ 어깨 · D14 P_A 창 진입 · D15 그림 2 ↔ 3 불폐합 · D16 before 처리 · D17 유지 사이클 방전 · D18 자료 공백 · D19 S10c 단조 · D20 [33] τ · D21 calendar 용어).
- 낱말 지문(본문 | ESI): `contact loss` 3 | 0(전부 가능성 · 인용) · `crack` 1 | 0 · `pressure` 0 | 2 · `MPa` 0 | 1 · `torque`/`Nm` 0 | 2 · `LAM` · `LLI` 0 · `lithium inventory`/`cyclable lithium` 3 · `DRT` 28 | 15 · `capacitan` 4 | 0(값 0) · `three-electrode`/`reference electrode` · `symmetric` 0 · `identif` 3(일반 뜻) · `uniq` · `uncertain` · `error` · `reproduc` · `±` 0 · `Kramers` · `Bayesian` 0 | 1 · `screen` 8 | 0.
- PDF 메타데이터: 본문 `%PDF-1.6` · Aspose.PDF for .NET 22.3.0 · 생성 2025-06-05 · **수정 2026-03-19** · XMP 3,820 B(dc:creator 5 · prism · crossmark 2025-06-5 · XMP Producer "Acrobat Distiller 8.1.0" — 정보 사전과 다름) · 개요 7 항목 전부 같은 문자열 · 10 쪽 · 그림 이미지 7 + p. 2 인라인 45×45(십자 글리프) · ESI `%PDF-1.3` · Aspose.Pdf for .NET 9.3.0 · 생성 2025-04-03(접수 뒤 · 승인 전) · 수정 2025-05-13 · XMP 237 B(빈) · 12 쪽 A4 · 이미지 14(그림 S1–S14 하나씩).
- 보류 (가)–(히) · (개)–(해) · (게) · (네) · (데): **(네)(대)(피)** 근거(강) · **(차)(루)(캐)(해)(츠)(브)(게)(오)** 근거(중) · (가)(나)(두)(러)(머)(저)(도)(므)(주)(히)(티)(너) 약 · (처) 정성 메모 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(노화 프로토콜 비교의 정규화 축 표기 · 예치 원자료의 교차 폐합 · 중복 검사 규칙 · 시간분해 EIS 의 측정 상태(· 기준선) 표기 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 90호 행 · 90편 누적 · Evidence 여든다섯 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[drt-peak-count-nonidentifiability]](일곱 번째 경보 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](일흔세 번째 적용 · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](서른네 번째 형태) · [[assb-apparent-capacity-decomposition]](90호 절 · 주장하지 않는 것) · [[assb-interphase-vs-contact-loss-attribution]](계보 90호 행 · 화살표 · 처방 6 · 8 표본 · 실험 열 편 · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](90호 절 — 토크 환산 명목 · 같은 구속의 셋째 값 · 주장하지 않는 것) · `index.md` 변경 없음(새 페이지 0 · 페이지 수 56).
- wiki 밖(호출자 몫): 원장 §1 — 이 편 받음 표시(원장 행 0 · 사용자 공급) · 새 행 후보(Hartel 2024 [13] · Zuo 2023 [15] · Schulze 2022 [7] · Huang 2023 [30] · Lu 2022 [31] · Whang 2024 [32] · Riegger 2023 [14]) · 재지목 Zuo 2021 [5] → 2 · Walther 2019 [8] → 4 · Wenzel 2018 [37] → 3 · **지목 누락** Hori 2023 *JPS* 556, 232450([34] · 11 · 90 = 2 · 원장 행 0) · Janek & Zeier 2023 [4] 은 36호 등급 없는 후속 표에만(누락으로 단정 안 함) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6 새 도착 절.
- 후속(서지 기준, 미열람): **Hori S., Kanno R., Sun X., Song S., Hirayama M., Hauck B., Dippon M., Dierickx S., Ivers-Tiffée E. 2023 *JPS* 556, 232450**([34] — 지목 누락 · 11 · 90 = 2) · **Hartel J., Banik A., Ali M.Y., Helm B., Strotmann K., Faka V., Maus O., Li C., Wiggers H., Zeier W.G. 2024 *Chem. Mater.* 36, 10731**([13]) · Zuo T.T., … Janek J. 2021 *Nat. Commun.* 12, 6669([5] — 재지목 → 2) · Zuo T., … Janek J. 2023 *Angew. Chem. Int. Ed.* 62, e202213228([15]) · Schulze M.C., … Johnson C. 2022 *JES* 169, 050531([7]) · Huang J., Sullivan N.P., Zakutayev A., O'Hayre R. 2023 *Electrochim. Acta* 443, 141879([30]) · Lu Y., Zhao C.-Z., Huang J.-Q., Zhang Q. 2022 *Joule* 6, 1172([31]) · Whang G., Huang J., Pham P.N.L., Kraft M.A., Zeier W.G. 2024 *ACS Electrochem.* 1, 249([32]) · ★ Walther F., … Janek J. 2019 *Chem. Mater.* 31, 3745([8] — 재지목 → 4) · ★ Wenzel S., … Janek J. 2018 *SSI* 318, 102([37] — 재지목 → 3) · ★ Riegger L.M., … Janek J. 2023 *Chem. Mater.* 35, 5091([14]) · ☆ Kalaga K., … Abraham D.P. 2018 *Electrochim. Acta* 280, 221([19]) · ☆ Zhu J., … Ehrenberg H. 2020 *JPS* 448, 227575([23]) · ☆ Jeong W.J., … McDowell M.T. 2024 *ACS Energy Lett.* 9, 2554([35]) · ☆ Vishnugopi B.S., … Mukherjee P.P. 2023 *Adv. Energy Mater.* 13, 2203671([36]).

## [2026-10-02] ingest | Zhang W., Zhang N., Wang Z., Li A.-M., … Wang C. 2026 — Mechanistic understanding of interphase-driven ageing in silicon anodes (Nature Energy 11, 558–570)
- **2026-10-02 논문 세미나 1번째 논문 · 사용자 공급**(업로드 파일명 번호 "1" — 사용자 "이건 오늘 논문세미나 하면서 받았던거야. 첫번쨰논문이고 관련해서 논문에이전트 진행해줘"). ⚠ `assb` 아님 — 액체 전해질 Si 음극 CR2032 반쪽전지(Li 상대극) + µ-Si/n-Si ‖ NMC811 풀셀 · `assb` 번호 · 태그 · 채움표 · 원장 미사용 · `pack-fault` 태그도 안 붙임(열화 기구 페이지 — SCHEMA 경계 ②) · `assb` 60 · 88 · 89 · 90호는 비교 링크만.
- raw: `raw/papers/zhang2026_si-anode-interphase-calendar-ageing.md` (sha256 봉인 00bfbc9d…f7fddc51 · `pdf_sha256` ca59e5ea…89d4e143 · 2,520,259 B · `si_sha256` f5445c81…ebde6b03 · 4,825,975 B · `zip_sha256` 6065fdba…0e3a · 11,489,903 B · xlsx 다섯 sha256 은 `source_url_note` — 전부 호출자 명시값과 일치(직접 재계산) · 원자료 xlsx 는 `zipfile` + XML 로 읽고 커밋하지 않음). 판정 먼저 · 서지 · 공백 G1–G16 · 보충 자료 대조 · 그림 · 절별 해체 · (a)–(h) · 재현 정리 · 어휘 · 참고문헌 · 인용 대조 · 어긋남 D1–D22 · 후속 26 행. 그림 `raw/figures/zhang2026_si-anode-interphase-calendar-ageing/` **자동 42 + 수동 8 = 50 — 전부 봄**(본문 7 장 중 자동 누락 둘(그림 1 · 4) · 부분 크롭 다섯 → 본문 7 장 전부 수동 · SI S32 A–D 수동 · 자동 본문 부분 크롭 다섯과 S28–S30 은 축소 몽타주로 봄).
- PDF 메타데이터: 본문 `%PDF-1.4` · creator Springer · author "Weiran Zhang" · subject "Nature Energy, doi:10.1038/s41560-026-01967-1" · 생성 · 수정 2026-04-23(+05'30' — 권호 인쇄판) · 13 쪽; SI `%PDF-1.7` · Adobe InDesign 17.4 · 생성 · 수정 2026-01-28(온라인 공개 6 일 전) · 51 쪽 Letter. Received 2024-04-24 · Accepted 2025-12-31(616 일) · online 2026-02-03 · 라이선스 "under exclusive licence to Springer Nature"(CC 아님) · 동료 심사 McBrayer(refs 16 · 25 · 30 의 제1저자).
- 논문이 한 것: Li ‖ Si 0.06 V 180 h 정전위 유지(15 형성 뒤 · 온도 인쇄 0) · 네 전해질(LiF-rich ↔ organic-rich) × µ-Si/n-Si · 지표 넷(1 − cCE · 1 − caCE · active = 1 − QD1/QD · leakage@180 h) · XPS · TEM · EQCM · KPFM · DFT · EIS → "SEI cracking + dissolution 이 달력 · 사이클 노화를 함께 지배 · 용해 지배가 아니면 calendar 와 cCE 가 양의 상관" · 풀셀 µ-Si/n-Si ‖ NMC811 개회로 1 달 + USABC 식 OCV-RPT 로 "검증".
- 판정: (a) 반쪽전지 음극 저전위 정전위 유지 · A Ah⁻¹ = QD 정규화 · 원전 refs 27–29 중 "SCP Protocol paper" = Schulze 2022 *JES* 169, 050531 · 상대극 산화 · 교차는 SI Note 2 + 도식으로 "기여 없음" 주장(측정 0) (b) cracking ↔ dissolution 분리는 **지표 정의 + 순위 상관**(용해 직접 측정 0) · 상관 n = 4 · `[재현]` r = 0.995 · 정확 순열 p = 1/24 · 1 − caCE 안에 1 − cCE 11–27 % 내장(빼도 r = 0.991) (c) active = LAM_Si 는 증명 안 됨 — S24 평균 전압 −3.4 ~ −12.9 mV · 균일 이동이면 컷오프 용량 1.7–6.5 % `[재현·가정]` ↔ 인쇄 active 0.87–3.40 % 같은 자릿수 · 정의상 µ-Si 보관 손실의 33–62 % 가 LAM_Si 쪽 · 풀셀 분해 0 (d) ✅ 그림 6d 98.99 · 96.41 · 93.43 · 90.10 % = **µ-Si ‖ NMC811 · LiPF6-이온성 액체 · 37.43 · 70.52 · 102.69 · 134.79 일 · 온도 인쇄 0**(다섯째 166.67 일 83.95 % 미언급) · QL 적분 = S7 · 4C = ∫4B · BET ×19.23 · ❌ 그림 5a EC = 표 S2 R_SEI-Li · ❌ 6B/6C 이름표 THF/MTHF ↔ IL · 원자료 없는 그래프 3C · 6A (e) 90호와 같은 원전 둘(Schulze 2022 · Kalaga 2018) · 전극 · 전위 · 지표 · 결론 층위는 반대 끝 (f) MSC 혼동의 근거가 된다 — 정상 유지 전류 0.088–0.250 mA/Ah · 늦은 꼬리 t⁻⁰·¹⁴–t⁻⁰·⁷³ · 잡음 ≈ 평균 · 180 h 누적의 59–82 % 가역 · 풀셀 회복분 3.0–10.2 pp/월 · 셀 간 산포 ≤10.7 pp (g) SI 51 쪽 전부 · 본문이 S1–S35 · Note 1–8 · 표 1–2 전부 부름 · SI 참고문헌 71–73 목록 없음 (h) 후속 ★★★ 다섯.
- ⚠ 어긋남 22 건(D1 그림 5a EC 막대 = 표 S2 R_SEI-Li · D2 풀셀 "LiF-rich" 이름표 THF/MTHF · IL SEI 미측정 · D3 S12 이름표 93.8 → 87.6 % 두 번 · D4 "comparable to Gr" ↔ 자료 9–12 pp 차 · D5 로그 축이 ≤0 점(셀당 107–4,877)을 숨김 · D6 Note 6 98.8 ↔ S21 98.4 % · D7 S19 패널 뒤바뀜 · D8–D10 SI 캡션 단위 · 패널 · D11 Note 7 ↔ S22B · D12 S26 Li₂CO₃ CBM · D13 KPFM 2.39 ↔ 2.373 V · D14–D22 이름표 · 머리 · 오기 · 참고문헌).
- 컴파일: 새 개념 [[potentiostatic-hold-current-attribution]](유지 전류 = 가역 이완 + 부반응 + 단락 · 표본 둘(이 편 · 90호) · 단락의 부호는 셀 구성에 따라 다르다 `[해석]` · MSC 문서 P3 · P7 연결) · 갱신 [[isc-detection-vs-balancing-masking]](Evidence — H2 쪽 셀 화학 근거 · Status Log · 관련 · sources · evidenceScope multi-source-primary · 채움표 행 없음) · [[thermo-kinetic-loss-partition]](함정 5 — 저율 한 전류 CC 용량 = ΔE + η · sources · evidenceScope) · index 1 줄 + 전체 페이지 57.
- 하지 않은 것: [[mode-identifiability-unmeasured-lineage]] 계보 수(18편) 변경 안 함(분해 도구가 OCV 곡선이 아니라 반쪽전지 쿨롱 장부 — digest 어휘 절에 이유) · [[22p-physics-or-degeneracy]] · [[pvs-sev-lli-lampe-separability]] 근거 없음 · wiki 밖(`bms-balancing/docs/MSC_SEMINAR_2026-09-23_APPLICATION.md` · `NEW_MODEL_REQUIREMENTS.md` §3 C3 · C6) 미수정 — 호출자 몫.
- `raw/figures/_sources.json`: 이 편 항목(50) 추가 · sun2025 항목 21 → 26(도구가 색인을 다시 쓰며 실제 `figures.json` 항목 수로 바로잡음 — 지난 수동 크롭 뒤 미갱신분).
- 후속(서지 기준, 미열람): **McBrayer J.D., Harrison K.L., Allcorn E., Minteer S.D. 2023 *Front. Batteries Electrochem.* 2, 1308127**([30] — "chemical > mechanical", 이 편과 반대 방향) · **McBrayer J.D. et al. 2021 *Nat. Energy* 6, 866**([16]) · **Schulze M.C. et al. 2022 *JES* 169, 050531**([29] — 90 · 이 편 = 2) · **Kalaga K., Rodrigues M.-T.F., Trask S.E., Shkrob I.A., Abraham D.P. 2018 *Electrochim. Acta* 280, 221**([26] — Si–흑연 · 90 · 이 편 = 2) · **Verma A. et al. 2023 *JES***([49] — blended Si–흑연 유지 · 권 · 쪽 미인쇄).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 127).

## [2026-10-02] ingest | assb 91호 — Danilov D., Niessen R.A.H., Notten P.H.L. 2011, Modeling All-Solid-State Li-Ion Batteries (J. Electrochem. Soc. 158(3), A215–A222)
- raw: `raw/papers/danilov2011_thin-film-assb-model-weak-electrolyte-parameter-fit.md` (sha256 봉인 e32b93d3…26b46829 — `pdf_sha256` e00bb986…419a105c · 1,137,644 B · 호출자 접두 `e00bb9869bd275eb` 일치 · SI 없음(원문에 보충 언급 0 — 직접 다시 셈) · 예치 원자료 0) · 그림 `raw/figures/danilov2011_thin-film-assb-model-weak-electrolyte-parameter-fit/` (자동 12 = `fig_1 … fig_12`(SI 오판 0 — 눈으로 확인) + **표 I · II 수동 렌더 2**(표 캡션 미인식) · **연 것 14/14** · 누락 0 · 크롭 잘림 · 과대 0 · 캡션 필드 괄호 자리 제어 문자 U+0001/U+0002(원 글꼴) · 그림 2–8 · 11 · 12 는 **PDF 벡터 경로**(쪽 4–9 래스터 0)를 눈금 숫자 중심으로 보정해 읽음 · 그림 1a 화소 판독 · 그림 7 가로 ×8 확대 렌더 — 판독 배열 · 재풀이 · CRB 코드는 `scratchpad` 에만 · 커밋 안 함). `raw/figures/_sources.json` 은 추출기 재집계로 이 편 항목 추가 + `sun2025_dl-eis-degradation-mode-diagnostics` 그림 수 21 → 26(그 폴더 실물 26 = 자동 21 + 수동 5 — 부수 효과 · 값은 실물과 일치).
- **4차 묶음 파일 51**(원장 §1 요청 14 편 중 첫 편 · 2026-10-02 사용자 공급 "이것도 논문 받아둬서 논문에이전트 진행하게") · 원장 행 "★★★ … 12 · 26 | 2 | Q4" · Eindhoven 공대 + Philips Research(Notten) · © ECS(오픈 액세스 0) · 첫 쪽 = IOP 내려받기 표지(인쇄 A215–A222 = PDF p. 2–9 · PageLabels 한 칸 밀림). 평면 박막 Si/TiO₂/Pt | LiCoO₂ 320 nm | Li₃PO₄ 1.5 µm | Li 금속(증착 미기재) · 공칭 10 µAh · 1 cm² · 1.6C CCCV + 1.6–51.2C 방전 여섯 · 25 ℃ · 셀 하나 · 1D 모형(BV + Fick + 해리 이원 SE · 식 22).
- ★★★ **(a) 매개변수 추정의 실체**: 표 II 12 행 = 설계 3(L · M · A — 본문 "determined by SEM" ↔ 그림 1a 띠 비 ≈0.97 · 축척 0 = 예시 셀) · NDP 측정 1(a₀ 6.01×10⁴) · 용량 유도 1(a_max — `[재현·가정]` 10 µAh ÷ (F·0.5·M·A) = 23.32 kmol m⁻³ ✅ · 조밀 LiCoO₂ 의 45 % `[재현·외부 값]`) · **적합 7**(k_r · δ · D_Li⁺ · D_n⁻ · D_Li · α · k₁ˢ — 손실 · 알고리즘 · 잔차 · 불확실성 인쇄 0) · 식별성 어휘 전수 0(NFKC 전후 · `fit` 만 0 → 1 합자) · "agree" 9 · **평형 전압 = 같은 곡선 네 율(1.6–12.8C) 회귀 외삽** — `[재현]` 붉은 점 11 개 ±2 mV · ±0.0015 µAh cm⁻² · 선형 ↔ 2차 Q 9.25 · 9.5 에서 10 · 28 mV · 가파른 끝 0.06 µAh cm⁻² · 25.6 · 51.2C 버림(이유 0).
- ★★★★ **재풀이**: `[재현]` 표 II 그대로 전해질 부분계(식 18–20)를 풀면 그림 8a · 11 · 12 가 안 나온다(51.2C η_mt 15 · 30 · 50.4 · 64.9 s −76 · −103 · −149 · −226 ↔ 지면 −70 · −86 · −101 · −109 mV · RMS 64 mV · 정상 한계 ≈257 µA cm⁻² < 512) · **k_r 하나만 ×100(≈0.90×10⁻⁶)** 이면 RMS 0.8 mV · 확산 / 이동 −43.5 / −65.6 ↔ −43.3 / −65.5 · 그림 12 농도 ±0.05 kmol m⁻³ · 3.2C 과도 ±0.1 mV(×95–×110 ≤2.0 mV · 다른 조합 미검사 — 유일성 주장 안 함) · 26호 "문헌값" 8.00×10⁻⁷ 과 같은 자릿수 · 본문 A221 에도 같은 0.9×10⁻⁸.
- ★★★ **k₁ˢ**: 단위 m^2.8 mol^−0.6 s^−1 = α 0.6 판(`[재현]` 차원 ✅ · 표 I k₋₁ "mol⁻⁴" 오기) · 인쇄 단위 i₀ 151 A · kmol 2.39 mA · mol cm⁻³ 0.38 mA ↔ 그림 8 이 요구하는 0.91–1.04 mA — 어느 관례도 불일치 · "50–100 Ω" 은 η_ct/I(26–66 Ω cm²) 쪽 자릿수(문장 주어 "total" 은 357–419).
- ★★★★ **율별 끝 용량**: `[도표·벡터]` 그림 7 측정 = 그림 2 와 같은 3,177 점 · 모형 3.0 V 도달 1.01 · 2.24 · 4.52 · 9.25 · 18.71 ↔ 측정 1.32 · 2.46 · 4.83 · 9.47 · 18.76 분 · 우리 전 셀 재풀이(k_r ×100 · i₀ 1 mA · E_eq = 그림 3 녹색)가 모형 선을 ±0.075 분 · 그림 8b 끝 0.840 분으로 재현 → **모형 = 측정의 73–78(51.2C) · 90 · 94–96 · 98 · 99 %** — "good agreement … for all discharge currents" 는 65 분 축 · 표지 지름 ≈0.81 분 속 시각적 일치(D3) · 1.6C 그림 없음(D4) · 같은 51.2C 모의 ≈50 s(그림 8b · 12) ↔ 1.08 분(그림 11)(D5).
- ★★★ **(c) 물리**: n⁻ = "nBO 에 묶인 미보상 음전하"(`vacanc*` 0) · D_n⁻ 5.10 > D_Li⁺ 0.90 → t₊ 0.15 ↔ "conductivity … Li⁺ ions only"(D15) · "전해질 절반 이상" = 모형 출력(독립 측정 0) · `[재현·가정]` 같은 σ 단일 이온이면 그림 11 끝 −108.7 mV 중 ≈71 % 소거 · `[재현·벡터]` η_mt 몫 시간 평균 45 %(51.2C) · 46 %(3.2C) · ≥ ½ 은 51.2C 0.49 분부터(초록 조건 탈락 D6) · 이중층 0(37호 물음 — 항 없음 · 37호 c_dl 5.1×10⁻⁶ F 와 k₁ˢ 5.1×10⁻⁶ 숫자 일치는 단서로만) · σ 2.44×10⁻⁶ S cm⁻¹ · 순수 옴 강하 31.5 mV ↔ "40 mV"(D7).
- ★★ **(b) 26호 계보**: 같은 이름 아홉 중 같은 값 0 · a₀ 1.7 % · D_e⁻ 없음(양극 단일 Fick · 이동항 무시) → 10 자릿수 표류는 이 편에서 시작 안 함 · 시작되는 것 = 인쇄 자릿수(k_r) · 단위 관례(k₁ˢ) · 용량 맞춤 a_max · "일치" 관행.
- ★★ **우리 국소 CRB**(`[재현·가정]` 재풀이 모형 · σ_V 1 mV · 여섯 율 · 2–85 % · ln θ): 전해질 넷 |ρ| ≥ 0.98(δ–D_Li⁺ −0.999) · 조건수 9.5×10⁵ · 최약 방향 D_Li⁺ −0.74 · δ +0.41 · k_r −0.40 · D_n⁻ −0.36 · D_Li ×1.005 · α ×1.03 · i₀ ×1.10 — "18 % mobile" 은 골짜기 위의 점 · 저자 분석 아님.
- ★★ **(d) 이식**: 넘길 것 = 과전압 골격 · 율 외삽 방법 + 모형 의존 폭 · 재풀이 검사 · CRB · 경고(a_max 가 θ · ε 를 삼키는 자리 = A1 축퇴의 박막판) / 못 넘길 것 = 값 전부 · 이원 SE · 조밀 평판(A1 자리 0) · Li 금속 무한 원천(A2 · A3 · M1–M3 자리 0) · 열화 · 이중층 · 압력 0.
- **채움표 91호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(`θ(N)` 0/91 · 층 하나 — A·k₁ˢ 곱 · 용량 맞춤 a_max) · Q2 없다 · Q3 층 하나(각주 셋 첫 표 · 인쇄 값 ×100 · 외삽 평형 곡선 · 용량 맞춤 유효값) · Q4 0/91 **여든세 번째 성질** · Q5 해당 없음(층 하나 — 음극 과전압 0 가정) · Q6 해당 없음(증착 압력만) · Q7 해당 없음 + 공백(Li 증착 미기재 · 마지막 층 Co 150 nm) · Q8 층 하나(율 외삽 평형 곡선).
- **곱 축퇴 처방 일흔네 번째 적용**: 1 · 3-a · 3-b · 4단계 ❌ · 2단계 ⚠(평판 = 면적을 아는 계면 · i₀ ≈1 mA cm⁻² 재료) · 율 스윕 ✅ 있으나 정적 ↔ 동적에 씀 · J^T J = 우리 CRB · 곱 문장 F·A·k₁ˢ · 용량 맞춤 a_max — 새 줄 0.
- ⚠ 어긋남 18 건(D1 SEM 예시 셀 · D2 30 min 휴지 그림 없음 · D3 고율 끝 용량 · D4 1.6C 없음 · D5 51.2C 모의 두 길이 · D6 초록 조건 탈락 · D7 40 ↔ 31.5 mV · D8 표 I 단위 오기 둘 · D9 [1] 연도 · D10 "Fig. 5" · D11 "total" ↔ η_ct · D12 k_r ×100 · D13 k₁ˢ → i₀ · D14 설계 ↔ SEM · D15 "Li⁺ only" ↔ t₊ 0.15 · D16 · D17 캡션 · D18 표 머리).
- PDF 메타데이터: `%PDF-1.4` · creator "XPP" · producer "Acrobat Distiller 6.0.1 (Windows); modified using iText® 5.5.13.5 ©2000-2026 iText Group NV (IOP Publishing Ltd; licensed version)" · 생성 2010-12-28 12:16:00Z · 수정 2026-10-02 13:41:27 +01:00(IOP 내려받기 — 표지 시각과 같음 · IP 는 옮기지 않음) · title · author · subject · keywords 빈 값 · XMP 3,349 B · PageLabels 1–9 · 래스터 4(p. 1 IOP 로고 · 광고 · p. 2 머리 장식 · p. 3 그림 1a) · "µ" 는 MathematicalPi-One 의 U+0001(텍스트 층).
- 보류 (가)–(히) · (개)–(해) · (게)–(베): **(치)(이)** 근거(강) · **(주)** 근거(중) · (대)(가)(차)(무)(루)(메)(다) 약 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷(인쇄 매개변수 표의 재풀이 폐합 검사 · 속도 상수의 i₀ 환산 표기 · 모형 "일치" 의 율별 끝 용량 잔차 표기 · 평형(OCV) 곡선의 출처 층위 표기 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 91호 행 · 91편 누적 · Evidence 여든여섯 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](일흔네 번째 적용) · [[assb-sensitivity-sweep-vs-identifiability]](91호 절 · 후보 처방 — 결정 대기) · [[spm-grouped-parameter-identifiability]](91호 행 둘) · [[constrained-crb-identifiability]](적용 — ASSB 원형 모형 첫 국소 FIM) · index 불변(새 페이지 0).
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행(✅ 91호 흡수 · **지목 칸 정정 "12 · 26 | 2" → "26 | 1"** — 12호는 본문 재인용 셋 · 후속 절 0) · 재지목 Danilov & Notten 2008 [27](26 → 26 · 91 = 2 · 파일 61) · 새 행 여섯(★★ Pop 2008 책 [31] · ★★ Iriyama 2005 [18] · ★★ Yamada 2007 [19] · ★ Munichandraiah 1998 [17] · ★ Xie 2007 [32] — 파일 62 와 다른 편 · ★ Sato 1997 [33]) · ☆ 행 없음(Bates [14,15] · Danilov & Notten 학회 [12,13] · Atlung · McKinnon · Kang–Ceder · weak electrolyte [22–25]) · 지목 누락 0 · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 51 행.
- 후속(서지 기준, 미열람): **Danilov D., Notten P.H.L. 2008 *Electrochim. Acta* 53, 5569**([27] — 재지목 · 파일 61 로 도착 · 처리 대기) · **Pop V., Bergveld H.J., Danilov D., Regtien P.P.L., Notten P.H.L. 2008 *Battery Management Systems: Accurate State-of-Charge Indication for Battery-Powered Applications*(Philips Research Book Series Vol. 9, Springer)**([31]) · **Iriyama Y., Kako T., Yada C., Abe T., Ogumi Z. 2005 *JPS* 146, 745**([18]) · **Yamada I., Iriyama Y., Abe T., Ogumi Z. 2007 *JPS* 172, 933**([19]) · Munichandraiah N., Scanlon L.G., Marsh R.A. 1998 *JPS* 72, 203([17]) · Xie J., Imanishi N., Hirano A., Matsumura M., Takeda Y., Yamamoto O. 2007 *SSI* 178, 1218([32]) · Sato H., Takahashi D., Nishina T., Uchida I. 1997 *JPS* 68, 540([33]) · 교차 참조(지목 아님): Raijmakers 2020(파일 58) · Kim 2019(파일 59).

## [2026-10-02] ingest | Oney, Monaco, Mitra, Medjahed, Burghammer, Karpov, Mirolo, Drnec, Jolivet, Arnoux, Tardif, Jacquet, Lyonnard 2025 — Dead, Slow, and Overworked Graphite: Operando X-Ray Microdiffraction Mapping of Aged Electrodes (Adv. Energy Mater. 15, e02032)
- **2026-10-02 논문 세미나 2번째 논문 · 사용자 공급**(업로드 파일명 번호 "2" — 사용자 "이게 두번째 논문이야" · 보충 영상 S1–S4 는 같은 날 추가 "여깄어 이거로 받아"). ⚠ `assb` 아님 — 액체 흑연 ‖ LFP–NCA(90/10 w%) 대형 원통 원소 셀(점검 용량 유지 70 % = 손실 30 %)에서 뗀 노화 흑연 · `assb` 번호 · 태그 · 채움표 · 원장 미사용 · `pack-fault` 해당 없음 · `assb` 74 · 76 · 78 · 79 · 80호는 비교 링크만(digest §비교).
- raw: `raw/papers/oney2025_dead-slow-overworked-graphite-operando-microxrd.md` (sha256 봉인 3f3e3b85…2d0d438b · `pdf_sha256` d8324b03…a0ec348 · 2,963,106 B · `si_sha256` 749dbdd6…cfec1ef192 · 2,474,413 B · `video_s1..s4_sha256` 442f872d… · d1563f00… · 9d6ddbec… · 6a2babb2… — 여섯 다 호출자 명시값과 일치(직접 재계산) · 영상 원본 · 전체 프레임 커밋 안 함). 판정 먼저 · 서지 · PDF 메타데이터 · 공백 G1–G18 · 보충 자료 대조 · 그림 · 절별 해체 · (a)–(g) · (f-2) · 어휘 · 참고문헌 · 인용 대조 · 어긋남 D1–D32 · 비교 · 후속. 그림 `raw/figures/oney2025_dead-slow-overworked-graphite-operando-microxrd/` **자동 28(본문 8 · 표 1 · SI 19) + 영상 판정 프레임 10 = 38 · 연 것 38/38** · 누락 0 · 자동 크롭 문제: 표 1 크롭이 p.10 전체(과대 — 자동 파일 유지) · caption 필드 900자 상한 11 항목 · Wiley 꼬리말 섞임 0 · `figures.json` notes 38 · 영상 프레임은 폭 900 px JPEG(합 0.68 MB, 출처 · 프레임 번호 · Selected Time · 추출 방법 기록). `raw/figures/_sources.json` 이 편 항목(38) 추가(도구 함수로 재생성 — 다른 항목 변화 0).
- PDF 메타데이터: 본문 `%PDF-1.6` · LaTeX/hyperref → Acrobat Distiller 25.0 + iText 4.2.0(1T3XT) · 작성 2025-09-17 · **수정 2026-09-27** · XMP crossmark 2025-08-21 · VoR · 17 쪽 · 개요 17(2.2 절 글리프 깨짐) · 2–17 쪽 텍스트 층 다운로드 워터마크 · 합자 222; SI `%PDF-1.7` · Word LTSC · author "ONEY Gozde" · **작성 = 수정 2026-10-02 20:31 +09:00** · 20 쪽 A4 · 이미지 19 = 그림 S1–S19 · **표 S1 없음**. 영상 AVI H.264 4 fps · 226 · 235 · 245 · 246 프레임(파이프 디코딩으로 재확인).
- 논문이 한 것: 원소 셀(C/2 CC–CV 3.8 V / C/2 → 2.5 V · 하루 4 · 24 사이클마다 C/3 점검 · 20 °C · ≈3000 사이클)에서 뗀 흑연을 코인 · 반쪽전지 · 3 mm Swagelok operando 셀 둘(ID13 3 × 3 µm · ID31 20 × 8 µm)로 — operando µXRD 지도(깊이 3 µm × 가로 100 µm)를 C/5 → C/2 → C/2 충전 · C 방전으로 돌려 **시간에 안 변하는 회절 성분 = 비활성**(4D 최소 필터) · 율속 ↑ 로 늘어나는 몫 = "slow" · 남는 몫 = "dead" · 비활성이 x = 0–1 여러 stage · 분리막 쪽 집중("overworked" 가설) · 활성분 반응이 거시 → 미시 불균일로. 모형 0(선형 회귀 하나).
- 판정: (a) 셀 · 이력은 인쇄로 선다 — 제조사 · 정격 0 · 해체 전 "SOC 0 %" ↔ S4 "1.5 V" · 표 S1 없음 (b) **dead/slow 는 정의(시간 최소 필터 + 율속 차이)** — slow = +10 %p(셀 둘 `[재현]`) · dead = C/5 값(상한) · 되돌아오는 저율 0 → 율속과 순서가 섞인다 · 같은 편 LAM_NE 가 ≈19 %(완전지 DVA `[재현]`) · ≈55 %(반쪽전지 DVA `[재현]`) · 34–57 %(operando) · 39 ± 8 %(논의 — `[재현·가정]` 셀 1 · 2 전체 사이클 평균 · 표본 SD)로 갈리는데 "consistent, albeit different in value" 로 닫음 · 최종 평탄 > 흑연 손실 ✅(33 ↔ 18.8 %) 이나 XRD 다리(FP 40 %)는 그림대로면 안 섬 (c) **li : de ≈1 : 1(셀 1) ~ 2 : 1(셀 2)(질량)** · `[재현·가정]` 갇힌 Li x ≈0.06–0.11 ≈0.17–0.33 mAh cm⁻² ≈ 용량 손실의 17–39 % · 점유율 **z_eff ≈0.17–0.25** · 이 편은 리튬화 비활성을 LAM 으로 세고 Li 몫은 정성만 · `[해석]` 1m: 실셀의 멈춘 흑연 = li · de 혼합, `{LAM_NE,de = δ, LLI = z_eff·δ}` — "계수 = 제거 때 점유율" 을 실셀 숫자로 지지(시험 아님) (d) (i) 점검 전류 의존 LAM_NE — 측정 · (ii) OCP 모양 — 반쪽전지 C/20 ICA 봉우리 자리 그대로(측정), 운용 전류 겉보기 곡선에서만 깨질 수 있음(추론) · (iii) LLI ↔ LAM_NE 결합 — 측정 + 재현·가정 (e) ✅ 율속 ↔ 전류(명목 0.169 mAh · 2.39 mAh cm⁻² · 노화 셀 실효 0.37 · 0.93 · 1.87 h⁻¹) · 73 % · 18.8 % · 표 1 합 · 부분집합 · x ≈0.1(LiC₁₂ 가정에서만) · ❌ x = 0.83 · 0.54 같은 규칙으로 안 맞음 · Q_th 미인쇄(그림 6a 역산 ≈3.0 mAh cm⁻²) · ❌ **SI S4 FP 39.7 % ↔ 그림 화소 ≈7–12 %** (f) SI 20 쪽 · S1–S19 전부 · 표 S1 없음 · 본문이 S11 · S18 · S19 안 부름 · SI 교차참조 여섯 곳 두 칸 밀림 (f-2) **S1–S2 = 노화 셀 1 · S3–S4 = 신품 — 본문 문장과 반대** · 프로토콜이 본문보다 길다(노화 5 사이클 · ≈4.9 h 휴지 · C/2–C 세 번 / 신품 4 사이클; 3.8 V 유지 0.22–0.7 h · 2.5 V 유지 0–0.19 h) · 첫 C/2–C 는 두 셀 다 지도 없음(= 그림 3d 평탄 띠) · 그림 6b/c = S3/S4 프레임 55(5.6 h) · S1/S2 프레임 33(3.5 h) · 영상에서만 `[도표·화소]`: 휴지 ≈4.9 h 에서 갇힌 Li 형태 불변(좌우 차 0.081 → 0.080) · C 방전 끝 집전체 쪽 지연이 2.5 V 유지에서 회수(노화 −0.050 ↔ 신품 −0.027) · 방전 끝 x 가 순서를 따라 0.105 → ≈0.15 로 쌓임 · 신품 분리막 쪽 진폭 ×1.04–1.05 · 노화 ×0.56 (g) ★★★ 여섯(아래).
- ⚠ 어긋남 32 건(D1 영상 대응 · D2 FP 39.7 % ↔ 7–12 % · D3 그림 4a 구역 4 캡션 · D4 프로토콜 · 유지 · D5 그림 3d 공백 · D6 S9 ×0.90 · D7 x 쌍 · D8 101 % · D9 "in-plane (x-axis)" · D10 "up to 11%" · D11 n 9 ↔ 6 · D12 15 mm ↔ 1.6 cm · D13 2.5 ↔ 2 µL · D14 2.25 ↔ 2.45 · D15 형성 컷오프 · D16 stage 3 "briefly" · D17 참고문헌 번호 · 이름 · [18] 미인용 · D18 SI 교차참조 · D19 단위 · D20 S10 구역 2 · D21 S3 ↔ 그림 2a · D22 SI 문단 중복 · D23 (100) ↔ (001) · D24–D25 SI 방향 서술 · D26 지도 범위 · D27 LiC₁₈/LiC₁₂ 순서 · D28 S2 끝 전압 · D29 깊이 축 부호 · D30 S19 캡션 · D31 fly scan 길이 · D32 해체 전 상태).
- 낱말 지문(본문 | SI): `identifiab*` · `degenera*` · `uniqu*` 0 | 0 · `uncertain*` 3 | 0(일반 뜻) · `error bar` 1 | 0 · `LAM` 2 · `LLI` **0** · `LCL` 6 · `trapp*` 10 · `inactiv*` 99 | 26 · `dead` 6 | 1 · `slow*` 17 | 2 · `heterogene*` 52 | 11 · `PyBaMM/P2D/DFN/Newman` 0 · `threshold` 0 | 2(값 0).
- 컴파일: 새 페이지 0 · 갱신 [[thermo-kinetic-loss-partition]](함정 6 — 율속 의존 겉보기 LAM · sources · 관련) · [[birkl-ocv-degradation-diagnostic]](새 절 "li/de 몫을 OCV 밖 관측으로 잰 실셀 값" · sources · 관련 · updated 2026-09-03 → 2026-10-02) · [[22p-physics-or-degeneracy]](Status Log — Evidence 변화 없음, 라벨 전류 축이라는 외적 타당도 경계 · sources) · [[mode-identifiability-unmeasured-lineage]](Thesis 18 → 19편 · §1 표 19 번째 행 · Argument §11 · 관련 · sources) · [[mode-observability]](Phase 1m 의 실셀 입력 줄 · sources) · `index.md` 해당 넷 줄에 2026-10-02 덧말(페이지 수 57 그대로).
- 하지 않은 것: [[pvs-sev-lli-lampe-separability]] — LFP 양극이 안정한 셀이라 LLI ↔ LAM_PE 근거 없음 · [[halfcell-ocp-shape-invariance]] · [[dv-peak-heterogeneity-descriptor]] — 근거가 "대조하지 않았다" 수준이라 digest §(d) · §비교에만 · 새 개념 페이지("율속 의존 겉보기 LAM")는 만들지 않음 — 함정 6 으로 기존 개념에 들어가면 충분(ΔE/η 의 LAM 판).
- wiki 밖(호출자 몫): `mode-observability/README.md` Phases 표 1m 행 · `docs/PHASE1M_NOTES.md` "다음" 둘째 항에 실셀 점유율 메모(z_eff ≈0.17–0.25 — 조건부) · `degradation-degeneracy/docs/RESULTS.md` "이 결론이 말하지 않는 것" #48(운용 범위 한 점)에 "실셀 라벨의 율속 의존" 참조 — 둘 다 수정 안 함(RUN_SCOPE 밖 문서지만 이 작업의 범위 밖).
- 후속(서지 기준, 미열람): **Li D., Danilov D., Gao L., Yang Y., Notten P.H.L. 2016 *Electrochim. Acta* 210, 445**([15] — 율속 의존 비활성의 인용 근거) · **Mikheenkova A. et al. 2024 *JPS* 599, 234190**([12]) · **Klett M. et al. 2014 *JPS* 257, 126**([8]) · **Waldmann T., Ghanbari N., Kasper M., Wohlfahrt-Mehrens M. 2015 *JES* 162, A1500**([17]) · **Tardif S. et al. 2021 *J. Mater. Chem. A* 9, 4281**([20] — 방법 원전) · **Lewerenz M., Marongiu A., Warnecke A., Sauer D.U. 2017 *JPS* 368, 57**([5] — kim2023 · dv-peak 인용, 재지목 → 2) · ★★ Dufour 2018 *EA* 272, 97 · Scipioni 2018 *EA* 284, 454 · Rauhala 2018 *J. Energy Storage* 20, 344 · Finegan 2020 *EES* 13, 2570 · Safari & Delacourt 2011 *JES* 158, A1123 · Dubarry 2011 *JPS* 196, 10336(재지목 → 2) · Petz 2024 *Batteries* 10, 68 · Ko 2025 *Small* 21, 2410795 · Smith 2023 *JPS* 573, 233118.
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 128).

## [2026-10-02] ingest | assb 92호 — Firouz Y., Goutam S., Cazorla Soult M., Mohammadi A., Van Mierlo J., Van den Bossche P. 2020, Block-oriented system identification for nonlinear modeling of all-solid-state Li-ion battery technology (J. Energy Storage 28, 101184)
- raw: `raw/papers/firouz2020_hammerstein-wiener-multisine-bla-nonlinearity-assb.md` (sha256 봉인 9c3b54aa…622c46f6 — `pdf_sha256` 9cf5d53f…2a9f7449 · 6,118,709 B · 호출자 접두 `9cf5d53f1aea0281` 일치 · SI 없음(원문에 보충 언급 0 — 직접 다시 셈) · 예치 원자료 0) · 그림 `raw/figures/firouz2020_hammerstein-wiener-multisine-bla-nonlinearity-assb/` (자동 13 = `fig_1 … fig_13`(SI 오판 0 — `SI_TAG` False 를 실행 전 확인 · 실행 뒤 이름 눈으로 확인) · **연 것 13/13** · 누락 0 · 표 0 · 크롭 문제 하나(fig_13 아래 가장자리에 캡션 첫 줄 윗부분 잘림 — 그림 내용 온전 · 자동 파일 그대로) · 캡션 필드 11/13 본문 섞임(900 자 잘림 8 · f2 520 · f7 844 · f11 쪽 바닥글 "9") · 그림이 전부 래스터라 여덟 장(그림 2 · 6 · 7 · 8a · 8c · 9 · 12a · 13)은 내장 이미지를 원 해상도로 꺼내 축선 · 격자선 화소로 눈금을 보정해 읽음 — 판독 배열 · 재현 코드는 `scratchpad` 에만 · 커밋 안 함 · `figures.json` notes 13 항목). `raw/figures/_sources.json` 은 추출기 재집계로 이 편 항목 추가 + `danilov2011_thin-film-assb-model-weak-electrolyte-parameter-fit` 그림 수 12 → 14(그 폴더 실물 = 자동 12 + 표 수동 2 — 부수 효과 · 값은 실물과 일치).
- **4차 묶음 파일 52**(원장 §1 요청 14 편 중 둘째 · 2026-10-02 사용자 공급) · 원장 행 "★★★ … 26 | 1 | Q4 | … 구조적 공백 1번 후보" · 지목 26호 [17] 하나(후속 ★★★) — 원장 일치(27호는 "인용하지 않는 것" 목록 — 지목 아님) · 원장 "Soult" = PDF "M. Cazorla Soult"(저자 줄 · XMP · CRediT — 같은 사람, 복합 성의 뒷부분 표기) · VUB MOBI + VUB SURF + Toyota Motor Europe(셀 TME 개발 · 사사) · © 2019 Elsevier(오픈 액세스 0) · 12 쪽 · 그림 13 · 표 0 · 식 35 · 참고문헌 60([24] Further reading 본문 인용 0) · 이 편은 우리 digest 를 인용하지 않는다(4차 묶음 13 편 포함 0).
- ★★★ **(a) 셀 · 대조군**: LiNbO₃ 코팅 LCO ‖ 흑연 코인셀 둘(각 하나 · 1 cm² · 0.55 mAh · 분리막 LiI-Li₂S-P₂S₅ 유리 σ₂₅ 10⁻³) · **양극층 SE 만 Li₂S-P₂S₅ 유리(σ₂₅ ≈10⁻⁴) ↔ γ-Li₃PS₄(≈10⁻⁵ S/cm)** — 25 ℃ 공칭 이름표(출처 · 측정 0) · 시험 60 ℃ · `[재현]` 분리막 500 µm(그림 1 에만) × 10⁻³ = 50 Ω cm² ↔ 셀 1 전체 Re(1 Hz) ≈20–21 Ω `[도표·화소]` → 60 ℃ σ ≥2.4 배 · "the only difference is the ionic conductivity" ↔ 같은 조작을 "boundary resistance" · "interface" 로도 부름(D5) · 조성 · 적재 · 음극층 SE · 압력 · 스프링 · 장비 인쇄 0(`pressure` · `MPa` · `spring` · `torque` 0 회).
- ★★★★ **(b) 식별의 실체**: 무작위 위상 등진폭 33 선 · M 4 × P 6 · 10 Hz · 첨두 ±2.74 mA `[도표·화소]` · 격자 k = 1 · 3 · 11 + 8j(f₀ 4 mHz · 선형 — 0.04 Hz 아래 2 / 33 `[도표·화소]`) · BLA 분산(식 9–11) = FRF 잡음 · 확률적 왜곡(매개변수 0) · `[재현]` 인쇄 식대로면 ×3.13(+5.0 dB — Monte Carlo) · "3rd order FIR" ↔ 식 12 IIR(D1) · H 3차 · W 6차 다항 · H-W 구간 선형("arbitrary breaking points") — 값 · 불확실도 · 차수 근거 · 정규화 0 · `[재현]` 블록 이득 · 오프셋 교환 출력 차 0(구조적 비식별) · 입력 블록 H 단독 확장 ↔ H-W 포화(D8 · 저자 "will be investigated more" 미해결) · accuracy 68.5 · 74.5 · 81 · 86.5 %(정의 0 · 차 ✅) · 식별성 어휘 전수 0(NFKC 전후).
- ★★★ **(c) 고장 검출**: 통계량 · 문턱 · 반복 · 교란 0 · ">100 times" 는 ≈0.07 Hz 위만(최저 두 선 31–35 dB · D12) · 같은 전류에 |Z| ×10.5–12.4 → 셀 2 ≈2.26 … ≈4.2 V(셀 1 ±0.05 V · RT/F 28.7 mV) · `[재현·가정]` BV 상대 왜곡 ∝ (R_ct·I)² · 순수 BV `A·j₀` 하나 → 검출 ≠ 귀속 · 대역 밖 왜곡 +54 … +29 dB(본문 정량 0).
- ★★★ **(d) 34호 처방**: ASSB 계보 첫 설계 가진 실측 · 목적 = 분리(Schoukens 계보) · 정보 기준 0 · 진폭 하나 · 블록 교환 = 입력으로 못 사는 구조적 비식별(34호 경고의 구체 표본).
- ★★ **(e) 이식**: OCV 하네스와 직교(OCV 상수 · 값 0) · 합성 truth 관측 후보(진폭 스윕 BLA + σ_S — 시험 전 · `C_dl ∝ A` 없이는 A1 못 가름 `[해석]`) · 측정 중 상태 이동(SoC 49.98 → 48.86 → 50.40 % ↔ 설계 ≤1 % — D3).
- **채움표 92호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(`θ(N)` 0/92 · 층 하나 — 비선형도 = 활성 면적당 분극) · Q2 없다 · Q3 층 하나(25 ℃ 이름표 · 그림뿐인 블록 · 정의 없는 accuracy %) · Q4 0/92 **여든네 번째 성질** · Q5 해당 없음(층 하나 — 음극층 SE 미기재) · Q6 보고 0(코인셀 · 성형까지 0 — (배)) · Q7 해당 없음(층 하나 — 흑연 도금 검사 0) · Q8 층 하나(OCV 상수 · 두 셀 선형 모형 중심 3.80 ↔ ≈3.6 V).
- **곱 축퇴 처방 일흔다섯 번째 적용**: 1 · 2 · 3-a · 3-b · 4단계 ❌ · 진폭 스윕 ❌ · `J^T J` = 블록 교환의 null 방향(구조) · 곱 문장 식 34–35 → `A·j₀` · 새 줄 0 · 경고 하나(비선형 진폭 채널은 `A·j₀` 를 못 가른다).
- ⚠ 어긋남 22 건(D1 FIR ↔ IIR · D2 "cell 1" · D3 SoC · D4 dB ↔ dB/Hz · D5 벌크 ↔ 계면 · D6 "only difference" · D7 음극층 σ · D8 H 곡률 반대 · D9 Y = X · D10 그림 12b 눈금 · D11 ±3.3 mA · D12 ">100 times" · D13 식 9–11 · D14 H-W "not investigated" · D15 검출 절차 0 · D16 인용 쓰임 · D17 저자 표기 · D18 잡음 위치 · D19 기호 · D20 accuracy · D21 proved ↔ proposed · D22 오기).
- PDF 메타데이터: `%PDF-1.7` · creator "Elsevier" · producer 빈 값 · author "Yousef Firouz" · subject "Journal of Energy Storage, 28 (2020) 101184. doi:10.1016/j.est.2019.101184" · keywords 다섯 · 생성 2020-05-10 21:53:33Z · 수정 2023-08-11 09:08:08 +05'30' · XMP 7,318 B(dc:creator 여섯 · prism 표지 날짜 "April 2020" · VoR · noindex) · PageLabels 1–12(인쇄 쪽과 같음) · 개요 29 · 래스터 16(p. 1 셋 + 그림 13) · "σ25ºC" 의 º = U+00BA(NFKC 뒤 "o").
- 보류 (가)–(히) · (개)–(해) · (게)–(체): **(다)(주)(치)(히)** 근거(중) · (세)(제)(이)(가)(차)(무)(배)(미)(대)(메)(베) 약 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(비선형도 지표의 측정 조건 표기 · 블록 지향 / "system identification" 편의 식별 산출물 표기 · "입력 설계" 의 목적 표기 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 92호 행 · 92편 누적 · Evidence 여든일곱 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](정의 표 새 줄 · 92호 절 · 처방 22 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](일흔다섯 번째 적용 · 주장하지 않는 것) · [[assb-interphase-vs-contact-loss-attribution]](계보 92호 행 · 화살표 · 실험 열한 편 · 주장하지 않는 것) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: [[drt-peak-count-nonidentifiability]] 변경 안 함(DRT 0 — 이 편의 차수 · 꺾인점 선택 근거 0 은 digest 에만) · [[assb-synthetic-truth-contact-loss-requirements]] 변경 안 함(진폭 스윕 관측은 후보 — 시험 전) · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행(✅ 92호 흡수 · 지목 칸 "26 | 1" 그대로 · 셋째 저자 "Soult" → "Cazorla Soult" 표기 보강 후보) · §2 구조적 공백 1번 — 후보 Firouz 2020 "확인으로 닫음"(식별성 0 · 75호 Naik 2022 와 같은 형식) · 재지목 Widanage 2016 [52](49 → 49 · 92 = 2) · Kato 2016 [5](64 · 92 = 2 · 지목 누락 — 새 행) · 새 행 후보(★★ Firouz 2016 [46] · ★★ Schoukens & Tiels 2017 [48] · ★★ Schoukens 2004 [40] · ★★ Relan 2017 [58] · ★ Schoukens · Bai · Rolain 2012 [50] · ★ Bai 1998 [56] · ★ Schoukens 2005 [43] · ★ Vanhoenacker 2001 [41] · ★ Allafi 2017 [53]) · 지목 누락 둘(Kato 2016 — 64호 ★ · Harting 2018 — 10호 ★ [184], 이 편 인용 0) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 52 행.
- 후속(서지 기준, 미열람): **Firouz Y., Relan R., Timmermans J.M., Omar N., Van den Bossche P., Van Mierlo J. 2016 *Energy* 106, 602–617**([46] — 액체셀 도구) · **Widanage W.D., Barai A., Chouchelamane G.H., Uddin K., McGordon A., Marco J., Jennings P. 2016 *JPS* 324, 61–69**([52] — 재지목) · **Schoukens M., Tiels K. 2017 *Automatica* 85, 272–292**([48]) · **Schoukens J., Swevers J., Pintelon R., Van der Auweraer H. 2004 *MSSP* 18, 727–738**([40]) · **Relan R., Firouz Y., Timmermans J.-M., Schoukens J. 2017 *IEEE TCST* 25(5), 1825–**([58] — 액체셀 도구) · Kato Y., Hori S., Saito T., Suzuki K., Hirayama M., Mitsui A., Yonemura M., Iba H., Kanno R. 2016 *Nat. Energy* 1, 16030([5] — 재지목 · 지목 누락) · Schoukens M., Bai E.-W., Rolain Y. 2012 *IFAC Proc. Volumes* 45(16), 274–279([50]) · Bai E.-W. 1998 *Automatica* 34(3), 333–338([56]) · Schoukens J., Pintelon R., Dobrowiecki T., Rolain Y. 2005 *Automatica* 41, 491–504([43]) · Vanhoenacker K., Dobrowiecki T., Schoukens J. 2001 *IEEE TIM* 50, 1097–1102([41]) · Allafi W., Uddin K., Zhang C., Sha R.M.R.A., Marco J. 2017 *Appl. Energy* 204, 497–508([53]) · 교차 참조(지목 아님): Harting N., Wolff N., Krewer U. 2018 *Electrochim. Acta* 281, 378–385(10호 ★ [184]).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 129).

## [2026-10-02] ingest | assb 93호 — Bielefeld A. 2023, How to Develop Useful Models for Solid-State Batteries – A Plea for Simplicity and Interdisciplinary Cooperation (Batteries & Supercaps 6, e202300180)
- raw: `raw/papers/bielefeld2023_useful-models-ssb-simplicity-perspective.md` (sha256 봉인 49186aac…87864832 — `pdf_sha256` 11fdd3cc…ce82dcb4 · 3,375,384 B · 호출자 sha256 일치(직접 재계산) · SI 없음(원문에 보충 언급 0 — 직접 다시 셈 · Data Availability "no new data were created or analyzed") · 예치 원자료 0) · 그림 `raw/figures/bielefeld2023_useful-models-ssb-simplicity-perspective/` (자동 4 = `fig_1` · `fig_2` · `fig_4` · `tab_1`(SI 오판 0 — `SI_TAG` False 를 실행 전 확인 · 실행 뒤 이름 눈으로 확인) + **수동 1 `fig_3_manual_p7`**(그림 3 자동 누락 — p. 7 캡션 블록이 오른쪽 단 본문 "Laue et al. …" 과 한 블록으로 묶임) · **연 것 5/5** · 크롭 과대 셋(fig_2 쪽 전폭 — 오른쪽 단 식 (3)(4) · 본문 · 워터마크 / fig_4 가로줄 · 워터마크 / tab_1 쪽 전체) — 자동 파일 그대로 · `figures.json` notes 5 · 그림 4 표지 화소 판독(축 비율) · 식 · 밀도 · 공극 문장 쪽 렌더 조각은 `scratchpad` 에만 · 커밋 안 함). `raw/figures/_sources.json` 은 추출기 함수로 재집계 — 이 편 항목(5) 추가 · 다른 항목 변화 0.
- **4차 묶음 파일 53**(원장 §1 요청 14 편 중 셋째 · 2026-10-02 사용자 공급) · 원장 행 "★★★ … 26 · 27 | 2 | Q4 | 1호 저자의 모델 방법론 의견" · 지목 26호 [6] · 27호 [2](후속 ★★ 둘 — 원장 일치) · JLU Giessen(ZfM · 물리화학) 단독 저자 · *Batteries & Supercaps* Perspective · CC BY-NC · 학위논문 재수록("lion's share … reprinted") · 12 쪽 · 그림 4(래스터) · 표 1 · 식 6 · 참고문헌 100 · 이 편은 우리 digest 여덟을 인용(1 · 22 · 54 · 55 · 56 · 57 · 73 · 77호) · 4차 묶음 13 편 인용 0.
- ★★★★ **(a) 안건**: Berro 9 단계 · 4단계만 수정("Identify model parameters that fit the data" → "Measure reliable model input parameters") · 비유일성 = Berro 경고 한 문장 · 처방 = 적합 삭제 · 못 재면 "결과에 영향 없을 정교한 추측" · 5단계 = 입력 정확도 · 정밀도의 국소 강건성 스윕 · 6단계 = 정성 검증(코드 대 코드 · 격자 세분화는 p. 2 자기 정의로 verification — D11) · 7단계 대안 가설 "(not done)"(그림 1 에만 — D7) · `identifiab*` · `uniqu*` · `uncertaint*` 0(NFKC 전후) · `validat*` 7 · `sensitiv*` 2.
- ★★★ **(b) 표 1**: 공극 = 네 부류 모두 입력 · 이온 경로 = 플럭스 출력(1D 균질은 입력) · 접촉 = 이름 없음(전도망 출력 활성 표면적 · 이용률) · 충방전 = 면적 · `j₀` 둘 다 입력 · OCV 입력 · 시간 축 0 · R3 원칙 인쇄("The assumption that all volume that is not filled with CAM contains electrolyte no longer applies" — 같은 저자 56호 검증 구조는 위반) · 결론 "ε · τ · 비표면적의 사이클 진화를 수정 Newman 에" = 접촉 손실을 `A_s·j₀` 곱 자리로(R5 · R1).
- ★★★ **(c) 공극 ≈15 %**: 이 편 측정 아님 · 인용 [13,19,20,67] = 55호 13.2(수지 + void) · 73호 14(가정 · SI 13–17) · Ruess · Jiang 미확인 · `[재현]` 평균 13.7 · 압착 조건 0 · 저자 57호 기본값 15("compromise")와 같은 숫자 · 위키 측정 4호 FIB-SEM 2.87 → 9.50 vol%(0 → 50 사이클 · ≈300 MPa 성형) · 82호 14.1–24.3 % · "6–8 %"[68] = 56호 [58] 같은 값 · 1호 예측 조건 20 %.
- ★★★★ **(d) 단순성 ↔ 유일성**: "입력이 적다 → 식별된다" 를 쓰지 않는다(식별성 낱말 0) · 근거 셋(과적합 — 자기 예 적합 0 · 작은 공간 — 물리 입력만 셈 · "distinguishable" — 척도 0) · 자기 예 출력 비유일(1호 `A_spec,a` 평탄) · 56호 그림 7(측정 SOC 의존 ↔ 상수 입력 가족이 같은 곡선 — 상수가 0.5 C 에서 더 맞음) 무언급 · 56호 `j₀` ← `R_CT` 면적 미정의 · 자기 평가: "qualitative agreement" 정직 · 예측 "68 vol%" 조건 탈락(D6) · `[재현]` 55/0.8 = 68.75(1호 69/31 고상) ↔ 73호 Φ(전체 · 14 %) → 고상 28.6–71.0 % · 문턱 위 1/5(D9) · VGCF 두 점(33 vol% +14…+19 % ↔ 61 vol% −2…−53 % — 73호 전사) 방향 ✅ · 위치 미시험 · 73호 전자 σ 무릎은 1호보다 아래 · 그림 4 자기 세 편 축 0.21 → 0.40 → 0.62(`[도표·화소]`).
- **채움표 93호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(`θ(N)` 0/93 · 층 하나 — 공극 인용 요약 · 1호 예측 조건 탈락) · Q2 없다 · Q3 층 하나("입력은 재라" · 측정 역모형 층위 0 · OCV 입력) · Q4 0/93 **여든다섯 번째 성질** · Q5 해당 없음 · Q6 보고 0 · Q7 해당 없음 · Q8 층 하나(OCV 입력 · `D̃(SOC)` 강조와 56호 그림 7 반대 결과 무언급).
- **곱 축퇴 처방 일흔여섯 번째 적용**: 적용 불가(1차 자료 0 — 87 · 81호와 같은 처리) · 곱 문장 넷(표 1 면적 · `j₀` 따로 입력 · Newman A_s · 결론 A_s(N) · 56호 `j₀` ← `R_CT`) · 후보 메모 하나("'측정 입력' 은 곱을 풀지 않는다") · 새 줄 0.
- ⚠ 어긋남 16 건(D1 appropriate ↔ useful · D2 geometric mean ↔ 식 (3) · D3 D_s · D4 D_bulk · D5 j_n · D6 68 vol% 조건 · D7 (not done) · D8 SEM 재구성 ↔ 합성 · D9 부피 기준 · D10 "solely" · D11 verification ↔ validation · D12 [70] · D13 [43] 쪽 · D14 Sangrós-Giménez · D15 오기 · D16 그림 1 6단계 예).
- PDF 메타데이터: `%PDF-1.6` · creator "ima-server®" · producer "PDFlib+PDI 9.0.7p3 (C++/Win64); modified using iText 4.2.0 by 1T3XT" · title(U+2010 하이픈) · author · keywords 빈 값 · subject "Batteries & Supercaps 2023.6:e202300180" · 생성 2023-08-23 17:23:44 +02'00' · 수정 2026-10-02 05:43:08 −07'00'(내려받기 — 워터마크 날짜와 같음 · 기관명 옮기지 않음) · XMP 3,594 B(doi · crossmark 2023-07-20 · VoR) · 개요 0 · PageLabels 0 · 링크 104 · 래스터 7(+ 마스크 1) · 텍스트 층 "=" → "¼" · ρ → "1" · κ → "k"(렌더로 확인).
- 보류 (가)–(히) · (개)–(해) · (게)–(페): **(치)(애)** 근거(강) · (이)(제) 근거(중) · (다)(차)(체)(호)(어)(캐)(해)(비)(그) 약 · (마) 반영(개념 R3 · R8 출처) · (라)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(측정 입력의 역모형 층위 표기 · "단순성" 근거 명제의 척도 · 출력 유일성 표기 · 모형 결론 회고 인용의 조건 복원 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 93호 행 · 93편 누적 · Evidence 여든여덟 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](정의 표 새 줄 · 93호 절 · 처방 23 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](일흔여섯 번째 적용 · 주장하지 않는 것) · [[assb-synthetic-truth-contact-loss-requirements]](R3 · R8 · `A_eff` 자리 출처 · 주장하지 않는 것 · updated 2026-09-29 → 2026-10-02) · [[composite-cathode-percolation-utilization]](93호 절 · 주장하지 않는 것 · updated → 2026-10-02) · [[assb-tortuosity-factor-effective-conductivity-split]](열다섯 번째 표본 · 주장하지 않는 것 · updated → 2026-10-02) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: [[assb-interphase-vs-contact-loss-attribution]] 변경 안 함(계면층 ↔ 접촉 귀속 실험 0) · [[assb-apparent-capacity-decomposition]] 변경 안 함(용량 분해 자료 0) · 새 개념 페이지("측정 대체") 만들지 않음 — 민감도 개념의 정의 표 새 줄로 충분 · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행(✅ 93호 흡수 · 지목 칸 "26 · 27 | 2" 그대로) · 재지목 Ruess 2020 [67](18 · 29 · 38 · 56 · 82 · 87 → + 93 = 7) · Kim 2017 *Nano Lett.* [68](65 · 86 → + 93 = 3) · 새 행 후보(★★ Berro 2018 [2] · ★★ Lee H. 2022 [32] · ★★ Ecker 2015 [29] — 지목 누락 보충 28 · 93 = 2 · ★★ Jiang 2022 [20] · ★ Möbius & Laan 2015 [9] · ★ Kim J.Y. 2022 [81] · ★ Alabdali 2022 [83]) · 지목 누락 보충 후보 둘(Deng 2016 [66] — 18호 ★ · Albertus 2021 [1] — 59호 ★ · 이 편 재지목 안 함) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 53 행.
- 후속(서지 기준, 미열람): **Berro J. 2018 *Biophys. Rev. Lett.* 10, 1637**([2] — 안건 원전 · 약어 원전 확인 필요) · **Lee H., Yang S., Kim S., Song J., Park J., Doh C.-H., Ha Y.-C., Kwon T.-S., Lee Y.M. 2022 *Curr. Opin. Electrochem.* 34, 100986**([32]) · **Ecker M., Tran T.K.D., Dechent P., Käbitz S., Warnecke A., Sauer D.U. 2015 *JES* 162, A1836**([29] — 재지목 · 지목 누락) · **Jiang W., Zhu X., Huang R., Zhao S., Fan X., Ling M., Liang C., Wang L. 2022 *AEM* 12, 2103473**([20]) · **Ruess R. 외 2020 *JES* 167, 100532**([67] — 재지목 → 7) · **Kim D.H. 외 2017 *Nano Lett.* 17, 3013**([68] — 재지목 → 3) · Möbius W., Laan L. 2015 *Cell* 163, 1577([9]) · Kim J.Y. 외 2022 *JPS* 518, 230736([81]) · Alabdali M., Zanotto F.M., Viallet V., Seznec V., Franco A.A. 2022 *Curr. Opin. Electrochem.* 36, 101127([83]) · 교차 참조(지목 아님): 4호 Shi 2020 *J. Mater. Chem. A*(공극 시계열) · 82호 Schlautmann 2023(공극 14.1–24.3 %).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 131).

## [2026-10-02] ingest | assb 94호 — Schmidt C.P., Sinzig S., Wall W.A. 2024, An Electro-Chemo-Mechanic Model Resolving Delamination between Components in Complex Microstructures of Solid-State Batteries (J. Electrochem. Soc. 171, 100502)
- raw: `raw/papers/schmidt2024_nitsche-contact-delamination-resolved-ssb-cathode.md` (sha256 봉인 c184fa10…cfbb6510aa — `pdf_sha256` a58e96d8…72ebe3957 · 2,786,517 B · 호출자 sha256 일치(직접 재계산) · SI 없음(원문에 보충 언급 0 — 직접 다시 셈) · 예치 = Zenodo 결과 자료 10.5281/zenodo.13802728(받지 않음)) · 그림 `raw/figures/schmidt2024_nitsche-contact-delamination-resolved-ssb-cathode/` (자동 17 = `fig_1 … fig_17`(SI 오판 0 — `SI_TAG` False 를 실행 전 확인 · 실행 뒤 이름 눈으로 확인) + **수동 9**(그림 1 전폭 — 자동 오른쪽 잘림 · 그림 11 — 자동 f11 은 그림 12 조각 오탐 · 표 I · B·I–B·VI — 표 캡션 7 개 전부 미인식) · **연 것 26/26** · 크롭 과대 둘(f4 위쪽 표 I 본문 · f12 그림 11 표지 · 본문) · 캡션 필드 오염 둘(f4 900 자 잘림 · f9 본문 섞임) · 그림 7 · 8 · 9 · 12 · 14 · 15 · 17 은 **벡터 경로**(곡선 외곽선 · 축 상자 · 별표)로 판독 · 식 · 표는 쪽 렌더 조각 — 판독 · 재현 코드는 `scratchpad` 에만 · 커밋 안 함 · `figures.json` notes 26). `raw/figures/_sources.json` 은 추출기 함수로 재집계 — 이 편 항목(26) 추가 · 다른 항목 변화 0.
- **4차 묶음 파일 54**(원장 §1 요청 14 편 중 넷째 · 2026-10-02 사용자 공급) · 원장 행 "★★★ … 27 | 1 | Q1 | … 27호가 재 보인 P2D 대비 상수 오프셋 0.07 이 바로 비연결 입자 몫 `1−u` … 그 기구의 모델 원전" · 지목 27호 [18](후속 ★★★ 하나 — 원장 일치) · TUM 계산역학연구소(Wall) + TUMint.Energy · 27호와 같은 연구실 · 같은 코드(4C)의 앞선 편 · CC BY · 16 쪽(p. 1 IOP 표지) · 그림 17 · 표 7 · 식 47 + A·1–5 + B·1–7 · 참고문헌 번호 1–61(인쇄 59 — 18 · 51 없음) · 우리 digest 셋을 인용(4 · 23 · 75호) · 4차 묶음은 파일 57 Koerver 2018 *EES* 하나([26]).
- ★★★★ **(a) 박리 · 재접촉 기준**: Hertz–Signorini–Moreau(식 17 — 인장 강도 0 · 무접착 · 무마찰) + 식 27 "p_n < 0 일 때만 BV" · 손상 · 이력 0 → **구성상 완전 가역** · Nitsche(θ = 0 · 요소별 고유값 벌칙 · 조화 가중)의 기준 벌칙 γ_n,0 인쇄 0 · 재접촉은 본문 0(`recontact*` 6 회 전부 틀 문장) — 그림 9 벡터 70 MPa 끝 SoC 93.5 → 94.5 % 에서 89.6 → 87.7 %(−1.9 %p · 무언급) 한 번 · 분리 시험 틀: 박리 = `θ_AM` 아닌 표면 `φ` 손실 → `η(i)` 경로 — "율 먼저 · 재가압 나중" 의 forward 표본 · 23호 50 사이클 방전 상태 틈 지속은 이 법칙으로 못 낸다(digest 전사).
- ★★★★ **(b) 스택 압력**: 예압 50 / 60 / 70 MPa = Robin 스프링 k 10¹³ Pa m⁻¹("assumed") 오프셋 목표(표 B·VI) · `[재현]` k·u_k 50.41 … 71.33 MPa · 셀 압축 → 유효 구속 탄성률 30.5–38.4 GPa(Reuss–Voigt 안 ✅) · 반력 이력 인쇄 0 · `[재현·가정]`(양극 쪽 경계 고정 · 측면 대칭 · Li 두께 성장) 반 사이클 **+13 / +53 / −58 MPa** · 초록 압력 명제 = 단순 기하 세 점(`[도표·벡터]` 시작 SoC 13.2 / 14.9 / 16.4 % · 끝 몫 97.1 / 90.5 / 87.8 % · 4.2 V 87.18 / 91.26 / 94.81 %) · 경계 70 MPa 아래 계면 인장 92.9 %(단순) · 79.8 %(복잡) — (캐)(태)(하)① 강한 모형 표본.
- ★★★★ **(c) 귀속**: 인쇄 사슬(박리 면 플럭스 0 → 남은 면 전류 ↑ → 내부 저항 ↑ → 컷오프 조기) · `[재현·가정]` 남은 면 BV ≈6 mV ↔ 전압 차 24 · 46 mV(90 · 94 %) · 그림 10f 농도 χ 0.406–0.436 → OCV 67 mV 퍼짐 · 컷오프 = 접촉 자리 표면이 OCV 4.2 V 점(χ 0.4065 `[재현]`)에 닿을 때 · (평균 − 표면)/0.596 = 4.78 % ↔ 결손 4.5 %p → **결손 = 입자 안 남은 Li(η 형)** · LAM 기구 0 · 고정 컷오프 곡선에서는 용량 축척처럼 보인다(유한 율 조건) · 율 스윕 · 휴지 0.
- ★★★★ **(d) 27호 `1−u` 0.07** — 확인하지 않는다: 27호 `u` = 전자 비연결(정적 · Sinzig 2024 `contact` 0 회) ↔ 이 편 `φ` = 이온 계면 박리(동적 · 부분 · 가역 · `connect*` · `utiliz*` · `percolat*` 0) · 꼴도 다름(상수 7 % ↔ 율 · 압력 · 조립 의존 4.5 · 3.1 · 0.2 %p) · 역학 경계도 다름(27호 5×10¹¹ Pa m⁻¹ · 예압 0 ↔ 10¹³ · 50–70 MPa) — 원장 행 "그 기구의 모델 원전" 은 두 기구를 묶은 기대.
- ★★★ **(e) 층위 · 검증**: 출처 열 = 측정 원자료([26] 부피 곡선 — 자료 χ ≤0.912 · 운용 창 위쪽 외삽) · 제일원리(β-LPS E 28.9 GPa [58] — 측정 원전 [59] Sakuda 는 밀도에만) · 남의 모형 입력 평균 · 조정([25] Neumann 2020) · 가정(k · χ0% 1.0 · χ100% 0.404) · `[재현]` 패치 시험 ✅(η −24.7 mV · σ_xx −0.552 Pa) · 표 B·VI ✅ · **질량 수지 ❌ 표 B·V**(양극 초기 2.10×10⁴ 이면 AM 88 % · c_max 로만 36 %) · OCV 4.2 V @ χ 0.4065 · 부피 ΔV/V −1.48 % · verification 둘 · validation 0(`validat*` 0) · `identifiab*` · `uniqu*` · `uncertain*` · `sensitiv*` 0 · `fit*` 0 → 2(NFKC).
- **채움표 94호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 층 하나(모형 `φ_del(SoC; P)` · `θ(N)` 0/94) · Q2 없다 · Q3 층 하나(출처 층위 넷 · 표 B·V ↔ 그림 7) · Q4 0/94 **여든여섯 번째 성질** · Q5 해당 없음 · Q6 보고(모형 예압 · 스프링 가정 · 이력 0) · Q7 해당 없음 · Q8 층 하나(문헌 OCV 함수 · 부피 법칙 외삽).
- **곱 축퇴 처방 일흔일곱 번째 적용**: 부분 적용 — 계면 법칙 쌍 = 2단계 "면적을 아는 대조군" 의 모형판 · 1 · 3단계 · 율 스윕 ❌ · 곱 문장 셋 · 후보 메모 하나("면적 손실의 관측 서명은 BV 보다 고체 확산 쪽") · 새 줄 0.
- ⚠ 어긋남 16 건(D1 표 B·V 양극 초기 농도 · D2 그림 5 전류 부호 · D3 recontacting ↔ 결과 0 · D4 "during cycling" · D5 "consistent with literature" · D6 "quantitative" · D7 단순 기하 측면 "—" · D8 참고문헌 18 · 51 없음 · D9 [22] 저널명 · D10 그림 9 캡션 · D11 서지 연도 · D12 "first charge or discharge" · D13 i₀ "factor" · D14 log 밑 · D15 질량 보존 모의 동일성 · D16 무시 근거의 압력 범위).
- PDF 메타데이터: `PDF 1.7` · creator "IOPP" · producer "iText® 5.5.13.5 ©2000-2026 iText Group NV (IOP Publishing Ltd; licensed version)" · author "Christoph P. Schmidt" · subject "Journal of The Electrochemical Society, 171(2024) 100502. doi:10.1149/1945-7111/ad76dc" · keywords 여섯(… recontacting …) · 생성 2024-10-03 19:42:06 +05'30'(게재 하루 전) · 수정 2026-10-02 13:43:42 +01'00'(내려받은 날 — IP 는 옮기지 않음) · XMP 5,942 B(VoR · crossmark 2024-10-04 · prism number 10) · PageLabels 1–16 · 래스터 12 · 벡터 그림 10(글자까지 외곽선) · 식 · 표 B·I–B·III 텍스트 층 깨짐 → 쪽 렌더로 읽음 · 합자 `ﬁ` 83 · `ﬂ` 25.
- 보류 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(냐): **(하)(캐)(태)(치)(세)** 근거(강) · (이)(노)(차)(키)(저)(냐) 근거(중) · (투)(러)(두)(제)(거)(애)(비)(체)(무) 약 · (마)(바) 반영(개념 출처 · 절) · (라)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(모형 "스택 압력" 의 구속 강성 · 사이클 중 압력 이력 표기 · "접촉 손실 → 용량 손실" 모형 결과의 결손 꼴(η ↔ θ) 표기 · 다른 편 현상의 "모형 원전" 지목 때 기구 층위 확인 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 94호 행 · 94편 누적 · Evidence 여든아홉 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-pressure-reapplication-separation-test]](94호 절 — 압력이 `φ → η` 경로로 · 설계 조건 D1 · D4 · D5 모형판 · 주장하지 않는 것 · updated 2026-09-29 → 2026-10-02) · [[assb-stack-pressure-operating-window]](94호 절 — 예압 · 스프링 · 표류 · 경계 ↔ 계면 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](일흔일곱 번째 적용 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](94호 절 — 결손 = `η(i)` · 주장하지 않는 것) · [[assb-synthetic-truth-contact-loss-requirements]](`A_eff` 자리 · R4 · R7 · R8 출처 · 주장하지 않는 것) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: 새 개념 페이지("박리 접촉 법칙" · "모형 압력 표기") 만들지 않음 — 기존 개념 절 · 새 판단 거리로 충분 · [[composite-cathode-percolation-utilization]] 변경 안 함(`θ_AM` · 전자 연결 계산 0 — `u` 대조는 digest §(d) 에만) · Zenodo 결과 자료 받지 않음(지시) · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행(✅ 94호 흡수 · 지목 칸 "27 | 1" 그대로 · 이유 칸 "그 기구의 모델 원전" 정정 — 다른 기구(이온 계면 박리 `φ`)의 원전) · 재지목 열(Tian & Qi 2017 [13] → 3 · Barai 2021 [20] → 4 · Neumann 2020 [25] → 5 · Jung 2019/2020 [10] → 3 · Koerver 2018 [26] → 13 · Bistri 2021 [21] → 2 · Sakuda 2013 [59] → 3 · Wang & Sakamoto 2018 [30] → 3 · Kasemchainan 2019 [5] → 4 · Kremer [61] → 3) · Shao 행(파일 63) 꼬리 — 12호 [63] 은 *Energy* 239, 121929(다른 편) · 새 행(★★★ Shao 2022 *Energy* [16] — 지목 누락 보충 12 · 94 = 2 · ★★★ Liu B. 2023 *SusMat* [12] · ★★ Schmidt 2023 *CMAME* [35] · ★★ Zhang T. · Kamlah · McMeeking 2024 *JMPS* [23] · ★★ Naik 2023 *ESM* [34] · ★★ Hänsel & Kundu 2021 [8] · ★★ Lewis 2021 *Nat. Mater.* [7] — 지목 누락 보충 14 · 19 = 2 · 이 편 재지목 안 함 · ★ Ganser 2019 [27] · Singer 2023 [28] · Yang 2016 [58] · Huang 2023 [24] · Farzanian 2023 [22]) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 54 행.
- 후속(서지 기준, 미열람): **Barai P. 외 2021 *Chem. Mater.* 33, 5527**([20] — 재지목 → 4) · **Tian H.-K., Qi Y. 2017 *JES* 164, E3512**([13] — 재지목 → 3) · **Shao Y.-q., Liu H.-l., Shao X.-d., Sang L., Chen Z.-t. 2022 *Energy* 239, 121929**([16] — 지목 누락 보충 → 2) · **Neumann A. 외 2020 *ACS AMI* 12, 9277**([25] — 재지목 → 5) · **Liu B. … Bruce P.G. 2023 *SusMat* 3, 721**([12]) · **Jung S.H. 외 *AEM* 10, 1903360**([10] — 재지목 → 3) · **Koerver R. 외 2018 *EES* 11, 2142**([26] — 4차 묶음 파일 57 · 재지목 → 13) · Schmidt C.P. 외 2023 *CMAME* 417, 116468([35]) · Zhang T., Kamlah M., McMeeking R.M. 2024 *JMPS* 185, 105551([23]) · Naik K.G. 외 2023 *ESM* 55, 312([34]) · Bistri & Di Leo 2021 *JES* 168, 030515([21] — 재지목 → 2) · Sakuda 2013 *Sci. Rep.* 3, 2261([59] — 재지목 → 3) · Wang M. & Sakamoto J. 2018 *JPS* 377, 7([30] — 재지목 → 3) · Hänsel C. & Kundu D. 2021 *Adv. Mater. Interfaces* 8, 2100206([8]) · Kasemchainan J. 외 2019 *Nat. Mater.* 18, 1105([5] — 재지목 → 4) · Kremer L.S. 외 *Energy Technol.* 8, 1900167([61] — 재지목 → 3) · Ganser 2019 *JES* 166, H167([27]) · Singer 2023 *Energy Technol.* 11, 2300098([28]) · Yang 2016 *ACS AMI* 8, 25229([58]) · Huang 2023 *EA* 463, 142873([24]) · Farzanian 2023([22] — 저널명 확인 필요) · 교차 참조(지목 아님): 27호 Sinzig 2024 · 58호 Asheri 2023 · 지목 누락(재지목 안 함): Lewis 2021 *Nat. Mater.* 20, 503([7]).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 132).

## [2026-10-02] ingest | assb 95호 — Khalik Z., Donkers M.C.F., Sturm J., Bergveld H.J. 2021, Parameter estimation of the Doyle–Fuller–Newman model for Lithium-ion batteries by parameter normalization, grouping, and sensitivity analysis (J. Power Sources 499, 229901)
- raw: `raw/papers/khalik2021_dfn-grouping-sensitivity-parameter-estimation.md` (sha256 봉인 ce935a9e…c22ab27c — `pdf_sha256` 24ba9143…bddb0165 · 3,574,085 B · 호출자 sha256 일치(직접 재계산) · SI 없음(원문에 보충 언급 0 — 직접 다시 셈) · 원자료 · 코드 공개 0) · 그림 `raw/figures/khalik2021_dfn-grouping-sensitivity-parameter-estimation/` (자동 12 = `fig_1 … fig_8` · `tab_1 … tab_4`(SI 오판 0 — `SI_TAG` False 를 실행 전 확인 · 실행 뒤 이름 눈으로 확인) + **수동 6**(그림 4 · 8 전폭 — 자동 왼쪽 잘림 · 표 1–4 단독 — 자동 표 넷은 쪽 전체 · `tab_1` = `tab_2` 바이트 동일) · **연 것 18/18** · 캡션 필드 오염 둘(`tab_2` 649 자 · `tab_3` 233 자 — 표 본문 섞임) · 그림 2–8 은 **벡터 경로**(곡선 꼭짓점 · 상자 · 중앙값 선 · 줄기 끝)로 판독 · 표 1 · 3 · 4 의 식 · 지수는 쪽 렌더로 읽음 — 판독 · 재현 코드는 `scratchpad` 에만 · 커밋 안 함 · `figures.json` notes 18). `raw/figures/_sources.json` — 이 편 항목(18) 추가 · 다른 항목 변화 0.
- **4차 묶음 파일 55**(원장 §1 요청 14 편 중 다섯째 · 2026-10-02 사용자 공급) · **⚠ 액체셀 도구 — ASSB 아님**(28호 Bizeray 선례 · 채움표 도구 칸) · 원장 행 "★★★ … 27 | 1 | Q4 | "P2D 파라미터를 실험에 맞춘다" 의 두 인용 중 하나 — DFN 파라미터 그룹화 도구 후보 (공백 1번 후보, 액체셀)" · 지목 27호 [27](후속 ★★★★ 하나 — 원장 "27 | 1" 일치 · 등급 ★★★★ ↔ 원장 ★★★ 는 표시만) · TU/e(+ NXP) + TUM EES(Sturm) · © 2021 Elsevier(OA 0) · 11 쪽 · 그림 8 · 표 4 · 식 1–22 · 참고문헌 [1]–[40](빠진 번호 0) · 우리 digest 하나를 인용([13] = 28호) · 4차 묶음 13 편 인용 0.
- ★★★★ **(a) 재매개화**: `[인쇄]` 원 DFN 35 → 묶음 24(표 1(b) 식 8–14 가 묶음만으로 쓰임 — 출력 = 묶음 함수의 **구성 증명** · 적어도 11 방향 구조적 비식별) → 추정 22(Q 측정 · `R̂_f,p` 범위 [0, 0]) → 권고 12(출력 RMSE 평탄). `[재현]` 35 = 표 2 "a" 34 + `A` · 24 = Q + 창 4 + 19. **24 의 식별성은 증명 0** — `[재현·대수]` 식 (9a) `D̂_e p̂` · (11a) `κ̂ p̂` 로만 쓰여 정확한 척도 대칭 하나(≤23) · 본문이 적지 않은 `α_c = 1 − α_a`(식 12a · b)가 `k̂₀` 묶음 정확성에 필요 · 셀 EMF 만 아는 구성(경우 1)에서 창 넷은 평형 채널에 정의상 무정보(`[인쇄]` "the same EMF-SOC relation can be reached with any choice between 0 and 1"). 감도 = 범위 정규화 β 위 유한차분 감도 행렬의 피벗 QR(Lund & Foss) — 한 점 · 계산점 미인쇄 · 문턱 0 · `[재현]` `|r₁₁|/|r_kk|` → cond ≥10^2.98(12 개). `identifiab*` 7 · FIM · CI · 프로파일 0(NFKC 전후 같음 · 합자 0).
- ★★★★ **(b) 강조문 다섯**: H1 "not necessarily physically meaningful" — 합성(무잡음 · 같은 모형)에서도 참값 IQR 밖 14/22 `[도표·벡터]` 로 선다 · H2 "not necessary to obtain an accurate model" — 출력 기준(결론 "(with respect to the output voltage)") · H3 "length … carefully selected" — 약함(회차 하나 · +0.42 · +0.78 mV = 같은 곡선 요동 크기 · 마지막 10 % = SoC 0.282 → 0.214 · 검증 RMSE 로 고름) · H4 "Modeling errors can lead to a large bias" — 가장 단단함(조건: 참값 하나 · 오차 꼴 둘 · 입력 하나) · H5 "both cell teardown and estimation" — 권고(좁힘 시험 0 — D12).
- ★★★★ **(c) 그림 2 보정**: 이동 · 늘림(우리 α·β)이 아니라 0–10 % 양극 형상 교체 + 음극 되계산(EMF 보존) — `[도표·벡터]` 직선 기울기 0.545 ↔ 규칙 0.564 V/SOC · 빌린 흑연 U_n 형상 오차가 U_p 로 1:1(+6 … +54 mV) · 분해 쌍 ↔ 셀 EMF −9.5 … +13.5 mV · 그림 2 ↔ 3 Cell 2 EMF 21–59 mV(D2). 경우 2(분해 OCP + 창 맞춤 — 방법 미인쇄) = 우리 α·β 와 같은 연산 · 형상 불변 가정 · 경우 1 = 형상 자유의 극단(창 무정보).
- ★★★★ **(d) 자료 길이 · 모형 오차**: 실셀 참값 없음 · 회차 하나 · `[재현·가정]` Cell 1 ≈10.4–10.6 Ah · 첨두 ≈2.3C · 그림 6 ↔ 5(b) 폐합(→ 14 개) · 검증 자료로 모형 선택(Cell 2 검증 = 추정 구간 포함) / 합성 = 참값 하나 · 같은 모형 · 무잡음 · 50 시작 · `[재현]` 표 4 무작위 기준 0.427 ↔ 0.43 ✅ · 출력 RMSE 중앙값 0.13 mV ≠ 0(수렴 실패 섞임 · `tol` 0) · 모형 오차 1.2 mV → β RMSE 0.43–0.44 = 무작위 · 세 수정 모두 `s_p,100%` 범위 하한(참 0.418 → 0.22) · 주입 오차 = 실셀 잔차 ×0.32–0.35(D3).
- ★★★ **(e) 이식**: 피벗 QR 조건수 하한(NEW_MODEL_REQUIREMENTS §7-1 ② 의 값싼 첫 판) · 합성 + 형상 오차 주입 + 무작위 기준 · 경계 접촉 + 범위 확장(§7-1 ③) / 못 함: 수치 규칙(12 개 · 70–90 %) · 경우 1 구성 · 다중 시작 산포 = 폭(§7-1 ①⑤) — 우리 쪽 수치는 옮기지 않음.
- **채움표 95호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나 — 정규화 DFN 묶음 대수 · `θ(N)` 0/95) · Q2 없다 · Q3 층 하나(적합 + 합성 참값 · 범위 끝 10/22) · Q4 ASSB 0/95 **여든일곱 번째 성질**(도구 칸) · Q5 해당 없음 · Q6 없다 · Q7 해당 없음 · Q8 층 하나(화학 · EMF 측정법 미인쇄 · 빌린 곡선 배분 오차).
- **곱 축퇴 처방 일흔여덟 번째 적용**: 적용 불가(액체 · 접촉 0) — 곱을 "묶음" 으로 선언하는 처방의 원형(`D̂_s = D_s/R_s²` 인쇄 · `k̂₀ × A_eff` · `R̂_f ÷ A_eff` `[재현·대수]` · 양극 `R̂_f,p` [0, 0] → 양극 `u` ≈ `LAM_PE`) · 후보 메모 하나 · 새 줄 0.
- ⚠ 어긋남 15 건(D1 창 목록 오기 셋 · D2 그림 2 ↔ 3 EMF · D3 "same range" ×0.32–0.35 · D4 그림 6 캡션 60 % · D5 "both modifications" · D6 "first 10 … close" · D7 그림 8 76.7 분 · "Time [s]" · D8 "(18)" ↔ (19) · D9 `α_c` 가정 무언급 · D10 식 (7) 부호 · (12b) 표기 · D11 단위 · D12 "bias … reduced" · D13 [13] 시간 영역 분류 · D14 "identifiability … not a large issue" · D15 보정 기울기 · MRSE · 표 4 단위).
- PDF 메타데이터: `PDF 1.7` · creator "Elsevier" · producer "Acrobat Distiller 8.1.0 (Windows)" · author "Z. Khalik" · subject "Journal of Power Sources, 499 (2021) 229901. doi:10.1016/j.jpowsour.2021.229901" · 생성 2021-05-12 23:51:50Z · 수정 2021-05-13 01:37:26Z(호출자 메모와 같음) · XMP 5,367 B(VoR · coverDate 2021-07-01) · PageLabels 1–11 · 래스터 4(그림은 그림 1 하나) · 벡터 그림 7 · 합자 0.
- 보류 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(먀): **(다)(체)** 근거(강) · (헤)(세)(치)(테)(이)(갸)(무)(차) 근거(중) · (가)(페)(러)(먀)(냐)(메)(제)(에) 약 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋(재매개화 · 묶음의 최소성 표기 · 다중 시작 · 합성 참값 시험의 일관성 ↔ 정확성 표기 · 빌린 곡선 + EMF 정의형 평형 모형의 창 무정보 · 배분 오차 + 분해 쌍 ↔ 셀 EMF 잔차 표기 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 95호 행 · 95편 누적 · Evidence 아흔 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](정의 표 새 줄 "둘째 줄의 직교화 순위 + 합성 다중 시작판" · 95호 절 · 처방 24 · 주장하지 않는 것) · [[spm-grouped-parameter-identifiability]](적용 표 95호 세 행 · DFN 판 절 · 한계) · [[halfcell-window-parametrization-lineage]](비교표 새 줄 · 여덟 번째 축 · 관련) · [[halfcell-ocp-shape-invariance]](95호 절 — 빌린 형상의 배분 오차 · 분해 쌍 잔차 · updated 2026-09-22 → 2026-10-02) · [[assb-lampe-contact-product-degeneracy]](일흔여덟 번째 적용 · 주장하지 않는 것) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: 새 개념 페이지("DFN 묶음 식별성") 만들지 않음 — [[spm-grouped-parameter-identifiability]] 의 DFN 판 절로 충분 · [[np-lip-ocv-reparametrization]] · [[data-window-identifiability]] · [[constrained-crb-identifiability]] 변경 안 함(연결은 digest · 위 페이지들의 링크로) · 원 참고문헌(28 · 27 · 93호 인용분) 다시 열지 않음 — digest 전사 대조 · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행(✅ 95호 흡수 · 지목 칸 "27 | 1" 그대로 · 등급 ★★★ 그대로(27호 ★★★★ 표시만)) · 재지목 열(Ecker 2015 [23] → 3) · 꼬리만(Forman 2012 행 — 이 편 [19] 은 2011 *ACC* 판 · Ramadesigan 2012 행 — 이 편 [27] 은 2011 *JES* 158, A1048 다른 편) · 새 행(★★★ Sturm 2019 *JPS* 412 [24] · ★★★ Jobman · Trimboli · Plett 2015 [25] · ★★ Lund & Foss 2008 [30] · ★★ Jin · Danilov · Van den Hof · Donkers 2018 [18] · ★★ Chu … Ouyang 2020 [22] · ★★ Ramadesigan 2011 [27] · ★★ Schmalstieg 2018 [26] · ★ Beelen 2018 [38] · ★ Bergveld · Kruijt · Notten 2002 [34] · ★ Zhou & Huang 2020 [17] · ★ Schmidt A.P. 2010 *JPS* 195, 5071 [16] · ★ Sturm 2019 *JPS* 436 [39]) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 55 행.
- 후속(서지 기준, 미열람): **Sturm J. 외 2019 *JPS* 412, 204**([24] — 우리 γ_Si 축 · 액체셀 도구) · **Jobman R., Trimboli M.S., Plett G.L. 2015 *J. Energy Chall. Mech.* 2(2), 45**([25]) · **Ecker M. 외 2015 *JES* 162, A1836**([23] — 재지목 → 3) · Lund B.F. & Foss B.A. 2008 *Automatica* 44, 278([30]) · Jin N. · Danilov D.L. · Van den Hof P.M. · Donkers M. 2018 *Int. J. Energy Res.* 42, 2417([18]) · Chu Z. … Ouyang M. 2020 *J. Energy Storage* 27, 101101([22]) · Ramadesigan V. 외 2011 *JES* 158, A1048([27]) · Schmalstieg J. 외 2018 *JES* 165, A3799([26]) · Beelen · Bergveld · Donkers 2018 CCTA([38]) · Bergveld · Kruijt · Notten 2002([34]) · Zhou & Huang 2020 *J. Energy Storage* 31, 101629([17]) · Schmidt A.P. 외 2010 *JPS* 195, 5071([16]) · Sturm J. 외 2019 *JPS* 436, 226834([39]) · 꼬리만: Forman 2011 *ACC*([19] — 원장 Forman 2012 행) · 재지목 안 함(목록 인용): Santhanagopalan 2007([11]) · Smith & Wang 2006([33]).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 133).

## [2026-10-02] ingest | assb 96호 — Lu D., Trimboli M.S., Fan G., Wang Y., Plett G.L. 2022, Nondestructive EIS Testing to Estimate a Subset of Physics-based-model Parameter Values for Lithium-ion Cells (J. Electrochem. Soc. 169, 080504)
- raw: `raw/papers/lu2022_nondestructive-eis-lumped-dfne-parameter-estimation.md` (sha256 봉인 f6593137…27a7f44b — `pdf_sha256` ffab9252…cf7815b8 · 5,151,189 B · 호출자 sha256 일치(직접 재계산) · SI 없음(보충 언급 0 — 부록은 본문 안 p. 22–28 · 직접 다시 셈) · 원자료 · 코드 공개 0) · 그림 `raw/figures/lu2022_nondestructive-eis-lumped-dfne-parameter-estimation/` (자동 19 = `fig_1 … fig_19`(SI 오판 0 — `SI_TAG` False 를 실행 전 확인 · 표 자동 검출 0) + **수동 10**(표 I–X 단독 — 쪽 렌더 300 dpi · 가로 쪽 표 VII 250 dpi) · **연 것 29/29** · 크롭 겹침 하나(`fig_4` 위 끝에 그림 3 캡션 꼬리 한 줄 — 그림 내용 온전) · 캡션 필드 오염 · 잘림 열하나(본문 섞임 — 그림 5 · 7 · 8 · 11 · 12 · 14 · 17 · 19 / 짧게 잘림 — 그림 3 · 16 · 18) · 그림 19 개 전부 **래스터**(벡터 0) — 화소 좌표를 축 눈금 · 격자선으로 보정해 판독 · 식 · 첨자는 쪽 렌더로 읽음 — 판독 · 재현 코드는 `scratchpad` 에만 · 커밋 안 함 · `figures.json` notes 29). `raw/figures/_sources.json` — 이 편 항목(29) 추가 · 다른 항목 변화 0.
- **4차 묶음 파일 56**(원장 §1 요청 14 편 중 여섯째 · 2026-10-02 사용자 공급) · **⚠ 액체셀 도구 — ASSB 아님**(28 · 95호 선례 · 채움표 도구 칸) · 원장 행 "★★★ … 27 | 1 | Q4 | 같은 문장의 두 번째 인용 — 집약(lumped) 파라미터 추정 (공백 1번 후보)" · 지목 27호 [28](후속 ★★★★ 하나 — 원장 "27 | 1" 일치 · 등급 ★★★★ ↔ 원장 ★★★ 는 표시만) · UCCS(ECE) + Cummins Inc.(자금) · © 2022 ECS/IOP(OA 0 · 꼬리말 TDM · AI 학습 권리 유보) · 29 쪽(p. 1 = 내려받기 표지 · 내려받기 IP 는 옮기지 않음) · 그림 19 · 표 10 · 식 [1]–[21] · 참고문헌 [1]–[87](빠진 번호 0 · [49] = [52] 중복) · 우리 digest 하나를 인용([27] = 51호) · 4차 묶음 13 편 인용 0.
- ★★★★ **(a) 추정 대상**: `[인쇄]` 초록 "thirteen lumped parameters plus multiple reaction-rate constants" = `p_EIS^lin` 열셋(D̄s,ref 2 · n_f 2 · C̄dl 2 · n_dl 2 · n̄e^r/ψ̄ 3 · κ̄D/ψ̄ · R_c — `[재현]` 13) + k̄0,j(실셀 흑연 6 + NMC 5 · 가상 7 + 4 = 11). 모드 좌표 Q · θ0 · θ100 과 OCP(MSMR)는 연재 앞 시험[3–5]의 입력 · 펄스 매개변수는 [6] · ψ̄ 는 [7] PSS 방전(표 I). 비용 식 [18] = 실수부 · 허수부 오차를 각 자료 |Z| 로 나눈 상대 제곱합(Strategy 1 — SOC × 주파수 균등) · Strategy 2 = SOC 별 · particleswarm + fmincon · 48 h · 실행 하나(기본 시드). 초기값 = DRT 봉우리 반전 + 연재 앞 값 + 부록 식 — `[재현]` κ̄D,0 −4.39×10⁻⁴ V K⁻¹ · ψ̄0 4.18×10⁻⁷ · 그림 11(e) 초기 X ≈2.12 ↔ 식 2.13 · n̄e/ψ̄ 초기 X 셋 폐합 · 경계 인쇄(부록).
- ★★★★ **(b) 식별성**: 구조적 = 인용("We know from Ref. 2 …" — 학회 판 · 지면 0) · 선형 = 손 분석 결론 둘(ψ̄ · n̄e^r · κ̄D 는 비로만 — `[재현·대수]` 부록 계수 척도 불변 ✅ · R_c ↔ 1/κ̄^s "identical") · 실제적 = 가상 셀 하나 · 같은 TF 모형 · 잡음 0.5 % 실현 하나 · 실행 하나 — `[도표·화소]` 부분 집합 열셋 중 열둘 ±5 %(n̄e^s/ψ̄ 1.48) / 전체 집합 n̄e/ψ̄ 1.20 · 0.48 · 1.25 · κ̄D/ψ̄ 1.19 · R_c 1.64(초기 = 참) · σ̄^p ≈1.66 · κ̄^p ≈1.44 · κ̄^n ≈1.29 · `[재현]` k̄0,6/7 참값 = 경계 하한의 1/1,287 · 1/411 · 출력 ≲0.04 mΩ — 본문은 "some degradation" · R_c "lack of convergence" 를 인쇄하나 초록 · 결론은 단서 없이 "highly accurate" · "very good accuracies" · `[해석]` R_c +0.64 ↔ R̄f^n −≈0.6 mΩ(직렬 골짜기 셋). DRT: "we simply assume"(τ 순서 배정) · 저자 그림에서 CPE 하나 → 극대 셋 · 참 모형 과정 다섯 → 극대 15(`[도표·화소]` · 본문 언급 0). `identifiab*` 19(NFKC — 합자 256 · NFKC 전 0) · `uniqu*` 4 · FIM · 공분산 · Hessian · bootstrap · Bayes · `uncertain*` 0.
- ★★★★ **(c) 검증**: 독립 측정 대조 0 · Panasonic 25 Ah 각형 흑연//NMC 하나(Ford C-MAX Energi PHEV 팩 · 이력 · SOH 미인쇄) · 25 °C · 19 SOC(그림 17(f) 6.4 … 100 % — 표 IV "identical to Table III" 와 어긋남) · C/50 정전류 · K–K(Gamry — 잔차 값 0) · SOC 당 "about a day" · 시간 영역 "planned for future publications". `[재현]` 표 VI ↔ 같은 편 부록: n̄e^n 1.0166 mol > 3Q/14 0.200 · κ̄D −1.46×10⁻⁸ ↔ −1.55×10⁻³ … −8.62×10⁻⁵ · κ̄^p/κ̄^s 0.072 < 2⁻³·⁵ · R̄dl^n 10⁻¹⁰ < 10⁻⁶ · K_n̄e 2.000 · n_dl^p 0.90 · ψ̄ 화해 불가(×3×10⁴) · κ̄D/ψ̄ S1 −0.040 ↔ S2 19 점 ×12 · 가상 셀 참 −492 · "consistent" 기준 0.
- ★★★ **(d) EIS = 관측 추가**: 이 편 그대로는 LLI ↔ LAM 분리 0(모드 좌표 = 입력 — 28호와 같은 쪽 끝) · 열리는 채널 = 전극별 C̄dl · k̄0(면적 비례 — LAM_PE · LLI · 표면 접촉 손실에 다른 서명 `[해석]`) · 조건 다섯(τ 순서 배정 · CPE 계수 n_dl 0.90–0.92 · SOC 별 산포 ×12 · SOC 당 ≈하루 · 노화 0) · 세미나 3번째(Sun 2025 — 학습형 · 적합 라벨과의 상관)와 대조 — 둘 다 "EIS 가 모드를 가르는가" 를 참값으로 시험 0 · 우리 쪽이 공급할 수 있는 시험은 설계 메모만(코드 0 — RUN_SCOPE 밖 별도 승인).
- ★★★ **(e) 후속**: 새 행 열아홉(★★★ 셋 — 연재 [4] OCV · 창 · [2] EVS-35 구조적 식별성 근거 · [5] 셀 안 양극 OCP / ★★ 여덟 — Danzer 2019 지목 누락 보충 포함 / ★ 여덟) · 재지목 셋(Jobman 2015 → 2 · Chu 2020 Part II → 2 · Wan 2015 → 3) · 재지목 안 함(Schmalstieg 2018 · Waag 2013 · Hahn 2019 — 목록 · 인용처) · 지목 누락(재지목 안 함) Schönleber 2014(18호 ★★).
- **채움표 96호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나 — LPM 의 C̄dl · k̄0 면적 비례 · `θ(N)` 0/96) · Q2 없다 · Q3 층 하나(적합 + 합성 참값 하나 · 실셀 값이 같은 편 경계 밖) · Q4 ASSB 0/96 **여든여덟 번째 성질**(도구 칸) · Q5 해당 없음 · Q6 없다 · Q7 해당 없음 · Q8 층 하나(MSMR OCP — 흑연 teardown 기반 · NMC 셀 안 재보정).
- **곱 축퇴 처방 일흔아홉 번째 적용**: 적용 불가(액체 · 접촉 0 · 노화 0) — 처방 1단계("R · C 를 같이")의 집약 모형판(전극별 C̄dl · k̄0 — `[해석·대수]` k̄0/C̄dl 면적 불변 · 변화비만) · 곱 문장 셋(R̄ct = RT/(F²Σṅ̄0,j) · a_sALC_dl · R_c ↔ 1/κ̄^s 합) · 단서(노화 0 · 배정 가정 — 실셀 C̄dl 초기 ↔ 최종 순서 뒤집힘 · CPE · 우리 대수) · 후보 메모 하나 · 새 줄 0.
- ⚠ 어긋남 17 건(D1 "highly accurate" ↔ 전체 집합 · D2 표 VI ↔ 부록 범위 · D3 그림 11 캡션 14 ↔ 13 · D4 갤러리 수 셋 · D5 SOC 19 ↔ 20 · D6 D̄s,ref^p 초기 ×7.1 경계 밖인데 수렴 · D7 '표준 정규' ↔ N(0, 0.2) Ω · D8 "realization" · D9 "as previously discussed in Fig. 5" · D10 "Wan et al.68" · D11 [49] = [52] · D12 D̄s 자릿수 · D13 그림 표기 넷 · D14 단위 · D15 "Nondestructive" ↔ teardown 기반 OCP · D16 그림 15(e) 평균선 · D17 Rabissi "40%").
- PDF 메타데이터: `PDF 1.7` · creator "IOPP" · producer "iTextSharp™ 5.5.13.4 … modified using iText® 5.5.13.5 …(IOP Publishing Ltd; licensed version)" · author "Dongliang Lu" · subject "Journal of The Electrochemical Society, 169(2022) 080504. doi:10.1149/1945-7111/ac824a" · 생성 2022-08-04 18:15:19 +05'30' · 수정 2026-10-02 13:45:02 +01'00'(호출자 메모와 같음 — 내려받기 시각 · p. 1 표지 "13:45" 와 같은 분) · XMP 6,012 B(VoR · MajorVersionDate 2022-08-05 · crossmark) · PageLabels 1–29 · p. 23 가로 · 래스터: 표지 둘 + 그림 19 · 벡터 그림 0 · 합자 256(NFKC 로 복원) · `%%EOF` 1.
- 보류 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(야): **(다)(샤)(뱌)(세)** 근거(강) · (피)(베)(테)(이)(치)(헤)(체)(야)(무)(루)(에)(차) 근거(중) · (가)(페)(메)(제)(냐)(먀)(케) 약 · (라)(마)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 셋("식별 가능" 주장의 층 표기 — 구조적 ↔ 선형 ↔ 실제적 · 최종 매개변수 표 ↔ 같은 편 경계 · 물리 범위 폐합 검사 + 합성 참값의 경계 위치 표기 · DRT 봉우리 → 전극 배정 규칙 표기 + 최종 적합의 배정 유지 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 96호 행 · 96편 누적 · Evidence 아흔한 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](정의 표 새 줄 "셋째 줄의 선형화(소신호) 손 분석 + 단일 실행 합성판" · 96호 절 · 처방 25 · 주장하지 않는 것) · [[spm-grouped-parameter-identifiability]](적용 표 96호 세 행 · 한계) · [[drt-peak-count-nonidentifiability]](여덟 번째 경보 · 체크리스트 96호 행 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](일흔아홉 번째 적용 · 주장하지 않는 것) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: 새 개념 페이지("집약 모형 EIS 식별성") 만들지 않음 — [[spm-grouped-parameter-identifiability]] 적용 표 · [[drt-peak-count-nonidentifiability]] 여덟 번째 경보로 충분 · [[halfcell-ocp-shape-invariance]] · [[halfcell-window-parametrization-lineage]] 변경 안 함(연재 [4 · 5] 미열람 — 이 편은 그 값을 입력으로 쓸 뿐 · 연결은 digest 참고문헌 표로) · [[zhang2020-eis-aging-dataset]] 변경 안 함 · 원 참고문헌(27 · 28 · 51 · 95호 · sun2025 인용분) 다시 열지 않음 — digest 전사 대조 · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행(✅ 96호 흡수 · 지목 칸 "27 | 1" 그대로 · 등급 ★★★ 그대로(27호 ★★★★ 표시만)) · 재지목 열(Jobman 2015 → 2 · Chu 2020 Part II → 2 · Wan 2015 → 3) · 새 행 19(★★★ Lu 2021 *JES* 168, 070533 [4] · ★★★ Plett & Trimboli 2022 EVS-35 [2] · ★★★ Lu · Trimboli · Plett 2022 *JES* 169, 070524 [5] · ★★ Lu 2021 *JES* 168, 070532 [3] · ★★ Lu 2021 *JES* 168, 080533 [6] · ★★ Guest 2020 *JES* 167, 160546 [7] · ★★ Chu 2019 Part I [10](95 · 96) · ★★ Rabissi 2021 [41] · ★★ Murbach 2018 둘 [28 · 29] · ★★ Danzer 2019 [69](11 · 96 — 지목 누락 보충) · ★★ Ciucci & Chen 2015 [68] · ★ Rodríguez 2018 [62] · ★ Kong 2020 [64] · ★ Oldenburger 2019 [76] · ★ Meddings 2020 [14] · ★ Oca 2021 [1] · ★ Zhang Q. 2022 [42] · ★ Duan 2022 [43] · ★ Verbrugge & Koch 2003 + Baker & Verbrugge 2012 [50 · 48]) · 지목 누락 기록(Schönleber 2014 — 18호 ★★ · 행 신설 여부 호출자 판단) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 56 행.
- 후속(서지 기준, 미열람): **Lu D. 외 2021 *JES* 168, 070533**([4] — OCV · 전극 창 · 우리 α·β 창 맞춤의 액체 판) · **Plett G.L. & Trimboli M.S. 2022 *Proc. EVS-35***([2] — 구조적 식별성 주장의 유일한 근거) · **Lu D., Trimboli M.S., Plett G.L. 2022 *JES* 169, 070524**([5] — 셀 안 양극 OCP 재보정) · Lu 외 2021 *JES* 168, 070532([3]) · Lu 외 2021 *JES* 168, 080533([6]) · Guest B., Trimboli M.S., Plett G.L. 2020 *JES* 167, 160546([7]) · Chu Z. 외 2019 *J. Energy Storage* 25, 100828([10] — 이 편 TF 의 출처) · Rabissi C. 외 2021 *Energy Technol.* 9, 2000986([41]) · Murbach M.D. 외 2018 *JES* 165, A2758 · A297([28] · [29]) · **Danzer M.A. 2019 *Batteries* 5, 53**([69] — 지목 누락 보충) · Ciucci F. & Chen C. 2015 *EA* 167, 439([68]) · Jobman 2015([8] — 재지목 → 2) · Chu 2020 Part II([66] — 재지목 → 2) · Wan 2015([74] — 재지목 → 3) · Rodríguez 2018 · Kong 2020 · Oldenburger 2019 · Meddings 2020 · Oca 2021 · Zhang Q. 2022 · Duan 2022 · Verbrugge & Koch 2003 + Baker & Verbrugge 2012 · 재지목 안 함(목록 · 인용처): Schmalstieg 2018([87]) · Waag 2013([38]) · Hahn 2019([71]) · 지목 누락(재지목 안 함): Schönleber 2014 *EA* 131, 20([34] — 18호 ★★).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 134).

## [2026-10-02] ingest | assb 97호 — Koerver R., Zhang W., de Biasi L., Schweidler S., Kondrakov A.O., Kolling S., Brezesinski T., Hartmann P., Zeier W.G., Janek J. 2018, Chemo-mechanical expansion of lithium electrode materials – on the route to mechanically optimized all-solid-state batteries (Energy Environ. Sci. 11, 2142–2158)
- raw: `raw/papers/koerver2018_chemo-mechanical-expansion-molar-volume-ocv-pressure-stress.md` (sha256 봉인 27c998f5…8c59af50 — `pdf_sha256` 0d6fe3ef…6cb04c9d · 3,035,900 B · `si_sha256` 2bf312f5…93728d36 · 4,901,307 B · 호출자 sha256 둘 다 일치(직접 재계산) · 예치 원자료 0) · 그림 `raw/figures/koerver2018_chemo-mechanical-expansion-molar-volume-ocv-pressure-stress/` (자동 15 = 본문 `fig_1 … fig_5` · `tab_1` + ESI `fig_S1 … fig_S8` · `tab_S2`(본문 `SI_TAG` False · ESI True — 호출자 확인대로) + **수동 10**(표 1 · S1 · S2 · S3 · S4 단독 · 그림 S1 · S2 · S5 · S6 · S8 — 300 dpi) · **연 것 25/25** · 자동 크롭 문제(그림 S1 · S6 · S8 아래 끝 잘림 — 축 이름 · 축척 막대 · 그림 S2 · S5 · 표 1 · 표 S2 과대 영역 · 표 S1 · S3 · S4 미검출 · 캡션 필드 900 자 잘림(그림 4 · S3 · S4) · 본문 섞임(그림 S1 · S2 · 표 S2)) 은 `figures.json` note 에 · 본문 그림 다섯 전부 래스터 — 화소 판독 · 식 · 표 머리 · 단위는 쪽 렌더 조각(판독용 · 커밋 안 함).
- **4차 묶음 파일 57**(원장 §1 요청 14 편 중 일곱째 · 2026-10-02 사용자 공급) · **원장 최다 지목 13 편** — 각 digest 후속 절 grep 재확인 4 · 27 · 33 · 37 · 41 · 53 · 59 · 73 · 75 · 81 · 82 · 87 · 94 = **13 — 원장 일치**(교차: 62호 "이 편 이후" · 93 · 95 · 96호 관계 문장 · 오탐 셋 제거) · ⚠ 23호(큐 22 Koerver 2017 *Chem. Mater.*) · 64호(Koerver 2017 *JMCA*)와 다른 편 · JLU Giessen + KIT BELLA + BASF SE + TH Mittelhessen · © RSC 2018(OA 0) · 본문 17 쪽(인쇄 2142–2158) · 그림 5 · 표 1 · 식 (1)–(12) · 참고문헌 [1]–[115](빠진 번호 0) · ESI 10 쪽(그림 S1–S8 · 표 S1–S4 · 식 (S1)–(S11) · SI 참고문헌 3) · 우리 digest 열하나를 인용(22 · 23 · 62 · 63 · 64 · 66 · 69 · 70 · 71 · 72 · 78호) · 4차 묶음 13 편 인용 0.
- ★★★★ **(a) 부피 변화**: 잰 것은 **LCO 격자 하나**(Mo-Kα operando XRD · 액체 파우치 · 0.1C · 25 °C) · NCM 곡선 = 69 · 66호 재수록 · 흑연 = Schweidler 2018 · NCA 는 캡션 출처 목록에 없음(D18) · 수평선(Li 12.97 · In/InLi 7.89 · LFP 11.62 · Si 8.85 · LTO ≈0)은 문헌 · `[도표·화소]` 계열마다 첫 점 0(NCM x ≈0.89–0.93 · LCO 0.985 — 94호 G9 "χ 0.912 위 자료" 0) · `[재현]` 그림 2(b) V̄m 이 같은 지면 부피 % × 식 단위 몰부피의 층상 ≈×3(NCM-811 ×2.9 · LCO ×2.5–2.7) · LFP ×3.8 · 흑연 ×0.95 ✅ — 지면은 "per formula unit" · Z 배수 의심(D15 · 원인 미확정) · "V̄m(Li) > Li 금속 몰부피" 명제가 이 배수에 걸림.
- ★★★★ **(b) 압력 의존 OCV**: In ‖ LTO · LCO ‖ In 셀 하나씩 · 25 °C · hot-press([115]) · 오름 램프 다섯(그림 S1 ≈49–235 MPa · 인쇄 톤 다섯 ↔ MPa 넷 — D8) · 표 S1 **0.122 mV MPa⁻¹** → V̄′(In/InLi) 11.81(결정학 7.89 의 ×1.497) · 표 S2 LCO 0.023–0.102 mV MPa⁻¹ — 기준 둘(7.89 → −1.95 … +5.70 · 11.81 → +1.97 … +9.62: 부호 반전은 7.89 에서만 — D16) · 초록 "1 mV/100 MPa" ↔ 측정 2.3–12.2 mV/100 MPa(D1) · OCV 안정 기준 "0.005 V s⁻¹"(D10) · `[재현]` 우리 OCV 맞춤에 압력 항 — 60–65 MPa 면 In/InLi 상수 +7.3–7.9 mV · 20 MPa 차 2.4 mV · LCO 형상 왜곡 ≈4.7 mV(60 MPa · x 0.65 ↔ 0.80) — 우리 수치는 RESULTS*.md 정본(옮기지 않음).
- ★★★★ **(c) 운전 압력**: 35 kN ≈445 MPa(`[재현]` 445.6) · "approximately 70 MPa"(명목 · 23 · 64호와 같은 문장) · 10 Nm "60 ± 8 MPa"(토크 교정) · 로드셀 KMT 55 계측 ≈61–65.5 MPa(그림 S5 · 휴지 16 h −3.6 · 사이클 92 h ≈−4 · 빈 케이스 −3.9 MPa / 69 h — PEEK) · **59호 "143 MPa" = OCV 램프 셋째 계단**(59호 D9 해소) · **33호 "445 / 70" = 실험 절 인쇄**(명목) · `[도표]` Δσ11 LCO +0.057(= 62호 자료 — 그림 4a "data from ref. 11" · 원장 "같은 측정 계열인지 미확인" 확인됨) · NCM −0.045 · NCA −0.053 · Li +1.48 · 흑연 +0.65 · InLi +1.08 MPa · 본문 "+0.6 MPa"(×10 — D2) · "ten- to twenty-fold"(×26–33 · ×11–14 — D7) · 'agree very well' = 계산 ↔ 계산(측정 몫 0.20 · 0.04 % — D6) · 인쇄 σ22 = −3Kε0(SI 경로 S10 → S11 재현 안 됨 — D4) · NCM σ22 부호(D3) · 표 S3 ↔ S4 pL(D5) · `[재현·가정]` 겉보기 강성 0.085–0.40 MPa µm⁻¹(셀 탄성의 1/110–1/510).
- ★★★ **(d) 표 1**: 측정 0 · 21 행 문헌(이론 12 · 박막 1) · `[재현]` 등방 폐합 17 행 ±5 % · 위반 넷(Li G 4.2 ↔ 1.73 · α-Si G > E/2 · γ-Li₃PS₄ K +24 % · Li₇P₃S₁₁ K −8 % — D14) · 각주 "eq. a1" 부재 · NCM-811 행 없음(SI "198 GPa (see Table 1)" — D13) · 82호 "194 GPa" = 이 표에서 LiMn2O4 이론값과 같은 수(확정 아님).
- ★★★ **(e) 혼합 · zero-strain**: 응력 측정 하나(셀 하나 · 한 사이클 그림 · 끝점 ≈0) + SEM/EDX 한 시야(그림 S7 — 대조 S8 = 23호 재수록) · 55 : 45 도출 · 용량 · 유지율 · 셀 수 0 · 초록 "better cycling performance" 근거 0 · `[재현·가정]` 단일 셀 Δx 대입 시 순 +0.00091 cm³ g⁻¹(상쇄가 창 · Δx 분배에서 왔을 수 있음) · zero-strain 은 문헌[55, 56, 60–62] · 특허[106] 인용.
- ★★★ **(f) 13 편 기대 대조**: ✅ 7(33 · 41 · 53 · 59 · 73 · 81 · 87) · 부분 5(4 · 27 · 37 · 75 · 94) · ❌ 1(82 — "대칭 셀 6 h 평형" 지면 0).
- **채움표 97호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 없다(층 하나 — 접촉 손실 서술 · 혼합 SEM · 겉보기 강성 · `θ(N)` 0/97) · Q2 없다(상대극 교체 · 모드 분리 0) · Q3 층 하나(수동 기저선 · 계산 ↔ 계산 일치 · 문헌 표) · Q4 0/97 **여든아홉 번째 성질**(일치 명제 둘이 비교 쪽 선택에서만) · Q5 층 하나(**서른다섯 번째 형태** — In/InLi 압력 계수 0.122 mV MPa⁻¹) · Q6 층 하나(명목 ↔ 교정 ↔ 계측 한 지면) · Q7 해당 없음 · Q8 층 하나(LCO V̄m(x) · ∂E/∂p(x)).
- **곱 축퇴 처방 여든 번째 적용**: 적용 불가(접촉 · 노화 0) — 62호 압력 채널 곱 `ΔP = k_eff · Σ Δh_e` 의 정량판(겉보기 강성 ≈×5 · 1/110–1/510 · 기저 표류 70–90 × 양극 신호 · 상대극 ×11–33) · 곱 문장 셋(Δp = −ε_vol·K · "pore filling … strain" · `k_app` `[재현·가정]`) · 후보 메모 하나 · 새 줄 0.
- ⚠ 어긋남 23 건(D1 "1 mV/100 MPa" · D2 "+0.6 MPa" · D3 NCM σ22 부호 · D4 σ22 경로 · D5 pL 두 표 · D6 "agree very well" · D7 "ten- to twenty-fold" · D8 톤 다섯 ↔ MPa 넷 · D9 90 ↔ 140 µA · D10 0.005 V s⁻¹ · D11 운전 압력 셋 · D12 참조 오류 · D13 eq. a1 · 198 GPa · D14 표 1 등방 위반 · D15 그림 2b 배수 · D16 부호 반전 기준 · D17 6 % @4.3 V · D18 NCA 출처 · D19 [88] · D20 표 S1 · S2 머리 · D21 그림 4a 셀 · D22 "As shown in Fig. 2" · D23 표기).
- PDF 메타데이터: 본문 `PDF 1.3` · 17 쪽 595.3 × 779.5 · creator "Aspose Ltd." · producer "Aspose.PDF for .NET 22.3.0" · author "Raimund Koerver" · title 의 en 대시가 "&#x2013;" 엔티티 문자열 · subject "Energy & Environmental Science (2018), 11, 2142-2158, doi:10.1039/C8EE00907D" · 생성 2018-08-04 15:30:35 +05'30' · 수정 2026-03-16 19:19:24 +00'00'(호출자 메모와 같음) · XMP 3,585 B(publicationDate · crossmark 2018-08-04) · 카탈로그 /JT · /FICL:Enfocus · PageLabels 시작 5 · 래스터 그림 다섯 + 아이콘 넷 · 합자 99 / ESI 헤더 1.3 · 카탈로그 /Version 1.4 · A4 10 쪽 · "Microsoft Word - Supporting Information.docx" · "Aspose.Pdf for .NET 9.3.0" · 생성 2018-03-28 05:28:14Z(= 접수일) · 수정 2018-05-29 10:02:25(= 수락일) · XMP 237 B(빈) · 그림 S3 · S4 벡터.
- 보류 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(캬): **(하)(노)(캐)(해)(댜)(세)(먀)** 근거(강) · (태)(이)(치)(냐)(재)(제)(모)(보)(소)(체) 근거(중) · (오)(리)(터)(애)(대)(미)(초)(랴)(네)(메)(너) 약 · (바) 결정 유지 — 근거 추가(이 편이 (바) 의 '닿는 논문') · (라)(마)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷(요약 수치 ↔ 같은 편 표 · 축 자릿수 대조 · 유도 열역학량의 기준 · 몰 기준 · 정규화 표기 · "계산 ↔ 실험 일치" 의 측정 몫 · 비교 축 표기 · (선택) 처방 효과의 측정 여부 표기 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 97호 행 · 97편 누적 · Evidence 아흔두 번째 · 새 제약 6 · Status Log · 주장하지 않는 것) · [[assb-maxwell-ocv-derivative-channels]](§3 다음 97호 절 — 계보 첫 ∂E/∂p 실측 · `evidenceScope` single-source → multi-source-primary · 주장하지 않는 것 · 관련) · [[assb-operando-pressure-signal-attribution]](표본 표 97호 행 · 62호 계열 "미확인" → 확인 · 함정 정량 메모 · 적용 · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](97호 절 — 운전 압력 다섯 층 · 143 해소 · "1 mV/100 MPa" 논거 자릿수 · 59호 절 주석 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](여든 번째 적용 · 주장하지 않는 것) · [[assb-li-in-reference-potential-window]](서른다섯 번째 형태 · 주장하지 않는 것) · [[nmc-lattice-li-content-calibration]](97호 절 — 하류 사용 · 첫 점 정규화 · −6 % ↔ −4.9 %) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: 새 개념 페이지("화학-기계 팽창 · 부분 몰부피") 만들지 않음 — 압력 채널 · Maxwell · 교정 개념에 절로 충분 · DEM/MPM 쪽 파일(다른 브랜치 소유)은 읽지도 고치지도 않음 — 그림 2 곡선의 DEM 입력 가능성은 사실(층위 · 정규화 · 배수)만 digest 에 · 원 참고문헌(22 · 23 · 62 · 63 · 64 · 66 · 69 · 70 · 71 · 72 · 78호 인용분) 다시 열지 않음 — digest 전사 대조 · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행(✅ 97호 흡수 · 지목 칸 13 그대로) · 재지목 열둘(Tian & Qi 2017 → 4 · Busche 2016 → 2 · Zhang W. 2017 *ACS AMI* 35888 → 5 · McGrogan 2017 → 2 · Ohzuku 1995 *JES* → 5 · Sakuda 2013 → 4 · Yang 2016 → 2 · Deng 2016 → 2 · Cheng 2017 NCM → 2 · Weber 2016 → 2 · Ito 2014 → 3 · Wenzel 2016 → 2) · 새 행(★★★ Schweidler 2018 [36] · ★★ Meethong 2007 [69] · Sauerteig 2017 [39] · Cannarella & Arnold 2014 [18] · Qi 2014 [82] · Qi 2010 [97] · Monroe & Newman 2005 [75](지목 누락 보충 — 61 · 97) · ★ Reimers & Dahn 1992 [42](지목 누락 보충 — 62 · 97) · Christensen & Newman 2006 [67, 68] · Rosciano 2014 특허 [106] · Shenoy 2010 [98](89 ☆ · 97) · Yamada 2005 [38] · Wang J.W. 2013 [58] · Rieger 2016 [41] · Mukhopadhyay & Sheldon 2014 [1] · Kraft 2017 [100]) · §3-b 표시(위) · TRANSFER_NOTE §6-3-j 파일 57 행.
- 후속(서지 기준, 미열람): **Schweidler S. 외 2018 *JPCC* 122, 8829**([36] — 흑연 V̄m · operando XRD + in situ 압력) · Tian & Qi 2017([30] — 재지목 → 4) · Busche 2016([115] — OCV–압력 장치 · 재지목 → 2) · **Meethong N. 외 2007 *ESSL* 10, A134**([69] — 응력 → Li 용해도) · **Sauerteig D. 외 2017 *JPS* 342, 939**([39] — 전극 층위 팽창) · **Cannarella J. & Arnold C.B. 2014 *JPS* 269, 7**([18] — 응력 → SOH · SOC) · **Qi Y. 외 2014 *JES* 161, F3010**([82]) · **Qi Y. 외 2010 *JES* 157, A558**([97]) · **Monroe C. & Newman J. 2005 *JES* 152, A396**([75] — 지목 누락 보충) · **Reimers J.N. & Dahn J.R. 1992 *JES* 139, 2091**([42] — 지목 누락 보충).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 135).

## [2026-10-03] ingest | assb 98호 — Raijmakers L.H.J., Danilov D.L., Eichel R.-A., Notten P.H.L. 2020, An advanced all-solid-state Li-ion battery model (Electrochim. Acta 330, 135147)
- raw: `raw/papers/raijmakers2020_thin-film-assb-model-double-layer-dc-ac-joint-fit.md` (sha256 봉인 14a949ea…6f5ba652 — `pdf_sha256` e21931c8…e1b93018 · 3,754,525 B · 호출자 sha256 일치(직접 재계산) · SI 없음(보충 언급 0 — 부록 A 는 본문 안 · 직접 다시 셈) · 원자료 · 코드 공개 0) · 그림 `raw/figures/raijmakers2020_thin-film-assb-model-double-layer-dc-ac-joint-fit/` (자동 13 = `fig_1` · `fig_3 … fig_11` · `tab_1 … tab_3`(SI 오판 0 — `SI_TAG` False 를 실행 전 확인) + **수동 4**(그림 2 — 자동 누락 · 표 1–3 단독 — 300 dpi) · **연 것 17/17**(재개 실행에서 직접) · 자동 크롭 문제(그림 2 누락 · 표 셋 쪽 전체 과대 · 표 1 · 2 캡션 필드에 표 글자 · 표 2 900 자 잘림 · 그림 캡션의 텍스트 층 대체 문자) 는 `figures.json` note 17 에 · 래스터 여섯 화소 판독 · 벡터 셋 경로 판독 · 식은 쪽 렌더 조각(판독용 · 커밋 안 함)). `raw/figures/_sources.json` — 이 편 항목(17) 추가 · 다른 항목 변화 0.
- **4차 묶음 파일 58**(원장 §1 요청 14 편 중 여덟째 · 2026-10-02 사용자 공급) · 원장 행 "★★★ … 26 · 37 | 2 | Q4·Q3" · 지목 26호 §11(★★★★ [10]) · 37호 §14([14] — 등급 칸 없는 후속 표) = **2 = 원장 일치**(91호 :618 = 교차 참조 · 92–96호 · 27호 = 관계 문장 — 지목 아님) · FZ Jülich IEK-9 + TU/e + RWTH + UTS · © 2019 Elsevier(OA 0) · 19 쪽 · 그림 11 · 표 3 · 식 (1)–(32) + 부록 (A.1.1)–(A.14) · 참고문헌 [1]–[42](빠진 번호 0) · 우리 digest 하나 인용([11] = 91호) · 4차 묶음 13 편 중 [11] · [28](파일 61) · [31](파일 62) 셋 인용 · ⚠ **재개 작업** — 앞 작업이 컨테이너 재시작으로 끊긴 것을 2026-10-03 에 이어받음 · 상태 메모 · 본문 조각은 근거로 쓰지 않고 메타데이터 · 본문 · 식 렌더 · 그림 17 · 재풀이를 이 실행에서 다시 확인(메모와 다른 값 — 그림 9 1C 판독 · 그림 11c 표지 중심 · 그림 3 몸통 RMS · 그림 4 이완 잔차 · 인용 순서 하나 — 는 이 실행 값으로 고침).
- ★★★★ **(a) 표 3 층위**: 21 행 = 직접 측정 2(T · A) · SEM 2(L · M — SEM 그림 0) · 사전 고정 3(α^p · α^n · c_Li) · EMF 유도 1(c_max) · **무각주 적합 13**(본문 "optimized") + 함수 둘(β(x) 그림뿐 · EMF 외삽) · 26호 '문헌값' 10 = 이 편 적합 9 + EMF 유도 1(측정 0) — 26호 G4 '예' · ×1.0500 관계는 이 편 인쇄값 기준으로 선다(일곱) · `D_e⁻` 원래 값 5.06×10⁻¹³(적합 · D_Li⊕ ×4.18 공통 β) · 26호 ρ 18.3 고정 = 이 편 적합값 · `[재현·대수]` 이름 ×1.05 뒤 조합은 움직임(D⁰_p ×1.30 · 경계 분배 0.807 → 1.00 · σ ×1.10 · i₀ ×1.08–1.13).
- ★★★★ **(c) 재풀이**: `[재현]` 표 3 그대로 전해질(식 23–25) 1C −3.82 · −70.02 · −73.84 ↔ 그림 6c −3.3 · −69.8 · −73.4 · 4C −296.73 ↔ −295.1 mV · k_r 인쇄 = 그림(×0.1 이면 1C −87.2 · 4C 고갈 — 91호 ×100 과 반대) · 벌크 옴 326.2 ↔ ≈327 · R_ct^n 43.9 ↔ ≈44.0 · R_ct^p 67.1 ↔ ≈67.3 · 합 455.7 ↔ ≈457 ✅ / ★ **음극 계면은 인쇄 식 (12) · (16)(두 계면 같은 j_bat → 방전 중 환원) 글자 그대로의 계산과만 맞음** — 그림 9e 4C −23.9 ↔ −23.8 mV(물리 −36.8 · 농도비 없이 34.0) · 9f 삽도 이완 부호(≈−24 → ≈+5 mV) · 11c 유도성 고리(`[재현·대수]` Gerischer 최저 (38.1, −3.2) · 10 mHz 끝 35.6 ↔ 그림 ≈(38.3, −3.4) · ≈35.6 · 물리 방향이면 축 위 · 끝 52.3) — 본문은 그 고리를 물리로 읽음(D1 · 코드 미공개 · 1C 는 판독 폭 안 · 성능 몫 ≈3 %).
- ★★★★ **(c) 검증**: 같은 자료가 '검증' 이자 '결정'(p. 2 "Since both DC and AC impedance measurements are used for model validation, it is to be expected that the model parameters can be determined much more accurately") · 보류 0 · 이완의 적합 여부 미인쇄 · `[도표·벡터]` 몸통 RMS 1.2 · 1.8 · 2.0 · 5.1 · 19.1 · 47.6 mV(0.1 · 0.5 · 1 · 2 · 4 · 6C — 측정 끝 용량의 5–80 %) · 4C · 6C 첫 1–2 분 −45 … −103 mV · 끝 용량 0.972 · 0.2C 이완 한 방향(≈+22 → +2.5–6 mV) · EIS 꼭대기 ≈157 ↔ ≈171(+9 %) · 예측(모의만)은 D 바꾸기 둘 — 그림 10e 모의는 ≈0.246 mAh cm⁻² · ≈3.74 V 에서 컷오프 없이 끝남(D9).
- ★★★ **(b) 이중층**: 기하 면적당 축전기(표 2 "per unit area" · 실제 계면 0) · `[재현·대수]` 숨은 면적 인자가 k · c_dl 에 같은 배수 → R_ct·C_dl 면적 불변 · 값 = DC + AC 적합 · `[재현·가정]` c^n_dl = c_geo ×5.4 · 등가 유전 두께 0.67–2.2 µm(공간전하층 값 아님) · c^p_dl 22–72 nm · τ_n 0.76 µs ↔ τ_LiPON 1.06 µs(겹침) · "작은 영향" = 대역 논증 + [26, 42] · 37호 F(전극 전체) 꼴 · A_eff 는 조상에 없는 변형 · 37호 값 ×12.2 · ×9.5(수치 상속 0) · 각주 글자 셋만 상속 · 91호 "5.1" 단서는 이 편 경유 아님.
- ★★★ **(a) C-rate · 용량**: 1C = 0.7 mA(공칭 · `[재현]` 71.1 · 13.0 분 = 그림 6 · 7 폐합) ↔ EMF 1.172 mAh(×1.67) · 0.1C ≥1.09 mAh · 26호 Q_ideal 1.23 = EMF × 1.05 → 26호 '1C' 가 Q_ideal 기준이면 ×1.76(26호 G2 · D4 의 데이터 쪽 전제 확인).
- ★★★ **(d) 계보**: 91호 → (Kazemi 2019 [18]) → 이 편 — 바뀐 물리 일곱(쌍극 · β(x) · 음극 BV · 이중층 둘 · 기하 축전기 · 직렬 ρ_s) · 같은 값 0 · 회복 둘(k_r 인쇄 = 그림 · k₁ˢ 단위 관례) · 유지 둘(용량 맞춤 · 같은 데이터 외삽 평형) · n⁻ = 공공(91호 D15) · 이원 가정 몫 ≈71 % → ≈8 %(`[재현·가정]`).
- **채움표 98호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(층 하나 — 면적 인자 × k · c_dl · `θ(N)` 0/98) · Q2 없다(층 하나 — DC + AC 한 벌 · 성분 분해는 모형 배정) · Q3 층 하나(무각주 13 동시 적합 · 하류 '문헌값' · 재풀이 ✅ / 음극 방향 ❌) · Q4 0/98 **아흔 번째 성질** · Q5 해당 없음(층 하나 — 음극 계면 항 · LiPON 호 겹침 · 방향) · Q6 해당 없음 · Q7 해당 없음 + 공백 · Q8 층 하나(율 외삽 EMF · c_max 유도).
- **곱 축퇴 처방 여든한 번째 적용**: 입력 점검 대부분 ❌ · 1단계 형식 ✅(R · C 같이)이나 c_dl 기하 면적당 적합 · 곱 문장 셋(A·k · c_dl 면적당 → R·C 불변 · c_max EMF 유도) · 후보 메모 하나(축전기 면적 기준 표기) · 새 줄 0.
- ⚠ 어긋남 19 건(D1 음극 방향 · D2 (18.3) ↔ (18.4) 부호 · D3 (23.3) · (23.4) 차원 · D4 (5) · (6) ↔ 그림 9 합산 · D5 (28) · (29) ↔ (30) 부호 규약 · D6 0.7 ↔ 1.172 mAh · D7 Δx 0.5 ↔ 0.49 · D8 3.9 V ↔ x 0.80 · 0.864 · D9 그림 10e · D10 이완 축 · 0.1C · '모든 조건' · D11 '넓은 율 범위' · D12 red ↔ 검정 · D13 p > n 이유 · D14 'Chairs of Phosphates' · D15 x 두 뜻 · D16 Li⁰ · D17 부록 기호 재사용 · D18 단위 표기 · D19 일반화 문장).
- PDF 메타데이터: `PDF 1.7` · 19 쪽 595.3 × 793.7 · creator "Elsevier" · producer "Acrobat Distiller 8.1.0 (Windows)" · author "L.H.J. Raijmakers" · subject "Electrochimica Acta, 330 (2020) 135147. doi:10.1016/j.electacta.2019.135147" · 생성 2019-12-05 22:10:06 +05'30' · 수정 22:10:59(호출자 메모와 같음) · XMP 7,068 B(VoR · coverDate 2020-01-10 · crossmark MajorVersionDate 2010-04-23) · StructTreeRoot · PageLabels 1 부터 · 래스터 그림 여섯 + p. 1 셋(로고 · 표지 · CrossMark) · 합자 154(NFKC 로 복원) · `%%EOF` 1.
- 보류 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(햐) · (겨): **(세)(먀)(체)(제)(대)(햐)** 근거(강) · (에)(이)(치)(냐)(뱌)(쟈)(챠)(베)(루)(겨) 근거(중) · (다)(차)(무)(탸)(가)(피)(캬)(헤)(메) 약 · (마) 결정 유지 — 근거 추가(이 편이 '닿는 논문') · (라)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷(계면 반응 방향의 재풀이 폐합 · '문헌값 일치' 의 자료 독립성 · 축전기 항의 면적 기준 · 물리 범위 · 출처 · (선택) 'validated' 의 자료 층위 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 98호 행 · 98편 누적 · Evidence 아흔세 번째 · 새 제약 6 · Status Log · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](98호 절 · 처방 26 · 주장하지 않는 것) · [[spm-grouped-parameter-identifiability]](적용 표 98호 행 넷 · 한계) · [[assb-synthetic-truth-contact-loss-requirements]](R5 출처 · 상태 — 조상 근거 · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](여든한 번째 적용 · 주장하지 않는 것) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: 새 개념 페이지("DC + AC 결합 적합 · 축전기 면적 규약") 만들지 않음 — 위 다섯 페이지의 절 · 행으로 충분 · [[drt-peak-count-nonidentifiability]] · [[constrained-crb-identifiability]] 변경 안 함(DRT 0 · 이 편 모형의 FIM 계산 안 함) · 원 참고문헌(26 · 37 · 91 · 10 · 54호 인용분) 다시 열지 않음 — digest 전사 대조 · 26호 digest 의 k¹_s 단위 표기('mol^0.5' ↔ 이 편 'mol^−0.5')는 raw 불변이라 표시만 · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행(✅ 98호 흡수 · 지목 칸 "26 · 37 | 2" 그대로) · 재지목 넷(Tian & Qi 2017 4 → 5 · Reimers & Dahn 1992 2 → 3 · Danilov & Notten 2008 2 → 3(파일 61) · Xie 2008 1 → 2(파일 62)) · 새 행(★★★ Kazemi 2019 *SSI* 334, 111 [18] · ★★★ Li D. 2016 *EA* 190, 1124 + 210, 445 [32 · 33] · ★★ Larfaillou 2016 *JPS* 319, 139 [35](10 · 98 — 지목 누락 보충) · ★★ Fabre 2012 *JES* 159, A104 [12] · ★★ de Klerk & Wagemaker 2018 [26] · ★★ Haruta 2015 [42] · ★★ Braun · Yada · Latz 2015 [25](54 · 98) · ★ Aizawa 2017 + Yamamoto 2010 [23 · 24] · ★ Put 2018 [40] · ★ Xia 2006 [29] · ★ Zhang X. 2015 [41] · ★ Teichert & Oldham 2017 *JES* [16]) · 지목 누락 기록(Larfaillou 2016 — 10호 ★ · 이 편이 재지목하며 보충) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 58 행.
- 후속(서지 기준, 미열람): **Kazemi N. 외 2019 *Solid State Ionics* 334, 111**([18] — 계보 가운데 편) · **Li D. 외 2016 *Electrochim. Acta* 190, 1124 · 210, 445**([32 · 33] — EMF 외삽 방법 · LFP 노화 열화 모드) · **Larfaillou S. 외 2016 *J. Power Sources* 319, 139**([35] — 지목 누락 보충) · Fabre S.D. 외 2012 *JES* 159, A104([12]) · de Klerk & Wagemaker 2018 *ACS AEM* 1, 5609([26]) · Haruta 외 2015 *Nano Lett.* 15, 1498([42]) · Braun · Yada · Latz 2015 *JPCC* 119, 22281([25]) · Aizawa 2017 · Yamamoto 2010 · Put 2018 · Xia 2006 · Zhang X. 2015 · Teichert & Oldham 2017 · 재지목: Tian & Qi 2017([15] → 5) · Reimers & Dahn 1992([34] → 3) · 4차 묶음 도착(새 행 아님): Danilov & Notten 2008([28] — 파일 61) · Xie 2008([31] — 파일 62).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 136).

## [2026-10-03] ingest | assb 99호 — Kim Y., Lin X., Abbasalinejad A., Kim S.U., Chung S.H. 2019, On state estimation of all solid-state batteries (Electrochim. Acta 317, 663–672)
- raw: `raw/papers/kim2019_assb-ekf-soc-estimation-weak-observability.md` (sha256 봉인 efac82b3…6778fe90 — `pdf_sha256` a11bdbcb…dd494bbf · 1,903,854 B · 호출자 sha256 일치(직접 재계산) · SI 없음(보충 언급 0 — 직접 다시 셈) · 원자료 · 코드 공개 0 · 실험 0) · 그림 `raw/figures/kim2019_assb-ekf-soc-estimation-weak-observability/` (자동 10 = `fig_1` · `fig_2` · `fig_4 … fig_9` · `tab_1` · `tab_2`(SI 오판 0 — `SI_TAG` False 를 실행 뒤 확인) + **수동 6**(그림 2 · 3 분리 · 그림 5 · 6 왼쪽 축 포함 · 표 1 · 2 단독 — 300 dpi) · **연 것 16/16** · 자동 크롭 문제(그림 2 + 3 한 항목 병합 → 그림 3 누락 · 그림 2 · 5 · 6 왼쪽 축 잘림 · 표 둘 쪽 전체 과대 · 표 1 · 2 캡션 필드에 표 글자 · 표 2 900 자 잘림 · 그림 9 캡션 대체 문자) 는 `figures.json` note 16 에 · 벡터 여섯(그림 2–6 · 8) 경로 판독 · 래스터 둘(그림 7 · 9) 화소 판독 · 식은 쪽 렌더 조각(판독용 · 커밋 안 함)). `raw/figures/_sources.json` — 이 편 항목(16) 추가 · 다른 항목 변화 0.
- **4차 묶음 파일 59**(원장 §1 요청 14 편 중 아홉째 · 2026-10-02 사용자 공급) · 원장 행 "★★ … 12 · 37 | 2 | Q4" · 지목 12호 후속(:510 · ★★ 3 · [62]) · 37호 §14(:414 · [21] — 등급 칸 없는 후속 표 · 98호 Raijmakers 셈과 같은 처리) = **2 = 원장 일치**(91호 :618 = 교차 참조 · 26호 :390 = 인용 0 메모 · 27 · 93 · 95 · 96 · 98호 = 관계 문장 — 지목 아님) · 원장 §2 구조적 공백 1번 후보 · UM-Dearborn + UOIT + WSU Vancouver · © 2019 Elsevier(OA 0) · 10 쪽(인쇄 663–672) · 그림 9 · 표 2 · 식 (1)–(28) · 참고문헌 [1]–[23](빠진 번호 0) · 우리 digest 하나 인용([10] = 91호) · 4차 묶음 13 편 중 [10](파일 51) 하나만 인용.
- ★★★★ **(b) 관측성**: "weak observability" = OCV 평탄 논증("the equilibrium potential has a plateau, making the Jacobian to be almost zero and hence the battery system becomes very weakly observable") + 같은 계열 합성 플랜트 위 EKF 실행 하나 · 관측성 행렬 · Gramian · 야코비안 값 · CRB 0 · 대상 = 상태(SOC) · `[재현]` 식 (22) \|dE/dSOC\| 최소 0.072 V/SOC @SOC 0.28(θ 0.859 · 3.901 V) · ≤0.17 V/SOC 창 SOC 0.195–0.399 · 0.1–0.4 중앙 0.126 ↔ 0.4–0.99 중앙 0.658 · '거의 0' = 고 SOC 의 1/12.5 · 그림 9 EKF4 Δη_total(−7 … −11 mV) ÷ 기울기 = 그림 7 SOC 오차(600 s −0.045 ↔ −0.048 · 800 s −0.084 ↔ −0.087 · ×0.7–1.5) → **9 % = 편향**(모형 불일치의 증폭) · EKF3 의 남은 −0.018 … −0.046 은 출력 오차(≈−1.6 … +0.7 mV)로 설명 안 됨 · 미래 과제 '궤적 창' 은 분산만 줄인다 → **Q4 0/99 아흔한 번째 성질** · 원장 §2 후보 Kim 2019 = 식별성 편 아님(75 · 92호 닫음 형식).
- ★★★★ **(a) 전체 모형**: `[도표·벡터]` 그림 4 단면으로 식 (14) 둘째 항 −∫E = −6.76 · −8.56 · −11.92 · −14.45 · −19.18 mV ↔ 그림 3 η_mt −6.99 · −8.83 · −12.19 · −14.73 · −19.55(1 · 10 · 50 · 100 · 300 s · ±0.3) · Nernst 항 −1.01 … −18.44 mV 없음 · 그림 2 V − Eeq(θ̄) = 그림 3 η_total ±0.02–0.41 mV · `[재현]` 재풀이(표 1 · D_n⁻ 5.1 · 91호 c_max 2.33×10⁴ · c_min = c_max/2 · SOC₀ 0.99 · T 298.15 K · Nernst 항 없이) 10C V · η 셋 1–300 s ±0.5 mV · 3.4 V 도달 691.63 · 335.77 · 157.84 ↔ 689.40 · 334.56 · 157.18 s · 식 (14) 그대로면 모형 4 오차 RMS 13.0 → 27.6 mV(우리 재풀이 · 표 2 인쇄 14.3 · 펄스 3.4 → 8.0) — D1 · 코드 미공개.
- ★★★★ **(a) 표 1 · 2**: 머리 "[15]"(Tian & Qi 2017 접촉 면적 손실 모의) ↔ 본문 "the model presented in Ref. [10]" · D_n⁻ 표 1 2.1 ↔ 표 2 기준 · 그림 5.1×10⁻¹⁵(`[재현]` η_mt(0⁺) −6.15 ↔ 그림 −6.21 · 2.1 이면 −12.3) · k_pos 5.1×10⁻⁴ m³ mol⁻¹ s⁻¹ = 91호 k₁ˢ ×100 · 다른 단위 · 식 (17) 차원 불일치(수치 i₀ 0.277 · ≈0.88 mA) · 인쇄 k_r 0.9×10⁻⁸(91호 ×100 문제) 그대로 · 표 2 = 축약 오차 OAT(동기 "assessing parameter identifiability or estimability [19,20]") · 그림 5 · 6 벡터 오차 = 표 2 기준 행 그대로 · 펄스 M3 0.0027(일곱 행) = t = 0⁺ 한 점(α 0.6 ↔ 0.5 2.68 mV · 그림 6 첫 점 +2.68) · k_r · δ 행 0 — k_r ×10 · 8.0×10⁻⁷ · ×100 이면 M2 4.19 / 1.62 · 14.82 / 6.50 · 15.33 / 6.77 mV · k_pos ×1/100(86.9 mV) "not physically realistic" 배제 · D_Li⁺ ×1/100 "Not converged" = ≈26 s 고갈(한계 전류 0.25C · 인쇄 값 25.1C).
- ★★★ **(d) 37호 물음**: 접촉 · 용량 손잡이 0(상태 = 농도 마디 · 매개변수 고정 · SOC 분모 고정 · A 한 값이 경계 · 식 17 모두에) → 둘 다 모형 불일치 → SOC 편향 한 통로 · `[재현·가정]` A_eff ×0.5 → Δη_ct ≈−2.9 mV → 평탄 −0.040 · SOC 0.4 위 −0.0044.
- ★★★ **(c) EKF**: 합성 한 번 · 잡음 · Δt · 실현 수 미인쇄 · P0 I₇ / I₄ · Q_w Diag(10⁻³I₃, 9·10³, 10⁴I₃) / 10 I₄ · R_v 10⁻³ · 상태 정의 8 ↔ P0 7(그림 8 여섯 마디 합 64,908 = 6 δc₀ 보존 → 독립 전해질 3 + 양극 4) · 1.1 배 초기값이 EKF4 줄에 인쇄 ↔ 그림 8 EKF3 셋 11,880 출발 · `[도표·화소]` 그림 7 전류 5.04C / 2.50C · Actual SOC 0.708 · 0.435 · 0.156(300 · 600 · 900 s) ↔ 그림 2–6 기준 쿨롱 0.740 · 0.490 · 0.240 → 전류 ×1.10–1.11(V 600 s 3.908 ↔ 3.911) · V_meas 띠 p5/p95 −63 / +68 mV · '9 % → 5 %' = SOC 절대 %p · '40 %' = 44 %.
- ★★ **(e) 계보**: 91호 적합값(인쇄 k_r 포함) + Fabre [11] 평형 곡선(유리함수 · 분자 영점 θ 1.00319 · 분모 극 θ 1.00369 — 물리 범위 바로 위) 혼성 · 91호 '실험 검증' 은 이 조합에 옮겨지지 않음 · 서론 [10] '10 mAh' ↔ 91호 10 µAh.
- **채움표 99호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(층 하나 — F·A·k_pos 곱 · k_pos ×1/100 배제 · `θ(N)` 0/99) · Q2 없다(전압 하나 · 손잡이 0) · Q3 층 하나(합성 플랜트 Nernst 항 없음 · 표 1 ↔ 그림 · 혼성) · Q4 0/99 **아흔한 번째 성질** · Q5 해당 없음(Li 금속) · Q6 해당 없음 · Q7 해당 없음 + 공백 · Q8 층 하나(Fabre 유리함수 · 평탄 = 관측성 창 · 극).
- **곱 축퇴 처방 여든두 번째 적용**: 입력 점검 전부 ❌ / ⚠(모의만) · 곱 문장 셋(F·A·k_pos 한 곱 · k_pos ×1/100 배제 · 손잡이 없는 추정기의 편향 통로) · 후보 메모 하나(추정기 SOC 오차를 진단 신호로 쓰기 전 손잡이 · 증폭 표기) · 새 줄 0.
- ⚠ 어긋남 21 건(D1 Nernst 항 · D2 D_n⁻ · D3 [15] ↔ [10] · k_pos · D4 식 (17) 차원 · D5 식 (8) γ(c₀² 이어야) · D6 초기값 줄 · D7 상태 차원 · D8 그림 7 C-rate · D9 '10 mAh' · D10 '40 %' · D11 'six' · D12 절 안내 · D13 'Table II' · 'Figs. 4–7' · D14 'dt' · D15 'Li2CoO2' · 'charge transfer number' · D16 'Time (t)' · D17 α 두 뜻 · D18 M3 휴지 표류 · M4 차 · D19 [10] 저널명 · [11] 연도 · D20 '평탄 없음' 문장 · D21 'Not converged' = 고갈).
- PDF 메타데이터: `PDF 1.7` · 10 쪽 595.3 × 793.7 · creator "Elsevier" · producer "Acrobat Distiller 8.1.0 (Windows)" · author "Youngki Kim" · subject "Electrochimica Acta, 317 (2019) 663-672. doi:10.1016/j.electacta.2019.06.023" · 생성 2019-07-23 17:12:16 +05'30' · 수정 17:12:46(호출자 메모와 같음) · XMP 7,164 B(VoR · coverDate 2019-09-10 · crossmark MajorVersionDate 2010-04-23) · StructTreeRoot · PageLabels 663 부터 · 래스터 그림 둘(7 · 9) + 그림 1 조각 셋 + p. 663 셋(로고 · 표지 · CrossMark) · 합자 65(NFKC 로 복원) · `%%EOF` 1.
- 보류 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(햐) · (겨)–(며): **(세)(치)(쟈)(대)(체)(며)** 근거(강) · (뎌)(이)(탸)(챠)(먀)(냐)(햐)(샤)(무)(에)(겨) 근거(중) · (다)(차)(페)(루)(뱌)(녀)(헤)(갸)(가)(리) 약 · (마) 근거 0 · (라)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷('관측성' 주장의 산출물 표기(상태 추정판) · 인쇄 식 ↔ 그림의 항 폐합 · 표에 적힌 값 ↔ 계산에 쓰인 값 + 출처 번호 거슬러 확인 · (선택) 축약 검증 표의 흔들지 않은 매개변수 · 배제 영역 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 99호 행 · 99편 누적 · Evidence 아흔네 번째 · 새 제약 6 · Status Log · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](정의 표 새 줄 · 99호 절 · 처방 27 · 주장하지 않는 것) · [[spm-grouped-parameter-identifiability]](적용 표 99호 행 셋 · 한계) · [[data-window-identifiability]](99호 절 — 평탄 창 · 궤적 창 · 편향 ↔ 분산 · 관련 · `updated`) · [[constrained-crb-identifiability]](적용 — 단일 점 감도 · 편향 ↔ 분산 · `updated`) · [[assb-lampe-contact-product-degeneracy]](여든두 번째 적용 · 주장하지 않는 것) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: 새 개념 페이지("상태 관측성 ↔ 매개변수 식별성") 만들지 않음 — 위 여섯 페이지의 절 · 행으로 충분 · EKF 자체는 재구현하지 않음(Δt · 잡음 · 상태 배열 미인쇄 — 편향 사상은 준정적 대수) · [15] Tian & Qi · [11] Fabre 원문 미열람(D_n⁻ 2.1 · k_pos 관례의 출처 미확인) · 원 참고문헌(12 · 26 · 37 · 91 · 98호 인용분) 다시 열지 않음 — digest 전사 대조 · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행(✅ 99호 흡수 · 지목 칸 "12 · 37 | 2" 그대로) · 재지목 둘(Tian & Qi 2017 5 → 6 · Fabre 1 → 2) · 새 행(★★ Lin X. 2018 *IEEE TIE* [19] · ★★ Mohan · Kim · Stefanopoulou 2016 *IEEE TCST* [20] · ★★ Lin · Kim · Mohan · Siegel · Stefanopoulou 2019 *ARCRAS* [14] · ★ Di Domenico 2010 [7] · ★ Wang 2017 *IEEE CSM* [13] · ★ Nesro & Elfadel 2013 [12] · ★ Jang 2001 [16]) · §2 공백 1번 행 꼬리(99호 확인 — 식별성 편 아님) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 59 행.
- 후속(서지 기준, 미열람): **Tian H.-K., Qi Y. 2017 *J. Electrochem. Soc.* 164, E3512**([15] — 재지목 → 6 · 표 1 머리 출처) · **Fabre S. 외 *J. Electrochem. Soc.* 159, A104**([11] — 재지목 → 2 · 식 (22) 원전) · **Lin X. 2018 *IEEE Trans. Ind. Electron.* 65, 7138**([19] — 편향 ↔ 분산) · **Mohan S., Kim Y., Stefanopoulou A.G. 2016 *IEEE TCST* 24, 1643**([20]) · **Lin X., Kim Y., Mohan S., Siegel J.B., Stefanopoulou A.G. 2019 *Annu. Rev. Control Robot. Auton. Syst.* 2, 393**([14]) · Di Domenico 2010 *JDSMC* 132([7]) · Wang 2017 *IEEE CSM* 37(4)([13]) · Nesro & Elfadel 2013 ICECS([12]) · Jang 2001 *ESSL* 4, A74([16]) · 4차 묶음: [10] = 91호(흡수) · Deng 2021(파일 60 · 100호 예정 — 교차 · 인용 0).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 137).

## [2026-10-03] ingest | assb 100호 — Deng Z., Hu X., Lin X., Xu L., Li J., Guo W. 2021, A Reduced-Order Electrochemical Model for All-Solid-State Batteries (IEEE Trans. Transp. Electrif. 7(2), 464–473)
- raw: `raw/papers/deng2021_assb-reduced-order-model-pade-polynomial.md` (sha256 봉인 34d93cbf…1c79133f — `pdf_sha256` c811ace7…c6192cb3 · 3,180,760 B · 호출자 sha256 일치(직접 재계산) · SI 없음(보충 언급 0 — 직접 다시 셈 · 임베디드 파일 하나는 Distiller 작업 설정) · 원자료 · 코드 공개 0 · 자기 실험 0) · 그림 `raw/figures/deng2021_assb-reduced-order-model-pade-polynomial/` (자동 9 = `fig_1` … `fig_9`(SI 오판 0 — `SI_TAG` False 를 실행 뒤 확인 · `fig_S…` 0) + **수동 8**(표 I–V 단독 · 그림 2 · 3 단독 · 그림 4 전체 — 300 dpi) · **연 것 17/17** · 자동 크롭 문제(표 I–V 자동 0 — 표 캡션 미인식 · `fig_2` 위 표 II 조각 · `fig_3` 위 표 III 조각 + 본문 단 · `fig_4` 오른쪽 가지 잘림 · `fig_6` 캡션 '(c) c+' 에서 끊김 · `fig_7` 캡션 끝 'TABLE IV' · `fig_5` 아래첨자 순서) 는 `figures.json` note 17 에 · 그림 2–9 벡터 경로 판독(축 프레임 · 눈금 선 보정 · 범례 상자 걸러 냄) · 식 · 표는 쪽 렌더 조각(판독용 · 커밋 안 함)). `raw/figures/_sources.json` — 이 편 항목(17) 추가 · 다른 항목 변화 0.
- **4차 묶음 파일 60**(원장 §1 요청 14 편 중 열째 · 2026-10-02 사용자 공급) · 원장 행 "★★ … 26 · 37 | 2 | Q4" · 지목 26호 §11(:383 · ★★★ · [16]) · 37호 §14(:413 · [29] — 등급 칸 없는 후속 표 · 98 · 99호 셈과 같은 처리) = **2 = 원장 일치**(99호 :546 = 교차 참조 "(이 편 이후 편 · 인용 0)" · 75호 :777 = 원장 §2 행 전사 · 93 · 94 · 95 · 96 · 98 · 99호 = 관계 문장 — 지목 아님) · 원장 §2 구조적 공백 1번 후보의 마지막 ASSB 편 · Chongqing Univ. + Ontario Tech Univ. + SJTU · © 2020 IEEE(OA 0) · 10 쪽(인쇄 464–473) · 그림 9 · 표 5 · 식 (1)–(29) · 참고문헌 [1]–[31](빠진 번호 0) · 우리 digest 셋 인용([7] = 91호 · [9] = 99호 · [11] = 98호) · 4차 묶음 13 편 중 [7] · [9] · [11] · [26](파일 61) 넷 인용.
- ★★★★ **(c) Q4**: 전달함수 계수 = 묶음 다섯(`[재현·대수]` 1/(A·F·L_p) · L_p²/D_Lis · L_e/(4A·F·D_Li⁺) · L_e²/D · A·k_pos) · 양극 축척 대칭 (A, L_p, D_Lis, k_pos) → (λA, L_p/λ, D_Lis/λ², k_pos/λ) · `identif*` 1(Fabre 소개) · `observab*` · `estimab*` · `sensitiv*` · `uniqu*` · `confiden*` · `uncertain*` · `±` · `correlat*` · `Fisher` · `Gramian` · `covarian*` · `noise` 0 · 매개변수 추정 0 · 묶음 목록 0("lumped-parameter model" 이름만) · 'SOC · SOH < 4 %' = 액체 문헌 [14] · [31] 의 외삽(추정기 실행 0 · 같은 계열 99호 9 % · 5 % 무언급) → **Q4 0/100 아흔두 번째 성질** · 원장 §2 후보 Deng 2021 = 식별성 편 아님(75 · 92 · 99호 닫음 형식 — 후보 목록의 ASSB 편 넷 모두 닫힘).
- ★★★★ **(a) '2.6 mV'**: 표 IV UDDS V_t RMSE 2.60 · MaxAE 40.5 mV("which occurs at the end of discharge") · 10C RMSE 0.54 · MaxAE 4.60 · η_d 6.60 / 76.30 mV · 초록 "less than 2.6 mV" = RMSE(결론은 바르게 씀 — D1) · `[도표·벡터]` 그림 8 ROM − PDE 최대 V 36.7 mV @2,722 s · η_d 36.0 @2,713 s · UDDS = 축척 두 번(2,742 s · 지연 1,370 s · −3.88 … +8.65C · 평균 1.29C · 순 0.979 Q) · 비교 대상 = 같은 매개변수 한 벌의 PDE · ★ V 4.6 ↔ η_d 76.3 mV — V = Eeq(θ_s) + η(식 16) 라 η_d ↔ Eeq(θ̄) 상쇄(출력이 맞는다 ≠ 성분이 맞다) · `[재현]` r 무시 10C RMS 0.40 · 최대 0.75 mV(인쇄 k_r) → 14.85 · 23.94 mV(k_r ×100).
- ★★★★ **(a) Padé**: `[재현·대수]` 표 II(y = L_p · 0) · 표 III 1–3차 계수 = √u coth √u · √u / sinh √u · tanh z / z 의 Padé(y = 0 2차 분자 부호 오기 하나 — D9) · `[도표·벡터]` 그림 2 PDE = 정확 coth ±0.13 dB · ±0.06° · 표지 = 표 II ±0.75 dB · ±0.34° · 그림 3 'PDE' ≠ 식 (22)(10⁻³ rad/s −3.9 ↔ −7.0° · 0.1 rad/s 142.5 ↔ 137.1 dB · 632 rad/s 499 ↔ 99 dB · 위상 진동 ↔ −45° 수렴 — 원인 미확정 · D2) · 3차 유효 대역(1 dB · 5°) 양극 1.18 rad/s(0.19 Hz) · 전해질 0.354 rad/s(0.056 Hz) ↔ 인용 기준 2.5 Hz(그곳에서 3차 −6.1 dB · −40° / −11.2 dB · −43.5° — D4).
- ★★★★ **(a)(b) 인쇄 식 ↔ 계산**: ROM = 인쇄 식 다섯 자리를 고친 꼴로만 그림이 닫힘 — 식 (21) D_e ↔ 그림 3 · 5(c) D_amb = 2D_e(1차 −45° @8.19×10⁻³ rad/s → 1.535×10⁻¹⁵ · D3) · 식 (27) L_e² ↔ L_e(그림 5(d) RMS 2–38 mol m⁻³ · 인쇄 꼴 3.6×10⁹ — D5) · 식 (28) 'D_e' ↔ 비 (D_Li⁺ − D_n⁻)/(D_Li⁺ + D_n⁻)(그림 7(a) ±0.08 mV · 그대로면 13.7 mV — D6) · 식 (18)–(20) √D(D7) · 식 (6) 부호(D10) · ★ 원 PDE = 식 (9) 그대로 Nernst 항 포함(`[재현]` 표 I · SOC₀ 1.0 · T 298.15 K 재풀이 η_mt ±0.05 mV 1–330 s · 빼면 최대 19.3 mV · V ±1.4 mV · 3.35 V 339.61 ↔ 339.01 s) — 99호 그림의 '전체 모형'(둘째 항만)과 다른 구현.
- ★★★ **(b) 그림 9 · 99호 상속**: "The experimental data come from [7], and the same model parameters in the reference are also used in this article." · `[재현·외부 값]` 표 I + 식 (14) 면 t = 1 s +74 … +92 mV ↔ [7] 외삽 EMF(91호 전사 11 점) 면 −2.0 … +2.6 mV · 대부분 ±7 mV → 그림 9 는 [7] EMF 로 계산된 것으로 읽힘(인쇄 0 · D11) · 실험 첫 표지 = 91호 측정 Q = 0 전압 ✅ · 실험 끝 546.4 · 266.6 · 124.2 s = 91호 측정 용량의 ×0.985 · 0.972 · 0.924(D12) · PDE 끝 ≈ Danilov 모형선 · 표 I: D_n⁻ 5.1 고침 · c_max 2.33×10⁴ · c_min 1.165×10⁴ 인쇄(1C 9.99 µA) · k_pos ×100 · 인쇄 k_r · Fabre 곡선 · α 0.5 · T 미인쇄 · k_neg · α_neg 새 값(머리 "[9], [27]" — [9] 에 음극 동역학 0) · "The results of [9] suggest …" = 99호 결론을 조건(인쇄 k_r) 없이.
- ★★★ **(d) 37호 물음**: θ · ε_p 둘 다 0 · 면적 A 한 값이 용량 극 · 수송 이득 · i₀ 에 · 양극 묶음의 면적 ↔ 두께 축척 대칭 — 37호 A_eff(BV 만)는 이 꼴 위의 뒤 추가 · 원장 R1 위반 표본 하나 더.
- **채움표 100호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(층 하나 — 면적 A 한 값 · 면적 ↔ 두께 축척 대칭 · `θ(N)` 0/100) · Q2 없다(전압 하나 · 인용 곡선 셋 · V 는 θ_s 만 본다) · Q3 층 하나(PDE = 인쇄 식 그대로 · ROM = 고친 꼴 · 표 I = 99호 계보 · 그림 9 = [7] 측정 + EMF) · Q4 0/100 **아흔두 번째 성질** · Q5 해당 없음(Li 금속 · η_ct,neg 0.05–0.06 mV) · Q6 해당 없음 · Q7 해당 없음 + 공백 하나 채움(c_max · c_min 인쇄) · Q8 층 둘(Fabre 유리함수 + [7] EMF).
- **곱 축퇴 처방 여든세 번째 적용**: 입력 점검 전부 ❌ / ⚠(모의 · 인용만) · 곱 문장 셋(A 가 A·k_pos 와 용량 극 · 수송 이득에 같은 값 · 양극 축척 대칭 · 37호 A_eff 는 이 꼴 위의 BV 추가) · 후보 메모 하나(축약 모형에서 A 가 들어가는 이득 · 축척 방향 · 붙인 자리 표기) · 새 줄 0.
- ⚠ 어긋남 18 건(D1 초록 '2.6 mV' 지표 탈락 · D2 그림 3 PDE 곡선 · D3 식 (21) D_e ×2 · D4 2.5 Hz 기준 ↔ 3차 대역 · D5 식 (27) L_e² · D6 식 (28) 'D_e' 두 뜻 · D7 식 (18)–(20) √D · D8 식 (19) 지수 · D9 표 II y = 0 부호 · D10 식 (6) 부호 · D11 그림 9 평형 곡선 교체 · D12 그림 9 실험 끝 · D13 '< 4 %' · D14 '0.2 ms'(10C 0.206) · D15 'SOC 0 %'(0.057 · 0.021) · D16 그림 1 'reprinted' ↔ 'modified' · D17 좌표 · 기호 · D18 [10] 연도 · 자금 기관명).
- PDF 메타데이터: `PDF 1.4` · 10 쪽 612 × 792 · 암호 0 · creator "Aspose Ltd." · producer "Aspose.Pdf for .NET 8.3.0; modified using iText® 7.1.1 ©2000-2018 iText Group NV (AGPL-version)" · author ""(빈 값) · subject "IEEE Transactions on Transportation Electrification;2021;7;2;10.1109/TTE.2020.3026962" · 생성 D:20210428172906+05'30' · 수정 D:20210510043430-04'00'(호출자 메모와 같음 · = 'date of current version') · XMP 3,386 B(prism 7 · 2 · 464–473 · "June 2021" · dc:creator 없음) · PageLabels 1 부터 · EmbeddedFiles 1("01-Web-res setting-web-IEEE.joboptions" — Distiller 작업 설정 · 보충 아님 · pymupdf embfile_count 0) · 래스터 = 1-bit 조각 · 마스크(그림 5 · 6 PDE 선) + 저자 사진 여섯 · 합자 84(NFKC 로 복원) · `%%EOF` 1.
- 보류 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(햐) · (겨)–(져): **(세)(셔)(여)(져)(치)(탸)(햐)(제)(체)(며)** 근거(강) · (냐)(벼)(겨)(대)(뎌)(이)(에)(뱌)(먀)(갸) 근거(중) · (무)(녀)(루)(차)(다)(쟈)(가)(리)(헤)(페) 약 · (마) 출처 추가만(결정 · 반영됨) · (라)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷(축약 · 근사 모형 오차 주장의 지표 · 위치 · 조건 표기 · 차수 · 대역 선택 근거 그림의 기준 곡선 검사 + 인용 대역 기준 ↔ 실행 표본 주기 · '실험 검증' 그림의 자료 경로 표기 · (선택) 출력에 안 보이는 성분의 표기 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 100호 행 · 100편 누적 · Evidence 아흔다섯 번째 · 새 제약 6 · Status Log · 주장하지 않는 것) · [[assb-sensitivity-sweep-vs-identifiability]](100호 절 · 처방 28 · 주장하지 않는 것) · [[spm-grouped-parameter-identifiability]](적용 표 100호 행 셋 · 한계) · [[assb-lampe-contact-product-degeneracy]](여든세 번째 적용 · 주장하지 않는 것) · [[assb-synthetic-truth-contact-loss-requirements]](R1 출처 · 상태 · 주장하지 않는 것) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: 새 개념 페이지("축약 모형의 묶음 · 출력 ↔ 성분 오차") 만들지 않음 — 위 다섯 페이지의 절 · 행으로 충분 · [[data-window-identifiability]] · [[constrained-crb-identifiability]] 변경 안 함(창 · FIM 계산 없음) · 저자 코드 · 이산화 재구현 안 함(우리 ROM 재현 = 연속 시간 계단 응답 · 이산화 미인쇄) · [27] Tian & Qi · [10] Fabre · [19] Marcicki 원문 미열람 · 원 참고문헌(26 · 37 · 91 · 98 · 99호 인용분) 다시 열지 않음 — digest 전사 대조 · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행(✅ 100호 흡수 · 지목 칸 "26 · 37 | 2" 그대로) · 재지목 넷(Tian & Qi 2017 6 → 7 · Kazemi 2019 1 → 2 · Fabre 2 → 3 · Danilov & Notten 2008 3 → 4(파일 61)) · 새 행(★★ Marcicki 2013 *JPS* 237, 310 [19](95 · 100 — 95호 ☆ 에서 올림) · ★★ Deng Z. 2017 *Energy* 138, 509 [23] · ★ Hu · Xu · Lin · Pecht 2020 *Joule* 4, 310 [13](12 · 100 — 지목 누락 보충) · ★ Hu X. 2018 *IEEE TVT* 67, 10319 [14] · ★ Han X. 2015 *JPS* 278, 802 · 814 [18 · 31] · ★ Forman *JES* 158, A93 [22] · ★ Smith 2007 · 2008 [20 · 21](2007 = 96 · 100 — 96호 ☆ [59] 에서 올림 · digest 후속 표의 '100 = 1(새)' 는 96호 ☆ 를 빠뜨린 셈 — raw 불변이라 여기서 정정) · ★ Deng Z. 2018 *Energy* 142, 838 [24] · ★ Lee · Chemistruck · Plett 2012 *JPS* 206, 367 [25] · ★ Yuan 2017 *JPS* 352, 245 [28]) · 지목 누락 기록(Hu · Xu · Lin · Pecht 2020 — 12호 ★ · 이 편이 재지목하며 보충) · §2 공백 1번 행 꼬리(100호 확인 — 식별성 편 아님 · 후보 목록의 ASSB 편 모두 닫힘) · §3-b 표시 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 60 행.
- 후속(서지 기준, 미열람): **Tian H.-K., Qi Y. 2017 *J. Electrochem. Soc.* 164, E3512**([27] — 재지목 → 7 · 표 I 머리 출처) · **Kazemi N. 외 2019 *Solid State Ionics* 334, 111**([8] — 재지목 → 2) · **Fabre S.D. 외 *J. Electrochem. Soc.* 159, A104**([10] — 재지목 → 3 · 식 (14) 원전) · **Marcicki J. 외 2013 *J. Power Sources* 237, 310**([19] — 2.5 Hz 기준 · 축약 모형 매개변수화 분석) · **Deng Z. 외 2017 *Energy* 138, 509**([23] — 축약 모형 + 다중 매개변수 식별) · Hu · Xu · Lin · Pecht 2020 *Joule* 4, 310([13] — 지목 누락 보충) · Hu 2018 *IEEE TVT*([14]) · Han 2015 Part I · II([18] · [31]) · Forman *JES* 158, A93([22]) · Smith 2007 · 2008([20] · [21] — 2007 재지목 → 2) · Deng 2018 *Energy* 142([24]) · Lee 2012([25]) · Yuan 2017([28]) · 4차 묶음: [7] = 91호 · [9] = 99호 · [11] = 98호(흡수 — 교차) · [26] Danilov & Notten 2008(파일 61 · 101호 예정 — 재지목 → 4).
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 138).

## [2026-10-03] ingest | assb 101호 — Danilov D., Notten P.H.L. 2008, Mathematical modelling of ionic transport in the electrolyte of Li-ion batteries (Electrochim. Acta 53, 5569–5578)
- raw: `raw/papers/danilov2008_liquid-electrolyte-transport-electroneutrality-dissociation.md` (sha256 봉인 6eed292b…c64e2a7f — `pdf_sha256` f427e873…8edf14a5 · 1,996,390 B · 호출자 sha256 일치(직접 재계산) · SI 없음(보충 언급 0 — 직접 다시 셈 · 임베디드 파일 0) · 원자료 · 코드 공개 0 · 자기 측정 그림 하나(그림 9 — 다른 셀)) · 그림 `raw/figures/danilov2008_liquid-electrolyte-transport-electroneutrality-dissociation/` (자동 13 = `fig_1` … `fig_12` · `tab_1`(SI 오판 0 — `SI_TAG` False 를 실행 뒤 확인 · `fig_S…` 0) + **수동 1**(표 1 단독 — 300 dpi) · **연 것 14/14** · 자동 크롭 문제(`fig_1` 위 식 (4.1) 붙음 · `tab_1` 쪽 전체 과대 · `fig_3` 캡션 필드에 본문 섞임 · 900 자 잘림 · `fig_7` 캡션 55 자 잘림 · `fig_8` 'η_down' · `fig_12` '(δ)' 글리프 깨짐) 는 `figures.json` note 14 에 · 그림 전부 ≈200 dpi JPEG — 8 · 9 · 11 · 12 는 PDF 에서 원본 래스터를 꺼내 축 눈금 화소로 판독 · 2–7 · 10 은 3D 면(`[도표]` 만) · 식은 쪽 렌더 조각(판독용 · 커밋 안 함)). `raw/figures/_sources.json` — 이 편 항목(14) 추가 · 다른 항목 변화 0.
- **4차 묶음 파일 61**(원장 §1 요청 14 편 중 열한째 · 2026-10-02 사용자 공급) · ⚠ **ASSB 아님 — 액체(유기) 전해질 LiPF₆ 수송 모형 원전**(95 · 96호 규칙 — 도구가 아니라 원전) · 원장 행 "★ … 26 \| 1 \| 모델 \| 해리 전해질 수송(이온+공공) 원전 — 'SE 에 농도 구배' 가정의 출처" · 지목 26호 §11(:382 · ★★ · [20]) · 91호 후속(:606 · ★★★ · [27]) · 98호 후속(:695 · '도착' · [28]) · 100호 후속(:580 · '도착' · [26]) = **4 = 원장(L289) 일치**(99호 :419 · 92–97호 = 관계 문장 · 26 · 91 · 98 · 100호 본문 · 참고문헌 표 = 지목 아님) · Eurandom + TU/e + Philips Research · © 2008 Elsevier(OA 0) · 10 쪽(인쇄 5569–5578) · 그림 12 · 표 1 · 식 (1)–(47) · 참고문헌 [1]–[18](빠진 번호 0) · 우리 digest 인용 0 · 4차 묶음 13 편 인용 0.
- ★★★★ **(b) 'SE 에 농도 구배 · 이온 + 공공'**: 지면 0(`solid` · `vacanc*` · `glass` · `single-ion` 0 회 · 운반체 Li⁺ · PF₆⁻ · 해리 = 중성 LiPF₆ 이온쌍 · 중성종은 확산(식 46)) — 이 편은 식 꼴의 원전(✅)이지 고체 물리의 원전(❌)이 아니다 · 이식 = 91호(n⁻ = nBO 미보상 전하 · 고정 Li⁰) → 98호(공공 · 국소 닫음 c₀ = c_Li⁰ + c_n) → 26호(98호 이름 차용) · `[재현·가정]` 이 편 표 1 + δ 0.8 · 50 min 에서 닫음만 바꾸면 농도 항 74.0 → 7.4 mV · 합 160.1 → 53.6 mV · 이원 가정 몫 72 → 17 %(액체 반사실) · 중성종 고정이면 50 min 한계 δ 0.60 → 0.90 · 단일 이온 극한: 식 (37) η_ss 는 D₋ 무관 — D₋ → 0 이어도 정상 농도 구배 그대로(정상 도달 시간만 ∞) → 'SE 에 농도 구배' 는 이원 + 차단 틀을 고르는 순간 구성상 정해진다(`[해석]`).
- ★★★★ **중심 표**: 지목 넷이 가져간 열일곱 줄 — ✅ 11(26호 식 22 · 23b · 25 · 26 꼴 · 91호 식 18 · 19 · 20 · 차단 경계 · 평형 관계 · 98호 식 23–24 · 100호 식 9 · 10) · 부분 2(91호 Li⁰ 고정 · 98호 식 31 이온–전자 쌍) · ❌ 4(26호 공공 · SE 농도 구배 근거 · 91호 n⁻ 정체 · 91호 k_r 대조처 · 98호 국소 닫음).
- ★★★★ **Nernst 항(99 · 100호 의문)**: 원전 정의 식 (27) η = Li⁺ 전기화학 퍼텐셜 차 = (RT/F) ln[c(L)/c(0)] + φ 차 · 그림 8 은 두 항(b 'diffusion' · c 'migration')을 따로 계산 — `[재현]` 표 1 PDE 재풀이 0.3–50 min ±1 mV(이동 ±0.3) → 100호 원 PDE(포함) = 원전 정의 · 99호 그림(둘째 항만) = φ 차 · 정상에서 두 항 같음(식 36 — 둘째 항만이면 정확히 절반 · 99호 '≈절반' 과 같은 자리) · 이 편 본문의 `Nernst` 3 회는 전부 'Nernst–Planck'(첫 항의 이름은 'diffusion overpotential').
- ★★★★ **성분 이름 두 벌**: 정의 분할 1 : 1(식 36) ↔ 측정 분할 2t₊ : 2(1−t₊)(식 41 — 끊는 순간 낙차) · `[재현]` 표 1 정상 137.26 = 68.63 + 68.63 ↔ 낙차 54.90 · 남는 82.35 mV(그림 8 (d) `[도표·화소]` 82.0 ✅) — 'migration overpotential' 은 전류 차단으로 재는 양이 아니다 · 이원 가정 몫의 원형: 식 (32) η₀ = 같은 σ 단일 이온 옴 강하 · 식 (38) 정상 몫 ≥ 1 − t₊(표 1 73.9 %).
- ★★★★ **표 1 ↔ 계산 두 상태**: 표 1 x 0.8706 ↔ 인쇄 x 0.9017(= L 2.900×10⁻⁴ 넷째 자리) · 표 1 로 닫힘 = 그림 8(±1 mV) · 11(A)(RMS 0.96) · 그림 3 바닥(−1235 V/m) · 그림 4 비(1.92) / L 2.9×10⁻⁴ 로만 닫힘 = x 0.9017 · '61 %' · 그림 11(B)(C)(RMS 1.06 · 0.83 ↔ 표 1 15.5 · 34.3 mV) · 그림 12(δ 0.70–0.997 ±3 mV — δ→1 끝 152 ↔ 그림 8 137 mV) · 한계 δ(재풀이 0.6576 ↔ 인쇄 0.6569 · 표 1 이면 0.6037) / 어느 쪽도 아님 = R_ss 0.1950 Ω(0.1906 · 0.2114) · x 묶음 가르기: 같은 x 의 한 매개변수 변경 넷 중 그림 11(C) 시간 경과는 L 만 RMS 0.83 mV(I/A 5.49 · c₀ 6.92 · D₊ 5.86) · `[재현·대수]` 완전 해리 출력은 I/(A·c₀) 로만 — 면적 ↔ 염 농도 정확 대칭.
- ★★★ **그림 9 '실험 검증'**: in-house Lithylene 300 mAh 셀 하나 · 0.4C ≈30 min · 기준극 쌍([13]) · `[도표·화소]` 선 정상 9.95 ± 0.1 mV · 끈 직후 ≈5.0–5.2 mV · 표지가 선에 겹침 · 잔차 0 · `[재현]` 표 1 Lithylene 행 전 두께면 정상 32.96 mV(×3.3) · `[재현·가정]` 가운데 29.6 µm 구간이면 상승 ±0.15 · 감쇠 ±0.4 mV 로 닫힘(위치 미인쇄) · 선 낙차/정상 ≈0.48–0.50 ≈ t₊ 0.5 — 식 (42) 처방을 자기 측정에 적용 0 · CGR17500 실험 0("R0 … in the good agreement with experimental results" 값 · 출처 0).
- ★★★ **해리 확장**: 한계 δ 는 중성 이온쌍 확산에 매달림(`[재현]` 고정이면 0.6576 → 0.923) · 식 (42) 해리 판 δ 0.8 에서 0.445 ↔ t₊ 0.4(L 2.9×10⁻⁴ 0.441) · 결론은 조건 없이 "simple experiments to determining the transference numbers".
- **채움표 101호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(층 하나 — 면적 ↔ 염 농도 정확 대칭 · 정상 x 묶음 · `θ(N)` 0/101) · Q2 없다(ASSB 관측 0 · 액체 기준극 쌍 측정 하나 · 성분 이름 두 벌) · Q3 층 하나(모형 원전 · [11] 책 값 · 두 매개변수 상태 · Nernst 항 포함 계산 · 실험 = 다른 셀 그림 하나) · **Q4 해당 없음 — ASSB 0/101 · 아흔세 번째 성질** · Q5 해당 없음(액체 · η = Li⁺ 전기화학 퍼텐셜 차 정의) · Q6 · Q7 · Q8 해당 없음.
- **곱 축퇴 처방 여든네 번째 적용**: 입력 점검 ❌ 다섯 · 4단계 ✅(모의 — 시간 척도 L²/D 가 x 묶음 안 L 을 가름) · 곱 문장 셋(완전 해리 출력 = I/(A·c₀) — 면적 ↔ 염 농도 정확 대칭 · 시간 경과로 L 분리 · 켬 · 끔 순간값은 다른 묶음) · 후보 메모 하나(정상 묶음이 같은 가설을 과도로 가르는 시험 — 정확 대칭은 시간으로도 안 깨짐) · 새 줄 0.
- ⚠ 어긋남 17 건(D1 표 1 ↔ x 0.9017 상태 · '61 % … agrees well with … Fig. 8' · D2 R_ss 0.1950 · D3 '완전 해리' 두 값 137 ↔ 152 mV · D4 식 (4.3)–(4.4) ↔ (6.3)–(6.4) 경계 부호 · D5 그림 11 본문 (ii) · (iv) 곡선 글자 · D6 그림 12 (d) 정의 0 · D7 그림 9 ↔ 표 1 Lithylene · D8 'Section 4' · D9 식 (24) · (25) 이름 · D10 PF₆⁻ 전도 문장 둘 · D11 '1/δ reduction' · D12 그림 4 캡션 · 'Fig. 3b' · 'y = 1' · D13 y 눈금 0.4 중복 · D14 전기중성 문장 · D15 R₀ 실험값 0 · D16 'early 1980s [1]'(1993 — 91호 같은 문장) · 오자 · D17 결론 t₊ 문장).
- PDF 메타데이터: `PDF 1.7` · 10 쪽 595.30 × 793.79 pt · 암호 0 · title "doi:10.1016/j.electacta.2008.02.086" · author · subject · keywords ""(빈 값) · creator "Elsevier" · producer "Acrobat Distiller 7.0 (Windows)" · 생성 D:20080429182246Z · 수정 D:20080429190135+05'30'(호출자 메모와 같음 ✅) · XMP 3,531 B(CreatorTool Elsevier · dc:title = doi · dc:creator 빈 항목 · DocumentID uuid:a31d2c3c-… · prism · CrossMark 0) · 트레일러 ID [5E8D790A… · 6F33CD8F…] · PageLabels 5569 부터(= 인쇄 쪽) · /Names → /Dests 만(EmbeddedFiles 0) · `%%EOF` 1 · 래스터 14(로고 · 표지 둘 + 그림 1–12 ≈200 dpi JPEG) · p. 5575 그리기 354 개는 쪽 상자 밖 · 합자 116(NFKC 로 복원) · η(U+0005 34 회) · μ · 괄호 · 적분 기호가 제어 문자 · δ → 'ı'(21 회).
- 보류 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(햐) · (겨)–(펴): **(먀)(냐)(치)(세)(여)(셔)(탸)** 근거(강) · (펴)(쟈)(뱌)(녀)(햐)(텨)(며)(뎌) 근거(중) · (대)(다)(에)(이)(헤)(갸)(쳐) 약 · (마) 근거 0(개념 목록 밖 메모만 — 결정 · 반영됨) · (라)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷(이식된 수송 식의 원전 계 · 닫음 표기 · 과전압 성분 이름의 정의 분할 ↔ 측정 분할 표기 · 한 지면 그림들의 매개변수 상태 일관성 검사 · (선택) 닫힌 꼴 '측정 비 → 매개변수' 처방의 조건 표기 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 101호 행 · 101편 누적 · Evidence 아흔여섯 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](여든네 번째 적용 · 주장하지 않는 것) · [[spm-grouped-parameter-identifiability]](적용 표 101호 행 둘 · 한계) · [[assb-sensitivity-sweep-vs-identifiability]](101호 절 · 처방 29 · 주장하지 않는 것) · [[assb-synthetic-truth-contact-loss-requirements]](목록 밖 메모 — SE 전해질 수송 모형 · 닫음 · 주장하지 않는 것) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: 새 개념 페이지("이식된 수송 식 · 성분 이름 분할") 만들지 않음 — 위 다섯 페이지의 절 · 행으로 충분 · 합성 truth 요구(R9)로 올리지 않음(새 판단 거리) · [[data-window-identifiability]] · [[constrained-crb-identifiability]] 변경 안 함(창 · FIM 계산 없음) · 저자 코드 미공개라 pdepe 재구현 대신 유한체적 재풀이 · 91 · 98호 SE 몫(≈71 · ≈8 %)을 이 편 식으로 다시 풀지 않음(그 digest 들의 계산) · [11] Bergveld 책 · [13] Zhou 2006 · [17] · [18] 원문 미열람 · 원 참고문헌(26 · 91 · 98 · 99 · 100호 인용분) 다시 열지 않음 — digest 전사 대조 · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행 L289(✅ 101호 흡수 · 지목 칸 "26 · 91 · 98 · 100 \| 4" 그대로) · 재지목 하나(Bergveld · Kruijt · Notten 2002 *BMS* 책 L315 95 → 95 · 101 = 2) · 새 행 하나(★ Zhou · Danilov · Notten 2006 *Chem. Eur. J.* 12, 7125 [13] — ⚠ 액체셀) · 지목 누락 0 · §3-b 표시 · §4 갱신 기록 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 61 행.
- 후속(서지 기준, 미열람): **Zhou J., Danilov D., Notten P.H.L. 2006 *Chem. Eur. J.* 12, 7125**([13] — ⚠ 액체셀 · 기준극 쌍 실측 원전 · 그림 9 기준극 위치 · 그림 8 성분 일치 '[13]' 근거) · **Bergveld H.J., Kruijt W.S., Notten P.H.L. 2002 *Battery Management Systems, Design by Modelling***([11] — 재지목 → 2 · 표 1 출처 · L · D 층위) · ☆ [1]–[10] · [12] · [14]–[18].
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 139).

## [2026-10-03] ingest | assb 102호 — Xie J., Imanishi N., Matsumura T., Hirano A., Takeda Y., Yamamoto O. 2008, Orientation dependence of Li–ion diffusion kinetics in LiCoO2 thin films prepared by RF magnetron sputtering (Solid State Ionics 179, 362–370)
- raw: `raw/papers/xie2008_lco-thin-film-orientation-diffusion-gitt-pitt-eis.md` (sha256 봉인 38f28451…ea513655 — `pdf_sha256` 28db7113…57c5b7c8 · 1,225,469 B · 호출자 sha256 일치(직접 재계산) · SI 없음(보충 언급 0 — 직접 다시 셈 · 임베디드 파일 0) · 원자료 · 코드 공개 0 · 데이터 ZIP 0(`[데이터]` 표시 0)) · 그림 `raw/figures/xie2008_lco-thin-film-orientation-diffusion-gitt-pitt-eis/` (자동 16 = `fig_1` · `fig_2` · `fig_4` … `fig_13` · `fig_15` · `fig_16` · `tab_1` · `tab_2`(SI 오판 0 — `SI_TAG` False 를 실행 뒤 확인 · `fig_S…` 0) + **수동 5**(그림 3 · 그림 14 · 그림 16 · 표 1 · 표 2 단독 — 300 dpi) · **연 것 21/21** · 자동 크롭 문제(**그림 3 누락** — 캡션 블록이 식 (2) 꼬리 '; t≪L²/D̃ (2)' 와 한 블록 · **그림 14 누락** — 아래 두 단 캡션이 한 블록이라 `fig_16` 에 합쳐짐 · `fig_16` 두 그림 과대 · `tab_1` · `tab_2` 쪽 전체 과대 · 캡션 필드 오염 셋(193 · 676 · 455 자)) 는 `figures.json` note 21 에 · 캡션 위치는 맞음(뒤바뀜 아님) · 그림 전부 ≈200 dpi JPEG — 3–16 은 PDF 에서 원본 래스터를 꺼내 축 눈금 화소로 판독 · 식은 쪽 렌더 조각(판독용 · 커밋 안 함)). `raw/figures/_sources.json` — 이 편 항목(21) 추가 · 다른 항목 변화 0.
- **4차 묶음 파일 62**(원장 §1 요청 14 편 중 열두째 · 2026-10-02 사용자 공급) · ⚠ **ASSB 아님 — 액체 전해질(1 M LiClO₄ EC/DEC) 3전극 비커셀의 스퍼터 LiCoO₂ 박막 확산계수 측정 편**(95 · 96 · 101호 규칙 — 도구 · 원전이 아니라 측정 편) · 원장 행 "★ … 26 \| 1 \| Q3 \| LCO 박막 확산계수를 GITT·EIS 로 **측정** — 적합된 `D_M⊕` 의 독립 대조" · 지목 26호 §11(:386 · ★★ · [23]) · 98호 후속(:696 · '도착' · [31] 재지목) = **2 = 원장(L291) 일치**(91호 :611 = 다른 편 Xie 외 2007 *SSI* 178, 1218 — 셈 밖 · 101호 :463 · 99호 :419 · 92–97호 = 관계 문장 · 98호 :543 = 참고문헌 표) · Mie University · © 2008 Elsevier(OA 0) · 9 쪽(인쇄 362–370) · 그림 16 · 표 2 · 식 (1)–(9) · 참고문헌 [1]–[21](빠진 번호 0) · 우리 digest 인용 0 · 4차 묶음 13 편 인용 0.
- ★★★★ **(a) 셀**: D̃ 는 고체 박막 전지가 아니라 **액체 셀**(1 M LiClO₄ EC/DEC · Li 박 상대 · 기준 · Au 900 nm / Al₂O₃ 8×8 mm 위 막 · 막 전면이 전해질)에서 · 고체는 σ 대조의 PEO–LiTFSI(정제 Li0.65CoO₂ · LiCoO₂ · 50–80 °C)뿐 · `LiPON` 0 · 두께 0.31 · 0.77 · 1.35 µm 는 이론 밀도 5.06 환산(질량 미인쇄) · SEM(Al₂O₃ 직접 막) ≈0.85 µm `[도표·화소]` ≈0.88 · 91 % · 배향은 두께가 정함(Bates [10]) — 두께 · 배향 · 막 구조가 한 손잡이.
- ★★★★ **(b) 방법 의존**: 표 1 한 물질 **6.4×10⁻¹⁴–6.0×10⁻⁹ cm² s⁻¹(4.97 dex)** · EIS/GITT ×20–225 · EIS/PITT ×4–1000('almost two orders') · (104)/(003) ×12–212('almost one order') · GITT/PITT ×0.03–11.9 · `[재현]` 네 닫힌 꼴이 미인쇄 S 0.64 cm² · Vm 19.34 · C 1/Vm · 298 K · 그림 5 삽도 dE/dδ 로 저자 그림을 다시 냄(CV 7.81 ↔ 7.7×10⁻¹² · GITT 0.07 · EIS 0.03(Z′ 기울기 — −Z″ 면 ×0.33) · PITT 0.05 dex(100–500 s 창 — 1500–2000 s 면 ×0.37)).
- ★★★★ **같은 막 · 같은 전위의 시간 상수**: `[재현·가정]` #120 · 4.08 V EIS 무릎(≈0.05 Hz) · 저주파 용량 0.70 F(≈막 삽입 용량 0.51 F) → 전 막 τ ≈8–30 s ↔ GITT · PITT L²/D ≈1400–3400 s(무릎 1–3×10⁻⁴ Hz — 창 밖) · GITT 100 s 평형 몫 2.3–3.4 mV ↔ 관측 10 mV — 앞인자가 아니라 시간 상수 차(반사 경계 · L = 두께 가정).
- ★★★★ **σ 대조('PITT 가 가장 믿을 만하다')**: `[재현]` ϕ = (F/RT)·δ·dE/dδ(그림 13(a) 비 0.7–1.3 — Li 기준이면 δ<0.35 에서 2–25 배) × C 상수(그림 14 − 13(b) 5.301 ± 0.005 dex · 49 쌍) → σ = 일관 Nernst–Einstein × 1/δ(Li0.65 ×2.86 · δ 0.031 ×≈32) · 고치면 Li0.65 에서 PITT (104) · (003/104) · GITT (104) 셋이 DC 와 ×0.6–1.2 · Li1.0 은 둘 다 안 맞음 · "dE/dδ is not involved … PITT" ↔ 식 (6)–(8) 모순 · `[재현·가정]` DC 정제 σ(60 °C 5.05×10⁻⁶ ✅ 그림 16)로 환산한 전자 차단 이완 ≈14–18 일 ↔ 관측 63 % ≈30 s · V–I 절편 0.25 V · 네 점 Arrhenius(Ea 81.8 · 구간 65 → 91 kJ mol⁻¹ 굽음) → RT 미인쇄(1.1×10⁻⁷ = 선형 22.3 °C).
- ★★★★ **(c) 계보 대조**: 98호 D_Li⊕(x 0.5–0.6) 7.9×10⁻¹⁴ m² s⁻¹ = **7.9×10⁻¹⁰ cm² s⁻¹**(98호 :129) ↔ EIS (003/104) ×1.4–2.9 · EIS (104) ×0.13–0.16 · GITT/PITT **×25–146** · 98호 D(x 1.0) 3.0×10⁻¹¹ ↔ δ 0.03–0.07 GITT ×2.0–2.3 · PITT ×16–23 · 26호 '문헌' D⁰_M⊕ 1.21×10⁻⁹ cm² s⁻¹(26호 :181 = 98호 :290 적합)는 척도 상수(β ≤0.65)라 대조 대상 아님 · 91 · 99 · 100호 D_Li 1.76×10⁻¹¹(91호 :239 · 320 nm) ↔ (003) GITT ×9–275 · PITT ×55–117 · (104) 띠 안 ⇒ **'범위 안' · '독립 대조' 불성립**(방법 칸이 결과를 정함 · 셀 다름 · 측정 D̃ ↔ 모형 D_Li⊕ 다른 양 — 98호 D_p ×1.61) · 98호 [31] 쓰임(국소 환경 의존)은 조성 의존 ✅ · 조건(액체 · 방법 · 배향 · 2상 '신뢰 불가') 빠짐.
- ★★★ **표 1 PITT ↔ 그림 9 · 12**(Li0.7 #60 ×5.4 · #120 ×3.4 · Li0.8 #120 ×23 — 그림 최대보다 큼 · GITT · EIS 열은 닫힘) · **CV**(그림 4(b) 0.6–4 mV s⁻¹ — 캡션 'over 1' ✗ · 봉우리 3.93 → 4.21 V 이동 · 2상 + 직렬 R 301–348 Ω 로도 닫힘 · 식 (1) T^{+½}) · **PITT 대표 과도 = 2상 평탄 시작**(3.92 V dδ/dE 9.2 V⁻¹ · 2000 s 에 차단 기준 86 배) · **조성 축 = #120 E(δ) 지도**(세 시료 δ 좌표 동일 · #30 펄스 Δδ 0.058 ↔ 점 간격 0.005–0.012 · 쿨롱 δ ×1.11) · **배향 기하**(PITT 비 중 ×19 = (1.35/0.31)² · 원시 τ 비 ×2.4–4.7 · (104) 의 Li 층은 ≈55° 기욺 `[해석·결정학]`).
- **채움표 102호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(`θ(N)` 0/102 · 층 하나: D̃·(S/Vm)² ↔ D̃/L²) · Q2 없다(ASSB 관측 0 · 정제 σ 대조 하나 · 자기 일관성 ✗) · Q3 층 하나(측정 D̃ = 원시 관측 × 미인쇄 가정 · 방법 라벨) · **Q4 해당 없음 — ASSB 0/102 · 아흔네 번째 성질** · Q5 해당 없음(Li 박 기준) · Q6 · Q7 해당 없음 · Q8 층 하나(GITT 이완 OCV · δ 닻 4.15 V · 세 막 공용).
- **곱 축퇴 처방 여든다섯 번째 적용**: 입력 점검 ❌ 셋 · ⚠ 셋 · 4단계 ✅(관측 — 같은 막 시간 상수가 방법끼리 ×≈50–430 안 맞음) · 곱 문장 셋(GITT · EIS · CV = D̃·(S/Vm)² · PITT = D̃/L² · 시간 영역이 방법 라벨을 드러냄 · σ 환산의 종 곱 1/δ) · 후보 메모 하나(같은 막 두 측정의 시간 상수 폐합 검사) · 새 줄 0.
- ⚠ 어긋남 15 건(D1 표 1 PITT ↔ 그림 9 · 12 · D2 'dE/dδ not involved … PITT' · D3 식 (7) 부호 · δ 기준 · D4 표 2 Li1.0 ↔ 그림 14 · D5 '한 자릿수 · 두 자릿수 · 같은 자릿수' · D6 그림 4 캡션 · D7 식 (1) T^{+½} · 식 (4) 부호 · D8 CV 값 Li0.5 행 · D9 대표 PITT = 2상 · D10 Li0.8 행 2상 · D11 그림 10 캡션 · D12 그림 5 삽도 라벨 · D13 (104) 'parallel' · D14 두께 ↔ SEM 다른 막 · D15 오자 — 'Yashuo' · 'diethylene carbonate' · 'Li065CoO2' · [20] 'Geder').
- PDF 메타데이터: `PDF 1.7` · 9 쪽 595.28 × 793.70 pt · 암호 0 · title "doi:10.1016/j.ssi.2008.02.051" · author · subject · keywords ""(빈 값) · creator "Elsevier" · producer "Acrobat Distiller 7.0.5 (Windows)" · 생성 D:20080412032645+08'00' · 수정 D:20080412040940+08'00'(호출자 메모와 같음 ✅) · XMP 3,392 B(CreateDate = ModifyDate 2008-04-12T03:26:45+08:00 — 정보 사전 수정 시각과 다름 · DocumentID uuid:7c65f99f-… · CrossMark · prism 0) · 트레일러 ID [DD5C1AD9… 같은 값 둘] · PageLabels 362 부터(= 인쇄 쪽) · `/FICL:Enfocus` · EmbeddedFiles 0 · `%%EOF` 1 · 래스터 18(로고 둘 + 그림 1–16 ≈200 dpi JPEG · 그림 2 만 RGB) · 합자 0 · 식 글꼴 깨짐('=' → '¼' 9 · 괄호 'ð' · 'Þ' 11 · 식 안 δ → 'd').
- 보류 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(햐) · (겨)–(혀) · (교)–(됴): **(헤)(뎌)(여)(탸)(뇨)(햐)(퍄)(매)** 근거(강) · (먀)(냐)(세)(뱌)(며)(체)(내) 근거(중) · (루)(베)(피)(대)(다)(이)(어) 약 · (마) 근거 0 · (라)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷(측정 확산계수의 방법 · 역모형 · 기하 가정 표기 · Nernst–Einstein · Darken 환산의 종(Li ↔ 공공) 일관성 표기 · 방법 신뢰도 판정에 쓴 기준 측정의 자기 일관성 검사 · (선택) 조성 축의 출처 표기 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 102호 행 · 102편 누적 · Evidence 아흔일곱 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](여든다섯 번째 적용 · 주장하지 않는 것) · [[spm-grouped-parameter-identifiability]](적용 표 102호 행 둘 · 한계) · [[data-window-identifiability]](102호 절 — 방법별 시간 창 · 한계 · 관련) · [[assb-sensitivity-sweep-vs-identifiability]](102호 절 · 처방 30 · 주장하지 않는 것) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: 새 개념 페이지("측정 확산계수의 층위") 만들지 않음 — 위 다섯 페이지의 절 · 행으로 충분 · 새 판단 거리로 올림 · [[constrained-crb-identifiability]] 변경 안 함(FIM 계산 없음) · 유한 Warburg 를 전 주파수로 적합하지 않음(무릎 · R_D·C 두 어림만) · 그림 3 · 4(a) · 15(a) 는 격자 판독(`[도표]`) — 7 · 9 · 11 · 12 · 13 · 14 · 5 · 6 · 8 · 10(b) · 15(b) · 16 은 화소 판독 · [5] Bouwman · [6] Jang · [7] Xia · [10] Bates · [13] Reimers & Dahn · [19] Montoro 원문 미열람 · 원 참고문헌(26 · 91 · 98 · 99 · 100호 인용분) 다시 열지 않음 — digest 전사 대조 · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행 L291(✅ 102호 흡수 · 지목 칸 "26 · 98 \| 2" 그대로) · 재지목 셋(Jang · Neudecker · Dudney 2001 L267 99 → 99 · 102 = 2 · Xia · Lu · Ceder 2006 L238 98 → 98 · 102 = 2 · Reimers & Dahn 1992 L350 62 · 97 · 98 → 4) · 새 행 셋(★★ Bouwman · Boukamp · Bouwmeester · Notten 2002 *JES* 149, A699 [5] · ★ Bates 외 2000 *JES* 147, 59 [10] · ★ Montoro · Rosolen 2004 *EA* 49, 3243 [19]) · 지목 누락 0 · §3-b 표시 · §4 갱신 기록 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 62 행.
- 후속(서지 기준, 미열람): **Jang Y.-I., Neudecker B.J., Dudney N.J. 2001 *Electrochem. Solid-State Lett.* 4, A74**([6] — ★★ 재지목 → 2 · 고체 전해질 셀 LCO 막 D̃ · ϕ 출처) · **Bouwman P.J., Boukamp B.A., Bouwmeester H.J.M., Notten P.H.L. 2002 *J. Electrochem. Soc.* 149, A699**([5] — ★★ 새 · Notten 연구실 LCO 막 D · 상도) · **Bates J.B. 외 2000 *J. Electrochem. Soc.* 147, 59**([10] — ★ 새 · 두께 → 배향) · **Montoro L.A., Rosolen J.M. 2004 *Electrochim. Acta* 49, 3243**([19] — ★ 새 · ϕ 정의) · **Xia H., Lu L., Ceder G. 2006 *J. Power Sources* 159, 1422**([7] — ★ 재지목 → 2) · **Reimers J.N., Dahn J.R. 1992 *J. Electrochem. Soc.* 139, 2091**([13] — ★ 재지목 → 4) · ☆ [1]–[4] · [8] · [9] · [11] · [12] · [14]–[18] · [20] · [21].
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 140).

## [2026-10-03] ingest | assb 103호 — Shao Y.-q., Shao X.-d., Sang L., Liu H.-l. 2022, A Fully Coupled Mechano-Electrochemical Model for All-Solid-State Thin-Film Li-Ion Batteries with Non-Porous Electrodes: Effects of Chemo-Mechanical Expansions on Battery Performance and Optimization Strategies for Stress Evolution (J. Electrochem. Soc. 169, 080529)
- raw: `raw/papers/shao2022_thin-film-assb-mechano-electrochemical-stress-partial-molar-volume.md` (sha256 봉인 7da0ce61…2b3f69 — `pdf_sha256` 813444c0…81723cdf10 · 1,591,783 B · 호출자 sha256 일치(직접 재계산) · SI 없음(보충 언급 0 — 직접 다시 셈 · /EmbeddedFiles 빈 사전) · 원자료 · 코드 공개 0('available from the corresponding author upon reasonable request') · 데이터 ZIP 0(`[데이터]` 표시 0)) · 그림 `raw/figures/shao2022_thin-film-assb-mechano-electrochemical-stress-partial-molar-volume/` (자동 12 = `fig_1` … `fig_9` · `fig_11` · `fig_12` · `fig_13`(SI 오판 0 — `SI_TAG` False 를 실행 전 정규식 · 실행 뒤 이름으로 확인 · `fig_S…` 0) + **수동 4**(그림 1 전폭 · 그림 10 · 표 I · 표 II — 300 dpi) · **연 것 16/16** · 자동 크롭 문제(**`fig_1` 잘림** — 쪽 전폭 그림의 왼쪽 단만 · **그림 10 누락** — 캡션이 그림 오른쪽 단이라 '그래픽 없음' 제외 · **표 I · II 미인식**(로마 숫자 캡션) · `fig_6` · `fig_12` 캡션 900 자 본문 오염 · `fig_13` 오른쪽 축 제목 끝 경계) 는 `figures.json` note 16 에 · 그림 3 만 래스터(555×424) — 나머지 12 장은 **벡터 경로를 PDF 에서 꺼내 축 눈금으로 판독**(`[도표·벡터]`) · 97호 그림 2 는 크롭 화소로 대조(`[도표·화소]`) · 식은 쪽 렌더 조각(판독용 · 커밋 안 함)). `raw/figures/_sources.json` — 이 편 항목(16) 추가 · 다른 항목 변화 0.
- **4차 묶음 파일 63**(원장 §1 요청 14 편 중 열셋째 · 2026-10-02 사용자 공급) · **모형 편 — 무공극 박막 ASSB(NCM111 240 nm \| 고분자형 이원 SE 'LiTFSI' 2 µm \| 흑연 200 nm + 폴리우레탄 스페이서)의 1D 역학–전기화학 결합(COMSOL 5.5) · 자기 실험 0** · 원장 행 "★ … 26 \| 1 \| Q1 \| 12호가 재인용한 'Shao — 접촉 면적 파라미터' 와 같은 편인지 미확인" · 지목 26호 §11 후속([14] ★) = **1 = 원장(L295) 일치**(94호 :713 · :742 · :756 = *Energy* 239 행의 '다른 편' 교차 · 12호 Shao = *Energy* 239 · lu2022 :61 = *JES* 169, 080504 다른 편) · Xidian University + Tianjin Institute of Power Sources · © 2022 ECS / IOP(OA 0 · AI 학습 유보 문장) · PDF 13 쪽(IOP 표지 + 논문 12 쪽 · 인쇄 쪽 번호 없음) · 그림 13 · 표 2 · 식 [1]–[70] · 참고문헌 1–51(빠진 번호 0) · 이 편이 인용한 우리 digest 셋([5] = 97호 · [10] = 69호 · [11] = 66호) · 4차 묶음 13 편 중 인용 = 파일 57 하나.
- ★★★★ **(a) 12호 '접촉 면적 매개변수' 의 Shao ≠ 이 편 ❌(원문 확정)**: 지면에 접촉 면적 변수 0(`contact` 6 회 · `area` 1 회 전부 정성 · 계면 "fully integrated") · `Newman` 0 · '0.4–1 MPa' 0 · '최적 압력' 문장 0 · ★ 이 편이 [41] **Shao · Liu · Shao · Sang · Chen *Energy* 239("21929")** 를 표 I 매개변수 출처('41–43')로 인용 — 12호 [63] = 이 편 [41] = 94호 [16] = 원장 L298 · 94호 서지 판정 확정 · 원장 L295 '미확인' 닫힘(*Energy* 239 원문은 미열람).
- ★★★★ **(b) 닫힌 꼴**: 박막 확산 τ 1.15 · 0.50 s ≪ 충전 540 s · σxx 균일 → 층 평균 0-D 대수(식 26–29 · 45 · 54–56 · 61 · 63–67)가 그림 4(rms 0.58 mV) · 10(c)(RT/F 0.02556–0.02568 V → **T ≈296.6–298.0 K**) · 10(g)(rms 0.10–0.22 mV) · 5 · 6 · 7 · 9 · 12(±1 %)를 다시 냄 — 단 **T 298 K(표 I 333 K ↔ 본문 'T is the room temperature') · i₀ 의 c_Li⁺ mol L⁻¹(식 24–25 · k SI 그대로면 V_ove 1.4–4.7 ↔ 그림 42–113 mV)** · 표 I 그대로면 그림 4 rms 58 mV · 끝 상태 SOC 0.9372 · 540.5 s · σxx −0.6017 MPa · 음극 +7.230 % · 양극 −2.982 % · SE −0.3646 %(인쇄 7.22 · 2.98 · 0.36 % ✅) · σ_h(양극) 3162 · (음극) −371 MPa(그림 9 ✅).
- ★★★★ **(b) 두 응력**: σxx = −K(Δl_c + Δl_a) 의 직렬 컴플라이언스 **99.87 % 가 SE**(K_SE 8.25 × 10¹³ Pa m⁻¹) · 전압 몫 −0.008 / +0.016 mV ↔ 전압 · 용량을 움직인 것은 **면내 구속(ε_yy = ε_zz = 0 · [40] Grazioli)의 σ_h — 양극 +3.16 GPa · 면내 σ_yy = σ_zz +4.75 GPa → V_str 91.4 mV** · `[재현]` 면내 자유면이면 Ωc 0.834–5 모두 SOC_cut 0.9899(용량 효과 0) · V_str = **0.1858 V × Δx**(기계 매개변수 여섯의 묶음 하나 = OCP 정규 용액 항 꼴) · Ωa 1.15(σxx +0.265 MPa 인장)도 용량 +1.60 % — 'σxx = 0' 과 '용량 증가' 는 독립.
- ★★★★ **(b) Ω 사슬(97호)**: 그림 8(a) "The data in ref. [5]" = 97호 ✅ · `[도표·벡터 ↔ 도표·화소]` [5] 그림 2(b) NCM-111 과 x 0.25–0.30 ±0.1 · x 0.45–0.93 +0.46–1.06 cm³ mol⁻¹ · x 0.94–1.0 은 [5] 에 없음 · 표 I Ωc 2.3('the average') ↔ 운전 창(x 0.488–0.98) 평균 1.84 · [5] 그림 2(a) NCM-111 격자 ΔV/V −0.64 … −0.71 %(x 0.926 → 0.488) ↔ [5] V̄m 적분 2.44 %(×3.4–3.8 — 97호 ×3 의심) ↔ 이 편 곡선 3.50 % ↔ 모형 4.78 %(**×6.7–7.5**) · 음극 Ωa 4.17 = ×1(97호 '≈13 %') · `[재현·가정]` 격자 기준 Ωc 0.31–0.34 면 m 0.074–0.082 · σxx −1.16 MPa · V_str 18 mV · NCM111 E 199 · μ 0.25 = 97호 표 1 값.
- ★★★★ **(c) 검증(그림 4)**: [45] = **Zhang Z. … Han W.-Q. 2021 *Energy Storage Mater.* 43, 229**('Stable all-solid-state lithium metal batteries …') — **63호(Zhang W. … Janek 2017 *JMCA*) 아님 ❌** · 셀 정보 · SOC 정규화 0 · 모의 = 그림 5–10 과 같은 실행이 4.03 V 를 넘어 4.150 V(SOC 0.993)까지(D4) · `[도표·벡터]` 최대 |ΔV| 96 mV @SOC 0 = **2.66 %**(인쇄 '최대 1.71 %' = SOC 0.90 국소 1.72 % — D3) · rms 35.4 mV · `[재현]` 응력 끔 + V^r 61.6 · **응력 진폭(≡ OCP g·Δx 항) 자유 + V^r 11.7 mV**(×2.17) — '검증' 은 역학 결합을 시험하지 않는다(이상 격자기체 OCP · V^r 3.8 V).
- ★★★ **(d) Q6 · 처방**: 외부 압력 입력 0 · 정변위 셸(양끝 u = 0) + 면내 강체 · 예압 0 · '0.6 MPa' = 반력(출력 · SOC 선형) · `[재현·가정]` 97호 표 1 무기 SE(같은 2 µm)면 −60 … −127 MPa(LiPON −195) · 스페이서 E_sp 1 MPa · 100 nm **79.36 %**(인쇄 79.33 % · σxx 만 — SOC_cut 0.9372 불변) · 500 MPa 0.76 %(인쇄 0.73 · l_sp 미인쇄) · 체적 손실 6.148 %(= 150/2440 ✅) · 중량 0.102 % ↔ 표 I ρ 0.176 %(D9) · '압축 응력으로 홀더 대체' = 셸 구속 위 · 결론 'm should be greater than mzs' 부호 반대(D7) · 그림 8(b) 비선형 −0.629 MPa ↔ 'fluctuates around 0 MPa'(D6 · `[재현]` 적분 정의면 −0.11).
- ★★★ **(d) Q1**: `θ(N)` 0/103 · 접촉 · 박리 계산 0 · ★ '용량 변화'(Ωc 4.647 → −39 %)는 같은 Li 재고에서 평형 항이 차단을 당긴 것(η · θ · Q_material 불변 · 율 무관 · 휴지 불변) → 전압 기반 용량에서 `LAM_PE` 서명(`[해석]` · 면내 구속 가정의 크기).
- ★★★ **표 II**: OAT · M = RMS(G/X) · `[재현·가정]`(x_n 0.30–0.70 · 0.5 제외) β^s1 2.763 × 10⁻² · β^s2 1.452 × 10⁻¹ ✅ · γ^s1 2.02 × 10⁻² · γ^s2 1.52 × 10⁻² ↔ 인쇄 6.91 × 10⁻³ · 1.99 × 10⁻¹¹(D10) · 기준점 γ = β 에서 i₀ 응력 인자 ≡ 1.
- **채움표 103호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 해당 없음(층 하나 — 응력 평형 항의 차단 당김 · `θ(N)` 0/103) · Q2 없다(전압 하나 · 헤드라인 응력 관측 이득 0 · V_str ≡ OCP 모양 항) · Q3 층 하나(그림 = 표 I + T 298 K + i₀ mol L⁻¹ · Ω 사슬 ×7 · 검증 = 다른 셀) · **Q4 해당 없음 — `assb` 0/103 · 아흔다섯 번째 성질** · Q5 해당 없음(흑연 · 이상 OCP) · Q6 층 하나(입력 0 · 출력 σxx · SE 강성 · 면내 구속 · Maxwell 모형판 Ω_c/F 2.38 · Ω_a/F 4.32 mV/100 MPa) · Q7 해당 없음 · Q8 층 하나(이상 격자기체 OCP · V^r 3.8 V · T 298 K 로 닫힘).
- **곱 축퇴 처방 여든여섯 번째 적용**: 입력 점검 ❌ 여섯(모형 · 실험 0) · 곱 문장 셋(V_str = A·Δx — 기계 매개변수 여섯의 묶음 하나 ≡ OCP 정규 용액 항 · σxx ≈ −K_SE × 순 팽창 — 관측 이득 0 · '용량 손실' = 평형 몫 — 시간 영역으로도 못 가름) · 후보 메모 하나('용량 손실' 의 평형 몫 표기) · 새 줄 0.
- ⚠ 어긋남 17 건(D1 T 333 ↔ 298 K · D2 i₀ 농도 단위 · D3 '최대 1.71 %' · D4 모의 4.03 V 넘음 · D5 '+1.72 %'(그림 +1.29 · 재현 +1.33) · D6 그림 8(b) · D7 결론 부등호 · D8 '−39.13 %'(그림 −38.73) · D9 ρ_c 2.28 ↔ 4.57 · 그림 13 중량 · D10 표 II γ · D11 그림 8(a) ↔ [5] · D12 Ωc '평균' · D13 기호 'u(x₁)' · 'Δl^dis' · D14 참고문헌(21929 · 10540 · Larcht'e · Physi · 2011) · D15 Yamamoto 번호 0 · D16 식 (8) 확산 항 · (20)–(21) i^s2 · (64) SE 부호 · D17 '79.33 %' 조건 탈락).
- PDF 메타데이터: `PDF 1.7` · 13 쪽(p. 1 595 × 842 · pp. 2–13 585.354 × 783.326 pt) · 암호 0 · title = 전체 제목(호출자 메모는 콜론에서 끊김) · author "Yu-qiang Shao" · subject "Journal of The Electrochemical Society, 169(2022) 080529. doi:10.1149/1945-7111/ac8b3a" · creator "IOPP" · producer "iTextSharp™ 5.5.13.4 … (AGPL-version); modified using iText® 5.5.13.5 ©2000-2026 iText Group NV (IOP Publishing Ltd; licensed version)" · 생성 D:20220826165919+05'30' · 수정 D:20261002134940+01'00'(호출자 메모와 같음 ✅ — 표지 내려받기 시각) · XMP 5,670 B(VoR · noindex · dc:creator 넷 · CrossMark 2022-08-29 · AI 학습 유보 저작권 문장) · 트레일러 ID 두 값 다름 · /FICL:Enfocus · /EmbeddedFiles 빈 사전 · PageLabels 1 부터 · `%%EOF` 1 · 래스터 3(표지 둘 + 그림 3) · NFKC 변환 78(합자 73) · 식은 낱글자 흩어짐.
- 보류 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(햐) · (겨)–(혀) · (교)–(쇼): **(세)(여)(뇨)(셔)(퍄)(텨)(탸)(댜)(치)(펴)(이)** 근거(강) · (노)(태)(에)(체)(먀)(햐)(제)(캐)(뱌) 근거(중) · (하)(며)(냐)(대)(혀)(교) 약 · (쿠) 재지목(Yamamoto 2020 → 4) · (마) 근거 0 · (라)(바)(사) 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**. 새 판단 거리 넷(면내 구속 응력 성분 표기 · 부분 몰부피 입력 층위 사슬 · 모형 · 측정 '용량 변화' 기구(차단 당김 ↔ 물질 손실) · (선택) 결합 항의 관측 꼴 — 글자는 호출자).
- 컴파일: 새 개념 0 · 갱신 [[assb-contact-loss-vs-lampe]](채움표 103호 행 · 103편 누적 · Evidence 아흔여덟 번째 · 새 제약 5 · Status Log · 주장하지 않는 것) · [[assb-lampe-contact-product-degeneracy]](여든여섯 번째 적용 · 주장하지 않는 것) · [[spm-grouped-parameter-identifiability]](적용 표 103호 행 둘 · 한계) · [[assb-sensitivity-sweep-vs-identifiability]](103호 절 · 처방 31 · 주장하지 않는 것) · [[assb-maxwell-ocv-derivative-channels]](§5 모형 쪽 · 근거 줄 · 주장하지 않는 것) · [[assb-stack-pressure-operating-window]](103호 절 · 주장하지 않는 것) · [[assb-apparent-capacity-decomposition]](103호 절 — 세 항 밖 평형 몫 · 주장하지 않는 것) · index 불변(새 페이지 0 · 페이지 수 57).
- 하지 않은 것: 새 개념 페이지("응력 평형 몫 · 결합 항의 관측 꼴") 만들지 않음 — 위 일곱 페이지의 절 · 행으로 충분 · 새 판단 거리로 올림 · [[data-window-identifiability]] · [[constrained-crb-identifiability]] 변경 안 함(창 · FIM 계산 없음) · COMSOL 재구현 대신 층 평균 0-D 닫힌 꼴(확산 · 응력 기울기 무시 — τ ≪ 충전 시간)로 재현 · 비선형 Ω 구현(그림 8(b))은 적분 정의 하나만 시험 · [41] *Energy* 239 · [45] Zhang 2021 · [34] Song 2020 · [38] · [40] Grazioli 원문 미열람 · 원 참고문헌(12 · 26 · 94 · 97호 인용분) 다시 열지 않음 — digest 전사 + 97호 그림 2 크롭 화소 대조 · wiki 밖(`bms-balancing/docs/`) 미수정 — 호출자 몫.
- wiki 밖(호출자 몫): 원장 §1 — 이 편 행 L295(✅ 103호 흡수 · 지목 칸 "26 \| 1" 그대로 · 12호 Shao = 다른 편 확정) · 재지목 다섯(*Energy* 239 L298 12 · 94 → 3 · Strauss L222 87 → 2 · Doux *JMCA* L421 → 5 · Fabre L232 → 4 · Yamamoto 2020 — 행 0 · (쿠) 꼬리 → 4) · 새 행 여덟(★★ Song 2020 *JPS* 452 [34] · ★★ Zhang Z. 2021 *ESM* 43 [45] · ★★ Grazioli 2019 *EA* 296 [40] · [38] · ★ Li R. 2019 *JES* 166 [42] · ★ Li Q.F. 2021 *IJER* 45 [43] · ★ Hao 2020 *JES* 167 [35] · ★ Tian 2020 *JES* 167, 090541 [32] · ★ He 2019 *AEM* 9 [6]) · 지목 누락 0(새로 — Yamamoto 2020 은 88호 기록 · (쿠) 대기) · §3-b 표시 · §4 갱신 기록 · `ASSB_TRANSFER_NOTE.md` §6-3-j 파일 63 행.
- 후속(서지 기준, 미열람): **Shao Y.-q. 외 2022 *Energy* 239, 121929**([41] — ★★★ 재지목 → 3 · 접촉 면적 매개변수의 실제 자리) · **Yamamoto M. 외 2020 *JPS* 473, 228595**([47] — ★★★ 재지목 → 4 · 원장 행 0) · **Song X. 외 2020 *JPS* 452, 227803**([34] — ★★ 새 · 확장 BV 원전) · **Zhang Z. 외 2021 *ESM* 43, 229**([45] — ★★ 새 · 검증 곡선) · **Grazioli D. 외 2019 *EA* 296, 1122 · 1142**([40] · [38] — ★★ 새 · 면내 구속 출처) · **Strauss F. 외 2020 *ACS Mater. Lett.* 2, 84**([12] — ★★ 재지목 → 2) · Doux 2020 *JMCA*([9] · ★ → 5) · Fabre *JES* 159, A104([44] · ★ → 4) · Li R. 2019 *JES*([42] · ★) · Li Q.F. 2021 *IJER*([43] · ★) · Hao 2020 *JES*([35] · ★) · Tian 2020 *JES*([32] · ★) · He 2019 *AEM*([6] · ★) · ☆ 나머지.
- `python3 wiki/tools/lint.py` → **0 errors, 0 warnings** (pages 57, raw files 141).

## [2026-10-03] ingest | GitHub 연구 브리핑 (2026-10-02 조사분) — PyBaMM #5813 실측 · pyimpspec · ISU-UConn 자료
- raw: `raw/articles/2026-10-02-github-research-briefing.md` (원문 + 1차 대조 — 공개 저장소를 git 으로 직접 받아 읽은 원문 · WebFetch 요약 아님) · `raw/repositories/2026-10-03-pybamm-pr5813-graded-electrode-and-synthetic-truth.md` (구배 음극 시험 · 우리 truth 두 조건 · `averages.py` diff · 출력 원문) · `raw/repositories/2026-10-03-pyimpspec-5.2-smoke-synthetic-2rc.md` (버리는 py3.12 venv · 합성 2-RC · 출력 원문) · `raw/repositories/2026-10-03-reil-uconn-moo-known-truth-table.md` (노트북 셀 · `util_LFP.py` 발췌 · 파일 해시 — 읽기만)
- 사용자 지시: "관련해서도 확인을 해보고 사용가능한지 판단을 해보고 추가로 필요한거 있음 codex 리뷰 받자"
- ① [[pybamm]] #5813 (2026-09-30 병합 · **26.9.0.0 미포함**): 버그는 우리 설치본 26.8 에 있고 구배 음극에서 `LLI [%]` 0.273 % · 음극 리튬 0.92 % 오차 → 패치로 1e-12 급. **우리 truth 에는 용량 Δ0 · 전압 ≤4.9e-8 V** (경로 밖 — 스칼라 활물질 분율 · PyBaMM 리튬 변수 미사용) · 단 바이트는 바뀐다. 상한 결정은 여전히 #5755 (2.7 mV) 가 주인 — §1-2 사용자 결정 대기 그대로.
- ② 새 페이지 2: [[pyimpspec]] (분석 전용 · GPL · py≥3.12 · 넓이는 버티고 높이는 λ 따라 7 배 · 가짜 피크 둘 — 제안 P1 · P2) · [[isu-uconn-lfp-gr-emulated-degradation]] (설계 참값 11 셀 · 같은 4 변수 구조 · 외부 검증 후보 — 제안 E1–E3)
- 갱신: [[pybamm]] (#5813 절 · 위험과 할 일) · [[22p-physics-or-degeneracy]] Status Log · [[isc-detection-vs-balancing-masking]] Status Log (탐색 음성 2 회째) · index 2 줄 + 머리 (57 → 59)
- 격리: 운영 환경 · 등록부 · 산출물 불변 · 설치는 스크래치패드의 버리는 venv 에만 (PyBaMM 사본 패치 · pyimpspec + cvxopt) · 남의 pickle 열지 않음 · RUN_SCOPE 0 바이트
- 하지 않은 것: requirements 상한 (RUN_SCOPE · 사용자 결정) · pyimpspec P1 · P2 · ISU-UConn E1–E3 (전부 승인 대기) · 논문 · 자료 페이지 열람
- 모델 provenance: 새 entity 2 의 frontmatter 에 `model` · `effort` 를 두지 않았다 (이 세션 하네스 규칙 — 저장소 산출물에 모델 식별자 금지)
