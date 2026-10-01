# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, verify, archive, delete

## [2026-07-30] create | Wiki initialized (kit)
- llm-wiki harness 킷(`llm-wiki-kit_260730`) — tools + commands + hooks + CI. 이 저장소에는 2026-09-11 에 이식했다 (아래).

## [2026-08-06] update | 하네스 v1.8~v1.10 채택 (킷 원본에서 전파)
- frontmatter `claimType`/`evidenceScope`, 타입 2종(`questions/` `syntheses/`), Paper Ingest Mode opt-in, raw changelog `raw/articles/2026-08-06-cmds-llm-wiki-changelog.md`.

## [2026-09-11] create | Li2S ASSB mothership 이식 — `main` 브랜치, wiki/ + webapp + 논문 에이전트
- 킷과 선행 브랜치의 적응(`wiki-*` 커맨드, hook 위치, repo-root 상대 경로, `<action>(wiki):` 접두, `no-hardcoded-branch-name` lint)을 그대로 가져와 도메인을 **Li2S 양극 all-solid-state Li–S** 로 바꿨다. SCHEMA 에 단위 규율·digest 4구분·`compare:` 블록·Li2S 태그 시드를 추가. 페이지에 모델 식별자를 적지 않는 규칙.
- 설계 기록: `raw/transcripts/2026-09-11-li2s-wiki-kickoff-session.md` (사용자의 연구 설명 원문 + 설계 결정 + 미결 Q1–Q4, sha256 봉인).

## [2026-09-11] create | 연구 시드 — satellite 2 · 개념 5 · 비교 1 · 질문 2 · 가이드 4
- entities: [[li2s-assb-reference-cell]] (진행 중) · [[anode-free-li2s-assb]] (계획).
- concepts: [[li2s-assb-composite-cathode]] · [[li2s-activation-first-charge]] · [[carbon-dimensionality-electron-network]] · [[capacity-normalization-li2s-vs-sulfur]] · [[mixing-equipment-ball-mill-thinky]].
- comparison: [[composite-cathode-mixing-routes]]. questions: [[reference-cell-500-600-mahg]] (active) · [[one-step-vs-two-step-mixing]] (open).
- guides: [[new-project-kickoff]] (상대 경로판) · [[paper-ingest-mode]] (모델 필드 제거) · [[seminar-prep-from-digest]] (신설) · [[wsl-li2s-setup]] (신설).
- 원칙: 사용자 진술만이 근거인 페이지는 `evidenceScope: user-original`, 일반 지식은 "미검증 배경" 으로 표시하고 인용 금지. 실험 수치는 위키에 없다 (정본은 실험 노트).

## [2026-09-11] ingest | Kim et al. 2023 — Long-lasting, reinforced electrical networking in a high-loading Li2S cathode (Carbon Energy 5, e308)
- raw 봉인: `raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md` (14쪽 본문 절별 해체 + SI 전문 대조, 공백표 G1–G14, `[인쇄]/[도표]/[해석]/[재현]` 4구분, `compare:` frontmatter). 그림: 본문 8장은 `extract_figures.py` 캡션 앵커 크로핑, SI 11장은 .docx 내장 이미지 → `raw/figures/kim2023_…/` (19장, `figures.json`).
- 판독: Fig. 1–8, S1, S4, S11 을 직접 봤다. S2·S3·S5–S10 은 캡션·본문만.
- 발견: 본문 p.8 "899.6 mAh g⁻¹ (11.5 mAh cm⁻²)" 의 괄호는 0.1 C 값 — 0.5 C 는 Table S1 의 9.3 mAh cm⁻² (G3). "800 사이클 안정" 은 CE 기준, 용량은 43 %.
- 컴파일: [[li2s-activation-first-charge]] · [[carbon-dimensionality-electron-network]] · [[capacity-normalization-li2s-vs-sulfur]] 의 근거. RQ 라우팅: [[reference-cell-500-600-mahg]] Evidence For(H1·H2·H4) · [[one-step-vs-two-step-mixing]] Evidence For(H1).

## [2026-09-11] query | Kim 2023 논문 세미나 준비
- [[kim2023-seminar-prep]]: 한 줄 메시지, 5막 스토리라인, 16장 슬라이드(그림 파일·패널 지정), 양단위 숫자표, 비판 3+3, 우리 연결 표, 예상 질문 10, 체크리스트. 절차는 [[seminar-prep-from-digest]] 로 가이드화.

## [2026-09-11] query | Kim 2023 세미나 초안 덱 (pptx)
- `queries/kim2023-seminar-draft.pptx` — [[kim2023-seminar-prep]] 의 슬라이드 표를 18장 덱으로 (그림은 `raw/figures/kim2023_…/` 크롭, 발표자 노트 포함, 발표자·날짜는 빈칸). 텍스트는 그 페이지에서만 가져왔고 수치의 `[도표]` 표시를 유지했다. 이 환경에는 렌더러(LibreOffice Impress)가 없어 시각 QA 는 휴리스틱(텍스트 상자 폭·높이 계산)으로만 했다 — 열어서 한 번 훑을 것.

## [2026-09-11] update | 작업 브랜치 이전 — `main` → 루트 CLAUDE.md 하드룰 1 의 브랜치
- 사용자 요청: main 에서 작업하지 않는다. 오늘의 커밋 5개를 새 브랜치로 옮기고 main 은 Initial commit 으로 되돌렸다. 킥오프 기록(raw, 불변)의 "main 을 mothership 으로" 결정은 이 항목으로 정정한다. 브랜치 이름은 위키에 적지 않는다.

