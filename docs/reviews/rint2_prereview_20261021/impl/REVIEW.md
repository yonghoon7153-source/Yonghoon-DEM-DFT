# 사전 리뷰 (구현 쪽 · `impl`) — Rint ② RCA 수정 묶음 · 검토 커밋 `a76f59d0d`

**결론 (한 줄): 정량 판정 GO 불가 — HOLD.  새 P1 1 (`PRE-impl-01` 같은 섬유 끊긴 두 조각이 한 셀에서 만나면 이음이 사라짐 · σ → 0) · P2 3 · P3 5.**
Codex 10-21 반례 (RCA-03–07 · 13 · RINT2-B01) 자체는 고친 코드에서 전부 닫힌다 (아래 보장 표 ✅).  막는 것은 고친 자리 **옆**에서 나온 같은 부류다.

- 기준: 작업 트리 `git reset --hard a76f59d0d` (fetch 안 함) · 기반 `47d23baba` (RCA 수정 묶음 전) 은 `git archive` 로만 읽음 · 리포에 쓰지 않음.
- 환경: Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · OpenBLAS SkylakeX (기본) · `OPENBLAS_CORETYPE=Haswell` (Codex 경로) · 모든 실행 `nice -n 19` · `OPENBLAS_NUM_THREADS=1` · ≤ 60 s · 게이트 창 안이라 무거운 묶음은 돌리지 않음 (§5).
- 숫자는 아래 탐침의 실행 출력 그대로 (JSON 동봉).  합성 반례의 오차율을 실침대 오차율로 옮기지 않는다.

## 1. 보장 목록 (보장 · 자리 · 반례 · 결과)

