# Codex 재검증 요청 (4차) — RGLR2-01 · 02 · 03 수정 + WSL 소형 통합 + 194 실행 등록 (2026-10-05 밤)

- 기준 판정: `docs/reviews/codex_review_rglr_reverify_20261005.md` (핀 `dbe0f076d` · 기존 RGLR-01 · 02 · 03 닫힘 · 새 P1 없음 · P2 셋 · 격리된 WSL 소형 통합만 조건부 GO · 재봉인 · 194 · 인계 HOLD).
- 이번에 고친 것: 판정문 §2 의 P2 셋 = `RGLR2-01` (일반 게시 경로 기술 검사) · `RGLR2-02` (되돌림 실패 표지 · 읽는 쪽 세대 불일치 거부) · `RGLR2-03` (옛 σ_VM 음수 근호 clamp) + §6-4 실환경 소형 통합 + §6-5 범위 · 봉인 기록.
- 1저자 비준: *"진행하자 ㅇㅇ"* (10-05 밤 · 수정 셋 · WSL 소형 시험 · 194 병렬 실행기) · *"권고하는대로 가"* (RGLR2-03 문턱 K = 2^20 — §1) · *"나로 진행하자"* (194 배치를 이 재검증과 **병렬** · 배포는 GO 뒤 — §5).
- 핀 = `11fcf91e8` (브랜치 `claude/sdcp-dem-manuscript-si-pqwtv8`).

## 1. 패치 (오래된 순)

| 커밋 | 원장 | 내용 |
|---|---|---|
| `902d549ff` · `a8a824cf8` · `ce16a0be7` | (실행 도구) | 194 병렬 실행기 `scripts/run_network_194_parallel.py` — 케이스마다 기존 배치 CLI (`lhs_webapp_batch.py --stop-after network --case`) 한 번 · 동적 큐 · 갈래 20 × 1 스레드 · 케이스별 TMPDIR (망 lock 이 케이스 안에서만 → 기계 전체 하나씩 잠금 대신 **메모리 예산 입장 관문** · 실측/추정 비 기록) · cwd = 케이스 폴더 (LHS-27) · pyc 경쟁 · merge = 배치 writer (순차 한 번과 바이트 대조) · manifest (git · 코드 해시 · 스레드 · lock) · selftest 29 |
| `c292c05be` | §6-4 | WSL 소형 통합 시험 `scripts/wsl_network_smoke.py` — 격리 ROOT · real_14 일반 경로 (실 Stage E) ↔ 망 정지 · LHS 셋 (관통 · 비관통 · lhsx) · 음성 대조 C1 · C1b · C2 · C3 (주입 발화 계수) · selftest 10 |
| `05fbf15aa` | (선택) | 웹앱 케이스 망 단계 격리 러너 `scripts/webapp_network_batch.py` (보고용 다섯 조성 재확인) |
| `8bf727724` · `7ca5211e8` | §6-5 | 인계 생성기 망 τ 묶음 `tau` — `--tau-results <work>/results` 의 케이스 폴더를 배치 기록과 대조 (P0 파일 · P1 run id = full_metrics = 도장 = provenance · P2 입력 다이제스트 · P3 같은 세대 투영) 뒤 `tau_flux.case_row` 그대로 · network 정지 배치에만 · 열 사전 τ 명명 규약 · LW 제외 유지 · τ 없으면 옛 산출 바이트 동일 (24 파일) |
| `b2d8f80dc` | RGLR2-03 | `diag_von_mises` — 전개식 근호 vm_sq > 2^20·B 면 옛 값 비트 동일 · 아니면 ½[(σxx−σyy)²+(σyy−σzz)²+(σzz−σxx)²] (B = 16·ε·Ŝ + 2^-1071 · 유도 최악 7.0001 ε S · 실측 1.19 ε Ŝ) · 정확 정수압 = 0 · 0 clamp 제거 · 계약 `v3-invalid-null-stable-vm` · 다시 계산 수 기록 · 감사기 같은 규칙 · 웹앱 툴팁 |
| `5d0f30984` | RGLR2-01 · 02 | `pipeline_service.network_record_verdict` (= `tau_flux.ion_record_problem` 을 두 모드 · 소비자가 읽는 모든 사본에) 를 일반 · 정지 경로 공통 승격 전 필수 단계로 · 되돌림 결과를 게시 전 해시와 대조 → 실패 = `rollback_failed` · active `invalid` · kept False · 복구 자료 보존 · 읽는 쪽 `tau_flux.network_generation_problem` (도장 손상 · 중단 흔적 · full_metrics ↔ 도장 불일치 · 무효를 남긴 최근 시도) → 화면 · 보고 · 목록 · 등급 가드 · τ `generation_invalid` · 중단된 게시 회수 규약 |
| `11fcf91e8` | 기록 | 탐침 재실행 기록 · 원장 · 실행 등록 · 실행기 봉인 경로 정정 (두 파일이 `webapp/` 로 잘못 적혀 해시가 None 으로 빠지던 것 → `scripts/` · 없는 봉인 파일 = 발사 거부) · τ 열 사전 사유 여섯 |

