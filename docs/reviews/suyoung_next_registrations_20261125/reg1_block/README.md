# 수영 2D 등록 ① 접촉 미니 · 실행 블록과 판독기 (11-26)

2026-11-26 · [DEM 우선 (수영)] · 개발 자료 · **결과 0 건 · 등록 팔 완주 0 · MPM 걸음 0** · 1저자 GO 전 준비물 (서브 세션 · 시험 먼저)

| 이번에 닫는 것 | 닫지 않는 것 |
|---|---|
| 등록 ① §6 실행 블록 (붙여넣기 TXT 하나 + `.sha256` · CHECK_ONLY · GO 한 번 · READBACK) · §4–§5 판독기 (J1–J5 · 첫 힘 · 감시 · 처분 코드) · §8 반환 꼴 · 시험 · 변이 시험 | 50 팔 실제 실행과 그 값 (1저자 GO 뒤) · WSL (Python 3.12.3 · NumPy 2.5.2) 에서의 CHECK_ONLY · 실제 팔 시간 · 반입 커밋에서 다시 빌드 · 등록 ② (탈압 · H_S · U4 · m3) 판독 |

## 1. 파일

| 파일 | 묶음 안 | 하는 일 |
|---|---|---|
| `build_block.py` | — | 고정 커밋의 파일을 `git show` 로만 읽어 TXT + `.sha256` 를 리포 밖에 만든다 (핀 대조 · 정렬된 tar.gz · 시각 0 · base64) |
| `run.sh` | 맨 위 | 묶음 안 실행기 (모드 셋) |
| `reg1_queue.py` | 맨 위 | 환경 관문 · 코어 둘 (Q13 `coordinate.py` 의 `eligible` · `topology` · `choose_cores` · `checks` 를 핀으로 불러 씀) · 50 팔 대기열 · 반환 풀기 |
| `reg1_reader.py` | 맨 위 | 판독기 → `summary.json` · READBACK 영수증 `return_receipt.json` |
| `test_reg1_block.py` | — | 시험 56 |
| `synth_runs.py` · `fake_worker.py` | — | 시험 전용: 드라이버 꼴 그대로의 합성 팔 (지어낸 숫자) · 시험 묶음에서만 `driver.py RUN` 자리에 넣는 가짜 일꾼 |
| `mutation_probe.py` | — | 변이 시험 (사본만 깨뜨린다) |

묶음 안 파일 18 = 블록 셋 + 드라이버 + 원천 일곱 (`driver.SOURCES`) + 등록 ① 원문 + U6(c) ⑥ 규칙 셋 (`force_rule.py` · `rule.json` · `doubling.py`) + Q13 `coordinate.py` (모두 리포 경로 그대로) + `RELEASE` + `SOURCE_SHA256SUMS`.  핀 13 = `reg1_queue.PINS` 여섯 + 드라이버 `SOURCES` 일곱 — 빌드 · 판독 때 둘 다 대조한다.  드라이버 · 원천 일곱 · 규칙 파일은 한 글자도 바꾸지 않았다.

## 2. 흐름 (등록 §6)

