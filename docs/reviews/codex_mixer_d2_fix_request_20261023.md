# Codex 재확인 요청 — 믹서 D2 생성기 수정 (2026-10-23 · 새 실제 런 0건 · 발송 = 1저자)

- **이번에 닫는 것:** `MXD2-02`–`MXD2-06` 생성기·회귀시험·벽 규칙·메타·웹앱 설명의 `claimed_fixed` 제안을 검토해 주세요. 내부 독립 재확인에서 발견한 실제 중력 누락, AM_P+SE 양성 회귀, 설명 줄 주입, scalar CLI 시험 누락도 함께 고쳤습니다.
- **이번에 닫지 않는 것:** `MXD2-01`은 **HOLD/open**입니다. lab/D2 되읽기·비교·스모크와 새 S1 셀·코호트·정책 v5를 구현·등록하지 않았습니다. `MXD2-07`의 밀도별 정적 천장 정정은 **D3 v2 설계 검토 대상**이며 이 생성기 수정으로 닫지 않습니다. 외부 GO·새 확인 블록·앵커 보정·LIGGGHTS·실물 믹서·장비 실행·배포 승인은 없습니다.

**발송 전 초안:** 공유 원장을 직접 고치지 않았습니다. 아래 내부 독립 v2는 생성기와 시험 범위에서 R1–R4가 닫혔고 새 결함을 발견하지 못했다고 판단했습니다. 저장소 FULL gate는 `mixer_d2_fix_evidence_20261023/full_gate_receipt.json`의 최종 상태로 별도 확인해야 하며, 현재 조립본은 **대기**입니다. 이 상태에서 발송 완료·verified·발사 가능을 주장하지 않습니다.

## 1. 검토 범위와 핀

| 항목 | 대상 |
|---|---|
| 작업 가지 | `codex/mixer-mxd2` — 이 가지를 유지하고 `codex/*`에만 push |
| 출발점 | `claude/sdcp-dem-manuscript-si-pqwtv8`의 `7799a2ff64ba462b42ce05edd3e63b7c2854d557` |
| 받을 커밋 | `Fix mixer D2 validation and preserve supported phase sets` 한 묶음, 쪽지 자리표시 `<<sha:Fix mixer D2>>` |
| 최종 review pin | commit 뒤 생성하는 전달 ZIP 바깥 `PIN.txt`에 전체 SHA. 자신을 포함하는 이 문서에는 새 SHA를 미리 적지 않음 |
| 발송 대조 | 최종 pin의 Git blob + 외부 `PIN.txt` + `MANIFEST.sha256`; 전체 gate PASS 뒤 root 담당자가 ZIP 작성 |
| 생산 코드 | `scripts/make_mixer_deck.py` 한 파일 |
| 사용자 설명 | `docs/mixer_devlog/v17_20261023.md` (`/mixer` 개발 이력), 이 요청서와 사전 점검·증거·새 협업 쪽지 |
| 근거 | `mixer_d2_fix_evidence_20261023/` — 아래 상대 경로는 이 요청서 위치 기준 |
| 기준 정본 | `docs/hetero_thesis.md` D2, `docs/mixer_d2_wall_gamma_derivation_20261014.md`, 인계서 §5-3, 원장 `MXD2-01`–`07` |

공유 `scripts/additives.py`, `webapp/app.py`, 전역 게이트·정책·봉인 32파일, `CLAUDE.md`·원장·진행 기록은 수정하지 않았습니다. 증거 폴더의 소스 사본은 검증 대상 신원과 재현을 보존하는 자료입니다. 물성·밀도·벽 계수·생산 중력·시드·새 캠페인 수준을 바꾸거나 정하지 않았습니다.

| 생성기 신원 | SHA-256 |
|---|---|
| 기준 소스 | `6baaa04c13c842c2d8e486cbef83bb5cb6f6e3d5f88c5f0f0d8c0904d3949f30` |
| 독립 v1 검토 소스 | `dada1ebbf22dfc74a0d47000e1a35493d5e2d30cc2bc8d9e92509984665ef81b` |
| 최종 v2 검토 소스 | `661936b78c3d60794714a63102f5461f7f42f581a5ad7da466c7c6fe0465bc27` |
| 원본→v2 full patch | `2b865ee1e553f4ebc737599888cd22ab99c7be6fe41cd65cf440b793786ad210` |
| v1→v2 delta | `ac13a4c415ab1d03985a56e12102b665a61a2746abccb1c5da795c5ae6604586` |

