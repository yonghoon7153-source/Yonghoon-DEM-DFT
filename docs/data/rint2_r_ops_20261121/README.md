2026-11-21 15:51 KST · gabia P1 사다리 `attempt_2`가 rc 3으로 정상 종료했음을 1저자 화면에서 확인했다. 사슬 끝 줄은 원장 잠금 파일 열기 실패(`ATTEMPT_LEDGER_MISMATCH`), 원장 자리에는 `ca1_ledger.parked`만 존재, `ladder_summary.json` 존재, 팔 JSON 54개, 사슬 프로세스 0개였다.

# Rint ② R 운영 기록

## 사다리와 원장

| 시각 | 기계 | 관측 또는 원장 동작 | 상태 |
|---|---|---|---|
| 11-20 10:36 KST | kgy | P0 사다리 `attempt_1` 종료, 원장 재수신 뒤 같은 기계에서 recover | 종료 rc 3, recover rc 0. origin8의 `CALIB_ORIGIN_SENSITIVE`와 등록 R_j,0 유지 |
| 11-21 15:51 KST | gabia | P1 사다리 종료. 1저자의 읽기 전용 화면에서 위 세 조건 확인 | rc 3 정상 종료. P1의 원장 채택은 recover 뒤에 확인 |
| 11-21 16:00 KST 인계 | kgy → gabia | 원장 넘김 ③과 같은 원위치의 P1 recover | 실행 전. 현 원장 보유자는 kgy. ③의 실제 UTC·HEAD·묶음 해시 대기 |
| 11-21 16:17:16 → 16:17:19 KST | kgy → gabia | 1저자 넘김 ③, flock, master | RECV_OK. gabia 활성, kgy parked |
| 11-21 16:18:28 KST | gabia | 같은 원위치에서 P1 `attempt_2` recover, 수신 HEAD에서 복구 HEAD로 이동 | rc 0 · completed · RECOVER_OK. 복구 직후 원장 끝 `190dd1aec0e99c76ebb4d87679b9178855676f4b` |
| 11-21 P1 복구 뒤 (완료 시각 미표시) | 양쪽 | 채택 사다리 P0·P1 상호 복사 | 각 147파일, 양쪽 BOTH_EQUAL · LADDERS_COPIED_AND_VERIFIED. 첫 단위 시작 영수증 대기 |
| 11-21 교차 복사 뒤 (등록 시각 미표시) | gabia | 첫 단위 `P1_c0_R_j_lo`, 시도 3 등록 및 분리 기동 | REGISTERED_AND_DETACHED, 등록 커밋 `8172c5141f78776216350d897ac617c4c8f970df`. 시작 행·그룹 확인 대기 |
| 11-21 넘김 ④ 전 | gabia | 시도 3 START_OK, 그룹 1개 | 시작 HEAD `a525c9afba6456475f82899ce2a5d225994dae0d`, 넘김 직전에도 해당 사슬 확인 |
| 11-21 16:40:04 → 16:40:08 KST | gabia → kgy | 원장 넘김 ④, STARTED 3 | kgy RECV_OK. 원장 보유자는 kgy. 두 쪽 사다리 완료, 단위 완료 0/12 |
| 11-21 넘김 ④ 뒤 | kgy | P0·P1 각 147파일 BOTH_EQUAL 재확인, `P0_c0_R_j0` 시도 4 등록·분리 기동 | REGISTERED_AND_DETACHED, 등록 커밋 `50d6a1a04fd3c7df6e310c232406f9e4b3734ecd` |
| 11-21 시도 4 등록 뒤 | kgy | 같은 기계·단위·시도 START_OK, 그룹 1개 | 원장 끝 `57389b26924a86584ab7b77e9165a80a209e61a7`. 양쪽 첫 단위 시작 확인, 종료 영수증 0/12 |
| 11-22 09:27:35 KST 화면 | gabia | `P1_c0_R_j_lo` 시도 3, 시작·종료 그룹 2/2, 팔 JSON 6개 | 종료 rc 3 |
| 11-22 넘김 ⑤ 전 (조회 시각 미표시) | 양쪽 | gabia 시도 3 status, 이어서 kgy 시도 4 status | gabia parked·요약·normal_parked_end 모두 true. kgy 시도 4의 rc는 null, 요약 미수령 |
| 11-22 09:42:11 → 09:42:14 KST | kgy → gabia | 넘김 ⑤, STARTED 4, gabia의 parked 종료 목록에 시도 3 한 건 | `RECV_OK`. 활성 원장은 gabia |
| 11-22 넘김 ⑤ 뒤 (회복 시각 미표시) | gabia | 원위치에서 시도 3의 기존 결과를 원장에 회복 | 회복 뒤 HEAD `51927c7c22d378d6c6a4382a842e7b3962eb9904`. 단위 완료 1/12 |
| 11-22 시도 3 회복 뒤 (등록 시각 미표시) | gabia | P0·P1 각 147파일의 양쪽 바이트·SHA256 재대조 후 `P1_c0_R_j_hi` 시도 5 등록·분리 기동 | 두 사다리 `BOTH_EQUAL`, `REGISTERED_AND_DETACHED`. 등록 커밋 `ea2433a170466fdc0fe40129b5661871a9893972`. 시작 행·그룹 확인 대기 |
| 11-22 시도 5 등록 뒤 (시작 시각 미표시) | gabia | `P1_c0_R_j_hi` 시도 5의 `START_OK`, 시작 그룹 1개 | 시작 HEAD `8ec18d69fcaadf75e8ca2aa053e64ebb42e17b93`. 단위 완료 1/12, kgy 시도 4 상태 재조회 대기 |
| 11-22 13:21:55 KST 화면 및 뒤이은 status | kgy | 시도 4 그룹 2/2 종료, 팔 JSON 6개, rc 3. parked=true, summary_present=true, normal_parked_end=true | 기존 결과의 원위치 recover 대상 |
| 11-22 13:30:42 → 13:30:46 KST | gabia → kgy | 넘김 ⑥, STARTED 5. kgy 수신 목록에 시도 4 한 건 | RECV_OK. 활성 원장은 kgy |
| 11-22 13:36:29 KST 영수증 | kgy | 시도 4 원위치 recover, rc 0, completed | 복구 뒤 원장 HEAD `f63c36ca21be73e1ef416d6a18a503163ff13413`, 단위 완료 2/12 |
| 11-22 시도 4 회복 뒤 (등록·시작 절대 시각 미표시) | kgy | `P0_c0_R_j_lo` 시도 6 등록 `b93f30c4160e66e5ae6fa3a8256253abb4fb378a`, 이어서 START_OK · 그룹 1개 | 마지막 확인 원장 HEAD `de3913418e4618721ff8d96a65a9cacada32d4e8` |
| 11-22 16:33 KST 화면 | gabia·kgy | 시도 5와 6 각각 시작 그룹 1, 종료 0, 팔 JSON 1, exit_rc=PENDING | 이 화면 뒤 종료 여부는 복귀 첫 status에서 확인 |

