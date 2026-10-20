# 인계 — 연장 세션 `claude/sdcp-dem-manuscript-si-pqwtv8` → 본 세션 `claude/stoic-knuth-NObVQ` 복귀 병합 (2026-10-20)

**작성** 2026-10-20 KST 오후 · **작성 세션** 연장 세션 (pqwtv8)
**계기** 1저자 10-20 *"원래 메인 브랜치로 넘어가야되는데 충돌안나게 잘 머지될 수 있도록 프롬프트 부탁할게 · 저 두개 응답도 메인에서 받을거야"* — 두 응답 = Codex 짧은 재확인 둘 (Rint · LHS214 · §5 첫 두 줄).
**앞선 인계 (같은 양식)** `docs/handoff_merge_to_stoic_knuth_20261012.md`

---

## 0. 한 줄

stoic-knuth 의 원격 헤드 `724c4ef08` (10-15 KST 밤 · check_doc_refs selftest 의 SELF-116 fixture 안정화) 는 이 브랜치의 **조상**이고 저쪽이 앞선 커밋은 **0** 이다 (10-20 `git fetch` 로 확인).
⇒ **fast-forward 이고 충돌이 원리적으로 없다.**  조건은 하나 — **병합 전에 stoic-knuth 에 아무것도 커밋하지 않는다.**

## 1. 브랜치 기하 (10-20 · 원격 SHA 는 `git ls-remote` 로 다시 확인)

| 브랜치 | 원격 SHA | merge-base | 이쪽이 앞선 | 저쪽이 앞선 | 병합 형태 |
|---|---|---|---:|---:|---|
| `claude/stoic-knuth-NObVQ` | `724c4ef08` | `724c4ef08` | **56 + 이 문서 커밋 1** (병합 커밋 0 · 묶음별 목록 = §4) | **0** | ✅ fast-forward |
| `claude/friendly-meitner-lldvar` (litdb 정본) | (적지 않는다) | — | — | — | 무관 — 이 세션은 `litdb/` 를 건드리지 않았다 (`git diff 724c4ef08 HEAD -- litdb/` 비어 있음) |

이쪽 HEAD = **이 문서를 담은 커밋** (자기 SHA 는 적을 수 없다 — §2 의 `DOC_OK` 가 확인한다).
⚠ 이쪽에 커밋이 더 생기면 같은 프롬프트를 다시 붙이면 된다 — 단 그 사이 stoic-knuth 에 아무것도 커밋하지 않았을 때만.

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
git cat-file -e "$P":docs/handoff_merge_to_stoic_knuth_20261020.md && echo DOC_OK
git diff --stat "$S" "$P" -- litdb/ | tail -1               # 비어야 한다
git rev-parse --is-shallow-repository                       # false 여야 한다
git fetch origin claude/friendly-meitner-lldvar             # litdb 정본 ref (check_doc_refs · litdb_sync 가 쓴다)

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
| 전수 게이트 | `bash scripts/check_all.sh` (위 스레드 환경변수) | `✓ 전부 통과` · `EXIT=0` (이쪽 HEAD 직전 두 커밋에서 10-20 통과) |
| 원장 | `python3 scripts/check_review_findings.py` | `원장 자기일관 ✓` (736 → **769** 항목 · 새 33 = L214R-05~11 · WEB-09 · L214K-01~08 · L214R-R01~R04 · L214R-S01~S06 · SELF-119~123 · RIMPR-03 · 04 · 상태 claimed_fixed 297 · open 262 · verified 202 · wontfix 8) |
| 인용 금지 스윕 | `python3 scripts/check_review_findings.py --ban-sweep` | 누수 없음 |
| 문서 참조 | `python3 scripts/check_doc_refs.py --quiet` | `✓ 깨진 참조 없음` (litdb 정본 ref 가 있어야 한다 — ⓪ 끝 줄) |
| 증거 바이트 | `git status --short` (체크아웃 직후) | 비어 있음 (`.gitattributes` = `docs/reviews/codex_*_evidence_*/**` `-text` · `docs/data/sdcp_dc_polarization_20261016/` 원본 `.mpr` 은 바이트 그대로 — CRLF · 정규화 커밋 금지) |

