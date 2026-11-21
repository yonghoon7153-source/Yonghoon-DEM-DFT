| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| 수영 U6(c) | F8 반걸음 | 개발 반환 판독 완료 | 지정 변위의 원 차이 +0.565977 MPa 중 시간 간격 대조 +0.029966 MPa, 같은 간격에서 +0.536012 MPa 잔여. | U6(c) 자격과 단계 3 보류. |
| 수영 U6(c) | F8 격자·F16 물질점·F16 시간 간격 | WSL 블록 준비, 1저자 실행 대기 | 새 한 팔, 물질점 39,053개, CPU 1. 새 개발 계산 0건. | 같은 변위에서 초기 표본을 맞춘 효과와 그 뒤의 격자 차이를 나눈다. |

가지 `codex/suyoung-u6c-dt-return-1122`, 바탕 `e200eb9e2204`(직전 수영 벽 관측 반환 인계 끝). 반입은 1저자 결정 뒤 cherry-pick -x 순서로 한다.

1. `b33b7f00a` — 개발 반환 요약·CSV 독립 검산·다음 팔 대조 기준. `docs/reviews/suyoung_u6c_dt_return_20261122/README.md`, 같은 폴더의 dt_summary.json, independent.json, check_dt_return.py. 반환 TAR·화면 2/2, 원 판독기로 다시 만든 JSON 바이트 일치. 변위 5,157점에서 차이의 합을 검산했다. F8 반걸음 5,191걸음, 198.48초.
2. `387858bb316d` — 새 팔 소스 핀. README의 1저자 운영 절 및 같은 폴더의 seed_control.py, test_seed_control.py, run_wsl.in, test_operator.py. 원 계산기 3파일 및 앞 팔의 판독기 보존. 합성 9/9, WSL 모의 운영 7/7. 실제 초기화 인수만 관찰해 시간 전진 0걸음에서 F8 전역격자 80·F16 시간 간격·초기 좌표/ID/부피 해시 3/3 일치를 확인했다. 최종 TXT의 실제 WSL CHECK_ONLY 통과.
3. 이 쪽지. 인계 ZIP의 HANDOFF.md에 전체 SHA와 patch-id, 전체 변경 경로가 있다. 실측 원 TAR는 1저자가 보존한다.

공유 기록 제안 — 수영 설정 ① 개발 대조에서 F8 시간 간격을 절반으로 줄인 뒤에도 고정 변위에서 F16과 0.536012 MPa 차이가 남았다. F16 피크로 나누면 84.43%. 다음은 시간 간격을 유지한 F8에 F16 원 물질점을 사용해 표본과 격자 민감도를 순서대로 대조한다.

1저자 GO 요청 — WSL에서 `GO_SUYOUNG_F8_DENSE_SEED_ONCE` 한 번, 입력은 직전 벽 관측 TAR와 F8 반걸음 TAR. TXT SHA256 `293fb355dd8723f13cd3c3e4de395816ee78af07f80d85f90b8b2aea01a5129e`.
