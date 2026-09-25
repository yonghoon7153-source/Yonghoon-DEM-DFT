# Gate71 회신 — 한정 GO 보류, E3·E9 잔여 2건

대상 요청/HEAD `4505b70c6e63453e0424239cac7d48488fee022a`, 코드 `876429562f6a69b59793c70700cb5b375391ab67`, 직접 계산 source_digest `b705a21a1237ec73`. 코드 대상→HEAD RUN_SCOPE diff 0. 회귀 보고 HEAD `0e6348be…` 이후 변경은 문서 3개뿐임을 확인했습니다.

**현재 한정 실행 NO-GO. E3 [P1]와 E9 [P2]의 잔여만 보완해 주세요. 무제한 독립 GO 요건을 추가한 것이 아닙니다.**

## 수용한 것

- G70-N1 하위 shell parser 경계 수정/회귀.
- E3 중 YAML index fail-closed·실제 구성원 SHA 대조. 실물 25개 payload 집합/SHA 직접 일치 확인.
- E5 modern/legacy typed reader 및 bool sealed. 국소 양성 2/부정 3과 기존 367개 레코드의 형식 확인. 과거 class 변경 없음.
- E6 이번 실행의 authority 격리·배타 운영 창·전후 delta 조건. 과거 351개 이관은 별건.
- E10 적법한 양성 fixture 보완. 보고된 Linux 1855 passed/2 xfailed·smoke rc0는 송신 실행 증거로 구분하며 수신 재실행으로 쓰지 않습니다.
- E1/E2/E4 한계 라벨 수용, E7/E8 유지. 같은 항목을 새 차단으로 재개봉하지 않습니다.

## E3-R [P1]: 결과 일치/산출 결속을 소비하지 않고 PASS 주장을 읽음

`tools/preserve.py:7737–7755`는 output의 비어 있지 않은 semantic 문자열·canonicalizer·rescored_summary와 outputs_agree=True만 봅니다. sealed_summary 존재, 실제 두 SHA 일치, source_file_sha256↔bundle.fits_sha256 결속은 검사하지 않습니다. `attach_bundle_evidence:7830–7854`도 이를 재검사하지 않고 current_validated로 올립니다. restore.run_dir_relative와 원장 evidence.out/해당 산출의 결속도 없습니다.

원래 실물 영수증을 검토자 소유 복사본에서 변형하고 core SHA를 다시 맞춰 지정 reader 본문만 확인했습니다.

- 정상 영수증 수용, 다른 leg/잘못된 core SHA/validation.ok=False 거부: 대조군 정상.
- sealed_summary 누락 / 두 semantic SHA 불일치: reader **수용**. 기존 생산자의 순수 `_outputs_agree`는 둘 다 **거부**.
- source fits SHA 불일치·부재, 다른 restore run 경로: reader **수용**.

전체 attach/복원/승격을 실행한 결과는 아닙니다. 프로젝트 import 없이 지정 AST reader와 순수 비교 술어만 호출했고 후속 원장 write 영향은 정적 대조했습니다. 실제 영수증의 수치가 틀렸다는 주장도 아닙니다.

새 정상 fixture `test_gate70_defensive.py:302–323` 자체가 output 한 개+outputs_agree=True여서 생산 계약의 비교 상대 요구를 시험에서 지워 놓았습니다. 선택 schema의 비교 쌍·실제 일치·source fits·실행/복원 경로 결속을 소비하고, 실물 양성+위 반례+거부 시 원장 불변을 제한 회귀로 닫아 주세요. 서명·OS principal·독립 attestation 추가 요구가 아닙니다.

## E9-R [P2]: 같은 초기 명령은 chunk resume이 아님

요청문 `:119–120`은 실패 뒤 같은 명령으로 이어간다고 하지만 초기 argv에는 --resume이 없습니다. `run.sh:56`은 RESUME=false, `:522–557`은 true일 때만 하위에 전달합니다. `src/grid.py:601–612`와 `src/fitting.py:1524–1526`은 resume이 아닐 때 완료 집합을 읽지 않습니다. claim 재개와 chunk 재개를 구분해야 합니다.

실패 즉시 중지·재승인으로 범위를 좁히거나, 동일 plan/token/source/부분 산출을 확인한 뒤 사용할 **명시적 --resume argv와 횟수**를 적어 주세요. 모든 실패를 플래그 하나로 복구할 수 있다고 쓰지 마세요. 이 정정은 본 계산 선실행을 요구하지 않습니다.

함께 정정할 표현: 실제 checkout은 prospective 계획을 담은 승인 HEAD(8764는 코드 기준), CANONICAL_RUN 상속 여부를 명시적으로 고정, E4의 4+1을 보고된 4+4와 통일. E6 격리 tree에는 requirements*.txt 두 파일이 복사되지 않으므로 원본 source_digest 동일 주장은 좁혀 주세요. 이 문구들은 별도 차단 목록으로 늘리지 않습니다.

## 질문 답과 다음 경계

① E3 아니오 / E5 예 / E6 예(한정 운영 조건) / E10 예(송신 증거 범위). ② E1/E2/E4 라벨 예(수량 정정). ③ E9 부분 수용. ④ **현재 한정 GO 아니오** — E3 소비 계약과 E9 실패 정책을 고정한 뒤 재판정합니다.

다음 자료는 이 두 잔여의 제한 diff/정상·부정 증거와 최종 commit/source_digest, 수정 명세면 됩니다. E1/E2/E4 전면 구현·역사적 registry migration을 요구하지 않습니다. RUN_SCOPE 변경 시 이전 영수증/회귀를 새 코드에 소급하지 마세요. 필요한 실제 복원/재채점은 별도 승인 대상입니다.

검토 checkout DD 추적 2,459개 전후 크기/SHA 동일, clean. 본 계산·COMSOL·Java·과학 분석 프로그램·복원·class/운영 원장 변경은 0회입니다. 이 회신은 본 실행이나 prospective 승인 기록 작성/커밋의 허가가 아닙니다. 자동 스크립트 실행/외부 발송도 요청하지 않습니다.
