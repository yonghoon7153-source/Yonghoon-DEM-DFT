# ULPR 재개 식별자 정수 파싱 보완 — 2026-10-24 KST

이 파일은 원본 scratch NOTE의 링크·도구 디렉터리 설명만 저장소 배치에 맞춘 live 사본이다. 원문은 history/reports-original.zip의 ulpr/NOTE.md이며, 원본 바이트와 변환 내역은 archive-provenance.json에 보존했다. 아래의 독립 NOTE 판정은 그 원문에 대한 판정이다. 사용자 2026-10-24 KST “계속 진행”·“다 비준이야” 지시는 이번 좁은 오류 수정의 진행 권한이며, 실물 결과·외부 GO·추가 과학값을 공급한 기록이 아니다.

기준은 `8347d32ea678c0174bd77d4c79cfbd7b0591e4a3`의 ULPR이다. 등록 §14-11①/§14-12의 같은 정수 경계 요구를 구현하는 파서 오류 수정이며, 과학 기준의 개정이 아니다. 기준판은 `RESUME k=3.49`를 3으로 반올림해 상태 k=3인 재개를 승인했다. 작은 fixture에서는 옛 행 5개를 제외했고, 실제 `arm` CLI fixture에서도 잘못된 경계를 승인했다. 이 재현은 잘못된 승인 증거이며 실제 물리 실험값이 틀렸다는 증거는 아니다.

최종 수정은 RESUME k/step과 상태 ul_k/ul_rstep의 원문 정수값을 비교한다. ASCII decimal/scientific 정수값, 정상 생산자 표기와 CRLF/CR은 유지한다. 실제 소수, 비유한/넘침, 비ASCII 숫자·공백, 중복 상태 식별자, 잘못된 runner 표지, 정상 사건과 모호한 RESUME의 공존은 경계를 승인하지 않는다. 사건 CSV 구조 오류가 있으면 남은 행만으로 재개를 인증하지 않는다. Decimal 앞의 유한 수 검사와 4096자 한도는 잘못된 토큰의 비용을 제한한다. 공용 `_i`/`_csv`와 일반 관측의 숫자 규칙은 바꾸지 않았다.

변경 파일은 reader, kit README, seal_kit.py, active_rules.json, SHA256SUMS, 사전등록 문서의 6개다. [범위 원자료](author/scope.json)는 94개 kit 파일 중 5개만 바뀌고 생산 덱 64개·history 16개·params가 그대로임을 기록한다. 나머지 변경 1개는 kit 밖 사전등록 문서다. 봉인은 76개 파일·24개 활성 규칙이며 R39 증인을 추가했다. main checkout·Git refs·commit·push는 이 작업에서 수정하지 않았다.

고정 산출물은 [candidate.diff](source/candidate.diff), reader는 [work의 원본](../../data/ps45_unload_20261009/ul_reader.py)이다.

- diff SHA-256: `ccd610c9e7c9b3d1443edba03324a8c0fdf0bed0330f908ca7844586b293efd0`
- reader SHA-256: `7a395a549e8ad3eae820a9e575f094219ca7d47a4b9a07c5bc27623d7018af4b`

최종 v5의 [13개 명령 원자료](author/final-v5-suite/summary.json)는 모두 rc 0, 실패 0이다. 그 원자료의 94개 실제 작업 파일 해시는 시험 후 현재 파일과 전부 일치했다. 출력의 Git tree 빈 값/빈 dirty 배열은 Git 저장소가 아닌 export의 결과이며, main checkout이 깨끗하다는 증거로 사용하지 않는다. 기준 pin과 실제 바이트는 scope.json 및 working_files_sha256으로 식별한다.

| 명령 | 통과 확인 줄 |
| --- | ---: |
| ul_lib --selftest | 24 |
| ul_s3 --selftest | 16 |
| ul_observers --selftest | 21 |
| ul_gates --selftest | 202 |
| ul_reader --selftest | 304 |
| seal_kit --selftest / --check | 12 / 1 |
| make_unload_decks --selftest / --check | 291 / 1 |
| history make_history_decks --selftest / --check | 172 / 1 |
| history read_history --selftest | 56 |
| ul_runner_test --selftest | 38 |

