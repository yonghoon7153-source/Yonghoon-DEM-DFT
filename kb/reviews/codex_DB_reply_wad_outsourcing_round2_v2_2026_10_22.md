---
title: "DB 회신 — W_ad 외주 2차 묶음 v2 (3d684e502 · MANIFEST b9450f6f…): NO-GO · 발송 보류 · P0 1 (시도 열거 — INCAR·attempt.json 없는 실행 흔적이 감사에서 빠짐) · P1 3 (불완전 시도의 커널 부정 증거 · KERNEL_UNVERIFIED 가 다른 결측을 가려 봉인 · 수동 초의 선행 0 = 8진수) · 해제 최소조건 넷"
tags: [review, wad, adhesion, vasp, outsourcing, runner, checker, codex, reply, letter]
letter: DB
date: 2026-10-22
track: wad
channel: codex
kind: reply
status: 수령 2026-10-22 (사용자 붙여넣기 · 원문 보존 · 마크다운 링크의 Codex 로컬 경로만 파일 이름·행으로 줄임 · 붙여넣기 첫 줄이 'O —' 로 시작 — 앞 글자가 잘린 듯 · 판정은 본문대로 NO-GO · 첨부 셋은 구분선과 코드 울타리만 더함)
confidence: medium
verificationStatus: verified
verifiedAt: 2026-10-22
verifiedBy: self
explored: false
authoredBy: external
claimType: mixed
evidenceScope: multi-source-primary
---

> 프롬프트: `codex_DB_prompt_wad_outsourcing_round2_v2_2026_10_22.md` (기준 커밋 `3d684e502`) · 트랙 W_ad (1저자 = 사용자). 아래는 원문이다 (고치지 않는다 · W 숫자 없음).

---

