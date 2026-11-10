# P1 언로딩 G2c′ — 샌드박스 준비물 (2026-11-10 · 결과 0 건 · 실행 없음)

- 등록 · 예측 = 메모 `docs/reviews/p1_g2c_compare_definition_20261105.md` §0 (11-10 개정 · 결과 전 · Codex Q6 답 `docs/reviews/codex_review_p1_g2c_q6_20261106.md` 반영 · **1저자 비준 전**) · §5-1.
- 11-04 파일 (`README.md` · 덱 조각 · `run_arms.sh` · `compare.py` · `run_40000/` · `dry/`) 은 그대로 — 이 묶음은 새 파일만 더한다.
- ⛔ 이 컨테이너 (11-10) 에 LIGGGHTS 실행 파일이 없다 → 건식 · 샌드박스 = 1저자 비준 (메모 §0-6 Q8 · Q10) 뒤.

| 파일 | 하는 일 |
|---|---|
| `BW.liggghts` | 팔 BW · CW 덱 = `include R.liggghts` + `write_restart ${RST}/restart_rt.bin` (R 덱 바이트 그대로 · 덤프는 `run 0` setup 에서 · 그 뒤 명령 restart) |
| `run_g2cp.sh` | 실행기 — A · A2 · B · B2 · C (11-04 와 같은 덱 · 인자) · BW · BR · CW · CR 차례 · 직렬 · `nice -n 19` · 시간 한도 |
| `compare_g2cp.py` | 대조기 — 메모 §0-3 예측마다 맞음 / 틀림 / 해당 없음 / 계산 못 함 + 등록 §3 판정 (허용폭 그대로 · 키트 `g2c_compare` 와 같은 식 · 30 열) |
| `test_g2cp.py` | 시험 — 합성 침대 (LIGGGHTS-PUBLIC 3d5c00f 줄을 옮긴 작은 모형) · 가짜 lmp · LIGGGHTS · MPI · 네트워크 없이 · 신호 시험은 `unshare -pf --mount-proc --kill-child` 안 |

## 돌리는 법 (비준 · 실행 파일 · 1저자 GO 뒤)

```
cd docs/reviews/p1_g2c_sandbox_20261104
LMP=<LIGGGHTS 3d5c00f 직렬 실행 파일> bash run_g2cp.sh 40000 <없거나 빈 출력 폴더>      # 팔 아홉 · 11-04 실측 A 20 s · A2 17 s · 재개 ≤ 1 s
python3 -I compare_g2cp.py <출력 폴더> 40000                                          # → <출력 폴더>/compare_g2cp.json + 화면 표 (rc 0 · 2)
python3 -I test_g2cp.py                                                              # 시험 (마지막 줄 G2CP_TEST … fail=0)
```

## 멈춤 (실행기)

| rc | 언제 | 남는 것 |
|---|---|---|
| 3 | 실행 전 — 인자 · N (200 이상 · 100 의 배수) · 도구 · `LMP` 없음 · 파일 아님 · 실행 권한 없음 · `-h` 첫 머리 줄 `LIGGGHTS (` 없음 · OUT 비지 않음 · 11-04 덱 일곱 md5 ≠ `run_40000/inputs.md5` · BW 꼴 · git 작업 트리면 이 폴더 커밋 안 된 변경 | 아무것도 (OUT 을 만들지 않는다 · 이유 = 화면) |
| 4 | 실행 중 — 팔 rc ≠ 0 (시간 한도 = 124) · ERROR 줄 · `Loop time of` 없음 · 기대 출력 없음 | OUT 에 그 팔까지 · `STOP.txt` · `rc.txt` (남은 팔 안 돎) |
| 0 | 팔 아홉 끝 | `lmp_identity.txt` · `inputs.md5` · `rc.txt` · 팔별 `log.txt` · `out.txt` · `post/` · `rst/` · `outputs.md5` |

- 끊기면 다시 돌리지 말고 보고 (새 빈 폴더 · 1저자 승인 뒤 · 이 묶음은 재개 도구가 아니다 — CLAUDE.md 멈춘 런 재개 체크리스트 ⑥).
- 시간 한도 = `G2CP_TLONG` (A · A2 · 기본 1800 s) · `G2CP_TSHORT` (나머지 · 기본 600 s) — 넘으면 `timeout` 이 TERM → 30 s 뒤 KILL.

## 하지 않는 것

ibb · RJ 323957 재실행 · 남은 네 침대 RJ · 허용폭 · 판정 규칙 · 키트 (`docs/data/ps45_unload_20261009/`) · 봉인 변경 · 자동 시작.
