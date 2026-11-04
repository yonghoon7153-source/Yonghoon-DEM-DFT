# Codex 작업창 인계 — 비 Rint 트랙 구현 (2026-11-04 · 1저자 비준 *"권고대로 해"*)

> 이 글 = Codex 작업창에 붙여 넣는 프롬프트이자 인계 문서다.  같은 글이 중심 가지 `claude/stoic-knuth-NObVQ` 에 `docs/handoff_codex_nonrint_20261104.md` 로 들어간다 (Claude 의 다음 게이트 뒤).  그 전에는 이 글이 정본이다.
>
> ⚠ **정정 (11-04 · 리포 반입 판)** — 처음 보낸 판의 §3-3 (D3) 이 10-21 시점 상태로 낡아 있었다 (Claude 쪽 확인 누락 · Codex 첫 답이 지적).  리포 판에서 §3-3 을 고치고, 그 뒤 사실 셋 (§1 의 기준 커밋 push · §3-1 ② 의 Claude 쪽지 · §4 순서) 을 더했다.  나머지 문장은 보낸 판 그대로다.

## 0. 역할 (11-04 부터)

| 누구 | 맡는 것 |
|---|---|
| **Codex DEM 실무 창 (이 창)** | 비 Rint 트랙의 **구현 · 수정 · 등록 초안 · 실행 명령 준비** — LHS · 믹서 (D2 · D3 · MXD2R) · (잠잠한) P1 언로딩 · 세대 2 / T12 |
| **Codex 반박 리뷰 창 (따로 있다)** | 독립 반박 리뷰 — 반례 재현 · 변이 시험 · 과장된 결론 · 누락 조건.  이 창이 만든 것도 그 창이 리뷰한다 (이 창은 자기 작업을 스스로 닫지 않는다) |
| Claude 본 세션 | Rint ② · gabia (FAM §12-7 발사 · Rint R 환경) · 50kg / DEM1 watch · **통합** (cherry-pick · 원장 · 진행 기록 · CLAUDE.md) |

### 0-1. 반박 리뷰 창을 잘 쓰는 법 (1저자 11-04 — *"실무 하는 곳과 반박하는 곳은 따로 있으니 잘 활용"*)

- **단위마다 보낸다** — 고침 하나 · 등록 하나 · 판정 하나 · 배포 요청 하나가 끝나면 반박 리뷰용 요청서 + ZIP 을 만든다 (발송 = 1저자).  큰 묶음을 오래 쌓지 않는다.
- 요청서 꼴 = 맨 위 *"이번에 닫는 것 / 닫지 않는 것"* · 리뷰 핀 = 이 창 가지의 **push 된** 커밋 · ZIP = 핀의 blob 그대로 + `PIN.txt` · 질문은 번호로 · 사전 공격 ①–④ 를 먼저 하고 그 결과 (한정) 를 요청서에 적는다.
- 판정문이 오면: 판정문 · 증거 반입 → 우리 트리에서 반례 재현 (`_repro_ours_<날짜>/` · 판정값 차이) → 원장 항목은 쪽지로 → 수정 계획 (Q 번호 + 권고) → 1저자 비준 → 시험 먼저 고침 → 짧은 재확인 요청.
- 리뷰 창의 GO 범위를 넓혀 읽지 않는다 (예: *"발사 확인 범위 GO"* ≠ 배포 GO).  GO 아래로 발사 · 배포 기준을 낮추는 안을 내지 않는다.
- 리뷰 순서가 Rint 회차 ② 와 겹치면 순서는 1저자가 정한다.

- 10-27 의 *"Codex = 반박 리뷰만"* 에서 바뀌었다 — 위 표의 트랙에 한해 이 창이 구현한다 (1저자 11-04).
- Rint ② · 50kg 의 결과 · 승인을 이 트랙에 자동 적용하지 않는다 (반대도 같다).

## 1. 가지 · 충돌 없는 합치기 규칙

