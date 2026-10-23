# 묶음 A″ 보고 — C1 정상 기록 거짓 거부 (FLOAT) 고침 (Rint ② RR · 10-23 · 1저자 Q17 (가) · Q18 (가))

> 옮겨 적음 = 메인 (10-23) · 원문 = 작업 트리 에이전트의 마지막 보고 (지시서 `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF.md` §보고 · 묶음 A″ 지시 = `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF_A3.md`) ·
> 메인 메모 = 맨 끝 절.  숫자 · 전칭은 에이전트 실행 출력이다 — 메인이 다시 돌린 것은 메인 메모에 따로 적는다.

FLOAT 기록을 이제 받습니다.  바꿔 끼우기 반례 (A2) 는 그대로 거부합니다.  회귀는 전부 rc 0 입니다.
- 가지 `rr-fix-a3` · 시작 `7799a2ff6` · 끝 `a32fcf32f` · 커밋 3.
- push · fetch · check_all 은 하지 않았습니다.  사본은 다 지웠습니다.

## 1. 커밋 (메시지마다 `author 10-23 ratified Q17-Q18 (가)` + 끝 두 줄)

| 커밋 | 무엇 |
|---|---|
| `e91a1f65e` A13 | 생산자 새 칸 `n_reach_pairs_cut` (아래 끝 · 위 끝) · 검증기 ⑥ 을 새 칸으로 · ⑧ 새 칸 ↔ 옛 칸 관계 · 새 칸 꼴 검사 · 시험 QD7 · S8h″ · SM2 · 사슬 고정물 · 등록 R 머리 줄 + §5-6 C1 단락 |
| `d474ea0c5` A13b | 변이 생존 둘 (P8 · V13) 상주 시험 (UPLATE · QD2 ① 위 끝 bool) · (a′) (b′) 한정 시험 · 주석 · 등록 R |
| `a32fcf32f` A14 | 원장 RCA2-04 |

## 2. 고친 내용 (Q17 (가))

**새 칸** (`scripts/carbon_junction.py` `_reach_pairs_cut`):
- 뜻: 판에 닿는 성분에 있는 dof 쌍 중, 그 끝에서 잇는 간선이 모두 빠진 쌍의 수.
  - 판에 닿는 성분 = 주 해 그래프 (끊기 전) 에서 판 결합이 있는 성분.  `kept_c = bot_c | top_c` 와 같은 규칙입니다.
- 병렬 간선은 한 쌍으로 셉니다.  증서 `target_n_edges` (상삼각 쌍 수) 와 같은 셈입니다.
- 위 끝도 같은 셈입니다.  판에 닿는지는 판 결합을 빼기 **전** 결합으로 판정합니다.
- 노브를 끈 주 경로에서는 계산하지 않습니다.

**검증기** (`scripts/ca_ext_svcf.py` `_topo_problem`):
- ⑥ 아래 끝: 새 칸 0 인데 증서 위상 수 ≠ 주 해 → 거부.  새 칸 > 0 인데 = 주 해 → 거부.
- ⑥ 위 끝: (새 칸 + n_plate_couplings_cut) 로 같은 판정.
- ⑧ 생산자가 보장하는 관계만 대조합니다 (등식 없음): 아래 끝 새 칸 ≤ n_sv_faces_cut, 아래 끝 새 칸 ≤ 위 끝 새 칸 ≤ 아래 끝 새 칸 + n_edges_cut.
- 새 칸 = 0 이상 정수 · int64 범위.  `_removed_problem` · `MISMATCH_EMPTY_KEYS` 에도 넣었습니다.
- ①–⑤ · ⑦ 은 그대로입니다.  옛 ⑤ 는 새 ⑥ 이 함의하지만 남겨 두었습니다.

**한 정의로 셋이 다 맞습니다** (FLOAT · 병렬 간선 · 위 끝 FLOAT).  그래서 이 점은 결정 필요가 아닙니다.
- QD7 ① 13 기록과 ⑦ 80 기록 모두 "새 칸 (+ 판 결합) > 0 ⇔ 위상 수 ≠ 주 해" 가 성립합니다.  어긋남 0.

## 3. 시험 수 (끝 판 시험을 `7799a2ff6` 코드에 얹음 → 끝)

