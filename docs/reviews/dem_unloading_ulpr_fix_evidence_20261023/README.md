# ULPR 수정·재현 증거 — 2026-10-23

ULPR-01–04의 판독기 수정과 내부 독립 공격 검토를 기록한다. 실제 LIGGGHTS 실행이나 외부 반박 세션 GO의 증거가 아니다. 최종 요청서는 `docs/reviews/codex_dem_unloading_ulpr_recheck_request_20261023.md`다.

## 판과 증거의 구분

| 위치 | 뜻 |
|---|---|
| `baseline/` | 소스 기준판에서 13개 키트 명령 rc0. reader 182, gates 41. 이미 알려진 반례를 막는다는 증거는 아니다. |
| `tests_first/` | 수정 전 구현에 새 시험을 넣은 실패 로그. 중간판별 시험 수가 다르므로 최종 214/202와 합산하지 않는다. `resume-tail-scope-clean-fixtures.log`만 해당 후속 수정판의 통과 로그다. |
| `final/` | 통합·재봉인 뒤 13개 명령 모두 rc0. reader 214, gates 202, lib 24, S3 16, observers 21, seal 자체시험 12, 덱 생성기 291, 이력 생성기 172, 이력 판독기 56, runner 38. |
| `mutations/resume-six/` | 최종 통합 reader의 여섯 기존 사유/조건 줄 변이. 앞 세 개는 거부 사유 줄만, 뒤 세 개는 조건/가드를 제거한다. 각 지정된 R38 단언에서 실패하며 예외나 무관한 실패가 없다. |
| `dump-final/` | 최종 덤프 후속 변이 10개 모두 예상 시험으로 검출, 독립 원형 복원 probe 12개 기대 결과. 구현자가 수행한 재현이며 별도 독립 검토로 세지 않는다. |
| `independent/REPORT.md` | 첫 독립 검토. 정상 재개 오거부 및 덤프 구조·시점 문제를 찾았다. 당시 코드 사본과 출력은 보존한다. |
| `independent/RECHECK-v2.md` | 수정 후 독립 재검토. 실제 arm/select/report/gate 소비 경로, 정상 재개, 구조·시점 및 추가 변이 4개. 코드 범위에서 새 차단 결함 없음. |
| `independent/PACKAGE-REVIEW.md` | 문서·시험 수·봉인 대조 및 첫 세 승인 조건을 실제 제거한 별도 독립 변이. 최신 reader에서 세 변이 모두 관련 단언으로 검출. 비수치 변이는 다른 가드가 거부를 유지한다. 초기 도구의 R28 실패 분류 부족도 원자료로 보존한다. |
| `probes/` | R10 fixture 실제 덱 순서 정정, 중단 재개·주값 보존 탐침. 합성 자료이며 실험 측정이 아니다. |
| `scope-verification.json` | 기준판 대비 키트 94개 파일 대조. 변경 6개, 생산 덱 64개·이력 폴더 16개·params·봉인 32개·지정 공유 기록/게이트 불변. |

`final/summary.json`의 `working_files_sha256`은 실행한 작업 파일의 실제 지문이다. `baseline_checkout_kit_git_tree`는 기준 HEAD의 내용 식별자이며 수정된 키트의 지문으로 쓰지 않는다. 자체시험 개수는 출력의 `✓` 줄 수로 셌다. 키트 봉인은 76개 파일·활성 규칙 24개·폐기 0개, 덱 재생성 대조 64개다. 이력 봉인은 15개 파일을 포함한다(폴더 전체 추적 파일 16개와 구분).

## 재현

Python 3.11, 필요한 저장소 의존성, BLAS 스레드 1로 실행한다. 출력은 checkout 밖 새 폴더를 사용한다. `REPO`는 저장소, `E`는 이 증거 폴더, `OUT`은 새 결과 폴더의 절대 경로다.

```bash
python3 -I "$E/tools/run_suite.py" "$REPO/docs/data/ps45_unload_20261009" "$OUT/suite"
python3 -I "$E/tools/mutation_check.py" --kit "$REPO/docs/data/ps45_unload_20261009" --out "$OUT/resume-six"
python3 -I "$E/independent/deck_probe.py" --repo "$REPO" --out "$OUT/deck-probe"
python3 -I "$E/independent/restore_probe.py" --repo "$REPO" --out "$OUT/restore-probe"
python3 -I "$E/independent/v2/downstream_probe.py" --repo "$REPO" --out "$OUT/downstream"
python3 -I "$E/independent/v2/focused_mutations.py" --repo "$REPO" --out "$OUT/focused-mutations"
```

독립 증거는 보고서·코드/도구·diff·JSON·로그를 보존한다. 도구가 다시 만드는 덤프/임시 restart/화면 파일은 중복 보관하지 않는다. 보고서의 scratch 절대 경로는 당시 실행 위치이며 재현에는 위 경로 인자를 사용한다. 구판 변이 스크립트는 그 판의 정확한 코드 문자열을 요구할 수 있다. 구판 결과를 최종판 재실행으로 읽지 않는다.

## 남는 범위

- 재개 꼬리의 소속이 불명확하면 경계 앞에서 완료한 유효 주 값만 보존한다. 전체 union이 없으므로 `rank_eligible` 단독으로 순위를 인증하지 않는다.
- 기존 RESUME 소수 k(`3.49`)의 정수 반올림 파싱은 남는다. 이 관찰은 승인 집합에 관한 것으로 잘못된 최종 물리값까지 승인된다는 입증은 아니다.
- 필수 G2c 열 결손은 UNCONFIRMED지만 구조 파손·다른 시점은 VALUE_MISMATCH다. 완료되어 바뀌지 않는 직교 덤프에 한정하며 물리 BOX/PBC 값이나 동시 갱신의 원자성을 인증하지 않는다.
- 웹앱에서 이 키트 판독기를 쓰는 화면은 검색되지 않았다(J20-l). 공용 웹앱·봉인 32 파일을 수정하지 않았다.
- 클라우드 환경 최초 전체 게이트는 venv의 symlink interpreter를 realpath로 실행할 때 의존성이 빠져 실패했다. Python/Python3/Python3.11을 venv 내 실제 실행 파일로 설치해 수정했다. 이 환경 실패를 성공 결과로 합산하지 않는다. 전체 저장소 최종 게이트 결과는 별도 실행 로그로 전달한다.
