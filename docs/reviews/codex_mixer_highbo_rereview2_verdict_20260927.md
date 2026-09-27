> **수신 기록** — Codex 적대 **3차 리뷰** 판정문 원문 (사용자 업로드 ZIP 안의 `codex_review_mixer_highbo_round3_20260927.md`, 2026-09-27 밤 KST 수신 · 고정 스냅샷 `20568797b` · 요청서 = `docs/reviews/codex_mixer_highbo_rereview2_request_20260927.md` · 2차 판정 = `docs/reviews/codex_mixer_highbo_rereview_verdict_20260927.md`).
> **한 글자도 바꾸지 않았다** (34,438 B · sha256 앞 16 자리 f52f4d0eeb76bcdb — 로컬 경로 링크 · 백틱 hex 가 없어 2차 때의 변환이 필요 없었다).  ZIP 187745 B.
> 재현 묶음의 증거 파일은 `docs/reviews/codex_mixer_highbo_rereview2_evidence_20260927/` (README 에 출처 대조 · **HEAD `04fe95ae8` 에서 probe 전 항목 재현 — 수치 505 개 전부 동일**).
> 대응 = 원장 `findings.json` HBR3-01 ~ HBR3-08 (신설) · HBR2-01 · 04 · 05 · 08 → 재개방 (부분) · HBR2-02 · 03 · 06 · 07 → verified (한정어 포함) · `docs/reviews/mixer_highbo_prereg_20260927.md` §10.

---

# 믹서 고-Bo LH 3차 리뷰 — 수정은 실재하나, 새 벽 증거 경로는 아직 fail-closed가 아니다

- 검토일: 2026-09-27.
- 브랜치: claude/stoic-knuth-NObVQ.
- 고정 코드: **20568797bea1b9895bfa92c293200941d0442178**.
- 요청: 첨부 「Codex 3차 리뷰 요청 — 믹서 고-Bo 확장 LH」의 HBR2-01~08 및 §3 Q1~Q5.
- 범위: 수정 코드·사전등록·영수증 계측 경로. **LIGGGHTS, 영수증 run.sh, 생산 후처리, LH 생성·발사 모두 실행하지 않았다.** 단위시험과 합성 fixture에서 실제 Python 함수를 호출했다. 생산 코드와 Git 상태는 바꾸지 않았다.
- 아래 파일:행은 위 고정 스냅샷이다. 재현 자료는 별첨 묶음에 있다.

## 0. 결론부터

**현재 스냅샷에는 조건부 GO도 주지 않는다.** 사용자가 정한 GO의 뜻인 “L 완주 + 영수증 통과 + 실행 덱 대조 뒤 발사 가능”을 적용해도, **그 영수증과 대조기의 PASS 자체가 충분한 증거가 아니다.**

다만 “이전 반례를 고치지 않았다”는 판정은 아니다. 실제 39각형 STL로 옛 반례를 다시 호출했으며:

| 옛 반례 | 이번 코드의 출력 | 판단 |
|---|---|---|
| 실제 벽 2%, 반 면각 어긋남 → PASS | **TECH / unidentified** | 기존 false-green 닫힘 |
| 실제 예정각, 벽 0.5% → TECH | **PASS / bounded** | 기존 false-TECH 닫힘 |
| 정상 bin 0인데 8바퀴 미완주로 스모크 실패 | smoke.tech_smoke=[], 최종 미완주는 별도 | 닫힘 |
| 직전 bin 2/25 프레임인데 flat=true | 최종값 유지, **flat=None + tech** | 기존 반례 닫힘 |
| 새 CED 비대칭·NaN·음수·명령 머리 변경 | 전부 **FAIL** | 기존 행렬 반례 닫힘 |
| id별 type 교환·radius 절반 | **REJECT** | 기존 반례 닫힘 |

이번에 남은 핵심은 **새 증거 생성기·소비자 사이의 누락 및 경계값**이다.

1. A 대조 덤프가 **0개**여도 passed=true; 심지어 재개 전 **step 0 하나**만으로도 재개 시험 통과.
2. 영수증의 바이너리 SHA가 null이어도 받는다. 다른 dt·덱을 시험한 영수증도 주기·축만 같으면 받는다.
3. ±0.05° 구간 내부에서 참 겹침 **1.000800000%**, 검사값 **0.999162714% → PASS**.
4. 끝판이 빠진 mesh 덤프도 독립 기하로 인정한다. 끝판 겹침 **2% → PASS**.
5. 기준 E0의 지정 t₀ 덤프가 없으면 이전 정착 프레임을 대신 먹고, M과 유효성 표지가 조용히 달라진다.

**실제 캠페인에서 이 결함들이 발생했다고 주장하지 않는다.** 현재 도구가 그 경우를 거부하지 못한다는 재현이다. B 공동 개입, Bo 38.4의 내부 탐색값 지위, 현재의 결과 공개·조건부 A 한정은 다시 뒤집지 않는다.

