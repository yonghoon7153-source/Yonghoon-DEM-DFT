# C-12 v35 발송 메일 (그대로 복붙)

> 첨부: `sdcp_c12_v35.zip` (0.6 MB · 16잡 · 전부 static)
> ⚠ 이 파일은 **자동 생성**이다 (tools/sdcp/c12_render_send_mail.py). 실행 블록·반송 목록·walltime
>   문장은 번들 README 에서 글자 그대로 뽑았다 — 손으로 고치지 마라.

## 제목
```
[DFT 위탁] SDCP/PTFE–LiNiO₂ 계면 단일점 16잡 — 번들 v35
```

## 본문

안녕하세요.

SDCP·PTFE 바인더 계면 계산 번들을 보내드립니다. **VASP 단일점(static) 16잡**이고,
실행·검증·분석 스크립트가 번들 안에 전부 들어 있습니다.

### 1. 무결성 확인 (먼저)

```
EXPECT_ZIP_SHA256      = 7e62c7519b68cf16268311a883ae7f40e766e452d71d9f4fe06130e8d7145b8e
EXPECT_MANIFEST_SHA256 = c074393b16528f52c08f4a83bb6cf20584243c8580eb7bda21bc98b548ab8ea5
```

```bash
sha256sum sdcp_c12_v35.zip          # 위 값과 대조 — 다르면 전송이 깨진 것입니다
mkdir -p <이 묶음 전용 빈 디렉터리> && cd <그 디렉터리>
unzip /경로/sdcp_c12_v35.zip && cd sdcp_c12_v35
sha256sum MANIFEST.json             # 위 값과 대조
```

### 2. 실행

⚠ 아래 변수가 **전부 필수**입니다. 하나라도 빠지면 러너가 즉시 멈춥니다
(조용히 다른 설정으로 도는 것보다 멈추는 게 낫다고 보아 그렇게 만들었습니다).
실행은 **계산 노드 할당 안에서** 해 주십시오 — 러너가 그 자리에서 잡 4개를 동시에 띄웁니다.

