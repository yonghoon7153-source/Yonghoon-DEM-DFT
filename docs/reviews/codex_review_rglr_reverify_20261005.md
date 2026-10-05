# RGLR 3차 재검증 — 기존 세 건 닫힘, WSL 소형 통합만 조건부 GO

검토일: 2026-10-05. 대상 핀: `dbe0f076d7b948b8ebcfa85a02a391125b104fe2`.
비교 핀: `bf4fb6aee0b388375ddf65694ac405e63e0e381c`.
대상: RGLR-01–03, WEB-03 최소 수정, LHS-33 좁은 amendment, 194 인계의 LW 제외.

## 0. 결론과 승인 범위

**기존 HOLD 해제조건 RGLR-01·02·03은 닫는다. 새 P1은 찾지 못했다.**

다만 이번에 함께 심사한 게시·복원·VM 정정에는 P2 세 항목이 남는다. 따라서 **격리된 WSL 소형 통합시험 착수는 조건부 GO, 공식 재봉인·194건 생산/인계는 HOLD**다. 소형 시험은 결함을 확인하는 개발 시험이지 현재 코드를 생산 승인하는 행위가 아니다.

| 대상 | 판정 | 경계 |
|---|---|---|
| RGLR-01: fallback 앞 입력 검사 | 닫힘 | 정지 경로와 τ 인계 소비자에서 기존 네 반례 차단. 정상 fallback은 유지 |
| RGLR-02: 두 σ 표현 대조 | 닫힘 | 저장 정밀도 허용폭 수용. 일반 게시 경로는 아래 별도 잔여 |
| RGLR-03: c_strs 손상을 미제공으로 바꿈 | 닫힘 | 실제 CSV→파서→LW에서 NaN·문자열·부분 튜플 차단 |
| WEB-03: 관통 풀이 실패 게시 | 닫힘 | 요청된 채널의 실패를 일반/정지 경로 모두 거부 |
| WEB-03: 동기 예외 복원·한 실패 어휘 | 부분 | 정상적인 복원은 성공. **복원 자체가 실패하면 잘못된 보존 표지** |
| LHS-33: 무효/미정의→null, 소비자 연동 | 부분 | 결손·NaN·0/0 처리는 수용. **음수 근호→0→computed는 별도 문제** |
| LW를 194 인계에서 명시 제외 | 닫힘 | 제외 기능만 승인. LW의 프레임/상별 응력은 여전히 미인증 |

이번 P2의 성격도 구분한다. `RGLR2-01`은 요청서가 공개한 일반 경로의 검사 생략을 실제로 반증한 것, `RGLR2-02`는 추가로 찾은 **동기 복원 실패 경계**, `RGLR2-03`은 질문 Q4의 clamp를 수치로 반증한 것이다. 기존 세 건을 새 이름으로 다시 열거나, 이미 공개한 정전 비원자성을 새 발견으로 세지 않는다.

읽기 전용으로 검토했다. 생산 코드·원장·Git 상태를 바꾸지 않았고, WSL·실 Stage E·real14 원자료 분석·재봉인·194건 실행도 하지 않았다. 작성한 파일은 별도 검토 폴더의 보고서·소형 시험·증거다.

## 1. 기존 해제조건 재검증

### 1-1. RGLR-01 — 닫힘

