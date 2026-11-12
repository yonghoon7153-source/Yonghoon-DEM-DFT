# 대피 세션 (litdb 논문 에이전트 전용) 상태 메모 — 압축 · 재시작 뒤 먼저 읽는다

갱신 2026-11-12 14:00 KST. 진행 상태의 정본 = 정본 가지 `litdb/_curation/status.tsv` (이 메모는 보조).

## ★ 멈췄다가 이어갈 때 (토큰 소진 · 압축 · 컨테이너 재시작) — 이 절부터 읽는다

이 파일의 사본이 정본 가지 `litdb/_curation/evac/STATE.md` 에 있다 (도구 사본 = `litdb/_curation/evac/tools/`). 진행 상태의 정본은 `litdb/_curation/status.tsv`.

1. 상태 보기: `git -C /home/user/litdb-ctl fetch origin claude/friendly-meitner-lldvar` → `git -C /home/user/litdb-ctl rebase origin/claude/friendly-meitner-lldvar` → `status.tsv` 에서 세션 칸이 '대피' 인 줄을 본다. **'도는 중' = 멈출 때 돌던 편.**
2. 돌던 편의 뒷정리 (트리 1 = `/home/user/litdb-canon` · 트리 2 = `/home/user/litdb-canon2`):
   - `git -C <트리> status --short` 가 비어 있고 원격에 그 논문 카드 커밋이 있으면 (`git log origin/claude/friendly-meitner-lldvar --oneline | head`) 에이전트는 끝낸 것이다 → `python3 -I <scratchpad>/tools/finish.py --key <키> --slug <slug> --commit <sha> --memo "<한 줄>"` 로 마무리 (모음 그림 = `<scratchpad>/litcards/<slug>_sheet*.png` → 1저자에게 보냄).
   - 트리가 더럽거나 (쓰다 만 카드 · 그림) 커밋이 없으면 에이전트가 중간에 멈춘 것이다 → ① 에이전트가 살아 있으면 (ListAgents) SendMessage 로 "지시서대로 이어서 끝내라" ② 없으면 쓰다 만 것을 `git -C <트리> stash -u` 로 치워 두고 (지우지 않는다) 같은 키로 다시 띄운다 (정독 NN 그대로 · `launch.py`).
3. 컨테이너가 새로 떴으면 (scratchpad · 트리 · 패키지가 없다):
   - `python3 -m pip install "pymupdf==1.28.2" pillow numpy openpyxl` → 트리 셋을 다시 만든다 (아래 '자리' 절) → `python3 tools/litdb/extract_figures.py --selftest` 84/84.
   - 도구: 정본 `litdb/_curation/evac/tools/*` 를 scratchpad `tools/` 로 복사 (경로 상수 `SCR` 은 파일 위치에서 정해진다 · `intake.py` 의 업로드 폴더 상수 `UP` 은 새 세션 경로로 고친다).
   - PDF: 업로드 폴더에 남아 있으면 `tools/seen.json` 없이 `python3 -I tools/intake.py` 를 다시 돌려 stage · inbox 를 채운다 (queue.json 의 손으로 쓴 항목은 그대로 둔다). 남아 있지 않으면 1저자에게 다시 올려 달라고 한다 (status.tsv 에 받은 번호가 적혀 있다).
4. 다음 차례 = status.tsv 의 '차례 기다림' 을 N 번호순으로 · 한 번에 둘 (트리 1 · 2) · **기존 카드 보강 (68-1 zhang2026 · 68-2 lyu2025 · N-148 · N-149) 은 맨 끝** (다른 에이전트가 같은 카드에 관련 카드 줄을 더하므로).
5. 한 편이 끝날 때마다: 모음 그림을 1저자에게 보냄 → `finish.py --key … --next <다음 키> --tree <1|2>` (status · wishlist · 이어가기 자료 push + 다음 지시문 출력) → 그 지시문으로 `litdb-curator` 에이전트를 띄움 → 1저자에게 표로 보고 (12 줄 안 + 의도 대조 한 줄).

