# Codex DEM 모델 검증 설계 리뷰 (10-08) — 반입 · 우리 트리 재현

- 판정문 = `docs/reviews/codex_review_model_validation_20261008.md` (ZIP 안 같은 이름 파일 **바이트 그대로** · 42,229 B · sha256 4393346f5fc183fca20501a91e4d88a28672f67ce9a6678af26be698f76974b1 · 안에 아무것도 덧붙이지 않았다).
- 원 ZIP = 1저자 업로드 codex_model_validation_review_20261008.zip — 583,022 B · sha256 864a76b5f8a241c5531c7cf25d53b99f7313ed0e1d12bbb643faff050c174c76 ·
  **107 항목** (파일 107 · 폴더 항목 0) = source/ 71 · evidence/ 22 · probes/ 7 · submitted/ 1 · 최상위 6 (README.md · 판정문 · run_review_checks.py · source_manifest.json · source_plan.json · BUNDLE_MANIFEST.json) ·
  절대 경로 · `..` · 역슬래시 · 심볼릭 링크 0 · CRC 107/107 맞음 (새 빈 폴더에 `python3 -I` 로 풀었다 · 실행기 = `evidence_rerun/tools/safe_extract_mv.py`).
- 핀 = `61ebd181b` (요청서가 들어간 커밋 · 전체 61ebd181b1ae5b47a76fe69d4400e4a3950dc8a3) · 반입 HEAD = `50ec7273b` (핀 뒤 3 커밋).
- 요청서: 판정문 머리의 sha256 475eddca54e4fcbe710518028871909c2845403b4b4d69dffde4e772d50b4ca4 = 핀의 `docs/reviews/codex_model_validation_request_20261008.md` (git show 61ebd181b 로 잰 값) = ZIP 의 submitted/ 사본 = ZIP 의 source/ 사본 — 셋 다 같다.
- 판정 = **새 보정 · 물리 검증 HOLD · 모델 내부 진단 수정 GO** (판정문 §0 · 최종 결론) · 새 finding MV-01 … MV-09 (P1 여섯 · P2 셋) → 원장 `docs/reviews/findings.json` (open · 수정 없음 · 반입만).

## 1. 이 폴더에 넣은 것 · 뺀 것

| 넣음 | 뺌 (원 ZIP 에만) |
|---|---|
| `README.md` (Codex 묶음 설명 원문) · `BUNDLE_MANIFEST.json` (배포 파일 106 의 크기 · sha256 · 자기 자신 제외) · `source_manifest.json` (71 · Git blob · sha256 · 크기) · `source_plan.json` · `run_review_checks.py` · probes/ 7 · evidence/ 22 — 전부 ZIP 바이트 그대로 (34 파일 sha256 대조 같음) | source/ 71 — 우리 git 의 핀 바이트와 같다 (§2) · `source_manifest.json` 으로 복원 |
| evidence_rerun/ — 우리 재현 (§3 · 출력 · 대조 · 실행기 · 첫 시도 실패 기록) | submitted/codex_model_validation_request_20261008.md — 핀의 요청서와 바이트 같음 (위 요청서 줄) |

## 2. 원본 신원

| 대조 | 결과 |
|---|---|
| ZIP source/ ↔ 핀 `61ebd181b` (경로마다 git show 바이트 비교) | **71/71 같음** |
| ZIP source/ ↔ 반입 HEAD `50ec7273b` | **70/71 같음** — 다른 하나 = `docs/session_20260923_progress.md` (핀 뒤 진행 기록 5 줄 추가 · 어느 탐침도 읽지 않는다) |
| source_manifest.json · source_plan.json (Git blob · sha256 · 크기 · 경로 집합) | 71/71 일치 |
| BUNDLE_MANIFEST.json | 106/106 크기 · sha256 일치 (목록에 없는 것 = 자기 자신뿐) |
| 추가 소스 evidence/mv_softening_in.ps_7_3_r45_61ebd18.liggghts (Git blob 52ed80f6…) | 우리 `dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts` 와 바이트 같음 (핀 · HEAD 같은 blob) |
| 추가 소스 evidence/mv_softening_normal_model_hooke_hysteresis_3d5c00f.h (Git blob 3921ff5c…) | 이미 커밋된 docs/reviews/codex_ps45_porosity_evidence_20261001/reference/normal_model_hooke_hysteresis.h 와 바이트 같음 — LIGGGHTS-PUBLIC 공개 저장소 3d5c00f 와의 직접 대조는 이 세션에서 못 했다 (그 저장소 GitHub 접근 없음) · ibb 실행 바이너리 신원 아님 (Codex README 와 같은 한정) |

