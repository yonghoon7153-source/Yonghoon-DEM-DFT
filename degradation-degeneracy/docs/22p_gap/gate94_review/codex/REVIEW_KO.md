# GATE94 한정 보완 검토

G93-N1 코드 차단과 G93-N2 원 로그 인계는 **이번 한정 범위에서 종결 수용**한다. 새 코드 차단사항은 발견하지 못했다. 출처 설명에는 비차단 정정 한 건이 있다. GATE94 §6의 “14개 모두 요청 커밋 전”은 틀리며, 마지막 docs-lint는 요청 커밋 뒤의 실행이다.

이 판정은 묶음 6 전체 종결이나 실행 GO가 아니다. 수신자는 제출 소스·시험·변이·분석 프로그램·COMSOL을 실행하지 않았다. 코드 흐름, 저장된 로그, Git tree와 파일 바이트를 검토했다.

## 고정 대상과 식별

| 항목 | 확인한 값 |
|---|---|
| 요청 커밋 | 2345051aadf7c9e5f764fa76966bd4e3ad9a02eb |
| 요청문 blob | 6a3cec281a7c43e497b52f6394a7ed5ee349b896 |
| 판정 코드 | 0ab2924f465461f1224d66c8f0a8c6013e857c6b |
| 이전 코드 | d7a97aa57ea926916d56c985ee4bc2bed96fa81a |
| 회귀 로그 HEAD | 168fd41a5158c4908cfc3ec08b05652b8f0b7629 및 fe72f9b81b141cc963696bfe1afe94e681cd09c3 |
| 제출 source_digest | 044e4f5513011a9b |
| GATE94 원 로그 증거 커밋 | 016e970f633161ca68300976ec91ba3a1ddcb625 |

첨부 요청문은 고정 요청 커밋의 파일과 SHA256가 같다. 각 커밋의 비절단 degradation-degeneracy tree에서 RUN_SCOPE 60개 파일의 blob·mode를 대조했다. 이전 코드→판정 코드의 차이는 src/io.py 하나이며, 판정 코드→검증 두 HEAD→요청 HEAD의 RUN_SCOPE 차이는 0이다. source_digest는 요청문·영수증에서 식별했고 저장소 함수를 실행해 재계산하지는 않았다.

원장 §148–150의 승인 기록과 제출 범위는 일치한다. 저장소의 승인 기록을 읽었다는 뜻이며, 이번 검토가 새 실행 권한을 부여하지 않는다.

## G93-N1 코드와 회귀 수용