```bash
cd <이 묶음을 푼 디렉터리>            # 묶음 **루트**에서 실행합니다 (잡 폴더 아님)
# ⛔⛔ 0단계 — **ZIP 을 풀기 전에**, ZIP 밖에서 SHA 를 대조하십시오 (회신 BA P0-1).
#    아래 값은 메일 본문에 있습니다. 이 대조는 번들 안의 어떤 스크립트도 쓰지 않습니다
#    — ZIP 안의 해시는 자기 자신을 증명하지 못하기 때문입니다.
#      sha256sum /경로/받은번들.zip     # ← 메일 본문의 값과 눈으로 대조
#    다르면 **풀지 마시고** 저희에게 알려 주십시오.
#
# ⚠ 러너는 배포 스크립트를 실행하기 **전에** 추출 파일 전수검사(census + files_sha256
#    + EXPECT)를 끝냅니다. v21 까지는 POTCAR 조립(SEAL)이 그 검사보다 **먼저** 돌아,
#    변조된 assembler 가 무결성 검사 전에 실행될 수 있었습니다 (회신 BA P0-1).
cd <이 묶음을 푼 디렉터리>              # 묶음 **루트**

# ── POTCAR 원본 트리와 allowlist (조립기가 쓴다) ──
export PP=/path/to/potpaw_PBE.54
# allowlist 는 그 트리의 변형별 POTCAR 해시 목록입니다. 없으면 이렇게 만드십시오:
#   for v in $(ls "$PP"); do sha256sum "$PP/$v/POTCAR"; done > /abs/site_allow.txt
#   (형식: `<sha256>  <PP>/<variant>/POTCAR` — sha256sum 기본 출력 그대로)
export POTCAR_ALLOWLIST=/abs/site_allow.txt

# ── 배포본 결박 (ZIP 밖의 값이 유일한 앵커입니다) ──
export BUNDLE_ZIP_SHA256=$(sha256sum /경로/받은번들.zip | cut -d" " -f1)
export EXPECT_MANIFEST_SHA256=c074393b16528f52c08f4a83bb6cf20584243c8580eb7bda21bc98b548ab8ea5
export EXPECT_ZIP_SHA256=7e62c7519b68cf16268311a883ae7f40e766e452d71d9f4fe06130e8d7145b8e

# ── 실행 방식 ──
# ⛔ 자유형 launcher 문자열(VASP_CMD·VASP_LAUNCHER)은 **폐지됐습니다** (회신 AV P0-2) —
#    문자열 검사는 우회가 가능해, 종류와 수만 받고 실행 명령은 러너가 조립합니다.
export VASP_LAUNCHER_KIND=mpirun            # mpirun|mpiexec|srun|none|wrapper
export LAUNCHER_BIN=/abs/path/to/mpirun     # **필수** — PATH 에서 찾지 않습니다. 없으면 exit 2
export VASP_NPROC=192                        # 랭크 수 (잡 하나당) — **KPAR × NCORE = 16 의 배수**여야 합니다
#    이 묶음의 INCAR 은 KPAR=4 · NCORE=4 로 고정했습니다. 쓸 수 있는 랭크: 48·64·96·128·192·256·384·512.
#    ⛔ KPAR 배수만으로는 부족합니다 — k-그룹당 랭크가 NCORE 로 안 나뉘면 VASP 가 조용히
#      NCORE 를 되돌립니다 (예: 랭크 20 은 KPAR 4 로 나뉘지만 그룹당 5 가 NCORE 4 로 안 나뉩니다).
#    배수가 아니면 러너가 **첫 VASP 실행 전에** 멈춥니다. INCAR 은 해시로 동결돼 고칠 수 없습니다.
#    ⚠ KPAR 은 k-그룹마다 배열 사본을 들어 **노드당 메모리가 늘어납니다.** 모자라면 랭크를
#      줄이지 마시고(배수 조건이 깨집니다) 노드를 늘려 주십시오.
export VASP_EXE=/abs/path/to/vasp_std       # 실행파일 절대경로 (봉인 대상)

# ⚠ 러너는 기본으로 잡 4개를 **동시에** 띄웁니다 (= 4 × VASP_NPROC 랭크).
#    할당이 그보다 적으면:  export JOBS_PARALLEL=<할당코어 ÷ VASP_NPROC>

# (선택) PAW release 기록 — 첫 VASP 실행 **전에만** 가능 · 안 하셔도 러너·판정에 영향 없음.
#   위 export 들이 같은 셸에 있어야 합니다. 결함이면 러너가 생산 **전에** 멈춥니다 (지우면 다시 돌아갑니다).
#   RELEASE_LABEL="potpaw_PBE.54" SITE="기관/담당자" bash MAKE_POTCAR_ATTESTATION.sh

bash run_staged.sh 1     # census → POTCAR 조립+봉인 → 봉인 census → 1단계 → 판정
bash run_staged.sh 2     # 1단계 통과(STAGE1_PASS.json) 뒤에만
```

⛔ **배열 잡으로 한꺼번에 던지지 말아 주십시오.** 2단계가 1단계 결과에 의존해서
동시에 돌리면 결과가 무의미해집니다.

### 3. POTCAR — 보내실 것 없고, 조립하실 것도 없습니다

**POTCAR 파일 자체는 주고받지 않습니다** (라이선스). 귀측 트리를 그대로 쓰시면 됩니다.
**POTCAR 를 따로 조립하지 마십시오** — `run_staged.sh` 가 첫 VASP 실행 전에 `SEAL_POTCAR_ROOT.sh` 로
전 잡을 조립하고, 원본 SHA256 · TITEL · 조립본 SHA256 을 `POTCAR_PROVENANCE.json` 에 남깁니다.
저희는 그 해시로 **"16잡이 한 트리에서 나왔는가"** 만 확인합니다 — 귀측 트리가 어느 배포판인지는
판정하지 않습니다 (이 묶음은 탐색용 정책이라 원고 인용 자격을 주장하지 않습니다).

(선택) PAW release 를 **기록**으로 남기시려면 실행 블록의 주석 한 줄(`MAKE_POTCAR_ATTESTATION.sh`)을
`bash run_staged.sh 1` **앞에서** 돌려 주십시오 — 첫 VASP 실행 뒤에는 만들 수 없습니다. 안 돌리셔도
계산·판정은 그대로입니다. 돌리셨는데 결함이 있으면 러너가 생산 **전에** 멈추고 이유를 찍습니다.

### 4. 반송해 주실 것

