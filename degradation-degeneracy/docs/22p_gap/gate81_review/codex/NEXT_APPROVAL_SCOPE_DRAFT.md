# 사용자용 — 단계 3 한정 구현 승인 범위 초안

**현재 미승인. 검토용 초안이며 실제 실행 명령/승인 파일이 아니다.** 사용자가 아래 범위를 명시 승인할 때만 구현자가 착수한다.

---

GATE81 요청 및 수신 REVIEW_KO.md의 G81-N1~N3을 반영하는 단계 3 한정 오프라인 구현·검증을 승인하는 안이다.

1. 시작 전에 계획/실현 필드 시점 표, legacy/prep/v6 dispatch, provider edge·좌표 결속 표를 고정한다. planned roster/obs_key는 79차 합의대로다. 이번 수용 조건에서 벗어나는 선택이 필요하면 구현 전 질문한다.
2. src/fitting.py, src/io.py, tools/design_wire.py, tools/preserve.py 범위에서 3-A/B/C를 한 라운드로 구현한다. 새 production helper나 다른 파일 변경이 필요하면 최소 범위를 별도로 제시한다. 과거 schema/산출/영수증/기본 계산을 덮어쓰지 않는다.
3. unit-cube bank·실제 row/bounds/x0·candidate ID·count를 생산/소비 경로에 연결한다. no-provider와 봉인 warm-provider를 분리한다. 새 schema의 필수 필드 누락이 legacy fallback으로 통과하지 않게 한다.
4. 새 기능 RED→GREEN 및 변이, legacy/prep 정상 대조, 실제 소비 경로의 합성/소유 fixture, 전체 회귀·strict smoke를 수행하고 실패 기록을 보존한다. 처음부터 통과해야 하는 기존 대조군을 억지로 RED로 만들지 않는다. 검증용 작은 계산과 새 연구 실행0을 구분한다.
5. 최종 코드가 고정된 clean 커밋에서 paired_fixed5_v4/grid_fit_v5의 영수증 검증용 격리 restore/validate/rescore를 leg별 1회 수행한다. 원래 영수증은 history에 바이트 그대로 보존한다. 실패·추가 RUN_SCOPE 이동이면 최종 완료로 게시하지 말고 회신한다.
6. 서브 브랜치에만 작업하고 본진/과거 artifact/class/투영을 수정하지 않는다. 본진으로의 실제 ff-only 복귀는 이번 구현 권한으로 자동 수행하지 않는다. source digest 이동 및 producer/validator 구분을 기록한다.
7. 수정 표·최소 diff·시험/변이/수치 불변·원본 보존·최종 식별·영수증 diff를 GATE82로 제출하고 정지한다.

이 승인안에는 실제 v6 연구 leg, provider 운영 canary, numerical floor 측정, B 채택/plateau/pilot, 단계4~6, 새로운 class/투영 게시, COMSOL 계산이 포함되지 않는다. grid_fit_v5는 진단 전용이고 기존 종결·보존 한계는 유지한다.

문서 작성자가 실제 user approval/state를 만들거나 이번 요청의 ㄱㄱ를 위 구현 승인으로 전환하지 않는다.
