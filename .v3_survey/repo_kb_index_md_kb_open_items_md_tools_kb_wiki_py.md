# repo — kb/index.md + kb/open_items.md + tools/kb_wiki.py

## 지금 무엇인가
kb 는 365개 관리문서(frontmatter 180 · 레거시 185) + 자동생성 카탈로그 `kb/index.md` + 1,483줄 원장 `kb/open_items.md` + 하네스 `tools/kb_wiki.py`(lint·index·new·env·reviews) 로 돼 있고, 지금 lint 는 0 errors / 45 warnings / 레거시 깨진 경로 20건이다. 내가 실제로 연 것: kb_wiki.py 737줄 전문 · SCHEMA.md 전문 · index.md(머리·전 섹션 헤더·projects/questions/syntheses/reviews 본문 + 재생성 대조 = 내용 완전 일치) · open_items.md 약 300줄(⏭ 블록 전체·판정대기 헤딩 전수·N·PDF/위시리스트·σ 규율·꼬리) · restart_runbook·MUST_READ·CODES.md·group_meeting 지침·reviews/INDEX.md·리뷰 프롬프트 4건 frontmatter·elements 표본 1건. **못 본 것: kb 문서 365개 중 340여 개의 본문, open_items 판정대기 786줄 중 약 660줄, litdb 219 digest, elements 118개 중 117개** — 이건 제목·frontmatter·grep 으로만 훑었다.

## 처음 오는 사람
처음 온 사람(또는 압축 뒤의 나)이 여기서 할 수 있는 건 `kb/index.md` 를 여는 것뿐인데, 그건 365줄짜리 알파벳순 목록이라 "지금 뭐가 살아 있나" 를 못 알려준다 — 날짜도 status 도 안 찍히고, 146줄에 똑같이 ○미열람이 붙어 있어 표시가 표시 구실을 못 한다. 그래서 자연스레 `kb/open_items.md` 로 가는데 맨 위 ⏭-0 이 "ORCA 8잡 실행 중" 이라고 말한다 — 9일 전 얘기고, 9월 7일 실측(restart_runbook)이 "프로세스 0개, gs0–gs3 는 시작도 안 했다" 로 뒤집은 상태다. 정작 오늘 상태를 아는 유일한 문서(`kb/projects/restart_runbook_2026_09_07.md`)는 index 자동목록 말고는 **아무 데서도 링크되지 않는다**. 결과적으로 막히는 지점은 셋이다 — (1) 어디부터 읽어야 하는지 알려주는 문서가 없다, (2) 원장 머리가 낡은 상태를 단언한다, (3) 9월 7~8일에 비준된 것들(LPSOCl 닫힘조건 · cascade 보고량 카드 · 봉인 v2)이 kb 안에서 검색으로 안 나온다.

