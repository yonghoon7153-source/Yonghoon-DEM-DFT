# 사전 공격 리뷰 4 회차 — Q9 설계 개정 3 + 10-24 결정 (Rint ② RR · 2026-10-24)

- 보고 = `PREATTACK_Q9R3.md` (독립 에이전트 하나 · 고친 쪽 설명 없이 · 문서만) · 탐침 = `probes/` · 에이전트 출력 = `logs/` · 메인 재현 = `logs/_repro_main/`.
- 대상 = `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` 개정 3 + 10-24 결정 표지 (`4040e4388`) · 비교 기준 개정 2 (`9a72d65c6`).
- 결론 = P1 0 · P2 4 (R4-01 – R4-04) · P3 9 (R4-05 – R4-13) · 질문 5 (D1 – D5) · 3 회차 발견 26 = 닫힘 22 · 부분 4 · 열림 0.
- 메인 재현 (10-24) = 같은 다섯 탐침을 `git archive 4040e4388` 사본에서 다시 돌림 → 판정값 같음 (차이 = 임시 경로 · 탐침이 만든 git 커밋 해시뿐).
  - 코드 줄 대조 (메인): 사슬이 러너를 `subprocess.run(['bash', runner], timeout=…)` 로만 부르고 프로세스 그룹을 죽이지 않는다 (`scripts/rint_r_chain.py` 1531–1535) · 러너는 payload 를 킷 런 폴더 (`$RUN`) 에서 만들고 검사 통과 뒤에만 옮긴다 (`scripts/sdcp_gain_vox015_8arm.sh` 855–880) · `code_key` 에 `runner_path` (`scripts/rint_r_chain.py` 1104 · 1115) · 예측의 첫 두 런 = SBE no-op (`scripts/rint_r_chain.py` 1830–1838).
  - ⚠ `orphan_kill_probe` 는 러너 구조를 흉내 낸 것 (GPU · 실제 payload 없음) — 실제 러너에서 고아가 payload 를 끝까지 쓰는지는 실측 전 (구조상 가능 · 추정).
- 처분 = ⬜ 1저자 (D1 – D5 · 개정 4 여부) — 1저자 결정 전에는 설계를 고치지 않는다.
- 다시 돌리기: 이 폴더에서 `mkdir -p tree work && git -C <리포> archive 4040e4388 scripts docs/reviews/rint2_rr_fix_evidence_20261023 | tar -x -C tree` →
  `OPENBLAS_NUM_THREADS=1 nice -n 19 python3 -I -B probes/partial_adoption_r3_probe.py tree/scripts probes` (나머지 = 보고 §E).
