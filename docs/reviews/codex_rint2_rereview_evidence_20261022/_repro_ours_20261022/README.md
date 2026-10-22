# Codex Rint ② 재검토 (10-22) — 우리 트리 재현 (10-22 · 읽기 전용)

판정문 `docs/reviews/codex_review_rint2_rereview_20261022.md` · 리뷰 핀 `0b3012460fb8e8b7d53484b0efe399e2dc506aec`.
리포 작업 트리를 고치지 않았다 (묶음 복사본 + 핀 git 객체로 다시 만든 `source/` · 세션 작업 폴더) · fetch / push 없음 · 원 미니 묶음 무변경.

## 0. 한 줄

판정문 §10 탐침 여섯을 우리 기계에서 그대로 돌렸다 — **판정값 (표지 · 문제 문장 · 판정 · 시험 통과 수 · 증서 구간 · census) 차이 0**.
다른 것은 숫자 끝자리뿐이다: CG · spsolve 반올림 (RCA-07 반례의 게시 G · 잔차 · 균형) · 버전 문자열 · Windows 텍스트 쓰기 (fixture CSV 3 바이트).
RCA-07 의 주 반례 (`main`) 는 10-21 재현과 같은 환경 칼날로 **B 하나만 뒤집힌다** (Codex B 통과 ↔ 우리 B 실패 · 판 불균형 9.148e-5 ↔ 1.472e-4) — ⓓ 는 둘 다 거부 · `ok` 둘 다 false · 연결 · 23 반복 사례는 우리 환경에서도 A/B/C 통과 + ⓓ 거부 (RCA-07 결론 그대로).

## 1. 환경

| | 우리 | Codex (판정문 §1) |
|---|---|---|
| OS | Linux 6.18.44 x86_64 | Windows |
| Python | 3.11.17 | 3.12.14 |
| NumPy | 2.4.6 | 2.5.3 |
| SciPy | 1.17.1 | 1.16.3 |
| 스레드 | OPENBLAS · OMP · MKL · NUMEXPR = 1 | 1 |
| 실행 | `nice -n 19 python3 -I -X utf8 -B` (형제 모듈을 import 하는 탐침 둘 = `tools/run_with_dir.py` 로 그 폴더만 sys.path 에 되돌림) | `python` |

## 2. 입력 재구성

| 대상 | 방법 | 결과 |
|---|---|---|
| 핀 소스 `source/` | `source_manifest.json` 경로마다 `git show 0b3012460:<경로>` (`tools/rebuild_source.py`) | **1,679 / 1,679** sha256 · git blob · 크기 같음 · 77,777,194 B (`source_rebuild_report.json`) |
| 묶음 나머지 | 미니 ZIP 그대로 (판정문 사본 하나 뺌) | 탐침 · fixture 바이트 = 반입본과 같음 |
| `RINT_REVIEW_SOURCE` | 지정 안 함 (= 다시 만든 `source/` · Codex 와 같은 입력 · git 밖) | — |

## 3. 탐침별 결과 (`logs/summary.txt` · 대조 = `compare/*.cmp.json` · 우리 출력 = `ours/`)

