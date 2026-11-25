# webapp — SDCP (/sdcp · /sdcp/self-doping · /composition/sdcp)

## 지금 무엇인가
SDCP 화면은 사실 **세 개**다 — `/sdcp`(wave1 흡착 결과 + 인용 게이트 표, doc.html), `/sdcp/self-doping`(자기도핑 개념 해설, doc.html), `/composition/sdcp`(조성 카드 화면, composition.html). 앞의 둘은 kb md 를 읽어 렌더하고, 셋째는 canonical_registry + db/structures 를 읽는다. 1저자가 사진으로 지적한 "N/A 넷 · TODO 셋 · 3D 버튼 95개" 화면은 **`/composition/sdcp`** 이고, `/sdcp` 는 그와 별개로 인용 게이트가 통째로 잠겨 있다(CITABLE 0). 세 화면은 서로 링크하지 않고, 같은 값에 대해 서로 다른 지위를 표시한다.

## 처음 오는 사람
처음 온 사람이 "SDCP" 를 찾으면 사이드바에서 **두 군데**를 본다 — 「자료·기록」 아래 `🧪 SDCP wave1`, 그리고 「Compositions」 아래 `SDCP (ORCA IR)`. 둘이 같은 주제인데 서로를 안 가리켜서, 어느 쪽이 입구인지 알 수 없다.

`/composition/sdcp` 로 들어가면 첫 화면이 **값 없는 카드 8장**(N/A 4 + TODO 4)과 **라벨이 원시 키인 카드 11장**(`SDCP_Eads_eV__sdcp_neutral_cross_Li_at_Ni` 같은)이다. 그 밑 기본 탭이 파일명 **95개 버튼**이고, 그중 24개(.vesta)는 눌러도 3D 가 안 뜬다. 이 화면만 보면 "SDCP 는 아직 아무것도 안 한 계산" 으로 읽힌다. 실제로는 캠페인이 마감됐고 확정값이 있는데, 그 사실이 화면 어디에도 없다.

`/sdcp` 로 들어가면 정반대로 막힌다. 표 8행 중 CITABLE 이 **0**이고, ptfe 4행은 "인용 원장에 **등록돼 있지 않다** — 등록하거나, 왜 없는지 원장에 적어라" 라고 뜬다. 그런데 **바로 그 표 아래 본문**이 "ptfe_dimer 36.1 · ptfe_c10 49.8 meV 낮았다" 를 결론으로 쓴다. 처음 온 사람은 표를 믿어야 할지 본문을 믿어야 할지 못 정한다(정답은 본문이다 — 표가 버그다).

그리고 화면 맨 위 264줄이 전부 비인용 표라, "여기만 읽어도 된다" 는 **30초 요약이 화면 391번째 줄**(전체 939줄 중)에 있다. 처음 온 사람이 제일 먼저 봐야 할 것이 제일 아래 있다.

**없어서 막히는 것 세 가지**: ① 지금 살아 있는 캠페인이 무엇인지 — 본문이 "본류는 C-12 로 옮겨갔다" 고 말하는데 C-12 로 가는 링크·화면이 없다(결정 원장에는 `D-2026-09-04-sdcp-c12-absolute-eads`가 active 로 있다). ② 마감 문서(`sdcp_neutral_closed_2026_08_28.json`)의 **허용 서술 / 금지 서술 / 재개 조건**이 화면에 한 줄도 안 나온다 — 파일명만 언급된다. 처음 온 사람이 "그래서 뭐라고 쓸 수 있나" 를 알 길이 없다. ③ 두 화면 사이 이동 경로.

`/sdcp/self-doping` 은 내용 자체는 이 세 화면 중 유일하게 처음 온 사람용으로 잘 쓰였다(등장인물 → 도핑 정의 → 프로톤 vs 수소원자). 다만 본문 앞에 YAML frontmatter 14줄(`verifiedBy: ...`, `authoredBy: agent`)이 그대로 찍혀서 첫인상이 깨진다.