독립 검토자는 full patch를 원본에 적용한 결과와 delta를 v1에 적용한 결과가 바이트까지 같음을 확인했습니다. 최종 commit의 생성기 blob도 위 최종 소스와 대조해 주세요.

## 2. 고쳤다고 주장하는 내용

| 항목 | 현재 동작과 검증 | 한정 |
|---|---|---|
| MXD2-02 (P2) | 실제 덱에 인쇄된 CED·영률·포아송비·반경·밀도·**중력 명령**에서 Bo를 독립 되읽기하여 입력/meta와 대조. gen1 밀도 강제·meta Bo 상수·D2에만 gravity=1.0 변이를 검출 | 기존 `diff --allow E`는 상대 경화 검사이며 절대 Bo 인증이 아님 |
| MXD2-03 (P3) | ρ=10, Bo=800의 AM_P–SE 혼합쌍 천장 반례를 상주 검사. 혼합쌍 천장 생략 변이를 검출 | 정적 무하중 겹침 검사로 동역학 자격을 주장하지 않음 |
| MXD2-04 (P3) | γ의 곱 대신 제곱근끼리 곱해 중간 언더플로 방지. 양의 유한 정상 float·계산 결과 검사. ASCII 십진수만 변환. 팔 이름 fullmatch, 설명의 비문자열/CR/LF를 생성자와 deck/meta 재검증에서 거부 | 합성 극단값의 산술 회귀이며 실제 분말 수준 제안이 아님. 임의 사전 구조 전체의 통제된 거부 보장 아님 |
| MXD2-05 (P3) | 실제 D2 덱/meta에 비코팅 NCM 벽 결합 필수. 활성 NCM의 γ는 모두 ρ 또는 모두 1. 기존 AM_P+SE 두 상 발행 유지. CLI 직접 벽값만으로 발행 거부, 도움말 정정 | helper의 일반 기하평균 계산과 실제 발행 자격을 구분. 모든 상 조합을 새로 지원한 것은 아님 |
| MXD2-06 (P3) | D2만 schema `mixer_deck_meta/2`, `registered=null`, `development_contract=D2-geomean/unregistered`. 실제 벽 주석 정정. v1.7에 `--dens-gen`·`--gm-wall-ncm`·개발 미등록 설명 | 기존 팔의 schema·덱 바이트는 자체 골든 검사 유지. 새 코호트 미등록 |

독립 v1의 R1–R4는 각각 실제 중력 누락, 빠진 AM_S를 요구하여 AM_P+SE를 거부한 양성 회귀, 설명 CR/LF 실행줄, wall/Bo scalar를 float로 되돌리는 변이의 생존이었습니다. 시험을 먼저 추가하여 R1·R2·R3 실패를 확인한 뒤 수정했습니다. R4는 원래 정상 거부하던 동작에 회귀 검출을 보강했습니다. 생산 물리 숫자는 변경하지 않았습니다.

작은 해석 반례: γ_AM=10⁻²⁰⁰의 동종 힘비는 `(r_AM/r_SE)γ=9×10⁻²⁰⁰`입니다. 기준 코드는 γ 곱이 0이 되어 힘비 0을 냈고, 수정판은 `9.000000000000226e-200`입니다. 이는 합성 수치 반례이며 실험 보정값이 아닙니다.

## 3. 시험과 독립 재확인 — 서로 다른 수를 합산하지 않음

Python 3.11.17, `python -I`, BLAS/OMP 스레드 1에서 실행했습니다. 덱 생성·파싱·합성 반례만이며 실제 시뮬레이터·GPU·실험 실행은 0건입니다.

