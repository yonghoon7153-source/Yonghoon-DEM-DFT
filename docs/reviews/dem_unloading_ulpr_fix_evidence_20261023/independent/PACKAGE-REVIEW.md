# ULPR package independent review — 2026-10-23

현재 요청서·등록·정식 봉인·원자료의 대조 범위에서 남은 차단 결함은 발견하지 못했다. 아래 P3 표현 문제는 검토 중 수정되었다. 이 판정은 **발송 전 초안의 문서·증거 정합**에 한정한다. 저장소 fullgate 확정 receipt와 최종 commit/ZIP pin 검증은 아직 완료하지 않았으며, 발송·외부 GO·물리 실행을 승인하는 판정이 아니다.

## 검토 입력과 고정

- 입력은 제공된 `ulpr-package-review.diff`, 실제 새 요청서, 증거 README, 등록·코드·시험·재현 도구와 그들이 가리키는 raw 로그/JSON/해시다. 구현자 별도 보고서/노트는 근거로 사용하지 않았다. `../dump-final/SUMMARY.md` 대신 원 JSON/로그를 대조했다.
- 기준 Git commit은 `7799a2ff64ba462b42ce05edd3e63b7c2854d557`이다. 생산 코드 지문은 이전 독립 v2와 같다: reader `34b46ebcf4530989917493f20d2d953043209e36d89e6b8282a2d629050a078d`, gates `c8d45a9cf75f0806e612d810942d23adea4b40feaa5f31f7d279eb8386358de6`.
- 이번 검토 자료는 이 보고서 옆 `package/`에 있다. `input-package.diff`는 최초 전달 입력, `snapshot/`은 표현 수정 후 읽은 문서/봉인 사본, `snapshot-sha256.json`은 각 사본의 지문이다. 이후 추가되는 fullgate receipt·최종 pin·요청서 변경까지 이 snapshot이 인증하지는 않는다.
- 추적 파일 수정·commit·push·전체 저장소 gate·외부 LIGGGHTS/GPU 실행은 수행하지 않았다. 관련 키트 seal 검사 및 아래 독립 3변이만 추가 실행했다. 기존 `REPORT.md`, `RECHECK-v2.md`와 v1/v2 원자료를 덮어쓰지 않았다.

## 발견 및 처리

**P3, 수정 확인 — 원 6변이를 모두 “가드 제거”로 기술한 표현이 실제 변이와 다름.**

최초 입력의 요청서 §2 ULPR-02/§3 변이 행과 증거 README는 여섯 기존 가드를 제거했다고 적었다. 그러나 `docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/tools/mutation_check.py:13–15`의 앞 세 변이는 `pr.append(...)`만 `pass`로 바꾸며 승인 거부 분기는 유지했다. 실제 원 로그도 허용 집합 `[]`가 유지되고 오류 사유만 사라진다. 이 증거만으로 첫 세 **승인 조건** 제거를 검출했다고 말할 수 없다. 영향은 검증 주장의 범위이며 생산 코드의 새 오승인을 뜻하지 않는다.

재현은 도구의 `MUTATIONS` 세 항목을 reader의 `_resume_auth` 조건과 대조하고 `mutations/resume-six/*.log`의 R38 실패 detail을 확인하면 된다. 보존한 입력 diff에는 원 표현이 남아 있다. 검토 후 요청서 28/65행, 증거 README 12행, 등록 956행은 앞 세 사유 줄과 뒤 세 조건/가드를 구분했으며, 도구 2행도 `six diagnostic/guard mutations`로 수정되었다. 원 여섯 결과를 교체하지 않았다.

## 독립 추가 승인 조건 변이

`package/authorization_mutations.py --repo REPO --out OUT`은 현재 reader를 메모리/별도 파일로 변이하고 실제 reader 전체 selftest를 실행한다. 저장소 소스를 수정하지 않는다. 결과는 `package/authorization-mutations-final/results.json`, 각 `.log`, 실제 mutant `.py`에 보존했다. JSON에 입력 코드·도구·mutant SHA256과 Python 판을 기록했다.

