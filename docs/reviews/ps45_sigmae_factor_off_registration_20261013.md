# ps45 σ_e 인자 끔 다섯 전자 망 진단 — 결과 전 등록 (10-13 KST · 보고 전용 실행 변형 · 결과 0 건)

> **왜**: Codex 10-13 판정 `docs/reviews/codex_review_ps45_sigmae_reporting_20261013.md` §3-3 · §4 (가′) · §8 — *"새 결과를 보기 전에 Hertz H0 + PC 인자 OFF + 공통 기준값 4.1 이라는
> 보고 규약과 다섯 case ID 를 고정한다 … 원 기하 · 접촉은 유지하고 다섯 전자 망만 별도 진단한다"*.  원장 `PS45E-03` (P2 · 예방 조건 — 실행 중 교체한 모형은 자기 manifest 를 가져야 한다) ·
> `PS45E-01` · `PS45E-02` (표기).  수치 근거 · 문헌 대조 = `docs/data/ps45_r45_network_g2_20261007/README.md` §σ_e (10-13 판정 반입판).
> **범위**: 보고 그림 한 장 (2차년도 보고 덱 p15 σe− 막대) 의 기준.  **생산이 아니다** — 194 · 보충 20 · v1.3 · 봉인 32 (`code_fp e8b2496b…`) · 웹앱 · 저장된 생산 JSON · TSV ·
> 상태는 바꾸지 않는다 · 새 DEM 없음 · 이온 · 열 망 안 푼다.
> **상태**: 결과 0 건 (이 문서 · 실행기를 쓰는 동안 실침대 망을 한 번도 풀지 않았다 — 컨테이너에는 원자료가 없다) · ⬜ 1저자 비준 → WSL 실행 (§5) → 결과 반입 → (필요하면) Codex 짧은 확인.

## 1. 보고 규약 (결과 전 고정 — 결과를 본 뒤 바꾸지 않는다)

| 항목 | 고정 값 |
|---|---|
| 주 값 | **Hertz H0** — Maxwell 협착 · 원기둥 bulk · 정확 Dirichlet 전극 (세대 2 코드 그대로 · `contact_mode='hertzian'`) |
| PC 크기 인자 | **끔** — 모든 AM 입자 σ_rel = 1 (`network_conductivity.sigma_AM_relative` 를 실행 중 상수 1 로 교체 · 파일 무변경 · 끝나면 되돌림) |
| 공통 기준값 σ_ref | **4.1 mS/cm = 0.0041 S/cm** (PC · SC 같음) — 이름표: *"20 °C NMC811 소결 (SPS) 다결정 펠릿 문헌 (Wang 2018) 의 약 4 mS/cm 를 참고한 지정 참조값 · 조건부"* (우리 PC · SC 각각의 실측값 아님 · 4.1 의 정확한 문장 · 시료 조건은 원문 재확인 전) |
| 보고 양 | σ_e,eff = q × 4.1 mS/cm · **q = σ_eff / σ_ref 병기** (= 공통 상 전도도 아래 기하 · 접촉 · 경계 모형 응답 — 기하만의 관측값이 아니다) |
| 다섯 케이스 (`docs/data/ps45_r45_network_g2_20261007/network_cases.tsv`) | 0:10 `260925_000001_0bee25` · 3:7 `260925_000448_bd85f9` · 5:5 `260925_000513_123978` · 7:3 `260925_000559_082983` · 10:0 `260922_222828_6e4ff6` |
| 등록 감도 | **Physics g2** (native AM–AM 원판 + ψ 곱셈 협착 — Tabor 아님) · 인자 끔 · 같은 σ_ref — 별도 열 · 주 값 대체 금지 |
| 보존 감도 (기존 해 · readout-only) | 인자 켬 × 4.1: Hertz 0.390802 · 0.235799 · 0.158887 · 0.108846 · 0.106783 · Physics g2 0.507671 · 0.319762 · 0.220523 · 0.154004 · 0.137301 mS/cm (Codex 재구성 · 우리 재현 같음) |
| 보고 범위 | **다섯 모두** — 비단조 · 문헌보다 낮거나 높아도 · 실패 상태는 상태 그대로 (값 칸 비움) · 섞인 세 침대를 보간 · ×4.375 · 평균 인자로 채우지 않는다 · 문헌에 가까운 모드 · 조성을 사후 선택하지 않는다 |