O — 현재 v2는 발송 보류입니다. P0 1건과 P1 3건이 남았습니다.
검토 대상은 3d684e502이고, MANIFEST SHA b9450f6f…가 첨부 요청과 일치했습니다. 기존에 승인한 설계·구조 봉인·집계 산식·optB88 입력 조합은 다시 열지 않았습니다.
이번 수정은 대부분 작동합니다. 남은 핵심은 “모든 시도를 감사한다”는 선언이 파일 일부가 빠진 반송에서도 성립하느냐, 그리고 등록부 봉인과 비용 제한이 예외 경로에서도 닫혀 있느냐입니다.
1. 발송 전에 남은 네 건
P0-1. 실행 흔적이 남아 있어도 INCAR와 attempt.json이 없으면 시도 전체가 감사에서 사라집니다
위치: [build_round2_vasp_package.py (line 1355)](build_round2_vasp_package.py:1355), _started() → resolve_job()의 시도 열거.
_started()는 INCAR 또는 attempt.json만 봅니다. 새로 도입한 attempt.start와 실제 OUTCAR는 시작 증거로 쓰지 않습니다.
재현했습니다.
1. 합성 반송에서 24잡이 모두 정상 판정되는 기준 상태를 만들었습니다.
2. 미채택 r1A에 다른 VASP 빌드의 OUTCAR를 넣으면 정상적으로 VERSION_MISMATCH와 전역 환경 고장이 나옵니다.
3. 그 r1A에서 INCAR와 attempt.json 두 파일만 제거했습니다. attempt.start, OUTCAR, stdout, PP 기록, OSZICAR는 남겼습니다.
4. 이제 그 시도는 감사 대상에서 빠집니다.
실제 검사 명령의 결과:
--check       → exit 0
--a4_result   → result=OK, common_environment_failure=None
합성 UMA 입력으로 집계의 상태 전파만 시험했을 때도 G5_C=PASS, 종료 0이었습니다. 실제 UMA 자료는 사용하지 않았습니다.
이는 단순히 “파일이 없어서 판정 불가”가 아닙니다. 남아 있는 다른 빌드의 실행 증거를 보지 않고 정상이라고 하는 경로입니다.
최소 수정: 알려진 시도 위치에서 attempt.start, OUTCAR, OSZICAR, stdout, killed.json 등 실행 흔적이 하나라도 있으면 감사 대상으로 포함하세요. 필수 메타데이터가 없으면 불완전 시도로 남기고, 원문 환경 증거는 계속 감사해야 합니다. 단, B 폴더가 A의 부모라는 이유로 폴더 존재만으로 B 실행을 인정해서는 안 됩니다.
P1-1. 불완전 시도의 커널 재생성 증거는 전역 환경 감사에 전달되지 않습니다
위치: [build_round2_vasp_package.py (line 1036)](build_round2_vasp_package.py:1036), env_evidence().
무결성 검사 전에 읽는 것은 버전·PP 해시·커널 해시입니다. 커널을 읽지 못했거나 재생성했다는 원문 증거는 여기에서 읽지 않습니다.
독립적으로 재현했습니다.
- optB88의 미채택 r1A에 INCAR와 실행 흔적을 남깁니다.
- stdout에 kernel differs, recalculating vdW kernel을 넣습니다.
- attempt.json이 없는 중단 상태로 만듭니다.
결과는 다음과 같습니다.
해당 시도     → INCOMPLETE_ATTEMPT
전역 환경 고장 → 없음
--a4_result   → result=OK, common_environment_failure=None
불완전한 optB88 잡 자체가 정상 에너지로 채택된다는 뜻은 아닙니다. 그러나 코드가 선언한 **“어느 시도든 KERNEL_NOT_READ이면 전체 정지”**는 지켜지지 않습니다.
최소 수정: optB88 시도의 명확한 커널 부정·재생성 증거도 env_evidence()에 보존하고, env_audit()가 완결성 검사 결과와 무관하게 전역 정지로 올리세요. 여기에서도 긍정 문구로 불완전 시도를 정상 승격해서는 안 됩니다.
P1-2. KERNEL_UNVERIFIED가 다른 필수값 결측을 가려 등록부 봉인을 허용합니다
위치: [build_round2_vasp_package.py (line 1300)](build_round2_vasp_package.py:1300), check_attempt(); [봉인 검사:1787 (line 1787)](build_round2_vasp_package.py:1787).
현재 순서는 다음과 같습니다.
커널 읽기 미확정 → KERNEL_UNVERIFIED로 반환
그 뒤에 TITEL·NIONS·NELECT·설정·에너지 완결성 검사
등록부 전에는 optB88이 의도적으로 KERNEL_UNVERIFIED이고, 봉인은 이 상태를 허용합니다. 따라서 뒤의 다른 결측까지 같이 가려집니다.
재현: 정상 합성 optB88 OUTCAR에서 해석 GGA 줄, PARAM1 줄, TITEL 줄을 각각 제거하고 실행 기록의 해시를 맞췄습니다. 세 경우 모두 등록부 전에는 KERNEL_UNVERIFIED, 정상 커널 긍정 문구를 지정한 seal_registry()는 봉인을 허용했습니다.
봉인 후 검사에서는 SETTINGS_UNVERIFIED 또는 POTCAR_UNVERIFIED로 잡힙니다. 따라서 잘못된 에너지의 최종 채택까지 확인한 결함은 아니지만, “그 밖 결측은 봉인을 거부한다”는 본배치 해제 계약은 위반합니다.
최소 수정: 커널 확인 대기와 다른 결측을 독립적으로 보존·판정하세요. 가장 작은 수정은 필수 완결성 검사 뒤에 KERNEL_UNVERIFIED를 반환하는 것입니다. A에 허용한 결측 예외를 일반 optB88 측정 시도까지 넓히면 안 됩니다.
P1-3. 수동 입력한 시간이 선행 0을 가지면 비용 상한을 우회합니다
위치: [실제 배포 run_all.sh:336 (line 336)](run_all.sh:336), wall_s_of(); [cap_ok():343 (line 343)](run_all.sh:343).
--infra-abort, --infra-wall, --killed는 [0-9]+를 허용하고 그대로 저장합니다. 합산은 Bash 산술입니다.
tot=$((tot + w))
따라서 허용된 입력 0007200은 7,200초가 아니라 8진수 7200, 즉 3,712초로 계산됩니다. 1.5시간 상한이라면 막아야 할 다음 잡을 허용합니다. Bash의 선행 0 해석은 GNU 공식 문서에 명시돼 있습니다.
08은 산술 오류를 일으킵니다. 그런데 cap_ok()는 합산 명령의 실패나 빈 결과를 별도로 거부하지 않습니다.
최소 수정:
- 세 입력 경로에서 10진수로 정규화하거나 선행 0을 거부.
- cap_ok()에서 합산 명령 실패·빈 결과·비숫자를 모두 UNKNOWN으로 처리.
- 유효한 0초는 그대로 허용.
이 건은 코드와 Bash 산술 규칙으로 확인한 결함입니다. 이 환경에서는 Bash 실행이 제한되어 격리 셸 재현까지 완료했다고 주장하지 않습니다.
2. Q-DB-1∼7 판정
질문	판정	확인 결과
1. 확정 모순 우선 차단	GO	Python 판정 탐침 41개와 독립 경계 시험 6개가 기대대로 동작했습니다. 확정 모순과 미종료 출력 결측을 구분합니다.
2. A→B 결박·재시작 규칙	GO	A 기록 부재·다른 WAVECAR 해시·봉인 문구 불일치를 거부합니다. A 머리와 실제 OUTCAR 대조도 연결됐습니다.
3. 모든 시도 환경 감사·봉인	NO-GO	기존 재현들은 닫혔지만, 위 P0-1·P1-1의 감사 누락과 P1-2의 봉인 조기 통과가 남습니다.
4. GGA·커널 판정	조건부	GGA 불일치와 정상적으로 읽힌 시도의 커널 부정·재생성은 잡습니다. 불완전 시도와 봉인 전 결측 처리에는 위 수정이 필요합니다.
5. 중단·미상 비용	NO-GO	UNKNOWN 보류와 복구 절차는 맞습니다. 수동 시간의 10진수 처리와 합산 실패 차단이 필요합니다.
6. 반송·의존성·진단·NaN	GO	열거 오류 전달, δ의 PBE 의존성, 채택 진단 표시, 미평가 구분, 비유한 좌표 거부가 반영됐습니다.
7. 재생성·묶음 검증	실물 GO / 전체 시험은 확인 제한	MANIFEST의 170개 항목 일치. 입력 변경은 지정 INCAR 네 개의 LVHAR뿐. 기록된 D3 값을 재사용한 빌드 재생은 전체 172개 파일이 바이트 일치했습니다. Linux 전체 시험은 여기서 재실행하지 못했습니다.


