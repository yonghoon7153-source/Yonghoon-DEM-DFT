# REIL C4 사전 검토 · C5 비용 한정 수용 · 실행 환경 결정

2026-10-13 · 문서/코드 정적 검토. 실행 승인문이 아니다.

## 판정

**C5 비용 기록은 한계와 문구 정정을 붙여 수용한다. C4 단계 구조·실행 수 산술은 적합하나, 요청문은 수정 조건부 적합이다. 환경 준비는 별도 승인 대상이며 현재 C4-0을 바로 시작할 상태는 아니다.**

검토 시작 때 브랜치 `claude/14-gate-code-review-9qkx05`의 HEAD를 **6014b206935b7f1969ba617a1d41fd943925663e**로 고정했다. 이후 아래 좌표와 판정은 모두 이 커밋에 한정한다. GitHub 읽기 API로 확인했으며 실행 기계에 checkout/fetch하거나 그 상태를 관측하지 않았다.

사용자의 기존 C4-0 승인 기록을 취소하는 판정은 아니다. 다만 이번에 드러난 감시 보완·시험 횟수 명확화는 구현 범위에 영향을 주므로, 요청문 §0의 조건대로 정정 범위를 사용자에게 재확인해야 한다. 설치·새 봉인 채택은 그와 별도의 권한이다. C4-E/A/B·자료 개봉·실제 맞춤 승인은 없다.

## 1. 발견 사항

### C4-N1 · P1 — 환경 재봉인의 실제 계산과 새 봉인 채택 조건이 승인 범위에 빠져 있다

