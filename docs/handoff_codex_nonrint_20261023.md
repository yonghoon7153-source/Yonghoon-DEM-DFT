# Codex 인계 — Rint 를 뺀 트랙 (2026-10-23 · 용훈 포메이션)

> **근거 (1저자 10-23 원문)**: *"Rint는 여기서 하고 나머지 믹서나 그런것들은 codex한테 전체적으로 부탁하고 관련해서 작업한것들 충돌없이 여기에 머지"* · *"용훈 포메이션에서 Rint 외적인 부분 … 그걸 부탁하고 싶은데"* · *"서로 소통하고"* · *"중간중간 codex 반박 리뷰도 받게 하고"* · *"우리 평소에 하던것처럼"* · *"지금 우리가 하는것처럼 메인브랜치에서 따로 분리된 브랜치이고 나중에 … claude/stoic-knuth-NObVQ 병합하도록 … 그대로 codex에서도 할 수 있나?"*
> **정본 순서**: `CLAUDE.md` > `docs/*.md` > 이 문서.  날짜를 보고 읽는다 — 날짜 없는 서술을 현재형으로 읽지 않는다 (CLAUDE.md 규율 ④).  이 문서의 상태 = `fdb48d378` (10-23) 기준 · 기록 밖 진행 (1저자가 기계에서 한 일 등) 은 반영 못 했다 — 표의 *"기록 없음"* 칸은 1저자에게 확인한다.
> **사본** — 1저자가 붙여 넣은 이 문서와 같은 내용을 Claude 가 `docs/handoff_codex_nonrint_20261023.md` 로 커밋한다 (A′ 병합 뒤).

## 0. 역할

| 누구 | 맡는 것 |
|---|---|
| Claude (클라우드 세션 · 가지 `claude/sdcp-dem-manuscript-si-pqwtv8`) | Rint ② 전부 · Codex 작업을 이 가지에 넣기 (cherry-pick → 전체 게이트 → push) · stoic-knuth 로 넘기기 (평소 fast-forward 인계) |
| Codex 작업 세션 (이 창) | Rint 를 뺀 트랙의 실무 (§5) — 구현 · 시험 · 계획서 · 요청서 초안 · 기록 조각 |
| Codex 반박 세션 (로컬 · 그대로) | 지금처럼 반박 리뷰 — Claude 작업 (Rint) 과 Codex 작업 둘 다 |
| 1저자 | 비준 · 발송 · 기계 실행 (kgy · gabia · ibb · v100 · WSL) |

## 1. 가지 — 지금 이 세션처럼 (메인에서 분리된 가지)

- 저장소 = GitHub `yonghoon7153-source/Yonghoon-DEM-DFT` · 메인 가지 = `claude/stoic-knuth-NObVQ` (연결 = 1저자).
- 네 가지 = `codex/<트랙>` (예: `codex/unloading-ulpr` · `codex/lhs214-relaunch` · `codex/mixer-mxd2`) — 트랙마다 하나 권장 (받는 쪽이 트랙 단위로 독립).
- **시작점 = `origin/claude/sdcp-dem-manuscript-si-pqwtv8` 의 `fdb48d378`** (또는 그 뒤 push 된 끝):
  - stoic-knuth 끝 `93d93bc02` (10-21) 은 이 가지보다 56 커밋 뒤다.  Rint 밖 트랙 파일은 둘이 같다 — 다른 것은 Rint 파일 + 공유 기록 (`CLAUDE.md` · 진행 기록 · 원장 · `docs/reviews/doc_refs_allowlist.tsv`) + `scripts/step3_sigma.py` · `webapp/templates/mpm_lab.html`.
  - `93d93bc02` 에서 새로 clone 해 전체 게이트를 돌리면 `scripts/test_carbon_junction.py` LEN-BIT 가 실패한다 — 10-22 기록: 같은 시험 파일인 `82dbe003c` 에서 실패 1 (기준 커밋이 원격에 없음) · 고친 커밋 `89e596954` 는 이 가지에만 있다.