“실물 GO”는 지정한 소스와 묶음이 일치한다는 뜻이지, 그 소스에 남은 결함까지 승인한다는 뜻은 아닙니다.
3. Q-DB-8 — 여덟 이탈
① regex 문자 제한: 찬성.
구절을 확인하는 목적에는 제한된 문법과 두 엔진의 파일럿 대조가 적절합니다. 다만 restart_regex_problems("reading WAVECAR\n")가 통과하는 작은 누락은 있습니다. 마지막 LF까지 금지하려면 fullmatch()로 닫으세요. 별도의 false OK를 입증한 것은 아니므로 P2입니다.
② vdW+kernel 줄로 좁히기: 조건부 찬성.
OS 커널 경고를 배제하는 방향은 맞습니다. 하지만 “vdW 없는 부정문을 놓쳐도 긍정 문구가 없으므로 항상 KERNEL_UNVERIFIED”라는 설명은 일반적으로 성립하지 않습니다. 긍정과 부정이 함께 있으면 현재는 긍정이 이길 수 있습니다.
실제로 VASP 공식 포럼에는 **No kernel file found**라는 출력 사례가 있습니다. 이 문구에는 vdW가 없습니다. 해당 원문
긍정 문구와 이 부정문을 함께 넣은 합성 입력은 현재 OK가 됩니다. 다만 업체의 5.4.4에서 두 문구가 실제로 함께 나오는지는 미확인입니다. 따라서 별도 확정 P0로 올리지는 않습니다.
권고는 모든 kernel 줄을 다시 잡는 것이 아니라, 확인된 VASP 부정문을 좁은 예외 패턴으로 추가하는 것입니다. 넓은 comput*, writ* 등이 실제 긍정 설명문에 걸릴 위험도 있으므로 파일럿 원문 확인은 필요합니다.
파서만 고치는 방침은 가능합니다. 단, 원문을 보존하고 관련 파일럿 전체를 새 파서로 재검사한 뒤 등록부·해제 파일의 계보를 갱신해야 합니다. 경보 하나를 없애고 종전 봉인을 그대로 쓰는 것은 부족합니다.
③ “25 executions when nothing fails”: 찬성.
A가 자격 미달이면 B가 생략되므로 “at least 25”보다 정확합니다.
④ run_aborted까지 감사: 찬성.
전자 스텝이 없더라도 빌드·PP 모순은 환경 문제입니다. 값 채택과 환경 정지를 분리한 것이 맞습니다.
⑤ A의 일부 결측을 봉인에서 허용: 조건부 찬성.
WAVECAR 전달에 필요한 A 자격을 충족한다면 최종 에너지용 결측과 구별할 수 있습니다. 다만 위 P1-2처럼 일반 측정 시도의 결측까지 커널 대기 상태 아래 숨기면 안 됩니다.
⑥ 이미 끝난 시도의 ATTEMPT_JSON 시간 재사용: 찬성.
유효한 elapsed_s가 있으면 미상으로 만들 필요가 없습니다. 중복 합산하지 않는 현재 구조도 맞습니다.
⑦ 결박되지 않은 증거로 정지: 찬성.
정상 승인에는 쓰지 않고 정지에만 쓰는 비대칭은 적절합니다. 거짓 경보는 원문과 발생 위치를 제시해 사람이 해소하면 됩니다. 다만 버전뿐 아니라 명확한 커널 부정 증거에도 동일하게 적용해야 합니다.
⑧ --killed와 /proc/uptime: 찬성, 비용 수정 조건.
기록 보완과 재시도를 분리한 것은 맞습니다. --killed는 시간을 채우는 명령이지, 실패한 계산을 정상 결과나 재시도 대상으로 바꾸는 명령이 아닙니다. Linux 지원 범위와 시작 시 읽기 실패 처리를 명시한 /proc/uptime 사용도 수용합니다.
4. Q-DB-9 — LOCPOT
현재 지정된 파일럿의 정보용 경로로는 GO입니다.
확인한 사항은 다음과 같습니다.
- 지정 잡의 사다리 INCAR 네 개에만 LVHAR가 추가됐습니다.
- 추출기는 격자와 값 개수·유한성을 검사하며, 실패하면 부분 파일을 버리고 경고합니다.
- 면평균 파일이 실행 기록 SHA에 묶입니다.
- 채택된 시도의 진단만 선택합니다.
- 면평균 배열은 G3/G4/G5 판정식에 들어가지 않습니다.
따라서 추가 데이터 블록 때문에 추출하지 못하는 경우를 정보 손실로만 처리하는 설계는 맞습니다. 그 결과를 “평탄하다”거나 “전하 이동 없음”으로 읽지 않으면 됩니다.
비차단 P2 보강은 두 가지입니다.
- [parse_zavg():974 (line 974)](build_round2_vasp_package.py:974): 헤더의 c_z_A 변환이 예외·유한성 검사 밖입니다. garbage면 예외, nan·0·음수면 정상 자료로 반환됩니다. 잘못된 진단은 {bad: …}로 처리하세요.
- [collect():1664 (line 1664)](build_round2_vasp_package.py:1664): run_id_matches=false여도 값 배열이 남습니다. 불일치면 bad/not_used로 배제하는 편이 안전합니다.
현재 작성 경로와 SHA 결박을 고려하면 이 둘은 이번 발송 차단 사유로 잡지 않았습니다.
5. Q-DB-10 — 자체 검토 S1∼S9
항목	판정
S1	미해제. 무결성 전에 환경 증거를 읽는 방향은 맞지만, 시도 열거와 커널 부정 증거에 누락이 남습니다.
S2	공통 경로 통합은 해제. 다만 공통 경로에 들어오기 전에 빠진 증거는 세 명령 모두 놓칩니다.
S3	조건부. 시작 표지·UNKNOWN·killed 절차는 맞고, 수동 시간 합산만 수정이 필요합니다.
S4	해제. 경과 시간과 달력 시각을 분리한 것이 맞습니다.
S5	주요 결함 해제. 끝 LF 허용은 P2 보강입니다.
S6	해제. 원문 줄바꿈을 보존하는 Python 판정 탐침이 통과했습니다.
S7	해제. stdout·PP 기록·시작 표지 변경을 실행 기록 불일치로 잡습니다.
S8	해제. 객체가 아닌 WAVECAR.info를 예외 없이 A 자격 미달로 처리합니다.
S9	해제. 빈 마지막 대입을 앞선 값으로 되살리지 않습니다.