| 단계 | 하는 일 |
|---|---|
| TXT 겉 | 모드 확인 (틀리면 rc 2 · 아무것도 안 만듦) → READBACK 이면 반환 폴더를 절대 경로로 → `mktemp` → base64 풀기 → 내장 sha256 · `RELEASE` 대조 → `run.sh` |
| 공통 | `SOURCE_SHA256SUMS` 전수 대조 → `~/Yonghoon-DEM-DFT/venv/bin/python` 이 3.12.3 · 2.5.2 이고 스레드 변수 여섯 = 1 인지 (아니면 `ENVIRONMENT_MISMATCH` rc 1) |
| CHECK_ONLY | 코어 둘 (서로 다른 (package, core_id)) → `driver.py CHECK_ONLY` (원천 핀 · 등록 숫자 대조 `reg1 50/50` · G1 · G2 시드 점 수와 해시 · `MPM_STEPS 0` · 이 줄 묶음 안에도 드라이버 자신의 `CHECK_ONLY_OK` 가 찍힌다) → 50 팔 대기열 표 (긴 팔부터 · 걸음 · 한도) · 등록 ① 계획 대조 → 판독기 자기 검사 (손으로 만든 입력 14 · trace 없음) → 끝 줄 **`CONTACT_MINI_CHECK_ONLY_OK`** |
| GO | CHECK_ONLY 와 같은 검사 → `~/suyoung_contact_mini_1125_once` 예약 (있으면 `ALREADY_RESERVED` rc 2) → 작업 · 반환 폴더 (`mktemp`) → 대기열: 팔마다 `taskset -c CPU python -I … driver.py RUN --arm … --cpu CPU` (스레드 변수 1) · 긴 팔부터 · 빈 코어가 다음 팔 · 드라이버가 등록 한도에서 스스로 멈추고 (rc 3) · 한도 + 30 초에도 살아 있으면 종료 (rc 124) · 자동 재시도 0 · 한 팔 실패에도 계속 → `execution.json` → 판독기 `summary.json` → 끝 (실패여도) `SHA256SUMS` · TAR · 화면 |
| READBACK | 반환 폴더 `SHA256SUMS` (TAR · 화면) → TAR 안 이름 (`run/` 아래 파일 · 폴더만) → 안쪽 `SHA256SUMS` → 화면 같음 · 끝 줄 `COMMAND_RC=0` → 판독기 다시 → 보관 `summary.json` 과 같은가 (다르면 `ARCHIVED_SUMMARY_MISMATCH`) → `return_receipt.json` (mktemp 폴더) · 가압 0 |

반환 TAR 안 (모두 `run` 폴더 아래 · 리포 파일 아님): RELEASE · SOURCE_SHA256SUMS · screen.txt · execution.json · 팔마다 arms 아래 trace.csv · result.json · receipt.json · logs 아래 팔 로그 · summary.json · SHA256SUMS.

## 3. 판독기 (등록 §4–§5 → 코드)

| 항목 | 코드 |
|---|---|
| J1 | U6(c) ⑥ `force_rule.compare` 를 핀 파일 그대로 실행 · 판정 쌍 합치기 = 같은 파일의 `aggregate` (유효한 초과 하나면 초과 · 둘 다 이내면 수렴 · 그 밖 보류) · 판정 16↔32 · 24↔48 · 보고 8↔16 · 32↔48 · 응답 = trace `bottom_MPa` (= 아래판 힘 / D × 10 MPa) · 좌표 u · 쌍마다 구간 끝 · 합집합 표본 수 · 분자 · 분모 · 비 · 처음 초과 변위 · 판정 |
| J2 | max \|윗판 힘 − 아래판 힘\| / max \|아래판 힘\| ≤ 1/20 (정확 비교 `force_rule.exceeds`) · 팔마다 |
| J3 | `compare(σ_G2(u), σ_G1(u/2))` · 같은 칸 · 재료 · V0/4 · 두 팔 J2 통과 · 판정 32 · 48 · S-P · F2-P = 처분 · S-E · F2-E · F1-P = 보고 |
| J4 | E-G1-V4 다섯 · ε = (u − 2 g_p)/D = 0.01 · 0.02 · 0.04 · ρ = σ_b / (4.924 MPa × ε) · 범주 ±20 % (ρ 값도 summary 에) |
| J5 | P-G1-V4 다섯 · σ_b 와 드라이버가 기록한 부피 평균 σ_yy (ΣV₀τ_yy / ΣV₀J · 압축 양수로) 의 꺾임 ε · 꺾임 응력 · 앞뒤 기울기 · NZ22 값 나란히 |
| 첫 힘 | σ_b > 0.008 MPa (엄격) 첫 걸음 · u_on − u_geo (G1 2 g_p · G2 4 g_p) · 드라이버 기록과 대조 |
| 감시 | G2 \|Δx\|/D ≤ 0.01 · 옆벽 0 · 아래판 침투 ≤ 2 × 10⁻¹² · 비유한 0 · 넘으면 그 팔 보류 (그 팔이 든 판정만 보류) |
| 기술 미완료 | `RELEASE` · 원천 목록 다름 · 실행 기록 없음 · 미완료 · 재시도 · 코어 둘 아님 · 일꾼 rc 1 · 2 · 팔 기록의 원천 · 환경 · 코어 배정 · 스레드 · 등록 설정 다름 → `TECHNICAL_INCOMPLETE` (물리 판정 안 함 · 팔별 rc 만) |
| 처분 | §5 줄 1–7 · 8 (`MINI_GAP_CORRECTION_HURTS` 표지) · 9 (`MINI_HELD`) · 0 |

