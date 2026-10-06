# GATE93 검토 회신

판정: **수정 후 재검토**. 요청 커밋 `0e3c244ea79db1b17f09a8f8043d808ab51ff43c`, 코드 `d7a97aa57ea926916d56c985ee4bc2bed96fa81a`를 정적으로 검토했습니다. 수신 코드·시험·분석기·COMSOL은 실행하지 않았습니다.

G92-N3의 사본 9키 대조(helper 6 + env 직접 3), 기존 재계산 분리, provider edge canonical digest 통일은 수용합니다. 닫힌 stage3/map의 기본 검사와 이유별 시험 구성도 확인했습니다. RUN_SCOPE 60개 중 변경은 io.py/fitting.py 둘뿐이며 코드→검증→요청 커밋 차이는 0입니다.

잔여는 두 건입니다.

1. **G93-N1 P2 — v6 경로의 유효 v3 envelope 차단 누락.** `io.py:1896`의 공통 reader는 유효한 planned-leg/v3에 ebad=[]를 돌려줍니다. v6 schema 검사와 축 유도는 실패하지만 `:2021`은 ebad만 보므로 정상 map/fits가 있으면 `:2033`에서 재유도로 넘어갑니다. 설계 SHA를 대조군과 맞춘 경우 `:1686`의 v4 전용 parameter_order_sha256 접근에서 KeyError로 빠지는 정적 경로가 남습니다. 현재 k04_env의 philox 사례만으로 이 경로는 닫히지 않습니다.
   - 역사적 reader를 바꾸지 않고 v6 경계에서 v4 schema+구조 유효성을 함께 차단 조건으로 삼아 주세요.
   - 실제 validate_provenance의 sig6/유효-v3 음성에 구조화된 실패·재유도 0을 단언하고, 정상 v4 및 planned_id 단독 불일치의 기존 의미를 유지해 주세요. 수정은 사용자 승인 범위를 확인한 뒤 진행합니다.
2. **G93-N2 P2 — 원문 로그 인계 누락.** 증거 커밋 2ab61069b 및 요청 커밋의 gate93_evidence에는 README만 있습니다(비절단 Git tree 확인). 00/03/04/05/06/08/10/11/12 및 aborted 당시 원문을 파일별 크기·전체 SHA·실행 상태와 함께 보내 주세요. 아직 2320 PASS·smoke rc0·421/421·clean 시작/종료는 제출자 보고로 구분합니다. 없는 원문을 재실행으로 대체할 필요는 없습니다.

두 leg의 history 바이트 보존, core의 두 validator identity 외 불변, 검사 35/34와 원장 앵커는 정적 대조로 확인했습니다. stamp의 C MISMATCH34와 grid dirty=true를 그대로 인정하되 정본 환경 일치로 승격하지 않습니다. 원문 보충 전에는 재생성·전체 검증 실행 증거의 최종 수용을 보류합니다.

다음 제출은 위 차단 잔여와 당시 로그 보충으로 한정해 주세요. 39개 위치 변이·C8 재개·C7 원장 결속·제외 세 객체는 그대로 이월입니다. **묶음 6 전체 종결·실행 GO·새 연구 leg 승인이 아닙니다.**