| 단계 | 관찰 | 근거 (`mixer_d2_fix_evidence_20261023/` 아래) |
|---|---|---|
| 기준 | 143/143 PASS | `mixer_d2_fix_evidence_20261023/author/logs/generator-baseline.log` |
| 첫 시험 먼저 | 145/154 PASS, 9 FAIL | `mixer_d2_fix_evidence_20261023/author/tests_first/generator-tests-only.py`, `mixer_d2_fix_evidence_20261023/author/logs/generator-red-final.log` |
| v1 수정 | 154/154 PASS | `mixer_d2_fix_evidence_20261023/author/logs/generator-green.log` |
| 독립 R1–R4 시험 먼저 | 155/158 PASS, R1·R2·R3 FAIL; R4의 정상 거부 유지 | `mixer_d2_fix_evidence_20261023/author/tests_first/generator-review-tests-only.py`, `mixer_d2_fix_evidence_20261023/author/logs/review-red-final.log` |
| **최종 생성기** | **158/158 PASS**, rc0 | `mixer_d2_fix_evidence_20261023/author/logs/review-green-final.log`, `mixer_d2_fix_evidence_20261023/independent/v2/selftest.log` |
| **작성자 변이** | **16개 전부 해당 MXD/MXDR 검사로 검출**. 알려진 세 약점의 의미를 재구성한 변이는 기준 143개에서는 생존 | `mixer_d2_fix_evidence_20261023/author/mutation-results.json`, `mixer_d2_fix_evidence_20261023/author/logs/mutation-*-{before,after}.log` |
| 독립 v1 | 10변이 중 7 검출·3 생존, R1–R4 지적 | `mixer_d2_fix_evidence_20261023/independent/v1/REVIEW.md`, `mixer_d2_fix_evidence_20261023/independent/v1/evidence/results.json` |
| 작성자의 v1 프루브 재실행 | 10변이 검출. 설명 거부를 기록하는 adapter 사용. **독립 판정 아님** | `mixer_d2_fix_evidence_20261023/author/auxiliary_archive/`의 원 도구·adapter diff·결과 |
| **최신 독립 v2** | **14/14 변이**를 관련 검사에서 검출, R1–R4 닫힘 | `mixer_d2_fix_evidence_20261023/independent/v2/REVIEW.md`, `mixer_d2_fix_evidence_20261023/independent/v2/evidence/results.json`, `mixer_d2_fix_evidence_20261023/independent/v2/evidence/mutants/*/selftest.log` |
| 독립 정상 3상 수치 대조 | **192덱·1,728접촉쌍** = 밀도2×CGF3×강성2×ρ4×코팅2×Bo2 | 같은 v2 `evidence/results.json → normal` |
| 독립 추가 양성·입력 | AM_P+SE **8덱**; 설명 7종×3경로 **21거부**, 정상 설명4; CLI **32거부**(gamma12+scalar20) | 같은 v2 JSON `observations`, `cli_input` |
| 독립 v1/v2 바이트 대조 | 정상192덱 모두 바이트 동일, meta는 source hash만 변경 | `mixer_d2_fix_evidence_20261023/independent/v2/prior_comparison.json` |
| 기존 소비자 호환 검사 | diff55/55, readback24/24, smoke 자체 검사 rc0 | `mixer_d2_fix_evidence_20261023/author/logs/{deck-diff,deck-readback,smoke-blind}-compat.log` |
| 웹앱 v1.7 | 실제 `/mixer`에 scratch 문서 조회를 주입: 페이지9/9 및 필수 CLI·schema·HOLD 표시 확인 | `mixer_d2_fix_evidence_20261023/author/logs/devlog-v2-render.log` |
| **저장소 FULL gate** | **root 최종 반입 뒤 대기**. PASS 전 발송 패키지 확정 불가 | `full_gate_receipt.json` |

정상 192덱의 최대 상대 Bo 오차는 `1.2876531367167487e-5`, 접촉쌍 힘비 최대 상대오차는 `2.5893352707528905e-5`입니다. 프루브의 사전 허용폭 `2e-5`, `3e-5` 이내이며 CED 인쇄 정밀도를 반영합니다. 정상 3상192덱과 추가2상8덱은 다른 집합입니다. 수치·구조·helper 경계49개는 관찰 범위로 기록했으며 전부 통제된 거부였다고 주장하지 않습니다.

내부 독립 검토자는 작성자의 결과 설명을 읽지 않고 diff·원본·이전 독립 반례로 재현했습니다. 옛 10-21 외부 scratch의 prereview_mixer_d2/REVIEW.md와 원래 24변이 스크립트는 이 체크아웃에 없으므로 그 24개를 전부 복원·재실행했다고 주장하지 않습니다. 이전 보고서·도구·원 manifest와 결과는 그대로 보존했습니다.

## 4. HOLD 및 남은 한계