R39 90개를 추가했다(기존 reader 214개 + 90개 = 304개). 최초 유효 red는 [test-first-final.log](author/test-first-final.log)의 R39 실패 44개이며, 2**53 정밀도 시험 추가 후 [test-first-r39.log](author/test-first-r39.log)는 21 PASS/46 FAIL이었다. 뒤따른 공백·개행·CSV 구조 반례도 수정 전에 각각 [4](author/test-first-state-space.log), [2](author/test-first-manifest-space.log), [9](author/test-first-line-separator.log), [3](author/test-first-event-separator.log)개의 해당 단언 실패를 보존했다. 초기 test-first.log/test-first-complete.log/test-first-ready.log 및 최초 final-suite에는 export 의존 파일 누락이 섞여 있으므로 red/최종 통과 증거로 세지 않는다. v1~v4와 final-suite-complete는 과거판 기록으로 남겨 최종 v5와 합산하지 않았다.

[최종 변이 11개](author/mutations-v5/results.json)는 전부 R39의 행동/사유 단언으로 검출되었고 예외는 없었다. 원문 대신 `_i` 사용 22개, Decimal 절단 12개, Unicode 숫자 허용 5개, 상태 마지막 정의 선택 2개, 잘못된 manifest 무시 7개, 모호 사건 무시 1개, 상태 공백 정규화 4개, manifest Unicode 접두공백 무시 2개, 상태/manifest splitlines 복원 6개/3개, CSV 구조 guard 제거 3개가 실패했다. 이 수는 변이별 단언 실패 수이며 독립 시험 사례 수로 더하지 않는다.

[실제 arm CLI 10개](author/cli-v5/results.json)는 정상/정수 decimal 2개가 OK·같은 rho를 유지하고, 잘못된 표지 8개가 승인 없음·UNIDENTIFIED·rho null이었다. 모든 사례에서 입력 CSV 바이트는 그대로다. [기준판 CLI 결과](author/cli-before/results.json)와 별도 비교할 수 있다. [생산 덱 모의 실행 + 실제 CLI](author/deck-probe-v5/deck_probe.json)는 k=0/1/2/3 정상 재개에서 모두 RM_STOP, OK, rho `0.20260778734286913`이었다. k=0/1의 행 전체는 중단 없는 fixture와 동일하지 않으므로 행 단위 완전 동등성은 주장하지 않는다.

독립 검토자의 [최종 보고서](independent/ulpr/final-v5/review.md)와 [원자료](independent/ulpr/final-v5/result.json)는 직접 공격 150/150, 독립 reader 304/304, manifest 일치를 기록한다. 검토 중 실제 발견된 manifest 앞 Unicode 공백, 상태/manifest Unicode 줄구분, 사건 CSV 구조 결손의 세 우회를 수정한 뒤 같은 고정 바이트로 PASS를 받았다. 독립 수치와 구현자 시험 수치는 서로 합산하지 않는다.

별도의 [독립 변이 2개](independent/ulpr/independent-mutations-v5/result.json)는 `_i` 복귀 68 PASS/22 FAIL, 사건 CSV 구조 guard 제거 87 PASS/3 FAIL이며, 모두 실제 R39 단언 실패이고 예외는 0이다. 구현자 변이 11개를 대체하거나 그 수에 더하지 않는다.

재현에는 완전한 기준 checkout에 candidate.diff를 적용한 경로 또는 검토 당시 work export를 `ULPR_REPO`로 지정하고, `ULPR_TOOLS`를 이 문서 옆 author 디렉터리로 지정한다. `ULPR_OUT`은 새 출력 디렉터리로 지정한다. Python 3.11.17 환경에서 실행했으며, runner 시험의 임시 출력 정책을 만족하는 TMPDIR이 필요하다. 이 환경의 activate.sh는 승인된 `/var/tmp/codex-nonrint-20261023`을 사용한다. 다른 환경은 그 환경에서 허용된 임시 디렉터리를 사용한다.

```bash
python3 "$ULPR_TOOLS/run_suite.py" "$ULPR_REPO/docs/data/ps45_unload_20261009" "$ULPR_OUT/suite"
python3 "$ULPR_TOOLS/deck_probe.py" --repo "$ULPR_REPO" --out "$ULPR_OUT/decks"
python3 "$ULPR_TOOLS/probe_cli.py" --repo "$ULPR_REPO" --fixtures "$ULPR_OUT/decks" --out "$ULPR_OUT/cli"
python3 "$ULPR_TOOLS/mutate_resume.py" --repo "$ULPR_REPO" --out "$ULPR_OUT/mutations"
```

범위 밖 일반 숫자 필드의 정수성 전체 강화, 모든 악성 파일 구문에 대한 전칭 보장, 실물 재개·설치 바이너리 검증, 외부 GO는 주장하지 않는다. 전체 저장소 gate와 main 통합·최종 발행은 root 담당으로 이 보고서의 완료 범위에 포함하지 않는다. 승인된 과학값·생산 덱·물리 런 결과를 추가하거나 바꾼 작업은 없다.