## [2026-09-11] lint | 브랜치 전수조사 — 드리프트 게이트 3종 신설, 깨진 도구 제거
- 전수조사(실행 증명): lint 0 errors(고의 파손 시 3 errors 로 죽는 것까지 확인) · 라우트 22개 200 · 그림 19장·정적자산 11개 서빙 · hook 2종 차단/통과 · shell 7 + python 7 문법 · CI green · sha256 봉인 · `figures.json` 19 ↔ 디스크 19.
- **발견 1 (하드룰 위반)**: `tools/new-page.py --model` 이 페이지 frontmatter 에 모델 식별자를 쓰고 있었다 — 루트 CLAUDE.md 하드룰 6 이 금지한 바로 그 자리다. 플래그 제거 + lint `no-model-identifier` 검사 신설. API 호출용 모델 문자열은 `webapp/chat.py` env 기본값 한 줄로 자리를 고정하는 예외를 하드룰에 명시했다.
- **발견 2 (provenance 손실)**: `raw/figures/_sources.json` 이 `figures: 8 · pdfs: [main.pdf]` 로 멈춰 있었다 — SI 11장의 출처(.docx)가 통째로 빠진 상태. PDF 원본을 저장소에 넣지 않으므로 이 파일이 유일한 출처 기록이다. 19장·2소스로 재생성.
- **발견 3 (사본 drift 위험)**: 복합양극 조성·목표 용량이 webapp 템플릿·index 로 복사되어 있는데 정본([[li2s-assb-reference-cell]])과 묶어주는 것이 없었다 — 브랜치 이름 drift(검사 15)와 같은 구조. lint `canonical-copy` 검사 신설 (`raw/` 면제).
- **발견 4 (없는 게이트를 주장)**: `CLAUDE.md`/`AGENTS.md` 가 "lint 로 parity 를 확인한다" 고 적어 놓았으나 그런 검사가 없었다. `parity` 검사 신설 — 이제 Essential Rules 가 갈리면 죽는다.
- **발견 5 (깨진 도구)**: `tools/init-wiki.sh` 는 이 저장소에서 `$SRC/.claude/*` 를 복사하는데 그 경로가 없어(여기선 repo root) 27행에서 죽는다. 생성하는 커맨드 이름도 킷의 옛 이름이었다. 참조처가 없어 삭제했다. (킷 출처 기록 `raw/transcripts/kit-provenance-260730.md` 는 불변 — 그대로 둔다.)
- **발견 6 (webapp 무검사)**: CI 가 `paths: ["wiki/**"]` 뿐이라 webapp 은 자동 검사가 0 이었다. `webapp/smoke.py` 신설(84건: 등록부 전 페이지·전 그림·정적자산·읽기전용 게이트·경로탈출·보안헤더·XSS) + CI 에 webapp job 추가 + `li2s smoke`. 게이트 검사는 처음에 status 405 만 봐서 게이트를 열어도 통과했다 — Flask 자체 405 와 구분되도록 응답 본문까지 보게 고쳤다(그 실패를 재현해 확인).
- 기타: 죽은 커맨드 이름(`/inbox` `/ingest` `/verify`) 정정 · CLAUDE.md 의 "digest 6만 자" → 실측 29,143자 · pptx 산출물을 index 에 등록(시각 QA 미결 명시).

## [2026-09-30] ingest | Huang et al. 2026 — 고엔트로피 황화물 kinetic accelerator (J. Energy Chem. 118, 352)
- raw 봉인: `raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md` (46,670자, 공백표 G1–G22, `compare:` 17키). 그림 24장 = 본문 5 + SI 19 (SI .docx 내장 이미지 21개 중 2개는 수식 WMF 라 제외, 투명배경 팔레트 PNG 는 흰 배경 합성). 판독 18/24.
- **이 위키 최초의 고체계 논문**이다 (앞선 Kim 2023 은 액체계). 단 **S8 양극**이지 Li2S 가 아니다.
- 핵심: 우리와 거의 같은 셀(LPSCl · Li–In · 상온 · 양극 450 MPa)에서 첨가제 없이 탄소만 넣은 S/KB/LPSC 양극의 0.1 C 첫 방전 **S 이용률 39 %** `[도표]`, 혼합 이온–전자 전도체 6 wt% 로 **76 %** (분극전압 0.56 → 0.38 V). 복합체 DC 분극 전도도 σ_e⁻ 1.71 → 23.80 mS cm⁻¹, σ_Li⁺ 2.41×10⁻⁵ → 6.50×10⁻³.
- 라우팅: [[reference-cell-500-600-mahg]] **H2(퍼콜레이션) 에 고체계 최초 근거** · H4 보강 · **H1 에는 무근거**(S8 출발이라 Li2S 첫 충전에 한 글자도 없다 — 그 공백을 카드에 명시했다) · [[one-step-vs-two-step-mixing]] Evidence Against(2단계도 고에너지 BM 인데 55–61 % 이용률).
- digest 가 원문에서 잡은 것: 서론 전류밀도 6.83 vs 초록·결론 5.4 mA cm⁻² 오기(G3, `[재현]` 5.36 으로 초록이 맞다) · **§3.3 본문의 Fig. 5 패널 지시가 뒤집혀 있다**(G5 — 그림을 안 봤으면 결론이 정반대) · "significantly lower overpotential" 의 GITT 방전 η_max 실제 차이는 **2 mV**(G15) · 사이클 후 EIS 에서 S/HES 의 Z′ 절편이 오히려 크다(G17).
- 비판: 대조군이 "첨가제 없음" 이 아니라 "덜 좋은 첨가제(Co9S8)" 다 · 유지율은 강점이 아니고(84.0 vs 76.9 %) 실제 차이는 절대 용량 1.7–2.4배인데 초록은 유지율을 앞세운다 · **운전 스택 압력이 아예 없다** · 셀은 조건당 1개.

