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

## 11-23 순환 (Claude 기록 · 1저자 현장 실행)

| 시각 (KST) | 기계 | 일 | 결과 |
|---|---|---|---|
| 09:1x | gabia | 시도 5 `P1_c0_R_j_hi` 끝 | rc 3 · parked · normal_parked_end true (정상 끝) |
| 09:1x | kgy | 시도 6 `P0_c0_R_j_lo` 끝 | rc 0 · 원장 kgy ACTIVE · tip `d11cf1f6b81dc0d61f9983fe10bf1e6020ad1f75` |
| 09:2x | kgy | 시도 7 `P0_c0_R_j_hi` 등록 → START_OK | entry `65e56de02485c0247974955076f31272bca6abdb` · ledger_head `5ad5a30be72234fd9ec182a0552949463d38146b` |
| 09:28 | kgy → gabia | 넘김 ⑦ | RECV_OK · tip `5ad5a30b…` · 묶음 sha256 `c1877d80419abad0170b8dcb0a7e9b47adb8f9fbe746beb89ba337feeb868866` · 수신 = 시도 5 |
| 09:3x | gabia | RECOVER_UNIT 5 | RECOVER_OK · POST_RECOVER_HEAD `79ef1c91b20fc452565d48f4c616ae9d67a6a140` |
| 09:3x | gabia | 시도 8 `P1_c1_R_j0` 등록 → START_OK | entry `6374f6b85728631528b1c30f1fffa83eedc76429` · ledger_head `a8279d298b1f3ddaf577b1eef062a15576e13027` |

채택 단위 4/12 (시도 3 · 4 · 5 · 6) · 도는 중 2 (kgy 시도 7 · gabia 시도 8) · 남음 6.  다음 = kgy 시도 7 끝 (rc 3 예상) → 넘김 ⑧ gabia → kgy → RECOVER_UNIT 7 → kgy `P0_c1_R_j0` · gabia 시도 8 끝 → gabia `P1_c1_R_j_lo`.

**1저자 중간 열람 (11-23 09:5x KST · 판정 아님).**  1저자가 등록 R 밖에서 채택 단위 시도 3–6 의 런별 σ_e 를 열람했다 (합치기 · 넘침 · 재검산 전 값).  값은 이 기록 · 리포 어디에도 적지 않는다.  등록 R · 봉인 · 단위 순서 · 판정 규칙은 바꾼 것이 없다.  판정 문장에는 *"1저자 중간 열람 (11-23 · 시도 3–6 · 판정 전 값)"* 한정어를 붙인다.

## 11-23 저녁 — kgy 재부팅 뒤 손 회복 (Claude 기록 · 1저자 현장 실행)

| 시각 (KST) | 기계 | 일 | 결과 |
|---|---|---|---|
| 16:34 | kgy | 비정상 재부팅 (`last -x` = reboot 줄 · shutdown 줄 없음 · 원인 미확인) | 시도 7 `P0_c0_R_j_hi` 의 사슬 · 러너가 끝남 (부모 사망) · 그때 그룹 1/0 · 팔 JSON 2 |
| 18:45 | kgy | uwatch | groups 1/0 · chain_procs 0 · GPU 30 % · 851 MiB (아무것도 안 돌 때 값) → `uptime` 2:18 로 재부팅 확인 |
| 19:12 | gabia → kgy | 넘김 ⑧ — **수동** (봉인 명령 문서 `docs/reviews/rint2_kgy_commands_20261020.md` (5)) | 운영 도구에 재부팅 경로가 없다 (넘김 = 받는 쪽 시도가 park 로 끝났다는 증거를 요구 · 회복 = `unit_summary.json` 을 요구) → flock 아래 묶음 · park · 전송 · `pull --ff-only` · T `20261123T101251Z` · tip `a8279d298b1f3ddaf577b1eef062a15576e13027` · 묶음 sha256 `69e7c4ea62c27c7089f28a1873d889d0d8e0b555b2ac34a56d30699b367e31a9` · PARKED_OK · RECV_OK |
| 19:1x | kgy | `--stage recover` 시도 7 (다른 부팅 · `--operator-confirm 7`) | 결과 줄 interrupted · 원인 parent_dead · 재실행 자격 True · rc 0 · 원장 kgy ACTIVE · tip `bf0b6d54b0605058c950e1d1bd764879f8cde1d8` (넘김 전에 한 번 = 원장 없음 rc 3 · 무해) |
| 19:16 | WSL | 도구 launch | ALREADY_REGISTERED_NO_RETRY (도구가 같은 단위의 재등록을 막는다) → 봉인 (4) 절차 (등록 → 바로 실행) |
| 19:18 | kgy | `ledger --add` (새 시도) | ATTEMPT_AFTER_ADOPTED (시도 7 = 채택 시도 · 원장 무변경) |
| 19:1x | kgy | `ledger --add --resume 7` | ATTEMPT_ADDED n=9 · resume_of 7 · commit `fa5ed05703c7e0ee73037c229a2ced845d0f1206` |
| 19:1x–19:20 | kgy | 시도 9 nohup predict | 1–2 분 만에 `RUNNER_RC` rc 2 — 러너가 venv 를 켜기 **전** 런 영수증 줄의 `python3` = 1저자 창의 conda base (python 3.13 · scipy 없음) → `ModuleNotFoundError: scipy` · 결과 줄 stopped · side=pre · runner_rc · resume_ok False · 결과 전 멈춘 재실행 = 기록만 (`adoption` PC5-05 · 사슬 끝 = 시도 7 그대로) · 원인 = 내가 준 블록에서 venv 켜기 줄 누락 (`SELF-187`) |
| 19:3x | kgy | `--resume 7` 다시 → 시도 10 (conda 끔 · venv 켬 · python3 경로 · numpy · scipy 판을 확인한 뒤에만 등록 · 실행) | ATTEMPT_ADDED n=10 · `[p2] 런 영수증` · `[p2] 규율 검사 통과` · groups 1/0 · chain_procs 2 (19:33) |

