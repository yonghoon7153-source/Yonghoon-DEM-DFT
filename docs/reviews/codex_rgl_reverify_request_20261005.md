# Codex 재검증 요청 — RGL-01 ~ 10 수정 (r_int 보조 수렴 · LHS ⑤⑥⑦ 인계 · LW 입자 응력 · `stop_after='network'` 망 정지 경로) (2026-10-05)

> **이전 판정** — `docs/reviews/codex_review_rint_g1_lhs_network_20261005.md` (10-05 · **HOLD · 새 P1 4** · 핀 `30c8205c5`) · 증거 `docs/reviews/codex_rint_g1_lhs_network_review_evidence_20261005/`.
> **비준** — 1저자 10-05 *"권고대로 진행해줘 · 오늘까지 접촉 네트워크등은 확실하게 닫아야돼"* (수정 계획 = 판정문 §7 해제 목록 순서 · 반례 먼저 = 실 생산자 사슬 · 봉인 = 저자 승인 amendment · 09-17 cutoff 유지).
> **고정** — 코드 = 이 요청서가 들어간 커밋 (`git log -1 -- docs/reviews/codex_rgl_reverify_request_20261005.md` · 브랜치 `claude/sdcp-dem-manuscript-si-pqwtv8`).  발송 = 1저자.
> **요청 범위** — 판정문 §7 의 1 – 7 이 닫혔는지.  **8 (WSL 소형 통합 · real14 회귀 · 봉인 · 194 건) 은 이 요청에 없다** — 판정문 그대로 194 건 실행 · 새 봉인을 요청하지 않는다 (GO 뒤 1저자 단계 · §6 Q6).

## 1. 패치 (오래된 순)

| 커밋 | 원장 | 내용 | 파일 |
|---|---|---|---|
| `159063be1` | RGL-10 · SELF-87 (일부) | "GOLD 8" = 단언 8 로 정정 · 원시 float.hex 비교 ⑨ (구식 eedada5d3 ↔ 현재 · 18 경우) · C1c 문구 · C1d 유한 전극 반례 (+12.05 %) | `scripts/test_network_boundary_rule.py` · `scripts/test_constriction_power_share.py` |
| `1d9af09d0` | RGL-01 · RGL-09 | wetted · bare 보조 솔브 각각 `run_contract.conv_ok` (주 솔브 · 판정기와 같은 conjunction) · 수렴 3 필드 보존 · 공용 component 계약 · 비유한 잔차 = 미수렴 (σ · 반응 솔브) / Spearman = 평균 동률 순위 · 정의 안 되면 None + 상태 · top 10 % 경계 동률 = None | `scripts/mpm_webapp_payload.py` · `run_contract.py` · `step3_sigma.py` · `rint03_je_compare.py` · `sdcp_gain_verdict.py` · 웹앱 viewer3d · mpm_lab · single · `mpm_lab_register.py` |
| `a8e53b2a0` | RGL-06 | LW 입력 검증 (위치 · 반경 · 부피 · 주기 길이 · mesh 판 높이 · c_strs 전부/전무 · 유한) · 영 척도 = 절대 + 상대 (atol 0) · 비유한 = FAILED · 평균 VM 0 = **UNDEFINED** · 벽 제외 `nowall_status` · 계약 표지 `love_weber_checks_v2` · 이름 한정 (입자 접촉력 기반 대칭 응력의 VM) · 입력 CSV 해시 | `scripts/dem_analysis_core.py` · `analyze_contacts.py` · `generate_comparison_plots.py` · 웹앱 app · single · group |
| `b162009f8` | RGL-03 · RGL-05 | `WA_STAGE_GROUPS['network']` · 관문 순서 = 원천 근거 → 유한 → 형/범위 → 식 · 쌍 · AM–AM 개수 · 총합 · 평균 함께 정규화 (`_wa_area_norm`) · 0 채움은 세 키 모두 빈칸일 때만 · 최종 레코드 재검 · 열 사전 문구 | `scripts/lhs_design_dataset.py` |
| `ef5e8dcfb` | RGL-02 · 04 · 07 · 08 | 비관통 증명 (FULL 풀이 앞 `active_fractions` · 같은 그래프 · 같은 띠) → `valid_zero` + `sigma_full_reason = no_through_path` · 관통인데 못 풂 = `not_computed` + `solve_failed` · 승격 순서 (솔버 → 내용 → 투영 → 채널 → σ₀ 짝 → 정지 계약 → 한 번에 승격 · 실패면 후보 치움 + 옛 세대 되돌림) · 정지 계약 ⑥ 파일 대조 ⑦ τ 입력 · 실 tau_flux ⑧ σ₀ 짝 · `NET_MERGE_KEYS` 에 온도 · σ₀ · 상태 | `scripts/network_conductivity.py` · 웹앱 `app.py` · `pipeline_service.py` · single · 시험 |
| (이 요청서 커밋) | SELF-86 · RGL-05 정의 맞춤 | 끝-끝 사슬 시험 `webapp/test_network_handover_chain.py` (check_all · CI) · 그룹 표 AM–AM 평균 면적 접촉 0 = 빈칸 (인계표와 같은 규칙) · 원장 | `webapp/test_network_handover_chain.py` · `app.py` · `group.html` · `test_closed_param_groupview.py` |

