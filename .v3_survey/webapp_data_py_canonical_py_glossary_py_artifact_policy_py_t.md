# webapp — 배관 (data.py · canonical.py · glossary.py · artifact_policy.py · tests/)

## 지금 무엇인가
화면 뒤의 데이터 층이다. canonical.py 가 db/properties/canonical_registry.json + governance 원장을 읽어 정본값·게이트·claim 결속을 판정하고, data.py(6238줄)가 그 위에 db/kb/litdb 로더 100여 개와 대시보드 카드 산문을 얹고, glossary.py 는 용어 250줄을 파이썬 리터럴로 들고 있고, artifact_policy.py 는 cascade 산출물 노출을 fail-closed 로 막는다. tests/test_webapp.py(3145줄·134 test)가 실제로 터졌던 회귀를 음성시험까지 붙여 굳혀 놨고, 전체 178 passed / 2 skipped 가 20초에 돈다.

## 처음 오는 사람
배관 쪽에서 보면 처음 온 사람은 세 군데서 막힌다. ① **길 안내가 없다** — 무인자 GET 라우트가 28개인데 `search_index()`(data.py:3344)에 등록된 페이지는 15개뿐이고, 사이드바에 버젓이 있는 `/governance`·`/ledger`·`/requests`·`/sdcp`·`/seminar`·`/fairchem` 여섯은 검색으로 못 찾는다. 하필 09-07~08 작업(LPSOCl 마감 비준·cascade 보고량 카드·결정 원장)이 전부 `/governance` 에 있는데 그게 안 잡힌다. ② **첫 화면이 실험노트다** — `dashboard_highlights()` 가 카드 41장을 내는데 2026-08-27 하루치 NEB 디버깅만 11장(27%)이다. 신규 방문자가 "이 랩이 뭘 알아냈나"를 묻는데 화면은 "우리가 어제 뭘 틀렸나"로 답한다. 최신 3장은 db 구동이라 신선하지만 나머지 38장은 하드코딩 산문이고, 그중 둘(data.py:4373·4540)은 8월 28일자 카드인데 본문이 "오늘만 세 번째", "오늘 새 발견으로 적었다"로 시작한다 — 9월 8일에 읽으면 그냥 거짓말이다. ③ **조성 페이지가 파일 서랍이다** — `/composition/sdcp` 는 N/A 칸 4 · TODO 칸 5 · 구조파일 이름 95개를 한 페이지에 전부 찍는다(li3n 60 · vgcf_hbn 64도 같다). 반대로 `/composition/comp3`~`comp5` 는 데이터파일 0건에 TODO 20칸이라 열어 볼 이유가 없는 페이지가 셋 있다. 정작 "무엇부터 보면 되나"를 말해 주는 라우트는 `/health`(JSON 두 줄) 말고 없고, 코드·템플릿 어디에도 온보딩 문구가 없다.

