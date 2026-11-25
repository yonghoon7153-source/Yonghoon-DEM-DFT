# webapp — 판정 원장(/governance) + 산출물·T·Q 원장(/ledger)

## 지금 무엇인가
/governance 는 네 원장(결정 22 · 게이트평가 4 · 산출물 12 · 인용위험 25)을 한 페이지에 순서대로 편 표 모음이고, 2026-09-08 커밋 d7d838896 으로 결정 원장 표가 신설되면서 kind·사전등록·근거문서·비준지문 칸이 붙었다. /ledger 는 그와 별개로 db/properties/tq_ledger_*.json 하루치(현재 단 한 개, 2026-08-26)를 T 17건 + Q 네 절 + 정정 8 + 도구 6 으로 펴는 화면이다. 두 화면 다 "값의 옳고 그름은 판정하지 않고 원장을 옮길 뿐"이라는 설계를 docstring 과 화면 하단에 명시하고 있고, 그 원칙 자체는 잘 지켜진다.

## 처음 오는 사람
처음 온 사람은 이 두 화면에 **닿지를 못한다**. 대시보드 본문에 `/governance` 링크가 0개다(전체 HTML 통틀어 1회, 그것도 사이드바 nav 항목). 유일한 입구는 사이드바 네 번째 절 "자료 · 기록" 안 다섯 번째 줄이고, 그 위 네 줄은 Files·Glossary·메모·미결 리스트라 "이게 이 repo 의 중심 규율"이라는 신호가 전혀 없다. 대시보드 헤더는 아직 `v2 (2026-08-26)` 배지를 달고 새 것으로 T·Q 원장을 가리키는데, 그게 하필 13일째 안 갱신된 화면이다.

들어간 뒤에도 막힌다. (a) 첫 화면이 초록 "✅ 원장 검증 통과" 인데, 그 아래로 유실 1건·BLOCKED 4건이 이어져서 초록이 무엇을 보증한 건지 알 수 없다 — 실제로는 그래프·어휘 무결성만 본 것이고 화면은 그 범위를 말하지 않는다. (b) 어휘 안내가 없다. 보고량·사전등록·지문 🔒 일치·`value:MD_Ea_eV/b2o3` 같은 claim_ref 형식·`kind: estimand` 툴팁이 아무 설명 없이 나오고 /glossary 로 가는 링크도 없다. (c) 결정 22건 중 14건은 근거 문서가 클릭이 안 되는 회색 문자열(`kb/questions/…md`)이라, "왜 그렇게 정했나"를 읽으러 갈 수가 없다 — 정작 `/todo` 는 kb 마크다운을 이미 렌더하고 있는데 여기만 안 붙어 있다. (d) 결정 표는 22행 × 여섯 칸이고 한 칸에 700자짜리 문단이 들어가서, 페이지 텍스트의 절반(602줄 중 286줄)을 이 표 하나가 먹는다. 필터도, 접힘도, 행별 앵커도 없다. (e) /ledger 는 "오늘 들어온 것 / 오늘 정정한 우리 기록 / 오늘 만든 도구 / 내일 원장이 채운다" 라고 12번 넘게 말하는데 그 '오늘'은 2026-08-26 이다.

처음 온 사람이 여기서 **할 수 있는 것**은 있다: 결정 ID·종류·상태·비준 여부를 훑고, 최신 4건이 결과를 보기 전에 봉인됐다는 사실을 확인하고, "무엇을 인용하면 안 되나"를 25행 표로 읽는 것. 문제는 그 셋 다 스크롤로만 도달하고, 그중 하나(b2o3 Ea)는 같은 페이지 안에서 서로 반대 지시를 준다는 것이다.

