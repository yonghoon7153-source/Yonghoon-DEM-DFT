# R13 검토 자료 재현 안내

판정: **NO-GO**. 주 보고서는 `HARNESS_R13_94ADD7B5_CODEX_REVIEW.md`다.

## 범위

이 묶음은 `bms-balancing/`의 과학 데이터/schema/CLI 기능 검사와 보관 파일의 읽기 전용 감사를 포함한다. 보안 우회 PoC, import/bytecode/filter 공격 재생, 과거 공격 스크립트는 포함하지 않는다. 원자료 fitting이나 MATLAB 원본 동치 검증도 포함하지 않는다.

대상 HEAD: `94add7b5d48ad5d19448d562a0909b15ce4dc056`.
코드 정본: `c7217c04f939889e88b915575fce6997005072aa`.
첨부 요청문과 대상 `reviews/R13_REQUEST.md`의 SHA-256은 같다.

대상 checkout은 별도로 준비하고 기존 변경을 덮어쓰지 않는다. 여기의 검사 스크립트는 target을 읽고 `--out`에 합성 자료만 생성한다. `--out`은 재실행마다 새 디렉터리를 사용한다. review script의 rc 0은 검사를 완료했다는 뜻이다. 개별 제품 판정 rc와 `promotion_eligible`은 results.json 및 stdout을 읽어야 한다.

## 이 기계에서 사용한 환경

- WSL Ubuntu / Python 3.12.3: `/home/yonghoon71/ddvenv/bin/python`.
- NumPy 2.5.3, SciPy 1.18.1, pandas 3.0.5, pytest 9.1.1, openpyxl 3.1.5.
- pytest 등 보조 패키지는 기존 `work/harness-r2-pydeps`를 PYTHONPATH로 사용했다.
- `PYTHONDONTWRITEBYTECODE=1`; 대상 소스 수정 없음.
- Octave 없음. MATLAB 보조 wrapper의 4·5단계만 실행했다.

일반적인 다른 환경에서는 프로젝트 의존성과 pytest가 있는 Python을 사용한다. 다음은 실제 WSL 경로를 사용한 예다. 다른 기계에서는 `R13_TARGET`과 `R13_OUTPUTS`만 해당 경로로 바꾼다.

```bash
export PATH=/home/yonghoon71/ddvenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PYTHONPATH=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r2-pydeps
export PYTHONDONTWRITEBYTECODE=1
R13_TARGET=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r13-target-wsl/bms-balancing
R13_OUTPUTS=/mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs
```

## 1. 행별 receipt의 일반 기능 검사

```bash
python -B "$R13_OUTPUTS/r13_receipt_identity_checks.py" "$R13_TARGET"
```

양성: matrix/profile 재정렬은 차이 없음, 첫 행 target/ref 입력 차이는 감지.
남은 문제: 양쪽 reference 누락은 `(문제[], 대조불가[])`; 문자열 reference의 schema 검사 비대칭; 빈 audit 객체.
보관 결과 `r13_receipt_identity_results.json`은 이 출력에 대상/환경 설명을 더한 wrapper다.

## 2. 과학 모집단·타입·shape writer 검사

```bash
python -B "$R13_OUTPUTS/r13_roster_schema_checks.py" \
  --target "$R13_TARGET" --out "$R13_OUTPUTS/r13_roster_repeat"
```

확인할 case:

- `control_profile_complete`, `control_matrix_complete`, `control_degeneracy`: 정상 대조군.
- `profile_wrong_grid`: 21개지만 잘못된 γ 집합도 rc0/promotion true.
- `matrix_self_declared_one_row_authority`, `matrix_wrong_member`: 독립 authority/member 미검증.
- `degeneracy_boolean_vs_numeric_baseline`: baseline 1.0, candidate true가 같다고 처리됨.
- `fresh_shape_producer`: 실제 writer에 유한 합성 측정을 전달한 결과가 profile로 오분류되어 rc2.

