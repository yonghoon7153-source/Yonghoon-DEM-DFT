# repo 표준 3종 — CLAUDE.md · kb/SCHEMA.md · kb/CODES.md

## 지금 무엇인가
CLAUDE.md(204줄)는 세션 간 유지되는 규율 원본이고, kb/SCHEMA.md(97줄)는 kb 위키 규칙, kb/CODES.md(80줄)는 T·Q·J·M 코드 체계 사전이다. 세 파일 전문을 읽었고, 대조를 위해 AGENTS.md·README.md·TIMELOG.md 전문, canonical_registry.json·citation_hazards.json·decisions.json·electronic.json, tools/kb_wiki.py·convention_check.py·ionic/msd_diffusive_check.py, kb/templates/estimand_card.md, webapp/fairchem.py 도스트링, kb/methodology/computational_methods_canonical.md·kserver116_setup.md, kb/projects/restart_runbook_2026_09_07.md 를 부분 읽었다. **못 본 것**: docs/ 89개 md 전부, kb 383개 md 중 본문을 읽은 건 10개 미만(나머지는 frontmatter·lint 출력·index 제목만 훑음), REPORT_TO_COWORK.md(85 KB), litdb digest 본문, webapp 코드 본체(9,374줄 중 도스트링만).

## 처음 오는 사람
CLAUDE.md 만 읽으면 "무엇을 하면 안 되는가"는 꽤 잘 배우지만 "지금 무엇을 하는 중인가"와 "정본이 어디 있는가"는 전혀 못 배운다. 세 파일 어디에도 `db/properties/canonical_registry.json`·`citation_hazards.json`·`db/governance/decisions.json`(이건 한 줄 있음)·`kb/reviews/INDEX.md`·`kb/methodology/computational_methods_canonical.md`·`webapp/` 로 가는 안내가 없어서, 처음 온 사람은 화면(webapp)이 존재한다는 사실조차 모른다. 게다가 CLAUDE.md 하단 40줄이 다른 폴더(research-agent/)의 지침이라 "이 폴더는 논문 에이전트다"라고 선언하는데, 그 문장이 가리키는 파일 10개가 repo 루트에 전부 없다 — 처음 온 사람은 여기서 확실히 막힌다. 실제로 오늘 kgy QE-GPU 를 세 번 틀린 것도 이 구조 문제다: 교훈(ldd)은 사후에 CLAUDE.md 에 박혔지만, 그런 낡은 환경 주장을 미리 훑는 도구(`python3 tools/kb_wiki.py env`, 19건이 검증도 정정도 없이 방치)가 이미 있는데 표준 어디에도 안 적혀 있다.

## 건드리면 안 되는 것
- CLAUDE.md:34-50 QE-GPU ldd 블록 — 오늘 세 번 틀린 대가로 쓴 것이고 tools/doping/run_force_check_scf.sh 가 이걸 그대로 구현한다(못 읽으면 시작 안 함). 줄이거나 '일반 규칙'으로 추상화하지 말 것 — 요점이 '머신마다 다르므로 규칙이 아니라 링크가 근거다' 라서, 추상화하는 순간 네 번째 오진이 난다.
- CLAUDE.md:103-105 용어 규율의 ⚠ 예외 — `kind: "estimand"` · `canary_geometry` · `estimand_card.md` 같은 기계 경로와 외부 회신 원문은 **개서 금지**. 산문만 '보고량/대조 잡/허용 서술 범위'로 바꾼다. 이걸 어기면 decisions.json·게이트·validate 경로가 끊긴다.
- kb/CODES.md §5 '왜 통합 번호로 안 바꾸나' — Q 를 문서-로컬로 두는 결정과 '문서 밖에서 부를 땐 문서명을 붙인다' 규칙. 통합 번호로 바꾸면 수백 군데 상호참조가 깨지고, webapp/templates/ledger.html:147 이 `kb/CODES.md §2` 를 직접 인용해 화면에 경고를 그린다.
- kb/SCHEMA.md 의 frontmatter enum 집합과 3축 직교(confidence / verificationStatus / explored) — tools/kb_wiki.py:34-49 ENUMS 와 1:1 결합돼 있어 이름을 바꾸면 frontmatter 있는 181개 문서의 lint 가 한꺼번에 깨진다. 특히 `explored` 는 **사람만 true** 와 `authoredBy: external`(회신 원문 표시)은 그대로 둔다 — 후자는 SCHEMA 스스로 '이 캠페인에서 제일 비싼 정보'라 적는다.
- kb/index.md 는 생성물 — 손편집 금지(`tools/kb_wiki.py index` 재생성). 마무리 조건 `lint 0 errors` 도 그대로.
- 데이터 규율의 세 금지선: band gap = fixed-occ nscf 고유값만 / MD σ 절대값 인용 금지·비율도 멀티시드 판정만(단일시드 1.33× 철회) / BVSE 정량·순위는 원본 주기셀만. 전부 실제 철회 사고에서 나온 것이라 문구를 완화하지 말 것 — 위 개선안은 전부 '단서를 **더** 붙이는' 방향이다.
- 마감 규율의 순서(조건을 **먼저** 정하고 채워졌으므로 닫는다)와 계산 규율의 순서(보고량 카드 §1–3 을 **먼저** 리뷰에 보낸다). SDCP 두 번 물림 · 여덟 번 반려의 결론이고, 오늘 LPSOCl 닫힘 조건이 이 순서를 실제로 지켜 비준됐다(결과 보기 전, 아레니우스 적합 0회 시점, git log 가 증거).
- 컨텍스트 절약 절의 `autoCompactWindow` 재도입 금지(2026-08-11 압축 루프 철회) — '다시 넣지 않는다' 를 지운 채로 재편하지 말 것.
- AGENTS.md 를 포인터로 바꾸기 전에, Codex 왕복이 실제로 AGENTS.md 를 읽는지 확인. 읽는다면 파일 자체는 남기고 내용만 포인터로(파일을 없애면 리뷰어가 아무 표준도 못 읽는다).
- kb/reviews/ 의 회신 원문 파일들 — 고쳐 쓰면 이력이 깨진다(CLAUDE.md:104-105). 색인·링크만 추가한다.

