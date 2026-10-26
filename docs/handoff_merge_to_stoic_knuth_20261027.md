# 인계 — 연장 세션 `claude/sdcp-dem-manuscript-si-pqwtv8` → 본 세션 `claude/stoic-knuth-NObVQ` 복귀 병합 + Codex 가지 통합 (2026-10-27)

> **근거 (1저자 원문)**: 10-27 *"이제 원래 메인브랜치 토큰 복귀됐어 관련해서 충돌되지 않게 예전처럼 프롬프트 주고 codex에서도 이제 같이 머지해야되니까 준비해야된다고도 같이 알려줘야돼"* · 10-26 *"claude 인계건은 메인브랜치에서 하고 너는 Rint랑 50kg에 집중하자"*.
> 이 문서는 pqwtv8 가지에만 있다 — 본 세션은 `git show FETCH_HEAD:docs/handoff_merge_to_stoic_knuth_20261027.md` 로 읽는다 (§9).

## 0. 한 줄

세 단계를 차례로 — 동시에 두 가지가 자라지 않게 한다.

| 단계 | 누가 | 무엇 |
|---|---|---|
| **A** | 본 세션 | stoic ← pqwtv8 **fast-forward** (§2 · §3) |
| **B** | 본 세션 | Codex 가지 통합 = stoic 위에 `cherry-pick -x` — **Codex 의 통합 계획 쪽지가 온 뒤에만** (§6) |
| **C** | 연장 세션 (이쪽) | pqwtv8 을 새 stoic 끝으로 fast-forward → Rint · 50kg 이어서 (§5) |

이쪽 (pqwtv8) 은 **이 문서를 담은 커밋 뒤로 커밋 · push 를 멈춘다** (§5) — 그래야 A · B 뒤에도 C 가 fast-forward 로 된다.

## 1. 브랜치 기하 (10-27 02:35 KST · 원격 SHA 는 `git ls-remote` 로 다시 확인)

| 가지 | 끝 | 관계 |
|---|---|---|
| `claude/stoic-knuth-NObVQ` | `93d93bc02` (10-22 01:31 KST) | pqwtv8 의 조상 — fast-forward 가능 · 뒤처짐 0 |
| `claude/sdcp-dem-manuscript-si-pqwtv8` | 이 문서를 담은 커밋 | stoic 보다 **118 커밋** 앞 (이 문서 커밋 포함 · 10-22 ~ 10-27 KST) |
| `codex/*` 17 개 | — | **전부 기준 `7799a2ff6`** (pqwtv8 · 10-23 18:43 KST · 묶음 A′ 병합) · pqwtv8 에 들어온 Codex 커밋 = **0** (조상 아님 · `git cherry` 패치 같은 것 0) |

**Codex 가지 구조** (이쪽 10-27 계산 — 확정은 Codex 통합 계획 쪽지):
- 주 사슬 18 커밋 (끝 `codex/p1-preflight-complete`) — 가지 12 개가 이 사슬의 앞부분이다: `dem-gen2-request` (4) ⊂ `dem-gen2-t12` (7) ⊂ `ulpri-closure` (8) ⊂ `dem-gen2-t12r` (10) ⊂ `t12r01-closure` (11) ⊂ `nonrint-claude-query` (12) ⊂ `nonrint-facts-reply` (13) ⊂ `nonrint-handoff` (14) ⊂ `p1-input-identity` (15) ⊂ `p1-readiness` (16) ⊂ `p1-staging-plan` (17) ⊂ `p1-preflight-complete` (18).
- 사슬 밖 4 갈래 (모두 `7799a2ff6` 에서 따로): `lhs214-relaunch` 4 · `mixer-d3-design` 4 · `mixer-mxd2` 4 · `unloading-ulpri` 6 (`unloading-ulpr` 4 를 담는다).
- 고유 커밋 = 18 + 4 + 4 + 4 + 6 = **36** · 바뀐 파일 합집합 **3,271** (주 사슬 615 · `lhs214-relaunch` 135 · `mixer-d3-design` 327 · `mixer-mxd2` 559 · `unloading-ulpri` 1,688 — 대부분 증거 폴더).
- **충돌 후보**: 우리 쪽 (`7799a2ff6`..이 문서 앞 커밋 = 600 파일) ∩ Codex (3,271 파일) = **0 파일** · Codex 끼리 = 주 사슬 ∩ `unloading-ulpri` = **53 파일** (ULPR · ULPRI 요청서 2 · 판정 폴더 8 · 증거 43) — **두 쪽 blob 이 53/53 같다** → 같은 내용의 추가라 내용 충돌은 없을 것으로 본다 (추정 · 확인 = Codex 시험 cherry-pick) · 넣는 순서는 Codex 가 정한다.  갈래 셋 (`lhs214-relaunch` · `mixer-d3-design` · `mixer-mxd2`) 은 다른 어느 가지와도 파일이 겹치지 않는다.
- Codex 커밋 중 다른 Codex 커밋 SHA 에 묶인 자리 (예: 주 사슬의 *"Repin T12 consumer contract to published ULPRI"*) — cherry-pick 뒤 새 SHA 가 생긴다.  `codex/*` 가지가 원격에 남아 있으면 옛 SHA 인용은 `check_doc_refs` 기준 (`rev-list --remotes HEAD`) 으로 계속 도달 가능하다 → 다시 묶어야 하는 자리 (계약이 "HEAD 의 조상" 을 요구하는 곳 등) 가 있는지는 Codex 가 목록으로 준다.
- Codex 커밋은 공유 기록 (`CLAUDE.md` · 진행 기록 · `docs/reviews/findings.json` · `docs/reviews/claims.json` · `docs/reviews/doc_refs_allowlist.tsv`) 을 건드리지 않았다 (파일 이름 대조) — 그 줄들은 Codex 쪽지의 조각으로 받아 본 세션이 덧붙인다.

