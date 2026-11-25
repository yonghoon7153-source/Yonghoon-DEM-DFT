---
title: "litdb 18편 병렬 정리 — 이어가기 카드 (2026-11-24 밤 · 세션이 끊겨도 이어지게)"
date: 2026-11-24
updated: 2026-11-24
tags: [handoff, litdb, curator, parallel, wad, lithiophilicity, void, sakamoto]
status: 끝
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: single-source
---

> ✅ **끝 (2026-11-24 낮 · 세션이 안 끊기고 다 했다)** — 18/18 digest · 합치기 `3679fd75` · 웹앱 그림 주석 파서 `adc62956` · W_ad DEM 보고서 8 절 `841e2834`. 18 번 slug 는 `chatterjee2025_diffuse_interface_metal_anode_void_model` (Na 계라 li_anode → metal_anode). 아래는 기록으로 남긴다.

# litdb 18편 병렬 정리 — 이어가기 카드

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자) 의 Li 친화성 · 공극 · Ag–C 층 문헌 보강. 사용자 요청 (2026-11-24): *'병렬로 논문에이전트 해서 litdb 에 저장 · 더 필요한 논문은 얘기 · 이 litdb 를 바탕으로 DEM-DFT 내용 추가 (html 에 정리)'* · *'세션 재시작해도 사라지는 거 없이 이어질 수 있게'*.

## 1. 지금 상태 (2026-11-24 밤)
- 논문 에이전트 (`litdb-curator`) 18 개가 이 세션 안에서 돈다 — 1–8 먼저, 9–18 뒤. **공유 파일은 안 건드린다.** 편마다 쓰는 것은 셋뿐:
  `litdb/papers/<slug>.md` · `litdb/figures/<slug>/` · 끝 보고 `litdb/_curation/batch_2026_11_24/<slug>.report.md` (**이 파일이 있으면 그 편은 끝**).
- 목록 = **`litdb/_curation/batch_2026_11_24/batch.json`** — 번호 · slug · 서지 · inbox 파일 · sha256 · 올린 원래 이름 · Jeff Sakamoto 여부 · 에이전트 규칙 · 끝 보고 규격 (a)–(g).
- 저장: 중간 커밋 (f241c243 · b60590e6 · 5870260f) + 20 분마다 자동 커밋 (세 경로만 · 세션이 살아 있는 동안). 중간본이다 — 완성 여부는 report 파일로 본다.
- 입력 원본 (PDF · 동영상 · 16 번 코드 · 데이터, 합계 192 MB) 은 **git 이 무시하는 `litdb/inbox/`** 에 있다 → 기계가 바뀌면 없다. 사용자 PC 원본: `C:\Users\Administrator\Desktop\읽어야되는 논문\DFT-DEM-COMSOL\261124 논문 추가\` (번호 붙은 이름 = batch.json `uploaded_as`).

## 2. 이어가는 법 (새 세션)
1. **어디까지 됐나**:
   ```
   python3 -c "
   import json,os
   b=json.load(open('litdb/_curation/batch_2026_11_24/batch.json',encoding='utf-8'))
   for p in b['papers']:
       s=p['slug'].split(' ')[0]; rep=f'litdb/_curation/batch_2026_11_24/{s}.report.md'
       dg=f'litdb/papers/{s}.md'; inb=all(os.path.exists(f['inbox']) for f in p['inbox_files'])
       print(p['n'], '끝' if os.path.exists(rep) else ('중간' if os.path.exists(dg) else '시작 전'), '· inbox', '있음' if inb else '없음', '·', s)
   "
   ```
   (18 번 slug 는 에이전트가 연도를 정한다 — `ls litdb/papers | grep chatterjee` 로 찾는다.)
2. **끊긴 편 (report 없음)**: inbox 파일이 없으면 사용자에게 **그 편 파일만** PC 폴더에서 다시 올려 달라고 한다 → sha256 을 batch.json 과 대조 → batch.json 의 `inbox` 이름으로 복사.
3. 같은 규칙 (batch.json `agent.prompt_rules` · `report_spec`) 으로 `litdb-curator` 를 다시 띄운다 — digest 가 있으면 **그 위에 이어서** 쓰라고 한다 (처음부터 다시 쓰지 않는다).
4. **다 끝나면 합치기** (메인 세션 한 번에):
   - report (a) → `litdb/INDEX.md` 행 (Jeff Sakamoto 공저면 둘째 칸 맨 앞 `🏷 **Jeff Sakamoto 공저** · `) · DEM 축이면 `python3 tools/litdb/build_index.py` 로 `INDEX_DEM.md` 생성
   - report (b) → `comparison_vs_ours.md` / `comparison_vs_ours_DEM.md` · (c) → `pdf_map.tsv`
   - 그림 출처 색인 다시: `python3 -c "import sys; sys.path.insert(0,'tools/litdb'); import extract_figures as E; E._write_sources_index()"`
   - `python3 tools/litdb/build_index.py --check` 0 건 · 웹앱 `/literature` 에서 Jeff Sakamoto 칩 수 확인 (데스크톱 · 폰) · 커밋 · push
5. **추가로 먹일 논문**: report (d) 를 모아 중복 · litdb 에 있는 것을 빼고 최근 2 년 먼저 사용자에게 목록으로.
6. **DEM-DFT 보고서 HTML 보강**: report (e) 바탕으로 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` 7 절 (Li 친화성) 과 연속체 입력 쪽에 문헌 근거 절. 규칙: 내부 사정 빼기 · 우리 W 값 비인용 · 출처 랩 표기 (*저널*, 권, 첫 쪽 (연도)) · 기준표 10 점 · 데스크톱 + 폰 렌더 확인 · "웹앱도 고쳤다 (공유 보고서)".

## 3. 따로 받은 것
- **16 번 Sup3 (코드 · 데이터)**: `litdb/inbox/shi2026_sup3/codes/` — `script_for_pore.m` · `script_2D_void_fraction.m` · `script_sparse.m` · `data/*.mat` 29 개 (MATLAB v5). 사용자가 원본 zip (38 MB) 을 코드 · 데이터 둘로 나눠 올렸다 — sha256: code `1C1516C9…` · part1 `958E0538…` · part2 `87AF7D19…` (전체는 batch.json `extra`). 데이터는 litdb 로 복사하지 않는다.
- **18 번 코드**: 공개 저장소 `souravmat-git/moose-batmodelling` (커밋 3e44674 · 읽기 전용 · 저장소 밖 `/home/user/souravmat-git/moose-batmodelling`). 다시 받기: batch.json `extra.18_code_repo.reclone`.

## 4. 반론 · 한계
- 에이전트는 이 세션 프로세스 안에서 돈다 — 컨테이너가 바뀌면 같이 멈춘다. 그때는 2 절대로 끊긴 편만 다시 띄운다 (끝 보고 파일이 판정 기준).
- 중간 커밋에는 쓰다 만 digest 가 들어 있다 — INDEX 에 올리기 전에는 완성본으로 읽지 않는다.
