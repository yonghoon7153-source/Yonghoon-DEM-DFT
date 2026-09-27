---
title: "리뷰 CF 회신 — A′ V5 VASP 외주 준비본 v2: NO-GO (P0 3 · P1 3 · D3 예산 조건부 찬성 · 3b′/3c 찬성)"
date: 2026-09-27
updated: 2026-09-27
tags: [review, codex, reply, adhesion, wad, prereg, vasp, outsourcing, uma, d3, dipole, g4, g5, pp-registry]
status: 수령 (1저자 붙여넣기 · 원문 그대로) → 대응 v3 커밋 c8d77dfd5 → 재리뷰 CG
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: single-source
---

> 원문 그대로 보존 (1저자가 대화에 붙여 넣은 전문 · 2026-09-27). 리뷰어가 본 대상 = 커밋 `e025c0db78754ab0d6117aff34b4e1133dd6968e`.
> 첨부: 재현 스크립트 `repro_cf.py` 는 `db/raw/codex_CF_repro_2026_09_27/repro_cf.py` 에 원문 그대로 · `results.json` 은 대화에 전문이 붙어 왔고, 여기엔 핵심 상태만 발췌했다 (§부록 — 발췌는 우리가 만든 것).
> ⚠ 리뷰어 환경에는 `simple-dftd3` 가 없어 원 selftest 82 와 돌연변이 20 은 **재현하지 않았다**고 명시했다.

## 요약 (붙여 넣은 머리글)

NO-GO — 발송 전 P0 3건·P1 3건이 남아 있어요.
`e025c0db7`을 고정해 확인했어요. 선언 해시 10개와 MANIFEST 93파일은 일치했고, 정상 합성 반송물은 18잡 OK였어요. 아래 결함은 실제 계산이 아닌 합성 반송물·가짜 VASP 실행으로 재현했어요.
필수 수정

1. P0 — 설정·PP 위반이 미수렴과 겹치면 r1이 위반을 덮어요.
[판정기:595 (line 595)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cf_e025c0db7/source/tools/wad/build_v5_vasp_package.py:595)
첫 시도 `ENCUT=400`·기대값 520에 rc≠0 또는 미수렴을 함께 넣고 정상 r1을 주면 OK예요. PP 해시 불일치도 같아요. 실행 실패로 먼저 반환하기 전에 존재하는 증거의 모순을 검사해야 해요.
2. P0 — PP 등록부 없이 최종 사용 승인이 나요.
[등록부 로더:708 (line 708)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cf_e025c0db7/source/tools/wad/build_v5_vasp_package.py:708)
등록부 옵션 생략 또는 정확한 해시를 붙인 `{}`를 공급하면 G5 PASS·usage_eligible=true·exit 0이에요. 등록 전 파일럿 검사와 최종 사용 판정을 분리하고, 후자에는 유효한 등록부를 필수화해야 해요.
3. P0 — G4의 D3 불일치가 수치수렴 실패를 가려요.
[G4 집계:797 (line 797)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cf_e025c0db7/source/tools/wad/build_v5_vasp_package.py:797)
ΔW=0.021 J/m² → FAIL인 사례에서 변형 far의 TOTEN·Edisp에 동일한 −0.0252419 eV를 넣으면, 0.019 → G4/G5 PASS로 바뀌어요. D3 편차는 0.04468%라 기존 1% 검사를 통과해요. 같은 기하인 G4에도 D3 일치 검사가 필요해요.
4. P1 — 마지막 NaN 에너지를 무시하고 앞 값을 사용해요.
[에너지 파서:500 (line 500)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cf_e025c0db7/source/tools/wad/build_v5_vasp_package.py:500)
유한 TOTEN 뒤 마지막 `TOTEN=NaN`을 넣어도 앞 에너지로 OK예요. 마지막 숫자 매치가 아니라 마지막 레코드를 선택한 뒤 유한성을 검사해야 해요.
5. P1 — 저장소의 실제 Edisp 출력 형식을 못 읽어요.
[Edisp 파서:503 (line 503)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cf_e025c0db7/source/tools/wad/build_v5_vasp_package.py:503)
실제 VASP 5.4.4의 `Edisp (eV) -28.80731`에는 콜론이 없는데, 파서는 `:`/`=`를 필수로 요구해서 `None`이 돼요. 6.x 전체의 호환성은 미확인이며, 못 읽으면 차단하는 정책 자체는 맞아요.
6. P1 — 반송 압축에 실패해도 성공 종료해요.
[배포 러너:79 (line 79)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cf_e025c0db7/source/db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh:79)
tar를 실패시키면 tgz가 없는데도 "✅ 끝"·exit 0이에요. 포장 실패를 nonzero로 반환하고 계산 재실행 없이 포장만 재시도하도록 해야 해요.

