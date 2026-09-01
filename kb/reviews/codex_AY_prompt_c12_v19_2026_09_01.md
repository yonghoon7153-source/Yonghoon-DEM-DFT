---
title: "리뷰 요청 AY — C-12 v19 (회신 AV P0 4건 + P1 1건 + 해제조건 ⑧ 이행 · 재생성본)"
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

# 리뷰 요청 AY — `sdcp_c12_v19.zip`

> 이전 회신: `kb/reviews/codex_AV_reply_c12_v18_2026_08_31.md` (NO-GO · P0 4건 · P1 1건 · 해제조건 8)
> **VASP 는 여전히 한 잡도 돌리지 않았습니다.**

```
ZIP      c423b0821ced031f8ac676fd007a2b95bbbbf3d4760c19995976c1bb616b3b36   (414,332 B)
MANIFEST 6d8dd2f4bf9f7217f36f255f7c47a82fa66d5bc3619499050dbdb5db20a3fb7f
생성기   263e9a807fa7e61475f5da3e89e18ba22b07cf77ac032c03e644e60268d80bee
배포본 분석기 e108537817d2b27beaaf4c6f812aeacac6cbc858f41e749ec589ccae9ff68030
커밋     3817eb5dda9b87a2109bf4c09e285a8f5699c9a1   ·   git_dirty **false**
```

생성 인자는 v18 의 `generated_argv` 를 **`--out` 만 바꿔 그대로** 썼습니다 — 같은 입력이어야
v18↔v19 차이가 “고친 것”만 남습니다. 계산은 하나도 늘리지 않았습니다(회신 AV Q6).

## 1. P0 4건 + P1 1건 — 무엇으로 막았는가

### P0-2 런처 우회 — **자유형 문자열을 폐기했습니다**

지적이 정확했습니다. 자유형 launcher 문자열은 이길 수 없는 게임이었습니다 — PATH 상의
이름이 `-x` 검사를 통과하고, basename 위조가 되고, `env` 는 인자 문법 자체가 실행입니다.

- `VASP_LAUNCHER_KIND` **enum**(`mpirun|mpiexec|srun|none|wrapper`) 으로 바꾸고,
  argv 는 **러너가 조립**합니다. 사용자 문자열이 명령줄에 들어가지 않습니다.
- `RUNNER_TOKEN` = 락 파일 **내용**을 소유권 증명으로 씁니다 — `run_job.sh` 직접 실행 차단.
- 단계마다 실행파일을 **재해시**해 root seal 과 대조하고, `EXECUTABLE_RECEIPT.tsv` 를
  **분석기가 읽는 필수 반송물**로 만들었습니다 (없으면 값이 안 나옵니다).

음성 시험을 실제로 `run_staged.sh` 를 돌려 rc≠0 로 확인합니다: legacy 문자열 · `env` 를
KIND 로 위장 · 잘못된 nproc · wrapper 없이 wrapper 선언 · 남의 락 · 영수증 결측/위조/
실행파일 불일치/단계 누락.

### P0-3 C1·C3 의 clean slab 의존 — **대수적으로 소거됩니다**

슬랩 Edisp 는 두 조각에 **공통 상수**이므로 D 의 차의 차에서 소거됩니다. 그래서
clean slab 을 C3 의 입력에서 뺐고, `vacconv` c2 잡은 **자세가 아니라 진공 탐침**으로
분리했습니다(자세 수에 세지 않습니다). C1 은 이 묶음이 절대 E_ads 를 정의하지 않으므로
`"n/a — …"` 를 명시적으로 냅니다 — **`n/a` 와 `unresolved` 를 구분**합니다(후자는 약속
불이행이라는 뜻이므로).

이번 산출 로그가 그 결과를 그대로 보여줍니다:
`D3-off 쌍둥이 0개 — C3 는 Edisp 로 낸다 (쌍둥이는 정보가 0)`.

### P0-4 반송 계약 — **한 정본을 세 곳에 축자 렌더**

README·SUBMIT·MANIFEST 의 세 사본이 갈라져 `KCONV_NOT_MEASURED`·
`CANARY_GEOM_UNCHECKED` 거부를 낳았습니다. 이제 `_return_contract(man)` 하나가 정본이고
세 문서는 그것을 **축자 렌더**합니다. 렌더 동일성 자체를 회귀시험으로 겁니다.

### P1-5 수치 예산 — **D_raw 와 인용 자격을 분리**

- `D_raw` 는 유효 입력이면 **항상 보존**합니다(예산 초과가 값을 지우지 않습니다).
- `B_num` 은 **“시험한 세 축의 보수적 sensitivity envelope”** 이고 **총 오차 상한이
  아닙니다** — 설계에 없는 축(ENCUT·교차항)은 `axes_not_designed` 로 **명시**됩니다.
- `citable_at_0.01eV` 를 방향 판정과 분리했습니다. 구간 `[D−B, D+B]` 가 가드(−0.10) 이하로
  **전부** 들어가면 보고 가능, 가드나 0 을 가로지르면 `NO_CLAIM`/`NO_DIRECTIONAL_CLAIM`,
  축 결측·상태 전이·기하/계약 실패일 때만 `NO_VALUE` 입니다.

