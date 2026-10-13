# Codex 요청 — [연구세미나 · DEM–MPM–복셀 파이프라인] 초안 4 덱 19 장 · 내용 + 미감 리뷰 (2026-10-13 · 발송 = 1저자)

> ⚠ **정오표 (10-13 · Codex v3 통합 판정 §3 · 원장 `SELF-110`)** — §2 "지금 크기" 의 **■ 제목 15 pt 는 오기** (실제 = master otherStyle **18 pt 상속** · 직접 지정 없음) · §2 "기준 문법" 의 **출처 줄 우상단 10 pt 는 이 덱에 구현돼 있지 않다** (생성기가 프로토타입 `TextBox 69` 를 지우고 `tag()` 를 호출하지 않는다 — p01–p19 전부).  판정 = `docs/reviews/codex_review_seminar_deck_v3_20261013.md` · 수정 계획 `docs/reviews/seminar_deck_fix_plan_20261013.md`.  발송본 원문은 아래 그대로 둔다.

> **한 줄**: 1저자의 연구실 연구세미나 덱 (본문 15 + 표지 · 요약 · 참고문헌 · 끝 = 19 장) 을 **세 축**으로 봐 달라 — ① 주장 ↔ 수치 ↔ 정본 ↔ 한정어가 맞는가 (과장 · 누락 · 금지값) ② 처음 보는 사람에게 **사람이 만든 연구실 발표**로 보이는가 · 교수가 **글이 많다**고 느낄 곳 ③ 분야 용어로 읽히는가.  수치 · 코드 변경 없음.  덱 pptx 는 리포 밖 (사용자 덱 규약) — ZIP 동봉.  검토 핀 = 이 요청서가 든 커밋.

## 1. 왜

- 발표 = 1저자의 연구실 연구세미나 (날짜 미정 — 표지의 `[date — to be set]` 는 의도).  주제 = 황화물 전고체 복합 양극의 입자 해상 다중스케일 시뮬레이션 (DEM 충전 · 압밀 → MPM 소성 압밀 → 복셀 수송 → 전극 응답) **진행 보고**.  본문 15 장 (p02–p16) + 표지 (p01) · 요약 (p17) · 참고문헌 (p18) · 끝 (p19).
- 1저자 요구 (10-13): 15 장 안팎 · **빽빽하지 않게** (기준 = 1저자 본인의 10-13 연구세미나 덱 — Codex 미감 리뷰를 거친 밀도) · 스토리라인 **① 파이프라인 → ② DEM 한계 → ③ MPM · SE 물성 · DEM↔MPM → ④ voxelization → ⑤ 첨가제 → ⑥ 문제 셋 → ⑦ 진행 → ⑧ 계획** · 내부 용어 배제 · 분야 용어 · 리포 · litdb 그림 적극 활용 · 리포에 없는 그림은 공백 + **채울 글** (나중에 검토할 때 넣는다).
- 만든 방식: 10-13 덱의 장 7 종을 프로토타입으로 **복제**해 글 · 그림만 바꿨다 (생성기 · 원래 장은 삭제) → 같은 템플릿 · 같은 틀.  새 그림 4 는 matplotlib (정본값 자동 대조 selftest).  자기검사 = `claims.json` `quotation_ban` 42 패턴 0 · 슬라이드 본문 내부 용어 0 · 19 장.
- 첫 초안은 글이 그림을 덮고 제목이 안 바뀌는 등 기계 티가 났다 → 초안 2–4 에서 본문 상자 높이 · 그림 위치 · 짧은 bullet · 제목 줄바꿈 · 자리 표시 글을 고쳤다.  **지금 묻는 것**: 그래도 남은 기계 티 · 글 밀도 · 수치 한정어 · 용어.

## 2. 볼 것

