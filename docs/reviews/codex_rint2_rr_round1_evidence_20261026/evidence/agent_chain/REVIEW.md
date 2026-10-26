# Chain review — pinned 2026-10-26 source

검토 핀: `9bec6b7646374daed0d3edbb9647f9f46d302750`. 비교 기준: `0b3012460fb8e8b7d53484b0efe399e2dc506aec`.

**판정: RCA2-09 최소 해결 닫힘. 사전 공격 C3/C4 닫힘. 이 범위에서 새 차단 결함은 확인하지 못했다.** 이는 실제 침대의 R 단조성 또는 연속 R·전체 origin을 새로 입증한 판정이 아니다. 검사된 것은 실제 판정 함수가 입력 증서 구간의 모순을 잡는지이다.

## 근거와 범위

- 실제 `Predict`, `arm_band`, `mean_band`, `r_monotone_problem`, `target_judge`를 불러 판정했다.
- Python 3.12.14, Windows. 순수 판정 입력·작은 정확 분수 열거만 사용. production solver, S0/DEM/R 런, Git 변경은 하지 않았다.
- production 소스 무변경. 산출은 이 폴더와 `tmp/chain`만 사용했다.
- `comparison.json`은 비교에 사용한 4개 파일 × 두 핀의 SHA256 및 Git blob을 `evidence/source_manifest.json`과 대조한다. 불일치 0.
- 선택한 상주 검사 10개(U17/U17b/U19/U20/M44/M45/M46/M47/M49/M50)는 `fixtures()`·CLI·가짜 러너 없이 함수로 직접 호출하여 10/10 통과했다. 전체 사슬·실러너 끝-끝 240/240을 이 실행이 재현했다고 주장하지 않는다.

## RCA2-09 / C3

현재 자리:

- `scripts/rint_r_chain.py:464–477`: 모든 R 쌍의 구간 순서 비교. 같은 R이면 떨어진 구간을 거부.
- `:480–486`: 최종 추정량 = arm0 또는 동일 8팔 평균 구간.
- `:495–502`: 이미 구한 origin마다 세 R를 구성.
- `:1857–1877`: 원 origin 및 확대한 8팔 기록을 보존.
- `:1882–1913`: 최종 추정량과 origin별 구간 검사, 모순 시 `R_MONOTONE_VIOLATION`.
- `scripts/test_rint_r_chain.py:2866–2922,2933–2947,3028–3079`: 원 반례, 전쌍, 같은 R, origin 회귀.

실제 실행 `chain_review_probe.json`:

| 입력 | 현재 함수 판정 | 확인한 내용 |
|---|---|---|
| R=.5/1/2, σ=4.2/4.7/4.4 mS/cm | R_MONOTONE_VIOLATION | 10-22 원 방어검사 반례 닫힘 |
| origin1=4.80/4.85/4.40, 나머지=5/4.7/4.4; c1=c0×1.5 | R_MONOTONE_VIOLATION, 조정 0 | 먼저 c/origin 검사에서 막히지 않은 C3 반례; origin_a1 사유 |
| origin0=4.6/4.7/4.4, 나머지=5/4.7/4.4 | R_MONOTONE_VIOLATION, 조정 12 | 최종 mean8 단조 통과 후 corner_a0가 검출 |
| origin1·2의 lo×1.08; origin3=4.4/4.7/4.4 | R_MONOTONE_VIOLATION, 조정 12 | 최종 mean8 단조 통과 후 origin8_a3가 검출 |
| 정상, 평탄, hi 정상 topology zero | PREDICTED | 과잉 거부 없음 |
| nominal lo=4.69995 < center=4.7, 증서 구간 겹침 | PREDICTED | nominal 오름만으로 거부하지 않음 |
| 모든 origin 단조지만 확대 필요 | PREDICTED, 조정 12 | 11개 기록 스트림 전부 검사 |

별도 정확 분수 기준: 끝점 0,1,2,3으로 가능한 10개 구간의 3점 곱 × R 순서/같음 5형 = **5,000회**. 각 구간에서 실제 단조 선택값이 존재하는지를 독립 전수열거하여 `r_monotone_problem`과 비교: 거짓 승인 0, 거짓 거부 0. 이 유한 검사는 전칭 증명을 대체하지 않는다. 수학적으로도 단조 선택 가능성은 각 앞 구간의 위끝이 모든 뒤 구간의 아래끝 이상인 조건과 일치한다(같은 R 그룹은 먼저 교집합).

저자 `preattack2/tools/atk2_rmono.py` 재실행의 증거 한정도 기록한다. 그 파일의 R1 “no overflow”는 실제 조정이 생기며, R1c는 `SAME_P_CONSISTENCY`에서 먼저 멈춘다. 이 출력만으로 두 의도한 분기를 확인하면 안 된다. 위 독립 입력 및 상주 U19는 그 가림을 제거하여 의도한 R 검사에 도달한다. 코드 결함으로 세지는 않는다.

## C4 / C6 선택

