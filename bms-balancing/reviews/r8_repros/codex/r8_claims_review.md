# R8 입력·기준 출처 독립 검토

대상 `a22da3380338f97b8eed2f600ffefad1e398c6c3`. 요청문을 완독하고 현행 소스를 다시 확인했다. 최종 실행 사본은 `work/harness-r8-target-wsl/bms-balancing`이다.

재현: [r8_claims_repros.py](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r8_claims_repros.py).

```bash
python /path/to/review/r8_claims_repros.py --target /path/to/a22da338/bms-balancing --case all
```

이 실행은 rc 0이었다. `noise`, `matrix`, `profile`, `shape`, `closures`를 각각 선택할 수 있다. rc 0은 닫힘 대조와 아래 반례의 예상 결과를 모두 관측했다는 뜻이다. NumPy 2.5.3 / SciPy 1.18.1 / pandas 3.0.5, Python 3.12.3에서 실행했다. R8에 그대로 보존된 R7 재현 파일의 합성 데이터·임시 fixture 유틸리티를 재사용한다.

대상 코드·원자료는 변경하지 않았다. 모든 계산 입력은 저장소의 합성 XLSX 생성기로 만들었다. 실제 loader/Objective/SciPy optimizer를 사용했고, GITT/Li/w=0, starts=2, seed=0, profile grid=3으로 실행 범위를 제한했다. 최적화 결과를 임의 반환값으로 바꾸지 않았다. 임시 경로와 XLSX 생성 시각 때문에 digest 문자열 자체는 재실행마다 달라질 수 있다. 시험은 입력 역할별 digest 관계와 수치 결과를 assert한다.

## 인정하는 닫힘

### R7-02 noise: 닫힘

[verify.py:188](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/bms_balancing/verify.py:188)의 `obj.full_cell_raw=(c,v)`와 [1721](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/bms_balancing/verify.py:1721)의 소비가 실제로 이어진다. build(A) 직후 같은 XLSX를 정상 B로 재-export해도 noise의 **전체 JSON이 A/A 대조와 정확히 같다**. 단순히 비율·분기만 같은 것이 아니라 입력 identity도 같다.

| 관측 | A/A | build 후 정상 B 재-export | 일관 B/B |
|---|---:|---:|---:|
| misfit RMSE (V) | 0.028876177864090954 | 같은 A 값 | 0.025941618063608392 |
| σ(k=1) (V) | 0.00001334727534677551 | 같은 A 값 | 0.018195773977771966 |
| misfit/σ | 2163.451124956898 | 같은 A 값 | 1.4256946747799122 |

이전 A 분자/B 분모 반례는 사라졌다. 잡음용 배열이 평활된 다른 배열로 바뀌지 않았다는 것도 A 대조의 수치 동일성으로 확인했다.

### R7-03 matrix: 닫힘

[verify.py:1389](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/bms_balancing/verify.py:1389)의 `ref_inputs_sha`와 target/ref `consumed_inputs`가 실제 두 build가 소비한 입력과 일치한다. pristine A를 만든 다음 공유 fullcell workbook의 pristine 전압 열만 +20 mV로 정상 재-export하여 target B를 만드는 기존 일정을 다시 실행했다.

| 관측 | reference A / target B | B/B |
|---|---:|---:|
| LAM_NE (%) | 2.849754951167859 | 5.367912841968694 |
| target inputs_sha | 같은 B 서명 | 같은 B 서명 |
| ref_inputs_sha | A 서명 | **다른 B 서명** |
| 두 전체 identity | 실제 A/B 소비와 일치 | 실제 B/B 소비와 일치 |

다른 export 사용을 허용하는 현행 정책 아래, 이제 둘을 구분할 정보가 행에 남는다. 같은 export를 강제하지 않았다는 사실 자체를 입력 서명 오류로 다시 세지 않는다.

### R6-03의 기존 build·ne_shape 다중 읽기: 닫힘 유지