- **왜 cherry-pick 인가** — 지금 이 세션이 stoic-knuth 로 fast-forward 할 수 있는 것은 그동안 stoic-knuth 가 멈춰 있기 때문이다.  분리된 가지가 둘 (Claude · Codex) 이 동시에 자라면 둘 다 fast-forward 할 수는 없다 (하나를 넣으면 다른 하나는 더 이상 그 끝의 후손이 아니다).  병합 커밋 · rebase · force-push 는 금지 (1저자) 이므로:
  - Codex 커밋 → Claude 가 이 가지에 **cherry-pick** (Rint 커밋 SHA 는 원장 · 문서가 이미 인용하므로 그대로 둔다) → 평소 fast-forward 인계로 stoic-knuth.
  - 그래서 cherry-pick 된 Codex 커밋은 SHA 가 바뀐다 → §2 "SHA" 줄.
- push = `codex/*` 에만.  `claude/*` 가지에 push · force-push 금지 · GitHub 에서 PR 병합 버튼을 누르지 않는다 (병합 커밋이 생기면 평소 인계가 막힌다).  `codex/*` 가지는 지우지 않는다 (요청서 · 쪽지가 그 SHA 를 인용한다).

- 연결 (1저자): 웹 Codex = 설정에서 GitHub 연결 → 이 저장소 선택 · 로컬 Codex = 반박 세션이 쓰는 폴더와 겹치지 않는 새 폴더에 clone (push 권한 확인).

```bash
# 로컬이면 한 번만
git clone https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT ~/codex-work && cd ~/codex-work
# 트랙마다
git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8
git checkout -b codex/<트랙> origin/claude/sdcp-dem-manuscript-si-pqwtv8
git log -1 --oneline                        # fdb48d378 (또는 그 뒤 끝)
git push --dry-run origin codex/<트랙>      # push 권한 확인 (실제로 올리지 않음)
```

## 2. 충돌 없이 합치는 규칙

| 규칙 | 내용 |
|---|---|
| 파일 소유 | Rint 파일 = Claude 만 (아래 목록) · 네 트랙 파일 = 너만 |
| 공유 기록 | `CLAUDE.md` · `docs/session_20260923_progress.md` · `docs/reviews/findings.json` · `docs/reviews/claims.json` · `docs/reviews/doc_refs_allowlist.tsv` · `wiki/` = 너는 직접 고치지 않는다.  바꿀 내용은 쪽지 (§3) 에 그대로 적는다 — 덧붙일 줄 · 원장 항목 JSON 조각.  Claude 가 반영하고 검사기를 통과시킨다 |
| 공유 코드 | 두 쪽이 다 쓰는 코드 — `scripts/step3_sigma.py` · `scripts/additives.py` · `scripts/dem_analysis_core.py` · `scripts/check_*.py` · `scripts/check_all.sh` · `.github/` · 웹앱 공용 (`webapp/app.py` 는 봉인 파일) — 를 고쳐야 하면 먼저 쪽지로 알리고 답을 기다린다 |
| 봉인 32 파일 | `scripts/run_network_194_parallel.py` 의 `CODE_FILES` — 등록 · 비준 없이 손대지 않는다 |
| SHA | 네 커밋의 SHA 를 문서 · 기록 조각에 적지 않는다 (cherry-pick 뒤 도달 못 하는 SHA 가 된다 · `SELF-116`).  필요하면 `<<sha:커밋 제목 앞 낱말>>` 자리 표시 → Claude 가 받은 뒤 새 SHA 표를 쪽지로 보낸다.  요청서의 리뷰 핀 = 네 `codex/*` 커밋 (가지를 지우지 않으므로 도달 가능) |
| 게이트 | 커밋마다 `python3 scripts/check_doc_refs.py` · `python3 scripts/check_review_findings.py` rc 0 · 넘기기 전 `bash scripts/check_all.sh` = "✓ 전부 통과".  줄이지 않는다 |
| 환경 | Linux/WSL 에서 작업 — Windows 줄바꿈 변환은 파일 지문 · sha256 을 바꾼다 |