## 4. 무엇이 넘어가나 (56 커밋 · 날짜 = KST)

| 묶음 | 커밋 (처음 → 끝) | 요지 |
|---|---|---|
| 원장 DR3-06 | `b54b0ded0` | 직경 보존 재척도의 VGCF 접촉 한계 메모 |
| LHS214R 수정 (10-16) | `2d02da2b3` → `a4a1e52c0` | 수정 계획 · 1저자 비준 → L214R-01~11 · WEB-09 (시험 먼저 → 수정) · 증거 · Codex 짧은 재확인 요청서 |
| Codex LHS214 재확인 반입 · R01–R04 (10-18 ~ 10-19) | `396d76eff` → `b2681cfec` · `155534744` | 판정 (HOLD · 새 P1 없음) · 우리 트리 재현 · R01 · R02 · R03 · R04 수정 · 요청서 |
| Codex LHS214RR 반입 · S01–S06 (10-19) | `be75bdd07` → `685c2bbdb` · `df551f708` → `34713ac96` | 수치 인계 코드 HOLD 해제 가능 판정 · S01 · S02 · S04 · S06 수정 · 요청서 둘 (마지막 = 리뷰 핀 `34713ac96`) |
| SDCP DC 원자료 · 앵커 v2 (10-19 ~ 10-20) | `85978b21e` · `77d8fd445` · `125944461` · `298a73197` · `45067b9cd` → `406cec59f` · `7db2c58ed` → `1fe3e0a29` | DC 분극 원본 16 파일 · 등록 v2 (결과 전) · §3-D 이온 σ₀ 앵커 · 원고 · SI 수정 체크리스트 · SELF-120 사슬 수정 · S1 · S2 · C (σ* 0.347) · R1 재압밀 · 최종 16 팔 · S1b 정찰 등록 · 결과 |
| Rint (10-20) | `3b9d51789` → `d8808c164` | RIMPR-01 · 02 조인 수정 · 원장 · 요청서 · 탄소 접점 · 첨가제 초안 둘 · Q7 막 값 관문 (`2b9efa253` = 리뷰 핀) · 통합 계획 v1 |

## 5. 넘어간 뒤 — 지금 상태 (날짜를 보고 읽을 것 · 10-20 오후)

