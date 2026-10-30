# LHS214 다시 발사 기록 — 194 + 보충 20 (10-30 · 승인 핀 B7 · 1저자 WSL)

- 무엇: Codex S2 발사 확인 범위 GO (10-30 · `docs/reviews/codex_lhs214_relaunch_review_20261030/`) 뒤 1저자 ⑤ 발사 승인 (10-30 채팅 *"ㅇㅇ"*) → 등록된 수동 순서로 실행 (연구실 PC WSL `~/dem-audit` · 단계마다 따로): 0 현장 확인 → 194 `run` → 완료 확인 · audit → 보충 20 `run` → 두 manifest + 전체 40 자리 승인 SHA 발사 영수증 → 읽기 전용 검사 (보충 audit · 두 다시 읽기).
- 승인 핀 B7 `35f0327377a4213774010a090df4d224e50d29e1` · ROOT = 10-28 사전 점검 때 이름 그대로 `/home/yonghoon71/net194_35f032737_1028` · `/home/yonghoon71/netsupp20_35f032737_1028` · `PY` = `/home/yonghoon71/Yonghoon-DEM-DFT/.venv/bin/python3`.
- 받은 파일 (1저자 10-30 업로드 · 이 폴더 = 받은 바이트 그대로 · 1저자 쪽 sha256 줄은 받지 못함 — 아래는 받은 바이트의 값):

| 파일 | 바이트 | sha256 |
|---|---|---|
| `net194_35f032737_1028_20261030_records.tar.gz` (멤버 402 · 경로 이탈 · 링크 0) | 566,730 | `d07a82e1f379016bc3131efc0989965daf30344d6a9746032f4cb3b2be3a059e` |
| `netsupp20_35f032737_1028_20261030_records.tar.gz` (멤버 51 · 경로 이탈 · 링크 0) | 73,985 | `e0c45ad48bf1ada488b01ecf1531e99bdb60a9e64898dfecacecfb3bbabc3940` |
| `launch_receipt_35f032737_1030_0917.json` (발사 영수증 · `supp20_input_receipt/v1` · 범위 launch) | 8,805 | `4c7d64905b7f1a7da119a718d9874010391ebf19b7a4a4e5a30bf5aacd69d62c` |

- 묶음 안 = manifest · runs · progress.tsv · seal_audit (tsv · json) · reread.json · merged (merge_report · 코호트 status · metrics_flat · parallel_cases) · cases/*/worker.json · log.txt (케이스 결과 원본 · 작업 폴더 · τ · 압력 · 인계표 = 빼고 · 실행기 안내 ③ 에서 그 셋을 뺀 목록).

## 1저자 화면 (채팅 붙여 넣기 · 10-30)

| 단계 | 화면 |
|---|---|
| 0 | `PIN=35f0327377a4213774010a090df4d224e50d29e1 (40자) · S=35f032737` (3 단계 첫 줄) |
| 194 `run` | watch 09:06 = `{'done': 194}` · 도는 중 없음 (`194 run rc` 줄 = 붙여 넣기에 없음) |
| 194 audit | `audit rc=0` · `{'SEALED': 194}` · merged `{'same': 194}` · 세대 `g2` 194 · 입력 지문 = 발사 기록 · import 관측 970 (시작 = 끝맺음) · 완료 시도 194 · 모듈 30 ⊆ 봉인 32 · 결합 = 완료 시도 `True 194 194` · expected ≠ observed `[]` · 감사 문제 `[]` · 미최종 0 |
| 보충 20 `run` | `[20/20]` 전부 `rc=0` · `{'done': 20}` · 0.079 h · `{'SEALED': 20}` · `supp20 run rc=0` |
| 발사 영수증 | `rc 0 — 대조 26 칸 · 다름 0` · F7 · G7 = 두 manifest `git.sha` = 승인 SHA (전체 40 자리) · H1 = 새 ROOT 둘 · 같은 발사 커밋 · 같은 봉인 지문 |
| 보충 audit | `supp20 audit rc=0` · `{'SEALED': 20}` · merged `{'same': 20}` · 세대 `g2` 20 · 입력 지문 = 발사 기록 · import 관측 100 (시작 = 끝맺음) · 완료 시도 20 |
| 다시 읽기 | `194 reread rc=0` · `supp20 reread rc=0` · 둘 다 `✓ 전부 통과` |

## 메인 대조 (이 컨테이너 · 받은 묶음을 빈 폴더에 풀어 `python3 -I` 로 읽기만)

| 칸 | 194 | 보충 20 |
|---|---|---|
| manifest `git.sha` · dirty | `35f0327377a4213774010a090df4d224e50d29e1` · false | 같음 · false |
| observe_imports · 관측 run id | true · `8bfa29d8…` | true · `75134598…` |
| code_fp · 기대 망 세대 | `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` · `g2` | 같음 · `g2` |
| 계획 수 · 입력 지문 n · ids | 194 · 194 · `a04282d7275bd8f9…` (등록 §2) | 20 · 20 · `991cf1150b183f64…` (보충 등록 §2) |
| seal_audit 판정 · 문제 · 시작/끝맺음 | `{'SEALED': 194}` · `[]` · 970/970 | `{'SEALED': 20}` · `[]` · 100/100 |
| merged 케이스 기록 상태 | `{'done': 194}` | `{'done': 20}` |
| reread n_fail · 집합 | 0 · production194 · 194 = 194 · set_equal true · missing/extra `[]` | 0 · supp20 · 20 = 20 · set_equal true · `[]` |
| 발사 영수증 (JSON) | — | rc 0 · 검사 26 모두 ok · approved_sha = B7 40 자리 · registration code_fp_pending null · warnings `[]` |

## 한정

- 이 기록 = 발사 확인 범위 (Codex S2 GO) 의 실행 결과 — 등록 §5 판정 (결과 자격 · 공란 의미 · Hertz 주 타깃 · 결과 보고) · τ 진단 · 압력 기록 · 인계표 v1.3 생성 · 배포 = 다음 단계 (v1.3 배포 = 따로 HOLD · H0 모형 한계 행).
- 다시 읽기 화면의 `physics NOT_COMPUTED` · `MODEL_BELOW_CONTINUUM_BOUND` 표지 = 등록된 모형 한계 표지 (레코드 게시 가능 · 194 §9-8) — 오류 아님.
- 케이스 결과 원본 (`merged/*/results` · 작업 폴더) 은 1저자 WSL ROOT 에만 있다 (리포 미반입).
- `L214P-02` (P3 · `launch_eligibility` 1140 행 LF) 열림 — 이번 발사는 전체 40 자리 승인으로 운영 (영수증 F7 · G7) · 한 줄 수정 = 이 발사 뒤 (1저자 10-28 밤 *"다 권고대로"*).
