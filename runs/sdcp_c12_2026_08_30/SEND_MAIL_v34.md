# C-12 v34 발송 메일 (그대로 복붙)

> 첨부: `sdcp_c12_v34.zip` (0.6 MB · 16잡 · 전부 static)
> ⚠ 이 파일은 **자동 생성**이다. 실행 블록·반송 목록을 손으로 고치지 마라 —
>   번들 README 에서 뽑은 것이고, 손으로 옮기다 `PP`·`dense` 를 빠뜨린 전례가 있다.

## 제목
```
[DFT 위탁] SDCP/PTFE–LiNiO₂ 계면 단일점 16잡 — 번들 v34
```

## 본문

안녕하세요.

SDCP·PTFE 바인더 계면 계산 번들을 보내드립니다. **VASP 단일점(static) 16잡**이고,
실행·검증·분석 스크립트가 번들 안에 전부 들어 있습니다.

### 1. 무결성 확인 (먼저)

```
EXPECT_ZIP_SHA256      = a58acad824b2b7bd621f30ed992585ec453ce86b84ab00b4fd51fabd0a5fbb59
EXPECT_MANIFEST_SHA256 = f13371a1cb9167b48873b9c59a7ab9e9a096a35548c74f058fefb11a522b9134
```

```bash
sha256sum sdcp_c12_v34.zip          # 위 값과 대조 — 다르면 전송이 깨진 것입니다
unzip sdcp_c12_v34.zip && cd sdcp_c12_v34
sha256sum MANIFEST.json             # 위 값과 대조
```

### 2. 실행

⚠ 아래 변수가 **전부 필수**입니다. 하나라도 빠지면 러너가 즉시 멈춥니다
(조용히 다른 설정으로 도는 것보다 멈추는 게 낫다고 보아 그렇게 만들었습니다).

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
export EXPECT_MANIFEST_SHA256=<메일 본문의 MANIFEST SHA256>
export EXPECT_ZIP_SHA256=<메일 본문의 ZIP SHA256>

# ── 실행 방식 ──
# ⛔ 자유형 launcher 문자열(VASP_CMD·VASP_LAUNCHER)은 **폐지됐습니다** (회신 AV P0-2) —
#    문자열 검사는 우회가 가능해, 종류와 수만 받고 실행 명령은 러너가 조립합니다.
export VASP_LAUNCHER_KIND=mpirun            # mpirun|mpiexec|srun|none|wrapper
export LAUNCHER_BIN=/abs/path/to/mpirun     # **필수** — PATH 에서 찾지 않습니다. 없으면 exit 2
export VASP_NPROC=48                        # 랭크 수 (잡 하나당)
export VASP_EXE=/abs/path/to/vasp_std       # 실행파일 절대경로 (봉인 대상)

# ⚠ 러너는 기본으로 잡 8개를 **동시에** 띄웁니다 (= 8 × VASP_NPROC 랭크).
#    할당이 그보다 적으면:  export JOBS_PARALLEL=<할당코어 ÷ VASP_NPROC>

