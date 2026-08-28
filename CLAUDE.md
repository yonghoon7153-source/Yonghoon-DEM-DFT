# CLAUDE.md — Yonghoon-DEM-DFT 프로젝트 지침

전고체전지(황화물 SE) 계산 캠페인 repo. 아래 규칙은 세션이 바뀌어도 유지되는 표준이다.

## 소통
- 한국어 대화체로 답한다. 문어체/번역체("-했다") 금지. 짧고 구체적으로.
- 그림 라벨·캡션은 영어만 (사용자 뷰어에서 한글 폰트 깨짐).
- 사용자는 물리는 알지만 계산 세부는 배우는 중 — 새 개념은 한 단계씩 설명.
- 원격 서버 작업은 "붙여넣기 블록 제공 → 사용자가 실행 → 출력 회수" 워크플로.

## 데이터 규율 (어기면 안 되는 것)
- **Band gap**: fixed-occupations nscf의 VBM/CBM 고유값만 인정. DOS-threshold 판독 금지 (~0.3 eV 과소).
  Canonical (db/properties/electronic.json): comp1 2.066 / modelc(LPSCl1.6) 2.099 / +B2O3 1.9671 / LPSOCl(+O) 2.2309 eV.
- **BVSE** (tools/comp1_v3/): softBV Li–X R0 = S 2.105 / Cl 2.249 / O 1.466, b=0.37; BVSE=(BVS−1)²;
  ~0.25 Å voxel; 채널% = above-min ≤ iso. **정량·순위는 원본 주기셀 값만** 인용(큐빅 박스는 표시용, ±1.3%p 표본 편차).
- **MLIP-MD** (tools/modelc_v3/, tools/ionic/): UMA-s-1p1(omat), Langevin NVT, dt 2 fs, friction 0.02,
  equilib 5 ps / prod 200 ps, **MSD 창 2–50 ps 고정**, 아레니우스는 600/800/1000 K 3점(400/500 K 제외 판정),
  σ는 Nernst–Einstein(Haven=1) — **절대값 인용 금지, 비율도 멀티시드 판정만**(단일시드 1.33× 철회 사례, SEMIFINAL 2026-07-09); Ea 오차막대는 600 K 3-시드.
- **UMA는 Li₃N에 사용 금지** (2026-06 결정론적 편향 판정). LPSCl 계열 MD에는 UMA가 검증된 표준.
- 평균류 지표(site mean-3p 등)는 **그림 표시 창과 동일한 창**(-8..0 eV)으로 계산·인용.
- 슬랩 계산은 기하 승계(verified-carry: 마지막 ATOMIC_POSITIONS 스플라이스 + 검증) + local-TF/저β 믹싱.

