# v3 재편 계획 (전수조사 29 에이전트 · 552 발견)

## 한줄
이 repo 는 값을 지키는 규율은 잘 만들어 놨는데 그게 화면에 안 실린다 — v3 는 (1) 인용 금지를 화면·복사·API 세 군데 다 걸리게 하고, (2) 첫 화면을 "지금 살아 있는 것"으로 바꾸고, (3) 8월 이전 것은 지우지 말고 접는 재편이다.

## IA 제안
## 한 줄 진단

지금 IA 는 "하는 일" 순서로 묶여 있는데(결과 보기 / 계산 돌리기 / 문헌·검증 / 자료·기록), 정작 이 repo 가 굴러가는 축은 **"이 값을 써도 되나"** 다. 그 축을 담은 `/governance`(결정 22 · 인용위험 25 · 유실 1)는 다섯 번째 묶음의 다섯 번째 줄이고 대시보드 본문 링크가 0건이다. 그리고 멈춰 있는 감사 화면(`/cascade`, 회신 AL NO-GO)이 "계산 돌리기"에 들어 있다.

## v3 사이드바 (6묶음)

```
▦ 오늘                      ← 신설: 대시보드가 아니라 "지금 상태"
   Dashboard
   ⚖ 판정 원장   /governance      ← 5번째 줄에서 2번째 묶음 첫 줄로 승격
   📋 미결       /todo
   ✎ 기록       /log   ├ 메모 /notes  ├ 1저자 요청 /requests

▤ 값 (인용 전에 여기)
   Property Explorer  /explorer   ← "정본 값 진입점" 이라고 부제에 선언
   두 계 비교         /compare    ← 도구로 좁힌다 (표는 explorer 로 링크)
   주기율표           /elements
   Compositions                   ← family 로 묶음, 아래 참조

▧ 어떻게 쟀나
   Methods /methods · Glossary /glossary · Fair-Chem·UMA /fairchem · Benchmarks /benchmarks

🧪 캠페인 (상태 배지 필수)
   LPSOCl 3×3×1   [진행 · 400 ps 9런 · 닫힘조건 비준]
   SDCP           [wave1 닫힘 / C-12 진행]   ← /sdcp 와 /composition/sdcp 를 한 입구로
   Cascade        [NO-GO hold · 해제조건 4건 남음]  ← "계산 돌리기"에서 이동
   Nd/O 공치환    [DFT 재채점 중]

▣ 문헌
   Literature /literature  ├ 발표덱(7) ├ 서베이(2) ├ 축별 대조(A–L)

🗂 자료 · 보관 (기본 접힘)
   Files · T·Q 원장(2026-08-26 스냅샷) · Seminar(2026-08 발표 완료) · Nd 서베이(2026-07)
```

### Compositions 묶음 규칙
- 대시보드와 **같은** `FAMILY_ORDER` 로 묶는다(지금은 사이드바만 평면 14개).
- 정렬은 알파벳이 아니라 **활성 캠페인 먼저**: lpsocl · modelc · b2o3 · modelc_nd_doped · comp1 · comp2 → argyrodite 나머지 접힘.
- canonical 값 0 · 분석 파일 0 인 5개(comp3/comp4/comp5/modelc_v3/lic6)는 "계획됨(자료 없음)" 접힘 그룹. **지우지 않는다** — 캠페인 범위 선언이다.

## 라우트별 "위에 뭘 올리고 뭘 접나"

| 화면 | 맨 위로 | 접기 |
|---|---|---|
| `/` | 위험 배너(유실 1·유일본 11·인용위험 25) → 온보딩 4칸 → 이번 주 바뀐 것 3건 → **살아 있는 계약**(마감·보고량 카드) | 핵심발견 41장 → 축별 묶음, 축마다 최신 1장만 펼침 / SEI 절은 캠페인 페이지로 이동 / family 카드는 매트릭스에 흡수 |
| `/explorer` | 방법검증 앵커 4칸(우리 계산기가 얼마나 맞나) + 배지 범례 | SDCP_* 11열 = "분자계" 열 그룹 접힘, 비인용 축(σ비 3열)은 표 밖 별도 절 |
| `/compare` | 비교묶음이 성립하는 기본 선택(ICOHP_PS 또는 B0) | 해설 카드 4장 → 최신순 + 옛것 접힘, 상세는 `/concept/*` 로 |
| `/composition/<cid>` | 이 조성의 살아 있는 결정 스트립 + 결론 카드 | 구조 버튼 95개 → 대표 5개 + 폴더별 접힘, TODO 타일 벽은 "아직 없는 축 N개" 한 줄 |
| `/cascade` | 캠페인 지위 밴드(NO-GO · 보고량 · 남은 해제조건 · 봉인) → "지금 인용할 수 있는 것/없는 것" 표 | 심화 배지 = 접힘 규칙으로 통일, superseded 탭 4개는 접되 삭제 금지 |
| `/sdcp` | 마감 카드(확정값·허용 서술·금지 서술·재개 조건) + 30초 요약 | 비인용 원자료 표 264줄 접힘(현재는 요약이 391번째 줄) |
| `/governance` | 결정 원장(22건)을 인용위험 표 **위**로 + 종류 칩 필터 | superseded/retracted 2건 접힘 — 단 DOM 에서 빼면 전건 렌더 시험이 깨진다 |
| `/literature` | 이번 주 새 digest + MUST-READ + 발표덱 탭 | Excel 레거시 57행·보유 PDF 51행 접힘 |
| `/log` | 날짜 묶음 + 종류 칩(`/notes` 패턴 재사용) + 기록 없는 구간 표시 | handoff 94장 → 최근 10장 + 검색 |

## 전역 규칙 세 개

1. **접기는 되고 삭제는 안 된다.** 금지 서술·철회 이력이 카드 본문에 들어 있다. `<details>` 안 텍스트는 claim 스캐너가 그대로 읽으므로(canonical.py 의 SKIP 은 script/style 뿐) 접어도 결속 시험은 통과한다.
2. **손으로 쓰는 판 번호·요약은 반드시 낡는다.** `v2` 배지·"오늘 들어온 것"·"진행 중" 같은 문구는 전부 원장에서 파생시킨다. 이미 두 번 낡았다.
3. **사이드바 = ⌘K = 라우트 표는 한 곳에서 나온다.** 지금 사이드바 21개 vs 검색 15개로 갈려 `/governance`·`/ledger`·`/fairchem`·`/seminar`·`/requests`·`/sdcp` 6개가 검색에서 안 나온다. `webapp/nav.py` 하나를 단일 출처로 두고 짝 검사 시험을 붙인다.

## 충돌 방지 — data.py 구역 소유제

`webapp/data.py` 6242줄은 여러 묶음이 동시에 만진다. 구역을 못 박고 **자기 구역 밖은 읽기만** 한다. 새 함수는 자기 구역 끝 또는 새 모듈에.

| 줄 | 구역 | 소유 |
|---|---|---|
| 168–303 | SDCP wave1 게이트 | E |
| 358–378 | open_items 요약 | B |
| 442–556 | _PREFIX / structures_for / datafiles_for | D |
| 1052–1475 | canonical_values · 배지 · sei_* · canonical_table | C |
| 1476–2060 | cascade 상수·로더·계보 | E |
| 2101–2162 | icohp_for | D |
| 3086–3300 | talks · topics · list_papers | I |
| 3344–3408 | search_index | A (nav.py 위임) |
| 3410–3600 | compute_preview · 러너 | K |
| 3929–4745 | dashboard_highlights · 카드 생성기 | B |
| 4805–5140 | safe_repo_path · gallery | G/H (아래 표 참조) |
| 5334–5950 | 코멘트·형광펜·노트 | H |
| 5951–6073 | md_to_html | F |

`webapp/tests/test_webapp.py`(3193줄)는 **아무도 안 고친다** — 묶음마다 `webapp/tests/test_v3_<묶음>.py` 를 새로 만든다. 기존 시험을 옮겨야 하면 그 커밋만 따로.
CSS 는 A 단독 소유. 다른 묶음이 새 클래스가 필요하면 A 에 요청하고 그 전까지 기존 클래스/인라인으로 간다.

## 온보딩
## 지금 상태

처음 온 사람이 `/` 에서 만나는 첫 두 덩어리가 부제 한 줄과 "LPSOCl 3×3×1 닫힘 조건 비준 — 허용차 δEa 0.05 eV" 다. LPSOCl 도, 닫힘 조건도, δEa 도 설명이 없다. `grep "처음|시작하기|안내|여기서 시작"` 이 index.html·base.html 에서 **0건**. 카드 41장 26,672자 = 한국어 정독 89분짜리 화면이다.