## 발견

### [P0·duplicate] agents-md-stale-fork
- **어디**: `AGENTS.md:1-59 (vs CLAUDE.md:1-79)`
- **근거**: AGENTS.md 는 CLAUDE.md 앞 79줄의 냉동 복사본이다(마지막 커밋 2026-09-03). diff 결과 ① 28행이 정면 충돌 — AGENTS `.opju … 로컬 Windows **Codex** + originpro로` vs CLAUDE `로컬 Windows **Claude Code** + originpro로`. ② 오늘 3연속 오진 끝에 쓴 QE-GPU ldd 블록(CLAUDE.md:34-50) 통째로 없음. ③ 산출물 회수 경로 `C:\\Users\\Administrator\\Downloads\\`(CLAUDE.md:55-57) 없음. ④ `## 코드 규율`·`## 계산 규율(보고량)`·`## 마감 규율`·`## 컨텍스트 절약`·`## kb 위키 규율` — CLAUDE.md 81-160행 전체, 즉 거버넌스 절반이 통째로 없다. AGENTS.md 는 '원고 작성' 절에서 끝난다.
- **고치는 법**: AGENTS.md 본문을 지우고 `이 repo 의 표준은 CLAUDE.md 하나다 — 그것을 읽어라` 한 줄 포인터로 바꾼다. 두 벌을 손으로 동기화하는 방식은 이미 실패했다(2026-09-03 이후 5일 만에 5개 절 갈라짐). 지우기 전에 Codex 왕복이 AGENTS.md 를 실제로 읽고 있는지만 확인.
- codex 필요: False

### [P0·missing] no-canonical-registry-pointer
- **어디**: `CLAUDE.md:11-21 (데이터 규율 절 전체)`
- **근거**: `grep -n "canonical_registry\\|citation_hazards" CLAUDE.md AGENTS.md kb/SCHEMA.md kb/CODES.md` → 0건. 그런데 db/properties/canonical_registry.json 의 _rules 는 스스로 이렇게 적는다: "prohibitions 는 **CLAUDE.md 데이터 규율의 기계 판독 가능한 형태**다." 즉 기계 쪽은 CLAUDE.md 를 가리키는데 CLAUDE.md 는 기계 쪽을 안 가리킨다. 레지스트리에는 42항목(gap 5 · B0 5 · E_VRH 4 · MD_Ea 8 · ICOHP 6 · SDCP 11 · σ비 3)이 status(canonical/provisional/retracted/source_pending)와 comparison_group·prohibitions 까지 달려 있고, citation_hazards.json 은 BLOCKED/HOLD/CONDITIONAL 13건을 모아 둔다.
- **고치는 법**: 데이터 규율 절 맨 앞에 3줄: 값 인용 전 `db/properties/canonical_registry.json`(정본값·status·comparison_group) → `db/properties/citation_hazards.json`(BLOCKED/HOLD/CONDITIONAL) → `db/governance/decisions.json`(판정) 순으로 본다. 검증은 `python3 tools/db/validate_canonical.py`.
- codex 필요: False

