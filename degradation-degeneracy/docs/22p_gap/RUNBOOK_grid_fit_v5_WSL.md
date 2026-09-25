# `grid_fit_v5` 한정 실행 runbook — WSL 로컬 (73차 조건부 GO, 원장 §98)

> 사용자 결정 2026-09-25: "wsl 에서 돌려도돼 로컬로 돌리자". 이 문서는 GATE71 §2 (E9-0~E9-6) + GATE72/73 §2 의 정정을 **WSL 한 기계**에
> 맞춰 명령 순서로 편 것이다. 규칙의 정본은 그 요청문들과 원장 §93·§95·§97·§98 이고, 여기는 순서표다.
> 코드는 바꾸지 않는다 — 판정 대상 `7a7945564e6a94803b4d3bc72e8202534189ccdb` · `source_digest c2ef1a811e70bb4c`.

## 0. 왜 WSL 에서 계획을 **다시** 뽑는가

계획 항목의 `run_spec.grid.discharged_cache_sha256` 은 **그 기계의 완방상태 캐시 바이트**를 묶는다 (51차 P0-A4). 컨테이너에서 뽑은 값(`00ebb05f…`)은
컨테이너 캐시의 것이라 WSL 에서는 gate 가 거부한다. 리뷰어 §6-1: "과거 문서의 dry 출력·구 source_digest·다른 기계 캐시 식별을 그대로 복사하지 않는다."
fresh clone 에는 캐시가 없으므로 값은 `null` 이 되고 그 뜻은 "이 실행이 계산한다 · 캐시 읽기 금지" 다 — 그것이 가장 단순한 결속이다.
**계획을 뽑은 뒤 실행 시작 전까지 pytest/smoke 를 돌리지 않는다** (캐시를 다시 쓴다 — 컨테이너에서 하루 사이 값이 바뀐 것을 실측).

## 1. checkout (WSL)

```bash
# WSL 셸. Windows git 의 autocrlf 가 RUN_SCOPE 바이트를 바꾸면 source_digest 가 달라진다 — WSL git 은 기본 false 지만 확인한다.
git config --global core.autocrlf false
git clone --branch claude/14-gate-code-review-9qkx05 <origin-url> ~/dd && cd ~/dd/degradation-degeneracy
git rev-parse HEAD                    # 브랜치 head (6d07eb44 이후)
git status --porcelain | wc -l        # 0 이어야 한다
git diff --quiet 7a7945564e6a94803b4d3bc72e8202534189ccdb HEAD -- src tools configs scripts run.sh requirements.txt requirements-gpu.txt && echo "RUN_SCOPE diff 0"
```

## 2. 환경

```bash
./scripts/setup_env.sh && source .venv/bin/activate          # docs/RESULTS.md §재현 그대로
./run.sh --mode verify                                        # 의존성·solver 확인
python3 -c "from src.io import source_digest; print(source_digest())"   # 반드시 c2ef1a811e70bb4c
nproc; df -h .                                                # 코어 수(10 h 추정은 코어 수에 따라 다르다) · 디스크(results/ 수 GB)
unset CANONICAL_RUN LEG DD_SMOOTH_CACHE                       # D8 — 상속 환경변수 제거 (DD_SMOOTH_CACHE 는 smoothing_backend 축, 52차 P0-6)
env | grep -E "CANONICAL_RUN|^LEG=|DD_SMOOTH" || echo "env clean"
```

`source_digest` 가 다르면 **멈춘다** (줄끝 정규화·부분 checkout 의심). 계획도 실행도 그 digest 위에서만 성립한다.

## 3. 계획 항목 생성 (출력만 — 원장은 사람이 쓴다)

```bash
python3 docs/22p_gap/plan_leg.py --leg grid_fit_v5 --cohort g18_2026_09_15 \
    --config configs/grid_fine.yaml --out results/grid_fit_v5 \
    --recorded-on $(date +%F) \
    --근거 "73차 조건부 한정 GO (원장 §98) — 현행 code identity 로 grid_fine 격자 grid/fit 재실행 (GATE71 §2 E9-0), WSL 로컬"
```

확인할 것: `authorized_source_digest: c2ef1a811e70bb4c` · `n_conditions 3993` · 목적함수 4 · `discharged_cache_sha256: null` (fresh clone) ·
`smoothing_backend` 값 · `in = out = results/grid_fit_v5` · `command` 줄. **출력 전문을 그대로 보관한다** (승인 근거).

## 4. 원장에 넣고 커밋 (= 승인 행위, 사람)

`docs/22p_gap/LEG_PRESERVATION.yaml`:
- `planned:` 목록 끝에 §3 출력 블록을 그대로 붙인다.
- `cohorts:` 의 `cohort_id: g18_2026_09_15` 항목의 `prospective_legs: []` → `prospective_legs: [grid_fit_v5]`.

```bash
python3 -c "from tools.preserve import assert_planned_index_consistent as f; print(f())"      # True
python3 -c "from tools.preserve import assert_planned_leg; from src.io import source_digest; print(assert_planned_leg('grid_fit_v5', source_digest())['recorded_on'])"
git add docs/22p_gap/LEG_PRESERVATION.yaml
git commit -m "dd: grid_fit_v5 prospective 계획 항목 — 73차 조건부 한정 GO 승인 (WSL, source_digest c2ef1a811e70bb4c)"
git push origin claude/14-gate-code-review-9qkx05
git rev-parse HEAD                    # = 최종 승인 HEAD. 실행은 이 HEAD 에서만.
```