- **렌더**: `render/p-01.png … p-19.png` (1280 × 960 · 4:3 · LibreOffice) · 한눈에 `render/contact_sheet.jpg`.  템플릿 글꼴은 대체 글꼴로 렌더됐다 — 줄바꿈은 PowerPoint 와 거의 같지만 ■ · ⁺ · µ 같은 기호 모양이 조금 다를 수 있다.
- **덱**: `seminar_20261013_draft.pptx` (리포 밖) · 생성기 `docs/seminar_20261013/build_seminar.py` (`--template <10-13 덱.pptx>` · 끝에 selftest) · 글 전문 + 발표자 메모 `docs/seminar_20261013/slide_text_draft3.md` · 장별 수치 출처 `slide_sources.json` · 재사용 그림 세대 · 자리 표시 목록 `README.md` · 비준 개요 `outline_v1.md`.
  고칠 것을 **좌표 (in) · 글자 크기 (pt) · 문구**로 주면 생성기에 그대로 반영한다.
- **지금 크기 (pt)**: 절 표지 24 (좌상단 "Introduction" · "DEM" …) · ■ 제목 줄 15 (프로토타입 상속) · 본문 bullet **13** (⚠ 10-13 덱은 15 — 글을 더 넣으려고 줄였다 · 그대로 둘지 15 로 올리고 글을 줄일지 = Q-SEM-4) · '< 캡션 >' 10 · 출처 줄 10 (회색 이탤릭 · 우상단) · 자리 표시 채울 글 10 · 결론 줄 14 (p07 · p08 오른쪽 상자는 12) · p14 점선 상자 항목 14 · p07 · p16 두 칸 14 / 13 · p17 요약 15 · p18 참고문헌 11.
- **기준 문법 (10-13 덱 → 우리 장)**: 표지 (p1) → p01 · **그림 본문 (p4) → p02 · p03 · p04 · p05 · p06 · p08 · p09 · p10 · p11 · p12 · p13 · p15 (12 장)** · 두 칸 (p11) → p07 · p16 · 점선 상자 (p3) → p14 · 요약 (p15) → p17 · 참고문헌 (p17) → p18 · Thank you (p16) → p19.  자리 표시 상자 · '< 캡션 >' 은 10-13 p2 의 "Figure" 타일 · 캡션을, 출처 줄은 p4 우상단 글상자를 복제했다.
  그 문법: 절 표지 + ■ 제목 한 줄 + bullet 2–3 · 핵심 단어만 파랑 · 미해결 · 경고는 빨강 · 그림 아래 '< 캡션 >' · 결론 한 줄 (파랑 또는 빨강) · 출처 줄 우상단 · 점선 상자 (흰 제목 탭 + 번호 항목) 는 p14 한 장.
- **그림 세 종류**:
  · **리포 재사용 그림 11** (값 세대 = README 표): ps73 7:3 침대 4 단계 3D + G1 porosity (p03) · p14 수송 tortuosity · p15 σLi⁺ (p04) · 이력 법선력 코드 재현 (p05) · 첨가제 모식도 둘 + G6 (p10) · 단면 하중 몫 + SE σ_VM 4 단계 (p13) · G5a · G5b · G3 (p15).  **다시 그리지 않는다** — 크기 · 자르기 · 캡션 · 빼기 제안은 된다.
  · **새 그림 4** (matplotlib **미리보기** · `docs/seminar_20261013/figs/` · png + svg + csv): F1 파이프라인 흐름도 (p02) · F2 격자 비 (p11) · F3 σ_e 모델 ↔ DC 분극 (p12 왼쪽) · F4 ps45 σ_e 다섯 조성 (p12 오른쪽).  값은 selftest 로 정본에 묶여 있다 — **무엇을 그리나 · 그래프 종류 · 축 · 크기 · 배치**를 봐 달라 (1저자가 Origin 으로 다시 그릴 수 있다).
  · **자리 표시 6** (p04 · p06 ×2 · p08 · p09 ×2): 일부러 비웠다 — 상자 안에 **무엇 · 출처 · 명령**을 적어 두었다.
