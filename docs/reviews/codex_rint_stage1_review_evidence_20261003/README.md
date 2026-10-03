# r_int stage1 독립 리뷰 묶음

판정문: codex_review_rint_stage1_20261003.md — **G1 HOLD / G2 HOLD**.

이 묶음은 생산 소스 수정본이 아니다. source/는 핀된 원본, evidence_*/는 합성 CPU 탐침·실행 로그다. 실제 DEM/MPM/GPU 캠페인이나 실침대 전수 검증을 포함하지 않는다.

## 무결성

- 구현 커밋: 5e0efdb8d185fb3a7fc152983ebf543f7b873e1c.
- 리뷰 문서/소비처 핀: 62f9e4cb3e969d13cf0c311858b5159ac75d6396.
- 핵심 코드 세 파일의 Git blob이 두 핀에서 같음을 source_manifest.json에 기록했다.
- 23개 원본의 Git blob SHA-1을 로컬 바이트로 재계산했고 모두 일치한다.
- inputs/request.md와 inputs/supplement_log.txt는 사용자 전달 원본이다.
- SHA256SUMS.json은 묶음 내 각 파일의 SHA-256이다. 압축파일 자체 해시는 배포 시 따로 제공한다.
- supplied log 일치는 출력된 유효 숫자 기준이며, 플랫폼 간 모든 미출력 비트 동일을 뜻하지 않는다.

## 실행 환경

검증에 사용한 Python 3.12.14 / NumPy 2.3.5 / SciPy 1.16.3.
의존성 패키지는 ZIP에 포함하지 않았다. 해당 패키지가 있는 Python 환경에서 실행한다. 추가 설치·GPU·네트워크는 탐침 자체에 필요하지 않다.

리뷰 폴더를 현재 디렉터리로 두고:

```text
python replay_review.py
python replay_review.py --full
```

기본 실행: 핀 검사, 제공 selftest/세 탐침, 소비처·면적·단위 독립 탐침.
--full: 실제 producer의 합성 OFF/ON/호출부 변이, 전체 규칙 J 원본/변이, check_arm, 계약 대조까지 추가.
변이의 PASS는 수정 완료가 아니라 현재 게이트의 거짓 초록을 재현하는 결과다.

NumPy/SciPy를 별도 디렉터리에서 쓰는 경우:

```text
python replay_review.py --deps /absolute/path/to/python/packages --full
```

재실행은 evidence_*/ 안의 합성 산출·일부 로그를 갱신한다. **수령 ZIP을 보존하고, 풀어 놓은 사본에서 실행**한다. source/는 읽기 전용으로 다루며 탐침도 변경하지 않는다. CPU toy도 별도 파일/메모리는 사용한다.

기존 리뷰 환경의 PowerShell 예시:

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' replay_review.py --deps 'C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/deps' --full
```

## 핵심 증거 연결

| 판정 | 증거 |
|---|---|
| 제공 로그 재현 | evidence_gates/reproduction_metadata.json · reproduction_comparison.json |
| 주 rint 배선 삭제 | evidence_gates/payload_mutation/summary.json · rule_J_mutant.stdout.txt |
| wetted/bare 변이 | evidence_gates/payload_mutation/summary_extended.json |
| 실제 check_arm/최종 계약 | evidence_gates/check_arm_mutant.stdout.txt · contract_edges.json |
| OFF AM pid 지도 오염 | evidence_consumers/consumer_results.json → pid |
| Joule/STEP4 규약 혼합 | 같은 파일 → joule / reaction_scope / serialization |
| 면적 정규화 후 위치 반례 | evidence_area/probe_outputs.json → AM_boundary_placement |
| L1/접합/모델 간 비교 한정 | evidence_area/independent_area_review.md |
| 단위 10⁻⁸ 및 비식별성 | evidence_root/probe_units_identifiability.json |
| VGCF100 도입 코드 | evidence_root/vgcf_origin_excerpt.json |

전문 보조 보고서 consumer_audit.md, independent_area_review.md, gate_findings.txt도 포함했다. 최종 통합 등급과 한정은 한국어 본문이 정본이다.