손실 = 시도 7 의 계산 약 7 시간 + 빈 시간 약 3 시간 (추정 · 재부팅 16:34 → 시도 10 19:3x).  시도 7 의 첫 런 (`U01_corner`) 은 끝 기록이 없어 시도 10 이 처음부터 다시 돈다 (추정 · 재실행 요약 `resume` 칸으로 확인).
운영 도구의 빈 곳 (이번에 고치지 않음 · 기록만): 넘김 · 회복 · launch 세 곳이 정상 끝만 가정한다.  재부팅 뒤 손 경로 = 위 표 (봉인 (5) 넘김 · `--operator-confirm` 회복 · `--resume` 재등록 · **venv 켬 확인 뒤** 실행).
도는 중 2 (kgy 시도 10 · gabia 시도 8) · 채택 4/12 · 다음 = gabia 시도 8 끝 → 넘김 kgy → gabia → RECOVER 8 → gabia `P1_c1_R_j_lo` · 12-05 어림은 gabia 시도 8 시간을 본 뒤 다시.

## 11-24 – 11-25 순환 (Claude 기록 · 1저자 현장 실행)

| 시각 (KST) | 기계 | 일 | 결과 |
|---|---|---|---|
| 11-24 13:0x | gabia | 시도 8 `P1_c1_R_j0` 끝 | 그룹 3/3 · 팔 JSON 12 · 사슬 0 · parked 끝 (원장 = kgy) · 시간 = 모서리 37,362 s + origin 24,546 s |
| 11-24 13:0x | kgy | 시도 10 `P0_c0_R_j_hi` (시도 7 재실행) 끝 | 그룹 3/3 · 팔 JSON 12 · 사슬 0 · 원장 kgy 에서 스스로 끝 기록 · 시간 = 모서리 29,309.6 s + origin 17,806.3 s |
| 11-24 13:1x | kgy | `P0_c1_R_j0` 시도 11 첫 시작 | 넘김 (묶음 041455Z · 041725Z) 이 시작 기록보다 먼저 돌아 사슬 Exit 3 · 원장 끝 항목 11 그대로 (`ebc80f0d8…`) · 두 묶음 = 쓰지 않음 (지우지 않음) |
| 11-24 13:2x | kgy | 같은 번호 11 로 다시 시작 (원장 세우기 → 시작 기록 · 그룹 확인 뒤에만 넘김) | START_OK 11 · 원장 끝 `start 11` |
| 11-24 13:26 | kgy → gabia | 넘김 ⑨ | T `20261124T042600Z` · tip `c4bf7a077d2c043cbe424c37c3e259401ca87d49` · 묶음 sha256 `f110b2c08e4c654f716149115e9a15989cde4e9c10629cf023b568a10380b9ac` · PARKED_OK · RECV_OK |
| 11-24 13:3x | gabia | recover 8 → `P1_c1_R_j_lo` 시도 12 등록 · 시작 | recover8 rc 0 · START_OK 12 (원장 = gabia) |
| 11-25 07:19 · 07:27 | kgy · gabia | 시도 11 · 12 끝 (화면) | 둘 다 그룹 3/3 · 팔 JSON 12 · 사슬 0 · 두 GPU 의 사용량 (58 % · 90 %) = 우리 사슬 밖 프로세스 (미확인) |
| 11-25 07:44 | gabia → kgy | `P1_c1_R_j_hi` 시도 13 등록 · 시작 → 넘김 ⑩ | 원장 끝 `result 12 completed` → START_OK 13 (항목 커밋 `17f260b8599d76b4ad9ba4274a566834610b2d8a`) · T `20261124T224357Z` · tip `5fc8e0bcefe06cd711cb11b1d76dd17a6f2d364d` · 묶음 sha256 `fe588245b61707f1cccdbbbe3d868124c72e79c78a43d0d433bae94ff2e8c1ae` · PARKED_OK |
| 11-25 08:5x | kgy | 넘김 ⑩ 받기 → recover 11 → `P0_c1_R_j_lo` 시도 14 등록 · 시작 | 묶음 sha256 같음 (`fe588245…`) · RECV_OK · recover 11 rc 0 (결과 줄 completed · post · 원인 None · 재실행 자격 False) · ATTEMPT_ADDED n=14 (항목 커밋 `70d63f0c066baac97543b8dcd7bc07730c379a31`) · START_OK 14 (원장 = kgy) |