- **대본**: 없다 — 발표자 메모 (notes · `slide_text_draft3.md` 에 전문) 가 그 자리 (출처 · 한정어).  화면 문장 중 "말로 하면 된다" 싶은 것은 **notes 로 옮기자**는 형태로 적어 달라.
- **장별 주장 ↔ 수치 ↔ 정본 ↔ 한정어** = §5 부록 표.
- **단어 수** (장 위 · 출처 줄 · 캡션 · 자리 표시 글 포함 · 바닥글 제외): p02 46 · p03 71 · **p04 118** (자리 표시 글 47 빼면 71) · p05 99 · **p06 120** (67 → 53) · **p07 151** · p08 104 (43 → 61) · **p09 133** (72 → 61) · p10 63 · p11 94 · p12 64 · p13 61 · **p14 113** · p15 62 · **p16 109** · p17 70 · (p18 참고문헌 156).  기준 10-13 덱은 61–126 이었다.

## 3. 고정 조건 — 이걸 바꾸자는 제안은 빼 달라

1. **숫자와 판정 문장은 정본에서 왔다** (`slide_sources.json` · 각 장 notes · §5).  값을 바꾸거나 더 센 문장 (최고 · 최적 · 개선율 · "수렴" · "실험과 일치") 을 제안하지 않는다.  장끼리 어긋나 보이면 **위치만** 짚어 달라.
   특히 **hold 값** — 8 팔 origin-factorial 의 σ_e 비 · 이득 · vox ≤ 0.15 격자값 · Richardson 극한 — 은 덱 어디에도 없어야 하고, 넣자는 제안도 안 된다.  격자 축에서 "lower bound" 는 금지 (철회됨) · 순수 SE 10 % 는 **보정 표적**이지 외부 앵커가 아니다 · 격자 비는 공개 3 점 (vox 0.4 · 0.3 · 0.25) 만.
2. **재사용 리포 그림은 세대 · 값 그대로**이고 다시 그리지 않는다.  **새 그림 4** 는 값 고정 (selftest) · 모양 제안은 된다.  우리 그림에 **문헌 값을 얹자**는 제안은 안 된다.
3. **템플릿** (표지 · 절 표지 · 로고 · 바닥글 · 쪽 번호 · 글꼴) 은 10-13 덱 그대로다.  장 위 글은 **영어만**.  내부 용어 (코드명 · 원장 ID · 기계명 · 세션명) 는 본문에 안 쓴다 (notes 에는 출처로 허용).
4. **19 장 · 순서 = 1저자 비준 개요 v1 (①–⑧)**.  장 추가 · 병합 · 순서 변경은 **P2** 로, 이유와 같이 (내용이 틀린 장은 예외 = P0).
5. **자리 표시 6 은 일부러 비웠다** — 채울 글 (무엇 · 출처 · 명령) 의 충분성과, 그 그림 없이도 장의 주장이 서는지만 봐 달라.
6. **참고문헌 14 = litdb 정본 카드 서지 그대로** — 기억으로 서지를 채우자는 제안은 안 된다.  빠진 원전 (Kirchhoff 망 · Holm 협착 등 · 정본 카드 없음 → 안 넣음) 은 그 처리의 적절성만.
7. 이 덱에 **인용 금지 값** (`claims.json` `quotation_ban`) 은 없다 — 넣자는 제안은 안 된다.
8. 표지 날짜 자리는 비워 둔다 (1저자 10-13).

이미 아는 것 (지적 안 해도 된다): p03 "densest of five" · p04 "73–75 % … contact necks" · p12 "×12, ×5.7" · p13 "matches the measured porosity order (n = 5)" 가 **가장 센 문장**이다 (Q-SEM-1 의 대상) · p13 오른쪽 SE σ_VM 열지도 = 0–150 MPa 선형 판 (벽 SE 제외) · p14 끝의 빨간 hold 문장 한 줄 · p12 F3 는 로그 축 · 본문 bullet 13 pt ≠ 10-13 덱 15 pt.

## 4. 확인 요청