Claude 소유 파일 (손대지 않음 · Rint ② + 옛 R_int 풀셀 · 사이클 도구 + SDCP 앵커 사슬): `scripts/` 의 `rint_*.py` · `ca_ext_*.py` · `ca_s0_census.py` · `carbon_junction.py` · `ptfe_face_alpha.py` · `step3_conv_cert.py` · `step4_rint_ladder.py` · `cycle_rint_synthesis.py` · `fit_rint_curve.py` · `plot_cycle_rint_decomp.py` · `rint03_je_compare.py` · `sdcp_anchor_v2_chain.py` · 그 시험 (`test_rint_*` · `test_ca_ext_*` · `test_ca_s0_census.py` · `test_carbon_junction.py` · `test_ptfe_face_alpha.py` · `test_step3_conv_cert.py` · `test_step3_target_cert.py`) · `webapp/test_ca_ext_labels.py` · `webapp/test_rint_*` · `webapp/static/explain/rint_*` · `docs/` 의 이름에 `rint` 가 든 파일 · 폴더 · `docs/reviews/` 의 `rint*` · `codex_*rint*` · `contact_resistance_pipeline_*` · `additive_physics_brief_*` · `docs/voxel_contact_free_gap.md`.

## 3. 서로 연락 — 쪽지 (git 안 · 쪽지 하나 = 새 파일 하나 · 고치지 않음)

| 방향 | 자리 | 내용 |
|---|---|---|
| Codex → Claude | 네 가지의 `docs/collab/codex_to_claude/` 에 `YYYYMMDD-HHMM_<트랙>.md` | 무엇을 했나 · 가지 · 끝 SHA · 받아 갈 커밋 범위 · 공유 기록에 넣을 줄 · 원장 JSON 조각 · 질문 |
| Claude → Codex | `claude/sdcp-dem-manuscript-si-pqwtv8` 의 `docs/collab/claude_to_codex/` 에 `YYYYMMDD-HHMM_<주제>.md` | 받은 커밋 ↔ 새 SHA 표 · 반영한 공유 기록 · Rint 쪽 변경 중 네 트랙에 닿는 것 · 답 · 질문 |

- 확인 = 단계를 시작할 때마다 상대 가지를 fetch 해서 새 쪽지를 읽는다 · 1저자가 "올렸다" 고 하면 바로.
- 쪽지는 정보다 — 발사 · 발송 · 비준 · 기계 실행은 늘 1저자 승인 뒤 (쪽지만으로 하지 않는다).

## 4. 검토 — 평소처럼

- 언제 (중간중간) = ① 트랙마다 수정 · 구현 묶음이 끝났을 때 ② 설계 · 등록 · 계획 초안이 나왔을 때 ③ 1저자 발송 · 발사 · 배포 전 (이 자리는 반박 세션 GO 필수).  받아 가기 (cherry-pick) 와 반박 리뷰는 서로 기다리지 않는다 — 리뷰 핀 = 네 `codex/*` 커밋.
- 네 작업 → Codex 반박 세션 리뷰 (평소 절차): 요청서 (맨 위 "이번에 닫는 것 / 닫지 않는 것" · 리뷰 핀 · ZIP = 핀 blob + `PIN.txt` + `MANIFEST.sha256`) → 1저자 발송 → 판정문 · 증거 → 반입 (`docs/reviews/codex_review_*` + 증거 폴더) → 우리 트리 재현 → 수정 계획 Q → 1저자 비준 → 시험 먼저 수정.
- 요청서 보내기 전 **사전 공격 리뷰** = `CLAUDE.md` "★ Codex 요청 전 사전 공격 리뷰" ①–④ 그대로 (숫자 · 전칭 대조 · 지난 HOLD 부류 · 독립 검토자가 diff 만 보고 반례 · 보장마다 작은 해석 반례).
- 발사 · 배포 GO 가 반박 세션 판정이던 자리 (LHS214 다시 발사 · 믹서 확인 블록 · 언로딩 본 실행 · FAM) 는 그대로다 — 기준을 낮추는 안을 내지 않는다 (1저자 10-20).

## 5. 트랙 (용훈 포메이션)

### 5-0. 멈춰 있던 일 · Codex 대기건 한눈에 (10-20 용훈 포메이션 보고 = 진행 기록 10-20 21 · 22 줄 이후 · `fdb48d378` 기준)

