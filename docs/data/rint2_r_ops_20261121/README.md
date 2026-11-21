2026-11-21 15:51 KST · gabia P1 사다리 `attempt_2`가 rc 3으로 정상 종료했음을 1저자 화면에서 확인했다. 사슬 끝 줄은 원장 잠금 파일 열기 실패(`ATTEMPT_LEDGER_MISMATCH`), 원장 자리에는 `ca1_ledger.parked`만 존재, `ladder_summary.json` 존재, 팔 JSON 54개, 사슬 프로세스 0개였다.

# Rint ② R 운영 기록

## 사다리와 원장

| 시각 | 기계 | 관측 또는 원장 동작 | 상태 |
|---|---|---|---|
| 11-20 10:36 KST | kgy | P0 사다리 `attempt_1` 종료, 원장 재수신 뒤 같은 기계에서 recover | 종료 rc 3, recover rc 0. origin8의 `CALIB_ORIGIN_SENSITIVE`와 등록 R_j,0 유지 |
| 11-21 15:51 KST | gabia | P1 사다리 종료. 1저자의 읽기 전용 화면에서 위 세 조건 확인 | rc 3 정상 종료. P1의 원장 채택은 recover 뒤에 확인 |
| 11-21 16:00 KST 인계 | kgy → gabia | 원장 넘김 ③과 같은 원위치의 P1 recover | 실행 전. 현 원장 보유자는 kgy. ③의 실제 UTC·HEAD·묶음 해시 대기 |
| 인계 시점 | 양쪽 | 양쪽 채택 사다리의 상호 복사, 단위 사슬 | 복사 전, 시작 및 완료 단위 0/12 |

## 넘김

| 차례 | 묶음 UTC | 방향 | 보낼 때 실제 HEAD | 묶음 SHA256 | 수신 |
|---|---|---|---|---|---|
| ① | 20261118T050239Z | kgy → gabia | `bcff6b0235a39ec799ef18f733b1599bfdb50463` | `fa63d348cd7065f86d695b1bae9a6d99bbe46536ba60c9471782190c84eb7d63` | 양쪽 대조, RECV_OK |
| ② | 20261120T022342Z | gabia → kgy | `7b43cc81df6d68e2c0094f4e6afd98243f265173` | `6bb6318bd83388bdccf417fad02e032c50a057589c8b7ac5975fc65a121a87dd` | 양쪽 대조, RECV_OK. 이후 kgy에서 P0 recover |
| ③ | 미실행 | kgy → gabia | ③ 송신 시 잠금 아래에서 읽음 | 미수령 | RECV_OK 대기 |

①·②의 근거는 `docs/data/rint2_r_start_20261118/README.md`의 ‘그 뒤’다. ③의 새 줄은 송신·수신 영수증의 UTC, HEAD, SHA256을 대조한 뒤 채운다. ②의 HEAD 이후에 P0 복구 기록이 추가됐다.

## 1저자가 이어갈 차례

1. 봉인 명령 §3-1b (5)로 넘김 ③을 완료하고 양끝의 HEAD·해시 및 수신을 확인한다. 전송이 끊기면 양쪽의 원장 자리를 우선 확인한다.
2. gabia에서 같은 부팅과 원위치를 확인하고 P1 `attempt_2`를 recover한다. rc 0과 해당 원장의 채택 기록을 확인한다. 부팅이 달라졌거나 기록이 모호하면 1저자가 확인한다.
3. 봉인 §3-1b (6) 7에 따라 kgy의 채택 P0, gabia의 채택 P1을 같은 상대 위치로 교차 복사하고 양끝 파일 집합과 바이트를 대조한다.
4. §3-1b (4), (6) 8–9에 따라 원장을 가진 기계부터 단위를 연다. 각 기계에서는 한 번에 한 사슬을 돌린다. 실제 시작 행과 프로세스 그룹 기록을 확인한 뒤 다른 기계로 원장을 넘긴다. rc 3으로 끝난 단위는 해당 기계에 원장이 돌아온 뒤 같은 시도에서 recover한다.

| 기계 | 단위 순서 |
|---|---|
| gabia (5) | `P1_c0_R_j_lo` · `P1_c0_R_j_hi` · `P1_c1_R_j0` · `P1_c1_R_j_lo` · `P1_c1_R_j_hi` |
| kgy (7) | `P0_c0_R_j0` · `P0_c0_R_j_lo` · `P0_c0_R_j_hi` · `P0_c1_R_j0` · `P0_c1_R_j_lo` · `P0_c1_R_j_hi` · `P1_c0_R_j0` |

첫 DBE 모서리 실측을 받은 뒤 12-05 24:00 KST 주 판정 목표의 시간 여유를 다시 계산한다. 합치기·넘침·재검산은 봉인 §3-1b (6) 10–13 및 (7) 순서다. 현장 확인용 화면과 기록에는 작업 신원, 파일 수, 시각, rc, 원장 동작만 남긴다. 판정값은 `verdict_results.json`에 두며 열람 주체는 1저자다.

근거 핀은 봉인 `29643188524f`, 코드 `64e4d213e`다. 봉인 가지의 `docs/reviews/rint2_kgy_commands_20261020.md` 및 `docs/reviews/rint2_seal_20261118/registration_R_sealed.md`를 따른다.
