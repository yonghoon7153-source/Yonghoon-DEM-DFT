---
title: "대피 인계 — 2026-11-20 (friendly 세션 사용 한도 → 서브 세션 · 머지 때 충돌 0 · W_ad 은 a5 고침 이어하기 · [혁주] MD-1 판독)"
date: 2026-11-20
updated: 2026-11-20
tags: [handoff, session, evacuation, branch, merge, wad, vasp, a5, review, hyeokju, md1]
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

# 대피 인계 — 2026-11-20

> 본 세션 (`claude/friendly-meitner-lldvar` · session …CTzs) 이 주간 사용 한도에 걸려서 (갈래 에이전트가 11-20 밤 'weekly limit · resets Nov 23 16:00 UTC' 로 멈췄다),
> 다음은 **서브 대시보드의 서브 브랜치**에서 이어 간다 (사용자 2026-11-20 *"토큰 없어서 예전처럼 서브 대시보드/브랜치에 가려하는데 저번에 했던 것처럼 머지할떄 충돌안되게 프롬프트 부탁해요"*).
> 선례: `handoff_2026_11_12_evacuation.md` (대피) → `handoff_2026_11_17_return_to_origin.md` (복귀 · 충돌 0).
>
> **충돌 0 의 조건은 하나다 — 대피하는 동안 friendly 에 아무도 쓰지 않는다.** 이 카드를 담은 커밋 ("Evacuation handoff card 2026-11-20") 이 friendly 세션의 마지막 커밋이다.
> 원격 (kgy · gabia) 회수 블록도 friendly 로 push 하지 않는다. 그러면 복귀는 `git merge --ff-only` 한 줄이다 (litdb 정리 · 사용자 메모 커밋이 끼면 ■6 의 --no-ff 경로).
>
> ⚠ 원격 상태 마지막 실측 = **2026-11-20 20:55 KST** (kgy MD-1 watch · 사용자 붙여넣기). 그 뒤는 사용자가 붙여 주는 출력으로만 쓴다.

## 0. 새 세션 (서브) 에 붙여 넣을 프롬프트