## 건드리면 안 되는 것
- **접힌 원자료 20건(`<details>` 비인용)** — doc.html:134-148. 지우면 안 된다. data.py:246-250 이 사유를 적어 뒀다: '값을 숨기지도 않는다 … 삭제하면 감사 추적이 끊기고, 현재형으로 두면 철회가 되살아난다'. v3 에서도 **접은 채로 남긴다** — 3일짜리 외주 배치를 다시 돌리게 만드는 게 이 화면의 최악 실패다.
- **행마다 붙은 지위 열 + 사유 열** (doc.html:108-120, 회신 AW P0-2). '상단 배너 하나로는 부족하다' 가 명시된 결정이다. 요약해서 배너 하나로 합치지 말 것.
- **basin 불일치가 판정바닥보다 위 계층이라는 로직** (data.py:275-287). 실측 반례(`sdcp_neutral/net4` −40.7 meV 인데 사유가 '30 meV 아래' 였던 것)까지 주석에 남아 있다. 리팩터링하면서 조각 판정으로 되돌리지 말 것.
- **fail-closed 배너 세 개** — `data.unreadable`(doc.html:72-82), `gate.source_missing`(doc.html:89-92), `_read_ledger`. 2026-09-05·09-07 에 '표가 말없이 사라짐' 과 '500' 을 각각 고쳐서 넣은 것이다. 화면을 정리하면서 '어차피 안 뜨는 배너' 로 지우지 말 것.
- **CANONICAL_NA 의 사유 문자열 전문** (data.py:744-766). li3n UMA 금지 · b2o3 골격 재배열 철회(β 실측값 나열) · 단일시드 1.33× 철회 — 이건 UI 카피가 아니라 **철회 기록**이다. 카드를 접거나 표로 바꾸더라도 문자열은 그대로 옮긴다.
- **마감 문서 `sdcp_neutral_closed_2026_08_28.json` 의 허용/금지/재개 세 절과 `status_history` 11건.** 화면이 요약하거나 부드럽게 바꾸면 안 된다 — 그대로 인용만 한다. 특히 `재개_조건_이것들만.⛔ '위 넷 말고 다른 이유로 이 값을 다시 열지 않는다'`.
- **`/sdcp/self-doping` 본문 전체.** 이 세 화면에서 유일하게 배경지식 0 독자를 위해 쓰인 자산이고(프로톤 제거 vs 수소 원자 제거 → charge/multiplicity), 원고 문구 결정의 근거다. frontmatter 누출만 고치고 내용은 손대지 않는다.
- **explainer md 최상단 2026-09-01 갱신 배너**(①②③)와 **§7 '게이트가 30/30 막았던 건 사실 우리 버그였다'** · **§7b 외부 리뷰가 표현 두 개를 고쳤다** 표. 자기 오류 기록이라 지우면 같은 실수를 다시 한다. 접어도 되지만 삭제 금지.
- **doc.html 의 '데이터 표는 설명문 위' 규칙 자체** — /sdcp 만 예외로 뒤집자는 것이지, 규칙을 없애자는 게 아니다. 인용 가능 값이 있는 다른 라우트에서는 이 순서가 맞다.
- **지위 어휘 4종(BLOCKED · HOLD · NO_VERDICT · CITABLE)과 `_STATUS_BADGE` 표.** 화면마다 다른 말을 쓰지 않기로 한 어휘다(data.py:1064 주석). UNKNOWN 을 **추가**하는 것은 맞지만 기존 4개의 이름·색을 바꾸지 말 것.
- **db/structures 의 95개 파일 자체.** 화면에서 접자는 것이지 파일을 지우자는 게 아니다 — .vesta 는 1저자 배포용이고 CLAUDE.md VESTA 규율(xyz + POSCAR 페어, .vesta+.cube 쌍)이 그 존재 이유다.

## 발견

### [P0·broken] gate-key-shape-mismatch
- **어디**: `webapp/data.py:204 · webapp/data.py:233-236`
- **근거**: 게이트가 만드는 allow-list 는 `"citable_dE": set((cit.get("dE_site_meV") or {}).keys())` = 실측 `['ptfe_c10_pm1','ptfe_dimer_branch_interaction','ptfe_dimer_net4','ptfe_dimer_pm1','sdcp_neutral_pm1']` (조각_시드 형태). 그런데 조회는 `if fragment not in gate.get("citable_dE", ())` 로 **맨 조각 이름**('ptfe_dimer','ptfe_c10')을 넣는다 → 영원히 불일치. 실측: `n_citable_dE 0`, 지위 분포 `{'BLOCKED': 4, 'UNKNOWN': 3, 'NO_VERDICT': 1}`. 화면에 뜨는 문장이 '`ptfe_dimer` 가 인용 원장(sdcp_wave1_citable.json 의 dE_site_meV)에 **등록돼 있지 않다** — 지위 불명이므로 인용하지 않는다. 등록하거나, 왜 없는지 원장에 적어라' 인데, 원장에는 `dE_site_meV/ptfe_dimer_pm1 = 36.071` 로 **등록돼 있다.** 같은 함수 안 `gate["dE_notes"]` 는 맨 조각 키(`dE_notes/ptfe_dimer`)를 쓰므로 두 키 모양이 한 함수에서 갈렸다. 상단 배지도 'CITABLE 0 · BLOCKED 4 / ΔE 8행' 으로 거짓을 센다.
- **고치는 법**: 두 키 모양을 맞춘다. 최소 수정은 조회를 `f"{fragment}_{seed}"` 로 바꾸는 것(시드별 게이팅) 또는 allow-list 를 `{k.rsplit('_',1)[0] for k in ...}` 로 접는 것(조각별 게이팅). 어느 쪽이 규율상 맞는지는 1저자가 정한다 — 원장이 시드별로 값을 나눠 두었으니 시드별 게이팅이 원장 구조와 맞다. 고친 뒤 **양성 시험**을 붙인다(아래 no-positive-test 항목).
- codex 필요: False