- **Q-SEM-1 (수치 · 한정어)** — §5 표 기준으로 제목 문장 · 소불릿 · 캡션 · 결론 줄이 정본보다 **강하게** 또는 **빠뜨리고** 말한 곳.  장 번호 · 문장 · 정본의 값 · 문장 · 고칠 **영어 문구**.
- **Q-SEM-2 (금지값 · hold 값 · 내부 용어)** — `quotation_ban` 외에 hold 수치 (고정 조건 1) 가 덱 · 그림 · csv · notes 어디에도 없나.  슬라이드 본문에 내부 용어가 남았나 (생성기 검사는 정규식 하나다 — 표현이 다르면 새 나간다).
- **Q-SEM-3 (첫인상 · AI 티)** — `contact_sheet.jpg` 를 3 초 보고 한 줄.  그다음 장별로 생성기가 만든 덱처럼 보이게 하는 요소: **시각** (같은 틀 12 장 반복 · 점선 자리 표시 6 · 대칭 두 칸 · 꺾쇠 캡션 · 장식) 과 **글** (병렬 3 항 · 'X, not Y' · 표어 같은 결론 줄 · 너무 매끈한 제목 · em-dash).  요소마다 **장 번호 · 무엇 · 어떻게 바꿀지**.
- **Q-SEM-4 (10-13 문법과 같은가)** — 복제한 틀 위에 새로 짠 글 · 그림이 기준 덱과 같은 문법인가: ■ 제목 · bullet 크기 (13 vs 15) 와 줄 간격 · 파랑/빨강 강조의 양 · 점선 상자 · '< 캡션 >' + 결론 한 줄 · 출처 줄의 자리와 크기 · 여백 · 그림 세로 위치.  어느 쪽에 맞출지.
- **Q-SEM-5 (글 밀도)** — 교수가 '글이 많다' 고 느낄 장은 (후보 p07 · p09 · p04 · p06 · p14 · p16)?  장마다 **지울 문장 · notes 로 넘길 문장**을 콕 집어 달라.  목표 단어 수를 제안해도 좋다.
- **Q-SEM-6 (투영 가독성)** — 프로젝터 뒷줄에서 안 읽힐 것: 출처 줄 · 캡션 (10 pt) · 자리 표시 글 · **그림 속 글씨** (p03 3D 라벨 · p04 두 그래프 · p05 이력 그림 · p10 모식도 · p11 F2 · p13 열지도 · p15 G5/G3).  최소 글자 크기 기준과, 키울 것 / 뺄 것.
- **Q-SEM-7 (그림의 당위성 · 오독)** — 재사용 11 + 새 4 가 그 장의 주장을 받치는가, 장식인가?  **오독 위험**: p04 두 그래프 = Hertz 주 값 (Tabor 아님 · σ₀ 1.5 mS/cm) · p11 F2 의 y 축 "ratio, with / without SDCP" · p12 F3 로그 축 = 모델 ↔ 실험 (측정 조건 미확인) · p13 열지도 = 벽 SE 제외 · p15 G5a = **기하** tortuosity (수송 아님).  크기 · 자르기 · 캡션 · 출처 표기를 바꿀 것.  litdb 크롭 (`litdb/figures/<slug>/` · `figures.json`) 에 더 맞는 그림이 있으면 slug 와 그림 번호로 (선택).
- **Q-SEM-8 (자리 표시 6)** — 채울 글이 충분한가 (무엇 · 출처 · 명령) · 그 그림 없이도 장이 서는가 · 발표 전에 못 채우면 그 장을 어떻게 할지 (상자 유지 / 글로 대체 / 장 합치기 — 합치기는 P2).
- **Q-SEM-9 (흐름 · 제목 · 용어)** — ■ 제목만 이어 읽었을 때 ①–⑧ 이야기가 서나?  Problem 1–3 (p11–p13) → Progress (p14–p15) → Plan (p16) 연결.  용어의 분야 표준성 — "heterogeneous-technology pipeline" · "transport tortuosity" · "contact constriction" · "contact-free branch" · "stress-stop thickness" · "origin-replicated" · "DC polarization" · "voxel electronic gain" — 더 표준적인 말이 있으면 제안.  바꿀 제목 · 줄만 **영어 문구로**.
- **Q-SEM-10 (참고문헌 14)** — 덱 주장에 필요한 최소인가 · 과잉인가 · 빠진 필수 인용의 처리 (고정 조건 6) 가 적절한가 · 본문 ↔ 번호 연결 ([n]) 을 넣을지.
- **Q-SEM-11 (판정)** — 이대로 발표해도 되나: **GO / 조건부 GO / NO-GO**.  **P0** (발표 전 꼭 · 생성기 한 번으로 되는 글 · 크기 · 좌표) · **P1** (되도록) · **P2** (그림을 채운 v2 · 순서 변경) 로 나눠, 항목마다 **장 번호 · 대상 요소 · 구체 수정 (좌표 · pt · 문구)**.  끝에 장별 한 줄 표 `장 | 그대로 / 손질 / 다시 | 걸리는 것 | 고칠 것` 을 붙여 달라.

