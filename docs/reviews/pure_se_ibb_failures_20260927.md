# 순수 SE 판정 시험 — ibb 제출 실패 3 회 · 원인 · 처방 (정정판, 2026-09-27)

> ⛔ **11:0x 판 (사용자에게 보낸 요약) 의 ③ 처방과 "지금 ibb 의 덱을 고치는 명령" 은 틀렸다.**  외부 검토가 LIGGGHTS-PUBLIC 3.8 소스와
> 실제 실행으로 확인했다 — AM 템플릿을 *정의만* 남겨도 똑같이 멈춘다.  이 문서가 그 판을 대신한다.  원장 = `findings.json` **SELF-53**.
> 사전등록 = `docs/reviews/pure_se_union_prereg_20260927.md` (§3 문구 정정 · §6 제출 기록).

## 목적

LHS 2-type 봉인 템플릿 (ibb `~/dem_test/lhs/lhs00_110/input_lhs00_110.liggghts`, sha256 `aca27397…`) 에서 **AM 을 0 개 넣고 SE 만** 넣은 침대 4 개
(r_SE 0.5 · 0.75 · 1.0 · 1.0 µm, volfrac 0.22, seed 20011 · 20021 · 20023 · 20029) 로, 이 DEM 프로토콜의 순수 SE 공극률을 잰다.

## 실패 3 회 — 정정된 원인과 처방

| 회 | job | 증상 | 원인 | 처방 |
|---|---|---|---|---|
| ① | 231852–55 | 6 s FAILED 85:0 · OpenMPI *"bind … more cpus than are available in your allocation"* | 사람이 sed 로 `#SBATCH -n 15` 만 바꿨다 — MPI 바인딩이 할당과 안 맞는다 | ⛔ 내 첫 처방 (`-N 1` 추가) 은 틀렸다.  사용자가 처음부터 짚은 **oversubscribe** 가 맞았다 |
| ② | 231865–68 | 2 s FAILED 85:0 · 같은 바인딩 오류 | `-N 1` 은 원인이 아니었다 (node01 = `Sockets=152 CoresPerSocket=1 ThreadsPerCore=1`) | 리포의 ibb 관례 `mpirun --oversubscribe -np N` (`dem_scripts/run_all_outlier_seeds.sh` 등) → `mpirun --oversubscribe --bind-to none -np 15` 를 `#SBATCH -n 15` 와 **짝으로** |
| ③ | 231896–99 | 8 s FAILED 1:0 · LIGGGHTS 시작 (`1 by 1 by 15 MPI processor grid` · 분포 `pts2 mass% 100`) 뒤 **`ERROR: Atom types must start from 1 for granular simulations (../properties.cpp:120)`** | **생성기 결함** — `--pure-se` 가 AM 입자 템플릿 (atom_type 1) 줄을 지웠다 | ~~AM 템플릿을 정의만 남기고 분포에서 빼기~~ ⛔ **틀림 (아래)** → **AM 템플릿을 분포에 가중 0 으로 남긴다**: `2 pts1 0.000000 pts2 1.000000` |

## ③ 의 근본 원인 (외부 검토 — LIGGGHTS-PUBLIC 3.8 소스)

- `Properties::max_type()` 가 run 초기화 때 입자 타입 범위를 모은다.  최소 타입이 1 이 아니면 `properties.cpp:120` 에서 멈춘다.
- 그 범위에 들어가는 것은 넷뿐이다 — **존재하는 원자 · 분포 (particledistribution) 에 든 템플릿 · 벽 (`primitive type N`) · 메시**.
  `fix particletemplate/sphere` 자체는 `min_type()` 을 보고하지 않는다 (Fix 기본값 0 이라 무시된다).
- 삽입 · 침강 동안에는 플래튼 메시 (type 1) 가 아직 없고 바닥 벽은 type 2 (SE) 다 ⇒ AM 줄을 **지운** 옛 생성기도, **정의만 남긴** ③ 처방도
  최소 타입이 2 가 되어 멈춘다.  두 형태 모두 실제 실행에서 `properties.cpp:120` 오류가 그대로 재현됐다.

## 올바른 처방 — AM 템플릿을 분포에 가중 0 으로

- 분포 줄 = `2 pts1 0.000000 pts2 1.000000`.  템플릿 정의 두 줄은 템플릿 덱과 한 글자도 같다.
- 소스 근거 (`fix_particledistribution_discrete.cpp`): 음수 가중만 거부하고 0 은 받는다 · 삽입 개수는 `int(N·w + U(0,1))` 라 w = 0 이면 **항상 0 개** ·
  exact_number 경로에서도 잔여 배분이 0 가중 템플릿으로 가지 않는다 · 분포의 최소 타입은 분포에 든 **모든** 템플릿으로 정한다 → type 1 이 남아 검사를 통과한다.
- 실행 확인 (검토자 — LIGGGHTS-PUBLIC 3.8 MPI 빌드, VTK 없음, LHS 2-type 형식 축소 덱): 분포 출력 `pts1 number%=0.000000%` · 삽입 입자 **전부 type 2**
  (r_SE 0.5 에서 19,958 개 · 1.0 에서 2,494 개) · 침강 → 플래튼 생성 → 안정화 → 압축 루프까지 오류 없음.
