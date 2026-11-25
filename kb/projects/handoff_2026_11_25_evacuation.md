---
title: "대피 인계 — 2026-11-25 (friendly 세션 토큰 소진 예상 · 오버나잇 → 서브 브랜치 · 머지 때 충돌 0 · b2o3 11b gabia 진행 · B 자리 DFT 11-28/29 예약 (V100))"
date: 2026-11-25
updated: 2026-11-25
tags: [handoff, session, evacuation, branch, merge, b2o3, dft, scf, v100, uma, md, wad, litdb, webapp]
status: 진행
kind: project
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# 대피 인계 — 2026-11-25

> 본 세션 (`claude/friendly-meitner-lldvar` · session …CTzs) 이 오버나잇 동안 토큰을 다 쓸 것 같아서, 다음은 **서브 대시보드의 서브 브랜치**에서 이어 간다
> (사용자 2026-11-25 *"오늘 오버나잇으로 돌다가 토큰 다 될거 같긴하거든 · 관련해서 평소처럼 서브 브랜치로 갈때 필요한 프롬프트 주고 머지할때 충돌안나게 해줘요"*).
> 선례: `handoff_2026_11_20_evacuation.md` (대피) → `handoff_2026_11_23_return_to_origin.md` (복귀).
>
> **충돌 0 의 조건은 하나다 — 대피하는 동안 friendly 에 아무도 쓰지 않는다.** 이 카드를 담은 커밋 ("Evacuation handoff card 2026-11-25") 이 friendly 세션의 마지막 커밋이다.
> 원격 (kgy · gabia · V100) 블록도 friendly 로 push 하지 않는다. 그러면 복귀는 `git merge --ff-only` 한 줄이다 (사용자 로컬 웹앱 메모 커밋이 끼면 ■6 의 --no-ff 갈래).
>
> ⚠ 원격 상태 마지막 실측 = **2026-11-25 13:19 KST** (gabia 11b watch) · kgy 큐 세움 확인 11-25 10:4x (블록 5c 출력). 그 뒤는 사용자가 붙여 주는 출력으로만 쓴다.

## 0. 새 세션 (서브) 에 붙여 넣을 프롬프트