1저자가 새 세션에 붙여 넣을 말 (이 세션이 아예 사라졌을 때):
> [논문 에이전트 전용 세션 이어가기] 정본 가지 `claude/friendly-meitner-lldvar` 를 받아 `litdb/_curation/evac/STATE.md` 를 처음부터 끝까지 읽고 그대로 이어서 해줘. 쓰는 곳은 그 가지 하나뿐이고 코드 · 문서 가지에는 아무것도 커밋 · push 하지 않는다. PDF 는 내가 다시 올려 줄게.

## 역할 (1저자 11-12)

- 이 세션은 litdb 논문 에이전트 일 (카드 · 크롭 · 정본 push) 만 한다. 코드 · 문서 가지 (pqwtv8 · stoic) 에는 아무것도 커밋 · push 하지 않는다. 쓰는 곳 = 정본 가지 `claude/friendly-meitner-lldvar` 하나 (litdb 한정 상시 승인).
- 맡은 것 = 후보 표 2 · 3 순위 N-52 부터 (제외: N-57 · N-58 · N-59 · N-72 첫째 — N-119 는 제외했다가 1저자가 PDF 를 찾아 **취소** (11-12) = 후보로 남는다). 1 순위 N-1–N-51 은 본 세션 몫 — 하지 않는다.
- 에이전트는 한 번에 둘까지. 끝날 때마다: 모음 그림 (sheet png) 을 SendUserFile 로 보내고 · status.tsv 를 끝 (slug · 커밋) 으로 고쳐 push · 한국어 12 줄 안 보고 + 의도 대조 한 줄.
- 정본 push 규칙 = `litdb/_curation/README.md` 2 절 (시작 · push 직전 fetch · rebase · 충돌은 두 쪽 줄 다 살림 · 강제 push 금지 · INDEX_DEM 은 build_index.py 로 재생성).
- wishlist: 에이전트의 정독 출력 `## n` 절에서 내가 `litdb/_curation/wishlist.md` 로 옮긴다 (꼴 = 그 파일 머리 · 서지는 원문 목록 그대로 · 모르면 [미확인]).
- 보고 = 한국어 · 짧게 · 표 위주 · 숫자는 원문에서만. 커밋 끝 두 줄 = 그 세션의 공동 저자 줄 · 세션 줄 — scratchpad `tools/trailer.txt` 에 두고 정본에는 올리지 않는다 (새 세션은 자기 두 줄을 그 파일에 적는다 · 그 밖의 글 · 문서에는 모델 이름을 쓰지 않는다).

## 자리

| 무엇 | 경로 |
|---|---|
| 에이전트 트리 1 | `/home/user/litdb-canon` (가지 tmp-litdb-evac) |
| 에이전트 트리 2 | `/home/user/litdb-canon2` (가지 tmp-litdb-evac2) |
| 내 기록용 트리 (sparse · _curation 만) | `/home/user/litdb-ctl` (가지 tmp-litdb-evac-ctl) — status.tsv · wishlist.md 커밋은 여기서 |
| 받은 PDF | 두 트리의 `litdb/inbox/` (git 무시) · 원본 = `/root/.claude/uploads/<세션>/` · 단계 폴더 = scratchpad `stage_20261112/N-xx/` |
| 대기열 · 지시서 재료 | scratchpad `tools/queue.json` (N → nn · pdf · si · extra · bib · model · dup · note) |
| 지시서 만들기 + Agent 지시문 찍기 | `python3 -I <scratchpad>/tools/launch.py N-xx <트리> <가지>` → `briefs/brief_N-xx.md` + 짧은 지시문 |
| 모음 그림 도구 | `python3 -I <scratchpad>/tools/make_sheet.py --figdir … --out <scratchpad>/litcards/<slug>_sheet.png` |
| 환경 | PyMuPDF **1.28.2** (2.1 은 selftest 1 건 실패) · Pillow 13 · numpy · openpyxl · ffmpeg 있음. 재시작 뒤: `python3 -m pip install "pymupdf==1.28.2" pillow numpy openpyxl` → `extract_figures.py --selftest` 84/84 확인 |

재시작으로 트리가 사라졌으면: `git fetch origin claude/friendly-meitner-lldvar` → `git worktree add ../litdb-canon origin/claude/friendly-meitner-lldvar -b tmp-litdb-evac` (canon2 · ctl 도 같은 꼴 · ctl 은 `--no-checkout` + `git sparse-checkout set '/litdb/_curation/'`) → inbox 에 PDF 다시 복사.

