# DEM 언로딩 키트 수정 재확인 — 전달 묶음

검토일: 2026-10-15. 대상 코드 핀: `eaecfba2a2dfbff6f13222f6afeb01d8ebeb5a84`.

## 먼저 읽을 것

- `codex_review_dem_unloading_kit_fix_recheck_20261015.md`: 최종 판정 **HOLD**, 기존 항목별 닫힘, Q1–Q6, 잔여 P2 세 건 및 최소 해제 증거.
- `evidence/resume_recheck.json`: 재개·분리 37사례. 기대 성질 32개 충족. 실패한 기대 5개를 결함 5건으로 세지 않는다.
- `evidence/receipt_ids_recheck.json`: 영수증·ID 92단언. 기대 성질 90개 충족. 나머지 둘은 같은 G2c 열 결손 경로의 두 변형.
- `notes/`: 각 탐침의 해석과 한정.

실제 LIGGGHTS·MPI·스케줄러는 실행하지 않았다. 대상 코드·등록값·생산 덱은 수정하지 않았다. `source/`는 핀에서 읽은 원본 사본이며, `source_manifest.json`의 Git blob 및 SHA256으로 마지막 포장 때 다시 확인했다. 제출된 Linux 실행 로그와 이번 독립 Python 탐침은 구분했다. Windows의 Bash 시작 실패 및 자체시험 LF/CRLF 차이를 운영 코드 결함으로 세지 않는다.

## 구성

| 경로 | 내용 |
| --- | --- |
| `source/` | 핀에서 읽은 원본 252파일; 키트·등록·기존 판정·Linux 증거·기존 실측 H0–H5 archive 포함 |
| `submitted/` | 첨부 요청서, 앞 판정 및 커밋 번호 정정 자료 |
| `probes/` | 독립 반례·양성 대조·재판독 도구 |
| `support/` | 앞 리뷰의 복원 양성 fixture 생성 함수 사본 및 출처 설명 |
| `evidence/` | 이번 결과 JSON, 전문 로그, 최종 탐침이 참조한 합성 자료, 기존 실제 이력의 안전 추출본 |
| `PACKAGE_MANIFEST.json` | 포장 파일별 길이와 SHA256; 자기 자신은 제외 |

중간 탐침 실행 폴더와 임시 자체시험 폴더는 삭제하지 않고 ZIP에서만 제외했다. 최종 JSON이 참조하는 재개·영수증 fixture 폴더는 포함했다. JSON 안 절대 경로는 원 실행 위치를 보존한 것으로, 압축을 푼 위치에서 새 탐침을 실행하면 새 위치의 합성 자료와 결과를 만든다.

## 재현

이 폴더를 작업 디렉터리로 사용한다. Python 표준 라이브러리만 필요하며 실제 시뮬레이터를 호출하지 않는다.

```text
python -X utf8 -B probes/resume_recheck.py
python -X utf8 -B probes/receipt_ids_recheck.py
python -X utf8 -B probes/grammar_types.py
python -X utf8 -B probes/grammar_provenance.py --run-id independent1
python -X utf8 -B probes/grammar_windows_r32.py
python -X utf8 -B probes/history_actual.py
python -X utf8 -B probes/kit_byte_checks.py
```

탐침의 rc0은 결과 저장 완료를 뜻할 수 있다. JSON의 `failed_expectations`와 사례별 판정을 읽을 것. 보존된 결과를 유지하려면 ZIP을 별도 폴더에 풀어 재현할 것. `grammar_provenance.py`의 run-id는 실행마다 새 값을 쓸 것.

`prepare_sources.py`와 `probes/source_audit.py`는 원본 수집·온라인 핀 대조의 작업 기록이다. 과거 검토 폴더 및 네트워크를 참조하므로 이 ZIP 단독 재현 명령에 포함하지 않는다. 그 결과는 `source_manifest.json`, `tree.json`, `evidence/source_audit.json`에 보존했다. `run_baselines.py`는 운영 Bash 의존 시험도 포함하므로 위의 표준 라이브러리 탐침과 구분한다.

## 포장 검증

`package_review.py`는 모든 원본 252파일의 바이트·Git blob을 검증하고, 전달 파일별 해시를 기록한 뒤 ZIP의 CRC와 파일별 해시를 다시 읽어 대조한다. 이는 전달 무결성 검사이며 코드의 과학적·논리적 정확성을 보증하지 않는다.