## 5분 경로 설계

### 0–30초 · `/` 최상단
h1 바로 아래 **한 줄 정체**: "황화물 고체전해질을 계산으로 스크리닝한 기록입니다. 값보다 먼저 **그 값을 써도 되는지**를 봅니다."

그 밑에 **4칸 패널** — 숫자는 전부 db 에서 읽고, 숫자가 있으면 반드시 링크로 건다:

| 칸 | 숫자 출처 | 가는 곳 |
|---|---|---|
| 정본 값 N건 | canonical_registry.json (status=canonical) | `/explorer` |
| 인용하면 안 되는 것 25건 | citation_hazards.json | `/governance` |
| 지금 살아 있는 결정 N건 | decisions.json (state=active) | `/governance#<id>` |
| 용어 33개 | glossary.py | `/glossary` |

그리고 그 줄 위에 **위험 배너 한 줄**: "되돌릴 수 없는 데이터 유실 1건 · 사본 1개뿐 11건 → 판정 원장". 지금은 이게 홈에서 링크조차 안 된다.

### 30초–1분 · 표지 범례
카드 제목의 별·경고·금지 표시가 사실상 체계적으로 쓰이는데(비준 4장 · 주의 4장 · 철회 2장 · 교훈 2장) 뜻이 앱 어디에도 없다. "핵심 발견" 제목줄 옆에 한 줄 범례를 둔다.
값 표면(explorer/compare/composition)에는 **상태 배지 6종 + TODO + '—' + 비인용** 범례를 표 바로 위에 둔다. 손으로 쓰지 말고 `_STATUS_BADGE` 를 템플릿에 내려 자동 생성 — 화면마다 어휘가 갈리는 걸 막는 게 그 dict 의 원래 목적이다.

세 상태를 반드시 구분해서 가르친다:
- **TODO** = 아직 안 했다
- **N/A** = 이 계에는 성립하지 않는다 (예: 분자계에 주기 밴드갭)
- **비인용** = 했는데 못 쓴다 (원자료가 금지했거나 게이트 미평가)

지금은 셋이 같은 점선 회색 칸으로 뭉쳐 있어서, "분자계라 정의가 다름"과 "미계산"이 눈으로 안 갈린다.

### 1–2분 · "이번 주 바뀐 것" 3건
손으로 쓰는 `v2` 배지를 버리고 highlights 최신 3장(제목 + 날짜 + 그 카드 앵커)을 자동 생성한다. 지금 배지가 광고하는 T·Q 원장·T1b 벤치·β 문턱은 전부 2026-08-26 산출이고, 그 뒤 09-07~08 비준 3건은 광고도 링크도 없다.

### 2–4분 · 두 갈래 중 하나로
- **"값이 궁금하다"** → `/explorer`. 부제에 "정본 값 진입점"이라고 쓰고, **방법 검증 앵커 4칸**(UMA 힘 30.0 meV/Å 등)을 27칸 표 위로 올린다. 표의 숫자를 믿을지 말지 정하는 정보가 지금은 맨 아래다.
- **"뭘 조심해야 하나"** → `/governance`. 맨 위 초록 배너 문구에 검사 범위를 넣는다("원장 **구조** 검증 통과 — 그래프·어휘만. 값의 타당성은 검사하지 않는다"). 지금은 그 초록 아래에 유실 1건과 BLOCKED 4건이 이어져서 초록이 뭘 보증했는지 알 수 없다.

### 4–5분 · 용어
`/glossary` 에 **"연구 규율"** 카테고리를 신설해 최소 5장: 보고량(estimand) · 닫힘 조건 · 대조 잡 · 허용 서술 범위 · 사전등록·봉인. 이 repo 에서 제일 자주 쓰이는 개념인데 용어집에 정의가 0건이다(`grep "보고량\|estimand\|닫힘"` → 0). "우리 계산" 칸에는 `kb/templates/estimand_card.md` · `decisions.json` · `*_closed_*.json` 을 실제 사례로 링크한다.

## 안내 문구는 새로 짓지 말고 있는 걸 올린다

이미 잘 쓴 문장이 아래에 묻혀 있다 — 끌어올리기만 하면 된다:
- `/requests` 본문 5.3% 지점: "처음 읽는 사람은 §16 부터. b2o3 의 전도도가 왜 닫혔는지, 그럼 무엇이 남았는지를 용어 정의부터 풀어 썼다." → 헤더 배너로.
- `/cascade` 의 "이 페이지가 무엇인가" 카드와 기초/심화 배지 → 이 패턴을 `/benchmarks`·`/nd-survey`·`/explorer` 에 복제.
- `/sdcp/self-doping` 본문 → 배경지식 0 독자용으로 유일하게 제대로 쓰인 글. frontmatter 누출만 고치고 내용은 그대로.
- `/composition/*` 의 긴 판독 규율 문장(ELF 는 [0.40,0.60] 창 최솟값이다, COHP x눈금은 패널마다 다르다) → 이 앱이 지식 허브인 이유. **줄이거나 툴팁으로 접지 말 것.**

