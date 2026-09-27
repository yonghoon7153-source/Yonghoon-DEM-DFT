# 재개-위상 영수증 — 1차 실측 (v0 · Codex 3차 수정 전 도구 산출)

⛔ **판정 경로에 쓰지 않는다.**  Codex 3차 리뷰 (`docs/reviews/codex_mixer_highbo_rereview2_verdict_20260927.md`, HOLD) 가 이 도구의 생산자 · 소비자를
fail-closed 가 아니라고 판정했다 (HBR3-01 · 02).  이 파일은 **측정 기록**으로만 둔다 — 수정된 생산자로 실행 시 봉인까지 붙여 다시 만든다 (초 단위).
`check_contact_validity.py --phase-receipt` 에 이 파일을 넣지 말 것 (지금의 소비자는 받아들인다 — 그것이 HBR3-02 다).

## 출처

- 실행: 사용자 WSL (`yonghoon71@DESKTOP-IK8J81H`) · 2026-09-28 00:0x KST (파일의 `date` 가 09-28 인 이유 — 명령에 쓴 이름은 `…_20260927.json` 이었다).
- 도구: `scripts/mixer_restart_phase_test.py` — `db589abf7` 판에 로컬로 `DROP_FIX = ('insert/',)` 한 줄만 바꾼 것 = `04fe95ae8` 과 **기능상 같다** (`analyze` 코드는 두 판이 같다).
  첫 시도 (템플릿 · 분포까지 뺀 덱) 는 A 가 `run 20000` 을 마친 뒤 `write_restart` 에서 `ERROR: Atom types must start from 1 for granular simulations (../properties.cpp:120)` 로 죽었다 → `04fe95ae8`.
- 명령 (WSL, 리포 `~/dem-web`, venv python):
  ```
  PY=~/Yonghoon-DEM-DFT/venv/bin/python3; R=dem_scripts/mixer_20260921/runs
  $PY scripts/mixer_restart_phase_test.py gen --deck $R/LC_s32452843/in.mixer --out ~/phase_test_20260927b
  bash ~/phase_test_20260927b/run.sh
  $PY scripts/mixer_restart_phase_test.py analyze ~/phase_test_20260927b --binary "$(command -v lmp_serial)" --out docs/data/mixer_phase_receipt_20260927.json
  ```
- 파일 `receipt_v0_pre_hbr3.json`: 사용자가 붙여 넣은 JSON 을 도구와 같은 `json.dump(…, ensure_ascii=False, indent=1)` 로 다시 쓴 것 (1,851 B · sha256 `8308decf64747949…`).
  ⬜ WSL 원본과의 바이트 대조 = 사용자 쪽 `sha256sum` (같으면 이 줄을 ✅ 로).

## 값

| step | 관측 각 (°) | 예정각 (연속) | 예정각 (재개 때 0 으로 리셋) | 오차 (°) | A↔B 꼭짓점 차 (m) |
|---:|---:|---:|---:|---:|---:|
| 20000 | 6.352988 | 6.352978 | 0.000000 | 9.9 × 10⁻⁶ | 0 |
| 25000 | 7.941243 | 7.941223 | 1.588245 | 2.0 × 10⁻⁵ | 0 |
| 30000 | 9.529474 | 9.529467 | 3.176489 | 6.5 × 10⁻⁶ | 0 |

- 주기 0.799562 s · 축 x · dt 7.055 × 10⁻⁷ s · N1 20000 · N2 10000 · 덤프 5000 마다.  예정각 = 360° · step · dt / 주기 (세 점 모두 소수 9 자리까지 재계산 일치).
- 읽는 법: B (`read_restart` 로 20000 에서 이음) 의 드럼 각이 **연속 가설** 과 10⁻⁵° 로 맞고 **리셋 가설** 과는 6.35° 떨어진다 · A (같은 프로세스로 쭉) 와 B 의 꼭짓점이 세 step 모두 **완전히 같다**.
- ⚠ 이 시험의 표본은 재개 뒤 10,000 step 이다.  수백만 step 캠페인에서의 각 오차 상한이 아니다 (Codex 3차 HBR3-02 ⑤).
- ⚠ 이 실측은 HBR3-01 이 보인 거짓 통과 모양 (A 대조 없음 · 재개 전 표본뿐) 이 **아니다** — A 3/3 존재 · 재개 뒤 step 2 개 · 차 0.  그래도 도구가 그 경우를 막지 못하므로 지위는 위 ⛔ 그대로다.

## 바이너리 · 덱 연결 (Codex 3차 HBR3-02 가 요구한 것의 일부 — 실행 시 봉인은 아니다)

- `lmp_serial` = `/home/yonghoon71/src/LIGGGHTS-PUBLIC/src/lmp_serial` · 8,299,592 B · 수정 시각 **2026-08-25 18:16:52 +0900** · sha256 `4efca042a1bbdafb…` (분석 시점에 잰 값).
- 배너 (A 의 `log.lmp`) = `LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-08-25-18:16:51 by yonghoon71, git commit 3d5c00f2…)`.
- **L 캠페인 `LC_s32452843/log.lmp` 첫 줄이 같은 배너다** (사용자 확인 09-28) ⇒ 09-21 발사 때의 빌드와 컴파일 시각 · LIGGGHTS 커밋이 같다.  바이너리 파일은 08-25 이후 다시 빌드되지 않았다 (수정 시각 = 컴파일 시각).
  ⚠ 그 런이 실행한 파일의 sha256 은 **기록된 적이 없다** — 배너 일치는 강한 정황이지 봉인이 아니다.
- 덱 `deck_source_sha256` `72b52c17…` (8,629 B) = 생성기 `b6d9a2036` (09-21 13:13) 이 `--n-total 100000 --cgf 151.4 --arm LC --seed 32452843 --revolutions 8` 로 내는 덱과 **바이트 동일** (09-28 재생성 대조).
  현재 생성기 (`6963632a0` 이후) 산출은 8,679 B · `94518e3a…` 로, 차이는 **LC 설명 주석 한 줄뿐**이다 (HB-01 의 라벨 정정 — 명령 차이 없음).