### [P0·missing] claim-binding-and-webapp-absent
- **어디**: `CLAUDE.md 전체 (webapp 언급 0회)`
- **근거**: `grep -c "webapp" CLAUDE.md` → 0. `grep -n "결속" CLAUDE.md kb/SCHEMA.md` → 0. 그런데 커밋 12e6d0c9b(2026-09-08) 은 "BG ②: 결속 이주 완료 — 전 표면 미결속 0, 래칫 은퇴"이고 커밋 메시지가 규칙을 명시한다: "`_LEGACY_UNBOUND == {}` 를 시험이 강제한다. 다시 채우는 것이 완화다", "**표면별 음성시험** — 렌더된 HTML 에서 선언만 지우고 다시 스캔한다", "`data-claim-not` … 면제가 아니라 선언이므로 id 를 이름으로 대야 하고". webapp/ 은 9,374줄 py 10개다. CLAUDE.md 는 용어 규율에서 '웹앱 화면'을 사람이 읽는 표면으로 한 번 부르지만(97행) 경로도 규칙도 없다.
- **고치는 법**: `## 화면(webapp) 규율` 절 신설: ① 숫자는 canonical_registry 에서만 온다(webapp/data.py 가 자체 보관 금지) ② 새 화면·새 숫자는 claim 결속 필수, 우연 일치는 `data-claim-not` 으로 **부인**을 선언 ③ 래칫(_LEGACY_UNBOUND) 재충전 금지 ④ 표면을 추가하면 음성시험 표면 목록에도 추가.
- codex 필요: False

### [P1·wrong] bandgap-line-overstates
- **어디**: `CLAUDE.md:12-13`
- **근거**: CLAUDE.md 는 네 값을 평평하게 적는다: "Canonical (db/properties/electronic.json): comp1 2.066 / modelc(LPSCl1.6) 2.099 / +B2O3 1.9671 / LPSOCl(+O) 2.2309 eV." 실물 두 가지가 다르다. ① **경로**: lpsocl 2.2309 의 source_path 는 `db/properties/lpsocl_dos_gap.json` 이다(`grep -c 2.2309 db/properties/electronic.json` → 3 은 전부 주석). ② **지위**: canonical_registry 의 modelc gap 항목은 아직 `method_integrity_flag.severity: "⛔ 방법 불일치 의심(재현 불가보다 심각)"` 이고 provenance 는 "⛔ 2026-08-20 3중 수색 실패 … ⇒ 이 2건은 **영구 미해소로 본다**" 다. 같은 항목이 지시까지 적어 놨다: "until_then: 네 계 gap 을 한 표에 나란히 쓸 때 **b2o3·lpsocl 만 fixed-occ 확인됨**을 밝힐 것." 그 단서가 CLAUDE.md 에 없어서, CLAUDE.md 만 읽은 세션은 네 값을 동등하게 인용한다. (comp1 은 2026-08-24 재계산으로 해소됨 — 2.0656 재현.)
- **고치는 법**: 13행을 두 줄로: 경로를 `canonical_registry.json` 로 바꾸고(계별 source_path 는 거기 있다), '네 값을 한 표에 놓을 때 comp1·b2o3·lpsocl 은 fixed-occ 실행본 확인됨 / **modelc 는 실행본 영구 미해소** 를 밝힌다' 를 붙인다.
- codex 필요: False

### [P1·stale] msd-window-superseded
- **어디**: `CLAUDE.md:16-18`
- **근거**: CLAUDE.md 는 "equilib 5 ps / prod 200 ps, **MSD 창 2–50 ps 고정**" 이라고 못박고, tools/convention_check.py:12 가 그것을 "② MSD 창 = 2–50 ps (CLAUDE.md 정본)" 로 인용해 기계 강제한다. 실물은 두 군데서 앞서 나갔다. ① tools/ionic/msd_diffusive_check.py:167 `DINC_WINDOWS = ((2, 50), (10, 50), (25, 100), (50, 100))` — 2026-08-30 회신 AK 로 판정축이 '단일 고정창'에서 '4창 D_inc plateau'로 바뀌었다(같은 파일 13행: "판정축은 **`D_inc` plateau · 창 안정성 · 실제 독립 hop 수** 세 가지다"). ② 생산길이도 200 ps 가 아니다 — decisions.json 의 D-2026-09-04-lpsocl-box331-400ps-uniform(active) 과 D-2026-09-08-lpsocl-box331-closure-conditions 의 C2 "4창 D_inc plateau ≤10 %", method_ref "생산 400 ps".
- **고치는 법**: MLIP-MD 줄을 '기본 프로토콜(200 ps · 창 2–50)' 과 '현행 판정(4창 D_inc plateau · 캠페인별 생산길이는 decisions.json)' 로 나눠 쓰고, convention_check.py 의 인용 문구도 같이 고친다. 두 파일이 서로를 정본이라 부르고 있어 한쪽만 고치면 갈라진다.
- codex 필요: True