| # | 보장 (주장하는 쪽) | 자리 | 반례 · 시험 | 결과 |
|---|---|---|---|---|
| 1 | RCA-03 — 같은 셀 다른 branch 를 합치지 않음 · 판정문 폴리라인 단락 없음 | `carbon_junction.py:748-786` · 설계 v1 §4-1 (줄 254) | 리포 시험 RCA03 (판정문 폴리라인 + 리드) | ✅ σ = 직렬 사슬 1.07142857 (옛 합침 2.5 · ×2.333) · 36/36 (RCA03 · 04 · 05 · 06 · KINK-R) |
| 1a | 옆 자리 — "s < s_min = 같은 가닥의 연속 · 이음은 그 경로의 축방향 간선뿐" | 같은 자리 `:786` (`path_only`) · `:782` (면 = 융합) | `probe_gap_revisit*.py` — 끊기 (gap) 두 끝이 같은 셀 / 면 인접 셀 | ❌ `PRE-impl-01` |
| 1b | 옆 자리 — 닫힌 고리 (첫 점 = 끝 점) | `_canon_flip` 이 닫힌 경로를 받는다 (`:255-258`) | `probe_closed_loop.py` | ❌ `PRE-impl-06` |
| 1c | 옆 자리 — 자기 접합 = 서로 다른 섬유와 같은 물리 ("같은 길이 법칙 · 같은 R_j") | 자기 후보 = 면 · 같은 셀 (`:720` · `:756`) ↔ 서로 다른 섬유 = `d ≤ D` (`:916`) | `probe_self_vs_distinct.py` | ❌ `PRE-impl-02` |
| 2 | RCA-04 — 포트 = 경로 반전 · 공선 세분 · fid 재명명 불변 | `_port_pick` `:1202-1234` · `_canonical_paths` | 리포 시험 RCA04 · 04-V · 04-EPS · 04-DUP · MUT-RCA (lexmax · 옛 k 규칙 변이 잡음) · 분석: 접점이 든 셀이 살아 있으면 그 셀이 최근접 중심 (격자 Voronoi) → 동률은 경계에서만 · 사전식 | ✅ |
| 2a | 옆 자리 — 접점 셀이 다른 상으로 덮일 때 (포트 r_port 안 재탐색) · Rayleigh 단조 (절연체를 늘려 σ 가 커지지 않음) | `:1249` (`_piece_cand` = 살아 있는 위치) · `:1282` · `ca_ext_cjunc.py:157` (centerline 받음) | `probe_ptfe_monotone.py` · `probe_sdcp_relocate.py` | ❌ `PRE-impl-03` |
| 3 | RCA-05 — 분산판 v0 · Codex 5 노드 1.366013071895 / 5 / 0.238095238095 S | `_n_sub` `:1367` · `_subedges` `:1376-1448` | 리포 시험 RCA05 (CX 침대 = Codex 회로 × 50 · 1e-12) | ✅ |
| 3a | 옆 자리 — L_c/L_par 가 1 (정수) 을 넘는 경계에서 σ 연속 | `_n_sub` (k = ceil · 1e-9 띠) | `probe_k_boundary*.py` (90° → 89.99°) | ⚠ `PRE-impl-05` (P3) |
| 4 | RCA-06 — 옛 지배 가드 철회 · `sv_local_dissipation` 진단 · 반사실 비 (노브) | `sv_counterfactual` `:2033-2072` · `_assemble` `:1926` | 리포 시험 RCA06 (SV 전류 몫 0.9151 · P_SV 0.2497 < P_VV 0.3067 · 비 10.291254 · 문턱 2.0 → `SV_DEPENDENT`) | ✅ |
| 4a | 옆 자리 — 반사실 비가 "SV 융합 우회가 VV 접합을 대신하는 크기" 를 잰다 | 같은 자리 (부류 `sv_face` 전부 끊음) | `probe_sv_cf.py` | ❌ `PRE-impl-04` |
| 5 | RCA-07 — 목표량 증서 ⓓ: 상한 U (Dirichlet) ≥ G* ≥ 하한 (결손 허용 Thomson) · 게시 G 보장 오차 ≤ 1e-4 · 정확 분수 판정 | `step3_conv_cert.py:418-597` | `probe_cert_codex.py` (Codex 반례 셋 · 설명용 후보 φ · 영값) × 두 BLAS 경로 · 손 분석 (아래 §3) | ✅ 여섯 경우 모두 참 G* 가 구간 안 · ⓓ 거부 · 판정 두 경로 같음 |
| 5a | ⓓ 생존성 — 정상 수렴 해를 거부하지 않음 (대비 1.9e6) | 같은 자리 | `probe_cert_liveness.py` (무작위 관통 침대 둘 · 생산 CG rtol 1e-12) | ✅ 보장 오차 1.33e-9 · 3.78e-8 · 직접해 대비 8.4e-10 · 3.7e-8 |
| 5b | RCA-13 — VALID_ZERO_TOPOLOGY ↔ POSITIVE_SOLVED 분리 · 증서 ↔ 결과 결합 | `early_record` `:612` · `run_contract.py:756-868` | `probe_limits.py` (바닥 = 영값 받음) · `probe_zero_binding.py` | ✅ 분리 · ⚠ 영값 증서 결합 `PRE-impl-07` (P3) |
| 6 | Z3 — α 먼저 · 접합 간선 α 없음 · P1 = face_alpha 만 · centerline/off + P1 거부 · σ(P1) ≤ σ(P0) | `cjunc_plan` `:1606` · `step3_sigma` couple (α `_keep` → `add_faces`) | 코드 읽기 · 그들 시험 A9 (face_alpha 단조 · 돌리지 않음) | ✅ face_alpha 경로 · ❌ centerline 경로 (`PRE-impl-03`) |
| 7 | 극한 — R_j = ∞ 바닥 (간선 없음 · 발자국 절단) · R_j = 0 천장 (양 끝 정확 축약) · 손 회로 | `cjunc_plan` · `_assemble` 축약 | `probe_limits.py` (CX · k = 5) × 두 BLAS 경로 | ✅ 유한 200 Ω 상대 1.75e-14 / 2.59e-14 · 천장 정확 / 1.6e-14 · 바닥 = `no_through_component` → VALID_ZERO (ok) |
| 8 | 끄면 비트 같음 (cjunc · face_alpha · 증서 끔) | `step3_sigma` 끈 경로 | `probe_off_bitid.py` — 기반 `47d23baba` scripts 전체 vs HEAD · 무작위 관통 침대 셋 · 생산 CG | ✅ 세 침대 모든 결과 칸 sha256 · σ hex · sid sha 같음 (러너 · payload 파일은 두 판 사이 diff 없음) |
| 9 | 사슬 — 멈춤 · 값 봉인 · 다른 판본 · 킷 · sid_off 섞임 멈춤 | `rint_r_chain.py:538-628` (두 판 사이 변경 없음) | 리포 시험 `test_rint_r_chain.py` | ✅ 89/89 (37.0 s) · 범위 밖 항목은 손대지 않음 |
| 10 | RINT2-B01 — 시험 작성기 LF 고정 (Windows 글자 모드 흉내) · parser 그대로 | `test_rint_g2_join.py:157-163` · J0w | `probe_b01_mutation.py` (원본 vs `newline='\n'` 뺀 변이) | ✅ 원본 2/2 · 변이 0/2 (옳은 이유 — CRLF 바이트) |