- 결과 전 기대 (관문 · 기록용 — 판정 기준 아님): 0:10 (SC 만) 인자 끔 = 켬 **비트 같음** (G4) → Hertz 0.390802 · 10:0 (PC 만 · 균일 반경 4.5 µm) OFF/ON = 35/8 이면
  Hertz **0.467175** (Codex §3-2 끝점 산술 — 0 면적 · ψ floor · 가드가 끼면 다를 수 있다 → 관측값 그대로) · 섞인 셋 = **예측 없음** (그래서 푼다).

## 2. 팔 (케이스마다 넷 · `scripts/ps45_sigmae_factor_off_variant.py` 의 `ARMS` 상수)

| 팔 | contact_mode | PC 인자 | σ_bulk (S/cm) | 역할 |
|---|---|---|---|---|
| `control_hertz_on` | hertzian | 켬 | 0.05 | 관문 — 저장된 g2 증서 q 재현 (입력 · 코드 결합) · 보고값 아님 |
| `main_hertz_off` | hertzian | **끔** | **0.0041** | **주 값** |
| `control_physics_on` | physics | 켬 | 0.05 | 관문 |
| `sens_physics_off` | physics | 끔 | 0.0041 | 등록 감도 |

- 호출 = `network_conductivity._run_all_networks` 의 전자 호출과 같은 인자: `run_decomposition(atoms, contacts, am_types, scale, plate_z, box_x, box_y, sigma_bulk=…, type_map=…,
  contact_mode=…, mode='electronic')` · ψ 배치 · 면적 규칙 = 모듈 기본 (multiply · physics_g2) · 입력 = 망 솔버 CLI 가 읽은 그 파일 (`atoms.csv` · `contacts.csv` · `mesh_info.json` ·
  `input_params.json` — 같은 로더 `analyze_contacts.load_atoms_raw` · `load_contacts_raw`) · type_map · scale = 저장 실행 (`status.json`) 의 것.
- 기준값은 모듈 상수 (`SIGMA_AM_ELECTRONIC` 0.05) 를 바꾸지 않고 `sigma_bulk=` 인자로 준다 → 주 팔 증서 `sigma_bulk_S_cm` = 0.0041 로 남는다 (Codex §3-3 — 소비자의 0.05 복원과 섞이지 않게 · 이 출력은 τ · 인계 소비자에 넣지 않는다).

## 3. 관문 (결과 전 · 어기면 그 값을 보고 표에 싣지 않는다 — 상태는 싣는다)

| 관문 | 조건 | 어기면 |
|---|---|---|
| G0 실행 전 | 깨끗한 트리 (추적 파일 변경 0) · `scripts/network_conductivity.py` sha256 = `da9ecfef…` (실행 핀 `0801d4ceb` 와 같음) · 봉인 32 `code_fp` = `e8b2496b…` · 모듈 `SIGMA_AM_ELECTRONIC` = 0.05 · 등록 표 다섯 ID = §1 · 원자료 `raw/ps45_network_g2.tgz` sha256 = `076727a8…` · 등록 문서 있음 · 출력 폴더 = 새 빈 폴더 · 리포 (git 체크아웃) · 입력 뿌리 (안 · 조상) · 배치 출력 (`status.json` schema · `work/results` + `solver_output`) · 웹앱 서빙 폴더 (env) · 다른 실행의 manifest 폴더 밖 | rc 2 · 아무것도 안 씀 |
| G1 패치 양성 대조 (풀이 앞 · 뒤) | 합성 균일 반경 4.5 µm 15 입자 망 (실제 생산 함수) — PC 만 OFF/ON = 35/8 (FULL · CF · 협착만 · 두 모드 · 상대 ≤ 1e-12) · SC 만 = 1 (비트) · 혼합 ∉ {1, 35/8} · 패치 뒤 원 함수 복원 · 모듈 기준값 불변 | 앞 = rc 2 · 쓰기 없음 · 뒤 = manifest 거부 (REFUSED · rc 2) |
| G2 입력 결합 (케이스마다) | 네 파일 · 기하 (plate_z · box · scale) = 저장 증서 기하 (두 모드) · 입자 수 = 저장 덤프 개수 · 접촉 행 = 저장 `contact_scan.n_rows_last` | 그 케이스 `inputs_refused` (값 비움) |
| G3 대조 팔 (케이스마다 · 두 모드) | 반올림 전 q = 저장 증서 q (상대 ≤ 1e-9) · 노드 · 간선 수 · 띠 규칙 · 증서 기하 같음 · 증서 문제 없음 | 그 케이스 `control_mismatch` (변형 값 비움) |
| G4 SC 만 (0:10) | 인자 끔 q = 켬 q (비트 · 두 모드) | run_status failed · rc 1 (패치가 SC 를 건드렸다 — 값 인용 금지) |
| G5 무변경 | 입력 네 파일 · 봉인 32 파일 sha256 실행 전 = 후 | manifest 거부 (REFUSED · rc 2) |
| G6 manifest | 필수 칸 (§4) 전부 · 등록 값 (팔 · σ_ref · 케이스 · 패치 표지 · 해시) 일치 · 산출 파일 해시 = 기록 | `manifest.json` 안 씀 → `manifest.REFUSED.json` · 표 = `*.REFUSED.tsv` · rc 2 |

