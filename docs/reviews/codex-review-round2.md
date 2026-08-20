---
title: Codex 2차 리뷰 과제 — 갱신 검증
created: 2026-08-20
updated: 2026-08-20
type: guide
tags: [review, audit, crosscheck]
sources: [docs/reviews/2026-08-20-internal-audit.md]
confidence: high
explored: false
verificationStatus: unverified
---

# Codex 2차 리뷰 — 갱신이 진짜로 고쳤는지

1차와 목적이 다르다. 저장소를 다시 훑는 것이 아니라, **`79b707b5` 가 실제로
고쳤는지, 고치면서 뭘 깨뜨렸는지**를 본다. 3,505줄이 바뀌었고 그중 상당수가
수치를 만드는 경로라, 수정이 새 결함을 심었을 위험이 1차보다 높다.

## 1. 먼저 동기화

Codex 채팅에 그대로:

```text
클로드 작업하고 왔어

git fetch origin
git merge --no-ff origin/claude/battery-charge-discharge-webapp-dq4ja3

머지 후 확인:
  git log --oneline -5
  git diff --stat 9a56358f..79b707b5 -- packages apps tools Makefile
```

`79b707b5 fix: 전수 감사 확정 65건 갱신` 이 보이면 준비된 것이다.

## 2. 리뷰 과제 (붙여넣기)

```text
79b707b5 의 갱신을 검증해줘. 저장소 전체를 다시 훑지 말고 이 커밋의 diff 에
집중해. 결과는 docs/reviews/2026-08-20-codex-review-round2.md 로 커밋해줘.

먼저 읽을 것:
- docs/reviews/2026-08-20-internal-audit.md — 각 항목의 "처리" 칸에 무엇을
  어떻게 고쳤는지, 어떤 회귀 테스트를 붙였는지 적혀 있다. 이번엔 봐도 된다.
- git diff 9a56358f..79b707b5 -- packages apps tools Makefile

검증할 것 (우선순위 순):

A. 수정이 결함을 실제로 닫았는가
   각 "처리" 항목에 대해, 원래 실패 시나리오를 새 코드로 다시 짚어봐라.
   특히 네가 1차에서 높음으로 올렸던 것들:
   - export.py 의 UnitCoulomb 우회 (#8): 이제 C 단위 파일과 Ah 단위 파일이
     같은 헤더 아래 다른 의미를 갖지 않는가?
   - cli.py 유지율 (#9): 기준 사이클 3 을 쓰는가, 없으면 뭐라고 하는가?
   - runs.py 재배정 3종 (#10 #11 #21): attach/detach/move/reparse 의 모든
     순열에서 cycle_number 가 유일하고 단조인가?
   - runs.py 원본 삭제 (#12): 정말로 원본을 지우는 경로가 사라졌는가?
   - bml PID kill (#13), CRLF 처방 (#14)
   - schedule.py C-rate (#7): 모호하면 None 인가, 아니면 다른 값을 짜내는가?

B. 수정이 새 결함을 심었는가 — 이쪽을 더 의심해라
   - cycles.py 의 taper 조건: taper 를 과대 추정해서 **정상 완료 사이클을
     incomplete 로 버리는** 반대 방향 오류가 생기지 않는가? 여러 taper 중
     최댓값을 쓰는데, 그게 맞는 선택인가?
   - composition.py 의 토큰 경계 매칭: 기존에 올바르게 인식되던 이름
     (NCM811, LPSCl, VGCF, Super P, PTFE, PVDF, LiPF6, SiOx...) 중 이제
     인식 못 하는 것이 생기지 않았는가? 인식 실패는 조용히 OTHER 가 되므로
     분모에서 빠진다 — 방향은 안전하지만 값은 여전히 틀린다.
   - knee.py 의 가속 검사: 진짜 knee 를 기각하는 경우가 늘지 않았는가?
     특히 완만한 2단 열화, 노이즈가 큰 셀.
   - analysis.py 의 reference_cycle_used/basis 필드 추가: 프론트가 이 필드를
     못 받는 옛 캐시/응답에서도 깨지지 않는가?
   - services.py 의 시각 처리: naive 로컬 비교로 바꿨는데, 서버와 계측기가
     다른 시간대일 때는 어떻게 되는가? 그게 이전보다 나은가?
   - bml 의 경로 경계 매칭: 정상 실행 형태를 하나라도 못 알아보게 되지
     않았는가? (bml serve / make serve / bml dev / worktree 실행)

C. 회귀 테스트가 진짜인가
   붙었다고 적힌 테스트가 실제로 결함을 잡는지 확인해라. 표본 5개 이상에서
   수정을 되돌리고 그 테스트만 돌려봐라. 통과해 버리면 그 테스트는 가짜다.
   반대로 과교정 방지용 대조군 테스트(수정 전후 모두 통과해야 하는 것)가
   실제로 그 역할을 하는지도 봐라.

D. 보류 18건 중 지금 고쳐야 할 것
   감사 보고서의 "보류한 항목" 표를 보고, 보류 이유가 타당하지 않은 것이
   있으면 지적해라. 특히 "파일 소유가 겹쳐서" 로 미룬 것들은 이제 그 제약이
   없다.

E. 아래 20건에 대한 독립 판단 (2차 갱신 대상)
   우리가 다음 라운드에서 고칠 목록이다. 각각에 대해 (1) 동의/이견,
   (2) 심각도, (3) 우선순위를 매겨줘. 이견이면 근거를 적어라.

   [표는 docs/reviews/codex-review-round2.md 의 "2차 갱신 대상" 절 참고]

보고 형식:

## 요약
갱신에 대한 총평. 닫힌 결함 / 안 닫힌 결함 / 새로 심어진 결함 수.

## 안 닫힌 것
| 원래 항목 | 왜 아직 열려 있는가 | 재현 |

## 새로 심어진 것
| 파일:줄 | 무엇이 깨졌나 | 실패 시나리오 | 어느 수정이 원인인가 |

## 가짜 회귀 테스트
| 테스트 | 왜 가짜인가 (수정을 되돌려도 통과함) |

## 보류 항목 재평가
동의하지 않는 보류가 있으면.

## 2차 갱신 대상 20건 판정
| # | 동의? | 심각도 | 우선순위 | 근거 |

## 이상 없음
검증했고 문제 없다고 판단한 수정들.
```