bash run_staged.sh 1     # census → POTCAR 조립+봉인 → 봉인 census → 1단계 → 판정
bash run_staged.sh 2     # 1단계 통과(STAGE1_PASS.json) 뒤에만
```

⛔ **배열 잡으로 한꺼번에 던지지 말아 주십시오.** 2단계가 1단계 결과에 의존해서
동시에 돌리면 결과가 무의미해집니다.

### 3. POTCAR — 보내실 것 없습니다

**POTCAR 파일 자체는 주고받지 않습니다** (라이선스). 그쪽 트리를 그대로 쓰시면 됩니다.
`POTCAR_ASSEMBLE.sh` 가 잡마다 조립하며 `POTCAR_PROVENANCE.json`(원본 SHA256 · TITEL ·
조립본 SHA256)을 만듭니다. 저희는 **그 해시로만** 대조합니다.

⚠ PAW release 를 원고에 적으려면 `MAKE_POTCAR_ATTESTATION.sh` 가 필요한데, **첫 VASP
실행 전에만** 만들 수 있습니다. 자세한 절차는 번들의 `POTCAR_ATTESTATION_REQUEST.md`
에 있습니다 (필요 변수가 더 있습니다). 안 돌리셔도 계산은 정상 진행됩니다 — 다만 그
경우 결과는 저희 쪽에서 dataset 신원 기록 없이 남습니다.

### 4. 반송해 주실 것

⚠ **푼 디렉터리를 통째로** 다시 압축해 주십시오 (배포 입력·MANIFEST 포함).
아래는 그 안에 **반드시 있어야 하는 산출물** 목록입니다.

## 보내 주실 것

**정본은 `MANIFEST.json` 의 `return_contract`** 이며 이 목록은 그 렌더입니다
(README 와 SUBMIT_CONTRACT 어디를 보셔도 같습니다 — 회신 AV P0-4).

각 잡 폴더에서:
- static/OUTCAR (또는 .gz)
- static/OSZICAR
- static/POSCAR — **실행된 기하** (부모↔canary 기하 대조·기하 감사. 없으면 CANARY_GEOM_UNCHECKED 로 막힙니다)
- POTCAR_PROVENANCE.json (조립기가 자동 생성)
- EXECUTABLE_RECEIPT.tsv — 상별 실행파일 해시 (run_staged 경로가 자동 생성 · 분석기가 root seal 과 대조합니다)

묶음 루트에서:
- POTCAR_ROOT_SEAL.json (첫 실행 전 봉인)
- ZIP_SHA256.txt
- STAGE1_PASS.json (1단계 통과 receipt)
- POTCAR_ATTESTATION.json — **선택** (탐색용 정책). 없어도 러너는 돕니다. ⚠ 다만 그 결과는 **원고 인용 자격이 없습니다** — 사후 provenance 는 무엇을 썼는지만 기록하고 그것이 승인된 PAW dataset 인지 판정하지 못합니다 (회신 AZ P0-7·Q4). 만들려면 `MAKE_POTCAR_ATTESTATION.sh` 를 **첫 VASP 실행 전에만** 돌릴 수 있습니다 (회신 AR P0-6)

보내지 않으셔도 되는 것: CHGCAR·WAVECAR (용량) · vasprun.xml (선택)
⚠ 발산·미수렴 잡도 지우지 말고 그대로 — 실패가 판정의 일부다

### 5. 예상 자원

16잡 전부 단일점(static)입니다. **가장 긴 잡**이 48코어 기준 중앙 추정 **약 111 시간**
이고 모형 불확실성이 ±2배입니다. 기본 동시 8잡으로 계획했습니다.

---

문제가 생기면 러너가 찍는 메시지를 그대로 보내 주시면 됩니다.

감사합니다.

---

## ⚠ 보내기 전 확인 (1저자)

- [ ] 첨부 zip sha256 == `a58acad824b2…`
- [ ] 본문에 두 해시가 정확히 들어갔는가
- [ ] 실행 블록에 `PP`·`POTCAR_ALLOWLIST`·`LAUNCHER_BIN` 이 살아 있는가
- [ ] 받는 사람 주소

## 이 판에서 바뀐 것

**dense(k 수렴) 2잡을 설계에서 뺐다** — 최장 잡 299.6 h → 111 h, 전체 12.5일 → ~4.6일.

⛔ 잃는 것: `ΔE_ads` 는 그대로 나오지만 **"0.01 eV 안에서 안정하다" 는 주장을 못 한다.**
진공·기체 두 축만 시험했다고 쓴다.

🔁 **재개 조건 (결과 보기 전에 선언 · MANIFEST 에 박힘)**
> |ΔE_ads| < 50 meV 이면 dense 2잡(primary complex 두 개)을 추가로 돌린다.
> (k 가드밴드가 10 meV 다 (GUARD_EV). 그 5배를 문턱으로 둔다 — 그 위면 k 오차가 부호·크기 판정을 못 바꾼다.)

이 조건 밖의 이유로 dense 를 추가하면 그것은 "결과를 보고 게이트를 바꾼 것" 이다.

## 기록

| | |
|---|---|
| 번들 | `runs/sdcp_c12_2026_08_30/sdcp_c12_v34.zip` |
| 증서 | `runs/sdcp_c12_2026_08_30/IDENTITY_v34.json` |
| 생성 커밋 | `2382b6d5` (clean · 생성 시점에 origin 에 있던 커밋) |
| 사람 확인 8가지 | 전부 PASS |
| 리뷰 | BF(외부 마지막) · BG(내부) · BH(다중 감사 7렌즈) — `kb/reviews/` |