## 대기열 (받은 PDF · 정독 NN) — 11-12 갱신 (1저자: "지금 먹여준 것들 다 논문 에이전트 돌린다")

차례 = 두 줄 (트리 1 · 트리 2) 로 번호순. 도는 중 / 끝은 status.tsv 를 본다. queue.json 키 = 표의 '키'.

| 키 | NN | 논문 | 메모 |
|---|---|---|---|
| N-52 | 101 | Taghikhani 2025 JMPS 198 106060 | 트리 1 · 11-12 10:40 KST 시작 |
| N-53 | 102 | Lu 2020 Joule 4 2746 (+SI) | 트리 2 · 11-12 10:40 KST 시작 |
| N-54 | 103 | Paulick 2015 Granular Matter 17 83 | 같은 저자 · 해 다른 카드 있음 |
| N-55 | 104 | Meyer 2017 JMPT 249 172 | |
| N-56 | 105 | Song 2025 Powder Technol 453 120667 (+SI) | 2 GPa 문턱 출처 |
| N-60 | 106 | Onoda–Liniger 1990 PRL 64 2727 | 스캔본 |
| N-61 | 107 | Meyer 2018 J Energy Storage 18 371 | N-55 가 끝난 뒤 (서로 가리키게) |
| N-62 | 108 | Cottrino 2013 Mater Charact 81 111 | |
| N-63 | 121 | Dixit 2022 ACS Energy Lett 7 3936 (본문 + 보충 PDF + xlsx 2) | 본문 PDF 받음 (11-12) |
| N-64 | 116 | Hayashi 2025 J Jpn Soc Powder Powder Metall 72 S1167 | |
| N-65 | 117 | Swinkels 1983 Acta metall 31 1829 | 스캔본 |
| N-66 | 118 | Ebner 2013 AEM 3 845 (+SI) | zhang2026 카드에 관련 카드 줄을 더한다 |
| N-67 | 119 | Ge 2022 Powder Technol 403 117366 | 〃 |
| N-68 | 122 | **Sonzogni 2024 Powder Technol 442 119891** (68-3 번 파일) | zhang2026 · lyu2025 카드에 관련 카드 줄 |
| X-68 | 115 | Kashkooli 2016 JPS 307 496 (+SI) (68 번 파일) | 후보 밖 · status.tsv 줄 이름 '후보 밖 (68 번 파일)' |
| N-69 | 120 | Stershic 2015 JPS 297 540 | zhang2026 카드에 관련 카드 줄 |
| N-70 | 109 | Xu 2023 Batteries & Supercaps 6 e202300371 (+SI · 영상 3) | 후보 표의 e202300525 는 원문과 다름 (카드 문제) |
| N-71 | 110 | Silbert 2001 PRE 64 051302 | |
| N-72 | 111 | Walton 1993 Mech Mater 16 239 (둘째) | 첫째는 제외 |
| N-73 | 112 | Chouchane–Franco 2021 B&S 4 1451 (+SI · 영상 1) | |
| N-74 | 113 | German 2014 Powder Technol 253 368 | |
| N-75 | 114 | Mullikin–Verbeek 1993 Bioimaging 1 6 | 스캔본 |
| X-68-1 | 123 | **기존 카드 보강** zhang2026_xct_dem_cathode_calendering_peel_calibration (68-1 번 파일) | ⚠ 맨 끝에 — N-66 · 67 · 68 · 69 가 다 끝난 뒤 (같은 카드를 건드린다) |
| X-68-2 | 124 | **기존 카드 보강** lyu2025_3d_dem_drying_calendering_lib (68-2 번 파일 + 영상 4) | ⚠ 맨 끝에 — N-68 이 끝난 뒤 |

3 순위 (N-76–N-129) 와 4-2 보강 (N-148 · N-149) 은 **11-12 에 전부 받았다** (1저자 "마지막이양"). 대기열 = `tools/queue.json` 79 항목 · status.tsv 에 한 줄씩 있다 (정독 NN 은 띄울 때 `launch.py` 가 '지금까지 쓴 가장 큰 NN + 1' 로 배정 — 125 부터).