### [P0·wrong] composition-eads-headline
- **어디**: `webapp/templates/composition.html:24-63 · 렌더 /composition/sdcp`
- **근거**: 보류 중인 절대 E_ads 가 **헤드라인 지표 카드**로 큰 글씨로 뜬다: `<div class="mv">-0.7675</div>` + 라벨 `SDCP_Eads_eV__sdcp_neutral_Litop` + 배지 '잠정'. 보류 사유('⚠ 2026-08-28 회신 O + INCAR 감사: **절대값 조건부 보류** … δ_m + δ_LREAL')는 **배지의 title= 안에만** 있어서 마우스를 올려야 보인다. 같은 값이 `/sdcp` 에서는 빨간 테두리 배너 '⛔ 절대 E_ads 는 전건 인용 보류다' 와 함께 `<details>` 접힘 안에 있다. 화면 둘이 같은 수치에 정반대 지위를 준다. citation_hazards.json 에도 `{"file": "db/properties/sdcp_wave1_citable.json", "level": "BLOCKED", "what": "절대 흡착에너지 4종과 0.346 eV 헤드라인"}` 로 BLOCKED 가 걸려 있는데 이 화면은 그걸 안 읽는다.
- **고치는 법**: composition.html 의 metric 카드에 `status != 'canonical'` 이면 **본문에 보이는** 한 줄 사유를 붙인다(hover 금지). 그리고 registry status 가 provisional/retracted/non_citable 인 metric 은 metrics-row 가 아니라 `/sdcp` 처럼 접힌 '비인용 원자료' 절로 내린다. 지우지는 않는다.
- codex 필요: False

### [P0·useless] cross-composition-todo-pollution
- **어디**: `webapp/data.py:782-788 (metric_meta) · webapp/templates/composition.html:59-61 · /composition/comp1 등 전 조성`
- **근거**: metric 행은 (레지스트리 전체 metric × 이 조성)의 곱집합이라, SDCP 분자 metric 11개가 **모든 조성 페이지**에 TODO 로 찍힌다. /composition/comp1 실측 렌더: `'TODO','SDCP_dE_site_meV__ptfe_dimer_pm1','TODO','SDCP_Eads_eV__sdcp_neutral_cross_Li_at_Ni'` … LPSCl 페이지가 PTFE 흡착에너지를 '미계산 TODO' 로 광고한다. 조성별 TODO 카드 수 실측: comp1 14 · modelc 13 · lic6 18 · li3n 18 · vgcf_hbn 17 (전체 metric 19개 중). /explorer 는 SDCP_Eads 28회·SDCP_dE_site 16회, /compare 는 35회·20회로 열까지 번졌다. data.py:2460 이 NOT_APPLICABLE 을 도입한 이유가 '금지된 계산을 TODO 로 광고하지 않기' 인데 이게 정면으로 어긴다 — 그것도 보류(HOLD)된 양을.
- **고치는 법**: metric 을 **축(axis) 그룹**으로 나눈다: 조성 공통 앵커(gap/B0/E_VRH/MD_Ea/ICOHP)와 캠페인 전용(SDCP_*)을 분리해, 캠페인 전용 metric 은 그 조성 페이지에서만 렌더한다. 곱집합을 그대로 그리지 않는다. 최소 조치로는 metric 에 `applies_to: [cid...]` 를 달고 composition.html·explorer·compare 가 그걸 본다.
- codex 필요: False

### [P1·useless] raw-key-metric-cards
- **어디**: `webapp/data.py:770-779 (_METRIC_LABEL) · webapp/data.py:791-806 (CANONICAL_META) · /composition/sdcp`
- **근거**: SDCP metric 11개가 `_METRIC_LABEL`·`CANONICAL_META` 에 **하나도 없다.** 그래서 라벨이 원시 레지스트리 키 그대로 나오고(`SDCP_dE_site_meV__ptfe_dimer_pm1`), 단위 칸은 빈 문자열, 방법 주석은 `<div class="mm" title=""></div>` 로 **빈 div** 다. 실측 렌더에 `<div class="metric" title="">` 가 11번. metric_meta() docstring 이 '없으면 metric 이름 그대로' 라고 폴백을 인정하는데, 폴백이 화면 절반을 차지하면 폴백이 아니라 UI 다.
- **고치는 법**: 11개에 label/unit/short 와 방법 한 줄(정본·게이트·단서)을 붙인다 — 예: `SDCP_dE_site_meV__ptfe_dimer_pm1` → ('자리대비 ΔE (ptfe_dimer, pm1)', 'meV', 'ΔE dimer'). 붙일 수 없으면 카드로 그리지 말고 표로 내린다. 빈 `mm` div 는 렌더하지 않는다.
- codex 필요: False

