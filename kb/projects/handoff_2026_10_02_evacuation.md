---
title: "대피 인계 — 2026-10-02 (friendly 세션 토큰 소진 → 서브 대시보드 세션 · 머지 때 충돌 0 설계)"
date: 2026-10-02
updated: 2026-10-02
tags: [handoff, session, evacuation, branch, merge, wad, p1b, kgy, li2s, elastic, cascade]
status: 진행
kind: project
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---

# 대피 인계 — 2026-10-02

> 본 세션(`claude/friendly-meitner-lldvar`)의 토큰이 다 떨어져서, 다음 세션은 **서브 대시보드의 서브 브랜치에서 잠깐** 이어 간다
> (사용자 2026-10-02: *"토큰을 다써서 다시 서브 대시보드로 가야되거덩. 저번에 했던것처럼 다시 머지됐을때 충돌되지 않도록 잘 프롬프트 짜서 넘기자"*).
> 선례: `handoff_2026_09_28_evacuation.md` (대피) → `handoff_2026_09_29_return_to_origin.md` (복귀 · fast-forward 49 커밋 · 충돌 0).
>
> **충돌 0 의 조건은 하나다 — 대피하는 동안 friendly 에 아무도 쓰지 않는다.** 이 카드를 담은 커밋이 friendly 의 마지막 커밋이다.
> 이 세션은 이 커밋 뒤로 friendly 에 쓰지 않는다. 대피 세션도 원격 블록도 friendly 로 push 하지 않는다.
> 그러면 복귀는 `git merge --ff-only` 한 줄이다.
>
> ⚠ **friendly 에 쓰는 세션이 하나 더 있다** — `session_01H191Ni4xzj9H5ftstAm7Ft` (litdb tortuosity 묶음 · 사용자 10-03 업로드 · DEM 쪽) 가
> 10-02 16:38 · 18:22 UTC 에 커밋 둘(4ba184975 · a626f72ef)을 friendly 에 올렸다 (이 카드는 그 위에 얹었다). 그 세션이 대피 중에도 friendly 에 쓰면
> 복귀는 fast-forward 가 아니라 `git merge --no-ff` (경우 C) 다. 그 세션은 **litdb/** (DEM 카드 · 그림 · INDEX_DEM · comparison_vs_ours_DEM · build_index 산출물)만
> 고치므로 겹칠 파일은 적다 — 대피 세션은 그 파일들을 건드리지 않는다 (■5).
>
> ⚠ **원격 상태는 10-02 22:05 KST 실측이 마지막**이다 (kgy 점검 블록 · DRY_RUN). 그 뒤 P1b **발사 블록을 줬고** 사용자가 watch 를 요청했다 —
> **발사 출력은 이 세션이 못 봤다.** 여기 적힌 "도는 중" 은 그때 기준이다. 다음 세션은 사용자가 붙여 주는 출력으로만 갱신한다.

## 0. 새 세션(서브 대시보드)에 붙여 넣을 프롬프트

```text
[대피 세션 시작 — 2026-10-02 · 서브 대시보드]

너는 Yonghoon-DEM-DFT 캠페인의 임시 대피 세션이다. 본 세션(브랜치 claude/friendly-meitner-lldvar)이 토큰을 다 써서
이 서브 브랜치로 잠깐 옮겨 왔다. friendly 세션이 하던 일을 그대로 이어 간다. 나중에 사용자가 "돌아가자" 하면
이 브랜치를 friendly 로 **충돌 없이** 되돌린다 — 그 조건이 아래 ■1·■5 다.

■ 1. 브랜치 (제일 먼저 · 이것부터 틀리면 다 틀린다)
- 이 세션 브랜치 = 너의 시스템 지시에 적힌 개발 브랜치 (아래 <이 세션 브랜치>).
- git fetch origin claude/friendly-meitner-lldvar
- git log --oneline -4 origin/claude/friendly-meitner-lldvar  → "대피 인계 카드 2026-10-02" 커밋이 보여야 한다
  (그 아래 a626f72ef · 4ba184975 = litdb 세션 커밋 · 그 아래 4d855c75c "점착 P1b 카드 비준"). 그 **위에** litdb 세션 커밋이 더 있어도 정상이다
  (session_01H191Ni4xzj9H5ftstAm7Ft 가 friendly 에 쓴다). 인계 카드 커밋이 아예 없으면 멈추고 사용자에게 말한다.
- 이 세션 브랜치가 friendly 끝을 포함하지 않고 (git merge-base --is-ancestor origin/claude/friendly-meitner-lldvar HEAD 실패)
  아직 내가 만든 커밋도 없으면, friendly 끝에서 다시 시작한다:
    git checkout -B <이 세션 브랜치> origin/claude/friendly-meitner-lldvar
  (첫 push 가 non-fast-forward 로 거절되면 그 원격 브랜치에 내 커밋이 없는지 확인한 뒤에만 --force-with-lease.)
  이미 내 커밋이 있으면 멈추고 사용자에게 묻는다.
- 브랜치를 옮겼으면 CLAUDE.md 를 다시 읽는다 (처음 로드된 게 옛 판일 수 있다).
- ⛔ friendly 에는 push 하지 않는다. CLAUDE.md 의 "friendly 에만 커밋/푸시" 는 이 세션에서 "friendly 에는 쓰지 않는다 · 커밋·푸시는
  <이 세션 브랜치> 에만" 으로 읽는다 (사용자 2026-10-02 대피 지시). friendly 반영은 ■6 대로만.
- ⛔ 원격(kgy·gabia)에서 git push 하는 블록도 <이 세션 브랜치> 로 보낸다 (friendly 로 보내면 복귀가 fast-forward 가 안 된다).
- PR 만들지 않는다 · force-push 는 --force-with-lease 만 · 커밋 메시지에 모델 ID 를 넣지 않는다.

■ 2. 먼저 읽을 것 (통째로 말고 grep · 부분 읽기)
- kb/projects/handoff_2026_10_02_evacuation.md  ← 이 인계 카드 (상태표 · 원격 · 바로 쓸 블록 · 주의)
- kb/open_items.md 의 ⏭ 절 맨 위 (grep -n "⏭-NOW-z5\|W_ad P1b\|li2s 유리 MD v2" kb/open_items.md)
- 점착: db/pipelines/adhesion_pipeline.json (log 마지막 4 줄) · db/properties/wad_agc_graphite_prereg_2026_10_02.json (P1b 카드 · ratified)
- 값·판정은 원장이 이긴다: db/governance/decisions.json · db/properties/canonical_registry.json · db/properties/citation_hazards.json

■ 3. 시작 점검 (종료코드로 판정 · set -o pipefail · 대피 직전 friendly 기대값을 옆에 적었다)
  set -o pipefail
  python3 tools/kb_wiki.py lint | tail -1                     # 0 errors
  python3 tools/db/validate_canonical.py | tail -2            # 거버넌스 결정 107 · 그래프 무결성 ✅ · 배선 전부 일치
  python3 tools/convention_check.py | tail -1                 # 0 위반
  python3 -m pytest webapp/tests -q -p no:cacheprovider | tail -2      # 634 passed · 2 skipped · 0 failed (repo 루트에서 돌린다)
  python3 tools/wad/agc_graphite.py --selftest | tail -1      # 47 통과 · 0 실패 ✅
  python3 tools/wad/cc_graphite.py --selftest | tail -1       # 53/53
  python3 tools/doping/judge_eprime.py --selftest | tail -1   # selftest PASS
  ⚠ 10-01 에 cascade 매니페스트 3 건 빨간불은 풀렸다 (12aaf523d) — 지금은 0 failed 가 정상이다. 빨간 게 있으면 새 문제다.

■ 4. 지금 상태 (원격은 10-02 22:05 KST 실측이 마지막 — 그 뒤는 사용자가 붙여 주는 출력으로만 쓴다)
- 점착 P1b Ag(111)|흑연 3층 (트랙 W_ad DFT · 1저자 = 사용자 · 결정 D-2026-10-02-wad-agc-graphite active):
  kgy 발사 블록 전달 (tmux agc · worktree ~/wt_agc_1002 @4d855c75c · RUN ~/work/runs/wad_agc_graphite_2026_10_02 ·
  watch: watch -n 60 bash ~/bin/agc_watch.sh). 1단계 = 기계 대조 CTRL 2 (V2 입력 그대로) → 이완 5 → (자동) 2단계 입력 → SCF 31 → 집계.
  ⏭ CTRL 두 잡 끝나면 G1 (V100 W 0.435487 와 |ΔW| ≤ 0.002 · FAIL → 헤드라인 보류) · 속도 (V100 179 · 140 s) → 첫 이완 벽시계로 총 견적 →
  7 일 넘으면 V100 으로 옮길지 사용자에게 묻는다 (카드 §8). 인계 카드 §4 에 바로 쓸 블록이 있다.
- 점착 V5 VASP 외주 (사용자): 09-30 업체 발송 · 파일럿 2 잡 반송 대기 → build_v5_vasp_package.py --check → --seal_pp → 사용자가 업체에 확인 →
  16 잡 → --collect → G5. 사용자 10-02: "외주한거 오면 관련해서 더 진행하자" — 오기 전엔 다른 점착 새 계산 없음 (P1b 는 사용자가 따로 승인).
- 점착 DEM 회신 9 (SE 쌍 UMA+D3 예측 · 사용자 검토·발송 대기) — V2 registry 중복 정정 한 줄을 넣을지 사용자 판단 (카드 §5).
- li2s 유리 MD v2 (⛔ 외부 1저자 · 사용자 승인 = 실행 승인일 뿐): kgy 몫 5 런 끝 (10-02 12:56) · gabia 몫 5 런 (tmux glassv2 · 10-01 01:43 발사) 상태 모름.
  카드 v2 proposed · 외부 1저자 동의 = 편지 CO (사용자 발송 대기). 두 기계 다 끝나면 원자료 회수 → 판독은 카드 v2 규칙대로.
- 탄성 modelc_2x (사용자): gabia tmux el_mc2x_1001 · 23_m 재개 (10-01 03:28 · BFGS 20 승계) 가 마지막 실측 · 남은 13_p/m · 12_p/m → fit.
- cascade (사용자): D_rel 파일럿 닫힘 (v6 방법상 무효). v7 탐침 카드 proposed — 편지 CP 는 codex 토큰이 없어 사용자가 기억해 두기로 (보내라고 재촉하지 않는다).
  살리는 길 제안 (사용자 미결): ① DFT 작은 대비 (PS₄ → PS₃O 옆 Li 홉 NEB · 권고) ② v7 ③ 글(정정 이력). '산화 안정 ↔ 수송 상충' 깔때기 발견은
  blocking 지표(4 Å 안 Li 비율 · S·Cl 안 셈) 탓일 수 있다는 경고 추가 제안도 미결.
- 대기 (사용자 몫): DEM 회신 9 · li2s 편지 CO · 9 월 gabia 증빙 캡처 · 용도 설명서 SEI 줄 · NEB collect (kgy) · 원고 Fig 2e.

■ 5. 충돌 안 나게 — 대피 중에 지킬 것 (복귀가 fast-forward 면 아래는 보험이다)
- friendly 에 쓰지 않는다 (■1). 이게 지켜지면 복귀는 충돌 0 이다.
- 그래도 보험으로, 같이 쓰는 파일은 **덧붙이기**로만 고친다:
  · kb/open_items.md — 새 블록은 ⏭ 절 맨 위에 "### ⏭-NOW-z6. … (대피)" 로 얹는다. 남의 줄은 지우거나 다시 쓰지 말고, 끝에 " · ⏩ 10-0x …" 를 붙인다.
    머리 줄(최종 갱신)은 바꿔도 되지만 굵게를 겹쳐 쓰지 않는다 (대시보드 시험이 깨진다).
  · db/governance/decisions.json — 새 결정은 끝에 추가 · 비준된 결정 본문은 한 글자도 고치지 않는다 (digest 가 깨진다) ·
    proposed → active 는 그 결정만 (status_history · ratification 추가). 저장은 json.dumps(…, ensure_ascii=False, indent=1) + "\n".
  · db/pipelines/adhesion_pipeline.json — log 는 끝에 한 줄씩 · systems/runs 는 그 항목만 고친다 · 저장 indent=1 (끝 줄바꿈 없음).
  · kb/index.md — 손으로 고치지 않는다. python3 tools/kb_wiki.py index 로만.
  · CLAUDE.md — 꼭 필요할 때만, 그 절 끝에 덧붙인다 (재배치·정리 금지).
- JSON 을 통째로 다시 정렬·재포맷하지 않는다 (키 순서·들여쓰기 그대로) — diff 가 커지면 보험이 무너진다.
- ⛔ litdb 의 DEM 쪽 파일은 고치지 않는다 — friendly 에 직접 쓰는 다른 세션(litdb tortuosity · session_01H191Ni4xzj9H5ftstAm7Ft)의 영역이다:
  그 세션이 만든 litdb/papers 카드 · litdb/figures · litdb/INDEX_DEM.md · litdb/comparison_vs_ours_DEM.md · build_index.py 산출물.
  우리 쪽 문헌을 더해야 하면 litdb/INDEX.md · litdb/comparison_vs_ours.md 에 덧붙이고, 인덱스는 손으로 말고 생성기로만 다시 만든다.

■ 6. friendly 로 돌아가기 (사용자가 "돌아가자" 할 때만)
- 이 브랜치를 push 하고 두 문서를 쓴다 (09-28/29 선례 그대로):
  kb/projects/merge_request_<날짜>.md — 커밋 표 (git log --oneline origin/claude/friendly-meitner-lldvar..HEAD) · 돌린 시험·종료코드 ·
    원장 변화 (새 결정·비준) · 원격에서 아직 도는 것 · 빨간불.
  kb/projects/handoff_<날짜>_return_to_origin.md — friendly 세션에 붙일 §0 프롬프트: ① 아무것도 쓰기 전에 git status · FF 확인
    ② 경우 A (FF 가능): git merge --ff-only origin/<이 세션 브랜치> → push (강제 없이)
    ③ 경우 C (friendly 가 움직였음 — litdb 세션 때문에 **이쪽이 기본**일 수 있다): 멈추고 묻기 → 허락 뒤 git merge --no-ff ·
       ⛔ rebase 금지 (커밋 해시가 결정 원장 ratification.commit · 기록 · 원격 worktree 에 박힌다) · litdb 인덱스류가 겹치면 양쪽을 받은 뒤 생성기로 재생성
    ④ 파일별 충돌 규칙 (■5 와 같은 원칙 · decisions 는 id 합집합 · open_items 합집합 · kb/index.md 재생성) ⑤ 머지 뒤 점검 기대값.
- 대피 브랜치는 지우지 않는다 (기록이다).
- ⚠ 사용자가 로컬 웹앱을 보려고 로컬 체크아웃을 이 브랜치로 옮겼다면, 복귀 머지 직후 되돌리라고 반드시 말한다:
  git switch claude/friendly-meitner-lldvar && git pull --ff-only   (09-28 대피 때 실제로 놓칠 뻔했다).
- 세션을 닫기 전에 kb/open_items.md 의 ⏭ 절을 갱신한다.

■ 7. 사용자 운영 규칙 (어기면 바로 잡힌다)
- 원격 작업은 "붙여넣기 블록 → 사용자가 실행 → 출력 회수". ssh 로 명령을 주지 않는다. 붙여 준 출력은 하나씩 보고 해석한다 — 앞서가지 않는다.
- ⛔ 인증을 묻는 명령(git push) 뒤에는 다른 줄을 두지 않는다 — 뒤에 할 일은 같은 줄에 && 로 (10-01 kgy: 다음 줄이 Username 으로 들어갔다).
- 큰 계산은 GPU 로만. gabia 에서 GPU pw.x 와 UMA 를 겹치지 않는다 (예외는 원장 active 결정만). kgy 는 프로세스 정보가 막혀 있다.
- 프로세스는 PID 나 잡 고유 인자로만 죽인다 (pkill -f pw.x · python · 스크립트 이름 금지).
- ⛔ 돌고 있는 러너의 worktree 를 다른 커밋으로 옮기거나 지우지 않는다 (bash 가 스크립트를 읽는 중이다) — kgy ~/wt_agc_1002 · gabia 탄성·li2s worktree.
- 봉인 카드 · 리뷰 회신 원문 · 비준된 결정은 고치지 않는다 (정정은 새 파일 · 덧붙임으로).
- 점착 W 값은 webapp 화면에 싣지 않는다 (결과 기록에만 · 화면 게재는 사용자 별도 결정).
- `1저자` 는 트랙마다 다르다 — 결정 항목을 쓸 때 트랙을 먼저 쓴다 (점착·cascade·ESW·탄성 = 사용자 · li2s = 외부 1저자 · CEI = 실험 쪽 다른 사람).
- 한국어 대화체로 짧게 · 그림 라벨은 영어 · 새 개념은 한 단계씩.

첫 답은: ■1 브랜치 결과 · ■3 점검 결과를 한 줄씩, 그리고 "kgy watch 출력이 있으면 붙여 주세요 — P1b 기계 대조부터 봅니다" 한 줄.
원격 명령 블록은 사용자가 요청할 때나 붙여 준 출력의 다음 한 수로만 준다.
```

---

## 1. 이 세션이 마지막으로 한 일 (10-01 ~ 10-02)

| 무엇 | 어디 |
|---|---|
| cascade v6 판독 (카드 정의 곡선) → 자격 0/40 · **방법상 무효로 마감** · 원자료 푸시 | `cascade_d_rel_closed_2026_10_01.json` · `db/raw/cascade_v6_2026_10_01/` |
| cascade 화면 fail-closed 해제 · 깔때기 G2 정정 창 · OCV 빈칸 = 안정창 없음 (21 탈락 · v3_pinned 82 행) | `cascade_screening_funnel_v2.json` · 결정 2 건 (10-01) |
| D_rel v7 탐침 카드 (proposed) · 편지 CP 초안 — **발송 보류** (codex 토큰 없음 · 사용자가 기억) | `cascade_estimand_card_v7_probe_2026_10_01.json` · `kb/reviews/codex_CP_prompt_…` |
| 'S→O 를 본 이유 (b2o3 모순)' 서술 검증 — 인용은 정확 · 09-12 첫 카드는 BN NO-GO · blocking 은 경로 폐색이 아니라 4 Å 안 Li 비율(S·Cl 안 셈) · 최하위는 불화물 · 정적 대조 순서 거꾸로 | 이 세션 대화 (기록 안 함 — 결론만 아래 §5) |
| 점착: 외주 V5 반송까지 대기 기록 · **P1b 카드·도구·입력** · V2 registry 대칭 중복 발견 · kgy 점검(DRY_RUN) · **비준** | `wad_agc_graphite_prereg_2026_10_02.json` · `tools/wad/agc_graphite.py` · `db/inputs/wad_agc_graphite_2026_10_02/` |
| li2s v2 kgy 몫 5 런 끝 기록 | `kb/open_items.md` |

## 2. 트랙별 상태 (1저자 먼저)

| 트랙 | 1저자 | 상태 (마지막 기록) | 다음 한 수 | 누구를 기다리나 |
|---|---|---|---|---|
| 점착 P1b (Ag\|흑연 3층) | 사용자 | kgy 발사 블록 전달 (10-02 밤) · 발사 출력 미확인 | CTRL 2 → G1 · 속도 → 첫 이완 → 총 견적 (7 일 기준) | 계산 · 사용자 watch |
| 점착 V5 VASP | 사용자 | 09-30 외주 발송 | 파일럿 2 잡 반송 → `--check` → `--seal_pp` | 업체 |
| 점착 DEM | 사용자 | 회신 9 초안 (SE 쌍 예측) | 사용자 발송 (+ V2 registry 정정 한 줄 여부) | 사용자 |
| li2s 유리 v2 | **외부 1저자** | kgy 몫 끝 (10-02 12:56) · gabia 몫 모름 | gabia 상태 확인 → 원자료 회수 → v2 판독 | 계산 · 편지 CO (사용자 발송) |
| 탄성 modelc_2x | 사용자 | 23_m 재개 (10-01 03:28) | watch 로 진행 확인 → 13_p/m · 12_p/m → fit | 계산 |
| cascade | 사용자 | D_rel 닫힘 · v7 proposed · CP 보류 | 살리는 길 선택 (① DFT NEB 권고 · ② v7 · ③ 글) | 사용자 |
| ESW | 사용자 | 정정 적용 끝 · `b2o3_esw.json` 은 옛 폭 (머리 경고) | — (요청 없으면 안 건드림) | — |

## 3. 원격 — 지금 도는 것 · 건드리지 말 것 (10-02 22:05 KST 기준)

- **kgy · P1b** (발사 블록 줬음 · 출력 미확인): tmux `agc` · worktree `~/wt_agc_1002` (@4d855c75c — ⛔ 도는 동안 checkout·삭제 금지) ·
  RUN `~/work/runs/wad_agc_graphite_2026_10_02` (`run_kgy.log` · `stage1/runner.log` · `stage1/jobs_run.tsv`) · watch `~/bin/agc_watch.sh`.
  pw.x `~/apps/qe-7.4.1-gpu/bin/pw.x` (sha 256293a3 · V100 은 912d8c8f) · PP `~/work/pseudo` (Ag `0494aa59` · C `9900d1ef` ✓) · RAM 58 GB · 디스크 304 GB.
  ⚠ GPU 에 출처 모를 잡 96 % · 0.8 GB (프로세스 정보 막힘) — 같이 돈다. 가드 = 합계 > 23,000 MiB 면 **우리 잡만** 멈춤.
- **kgy · li2s v2**: 큐 끝 (10-02 12:56:44 · `■ 큐 끝 · 600:1:400 550:2:800 600:3:400 550:4:800 550:5:800`).
- **gabia · 탄성 modelc_2x**: tmux `el_mc2x_1001` · 로그 `/root/logs/el_modelc2x_1001.log` · watch `ALL=1 bash tools/elastic/watch_elastic.sh` (러너 worktree 건드리지 않는다).
- **gabia · li2s v2 몫**: tmux `glassv2` (10-01 01:43 발사 · 예외 `D-2026-09-30-gabia-uma-coexist-elastic-li2s-v2` · 5 런 끝나거나 탄성 끝나면 소멸).
- ⚠ gabia `/data/work/repo` 자동 repack `bad object worktrees/wt_li2s_v2_0930/HEAD` (10-01 · 미해결 · 읽기 전용 조사만 · gc·prune 금지).

## 4. 바로 쓸 블록 (kgy)

**(a) CTRL 두 잡이 끝났을 때 — 기계 대조 G1 · 속도 (읽기만 · 돌고 있는 러너와 무관)**
```bash
cd ~/wt_agc_1002 && /home/kgy/apps/miniforge3/envs/uma/bin/python -c "import sys,json; sys.path.insert(0,'tools/wad'); import agc_graphite as G; r=G.ctrl_check('db/inputs/wad_agc_graphite_2026_10_02/stage1','$HOME/work/runs/wad_agc_graphite_2026_10_02/stage1'); print(r['status'], 'ΔW', r['dW_J_m2'], '· W here', r['W_here_J_m2'], '· ΔF meV', r['dF_vs_V100_meV_info'], '· 속도', {k:v['ratio'] for k,v in r['speed_info'].items()})"
```
기대: `PASS ΔW (|·| ≤ 0.002)` · ΔF 는 정보 · 속도 = V100 대비 느린 배수. FAIL 이면 헤드라인 보류 (MACHINE_MISMATCH) — 원인(바이너리·D3 구현) 확인 전 계속 돌려도 되지만 V2·WAD-CC 와 같은 표에 놓지 않는다.

**(b) 총 견적 (첫 이완이 끝난 뒤 · 어림)** — 1단계 ≈ 이완 5 × 첫 이완 벽시계 (N4 는 조금 더) · 2단계 ≈ 31 × (CTRL 한 잡 벽시계 × 3–5 — 원자 20 → 36 · 셀 c 24 → 35 Å).
7 일을 넘으면 사용자에게 V100 으로 옮길지 묻는다 (러너를 PID 로 멈추고 같은 입력을 V100 run_sese_gpu.sh 로 · G1 이 같은 입력 대조로 지킨다).

**(c) 이완 하나가 실패하면** (러너가 rc 6 으로 멈춤 → run_kgy rc 2): 카드 §4 — 그 모델 INCOMPLETE (교체 없음). 나머지만:
`JOBS="<남은 1단계 잡 …>" STAGE=1 PWX=… bash db/inputs/wad_agc_graphite_2026_10_02/run_kgy.sh` → `STAGE=2 PWX=… bash …` (tmux 안).
2단계 SCF 미수렴: `FALLBACK="<그 잡>" PWX=… bash …/run_kgy.sh` (β 0.1 판 한 번 · 나머지 재개 · 집계).

**(d) 다 끝나면 — 원자료 회수 (새 worktree · <이 세션 브랜치> 로 push · 한 줄)**
러너 worktree(`~/wt_agc_1002`)에서 커밋하지 않는다. `~/lldvar` 에서 `git fetch origin <이 세션 브랜치>` → `git worktree add --detach /tmp/wt_agcraw FETCH_HEAD` →
RUN 을 `tmp/` 빼고 `db/raw/wad_agc_graphite_2026_10_02/` 로 복사 (+ sha256 manifest) → 커밋 →
`git push origin HEAD:<이 세션 브랜치> && cd ~/lldvar && git worktree remove --force /tmp/wt_agcraw && echo "push ✓"` (push 뒤 다른 줄 금지).
repo 에서: `agc_graphite.py --verify_stage2 <raw>/stage2_pkg --stage1_dir … --relax_raw <raw>/stage1` → `--collect … --atm` → 결과 기록 → 점착 원장 → DEM 회신 (값은 화면에 안 싣는다).

## 5. 주의 — 다음 세션이 밟기 쉬운 것

- ⚠ **V2 의 registry 넷은 대칭으로 둘이다** (bridge ≡ top_fcc 병진 · top_hcp ≡ hollow_fcc 거울 · W 16 자리 같음 · 3e-6 차) — V2 값 0.435 는 그대로, "registry 4" 를 "비등가 2" 로 읽는다
  (`wad_aprime_pilot_result_v2_2026_09_26.json` 덧붙임). DEM 회신 5 에 "registry 4 곳 모두 같은 값" 이라 썼다 — 회신 9 에 한 줄 넣을지 사용자 판단.
  P1b 는 흑연 3층에서 쌍별 비등가 넷 (top_fcc · top_hcp · hollow_fcc · s01) — 흑연 2층이 거울을 깬다.
- ⚠ **kgy 3090 은 FP64 가 약하다** — QE 가 V100 보다 몇 배 느릴 수 있다. 속도 판단은 CTRL·첫 이완 실측으로만.
- ⚠ **FETCH_HEAD 는 worktree 마다 따로다** — worktree 를 갱신할 땐 그 안에서 fetch.
- ⚠ **'b2o3 모순' 서술**: 09-12 첫 카드 원문 그대로지만 같은 날 리뷰 BN NO-GO — blocking 은 '4 Å 안 Li 비율' (S·Cl 도펀트 원자 안 셈 · 경로 폐색 아님) ·
  최하위 족은 산화물이 아니라 불화물 (0.714) · 정적 대조는 BN P0-4 가 먼저 요구했고 S 힘 10.6 배는 그 결과 (구성 (b) = UMA 완화 구조라 UMA 힘이 원래 ~0) ·
  파일럿은 v5 에서 탄성 보류 → 수송만 · 양이온은 Al. 이걸 다시 설명할 때 이 사실들을 섞지 않는다.
- ⚠ **cascade 편지 CP 는 보내라고 재촉하지 않는다** (사용자가 기억). v7 탐침은 돌리지 않는다 (카드 proposed).
- 원격 실측 없이 *"돌고 있다"* 고 쓰지 않는다. `pgrep -f` 개수는 자기 자신을 센다 — PID 를 잡아 `kill -0`.

## 6. 이 카드가 못 하는 것

- 원격 기계의 **지금** 상태를 말하지 않는다 — 10-02 22:05 KST (kgy 점검) 가 마지막이다. P1b 발사 출력은 못 봤다.
- 결정의 비준을 대신하지 않는다 — proposed 인 것 (cascade v7 탐침 · li2s v2 카드 등) 은 여전히 proposed 다.
- 다음 세션에 배정될 **브랜치 이름을 모른다** — 프롬프트는 `<이 세션 브랜치>` 로 적었다.