## 넘김

| 차례 | 묶음 UTC | 방향 | 보낼 때 실제 HEAD | 묶음 SHA256 | 수신 |
|---|---|---|---|---|---|
| ① | 20261118T050239Z | kgy → gabia | `bcff6b0235a39ec799ef18f733b1599bfdb50463` | `fa63d348cd7065f86d695b1bae9a6d99bbe46536ba60c9471782190c84eb7d63` | 양쪽 대조, RECV_OK |
| ② | 20261120T022342Z | gabia → kgy | `7b43cc81df6d68e2c0094f4e6afd98243f265173` | `6bb6318bd83388bdccf417fad02e032c50a057589c8b7ac5975fc65a121a87dd` | 양쪽 대조, RECV_OK. 이후 kgy에서 P0 recover |
| ③ | 20261121T071716Z | kgy → gabia | `3be5856df670276eb2ca450d260ba1c9534efaee` | `0b1d36d19c25e5cbda52248d3a20086f21b8757c616c7e6e8c5b57663c226aa5` | 20261121T071719Z · RECV_OK |
| ④ | 20261121T074004Z | gabia → kgy | `a525c9afba6456475f82899ce2a5d225994dae0d` | `99ad84e2548555e77571e15a144e63227c3e363a2dd7a7e94eb095623bdb5743` | 20261121T074008Z · master · flock · RECV_OK |
| ⑤ | 20261122T004211Z | kgy → gabia | `57389b26924a86584ab7b77e9165a80a209e61a7` | `8d18507d428a7b7d7589843a1d309ab414da58ba7a5a4f0eef59cc88de3d5baf` | 20261122T004214Z · master · flock · RECV_OK. 수신 목록에 `unit:P1_c0_R_j_lo` 시도 3 |
| ⑥ | 20261122T043042Z | gabia → kgy | `8ec18d69fcaadf75e8ca2aa053e64ebb42e17b93` | `84efb1d74a2f764f08c540c5ca4c3eec05df3031eaf11a0cf255b009aded9150` | 20261122T043046Z · master · flock · RECV_OK. 수신 목록에 `unit:P0_c0_R_j0` 시도 4 |