## 2. 판정문 §6 최소 증거 대응

| §6 | 무엇을 했나 | 증거 (수정 전 → 수정 뒤) |
|---|---|---|
| 1 일반 게시 | 공용 기록 검사를 두 경로 공통 승격 전 단계로 · 과학적 HOLD (L1/L2 띠 폴백 · 비관통 valid_zero · 온도 변환) 는 옮기지 않음 | `webapp/test_pipeline_provenance.py` 268/284 → **284/284** (T21a–b) · `scripts/test_tau_flux.py` 50/55 → **55/55** · Codex 탐침: `general_ratio_times4` · `general_band_ratio_missing` done → **failed** · 양성 셋 그대로 |
| 2 복원 실패 | 상태 · UI · 소비자에서 구분 · 상태 파일을 못 써도 읽는 쪽이 디스크로 판정 | T22b–h · T23a–g · `webapp/test_tau_handover_status.py` 32/37 → **37/37** · `webapp/test_tau_grade_unify.py` 19/20 → **20/20** · 탐침 `rollback_destination_failure`: kept True · active success · "그대로" → **rollback_failed · kept False · active invalid** · τ NOT_COMPUTED (generation_invalid) |
| 3 LHS-33 (VM) | 승인된 안정식 처리 (1저자 비준) · 정상 값 범위 = 편차/압력 ≳ 8.6e-5 입자는 비트 동일 · 거의 정수압 반례 포함 | `scripts/test_love_weber_stress.py` 113/139 → **139/139** (Codex 반례 Python · NumPy → CV 0.0 · 평균 = 정확 VM 비트 동일 · 퍼즈 600 · 결정 규칙 1,200 · float32 · 정확 정수압) · `webapp/test_stress_lw_labels.py` 69/72 → **72/72** · `scripts/lhs_stress_constriction_audit.py --selftest` 12/14 → **14/14** (real_14 감사 JSON 바이트 동일 · 다시 계산 0) · 탐침 vm: CV 100 → **0.0** |
| 4 실환경 소형 통합 | WSL (1저자 · `~/dem-audit`) | 고치기 전 `05fbf15aa`: 실데이터 22/22 PASS · 음성 대조 4 FAIL (Codex 증상 그대로 = 정상) · rc 2 · 고친 뒤 `11fcf91e8`: **26/26 PASS · rc 0** — 실데이터 22 그대로 · C1 (일반 ×4) · C1b (일반 L1 + σ_ratio None) → failed · C2 (I/O 실패 둘) → 되돌림 실패 상태 · C3 (거의 정수압) → CV 0 · real_14 · LHS 셋의 σ 는 고치기 전과 같다 (수정은 풀이를 안 건드린다) · 기록 `docs/reviews/codex_rglr2_fix_probe_rerun_20261005/wsl_smoke_postfix_11fcf91e8.md` (고치기 전 `wsl_smoke_prefix_05fbf15aa.md`) · real_14 망 정지 27 s · 0.55 GB · 일반 경로 (실 Stage E) partial = 리포에 없는 부가 분석 스크립트 · 필수 단계 전부 성공 · collector 계획/미계획 = 웹앱 망 경로에 STEP3 collector 가 없어 해당 없음 |
| 5 범위 · 봉인 | ⑤⑥⑦ · 망 τ 만 · LW 제외 유지 · 실행 등록 `docs/reviews/lhs_network_batch_registration_20261005.md` (19 파일 sha256 = 실행기 manifest 대조 · 결과 전 관문 · 회귀 허용 변경 목록 · 09-17 cutoff 무변경) | — |

탐침 재실행 기록 = `docs/reviews/codex_rglr2_fix_probe_rerun_20261005/README.md` (결함 단언만 뒤집은 사본 둘 · 1–104 행 동일 · 증거 JSON).

## 3. RGLR2-03 문턱 — 비준 문자 (B) 와 다른 점

비준 문안은 "vm_sq ≤ B 면 다시 계산" 이었다.  B 그대로 (K = 1) 면 경계 바로 밖에서 같은 부류가 남는다 — 쌍 (68032.70000000001, 68032.70000000001, 68032.70680327002) 과 오프셋 없는 짝의 CV **1.725 %** (정확 0) · 퍼즈 600 중 98 이 4 ulp 밖 (최악 VM 오차 1.1 %).  K = 2^20 이면 둘 다 0 · 지켜진 값의 상대 오차 < 9.5e-7 (엄밀 · 실측 최대 2.2e-8).  1저자 *"권고하는대로 가"*.  상수 하나 (`VM_RESOLVE_K`).

## 4. RGL-06 · RGL-08 — 닫힘 확인 요청