**정본은 `MANIFEST.json` 의 `return_contract`** 이며 이 목록은 그 렌더입니다
(README 와 SUBMIT_CONTRACT 어디를 보셔도 같습니다 — 회신 AV P0-4).

**보내는 방법**: 가장 쉬운 방법 — 푼 디렉터리를 **통째로** 다시 압축해 보내 주십시오 (배포 입력·MANIFEST 포함 · 위 목록이 자동으로 충족됩니다). 예: `tar --exclude=CHGCAR --exclude=WAVECAR -czf 반송.tgz <푼 디렉터리>`

각 잡 폴더에서:
- static/OUTCAR (또는 .gz)
- static/OSZICAR
- static/POSCAR — **실행된 기하** (부모↔canary 기하 대조·기하 감사. 없으면 CANARY_GEOM_UNCHECKED 로 막힙니다)
- POTCAR_PROVENANCE.json (조립기가 자동 생성)
- job.json (받으신 그대로 — 분석기가 잡의 정체·상 목록을 이것으로 읽습니다 · 없으면 그 잡은 차단)
- EXECUTABLE_RECEIPT.tsv — 상별 실행파일 해시 (run_staged 경로가 자동 생성 · 분석기가 root seal 과 대조합니다)

묶음 루트에서:
- MANIFEST.json (받으신 그대로 — 분석기가 가장 먼저 읽습니다)
- POTCAR_ROOT_SEAL.json (첫 실행 전 봉인)
- ZIP_SHA256.txt
- RESULTS.json (run_staged 가 판정 때 만듦 — 있으면 그대로)
- STAGE1_PASS.json (1단계 통과 receipt)
- POTCAR_ATTESTATION.json — **선택** (탐색용 정책). 없어도 러너는 돌아갑니다. ⚠ 다만 그 결과는 **원고 인용 자격이 없습니다** — 사후 provenance 는 무엇을 썼는지만 기록하고 그것이 승인된 PAW dataset 인지 판정하지 못합니다 (회신 AZ P0-7·Q4). 만들려면 `MAKE_POTCAR_ATTESTATION.sh` 를 **첫 VASP 실행 전에만** 돌릴 수 있습니다 (회신 AR P0-6)

보내지 않으셔도 되는 것: CHGCAR·WAVECAR (용량 — 압축에서 빼셔도 됩니다 · ⚠ 서버에서는 지우지 말고 두십시오) · vasprun.xml (선택)
⚠ 발산·미수렴 잡도 지우지 말고 그대로 보내 주십시오 — 실패도 판정의 일부입니다

### 5. 예상 자원

16잡 전부 단일점(static)입니다. 기본 **동시 4잡 · 192코어/잡**으로
계획했습니다 (그 조건에서 전체 약 3.35일 — 모형이라 ±2배).
⚠ **walltime** — 가장 긴 잡의 중앙 추정 **29 h** (192코어/잡 · 모형 불확실성 ±2배 → 외피 58 h). 잡당 walltime 은 **84 h** 를 권합니다 (= **NELM 천장 77 h**(NELM 200 · 기동 1회의 결정론적 상한)을 12 h 단위로 올림 — 모형 외피 58 h × 1.1 보다 이쪽이 크므로 이쪽을 씁니다. 천장은 이미 최대값이라 여유를 더 얹지 않습니다 · 그보다 짧으면 잘립니다). 큐 상한이 84 h 보다 짧으면 **제출 전에** 알려 주십시오 — static 단일점은 나눌 수 없고 재개도 없어, 그 잡은 더 긴 큐/노드 배정이 필요합니다.
⚠ **실행 위치** — `run_staged.sh` 는 **계산 노드 할당 안에서**(로그인 노드 아님) 잡 4개 × VASP_NPROC 랭크를 동시에 띄우므로, 그 할당이 **요청 walltime 84 h** 동안 유지돼야 합니다 (1단계 최장 잡의 중앙 추정은 29 h 지만, 잘리지 않으려면 위 84 h 로 잡아 주십시오). 봉인 프로브도 같은 노드에서 VASP 를 인자 없이 한 번 잠깐 기동합니다.
⚠ **잘릴 수 있는가 (모형이 아니라 천장으로)** — 한 번의 VASP 기동은 `NELM=200` 전자스텝에서 끊깁니다. 이 묶음의 최장 천장은 **77 h** 이고, 알려 주신 큐 상한 91 h 안에 들어갑니다 (여유 14 h). 추정치(29 h)는 모형이라 ±2배지만 이 천장은 결정론입니다 — 둘을 같은 확신으로 읽지 말아 주십시오.
⚠ **전체 일정** — 동시 4잡 기준 약 **3.35일**입니다 (1단계 최장 28.9 h → 게이트 → 2단계 최장 26.0 h · 두 단계는 **직렬**이라 동시 실행을 늘려도 이 아래로는 내려가지 않습니다). 여기에 1단계 반송 뒤 저희 판정 왕복 시간은 포함돼 있지 않습니다.
💡 **먼저 한 잡만 재 보시길 권합니다.** 위 추정은 모형이라 ±2배입니다. 큐 상한이 빠듯하시면 `refs/` 의 기체 잡 하나(가장 짧습니다)나 복합체 한 잡을 먼저 돌려 실제 벽시계를 알려 주시면, 나머지 walltime 을 그 값으로 다시 잡아 드립니다. 1단계 전체를 던진 뒤 큐에서 잘리는 것보다 쌉니다 — 잘린 잡은 재개할 수 없어 통째로 다시 돌려야 합니다.

