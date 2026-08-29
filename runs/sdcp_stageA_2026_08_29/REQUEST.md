# VASP 계산 요청 — SDCP / perfluorodecane 조각의 LiNiO₂(104) 흡착 (Stage A)

- 요청일: 2026-08-29 · 묶음 **하나**: `sdcp_stageA_v5.zip` (**40잡**)
- ⚠ `sdcp_motifprobe_v2`(10잡)는 **이번에 보내지 않습니다** (아래 §8)
- 생성기: `tools/sdcp/vasp_handoff_bundle.py` (모드 `--closure --d3_pairs --both_seeds`)
- 계보: 2026-08-12 묶음(30잡, 2026-08-25 반송)과 **같은 생성기·같은 U·같은 ENCUT**.
  달라진 것은 아래 §3 에 전부 적었습니다.

---

## 0. 먼저 — 이 묶음은 **단일점만** 돕니다 (이전 요청과 다른 점)

| | 2026-08-12 묶음 | **이번 묶음** |
|---|---|---|
| 상(phase) | `pre` → `relax` → `static` (+일부 `dense`) | **`static` 하나뿐** |
| 기하 | VASP 가 이완 | **고정** (MLIP 이 고른 기하 그대로, 전 원자 고정) |
| 반송물 | relax/OUTCAR + CONTCAR + static/OUTCAR | **`static/OUTCAR` 만** |

⚠ **묶음 안 `README_REQUEST.md` 는 이전 판의 문구가 일부 남아 있습니다.**
82 systems · 259 phase runs · relax 반송 · tier/pair 표가 보이면 **이 파일(§4)이 우선**입니다.
잡 폴더에 `relax/` 가 아예 없으므로 실물이 이 문서와 맞습니다 — 확인하실 수 있습니다:

```bash
find . -maxdepth 3 -type d -name relax | wc -l    # → 0 이어야 정상
find . -maxdepth 3 -type d -name static | wc -l   # → 그 묶음의 잡 수와 같아야 정상
```

---

## 1. 무엇을 묻는가

**같은 표면 위에서 두 고분자 조각 중 어느 쪽이 더 강하게 붙는가**, 그리고
**그 결합이 어느 접촉 모티프에서 오는가.**

- 조각 A: 중성 SDCP 단량체 (술폰산기를 가진 유기물)
- 조각 B: CF₃–(CF₂)₈–CF₃ (perfluorodecane) — 대조군

산출물은 잡마다의 **`static` 전자에너지 하나**입니다. 조합·판정은 저희가 합니다
(묶음 안 `analyze_results.py`).

`sdcp_motifprobe_v2` 는 별도 질문(접촉 모티프 대비)이라 **다른 묶음**으로 분리했습니다.
두 묶음은 같은 clean slab 에서 파생됐고 계산 조건이 동일합니다.

---

## 2. 잡 구조

각 잡 폴더:

```
<잡폴더>/
  POSCAR              ← 계산할 기하 (고정)
  static/INCAR
  static/KPOINTS
  POTCAR_ASSEMBLE.sh  ← ★ 잡마다 종 순서가 다릅니다
  POTCAR_SPEC.txt
  job.json            ← 이 잡의 기대 INCAR·MAGMOM·k 메시
  run_job.sh          ← 이걸 실행하면 됩니다
```

실행:

```bash
cd <잡폴더>
PP=/경로/potpaw_PBE.54 bash POTCAR_ASSEMBLE.sh      # ★ 잡마다 반드시 새로
VASP_CMD="srun -n 256 vasp_std" bash run_job.sh
```

### ⛔ 제일 비싼 사고 — POTCAR 돌려쓰기

POSCAR 의 **종 순서가 잡마다 다릅니다**:
`Li Ni O` · `Li Ni O C F` · `Li Ni O C F H` · `Li Ni O S C H`.
공통 POTCAR 하나를 전 잡에 복사하면 그 잡은 **에러 없이 다른 계를 계산**합니다.
`POTCAR_ASSEMBLE.sh` 가 잡마다 조립하고 TITEL 수까지 확인합니다 — 반드시 잡마다 부르세요.

