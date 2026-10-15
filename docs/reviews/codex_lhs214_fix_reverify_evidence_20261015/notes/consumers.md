# L214-02 독립 소비자 재검증

검토 핀 `9e3ef54ca228111360bfe5f6d9dad4ebe26d54af`, 기준 `0c557e72aaffdf6cfd033c0667c643de4501c5b1`. 생산 코드·원장·등록·Git 수정 없음. 실행은 작은 합성 침대, 제출 회귀 시험, 별도 합성 빌더 fixture만이다. 새 214 망 실행·실자료 재계산·배포 승인은 하지 않았다.

## 판정

**L214-02 전체 닫힘 불가.** 과거 세 검사 면제 반례(CF 증서, 세대 필드, 미채택 FULL 실제 증서 보존)는 닫혔고 다른 채널 실패도 차단된다. 그러나 **띠 폴백과 함께 발생한 H0 모형 한계가 배포 HOLD에서 사라지는 P2 반례**를 실제 생산자부터 인계까지 확인했고, 실제 `build_v13`/`check_v13`의 합성 경로에서도 재현했다.

### P2 — BAND_FALLBACK이 H0 FULL 모형 한계를 덮어 주 타깃 배포 HOLD 누락

원인 위치:

- `source/scripts/tau_flux.py:1234`–1236: L1/L2이면 `BAND_FALLBACK`, 사유 공란으로 반환. FULL `full_over_conduction` 표시는 그 뒤(1254–1260)에 있다.
- `source/scripts/lhs_release_build.py:666`–676: 모형 한계 식별을 **τ 상태 NOT_COMPUTED + 정확한 사유**에만 의존. canonical FULL 상태나 별도 분류 열을 읽지 않는다.
- 같은 식별자가 실제 build(2231–2235)와 check(2440)에 적용된다. `BAND_FALLBACK`은 기존 빈칸 코드 `HOLD_BAND_FALLBACK`으로 통과(885–886, 938–939).

재현은 상태 문자열 위조가 아니다. 기존 `band_l1`/`band_l2` 합성 사슬의 상자 변 길이만 10에서 0.1로 줄인 입력을 실제 생산자 CLI에 보냈다. 반경 0.4, z 간격 0.5, 면적 0.016, δ 0.02, 판 높이 40이다. L1은 81노드(0…40), L2는 21노드(0…10). 작은 상자 때문에 구 부피 분율은 물리적 침대 범위를 넘으며, 이는 **분류·게시·배포 계약의 합성 반례**이지 실제 침대의 발생률 주장이나 물리 검증이 아니다.

| 실제 생산자 fixture | H0 진단 q | 생산자 FULL | 게시 | reread | 인계 τ | 배포 H0 관문 |
|---|---:|---|---|---|---|---|
| L0 대조 `ml_hertz` | 1.6231747351909995 | not_computed / full_over_conduction | done | K1–K7 통과 | NOT_COMPUTED / full_over_conduction | HOLD |
| 독립 L1 | 8.927503013108073 | not_computed / full_over_conduction | done | K1–K7 통과 | BAND_FALLBACK / 공란 | 문제 없음 |
| 독립 L2 | 35.710012052432674 | not_computed / full_over_conduction | done | K1–K7 통과 | BAND_FALLBACK / 공란 | 문제 없음 |

H0/H12/Physics 세 모드의 `full_model_limit_problem`은 L1/L2에서 모두 None, 주 타깃 accepted 값은 null이다. `load_tau_results(expected_generation='g2')`의 P0–P4와 `build_handover(webapp_groups='tau')`를 실제로 거쳤으며, L1/L2 행의 빈칸 일관성 검사도 문제 0이다. 상태 우선순위 자체는 요청서 §5-7과 일치하지만, **그 상태를 유일한 모형 한계 식별자로 다시 사용하는 배포 규칙**과 충돌한다.

증거:

- `evidence/consumers_probe.json:270` L1 생산→소비, `:358` L2 생산→소비. 인계 결과 `:1432`, `:1452`.
- 원 입력·게시 파일·실제 수치 증서: `evidence/consumers_fixtures/independent_l1_h0/`, `independent_l2_h0/`.
- `evidence/consumers_release_probe.json:12` 및 `:32`: 실제 `build_v13(dry_run=False, diagnostic=False)`가 각 27파일 생성, warnings=[], `check_v13` 문제 [] 반환. L0 음성 대조는 `:4`의 ReleaseError.
- 생성 산출물: `evidence/consumers_release_verified/independent_l1_h0/output/`, `independent_l2_h0/output/`. 상위 `TEST_ONLY_NOT_GO.txt`대로 시험 전용이다.

**빌더 재현의 한정:** 빌더의 214행 중 나머지 행·감사/배치 기록은 제출 `test_lhs_release_v13.py`의 합성 fixture다. 선택행만 실제 생산·게시·P0–P4를 거친 인계 칸으로 대체했다. 선택행 K1–K7 결과도 합성 reread 기록에 실제 내용으로 넣었다. `v13_reread_tau`의 비교 함수는 그대로 실행하고, 원천 공급만 어댑터를 써서 선택행은 실제 검증한 `load_tau_results` 칸과 대조했다. 다른 행의 실제 수치 계산이나 생산 감사까지 독립 검증했다고 주장하지 않는다. 이 시험이 보여 주는 것은 **유효한 H0 모형 한계와 띠 폴백의 결합을 실제 빌더와 검사기가 누락한다**는 점이다.

무너지는 결론: 요청서 §5-4의 “H0 모형 한계는 진단 게시 후 실제 v1.3 배포 빌더에서 HOLD”가 **모든 허용 띠 규칙**에서 유지된다는 주장.

최소 처방: τ의 BAND_FALLBACK 표시 우선순위는 유지할 수 있다. 별도로 canonical FULL 모형 한계 사실을 인계/배포까지 보존하고, build와 check가 그 사실로 H0 HOLD를 판정해야 한다. 예를 들어 독립된 생산자 분류/사유 열 또는 원천 재독 결과를 사용할 수 있다. BAND_FALLBACK 전체를 막는 것은 기존 과학적 HOLD 정책을 불필요하게 바꾸므로 이 반례가 요구하는 수정이 아니다. L0/L1/L2 × H0/Physics/H12의 교차 회귀가 필요하다.

## 기존 반례 및 음성 경로

실제 `ml_physics` 생산 레코드 복사본의 Physics를 독립 변이하고 모드/dual 사본을 함께 갱신했다. 상태 투영 키도 맞춰 사본 불일치만으로 거부되는 시험이 되지 않게 했다. 결과는 `evidence/consumers_negative_paths.json`.

| 변이 | 일반 내용 검사 | 일반 레코드 검사 | stop | reread 거부 | 인계 |
|---|---|---|---|---|---|
| CF residual_rel=1 | 통과 | 거부 | 거부 | K2/K3/K4/K5/K6 | P4 거부 |
| bulk_model 삭제 | 통과 | 거부 | 거부 | K2/K3/K4/K5/K6 | P4 거부 |
| q_withheld ×1.01 | 거부 | 거부 | 거부 | K4/K6 | P4 거부 |
| thermal_status=failed | 거부 | 통과 | 거부 | K4 | P4 거부 |
| electronic_status=failed | 거부 | 통과 | 거부 | K4 | P4 거부 |
| 사유에 `:extra` 추가 | 거부 | 거부 | 거부 | K4/K6 | P4 거부 |
| Physics 증서 role=H12 | 거부 | 거부 | 거부 | K4/K6 | P4 거부 |

이온 FULL 전용 함수가 다른 채널의 실패를 직접 판정하지 않는 것은 각 경로에서 내용 검사를 함께 실행하는 현재 조합에서는 우회가 아니다. 일반 게시의 두 검사와 stop/P4에서 해당 실패를 실제로 막는다. 다만 수치 증서 내부 검사 자체의 타당성은 별도 수치 검증 결과를 합쳐 판단해야 한다.

Q1(L214-02): 실제 FULL 증서 보존, CF 증서 검사 재활성화, 세대 필드 누락 거부는 확인됐다. 정상 Physics 모형 한계, H0 모형 한계의 진단 게시, 전자 모형 한계 상태/사유 투영도 제출 끝-끝 시험 및 독립 fixture에서 확인됐다. 위 배포 차단 누락 때문에 전체 닫힘은 불가.