## 건드리면 안 되는 것
- **세 상태를 가르는 지문 표시**(app.py:596-603, governance.html:148-150) — 없음/일치/불일치. 종전 판이 `want is None` 을 '일치' 로 세어 승인이 아예 없는 결정에도 🔒 를 붙였던 실측 회귀다. 'none' 을 'ok' 로 합치는 단순화 금지.
- **'– 미기재' 를 기본값으로 메우지 않는 규율**(app.py:606-607, governance.html:126-128)과 그것을 문자열 개수로 잠그는 시험 test_governance_missing_results_seen_is_unstated_not_prereg. 이 repo 의 반복 사고형(없는 것을 0/거짓으로 읽기)에 대한 유일한 자동 방어다. 열을 옮기더라도 '미기재는 사전등록이 아니다' 는 화면과 시험에 함께 남아야 한다.
- **시험이 글자 그대로 집는 문구 다섯**: "🔒 일치" · "본문이 승인 뒤 바뀌었다"(test_governance_digest_binding_shown, 템플릿 146-147행에 경고 주석까지 달려 있다) · "◻ 미평가" · "미평가는 실패가 아니다" · "철회된 옛 판정"(test_governance_page_negative_vocabulary). v3 에서 문구를 다듬고 싶으면 시험을 같은 커밋에서 옮겨야 한다.
- **전건 렌더 시험 두 개**: test_governance_page_renders_every_ledger_row 와 test_governance_decision_ledger_renders_every_decision 은 모든 artifact ID·decision ID·assessment claim_ref, 그리고 `원장 kind: <k>` 툴팁 문자열과 모든 `record` 경로가 HTML 에 있어야 통과한다. ⇒ **옛 결정을 접는 것은 되지만 DOM 에서 빼는 것은 안 된다.** 접힘은 CSS/details 로.
- **accessor 가 dict 를 준다는 사실과 `_rows()` 헬퍼**(app.py:574-578). 첫 판이 `.get("artifacts", [])` 라 화면이 조용히 빈 표가 됐고 '원장이 비었다' 와 '원장을 잘못 읽었다' 가 구분이 안 됐던 실측 회귀다. 주석 통째로 보존.
- **'원장 부재 ≠ 위험 0' 분기**(governance.html:77-83): 인용위험 원장을 못 읽으면 빈 표가 아니라 붉은 '⛔ 인용 위험 원장을 못 읽었다' 를 그린다. /ledger 의 3분법(파일 없음 / 못 읽음 / 칸 비어 있음, ledger.html:42-65)도 같은 계열이고 docstring 이 그 계보를 적어 놨다. 둘 다 유지.
- **두 화면의 '이 페이지가 못 하는 것' docstring**(app.py:557-568, 647-663). 한계를 화면 코드 옆에 적어 두는 것이 이 repo 규율이고, 실제로 이번 조사에서 kb 링크 한계·해석 안 함 선언을 여기서 확인했다. 기능이 바뀌면 같이 고치되 지우지 않는다.
- **Q 번호가 문서별 로컬이라는 절마다의 경고**(ledger.html:146-147)와 헤더의 kb/CODES.md 안내. 반복이 장황해 보여도 이게 오독 방지 장치다.
- **T 상태 이모지를 해석하지 않고 색만 입히는 원칙**(app.py:640-642, 676-678) — 원장 문자열을 그대로 옮기고 모르는 이모지는 기본색. '기타' 버킷도 유지.
- **산출물 원장의 위험순 정렬**(app.py:581-583, lost → suspect_banned → superseded → reference → canonical, 그 안에서 사본 수 오름차순)과 reassessment/status_history 를 행 아래 펴는 것. 재판정의 '쓸 수 있는 것 / 못 쓰는 것' 2행은 이 원장에서 가장 실용적인 부분이다.
- **claim ID 결속 구조 전체**(canonical.py:389-505, governance.html:62-65·211-212) — ±140자 근접성을 폐기하고 data-claim 으로 이름을 대게 한 2026-09-08 이주분. claim_ref_to_id 가 형식이 안 맞으면 빈 문자열을 돌려 유령 결속을 안 만드는 것도 그대로.
- **/ledger ↔ /todo 상호 링크**(ledger.html:35 의 '📋 미결 리스트' 버튼, app.py:520-521 의 /todo 배너). 하루치 원장과 원본 open_items 를 잇는 유일한 다리이고 날짜를 하드코딩하지 않았다.
- **'값 대기' 라는 말 자체**(빈칸을 0 이나 '없음' 으로 쓰지 않는 어휘). 종료된 행에 붙는 것만 고치고 어휘는 남긴다.

## 발견

