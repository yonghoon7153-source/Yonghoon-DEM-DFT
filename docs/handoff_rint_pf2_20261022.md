# Rint ② 사전 리뷰 2 회차 고침 — 새 세션 인계 (2026-10-22)

## 0. 한 줄
- 본 세션 (`claude/stoic-knuth-NObVQ`) 은 사용량 (1저자 10-22 *"지금 토큰이 2%정도 남아서"*) 때문에 여기서 멈춘다.
- 새 세션이 인계 브랜치에서 일을 이어받는다.  할 일 = 1저자 Q1 (게이트 → push) · Q2 (사전 리뷰 2 회차 고침).  1저자 10-22 *"q1하고 q2는 그럼 서브 브랜치/대시보드에서 하자"*.
- 단계마다 1저자 승인을 받고, 끝나면 stoic-knuth 로 **fast-forward** 병합 인계 문서를 쓴다.
- 충돌을 막는 규칙 셋: 본 세션 동결 · 새 세션은 인계 커밋 위에만 쌓기 · 병합은 ff 만 (§4).

## 1. 브랜치 기하 (10-22 01 UTC · 원격 SHA 는 `git ls-remote` 로 다시 확인)

| 브랜치 | 끝 | 뜻 |
|---|---|---|
| `claude/stoic-knuth-NObVQ` (원격) | `93d93bc02` | 게이트 155 ✓ · push 됨.  **병합이 돌아올 때까지 그대로** (본 세션 동결) |
| `claude/rint-pf2-handoff-20261022` (인계) | `93d93bc02` → `bf79d44c2` → 이 문서 커밋 | `bf79d44c2` = 사전 리뷰 2 회차 판정문 반입 · 수정 계획 §6 (결정 + 쉽게 말하면 상자 셋) · 진행 10-22 01 · CLAUDE.md 표지.  이 문서 커밋 = 이 문서 + `docs/handoff_rint_pf2_20261022/` |
| 새 세션 브랜치 | (플랫폼이 정함) | 처음에 인계 브랜치 끝으로 맞춘다 (§2) |
| `claude/wip-20261021/evac` (백업) | (`git ls-remote` 로 확인) | 멈춘 네 트랙의 스냅숏 + 이어받기 카드 (그 브랜치 안 폴더 evac_20261021 의 RESUME_paused 카드 · 10-21).  **이번 범위 밖 · 건드리지 않는다** |

- `bf79d44c2` 의 게이트는 본 세션에서 돌던 중이었다.  그 결과는 새 세션에서 볼 수 없다 → **새 세션 게이트가 정본**이다.

## 2. 시작 절차 (새 세션 · 그대로 실행)
1. `git fetch origin claude/rint-pf2-handoff-20261022 claude/stoic-knuth-NObVQ claude/friendly-meitner-lldvar`
   - 셋째 = litdb 정본 브랜치.  없으면 `scripts/check_doc_refs.py` 가 실패한다.
2. 자기 브랜치에 자기 커밋이 0 개인지 본다.  0 개면 `git reset --hard origin/claude/rint-pf2-handoff-20261022`.  커밋이 있으면 멈추고 보고한다.
3. 확인 셋 (하나라도 안 맞으면 멈추고 보고)
   - `git merge-base --is-ancestor origin/claude/stoic-knuth-NObVQ HEAD` = 참 (나중에 ff 가능).
   - `git log --oneline origin/claude/stoic-knuth-NObVQ..HEAD` = 2 커밋 (`bf79d44c2` + 이 문서 커밋).
   - 작업 트리 깨끗.
4. 파이썬 패키지 (numpy · scipy · flask · pyflakes) 확인.  없으면 설치한다.
5. 무거운 실행 잠금 = `docs/handoff_rint_pf2_20261022/heavy.sh` (칸 둘 · `HEAVY_LOCK_DIR` 로 잠금 자리 지정 · 기본 `${TMPDIR:-/tmp}/rint_heavy_locks`).
6. 읽을 것 (이 순서 · 다른 것은 필요할 때만)
   - 이 문서
   - 수정 계획 `docs/reviews/rint2_design_fix_plan_20261021.md` §6
   - 브리프 `docs/handoff_rint_pf2_20261022/pf2_fix_BRIEF.md`
   - 판정문 둘 `docs/reviews/rint2_prereview2_20261022/impl/REVIEW.md` · `docs/reviews/rint2_prereview2_20261022/design/REVIEW.md`

## 3. 할 일 — 단계마다 1저자 승인
1저자 10-22 원문: *"1,2,3,4,5 자동으로 하지말고 나한테 승인 받으면서 하자"* · *"1,2 넘어가기전에 나한테 알람주고"*.  ⇒ 단계를 시작하기 전에 승인을 받는다.  단계가 끝나면 알람 (푸시 알림) 을 주고, 다음 단계로 저절로 넘어가지 않는다.

