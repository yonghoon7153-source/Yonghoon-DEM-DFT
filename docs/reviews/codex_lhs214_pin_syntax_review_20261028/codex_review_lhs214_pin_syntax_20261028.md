# LHS214 사전 점검 SHA 형식 수정 재확인

작성 2026-10-28 KST · 독립 검토 · 실제 발사 없음

**판정: LHS214-PRE-01은 닫힘. P7/P10 두 줄 수정은 GO다.** 정상 입력을 유지하면서 원래 LF 반례를 거부한다. 이번 범위에서 새 P1/P2 코드 결함은 발견하지 않았다. 첨부된 실제 WSL 사전 점검 영수증도 독립 재검증을 통과했다.

**이 판정은 실제 214건 발사 GO가 아니다.** WSL 묶음에는 자체시험 다섯 개의 실제 셸 종료코드가 따로 보존되지 않았다. 아래 수치 대조 표를 수령표에 연결하고 기존 단계별 종료코드 기록을 보완한 뒤 발사 범위를 종결할 수 있다. 이미 비준된 설계 선택을 다시 묻는 판정은 아니다.

## 1. 대상과 증거의 신원

| 구분 | 고정 값 |
| --- | --- |
| 수정 전 본 가지 | `1baa0d9b7a9d5b2c6b101b5d203eacb1e18fd6ca` |
| 수정 커밋 | `09bf1813c1b5a188c0caf056ad490ea0f86da8fb` |
| 요청서의 리뷰 핀 | `b7a979032160dc1d9514c612aa36ff0d6c28bf54` |
| 실제 첨부 WSL 핀 | `35f0327377a4213774010a090df4d224e50d29e1` |
| WSL TGZ SHA-256 | `9c05aef7591ad10af70af52c01508b494ddc71855322b0ce367f42f67a5be0b8` |
| 활성 CODE_FILES 지문 | `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` · 32개 |

10-27 정정 요청서를 본체로, 10-24 원본과 WSL 단계 0–6 안내·실제 TGZ를 함께 검토했다. 수정 커밋의 원격 커밋 메시지에는 원 수정 `ed6ed401f904d9f818cbdced42d111a7b1efb8d2`의 cherry-pick 기록이 있다. 커밋 메시지 자체를 코드 동일성의 증명으로 사용하지 않고 바이트를 대조했다.

고정 리뷰 핀의 39개 소스·도구를 Git blob SHA로 검증했다. 봉인 32개가 모두 포함된다. 이 39개는 WSL 핀과도 동일하며 두 등록 문서는 별도로 동일성을 확인했다. 요청서가 말하는 여섯 커밋 쌍 전체를 새로 인증한 것은 아니다. 이번 독립 판정에 필요한 수정 전→후의 두 줄과 리뷰 핀→실제 WSL 핀의 관련 파일을 직접 대조했다.

리뷰 핀과 WSL 핀은 **전체 저장소가 같은 커밋이 아니다.** GitHub 비교 응답은 변경 파일 300개에서 끝났으므로 그 응답을 전수 목록으로 해석하지 않았다. 관련 파일 동일성은 해당 Git 하위 트리의 blob 목록으로 별도 확인했다.

실제 수령 TGZ는 일반 파일 18개와 디렉터리 1개다. 경로 이탈·링크·이름 충돌을 검사한 뒤 읽었다. 실제 WSL 원문은 `wsl/`에 보존했다.

## 2. LHS214-PRE-01 종결 근거