| 트랙 | 멈춘 자리 (마지막 기록) | 이어서 할 일 | 자세히 |
|---|---|---|---|
| 언로딩 | 재확인 2 요청서 발송 전 사전 리뷰 = `ULPR-01`–`04` → *"고친 뒤 발송"* (10-21) | 고치기 (시험 먼저) → 독립 재확인 → 요청서 갱신 → 발송 (1저자) | §5-4 |
| LHS214 | 다시 발사 묶음 비준 · 확인 요청서 초안 2 (10-21) | 독립 사전 리뷰 → WSL 사전 점검 (1저자) → 반입 → 발송 | §5-1 |
| 믹서 D2 | 구현 뒤 사전 리뷰 `MXD2-01`–`07` → *"고친다"* (10-21) · Codex 검토 아직 없음 | 고치기 (시험 먼저) → Codex 요청 | §5-3 |
| 믹서 D3 | 설계 v1 사전 공격 리뷰 = 깨짐 8 → *"고친뒤 보내자"* (10-21) | 설계 v2 → 독립 재공격 → 발송 · 1저자 자료 칸 빈칸 | §5-3 |
| DEM 프로토콜 세대 2 | 계획 초안 Q1–Q16 결정 끝 (10-14 · 10-20) · Codex 요청서 아직 없음 | 계획서 §9 개요대로 요청서 + 사전 공격 리뷰 → 발송 · 1저자 측정 (Q7 펠릿 두께 · Q8 랩 표준 기록) | §5-5 |
| 믹서 원장 | claimed_fixed 25 (HB 3 · HBR2 4 · HBR3 5 · HBR4 2 · HBR6 2 · HBR10 3 · MIX 6) = Codex 확인 대기 | 다음 믹서 요청서에 확인 목록으로 | §5-3 |
| 1저자 자료 대기 (10-20 용훈 포메이션) | Q8 D3 장비 목록 · Q11 언로딩 실험 입력 · Q13 EIS 펠릿 · Q16 10/21 덱 정정 — 그 뒤 기록 없음 | 1저자에게 확인 · 받기 전 해당 칸은 빈칸 | §5-3 · §5-4 · §5-5 · §5-8 |


### 5-1. LHS 접촉망 — 214 다시 발사 · v1.3

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| Codex 10-20 재확인 | S06 · S02 닫힘 · 새 결함 없음 · 새 214 = 다섯 단계 (등록 비준 · 재결합 · 승인 핀 · 새 ROOT 사전 점검 · 1저자 발사 승인) 뒤 | `docs/reviews/codex_review_lhs214cx_fix_recheck_20261020.md` §5 | — |
| 다시 발사 묶음 | 1저자 10-21 *"다 진행하자"* → 영수증 S0b 시험 수정 `fe23f2b83` (`SUPR-03` claimed_fixed) · 두 등록 비준 `f82929b06` · 확인 요청서 초안 2 `02393562f` | `docs/reviews/lhs214_relaunch_package_20261020.md` · `docs/reviews/codex_lhs214_relaunch_check_request_20261020.md` · `docs/reviews/lhs214_relaunch_s0b_evidence_20261021/` | ▶ 남은 순서 (10-21 기록 · 그 뒤 진행 기록 없음 — 1저자에게 확인): 독립 사전 리뷰 (규칙 ③ — 너는 이 묶음을 쓰지 않았으니 독립 검토자가 될 수 있다) → WSL 사전 점검 (B7 핀 · 새 ROOT 둘 · 1저자) → 반입 → 발송 (1저자) → 반박 세션 GO → 1저자 발사 승인 |
| 등록 | 194 · 보충 20 (봉인 32 = 묶음 §2 지문) | `docs/reviews/lhs_network_batch_registration_20261007_g2.md` · `docs/reviews/lhs_network_batch_registration_20261012_supp20.md` | 지문은 묶음 문서 절차로만 |
| 10-20 결정 (용훈 포메이션 Q3–Q6) | Q3 194 §9-8 · 보충 §9-3 개정 + 활성 §3 지문 비준 (비준 커밋 = 다섯 단계 묶음 뒤) · Q4 σ₀ 1.5 = 이번 재봉인 제외 · Q5 다섯 단계 묶음 Codex 확인 뒤 발사 · Q6 S05 = v1.3 뒤 · SUP20 영수증 = 일반 실행 게이트에 안 넣음 | 진행 기록 10-20 22 | — |
| v1.3 배포 (최종판) | 214 판정 뒤 한 번에 | `docs/reviews/lhs_release_v13_plan_20261007.md` | 214 뒤 |
| 열린 원장 | `WEB-10` (P3 · 요약 복사 문구 AM_P 0 · 214 뒤 생산자 None 결정과 함께) · `L214K-01`–`08` (P3 · 알려진 항목 · 1저자 마지막 라운드) · 머리글자별 (`fdb48d378`): LHS open 12 · claimed_fixed 18 · L214 open 10 · claimed_fixed 3 · LHSC open 4 · claimed_fixed 1 · G2 open 2 · claimed_fixed 3 · WEB open 7 · claimed_fixed 1 | `docs/reviews/findings.json` | claimed_fixed = 다음 LHS 요청서에 확인 목록 |
| 수영 님 ML 대조 | 10-05 1차 · 회신 = 1저자 | `docs/data/lhs_ml_crosscheck_20261005/README.md` | 1저자 |

