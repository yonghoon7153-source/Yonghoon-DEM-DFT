# 믹서 D2 개발 소비자 재검토 (10-27) — MXD2R-01 · 02 · 03 수정 계획 초안 (2026-10-30 · ⬜ 1저자 비준 대기)

> 근거 = Codex 독립 재검토 `docs/reviews/codex_mixer_d2_review_20261027/codex_review_mixer_d2_20261027.md` (리뷰 핀 `045e0b309` · `codex/mixer-mxd2` · 요청서 `docs/reviews/codex_mixer_d2_consumers_request_20261024.md`) · 반입 `docs/reviews/codex_mixer_d2_review_20261027/README_import.md` (우리 트리 재현 = 판정값 차이 0 · 반례 CLI rc 판정문과 같음).
> 판정 요지: **HOLD** — MXD2-01 의 개발 소비자 하위 범위도 닫히지 않는다 · 새 P1 둘 · P2 하나 · **정상 덱 산술 (밀도 세대 · 상별 계획수 · 인쇄 CED 로 SE Bo) 은 수용** · `--d2-plan` 이 증서 · 실행 GO 를 만들지 않음도 수용.
> 범위: 개발 소비자 셋 `scripts/mixer_deck_readback.py` (`--d2`) · `scripts/mixer_deck_diff.py` (`--allow D2`) · `scripts/mixer_smoke_blind.py` (`--d2-plan`) + 회귀 `scripts/test_mixer_d2_consumers.py` · `/mixer` 개발 이력 (같은 묶음).  생성기 `scripts/make_mixer_deck.py` 의 정상 출력 · 등록 표 (E · E0 · DT · B · U) · 봉인 32 · 실행 정책은 건드리지 않는다.  **이 문서는 계획만 — 코드는 고치지 않았다.**

## 1. 결함과 최소 해결 (판정문 §3 · §4 · §5 그대로)

| ID | 결함 | 자리 (핀 `045e0b309` = 우리 기반 같은 바이트) | 최소 해결 (판정문) |
|---|---|---|---|
| `MXD2R-01` P1 | 명령 토큰이 같아도 시간 · 삽입 · 회전 계약이 달라진다 — 두 덱에 같은 `run N upto` · 마지막 run 뒤 `timestep` · 삽입 `start 9000000` · Front 주기 0.1 s 를 넣고 메타를 다시 묶으면 세 소비자 PASS / rc 0 (upto 실제 증분 `[1, 560605, 0, 6034776]` · 최종 step 7,716,595 → 6,595,382 · 회전 2.00008713 → 1.83008017 · 삽입 fix 가 start 전에 제거) | `mixer_deck_readback.py:167–171` (timestep 위치 무시 · run 첫 정수만) · `:981–1003` · `:1104–1179` (run 옵션 · dt 효력 시점 · 삽입 start · 끝판 주기 의미 없음) · `:1291–1321` · `mixer_deck_diff.py:169–204` · `mixer_smoke_blind.py:245–252` | 개발 덱 지원 문법을 닫는다 — 생성기 문법만이면 `run <정수>` 두 토큰만 · dt 는 첫 run 전 한 번 · 이후 불변 · 삽입 `start` · 반복 옵션 거부 (또는 실제 활성 구간 · 스케줄 계산) · Drum/Front/Back 주기 · 축 · 원점 · 시작/종료를 공동 회전 계약에 각각 결합 · 두 덱 같은 변경 상주 회귀 |
| `MXD2R-02` P1 | `neigh_modify exclude type 3 3` (SE–SE 이웃 제외 = 그 쌍 상호작용 끔) 을 두 덱에 넣어도 세 소비자 PASS / rc 0 · 정상 SE–SE CED · Bo 를 그대로 낸다 · 보조: `coefficientFriction` 행렬 fix 삭제도 PASS (별도 finding 아님) | `mixer_deck_readback.py:1240` (허용 명령 `neigh_modify` · 인자 의미 제한 없음) · `:1248–1252` (pair/wall 모델 문자열만) · `:1271–1290` (인쇄 행렬로 힘 · 겹침) | 지원 `neigh_modify` 문법 고정 · 접촉 제외 옵션 거부 · 지원 pair/wall 모델에 필요한 재료 fix 의 완비성 · 적용 전 순서 명시 · 모르는 의미는 개발 소비자에서 명시 거부 (임의 LIGGGHTS 입력 전체 해석 불필요) |
| `MXD2R-03` P2 | 파일 바이트 해시 ↔ 정규화 텍스트 해시 — CRLF 덱 (13,833 B · `0b92f856…`) + LF 메타 (13,654 B · `32033f6b…`) = rc 0/0/0 · 실제 CRLF 해시 · 길이를 적으면 1/1/1 | `mixer_deck_readback.py:1196–1199` (`text.encode('utf-8')`) · `:1358` · `mixer_deck_diff.py:838` · `:1798` · `mixer_smoke_blind.py:985` (텍스트 읽기 = 개행 정규화) | CLI 에서 `read_bytes()` 로 실제 바이트의 해시 · 길이를 먼저 확인 → 검증한 바이트를 디코딩해 파싱 · LF 만 지원이면 CRLF 를 구체 사유로 거부 · 정규화 해시를 쓰려면 별도 이름 · 규약 + 물리 파일 해시 따로 보존 · 세 CLI 양방향 회귀 |