### [P1·useless] structures-95-buttons
- **어디**: `webapp/templates/composition.html:129-135 · webapp/data.py:468-489 · /composition/sdcp`
- **근거**: 기본 탭이 Structure 이고, 그 안이 파일명 버튼 **95개** 한 줄 나열이다(실측 `n structures 95`). 폴더 분포 `{'sdcp_wave1': 48, '(root)': 20, 'sdcp_poses_qe': 9, 'sdcp_orca_gs0': 6, 'sdcp_orca_stageA': 6, 'sdcp_poses_phaseB': 4, 'c12_frozen': 2}`, 확장자 `{'xyz': 44, 'vasp': 27, 'vesta': 24}`. **.vesta 24개는 `fmt` 가 빈 문자열**이라 눌러도 3D 가 안 뜬다(툴팁만 '3D 파서 없음 — 다운로드해서 VESTA로 보세요') — 같은 모양 버튼인데 4분의 1이 다른 일을 한다. 같은 구조가 vasp/vesta/xyz 3벌로 중복돼 실체는 약 32개다. li3n 60 · vgcf_hbn 64 로 다른 조성도 같은 증상이다.
- **고치는 법**: ① 폴더별로 접는다(sdcp_wave1 48 · poses_qe 9 …), 기본은 접힘. ② 같은 stem 의 3형식을 **한 항목**으로 묶고 형식은 그 항목 안 작은 토글로(3D 는 xyz/vasp, 다운로드는 vesta). ③ .vesta 는 버튼이 아니라 다운로드 아이콘으로 분리 — 3D 뷰어 줄에 섞지 않는다. ④ 파일명 검색 상자 하나.
- codex 필요: False

### [P1·broken] frontmatter-leak
- **어디**: `webapp/app.py:151-178 (md_html) · /sdcp · /sdcp/self-doping`
- **근거**: kb 문서의 YAML frontmatter 가 본문으로 렌더된다. /sdcp/self-doping 화면 80–93줄이 `title: 자기도핑(self-doping)이란 …` / `date: 2026-08-26` / `verifiedBy: "우리 계산 설정(make_phaseB_doped_v2.py: charge 0 · tot_magnetization 1.0)과 …"` / `authoredBy: agent` 그대로다. /sdcp 도 350번째 줄에서 같다. `md_html` 의 extension 목록에 frontmatter/meta 처리가 없다. 대조: /methods·/todo 는 안 새는데 그건 그 md 에 frontmatter 가 아예 없어서다(둘 다 `# ...` 로 시작). 즉 **kb_wiki 규약을 지킨 문서일수록 화면이 깨진다.** 결과로 제목이 세 번 겹친다(h1 '⚗️ 자기도핑이란 무엇인가' → frontmatter title → md h1).
- **고치는 법**: `md_html` 진입부에서 `---\n…\n---` 선두 블록을 떼어낸다(또는 markdown `meta` extension 등록 후 본문만 렌더). 뗀 frontmatter 는 버리지 말고 doc.html 상단 작은 메타 줄(updated · verificationStatus · confidence)로 되살리면 신선도가 오히려 화면에 올라온다.
- codex 필요: False

### [P1·broken] hazard-binding-inert
- **어디**: `webapp/data.py:191-199`
- **근거**: 2026-09-07 회신 BG ① 로 넣은 hazard 결속이 **한 건도 안 걸린다.** 실측 `hazards_by_fragment = {}`. 이유 둘: ① 매칭이 `" ".join(h.get(k) for k in ("file","what","why"))` 안에서 조각 이름 4개를 substring 으로 찾는데, 정작 SDCP 최대 위험인 `{"file":"db/properties/sdcp_wave1_citable.json","level":"BLOCKED","what":"절대 흡착에너지 4종과 0.346 eV 헤드라인"}` 에는 그 4개 이름이 **안 들어 있다**(파일 단위 hazard 라서). ② 레벨 필터가 `("BLOCKED","HOLD")` 라 `sdcp_neutral_closed_2026_08_28.json` 의 `level: "CONDITIONAL"`(술폰산 접촉 기전 양방향 금지)은 통째로 버려진다. ③ 설령 걸려도 ptfe 조각은 위 gate-key 버그의 UNKNOWN 리턴이 **먼저** 나가서 hazard 검사 줄(data.py:237)에 도달하지 못한다 — 죽은 코드다.
- **고치는 법**: 조각 이름 substring 대신 **hazard 의 file 경로 ↔ 이 화면이 읽는 원장 경로**로 건다(sdcp_wave1_citable.json 이면 그 화면 전체에 배너). CONDITIONAL 도 표시 대상에 넣되 색을 달리한다. hazard 검사를 UNKNOWN 리턴보다 **앞으로** 옮긴다.
- codex 필요: False

