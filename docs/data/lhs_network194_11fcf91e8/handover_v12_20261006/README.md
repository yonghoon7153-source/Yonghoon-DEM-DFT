# 194 망 배치 — 인계 v1.2 · 봉인 감사 · 다시 읽기 검산 (2026-10-06)

- 무엇: Codex 4차 재검증 (`docs/reviews/codex_review_rglr2_reverify_20261005.md`) §8 의 4 (실제 194 증거).  배치 `11fcf91e8` 결과 (`docs/data/lhs_network194_11fcf91e8/`) 에서 **고친 생성기** (RGLR3-02 = `74ef3c8a7` · 체크아웃 `061ec1b58`) 로 인계표를 다시 만들었다.  **배치는 다시 돌리지 않았다** (실행 등록 `docs/reviews/lhs_network_batch_registration_20261005.md` §7).
- 생성 = 1저자 WSL 10-06 02:11 KST — 명령 · 출력 그대로 `wsl_run_20261006.md`.
- ⛔ **배포 전** — 수영 님 전달은 Codex 5차 GO 뒤 (요청서 `docs/reviews/codex_rglr3_reverify_request_20261006.md`).

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
| C7 원천 sha256 = 출처 부록 · `tau_flux.ion_columns` 독립 재계산 = 표 칸 (완전 일치) | 130 / 130 | 64 / 64 |
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