⚠ `scripts/network_conductivity.py` 는 S3 수치 모듈이다 — `ef5e8dcfb` 가 바꿨다 → 봉인은 §7-8 절차 (amendment) 에서 다시.

## 2. 판정문 §7 해제 목록 대응

| §7 | 무엇을 했나 | 우리 시험 (옛 코드 → 새 코드) |
|---|---|---|
| 1 보조 미수렴 | 실물 producer 가 wetted · bare **각각** 수렴을 요구 · 못 채우면 collector `unconverged` · R_geom · jb 미게시 → required 라 exit 3 (게시 안 함 · 진단본 `.failed`) · 공용 component 계약이 보조 수렴 3 필드를 본다 (producer · check_arm · 판정기) | `test_rint_receipts` G 절 (실물 producer · 한 호출만 CG 제한 · r-OFF · r-ON) 63 PASS 29 FAIL → **102/102** · `run_contract` G8–G15 113/124 → 124/124 · 판정기 ㊽ 174/177 → 177/177 |
| 2 실 producer → 정지 → τ | 관통 · 정상 비관통 · 수치 실패 (spsolve 예외 주입) = done · done · failed · τ = OK · NOT_PERCOLATING · NOT_COMPUTED | `test_pipeline_provenance` T13a–i (실 CLI 그대로 · runpy) · **끝-끝 사슬 시험 10/10 (옛 코드 5/8)** |
| 3 network 배치 → build_handover | network 배치 (생산 형식 `write_outputs` → `load_webapp`) 를 ⑤⑥⑦ 로 받는다 · 모르는 묶음 · 정지점 · 역량 밖 = 거부 · 안내 문구 | `lhs_design_dataset` ㉖a–i (실데이터 130/130 · 64/64 = 접촉 판과 같은 표) · 끝-끝 사슬 (실 정지 상태 셋을 실 배치에 얹어 인계 — done 두 행 = 접촉 판 · failed 행 = 빈칸 81 칸 · 거부 없음) |
| 4 실패 시 보존 | 정지 관문 실패 → 옛 네 JSON · full_metrics · active provenance 그대로 · 최근 시도만 failed + 단계 · 첫 실행 실패 = 활성 세대 없음 · 망 JSON 없음 | T14a–g (L9 변이) · T13i · 끝-끝 사슬 ① |
| 5 G4 · LW 반례 | G4 비유한 · 범위 · 필수 근거 · 부분 null 변이 19 종 거부 · LW 원자 기하 · plate · 영 분모 반례 · 194 행 요약표 산술 유지 (replay = 판정문 §4 표와 같다 · 커밋된 인계표 재생성 바이트 동일 — 수정 에이전트 보고) | ㉗ 34 건 · 241/277 → **277/277** · `test_love_weber_stress` R0–R12 47/76 → **76/76** · `test_stress_lw_labels` 34/48 → 48/48 |
| 6 τ 입력 · 짝 | 정지 계약 ⑦ τ 입력 5 키 · 장부 4 키 · 실 `tau_flux.ion_columns` 상태 · ⑥ per-mode ↔ dual ↔ legacy 전 레코드 · full_metrics 망 소유 키 = 이번 세대 투영 · ⑧ σ₀ · 온도 짝 (두 모드 · legacy · full_metrics) · 깨끗한 신규 ↔ 옛 온도 retry 를 갈라 시험 | T15a–d · T16a (Codex 수치) · **T16b 실 `/retry-network`: 옛 σ₀ 12 · τ 6.6286 (2 배) → 3 · 3.3143 (깨끗한 입력과 같다)** · T16c |
| 7 순위 · 문구 | Spearman 평균 동률 순위 · 정의 안 되면 None · RINT-03 세 값 (0.270 · 0.954 · 14 % · 91 %) = **잠정** (입자 벡터 미보존 → 재계산 불가 · `docs/data/rint03_je_20261005/README.md`) · "GOLD 8 침대" · "전극 영향 없음" 정정 | `rint03_je_compare` T7–T11 9/14 → 14/14 (scipy 오라클) · 경계 ⑨ · C1c · C1d |