(컨테이너 세션에 출력을 붙여 주면 거기서 넣고 커밋할 수도 있다 — 그 경우 WSL 에서 `git pull` 뒤 §5 로. 어느 쪽이든 커밋이 승인이다.)

## 5. 배타 운영 창 열기 (E6-b)

```bash
mkdir -p ~/grid_fit_v5_window && W=~/grid_fit_v5_window
git rev-parse HEAD > $W/approval_head.txt; git status --porcelain > $W/status_before.txt   # 비어 있어야
python3 - <<'EOF' > ~/grid_fit_v5_window/registry_before.txt
import hashlib,pathlib
for p in sorted(pathlib.Path("docs/22p_gap/_exec_class").glob("*.json")): print(p.name, hashlib.sha256(p.read_bytes()).hexdigest())
EOF
wc -l $W/registry_before.txt          # 367
ps aux | grep -E "run.sh|pytest|smoke_e2e|src\.(grid|fitting)" | grep -v grep || echo "no other publisher"
```

창 안에서 금지: pytest · smoke · 다른 `run.sh` · 커밋 · 원장 편집 · 캐시 재생성.

## 6. 실행 (E9-1)

```bash
cd ~/dd/degradation-degeneracy && source .venv/bin/activate && unset CANONICAL_RUN LEG DD_SMOOTH_CACHE
nohup ./run.sh --mode all --leg grid_fit_v5 --config configs/grid_fine.yaml --nproc "$(nproc)" --out results/grid_fit_v5 \
      > ~/grid_fit_v5_window/run_$(date -u +%Y%m%dT%H%M%SZ).log 2>&1 &
echo $! > ~/grid_fit_v5_window/run.pid; tail -f ~/grid_fit_v5_window/run_*.log
```

기대 순서: 실행 전 gate 통과(사전 점검·새 발급) → grid (~3993 조건) → gate 통과(소유한 재개) → fit (4 목적함수 × 3069 조건 × restart 5) → `✅ 실행 기록을 닫았다 — grid_fit_v5 … preservation_status=preservation_pending` → score → report `docs/RESULTS_grid_fit_v5.md`.

## 7. 실패 시 (E9-4 D6)

**즉시 정지.** 로그 전문 보존. 그 다음 사람이 확인:
```bash
python3 -c "from tools.preserve import precheck_leg_run; from src.io import source_digest; print(precheck_leg_run('grid_fit_v5', source_digest()))"   # kind == 'resume' 이어야
ls results/grid_fit_v5/ ; ls results/grid_fit_v5/fit_completed.jsonl 2>/dev/null   # 부분 산출 온전한가
```
같은 plan/token/source_digest 이고 부분 산출이 온전하면 **정확히 1회**:
```bash
nohup ./run.sh --mode all --leg grid_fit_v5 --config configs/grid_fine.yaml --nproc "$(nproc)" --out results/grid_fit_v5 --resume \
      > ~/grid_fit_v5_window/resume_$(date -u +%Y%m%dT%H%M%SZ).log 2>&1 &
```
2회째 실패 → 재승인(새 계획 항목). finalize/archive/영수증/attach 의 실패는 `--resume` 대상이 아니다 — 사유를 보존하고 게이트로.

## 8. 실행 뒤 — 보존·영수증·원장 (E9-3 2~5)

```bash
python3 - <<'EOF' > ~/grid_fit_v5_window/registry_after.txt
import hashlib,pathlib
for p in sorted(pathlib.Path("docs/22p_gap/_exec_class").glob("*.json")): print(p.name, hashlib.sha256(p.read_bytes()).hexdigest())
EOF
diff ~/grid_fit_v5_window/registry_before.txt ~/grid_fit_v5_window/registry_after.txt      # 기대: +2 (grid·fit) · 삭제 0 · 바뀜 0
ARCHIVE_DEST=artifacts ./scripts/archive_results.sh results/grid_fit_v5                     # 묶음 artifacts/grid_fit_v5
python3 docs/22p_gap/make_receipt.py grid_fit_v5                                            # 영수증 (empty-root 복원·재채점)
python3 -c "from tools.preserve import attach_bundle_evidence as f; print(f('grid_fit_v5','docs/22p_gap/receipts/grid_fit_v5.validate.yaml'))"
```
그 뒤 사람이 그 leg 의 `claim_roles`·`근거` 를 원장에 적는다 (docs-lint 요구). **창을 닫은 뒤에야** `python -m pytest tests/ -q` + `./scripts/smoke_e2e.sh`.
커밋: `artifacts/grid_fit_v5/` · `docs/22p_gap/receipts/grid_fit_v5.validate.yaml` · 원장 · `docs/RESULTS_grid_fit_v5.md` · `~/grid_fit_v5_window/*` 는 `docs/22p_gap/run_windows/grid_fit_v5/` 로 옮겨 커밋(로그 전문 포함).

## 9. 라벨 (GATE72 §1 그대로 — 실제 값으로 채운다)

실행 허용 범위 · 코드/입력/실행 식별(승인 HEAD · `c2ef1a811e70bb4c` · config · OUT) · 현지 검증(창 닫은 뒤 pytest/smoke 실측) · E1/E2/E4 한계 · E6 근거(전후 delta) ·
execution_class/보존/validation/inference_role 실제 값 · archive/복원/retention 수행·미수행 · 실패 처리 이력. `N/M` 없이.
