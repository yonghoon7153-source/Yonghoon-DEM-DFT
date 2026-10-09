# 재검증 6 사전 점검 (WSL 재확인 ①–⑤) — 10-09 21:13–21:17 KST

- 요청서: `docs/reviews/codex_gen2_network_reverify6_request_20261009.md` (`ff3118cd8` · 머리 명령 블록 · 결과 전 기대 표).
- 실행: 1저자 WSL `yonghoon71@DESKTOP-IK8J81H` · 체크아웃 `~/dem-audit` detached `956173e1c` (HEAD = origin) · dirty 0 · 파이썬 `~/Yonghoon-DEM-DFT/.venv/bin/python3` · numpy 2.5.2 · scipy 1.18.1 · networkx 3.7.
- 받은 것 = 묶음 `g2rr6_956173e1c_1009_2113.tar.gz` (37,324 B · sha256 `b147dcd5babefcad7897d7bba8dbe0ecbdffa3453edb96d45a86a2dd659a2cab` · 이 폴더에 원본 그대로) + 1저자 터미널 화면 (대화 붙여 넣기 — 아래 §1 의 0 단계 줄은 화면에서).

## 1. 받은 목록 (묶음 안 · 원 프로세스 출력 그대로)

| 파일 | 단계 | 내용 |
|---|---|---|
| `commit.txt` · `python.txt` | 0 | 커밋 전체 sha · 시각 · 파이썬 경로 |
| `g2pre_pilot_*.before` (둘) | 0 · 5 | 시범 ROOT 파일 목록 지문 (실행 전) |
| `st_reread.txt` · `st_runner.txt` · `st_smoke.txt` · `st_smoke_real.txt` | 1 | 도구 자체 시험 전체 출력 |
| `smoke.txt` · `smoke_report.json` · `smoke_summary.txt` | 2 | 스모크 전체 출력 · 보고 JSON (검사 id 포함) · 요약 |
| `smoke_reread.txt` · `reread.json` | 3 | `--smoke-root` 다시 읽기 출력 · 판정 JSON |
| `audit_<ROOT>.txt` · `audit_<ROOT>.json` (둘씩) | 4 | 고친 실행기 읽기 전용 재감사 (JSON 은 ROOT 밖) |
| `gate_readonly.txt` · `gate_readonly.json` | 5 | 고친 배포 관문 함수로 감사 JSON 읽기만 |

**받지 않은 것**: 케이스 파이프라인 산출물 원파일 (게시된 dual / full_metrics · 망 결과) · 스모크 ROOT 자체 · 시범 ROOT 자체 (읽기만 했다 · 실행 전후 파일 목록 지문만) · 194 dry-run (이번 범위 밖).

## 2. 결과 ↔ 결과 전 기대 (요청서 표)

| 단계 | 기대 | 결과 | 판정 |
|---|---|---|---|
| 0 | 커밋 = 요청서 커밋 이후 · dirty 0 | `956173e1c` (요청서 `ff3118cd8` 의 다음 커밋 · 진행 기록만) · dirty 0 | 같음 |
| 1 | rc 넷 0 · 23/23 · 124/124 · 16/16 · 4/4 | rc 0 × 4 · 다시 읽기 23/23 (✓ 24 줄 = 23 + 끝줄) · 실행기 124/124 · 스모크 16/16 · 실제 판 4/4 | 같음 |
| 2 | smoke rc 0 · case15 검사 일곱 각 한 번 전부 PASS · real14 · LHS 셋 = 10-07 값 · report rc 0 | smoke rc 0 · 검사 27/27 · `case15.proc` · `raw_sha` · `nc1_blocked` · `nc2_tau` · `nc3_cause` · `nc4_ionic` · `nc5_attempt` 전부 PASS · real14 σ_ratio 0.02102106 · 0.03164009 · 0.02494138 (= 등록 §1 참고값 8 자리) · lhs00_055 · lhsx_007 두 모드 computed · lhs00_128 valid_zero · τ NOT_PERCOLATING · report rc 0 | 같음 |
| 3 | `smoke_reread rc=0` · S0 · S0b | rc 0 · S0 (4 · 등록 음성 대조 1 제외 · 미등록 0) · S0b (등록 1 · 안정 ID 7 각 1 회 · 공용 판정 재계산 = 기록) · 네 케이스 세대 g2 · K1–K7 · H1 ✓ | 같음 |
| 4 | 두 ROOT audit rc 0 · SEALED 3 · 시작 15 = 끝맺음 15 · 완료 3 · ✗ 없음 | 두 ROOT rc 0 · SEALED 3 · merged same 3 · 레코드 세대 g2 3 · 입력 지문 = 발사 기록 · 프로세스 15 (시작 15 · 끝맺음 15) · 완료 시도 3 · 리포 모듈 30 ⊆ 봉인 32 · ✗ 없음 | 같음 |
| 5 | gate rc 0 · 두 ROOT 신원 · 관측 · 감사 관문 문제 0 · `stage_binding/v2` · 결합 시도 3 · expected=observed · unclassified [] · 계획 출처 (c3117438a = 지금 케이스 기록 · 839dbac6b = 시도 사본) · 파일 변화 없음 | 그대로 — c3117438a 결합 출처 `out/status.json 케이스 기록` · 839dbac6b `worker.json attempts[]` · 두 ROOT "파일 변화 없음" | 같음 |

⇒ **다섯 단계 모두 결과 전 기대와 같다.**  옛 v1 결합 기록 감사 대신 고친 실행기의 v2 결합 기록이 실제 시범 ROOT 둘에서 나왔고, 배포 관문 함수 (진단: 관측 필수 집합에 pilot3 를 더함) 가 둘 다 문제 0 으로 받았다.

## 3. 한정

- 194 생산 · v1.3 배포 · S3 를 돌린 것이 아니다 — 고친 검사 도구가 실제 WSL 기록 (기존 시범 ROOT 둘 · 새 스모크) 에서 기대대로 동작함을 보인 것.  194 발사 = Codex 재검증 6 GO 뒤 별도 발사 승인 (등록 §0 · §9-6).
- 5 단계의 관측 필수 검사는 진단 설정 (`V13_IMPORT_OBS_REQUIRED` 에 pilot3 를 더함) 이다 — 생산 배포 관문은 production194 에만 그 검사를 건다.