풀셀/half-cell/문헌 Si/Gr 각각 snapshot 직후 같은 경로를 정상 재-export했지만 파일당 읽기는 1회, 배열과 digest는 A/A였다. stable B를 별도로 읽으면 값과 digest가 함께 바뀌었다.

ne_shape의 200 half-cell snapshot 뒤 PE +20 mV 및 NE capacity ×0.8 재-export에서도 HalfCell·raw capacity·identity가 모두 A를 사용했다. 원래/중간 산출의 `cap_delta_pct=0.0000`, `pe_shape_max_mV=8.000000`; stable B는 각각 `-20.0000`, `12.000000`이었다. 현재 입력 하나 내부에서 다시 hash만 B를 읽는 반례는 만들지 못했다.

## 새 조건 C1 — P1: profile의 전체 입력 identity가 검증 묶음 밖의 소모성 로그에만 있다

영향은 **원시 입력 provenance의 보존**이다. profile CSV 숫자가 틀렸다거나, 실패한 새 실행을 성공했다고 보고했다는 반례는 아니다. target/ref의 **짧은 aggregate digest 두 개는 CSV에 남는다**는 점을 인정한다.

관련 위치:

- [verify.py:1560](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/bms_balancing/verify.py:1560): CSV 행에는 target/ref aggregate digest만 있다.
- [1571](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/bms_balancing/verify.py:1571), [1595](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/bms_balancing/verify.py:1595): 개별 파일 path·sha256을 포함한 전체 identity는 `SUMMARY`로 stdout에만 출력한다.
- [run_states.sh:154](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/run_states.sh:154), [218](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/run_states.sh:218): stdout은 고정 `.csv.log`를 실행 전에 잘라 기록한다.
- [run_states.sh:67](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/run_states.sh:67): meta는 CSV를 검증하지만 그 SUMMARY를 포함하거나 log에 결속하지 않는다.

### 실행 가능한 상태

`--case profile`은 실제 profile 최적화로 3개 CSV 행과 SUMMARY를 만든 뒤, 현재 `write_meta()`의 원문을 실행하여 정상 묶음을 만든다. data_root/starts는 실제 합성 입력/2회로 설정했다. 첫 `verify_unit`은 `(True, '일치')`다. SUMMARY에는 양쪽 전체 identity가 있고 행의 aggregate digest와 일치한다.

이어 현재 `run()` 원문을 실행하면서, 정상적으로 존재하지 않는 입력 경로로 profile을 재시도한다. 이는 데이터 디렉터리가 잠시 마운트되지 않은 경우와 같은 일반 실행 실패다. 새 producer를 사칭하거나 run_id를 복사하지 않는다.

직접 관측:

```text
profile_rows: 3
summary_had_both_input_identities: true
retry_rc: 1
old_csv_and_meta_unchanged: true
old_unit_after_retry: [true, "일치"]
old_identity_summary_remaining: false
log: .../input-export-not-mounted 아래에 data/literature 가 없다 — 경로가 맞나?
```

기존 CSV/meta는 그대로이고 여전히 정상 검증되지만, 그 결과가 소비한 파일별 path·hash를 적은 유일한 SUMMARY는 사라졌다. 두 aggregate digest는 파일별 identity를 역산하는 데이터가 아니다. 현재 pathname을 다시 hash하여 채우면 이후 재-export와 구분할 수 없다. 별도 matrix가 같은 입력을 썼다는 보장도 profile CLI에는 없다.

이는 F01b 재보고가 아니다. 과거 계산 결과 묶음 자체는 보존되어 있다. **이번 R8이 입력 identity를 새로 배치한 위치가 그 묶음 밖**이라는 결함이다. wrapper가 재시도를 rc 1로 정확히 보고하는 것도 인정한다.

