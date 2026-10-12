# 인계 — 연장 세션 `claude/sdcp-dem-manuscript-si-pqwtv8` → 본 세션 `claude/stoic-knuth-NObVQ` 복귀 병합 (2026-10-12)

**작성** 2026-10-12 KST · **작성 세션** 연장 세션 (pqwtv8 · 서브 세션)
**계기** 1저자 10-12 이어받기 메시지 — *"이 세션의 작업 브랜치가 claude/stoic-knuth-NObVQ 가 아니면, 그 브랜치를 origin/claude/stoic-knuth-NObVQ 에서 시작하고 끝날 때 fast-forward 병합 인계 문서를 남긴다"*
**앞선 인계 (같은 양식)** `docs/handoff_merge_to_stoic_knuth_20261006.md`

---

## 0. 한 줄

stoic-knuth 의 원격 헤드 `46cd0bdb8` (10-11 밤 · DEM 지배방정식 배경 보고서) 는 이 브랜치의 **조상**이고 (이 세션은 그 커밋으로 fast-forward 한 뒤에만 커밋했다) 저쪽이 앞선 커밋은 **0** 이다.
⇒ **fast-forward 이고 충돌이 원리적으로 없다.**  조건은 하나 — **병합 전에 stoic-knuth 에 아무것도 커밋하지 않는다.**

## 1. 브랜치 기하 (10-12 · 원격 SHA 는 `git ls-remote` 로 다시 확인)

| 브랜치 | 원격 SHA | merge-base | 이쪽이 앞선 | 저쪽이 앞선 | 병합 형태 |
|---|---|---|---:|---:|---|
| `claude/stoic-knuth-NObVQ` | `46cd0bdb8` | `46cd0bdb8` | 8 — 언로딩 재검토 반입 `23a8fa48f` · 세대 2 재검증 7 반입 `2e2d0a32b` · 이 문서 첫 판 (+ `G2RR7-01` claimed_fixed) `c7606f0b1` · 보충 20 지원 U1 · U2 `28492841f` · U3 `74a44aa12` · U3b `b9ee7ac97` · U4 `8c19276ca` · U5 + 이 문서 갱신 (이 커밋) | **0** | ✅ fast-forward |
| `claude/friendly-meitner-lldvar` (litdb 정본) | (적지 않는다) | — | — | — | 무관 — 이 세션은 `litdb/` 를 건드리지 않았다 |

이쪽 HEAD = **이 문서를 담은 커밋** (자기 SHA 는 적을 수 없다 — §2 의 `DOC_OK` 가 확인한다).
⚠ 이쪽에 커밋이 더 생기면 (예: 보충 20 지원 구현 · 언로딩 개정 2) 같은 프롬프트를 다시 붙이면 된다 — 단 그 사이 stoic-knuth 에 아무것도 커밋하지 않았을 때만.

## 2. 병합 절차 (저쪽 세션이 그대로 실행)

```bash
# ⓪ 아무것도 커밋하기 전에 — 작업 트리 · 로컬 커밋이 깨끗한가
git status --short                                          # 비어야 한다
git fetch origin claude/stoic-knuth-NObVQ && S=$(git rev-parse FETCH_HEAD)
git log --oneline "$S"..HEAD                                # 비어야 한다 (푸시 안 된 로컬 커밋 0)

# ① 기하 — 브랜치별 fetch 를 한 번에 하나씩 (FETCH_HEAD 가 덮인다)
git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && P=$(git rev-parse FETCH_HEAD)
git merge-base --is-ancestor "$S" "$P"   && echo FF_OK       # 원격 stoic ⊂ pqwtv8
git merge-base --is-ancestor HEAD "$P"   && echo LOCAL_FF_OK # 로컬 HEAD ⊂ pqwtv8
git cat-file -e "$P":docs/handoff_merge_to_stoic_knuth_20261012.md && echo DOC_OK
git diff --stat "$S" "$P" -- litdb/ | tail -1               # 비어야 한다
git rev-parse --is-shallow-repository                       # false 여야 한다

# ② 병합 = fast-forward 만
git checkout claude/stoic-knuth-NObVQ
git merge --ff-only "$P"

# ③ 검사 (§3) → ④ 푸시
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 bash scripts/check_all.sh; echo "EXIT=$?"   # 파이프로 받지 말 것 (SELF-29)
git push -u origin claude/stoic-knuth-NObVQ                 # 네트워크 오류면 2 · 4 · 8 · 16 s 간격으로 재시도
```

