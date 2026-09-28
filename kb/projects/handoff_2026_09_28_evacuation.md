---
title: "대피 인계 — 2026-09-28 (friendly 세션 컨텍스트 소진 → 서브 브랜치 임시 작업)"
date: 2026-09-28
updated: 2026-09-28
tags: [handoff, session, evacuation, branch, wad, li2s, elastic, vasp]
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

# 대피 인계 — 2026-09-28

> 본 세션(`claude/friendly-meitner-lldvar`)이 컨텍스트를 다 써서, 다음 세션은 **서브 브랜치에서 잠깐** 이어 간다
> (사용자 2026-09-28: *"평소에 하던것처럼 서브 브랜치로 잠깐 대피"*). 선례: `handoff_2026_09_16_cathode_cei.md` ·
> 다른 브랜치의 복귀 프롬프트·병합 요청 문서.
>
> ⚠ 이 카드가 쓰일 때 **원격 기계 상태는 09-27 14:02 실측이 마지막**이다. 이 세션은 그 뒤 원격을 안 건드렸다.
> 여기 적힌 "진행 중" 은 **그때 기준**이지 지금 사실이 아니다 — 다음 세션은 사용자가 붙여 주는 출력으로만 갱신한다.

## 0. 새 세션에 붙여 넣을 프롬프트

```text
[대피 세션 시작 — 2026-09-28]

너는 Yonghoon-DEM-DFT 캠페인의 임시 대피 세션이다. 본 세션(브랜치 claude/friendly-meitner-lldvar)이
컨텍스트를 다 써서 이 서브 브랜치로 잠깐 옮겨 왔다. friendly 세션이 하던 일을 그대로 이어 간다.

■ 1. 브랜치 (제일 먼저 · 이것부터 틀리면 다 틀린다)
- git fetch origin claude/friendly-meitner-lldvar
- 이 세션 브랜치가 friendly 끝을 포함하지 않고(git merge-base --is-ancestor origin/claude/friendly-meitner-lldvar HEAD 실패)
  아직 내가 만든 커밋도 없으면, friendly 끝에서 다시 시작한다:
    git checkout -B <이 세션 브랜치> origin/claude/friendly-meitner-lldvar
  이미 커밋이 있으면 멈추고 사용자에게 묻는다.
- 브랜치를 옮겼으면 CLAUDE.md 를 다시 읽는다 (처음 로드된 게 옛 판일 수 있다).
- 커밋·푸시는 이 세션 브랜치에만. CLAUDE.md 의 "friendly 에만 커밋/푸시" 는 이 세션에서는
  "friendly 에는 push 하지 않는다" 로 읽는다 (사용자 지시 2026-09-28). friendly 반영은 아래 5 번대로만.
- PR 만들지 않는다 · force-push 는 --force-with-lease 만 · 커밋 메시지에 모델 ID 를 넣지 않는다.

■ 2. 먼저 읽을 것 (통째로 말고 grep · 부분 읽기)
- kb/projects/handoff_2026_09_28_evacuation.md  ← 인계 카드 (상태표 · 열린 일 · 주의)
- kb/open_items.md 의 ⏭-NOW-y · ⏭-NOW-x 블록  (grep -n "⏭-NOW-[xy]" kb/open_items.md)
- kb/reports/weekly_2026_09_27.md  ← 09-21~27 전체 흐름 (처음 보는 사람용으로 썼다)
- 값 · 판정은 원장이 이긴다: db/governance/decisions.json · db/properties/canonical_registry.json ·
  db/properties/citation_hazards.json · 점착은 db/pipelines/adhesion_pipeline.json

■ 3. 시작 점검 (종료코드로 판정 · 파이프가 실패를 삼키지 않게 set -o pipefail)
  set -o pipefail
  python3 tools/kb_wiki.py lint | tail -2
  python3 tools/db/validate_canonical.py | tail -2
  python3 tools/convention_check.py | tail -2
  python3 -m pytest webapp/tests -q -p no:cacheprovider | tail -3
  ⚠ 웹앱 시험은 cascade 3 건 빨간불이 정상이다 (09-28 기준 584 passed · 2 skipped · 3 failed):
    test_cascade_headline_comes_from_the_manifest · test_manifest_tamper_fails_closed · test_audit_figures_are_the_only_default_figures
    09-22 ESW 가장자리 수정이 해시 박힌 4 파일을 바꿔서 화면이 fail-closed 다 (kb/open_items.md ⏭-NOW-w).
    ⛔ manifest 해시만 다시 박아서 초록불로 만들지 않는다 — 풀 입력 → 퍼널 → 감사 그림 → manifest 순서로 다시 만들어야 하고
    퍼널 통과 목록이 바뀔 수 있어 1저자(사용자) 결정이다. 이 3 건 말고 다른 게 빨가면 그건 새 문제다.

■ 4. 지금 상태 (원격은 09-27 14:02 실측이 마지막 — 그 뒤는 사용자가 붙여 주는 출력으로만 쓴다)
- 점착 W_ad (1저자 = 사용자): gabia V4 본 잡 9 개 (tmux v4main) — bound 끝 · far 진행이 마지막 실측.
  끝나면 collect_aprime_s4.py --v4 → 결과 기록 → DEM 회신 7 (+V2 D3 ATM 열) → 점착 DFT 마감 기록.
- V5 VASP 외주 (1저자 = 사용자): 준비본 v6 Codex CK GO. 개정 v6.1 비준은 1저자가 외주 보낼 때 알려 준다 — 먼저 꺼내지 않는다.
- li2s 유리 (외부 1저자): 편지 CH 회신 대기. 사용자의 "진행해" 는 실행 승인이지 외부 1저자의 동의가 아니다 → 우리 판단은 잠정.
- 탄성 modelc_2x (1저자 = 사용자): 23_p 를 EXIT 로 세웠다 (BFGS 67 · .bfgs 저장). 재개는 V4 가 GPU 를 비운 뒤.
  재개 방식은 인계 카드 §3 의 ⚠ 를 먼저 보고 1저자에게 묻는다.
- 끝난 것: b2o3 사건빈도 결과 (봉인 문장만 인용) · Nd ICOHP 닫힘 · 주간보고 게시.
- 대기: cascade 산물 갭 재생성 (HOLD) · Li₂S 4×4×4 gabia 재프로브 (탄성 뒤).

■ 5. friendly 로 돌아가기 (사용자가 "돌아가자" 할 때만)
- 이 브랜치를 push 하고 kb/projects/merge_request_<날짜>.md 를 쓴다:
  커밋 목록 (git log --oneline origin/claude/friendly-meitner-lldvar..HEAD) · 돌린 시험과 종료코드 ·
  원격에 아직 돌고 있는 것 · 충돌 여부.
- friendly 가 그사이 안 움직였으면 (fast-forward 가능) 사용자 허락을 받고
  git push origin HEAD:claude/friendly-meitner-lldvar  (강제 없이). 움직였으면 멈추고 rebase / merge 를 묻는다.
- 세션을 닫기 전에 kb/open_items.md 의 ⏭ 절을 갱신한다 (머리 줄에 굵게를 겹쳐 쓰지 않는다 — 대시보드 시험이 깨진다).

■ 6. 사용자 운영 규칙 (어기면 바로 잡힌다)
- 원격 작업은 "붙여넣기 블록 → 사용자가 실행 → 출력 회수". ssh 한 줄 명령으로 주지 않는다.
- 붙여 준 출력은 하나씩 보고 해석한다 — 앞서가지 않는다. 확실하지 않으면 history · 기록부터 확인한다.
- 큰 계산은 GPU 로만 (CPU 로 돌리는 계획을 세우지 않는다). gabia 에서 GPU pw.x 와 UMA 를 겹치지 않는다.
- 프로세스는 PID 나 잡 고유 인자로만 죽인다 (pkill -f pw.x · python · 스크립트 이름 금지).
- 봉인 카드 · 리뷰 회신 원문 · 비준된 결정은 고치지 않는다 (정정은 새 파일 · 정오 기록으로).
- 점착 W 값은 webapp 화면에 싣지 않는다 (결과 기록: "화면 게재는 1저자 별도").
- 한국어 대화체로 짧게 · 그림 라벨은 영어 · 새 개념은 한 단계씩.

첫 답은: 1 번 브랜치 결과 · 3 번 점검 결과를 한 줄씩, 그리고 "무엇부터 할까요" 한 줄.
원격 명령 블록은 사용자가 요청할 때만 준다.
```