- `scripts/rint_r_chain.py:435–454`: 증서의 `scale × [target_lo,target_hi]`를 정확 분수로 비교한다.
- `:457–461`: 팔마다 자기 scale의 양끝을 먼저 환산하고 정확 평균.
- `:1431–1435`: 원 증서에서 err_rel 재계산.
- `:1456–1459`: 원 증서의 목표 구간과 scale을 판독 팔로 전달.
- `scripts/test_rint_r_chain.py:3133–3188`: C4 경계 및 누락/잘못된 칸 검사.

원 C4 칼날: A의 위끝=B의 아래끝=`1.4656880073121192`이면 통과. B의 아래끝만 `nextafter(+inf)=1.4656880073121195`로 바꾸면 모순. scale=0.001을 곱한 뒤에도 동일하며, 8개 서로 다른 scale의 평균은 독립 정확 분수 식과 같다. A/B err_rel은 각각 `2.588422238019952e-05`, `1.0048255880306897e-05`이다.

C6 관련 판단:

- 증서 구간 자체를 띠로 사용하고 τ_mono를 더하지 않는 것은 타당하다. 더 넓은 임의 띠로 실제 인증 구간의 모순을 덮을 필요가 없다.
- 인증 scale 사용도 타당하다. 게시 σ/I_bot을 역산하면 추가 반올림이 생긴다.
- `R_MONOTONE_VIOLATION`을 표지가 아닌 STOP으로 처리하는 선택은 등록 §10과 정합한다.
- `checks.r_monotone[].ok`가 최종 추정량 결과이고 `origins`가 별도라는 형식은 문서대로다. 소비자는 ok만 보아 전체 통과로 해석하면 안 된다. 현재 실행은 origin 실패에서도 Stop하므로 새 거짓 승인 결함으로 세지 않는다.
- 원 기록 구간칸이 없는 합성 입력의 ARM_UNREADABLE은 의도한 새 계약이다. 실제 원 증서 검증을 우회하는 direct arm_band 호출에서 sigma/상태/구간 일관성까지 전부 검사하지 않는 것을 production의 거짓 승인 증거로 세지 않았다.

## C7 — 기존 registration 탐침 적응

`registration_adapter.py`는 원 `rint2_rereview_20261022/registration/probe_registration_current.py`를 그대로 로드한 뒤 합성 `arm()`에만 목표 구간 1±err, scale=σ를 넣는다. zero는 세 칸 None. production 함수는 패치하지 않는다. 원 반례의 새 Stop을 기록하고 probe-owned JSON fixture 출력만 `tmp/chain/<label>`로 보낸다.

- 적응 baseline vs 10-22 원 JSON: **466/466 scalar leaves exact**, 차이 0.
- current vs baseline의 `DBE_R_monotonicity` 절 제외: **457/457 scalar leaves exact**, 차이 0.
- 유일하게 바뀌는 절: σ=4.2/4.7/4.4가 `PASS_INFORMATIVE`에서 `R_MONOTONE_VIOLATION`으로 바뀜.
- 따라서 증서 칸 없는 옛 입력에서 난 ARM_UNREADABLE을 고침의 검출 성과로 세지 않았다.

아래 **기존 한정은 현재도 그대로**다:

1. 세 origin 표본은 `W=0.2930476573691437`, PASS; 고정8 평균은 `W=0.6803855313301495`, WEAK인 이전 해석 반례가 동일하다.
2. `all3`라도 SV 요청은 corner 12, origin 0, origin8 0이다. 최종 값 12개가 모두 8팔 평균으로 확대되어도 그대로다. 현재 위치는 `scripts/rint_r_chain.py:1841`(corner SV), `:1859`(origin), `:1872`(origin8), `:2541`(판정의 `pr.vals` 소비)이다. 이번 R 단조 수정이 SV 평균 범위까지 넓혔다고 읽으면 안 된다.

## C3 / C8 단계 진입에 대한 이 범위의 의견

이 R 검사는 DBE Predict 경로다. 이 범위에서 S0 단계 1 개발 자료 또는 SBE 숫자 탐침을 새로 막아야 할 결함은 확인하지 못했다. 그렇다고 등록 R 실행 HOLD를 해제하는 것은 아니다. 같은 코드·같은 침대 귀속(묶음 B), 실행 봉인(묶음 C), 원 SV scope의 한정은 별개다. X6/X3/X5의 전체 판정은 SV/census 담당 증거와 합쳐야 한다.

## 재현

리뷰 폴더를 현재 디렉터리로 두고 PowerShell:

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B evidence/agent_chain/chain_review_probe.py --repo repo
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B evidence/agent_chain/registration_adapter.py --repo repo --original ../rint2_rereview_20261022/registration/probe_registration_current.py --label current
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B evidence/agent_chain/registration_adapter.py --repo baseline --original ../rint2_rereview_20261022/registration/probe_registration_current.py --label baseline
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B evidence/agent_chain/compare_registration.py
```