## [2026-09-30] ingest | Zhang et al. 2026 — 저압 anode-free ASSLSB, 반응형 Li2S + Na 집전체 (Adv. Energy Mater.)
- raw 봉인: `raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md` (53,934자, `compare:` 18키). 그림 21장 = 본문 6 + SI 15, **21/21 전부 판독**. **본문 PDF 에 Experimental 절이 없어** 재현 조건은 전부 SI 에서 옮겼다 (digest §3).
- [[anode-free-li2s-assb]] 를 정면으로 겨냥한 첫 논문. 그 페이지가 "근거 논문 없음" 으로 비워 둔 4번 항목(스택 압력·집전체)을 이 digest 로 채웠다.
- 결정적 환산 셋: **"PI3 8 %" 는 몰 기준 → 실제 43.8 wt% PI3 / 56.2 wt% Li2S**(첨가제가 아니라 절반; AIMD 셀 Li138S69P6I18 = 6/75 = 8.00 % 로 교차 확인) · **첫 충전이 이론용량 초과**(≈1330 > 1166) 이고 LiI 전량 1 e⁻ 산화 몫 `[재현]` 152 mAh g⁻¹ 가 초과분과 크기가 맞아 **요오드 산화환원이 "Li2S 용량" 에 섞였을 가능성**을 배제 못 한다 · 전해질층 127 mg cm⁻² = 복합양극의 27배.
- **단위 기준을 원문이 글자로 밝히지 않는다** — Fig. 5a 의 이론용량 수직선 ≈1166 과 Fig. S12 의 1 C = 3.26 mA cm⁻² / 2.81 mg cm⁻² = 1160 mA g⁻¹ 두 간접 증거로 `(Li2S)` 로 확정하고 근거를 digest 에 남겼다.
- 라우팅: [[reference-cell-500-600-mahg]] **H1 에 고체계 최초 근거**(같은 셀에서 pristine Li2S 첫 방전 ≈270 vs 처리 971) · **H3 에 위키 최초 근거**(격자상수 불변 a = 5.7189 Å 인데 나노결정화+비정질화만으로 3.6배; 단 SEM 은 여전히 1–5 µm 이차입자) · H4 에 실질적 답(복합양극 기준 143–159 vs 우리 목표 환산 150–180 — 같은 대역) · H2 에 **부분 반증**(탄소 MWCNT 10 wt% 뿐인데 971).
- [[anode-free-li2s-assb]] 갱신: Cu 집전체 배제(Cu–Cu ≈140 vs Na–Na ≈26.5 Ω cm², Li–Cu 60 사이클 단락) · **0 MPa 는 60 사이클 붕괴**(최소 1 MPa) · Li 은 Na 박 위가 아니라 **Na/SE 사이에** 깔린다 · **초기 5 사이클에 ≈45 % 손실**이 진짜 과제 · 진단 2개(충전 중 압력 상승 = Li 석출, 방전 말기 ≈1.65 V 단차 = 재고 소진).
- 비판: "200 사이클 ≈100 % 유지" 는 첫 방전이 아니라 5사이클 만에 ≈900 → ≈500 으로 떨어진 **뒤**를 기준으로 삼은 값(첫 방전 기준이면 63 %)이고, 그 초기 45 % 손실을 한 번도 설명하지 않는다 — anode-free 논문에서 **Li 재고 수지를 안 쓴 것**이 최대 결함 · 셀은 전부 단일 곡선인데 초록은 소수 둘째 자리까지 쓴다 · 원문 내부 불일치 7건(§14).

## [2026-09-30] lint | canonical-copy 검사를 기준(basis) 인식으로 고침
- 2026-09-11 에 넣은 `canonical-copy` 검사가 **오탐을 냈다** — 질문 카드에 적은 `143–159 mAh g⁻¹(composite)` 를 "목표가 바뀌었다" 로 잡았다. 그건 목표의 drift 가 아니라 복합양극 기준 환산값이다.
- 수정: 용량 범위를 **기준까지 함께** 읽고, `(S)`·`(composite)` 처럼 **다른 정규화가 명시된** 값은 환산으로 보아 면제한다. 기준이 없거나 목표와 같은 기준인 값만 정본과 대조한다.
- 고친 뒤 재검증(실행 출력): 오탐 0 · 기준 없이 400–500 으로 바꾸면 잡힘 · `(Li2S)` 기준 420–480 도 잡힘 · 조성 30:55:15 도 잡힘. 검사를 무력화하지 않았음을 확인했다.

## [2026-09-30] ingest | ASSB 논문 4편 (Cronk 2026 · Qu 2025 · Wang 2023 · Lee 2026) + raw 오염 사고
- raw 봉인 4편, 전부 **SI 미확보**(본문 PDF 만) — 각 digest 가 "SI 미확보"를 공백표 G1 로 최상단에 박았다.
  - `cronk2026_…` (Nat. Commun., Meng 그룹 + LG Energy Solution) 57,619자 · 그림 7장. ★ **우리와 조성이 같다** — 활물질 : LPSCl : AB = 30 : 50 : 20 wt%, Li–In, 25 °C. 혼합 경로 직접 비교(one-step ≈1500 vs multi-step ≈610 vs hand-mix ≈200 mAh g⁻¹(S)), pristine 상용 Li2S 반쪽셀 **723 mAh g⁻¹(Li2S)**(이론 62 %), 밀링 레시피 수치(500 rpm 1 h, BPR 1:30, Ar; **LPSCl 단독 10 h 밀링은 전도도 30배 하락**).
  - `qu2025_…` (Nano Energy, UW-Milwaukee + PNNL) 50,785자 · 그림 8장. ★ **스택 압력 구멍을 메운다** — 정압 7 MPa(스프링+LVDT) vs 정용적(볼트). Li2S 양극 총 수축 −19 µm / −0.60 MPa, **첫 충전 한 번에 −10 µm(총 수축의 53 %)**, 100 사이클 유지 정압 63 % vs 정용적 50 %. 양극 Li2S:C65:LPSCl = 33:17:50 wt% — **SE 50 wt% 가 우리와 동일**.
  - `wang2023_…` (Nat. Commun. 14, 1895) 49,721자 · 그림 4장(추출기가 Fig. 4 를 놓쳐 캡션 좌표로 재크롭). 저밀도 Li3PS4–2LiBH4 SE(1.491 g cm⁻³). ★ `[재현]` **우리 30:50:20 의 SE 부피분율이 48–52 vol%** 로 이 논문의 "충분" 기준 35.4 vol% 보다 13–16 %p 높다 → **우리는 SE 부피 부족 영역에 없다**. **Li–In = 0.62 V vs Li/Li⁺ 의 출처가 생겼다**(SCHEMA 가 "근거 없음, 인용 금지"로 두었던 값).
  - `lee2026_…` (Chem. Eng. J. 546, 179625, KIST) 51,102자 · 그림 6장. ★ 조성 30:20:50 wt%, Li–In, 상온 — 우리와 같은 계. 같은 셀에서 S8 출발 vs Li2S 출발을 갈랐다. in situ XRD 에서 **LiPS 도 S8 도 없이 Li2S ↔ S2–4**(Fig. 3e, 23.1° 전 구간 부재) → 고체계 도착지가 S8 이라는 Kim 2023 모델과 갈린다.