## 건드리면 안 되는 것
- **kb/index.md 손편집 금지** — 지금 실물이 재생성본과 **완전 일치**한다(내가 메모리에서 다시 만들어 diff = IDENTICAL). 고칠 게 있으면 tools/kb_wiki.py 의 cmd_index 를 고친다. 손으로 한 줄만 고쳐도 다음 `index` 실행에 날아간다.
- **lint 0 errors 상태(문서 365개)** — 이건 지금 이 repo 에서 유일하게 초록불인 게이트다. 경고를 줄이는 리팩터를 하더라도 errors 는 0 을 유지한다.
- **review_chain() 의 3단계 짝짓기와 음성 selftest 12건** (tools/kb_wiki.py:483-598, 645-713) — `_taken` 으로 회신을 **소비**하는 로직(V_prompt 가 U 의 회신을 가로채 거짓 ERROR 를 낸 사고), 재사용 라벨(S·T·U·V·W·X)의 인용을 증거로 안 쓰는 규칙, AU←AV·AQ←AR 라벨 어긋남 처리 — 전부 실제 오판에서 나온 것이고 주석에 사건이 적혀 있다. '단순화' 하면 그 사고가 그대로 돌아온다.
- **cmd_env 의 CORRECTED_RE 4줄 창 + '멀리 있는 정정은 안 세어 준다' 음성 시험** (tools/kb_wiki.py:338-341, 452-457) — 도구가 늑대소년이 되는 걸 막는 장치다. 창을 넓히거나 '아무 ⛔ 나 있으면 통과' 로 바꾸면 안 된다.
- **open_items 의 철회·정정 원문 전부** — ⏭-1 의 `⛔ **β=0.8 하드게이트는 2026-08-26/27 폐기됐다** ... ⚠ **양방향이다** — 문턱을 내리면 '다 통과' 가 아니라 **통과했던 것도 무효**다`, ⏭-3 의 취소선 처리, item N 의 `**오류를 정정하면서 같은 종류의 오류를 반복했다.**`, 회신 AL 의 P0 목록. SCHEMA Update Policy 상 덮어쓰기 금지 — 재배치는 되지만 삭제는 안 된다.
- **⏭-3 「사전등록 채점 — 기준을 고치지 말 것」 전체 블록** (kb/open_items.md:132-142) — `⛔⛔ **측정 뒤에 기준을 고치면 이 기록의 의미가 통째로 사라진다.**` 이건 정리 대상이 아니라 정리하면서 지켜야 할 규율 자체다.
- **kb/reviews/ 의 회신 원문 파일 28개** — CLAUDE.md 용어 규율이 `회신 원문을 고쳐 쓰면 이력이 깨진다` 라고 못 박았다. authoredBy 를 external 로 고치는 것은 frontmatter 뿐이고, 본문·제목·파일명은 손대지 않는다.
- **open_items:1371-1389 「σ 절대값 규율 — 근거 재정의」** — 원장 안의 σ 수치(Adeli 9.4 mS/cm · Kim 10.2 · optB88 2.3)는 전부 문헌 출처가 붙어 있어 '우리 MD σ 절대값 인용 금지' 규율 위반이 아니다. 규율 위반으로 오인해 지우면 규율의 **근거**가 사라진다.
- **kb/CODES.md** — `Q1–Q10 이 서로 다른 문서 4곳에서 각각 다른 뜻으로 쓰이고 있었다` 를 푸는 유일한 문서이고 webapp 두 곳이 참조한다. 인덱스에 안 보인다고 지우면 안 된다 — 보이게 만드는 게 답이다.
- **kb/projects/restart_runbook_2026_09_07.md** — 지금 이 repo 에서 '무엇이 어디서 돌고 있나' 를 실측으로 아는 유일한 문서다. 낡았다고 지우지 말고, 최신본으로 계속 이어 쓰는 계보로 만든다.
- **`<!-- lint-skip-path -->` 관례** (SCHEMA.md:76-78) — 존재하지 않는 경로를 일부러 기록하는 정당한 경우가 있다(리뷰어 오인용 정정, 서버 전용 스크립트). 깨진 경로 20건을 정리할 때 이 장치를 없애지 말고 **쓰라고 만든 곳에 쓴다**.

## 발견

### [P0·wrong] ledger-head-contradicts-runbook
- **어디**: `kb/open_items.md:10,30 ↔ kb/projects/restart_runbook_2026_09_07.md:48,50,160-162`
- **근거**: 원장 맨 위: `### ⏭-0. SDCP doped 재개 — **회신 R4 조건부 GO · ORCA 8잡 실행 중**` / `- ▶ **ORCA 8잡 실행 중** (2026-08-31 실측: gs0·gs1 완료 · gs2 진행)` + 같은 줄에 `⚠ 실행 기계 표기가 문서마다 다르다(데스크탑 WSL vs gabia CPU) — 확인 필요.` 반면 9월 7일 실측: `| desktop | **Stage A** ORCA (gs0–gs7) | **이미 멈춰 있었다** (프로세스 0개) | 없음 |`, `⚠ 재부팅 전에도 **Stage A 는 안 돌고 있었다.**`, `⇒ 이번 캠페인에서 실제로 돌린 것은 **gs4·gs5 둘**이다. ... `gs0–gs3·gs6·gs7` 은 **아직 시작도 안 했다.**` — 런북이 원장의 '확인 필요' 를 실제로 확인해 줬는데 그 답이 원장으로 안 돌아왔다. webapp/app.py:517·525 가 이 파일을 화면에 그대로 띄운다.
- **고치는 법**: ⏭-0 제목·30줄의 '실행 중' 을 지우고 09-07 실측(gs4 수렴 · gs5 cyc0 사망 · 나머지 6개 미착수)으로 교체, 런북 경로를 인용. gs0·gs1 '완료' 가 어느 폴더 얘기였는지는 데스크탑에서 한 번 재확인해야 확정된다 — 확정 전에는 '미확인' 으로 적는다(0 으로 적지 말 것).
- codex 필요: False

