# ULPR 재개 식별자 정수 파싱 — 구현·검토 증거 (2026-10-24 KST)

사용자 “계속 진행”·“다 비준이야” 이후, 기존에 남긴 fractional RESUME k 문제를 기존 등록의 정수 경계 요구 안에서 수정했다. 새로운 과학값이나 물리 실행 결과를 정한 작업은 아니다. [검토 요청서](../codex_dem_unloading_resume_integer_request_20261024.md), [상세 인계 NOTE](NOTE.md), [수정 diff](source/candidate.diff)를 함께 읽는다.

기준 pin은 `8347d32ea678c0174bd77d4c79cfbd7b0591e4a3`이다. 최종 reader SHA-256은 `7a395a549e8ad3eae820a9e575f094219ca7d47a4b9a07c5bc27623d7018af4b`, 6파일 diff SHA-256은 `ccd610c9e7c9b3d1443edba03324a8c0fdf0bed0330f908ca7844586b293efd0`이다. [source_manifest.json](source_manifest.json)은 6파일의 기준·현재 SHA와 바이트 수를 기록한다. 자기 커밋 번호를 예측하지 않으며 최종 반입 pin은 root가 따로 고정한다.

| 구분 | 실제 최종 결과 | 원자료 |
| --- | --- | --- |
| 작성자 13개 kit 명령 | 모두 rc 0·FAIL 0; reader 304(기존 214 + R39 90), gates 202 | [summary.json](author/final-v5-suite/summary.json), 같은 디렉터리의 13개 로그 |
| 봉인·덱 정합 | 봉인 76파일·24규칙, 생산 덱 64개 생성 결과와 일치 | 위 seal/check 및 deck/check 로그 |
| 작성자 변이 | 11개 모두 해당 R39 단언으로 검출, 예외 0 | [results.json](author/mutations-v5/results.json), 개별 로그·mutant-sources.zip |
| 실제 arm CLI | 정상 2개 OK·같은 rho; 잘못된 표지 8개 승인 없음·UNIDENTIFIED·null; 입력 CSV 무변경 | [최종](author/cli-v5/results.json), [기준판](author/cli-before/results.json), 각각 raw-fixtures.zip |
| 생산 덱 모의 실행 + 실제 CLI | k=0/1/2/3 모두 RM_STOP·OK·같은 rho; k=0/1 행 전체 동등성은 주장하지 않음 | [deck_probe.json](author/deck-probe-v5/deck_probe.json), raw-fixtures.zip |
| 독립 직접 공격 | 150/150 PASS; reader 별도 304/304; manifest 일치 | [review.md](independent/ulpr/final-v5/review.md), [result.json](independent/ulpr/final-v5/result.json) |
| 독립 변이 | 별도 2개: `_i` 복귀 22개, 사건 CSV 구조 guard 제거 3개 R39 단언 실패; 예외 0 | [result.json](independent/ulpr/independent-mutations-v5/result.json), 개별 로그 |
| 독립 원문 NOTE 대조 | 원문 구체적 주장 41/41 확인 | [note-review.md](independent/ulpr/note-review.md), [JSON](independent/ulpr/note-review.json) |
| 저장소 전체 gate | **PENDING** — root의 통합된 깨끗한 후보에서 실제 수행 필요 | [full_gate_receipt.json](full_gate_receipt.json) |

13개 명령·304개 reader 확인·150개 독립 공격·작성자 변이 11개·독립 변이 2개는 서로 다른 집계다. 합쳐서 독립 시험 수나 과학적 완전성으로 표시하지 않는다. 내부 독립 검토는 외부 Codex 세션 판정문을 새로 만든 기록이 아니다.

원래 결함은 fractional k를 반올림해 재개를 승인하고 fixture의 옛 행 5개를 제외한 것이다. 경계의 정수성만 강화했다. shared `_i`/`_csv`, 생산 덱, history, params, 물리 기준은 그대로이며, 사건 CSV 구조 오류에서는 재개 승인만 막는다. 시험 먼저 실패시킨 로그와 과거판은 author에 보존했다. 의존 파일이 빠졌던 초기 export 실패는 기능 red/최종 통과로 세지 않는다. scratch의 빈 Git 메타데이터는 main의 clean 상태 증거가 아니다.

