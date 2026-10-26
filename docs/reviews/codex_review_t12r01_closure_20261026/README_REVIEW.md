# T12R-01 외부 종결 재확인 (2026-10-26)

판정문: `codex_review_t12r01_closure_20261026.md`.

**T12R-01 CLOSED — 자동 fetch 차단·정상 52개 결과 보존에 한정. 실제 물리 실행 GO는 별도.**

- 검토 핀: 96f15ed17e03181b6096fb65f71ec7f577f17523.
- 후보: 3eecce8af503556b678f8f4a02343e6bce3d0b83.
- 소비자: 4c29705fa1c4ba94737a858b206fa4f4c5bb2bde.
- 실제 Windows Git 2.55.0: 누락 객체 11조건 모두 rc2/fetch0/저장소 파일 불변. 보호 제거 대조 fetch3.
- 완전한 필요 객체: 기존 52개 전체 관측 배열·여섯 소스 hash 동일. 별도 8/8 거부, 13/13 변이 재현.
- 미지원 Git 응답은 mock. 실제 옛 Git 인증 아님. 공유155는 제출 로그 감사.

`review_scope.json`은 좁은 외부 종결이며 범용 물리 GO 칸에 넣지 않는다.

새 폴더에 ZIP을 펼친 뒤 그 폴더에서:

```bash
python3 -I -X utf8 -B build_object_repo.py
python3 -I -X utf8 -B probe_offline_independent.py --out ./fresh_offline_recheck
```

원래 Git 객체 metadata와 동봉 consumer 여섯 파일로 독립 시험 저장소를 만든다. 기존 리포가 필요 없고 외부 fetch도 필요 없다. 반례 대조는 file 프로토콜의 로컬 빈 원격만 허용한다. 원문 snapshot·실제 trace·반환 코드·관측값을 보존했다. 기존 출력 폴더를 재사용하지 않는다. 새 Git 객체 저장소·실행 임시파일은 패키지에서 제외했다.

`intake.py`는 최초 Downloads 첨부 반입 기록이며 재현의 필수 단계가 아니다. `run_harnesses.py`는 기존8/13을 다시 실행할 수 있지만 새 추출 폴더에서도 evidence/loader·mutants가 이미 있으므로 실행 전 별도 사본에서 출력 이름을 바꿔야 한다. 핵심 독립 재현은 위 두 명령이다.