## 2. 단계 A — 병합 절차 (본 세션이 그대로 실행)

```bash
# ⓪ 아무것도 커밋하기 전에 — 작업 트리 · 로컬 커밋이 깨끗한가
git status --short                                          # 비어야 한다
git fetch origin claude/stoic-knuth-NObVQ && S=$(git rev-parse FETCH_HEAD)
git log --oneline "$S"..HEAD                                # 비어야 한다 (푸시 안 된 로컬 커밋 0)

# ① 기하 — 브랜치별 fetch 를 한 번에 하나씩 (FETCH_HEAD 가 덮인다)
git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && P=$(git rev-parse FETCH_HEAD)
git merge-base --is-ancestor "$S" "$P"   && echo FF_OK       # 원격 stoic ⊂ pqwtv8
git merge-base --is-ancestor HEAD "$P"   && echo LOCAL_FF_OK # 로컬 HEAD ⊂ pqwtv8
git cat-file -e "$P":docs/handoff_merge_to_stoic_knuth_20261027.md && echo DOC_OK
git diff --stat "$S" "$P" -- litdb/ | tail -1               # 비어야 한다
git rev-parse --is-shallow-repository                       # false 여야 한다
git fetch origin claude/friendly-meitner-lldvar             # litdb 정본 ref (check_doc_refs · litdb_sync 가 쓴다)

# ② 병합 = fast-forward 만
git checkout claude/stoic-knuth-NObVQ
git merge --ff-only "$P"

# ③ 검사 (§3) → ④ 푸시
bash scripts/setup_kgy_py38.sh                              # 게이트의 kgy 판 단계 (10-24) — 컨테이너마다 한 번
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 bash scripts/check_all.sh; echo "EXIT=$?"   # 파이프로 받지 말 것 (SELF-29)
git push -u origin claude/stoic-knuth-NObVQ                 # 네트워크 오류면 2 · 4 · 8 · 16 s 간격으로 재시도
```

**FF_OK · LOCAL_FF_OK · DOC_OK 중 하나라도 안 나오면 멈추고 보고한다** (rebase · force-push · merge 커밋을 추측으로 만들지 않는다).

## 3. 병합 뒤 검사

| 검사 | 명령 | 기대 |
|---|---|---|
| 전수 게이트 | `bash scripts/check_all.sh` (위 스레드 환경변수) | `✓ 전부 통과` · `EXIT=0` (이쪽 10-27 마지막 게이트 = 157 개 · 실패 0) |
| 원장 | `python3 scripts/check_review_findings.py` | `원장 자기일관 ✓` (805 → **839** 항목 · claimed_fixed 321 · verified 228 · open 281 · wontfix 9) |
| 인용 금지 스윕 | `python3 scripts/check_review_findings.py --ban-sweep` | 누수 없음 |
| 문서 참조 | `python3 scripts/check_doc_refs.py --quiet` | `✓ 깨진 참조 없음` (litdb 정본 ref 가 있어야 한다 — ① 끝 줄) |
| 증거 바이트 | `git status --short` (체크아웃 직후) | 비어 있음 (원본 `.mpr` · 증거 폴더는 바이트 그대로 — CRLF · 정규화 커밋 금지) |