| 트랙 | 마지막 기록 | 다음 (⬜ = 1저자) |
|---|---|---|
| **Rint** (1저자 10-20 최우선 · LHS 보다 먼저) | RIMPR-01 · 02 수정 `3b9d51789` (claimed_fixed) · Q7 일반 관문 막 값 불변량 `2b9efa253` (r_face 유한 · ≥ 0 · r = 0 허용 · iface 끔 무관 · 시험 133/136 → 136/136 · rrm 54/55 → 55/55) · Codex 짧은 재확인 요청서 `docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md` (**리뷰 핀 `2b9efa253`** · 핀 칸 채운 발송본 = 1저자가 보냄) · 새 P3 RIMPR-03 · 04 (다음 묶음) | **Codex 응답 = 본 세션에서 받는다** → 판정문 · 증거 반입 · 우리 트리 재현 · 원장 (닫힌 것만 verified · 범위 한정) → ⬜ 통합 계획 v1 `docs/reviews/rint_carbon_additive_plan_20261020.md` Q1–Q12 비준 (권고 = 표 그대로 · Q1 = SBE 1.63 보정 한 점 · DBE 4.68 holdout) → Codex 설계 리뷰 (S0–S3 + 등록 초안 한 회차) → S0 → S1 PTFE 면 개구율 → S2 탄소 접합 R_j → S3 SDCP 수정자 (시험 먼저 · 기본 끔 · 웹앱 같은 묶음) |
| **LHS214** | S06 `3260891d4` · S02 `4c285dd5d` (claimed_fixed) · Codex 짧은 재확인 요청서 `docs/reviews/codex_lhs214cx_fix_recheck_request_20261019.md` (**리뷰 핀 `34713ac96`** · 같은 Windows 환경에서 고치지 않은 원본 시험 재실행 요청 · 발송본 = 1저자가 보냄) | **Codex 응답 = 본 세션에서 받는다** → 반입 · 재현 · 원장 → GO 면 ⬜ 등록 개정 비준 · 재봉인 · B7 승인 핀 · 새 ROOT · 사전 점검 · 1저자 발사 승인 → 새 214 → §5 판정 · v1.3 (Codex 10-19 = 수치 인계 코드 HOLD 해제 가능 · 새 214 는 그 절차 전 HOLD) |
| **SDCP σ_e 앵커 v2** (원고 10-20) | 최종 16 팔 ✅ (8 팔 평균 SBE σ_e 1.6209 · σ_ion 0.13704 · DBE σ_e 1.8877 · 비 1.1646) · S1b 정찰 σ_VGCF 2.618 → DBE 4.7524 mS/cm (+1.5 %) · **1.309 = 완주 (10-20 11:28 KST · resid 1.0e-08 · 값 미열람)** · 기록 = `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md` §7 | ⬜ kgy `python3 ~/s1b_values.py` 로 세 점 (0.347 · 1.309 · 2.618) + 등록 S2 값 열기 → ⬜ 1저자 DBE 보정값 결정 (권고 = 2.618 · 8 팔 · LEAN=4 · 명령은 10-20 대화 · 출력 `~/sdcp/final8_dbe_vgcf2618` · 로그 `~/final8_dbe_vgcf2618.log`) → 고른 값 그대로 기록 (라벨 = 실측 전극 DC 앵커 보정 · 사다리 점 · 예측 아님) → 원고 · SI · Table S3 · 그림 = `docs/reviews/ms_change_checklist_sdcp_v2_20261019.md` |
| DEM 언로딩 키트 | 이 연장 세션에서 손대지 않음 (CLAUDE.md 줄 그대로) | 그대로 |
| 세미나 덱 | 10-16 트랙 닫음 (`6cb256956`) | 발표 PC 확인 = 1저자 |
| 그 밖 1저자 결정 | 믹서 D3 첫 Codex 검토 · MV · CL-94 / 95 · DEMP-01 가지 실험 등 (앞선 인계 §5 그대로) | 그대로 |

⚠ **kgy**: GPU 런이 도는 동안 kgy 리포 체크아웃을 `git pull` · `checkout` 하지 않는다 — 러너가 팔마다 새 파이썬을 띄워 스크립트를 디스크에서 다시 읽는다 (10-20 13:46 GPU 98 % · 18.7 GB 사용 중).  런이 끝난 뒤 kgy · WSL 명령의 `origin/claude/sdcp-dem-manuscript-si-pqwtv8` 는 `claude/stoic-knuth-NObVQ` 로 바꿔 쓴다.

## 6. 지킬 것 (CLAUDE.md 가 정본)

- **보고 → 설명 → 비준 → 실행.**  1저자에게는 게이트 · 커밋 얘기 없이 결과만.  혼자 앞서 가지 않는다 (*"니 혼자서 하지말고"*) · 파일은 **달라고 할 때** 보낸다 (*"내가 주라고 할떄 줘"*).
- 커밋 하나 → 게이트 (`check_all.sh` "✓ 전부 통과") → 바로 push · 로컬 커밋을 쌓지 않는다 · 게이트 도는 동안 작업 트리를 건드리지 않는다 · PR 만들지 않는다 · 봉인 32 파일 (`code_fp e8b2496b…`) 수정 금지.
- Codex 판정 반입 = 판정문 · 증거 (`source/` · `upstream/` · `submitted/` 는 manifest · sha 만) · **우리 트리 재현** · 원장 · 진행 기록을 한 묶음으로.  받은 ZIP 은 새 빈 폴더에 풀고 `python3 -I` 로 읽기만 — 안에 든 스크립트를 그 폴더에서 실행하지 않는다.  판정문의 "닫힘" 이 범위 한정이면 원장 `verified_scope` 에 그 범위를 적는다.
- **요청서의 리뷰 핀은 요청서를 담은 커밋으로 고정**한다 (Rint = `2b9efa253` · LHS = `34713ac96` — 둘 다 원격에 있다 · fast-forward 뒤에도 같은 SHA).
- 컨테이너 재시작 대비 (10-20 에도 두 번 났다): 받은 원자료는 기록 폴더에 먼저 넣어 push · 작업 트리 에이전트가 끊기면 남은 작업 트리에서 시험 커밋 · 수정을 회수해 새 빈 폴더에서 고치기 전 실패를 다시 확인한 뒤 옮긴다 · 다 옮긴 작업 트리는 지운다.
- 보정값은 1저자가 고른 그대로 기록하고 보정이라 적는다 — 보정한 값을 예측이라 부르지 않는다 · 모델에 없는 물리 (탄소 접점 Rint ②) 를 있는 것처럼 적지 않는다 (등록 v2 §7 · 통합 계획 §3 금지 문장).
- 서지 · 값은 litdb 정본 카드에서만 · 커밋 · PR · 코드 주석에 모델 식별자를 넣지 않는다 · ibb 주소 · 포트는 리포에 쓰지 않는다 · 웹앱은 :5002 만.