**FF_OK · LOCAL_FF_OK · DOC_OK 중 하나라도 안 나오면 멈추고 보고한다** (rebase · force-push · merge 커밋을 추측으로 만들지 않는다).  해법은 이쪽 (pqwtv8) 에서 stoic 의 새 커밋을 먼저 반입해 다시 fast-forward 로 만드는 것.

## 3. 병합 뒤 검사

| 검사 | 명령 | 기대 |
|---|---|---|
| 전수 게이트 | `bash scripts/check_all.sh` (위 스레드 환경변수) | `✓ 전부 통과` · `EXIT=0` (이쪽 HEAD 에서 10-12 통과) |
| 원장 | `python3 scripts/check_review_findings.py` | `원장 자기일관 ✓` (636 → **644** 항목 — `ULR1-01` ~ `05` · `SELF-105` · `G2RR7-01` · `SELF-106`) |
| 인용 금지 스윕 | `python3 scripts/check_review_findings.py --ban-sweep` | 누수 없음 |
| 문서 참조 | `python3 scripts/check_doc_refs.py --quiet` | `✓ 깨진 참조 없음` |
| 증거 바이트 | `git status --short` (체크아웃 직후) | 비어 있음 (`.gitattributes` = `docs/reviews/codex_*_evidence_*/**` `-text` · CRLF 로 보이면 로컬 `core.autocrlf` 문제 — 정규화 커밋 금지) |

## 4. 무엇이 넘어가나 (10-12)

| 줄기 | 산출 | 정본 |
|---|---|---|
| **Codex 세대 2 재검증 7 반입** (10-12 인계 작업 A) | 판정문 (바이트 그대로) · 증거 (slim 229 / 229 = 묶음 MANIFEST · 뺀 608 = `SLIM_EXCLUDED.tsv` · source 573 = 핀 `3cedd40a5` blob · parent 2 = `821f0e151` blob · baseline_r6 = 10-11 반입 · GitHub API 응답 넷 = git 으로 복원) · 우리 트리 재현 (묶음 재구성 → Codex `run_checks.py` 무변경 전부 rc 0 · 다시 읽기 자체시험 26 / 26 · 출력 113 판정값 차이 0 · `r7_contract` 우리 판 = Codex 와 같음 · 봉인 32 `code_fp e8b2496b…` 불변 · 인계 도구 `g2_network_reread.py` 지문 `248ee5c0…`) · 원장 `G2RR6-01` · `G2RR5-03` → **verified** (범위 = `verified_scope`) · 새 `G2RR7-01` (P3 · 요청서 문장 과장) → 정정 표지 → claimed_fixed · 1저자 10-12 순서 **(나)** 기록 | `docs/reviews/codex_review_gen2_network_reverify7_20261012.md` · `docs/reviews/codex_gen2_network_reverify7_evidence_20261012/_README_import.md` · `docs/reviews/g2rr6_fix_plan_20261011.md` 머리 |
| **Codex 언로딩 개정 1 재검토 반입** | 판정문 (바이트 그대로) · 증거 (묶음 154 / 154 · source 97 = 핀 `3409814a3` blob · upstream 27 = 10-11 반입과 같음) · 우리 트리 재확인 (Codex 탐침 무변경 재실행 JSON 같음 · 우리 식 인용 등록 줄 34 / 34 · 산술 전부 같음) · 원장 `UL-01` ~ `UL-10` 노트 (open 유지) · 새 `ULR1-01` · `ULR1-02` (P1) · `ULR1-03` · `ULR1-04` · `ULR1-05` (P2) · `SELF-105` · 반영 계획 (⬜ 1저자 Q1–Q4) | `docs/reviews/codex_review_dem_unloading_prereg_rereview_20261012.md` · `docs/reviews/codex_dem_unloading_prereg_rereview_evidence_20261012/_README_import.md` · `docs/reviews/dem_unloading_ulr1_fix_plan_20261012.md` |

| **보충 20 지원 (U1–U5)** (1저자 (나) · Q4 (가) lhss · Q5 (가) · Q6 (가) 하중 열) | 실행기 등록 집합 supp20 · 관측 필수 (130/130) · 다시 읽기 `--expect-set supp20` (30) · lhss 설계 어댑터 + 본 하중 열 (27/27 · `docs/data/lhss_design_adapted_20261012.csv` 20 × 40) · 인계 생성기 열 사전 lhss_* (389/389) · 배포 생성기 두 배치 · 214 결합 (`--supp-batch-root` · 234/234) · 봉인 32 무변경 · 짧은 Codex 검토 요청서 초안 `docs/reviews/codex_supp20_support_review_request_20261012.md` · 자기 결함 `SELF-106` (v1.3 계획 §2-4 컨테이너 대조 문장) | `docs/reviews/g2rr6_fix_plan_20261011.md` §2 · `docs/reviews/lhs_release_v13_plan_20261007.md` §2b |