## 2. 결함

| ID | 등급 | 자리 | 반례 (입력 · 기대 · 실제) | 최소 해결 |
|---|---|---|---|---|
| **PRE-impl-01** | **P1** | `carbon_junction.py:748-786` (재방문 쌍 → s < s_min 이면 `path_only` · 간선 없음) ↔ `:782` (같은 조건의 면 = `K_SELF_FUSED` 융합) · 설계 v1 §4-1 줄 254 *"s < s_min → 접합 없음 — 이음은 그 경로의 축방향 간선뿐"* | 섬유 하나가 `fibre_pieces` 끊기 (틈 > 2 × 점 간격 중앙값) 로 두 조각 · 두 끝이 **같은 셀**.  조각 사이에는 축방향 간선이 없으므로 "경로" 가 없다.  ① 시험 단위 (h 1 · r_f 0.5 · 틈 0.70 · s_min 3): 기대 (옛 경로 = 손 직렬 사슬) **12.5** · 실제 **0.0** (`no_through_component`) · 같은 틈이 **면 인접** 셀이면 12.5 (융합).  ② 생산 단위 (h 0.15 · r_f 0.075 · tol_ff 0.03 · 점 간격 0.05 · 틈 0.12 · s_min 0.3 (가정)): 같은 셀 **0.0** ↔ 면 인접 **872.664444444446 S/cm** = 옛 경로.  두 끝 중심선 거리 (0.12) < 2 r_f (0.15) — "끊긴 섬유" 로 읽어도 닿는 접촉이다.  census 는 이 쌍을 `n_self_revisits_path_only` 1 ("경로로만 이어진다") 로 적는다 (거짓). | `path_only` 는 **실제로 이어진 경로가 있을 때만** — 두 위치 사이 축방향 사슬이 같은 조각 안 · 살아 있는 위치로 이어지는지 원장에서 확인 · 아니면 (다른 조각 · 끊긴 경로) 같은 쪽 규칙을 면과 맞춘다 (s < s_min = 융합 또는 서로 다른 섬유와 같은 `d ≤ D` 접촉).  시험 = 위 두 꼴 + 면 인접 대조 + census 칸 정정.  ⚠ 실침대 빈도 미확인 (S0 census 에 "조각 수 > 섬유 수 · 같은 셀 조각 끝" 을 보탤 것) |
| **PRE-impl-02** | P2 | 자기 후보 = 셀 인접 (`:720` 면 · `:756` 같은 셀 · 중심선 거리 검사 없음) ↔ 서로 다른 섬유 = `d ≤ D = 2 r_f + tol_ff` (`:916`) · 설계 v1 줄 253 · 한정어 *"instance = 중심선 기하 근접"* · *"자기 접합 = 같은 길이 법칙 · 같은 R_j"* | 같은 두 가닥 기하인데 fid 가 같으냐로 접합이 갈린다.  (i) 두 다리 중심선 1.2 > D 1.1 (닿지 않음 · 면 인접 셀): 같은 fid = 자기 접합 1 (L_c 0 · 배율 1) · σ **6.13208** (R_j = ∞ 이면 5.88235 · **+4.25 %**) ↔ 다른 fid = instance **0** (미등록 면 4 · cut).  (ii) 두 다리 중심선 **0.14142 < 2 r_f 1.0** (닿음 · 모서리 인접 셀 · 공유 면 없음 · 호 길이 먼 쪽): 같은 fid = 두 다리 사이 자기 접합 **0** ↔ 다른 fid = instance **1** (L_c 2.98995 · 배율 1.495).  같은 셀 · 면 인접 셀은 중심선이 h√3 ≈ 0.26 · h√6 ≈ 0.37 µm 떨어져도 자기 후보다 (서로 다른 섬유 D = 0.15 + tol_ff — tol_ff 0.03 이면 0.18 µm · tol_ff 숫자는 S0 뒤 등록). | 자기 후보도 서로 다른 섬유와 같은 중심선 근접 검사 (선분 쌍 `d ≤ D` · 호 길이 s 로 같은 가닥 연속을 거른 뒤) 로 정하고, 셀 인접은 후보 출처로만 쓴다.  UNREG (fused) 감도가 자기 접촉에는 걸리지 않는 것도 같이 적는다.  시험 = (i) · (ii) 두 꼴 · fid 같음/다름 σ 대조 |
| **PRE-impl-03** | P2 | 포트 = 조각의 **살아 있는** 위치 중 r_port 안 최근접 (`:1249` · `:1282`) — 접점 셀이 다른 상으로 덮이면 다른 셀로 옮겨 붙는다 · `ca_ext_cjunc.py:157` 이 cjunc + `centerline` (P0) 을 받는다 | ① **Rayleigh 위반 (centerline)**: F2 꼴 (A 위끝 ↔ B 아래끝 접점) 에 A 위끝 셀만 지나는 PTFE 피브릴 (centerline → 그 셀 sid 7) 을 **더하면** 포트 (1,1,3) → (1,1,2) 로 옮겨 σ **5.55556 → 5.88235 (+5.88 %)** = 손 회로 (A 축 면 하나 빠진 짧은 길).  같은 침대 옛 경로 = 11.1111 → **0.0** (PTFE 가 끊는다).  절연체를 더해 σ 가 오른다.  ② **등록 런 (face_alpha) 에서도 같은 기구 — SDCP 덮임 (DBE)**: 같은 접점 셀을 SDCP 점 스탬프가 덮으면 포트가 (1,1,2) 로 옮겨 접합이 SDCP 셀 SV 융합 경로와 **병렬로 한 번 더** 들어간다 — σ 12.15352 vs SV 경로만 11.90476 (**+2.09 %**) · 두 값 모두 손 회로 (SV 두 면 · 옮긴 접합 유무) 와 출력 자리까지 같음.  SBE (SDCP 없음) 에서 보정한 R_j 가 DBE 에서만 이렇게 두 번 세인다. | 접점 셀이 덮이면 옮기지 말고 미실현 (`covered_*` 사유 · 수 기록) 으로 두거나, 옮김을 같은 가닥 · 같은 국소 구간 (접점 호 좌표 ± r_f) 으로 묶고 SV 융합과의 이중 계상을 명시.  centerline + cjunc 는 Rayleigh 를 지킬 때까지 정량 거부 (off · face_alpha 만).  시험 = ① · ② 두 꼴 · "PTFE 를 더해 σ 증가 없음" 을 centerline 에도 |
| **PRE-impl-04** | P2 | `sv_counterfactual` `:2033-2072` — 부류 `sv_face` (VGCF\|SDCP 면) 를 **전부** 끊고 단자 G 비 | 섬유 하나 (접합 0 · VV instance 0) 가 SDCP 점 셀 하나를 지남 (생산 규약 = SDCP 가 VGCF 셀을 덮는다): 비 = **∞** (`no_through_without_sv`) · `SV_DEPENDENT` (문턱 2.0).  F1 (접합 1) 에 접합에서 먼 A 셀 하나만 SDCP: 비 **∞** · `SV_DEPENDENT` (SDCP 없으면 비 1.0).  이 노브는 "SV 융합 우회가 VV 접합을 대신하는가" 가 아니라 "SDCP 가 덮은 섬유 연속을 포함한 SV 면 전체 의존" 을 잰다 → SDCP Ø1 µm DBE 침대에서는 거의 늘 ∞ (판정 문장 늘 제한 · 정보 없음 · 추정). | Codex RCA-06 최소 해결의 "역할이 분리된 표현" 을 반사실에도 — 서로 다른 섬유를 잇는 SV 면 (SDCP 성분이 두 fid 이상에 닿는 것 · `_sdcp_bridging` 이 이미 셈) 만 끊고 같은 섬유의 SDCP 통과는 남기는 판, 또는 대안을 "SV 접촉 저항 유한" 으로 정의.  지금 노브의 뜻을 기록 · 등록 문턱 전에 시험 = 위 두 꼴 (비 = 1 이어야 하는 꼴) |
| PRE-impl-05 | P3 | `_n_sub` `:1367-1373` (k = ceil(L_c/L_par) · 1e-9 띠) · 분산 간선 자리 = 닿음 구간 k 등분 가운데 점 | 깊은 교차를 90° → 89.99° 로 기울임 (L_c/L_par = 1.0000000152 · sid 같음): k 1 → 2 · 배율 차 1.5e-8 인데 σ 가 뛴다 — 시험 단위 **−1.049 %** (4.347826 → 4.302204) · 생산 단위 R_j 1e2 Ω **−0.978 %** · 1e4 Ω **−2.10e-4** · 1e6 Ω **−2.11e-6**.  원인 = 반쪽 간선이 셀 경계 (±L_c/4 = ±h/2) 로 가 사전식 최소 셀로 옮겨짐.  깊은 교차 (d0 ≈ 0) 의 L_c/L_par = 1/sin θ 라 비직교면 k ≥ 2 (k = 1 = 옛 점 접합은 정확한 직교뿐 · 분석 — 실침대 분포 미확인). | 이산화 오차로 기록 (분산판 v0 = 계단 근사 · 경계 불연속 크기 ∝ h·r′/R_j) · origin · SVORDER 비교에서 이 뜀이 잡음으로 섞임을 한정어로.  필요하면 경계 연속 배치 (k 바뀌어도 간선 자리가 연속) |
| PRE-impl-06 | P3 | `PRE-impl-01` 과 같은 뿌리 (닫힌 경로의 첫 · 끝 위치 = 비연속 재방문) | 닫힌 고리 (이음매 = 왼 다리 z 4.2) — 손 회로 연속 고리 = 옛 경로 **25.6410** · s ≥ s_min: 이음매 = R_j 접합 → **18.4735 (−27.95 %)** · s < s_min: 이음매 끊김 → **12.9310 (−49.57 %)**. | 닫힌 경로는 첫 · 끝 위치를 축방향으로 잇는다 (또는 정량 입구에서 거부 · 수 기록) |
| PRE-impl-07 | P3 | `run_contract.py:756-787` · `:850-868` — 영값 증서의 `fp_sid` · `fp_sig` 는 hex 32 형식만 · σ 결합 (0 = 0) 은 아무것도 묶지 않는다 | CX 바닥 (R_j = ∞) 의 실제 영값 증서에서 지문만 바꾼 사본 → `conv_cert_problem` = None · `next_gen_cert_ok` = (True, None).  대조할 칸은 있다: 증서 `fp_sid` = 접합 원장 `ca_ext.cjunc.evidence.fp.sid` (같은 함수 · 실측 `c83492d6…` 같음). | 영값 증서 `fp_sid` ↔ 매니페스트 `ca_ext.cjunc.evidence.fp.sid` (조합 런 = `ptfe_face.evidence.fp.sid_off` 도) 대조 · 양의 증서에도 같은 지문 칸 (지금은 σ 1e-9 결합뿐) |
| PRE-impl-09 | P3 | `test_carbon_junction.py:2853` (MUT-RCA 변이 `cf_nodrop(self, solve_, I_full, request)`) ↔ 생산 호출 `sv_counterfactual(..., certify=…)` (`step3_sigma.py` · 10-21 위생 커밋 `2da0f63d0` 이 키워드를 보탰다) | 시험에 적힌 변이 = `TypeError: cf_nodrop() got an unexpected keyword argument 'certify'` → `_try` 가 None → 비 NaN → "잡음" (옳은 이유 아님).  서명만 맞춘 같은 변이 = 비 **1.0** (기준 **10.291253935345084**) → 검사 자체는 판별력 있음 (`probe_mut_cf.py`). | 변이 서명을 `certify=None` 까지 받게 고치고, 변이에서 예외가 나면 "잡음" 이 아니라 하네스 실패로 센다 (T18 의 '기준선 통과 단언만' 규칙과 같게) |
| PRE-impl-08 | P3 | `ca_ext_cjunc.py:57` `LABEL_CJUNC` (웹앱이 띄우는 유일한 문자열) ↔ 설계 v1 §4-6 줄 330 *"표지에 '긴 접촉 = 분산판 v0' · '같은 가닥 재방문 = branch 따로' · 'SV 소산 = 진단 — 지배 보증 아님 · 반사실 대조 비 따로' 를 보탠다 — 문구의 자리 = LABEL_CJUNC"* | `LABEL_CJUNC` 는 10-20 문구 그대로 (세 표지 없음) · 새 한정어는 `evidence.qualifiers` 에만 있고 템플릿은 `label` 만 띄운다 · `webapp/test_ca_ext_labels.py` 25/25 (W8c 는 사본 금지만 보고 내용은 안 본다). | 상수에 세 표지를 보태고 웹앱 시험에 내용 단언 (CLAUDE.md 코드 → 웹앱 순차 반영) |