판독기 해석 일곱 (결과 0 건일 때 고정 · `summary.json` 의 `reader_rules` 에 그대로 실린다):
1. J2 의 "구간 · 합집합 표본" = 그 팔 자신의 [0, 끝 변위] · 자기 표본 (윗판 · 아래판 힘이 같은 표본을 쓴다).
2. J3 판정 = 32 · 48 칸을 U6(c) `aggregate` 로 합친다 — 유효한 초과 하나면 불일치 · 둘 다 이내면 일치 · 그 밖 보류 (보류된 판정 칸이 모두 J2 보류이면 "J2 미통과로 보류").
3. 처분 = 줄 1–7 가운데 세 값 논리 (보류 = 모름) 로 참인 첫 줄 · 그 위에 아직 모르는 줄은 `undetermined_rows_before_decision` 에 적는다 · 참인 줄이 없으면 `MINI_HELD` (§5 *"1–7 가운데 정해지는 줄이 있으면 그 줄을 쓴다"*).
4. 줄 7 의 "(G1 수렴)" = 탄소성 원판 하나 V0/4 의 J1 수렴.
5. 줄 4 = "수렴하는 접촉 방식 X" 의 J1 부분이 참이고 J3 이 J2 보류로만 보류.
6. 가로 어긋남 감시 = 원판 둘 팔만 (§4-4 가 G2 위 원판을 지목) · 원판 하나 값은 보고만.
7. J5 꺾임 = ε ≥ 0 표본에 이어진 두 직선 최소제곱 · 꺾임점 = 실제 표본 (왼쪽 3 개 이상 · 오른쪽 2 개 이상) — 등록이 정의를 두지 않아 정했다 (보고 전용).

## 4. 시험

`python3 -I -X utf8 -B docs/reviews/suyoung_next_registrations_20261125/reg1_block/test_reg1_block.py` (이 컨테이너 약 140 초 · Python 3.11.18 · NumPy 2.4.6)

| 시점 | 결과 |
|---|---|
| 시험 먼저 (블록 없음 · 커밋 `b4acb8ca0`) | 54 중 통과 0 — 오류 45 · 클래스 준비 오류 2 (그 안 8 시험 미실행) · 건너뜀 1 (git 빌드 시험은 블록 커밋 뒤에만) |
| 첫 구현 | 54 중 53 통과 · 건너뜀 1 (구현 쪽 고침 하나: 환경 상수 표기를 시험이 쓰는 꼴 `('3.12.3', '2.5.2')` 로) |
| 자체 검토 뒤 보강 | 시험 2 추가 — 고치기 전 2/2 실패 확인: ① 보류 팔의 첫 힘 걸음 변위가 NaN 이면 summary JSON 이 깨졌다 (`ValueError: Out of range float`) ② 화면 파이프가 닫히면 `execution.json` 이 빠졌다 (`BrokenPipeError`) → 고침 · CHECK_ONLY 끝 줄이 드라이버의 `CHECK_ONLY_OK` 와 같아 헷갈리던 것 → `CONTACT_MINI_CHECK_ONLY_OK` (끝 줄 단언 추가 · 옛 끝 줄로 되돌린 변이를 이 단언이 잡는다 — §5) |
| 지금 | **56/56** (git 빌드 시험 포함 · 구현 커밋에서) |