---

## 3. 계산 조건 (INCAR 에 들어 있음 — 바꾸지 말 것)

| 항목 | 값 |
|---|---|
| 범함수 | PBE |
| `LDAU` | Ni 만 U = 6.2 eV (Dudarev, `LDAUTYPE=2`), `LMAXMIX=4` |
| `ENCUT` | 520 |
| `ISMEAR` / `SIGMA` | 0 / 0.05 |
| `LASPH` / `ADDGRID` | `.TRUE.` |
| `LREAL` | **`.FALSE.`** (이 묶음은 전 잡 강제) |
| `IVDW` | **11 = D3 zero damping** — 일부 잡은 `IVDW` 없음(분산 없는 짝) |
| `ISPIN` / `MAGMOM` | 2 / 잡마다 다름 — `job.json` 에 기대값 |
| 슬랩 | `LDIPOL=.TRUE.` · `IDIPOL=3` · `DIPOL`=질량중심 |
| 기체 | `IDIPOL=4` · 진공 상자 |

> ⚠ 2026-08-11 요청문이 `IVDW=11` 을 "D3-BJ" 라고 적었는데 **오기**입니다.
> `IVDW=11` 은 **D3 zero damping** 입니다. 계산은 그때와 같고 이름만 정정한 것입니다.

**D3 짝(pair)**: 같은 기하를 `IVDW=11` 있는 판과 없는 판으로 각각 돌립니다.
둘의 차이가 분산 기여입니다 — 그래서 **두 잡이 같은 POSCAR 를 씁니다. 정상입니다.**
중복이라고 하나만 돌리지 말아 주세요.

**자기 seed 2종**: 같은 기하를 서로 다른 `MAGMOM` 으로 시작하는 잡이 있습니다
(`pm1` / `net4`). 이것도 **중복이 아닙니다** — 자기상태 민감도를 재는 것이 목적입니다.

### SCF 가 안 붙을 때만 (순서대로)

1. `ALGO = All`
2. `AMIX=0.1 · BMIX=0.0001 · AMIX_MAG=0.2 · BMIX_MAG=0.0001`

쓰신 것을 그 잡 폴더의 `NOTES.txt` 에 남겨 주세요. 그래도 안 되면 **그 잡은 중단하고
알려 주세요** — 임의로 조건을 바꾸는 것보다 미수렴으로 남는 편이 낫습니다.
`NCORE` / `KPAR` / `NSIM` 등 병렬 태그는 자유롭게 조정하셔도 됩니다.

---

## 4. 반송물 (잡마다)

- **`static/OUTCAR` — 필수** (`.gz` 그대로 가능). 이것 하나면 판정이 됩니다.
- `static/vasprun.xml` — 선택
- `NOTES.txt` — 위 SCF 조치를 쓰셨다면 필수
- **CHGCAR / WAVECAR 반송 불필요** (용량)
- ⚠ `INCAR` · `KPOINTS` · `POSCAR` 를 고치지 마세요. 저희 분석기가 `MANIFEST.json` 의
  `files_sha256` 과 대조해 바뀐 파일을 잡아냅니다 (병렬 태그는 예외 — 고치셨으면 알려 주세요).
- 발산·미수렴 잡은 **지우지 말고 그대로** 보내 주세요. 어느 잡이 왜 실패했는지가 판정의 일부입니다.

완주 후 확인용(선택):

```bash
python3 analyze_results.py .     # stdlib 만 씁니다
```

필수 산출이 빠지면 `exit 2` 로 알려 줍니다.

---

## 5. 규모 · 일정

| | |
|---|---:|
| 잡 | 50 (40 + 10) |
| 상 | 잡당 `static` 1회 |
| 계획 병렬도 | **256 코어/잡 · 동시 8잡** |
| 예상 makespan | **약 3일** (가장 긴 잡 ~19 h @256코어) |