## 3. 확인했지만 결함 아닌 것

- **ⓓ 의 수학 (손 분석)**: 상한 = 근사 φ 의 에너지 ≥ G* (Dirichlet) · 하한 = Σ q Δφ* = F_bot − Σ φ*_v d_v 와 Cauchy–Schwarz · 최대 원리 0 ≤ φ* ≤ 1 → G* ≥ (F − Σ max(d, 0))² / W (위 판 쪽도 대칭) — 코드의 식과 같다.  부동소수: 항 반올림 (U 항 4u · W 항 2u) 을 2 배로 · `math.fsum` (정확 반올림) · 뺄셈 · 나눗셈 · 마지막 곱의 여유 · 부정규 = NOT_CERTIFIABLE — 여유가 모자란 자리를 찾지 못했다.  하한 흐름은 φ 와 무관한 아무 흐름이어도 성립하므로 φ 를 조작해도 구간이 G* 를 놓치지 않는다 (가짜 후보 φ: 게시 0.25 · 구간 [0.33333, 0.375] → ⓓ 거부).
- **Codex RCA-07 반례 셋 (HEAD · 두 BLAS 경로)**: 주 (24 사슬) 상대 오차 +5.56e-4 (SkylakeX) / +5.12e-4 (Haswell) · 11 사슬 −1.890e-4 / −1.886e-4 · 연결 −9.037e-3 / −9.037e-3 — 여섯 모두 ⓐⓒ 통과 (11 사슬 SkylakeX 만 ⓑ 실패) · **ⓓ 실패 → ok False · 참 G* 구간 안** · 최종 판정 두 경로 같음.
- RCA-13 상태: 바닥 극한 = `no_through_component` → VALID_ZERO (ok · `conv_cert_problem` None) · 행렬 경로 영값 (Codex 두 노드) = VALID_ZERO · zero_exact.
- 끈 경로 = 기반과 비트 같음 (세 침대 · 생산 CG · 모든 결과 칸 sha256).  face_alpha 계획 지문 (`plan_fp`) 에 새 진단 `false_cut_check` 는 안 들어간다 (지문 불변).
- 극한 런은 `quantitative False` 여도 원장 거부 사유를 정량 런과 같게 막는다 (`ca_ext_cjunc.py` payload_prepare).
- 사슬 판본 섞임: 다시 계산한 p3ca id · `ca_ext_record_ok` (원장 규칙 판 · model 문자열) · 킷 접두 · sid 지문 무리 · 단계 코드 핀 — 자리 있음 · 시험 89/89.
- 상주 변이 (MUT-RCA · 실행 6/6): 포트 lexmax · 옛 k 규칙 · fid 순 경로 · k = 1 (한 포트 집중) · 재방문 합침 다섯은 손 회로 · 비트 대조로 잡힌다.  여섯째 (반사실이 SV 를 안 끊음) 는 `TypeError` 로만 잡힌다 → `PRE-impl-09`.
- `PRE-impl-05` 의 크기는 R_j 가 클수록 작다 (1e4 Ω 에서 2.1e-4) — 등록 사다리의 1e4 Ω 이상에서는 판정 문턱보다 훨씬 작다 (추정 · 합성 한 접합).

