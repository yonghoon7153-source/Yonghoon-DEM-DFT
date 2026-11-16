# 시도4 DONE 뒤 대기열 — 지금은 수정 안 함

| 순서 | 대상 | 예정 변경 | 선행·현재 상태 |
|---|---|---|---|
| 1 | 수영 전용 로컬 출력·새 시험 | 현재 로컬 바이트 검토→코드 커밋·push→고정 실행 핀·소스 tar 결속→WSL CPU1 블록 | 1저자 시도4 DONE 통보 필요. 현재 코드 커밋0 |
| 2 | `scripts/viz_mpm_morphology.py:147` 및 `scripts/mpm2d_morphology.py` | `total strain ε (vs seed)`를 **누적 변형량 ∫‖D‖dt**, Σdg를 **누적 소성 보정량**으로 표기 | 문구 의미/현재 줄은 작업 시작 시 실제 최신 파일에서 확인. 지금 무변경 |
| 3 | `scripts/mpm3d_compaction.py:2250` | `(0 ⇒ pristine/no memory)` 정정: F는 탄성 상태, 영구 형상은 x, 이력은 Σdg | FAM 봉인·공유 파일. 동결 해제만으로 봉인 교체 권한으로 읽지 않음; Claude와 고정 변경 범위를 맞춘 뒤 |
| 4 | 같은 파일 `:3261` | 공극률 `max(0,…)` 잘림 때 표지와 음수 원값 기록 | 출력 계약·봉인 영향 확인 후 별도 변경. 지금 구현0 |
| 5 | 그림 패널 `AM 0 %` | 물질점 구성비이며 scaffold AM 장애물은 별도라고 표기 | 해당 생성 경로 확인 뒤. 지금 그림/값 수정0 |

위2–5 근거는 Claude의 `docs/mpm_basics_20261116.md` **[반입 예정·현재 이 가지에서 미확인]**와 1저자11-16 지시다. 파일 내용을 이번에 검증했다고 쓰지 않는다. 줄 번호는 지시 시점 기준으로, 실제 수정 전 최신 바이트에 다시 대응한다.

Claude 전용 네 경로는 참조만: `docs/reviews/dem_redesign_direction_20261109/seminar_feedback_20261113.md`, `docs/mpm_basics_20261116.md`, `webapp/static/explain/mpm_basics_20261116.html`, `CLAUDE.md`. 이 창에서 생성/수정하지 않는다.

G2c′ 최초 내용 판정은 NP2=366288·NP4=366290 고정. 시도4 DONE은 같은N40000을 다시 돌릴 허가가 아니다. 50kg Love–Weber 재작도·후막 작업은 대기열에 넣지 않는다.
