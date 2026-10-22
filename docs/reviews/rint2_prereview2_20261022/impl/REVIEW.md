# 사전 리뷰 2 회차 — 구현 쪽 (`impl`) · 검토 판 `93d93bc02` · 2026-10-21

**결론 (한 줄): 고친 뒤 발송 — 새 P1 1 (`PRE2-impl-01` SV 반사실이 "두 섬유 이상이 함께 지나는 SDCP 성분" 다리를 끊지 않고 비 1.0 · `computed` 를 내고, 사슬은 `SV_DEPENDENT` · `SV_UNCHECKED` 둘 다 안 붙인다 — 실제 payload 끝-끝 재현: 같은 침대 대조 비 85.42 · `SV_DEPENDENT` ↔ 두 섬유 꼴 1.0 · 표지 없음) · 새 P3 3 (SV 기록 검증기 · 계획 읽기 큰 정수 · 중복 칸 · SV 반사실 시험 틈).  1 회차 impl 결함 9 건은 원 반례에서 전부 닫힘 (05 = 한계 기록).**

- 기준: 격리 작업 트리 `git reset --hard 93d93bc02` (fetch 안 함) · 기반 `a76f59d0d` 는 `git archive` 사본으로만 · 리포에 쓰지 않음 (변이는 내 작업 트리에서 바꾸고 원본 바이트로 되돌림 · sha256 대조 · 봉인 32 파일 아님).
- 환경: Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · OpenBLAS SkylakeX (기본) · `OPENBLAS_CORETYPE=Haswell` (Codex 경로) · `nice -n 19` · 스레드 1 · 60 s 넘는 실행 = `heavy.sh`.
- 숫자 = 아래 탐침 · 시험의 실행 출력 (JSON · 로그 동봉).  합성 반례의 값 · 빈도를 실침대 값으로 옮기지 않는다 (추정 표지).

## ① 지난 회차 (1 회차 impl) 결함 재확인

| ID | 판정 | 숫자 (`93d93bc02` · 1 회차 탐침 그대로 · `rerun_r1.log`) |
|---|---|---|
| PRE-impl-01 (P1) | **닫힘** | 같은 셀 끊김 (시험 단위): σ **5.5556** = 손 사슬 + R_j 간선 (`chain_I(G_PL, 7 G_AX, G_PL, 10)` 5.5556 · 옛 0.0) · 면 인접 끊김 **5.8824** = 손 (6 G_AX + R_j) — 두 꼴이 같은 규칙 (Q-A 끊긴 조각 = 다른 섬유).  생산 단위 (R_j 1e6 Ω): 같은 셀 0.0592552 ↔ 면 인접 0.0592557 (옛 0.0 ↔ 872.66).  MUT-RCA2 `_distinct_keep` 변이 잡힘 |
| PRE-impl-02 (P2) | **닫힘** | (i) 같은 fid · 다리 중심선 1.2 > D 1.1: 자기 instance 0 · 접합 효과 0 (옛 +4.25 %) = 다른 fid (instance 0 · 미등록 면 4).  (ii) 같은 fid · 다리 0.1414 < 2 r_f: 다리 사이 자기 instance **1** (d0 0.1 · L_c 4.085 · k 3 · 실현 3 · 옛 0) (`probe2_selfd_ii.json`) |
| PRE-impl-03 (P2) | **닫힘** | ① 접합 + centerline = `cjunc_plan` ValueError · payload 입구 `PTFE_CENTERLINE` · protocol 거부.  ② SDCP 덮인 접점: σ **11.9048** (R_j 1e3 = R_j ∞ = 손 "SV 두 면만" · 옛 12.1535 +2.09 %) · MUT-RCA2 `_piece_cand` 변이 잡힘 |
| PRE-impl-04 (P2) | **원 반례 닫힘 · 옆 자리 열림** | 섬유 하나가 SDCP 지남: 비 **1.0** (옛 ∞) · F1 + 먼 SDCP: 비 **1.0** (옛 ∞) · 한 섬유만 지나고 다른 섬유 끝이 닿음 (QD ③): ∞ (참).  두 섬유가 함께 지나는 성분 = 끊지 않음 → **새 `PRE2-impl-01`** |
| PRE-impl-05 (P3) | 한계로 기록 (고치지 않음 · 1 회차 권고대로) | 90° → 89.99° (L_c/L_par 1 → 1.0000000152): 시험 단위 −1.049 % · 생산 1e2 Ω −0.978 % · 1e4 Ω −2.10e-4 · 1e6 Ω −2.11e-6 (1 회차와 같은 수) · `_n_sub` 주석 · 등록 ⑫ · `CJUNC_QUALIFIERS` · 시험 KBND |
| PRE-impl-06 (P3) | **닫힘** | 닫힌 고리 σ **25.6410** = 손 연속 고리 (s_min 3 · 100 둘 다 · 옛 18.47 · 12.93) · MUT-RCA2 `_ring_alias` 잡힘 |
| PRE-impl-07 (P3) | **닫힘** | `probe_zero_binding.py` (새 API · 매니페스트 필수): 자기 영값 · 양의 해 증서 = 받음 · 다른 침대 지문 · 같은 σ 다른 plan_rows · 결합 칸 결손 · 판 `cert-bind-v0` · 매니페스트 registry 결손 · 매니페스트 없음 = **6 꼴 모두 거부** (`CERT|bind|`) |
| PRE-impl-08 (P3) | **닫힘** | 웹앱이 생산자 `CJUNC_QUALIFIERS` (8 줄) 를 그대로 띄운다 (W14 · 템플릿 사본 없음).  ⚠ 그 한정어 문장이 "다리만 끊는다" 고만 적어 못 가른 다리를 말하지 않는다 (→ PRE2-impl-01 해결에 포함) |
| PRE-impl-09 (P3) | **닫힘** | MUT-RCA 6/6 · MUT-RCA2 5/5 — 변이 서명 = 생산 호출 (`certify=`) · 변이 안 예외 = 하네스 실패 (깨끗한 사본 실행).  1 회차 `probe_mut_cf.py` 는 API 가 바뀌어 (반사실 = `_assemble(counterfactual=)`) 더 쓰지 않음 |
| (재확인) RCA-07 · 13 증서 ⓓ | 그대로 | Codex 반례 여섯 (주 · 11 사슬 · 연결 · 설명용 φ · 영값) ⓓ 거부 · 참 G* 구간 안 · 최종 판정 두 BLAS 경로 같음 · 생존성 보장 오차 1.33e-9 · 3.78e-8 (1 회차와 같음) · 극한 유한 200 Ω 1.75e-14 (기본) / 2.59e-14 (Haswell) · 바닥 VALID_ZERO · 천장 축약 정확 |
| (재확인) RINT2-B01 | 그대로 | 원본 2/2 · 줄바꿈 고정 뺀 변이 0/2 |