### [P1·missing] no-sdcp-claim-ids
- **어디**: `webapp/canonical.py (all_claims) · 세 라우트 전부`
- **근거**: claim 결속 스캔 실측: `/sdcp` bound 0 / unbound 0, `/sdcp/self-doping` 0/0, `/composition/sdcp` 0/0. `all_claims()` 는 10건이고 전부 b2o3·LPSOCl MD 계열(`MD_Ea_eV@b2o3`, `MD_sigma_ratio_*@b2o3_vs_modelc`, `HZ-lpsocl-Ea-diffusive-gate`, `HZ-cross-system-Ea`, `HZ-beta-hard-gate`) — **SDCP claim 이 하나도 등록돼 있지 않다.** 그래서 2026-09-08 커밋 12e6d0c9b '전 표면 미결속 0, 래칫 은퇴' 의 초록불이 이 세 화면에서는 '결속이 잘 돼서 0' 이 아니라 **'결속할 claim 자체가 없어서 0'** 이다. 이건 test_webapp.py:2950 이 스스로 경계한 상황('화면의 미결속 0 이 *선언 덕분*인지 *글자가 없어서*인지 가른다')과 같은 종류다.
- **고치는 법**: SDCP 철회·보류 3건에 claim ID 를 발급한다 — (a) 절대 E_ads / 0.346 eV 헤드라인(BLOCKED, hazard 이미 있음), (b) 'O···Li 2.09 Å · 술포네이트 앵커링' 접촉 기전(2026-08-29 회신 T 철회), (c) '두 배 세게'·'넷 다 Li 자리 선호'(보류·오요약). 그러면 세 화면 산문에 자동 결속이 붙고, 초록불이 실질을 갖는다.
- codex 필요: False

### [P1·buried] summary-buried-under-blocked-table
- **어디**: `webapp/templates/doc.html:56-150 · /sdcp`
- **근거**: doc.html 은 '데이터 표는 **설명문 위**에 둔다 — 값 보러 온 사람이 스크롤하지 않게' 라는 규칙으로 표를 먼저 그린다. 그런데 /sdcp 는 그 표의 인용 가능 행이 **0**이다. 실측: 화면 가시 텍스트 939줄 중 표가 81–345줄, '🟢 0. 30초 요약 (여기만 읽어도 된다)' 는 **391줄**. 즉 비인용 값 264줄을 지나야 요약이 나온다. 규칙의 전제(값 보러 온 사람)가 이 페이지에서만 뒤집혀 있다.
- **고치는 법**: doc.html 에 `data_first=False` 같은 스위치를 주고 /sdcp 는 순서를 뒤집는다 — ① 마감 상태 카드(확정값·허용 서술·금지 서술·재개 조건) ② 30초 요약 ③ 그 다음 접힌 원자료 표. 표를 지우지 말고 **접는다**.
- codex 필요: False

### [P1·missing] closure-doc-not-on-screen
- **어디**: `db/properties/sdcp_neutral_closed_2026_08_28.json · /sdcp 화면`
- **근거**: 마감 문서에 `허용_서술_이대로만_쓴다`(비교·자리_dimer·자리_c10·자리_neutral·접촉_기전) 5항, `⛔_금지_서술` 7항, `재개_조건_이것들만` 4항, 그리고 `status_history` 최신 상태 `"closed_for_scope_pending_reference_equivalence"`(2026-08-31) 가 있다. /sdcp 화면에는 이 중 **한 줄도** 안 나온다 — 파일명만 `sdcp_neutral_closed_2026_08_28` 로 두 번 언급된다. 화면이 판정하지 않는다는 원칙은 맞지만, 정본을 **읽어서 보여주는 것**과 파일명만 대는 것은 다르다. 지금은 '그래서 뭐라고 쓸 수 있나' 를 화면에서 알 수 없다.
- **고치는 법**: /sdcp 최상단에 마감 카드 하나: 상태(closed_for_scope_pending_reference_equivalence) · 확정값 4+4 · 허용 서술 그대로 · 금지 서술 그대로 · 재개 조건 4개. 전부 JSON 에서 읽어 렌더하고, 화면이 문구를 새로 짓지 않는다.
- codex 필요: False

### [P1·wrong] n-jobs-30-vs-20
- **어디**: `webapp/templates/doc.html:86-87 · db/properties/sdcp_wave1_results.json`
- **근거**: 화면 부제가 '{{ data.meta.code }} · 잡 {{ data.meta.n_jobs }} · OUTCAR {{ data.meta.n_outcar }}' 라 '잡 **30** · OUTCAR 43' 으로 뜨고, 바로 아래 접힘 요약은 '원자료 **20**건 펼치기' 다(실측 `n_jobs: 30`, `len(jobs) = 20`). 본문 md 도 '외주 30잡' 이라 쓴다. 30 과 20 의 차이를 화면이 설명하지 않아서, 10건이 사라진 건지 30 이 다른 것을 세는 건지 알 수 없다.
- **고치는 법**: 헤더 수치를 '표에 실린 복합체 잡 20 / 번들 전체 30(분자·슬랩 포함)' 처럼 **무엇을 세는지**와 함께 쓴다. 어느 쪽이 맞는지는 원장에서 확인해 라벨을 붙일 것 — 값을 고치지 말고 이름을 붙인다.
- codex 필요: False