### 5-2. LHS DEM 런 — 후막 8

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| 보충 20 + 후막 8 DEM | 28/28 완주 (10-11 · ibb) · 보충 20 = 214 에 들어감 | `docs/data/lhs_supp_runs_20261006/` · `docs/reviews/lhs_supp_thick_registration_20261006.md` | — |
| 후막 8 (6 · 8 mAh 짝 · LHS 밖) | 수확 · 접촉 · 망 = 기록 없음 (미확인) · 1저자 순서 = LHS 인계 먼저 → 후막 바이모달 미세구조 | 진행 기록 10-05 · 10-11 | 214 · v1.3 뒤 · 1저자 |

### 5-3. 믹서 · 이종기술

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| 논지 정본 | 1저자 비준 10-05 · 비준 블록 = 웹앱 `/hetero` 가 읽는다 (바꾸려면 비준) | `docs/hetero_thesis.md` | — |
| 결정 D1–D14 | D1–D6 = 1저자 10-14 권고대로 (D1 확인 18 런 동결 · 결합 규칙 팔로 새 확인 블록 · D2 기하평균 결합 규칙 · D3 유동성 실측 앵커 · D4 NCM · LPSCl 표면 에너지 + 계면 분리일 = VASP 외주 결과 뒤 · D5 · D6 10/21 자료) · D7–D14 = 1저자 10-20 권고대로 (D7 코팅 SE 를 자유 SE 에서 뺌 (코팅 두께 실측 필요) · D8 통계 이식 + 무작위 배치 음성 대조 · D9 s1 · s2 + 점착 0 회전 기준 + 이론 분모 Lacey · D10 8 바퀴 한 런을 bin 1 · 3 · 7 로 · D11 층상 유지 + SE 덩어리 시작 DEV 먼저 · D12 ×20 · ibb NP 20 · 처음부터 · 확인 시드 셋 · D13 빠진 원자 처리 권고 · D14 실험 변수 셋 · 담당) | `docs/hetero_thesis.md` §4 · `docs/mixer_paper_pipeline_draft_20261013.md` §4 | — |
| 밀도 세대 | gen1 · lab20261014 (10-14 구현) | `scripts/additives.py` `DENS_GENERATIONS` · 진행 기록 10-14 밤 10 · 11 | ⚠ `scripts/additives.py` = 공유 코드 (§2) |
| D2 구현 | 1저자 10-14 *"이거 진행하자"* · 벽 값 γ_W/γ = 0.0256 (10-14 Q1′) · Codex 검토 아직 없음 | 진행 기록 10-14 밤 3 · 6 | MXD2 고친 뒤 Codex 요청 |
| D2 사전 리뷰 | `MXD2-01`–`07` open (P2 2 · P3 5 — 되읽기 · 비교 · 스모크가 lab 세대 · D2 규칙을 모름 · 변이 생존) · 1저자 10-21 *"권고대로 해줘"* = 고친다 (시험 먼저) · `MXD2-07` = D3 v2 에서 | `docs/reviews/findings.json` · 진행 기록 10-21 06 | ▶ 고치기 |
| D3 설계 | v1 (10-15 · Q1–Q12 비준) → 사전 공격 리뷰 (10-21) = 보장 14 중 깨짐 8 · 조건부 5 · 선례 위험 1 → 1저자 *"고친뒤 보내자"* = 설계 v2 (새 파일 · 원장 `MXD3` 항목 · 반례를 검사로 먼저) → 독립 재공격 → 발송 · Codex 두 회차 (10-20 Q9) | `docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md` · `docs/reviews/codex_mixer_d3_design_request_20261021.md` (+ 같은 이름 `_evidence_20261021/`) | ▶ v2 · 1저자 자료 대기 칸은 빈칸 (장비 목록 · 실험 혼합기 · G · 벽 재료 · SE 진밀도 1.64 ↔ 1.86 · 측정자 · 탭 방식 · 시료량 · 반복 · 입도 측정법) |
| 고-Bo 확인 18 런 | 동결 (D1) | `docs/reviews/mixer_highbo_prereg_20260927.md` | D2 · D3 뒤 새 확인 블록 |
| 층상 본 캠페인 | 완료 (09-30 · 등록된 무분리 범주 · 한정어 필수) | `docs/reviews/mixer_layered_prereg_20260921.md` | — |
| 믹서 원장 (`fdb48d378` · 머리글자별) | claimed_fixed 25 = HB 3 · HBR2 4 · HBR3 5 · HBR4 2 · HBR6 2 · HBR10 3 · MIX 6 (Codex 확인 대기) · open = HB 1 · HBR5 2 · HBR6 1 · HBR7 6 · HBR8 4 · MIX 6 · MXD2 7 | `docs/reviews/findings.json` | 다음 믹서 요청서에 확인 목록 |
| 웹앱 `/mixer` · `/hetero` | `/mixer` v1.5 (10-06 기록) | `webapp/mixer_bed.py` · `webapp/mixer_view_policy.json` | 코드 바꾸면 같은 묶음 (J20-l) |