### [P0·wrong] gov-force-statement-700k
- **어디**: `db/governance/decisions.json (D-2026-09-08-b2o3-uma-vs-dft-force.statement) → webapp/templates/governance.html:131-132`
- **근거**: 화면 '무엇을 정했나' 칸에 이렇게 찍힌다: "기존 궤적(highT_reseed_traj) s2 의 800·1000 K 에서 2–50 ps 창 등간격 5프레임씩, 계 2 × 온도 2 × 5 = 20 점." 그런데 비준된 카드(db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json §4)는 "kgy ~/work/runs/arrhenius_6pt_traj/{b2o3,modelc}/T700_s{2,3,4}/… traj.xyz" · "각 계 × 시드 s2·s3 × 700 K … 계 2 × 시드 2 × 5 = 20 점. ⚠ 종전 판의 '온도 2축' 을 시드 2축으로 바꾼 것이다" 다. 결정 자신의 status_history 도 "§4 개정판 재비준 (2판). 표본 700 K · 시드 2축 · kgy CPU 빌드" 라고 적고 ratification.revision = "2판 (§4 개정)" 인데 statement 만 1판 그대로다. 화면은 그 행에 '✅ 비준 2026-09-08 · 지문 🔒 일치 · 🔒 결과 보기 전' 을 나란히 찍는다 — digest 는 statement 를 포함해 계산되므로 낡은 문장이 '봉인된 정본'으로 도장을 받는다. 게다가 statement 가 이름 댄 highT_reseed_traj 는 같은 페이지 산출물 원장 첫 행 'A-highT-reseed-traj | ⛔ 유실 | 0 | lost | search_exhausted' 다.
- **고치는 법**: decisions.json 의 statement 에서 §4 표본 문장을 카드 2판과 일치시키고(700 K · 시드 s2·s3 · arrhenius_6pt_traj) 1저자 재비준으로 digest 를 다시 찍는다. 근본 대책은 statement 에 §4(설계·표본)를 복사하지 않고 카드 §2(보고량)·§5(문턱)만 두는 것 — 카드가 개정될 때마다 statement 가 조용히 갈라진다. 화면 쪽은 statement 가 인용한 산출물 ID(highT_reseed_traj 등)를 산출물 원장 상태와 대조해 'lost 인 산출물을 근거로 든 결정' 을 표시하는 검사를 붙인다.
- codex 필요: False

### [P0·wrong] gov-b2o3-hazard-vs-closure
- **어디**: `db/properties/citation_hazards.json (b2o3_md_arrhenius 행) → webapp/templates/governance.html:61-71 · 같은 페이지 governance.html:112-152 의 D-2026-09-07-b2o3-md-closure-retrospective 행`
- **근거**: 한 화면에 반대 지시가 위아래로 있다. 위(인용위험, 먼저 읽힌다): "CONDITIONAL | db/properties/b2o3_md_arrhenius.json | Ea — 헤드라인이 3회 교체됨 … | 풀리는 조건: FINAL_for_paper.Ea_eV_PAPER 만 인용". 아래(결정, active·ratified·지문 일치): "b2o3 의 UMA-MD 전도도 축(D · Ea · σ · 구간 Ea)은 인용 불가다. 이 축에서 인용 가능한 수는 0개이며, 상태명은 closed_no_action / non-citable 이다." 마감 기록 원문(b2o3_md_closed_retrospective_2026_08_25.json 금지_서술)은 더 명시적이다: "⛔ b2o3 의 D · Ea · σ · 구간 Ea 중 어느 것도 물질 값으로 인용 — 0.222 eV 포함." 더구나 hazard 가 가리키는 키 `FINAL_for_paper.Ea_eV_PAPER` 는 그 파일에 더 이상 없다 — 실물은 `Ea_eV_PAPER_SUPERSEDED_600K_only` 와 `Ea_eV_PAPER_RETRACTED_2026_08_23` 둘뿐이고 둘 다 철회다. 인용위험 원장 헤더도 '갱신 2026-08-31' 이라 09-07 마감 이전이다.
- **고치는 법**: citation_hazards.json 의 그 행을 CONDITIONAL → BLOCKED 로 올리고 fix 를 "인용 가능한 수 0개 — D-2026-09-07-b2o3-md-closure-retrospective" 로 바꾼다. 더 중요한 구조 수정: 마감 결정(kind=closure)이 어떤 파일의 축을 닫으면 화면이 그 파일의 hazard 행과 자동으로 대조해 어긋나면 붉게 표시하게 한다 — 지금은 두 원장이 같은 페이지에 있으면서 서로를 안 본다. hazard 행에 `decision_ref` 필드를 두는 게 최소 배선이다.
- codex 필요: False

