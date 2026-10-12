# ps45 σ_e 인자 끔 다섯 전자 망 진단 — 결과 (10-13 · 보고 전용 · 결과 전 등록대로)

- 등록 = `docs/reviews/ps45_sigmae_factor_off_registration_20261013.md` (manifest 기록 sha256 `d56b7693…`) · 실행기 = `scripts/ps45_sigmae_factor_off_variant.py` ·
  1저자 비준 10-13 *"이것도 하고서 넘어갈까"* (Physics g2 감도 팔 포함 · 등록 그대로) · 실행 = 1저자 WSL · 실행 커밋 `66d537f24` (dirty 0) ·
  입력 뿌리 = 10-07 세대 2 배치 작업 폴더 (`~/ps45_network_g2_0801d4ceb/work/results`) · Python 3.12.3 · numpy 2.5.2 · scipy 1.18.1 · networkx 3.7 · pandas 3.0.5 · 스레드 1.
- 원 묶음 `raw/ps45_sigmae_factor_off_20261013.tgz` (26,050 B · sha256 `21730156db43aead1700a72c753e62ba6fab439e738f8eaf1b749b89894becc6`) = manifest.json · records 20 · logs 20 · 표 · 실행 로그
  (반입 = 새 빈 폴더 · `python3 -I` 로 읽기만).  표 `factor_off_electronic.tsv` = 묶음 안과 같은 바이트 (sha256 `da5ff254…`).
- manifest: run_status **ok** · run_problems 없음 · 다섯 케이스 ok · kind = report-only model variant.

## 결과 (mS/cm · 기준값 σ_ref 4.1 mS/cm · PC:SC 0:10 → 10:0)

| PC:SC | 0:10 | 3:7 | 5:5 | 7:3 | 10:0 |
|---|---|---|---|---|---|
| **주 값 — Hertz H0 · PC 인자 끔** (σ_e) | **0.390802** | **0.405815** | **0.402466** | **0.374697** | **0.467175** |
| 주 값 q = σ_eff / σ_ref | 0.0953175 | 0.0989792 | 0.0981624 | 0.0913895 | 0.113945 |
| 등록 감도 — Physics g2 · 인자 끔 | 0.507670 | 0.538962 | 0.538879 | 0.503943 | 0.600691 |
| 보존 감도 — Hertz · 인자 켬 (같은 실행의 대조 팔 × 0.082) | 0.390802 | 0.235798 | 0.158887 | 0.108846 | 0.106782 |
| 인자 끔 / 켬 (Hertz) | 1 | 1.721 | 2.533 | 3.442 | 4.375 |
| 노드 · 간선 (전자 망 · AM–AM) | 4588 · 8970 | 3330 · 5794 | 2491 · 3878 | 1656 · 2208 | 403 · 733 |

## 검사 (등록 §3 관문)

- G0 통과 — 깨끗한 트리 · `scripts/network_conductivity.py` sha256 `da9ecfef…` = 기대 · 봉인 32 `code_fp e8b2496b…` 실행 앞뒤 같음.
- G1 패치 양성 대조 (풀이 앞 · 뒤) 통과 — 합성 망 PC 만 OFF/ON = 35/8 (FULL · CF · 협착만 · 두 모드) · SC 만 = 1 (비트) · 혼합 ∉ {1, 35/8}.
- G2 입력 결합 — 다섯 ok · 배치 업로드 사본 = 보관 원본 (atom · contact · mesh · 덱 · meta) 같음.
- G3 대조 팔 — 인자 켬 팔의 q = 저장 증서 q (상대차 **0** · Hertz · Physics · 다섯 모두).
- G4 0:10 (SC 만) — 인자 끔 = 켬 (비트 · 두 모드).
- 10:0 (PC 만 · 균일 반경 4.5 µm) — OFF/ON − 35/8 = 3.0e-14 (Hertz) · 1.1e-14 (Physics) ⇒ Codex §3-2 끝점 산술 0.467175 와 같다.
- G5 무변경 — `production_inputs_unchanged` true · 봉인 32 앞뒤 같음.  G6 — `manifest.json` (REFUSED 아님).
- ⚠ `--selftest` · `--check-only` 출력은 묶음에 없다 (화면만 · 실행 로그 = 3 단계 tee) — 실행 결과는 manifest run_status ok 로 확인.

## 판독 (등록 §1 · §6 · Codex 10-13 §4 · §6)

- 주 값 = **0.375–0.467 mS/cm — 다섯 조성에서 거의 평평 · 비단조** (7:3 최저 · 10:0 최고).  인자 켬 (나) 의 0:10 → 10:0 3.66 배 하락은 PC 크기 인자
  (입력 가정 · r 4.5 µm 에서 0.2286) 에서 왔다 — 구조만의 효과가 아니다 (Codex Q2 · §3-2 가 예상한 방향 그대로 · 섞인 셋은 이번 풀이로 처음 값이 생겼다).
- 다섯 조성은 반복이 아니다 — SD · 95 % 구간을 만들지 않는다 · Physics g2 · 인자 켬 = **모형 선택 감도** (별도 마커 · 패널).
- 문헌 = 정성적 규모 대조만 (Codex Q6): Ketter 2025 고체 60 vol% DC 1.035 · EIS 1.121 mS/cm 보다 **2.2–3.0 배 낮다** — 조성 · 입도 · 기공 · 압력이 달라
  반증도 일치도 아니다 · 차이 배수를 그대로 적는다.
- 실험 관찰 (최종 덱 p9 *"전자저항은 (No.1 · No.2 · PC) 유사한 수준"*) 과 방향이 어긋나지 않는다 — 단 **검증 · 재현 문구로 쓰지 않는다** (Codex Q6 · 인자 끔은
  그 관찰에 맞춘 선택이 아니라 결과 전에 등록한 보고 규약이다).
- 그림 각주 = `docs/data/ps45_r45_network_g2_20261007/README.md` §σ_e 의 Codex §6-1 문안 그대로 (PC 경험적 크기 인자 적용 안 함 · 공통 기준 4.1 = 조건부).
- 범위: report-only model variant — 194 · 보충 20 · v1.3 · 웹앱 · τ 인계에 넣지 않는다 · 생산 상수 (`SIGMA_AM_ELECTRONIC` 0.05 · 크기 인자) · 봉인 32 그대로.
  원장 `PS45E-03` (실행 중 교체한 모형은 자기 manifest 를 가져야) 의 조건을 이 실행이 지켰다 (manifest · 패치 표지 · 별도 출력) — 상태는 그대로 둔다 (확인 = Codex 몫).