- **ID / 심각도:** LHS214-PRE-01 / 기존 P3.
- **원래 반례:** 승인된 소문자 40자리 SHA 뒤에 LF 한 글자가 붙어도 정규식 `^[0-9a-f]{40}$`의 `.match()`는 매치한다. Python의 `$`가 마지막 LF 앞에도 매치하기 때문이다.
- **수정:** [runner P7](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b7a979032160dc1d9514c612aa36ff0d6c28bf54/scripts/run_network_194_parallel.py#L2049), [P10](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b7a979032160dc1d9514c612aa36ff0d6c28bf54/scripts/run_network_194_parallel.py#L2082)의 `.fullmatch(gsha)` 두 곳.
- **독립 재현:** 실제 194·보충 20 영수증 모두에서 수정 전 코드가 LF를 수용함을 재현했다. 수정 뒤에는 원문 SHA를 정규화하지 않고 P7/P10이 거부한다.
- **최소 해결:** 이번 두 줄로 해당 결함은 해결됨. 전역 정규식 변경이나 수치 코드 변경을 추가 조건으로 요구하지 않음.

| 입력 | 수정 전 | 수정 후 |
| --- | --- | --- |
| 실제 정상 40자리 SHA + 동일한 전체 승인 SHA | P0–P10 통과 | P0–P10 통과 |
| 영수증 SHA에 LF 추가 | P7/P10 통과 — 원래 반례 | P7/P10 실패 |
| 영수증 SHA에 CRLF 추가 | 거부 | 거부 |
| 마지막 hex 한 자리 변경 + 전체 승인 SHA | P10 실패 | P10 실패 |
| 정상 SHA + 기존 7자리 승인 접두 | 통과 | 통과 |
| 영수증 SHA의 비문자열·길이 초과·중간 공백·비ASCII 문자 등 | 별도 상세 기록 | 의도한 거부 |

마지막 자리만 다른 SHA는 짧은 로그 접두와 일치할 수 있어 P7만으로는 구별되지 않는다. **전체 승인 SHA를 주면 P10이 구별한다.** 승인값을 7자리로 주면 그 접두 밖 차이를 구별하지 않는 것은 기존 계약이다. 이번 수정이 이를 전체 SHA 일치 계약으로 바꿨다고 해석하면 안 된다.

실제 영수증 2개 × 원문 SHA 20종 × 승인 방식 3종(전체·7자리·생략) = **120개 기대 결과 일치**. 기존 6개 경계 시험도 실제 생산 검사기를 호출하여 **6/6 통과**, 그 과정의 영수증 자체시험은 **123/123, rc 0**이었다.

## 3. 질문 Q1–Q5 답

| 질문 | 판정 | 이유 |
| --- | --- | --- |
| Q1 LF 차단과 정상 동작 보존 | **닫힘** | 위 실제 영수증 기반 120개 대조. 원문 SHA를 strip하지 않고 검사한다. 정상 핀·전체 승인값 불일치 거부·기존 승인 접두 동작 보존 |
| Q2 실제 검사기 사용과 회귀 보존 | **닫힘** | 원 경계 시험은 `preflight_receipt_checks`를 호출한다. 고정 코드의 기존 123개 시험도 함께 통과하여 정상 preflight·합성 launch·S0b 회귀를 보존했다. 별도로 합성 manifest 15개를 실제 영수증 함수에 적용 |
| Q3 봉인·물리 경로 비변경 | **닫힘** | 전체 runner 바이트 차이가 두 호출뿐이다. runner는 CODE_FILES 32에 포함되지 않는다. 32개 파일의 지문과 두 등록의 활성 지문을 독립 재계산하여 일치 확인. 물리값의 새 검증이나 재적합을 뜻하지 않음 |
| Q4 체크리스트의 지위 | **동의, 실제 수령 상태만 갱신 필요** | 기존 도구의 수령표이며 새 collector가 아니다. 실제 WSL 자료와 합성 회귀 자료를 구별한다. 실제 자료 대부분이 도착했으므로 계속 모두 “미수령”으로 적어 두면 낡은 상태가 됨. 종료코드·확인 기록은 아래처럼 구분 |
| Q5 남은 match와 승인 정규화 | **범위 분리 동의, 아래 잔존 경계 명시** | F7/G7의 원문 SHA fullmatch가 승인 경로에서 차단한다. 승인 입력의 strip/lower는 사용자가 준 승인 문자열 규약이며, 영수증 원문을 정리해 통과시키는 것과 다름 |

### Q5의 잔존 반례

[launch_eligibility 1140행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b7a979032160dc1d9514c612aa36ff0d6c28bf54/scripts/run_network_194_parallel.py#L1140)은 여전히 LF를 받는다. 이를 “고쳐졌다”고 쓰면 안 된다.

실제 생산 함수 `launch_eligibility`와 `supp20_input_receipt.receipt`로 만든 별도 15개 대조의 결과:

| 두 manifest의 원문 SHA | 전체 승인 SHA 제공 | 7자리 승인 접두 제공 | 승인값 생략 |
| --- | --- | --- | --- |
| 둘 다 정상 | rc 0 | rc 0 | rc 0 |
| 보충 manifest만 LF | F7·H1 실패 | F7·H1 실패 | H1 실패 |
| 194 manifest만 LF | G7·H1 실패 | G7·H1 실패 | H1 실패 |
| 둘 다 같은 SHA+LF | F7·G7 실패 | F7·G7 실패 | **rc 0** |
| 둘 다 마지막 한 자리만 같은 오값 | F7·G7 실패 | rc 0 | rc 0 |

이 결과는 **남아 있는 P3 형식 경계**이며 새로운 커밋 우회를 주장하는 P1 반례가 아니다. 형식상 같은 SHA 뒤의 LF이고, 승인값 없는 경로는 원래 승인 대조를 보증하지 않는다. 그러나 “모든 발사 경로가 SHA 형식에 fail-closed”라는 일반화는 반박한다.

이번 LF 수정의 종결을 막지는 않는다. 기존 실행표대로 **전체 40자리 approved-sha를 계속 제공**하고 두 실제 manifest를 F7/G7에 통과시켜야 한다. 승인값 없는 rc 0을 승인 핀 일치 증서로 사용하지 않는다. 원문 SHA fullmatch는 [영수증 357–361행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b7a979032160dc1d9514c612aa36ff0d6c28bf54/scripts/supp20_input_receipt.py#L357)에 있다.

## 4. 실제 WSL 증거 재검증

실제 PIN은 `35f0327377a4213774010a090df4d224e50d29e1`이다. 리뷰 핀 b7을 승인 인자로 대입하면 P10이 실패한다. 두 역할을 바꿔 적지 않는다.

| 항목 | 실제 자료 및 독립 대조 |
| --- | --- |
| 시작 기록 | 2026-10-28 17:32:39 KST · checkout `/home/yonghoon71/dem-audit` |
| Python | `/home/yonghoon71/Yonghoon-DEM-DFT/.venv/bin/python3` · 일반/-I 동일 |
| WSL 의존성 | Python 3.12.3 · NumPy 2.5.2 · SciPy 1.18.1 · networkx 3.7 — env.txt 원문 |
| HEAD / dirty | head.txt = 실제 PIN · dirty.txt 비어 있음 |
| 194 ROOT | `/home/yonghoon71/net194_35f032737_1028` |
| 보충 ROOT | `/home/yonghoon71/netsupp20_35f032737_1028` · 194와 다름 |
| 실제 194 영수증 | P0–P10 **11/11 통과** |
| 실제 보충 영수증 | P0–P10 **11/11**, 전체 receipt **24/24**, rc 0 |
| 로그 보존 | 194 4,628 B · 보충 4,390 B · 원문 SHA-256와 receipt/receipts_sha256.txt 일치 |
| 입력 지문 | 고정 214개 descriptor 및 등록 자료로 계획 재구성 · 두 영수증의 input_digest 일치 |
| 범위 | 실제 dry-run 사전 점검. manifest·primary_manifest 입력은 null. 실제 발사 영수증 아님 |

독립 재검증에서 원문 영수증의 `log.path`만 아카이브 안의 같은 로그 파일로 옮긴 사본을 사용했다. **PIN·지문·내용·기대값을 교체하지 않았다.** 원본은 보존했고 경로를 옮긴 사본은 `independent/*_relocated.json`으로 구분했다.

원 WSL 덤프 자체가 이 TGZ에 들어 있지 않으므로 원 덤프 214개를 다시 읽었다는 주장은 하지 않는다. P8의 “raw 문제 0”은 원 실행이 기록한 로그와 영수증의 일치를 확인한 것이다. P9는 등록·descriptor 자료에서 독립 재계산했다.

### 194 여섯 칸 대조

아래 값은 등록 원문, 실제 WSL 로그의 두 기계 판독 줄, 독립 계획 재계산을 대조한 결과다. 확인 기록은 **본 독립 검토, 2026-10-28 KST**이며 WSL 현장 작업자 신원을 대신하지 않는다.

| 칸 | 실제 값 = 등록 값 | 대조 |
| --- | --- | --- |
| n / missing_raw_sha | `194` / `[]` | 일치 |
| ids_sha256 | `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf` | 일치 |
| raw_sha256_table_sha256 | `da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784` | 일치 |
| cohort_tsv_sha256.lhs | `32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809` | 일치 |
| cohort_tsv_sha256.lhsx | `0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45` | 일치 |
| code_fp / 파일 수 | `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` / `32` | 일치 |

별도 “수집기”를 만들 필요는 없다. 기존 수령표에 이 대조 결과와 증거 경로를 연결하면 된다. 원 묶음의 `handcheck_194_lines.txt` 자체는 두 로그 줄의 발췌이며 완성된 확인자 표가 아니었다.

## 5. 발사 증거에서 남는 항목

**증거 보완 E1 — 자체시험의 실제 종료코드 기록.** [기존 체크리스트 30·34·36행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b7a979032160dc1d9514c612aa36ff0d6c28bf54/docs/reviews/lhs214_wsl_receipt_checklist_20261024.md#L30)이 이미 요구하는 항목이다.

첨부 로그 끝에는 fast16 16/16, real4 4/4, reread “전부 통과”, runner 139/139, receipt 123/123이 있다. 그러나 이 다섯 명령 뒤에 화면으로 출력한 실제 셸 종료코드는 18개 파일에 별도로 들어 있지 않다. **출력의 PASS로 실제 프로세스 종료코드까지 만들지 않는다.** preflight 생산자 JSON의 exit_code 0 및 검증 JSON의 rc 0은 별도로 존재하므로 그 기록까지 누락이라고 분류하지 않는다.

최소 해결은 당시 터미널의 단계별 종료코드 출력을 보완하는 것이다. 기존 화면 기록을 회수할 수 있으면 재실행할 필요가 없다. 기록이 사라졌다면 잃은 검사 증거만 같은 환경에서 다시 확보한다. 이 이유로 물리 배치나 이미 확보한 preflight 전부를 다시 돌리라는 요구는 아니다.

**증거 보완 E2 — 수령표의 신원·확인 기록 연결.** 위 여섯 칸 수치는 이번 검토에서 모두 대조했다. 원 요청의 실제 작업자·확인 시각은 임의로 채우지 않고, 이 독립 대조와 WSL 작업 기록을 각자의 출처로 연결한다.

두 항목은 코드 결함으로 새 P1을 붙인 것이 아니라 기존 발사 증거 계약의 완료 여부다. 외부 발사 범위 확인, 실제 승인 PIN과 실행 직전 환경·ROOT 점검은 기존 절차대로 남는다. 새 비준 절차를 추가하지 않는다. S3·v1.3 주 타깃·기존 L214R-S03/S05 한정도 이 형식 수정으로 풀리지 않는다.

## 6. 재현과 검사 범위

ZIP을 새 폴더에 풀고 Python에 NumPy·SciPy·networkx가 준비된 환경에서:

```text
python -I -X utf8 -B probe_receipts.py
python -I -X utf8 -B probe_launch_contract.py
python -I -X utf8 -B run_canonical_complete_env.py
python -I -X utf8 -B audit_delivery.py
```

첫 둘은 생산 검사 함수를 호출하는 독립 탐침이다. 세 번째는 핀에 있던 기존 경계 시험과 receipt 자체시험을 실행한다. 네 번째는 첨부 해시·보충 전체 24칸·194 수치 대조를 확인한다. 어느 명령도 실제 DEM/214 배치를 발사하지 않는다.

이번 독립 실행은 Windows Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3 · networkx 3.7이었다. WSL 실측 환경과 혼동하지 않는다. 처음의 기본 환경에는 SciPy와 역사 회귀용 fixture가 없어 105/123이었고, 작업 폴더의 임시 디렉터리 접근 설정도 필요했다. 고정 blob의 fixture 및 이미 로컬에 있던 의존성을 갖춘 뒤 **제품 코드·기대값을 변경하지 않고** 123/123을 얻었다. 두 synthetic manifest가 처음 같은 폴더에 있던 검토용 fixture 실수도 H1에 걸렸으며, 별도 폴더로 고친 뒤 정상 대조를 포함한 15개 결과를 얻었다.

과거 전체 게이트 155 PASS/0 FAIL/rc 0은 `ed6ed401f…` 후보의 역사 기록이다. 이를 이번 b7/35f 전체 게이트를 독립 재실행한 결과로 부르지 않는다. 이번에 runner 139·fast16·real4·전체 check_all을 독립 재실행했다는 주장도 하지 않는다. 그 숫자는 첨부 WSL 로그와 출처를 구분한다.

핵심 산출:
- `runner_independent.diff`: 실제 수정 전/후 바이트 차이
- `cache_verified.json`, `b7_to_35_identity.json`, `registration_pin_identity.json`: 원격 blob·핀 동일성
- `independent/receipt_probe.json`: 120개 경계·수정 전 LF 재현·실제 두 영수증
- `independent/launch_contract_probe.json`: 15개 manifest 경계
- `canonical_boundary_complete_env/summary.json`: 6개 경계와 123개 자체시험
- `independent/supp20_reverified.json`: 실제 보충 영수증 전체 24칸
- `independent/delivery_audit.json`: 수령 파일 해시·활성 32 지문·여섯 칸 대조

**최종: LHS214-PRE-01 닫힘 / 두 줄 수정 GO. 실제 발사 GO는 이번 판정으로 부여하지 않음.**