시험이 보는 것: 묶음 안 파일 = 고정 파일 바이트 · 핀 · 목록 · TXT 왕복 (풀어낸 묶음 = 원본 바이트 · 두 번 빌드 같음) · 고친 고정 파일이면 빌드 거부 · TXT 글자 하나 (base64 몸 · RELEASE 줄) · 묶음 파일 한 바이트 · 모드 틀림 → 관문 닫힘 (Python 0 회) · 진짜 묶음이 이 컨테이너에서 환경 관문에서 멈춤 · CHECK_ONLY 계산 0 (드라이버 RUN 0 · 가짜 일꾼 호출 0 · 예약 · 작업 · 반환 폴더 0) · 대기열 (등록 계획 그대로 긴 팔부터 · 팔마다 한 번 · 재시도 0 · 코어 둘 동시 · taskset 확인 · 실패 팔에도 계속 · 한도 + 유예 넘으면 rc 124 · 같은 물리 코어 거부 · 화면 닫혀도 기록) · 반환 풀기 (해시 · 이름 · 화면 · 끝 rc) · 판독기 규칙 (J1 = `force_rule.compare` 와 같은 결과 · 5 % 경계 21.0 / 21.01 · 보고 쌍은 판정 안 함 · J2 경계 1/20 · 분모 0 · J3 u/2 · 판정 칸 32 · 48 · 보류 종류 · 첫 힘 엄격 · 꺾임 맞춤 · 처분 코드마다 한 경우 · 순서 · 세 값 · 틈 표지) · 팔 읽기 (NaN · 열 빠짐 · 빈 팔 · 미완료 · 시간 초과 · 가로 어긋남 G2 만 · 옆벽 · 침투 경계 · trace 해시 · 일정 · 원천 · 코어 · 일꾼 rc 2) · 합성 전체 런 (줄 3 · 7 + 표지 · 4 · 9 · 기술 미완료 여섯) · 판독기 해법기 거부 · GO → `ALREADY_RESERVED` → READBACK (상대 경로 · 영수증 칸 · 가압 0) · 바꾼 summary · trace · TAR 한 바이트를 READBACK 이 거부 · 개인 문자열 없음.

## 5. 변이 시험

`python3 -I -X utf8 -B docs/reviews/suyoung_next_registrations_20261125/reg1_block/mutation_probe.py` — 사본에서 규칙 하나씩 깨고 지정 시험이 실패하는지 본다 (리포는 안 바뀐다).  대조 (안 깨뜨림) 23/23 통과 · **변이 40 가지 모두 잡힘** (`MUTATIONS_ALL_CAUGHT 40/40` · 이 컨테이너 몇 분 — 끝-끝 예약 · 한도 종료 둘이 각 약 1 분).

변이: J1 판정 쌍 · 초과를 보류로 · 거친/고운 뒤바꿈 · J2 문턱 · 분모 · J3 u/2 · 판정 칸 · 보류 종류 · 첫 힘 문턱 · 가로 감시 범위 · 한계 · 옆벽 · 침투 경계 · 비유한 · 일정 · trace 해시 · 원천 · 일꾼 rc 2 · J4 ε · J5 부호 · 세 값 논리 · 처분 순서 · 줄 7 · 틈 표지 · 해법기 거부 · 물리 코어 · 환경 · READBACK 비교 · 비유한 첫 힘 · JSON 안전 · 화면 닫힘 · 대기열 순서 · 유예 · 재시도 · 같은 코어 · 한도 종료 · 반환 rc · CHECK_ONLY 멈춤 · 끝 줄 · 예약.

## 6. 만든 TXT (리포 밖 · 커밋하지 않음)