Q2 §5-4: H0의 진단 게시 자체는 역할별 정책과 양립하며 게시 단계에서 막아야만 하는 것은 아니다. 대신 그 게시물이 주 타깃 배포로 넘어가지 못하는 관문이 완전해야 하는데 현재 L1/L2 결합에서 불완전하다.

Q2 §5-6: K2 위임은 **K4/K6 필수 결합 경로에서는 수용 가능**하다. q×1.01 변이에서 K2 통과·K4/K6 거부를 독립 재현했다. K2만 통과한 것을 증서 전체 유효성으로 표현하면 안 된다. 다른 채널 실패는 K4에서 막히므로 모든 케이스가 K4를 빠짐없이 거쳐야 한다.

Q2 §5-7: 띠 폴백 우선순위는 유지 가능하지만, 주 타깃 배포 자격 판정에 필요한 원인 정보도 독립 보존해야 한다. 현 구현처럼 단일 상태/사유에만 의존하면 §5-4와 충돌한다.

## 회귀 및 재현

- `test_tau_flux.py`: 55/55 PASS.
- `test_gen2_role_contract.py`: 44/44 PASS.
- `test_network_handover_chain.py`: 34/34 PASS.
- 기록: `evidence/consumers_baseline.json` 및 `consumers_baseline_*.log`.

처음에는 임시폴더 쓰기 권한, Windows 자식 프로세스 문자 인코딩, 미수집 docs/data 때문에 중단했다. 별도 evidence 임시폴더·PYTHONUTF8/PYTHONIOENCODING·핀 확인된 자료 보충 후 **생산/시험 코드 수정 없이** 위 결과를 얻었다. 통과 수는 반례를 무효화하지 않는다.

재현 명령(작업 루트, 환경 PYTHONPATH에는 `lhs_coverage_review_20260930/deps`와 `gen2_network_reverify3_20261007/deps`, 수치 스레드 1):

```text
C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B lhs214_fix_reverify_20261015/probes/l214_consumers.py --baseline
C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B lhs214_fix_reverify_20261015/probes/l214_consumers.py
C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B lhs214_fix_reverify_20261015/probes/l214_consumers.py --negative
C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B lhs214_fix_reverify_20261015/probes/l214_consumers.py --release
```

## 보충 자료 반입 뒤 최종 두 회귀

핀에서 확인한 누락 감사 원천과 r6 S0b 입력 7개를 공급한 뒤, 원본 두 스크립트를 변경 없이 다시 실행했다. 전체 로그는 `evidence/baseline_release_final.log`, `evidence/baseline_reread_final.log`, 요약과 환경 대조는 `evidence/baseline_consumers_final_summary.json`.

- `g2_network_reread.py --selftest`: 29/29, rc=0, 29.3초. 실제 S0b 기록의 양성·음성 대조까지 통과.
- `test_lhs_release_v13.py`: 254/256, rc=1, 76.3초. 잔여 실패는 V10a와 V16a.
- V10a (`test_lhs_release_v13.py:705`): 실제 `/R\\manifest.json`, `/R\\merged\\lhsx\\results`, `/R\\merged\\lhsx`를 POSIX 문자열과 직접 비교한다. 세 경로 모두 `os.path.normpath`로 비교하면 동일하다. Windows 구분자 의존 기대값의 환경 실패다.
- V16a (`test_lhs_release_v13.py:973`): `sealed_changed=[]`, `handover_changed=[]`이며 봉인/인계 해시 대조는 통과했다. 다만 Git checkout이 아닌 핀 검토 사본이라 `git_head=None`; 시험은 추가로 40자리 HEAD를 요구한다. 읽기 전용 `git rev-parse --show-toplevel`도 `not a git repository`였다. 이 실패를 없애려 Git을 만들거나 판정 값을 위조하지 않았다.

재현은 같은 탐침의 `--final-baselines`와 `--final-baseline-environment`. 이 두 환경 실패를 256/256으로 계수하지 않는다. 위 P2 반례의 판단에는 변화가 없다.
