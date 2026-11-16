# MPM 이름·주석·관측 출력 정정 — 2026-11-16

바탕 `fd7995b29d4e7b0621cac1658edfbaf734c22ff9`, 가지 `codex/dem-observations-1116`. 1저자11-16 저녁 대기열2–5 진행 지시. 계산값·계산 순서·기존 출력 키/배열은 유지한다. 실제 엔진·현장 실행0, 운영 봉인 갱신0.

| 항목 | 바뀐 곳 | 내용 | 확인 |
|---|---|---|---|
| 2 | `scripts/viz_mpm_morphology.py`, `scripts/mpm2d_morphology.py`, `scripts/mpm3d_compaction.py` | 이름·도움말·주석을 cumulative deformation ∫‖D‖dt / cumulative plastic correction Σdg로 정정 | eps_acc의 실제 식은 norm(sym nc)×dt. 기존 식·값·색 범위 보존 |
| 3 | `scripts/mpm3d_compaction.py` 재개 로그 | F=I는 탄성 기준 상태이며 x와 누적 이력은 남는다고 설명 | pristine/no memory 삭제. 저장/재개 계산 및 키 보존 |
| 4 | `scripts/mpm3d_compaction.py` 프레임 공극률 줄 바로 뒤 | 음수 원값 때만 별도 POROSITY_OBSERVATION: frame, raw_pct, clipped=True, reported_pct | 기존 por 식 그대로. 새 진단 변수는 힘·제어·종점에 쓰지 않음. 기존 로그 줄/JSON 키/NPZ는 그대로 |
| 5 | `scripts/viz_mpm_morphology.py` build_lab → am_f → full 제목 | AM·SE·void의 분모를 raster area로 명시. scaffold를 그리기에 주지 않으면 AM 기하가 표현되지 않음을 별도 설명 | **물질점 개수 구성비가 아님**. 계산 `(lab==1)|(lab==2)`의 면적 분율 유지 |
| 설명 페이지 | `webapp/static/explain/mpm_basics_20261116.html` Q23–Q26 | 코드 정정 뒤 같은 정의를 전달. Q26의 AM 분모도 바로잡음 | Q23–Q26 밖 본문·스타일·스크립트 바이트 동일 |

## AM 0%의 생성 지점

`scripts/viz_mpm_morphology.py`는 --scaffold가 없으면 am_t/am_c/am_r를 빈 배열로 둔다. build_lab은 SE 점을 래스터에 놓고, 제공된 AM 구 단면으로 lab=1/2를 채운다. 제목의 am_f는 그 lab의 면적 비율이다. --phase를 주어 왼쪽 화면이 물질점 산점도로 바뀌어도 제목의 분모는 같은 lab이다. 따라서 해당 AM0%를 AM 물질점 수나 실제 AM 부재로 읽으면 안 된다.

원 그림13장의 실제 실행 인자는 이번에 확인하지 않았다. 개별 역사 이미지의 AM0 원인을 특정한 것이 아니라 해당 생성 경로와 분모를 확인한 것이다. `scripts/mpm3d_compaction.py`의 seed density AM값은 별도의 격자 부피 / bed 부피이며 건드리지 않았다.

Claude 소유 `docs/mpm_basics_20261116.md` §4·§5에도 물질점 장부/AM 물질점0이라는 옛 설명이 있다. 이 문서는 직접 수정하지 않고 쪽지에 같은 정의로 정정할 문장을 제안한다. 새 웹 페이지 Q26에는 올바른 정의를 반영했다.

## 시험

`scripts/test_mpm_observation_labels.py`: 수정 전 8메서드 중6실패·오류0 → 수정 후8/8. 양수·0·음수·작은 음수 공극률 입력에서 기존 por float 비트와 원식 보존, clipping 관측 원값·표지, 계산 AST 및 기존 dict/subscript 문자열 키 대조를 포함한다. 기준은 `docs/reviews/mpm_observation_labels_20261116/baseline_contract.json`이다. 검사에서는 출력 문자열/print와 명시적 관측 전용3문장만 제외하며 계산 구조를 비교한다.

작은 합성 배열로 실제 수정 렌더러를 호출해 AM0% 래스터 제목과 새 색 라벨을 확인했다. MPM solver는 import/실행하지 않았다. 생성 그림을 직접 확인했고 잘림/누락은 관찰하지 못했다. 결과는 `docs/reviews/mpm_observation_labels_20261116/verification.json`.

FAM 파일의 소스 해시는 변경된다. 계산이 보존됐다는 국소 시험을 현장 물리 자격·기존 운영 봉인 교체로 확대하지 않는다. 공유 원장·CLAUDE.md·진행 기록·scripts/check_all.sh는 변경하지 않는다.
