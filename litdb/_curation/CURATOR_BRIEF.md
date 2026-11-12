> ⚠ 이 파일은 본 세션 (stoic) scratchpad 에서 옮긴 사본이다 (2026-11-12).  안의 경로는 이렇게 읽는다: `…/scratchpad/litread/` = 이 폴더의 `reading/` (정독 출력 자리 · 커밋 · push) · `…/scratchpad/litcards/` = 너의 세션 scratchpad (모음 그림은 만든 뒤 1저자에게 보낸다) · `/home/user/litdb-canon` · `litdb-canon2` = 너의 정본 작업 트리 · `/home/user/Yonghoon-DEM-DFT` = 리포 본 트리 (쓰지 않는다) · "본 세션" = 이 키트를 만든 stoic 세션.

# 논문 에이전트 공통 지시 (2026-11-10 · 본 세션 · [DEM 우선 (수영)] 문헌 보강)

1저자가 PDF 를 주었다. 한 번에 **논문 하나**를 정본 litdb 에 넣는다 (카드 + 그림 크롭 + 인덱스 + 비교 문서 + push). 논문별 사항은 프롬프트에 있다.

## 1. 자리

- 정본 = 원격 가지 `claude/friendly-meitner-lldvar` 의 `litdb/` 하나뿐이다. 네 작업 트리와 가지는 프롬프트가 알려 준다 (그 트리에서만 쓴다).
- `/home/user/Yonghoon-DEM-DFT` (다른 가지의 본 트리) 의 파일은 만들거나 고치지 않는다. 그 안의 `litdb/` 는 동결 사본이다.
- PDF 는 작업 트리의 `litdb/inbox/` 에 있다 (git 이 무시하는 폴더 · 커밋되지 않는다). PDF 는 읽기만 한다.
- 정본 가지에는 다른 세션이 오늘도 커밋한다 (litdb 밖의 파일 포함). 그래서 **시작할 때와 push 직전에** fetch 한다.

## 2. 순서

1. `git fetch origin claude/friendly-meitner-lldvar` → 작업 트리가 깨끗한지 보고 `git rebase origin/claude/friendly-meitner-lldvar` (시작점 맞추기).
2. **중복 확인** (인덱스가 아니라 파일 목록으로): `git ls-tree -r --name-only origin/claude/friendly-meitner-lldvar litdb/papers/` 와 `git grep -i '<DOI 또는 제목 낱말>' origin/claude/friendly-meitner-lldvar -- 'litdb/papers/*.md'`. 이미 카드가 있으면 새 카드를 만들지 말고 멈추고 보고한다 (프롬프트가 "기존 카드 보강" 이라고 한 경우만 그 카드를 고친다).
3. **원문을 직접 읽는다** (본문 + 보충 자료 전부). 서지 (저자 · 제목 · 학술지 · 권 · 쪽 · 연도 · DOI) 는 PDF 첫 쪽과 머리글에서 확인한다. 프롬프트에 적힌 서지는 1저자가 준 메모일 뿐이니 원문과 다르면 원문을 따르고 다른 점을 보고한다.
4. **그림 크롭**: `python3 tools/litdb/extract_figures.py --slug <slug> --pdf "litdb/inbox/<파일>.pdf" [--pdf "<보충>.pdf"] --clean` (도구 머리 주석의 사용법을 먼저 읽는다). 만든 그림을 **전부 직접 열어 본다**. 잘린 축 · 캡션 누락 · 이웃 문단이 섞임 · 두 쪽에 걸친 표 · 빈 그림은 다시 자르고, 고친 그림은 `figures.json` 에 그 도구의 관례대로 표지한다 (recrop · manual_crop · `figures.json` 은 indent=1). 논문의 그림 · 표를 빠짐없이 (본문 + 보충).
5. **카드** `litdb/papers/<slug>.md`: 같은 계열의 기존 카드 꼴을 그대로 따른다 (프롬프트가 본으로 삼을 카드를 알려 준다 · 절 번호 체계 · 머리 요약 상자 · 서지 표 · 그림 표 · "우리 DEM + MPM 과 비교" · 행동 · [미확인] 목록). 카드만 읽어도 논문을 읽은 것과 같게 쓴다 (길이 제한 없음).
   - 숫자마다 원문 위치 (쪽 · 식 · 그림 · 표) 와 표지를 단다: 본문에 인쇄된 값 / 그림에서 읽은 값 ([판독]) / 카드가 계산한 값 ([카드 산술] · 식을 같이) / 원문에 없음 ([미확인]). 기억이나 검색으로 채우지 않는다.
   - 계산 방법 (모델 식 · 접촉 법칙 · 수치 기법 · 입자 수 · 차원 · 격자 / 요소 수 · 계산 비용 · 맞춘 값과 맞춘 대상 · 검증) 을 빠짐없이.
   - 이 묶음의 목적 때문에 아래를 **꼭** 넣는다: (i) 논문이 DEM (단단한 구 · 점접촉) 의 한계를 말한 문장과 위치 (원문 문장을 따옴표로) (ii) 입자의 소성 · 큰 변형을 계산에 넣기 어려운 이유와 그 논문의 우회 · 비용 (iii) 2D 인지 3D 인지와 2D → 3D 전이에 대한 원문의 말 (iv) 압력을 뺄 때의 거동을 다뤘는지.
   - 다른 재료의 값을 우리 재료 (LPSCl · NCM) 값처럼 쓰지 않는다. 절대값 전이가 되는지 안 되는지를 머리 요약에 적는다.