- **★ 사고: digest 하나가 다른 논문 본문으로 봉인됐다.** 논문 에이전트 5개를 병렬로 돌렸는데 `yu2024_…md` 가 **Yu frontmatter + Wang 2023 본문**으로 나왔다(본문에 CuS 0회, LPB 107회). **기존 lint 가 못 잡았다** — 두 파일 각자는 declared == actual 이라 검사 7(sha256 봉인)을 통과한다. 봉인은 "본문이 나중에 바뀌지 않았음" 만 보증하고 "올바른 본문인지" 는 보지 않는다.
- 원인: **5개 에이전트가 같은 스크래치패드에 `body.md`/`final.md` 같은 일반 이름을 써서 서로 덮어썼다.** 스크래치패드 실물이 확증한다 — `final.md` 74,555 bytes 가 `wang2023_….md` 의 정확한 크기고 오염 파일 쓰기 시각과 겹친다. **지시를 그렇게 준 내 잘못**이다(같은 경로를 주면서 이름 충돌을 경고하지 않았다).
- 조치 셋: (1) 오염 파일 제거 후 해당 에이전트에 재작성 요청 — **없는 내용을 채우지 말라**고 못박았다. (2) lint 검사 2종 신설, 고의 재현으로 작동 확인 — **19** 두 raw 의 본문 sha256 이 같으면 error · **20** frontmatter 의 `doi` 가 본문에 없으면 error(파일 하나만 봐도 잡힌다). (3) `.claude/agents/paper-curator.md` 에 Procedure 0 신설 — 스크래치는 `<scratchpad>/<slug>/` 전용 디렉토리에, Write 직후 본문 첫 300자를 눈으로 확인. `/paper` 커맨드에도 병렬 실행 주의를 적었다.
- Yu 2024 는 재작성 중이라 이 항목에 넣지 않았다. 컴파일(개념·질문카드·index)도 8편이 모인 뒤 한 번에 한다.

## [2026-10-01] create | synthesis 1호 — 고체 복합양극의 병목은 벌크 전도도가 아니라 계면의 질이다
- `syntheses/interface-quality-not-bulk-conductivity.md` 신설 (이 위키의 첫 synthesis). ASSB digest 네 편(Yu 2024 · Huang 2026 · Wang 2023 · Cronk 2026)을 합쳐야 보이는 논지라 개별 digest 나 개념 페이지가 아니라 논지 페이지로 세웠다.
- **Thesis**: 활물질 이용률을 올리는 것은 전자 네트워크의 벌크 전도도도, 이온 네트워크의 부피분율도 아니라 **활물질–황화물 계면의 질**이다.
- Argument 넷: ① Yu 가 σ_e 를 **200배 낮추고도**, Huang 이 **14배 올려서** 비슷한 개선을 냈다 — 두 논문에서 같은 방향으로 움직인 양은 σ_Li⁺ 와 활물질 표면의 새 상뿐이다. ② `[재현]` 우리는 이미 SE **48–52 vol%** 로 Wang 2023 의 "충분" 기준 35.4 vol% 보다 13–16 %p 높다 → 이온의 "양" 도 병목이 아니다 (Cronk 의 토르투오시티 모델도 같은 방향). ③ Cronk 는 첨가제·호스트 없이 **혼합 방식만** 바꿔 7배 차이를 냈고 기전은 밀링이 만드는 thiophosphate 계면상이다 — **무게 대가 0**. ④ 그래서 [[reference-cell-500-600-mahg]] 의 실험 순서를 계면 공정 변수로 바꿨다.
- **Counter-arguments 7개를 보존했다** (SCHEMA 의 synthesis 규칙: 반론 삭제 금지). 가장 센 셋: (1) 두 논문 모두 **DC 분극 측정 시료의 정체를 안 적어** 절대값 비교가 불가하고 비(ratio)만 유효하다. (3) **둘 다 전자 퍼콜레이션 고원 위일 수 있다** — 그렇다면 σ_e 가 무관해 보이는 것은 그 영역의 성질이고 탄소가 더 적은 양극은 여전히 전자 제한이다. **우리 AB 20 wt% 가 고원 위인지 아래인지는 미측정** — 이 논지의 최대 미검증 전제다. (4) Yu 의 Fig. 3d 가 **σ_e 높은 쪽에서만** "Electrolyte decomposition" 을 주석하므로 "무관" 이 아니라 "상한이 있다" 는 다른 기전일 수 있다.
- **Gap**: σ_Li⁺ 와 계면 화학을 고정한 채 **σ_e⁻ 만** 바꾼 대조를 아무도 하지 않았다. 우리 셀의 두 전도도도 미측정 — DC 분극을 AB 10/20/30 wt% 로 돌리면 반론 3 이 바로 갈린다. 그리고 **"계면의 질" 이 아직 조작적으로 정의되지 않았다**(Cronk 도 두께·조성·전도도를 직접 재지 않았다).
- 역링크: [[reference-cell-500-600-mahg]] Evidence Against 와 [[carbon-dimensionality-electron-network]] 에 "고체계에서는 이 개념의 전제가 흔들린다" 절을 달았다 — 그 개념은 액체계 단일 출처에서 왔다.

## [2026-10-03] ingest | ASSB 논문 3편 (Kim 2025 선양국 · Wan 2021 · Wang 2026) + 질문 카드 재정리
- raw 봉인 3편, 전부 **SI 미확보**. digest 는 커밋 `c4fd001` 에 들어갔다 — 다만 그 커밋 메시지가 **Kim 2025 를 언급하지 않는다**(내가 `git add -A` 로 쓸어 담았고 그때 그 digest 가 막 생겼다). 내용은 온전하고 검산도 통과했다. 이 항목이 그 기록을 바로잡는다.
  - `kim2025_…` (*Adv. Energy Mater.* 15 (2025) 2500867, **선양국 그룹** — 이 위키 첫 논문 kim2023 과 같은 그룹) 57,961자 · 그림 5장.
  - `wan2021_…` (*Nano Lett.* 21 (2021) 8488, C. Wang/UMD) 54,238자 · 그림 5장. ⚠ **주 활물질이 MoS2**.
  - `wang2026_…` (*Energy Storage Mater.* (2026)) 46,807자 · 그림 6장. ⚠ `wang2023_…` 과 **다른 Wang**.
