# C-12 v32 발송 메일 (그대로 복붙)

> 첨부: `sdcp_c12_v32.zip` (0.6 MB · 16잡)
> 이 파일 자체는 발송 기록이다 — 보낸 뒤 고치지 않는다.

---

## 제목

```
[DFT 위탁] SDCP/PTFE–LiNiO₂ 계면 단일점 16잡 — 번들 v32
```

## 본문

안녕하세요.

지난번 말씀드린 SDCP·PTFE 바인더 계면 계산 번들을 보내드립니다. **VASP 단일점(static) 16잡**이고,
번들 안에 실행 스크립트·검증 스크립트·분석기가 전부 들어 있습니다.

### 1. 무결성 확인 (먼저 해 주십시오)

```
EXPECT_ZIP_SHA256      = ae72a179b28c344dcc91677c874a97393804b988b66f625672ee8782adea0c82
EXPECT_MANIFEST_SHA256 = f30f2b2748ddb9817fdfb9dc92c0ea841d95170cc1fce8e5a32016f5b00f51f8
```

받으신 zip 의 sha256 이 위와 다르면 **전송이 깨진 것**이니 다시 요청해 주십시오.

```bash
sha256sum sdcp_c12_v32.zip     # 위 EXPECT_ZIP_SHA256 과 대조
unzip sdcp_c12_v32.zip && cd sdcp_c12_v32
sha256sum MANIFEST.json        # 위 EXPECT_MANIFEST_SHA256 과 대조
```

### 2. 실행

⚠ **환경변수 여섯 개가 전부 필수**입니다. 하나라도 빠지면 러너가 즉시 멈춥니다
(조용히 다른 설정으로 도는 것보다 멈추는 게 낫다고 보아 그렇게 만들었습니다).

```bash
export BUNDLE_ZIP_SHA256=$(sha256sum /경로/sdcp_c12_v32.zip | cut -d" " -f1)
export EXPECT_MANIFEST_SHA256=f30f2b2748ddb9817fdfb9dc92c0ea841d95170cc1fce8e5a32016f5b00f51f8
export EXPECT_ZIP_SHA256=ae72a179b28c344dcc91677c874a97393804b988b66f625672ee8782adea0c82

export VASP_LAUNCHER_KIND=mpirun            # mpirun|mpiexec|srun|none|wrapper
export LAUNCHER_BIN=/abs/path/to/mpirun     # ★ 절대경로 (PATH 에서 찾지 않습니다)
export VASP_NPROC=48                        # 랭크 수 — 환경에 맞게
export VASP_EXE=/abs/path/to/vasp_std       # 실행파일 절대경로

bash run_staged.sh 1     # census → POTCAR 조립·봉인 → 1단계 → 판정
bash run_staged.sh 2     # 1단계가 STAGE1_PASS.json 을 낸 뒤에만
```

⛔ **배열 잡으로 한꺼번에 던지지 말아 주십시오.** 2단계가 1단계 결과에 의존해서
동시에 돌리면 결과가 무의미해집니다. 그래서 `run_all.sh` 를 일부러 안 넣었습니다.

### 3. POTCAR — 보내실 것 없습니다

**POTCAR 파일 자체는 주고받지 않습니다** (라이선스). 그쪽 트리를 그대로 쓰시면 됩니다.

`POTCAR_ASSEMBLE.sh` 가 잡마다 조립하면서 `POTCAR_PROVENANCE.json`(변형별 원본 SHA256 ·
TITEL 줄 · 조립본 SHA256)을 자동으로 만듭니다. 저희는 **그 해시로만** 대조합니다.
파일은 그쪽에 두시면 됩니다.

> 종 순서가 잡마다 다르므로 **잡별로** 조립 스크립트를 돌려 주십시오. 손으로 POTCAR 를
> 놓으면 `run_job.sh` 가 실행을 거부합니다.

**선택 — 그러나 첫 실행 전에만 가능합니다.** 저희가 결과를 원고에 인용하려면 PAW 데이터셋
release 확인이 필요합니다. `bash MAKE_POTCAR_ATTESTATION.sh` 를 **첫 VASP 실행 전에** 한 번
돌려 주시면 됩니다 (1분 · 파일 하나 생성). 안 돌리셔도 계산은 전부 정상 진행되지만,
그 경우 결과는 저희 쪽에서 **탐색용**으로 분류되고 원고에는 못 씁니다. 실행 뒤에는
다시 만들 수 없어 미리 말씀드립니다.

### 4. 반송해 주실 것

잡마다:
- `static/OUTCAR` (또는 .gz) · `static/OSZICAR`
- `static/POSCAR` — 실행된 기하 (기하 감사용, 없으면 분석이 막힙니다)
- `POTCAR_PROVENANCE.json` (조립기가 자동 생성)
- `EXECUTABLE_RECEIPT.tsv` (러너가 자동 생성)

루트에:
- `POTCAR_ROOT_SEAL.json` · `ZIP_SHA256.txt` · `STAGE1_PASS.json`

**안 보내셔도 되는 것**: CHGCAR · WAVECAR (용량) · vasprun.xml · **POTCAR**

⚠ **발산·미수렴 잡도 지우지 말고 그대로 보내 주십시오.** 실패도 판정의 일부입니다.

### 5. 예상 자원

16잡 단일점입니다. **가장 긴 잡**이 48코어 기준 중앙 추정 **약 300 시간**이고 모형 불확실성이
±2배입니다 (번들 README 의 추정 그대로 — 전체 합이 아니라 최장 잡 하나입니다). 1단계 → 2단계 순차입니다.

---

문제가 생기면 러너가 찍는 메시지를 그대로 보내 주시면 됩니다. 어디서 멈췄는지 알 수 있게
만들어 두었습니다.

감사합니다.

---

## ⚠ 보내기 전 마지막 확인 (1저자)

- [ ] 첨부한 zip 의 sha256 == `ae72a179…` (위 EXPECT 와 같은지)
- [ ] 메일 본문에 두 해시가 **정확히** 들어갔는지 (오타 나면 상대 러너가 멈춘다)
- [ ] `LAUNCHER_BIN` 줄이 살아 있는지 (이게 빠져서 v30 까지 문서대로 실행하면 exit 2 였다)
- [ ] 받는 사람 주소

## 기록

| | |
|---|---|
| 번들 | `runs/sdcp_c12_2026_08_30/sdcp_c12_v32.zip` |
| 증서 | `runs/sdcp_c12_2026_08_30/IDENTITY_v32.json` |
| 생성 커밋 | `008f1c05` (clean tree · 생성 시점에 이미 origin 에 있던 커밋) |
| 사람 확인 8가지 | 전부 PASS (IDENTITY_v32 의 `사람_확인_8가지` · ⑧ 커밋 도달성은 v31 판에서 깨져 추가) |
| 리뷰 | 회신 BF(외부 마지막) · BG(내부) — `kb/reviews/` |
