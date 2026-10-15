# L214-01 독립 수치·생산자 재검증

검토 핀 `9e3ef54ca228111360bfe5f6d9dad4ebe26d54af`, 기준 `0c557e72aaffdf6cfd033c0667c643de4501c5b1`.
`source/AGENTS.md`, 10-14 판정 및 10-15 요청서를 읽고 별도 사본에서만 실행했다. 검토 폴더는 Git 저장소가 아니며 Git 상태 확인 네 명령은 모두 그 사실을 반환했다. 소스·등록·원장·Git 상태를 수정하지 않았다. **본 수치 탐침**에는 실제 침대·새 214 실행이 없다. 이후 별도로 허용된 원 A4의 real_14/case15 회귀 재실행은 `notes/a4.md`에 구분해 기록했다.

## 판정

**L214-01은 닫힘 보류.** 정상 생산자 동작과 이전 핵심 반례의 차단은 확인했지만, 새 공용 증서 판정에 재구성 q의 유한성 누락이 남았다. 마지막 채택 시도의 수치 기록과 상위 요약 간 모순도 통과한다. 두 반례 모두 사유 문자열만의 시험이 아니라 실제 생산자에서 나온 합성 레코드의 복사본과 실제 소비 함수를 사용했다.

## N1 · P2 · 비유한 재구성 q를 유효한 모형 한계로 받음

위치: `source/scripts/network_conductivity.py:1011`–`:1015` (`model_limit_certificate_problem`).

21노드 합성 생산자 Physics 레코드의 원 진단 q는 `2.593468501694396`이다. 다른 레코드·기하·σ₀·채널·역할·출력 null을 그대로 두고 FULL 증서의 `I_bottom=1e308`, `I_top=-1e308`, `sum_g=1e308` 및 마지막 pass 시도의 두 전류만 같은 값으로 바꿨다. `T=20`, `A=1`, `delta_V=1`이므로 기록된 식의 `q_rec=(1e308/1)*20/1`은 `+inf`다. 전류 합은 0이고 병렬 상한 `1.1e308`은 유한하다.

`q_withheld`는 여전히 유한한 `2.593468501694396`인데, 상대오차 검사가 `abs(finite - inf) <= 16*epsilon*abs(inf)`, 즉 `inf <= inf`가 되어 통과한다. 이후 두 q의 `>1.5` 검사도 통과한다.

실제 함수 반환:

| 검사 | 반환 |
|---|---|
| `full_model_limit_problem` | `None` (유효) |
| `ion_record_problem` | `None` |
| `certificate_binding_problems('physics', rec)` | `[]` |
| `network_generation_contract(dual)` | `generation='g2'`, `problems=[]` |
| `channel_verdict(rec, 'ionic', 'physics')` | `ok` |
| `ion_columns` | Physics `NOT_COMPUTED/full_over_conduction`; 네 파생값 null |
| 모드 JSON 두 파일을 읽는 `network_content_verdict` | `(True, 'ok: hertzian, physics')` |

별도 3노드 증서에서도 `T=A=1e308`, `g_to_q=1`, `I_bottom=2`, 저장 q=2로 같은 문제가 재현된다. 반면 그 기하의 **실제 solve_network**는 중간 곱으로 q=inf가 되면 `not_computed/non_finite`로 거부한다. 즉 생산자와 공용 증서 판정이 서로 다른 결론을 낸다.

최소 수정: 비교 전에 재구성 `T/A`와 `q_rec`를 명시적으로 유한 양수로 검사하고, 연산 넘침을 안전하게 거부한다. 원 정밀도의 q>1.5 및 상대 16ε 규칙은 그 뒤에 적용한다. 해당 변이체가 공용 판정과 파일 소비 관문에서 기술 실패로 차단되는 시험 필요.

한정: 실침대에서 이런 전류가 발생했다거나 214의 실제 결과가 잘못 게시됐다는 뜻은 아니다. 새 예외의 필수조건인 유한 q를 만족하지 않는 **내부적으로 모순된 레코드**가 실제 수용 함수에 통과한다는 반례다. 전체 승격·정지·reread·배포 절차까지 이 탐침 하나로 실행한 것은 아니다.

증거: `evidence/numeric_probes.json` → `records.overflow_q_reconstruction_currents`, `certificate_mutations.overflow_q_reconstruction_geometry`, `solves[label=q_intermediate_overflow]`.

## N2 · P2 후보 · 마지막 pass 시도의 수치 실패 기록이 상위 요약과 결합되지 않음

위치: `source/scripts/network_conductivity.py:993`–`:998`.

