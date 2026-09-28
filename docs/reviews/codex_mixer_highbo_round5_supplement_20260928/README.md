# 5차 보충 리뷰 v2 — E0 실측·Q6/Q7 (2026-09-28)

대상: 978158d334611847ed72c3086278cbee69091b63.
기존 5차 코드 핀: 091bb21143c426beecd196d6115666fdd49155b1.
두 핀 사이 믹서 코드 변경 없음. 기존 발견을 수정 완료로 올리지 않았다.

판정문: codex_review_mixer_highbo_round5_v2_20260928.md.
앞부분이 최신 보충 판단이고 부록 A는 기존 5차 판단의 보존본이다.
E0 원 덤프를 받은 것은 아니다. E0 검사 집계 JSON에서 숫자를 다시 계산했다.
첫 LH의 발사는 저자의 기록으로만 알며 실제 job_start/SLURM 원자료는 받지 못했다.
시뮬레이터·MPI·제출·실행중 작업 제어·Git 상태 변경은 하지 않았다.

## 재현

ZIP을 푼 뒤 두 폴더를 형제 디렉터리로 유지한다.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 mixer_highbo_round5_supplement_20260928/review_round5_supplement_probe.py
```

Python 3 표준 라이브러리와 동봉 원 생성기만 사용한다. 프로브가 생성기를 import해
plan의 물성/반경을 읽을 뿐, CLI 덱 생성이나 시뮬레이션을 실행하지 않는다.
실행 결과는 supplement_output.json에 기록되며 종료 코드 0, 단언 7/7이다.

- sources.json: 새 자료 9개 + 역사 문서 3개의 핀/원 Git blob SHA.
- supplement_output.json: 원문 바이트로 12/12 Git blob 일치, E0 분율·Hertz 탄성항,
  판정선 변경 반례, 문서 역사, WSL/ibb np1 영수증의 해당 수치 208행 일치.
- snapshot_comparison.json: 읽기 전용 GitHub 비교 API의 파일 변경 목록.
- history_index.json: 역사 문서의 커밋 시각. 실제 실행·열람 시각 인증이 아니다.
- history/: 초기 계약과 나중에 추가된 진단 전용 문구의 실제 문서.
- docs/: 확장 요청서와 E0 집계 원바이트, 문서 및 WSL v2 증서.

벽 초과율의 분모는 입자–면 접촉 수가 아니라 벽에 접촉한 입자 수다.
0.48% 꼬리의 힘/에너지 비중 예는 구성 반례이지 실제 E0 동역학 추정이 아니다.
기존 5차의 상세 코드 프로브·자체시험 출력/환경 제한은 형제 evidence 폴더 README 참조.
기존 전체 시험을 보충에서 다시 실행하지 않았다.

## 판정 요약

HOLD 유지. E0의 기존 1% 계약은 3/3 실패이며, 분위수로 변경해 소급 합격시킬 수 없다.
새 계약은 부분 결과 열람 뒤 개정으로 표시하고 독립 오차 근거가 필요하다.
첫 LH 선발사는 자동 폐기 사유가 아니나 실제 실행 기록을 독립 대조해야 한다.
본 캠페인의 "원래부터 진단 전용" 해석은 초기 §1과 충돌한다.

