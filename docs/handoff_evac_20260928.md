# 대피 인계 — `claude/stoic-knuth-NObVQ` 세션 → 연장 세션 (2026-09-28)

**작성** 2026-09-28 오전 · **작성 세션** stoic-knuth (컨텍스트 소진으로 잠시 대피)
**대상 독자** 이 문서를 받아 이어 일할 새 세션

## 0. 한 줄

앞 세션의 기억은 **이 대화에 없다** — 상태는 전부 리포에 있다.  규칙은 `CLAUDE.md` 가 정본이고, 오늘 상태와 남은 일은
`docs/session_20260923_progress.md` 의 **㉖** 에 있다.

## 1. 브랜치

- 배정받은 작업 브랜치를 **`origin/claude/stoic-knuth-NObVQ` 최신에서** 시작한다.  ⚠ 리포의 GitHub 기본 브랜치
  (`claude/dft-script-generator-webapp-GPSAG`) 는 **다른 계보**다 — 거기서 시작하지 않는다 (`docs/handoff_merge_to_stoic_knuth_20260915.md` §1).
  ```
  git fetch origin claude/stoic-knuth-NObVQ
  git log -1 --format='%h %s' FETCH_HEAD            # 이 문서를 담은 커밋 이후여야 한다
  git checkout -B <배정 브랜치> FETCH_HEAD            # 배정 브랜치에 아직 커밋이 없을 때만
  ```
- 작업은 배정 브랜치에 커밋 · 푸시한다.  stoic-knuth 로 되돌리는 병합은 **fast-forward** 여야 하고
  (`git merge-base --is-ancestor origin/claude/stoic-knuth-NObVQ HEAD`), **사용자 비준 뒤**에만 한다.

## 2. 먼저 읽을 것 (순서)

1. `CLAUDE.md` 맨 위 "현재 상태" 표 · ⛔ DO-NOT 블록 · "멈춘 런 재개 체크리스트"
2. `docs/session_20260923_progress.md` 의 ㉔ · ㉕ · **㉖** (최신 상태와 남은 일 ①–⑨)
3. 필요할 때: `docs/worklog/weekly_20260927.md` (지난 주 09-21 ~ 27 요약, 처음 보는 사람용)

## 3. 지금 돌고 있는 것 (09-28 오전)

| 기계 | 무엇 | 확인 |
|---|---|---|
| v100 | 재현 2 런 `rep288` (코드 세대 점검 — 판정선 `docs/se_curve_transfer_verdict_20260806.md` §⑩-b) | `grep -m3 -E '^venv:\|repo HEAD\|ABORT\|^=== ' ~/rep288.log` — `venv:` 줄이 eq288 과 같아야 (㉖) |
| WSL | 믹서 측정 10 런 (09-27 기준 60–69 %) · 재개-위상 영수증 v1 **통과** | 영수증 파일 `receipt_v1.json` 을 사용자가 올리면 `docs/data/mixer_phase_receipt_20260928/` 에 커밋 (㉖ ①) |
| ibb | 순수 SE `pse_r050_a` (job 233951, 60 MPI 재개) | 완주 뒤 prereg `docs/reviews/pure_se_union_prereg_20260927.md` §4 Q1–Q3 |
| kgy | Phase A 100 GPa 재현 STEP3 | prereg `docs/reviews/phase_a_replication_vgcf100_prereg_20260926.md` §4 |

## 4. 꼭 지킬 것 (최근 사고에서)

- **명령에 넣는 경로 · 인터프리터 · 환경은 그 기계의 기록으로 먼저 확인한다** (`SELF-55` · `SELF-57`).  v100 배치는 `(uma)` 셸에서 띄우면
  `activate_dem.sh` 가 venv 를 건너뛴다 → `conda deactivate` 뒤에 띄운다.  WSL 파이썬은 `~/Yonghoon-DEM-DFT/venv/bin/python3`.
- **멈춘 런은 `scripts/resume_ckpt.sh` 로만 잇는다** (믹서는 `scripts/make_mixer_resume.py`).  처음부터 다시 돌리지 않는다 (`SELF-54`).
- 믹서 검사 도구 (접촉 검사기 · 판독기 · 덱 비교기 · 영수증) 로는 **Codex 4 차 GO 전까지 발사 · 판정 결정을 하지 않는다**
  (요청서 `docs/reviews/codex_mixer_highbo_rereview3_request_20260928.md`, §0-b 포함).
- v100 의 `~/Yonghoon-DEM-DFT` 는 ps45 15 런이 끝날 때까지 **pull 금지** (`93a8b2d27` 로 eq288 과 같은 코드 — ps45 사전등록 §5).
- 커밋 전 `G=scripts/check_all; bash "$G.sh"` (명령줄에 스크립트 이름을 그대로 쓰면 자기 종료 사고가 난다).

## 5. 새 세션에 붙여 넣을 프롬프트

```
너는 claude/stoic-knuth-NObVQ 에서 일하던 세션의 연장 세션이다 (앞 세션 컨텍스트가 차서 잠시 옮겨 왔다).
앞 세션의 기억은 없고 상태는 전부 리포에 있다.

1) 배정 브랜치를 origin/claude/stoic-knuth-NObVQ 최신에서 시작해라 (리포 기본 브랜치 GPSAG 는 다른 계보라 쓰지 말 것):
   git fetch origin claude/stoic-knuth-NObVQ && git checkout -B <배정 브랜치> FETCH_HEAD   (배정 브랜치에 커밋이 없을 때만)
2) docs/handoff_evac_20260928.md 를 먼저 읽고, 거기 §2 순서대로 CLAUDE.md 상단 · docs/session_20260923_progress.md ㉖ 을 읽어라.
3) 규칙은 CLAUDE.md 가 정본이다: 보고 → 설명 → 비준 → 실행 · 커밋 전 check_all · 확인 안 한 경로/환경을 명령에 쓰지 않기 (SELF-55/57) ·
   멈춘 런은 resume_ckpt.sh 로만.
4) 첫 행동: 읽은 현재 상태를 짧게 요약하고, ㉖ 의 남은 일 ①–⑨ 중 무엇부터 할지 제안해라 (실행은 비준 뒤).
   지금 사용자에게 받을 것: WSL 영수증 파일 receipt_v1.json · v100 rep288 로그의 venv 줄.
5) 작업이 끝나면 배정 브랜치에 푸시하고, stoic-knuth 로의 fast-forward 병합은 사용자 비준 뒤에 한다.
```