| 칸 | 값 |
|---|---|
| 고정 커밋 (`RELEASE`) | `63e104b0774402ab0d11fc2c1c997fc331ba4555` (B 의 구현 커밋 · 조수 가지의 구현 커밋을 cherry-pick 한 것 · 11-26 반입 때 다시 빌드) |
| 이름 | `PASTE_SUYOUNG_CONTACT_MINI_63e104b07744_1125.txt` |
| TXT sha256 | `1831e1b8827a38765f3efa2c3bb55adc8d7b16692d07a0b676bbcab45dbcfcc1` (같은 커밋에서 두 번 빌드 = 바이트 같음) |
| TXT 크기 | 109,746 바이트 |
| 묶음 (tar.gz) sha256 · 크기 | `0148717655e79db4ab8ea5fbd1baeb40570e37fa322a645f074afe6b0fb0f57c` · 80,472 바이트 |
| 묶음 안 파일 · `SOURCE_SHA256SUMS` sha256 | 18 · `3f43e053b8dc3901658eb9892120b348df9e3895a8376489a177372003baadc2` |

같은 커밋에서 두 번 빌드한 TXT 는 바이트가 같았다.  ⚠ 반입 (cherry-pick) 으로 커밋 번호가 바뀌면 이 TXT 의 `RELEASE` 는 가지에 없는 커밋이 된다 → 반입 커밋에서 다시 빌드하고 그 이름 · 해시를 1저자에게 준다:

```bash
python3 -I -X utf8 -B docs/reviews/suyoung_next_registrations_20261125/reg1_block/build_block.py . <반입 커밋> <리포 밖 새 폴더>
```

## 7. 이 컨테이너에서 CHECK_ONLY (Python 3.11.18 · NumPy 2.4.6)

- **진짜 TXT**: 겉 `sha256sum -c` OK → `source.tar.gz: OK` → `RELEASE=<고정 커밋>` (조수 가지에서 돌린 판 · B 판 TXT 는 같은 꼴로 바뀐 RELEASE 만 다르다) → `ENVIRONMENT_MISMATCH python=3.11.18 numpy=2.4.6 target=3.12.3/2.5.2` rc 1 에서 멈춤 — 정상 (환경 관문).  HOME 에 만든 것 0.
- **시험 경로** (같은 묶음에서 `TARGET_ENVIRONMENT` 한 줄만 이 컨테이너 값으로 바꾸고 목록 다시 계산 · 겉 TXT 없이 `bash run.sh CHECK_ONLY`): rc 0 · `ENVIRONMENT_OK` · `CORES cpu=0 core=[0, 0] cpu=1 core=[0, 1]` · 원천 일곱 `SOURCE_OK` · `PLAN_MATCHES_REGISTRATION reg1 50/50 reg2 14/14` · `TOTAL reg1 arms=50 cpu_h=3.34-4.76 two_core_wall_h=1.67-2.38 longest_limit_s=5640` · 시드 G1 · G2 (원판당 197 · 797 · 1,793 · 3,209 · 7,213 점 · 외곽선 256 · 512) · `MPM_STEPS 0` · 대기열 50 줄 (첫 줄 `R1-G2-S-E-V4-48` 21,775 걸음 · 한도 5,640 s · 끝 줄 `R1-G1-PLATE-P-V0-08` 454 걸음 · 600 s) · `READER_SELFCHECK_OK checks=14 solver_calls=0` · 끝 줄 `CONTACT_MINI_CHECK_ONLY_OK` · 예약 · 작업 · 반환 폴더 0.

## 8. 1저자 WSL 명령 (등록 §6 그대로)

```bash
# 새 빈 폴더에서 · 받은 TXT 와 .sha256 를 둔 뒤
PASTE=PASTE_SUYOUNG_CONTACT_MINI_63e104b07744_1125.txt
sha256sum --strict -c "$PASTE.sha256"
bash "$PASTE" CHECK_ONLY                              # 계산 0 · 끝 줄 CONTACT_MINI_CHECK_ONLY_OK
bash "$PASTE" GO_SUYOUNG_CONTACT_MINI_ONCE            # 1저자 GO 뒤 한 번 · 다시 치면 ALREADY_RESERVED · 어림 1.7–2.4 h
bash "$PASTE" READBACK "$RETURN_DIRECTORY"            # GO 끝 줄의 RETURN_DIRECTORY · 가압 0 회
```