## 4. 탐침 · 재실행

폴더 `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_impl/` (리포 밖) · 모든 탐침은 `pcommon.py` (리포 함수 그대로 · 기대값 = 손 회로 `ref_I` · `chain_I`) 를 쓴다 · `PRE_REPO` 로 검토 트리를 바꿀 수 있다.

```
cd /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_impl
R='nice -n 19 env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -I'
$R probe_gap_revisit.py          # PRE-impl-01 (시험 단위)        → probe_gap_revisit.json
$R probe_gap_revisit_prod.py     # PRE-impl-01 (생산 단위)        → probe_gap_revisit_prod.json
$R probe_self_vs_distinct.py     # PRE-impl-02                    → probe_self_vs_distinct.json
$R probe_ptfe_monotone.py        # PRE-impl-03 ①                  → probe_ptfe_monotone.json
$R probe_sdcp_relocate.py        # PRE-impl-03 ②                  → probe_sdcp_relocate.json
$R probe_sv_cf.py                # PRE-impl-04                    → probe_sv_cf.json
$R probe_k_boundary.py           # PRE-impl-05 (시험 단위)        → probe_k_boundary.json
$R probe_k_boundary_prod.py      # PRE-impl-05 (생산 단위)        → probe_k_boundary_prod.json
$R probe_closed_loop.py          # PRE-impl-06                    → probe_closed_loop.json
$R probe_zero_binding.py         # PRE-impl-07                    → probe_zero_binding.json
$R probe_cert_codex.py           # ⓓ · Codex 반례 (기본 경로)      → probe_cert_codex_default.json
OPENBLAS_CORETYPE=Haswell $R probe_cert_codex.py   #  (Haswell)  → probe_cert_codex_Haswell.json   · 요약 python3 -I show_cert.py
$R probe_limits.py               # 극한 · 상태 (기본 → *_default · Haswell 로 한 번 더 → *_Haswell 로 이름 바꿈)
$R probe_cert_liveness.py        # ⓓ 생존성                       → probe_cert_liveness.json
$R probe_off_bitid.py            # 끄면 비트 같음 (기반 git archive) → probe_off_bitid.json
$R probe_b01_mutation.py         # RINT2-B01 변이                  → probe_b01_mutation.json
$R probe_mut_cf.py               # PRE-impl-09 (MUT-RCA 반사실 변이) → probe_mut_cf.json
# MUT-RCA 원 묶음:  python3 scripts/test_carbon_junction.py --only MUT-RCA  (6/6 · 여섯째 줄 위 '(예외 TypeError …)' 출력)
# 리포 시험 (읽기만):  python3 scripts/test_carbon_junction.py --only RCA03,RCA04,RCA05,RCA06,KINK-R  (36/36)
#                     python3 scripts/test_rint_r_chain.py (89/89) · python3 webapp/test_ca_ext_labels.py (25/25)
```