①·②의 근거는 `docs/data/rint2_r_start_20261118/README.md`의 ‘그 뒤’다. ③은 1저자 WSL의 `transfer.json`과 `recover_2.json`을 화면과 대조했다. ③의 수신 HEAD와 P1 recover의 시작 HEAD가 40자리 모두 일치했다. 사다리 복사에는 복구 **후** HEAD를 사용한다.

## 1저자가 이어갈 차례

복사 확인은 1저자 WSL 화면에 표시된 두 줄과 완료 표지를 근거로 한다. 원장 끝은 P1 복구 후 HEAD였다.

| 사다리 | 전송 방향 | 파일 | 바이트 | 양쪽 폴더 SHA256 |
|---|---|---:|---:|---|
| P0 attempt_1 | kgy → gabia | 147 | 3,498,403,776 | `132069385076f435577bbeadfdc1a4d617da6a9b9d0d1de799fdc321756f2f3b` |
| P1 attempt_2 | gabia → kgy | 147 | 3,498,397,972 | `83f1264cfd25709cbc76a6daf14e308937b5d5297bc8cf8b589fc7a586f6cda1` |

마지막 확인 시점에 채택 단위는 2/12(시도 3·4)였다. gabia의 `P1_c0_R_j_hi` 시도 5, kgy의 `P0_c0_R_j_lo` 시도 6은 이미 등록·시작됐다. 1저자 WSL의 기존 운영 폴더에서 두 단위 status와 원장의 STATUS를 먼저 조회한다. 마지막 확인 당시 활성 원장은 kgy, gabia는 parked였으며 이후 상태는 새 영수증으로 갱신한다. 조회 결과와 봉인 §3-1b (4)–(7)에 따라 다음 넘김 또는 recover를 정한다.

| 기계 | 단위 순서 |
|---|---|
| gabia (5) | `P1_c0_R_j_lo` · `P1_c0_R_j_hi` · `P1_c1_R_j0` · `P1_c1_R_j_lo` · `P1_c1_R_j_hi` |
| kgy (7) | `P0_c0_R_j0` · `P0_c0_R_j_lo` · `P0_c0_R_j_hi` · `P0_c1_R_j0` · `P0_c1_R_j_lo` · `P0_c1_R_j_hi` · `P1_c0_R_j0` |

첫 DBE 모서리 실측을 받은 뒤 12-05 24:00 KST 주 판정 목표의 시간 여유를 다시 계산한다. 합치기·넘침·재검산은 봉인 §3-1b (6) 10–13 및 (7) 순서다. 현장 확인용 화면과 기록에는 작업 신원, 파일 수, 시각, rc, 원장 동작만 남긴다. 판정값은 `verdict_results.json`에 두며 열람 주체는 1저자다.

근거 핀은 봉인 `29643188524f`, 코드 `64e4d213e`다. 봉인 가지의 `docs/reviews/rint2_kgy_commands_20261020.md` 및 `docs/reviews/rint2_seal_20261118/registration_R_sealed.md`를 따른다.