## P0 34줄
1. tools/doping/axis_corr_csv.py:115,159-166,663 — 09-08 비준 카드가 삭제한 0.90 게이트·|ρ|<0.2 실패조건을 아직 prereg 로 찍고 selftest 가 그 문구를 '있어야 통과'로 막는다 — 게다가 이 파일 sha256 이 cascade_seal_v2 에 봉인돼 있어 봉인이 철회된 문구를 보증하는 꼴이다
2. webapp/data.py:3908-3925 + webapp/app.py:447 — /api/element 가 /cascade 의 archive 게이트를 우회해 47종 rank·score·ox_V 를 그대로 내보낸다 — 사이트가 '승인 랭킹 0종'이라 쓰면서 순위를 배포하는 그 자기모순이고, 주기율표 33칸이 그 경로로 강조돼 있다
3. webapp/templates/explorer.html:70-73,126 — 셀 클릭 인용 복사가 레지스트리 status 를 빼고 복사한다 — 화면 배지는 '철회'인데 클립보드에는 '철회'도 'retracted'도 없이 b2o3 0.199 가 나간다
4. webapp/templates/composition.html:803-810 — copyComp 이 철회·잠정 배지를 안 싣고 '출처: … (canonical, 방법 표기 포함)' 꼬리를 붙인다 — 철회값이 정본 꼬리표를 달고 클립보드로 나간다
5. webapp/data.py:2115-2123 → webapp/templates/composition.html:213 — Nd ICOHP 표가 CUTOFF ARTIFACT 로 정정된 Li-S −2.493 / Li-Cl −2.265 를 경고 없이 찍는다 — 같은 페이지 아래 카드는 정정본 −1.647/−2.132 를 써서 한 화면이 자기를 부정한다
6. webapp/templates/compare.html:472-549 — 폐기된 β≥0.80 하드게이트를 판정으로 쓰고 'β가 낮으면 확산이 아니다 — 그 D는 인용 금지'라고 단정한다 — HZ-beta-hard-gate 는 SUPERSEDED 이고 우리 운영점에서 거짓탈락률 50 % 다
7. webapp/data.py:204,233-236 — SDCP wave1 인용 게이트가 키 모양 불일치(조각_시드 vs 조각)로 영원히 CITABLE 0 이다 — 원장에 dE_site_meV/ptfe_dimer_pm1=36.071 로 등록된 값을 화면이 '등록돼 있지 않다'고 말한다
8. webapp/templates/composition.html:24-63 (/composition/sdcp) — 조건부 보류된 절대 E_ads −0.7675 가 헤드라인 큰 글씨로 뜨고 보류 사유는 title= 툴팁 안에만 있다 — 같은 값을 /sdcp 는 빨간 배너 + 접힘으로 다루는데 두 화면이 정반대 지위를 준다
9. webapp/data.py:782-788 metric_meta 곱집합 — SDCP 분자 metric 11개가 전 조성 페이지에 TODO 로 찍힌다 — LPSCl 페이지가 PTFE 흡착에너지를 '미계산'으로 광고하고, 그것도 보류(HOLD)된 양이다
10. webapp/templates/cascade.html:205-215 — 2026-08-12 에 해소된 값 충돌을 '미해소'라는 빨간 제목 아래 띄우고(루프가 k.startswith('_CONFLICT')) 그 안에 파이썬 dict repr 이 이스케이프된 채 화면에 노출된다
11. webapp/templates/cascade.html:1488-1495 — 기본 화면에서 딥링크 핸들러가 r.cells[1] undefined 로 TypeError 를 내고, 같은 script 블록 뒤쪽 THEMES/TDOP 할당이 통째로 죽어 테마 탭 전체가 안 돈다 — 페이지가 스스로 뿌리는 48개 칩이 전부 그리로 간다
12. webapp/templates/cascade.html:1100-1171 — manifest 에 없는 v1 47종 champions 141행·litransport·synergy·themes 가 기본 DOM 에 전량 실린다 — 같은 파일을 /api/file 로 받으면 403 이라 다운로드는 막고 화면은 내보내는 상태다
13. webapp/templates/cascade.html 전체 — 회신 AL NO-GO(08-30)·09-08 보고량 카드 비준·cascade #7 봉인이 한 글자도 없다(화면 최신 날짜 2026-08-25) — 정작 대시보드에는 그 카드가 떠 있고 cascade 페이지만 자기 지위를 모른다
14. webapp/templates/index.html:117 + webapp/data.py:4050 — 'MP frozen-4f 값을 인용할 것'이 27일 낡았다 — 2026-08-12 에 우리 frozen-4f 3.948/3.698/0.770 으로 마감했고 MP 우회는 폐기됐다
15. db/properties/citation_hazards.json:54-58 — b2o3 MD Ea 가 CONDITIONAL 이고 fix 가 'FINAL_for_paper.Ea_eV_PAPER 만 인용'인데 그 키는 파일에 없다 — 09-07 비준 결정이 이 축 전체를 인용 불가(가능한 수 0개)로 마감했다
16. db/properties/canonical_registry.json:430,436,566,573 — 폐기된 blocking_gate 'beta_600K'/'beta_all_temps' 가 남아 화면이 '게이트 미통과'라고 찍는다 — 해제 조건이 원리적으로 충족 불가라 값이 영구히 잠긴다
17. webapp/canonical.py:280 gate_outcome — σ비 3항목의 verdict=not_assessed 가 lineage.gate_outcome 부재로 fail 렌더된다 — D-2026-08-20-no-retro-gate-without-artifact('미평가는 pending 이 아니다')와 정면으로 어긋난다
18. db/interphases/li3n.json:33,37 — 철회된 thin-slab UMA 경로의 0.049/0.054 eV 와 bridge_uma −0.032 가 표시 없이 살아 있다 — diffusion.json 은 같은 값을 CAVEAT_2026-06-06 으로 철회했고 CLAUDE.md 는 UMA-Li₃N 사용 금지다
19. tools/doping/run_md_sigma.py:16,239 + tools/ionic/hops_per_ion.py:21,110 — 철회된 Haven 0.3–0.7 과 '나누기 2 = 상한' 지시가 산출 JSON caveats 와 CSV 헤더로 나간다 — 실측 H_R=0.84±0.06 이고 부호가 반대(NE 는 과소)다
20. tools/figures/plot_cascade3.py:3,20,22 → docs/figures/cascade/cascade_conc_trends.png — 존재하지 않는 농도축으로 그린 그림이 배포 경로에 살아 있다 — x002/x005/x010 은 슈퍼셀 버그로 전부 x=0.25 인 배치 반복이고 같은 폴더의 plot_cascade_v23.py 가 그 사실을 적어 놨다
21. tools/modelc_v3/run_b2o3_md.sh:28-31 + disorder_ensemble_diffusion.py:321 + aimd_mlip.py:265 — MD 드라이버 기본 MSD 창이 5–40 / 2–20 ps 라 정본 2–50 이 아니고 --save_traj·--seed 도 없다 — convention_check 가 argparse default 를 안 봐서 '0 위반'으로 통과한다
22. tools/sdcp/site_screen.py:14,607 — 철회된 dE_extract +0.336 eV 부호가 '추출이 열역학적으로 불리함이 확인됐다'는 스크리닝 판정 규칙의 근거로 살아 있다 — 회신 P P0 가 그 부호를 철회하고 citable:no 로 강등했다
23. webapp/data.py:3581-3597 (_md_template) — /compute 가 내주는 MD 스크립트가 존재하지 않는 fairchem API(OCPCalculator)를 부르고 궤적 저장이 없다 — 바로 위 화면이 '--save_traj 없이 돌리지 않는다'고 굵게 가르치는데 그 화면이 만든 산출물이 그걸 어긴다
24. webapp/data.py:3482,3416 — Nd 계 경고가 VASP 키워드 ISPIN=2 를 QE 에 권하고 &SYSTEM 안 Hubbard 블록을 시키며 존재하지 않는 PP 이름을 준다 — 09-08 실측으로 gabia 의 Nd PP 는 frozen-4f 라 U 를 걸 대상이 없다
25. webapp/data.py:3487 — kgy/gabia 생성 입력의 pseudo_dir 이 './pseudo   # ← 교체' 로 주석이 Fortran 문자열 **안**에 있다 — QE 가 경로 전체를 리터럴로 읽어 세 서버 중 둘에서만 조용히 깨진다
26. kb/methodology/computational_methods_canonical.md:143-153 — '단일 기준'을 자칭하는 문서가 네 조성 MD Ea 를 비교표로 내고 '조성 간 비교 성립'이라고 권한다 — 레지스트리 기준 그 표는 철회 1·잠정 5 이고 cross_composition_ranking 이 금지돼 있다
27. kb/methodology/beta_gate_seed_policy.md:12,36,78 — 폐기된 β 0.8–1.2 하드게이트를 '규칙(이대로 집행한다)'로 두고 있고 tools/ionic 의 도구 2개가 이 카드를 선언 문서로 인용한다 — 폐기가 카드까지 안 내려왔다
28. kb/methodology/esp_z590_setup.md:78,92,114 — kgy 런타임을 'HPC-X mpirun 을 써야 한다'로 적어 09-08 에 세 번 틀린 바로 그 답을 준다 — 실측은 ~/apps/openmpi-4.1.6 이고 kb 전체에 ldd 규율이 0건이다
29. kb/open_items.md:10,30,75 + 섹션 머리 — 원장 맨 위가 'ORCA 8잡 실행 중'(09-07 실측은 프로세스 0개, gs0–gs3 미착수)이고 cascade '해제조건 7건 미이행'이 09-08 비준 4건을 모른다 — 다음 세션이 제일 먼저 읽는 문서가 제일 틀렸다
30. kb/projects/MUST_READ_digital_twin_north_star.md:61,136 — '첫 5분 안에 무조건 읽기'라는 2026-05-18 문서가 'Nd 서사 강화는 안티패턴'이라 가르친다 — 2026-09-03 교수 지침이 Nd/O 공치환을 1차 지침으로 지정했다
31. kb/papers/lpscl_vs_lpscl16_20min_script.md:33,58,79 — 폐기된 DOS-threshold 갭 1.76/1.82 를 결론으로 쓰고 'Figure caption 을 1.76 으로 수정하라'고 지시한다 — 같은 캠페인 마스터 문서가 그 값을 폐기하고 2.066/2.099 를 정본으로 박아 뒀다
32. litdb/comparison_vs_ours.md:115 — non_citable σ 비로 'σ를 깎지 않는(보존)·동등' 주장을 하고 600/800/1000 K 비를 'σ300' 으로 오표기한다 — 레지스트리가 그 metric 에 statistically_equivalent_transport·conductivity_preserved 를 명시적으로 금지했다
33. litdb/our_dem_baseline.md 부재 — DEM digest 84편·comparison_vs_ours_DEM 이 98곳에서 가리키는 기준값 파일이 이 브랜치에 없다 — DEM 트랙 전체가 기준점 없이 서 있다
34. webapp/app.py:151-178 (md_html) — kb frontmatter 15줄이 본문으로 렌더돼 /sdcp·/sdcp/self-doping 첫 화면이 'verifiedBy: …' 로 시작하고 목차 1번 항목이 된다 — kb_wiki 규약을 지킨 문서일수록 화면이 깨진다

## 이번 조사가 못 본 것
이번 조사가 못 본 것을 그대로 적는다.

**브라우저를 한 번도 안 띄웠다.** 화면 판단은 전부 서버 렌더 HTML 을 텍스트로 읽은 것이다 — 다크모드 실제 대비, 모바일 폭, JS 실동작(드래그 업로드·3D 뷰어·Plotly·⌘K 키보드), CDN 도달 여부, 인쇄 레이아웃은 확인 못 했다. 그래서 "다크에서 별표 결론 두 개가 사라진다" 같은 항목은 CSS 를 읽고 추론한 것이지 눈으로 본 게 아니다.

**litdb 크로핑 PNG 를 한 장도 안 봤다.** CLAUDE.md 는 litdb 를 볼 때 그림을 Read 로 같이 보라고 하는데, 이번엔 구조·인덱스·digest 텍스트만 봤다. 문헌 수치 판단에는 그만큼 구멍이 있다.