### [P1·stale] ledger-frozen-2026-08-26
- **어디**: `webapp/app.py:664 (D.load_tq_ledger) · db/properties/tq_ledger_2026_08_26.json (유일 파일) · webapp/templates/ledger.html:134-137`
- **근거**: `ls db/properties/tq_ledger_*.json` 결과가 tq_ledger_2026_08_26.json 하나뿐이고 화면 제목이 "🧾 T·Q 원장 — 2026-08-26 심포지엄 판독 하루치" 다. 오늘은 2026-09-08 — 13일 전 스냅샷이다. 그런데 화면 문구는 전부 현재형이다: "📥 오늘 들어온 것" · "🔴 오늘 정정한 우리 기록 (8건)" · "🧰 오늘 만든 도구 (6건)" · "9 '오늘' 칸 값 대기" · 표 아래 각주 "값 대기 = 원장의 '오늘' 칸이 - — 내일 원장이 채운다". 그 '내일'이 13일째 안 왔는데 화면 어디에도 그 사실이 없다. 내용도 이미 추월당했다 — T1b 는 "b2o3 붕괴를 softening 으로 설명하는 길이 사실상 닫힌다" 에서 멈춰 있는데 그 사이 D-2026-09-07-b2o3-md-closure-retrospective 로 축 전체가 닫혔고 D-2026-09-08-b2o3-uma-vs-dft-force 로 힘 대조 카드가 비준됐다. Q 절의 RF-1("우리 MD 셀이 UMA 수용영역보다 좁다")도 D-2026-09-07-b2o3-cell-expansion-diagnostic 이 이미 전향적 카드로 받았다.
- **고치는 법**: 화면 상단에 원장 날짜와 오늘의 간격을 계산해 배지로 박는다(예: '13일 전 원장 · 이후 갱신 없음'). '오늘/내일' 어휘를 원장 날짜로 바인딩한다 — "2026-08-26 에 들어온 것" · "이 원장 이후 갱신 없음". v3 재편에서는 이 화면을 '하루치 로그'가 아니라 '최근 원장 + 이후 결정 원장 델타' 로 잇는 게 맞다(T·Q 항목이 그 뒤 어느 결정으로 흡수됐는지).
- codex 필요: False

### [P1·useless] ledger-value-pending-noise
- **어디**: `webapp/templates/ledger.html:124-125 (값 대기 배지) · 86-89 (요약 타일) · db/properties/tq_ledger_2026_08_26.json T 절`
- **근거**: T 표 17행 중 9행이 '오늘' 칸에 노란 '값 대기' 배지만 달고 있고 도구 칸도 '–' 다 (T5·T6·T7·T9·T10·T11·T13·T15·T16). 그중 둘은 애초에 채울 것이 없는 행이다 — T9 는 상태가 "✅ 완료(2026-07-28)", T10 은 "⛔ 폐기(2026-07-28)" 인데 둘 다 '값 대기' 를 단다. 한 달 반 전에 끝난 항목에 '내일 채워진다' 배지가 붙어 있는 셈이다. T16 은 무엇 칸이 아예 "(open_items 참조)" 라는 플레이스홀더고 상태는 "⏳" 뿐이다. 상단 요약 타일에도 "9 · '오늘' 칸 값 대기" 가 독립 타일로 나와 6개 타일 중 하나를 차지한다.
- **고치는 법**: 상태 접두가 ✅/⛔ 인 행은 '값 대기' 가 아니라 '해당 없음(종료)' 으로 그린다 — 이미 템플릿 각주가 "완료·폐기 항목은 채울 것이 없을 수 있다" 고 인정하는데 배지는 그대로 붙인다. 값이 있는 행을 먼저 정렬하고 값 없는 행은 접는다. T16 처럼 무엇 칸이 비어 있는 행은 원장 쪽에서 채우거나 빼야 한다 — 화면에서 가릴 문제가 아니다.
- codex 필요: False

