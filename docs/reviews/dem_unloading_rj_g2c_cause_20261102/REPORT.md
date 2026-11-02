# RJ 323957 · G2c 복원 불일치 — 원인 읽기 전용 확인 (2026-11-02)

**출처:** 본문 = 언로딩 원인 확인 서브에이전트의 반환문 그대로 (11-02 · 하네스가 서브에이전트의 보고 .md 쓰기를 막아 메인이 이 파일로 저장 · 고친 것 = 이 줄뿐). 같은 폴더의 도구 · 증거 4 파일 (`paste-cause-check.sh` · `rj_g2c_cause_check.py` · `selftest_synthetic.py` · `selftest_output.txt`) = 본 가지 `a4227aa68` (`cherry-pick -x` · 부모 쪽 기준 = stoic 끝 `21629b4a0`). 커밋 전 사전 점검 `check_doc_refs` · `check_review_findings` · `check_method_discipline` = rc 0 (에이전트 · 전체 게이트는 메인).

- 요청: 1저자 11-02 — *"RJ 복원 불일치 원인을 읽기 전용으로 먼저 확인 (재시작 파일에 접선력 이력이 남는지) → 그 결과로 v2 시험 설계 → Codex"*.
- 읽은 것: RJ 기록 (`docs/reviews/codex_p1_g2c_diagnosis_20261027/` 판정 · manifest · 10-27 실제 두 덤프 성분 분해) · 키트 (`docs/data/ps45_unload_20261009/` 덱 · `ul_gates.py` · 러너 · 이력 시험) · r8 원 덱과 로그 (`docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz` 멤버 · 덱 sha256 `097658aa…` · 로그 `35e28690…`) · 등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` · LIGGGHTS-PUBLIC 공개 소스 `3d5c00f` (스크래치에 복제 · 빌드 · 설치 없음 · `src/compute_pair_gran_local.cpp` sha256 `71c4d3b5…` = 리포 핀 `docs/data/liggghts_add_pair_pin.json`).
- 하지 않은 것: ibb · GPU · LIGGGHTS 실행 · 설치 · 리포 기존 파일 수정 · push. 판정이 아니다. 재실행 · 후속 팔 · 허용폭 변경을 제안하지 않는다 (새 ibb 실행은 등록 · Codex · 1저자 승인 뒤).
- 표지: **확인됨** = 소스 · 덱 · 기록 줄로 직접 확인 · **추정** = 그 위의 추론 (실제 두 덤프로 대조 전) · **미확인** = 자료 없음.

## 0. 결론

| # | 결론 | 표지 |
|---|---|---|
| 1 | **재시작 파일에 접선 이력은 남아 있다 (지워지지 않았다).** 다만 S0 파일 `restart_compress_3200000.bin` 은 r8 런의 **주기 `restart 50000` 출력**이고, 이 소스에서 주기 restart 의 쌍 접촉 이력은 **그 step 의 힘 계산 전 (pre_exchange) 사본**이다. 원 덤프 `contact_3200000` 은 **그 step 의 이력 갱신 뒤** 다시 계산한 값이다 ⇒ RJ setup 의 접선 힘은 원 덤프보다 **한 step 증분 (kt·vtr·dt) 늦은 이력**으로 계산된다 | 기전 = 확인됨 (소스 · 덱) · 이것이 접선 불일치 96.85 % 를 설명한다는 것 = 추정 (§3 검사로 확정) |
| 2 | 법선력 3,295 쌍의 작은 차이는 다른 기전 후보: 원 런의 in-run 출력은 **유령 원자 (다른 랭크 · 주기 상) 의 속도 · 각속도를 반 step 값**으로 쓴다 → 원 24 랭크 (6×4) 분할에서 경계를 넘는 쌍의 감쇠 항만 다르다. RJ setup 은 모든 원자가 같은 시점 속도 | 기전 = 확인됨 (소스) · 3,295 쌍이 그 쌍이라는 것 = 추정 |
| 3 | 따라서 등록된 G2c 기대 ("이력이 이어지면 글자 같음 · 1e-5") 는 이 바이너리의 주기 restart 파일로는 **원리상 성립할 수 없다** — VALUE_MISMATCH 는 복원 결함의 증거라기보다 시험 전제의 오류일 가능성이 크다 | 추정 (1 · 2 가 §3 에서 확인되면 강함) |
| 4 | 나머지 네 침대 S0 도 `restart_*.bin` → 지금 G2c 로 RJ 를 돌리면 같은 실패가 예상된다. 중력 팔 G2c (C12) 도 in-run 덤프 ↔ setup 덤프 비교라 2 번 기전에 걸린다 | 7:3 = 확인됨 · r6 세 침대 · 10:0 (r2) = 미확인 (덱이 리포에 없다) · C12 결과 = 추정 |

## 1. 이미 있는 숫자 (리포 기록)

| 항목 | 값 | 출처 | 표지 |
|---|---|---|---|
| 위치 · 겹침 · 면적 · 접점 | 다른 쌍 0 / 562,605 | `docs/reviews/codex_p1_g2c_diagnosis_20261027/real_run_20261027/diagnostic_output.json` | 확인됨 |
| 법선력 c_cpl[13–15] | 3,295 쌍 (0.59 %) · 최대 \|Δ\| 1.2e-4 | 같음 | 확인됨 |
| 접선력 c_cpl[16–18] | 544,890 쌍 (96.85 %) · 최대 \|Δ\| 0.0165–0.0236 | 같음 | 확인됨 |
| 예시 3 쌍 (8–5895 · 8–18352 · 8–21165) | \|ΔFt\|/\|Ft\| = 1.16e-4 · 9.9e-5 · 1.27e-4 · ΔF_합력 = ΔFt (출력 6 자리 안) → ΔFn ≈ 0 · cos(ΔFt, Ft) = −0.94 · +0.98 · +0.89 | 같은 파일 examples 로 계산 | 확인됨 (예시 3 쌍뿐 · 표본 아님) |
| 0 · 부호 | 0 인 힘 값 0 · 0 아닌 값 부호 뒤집힘 = 접선 277–337 · 법선 1 (열마다 · 전 쌍 통계) | 같음 | 확인됨 |
| 방향 | 원 reversed 131,854 · 시험 109,001 · 바뀜 22,853 = 정확히 둘의 차 ⇒ 시험 reversed ⊂ 원 reversed | 같음 (산술) | 확인됨 (산술) · 해석 = §2 H2 |
| G1 · G2 · G3 | setup KE 상대 0 · 원자 0 / 160,417 (id type x y z radius vx vy vz 글자) · S0+1,000 판 압력 0.16543146 (시험) vs 0.16542994 (원) = 상대 9.19e-6 | `restore_verdict.user-relayed.json` · `ul_gates.py` 272–287 | 확인됨 |
| S0 의 자리 | r8 PHASE 4 `run 100000` (3,125,000 → 3,225,000) 의 **중간** step · KE 1.34e-6 · 판 압력 0.309 → 0.166 (이완 중 −46 %) · 24 procs `6 by 4 by 1` · 이 run 의 이웃 목록 재구성 20 회 | r8 로그 29 · 3042 · 3117 · 3143 · 3161 행 | 확인됨 |
| S0 파일의 출처 | r8 덱에 `write_restart` 명령 없음 · `restart 50000 …/restart_compress_*.bin` (132 행) · PHASE 4 접촉 덤프 `dump … local 10000` (146–150 행) · r8 자신도 `restart_compress_2650000.bin` 에서 시작 (46 행) | r8 덱 | 확인됨 |

## 2. 가설 순위 (Q1)

### 2-1. H1 기전 사슬 (공개 3d5c00f `src/` 줄)

| 순서 | 원 런 S0 step (3,200,000) 안에서 | 근거 |
|---|---|---|
| ① | step 증가 · `initial_integrate` → x(n), v(n−½) | verlet.cpp:283 · 293 |
| ② | restart 를 쓰는 step 이면 이웃 목록 재구성 강제 | neighbor.cpp:1359–1361 (`output->restart_requested`) · r8 덱 132 행 |
| ③ | `pre_exchange` — 이웃 목록 이력 → 원자별 배열로 복사 (= H(n−1), 이 step 갱신 전) | verlet.cpp:307 · fix_contact_history.cpp:305–424 (setmask 196–201) |
| ④ | 이웃 목록 다시 만들 때 원자별 배열 값을 이웃 목록 저장소로 **복사** | verlet.cpp:328 · neigh_gran.cpp:158–163 |
| ⑤ | 쌍 힘 계산 — **이웃 목록 쪽 이력만** shear += vtr·dt → H(n) | verlet.cpp:343 · pair_gran.cpp:665–667 · pair_gran_base.h:320 · tangential_model_history.h:143–159 |
| ⑥ | `final_integrate` (v(n)) → 출력: **덤프 먼저** (c_cpl = 이웃 목록 이력 H(n) 로 다시 계산 · 갱신 없음) → **restart** (원자별 배열 H(n−1) 를 씀 · 동기화 호출 없음) | verlet.cpp:373 · 381 · output.cpp:335–376 · compute_pair_gran_local.cpp:321 · pair_gran.cpp:676–708 · pair_gran_base.h:446–447 · fix_contact_history.cpp:588–603 · write_restart.cpp:194–199 (동기화 `setup_pre_exchange` 는 `write_restart` **명령** 경로만 · 178 행) |
| ⑦ | RJ: `read_restart` → `run 0` setup (이력 갱신 꺼짐 · 새 pair 라 `setup_pre_exchange` 가 덮어쓰지 않음) → c_cpl = H(n−1) · v(n) | in.R.liggghts 27 · 86–96 · pair_gran.cpp:113 · 667 · fix_contact_history.cpp:290–297 · verlet.cpp:142–196 |

- 쌍 이력 배열 = [deltaMax, shear x · y · z] (dnum 4) — 한 배열로 함께 저장 · 복원 (contact_models.h:153–157 · normal_model_hooke_hysteresis.h:70 · tangential_model_history.h:78–80 · cdt 구름 마찰은 이력 없음) — 확인됨.
- H1 예측: 고착 (sticking) 쌍 ΔFt(시험 − 원) = kt·dt·vtr (접선 열 · 투영 뒤 정확) · 법선 열 ≈ 0 (늦은 shear 가 새 법선 쪽으로 새는 몫 kt·shear·Δe 뿐 · 보통 1e-8 N 대) · 미끄럼 쌍은 \|Ft\| = μ\|Fn\| 같고 방향만 조금 · deltaMax 를 올리는 갱신은 조건 없이 돌고 (normal_model_hooke_hysteresis.h:156–158) 응집 쪽 내림만 조건부 (176–177 · 191–192) → 법선 힘은 같게 나온다 — 식 = 확인됨 · 이 런 수치 = 추정.
- 벽 이력은 해당 없음: 메시 벽 = 현재 자료를 가리키는 원자별 저장 (fix_contact_history_mesh.cpp:272–294 · fix_contact_history_mesh_I.h:115–122) · 바닥 벽 = property/atom (fix_wall_gran.cpp:506–519) — 확인됨 (소스) · mesh md5 PASS · G3 9.19e-6 와 정합 — 추정.

크기 (추정 · 덱 재료값과 r8 덱 주석 밀도로 계산 — §3 검사는 덤프의 실제 반지름 · 질량을 쓴다):

| 쌍 | kt·dt [N·s/m] | γt = γn [kg/s] | γt/(kt·dt) |
|---|---|---|---|
| SE–SE | 1.39e-4 | 6.1e-3 | 44 |
| AM_P–SE · AM_S–SE | 3.5e-4 · 3.3e-4 | 1.4e-2 · 1.3e-2 | 39–40 |
| AM–AM (S–S · P–S · P–P) | 0.026 · 0.034 · 0.060 | 1.04 · 1.61 · 5.28 | 40–89 |

- 식: kt = kn = 16/15·√R*·Y*·(15·m*·v_c²/(16·√R*·Y*))^0.2 · γ = √(4·m*·kn/(1+(π/ln e)²)) · Y* = 1/((1−νi²)/Yi + (1−νj²)/Yj) · e 0.3 · v_c 2.0 · 접선 감쇠 기본 켬 (normal_model_hooke_hysteresis.h:139–142 · normal_model_hooke.h:98 · global_properties.cpp:432 · 516) — 확인됨.
- SE–SE 쌍 (\|Ft\| 성분이 열 중앙값 ≈ 3.1e-3 이하) 은 \|vtr\| 성분 ≳ 2.2e-4 m/s 면 G2c 허용을 넘는다. S0 KE 1.34e-6 J 를 입자 수로 나누면 SE 크기 v_rms ≈ 4e-3 m/s (회전은 thermo 에 없음) → 거의 모든 쌍이 넘는다 = 96.85 % 와 정합 — 추정. 예시 쌍 크기 (\|ΔFt\| 2.3–5.7e-6) 는 AM_P–SE 라면 vtr 7–16 mm/s — 추정 (원자 8 의 형식 = 미확인 · id 가 랭크별로 매겨져 id 로 형식을 알 수 없다).

### 2-2. 가설 표

| 순위 | 가설 | 찬성 | 반대 | 판별 (§3 검사 항목) | 표지 |
|---|---|---|---|---|---|
| 1 | **H1** 주기 restart 의 쌍 이력이 한 step 증분 늦다 (= "덤프와 체크포인트가 다른 sub-step" 의 정확한 꼴) | §2-1 사슬 · S0 = 주기 restart · 기하 0 차 · 법선 99.4 % 같음 (H1 예측과 정합) · 예시 ΔF_합력 = ΔFt · 상대차 1e-4 · 크기가 kt·dt·vtr 와 정합 | 아직 쌍별 속도로 대조 안 함 | B1: 원 분할 내부 (local) 고착 쌍에서 ΔFt vs kt·dt·vtr(n) 기울기 ≈ 1 · R² ≈ 1 · 예측 실패 ≈ 관측 실패 | 기전 확인됨 · 이 런 = 추정 |
| 2 | **H2** 원 in-run 출력의 유령 원자 v · ω 가 반 step (부분 · 법선 3,295 쌍 후보) | 통신은 힘 계산 전만 (verlet.cpp:299–330) · final_integrate 뒤 통신 없음 (373–381 · nve/sphere · viscous · gravity 에 forward_comm 0 건) · c_cpl 이 atom->v · omega 사용 (pair_gran_base.h:349–350 · 403–404) · 유령 쌍은 tag_i > tag_j 쪽만 기록 (compute_pair_gran_local.cpp:428) → 시험 reversed ⊂ 원 reversed 와 정합 (RJ 6 랭크 3×2 경계 ⊂ 원 6×4 경계) · AM 쌍은 γ 가 커 법선 감쇠에 민감 | 3,295 쌍이 원 유령 쌍인지 모름 | A1: 법선 실패 ⊂ 원 6×4 유령 쌍 (격자 재구성 검증 = "원 유령 쌍인데 reversed 아님" 0) · 형식 쌍 교차표 · B2: 법선 차 ≈ −γn·(½dt·f/m)·e 부호 일치 · 기울기 ≈ 1 | 기전 확인됨 · 이 런 = 추정 |
| 3 | 미끄럼 ↔ 고착 갈래 전환이 일부 쌍 (최대 \|Δ\| 0.02) 을 키움 — 독립 원인 아님 (1 · 2 의 결과) | 감쇠 −γt·vtr 는 고착 갈래에만 더해진다 (tangential_model_history.h:174–217) · AM 쌍 γt·vtr 가 0.02 N 대 가능 | — | 전환 쌍의 \|ΔFt\|/(γt\|vtr\|) ≈ 1 · 상위 20 쌍 | 추정 |
| — | 이력 0 초기화 · 소실 | — | 예시 상대차 1e-4 (소실이면 ≈ 1) · 0 아닌 값 부호 뒤집힘 열마다 0.05 % (전 쌍) · RJ reset 로그 contacthistory 있음 · G3 9.2e-6. ⚠ 법선 일치는 넓은 증거가 아니다 — SE 쌍 대부분은 큰 겹침 갈래 (SE–SE δmaxLim = 0.0125·R* ≈ 3e-6 ≪ δ 중앙값 5e-5) 라 법선 힘이 deltaMax 와 무관하다 (AM–AM 만 민감) | reset_like ≈ 0 · rel_dFt_over_Ft 분위 · B1 기울기 | 기각에 가까움 (추정 · §3 으로 확정) |
| — | 방향 바뀐 22,853 쌍의 이력 부호 오류 | — | 복원 = 상대 tag 로 찾고 shear 만 부호 반전 (fix_contact_history.cpp:403–411 · neigh_gran.cpp:158–163) · 부호 오류면 접선 부호 뒤집힘 ≈ 22,853 인데 277–337 | sign_flip_like · 방향 바뀐 쌍 교차표 | 기각에 가까움 (확인됨 + 추정) |
| — | 부동소수 · 직렬화 정밀도 | — | restart = double (atom_vec_sphere.cpp:939–) · 기하 열 0 차 · G1 KE 0 | — | 기각 (확인됨) |
| — | 이웃 목록 · 분할 차이 자체 | — | 쌍 집합 같음 (빠짐 · 추가 0) · 쌍 힘은 그 쌍의 x · v · ω · 이력만 씀 → 분할은 방향 · 유령 여부 (H2) 로만 들어온다 | — | 직접 원인 아님 (확인됨) |

## 3. 읽기 전용 검사 (ibb 붙여 넣기)

### 3-1. 무엇을 하나
- 파일: `paste-cause-check.sh` (sha256 `67b2da8af47e…a9177`) — `rj_g2c_cause_check.py` (sha256 `beb457f95e4e…bd09`) 를 글자 그대로 담는다 · 출력 `check_sha256` 이 이 값과 같아야 한다.
- 읽는 것: `$UL_ROOT/ps_7_3_r45/in/contact_3200000.liggghts` (원) · `…/RJ/R/g2/contact_3200000.liggghts` (시험) · `…/RJ/R/obs/post_atom_3200000.dump` (R 덱 94–95 행 · `run 0` setup 의 x · v · ω · f · 질량 · 반지름 %.17g · 리포에 sha 기록 없음 → 출력에 새로 기록 · 없으면 A 만 하고 B = NOT_RUN) · `…/RJ/R/screen.txt` (격자 줄 · 정보용).
- 묶기: 원 · 시험 크기 · sha256 (`53ae293b…` · `193e6e6c…`) · 562,605 쌍 · 관문과 같은 식 불일치 545,583 쌍이 아니면 분해를 숨기고 `BINDING_MISMATCH` (rc 2).
- 하지 않는 것: 파일 쓰기 · 복사 · 전송 · 설치 · fetch · sbatch · LIGGGHTS/MPI · 기존 판정 · 허용폭 · 원본 변경. 출력 = 화면 JSON 하나.
- 시간 · 메모리: 1–2 분 · 수백 MB (추정 — 합성 10 만 쌍 14 초 · 최대 RSS 493 MB (생성기 포함)). Python 3.8.20 · 3.11 같은 결과.
- 상수 (r8 덱 그대로): Y 1.4e8 · 1.4e8 · 1.35e6 · ν 0.25 · 0.25 · 0.30 · e 0.3 · μ 0.5 · v_c 2.0 · dt 1e-6 · 상자 0.05 × 0.05 · 원 격자 6×4 (r8 로그 29 행). 미끄럼 = \|Ft\|/(μ\|Fn\|) 가 1 ± 1e-4 (고착 갈래는 감쇠가 friction 판정 뒤에 더해져 1 을 넘을 수 있다).

### 3-2. 출력 읽는 법

| 출력 항목 | H1 이면 | H2 이면 | 이력 소실이면 | 부호 오류면 |
|---|---|---|---|---|
| `M1_fit.local_stick` 기울기 · `r2_unit_slope` · 10 % 안 비율 | ≈ 1 · ≈ 1 · 높음 | (local 영향 없음) | 0 근처 · 음수 | local 정상 · ghost 쪽 (방향 바뀐 쌍) 만 깨짐 |
| `tables.m1_predicted_fail_x_observed_tangent_fail` | 대부분 대각 | — | 대각 아님 | — |
| `tables.ghost_orig_x_fail_normal_tangent_total` · `pairtype_x_ghost_x_normal_fail` | 접선 실패율 local ≈ ghost | 법선 실패가 ghost (특히 AM 쌍) 에 몰림 · local 법선 실패 ≈ 0 | 둘 다 거의 전부 | — |
| `M2_normal.ghost` 부호 일치 · 기울기 | — | ≈ 1 · ≈ 1 | — | — |
| `orig_ghost_pairs_not_reversed` | 0 이어야 격자 재구성이 맞다 (아니면 H2 해석 보류) | 0 | — | — |
| `reset_like_pairs` · `sign_flip_like_pairs` | ≈ 0 · ≈ 0 | ≈ 0 | 대부분 | 방향 바뀐 쌍 수 근처 |
| `rel_dFt_over_Ft` 분위 | 1e-5–1e-3 대 | — | ≈ 1 | ≈ 2 |
| `test_grid_violations` · `rj_screen_processor_grid` | RJ 격자 (정보 · 3×2 예상) | — | — | — |

- 7:3 에서는 결과를 보는 **사후 진단**이다 — §4 의 등록 판정 자료로 쓰지 않는다.

### 3-3. 합성 자료로 먼저 확인 (이 컨테이너 · `selftest_synthetic.py` → `selftest_output.txt`)

6,000 쌍 가짜 덤프 (원 · 시험 = LIGGGHTS %g 26 열 · 원자 = %.17g) 에 기전을 넣고 같은 `analyze` 로 읽었다.

| 넣은 것 | local 고착 기울기 · R² | M2 ghost 부호 · 기울기 | reset_like · sign_flip_like | 격자 |
|---|---|---|---|---|
| H1 + H2 | 1.0001 · 1.0 (n 4,291 · 10 % 안 98 %) | 1.0 · 1.0006 | 2 · 0 | 원 유령 not-reversed 0 · 3×2 위반 0 (다른 후보 245–371) |
| 차이 없음 | n 0 | n 0 | 0 · 0 | 같음 |
| 이력 0 초기화 | −2.06 · −0.0001 | n 0 | 5,736 · 0 | 같음 |
| 방향 바뀐 쌍 부호 오류 | local 1.0001 · 1.0 · ghost R² 0.0003 | n 0 | 350 · 235 | 같음 |
| H2 만 | local n 0 | 1.0 · 1.0006 | 0 · 0 | 같음 |

- 한계: 합성 기하는 실제 침대가 아니다 (쌍마다 원자 둘) — 도구의 산술 · 판별력 확인일 뿐.

### 3-4. 붙여 넣기
```bash
# ibb 로그인 노드 · 아무 폴더 (파일을 쓰지 않는다)
# 리포 docs/reviews/dem_unloading_rj_g2c_cause_20261102/paste-cause-check.sh 의 내용 전체를 그대로 붙여 넣는다.
# 맨 위 두 줄 기본값이 10-27 진단 때와 다르면 두 변수만 바꾼다:
#   PY="${PY:-$HOME/.conda/envs/myenv/bin/python3}"      (10-27 paste-diagnostic.sh 와 같은 Python)
#   UL_ROOT="${UL_ROOT:-$HOME/ps45_unload_20261009}"     (ps_7_3_r45/ 를 담은 작업 루트)
# 끝 줄 "rc=0" = 분해 완료 · "rc=2" = 거부/미완료 — 어느 쪽이든 출력 JSON 전체를 그대로 전달.
```

## 4. v2 복원 시험 설계 초안 (Q2 · 설계만 — 등록 · Codex 는 뒤)

**목적을 둘로 나눈다** — A. 복원 경로 무결성 (판정 · 엄격) · B. 원 런과의 연속성 (보고 · 또는 결과 전 등록한 기준). 지금 G2c 는 A 를 보려고 B 의 자료 (원 in-run 덤프) 를 썼고, B 에는 H1 · H2 차이가 원리상 들어 있다.

| 단계 | 내용 | 비교 열 · 시점 · 허용 | 통과 / 실패 |
|---|---|---|---|
| T0 의미 fixture (작은 침대 · ibb · 판정 선행 조건) | 움직이는 20–50 입자에서 (a) 주기 `restart N` + 같은 step in-run 쌍 이력 덤프 (`compute pair/gran/local id history` %.17g) → 새 프로세스 setup 덤프 (b) 같은 상태 `write_restart` 명령 → setup 덤프 (c) NP 2 에서 랭크 경계를 걸친 쌍 · 내부 쌍 (주기 경계에서 떨어뜨림) 의 in-run 출력 ↔ setup 출력 | (a) setup 이력 = in-run 이력 − P(vtr(n−½))·dt (b) 글자 같음 (c) 경계 쌍만 감쇠 항 차이 · 내부 쌍 같음 | 등록대로면 소스 판독이 실제 바이너리로 확인 · 아니면 SEMANTICS_UNCONFIRMED → 멈춤 |
| T1 왕복 복원 (주 판정) | S0 → 지금 머리 → `run 0` → setup 덤프 A (c_cpl 26 열 %.17g → `uncompute cpl` → `compute ul_ph … id history` → `run 0` → 쌍 이력 %.17g · 원자 x v ω f 벽 이력) → `write_restart` (명령 · 동기화) → 새 프로세스 (같은 NP 하나 + 다른 NP 하나) → 같은 덤프 B. (pair/gran/local 은 하나만 등록되므로 G0 머리는 그대로 두고 첫 run 뒤에 바꾼다) | 무순서 쌍 키 · 방향 정규화 (위치 교환 · 힘 · 토크 · shear 부호 반전 · deltaMax 그대로) · 같은 NP = **모든 열 글자 같음** · 다른 NP = 이력 · 힘 ulp 수준 (값은 등록 — 원 유령 · 주기 쌍은 두 랭크 사본이 끝자리에서 다를 수 있다) | 통과 = RESTORED (복원 경로) · 실패 = VALUE_MISMATCH (열 · 부류 보고) · 런 실패 = TECH |
| T2 연속성 (보조) | RJ setup 덤프 ↔ 원 `contact_S0` 를 H1 · H2 보정 (§3 과 같은 식) · 짧은 궤적 판 압력 · KE (S0+1,000 … +10,000) 를 같은 S0 다른 NP 쌍둥이의 갈라짐 폭과 비교 | 원 local 고착 쌍 기울기 · R² · reset_like · sign_flip_like · 원 local 법선 ≈ 0 | 7:3 = 사후 보고만 · 나머지 침대 = 판정에 쓰려면 숫자를 결과 전 등록 |
| T3 중력 팔 (C12) 정정 | 출처 팔이 R_M `write_restart` 직후 `run 0` setup 덤프를 남기고 G_ 팔 setup 덤프와 비교 — in-run 창 끝 덤프 (in.U_UB 122–123 행) 는 쓰지 않는다 | T1 과 같은 규칙 (같은 NP = 글자 같음) | 같음 |

- 체크포인트 절차: (1) 기존 S0 파일은 바꿀 수 없다 — "S0 상태 = 파일 상태 (x · v · ω · 벽 이력 = S0 끝 · 쌍 이력 = S0 힘 계산 전)" 로 정의하고 한정어로 적는다 (H(n) 은 파일에서 되살릴 수 없다 · 차이 = 접촉마다 한 증분, \|Ft\| 의 1e-4 대 — 추정) (2) 키트가 새로 만드는 체크포인트는 지금처럼 `write_restart` **명령**만 (팔 덱 294 · 309 · 360 · 365 행 — 동기화 경로 · 확인됨) (3) 정확 비교의 기준 덤프는 setup (`run 0`) 덤프만 (4) 정확 비교 시점 = setup · N step 뒤에는 거시량만.
- 결과 전 등록할 것: T0 기대 (식 포함) · T1 NP 집합 · 정규화 규칙 · 열별 허용 · T2 지위 (보고 / 판정 + 숫자) · 판정표 (RESTORED · SEMANTICS_UNCONFIRMED · VALUE_MISMATCH · TECH) · 적용 침대 · 323957 처리 (VALUE_MISMATCH 기록 유지 · 소급 PASS 없음 · "등록 기대 오류로 설명됨" 은 Codex 확인 뒤 표지로만) · §3 검사 결과는 사후 진단이라는 점.

## 5. 결과와 무관하게 고칠 것 (Q3)

| # | 대상 | 문제 | 제안 | 표지 |
|---|---|---|---|---|
| 1 | `ul_gates.g2c_compare` · REG §3-2 G2c 행 (229 행) · 근거 (233–234 행) | "이어지면 같다 · 지워지면 다르다" 둘만 가정 — 셋째 (이어졌지만 한 증분 늦음 · 출력 의미 차이) 가 빠짐 → 주기 restart S0 에서 성립 불가 | 남은 침대 RJ 전에 v2 (§4) 로 대체 · 근거 문장 정정 | 7:3 = 확인됨 · 나머지 = 추정 |
| 2 | REG C12 중력 팔 G2c (809 행) | in-run 창 끝 덤프 ↔ setup 비교 = H2 차이 (같은 NP 라도 유령 쌍) | 기준을 setup 덤프로 (T3) | 기전 확인됨 · 결과 추정 |
| 3 | 이력 시험 H0–H5 | 소비자가 `write_restart` 명령 파일 (`fixture.bin` · in.hist_producer 167 행 · run_history.sh 132 · 155 행) 만 읽고 마지막 990 step 은 속도 0 (147–148 · 158 행) → 주기 restart 지연을 원리상 못 본다 · `auto_1500` (주기) 은 정보로만 (read_history.py 579–581) | T0 를 양성 대조로 추가 | 확인됨 |
| 4 | REG 237 행 ("G2c 실패면 r3 · r6–r8 이력 보존도 같은 의문 → 원장 후보") | 원 조각들은 주기 restart 로 이어졌다 (r8 덱 46 행) → 경계마다 한 증분 지연이지 소실이 아니다 | 원장 후보 문장을 "조각 경계마다 쌍 이력 한 증분 지연 (크기 kt·vtr·dt)" 으로 | 추정 (§3 확인 뒤) |
| 5 | G2c 비교 원천 = 6 자리 원 형식 덤프 | 정확 · 이력 비교에 해상도 부족 | v2 는 %.17g · 이력 열 직접 | 확인됨 |
| 6 | in-run c_cpl (원 런 · 팔) | 감쇠 항이 유령 쌍에서 분할 의존 (반 step 속도) | 판독기 · 열 사전에 한정어 · 다른 NP 간 · setup ↔ in-run 정확 비교 금지 | 기전 확인됨 · 크기 추정 (1e-5–1e-4) |
| 7 | 10:0 (r2 · `restart_settling_3600000.bin`) · r6 세 침대 S0 | 주기 restart 인지 — 덱이 리포에 없어 확인 못 함 | ibb 에서 각 마지막 조각 덱에 `grep -n "restart" <덱>` 한 줄 (읽기 전용) | 미확인 |
| 8 | 바이너리 수준 | 소스 = 핀 커밋 (파일 sha 같음) 이지만 실행 파일 (`lmp_mpi` sha `ee2d7726…`) 이 이 소스로 빌드됐는지는 가정 (핀 문서 한계) | T0 가 실측 | 미확인 |

- `diagnose_g2c.py` (10-27 도구) 는 고칠 것 없음 — 예시 3 쌍은 시험 파일 순서의 첫 셋이라 표본이 아니다 (도구 자신도 그렇게 적는다).

## 6. 1저자가 정할 것
- [언로딩] Q1 — §3 읽기 전용 검사를 ibb 에서 한 번 돌릴지. 권고: 예 (1–2 분 · 파일 쓰기 없음 · 출력 JSON 전체 전달 → H1 · H2 확정 또는 기각).
- [언로딩] Q2 — 검사가 H1 (· H2) 를 지지하면 v2 (T0 · T1 판정 · T2 보고 · T3 C12) 를 등록 초안으로 써서 Codex 로. 권고: 예 — T0 를 맨 앞에 (소스 판독을 실제 바이너리로 확인).
- [언로딩] Q3 — 그때까지 나머지 네 침대 RJ 와 중력 팔 제출 보류. 권고: 예 (지금 G2c 로는 예측된 실패에 물리 시도를 쓴다).