- 부수 효과 (의도대로 둔 것 — 물리 불변): 이웃 목록 bin 이 여전히 r_AM 기준 (lhsx mono 덱과 같은 조건) · 플래튼 높이 `zmax + r_AM + margin` 과
  플래튼 메시 재질 type 1 도 LHS 프로토콜 그대로.  도구가 이 줄들을 "AM 참조" 로 출력한다.

## 러너 · 영역 분할

- **러너 (①②)**: ibb 에서 여러 코어를 쓰려면 `#SBATCH -n N` 과 `mpirun --oversubscribe --bind-to none -np N` 이 **짝**이어야 한다.
  생성기의 `--ntasks N` 이 두 자리를 같이 바꾸고 되읽어 대조한다.  반쯤 고친 러너 (`-n` 과 `-np` 가 다르거나 플래그가 빠진 것) 를 잡고,
  `-n` 줄이 없는 러너는 거부한다.
- **`processors * * 1`** (새로 넣은 것): processors 줄이 없으면 LIGGGHTS 가 키 큰 상자를 z 로만 자른다 (③ 로그 `1 by 1 by 15`) — 침강 뒤 ≈ 27 µm
  침대가 한두 조각에 몰려 나머지 코어가 논다.  `* * 1` 이면 x · y 로 자른다 (검토자 시험 5 by 3 by 1 · **실제 제출 3 by 5 by 1** — 상자 모양에 따라
  LIGGGHTS 가 고른다, 둘 다 x · y 분할).  `region reg_box` 앞에 넣어 `dem_restart.py` 의 재시작 덱 (head 블록) 에도 따라간다.
  **물리 불변** — 코어 수를 바꿀 때처럼 비트 단위로 같지는 않다.
- insert/pack 의 `ninsert_this_local × maxattempt` 는 int 로 계산된다.  r_SE 0.5 침대 (≈ 141 k 개) 를 1 코어로 돌리면 2.8e9 로 int 범위를 넘는다.
  x · y 15 분할이면 코어당 ≈ 1 만 개라 여유가 크다.

## 검토 요청에 대한 답

1. *AM 템플릿을 정의만 두고 분포에서 뺀 덱이 AM 0 개 · SE 만 삽입하는가?* → **아니다 — `properties.cpp:120` 에서 멈춘다.**  AM 0 개는 **가중 0** 으로만 된다.
2. *벽 재질 · 재질 행렬이 원래 LHS 덱과 같은 프로토콜인가?* → 같다.  바닥 `primitive type 2` (SE) · 2×2 재질 행렬 · 플래튼 메시 type 1 은 템플릿 그대로이고,
   도구가 AM 에 기대는 줄을 출력해 확인할 수 있다.
3. *15 MPI (원래 1) 가 결과에 영향이 없는가?* → 영역 분할만 바뀐다 · 물리 불변 · 비트 동일은 아니다.
4. *근본 수정* → 검토자 판 생성기로 교체 (selftest 42 → 61): `render_pure_se` (AM 가중 0 · SE 1 · `--procs` · 분포 순서/AM type 검사) ·
   `roundtrip_pure_se` (템플릿 2 개가 둘 다 분포에 · AM type 1 가중 0 · SE 가중 1 · 분포 최소 타입 1 · processors 가 create_box 앞 — **옛 생성기 형태와 ③ 처방
   형태 둘 다 여기서 걸린다**) · `parse_deck` (min_type · processors) · 설계 흐름 `roundtrip` 에도 최소 타입 1 검사 · `--ntasks` · `am_references()` · manifest.

## 교훈 (SELF-53)

- 합성 픽스처 시험 (42/42) 은 LIGGGHTS 를 돌리지 않아 **LIGGGHTS 자체 규칙** (타입 1 부터) 을 못 잡았다.  ③ 처방도 소스를 확인하지 않은 추정이었다.
  ⇒ 덱 생성기를 바꿀 때는 **LIGGGHTS 스모크 시험** (삽입 + 수백 스텝, 축소 덱) 을 통과 조건으로 둔다.
- ①② 에서 나는 사용자가 짚은 oversubscribe 를 내 판단으로 물리쳤고 리포의 ibb 관례를 먼저 찾지 않았다.  ⇒ 실행 환경 문제는 **리포 관례를 먼저 찾는다**.

## 네 번째 제출 — 정상 실행 (09-27 ≈ 11:40 KST)

- 옛 실패 폴더는 지우지 않고 `~/dem_test/lhs/pse_*.fail_0927` 로 옮기는 명령을 썼다.
- 덱: WSL 에서 검토자 생성기 (`~/lhs_ext_materialize.py`, sha256 `43bd16216e334653…`, selftest 61/61) 로
  `--box ~/dem-web/docs/data/lhs_ext_box_v2_20260829.json --template-run … --ntasks 15 --outdir ~/pse_decks_20260927b` → ibb 로 복사.
- job **231946 – 231949** (`pse_r050_a` · `pse_r075_a` · `pse_r100_a` · `pse_r100_b`) RUNNING · node01 · 15 MPI · **`3 by 5 by 1 MPI processor grid`** · ERROR 0 ·
  삽입 **139,706 · 41,394 · 17,463 · 17,463** (사전 추정 ≈ 141 k · 42 k · 18 k · 18 k) · PHASE 1 (침강).