[tau_flux.py:290](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/scripts/tau_flux.py#L290)의 `ion_record_problem` 호출이 BAND_FALLBACK 반환보다 앞이다. 정지 계약도 [pipeline_service.py:829](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/webapp/pipeline_service.py#L829)에서 같은 함수를 부른다.

실 network CLI가 만든 네 JSON을 서로 일관되게 변조했다. 파일끼리 다르기 때문에 거부된 것이 아니다.

| 입력 | 이전 | 현재 정지 경로 |
|---|---|---|
| 정상 L0 | done | done |
| 정상 비관통 | done | done |
| 정상 L1 fallback | done | done, 과학적 HOLD 유지 |
| L1 + σ_ratio=None | done | failed |
| L1 + σ_ratio=NaN | done | failed |
| L1 + σ_ratio=−1 | done | failed |
| L1 + 관통 분율=2 | done | failed |

기술 실패를 과학적 HOLD로 숨기던 이전 반례는 닫혔다. `test_tau_flux`의 L2/L2b/L3도 모드별 격리와 정상 L2·연속체 하한 유지에 통과했다. **비관통 자체를 계산 실패로 바꾸라는 요구가 아니다.**

재현: `python3 run_probes.py network` → `evidence/network_adversarial.json`.

### 1-2. RGLR-02 — 닫힘

생산자 [network_conductivity.py:1259](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/scripts/network_conductivity.py#L1259)의 두 값은 같은 반올림 전 해에서 나온다. 현재 공용 검사는 그 관계를 확인한다.

양성 기준:

- σ_ratio = `0.00400388` (무차원).
- σ_dim = `0.012012 mS/cm`, σ₀ = `0.003 S/cm`.
- 인계 τ² = `10.984918916215547`, 등급 getter τ² = `10.984589697866410`.
- 두 τ²의 작은 차이는 각 8자리/6자리 저장값을 쓰는 차이로 유지된다. 두 getter의 숫자를 강제로 같게 만들지 않았다.

σ_ratio만 네 파일에서 ×4로 바꾸면 현재 정지 경로는 failed다. 이전의 τ²÷4 false-green은 재현되지 않는다. 허용폭·작은 값의 한정은 §3 Q3에 별도로 판정한다.

재현: `python3 run_probes.py network precision`.

### 1-3. RGLR-03 — 닫힘

[analyze_contacts.py:64](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/scripts/analyze_contacts.py#L64)에서 원 c_strs 열의 존재와 손상을 보존하고, [dem_analysis_core.py:1342](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/scripts/dem_analysis_core.py#L1342)에서 any-present/all-complete를 구분한다.

| 실제 입력 경로 | 현재 결과 |
|---|---|
| 정상 CSV c_strs=(0,0,−0.9) | OK, 독립 virial 대조 실행 |
| c_strs 세 열 전무 | 기존 미제공 처리 유지; LW 계산 가능하나 c_strs 대조 증명은 없음 |
| 첫 c_strs=NaN | FAILED invalid_input, sigma 키가 사라지지 않음 |
| 첫 c_strs=문자열 | FAILED invalid_input |
| 첫 c_strs=Inf | FAILED invalid_input |
| 유한 c_strs의 virial −2.7 | FAILED virial mismatch |
| NaN으로 −2.7 불일치를 가림 | FAILED invalid_input |
| 직접 dict에서 모든 입자의 sigma_xx만 삭제 | FAILED invalid_input |

이것은 손상된 대조 입력을 감추는 우회가 닫혔다는 판정이다. **LW의 프레임·상 배분 인증이 끝났다는 뜻은 아니다.**

재현: `python3 run_probes.py lw` → `evidence/lw_replay.json`. 저장소 회귀의 실제 CSV→CLI 음성 대조도 통과했다.

## 2. 남은 P2 세 항목

### RGLR2-01 · P2 — 일반 게시 경로에는 같은 σ 기술 검사가 없다

**위치:** [app.py:3326](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/webapp/app.py#L3326), 특히 `if stop_before_stage_e`인 :3346. 공용 검사는 [tau_flux.py:112](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/scripts/tau_flux.py#L112).

**검산:** 실제 생산자 출력 네 파일을 같은 방식으로 변조하고 일반 helper를 호출했다. Stage E만 테스트 대역이다.

| 일반 경로 입력 | helper | 게시된 값 | 별도 소비자 |
|---|---|---|---|
| σ_ratio만 ×4 | done | ratio `0.01601552`, dim `0.012012 mS/cm` | τ 인계 NOT_COMPUTED, 등급 getter τ² `10.984589697866410` |
| L1의 σ_ratio=None | done | dim `0.002678 mS/cm`, ratio 없음 | τ 인계 NOT_COMPUTED, 등급 getter τ² `6.081410125544993` |

**무너지는 결론:** “일반/정지 어느 경로로 게시해도 같은 기술적 입력 계약을 만족한다.” 생산자가 같은 q*를 쓴다는 사실은 정상 생산 식의 성질이지 게시 경계의 독립 검증이 아니다. 이 반례는 현재 정상 솔버가 스스로 ×4를 만든다고 주장하지 않는다. 출력 변조/회귀 결함에 대한 게시 검사 생략을 시험한다.

**무너지지 않는 것:** 수정된 관통 `spsolve` 실패 차단, 정지 경로, τ 소비자의 fail-closed 동작은 유지된다. 실 Stage E 수치 결과를 시험했다고 해석하지 말 것. 일반 helper가 Stage E에 잘못된 후보를 넘기기 전에 막지 못한다는 검증이다.

**최소 수정/해결 증거:** 양쪽 모드의 `ion_record_problem`을 일반/정지 공통의 승격 전 검사로 호출한다. **전체 stop 계약의 과학적 HOLD 조건을 일반 경로로 복제하는 것이 아니다.** 위 두 반례는 게시 거부, 정상 L0/L1/L2·비관통·온도 변환은 유지하는 시험이 필요하다.

재현: `python3 run_probes.py network`의 `general_ratio_times4`, `general_band_ratio_missing`.

### RGLR2-02 · P2 — rollback 실패를 기록하면서도 “이전 세대 그대로”라고 표시한다

**위치:** [pipeline_service.py:1159](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/webapp/pipeline_service.py#L1159)의 예외/복원 처리, [동일 파일:1080](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/webapp/pipeline_service.py#L1080)의 `previous_generation_kept` 계산, [app.py:793](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/webapp/app.py#L793)의 표시.

**양성 대조:** 단순 full_metrics 쓰기 OSError에서는 현재 코드가 failed를 반환하고 이전 여섯 파일의 SHA-256을 모두 보존한다. 첫 실행이면 망 후보·도장이 남지 않는다. 이 수정은 옳다.

**새 반례의 조건:** 성공한 기존 세대를 만든 뒤, 접촉 면적·δ를 각각 절반으로 바꿔 **다른 정상 CLI 해**를 계산한다. 이번에는 마지막 success-attempt 쓰기에 OSError, 이어 full_metrics 복원에 PermissionError를 주입한다. 두 I/O 실패가 필요하며 단일 쓰기 실패의 보통 경로를 부정하는 반례가 아니다. kill-9/정전은 쓰지 않았다.

| 실패 후 관측 | 값 |
|---|---|
| 필수 단계 / helper | failed |
| 네 망 JSON 및 provenance | 이전 세대, Hertz σ_dim `0.012012 mS/cm` |
| full_metrics | 새 세대, Hertz σ_dim `0.008755 mS/cm` |
| full_metrics ID ↔ provenance ID | 서로 다름 |
| 등급 getter τ² | `15.071032718534700` — 새 full_metrics 숫자를 읽음 |
| attempt.previous_generation_kept | **true** |
| active_status | **success** |
| 실제 UI 행 생성 함수 | **“활성 세대 … 의 값 (이전 성공 세대 그대로)”** |

실패 사유에 `full_metrics 되돌림 실패` 경고도 함께 들어 있다. 그러므로 경고 누락이 아니라 **경고와 보존/활성 판정이 모순**인 결함이다. `_active_generation`은 provenance만 읽으므로 다른 파일의 복원 성공을 증명하지 못한다. 이 반례는 파이프라인이 done이라고 속였다는 주장이 아니다. 파이프라인은 failed지만 남아 있는 값의 유효성 설명이 틀리다.

**최소 수정/해결 증거:** 복원 실패를 명시적 `rollback_failed` 또는 동등한 격리 상태로 올린다. 이때 `previous_generation_kept`는 false/unknown, active는 invalid/unknown이고 숫자를 유효한 이전 값으로 인용하지 않아야 한다. 복원이 성공했다는 표지는 실제 복원 결과와 세대 일치 검산을 통과했을 때만 낸다. 상태 파일마저 쓸 수 없는 경우도 읽는 쪽에서 full_metrics/provenance 불일치를 보고 fail-closed해야 한다. 백업은 복구 자료로 보존한다.

세대별 디렉터리+단일 포인터는 좋은 해법이지만 **이 문제를 고치는 유일한 구현이라고 요구하지 않는다.** 현재 최소안도 “복원 실패 시 유효 세대 주장 금지”를 구현하면 진전할 수 있다. 어떤 구현이든 검증 없이 pointer만 바꾸면 내용 일치 증명은 생기지 않는다.

재현: `python3 run_probes.py network`의 `rollback_destination_failure`. 증거에는 각 파일 해시·두 run_id·input_digest·실제 UI 행을 모두 남겼다.

### RGLR2-03 · P2 — VM 음수 근호 clamp가 유효 입력의 CV를 만들어 낸다

**위치:** [dem_analysis_core.py:1214](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/scripts/dem_analysis_core.py#L1214)의 `vm_sq` 및 :1217의 0 clamp, 아래 CV 및 computed 반환. 등급은 [grade_engine.py:909](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/scripts/grade_engine.py#L909)에서 해당 수를 소비한다.

같은 정의의 수학적 항등식을 이용해 검산했다. 전단성분을 추가하는 새 응력 모델이 아니다.

`VM² = ½[(σxx−σyy)² + (σyy−σzz)² + (σxx−σzz)²]`.

두 입자의 대각 응력을 sim Pa로 다음처럼 준다:

1. `(1073.1, 1073.1, 1073.1000001073098)`.
2. `(0, 0, 1.0730991562013514e−7)`.

두 번째는 첫 번째에서 동일한 정수압 성분을 뺀 것이다. 입력 float 자체를 유리수로 정확히 바꾸어 계산하면 **두 VM은 정확히 같고**, 각각 `1.0730991562013514e−7 sim Pa`, 따라서 CV는 `0%`다.

실제 함수에서는 첫 입자의 전개식 근호가 `−4.656612873077393e−10 (sim Pa)²`로 나온다. 정확한 근호는 `1.1515417990400524e−14 (sim Pa)²`다. clamp 뒤 결과:

- 첫 입자 VM=0, 둘째 VM>0.
- `vm_cv=100.0%`, `status='computed'`, `contract='v2-invalid-null'`.
- Python float와 파서가 사용하는 NumPy float64 유형 모두 같은 반례.
- 두 입자에 둘째 응력을 동일하게 주는 양성 대조는 정상 `CV=0.0% / computed`.

**한정:** 거의 정수압인 매우 작은 편차응력의 경계 반례다. 현재 194개 침대에서 그 빈도나 실효 오염 크기를 측정한 것은 아니다. 그러나 “근호 음수면 물리적 VM이 0”은 거짓이고, 유효한 입력이 아닌 것으로 처리해야 할 수치 불확실성을 정상 `computed` 통계로 승격한다. 원 함수가 NaN을 통해 거짓 CV=0을 내던 결함도 정당화하지 않는다.

**Q4 답/최소 수정:** 현재 좁은 amendment의 “무효·미정의만 null+reason”으로는 이 clamp를 승인할 수 없다. 가장 좁은 처방은 수치적으로 부호를 잃은 비정수압 입력을 null+수치 사유로 보내는 것이다. 정확히 σxx=σyy=σzz인 입력은 해석적 VM=0임을 별도로 증명할 수 있다. 안정한 차이제곱식으로 재계산하는 대안도 가능하지만 **계산 알고리즘 교정의 별도 승인·회귀 범위**를 명시해야 한다. 모든 정상 입력을 무단 재산출하라는 요구가 아니다.

해결 증거에는 현재 S7의 *정확한 정수압* 양성 예제만이 아니라 위의 *거의 정수압* 예제를 추가할 것. null 처방이면 computed가 아니어야 하고, 승인된 안정식 처방이면 정확한 불변량과 일치해야 한다.

재현: `python3 run_probes.py vm` → `evidence/vm_boundary.json`.

## 3. 질문 Q1–Q5에 대한 직접 답

### Q1. 일반 경로에 검사를 생략해도 되는가?

**반대. 공용 기술 검사를 양쪽 게시 경로에 요구한다.** §2 RGLR2-01의 실례 때문이다. 기술 계약과 과학적 HOLD를 분리한 현재 구조를 유지하면서 공용 검사를 재사용하면 된다. 일반 경로에서도 fallback을 무조건 실패시킬 이유는 없다.

### Q2. 최소 rollback으로 다음 단계에 가도 되는가? pointer가 필수인가?

**격리된 WSL 소형 시험에는 갈 수 있다. 194로 이어지는 포괄 GO는 아니다.** 아래 네 조건을 붙인다.

1. 이번 소형 시험의 결과는 검증용이며 공식 활성 결과/ML 인계에 합치지 않는다. 별도 출력 위치에서 수행한다.
2. 정상 복원뿐 아니라 복원 실패도 넣고, 값·상태·실패 이유·UI가 일치하는지 검사한다.
3. 공식 재봉인/194 전에는 RGLR2-02를 닫고, 실행 중단 또는 잔여 stash/backup이 있는 디렉터리를 자동으로 유효 세대로 재사용하지 않는 회수 규약을 정한다. 현재 `recover_stale_stashes`는 파일 존재에 따라 옛 파일 일부만 복구하므로 원자성 증명이 아니다.
4. 실 Stage E·WSL·real14 회귀 결과와 코드/자료 봉인은 다음 판정에 제시한다.

원자적 다중 파일 commit을 주장하려면 generation directory+pointer 또는 복구 가능한 commit protocol이 필요하다. 반대로 **그 보장을 주장하지 않는 최소 구현**을 현재 범위에서 일률적으로 금지하지 않는다. 최소 구현이더라도 불완전한 복원을 “이전 값 그대로 유효”라고 말하는 것은 허용하지 않는다.

### Q3. 16ε 여유는 적절한가?

**현재 저장 규약과 정상 범위에서 채택 가능. 물리 오차막대나 모든 float에 대한 무조건 상한으로 부르지 말 것.**

먼저 정확한 십진 반올림을 가정하면 삼각부등식으로

`|σ_d − 1000·σ₀·q| ≤ 5e−7 + 1000·σ₀·5e−9 [mS/cm]`

가 나온다. 두 반폭의 합은 타당하다. σ₀는 실제 생산자에서 [network_conductivity.py:1414](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/scripts/network_conductivity.py#L1414)로 그대로 실리며, 이 검사에는 화면용 반올림 σ₀를 쓰지 않는다.

NumPy의 십진 반올림에는 10의 거듭제곱을 곱하고 나누는 오차가 추가된다. 이는 공식 [NumPy round 설명](https://numpy.org/doc/stable/reference/generated/numpy.round.html)의 구현 설명과 맞는다. 따라서 양의 유한 binary64 값, 중간 산술 overflow/underflow 없음, 현행 8/6자리 규약이라는 조건에서 생산자 곱·round·소비자 곱/뺄셈의 기계오차 여유를 더하는 것이 타당하다. `16ε`는 이 범위에서 보수적인 수치 여유로 수용하지만, 표본 통과만으로 무제한 전역 정리를 증명한 것은 아니다. 극단 입력까지 API 계약으로 받으려면 중간 곱·차·허용폭도 finite인지 검사하고 지원 범위를 명시해야 한다.

독립 검산:

- 8자리 반올림의 half-grid와 양옆 `nextafter`, σ₀의 온도/Ea 값, Python/NumPy 두 유형을 조합한 936건.
- 저장 후 양수 **648건 모두 수용**, 저장 후 0인 **288건 모두 거부**. 정상 양수 거짓 거부 0.
- 정확한 float 유리수 산술로 계산한 잔차/허용폭 최대 `0.9872210615678688`.
- 기준 예제 허용폭 `5.150000000853491e−7 mS/cm`. 양자화 항만은 `5.15e−7`, 추가 여유는 약 `8.535e−17 mS/cm`.
- 허용폭의 0.999배 잔차는 수용, 1.001배는 거부.

저장소의 2만 표본 시험도 다시 실행했다. 정확한 표현은 **19,900 양수 표본 수용 + 반올림 0인 100표본 거부**이며, “2만 개 정상 출력 전부 수용”이라고 압축하지 않는다.

**주의:** 이 검사는 두 저장값이 공통 원해에서 나올 수 있는 허용 범위인지 본다. 해의 물리적 정확성·수렴·유효숫자 충분성까지 보증하지 않는다. σ가 반올림 바닥에 가깝다면 절대 허용폭이 큰 상대 차이를 허용할 수 있다. 또한 round(q*,8)=0 또는 round(σ*,6)=0은 정상 비관통으로 바꾸지 않고 현재처럼 별도 기술 실패로 남겨야 한다. 유효숫자를 늘리려면 다른 계약 변경이다.

재현: `python3 run_probes.py precision`; `python3 run_tests.py tau`.

### Q4. VM clamp가 좁은 amendment 안인가?

**아니다. §2 RGLR2-03.** 결손·NaN·무하중의 null/상태 전파는 수용한다. 정상 균일 양의 VM의 CV=0 보존도 수용한다. 그러나 근호의 부호를 수치적으로 잃은 비정수압 입자를 VM=0으로 간주해 유한 CV를 생성하는 것은 “무효만 null”과 다르다. 별도 승인 없이 정상 계산값으로 승격하지 말 것.

### Q5. LW를 빼고 ⑤⑥⑦·망 τ만으로 Q6의 1단계에 넘어가도 되는가?

**동의. WSL 소형 통합시험 착수에 한정한 GO다.** RGLR-01–03이 닫혔고 LW 제외가 실재하므로 이전 문턱은 넘었다. 이후 일반 경로 게시·복원/VM 결정을 정리하고 재봉인해야 하며, 이 답으로 194건 또는 ML 배포까지 승인하지 않는다.

LW 제외는 [lhs_design_dataset.py:1219](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/scripts/lhs_design_dataset.py#L1219)의 실제 필터에서 작동한다. `_excluded.tsv`는 [동일 파일:4441](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/dbe0f076d7b948b8ebcfa85a02a391125b104fe2/scripts/lhs_design_dataset.py#L4441)에서 출력한다.

전역 virial은 상 배분/프레임 인증을 대체하지 않는다. 두 dimer의 힘을 교환한 이전 반례도 여전히 양쪽 OK이며 상 상대 응력은 0.5↔1.5다. 따라서 LW를 인계에서 뺀 것은 문제 해결이 아니라 **승인 범위를 정직하게 좁힌 것**이다. 웹앱이 LW 숫자를 표시할 수 있다는 사실과 ML 인계 자격도 구분한다.

## 4. 값 보존과 인계표 독립 대조

### 4-1. 원시 solver 수치

검증된 `eedada5d3` 기준 solver 파일과 현재 파일로 L0/L1/L2 × Hertz/Physics × FULL/CF/CONSTR **18경우**를 비교했다. 경계 집합과 `(G, σ_ratio)`의 `float.hex`가 전부 같다. `solve_network` AST도 같다. producer의 실패 상태 분류 변경을 수치 모델 변경으로 오인하지 않는다.

재현: `python3 run_probes.py raw18`. 이 비교는 `.git` 없이도 실행되며 원 참조 blob `2e0c4a47721cd8593b039fe1e189419bbb2eea64`를 검사한다.

### 4-2. 이미 커밋된 130/64 요약을 이용한 이전판↔현재판 인계 재생성

| 코호트 | 선택 묶음 | 표 크기 | 표·열 사전 이전/현재 |
|---|---|---:|---|
| 130 | contact,percolation | 130×189 | 바이트 동일 |
| 130 | 위 + f1,fracture,area | 130×223 | 바이트 동일 |
| 64 | contact,percolation | 64×191 | 바이트 동일 |
| 64 | 위 + f1,fracture,area | 64×225 | 바이트 동일 |

비교는 판정 대상이 신고한 해시를 그대로 믿은 것이 아니라, 이전/현재의 `build_handover`와 `column_dictionary`를 각각 실행하고 실제 CSV/TSV 직렬화를 대조한 것이다. 모든 SHA-256은 `evidence/handover_before_after.json`에 있다. LW 이름의 제외와 legacy σ_VM 이름의 비제외도 별도 검사했다. 저장소의 census✅·묶음 제한 없음·검토 목록 밖 변이 시험도 통과했다.

기존 요약의 산술도 다시 계산했다. 단계 비율 잔차 최대는 130에서 `0.004996359899 %p`, 64에서 `0.004978165939 %p`; 파괴지수 잔차는 각각 `4.9350649351e−5`, `4.8484848485e−5`. 쌍별 평균×개수=총합은 817+394개 비영 쌍에서 상대차 최대 `2.5613963026e−16`이다.

**새 194건 실행도, 원 dump 194건 재분석도 아니다.** 또한 기존 contact 요약에 `stop_after=network` 라벨을 붙였을 때 동일한 기존 열을 낸다는 시험은 실제 새 망 τ 수치의 인계 왕복을 대체하지 않는다. 그 끝-끝 검증은 후속 단계에 남긴다.

재현: `python3 run_probes.py handover handover_diff`.

## 5. 실행 결과와 미확인 범위

검토 사본의 소스/자료 443파일을 고정 핀의 Git blob 및 SHA-256으로 확인했다. 변경 목록은 두 핀 사이의 완전한 287파일 비교로 분리했고, 믹서 변경은 심사하지 않았다. 대형 `findings.json`은 별도로 원 blob을 읽어 관련 항목만 `inputs/findings_excerpt.json`에 보존했다. **443파일 전체 검증 목록에 전체 원장은 포함되지 않는다.** 원장의 claimed_fixed는 판정 근거로 삼지 않았다.

환경: Windows, Python 3.12.14, NumPy 2.5.3. 실제 실행 버전은 `evidence/precision_boundary.json` 및 `environment.json`에 남겼다. Linux/WSL 동일성은 이번에 확인하지 않았다.

| 저장소 시험 | 독립 실행 결과 |
|---|---|
| test_tau_flux | 51/51 |
| test_pipeline_provenance | 265/265 |
| test_tau_handover_status | 32/32 |
| test_network_handover_chain | 10/10 |
| network_conductivity selftest | 30/30 |
| test_network_boundary_rule | 8/8, ⑨ SKIP — 사본에 .git 없음; 위 raw18로 별도 대조 |
| test_love_weber_stress | 108/109 실행 단언; L12 real14 fixture 부재로 해당 그룹 실패 |
| test_stress_lw_labels | 70/70 |
| lhs_design_dataset selftest | 281/281 |
| lhs_stress_constriction_audit selftest | 12/12 |
| test_closed_param_groupview | 44/44 |
| test_tau_grade_unify | 19/19 |
| test_rint_receipts | 102/102 |

real14 자료가 없어 요청서의 **118/118 전체를 재인증하지 않는다.** 108/109는 missing-fixture 그룹을 포함한 실행 수이지 “118개 중 9개 코드 실패”가 아니다. `check_all.sh` 전수 초록도 독립 확인했다고 하지 않는다.

리뷰어 탐침 7묶음은 모두 예상한 결과에 도달했다. 여기에는 **결함이 발화해야 통과하는 반례 시험**도 포함된다. 따라서 `run_probes.py`의 exit 0은 제품 GO가 아니다.

## 6. 다음 판정에 필요한 최소 증거

1. **일반 게시:** RGLR2-01의 두 변이를 공용 기술 검사로 막고 정상 L0/L1/L2·비관통을 유지.
2. **복원 실패:** rollback 성공/실패를 상태·UI·소비자에서 구분. 위 혼합 세대가 유효한 이전 세대로 표시되지 않음. 기록 자체가 실패해도 읽는 쪽에서 불일치를 거부.
3. **LHS-33:** 비정수압 음수 근호의 null 처분 또는 별도 승인된 안정식 처리. 정상 값 불변/변경 범위와 계약을 정확히 적고 거의 정수압 반례 포함.
4. **실환경 소형 통합:** 실제 Stage E 사용 여부를 구분하고 WSL/real14·관통/비관통/풀이 실패·collector 계획/미계획을 검증. 이번 세 항목을 소형 검증의 음성 대조로 포함 가능.
5. **범위/봉인:** ⑤⑥⑦·망 τ만, LW 제외를 유지하고 수정된 파일을 승인된 amendment로 재봉인. 이후 별도 승인된 194 배치, τ 관문, 실제 숫자가 들어간 인계 왕복 순서.

이 리뷰는 위 목록을 구현하거나 사용자의 실행 승인을 대신하지 않는다. 기존 닫힘 항목을 이유 없이 다시 수정할 필요도 없다.

## 7. 재현 묶음

압축을 풀어 이 폴더에서 프로젝트 의존성이 있는 Python으로 실행한다. `run_tests.py`는 이 컴퓨터에 있을 때만 검토용 의존 경로를 추가하고, 다른 환경에서는 설치된 의존성을 사용한다.

```bash
python3 verify_source.py
python3 run_probes.py
python3 run_tests.py tau pipeline tau_status chain network boundary lw lw_labels lhs stress_audit group grade receipts
```

핵심 파일:

- `evidence/network_adversarial.json`: 실제 CLI·정지/일반 helper·복원 반례와 파일 해시·실제 UI 행.
- `evidence/lw_replay.json`: 원 CSV 파서→LW, 이전 반례의 닫힘.
- `evidence/vm_boundary.json`: 유리수 기준 VM·실 함수·양성 대조.
- `evidence/precision_boundary.json`: 반올림 경계·잔차·허용폭.
- `evidence/handover_before_after.json`, `handover_excluded.tsv`: 실제 인계 직렬화 대조·제외 사유.
- `evidence/raw18.json`: 원시 해 18비교.
- `source_manifest.json`, `package_manifest.json`, ZIP 옆 영수증: 검토 소스/묶음 무결성.
- `findings_review.json`: 이 검토의 지적 사항. 저장소 원장은 수정하지 않았다.

문서 작성 지침에 따라 **재현 사실·권고·미확인 범위**를 분리했다. 첨부 요청서의 자기신고는 검사 대상을 정하는 데만 썼으며, 닫힘 판정은 코드·실행·독립 산술에 근거한다.

**WSL 소형 통합시험만 조건부 GO / 공식 재봉인·194 생산·인계 HOLD**
