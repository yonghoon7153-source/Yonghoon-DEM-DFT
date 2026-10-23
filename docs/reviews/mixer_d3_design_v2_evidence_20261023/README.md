# D3 v2 설계 · 독립 사전 검토 반입 증거 (2026-10-23)

최종 통합 상태는 [전체 게이트 영수증](full_gate_receipt.json)과 `final-gate/` 로그가 정본이다. 아래 및 원 검토문·쪽지의 작성 당시 대기 표현은 이력으로 보존한다. 깨끗한 후보 커밋에서 축소 없는 전체 게이트를 실행했고, 이후 커밋은 이 영수증·로그와 새 상태 쪽지만 기록한다. 외부 GO·비준·발송·실제 기계 실행 상태는 승격하지 않는다.

현재 문서 = `docs/reviews/mixer_d3_se_flowability_anchor_design_v2_20261023.md`, 요청서 = `docs/reviews/codex_mixer_d3_design_v2_request_20261023.md`. 작업 가지는 `codex/mixer-d3-design`, 예정 커밋은 `<<sha:Revise mixer D3>>` (`Revise mixer D3 finite-grid design proposal`)이다. 이 증거를 준비한 것만으로 가지 생성·커밋·push·핀 ZIP 제작이 끝났다고 주장하지 않는다.

**현재 지위:** 독립 사전 리뷰의 P3 네 건은 수정판에서 문서 수준 해소했다. 예약 시드의 정본 ID·순서·역할 일치도 확인했다. 전체 `bash scripts/check_all.sh`는 최종 반입 묶음에서 대기이며, 외부 발송 승인·D3 ① 외부 GO·V2-Q1 등 새 제안 비준·실제 manifest 검증·실측/DEM 실행은 완료하지 않았다.

## 보존한 판과 검사 범위

| 자리 | 원문·검사 | 의미 |
|---|---|---|
| `original-draft/` | 최초 설계/요청서·당시 README·원 MANIFEST | 원검토판 그대로. 당시 “독립 검토 전” 문장은 이력이다. 원 manifest 멤버의 현재 위치는 `ORIGINAL_MANIFEST_MAP.json`으로 연결한다. |
| `d3_v2_counterexamples.py`, `counterexamples.json` | 작성자 반례·산술 29/29, 반복 출력 동일 | 설계의 보장 한계와 산술 관계. 생산 판독기·통계·기하 구현의 회귀가 아니다. |
| `baseline_numbers.txt`, `SOURCE_SHA256SUMS` | 기존 10-21 스크립트 재실행, rc 0 | 소스 핀/지문에 묶인 생성기 함수의 숫자 대조다. 시뮬레이션이 아니다. |
| `harness_first_output.json` | 초기 작성자 하니스 25/26 | float 비율 `==3`의 하니스 오류를 보존했다. 이후 `isclose`로 수정하고 검사를 보강했다. 생산 결함의 red→green 증거로 세지 않는다. |
| `reviewed-revision1/` | P3 네 건 수정판 두 문서·diff·지문·provenance | 독립 재확인이 실제로 읽은 판이다. 최상위 반입 문서에는 이후 검토 상태 요약만 추가했다. |
| `independent/REVIEW.md` 및 도구/JSON | 최초 독립 사전 공격 리뷰, 25/25 | 작성자 코드/출력을 보지 않고 수행. 새 P1/P2 발견 없음, P3 네 건. 범위는 보고서에 명시했다. |
| `independent/RECHECK-v2.md`, `recheck-v2-evidence/` | P3 네 건 문서 수준 해소, 의미 재공격 7/7(81상태 조합) | 실제 접근 통제·통계 판독기·manifest 검사의 구현 인증이 아니다. |
| `independent/seed-confirmation/` | 원문 ID·순서·D1/D12 역할 5/5 대조 | 실제 C0/C1/C2 manifest의 미사용이나 교집합 검사를 확인한 것이 아니다. |

독립 재확인 보고서의 “숫자 출처 미확인”은 당시 제한된 입력 범위다. 이를 삭제하지 않고 `docs/reviews/mixer_d3_design_v2_evidence_20261023/independent/seed-confirmation/ADDENDUM-reserved-seeds.md`로 보충했다. 시드 부록도 새로운 비준이나 실행 허가가 아니다.