---

## 1. 이 세션이 마지막으로 한 일 (09-27 ~ 09-28)

| 무엇 | 어디 |
|---|---|
| 주간보고 09-21~27 (처음 보는 사람용 · 용어 풀이 · 그림 3) | `kb/reports/weekly_2026_09_27.md` · 화면 `/weekly` |
| 주간보고 그림 도구 (selftest 양성 12 · 음성 8 · 음성 가드 6 개 지워 빨간불 확인) + Origin CSV 4 | `tools/figures/fig_weekly_2026_09_27.py` · `db/properties/*_origin_2026_09_27.csv` |
| 지난 두 주 주간보고 제목 요일 정정 (월 ~ 일) | `kb/reports/weekly_2026_09_14.md` · `weekly_2026_09_20.md` |
| ⏭ 절 머리 줄 겹친 굵게 → 대시보드 `**` 누출 수정 (웹앱 시험 1 건) | `kb/open_items.md` ⏭ 머리 · ⏭-NOW-y |
| (그 전) V5 VASP 준비본 Codex CK GO · zip 인계 · litdb 2 편 · 규칙 2 (홉 수 검산 · C5 열린 껍질) · 그림 추출기 누락 수정 | ⏭-NOW-x · `CLAUDE.md` |

## 2. 트랙별 상태 (1저자 먼저)

