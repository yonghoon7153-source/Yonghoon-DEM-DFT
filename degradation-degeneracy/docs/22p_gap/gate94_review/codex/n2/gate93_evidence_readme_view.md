# gate93_evidence — 92차 단계 4 (묶음 6) 구현 결과의 원 로그 (2026-10-06)

| 파일 | 무엇 | HEAD |
|---|---|---|
| `00_red_…` | RED — `tests/test_gate92_stage4_linkage.py` 138 node · 41 failed · 97 passed (예외로 떨어진 5 는 AttributeError 4 · WireError 1) | `7e5bdd9e9` 직전 작업 트리 (시험 파일 = 그 커밋) |
| `03_…` | `mutation_replay.py -k g92 --emit-expect` — 9 변이 관측 (EXPECT 없음 표시는 선언 전이라서) | `5768b7f8f` 직전 |
| `04a_…` | EXPECT 붙인 뒤 `-k g92` — 8 / 9 물었다 · k07 증인에 실행마다 다른 digest (G67-T1-b 위반) | 같음 |
| `04b_…` | k07 시험 메시지에서 digest 제거 뒤 그 변이만 — 물었다 · rc 0 | `5768b7f8f` |
| `05a_` · `05b_` | §16-5 `-k` 확장 둘 (사용자 승인 "다 승인") `--emit-expect` — 13 / 2 node 사망 · 증인 `DID NOT RAISE PreserveError` (불변). EXPECT 반영 뒤 각각 물었다 (원장 §146) | `7ae871687` 직전 |
| `06_…` | `make_receipt.py` 두 leg 1 회 (rc 0 · 35 / 34) | `683503225` (clean) |
| `08_…` | `python -m tools.env_profile --json` — **MISMATCH 34** (기록 전용 · 이 컨테이너 이미지가 91차와 다름) · rc 0 | `3ec8aadb1` |
| `10_…` | 전체 `pytest tests/ -q -rfEx` — **2320 passed · 1 xfailed · rc 0** (1:18:04) · 시작 = 끝 HEAD · dirty 0 | `3ec8aadb1` |
| `11_…` | `./scripts/smoke_e2e.sh` — **rc 0** · dirty 0 | `3ec8aadb1` |
| `12_…` | 등록부 전체 재생 (`-k` 없음) — **421 / 421 call 단계에서 물었다 · rc 0** · scenario 432 (executable 421 · declared 11) · site 470 · 15:13:26Z → 18:42:28Z | `3ec8aadb1` |
| `aborted/run1_…` | 1 차 전체 회귀 — 15 % 지점 docs-lint F 4 (원장 앵커 3 · 계약 줄 인용 1) 에서 중단 | `7fea9cdb7` |
| `aborted/run2_…` | 2 차 전체 회귀 — 같은 자리 F 1 (계약 줄 인용 둘째 줄) 에서 중단 | `7ae871687` |

파일로 남기지 않은 실행 (출력은 커밋 메시지 · 원장에만): GREEN 직후 새 파일 138 passed · G81/G82/G84/G85/G87/G88/G89 179 passed (`d7a97aa57` 메시지) ·
영수증 identity 시험 (gate70/71/72/74 defensive) 113 passed · `make_receipt.py --check` 두 leg core 바이트 동일 (원장 §146).
