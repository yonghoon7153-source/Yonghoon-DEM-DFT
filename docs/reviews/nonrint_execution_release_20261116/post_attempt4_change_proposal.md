# 대기열 2–5 — 코드 변경 전 줄·시험·영향 제안

현재 조사 핀 `6c1144cde6b3671be55b85c626044020ae1f734d`. **이 문서는 제안이며 아래 대상 코드 변경0·시험 실행0이다.** 1저자11-16 지시에 따라 먼저 Claude에 고정 범위를 알린다. Claude 반입 뒤 실제 파일의 줄을 다시 대조한다.

| 항목 | 지금 바꿀 후보 줄 | 제안 | 시험을 먼저 만들 내용 | 영향·선행 |
|---|---|---|---|---|
| 2 | `scripts/viz_mpm_morphology.py` 146–147 · `scripts/mpm2d_morphology.py` 8·170·178 | total strain ε (vs seed) → 누적 변형량 ∫‖D‖dt, plastic strain Σdg → 누적 소성 보정량. 연관 주석/설명도 같은 뜻으로 | 기존 라벨을 기대 새 문구로 검사해 red, 수정 뒤 green. 같은 합성 배열의 색·범위·좌표·집계 바이트 보존; 라벨 이외 그리기 호출 AST 동일 | 렌더링 문구만. 물리/측정 수치0변경. 현재 ε 누산 정의가 ∫‖D‖dt와 맞는지 최신 생산식 읽기 대조 뒤 적용 |
| 3 | `scripts/mpm3d_compaction.py` 2245·2250 | pristine/no memory 단정 삭제. F=I는 탄성 기준 상태이며 x와 누적 이력이 유지됨을 설명. 위쪽 plastic history F 표현도 F/이력 구분 | 같은 합성 x·F·Σdg의 저장/재개 객체와 계산 AST 불변, stdout 해당 문구만 변화. F 초기화가 x/Σdg 초기화를 뜻하지 않는 문구 반례 | FAM 봉인 파일. 먼저 Claude와 문구 범위 확정. 엔진 실행0·수치 변경0; 새 source SHA를 기존 봉인에 자동 적용하지 않음 |
| 4 | `scripts/mpm3d_compaction.py` 3261 `por = max(0.0, 1.0 - solid_vol / (area * height)) * 100.0` | 이 줄의 값/순서 그대로. 별도 관측 출력에 por_raw_pct와 por_clipped를 추가해 음수 원값 보존 | 양수·0·작은 음수·큰 음수 합성 입력에서 기존 por의 float 비트 보존. raw<0일 때 표지, 원값과 단위 기록. 제어·힘·종점 입력으로 유입하지 않는 AST/의존 검사 | 숫자 계산·제어 변경0. 출력 계약만 별도 추가. restart/기존 NPZ·봉인 스키마 변경은 이번 제안에 포함 안 함 |
| 5 | AM 0%가 표시된 실제 패널의 생성 지점 **[미확인]** | 물질점 조성 패널이면 물질점 구성비로 표기하고 scaffold AM 장애물은 별도라고 명시 | SE-only 물질점 + AM scaffold 합성 자료에서 표기/분모 검사. AM 장애물 존재를 물질점 AM0으로 소거하지 않음 | 해당 그림/템플릿 식별이 먼저. 현재 찾은 아래 두 분율은 물질점 구성비가 아니므로 일괄 이름 변경 금지 |

## 1. 항목5의 중요한 구분

`scripts/viz_mpm_morphology.py`의 AM 비율은 raster lab에서 `(lab==1)|(lab==2)`의 면적 비율로 계산한다. `scripts/mpm3d_compaction.py` 2371–2379의 seed density AM 비율은 pin 격자 부피 / bed 부피다. 둘을 물질점 개수 구성비로 바꾸면 뜻이 틀린다. 따라서 요청한 AM0% 패널의 실제 생성 위치가 확인될 때까지 문구를 고치지 않는다. 새 값 열람 없이 생성 코드/템플릿으로 위치를 식별한다.

## 2. 공동 경계

`docs/mpm_basics_20261116.md`는 Claude 반입 예정 기준 자료이며 현재 이 가지에 없는 본문을 확인했다고 기록하지 않는다. Claude 소유 `docs/reviews/dem_redesign_direction_20261109/seminar_feedback_20261113.md`, `docs/mpm_basics_20261116.md`, `webapp/static/explain/mpm_basics_20261116.html`, `CLAUDE.md`를 만들거나 고치지 않는다.

보존: Rint 실행 핀과 고정 가지, 공유 풀이·payload·네트워크 코드, kgy 트리/저장본. 50kg Love–Weber 재작도0. G2c′ 366288·366290 고정이며 새 계산·제출0. 위 네 제안은 수영 실행 블록/믹서 E0 발사 도구와 분리하여 다음 변경으로 처리한다.