| 실제 제거한 조건 | 결과 | 의미 |
|---|---|---|
| `elif e['step'] not in rf:` → `elif False:` | rc1, R38 1 실패 | 목록 밖 `(3,3350001)`가 승인 집합에 생긴 행동 변화를 검출 |
| `if e['k'] is None or e['step'] is None:` → `if False:` | rc1, R38 2 실패 | 숫자 전용 사유가 상태 불일치/목록 밖 사유로 바뀜을 검출. 다른 방어가 승인을 계속 막으므로 잘못 승인된다고 주장하지 않음 |
| 상태 `ul_rstep/ul_k` 일치 → 무조건 참 | rc1, R38 1 + 기존 R28 2 실패 | R38의 상태 불일치 승인, R28의 상태 k 불일치/상태 파일 없음 처리 실패를 함께 검출 |

세 변이 모두 예외 없이 해당 조건의 행동/사유 단언에서 실패했다. 상태 변이의 기존 R28 두 실패는 같은 상태 검사를 직접 다루며 무관한 실패가 아니다. 첫 실행기의 R38-only 분류는 이를 `unexpected`로 표시했으므로 그 원 실행과 실행기 사본을 `package/authorization-mutations/`에 그대로 보존했다. 최종 실행기는 **그 두 R28 문구만** 관련 기존 실패로 따로 분류하며 재실행했다. 최초·최종 mutant SHA와 실패 내용은 같다. 이 3변이는 구현자 6변이 및 독립 v2 4변이와 별도 증거다.

## 숫자·원자료·봉인 대조

`package/audit.py --repo REPO --out OUT`으로 다시 대조할 수 있다. 이번 결과는 `package/final-audit/audit.json`이다.

- 최종 summary의 실제 작업 파일 SHA가 현재 키트와 모두 같다. 13개 각 원 로그의 통과/실패 줄·rc가 summary와 일치하며 모두 rc0이다. reader 214, gates 202; lib 24, S3 16, observers 21, seal 자체시험 12, 덱 자체시험 291, 이력 생성기 172, 이력 reader 56, runner 38이다.
- 기준판 13개 로그도 각각 summary와 일치한다. 기준 reader 182/gates 41을 최종 수와 섞지 않았다.
- test-first 원 로그의 문서 수는 일치한다: resume 191통과/5실패, 초기 dump gates 40/17·reader 177/6, 정상재개 보정 전 reader 200/1, tail-scope 204/1, BOX/G2c 보강 전 gates 106/96·reader 186/5. clean-fixture 205/0 로그는 실패 증거로 세지 않는다.
- 기준 94개 파일 해시를 기준 Git blob과 대조했다. 정확히 README/SHA256SUMS/active_rules/seal_kit/reader/gates 6개만 변경됐다. 생성 덱 64개·history 폴더 16개·params와 별도 봉인 대상 32개는 기준/현재가 같다.
- 정식 `SHA256SUMS` 76개와 history 봉인 15개 모두 실제 파일과 일치한다. history 폴더 16개와 봉인 15개를 구분한 설명이 맞다. 독립 `seal_kit.py --check`는 rc0, 76파일·활성24규칙·폐기0·증인 실재 참이다. 원 출력은 `package/seal-check.log`다.
- `dump-final/MANIFEST.sha256`의 299개 지문이 모두 일치한다. 최종 dump 변이 10개와 baseline 두 로그에서 JSON의 실패 목록이 raw 로그와 같다. 변이 실패 수는 39/12/6/12/72/21/2/1/1/1이며 예외/무관 실패를 찾지 못했다. 12개 restore probe의 JSON은 정상 RESTORED/0, 열 결손 UNCONFIRMED/2, 대상 구조·시점 위반 VALUE_MISMATCH/2와 일치한다.
- 구현자 resume-six의 6개 raw 로그와 JSON 실패 목록이 모두 같다. 원 mutant 파일은 이 묶음에 별도 보존되지 않았으나 보존 도구+최종 reader로 재구성한 SHA는 기록된 여섯 mutant SHA와 모두 같다.
- R10 전후 windows/steps는 실제 바이트가 같고 events만 다르다. 고친 fixture는 수정 전·후 reader에서 모두 `rho=0.2026077873428664`, 주 값 OK, 옛 행 두 개 제거라는 원 JSON 기록과 일치한다. 이전 독립 v2가 검증한 생성 덱 정상재개와 혼동하지 않았다.
- 독립 v2 코드 사본 두 개는 현재 코드와 바이트가 같다. 묶음의 deck/restore/edge/downstream/focused 도구도 실제 검토에서 사용한 portable 원본과 바이트가 같다. 당시 scratch 절대 경로는 실행 provenance이며 재현 인자는 `--repo/--out`이다.

