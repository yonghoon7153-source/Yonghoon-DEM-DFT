# Rint ② RR 회차 ② 독립 검토 증거

최종 판정은 codex_review_rint2_rr_round2_20261105.md를 읽는다.
핀: 6917c3c9fa397936d3381ba1c1785562c5232e46.

새 지적: RR2-01 P2, RR2-02 P3, RR2-03 P3. 기존 PC6-05는 재등록하지 않았다.
registered R / 물리 실행 / 배포 / 통합 / 원장 종결은 HOLD다.

received/는 받은 ZIP의 고정 파일과 별도 기록된 같은 핀 import/회귀 자료다.
원래 619개 바이트는 마지막 대조에서도 불변이다. 보충 파일은 same_pin*.json에 출처를 남겼다.
intake_results.json은 원 ZIP manifest 및 원격 repo 606 blob 대조 결과다.
litdb_identity_check.json은 카드 12개 신원만 증명하며 원문 수치 인증은 아니다.

graph_review/: 실제 작은 그래프와 증서·정확 유리수 기준·원래 교환 반례·선언된 위조 한정.
runtime_review/: 실제 파일/임시 Git + 모의 Linux 신원·순차 잠금 대체. 실제 Linux kill/flock 자격 아님.
root_review/: 재판정 byte/report 탐침, 첫 결과 표지 시험, 시간 산술.
science_review/: BAN8 독립 해석과 메모리 변이, 문헌·개발 열람 범위.

하위 REVIEW 문서의 임시 ID/등급 제안은 분석 메모다. 통합 판정의 ID/등급은 최종 판정문이 정본이다.
특히 malformed rc의 정상 생산 발생 경로는 발견하지 못했으나 실제 재개 자격이 바뀌므로 통합 등급은 P2다.
수치는 중첩 assertion이며 합산하지 않는다. 작성 측 제출 PASS를 이번 독립 실행으로 세지 않았다.

재현은 Python 3.12 + NumPy + SciPy + Git이 있는 별도 합성 폴더에서 한다.
probe_runtime.py는 합성 scratch Git을 새로 만들며 검토 소스를 수정하지 않는다.
science 변이와 후보 수정은 메모리 안에서만 하고 복구한다.
전체 check_all, 실제 연구 경로, 실제 호스트는 재현 대상이 아니다.

배포 ZIP에는 scratch Git들의 모든 object 사본은 넣지 않았다.
정확한 입력을 만드는 스크립트와 실제 recover 결과·다음 자격·후보 수정 대조를 보존했다.
원 로그의 초기 import/Windows 인코딩/추가 역사 비교 실패도 보존했다.
해시 확인: python verify_evidence.py