## 2. 1저자가 정할 것

| Q | 결정 | 선택지 | 권고 |
|---|---|---|---|
| Q1 (`MXD2R-01`) | 시간 · 삽입 · 회전 명령을 어디까지 받나 | (가) **생성기 자신의 문법만** 받고 모르는 의미는 거부 — `run <정수>` 두 토큰 · `timestep` 은 첫 run 전 한 번 · 삽입 fix 의 `start` · 반복 옵션 거부 · 세 메시의 회전 주기 · 축 · 원점 · 시작/종료를 각각 계약에 묶음 · (나) LIGGGHTS 의미를 계산 (upto 증분 · dt 효력 시점 · 삽입 스케줄 · 메시별 회전) | **(가)** — 개발 덱은 생성기가 만든다 · 의미 계산은 표면이 커서 새 반례를 부른다 (판정문도 "현재 생성기 문법만 지원한다면" 을 먼저 든다) |
| Q2 (`MXD2R-02`) | 접촉 제외 · 재료 fix 를 어떻게 막나 | (가) **접촉 제외 거부** (`neigh_modify` 는 생성기가 쓰는 정확한 꼴만 · `exclude` 등 모르는 옵션 거부) + 지원 pair/wall 모델이 요구하는 재료 fix (영률 · 포아송 · 반발 · 마찰 · 구름 마찰 · CED 행렬) **완비성 · 적용 전 순서** 검사 · (나) `exclude` 만 거부 | **(가)** — 같은 부류 (보조 탐침의 마찰 행렬 삭제) 까지 한 번에 닫는다 · 재료 fix 목록은 생성기 덱에서 뽑아 정확히 비교 |
| Q3 (`MXD2R-03`) | 해시 · 개행 규약 | (가) **실제 파일 바이트를 먼저 해시** · 길이 확인 → 그 바이트를 디코딩 · CRLF 는 구체 사유로 거부 (LF 만 지원) · (나) CRLF 를 받되 정규화 해시를 별도 이름으로 · 물리 바이트 해시도 보존 | **(가)** — 생성기는 LF 만 쓴다 · 메타의 `deck_sha256` 는 그대로 "실제 파일 바이트" 뜻으로 남는다 · 세 CLI 양방향 회귀 (LF 메타 + CRLF 덱 = 거부 · CRLF 메타 + CRLF 덱 = CRLF 사유로 거부) |

## 3. 순서 (비준 뒤 · 시험 먼저)

| 단계 | 할 일 | 통과 기준 |
|---|---|---|
| 1 | 반례를 `scripts/test_mixer_d2_consumers.py` 에 **먼저** 옮긴다 — Codex 탐침의 공통 변조 여섯 (`run_upto` · `late_timestep` · `insert_start_late` · `front_period` · `exclude_SE_SE` · `friction_missing`) · CRLF 두 방향 · 세 CLI 와 API 모두 | 고치기 전 코드에서 새 시험이 **옳은 이유로 실패** (각 반례 PASS = 시험 실패) · 기존 13 메서드는 그대로 통과 |
| 2 | Q1–Q3 결정대로 세 소비자 수정 | 새 반례 전부 거부 (API FAIL · CLI rc 1 · 사유 문구) · 음성 대조 둘 (중력 · 적분기) 그대로 거부 |
| 3 | 양성 보존 (판정문 §7 최소 해제 증거 (4)) | 정상 2 상 / 3 상 · 밀도 두 세대 · 층상 / 균일 · ρ = 1 퇴화 비교 · Codex 독립 정상 48 조합 · `--d2-plan` 의 `registered=null` · `execution_authorized=false` 유지 |
| 4 | 구 경로 회귀 | `mixer_deck_readback --selftest` 24/24 · `mixer_deck_diff --selftest` 55/55 · `mixer_smoke_blind --selftest` rc 0 (10-30 Linux 기준값 · 반입 `_repro_ours_20261030/legacy_selftests_linux/`) |
| 5 | 웹앱 `/mixer` 개발 이력 (같은 묶음 · 코드 → 웹앱 순차 반영) · 원장 MXD2R-01–03 claimed_fixed | 개발 덱 문법 한정 문구 · 해시 = 파일 바이트 |
| 6 | 사전 공격 리뷰 (보장마다 작은 반례 · 변이 시험) → 게이트 → Codex 짧은 재확인 (수정 diff + 반례 회귀 + 입력 지문) | Codex 재확인 GO 전에는 MXD2-01 개발 소비자 하위 범위 종결을 주장하지 않는다 |

- 닫지 않는 것: 새 S1 셀 · 코호트 · 정책 구현 · 등록 · 실물 입력 (MXD2-01 (3)) · 생성기 쪽 `MXD2-02`–`07` · 실제 DEM · 믹서 실행.