원 결과 = `evidence_rerun/source_identity_check.json` (경로마다 bytes · sha256 · blob · 핀 같음 · HEAD 같음).

## 3. 우리 트리 재현 (10-08 · Linux)

- 환경 = Python 3.11.15 · NumPy 2.4.6 · pandas 3.0.6 · NetworkX 3.6.1 (SciPy 1.17.1 · python-dateutil 2.9.0.post0) — `evidence_rerun/environment.json`.
  Codex = Windows Python 3.12.14 · NumPy 2.3.5 · pandas 3.0.1 · NetworkX 3.7.
- 방법: 재현 뿌리 (스크래치) 의 source/ 를 ZIP 이 아니라 **우리 worktree HEAD `50ec7273b` 의 같은 71 경로**로 채웠다 (70/71 = Codex 사본과 같은 바이트 · 다른 하나는 탐침이 읽지 않는 진행 기록) ·
  probes/ = ZIP 바이트 그대로 (실행 전에 일곱 개 전부 읽음 — 네트워크 · 삭제 · 자기 출력 자리 밖 쓰기 없음) · evidence/ = 빈 폴더 (탐침이 자기 결과를 쓴다) ·
  탐침마다 `python3 -I -B` · 탐침 원본 무변경 · 순서 = Codex `run_review_checks.py` 의 여섯 + mv_stress_portability.py.
  실행기 = `evidence_rerun/tools/mv_build_rerun_root.py` · `evidence_rerun/tools/mv_run_probes.py` · `evidence_rerun/tools/mv_probe_launcher.py` · `evidence_rerun/tools/mv_compare.py`.
- ⚠ **첫 시도 (순수 -I) = 두 탐침 rc 1** — mv_stress_core_probe.py: 이 컨테이너의 pandas 는 사용자 site (~/.local) 에 있는 python-dateutil 을 필요로 하는데 -I 가 사용자 site 를 끈다 →
  탐침 안의 plane_load_share selftest T10 배치 두 케이스가 ImportError 로 FAILED → KeyError 'force_source' (같은 코드를 일반 모드로 돌리면 54/54 — 코드 · 탐침 결함이 아니라 환경) ·
  mv_stress_portability.py: core 결과 파일이 없어 연쇄 실패.  기록 = `evidence_rerun/attempt1_isolated_no_usersite/_runs.json` · 같은 폴더 stderr 둘.
  → 사용자 site 경로 하나만 일반 모드와 같은 자리에 더하는 실행기 (`evidence_rerun/tools/mv_probe_launcher.py` · `-I -B` 그대로 · 탐침은 runpy.run_path) 로 일곱 개 전부 다시 = **7/7 rc 0 · stderr 전부 0 B**.
- mv_stress_portability.py 는 자기가 만든 최소 ZIP (11 파일) 안에서 두 스트레스 탐침을 자식 프로세스 (`-B` · `-I` 없음) 로 다시 돌린다 — 그 두 탐침과 우리 코드 사본만 담긴 임시 폴더라 받아들였다.

### 3-1. 결과 JSON 대조 (Codex evidence/ ↔ 우리 evidence_rerun/ · 파싱 값 · `evidence_rerun/compare_vs_codex.json`)