| 시험 | 고치기 전 | 끝 |
|---|---|---|
| test_carbon_junction QD7 (새 41) | 1/41 (통과 = ⑥ 한정 (c)) | 41/41 |
| test_carbon_junction 전체 | 399/399 (옛 시험) | 440/440 |
| test_ca_ext_b6 | 449 PASS / 5 FAIL (S8h″ 3 · SM2 2) | 454/454 |
| test_rint_r_chain | 240/240 (고정물 새 칸 4 · 10 = 옛 코드도 받음) | 240/240 |
| test_rint_r_chain_e2e | — | 16/16 |

QD7 의 꼴:
- ① 생산자 기록 13 = 계약 None + 관계: SVX · QD2 ①②③ · QD4 · 다섯째 rail · QDX · QD11R · FLOAT · 병렬 간선 (c 1 · c 없음) · 위 끝 FLOAT · UPLATE.
- 받음: ② FLOAT · ③ 병렬 간선 · ③′ 위 끝 FLOAT · ③″ UPLATE (위 끝 새 칸 6).
- 거부: ④ A2 · QD2 ③ 위 끝 바꿔 끼우기 · ⑤ 새 칸 꼴 · 관계 위반 17.
- 받음 확인 (한정): ⑥ (a) (b) (c) · ⑥′ (a′) (b′).
- ⑦ 모티프 침대 80 기록: 위 끝 computed 56 · c 1 축약 25 · 옛 판정이면 거짓 거부 (아래 31 · 위 16) · 어긋남 0.

사본 탐침 (리포 밖 · 지움): 600 기록 · 관계 어긋남 0 · 옛 판정이면 거짓 거부 아래 155 · 위 77.

## 4. 회귀 (코드 `d474ea0c5` = 끝과 같은 코드 · 전부 rc 0)

- chain 240 · e2e 16 · b6 454 · carbon_junction 440.
- runner 128 · z1 95 · z3 84 · verdict 31 · s0 152.
- target_cert 빠른 판 260/260 · `--long` 309/309 (heavy.sh).  T17c3 생략 = 이 기계에서 OpenBLAS 경로가 안 바뀜.  T18 변이 37.
- conv_cert 27 · ptfe 242 · run_contract `--selftest` 124 · step3 `--selftest` · `--selftest-rint` PASS.
- `check_method_discipline` 오류 0 (경고 17) · `--selftest` 128/128.
- 웹앱 `webapp/test_*.py` 51 파일 전부 rc 0 (ca_ext_labels 84 · rint_explainer_page 62 · rint_scope_labels 31).

## 5. 끈 경로 (`7799a2ff6` scripts 사본 대비)

- b6 `--old-scripts --only=B` 30/30: payload 일곱 꼴 모두 허용된 칸 0.  B0 영수증 44 · B0b 34 짝이 같습니다.
- z3 `--old-scripts --only=O` 11/11: O1 face_alpha 의 σ · n_dof · cg_info · resid 가 비트 같습니다.  O2 payload 여섯 꼴은 허용된 칸 0.
- SV 켬 (`--step3-cjunc-sv-cf` · rtol 1e-12 · fixture DBE · unsplit z 6.5 · z 12.5):
  - σ 같음 (0.00043695843728313 · 0.039231639340228545 · 0.03922245385285839).  n_dof 같음 (3338 · 3345 · 3341).
  - 차이는 더해진 칸 `…sv_counterfactual.n_reach_pairs_cut` 뿐 (1 · 2 · 1 개).  바뀐 칸 0 · 빠진 칸 0.

## 6. 변이 표 (한 줄 되돌림 24 · 끝 판 사본 · QD = QD7+QD5 73 단언)

| 되돌림 | 결과 |
|---|---|
| 생산자 P1–P10: 아래 · 위 칸 안 실음 · 병렬 간선 합침 끔 · 판에 닿음 거름 끔 · 아래 · 위 판 표시 줄 · keep0 을 끊은 뒤에 · 위 끝 판 결합 다시 셈 끔 · 끝점 표시 한 줄 · keep0 안 만듦 | QD 37 · 52 · 70 · 68 · 69 · 72 · 59 · 72 · 70 · 50 /73 = 10/10 잡음 |
| 검증기 V1–V13: 꼴 검사 둘 · ≤ c · 0 → 같음 · > 0 → 다름 (옛 c 로 / 끔) · 위 끝 관계 · 하한 · 상한 · 위 끝 0 → 같음 · 옛 끊은 수 · > 0 → 다름 · `_removed_problem` 새 칸 | QD 66 · 72 · 72 · 67 · 69 · 72 · 70 · 72 · 71 · 72 · 68 · 70 · 72 /73 = 13/13 잡음 |
| V14 `MISMATCH_EMPTY_KEYS` 새 칸 | QD 73/73 · b6 452/454 (SM2 2) = 잡음 |