```text
[대피 세션 시작 — 2026-11-25 · 서브]

너는 Yonghoon-DEM-DFT 캠페인의 임시 대피 세션이다. 본 세션(브랜치 claude/friendly-meitner-lldvar)이 토큰을 다 써서
이 서브 브랜치로 옮겨 왔다. friendly 세션이 하던 일을 그대로 이어 간다. 나중에 사용자가 "돌아가자" 하면
이 브랜치를 friendly 로 **충돌 없이** 되돌린다 — 그 조건이 아래 ■1 · ■5 · ■6 이다.

■ 1. 브랜치 (제일 먼저)
- 이 세션 브랜치 = 너의 시스템 지시에 적힌 개발 브랜치 (아래 <이 세션 브랜치>).
- git fetch origin claude/friendly-meitner-lldvar
- git log --oneline -4 origin/claude/friendly-meitner-lldvar → 맨 위가 "Evacuation handoff card 2026-11-25" 커밋이어야 한다
  (그 아래 22f6e466 "W_ad shared report: back button works inside the webapp frame" · 67b7e513 "… section numbers … become links").
  카드 커밋 위에 커밋이 더 있으면 누가 올렸는지 (git log --format='%h %an %ad %s') 본다 — 사용자 로컬 웹앱 메모
  (`notes: 화면에서 쓴 메모·형광펜`) · 사용자 회수 커밋은 정상이다 (알리기만). 그 밖의 것이면 사용자에게 묻는다. 카드 커밋이 없으면 멈추고 말한다.
- 이 세션 브랜치가 friendly 끝을 포함하지 않고 아직 내 커밋도 없으면 friendly 끝에서 시작한다:
    git checkout -B <이 세션 브랜치> origin/claude/friendly-meitner-lldvar
  (첫 push 가 non-fast-forward 로 거절되면 그 원격 브랜치에 내 커밋이 없는지 확인한 뒤에만 --force-with-lease.) 이미 내 커밋이 있으면 멈추고 묻는다.
- 브랜치를 옮겼으면 CLAUDE.md 를 다시 읽는다.
- ⛔ friendly 에는 push 하지 않는다. CLAUDE.md 의 "friendly 에만 커밋/푸시" 는 이 세션에서 "friendly 에는 쓰지 않는다 · 커밋 · 푸시는 <이 세션 브랜치> 에만"
  으로 읽는다 (사용자 2026-11-25 대피 지시). friendly 반영은 ■6 대로만.
- ⛔ 원격 (kgy · gabia · V100) 붙여넣기 블록에서 git fetch · checkout 할 때도 <이 세션 브랜치> 를 쓴다 (friendly 로 push 하면 복귀가 꼬인다).
  gabia 11b 는 이미 고정된 판 (계획 4a33eb41 · 드라이버 c3e2d358) 으로 돈다 — 회수 · 판독은 런로그 11b_* 키의 블록 그대로.
- PR 만들지 않는다 · force-push 는 --force-with-lease 만 · 커밋 메시지에 모델 ID 를 넣지 않는다.

■ 2. 먼저 읽을 것 (큰 파일은 grep · 부분 읽기)
- kb/projects/handoff_2026_11_25_evacuation.md ← 이 인계 카드 (§1–§5 통째로)
- kb/open_items.md 머리 ('지금 상태 — 2026-11-25' 목록) · 🔔 줄 (grep -n "🔔 용훈 포메이션" kb/open_items.md)
- b2o3 B 자리 DFT: 카드 db/properties/b2o3_site_dft_estimand_2026_11_23.json 의 ⏩_개정_1_2026_11_25_결과_전 ·
  결정 D-2026-11-25-b2o3-site-dft-amend1 (active) · 런로그 db/properties/b2o3_site_dft_runlog_2026_11_23.json 의
  kgy_블록_5_점검_결과 · kgy_블록_5c_큐_세우기 · kgy_블록_5c_결과 키 (모두 2026_11_25)
- b2o3 11b: 런로그 db/properties/b2o3_bo_placement_stage1_runlog_2026_11_09.json 의 11b_* 키 (발사 · 이어돌리기_규칙 · 감시_v2 · 판독_계약_결과_전)
- 값 · 판정은 원장이 이긴다: db/governance/decisions.json · db/properties/canonical_registry.json · db/properties/citation_hazards.json

■ 3. 시작 점검 (대피 직전 friendly 실측 기대값을 옆에 적었다)
  python3 tools/kb_wiki.py lint | tail -1                 # RESULT: 0 errors
  python3 tools/db/validate_canonical.py | tail -3        # 거버넌스 결정 205 · 판정 8 · 그래프 무결성 ✅ · 배선 전부 일치
  python3 tools/convention_check.py | tail -1             # RESULT: 0 위반
  python3 tools/litdb/build_index.py --check > /tmp/bi.log; echo $?    # 0 (DFT 280/280 · 어느 인덱스에도 없는 digest 0)
  python3 -m pytest -q webapp/tests/test_collab_reports.py | tail -1   # 17 passed

■ 4. 지금 상태와 할 일 — 인계 카드 §1–§4. 요약:
- b2o3 B 자리 DFT (트랙 우리 DFT 기준선 · 1저자 = 사용자): kgy 단일점 큐는 11-25 에 세웠다 — BMLi_00 이 반복 2 에서 GPU 메모리 부족
  (addusdens_g 8.99 GB 할당) · 첫 SCF 오차가 57 Å 막대 셀 세 구조에서 2–5 만 Ry. 개정 1 (local-TF β 0.2 · V100 32 GB · 12 점 전부 새 폴더 sp_dft_v2) active.
  🔔 실행은 11-28/29 예약 (사용자) — 그 전에 할 것 = 카드 §1 순서 (도구 → V100 준비 → 발사). 수렴 에너지는 판독 도구로만 읽는다 (결과 전 규칙).
- b2o3 11b (gabia · UMA MD · tmux b2o3_s11b · B₂O₃ 원고 계산 쪽 — 원고 1저자는 사용자 아님 · 계산 결정 = 사용자): 11-25 13:19 cfg0040 두 줄 T800 220/405 ps · 줄마다 41.2 ps/h
  → 어림 끝 11-29 10시 (마지막 단위가 150 h 상한 전에 시작). 끝나면 회수 → 판독 (11b_판독_계약_결과_전 그대로).
  그동안 gabia GPU pw.x 못 씀 (UMA 공존 금지) — 11b 뒤 9 단계 2 번 후보 이완 셋 (개정 6) → 12a/12b 띠틈.
- W_ad a5: Codex ET GO · 배포 zip 준비 끝 → 🔔 사용자 결정 = 업체 발송 (메일 본문에 MANIFEST sha) · DEM 편지 10 은 반송 뒤.
- litdb: 11-25 (3 편) · 11-25b (Shen Li–S 1 편) 끝. 다음 후보 (7 + 23 + 8 편) 는 🔔 사용자 결정 대기.
- W_ad 공유 보고서: 11-25 에 7 절 세 양 표 · 절 번호 링크 91 · ↩ 돌아가기 (웹앱 iframe 대응) — 공유 HTML 을 고치면 웹앱 COLLAB_REPORTS note 도 같이 (CLAUDE.md).
- 원격: gabia = 11b MD · kgy = 우리 잡 없음 (남의 python3 7.7 GB) · V100 = 11-28/29 예약 · 새 계산 승인은 개정 1 의 단일점 12 (+ 단계 2) 뿐.

■ 5. 머지 충돌을 안 만드는 규칙 (friendly 에는 사용자 로컬 웹앱만 쓸 수 있다 — 그 파일은 건드리지 않는다)
- ⛔ 손대지 않는다: db/file_comments.json · db/file_highlights.json · db/note_images/ (사용자 로컬 웹앱이 friendly 에 쓴다).
- 생성 파일은 손으로 고치지 않는다 — kb/index.md (python3 tools/kb_wiki.py index) · kb/reviews/INDEX.md (python3 tools/kb_wiki.py reviews --write).
- litdb: litdb/INDEX.md · litdb/comparison_vs_ours.md · litdb/figures/_sources.json · litdb/pdf_map.tsv · litdb/_curation/wishlist.md 는 **행을 덧붙이기만** 한다
  (논문 에이전트는 digest · 그림 · report 만 쓰고 공유 파일은 이 세션이 합친다 — 선례 batch_2026_11_25b).
- kb/open_items.md: ⏭ 머리는 '지금 상태' 목록 꼴이다 — 목록 줄을 고치고, 밀려난 상태는 접힌 '지난 갱신 기록' 맨 위에 한 항목으로 옮긴다.
  그 밖의 절은 옛 문장을 지우거나 고쳐 쓰지 않고 '⏩ **날짜**: …' 로 덧붙인다. 🔔 줄은 처리되면 ✅ 로 바꾼다 (지우지 않는다).
- db/governance/decisions.json: 내가 다루는 결정만 고친다 · ratification 이 있는 결정은 내용을 바꾸지 않는다 (decision_digest 가 깨진다) — 새 사실은 새 결정이나 runlog 에.
  새 결정의 digest 는 webapp/canonical.py::decision_digest 로 낸다 (접두 sha256: 포함 · tools/sdcp/prereg_ratify.py 의 것은 접두가 없다).
- runlog · 카드 JSON 은 새 키를 덧붙인다 · 파일마다 원래 indent (1) · ensure_ascii=False 를 지킨다.

■ 6. 복귀 (사용자가 "돌아가자" 할 때)
- 이 세션이 kb/projects/handoff_<날짜>_return_to_origin.md 를 쓴다 (선례 handoff_2026_11_23_return_to_origin.md) — §0 에 friendly 세션용 프롬프트.
- 먼저 가상 머지로 충돌을 잰다 (아무것도 안 바꾼다):
    git fetch origin claude/friendly-meitner-lldvar <이 세션 브랜치>
    git merge-tree --write-tree origin/claude/friendly-meitner-lldvar origin/<이 세션 브랜치> | tail -5   # 충돌 줄이 없어야 한다
- friendly 가 이 카드 커밋에서 안 움직였으면: friendly 쪽에서 git merge --ff-only origin/<이 세션 브랜치> 한 줄 (충돌 0).
- friendly 가 움직였으면 (메모 커밋): 이 세션 브랜치에서 먼저 git merge --no-ff origin/claude/friendly-meitner-lldvar →
  충돌은 생성 파일이면 도구로 다시 만들고 · litdb 표 · open_items 는 양쪽 행을 다 남기고 → lint 0 · validate ✅ · 웹앱 시험 확인 → push →
  그 다음 friendly 쪽은 git merge --ff-only origin/<이 세션 브랜치> (friendly 에서 rebase · force 금지).
- 복귀 카드에 원격 상태 (11b · B 자리 DFT · 마지막 실측 시각) 와 이 세션에서 바뀐 원장 목록을 적는다.
- 로컬 웹앱 안내: 로컬 127.0.0.1:5001 은 로컬 체크아웃을 읽는다 — 대피 중 로컬을 대피 브랜치로 옮겼으면
  git switch claude/friendly-meitner-lldvar && git pull --ff-only · friendly 에 있었으면 git pull --ff-only.
```

