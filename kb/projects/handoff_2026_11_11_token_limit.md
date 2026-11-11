---
title: "토큰 한도 인계 (2026-11-11 오후) — 같은 브랜치 friendly · 돌고 있는 것 둘 (gabia b2o3 8 단계 · kgy li2s-3 2 단계) · 다음 행동 · 사용자 결정 대기"
date: 2026-11-11
updated: 2026-11-11
tags: [handoff, gabia, kgy, b2o3, li2s, cascade, webapp]
status: 인계 — 다음 세션이 이 카드부터 읽는다
confidence: medium
verificationStatus: verified
verifiedAt: 2026-11-11
verifiedBy: self
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---


# 토큰 한도 인계 — 2026-11-11 오후 (브랜치 `claude/friendly-meitner-lldvar` · 끝 커밋은 이 카드를 넣은 커밋)

> 사용자 *"곧 토큰 끝나니까 대비해야될듯"*. 원장 · 카드 · 런로그가 정본이고 이 카드는 **어디를 보면 되는지** 만 모은다.
> 저장소는 **public** 이다 (11-11 사용자가 private 로 바꿨다가 되돌림 — private 이면 이 세션 git 이 403 · 아래 §5).

## 0. 다음 세션 첫 줄 (붙여 넣기용)

```
kb/projects/handoff_2026_11_11_token_limit.md 부터 읽고 이어서 해 줘. gabia b2o3 8 단계 · kgy li2s-3 2 단계가 돌고 있어.
```

## 1. 돌고 있는 것 둘

| 기계 | 무엇 | 위치 | 끝 어림 | 끝나면 |
|---|---|---|---|---|
| gabia | b2o3 1 단계 **8 단계** (54 구조 · UMA 어닐 100 ps → 이완) | tmux `b2o3_s8` · `R=/data/work/runs/b2o3_bo_2026_11_09` · 감시 `bash $HOME/w_b2o3_s8.sh \| sed …` (화면 '(20 ps 까지)' 는 옛 문구 · 실제 100 ps) | 11-11 14:26 기준 21/54 · **11-13 오전 10 시쯤** | gabia **블록 v3** — 런로그 `db/properties/b2o3_bo_placement_stage1_runlog_2026_11_09.json` 의 `8b_진단_블록_v3_2026_11_10` (② worktree 를 `7002085204183c88a0bec725e6d82f522eeeb1ef` 로 → ⓪ 검사 → ⓪b 궤적 에너지 → ① 본 판독 → ③ 추출 → ④ 이완 큐 → ④b rc → ⑤ 판정) · 카드 개정 4 active (`D-2026-11-10-b2o3-bo-placement-amend4-ea`) |
| kgy | li2s-3 **2 단계** (16 런 × 400 ps · v1 큐) | tmux `li2s3s2` · `B=~/work/runs/li2s3_stage2_2026_11_10` · 큐 worktree `~/wt_li2s3` (⛔ 올리지 않는다) | 11-11 18:53 기준 4/16 · 650 K 부터 공유 GPU 경합으로 ≈ 55 ps/h (런당 ≈ 7.4 h) · **11-15 아침** (경합이 풀리면 11-14) | 큐 끝 줄이 찍힌 뒤 **readout · pressure 한 번** (아래 §2) |

- ⛔ v1 큐 (`run_stage2_kgy.sh`) 는 멈추거나 끝나도 **다시 치지 않는다** (사다리 판독이 보류된다 · 카드 개정 3). 남은 런 · 재실행 · cond550 은 큐 v2 로만.
- kgy GPU 의 ≈ 4 GB 는 esp 계정 그래픽 앱이다 (우리 것 아님).

## 2. li2s-3 판독 (16 런 끝난 뒤 · kgy)

- 판독 허가는 걸려 있다: 카드 `lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json` 의 `판독_허가_2단계` — 대조 잡 출력 `/home/kgy/li2s3_control_job_v3.json` (sha256 `63fb4bb1…`) · ⚠ **이 파일을 지우거나 고치지 않는다**.
- 도구는 `~/wt_li2s3_q2` 에서 돈다 (깨끗한 트리 · 판독 도구 sha16 **`60a7ef3ce31d0bb2`** 이어야 허가가 선다 — 도구를 바꾸면 대조 잡을 다시).
  worktree 를 올릴 때는 `git -C ~/wt_li2s3_q2 fetch … && git -C ~/wt_li2s3_q2 checkout --detach FETCH_HEAD` (FETCH_HEAD 는 worktree 마다 따로).
