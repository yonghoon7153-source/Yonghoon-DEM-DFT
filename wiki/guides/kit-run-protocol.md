---
title: 킷 실행 프로토콜 — V100 부트스트랩 → run_mpm → 완료판정 → A/B
created: 2026-08-11
updated: 2026-08-11
type: guide
tags: [environment, mpm, pipeline]
sources: [scripts/setup_v100.sh, scripts/trace_deps.py, scripts/patch_kit_quasistatic.py, scripts/sr01_stamp_ab.sh, docs/server_bootstrap_runbook.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: prescriptive
evidenceScope: multi-source-primary
anchored: n-a
scope: n-a
---

# 킷 실행 프로토콜

## 목적
새 GPU 박스에서 킷([[mpm-kit-pipeline]])을 **드립 없이** 돌린다.  2026-08-11 실측
드립 3연속(pandas→networkx→skimage)의 재발 방지 절차.

## 절차
1. **환경**: `bash scripts/setup_v100.sh` — pip 목록은 `trace_deps.py` 가 코드에서
   유도한 것과 `--check` 로 대조된다 (drift 가드).  ⚠ 설치는 반드시 **그 venv 의
   python** 으로 (`venv/bin/python3 -m pip install …` — venv 는 ~/.local 을 안 본다).
2. **브랜치**: GPU 박스 레포가 다른 브랜치에 있으면 pull 하지 말고 **worktree**:
   `git worktree add --detach ~/dem-sk origin/<branch>` + 킷 폴더에
   `ln -sfn ~/dem-sk/scripts <데이터루트>/scripts` (run_mpm 은 `$KIT/../scripts` 를 본다).
3. **게이트 소급 배선**: `python3 scripts/patch_kit_quasistatic.py <킷들 폴더>` (멱등)
   — 없으면 준정적 게이트가 킷을 거부한다 ([[quasistatic-platen-gate]]).
   절대값 트랙이 필요하면 `MPM_QUASISTATIC=1` (런타임 ~10×, 기존 코퍼스와 비교 금지).
4. **실행**: `bash <kit>/run_mpm.sh` — self-detach 라 SSH 끊겨도 산다.
   watch: `tail -f <kit>/run_VGCF*_*/mpm_run.log`.
   완료판정: `test -f <kit>/latest_run/mpm_done.marker`.  ⚠ payload 실패 시
   latest_run 심링크가 **안 생긴다** — run 폴더를 직접 지정해 이어간다.
5. **첫 화면 확인**: `[platen] … V/c_P=… 승인됨` 줄 + `[run_mpm] 준정적:` 배너.
   metrics JSON 의 `quasistatic_violation` 이 결과 라벨을 정한다.
6. **SR-01 A/B** (해당 시): `bash scripts/sr01_stamp_ab.sh <kit> [run_dir]` —
   두 팔(점/선분)을 직접 돌리고 production 산출물은 건드리지 않는다.
   ⚠ run_mpm.sh 안내의 sed 한 줄은 틀렸다 (범위 재개방으로 파일 끝까지 뱉음) —
   반드시 러너를 쓸 것.  배경은 [[sr01-stamp-fragmentation]].

## 함정 목록 (전부 실측)
- `run_mpm.sh` 의 자동 git pull 은 **배치 중간에 코드가 바뀌는** 사고를 낸다 —
  worktree(.git 파일) 에선 자동 스킵.  배치 러너는 첫 줄에 HEAD·md5 를 박는다.
- 킷 스캐폴드 5종의 러너는 **킷별로 다르다** (해시 전부 다름) — 한 벌 재사용 금지.