## 그림 하우스 스타일 (모든 새 그림)
- `tools/figures/house_style.py` import (INK #1f2937, MUT #6b7280; 원소 팔레트 Li #0d9488 / P #7c3aed /
  S #c05621 / Cl #65a30d / O #be123c / B #0284c7; gap 밴드 #fef9c3 + #2563eb dashed).
- spines top/right 제거, dpi 300, 같은 계열 그림은 기존 family와 양식 통일.
- 데이터 그림은 **Origin-ready CSV를 동시 출력**해 db/properties/에 등록 (열 이름 명시적).
- .opju 자동화는 클라우드에선 불가 — 로컬 Windows Claude Code + originpro로 (CSV가 우리 쪽 절반).

## 계산 자원 (2026-07 기준)
- **KISTI** neuron(x3430a02): Slurm, QOS 제출 제한 — scancel 직후 재제출 금지(카운터 지연). pseudo는
  /scratch/x3430a02/kgy/manuscript_support/pseudo.
- **kgy** (RTX3090, QE-GPU + uma env): ssh kgy@59.12.161.91.
- **gabia** (A6000 단일 GPU, QE-GPU + fairchem/UMA): root@121.78.116.27. **pw.x와 UMA 동시 실행 금지**
  (VRAM 47/48 GB 점유 사례) — nvidia-smi로 확인 후 실행.
- **desktop WSL**: ORCA r2SCAN-3c (SDCP 분자 계열).
- 공통: 실행 스크립트에 pgrep 중복실행 가드, 출력 grep은 `grep -a`(NUL 오염 대비), watch 스크립트 관례 유지.

## Git
- 브랜치 **claude/friendly-meitner-lldvar** 에만 커밋/푸시. PR 생성 금지(요청 시에만).
- force-push는 --force-with-lease만. 커밋 메시지에 모델 ID 넣지 않기.

## VESTA 산출물
- .vesta 파일은 **ASCII 전용 + CRLF** (em-dash 등 비ASCII가 IMPORT_DENSITY 파싱을 깨뜨린 사례).
- 부피 데이터 cube는 aboveMin 관례(맵 최소 빼기), .vesta + .cube를 쌍으로 배포(같은 폴더).
- 구조 배포는 xyz + POSCAR(.vasp) 페어 (xyz는 격자 없음 → Boundary 타일링은 vasp).

## litdb (문헌)
- "논문 에이전트" 요청 = litdb-curator 서브에이전트: litdb/papers/ digest + INDEX.md + comparison_vs_ours.md 갱신.
- 문헌 수치는 소환값 — 우리 db 절대값과 섞지 않기 (방법 명시 없이 이식 금지).
- **litdb 를 볼 때는 `litdb/figures/<slug>/` 의 크로핑 PNG 를 Read 로 같이 본다** (digest 텍스트만
  보고 답하지 않기). 어느 그림인지는 그 폴더의 figures.json caption 으로 찾고, 없으면
  `tools/litdb/extract_figures.py --inbox` 로 먼저 만든다. **본 그림/안 본 그림을 구분해 말한다.**
  그림에서만 읽은 값은 `figure-read ≈` 표기. 표(tab_*.png)는 PDF 텍스트가 더 정확하다.

## 원고 작성
- kb/templates/manuscript_prompts.md 의 템플릿 사용 (figure 단위 요청, Wiley 스타일 R&D, 학술 5문장 재번역,
  로컬 PDF 기반 reference list).
- 레퍼런스는 링크가 아니라 **로컬 PDF/litdb digest 기준**으로 작성, 인용 역할 확인 후 삽입(2026-07 Kim/Cui 교훈).

## 코드 규율 (2026-08-11 채택)
- **새 스크립트 쓰기 전 기존 것부터 찾는다** (tools/ 에 py 305 · sh 106 · 62k줄 — 중복이 진짜 위험).
  사다리: ① 이게 있어야 하나 → ② tools/ 에 이미 있나(`grep -rl`) → ③ 기존 도구에 플래그 추가로 되나
  → ④ stdlib 로 되나 → 그 다음에 새 파일. **기존 도구 확장이 새 파일보다 항상 낫다.**
- 물리 규약(MSD 창 2–50 ps, 자유절편 D)은 여러 파일에 복사돼 있다 — 수정하면
  `python3 tools/convention_check.py` 로 갈라졌는지 확인 (0 위반 유지, 예외는 EXEMPT 에 **사유 명시**).
- **새 도구는 `--selftest` 를 단다 — 음성 경로(틀린 입력을 잡아내는지) 포함.**
  양성만 있는 selftest 는 통과해도 아무것도 보증 못 한다 (vasp 번들 v2 선례).
- 도구 docstring 에 **"이 도구가 못 하는 것"** 을 적는다 (한계 은폐가 제일 비싼 버그).
- 진행 보고·붙여넣기 출력 해석은 **짧게**. 단, 새 개념 설명은 위 소통 규칙대로 한 단계씩 — 압축하지 않는다.
- **도구 출력은 기본이 요약이다.** 매번 찍히는 목록은 플래그 뒤로 숨긴다
  (`kb_wiki.py lint` 은 레거시 49건을 한 줄로 — 목록은 `--legacy`. 이 한 건이 출력 81% 감소).

## 계산 규율 — **던지기 전에 estimand** (2026-08-28 채택)

- **새 물리량을 계산하기 전에 `kb/templates/estimand_card.md` 를 채운다.**
  리뷰에 보내는 것은 번들이 아니라 그 카드의 §1–3 이다 — *"무엇을 원하고, 어떤 식으로 재고,
  **이 계에서 그게 잘 정의되는가**"*.
- 채택 배경: SDCP-doped 흡착에너지를 **여덟 번** 계산했고 여덟 번 반려됐다. 받은 리뷰는
  전부 *"제대로 돌렸나"*(무결성·해시·INCAR·pin·게이트)였고 전부 통과했다.
  *"맞는 양을 재고 있나"* 는 여덟 번째에야 물었고 즉시 P0 가 나왔다.
  (⚠ 회신 N: "일곱 번은 안 돌려도 됐다" 는 철회 — 카드 블라인드 재생 시 확실히 잡는 것은
  #7–8 정도다. 여덟 실패의 원인은 하나가 아니라 층위다.)
- **판정 기준 (회신 N 문구): admissible state 가 여럿인데 선택·집계 규칙이 없으면
  scalar estimand 는 정의되지 않는다.** 열린 껍질 · 자성 기판 · 산화환원 활성은 그 위험
  신호다. 걸리면 상태를 선언해 `X(상태)` 로 정의하거나, 집계 규칙(최저/앙상블/분포)을
  미리 적거나, 질문을 바꾼다.
- estimand·마감 판정은 **`db/governance/decisions.json` 에 등록**한다 (proposed → 사람이
  ratify 해야 active). 해석 레지스트리는 이미 있다 — 새로 만들지 말고 그 그래프에 붙인다.
- **검증 게이트를 결과 보기 전에 정한다.** 물리적으로 정수여야 할 양(고립 doublet 총자화 =
  1.000 등)이 정수인지부터. 실측: `mol_doped` 자화가 **0.175** 인 채로 여덟 번의 기준이 됐다.
- **규약 대조 30초**: `grep -rl "<양이름>" kb/` — 이미 판정이 있으면 그게 이긴다.

## 마감 규율 — **닫힘 조건을 먼저 박는다** (2026-08-28 채택)

- 캠페인을 닫을 때 **`db/properties/<계>_closed_<날짜>.json`** 를 남긴다:
  확정값 · **허용 서술(이대로만)** · **금지 서술** · **재개 조건(이것들만)**.
- 순서가 핵심이다 — 데이터를 보고 "닫혔다" 고 판단하지 않는다. **조건을 먼저 정하고,
  그게 채워졌으므로 닫는다.** SDCP 는 조건 없이 두 번 닫았다가 두 번 물렸다
  (2026-07-17 doped v1 철회 · 2026-08-28 회신 M 마감보류).
- **재개 조건 밖의 이유로 다시 열지 않는다.** "새 자세를 하나 더 봤다" 는 재개 사유가 아니다.
- 선례: `db/properties/sdcp_neutral_closed_2026_08_28.json`

## 컨텍스트 절약 (2026-08-11)
- 자동 compact 은 **기본값(실제 한계 근처)** 으로 둔다. `autoCompactWindow` 로 창을 좁혀
  50% 발동을 걸었다가 **압축 루프**를 맞았다(2026-08-11 철회 — 요약+파일 재독이 곧바로
  임계를 다시 넘겨 연속 3회 압축, 다른 브랜치 세션 사실상 정지). 다시 넣지 않는다.
  대신 상태줄(`tools/claude/statusline.py`)이 사용률을 상시 표시 — 70%↑ 에서 손으로 `/compact`.
- 읽기는 **부분 읽기 우선**: 큰 파일은 offset/limit, 검색은 head_limit.
  `kb/index.md`(25 KB)·`kb/open_items.md`(72 KB)는 **통째로 읽지 말고 grep**.
- **방금 쓴 파일을 다시 읽지 않는다.** 만든 파일 내용을 답변에 다시 붙여넣지 않는다.
- 긴 출력은 파일로 떨군 뒤 grep (`… > /tmp/x.log` → 필요한 줄만).
- 세션을 새로 여는 것보다 **이어가는 게 싸다**(프롬프트 캐시). 정리는 `/clear` 말고 `/compact` —
  `/clear` 는 CLAUDE.md·kb 재독을 다시 유발한다.
- 진짜 절감은 **재논증 방지**다: 이미 판정된 건 kb 카드에서 확인하고 다시 논증하지 않는다.

## kb 위키 규율 (2026-08-11 채택)
- kb 문서를 만들거나 크게 고치기 전에 **kb/SCHEMA.md 를 읽는다** (규칙 원본).
- 새 문서는 `python3 tools/kb_wiki.py new <dir> <slug>` 로 생성 (frontmatter 필수 — 기존 문서 소급 없음).
- 답이 안 난 반복 질문 → `kb/questions/` 카드, 논지 방어 → `kb/syntheses/` 카드 (반론 절 삭제 금지).
- `explored:` 는 **사람만** true 로 바꾼다. 근거가 하나뿐이면 `confidence: high` 금지.
- 마무리: `python3 tools/kb_wiki.py index` 재생성 + `lint` **0 errors** (kb/index.md 손편집 금지).
- 채택 배경: kb/methodology/llm_wiki_adoption_2026_08_11.md.