고정 코드 [src/io.py 1904](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0ab2924f465461f1224d66c8f0a8c6013e857c6b/degradation-degeneracy/src/io.py#L1904)와 [2026](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0ab2924f465461f1224d66c8f0a8c6013e857c6b/degradation-degeneracy/src/io.py#L2026)을 기준으로 판단했다.

유효 v3는 역사 reader에서 여전히 빈 오류 목록을 받지만, 기존 stage3_axis_from_envelope는 v4 schema가 아니면 PreserveError를 낸다. 새 코드는 이 이유를 ax_err로 보존하고 v4_bad에 합친다. 따라서 네 재유도 관련 검사를 이유 있는 실패로 남기고 반환하며, 아래 _stage3_rederive의 v4 전용 키 접근에 도달하지 않는다.

정상 v4에서는 두 오류 원천이 모두 비어 기존 재유도가 유지된다. planned_id만 다른 경우는 envelope 자체의 schema·구조 오류와 분리되므로, 기존 독립 실패 판정을 남기면서 재유도는 진행한다. 단순 사본 값 불일치인 ax_bad 전체를 차단 조건으로 쓰지 않은 것도 이 구분에 맞는다. preserve.py는 이전 코드와 blob·전체 텍스트가 같아 역사 reader 및 축 helper의 의미가 유지됐다. io.py 전체도 제출된 두 hunk만으로 이전 텍스트에서 재구성된다.

새 n1은 실제 v6 산출 fixture를 유효한 v3 envelope로 바꾸고 계획 ID·record·run signature·fits 봉인을 다시 맞춘다. 실제 validate_provenance를 부르는 spy는 예외를 삼키지 않는다. 따라서 KeyError를 임의의 거부 성공으로 세지 않는다. n1은 재유도 호출 0, 네 실패 키 및 v4 경계 이유를 단언한다.

c1은 정상 v4에서 clean_worktree·코드_identity를 제외한 검사의 무실패와 실제 재유도를 확인한다. c2만 보면 실패 집합 전체가 아닌 부분 단언이지만, 기존 k06[planned_id]가 같은 제외 조건의 _only로 정확히 stage3_planned_envelope 하나만 실패하도록 고정한다. 둘을 합친 근거로 기존 의미 보존을 수용하며 새 시험 추가를 요구하지 않는다.

신규 변이는 ax_err를 차단에서 빼 이전 결함을 되살리고, n1의 정확한 KeyError 증인을 요구한다. 기존 k04_env 변이는 조건 변수 이름만 새 코드에 맞췄다. 제출 로그의 RED는 이전에 정적으로 지적한 parameter_order_sha256 KeyError와 일치한다.

수용 범위는 이 특정 v3 경계와 대조군이다. 독립적으로 망가진 record 등에서 앞선 기존 반환이 일어나는 모든 조합까지 네 검사 키를 보장한다는 뜻은 아니다.

## G93-N2 원 로그 인계 수용

수신 ZIP은 128,409 bytes, SHA256 b76e663dcf9fba7ce18a0381e01b1777ad7e594d341d42a74376669d37c3f7c6이다. 별도 manifest는 11,913 bytes, SHA256 b2ee0d56a10be75c16dcd81fd23d65c4f1814ef6426b3fddabb37e08ec577620이다.

14개 파일의 정확 집합·크기·전체 SHA256·CRC를 확인했다. 중복·경로 탈출·대소문자 충돌·링크 문제는 발견하지 못했다. 모든 압축 해제 바이트를 Git blob 형식으로 해시해 후속 e0e9f213deecabfd50254217a428bac6a85819f8 tree와 14/14 대조했다. 기존 요청 0e3c244ea에는 README만 있었다는 G93 관측은 그대로이며, 이번 후속 인계로 결손이 해소됐다.

원문으로 2320 passed / 1 xfailed, smoke rc0, 전체 변이 421/421 rc0, 당시 완료 단계의 시작·끝 HEAD 및 dirty0을 확인했다. 이는 제출된 실행 기록의 수용이며 현장 독립 관측이나 수신자 재실행은 아니다.

초기 emit 로그와 실패·중단 기록도 남아 있다. 초기 replay/emit 다섯 파일에는 실제 rc 줄이 없으며, 04b 파일명의 rc0을 원문 종료코드로 인증하지 않는다. 마지막 전체 replay의 rc0은 확인되지만 이를 앞선 누락 rc에 소급 적용하지 않는다. manifest의 status_lines 중 세 항목은 200자 prefix다. 원문은 온전하고 발췌만 잘린 것이므로 로그 인계를 보류할 사유는 아니다.

## G94 C1 비차단 출처 문장 정정

위치: [GATE94_REQUEST.md 68](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/2345051aadf7c9e5f764fa76966bd4e3ad9a02eb/degradation-degeneracy/docs/22p_gap/GATE94_REQUEST.md#L68), gate93_n2_supplement/README.md 18. 우선순위 P2, 문서 정정이며 코드·원 로그 인계 종결을 막지 않는다.

- G93 요청 커밋 0e3c244ea의 author/committer 시각: 2026-10-06 18:44:27Z.
- 14_docs_lint 로그: 같은 요청 HEAD에서 18:44:35Z 시작, 19:17:57Z 종료.
- 후속 원 로그 추가 커밋 e0e9f213d: 19:18:27Z.

따라서 14 docs-lint는 요청 커밋 뒤의 검사다. 다음처럼 정정하면 된다.

> 14개 로그 중 00–12 및 중단 두 로그의 제출된 수정 시각은 요청 커밋 전이다. 14 docs-lint는 요청 HEAD 0e3c244ea가 만들어진 뒤 18:44:35Z–19:17:57Z에 실행됐다. 14개 모두 후속 e0e9f213d의 blob과 일치한다. 원 scratch와의 동일성·수정 시각·보충 과정의 재실행 0은 제출자 기록이며, 수신자가 당시 scratch를 직접 관측한 것은 아니다.

원 로그·ZIP·manifest를 고치거나 시험을 다시 돌릴 필요는 없다. 요청문과 보충 설명에 정정 이력을 남기는 것으로 충분하다.

## GATE94 완료 로그와 실패 보존

요청 tree에는 16개 파일이 있다. 정확히는 .log 14개와 README 2개다. 요청문의 “로그 15 + README”는 aborted/README.txt까지 로그로 센 표현이므로 파일 수가 빠진 것은 아니다. README에 열거된 15개 항목의 바이트·SHA를 모두 대조했다.

| 단계 | 원문에서 확인한 결과 | 경계 |
|---|---|---|
| 개발 RED | n1 KeyError, c1·c2 통과 | 수정 전 시험 |
| 개발 GREEN 01·02 | 각각 204 passed | dirty 개발 기록이며 02는 짧은 tail |
| 신규 변이 EXPECT | n1의 KeyError | emit 단계 rc1은 검증 PASS가 아님 |
| 신규 변이·기존 k04 재생 | 각각 rc0 | 저장된 검증 로그 |
| 전체 pytest 10a | 1 failed, 2322 passed, 1 xfailed, rc1 | 위키 raw SHA lint 실패 |
| 전체 pytest 10b | 2323 passed, 1 xfailed, rc0 | fe72f9b81, 08:00:31Z–09:39:31Z |
| strict smoke | rc0 | 168fd41a5, 03:35:39Z–03:39:41Z |
| 전체 변이 | 433 scenario, 422 executable, 11 declared, 422/422, rc0 | 168fd41a5, 03:39:41Z–07:59:44Z |

정식 검증 로그 08·10a·10b·11·12는 각 단계 시작·끝 HEAD 동일, dirty0을 기록한다. 168fd41a5→fe72f9b81의 전체 저장소 diff는 위키 raw 파일 하나다. 이 때문에 기존 smoke·변이 결과와 위키 정정 후 전체 pytest 결과를 함께 사용하는 것은 수용한다. 요청 HEAD에서 전체 pytest를 새로 돌렸다고 표현하지는 않는다.

smoke 안의 n_failed=2는 내부 합성 격자 결과이며, 최종 smoke rc0 및 실패 라벨을 포함한 검증과 구분한다. smoke는 작은 grid·fit·복원 계산을 포함하므로 제출 수행 전체를 “모든 계산 0”이라고 쓰지 않는다. 연구용 새 leg 실행과는 다르며, 수신자는 이 smoke를 다시 실행하지 않았다.

중단 run1은 34%까지의 부분 로그와 rc 부재를 그대로 둔다. 그 안에 이미 F 표식도 있으므로 성공으로 세지 않는다. 컨테이너 재시작 원인과 메모 추가 후 원래 길이로 되돌렸다는 경위는 제출자 신고다. 현재 1,555-byte Git blob은 확인했지만, 더 이른 독립 사본 없이 편집 전 원본 동일성을 별도로 입증한 것은 아니다. 후속 완료 로그의 수용과 이 중단 로그의 출처 한계를 분리한다.

## 영수증과 환경

두 leg의 c7f48918ff971e91 history는 재생성 전 현행본과 Git blob이 같다. 현행 core는 이전 core에서 validator_source_digest와 src_io_sha256 두 필드를 제외하면 같다. 검사 수 35/34, producer·bundle·산출·복원 근거는 유지됐다. 원장 앵커도 새 core와 validator digest를 가리킨다.

| leg | 현행 영수증에 기록된 core SHA256 |
|---|---|
| paired_fixed5_v4 | 68a74c60b219db4421f834c6b7756e9f741f611a4bf4bd8963cdb4f96d048bf9 |
| grid_fit_v5 | 16d3be2555fd6a4ef745ca4ed3f651be61afcd74c3ebeb5965cdd60f4c524856 |

영수증 stamp의 commit·시각·플랫폼은 갱신됐고, 환경 C MISMATCH 34는 유지됐다. paired dirty=false / grid dirty=true도 유지된다. 요청 §4의 clean은 시작 HEAD에 대한 기록이지 두 영수증 stamp가 모두 clean이라는 뜻이 아니다. 정본 환경 MATCH나 loaded-module origin 확인으로 승격하지 않는다. 이 정적 비교는 영수증 재생성·복원·재채점을 수행한 검토가 아니다.

## 회신 후 범위

G93-N1·N2 종결과 위 문서 정정을 접수하면 된다. 이번 회신 때문에 동일 코드의 시험·영수증을 다시 생성할 필요는 없다.

39개 위치 변이, C8 재개, C7 envelope와 원장 결속, run_spec 최상위·solution map header·원장 항목의 제외 세 객체는 그대로 이월한다. 이 중 다음에 다룰 한정 범위는 별도 요청·승인으로 정한다. 묶음 6 전체 종결, 새 연구 leg, class 변경, 투영 게시, 복원·COMSOL 실행 GO는 부여하지 않는다.

상세 코드·회귀·N2·영수증 근거는 notes/, 파일 식별과 Git tree 비교는 JSON 증거에 있다. 리뷰어 text view의 줄바꿈과 원문 바이트는 구분했다. 최종 LF가 없는 G94 중단 로그는 ORIGINAL_CONTENT.json의 UTF-8 content로 정확한 1,555 bytes를 보존했고, 인접 .log는 LF 하나가 덧붙은 텍스트 표시 사본임을 명시했다.