- **★ Kim 2025 — "dual-phase electrolyte" 는 두 화합물이 아니라 같은 LPSCl 의 두 이력 상태**다 (밀링 비정질상 = 삼상 계면 담당 / 손혼합 결정상 = 두께 방향 Li⁺ 경로). 밀링이 LPSCl 의 Young's modulus 를 `[인쇄]` **21.98 → 4.63 GPa** 로 떨어뜨린다.
- **★ 최적 혼합 경로가 로딩의 함수다** (2차 방전, 0.1 C, 같은 최종 조성): 3 mg(S) cm⁻² 에서 one-step 5.00 > two-step 4.05 mAh cm⁻², **10 mg cm⁻² 에서는 4.46 ≪ 10.85 (2.4배 역전)**. → [[one-step-vs-two-step-mixing]] 에 **H5(로딩 의존) 신설**하고 카드의 질문을 "어느 쪽이 이기나" 에서 **"교차점이 어느 로딩인가"** 로 고쳤다. 교차점은 3–6 mg(S) cm⁻².
- **H2(SE 보호)에 이 위키 최초의 직접 지지** — SE 를 밀링:손혼합으로 쪼갠 비율만 바꿔 복합양극 σ_Li⁺ 가 `[인쇄]` **0.07 → 0.42 mS cm⁻¹**. 단 **고로딩 한정**으로 조건화했다. **H4(밀링 에너지 상한)에 최초의 rpm 스캔** — 같은 6 h 에서 **600 rpm 꼭지**(`[도표]` 160/620/870/670 @ 200/400/600/800 rpm). **H3 는 저로딩 한정으로 범위 축소.**
- **Cronk 2026 과의 충돌이 세 축으로 해소된다**: ① Cronk 의 1 mg cm⁻² 은 교차점 **왼쪽** ② **"two-step" 의 정의가 다르다** — Cronk 의 multi-step(밀링 SE 0 %)과 Kim 의 M&M19(10 %)가 **똑같이 실패**하므로 두 논문은 **"SE 를 밀링에서 완전히 빼면 안 된다" 에 합의**한다 ③ 밀링 좌표가 다르다(BPR 5배). 중간상도 독립적으로 같은 종(Li3PS4+n ↔ 3Li⁺–PS4+n³⁻)으로 동정됐다.
- **★★ [[reference-cell-500-600-mahg]] H2b 의 "거의 배제" 를 철회했다.** 2026-09-30 에 "Wang 2023 기준으로 우리는 이미 SE 48–52 vol% 라 배제" 라고 적었는데 **성급했다**. Kim 2025 가 **같은 조성·같은 부피분율에서 혼합 이력만으로 σ_Li⁺ 를 6배** 바꿨다. 질문을 **"SE 가 모자란가" → "밀링을 겪은 SE 가 아직 superionic 인가"** 로 고쳐 썼다. **우리 one-step 셀의 LPSCl 은 전량이 밀링을 겪었다.**
- **★ Wan 2021 — 활성화 전위 사다리가 완성됐다** ([[li2s-activation-first-charge]] 에 표). Cronk **2.4 V / 무게 대가 0**(밀링 계면상, "촉매 없이") · Wan **2.80 V / 39.9 wt%** · Zhang **2.87 V / 43.8 wt%** · Lee 컷오프 3.62 V. → **요오드 경로는 2.8 V 아래로 못 내리고, 무촉매파가 더 낮은 전위를 무게 0으로 달성한다.** 기여 분해를 한 것도 Cronk 뿐이다.
- **첨가제 없으면 첫 충전 plateau 자체가 없다** (Wan Fig. 2a, `[도표]`): 무첨가 Li2S 는 2.5 → 3.5 V 단조 상승에 ≈900 mAh g⁻¹(Li2S)(이론 77 %), LiI–LiBr 은 **≈2.80 V 평탄 plateau** + ≈1165(≈100 %). → **plateau 의 유무가 활성화 경로 개방의 지표**다.
- ⚠ **"촉매" 인지 "매개체" 인지 모른다.** 2.80 V plateau 는 Li2S 산화치고 너무 평탄·너무 길어 **매개체 반응의 모양**이고 후보는 I⁻/I₃⁻ 다. 그 논문은 "catalyzer" 를 10회 쓰면서 "mediator" 를 한 번도 쓰지 않는다. 그리고 **Wan 도 Zhang 도 할로겐화물 자신의 용량 기여를 분리하지 않았다**(`[재현]` LiI 1e⁻ 몫 109.4 / 152 mAh g⁻¹(Li2S)). → 이 위키는 **"할로겐화물 첨가제"** 로 부르고, 대조셀 **`LiI + LPSCl + AB`** 를 실험 목록에 추가했다.
- **이론 초과 용량이 digest 10편 중 6편**이 됐다 (Cronk 129 % · Lee 101–107 % · Yu 124 % · Zhang 114 % · Wang 2026 111 % · Kim 2025 Φc 137.6 %). **Kim 2025 는 그것을 숨기지 않고 LPSCl 산화분해물 리독스로 명시 귀속한 첫 논문**이다.
- Wang 2026: σ_e·σ_Li 를 **아예 측정하지 않아** 전도도 논쟁에 참여하지 못한다. 대신 **측정 규율 하나**를 줬다 — 같은 셀에서 CV(Randles–Ševčík) D_Li⁺ 가 EIS/DRT 와 **10¹⁰배** 어긋난다. → **고체셀 D_Li⁺ 를 CV 로 재지 않는다.** 내부 불일치 10건으로 수치 신뢰도가 낮아 비판적 읽기 사례로만 쓴다.
- index.md "Raw 논문" 절을 **10편 전부**로 채웠다 (그간 2편만 올라 있었다).

## [2026-10-03] lint | canonical-copy 검사의 오탐 2건을 더 고쳤다 — 검사 대상 범위 축소
- 2026-09-30 에 기준(basis) 인식을 넣어 오탐 하나를 고쳤는데, 이번에 **두 건이 더** 나왔다. 둘 다 같은 부류 — **남의 논문 수치를 인용하는 것을 우리 수치의 drift 로 잡았다**: `25:50:25`(Kim 2025 조성, 혼합 질문 카드) · `30:20:50`(Lee 2026 조성, index.md 의 Raw 논문 절).
- 수정 둘: (1) **위키 콘텐츠 페이지**(questions/syntheses/comparisons/concepts)를 대상에서 뺐다 — 문헌 수치를 인용하는 것이 그 페이지들의 본업이고, 그걸 drift 로 보면 논문을 비교할 수 없다. (2) **`index.md` 의 `## Raw 논문` 절부터는 보지 않는다** — 설계상 문헌 색인이다. index.md 의 앞부분(우리 프로젝트 요약)과 README·webapp 템플릿은 계속 검사된다.
- 대가를 적어 둔다: 위키 콘텐츠 페이지의 **우리 수치 drift 는 이제 이 검사가 못 잡는다.** 그쪽은 산문이라 문맥에서 눈에 띄고, 정본(entity)·index 앞부분·webapp 은 계속 검사된다.
- 고친 뒤 재검증(실행 출력): 오탐 0 · **index.md 본문의 30:45:25 → 잡힘** · **roadmap.html 의 30:55:15 → 잡힘** · roadmap 의 400–500 mAh → 잡힘. 검사를 무력화하지 않았음을 확인했다.