## 5. 넘어간 뒤 — 지금 상태 (날짜를 보고 읽을 것)

| 트랙 | 마지막 기록 | 다음 (⬜ = 1저자) |
|---|---|---|
| **DEM 언로딩** | Codex 재검토 (10-12) = **문서 부분 수용 · 키트 개발 가능 · 본 R · 10:0 이완 연장 · 개발 / 생산 U = HOLD** · 앞 판정 §8 문서 1 · 5 닫힘 · 2 · 3 · 4 · 6 부분 · Q2 (숫자 = 키트 fixture 뒤) 받음 · Q4 범위 축소 동의 · Q6 10:0 일정 문서 닫힘 | ✅ 반영 계획 Q1–Q4 = 1저자 10-12 권고대로 (Q1 개정 2 + 키트 착수 · Q2 상쇄 우세 주 값 = 진단값 · Q3 비단조 = 첫 교차 + 교차 괄호 합집합 · Q4 "창에서 0" = 매 창 끝 샘플) → ✅ 개정 2 = REG §13 (10-12) · 개정 2 (문서 · `SELF-105` 같은 커밋) → 키트 (시험 먼저 · 판정문 해결 증거 그대로) + S3 함수 · σ_P · 회전 KE 기준 · 표면 관측자 fixture → §12 덧붙임 → ibb 작은 시험 → Codex (키트 증거 + 개정 2) → GO |
| **세대 2 망 · 재검증 7 · 보충 20** | Codex 재검증 7 (10-12 · 핀 `3cedd40a5`) = **GO = 기존 194 발사 승인 · 사전 점검 단계 진입** (보충 20 / 214 GO 아님) · 보충 지원 U1–U5 ✅ (10-12 · 시험 먼저) · 등록 초안 `docs/reviews/lhs_network_batch_registration_20261012_supp20.md` (§2 재수확 지문 빈칸) | ⬜ 1저자 WSL 재수확 (`1e09f661d` · `docs/data/lhs_supp_runs_20261006/README.md` 끝) → ✅ 반입 · r2 키별 대조 (값 동일) · 등록 §2 지문 (10-12) → ✅ 등록 비준 (1저자 10-12 *"비준이야"* — 지문 채운 판) · ⛔ **Codex 보충 검토 (10-12 · 핀 `b429c3c1d`) = HOLD · 새 P1 없음** — P2 `SUP20-01` (배포 대조 `check_v13` 의 배치별 재판정 ROOT (`batch_gate.batch_root`) ↔ 배치 교차 ROOT (`batches[이름].root`) 미결합 — 교차 ROOT 결손 · 없는 경로 = 교차 검사 생략 · 보충 `code_identity` 미검사) · P3 `SUP20-02` (`lhss_w_AM_P` · `lhsx_w_AM_P` 열 사전 — mono 덱의 P 슬롯 = 단일 AM 자리 · mono_AM_S 의 ps_frac = 0 인데 P/(P+S) = 1 로 적힘 · 값은 정상) · 194 R7 기술 GO 유지 · 수치 재계산 요구 없음 · ✅ 판정문 · 증거 반입 (10-12 · `docs/reviews/codex_review_supp20_support_20261012.md` · 증거 `docs/reviews/codex_supp20_support_review_evidence_20261012/` · 우리 트리 재현 `b556dd5db` = Codex 탐침 둘 판정값 차이 0 · 원장 `SUP20-01` · `02` open) · ⬜ 수정 계획 `docs/reviews/sup20_fix_plan_20261012.md` (Q1–Q4 · 1저자 비준 대기) → 반례 먼저 → 짧은 재확인 (수정 diff + 입력 지문 영수증) → 1저자 발사 승인 · ✅ 짧은 Codex 검토 요청서 발송 10-12 (리뷰 핀 `b429c3c1d`) → GO 뒤 같은 날 194 → 보충 20 → v1.3 (§2b) · ✅ `SELF-106` claimed_fixed (10-12) · 재수확 명령 = 배치 venv (`$PY`) 로 정정 |
| **DEM 지배방정식 보고서** (`46cd0bdb8`) | `docs/dem_governing_equations_background_20261011.md` · 자료 `docs/data/dem_governing_equations_report_20261011/` | ⬜ Luding 2008 카드 f_min 의 k_c 인자 누락 → PDF 확인 뒤 정본 브랜치에서 고침 · 고전 출처 7 은 정본 카드 없음 → 이름 언급만 |
| **`/mixer` 침대 보기** | 10-12 1저자 화면에서 LU 두 런이 목록에 없었다 → **`git pull` 뒤 다시 나옴** (원인 = 웹앱 코드가 10-06 정책 갱신 전 판 · 정책에 없는 런은 목록이 아니라 "잠긴 런 · 루트 · 정책" 칸으로 간다 · 런처 `--no-pull` 이면 재발) · DEV 런 사본 = WSL `~/mixer_dev_view/` (LU 포함 6) · `~/mixer_dev7_runs/` (LU 없는 옛 사본) | — |
| 그 밖 1저자 결정 (10-12 인계 4) | MV 실행 · CL-94 / 95 · SELF-100 비준 · 믹서 D1–D6 · 실험 원표 회수 · E_SE 민감도 가지 · DEMP-01 가지 실험 B (ibb job 271368) | 그대로 |

