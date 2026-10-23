# MXD2 생성기 v2 증거 (2026-10-23)

생산 수정 대상은 `scripts/make_mixer_deck.py` 한 파일이다. MXD2-02–06은 claimed_fixed 제안, MXD2-01은 HOLD/open, MXD2-07은 D3 v2 설계 검토다. FULL gate는 최종 반입 담당자가 `full_gate_receipt.json`에 확정해야 한다. 이 묶음은 외부 GO·실험·정책 v5·런 등록을 뜻하지 않는다.

## 원자료와 수

- `final_summary.json`: 최종 신원·검증 집합·한계. 작성자16변이, 독립v2 14변이를 구분한다.
- `author/tests_first/`, `author/logs/`: 최초145/154 및 독립 지적 뒤155/158 red, 최종158/158 green, 소비자 자체 시험·웹앱 페이지9/9 원 로그.
- `author/mutation_runner.py`, `mutation-results.json`: 16변이를 각각 의도한 검사로 검출. 밀도·meta상수·혼합쌍 생략의 3변이는 기준143개 시험에 생존한 원 로그도 보존했다.
- `independent/v1/`: 작성자 설명을 읽지 않은 검토자의 첫 보고·도구·입력patch·JSON·원 manifest. 10변이 중3생존, R1–R4를 기록한다.
- `independent/v2/`: 같은 독립 검토자의 최종 보고·도구·입력full/delta·JSON·원 manifest. 158/158, 14/14변이, 정상3상192덱/1728접촉쌍, 추가AM_P+SE8덱, 설명21거부/4양성, CLI32거부, v1/v2 192덱 바이트 동일.
- `author/auxiliary_archive/`: MXD2-01 HOLD와 정적 천장/언더플로 진단, 작성자가 재실행한 v1 프루브10변이 및 설명거부 기록adapter. 이 재실행은 독립 판정이 아니다.
- `ledger-update-proposals.json`: 공유 원장 담당자용 부분 갱신 제안. 원장 전체를 이 파일로 덮어쓰지 않는다.

독립 v1/v2 보고·도구·입력patch·결과·원 manifest는 복사할 때 바꾸지 않았다. raw JSON의 절대 경로는 실행 당시 scratch 경로이며, 보존한 대응 파일은 같은 상대 구조에 있다. mutant 소스는 용량/중복을 줄이기 위해 생략했으며 해당 도구가 입력 소스로부터 다시 생성한다. 변이별 전체 selftest 로그는 보존했다. 옛10-21 원24변이 스크립트를 입수·전부 재실행한 자료는 아니다.

`author/SUMMARY_V2.json`은 독립 v2 완료 전의 작성자 스냅샷이라 reviewer10·독립대기로 남아 있다. 이를 최신 판정으로 읽지 말고 `final_summary.json` 및 `independent/v2/REVIEW.md`를 사용한다. 최초 원자료를 소급해 고치지 않았다.

## 재현 (새 출력 폴더 사용)

Python3.11.17로 실행했다. 아래 `MXD_EVIDENCE`는 이 폴더의 절대 경로, `MXD_RUN`은 저장소 밖 새 폴더다. 셸 변수는 사용자가 실제 경로로 지정한다. 원 증거 폴더에서 새 로그를 쓰지 않는다.

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p "$MXD_RUN/base/scripts"
cp "$MXD_EVIDENCE/author/baseline/make_mixer_deck.py" "$MXD_RUN/base/scripts/"
cp "$MXD_EVIDENCE/author/baseline/additives.py" "$MXD_RUN/base/scripts/"
python -I "$MXD_EVIDENCE/independent/v2/reproduce.py" \
  --repo "$MXD_RUN/base" \
  --patch "$MXD_EVIDENCE/independent/v2/input_generator.patch" \
  --out "$MXD_RUN/review-v2"
python -I "$MXD_EVIDENCE/independent/v2/compare_prior.py" \
  --prior "$MXD_EVIDENCE/independent/v1/evidence/snapshot/scripts/make_mixer_deck.py" \
  --current "$MXD_RUN/review-v2/snapshot/scripts/make_mixer_deck.py" \
  --out "$MXD_RUN/prior-comparison.json"
```

프루브는 JSON 관찰 기록기다. rc0만 보지 말고 source hash·각 변이의 실패 검사·192덱·양성/음성 항목을 확인한다. 위 miniature base는 원 생성기와 그 공유 의존성의 보존 사본이며 전체 저장소 gate를 실행하는 환경이 아니다.

작성자16변이와 시험 먼저 단계는 복사본에서 재현한다.

```bash
cp -R "$MXD_EVIDENCE/author" "$MXD_RUN/author"
python -I "$MXD_RUN/author/tests_first/generator-tests-only.py" --selftest
# 예상 rc1, 145/154 PASS (9 FAIL)
python -I "$MXD_RUN/author/tests_first/generator-review-tests-only.py" --selftest
# 예상 rc1, 155/158 PASS (3 FAIL)
python -I "$MXD_RUN/author/scripts/make_mixer_deck.py" --selftest
# 예상 rc0, 158/158 PASS
python -I "$MXD_RUN/author/mutation_runner.py"
# 비변이 pass 뒤16개 변이 각각 예상 검사 실패를 단언한다.
```

`auxiliary_archive`의 원 도구는 당시 scratch의 `baseline/`, `scripts/`, `deliverables/` 배치와 실제 웹앱 경로를 전제로 한다. 그대로 단독 실행되는 portable 도구라고 주장하지 않는다. MXD2-01·정적 진단 JSON과 원 로그는 보존했으며, 재현하려면 위 baseline과 pin의 소비자 의존성·v17 문서를 새 scratch에 같은 구조로 준비해야 한다. 현재 생산 소비자 지원/정책 등록이 완료됐다는 근거로 사용할 수 없다.

## 해시와 최종 반입

각 `independent/v1`, `independent/v2`에서 `sha256sum -c MANIFEST.sha256`로 원 검토 신원을 확인한다. 이 폴더 루트의 `MANIFEST.sha256`은 원 증거 전체를 포함한다. FULL gate receipt·최종 로그를 추가한 뒤 반입 담당자가 루트 manifest를 재생성해야 한다. 독립 하위 원 manifest를 덮어쓰지 않는다.

전체 gate·문서 참조·원장 검사는 최종 `codex/mixer-mxd2`에 문서와 패치를 반입한 뒤 시행한다. PASS 뒤 commit하고 그 pin의 Git blob으로 ZIP/PIN/MANIFEST를 별도 작성한다. 새 commit SHA는 문서의 `<<sha:Fix mixer D2>>` 자리에 미리 넣지 않는다.

## 최종 반입 UI 확인

`integration-ui/README.md`에 후보 커밋 전 실제 Flask render 및 로컬 브라우저 결과를 기록했다. 원 작성자/독립 실행 결과와 구분한 추가 UI 검사이며 등록 또는 외부 실행 승인으로 읽지 않는다.