설계 쪽 결함 중 코드에 닿는 넷 (판정은 design 검토자 몫 · 여기는 코드 확인만): PRE-design-08 (`judge_set` NOT_COMPUTED 우선 = 변이 C1 이 U11 · U11b 에 걸림) · PRE-design-10 (W₊ = 변이 C5) · PRE-design-11 (단락 = NOT_COMPUTED = §③ Q1 표) · PRE-design-04 (단계 2 관문 = R 계획 줄 · 숫자 넷 = 변이 S1 · S2).

## ② 보장 목록 (보장 · 자리 · 반례 · 결과)

| # | 보장 | 자리 (`93d93bc02`) | 반례 · 시험 | 결과 |
|---|---|---|---|---|
| A1 | Q-A 끊긴 조각 = 서로 다른 섬유 규칙 (d ≤ D → R_j) | `carbon_junction.py:171` `_distinct_keep` · `:487` `_segments_of` | 같은 셀 · 면 인접 끊김 (위 ①) · 0 길이 선분 1 · 3 연속 · 셀 면 위 꼭짓점 · 셀 모서리 스침 → σ = 손 사슬 12.5 (상대 1.7e-15 · 가짜 조각 · 접합 0) (`probe2_degenerate.json`) | ✅ |
| A2 | Q-A 닫힌 경로 이음매 = 연속 (끊기면 이음매를 지나 한 조각) | `:177` `_ring_alias` · `:481` · `:509` · `:582` | 고리 25.6410 = 손 · 변이 J5 (끊긴 고리 잇기 끔) · J6 (고리 짧은 쪽 호 끔) | ✅ · 변이 ④ |
| A3 | Q-B 자기 접합 = 같은 조각 중심선 쌍 d ≤ D + 바닥 (s > D · s > (π/2)d) + 쌍마다 s ≥ s_min | `:162` `_self_floor` · `:1160` `_continuity` · `:1209` `_self_pairs` | (i) (ii) 위 ① · 변이 J3 · J7 · J8 | ✅ · 변이 ④ |
| A4 | Q-C 포트 옮김 없음 (덮이면 미실현) · 덮은 상의 법칙만 · 접합 + centerline 거부 | `:1446` `_piece_cand` · `:1466` `_port_take` · `:1943` · `ca_ext_cjunc.py:160` · payload `PTFE_CENTERLINE` | SDCP 덮임 11.9048 = SV 만 · centerline 거부 · 변이 J4 | ✅ · 변이 ④ |
| A5 | **Q-D 반사실 = 다른 섬유 사이 SV 우회만 끊음 · 섬유 자기 연속 유지** (등록 R 4판 §5-6 SV 행: "한 SDCP 성분을 거쳐 다른 섬유로 넘어가는 길") | `:183` `_sv_cut_rows` · `:1802` `_sv_split` · `:2388` `sv_counterfactual` · `ca_ext_svcf.py:134` · 사슬 `rint_r_chain.py:519` `sv_assess` | 한 섬유 지남 1.0 · F1 먼 SDCP 1.0 · 한 섬유 지남 + 다른 섬유 끝 닿음 ∞ (참 · `SV_DEPENDENT`) · **두 섬유가 같은 성분을 지남 → 비 1.0 · `computed` · 사슬 표지 [] (참 = ∞)** | ❌ **PRE2-impl-01** |
| A6 | Q1 단락 = `NOT_COMPUTED` (사유 `ELECTRODE_SHORT`) · σ None + 증서로 남음 · 다른 멈춤 이름으로 흐리지 않음 | payload `mpm_webapp_payload.py:894` `_step3_early` · `run_contract.py:1081` (short 가지) · `sr01_stamp_compare.check_arm` · 사슬 `:199-200` · `:1049-1052` · `:1750-1753` | 코드 읽기: 단락 조기 기록에 반사실 칸 없음 (요청 칸만) → `sv_cf_problem` None · 증서 없음 · σ +∞ 옛 꼴 · 다른 판 · zero ↔ short 사유 엇갈림 = 모두 NOT_COMPUTED (사유 없음 · 보수 쪽) · 시험 E9 · SP9–SP13 · Z02–Z07 · 변이 C12 · P1 · R2 · R3 | ✅ · 변이 ④ |
| A7 | Q2 §3-2c 한 끝이라도 NOT_COMPUTED → 전체 NOT_COMPUTED | `rint_r_chain.py:1819` `judge_set` | 변이 C1 | ✅ |
| A8 | Q2 §3-2b ③″ 보호 띠 (e = 그 런 증서의 보장 오차) · 칼날 e > d/(1 − d) | `:372` `outside_band` · `:379` `edge_hit` · `:1061-1068` (e 재계산) | RCA-01 회로 + 실제 `Ladder`: d 3.72825e-5 · 칼날 3.72839e-5 · 칼날 × (1 − 1e-6) → hi 끝 후보 (비 599.035) · × (1 + 1e-6) → 바깥 이웃 1e7 (비 1,000) · e 3.7e-5 / 3.8e-5 / 1e-4 = 등록 ⑧ 그대로 (`probe2_band_knife.json`) · 변이 C2 · C3 · C11 | ✅ |
| A9 | Q2 §4-2 origin 상태 다름 = 넘음 · W ∈ {0, +∞} 이면 W₊ | `:405` `dbe_origin_ok` · `:417` `w_pos_of` | 변이 C4 · C5 | ✅ · 변이 ④ |
| A10 | Q2 §5-5b 결정표 (오른쪽 칸 · 점 구간 · ⑰ · ⑱) · 닫힘 | `:186` `DECISION` · `:193` `STATE_VERDICTS` · `:488` `decide_sentence` · `:442` `judge` | `judge` 출력 = 상태별 허용 이름의 부분집합 (positive: 5 · point: PASS/FAIL · extended: UNINF/GAP/FAIL · 겹침 없음 · 손 분석) · 혼합 탐침 A–E (`probe2_item9_assemble.json`) · 변이 C10 · C15 | ✅ · 변이 ④ |
| A11 | §5-6 ② ③ ④ · 항목 9 (멈춘 변이 단계 = `<V>_UNCHECKED` · 주 판정 유지 · 주 단계 멈춤 = 전체 NOT_COMPUTED) | `:205` · `:212` · `:1838` `variant_flag` · `:1999-2001` · `:2032-2033` | 혼합 A (멈춤 · 다른 이름 · 같음 · 안 돌림): `FIBRE_UNCHECKED · SVORDER_UNCHECKED · UNREG_SENSITIVE` · PASS 이름 그대로 · 문장 보류 + 감도 미완료 · B (넷 다 멈춤): 넷 다 UNCHECKED · 감도 미완료 없음 (㉘ 읽기) · C (GRID 자기 CALIB_ORIGIN_SENSITIVE): `GRID_UNCHECKED` · E (변이 CALIB_EDGE): `FIBRE_SENSITIVE` · 주 단계 멈춤 = `INPUT_STAGE_STOPPED` → NOT_COMPUTED · 변이 C6 · C7 · C8 | ✅ · 변이 ④ |
| A12 | §5-6 SV 문턱 = "넘으면" (비 > 문턱) | `:535` | 변이 C9 (≥) → V06b · U08 실패 | ✅ |
| A13 | Q-G 결과 전 숫자 넷 (점 상한 · 역폭 상한 · SV 문턱 · 범위) 이 null · NaN · 음수 · 문자열 · bool · 다른 해시면 막음 | `rint_r_chain.py:644` `load_plan` · `:683` `require_plan_numbers` · `ca_s0_census.py:895-976` | 28 꼴 (`probe2_plan_gate.json`): null 4 · NaN 3 · 1e400 (→ inf) 3 · 음수 3 · 문자열 3 · bool 3 · 12.0 · 0.99 · 1.0 = 구조화 멈춤 · **10**400 정수 3 = 잡히지 않은 OverflowError · 중복 칸 = 받음 (마지막 값)** · 변이 C13 · S1 · S2 | ⚠ PRE2-impl-03 |
| A14 | B 증서 ↔ 런 결합 (격자 · 계획 · 접합 지문 · 판 · 칸) | `run_contract.py:838` · `:917` `cert_binding_problem` | ① PRE-impl-07 6 꼴 거부 · 변이 R1 · R4 | ✅ · 변이 ④ |
| A15 | 끄면 비트 같음 (매니페스트 · step3 값 · 영수증 · 팔 이름 · σ) ↔ `a76f59d0d` | 리포 b6 B 묶음 (`--old-scripts` = `a76f59d0d` 사본 + docs 링크) | **30 PASS · 0 FAIL**: 영수증 44 개 `receipt_digest` 같음 · 34 짝 `receipt_match` 같음 · payload off LEAN2 · centerline LEAN2 · off LEAN3 · face_alpha LEAN2 = **차이 0** · off + rtol / face_alpha + rtol = 허용 칸 6 (RCA2 결합 칸) · off + 접합 = 허용 칸 27 (RCA1 · RCA2) · σ 는 허용 목록 밖인데 차이 없음 (`b6_B_vs_a76.log`) · 러너 영수증 `sv_counterfactual` = 켤 때만 칸 | ✅ |
| A16 | ⓓ 목표량 증서 (U ≥ G ≥ 1/R_q · 보장 오차 ≤ 1e-4) · 두 BLAS 경로 | `step3_conv_cert.py` (두 판 사이 = 결합 칸만 바뀜) | ① 재확인 줄 | ✅ |
| A17 | SV 반사실 기록 검증기 — 상태 ↔ 비 ↔ 표지 · 요청 ↔ 기록 | `ca_ext_svcf.py:89` `sv_cf_problem` | 6 꼴 (`probe2_svcf_record.json`) — 비 ≠ G_full/G_cut · 반사실 증서 실패인데 computed · 비 0.5 (< 1) · G_cut None · n_unsplit 1 = **모두 받음** | ⚠ PRE2-impl-02 |