## 4. 무엇이 넘어가나 (pqwtv8 10-22 ~ 10-27 · KST)

| 묶음 | 내용 | 정본 |
|---|---|---|
| Rint ② 사전 리뷰 2 회차 · 수정 A–F (10-22) | SV 괄호 판정 · 계획 해시 · 같은 코드 지문 · 결정 30 | `docs/reviews/rint2_pf2_fix_evidence_20261022/stage2_report.md` |
| Codex 재검토 반입 · 수정 계획 Q1–Q8 · 묶음 A · A′ · A″ (10-22 ~ 23) | RCA2-01 · 04 · 06 · 08 · 09 · 사전 공격 리뷰 · C1–C5 | `docs/reviews/rint2_rr_fix_evidence_20261023/` |
| 재압밀 VGCF 100 GPa (kgy · 10-23) | 결과 전 기대 전부 일치 | `docs/data/rint2_recompaction_vgcf100_20261023/README.md` |
| Python 3.8 호환 · CPU CG (10-24) | `SELF-132` · `133` · 게이트 kgy 판 단계 | `scripts/check_kgy_py38.sh` |
| Q9 설계 개정 2–5 · 사전 공격 리뷰 3 · 4 회차 (10-23 ~ 26) | 예측 12 단위 · 시간표 | `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` |
| Codex 회차 ① 요청 · 판정 반입 · 수정 계획 Q1–Q7 · 묶음 B · B″ (10-24 ~ 26) | RR1-01 · 02 · RCA2-02 · 03 · 조립만 경로 · 시험 판독기 보강 | `docs/reviews/codex_review_rint2_rr_round1_20261026.md` · `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_B2.md` |
| 50kg (10-26) | 7 쪽 계획 · 덱 생성기 · Codex 덱 리뷰 (HOLD) · v2 덱 · 재개 도구 고침 (KG50-02 · 10) | `docs/50kg/kg50_fix_plan_20261026.md` · `docs/data/kg50_decks_20261026_v2/README.md` |
| P1 7:3 입력 신원 (10-26) | ibb 원본 여섯 = 10-09 크기 · 해시 그대로 | `docs/reviews/p1_ps73_input_identity_20261026/README.md` |
| 이종기술 ① SE 펠릿 EIS (10-26 · 27) | 소립 · 대립 각 2 · 절편 R · 0.1 g · ⌀10 mm | `docs/data/se_pellet_eis_20261026/README.md` |
| 주간 보고 10-19 ~ 25 | — | `docs/worklog/weekly_20261025.md` |

## 5. 이쪽 (pqwtv8) — 넘기는 동안 멈춤 (충돌 방지)

- 이 문서를 담은 커밋 뒤로 pqwtv8 에 **커밋 · push 를 하지 않는다**.  그동안 기계 런 (hit D3 여섯 · ibb D0.7 재개 시험 · ibb D3 s1) 은 그대로 돈다 — 리포 push 와 무관.  결과 판독 · 1저자 질문 답은 계속 (커밋 없이).
- 단계 A · B 가 끝나 본 세션이 stoic 을 push 하면 1저자가 이쪽에 알린다 → 이쪽 (단계 C):
  ```bash
  git fetch origin claude/stoic-knuth-NObVQ
  git merge-base --is-ancestor HEAD origin/claude/stoic-knuth-NObVQ && echo C_FF_OK   # pqwtv8 끝 ⊂ 새 stoic
  git merge --ff-only origin/claude/stoic-knuth-NObVQ && git push -u origin claude/sdcp-dem-manuscript-si-pqwtv8
  ```
  → 병합 커밋 없이 pqwtv8 = 새 stoic 끝 → Rint · 50kg 를 이어간다 · 다음 인계도 같은 fast-forward.