## 건드리면 안 되는 것
- **canonical.py 의 신선도 계약** — `_mtime_key()` 가 레지스트리뿐 아니라 **source_path 원자료 19개까지** 캐시 키에 넣는 것, 그리고 `CANONICAL` 이 `_LazyMap` 인 것. 성능 findings 에서 손대고 싶어지는 자리인데, `test_running_process_sees_source_change`(tests/test_webapp.py:634)가 `srcs <= keyed` 와 `type(D.CANONICAL).__name__ == "_LazyMap"` 을 명시적으로 요구한다. 첫 판이 import 때 스냅샷을 떠서 재시작 전엔 db 수정이 화면에 안 나왔던 회귀의 수리다. 캐시를 세게 걸더라도 '오래 사는 worker 가 다음 요청에서 db 변경을 본다' 는 성질은 반드시 유지.
- **`_read_ledger()`(data.py:944)와 그것을 쓰는 세 자리** — '못 읽었다'와 '세어 봤더니 0'을 가르는 유일한 장치다. 반환 타입이 `(dict, 사유)` 라 불편해 보여도 그게 계약이다. sei_axes 의 3상태 처리(data.py:1380-1383: `⛔ 원장 못 읽음` / `⛔ 철회 — 재계산 중` / `완료|진행 중`)와 detail 문구("이 칸이 비어 보이는 것은 '아직 계산 안 함' 이 아니라 '판정 불가' 다")도 그대로 둔다 — CLAUDE.md 의 '없는 것을 0 으로 표시하지 않는다' 가 화면에서 실제로 살아 있는 몇 안 되는 자리다.
- **대시보드 카드의 철회·오진 기록 전부** — 특히 `md_ea_ranking` 카드(data.py:3985 부근)의 '순위 보류' 로직. b2o3 가 게이트 미평가로 빠지자 남은 하나를 '최저'라고 쓰던 자기모순을 막으려고 `held` 를 세어 순위 주장 자체를 차단한다. 그리고 '⛔ 철회', '내 증거 절반이 무효 데이터 위에 있었다' 류 카드는 정리 대상으로 보이기 쉽지만 이 repo 의 자산이다. **접어도 되고 db 로 옮겨도 되지만 지우면 안 된다.**
- **claim 결속 검사 3종 세트** — `test_retracted_claims_are_id_bound_on_every_surface`(2897) · `test_legacy_ratchet_is_retired_not_reintroduced`(2938) · `test_each_surface_zero_comes_from_declarations_not_from_absence`(2949). 특히 `_LEGACY_UNBOUND: dict = {}` 를 **빈 채로 유지**하는 것(2849)과 `_DISCLAIMED` 가 빈 사유를 금지하는 것. 위에서 must 목록을 넓히라고 적었지만 그건 **더 조이는** 방향이고, 래칫을 다시 채우거나 `_BINDING_SKIP_PREFIX` 를 늘리는 건 완화다.
- **`_guard_mutation()` 의 3상태 판정**(app.py:41-49) — 로컬 기본 열림 / Render 기본 잠금 / 명시 env 가 양방향으로 이김, 그리고 알 수 없는 값("maybe")은 환경 판정으로 떨어짐. 2026-08-16 에 로컬까지 잠가서 자기 노트북에서 코멘트를 못 달던 사고의 수리다. `test_mutations_locked_on_render_open_locally`(929)가 여섯 케이스를 다 본다.
- **`_runner_qe()` 의 kgy/gabia 블록**(data.py:3540-3574) — 2026-09-08 에 `ldd` 로 링크된 MPI 를 캐고, `OMP_NUM_THREADS=1` 을 걸고, `LD_LIBRARY_PATH` 끝의 `:` 를 지우고, mpirun 이 없으면 시작 안 하는 그 전부. 같은 자리에서 세 번 죽고 나온 것이고 `test_compute_runner_does_not_guess_gpu_runtime`(727)이 지킨다. '간결하게' 줄이고 싶어지는 모양인데 각 줄이 사고 하나다.
- **artifact_policy 의 두 축 분리**(approval_status × use_scope)와 미등록=거부 규칙. 모양 검증 구멍은 위에서 P2 로 적었지만, `GOVERNED_PREFIXES` 에 걸린 경로가 원장에 없으면 거부한다는 규칙 자체와 `envelope()` 가 값과 지위를 같이 내보내는 것은 그대로 둔다.
- **`record_shown()` 이 allowlist 라는 점 자체**(data.py:35). 위에서 '어휘가 원장별로 다르다' 를 P1 로 적었지만, 고칠 방향은 **denylist 로 되돌리는 게 아니라** 어휘를 원장별로 주는 것이다. denylist 였을 때 retracted 로 표시한 −6.46 eV 갭이 화면에 계속 나왔다는 게 docstring 에 적혀 있다.
- **`glossary.py:191` 의 결속 문법** — `<span data-claim='MD_Ea_eV@b2o3'><s>b2o3 0.199±0.034</s> ⛔ 철회 (2026-08-23)</span>` 와 `<span data-claim='HZ-cross-system-Ea'>…+90 meV…</span>`. 09-08 이주가 실제로 착지한 자리고, 다른 산문을 고칠 때 베낄 본보기다.
- **`_closure_and_prereg_cards()`(data.py:4615)와 `_nd_anneal_card()`(data.py:4685)** — 09-07~08 에 들어온 db 구동 카드 3장. 대시보드 38장을 어디로 옮길지의 정답이 이미 여기 있다. `test_dashboard_closure_cards_read_db_not_hardcode`(690)가 규약을 굳혀 놨으니 시험도 같이 둔다.

## 발견