봉인을 막는 일곱 사유로 확대한 것도 수용합니다. 실행 하나의 기록이라고 인정할 수 없는 모순을 물리적 미수렴과 구별한 것입니다. 다만 그 목록이 전체 필수값 검사를 대신할 수는 없습니다.
6. Q-DB-11 — 발송 해제 최소조건
현재 MANIFEST b9450f6f…의 v2 발송은 NO-GO입니다. 해제에는 아래 네 수정이면 됩니다.
1. 시도 열거 보완: INCAR·attempt.json이 없어도 남은 실행 흔적을 감사하고, 불완전 시도를 정상 잡 뒤에 숨기지 않기.
2. 커널 부정 증거 전달: 불완전·무결성 실패 시도의 명확한 부정·재생성 원문도 전역 정지에 연결하기.
3. 봉인 완결성 분리: 커널 대기 상태가 다른 필수값 결측을 가리지 않도록 하기.
4. 시간 합산 보완: 수동 초를 10진수로 처리하고 합산 실패·빈값은 다음 실행을 차단하기.
그 뒤 묶음을 재생성하고, 위 네 음성 사례를 배포본 검사기와 Linux 러너에서 확인하면 됩니다. 카드 문턱·구조·잡 행렬·물리 설계를 바꿀 요구는 없습니다.
검증 범위도 분명히 남깁니다. Python 판정·CLI·합성 반송 시험, interfaces 79/79 및 추가 비유한값 12건, 묶음 해시와 빌드 재생은 직접 확인했습니다. 반면 이 환경의 Bash/AWK 실행 제한으로 제출측 Linux 156/156 전체 시험을 독립 재현했다고 하지는 않습니다. 실제 VASP·UMA 계산과 실제 UMA 결과 열람은 하지 않았습니다.
재현 자료: [환경 감사·CLI 결과](cli_and_unbound_kernel_summary.json) · [판정 탐침 결과](runner_db_contract_results.json) · [묶음·LOCPOT 검증 상세](db_q6_q7_q9_review.txt)