## [2026-10-04] ingest | Jeong et al. 2026 (Joule, PNNL) — TPB 와 토르투오시티의 화해 + raw 오염 2차 발견
- raw 봉인: `jeong2026_reconciling-triple-phase-boundaries-tortuosity-assb.md` **75,189자**(이 위키 최대) · 그림 7장. SI 미확보 — 본문이 SI 에 맡긴 22개 항목을 digest §14 에 전수 목록으로 남겼고 **추정은 하지 않았다**. 추출기가 Scheme 1·Graphical abstract 를 "그래픽 없음" 으로 오판해 제외했는데 실제로는 래스터가 있어 bbox 수동 지정 400 dpi 재크롭했다(`figures.json` 에 `note`).
- 조성 S : C : SSE = **49 : 21 : 30 wt%**, SE = 자체합성 Li7P2S8Br0.5I0.5(5.2 mS cm⁻¹), 성형 700 MPa, **운전 스택압 50 MPa 정용적**. 탄소 **21 wt%** 가 우리 AB 20 wt% 와 거의 같다.
- ★ **σ_e 역방향 사례가 세 번째로 독립 확인됐다.** 탄소 함량 **고정**, 같은 조성에서 **σ_e 가 6배 낮은 군(large)이 율속에서 이긴다** (2C 비용량 `[인쇄]` **1,070 vs 338 mAh g⁻¹(S)**). Yu 2024 **200배 ↓** · Huang 2026 **14배 ↑** · Jeong 2026 **6배 ↓** — 방향이 ↓↑↓ 인데 셋 다 이겼다. 그리고 **같은 방향으로 움직인 양은 여전히 σ_Li⁺ 뿐**(1.8 / 270 / **3.2배 ↑**).
- ★ **반론 3(전자 퍼콜레이션 고원)에 눈금이 생겼다.** 탄소 21 wt% 복합양극의 σ_eff,elec 이 `[인쇄]` **0.015–0.108 S cm⁻¹** 인데 Yu 2024 의 **승자**는 2.9×10⁻⁴ → `[재현]` **50–370배 낮다**. 즉 탄소 ≈20 wt% 급은 "고원의 한참 위" 일 개연성이 높다. **닫히지는 않았다** — 탄소 함량을 한 번도 바꾸지 않았고(바뀐 건 탄소의 *형태*), σ_e 와 함께 σ_ion·TPB·황 재배치가 동시에 움직인다. → **닫는 실험이 하나로 줄었다: `AB 10/20/30 wt% DC 분극`.** 이 논문이 그 프로토콜과 눈금을 동시에 준다.
- ⚠ **제목의 두 양이 본문에 숫자로 없다**(G1): τ 값 0개(정의식만, 모델 결과는 SI), TPB 는 Fig. 2B 막대 두 개(`[도표]` 마이크로포어 ≈510 vs 메조포어 ≈285 µm⁻²). 둘 다 **모델값이지 측정이 아니다**. 그리고 **Cronk 의 τ ≈ 2–3.4(SE 상만의 기하 모델)와 여기 역산 ≈36–114(계면저항 포함 측정)는 서로 비교 불가**다 — digest §4.3 에 명시.
- ★ **교차 단서 하나가 크다**: 네 호스트 중 **꼴찌가 Ketjenblack(Mes-S)** 이다. 이 위키의 **Huang 2026 대조군(S/KB/LPSCl, 이용률 39 %)**·**Wang 2023(S/KB/LPB)** 이 바로 그 KB 를 쓴다 → 두 논문의 낮은 기준선이 "탄소만으로는 부족" 이 아니라 **"하필 가장 나쁜 호스트"** 일 가능성이 처음 열린다.
- H3 강화: 최적 호스트 입자창 **2.5–7 µm**, Cronk 의 활물질 0.5–5 µm 와 **교집합 2.5–5 µm**. 단 Cronk 는 활물질, Jeong 은 탄소 호스트다. H5 강화: 첫 방전 후 양극 두께 **+46.6 %(Mic-S) vs +36.8 %(Mic-L)**, EIS 300사이클 후 1,750 vs 650 Ω. **이론 초과 용량 없음**(최대 91.8 %) — digest 11편 중 드문 경우이고 `[재현]` I⁻ 산화 상한이 1.1 % 로 작다.
- ★ **Cronk 와 밀링에 대해 정반대를 말한다**: Cronk = 밀링이 활물질 표면에 **이득**(Li3PS4+n interphase, XRD **비정질화**) / Jeong = **손해**(황을 꺼내 **결정으로 재석출**, XRD **결정화**). **증거의 방향이 반대고 서로의 관측을 측정하지 않았다**(Cronk 는 황 재배치를, Jeong 은 계면 화학을 — 게다가 Jeong 의 수세법 자체가 계면상을 씻어낸다). → [[one-step-vs-two-step-mixing]] H4(에너지 총량 최적점)의 간접 근거.

## [2026-10-04] lint | raw 오염 2차 발견 — `qu2025` 가 자기 서지를 Lee 2026 으로 적고 있었다
- **Jeong 에이전트가 작업 중 발견해 보고했다.** 내가 절별로 재확인했다 (Qu 고유어 LVDT·fixture·정압·정용적 vs Lee 고유어 cej·Chung·Eunbyoul·KIST 빈도):
  - **`# 수집 목적`(Lee 6) · `## 0. 서지사항`(Lee 12, 표 전체) · `## 1. 한 문단 요약` · `## 2. 서론이 세운 문제 틀` = Lee 2026**
  - **`## 3`–`## 18` 분석 본체 = Qu 2025 ✓ 정상** (fixture·변위·사후 SEM·DRT·3논문 압력 대조 전부)
  → 즉 **분석은 맞고 "신원" 층만 틀렸다.** 그래도 §0 서지사항을 보고 인용하면 **잘못된 논문을 인용**한다.
- **내가 위키에 라우팅한 Qu 수치는 유효하다** — 7 MPa · 사후 SEM 80.5/72.9/88.1 µm · 정압 63 % vs 정용적 50 % · 첫 충전 −10 µm 가 전부 진짜 Qu 절(§9·§10)에 있음을 확인했다.
- **역오염·추가 오염 없음**: `lee2026` 에 Qu 고유어 0건. digest 12편 전부 "frontmatter 제1저자가 본문 머리 20행에 나오나" 검사 → **qu2025 만 실패**.
- **왜 lint 가 못 잡았나**: 검사 19(본문 sha256 중복)는 두 파일이 완전히 같지 않아 통과. 검사 20(doi 가 본문에)은 **Qu 의 DOI 가 본문 666행에 참고문헌 인용으로 우연히 들어 있어** 통과.
- **검사 20 을 강화했다 — DOI 는 본문 머리 30행 안에 있어야 한다.** 근거는 실측: 건강한 digest 11편은 전부 자기 DOI 를 **본문 5–7행**(`# 수집 목적`)에 적고 2–3회 반복한다. 사고 형태를 그대로 재현(frontmatter 는 논문 A, 머리는 논문 B 서지, A 의 DOI 는 600행 뒤 참고문헌)해 **구 검사는 통과하고 새 검사는 잡는 것**을 확인했다.
- 조치: 손상 파일 제거(재작성 경로 확보 — hook 이 기존 raw Write 를 막는다) → 해당 에이전트에 **앞 5개 절만 Qu 2025 로 재작성** 요청(분석 본체는 그대로, **없는 내용 채우지 말라** 명시) → 질문 카드 2장의 `sources:` 에서 임시 제거하고 본문에 경고 블록 삽입(재작성 후 복원). 그림 8장은 정상이라 그대로 둔다.