## 7. 붙여 넣을 프롬프트 (stoic-knuth 세션에)

```text
연장 세션 브랜치(claude/sdcp-dem-manuscript-si-pqwtv8)를 이 브랜치(claude/stoic-knuth-NObVQ)로 fast-forward 병합해줘.
인계 문서는 pqwtv8 쪽에만 있으니 먼저 읽어 (10-20):
  git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && git show FETCH_HEAD:docs/handoff_merge_to_stoic_knuth_20261020.md
1. 아무것도 커밋하지 말고 §2 를 그대로 해: 작업 트리 깨끗 · 로컬 커밋 0 → FF_OK · LOCAL_FF_OK · DOC_OK · litdb 비어 있음 · shallow false · litdb 정본 ref fetch → git merge --ff-only.
   하나라도 안 나오면 rebase · force-push · merge 커밋을 만들지 말고 멈추고 보고해.
2. §3 검사 (check_all "✓ 전부 통과" · 원장 769 · ban-sweep · 문서 참조 · 증거 바이트) → claude/stoic-knuth-NObVQ 로 푸시.
3. Codex 응답 둘을 이 세션에서 받는다 (내가 올린다):
   - Rint 짧은 재확인 (RIMPR-01 · 02 + Q7 · 리뷰 핀 2b9efa253 · 요청서 docs/reviews/codex_rint_join_rimpr_fix_recheck_request_20261020.md)
   - LHS214 짧은 재확인 (S06 · S02 · 리뷰 핀 34713ac96 · 요청서 docs/reviews/codex_lhs214cx_fix_recheck_request_20261019.md)
   받으면 각각: ZIP 은 새 빈 폴더에 풀고 python3 -I 로 읽기만 → 판정문 · 증거 반입 → 우리 트리 재현 → 원장 (닫힌 것만 verified · 범위 한정) → 진행 기록 → 나한테 결과만 보고.
   새 결함이 나오면 수정 계획 (Q 마다 권고 한 줄) 을 먼저 보여주고 내 비준 뒤 시험 먼저 → 수정.
4. 그다음 인계 §5 표 순서 — 각 줄의 ⬜ 는 나한테 먼저 묻고:
   - Rint 가 LHS 보다 먼저.  Rint ② 통합 계획 v1 (docs/reviews/rint_carbon_additive_plan_20261020.md) Q1–Q12 는 내가 정한다 → 그 뒤 Codex 설계 리뷰 → S0 부터.
   - LHS214 는 Codex GO 뒤 등록 개정 비준 · 재봉인 · 사전 점검 · 내 발사 승인 → 새 214 → v1.3.
   - SDCP: kgy S1b 세 점 (python3 ~/s1b_values.py) 을 내가 올리면 등록 v2 §7 에 기록 · DBE 보정값은 내가 정한다 (권고 2.618 · 8 팔) → 고른 값 그대로 · 보정이라 기록 → 원고 · SI 체크리스트.
     kgy 에서 런이 도는 동안 kgy 체크아웃 git pull 금지.
보고 → 설명 → 비준 → 실행.  게이트 · 커밋 얘기는 빼고 결과만 담백하게.  파일은 내가 달라고 할 때만.
```