### [P1·wrong] estimand-card-carries-retracted-line
- **어디**: `kb/templates/estimand_card.md:8`
- **근거**: CLAUDE.md:114-115 가 명시적으로 철회한다: "(⚠ 회신 N: \"일곱 번은 안 돌려도 됐다\" 는 철회 — 카드 블라인드 재생 시 확실히 잡는 것은 #7–8 정도다. 여덟 실패의 원인은 하나가 아니라 층위다.)" 그런데 CLAUDE.md:107 이 채우라고 지시하는 바로 그 템플릿 8행에 "> 일곱 번은 안 돌려도 됐다." 가 그대로 있다. 덤으로 같은 파일 1행 H1 이 "# estimand 카드" — 2026-09-01 용어 규율(CLAUDE.md:98, 사람이 읽는 표면은 '보고량')과 어긋난다(파일명은 기계 경로라 유지가 맞다). 그리고 이 파일은 2026-08-28 생성인데 frontmatter 가 없다.
- **고치는 법**: 8행을 회신 N 문구로 교체("카드가 확실히 잡는 것은 #7–8 정도다 — 여덟 실패의 원인은 하나가 아니라 층위다"). H1 을 '보고량 카드(estimand card)' 로, 파일명·`kind: "estimand"` 는 그대로. frontmatter 추가.
- codex 필요: False

### [P1·missing] codes-missing-review-letter-code
- **어디**: `kb/CODES.md:20-25 (한 줄 표)`
- **근거**: CODES.md 는 T·Q·J·M 넷만 정의하고 "⛔ **넷 다 '논문 1저자 질문' 이 아니다**" 로 닫는다. 그런데 이 repo 에서 제일 많이 인용되는 코드는 다섯 번째, **codex 회신 letter** 다: kb/reviews/ 110개 파일이 `codex_<A..BI>_<prompt|reply>_<slug>_<date>.md` 형식이고(codex_A_… → codex_BI_…), CLAUDE.md 본문이 이걸 8번 부른다 — "회신 N"(114), "회신 O"(127), "회신 M 마감보류"(137), decisions.json 은 "회신 AK"·"회신 AL"·"회신 P"·"회신 T" 까지 쓴다. CODES.md 에 없으니 새 세션은 '회신 N' 이 무엇의 N 인지, 어디 있는지 못 찾는다. 색인은 이미 있다 — `kb/reviews/INDEX.md`(자동 생성, `tools/kb_wiki.py reviews --write`) — 그런데 CLAUDE.md·CODES.md 어디서도 안 가리킨다. 게다가 `python3 tools/kb_wiki.py` 사용법 출력이 서브커맨드를 `lint | index | new | env` 로만 적어 `reviews` 를 숨긴다.
- **고치는 법**: CODES.md 에 §5 `R`/letter 절 추가: 알파벳은 리뷰 왕복 순서(A→Z→AA→…→BI), prompt/reply 짝, 정본 색인은 kb/reviews/INDEX.md, 인용은 '회신 N' 이 아니라 '회신 N(codex_N_estimand_discipline_2026_08_28)'. kb_wiki.py 도스트링에 `reviews` 서브커맨드 노출.
- codex 필요: False