## 1. HBR2 항목별 종결 판정

“닫힘”은 지정 결함 또는 정의 정정의 닫힘이지, 아직 보지 않은 실제 런의 합격을 뜻하지 않는다.

| 항목 | 판정 | 이유·남은 조건 |
|---|---|---|
| **HBR2-01 벽 위상** | **부분** | fitting을 증거에서 뺀 것은 옳고, 옛 양방향 반례도 닫혔다. 하지만 새 receipt 및 mesh-dump 경로가 HBR3-01~04로 다시 거짓 통과한다. |
| **HBR2-02 스모크/최종 창** | **닫힘** | 정상 26프레임 bin 0 스모크는 통과하면서 final bin 7 미완주는 최종 tech에만 남는다. bin 0 결손 시험도 발화한다. 단 **첫 시드만 발사하는 운영 명령**은 HBR3-08로 별도 보완해야 한다. |
| **HBR2-03 시간 표본** | **닫힘 — 관측량 한정** | D-1을 저장 snapshot 최대로 명시했고, 창 내부 계획 덤프 결손은 TECH. 옛 중간 프레임 결손은 이제 거부한다. **전 적분 최대 및 동적 접촉 건전성은 여전히 NOT OBSERVED**다. 이를 전체 시간의 1% 준수로 인용할 수 없다. |
| **HBR2-04 bin 완전성** | **부분** | 직전 bin 결손으로 flat을 내던 구멍은 닫혔다. 그러나 기준 t₀의 존재를 먼저 고정하지 않으며, 판독기는 격자 밖 추가 프레임을 평균에 넣는다(HBR3-05). |
| **HBR2-05 실행 덱 비교** | **부분** | 기존 CED 변이 4종 및 방향·목표 행렬 검사는 실재한다. 다만 **디렉터리 3개 = 실제 서로 다른 seed 3개**는 아니다(HBR3-07). 정본 명령 §2-2에는 --expect-deck도 아직 빠져 있다. |
| **HBR2-06 부피 누락 QC** | **닫힘 — 규약 한정** | 평균 0.90과 type별 프레임 최솟값 0.80을 구분하고, 대표성 보증이라는 주장을 철회했다. 2/25 프레임 0 유지율은 평균 0.92여도 QC 미달. 0.80은 **새로 등록한 공학적 허용선**이지 데이터가 검증한 대표성 문턱은 아니다. t₀·E0·bin 6·7을 실제 표로 내는 단계는 미실행이다. |
| **HBR2-07 해석 라벨** | **닫힘** | “무분리 범주”, “LC 기준 경로상 contrast 비”, “A 미발동=미검사”, “A는 평탄 참에서만”은 의도에 맞다. 결과-맹검 확증으로 격상하지 않는 한 수용한다. |
| **HBR2-08 id별 속성** | **부분** | 기존 type 교환/radius 변경은 잡는다. 그러나 후속 프레임의 id 열 부재·헤더 부재·소수 type을 허용한다(HBR3-06). |
| **HB-01 잔여 라벨** | **부분** | 생성기 현재형 앵커 설명 철회와 골든 해시 유지 확인. [docs/mixer_devlog/v09_20260927.md:11](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/docs/mixer_devlog/v09_20260927.md#L11) 의 “CED 고정” 열에 0.212를 적은 것은 아직 단위·양의 혼동이다(:15~17). PNG는 이번에 시각 검사하지 않았고, 요청서도 미수정이라고 밝힌다. |
| **K7 규칙 원장** | **부분** | §12에 원/현 규칙과 열람 상태를 남긴 방향은 맞다. 실제 규칙의 우선순위 충돌과 커밋 자리표시자가 남는다. §3 Q5의 정정 목록을 닫으면 된다. |

이전 K1~K7에 대한 변화: **K1 관측량 분리 수용, K2 현재 구현 반대, K3 QC 지위 수용, K4 경로별 효과·발동 한정 수용, K5 첫 시드 스모크 설계 수용/운영 배선 미완, K6 M_all 고정 진단 수용, K7 원장 형태 수용/정본 정리 미완**이다.

## 2. 새 반례

### HBR3-01 · P1 — 재개 영수증이 필수 대조와 재개 후 표본 없이 통과한다

**위치:** [scripts/mixer_restart_phase_test.py:149](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/mixer_restart_phase_test.py#L149) · [scripts/mixer_restart_phase_test.py:160](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/mixer_restart_phase_test.py#L160) · [scripts/mixer_restart_phase_test.py:167](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/mixer_restart_phase_test.py#L167).

A 파일이 없으면 dab=NaN이다. ab는 0으로 시작하며 유한 dab만 반영하므로, A가 하나도 없으면 “A↔B 최대 차=0”이 된다. B에 실제로 있는 파일만 열거하며 기대 step 집합, step>N1, N2 완료를 요구하지 않는다.

**검산 — 실제 analyze() 호출, 시뮬레이션 아님:**

| 합성 증거 | 출력 |
|---|---|
| B=[25000,30000], A 대조파일 0개 | passed=true, 행별 A↔B 차는 NaN, 요약 차는 **0 m** |
| B=[25000] 한 장, A 0개 | passed=true |
| A/B 모두 **mesh_0.stl 한 장** | passed=true, 각 오차 **0°**, “reset gap” **6.352978256°** |

마지막 경우는 재개 전 정적 형상밖에 없는데 재개 연속성 증서가 발행된다. reset gap은 실제 재개를 관측한 값이 아니라 두 예정식의 차이여서 이 구멍을 막지 못한다. 덤프 디렉터리를 정리/세대 분리하지 않는 RUN_SH(:88)와 결합하면 이전 시험 파일 혼입도 구별하지 못한다.

**무너지는 결론:** “영수증 passed라 이 바이너리의 read_restart 연속성을 실측했다.”

**해제 증거:** N1/N2/EVERY에서 도출한 기대 후속 step 집합을 양쪽에 요구하고, 누락·추가·비유한·형상 차원/개수 불일치는 실패시킬 것. A와 B 각 실행의 시작·완료·exit code·덤프 해시를 묶고, 이전 실행 파일과 섞이지 않게 할 것. 위 세 변이가 각각 실패해야 한다. 실제 바이너리 시험은 이 수정을 한 뒤 수행한다.

재현 키: receipt_missing_all_A · receipt_one_B_missing_all_A · receipt_only_step0.

### HBR3-02 · P1 — “시험한 바이너리”와 “판정할 런” 사이의 연결이 없다

**위치:** [scripts/mixer_restart_phase_test.py:178](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/mixer_restart_phase_test.py#L178) · [scripts/mixer_restart_phase_test.py:182](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/mixer_restart_phase_test.py#L182) · [scripts/check_contact_validity.py:322](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/check_contact_validity.py#L322).

생산자는 --binary 없이도 PASS를 발행한다. 바이너리 해시는 실행 시 봉인한 값이 아니라 **분석 시 사용자가 지목한 파일**의 해시다. 소비자는 해시 키의 존재만 확인하며, 런의 실행 기록과 비교하는 인자·경로가 없다.

load_phase_receipt()가 실제로 받아들인 변이:

- binary_sha256=null 또는 "not-a-sha".
- dt=2×현재 dt, 다른 deck_source_sha256.
- axis=[0,0,0]: 정규화 후 NaN, 비교가 false가 되어 통과.
- period=NaN.
- passed="false": 비어 있지 않은 문자열이라 참으로 취급.

정상 합성 A/B만 주고 로그와 바이너리를 전혀 주지 않은 경우도 passed=true, binary_sha256=null, 버전 빈 문자열이었다.

**무너지는 결론:** “주기·축이 맞는 영수증이면 L/LC/LH의 예정각을 검증된 실제 벽 각으로 써도 된다.”

**해제 증거:**

1. 불리언·양의 유한 period/dt·유한 단위축·비음수 유한 오차·정상 SHA 형식을 엄격히 검사.
2. 실행 직전 봉인한 binary/mesh/A·B 덱, 실행 결과와 receipt를 연결.
3. 캠페인 실행/재개 기록과 비교할 **명시적 호환 계약**을 둘 것: 바이너리, 정적 mesh/scale, 회전 중심·축·주기·dt, mesh/move fix ID·스타일·순서, 원래 회전 시작 step, 실제 checkpoint와 이어진 구간.
4. LC와 LH는 CED가 다르므로 **원 덱 전체 SHA가 같아야 한다는 처방은 틀리다.** CED·입자 명령은 전이 허용 차이, 메시 운동과 재개 상태는 불변량으로 구분해 비교한다.
5. 시험에서 잰 최대 오차는 그 짧은 표본의 오차이지, 수백만 step 캠페인의 오차 상한이 아니다. 전이할 ε의 근거도 따로 필요하다.

재현 키: receipt_nominal_no_binary_no_logs · receipt_load_mutants.

### HBR3-03 · P1 — ±ε 양 끝과 중앙은 구간 최댓값이 아니다; 0.05° 영향도 과소 서술됐다

**위치:** [scripts/check_contact_validity.py:517](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/check_contact_validity.py#L517) — θ, θ−ε, θ+ε 세 점만 잰다.

실제 저장소의 **39면 Drum STL**, 캠페인 SE 반경 **75.7 µm**, ε=**0.05°**를 썼다. 면 중앙을 향하는 최악 위상을 구간 내부 **θ+0.025°**에 두었다.

- 실제 구간 내부 최대 δ/r = **0.010008000000066 = 1.000800000007%**.
- 현재 세 점 검사 최대 = **0.009991627136177 = 0.999162713618%**.
- 출력 **PASS / receipt**, tech=[], reject=[].

이는 1% 문턱 근처의 **좁지만 실제인 산술 반례**다. 큰 겹침을 광범위하게 숨긴다고 과장하지 않는다.

**Q3의 “0.05°이면 ≤0.02%p”도 일반적으로 틀리다.** 같은 실제 면에서 중심점이 아니라 면 반폭의 0.8 지점에 SE 입자를 놓으면:

| 각도 | δ/r (%) |
|---|---:|
| 예정각 | 0.500000000003 |
| −0.05° | −0.481485142837 |
| +0.05° | 1.468387223147 |

증가 **0.968387223144%p**다. 면 중앙에서 얻은 작은 값은 접선 방향 위치가 다른 입자에 대한 상한이 아니다.

**해제 증거:** 각 평면의 거리식을 a cos θ + b sin θ + c 형태로 두고 구간 양 끝과 **구간 내부 정지점**을 모두 평가하거나, 증명된 보수적 거리 경계를 사용한다. 더 조밀한 샘플링만으로 엄밀한 상한이라고 부르지 않는다. ε는 출력 반올림·측정 오차·장시간 전이 오차를 포함해야 하며, 실제 시험의 관측 최대값을 0으로 얻었다고 전 캠페인 ε=0으로 두지 않는다.

불확실 구간에 1% 양쪽 값이 함께 있으면 “실제 1% 초과 실측”이 아니라 **위상 불확실성으로 미식별**이다. 보수적 실행 금지는 가능하지만, REJECT를 실제 접촉 위반과 같은 문장으로 쓰지는 말 것.

재현 키: angle_interior_false_pass · angle_tolerance_side.

### HBR3-04 · P1 — mesh 파일의 존재·볼록성은 전체 용기 존재를 보증하지 않는다

**위치:** [scripts/check_contact_validity.py:348](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/check_contact_validity.py#L348) · [scripts/check_contact_validity.py:435](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/check_contact_validity.py#L435) · [scripts/check_contact_validity.py:523](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/check_contact_validity.py#L523).

모든 입자 프레임에 대응하는 mesh 파일이 있으면 독립 기하로 우선한다. 그러나 그 파일에 **Drum만 있고 Front/Back이 없어도** 볼록성 검사에 통과한다. 끝판이 없으면 cap_rel=−∞로 두고 계속 판정한다.

실제 STL에서 Front 면에 δ/r=**0.02 (2%)** 들어간 입자를 만들었다. 각 step의 mesh 파일에는 **정상 회전한 Drum 삼각형만** 넣었다.

- phase_status=mesh-dump.
- verdict=PASS, tech=[], reject=[].
- 보고 wall_max는 드럼과의 거리뿐인 **−171.986607...**(무차원)이다. 진짜 끝판 겹침을 검사하지 않았다.

공식 dump mesh/stl은 기본 전체 메시뿐 아니라 **mesh ID 선택 출력**도 지원한다. 이 반례는 문법상 불가능한 파일이 아니다. 반대로 현재 영수증 생성기의 기본 dump 명령이 일부 메시만 내보낸다고 주장하는 것도 아니다. [공식 dump 설명](https://www.cfdem.com/media/DEM/docu/dump.html)

**해제 증거:** 기대 세 구성요소, 닫힌 용기, 끝판 양쪽, 삼각형/면의 완전성, 원 기하와 강체 변환 정합 및 시간·런 출처를 확인할 것. ID가 없는 STL이면 구성요소별 파일 또는 원 기하와 전체 비교가 필요하다. Drum-only·끝판 하나 삭제·잘못된 시각/런의 파일은 실패해야 한다.

재현 키: mesh_missing_caps (true_complete_wall_overlap과 판정 동시 보존).

### HBR3-05 · P1 — 기준 t₀를 “있는 것 중 마지막”으로 정해, 없어진 기준 프레임을 조용히 대체한다

**위치:** [scripts/measure_mixing_index.py:149](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/measure_mixing_index.py#L149) · [scripts/measure_mixing_index.py:164](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/measure_mixing_index.py#L164) · [scripts/measure_mixing_index.py:170](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/measure_mixing_index.py#L170) · [scripts/measure_mixing_index.py:224](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/measure_mixing_index.py#L224).

계획 격자는 관측에서 고른 st0를 출발점으로 만든다. **계획상 t₀ 프레임이 실재하는지**가 먼저 서지 않는다. 특히 E0 기준 프레임은 자기 헤더·기대 종료/정착 step을 이 함수에서 확인하지 않는다.

합성 판독 예 (4셀, 각각 24입자; 실제 analyse() 호출):

| 기준 입력 | S₀² | S_R² | S₀²/S_R² | 등록 M_final |
|---|---:|---:|---:|---:|
| 지정 E0 step 200 존재 | 0.25 | 0.006944444444 | 36 | **0.450000000000** |
| step 200 없음; step 160 정착 프레임만 존재 | 0.25 | 0.043402777778 | 5.76 | **0.529411764706** |

둘 다 planned.complete=true, flat=true, tech=[], smoke.tech_smoke=[]다. 같은 평가 궤적에서 기준 덤프 대체만으로 **M이 0.079411764706 이동**한다. 단순 S₀²/S_R²≥5 조건도 이 예를 거부하지 못한다. 이것이 실제 16×16×4/8×8×2 캠페인 전체 게이트를 통과했다는 주장은 아니다.

평가 런 자체의 t₀를 지워도 이전 프레임을 t₀로 고른다. 이때 현재 스모크는 bin 0 결손을 잡지만, 최종 tech는 비어 있을 수 있다. **평가 런 누락은 별도 접촉 계약이 잡을 수 있다는 한정을 보존한다.** 가장 직접적인 사각지대는 E0 기준 t₀의 정확한 선택이다.

**부수 P2 — 격자 밖 추가 표본도 평균에 섞인다.** 계획 25개를 모두 두고 step 7301 한 장을 추가하면 expected=25, n=26, complete=true, tech=[]. 평균이 0.45 → **0.432692307692**로 바뀐다. dump_gaps는 기록하지만 거부하지 않는다. 접촉 검사기에는 격자 밖 검사가 있으므로 이를 전체 캠페인의 자동 우회라고 부르지는 않는다.

**해제 증거:** 계획 덱·실제 dump 스케줄에서 기대 t₀를 먼저 확정하고, 평가/E0 양쪽에 그 프레임의 존재·헤더·입자 수·출처를 요구할 것. t₀ 누락 시 이전 프레임 대체 금지. bin의 집합 비교는 누락뿐 아니라 **추가**도 다루고, 허용 밖 표본이 평균·SD·flat에 들어가지 않게 할 것. 기존 정상 창과 값은 유지한다.

재현 키: reference_endpoint_missing · reader_nominal · reader_missing_t0 · reader_offgrid_extra.

### HBR3-06 · P2 — 모든 프레임의 필수 스키마를 검사하지 않는다

**위치:** [scripts/check_contact_validity.py:457](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/check_contact_validity.py#L457) · [scripts/check_contact_validity.py:458](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/check_contact_validity.py#L458) · [scripts/check_contact_validity.py:464](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/check_contact_validity.py#L464) · [scripts/check_contact_validity.py:480](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/check_contact_validity.py#L480) · [scripts/measure_mixing_index.py:55](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/measure_mixing_index.py#L55).

실제 check_window() 결과:

- t₀에는 id가 있고 그 뒤 프레임에는 **id 열 없음** → PASS.
- TIMESTEP/NUMBER OF ATOMS 헤더를 모두 빼고 ATOMS 본문만 유지 → PASS.
- type을 **1.5·3.5**로 넣고 expect_counts={1:1,3:1} 요구 → 정수 절삭 후 PASS.

“type 교환+반경 변경” 수정은 실제로 작동한다. 다만 필수 입력 부재가 “변화 없음”으로 바뀌는 별도 경로가 남는다. 현재 덱이 정상 출력하면 이런 형태가 생긴다는 주장은 아니다.

**해제 증거:** 매 프레임에 필수 헤더·열 존재, id/type의 유한 정수성, id 유일성, 좌표 유한성, 양의 유한 반경을 검사한 뒤 캐스팅·접촉 계산할 것. malformed 입력은 분명한 TECH/오류 종료. t₀만 id를 요구하는 형태는 불충분하다.

재현 키: missing_id_after_t0 · missing_headers · fractional_type.

### HBR3-07 · P2 — 예정 디렉터리 3개를 서로 다른 실제 seed 3개로 인증한다

**위치:** [scripts/mixer_deck_diff.py:141](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/mixer_deck_diff.py#L141) · [scripts/mixer_deck_diff.py:279](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/scripts/mixer_deck_diff.py#L279).

세 예정 디렉터리 32452843/49979687/67867967에 **내용은 모두 seed=32452843인 LC/LH 한 쌍을 복사**했다. 실제 CLI에 --expect-deck까지 주었다.

결과: **3/3 PASS, exit 0**. 각 쌍 안에서는 seed가 같으므로 비-CED 비교가 통과하고, 디렉터리 이름으로만 세는 코호트도 통과한다.

**한정:** 기존 LC 세 덱이 실제로 서로 다른 올바른 seed로 봉인되어 있다면 잘못된 LH 하나는 쌍 비교에서 잡힐 수 있다. 여기서 깨진 것은 비교기가 스스로 “서로 다른 실제 세 시드”까지 보증한다는 해석이다.

**해제 증거:** 실제 삽입/분포 seed 명령을 해당 설계 seed에서 도출되는 기대값과 맞추고, LC/LH 각각의 실제 seed 서명을 기록·고유성 검사할 것. 예정 밖 디렉터리도 별도로 거부/보고하여 4/3 PASS를 정상 코호트로 쓰지 못하게 할 것.

재현 키: duplicated_physical_seed_three_dirs.cli.

### HBR3-08 · P2 — “첫 시드 스모크 후 나머지” 결정과 남아 있는 발사 명령이 다르다

**위치:** [docs/reviews/mixer_highbo_prereg_20260927.md:98](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/docs/reviews/mixer_highbo_prereg_20260927.md#L98) vs :171 · [dem_scripts/mixer_20260921/run_all.sh:48](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/dem_scripts/mixer_20260921/run_all.sh#L48) · [dem_scripts/mixer_20260921/run_all.sh:62](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/20568797bea1b9895bfa92c293200941d0442178/dem_scripts/mixer_20260921/run_all.sh#L62).

§8은 첫 시드만 먼저라고 정정했지만, §2-5에는 여전히 같은 runs 디렉터리에서 MAXJ=3 ... run_all.sh를 쓰라고 한다. 런처는 미실행 _s* 전체를 순회하며 **smoke 결과를 읽지 않는다**. 따라서 LH 덱 세 개가 준비된 상태의 그 명령은 처음부터 셋을 시작한다.

**MAXJ=1로 바꾸는 것만으로도 해결되지 않는다.** 첫 런 종료 후 다음 런을 자동 발사할 뿐, bin 0 스모크의 기술 판정을 기다리는 기능이 아니다.

이 항목은 소스·정본 명령의 충돌 판정이다. 이번 환경에서 Linux 런처 동작 시험은 실행하지 않았다.

**해제 증거:** 첫 호출은 정확히 LH_s32452843 하나만 선택하고 종료, 스모크 증서를 확인한 별도 호출만 나머지 둘을 선택하도록 명령/선택 인자를 명확히 할 것. 전역 live 상한은 유지. 가짜 실행파일 시험으로 **스모크 실패이면 나머지 둘의 발사 0건**을 강제할 것. 이 리뷰는 런처 변경이나 실제 발사를 수행하지 않는다.

## 3. §3 Q1~Q5 답

### Q1 — 현재 영수증 + 예정각을 L·LC·LH의 벽 근거로 수용하는가?

**반대 — 현재 구현은 안 된다. 수정한 방식 자체는 조건부 수용 가능하다.**

입자가 0개라는 것 자체가 핵심 결함은 아니다. 여기서 시험하는 move/mesh rotate는 주어진 축·주기의 운동이고, 공식 설명도 prescribed motion 및 restart 연속성을 다룬다. 입자 없이 그 운동의 연속성을 시험하는 것은 유효한 단위시험이다. **그것이 실제 checkpoint가 올바른 상태라는 증거까지 되는 것은 아니다.** [공식 move/mesh 설명](https://www.cfdem.com/media/DEM/docu/fix_move_mesh.html)

구분할 두 증거:

1. **실행 구현 증거:** 이 봉인된 binary와 메시/fix 계약으로 restart 전후 운동이 연속인가.
2. **개별 런 상태 증거:** 이 L/LC checkpoint와 실제 재개 덱이 바로 그 계약·원래 시작 위상·step을 이어받았는가.

현재 도구는 1도 HBR3-01/02로 미완이며 2는 담지 않는다. 수정 영수증을 한 번 만들었다는 이유만으로 모든 과거 LC를 인증하면 안 된다.

**실행 가능한 권고:**

- 기존 L/LC: 보존된 **실제 사용 checkpoint의 복사본**과 실제 재개 덱을 별도 검사 디렉터리에서 읽어, 첫 상태 및 소수 후속 step의 **전체 mesh**를 내는 검사를 권고한다. checkpoint SHA, 실제 step, 원 회전 시작, binary/mesh/fix 서명과 함께 예정 기하에 대조한다. make_mixer_resume.py --smoke-steps를 쓰더라도 생산 디렉터리의 출력/로그를 덮지 않도록 별도 환경에서 수행해야 한다.
- 그 한 장/짧은 검사는 **그 이전 모든 프레임을 직접 관측한 것**이 아니다. 단일 고정 회전 규약·동일 binary·연속한 구간과 재개 이력이 입증될 때만 해당 구간으로 전이한다. 원래 실행 binary/이력이 없으면 끝까지 조건부·미식별임을 남긴다.
- 앞으로의 LH: 같은 계약과 fresh 초기 기하를 발사 시 봉인하고, 충분한 시간 범위에서 검증한 오차 한계를 적용하면 별도 생산 checkpoint가 생기기 전부터 경로를 세울 수 있다. 생산 mesh 저장을 선택한다면 저장량/동등성 규칙도 사전에 명시한다.
- E0는 회전 0이므로 정적 기하/실행 상태를 따로 확인할 수 있다. 회전하는 LC의 재개 증서를 기계적으로 강요하는 것이 물리적 필수는 아니다.

**9개 런 재실행을 요구하는 판정은 아니다.** 상태 확인용 짧은 별도 시험 또는 동등한 봉인 증거를 요구한다. 이 리뷰에서는 그 시험도 실행하지 않았다.

### Q2 — 표지 꼭짓점과 A↔B 일치가 주 근거로 충분한가?

**수정안.**

- 같은 표지의 대응이 보장되면 각도 계산은 유효하다. 그러나 “파일의 첫 삼각형”은 영구 식별자가 아니다. 현재 _drum_angle()의 ref_vertex 인자도 실제 대응에 사용되지 않는다(:117).
- A↔B **전체 좌표** 일치는 재개 전후 연속성의 좋은 검사지만, 필수 파일·유한성·전체 형상을 강제한 뒤에만 그렇다(HBR3-01).
- A와 B가 공통으로 잘못된 형상/축/초기 상태를 쓰는 경우는 A↔B 비교 하나로 배제하지 못한다. **봉인된 원 전체 mesh의 예정 강체 변환**과도 대조해야 한다.
- 순서가 바뀐 파일은 기하학적 대응을 정규화해 비교하거나 명시적으로 TECH로 두면 된다. “반드시 거짓 실패만 만든다”는 일반 보증은 주지 않는다.
- 현재 캠페인 덱에서 N1=20000의 회전은 **6.352978256°**다. 정규 39각형의 모양은 9.230769231°마다 같으므로 무표지 형상 기준 최소 위상 간격은 약 **2.877790975°**다. 지금 선택은 여전히 1°보다 크지만, 앞으로 N1/period를 바꿀 때에는 **도형 대칭을 고려한 실제 형상 구분도**로 검사를 등록해야 한다.

### Q3 — 0.05° 허용과 reset gap≥1°가 적절한가?

**수정안; “벽 영향 ≤0.02%p” 근거는 반대.**

- 현재 캠페인 설정에서 연속/리셋 대안을 구별하는 1° 기준은 후보로 쓸 수 있다. 다만 면각의 10%라는 비율 자체가 측정오차 근거는 아니다. 수치/출력 오차에 비해 충분히 떨어졌음을 실제 mesh 차이로 보여야 한다.
- 0.05°는 재개 시험의 각도 허용선으로 등록할 수 있지만, **벽 겹침의 허용오차가 작다는 보증은 아니다**. HBR3-03의 면 가장자리 반례가 0.9684%p 이동을 보였다.
- consumer가 받는 오차 상한은 현재 **0.5°**(:343)로 producer의 **0.05°**와 다르다. 계약을 한 곳에서 정의할 것.
- ε가 실제 런에 대한 유효한 상한이라는 증거 → 구간 전체 거리 경계 → PASS/미식별/명백 위반 순서로 판정해야 한다. 합격하도록 ε를 작게 잡는 것은 해결이 아니다.

### Q4 — 회전각 무관 bounded 판정은 fail-closed로 충분한가?

**동의 — 검증된 현재 용기·입력과 해당 벽 판정 범위에 한해.**

현재의 중심 정렬된 볼록 39각 드럼 및 알려진 두 끝판에서, 회전각 무관 안전 상한이 1% 이하이면 위상을 몰라도 PASS를 줄 수 있다. 확실한 위반 하한이 1%보다 크면 REJECT, 그 사이 TECH라는 구조는 맞다. 실제 옛 반례의 0.5%는 bounded PASS, 반 면각 어긋난 2%는 TECH가 됐다.

다만 이것은 **bounded 분기의 논리**에 대한 답이다. mesh 불완전성, 누락 id/헤더, 다른 용기 형상, 관측되지 않은 시간 peak까지 보증하지 않는다. 예정각 wall_max는 bounded 상황에서 미검증 계산값과 인증된 상·하한을 구분해 표시해야 한다.

### Q5 — HB-01과 발사 기록 봉인을 발사 직전에 해도 되는가?

**수정안.**

- 실제 STL 내용·binary·실행 덱·선택 seed·환경·시각 봉인을 **실행 직전** 하는 것은 맞다. 단 영수증 시험도 자기 실행 **직전** 같은 봉인을 하고, 생산/기존 LC와 대조해야 한다. 분석 시 새 binary 해시를 붙이는 것은 실행 증거가 아니다.
- v09 0.212와 PNG는 기존 공개 설명의 오류다. LH 발사까지 기다릴 이유가 없다. 먼저 정정하고 정정 이력을 남긴다. PNG는 별도 렌더/시각 확인 필요.
- 스냅샷의 정본 §2-5는 실제 STL 해시를 아직 열거하지 않는다(:99). 요청서에 적었다는 것과 실행 정본에 강제됐다는 것은 다르다.
- §2-2 명령에 --expect-deck와 실제 seed 검증을 반영하고, §2-5/§8의 발사 선택을 일치시킬 것.
- §2-3 :76은 직전 bin 결손까지 “최종값 없음”이라고 하고, §5 :150과 새 reader는 “값 보고, flat 불가”를 허용한다. **값의 기술 보고 가능성 / 판정 적격성 / A 발동 가능성**을 분리해 정본을 하나로 만들 것.
- §12의 “같은 커밋 / SHA는 §10에 기입”을 실제 수정 커밋 20568797b와 원장 등재 커밋으로 보완한다. 독자가 6963632a0을 수정 완료 커밋으로 오독하지 않게 한다.
- 검사기 머리말(:24~25), deck_walls 설명(:168), infer_drum_phase 설명(:281~282)에는 되읽기로 예정각이 확인된다는 옛 설명이 남아 있다. 실제 판정에서 분리한 수정은 인정하되, 이 문구도 진단 전용으로 정정한다.

## 4. 최소 해제 목록 — 새 연구 설계를 요구하지 않는다

1. **영수증 생산자:** 기대 A/B 후속 표본·완료·유한성·전체 형상·실행 provenance를 강제. 누락 A 및 step 0만인 시험은 실패.
2. **영수증 전이:** 타입/값 검증, 실행 시 binary/mesh/운동 계약 봉인, 실제 L/LC 재개 상태와 연결. 짧은 빈 계 시험의 최대 오차를 장시간 전체 상한이라고 쓰지 않음.
3. **벽 계산:** ±ε 구간의 엄밀한 최대/최소 또는 안전 경계, 전체 용기 메시 완전성. 내부 극값·끝판 누락 반례 실패.
4. **판독 입력:** 평가/E0 지정 t₀ 강제, 전 프레임 필수 스키마, bin 표본 집합 검증. 기준 프레임의 조용한 대체를 없앰.
5. **실행 증서:** 실제 세 seed, 목표 CED, STL/binary 봉인, 첫 시드만 발사하는 정확한 절차와 가짜 런처 회귀. 뒤 둘은 스모크 실패 시 발사 0건.
6. **정본:** 기존 라벨/PNG·보고/적격성 문구·규칙 원장 정리.

그 뒤 요청서의 순서인 **영수증/실제 상태 확인 → L 완주 → 생산 덱 3쌍 대조 → 봉인 → 첫 시드 → bin 0 기술 스모크 → 나머지 둘**을 조건부로 승인할 수 있다. 문턱을 바꾸거나 LC를 폐기하거나 새 Bo/seed를 추가할 필요는 이 리뷰에서 도출되지 않았다.

## 5. 재현 및 한계

재현 묶음 디렉터리에서 NumPy/SciPy가 있는 Python 3로:

~~~bash
PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 python3 run_selftests.py
PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1 python3 review_round3_probe.py
~~~

두 명령 모두 LIGGGHTS나 런처를 실행하지 않는다. 임시 합성 덤프를 만들고 고정 소스의 실제 함수를 호출한다.

| 실행 | 독립 결과 |
|---|---|
| check_contact_validity selftest | 32/32, exit 0 |
| measure_mixing_index selftest | 23/23, exit 0; 선택적 실제 덱 ⑪은 SKIP |
| mixer_deck_diff selftest | 14/14, exit 0 |
| mixer_restart_phase_test selftest | 7/7, exit 0; 합성 기하 시험 |
| make_mixer_deck selftest | 89/89, exit 0 |
| 독립 round3 probe | exit 0; 새 반례 및 옛 반례 변경 결과 JSON 보존 |
| test_launcher.sh | Bash **구문 검사만** exit 0; Linux 실행 31/31은 독립 재현하지 않음 |
| check_all.sh | 전체 리포/실행 환경이 아닌 읽기 전용 사본이므로 실행하지 않음 |
| 실제 binary·checkpoint·캠페인 덤프 | 미입수/미실행; 실데이터 합격 판정 없음 |

Windows 기본 cp949로 임시 시험 파일을 쓰는 두 selftest는 처음 환경 오류가 났다. **소스를 고치지 않고 PYTHONUTF8=1**로 다시 실행해 통과했다. 이를 캠페인 결함으로 등재하지 않는다.

옛 probe의 assert 실패 자체를 수정 증거로 세지 않았다. 이전 fixture와 함수 호출을 다시 실행해 **모든 출력**을 수집하고, 바뀌어야 하는 각 상태를 별도로 대조했다. 파일·blob SHA는 sources.json, 실행 원문은 selftests_output.json, 수치 정본은 review_round3_output.json이다.

생산 결과·생산 파일은 수정하지 않았다. 증거 패키지와 이 리뷰문만 새로 작성했다.

재현 사본의 소스 17개는 원격 Git blob SHA와 바이트 단위 일치를 확인했다. 수집 과정에서 생긴 마지막 LF/CRLF 차이만 원본대로 복구한 뒤 시험을 다시 돌렸으며, 코드 로직·수치는 수정하지 않았다.

HOLD