### [P1·stale] stale-c12-12jobs
- **어디**: `kb/results/sdcp_wave1_explainer_2026_08_25.md:249 (렌더되는 §8)`
- **근거**: 화면 §8 이 '→ **C-12 재설계로 흡수** (회신 AI §A-Q4 = C, 08-30) — wave 체계 게이트는 더 다듬지 않고, **새 12잡 경로**의 분석기 게이트가 그 역할을 잇는다' 로 뜬다(렌더 HTML 에 '12잡' 1회). 그런데 citation_hazards.json 이 같은 것을 STALE 로 잡아 뒀다: `{"file":"db/properties/sdcp_c12_protocol_2026_08_30.json","level":"STALE","what":"잡 수(§0 '12잡' · §12 '19잡') …","why":"실물 v18 은 **16잡**이고 clean slab 은 제거됐다(커밋 57cfcdea · 회신 AV Q6)"}`. 원장이 stale 로 등록한 문자열이 화면에 살아 있다.
- **고치는 법**: '새 12잡' → '새 C-12 경로(실물 v18 · 16잡)' 로 고치거나 잡 수를 빼고 이름만 쓴다. 근본은 hazard-binding-inert 와 같다 — STALE hazard 가 화면 문자열에 결속되면 이런 게 자동으로 표시된다.
- codex 필요: False

### [P1·missing] no-link-to-live-campaign
- **어디**: `webapp/app.py:463-486 (/sdcp 라우트의 parent/child/artifact) · db/governance/decisions.json`
- **근거**: 결정 원장에 SDCP 관련 9건이 있고 그중 살아 있는 것이 `D-2026-08-30-sdcp-c12-path`(active) · `D-2026-09-03-sdcp-c12-kconv-axis-excluded`(active) · `D-2026-09-04-sdcp-c12-absolute-eads`(active) · `D-2026-08-31-sdcp-polaron-S0-four-layer`(active) 다. /sdcp 본문이 '이후 본류는 **C-12 외주 VASP**(고정기하 조각 대비 D)로 옮겨갔다' 라고 스스로 말하는데, 화면이 주는 링크는 `parent=/log`, `child=/sdcp/self-doping`, artifact 하나뿐이다. C-12·폴라론 화면도, /governance 로 가는 문맥 링크도 없다(사이드바 전역 링크만 있다). 즉 **끝난 캠페인 화면은 있고 진행 중인 캠페인 화면은 없다.**
- **고치는 법**: /sdcp 상단에 '지금 진행 중' 줄 하나 — C-12(active 결정 3건) · 폴라론 S0 로 링크하고, 이 페이지는 '닫힌 wave1' 임을 명시. /governance 의 SDCP 결정 9건으로 앵커 링크를 건다. v3 에서는 `/sdcp` 를 캠페인 허브(wave1 접힘 · C-12 앞)로 재편하는 게 맞다.
- codex 필요: False

### [P2·duplicate] two-sdcp-nav-entries
- **어디**: `webapp/templates/base.html 사이드바 · /sdcp · /composition/sdcp`
- **근거**: 사이드바에 SDCP 항목이 둘이다 — 「자료 · 기록」 그룹의 `🧪 SDCP wave1`(→ /sdcp)과 「Compositions」 목록의 `SDCP (ORCA IR)`(→ /composition/sdcp). 링크 실측: /composition/sdcp 안의 `href="/sdcp"` 는 **1회뿐이고 그게 사이드바다**(본문 교차링크 없음). /sdcp 쪽도 본문에서 /composition/sdcp 를 안 가리킨다. 두 화면이 같은 조성의 다른 절반(개념·결과 vs 구조·차트)을 들고 서로 모른다.
- **고치는 법**: 둘 중 하나를 정본 입구로 정하고 나머지는 그 안의 탭으로 넣는다. 최소 조치는 양쪽 page-actions 에 상호 링크 버튼 하나씩(doc.html 은 `child`, composition.html 은 새 버튼). 사이드바에서는 SDCP 를 한 곳으로 모은다.
- codex 필요: False