```text
[대피 세션 시작 — 2026-11-20 · 서브]

너는 Yonghoon-DEM-DFT 캠페인의 임시 대피 세션이다. 본 세션(브랜치 claude/friendly-meitner-lldvar)이 사용 한도에 걸려서
이 서브 브랜치로 옮겨 왔다. friendly 세션이 하던 일을 그대로 이어 간다. 나중에 사용자가 "돌아가자" 하면
이 브랜치를 friendly 로 **충돌 없이** 되돌린다 — 그 조건이 아래 ■1 · ■5 · ■6 이다.

■ 1. 브랜치 (제일 먼저)
- 이 세션 브랜치 = 너의 시스템 지시에 적힌 개발 브랜치 (아래 <이 세션 브랜치>).
- git fetch origin claude/friendly-meitner-lldvar
- git log --oneline -6 origin/claude/friendly-meitner-lldvar → 맨 위가 "Evacuation handoff card 2026-11-20" 커밋이어야 한다
  (그 아래 93abf3eb "W_ad a5 해석 1 비준 …" · e374d7fd "W_ad a5: 내부 독립 리뷰 EM (NO-GO) 보관 …").
  카드 커밋 위에 커밋이 더 있으면 누가 올렸는지 (git log --format='%h %an %ad %s') 본다 — litdb 정리 세션 · 사용자 로컬 웹앱 메모
  (`notes: 화면에서 쓴 메모·형광펜`) · 사용자 회수 커밋은 정상이다 (알리기만). 그 밖의 것이면 사용자에게 묻는다. 카드 커밋이 없으면 멈추고 말한다.
- 이 세션 브랜치가 friendly 끝을 포함하지 않고 아직 내 커밋도 없으면 friendly 끝에서 시작한다:
    git checkout -B <이 세션 브랜치> origin/claude/friendly-meitner-lldvar
  (첫 push 가 non-fast-forward 로 거절되면 그 원격 브랜치에 내 커밋이 없는지 확인한 뒤에만 --force-with-lease.) 이미 내 커밋이 있으면 멈추고 묻는다.
- 브랜치를 옮겼으면 CLAUDE.md 를 다시 읽는다.
- ⛔ friendly 에는 push 하지 않는다. CLAUDE.md 의 "friendly 에만 커밋/푸시" 는 이 세션에서 "friendly 에는 쓰지 않는다 · 커밋 · 푸시는 <이 세션 브랜치> 에만"
  으로 읽는다 (사용자 2026-11-20 대피 지시). friendly 반영은 ■6 대로만.
- ⛔ 원격 (kgy · gabia) 붙여넣기 블록에서 git fetch · push 할 때도 <이 세션 브랜치> 를 쓴다 (friendly 로 push 하면 복귀가 꼬인다).
  kgy MD-1 의 worktree (/home/kgy/wt_hj_md1) 는 이미 고정돼 있다 — 판독은 그 worktree 를 그대로 쓴다 (인계 카드 §2).
- PR 만들지 않는다 · force-push 는 --force-with-lease 만 · 커밋 메시지에 모델 ID 를 넣지 않는다.

■ 2. 먼저 읽을 것 (큰 파일은 grep · 부분 읽기)
- kb/projects/handoff_2026_11_20_evacuation.md ← 이 인계 카드 (§1–§4 통째로)
- kb/open_items.md 머리 ('지금 상태 — 2026-11-20' 목록)
- W_ad a5: 개정 db/properties/wad_aprime_pilot_prereg_v5_amendment_5_e70_retry_2026_11_20.json (v2 · 비준) ·
  결정 D-2026-11-20-wad-aprime-v5-e70-a5-retry · D-2026-11-20-wad-aprime-v5-e70-a5-interp1 (둘 다 active) ·
  리뷰 kb/reviews/internal_EM_reply_wad_a5_package_2026_11_20.md (NO-GO · 끝의 '주 세션 처리') · 빌드 기록 db/properties/wad_a5_build_log_2026_11_20.json
- [혁주] MD-1: runlog db/properties/hyeokju_lzo_md1_runlog_2026_11_20.json · 카드 db/properties/hyeokju_lzo_md_card_2026_11_16.json 의 ⏩_개정_2_2026_11_20_MD1_결과_전 (기계_판독_값 포함)
- 값 · 판정은 원장이 이긴다: db/governance/decisions.json · db/properties/canonical_registry.json · db/properties/citation_hazards.json

■ 3. 시작 점검 (대피 직전 friendly 실측 기대값을 옆에 적었다)
  python3 tools/kb_wiki.py lint | tail -1                 # RESULT: 0 errors
  python3 tools/db/validate_canonical.py | tail -3        # 거버넌스 결정 200 · 판정 8 · 그래프 무결성 ✅ · 배선 전부 일치
  python3 tools/convention_check.py | tail -1             # RESULT: 0 위반
  sha256sum kb/projects/handoff_2026_11_20_a5_fix_wip.patch | cut -c1-16   # f31eb96ee271b6f3
  git apply --check kb/projects/handoff_2026_11_20_a5_fix_wip.patch && echo ok   # ok (friendly 끝 위에 깨끗이 얹힌다)

■ 4. 지금 상태와 할 일 — 인계 카드 §1–§3. 요약:
- W_ad 은 a5 (트랙 W_ad · 1저자 = 사용자): 묶음은 아직 안 보냈다. 내부 독립 리뷰 EM = NO-GO (P0 2 · P1 4).
  고침은 갈래 에이전트가 하던 중 한도로 멈췄다 — 미완 · 시험 미확인 고침이 kb/projects/handoff_2026_11_20_a5_fix_wip.patch (도구 두 파일 · 기준 2cecb0fb).
  할 일 = 카드 §1 순서 (패치 얹기 → 시험 · 돌연변이 · 재현 · 리뷰어 재현 스크립트 → 남은 고침 → 묶음 다시 빌드 → Codex 리뷰 (사용자 '받자' 11-20) → GO → zip · 운영 안내 · handoff).
  DEM 편지 10 은 a5 가 끝난 뒤 보낸다 (사용자 11-20).
- [혁주] MD-1 (트랙 [혁주] · 1저자 = 혁주 · 계산 쪽 결정 = 사용자): kgy tmux hjmd1 · 세 시드 600 K 1 ns · 11-20 20:55 에 생산 약 126/1000 ps · 끝 어림 11-22 오후.
  끝나면 카드 §2 의 판독 블록 (시드마다 --md1 → --md1_ensemble) · 결과 전 규칙 그대로 (P–O < 1.8 · Zr–S < 2.9 Å · 1 ps 지속 · 시드 2/3).
- 그 밖: b2o3 다음 단계 (11a 포논 · 11b 열 안정성 · 12 띠틈) 는 사용자 '발사' 대기 · gabia 정리 (hj_md0k tmp · wt_hj_md0k) · 카드 §3.
- 원격: kgy = MD-1 (GPU 약 8.4 GB) · gabia = 우리 잡 없음 (b2o3 9 단계 끝) · IBB DEM 잡은 사용자 쪽 · 새 계산 승인 없음.

■ 5. 머지 충돌을 안 만드는 규칙 (friendly 에 다른 둘이 쓸 수 있다 — 그 파일은 건드리지 않는다)
- ⛔ 손대지 않는다: db/file_comments.json · db/file_highlights.json · db/note_images/ (사용자 로컬 웹앱이 friendly 에 쓴다) ·
  litdb/_curation/ (litdb 정리 세션). litdb 에 새 digest 를 넣어야 하면 litdb/INDEX.md · litdb/comparison_vs_ours.md ·
  litdb/figures/_sources.json · litdb/pdf_map.tsv 는 **행을 덧붙이기만** 한다.
- 생성 파일은 손으로 고치지 않는다 — kb/index.md (python3 tools/kb_wiki.py index) · kb/reviews/INDEX.md (python3 tools/kb_wiki.py reviews --write) ·
  litdb build_index.py 산출물 (복귀 머지 뒤 도구로 다시 만든다).
- kb/open_items.md: ⏭ 머리는 '지금 상태' 목록 꼴이다 — 목록 줄을 고치고, 밀려난 상태는 접힌 '지난 갱신 기록' 맨 위에 한 항목으로 옮긴다.
  그 밖의 절은 옛 문장을 지우거나 고쳐 쓰지 않고 '⏩ **날짜**: …' 로 덧붙인다.
- db/governance/decisions.json: 내가 다루는 결정만 고친다 · ratification 이 있는 결정은 내용을 바꾸지 않는다 (decision_digest 가 깨진다) — 새 사실은 새 결정이나 runlog 에.
- runlog · 카드 JSON 은 새 키를 끝에 덧붙인다 · 파일마다 원래 indent (1 또는 2) · ensure_ascii=False 를 지킨다.
- a5 도구 두 파일 (tools/wad/build_a5_vasp_package.py · build_v5_vasp_package.py) 과 db/inputs/wad_a5_vasp_2026_11_20/ 은 이 세션만 고친다 (friendly 는 안 건드린다).

■ 6. 복귀 (사용자가 "돌아가자" 할 때)
- 이 세션이 kb/projects/handoff_<날짜>_return_to_origin.md 를 쓴다 (선례 handoff_2026_11_17_return_to_origin.md) — §0 에 friendly 세션용 프롬프트.
- 먼저 가상 머지로 충돌을 잰다 (아무것도 안 바꾼다):
    git fetch origin claude/friendly-meitner-lldvar <이 세션 브랜치>
    git merge-tree --write-tree origin/claude/friendly-meitner-lldvar origin/<이 세션 브랜치> | tail -5   # 충돌 줄이 없어야 한다
- friendly 가 이 카드 커밋에서 안 움직였으면: friendly 쪽에서 git merge --ff-only origin/<이 세션 브랜치> 한 줄 (충돌 0).
- friendly 가 움직였으면 (litdb 정리 · 메모 커밋): 이 세션 브랜치에서 먼저 git merge --no-ff origin/claude/friendly-meitner-lldvar →
  충돌은 생성 파일이면 도구로 다시 만들고 · litdb 표 · open_items 는 양쪽 행을 다 남기고 → lint 0 · validate ✅ · 웹앱 시험 확인 → push →
  그 다음 friendly 쪽은 git merge --ff-only origin/<이 세션 브랜치> (friendly 에서 rebase · force 금지).
- 복귀 카드에 원격 상태 (MD-1 · a5 발송 여부 · 마지막 실측 시각) 와 이 세션에서 바뀐 원장 목록을 적는다.
- 로컬 웹앱 안내: 로컬 127.0.0.1:5001 은 로컬 체크아웃을 읽는다 — 대피 중 로컬을 대피 브랜치로 옮겼으면
  git switch claude/friendly-meitner-lldvar && git pull --ff-only · friendly 에 있었으면 git pull --ff-only.
```

