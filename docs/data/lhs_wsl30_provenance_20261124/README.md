# LHS WSL30 출처 확인 도구 (11-24 · 값 안 보는 읽기 전용)

1저자 WSL 에서 `lhs00_100`–`lhs00_129` 를 값 출력 없이 확인한 두 스크립트다.  결과 원문 두 개 = `docs/reviews/lhs_wsl30_source_freeze_20261124/evidence/` (반입 ㉞ · Codex 가 받은 바이트).

| 스크립트 | sha256 앞 16 | 보는 것 |
|---|---|---|
| `check_wsl30.py` | sha256 `04f1c4bdd49396b3` | 배너 · `Finished!` 수 · 두 로그의 압력 줄 목록 같음 (해시) · log.txt 줄이 log.liggghts 안에 순서대로 · 덱 (+ include) 줄 되풀이 · 덱 · atom 지문 = `docs/data/area_s2_cohort.tsv` · 코호트 하베스트 step 이 두 로그의 step 범위 안 |
| `check_wsl30_b.py` | sha256 `0ff5b548a645e281` | 위에서 남은 줄의 줄 번호 + 첫 낱말 종류만 · 30 케이스 패턴 대조 |

결과 (30/30 같은 꼴): 배너 1/1 · `Finished!` 1 · 압력 줄 목록 같음 · log.txt 줄 99.9 % 가 log.liggghts 안에 순서대로 · 덱 · atom 지문 = 코호트 · 코호트 step 이 **정수로 시작하는 줄** 에 정확히 있음.  첫 도구의 CHECK 30 = 내 엄격 기준 (남는 줄 0 요구) 때문 — 남는 줄 = 이어 쓰기 `&` 조각 28 (자리 30/30 같음) · 화면 전용 LIGGGHTS 안내 20–22 · 로그 전용 빈 줄 20.

한정: 이어 붙인 `&` 줄의 바이트 대조는 하지 않았다 · step 이 든 줄이 thermo 행인지 (머리글) 는 도구가 보지 않았다 (Claude 의 'thermo 에 있음' 은 넘친 서술 = `SELF-196`) · 화면 전용 줄이 경고라는 것은 첫 낱말 분류에서 나온 Claude 의 해석이다 · LIGGGHTS 실행 파일 신원 · 목표 압력 도달은 보지 않았다 (값 = §5 몫).
