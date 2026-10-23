# D3 v2 설계 준비 증거 (2026-10-23 · scratch, 미반영)

이 묶음은 실험/DEM/등록을 실행하지 않고 D3 v1의 과도한 보장을 새 설계안으로 바꾼 작업이다. tracked 파일을 직접 수정하지 않았다. 작성자 자체 검산이며 독립 사전 공격 리뷰는 아직 없다.

## 반영 후보

| scratch 파일 | 제안 저장소 경로 |
|---|---|
| `mixer_d3_se_flowability_anchor_design_v2_20261023.md` | `docs/reviews/` 아래 같은 이름 |
| `codex_mixer_d3_design_v2_request_20261023.md` | `docs/reviews/` 아래 같은 이름 |
| `d3_v2_counterexamples.py`, `counterexamples.json`, `baseline_numbers.txt`, `SOURCE_SHA256SUMS`, 이 README | `docs/reviews/mixer_d3_design_v2_evidence_20261023/` |
| `proposed_ledger_fragments.json` | 공유 원장에 직접 적용하지 말고 Codex 새 협업 쪽지의 제안 조각으로 전달 |

`MANIFEST.sha256`은 최종 scratch 산출물 지문이며 핀 ZIP의 manifest가 아니다. 요청서 리뷰 핀은 비어 있고 발송 상태는 HOLD다. 최종 경로에 복사·검토·전체 게이트 이후 실제 커밋 blob으로 ZIP/PIN/MANIFEST를 만들어야 한다.

## 수행과 결과

환경: Linux, Python 3.11.17, `/workspace/.venvs/yonghoon-dem`, BLAS 한 스레드. 검산 소스 HEAD 및 각 파일 SHA는 `counterexamples.json` / `SOURCE_SHA256SUMS`에 있다.

1. 기존 `docs/reviews/codex_mixer_d3_design_request_evidence_20261021/d3_precheck_numbers.py`를 `python -I`로 실행: rc 0, `baseline_numbers.txt`.
2. 새 `d3_v2_counterexamples.py --repo /workspace/Yonghoon-DEM-DFT`를 `python -I`로 실행: rc 0, **29/29** 반례/산술 관계 PASS, `counterexamples.json`.
3. 같은 명령을 다시 실행: rc 0, **29/29**, 출력 `cmp` rc 0(바이트 동일).
4. 같은 SE–SE 정적 천장을 생성기 역계산뿐 아니라 평형식에서 푼 닫힌식으로 대조했다: gen1 832.6622178589646, lab20261014 1015.4417290962982. 생성기에 다시 넣으면 δ/r=0.01(상대 허용 1e-12).

실측/DEM 런/생산 덱 생성은 모두 0이다. 시험 기하 코드·생산 판독기를 구현한 것이 아니므로 **29개 생산 회귀 시험 통과**, **깨짐 8건 종결**, **C0 GO**라고 해석하면 안 된다.

검사기는 문서 개정에 앞서 핵심 반례를 작성하고 실행했으며, 문서 검토 중 실제 SE-only 생성기·기하/예산·발사 정책 검사를 보강했다. 초기 하니스에서 마지막 격자 비율을 float `== 3`으로 검사해 1건이 실패했다(수학적 비율은 3, float 반올림 차). 이를 `isclose(..., rel_tol=1e-14)`로 고쳤다. 이 하니스 실수를 v1 생산 코드의 실패→수정 증거라고 세지 않는다. 초기 출력은 scratch의 `harness_first_output.json`에 보존했다.

## 변경 제안과 한계

- 기본 결과를 유한 Bo 후보 집합으로 바꾸어 근거 없는 연속 보간 구간/중심을 주장하지 않는다. **이것은 새 설계 선택(V2-Q1)이며 아직 비준되지 않았다.**
- 모든 판정 점 불확도·날/시드/시간 상관·국소 감도 검출력은 등록 필수 조건이다. 반복 수·통계 방식·예산을 새로 정해야 한다.
- 고정 벽/ρ 조건부성, 관측 불가, 미지원 계약, 부분 검증, SOP→측정→곡선 봉인→열람을 분리한다.
- 단순 양 끝 감도는 내부 외피가 아니며, 검증 양 끝+중심은 내부 이진 전이를 놓칠 수 있음을 추가 반례로 보였다.
- 기존 장비·혼합기·G·벽·밀도·시료량·측정자·탭·반복·입도 측정법 빈칸은 그대로다.
- 문헌은 기존 정본을 연결했으며 새 PDF/SI 원문 검증은 없다. 옛 드럼 선례의 현 덱 재현·LIGGGHTS 문법·실제 처리량도 미확인이다.
- 공유 원장용 MXD3 8개는 **open 등재 제안**이며, `MXD2-07`도 자동으로 claimed_fixed/verified로 바꾸지 않는다.
