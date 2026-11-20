# Rint ② R 시작 기록 — kgy P0 시도 1 · gabia P1 시도 2 (20261118)

- 1저자 11-18 Q1 = R GO (S0 단계 2 뒤 · `docs/data/rint2_s0_dbe_20261118/`) · 흐름 = 봉인 커밋 `29643188524f` 판 `docs/reviews/rint2_kgy_commands_20261020.md` §3-1b (3)(4)(5) (stoic 판에는 이 절이 없다 · 봉인 가지 `claude/rint2-seal-20261118`) · 실행 트리 = 봉인 커밋 `29643188524f` (두 기계).
- 화면 = 1저자가 붙여 준 출력을 가린 사본 (`kgy_R_start_screen.txt` · `gabia_R_start_screen.txt` · 홈 → `<HOME>` · 주소 · 셸 머리 줄 · scp · 비밀번호 줄 뺌).  스크립트 = 실행한 판 그대로 (`scripts/` · md5 = 붙여넣기 게이트 값).

| 단계 | kgy (14:0x KST) | gabia (14:1x KST) |
|---|---|---|
| 0. 확인 (읽기만) | 실행 트리 29643188524f · 세 해시 기대대로 (R 계획 `d8595a52…` · 새 DBE S0 보고 `e6989481…` · S0 단계 1 보고 `c9307cfc…`) · RTX 3090 · 드라이버 560.35.03 · 시작 전 사용 3,610 MiB (다른 프로세스 · [미확인]) | 같음 · RTX A6000 · 595.58.03 · 시작 전 사용 35,162 MiB (QE pw.x · 다른 일 · 누구 일인지 [미확인] · 1저자 = 그대로 두고 첫 팔 시간으로 판단) |
| 원장 | (3) `LEDGER_INIT` · 커밋 `15352f8e7f91a44aa0fa649ee8a03197804bd81f` · 가지 master | (5) `RECV_OK` (묶음 sha256 · 끝 커밋 대조) |
| dry-run | 사다리 P0 첫 다섯 env (RJ inf · 0 · 1e4 · 1e6 · 1e8 · s_min 0.0 · tol_ff 0.07381254285530132 · face_alpha · maxiter 5,000,000 · rtol 1e-12 · σ 표시 없음) | 사다리 P1 같은 꼴 (`CJUNC_PTFE_JLAW=P1`) |
| 시도 | `ATTEMPT_ADDED n=1 target=ladder:P0 machine=kgy commit=9234384f1a6256d1e2ba73d6f213fd8b7887f4bd` → `START_OK 시도 1` | `ATTEMPT_ADDED n=2 target=ladder:P1 machine=gabia commit=db71fe19685d072f5a7216d1b51706964489f10d` → `START_OK 시도 2` |
| 원장 넘김 | `PARKED_OK` · 기록 `20261118T050239Z` kgy → gabia · 가지 master · 끝 커밋 `bcff6b0235a39ec799ef18f733b1599bfdb50463` · 묶음 sha256 `fa63d348cd7065f86d695b1bae9a6d99bbe46536ba60c9471782190c84eb7d63` · flock | 원장 = gabia 에 둔다 (먼저 끝난 기계가 받는다 · §3-1b (6)) |

- 감시 = `scripts/rwatch.sh` (읽기만 · 파일 수 · 프로세스 · GPU · σ 를 열지 않는다) · 시간 = `scripts/rtimes.sh` (L 폴더 첫 파일 → `p2_*.json` 초).
- 1저자 11-18 규칙 (권고대로): gabia 첫 팔 (L01 · 접합 저장본을 짓는 런 · ⚠ 11-18 판의 'L03 · 첫 정상 점' = 내 오기 · `SELF-185`) 이 3 판 어림 T_first 10,817 s 의 1.5 배 (16,226 s) 를 넘으면 QE 를 사다리 끝까지 멈추거나 단위 배정을 kgy 쪽으로 옮긴다 (배정 = 봉인 밖) · 참고 = kgy 의 같은 1.5 배 값 13,600 s (T_first 9,067 s · 규칙은 gabia QE 판단용).
- 다음 = 먼저 끝난 사다리 → 원장 받기 + recover (§3-1b (6) 5–6) → 채택 사다리 폴더 서로 옮김 → 단위 (첫 배정 kgy 7 · gabia 5) → 합치기 · 넘침 점 (112 h 규칙) · 판정.  원장 없이 끝난 사슬의 rc 3 = 정상 (§3-1b (6)).
- 이 폴더 바이트 = `SHA256SUMS`.

## 그 뒤 (11-19 · 11-20 · 기록 = 런 이름 · 시각 · 원장 동작만 · σ 미열람)

- 1저자 규칙 판단 (11-18 20 시): gabia 첫 팔 L01_floor 12,342 s < 문턱 16,226 s (3 판 T_first 10,817 s 의 1.14 배) → QE · 단위 배정 그대로.  kgy L01 7,936 s (모형 9,067 s 의 0.88 배).
- kgy P0 사다리 (`rtimes.sh` 초 = 런 폴더 첫 파일 → 가장 이른 p2 JSON · 팔 여럿 런은 첫 팔 끝 = `SELF-186`): L01 floor 7,936 · L02 ceiling 2,871 · L03–L07 point 2,998 · 3,496 · 4,215 · 3,103 · 3,342 · L08 confirm 3,476 · L09 end_confirm 3,371 · L10 end_origin (팔 1 · 2) 7,453 · L11 end_confirm 3,487 · L12 · L13 end_origin 3,470 · 4,102 · L14 origin (팔 1 · 2) 3,456 · L15 origin8 (첫 팔 3,482) · L16 no-op · 끝 11-20 10:36 KST (요약 있음 · 끝난 팔 JSON 54 = 팔마다 둘).
- 사슬 갈래 (봉인 `rint_r_chain.py` 의 end_pick · end_origin_push · origin 순서로 읽음): lo 끝 (T⁺ = 1.63 × 1.02) = 한 번에 통과 · hi 끝 (T⁻ = 1.63 × 0.98) = 세 origin 중 하나가 띠 안 → 바깥 점으로 한 번 밂 (L12 → L13) · origin (§3-3) = 문턱 0.02 넘음 → origin8 (8 팔 평균) + `CALIB_ORIGIN_SENSITIVE` (R_j,0 그대로 · PASS 문장 금지 · 등급 불변).  origin 팔 런은 점 수 상한 (16) 에 안 센다 (kgy 점 = 10).
- kgy 사슬 끝 = rc 3 정상 끝 (끝 줄 `멈춤 [ATTEMPT_LEDGER_MISMATCH] … 원장 잠금 파일을 못 연다` · 그때 `ca1_ledger` 없음 · 요약 있음).
- 원장 넘김 ② (§3-1b (5)): `20261120T022342Z` · gabia → kgy · 원장 끝 커밋 `7b43cc81df6d68e2c0094f4e6afd98243f265173` · 묶음 sha256 `6bb6318bd83388bdccf417fad02e032c50a057589c8b7ac5975fc65a121a87dd` · flock · kgy `RECV_OK` (sha · 끝 커밋 대조 · 같은 부팅) → kgy `--stage recover` rc 0 (attempt_1 결과 줄 completed · 원인 없음 · 재실행 자격 없음).
- gabia P1 = 진행 (원장 없이 · 끝나면 rc 3 정상 → 원장을 gabia 로 → recover → 채택 사다리 폴더 서로 옮김 → 단위).  gabia QE 는 11-20 오전에 멈춤 (GPU 0 % · 1 MiB · 1저자 "알아서 멈출거야").