**바이너리 미열람** — kb/seminars 의 pptx 13개(23 MB), kb/reviews 의 docx 6개, kb/papers 의 pptx 1개. 어느 판이 실제 제출본인지는 파일 밖 기록으로만 추정했다.

**전수 아닌 표본** — kb 383개 중 본문을 읽은 건 60여 편(나머지는 frontmatter·목차·grep), db/properties 431개 중 30여 개, tools 526개 중 내용을 연 건 46개(doping 21개 · ionic 14개 · cascade 11개 전부의 본문은 안 봤다). comparison_vs_ours_DEM.md 3,190줄, kb/open_items.md 판정대기 786줄 중 약 660줄, REPORT_TO_COWORK.md 85 KB, docs/ 89개 md 는 통째로 안 봤다.

**시험은 통과를 전제로 삼았다.** pytest 178 passed 는 보고를 받은 것이고, 각 시험이 실제로 무엇을 얼마나 세게 잡는지는 표본(claim 결속 3종·게이트·manifest 위조)만 확인했다. 그래서 "이 시험이 지켜 준다"고 적은 항목 중 일부는 이름과 주석에 기댄 판단이다.

**성능·용량 숫자는 1회 측정** — /files 921 KB, /literature 955 KB, /cascade 557 KB, registry() 호출 수 같은 값은 한 번 재고 인용했다. 캐시 상태·머신에 따라 달라진다.

**repo 밖은 아무것도 확인 못 했다** — kgy·gabia·KISTI 의 실제 프로세스 상태, runs/ 하위 원자료 실물, 원격 경로 102개의 존재 여부. "지금 무엇이 돌고 있나"는 kb/projects/restart_runbook_2026_09_07.md 를 믿고 적었다.

**P0 목록은 중복을 접었다.** 원 조사 JSON 의 P0 severity 항목은 약 60건인데, 같은 결함이 여러 표면에 나타나는 경우(b2o3 MD 축 마감이 화면·kb·db 에 각각 반영 안 됨 등)를 한 줄로 묶어 34줄로 줄였다. 묶는 과정에서 어느 표면 하나가 목록에서 빠졌을 수 있다 — 구현할 때는 원 JSON 의 where 필드를 다시 훑어야 한다.

**안 한 판단 하나** — 이 조사는 "화면이 원장과 어긋나는가"만 봤고, **원장 자체가 물리적으로 맞는가**는 한 번도 검증하지 않았다. 값의 타당성은 여전히 미검사다.

## 묶음

### A. 셸·IA·온보딩 (단일 출처 nav)
- files: ['webapp/nav.py (신규)', 'webapp/templates/base.html', 'webapp/templates/_onboard.html (신규)', 'webapp/templates/_legend.html (신규)', 'webapp/static/css/style.css (전용 소유 — 다른 묶음은 요청만)', 'webapp/data.py:3344-3408 (search_index 만 — nav.py 위임)', 'webapp/tests/test_v3_nav.py (신규)']
- risk: base.html 의 접근성·조작 배선(skip-link, aria-expanded 동기화, rail 접기 FOUC 방지, ⌘K combobox/aria-activedescendant, Esc 우선순위)은 촘촘하게 맞춰 놓은 것이다 — 껍데기만 바꾸고 통째로 다시 쓰지 말 것. CSS 단독 소유라 여기가 늦으면 C·D 가 막힌다 → A 를 먼저 착수.
  - 사이드바를 6묶음(오늘 / 값 / 어떻게 쟀나 / 캠페인 / 문헌 / 자료·보관)으로 재편하고 /governance 를 두 번째 묶음 첫 줄로 승격
  - Compositions 를 FAMILY_ORDER 로 묶고 활성 캠페인 먼저 정렬 · argyrodite 나머지와 자료 0인 5개는 접힘
  - nav.py 를 사이드바·⌘K·라우트 라벨의 단일 출처로 만들고 data.py:search_index 를 거기에 위임 — 지금 빠진 6개(/governance /ledger /fairchem /seminar /requests /sdcp) 자동 포함
  - base.html 의 nav href 집합 ⊆ 검색 인덱스 url 집합 짝 검사 시험 신설(손으로 맞춘 두 목록은 반드시 또 갈라진다)
  - _onboard.html: 4칸 패널(정본값/인용금지/살아있는 결정/용어) + 위험 배너 한 줄 — 숫자는 전부 db 파생, 숫자가 있으면 링크
  - _legend.html: 카드 표지 범례 + 상태 배지 6종 + TODO/N-A/비인용 3구분 — _STATUS_BADGE 를 템플릿에 내려 자동 생성
  - 다른 묶음이 요청한 CSS 클래스 반영: [data-claim] 시각 표식(밑줄+금지 표시), .metric.na, 접힘 카드 clamp

### B. 대시보드 (/)
- files: ['webapp/templates/index.html', 'webapp/data.py:358-378 (open_items 요약)', 'webapp/data.py:3929-4745 (dashboard_highlights · _closure_and_prereg_cards · _nd_anneal_card)', 'webapp/data.py:2320-2332 (index_metrics/literature_count 한 함수만)', 'webapp/app.py:274-285 (index 라우트)', 'webapp/tests/test_v3_dashboard.py (신규)']
- risk: 카드 3장의 key(md_ea_ranking · lpsocl_box331_closure · ndo_lpscl16_anneal)는 시험이 제목이 아니라 key 로 집는다 — 바꾸거나 빼면 깨진다. 카드 본문에 금지 서술·철회 이력이 들어 있으니 접기는 되고 삭제는 안 된다. _closure_and_prereg_cards 의 'db 없으면 카드 안 만든다' 음성 시험을 유지 — 숫자를 템플릿에 박지 말 것.
  - 카드 41장에 축 태그(finite-size / beta / neb / gap / closure / screening) 부여 → 축별 묶음, 축마다 최신 1장 펼침 · 나머지 '이 축의 이력 N건' 접힘 (묶음 안 정렬은 최신순 유지)
  - v2 배지·부제의 손으로 쓴 요약을 버리고 '이번 주 바뀐 것 3건'을 highlights 최신 3장에서 자동 생성
  - 미결 카운트 정정: ### 항목이 취소선/완료 표시면 대기에서 빼고 '닫힘 8건'을 따로 센다(현재 47 중 8이 이미 닫힘, 실제 39)
  - index.html:117 + data.py:4050 의 Nd 갭 지시를 우리 frozen-4f 값으로 교체하고 표 행 이름에 (frozen-4f) 병기
  - 통계 4칸을 갈 데 있는 숫자로 교체(정본값→/explorer · 인용위험 25→/governance · 미결 39→/todo · 문헌→/literature) + 대시보드 218 을 /literature 215 와 같은 정의로 통일
  - 커버리지 매트릭스에서 cascade 열 제거(14칸 중 12칸이 —) + db/_index.json 스냅샷 날짜(2026-06-02) 명시 · 부제의 '실시간 동기화' 범위 좁힘
  - family 카드 14장을 매트릭스에 흡수(조성마다 링크가 2번씩 중복) · SEI 절은 index.html 에서 잘라내 E 에 넘김
  - 카드 본문의 결정 ID(D-2026-…)를 /governance#<id> 링크로 승격

### C. 값 표면 + 인용 안전 (explorer·compare·elements)
- files: ['webapp/templates/explorer.html', 'webapp/templates/compare.html', 'webapp/templates/elements.html', 'webapp/canonical.py', 'webapp/data.py:1052-1475 (canonical_values·배지·canonical_table)', 'webapp/app.py:313-343,402-427,447-452 (compare/elements/explorer/api_element 라우트)', 'webapp/tests/test_v3_values.py (신규)']
- risk: compare 의 domGroup/splitByGroup 비교묶음 강제는 절대 완화 금지 — 첫 로드에서 그림이 반쪽인 건 그 장치가 일하고 있다는 증거다. 고칠 것은 기본 선택이지 강제가 아니다. metric_meta 의 레지스트리 자동 생성과 explorer 의 파생 결속(data-claim={{key}}@{{cid}})도 손 목록으로 되돌리지 말 것. 배지는 하나만(레지스트리 status 우선) 규칙 유지.
  - citeVal/data-method 를 서버에서 status 포함으로 만들고 retracted/non_citable 은 복사 문자열 맨 앞에 금지 표시를 강제하거나 복사 자체를 막는다 — 회귀시험은 '철회 셀 복사문에 철회가 없으면 실패'
  - /api/element 에 /cascade 와 같은 archive 게이트를 걸어 rank/score/ox_V/E_GPa 를 ?archive=1 에서만 낸다 + 주기율표 범례를 'historical 스크리닝(superseded)'로
  - compare 의 β 카드 판정축을 D_inc plateau·창 안정성·홉 수로 다시 쓰고 β 표는 경보로 강등·접기 + data-claim=HZ-beta-hard-gate 결속
  - citable:false metric(σ비 3열)을 본 표에서 빼 '비인용 축(사유 포함)' 접힘 절로 — TODO(안 함)와 비인용(했는데 못 씀)을 같은 기호로 쓰지 않는다
  - explorer has.v 에 analysis_matrix 포함(vgcf_hbn·li3n 이 자료가 있는데 숨는다) + SDCP_* 11열을 분자계 열 그룹으로 접고 라벨/단위 채움 + 방법검증 앵커 4칸을 표 위로
  - compare 기본 activeKey/기본 선택을 비교묶음이 성립하는 축으로 교체(현재 첫 로드에서 막대 2개·레이더 미표시) + 칩에 '이 선택에서 몇 개 남는지' 표시
  - compare MSD 카드를 3×3×1·400 ps·9런·C1–C6 축으로 다시 쓰고 200 ps 곡선은 이력 접힘 — 상태·날짜는 decisions.json 에서 읽는다
  - 다크모드 3블록 color 지정 + plotBvse/msd3 에 plotlyFont/plotlyBG + themechange 재렌더 + var(--line) → var(--border)