| 키 | 논문 | 메모 |
|---|---|---|
| N-76 … N-129 | status.tsv 의 메모 칸에 서지 | 번호순 · 자동 항목 (서지 = PDF 문서 정보 + 첫 쪽 — 에이전트가 첫 쪽에서 다시 확인) |
| N-112-1 · N-112-2 | Li–McCarthy 2003 PRL 90 184301 · 2005 PRE 71 021305 | 후보 표 N-112 한 행 = 논문 둘 → 에이전트 둘 · status 줄 이름 'N-112 첫째' · 'N-112 둘째' |
| N-114 | Thiel–Lai–Hersey 1981 (114-1) + Egermann 1980 Powder Technol 26 235 (114-2 · 후보 밖) | 에이전트 하나가 카드 둘 → `finish.py` 는 첫 카드 slug 로 · 둘째 카드 slug · 커밋은 메모에 손으로 |
| N-105 | Ji 2025 Nat Commun 16 7667 | 보충 3 (260 MB) 은 원자료 xlsx · README 만 받음 |
| N-107 | Chouchane 2024 ACS Energy Lett | 참고 저장소 `/home/user/lescopenaccess/codes-and-data` (읽기 전용 · 실행 금지 · .pkl 열지 않음) |
| N-124 | Adam 2026 Mater Horiz 13 6380 | 참고 저장소 `/home/user/adama-wzr/effectivediffusivityfvm` (읽기 전용) |
| N-128 | Liu–Roters–Raabe 2024 Nat Commun 15 7970 | 참고 저장소 `/home/user/damask-multiphysics/damask` (태그 v2.0.2 · 읽기 전용 · 이 논문의 화학–역학 구현은 비공개 가지라고 원문이 적음) |
| N-148 | **기존 카드 보강** tron2023_rational_cathode_composite_optimization_lpscl ← 보충 자료 (SI PDF 4 쪽) | ⚠ 맨 끝에 |
| N-149 | **기존 카드 보강** boger2023_thermal_conductivity_argyrodite_lgps ← 본문 + 보충 두 파일 | ⚠ 맨 끝에 |

참고 저장소는 컨테이너가 새로 뜨면 사라진다 → 그 논문을 띄우기 전에 다시 받는다 (`GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 [--branch v2.0.2] https://github.com/<owner>/<repo> /home/user/<owner>/<repo>` · 소문자 경로 · 지시서의 경로와 같게).

## 열린 것

- **사용량 한도로 에이전트가 끊기면** ("out of usage credits" 로 failed 알림): 그 에이전트의 트리는 쓰다 만 채로 남는다 (미추적 그림 폴더 · `_sources.json` 수정). 1저자가 초기화권을 쓴 뒤 "이어서" 라고 하면 → `SendMessage(to=<그 에이전트 id>)` 로 "끊긴 자리에서 이어서 끝까지 · 트리 상태 그대로 · push 직전 fetch · rebase" 를 보낸다 (11-12 N-56 에서 이렇게 이었다). 에이전트 id 를 모르면 (세션이 바뀜) 위 2 절의 '없으면' 절차.
- 에이전트가 끝나면: ① 답장의 slug · 커밋을 정본에서 확인 ② 모음 그림을 열어 보고 SendUserFile ③ `finish.py --key … --slug … --commit … --memo … --next <다음 키> --tree <1|2>` ④ 찍힌 지시문으로 `litdb-curator` 에이전트 ⑤ 12 줄 보고 + 의도 대조 한 줄.
- 에이전트 한 편 = 43–72 분 · 30–75 만 토큰 (쪽 수 · 보충 자료에 따라). 남은 편수가 많으니 한도에 자주 닿을 수 있다 — 닿으면 위 절차.
- 키트 README 6 절 (환경 메모) 은 이 세션이 더했다 (`533c30320`).

- 11-12 끝난 것: N-52 (1ef7e9486) · N-53 (5fb0272d7) · N-54 (9c6ff51aa) · N-55 (b6f5f591c) · N-60 (063da4bc7). 도는 중 (14:00 KST 기준): N-56 (트리 2 · 한도로 한 번 끊겼다가 이어서) · N-61 (트리 1). 다음 차례: N-62 → N-63 → N-64 → N-65 → N-66 → N-67 → N-68 → X-68 → N-69 → N-70 → … → N-75 → N-76 … N-129 → 보강 넷 (X-68-1 · X-68-2 · N-148 · N-149).