- 첫 판 (A13 시험) 은 22/24 였습니다.  생존 P8 · V13 은 다른 검사에 가려졌습니다.
- A13b 상주 시험 뒤 24/24 입니다.  기준선 = QD 73/73 · b6 454/454.

## 7. 탐침 재실행 (무변경 사본 · `RINT_REVIEW_SOURCE` = `7799a2ff6` 사본 ↔ 끝 트리)

**사전 공격 리뷰** `docs/reviews/rint2_rr_fix_evidence_20261023/preattack/tools/atk_sv.py`:

| 공격 | `7799a2ff6` | 끝 |
|---|---|---|
| A1 ×5 | 계약 None | 계약 None · 구간 같음 |
| A2 정상 SVX | None · [SV_DEPENDENT] | 같음 |
| A2 아래 끝 ← 주 해 증서 | 거부 (C1 · 끊은 다리 면 2 · (44, 44, 1, 1)) | 거부 (C1 · 묶음 A″ · 판에 닿는 성분에서 끊은 쌍 2) |
| A3 칼날 다섯 · A4 18 | — | 둘 다 같음 · A4 18 거부 · 문장 같음 |

**Codex 판정문 탐침** (`docs/reviews/codex_rint2_rereview_evidence_20261022/` 사본):
- registration: 둘 다 rc 1 (ARM_UNREADABLE · R 단조 절 · REPORT_A2 §6 과 같음).
  - preattack `reg_each.py` (함수 10): 둘 다 ok 7 · Stop 3.  61 exact · 다름 0.
- certificate: 707 exact · 다름 0.  selected tests: 202/202 둘 다.
- geometry: 1067 exact.
  - 다름 2 = source sha256 (`carbon_junction.py` · `ca_ext_svcf.py`).
  - 더해진 칸 11 = 기록의 새 칸.  판정값은 같습니다.
- provenance: 37 exact · type 4 = F1 head · dirty (옛 사본은 git 밖 = 환경 차).
- s0: 34 exact.

**C1 한계 탐침** (생산자 실기록):

| 꼴 | `7799a2ff6` | 끝 |
|---|---|---|
| FLOAT (끊은 다리 면 2 · 판에 안 닿는 섬 · 아래 끝 증서 = 주 해 (11, 12, 1, 1)) | 거부 (옛 ⑥) | None · [] (원래 판정) · 새 칸 0 |
| (a) SVX 아래 ← 주 해 증서 + n_sv_faces_cut 0 | None · [] | 새 칸 2 남김 = 거부 · 새 칸도 0 = None · [] |
| (b) QD2-3 위 ← 주 해 증서 + n_edges_cut 0 | None · [] | 위 끝 새 칸 6 남김 = 거부 · 새 칸도 0 = None · [] |
| (c) QDX 위 ← 아래 끝 증서 | None · [] | None · [] |
| (a′) · (b′) 새 칸만 0 (옛 칸 그대로) | — | None · [] |
| QDX 아래 ← 주 해 증서 + 새 칸만 0 | — | 거부 (위 끝 8 ∉ [0, 6]) |

Q18 (가) 에 대한 답:
- (a) · (b) 는 이제 새 칸까지 0 으로 고쳐야 받습니다.  옛 칸만 고치면 ⑧ 이 거부합니다.
- (c) 는 지금처럼 받습니다.

## 8. 문서 · 원장 · 기타

- **등록 R** `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md`: 머리 줄 (묶음 A″) · §5-6 SV 행 C1 단락 (옛 한정 문장 취소선 → 새 단락).
- **코드 문서**: `scripts/ca_ext_svcf.py` 모듈 머리 · `_topo_problem` (①–⑧ · ⚠), `scripts/carbon_junction.py` `_reach_pairs_cut` · `sv_counterfactual`, `scripts/test_carbon_junction.py` QD7.
- **원장** `docs/reviews/findings.json` RCA2-04:
  - note 끝에 지시서 문장을 넣고 정의 · 변이 · 한정을 붙였습니다.
  - evidence_tests 4 줄 추가 · claimed_fixed_sha `5cf848157` → `e91a1f65e` · 새 ID 없음.
  - 커밋마다 `check_doc_refs` · `check_review_findings` rc 0.