## [2026-10-04] ingest | Qu 2025 재작성 — 오염 범위가 내 진단보다 넓었다 (§5 까지)
- `qu2025_…md` 재작성 완료. **58,373자**(이전 손상본 50,785자보다 크다 — **§3·§4·§5 가 복구됐기 때문**). sha256 `6a880165…`(이전 `8513ad8e…` 폐기).
- ★ **내 진단을 정정한다.** 나는 오염이 `## 2` 까지라고 적었는데 실제로는 **`## 5` 까지**였다. 담당 에이전트가 heading 과 **바이트 산술**로 확정했다 — 자기 `body_part1.md` 가 37,919 B 였는데 concat 시점에 읽힌 것은 26,064 B 였다. 즉 다른 에이전트가 **같은 이름으로 덮어썼고** 그 파일은 자기 §5 까지를 담고 있었다.
- 그래서 **Qu 의 §3(fixture 설계 재현 표)·§4(LTO 대조셀 Fig. 2)·§5(Fig. 3 본체)가 파일에서 통째로 사라진 상태**였다. 복구된 것 중 이전 파일에 **없던** 것: 정압 fixture 사양(Cr12MoV 플런저 φ0.495 in · PEEK ID 0.5 in · 스프링 4×14.29 lb mm⁻¹ · LVDT HGSI LPPS-SL-010) · `[재현]` 설계 환산 10행(869 N / 254.3 N mm⁻¹ / 압축 3.42 mm / **허용 변위 4.9 µm**) · 정용적 fixture(ATO DYHW-116) · 양극 조성 **Li2S:C65:LPSCl = 2:1:3 = 33.3:16.7:50.0 wt%** · one-step Fritsch P7 300 rpm 4 h · 성형 압력 전부 · **Fig. 2 대조셀 −2 µm/−0.12 MPa**(본문은 "변화 없음" — G11) · **Fig. 3: S −15 µm, Li2S −19 µm/−0.60 MPa, 첫 충전 −10 µm = 총 수축의 53 %** · 몰부피 `[재현]` 표(27.68 vs 15.49 cm³ mol⁻¹).
- ★★ **내가 사용자에게 한 말도 정정해야 한다.** 나는 "라우팅한 Qu 수치가 전부 진짜 Qu 절에 있다" 고 했는데, **−19 µm 과 −10 µm 은 파일에 없었다** — 그 두 값은 에이전트 **보고서**에서 온 것이다. 내 확인 grep 의 출력에 그 두 값이 안 보였는데 내가 알아채지 못했다. (라우팅 내용 자체는 유효하다 — 복구된 파일과 대조해 확인했다. 다만 "파일에 근거가 있다" 는 당시엔 사실이 아니었다.)
- 복구 방법: §3–§5 는 에이전트 컨텍스트의 heredoc 원문 + 무손상 PDF 덤프로 수치 대조 후 복원, §6–§18 은 손상본에서 **한 글자도 바꾸지 않고** 이어 붙였다. 없는 내용을 지어내지 않았다.
- 검증(내가 독립 실행): sha256 일치 · doi 가 **본문 머리 30행에 2회** · 제1저자 Qu 머리에 있음 · **Lee 오염어 0**(Chung·cej·Eunbyoul·KIST·Solartron·cryo-milling 전부 0) · Qu 고유어 LVDT 12·fixture 26·정압 47·정용적 46 · **절 0–18 연속** · raw 15편 본문 해시 전부 고유 · lint 0 errors · smoke 0 failures(207건).
- 질문 카드 2장의 `sources:` 를 **복원**하고 임시 경고 블록을 제거했다.
- **재발 방지 확장** (에이전트 제안을 받아 `paper-curator.md` Procedure 4 에 박았다): 봉인 직후 **① 본문 첫 300자 출력 ② frontmatter 의 doi 가 본문 머리 30행 안에 있는지 카운트** 를 의무화하고 보고에 출력을 붙이게 했다. 그리고 **조각을 concat 할 때는 직전에 각 조각의 바이트 수를 확인**하라고 적었다 — 이번 사고의 실제 기전이 그것이다.