## 3. 판정문 탐침 재실행 — 우리 트리 (Linux · Python 3.11.15)

방법 — 받은 zip 의 탐침 7 개를 **무변경**으로 두고 `source/` 만 이 커밋의 같은 경로 파일로 바꿨다.  탐침 안의 `assert` (옛 결함을 전제로 한 단언) 는 결과를 기록하도록만 바꿨다 (실행 흐름 동일).
같은 도구로 핀 `30c8205c5` 를 먼저 돌려 받은 증거와 같은 값 (단언 41 개 전부 성립 · 실행 시각 · 임시 이름 말고 차이 0) 임을 확인한 뒤 수정 트리를 돌렸다.

| 원장 | 탐침 | 핀 `30c8205c5` | 수정 트리 |
|---|---|---|---|
| RGL-01 | probe_adversarial | wetted · bare 미수렴 = rc 0 · 게시 · R_geom 3.8 / 0.0 · check-arm 0 | **rc 3 · 미게시** (STEP3_REQUIRED_INCOMPLETE `collector_geom(unconverged)`) · 정상 = rc 0 · R_geom 0.0 · check-arm 0 그대로 |
| RGL-01 | 〃 비유한 잔차 | 경고 없음 · unconverged False | 경고 · unconverged True |
| RGL-09 | 〃 Spearman | [1,1,2]↔[1,2,2] = 1.0 · 전부 0 = 0.9999999999999999 | (0.5, ok) · (None, constant_input) |
| RGL-02 | probe_actual_zero | 생산자 not_computed · 정지 failed · τ NOT_PERCOLATING · f 0 | 생산자 **valid_zero** · 정지 **done** · τ NOT_PERCOLATING · f 0 |
| RGL-04 · 08 | probe_contracts | missing_tau_inputs · permode_vs_dual_disagree · percolating_power_missing = done · L9 = failed · 옛 세대 생존 4/4 False | 넷 다 **failed · 옛 세대 생존 True** · healthy = done 그대로 |
| RGL-07 | 〃 stale_temperature_factor4 | σ₀ 12.0 · τ 4.898979485566356 | **σ₀ 3.0 · τ 2.449489742783178** (= healthy) |
| RGL-03 | probe_g4 | network_stage_contact_groups 거부 | **수용** |
| RGL-05 | 〃 | 결함 변이 19 종 수용 | **19 종 거부** · 의도된 수용 (0 쌍 세 키 빈칸 · 명시 0 평균 0 · 반폭 경계 0.004999 / 0.005 · 4.999e-5 / 5e-5 · 미검토 제외 · 기준선 둘) 그대로 · 0.005001 · 5.001e-5 거부 그대로 |
| RGL-06 | probe_lw_independent | 반경 NaN = OK · CV 0 · F=0 ∧ Fn+Ft ≠ 0 = OK · F=0 ∧ c_strs=0 = FAILED (virial inf) · plate NaN = OK | FAILED (invalid_input: bad_radius · c_strs 부분 결측) · FAILED (force_columns 영 척도) · **UNDEFINED (zero_load)** · FAILED (invalid_input) · 맞바꾼 접촉력 = OK 그대로 (`virial_scope` = 프레임 대응 증명 아님) |
| RGL-10 · Q4 | probe_network_independent | 구 · 신 18 비교 원시 hex True | 같다 (18 True) · 비관통 단언 (`not_computed`) 만 성립 안 함 = RGL-02 수정 |