- 명령 꼴 (uma python `/home/kgy/apps/miniforge3/envs/uma/bin/python`): `tools/ionic/li2s3_stage2_readout.py verify --base $B --worktree ~/wt_li2s3 --out …` → `readout --base $B --worktree ~/wt_li2s3` → `pressure --base $B --worktree ~/wt_li2s3 --device cuda` (GPU · 큐가 끝난 뒤).
  readout 은 **한 번** (출력이 있으면 덮지 않고 거부). 600 K 두 계가 측정 가능이면 cond550 자격 → `--phase cond550` 은 큐 v2 로 550 K 를 돈 **뒤** 한 번 더.
- 카드 §9 · 개정 DZ · EB · 3 (큐 v2) 문장이 판독 규칙이다. 트랙 = li2s (외부 1저자 · **위임 10-30**: 정하고 '사용자 (위임 10-30)' 로 적는다).

## 3. 오늘 (11-11) 끝낸 것

- **cascade 묶음 2 닫힘** — 판독 G2 멈춤 (Cl 을 F · Br 로 다 바꾼 TiF4 · ZrBr4 · ZrF4 의 원자 부피 판) → 개정 2 (비준 · 기록기 · 판독기 고침) → gabia 재실행 (회수 4259cb18 · 부피 거부 0) → 판독 (막는 게이트 전부 통과) → 마감 `db/properties/cascade_axes_bundle2_closed_2026_11_11.json` · `D-2026-11-11-cascade-axes-bundle2-closed` (사용자 비준). 선택 As2S3 · BaO · Na2O · SiO2 · SrCl2 · SrO · 핵 As2S3 · SiO2.
- **웹앱** — `/cascade#bundle2` '묶음 2 · 원소별 효과' 패널 (두 축 Pareto 그림 · 호스트 대비 표 · bf140bb9) · 여백 메모 **[접기 ▸ / ◂ 펴기]** 버튼 (cfdbe475 · 논문 페이지에서 머리줄이 목차 뒤로 숨던 것도 고침). 사용자 로컬은 `git pull --ff-only` → `python webapp/app.py` 재시작 → Ctrl+F5.
- **li2s-3** — 대조 잡 v3 same = True → 판독 허가 키 (028e0aa7).
- 논문 에이전트 #125–128 (Kamaya 2011 · Kato 2016 · Deiseroth 2008 · Janek & Zeier 2016) 은 11-10 에 끝났다.

## 4. 사용자 결정 대기

- **[cascade]** DFT 확인 카드 — 무엇을 (권고: '도핑이 격자에 들어가나' · 도핑 에너지) · 어느 후보 (권고: 선택 핵 As2S3 · SiO2 부터 · As 독성은 사용자 판단) · GPU 는 두 기계가 비는 11-14 뒤. 사용자가 `/cascade#bundle2` 를 보고 정한다고 했다.
- **[cascade]** 설계 전하 불균형 후속 · comp1 질서 배열 가설 (하려면 보고량 카드부터) — 급하지 않음.
- **[정리]** `/ro_st4.log` 지우기 (막힌 에이전트가 남긴 파일 · 사용자 몫).

## 5. 환경 주의

- Codex 토큰 없음 → 반박 리뷰는 에이전트로 (사용자 11-10 '반박 리뷰를 에이전트 사용해서').
- 저장소를 다시 **private** 로 하려면: ① Claude GitHub App 을 이 저장소에 설치 ② gabia · kgy 토큰에 비공개 권한 (classic `repo` · fine-grained Contents R/W) + `git config --global credential.helper 'cache --timeout=7200'` ③ Codex 쪽 GitHub 연결.
- 이 컨테이너에서 웹앱 브라우저 시험이 돈다 — `PW_CORE_FROM=/opt/node-tools/package.json node webapp/tests/docnote_paint.test.mjs` (pytest 감싸개도 찾아 쓴다) · Plotly 는 npm (`plotly.js-dist-min@2.35.2`) 에서 받아 `webapp/static/vendor/` 에 (gitignore).
- cascade v23 감사 원장 (`cascade_audit_manifest.json`) 은 이 컨테이너에서 다시 만들지 않는다 — 고정 커밋 원본 해시가 깨진다 (11-11 실측).
