#!/usr/bin/env python3
"""SEND_MAIL_v<N>.md 렌더 (C-12 발송 메일) — 번들 README 에서 실행 블록·반송 절·walltime 문장을 **글자 그대로** 뽑는다.

  python3 tools/sdcp/c12_render_send_mail.py --bundle <sdcp_c12_v35 dir> --zip <sdcp_c12_v35.zip> \
      --commit <생성 커밋 sha> --out runs/sdcp_c12_2026_08_30/SEND_MAIL_v35.md [--variant A]

⚠ 손으로 옮기다 PP·dense 를 빠뜨린 전례가 있어 자동으로만 만든다 (v33 교훈).
   렌즈4 P1-2/P1-3/P1-4 · 렌즈5 P2(4.6일→8.16일) · P2-5(그쪽·돕니다·반말) 반영.
"""
import argparse, hashlib, json, pathlib, re

ap = argparse.ArgumentParser()
ap.add_argument("--bundle", required=True)
ap.add_argument("--zip", required=True)
ap.add_argument("--commit", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--variant", default="?")
a = ap.parse_args()

B = pathlib.Path(a.bundle)
readme = (B / "README_REQUEST.md").read_text(encoding="utf-8")
man = json.loads((B / "MANIFEST.json").read_text(encoding="utf-8"))
zsha = hashlib.sha256(pathlib.Path(a.zip).read_bytes()).hexdigest()
msha = hashlib.sha256((B / "MANIFEST.json").read_bytes()).hexdigest()
label = B.name
n_jobs = len(man.get("planned") or {})
zip_mb = pathlib.Path(a.zip).stat().st_size / 1e6

# ── 실행 블록: README 의 ```…``` 중 `run_staged.sh 1` 이 든 것 (하나여야 한다) ──
blocks = [b for b in readme.split("```") if "run_staged.sh 1" in b]
assert len(blocks) == 1, "README 실행 블록이 %d개" % len(blocks)
run_block = blocks[0].strip("\n")
# 메일에는 EXPECT 두 값을 실제 값으로 박는다 (README 는 '<메일 본문의 …>' 자리표시자)
run_block_mail = (run_block
                  .replace("export EXPECT_MANIFEST_SHA256=<메일 본문의 MANIFEST SHA256>",
                           "export EXPECT_MANIFEST_SHA256=%s" % msha)
                  .replace("export EXPECT_ZIP_SHA256=<메일 본문의 ZIP SHA256>",
                           "export EXPECT_ZIP_SHA256=%s" % zsha))
for v in ("PP=", "POTCAR_ALLOWLIST=", "BUNDLE_ZIP_SHA256=", "EXPECT_MANIFEST_SHA256=",
          "EXPECT_ZIP_SHA256=", "VASP_LAUNCHER_KIND=", "LAUNCHER_BIN=", "VASP_NPROC=", "VASP_EXE="):
    assert v in run_block_mail, "실행 블록에 %s 없음" % v

# ── 반송 절: README '## 보내 주실 것' 다음 문단들 → 다음 '## ' 전까지 ──
m = re.search(r"## 보내 주실 것\n\n(.*?)(?=\n## )", readme, re.S)
assert m, "README 에 '## 보내 주실 것' 절 없음"
ret = m.group(1).strip("\n")
assert "MANIFEST.json" in ret and "job.json" in ret and "RESULTS.json" in ret, "반송 절에 정본 항목 누락"

# ── walltime 문장: README 의 '⚠ **walltime**' 로 시작하는 불릿 (한 문장 출처) ──
mw = re.search(r"- (⚠ \*\*walltime\*\*.*?)(?=\n- \*\*POTCAR)", readme, re.S)
assert mw, "README 에 walltime 문장 없음"
wall = mw.group(1).strip()

# ── 재개 조건: MANIFEST.kconv_pair (사전등록에서 복사된 것) ──
kp = man.get("kconv_pair") or {}
reopen = next((v for k, v in kp.items() if "재개_조건" in str(k)), {}) or {}
mk = (man.get("cost_frozen") or {}).get("makespan_d") or {}
conc = int(((man.get("submission") or {}).get("max_concurrency")) or 8)
mk_c = mk.get(str(conc), mk.get(conc))
longest = round((man.get("cost_frozen") or {}).get("longest_job_h") or 0)
cores = int((man.get("submission") or {}).get("cores_per_job") or (man.get("cost_frozen") or {}).get("cores_per_job") or 48)

mail = f"""# C-12 {label.split('_')[-1]} 발송 메일 (그대로 복붙)

> 첨부: `{label}.zip` ({zip_mb:.1f} MB · {n_jobs}잡 · 전부 static)
> ⚠ 이 파일은 **자동 생성**이다 (tools/sdcp/c12_render_send_mail.py). 실행 블록·반송 목록·walltime
>   문장은 번들 README 에서 글자 그대로 뽑았다 — 손으로 고치지 마라.

## 제목
```
[DFT 위탁] SDCP/PTFE–LiNiO₂ 계면 단일점 {n_jobs}잡 — 번들 {label.split('_')[-1]}
```

## 본문

안녕하세요.

SDCP·PTFE 바인더 계면 계산 번들을 보내드립니다. **VASP 단일점(static) {n_jobs}잡**이고,
실행·검증·분석 스크립트가 번들 안에 전부 들어 있습니다.

### 1. 무결성 확인 (먼저)

```
EXPECT_ZIP_SHA256      = {zsha}
EXPECT_MANIFEST_SHA256 = {msha}
```

```bash
sha256sum {label}.zip          # 위 값과 대조 — 다르면 전송이 깨진 것입니다
mkdir -p <이 묶음 전용 빈 디렉터리> && cd <그 디렉터리>
unzip /경로/{label}.zip && cd {label}
sha256sum MANIFEST.json             # 위 값과 대조
```

### 2. 실행

⚠ 아래 변수가 **전부 필수**입니다. 하나라도 빠지면 러너가 즉시 멈춥니다
(조용히 다른 설정으로 도는 것보다 멈추는 게 낫다고 보아 그렇게 만들었습니다).
실행은 **계산 노드 할당 안에서** 해 주십시오 — 러너가 그 자리에서 잡 {conc}개를 동시에 띄웁니다.

```bash
{run_block_mail}
```

⛔ **배열 잡으로 한꺼번에 던지지 말아 주십시오.** 2단계가 1단계 결과에 의존해서
동시에 돌리면 결과가 무의미해집니다.

### 3. POTCAR — 보내실 것 없고, 조립하실 것도 없습니다

**POTCAR 파일 자체는 주고받지 않습니다** (라이선스). 귀측 트리를 그대로 쓰시면 됩니다.
**POTCAR 를 따로 조립하지 마십시오** — `run_staged.sh` 가 첫 VASP 실행 전에 `SEAL_POTCAR_ROOT.sh` 로
전 잡을 조립하고, 원본 SHA256 · TITEL · 조립본 SHA256 을 `POTCAR_PROVENANCE.json` 에 남깁니다.
저희는 그 해시로 **"{n_jobs}잡이 한 트리에서 나왔는가"** 만 확인합니다 — 귀측 트리가 어느 배포판인지는
판정하지 않습니다 (이 묶음은 탐색용 정책이라 원고 인용 자격을 주장하지 않습니다).

(선택) PAW release 를 **기록**으로 남기시려면 실행 블록의 주석 한 줄(`MAKE_POTCAR_ATTESTATION.sh`)을
`bash run_staged.sh 1` **앞에서** 돌려 주십시오 — 첫 VASP 실행 뒤에는 만들 수 없습니다. 안 돌리셔도
계산·판정은 그대로입니다. 돌리셨는데 결함이 있으면 러너가 생산 **전에** 멈추고 이유를 찍습니다.

### 4. 반송해 주실 것

{ret}

### 5. 예상 자원

{n_jobs}잡 전부 단일점(static)입니다. 기본 **동시 {conc}잡 · {cores}코어/잡**으로
계획했습니다 (그 조건에서 전체 약 {mk_c}일 — 모형이라 ±2배).
{wall}

---

문제가 생기면 러너가 찍는 메시지를 그대로 보내 주시면 됩니다.

감사합니다.

---

## ⚠ 보내기 전 확인 (1저자)

- [ ] 첨부 zip sha256 == `{zsha[:14]}…`
- [ ] 본문에 두 해시가 정확히 들어갔는가
- [ ] 실행 블록에 `PP`·`POTCAR_ALLOWLIST`·`LAUNCHER_BIN`·`VASP_EXE` 가 살아 있는가
- [ ] 받는 사람 주소

## 이 판에서 바뀐 것 (v34 → {label.split('_')[-1]})

- **선택 attestation 함정 제거**: `MAKE_POTCAR_ATTESTATION.sh` 가 VASP stdout 전문을 적고 봉인은 토큰만
  담아, 돌리면 1단계 ~{longest} h 뒤 판정이 막히는 결함(렌즈4 P0-1). 둘 다 토큰으로 통일하고,
  post_hoc 이라도 증서가 있으면 러너가 **생산 전에** 검증한다.
- **δ_k 설계 제외의 근거를 비준 사전등록에 둔다**: `3_오차예산.{kp.get('prereg_entry')}` (1저자 비준 · 안 {a.variant}).
  재개 조건은 문장이 아니라 기계 평가 구조(판정량 `D_raw_eV` · 문턱 {reopen.get('문턱_eV')} eV · 비교 `{reopen.get('비교')}`)
  로 MANIFEST 에 복사되고, 분석기가 결과에 `reopen_eval` 로 남긴다. 종전 "|ΔE_ads|<50 meV → dense 추가" 는
  비준 프로토콜 §7·§8 과 반대여서 폐기.
- `overall_citable_at_0.01eV` 는 δ_k 가 없으면 **False**(None 아님) — 문서와 기계 기록이 같은 말을 한다.
- 반송 목록에 `MANIFEST.json`·`job.json`·`RESULTS.json` 과 "통째로 압축" 을 정본으로 넣었다.
- walltime 문장 세 문서 통일 · 종 순서 목록 실물화 · dense 잔존 문구 제거 · 일정 {mk_c}일(동시 {conc}잡).

🔁 **재개 조건 (비준 사전등록에서 복사 · 결과 보기 전 선언)**
> {reopen.get('규칙')}

## 기록

| | |
|---|---|
| 번들 | `runs/sdcp_c12_2026_08_30/{label}.zip` |
| 증서 | `runs/sdcp_c12_2026_08_30/IDENTITY_{label.split('_')[-1]}.json` |
| 생성 커밋 | `{a.commit[:8]}` (clean · 생성 시점에 origin 에 있던 커밋) |
| 리뷰 | BH(다중 감사 7렌즈) · v34 6렌즈 — `kb/reviews/` |
"""
# 문체 — 외주처 문서에 남기지 않을 표현
for bad in ("그쪽", "돕니다", "판정의 일부다"):
    assert bad not in mail.split("## ⚠ 보내기 전 확인")[0], "메일 본문에 '%s' 잔존" % bad
pathlib.Path(a.out).write_text(mail, encoding="utf-8")
print("→", a.out, "| zip", zsha[:12], "| manifest", msha[:12], "| makespan", mk_c, "일 @", conc)