저장 결과는 `r13_roster_schema_results/`다. 같은 잘못된 데이터가 양쪽에 있는 사례는 candidate 독립 유효성 검사의 실패를 보여 주며, 정상 baseline과 다른 행 집합을 숨겼다는 증거는 아니다. partial 사례는 기존 신고 항목과 겹치므로 새 발견 수에 더하지 않았다.

## 3. 실제 CLI의 candidate schema·종료 계약 검사

```bash
python -B "$R13_OUTPUTS/r13_cli_contract_checks.py" \
  --target "$R13_TARGET" \
  --fixtures "$R13_OUTPUTS/r13_roster_repeat" \
  --out "$R13_OUTPUTS/r13_cli_repeat"
```

최종 저장 결과는 **`r13_cli_contract_results_v3/`**다. 과거 v1/v2는 최종 package에서 제외했다.

| case | 현재 코드에서 재현되는 값 |
|---|---|
| candidate_reference_receipt_empty | rc2, promotion false |
| baseline_reference_receipt_empty | rc4, promotion false |
| both_reference_receipts_empty | rc0, promotion true — 문제 |
| reference_receipt_string_missing_locator | rc0, promotion true — 문제 |
| complete_audit_control | rc0, promotion true — 정상 대조군 |
| candidate_audit_empty_object | candidate 감사만 `{}`여도 rc0, promotion true — 문제 |
| bom_json_schema_only | rc1, PROMOTION 없음, JSONDecodeError — 문제 |
| schema_only_missing_env_fields | rc0, schema/env blocker 0; promotion false — schema 진단 누락 |

`candidate_audit_empty_object/control.new/`에 변경 전 양성 candidate의 정확한 bytes/sidecar를 보존했다. `old/`는 그대로이고, 양성 출력은 `control.stdout.txt`/`control.stderr.txt`, 변경 후 출력은 `stdout.txt`/`stderr.txt`다. 결과의 `complete_audit_control.command`는 그 당시 사용한 `new/` 경로를 기록하므로, 현재의 변경 후 `new/`와 혼동하지 않는다.

## 4. 보관 증거의 읽기 전용 감사

```bash
python -B "$R13_OUTPUTS/r13_passive_evidence_audit.py" --target "$R13_TARGET"
```

보관 JSON/rc를 읽고 manifest 해시만 계산한다. target/보관 Python 코드는 import하거나 실행하지 않는다. `r13_passive_evidence_results.json`이 실제 stdout이다. 기록의 `closed:true`와 남은 상태를 함께 읽어야 하며, hash 일치가 과거 과학/보안 결론의 옳음을 증명하지 않는다.

## 5. 선택 회귀와 일반 보조 검사

```bash
cd "$R13_TARGET"
python -m pytest tests/ -q -p no:cacheprovider \
  -k 'not d10_12 and not d10_13 and not d10_14 and not e11_09 and not e11_10 and not e11_17 and not e11_18 and not d8_07 and not d9_08 and not d7_05'
bash matlab/tests/run_all.sh
python scripts/check_u14.py --new out --schema-only
```

이번 측정은 226 passed/10 deselected, MATLAB 보조 단계4·5 PASS(1~3 미실행), 현행 out rc2다. 236개 전체 회귀나 과거 보안 재생을 완주했다는 뜻이 아니다. 보조 wrapper가 출력한 “전부 통과”도 이 환경에서 실제로 실행한 두 단계만 의미한다.

## 포함 자료와 무결성

- 주 보고서, 이 README, `R13_VALIDATION_RESULTS.json`.
- 기능 검사 3개, 읽기 전용 감사 1개, 분담 근거 보고서 3개.
- 과학 roster의 합성 입력/결과, 최종 CLI 입력/결과, receipt/보관 감사 JSON.
- `R13_PACKAGE_MANIFEST.json`: package payload 파일들의 SHA-256. manifest 자체와 zip 자체는 자기 목록에 포함하지 않는다.

합성 input digest·run ID·sidecar는 검사 fixture다. 실제 실행 출처/과학 결론으로 재사용하지 않는다. 대상 코드 수정·commit·push는 하지 않았다.