## 1. W_ad 은 e70 far 재시도 a5 — 고침 이어하기 (트랙 W_ad · 1저자 = 사용자)

**정한 것 (원장 · 다시 논증하지 않는다)**
- 개정 5 v2 비준 (11-20 · `D-2026-11-20-wad-aprime-v5-e70-a5-retry` active): A5 (LDIPOL 끄고 먼저 수렴 · 보존 ⓐ 가 확인되면 이어서 · 아니면 새로) → c1 (Davidson · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 400) → c2 (ALGO All · TIME 0.1 · NELM 400) · 채택 c1 주 → c2 주 → c1 보조 → c2 보조 · 보조 = u_W ≤ 0.002 J/m² 이고 G4 판정에 u_W 를 더함 · 상한 180 h · a5 가 마지막 · 라벨 'G5 원시 결과를 본 뒤 정한 재시도 (개정 5 · 1저자 결정)'.
- 해석 1 (11-20 · `D-2026-11-20-wad-aprime-v5-e70-a5-interp1` active · 사용자 '멈추고 1저자에게'): 다음 단은 앞 단이 확인된 미수렴 · 실행 실패 (전자 스텝 ≥ 1 · 끊김 기록 포함) 로 끝났을 때만 · 스텝 0 은 멈추고 0 스텝 기록 뒤 같은 단 · 재시작 미이행 · 미확인 · 설정 위반은 멈추고 1저자.
- 주 세션 구현 해석 (보수 · 사용자에게 알림 · 이의 없음): c1 보조 채택은 c2 가 확인된 결과 (확인된 미수렴 · 실행 실패/끊김 ≥ 1 행) 로 끝났을 때만 — c2 가 없거나 미확인 · 재시작 미이행 · 설정 위반이면 자동 채택 없음 → 1저자.
- 사용자: Codex 리뷰도 받는다 (11-20 *"codex 리뷰도 받을까"* → 권고 '받자') · DEM 편지 10 은 a5 끝내고 보낸다.
- 사실: W0 (보존 ⓐ WAVECAR) 는 지워졌을 가능성이 높다 — 외주 2차 러너 drop_wav 는 FINAL SCF_NOT_CONVERGED 에서 `rm -f` · 반송 env.txt 에 '남긴다' 줄 없음 (RETURN_NOTES 'stage-ⓐ WAVECAR 포함' 과 어긋남). 개정 5 는 이 경우를 정해 뒀다 (A5 새로).

