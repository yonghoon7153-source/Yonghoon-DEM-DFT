---
title: "리뷰 CG 회신 — A′ V5 VASP 외주 준비본 v3: NO-GO (P1 3 · 새 P0 없음 · S3 찬성 · S4 조건부 찬성 · S5 찬성 · 선택 권고 3)"
date: 2026-09-27
updated: 2026-09-27
tags: [review, codex, reply, adhesion, wad, prereg, vasp, outsourcing, uma, d3, dipole, g4, g5, pp-registry, packaging]
status: 수령 (1저자 붙여넣기 · 원문 그대로) → 대응 v4 → 재리뷰 CI
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: single-source
---

> 원문 그대로 보존 (1저자가 대화에 붙여 넣은 전문 · 2026-09-27). 리뷰어가 본 대상 = 커밋 `c8d77dfd599cf2a867afa7bfdd3aef4c331b0ed3` (프롬프트 CG `codex_CG_prompt_wad_aprime_v5_vasp_outsourcing_v3_2026_09_27.md`).
> 첨부: 결과 JSON 전문은 대화에 붙어 왔고 `db/raw/codex_CG_repro_2026_09_27/results_pasted.json` 에 그대로 두었다 (파일명 미상 — 리뷰어는 `repro_cg.py`/`results.json` · `focused_cg.py`/`focused_results.json` 을 말했지만 **스크립트 둘은 받지 못했다**).
> ⚠ 리뷰어 환경에는 `simple-dftd3` 가 없어 selftest 130/130 · 돌연변이 38/38 은 **재현했다고 주장하지 않는다**고 명시했다 (봉인 배포본 기준값으로 독립 시험).
> 리뷰어의 Windows 경로 링크(`C:/Users/Administrator/Documents/Codex/...`)는 리뷰어 쪽 스냅샷이다 — 이 저장소 경로가 아니다.

## 붙여 넣은 머리글

NO-GO — 보내기 전 P1 3건 수정이 필요해요. 새 P0는 확인하지 못했어요.
`c8d77dfd5`를 고정해 직접 재현했어요. CF의 기존 실패 사례는 막혔지만, 아래 세 경로가 남아 있습니다.
필수 수정
1. P1 — 실패 시 POTCAR 본문이 반송 압축에 들어가요
[run_all.sh (line 20)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cg_c8d77dfd5/source/db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh:20)
`pack()`은 `run/` 전체를 압축하지만 POTCAR 삭제는 정상 실행 후 경로에만 있어요.

* Li_sv를 조립한 뒤 다음 P 파일이 없어 중단되면, 부분 POTCAR 본문이 압축에 포함됩니다.
* 중단된 실행 폴더에 POTCAR가 남은 상태에서 `PACK_ONLY=1`을 실행하면 rc=0·성공 안내와 함께 POTCAR가 포함됩니다.

합성 POTCAR로 배포 러너를 실행해 확인했어요. 포장 단계 자체에서 POTCAR를 제외하고, 준비 실패·PACK_ONLY 양쪽에서 압축 구성원을 검사해야 합니다.
2. P1 — 봉인한 파일럿과 다른 실행도 최종 PASS예요
[build_v5_vasp_package.py (line 817)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cg_c8d77dfd5/source/tools/wad/build_v5_vasp_package.py:817)
`from_pilot`의 형식은 검사하지만, 최종 채택한 파일럿의 `run_id`와 같은지는 검사하지 않아요.
봉인 등록부와 고정 SHA는 그대로 두고, 반송 파일럿의 ID를 다음 날 실행 ID로 바꿨습니다. 실제 CLI 결과는 rc=0 · G5 PASS · usage_eligible=true였어요.
최소 수정은 두 파일럿 각각의 채택 시도 ID = 봉인 ID 대조입니다. 등록부를 도구 밖에서 커밋·해시 봉인하는 절차 자체는 괜찮아요. 다만 지금은 PP·버전 일치까지만 확인하며, 봉인 파일럿 재사용까지 확인하지는 않습니다.
3. P1 — 정상 TITEL 일부만 찍힌 조기 종료를 모순으로 오판해요
[build_v5_vasp_package.py (line 751)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cg_c8d77dfd5/source/tools/wad/build_v5_vasp_package.py:751)
정상 POTCAR 기록은 모두 있고, OUTCAR에 올바른 첫 TITEL만 찍힌 뒤 rc=1인 상황을 만들었습니다. 정상 r1을 붙여도 POTCAR_MISMATCH · r1_ignored였어요.
미완료 출력에서 기대 목록의 정상 접두 부분만 관측된 것은 결측이지 모순은 아닙니다. 반면 다른 종·날짜·순서는 계속 차단해야 해요. 모순 검사를 단순히 rc 뒤로 옮기면 CF 결함이 재발합니다.
S3·S4·S5 판정