- **기록 (판정 아님)**: 10:0 의 OFF/ON 비와 35/8 의 차 · AM 반경 집합 · AM–AM 0 면적 접촉 수 · 배치 업로드 사본 sha256 = 저장 `source_sha256` (있으면) · 협착 전력 몫 · ψ floor · clamp 수.
- G3 이 실패하면 (입력 · 환경이 저장 실행과 다르다) 그 케이스는 값 없이 보고하고 원인을 따로 본다 — 허용치를 결과 뒤에 넓히지 않는다.

## 4. 산출 · manifest (별도 폴더 · 리포 밖)

- `factor_off_electronic.tsv` (다섯 행 · 등록 순서 · 주 q · σ (반올림 전 · 6 자리) · 상태 · 감도 · 인자 켬 readout · OFF/ON · 대조 상대차 · 노드 · 간선 · 띠 규칙 · 반경) ·
  `records/<id>__<팔>.json` (요약 + run_decomposition 원 결과) · `logs/<id>__<팔>.log` (솔버 출력) · `manifest.json`.
- manifest 필수 칸: schema · kind (`report-only model variant`) · 등록 문서 경로 · sha256 · 실행기 (wrapper) 경로 · sha256 · git HEAD · dirty · 코드 (network_conductivity.py sha256 · 봉인 32
  해시 전 · 후 · code_fp · import 관측 · 모듈 기준값) · 환경 (Python · NumPy · SciPy · networkx · pandas · 스레드 env) · σ_ref (+ 이름표) · σ_base · 팔 정의 · 패치 표지 (대상 · 대체 ·
  범위 · `source_files_modified false` · *"원 코드 파일 불변 · 실행 모형 변경"*) · 원자료 · 등록 표 sha256 · 입력 뿌리 · 출력 · 케이스 (입력 네 파일 sha256 · 기하 · type_map · 입자 · 접촉 수 ·
  반경 · 팔마다 q · σ · 상태 · 사유 · **수치 증서** · 증서 문제 · 저장 대조) · G1 (앞 · 뒤) · 출력 파일 sha256 · 입력 무변경 · run_status · run_problems · 시각 (UTC · KST).
- 이 출력은 **report-only model variant** 다 — 원 생산 JSON · TSV · 상태 · code_fp 를 덮어쓰지 않고, 인계 (τ · v1.3) · 웹앱 케이스 페이지에 넣지 않는다 · 단위 환산 표 (readout-only ·
  인자 켬) 와 같은 표에 섞을 때는 열 이름으로 가른다.

## 5. WSL 명령 (1저자)