## 문서 범위와 남는 확인

등록 §14-12와 키트 rule/seal는 G2c 필수 열 결손을 NOT_COMPUTED→UNCONFIRMED로 정정하고 구조/시점/값 위반과 기술 실패를 구분한다. 옛 재확인2 §5 Q3의 열 결손 질문만 대체한다는 문구는 문법 원자료 재판독 Q3을 취소하지 않는다. 불명확 꼬리에서 완료한 주 값 보존과 전체 union/비단조/최종 분리·표면 미확인의 구분은 이전 독립 downstream 결과와 맞는다. `rank_eligible`만으로 쌍 순위를 인증하지 않는 한정도 맞다.

요청서는 임의 파손 파일 전체, 동시 쓰기 원자성, 물리 BOX/PBC 동일성, RESUME 정수 문법 전체, 실제 물리 실행을 인증한다고 주장하지 않는다. 남은 `k=3.49` 반올림은 승인 집합 관찰이며 잘못된 최종 물리값 승인까지 입증한 것이 아니라는 한정이 정확하다. 제한된 반례/변이/로그 대조에서 신규 문제가 없다는 것과 모든 입력에서 결함이 없다는 것은 다르다.

검토 당시 `full_gate_receipt.json`은 PENDING이다. 요청서는 PASS 전에 전달 불가라고 명시하므로 현재 초안을 fullgate 완료로 오해하게 하지는 않는다. 다만 **최종 receipt·원 fullgate 로그, 최종 commit의 Git blob, ZIP 외부 PIN.txt/MANIFEST.sha256 대조는 아직 미검증**이다. 후속 문서/도구 추가분과 실제 최종 발송물을 이 보고서의 고정 snapshot과 다시 대조해야 한다. 전체 저장소 gate를 중복 실행하지 않았다.

독립 재현 명령 예시(현재 파일들이 보존된 checkout/출력 경로를 사용):

```bash
python -I "$REVIEW/package/audit.py" --repo "$REPO" --out "$OUT/audit"
python -I "$REVIEW/package/authorization_mutations.py" --repo "$REPO" --out "$OUT/authorization-mutations"
python -I "$REPO/docs/data/ps45_unload_20261009/seal_kit.py" --check
```

`REVIEW`는 이 보고서가 있는 디렉터리, `OUT`은 새 scratch 출력이다. 기존 증거를 덮어쓰지 않는다. 코드 판정과 직접 production entrypoint의 상세 범위는 이전 `RECHECK-v2.md` 및 그 원자료에 있다.


반입 메모: 검토 당시 문서 사본은 상대 경로의 기준을 보존한 `package/reviewed-snapshot.zip` 안 `snapshot/`에 보관한다. ZIP의 `PACKAGE-REVIEW.original.md`는 이 보고서의 원본이며, 반입판은 dump-final 참조에 `../`를 붙였다. 원문 바이트는 ZIP 대조로 확인했다.
