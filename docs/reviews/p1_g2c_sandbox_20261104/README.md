# P1 언로딩 G2c — 샌드박스 작은 침대 (2026-11-04 · Ⓐ ① · 등록 = 노트 §6 · §6-1)

- 등록 · 예측 = `docs/reviews/p1_g2c_source_check_20261104.md` §6 · §6-1 (결과 0 건 · 이 폴더 = 실행 전 묶음).
- 실행: `LMP=<LIGGGHTS 3d5c00f 직렬 실행 파일> bash run_arms.sh 40000 <빈 출력 폴더>` → `python3 -I compare.py <출력 폴더> 40000`.
- 팔 = A (끊김 없는 원 런) · A2 (step N 에서 run 끝 + `write_restart` 명령) · B (A 의 주기 restart 재개) · B2 (A2 의 주기 restart 재개) · C (A2 의 명령 파일 재개).
- `dry/` = 건식 (N = 200 · 접촉 0 개 = 대조 정보 없음) — 다섯 팔 rc 0 · 대조기 rc 0 · 세 restart 파일 md5 같음 · 입력 md5.
- 하지 않는 것: ibb · RJ 323957 재실행 · G2c 허용폭 · 판정 규칙 변경.