## 6. 지킬 것 (CLAUDE.md 가 정본)

- **보고 → 설명 → 비준 → 실행.**  1저자에게는 게이트 · 커밋 얘기 없이 결과만.
- Codex 판정 반입 = 판정문 · 증거 (`source/` · `upstream/` · `submitted/` 는 manifest · sha 만) · **우리 트리 재현** · 원장 · 진행 기록을 한 묶음으로.  판정문의 "닫힘" 이 **문서 항목** 한정이면 원장을 verified 로 올리지 않는다 (이번 `UL-*`).
- 결정표 · 창 같은 *"규칙이 완결된다"* 문장은 입력 공간 (무효 · 결손 · NaN · 다른 dt) 을 다 적었을 때만 쓴다 (`SELF-105`).
- 시험표의 *"고치기 전 전부 …"* 같은 묶음 문장은 행마다 확인한 뒤에만 쓴다 (`G2RR7-01` — 25 중 1 은 옛 판정식도 이미 거부).
- 재검증 7 의 GO 는 **그 핀의 기존 194** 에 한정 — 보충 지원 코드를 합친 핀으로 발사하면 이 GO 를 그 diff 까지 승인한 것으로 쓰지 않는다 (짧은 Codex 검토가 그 몫).
- 커밋 · PR · 코드 주석에 모델 식별자를 넣지 않는다.

## 7. 붙여 넣을 프롬프트 (stoic-knuth 세션에)

```text
연장 세션 브랜치(claude/sdcp-dem-manuscript-si-pqwtv8)를 이 브랜치(claude/stoic-knuth-NObVQ)로 fast-forward 병합해줘.
인계 문서는 pqwtv8 쪽에만 있으니 먼저 읽어:
  git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && git show FETCH_HEAD:docs/handoff_merge_to_stoic_knuth_20261012.md
1. 아무것도 커밋하지 말고 §2 를 그대로 해: 작업 트리 깨끗 · 로컬 커밋 0 → FF_OK · LOCAL_FF_OK · DOC_OK · litdb 비어 있음 · shallow false → git merge --ff-only.
   하나라도 안 나오면 rebase · force-push · merge 커밋을 만들지 말고 멈추고 보고해.
2. §3 검사 (check_all "✓ 전부 통과" · 원장 643 · ban-sweep · 문서 참조 · 증거 바이트) → claude/stoic-knuth-NObVQ 로 푸시.
3. 그다음 인계 §5 표 순서로 이어가:
   - DEM 언로딩: docs/reviews/dem_unloading_ulr1_fix_plan_20261012.md 의 Q1–Q4 를 나한테 받고 개정 2 → 키트 (반례 먼저).  키트 코드 · ibb 작은 시험은 Codex GO 전 본 실행 아님.
   - 세대 2 망 (보충 지원 U1–U5 구현 끝 · 1저자 순서 (나) · Q4 = (가) lhss · Q5 = (가) 1e09f661d 재수확 · Q6 = (가) 하중 열): 내가 WSL 재수확 묶음을 올리면 반입 (새 빈 폴더 · python -I) · r2 와 키별 대조 · 등록 §2 지문 채움 · SELF-106 claimed_fixed → 짧은 Codex 검토 요청서 docs/reviews/codex_supp20_support_review_request_20261012.md 핀 확정 (발송 = 나).  그 GO 전에는 194 도 발사하지 않는다 (두 배치 같은 날).
보고 → 설명 → 비준 → 실행.  게이트 · 커밋 얘기는 빼고 결과만 담백하게.
```