## 1. b2o3 B 자리 DFT — 단일점 다시 (11-28/29 예약 · 트랙 우리 DFT 기준선 · 1저자 = 사용자)

**정한 것 (원장 · 다시 논증하지 않는다)**
- 카드 `db/properties/b2o3_site_dft_estimand_2026_11_23.json` (결정 `D-2026-11-23-b2o3-site-dft` active) · 개정 1 `⏩_개정_1_2026_11_25_결과_전` (결정 `D-2026-11-25-b2o3-site-dft-amend1` active · 사용자 11-25 AskUserQuestion — 믹싱 'local-TF · β 0.2' · 기계 'V100 32 GB').
- 바뀌는 것은 SCF 경로 (mixing) 와 기계뿐 — 보고량 · 판정 규칙 (|D| ≥ 0.10 eV/B · 단계 2 고르기 · 압력 어림 · k 탐침) · 다른 DFT 설정 (ecut 52/520 · gaussian 0.01 · nspin 1 · nosym · conv_thr 1e-8 · electron_maxstep 200 · david · PP 6 · k 3 3 1 · UMA 셀 그대로) 은 그대로.
- 사용자 11-25: *"이건 나중에 11-28, 29쯤에 하자 · 용훈 포메이션에 예약으로 적어놔줘"* → 🔔 줄 (`kb/open_items.md` '지금 상태').

