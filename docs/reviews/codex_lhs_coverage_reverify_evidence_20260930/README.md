# LHS 피복률 재검증 — 독립 증거 (2026-09-30)

판정문: docs/reviews/codex_lhs_coverage_reverify_verdict_20260930.md.
요청서/패치 핀: ac484ba5cda082caffe2c3c408de86cbd760befc.
검토 대상: da4670594 + 제출 0001–0011. 이전 검토 핀: 2e57dff90e7eebead7a446478f97e2c414176c28.

## 결과와 포함 범위

- 기존 P1 두 건 닫힘, 이번 범위 새 P1 발견 없음. LHSC-03·04의 P2 잔여로 묶음 HOLD.
- audit.py / audit_harvest.py / audit_cli.py: 이전 감사 스크립트를 수정 없이 후보 트리에 실행.
- audit_pipeline.py: 이전 코드의 atoms-only full_metrics.read_text 한 곳에 파일 존재 guard만 추가. 거부 시 파일이 없는 것이 정상이다.
- audit_delta.py: 실제 생산자의 정상 파일과 변이 스키마, 실제 contact_area_check를 이용한 지원 범위 안 반올림 반례, SE-only 양성 대조, 깨끗한 import 검사. decimal60 교차검산 포함.
- prior_audit_results.json: 이전 핀에서 실행한 결과. 옛 반올림 반례의 입력만 가져오기 위해 포함했다. 현재 결과와 혼동하지 않는다.
- selftests.json / *.log / *_results.json / harvest_comparison.json: 독립 실행과 명시된 플랫폼 통제 결과.
- fixtures / delta_fixtures / pipeline_fixtures / cli_fixtures: 합성 원자료와 출력. 실 130/64 침대가 아니다.
- lhs_coverage_reverify_20260930/source_manifest.json: 새 패치 SHA와 후보 대상 9파일 SHA, 이전 패치와의 비교.
- lhs_coverage_review_20260930/{baseline,candidate}: 이전 대상 8파일 및 옛 패치 7개를 대조용으로 포함.
- lhs_coverage_reverify_20260930/candidate: 이번 대상 9파일. **이 ZIP은 완전한 실행 저장소가 아니다.**
- submitted 아래 로그·재현 결과는 제출자 증거다. 독립 로그는 이 README가 있는 증거 폴더에 있다.
- PACKAGE_SHA256SUMS.json은 각 ZIP 구성원의 SHA256. ZIP 자체 해시는 옆 .json에 있다.

기존 0001–0007은 원시 패치 바이트/SHA가 전부 다르지만 diff --git 이후 본문은 7/7 동일하다.
메일 패치 번호와 제목 인코딩/줄 접기 변화다. 이전 GO 코드가 달라졌다는 뜻은 아니다.

## 실행 환경

Windows / Python 3.12.14 / NumPy 2.3.5 / pandas 3.0.1 / SciPy 1.16.3 / NetworkX 3.7 / Flask 3.1.3.
의존 라이브러리는 ZIP에 포함하지 않았다. 분석 대상은 이 핀의 전체 소스 사본이어야 한다.
생산 checkout을 변경하거나 시뮬레이션을 실행할 필요는 없다.

1. 별도 전체 소스 사본에 da4670594 기준 제출 패치 0001–0011을 적용한다.
2. 후보 대상 파일 SHA가 source_manifest.json의 candidate_targets와 일치하는지 확인한다.
3. 증거 보존을 위해 압축 해제 사본에서 아래 스크립트를 실행한다. 증거 디렉터리 안의 fixture와 결과는 다시 쓴다.

~~~bash
export LHS_REVIEW_REPO=/absolute/path/to/isolated/full/candidate
export LHS_REVIEW_BASELINE=/absolute/path/to/unpacked/lhs_coverage_review_20260930/baseline
export PYTHONUTF8=1
export PYTHONDONTWRITEBYTECODE=1
python3 lhs_coverage_reverify_evidence_20260930/audit.py
python3 lhs_coverage_reverify_evidence_20260930/audit_pipeline.py
python3 lhs_coverage_reverify_evidence_20260930/audit_harvest.py
python3 lhs_coverage_reverify_evidence_20260930/audit_cli.py
python3 lhs_coverage_reverify_evidence_20260930/audit_delta.py
python3 lhs_coverage_reverify_evidence_20260930/run_selftests.py
~~~

PowerShell은 export 대신 $env:LHS_REVIEW_REPO='C:/...' 등을 쓴다.
이전 감사 코드의 기본 경로는 이전 review 디렉터리이므로 LHS_REVIEW_REPO를 반드시 명시한다.
audit_delta.py의 prior_audit_results.json은 같은 증거 디렉터리에 이미 포함되어 있다.

## 측정과 대역의 경계

- audit.py의 v2 산출물은 실제 compute_case와 합성 atoms/contacts CSV로 생성된다.
- audit_delta.py의 스키마 변이는 실제 정상 compute_case 산출물에서 출발한다.
- 변이 파일을 _coverage_stage까지 넣는 두 검사는 계산 subprocess만 명시적 malformed writer로 대체한다. 검증기·필수 단계·최종 상태 요약은 실제 함수다. 정상 producer가 그 파일을 만든다는 주장은 아니다.
- 반올림 반례는 실제 geometry 함수, 실제 _in_domain_rows, 실제 contact_area_check를 호출한다. 60자리 독립 십진 계산에서도 동일 %.6g 면적 토큰이다.
- 깨끗한 import 검사에서는 별도 Python 프로세스에 수확기만 import한다. plastic_coverage가 sys.modules에 없는지 검사한다.
- 파이프라인 감사는 원격 DB 설정을 비우고 계산 subprocess를 대역 처리한다. atoms-only 반례는 subprocess를 호출하지 않는다.
- batch copy-shim은 Windows symlink 권한 제한을 우회한 테스트 통제다. 실제 배포 symlink의 성공 증서가 아니다.
- harvest LF 통제는 fixture 쓰기만 LF로 바꾼다. 기준/후보 τ median은 둘 다 2.080532952769607이며, 고정 핀 2.0805329527696066과 1 ULP 차이다.
- 깊은 겹침 반례의 실 코퍼스 빈도·물리 적격성은 미측정. 새 반올림 반례는 기록용 진단만 건드리며 피복률 값·수확 거부에는 사용되지 않는다.
- 전체 check_all은 독립 재실행하지 않았다. 제출자의 gate 169/170과 litdb 단독 통과는 제출 증거로만 보관했다.

독립 selftest: lens 5, plastic 28, coverage 16(①b 포함), provenance 206, dataset 113 통과.
수확기 원형 142/144 → LF 통제 143/144(τ 핀 1 ULP 남음). 배치 원형 권한 실패 → copy 통제 29/29.
legacy 수확기 16호출 × 36키 불일치 0. 이를 “전체 초록”으로 요약하지 않는다.

## 최소 반례를 읽을 곳

delta_results.json:
- schema_mutations.missing_n_am_and_coverage: accepted=true / required_stage_ok=true / pipeline_status=done.
- schema_mutations.area_nan: 동일한 필수 단계 false-green.
- in_domain_rounding_false_alarm: domain=true / boundary=0 / beyond=1 / diff_over_tol=1.3323976750260462.
- old_examples_at_production_entry: 옛 반례 3개는 boundary=1 / beyond=0으로 바뀜.
- clean_harvester_import: rc=0 / stdout=False.

보고서와 로컬 소스 링크는 원래 작업 공간의 절대 경로다. 다른 컴퓨터에서는 ZIP 안의 동일 상대 파일과 줄 번호를 사용한다.