## ③ 새 결함

| 임시 ID | P | 자리 | 반례 (입력 · 기대 · 실제) | 최소 해결 |
|---|---|---|---|---|
| **PRE2-impl-01** | **P1** | `carbon_junction.py:183-198` `_sv_cut_rows` (지나는 무리 ≥ 2 = `continue` · 끊지 않음) · `:1871-1883` (`n_unsplit_bridging_components` 셈만) · `:2402-2431` (그대로 `computed` · 비 = G_full/G_cut) · `ca_ext_svcf.py:134` `chain_view` (상태 · 비만) · `rint_r_chain.py:519-539` `sv_assess` (비 > 문턱만) · 웹앱 `mpm_lab.html` "🔀 SV 반사실 비" · 등록 R 4판 §5-6 SV 행 ("한 SDCP 성분을 거쳐 다른 섬유로 넘어가는 길" 을 끊는다 · "원장을 못 읽으면 `SV_UNCHECKED`") | **두 섬유가 같은 SDCP 성분을 지남** (vox 1 · 5×3×9 · A = 아래 판 → z 6.5 끝 · B = z 2.5 끝 → 위 판 · A↔B 중심선 2.0 > D 1.1 · SDCP 셀 (1,1,4) (2,1,4) (3,1,4) 이 A · B 의 z 4 셀을 덮음 · 아래 → 위 길은 A → SDCP 셋 → B 하나뿐): I_full **10.8696** = 손 사슬 (1/200 + 3/100 + 1/142.857 + 2/250 + 1/142.857 + 3/100 + 1/200).  다른 섬유 사이 우회를 끊은 참 G_cut = 0 → **기대 비 +∞ (`SV_DEPENDENT`)** · 실제 = `n_bridging_components` 1 · `n_unsplit_bridging_components` 1 · `n_sv_faces_cut` 0 · 상태 **`computed` · 비 1.0** · 사슬 `sv_assess(문턱 2.0)` 표지 **[]** (`SV_UNCHECKED` 도 없음) → 차단 표지 없이 PASS 문장이 열릴 수 있다 (혼합 탐침 D 꼴).  대조: B 가 성분 안에서 시작 (한 섬유만 지남) = 비 ∞ · `SV_DEPENDENT` (옳음).  **실제 payload 끝-끝 (b6 고정물 꼴 · vox 1 µm · `--step3-cjunc-sv-cf` · rtol 1e-12)**: 두 섬유 지남 = σ_e 0.039232 (POSITIVE · 증서 통과 · `ca_ext_record_ok` 통과) · 반사실 `computed` · **비 1.0** · 끊은 면 0 · 못 가른 다리 1 · 사슬 표지 **[]** ↔ 같은 침대에서 B 아래 막다른 가지만 뺀 대조 (한 섬유만 지남) = σ_e 0.039222 · 비 **85.42** · `SV_DEPENDENT` (`probe2_sv_unsplit_payload.json`) — 주 σ 는 0.02 % 차이인데 SV 차단 표지가 뒤집힌다 (참 비 ≈ 85 · 추정: 두 침대의 SV 다리 뒤 남는 길 (AM 경유) 이 같다).  빈도 [추정 · 합성]: 생산 단위 (vox 0.15 · VGCF Ø0.15 · VGCF 셀 2.5–3.4 % · SDCP Ø1 µm 구 셀 3.1–6.5 %) 침대 8 개에서 다리 18 개 중 **9 개 (50 %)** 가 못 가른 다리 · 침대 8 개 중 **7 개** 에 하나 이상 (`probe2_sv_unsplit_freq.json`) — DBE (SDCP 1 µm) 에서는 이 반사실 비가 흔하게 아래로 치우친다 (실침대 미확인).  시험에 이 꼴이 없다 — 변이 J1 · J2 생존 (접합 시험 전체 312/312 · PRE2-impl-04) | 결과 전 · 둘 중 하나 (1저자): **(가) fail-closed** — `n_unsplit_bridging_components` > 0 이면 반사실 상태 = 비를 싣지 않는 이름 (예 `unsplit_bridges`) 또는 `chain_view` 가 비 None → 사슬 `SV_UNCHECKED` (등록 "못 읽으면 SV_UNCHECKED" 그대로 · 뜻 변경 없음) · 웹앱 · 한정어 문장에 "못 가른 다리 n" · 시험 = 위 회로 (기대 `SV_UNCHECKED`) + 대조 회로.  (나) 역할 분리 표현 (Codex RCA-06 최소 해결 문구) — 지나는 섬유마다 덮인 구간의 자기 연속 간선을 따로 두고 다리 성분의 SV 면을 다 끊음 → 비 = 정의대로 · 등록 R §5-6 개정 (결과 0 건) · Codex 에 물을 것.  (가) 면 DBE 판정이 거의 늘 `SV_UNCHECKED` 일 수 있다 (추정 · 위 빈도) — 그 사실도 요청서에.  **(다) Rayleigh 괄호** (새 표현 없이 · 같은 조립기) — 못 가른 성분의 **모든 면** (SV 면 + 그 SDCP 셀의 다른 면 = 성분을 통째로 뺌) 을 끊은 판을 한 번 더 풀어 비의 위 끝, 지금 판 (못 가른 다리를 남김) = 아래 끝: 다른 섬유 사이 길만 끊는 어떤 정의든 지금 셀 그래프에서 그 성분에 닿는 간선 일부를 빼는 꼴이면 참 비 ∈ [아래, 위] (간선을 빼면 G 가 줄기만 한다 · Rayleigh) · 아래 > 문턱 → `SV_DEPENDENT` · 위 ≤ 문턱 → 표지 없음 · 걸치면 `SV_UNCHECKED` (등록 §5-6 개정 = 판정 규칙 · 결과 0 건 · 1저자) |
| PRE2-impl-02 | P3 | `ca_ext_svcf.py:89-131` `sv_cf_problem` — 상태 ↔ 비 꼴 · 문턱 ↔ 표지만 보고 기록 안 수를 다시 대조하지 않는다 (같은 판의 증서 검사는 "플래그를 믿지 않는다" 꼴) | 정상 기록 (G_full 10 · G_cut 5 · 비 2.0) 에서 하나씩 바꾼 사본: 비 1.0 (≠ G_full/G_cut 2.0) · 반사실 증서 ok False 인데 `computed` · 비 0.5 (< 1 · Rayleigh 위반) · `computed` 인데 G_cut None · n_unsplit 1 → **5 꼴 모두 문제 None** · 사슬 `chain_view` 가 그 비를 그대로 읽음 (`probe2_svcf_record.json`).  생산자 정상 경로는 비 = G_full/G_cut 로 만들므로 실제 오염 증거는 아님 (생산자 결함 · 옮김 오류가 있을 때만) | `computed`: G_full · G_cut 유한 > 0 · 비 = G_full/G_cut (상대 1e-12) · 비 ≥ 1 − (증서 폭 꼴의 여유) · 반사실 증서가 있으면 ok True · `no_through_without_sv`: G_cut 0 · PRE2-impl-01 (가) 를 고르면 n_unsplit > 0 ↔ 상태 결합도 여기 |
| PRE2-impl-03 | P3 | `rint_r_chain.py:640` `_num` (`math.isfinite(int)` → OverflowError) · `:649` `json.loads` (중복 칸 = 마지막 값) · 같은 함수를 S0 단계 2 관문이 부름 (`ca_s0_census.py:961-966` · `except _rrc.Stop` 만) | R 계획에 `"sv_cf_threshold": 1` + 0 400 개 (정수) → **잡히지 않은 OverflowError** (사슬 · 단계 2 관문 둘 다 · 구조화 멈춤 `PLAN_INVALID` 아님 · `s_min_um` · `calib_rj_ratio_max` 도 같음) · `max_ladder_points` 10**400 = 받음.  `"sv_cf_threshold": 2.0, …, "sv_cf_threshold": 50.0` → **받음 (50.0)** — 등록 sha 로 묶인 같은 바이트를 사람 (앞 값) 과 사슬 (뒤 값) 이 다르게 읽는다 (RIMPR-01 중복 칸과 같은 부류) · S0 계획은 정준 바이트 검사로 막히는데 R 계획엔 없다 (`probe2_plan_gate.json`) | `_num` 에서 OverflowError = 유한 아님 · `json.loads(object_pairs_hook=…)` 로 중복 칸 거부 (또는 S0 계획처럼 정준 바이트 대조) · 시험 = 위 두 꼴 (사슬 · 단계 2 관문) |

