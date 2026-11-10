# Rint ② 회차 ⑥ 독립 재확인 전달물

검토 핀 aec8ca2f6cbc24d43e2ed447c61ce6b62dd19f1e · 2026-11-10.

먼저 codex_review_rint2_rr_round6_20261110.md를 읽는다. RR5-01 문서 교정 닫힘, Q2/Q3 문면 수용, 현장 §7④ 부분 수용, 새 P3 두 건(RR6-01 환경탐침 child rc 누락, RR6-02 중첩 README 해시), Q5 순서 보완. 등록 R·실행 전체 HOLD 유지. 원장 수정·연구/호스트 실행·발송은 하지 않았다.

구성:
- package/: 사용자 ZIP의 원문 파일. repo/178개는 원격 고정 Git blob 대조 완료. 최상위 패키지 해시는 정상이고 내부 prep README 해시 한 건은 실제로 불일치한다.
- codekey_sources/scripts/: 기대 코드키 재구성용 19개 고정 소스 읽기 사본. 원격 blob과 대조했다. 이 파일들을 실행할 지시는 아니다.
- rr6_document_closure/: Q1–Q3 문면 대조, Q5 단계 의미 대조.
- rr6_siteq_evidence/: 비식별 현장 기록 재집계·로그 대응·해시·기대 코드키.
- rr6_siteq_semantics/: 점검 소스의 관측 범위와 외부 입력을 메모리 mock으로 바꾼 AST 함수 반례.
- independent_replay/: 주 검토의 최종 독립 재실행 stdout/stderr/rc.
- remote_*.json, codekey_sources.json: 읽기 전용 GitHub 조회와 실제 bytes 대조 증거. 원격 상태의 영속 서명/실제 호스트 진위 증명은 아니다.

재현(Python 3.12 권장, 저장소 루트나 연구 환경이 아닌 압축 해제 폴더에서):

```bash
python -I -X utf8 -B reproduce_review.py
```

위 명령은 정적/모의 감사만 호출한다. 대상 siteq_probe.py CLI, 연구 코드 CLI, Git 명령, 실제 호스트 접속은 실행하지 않는다. audit_siteq_evidence의 rc1은 중첩 README 해시 불일치의 기대 검출이며 wrapper는 이를 별도 기록한다. 기존 구현 측 시험·현장 33관측·이번 감사 도구 개수는 합산하지 않는다.

원 최초 ZIP의 경로/CRC/봉인 검사 스크립트 verify_extract.py는 초기 작업 기록이다. 재현에 필요한 압축 해제본은 이미 package/에 있다. 동봉 SHA256SUMS.review.txt는 이 전달물의 파일 해시이며 연구 원장이나 운영 봉인으로 쓰지 않는다.