* S3 — 찬성. 고정 기하·같은 D3 설정에서 k/ENCUT/σ만 바꿨다면 D3는 같아야 합니다. `1e-4 eV`는 이 면적에서 끝점당 약 7.92×10⁻⁶ J/m²로, 인쇄 오차 여유를 둔 운영 문턱으로 적절해요. 구조 이완이나 다른 분산 모델까지 일반화하면 안 됩니다. [VASP DFT-D3 설명](https://vasp.at/wiki/DFT-D3)
* S4 — 조건부 찬성. `min pos / NGZF`를 cut 위치 증거로 쓰는 것은 공식 개발자 설명과 맞습니다. ±2 격자는 운영 허용치이지 0/1 인덱싱을 확인했다는 증명은 아니에요. 예정된 파일럿에서 실제 격자·cut·편차를 기록하세요. 전자밀도 검증을 대신하지도 않습니다. [공식 cut 설명](https://vasp.at/forum/viewtopic.php?p=30185&sid=8dc8416efa5c83885d72db5f9312640a)
* S5 — 찬성. 최종 `FREE ENERGIE` 구획으로 제한하는 방향은 맞아요. 공식 튜토리얼도 같은 구획을 사용합니다. 다만 업체의 모든 6.x 빌드를 확인한 것은 아니므로, 미인식 → 미검증 → 파일럿 원문으로 파서만 적응하는 정책을 유지하세요. [공식 튜토리얼](https://vasp.at/tutorials/latest/molecules/part1/)

확인 범위와 해제조건
파일 해시 12개·MANIFEST 93파일을 확인했고, CF→CG 계산 입력 90개와 D3 기준값도 불변이었어요. 기존 G4 뒤집힘·등록부 생략·NaN·tar 실패 재현은 차단됐고, 정상 대조군과 정당한 r1은 통과했습니다.
`simple-dftd3` 설치가 완료되지 않아 selftest 130/130·돌연변이 38/38은 재현했다고 주장하지 않습니다. 봉인 배포본 기준값으로 독립 시험했어요.
위 P1 세 경로를 수정·재시험하고 배포본과 결속 해시를 갱신하면 됩니다. 새 대형 계산이나 물리 문턱 변경은 요구하지 않아요. 실행은 이후에도 1저자 비준이 별도로 필요합니다.
[전체 회신·S1–S6·선택 권고](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cg_c8d77dfd5/REVIEW_CG.md) · [집중 재현 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cg_c8d77dfd5/focused_results.json)

## 회신 CG 본문 (REVIEW_CG.md · 원문)

# 회신 CG — V5 VASP 외주 준비본 v3 재리뷰

**NO-GO — 보내기 전 P1 3건을 고쳐야 합니다. 새 P0는 확인하지 못했습니다.**

대상은 `c8d77dfd599cf2a867afa7bfdd3aef4c331b0ed3`입니다. CF의 원래 재현 사례들은 차단됐습니다. 이번 NO-GO는 그 수정들을 부정하는 판정이 아니라, 아래 세 경로에 한정합니다. 실제 VASP/QE/UMA 계산, 서버 작업, 제출, 대상 코드 수정은 하지 않았습니다.

## 1. 보내기 전 필수 수정

### P1-1. 실패 경로에서 POTCAR 본문을 반송 압축에 넣습니다

위치: [배포 run_all.sh:20](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cg_c8d77dfd5/source/db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh:20), 같은 파일 62–66·81행. 생성기 안의 동일 구현은 `RUN_ALL`, 311행입니다.

`pack()`은 `run/` 전체를 압축하지만, POTCAR 삭제는 `run_one()`의 정상적인 실행 후 경로에만 있습니다.

실제 배포 러너를 합성 POTCAR로 실행한 재현:

- Li_sv만 있고 두 번째 P 파일이 없는 PP 트리 → Li_sv 본문을 조립한 뒤 `return 3` → 마지막 포장은 수행 → `run/V5_s_outer_A_bound/POTCAR`가 압축에 포함됐습니다. rc=1이며 러너는 실패도 그대로 반송하라고 안내합니다.
- 실행 중단 뒤를 모사해 `run/<job>/POTCAR`와 WAVECAR를 남기고 `PACK_ONLY=1` → rc=0, 성공 안내, 두 파일 모두 반송물에 들어갔습니다.

이는 README의 **POTCAR 본문 반송 금지**와 직접 충돌합니다. 실제 라이선스 파일은 사용하지 않았습니다.

최소 수정: 포장 단계 자체에서 허용 파일만 수집하거나 POTCAR·WAVECAR·CHGCAR 등 제외 대상을 강제하세요. 정상 실행 후 삭제에만 의존하면 안 됩니다. 압축 구성원 목록을 확인하는 음성시험을 준비 실패와 PACK_ONLY 양쪽에 넣으세요. 원본 PP 트리를 삭제하라는 뜻이 아닙니다.

### P1-2. 봉인한 파일럿의 run_id를 최종 파일럿과 대조하지 않습니다

위치: [build_v5_vasp_package.py:817](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cg_c8d77dfd5/source/tools/wad/build_v5_vasp_package.py:817), `check()` 833–845행.

등록부의 `from_pilot`은 형식만 검증합니다. 최종 선택된 파일럿 시도의 `run_id`와 같다는 검사는 없습니다.

재현: 정상 18잡에서 `seal_pp()`로 등록부를 만들고 **그 등록부와 고정 해시는 그대로 둔 채**, 반송된 far 파일럿의 실행 ID를 `20260927T120000-42-123`에서 `20260928T120000-99-456`으로 바꿨습니다. 시간 필드도 유효하게 두었습니다. 실제 CLI `--collect --pp_registry ... --pp_registry_sha256 ...` 결과는 **rc=0 · G5 PASS · usage_eligible=true**였습니다.

이 검사는 같은 PP·버전이라는 사실은 보증하지만 **봉인했던 파일럿을 재사용했다는 사실은 보증하지 않습니다**. 다른 폴더에서 재실행한 파일럿이 돌아오는 실수를 검출하지 못합니다. 전체 위조 방어를 요구하는 것이 아닙니다.

최소 수정: 두 파일럿 각각에서 최종 채택한 시도(0 또는 허용된 r1)의 `run_id == registry.from_pilot[job]`를 요구하세요. 다르면 자동 교체하지 말고 새 승인 대상으로 막으세요. 봉인 당시 attempt/OUTCAR 해시도 함께 남기면 같은 ID 아래 파일이 교체되는 사고까지 대조할 수 있습니다.

### P1-3. 올바른 TITEL 일부만 기록된 조기 종료를 모순으로 오판합니다

위치: [build_v5_vasp_package.py:751](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cg_c8d77dfd5/source/tools/wad/build_v5_vasp_package.py:751).

`outcar_titel`이 비어 있지 않으면 전체 목록과의 불일치를 곧바로 POTCAR_MISMATCH로 처리합니다. 그러나 출력이 중간에 끊겼다면 짧은 목록은 결측이지 반드시 모순은 아닙니다.

재현: POTCAR 기록 세 파일은 완전·정상이고 OUTCAR에는 버전 줄과 올바른 첫 TITEL `PAW_PBE Li_sv 10Sep2004`만 남긴 뒤 rc=1. 정상 r1을 붙여도 **POTCAR_MISMATCH · r1_ignored · r1_status=OK**였습니다.

대조군도 실행했습니다. TITEL 없이 버전/ENCUT=520만 남긴 rc=1은 정상 r1로 승격됐습니다. ENCUT=400 또는 잘못된 Fe TITEL은 모순으로 차단됐습니다. 문제는 **정상 목록의 일부만 보이는 경계**입니다.

최소 수정: 실패·미완료 시도에서 관측된 완전한 TITEL들이 기대 순서의 정상 접두 부분이면 미관측 나머지와 실제 모순을 구분하세요. 다른 종·다른 날짜·틀린 순서는 계속 즉시 차단하고, 성공 시도의 TITEL 결측은 계속 미검증으로 막아야 합니다. 단순히 모순 검사를 rc 뒤로 되돌리면 CF P0-1이 재발합니다.

## 2. CF 수정 확인 및 검증 범위

- 프롬프트의 파일 해시 12개가 커밋 실물과 모두 일치했습니다.
- MANIFEST의 배포파일 93개 검증을 통과했습니다.
- CF→CG의 INCAR/INCAR.r1/POSCAR/KPOINTS/POTCAR.spec 90개와 D3 기준값은 불변입니다.
- S3v2→POSCAR 18개에서 종별 재정렬·좌표·원본 해시를 확인했습니다. 좌표 차이는 0, 셀 텍스트 반올림 차이는 최대 약 3.4e-11 Å였습니다.
- ENCUT=400 + rc=1/미수렴 + 정상 r1, 다른 Ag PP + rc=1 + 정상 r1은 이제 차단됩니다.
- 등록부 없음 또는 해시만 맞는 빈 등록부의 최종 CLI 집계는 rc=2입니다. 파일럿 집계는 사용 자격을 열지 않습니다. 정상 등록부·정상 18잡의 합성 대조군은 G3/G4/G5 PASS입니다.
- G4의 원래 실패 ΔW=0.021 J/m²를 D3/TOTEN 동시 이동으로 0.019로 보이게 만든 재현은 이제 G4 INCOMPLETE·usage_eligible=false·rc=11입니다.
- 최종 NaN/Inf/별표 및 최종 FREE ENERGIE 구획 부재는 ENERGY_UNPARSEABLE입니다.
- 실물 5.4.4 OUTCAR.gz 전체에서 TOTEN=-1151.29778848, E(σ→0)=-1151.29228248, Edisp=-28.80731 eV를 읽었습니다. NGZF는 dimension의 560이며 support grid의 1120이 아닙니다. min pos=520도 일치했습니다. 이는 다른 SDCP 계의 **파서 검증용 자료**이지 V5 결과가 아닙니다.
- 배포 bash 러너를 가짜 VASP로 실행했습니다. 정상 실행·재실행 거부·실패·정당한 r1·성능파일 거부·tar 실패 rc=4를 확인했습니다. PACK_ONLY 복구는 rc=0이며 기존 시도/출력 파일 해시는 바뀌지 않았습니다.

한계: Python `dftd3`가 없어 원래 `--selftest`는 합성 build 단계에서 중단됐습니다. 설치 시도도 완료되지 않아 **130/130과 돌연변이 38/38은 이번 환경에서 재현했다고 주장하지 않습니다**. 프롬프트가 허용한 대로 봉인 배포본의 D3 기준값을 사용해 판독·판정·러너를 독립 검증했습니다. 이 환경 제약 자체를 제품 결함으로 세지 않았습니다.

## 3. S1–S6 답변

### S1 — 원래 재현은 차단, 결측과 모순의 경계는 일부 남음

CF 원래 재현은 수정됐습니다. 다만 P1-3의 정상 TITEL 접두 부분을 미완료 출력에서 다르게 취급해야 합니다. 증거가 전혀 없는 경우와 잘못된 증거가 있는 경우의 대조군은 기대대로 동작했습니다.

### S2 — 등록부 외부 봉인은 허용, 소비 시 파일럿 결속 보강 필요

등록부를 도구 밖에서 커밋하고 SHA를 고정하는 절차는 괜찮습니다. CLI가 그 SHA·schema·패키지·PP·버전을 필수 대조하는 설계도 맞습니다. 다만 P1-2 때문에 현재 표현은 **PP/버전 신원 대조**까지이며 **봉인 파일럿 재사용 검증**까지는 아닙니다. 두 가지를 혼용하지 마세요.

### S3 — 같은 기하 D3 차 1e-4 eV: 찬성

고정 원자종·좌표·셀·PBE-BJ 계수·절단·구현에서 2체 D3는 기하에 의해 정해집니다. k/ENCUT/σ만 바꾸는 이 G4에서는 D3가 달라질 물리적 이유가 없습니다. 전자밀도에 의존하는 다른 분산 모델이나 구조 이완까지 같은 논리를 확장하면 안 됩니다. [VASP DFT-D3 공식 설명](https://vasp.at/wiki/DFT-D3)

이 패키지 면적 202.209896 Å²에서 1e-4 eV는 끝점당 약 **7.92e-6 J/m²**, 두 끝점 반대 방향의 최악 차이는 **1.58e-5 J/m²**입니다. G4 0.02 J/m² 문턱보다 충분히 작습니다. 인쇄 5자리의 양자화 오차보다 여유를 둔 운영 허용치로 적절하며, 신뢰구간이라는 뜻은 아닙니다. 위반 시 문턱을 늘리지 말고 설정·절단·구현·기하 차이를 점검하는 현재 방향에 찬성합니다.

### S4 — min pos/NGZF 둘째 길: 제한된 해석값 증거로 조건부 찬성

공식 개발자 설명도 IDIPOL=3에서 NGZF를 사용하고 DIPOL 중심에 반 셀을 더한 위치를 cut으로 설명합니다. 또 dimension 줄의 격자를 사용하라는 공식 답변이 있습니다. 따라서 이번 해석은 실물 한 건의 우연한 맞춤만은 아닙니다. [cut 알고리즘 설명](https://vasp.at/forum/viewtopic.php?p=30185&sid=8dc8416efa5c83885d72db5f9312640a), [dimension 격자 설명](https://vasp.at/forum/viewtopic.php?t=19849)

**±2 격자는 위치 일관성 검사의 운영 여유로 허용합니다. 0/1 인덱싱이 확인됐다는 증명은 아닙니다.** 파일럿에서 실제 버전·NGZF·min pos·기대 cut·격자 단위 편차를 남기고 의미를 확인하세요. 이미 예정한 두 파일럿에서 할 일이며 새 계산 요구가 아닙니다. 불명확한 새 형식은 미검증으로 막고 문서화된 파서 적응 절차를 쓰면 됩니다.

이 검사가 전자밀도가 cut에서 충분히 작음을 보증하지는 않습니다. 핵-구간 여유 4 Å와 전자밀도 검증은 별개라는 기존 제한을 유지하세요. [DIPOL 공식 문서](https://vasp.at/wiki/DIPOL)

### S5 — 최종 FREE ENERGIE 구획: 찬성, 6.x 모든 빌드 검증 완료 주장은 금지

SCF 중간 값과 최종 에너지를 구분하는 방향은 맞습니다. 현재 공식 튜토리얼도 같은 최종 헤더 아래 TOTEN·무엔트로피·σ→0 값을 설명합니다. 실물 5.4.4에서도 D3가 들어간 최종 에너지를 정확히 읽었습니다. [VASP 공식 튜토리얼](https://vasp.at/tutorials/latest/molecules/part1/)

이번 검증만으로 업체 VASP 6.x 모든 빌드를 시험했다고 할 수는 없습니다. **헤더가 안 맞으면 미검증 → 실제 파일럿 출력으로 파서만 적응**하는 정책은 적절합니다. 그 때문에 지금 대형 계산을 추가할 필요는 없습니다. 임의의 마지막 숫자나 SCF 중간 값으로 fallback하지 마세요.

### S6 — 재실행·포장·정책

수동 재실행은 새 승인, 포장만 재시도는 계산 없음이라는 분리는 맞습니다. tar 실패가 rc=4로 전달되는 수정도 확인했습니다. 다만 P1-1처럼 **포장 대상 파일 자체**를 제한해야 업체에 보낼 수 있습니다.

개정 3과 결정문은 여전히 proposed입니다. 리뷰를 통과해도 1저자의 비준·업체/예산 확정·파일럿 확인·PP 등록부 봉인을 대신하지 않습니다. 파서 적응 시 기대값·문턱·상태 순서를 유지하고 변경 SHA/시험 근거를 남긴다는 정책에는 찬성합니다.

## 4. 선택 권고 — 새 필수조건으로 확대하지 않음

1. **빈 최종 에너지 레코드 처리.** 603–605행의 `\S+` 때문에 정상 종료 출력 뒤 EOF에 `free energy TOTEN =`만 덧붙인 비정상 파일에서는 그 빈 레코드를 건너뛰고 앞 에너지를 사용합니다. σ→0·무엔트로피도 동일했습니다. 재현된 파서 경계 결함이지만, 이번 시험은 정상 footer 뒤에 불완전 중복 레코드를 붙인 합성 상태이며 실제 단일점 출력에서 관측한 것은 아닙니다. 새 P0/P1로 과장하지 않습니다. 레코드 존재와 값 파싱을 분리해 빈 값도 마지막 레코드로 취급하는 보강을 권합니다.
2. **본문·해시 쌍 포장 승격.** 현재 tar는 SHA 계산 전에 최종 파일명으로 승격됩니다. SHA 단계 실패를 rc=4로 알리므로 조용한 성공은 아니지만, 기존 파일이 있으면 새 tar/옛 SHA가 한때 공존할 수 있습니다. 두 임시 파일이 완성된 뒤 승격하는 편이 좋습니다.
3. **등록부 증거 확장.** `from_pilot` ID 대조는 필수(P1-2), 추가로 봉인한 attempt.json/OUTCAR 해시를 기록·대조하는 것은 저비용 강화입니다. 외부 서명 체계나 VASP 바이너리 전체 인증을 새로 요구하지 않습니다.

## 5. 해제조건

1. 정상·준비 실패·PACK_ONLY 모두에서 반송 압축에 POTCAR 본문이 포함되지 않을 것. 실제 압축 구성원 검사로 입증할 것.
2. 봉인 등록부와 최종 채택 파일럿 run_id 불일치를 실제 CLI에서 차단할 것. 정상 파일럿/r1 재사용 양성 경로는 유지할 것.
3. 미완료 OUTCAR의 정상 TITEL 접두 부분은 결측, 잘못된 종·순서는 모순으로 구분할 것. 정상 r1은 살리고 CF의 설정/PP 모순 세탁 경로는 계속 막을 것.

위 세 수정 후 생성기와 배포 run_all.sh를 함께 갱신하고 MANIFEST·개정 결속 해시를 재생성하세요. 물리 보고량·표본·G3/G4/G5 문턱을 바꾸거나 새 대형 계산을 추가할 필요는 없습니다.

## 재현물

- `repro_cg.py` / `results.json`: CF 회귀, 정상 대조군, 실물 OUTCAR, 배포 러너, PACK_ONLY.
- `focused_cg.py` / `focused_results.json`: P1 세 건 및 선택 권고의 집중 재현, CLI 포함.
- 합성 계산 폴더는 시험 종료 시 삭제됐습니다. 대상 커밋 스냅샷과 재현 코드/결과만 이 리뷰 폴더에 보관했습니다. 원본 작업 트리의 기존 변경은 그대로입니다.

## 부록 — 붙여 온 결과 JSON (핵심 상태 발췌 · 전문은 `db/raw/codex_CG_repro_2026_09_27/results_pasted.json`)

| 항목 | 리뷰어 결과 (c8d77dfd5) |
|---|---|
| declared_hashes 12 · manifest_files_verified | 전부 true · 93 |
| geometry 18 잡 | source_sha_ok · max_pos_diff 0 · max_cell_diff 3.36e-11 Å · order_ok |
| native_selftest | 미완료 — `PkgError("simple-dftd3 가 없다 …")` |
| header_only · partial_expected_setting | OK (정상 r1 승격 · first_attempt EXECUTION_FAILED) |
| partial_bad_setting (ENCUT 400) | SETTINGS_MISMATCH · r1_ignored |
| **partial_correct_titel** (Li_sv 하나만 · rc 1) | **POTCAR_MISMATCH · r1_ignored · r1_status OK** ← P1-3 |
| partial_wrong_titel (Fe) | POTCAR_MISMATCH · r1_ignored (기대대로) |
| **pilot_replaced_after_seal / pilot_replaced_cli** | **rc 0 · G5 PASS · eligible true** ← P1-2 |
| empty_eof_TOTEN / sigma0 / noentropy | OK (앞 값 사용) ← 권고 1 |
| **runner_partial_pp_archive** | rc 1 · 압축에 `run/V5_s_outer_A_bound/POTCAR` (부분 본문) ← P1-1 |
| **pack_only_interrupted_leak** | rc 0 · 구성원에 `run/V5_s_outer_A_far/POTCAR` · `WAVECAR` ← P1-1 |
| CF_physical_input_comparison | files 90 · all_equal · D3_equal |
| D3_tolerance_units | area 202.209896 Å² · 1e-4 eV = 7.92e-6 J/m² (끝점) · 1.58e-5 (최악 쌍) |
