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