| 단계 | 무엇 | 승인 |
|---|---|---|
| ① | 인계 판에서 전체 게이트 `bash scripts/check_all.sh` → "✓ 전부 통과" → **자기 브랜치에** push (stoic-knuth 아님) | 시작 전 승인 · 끝나면 알람 |
| ② | 고침 = 브리프 A–H.  Q1 (다) SV 괄호 판정 · Q2 ⑥ 숫자 탐침을 단계 2 앞으로 + 계획 해시 대조 · Q3 시간 문장 · 같은 판 지문 대조 · 작은 것 · 문서 + 웹앱 하이라이트 · 원장 · 회귀.  시험 먼저 · 커밋 하나씩 · 등록이 정하지 않은 자리는 고르지 말고 묻는다 | 시작 전 승인 · 묶음마다 알람 |
| ③ | 짧은 독립 재확인 (고친 사람 설명 없이 · 판정문 탐침 재실행 + 고친 자리 새 반례) → 게이트 → 자기 브랜치 push | 승인 |
| ④ | stoic-knuth 로 ff 병합 인계 문서 (꼴 = `docs/handoff_merge_to_stoic_knuth_20261020.md` §0–§7 · 붙여 넣을 프롬프트 포함) | 승인 |
| ⑤ | (1저자) 금 10-23 kgy 재압밀 → S0 단계 1 (SBE 기하 · σ 안 엶) → ⑥ 숫자 탐침 (SBE · σ 봉인) → Codex 재검토 요청 ≈ 10-24 | 1저자 |

- **WIP 패치** `docs/handoff_rint_pf2_20261022/pf2_wip_carbon_junction.patch` (+197 / −39 · `scripts/carbon_junction.py`)
  - 본 세션 고침 에이전트가 멈출 때까지 쓴 생산자 쪽 초안 (브리프 A 의 1) 이다.
  - 시험 없이 쓴 것이다 → **참고용**.  시험 먼저 원칙대로 시험부터 다시 쓰고, 패치에서는 쓸 만한 것만 가져온다.
  - `pf2_wip_probe_circuits.py` = 같은 에이전트의 탐침 초안 (참고용).
- 사용량 아끼기: 에이전트는 하나씩 · 리뷰 · 고침 보고는 짧게 · 큰 파일은 필요한 함수만 읽는다.

## 4. 병합 — 충돌 막기
- **본 세션 = 동결.**  병합이 돌아올 때까지 stoic-knuth 에 커밋 · push 하지 않는다.  멈춘 네 트랙도 그대로 둔다.
- **새 세션 = 인계 커밋 위에만 쌓는다.**  rebase · force-push · merge 커밋은 금지.  stoic-knuth 에 직접 push 하지 않는다 — 병합은 ④ 문서로 stoic-knuth 세션이 ff 로 한다.
- 공유 파일은 덧붙이기만 한다.  그러면 나중에 멈춘 트랙 (evac) 을 합칠 때도 충돌이 작다.
  - `CLAUDE.md`: Rint ② 줄 끝 표지 한 줄만.
  - `docs/session_20260923_progress.md`: 끝에 줄 덧붙이기만.
  - `docs/reviews/findings.json`: 브리프 G 의 RCA-06 메모만 (다른 항목은 손대지 않는다).
- 병합 때 확인 (④ 문서에 넣는다): `git merge-base --is-ancestor origin/claude/stoic-knuth-NObVQ <새 브랜치 끝>` = 참 → `git merge --ff-only` → 게이트 → push.

## 5. 지금 상태 (10-22 01 UTC · 날짜를 보고 읽을 것)
- 사전 리뷰 2 회차 (기반 `93d93bc02`)
  - 구현 쪽 = 고친 뒤 발송 · 새 P1 1 · P3 3.
  - 설계 · 등록 쪽 = 고친 뒤 발송 · 새 P2 3 · P3 7.
  - 판정문 · 탐침 = `docs/reviews/rint2_prereview2_20261022/`.
- 1저자 결정 = 수정 계획 §6.  Q1 (다) · Q2 · Q3 비준 (10-22 *"이러한 부분 잘 이해못하니까 잘 하이라이트로 저장해두고 권고대로 해줘"*) · Q3-b (추가 GPU 기계) 미답.
  - ★ 1저자가 이해하기 어려워한 부분 = SV 괄호 판정 · 계획 봉인 순서 · 시간.  설명할 때는 수정 계획 §6 의 쉽게 말하면 상자 ① ② ③ 을 쓴다.
  - 핵심 한 줄: SV 비는 범위 [아래, 위] 로만 알고, 주 값 (DBE σ_e) 은 한 값 그대로다.