실제 합성 생산자 Physics FULL 증서의 마지막 시도에서 `residual_rel` **한 필드만** `1.0`으로 바꾸면 상위 요약의 작은 잔차와 모순된다. 현재 검사는 `outcome='pass'`, 방법, 두 전류만 결합하고 해당 시도의 잔차를 검사하지 않아 N1 표의 모든 함수가 동일하게 통과한다. 마지막 시도의 `conservation_rel=1.0`, `krylov_info=1`도 각각 통과한다. 3노드 증서 수준에서는 잔차 NaN, 예외 error 문자열이 남아 있어도 통과한다. 반대로 outcome 변경 또는 마지막 전류만 바꾼 대조군은 거부한다.

이는 마지막 시도 기록을 필수 증거로 쓰면서 그 내용의 자기모순은 허용하는 결합 누락이다. 생산자의 실제 사다리는 `source/scripts/network_conductivity.py:1314`의 미수렴 검사와 이어지는 잔차 검사를 통과한 값만 채택하므로, 정상 생산자가 이 모순을 만들어낸다는 주장은 하지 않는다. 기존 일반 발행 증서가 attempts 전체를 검사하지 않는 정책과 새 FULL 모형 한계의 "마지막 pass" 보증을 구분해야 한다. 통합 검토에서 등급을 결정할 수 있도록 P2 후보로 남긴다.

최소 수정: 채택 시도의 보존·내부 잔차를 동일 수치 규칙으로 검사하고 상위 요약과 결합한다. 채택 방법에 맞는 `krylov_info` 성공 조건과 예외 없음도 확인한다. 기록이 상충하면 더 유리한 요약만 골라 믿지 않는다.

증거: `evidence/numeric_probes.json` → `records.contradictory_attempt_residual_rel`, `records.contradictory_attempt_krylov_info`, `records.contradictory_attempt_conservation_rel`; `certificate_mutations`의 대응 항목.

## 별도 낮은 위험 관측 · 극단 유한 scale의 제곱 예외

`source/scripts/network_conductivity.py:961`의 `scale ** 2`는 Python float `scale=1e200`에서 `OverflowError`를 낸다. `solve_network`의 초기 `_g2q` 계산은 예외를 잡지만 새 `_geometry_TA` 호출은 잡지 않아 상태·사유가 null인 미완성 solve_info를 남긴다. 공용 증서 함수도 같은 예외를 낸다. `channel_verdict`는 이 예외를 잡아 fail로 반환하므로 게시 허용 반례는 아니다. 극단 무효 기하를 `invalid_geometry`로 정리한다는 반환 계약의 보완점(P3 수준)이며 N1과 같은 fail-open으로 취급하지 않는다.

## 닫힌 부분과 재계산한 근거

- 독립 실제 solve_network 탐침 38개: q=1.5 및 `nextafter` 양옆은 각각 `1.4999999999999998` computed, `1.5` computed, `1.5000000000000002` full_over_conduction. 열 q=2는 computed. CF q=5, 협착-only q=10/3은 진단값 유지.
- 기하 네 필드 각각 bool·문자열·0·음수·NaN·±inf 28조합이 invalid_geometry로 차단된다. 무한 plate_z를 정상 모형 한계로 읽던 옛 직접 반례는 닫혔다.
- q=2의 상대 16ε 경계에서 +1/+8/+16 ulp 허용, +17/+32 ulp 거부. 이 유한 범위의 허용은 구현·문서와 맞는다.
- `_cg` 시작부터 전도도 환산 직전까지의 기존 수치 사다리 바이트는 base/source **완전 동일**. 독립 21노드 정상 합성 대조(Hertz/Physics, box=3)에서는 새 상태·사유 네 메타 키를 제외한 모든 필드가 `float.hex()` 포함 재귀 비교에서 동일하다. 이 대조를 실침대 A4 전체의 독립 재실행으로 확대 해석하지 않는다.
- 실제 생산자 FULL 모형 한계에서 accepted σ·차원 σ null, CF/FULL·Bruggeman/FULL 비 없음, 협착 전력 몫 null 및 정확한 모델 사유, τ f/f_gap/τ²/τ null을 확인했다.
- 기존 `test_lhs214_model_limit.py --selftest`를 실행해 **55/55 PASS**. `network_conductivity.py --selftest`도 종료코드 0, status **31/31 PASS**. 첫 실행 한 번은 Windows 기본 임시 폴더 쓰기 권한으로 52/53에서 멈췄고, TMP/TEMP를 검토 폴더 `tmp`로 한정해 재실행 후 모두 통과했다. 이 환경 실패를 제품 결함으로 세지 않는다.

## 재현

검토 루트에서:

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B probes/l214_numeric.py
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B probes/l214_numeric.py --selftests
```

탐침이 deps 두 경로, 단일 BLAS/OMP 스레드 및 검토 전용 TMP/TEMP를 설정한다. 출력: `evidence/numeric_probes.json`, `evidence/numeric_selftests.json`, `evidence/numeric_selftest_model_limit.log`, `evidence/numeric_selftest_network.log`. NaN/Infinity는 무효 입력을 정확히 보존하기 위한 검토 JSON 표현이며 생산 파일에서는 유효 레코드 변이체의 유한 값만 사용한다.
