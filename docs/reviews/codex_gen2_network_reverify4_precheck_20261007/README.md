# 세대 2 · 194 등록 §1 WSL 사전 점검 결과 (10-07 14:15 KST · 1저자 · 재검증 4 요청서에 붙임)

- **무엇**: 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` §1 명령 블록 그대로 · 1저자 WSL · `~/dem-audit` detached `c3117438a` (dirty 0) ·
  Python venv numpy 2.5.2 · scipy 1.18.1 · networkx 3.7.  1저자 Q1 *"예"* (사전 점검을 돌려 재검증 4 요청서와 함께 보낸다).
- **원자료**: `g2pre_c3117438a_1007_1415.tar.gz` (21,825 B · sha256 `ba840f7e1cf3488686c3da27e8bcbad282c7d6234727c964c385e1bc7cfb58d7` · 9 파일 = 스모크 보고 · 요약 · 다시 읽기 /
  시범 manifest · 감사 TSV · JSON · 다시 읽기 · merge 보고 · progress) · 화면 = `wsl_terminal_c3117438a_1007_1415.txt` (1저자가 붙여 넣은 그대로 — 붙여 넣기 때 명령 줄
  메아리 한 줄이 섞였다 (`--casls -la …`) · 실행은 명령 블록 그대로: 시범 M3 = 세 케이스 기대 3 = 읽음 3).
- **우리 재현**: `case15_solver_direct_4950b2e79.log` (아래 §2 · 스크래치 경로는 `<scratch>` 로 바꿈).

## 1. 결과 ↔ 등록 기대 (결과 전 등록 — 고르지 않는다)

| 단계 | 등록 기대 | 결과 | 판정 |
|---|---|---|---|
| 0 | detached · dirty 0 | `c3117438a` · dirty 0 | 기대대로 |
| 1 | 다시 읽기 · 실행기 자체 시험 전부 통과 (17/17 · 100/100) | ✓ 전부 통과 · ✓ 전부 통과 (100/100) | 기대대로 |
| 2 | `code_fp e8b2496b…` (32) · 'g2' · 세 모드 · 전이 의존 30 ⊆ 32 · 지연 import 90 / 분류 밖 0 · 입력 지문 194 · `a04282d7…` · `da7c93f9…` · 결손 0 · 문제 0 · ⛔ 없음 | 전부 같음 | 기대대로 |
| 3 | `smoke rc=0` — real14 · case15 망 정지 done · LHS 셋 · 음성 대조 넷 PASS | **`smoke rc=1`** — 검사 23 · PASS 22 · **case15_network = failed** (Network Solver) · real14 · LHS 셋 · 음성 대조 넷 = 기대대로 | **기대와 다름 (case15)** |
| 4 | `reread rc=0` · real14 σ_ratio 참고 0.02102106 · 0.03164009 · 0.02494138 | **`reread rc=1`** (S0 — case15 failed) · real14 σ_ratio = 참고값과 **8 자리 같음** · τ 세 모드 OK · physics 협착-only not_computed · 네 케이스 K1–K7 ✓ | case15 때문에 다름 · 나머지 기대대로 |
| 5 | pilot · audit · reread rc 0 · SEALED 3 · g2 3 · 관측 영수증 (G2RR3-02) · 다시 읽기 JSON v3 · manifest 줄 2 + 2 | pilot rc 0 · audit rc 0 (SEALED 3 · merged same 3 · 레코드 g2 3 · 입력 지문 ✓ · **관측 = 프로세스 15 (시작 15 = 끝맺음 15) · 완료 시도 3 (역할 worker/network_solver) · 리포 모듈 30 ⊆ 32 ✓**) · reread rc 0 (M0 · M-plan · M-reg · M1–M3 · H1 lhs · lhsx ✓) · manifest 줄 2 + 2 | 기대대로 |

## 2. case15 실패 원인 (우리 컨테이너 재현 · 같은 원자료 · 같은 실패)

- 재현 = 커밋된 원자료 `docs/data/case15_corner_20261001/` 로 `scripts/wsl_network_smoke.py --skip-real14 --skip-lhs --skip-controls` (코드 `4950b2e79` = `c3117438a` + 문서만) →
  WSL 과 같은 실패 · 같은 사유.  파이프라인 기록 (`network_attempt.json` · 단계 err) 은 사유를 **끝 300 자만** 남겨 앞 채널이 잘린다 → 같은 입력 · 같은 인자로 망 풀이를
  직접 (`network_conductivity.py atoms.csv contacts.csv -o <mesh_info.json · input_params.json 사본> -t 1:AM_P,2:SE -s 1000 --contact-mode both`) 돌려 채널별 전체 로그를 얻었다.

| 채널 | Hertz | Physics (세대 2) |
|---|---|---|
| 이온 (SE–SE · 65,866 노드) | FULL σ/σ_bulk **0.000326** · CF 0.003922 · 협착-only 0.000357 (Codex 직접 풀이 0.00032635 과 같음) | FULL **0.000362** (Codex 0.00036225) · 협착-only = not_computed (관통 R_c = 0 간선 **312** — 등록 기대 그대로) |
| 전자 (AM–AM · 104 노드 · 바닥 56 · 위 52) | 띠 겹침 B ∩ T = **4 노드** → `boundary_overlap` (정확 Dirichlet 이 풀 수 없다 · 풀지 않는다) | 같음 |
| 열 (전 접촉 · 65,970 노드) | 띠 겹침 4 노드 → `boundary_overlap` | 망을 만들다 거부 — 간선 (31, 29241) 의 LIGGGHTS 접촉 면적 **−0.186036 µm²** < 0 → `physics_g2` ValueError (fail-closed) |

- **왜 겹치나**: case15 = 얇은 corner 침대 (판 간격 19.1455 µm · AM_P 반지름 6 µm · AM:SE 85:15 · P:S 10:0).  L0 띠 = 입자마다 z ≤ 2r (바닥) · z ≥ plate_z − 2r (위)
  (`network_conductivity.boundary_sets` · boundary_factor 2.0) ⇒ AM_P 는 중심이 7.1455–12 µm 이면 **두 띠에 동시에** 든다 (판 간격 < 4 r_AM).  이온 채널은 r_SE 0.5 µm → 띠 1 µm · 겹침 없음.
- **게시 규약** = WEB-03 Q1 (`e03c0a84b` · Codex 5 차 verified): 관통 성분이 있는데 풀지 못한 채널이 하나라도 있으면 망 게시 전체를 막는다 ⇒ 이온 값은 계산되지만
  게시되지 않고 τ 세 모드 = NOT_COMPUTED (missing_input).  **코드는 등록된 계약대로 움직였고, case15 를 done 으로 둔 등록 기대가 틀렸다** — 기대를 Codex 의 이온 단독
  직접 풀이에서 가져왔고 전자 · 열 채널과 게시 규약을 대조하지 않았다 (원장 `SELF-92`).
- **덤 관찰** (case15 값에는 영향 없음 — 띠 겹침이 먼저 걸린다): Hertz 경로는 접촉 면적 ≤ 0 이면 `a = 0` → `R = 1e12` (사실상 끊긴 간선 · 표지 없음) 로 두고, Physics 세대 2 는
  같은 간선을 거부한다 — 두 모드의 처리가 다르다 (`network_conductivity.py` `a_contact` · `R_Maxwell` 줄 · `physics_g2` 거부 줄).

## 3. 194 에 닿는가 (기록으로 본 범위)

| 조건 | 194 기록 | 근거 |
|---|---|---|
| 띠 겹침 B ∩ T | SE 띠 · AM 띠 겹침 **0 / 130 · 0 / 64** | `docs/data/lhs_perc_audit_20261001/lhs_20261001_d1ec42fba/perc_audit.tsv` · `docs/data/lhs_perc_audit_20261001/lhsx_20261001_d1ec42fba/perc_audit.tsv` (`se_overlap` · `am_overlap` · `harv_overlap` 열) |
| 열 채널 띠 겹침 | 따로 센 기록 없음 — 같은 입자별 L0 규칙이면 SE · AM 겹침 0 에서 0 이 따라 나온다 | `boundary_sets` (입자 자기 반지름으로 판정) |
| 음수 · 0 덤프 접촉 면적 | **0 / 194** (전 접촉 행 = `all` 묶음의 `n_area_dump_negative` · `n_area_dump_zero`) | `docs/data/lhs_descriptors_cov_1e09f661d/` · `docs/data/lhsx_descriptors_cov_1e09f661d/` (수확 v3) |
| 시범 셋 | lhs00_055 (관통) · lhs00_128 (정상 비관통) · lhsx_007 (관통) = 기대대로 | §1 단계 5 |

⇒ case15 의 두 실패 경로 (띠 겹침 · 음수 덤프 면적) 는 기록상 194 에서 일어나지 않는다.  ⚠ 194 본 실행의 실측이 아니라 같은 원자료에 대한 다른 감사의 수다.

## 4. 남은 것

- 판정문 §8-4 의 "원 rc 와 **전체** 출력": 등록 §1 명령이 tail · grep 을 쓴다 (rc 는 `PIPESTATUS` = 원 프로세스 rc) → ✅ 1저자 보충 묶음 받음 = §5.
- case15 를 스모크에서 어떻게 둘지 (음성 · 한계 사례로 둘지 · 얇은 침대 띠 규칙 · 채널별 게시) = 재검증 4 요청서 Q6 (Codex) — **스모크 기대를 결과를 본 뒤 고치지 않는다**.

## 5. 보충 묶음 (판정문 §8-4 · 10-07 · 1저자)

- `g2pre_extra_c3117438a_1007_1415.tar.gz` (18,719 B · sha256 `7161a2351d1425750d7ac32543f11694a898321ad6a2da2da586f9a3a3c037dd` · 44 항목) — 같은 체크아웃 `c3117438a` 에서:
  자체 시험 전체 출력 둘 (`g2_network_reread --selftest` rc 0 ✓ 전부 통과 · `run_network_194_parallel --selftest` rc 0 ✓ 100/100 — tail 없이 파일로) ·
  14:15 시범 ROOT 의 `import_obs/` (시작 영수증 15 = 끝맺음 로그 15 · 관측 훅 sitecustomize 사본) · 묶음 안 실행 기록 run_001 (3 케이스 done · 봉인 깨짐 0 · 최대 동시 3) ·
  케이스 `worker.json` · `log.txt` (lhs00_055 · lhs00_128 · lhsx_007).
- 같은 날 14:36 1저자 WSL 재실행 (`4950b2e79` = `c3117438a` + 문서만 · 단계 1–4) = 14:15 와 같은 결과 (case15 failed · 나머지 기대대로) — 화면만 · 묶음 없음 · 단계 5 는 붙여 넣기가 끊겨 돌지 않았다.