### [P1·broken] gov-assessment-correction-blank-row
- **어디**: `webapp/templates/governance.html:210-225 · db/governance/assessments.json (A-2026-08-20-b2o3-framework-correction)`
- **근거**: 게이트 평가 표 4행 중 2행이 **완전히 빈 행**으로 렌더된다: "value:MD_Ea_eV/b2o3 | – | – | (빈칸)". 원인은 그 레코드가 `kind: "correction"` 이라 `gate`·`result`·`reason` 이 없기 때문이고, 템플릿은 `a.gate or a.slot`, `a.result or a.gate_outcome or a.outcome`, `a.reason or a.why_retracted or a.note` 만 읽는다. 정작 그 레코드가 들고 있는 것은 `what_was_wrong`("beta 를 잰 궤적과 값을 만든 궤적이 다른데 연결했다") · `second_error_corrected`(과교정 철회) · `third_error_corrected`("'high-T 궤적 9개 전부 부재' 로 적었다 — 실제 미보존은 6런") · `scope` · `evidence` 4건 · `reviewed_by` 다. 원장 자신의 _rules 는 "★ 정정도 산출물이다: correction 레코드는 범위·근거·대상 ID 를 갖고…" 라고 못 박는데, 화면에서는 그 산출물이 빈 줄이다.
- **고치는 법**: 템플릿에 correction 분기를 만든다 — 판정 칸에 '✎ 정정', 사유 칸에 what_was_wrong + second/third_error_corrected + scope, 아래 접힘 줄에 evidence. 겸사겸사 assessment_id·state·binding(bound / diagnostic_unbound)도 화면에 없다 — append-only 원장인데 화면이 레코드 ID 를 안 보여주면 '어느 판정을 말하는지' 를 못 가리킨다.
- codex 필요: False

### [P1·stale] gov-artifact-ledger-vintage
- **어디**: `db/governance/artifacts.json (_history 항목 1개) → webapp/templates/governance.html:162-200 · 34-44`
- **근거**: 산출물 원장은 12건이고 `_history` 에 든 항목이 "2026-08-20a: 신설. 오프라인 백업 2벌 + kgy + gabia 전수조사 결과를 기계 가독으로 옮겼다" 하나뿐이다. 19일간 추가된 게 없다. 그 사이 생산된 것들 — LPSOCl 3×3×1 400 ps 9런, SDCP C-12 번들, cascade 실행, 그리고 활성·비준된 힘 대조 카드가 입력으로 지목한 `arrhenius_6pt_traj/…/T700_s{2,3,4}` 궤적 — 은 파일에 문자열로도 없다(grep 결과 'arrhenius_6pt' 0건, 'box331' 0건, 'c12' 0건, 'sdcp' 0건). 화면 헤더는 "📦 산출물 원장 (12건 · 위험한 것부터)" 라 완결 목록으로 읽히고, 그 위 '🚨 데이터 위험' 카드는 "유일본(사본 1) 11건" 이라고 12건 중 11건을 위험으로 센다 — 실제로는 오프라인 백업 색인이라 그런 것이지 랩 산출물의 92 % 가 사본 하나라는 뜻이 아니다.
- **고치는 법**: 화면에 원장의 조사 시점과 범위를 한 줄로 박는다: "2026-08-20 전수조사 기준 · 이후 캠페인 미등재". 그리고 '데이터 위험' 카드 숫자에 그 범위를 붙인다. 등재 자체는 별건이지만, 최소한 화면이 '전부' 인 척하지 않게 한다.
- codex 필요: False