### [P0·stale] ledger-blind-to-0907-0908
- **어디**: `kb/open_items.md:6 (섹션 머리) · :75 (⏭-2)`
- **근거**: 섹션 머리가 `## ⏭ 다음 세션이 **바로 이어서 할 것** (2026-08-28 등록 · **최종 갱신 2026-08-31**)` 이고, 파일 안에서 가장 최근 날짜는 2026-09-02 다(`git log -1 -- kb/open_items.md` = 2026-09-05 4d0b49f76). 그 뒤 커밋 25건이 원장에 없다: `5196c1081 LPSOCl 3×3×1 닫힘 조건 — 1저자 비준 (proposed → active)` · `cc7096eda/22b00e909 cascade 보고량 카드 비준` · `c221ac933 cascade #7 — 실제 봉인 (v2_2026_09_08)` · `83c868a97 Nd2O3-LPSCl1.6 어닐 6셀 회수` · `12e6d0c9b BG ②: 결속 이주 완료` · `5769e2328 런타임은 추측하지 않는다 — ldd`. 특히 ⏭-2 제목이 아직 `해제조건 8건 중 ②(anneal seed 고정)만 이행(34a400e9), 나머지 7건 미이행` 인데, 09-08 에 #1·#2b·#5·#6 이 비준되고 Step 1·2 가 구현(8c9338c96·46566ca64)되고 #7 이 봉인됐다.
- **고치는 법**: ⏭-2 를 09-08 카드 기준으로 다시 쓰고(남은 건 #3 전 시드 재실행·#4 v2 동결·#8 sentinel), ⏭ 블록 머리 날짜를 갱신. 그리고 '원장 갱신' 을 캠페인 커밋의 마무리 단계로 붙인다 — 지금은 db/governance 와 kb/reviews 는 갱신되는데 원장만 뒤처진다.
- codex 필요: False

### [P0·missing] estimand-card-invisible-from-kb
- **어디**: `db/properties/cascade_d_rel_estimand_2026_09_08.json (kb 에서 인용 0건)`
- **근거**: `grep -rln cascade_d_rel_estimand` 결과가 `tools/doping/axis_corr_csv.py` · `tools/cascade/build_cascade_audit_manifest.py` · `webapp/data.py` · `db/governance/decisions.json` · `db/properties/cascade_seal_v2_2026_09_08.json` 뿐 — **kb/ 문서 0건**. 비교하면 LPSOCl 쪽 `lpsocl_box331_closure_conditions_2026_09_07.json` 은 kb 3곳(restart_runbook · codex_BG_prompt · concepts/msd_reading.md)에서 인용된다. CLAUDE.md 코드규율의 `규약 대조 30초: grep -rl "<양이름>" kb/` 가 cascade 보고량에는 아무것도 못 찾는다.
- **고치는 법**: `kb/methodology/` 에 cascade D_rel 보고량 카드 해설 한 장(무엇을 재나 · 허용/금지 서술 · 남은 해제조건 #3·#4·#8 · 무효 조건 5개) — 숫자는 복사하지 말고 json 경로 인용으로. 같은 점검을 LPSOCl·Nd 어닐에도 한 번씩 돌린다.
- codex 필요: False

### [P1·wrong] must-read-points-wrong-way
- **어디**: `kb/projects/MUST_READ_digital_twin_north_star.md:1,9-12`
- **근거**: `# 🚨🚨🚨 MUST READ` / `> **새 session / 압축 후 첫 5분 안에 무조건 읽기**.` / `> 이 문서를 안 읽으면 Claude가 **반드시 Nd2O3 paper narrative로 drift함** — 그 drift는 본 프로젝트의 진짜 목적이 아니다.` / `> 마지막 갱신: 2026-05-18`. 그런데 `kb/seminars/group_meeting_2026_09_03_nd_professor_directives.md` 는 `title: "★ 지침 — 2026-09-03 그룹미팅 교수님 코멘트 (Nd/O 공치환 논문 방향)"` 이고 본문에 `**이 문서의 지위**: 앞으로 Nd 논문·연구세미나·원고를 쓸 때의 **1차 지침**.` 이라고 적혀 있다. 즉 4개월 전 문서가 '금지된 drift' 라고 부른 것이 지금의 1차 지침이다.
- **고치는 법**: MUST_READ 상단에 09-03 지침 링크와 함께 '이 문서의 Nd drift 경고는 2026-09-03 지침으로 대체됐다' 를 박거나(원문 보존 규율상 삭제 말고 병기), 아예 north-star 역할을 restart_runbook + 09-03 지침으로 넘기고 이 파일은 history 로 강등. 🚨🚨🚨 는 지금 가장 낡은 문서에 붙어 있다.
- codex 필요: False

### [P1·wrong] drel-gate-090-head-stale
- **어디**: `kb/open_items.md:82-83 (같은 항목 :117 과 충돌)`
- **근거**: 항목 머리: `⚠ 조건 셋: 전 설계가 **같은 창(2–50 ps)** · **같은 셀(2×2×2)** · **두 창 병기 보고**.` / `축은 `D_rel_vs_host`(host 대비 비), 게이트 **0.90** (Deng 2026 의 σ 손실 7 % 허용 / 31 % 실패 사이).` 같은 항목 아래 :117 에는 `⇒ 보고량을 **600 K 조건부 tracer D_rel** 로 한정하고 300 K σ·0.90 게이트는 **제거**.` 09-08 카드 커밋도 `#6 보고량 = D_rel(600 K · 2–50 ps · cell-conditioned). 300 K σ·Deng 0.90·2온도 외삽 삭제.` 로 못 박았다. 위만 읽으면 폐기된 게이트를 그대로 쓰게 된다 — ⏭-3 이 :137 에서 `⚠ ⏭-2 에는 반영돼 있었는데 여기만 남아 같은 파일 안에서 충돌했다` 라고 같은 유형을 이미 자백했다.
- **고치는 법**: 82-83 줄에 취소선 + 폐기 근거(회신 AL P0-5 · 09-08 카드 #6) 병기. 규칙: **항목 머리는 최신 판정만, 폐기 처방은 아래로 접는다** — 지금은 반대로 돼 있다.
- codex 필요: False

### [P1·stale] reviews-index-stale-no-gate
- **어디**: `kb/reviews/INDEX.md (생성 2026-09-03) · tools/kb_wiki.py:174-182`
- **근거**: INDEX frontmatter `date: 2026-09-03` · `verifiedBy: tools/kb_wiki.py reviews --write`, `grep -n "BG_prompt|BH_prompt|BI_prompt" kb/reviews/INDEX.md` = 0건인데 실물엔 `codex_BG_prompt_webapp_aw_release_2026_09_07.md` · `codex_BH_prompt_md_axis_audit_2026_09_07.md` · `codex_BI_prompt_webapp_claim_binding_2026_09_08.md` 가 있다. 게다가 INDEX 의 모순 목록은 5건(AY·AZ·BB·BC·BF)인데 오늘 lint 는 3건(AZ·BC·BF)이라 두 화면이 서로 다른 말을 한다. lint 는 `kb/index.md` 만 `managed-files: (\d+)` 로 신선도를 보고 reviews/INDEX.md 는 **아무도 안 본다**.
- **고치는 법**: lint 에 reviews/INDEX.md 신선도 검사 한 줄 추가(파일 수 또는 프롬프트 목록 해시 비교), 또는 lint 가 돌 때 reviews --write 를 같이 돌린다. 자동생성물이 손으로 갱신을 기다리는 구조는 반드시 썩는다.
- codex 필요: False

### [P1·ia] closed-section-is-a-stub
- **어디**: `kb/open_items.md:3,1481-1483`
- **근거**: 머리말 규칙: `> 세션이 바뀌어도 유지되는 미결 사항 추적. 닫을 때 날짜+근거를 남기고 ✅로 옮긴다.` 그런데 도착지는 `## ✅ 닫힌 항목` + `- (여기로 이동)` 두 줄뿐이다. 실제로는 닫힌 항목 8개가 본문에 그대로 산다 — `### 3. ~~VGCF 2×2 barrier 행렬~~ → ✅ **완료 (2026-07-30)**` · `### 6. ~~LPSOCl COHP 곡선 원자료 회수~~ → ✅ **완료**` · `### 7. ~~litdb 인덱스 정합~~ → ✅ **닫음**` · `### 10. ~~ELF·그림 계 표시명~~ → ✅ **닫음**` · `### O. ✅ Nd 갭` · `### R. ✅ litdb 인덱스 미편입 5편` · `### ~~M6~~. ✅ cascade 양극 반응성 게이트` · `### ⏭-1. T13 확인 — ✅ **판정 완료**`. '판정 대기' 786줄 = 파일의 53%.
- **고치는 법**: 닫힌 8건을 실제로 ✅ 섹션(또는 `kb/results/` 카드)으로 옮기고 본문엔 한 줄 요약 + 링크만 남긴다. 판정·근거 원문은 **지우지 말고 이동**(SCHEMA 철회 원문 보존). 이것만으로 원장이 눈에 띄게 얇아진다.
- codex 필요: False

### [P1·ia] ledger-rq-cards-disconnected
- **어디**: `kb/open_items.md ↔ kb/questions/ (11장)`
- **근거**: SCHEMA.md:66 `⚠ `kb/open_items.md` 는 **원장(ledger)** 으로 유지 — 큰 항목이 카드로 승격되면 상호 링크.` 실측: 원장 → 카드 인용 **2건**(:191 esw_reduction_limit · :895 sdcp_site_preference), 카드 → 원장 인용 **11장 중 1장**(lpsocl_low_beta_mechanism.md). sdcp_doped_estimand·sdcp_doped_reopen_v2/v3 는 원장 ⏭-0 과 같은 얘기를 하는데 서로를 안 가리킨다.
- **고치는 법**: 카드로 승격된 항목은 원장에서 본문을 지우고 **한 줄 + 카드 경로**로 축약, 카드 frontmatter 에 `feedsInto:` 대신(또는 함께) 원장 앵커를 적는다. lint 에 'questions 카드는 open_items 를 인용한다' 검사를 넣으면 자동으로 지켜진다.
- codex 필요: False

### [P1·useless] warnings-are-noise
- **어디**: `tools/kb_wiki.py:130-131,61,137-139`
- **근거**: warnings 45건의 구성: `authoredBy agent 인데 effort 없음` **20건**, 오래된 status **17건**, single-source+high **4건**, 리뷰사슬 모순 **3건**, litdb INDEX **1건**. `effort` 는 `grep -rn effort tools/*.py webapp/*.py` 결과 kb_wiki.py 자기 자신 말고 **아무도 안 읽는다** — 경고를 위해서만 존재하는 필드다. status 검사도 오탐이 섞인다: `kb/methodology/li3nd_metal_protocol_note_2026_08_11.md` 의 `status: 종결 — 코드 반영 + PP 확보 + 금속 실측 완료, NEB 파일럿 진행 (§7)` 이 `STALE_STATUS = re.compile(r"대기|HOLD|진행|보류|pending")` 의 '진행' 에 걸려 '28일 방치' 로 나온다(문장은 '종결' 로 시작한다). 정작 진짜 신호 3건(회신 파일이 있는데 status 가 발송 대기 — BF)이 45줄 속에 묻힌다.
- **고치는 법**: ① effort 경고를 없애거나(필드 폐기가 정직하다) `--pedantic` 뒤로 숨긴다. ② STALE_STATUS 를 status **머리 토큰**으로 판정(종결/완료/마감으로 시작하면 통과). ③ 리뷰사슬 모순은 WARNINGS 가 아니라 별도 🔴 블록으로 맨 위에 올린다. 목표는 CLAUDE.md 의 선례와 같다 — 매번 찍히는 목록은 플래그 뒤로.
- codex 필요: False

### [P1·useless] explored-marker-dead
- **어디**: `tools/kb_wiki.py:243-244 · kb/index.md (146줄)`
- **근거**: `grep -rh '^explored:' kb/*/*.md | sort | uniq -c` → `146 explored: false` / `1 explored: true`. 그래서 index 의 `○미열람` 이 목록 146줄에 붙는다(전체 표시 문서의 99%). 같은 생성기의 `⛔철회` 는 `verificationStatus: retracted` 가 실물에 **0건**이라 한 번도 안 찍힌다 — 철회 사례(doped v1 · local-TF · 1.33× σ)는 repo 에 여럿인데 frontmatter 로는 하나도 안 잡힌다.
- **고치는 법**: ○미열람은 기본 숨기고 `explored: true` 인 것에 ✔ 를 붙이는 쪽으로 뒤집는다(적은 쪽이 신호다). 그리고 철회 문서에 `verificationStatus: retracted` 를 실제로 달아 ⛔철회 마크를 살린다 — 지금 그 마크는 죽은 코드다.
- codex 필요: False

### [P1·buried] runbook-buried
- **어디**: `kb/projects/restart_runbook_2026_09_07.md (피인용 0) · kb/index.md:5`
- **근거**: `grep -rln restart_runbook_2026_09_07` → `./kb/index.md` 하나(그것도 자동생성 목록 줄). index 머리 안내는 `규칙: kb/SCHEMA.md · 열린 질문: kb/questions/ · 논지 카드: kb/syntheses/ · 원장: kb/open_items.md · 문헌: litdb/INDEX.md` 로 런북을 안 가리킨다. 정작 이 문서에는 두 기계에서 무엇이 어디서 어떤 명령으로 도는지, clone 이 둘이라 상대경로가 갈린다는 것(`⚠ **desktop 에 repo clone 이 둘 있다**`), gabia 감시가 8.7일간 가짜 경보를 찍었다는 것까지 실측으로 들어 있다.
- **고치는 법**: index 머리 줄에 '지금 무엇이 도는가: kb/projects/restart_runbook_<최신>.md' 를 추가하고, 런북 계열은 이름을 `runbook_ops_<날짜>.md` 로 통일해 최신본이 자동으로 앞에 오게 한다. kb/projects/ 24개 알파벳 목록 안에 두면 못 찾는다.
- codex 필요: False

### [P2·ia] index-has-no-time-axis
- **어디**: `tools/kb_wiki.py:218-258 (cmd_index)`
- **근거**: 생성기가 찍는 건 `- `kb/<dir>/<file>` — <title><mark>` 뿐이다. frontmatter 에 `updated:` 가 있는데 안 쓴다. 그래서 365줄 목록에 날짜도 status 도 없고 정렬은 `sorted(dd.glob("*.md"))` = 파일명 알파벳순이다. 기억을 되찾는 쪽에서 제일 필요한 컷('최근 2주에 뭐가 바뀌었나')이 없다.
- **고치는 법**: 생성기 맨 위에 `## 최근 갱신 (updated 기준 상위 20)` 블록을 추가하고 각 줄에 `updated` 와 `status` 를 붙인다. 디렉터리별 전체 목록은 그 아래로. 손편집 금지 규율은 그대로 두고 **생성기만** 고친다.
- codex 필요: False

### [P2·broken] legacy-broken-paths-20
- **어디**: `tools/kb_wiki.py lint --legacy 출력 20건`
- **근거**: 성격이 셋으로 갈린다. (a) **처음부터 없던 계획 파일 8건** — `kb/papers/si_figures_plan.md` 의 `tools/plot_wad_stats.py`·`tools/plot_ncm_convergence.py`·`tools/plot_method_comparison.py`·`tools/analyze_halogen_bonds.py`·`tools/li_layer_partition.py`·`tools/br_swap_test.py` 와 `kb/projects/sdcp_master_v2_2026_07_11.md` 의 `docs/sdcp_master.md`·`docs/sdcp_manuscript_anchors.md`: `find tools -name '*plot_wad_stats*'` 0건 + `git log --diff-filter=D --all` 0건 = 만든 적 없음. (b) **잘린 경로 1건** — `kb/seminars/seminar_redirect_2026_08_11.md` 의 `litdb/figures/duquesnoy2023_.../fig_6.png`, 실제 폴더는 `litdb/figures/duquesnoy2023_ml_multiobjective_manufacturing_optimization/`. (c) **한때 있다가 지워진 것** — `docs/figures/oxidation/interface_decomp_b2o3_vs_undoped.png` 는 커밋 `acfc3fbc8`·`62ae8d826` 에 존재한다.
- **고치는 법**: (a)는 SCHEMA 가 정한 대로 그 줄에 `<!-- lint-skip-path -->` + '미생성' 표기(또는 계획 자체를 폐기 표시). (b)는 실제 폴더명으로 고친다 — 이건 그냥 오타다. (c)는 삭제 커밋 해시를 병기. 소급 수정을 '안 한다' 가 아니라 **분류하고 20건을 0으로 만든 뒤 규칙을 error 로 올린다**.
- codex 필요: False

### [P2·ia] kb-root-docs-unlinted-unindexed
- **어디**: `kb/SCHEMA.md · kb/CODES.md · tools/kb_wiki.py:28-32,77-83`
- **근거**: `MANAGED` 는 하위 디렉터리 14개뿐이고 `all_pages()` 가 `KB/<d>/*.md` 만 모은다 → kb 루트의 SCHEMA.md·CODES.md 는 **lint 도 index 도 안 탄다**. CODES.md frontmatter 는 `type: methodology` · `created: 2026-08-26` 로 스키마 밖 키를 쓰고 `date:` 가 아예 없다(REQ_KEYS 위반인데 검사 대상이 아니라 안 걸린다). CODES.md 를 인용하는 건 `webapp/data.py:4271` 과 `webapp/app.py:650` 뿐 — kb 안에서는 아무도 안 가리킨다. 내용은 `**`Q1`–`Q10` 이 서로 다른 문서 4곳에서 각각 다른 뜻으로 쓰이고 있었다.**` 를 푸는 유일한 문서다.
- **고치는 법**: kb 루트 md 를 lint 대상에 넣고(REQ_KEYS 만이라도), index 머리 안내 줄에 `코드 체계: kb/CODES.md` 를 추가. 규칙 원본이 검사 밖에 있는 게 제일 이상한 배치다.
- codex 필요: False

### [P2·wrong] authoredby-external-unused
- **어디**: `kb/reviews/*reply*.md (28건) · kb/SCHEMA.md:38-40`
- **근거**: SCHEMA: `authoredBy: agent | human | external      # external = 바깥 리뷰어가 쓴 **회신 원문**` + `그 구분이 이 캠페인에서 제일 비싼 정보다`. 실측: reply 파일 28개 중 `external` 은 **2개**(codex_AW_reply_webapp_audit_2026_09_01 · codex_U_reply_polaron_S0_2026_09_01), `agent` 7개(예: codex_AT_reply_c12_v17_2026_08_31), `human` 6개, 나머지는 필드 없음. 리뷰어가 쓴 글이 우리 에이전트 작성으로 표시돼 있다 — 그리고 그 오표기가 다시 'agent 인데 effort 없음' 경고를 만든다.
- **고치는 법**: reply 파일 일괄로 `authoredBy: external` 로 정정(본문은 절대 손대지 않는다 — 회신 원문 보존 규율). lint 에 '파일명에 _reply 가 있으면 authoredBy 는 external 이어야 한다' 검사 추가하면 재발이 막힌다.
- codex 필요: False

### [P2·duplicate] literature-wishlists-in-ledger
- **어디**: `kb/open_items.md:1093-1119 · :1390-1425`
- **근거**: `## 📄 PDF 확보 대기` 27줄 + `### 이상욱 랩 논문 확보 위시리스트` + `### 스크리닝 방법론 논문 위시리스트` 가 원장 안에 있는데, 행 대부분이 이미 닫혀 있다: `| ~~1~~ | ✅ **확보·다이제스트 완료 (2026-07-28)** de Klerk et al.` · `| ~~10~~ ✅ | **Park 2024 SevenNet** ... **확보·정독 완료 2026-08-26** (`litdb/papers/park2024_sevennet_parallel_gnn_md.md`)`. CLAUDE.md·SCHEMA 는 `문헌은 litdb/ 가 정본 (digest + INDEX.md + comparison_vs_ours.md)` 라고 정해 뒀다. 같은 lint 가 `litdb INDEX*.md 어디에도 없는 digest 8개` 도 경고한다 — 문헌 추적이 두 곳에 갈려 있다는 증거다.
- **고치는 법**: 확보 완료 행은 litdb 경로만 남기고 원장에서 삭제, 미확보 위시리스트는 `litdb/WISHLIST.md`(또는 INDEX 의 한 절)로 이관하고 원장엔 한 줄 링크. 원장은 '우리가 계산으로 결판낼 것' 만 남긴다.
- codex 필요: False

### [P2·broken] index-freshness-count-only
- **어디**: `tools/kb_wiki.py:179-182`
- **근거**: `m = re.search(r"managed-files: (\d+)", idx.read_text())` 로 **개수만** 비교한다. 파일 1개 삭제 + 1개 추가, 또는 title 변경·frontmatter 마크 변경은 개수가 그대로라 lint 가 0 errors 로 통과한다. (오늘은 다행히 실제로 신선하다 — 내가 index 를 메모리에서 재생성해 대조했더니 완전 일치였다.)
- **고치는 법**: 생성 내용의 sha256 을 index 머리에 같이 찍고 lint 가 그걸 비교한다. 한 줄짜리 수정이고 '자동생성물이 조용히 낡는' 유형을 통째로 막는다.
- codex 필요: False

### [P2·stale] item-N-progress-claim-unbacked
- **어디**: `kb/open_items.md:725 · db/properties/canonical_registry.json (modelc gap 항목 provenance_open)`
- **근거**: 원장: `· **modelc ⏳ 진행 중** — 2026-08-31 16:51 nscf 재시작 (`--mca btl self,vader`, np 10 -nk 10).` 8일 전 얘기고, 09-07 프로세스 전수 조사(restart_runbook §1 표)에 이 잡이 없다. 레지스트리의 같은 필드는 한 문단 안에서 `⏳ modelc 는 재계산 진행 중.` 과 `⇒ KISTI 원본이 없으므로 이 2건은 **영구 미해소로 본다.**` 를 동시에 말한다.
- **고치는 법**: modelc nscf 가 끝났는지/죽었는지 한 번 확인해 '완료' 또는 '중단' 으로 확정하고, 레지스트리 문구도 둘 중 하나로 통일. 확인 못 하면 '2026-08-31 이후 상태 미확인' 이라고 쓴다 — '진행 중' 은 근거 없는 현재형이다.
- codex 필요: False

### [P2·ia] ledger-numbering-scrambled
- **어디**: `kb/open_items.md:307-1092 (판정 대기 헤딩)`
- **근거**: 헤딩 순서가 `1, 2, 3, 4, 5, 6, 6b, 7, 10, 8, 9, 11, 12, 13, 14, N, O, P, Q, R` — 10 이 8·9 앞에 있고, 숫자 체계와 알파벳 체계가 섞여 있다(N·O·P·Q·R 은 2026-08-07 이후 신설분). 신설 순서도 뒤죽박죽이라 '최신이 앞' 규칙이 없다.
- **고치는 법**: 번호를 다시 매기지 말고(인용이 깨진다) **상태별로 재배치**한다: 🔴 살아 있는 것 → 🟡 조건 대기 → ✅ 닫힘(접기). 각 헤딩에 마지막 갱신일을 붙이고 그 날짜 역순으로 정렬하면 번호 체계를 안 건드리고도 최신이 앞에 온다.
- codex 필요: False

### [P2·useless] elements-118-encyclopedia
- **어디**: `kb/elements/ (118 json)`
- **근거**: `kb/elements/Ac.json` 의 role 필드: `"방사성 악티나이드(배터리 무관, 백과사전 완성용). ... SSB·전지와는 무관."` 118개 전부 원소 백과 항목이고 마지막 커밋은 2026-07-27(`MAX 감사`). kb 문서에서 `kb/elements` 를 인용하는 건 4건뿐이다. index 는 개수만 찍어서(`## elements/ — 118개`) 화면을 막진 않지만, 관리 대상 문서 수가 실제보다 커 보이게 한다.
- **고치는 법**: 지우지는 말고(도판트 스크리닝에서 참조된다) `db/` 쪽 데이터로 옮기거나 kb/elements/README 한 장에 '전지 무관 원소 N개 포함, 소비처는 X' 를 적는다. v3 재편에서 '해석 위키' 와 '참조 데이터' 를 가르는 기준선으로 쓰기 좋은 사례다.
- codex 필요: False