| PRE2-impl-04 | P3 | `test_carbon_junction.py` QD (SV 반사실 시험 넷 = 한 섬유 지남 · F1 먼 SDCP · 한 섬유 지남 + 다른 섬유 끝 닿음 · 기록 꼴) | 변이 J1 (`_sv_cut_rows` 의 못 가른 다리 지킴 줄 삭제) · J2 (`_sv_split` '지남' = 사이 위치가 덮임 · 같은 성분 조건을 뺌 → 덮이지 않은 사이로 두 번 닿는 섬유도 '지남') 둘 다 접합 시험 전체 **312/312 PASS** (생존).  J2 꼴이 실제로 돌면: 다른 섬유 B 가 SDCP 성분 옆을 따라 두 번 닿고 (사이 셀은 살아 있음) A 가 성분을 지나면 B 도 '지남' → 못 가른 다리 → 반사실이 B 를 안 끊는다 (PRE2-impl-01 과 같은 거짓 비 1.0 쪽 · 추정 · 코드 읽기) | PRE2-impl-01 시험 (두 섬유 지남 · 기대 = 고른 해결의 이름) + 덮이지 않은 사이로 두 번 닿는 섬유 + 지나는 섬유 꼴 (기대 = 그 섬유 SV 면 끊음) + 지나는 무리 둘 + 지나지 않는 무리 하나 꼴 · 각 변이 (J1 · J2) 가 옳은 이유로 실패하는지 |