| 트랙 | 1저자 | 상태 (마지막 기록) | 다음 한 수 | 누구를 기다리나 |
|---|---|---|---|---|
| 점착 A′ V4 | 사용자 | gabia `v4main` 9 잡 · bound 끝 (09-27 14:02) | 9 잡 끝 → `collect_aprime_s4.py --v4 <S3v2 패키지> --raw <원자료>` → 결과 기록 | 계산 (watch 출력은 사용자가 붙여 줌) |
| 점착 마감 | 사용자 | V2 보고 끝 · DEM 열린 질문 0 | V4 결과 → DEM 회신 7 (+V2 ATM 열) → 마감 기록 (경보 원인 미분류로 닫는 문장 · 재개 조건 먼저) | V4 |
| V5 VASP 외주 | 사용자 | 준비본 v6 · Codex CK GO · 개정 v6.1 초안 · 결정 proposed | 1저자 비준 → 업체·예산 → 파일럿 2 잡 | **1저자가 외주 시점을 알려 줌** |
| li2s 유리 | **외부 1저자** | 편지 CH 발송 (09-27) · 개정 초안 v2 · 결정 proposed | 회신 오면 원문 보존 → 개정 v2 확정·비준 → 본 런 15 런 설계 | 외부 1저자 회신 |
| 탄성 modelc_2x | 사용자 | 23_p EXIT 정지 (BFGS 67 · `.bfgs` 3.9 MB 저장) · 러너 bash 248598 `T` | V4 뒤 재개 — 아래 §3 ⚠ | V4 · 1저자 |
| b2o3 사건빈도 | 사용자 | 결과 기록 끝 | — (재개 조건 밖) | — |
| cascade 산물 갭 | 사용자 | HOLD (비바닥 다형 241/352) | `run_cascade_extras.sh` 재생성 | 기계 여유 |
| cascade 화면 | 사용자 | **fail-closed** (09-22 ESW 수정이 manifest 해시 4 파일을 바꿈 · 웹앱 시험 3 건 빨간불 = 정상 경보) | 풀 입력 → `build_screening_funnel.py` → 감사 그림 → `build_cascade_audit_manifest.py` (해시만 다시 박지 않는다) | 1저자 — 퍼널 통과 목록이 바뀔 수 있다 |
| Li₂S 4×4×4 셀수렴 | 사용자 | kgy 탐침 45 GB 로 중단 | 탄성 끝난 뒤 gabia 단독 재프로브 | 탄성 |

## 3. 주의 — 다음 세션이 밟기 쉬운 것

- ⚠ **탄성 재개 방식이 기록 안에서 두 가지로 적혀 있다.** ⏭-NOW-x 의 *"재개 = `kill -CONT 248598`"* 는 **러너 결함 수정
  (c181c2f3e · 09-27) 전** 문장이다. 수정 뒤 기록은 *"23_p 를 세웠으면 재개는 새 러너로만 — 옛 러너 코드는 세운 계산을
  `unconverged` 로 보고 처음 좌표부터 돈다"* 이다. 248598 은 **옛 코드로 떠 있는 프로세스**다 ⇒ CONT 하면 23_p 를 실패로
  찍고 23_m 으로 넘어갈 수 있다. **어느 쪽으로 할지 1저자에게 묻고**, 정리는 PID 로만 한다.
- ⚠ **V4 는 조각 모형이다** — G3/G4 는 ΔE_frag(eV/조각)의 **변화** 5·10 meV 로 판정하고 J/m² 로 바꾸지 않는다
  (결정 `D-2026-09-23-wad-a-prime-scope` ⑦ · 정오 `wad_aprime_gate_reading_erratum_2026_09_27.json`).
- ⚠ **대시보드 시험**(`test_no_literal_bold_markers_in_rendered_body`)은 `kb/open_items.md` 의 `##`·`###` 제목을 그대로 읽는다 —
  제목에 굵게를 겹치면 빨간불이다. 09-27 에 한 번 깨졌고 이 세션이 고쳤다.
- ⚠ **li2s 는 외부 1저자 트랙**이다 — 결정 항목을 쓸 때 트랙을 먼저 적는다 (CLAUDE.md 소통 절).
- 원격 실측 없이 *"돌고 있다"* 고 쓰지 않는다. `pgrep -f` 개수는 자기 자신을 센다 — PID 를 잡아 `kill -0`.

## 4. 이 카드가 못 하는 것

- 원격 기계의 **지금** 상태를 말하지 않는다 — 09-27 14:02 실측이 마지막이다.
- 결정의 비준을 대신하지 않는다 — proposed 두 건(`D-2026-09-27-wad-aprime-v5-vasp-route` ·
  `D-2026-09-26-lpscl-smallcell-glass-amend-cc`)은 여전히 proposed 다.
- 다음 세션에 배정될 **브랜치 이름을 모른다** — 프롬프트는 `<이 세션 브랜치>` 로 적었다.