탐침 쪽 주의 (우리 코드 결함 아님):
- `probe_adversarial` 는 payload 를 `evidence_g1/<mode>.json` 에 쓰고 `p.exists()` 로 게시를 판정한다 → zip 에 든 옛 payload 가 남아 있으면 rc 3 인데도 "게시" 로 읽힌다.  우리 재실행은 실행 전에 그 네 파일을 지웠다.
- `probe_lw_independent.invalid_atom_geometry()` 는 반환에서 `r['arrays_vm']` 을 읽는다 — 이제 FAILED 라 배열이 없어 KeyError (위 표의 값은 같은 입력의 `run()` 결과).
- `replay_g4.py` 는 지운 사설 함수 `_wa_area_prep(case, row, rep)` 를 부른다 → `_wa_area_norm(case, wr, rn, rep)` (rn = `_wa_raw_phase_n(phase_counts, 설계 상 (mono) | None, 웹앱 반지름 이름)`).  인계 생성기 본 경로 (`build_handover`) 가 같은 순서로 부른다.

## 4. 스키마 · 소비자 변화 (요지)

- 망 JSON — 새 키 `sigma_full_reason` · `sigma_bulk_net_reason` · `sigma_constr_net_reason` · 비관통 상태 `not_computed` → `valid_zero` · 이온 채널 `valid_null` → `valid_zero` (비관통일 때) · 전력 몫 사유 문자열 하나 추가 (`not_computed (FULL solve failed on a percolating network)`).  관통 침대 σ 는 비트 동일 (GOLD · 무작위 3 상 6 침대 · 원시 hex 18).
- `full_metrics` — 망 세대가 새 키 6 개 소유 (온도 · σ₀ · 상태 · 사유) · `network_attempt.json` 에 `stage` · `network_stop_verdict(…, fm=)` (기존 호출 호환).
- collector — `step3.collector_geometric` 에 보조 수렴 6 키 · 상태 어휘 `unconverged` · 옛 schema 3 payload 중 collector 를 계획했는데 수렴 필드가 없는 것 = 거부 (커밋된 `docs/data` 매니페스트 전수 = 해당 없음 · LEAN 런은 `--no-collector`).
- LW — 상태 어휘 UNDEFINED 추가 · `nowall_status` · `contract = love_weber_checks_v2` · 영 척도 상대 차 = None (inf 안 씀) · `full_metrics` 에 계약 · 검사 · 입력 해시 키.  옛 결과 (계약 표지 없음) 는 웹앱에서 "입력 검증 전 세대" 로 표지.
- 인계 생성기 — 값 · 열 순서 그대로 (열 사전 문구만) · AM–AM 접촉 0 의 평균 = 빈칸 (웹앱 그룹 표도 같은 규칙).

## 5. 남긴 것 · 한정 (원장)

- `WEB-03` (P2 · open) — 일반 경로 (Stage E 까지) 의 채널 판정은 "관통인데 풀지 못한" 이온 (not_computed · solve_failed) 을 여전히 통과시킨다 (정지 계약 · τ 인계만 거부) · 전자 · 열 채널은 같은 경우에도 valid_null · 실패 처리 두 갈래 · 크래시 창 (§6 Q1 · Q2).
- `LHS-33` (P2 · open) — 옛 σ_VM 열 (`stress_cv`) 의 무효 입력이 0 → 등급 축 "기계적 안정성" (낮을수록 좋음) 거짓 최고 등급.  LHS-29 결정 (옛 열 값 · 키 불변) 때문에 이번에 손대지 않았다 (§6 Q7 · 1저자 결정).
- LW — TIMESTEP 미기록 (파서가 버린다 · 원자 · 접촉 덤프는 `find_last_file` 로 따로 고른다 → 같은 프레임인지 미확인) · 입자별 c_strs 대조는 관문 불가 (real_14 에서 접촉 덤프로 다시 만든 50/50 virial 도 입자별 상대 잔차 중앙 2.6e-4 · p99 0.61 · 최대 17.8 — 전역 합 5.0e-5 · 원인 미확인) · UNDEFINED (zero_mean_vm) 분기 미시험 (이 기하로 침대를 못 만든다).
- 관통 분율을 소수 4 자리로 반올림해 아주 작은 관통은 정지 계약에서 실패한다 (실패로 닫히는 쪽) · 질량 보존 장부 · `percolation_pct` 없는 케이스는 network 정지 실패 (의도).
- 망 단계 고유 산출 (tau2 · f · ④a 전력 몫 · electronic_active_fraction) 은 아직 인계 묶음이 아니다.
- 실 덤프 · WSL 런 · real14 회귀는 하지 않았다 (§7-8 = GO 뒤).