1. 기준 = `origin/claude/stoic-knuth-NObVQ` 끝 (11-04 오전 = `7b51e591e` → 11-04 낮 Claude 게이트 통과 뒤 push = `74150affc` — FAM prereg 한 파일만 바뀜 · 이 트랙과 무관 · 다시 맞출 필요 없음).
2. 새 가지만 쓴다: `codex/lhs-v13-1104` · `codex/mixer-1104` (트랙마다 하나).  `claude/*` 에 push · 병합하지 않는다.  옛 `codex/*` 가지는 보존 (정본 아님).
3. **파일 주인** — 이 창이 고치는 파일 = 자기 트랙 것만: `scripts/lhs_*` · `scripts/mixer_*` · `scripts/make_mixer_deck.py` · 해당 시험 · `docs/data/lhs_*` · `docs/data/mixer_*` · `docs/reviews/*lhs*` · `docs/reviews/*mixer*` · `docs/reviews/mxd2*` · 트랙 증거 폴더.
4. **공유 파일 넷은 고치지 않는다** — `docs/reviews/findings.json` (원장) · `docs/session_20260923_progress.md` (진행 기록) · `CLAUDE.md` · 웹앱 공통 (`webapp/app.py` · `webapp/templates/base*`).  대신 **쪽지** `docs/collab/codex_to_claude/<YYYYMMDD-HHMM>_<주제>.md` 에: ① 커밋 목록 (자기 가지 SHA) ② 원장에 넣을 항목 (JSON 조각 · 형식 = `json.dumps(indent=2, ensure_ascii=False)` · claimed_fixed 면 `claimed_fixed_sha` + `evidence_tests`) ③ 진행 기록 줄 ④ CLAUDE.md 줄 제안.  쪽지 규칙 = `docs/collab/README.md`.
5. 합치기 = Claude: `cherry-pick -x` → 옛 → 새 SHA 대응 → 쪽지 반영 → 전체 게이트 (`scripts/check_all.sh`) → push.  그래서 문서 안 SHA 는 *"(본 가지 번호 = 반입 때)"* 로 비워 두거나 자기 가지 SHA 를 쪽지에만 적는다.
6. 넘기기 전 최소 검사: `python3 scripts/check_doc_refs.py` · `python3 scripts/check_review_findings.py` (원장을 안 고쳤어도) · 바뀐 시험 전부.

## 2. 일하는 규칙 (CLAUDE.md 그대로 — 요점)

- 보고 → 설명 → 비준 → 실행.  1저자에게 묻는 것은 `[트랙] Q 번호` + 권고 한 줄.  답은 한국어 · 표 중심 · 짧게.
- 시험 먼저 (고치기 전 실패를 기록) · 숫자는 실행 출력과 원문에서만 · 전칭 (*"전부"* · *"N/N"* · *"바이트 같음"*) 은 대조한 범위와 함께.
- Codex 반박 리뷰에 보내기 전 사전 공격 ①–④ (숫자 · 전칭 대조 · HOLD 부류 · 독립 반례 · 맨 위 *"이번에 닫는 것 / 닫지 않는 것"*).
- **실제 계산 (WSL · ibb 실행 · 제출 · 재제출) · 등록값 변경 = 1저자 결정 뒤에만.**  명령은 1저자가 붙여 넣기 쉽게: 실제 경로를 채운 **파일 하나** (1저자 = TeamViewer · 영문 입력) — 멈춤 조건 · 기대 화면 · 돌려받을 묶음을 함께.
- 원본 · 실패 시도 폴더는 지우지 않는다 (이름 바꿔 보존).  호스트 주소 · 포트는 리포에 적지 않는다.
- 모델 이름을 커밋 · 문서 어디에도 쓰지 않는다.

## 3. 트랙별 지금 상태 · 할 일

### 3-1. LHS — v1.3 (§5 판정 · 압력 기록 · 인계표) — 정본 `docs/data/lhs_network214_35f032737_20261030/s5_judgment/README.md` §11

**11-04 WSL 결과 (1저자 실험실 PC · 아직 리포에 없음 → 첫 커밋에서 기록 반입)**