R3·R4 판단

* D3 예산: 조건부 찬성. 쌍 0.005는 총 W 인용 제한, G3 0.001 초과는 물리 FAIL이 아닌 INCOMPLETE로 두는 구분이 맞아요. 다만 G4 누락을 닫아야 하고, 이 숫자는 통계적 신뢰구간이 아닌 운영 예산이에요.
* 3b′·3c: 정의와 제한에 찬성. 잔차 진단으로 DEM을 열지 않는 것, `raw_error_criteria_met`와 사용 자격을 분리하는 것이 적절해요. 단, 사용 자격에는 PP 등록 검증도 연결해야 해요.

새 대형 계산은 해제조건이 아니에요. 82건 selftest는 로컬 `simple-dftd3` 미설치로 완주하지 못했으며, 통과했다고 주장하지 않았어요.
[전체 회신·R1–R7 답변·해제조건](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cf_e025c0db7/REVIEW_CF.md) · [재현 코드](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cf_e025c0db7/repro_cf.py) · [시험 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cf_e025c0db7/results.json)

# 회신 CF — A′ V5 VASP 외주 준비본 v2

**NO-GO — 발송 전 P0 3건과 P1 3건 수정이 필요해요.**

대상은 `e025c0db78754ab0d6117aff34b4e1133dd6968e`로 고정했어요. 실제 VASP·QE·UMA 계산, 서버 접속, 외주 제출은 하지 않았어요. 아래 수치 재현은 배포본 입력에 합성 OUTCAR·POTCAR 기록·UMA 에너지 JSON을 넣은 판정기 시험이며, 물리 실측이 아니에요. 저장소 원본은 수정하지 않았어요.

## 확인 범위

- 요청에 적힌 SHA256 10개가 모두 맞고, 승인 MANIFEST의 93파일 대조가 통과했어요.
- 배포본은 18잡이고, POSCAR 좌표는 봉인 S3v2 구조와 종 순서를 맞춰 직접 대조했어요. 좌표 최대 차이는 0 Å, 셀 최대 차이는 약 3.4×10⁻¹¹ Å였어요.
- 정상 합성 반송물은 18잡 OK, G3/G4/G5 PASS, `usage_eligible=true`, 종료 0을 재현했어요. 정상 PP 등록부를 공급해도 같아요.
- CE의 단독 결함 재현인 세미콜론 EFIELD, rc 1, 복수 실행, ENCUT 400, NELECT/Edisp/PP sha 결측, 기록 뒤 OUTCAR 교체, UMA NaN·잘못된 task는 막혔어요.
- 배포 `run_all.sh`를 Git Bash와 가짜 VASP로 직접 실행했어요. 파일럿 정상, 재실행 거부, `VASP_CMD=false`, 성능 파일 우회, 없는 성능 파일, 없는 PP, 미수렴→r1, 정상 출력+rc 1을 확인했어요.
- **82/82 selftest와 돌연변이 20/20은 이 환경에서 재현했다고 말하지 않겠어요.** 원본 selftest를 실행했지만 `simple-dftd3` 미설치로 build 단계에서 중단됐어요. 따라서 D3 기준값 자체의 재계산·패키지 재생성도 이번 확인 범위 밖이에요. 독립 시험은 봉인된 배포본의 기준값을 그대로 사용했어요.

## 발송 전 필수 수정

### P0-1. 설정·PP 위반이 실행 실패/미수렴과 겹치면 r1이 그 위반을 덮어요

