---
title: "리뷰 요청 AZ — C-12 v20 (회신 AY P0 5건 + P1 전건 이행)"
date: 2026-09-01
updated: 2026-09-01
tags: [review, codex, sdcp, c12, vasp, handoff, prompt]
status: 발송 대기
kind: review-request
system: sdcp
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 AZ — `sdcp_c12_v20.zip`

> 이전 회신: 회신 AY (NO-GO · P0 5건 · P1 6건 · Q1–Q6)
> **VASP 는 여전히 한 잡도 돌리지 않았습니다.**

```
ZIP      e0fb9e14d3e737d36eb8085163ea62d67b7f56cfe5c0e676908254b889c2b8db
MANIFEST e1b935e65fa57b6c06fd3599d4642dc0dcf1735e4fe37dc7a08a957df8758222
생성기   2571759c5f85f6da79597966ab9262766fb5dc45376e30e8f36a84dbd84016ec
배포 분석기 49f0c8acc5358422c5f627fe5743f968ec14d9b6a73653d35bd78ccee933c34a
커밋     1d03cae9d638f75414ee6e3e631f0550a78eafd0   ·   git_dirty false
```

생성 인자는 v19 와 **완전히 같습니다**(`--out` 만). 잡은 **16개 그대로** — 회신 AY Q6
그대로 계산을 늘리지도 줄이지도 않았습니다.

## 1. P0 5건

### P0-1 launcher 봉인 — **지적이 정확했고, AV 판은 우회를 닫은 게 아니라 미룬 것이었습니다**

`run_staged.sh` 가 `command -v mpirun` 으로 **호출자 PATH** 에서 launcher 를 찾았습니다.
PATH 앞에 가짜 `mpirun` 을 두면 봉인된 `VASP_EXE` 를 인자로 받고도 무시하고 다른
실행파일을 돌릴 수 있었고, 영수증 분석이 그것을 통과시켰습니다.

- `SEAL_POTCAR_ROOT.sh` 가 `VASP_LAUNCHER_KIND` 와 **`LAUNCHER_BIN`(절대경로)** 을 받아
  `launcher_kind / launcher_path / launcher_sha256` 을 root seal 에 봉인합니다.
  상대경로·비실행 파일은 거부합니다.
- 러너는 **PATH 조회를 폐기**하고 봉인된 절대경로만 씁니다. 환경으로 준 `LAUNCHER_BIN`
  이 봉인과 다르면 거부합니다.
- **상 직전마다 launcher 를 재해시**해 봉인과 대조합니다 — 실행파일만 보던 종전
  검사로는 긴 실행 중 launcher 교체를 못 잡았습니다.
- 영수증이 6열 → **8열**(`launcher`, `launcher_sha256`)이 되고 분석기가 봉인과
  대조합니다.

⚠ **외주처 절차가 바뀝니다**: 봉인 시 `VASP_LAUNCHER_KIND`·`LAUNCHER_BIN` 을 주지 않으면
거부됩니다. README 와 메일 본문에 넣었습니다.

### P0-2 `RUNNER_TOKEN` — **주장을 내렸습니다** (고치지 않고)

지적대로 `.lock_bundle` 은 같은 사용자가 읽을 수 있으므로 그 값을 `RUNNER_TOKEN` 에
넣으면 직접 호출이 통과합니다. **소유권 증명이 아닙니다.** 주석·메시지에서 그 주장을
걷고 실제로 하는 일로 적었습니다 — *"사고성 직접 실행(러너를 안 거치고 잡 폴더에서
바로 `bash run_job.sh`)을 막는 표시"* 이며, 같은 사용자의 의도적 우회는 위협모델
밖(계약 문제)입니다.

사후 구분은 분석기가 집니다: 영수증의 **`_runner_start` 가 정확히 하나**여야 하고
(0이면 러너를 안 거친 실행, 2개 이상이면 이어붙인 것), 상별 실행파일·launcher 해시가
root seal 과 같아야 합니다.

### P0-3 진공 판정 — 코드 쪽으로 일원화

문서·docstring 이 `|Δ_vac| ≤ 5 meV` **그리고** 0.01 eV 반올림 일치를 요구했는데,
코드는 2026-08-31(회신 AM Q1)에 이미 반올림을 정보용으로 내렸습니다. 지적하신
`D(c1)=0.0049 · D(c2)=0.0051` 이 정확히 그 틈입니다. **hard gate 는 `|Δ_vac| ≤ 5 meV`
하나**로 통일하고 `same_rounded` 는 표시 안정성 정보로 남겼습니다.

### P0-4 governing rule — 이름은 확정, **거버넌스는 아직입니다**