근거: [reil_c6_profile.py:170](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c6_profile.py#L170), [reil_c6_profile.py:191](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c6_profile.py#L191), [reil_c6_profile.py:222](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c6_profile.py#L222), [reil_c6_profile.py:237](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c6_profile.py#L237), [reil_c5_pilot.py:675](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L675), [REIL_C5_PILOT_APPROVAL_REQUEST_v2_ADDENDUM_20261006.md:8](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C5_PILOT_APPROVAL_REQUEST_v2_ADDENDUM_20261006.md#L8).

현재 Python 3.11.17에 같은 패키지 판을 설치하는 것은 이전 CPython 3.11.15/2026-03-03 빌드 환경의 동일 복원이 아니라 **새 환경 세대의 제안**이다. 기존 PROFILE과 lock의 바이트 대조를 약화하여 통과시키면 안 된다.

또한 `emit`은 합성 COBYQA 최적화와 Sobol 생성 경로를 실행하며, `check`도 임시 폴더에서 `emit`을 다시 호출한다. 따라서 emit 1회 + check 1회에는 **합성 최적화 2회와 전체 배열 생성 경로 2회**가 들어 있다. 연구 자료의 맞춤은 아니지만 “설치·메타데이터 확인만”도 아니다.

새 emit/check의 일치는 새 환경 내부의 재현 일치일 뿐이다. 과거 봉인과의 차이를 허용하는 판정까지 수행하지 않는다. 새 환경을 곧바로 C4 봉인으로 자동 채택하지 말고 다음을 대조해야 한다.

- 과학 환경의 전체 배포판 30개 집합·판, Python 판/빌드, 플랫폼/libc, BLAS/LAPACK 메타데이터.
- RECORD·설치 파일 검증·충돌 목록. 같은 버전이라는 이유로 새 RECORD 차이를 포괄 수용하지 않는다.
- COBYQA 8개 옵션·구현 파일 4개 SHA, 기존 Sobol 6개 배열의 .npy 바이트 및 raw float64 해시.
- 새 봉인의 정확 경로·MANIFEST와 C4 실행기가 실제 참조하는 봉인의 연결. 옛 기본 경로를 암묵적으로 물려받지 않는다.

기존 30개 배포판 lock에는 pytest/pluggy/iniconfig가 없다. 이전 시험은 별도 `pytest_t` 경로를 사용했다. 그 경로의 현존 여부는 미확인이다. 기존 시험 도구를 식별해 재사용하거나, 필요한 시험 전용 환경을 별도 명시해야 한다. “동일 30개 설치 완료”를 C4-0 시험 준비 완료로 부르면 안 된다. 근거: [REIL_C5_PILOT_APPROVAL_REQUEST_v2_ADDENDUM_20261006.md:38](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C5_PILOT_APPROVAL_REQUEST_v2_ADDENDUM_20261006.md#L38).

**최소 조치:** 별도 C4-ENV 승인문에 설치·합성 자기점검의 실제 횟수·old→new 대조·새 봉인 채택 경계를 명시한다. 임의 차이는 중지하고 새 승인을 받는다. 이 P1은 제안된 승인 경로의 누락이며, 이번 검토에서 실제 무단 설치가 있었다는 지적이 아니다.

### C4-N2 · P2 — 기존 감시기는 늦게 도착한 성공 표본의 공백을 놓친다

근거: [reil_c5_pilot.py:469](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L469), [reil_c5_pilot.py:488](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L488), [reil_c5_pilot.py:498](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L498), [reil_c5_pilot.py:504](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L504), [reil_c5_pilot.py:515](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L515).

현재 코드는 RSS/디스크 표본이 `None`일 때만 마지막 표본 이후 공백을 검사한다. 값이 성공적으로 반환되면 먼저 마지막 시각을 갱신한다. 예컨대 5초를 넘겨 도착한 RSS 성공 표본도 이 경로에서는 누락 중단을 피한다. 시각도 표본 호출 전에 취득하므로 수집 지연을 온전히 나타내지 못한다. 이는 소스 제어 흐름으로 확인한 반례이며 이 검토에서 실행한 시험이 아니다.

**최소 조치:** C4용 감시에서는 수집 전후 시각과 유효 표본 간격을 기록하고, 성공 여부와 무관하게 공백을 검사한 뒤 마지막 유효 시각을 갱신한다. 늦은 성공 반환 후에도 마감·중단 조건을 재확인한다. 합성 시험에는 늦은 성공, None, 예외, 최초 표본 지연을 넣는다. OS 조회 자체가 영구 블로킹될 때의 강제 종료를 보장한다고 확대하지 않는다.

C5의 보존 RSS 표본에서 최대 기록 간격은 약 1.00767초였다. 따라서 이 결함만으로 과거 C5 실행이 실제 5초 누락 조건을 위반했다고 판정하지 않는다. C4의 더 긴 실행에 기존 함수를 수정 없이 재사용할 수 없다는 지적이다.

### C4-N3 · P2 — 산출량 감시와 자체 산출 경로 분류가 불완전하다

근거: [reil_c5_pilot.py:364](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L364), [reil_c5_pilot.py:626](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L626), [reil_c5_pilot.py:813](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L813), [reil_c5_pilot.py:826](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L826).

산출량 표본은 본체 폴더만 포함하고, 마지막 결과 파일은 감시 종료 뒤 작성한다. 래퍼 로그까지 포함하는 “새 산출 ≤1 GiB”와 동일하지 않다. `split_dirty`의 접두사 비교도 경로 경계를 보지 않아 `out_wrapper/` 또는 `out_backup/`을 `out/` 소유 범위로 받아들일 수 있다.

**최소 조치:** 본체·래퍼·임시/최종 기록의 정확한 소유 루트를 미리 열거한다. 경로는 정확 일치 또는 구분자 뒤 하위 경로만 허용한다. 감시와 종료 기록 후 크기 대조를 같은 파일 집합으로 수행하고 마지막 관측의 범위를 명시한다. Git 상태 원문은 분류 결과와 별도로 보존하며 모호한 경로 표기를 자체 산출로 간주하지 않는다.

보존된 C5 본체 191,753 B + 래퍼 237,656 B = 429,409 B로, 이번 과거 자료의 실제 합계는 1 GiB 이내였다. 원 실행 기록을 다시 쓰거나 실패로 소급 변경할 이유는 없다.

### C4-N4 · P2 — 등록 규칙과 충돌하는 요약 문장 세 곳

근거: [REIL_C4_APPROVAL_REQUEST_20261007.md:31](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L31), [REIL_C4_APPROVAL_REQUEST_20261007.md:35](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L35), [REIL_C4_APPROVAL_REQUEST_20261007.md:66](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L66), [REIL_C4_APPROVAL_REQUEST_20261007.md:90](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L90).

1. H3의 `(1+δ)Ĵ` 요약을 단일 목적과 결합 ρ로 나눈다. 단일 목적은 `J_o≤(1+δ)Ĵ_o`, 결합은 `ρ=max(J_V/Ĵ_V,J_D/Ĵ_D)≤1+δ`이다. ρ 자신의 발견 최소를 다시 곱하지 않는다. H4는 `T_s=Ĵ_s+2σ̂_v`로 분리한다. A:81,89–93.
2. “대체 없음/대체 시작 금지”는 등록된 대체 사슬까지 금지한다. B:108–111,119의 이웃 증인→다음 Phase A 증인 사슬은 유지하고, 임의 대체·복제·추가 시작만 금지한다. 등록 사슬이 소진되면 시작부족이다.
3. “동시 Sobol 12 봉인”은 **16개 전체를 생성·봉인하고 앞 12개를 사용**하는 규칙으로 고친다. B:99,120 및 C5v2:108–112.

이는 새 과학 규칙 제안이 아니라 이미 유효한 프로토콜을 정확하게 옮기는 정정이다.

### C4-N5 · P2 — RED→GREEN과 “시험 집합 1회”의 권한이 모호하다

근거: [REIL_C4_APPROVAL_REQUEST_20261007.md:48](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L48), [REIL_C4_APPROVAL_REQUEST_20261007.md:68](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L68), [REIL_C4_APPROVAL_REQUEST_20261007.md:69](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L69), [REIL_C4_APPROVAL_REQUEST_20261007.md:77](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L77).

RED를 관측하고 구현한 뒤 GREEN을 확인하려면 시험 호출은 적어도 두 번이다. “단계 1회/재시도 0” 및 “시험 집합 1회”와 함께 읽으면 범위가 불명확하다.

**최소 조치:** RED 1회, GREEN 1회, 전체 C6 자기점검, 배열 봉인, 건조 1회를 별도 항목으로 명시하고 합산 계산시간 ≤1,800초와 전체 작업시간 ≤4시간을 함께 유지한다. 이는 권고안이며 사용자가 횟수를 재확인하기 전 실행할 권한이 아니다. GREEN의 예상 밖 실패 뒤 자동 수정·재시험은 금지한다. 새 환경의 check 1회를 C4의 전체 자기점검 1회로 인정하면 중복 check를 요구하지 않는다. 환경 승인과 C4-0의 시간 원점은 별도다.

### C4-N6 · P2 — 비용 보고의 범위·중앙값·CPU 표현을 정정해야 한다

근거: [REIL_PREREQUISITES_STATUS_20261004.md:480](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md#L480), [REIL_PREREQUISITES_STATUS_20261004.md:483](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md#L483), [reil_c5_pilot.py:551](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L551), [reil_c5_pilot.py:579](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/scripts/reil_c5_pilot.py#L579), [REIL_C4_APPROVAL_REQUEST_20261007.md:42](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L42), [REIL_C4_APPROVAL_REQUEST_20261007.md:52](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L52).

- 내부 평가 횟수 범위는 **96–1006**이다. 103–851이 아니다. 851은 최빈값(12건)이다.
- 기록의 1.657817164초는 128개 정렬 자료의 **위쪽 중앙 순서통계**이다. 통상적인 두 중앙값 평균은 **1.6506008645초**다. 기존 JSON을 덮어쓰지 말고 정정 설명을 붙인다.
- 5.113 ms = local-run wall 합 238.9924658초 / 내부 평가 46,741회다. solver 부대 처리·독립 재평가·라벨 처리까지 포함한 분할 비용이며 고립된 목적함수 호출 시간이나 CPU 시간은 아니다. 실제 local CPU 합은 231.8955988초다.
- “RSS 최대”는 408개 보존 표본의 최대 941,879,296 B이다. 순간 최대 또는 OS 강제 상한 입증이 아니다.
- “산출 192 KB”는 본체만이며 래퍼 포함 합계는 429,409 B다.
- ST:480의 배열 해시는 .npy 파일 해시와 raw float64 payload 해시를 구분해서 표기한다. 발견된 해시 불일치는 아니다.

### C4-N7 · P2 — 시간 추정과 실제 실행 상한을 분리해야 한다

근거: [REIL_C4_APPROVAL_REQUEST_20261007.md:9](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L9), [REIL_C4_APPROVAL_REQUEST_20261007.md:50](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L50), [REIL_C4_APPROVAL_REQUEST_20261007.md:56](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_C4_APPROVAL_REQUEST_20261007.md#L56), [REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md:271](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md#L271).

C4-A 1.3/7.0시간, C4-B 5.8/31.7시간의 산술은 맞다. 그러나 “maxfev까지 모두 실행하고 평가당 비용이 C5와 같다”는 가정의 추정이지 시간의 최악 보증이 아니다. E3a pymoo 경로, 다른 상자/목적, 1차원 평가, 시작점 구성, 독립 재평가, H4 대조/ray, 로그·종결 비용은 같은 단가가 보장되지 않는다.

109,817,477도 국소 solver 평가와 명목 격자 평가의 상한이며 독립 재평가·H4 대조/ray·E3a를 모두 포함하는 총 호출 상한이 아니다. 별도 횟수 장부를 둔다.

**최소 조치:** “최악”을 “maxfev 포화·동일 평균단가 가정 추정”으로 바꾸고, 단계 예산은 준비부터 소유 정리·최종 기록까지 포함하는 실제 한도로 정의한다. 연구 실행 승인 전에 종료/기록 reserve와 내부 마감을 고정한다. §3의 “예: 중앙 3배”는 구현 가능한 고정 규칙이 아니므로 기준 통계·최소 표본수·판정 창·중단 시점을 결과를 보기 전에 명시한다. 이 미정은 지금 예산 사전 의견을 막지 않지만 C4-E/A/B 실행 승인 전에는 닫아야 한다.

## 2. 수용한 설계·산술

| 항목 | 대조 판정 |
|---|---|
| 단계 | C4-0 → C4-E → C4-A → C4-B 적합. E3a 미완 시 H 금지. 각 실행 승인 별도 |
| E3a | 노트북을 실행하지 않고 보존 util의 run_optimization 직접 호출. 6 case×11셀=66 외부 호출=275 optimizer 호출 |
| E3a 평가 추산 | 선택 경로의 GA20×100세대, NSGA2/3 100세대 적용. pop×세대 산술 1,501,500은 맞음. 실측 호출 수/엄격한 총 평가 한도는 아님 |
| H unit | 33(J_V)+22(J_D·ρ)+22(H4)=77 |
| Phase A | 77×128=9,856 |
| 명목 전체 | ≤54,901 국소 실행 |
| P0 반영 | 동시 −320, 명목 정제 −32 → ≤54,549, Phase B ≤44,693 |
| profile | 3좌표 각각 ≤46점×명목4시작. 부족/등록 대체 규칙 적용 |
| 세대·금지 | E3b 미등록, C5 과학 결과 재사용 금지, H4의 철회된 반증 주장을 되살리지 않음 |

E3a의 별도 `run_nsga` 함수에 있는 150세대를 가져오지 않았다. 실제 선택 함수의 100세대와 맞는다. 근거: [util_LFP.py.txt:564](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/reviews/prereview_pybamm_reil_20261003/external/util_LFP.py.txt#L564), [util_LFP.py.txt:682](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/6014b206935b7f1969ba617a1d41fd943925663e/bms-balancing/reviews/prereview_pybamm_reil_20261003/external/util_LFP.py.txt#L682).

## 3. C5 비용 증거의 수용 범위

128개 고유 run ID·worker 배치와 비용 필드, 자원 표본, 기록 식별만 대조했다. 맞춤 J·증인 순위·명목 거리·맞춤 상태를 요약하거나 판정하지 않았다.

- 내부 평가 46,741회, 독립 재평가 시도 128회의 비용 장부가 연결된다.
- 측정 wall 약 63.28초, 내부 최종 snapshot 71.108초, 외부 래퍼 약 71.71초는 서로 다른 경계다. 더하거나 하나로 바꾸지 않는다.
- 실행 HEAD 시작·끝은 `b76418680550c1a16a23455e16bf45c648b6f7af`. 소스·기준 해시와 Model/halfcell 기록상 전후 식별이 같다.
- 본체 증거 네 파일의 수신 바이트 SHA는 외부 기록과 일치한다. 실행본도 현재 검토한 스크립트와 같은 바이트다.
- raw 작업트리 시작/종료 기록에는 본체/래퍼 산출 경로가 보존되어 있다. 잘못된 접두사 분류를 무변경·clean tree 증명으로 쓰지 않는다.
- lock/profile/MANIFEST의 실행 기록 결속은 있다. 원자료의 당시 보존을 지금 직접 재측정한 것은 아니다.
- RSS 표본 최대와 관측 디스크 여유/보존 파일 합계는 제한 이내다. 샘플 사이 순간 피크·모든 시각의 디스크 크기·원시 OS 감사까지 수용하지 않는다.
- C5 구현 단계에 기록이 없는 첫 import 실패가 있었다는 신고는 유지한다. 그 호출 시간까지 포함한 구현 단계 전체시간을 새로 복구하거나 “완전 기록”으로 승격하지 않는다. 이는 보존된 비용 측정 단계의 수치·원문 결속과 별개다.

**결론:** `C5_COST_EVIDENCE_ACCEPTED_WITH_DOCUMENTED_LIMITS`. 비용 자료 무효나 C5 재실행을 요구하지 않는다. C4용 감시·기록 보완은 위 C4-N2/N3의 한정 구현 및 합성 검증으로 처리할 수 있다.

## 4. 요청문 §5의 일곱 결정

| 결정 | 의견 |
|---|---|
| 1 함께 검토 | 동의. 이번 회신에서 수행 |
| 2 E3a 직접 호출 | 동의. 보존 util·case 상수 결속, 노트북 실행 없음 |
| 3 REEVAL_ERROR | 동의. 독립 재평가 사건/증인 무효 이유로 별도 기록하고 solver termination을 덮어쓰지 않음 |
| 4 unclassified | 동의. 알려진 셋으로 임의 매핑하지 말고 구조적 미분류로 전체 중지·기록. 지역 budget과 구별 |
| 5 전체 환경 자기점검 | 동의하되 실제 계산 권한과 중복 횟수 정정. 수용된 새 환경 check를 1회분으로 인정하는 안 권고. E/A/B 시작은 해당 봉인 identity 대조 |
| 6 지난 사본 삭제 | 현재 불필요. 약26 GB는 제출자 관측이며 검토자 직접 관측 아님. 다음 실행 직전 여유 재확인. 삭제 승인 없음 |
| 7 B 후속 예산 | 동의. C4-A 비용 뒤 새 승인. 결과/참값 적합성에 따라 과학 규칙·시작점·영역을 바꾸는 권한은 아님 |

## 5. 환경 물음에 대한 선택

**권고: 새 환경 준비를 별도 C4-ENV 1건으로 먼저 승인하고, old→new 대조와 새 봉인 수용 뒤 C4-0을 재개한다.**

현재 interpreter의 같은 패키지 판 재설치는 선택할 수 있다. 다만 “이전 환경과 동일”이 아니라 사전에 정한 차이를 가진 새 환경이라고 기록한다. 30분·디스크 2 GB는 제안 상한으로 둘 수 있으나 설치 완료 가능성을 보증하지 않는다. GB는 승인문에서 2,000,000,000 B로 명시하는 안을 제시했으며 다른 단위를 택하려면 수치를 다시 적는다.

정확 복원도 원칙적으로 가능 경로지만 판 문자열만 같아서는 안 된다. 빌드·플랫폼·설치 바이트까지 맞는 아티팩트가 실제 확보 가능한지는 미확인이다. 어려움을 이유로 기존 식별 대조를 약화하지 않는다.

C4-0을 코드 작성만 먼저 하는 단계로 나눌 수는 있지만, 현재 사용자 결정의 순서를 바꾸므로 다시 선택을 받아야 한다. 이 검토에서는 자동 분할·착수를 하지 않는다.

반복되는 컨테이너 교체에는 **승인된 동일 환경 아티팩트의 제한된 복원**과 **새 interpreter/패키지/RECORD 세대 채택**을 구분한다. 전자는 정확 아티팩트·경로·횟수·예산을 사전 승인할 수 있다. 후자는 매번 별도 차이·승인이 필요하다. “같은 버전 재설치 후 emit/check만 되면 자동 채택”하는 포괄 규칙은 권하지 않는다.

실제 새 환경의 경로·현재 interpreter·시험 도구 식별은 실행 측에서 아직 확정해야 한다. 동봉 승인문은 이 필드가 채워지고 사용자에게 승인받기 전에는 비활성이다. 새 환경의 check 통과도 E/A/B 실행 GO가 아니다.

## 6. 이번 검토의 경계

허용된 문서·소스·기록을 읽고, 검토자 자체 도구로 비용 산술·텍스트/파일 식별만 대조했다. xlsx/pkl/노트북을 열지 않았고, 수신 source의 import/실행·합성 시험·Sobol 재생성·설치·환경 재구축·COMSOL은 0회다. 과학 코드나 원본 기록을 고치지 않았다. 공개/외부 발송도 하지 않았다.

산출물: 이 보고서, 요청문 최소 정정안, 비활성 C4-ENV 승인 초안, Claude 회신문, DECISION.json, 비용만 남긴 C5_COST_AUDIT.json, 출처/무결성 목록. 검토 결과의 수용과 사용자 실행 권한을 분리했다.