위치: `tools/wad/build_v5_vasp_package.py:595` 및 `:603`, `:652`.

`check_job`이 rc/미수렴 상태로 먼저 반환하므로 뒤의 PP·설정 검사를 건너뛰어요. 이어서 `check`가 그 상태를 r1 자격으로 받아요.

실제 재현:

- 첫 OUTCAR ENCUT=400, 기대 INCAR=520, rc=1 + 정상 r1 → **OK**, `first_attempt=EXECUTION_FAILED`.
- 같은 설정 모순, rc=0, 미수렴 + 정상 r1 → **OK**, `first_attempt=SCF_NOT_CONVERGED`.
- 첫 시도 Ag sha가 봉인 등록부와 다름, rc=1 + 정상 r1 → **OK**. 이 경우에도 등록부를 실제로 공급했어요.

따라서 "무결성·PP·설정 위반은 승격 안 함"이라는 개정문이 아직 실행 경로와 달라요. 기존 시험은 이 결함들을 각각 하나씩만 넣어서 조합을 놓쳤어요.

최소 수정: **실행 상태와 증거의 모순을 별도 축으로 기록**하고, r1 채택 전에 존재하는 입력·PP·설정 증거의 모순을 우선 차단하세요. 실행 초기에 죽어서 OUTCAR가 없는 경우까지 설정 되울림을 요구하라는 뜻은 아니에요. "증거 없음"과 "있는 증거가 기대값과 모순"을 구분하면 현재의 정당한 r1 경로를 보존할 수 있어요.

### P0-2. PP 등록부를 생략하거나 빈 JSON을 줘도 최종 사용 자격이 열려요

위치: `tools/wad/build_v5_vasp_package.py:708`, `:618`, `:821`.

`load_pp_registry`는 파일 해시만 확인하고 내용을 검증하지 않아요. `None` 또는 `{}`는 `if pp_registry`를 건너뛰어요.

실제 CLI 재현:

- `--collect ... --uma ...`에서 등록부 옵션 생략 → **G5 PASS, rc 0, usage_eligible=true**.
- `--pp_registry empty.json --pp_registry_sha256 <{} 파일의 정확한 SHA>` → **동일하게 PASS**.
- 정상 등록부에서 schema를 임의 문자열로, package_manifest_sha256을 전부 0으로 바꾸고 version/assembled_sha256을 제거한 객체도 판정 함수에서는 PASS예요.

현재 통과가 보증하는 것은 "이번 반송 잡들끼리 일관적"이지 "파일럿에서 봉인한 등록부와 대조됨"이 아니에요. 뒤의 주장을 하려면 생략이 최종 PASS 경로가 되어서는 안 돼요.

최소 수정: 등록 전 **파일럿 검사만 명시적으로 예외**로 두고, 최종 collect/usage 판정에는 등록부와 고정 SHA를 필수화하세요. schema·package manifest·전체 종별/조립본 해시·버전·파일럿 두 잡의 연결정보를 검사하고, 검증한 등록부 SHA도 결과 JSON에 남기세요. `run_id`가 없어도 현재 OK 및 봉인이 가능하므로, 연결에 쓸 필드라면 결측도 차단해야 해요.

### P0-3. G4에는 D3 오차 통제가 빠져 수치수렴 실패가 PASS로 뒤집혀요

위치: `tools/wad/build_v5_vasp_package.py:797`.