## [2026-10-05] update | 복합양극 ball milling 조건 전수 대조표 (digest 12편) + 중복 2편 차단
- 사용자 요청: "모든 논문의 복합양극 제작 방법도 표에 추가 — ball milling 조건만 간단히". `comparisons/composite-cathode-mixing-routes.md` 에 **ball milling 조건 전수 대조표**를 추가했다 (논문 · 경로 · 장비 · rpm · 시간 · BPR · 볼·용기 · 분위기). 수치는 각 digest 의 `compare:` 블록에서 왔고 이 표는 **사본**이다 (정본은 digest → 원문).
- ★ **표에서 읽힌 것 중 가장 큰 것: BPR 을 적은 논문이 12편 중 3편뿐이다** (cronk 1:30 · jeong 50:1 · zhang ≈30:1). BPR 은 밀링 에너지를 정하는 1차 변수인데 대부분이 안 적는다 → **논문 간 "밀링 강도" 비교가 원리적으로 불가능하다.** 볼 재질·지름은 2편, 분위기는 5편, rpm·시간은 8편만 적는다. **4편(kim2023·wan2021·wang2026·yu2024)은 한 글자도 안 적고**, 그중 wang2026 은 Experimental 절 자체가 없고 yu2024 는 Methods 가 SI 에만 있다.
- 같은 Fritsch P7 안에서도 좌표가 제각각이다 — qu2025 **300 rpm 4 h one-step** · lee2026 250 rpm 6.5 h · huang2026 350 rpm 4 h · wang2023 **350 rpm 10 h** · kim2025 **600 rpm 6 h**. cronk2026 은 Retsch **500 rpm 1 h** 로 가장 짧고 세다. zhang2026 **1400 rpm** 은 3D 스윙밀이라 계열이 달라 직접 비교 불가. → **밀링 조건과 성능의 대응은 이 표로 안 나온다**(조성·활물질·SE 가 전부 다르다). 한 논문 안에서 밀링만 바꾼 스캔을 한 것은 **kim2025 뿐**(200/400/600/800 rpm, 600 최적).
- **간헐 밀링(on/off)을 쓰는 논문이 셋** — jeong 5/10 min · zhang 15/5 min · lee 30/10 min. `[해석]` 황의 m.p. 115 °C 를 의식한 설계로 보이고, **연속 밀링(cronk 1 h)과는 같은 "시간" 이어도 열 이력이 다르다** — Cronk↔Jeong 이 밀링 효과를 정반대로 보고하는 이유의 후보다.
- **S8 계는 밀링 전 멜트 함침(155–160 °C, 10–12 h)을 넣는다**(huang·jeong·kim2025·wang2023 넷). **우리 Li2S 계에는 해당하지 않는다**(Li2S m.p. 938 °C).
- 우리 조성과 겹치는 둘의 밀링이 반대다 — **qu2025(33:17:50) one-step** vs **lee2026(30:20:50) two-step**. 둘 다 작동하고 절대 용량을 적은 쪽은 lee2026 뿐이다.
- 표의 **빈칸이 곧 우리 기록 체크리스트**다: 장비·용기 부피·볼 재질/지름/개수·총 투입량·**BPR**·rpm·순 밀링 시간과 on/off 주기·분위기·단계별 조성·(S8 계면) 멜트 함침·성형 압력.
- **중복 업로드 2편을 digest 만들기 전에 차단했다**: `01b016c2…`(= kim2025, DOI 10.1002/aenm.202500867) · `f18c115a…`(= zhang2026, DOI 10.1002/aenm.71471). 업로드 PDF 의 DOI 를 기존 digest 의 `doi:` 키와 대조하는 방식으로 잡았다 — 파일 바이트는 달라도 같은 논문이었다.
- 검증(실행 출력): lint 0 errors · smoke 0 failures(219건) · `/doc/comparisons/composite-cathode-mixing-routes` 200 (표 렌더 확인).

## [2026-10-06] ingest | Liu 2026 (Li4SnS4 소결 코팅) · Zhang Jiaxu 2026 (strain coordination) + index 복구
- **digest 2편 착지** (논문 에이전트). `raw/papers/liu2026_li4sns4-molecular-mediator-low-barrier-li2s-chemistry.md` (본문 39,736자, 그림 5장) · `raw/papers/zhangj2026_strain-coordination-long-cycling-assb.md` (본문 46,973자, 그림 7장). raw 14편.
- 검증(내가 독립 실행, lint 와 같은 해시 규약 `body.lstrip('\n')`): 14편 전부 **봉인 일치 · doi 가 본문 머리 30행 안 · 그림 ≥4장 · 모델 식별자 0 · 본문 해시 전부 고유**. zhangj2026 의 타 논문 고유어(LVDT 3 · CuS 1 · Na 집전체 1)는 **§11 비교표의 의도된 교차인용**임을 문맥으로 확인했다.
- ★ **Liu 2026 의 "mediator" 는 같은 논문의 Fig. 4d 가 반증한다** — Sn 3d XPS 가 충방전 9지점 전부에서 불변이다. 매개체의 정의가 자기 산화환원이므로 이것은 **정적 계면층(interphase)**의 서명이다. 이 위키는 **"Li4SnS4 계면층(소결 코팅)"** 이라 적고 계열을 Wan/Zhang(요오드)이 아니라 **Cronk(계면상)** 에 둔다. 반론 보존: Sn 이 4+ 여도 배위된 S²⁻ 는 산화될 수 있고, Fig. 4c 의 S 2p 피팅에 SnS4⁴⁻ 성분이 없다 — 그 창이 논문에 없다.
- ★ Liu 의 **2.41 V 를 그대로 인용하면 안 된다**: plateau 가 아니라 **개시 변곡**이고 두 셀 모두 **4.0 V 컷오프까지 단조 상승**하며, 저자가 그 전위에서 SE 산화분해를 자인한다. → **H1 재정의판("활성화 완료 전위 > SE 산화 전위")은 아직 아무도 풀지 못했다**는 가장 직접적인 고체계 근거다.
- ★ **Li4SnS4 함량(반응식의 x)이 논문 어디에도 없다.** Rietveld(Rp 5.83 %)를 하고도 상 분율을 인쇄하지 않았다. `[재현]` 10–20 wt% · 4 e⁻ 만으로 **관측 개선폭 ≈100 mAh g⁻¹(Li2S)를 거의 다 설명**할 수 있다 — Wan(109.4)·Zhang(152)에 이어 **같은 급의 미분리 항이 세 편 연속**이다.
- **ball milling 전수 대조표를 14편으로 늘렸다** (사용자 상시 요청). 새 행 둘: liu2026 = **밀링이 아니라 고상 소결 코팅**(조건 전량 미기재, "Sintering for 6 h" 가 Fig. 2a 안의 글자뿐) · zhangj2026 = planetary 300 rpm 2 h one-step(BPR 미기재). **조건을 한 글자도 안 적는 논문이 4 → 5편**이 됐고, 그래서 표의 소견 3을 "미기재가 다수 관행에 가깝다" 로 고쳤다.
- ★ 표에 **다섯 번째 경로**를 소견 8로 세웠다 — **고상 소결 코팅은 SE 를 밀링에 넣지 않으므로 H2b(밀링을 겪은 LPSCl 이 아직 superionic 인가)를 원리적으로 우회한다.** 목적은 Cronk 와 같고 수단만 열이다. **단 소결 온도·분위기가 논문에 없어 지금은 시도 불가** — SI 확보 시 최우선.
- **`index.md` 의 "Raw 논문" 절이 digest 13편 중 3편만 적고 있었다 (드리프트).** 배치 ingest 가 연달아 들어오는 동안 이 절만 뒤처졌다. 발행 연도 순으로 **14편 전부를 복구**했고, ⚠ **zhang2026(산둥대 Qi Zhang, anode-free)과 zhangj2026(Jiaxu Zhang, strain)은 다른 논문**임을 색인에 명시했다.
- 검증(실행 출력): `python3 wiki/tools/lint.py` **0 errors** · `.venv/bin/python webapp/smoke.py` **0 failures (229건 · 페이지 33 · 그림 136 · 정적 11)**. ※ smoke 는 flask 가 필요해 시스템 python3 가 아니라 `.venv/bin/python` 으로 돌린다.
