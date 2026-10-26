# 우리 트리 재현 — Codex Rint ② 재검토 회차 ① (10-26)

- 무엇을: 판정문 §3 · §6 의 탐침 셋을 **고치지 않고** 다시 돌렸다 — `docs/reviews/codex_rint2_rr_round1_evidence_20261026/evidence/agent_sv/probe_actual.py` · `docs/reviews/codex_rint2_rr_round1_evidence_20261026/evidence/agent_sv/probe_weighted.py` · `docs/reviews/codex_rint2_rr_round1_evidence_20261026/evidence/agent_runtime/probe_diagnostic_overflow.py`.
- 우리 트리 = 묶음 복사본의 `repo/` 자리에 핀 `9bec6b764` 의 `scripts/` 를 `git archive` 로 넣음 (HEAD `20651fd36` 의 `scripts` 트리 id 와 같다 — 그 사이 커밋은 문서뿐).  탐침이 import 하는 생산 모듈은 이 사본만 쓴다.
- 환경 (우리) = Linux · Python 3.11.17 · numpy 2.4.6 · scipy 1.17.1 · OPENBLAS / OMP / MKL 1 스레드.  환경 (Codex) = Windows · Python 3.12.14 · numpy 2.5.3 · scipy 1.16.3.
- 세 탐침 모두 rc 0.  `probe_actual.py` 안의 단언 (정직한 기록 · 바꿔치기 기록 둘 다 `ca_ext_record_ok = (True, None)` · 문턱 1.01 에서 정직 = `SV_DEPENDENT` · 바꿔치기 = `[]` · 모든 `n_*` 칸 그대로 · 주 증서 결합 같음) 이 우리 환경에서도 그대로 성립했다.

## 결과 (`comparison.json`)

| Codex 출력 | 잎 | 같음 | 숫자만 다름 (최대 상대 차) | 그 밖 다름 |
|---|---:|---:|---|---|
| `docs/reviews/codex_rint2_rr_round1_evidence_20261026/evidence/agent_sv/probe_actual_results.json` | 165 | 147 | 11 (4.94 × 10⁻¹⁴) | 7 = 산출 파일 sha256 4 (숫자 끝자리 때문) + 환경 판 3 |
| `docs/reviews/codex_rint2_rr_round1_evidence_20261026/evidence/agent_sv/weighted_graph_results.json` | 21 | 21 | 0 | 0 — 정확 유리수 소거 비 1.0170715052190031 같음 |
| `docs/reviews/codex_rint2_rr_round1_evidence_20261026/evidence/agent_sv/k0_honest_manifest.json` | 303 | 286 | 17 (해 잔차 `resid` 2.5 × 10⁻¹⁶ ↔ 2.4 × 10⁻¹⁶ 만 2.9 × 10⁻² · 나머지 ≤ 1.1 × 10⁻¹⁵) | 0 |
| `docs/reviews/codex_rint2_rr_round1_evidence_20261026/evidence/agent_sv/k0_swapped_manifest.json` | 303 | 285 | 18 (같은 꼴) | 0 |
| `docs/reviews/codex_rint2_rr_round1_evidence_20261026/evidence/agent_sv/k0_assembled_systems.json` | 1,251 | 1,251 | 0 | 0 — 조립된 행렬 항 그대로 |
| `docs/reviews/codex_rint2_rr_round1_evidence_20261026/evidence/agent_runtime/diagnostic_overflow.json` | 15 | 14 | 0 | 1 = 실행 경로 문자열 |

- 판정값 (`docs/reviews/codex_rint2_rr_round1_evidence_20261026/evidence/agent_sv/probe_actual_results.json` 의 flags · run_contract · problem · status 잎 20) = **20 / 20 같음**.
- 숫자 차 = CG · spsolve 반올림 끝자리 (기계 · 라이브러리 판) — 판정에 닿는 값은 없다.
- 우리 실행이 쓴 산출 JSON 은 리포에 넣지 않았다 (sha256 = `comparison.json` 의 `ours_sha256`).  로그 셋 = 이 폴더 `*.ours.log`.

⇒ **판정값 차이 0** (RR1-01 의 k=0 증서 바꿔치기 거짓 clear · RR1-02 의 진단 합 넘침 경고 · RCA2-01 옛 문턱 반례가 지금 `SV_DEPENDENT`).
