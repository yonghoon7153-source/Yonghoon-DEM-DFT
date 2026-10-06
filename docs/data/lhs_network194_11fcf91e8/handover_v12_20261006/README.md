# 194 망 배치 — 인계 v1.2 · 봉인 감사 · 다시 읽기 검산 (2026-10-06)

- 무엇: Codex 4차 재검증 (`docs/reviews/codex_review_rglr2_reverify_20261005.md`) §8 의 4 (실제 194 증거).  배치 `11fcf91e8` 결과 (`docs/data/lhs_network194_11fcf91e8/`) 에서 **고친 생성기** (RGLR3-02 = `74ef3c8a7` · 체크아웃 `061ec1b58`) 로 인계표를 다시 만들었다.  **배치는 다시 돌리지 않았다** (실행 등록 `docs/reviews/lhs_network_batch_registration_20261005.md` §7).
- 생성 = 1저자 WSL 10-06 02:11 KST — 명령 · 출력 그대로 `wsl_run_20261006.md`.
- ✅ **Codex 5차 (10-06 · `docs/reviews/codex_review_rglr3_reverify_20261006.md`) = 이 고정 194 행 (아래 두 CSV sha256) 은 모델 내부 ML 기술자로 조건부 인계 GO** — 판정문 §6 사용 설명 (§7 README 문안) 동봉 · Hertz = 기본 지표 · Physics = 면적 + 협착 규약의 결합 민감도 (기본 학습 열 제외 · opt-in) · 재실행 불요.  실험 절대값 타깃 · 실물 순위 · COMSOL 물성 대입은 HOLD.
- ⚠ **`reread_v12.py` 의 PASS 는 자동 배포 관문이 아니다** — C4 가 공통 칸 차이를 실패로 안 세고 (`RGLR4-01`) C8 이 케이스 ID 집합을 안 본다 (`RGLR4-02`).  이 고정본은 Codex 독립 대조 (공통 36,600 칸 차이 0 · 봉인 감사 고유 194 · record hash 일치) 로 따로 확인됐다.
  ↪ **검산기 수정 (10-06 · 반례 먼저 — `scripts/test_reread_v12.py` 옛 검산기 2 PASS · 10 FAIL → 13/13)**: C4 = diff 칸 · 등록 안 된 탈락 열 · 짝 없는 행이면 **실패** (의도된 변화는 세대별 허용 목록 `C4_ALLOWED` — 열마다 기대 칸 수 · v1.2 = 빈 목록) ·
  C6 = 행 수 = 표 행 수 · 케이스 중복 0 · C8 = 케이스 중복 0 · 집합 = 인계표 두 코호트 = 등록 manifest `plan.queue` · 코호트 · record 상태 = 병합 기록 · record sha256 = 병합 기록 정규 JSON (194/194).
  고친 검산기로 이 폴더를 다시 돌려도 **PASS** (C4 차이 0 · C8 고유 194 · record sha 일치 194).  아래 표 · `reread_20261006.json` 은 **옛 검산기** 실행 기록이다 (그대로 둔다).
  ⛔ 고친 뒤에도 자동 배포 관문으로 쓰지 않는다 (Codex 5차 QV1 — 검산 도구).
  ↪ **검산기 수정 2 — `G2RR-03` (10-06 밤 · Codex 세대 2 재검증 §5 · 1저자 비준 *"권고대로"* · 반례 먼저 — `scripts/test_reread_v12.py` 옛 검산기 17 PASS · 5 FAIL → 22/22)**: 옛 C8 은 등록 큐가 비거나 (`plan.queue = []`) · 없거나 (`plan` · `queue` 키 삭제 · `null`) · 첫 ID 를 중복 추가해도 (194 + 1 행) PASS · rc 0 이었다.
  이제 C8 = `registration_queue()` 가 큐를 **dict 로 바꾸기 전에** 검사 (비지 않은 목록 · 행 형식 · 원 행 수 194 · ID 중복 0 · 코호트 lhs 130 · lhsx 64 = 인계표 · 행마다 코호트 = 인계표 · 케이스 집합 = 인계표) · 빈 큐에서도 감사표 ↔ 큐 집합 비교 ·
  큐 코호트가 없는 감사표 행 = 실패 · 그 병합 기록은 대조 안 함 (인계표로 대체하지 않는다) · 출력 `queue_n` = 큐 원 행 수 + `queue_n_unique` · `queue_cohorts` · `record_unreferenced`.  Codex 탐침 (`docs/reviews/codex_gen2_network_reverify_evidence_20261006/probes/reread_extra.py` 무변경 사본) = 정상 큐 rc 0 · 세 변이 rc 1.
  고친 검산기로 이 폴더를 다시 돌려도 **PASS** (C4 24,440 + 12,160 칸 같음 · C7 130 + 64 · C8 194 행 · 고유 194 · 등록 큐 194 = lhs 130 · lhsx 64 · record sha 194 · 문제 0 — 옛 검산기 출력과 다른 것은 새 C8 필드 셋뿐) · `--seal-audit` 은 그대로 선택 · v1.2 값 · 자료 파일 변경 없음.

## 파일