## 6. 질문

- **Q1 (WEB-03)** — 일반 경로 채널 판정도 관통-풀이실패 이온을 거부해야 하나?  지금은 정지 계약과 τ 인계만 거부하고 케이스 화면은 "미계산 — 관통인데 풀지 못함 (solve_failed)" 으로 보인다.
- **Q2** — 실패 처리 두 갈래 (솔버 단계 실패 = 옛 RR2-01 / P1c 대로 full_metrics 에 failed 표지 · 후보 거부 = full_metrics 바이트 그대로) 를 하나로 맞춰야 하나?
- **Q3** — 전력 몫 생산자 사유 `'not_computed (zero or non-finite dissipation)'` 은 0 과 수치 실패를 한 문자열에 묶는다 → 정지 계약은 등록하지 않고 거부한다 (관통 σ > 0 에서 ΣI²R = 0 은 불가).  생산자 문자열을 갈라 등록할 이유가 있나?
- **Q4 (RGL-01)** — collector 를 계획했는데 보조 수렴 필드가 없는 옛 schema 3 payload 를 거부하는 것 (판정문이 요구한 쪽) 에 동의하나?
- **Q5 (RGL-06)** — 전역 virial 합 (부호 · 척도) 만 관문으로 두고 입자별 대조는 관문에서 빼는 것이 충분한가?  TIMESTEP · 프레임 대응은 파서 변경이 필요하다 — 이번 범위 밖으로 둬도 되나?
- **Q6 (§7-8 순서)** — GO 뒤: WSL 작은 양성 · 음성 통합 (관통 · 비관통 · 실패 · collector 계획/미계획) + real14 fixture 회귀 → 저자 승인 amendment 봉인 (09-17 cutoff · frozen inventory 그대로) → 194 건 network 배치 → tau_flux 관문 → 인계 v1.2.  이 순서에 동의하나?
- **Q7 (LHS-33)** — 옛 σ_VM 열에서 무효 입력만 빈칸으로 바꾸는 것 (정상 값 불변) 이 LHS-29 의 "옛 열 값 · 키 불변" 과 충돌하지 않는다고 보나?

## 7. 재현 (Linux · 리포 뿌리)

```bash
bash scripts/check_all.sh                                   # 리포 전체 (아래 시험 전부 포함)
python3 webapp/test_network_handover_chain.py               # 끝-끝 사슬 10/10
python3 webapp/test_pipeline_provenance.py                  # T12–T16 · 250/250
python3 scripts/test_tau_flux.py                            # 37/37
python3 webapp/test_tau_handover_status.py                  # 27/27
python3 scripts/network_conductivity.py --selftest          # 30/30
python3 scripts/test_rint_receipts.py                       # 102/102
python3 scripts/run_contract.py --selftest                  # 124/124
python3 scripts/rint03_je_compare.py --selftest             # 14/14
python3 scripts/test_love_weber_stress.py                   # 76/76
python3 scripts/lhs_design_dataset.py --selftest            # 277/277
python3 scripts/test_network_boundary_rule.py               # 9/9
python3 scripts/test_constriction_power_share.py            # 17/17
```

탐침 재실행 — 받은 zip 을 풀고 `source/` 를 이 커밋의 같은 경로 파일 (+ `scripts/*.py` · `webapp/*.py` · `webapp/*.json`) 로 바꾼 뒤 판정문 §5 의 명령 그대로 (`evidence_g1/{normal,wetted_unconverged,bare_unconverged,main_unconverged}.json` 은 먼저 지운다 · 위 §3 주의).