| 단계 | 결과 |
|---|---|
| ① Q1 확정 (§11-1 (e)) | `lhs00_123` **INCLUDE** rc 0 (FULL Δ_전극 1.5297e-05 · 결과 전 기대 1e-5–4e-5 안) · `lhsx_026` **HOLD** rc 3 — B 거짓의 원인 = **반올림 칼날**: full 가지 옛 전극 `0.42381246501935615` ↔ v1.2 기록 `0.42381246` (8 자리) · 차 5.0194e-9 > 도구 허용 `HALF 5e-9 + 1e-12` (1.9e-11 넘음) · bulk_only · constriction_only 는 재현 · Δ_전극 FULL **1.5230e-4** (결과 전 기대 구간 (1.5226e-4, 1.5231e-4) 안 · 설계 기록 어림 ≤ 1.5e-4 보다 1.5 % 큼) · 묶음 `q1_settle_20261104.tar.gz` (2,333 B · 1저자 다운로드 폴더 → 받아서 반입) |
| **1저자 Q7 = (가)** (11-04) | `lhsx_026` 을 싣는다 — 등록 §5-7 *"그 밖의 차이는 보고하고 원인을 밝힌 뒤에만 싣는다"* · 원인 (전극 모형뿐 · 재현 칼날 1.9e-11) 과 Δ 를 §5-7 결과 칸에 적는다 · 도구 규칙은 사후에 바꾸지 않는다 |
| **1저자 Q6 = (가)** (11-04) | 봉인 인계 도구 그대로 · v1.3 배포 README 정오에 실측 최대 1.5228e-4 (`lhsx_026`) 와 출처 (§11-1 (a)) |
| ② 단계 A (§11-3) | 사전 점검 ✓ (manifest · seal_audit · reread sha · handover_code_hashes · 결과 폴더 130 · 64 · 20) → **압력 기록 214/214 REFUSED** → §11-4 관문이 등록대로 멈춤 (인계표 안 만듦) |
| 거부 꼴 | `lhs00_000`–`099` (100) · `lhsx_001`–`064` (64) = *"판정 줄 (Current Pressure: …) 이 있는 로그가 없다 (후보 0)"* · `lhs00_100`–`129` (30) = *"판정 줄이 있는 로그가 둘 이상 (['log.liggghts', 'log.txt'])"* · `lhss_001`–`020` (20) = *"… 없다 (후보 1)"* |
| 남은 파일 (보존) | 거부 TSV 셋 = 1저자 WSL `~/net194_35f032737_1028/pressure/{lhs,lhsx}_pressure_record.tsv` · `~/netsupp20_35f032737_1028/pressure/lhss_pressure_record.tsv` — 다시 돌리기 전에 이름 바꿔 보존 (사전 점검이 기존 파일을 거부) |
| 쓴 스크립트 | 등록 블록 §11-1 (e) · §11-3 에 경로만 채운 둘 — WSL 자리: `~/dem-audit` (B7 `35f0327377a4213774010a090df4d224e50d29e1` 깨끗) · MAIN = `~/dem-main-7b51e` (`7b51e591e` 작업 트리) · PY = `~/Yonghoon-DEM-DFT/.venv/bin/python3` · R = `~/net194_35f032737_1028` · RS = `~/netsupp20_35f032737_1028` · 다운로드 = `/mnt/c/Users/Administrator/Downloads` |

**할 일 (순서)**: ① Q1 · Q7 · Q6 · 단계 A 거부를 §11 에 기록 (결과 칸 · 화면 요지) ② 압력 기록 거부 원인 — `scripts/lhs_pressure_record.py` (B7 판) 가 찾는 로그 자리 ↔ 수확 폴더 실제 내용 · `Current Pressure:` 줄이 있는 원래 LIGGGHTS 로그의 자리 (ibb · WSL) · log.liggghts / log.txt 쌍 · lhss 로그에 줄이 없는 까닭 → 선택지 + 권고를 1저자에게 (Claude 쪽 분석 = 쪽지 `docs/collab/claude_to_codex/20261104-0233_lhs-pressure-refusal.md` — 원인 셋 · 선택지 A–D · Claude 권고 A · 순서 문제 하나) ③ 1저자 결정 뒤 단계 A 다시 (파일 하나 · 실제 경로) ④ 인계표 수준 §5-7 회귀 ⑤ Codex v1.3 배포 GO 요청서 (발송 = 1저자) ⑥ 1저자 배포 승인 → 수영 님 전달 (`--pressure-unverified` 쓰지 않는다 · OK 아닌 침대를 빼고 만들지 않는다 · §11-4).

### 3-2. 믹서 — MXD2R 짧은 재확인 요청서