### 5-4. DEM 언로딩 키트 (ps45)

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| 등록 · 키트 | 등록 (개정 3 = §14) · 키트 | `docs/reviews/dem_unloading_ps45_prereg_20261009.md` · `docs/data/ps45_unload_20261009/` | — |
| ibb 문법 실행 2 | PASS (10-15 · 19/19 · 반복도 19/19) · `GRAMMAR_VERDICT` = 실행 2 런 (1저자 10-15) | `docs/reviews/dem_unloading_grammar_fixture_runs_20261015/README.md` | — |
| Codex 짧은 재확인 2 | 요청서 (리뷰 핀 `92e6cda4d`) → 발송 전 사전 리뷰 (10-21) = `ULPR-01` (P2 · 이어 돌린 새 시도가 단 줄을 다시 쓰기 전에 끝나면 옛 시도의 그 줄이 정상 관측으로 쓰인다) · `ULPR-02`–`04` (P3) → 1저자 *"권고대로"* = 고친 뒤 발송 · `ULPR-04` = G2c 열 결손 = UNCONFIRMED (등록 §14-10) | `docs/reviews/codex_dem_unloading_kit_fix_recheck2_request_20261015.md` · `docs/reviews/findings.json` | ▶ 고치기 (시험 먼저) → 독립 재확인 → 요청서 갱신 → 발송 (1저자) |
| 1저자 자료 대기 | Q11 언로딩 실험 입력 (10-20 · 그 뒤 기록 없음) | 진행 기록 10-20 22 | 1저자 |
| 언로딩 원장 (`fdb48d378`) | claimed_fixed 10 = ULKR 4 · ULKRF 3 · ULKRR 3 (재확인 2 에서 확인) · open = ULPR 4 · ULR1 3 | `docs/reviews/findings.json` | — |
| 본 R · 10:0 연장 · U | ⛔ 재확인 GO 뒤 · 7:3 `RJ` 의 `HIST_VERDICT` = ibb `hist_20261014_094731/` (지우지 않는다) | `CLAUDE.md` 10-14 줄 | GO 뒤 1저자 실행 |

