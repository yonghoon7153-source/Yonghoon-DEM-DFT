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

## 원고 작성
- kb/templates/manuscript_prompts.md 의 템플릿 사용 (figure 단위 요청, Wiley 스타일 R&D, 학술 5문장 재번역,
  로컬 PDF 기반 reference list).
- 레퍼런스는 링크가 아니라 **로컬 PDF/litdb digest 기준**으로 작성, 인용 역할 확인 후 삽입(2026-07 Kim/Cui 교훈).