---

## 첨부 (사용자가 회신과 함께 붙인 재현 자료 셋 — 원문 그대로 · 구분선과 코드 울타리만 더함)

### cli_and_unbound_kernel_summary.json

```json
{
 "synthetic_only": true,
 "check_exit_missing_two_files": 0,
 "a4_status_missing_two_files": "OK",
 "a4_common_missing_two_files": null,
 "incomplete_kernel_attempt_status": "INCOMPLETE_ATTEMPT",
 "incomplete_kernel_global": [],
 "incomplete_kernel_a4_status": "OK",
 "incomplete_kernel_a4_common": null
}
```

### runner_db_contract_results.json

```json
{
  "commit": "3d684e502a7fcfefa2e8ddd46853423fa6ad88ab",
  "manifest_sha256": "b9450f6f7e188b9159030b6cc6a031a106682fbd2076c27dd66acfd6f4f7bc70",
  "runner_matches_generator": true,
  "repository_python_probes": {
    "total": 41,
    "failures": {},
    "changes_from_CZ": {
      "rc1_two_runs": {
        "CZ": "RUN_FAILED",
        "DB": "SCF_UNVERIFIED"
      },
      "rc1_it_mismatch_term": {
        "CZ": "RUN_FAILED",
        "DB": "SCF_UNVERIFIED"
      },
      "crash_outcar_ahead": {
        "CZ": "RUN_FAILED",
        "DB": "SCF_UNVERIFIED"
      },
      "noterm_two_runs": {
        "CZ": "RUN_FAILED",
        "DB": "SCF_UNVERIFIED"
      },
      "term_no_header": {
        "CZ": "RUN_FAILED",
        "DB": "SCF_UNVERIFIED"
      },
      "cr_row": {
        "CZ": "OK",
        "DB": "SCF_UNVERIFIED"
      },
      "incar_empty_last": {
        "CZ": "OK",
        "DB": "SCF_UNVERIFIED"
      },
      "incar_cr": {
        "CZ": "OK",
        "DB": "SCF_UNVERIFIED"
      }
    }
  },
  "additional_probes": {
    "zero_rows_rc1": {
      "got": "SCF_UNVERIFIED",
      "want": "SCF_UNVERIFIED"
    },
    "duplicate_same_version_rc1": {
      "got": "SCF_UNVERIFIED",
      "want": "SCF_UNVERIFIED"
    },
    "completed_iteration_mismatch_rc1": {
      "got": "SCF_UNVERIFIED",
      "want": "SCF_UNVERIFIED"
    },
    "unfinished_one_ahead_rc1": {
      "got": "RUN_FAILED",
      "want": "RUN_FAILED"
    },
    "unfinished_two_ahead_rc1": {
      "got": "SCF_UNVERIFIED",
      "want": "SCF_UNVERIFIED"
    },
    "empty_last_ediff": {
      "got": "SCF_UNVERIFIED",
      "want": "SCF_UNVERIFIED"
    }
  },
  "release_caps_python": {
    "nan": "rejected",
    "inf": "rejected",
    "zero": "rejected",
    "negative": "rejected",
    "bool": "rejected",
    "scientific_output": "rejected",
    "positive": "accepted"
  },
  "regex_format_python": {
    "reading WAVECAR": [],
    "-*reading WAVECAR": [
      "'-' 로 시작 — grep 이 옵션으로 읽는다 (러너는 -e 로 넘기지만 손으로 돌리는 grep 과 뜻이 갈린다 · 자체 검토 S5)"
    ],
    "X*+X": [
      "수량자가 붙어 있다 (*+ · ++ · ?+ · +? … — 파이썬 3.11 은 소유·게으른 수량자로 읽고 ERE 는 겹친 반복으로 읽는다 · 자체 검토 S5)"
    ],
    "X++X": [
      "수량자가 붙어 있다 (*+ · ++ · ?+ · +? … — 파이썬 3.11 은 소유·게으른 수량자로 읽고 ERE 는 겹친 반복으로 읽는다 · 자체 검토 S5)"
    ],
    "X?+X": [
      "수량자가 붙어 있다 (*+ · ++ · ?+ · +? … — 파이썬 3.11 은 소유·게으른 수량자로 읽고 ERE 는 겹친 반복으로 읽는다 · 자체 검토 S5)"
    ],
    "X+?X": [
      "수량자가 붙어 있다 (*+ · ++ · ?+ · +? … — 파이썬 3.11 은 소유·게으른 수량자로 읽고 ERE 는 겹친 반복으로 읽는다 · 자체 검토 S5)"
    ],
    "X*?X": [
      "수량자가 붙어 있다 (*+ · ++ · ?+ · +? … — 파이썬 3.11 은 소유·게으른 수량자로 읽고 ERE 는 겹친 반복으로 읽는다 · 자체 검토 S5)"
    ],
    "(?i)reading": [
      "'(?' — 파이썬 확장 (ERE 에 없다)"
    ],
    "a*": [
      "빈 문자열에 맞는다 (무엇에나 맞는다)"
    ],
    "reading WAVECAR\n": []
  },
  "shell_execution": "NOT RUN: Bash/awk sandbox access denied in prior turn; no bypass attempted.",
  "static_budget_issue": {
    "accepted_wall_s": "0007200",
    "decimal_intended": 7200,
    "bash_octal_value": 3712,
    "accepted_error_value": "08",
    "cause": "wall_s digit validation permits leading zero; bash arithmetic uses octal and cap_ok does not check wall_s_of success or numeric output"
  },
  "scope": "Synthetic parser inputs only; no actual UMA/G5 data or W values."
}
```