### 5-5. DEM 프로토콜 세대 2 · 모델 검증

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| Codex 모델 검증 판정 (10-08) | 원장 `MV-01`–`09` open (서보 종료 규칙 · fix 재생성 이력 · ε 정의 · 기하 고정 · 중력 순서 · dt · LW 응력 · 보존 · README 값) · `DEMP-01` (전역 감쇠가 '300 MPa' 의 큰 몫) · `DEMP-02` (판 메시 관통) open | `docs/reviews/codex_review_model_validation_20261008.md` · `docs/data/ps73_damping_branch_20261007/README.md` · `docs/reviews/findings.json` | 세대 2 가 닫는다 |
| 세대 2 계획 초안 | 단계 = 삽입 → 안정화 → 압축 → 서보 → 이완 → 언로딩 → 판 분리 · 자유 표면 · 진밀도 NCM 4.85 · SE 1.64 · ν_SE 0.37 · Q1–Q16 결정 끝 (1저자 10-14 · 10-20 권고대로) · 런 0 · 등록 아님 | `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` §8 | ▶ §9 개요대로 Codex 설계 검토 요청서 (사전 공격 리뷰 먼저) → 발송 (1저자) → 등록 · 시험 먼저 → 런 |
| 1저자 측정 · 기록 | Q7 EIS 펠릿 두께로 진밀도 1.64 검산 (0.100 g · 지름 10 mm 펠릿이 0.776 mm 보다 얇으면 1.64 불가) · Q8 "10–13 % 랩 표준" 측정 기록 · Q9 펠릿 두께를 재는 상태 | 같은 문서 §8 | 1저자 (기록 없음 — 확인) |
| 언로딩 키트 접합 (T12) | 세대 2 의 서보 끝 = 언로딩 키트 판독기 · 관문이 읽는다 — 키트 재확인 GO 가 선행 | 같은 문서 · §5-4 | 언로딩 GO 뒤 |
| ibb 순서 (Q16) | 진행 중인 것 먼저 · 세대 2 자격 런은 빈 코어 · 다른 job 은 끄지 않는다 | 같은 문서 §8 | — |

### 5-6. MPM/FAM 플래튼

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| §12-6 (10-03) | `f = 0` 적격 (t_0 25.842 µm · I_0 거짓) · f_(a) `EXECUTION_FAILED` → 네 칸 · 순서 미배정 (I_b 값만) | `docs/reviews/fam_platen_prereg_20260812.md` §12-6 | — |
| §12-7 | gabia (A6000 48 GB · 확인 런 1 + corner 3) = 딴 시뮬 끝난 뒤 · 그 결과를 본 뒤의 등록 | 같은 문서 | ⚠ 10-20 Q15 = *"gabia = Rint · 214 뒤"* · 10-23 gabia = Rint R 배정 (§6) → 시점 = 1저자 |
| DO-NOT | MPM 을 "진짜 300 MPa 에 닿게" 만들려 하지 않는다 (R1 반증 · ② AM 하중분담이 병목) | `CLAUDE.md` 머리 DO-NOT | — |

### 5-7. SDCP 원고 · SI

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| 값 | SBE σ_e 1.6209 · DBE 보정 σ_VGCF 2.618 (8 팔 σ_e 4.729 mS/cm · +1.0 %) · 이온 σ₀ 앵커 · 원고 · SI 값 = 1저자 10-20 닫음 | `docs/reviews/ms_change_checklist_sdcp_v2_20261019.md` · `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md` | 원고 반영 = 1저자 (요청 때만) |
| 다음 세대 침대 (VGCF E 100 GPa 재압밀) | Rint ② 쪽 (kgy) | — | Claude |