| 탐침 | rc | 숫자 칸 | 다른 칸 | 최대 차이 | 판정 |
|---|---|---|---|---|---|
| mv_anchor_porosity | 0 | 22 | 0 | 0 | 같음 (바이트 차이 = 줄바꿈 CRLF 뿐) |
| mv_pressure_arithmetic | 0 | 51 | 0 | 0 | 같음 (CRLF 뿐) |
| mv_softening_scaling | 0 | 94 | 0 | 0 | 바이트까지 같음 |
| mv_softening_frozen_reweight | 0 | 25 | 9 | 절대 2.27e−13 · 상대 3.6e−16 | 끝자리 (아래) |
| mv_stress_probe | 0 | 241 | 24 | 절대 1.42e−14 (상대 최대 0.33 = 0 근처 잔차끼리 · ps45 10:0 contribution_max_abs_error_pp 1.42e−14 ↔ 2.13e−14) | 끝자리 (아래) |
| mv_stress_core_probe | 0 | 25 | 0 | 0 | 같음 (CRLF 뿐) · plane_load_share selftest 54/54 |
| mv_stress_portability | 0 | 2 | 0 | 0 | 두 탐침 JSON = 자기 기록과 같음 (true) · 다른 칸 = 실행 환경 문자열 넷 (python · numpy · pandas · networkx) + external_review_cache_used_as_environment (Codex true · 우리 false — 우리 환경에는 NetworkX 가 설치돼 있어 캐시가 필요 없다) |

- 표준 출력: 다섯 = CRLF 를 빼면 같음 · mv_softening_frozen_reweight = 위 끝자리 · mv_stress_probe = 마지막 output 경로 줄 (Codex Windows 작업 폴더 ↔ 우리 스크래치) · portability = Codex 묶음에 stdout 없음.
- **끝자리 원인 = Python 3.12 내장 sum() 의 보정 합산 (Neumaier)** — 3.11 은 단순 합산이다.  확인: CPython 3.12 sum() 을 흉내 낸 진단 실행기
  (`evidence_rerun/tools/mv_probe_launcher_sum312.py`) 로 같은 탐침을 다시 돌리면 결과 JSON 여섯 개 전부 Codex 와 파싱 값이 같다 (`evidence_rerun/diag_py312_sum_emulation.json` ·
  이 진단의 portability rc 1 = 자식 프로세스는 바꾼 sum 을 쓰지 않아서 생기는 정상 결과 · 판정 증거 아님).  판정에 걸린 숫자 (아래 표) 는 끝자리 차이 칸에 없다.

### 3-2. 판정문의 숫자 ↔ 우리 재실행

| 판정문 | Codex | 우리 (evidence_rerun/) |
|---|---|---|
| MV-01 B 수렴 합성 입력 | KE 0.5 J → 구간 10 CONVERGED (초기 참조 KE 1.695918e−5 J 의 29,483 배) · KE 0.009 J → 14 번째 | CONVERGED 10 · 29,482.56 배 · CONVERGED 14 |
| MV-02 법선 이력 초기화 | 0.16 → 0.40 | 0.16000000000000003 → 0.4 |
| MV-03 pure-SE 정의 차이 | 12.42 / 11.41 %p · 밀도비 1.138123 / 1.129131 | 12.42 / 11.41 · 1.1381228 / 1.1291308 |
| MV-03 세 구 반례 (calc_porosity_dual 48–110 행) | 90.693849887 ↔ 88.648542170 % · 2.045307717 %p | 90.69384988682711 ↔ 88.64854216964626 · 2.0453077171808474 |
| MV-07 상 힘 교환 | 전역 virial 상대오차 0 · AM/SE 평균 VM 21.485917 / 64.457752 역전 | 0.0 · 21.485917317405868 / 64.45775195221759 ↔ 64.45775195221759 / 21.485917317405868 |
| MV-07 접촉점 이동 | 상 평균 VM ÷ 전체 수평균 1/1 → 0.75/1.25 | 1.0000000000000004 / 0.9999999999999997 → 0.7500000000000001 / 1.25 |
| MV-07 회전 · 병진 | tensor 6.34e−16 · VM 4.41e−16 | 6.340860639987258e−16 · 4.409354743161529e−16 |
| MV-08 수 가드 | AM 한 개 0.137486 %p · 50 개 6.874320 %p | 0.13748640543570936 · 6.874320271785467 |
| MV-09 3.1M → 이완 | AM–AM −3.28564 %p · α_SE +0.034467 (+7.3205 %) · α_PC −0.031422 | −3.2856423729379074 · +0.034467257234485016 (+7.320533186629907 %) · −0.03142247718500868 |
| §3 Q1 · Q10 | 300,000 Pa · 750 N · 412.5 N · 0.75 N · τ 0.05319 / 0.53191 s · 잔류 0.532 µm | 같음 |
| §3 Q1 감쇠 저항 | 434.3 N = 173.72 MPa 상당 · 300.95 − 165.34 = 135.61 MPa | 같음 (직접 산술 — 탐침 밖) |
| §5 Q7 표 | Rayleigh 63.4103 / 52.6665 / 24.9819 µs · dt 비 1.5770 / 1.8987 / 4.0029 % · kn 1.7411 / 1.7275 · 3.0314 / 2.9617 · 9.9977 / 8.8477 · E 비 103.7037 … 5.8333 · dt 배율 0.23717 | 같음 |
| §6 V5 | g 9.81e−6 · 2.97420 MPa ↔ 2.97420 Pa · 245.24 덱 s · 1.962e−7 m · λ_t 31,622.7766 | 9.810000000000001e−06 · 2.9741958 · 245.2401099307744 · 1.9620000000000002e−07 · 31622.776601683792 |
| §7-3 21 면 ↔ 정확 적분 | 상별 최대 ≈0.699 %p | 0.6990739143802642 (ps45 10:0 AM–SE) |
| §7 요청서 검사 숫자 | 2.2175e−6 · 8.7016e−7 (3.1M) · 1.0005685 · 3.1226e−6 · 1.4638e−5 (이완 7:3) | 같음 (기록된 LW checks) |
| §9 plane_load_share selftest | 54/54 | 54/54 |

