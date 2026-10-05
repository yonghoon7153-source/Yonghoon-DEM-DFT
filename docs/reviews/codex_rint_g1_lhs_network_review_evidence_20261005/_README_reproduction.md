# Codex RINT G1 · LHS 망 리뷰 — 반입 + 우리 트리 재현 (2026-10-05)

- 판정문: `docs/reviews/codex_review_rint_g1_lhs_network_20261005.md` (= zip 의 `codex_review_rint_g1_lhs_network_20261005.md` · 483 행 · sha256 `593b37d0a189fd8555cf6e879b5b8aa53a3765d3c1d8f5743f28cfbf037d76ab`) — **HOLD · 새 P1 4** (`RGL-01`~`04`) · P2 5 (`RGL-05`~`09`) · P3 1 (`RGL-10`) · G3 (전력 몫 정의 · 경계 추출) 만 한정 GO · 194 건 배치 · 새 봉인 승인 아님.
- 반입 원본: 사용자 전달 zip `codex_rint_g1_lhs_network_review_20261005.zip` — 3,138,836 B · sha256 `e42ccd90b76c15807933d8597f1d24c5853c82a18e535315bd5c04e699472aaa` · 313 파일 · `package_manifest.json` 312/312 일치.
- 핀: `30c8205c5efb3873ae6fa856881fa184bd041d4d` — `source_manifest.json` 의 223 파일 git blob 이 **핀의 blob 과 223/223 같다** (real14 원자 · 접촉 gz 둘은 Codex 미취득 = `missing_binary_fixtures`).
- 이 폴더 = zip 에서 핀 소스 사본 223 개와 아래 7 개를 **뺀** 83 파일 + 우리 재현 기록 `_reproduction_compare_linux.json` · 이 README.
  뺀 것 (sha256 은 그 JSON 의 `excluded_from_repo`): 우리 요청서 사본 · 판정문 원본 (위 경로로 반입) · 합성 payload JSON 4 (`evidence_g1/` 의 normal · wetted · bare · main 미수렴 · 각 ≈ 375 KB — `probe_adversarial.py` 가 재생성) ·
  구식 망 모듈 사본 (`git show eedada5d3:scripts/network_conductivity.py` 와 blob 동일).
  ⇒ 탐침 재실행은 **zip 원본**을 풀어 그 안에서 (이 폴더만으로는 `source/` 가 없어 돌지 않는다 · `verify_snapshot.py` · `package_review.py` 도 zip 기준).

## 우리 트리 재현 — 여덟 탐침 무변경 (Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1)

| 대조 | 결과 |
|---|---|
| 증거 JSON 25 개 (받은 것 ↔ 재현) | **결정값 차이 0** · 미분류 차이 0 — 차이는 전부 `classes` 분류 안 (CG 잔차 상대 ≤ 5.2e-8 · run_id · 시각 · 합성 입력 해시 · 입력 경로 · 환경 · 경로 구분자 · 문자열 실수 1 ULP) |
| evidence_g4/probe.stdout.txt ↔ probe_g4.ours.stdout.txt | same (CR · seconds 제거 뒤) |
| evidence_g23/probe_lw_independent.final.stdout.txt ↔ ours | same |
| evidence_g23/probe_network_independent ↔ ours | old==new 원시 hex: Codex 18/18 True · 우리 18 True · 플랫폼 간 출력 값 최대 상대차 2.24e-11 (같은 플랫폼 안 구·신 비교는 양쪽 다 비트 동일) · not_percolating · independent_power = same |

### 판정의 핵심 값 — 우리 재현에서 읽은 값 (손으로 옮기지 않고 재현 JSON · stdout 에서 뽑음)

| 원장 | 양 | 우리 재현 |
|---|---|---|
| `RGL-01` | 보조 σ 정상 / wetted 반복 1 회 / bare 반복 1 회 (S/cm) · R_geom (Ω·cm²) · collector · check-arm | 0.0009487 / 0.007179 / 0.007179 · 0.0 / 3.8 / 0.0 · complete · complete · rc 0 · 0 (주 σ_e 그대로 True) |
| `RGL-02` | 실 비관통 망 → 정지 관문 · tau_flux | 생산자 sigma_full_status not_computed · 관문 failed · tau NOT_PERCOLATING · f 0.0 |
| `RGL-03` | build_handover stop_after contact / network | True / False |
| `RGL-04` | L9 변이 · 실 비관통: summary / active provenance / full_metrics | failed / success / success · failed / success / success · 옛 세대 생존 False |
| `RGL-05` | NaN % · NaN index · F1 h inf · aug −999 (근거 삭제) · 0 채움 평균 → 수용 | True · True · True · True · True (명시 0 + 평균 → False) |
| `RGL-06` | SE 반경 NaN → status · vm_cv · AM_P ratio · SE mean / 진짜 무하중 → status | OK · 0.0 · 0.0 · nan / FAILED |
| `RGL-07` | 깨끗한 입력 / 옛 factor 4 생존: 짝 σ₀ · grade τ | 3.0 · 2.449489742783178 / 12.0 · 4.898979485566356 |
| `RGL-08` | 입력 삭제 · per-mode≠dual · 관통인데 전력 몫 None+내부 예외 → network | done · done · done |
| `RGL-09` | Spearman [1,1,2] vs [1,2,2] (참 0.5) · 전부 0 (참 미정의) | 1.0 · 0.9999999999999999 |
| `RGL-10 · Q4` | 구·신 18 비교 원시 hex · 전력 몫 실제 / 해석 / 이상 전극 (+%) | True (18) · 0.09167871335514417 / 0.0916787133551442 / 0.08181818181818182 (+12.05 %) |
| `Q2 (RINT-03)` | 독립 raster 옛/새 je 배수 · 새 = 직접 AM mask | 126.5602 · 120.9457 · True |

## 한정 (Codex 그대로)

- 합성 fixture · 소형 CPU 검산이다 — 실침대 r_int NPZ 셋 · real14 압축 dump 는 Codex 가 독립 재실행하지 않았다 (저자 수치를 독립 측정으로 승격하지 않음).
- 반례 탐침의 rc 0 은 **현재 결함을 재현했다**는 뜻이지 대상 코드 GO 가 아니다 · `probe_contracts.py` 는 실 helper · merge · validator · grade 를 부르고 solver 파일 작성만 fixture 로 대신한다.
- 194 행 검산 (판정문 §4) 은 커밋된 요약 CSV 의 산술 검산이다 — 194 개 원 dump 재분석 · 인계 재생성이 아니다.
- `environment_adapters.py` 두 모드는 native Git/WSL/symlink 시험의 대체 인증이 아니다 · 판정문 안 `C:/Users/Administrator/Documents/Codex/…` 경로는 Codex 작업 폴더다 (이 리포에 없다).
