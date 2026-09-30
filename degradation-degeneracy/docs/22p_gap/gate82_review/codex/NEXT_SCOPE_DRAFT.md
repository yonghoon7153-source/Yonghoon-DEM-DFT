# 82차 잔여 보완 범위 초안

비활성 제안이다. 사용자 별도 승인 전 코드 수정·시험·영수증 재생성·라운드 2 착수 권한이 없다.

## 목적과 변경 경계

G82-N1 관측 roster, G82-N2 지원 bank profile, G82-N3 선언 세대 연결만 닫는다. 현재 승인된 네 production 파일 안의 소비·검증 부분을 최소 수정하며, 새 production 파일이나 계산 알고리즘·ID 도메인·골든 변경이 필요하면 먼저 범위 차이를 보고한다.

관측 noise seed와 optimizer seed를 혼동하지 않는다. 관측 자료의 정확한 출처를 정하고 필요한 경우 봉인 입력과 출력 cond_id를 연결한다. 반환된 후보 수와 수치 건전성을 분리하며 Q7 때문에 최적화 동작이나 legacy ok를 바꾸지 않는다.

## 먼저 고정할 회귀

아래는 실행하지 않은 반례 설계다. 구체 node 수/예산/실행 명령은 사용자 승인안에서 확정한다.

- N1 양성: 같은 pair_group에 두 noise realization, 두 objective의 정확한 쌍.
- N1 음성: 한 objective의 noise 변경, realization 교차, 같은 n_obs의 다른 관측 집합. 파일 봉인·record 자체 해시를 일관되게 갱신한 자료에서도 관측 결속 오류로 거부해야 한다. 잘못된 JSON/누락 파일만으로 음성을 대신하지 않는다.
- N2 양성: 현재 pcg64·지원 version·seed rule·float64·little-endian profile, 정상 bank/candidate 바이트 불변.
- N2 음성: envelope/design generator 불일치, 양쪽이 같은 미지원 generator, version 불일치, dtype/endian/seed rule 불일치. 실행 전 소비자와 최종 validator 모두의 도달 단계·정확 이유를 확인한다.
- N3 양성: 계획/record/행/sig의 지원 세대 일치 및 기존 legacy/prep 호환.
- N3 음성: sig6 아래 계획과 record가 함께 v5인 자료, 서로 다른 세대 자료. 임의 파싱 오류가 아니라 선언 충돌로 거부해야 한다.

이미 수용된 provider·후보·legacy 시험을 필요 없이 새 결함으로 재분류하지 않는다. 기존 회귀와 변이는 영향 범위에 맞춰 유지한다. 이번 리뷰는 그 실행을 승인하지 않는다.

## 봉인과 기록

원본 영수증·history·실패·2004 PASS 보고를 소급 변경하지 않는다. 보완 후 코드가 확정되고 사용자 승인 범위가 정해지면 새 validator 세대에 필요한 영수증·원장 앵커를 일치시키고, 해당 최종 조합의 회귀를 보고한다. 현재 2차본을 지금 다시 만들지는 않는다.

제출물은 최소 diff, 이유별 회귀/변이, 세 선언 대응표, 관측 roster의 출처와 소비 경로, 새 source 식별 및 보존 비교다. 읽기 전용 검토에서 제안한 반례를 실제로 검증했는지 분리해 적는다.

새 연구 leg·floor·pilot·실행 GO·COMSOL·class 변경·투영 게시·p_ini 구현·라운드 2 착수는 포함하지 않는다.