원본 NOTE/독립 보고서/원본 artifact manifest는 [history/reports-original.zip](history/reports-original.zip)에 원래 상대경로로 보존했다. [archive-provenance.json](archive-provenance.json)은 복사·ZIP member의 원본 경로, SHA, 바이트 수와 live NOTE의 링크 정규화를 명시한다. 역사적 실행 로그의 절대경로는 고치지 않았다. 현재 재현은 아래 명령을 쓴다. 독립 scope/NOTE 검사 도구의 원본은 당시 scratch 배치에 결합한 역사 자료이며 다른 배치에서 그대로 실행한다고 주장하지 않는다.

저장소 루트에서 `ULPR_REPO`를 현재 checkout의 절대경로, `ULPR_OUT`을 새 scratch 경로로 정한다. Python 3.11.17에서 검증했으며 runner는 해당 환경이 허용하는 TMPDIR을 사용해야 한다.

```bash
ULPR_TOOLS="$ULPR_REPO/docs/reviews/ulpr_resume_integer_evidence_20261024/author"
python3 "$ULPR_TOOLS/run_suite.py" "$ULPR_REPO/docs/data/ps45_unload_20261009" "$ULPR_OUT/suite"
python3 "$ULPR_TOOLS/deck_probe.py" --repo "$ULPR_REPO" --out "$ULPR_OUT/decks"
python3 "$ULPR_TOOLS/probe_cli.py" --repo "$ULPR_REPO" --fixtures "$ULPR_OUT/decks" --out "$ULPR_OUT/cli"
python3 "$ULPR_TOOLS/mutate_resume.py" --repo "$ULPR_REPO" --out "$ULPR_OUT/mutations"
sha256sum -c docs/reviews/ulpr_resume_integer_evidence_20261024/MANIFEST.sha256
```

독립 도구의 원본 절대경로는 보존하고 [portable 사본](independent/ulpr/portable/)을 따로 추가했다. [provenance.json](independent/ulpr/portable/provenance.json)에 원본/사본 SHA·경로 변경·격리된 `--help` rc 0을 기록했다. 이 이동성 확인은 원래 150개 공격·2개 변이를 다시 실행한 결과로 세지 않는다. attack의 `--repo`는 기준 pin을 읽을 Git 저장소이고 `--work`는 검증할 후보/export다. mutations의 `--repo`는 검증할 후보/export다. 완전한 현재 checkout을 쓰면 아래처럼 같은 경로를 지정할 수 있다.

```bash
ULPR_AUDIT="$ULPR_REPO/docs/reviews/ulpr_resume_integer_evidence_20261024/independent/ulpr/portable"
python3 -I "$ULPR_AUDIT/attack_ulpr_resume.py" --repo "$ULPR_REPO" --work "$ULPR_REPO" --out "$ULPR_OUT/independent-attacks" --reader-sha 7a395a549e8ad3eae820a9e575f094219ca7d47a4b9a07c5bc27623d7018af4b
python3 -I "$ULPR_AUDIT/independent_mutations.py" --repo "$ULPR_REPO" --out "$ULPR_OUT/independent-mutations"
```

[package_manifest.json](package_manifest.json)은 repo 상대경로의 파일별 SHA·바이트 수를 담고 자기 자신과 MANIFEST.sha256은 제외한다. MANIFEST.sha256은 package_manifest.json까지 포함하며 자기 자신은 제외한다. root에게 전달한 외부 deliverables-filelist.json/tsv는 모든 반입 파일을 덮는다. 전체 work snapshot은 반입하지 않는다. 실물 실행·설치 바이너리·외부 GO·일반 숫자 필드 전체의 강화·모든 악성 구문에 대한 전칭 보장은 이 패키지 범위 밖이다.