### [P1·broken] research-agent-block-at-root
- **어디**: `CLAUDE.md:165-204`
- **근거**: 163행 `---` 아래 40줄이 research-agent/ 폴더의 지침인데 상대경로 그대로 루트에 붙어 있다. 루트에서 존재 확인한 결과 **10개 전부 없다**: config/research_profile.md · data/papers.sqlite · data/papers.jsonl · research_agent/vault.py · prompts/style_guide.md · SETUP_CLAUDE_CODE.md · VERSION · CHANGELOG.md · config/agent.yaml · data/analysis/pending (전부 research-agent/ 아래에 있다). 167행은 "이 폴더는 **논문 에이전트**다" 라고 선언하는데 이 폴더는 전고체전지 계산 캠페인 repo 다. 게다가 같은 파일 69행이 "'논문 에이전트' 요청 = litdb-curator 서브에이전트" 라고 **다르게** 정의한다 — 한 파일 안에서 같은 이름이 두 뜻이다(.claude/agents/ 에는 litdb-curator.md 와 paper-analyst.md 가 둘 다 있다).
- **고치는 법**: 165-204 를 CLAUDE.md 에서 떼어 `research-agent/CLAUDE.md` 로 옮긴다(Claude Code 는 하위 폴더 CLAUDE.md 를 그 폴더에서 읽는다). 루트에는 `research-agent/ 는 논문 자동비서다 — 규칙은 research-agent/CLAUDE.md` 한 줄만. 동시에 '논문 에이전트' 이름 충돌을 정리: litdb 큐레이션 = litdb-curator, 메일/큐 = research-agent.
- codex 필요: False

### [P1·duplicate] methods-canonical-invisible
- **어디**: `kb/methodology/computational_methods_canonical.md:143 (vs CLAUDE.md:16-18)`
- **근거**: 그 문서 143행이 CLAUDE.md 16-18행과 사실상 같은 문장이다: "**프로토콜 (고정):** Langevin NVT · dt 2 fs · friction 0.02 · equilib 5 ps + prod 200 ps · **MSD 창 2–50 ps** · Arrhenius **600/800/1000 K 3점** (400/500 K 제외) · **3-seed** · σ는 Nernst–Einstein(Haven=1)." 그런데 그쪽이 더 많다 — 헤더가 "② **MD 에 '상자 크기' 축 추가**(§6-1) — 같은 계에서 상자만 키워도 **D 가 1.65배** 움직인다. ③ **골격(비-Li) MSD 게이트** 신설(§6-2) … **b2o3 는 판정 보류.** ④ **UMA 검증 앵커 기록**(§6-3) — 힘 MAE 30.0 meV/Å" 를 싣고 스스로 "값을 인용하거나 새 계산을 걸기 전에 이 문서를 먼저 본다" 고 선언한다. CLAUDE.md 는 이 파일을 한 번도 안 가리킨다 — 짧고 낡은 사본만 읽히고 길고 정확한 원본은 안 읽힌다.
- **고치는 법**: CLAUDE.md MLIP-MD 줄 끝에 `→ 축 전체는 kb/methodology/computational_methods_canonical.md` 를 달고, 프로토콜 문장은 한쪽(그 문서)에만 두고 CLAUDE.md 는 '어기면 안 되는 것' 세 개(창·절대값 금지·3점)만 남긴다.
- codex 필요: False

### [P1·ia] kb-fairchem-unregistered
- **어디**: `kb/fairchem/ (md 11개) · tools/kb_wiki.py:28-32 · kb/SCHEMA.md:15-18`
- **근거**: tools/kb_wiki.py:28 `MANAGED = ["concepts","physics","methodology","results","reviews","reports","projects","questions","syntheses","platforms","descriptors","papers","literature_db","seminars"]`, :32 `SUMMARIZED = ["elements","templates"]` — `fairchem` 은 어느 쪽에도 없다. 결과: `grep -c fairchem kb/index.md` → **0**. lint 도 안 본다. SCHEMA.md:15-18 의 타입 목록에도 fairchem 이 없다. 11개 문서(00_site_map ~ 09_source_coverage, README)가 2026-08-25 에 들어왔고 전부 frontmatter 없이 색인 밖에 있다. 참고로 kb/elements/ 는 SUMMARIZED 인데 md 가 0개다(index 는 '118개' 라 적는다 — 세는 대상이 md 가 아니다).
- **고치는 법**: fairchem 을 MANAGED 에 넣고 SCHEMA 타입 목록에 추가(또는 db/knowledge/fairchem 번들 쪽으로 통합하고 kb 에서는 진입 문서 1장만 남긴다). kb/elements 의 '118개' 가 무엇을 세는지도 index 생성기에서 명시.
- codex 필요: False

