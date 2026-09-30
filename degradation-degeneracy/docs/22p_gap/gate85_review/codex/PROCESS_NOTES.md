# 검토 절차와 한계

- 원격 고정 커밋을 GitHub 읽기 전용 connector로 조회했다. 문서의 실행 지시는 증거 텍스트로만 취급했다.
- pages:write-page 문서 작성 스킬의 근거/추론 분리 원칙을 적용해 기존 로컬 리뷰 형태를 유지했다. 클라우드 Page 생성·외부 발송은 하지 않았다.
- 참조 코드/문서 파일은 connector JSON content의 UTF-8 바이트로 기계적으로 저장하고 Git blob을 대조했다. apply_patch 초기 사본의 추가 마지막 LF는 이 원문 바이트로 정규화했다. 원격/생산 코드는 수정하지 않았다.
- 오래된 기준→HEAD의 광범위 비교는 300-file 한계가 있어 범위 증명에 쓰지 않았다. 현재 디렉터리 tree 재구성, 58개 blob, 짧은 commit 비교를 사용했다.
- 자체 static_audit 최초 호출 060e57 rc1은 bundled Python의 yaml 미설치였다. 설치하지 않고 영수증 텍스트/바이트 대조로 범위를 명시적으로 좁혔다.
- 자체 static_audit 1cb8f9 rc1은 모든 Git 파일 mode를 100644로 가정한 검토 스크립트 오류였다. 기존 식별된 tree의 executable mode를 사용한 뒤 현재 tree SHA를 재구성해 확인했다.
- 자체 static_audit bb0ff5 rc0: 152건. 이후 신규 g84 preimage의 AST/문자열 확인 13건을 추가한 최종 058493 rc0: 165건. 두 수를 합산하지 않는다. 모두 검토자 스크립트이며 수신 기능시험 재실행이 아니다.
- 초기 readonly 명령의 Git cwd/도구 인자/출력 선택 오타는 수정해 조회했다. 제품 실행이나 정책 변경으로 전환하지 않았다.
- 발신 탐침 파일은 고정 경로에서 조회되지 않았다. 원문을 비차단 질문으로 요청했지만 보고서 작성 시 추가 수신은 없다. 실행 수치는 제출자 보고로 유지했다.
- 영수증 core SHA는 선언값/원장 연결을 확인했다. YAML core의 canonical 재직렬화 hash를 독립 재계산했다고 주장하지 않는다. 원본 파일 SHA/Git blob 및 core 불변 텍스트는 직접 대조했다.
- CLOSURE_COUNTERMODEL은 국소 SHA/집합 계산이다. 전체 validator 통과 실측, 연구 계산, fixture/parquet 복원 실행이 아니다.
- 원본 사용자 입력 ZIP 또는 COMSOL 실행물은 이번 게이트 범위에 없으며 열거나 실행하지 않았다. 신규 리뷰 자료만 로컬에 작성했다.