회신은 한국어로, 장 위에 들어갈 문구 제안만 영어로.  리포는 고치지 말고 회신 (판정문 마크다운 하나 — 우리가 리포 `docs/reviews/` 에 Codex 판정문으로 반입 · 필요하면 증거 폴더) 으로만.  수치 재현이 필요하면 핀에서 `python3 docs/seminar_20261013/figs/make_seminar_figs.py --selftest` (정본값 대조 · 철회값 스윕).

## 5. 부록 — 장별 주장 ↔ 수치 ↔ 정본 ↔ 한정어 (덱 notes 와 같음)

| # | 절 | 주장 (제목 문장) | 수치 | 정본 | 한정어 (덱 notes) |
|---|---|---|---|---|---|
| 2 | ① | Heterogeneous-technology pipeline — each stage anchored to experiment, never to one another | 없음 | `CLAUDE.md` DEM↔MPM frame [1]–[5] | — |
| 3 | ① | Soft-sphere DEM reproduces the composition dependence of porosity | porosity (exact union) 31.8 · 25.1 · 16.7 · 16.5 % (0 · 47 · 296 · 165 MPa) · 다섯 조성 20.59 · 18.67 · 17.67 · 16.49 · 16.90 % | `docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md` §6 · `docs/report_20261021/summary.json` G1 | 조성당 침대 1 · 시드 반복 없음 |
| 4 | ① | Kirchhoff network with contact constriction gives Li⁺ transport | tau2 7.24 · 5.97 · 5.45 · 5.03 · 5.29 · σ_ion (σ₀ 1.5) 0.0587–0.0893 mS/cm · 협착 전력 몫 73–75 % · 협착 뺀 tau2 1.25–1.79 | `docs/data/ps45_r45_network_g2_20261007/README.md` (값 · σ₀ 1.5 · 분해 절) | tau2 = φσ₀/σ (제곱근 아님) · Hertz 주 값 · 분해 = 모형 내부 비 · 7:3 ↔ 10:0 = 시드 산포 안 · 전류 경로 그림 = 자리 표시 |
| 5 | ② | What a rigid-sphere DEM cannot do | SE E 24 → 1.35 GPa · 문헌 22 편 (연화 0 · 캡 7 · 선형 이력 1 · 전역 감쇠 보고 0) · 감쇠 57.9 % → "58 %" | `docs/dem_governing_equations_background_20261011.md` §5 · §10.3 · §11 · 원장 `DEMP-01` | 문헌 집계 = 우리 분류 · 감쇠 = ps45 7:3 실측 (열린 결함) |
| 6 | ③ | MPM supplies the plastic half | 2D E 1.53 · σy 0.15 / 3D E 1.53 · ν 0.49 · σy 0.30 | `CLAUDE.md` MPM 절 | 그림 둘 = 자리 표시 (리포에 MPM 렌더 없음) |
| 7 | ③ | How the electrolyte parameters were fixed — what is not an external anchor | K 25.5 ≈ DFT B₀ 26.2 GPa · 순수 SE 10 % = 보정 표적 (랩 표본 · 미출판) | `CLAUDE.md` 3D MPM · `CL-94` · 10-08 1저자 확인 | "Heckel test" = DPC/jamming 교차검사 (`docs/mpm_dpc_cap_crosscheck.md`) |
| 8 | ③ | DEM-scaffold MPM — what agrees, what does not count as evidence | 두께 30.7 vs 30.28 µm · ε_sphere 1.13 % vs 15.6 % · 14.5 %p | `CLAUDE.md` scaffold + 09-09 정정 (CDX-16) · `fam_platen_prereg_20260812.md` §11 | 그림 = 자리 표시 |
| 9 | ④ | Voxelization turns morphology into a transport mesh | 없음 (4.04× 는 notes 만) | `CLAUDE.md` 두 솔버 표 · `CL-81` | contact-free 가지 · 그림 둘 = 자리 표시 |
| 10 | ⑤ | Additives enter at the voxel stage | Phase A ORDER-ROBUST 72/72 (104 팔) | `docs/data/phase_a_rep100_20260930/README.md` · `CL-60` · G6 | 등록 estimand = 순서만 · 증분 = 기술 보고 · 접촉 저항 미포함 |
| 11 | ⑥ | Problem 1 — grid dependence | 1.4215 → 1.1621 → 1.0849 · 1.0742 → 0.9926 → 0.9908 (vox 0.4 · 0.3 · 0.25) | `CL-24` (live · 공개값) | vox ≤ 0.15 값 (`CL-41`) 미게시 · "하한" (`CL-72`) 안 씀 · 증분비 · 멱법칙 불성립 |
| 12 | ⑥ | Problem 2 — absolute σ_e vs DC polarization | 54.0 · 70.6 ↔ 4.47 · 12.4 mS/cm · ps45 σ_e 0.391 · 0.406 · 0.402 · 0.375 · 0.467 | `sdcp_sigma_e_dcp_anchor_registration_20261012.md` · `docs/data/ps45_sigmae_factor_off_20261013/README.md` · Codex §6-1 | 실험 조건 미확인 · 재실행 등록 (결과 0) · 각주 = Codex §6-1 (notes 전문) |
| 13 | ⑥ | Problem 3 — compaction mechanics: load sharing | AM–AM σ_zz 기여 59.6 · 54.6 · 52.4 · 48.5 · 56.9 % | `docs/data/ps45_plane_load_20261007/README.md` · Codex 10-09 (`RB-01/02`) | 순서 일치 = 탐색 (n = 5 · 실험 = 추린 자료) · 되튐 해석 HOLD |
| 14 | ⑦ | Pre-registered, origin-replicated runs | 72/72 · replay 0.00000 % · R = 2.07 · Q = 0.84 · "7 external re-verification rounds" | `sdcp_gain_prereg_v2` · `phase_a_rep100` · `lee_abs_sigma_e_prereg` §5 · 재검증 1–7 | 8팔 비 · 이득 = hold (절차 · 판정만) · R 2.074 = Tier 1 (밴드 안 아님) |
| 15 | ⑦ | 194-bed dataset for ML | 130 + 64 · 관통 106/130 · τ_geo 1.3–4.2 · OOF R² 0.99 / 0.98 | 배포 v1.2 README · `summary.json` G5 · `lhs_ml_crosscheck_20261005` | 기하 tortuosity ≠ 수송 |
| 16 | ⑧ | Next steps | 없음 | Rint v3.1 · FAM §12 · 언로딩 §13 · `hetero_thesis.md` §4 | 전부 예정 |
| 17 | 요약 | What the pipeline can and cannot say today | 없음 | 3–15 장 | — |
| 18 | 참고문헌 | 14 편 | — | litdb 정본 카드 서지 그대로 (기억으로 채운 칸 없음) | — |

## 6. 동봉 (ZIP)

- `seminar_20261013_draft.pptx` (리포 밖) · `seminar_20261013_draft.pdf` · `render/p-01 … p-19.png` + `contact_sheet.jpg` · 리포 `docs/seminar_20261013/` (생성기 · 그림 4 + svg · csv · `slide_sources.json` · `slide_text_draft3.md` · `outline_v1.md` · README) · 이 요청서.
- 양식 = 1저자 10-13 연구세미나 덱 (리포 밖 · 생성기 템플릿) — 밀도 · 장 틀 기준.  동봉하지 않았다 (생성기 재실행이 필요하면 1저자가 따로).