채택 단위 6/12 (시도 3 · 4 · 5 · 6 · 8 · 10) → 시도 11 (kgy recover) · 12 (gabia 원장이 스스로 기록) 이 들어가면 8/12.  남음 = kgy `P0_c1_R_j_lo` · `P0_c1_R_j_hi` · `P1_c0_R_j0` · gabia `P1_c1_R_j_hi`.  다음 = 넘김 ⑩ (gabia → kgy · gabia 가 `P1_c1_R_j_hi` 시작 확인 뒤) → kgy recover 11 → `P0_c1_R_j_lo`.  넘김 ⑩ 끝 (위 표 끝 두 줄) → 채택 8/12 · 진행 = gabia 시도 13 `P1_c1_R_j_hi` · kgy 시도 14 `P0_c1_R_j_lo` · 남음 = kgy `P0_c1_R_j_hi` · `P1_c0_R_j0` (+ gabia 부록 팔).

## 11-25 밤 – 11-26 아침 (서브 세션 · Claude 기록 · 1저자 현장 실행)

σ 값은 이 표에 없다 (판독 = `verdict_results.json` 에만).  주소 · 계정 · 홈 경로는 적지 않는다.

| 시각 (KST) | 기계 | 일 | 결과 |
|---|---|---|---|
| 11-25 19:55 | kgy | 시도 14 `P0_c1_R_j_lo` 끝 (본 세션 인계 · 화면) | 그룹 3/3 · 팔 JSON 12 · 사슬 0 · 원장 kgy 에서 스스로 결과 줄 (`result 14`) |
| 11-25 20:0x | kgy | `P0_c1_R_j_hi` 시도 15 등록 · 시작 (본 세션) | ATTEMPT_ADDED n=15 (항목 커밋 `5a32b2412a9b1a3b1212452857db3b0e1b35a236`) · START_OK 15 (원장 = kgy) |
| 11-25 21:34 | kgy → gabia | 넘김 ⑪ (서브 세션 블록 · 원장 끝 `start 15` 와 시도 15 그룹을 확인한 뒤에만) | T `20261125T123420Z` · tip `a82212d8dbc69f723051d7102699aff98a9e5e94` · 묶음 sha256 `33c98e6dda53b7c4ba28211528dec7e895a78ed15cfabff1f13e43452a1a9043` · PARKED_OK |
| 11-25 21:5x | gabia | 넘김 ⑪ 받기 2 회차 | bash 문법 오류 — 아무것도 실행 안 됨 (원장 · 묶음 무영향) · 원인 = 다시 보낸 블록을 1저자 화면 글에서 옮겨 만들다 바깥 `fi` 한 줄이 빠졌다 (`SELF-201`) |
| 11-25 21:5x | gabia | 넘김 ⑪ 받기 3 회차 (원래 보낸 블록 그대로 · `bash -n` 통과) | 묶음 sha256 같음 (`33c98e6d…`) · RECV_OK · 원장 = gabia (세워 둔 사본 없음) · 시도 13 `P1_c1_R_j_hi` 진행 (22:02 = 그룹 2 시작) |
| 11-25 22:0x | gabia | 부록 팔 준비 블록 A (읽기 · 준비 · 결과 0 건 · GPU 안 씀) | 압밀 코드 작업 트리 = `298a73197` (`mpm3d_compaction.py` sha256 앞 16 `b8bb85278b09e423` = kgy 10-23 재압밀과 같음) · 실행기 작업 트리 = `49f60159a` (사슬 sha256 앞 16 `5fbc1c3417f17eba` = 봉인) · 킷 ② `kit_DBE_ptfe05_sdcp0_vgcf100` = DBE 입력 일곱 파일 복사 + 압밀 줄 두 곳 (`--sdcp-agg-d 1.0` 뺌 · 조성 `VGCF:PTFE=3:0.5`) · `run_mpm.sh` 45 줄의 RUN_DIR 표지 글자는 옛 `SDCP0.5` 그대로 (기록만 · 표지 글자) · 부록 팔 계획 rc 0 · 저장본 = 본 사슬과 따로 (1저자 11-25 밤 Q5) |
| 11-25 22:05 | gabia | 블록 B — 압밀 대기 | 시도 13 결과 줄을 본 뒤에만 ② 압밀 (gabia 의 본 사슬 단위가 끝난 뒤 · 남은 본 사슬 단위는 kgy 몫) · 대기 스크립트 sha256 앞 16 `c8f684e0e557fddc` |
| 11-25 22:0x | — | 1저자 *"권고대로 해요"* = 부록 팔 칸 발사 GO | ② 압밀 끝 → ① P0 → ① P1 자동 · ② 칸 = 침대 점검 (`docs/reviews/rint2_middle_arm_ptfe05_sdcp0_registration_20261124.md` §3) 을 통과해 표지 파일을 만든 뒤에만 · 칸 사이 멈춤 파일 |
| 11-25 22:12 | gabia | 블록 C — 칸 차례 실행기 | ① P0 → ① P1 → [② 침대 점검 표지] → ② P0 → ② P1 · 칸 스크립트 sha256 앞 16 `6ccb93d31b6149ca` · 두 스크립트 지문 · `SYNTAX_OK` = 1저자 화면 대조 |
| 11-26 06:1x | kgy · gabia | 화면 (watch) | kgy 시도 15 = 그룹 3 시작 · 팔 JSON 8/12 · gabia 시도 13 = 그룹 3 · 팔 JSON 11/12 (끝 아님) |