**왜 (사실 · 결과 아님 — SCF 진단 줄만 봤다)**
- 57 Å 막대 셀 (면 간격 5.7 · 5.7 · 57.3 Å · 10 월 UMA 셀) 세 구조의 첫 SCF 오차: BMLi_00 51,762.63 · BMLi_01_OB 39,027.28 · BMP_04 (블록 4 프로브) 21,339.76 Ry ↔ 9 단계 (29.1 Å · plain 0.3 · 수렴) 106.5 Ry · BMLi_00 반복 2 Davidson 평균 74.6 회.
- 메모리: BMLi_00 반복 2 에서 `addusdens_g` (PW/src/addusdens.f90:130) 가 장치 메모리 8,992,747,728 바이트 할당 실패 (P PP β 18 개 → 짝 171 × G ≈ 3.3 M) · 그때 전체/빈 CUDA 25.32/9.22 GB · 우리 바탕 ≈ 12.5 GB → 혼자여도 ≈ 21.5–22 GB · kgy 남의 몫 7.7 GB 면 안 들어간다.
- kgy 에 남은 것: `~/work/runs/b2o3_site_dft_2026_11_23/sp_dft/` (옛 폴더 · 그대로 둔다) · 보관본 `BMLi_01_OB_scf_stop_1125.out` · 큐 tmux `bsite_sp` 닫힘 · 비용 ≈ 2 GPU-h (상한 150 에 센다).

**할 일 (11-28/29 · 순서)**
1. **도구 (결과 전 · 커밋 먼저)** — `tools/doping/b2o3_site_dft.py`:
   - `sp_inputs` 에 믹싱 덮어쓰기 인자 (예 `--mixing local-TF:0.2`) → 판 고정 `b2o3_bo_dft.py` 의 `mixing_mode` · `mixing_beta` 줄만 바꾸고 (각 줄이 정확히 하나인지 확인 · `pw_text` 의 disk_io 바꾸기와 같은 꼴) · `sp_plan.json` 에 기록.
   - `read_sp` 가 같은 덮어쓰기로 입력을 다시 만들어 sha256 대조 (G2) — 계획에 덮어쓰기가 없거나 다르면 거부. 출력 판정 (`out_problems`) 의 믹싱 대조가 있으면 같이.
   - 단계 2 이완 입력도 같은 믹싱.
   - selftest 음성 경로: 덮어쓰기 없는 옛 계획을 새 판독이 받지 않는다 · 한 폴더에 믹싱이 섞이면 거부 · 덮어쓰기 값 오타 거부. 고친 함수에 닿는 변이만 (CLAUDE.md 전수 변이 규칙 — P0/P1 이면 전수).
   - 실행기 `tools/doping/run_force_check_scf.sh` 의 설정 균일성 검사 (`_UNIFORM_KEYS`) 는 새 폴더 안에서 그대로 통과해야 한다 (12 점 전부 같은 믹싱).