> ⚠ 묶음 안 `SUBMIT_CONTRACT.md` 는 "잡 40 / 총 VASP 실행 24" 로 **서로 어긋난 두 숫자**를
> 적고 있습니다 (생성기가 실행 횟수를 셀 때 D3-off 쌍둥이 16잡을 빠뜨립니다).
> **실제는 40잡 전부가 각각 static 1회** — 즉 40회입니다. `run_job.sh` 가 있는 폴더 수가
> 정답입니다: `find . -name run_job.sh | wc -l`.

⚠ 위 시간은 실측 기반 **모형값이고 ±2배** 범위입니다 (`tools/sdcp/vasp_cost_estimate.py`,
2026-08-08 납품 OUTCAR 기준). walltime 은 넉넉히 잡아 주세요 — 잘리면 그 잡을 다시 돌려야 합니다.

잡 사이에 의존성이 **없습니다.** 순서는 자유이고 전부 동시에 던지셔도 됩니다.

---

## 6. 무결성

| 항목 | 값 |
|---|---|
| 파일 | `sdcp_stageA_v5.zip` (약 0.4 MB) |
| ZIP SHA256 | `8c6587635e559e81dff68be0b960d318e852ea2b4b608d26f0f11bc656ba713c` |
| `MANIFEST.json` SHA256 | `0860ae4340218b599100052d12fa941aa2a319a74f1b43de8c6ddd36a876670e` |
| 잡 | 40 (references 16 + calibration complexes 24) |
| 총 VASP 실행 | 40 (전부 `static`) |
| clean slab | `d5f18feb15701f3fc932a1c8f64a09ed48c39ca270d8d8a8f5339658b6c43676` |
| 후보집합 | `db/properties/prospective_basins_2026_08_29.json` · frozen `94675e66e02c855a` |

받으신 뒤 대조해 주세요 — `sha256sum sdcp_stageA_v5.zip`.

⚠ 파일명 끝의 **`_v5`** 를 확인해 주세요. `_v1` ~ `_v4` 는 전부 폐기본입니다:
`_v2`(40잡)는 문서가 이완판이라 반송 계약이 틀렸고, `_v3`(34잡)는 후보집합이 다르며
(c10 이 2자세), `_v4`(40잡)는 `MANIFEST` 의 실행 횟수가 24 로 잘못 적혀 있었습니다.
`_v5` 만이 위 해시와 맞습니다.

각 묶음 안 `MANIFEST.json` 의 `files_sha256` 로 개별 파일까지 대조하실 수 있습니다:
`sha256sum <파일>`.

---

## 7. 범위 밖

변형에너지 분해(E_int/E_deform) · DOS/Bader · 진동/ZPE · 구조 이완 —
이번 요청 범위 밖입니다.


---

## 8. 이번에 보내지 않는 것 — `sdcp_motifprobe_v2`

접촉 모티프 대비를 묻는 10잡 묶음을 따로 만들어 두었지만 **이번 요청에서 뺐습니다.**

이유는 순서입니다. 그 묶음은 Stage A 회수 뒤에 정할 선택창 (W) 안팎을 가르는
후보 선정과 **같은 자세 풀**에서 나옵니다. 결과를 먼저 보면 Stage B 후보 선정이
그 결과에 오염됩니다 — 즉 "무엇이 낮은지 보고 나서 무엇을 후보로 삼을지 정하는"
모양이 됩니다.

그래서 순서를 이렇게 고정했습니다:

1. **Stage A 40잡** (이 요청)
2. 회수 → (B)·(W) 확정 → Stage B candidate·audit **동결**
3. 그 다음에야 motif probe 실행

실행하게 되면 exact 10잡 · matched contrast · seed · D3 상태를 별도 manifest 에
박아 다시 요청드리겠습니다. 그 결과는 primary minimum 에 **포함하지 않고**,
사전 지정된 matched contrast 의 descriptive 결과로만 씁니다.