- ⛔ 단계 C 는 **A · B 가 둘 다 끝난 뒤에만** 한다.  A 만 끝난 뒤 이쪽이 커밋을 다시 시작하면 stoic (B 의 cherry-pick) 과 pqwtv8 이 따로 자라 fast-forward 가 깨진다 (병합 커밋 · rebase · force-push 금지라 되돌릴 길이 없다).  그래서 B 를 짧게 한다 (§6 — 한 묶음) · B 는 본 세션 몫 (1저자 10-26).
- 동결 시간 (추정) = A (게이트 한 번) ‖ Codex 쪽지 준비 → B (cherry-pick 한 묶음 + 게이트 한 번) ≈ 반나절 안.  그동안 꼭 먼저 커밋해야 하는 결과 전 등록 (예: 50kg D0.7 압축 전 Q5 dt · 감쇠 등록) 이 생기면 압축 발사를 동결 뒤로 미룬다 (1저자 판단).

## 6. 단계 B — Codex 가지 통합 (본 세션)

- **Codex 통합 계획 쪽지가 온 뒤에만** 시작한다 — 가지 `codex/merge-prep` 의 `docs/collab/codex_to_claude/` 에 새 쪽지 (`YYYYMMDD-HHMM_merge-plan.md`).  쪽지에 들어올 것 = 넣을 가지 · 커밋 순서 · 의존 · 53 파일 (두 쪽 같은 내용) 을 어느 커밋으로 넣을지 · 다시 묶을 SHA 자리 · 공유 기록 조각 · 원장 JSON 조각 · 새 기준 위 시험 cherry-pick 결과 (Codex 쪽 프롬프트 §10).
- 단계 A push 뒤 단계 B 가 끝날 때까지 **stoic 에도 다른 커밋을 올리지 않는다** — Codex 의 시험 cherry-pick 기준 (= 이 문서 커밋) 과 실제 기준이 같아야 쪽지의 충돌 판정이 그대로 맞는다.
- 시작 전에 Codex 가지를 원격 추적 ref 로 받아 둔다: `git fetch origin '+refs/heads/codex/*:refs/remotes/origin/codex/*'` — Codex 문서가 인용하는 옛 SHA 는 이 ref 들로 도달 가능해야 `check_doc_refs` 가 통과한다.
- 방법 = stoic 위에 쪽지 순서대로 `git cherry-pick -x` (Codex 원 SHA 는 커밋 메시지의 `cherry picked from` 줄).  **병합 커밋 · rebase · force-push · GitHub PR 병합 버튼 금지** (`docs/handoff_codex_nonrint_20261023.md` §1).  `codex/*` 가지는 지우지 않는다 (요청서 · 쪽지가 그 SHA 를 인용한다).
- 쪽지 순서대로 **전부 cherry-pick 한 뒤 전체 게이트 한 번 → push** (연장 세션의 동결 시간을 줄인다 · 게이트는 줄이지 않는다 — CLAUDE.md 10-21 *"커밋을 묶어 횟수를 줄이고"*).  게이트가 실패하면 push 하지 않고 멈추고 보고한다.  공유 기록 줄 = Codex 조각을 본 세션이 덧붙인다 (같은 묶음의 마지막 커밋) · 원장 조각 = `check_review_findings.py` 통과.  Codex 원 SHA 를 인용하는 문서는 그대로 둔다 (`codex/*` 가지가 원격에 남아 도달 가능) — 고치는 것은 Codex 쪽지의 "다시 묶을 자리" 목록뿐이다.
- **충돌이 나면 멈추고 보고한다** — 추측으로 고르지 않는다 (정본은 Codex 쪽지).  우리 쪽 파일과는 겹침이 0 이라 충돌은 Codex 끼리 (53 파일 · blob 같음) 에서만 날 수 있고, 같은 내용이라 나지 않을 것으로 본다 (추정 — Codex 시험 cherry-pick 이 확인한다).
- 쪽지 커밋 자체 (`codex/merge-prep`) 도 마지막에 cherry-pick 한다 (쪽지는 cherry-pick 으로 이 가지에 들어온다 — `docs/collab/README.md`).
- 끝나면 새 SHA 표 쪽지 = `docs/collab/claude_to_codex/` 에 `YYYYMMDD-HHMM_sha-map.md` (Codex SHA → stoic SHA) · Codex 의 새 일은 새 stoic 끝에서 새 가지로.

## 7. 넘어간 뒤 상태 (10-27 02:35 KST — 날짜를 보고 읽을 것)