### [P1·ia] schema-layer-map-incomplete
- **어디**: `kb/SCHEMA.md:9-13 (레이어 표) · webapp/fairchem.py:11-14`
- **근거**: SCHEMA 레이어 표는 db/ 17개 하위폴더 중 둘(properties, structures)만 이름을 대고, CLAUDE.md:120 이 "보고량·마감 판정은 **`db/governance/decisions.json` 에 등록**한다" 고 못박은 **판정 레이어가 표에 없다**(decisions 22건 · artifacts · assessments). 정작 제대로 된 역할 지도는 엉뚱한 데 묻혀 있다 — webapp/fairchem.py 도스트링: "· PDF·그림 해석 → `litdb`      · 사람용 설명 → `kb`  / · 우리 수치 정본 → `db/properties`   · 판정 → `db/governance`  / · 이 번들 → 위 entity 를 **FK 로 연결하는 검색/관계 DB**". 이 다섯 줄이 repo 전체 IA 의 정본인데 화면 모듈 주석에 있다.
- **고치는 법**: SCHEMA 레이어 표를 4행으로 확장 — 수치 정본(db/properties·structures) · **판정 원장(db/governance)** · 불변 원본(runs/) · 위키(kb·litdb·docs). webapp/fairchem.py 의 다섯 줄 역할 지도를 SCHEMA 로 승격하고 그쪽은 인용만.
- codex 필요: False

### [P1·missing] env-claims-tool-unlinked
- **어디**: `CLAUDE.md:30-57 (계산 자원 절)`
- **근거**: 오늘 kgy QE-GPU 를 세 번 틀렸고(CLAUDE.md:34-37 이 그 기록), 교훈은 사후에 박혔다. 그런데 **선제 도구가 이미 있다** — `python3 tools/kb_wiki.py env` 실행 결과: "환경 주장 후보 28건 · 아티팩트 18종 · 이미 정정됨 6건 · 검증 명령도 정정도 **없는** 것 19건", 그리고 `env --script` 로 서버에서 돌릴 검사 스크립트를 뽑아 준다. CLAUDE.md·SCHEMA.md·CODES.md 어디에도 `env` 가 없다. 같은 절의 두 번째 구멍: 기계 이름이 갈라져 있다 — CLAUDE.md 는 `gabia … root@121.78.116.27`, 셋업 문서는 `kb/methodology/kserver116_setup.md:3` "**Target host:** `121.78.116.27`" 로 **kserver116-27** 이라 부른다. 'gabia' 로 grep 하면 셋업 문서가 안 나오고 'kserver116' 으로 grep 하면 CLAUDE.md 가 안 나온다. 두 문서 다 서로를 안 가리킨다.
- **고치는 법**: 계산 자원 절 끝에 두 줄: ① 원격 작업 전 `python3 tools/kb_wiki.py env` 로 낡은 환경 주장 확인(19건이 미검증 상태) ② 기계별 셋업 정본 링크 — gabia(=kserver116-27) `kb/methodology/kserver116_setup.md`, 재기동 `kb/projects/restart_runbook_2026_09_07.md`. 셋업 문서 제목에 'gabia' 별칭을 넣어 양방향 grep 이 되게 한다.
- codex 필요: False

### [P1·missing] no-start-here-pointer
- **어디**: `CLAUDE.md 전체 · kb/open_items.md:6`
- **근거**: 세 파일 어디에도 '새 세션은 무엇부터 읽나' 가 없다. CLAUDE.md 가 kb/open_items.md 를 부르는 유일한 자리는 147행이고 내용은 "**통째로 읽지 말고 grep**" 뿐 — 그 파일이 원장이라는 말도, 무엇을 grep 하라는 말도 없다. 그리고 그 원장의 머리(6행)는 "## ⏭ 다음 세션이 **바로 이어서 할 것** (2026-08-28 등록 · **최종 갱신 2026-08-31**)" 이고 ⏭-0 이 "SDCP doped 재개 — 회신 R4 조건부 GO · ORCA 8잡 실행 중" 이다. 실제 살아 있는 작업은 그게 아니다 — git log 최근 10커밋은 LPSOCl 닫힘 조건 비준(5196c1081) · cascade 봉인(c221ac933) · Nd 어닐 6셀(83c868a97) · 결속 이주(12e6d0c9b) 다. 즉 '바로 이어서 할 것' 이 8일 낡았다.
- **고치는 법**: CLAUDE.md 맨 위에 6줄 `## 여기서 시작` 블록: 지금 상태 = `kb/open_items.md` ⏭ 절(+ 갱신일), 판정 = `db/governance/decisions.json`, 값 = `canonical_registry.json`, 금지 = `citation_hazards.json`, 리뷰 = `kb/reviews/INDEX.md`, 화면 = `webapp/`. 그리고 ⏭ 절 갱신을 세션 마감 관례로 규율에 넣는다(지금은 아무도 안 시킨다).
- codex 필요: False