- 원장
  - RCA-01–10 · 12 · 13 = claimed_fixed · RCA-11 = open (S0 단계 1 뒤).
  - 사전 리뷰 결함 (PRE2-…) 은 원장 ID 없이 수정 계획에 기록한다 (1 회차와 같음) → 고칠 때 RCA-06 메모만 쓴다.
- 일정: 금 10-23 kgy 재압밀 → S0 단계 1 → ⑥ → Codex 요청 ≈ 10-24 · 기한 10-31.
  - Q3 결정: 주 판정이 10-31 에 안 끝나면 그날은 진행 보고만 하고, 등록 팔은 줄이지 않는다.
- 멈춘 트랙 (이번 범위 밖)
  - 언로딩 ULPR 수정 재확인
  - LHS214 S0b 고침
  - 믹서 D2 수정 재확인
  - 믹서 D3 설계 v3
  - 스냅숏 · 이어받기 카드 = evac 브랜치.

## 6. 지킬 것 (CLAUDE.md 가 정본)
- 보고 → 설명 → 비준 → 실행.  한국어 · 표 · `[트랙]` 머리.
- push 전에 전체 게이트 `scripts/check_all.sh` "✓ 전부 통과" (줄이지 않는다).  그 전에 `check_doc_refs` · `check_review_findings` 를 먼저 돌린다.
- 봉인 32 파일 (`scripts/run_network_194_parallel.py` CODE_FILES) 은 손대지 않는다 (214 발사 전).
- 숫자 · 전칭은 실행 출력으로만 (SELF-124).  문서에 작업 트리 전용 SHA 를 쓰지 않는다 (SELF-116).
- 웹앱은 :5002 만 쓴다 · 5001 은 건드리지 않는다.  kgy · ibb 주소 · IP 는 리포에 쓰지 않는다.
- Codex 요청 전 사전 공격 리뷰 (규칙 ③).  Codex GO 아래로 기준을 낮추는 안은 내지 않는다.

## 7. 붙여 넣을 프롬프트 (새 세션에)

```text
Rint ② 사전 리뷰 2 회차 고침을 이어받아줘. 본 세션(claude/stoic-knuth-NObVQ)은 사용량 때문에 멈췄고, 이 세션이 인계를 받는다.
먼저 인계 문서를 읽어 (10-22):
  git fetch origin claude/rint-pf2-handoff-20261022 && git show FETCH_HEAD:docs/handoff_rint_pf2_20261022.md
1. 문서 §2 대로 시작해: 네 브랜치에 커밋이 없으면 인계 브랜치 끝으로 reset · litdb 정본 브랜치(claude/friendly-meitner-lldvar) fetch · 확인 셋 · 패키지. 하나라도 안 맞으면 멈추고 보고.
2. §3 단계 ①–④ 를 하나씩 해. 각 단계를 시작하기 전에 나한테 승인받고, 끝나면 알람(푸시 알림)을 줘. 저절로 다음 단계로 넘어가지 마.
   ① 전체 게이트(scripts/check_all.sh · "✓ 전부 통과") → 네 브랜치에 push.
   ② 브리프(docs/handoff_rint_pf2_20261022/pf2_fix_BRIEF.md) A–H 고침 · 시험 먼저 · 커밋 하나씩 · 등록이 정하지 않은 자리는 고르지 말고 나한테 물어봐. WIP 패치는 참고용.
   ③ 짧은 독립 재확인 → 게이트 → push.
   ④ stoic-knuth 로 fast-forward 병합 인계 문서(docs/handoff_merge_to_stoic_knuth_20261020.md 꼴 · 붙여 넣을 프롬프트 포함).
3. 충돌 막기(§4): stoic-knuth 에 직접 push 하지 마 · rebase · force-push · merge 커밋 금지 · 공유 파일(CLAUDE.md · 진행 기록 · 원장)은 덧붙이기만.
4. 내가 헷갈려한 부분(SV 괄호 판정 · 계획 봉인 순서 · 시간)은 수정 계획 §6 의 쉽게 말하면 상자로 설명해줘.
5. 사용량 아끼기: 에이전트는 하나씩 · 보고는 짧게.
보고 → 설명 → 비준 → 실행. 결과는 [Rint] 머리 · 표로 담백하게.
```

## 8. 돌아올 때 (stoic-knuth 세션에)
- 새 세션이 ④ 에서 쓴 병합 인계 문서의 §7 프롬프트를 stoic-knuth 세션에 붙여 넣는다.
- 그 세션이 ff 병합 → 검사 → 게이트 → push 를 한다.
- 그 뒤 멈춘 네 트랙은 evac 브랜치의 이어받기 카드로 하나씩 다시 연다 (1저자 승인 뒤).