3차 판정은 두 항목의 잔여를 따로 판정하지 않았다 (원장 claimed_fixed 유지).  닫힘 여부를 명시해 달라.

## 5. 194 배치 — 이 재검증과 병렬 (이탈 기록)

- 1저자 (나): 수정 셋은 망 σ · τ 수치 경로를 바꾸지 않는다 (원시 해 비트 동일 = 3차 §4-1) → 194 배치를 이 요청과 **동시에** 돌린다.  결과는 격리 폴더 · 실행기 manifest 의 코드 지문 = 등록 표 · **배포 (ML 인계) 는 GO 뒤** · 값에 영향 주는 결함이 나오면 해당 케이스 재실행 + 등록 덧붙임.
- 시범 (고치기 전 코드 · 시간 · 메모리만): `lhsx_040` (접촉 62 만) 171 s · RSS 2.6 GB · WSL MemTotal 15.5 GB.

## 6. 정오 (SELF-88)

3차 요청서 §9 RGLR-02 행 *"생산자 형식 표본 20,000 … = 수용"* → **양수 표본 19,900 수용 · 반올림 0 인 표본 100 거부** (`test_tau_flux` L5 메시지 그대로).

## 7. 남긴 것 · 한정

- RGLR2-02 는 **검출 · 격리**다 — 세대 폴더 + 단일 포인터 (정전 원자성) 는 아니다.  풀이 중에는 그 풀이의 stash 때문에 케이스 화면이 "무효" 로 보인다 · 무효는 성공한 게시 전까지 유지 · 재분석 경로는 거부 사유를 meta 에 적은 뒤 results_dir 를 지운다 (복구 자료 포함).
- 가드 없이 full_metrics 를 직접 읽는 소비자가 남는다: 그룹 비교 · 코퍼스 화면 · `scripts/export_comsol_2d.py` · `scripts/build_tau_regime_db.py` (탐침의 `grade_tau2` 15.07 이 그 예 — 케이스 화면 · 등급 경로는 None).
- 일반 경로는 사본별 기술 검사만 — 사본 사이 일치 (일관된 legacy 단독 변조) 는 정지 계약 ⑥ 만 본다.
- 접촉 단계 재실행 뒤 망 실패 (full_metrics 에 망 id 없음 + 옛 provenance) 는 불일치로 표시하지 않는다.
- `grade_engine` 메시지는 저장된 v2 결과에도 현재 계약 문자열 (v3) 을 적는다 (표시만).
- 인계 τ 의 `f_ion_<m>` (질량보존 두께 재척도) 와 웹앱 COMSOL 2D 내보내기의 `f_ion_<mode>` (판 간격 = 인계 `f_ion_<m>_gap`) 이름이 겹친다 — 열 사전 경고만 · 개명은 1저자 결정.
- 실행기의 케이스별 망 lock = 동시 망 풀이 (지시 "20 갈래") — 기계 전체 OOM 보호는 메모리 예산 관문 (추정 150 MB + 4.5 MB/천 접촉 · 실측/추정 0.88–1.06).

## 8. 질문

1. RGLR2-01 · 02 · 03 이 §6-1 · 2 · 3 을 채우는가?  RGLR2-03 의 K = 2^20 (§3) 을 "승인된 안정식 처리" 로 받는가?
2. §5 의 병렬 배치 (격리 · 코드 지문 대조 · 배포는 GO 뒤) 를 받아들이는가?  실행 등록이 §6-5 의 "승인된 amendment 재봉인" 을 채우는가?
3. 가드 없는 소비자 (§7) 를 194 인계 전에 막아야 하는가, 인계 범위 (인계표 · τ 표) 밖이라 다음으로 미뤄도 되는가?
4. RGL-06 · RGL-08 닫힘 (§4).

## 9. 재현 (Linux · 리포 뿌리)

```bash
python3 webapp/test_pipeline_provenance.py      # 284/284
python3 scripts/test_tau_flux.py                # 55/55
python3 webapp/test_tau_handover_status.py      # 37/37
python3 webapp/test_tau_grade_unify.py          # 20/20
python3 scripts/test_love_weber_stress.py       # 139/139
python3 webapp/test_stress_lw_labels.py         # 72/72
python3 scripts/lhs_stress_constriction_audit.py --selftest   # 14/14
python3 scripts/lhs_design_dataset.py --selftest              # 312/312
python3 webapp/test_network_handover_chain.py                 # 12/12
python3 scripts/run_network_194_parallel.py --selftest
python3 scripts/wsl_network_smoke.py --selftest
# 판정 묶음 탐침 (zip 을 풀고 source/ = git archive 11fcf91e8): source/ 에서
#   python3 <이 리포>/docs/reviews/codex_rglr2_fix_probe_rerun_20261005/network_adversarial_after_fix.py 를 묶음의 probes 폴더에 두고 실행
```