### [P2·ia] na-cards-styled-as-todo
- **어디**: `webapp/templates/composition.html:52-58 · webapp/static/css/style.css:193-194`
- **근거**: N/A 카드가 `<div class="metric todo">` 로 **TODO 와 같은 클래스**를 쓴다. CSS 는 `.metric.todo{background:var(--todo-bg);border-style:dashed;...}` 하나뿐이라 '성립 안 함(N/A)' 과 '미계산(TODO)' 이 시각적으로 구분이 안 된다 — 점선 테두리·흐린 배경이 똑같다. data.py:2459-2460 이 둘을 나눈 1순위 이유가 '금지된 계산을 TODO 로 광고하지 않기' 인데, 데이터층은 나눴고 CSS 가 다시 붙였다.
- **고치는 법**: `.metric.na` 클래스를 따로 준다(점선 대신 실선 회색 · '해당 없음' 어휘). 더 나은 안: 분자계인 /composition/sdcp 에서는 주기계 전용 축(gap/B0/E_VRH/MD_Ea) 4장을 카드로 그리지 말고 '이 계에 적용되지 않는 축 4개' 한 줄 접힘으로 내린다.
- codex 필요: False

### [P2·broken] unknown-status-no-color
- **어디**: `webapp/templates/doc.html:68-71`
- **근거**: `st_badge` 매크로의 색 표가 `{'CITABLE':'#0d9488','NO_VERDICT':'#c05621','HOLD':'#c05621','BLOCKED':'#be123c'}` 인데 `_wave1_status` 가 돌려주는 **`UNKNOWN` 이 없다** → `c.get(s,'#6b7280')` 폴백으로 회색이 된다. 지금 화면에서 UNKNOWN 은 4행 중 3행이고 의미상 '지위 불명 = 인용 금지' 인데, 색은 가장 순한 회색이라 CITABLE 보다도 덜 위험해 보인다. 2026-09-07 에 `retracted` 배지가 표에 없어 철회값이 정상 카드로 떴던 것(data.py:1074-1081)과 같은 종류의 누락이다.
- **고치는 법**: `st_badge` 색 표에 `'UNKNOWN':'#be123c'` 를 넣는다(BLOCKED 와 같은 급). 그리고 어휘 목록 `WAVE1_STATUS = ("BLOCKED","HOLD","NO_VERDICT","CITABLE")` 에도 UNKNOWN 이 빠져 있으니 같이 넣고, 시험이 '색 표 ⊇ 함수가 내는 지위 집합' 을 검사하게 한다.
- codex 필요: False

### [P2·missing] no-positive-gate-test
- **어디**: `webapp/tests/test_sdcp_wave1.py:223 · :234 · :301`
- **근거**: 게이트 시험이 **음성만** 있다: ':223 doped 는 마감이라 어느 표에서도 CITABLE 이 아니다', ':234 절대 E_ads 는 어떤 조각도 CITABLE 이 될 수 없다', ':301 `assert r["n_citable_dE"] == 0` (원장 못 읽었을 때)'. 'CITABLE 이 나와야 하는 경우' 를 확인하는 양성 시험이 없어서, gate-key-shape-mismatch 로 게이트가 **영구히 잠긴** 상태가 전 시험을 통과했다. CLAUDE.md 코드 규율의 '양성만 있는 selftest 는 통과해도 아무것도 보증 못 한다' 의 정확한 거울상이다.
- **고치는 법**: `ptfe_dimer` 두 행이 CITABLE 이고 사유가 `dE_notes/ptfe_dimer` 문자열과 일치하는지 보는 양성 시험 하나. 그리고 '지위 4종이 각각 최소 1행씩 나온다' 는 커버리지 시험(어느 지위도 0 이면 게이트가 한쪽으로 붙었다는 신호).
- codex 필요: False

### [P2·useless] chart-chips-undifferentiated
- **어디**: `webapp/templates/composition.html:165-167 · /composition/sdcp Charts 탭`
- **근거**: 칩 15개 중 **11개 라벨이 똑같이 'data'** 다(실측: data ×11, Binding ×2, IR ×2). 실제 파일은 `sdcp_nseries_spin_2026_09_08.csv`, `sdcp_wave1_incar_echo_2026_08_28.csv`, `sdcp_v7c_trimer_spin.csv` 처럼 서로 완전히 다른 것들인데 화면에서는 구분이 안 돼 하나씩 눌러 봐야 안다. 렌더 텍스트가 그대로 'data data data data data data data Binding data data Binding data data IR IR'.
- **고치는 법**: `kind` 폴백을 파일 stem 에서 만든다(`sdcp_nseries_spin_2026_09_08` → 'n-series spin'). 최소 조치로도 폴백일 때는 'data' 대신 파일명 stem 을 쓴다 — 이름이 없는 것보다 긴 이름이 낫다. 그리고 최신 파일(2026-09-08 n-series spin)을 첫 칩으로.
- codex 필요: False

