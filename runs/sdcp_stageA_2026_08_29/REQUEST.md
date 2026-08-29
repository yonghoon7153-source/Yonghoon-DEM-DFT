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
| 파일 | `sdcp_stageA_v9.zip` (476238 B) |
| ZIP SHA256 | `246da98748e9f2754925504e0cbeb865db91ddd4c68e401b456abfc008dabc3b` |
| `MANIFEST.json` SHA256 | `e232e975e0659f8756c993d1dd1d093c6d701f7f98ce46ff43bf88eee3c053a0` |
| 잡 | 40 (references 16 + calibration complexes 24) |
| 총 VASP 실행 | 40 (전부 `static`) |
| clean slab | `d5f18feb15701f3fc932a1c8f64a09ed48c39ca270d8d8a8f5339658b6c43676` |
| 후보집합 | `db/properties/prospective_basins_2026_08_29.json` · 전체 SHA `20fdde06760b36e15a9bd544925c71e4b1a52f430348ff64a2224f1bf61f6d6e` |

받으신 뒤 대조해 주세요 — `sha256sum sdcp_stageA_v9.zip`.
증서는 `ATTESTATION_v9.json` 에 같이 있습니다 (ZIP 바이트에서 직접 생성).

⚠ 파일명 끝의 **`_v9`** 을 확인해 주세요. `_v1` ~ `_v8` 은 전부 폐기본입니다.

---

## 7. POTCAR 검증 — 실행 전에 목록이 필요합니다

`POTCAR_ASSEMBLE.sh` 가 조립 전에 **신뢰하는 PBE.54 세트의 sha256 목록**과
대조합니다. variant 이름과 `PAW_PBE` 만 확인해서는 "전부 같은 잘못된 세트" 를
못 막기 때문입니다.

목록은 **한 번만** 만들어 전 잡에 같은 파일을 쓰세요 (잡마다 새로 만들면
아무것도 검증하지 않습니다):

```bash
for v in $(ls "$PP"); do sha256sum "$PP/$v/POTCAR"; done > /abs/site_allow.txt
# 그 다음 각 잡에서
PP=/path/to/potpaw_PBE.54 POTCAR_ALLOWLIST=/abs/site_allow.txt bash POTCAR_ASSEMBLE.sh
```

이 목록은 **외주처 내부에만** 두시면 됩니다 — 저희에게 보내실 필요 없습니다.
대조 없이 진행하셔야 하면 `POTCAR_ALLOWLIST_WAIVED=1` 로 명시해 주세요
(그 사실이 `POTCAR_PROVENANCE.json` 에 기록됩니다).

## 8. 이 잡들은 **1회용**입니다

`run_job.sh` 가 시작 전에 `OUTCAR`·`WAVECAR`·`CHGCAR` 등이 있으면 **거부**합니다.
같은 폴더에서 두 번 돌리면 다른 설정의 결과가 섞이고, 회수 후에는 구별할 방법이
없기 때문입니다. 의도한 재개면 `ALLOW_RESUME=1` 로 주시고 `NOTES.txt` 에 남겨 주세요.

## 7. 범위 밖

변형에너지 분해(E_int/E_deform) · DOS/Bader · 진동/ZPE · 구조 이완 —
이번 요청 범위 밖입니다.


---

## 9. 이번에 보내지 않는 것 — `sdcp_motifprobe_v2`

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
