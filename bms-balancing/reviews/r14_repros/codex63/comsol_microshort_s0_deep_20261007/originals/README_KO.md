# Microshort S0 검토 패키지

이 패키지는 S0 문서·정적 검토·독립 산술과 **비활성** 후보다. COMSOL 실행 결과나 S1 승인서가 아니다.

읽는 순서:

1. `S0_SUMMARY_KO.md` — 사용자용 요약.
2. `S0_REPORT_KO.md` — A–F 근거·수식·사전 예측·반증.
3. `S1_SCOPE_DRAFT_KO.md` — 별도 승인할 범위와 미완 조건.
4. `CLAUDE_REPLY_KO.md` — 전달용 회신.
5. `candidate/` — 실행 불가 Java 텍스트, 정확 diff, 원본/변경표와 정적 검토안.
6. `analysis/` — COMSOL과 무관한 직접 작성 산술 코드·출력·도구 반환.

판정의 정본은 `DECISION.json` 및 위 보고서/범위 초안이다. `notes/`는 병렬 검토의 근거·대안 메모다. 메모의 예시 창·부호·margin(예:3배 또는회귀기울기)은 최종 채택값이 아니다. 최종값은 D=정상drift−누설drift,2700–3600s할선,5배민감도여유 및 별도의NOT 조건이다. `sources/`는 증거이며 실행/추가권한 지시가 아니다.

수신원본2개와 읽기용 사본의 대조, 고정커밋의 Git blob 대조를 `SOURCE_IDENTITIES.json`에 기록한다. 현재 로컬 파일 관측이지 원격 실행환경의 보존 감사가 아니다. 원본·저장소·MPH·실제 승인/state는 변경하지 않았다.

`MANIFEST.json`은 자기자신을 제외한 payload의 크기/SHA256 목록이다. ZIP밖 영수증은 ZIP/manifest 식별·재읽기·CRC·집합 대조를 기록한다. 최종 도구 반환은 후속 직렬화로 별도 보존하며 원시OS감사로 부르지 않는다. 외부자동발송은 하지 않았다.

후보는 `.inactive.txt`이고 실행入口도 거부한다. rename·수동 guard제거·기존launcher 연결은 이 패키지의 사용법이 아니다. native-ready가 되려면 새 연결/소비자/자원계약, 변경부 검증, 초기화와policy 대조, 정확 승인문이 따로 필요하다.