### [P2·useless] raw-tab-empty-todo
- **어디**: `webapp/templates/composition.html:193 · /composition/sdcp Raw 탭`
- **근거**: 탭 라벨이 '🗂 Raw (0)' 인데 안을 열면 '인덱스 메트릭 없음 <span class="badge b-todo">TODO</span>' 다(실측 `metrics(raw tab) 0`). 0 이라고 이미 라벨에 적어 두고 빈 탭을 만들어 그 안에 또 TODO 배지를 단다. db/_index.json 스냅샷에 분자계 metric 이 없는 것은 '미계산' 이 아니라 '그 인덱스의 대상이 아님' 이다.
- **고치는 법**: 항목 수가 0 이면 탭 자체를 렌더하지 않는다(Bonding 탭은 이미 `{% if icohp or ... %}` 로 그렇게 한다 — 같은 규칙을 Structure/Charts/Raw 에도 적용). 빈 상태의 TODO 배지는 전부 뺀다.
- codex 필요: False

### [P2·stale] partial-correction-7b
- **어디**: `kb/results/sdcp_wave1_explainer_2026_08_25.md:239-241 (렌더되는 §7b)`
- **근거**: '숫자 자체는 안 바뀌었다 — **숫자에 붙는 주장 강도**를 낮춘 것이다. 결론(**어디에 붙나**·얼마나 세게 붙나)은 그대로다. *(⚠ 08-25 시점 문장 — "얼마나 세게" 쪽은 그 뒤 08-28 회신 P 로 보류됐다. 맨 위 갱신 배너 참조.)*' — 괄호 정정이 '얼마나 세게' **한쪽만** 덮는다. 그런데 '어디에 붙나'(자리 선호)도 그 뒤 낮아졌다: sdcp_neutral 은 NO_VERDICT('30 meV 판정 해상도에서 미해결'), ptfe 는 화면상 UNKNOWN 이고, 마감 문서 금지 서술 1번이 "'자리 불문' — 자리대비는 미해결이다" 다. 부분 정정이 나머지 절반을 살려 둔다.
- **고치는 법**: 괄호를 '두 결론 다 그 뒤 낮아졌다 — 세기는 보류(회신 P), 자리는 neutral 미해결·조각 간 일반화 금지' 로 넓힌다. 같은 문장 안에서 반쪽만 정정하지 않는다.
- codex 필요: False

### [P2·wrong] title-promises-unresolved-answer
- **어디**: `webapp/app.py:476 · webapp/app.py:484-485`
- **근거**: h1 이 '🧪 SDCP wave1 — **바인더가 NCM 표면 어디에 붙나**' 이고 부제가 'VASP 외주 30잡 · **realized-basin 일치분만 인용** · db/properties/sdcp_wave1_results.json' 이다. 그런데 '어디에 붙나' 는 마감 문서가 `자리_neutral: **30 meV 판정 해상도에서 미해결**`, 금지 서술 1번 "'자리 불문' — 자리대비는 미해결이다" 로 닫아 둔 질문이고, '일치분만 인용' 은 현재 인용 가능 행이 0 이라 인용하는 게 없다. 제목·부제가 본문 게이트보다 강하게 약속한다.
- **고치는 법**: 제목을 '바인더가 NCM 표면에 어떻게 붙나 — wave1(닫힘, 2026-08-28)' 로, 부제를 '자리대비 미해결 · 절대 E_ads 보류 · 인용 가능 행 N건' 처럼 **게이트가 센 수를 그대로** 넣는다(하드코딩 금지, `data.n_citable_dE` 로).
- codex 필요: False

### [P2·missing] closure-value-missing-from-registry
- **어디**: `db/properties/canonical_registry.json (SDCP_Eads_eV__* 7건) · db/properties/sdcp_neutral_closed_2026_08_28.json 확정값`
- **근거**: 마감 문서 `확정값_pm1_box24_eV` 는 8개 값을 담는다 — neutral 4종 + `대조군_ptfe_c10_Litop: -0.4124` · `대조군_ptfe_c10_Nitop: -0.3626` · `대조군_ptfe_dimer_Litop: -0.3663` · `대조군_ptfe_dimer_Nitop: -0.3302`. 레지스트리에는 7건뿐이고 **`SDCP_Eads_eV__ptfe_c10_Litop`(-0.4124) 가 없다**(실측 목록에 c10 은 Nitop 만). 마감 문서 스스로 '레지스트리 — SDCP_Eads_eV__* 7건' 이라 적어 두어 내부적으로는 모순이 없지만, 화면(/composition/sdcp)은 확정값 8개 중 7개만 보이고 하나가 왜 없는지 말하지 않는다. 나는 이게 의도된 제외인지 누락인지 **확인하지 못했다.**
- **고치는 법**: 둘 중 하나 — 등재하거나, 마감 문서에 '레지스트리 제외: ptfe_c10_Litop, 사유 …' 를 한 줄 적는다. 화면은 그 사유를 읽어 표시한다. 값을 새로 만들지는 않는다.
- codex 필요: True