G3의 D3 예산은 구현됐지만 G4는 TOTEN 차만 판정해요. G4 e70/k1/s05는 같은 POSCAR·셀·D3 설정이고, 달라야 하는 것은 전자계산의 수치 조건이에요. D3는 고정 기하 기반 항이라 이 비교에서 동일해야 해요. [VASP DFT-D3 공식 설명](https://vasp.at/wiki/DFT-D3)

실제 배포본 기준값을 쓴 재현:

1. ENCUT 변형의 ΔW=**0.021 J/m²** → G4 FAIL, G5 INCOMPLETE.
2. 그 far 잡의 TOTEN과 Edisp에 같은 **−0.0252419 eV**를 넣음. W_PBE는 그대로이고, D3 편차는 기준값의 **0.04468%**라 1% 검사는 통과해요.
3. 관측 ΔW는 **0.019 J/m²**가 되어 **G4 PASS → G5 PASS, usage_eligible=true, rc 0**이에요. 이 D3 변화에는 별도 경고도 없어요.

최소 수정: G4도 기준 잡과 같은 기하의 D3 항 일치/차이의 차이를 검사하고, 부적합이면 G4 판정과 사용 승인을 막으세요. 같은 기하라 정확히 소거되어야 하는 D3 항을 확인한 뒤 전자에너지 수치변화를 판정할 수 있어요. 새로운 대형 계산이나 문턱 상향이 필요한 수정은 아니에요.

### P1-1. 마지막 에너지가 비유한값이어도 앞의 유한값을 되살려요

위치: `tools/wad/build_v5_vasp_package.py:487`, `:500`.

정규식이 "마지막 TOTEN 레코드"가 아니라 "마지막으로 소수 숫자에 매치된 TOTEN"을 골라요. 한 실행 안에 유한 TOTEN 뒤 `free energy TOTEN = NaN eV`가 있고 종료 줄이 있는 합성 출력을 넣으면, 마지막 NaN을 무시하고 이전 **−993.6895255 eV**로 **OK**예요. 실행 기록 해시도 그 파일과 일치시켰으므로 파일 변경 검사가 대신 잡아주지 않아요.

최소 수정: 먼저 마지막 해당 레코드 전체를 고른 뒤 수치 토큰을 완전하게 해석하고 유한성을 검사하세요. NaN/Inf/별표/잘린 값이면 미검증으로 끝내고, 앞 값으로 돌아가지 마세요. E_sigma0·Edisp도 같은 원칙이 필요해요. 이 재현은 파서 음성시험이지 실제 VASP에서 해당 NaN 실패를 관측했다는 뜻은 아니에요.

### P1-2. Edisp 파서의 필수 구분자가 저장소의 실제 VASP 출력과 달라요

위치: `tools/wad/build_v5_vasp_package.py:503`, 시험 픽스처 `:873`.

파서는 `(eV)` 뒤 `:` 또는 `=`를 요구하고, 가짜 출력도 항상 `:`를 넣어요. 하지만 같은 커밋의 실제 VASP 5.4.4 출력에는 다음과 같이 찍혀 있어요.

` Edisp (eV)  -28.80731`

원자료: `db/properties/sdcp_c12_v41_partial_raw/prospective/sdcp_neutral__b00__afm2424_pm1/static/OUTCAR.gz`, 압축 해제 후 **178668행**. 실제 파서 결과는 `Edisp_eV=None`이었어요. 별도의 기존 phaseB 원출력도 같은 무구분자 형식이에요.

최소 수정: 해당 실물 형식을 지원하고 실물에서 가져온 최소 픽스처를 추가하세요. 이건 잘못된 값의 PASS가 아니라 정상 반송물의 오차단이에요. **VASP 6.x도 모두 이 형식이라고 단정하지 않아요.** 현재 업체 버전이 미정이고 구버전을 일괄 금지하지 않았으므로, 이미 확인 가능한 형식 누락은 발송 전에 고치는 편이 맞아요.

### P1-3. 반송 압축 실패를 성공 종료로 보고해요

위치: 배포 `db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh:79` 및 생성기 `tools/wad/build_v5_vasp_package.py:319`.

정상 가짜 파일럿 뒤 tar만 종료 73으로 실패시키면, **tgz가 없는데도 "✅ 끝"·exit 0**이에요. `tar ... && sha256sum ...`의 실패를 `fail`에 반영하지 않기 때문이에요. 디스크 부족이나 기록 오류에서도 같은 제어 흐름이에요.

최소 수정: 압축·해시 작성 실패를 별도 nonzero로 반환하고 완료 표시를 금지하세요. 기존 반송 묶음과 혼동하지 않게 임시 파일을 성공 시 승격하는 것도 안전해요. 이미 성공한 계산을 다시 돌리라는 처방은 아니고, **포장만 재시도**할 수 있어야 해요.

## R1–R7 판정

### R1 — CE 재현 차단

**부분 해제.** 단독 입력 결함 차단은 크게 개선됐고 실제 러너의 기존 출력 재사용 거부도 확인했어요. 그러나 P0-1의 "실패+설정/PP 위반" 조합과 P0-2의 등록부 생략이 남아 있어 전체 해제로 판단할 수 없어요.

### R2 — 해석된 설정을 읽는가

**조건부.** ENCUT의 eV 포함 줄, ISMEAR/SIGMA 쌍, ISPIN/LDIPOL/IDIPOL은 기존 실물의 설정 요약을 읽었어요. IVDW는 확인한 5.4.4 실물에서 DFTD3 요약의 값을 읽었어요. 반면 같은 실물에는 DIPOL 대입 줄 자체가 없었어요.

현재 정규식은 출력의 구획·출처를 식별하지 않으므로, IVDW/DIPOL이 다른 버전에서 입력 에코에만 있으면 그것을 해석값으로 인증할 수 없어요. **입력 에코와 해석된 설정을 구별해 기록하고**, 실제 파일럿 원문으로 출처와 형식을 확인해야 해요. VASP도 OUTCAR의 해석된 입력을 확인하라고 권고하지만, 그 말이 모든 `KEY=value` 매치의 신원을 보증하지는 않아요. [공식 INCAR 안내](https://vasp.at/wiki/INCAR)

못 읽으면 SETTINGS_UNVERIFIED/D3_UNVERIFIED로 막는 선택은 맞아요. DIPOL이 인쇄되지 않는 빌드라면, 승인 입력 + 실제 min-pos/NGZF 확인을 어떤 증거 수준으로 쓸지 명시해야 하고 `None`을 자동 통과로 바꾸면 안 돼요. 업체 VASP 6.x 원출력이 없어서 그 호환성은 **미확인**이에요.

### R3 — D3 예산

**결과 전 운영 규칙으로는 조건부 찬성**이에요. 0.005/0.001은 물리적으로 유일한 허용오차나 통계적 신뢰구간이 아니라, 등록한 문턱의 일부를 배정한 운영 예산이라고 명시하세요. V2/D3 진단을 이미 봤다는 개정 이력은 유지하면 돼요.

- 표본 쌍 0.005 초과 시 총 W 인용을 막되, 같은 Edisp를 양쪽에 쓰는 `Δ=W_PBE−W_UMA` 오차표를 남기는 대수는 맞아요. **잔차 사용 자격과 총 W 인용 자격은 별개**예요.
- G3 차이의 차이 0.001 초과를 물리 FAIL이 아니라 **INCOMPLETE**로 두는 것도 맞아요. 수치 불일치 때문에 물리 판정을 신뢰할 수 없는 상황이니까요. 합성 0.0015 입력이 G3/G5 INCOMPLETE와 usage=false로 이어지는 것을 확인했어요.
- 다만 **G4 누락(P0-3)을 먼저 닫아야 해요.** 또한 0.001 이내라도 문턱 가까운 값의 분류가 참조 D3로 바꿨을 때 불변이라는 보증은 아니에요. 예산 통과를 "참조값에 대한 오차가 0"으로 해석하지 마세요.
- VDW_RADIUS/CNRADIUS를 입력에 명시하고 외부 기준과 맞추는 방향은 맞아요. [VDW_RADIUS](https://vasp.at/wiki/VDW_RADIUS), [VDW_CNRADIUS](https://vasp.at/wiki/VDW_CNRADIUS)

### R4 — 3b′·3c

**보고량 정의와 제한에는 찬성**이에요.

3b′의 δΔ=δW_PBE−δW_UMA는 맞고, 세 G3 구조의 UMA 값이 있을 때만 별도 진단으로 쓰며 G5/DEM을 열지 않는 구분도 적절해요. G3 FAIL, 원시 Δ 기준 충족인 합성 사례에서 `raw_error_criteria_met=true`, `usage_eligible=false`, G5 INCOMPLETE, 종료 11을 확인했어요.

다만 `usage_eligible`은 지금 PP 등록 검증을 포함하지 않아서 P0-2를 고쳐야 진짜 최종 사용 자격이 돼요. 추가로 G3 FAIL과 원시 Δ FAIL이 동시에 있으면 코드 827행이 먼저 적용되어 G5 문자열은 FAIL이에요. 사용 금지는 유지되므로 별도 P0는 아니지만, 상태 우선순위를 문서와 맞추세요.

### R5 — PP·버전과 파일럿 순서

**설계는 조건부 찬성, 현재 구현은 미해제**예요. 이 18잡은 종 순서가 같고 파일럿 두 잡에 다섯 종이 모두 있으므로, 그 두 잡으로 종별·조립본 등록부를 만드는 순서는 성립해요. 파일럿 재사용도 패키지와 입력이 그대로이고 해당 결과를 봉인하면 괜찮아요.

다만 등록부 생략·잘못된 스키마를 허용하면 절차가 강제되지 않아요(P0-2). TITEL 날짜와 자체 sha는 데이터셋 간 일관성 증거이지 공개 기준 해시에 의한 PBE_54 인증은 아니라는 제한도 유지하세요. OUTCAR 버전 줄 일치는 같은 **버전/빌드 표기**의 일치이지 바이너리 전체 동일성을 입증하지는 않아요.

VDW_S6의 내장 D3 사용자 조정이 6.6.0부터라는 정정은 공식 문서와 맞아요. s6=1.0을 쓰는 이유만으로 6.6 이상을 새 필수조건으로 걸지는 않겠어요. [공식 VDW_S6](https://vasp.at/wiki/VDW_S6)

### R6 — r1·종료코드

rc 0인데 OUTCAR/OSZICAR가 없는 것을 NOT_TERMINATED로 분류하고 제한된 r1을 허용하는 정책은 가능해요. 실제 준비 실패인 없는 PP는 r1을 실행하지 않는 것도 확인했어요.

그러나 **있는 증거의 모순까지 rc/미수렴으로 덮으면 안 돼요**(P0-1). 수집기 종료코드 분리는 방향이 맞지만, 등록부 누락 PASS와 러너 포장 실패 exit 0(P1-3)을 고쳐야 자동 파이프라인에서 믿을 수 있어요.

### R7 — 문서·자원·범위

18잡·파일럿 2잡 재사용·사전등록 r1 1회라는 설명은 현재 잡 목록과 맞아요. 16.1 GB를 파동함수 몫으로 한정하고 peak RSS/시간은 파일럿에서 받는 것도 적절해요. 업체·예산 미정과 proposed 상태도 그대로 확인했어요.

MP1의 TOTEN 차를 실제 전자온도 자유에너지나 수렴된 0 K 점착에너지라고 부르지 않는 제한은 적절해요. E(σ→0)·−TS 차 병기도 유지하세요. [공식 smearing 설명](https://vasp.at/wiki/Smearing_technique)

## 선택 권고 — 추가 계산 요구 아님

- 총 W에는 문자열 W_label뿐 아니라 `total_w_citable` 같은 기계 필드를 두면 잔차 PASS와 혼동하기 어려워요.
- 실행 ID·시각을 필수로 주장할 거면 실제 스키마 검사도 넣으세요. 현재 run_id 삭제가 OK예요. ID가 있어도 모든 산출물의 일관 위조를 인증해 막는 것은 아니에요.
- 현재의 `폴더 없음 확인 → mkdir -p`는 원자적 잠금이 아니에요. 병렬 중복 제출을 지원/방어하려면 원자적 디렉터리 생성 또는 별도 lock을 쓰세요. 이번에는 경쟁 실행을 재현하지 않았으므로 실행 관측으로 세지 않았어요.
- README의 "다시 돌리려면 run/을 통째로 옮기세요"는 1회 재시도 상한과 충돌하기 쉬워요. 수동 추가 실행은 새 승인, 반송 포장 재시도는 계산 재실행 불필요라고 분리하는 편이 좋아요.
- 수치 문턱을 올리거나 V2 bridge·새 대형 계산을 재승인 조건으로 추가할 필요는 없어요.

## 재승인 최소조건

1. 존재하는 설정/PP 모순과 실행 실패를 조합한 음성시험에서 r1 승격을 막기.
2. 최종 사용 판정에 봉인 PP 등록부·스키마·패키지 결속을 필수화하기. 파일럿 예외는 명시적으로 분리하기.
3. G4 D3 불일치가 0.021→0.019처럼 판정을 뒤집는 재현을 차단하기.
4. 마지막 비유한 에너지 처리, 실물 Edisp 형식, 반송 압축 실패 종료코드를 수정하고 배포본으로 재시험하기.
5. 정상 18잡 및 정당한 r1 경로를 유지한 재생성 패키지 해시를 고정하기. 그 뒤 1저자가 개정 3 v2의 과학적 선택을 비준하기.

## 재현 자료

- `repro_cf.py`: 봉인 배포본 검사, 정상/음성 반송물, CLI, 실제 배포 Bash 러너 시험. 사용자 입력이나 제품 코드는 수정하지 않아요.
- `results.json`: 위 시험의 구조화된 결과. 합성 에너지는 물리 결과로 사용할 수 없어요.
- `inspect_real_outcar.py`, `real_outcar_parse.json`: 고정 커밋의 기존 실물 출력 형식 확인.

모두 이 회신과 같은 `review_cf_e025c0db7` 디렉터리에 있어요. 원본 작업트리의 기존 수정/미추적 상태는 변하지 않았어요.

## 부록 — results.json 핵심 상태 발췌 (우리가 뽑은 것 · 전문은 대화에 붙어 왔다)

| 시험 | 결과 (리뷰어 환경 · 커밋 e025c0db7) |
|---|---|
| declared_hashes 10 | 전부 true · manifest_files_verified 93 |
| geometry 18 | source_sha_ok · order_ok 전부 true · max_pos_diff 0 · max_cell_diff 3.36e-11 Å |
| native_selftest | not_completed — `PkgError(simple-dftd3 가 없다 …)` |
| positive · positive_sealed | G3·G4·G5 PASS · usage_eligible true · rc 0 |
| CE_direct_regressions | semicolon INPUT_MODIFIED · rc1 EXECUTION_FAILED · concat MULTIPLE_RUNS · encut400 SETTINGS_MISMATCH · nelect_absent SYSTEM_UNVERIFIED · d3_absent D3_UNVERIFIED · pp_sha_absent POTCAR_UNVERIFIED · outcar_changed ATTEMPT_MISMATCH · all_nan BLOCKED · wrong_task BLOCKED |
| bad_settings_and_rc1_rescued | **OK** (attempt r1 · first_attempt EXECUTION_FAILED) |
| bad_settings_and_nonconv_rescued | **OK** (first_attempt SCF_NOT_CONVERGED) |
| bad_pp_and_rc1_rescued | **OK** (등록부 공급 상태) |
| no_pp_registry · empty_pp_registry · invalid_registry_metadata | **G5 PASS · usage_eligible true · rc 0** |
| G4_true_021 | G4 e70 dW 0.02100 FAIL → G5 INCOMPLETE (G3 PASS · G4 FAIL) · rc 11 |
| G4_masked_by_D3 | D3 이동 −0.0252419 eV (0.0447 %) → e70 dW 0.01900 **PASS** → G5 PASS · rc 0 |
| nonfinite_final_TOTEN | **OK** (TOTEN −993.6895255 — 앞 값) |
| missing_run_id | **OK** |
| G3_D3_budget_blocks | G3 INCOMPLETE (D3 차이의 차이 0.001499) · G5 INCOMPLETE · rc 11 |
| G3_FAIL_keeps_raw_only | G3 FAIL · raw true · usage false · rc 11 |
| registry_cli | absent rc 0 · empty_with_matching_sha rc 0 (둘 다 G5 PASS) |
| runner_positive / repeat / false / badperf / rescue / rc1 / missing_perf / missing_pp | 0 / 1 / 1 / 2 / 0 / 1 / 2 / 1 (기대대로) |
| runner_tar_failure | **rc 0 · tgz 없음 · "✅ 끝"** |