### [P1·broken] md-to-html-bypasses-claim-binding
- **어디**: `webapp/data.py:5947 (md_to_html) · webapp/app.py:1170 · webapp/app.py:189 (_bind_claims)`
- **근거**: 마크다운 렌더 경로가 둘인데 결속은 한쪽에만 걸려 있다. app.py:189 `return _C.annotate_claims(html)[0]` 은 `md_html()` 안에만 있고, data.py:5947 `md_to_html()` 은 "세미나/용어 문서를 페이지에 그대로 싣기 위한 **최소** 마크다운 렌더러" 라면서 annotate_claims 를 부르지 않는다. app.py:1170 `"html": D.md_to_html(path.read_text(...))` 로 `/seminar` 가 kb/seminars/*.md 전체를 이 경로로 싣는다. 실측: `/seminar` 의 data-claim 개수 0 · bound 0. 그 화면에 철회된 σ비가 산문으로 있다 — "단일 시드로 낸 1.33배 전도도 비교 — 멀티시드 판정으로 바꿨습니다". 지금은 철회를 **설명하는** 문장이라 규율 위반은 아니지만 스캐너는 그 구분을 못 하고, 이 표면은 애초에 결속 대상 문자열을 잡을 장치가 없다. BI 리뷰 요청 §6 가 스스로 물은 *"한 표면 안에서 렌더 경로가 갈라지는 것"* 의 구체적 실물이 이것이다.
- **고치는 법**: data.py:md_to_html 마지막 `return "\n".join(out)` 을 app.py 의 `_bind_claims` 와 같은 처리로 감싼다. 순환 import 를 피하려면 결속을 app.py 쪽 한 겹으로 올리거나(`md_to_html` 결과도 `_bind_claims` 를 통과시키기), canonical.annotate_claims 를 data.py 에서 지연 import 한다. 그리고 렌더러가 둘인 이유(외부 입력 vs repo 문서)를 남길 거면 **두 경로 모두 결속을 탄다**는 것을 시험으로 못 박는다.
- codex 필요: False

### [P1·broken] surface-zero-by-absence
- **어디**: `webapp/tests/test_webapp.py:2959 (test_each_surface_zero_comes_from_declarations_not_from_absence 의 must 목록)`
- **근거**: 표면별 음성시험의 `must` 는 손 목록 10개다: `["/", "/compare", "/explorer", "/glossary", "/governance", "/log", "/methods", "/requests", "/todo", "/api/handoff/..."]`. 무인자 GET 라우트는 28개다. 실측으로 결속이 **0개**인 표면: /seminar · /literature · /sdcp · /notes · /ledger · /nd-survey · /benchmarks · /elements · /compute · /files (10곳, data-claim 개수 0 · bound 0 · unbound 0). /cascade 는 data-claim 이 1개인데 bound 0 이다. 즉 이 11곳의 초록은 '선언 덕분' 이 아니라 '글자가 없어서' 인데, 그걸 가르라고 만든 시험이 바로 이 열한 곳을 안 본다. 같은 파일 2938행 `test_legacy_ratchet_is_retired_not_reintroduced` 는 "이주는 2026-09-08 에 끝났다(전 표면 0)" 이라고 적고 래칫을 비웠다.
- **고치는 법**: `must` 를 손 목록에서 `_html_routes()` 자동 열거로 바꾼다. 결속 0 인 표면은 실패시키지 말고 **`_NO_TARGET_SURFACES` 원장에 '이 화면은 결속 대상 문자열을 안 그린다' 를 사유와 함께 선언**하게 한다(DYNAMIC_EXEMPT 관례 그대로, 빈 사유 금지). 그러면 그 표면에 나중에 대상 문자열이 들어온 순간 선언이 거짓이 되어 시험이 잡는다.
- codex 필요: False

### [P1·missing] search-index-misses-six-sidebar-pages
- **어디**: `webapp/data.py:3344-3369 (search_index 의 pages 리터럴)`
- **근거**: `pages` 는 손으로 적은 14줄이고 주석은 "순서·묶음은 사이드바(base.html)와 같게 — 두 군데가 어긋나면 찾는 사람이 헷갈린다" 라고 경고한다. 실측으로 어긋났다: base.html 의 사이드바 링크 21개 중 `/governance` · `/ledger` · `/requests` · `/sdcp` · `/seminar` · `/fairchem` 여섯이 search_index 에 없다(`/sdcp/self-doping` 은 사이드바에도 없다). 같은 함수 안 주석이 이미 재발을 기록하고 있다 — "⚠ Benchmarks·Nd 서베이는 사이드바엔 있는데 검색으론 못 찾던 것, 2026-07-29 감사". 시험은 없다: tests/ 에서 search_index 를 부르는 곳은 test_webapp.py:2296 한 줄뿐이고 메모 라벨만 본다.
- **고치는 법**: pages 리터럴을 지우고 라우트 표에서 열거하거나(라벨은 별도 dict), 최소한 `set(사이드바 href) - set(search_index 페이지 url) == 셋()` 을 시험으로 건다. 손 목록을 남길 거면 빠뜨린 라우트마다 **사유**를 적게 한다.
- codex 필요: False

### [P1·wrong] record-shown-allowlist-is-ledger-blind
- **어디**: `webapp/data.py:29 (_STATUS_OK) · data.py:35 (record_shown)`
- **근거**: `_STATUS_OK = {"", "none", "canonical", "ok"}` 에 안 든 status 는 전부 숨긴다. docstring 은 "db record 하나의 release 노출 판정" 이라는 **범용** 이름을 달고 "이 status 만 정본으로 본다. 나머지는 **전부** release 화면에서 뺀다" 고 적었다. 그런데 status 어휘는 원장마다 다르다. db/properties/**.json 실측 분포에 record_shown 을 걸어 보면: ratified(8)→False · confirmed(7)→False · converged(4)→False · completed(3)→False · resolved(2)→False · 완료(5)→False · recovered(3)→False · primary_paper_value(2)→False. 특히 sei_neb.json 의 NEB 결과는 전부 `status: 'converged'` 라, 이 게이트를 그 원장에 적용하는 순간 ① Li⁺ 확산장벽 축이 통째로 빈다. 지금은 호출처가 딱 둘(data.py:1251 sei_summary · data.py:1341 sei_axes, 둘 다 sei_electronic.json)이라 안 터졌을 뿐이다.
- **고치는 법**: 이름과 계약을 좁힌다 — `record_shown(rec)` → `gap_record_shown(rec)` 이거나, 원장별 어휘를 인자로 받게 한다(`record_shown(rec, ok={...})`). docstring 의 "못 하는 것" 절에 **"이 allowlist 는 sei_electronic.json 어휘다. 다른 원장에 그대로 걸면 정상 기록이 사라진다"** 를 명시. v3 에서 이 게이트를 넓힐 계획이면 반드시 이걸 먼저 한다.
- codex 필요: False

### [P1·duplicate] sei-neb-two-loaders-zero-vs-unreadable
- **어디**: `webapp/data.py:1192 (sei_neb_by_phase) vs webapp/data.py:1351 (sei_axes) — 같은 db/properties/sei_neb.json`
- **근거**: 한 파일을 두 함수가 서로 다른 실패 규약으로 읽는다. sei_axes 는 `_nj, neb_unreadable = _read_ledger(np_)` 로 못 읽음을 세 번째 상태로 낸다. 같은 함수가 바로 아래에서 부르는 `sei_neb_by_phase()` 는 data.py:1192 `j = _load_json_safe("db/properties/sei_neb.json") or {}` — 조용히 {} 다. 임시 디렉터리에 깨진 sei_neb.json 을 놓고 실측: sei_axes ①축 state = `⛔ 원장 못 읽음`, 같은 시점 sei_neb_by_phase() = `{}`. sei_summary 표의 NEB 칸은 sei_neb_by_phase 에서 나오므로 그 표는 **아무 말 없이 빈칸**이 된다. data.py:1224 주석이 정확히 이걸 금지한다 — "둘 다 안 된다 — 못 읽었으면 못 읽었다고 화면이 말해야 한다"(2026-09-07). 09-04 에 들어온 NEB 리더가 09-07 이주에서 빠졌다. 로더는 셋이다: `_load_json`(68, 손상 로그) · `_load_json_safe`(927, 무음) · `_read_ledger`(944, 사유 반환).
- **고치는 법**: `sei_neb_by_phase()` 를 `_read_ledger` 로 바꾸고 `(dict, unreadable)` 을 반환해 호출처가 사유를 실어 나르게 한다. 나머지 `_load_json_safe` 호출처 4곳(data.py:834·858·900)도 같은 기준으로 훑는다. 장기적으로 로더 셋을 `_read_ledger` 하나로 모으고 `_load_json_safe` 는 폐기 — CLAUDE.md 의 '없는 것을 0 으로 표시하지 않는다' 를 강제하는 건 셋 중 하나뿐이다.
- codex 필요: False

### [P1·wrong] talk-exempt-reason-is-false
- **어디**: `webapp/tests/test_webapp.py:812-814 (DYNAMIC_EXEMPT["/talk/<slug>"])`
- **근거**: 사유가 사실과 다르다: "발표 슬러그가 kb/seminars 파일명과 1:1 이 아니다 — 대응 규칙을 확인하기 전에는 임의 슬러그를 넣어 404 를 통과로 세게 된다. ⏳ 규칙 확인 후 fixture 로 옮긴다." 그런데 app.py:1108 은 `p = D.LITDB / "talks" / f"{slug}.md"` 로 **litdb/talks** 를 읽고, kb/seminars 와 무관하다. `list_talks()` 의 `id` 가 곧 파일 stem 이라 대응은 1:1 이다. 실측: 7개 슬러그 전부 200 (do2026_bml_alzib_preconditioning · lee2026_skku_mlip_materials_design · … · yang2026_ncm_radial_microstructure_ml). 결과로 발표 7페이지가 결속 스캔 밖에 있다(직접 스캔해 보면 지금은 unbound 0 이라 실피해는 없다). 이건 2026-09-08 에 고친 `/api/handoff` 와 **똑같은 유형**이다 — 그 주석이 그렇게 적혀 있다: "⛔ 2026-09-08 (회신 BG ②) — EXEMPT 사유가 **사실과 달랐다** … 틀린 사유가 결속 검사에서 handoff 를 통째로 빼고 있었다".
- **고치는 법**: EXEMPT 에서 빼고 `DYNAMIC_FIXTURES["/talk/<slug>"] = ["lee2026_skku_mlip_materials_design", "yang2026_ncm_radial_microstructure_ml"]` 로 옮긴다(둘 다 200 확인). 겸사겸사 EXEMPT 사유를 **주장으로 취급**하는 시험을 하나 더 건다 — 사유에 나오는 경로가 실제 코드 경로와 맞는지까지는 기계로 못 보지만, 최소한 "⏳" 가 붙은 항목은 만료일을 요구할 수 있다.
- codex 필요: False

### [P1·broken] write-routes-have-no-orphan-guard
- **어디**: `webapp/tests/test_webapp.py:907 (MUTATION_PROBES) · test_webapp.py:949 (403 시험) · webapp/app.py:52 (_guard_mutation)`
- **근거**: 동적 GET 라우트에는 '고아 금지' 시험이 있는데(test_dynamic_routes_are_covered_not_skipped) 쓰기 라우트에는 없다. 앱의 쓰기 라우트는 7개다: /api/note-image(POST) · /api/concept-upload/<cid>(POST) · /api/comments/<rel>(POST·PATCH·DELETE) · /api/highlights/<rel>(POST·DELETE) · /api/file-rename(POST) · /api/log(POST). MUTATION_PROBES 는 5줄뿐이고 `/api/note-image` · `/api/highlights/<rel>` POST·DELETE · `PATCH /api/comments` 가 빠져 있다. 게다가 그 시험은 `if not A.READ_ONLY: pytest.skip(...)` 이라 로컬 기본에서 **항상 건너뛴다** — 실행 결과가 그렇다: `SKIPPED [1] webapp/tests/test_webapp.py:949: 이 실행은 쓰기가 열려 있다`. `RENDER=1` 로 돌리면 2 passed 다. `_guard_mutation()` 은 before_request 훅이 아니라 라우트마다 손으로 부르는 헬퍼(호출처 7곳: app.py 895·932·969·999·1013·1027·1263)라, 새 POST 라우트가 가드를 빼먹어도 아무 시험도 안 터진다.
- **고치는 법**: ① 라우트 표에서 write 메서드를 자동 열거해 `MUTATION_PROBES` 에 다 있는지 확인하는 고아 시험을 추가한다(GET 쪽 관례 그대로). ② 403 시험의 skip 을 없앤다 — `A.READ_ONLY` 를 monkeypatch 하거나 `RENDER=1` 하위프로세스로 돌려 항상 실행되게 한다. 지금은 CI 에서 이 게이트가 한 번도 안 밟힌다.
- codex 필요: False

### [P1·ia] dashboard-highlights-673-line-prose
- **어디**: `webapp/data.py:3929-4601 (dashboard_highlights, 673줄 단일 함수)`
- **근거**: 카드 41장 중 **38장이 함수 본문에 박힌 산문**이고, db 를 읽어 만드는 건 3장뿐이다(`_closure_and_prereg_cards()` 2 + `_nd_anneal_card()` 1 — 전부 09-07~08 에 들어온 것). 날짜 분포: 08-27 하루가 11장, 08-28 이 6장. 정본 숫자가 산문에 복사돼 있다 — data.py:4191 "정본 기록(2.066)과 소수 넷째 자리까지 일치", 4199 "**gap 2.0989 eV** (정본 2.099)", 4208 "인용은 계속 2.066 / 2.099". 레지스트리가 바뀌어도 이 문자열은 안 따라온다. `test_no_hardcoded_canonical_numbers`(test_webapp.py:35)는 `^CANONICAL\s*=\s*\{` 리터럴만 찾으므로 산문 안 숫자는 못 본다. 정렬은 data.py:4597 `hi.sort(key=lambda c: c.get("d") or "", reverse=True)` 로 최신순은 맞다.
- **고치는 법**: v3 에서 카드를 db 로 옮긴다 — `_closure_and_prereg_cards()`(data.py:4615)가 이미 그 형태이고 `test_dashboard_closure_cards_read_db_not_hardcode`(test_webapp.py:690)가 규약을 굳혀 놨으니 그 패턴을 그대로 늘린다. 화면 쪽은 '이번 주'(최근 7~14일) 기본 노출 + 나머지는 월별 접힘. **카드를 지우지는 않는다** — 철회·오진 기록이 이 repo 의 자산이다. 옮기면서 하드코딩 정본값은 `canonical_comparable()` 조회로 바꾼다.
- codex 필요: False

### [P2·stale] today-in-dated-cards
- **어디**: `webapp/data.py:4373 · webapp/data.py:4540`
- **근거**: 둘 다 `"d": "2026-08-28"` 카드인데 본문이 상대 시간어를 쓴다. 4373: "**오늘만 세 번째로 나온 같은 종류의 실수: 다른 것을 비교하고 그 차이를 물리라고 불렀다.**" 4540: "\"시드 산포 96 %\" 와 \"1200 K 독립 재현\" 을 오늘 새 발견으로 적었다." 오늘(2026-09-08) 대시보드에서 읽으면 11일 전 일이 오늘 일로 읽힌다. 같은 유형이 test_webapp.py:2685 주석에도 있다("오늘만 세 번 겪은").
- **고치는 법**: "오늘" → "그날"/"08-28 하루에" 로 바꾼다. 카드가 db 로 이주하면 상대 시간어를 금지어로 걸 수 있다 — 카드 본문에 `오늘|어제|이번 주` 가 있으면 실패하는 한 줄 시험이면 된다(날짜 필드가 이미 있으니 상대어는 항상 잉여다).
- codex 필요: False

### [P2·duplicate] glossary-hardcoded-canonical-numbers
- **어디**: `webapp/glossary.py:41 · glossary.py:63 · glossary.py:191 · glossary.py:243 · (시험) webapp/tests/test_webapp.py:35`
- **근거**: 정본값 사본이 용어집 산문 안에 산다. glossary.py:41 `"ours":"canonical(eigenvalue): comp1 2.066 / modelc 2.099 / +B₂O₃ 1.9671 / lpsocl 2.2309 eV · comp2 2.04는 <b>잠정</b>…"`. glossary.py:63 은 ICOHP `comp1 −5.938 / comp2 −5.913`, `Li–Cl/Li–Br(−2.111 / −1.934)`, `comp1의 Li–Cl은 −1.861`, `E_VRH 22.06→20.03, B_VRH −18.2%`. **오늘 기준으로는 전부 레지스트리와 맞는다**(gap 4종·ICOHP comp1 −5.9381·comp2 −5.913·E_VRH 22.06/20.03 대조 완료) — 그래서 wrong 이 아니라 duplicate 다. 문제는 감시가 없다는 것: `test_no_hardcoded_canonical_numbers` 는 `ROOT/"webapp"/"data.py"` 만 읽고 glossary.py 는 안 본다. 레지스트리가 바뀌면 여기만 조용히 옛 값을 말한다 — 그게 data.py 에서 실제로 일어났던 drift 다(data.py:737 주석의 comp2 0.275 사례).
- **고치는 법**: 두 가지 중 하나. ① 이 문장들의 숫자를 `{gap[comp1]}` 식 자리표시자로 바꾸고 렌더 때 `canonical_comparable()` 로 채운다. ② 최소 조치로, 레지스트리에 있는 값의 문자열이 glossary.py 에 있으면 그 값이 **현재 레지스트리 값과 같은지** 대조하는 시험을 추가한다(어긋나면 실패). ①이 낫지만 산문 가독성을 해치므로 v3 설계 때 판단. 참고로 glossary.py:191 은 이미 `data-claim='MD_Ea_eV@b2o3'` · `data-claim='HZ-cross-system-Ea'` 로 제대로 결속돼 있다 — 그 줄이 모범이다.
- codex 필요: False

### [P2·broken] artifact-policy-not-fail-closed-on-shape
- **어디**: `webapp/artifact_policy.py:63-77 (_load) · 특히 71행`
- **근거**: 모듈 docstring 이 fail-closed 를 계약으로 내걸고("요청이 필요한 opt-in 을 안 들고 오면 **거부한다**(fail-closed)"), `_load()` docstring 도 "원장이 없거나 깨졌으면 빈 dict (= 전부 거부)" 라고 적었다. 그런데 try 는 `json.loads` 만 감싸고, 71행 `out[_norm(a["source_path"])] = a` (와 74·77행의 `s["path"]`·`f[k]`)는 밖이다. 실측: manifest 의 artifacts[0] 에서 `source_path` 키만 빼고 resolve 를 부르면 `KeyError: 'source_path'` 가 그대로 올라간다 → 거부가 아니라 500. `test_manifest_tamper_fails_closed`(test_webapp.py:1429)는 **어휘** 위조(approval_status 를 "approved_by_nobody" 로)만 보고 **모양** 위조는 안 본다. 게다가 그 시험이 보는 건 `D.cascade_truth()` 지 `AP.resolve()` 가 아니다.
- **고치는 법**: `_load()` 의 루프를 `try/except (KeyError, TypeError)` 로 감싸 빈 dict 를 돌려주거나, 항목별로 필수 키가 없으면 그 항목만 건너뛰되 **원장 자체를 무효로 표시**한다(부분 로드가 더 위험하다 — 빠진 항목이 '미등록'이 되어 거부되는 건 맞지만, 조용히 그러면 안 된다). 시험은 모양 위조 케이스를 추가한다 — 필수 키 제거 · artifacts 가 list 가 아님 · 항목이 dict 가 아님.
- codex 필요: False

### [P2·broken] tamper-test-writes-the-real-ledger
- **어디**: `webapp/tests/test_webapp.py:1442-1450 (test_manifest_tamper_fails_closed)`
- **근거**: 시험이 저장소의 governed 원장을 **제자리에서 덮어쓴다**: `D.CASCADE_MANIFEST_PATH.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")` 하고 `finally` 에서 원문을 되돌린다. pytest 가 중간에 죽으면(Ctrl-C·OOM·타임아웃) db/properties/cascade_audit_manifest.json 이 위조된 채로 남는다. 그 파일은 artifact_policy 의 fail-closed 근거이자 sha256 대조 대상이라, 남으면 다음 실행의 `test_manifest_tamper_fails_closed` 앞부분 해시 대조가 통째로 무너진다. 같은 파일 1969행에 `test_db_property_files_are_lf_pinned` 가 있어 줄끝까지 관리하는 원장이다.
- **고치는 법**: tmp_path 에 사본을 만들고 `monkeypatch.setattr(D, "CASCADE_MANIFEST_PATH", tmp)` 로 돌린다. 이미 test_webapp.py:119 `test_assessment_sidecar_is_authoritative(tmp_path, monkeypatch)` 가 그 방식이니 관례가 이미 있다 — 이 한 건만 옛 방식이다.
- codex 필요: False

### [P2·broken] lazymap-json-dumps-returns-empty
- **어디**: `webapp/data.py:618 (_LazyMap) · data.py:665 (_LazyIndex)`
- **근거**: 둘 다 `dict` 를 상속하는데 하부 저장소를 절대 안 채운다. 오버라이드한 메서드(`__getitem__`·`get`·`items`·`keys`·`values`·`__iter__`·`__len__`·`__contains__`)로만 산다. C 레벨을 직접 보는 연산은 **조용히 빈 값**이다. 실측: `len(CANONICAL)=19` · `dict(CANONICAL)` 정상 · `{**CANONICAL}` 정상 · 그런데 `json.dumps(CANONICAL)` → `{}` 이고 `CANONICAL.copy()` → `{}` 다. 지금은 템플릿이 `canonical=D.canonical_table()`(평범한 dict, data.py:1464)을 받으므로 새는 데는 없다 — compare.html:33 `const CANON={{ b.canonical|tojson }}` 도 그쪽이다. 하지만 누가 `D.CANONICAL` 을 `|tojson` 에 넘기면 화면 전체 정본표가 `{}` 가 되고 아무것도 안 터진다.
- **고치는 법**: `json.dumps` 로 새어 나가는 걸 막으려면 `__reduce__`/`to_dict()` 를 주거나, 안전하게는 클래스 docstring 의 "못 하는 것" 절에 **"`json.dumps`·`.copy()`·`.pop()`·`.update()` 는 빈 값이다. 직렬화하려면 `dict(CANONICAL)` 을 먼저 씌워라"** 를 명시하고, `assert json.dumps(D.CANONICAL) != "{}"` 가 아니라 반대로 '템플릿에 _LazyMap 을 넘기지 않는다' 를 시험으로 건다. ⚠ `_LazyMap` 자체는 지우면 안 된다 — test_running_process_sees_source_change(test_webapp.py:634)가 `type(D.CANONICAL).__name__ == "_LazyMap"` 을 명시적으로 요구한다.
- codex 필요: False

### [P2·useless] registry-cache-key-reparses-every-call
- **어디**: `webapp/canonical.py:184 (_mtime_key) · canonical.py:197 (registry)`
- **근거**: `registry()` 는 캐시가 맞는지 보려고 매번 `_mtime_key()` 를 부르는데, 그 함수가 88 KB 레지스트리를 **다시 json.load 하고** 거기서 뽑은 고유 source_path 19개를 전부 stat 한다. 즉 캐시 히트 경로가 원본 파싱 1회 + stat 20회다. 페이지당 registry() 호출 실측: `/` 56회 · `/compare` 93회 · `/explorer` 113회 · `/composition/comp1` 79회. `/explorer` 기준 페이지당 JSON 파싱 113회 + stat 2260회이고, `_mtime_key()` 113회만 따로 재면 0.108 s — 그 페이지 전체 렌더 0.15 s 의 약 70 % 다. 원인은 `_LazyMap._now()`(data.py:621)가 dict 접근 **한 번마다** registry() 를 부르는 구조다.
- **고치는 법**: 신선도 계약은 못 건드린다(아래 keep_as_is 참조). 대신 ① 요청 단위 memo — Flask `g` 에 registry 를 한 번만 담거나, ② `_mtime_key` 결과를 아주 짧게(예: 같은 요청 안 / 0.5 s) 캐시한다. ③ 더 근본적으로는 `_now()` 를 매 접근이 아니라 registry 객체 identity 로 memo 한다. 어느 쪽이든 `test_running_process_sees_source_change` 와 `test_source_edit_propagates_to_screen` 이 계속 통과해야 한다.
- codex 필요: False

### [P2·useless] sei-axes-returns-dead-neb-payload
- **어디**: `webapp/data.py:1419 (`], "neb": neb}`)`
- **근거**: `sei_axes()` 가 sei_neb.json 의 **results 원본 전체**를 `neb` 키로 같이 돌려준다 — protocol_payload · endpoint_coords_sha · allowed_statement · forbidden_statement · citable_downgraded_by 까지 통째로. 소비처가 없다: 템플릿에서 sei_axes 를 쓰는 곳은 index.html:66 `{% if sei_axes and sei_axes.axes %}` 와 index.html:69 `{% for a in sei_axes.axes %}` 두 줄뿐이고 app.py:283 `sei_axes=D.sei_axes()` 가 전부다. `.neb` 를 읽는 템플릿은 없다.
- **고치는 법**: `"neb": neb` 를 뺀다. 함수 안에서 n_neb·neb_retracted 계산에만 쓰이므로 반환에서 빼도 화면은 그대로다. 굳이 남길 거면 왜 남기는지 주석을 단다.
- codex 필요: False

### [P2·useless] dead-code-canonical-group-and-empty-provisional
- **어디**: `webapp/data.py:703 (canonical_group) · data.py:741 (CANONICAL_PROVISIONAL_VALUES) · 그 위를 도는 루프 data.py:1058 · data.py:1471`
- **근거**: repo 전체(py·html·js)에서 `canonical_group` 은 정의 한 곳(data.py:703)뿐, 호출 0. `CANONICAL_PROVISIONAL_VALUES = {}` 는 영구 빈 dict 인데(주석: "⚠ 여기에 숫자를 다시 넣지 말 것 — 정본은 db/properties/canonical_registry.json 이다") 두 함수가 여전히 그 위를 돈다: canonical_values 의 `for (k, c), val in CANONICAL_PROVISIONAL_VALUES.items():`(1058) 과 canonical_table 의 같은 줄(1471). 게다가 canonical_values 의 docstring 이 "조성 하나의 canonical 값 — 잠정값(CANONICAL_PROVISIONAL_VALUES)도 채워 넣는다" 라고 **없는 동작을 설명**한다.
- **고치는 법**: canonical_group 은 지우거나(같은 정보는 `CANONICAL_ENTRY[(m,s)]["comparison_group"]` 로 직접 나온다) 실제로 쓰는 곳을 만든다. CANONICAL_PROVISIONAL_VALUES 와 그 두 루프는 지우고, 대신 상수 자리에 **묘비 주석만** 남긴다(왜 비웠는지가 자산이다). canonical_values docstring 도 같이 고친다.
- codex 필요: False

### [P2·duplicate] structures-for-unbounded-and-duplicated
- **어디**: `webapp/data.py:442 (_PREFIX) · data.py:455 (_blocked_by_longer) · data.py:468 (structures_for)`
- **근거**: 두 가지가 겹친다. ① **무제한**: `structures_for()` 는 db/structures 를 rglob 해 prefix 가 맞는 걸 전부 낸다 — 실측 sdcp 95 · vgcf_hbn 64 · li3n 60 이고, 렌더된 HTML 에서 그 이름이 **95/64/60 전부 문자열로 확인**된다(/composition/sdcp 71 KB). ② **중복 소유**: `_PREFIX["vgcf_hbn"] = ["vgcf", "hbn", "li3n", "lic6"]` 인데 `li3n` 은 _PREFIX 키가 아니라 `[cid]` 폴백으로 같은 "li3n" 을 쓴다. `_blocked_by_longer` 는 **더 긴** prefix 만 막으므로 길이가 같은 이 충돌은 못 막는다. 실측 겹침: vgcf_hbn 64개 중 60개가 li3n 것과 동일(vgcf_hbn 전용은 4개뿐), 데이터 CSV 도 8개 겹침(li3n_barrier_fig_origin.csv 등). 그리고 `lic6` 페이지는 vgcf_hbn 이 자기 prefix 로 선언했는데도 구조 0건이다. 주석은 이 장치의 목적을 "modelc 페이지가 modelc_nd_doped_* / modelc_v3_* 파일을 끌어오지 않게" 라고 적었는데, 같은 길이 충돌은 설계에서 빠져 있다.
- **고치는 법**: ① 소유를 명시적으로 만든다 — `_PREFIX` 를 파일→조성 단일 매핑으로 뒤집거나, 같은 길이 prefix 를 둘 이상이 선언하면 **시작할 때 실패**하게 한다(지금은 조용히 둘 다 가져간다). ② 화면 쪽은 대표 구조 3~5개만 기본 노출 + "구조 95개 전체" 는 접거나 별도 라우트. 파일을 지우자는 게 아니라 **첫 화면에서 내리자**는 것이다.
- codex 필요: False

### [P2·missing] retracted-sigma-ratio-has-no-scannable-text
- **어디**: `db/properties/canonical_registry.json (MD_sigma_ratio_600K/800K/1000K @ b2o3_vs_modelc, value: null) · webapp/canonical.py:403 (bound_claims)`
- **근거**: CLAUDE.md 가 이름을 대는 철회 선례 — "단일시드 1.33× 철회 사례, SEMIFINAL 2026-07-09" — 가 스캐너에 안 잡힌다. 레지스트리의 세 σ비 항목은 `value: None` 이라 `all_claims()` 에서 `text=None` 으로 나오고(실측: `non_citable MD_sigma_ratio_600K@b2o3_vs_modelc text='None'`), citation_hazards.json 에도 `1.33` 문자열이 없다(grep 0건). 그래서 지금 화면 네 곳이 "1.33×/1.33배" 를 결속 없이 찍는다 — /glossary("단일 config 판정 금지(단일시드 1.33× 철회 교훈)") · /log · /requests · /seminar. 넷 다 철회를 **설명하는** 맥락이라 규율 위반은 아니지만, 스캐너는 그 구분을 못 하므로 앞으로 누가 "b2o3 가 1.33× 빠르다" 라고 써도 시험은 초록이다.
- **고치는 법**: citation_hazards.json 에 이 선례를 hazard 로 올리고 `forbidden_phrases: ["1.33×", "1.33배"]` 를 넣는다. 그러면 네 곳은 `data-claim` 을 달아야 하는데 — 그게 바로 이 repo 가 원하는 상태다(철회를 이름 대고 말하는 것). 오탐이 걱정되면 "1.33× 전도도" 처럼 문구를 구체화한다(hazard_claims docstring 이 이미 그 위험을 적어 뒀다).
- codex 필요: False

### [P2·useless] files-literature-ship-a-megabyte
- **어디**: `webapp/data.py:5045 (gallery_files) · /files · /literature 라우트`
- **근거**: 실측 응답 크기: /files 921 KB · /literature 955 KB · /cascade 585 KB. `gallery_files()` 는 페이지네이션 없이 1122건을 한 번에 내고(0.14 s), 그 전부가 HTML 행으로 렌더된다. 서버는 빠르지만 브라우저에 100만 자짜리 DOM 이 간다. 대시보드조차 123 KB 다.
- **고치는 법**: 서버 쪽 페이지네이션이나 최근 N일 기본 + 더보기. `gallery_days()`(data.py:5095)가 이미 날짜 묶음을 내니 '오늘·어제·N일 전' 첫 3~5묶음만 렌더하고 나머지는 접거나 lazy 로드하면 된다. 검색·필터는 이미 서버 쪽(q/kind/used/folder/cmt)이라 구조는 갖춰져 있다.
- codex 필요: False

### [P2·ia] journal-jsonl-lives-in-the-code-dir
- **어디**: `webapp/journal.jsonl (81줄·81 KB) · webapp/app.py:1231 (JOURNAL)`
- **근거**: POST /api/log 가 append 하는 가변 데이터 파일이 코드 디렉터리에 있고, gitignore 도 안 돼 있어 커밋에 계속 섞인다(최근 3커밋: fc3624184 "작업기록 5건" · 12e6d0c9b · 10fd99b0b). 다른 원장은 전부 db/ 아래에 있다(db/properties/**, db/governance/**, db/file_comments.json, db/file_highlights.json — 뒤 둘은 data.py:5334-5335 에서 DB 아래를 가리킨다).
- **고치는 법**: db/journal.jsonl 로 옮긴다(app.py:1231 한 줄 + 기존 파일 git mv). 코드와 데이터가 같은 폴더에 있으면 v3 재편 때 무엇이 산출물인지 판단이 흐려진다.
- codex 필요: False