6. **인덱스 · 비교 문서**: `litdb/INDEX_DEM.md` 의 맞는 절에 한 줄 (프롬프트가 절을 알려 준다 · 이웃 줄과 같은 칸 구성) 과 그 절 · 문서의 편수 표기 갱신, `litdb/comparison_vs_ours_DEM.md` 의 맞는 절에 보탬. `python3 tools/litdb/build_index.py --check` 가 있으면 돌려 맞춘다. SE 축 `litdb/INDEX.md` 는 그 축에 해당할 때만.
7. **커밋 · push**: litdb (와 그 그림) 만 커밋한다. 메시지는 한국어 한두 줄 + 끝에 아래 두 줄. 모델 이름 · ID 를 그 밖의 어디에도 쓰지 않는다.
   ```
   Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
   Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft
   ```
   push 직전: `git fetch origin claude/friendly-meitner-lldvar && git rebase origin/claude/friendly-meitner-lldvar` (충돌이 나면 양쪽 줄을 모두 살린다 · 인덱스 편수는 다시 센다) → `git push origin HEAD:claude/friendly-meitner-lldvar` (fast-forward 만 · force 금지). 거절되면 fetch · rebase 부터 다시 (세 번까지). 그래도 안 되면 멈추고 보고한다.
8. **정독 표에 넣을 줄** (본 세션이 모은다): `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/litread/BRIEF.md` 의 3–5 절 양식대로 이 논문의 한 줄 (칸 8 개 · 탭 구분 · 머리 행 없음) 을 `…/scratchpad/litread/batch_NN.tsv` 에, 질문 a–n 의 근거를 `…/scratchpad/litread/batch_NN_findings.md` 에 쓴다 (NN 은 프롬프트가 준다 · 절 머리는 `## a — …` 꼴로 a 부터 n 까지 · 끝에 `## 카드 문제`). 질문 n (논문 에이전트 후보) 은 이 논문이 인용했지만 정본에 카드가 없는 논문 가운데 a–m 에 직접 쓸 만한 것 — 많아야 다섯 · 서지는 원문 참고문헌 목록에 적힌 그대로.
9. **검토용 모음 그림**: 만든 크롭을 한 장에 작게 모아 (이름표 포함) `…/scratchpad/litcards/<slug>_sheet.png` 로 둔다 (본 세션이 한눈에 확인한다). 스크립트는 scratchpad 에 둔다.

## 2-1. 크롭 품질 (1저자 11-11: "잘 크롭핑해서")

- 그림 · 표는 **빠짐없이**, 그리고 **핵심 식을 식 번호별로 따로** 자른다 (지배 방정식 · 구성식 · 접촉 · 이산화 · 그 논문 고유의 결합 식) — 1저자가 보고서의 MPM 절에 그대로 붙여 쓴다.
- 렌더 해상도는 도구 기본값보다 낮추지 않는다 (작은 글씨가 깨지면 올린다). 여백은 사방 고르게 · 식 번호 포함 · 이웃 문단 · 쪽 머리글 · 쪽 번호가 섞이지 않게 · 여러 줄 식은 한 장에 · 그림은 캡션까지 한 장에 (도구 관례대로).
- 식 크롭의 파일 이름 · `figures.json` 항목은 도구 관례를 따른다 (손 크롭 표지 · 쪽 번호 · 식 번호 · 한 줄 뜻). 도구에 식 크롭 관례가 없으면 기존 MPM 카드의 그림 폴더 (예: `litdb/figures/bardenhagen2001_mpm_improved_contact_granular_stress_waves/` · `litdb/figures/hu2018_mls_mpm_cpic_two_way_rigid_coupling/`) 가 쓴 꼴을 따른다.
- 자른 것을 **전부 직접 열어 본다**. 모음 그림 (9 번) 에 식 크롭도 넣는다. 다시 자른 것의 수를 답장에 적는다.

## 3. 답장 (12 줄 안)

slug · 정본에 push 된 커밋 sha · 카드 줄 수 · 그림 수 (다시 자른 수) · 넣은 인덱스 절 · 원문과 달랐던 서지 · 남은 [미확인] 두세 개 · DEM 한계 / 소성 관련 핵심 한두 줄 · 문제 (있으면). 카드 본문을 답장에 붙이지 않는다.