2. **V100 준비 (검사 · run 아님)**: 비었나 (nvidia-smi) · `ldd <pw.x>` 로 런타임 (CLAUDE.md kgy 절의 ldd 순서 · V100 은 hpcx OpenMPI · NVHPC 24.11 · cc70) · PP 6 개 MD5 (런로그 `kgy_블록_1_2026_11_23` 블록 ③ 의 md5 여섯 줄 — gabia `/data/work/pseudo` 에서 scp · V100 접속은 `ssh v100`) · worktree (`<이 세션 브랜치>`) · 메모리 프로브 (GPU · 300 초 · `< /dev/null` · `timeout -k` — 블록 4 v4 꼴) 로 피크가 32 GB 안인지.
3. **발사**: `sp_inputs --mixing …` → 새 폴더 `sp_dft_v2` → DRY_RUN → tmux · 감시는 자세한 watch (런로그 `kgy_블록_5b_BMLi_00_세우기_2026_11_25.감시` 를 V100 경로로) — 첫 점 첫 오차가 수십 Ry 대인지 · 반복이 줄어드는지 · '마지막 쓰기' 20 분 넘게 멈추면 이번과 같은 꼴.
4. 12 점이 다 끝나면 `read_sp` (블록 6 꼴 · 새 폴더 · 새 인자) → 단계 2.

## 2. b2o3 11b — gabia UMA MD 진행 중 (B₂O₃ 원고 계산 쪽 · 결정 = 사용자)

- 실행: gabia tmux `b2o3_s11b` · `/data/work/runs/b2o3_bo_2026_11_09/s11b_md` · 계획 4a33eb41 · 드라이버 c3e2d358 · 단위 8 (cfg0040 · cfg0015 · cfg0019 + 1×2×5 대조 × 시드 2) · 두 줄 · 단위마다 300 → 600 → 800 → 1000 K 각 405 ps.
- 11-25 13:19 실측: 대조 둘 끝 (ctrl_s1 26.34 h) · cfg0040 s1 219.63 / s2 220.05 ps (T800) · 줄마다 41.2 ps/h → 어림 끝 cfg0040 11-26 04시 · cfg0015 11-27 19시 · cfg0019 11-29 10시 · 범위 11-28 04시 (61 ps/h) ~ 11-30 24시 (29 ps/h) · 150 h 상한 (11-29 16:01) 전에 마지막 단위가 시작하므로 이어 띄우기는 필요 없을 듯 (서면 런로그 `11b_이어돌리기_규칙_2026_11_23`).
- 감시 = 런로그 `11b_감시_v2_2026_11_23` · 끝나면 회수 → 판독 계약 `11b_판독_계약_결과_전_2026_11_23` 그대로 (결과 전에 정한 것 · 다시 해석하지 않는다).
- 그 뒤 gabia 줄: 9 단계 2 번 후보 이완 셋 (개정 6 active) → 12a/12b 띠틈.

## 3. W_ad — a5 발송 대기 · 공유 보고서 (트랙 W_ad · 1저자 = 사용자)