최소 닫힘 조건: 전체 target/ref 입력 identity를 profile CSV의 검증되는 내용에 담거나, 함께 결속되는 metadata/sidecar에 한 번 보존한다. 별도 로그를 전체 원자료 provenance의 유일한 보관소로 삼지 않는다. 불변 generation이나 전체 로그 보관 시스템을 요구할 필요는 없다. 위 실패 재시도 뒤에도 기존 정상 profile의 전체 identity를 그 검증 묶음에서 회수할 수 있으면 이 조건은 닫힌다.

## Q3 관련 관측 — shape의 fit export와 평가 export 정책 (별도 P1로 세지 않음)

실제 matrix 네 상태를 적합·정상 게시한 다음, 문헌 Gr workbook만 `voltage += 0.040 * normalized_capacity²`로 정상 재-export했다. ne_shape를 전후에 실행하면 둘 다 rc 0이고 원래 matrix의 γ쌍을 그대로 쓴다. 합성 200의 실제 적합 쌍은 `(0,0)`였다.

| 200 관측 | 적합에 사용한 Gr A | 현재 평가 Gr B |
|---|---:|---:|
| (c) max (mV) | 462.929878 | 463.694386 |
| (c) rms (mV) | 248.674214 | 247.792133 |
| γ sampled family max (mV) | 227.662346 | 228.022038 |

여기서 ne_shape meta는 원래 matrix의 bytes identity와 현재 Gr B의 identity를 **정직하게 둘 다** 기록한다. 따라서 이것을 A 계산/B 서명 혼합으로 세지 않는다. 다만 [ne_shape.py:107](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/ne_shape.py:107) 이후 선택은 matrix의 새 `consumed_inputs`를 현재 문헌 입력과 대조하지 않으므로, 기본 출력의 `Blend(x, γ_적합)`이 "원래 적합 모델"인지 "새 문헌 곡선에 과거 숫자를 대입한 평가"인지 자동 구분하지 않는다.

이를 이번에 새 P1로 자동 계수하지 않는다. 다른 export에서 과거 γ를 평가하는 것은 명시적인 비교 실험으로도 유효하다. 권고는 그 모드를 원래 적합 모델 재현과 구분하고, 버전이 다르면 그 차이를 출력하는 것이다. 특히 **ne_shape에는 재적합 경로 자체가 없다**. 요청문 Q2의 '재적합 경로'는 정확히는 저장된 γ쌍 평가 경로다.

## 질문에 대한 범위 답변

- **Q2:** noise와 HalfCell/raw capacity/문헌 snapshot에 대한 기존 이중 읽기는 닫혔다. 새 C1은 이중 읽기가 아니라 기록 보존의 다음 단계다.
- **Q3:** identity가 양쪽을 정확히 기록한다면 서로 다른 export를 읽었다는 사실만으로 수치가 자동 무효가 되지는 않는다. 단 "같은 모델/같은 공통 원자료에서 상태만 비교"하는 모드는 공유 문헌·공유 workbook snapshot 재사용을 기본으로 하는 것이 명확하다. 별도 export 비교는 각 역할·버전을 명시한다. 상태별로 원래 다른 half-cell 파일을 동일하게 만들 필요는 없다.
- **Q6:** 다섯 관측의 제한된 인용은 이번 대조로 반증되지 않았다. 이 합성 반례를 비공개 실측의 오류로 소급하지 않는다. 후보 모델 변경·대안·구분 실험·기각 기준을 분리하는 구조를 유지한다.

## 작업 무결성

shape 첫 probe에서 `--out-dir`를 쓰기 옵션으로 잘못 이해하여 작업공간 루트에 합성 CSV/meta/lock 3개를 생성했다. 기존 root `out/`이 없었음을 부모가 확인했고, 정확한 3개 파일을 `outputs/r8_claims_accidental/`로 옮겨 보존한 후 빈 root `out/`만 제거했다. 최종 probe는 `--write`를 임시 경로로 지정한다. 대상 checkout은 이 과정에서도 수정하지 않았으며 Git status가 clean인 것을 확인했다.