## 5. 못 본 것 · 이유

- 실침대 (재압밀 전 · S0 census 없음) — `PRE-impl-01` · `02` · `03 ②` · `04` 의 빈도는 미확인.  S0 단계 1 census 에 보탤 칸: 같은 셀에서 만나는 조각 끝 수 · 자기 후보의 중심선 거리 분포 (> D 몫) · 덮인 접점 셀 → 포트 옮김 수 · SDCP 가 덮은 섬유 셀 수.
- 게이트 창 (≤ 60 s · 한 프로세스) 때문에 돌리지 않음: `test_carbon_junction.py` 전체 (C0 · FP · PIECE4 등) · `test_step3_target_cert.py` (T5 탐색 · T17 OpenBLAS 여섯 경로 · T14 시간) · `test_ca_ext_z3.py` (A9 face_alpha 단조 — 시험이 있음만 확인) · `test_ptfe_face_alpha.py` · 실제 생산 → full payload → 축소 → 재판정 → 뷰어 통합.
- 3 번 이상 같은 셀 재방문 · 0 길이 선분 · 셀 경계 위 꼭짓점은 코드만 읽었다 (재방문 쌍마다 후보 · 퇴화 선분 처리 확인 · 수치 탐침 없음).
- 범위 밖 (다른 에이전트가 고치는 중): 사슬의 `sv_dominant` 읽기 · VALID_ZERO / ELECTRODE_SHORT 수용 · 등록 R 3 판 규칙 · SV 반사실 노브 배선 — `PRE-impl-04` 는 노브 **뜻** (설계 수준) 만 다룬다.