## 2차 갱신 대상

Codex 1차에서만 나온 8건과, Opus 재감사에서 새로 확정된 12건이다.

| 출처 | 심각도 | 위치 | 항목 |
|---|---|---|---|
| Codex #1 | 높음 | `normalize.py:102` | 활물질 비율을 모르면 전극 **전체**를 활물질로 계산 (ADR 0007 핵심 계약 위반) |
| Codex #3 | 높음 | `schemas.py:31` | 물리 입력값 범위·유한성 검증 없음 (음수 질량/wt%, reference_cycle=0) |
| Codex #15 | 중간 | `nrbf.py:388` `wrd.py:297` | 잘린 NRBF/마지막 행을 예외 없이 **정상**으로 수용 |
| Codex #17 | 중간 | `export.py:74` | 미완료 마지막 사이클 수치가 기본 CSV 에 포함 |
| Codex #23 | 중간 | `CompositionEditor.tsx:52` | "조성 지우기" 가 조성을 안 지움 |
| Codex #25 | 중간 | `analysis.py:505` | 불연속 사이클을 균등 간격으로 복원해 x축·knee 위치 왜곡 |
| Codex #26 | 중간 | `bml:501` | pull 후에도 기존 프로세스가 **이전 HEAD** 를 서비스 |
| Codex #31 | 낮음 | `.gitignore` | bootstrap 이 만드는 `.venv-codex` 가 ignore 안 됨 |
| Opus | medium | `apps/api/app/storage.py:47` | npz 캐시를 제자리에 덮어써서, 재작성 중 읽는 요청이 EOFError 로 500 을 받는다 |
| Opus | medium | `apps/api/app/routers/runs.py:108` | 업로드 부분 실패 핸들러가 파싱 결과를 그대로 커밋하고 renumber 를 건너뛰어, 되돌릴 수 없는 불일치 레코드를 남긴다 |
| Opus | medium | `apps/api/app/storage.py:38` | 원본 쓰기가 원자적이지 않아, 중단된 업로드가 남긴 잘린 .wrd 를 이후 어떤 재업로드로도 고칠 수 없다 |
| Opus | medium | `apps/api/app/routers/groups.py:53` | PATCH /api/groups/{id} 가 보내지 않은 필드를 기본값으로 지운다 — 그룹 라우터에 PATCH 테스트가 아예 없다 |
| Opus | medium | `apps/api/tests/test_exports.py:59` | 내보내기 테스트가 헤더·행수만 보고 값을 한 번도 검증하지 않는다 — mAh/g 헤더 아래 raw mAh 를 내보내도 통과 |
| Opus | medium | `apps/api/tests/test_runs.py:110` | '계측기가 아는 것을 다시 묻지 않는다' 경로가 CI 에서 0% 커버 — 이름이 그 기능인 테스트가 반대를 어서션한다 |
| Opus | medium | `apps/api/tests/test_analysis.py:68` | 미완료 사이클 배제는 /cycles 에만 테스트가 있고 profile·compare·dashboard·CSV·XLSX 5개 경로는 전부 무방비 |
| Opus | low | `apps/api/app/routers/samples.py:168` | delete_sample(delete_runs=true) 이 run 캐시를 지우지 않아 npz 고아 디렉터리가 무한 누적된다 |
| Opus | low | `apps/api/tests/test_analysis.py:51` | '기준 사이클은 완료된 사이클이어야 한다' 가드가 테스트로 고정돼 있지 않다 |
| Opus | low | `tools/wiki_lint.py:138` | index 등재 검사가 부분 문자열 포함 검사 (※ 이번 갱신에서 이미 고쳤다 — 중복 확인용) |
| Opus | low | `apps/web/src/lib/i18n.ts:90` | resolved_cell.notes.composition 이 어떤 번역 규칙에도 안 걸려 항상 영어로 표시된다 |
| Opus | low | `apps/web/src/lib/i18n.ts:111` | 집전체 차감 + 조성 없음 조합의 active_mass 노트가 CELL_NOTES 어느 패턴에도 안 맞는다 |

## 실측 파일이 있어야 답할 수 있는 것

1차에서 Codex 가 "확신 없음"으로 남긴 것 중 셋은 합성 픽스처로는 결론이 안 난다.
실측 `.wrd` 가 있으면 `WRDKIT_SAMPLE=/path/to.wrd` 를 걸고 확인해 달라.

- `cycles.py:161` — CC→CV 전환 행에서 두 Q 값이 같은가? 다르면 스텝 경계
  증가분이 빠지고 있다.
- `Plot.tsx:54` — 용량 plateau 에서 같은 x 가 실제로 중복되는가?
- `schedule.py:185` — `planned_cycles = max(loop_count)` 가 formation 을
  포함하는가? 아니면 health 가 1~2 사이클 일찍 finished 로 판정한다.

## 끝나면

Codex 리뷰가 커밋되면 Claude 세션에 "codex 2차 리뷰 나왔어" 라고 알린다.
그때 2차 갱신을 돌린다 — Codex 가 "새로 심어진 것" 으로 지목한 것을 **먼저**
고치고, 그 다음 20건 대상을 우선순위대로 처리한다.