| 탐침 | rc · 시간 | 우리 결과 | Codex JSON 키 대조 |
|---|---|---|---|
| `registration/probe_registration_current.py` | 0 · 0.1 s | RCA-01 끝 [10,000, 5,990,349.747388] / [10,000, 10⁷] Ω · W 0.785238 / 0.786487 WEAK · 양의 해석 회로 54 (멈춤 0) · 보호 띠 팽창 443,434,903.8 (15 점) · 시간 191.353–231.409 → 205.806–248.888 h · 세 origin W 0.2930 PASS ↔ 고정 8 0.6804 WEAK · SV all3 = corner 12 / origin 0 / origin8 0 · R 비단조 PASS · 계획 오류입력 7 = PLAN_INVALID | **467: 정확 467 · 다름 0** · fixture 7 / 7 바이트 같음 |
| `certificate/probe_certificate.py` | 0 · 2.1 s | 독립 망 180 · 후보 540 · 구간 540 · ⓓ 통과 192 · 구간 누락 0 · 거짓 합격 0 · 5 노드 합산 = `OverflowError` (`intermediate overflow in fsum`) · 소비자 변이 12 판정 같음 | 690: 정확 617 · ≤1e-12 9 · 경로 1 · **다름 63 = CG 반올림 61 (prior.main · connected · iter23) + 버전 2** · 판정값 다름 = `prior.main.certificate.pass_b` 하나 (위 §0) |
| `certificate/run_selected_tests.py` | 0 · 2.2 s | **202 / 202 PASS** | 로그 PASS/FAIL 줄 = 같은 이름 · 다른 것 = 줄에 찍힌 오차 숫자 (1.886e-04 ↔ 1.890e-04 등) · 시간 |
| `geometry/run_review.py` | 0 · 26.6 s | 저자 회귀 **122 / 0** · S1 **44 / 0** · 첫 성분만 지우는 변이 아래 QD2 **13 / 13 통과** · 두 성분 G 47.61904761904763 · 변이 위비 2.0 · 증서 비 구간 **[10.29125393534377, 10.291253935346631] (비트 같음)** · 최종 SV 표지 [] · 기록 변이 7 문제 · 표지 같음 · 포트 넷 G · σ · digest 같음 | 860: 정확 820 · ≤1e-12 21 · 경로 1 · **다름 18 = 잔차 · 균형 · kcl · dsigma · 오차 상계의 끝자리 16 + 버전 2** |
| `probes/provenance_probe.py` | 0 · 0.2 s | F1 git 밖 HEAD/dirty None 통과 · status rc 128 → dirty False · F2 chain ↔ runner 혼합 통과 · F8 투영 키에 입력 없음 · F5 `commit:` 통과 | **41: 정확 41 · 다름 0** |
| `probes/s0_integration_probe.py --fixture-argv` | 0 · 1.3 s | 접합 1 → 0 · 셀 수 0/1/3/5/6 = 295826/8448/87/19/324 전후 같음 · 옛 · 새 보고 둘 다 관문 통과 · 입력 binding 없음 · transport 0 회 | **34: 정확 34 · 다름 0** |
| 같은 탐침의 S0 보고 셋 (`s0_actual_stage1` · `stage2` · `stage2_changed_bed`) | — | census · raster 값 전부 같음 | 정확 356 / 506 / 414 · **다름 8 씩 = 버전 3 · scaffold CSV (123 ↔ 120 B — 시험 작성기 `open(…, 'w')` 가 Windows 에서 줄 끝 CRLF · 3 줄) 와 그것을 담는 sha 둘 (입력 · 계획) · argv sha · 걸린 시간** |

## 4. 관찰 (고치지 않음 · 시험으로 확인 전)

- `certificate/probe_certificate.py` 의 stderr 에 `step3_conv_cert.py:344: RuntimeWarning: overflow encountered in add` (`tol_r` 계산) — 큰 유한 규모 입력 (`finite_subtotals_overflow` 꼴) 에서 최종 `fsum` 전에 중간값이 이미 inf 가 된다.  RCA2-08 과 같은 부류 — 수정 때 함께 본다.
- S0 시험 작성기의 텍스트 쓰기 (줄 끝 CRLF) = `RINT2-B01` 과 같은 부류 (Windows 에서 fixture 바이트가 달라짐) · 이 탐침에서는 census 값에 영향 없음 · 판정 영향 없음.

## 5. 다시 돌리는 법

`tools/run_all.sh` (`SP` = 작업 폴더 · `REVIEW` = 미니 묶음 복사본 + `tools/rebuild_source.py` 로 만든 `source/`) → `tools/compare_json.py <codex.json> <ours.json> <out.json>` (잎 단위: 정확 · 상대 ≤1e-12 · 경로 · 다름).
`ours/` 의 JSON 안 경로 문자열 = 그 세션 작업 폴더 (환경 값 · 판정값 아님).