### 해제조건 ③⑦

`coverage_scope` 를 “주기영상 항의 소거를 **주장하지 않는다**” 로 재서술하고, 철회된 문구를
스스로 인용하지 못하게 하는 회귀시험을 넣었습니다(철회 기록 안의 정당한 인용은 예외 처리).

## 2. 검증 — 실물로 돌린 것

```
verify_zip        PASS · rc 0 · 입력 preflight 게이트 0건(job.json 16개) · 해시확인 110/110
배포본 selftest   294/294 PASS      (v18: 274/274)
보고량 판정 검사  94건 (배포본 안)  (v18: 87건)
비UTF8 로케일     PASS (env -u PYTHONIOENCODING LC_ALL=C PYTHONUTF8=0)
k-selftest        PASS
zip_entry_hazards []
```

산출물에서 **직접 센** 구성(설명문이 아니라 실물):
`references 8(endpoints) · complexes 8(pose×seed) · d3_off_twins 0 · audit_pose 0 · 총 16잡`,
디스크상 `static 16 · dense 2`.

## 3. 알고 보내는 한계 — 숨기지 않습니다

1. **POTCAR pin 없음.** `--allow_no_pin` 을 v18 argv 그대로 승계했습니다. 회수 시
   `POTCAR_PROVENANCE.json` 으로 **사후** 대조하고 `run_job.sh` 는 그 파일 없이는 돌지
   않지만, *“우리가 의도한 트리와 다른 트리를 썼다”* 는 못 봅니다.
2. **calibration·audit 자세 0개.** 결함이 아니라 회신 AI §A-Q4 = C 채택의 결과입니다
   (H1·holdout·calibration/holdout merge·adaptive δ 를 실행 경로에서 제거).
3. **단일점.** relax 상이 없습니다 — 고정 기하 위의 단일점이 보고량 정의의 일부입니다.

### 🔴 번들 **밖**에 남은 것 셋 (우리가 아직 못 닫았습니다)

- `sdcp_c12_protocol_2026_08_30.json` 이 잡 수를 **§0 12잡 · §12 19잡** 으로 적어 실물
  **16잡**과 다릅니다. 인용위험 원장에는 올렸지만 파일은 안 고쳤습니다.
- 같은 프로토콜 §1 이 보고량을 `adsorption energy` 라 부르는데, `sdcp_c12_claim_prereg_
  2026_08_31.json` 은 그 이름을 **금지어**로 지정했습니다. **사전등록 둘이 충돌**합니다.
- 거버넌스: `D-2026-08-30-sdcp-c12-path` 를 `proposed` 로 소급 등록했으나, 별도 리뷰(AW)가
  **proposed successor 가 전역 policy 를 폐기한 간선은 불허**로 판정해 그 간선 제거가
  선행돼야 합니다.

## 4. 여쭙는 것

**Q1.** P0-2 의 KIND enum 이 현장에서 **너무 좁습니까?** `aprun`·`jsrun`·`ibrun` 을 뺐고
`wrapper` 하나로 받게 했는데, 외주처가 자체 래퍼를 쓰면 그 래퍼 자체가 다시 자유형입니다.
이 설계가 우회를 정말 닫습니까, 아니면 한 겹 미뤘을 뿐입니까?

**Q2.** P0-3 의 “슬랩 Edisp 는 차의 차에서 소거된다” 는 **IVDW=11(D3) 의 슬랩 항이 조각과
무관하게 같다**는 가정 위에 있습니다. 두 조각이 슬랩 원자 위치를 (고정 기하라도) 다르게
편극시키지 않으므로 성립한다고 봤습니다 — 이 논증이 맞습니까?

**Q3.** P1-5 의 `B_num` 을 “총 오차 상한이 아니다” 로 낮춘 것이 **인용 문구에 충분히
반영됐습니까?** 지금은 `citable_at_0.01eV` 가 참일 때도 세 축 밖의 오차는 언급되지 않습니다.

**Q4.** §3 의 **POTCAR pin 없음**을 이대로 보내도 됩니까, 아니면 `--potcar_pin` 으로 다시
만들어야 합니까? 다시 만들면 해시가 전부 바뀝니다.

**Q5.** §3 의 번들 **밖** 세 건 중 **외주 발송 전에 반드시 닫아야 하는 것**이 있습니까?
저희 판단은 “셋 다 발송을 막지는 않는다(외주처가 읽는 것은 번들 안 문서다)” 인데,
사전등록 충돌은 **결과 해석 시점**에 문제가 되므로 그 전에 닫아야 한다고 봅니다.

**Q6.** 이번에도 **결과를 보기 전에** 더 넣거나 빼야 할 잡이 있습니까?

파일은 수정하지 않으셔도 됩니다 — **GO/NO-GO 와 P0/P1** 판정만 주십시오.