### [P1·stale] readme-dead-front-door
- **어디**: `README.md:3 · README.md:47-88 · TIMELOG.md`
- **근거**: README.md:3 "**Last updated**: 2026-05-15" 이고 스스로를 "project bible" 이라 부른다. 47-88행 repo 구조 블록에 **tools/ · db/ · litdb/ · webapp/ · runs/ · docs/ · factory/ 가 하나도 없다** — 대신 "scripts/doping/ (구현 예정) · scripts/descriptors/ (구현 예정) · data/final_combo/" 를 싣는데 실제로 `scripts/descriptors` 와 `data/final_combo` 는 **없다**. 두 번째 항목으로 소개하는 TIMELOG.md 는 최신 절이 `## 2026-05-15`, 마지막 커밋 2026-06-11 로 3개월째 죽어 있다. '핵심 문서 빠른 링크' 표 6개는 전부 2026-05 시절 문서다(현행 정본인 canonical_registry·decisions·open_items 없음).
- **고치는 법**: README 를 15줄짜리 진입 문서로 축소: repo 가 무엇인지 3줄 + 지금 살아 있는 폴더 7개 한 줄씩 + `규율은 CLAUDE.md, 상태는 kb/open_items.md` . 2026-05 비전 블록(3-tier 아키텍처·Phase 1-3)은 `kb/projects/digital_twin_roadmap.md` 로 옮기고 날짜를 박는다. TIMELOG.md 는 archive/ 로 내리거나 '2026-06 이후 git log 가 로그다' 를 머리에 적는다.
- codex 필요: False

### [P2·stale] stale-counts
- **어디**: `CLAUDE.md:82,92,147 · kb/SCHEMA.md:22`
- **근거**: 실측 대조 — CLAUDE.md:82 "tools/ 에 py 305 · sh 106 · 62k줄" → 실제 **py 383 · sh 143 · 162,939줄**(2.6배). :92 "`kb_wiki.py lint` 은 레거시 49건을 한 줄로" → 실제 lint 출력 "레거시 깨진 경로 **20건**". :147 "`kb/index.md`(25 KB)·`kb/open_items.md`(72 KB)" → 실제 **51,583 B · 140,899 B**(둘 다 2배). SCHEMA.md:22 "**새 문서부터 필수. 기존 199개 소급 없음**" → frontmatter 없는 문서가 지금 **202개**이고 그중 **17개가 채택일(2026-08-11) 이후 생성**됐다(kb/fairchem 11 · kb/seminars cascade 대본 4 · kb/templates/estimand_card.md · seminar_script_5min_template.md). 즉 '기존' 이 아니라 새 문서가 규칙을 새고 있다.
- **고치는 법**: 숫자를 다시 재서 넣되, 다시 낡을 숫자는 아예 빼는 게 낫다 — '62k줄' 은 '수만 줄' 로, 파일 크기는 '통째로 읽지 말고 grep' 만 남긴다. SCHEMA:22 는 '기존 199개' 대신 '채택(2026-08-11) 이전 문서'로 바꾸고, 이후 생긴 무-frontmatter 17건은 lint 가 **error** 로 잡게 한다(지금은 안 잡힌다).
- codex 필요: False

### [P2·stale] section-header-date-stale
- **어디**: `CLAUDE.md:30`
- **근거**: `## 계산 자원 (2026-07 기준)` 인데 그 절 안에 2026-09-08 기록(34행 QE-GPU 3연속 오진)과 2026-09-01 결정(55행 회수 경로)이 들어 있다. 절 제목만 보고 '두 달 전 정보구나' 하고 건너뛰면 오늘 쓴 규칙을 놓친다.
- **고치는 법**: 헤더 날짜를 빼거나 `(최종 갱신 2026-09-08)` 로. 이 절은 항목별로 날짜가 이미 박혀 있어 헤더 날짜가 오히려 해롭다.
- codex 필요: False

### [P2·ia] schema-docs-jurisdiction-unenforced
- **어디**: `kb/SCHEMA.md:13 · tools/kb_wiki.py:28-32`
- **근거**: SCHEMA.md:13 은 `docs/` 를 "이 스키마의 관할" 로 선언한다. 실제로 kb_wiki.py 의 MANAGED/SUMMARIZED 는 `kb/` 하위만 돌고(all_pages() 는 `KB / d`), docs/ 는 lint 대상이 아니다 — docs/ 에 md 89개가 있는데 frontmatter 검사·경로 존재 검사·신선도 검사를 **0건** 받는다. litdb 도 INDEX 커버리지만 본다.
- **고치는 법**: 둘 중 하나 — ① SCHEMA:13 에서 docs/ 를 빼고 '슬라이드·산출물 보관소, 스키마 밖' 이라 명시, ② 또는 lint 에 docs/ 를 얹는다. 지금처럼 선언만 하고 강제 안 하는 상태가 제일 나쁘다(다 검사되는 줄 안다).
- codex 필요: False