- **`S0_SAME_FILES`**: 일곱 중 바뀐 것은 `carbon_junction.py` 하나입니다 (sha256 f80aa0e3… → 2ad37531…).  S0 단계 1 보고는 끝 핀에서 다시 만들어야 합니다.
- **봉인 32**: 바뀐 7 파일 중 0.
- **웹앱**: 해당 화면 없음 (`webapp/` 에 끊은 수 칸 이름 0 곳).

## 9. 결정 필요 (지금 동작 유지 · 고르지 않음)

1. **(a′) · (b′) 를 받습니다.**  새 칸만 0 으로 고친 바꿔 끼우기는 정직한 FLOAT · 위 끝 FLOAT 기록과 같은 꼴이라 기록 안에서 가를 수 없습니다.
   - 위 끝 풀이 기록이 있으면 ⑧ 이 아래 끝 편집을 잡습니다 (QDX).
   - Q18 의 (a) (b) (c) 밖의 새 꼴입니다.  Codex 회차 ① 한정에 넣을지 정해 주세요.
2. **판에 닿음을 어느 그래프에서 판정하나.**  `kept_c` 규칙을 주 해 그래프 (끊기 전) 에 적용했습니다.
   - 이유: 끝 그래프에서는 빠진 쌍이 속한 성분이 없습니다.
   - 위 끝은 판 결합을 빼기 전 결합으로 판정합니다 (UPLATE).
   - 지시서의 "kept_c 와 같은 판정" 이 이 뜻인지 확인해 주세요.
3. **새 칸 이름** `n_reach_pairs_cut` 을 확인해 주세요.
4. **새 칸 꼴 검사 범위.**  위상 대조 밖 끝 (+∞) 에도 정수를 요구하고, census 불일치 기록에서는 비어야 합니다.  옛 칸과 같은 대우인데, 이대로 둘지 확인해 주세요.
5. **비용.**  SV 켬 런에서 끝마다 연결 성분 계산이 한 번 더 듭니다.  실침대 시간은 재지 않았습니다.

---

## 메인 메모 (10-23)

- **병합**: fast-forward `7799a2ff6` → `a32fcf32f` (커밋 3 · SHA 그대로 · 원장 `claimed_fixed_sha` `e91a1f65e` 도달 가능).
  - 봉인 32 ∩ 바뀐 7 파일 = 0 — 메인이 `scripts/run_network_194_parallel.py` 의 `CODE_FILES` 로 다시 셈.
  - 전체 게이트 = 이 보고 커밋에서 (결과는 진행 기록 10-23 줄).
- **§9 결정 필요의 처리**:
  1. → **1저자 Q19** (권고 (가) = Codex 회차 ① 요청서의 한정에 넣는다 · Q18 (가) 와 같은 부류 = 끊은 수 칸을 맞춘 편집).
  2. → 메인 확인 — 지시서의 *"kept_c 와 같은 판정"* 은 주 해 그래프 (끊기 전) 에 그 규칙을 쓰라는 뜻이다 (끝 그래프에는 빠진 쌍의 성분이 없다).
     - 메인 추론 (실행 출력 아님): 끊기 전 판에 안 닿는 성분은 끊어도 판에 안 닿는다 → 거기서만 끊으면 끝 증서 = 주 해 증서.
     - 판에 닿는 성분의 쌍이 하나라도 빠지면 끝 증서의 쌍 수가 준다 → 위상 수가 다르다.
     - 실행 출력 근거 = §3 QD7 ⑦ 80 기록 · 사본 600 기록 어긋남 0.
  3. → 지시서가 이름을 에이전트에게 맡겼다 (*"이름은 기존 칸 꼴을 따라 네가 정한다"*) — `n_reach_pairs_cut` 그대로.
  4. → 지금 동작 유지 (옛 칸과 같은 대우) · Codex 회차 ① 요청서에 적는다.
  5. → 묶음 C 시간 표 (Q9 · 실침대 시간 미측정) 로 넘긴다.
- **Q18 (가) 한정 문장 바뀜**: (a) · (b) = 이제 옛 칸 · 새 칸을 **모두** 0 으로 맞춘 편집만 받는다 · (c) 그대로 · (a′) · (b′) = 새 꼴 (Q19).
- **S0**: `S0_SAME_FILES` 일곱 중 `carbon_junction.py` 가 바뀜 → S0 단계 1 보고는 R 끝 핀에서 다시 만든다 (지금 단계 1 = 개발 자료).