**지금 있는 것**
- 도구 (friendly · 검토 · 받아들임): `tools/wad/build_a5_vasp_package.py` (sha 5c61c5f9…) · `tools/wad/build_v5_vasp_package.py` (daf9b990…) · 묶음 `db/inputs/wad_a5_vasp_2026_11_20/` (MANIFEST 026abb2d…) — **EM 리뷰 전 판이다. 이대로 보내지 않는다.**
- 미완 고침 패치: `kb/projects/handoff_2026_11_20_a5_fix_wip.patch` (sha256 f31eb96e… · 205 kB · build_a5 +1,550/−299 꼴 · V5 +82 꼴 · 기준 2cecb0fb · friendly 끝에 `git apply --check` 통과). 갈래 에이전트 마지막 말: 고침 뒤 돌연변이 전체를 돌리던 중 (12:49 UTC 시작 · 끝 못 봄) — **고침이 다 들어갔는지 · 시험이 초록인지 모른다.**
- 리뷰어 재현 스크립트: `kb/reviews/internal_EM_probes/` (12 개 · scratch 경로 · venv 경로가 박혀 있으니 고쳐 쓴다).
- 갈래 에이전트에게 보낸 고침 목록 = EM 회신의 P0-1 … P3 전부 + 해석 1 + 위 구현 해석 (자세한 줄은 EM 회신 원문).