```bash
# ── 0. 체크아웃 (detached · 깨끗한 트리) · 파이썬 = 배치 venv ──
cd ~/dem-audit
git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8        # 이 등록 · 실행기를 담은 브랜치 (stoic-knuth 로 병합됐으면 그쪽)
git checkout --detach FETCH_HEAD && git log -1 --oneline        # ★ 이 sha 를 §7 에 적는다 (manifest git.head 에도 남는다)
echo "dirty 줄 수 = $(git status --porcelain --untracked-files=no | wc -l) (0 이어야)"
PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1)
$PY -c "import numpy, scipy, networkx, pandas; print(numpy.__version__, scipy.__version__, networkx.__version__, pandas.__version__)"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
IN=~/ps45_network_g2_0801d4ceb/work/results                    # 10-07 g2 배치의 케이스 결과 (읽기만)
OUT=~/ps45_sigmae_factor_off_20261013                           # 새 폴더 (없어야)
ls "$IN"                                                       # 다섯 케이스 폴더

# ── 1. 자체시험 (합성 · 1 분 안) ──
$PY scripts/ps45_sigmae_factor_off_variant.py --selftest 2>&1 | tail -3

# ── 2. 관문만 (G0 · 케이스 입력 기하 — 풀이 · 쓰기 없음) ──
$PY scripts/ps45_sigmae_factor_off_variant.py --check-only --inputs-root "$IN" --out "$OUT"

# ── 3. 실행 (전자 망 다섯 × 팔 넷 · CSV 읽기 포함 수 분) ──
$PY scripts/ps45_sigmae_factor_off_variant.py --inputs-root "$IN" --out "$OUT" 2>&1 | tee "$OUT.log"; echo "rc=${PIPESTATUS[0]}"

# ── 4. 보내기 (반입 = 다음 세션) ──
tar czf "$OUT.tgz" -C ~ "$(basename "$OUT")" "$(basename "$OUT").log" && sha256sum "$OUT.tgz" && ls -l "$OUT.tgz"
DL=/mnt/c/Users/Administrator/Downloads        # 다른 PC 면 /mnt/c/Users/안용훈/Downloads
cp "$OUT.tgz" "$DL/"
```

- g2 작업 폴더 (`~/ps45_network_g2_0801d4ceb/work/results`) 가 지워졌으면 같은 업로드에서 만든 세대 1 작업 폴더 `~/ps45_network_20261006/work/results` 로 바꿔 친다 —
  G2 · G3 이 입력 결합을 판정한다 (저장 g2 증서 q 를 재현하면 같은 입력).  둘 다 없으면 멈추고 보고 (웹앱 재분석으로 만들지 않는다 — 새 등록 필요).
- rc: 0 = 다섯 ok · 1 = manifest 는 있고 케이스 · 실행 문제 있음 (표에 상태) · 2 = 관문 거부.  rc 2 면 화면의 ⛔ 줄을 그대로 보고 (고치지 말고).

## 6. 결과 뒤 금지 (등록 위반)

- σ_ref · 팔 · 모드 · 케이스 집합 · 허용치를 바꿔 다시 돌려 고르기 · 실패한 케이스를 빼고 넷만 그리기 · 섞인 셋을 끝점에서 보간 · 문헌 (Ketter · Minnmann) 에 가까운 쪽을 주 값으로 고르기.
- *"이중 할인 제거로 실측 정답"* · *"SC = PC 고유 전도도 입증"* · *"실험 재현 · 검증"* 문구 (Codex §4 · §6) — 그림 각주 = 판정문 §6-1 그대로 (ps45 g2 README §σ_e 에 옮겨 둠).
- 다섯 조성은 반복이 아니다 — SD · 95 % 구간 금지 · Hertz–Physics · 인자 켬/끔 차이는 모형 선택 감도 (별도 마커 · 패널).
- 이 출력을 194 · v1.3 · 웹앱 · τ 인계에 넣기.

## 7. 실행 기록 (실행 뒤 채운다 — 결과 칸은 비워 둔다)

| 항목 | 값 |
|---|---|
| 1저자 비준 | ⬜ |
| 실행 커밋 (`git log -1`) · dirty | ⬜ |
| 입력 뿌리 | ⬜ |
| `--selftest` · `--check-only` · 실행 rc | ⬜ |
| 받은 tgz sha256 | ⬜ |