| 파일 | 무엇 |
|---|---|
| `lhs_handover_v12_20261006.csv` · `lhsx_handover_v12_20261006.csv` | 인계표 130 × 251 · 64 × 253 (key `case` 포함) |
| `*_columns.tsv` | 열 사전 (열마다 뜻 · 출처 · 한정어) |
| `*_tau_provenance.tsv` | τ 출처 부록 — 케이스마다 run id · 입력 digest · 원천 sha256 · 같은 세대 검사 `P0_records;P1_run_id;P2_input_digest;P3_batch_tie;P4_stop_contract;P4_generation;P4_read_stable` · 근거 `current_files_no_publish_hash` |
| `*_excluded.tsv` | 명시 제외 6 패턴 (LW ④b = frame_unverified · `path_hop_area_*` · δ 판 파괴 · 상 쌍별 파괴 · physics 면적 · `tortuosity_dijkstra_SE`) |
| `seal_audit.tsv` | 봉인 감사 (`scripts/run_network_194_parallel.py audit`) 194 행 |
| `net194_tau_sources_20261006.tar.gz` | τ 원천 — 케이스마다 `network_conductivity_dual.json` · `full_metrics.json` · `network_provenance.json` (582 파일 · 독립 재계산용) |
| `reread_v12.py` · `reread_20261006.json` | 다시 읽기 검산기 · 결과 (이 폴더 기준으로 다시 돌린 것) |
| `wsl_run_20261006.md` | WSL 실행 기록 · 두 묶음 sha256 |
| `tau_below1_check.py` | Physics 수송 tortuosity < 1 원인 점검 (`merged/*/metrics_flat.csv` 만 · 같은 망의 CONTACT_FREE 해 · 협착 전력 몫) — 요청서 §6-3 의 7 의 숫자 |

## 다시 읽기 검산 — **PASS** (실패 0)

| 검사 | LHS 130 | LHSx 64 |
|---|---|---|
| C1 행 = 배치 `metrics_flat` 집합 · 중복 | 130 · 0 | 64 · 0 |
| C2 LW 열 (`stress_lw_*` · `stress_cv_lw*` · `stress_ratio_*_lw*`) · 제외 노트 frame_unverified | 0 · 있음 | 0 · 있음 |
| C3 열 사전 ↔ 표 열 · 빈 뜻 | 251 = 251 · 0 | 253 = 253 · 0 |
| C4 옛 인계 (`docs/data/lhs_handover_20261001.csv` · `lhsx_…` = d1ec42fba 접촉 배치) 와 공통 열 값 | 188 열 · **24,440 칸 같음** · 차이 0 | 190 열 · **12,160 칸 같음** · 차이 0 |
| C4 새 열 · 빠진 열 | 62 (⑤⑥⑦ 34 + 망 τ 묶음 28) · 0 | 62 · 0 |
| C5 τ 상태 Hertz | OK 106 · NOT_PERCOLATING 24 | OK 64 |
| C5 τ 상태 Physics | OK 106 · NOT_PERCOLATING 24 | OK 54 · **MODEL_BELOW_CONTINUUM_BOUND 10** |
| C5 NOT_COMPUTED · BAND_FALLBACK | 0 · 0 | 0 · 0 |
| C5 값 — metrics_flat 에서 다시 계산 (상대 1e-9) · tau = √tau2 · OK ⇒ ≥ 1 · MBCB ⇒ < 1 · 비관통 f = 0 · tau2 빈칸 | 어긋남 0 | 어긋남 0 |
| C5 비관통 집합 = 퍼콜 감사 `se_perc_webapp_dump` (`docs/data/lhs_perc_audit_20261001/`) | 같음 (24) | 같음 (0) |
| C5 공통 메타 σ₀ · T · φ 기준 · L 기준 | 3.0 mS/cm · 25 °C · mass_conserving · L_mc | 같음 |
| C6 출처 부록 = 표 집합 · run id = 배치 status · `tau_flux.py` sha256 = 발사 봉인 | 130 · 어긋남 0 | 64 · 어긋남 0 |
| C7 원천 sha256 = 출처 부록 · 원천에서 생성기와 같은 식 (`tau_flux.ion_columns`) 을 다시 불러 = 표 칸 (완전 일치 · 자료 경로 독립 · 식 독립 검산은 C5 — `SELF-90`) | 130 / 130 | 64 / 64 |
| C8 봉인 감사 | 194 행 = **SEALED_LEGACY 194** · merged = 케이스 폴더 **194 같음** | (공통) |

- MODEL_BELOW_CONTINUUM_BOUND 10 = `lhsx_048` · `050` · `051` · `053` · `054` · `060` · `061` · `062` · `063` · `064` (Physics 수송 tortuosity 0.89–1.00 · 값 유지 + 표지).  같은 10 건의 Hertz = 1.25–1.39.  원인 분석 = 요청서 §6-3 의 7.
- `stress_cv` 계열 (옛 σ_VM · `LHS-33`) 은 이 인계표에 **없다** (10-01 판에도 없었다 — 빠진 열 0).

## 재현 (리포 뿌리 · Linux)

```bash
mkdir -p /tmp/net194_tau && tar -xzf docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz -C /tmp/net194_tau
python3 docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/reread_v12.py \
  --handover-dir docs/data/lhs_network194_11fcf91e8/handover_v12_20261006 \
  --seal-audit docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/seal_audit.tsv \
  --tau-sources /tmp/net194_tau --out /tmp/reread.json
```

## 한정

- 같은 세대 검사의 근거는 **지금 파일들** (`current_files_no_publish_hash`) — 모든 사본을 일관되게 고친 변조는 게시 때 해시 없이는 잡지 못한다.
- 이 검산은 생성된 표를 커밋된 배치 증거 · τ 원천과 대조한 것이다 — 망을 다시 푼 것이 아니다.
- 값의 지위: ML 기술자 (이 모델 안 상대 비교) · 실험 절대 대조 HOLD (`docs/reviews/codex_lhs_release_final_verdict_20261001.md`) · σ₀ = 펠릿값 3.0 mS/cm.