원장 JSON은 **새 협업 쪽지 `docs/collab/codex_to_claude/20261023-1258_mixer-d3-design.md` 안에만** 있다. 현 제안과 원초안 이력 블록을 구분했으며, MXD3 여덟 건은 open 등재 제안, MXD2-07은 상태 자동 변경 없음이다. 원초안 JSON의 바이트는 이력 블록(끝 LF 포함)에서 복원해 원 manifest와 대조했다. 공유 원장·CLAUDE·진행 기록은 이 묶음에서 수정하지 않는다.

## 재현 (리포 루트에서)

```bash
K=docs/reviews/mixer_d3_design_v2_evidence_20261023
python -I -B "$K/d3_v2_counterexamples.py" --repo .
python -I -B "$K/independent/independent_d3_review.py" --repo .
python -I -B "$K/independent/recheck-v2-evidence/recheck_probes.py"
python -I -B "$K/independent/seed-confirmation/check_seed_provenance.py" \
  --repo . --draft docs/reviews/mixer_d3_se_flowability_anchor_design_v2_20261023.md
python -I -B docs/reviews/codex_mixer_d3_design_request_evidence_20261021/d3_precheck_numbers.py
```

29/25/7/5는 서로 다른 검사 묶음의 결과다. 합해서 하나의 생산 테스트 수로 쓰지 않는다. 생성기/계약 소스가 바뀌면 원 소스 SHA의 출력을 새 판의 실행 결과로 재사용하지 말고 다시 실행한다. `PACKAGE_CHECKS.json`은 반입 경로에서 위 앞 네 도구가 실행되는지 확인한 기록이며 새 독립 검토 판정이 아니다.

## 지문·범위

`MANIFEST.sha256`은 이 증거 폴더의 최종 멤버를 봉인한다. `FINAL_DOCUMENTS.sha256`은 최상위 문서 두 개와 새 협업 쪽지를 결합한다. `PACKAGE_PROVENANCE.json`은 검토된 수정판과 상태 요약을 추가한 반입본의 지문을 구분한다. 이 파일들은 최종 Git 핀 ZIP의 PIN.txt/MANIFEST를 대신하지 않는다.

옛 지문 목록에는 당시 scratch 절대 경로가 남아 있다. 당시 입력의 출처 표지로 보존했으며 재현 명령은 위의 저장소 상대 경로를 사용한다. `independent/recheck-v2-evidence/MANIFEST.sha256`의 상대 경로 기준은 `independent/`이다. `original-draft/MANIFEST.sha256`은 분산 배치된 옛 멤버 목록이므로 `ORIGINAL_MANIFEST_MAP.json`으로 대조한다.

중복 `counterexamples_repeat.json`과 생성된 fixture 복사본은 반입하지 않았다. 실험·LIGGGHTS/GPU 실행·생산 덱 생성은 없다. 장비·G·벽·시료량·반복·밀도·측정자·탭·입도 입력은 미정이다. 최종 저장소 전체 게이트·핀·외부 발송·등록·단계별 실행 승인 전 HOLD를 유지한다.

## 경로 정규화 반입의 원본·현재 구분

현재 저장소 문서 참조 검사를 위해 누락 경로 토큰만 실제 저장소 상대 경로로 확장했다. 숫자·판정·설계·미비준·실행 한계는 바꾸지 않았다. 원문 안의 “그대로/변경하지 않음”과 입력 SHA·원 diff·검토 행 번호는 당시 검토판의 이력이다. 원 바이트는 `import-paths/original-package-docs.zip`에서 확인한다. 현재 파일과 혼동하지 않도록 각 원본/반입 SHA·토큰 치환·diff를 `import-paths/provenance.json`에 기록했다. 아래 live manifest만 경로 정규화본의 반입 manifest로 재계산했으며, 같은 이름의 원 manifest는 ZIP에 그대로 있다: `independent/MANIFEST.sha256`, `FINAL_DOCUMENTS.sha256`. 원 source/literature 지문과 수치 JSON·로그·도구는 변경하지 않았다.
