# Rint ② R 운영 복귀 · 2026-11-22

| 트랙 | 마지막 확인 | 복귀 첫 동작 |
|---|---|---|
| Rint 사다리·단위 | 사다리 P0·P1 복사 확인. 시도 3·4 completed, 단위 2/12. 16:33 KST 화면에서 시도 5·6 PENDING | 기존 작업의 두 status 및 원장 STATUS |
| 1저자 운영 원장 | 넘김 ⑥ gabia→kgy, 시도 4 recover, 시도 6 START_OK. 마지막 확인 활성 kgy, HEAD `de3913418e4618721ff8d96a65a9cacada32d4e8` | 새 status 결과와 대조 |

복귀 주체는 Claude다. 가지 `codex/rint2-r-1121`의 직전 기록 `0c1474fcbc0f` 뒤에 1저자 화면 및 넘김 ⑥·recover_4 영수증을 정리했다. 변경은 `docs/data/rint2_r_ops_20261121/README.md`와 이 쪽지 두 파일이다. 봉인 핀과 제출기는 종전 그대로이며 검산은 기록의 SHA 및 Git 객체 대조다.

1저자 WSL에서 기존 운영 폴더로 이동한 뒤 아래 세 조회를 사용한다.

```bash
bash units/PASTE_RINT_UNITS.txt status gabia P1_c0_R_j_hi 5
bash units/PASTE_RINT_UNITS.txt status kgy P0_c0_R_j_lo 6
bash ledger/PASTE_RINT_LEDGER.txt STATUS
```

기존 발사·복구를 반복하는 대신 이 조회의 원장 보유자, 실제 tip, 정상 parked 종료 표지로 다음 단계를 결정한다. `docs/collab/claude_to_codex/20261121-1600_rint2-to-codex-practice.md`, 봉인 가지 `29643188524f`의 `docs/reviews/rint2_kgy_commands_20261020.md` §3-1b (4)–(7)이 근거다. 운영 실행 권한은 1저자, 판정값의 위치는 verdict_results.json이다. 이번 인계의 현장 실행·판정값 열람은 0회다.

공유 기록 제안 — Rint R 운영을 Claude에 복귀. 시도 3·4 completed, 2/12. 시도 5·6은 새 status 대기, 마지막 확인 활성 원장은 kgy.

1저자 GO 요청: 없음. 첫 요청은 읽기 전용 상태 조회다.