### D. 조성 상세 + 구조·파일 목록
- files: ['webapp/templates/composition.html', 'webapp/decisions_view.py (신규 — 조성별 살아있는 결정 필터)', 'webapp/data.py:442-556 (_PREFIX·structures_for·datafiles_for)', 'webapp/data.py:2101-2162 (icohp_for)', 'webapp/app.py:286-312 (composition 라우트)', 'webapp/tests/test_v3_composition.py (신규)']
- risk: Bonding 카드의 긴 한국어 판독 규율(ELF 창·COHP x눈금·window_coverage·Bader 밀도 소스·std 큰 자리)이 이 화면이 지식 허브인 이유다 — 줄이거나 툴팁으로 접지 말 것. b2o3 캐스케이드 배너의 '같은 조성의 검증이 아니다' 상자와 그 시험, Charts 의 ^sig 기본 제외(σ 절대값 금지의 유일한 화면 강제), 3D 뷰어의 PS₄ 주기이미지 로직도 그대로.
  - copyComp 에 canonical_status 를 넣어 철회/잠정/비인용을 라벨 뒤에 강제 표기하고 대체값(retracted.usable_instead)까지 싣는다
  - icohp_for 가 _CORRECTION* 이 있으면 bonds_4.0A_cutoff_for_comparison 을 bonds 로 승격(원래는 bonds_superseded 로 접기) + 표 머리에 승격 표시
  - 구조 버튼 95개 → 폴더별 접힘 + 같은 stem 의 xyz/vasp/vesta 를 한 항목으로 묶기 + .vesta 는 3D 줄에서 분리해 다운로드로
  - _PREFIX 에 'ndo' 추가(09-08 Nd 어닐 6셀이 화면에서만 사라졌다) + li3n/lic6/sdcp 를 명시하고 vgcf_hbn↔li3n 소유 충돌 해소
  - 철회 status 타일에 취소선+회색 + 값 아래 본문에 '대신 쓸 값' 한 줄 + 타일 자체에 data-claim 부여(지금은 인용만 하는 페이지에만 결속이 있다)
  - metric 타일 상단에 '이 조성의 살아 있는 결정' 스트립(decisions.json applies_to 필터, /governance#<id> 링크) + 마감 조건 파일이 있으면 헤더 배지
  - 값 0개 조성 페이지에 '아직 계산 전 — 왜 목록에 있나' 한 줄 + TODO 타일 19개 접힘, Charts 칩 라벨을 kind 대신 파일 stem 축약으로
  - 본문 하단 '더 보기' 줄 신설(/methods · /governance · /files?q=<cid> · /explorer · /todo) + metric 타일에 source_path·updated 표시
  - bader note 셀의 _comparison_bader Undefined 가드(현재는 우연히 500 이 안 날 뿐)

### E. 캠페인 감사 (cascade · SDCP)
- files: ['webapp/templates/cascade.html', 'webapp/templates/cascade_diagnostic.html', 'webapp/templates/_campaign_band.html (신규)', 'webapp/app.py:344-401,463-514 (cascade·sdcp 라우트)', 'webapp/data.py:168-303 (SDCP wave1 게이트)', 'webapp/data.py:1476-2060 (cascade 상수·로더·계보)', 'webapp/tests/test_v3_cascade_sdcp.py (신규)']
- risk: fail-closed 게이팅 3종(archive=1 / view=diagnostic / manifest 미등록=403)은 Codex 가 두 번 잡아 만든 장치다 — '경고 배너 붙이고 DOM 에는 싣기'로 되돌리면 같은 사고가 재발한다. FORBIDDEN 주석쌍, data-claim-not 부인 래퍼, superseded 탭 4개, '회수로 뒤집힌 서술' 카드는 이동은 되고 삭제는 안 된다. /sdcp 의 접힌 원자료 20건도 그대로 둔다(3일짜리 외주 배치를 다시 돌리게 만드는 게 최악).
  - 타일 아래에 캠페인 지위 밴드 신설: 회신 AL NO-GO(08-30) · 비준 보고량 D_rel(600 K·2–50 ps·cell-conditioned) · 남은 해제조건 #3·#4·#7·#8 · 봉인 v2_2026_09_08 — 값은 _closure_and_prereg_cards 가 읽는 JSON 재사용(하드코딩 금지)
  - _CONFLICT 루프를 _CONFLICT_UNRESOLVED 로 좁혀 해소분을 회색 접힘으로 내리고 dict repr 누출 제거 + 근거 없는 '전부 잠정' 꼬리말 삭제
  - 딥링크 블록에 r.cells.length 가드 + try/catch, 게이트 안내 행을 tbody 밖으로 — 지금은 이 한 줄이 테마 탭 전체를 죽인다
  - archive 게이트를 ranked 뿐 아니라 champions·litransport·synergy·themes.dopants 까지 확장하고, 화면에는 '보관함 열기' 버튼만 남긴다 (게이트 완화가 아니라 확장)
  - 게이트가 걸린 자리에서 숫자 대신 '가려짐'을 찍는다(archive_gated/diagnostic_gated 플래그 사용) — 없는 것을 0 으로 표시하지 않는다
  - |bold 필터 누락 8곳(리터럴 ** 48회) + 렌더 본문에 ** 가 0회일 것을 회귀시험으로
  - 기본 탭 순서를 뒤집는다: 인용 가능/불가 표 → 지위 밴드 → 감사 그림 → 축별 완성도, 심화 배지 = 접힘 규칙으로 통일 (현재 그 표는 탭 35,826바이트 중 34,837 지점)
  - SDCP 게이트 키 모양 정합(시드별 게이팅 권장) + UNKNOWN 배지 색을 위험색으로 + hazard 결속을 조각 이름이 아니라 원장 파일 경로 기준으로 + 양성 시험 신설
  - /sdcp 순서 뒤집기: 마감 카드(확정값·허용/금지 서술·재개 조건) → 30초 요약 → 비인용 원자료 접힘, 그리고 진행 중인 C-12 링크 신설
  - index.html 에서 넘어온 SEI 절을 캠페인 페이지로 받되 unreadable 분기 두 개를 그대로 옮긴다

### F. 마크다운 렌더 + 문서·용어 표면
- files: ['webapp/app.py:88-233 (_mdlite·md_html·_bind_claims·_sanitize_urls·_bold)', 'webapp/data.py:5951-6073 (md_to_html)', 'webapp/templates/doc.html', 'webapp/templates/concept.html', 'webapp/templates/glossary.html', 'webapp/glossary.py', 'webapp/app.py:454-462,488-514,1193-1240 (methods/self-doping/glossary/concept 라우트)', 'webapp/tests/test_v3_markdown.py (신규)']
- risk: 볼드 가드 3개(코드 스팬 선격리 · 300자 상한 · 여는 별표 뒤 닫는 문장부호 배제)는 globstar 사고에서 나왔다 — 우회하거나 순서를 바꾸지 말 것. md_html 의 raw HTML 차단과 URL scheme 화이트리스트는 litdb digest 가 외부 PDF 요약이라 필요하다. glossary 의 '문헌에서 본 것' 칸 분리와 data-claim 결속 span 도 유지.
  - _mdlite 에 취소선(~~) 추가 — 코드 스팬 격리 뒤에, 볼드 가드 3개 순서 유지
  - 이탤릭(*…*) 추가하되 단어경계 요구 — 음성 픽스처에 'D*(design) / D*(host)' 를 반드시 넣는다(실측 유일 충돌)
  - _mdlite(0) 이 빈 문자열을 내는 버그 수정 — 실측 0 이 화면에서 사라져 결측으로 보인다
  - md_html 진입부에서 YAML frontmatter 스트립 + 뗀 updated/status/confidence 를 헤더 배지로 되살림
  - heading slug id 생성(python-markdown toc slugify, 한글 보존) — compare 의 /concept/dft#12 계열 죽은 앵커와 앞으로 생길 §링크가 한 번에 산다
  - md_to_html(세미나 경로)도 _bind_claims 를 타게 하거나 md_html 로 통합 — 지금 /seminar 만 결속 밖이다
  - doc.html 에 sticky 목차 + 검색(seminar.html 의 buildToc 재사용) + data_first 스위치(=/sdcp 가 순서를 뒤집을 수 있게)
  - 글로서리에 '연구 규율' 카테고리 신설 5장(보고량·닫힘 조건·대조 잡·허용 서술 범위·사전등록·봉인) + 카드에 id 부여로 /glossary#beta-gate 앵커 살리기 + 카드 내부 상호참조를 같은 페이지 앵커 링크로
  - glossary 검색 색인에 how/ours/lit 추가('b2o3' 10장 중 1장, '철회' 6장 중 1장만 걸리는 상태) + neb 카드 3986자를 개요+더보기로 분할
  - claim-flag 툴팁의 마크다운 별표 제거

### G. 원장 화면 (governance · ledger · kb 뷰)
- files: ['webapp/templates/governance.html', 'webapp/templates/ledger.html', 'webapp/app.py:515-737 (todo·requests·governance·ledger 라우트)', 'webapp/data.py:4805-4830 (safe_repo_path·_ATT_ROOTS)', 'webapp/app.py 신규 라우트 /kb/<path>', 'webapp/tests/test_v3_governance.py (신규)']
- risk: 지문 3상태(없음/일치/불일치)와 '– 미기재'를 기본값으로 메우지 않는 규율, 그리고 그것을 문자열 개수로 잠그는 시험은 그대로. 시험이 글자 그대로 집는 문구 다섯('🔒 일치' · '본문이 승인 뒤 바뀌었다' · '◻ 미평가' · '미평가는 실패가 아니다' · '철회된 옛 판정')을 다듬으려면 시험을 같은 커밋에서 옮겨야 한다. safe_repo_path 를 넓힐 때 메모 대상 화이트리스트(_NOTE_DOC_DIRS)와는 계속 분리한다.
  - 결정 표를 인용위험 표 위로 올리고 종류 칩 필터(정책 7/보고량 7/마감 3/게이트 3/지표 2) + superseded·retracted 기본 접힘 (DOM 에서 빼면 전건 렌더 시험이 깨진다 — CSS/details 로만)
  - 각 <tr> 에 id={{d.id}} 부여 + statement·reopen_criteria 안의 D-YYYY-… 패턴 자동 링크로 결정 참조 그래프를 화면에서 걷게 한다
  - kb 마크다운 읽기 라우트(/kb/<path>)를 doc.html 로 붙이고 근거 문서 14건(kb 카드)의 죽은 회색 코드 문자열을 링크로 — /todo 가 이미 kb md 를 렌더하니 능력이 아니라 배선 문제다
  - correction 레코드 분기 신설 — 지금 게이트 평가 표 4행 중 2행이 완전히 빈 행이고 what_was_wrong/evidence 가 화면에서 사라진다
  - 초록 배너 문구에 검사 범위 명시('원장 구조 검증 — 그래프·어휘만')와 실제 위험 카운터(BLOCKED n · 유실 n · 비준 없는 active n) 병기
  - 인용위험 행에 '결속됨 / 산문' 배지 — 25건 중 id 있는 건 3건뿐인데 화면은 25행을 똑같이 그린다
  - /ledger 상단에 원장 날짜와 오늘의 간격 배지(13일 전) + '오늘/내일' 어휘를 원장 날짜로 바인딩 + 종료(✅/⛔) 행의 '값 대기' 배지를 '해당 없음'으로
  - 결정 표 위 4–5줄 읽는 법(종류 다섯 · 사전등록이 왜 핵심인지 · 지문이 무엇을 막는지) + /glossary 링크
  - 봉인 절 신설 또는 cascade 결정 행에서 cascade_seal_v2 로 링크 — 지금 봉인은 화면 밖이다

### H. 기록 화면 (log · todo · requests · notes · files)
- files: ['webapp/templates/log.html', 'webapp/templates/notes.html', 'webapp/templates/files.html', 'webapp/templates/requests.html', 'webapp/app.py:1035-1061,1231-1300 (notes·files·journal·handoff)', 'webapp/data.py:5045-5140 (gallery)', 'webapp/data.py:5334-5950 (코멘트·형광펜·노트)', 'webapp/tests/test_v3_records.py (신규)']
- risk: 메모 77건·형광펜 19건의 글은 한 글자도 지우지 않는다(대상 파일이 사라진 1건도 '대상 없음' 표시만). 딥링크 규약(note_url → ?note=<id> → docnote 앵커 복원)은 이 화면의 유일한 강점이라 그대로 가져간다. 쓰기 잠금 기본값 로직(로컬 열림/Render 잠금)은 건드리지 말고 표시만 고친다. kb/results 94개 파일은 목록을 접는 것이지 삭제가 아니다.
  - /log 상단 SDCP 카드의 숫자 셋을 원본 explainer 의 판정문으로 교체(게이트 30→0 은 INCAR 불일치였고 게이트는 0/30→17/30 · basin 50 meV 는 진단값이지 측정 아님 · 0.1 meV 정확도 주장 금지)
  - journal 을 ts 기준 정렬 + 날짜 묶음 + 종류 칩 필터(/notes 패턴 재사용, 새로 짜지 말 것) + 기록 없는 구간을 '2026-08-26~09-07 · 기록 없음(커밋 806)' 회색 줄로 명시
  - handoff 격자 94장 → 최근 10장 펼침 + 나머지 접힘, 정렬을 파일명 역순에서 날짜순으로, 카드에 날짜·조성·첫 문장
  - /files 카드에 hazard 배지(canonical.hazard_claims 재사용) + SUPERSEDED/RETRACT 파일명은 '옛 판' 탭으로, 모달 CSV 의 규율 주석(DO NOT QUOTE·NOT ASSESSED)을 details 밖 경고 상자로
  - /files 403 파일 132개에 상태 표시 + 모달 fetch 에 r.ok 검사(지금은 403 JSON 을 CSV 표로 그린다) + 날짜 출처를 mtime(=체크아웃일)에서 git 커밋일로, 못 얻으면 '날짜 미상'
  - facet 상태 유지 수리(검색하면 kind/folder 가 사라진다) + PDF 탭 신설 + 죽은 cmt 탭·rename 버튼 정리
  - /notes 헤더에 '마지막 메모 8일 전' 표시 + 형광펜 19건을 같은 타임라인에 편입 + note-image 렌더를 comments.js 와 같은 화이트리스트 규칙으로
  - READ_ONLY 를 템플릿에 내려 배포판에서 저장 폼을 비활성화하고 서버가 준 사유(why/how)를 그대로 표시
  - /todo 부제에 '⏭ 바로 이어서 할 것' 추가 + 문서 최종 갱신일과 decisions.json 최신 비준일을 나란히 찍는 신선도 줄

### I. 문헌 (literature · talks · paper)
- files: ['webapp/templates/literature.html', 'webapp/app.py:820-842,1078-1131 (literature·api_paper·talk 라우트) + 신규 /paper/<slug>', 'webapp/data.py:3086-3300 (talks·topics·list_papers·read_csv)', 'litdb/README.md', 'litdb/INDEX.md', 'litdb/INDEX_DEM.md (재생성)', 'webapp/tests/test_v3_literature.py (신규)']
- risk: digest 본문 219개가 이 영역의 전 재산이다 — 줄이거나 요약본으로 갈아치우지 말 것. 발표덱 인용등급 경고('논문 수에 합산하지 않는다 · 소환값보다 한 단계 낮다 · 부재의 증거가 아니다')는 노출을 올릴 때 반드시 같이 움직인다. __seminar 제외 규칙과 정렬 tie-breaker(digest 날짜 없는 2편이 사라지지 않게)도 유지. litdb/figures 의 figures.json·_sources.json 은 복원 경로라 절대 삭제 금지.
  - 기본 정렬을 digest 날짜 내림차순으로 뒤집고 '최근 30일 새로 들어온 것' 스트립 신설 — 지금 09-08 digest 두 편이 148·197번째다
  - digest 에서 인용금지 블록을 파싱해 카드에 제한 배지 + 그것만 거르는 칩(219편 중 80편이 인용 제한을 달고 있다)
  - 뼈대 5편에 '인용금지' 배지 + 기본 그리드에서 접기, evidence_level 오표기(fulltext) 정정, 헤드라인 카운트는 완성 digest 만
  - 발표덱 탭 신설 + 카드에 id 부여(검색 앵커가 지금 아무 데도 안 걸린다) + 발표덱 묶음을 논문 그리드 위로, 인용등급 경고 callout 을 그 묶음에 붙여서 같이 옮긴다
  - /paper/<slug> 전체 페이지 라우트 신설(digest 가 58–63 KB 인데 모달만 있다) + /talk 과 같은 목차·형광펜 경로
  - 캡션 색인 279 KB 를 DOM 속성에서 빼 서버 검색 또는 별도 JSON 으로 — 페이지 899 KB 의 3분의 1이다
  - 우리 논문 2편에 '자체·공저' + 미출판이면 '투고본' 배지 + 전용 칩
  - litdb/README 구조표를 실물에 맞춰 다시 쓰고(DEM 트랙·talks·surveys·topics.json 누락, 없는 properties/ 2곳) INDEX 머리말의 '0편'·'64/64 편입' 같은 고정 숫자를 --check 참조로 교체 + INDEX_DEM 재생성
  - gloss/caution(손 큐레이션 22줄)을 카드 툴팁·모달 머리에 실제로 렌더 — 지금은 계산돼서 버려진다

### J. db 원장 정합 (파일만 — 화면 안 건드림)
- files: ['db/properties/citation_hazards.json', 'db/properties/canonical_registry.json', 'db/governance/decisions.json (status/ratification 없는 항목만)', 'db/governance/artifacts.json', 'db/governance/assessments.json', 'db/_index.json', 'db/interphases/li3n.json', 'db/README.md (신규)']
- risk: ★ ratification.content_digest 가 박힌 카드 8건(b2o3 3 · lpsocl 1 · cascade 1 · sdcp c12 2 · polaron S0 1)은 본문을 한 글자도 고치면 안 된다 — 8/8 지문이 지금 일치하고, 오탈자 하나만 고쳐도 19건의 승인이 무효로 보인다. 사전등록 파일(prereg_d_rel 등)도 사후 편집 금지 — SUPERSEDED 표시만 붙이고 값은 그대로. 기계 필드명(kind:"estimand", canary_geometry)은 개서 금지.
  - b2o3 MD Ea hazard 를 CONDITIONAL→BLOCKED 로 올리고 없는 키(FINAL_for_paper.Ea_eV_PAPER) 지시 삭제 + D-2026-09-07-b2o3-md-closure-retrospective 결속
  - hazards 25건 전부에 안정 id(HZ-<slug>) 부여, 수치 위험은 claim(<metric>@<system>), 산문 위험은 forbidden_phrases — 지금 결속 가능한 건 3건뿐이다
  - 새 hazard 신설: σ비 non_citable(b2o3_vs_lpscl16_conductivity.csv, 금지문구 '동등/보존/σ300') · 단일시드 1.33×(CLAUDE.md 가 이름 대는 철회인데 스캐너가 못 잡는다) · Nd 어닐 UMA 순위(DFT 재채점 전) · UMA-Li₃N 금지 · β 하드게이트에 'β<0.8' 변형 추가
  - 레지스트리의 폐기된 blocking_gate(beta_600K/beta_all_temps)를 도달 가능한 조건으로 교체하고, σ비 3항목에 lineage.gate_outcome=not_assessed 를 넣어 fail 오역을 막는다
  - provenance_open 을 provenance_state(open/resolved/permanently_unresolved) + note 로 분리하고 comp1(해소)·modelc(영구 미해소) 문구를 세 곳에서 하나로 통일
  - _history/changelog/_changelog 세 이력 키를 하나로 병합(가장 최신 09-08 BH③ 회수 기록이 아무도 안 읽는 키에 혼자 있다)
  - li3n.json 의 철회된 UMA 값 두 개에 diffusion.json 과 같은 철회 표기 또는 참조 한 줄로 교체
  - db/_index.json 최상위에 STALE 경고 + 인용 금지된 절대 σ·단일시드 Ea 헤드라인 격리, artifacts/assessments 의 '2026-08-20 진행 중' 두 건을 09-07 마감 결정으로 종결
  - db/README.md 10줄 신설: 값 인용 순서(registry → hazards → decisions) · 검증 명령 · _index.json 은 근거가 아니다 · 문헌 정본은 litdb

### K. 도구·계산 규율 (tools + /compute)
- files: ['tools/doping/axis_corr_csv.py', 'tools/doping/run_md_sigma.py', 'tools/ionic/hops_per_ion.py', 'tools/ionic/plot_msd_3sys.py', 'tools/ionic/plot_arrhenius.py', 'tools/ionic/build_final_conductivity.py', 'tools/figures/plot_cascade3.py', 'tools/figures/house_style.py', 'tools/modelc_v3/run_b2o3_md.sh', 'tools/modelc_v3/disorder_ensemble_diffusion.py', 'tools/modelc_v3/aimd_mlip.py', 'tools/electronic/run_comp2_saddle_check_kgy.sh', 'tools/sdcp/site_screen.py', 'tools/convention_check.py', 'webapp/templates/compute.html', 'webapp/data.py:3410-3600 (compute_preview·러너)', 'webapp/app.py:428-446']
- risk: QE-GPU ldd 러너 블록은 같은 자리에서 세 번 죽고 얻은 것이다 — '보기 싫으니 한 줄로'는 네 번째 사고를 부른다. 규율 카드의 괄호 안 사례(12런·21런이 궤적 없이 끝났다)는 접기만 하고 삭제 금지. compute_preview 의 fail-closed 두 갈래(sdcp→ORCA 안내만, li3n+md→금지)는 없애지 말고 확장. 봉인 재발행은 J 와 순서를 맞춰야 한다.
  - axis_corr_csv 의 prereg 생성 블록을 09-08 비준 카드 §1·§3 으로 교체(0.90 게이트·|ρ|<0.2 삭제, CI 3분 판정)하고 selftest 의 양성 단언을 '삭제된 문구가 나오면 실패'로 뒤집는다 → 그 뒤 cascade_seal 재봉인
  - MSD 창 기본값을 2–50 으로 통일하거나 필수 인자로 강제 + convention_check 에 argparse default 패턴 추가(지금 0 위반은 검사기가 못 보는 것)
  - Haven 0.3–0.7·'나누기 2' 문구를 세 파일에서 제거하고 실측 H_R 0.84±0.06(부호 반대)로 교체 + hops_per_ion.csv 재생성
  - plot_cascade3.py 에 철회 배너 + cascade_conc_trends.png 를 배포 경로에서 내림(스크립트는 남긴다)
  - run_comp2_saddle_check_kgy.sh 의 hpcx 자동탐지를 run_force_check_scf.sh 의 ldd 유도 블록으로 교체하고 그 블록을 공용 함수로 추출
  - /compute 의 MD 스크립트 생성을 버리고 정본 러너(run_arrhenius_6pt.sh → disorder_ensemble_diffusion.py, --save_traj·--fit_window_ps 2 50 포함)를 붙여넣기 블록으로 낸다
  - pseudo_dir 주석을 문자열 밖으로 + Nd 경고를 PP 조건부(frozen-4f 면 U 거부)로 + PSEUDO_LIB['Nd'] 를 실물 이름으로 + KISTI 러너에 랭크 수 지정
  - COMPUTE_SETTINGS 에 없는 조성 6개는 폴백을 없애고 _none 갈래로(지금 존재하지 않는 cif 경로로 입력을 만들어 준다)
  - 규율 카드에 0번 규율 신설(입력을 만들기 전에 보고량 카드·게이트가 정해졌나 + /governance 링크)하고 도구를 카드 위로 올린 뒤 규율은 선택에 따라 자동 펼침
  - site_screen.py 의 dE_extract 부호 근거를 기하 판정으로 다시 쓰고 철회 사실을 docstring 에 명시
  - tools/<dir>/INDEX.md 를 docstring 첫 줄에서 생성(526개 중 338개가 kb 에서 이름이 안 불린다)

### L. kb·repo 문서 정합
- files: ['CLAUDE.md', 'AGENTS.md', 'README.md', 'kb/SCHEMA.md', 'kb/CODES.md', 'kb/open_items.md', 'kb/methodology/*.md (beta_gate_seed_policy · computational_methods_canonical · terminology_register · esp_z590_setup · electron_localization_framework · md_axis_status)', 'kb/results/*.md (b2o3 6편 · ionic 3편 · MASTER)', 'kb/projects/MUST_READ_digital_twin_north_star.md', 'kb/papers/lpscl_vs_lpscl16_20min_script.md', 'kb/templates/estimand_card.md', 'tools/kb_wiki.py', 'litdb/comparison_vs_ours.md']
- risk: 회신 원문(kb/reviews/*reply*)과 발송된 프롬프트 본문은 고쳐 쓰지 않는다 — frontmatter status 와 문서 상단 후주만. 철회·자기정정 블록(cascade_pipeline_anatomy 의 '앞 절 정정', beta-gate §7-2, msd_sampling §5 반론 절)은 재배치는 되고 삭제는 안 된다. kb/index.md 는 생성물이라 손편집 금지 — 고칠 것은 생성기다. explored: 는 사람만 true 로 바꾼다.
  - CLAUDE.md 맨 위에 '여기서 시작' 6줄(상태=open_items ⏭ / 판정=decisions.json / 값=canonical_registry / 금지=citation_hazards / 리뷰=kb/reviews/INDEX.md / 화면=webapp) + 화면(webapp)·claim 결속 규율 절 신설 + research-agent 블록을 research-agent/CLAUDE.md 로 분리
  - AGENTS.md 를 CLAUDE.md 포인터 한 줄로(5일 만에 5개 절이 갈렸고 .opju 항목은 정반대를 말한다)
  - kb/open_items.md ⏭-0/⏭-2/⏭-3 을 09-07 실측·09-08 비준으로 갱신하고 D_rel 주기준까지 비준 카드로 교체(지금 반쪽만 취소선) + 닫힌 8건을 ✅ 절로 실제 이동
  - beta_gate_seed_policy 에 SUPERSEDED 배너(도구 2개가 이 카드를 선언 문서로 인용한다) · esp_z590_setup 의 HPC-X 지시를 ldd 규칙으로 · computational_methods_canonical §6 표에 status/HOLD 열과 gen0 영문 각주 · terminology_register 에 09-01 용어 3쌍 추가
  - kb/results 의 b2o3 MD 카드 6편·σ 4배 카드 5편에 축 마감/철회 배너(값은 보존, 배너만) + kb/results README 를 계별 지도로 신설
  - MUST_READ 를 2026-05 아카이브로 강등하고 north-star 역할을 restart_runbook + 09-03 교수 지침으로 넘김 · README.md 를 15줄 진입 문서로 축소
  - estimand_card 템플릿의 철회된 '일곱 번은 안 돌려도 됐다' 문장을 회신 N 문구로 교체 + 산문 용어를 '보고량'으로(파일명·kind 필드는 그대로)
  - kb_wiki.py: reviews 정규식에 internal_ 포함 + 판정 인용 패턴 확장 + reviews/INDEX.md 신선도 검사 + index 생성기에 updated/status 표시와 최신순 정렬 + explored 마크 반전 + fairchem 을 MANAGED 에 추가
  - kb/reviews/INDEX.md 재생성 + '안 닫힌 것'(미회신 / 이행 미완) 절을 맨 위에 + BG·BH status 정정 및 회신 원문 복원 · 라벨 중복(BG/BH) 해소
  - litdb/comparison_vs_ours.md:115 의 σ 동등·보존 주장을 레지스트리 allowed_sentence 로 교체 + β 하드게이트 3곳 · gap 2.098 5행 정정
  - kb/CODES.md 에 회신 letter 체계(A–BI) 절 추가 + J-8 축

## Codex 회부 후보
- cascade 비준 카드의 §4 허용 서술 · §5 금지 서술 · §6 구조적 공백('MLIP 로 만든 순위를 MLIP 로 검증한다')을 화면 어느 use_scope 로 올릴 것인가 — Round-3 공개 경계 계약이 항목별 열거로 노출을 정해 두었고, §6 은 카드 스스로 '신설 해제조건으로 올릴지는 1저자·리뷰 판단'이라고 유보한 건이라 우리가 배치를 정하면 계약을 우회하는 셈이 된다.
- CLAUDE.md 의 'MSD 창 2–50 ps 고정'과 현행 판정축(4창 D_inc plateau · 창 안정성 · 홉 수)의 관계를 규율 문서에 어떻게 쓸 것인가 — convention_check.py 가 CLAUDE.md 를 정본이라 인용하며 2–50 을 기계 강제하는데, 도구(msd_diffusive_check)와 09-04/09-08 결정은 이미 4창·400 ps 로 갔다. 한쪽만 고치면 두 정본이 갈린다.
- 유한크기 배수를 1.65×(50 ps 창, 상자 비교)로 쓸 것인가 1.79×(805 ps, T13 정본)로 쓸 것인가 — T13 자신이 '원자수뿐 아니라 슈퍼셀 모양도 다를 수 있다'고 단서를 달았고 창 길이 축이 섞여 있어 우리가 고를 근거가 없다.
- BVSE R0 표가 두 벌이다(정본 softBV Li–S 2.105/Cl 2.249 vs cascade 쪽 Brown-Adams 1.94/1.91) — cascade 의 이동도 축(bvs_li_proxy_score, G4 게이트)을 softBV 로 다시 매길 것인가. Cl 0.34 Å 차이는 이웃당 약 2.5배이고 47종 순위가 바뀔 수 있다.
- W_ad 부착일 값의 정본 세대를 정해 달라 — 20시드 전체 평균(순위 두 쌍이 역전)과 논문에 쓴 5시드 선택본(R=0.9999) 중 어느 것인가. 100시드 통계는 Li5.4 내부 순위를 유의하지 않다고 하고, W_ad 는 canonical_registry 에도 citation_hazards 에도 등록돼 있지 않다.
- b2o3 의 '면내 BVSE 채널 개방이 O-penalty 를 상쇄한다'는 기전 주장이 σ 비 non_citable 잠금(BH P0-1) 이후에도 서는가 — kb/methodology/electron_localization_framework §5 의 수지 결론 전체가 그 위에 서 있다.
- UMA-Li₃N 금지의 범위를 한 줄로 확정해 달라 — 장벽 절대값만인가, 구속 PES 도인가, 기하 정찰(path-finder)은 허용인가. CLAUDE.md 는 전면 금지인데 kb 카드 2026-07-09 UPDATE 는 구속 PES 0.156 eV 에 합격 도장을 찍었고 도구 4개가 그 사이에서 아무 표시 없이 돈다.
- SDCP wave1 인용 게이트를 시드별(ptfe_dimer_pm1)로 걸 것인가 조각별(ptfe_dimer)로 걸 것인가 — 원장이 시드별로 값을 나눠 두었으니 시드별이 구조와 맞지만, 인용 단위를 바꾸는 판정이라 우리가 정하면 안 된다.
- SDCP_Eads_eV__ptfe_c10_Litop(−0.4124)이 레지스트리에 없는 것이 의도된 제외인가 누락인가 — 마감 문서 확정값은 8개인데 레지스트리는 7건이고 마감 문서 스스로 '7건'이라 적어 두어 내부 모순은 없다.
- kb/open_items.md 의 닫힌 항목 8건을 원장 원문에서 옮길 것인가 화면에서만 접을 것인가 — 원장은 사람이 쓰는 문서이고 화면은 그걸 옮기기만 한다는 원칙과, 대시보드 카운트가 47이 아니라 39여야 한다는 요구가 부딪힌다.
- db/_index.json(2026-06-02 스냅샷)을 재생성할 도구를 만들 것인가 Raw/Record 탭을 은퇴시킬 것인가 — 재생성 스크립트가 repo 에 없고, 지금은 조성마다 밀도가 다른 6월 스냅샷(comp1 97행 / lpsocl 4행 / sdcp 0행)이 조성 페이지에 탭으로 붙어 있다.
- litdb/our_dem_baseline.md 를 다른 브랜치(2026-07-15 판)에서 정본으로 승격해도 되는가 — DEM digest 는 2026-09-04 까지 늘었는데 그 파일은 7월 판이라, 각 행이 지금도 정본인지 확인 없이 올리면 84편이 낡은 기준점을 가리키게 된다.
- D-2026-08-28-estimand-before-compute 가 11일째 proposed 다 — 이 결정 위에 카드 9장과 후속 결정 5건이 서 있는데 원장 규칙은 'ratification 없이 active 가 될 수 없다'이다. 비준하거나, 반대로 CLAUDE.md 의 '2026-08-28 채택'을 제안 상태로 낮춰야 한다(사람 판단).