- 상태: MXD2R-01–04 (+ neighbor skin 고정) = 중심 가지 반입 · 원장 claimed_fixed · 증거 `docs/reviews/mxd2r_fix_evidence_20261103/` (README · `docs/reviews/mxd2r_fix_evidence_20261103/mxd2r04/README.md` §9 · `docs/reviews/mxd2r_fix_evidence_20261103/mxd2r04/q4_skin/` · `SHA256SUMS`) · 고친 커밋 = `git log --oneline 80095a7f0..7b51e591e -- scripts/mixer_deck_readback.py scripts/mixer_deck_diff.py scripts/mixer_smoke_blind.py scripts/test_mixer_d2_consumers.py`.
- 할 일: 짧은 재확인 요청서 `docs/reviews/codex_mixer_mxd2r_recheck_request_<날짜>.md` (꼴 = `docs/reviews/codex_lhs214cx_fix_recheck_request_20261019.md` · §0 닫는 것 / 닫지 않는 것 · 바뀐 것 · 시험 수 (다시 돌린 값) · 질문 · ZIP 목록 · PIN = ZIP 때 PIN.txt) + 사전 공격 ①②④ → 1저자 발송.

### 3-3. 믹서 — D3 (SE–SE 점착 유동성 실측 앵커)

> ⚠ 11-04 정정 — 처음 보낸 판의 이 절은 10-21 상태였다 (아래가 리포의 실제 흐름).

- 흐름: v1 `docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md` (결과 0 건 · 1저자 Q1–Q12 권고대로) → 10-21 사전 공격 = 설계 보장 14 중 깨짐 8 · 조건부 5 · 선례 위험 1 (`docs/reviews/codex_mixer_d3_design_request_20261021.md` §2-3) → **v2 설계 (10-23)** `docs/reviews/mixer_d3_se_flowability_anchor_design_v2_20261023.md` (요청서 `docs/reviews/codex_mixer_d3_design_v2_request_20261023.md` · 증거 `docs/reviews/mixer_d3_design_v2_evidence_20261023/`) → **후보 판독기 (10-24)** 계약 `docs/reviews/mixer_d3_candidate_reader_contract_20261024.md` (요청서 `docs/reviews/codex_mixer_d3_candidate_reader_request_20261024.md` · 증거 `docs/reviews/mixer_d3_candidate_reader_evidence_20261024/`) → **Codex 10-27 판정** `docs/reviews/codex_mixer_d3_review_20261027/codex_review_mixer_d3_20261027.md` = *"입력 조건부 유한 후보 판독기 범위 GO"* · 새 P1/P2/P3 없음 · 실제 실행 · S1/S3 등록 · 통계 · 물리 타당성 GO 아님 · 독립 출력 전부 `execution_ready=false`.
- 할 일: 최신 문서와 대조해 **남은 범위를 표로 보고** (S1/S3 등록에 필요한 것 · 원자료 · 실측 조건 · `MXD2-07` 상태는 원장에서) → 코드 · 새 문서는 1저자 비준 뒤.  새 물리 · 새 런 없음.

### 3-4. P1 언로딩 · 세대 2 / T12

- 잠잠 — 인계 당시 상태 그대로 (RJ 323957 = `VALUE_MISMATCH` · 재실행 없음 · contact 진단 = 기록 판정만 · ULPRI-01/02 · T12R-01 CLOSED = 범위 한정).  1저자 지시 없이는 손대지 않는다.

## 4. 기한 · 우선순위

- 우선: LHS ② (Claude 쪽지 → `[LHS] Q` → 결정 뒤 실행 파일) → 믹서 MXD2R 요청서 → D3 남은 범위 보고.
- Rint 기한 (Codex GO ≤ 11-20 · 봉인 ≤ 11-21 · R 런 11-22–29) 동안 Codex 로컬 반박 리뷰 세션의 Rint 회차 ② 가 먼저일 수 있다 — 리뷰 순서는 1저자가 정한다.

## 5. 첫 응답으로 할 것

1. 이 글을 읽었다는 확인 + 기준 커밋 (`git rev-parse origin/claude/stoic-knuth-NObVQ`).
2. 트랙별 첫 작업 계획 (용훈 포메이션 꼴 표) + 1저자에게 물을 것 (`[LHS] Q…` · 권고 한 줄).
3. 가지 둘 만들기 (아직 커밋 없이도 됨).