## ④ 변이 (자리 · 바꾼 줄 · 잡힘 / 생존)

방법: 내 작업 트리에서 한 자리 (정확히 한 번 나오는 글) 를 바꿈 → 시험 묶음 → 원본 바이트로 되돌림 (sha256 대조 · 끝에 `git status` 깨끗) · 묶음마다 변이 없는 기준선 먼저 = 12 묶음 모두 실패 0 (`baselines_result.json`) · 사슬 = `test_rint_r_chain.py` 전체 (기준 174/174 · 92.2 s).  **32 변이 → 잡힘 30 · 생존 2 (J1 · J2)** (`mutations_result.json` · 생존 셋 다시 = `mutations_v1b_result.json`).

| # | 자리 | 바꾼 줄 | 결과 (실패한 시험) |
|---|---|---|---|
| C1 | `rint_r_chain.judge_set` | NOT_COMPUTED 우선 끔 (3판 순서) | 잡힘 U11 · U11b |
| C2 | `outside_band` | 보호 띠 e 무시 | 잡힘 U01e · U12b · U12c |
| C3 | `edge_hit` | 보호 띠 e 무시 | 잡힘 U12 · L22 |
| C4 | `dbe_origin_ok` | 상태 다름 = 넘음 끔 | 잡힘 U06 |
| C5 | `dbe_origin_ok` | W ∈ {0, ∞} 에도 W 그대로 (W₊ 끔) | 잡힘 U06 · U13b |
| C6 | `variant_flag` ③ | NOT_COMPUTED → SENSITIVE 로 | 잡힘 U14 · V18 · V21 · V22 |
| C7 | `variant_flag` ④ | 변이 자신의 CALIB_ORIGIN_SENSITIVE 무시 | 잡힘 U14 |
| C8 | `variant_stage_stopped` | 늘 False (항목 9 끔) | 잡힘 V21 · V22 |
| C9 | `sv_assess` | 비 > 문턱 → ≥ | 잡힘 V06b · U08 |
| C10 | `decide_sentence` | ⑰ 감도 미완료 덧붙임 끔 | 잡힘 V02 · U07 · V21 · V22 |
| C11 | `read_run` | 판독 보장 오차 e = 0 | 잡힘 L22 |
| C12 | `REG_STATES` | 단락 = POSITIVE_SOLVED | 잡힘 Z02 · Z04 · Z05 · Z07 |
| C13 | `PLAN_REGISTERED_NUMBERS` | sv_cf_scope 뺌 | 잡힘 N01 |
| C14 | `end_origin_push` | 끝 origin 팔 1 · 2 무시 | 잡힘 U10 · L21 |
| C15 | `judge` | GAP_ENVELOPE_ONLY → FAIL | 잡힘 U03 · U06 |
| **J1** | `carbon_junction._sv_cut_rows` | 못 가른 다리 (지나는 무리 ≥ 2) 지킴 줄 삭제 | **생존** (QD · SV · RCA06 · RCA06-H · MUT-RCA · MUT-RCA2 · CEN 40/40) |
| **J2** | `_sv_split` | '지남' = 사이 위치가 덮임 · 같은 성분 조건 뺌 | **생존** (40/40) |
| J3 | `_continuity` | s_min 무시 (바닥만) | 잡힘 KINK · KINK-R |
| J4 | `_port_take` | 덮인 위치를 포트로 (미실현 안 함) | 잡힘 QC · QD · MUT-RCA2 |
| J5 | `_segments_of` | 끊긴 닫힌 경로 이음매 잇기 끔 | 잡힘 RING |
| J6 | `_self_pairs` | 고리 짧은 쪽 호 끔 | 잡힘 RING |
| J7 | `_self_pairs` | 중심선 d ≤ D → 10 D | 잡힘 KINK · SELFD |
| J8 | 같은 조각 접촉 면 | 늘 융합 (자기 접합 자리 절단 없음) | 잡힘 KINK · KINK-R · RCA03 · SELFD |
| J10 | `_sv_split` | '지나는 무리' 표지 끔 | 잡힘 QD |
| R1 | `run_contract.cert_binding_problem` | 접합 지문 대조 끔 | 잡힘 T21f · T21j |
| R4 | `cert_binding_problem` | face_alpha 계획 지문 대조 끔 | 잡힘 T21g · T21j |
| R2 | `next_gen_state` short | 축약 instance > 0 검사 끔 | 잡힘 S3 |
| R3 | `next_gen_state` short | 결과 σ None 검사 끔 | 잡힘 S3 · S5d |
| P1 | `mpm_webapp_payload._step3_early` | 단락 σ None → 0.0 | 잡힘 S10b · SP9 · SP10 · SP11 · SP12 |
| S1 | `ca_s0_census.verify_plan_commit` | `require_plan_numbers` 끔 (Q-G) | 잡힘 L3v · L3w |
| S2 | `verify_plan_commit` | R 계획 tol_ff ↔ S0 tol_ff 대조 끔 | 잡힘 L3m |
| V1 | `ca_ext_svcf.sv_cf_problem` | 표지 ↔ 문턱 대조 끔 | 잡힘 S8e · S8f (b6 S 묶음 · 첫 판 묶음 SP · R 117/117 · 사슬 174/174 에는 없음 — 사슬은 생산자 표지를 안 읽는다) |