### 5-8. 기타

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| 5:5 SUS 대칭셀 σ_e | 대조만 (10-20 Q14) | 진행 기록 10-20 22 | — |
| 10/21 덱 정정 | 1저자 자료 대기 (10-20 Q16) · 그 뒤 기록 없음 | 진행 기록 10-20 22 | 1저자에게 확인 |
| 보고자료 원칙 | 한글 글꼴 KoPubWorld돋움체 ↔ 맑은 고딕 = 1저자 결정 대기 | `docs/report_making_principles.md` | 1저자 |
| 세미나 덱 | 내용 GO (10-15) · PowerPoint 확인 = 1저자 직접 (추적 닫음) | `docs/reviews/codex_review_seminar_v33_closure_20261015.md` | — |
| ps45 σ_e PC ↔ SC 문헌 | 나중 (1저자 10-13) | `docs/data/ps45_r45_network_g2_20261007/README.md` | — |
| litdb | 정본 = `origin/claude/friendly-meitner-lldvar` 의 `litdb/` · 중복 확인 = `papers/` 파일 목록 (INDEX 아님) · 원문 (SI 포함) 으로 확인 안 된 서지 · 값 = `[미확인]` | `CLAUDE.md` litdb 절 · 규율 ⑥ | 카드는 쪽지로 (정본 가지 push 는 네 규칙 밖) |
| 원장 | 815 항목 · open 283 (Rint 포함) | `docs/reviews/findings.json` (`fdb48d378`) | 네 트랙 항목만 |

## 6. 기계

| 기계 | 배정 |
|---|---|
| kgy · gabia | Rint R 캠페인 (1저자 10-23) |
| v100 | 유료 — 1저자가 하라고 할 때만 |
| ibb | DEM · SLURM · 1저자 운영 |
| WSL (1저자 PC) | 사전 점검 · 수확 · 웹앱 (:5002) |

- 네 트랙이 기계를 써야 하면 명령 · 결과 전 기대를 준비하고 1저자에게 배정 · 실행을 요청한다.  주소는 리포에 적지 않는다.

## 7. 규칙 요약 (정본 = `CLAUDE.md`)

- 보고 → 설명 → 비준 → 실행.  단계 시작 전 1저자 승인 · 끝나면 알림.  등록이 정하지 않은 자리는 고르지 말고 묻는다.
- 보고 = `[트랙]` 머리 · 표 · 담백하게.  1저자가 "용훈 포메이션으로 정리해줘" 하면 `CLAUDE.md` 의 그 틀.
- 시험 먼저 (고치기 전 판에서 실패 확인) → 고침 → 커밋 하나.
- 숫자 · 전칭은 실행 출력으로만 (`SELF-124`) · 철회값 (`docs/reviews/claims.json` `quotation_ban`) 쓰지 않음 · 사전등록 창을 결과 보고 옮기지 않음.
- python `-I` · BLAS 스레드 1 · 무거운 실행 `nice` · 받은 zip · PDF = 새 폴더에 두고 `-I` 로 읽기.
- 멈춘 LIGGGHTS 런 재개 = `scripts/resume_ckpt.sh` 만 (`docs/resume_ckpt_procedure_20260927.md`).
- 코드 → 웹앱 순차 반영 (같은 묶음 · J20-l).

## 8. 첫 할 일

1. `CLAUDE.md` (머리 표 · DO-NOT · 작업 규율 · ★ 사전 공격 리뷰) · 이 문서 · §5 정본 문서를 읽는다.
2. §5 표를 저장소와 대조해 다른 곳을 첫 쪽지 (§3) 로 남기고 1저자에게도 보고한다.
3. 1저자에게 트랙 순서 (§9 Q1) 를 받고 첫 단계를 승인받아 시작한다.

## 9. 사용자가 정할 것

- **[Rint 외 전체] Q1** 트랙 순서 — 권고: ① 언로딩 `ULPR` 고치기 (작고 발송 직전) ② LHS214 다시 발사 독립 사전 리뷰 (Codex 가 쓰지 않은 묶음이라 독립) ③ DEM 프로토콜 세대 2 설계 검토 요청서 ④ 믹서 `MXD2` 고치기 ⑤ D3 설계 v2 ⑥ 후막 8 · v1.3 = 214 뒤.
- **[FAM] Q2** §12-7 (gabia) — 권고: Rint R 이 끝난 뒤.