---

문제가 생기면 러너가 찍는 메시지를 그대로 보내 주시면 됩니다.

감사합니다.

---

## ⚠ 보내기 전 확인 (1저자)

- [ ] 첨부 zip sha256 == `7e62c7519b68cf…`
- [ ] 본문에 두 해시가 정확히 들어갔는가
- [ ] 실행 블록에 `PP`·`POTCAR_ALLOWLIST`·`LAUNCHER_BIN`·`VASP_EXE` 가 살아 있는가
- [ ] 받는 사람 주소

## 이 판에서 바뀐 것 (v34 → v35)

- **선택 attestation 함정 제거**: `MAKE_POTCAR_ATTESTATION.sh` 가 VASP stdout 전문을 적고 봉인은 토큰만
  담아, 돌리면 1단계 ~29 h 뒤 판정이 막히는 결함(렌즈4 P0-1). 둘 다 토큰으로 통일하고,
  post_hoc 이라도 증서가 있으면 러너가 **생산 전에** 검증한다.
- **δ_k 설계 제외의 근거를 비준 사전등록에 둔다**: `3_오차예산.축_설계_제외_2026_09_03` (1저자 비준 · 안 A).
  재개 조건은 문장이 아니라 기계 평가 구조(판정량 `D_raw_eV` · 문턱 0.05 eV · 비교 `boundary`)
  로 MANIFEST 에 복사되고, 분석기가 결과에 `reopen_eval` 로 남긴다. 종전 "|ΔE_ads|<50 meV → dense 추가" 는
  비준 프로토콜 §7·§8 과 반대여서 폐기.
- `overall_citable_at_0.01eV` 는 δ_k 가 없으면 **False**(None 아님) — 문서와 기계 기록이 같은 말을 한다.
- 반송 목록에 `MANIFEST.json`·`job.json`·`RESULTS.json` 과 "통째로 압축" 을 정본으로 넣었다.
- walltime 문장 세 문서 통일 · 종 순서 목록 실물화 · dense 잔존 문구 제거 · 일정 3.35일(동시 4잡).

🔁 **재개 조건 (비준 사전등록에서 복사 · 결과 보기 전 선언)**
> 재개하지 않는다. |D_raw| < 0.05 eV 는 프로토콜 §7 미해결 · §8 '계산을 확장하지 않는다'. |D_raw| ≥ 0.05 eV 면 k 가드밴드(0.01 eV)가 부호·판정을 못 바꾼다. 경계 구간 0.05 ≤ |D_raw| < 0.06 eV 에서는 분석기가 KCONV_UNTESTED_AXIS_AT_THRESHOLD 자문을 내고 원고는 '미시험 축에 판정이 민감하다' 를 적는다 — 계산은 추가하지 않는다.

## 기록

| | |
|---|---|
| 번들 | `runs/sdcp_c12_2026_08_30/sdcp_c12_v35.zip` |
| 증서 | `runs/sdcp_c12_2026_08_30/IDENTITY_v35.json` |
| 생성 커밋 | `11bfb150` (clean · 생성 시점에 origin 에 있던 커밋) |
| 리뷰 | BH(다중 감사 7렌즈) · v34 6렌즈 — `kb/reviews/` |
