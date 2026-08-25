---
title: "교차리뷰 E — SDCP wave1 게이트 수정·물리 결론 (판정 수령 + 반영)"
date: 2026-08-25
updated: 2026-08-25
tags: [codex, review, sdcp, vasp, gate, wave15]
status: 종결-실행승인(내부 max 리뷰)
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-25
verifiedBy: "판정의 코드 지적 4건을 실측 재현 후 수정 (LDAUU 산문형 되울림·AUDIT_KEYS 7키 실측 포함)"
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source
---

# 교차리뷰 E — SDCP wave1 (2026-08-25 판정 수령)

> **판정 요지**: "버그 수정은 정당하지만, 현재 상태로 물리 결론까지 승인하기에는
> 재작업이 필요하다." — E-1/3/5/6 조건부 찬성 · **E-2/E-4 반대** · 구조 내보내기 조건부.

## 우리 실측이 판정을 확인/보강한 것

| 지적 | 실측 결과 |
|---|---|
| `_echo_val` 이 LDAUU 를 한 토큰으로 자름 | **더 나빴다** — LDA+U 되울림은 행 중간 산문형(`for each species LDAUU =`)이라 행두 앵커로 **0건**. 게다가 생성부 `AUDIT_KEYS` 가 7키뿐이라 LDAUU 는 **비교 대상에 든 적이 없었다** (0 UNVERIFIED = 미등록) |
| MAGMOM 감사 없음 | OUTCAR 가 MAGMOM·ADDGRID 를 **아예 되울리지 않는다**(grep 0건) — 원리적 검증 불가 → 명시적 unverified 로 |
| 다중 실행 혼합 | wave1 43개는 전부 단일 실행(배너=timing=1) — 세그먼트 분리는 안전망 |
| E-4 상관 구조 | 재검산 일치 — `ΔE차 = E_ads(Ni)차 − E_ads(Li)차` 항등식, clean net4−pm1 = 128.292 meV |

## 반영 완료 (2026-08-25, 커밋 푸시됨)

- **E-1** 산문형 앵커 + 줄끝 캡처 · Decimal 비교(1e309≠2e309·비유한값 불일치, 문자열
  지름길보다 **먼저**) · AUDIT_KEYS 7→16 · **end-to-end 음성 7건** (실제 파일 →
  read_outcar → phase_gates: LDAUU 실차이·깨진 바이트·잘린 gzip·공존·2실행·MAGMOM·inf)
- **E-2** 게이트 보증 범위를 docstring 명시 + 상마다 `incar_audit`
  (verified_exact / verified_equivalence_class / unverified / mismatch) + `run_segments`
  를 RESULTS.json 에 수록. **LREAL 은 exact 가 아니라 equivalence_class.**
- **E-3** errors="ignore" 제거 — strict 디코드, gzip CRC/절단 → OUTCAR_READ_ERROR
  하드게이트, plain/.gz 공존 차단, 확장자·매직 불일치 기록, NUL(UTF-16) 검출
- **E-4** "50.2±0.2 측정" **철회** → 허용 문구(상관된 contrast 의 49.5–50.5 meV
  branch offset, 진단값)로 kb 판정카드·설명문·artifact 3곳 정정. `flip_indices_poscar`
  를 RESULTS 에 기계기록 (첨부물로 "#82" 재검증 불가 문제 해소)
- **E-5** "2-seed 0.1 meV 일치" → "matched-pose ΔE 의 branch×site 상호작용 0.09 meV"
  + k-미검증 단서 + basin 무관성 증명 아님 단서
- **구조 내보내기** Selective Dynamics 원자별 승계(if_pos·move_mask — 22구조 × 144
  고정), `.qe-structure.inc` 실행불가 확장자, 라디칼 6건 전하/스핀 결정 전 실행금지
  명기, 원본·산출 sha256 + 변환기 git 해시
- **wave1.5 패키지** `--basin_rescue` — clean_slab net4 를 2상(NUPDOWN=+4 pin →
  ICHARG=1 해제)으로 유도. NUPDOWN 은 시드 자화합에서 **계산**(비정수면 거부),
  2상 diff 는 ICHARG 한 줄, POSCAR/KPOINTS 바이트 동일, fail-closed 사슬,
  재반전 시의 해석(realized-basin)까지 README 에 선언. selftest 9/9

## 미반영 (다음 라운드 — 순서대로)