생존 둘을 시험 파일 전체로 다시: **J1 · J2 = `test_carbon_junction.py` 312/312 PASS (생존)** — 못 가른 다리 가지 · '지남' 판정 조건을 보는 시험이 없다 (→ PRE2-impl-04 · PRE2-impl-01 과 같은 자리).

## ⑤ 확인했지만 결함 아닌 것

- 단락 + SV 반사실 요청 (DBE 모서리 · c = 1 축약): 단락 조기 기록 (`early_record`) 에 반사실 칸이 없고 요청 칸 (`sv_counterfactual_request`) 만 있어 `sv_cf_problem` = None → `CA_EXT_RECORD` 로 흐려지지 않는다 (코드 읽기 · 실행 시험은 천장 단락 E9 · SP9–SP13 뿐 — DBE 모서리 단락 + 반사실 요청 조합의 실행 시험은 없다).
- 반사실 조립의 단락 판정은 주 해와 같다 (축약 무리 · 판 결합이 같고 반사실은 간선만 뺀다) → 반사실 상태 `cjunc_electrode_short` 는 주 해가 단락이 아니면 나오지 않는다.
- S0 단계 2 보고의 R 계획 sha 를 사슬이 다시 대조하지 않는다 — 등록 §2-1 이 "관문 = 순서 · 결합의 기록 · 미열람은 이력 공개로만" 이라 적은 자리 (사람 규율 · 결함 아님).
- 웹앱 `viewer3d.js` 변경 = 비교표 없는 AM 상 (WEB-10 · F11) — Rint ② 와 무관.
- PRE-impl-02 (ii) 의 같은 fid 자기 instance L_c 4.085 ↔ 다른 fid 2.990 차이 = 기하 차이 (같은 fid 판에는 위 가로가 다리 2 를 0.1 거리로 지나는 접촉이 더 있다 · 이웃 선분 무리로 한 instance) — 같은 접촉 기준.