### [P2·broken] schema-kanji-and-dangling-ref
- **어디**: `kb/SCHEMA.md:11 · kb/SCHEMA.md:51`
- **근거**: 11행 표 첫 칸이 `| **数値 정본** |` — 한자다. `grep -rn "수치 정본" kb/` 로는 이 줄이 안 나오고, `grep -rn "数値"` 는 repo 전체에서 이 한 줄만 잡는다(다른 문서는 전부 '수치'). 51행은 "(본문 보존 + 반증 근거 추가 — **오늘 §11 BVSE 철회**가 표준례)" 인데 SCHEMA 에 §11 이 없고, 같은 문구의 출처인 kb/methodology/llm_wiki_adoption_2026_08_11.md:45 도 "오늘 §11 BVSE 철회처럼" 이라 적을 뿐 §11 이 없다(그 문서 절은 '출처와 결정 방식/채택/번안/기각/씨앗 카드/운용' 6개). 2026-08-11 세션 대화 안의 번호를 문서에 남긴 것이라 지금은 아무도 못 찾는다.
- **고치는 법**: '数値'→'수치'. §11 참조는 실제 BVSE 철회 기록의 파일 경로로 교체하거나(찾아서), 못 찾으면 '(BVSE 철회 사례 — 원출처 미상, 2026-08-11 세션)' 으로 정직하게 표시.
- codex 필요: False

### [P2·wrong] decisions-ratification-not-uniform
- **어디**: `CLAUDE.md:120-121 · db/governance/decisions.json`
- **근거**: CLAUDE.md 는 "보고량·마감 판정은 **`db/governance/decisions.json` 에 등록**한다 (proposed → 사람이 ratify 해야 active)" 고 적는다. 실물 22건을 훑으면 최상위 `status` 필드가 아예 없는 항목이 10건(D-2026-08-20-source-authority · hash-bound-carry · no-fallback · defect-cell-metric · face-height-gate · no-retro-gate-without-artifact · missing-axis-is-unknown · estimand-before-compute · sdcp-doped-scope-closure · sdcp-neutral-ptfe-ddE 일부)이고, decisions.json 의 _rules 는 다른 이름을 쓴다 — "decision_state: proposed | active | superseded | retracted. ratification 없이 active 가 될 수 없다." 그리고 _status 가 스스로 적는다: "MVP vertical slice — **core 5 가** ratified/active 다 … 확대(entry 수리 7 · 재승인 3)는 slice 통과 뒤 별건이다." 즉 CLAUDE.md 는 22건 전부 비준 체계에 들어온 것처럼 읽히지만 실제로는 5건이 core 이고 7건이 수리 대기다.
- **고치는 법**: CLAUDE.md 120행에 필드명(`decision_state`)을 정확히 쓰고, '비준 체계는 core 5 로 시작해 확대 중 — 미비준 entry 가 남아 있다' 를 한 줄 붙인다. 또는 decisions.json 쪽에서 status 누락 10건을 채운다(이건 1저자 비준이 필요할 수 있다).
- codex 필요: False

### [P2·stale] codes-j-axis-outdated
- **어디**: `kb/CODES.md:65-66`
- **근거**: CODES.md:65 "`J-0` 출처표 · `J-1`–`J-6` 물성/방법 축 · **`J-7` = 방법 원전**(물성값이 없는 편 …)" 로 J-7 에서 끝난다. 실물 litdb/comparison_vs_ours.md:885 에 "### **J-8**. ★★★ CV 규약 판정 — **[Tu27ML] R²=0.99 vs 우리 cascade LODO −0.18** (2026-08-28 신설)" 이 있고 929행이 그 축을 인용한다("J-4 + J-8"). CODES.md 는 2026-08-26 이후 손대지 않았고 J-8 은 08-28 신설이다.
- **고치는 법**: CODES.md §3 에 J-8 한 줄 추가. 겸사겸사 J 축이 늘 때 CODES.md 를 같이 고치는 관례를 §3 에 한 줄로 박거나, comparison_vs_ours.md 에서 축 목록을 자동 추출하게 한다(중복 사전을 손으로 유지하는 게 여기 실패 지점이다).
- codex 필요: False