⇒ 판정문의 숫자는 우리 트리에서 전부 재현된다.  차이는 환경 (Python 3.12 sum 끝자리 · 줄바꿈 · 경로 · 버전 문자열) 뿐이다.

- 관찰 (판정 바꾸지 않음): MV-07 첫 반례 (같은 기하 두 dimer 의 힘 맞바꿈) 는 우리 코드가 RGL-06 수정 (커밋 `a8e53b2a0`) 부터 검사 범위로 적고 있다 — 탐침 출력
  `evidence_rerun/mv_stress_core_controls.json` 의 changed_cp_checks.virial_scope 에 그 문장이 그대로 찍힌다.  MV-07 이 겨누는 것은 요청서 V6 의 "같은 모델 안 상대값이므로 안전" 논리와 접촉점 배분 (둘째 반례) 이다.

## 4. 한정

- Codex 는 설계 · 추론 · 후처리만 검토했다 — DEM/MPM 실행 · 덱 생산 · 스케줄러 조회/조작 · 생산 코드 수정 · 보정 없음 · **ibb B job 271368 의 상태를 조회하거나 중단 · 변경 · 재제출하지 않았다** ·
  기존 B1–B5 예측 띠도 바꾸지 않았다 (판정문 §0 · §1 · 묶음 `README.md`).  우리 재현도 산술 · 후처리만 — DEM · MPM · ibb 접근 없음.
- 이 재현은 Codex 탐침이 우리 코드 · 저장 CSV/JSON 에서 같은 값을 낸다는 확인이다 — pure-SE atom/contact 원덤프 · B 끝점 · 실험 표준 원측정의 재구성이 아니다 (판정문 §1 의 한정 그대로).
- 판정문의 합성 반례는 "검사식이 허용하는 입력" · "정의 반례" 다 — 실제 B 런 · 실제 침대가 그렇게 움직였다는 보고가 아니다 (MV-01 · MV-03 · MV-07 · MV-08 각 절).
- mv_softening_frozen_reweight 결과는 감쇠 힘을 무시한 고정 상태 구성식의 조건부 산술 예시다 — DEM 결과 · 재평형 예측이 아니며 판정문 V4 숫자에 쓰이지 않았다 (묶음 `README.md`).
- 원장: MV-01 … MV-09 = open · owner claude · 수정 없음.  MV-04 = Codex 표기 "P1/P2" → 원장 P1 (이름만 잘못 붙인 경우 = Codex 기준 P2 · note 에 적음).
  원장에 관련 항목 칸이 없어 (있는 것은 supersedes — 뜻이 다르다) MV-01 · MV-02 · MV-08 의 note 에 "관련: DEMP-01" 로만 적었다 (DEMP-01 본문은 바꾸지 않았다).