## ⑥ Codex 에 물을 것 (코드가 고른 자리 · 등록 §10-2 ㉓–㉞ 와 겹침 표시)

1. (Q-A · ㉓–㉞ 밖) 생산 끊기 규칙 (gap_tol 2 × 중앙 점 간격) 이 물리 끊김과 표본화 끊김을 가르지 않는다 → 표본 간격이 국소로 두 배를 넘는 연속 섬유에도 R_j 접합이 들어간다 (S0 census `n_pieces` · `n_instances_same_fid_pieces` · `n_piece_cell_meets` 가 셈).  이 읽기가 Q-A 의 뜻인가.
2. (Q-D · PRE2-impl-01 과 같은 자리 · ㉓–㉞ 밖) 같은 섬유가 한 SDCP 성분을 두 번 지날 때 (지나는 무리 둘 · 같은 조각) 의 SDCP 지름길 = 지금 "못 가른 다리" 로 세고 안 끊는다 · 같은 조각의 지나지 않는 닿음은 끊는다 (자기 지름길 일부를 끊음) — 등록 "다른 섬유로 넘어가는 길" 과 어디까지 같은가.
3. (§5-6 SV 문턱 · ㉓–㉞ 밖) 사슬 = 비 > 문턱 (등록 "넘으면") · 생산자 자기 표지 = 비 ≥ 문턱 (이 배선에서는 문턱 None 이라 안 씀) — 칼날 하나가 두 곳에서 다르다 (사슬 쪽 > 는 변이 C9 로 V06b · U08 이 지킨다 · 생산자 쪽 ≥ 는 이 배선에서 쓰이지 않음).
4. (㉘ · ㉛ 그대로) 멈춘 변이 = 돌림 (감도 미완료 안 붙음) · 입력 기록 전에 멈춘 변이 단계 = 판정 전체 NOT_COMPUTED — 혼합 탐침 B 가 그 읽기대로 나온다.

## ⑦ 요청서 맨 위 "이번에 닫는 것 / 닫지 않는 것" 문장 후보

**닫는 것** (근거 시험 · 탐침):
- 1 회차 impl 01 · 02 · 03 · 06 · 07 · 08 · 09 (원 반례) — GAP · SELFD · QC · RING · T21 · W14 · MUT-RCA 6/6 · MUT-RCA2 5/5 · 2 회차 탐침 (`rerun_r1.log` · `probe_zero_binding.json` · `probe2_selfd_ii.json`).
- PRE-impl-04 의 원 두 꼴 (섬유 하나가 SDCP 를 지남 · 접합에서 먼 SDCP → 비 1) — QD ① ②.
- Q1 단락 = `NOT_COMPUTED` (사유 `ELECTRODE_SHORT`) — E9 · SP9–SP13 · Z02 · Z04 · Z05 · Z07 (+ 변이 ④).
- Q2 규칙 여섯 · 항목 9 — U01e · U11 · U11b · U12 · U12b · U12c · L22 · U06 · U13b · U14 · V18 · V21–V24 · U07 · X05b · M29–M40 · 칼날 탐침 (`probe2_band_knife.json`) · 혼합 탐침 (`probe2_item9_assemble.json`).
- Q-G 결과 전 숫자 넷 = null · NaN · 음수 · 문자열 · bool 거부 — 사슬 N 묶음 · S0 L3v · L3w · `probe2_plan_gate.json` (큰 정수 · 중복 칸은 PRE2-impl-03).
- B 증서 ↔ 런 결합 — T21 · `probe_zero_binding.json`.
- 끄면 비트 같음 (`a76f59d0d` 대조) — b6 B 30/30 · off 네 경우 차이 0 · 접합 켬 σ 같음.