돌려줄 것: 반환 폴더의 `suyoung_contact_mini_result.tar.gz` · `screen.txt` · `SHA256SUMS` (+ READBACK 화면).  ⚠ 이 셋은 리포에 넣지 않는다 (화면 · 실행 기록에 홈 경로가 있다) — 리포 기록은 등록 §8 의 세 파일 (`return_receipt.json` · `summary.json` · README).

## 9. 확인 못 한 것

- WSL 에서 한 번도 안 돌렸다 (CHECK_ONLY 포함).  이 컨테이너는 환경 관문에서 멈추는 것이 정상이다.
- 실제 `driver.py RUN` 을 블록 대기열로 돌린 적 없다 — GO 끝-끝 시험은 시험 전용 가짜 일꾼 (지어낸 숫자) 이다.  드라이버 RUN 자체는 드라이버 시험 (SMOKE · 잘린 일정) 이 본다.
- 실제 팔 시간 · 반환 크기 (trace 합 약 38 만 줄 · 합성 trace 로는 약 80 MB — 실제는 미측정).
- J2 는 걸음마다 값의 최대 (등록 그대로) — 판 반력이 걸음마다 튀면 관성이 아니어도 1/20 을 넘을 수 있다 [짐작 · 미측정].  그러면 J3 · J4 · J5 가 보류되고 처분이 줄 4 쪽으로 간다.
- J5 꺾임 정의 (§3 의 7) 가 NZ22 카드의 꺾임 읽기와 같은 정의인지 모른다 (카드에 정의 없음).
- J1 · J3 은 U6(c) ⑥ 규칙 파일을 그대로 부르므로 같은 식이다 (시험: 무작위 곡선 다섯에서 결과 칸이 `force_rule.compare` 와 같음 · 5 % 경계 21.0 / 21.01).  ⑥ 자체의 판정력 (1.5 배 · 두 배 쌍) 은 이 블록이 보지 않는다.

## 10. 등록 · 드라이버와 어긋난 곳 (고치지 않음)

- 드라이버 `Monitors` 는 원판 하나 팔 (G1) 의 가로 어긋남도 `technical_hold_reasons` 에 `LATERAL_OFFSET` 으로 적는다.  등록 §4-4 는 G2 위 원판만 지목한다 → 판독기는 등록대로 G2 만 보류하고, 드라이버 표지는 `monitors.driver_technical_hold_reasons` 에 그대로 옮긴다.
- 등록 §6 CHECK_ONLY 의 "서로 다른 core_id" — 블록은 Q13 처럼 (physical_package_id, core_id) 쌍으로 가른다 (소켓 하나인 WSL 에서는 같은 뜻).
- 등록 숫자 (팔 · 걸음 · 한도 · 점 수 · 시간) 와 어긋난 곳은 없다 (드라이버 `registration_problems` 0 건 · 블록 계획 대조 0 건).

## 11. 1저자가 정할 것

- **Q-B1** 판독기 해석 일곱 (§3) — 권고: 그대로 (모두 결과 0 건일 때 고정했고 등록이 정한 숫자 · 식은 건드리지 않는다).
- **Q-B2** 반입 커밋에서 TXT 다시 빌드 → 1저자 WSL CHECK_ONLY → GO — 권고: 그 순서 (이 TXT 의 `RELEASE` 는 이 가지의 커밋이다).
- **Q-B3** 게이트 단계 (이 시험 약 140 초 · `mutation_probe.py` 는 넣지 않음) — 권고: 반입 때 한 단계 (드라이버 Q-D7 과 같이).

## 12. 근거

등록 ① `docs/reviews/suyoung_next_registrations_20261125/reg1_contact_mini_20261125.md` §2–§8 · 드라이버 `docs/reviews/suyoung_next_registrations_20261125/driver/README.md` · U6(c) ⑥ `docs/reviews/suyoung_u6c_force_rule_20261122/rule.json` · Q13 블록 `docs/reviews/suyoung_q13_setting2_20261125/` · Q13 반환 판독 `docs/reviews/suyoung_q13_return_20261125/`.