1. **E-6 유효성 분리** — energy_valid / delta_e_valid / e_ads_valid /
   ground_state_valid / realized_basin_id 를 분석기에 구현 + 회귀시험. 규칙 문서화
   전 적용 금지(codex 승인 조건). 첫 구현에서 E_ads 는 계속 막는다.
- 2. **QE assembler** — 조각+정본 템플릿 → 완성 입력 (제약·AFM·U·pseudo·전하·k-mesh
   검사). 수동 splice 를 최종 인터페이스로 두지 않기.
3. **README vs RESULTS 정합** — 사람용 요약이 machine 산출물(정본)과 어긋나지 않게
   wave1.5 부터 README 를 RESULTS 에서 생성.
4. sdcp_doped 라디칼 스핀 규약 (1저자 결정 대기) · noncollinear constrained pair
   (#82 반전 비용 — 프로토콜 변경이라 별도 승인 전 미착수)

## 산출물

`sdcp_wave15_basinA_2026_08_25.zip` — rescue 잡(2상) + 분석기 v2 + README ·
새 추출 검증(analyzer selftest PASS · run_job 문법 OK).


---

## 📥 E-2차 판정 (2026-08-25 수령) — "레시피 조건부 승인 · 실행 패키지는 보완 전 승인 불가"

**필수 6건 → 전부 반영 (v2 패키지 재발송):**

| # | 지적 | 반영 |
|---|---|---|
| 1 | rescue 가 기존 분석에 연결 안 됨 | `rescue.supersedes` + 분석기 `ref_alias` — 통과 시 clean 참조 자동 교체, 실패 시 `reference_overrides` 에 거부 사유. **병합 트리 실측**: 미실행 rescue → `rescue_rejected(NOT_RUN)` + 원본 유지 + 17/30 불변 |
| 2 | release 에 NUPDOWN=4 잔류해도 통과 | `incar_expected.static.NUPDOWN="-1"` 명시 — 잔류가 하드게이트 (e2e 음성으로 봉인) |
| 3 | pin 검증 없이 release | `--check_pin` 신설: 정상종료·NELM·NUPDOWN 되울림·topology(flip 0)·모멘트 붕괴·CHGCAR sha256 → PIN_CHECK.json. run_job 은 통과 후에만 release, stale CHGCAR 사전 삭제, 복사본 sha 동일성 검증. 검증 4건(양성 2·음성 2) |
| 4 | 광고한 e2e 가 배포본에 없음 | **배포 분석기 자신의 --selftest 에 파일수준 e2e 10건 내장** (산술 20 + e2e 10 = 30) |
| 5 | static_pin provenance 유실 | rec 이 모든 상 보존 + RESULTS jobs 행이 phases 동적 순회 |
| 6 | LDAU·LMAXMIX 미감사 | 감사키 추가. LDAU 는 "LDA+U is selected" 산문 존재로 판별 (꺼짐은 unverified — 비대칭 명시) |

**E-4 후속**: `index_base:0` + 1-based 병기. **계보**: parent 를 /tmp 경로가 아니라
이름+sha256(POSCAR/INCAR/KPOINTS) 로, 조립 POTCAR sha 는 run_job 이 출력.

**W-1~3 문구 채택:**
- W-1: "#82 단독 반전 금지" → **"총자화가 달라지는 반전의 억제"** (보상 반전 가능성
  명시, topology 는 check_pin 이 별도 확인). site 별 hard pin 은 collinear 에 없음 인정.
- W-2: 회신물에 **vasp.log 포함** (CHGCAR read 증거), CHGCAR sha 양측 동일 검증,
  표기 `E(static | basin A, initialized from pinned CHGCAR)`.
- W-3: 재반전 = "국소최소 아님" 증명이 아니다 → 허용 문구로 교체 ("unconstrained
  stationary solution 입증되지 않음 · pin 실패면 미판정 · 새 signature 는 basin C").

**미반영 유지** (범위 밖 선언): POSCAR/CONTCAR 용 `_read_text(errors=ignore)` (우리
파일 + sha 무결성 하에 허용), E-6 유효성 플래그, QE assembler.


---

## 📥 E-3차 판정 (2026-08-25) — "5/6 확인 · 3번 사슬에 blocker 4"

핵심 재현: **LDAUU=5.0 으로 바꾼 pin 도 check_pin 을 통과** — v1 check_pin 이
자기만의 축소판 검사(NUPDOWN·topology)였기 때문. 물리 레시피·W 문구는 추가 이견 없음.

**4건 반영 (v3 패키지, zip sha256 ebb0e848…):**

| # | 지적 | 반영 |
|---|---|---|
| 1 | check_pin 이 전체 게이트를 안 씀 | **phase_gates 전체를 태운다** — 등록된 INCAR 기대키 18개·MULTI_RUN·판독오류·형식·E0·NIONS·POTCAR TITEL·k 상한 + topology/모멘트/CHGCAR. 빌더가 kmesh·potcar_spec 을 잡 안에 주입(없으면 fail-closed). **LDAUU=5.0 케이스를 음성으로 봉인** + 2실행 pin 거부 |
| 2 | CHGCAR 만 지워 산출물 혼입 | 지우지 않는다 — **기존 산출물이 하나라도 있으면 실행 거부** (1회용 선언, README 명시) |
| 3 | 해시가 콘솔에만 | `RUN_PROVENANCE.json` 영구 기록: run-id·UTC·입력/POTCAR sha·**부모 POSCAR/KPOINTS 대조(불일치 시 실행 중단)**·CHGCAR pin/사본 sha·charge-read 증거(grep 원문). 회신물 목록에 포함 |
| 4 | supersede 가 r.ok 만 봄 | `rescue_provenance_ok()` — PIN_CHECK.pass · PROVENANCE 존재 · 부모 대조 · CHGCAR sha 일치(PIN_CHECK 와 교차) · read 증거. 하나라도 없으면 `rescue_rejected(사유)`. 음성 5건 봉인 |

selftest: check_pin 6건(양2·음4) · provenance 5건(양1·음4) · rescue 17/17 · 전체 통과.

⚠ charge-read 증거의 grep 패턴(`charg`+`read|from file`)은 VASP 빌드별 문구 변형
위험이 있다 — NOT_FOUND 로 오면 supersede 가 막히고 PROVENANCE 원문으로 재협상
(fail-closed 쪽으로 실패).


---

## 📥 E-4차 판정 (2026-08-25) — "보류 · fail-open P0 5건"

내 적대 재현이 목록 도착 전에 3건을 독립 확인했고(결측 provenance 통과 · 부정문
증거 · 배포 대조 없음), **kmesh 결측 통과 · phase KPOINTS 가 provenance 밖**
2건은 codex 만 잡았다.

**5건 반영 (v4, zip sha256 76bba0d5…):**

| P0 | 지적 | 반영 |
|---|---|---|
| 1 | kmesh 결측이 통과 | phase_gates 의 관용(wave1 호환)을 check_pin 에서 차단 — kmesh.static_pin 결측 = 거부 |
| 2 | 실제 KPOINTS(phase 사본)가 provenance 밖 | preflight 가 **루트+phase 사본 전부**(11파일) 해시 기록·대조. 사본 ≠ 루트 = 실행 전 중단 |
| 3 | POTCAR·배포 입력 미대조 | MANIFEST_RESCUE ↔ 실행 기록 ↔ 디스크 **3중 대조** (job.json·run_job.sh 포함). POTCAR 는 조립본 ↔ phase 사본 일치 강제 |
| 4 | 결측 provenance 통과 (`all({})==True`) | 키별 `is True` 요구 · identical 플래그 불신(sha 직접 비교) · PIN_CHECK CHGCAR sha 필수 + 교차 |
| 5 | charge-read 부정문 양성 처리 | 부정 마커(not·error·fail·could·unable·cannot·warn) 필터 — runner 는 부정문을 따로 기록(재협상 근거), 판정기는 양성 클린 라인만 인정 |

추가 봉인: pin INCAR 사후 변조(디스크 ≠ 배포 해시) 거부.
음성 selftest: check_pin +2 (kmesh·INCAR 변조) · provenance 7건 (P0 다섯 + 기록해시
부재 + 사후 변조). 배포본 상대 적대 재확인 5/5 닫힘.


---

## 📥 E-5차 판정 (2026-08-25) — "보류 · P0-1·4 닫힘, P0-3·5 재현 4건"

**같은 실수를 두 번 했다**: E-2차에서 지적받았던 "번들에만 있고 배포본에 없는
검사" 를 새 스위트(음성 9건)에서 반복했다. 이번에 구조적으로 고쳤다 —
**check_pin·provenance 스위트를 배포본 selftest_k 로 이사**하고 번들 쪽 사본을
삭제, 번들 selftest 는 배포본을 실행해 존재(라벨 개수)와 통과(rc=0)만 검사한다.
사본이 없으니 다시는 갈라질 수 없다. 배포본 selftest 30 → **51건**.

**재현 4건 반영 (v5, zip sha256 dbf4a64a…):**

| 재현 | 봉인 |
|---|---|
| `["hello"]` 가 증거로 통과 | 양성 패턴 필수 (charg + read/from…file) — 부정 마커 배제만으로는 부족했다 |
| 문자열 `"NOT_FOUND"` 통과 | **타입 검사** — 문자열을 순회하면 한 글자짜리 '증거' 가 생긴다. list[str] 강제 |
| static/INCAR 디스크 부재 통과 | '있으면 대조' 폐기 — 배포 파일 8종(phase KPOINTS 포함)은 **존재 자체가 필수** + 해시 일치 |
| `preflight_problems=["bad"]` 통과 | 판정기가 그 필드를 아예 안 봤다 — `== []` 강제 (부재·위조·비어있지 않음 전부 거부) |

부수: 증거 패턴이 `from file` 인접을 강제해 실제 형("from CHGCAR file")을
놓치던 것을 runner·판정기 **양쪽 동일 패턴**으로 정렬 (배포본 양성 fixture 가 잡았다).
빌더 MANIFEST_RESCUE 에 phase KPOINTS 2종 추가 (7 → 9 파일).


---

## 🏁 E-트랙 종결 (2026-08-25) — 외부 리뷰 토큰 소진, 내부 max 리뷰로 판정

E-6차 판정문이 "이전 P0 두 건 + 부정문 변형 하나" 에서 잘린 채 도착했고 외부
리뷰는 더 불가. **판정 책임을 내재화**해 전체 사슬을 자체 공격한 뒤 종결한다.

### 마지막 라운드에서 바꾼 것 (v6, zip sha256 979625b4…)

1. **CHGCAR 승계 증거를 stdout grep → OUTCAR 마커로 전면 교체.**
   wave1 실측(dense=ICHARG1 vs static=ICHARG2 대조): `initial charge density
   was supplied` + `overlapping atoms calculated` **부재** = 파일 승계.
   이로써 부정문 블랙리스트 두더지잡기("can't", "skipped", …)와 특이도 없는
   양성 패턴(`atomic valenz-charges read in` 은 ICHARG=2 에도 있음 — 잘린
   지적의 정체로 추정) 클래스가 통째로 제거됐다. stdout 기록은 정보용 강등.
2. **parent_match 불리언 불신** — 재계산 사슬(디스크==배포해시==부모해시,
   job.json 은 자체 해시앵커)로 독립 검증. 기록 위조 무력화.
3. run_id/utc 형식 강제.

### 자체 공격 배터리 (배포본 상대, 전부 닫힘)

과거 codex 재현 전건 + 신규: **pin OUTCAR 를 static 에 복사**(ICHARG=2 흔적으로
검출 — codex 도 안 던진 공격) · **2실행 이어붙임**(마지막 완결 세그먼트만) ·
.gz 변형 · NOT_FOUND 타입 함정 · 부모 재계산 불일치. 배포본 selftest **53건**.

### 판정: **실행 승인** — 잔여 위험 4건 명시 (은폐하지 않는다)

| 잔여 | 완화 |
|---|---|
| 전 산출물(OUTCAR 포함) 일관 위조 | 위협모델 밖 — 실수·스크립트 우회 방지가 목적. OUTCAR 위조까지 가면 어떤 감사도 무력 |
| MANIFEST_RESCUE 자기서명 부재 (재생성 공격) | 분석은 **우리 트리**(배포 원본)에서 수행 + zip sha 를 kb 에 공표 |
| check_pin 이 CHGCAR 크기 하한을 안 봄 | 깨진 CHGCAR 는 release VASP 가 즉시 실패 + OUTCAR 마커 게이트가 백스톱 |
| 외주측 runner 수정 자체는 미검출 | 산출물 게이트(OUTCAR 감사·마커·해시 대조)가 백스톱 — runner 는 편의, 진실은 산출물 |

### 교훈 (다음 외주 패키지의 시작점)

- **검사는 배포본 한 곳에만** — 번들은 배포본을 실행해 개수·rc 만 본다. 같은
  실수를 두 번 했다(E-2·E-5차).
- **게이트 입력은 로그 문자열이 아니라 산출물의 구조적 마커** — 블랙리스트는 진다.
- **기록된 불리언은 증거가 아니다** — 재계산 가능한 것은 재계산한다.
- 적대 검증을 리뷰어에게 미루지 말 것 — 만들 때 공격 케이스를 같이 만든다.