| 트랙 | 상태 | 다음 (맡는 쪽) |
|---|---|---|
| Rint ② | Codex 회차 ① = HOLD (새 P1 없음) · 수정 묶음 B · B″ 반입 (게이트 157 · 0) | 묶음 C (Q4 재시도 봉인 · Q9 구현 · 시간표) → Codex 회차 ② (위조 한정 질문 포함) · 웹앱 SV 문구 = 다음 웹앱 묶음 · kgy `free -g` 1저자 (연장 세션 · 단계 C 뒤) |
| 50kg | hit D3 칸 비교 여섯 (b40 · b50 × 시드 3) = 삽입 검사 통과 · 압축 진행 (마지막 확인 10-26 밤) · ibb D0.7-40 삽입 완주 (job 323818 · 원자 2 개 잃음 — thermo 줄 기준 step 9,000 · 16,000 에서 하나씩 줄어 보임 · 체크포인트 20,001 전) → 재개 시험 `-T` NP 56 (1저자 발사 · 결과 대기) · ibb D3-40 s1 (job 323925 · hit 와 빌드 교차) 압축 중 | Q5 dt · 감쇠 등록 문서 (D0.7 압축 전 · 잃은 원자 수 = 관측량 후보) · Codex 짧은 재확인 (v2 덱 · 재개 도구) · 판정 모드 (Hertz 권고 · 1저자) (연장 세션) |
| 이종기술 실험 | SE 펠릿 EIS 4 판독 (절편 R 소립 38.9 · 41.8 · 대립 25.4 · 27.7 Ω) · 두께 측정 대기 | 실험 계획 Q1–Q3 (질량 시리즈 · 몰드 안 측정 · 압력 시리즈) 1저자 (연장 세션) |
| Codex 비 Rint 트랙 | 가지 17 · 고유 커밋 36 · 통합 0 | 통합 계획 쪽지 (Codex) → 단계 B (본 세션) |

## 8. 지킬 것 (CLAUDE.md 가 정본)

- **보고 → 설명 → 비준 → 실행.**  1저자에게는 게이트 · 커밋 얘기 없이 결과만.  각 단계를 시작하기 전에 승인 · 끝나면 알림.
- 커밋 하나 → 게이트 (`check_all.sh` "✓ 전부 통과") → 바로 push · 게이트 도는 동안 작업 트리를 건드리지 않는다 · PR 만들지 않는다 · 봉인 32 파일 (`code_fp e8b2496b…`) 수정 금지 · 게이트를 줄이는 안 금지.
- 받은 ZIP · 원자료는 새 빈 폴더에서 `python3 -I` 로 읽기만 · 서지 · 값은 litdb 정본 카드에서만 · 커밋 · 코드 주석에 모델 식별자 금지 · ibb · hit 주소 · 포트는 리포에 쓰지 않는다.

## 9. 붙여 넣을 프롬프트 — 본 세션 (`claude/stoic-knuth-NObVQ`)

```text
연장 세션 브랜치(claude/sdcp-dem-manuscript-si-pqwtv8)를 이 브랜치(claude/stoic-knuth-NObVQ)로 fast-forward 병합하고, 그다음 Codex 가지들을 통합해줘.
인계 문서는 pqwtv8 쪽에만 있으니 먼저 읽어 (10-27):
  git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && git show FETCH_HEAD:docs/handoff_merge_to_stoic_knuth_20261027.md
1. (단계 A) 아무것도 커밋하지 말고 §2 를 그대로 해: 작업 트리 깨끗 · 로컬 커밋 0 → FF_OK · LOCAL_FF_OK · DOC_OK · litdb 비어 있음 · shallow false · litdb 정본 ref fetch → git merge --ff-only.
   하나라도 안 나오면 rebase · force-push · merge 커밋을 만들지 말고 멈추고 보고해.
2. §3 검사 (setup_kgy_py38 → check_all "✓ 전부 통과" · 원장 839 · ban-sweep · 문서 참조 · 증거 바이트) → claude/stoic-knuth-NObVQ 로 푸시 → 나한테 알려줘.
3. (단계 B) Codex 가지 통합은 Codex 의 통합 계획 쪽지 (가지 codex/merge-prep · docs/collab/codex_to_claude/ 의 새 merge-plan 쪽지) 가 올라온 뒤에만 — 내가 "올렸다" 고 하면 시작.
   쪽지 순서대로 전부 cherry-pick -x (쪽지 커밋 자체도 마지막에) → 전체 게이트 한 번 → push (연장 세션이 그동안 커밋을 멈추고 기다리니 한 묶음으로) · 충돌이나 게이트 실패가 나면 추측으로 고르지 말고 멈추고 보고 · 끝나면 새 SHA 표 쪽지를 claude_to_codex 에.
   단계 A 뒤 B 가 끝날 때까지 이 브랜치에 다른 커밋을 올리지 마 (Codex 시험 cherry-pick 의 기준과 같아야 한다).
   병합 커밋 · rebase · force-push · PR 병합 버튼 금지 · codex/* 가지는 지우지 마.
4. 단계 A · B 가 끝나면 나한테 알려줘 — 연장 세션이 pqwtv8 을 새 끝으로 fast-forward 해서 Rint · 50kg 을 이어간다 (§5).  Rint · 50kg · 이종기술 실험은 연장 세션이 계속 맡는다.
각 단계를 시작하기 전에 나한테 승인받고 끝나면 알려줘.  보고 → 설명 → 비준 → 실행.  게이트 · 커밋 얘기는 빼고 결과만 담백하게.
```

