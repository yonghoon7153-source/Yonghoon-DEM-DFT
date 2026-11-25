# 1층 g2 A/seed1 — 원자료 (kgy 회수)

출처: kgy `/home/kgy/work/runs/li2s_layer1_g2/A/seed1` · 회수 2026-09-14.
해시는 kgy 에서 받은 값과 **repo 에 넣은 뒤 대조**했다 (sha256 -c: OK).

| 파일 | sha256 | 상태 |
|---|---|---|
| plan.json | `7763ecdca79f43d6ec2ade2d453b61e2e3e68aa72268fe9fb2f6563356301952` | ⭕ 대조 통과 |
| result.json | `18161aa538011164ececf80932ad7de8a6ed085ba9fa0f765d1013d1f695d151` | ⭕ 대조 통과 |
| thermo.csv | `78a2def219878fca497980007b892dc39cb0babf694110cfd9bae60a5f260ad4` | ⏳ 회수 중 (전송 중 손상, 재전송 대기) |
| gr_partials.csv | `62b362c047ac6e606d032fe83d268ea85169490134849d57098addf665938f8d` | ⏳ 회수 중 |
| traj.xyz (66 MB) | — | repo 에 안 넣는다. G1 스냅샷·committee 입력이 그것이다 |

⛔ `plan.json` 에 `게이트_입력` 이 **없다**. 2026-09-12 실행이라 그 필드가 도구에 들어가기 전이다 —
`melt_quench_uma.py --gate_check` 가 이 런에서 "기록없음 · thermo 역추적" 으로 fail-closed 했고,
그게 이 필드를 만든 계기다. 다음 런부터는 앙상블 선언이 plan.json 에 들어간다.

해석은 `db/properties/lpscl_li2s_layer1_g2_seed1_2026_09_14.json`.

## 2026-09-14 회수 완료

네 파일 모두 sha256 대조 통과. `thermo.csv` 는 base64 전송이 두 번 깨져
(263/1051 행) **평문 3조각으로 다시 받아 재조립**했고, 재조립본이 kgy 원본과
비트 단위로 같다 (`78a2def2…`).

- `gate_check_kgy_2026_09_14.json` — kgy 에서 돌린 원본 (유지구간 블록추세 도입 **전**)
- `gate_check.json` — repo 에서 다시 돌린 것 (블록추세 포함)
