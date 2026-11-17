# 오프라인 소형 검토 재현

첨부 증거를 풀어 놓고, 코드 핀 `64e4d213e8267bafaf3ae5af00a42996cefd3f33` 및 역사 커밋 `6bf70fe4a`, `11a794674`, `b3481336c`와 필요한 blob을 이미 가진 **로컬 고정 저장소**를 준비한다. Python의 해당 `sys.executable`에 numpy/scipy가 이미 설치돼 있어야 한다. 설치·추가 네트워크 fetch는 준비 도구가 하지 않는다. 실제 운영 원장/저장본/킷/결과 경로를 인자로 주지 않는다.

```powershell
python -I -B prepare_reproduction.py --repo 'D:/local-fixed-repository' --out 'D:/new-review-reproduction'
```

`--out`은 존재하지 않는 새 폴더이며 원 증거 및 원 저장소 밖이어야 한다. 원 저장소는 객체를 읽기만 한다. 새 bare 저장소에 read-only 객체 alternates를 두고 **첨부된 로컬 bundle만** 받아 후보 `c80d700bdd5915da82f77f839cb96ed4a5a6582e`의 필요한 scripts/문서 경로만 sparse checkout한다. 전체 저장소 archive, 원 저장소 ref/index/config 수정, 원격 fetch는 하지 않는다. 부족한 고정 객체가 있으면 준비/검증이 실패하며 자동으로 가져오지 않는다. alternates를 사용하므로 재현 중 원 객체 저장소를 유지한다.

원 로그·보고서는 새 폴더의 `reference_evidence`에 별도 보존한다. 실행 폴더에는 동일한 검토 스크립트만 복사하므로 새 결과가 원 성공 로그를 덮어쓰지 않는다. `PREPARATION.json`의 7개 script SHA256 원본/사본 일치와 후보 커밋을 먼저 확인한다. `seal_form_review/work/scripts`는 후보 코드 사본이다. 제외된 `work/deps`가 없어도 Python 전역 numpy/scipy를 사용한다.

아래 **7개만**, 새 출력 루트에서 순서대로 실행한다. `probe_form_build.py`가 만든 시험 고정물을 `probe_s0_gate.py`가 사용한다. 출력 저장은 새 루트 안에서만 한다.

```powershell
Set-Location 'D:/new-review-reproduction'
python -I -B -X utf8 measurement_review/verify_measurements.py
python -I -B -X utf8 measurement_review/verify_e4_baseline.py
python -I -B -X utf8 seal_form_review/scripts/audit_supplied_form.py
python -I -B -X utf8 seal_form_review/scripts/audit_pin_boundary.py
python -I -B -X utf8 seal_form_review/scripts/probe_form_build.py
python -I -B -X utf8 seal_form_review/scripts/probe_s0_gate.py
python -I -B -X utf8 resume_review/review_resume.py
```

여러 로그의 검사 수는 서로 다른 단위이며 중복도 있으므로 합산해서 하나의 통과 건수로 주장하지 않는다. 측정 자료 검사는 제공된 비수송 기록/선언 해시와 고정 소스의 대조다. 전체 게이트, 엔진, S0 census, 실침대, GPU, 실제 원장 전송, 실제 봉인을 실행하는 안내가 아니다.

봉인 형식 시험은 Windows stdout만 LF로 맞춰 원본 사슬의 plan-doc를 호출한다. 이는 Linux 현장 전체 실행 확인이 아니다. 재개 시험의 일부 제어 함수는 정확한 AST 본문을 작은 모의 환경에서 검사하며 Linux flock/프로세스 동작이나 현장 두 기계 전송의 완전 재현을 뜻하지 않는다.

시험의 네 값 `12`, `'none'`, `2.0`, `'all3'` 및 해시 불일치 시험의 `3.0`은 모두 fixture 전용이다. 실제 미정값 결정·추천이 아니다. `TEST_ONLY_final_output`과 소형 Git 커밋을 실제 봉인으로 가져가지 않는다. 원 검토는 Python 3.12.14 / numpy 2.3.5 / scipy 1.16.3에서 했으며 현장 봉인 환경 3.8 / 1.24.4 / 1.10.1을 대체하지 않는다.