### db_q6_q7_q9_review.txt

```text
DB scoped delta review — commit 3d684e502a7fcfefa2e8ddd46853423fa6ad88ab
Baseline CZ 8d41e4e0. Existing geometry/mask/design GO was not reopened.

Q-DB-6 (assigned portions): GO.

- NaN round-trip defect is closed: build_aprime_interfaces.py:488 validates all
  four parent/probe position and cell arrays before subtraction/comparison.
  Native interfaces suite: 79/79 PASS. Additional native Python tests reject
  NaN, +Inf, -Inf independently in parent/probe coordinates and cells (12 cases),
  while the positive rigid translation still passes. This is the precise fix
  requested by CZ, with no new geometric policy.
- pack() now includes run_aborted only if it exists and preserves find's exit
  status, returning packaging failure on enumeration errors
  (build_round2_vasp_package.py:407-413); finish converts failure to exit 4
  (:443-444). This part was source-reviewed, not shell-executed on this host.
- delta failure dependencies include each corresponding PBE+D3 pair, in
  addition to optB88 (:1687-1688), matching the quantity's two-input dependency.
- far diagnostics identify source_rung/source_status/adopted (:1652-1656).
  Only adopted p_z participates in the signal comparison (:1668-1674). Missing
  p_z or G3 difference data explicitly populates not_evaluated and G5 labels
  (:1670-1683), without changing numerical gate thresholds.
- Executed exact collector diagnostic AST statements on synthetic dictionaries:
  adopted r1B chosen correctly; failed far gets adopted=false and zavg not_used;
  missing p_z receives the unevaluated label; missing zavg alone is information
  loss without creating an unrelated charge-transfer missing-data signal.
- English execution count is accurately qualified: 24 jobs / 25 executions
  when nothing fails / at most 94 registered ladder executions, excluding
  separately recorded infrastructure retries (README/source English summary).
  Resume PP and numeric cap details belong to the runner audit.

Q-DB-7 (package regeneration/integrity): GO.

- Actual v2 MANIFEST SHA256 matches
  b9450f6f7e188b9159030b6cc6a031a106682fbd2076c27dd66acfd6f4f7bc70.
- Every one of its 170 listed members matches the declared hash.
- All 166 job-file paths are preserved. The only changed job files are
  P2S_S_A_far/{INCAR,INCAR.r1A,INCAR.r1B,INCAR.r2B}; semantic comparison finds
  exactly LVHAR=.TRUE. added in those four, with no other setting changes.
- All 24 job identities/stages/methods/ladder/structures/nions/compositions/
  electron counts/ENCUT/ISMEAR/SIGMA/k/cells/area/dipol/source geometry hashes
  match CZ. The entire v1 package directory and original geometry seal directory
  remain byte-identical to the CZ snapshot.
- The actual v2 run_all.sh is byte-identical to current run_all_text().
- Replayed the current builder using recorded per-geometry D3 references from
  its jobs.json as a lookup stub for d3_ref_eV: all 172 package files, including
  README and MANIFEST, are byte-identical to the supplied v2 package. This tests
  packaging reproducibility; it does not rerun or independently validate D3.
  No actual UMA SP/G5 result file was opened and no W values were emitted.

Q-DB-9 (LOCPOT): GO for the specified fixed-geometry pilot information path;
two nonblocking P2 defensive details are noted below.

- LVHAR is restricted to P2S_S_A_far and all its four rung INCARs
  (source :75, :112-113, :259).
- The extraction rules (:680-704) handle VASP5 normal and Selective dynamics
  coordinate layouts, find the three positive grid sizes after atom positions,
  count exactly nx*ny*nz scalars, reject missing/excess data and nonfinite input,
  group the x-fast/y-next values into xy planes, and label z=k*c_z/nz.
  This is appropriate for the existing orthogonal-c, positive-scale structures.
- LOCPOT extraction failure is intentionally nonfatal (:760); it removes the
  partial file and logs a warning (:705-706). Normal completion deletes the raw
  LOCPOT (:767). The raw file is forbidden from returns, while zavg is allowed
  (:73-74). An additional data block after the first scalar grid therefore loses
  this optional diagnostic and leaves SCF/gate decisions unchanged, as intended.
- The zavg header stores source LOCPOT SHA and run_id (:702), and the derived
  file is bound into attempt.json (:761-764); check_attempt verifies that hash
  (:1194-1200). Collection selects the adopted rung and suppresses data from
  unadopted results (:1652-1665). The zavg arrays feed no G3/G4/G5 equation or
  charge-transfer signal; p_z and the registered G3 diagnostics remain separate.
- A faithful Python model of the AWK stream rules passed the regular/selective
  header and plane-index arithmetic cases plus truncated, extra-value,
  extra-block, NaN, overflow-to-Inf token, both wrong grid sizes, and VASP4 cases.
  This is an indexing/math/source check, NOT native AWK execution.

P2 optional hardening — parse_zavg header validation (:964-974).
  Header c_z_A conversion occurs outside the numeric try block and is not checked
  for finiteness/positivity. A synthetic c_z_A=garbage raises ValueError rather
  than returning {bad:...}; c_z_A=nan, 0 or -10 returns normal data. nx/ny and z
  spacing are also not validated. Current runner emits the header from known
  fixed input geometry, and modified derived files are caught by attempt SHA,
  so this is not a reason to block the supplied package. Minimum hardening:
  parse c_z/grid within the same try, require positive finite c_z and positive
  nx/ny/nz, verify z against k*c_z/nz at output-rounding tolerance; return bad
  instead of throwing. No physical threshold or card change is required.

P2 optional hardening — mismatched diagnostic header run_id (:1664-1665).
  Exact collector-block execution shows it returns V_eV with run_id_matches=false
  if the header differs. It is visibly flagged and does not affect gates, and
  the current writer sets the correct ID. Prefer a bad/not_used diagnostic on
  mismatch so callers cannot accidentally consume the flagged values.

Verification limitation:
  Native Git gawk.exe fails with NtCreateDirectoryObject / MSYS access denied;
  Git bash.exe exits 1. Accordingly there is no independent Bash/mawk/gawk
  execution claim in this review. Full Linux runner test counts in the prompt
  remain author-reported; native Python interfaces and package replay above
  were independently executed here.

Repro files beside this report:
  db_geometry_package_audit.py — hashes, byte diffs, recorded-D3 package replay,
      NaN fix, native parse_zavg positive/negative/header tests.
  db_locpot_contract_tests.py — explicitly modelled AWK and exact collector AST.
Run with bundled python.exe -B -X utf8 from this review directory.
```
