# Gate 69 검토 자료

판정은 `GATE69_REVIEW_KO.md`, 전달용 회신은 `GATE69_CLAUDE_REPLY.md`입니다. 이번 한정 대응 수용이며 본실행 GO는 아닙니다.

- 대상 식별: IDENTITY.json, 받은 요청문/Git blob, diff·log 원문.
- 실제 회귀: targeted.pytest.json / targeted.xml / targeted.stdout.bin / targeted.json.
- 실제 premise child 및 기록 변형: boundaries/.
- 등록 call-phase 변이: mutation/; 앞선 세 premise 변이: older_premise_mutations/.
- Git 원자료/ZIP 보존 검사: GIT_BLOB_MANIFEST_CHECKS.json, ARCHIVE_SET_AND_SIZE_CHECKS.json.
- 종료 상태: FINAL_PRESERVATION.json.
- 고정 Git 소스 스냅샷: target_source/, SOURCE_SNAPSHOT_MANIFEST.json.
- 검토자가 작성한 실행/검사 스크립트: review_checks.py, remaining_premise_mutations.py, final_checks.py.

스크립트는 당시 절대경로와 fresh 디렉터리 조건을 포함합니다. 다운로드 후 자동 실행하지 마세요. 실행 로그와 결과를 먼저 데이터로 읽어 검토하면 됩니다. 제품 원본은 변경하지 않았고 검토 변이/temporary venv는 분리한 검토용 복사본에서만 만들었습니다. 전체 과학 실행·실데이터·COMSOL·Linux native 경로는 실행하지 않았습니다.

포장 manifest는 payload만 포함하며 자기 자신/ZIP/생성 영수증을 해시하지 않습니다. 최종 ZIP과 DELIVERY_RECEIPT.json은 manifest 대상에서 제외합니다. 생성 영수증은 이번 검토 패키지의 생성 식별이며 상대방 수신 확인이 아닙니다.