**MXD2-01:** lab D2 덱의 되읽기 표 E는 gen1 밀도 고정 때문에 FAIL, 같은 ρ 세계 코팅/비코팅 짝은 A/B/U/E/EB에서 모두 FAIL입니다. N=100000, CGF151.4에서 스모크 계획 수는 `(176,859,98965)`인데 lab 계획은 `(143,699,99158)`입니다. 기존 소비자 자체 시험 통과는 이 문제의 해결 증거가 아닙니다 (`mixer_d2_fix_evidence_20261023/author/auxiliary_archive/mxd2-01-probe.json`).

후속은 (1) 실제 밀도/세대·계획 수의 결합 검증, (2) D2 전용 쌍 비교 규칙, (3) 실물 입력·결정과 결합한 S1 셀·코호트·정책 v5 등록으로 나눠 제안합니다. 기존 A/B/U/E/EB 허용목록에 새 계약을 끼워 넣거나 새로운 ρ/Bo/시드를 정하지 않았습니다. 실행 정책 v5는 미승인입니다.

**MXD2-07:** D3 v2에서 gen1과 lab20261014의 정적 천장 숫자·적용 조건을 구별해 검토합니다. 이 요청의 보조 산술 진단은 후속 설계 근거이며 새로운 물리 상한·실험 앵커·실행 승인이 아닙니다.

독립 리뷰가 다시 관찰한 임의 text와 deck_meta 입력의 결합, 호출자가 변조한 plan의 밀도 세대 라벨/표 불일치, 점착 지배 무하중 δ0와 중력 하중 접촉의 구분, 일부 비정상 사전의 TypeError/KeyError는 닫지 않았습니다. AM_S+SE 단독 plan의 기존 AM_P KeyError도 이 AM_P+SE 양성 회귀 수정과 다릅니다.

기존 믹서 `claimed_fixed` 25개는 다음 확인 목록으로 이 요청에 함께 보존합니다. **이번 새 158개/변이/192덱으로 25개를 새로 검증했다고 주장하지 않으며**, 각 기존 원장 근거를 별도로 판정해 주세요.

| 묶음 | 기존 claimed_fixed 확인 대상 |
|---|---|
| HB (3) | HB-01, HB-04, HB-05 |
| HBR2 (4) | HBR2-01, HBR2-04, HBR2-05, HBR2-08 |
| HBR3 (5) | HBR3-01, HBR3-02, HBR3-03, HBR3-04, HBR3-08 |
| HBR4 (2) | HBR4-01, HBR4-05 |
| HBR6 (2) | HBR6-01, HBR6-03 |
| HBR10 (3) | HBR10-01, HBR10-02, HBR10-03 |
| MIX (6) | MIX-01, MIX-02, MIX-03, MIX-04, MIX-05, MIX-08 |

## 5. 재현과 부탁드리는 판정

`mixer_d2_fix_evidence_20261023/README.md`에 새 출력 폴더로 실행하는 명령과 원 결과 경로가 있습니다. 최종 pin의 생성기 자체 시험 및 보존한 원본+patch의 독립 프루브를 각각 실행해 주세요. 기록기의 rc0 하나가 승인 판정은 아니므로 JSON의 항목별 실제/기대 결과를 확인해야 합니다.

1. MXD2-02–06 각각 수정 범위와 양성 대조·변이 검출이 충분한지, 추가 수정/claimed_fixed 유지/verified 가능을 나눠 주세요.
2. 실제 gravity를 포함한 절대 Bo 검산, 혼합쌍 천장, scalar 검사 전 숫자 정규화, 생성 후 사전 변조까지 포함한 설명 CR/LF 차단이 각각 해당 반례를 잡는지 확인해 주세요.
3. 활성 NCM의 두 허용 상태와 AM_P+SE 양성 발행, D2 미등록 메타, 필수 밀도/벽 CLI와 `/mixer` v1.7이 정본과 일치하는지 확인해 주세요.
4. MXD2-01 HOLD·정책 v5 미승인·MXD2-07 D3 설계 분리 및 위 한계가 실제 검증 범위를 넘지 않는지 판정해 주세요.
5. 최종 pin·원 manifest·FULL gate receipt와 소스 신원이 일치하는지 확인한 뒤 외부 코드 판정을 부탁드립니다. 새 실험·새 확인 블록·발사/배포는 별도입니다.

추가 finding에는 적용 pin, 재현 입력/명령, 실제/기대 출력과 최소 반례를 부탁드립니다. 발송과 원장 최종 반영은 1저자/공유 기록 담당자가 수행합니다.
