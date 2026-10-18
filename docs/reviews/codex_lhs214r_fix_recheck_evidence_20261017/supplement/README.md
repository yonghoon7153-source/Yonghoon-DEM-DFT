# LHS214 증거 보충 확인 묶음

`codex_lhs214r_evidence_supplement_20261017.md`가 이번 보충 판정입니다. 확정 핀은 `a4a1e52c0bc01731f4c1d00924099b56c05a055f`이고, 코드 핀 `60ba39e22`와 scripts/webapp 전체가 동일합니다. 기존의 후속 커밋·증거 미확인 제한만 해제하며, 기존 P2 1건·P3 2건 및 HOLD는 유지합니다.

- `submitted/`: 받은 ZIP의 요청서·증거·PIN.txt. Git blob 및 SHA256 검증 완료.
- `evidence/`: 원격 비교/트리/파일 대조, A4 직접 재실행 결과와 환경 어댑터 기록.
- `notes/consumer_supplement.md`: 제출 로그 및 소비자 증거 교차검토.
- `verify_and_a4.py`: 원 스크립트 본문을 바꾸지 않고, Git 읽기를 검증된 이전 스냅샷으로 공급하는 재현기.
- `PACKAGE_MANIFEST.json`: 전달 파일 해시·크기.

재현은 이전 `lhs214r_fix_recheck_20261017/` 검토 폴더를 이 폴더의 형제 위치에 두고, 동일한 Python 라이브러리 환경에서 수행합니다. 이전 67.7 MB 전체 증거 ZIP은 이번 보충 ZIP에 중복 포함하지 않습니다. 외부 의존성 경로는 실행기에 명시되어 있습니다.

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B './lhs214r_supplement_a4a1e52c0_20261017/verify_and_a4.py'
```

`--verify-only`는 원격 기록과 받은 파일의 바이트 대조만 수행합니다. 전체 실행은 보충 폴더의 로그·JSON을 다시 쓰므로 원본 ZIP을 보존하고 사본에서 실행하세요. source/base와 실제 Git 상태는 변경하지 않습니다. 원격 기록의 재조회는 원격 읽기 도구가 필요하며 이 실행기는 이미 보존한 원격 기록을 사용합니다.