- **이름**: 1저자 결정으로 **`E_ads`** 로 통일했습니다. MANIFEST 의 금지어 목록에서
  `adsorption energy` 를 걷고, 대신 `⚠_반드시_함께_적는_단서`(ko/en)를 넣었습니다 —
  *"MLIP 이완 기하 위 단일점, DFT 이온 이완 없음, 조각·표면 변형과 고정 gas conformer
  효과 포함"*. **단서는 이름이 아니라 Methods 가 집니다.**
  ⚠ 이 결정 때문에 회신 AS 8 을 강제하던 selftest("이름이 adsorption energy 가
  **아니어야** 한다")가 깨졌습니다 — 그 시험을 **"이름 금지" 에서 "단서 의무"로**
  바꿨습니다.
- **B_num**: `citable_at_0.01eV` → **`tested_axes_stable_at_0.01eV`** 로 개명하고,
  `overall_citable_at_0.01eV` 는 별도 키로 두되 ENCUT 근거가 없으므로 **`None`(모른다)**
  입니다 — `False` 가 아닙니다. `axes_not_designed` 에 ENCUT·축간 상호작용을 실제
  배열로 넣었습니다.
- 🔴 **거버넌스는 아직 안 닫혔습니다.** `D-2026-08-30-sdcp-c12-path` 가 `proposed` 인데
  좁은 C-12 노드가 전역 마감정책을 supersede 합니다. 별도 리뷰(AW P0-3)가 **불허**로
  판정했고, 간선 제거와 비준이 남아 있습니다. **이것은 이번 판에서 못 고쳤습니다.**

### P0-5 POTCAR — 1저자가 **세 번째 길**을 택했습니다

주신 두 선택지(`--potcar_pin` 재생성 / 조건부-PP 보고량 비준)가 아니라
**외주처 소관**으로 결정했습니다. pin 없이 보내고 회수 시 `POTCAR_PROVENANCE.json` 으로
사후 대조합니다. 남는 한계를 사전등록에 명시했습니다 — *"우리가 의도한 트리와 다른
트리를 썼다" 는 못 본다 → 인용 시 PAW dataset 조건부 병기*.

## 2. P1 전건

- README 부분 재실행 안내가 **코드와 반대**였습니다 — "그냥 다시 부르면 완료된 잡은
  건너뜁니다" 로 적혀 있었는데 코드는 `ALLOW_RESUME=1` 없이는 **거부**합니다. 거부가
  맞는 동작이므로(회신 AA P0-5) 안내를 코드에 맞췄습니다.
- SUBMIT 의 *"`MANIFEST.planned` 는 D3-off 를 빼서 적게 센다"* 는 **거짓**이었습니다 —
  이 묶음은 D3-off 를 0개 만들고 실물·planned 가 같습니다.
- attestation 을 **선택**으로 통일했습니다(반송 목록엔 있고 실행 절차엔 생성 단계가
  없어 갈렸습니다). 없으면 PAW release 를 조건부로만 보고합니다.
- 영수증 형식: **열 8개 정확히**(종전 `len < 6` 은 열이 남아도 통과 — 지적하신 줄바꿈
  주입이 그 틈입니다), UTC `...Z`, `nproc` 양의 정수.

## 3. Q2 — **우리 근거가 틀렸습니다**

리뷰 AY 에 저희가 적은 *"두 조각이 슬랩을 다르게 편극시키지 않는다"* 는 틀렸습니다.
D3 계수는 원자종·배위 기하에 의존하므로 그 전제는 성립하지 않습니다. 실제 근거는
하나입니다 — **D3(IVDW=11)가 SCF 에 들어가지 않으므로 고정기하 static 에서
`E_on − E_off = Edisp` 가 항등식**이고, 그래서 독립 reference-slab 항이 차의 차에서
대수적으로 소거됩니다. ⇒ C3 는 **exact-cell 차등량에 대한 전체 D3 기여**이지
조각–슬랩 쌍 분산만이 아닙니다. 결론(쌍둥이 잡 불필요)은 그대로이고 이유를
코드 주석에 정정해 박았습니다.

## 4. 검증

```
verify_zip        PASS · rc 0
배포본 selftest   300/300 PASS      (v19 294 · v18 274)
보고량 판정 검사  94건 (배포본 안)
비UTF8 로케일     PASS · k-selftest PASS
```

신설 음성시험: 가짜 launcher 해시(PATH 앞의 가짜 mpirun) · `_runner_start` 0개/2개 ·
열 수 불일치 · `nproc` 0 · 시각 형식 불량.

## 5. 여쭙는 것

**Q1.** P0-1 이 이번엔 실제로 닫혔습니까? 봉인된 절대경로 + 상별 재해시 + 영수증
대조로 **PATH 우회**는 막았다고 봅니다만, 봉인 자체를 외주처가 만드는 구조라 "봉인할 때
가짜를 봉인" 하는 경로가 남습니다. 그것은 위협모델 밖입니까, 아니면 사전 승인된 launcher
지문이 필요합니까?

**Q2.** P0-2 처럼 **고치는 대신 주장을 내리는** 처리가 이 경우 적절합니까? 아니면
lock 을 읽을 수 없게 만드는(권한·별도 채널) 실제 강화가 필요합니까?

**Q3.** `overall_citable_at_0.01eV = None` 이 맞는 표현입니까? `False` 로 두면 "0.01 eV
안정성이 없다" 로 읽히고, `None` 은 "안 재봤다" 입니다. 저희는 후자가 사실이라고 봅니다.

**Q4.** P0-5 의 세 번째 길(외주처 소관)이 **원고용으로** 성립합니까? 저희가 붙인 단서
("PAW dataset 조건부")로 충분합니까?

**Q5.** 🔴 거버넌스 간선(§P0-4 셋째)은 아직 안 닫혔습니다. **발송을 막습니까**, 아니면
결과 해석 전까지만 닫으면 됩니까?

**Q6.** 이번에도 결과를 보기 전에 더 넣거나 뺄 잡이 있습니까?

파일은 수정하지 않으셔도 됩니다 — **GO/NO-GO 와 P0/P1** 판정만 주십시오.