남음 = gabia 시도 13 끝 → 넘김 ⑫ (gabia → kgy · 원장 끝 `result 13 completed` · gabia 에 사슬 없음을 확인한 뒤에만) → kgy 시도 15 끝 → 마지막 단위 `P1_c0_R_j0` (kgy) · 부록 팔 = 압밀 → ① 칸 둘 → ② 침대 점검 → ② 칸 둘 (σ 판독은 등록대로).

## 11-26 (서브 세션 · Claude 기록 · 1저자 현장 실행)

| 시각 (KST) | 기계 | 일 | 결과 |
|---|---|---|---|
| 11-26 07:28 | gabia | 시도 13 결과 줄을 본 뒤 부록 팔 ② 압밀 발사 (블록 B) | `run_mpm.sh` rc 0 · 분리 실행 |
| 11-26 07:48 | gabia | ② 압밀 끝 → 부록 팔 arm 1 P0 칸 시작 (블록 C) | 완료 표지 있음 · ② 압밀 런 폴더 이름의 `SDCP0.5` = 옛 표지 글자 (기록만) · ② 침대 점검 = arm 2 칸 전에 따로 (읽기만 · σ 안 읽음) |
| 11-26 09:03 | gabia → kgy | 넘김 ⑫ (원장 끝 `result 13 completed` · gabia 에 본 사슬 없음 확인 뒤) | T `20261126T000305Z` · tip `ab534f701b7df18849d9673c7f7fc76efc46ce4d` · 묶음 sha256 `403894d25084bfff0d7c9c9897b83412d3ffaeef8bc7b4813a10b6a70faf1776` · PARKED_OK |
| 11-26 09 시대 | kgy | 넘김 ⑫ 받기 (블록이 venv 를 스스로 켬) | 묶음 sha256 같음 · RECV_OK · 원장 = kgy · 시도 15 진행 중 → 끝에 스스로 결과 줄 |
| 11-26 09:45 | kgy | 시도 15 `P0_c1_R_j_hi` 끝 | 그룹 3/3 · 팔 JSON 12 · 사슬 0 · GPU 59 % · 3.3 GB = 본 사슬 밖 프로세스 (미확인 · 11-25 에도 보임) |

**1저자 중간 열람 (11-26 오전 · 판정 아님).**  1저자가 등록 R 밖에서 끝난 단위 열 개 (시도 3 · 4 · 5 · 6 · 8 · 10 · 11 · 12 · 13 · 14) 의 런별 σ_e 를 열람했다 (11-23 과 같은 읽기 전용 스크립트 · 합치기 · 넘침 · 재검산 전 값).  값은 이 기록 · 리포 어디에도 적지 않는다.  등록 R · 봉인 · 단위 순서 · 판정 규칙은 바꾼 것이 없다.  판정 문장의 한정어 = *"1저자 중간 열람 (11-23 · 11-26 · 판정 전 값)"*.

남음 = 마지막 단위 `P1_c0_R_j0` (kgy · 원장 끝 `result 15 completed` 확인 뒤 등록 · 시작 블록) · 부록 팔 = arm 1 P0 → arm 1 P1 → [② 침대 점검 → 표지] → arm 2 P0 → arm 2 P1.