- a5: Codex ET GO (11-24 · `kb/reviews/codex_ET_reply_wad_a5_es_fixes_2026_11_24.md`) · 배포 zip `wad_a5_vasp_2026_11_20_990f8f84.zip` (sha256 dc1fbcad… · MANIFEST 01e39753…) · 인계 `db/properties/wad_a5_vasp_handoff_2026_11_24.json` → 🔔 사용자 결정 = 업체 발송 → 반송 오면 인계 '보낼_때' ⑤ · DEM 편지 10 은 그 뒤 (🔔 W_ad · DEM 다음 편지 줄).
- 공유 보고서 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` (웹앱 `/reports/wad-dem`): 11-25 에
  ① 7 절 세 양 비교 표 (Li 원자 흡착 에너지 · W · γ_Li · 사용자 9 9 9 9) `127fc757`
  ② 본문 절 번호 링크 91 · 도착 제목 강조 · ↩ 돌아가기 `67b7e513`
  ③ 웹앱 iframe 대응 (웹앱은 iframe 을 보고서 길이만큼 늘리고 바깥 창이 스크롤한다 → 바깥 창 스크롤로 재고 되돌림 · 단추는 보이는 칸 오른쪽 아래 · 제목은 메모 줄 아래 56 px) `22f6e466`.
  사용자 지시: 보고서는 사용자가 *'이 부분 추가해줘'* 할 때만 고친다 (11-25).

## 4. litdb · 웹앱 · 그 밖

- litdb 11-25 (Kotakadi · Sandoval · Park) · 11-25b (Shen *ACS Nano* 2026 · CPME/THF Li–S · `b86dff00`) 끝. 다음 후보: 🔔 litdb 줄 (7 편 미룸 · 11-25 묶음 23 편 · 11-25b 8 편 — `litdb/_curation/batch_2026_11_25b/extra_papers_2026_11_25b.md`).
- Sakamoto 칩 (11-25): Shen digest 머리의 '저자 아님' 줄을 지웠다 (`716e5793`). 우리 웹앱 코드는 이미 그런 줄을 거른다 — 사용자 화면 ('문헌 지도 · 분류 대기 · digest 등록' 글자) 은 이 저장소 웹앱 코드에 없는 판이다. 같은 꼴의 줄이 남은 digest 넷 (baer2026 · cicvaric2026 · park2025 · yang2021) — 사용자가 그 화면에서 칩을 보면 같이 지운다.
- 논문 에이전트에게 줄 규칙 (다음부터): 'Jeff Sakamoto 저자 여부' 는 report (g) 에만 쓰고 digest 머리에 '저자 아님' 줄을 쓰지 않는다.
- '분류 대기' 는 최근 digest 가 다 그렇다 (litdb/topics.json 에 아직 안 넣음) — 사용자가 묻기 전에는 손대지 않는다.

## 5. 이 세션이 대피 직전에 한 것 (11-25)

- b2o3 B 자리 DFT: kgy 블록 5 점검 → BMLi_00 정체 · OOM 진단 → 큐 세움 (블록 5c) → 개정 1 · 결정 (사용자 선택) · 🔔 11-28/29 예약 (`9b021a7c` · `90d1ec08` · `bd41ae24`).
- b2o3 11b 끝 시각 다시 잼 (`b87bcaf9`).
- litdb 11-25b Shen (에이전트 · 컨테이너 재시작으로 한 번 다시 띄움 · 합침 `b86dff00`) · Sakamoto 칩 줄 지움 (`716e5793`).
- W_ad 공유 보고서 셋 (`127fc757` · `67b7e513` · `22f6e466`).
- 설명 (기록만 · 원장 변경 없음): W → 젖음각 (Young–Dupré) · Li 원자 흡착 에너지 대 γ_Li · Li₂S / Li₃Nd NEB 끝점 · 이미지 선정 (sei_neb.json · pick_hop · 10-26 끝점 재배열 기록).

## 6. 복귀 체크리스트 (복귀 카드에 옮길 것)

- [ ] friendly 가 이 카드 커밋에서 움직였는가 (`git log origin/claude/friendly-meitner-lldvar`) → 안 움직였으면 ff-only · 움직였으면 대피 브랜치에서 먼저 --no-ff 머지
- [ ] 가상 머지 `git merge-tree --write-tree` 에 충돌 줄 0
- [ ] 생성 파일 다시 만들기 (kb_wiki index · reviews --write) · lint 0 errors · validate_canonical ✅ · convention_check 0 · build_index --check 0 · 공유 보고서 시험
- [ ] 원격 마지막 실측 (gabia 11b · V100 B 자리 DFT · 시각) · 이 세션에서 바뀐 원장 목록 (카드 · runlog · decisions · open_items · litdb · 공유 보고서)
- [ ] CLAUDE.md 를 고쳤으면 그 줄을 복귀 카드에 적는다
- [ ] 로컬 웹앱 안내 (■6 마지막 줄)