**할 일 (순서)**
1. scratch worktree 에서 `git apply kb/projects/handoff_2026_11_20_a5_fix_wip.patch` (friendly 끝 기준).
2. dftd3 가 없으면 scratch 가상환경: `python3 -m venv <scratch>/venv && <scratch>/venv/bin/pip install simple-dftd3==1.6.0 numpy ase` (V5 selftest 가 쓴다 · 전역 설치 안 함).
3. 세 selftest (build_a5 · build_v5 · build_round2) · `build_a5 --mutants` · 11-20 G5 집계 재현 (`db/raw/wad_aprime_v5_vasp_2026_09_27/g5_collect_2026_11_20/COMMAND_AND_CHECKS.txt` 의 본 집계 명령 · V5 반송 tgz 를 scratch 에 풀어서 · sha afecfa08… 와 같아야 한다).
4. EM 재현 스크립트로 P0-1 · P0-2 (두 경로) · P1-1 · P1-2 · P1-3 · P2 (준비 실패 · 함께 푼 폴더) 를 고침 전 (friendly 도구) · 고침 후 (패치) 로 다 돌려 본다.
5. 남은 것 고치기 — EM 회신의 목록 전부 · 시험 음성 경로 · 돌연변이 표에 새 관문 · 각 돌연변이 빨간불.
6. 묶음 다시 빌드 (`build_a5 --build --out <scratch>` → 지금 폴더와 diff → 바꿔 넣기 · jobs.json 이 도구 sha 를 박는다) · 빌드 기록에 키 덧붙이기.
7. Codex 리뷰 편지 (다음 글자 EN · 영어 · 선례 codex_DE_prompt_wad_outsourcing_round2_v5_2026_10_22.md 꼴) → 사용자가 보낸다 → GO 까지.
8. zip (`git archive --format=zip --prefix=wad_a5_vasp_2026_11_20/ <커밋>:db/inputs/wad_a5_vasp_2026_11_20`) · handoff JSON (선례 `db/properties/wad_round2_vasp_handoff_v5_2026_10_22.json` 꼴) · 건엽 운영 안내 (한국어): 먼저 `ls -l` · `sha256sum` 로 W0 확인 (없으면 W0_WAVECAR=none) · 외주 2차 러너를 다시 돌리지 말 것 · 모든 단 같은 병렬 배치 (64 랭크 · KPAR 2 · NCORE 4 → NBANDS 872) · 단별 최악 벽시계 (A5 ≈ 33 h · c1 ≈ 44 h · c2 ≤ ≈ 88 h) · 빈 새 폴더 · 절대 경로 · 종료 코드 · 반송 파일.

## 2. [혁주] MD-1 — kgy 진행 중 (트랙 [혁주] · 1저자 = 혁주 · 계산 쪽 결정 = 사용자)

- 실행: kgy tmux `hjmd1` · 결과 폴더 `/home/kgy/work/runs/hj_md1_1120` (s1 · s2 · s3) · worktree `/home/kgy/wt_hj_md1` · 11-20 14:33 KST 시작 · 20:55 실측 생산 126/1000 ps (프레임 1263 · 100 fs 간격) · 끝 어림 11-22 오후 (어림).
- 감시: runlog `감시_블록` (watch -n 30 · 경고 줄 거르고 프레임 수 보는 판은 이 세션 11-20 대화에서 줬다).
- 끝 신호: `(tmux 끝)` + run.log 에 `s1 rc 0` · `s2 rc 0` · `s3 rc 0` · 시드마다 `md1s<k>_traj.xyz` (`.part` 가 아니다 — 끝날 때 이름을 바꾼다).
- 판독 (kgy · 결과 전 규칙 · 도구 `tools/oxidation/analyze_interface_decomp.py` sha 8d8049ef… · **블록을 주기 전에 `--help` 로 인자 이름을 확인한다**):
  시드마다 `--md1 <R>/s<k>/md1s<k>_traj.xyz --freeze <W>/db/structures/hyeokju_md1_2026_11_20/I142_liouter_aLZO16_md1s<k>_init_freeze.json --label md1s<k> --out_json … --out_csv …` →
  `--md1_ensemble J1 J2 J3 --out_json …` (관측창 줄은 tools/sei/collect_neb.py observation_window 를 쓴다) · 파이썬 = /home/kgy/apps/miniforge3/envs/uma/bin/python.
- 회수: kgy 블록의 push 는 <이 세션 브랜치> 로 · 인증 묻는 push 뒤에 다른 줄 두지 않기 (CLAUDE.md 소통 규칙).
- 판정 문장은 카드의 허용 · 금지 문장에서만 · 관측창 한 줄 같이 (CLAUDE.md 짧은 MD 규칙).

## 3. 그 밖

- b2o3 (1저자 = 사용자): 9 단계 판독 끝 (11-20 · EOS 건너뜀 규칙) · 다음 11a 포논 · 11b 열 안정성 · 12 띠틈/DOS 는 사용자 '발사' 대기 · relax_verdict · 이완 xyz 회수 push 블록은 아직 (gabia 에만 있다).
- gabia 정리 (사용자 블록): `/data/work/runs/hj_md0k_1120` 의 tmp/ (파동함수) · worktree `/data/work/wt_hj_md0k`.
- W_ad 외주 2차: 닫힘 (11-19 최종 반송 · G5_C PASS) · 은 V5 G5 는 11-20 집계 (INCOMPLETE · 오차표만) — a5 뒤 한 번 다시 집계.
- 원격 규칙은 CLAUDE.md 그대로 (QE run 은 GPU · gabia GPU pw.x ↔ UMA 동시 금지 · pkill -f pw.x 금지 · watch -n 30).
