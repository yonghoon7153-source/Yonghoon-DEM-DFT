# Codex 4차 재검증 탐침 — 고친 트리 재실행 (RGLR3-01 · 02 · 03 · 2026-10-06)

- 기준 판정: `docs/reviews/codex_review_rglr2_reverify_20261005.md` (핀 `11fcf91e8` · 새 P2 `RGLR3-01` retry 가 같은 HEAD dirty 코드를 안 막는다 · `RGLR3-02` τ 인계 로더가 띠 규칙 · σ₀ 사본 불일치를 수용 · P3 `RGLR3-03` 후속 명령에 τ 없음).
- 고친 커밋: `0c48297f9` (RGLR3-01 · 03 — `scripts/run_network_194_parallel.py`) · `74ef3c8a7` (RGLR3-02 — `scripts/lhs_design_dataset.py` τ 로더 P4) · 기록 `061ec1b58`.  재실행 트리 = `061ec1b58` (`source_rev.json` · 판정 묶음과 같은 456 경로 · 빠진 경로 0).
- 방법: 판정 묶음 `docs/reviews/codex_rglr2_reverify_review_evidence_20261005/` (source 는 manifest 만 커밋) 을 복사하고 source/ 를 고친 트리의 같은 경로로 채워 **묶음의 실행기 그대로** 돌린다 — `drive_fix_probe.py` 한 번.
  탐침 `new_probes.py` 는 결함이 **있음을** 단언한다 (고친 트리에서 AssertionError 가 정상) → 결함 단언 두 줄만 뒤집은 사본 `new_probes_after_fix.py` (원본과 40 · 79 행 · 출력 파일 이름만 다름 · 사본은 스크립트가 원본에서 만든다).

```bash
python3 docs/reviews/codex_rglr3_fix_probe_rerun_20261006/drive_fix_probe.py /tmp/rglr3_probe_rerun     # 기대 rc: 7 탐침 0 · 사본 0 · 원본 1
```

## 결과 (Linux · Python 3.11 · `drive_fix_probe.py` rc 0)

| 사례 | 핀 `11fcf91e8` (Codex) | 고친 트리 `061ec1b58` |
|---|---|---|
| τ 로더 — 띠 규칙 dual 만 L0 → L1 (RGLR3-02) | 수용 (OK) | **인계 전체 거부** (FillRefusal · P4: 망 정지 계약 재검사 ⑥ 모드 파일 ↔ dual 사본 불일치) |
| τ 로더 — σ₀ ×2 dual 만 (σ_dim 재계산 · RGLR3-02) | 수용 (OK) | **인계 전체 거부** (P4 ⑥ 같은 사유) |
| τ 로더 — atoms 입력 변조 · σ_ratio ×4 dual 만 · run id 불일치 | 거부 (P2 · P3 · P1) | 거부 (그대로) |
| τ 로더 — 정상 (baseline) | 수용 | 수용 (그대로) |
| retry — 같은 HEAD · 봉인 파일 dirty (`scripts/network_conductivity.py`) (RGLR3-01) | rc 0 · 워커 실행 · run_002 기록 | **rc 2 · 워커 안 띄움 · run_002 없음** — 사유 "세대: 코드가 발사 봉인과 다르다 (HEAD 가 같아도)" · "dirty: 추적 파일이 바뀐 트리" (`new_probes_after_fix.log` 끝) |
| merge (시도 사이 지금 트리만 바뀜) | rc 0 · `code_changed_since_launch` 기록 | 그대로 (rc 0 · 정보로 기록) |
| 후속 명령 (RGLR3-03) | τ 없음 | ⓪ 봉인 감사 · ① τ 진단 표 · ② 생성기 `--webapp-groups …,tau --tau-results` · ③ 묶음에 인계 파일 · 봉인 감사 · ③b τ 원천 (`new_probes_after_fix.json` → `launcher.followups`) |
| 실행 등록 19 파일 sha256 | 19 / 19 | 19 / 19 |
| VM 정확 유리수 검산 5,000 | 경계 위반 0 | 그대로 |
| 나머지 독립 탐침 7 (network_adversarial · lw_replay · vm_boundary · precision_boundary · raw18 · handover_replay · handover_before_after) | rc 0 | **rc 0** (`probe_summary.json`) |
| 원본 `new_probes.py` | rc 0 | **rc 1** (40 행 AssertionError = 결함이 없어졌다 · `new_probes_original.log`) |

## 한정

- P4 가 dual-only 변조를 막는 근거는 **사본 불일치** (모드 파일 · legacy ↔ dual) 다 — 모든 사본을 일관되게 고친 변조는 게시 때 해시 없이는 못 잡는다 (출처 부록 `same_generation_basis = current_files_no_publish_hash`).  일관된 띠 규칙 변경은 상태 칸 (BAND_FALLBACK) 으로 드러난다.
- 실제 194 의 증거는 따로: 봉인 감사 · 인계 v1.2 · 다시 읽기 검산 = `docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/`.
- 이 재실행은 판정 묶음의 합성 fixture 위에서다 — 생산 배치를 돌리지 않았다.