## 10. 붙여 넣을 프롬프트 — Codex 작업 창

```text
Claude 본 세션(claude/stoic-knuth-NObVQ)이 곧 연장 세션 가지(claude/sdcp-dem-manuscript-si-pqwtv8)를 fast-forward 로 받고, 이어서 네 codex/* 가지들을 cherry-pick 으로 통합한다.  통합 준비를 해줘.
먼저 읽을 것 (pqwtv8 가지):
  git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8
  git show FETCH_HEAD:docs/handoff_merge_to_stoic_knuth_20261027.md      # §1 가지 구조 · §6 통합 방식
  git show FETCH_HEAD:docs/collab/claude_to_codex/20261026-1735_merge-prep.md
할 일 (읽기 · 계산 · 쪽지만 — 발사 · 발송 · 기계 실행 없음):
1. 통합할 가지 · 커밋 목록과 순서 (주 사슬 18 + lhs214-relaunch · mixer-d3-design · mixer-mxd2 · unloading-ulpri 갈래) · 의존 관계 · 이미 낡아 넣지 말아야 할 커밋이 있으면 그 이유.
2. 주 사슬과 unloading-ulpri 가 함께 담은 53 파일 (ULPR · ULPRI 요청서 · 판정 · 증거 — 이쪽 계산으로는 두 쪽 blob 53/53 같음) 을 어느 커밋으로 넣을지 · 내용이 다른 파일이 있으면 정본.
3. 다른 Codex 커밋 SHA 에 묶인 자리 (요청서 리뷰 핀 · "Repin T12 … published ULPRI" 같은 계약) 목록 — cherry-pick 뒤 새 SHA 가 생기니, 옛 SHA 그대로 둬도 되는 자리 (codex/* 가지가 남아 도달 가능) 와 다시 묶어야 하는 자리 (예: HEAD 의 조상이어야 하는 계약) 를 나눠서.
4. 공유 기록 (CLAUDE.md · 진행 기록 · findings.json · claims.json · doc_refs_allowlist.tsv) 에 넣을 줄 · 원장 JSON 조각 (본 세션이 덧붙인다).
5. 새 기준 = origin/claude/sdcp-dem-manuscript-si-pqwtv8 끝 (= fast-forward 뒤 stoic) 위에서 1 의 순서대로 시험 cherry-pick 을 로컬에서 해 보고 충돌 여부 · 그 파일을 적어 (시험 가지는 push 하지 마).
6. 할 수 있으면 그 시험 트리에서 bash scripts/check_all.sh 도 돌려 결과를 적어 (실패하면 어느 단계 · 무슨 메시지인지) — 본 세션의 한 묶음 게이트가 실패하면 연장 세션의 동결이 길어진다.
→ 새 가지 codex/merge-prep 를 그 기준에서 만들고 docs/collab/codex_to_claude/<UTC 시각>_merge-plan.md 하나만 커밋해 push.  쪽지 안에 네 커밋 SHA 대신 <<sha:커밋 제목 앞 낱말>> 자리 표시 (docs/collab/README.md 규칙) — 제목이 비슷한 커밋이 있으니 (예: "Record verified full gate for …" 둘) 가를 만큼 낱말을 넣고, 가지 위치 (예: codex/p1-preflight-complete~17) 도 같이 적어 (통합 동안 가지가 얼어 있어 위치가 변하지 않는다).
통합이 끝날 때까지 기존 codex/* 가지에 새 커밋을 올리지 말고 (새 일은 새 가지 · 통합 뒤 새 stoic 끝에서), 가지는 지우지 마.  claude/* 가지에는 push 하지 마.
결과는 용훈 포메이션으로 나한테 보고해 줘.
```