**닫지 않는 것**:
- 두 섬유 이상이 같은 SDCP 성분을 지나는 다리 (PRE2-impl-01) — 반사실이 끊지 않고 `computed` 비를 낸다 → 고친 판 (가 또는 나) 을 보낼 때까지 SV 행은 닫지 않는다.
- PRE-impl-05 분산판 v0 k 경계 계단 = 한계 기록 (등록 ⑫ · 고치지 않음).
- 실침대 빈도 (못 가른 다리 · 조각 끊김 · 덮인 포트) = S0 census 뒤 · 합성 어림만 있음.
- 웹앱 SV 반사실 줄이 못 가른 다리를 표시하지 않음 (PRE2-impl-01 해결과 같은 묶음).
- SV 반사실 '지남' 판정 · 못 가른 다리 가지의 시험 (변이 J1 · J2 가 접합 시험 전체 312/312 를 지난다 · PRE2-impl-04).
- SV 반사실 기록의 내부 일관성 재대조 (PRE2-impl-02) · R 계획 큰 정수 · 중복 칸 (PRE2-impl-03).

## ⑧ 못 본 것 · 이유

- PRE2-impl-01 payload 끝-끝은 돌렸다 (위 ③) — ⚠ 첫 두 판은 고정물 결함 (SE 점이 섬유 셀을 덮음 · AM 꼭대기로 정하는 상자 위끝이 낮음) 이라 버렸다 · 셋째 판 = b6 AM 기둥 줄 그대로 + SE 를 섬유에서 멀리.  사슬 실제 `read_run` (러너 영수증 · 등록 계획) 까지는 안 갔다 (`chain_view` · `sv_assess` 는 실제 함수).
- 실침대 · GPU 0 · `test_carbon_junction.py` 전체 · `test_step3_target_cert.py --long` (T17 여섯 경로) · e2e 실제 러너 묶음 = 메인 게이트 (155 ✓) 가 돈 것 · 다시 안 돌림 (지시).
- 셋 이상 같은 셀 재방문 · 셋 이상 포트 동률 · 주기 경계 (접합은 주기 거부) — 코드 읽기만 (쌍마다 따로 · 사전식 최소 · `PERIODIC` 거부).

## ⑨ 탐침 · 재실행

폴더 `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview2_impl/` (리포 밖).  `PRE_REPO` = 검토 트리 (작업 트리 또는 `git archive 93d93bc02` 사본 `head_93d/`).

```
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview2_impl
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a388f740a6ce4524d
# 사본 다시 만들기 (다 쓴 뒤 지웠다):  mkdir -p $D/head_93d $D/base_a76
#   git -C $WT archive 93d93bc02 scripts | tar -x -C $D/head_93d ;  ln -sfn $WT/docs $D/head_93d/docs
#   git -C $WT archive a76f59d0d scripts | tar -x -C $D/base_a76 ;  ln -sfn $WT/docs $D/base_a76/docs
export PRE_REPO=$D/head_93d          # git archive 93d93bc02 scripts + docs 링크 (변이 중에도 깨끗)
R='nice -n 19 env OPENBLAS_NUM_THREADS=1 python3 -I'
bash $D/rerun_r1.sh                  # 1 회차 탐침 11 개 → rerun_r1.log + JSON
bash $D/rerun_cert.sh                # 증서 · 극한 두 BLAS 경로 → rerun_cert.log · probe_cert_codex_{default,Haswell}.json
cd $D && $R probe_limits.py          # 고친 판 (매니페스트 결합) → probe_limits.json (Haswell 은 OPENBLAS_CORETYPE=Haswell)
$R probe_zero_binding.py             # PRE-impl-07 · B 결합 7 꼴
$R probe2_sv_unsplit.py              # PRE2-impl-01 회로 + 대조
bash $D/run_sv_payload.sh            # PRE2-impl-01 실제 payload 끝-끝 (b6 고정물 꼴) → probe2_sv_unsplit_payload.json
$R probe2_sv_unsplit_grid.py         # payload 와 같은 rasterize 인자로 격자 셀 · census 직접
$R probe2_sv_unsplit_freq.py         # PRE2-impl-01 합성 빈도 (8 침대)
$R probe2_svcf_record.py             # PRE2-impl-02
$R probe2_plan_gate.py               # PRE2-impl-03 · Q-G 28 꼴
$R probe2_band_knife.py              # ③″ 칼날
$R probe2_item9_assemble.py          # 항목 9 · 결정표 혼합
$R probe2_selfd_ii.py                # PRE-impl-02 (ii)
$R probe2_degenerate.py              # 0 길이 선분 · 경계 꼭짓점
bash $D/heavy.sh bash $D/run_b6_B.sh B            # 끄면 비트 같음 (base_a76/ = git archive a76f59d0d + docs 링크) → b6_B_vs_a76.log
bash $D/heavy.sh python3 -I $D/mutate.py $D/mutations.json $D/mutations_result.json   # 변이 32 (작업 트리 · 원본 바이트로 되돌림)
bash $D/heavy.sh python3 -I $D/mutate.py $D/baselines.json $D/baselines_result.json   # 같은 묶음 기준선 (변이 없음)
bash $D/heavy.sh python3 -I $D/mutate.py $D/mutations_v1b.json $D/mutations_v1b_result.json   # 생존 셋을 시험 파일 전체로
bash $D/heavy.sh bash $D/run_chain_test.sh          # 사슬 시험 기준선 (174/174 · 92.2 s) → chain_baseline.log
```