### [P1·broken] gov-evidence-deadend-kb
- **어디**: `webapp/templates/governance.html:134-138 · webapp/app.py:608-615 · webapp/data.py:4801-4811 (safe_repo_path, _ATT_ROOTS)`
- **근거**: 결정 22건 중 근거 문서가 클릭 가능한 것은 8건뿐이다(전부 db/properties/*.json). 나머지 14건은 회색 `<code>` 문자열로 끝난다 — kb 카드 12건(kb/projects/decision_registry_design_2026_08_20.md ×4, kb/questions/sdcp_backbone_polaron_estimand_2026_08_31.md ×2, kb/methodology/estimand_before_running_2026_08_28.md, kb/reviews/codex_N_estimand_discipline_2026_08_28.md, kb/reviews/codex_AI_prompt_current_head_2026_08_30.md, kb/questions/sdcp_doped_estimand_2026_08_28.md, kb/methodology/cascade_rerank_runbook_2026_08_25.md, kb/methodology/defect_cell_size_metric_2026_08_16.md) 와 조각 참조 2건(`…json#1_보고량`, `…json#3_오차예산.축_설계_제외_2026_09_03`). 실제로 `/api/file/kb/questions/sdcp_doped_estimand_2026_08_28.md` 를 치면 404 다(safe_repo_path 의 허용 뿌리가 docs·db 뿐). 그런데 같은 앱의 `/todo`(app.py:515-525)는 kb/open_items.md 를 doc.html 로 이미 렌더한다 — 능력이 없는 게 아니라 배선이 없는 것이다. 정책 결정 7건은 근거가 **전부** kb 카드라, 결정 원장에서 정책의 논거로 가는 길이 하나도 없다.
- **고치는 법**: kb 마크다운 전용 읽기 라우트(예: /kb/<path>)를 doc.html 로 붙이고 결정 표의 카드 링크를 그리로 보낸다. 조각 참조(`file.json#절`)는 파일 링크 + 절 이름 배지로 쪼갠다. 화면 docstring 의 '못 하는 것' 문구는 그때 같이 갱신한다.
- codex 필요: False

### [P1·buried] gov-no-entry-from-dashboard
- **어디**: `webapp/templates/index.html:6-14 · webapp/templates/base.html:72-79`
- **근거**: 렌더한 `/` 본문에서 `/governance` 링크가 **0개**다(사이드바 포함 전체 HTML 에 1회 = nav 항목뿐). `/ledger` 는 헤더 한 줄에 1회 나온다. 그 헤더 문구는 "v2: T·Q 원장 · T1b 힘 벤치 · β 문턱 폐기" 이고 템플릿 주석은 "v2 (2026-08-26) — 심포지엄 판독 T·Q 원장 + β 문턱 폐기 + T1b 힘 벤치가 들어간 판" 이다. 즉 대시보드가 '새 것' 으로 광고하는 것이 13일 전 화면이고, 그 뒤에 들어온 결정 원장 표(2026-09-08)는 광고도 링크도 없다. nav 위치도 '자료 · 기록' 절의 Files·Glossary·메모·미결 리스트 다음 다섯째 줄이다. 반면 09-08 비준 2건은 대시보드 핵심발견 카드로 이미 떠 있고(data.py:4640-4681) 카드 본문 끝에 "결정 원장 D-2026-09-08-lpsocl-box331-closure-conditions" 를 **평문으로** 적는다 — ID 를 말하면서 링크는 안 건다.
- **고치는 법**: 대시보드에 원장 요약 스트립을 올린다(결정 22 · 유효 18 · 제안 2 / 인용위험 25 · BLOCKED 4 / 산출물 유실 1). 핵심발견 카드의 결정 ID 를 /governance#<id> 로 링크한다(아래 앵커 항목과 짝). nav 에서는 판정 원장을 '자료 · 기록' 아래가 아니라 독립 절이나 상단으로 올린다 — 이 repo 에서 가장 자주 되돌아봐야 하는 화면이다.
- codex 필요: False

### [P1·ia] gov-decision-no-per-row-anchor
- **어디**: `webapp/templates/governance.html:98 (id="decisions" 카드 하나) · 112-153 (행 루프에 id 없음)`
- **근거**: 앵커는 카드 전체에 붙은 `id="decisions"` 하나뿐이고(헤더의 `href="#decisions"` 가 그리로 간다), 22개 행에는 id 가 없다. 그런데 결정 ID 는 repo 전체가 인용 단위로 쓴다 — webapp/app.py:560 docstring, data.py:4659·4681 의 대시보드 카드 본문, decisions.json 의 reopen_criteria 상호참조(D-2026-09-08-b2o3-uma-vs-dft-force 가 D-2026-09-07-b2o3-md-closure-retrospective 를 지목), citation_hazards·closure 기록 다수. 이름을 대는데 갈 곳이 없다.
- **고치는 법**: 각 `<tr>` 에 `id="{{ d.id }}"` 를 붙이고, statement·reopen_criteria 안의 `D-YYYY-MM-DD-…` 패턴을 같은 페이지 앵커로 자동 링크한다(결정끼리의 참조 그래프가 화면에서 걸어진다). 대시보드·kb 쪽 인용도 그리로 보낸다.
- codex 필요: False

### [P1·ia] gov-old-decisions-inline
- **어디**: `webapp/templates/governance.html:11 (절 순서 주석) · 98-159 (결정 표)`
- **근거**: 템플릿 주석이 순서를 "검증 → 데이터 위험 → 인용 위험 → 결정 → 산출물 → 평가" 로 선언했는데, 실제로 페이지의 절반을 먹는 결정 표가 25행짜리 인용위험 표 **뒤**에 온다(렌더 텍스트 602줄 중 결정 표가 195–481줄). 결정 표 안에서도 최신순 정렬만 있고 필터·접힘이 없어서, superseded 1건(D-2026-08-30-sdcp-neutral-ptfe-ddE-obs)과 retracted 1건(D-2026-08-16-face-height-gate)이 active 18건과 같은 굵기·같은 길이로 인라인 배치된다. 정책 7건은 전부 2026-08-16~28 것이라 사실상 상시 규약인데도 매번 캠페인 결정과 섞여 스크롤된다.
- **고치는 법**: ① 결정 표를 인용위험 위로 올린다(가장 최신·가장 자주 보는 원장). ② 종류별 탭 또는 칩 필터(정책 7 / 보고량 7 / 마감 3 / 게이트 3 / 지표 2 — 요약 줄에 이미 있는 수치를 그대로 필터로). ③ superseded·retracted 는 기본 접힘 + '옛 결정 2건 보기'. ⚠ 접되 DOM 에서 빼면 안 된다 — 아래 keep_as_is 참조. ④ 상시 규약(정책)과 캠페인 결정(보고량·마감·게이트)을 두 묶음으로 나눈다.
- codex 필요: False

### [P2·wrong] gov-green-banner-scope-unstated
- **어디**: `webapp/templates/governance.html:27-31 · webapp/app.py:637 (problems=validate_governance+validate_artifacts) · webapp/canonical.py:831`
- **근거**: 페이지 최상단 배너가 "✅ 원장 검증 통과 — 거버넌스·산출물 음성 체크 전부 통과." 다. 그 바로 아래가 '유실 1건', 그 아래가 BLOCKED 4건이 든 25행 인용위험 표다. 검사 함수 자신의 docstring 은 범위를 분명히 좁혀 놓았다: "⛔ 못 하는 것: 판정의 과학적 타당성은 안 본다. 그래프 무결성과 어휘만 본다."(canonical.py:831) 화면은 그 한정을 옮기지 않아서, 초록 도장이 페이지 전체 건강 신호로 읽힌다. 이 repo 가 /fairchem 화면에서 이미 경계한 실패형("합치면 200 인데 실행 실패한 튜토리얼이 '정상' 으로 보인다")과 같은 모양이다.
- **고치는 법**: 배너 문구에 검사 범위를 넣는다: "✅ 원장 구조 검증 통과 — 그래프·어휘 무결성만. 값·판정의 타당성은 검사하지 않는다." 그리고 그 옆에 실제 위험 카운터(BLOCKED n · 유실 n · 비준 없는 active n)를 나란히 둔다.
- codex 필요: False

### [P2·ia] gov-hazard-binding-unmarked
- **어디**: `webapp/templates/governance.html:62-65 · db/properties/citation_hazards.json`
- **근거**: 템플릿은 `{% set _cids = [h.claim, h.id]|select|join(' ') %}` 로 위험 행에 data-claim 을 건다. 실제 렌더된 HTML 의 data-claim 은 다섯 개뿐이다: HZ-beta-hard-gate · HZ-cross-system-Ea · HZ-lpsocl-Ea-diffusive-gate · MD_Ea_eV@b2o3(4회) · MD_Ea_eV_singleseed@b2o3. 원장 25건 중 `id` 가 있는 것은 3건, `claim` 이 있는 것은 1건이라 **21행은 결속 대상 자체가 아니다**. 화면은 25행을 전부 똑같이 그려서 어느 행이 기계 결속(다른 화면에서 그 문구를 쓰면 잡힌다)이고 어느 행이 사람이 읽어야만 하는 산문인지 구분이 안 된다. canonical.py:456-470 의 hazard_claims 도 id 없는 행과 RESOLVED 를 그냥 건너뛴다.
- **고치는 법**: 행마다 '결속됨 / 산문' 배지를 붙이고, 결속 안 된 행은 그 사실을 표시한다 — 없는 결속을 있는 것처럼 보이게 두지 않는 게 이 repo 규율이다. 그리고 자주 인용되는 위험부터 id·forbidden_phrases 를 채워 결속 대상으로 승격시킨다.
- codex 필요: False

### [P2·missing] cascade-seal-off-screen
- **어디**: `db/properties/cascade_seal_v2_2026_09_08.json (커밋 c221ac933, sealed_at 2026-09-08T14:41:28) — webapp/ 어디에도 참조 없음`
- **근거**: 오늘 만들어진 거버넌스 기록인데 화면이 하나도 없다. `grep -c cascade_seal db/governance/decisions.json` = 0, `grep -rln cascade_seal_v2 webapp/ db/governance/` = 결과 없음. 파일 자체는 `schema: cascade_prerun_seal/v1` · `label: v2_2026_09_08` · 코드 9개 sha256 + 규칙 5개 + "⛔_이_봉인이_보장하지_않는_것" 을 갖춘 정식 봉인이고, 커밋 메시지는 "이 시각 이후의 cascade 실행만 이 봉인에 귀속된다" 고 선언한다. 결정 원장 화면은 22건을 '전건' 으로 보여주지만 그 22건은 decisions.json 만이고, 봉인은 별도 스키마라 잡히지 않는다.
- **고치는 법**: 봉인을 결정 원장에 등재하거나(kind 를 하나 늘리거나), /governance 에 '봉인' 절을 만들어 label·sealed_at·미정 규칙 수·보장하지 않는 것을 편다. 최소한 D-2026-09-08-cascade-d-rel-estimand 행에서 이 봉인 파일로 가는 링크를 건다 — 지금은 보고량 카드는 화면에 있고 그 카드가 통제하는 실행의 봉인은 화면 밖이다.
- codex 필요: False

### [P2·ia] gov-prereg-column-mostly-blank
- **어디**: `webapp/templates/governance.html:109-129 (사전등록 칸) · db/governance/decisions.json (results_seen 이 있는 건 4건)`
- **근거**: '사전등록' 이 여섯 칸 중 하나를 통째로 차지하는데 22행 중 18행이 "– 미기재" 다. 값이 있는 4건은 전부 2026-09-07~08 것(b2o3-cell-expansion · b2o3-uma-vs-dft-force · lpsocl-box331-closure-conditions · cascade-d-rel). 한 행은 특히 어색하다 — D-2026-09-07-b2o3-md-closure-retrospective 는 record_kind 가 `retrospective`(2026-08-25 에 이미 닫힌 축을 09-07 에 기록)라 결과를 본 것이 확실한데 results_seen 이 원장에 없어 화면은 "– 미기재 / retrospective" 로 나온다. 미기재를 미기재로 적는 것 자체는 옳지만(그 정직성은 시험이 지킨다), 열이 82 % 비어 있다.
- **고치는 법**: 열을 없애지 말고 **행 안 배지**로 옮긴다 — 값이 있는 행에만 🔒/👁 를 제목 옆에 붙이고, 미기재는 표시하지 않는 대신 표 머리에 '사전등록 표시 4/22 · 나머지는 원장 미기재' 를 한 줄로 쓴다. ⚠ 이렇게 바꾸면 문자열 카운트로 검사하는 test_governance_missing_results_seen_is_unstated_not_prereg 가 깨진다 — 시험을 같이 옮겨야 한다(지우면 안 된다). retrospective 기록에 results_seen: true 를 넣을지는 원장 쪽 판단이다.
- codex 필요: False

### [P2·missing] gov-no-vocabulary-help
- **어디**: `webapp/templates/governance.html 전체 (glossary 링크 0) · 대비: webapp/templates/ledger.html:30-31·146-147 은 코드 체계 설명과 Q-로컬 경고를 절마다 박는다`
- **근거**: /ledger 는 처음 온 사람을 배려한다 — 헤더에 "kb/CODES.md — T=실행항목(전역) · Q=미해결질문(⚠문서별 로컬) · J=문헌대비축 · M=원고항목" 을 깔고, Q 네 절 머리마다 "⚠ Q 번호는 문서별 로컬 — 같은 Q3 이 문서마다 다른 뜻이다" 를 반복한다. /governance 에는 그런 게 하나도 없다. 화면에 아무 설명 없이 나오는 것들: '보고량'(툴팁 "원장 kind: estimand" 로만 원문 노출) · '사전등록 🔒 결과 보기 전' · '지문 🔒 일치' · 'ratification 없이 active 가 될 수 없다(원장 _rules)' · 게이트 평가 대상 칸의 `value:MD_Ea_eV/b2o3` 형식 · 산출물의 '검증 level = location_size / content / listing / search_exhausted'. /glossary 로 가는 링크도 없다.
- **고치는 법**: 결정 표 위에 4–5줄짜리 읽는 법을 둔다: 종류 다섯 가지가 무엇인지, 사전등록이 왜 이 repo 의 핵심인지(결과를 보고 규칙을 정하면 규칙이 아니다), 지문이 무엇을 막는지, 그리고 '이 표는 옳고 그름을 판정하지 않는다'(이미 표 아래 있는 문장을 위로). 용어는 /glossary 로 링크한다.
- codex 필요: False
