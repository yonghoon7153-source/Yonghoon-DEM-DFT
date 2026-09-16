# 진행 상태 — α·β 검증 하네스

> **이 파일이 "지금 어디까지 왔나" 의 정본이다.** 수치의 정본은 `FINDINGS.md` + `out/`.
> 갱신 규칙: 단계가 열리거나 닫히면 **그 커밋에서 같이** 고친다.

**목표가 바뀌었다 (2026-09-11, 사용자 결정).** 코드를 준 분이 은퇴하며 사용자가
**전권**을 받았다. 규진팀에 회신하지 않고 **우리 독자 모델로 발전**시킨다.
그러므로:
- `FOR_BMS_TEAM.md` 는 더 이상 산출물이 아니다 — **보관**(배너로 표시, 갱신 안 함).
- 검증 하네스의 발견은 "남의 코드 감사" 에서 **"우리가 물려받은 코드의 감사 +
  새 모델의 설계 요구서"** 로 역할이 바뀐다. 새 모델의 출발점은 리뷰가 남긴 **관측**이다
  — PE 기준 처리가 답을 %p 단위로 바꿈 · 원통형의 적합 잔차가 사이클과 함께 커짐 ·
  선택된 γ 쌍의 진폭비 3~16 % · 블렌드 vs 측정 음극 rms 19~24 mV. "모델 부적합"
  은 그 관측들을 함께 설명할 **후보 가설**이지 확인된 원인이 아니다 (Codex R3-01·02:
  정확한 모델 + 상태별 잡음, 정확히 표현 가능한 곡선이 같은 표·같은 비를 낸다).
  새 모델의 요구서는 `관측 → 후보 원인 → 구분 시험 → 채택 기준 → 남는 한계` 로 쓴다.
- 규진팀에 물어봐야 닫히던 U1(전사 함수 2 개)·U2(pOCV 원자료 여부)는 이제 **우리가
  원본 코드·원자료를 직접 열어** 닫을 수 있다.
- 원자료는 여전히 public 저장소에 넣지 않는다 (전권 ≠ 공개). 바꾸려면 사용자 결정.
- 게이트(`degradation-degeneracy/`)는 본체 브랜치 일이다 — 이 브랜치는 R2 원장을
  끝까지 닫고 R3 를 받는다.
  *(2026-09-15 갱신: 사용자 결정으로 **본진이 이 디렉터리를 흡수했다.** 서브
  브랜치에 새 커밋을 얹지 않고 `bms-balancing/` 도 본진
  `claude/14-gate-code-review-9qkx05` 에서 직접 고친다. 정본은 루트 `CLAUDE.md`
  하드룰 1, 경위는 `BRANCHES.md`. 아래 "이 브랜치" 표현은 그 이전의 기록이다.)*

최종 순서(갱신): R2 원장 닫기 → R3 리뷰(GO 까지) → 새 모델 설계 요구서

---

## 지금 상태 — **R14 가 열어 둔 셋을 닫았다 (R15, 2026-09-15)**

Codex R14 는 GO 였지만 §7 의 답 2·3·4 를 "다음 라운드" 로 남겼다. 그 셋을 구현으로 닫았다.
서사와 실측은 `reviews/R14_RESPONSE.md` §8, 기록된 결정은 `reviews/PROMOTION_DECISIONS.json`.

| 항목 | 무엇이 없었나 | 무엇이 생겼나 |
|---|---|---|
| U18-05 (§7-3) | sidecar 마다 커밋이 40-hex 인지만 봤다 — **묶음이 한 코드 상태에서 나왔는가**는 아무도 안 봤다 | `blocked_by.bundle_commits` (혼재 = rc 2) · 예외는 **정확한 full commit 집합**에만 걸리는 기록 |
| `legacy_transition_approved` (§7-2) | 옛 정본과의 일회성 이관과 일반 승격을 가를 판정이 없었다 | 판정 둘(`legacy_transition_approved` · `legacy_transition`) — `promotion_eligible: false` 와 rc 4 는 **그대로** |
| 기록용 CLI 인자 (§7-4) | 부르는 쪽만 고쳤고 CLI 는 침묵으로 `out` 을 가정했다 | 생략·빈 문자열은 rc 2 · 옛 기본값은 `--default-out-diagnostic` 으로만 |

RED 관측: `tests/test_r15_open_items.py` 첫 실행 **12 failed · 2 passed** (통과한 둘은 "바뀌지
않는다" 를 재는 대조군). GREEN **15 passed**, 전체 **326 passed**.

**넷째가 실전에서 하나 더 나왔다 (2026-09-15).** 사용자가 `preserve_handoff.sh` 로 COMSOL
`physical600_b` 원문을 보존했는데, 스크립트가 마지막에 찍는 안내가 **본진이 흡수한 서브
브랜치로 push 하라**고 말하고 있었다. 그대로 따랐으면 새 커밋을 얹지 않기로 한 브랜치에 1 GB
짜리 보존 커밋이 올라갔을 것이다. 요청문 쪽은
`test_review_request_clones_the_branch_that_owns_bms_balancing` 이 막고 있었고 **스크립트
쪽은 아무도 안 봤다** — 2026-08-20 에 여덟 곳이 대체된 이름을 붙들고 있던 것과 같은 형태다.
이름을 루트 `CLAUDE.md` 의 브랜치 표에서 읽게 고쳤고, `scripts/*.sh`·`*.py` 전체를 훑는 회귀
(`…_push_to_a_retired_branch`)로 고정했다. 주석에도 옛 이름을 적지 않는다 — 이름을 옮겨
적지 않는 것이 규칙이기 때문이다.

**같은 안내문에서 하나 더.** 재대조 python 블록이 **저장소 루트 기준** 경로를 쓰는데 그 명령을
찍는 자리는 `bms-balancing/` 안이라, 복사해 친 사람이 `FileNotFoundError` 를 봤다. 블록 앞에
루트로 옮기는 줄을 넣고(그 위 git 세 줄은 이 디렉터리 기준이라 그대로 둔다) 회귀로 고정했다
(`…_printed_recheck_block_says_where_to_stand`). **안내문은 사람이 그대로 붙여 넣는 코드다** —
코드와 같은 규율로 본다.

fail-closed 실측 — `PROMOTION_DECISIONS.json` 을 치우면 정본 `out/` 이 `rc 2 · bundle_commits 1`
로 떨어지고 `066866595ab7 (9 개) · 419c1abaeec9 (4 개)` 를 이름으로 지목한다. 예외가 사라지면
조용히 넘어가지 않는다.

전수 실행이 **이번 라운드와 무관한 빨강 둘**도 드러냈다: `CODEX_REVIEW_REQUEST.md` 가 흡수된
서브 브랜치를 clone 하라고 적고 있던 것(2026-09-15 흡수 뒤 전수를 안 돌려서 안 드러났다)과,
시험을 더해 낡은 기대 개수. 둘 다 고쳤다.

**COMSOL (2026-09-15)**: 물리축 B(300→600) 원문이 저장소에 들어왔고 **우리가 원시 CSV 로 다시
셌다** — `scripts/recheck_physical600_b.py`. 여덟 창 전부에서 묶음 보고값·수신 측 재계산·우리
재계산이 표본 수·최대값·최대 시각·전극·위치까지 같다. 시간 이력(986 구간)도 재계산으로 확인했다.
`docs/COMSOL_REBUILD_SPEC.md` §19 의 전달값 배너를 내렸다.

**인계 (2026-09-15, §23).** codex 토큰 소진으로 COMSOL 갈래가 인계됐다. 인계 묶음의 문서
셋을 보존하고 본체 ZIP(548 MB · 항목 201)은 지문과 구성만 남겼다. 읽어 보니 **A 단계 구현이
이미 끝나 있었다** — Java·launcher·별도 분석기·출력 계약·합성 시험 38 통과. §22 의 "아직 코드가
없다" 를 정정했다 (리뷰어에게 제출되지 않았다는 뜻이었다). 실물 미시험은 넷으로 남아 있고
준비 문서가 "A 통과는 그 항목들의 성공 증거가 아니다" 라고 스스로 적었다. 인수자 경고 하나가
제일 중요하다 — **다른 PC 에서 기존 launcher 를 그대로 실행하지 말 것** (절대 경로가 박혀 있다).
본체 ZIP 안의 manifest 지문 넷이 우리 보존 묶음과 일치한다.

**A 준비본 수신 검토 — B 는 NO-GO (2026-09-15, §24).** 그 준비본이 수신 측으로 건너가 독립
검사를 받았고 **세 자리가 막혔다**. 포장은 깨끗했고(144,120 B · `a0fc89f9…` · 31 payload +
manifest, 집합·CRC·크기·SHA 전부 통과) 합성 시험 38 개도 그 기계의 짧은 경로에서 다시 통과했다
(failure 0 / error 0, 약 5.687 초 — 처음 깊은 경로의 failure 1/error 3 은 경로 관련
`FileNotFoundError` 라 COMSOL 결함으로 세지 않았다). 막힌 셋: **P1-R1** 기대 속성 1,143 중
소비자가 991 만 고른다(`sol1/v2` 152 제외) → 값이 전부 맞아도 거부 · **P1-R2** 새 Java `row()`
가 플랫폼 줄바꿈(Windows CRLF)인데 계약이 SHA 로 고정한 기준 표는 LF (5,444→5,477 ·
5,446→5,479 bytes, parsed cell 동일) → raw SHA 대조 실패 · **P1-R3** `Li_N` 단위 하나만
`mol/m^2 → mmol/m^2` 로 바꿔도 overall `COMPLETE_WITHIN_DECLARED_RECOVERY_SCOPE`.
**셋 다 우리가 이미 값을 치른 축이다** — R2 는 `U14-01`(줄끝이 서명을 깬다) · R3 는
`R11 P1-9`(신고된 위험은 값으로 소비한다) · R1 은 CLAUDE.md 작업규율 2(fixture 가 진실을
가린다 — 저쪽 양성 fixture 는 expected 를 `sol1/t1/rtol` **키 하나**로 줄여 접점을 지나가지
않았다). 검토자가 경계를 직접 적었다 — **"복구 경로를 폐기한 판정이 아니라 B 전에 해결 가능한
A 구현 접점 문제를 분리한 판정"**. 순서는 **A 보완 → 재검토 → B 별도 승인**이고 `approved` 는
false 그대로다. 우리 쪽 COMSOL 호출 0 · 제출 코드 수정 0 · 승인 JSON 변경 0.

`COMSOL_REBUILD_SPEC.md` 에 §20~§24 를 더했다 — §20 Desktop 부분 회수(우리 재계산) ·
§21 그 앞 이야기(정상 guard 가 후처리에서 죽고 API 복구가 파일 읽기에서 막힌 것) ·
§22 저장 해 API 경로의 실행 전 검토와 **우리 쪽 A 단계 검토 기준 여섯**.

Desktop 부분 후처리(§20)는 보존이 한 번 멈췄고 **원인이 우리 스크립트였다.** 그 묶음의
manifest 이름은 `manifest.json` 인데 `preserve_handoff.sh` 가 `package_manifest.json` 만
찾았다. ZIP 의 크기·SHA 는 전달값과 정확히 일치했고 `manifest.json` 의 해시도 전달값 그대로였다 —
스크립트가 찾은 것은 재사용 증거로 딸려 온 **이전 묶음의** package_manifest 하나뿐이었다.
후보 집합만 넓혔다 (고르는 것은 여전히 `--expect-manifest-sha`, fail-closed 유지).
보존은 그 뒤 통과했다 — 명세 82 전수 일치 · 보존 50 · 커밋 안 bytes 재대조 50/50.

**그 다음 셋이 또 멈췄다 — 이번엔 목록 키였다.** guard·복구 기록·수신 검토 기록이 5 단계에서
`manifest 에 entries 가 없다` 로 섰는데, ZIP 크기·SHA·manifest 해시는 셋 다 전달값과 정확히
일치했다. 다른 것은 자료가 아니라 **키 이름**이다: `entries`(desktop) · `files`(guard·review) ·
`payload`(recovery). 항목 모양은 셋 다 같다 (`path`·`bytes`·`sha256`). 판별을
`scripts/handoff_manifest.py` 한 자리로 빼고(bash heredoc 안에 두면 시험할 수 없다) 아는 키만
넓혔다. 모르는 모양·둘 이상 후보·`path`/`sha256` 누락은 **계속 멈춘다**.

**남은 열린 것**: 조건 6(동적 인증) · 조건 8(다섯 축) ·
r11 `publish:profile_partial_stdout` 대체 증거. (**`openpyxl` 은 R16 에서 닫았다 — 아래.**)

**R16 (2026-09-16) — `openpyxl` 을 env 축에 넣었다.** 리뷰어 정적 지적을 닫았다. 과학 입력이 전부
`pd.read_excel` 로 읽히고 pandas 는 **openpyxl 로** xlsx 를 연다 — C18 이 pandas 를 넣은 것과 같은
논거다(`ENV_KEYS` 는 `env_signature()` 가 적는 것 **전부**여야 한다).

**어려운 자리는 계약이 아니라 이미 게시된 정본이었다.** 축을 그냥 더하자
`check_u14 --new out --schema-only` 가 **rc 0 → rc 2**, 정본 13 개가 전부 계약 위반이 됐다 (실측).
그 묶음은 사용자 기계의 실데이터 재실행으로 승격한 것(`37a889b`)이라 다시 만들 수 없다.

**처음 설계를 버렸다.** "openpyxl 이 없으면 나이" 로 **축의 이름으로** 면제하려 했는데, 그러면
`test_h02` 가 재는 계약("한 축씩 빼도 전부 걸려야 한다")이 그 축에 대해 **영구히** 약해지고 누구든
그 축을 지워 통과한다. 면제를 `reviews/PROMOTION_DECISIONS.json` 의 **기록된 결정**으로 옮겼다 —
`env_contract_legacy` 항목이 산출 이름 · **sha256** · **그때의 env 값 전부**를 고정하고, 셋이 전부
맞고 그 축이 **키째 없을 때만** 면제한다. 면제는 `UNKNOWN_BLOCKERS` 라 **승격은 계속 불가**다.

**내가 연 구멍 셋을 시험이 잡았다** (전부 RED 로 고정): ① 면제가 산출 bytes 만 보고 사이드카 env 를 안
봐서 **축만 `""` 로 비운 조작본이 통과**했다 (`test_r16_06`) → 기록이 env 값까지 고정. ② `env_legacy` 를
`not_promotable` 에 그냥 넣자 `--schema-only` 가 rc 0 → **rc 4** 가 됐다 (코드가 명시적으로 금지한 것)
→ "승격 대조를 물었을 때만" 으로 좁힘 (`test_r16_08`). ③ env 계약이 **사이드카와 degeneracy 본문 두
자리**에서 강제되는데 한쪽만 면제해 같은 bytes 가 한 검사는 통과하고 다른 검사는 막혔다 →
`check_degeneracy(env_exempt=…)` 로 같이 닿게 함.

**fixture 가 아홉 번째로 깨졌다.** 축을 더하자 15 건이 빨갰고 원인은 전부 같았다 — 여러 fixture 가
5 축짜리 env 를 **각자 박아** 쓰고 있었다. `tests/conftest.py` 의 `fixture_env()` **한 자리**로 모았고,
축이 또 늘면 거기서 먼저 크게 깨진다 (R14 P2-2 의 "규칙이 두 벌" 과 같은 축). 오류 문구의
"환경 축 **다섯**" 도 걷어냈다 — 개수를 박으면 축을 더할 때 문구가 거짓이 된다.

**⚠ 사용자 결정이 필요한 것 하나.** `U18B-2026-09-14` legacy transition 기록이 스스로 **"이 승인은
unknown 사유 **둘**만 덮는다"** 고 적어 두었는데 R16 이 셋째(`env_contract_legacy`)를 만들었다. 셋째를
그 기록에 끼워 넣는 것은 **기록된 사용자 결정을 고쳐 쓰는 일**이라 하지 않았다 — 승인은 fail-closed 로
사라진다 (rc 4 · 승격 false · 계약 축 0 은 그대로). 되살리려면 **새 기록**이 필요하다. U18B 는 이미
끝난 이관이라 실무 영향은 없다.

**실데이터 폭 측정(`--w-dqdv 0 ↔ 1`) — 파일럿이 돌았다 (2026-09-15, `BML_R1_RESPONSE.md` §14).**
사용자 기계에서 HD_knee `--cycles 0,1,2` · `--starts 20 --seed 0 --scale-seed 0` ·
`--widths --width-tol 0.01 --width-starts 4` 로 두 번, `--w-dqdv` **한 줄만** 다르게 돌았고
`width_report --axis w_dqdv` 가 **rc 0** 을 냈다 (축 하나만 달랐다는 것을 기계가 확인 — 20 개
설정·입력 sha·env·git `fe26daff` 전부 동일). **답은 "안 좁아진다"**: LAM_PE 3.137→3.388 %p
(1.08배) · **LAM_NE 2.439→7.099 %p (2.91배)** · LLI 1.172→1.402 %p (1.20배). 가장 무거운 것은
`w_dqdv 1` 의 cycle 1 에서 LAM_NE 가 **[−0.60, +6.50] %p 로 0 을 가로질러 부호 식별을 잃은 것**
(`w_dqdv 0` 에서는 [6.59, 9.02]). 난간이 같은 자리를 독립으로 짚었다 — w1 에만 warning
`a_NE: lb 접촉 1/3 · 최소 거리 0.000e+00`. **LLI 는 두 설정 모두에서 가장 좁다** — 축퇴 행렬(§3)·
pyDMA(§12)에 이어 **세 번째 경로**로 같은 결론. `check_rails` 둘 다 rc 0 (error 0). 산출은
커밋하지 않는다 — 정본은 사용자 기계의 `~/out_widths/pilot_w{0,1}/`.

**그 자리에서 발견 하나 (W-19, 닫음).** 내가 런북에 `check_u14 --new w1 --old w0` 을 쓰라고 적은
것이 잘못이었다 — u14 는 승격 게이트라 "안 고쳤으니 같아야 한다" 를 묻는데 우리는 축을 일부러
바꿨다. 런북을 `--schema-only` 로 고쳤다. 다만 그 출력이 **`blocked_by.controls = 0`** 을 보여
줬다: `w_dqdv` 가 `CYCLES_META_CONTROLS` 에 **없어서** 일부러 바꾼 축이 "설명 없는 숫자 변화
58" 로 보고됐다 (`seed` 축은 목록에 있어 §10-5 에서 `controls 1` 로 잡혔다). **`width_report.py`
는 같은 축을 이미 견주고 있었다 — 두 자가 다른 것을 재고 있었다.** RED
(`tests/test_cycles.py::test_cy_11`, 실제 producer 두 번 + 실제 게이트 → `controls 0` 관측) →
`w_dqdv` 를 control 로 추가 → GREEN. **fixture 가 여덟 번째로 깨졌다** (`test_cy_01` 이 5 개
튜플을 박아 두고 있었다 → 개수가 아니라 키의 존재를 묻도록). `--gamma-lb` 는 기본 `null` 이라
같은 목록에 넣지 않았다 (`None` 은 schema-only 에서 부재로 세어진다).

**§13-5 의 열린 둘도 닫았다 (§15).** ① `mode_profile_extrema` 를 cycles 경로에 붙였다 —
`--width-grid N` (기본 0 = 꺼짐), 켜면 제약 극값과 **합집합**이고 `width_method`·`width_grid` 가
sidecar 에 실려 `width_report` 가 방법이 다른 폭의 비교를 거부한다. **그런데 이득이 0 이었다**:
굽은 골짜기 둘(제약 40.000/14.044 vs 프로파일 39.393/7.558 — 합집합이 제약과 같다)과 합성
파이프라인 전체(3 사이클 × 3 mode = **9 칸 전부 동일**, 합계 +0.0000 %p, 벽시계 37.3→61.3 s
**+64 %**). 비용은 확실하고 이득은 자료에 달렸으므로 **기본은 끈 채로 둔다** — §14 의 실데이터
폭은 기본값으로 잰 것이라 그대로 유효하다. 회귀 W-19·W-20·W-21 (W-20 은 처음부터 통과해
**변이로 가짜 통과가 아님을 확인**했다). ② γ 사전 적합: 원인을 가르는 관측은 적합값이 아니라
**60 점 스캔의 모양**이다. 합성으로 손상별 서명을 먼저 쟀더니 — 방향 뒤집힘은 RMSE 가 **자릿수로**
튀고(5.04·4.30), 역할 교환·좁은 측정 구간은 **상**한 0.5 에 붙는다. **실데이터 서명(하한 0.02 ·
RMSE 0.4739)을 내는 것이 하나도 없다** → 세 의심 중 **방향 규약은 배제**된다. 남는 둘(반쪽전지
선택·재정규화 구간)은 `scripts/gamma_prefit_report.py` 로 사용자 기계에서 가른다 (읽기만 하고
게시하지 않는다; `MONOTONE_AT_LB`/`INTERIOR`/`FLAT`/`MONOTONE_AT_UB` 로 이름을 부른다).
이 항목은 **LAM 결론을 바꾸지 않는다** — §12-5 실측대로 5 파라미터 적합은 초기값과 무관하게
같은 곳에 앉는다.

**γ 진단 1 회 실행 (§15-4, 사용자 기계).** 규진팀 native 쌍에서 **하한에 안 붙는다** —
γ 0.276053 · RMSE 0.495774 · 스캔 최소 γ 0.280339 · 판정 **INTERIOR** (0.02 에서 0.6029 로 시작해
0.28 에서 0.4959 로 내려갔다 올라가는 분명한 그릇) · 공통 전압 구간 [0.0400, 0.6834] V.
**§13-5 의 반박이 아니라 대조군이다** — §13-5 의 γ 0.02 는 **pyDMA 예제 쌍**(`--si-source external
--literature`) 맥락이고 이번 건 native 쌍이다. 대조군이 말해 주는 것은 "구현이 항상 끝으로 붙는
것은 아니다" 이고, 합성에서 배제한 방향 규약과 합쳐 **남는 것은 그 pyDMA 입력 쌍 고유의 무엇**이다.
다음 관측 한 번(같은 스크립트를 pyDMA 반쪽전지·문헌으로)이 가른다. 겸사로 **γ 가 native 쌍에서도
약하게만 식별된다**는 것이 보였다 (γ 가 0.05 넘게 움직여도 RMSE 1 % 남짓) → 진단이 **식별 띠**
(`RMSE ≤ 최소·(1+tol)` 인 γ 범위, 기본 tol 0.01 = `--width-tol` 과 같은 자)를 같이 찍게 했다.
이 띠도 격자 위라 **하한**이다. §12-5 와 같은 결 — 점추정 하나를 자료가 정한 값처럼 쓰지 않는다.

**pyDMA 쌍 재현 (§15-6) — γ 항목을 닫는다.** RMSE **0.473923** 이 §13-5 기록과 **자릿수까지** 같게
나왔다 (판정 `MONOTONE_AT_LB` · 띠 폭 0.0000 · 사본 둘은 같은 바이트). 가설 셋을 실측으로 배제했다 —
방향 규약(합성, RMSE 가 5 자리로 튄다) · "늘 끝에 붙는다"(native 쌍이 안쪽 최소) · **측정 전압 범위가
문헌보다 넓다**(합성 측정 상한 0.90→2.00 V, γ 0.2256→0.2255 로 **안 움직인다** — 이 절에서 새로 세우고
새로 무너뜨린 가설). **진짜 답**: 최소 RMSE 가 합성 대조군 0.00065 · native 0.4959 · pyDMA 0.4739 로
**세 자릿수** 차이다. "하한에 붙는다" 는 하한의 문제가 아니라 **어느 γ 에서도 안 맞는다는 것의 증상**
이고, 안 보였던 이유는 RMSE 의 크기를 잴 자가 없었기 때문이다. 진단에 자를 더했다 — 측정 dV/dQ
**자신의 RMS**(= 아무것도 예측하지 않는 모델의 RMSE)로 나눈 **맞춤 정도**, 1 에 가까우면 그 γ 는 잘
맞는 값이 아니라 덜 나쁜 값이다. 회귀 `test_cy_12` 가 양쪽에서 건다 (정답 자료 < 0.05 · 뒤집힌 문헌
> 0.5). **닫힘**: γ 가 하한에 붙는 것은 버그가 **아니다**. **남음**(우선순위 낮음): 왜 설명하지 못하는가
(반쪽전지-문헌 물질계 짝 · dV/dQ 평활 인자). **안 바뀜**: §12-5 대로 5 파라미터 적합은 초기값과 무관하고
LAM 결론을 안 바꾼다 — 같은 자료에서 5 파라미터는 γ 0.2407·0.2396 (pyDMA blend 0.224) 을 냈고, 사전
적합 0.02 와 **모순이 아니다** (다른 목적함수이고 잘 맞는 쪽은 5 파라미터다).

**정정 (§14-8): 전 사이클 실행이 남은 게 아니라 §14 가 이미 전수였다.** 이 워크북이 담은 사이클은
`discover_cycles` 기준 **`[0, 1, 2]` 셋뿐**이라 `--cycles 0,1,2` 가 워크북 전체와 같다. 합성 워크북으로
양쪽을 돌려 실측했다 — 비교 대상 설정 21 개 **전부 동일** · `meta["cycles"]` 동일 · `run_id` 를 뺀 본문
digest `c5bf28c49e56d272` 로 **동일**. 다만 **"전 사이클" 이 "300 사이클 전부" 라는 뜻은 아니다** —
셀은 300 사이클을 돌았지만 워크북에 실린 것은 체크포인트 셋이고, §14 의 판정은 그 셋 한정이다.

**남은 것**: 이 갈래에서 사용자 기계가 할 일은 **없다**. (우선순위 낮은 잔여: §15-6 의 "왜 사전 적합이
실데이터를 설명하지 못하는가" — 반쪽전지-문헌 물질계 짝 · dV/dQ 평활 인자.)

**런북 (2026-09-15, `docs/WIDTH_RUN.md`).**
원자료는 여전히 사용자 기계에 있지만 **배관은 여기서 끝에서 끝까지 돌렸다** — 합성 원자료
(`matlab/tests/gen_synth_xlsx.py`) 3 사이클로 `fit_cycles --widths` 두 번(`--w-dqdv` 0/1,
rc 0 · 37.2 s / 104.8 s) → `width_report --axis w_dqdv` rc 0 → `check_rails` rc 0(error 0) →
`check_u14 --schema-only` rc 0, meta 의 비교 대상 설정 20 개 전부 기록. **가드 셋도 실제로
물었다** — 같은 축(rc 2) · 엉뚱한 `--axis`(rc 2) · **축 말고 `seed` 도 다른 짝**(rc 2,
`seed: 0 ↔ 1` 을 지목). 회귀는 이미 `tests/test_widths.py` W-16·W-17·W-18 이다.
**이 숫자는 합성이라 인용 불가다** — 확인한 것은 배관뿐이고, 정본은 사용자 기계에 생길
`cycles_HD_knee_Li.csv` + `.meta.json` 이다. 세트는 HD_knee, 두 실행은 `--w-dqdv` **한
줄만** 다르고 `--seed 0 --scale-seed 0 --starts 20 --width-tol 0.01 --width-starts 4` 는
양쪽 같다. 먼저 `--cycles 0,1,2` 파일럿으로 벽시계를 재고 본 실행을 정한다 (`cycles` 도
비교 대상 설정이라 **양쪽에 똑같이** 줘야 한다). 산출은 커밋하지 않는다 — 돌아오는 것은
`width_report` 출력 전문 · 두 meta 의 `run_id`/`inputs_sha`/`env`/`git` · RAILS·PROMOTION
줄 · 벽시계 넷이고, 그것이 오면 `BML_R1_RESPONSE.md` §14 로 적는다.

---

## 직전 상태 — **자체 적대적 리뷰 35 건 닫음 (Codex 토큰 소진 → 내부 6 렌즈) · 현행 정본은 provenance-incomplete**

2026-09-13 Codex 를 더 못 쓰게 되어 `/self-review` 로 6 렌즈를 병렬로 돌렸다 (sig-완전성 · validator-우회 ·
순서-TOCTOU · 파생-보고서 · archive-이식성 · 공정성-의미). 원시 45 건 → 중복 합쳐 **35 건**, `결론이_바뀜` 14 건.
**같은 축을 여러 렌즈가 독립으로 친 것이 셋**이다 (C01·C04·C11 각 3회).

요지는 하나다 — **직전 라운드(R11)가 "닫았다" 고 적은 것의 절반이 반쪽이었다.** 입력 identity 비교는 파일당 한 벌만
만들어 마지막 행만 봤고(C01), alias 는 inode 만 봐서 `cp` 사본이 통과했고(C02), "신고된 위험을 값으로 소비" 는 실은
"키가 있을 때만" 이었고(C03), 정본 격자 검사는 본문과 한 번도 안 댔고(C04), matrix 의 모집단은 stdout 에만
있었고(C05), 유한성은 JSON 문자열을 통과시켰고(C06), 도구 봉인은 checkout filter 를 안 막았고(C07), import 격리는
bytecode 만 막았고(C08·C09), `rc 0` 인데 승격 불가인 상태를 런북이 "0 이면 교체" 로 읽었다(C11).

35 건 전부 RED(`tests/test_r12_selfreview.py` f01~f28) → 수정 → GREEN. 원장은 `reviews/R6_LEDGER.md` "자체 적대적
리뷰" 절. **fixture 는 일곱 번째로 깨졌다** — 정본과 재실행 fixture 가 같은 `run_id` 를 쓰고 있었고, C02 를 닫기
전에는 그것이 아무 의미도 없었으므로 아무도 안 봤다.

**새 규약(자체 리뷰에서 더한 것)**: 입력 identity 는 **행 key 별로** 댄다 · 독립 baseline 은 run id 가 달라야 한다 ·
부재는 안전값이 아니다 · roster 는 본문에 묶인다 (`combo_roster` 가 matrix 행에도) · 과학 값은 문자열이어도 유한해야
한다 · 도구 봉인과 snapshot 검증은 **같은 플래그**(`--no-filters`) · 러너는 `-P -E` 로 재실행해 봉인을 import 앞에
둔다 · production heredoc 은 `-I -P` · 줄끝은 catch-all 로 고정 · 승격 불가는 rc **4** (단 `--schema-only` 는 승격을
묻지 않은 진단이라 0) · 명부는 배제목록 · 러너 rc 는 `evidence_eligible` 을 반영한다.

**정본 범위 (변화 없음)**: `check_u14 --new out --schema-only` rc 2 · `promotion_eligible: false`. 새 검사가 늘면서
수치가 커졌다 — 스키마 누락 59 (sidecar `argv`·`roster` 26 + `gamma_roster` 4 + `combo_roster` 등) · 출처 열 27 ·
내용 5 · provenance 1. **숫자는 하나도 안 움직였다**; 늘어난 것은 요구하는 축이다. U18 재실행이 새 규칙으로 서명한다.

### 리뷰 3 건 결과 — **전부 NO-GO** (2026-09-13)

셋을 독립 트랙으로 본다. 서로의 판정을 이어 붙이지 않는다.

| 트랙 | 판정 | 지금 상태 |
|---|---|---|
| ① mph 마이크로 쇼츠 | NO-GO ×2 (v1·v2) → **6.3 재구축 제한 검증 '뒷받침됨'** (Codex 독립 검토 2026-09-13, 원문 `reviews/r14_repros/codex63/`) | **문서 v3: M1 철회** (`cEeqref_mat = from_mat` — 값 칸의 사용자 식은 선택되지 않았다; `MPH_R1_RESPONSE.md` §6). 재구축은 §0-a 대로 — §5 검산값 `x_NCM 0.924064`·`x_Gr 0.0117207` 이 독립 산술로 재현됐고 초기 OCV 2.1653 V 는 MCMB 표 가파른 구간(오류 아님). **전체 프로토콜은 보류**: 4.25 V CV 가 양극 OCP 표 하한(x=0.2229 → 평형 4.1856 V)과 충돌 → OCP 범위 중단조건·phase 별 cutoff·시간간격·mesh 비교 (`docs/COMSOL_REBUILD_SPEC.md` §8). **현지 사전 진단 (§9, 2026-09-13 밤)**: 초기 Eeq 3.578387/1.413053 V (차 2.165333 V, 보정 안 함) · 표 내부 평형 OCV 상한 4.185562 V · 표면 조성 표 이탈을 실제 감지해 `INCOMPLETE_RANGE_STOP` 으로 보존 · 2.7 V cutoff 가 첫 충전 안 막음 · 축소 조건 CC→CV→휴지→방전 전이 확인(eventtol 1e-6, 2 s → 2.000002 s). **미완**: 메시 수렴(150/20→300/40 최대 2.041557 mV > 1 mV) · 저전류 CV 완료 · 전해질 양수 검사는 후처리뿐 · 원본/실험 OCP·물성 출처 대조 · 전체 프로토콜·유한 누설·sweep. **전체 운전 보류 유지 — GO 아님**. 원문 `PREFLIGHT_RESULTS_KO.md`·`NEXT_RUN_PLAN.md` 는 `reviews/r14_repros/codex63/preflight/` 에 보존 (둘 다 원문 — 후자는 sha 일치, 전자는 원본이 CRLF 라 LF 정규화 사본이고 CRLF 로 되돌리면 manifest sha 와 일치). **메시 축별 진단 (§10, 원문 대조 완료 2026-09-14)**: 반경축 300/40→300/80 최대 2.505 mV @0.04 s (1 mV 초과, 거의 전부 Eeq 항) · 물리축 300/40→600/40 1.1e-11 V (충족) · 두 실행의 내부 step 이 달라(0.005/0.002 s) 시간 효과와 미분리 → 다음은 제안 A(300/40·300/80 × 초기 최대 step 0.001·0.0005 s, 4 회; 600/80 보류). 보존 증거 미결 1 (이전 ZIP 포장본 식별 불일치 46,999,470 B/`3bc4e4e4…` vs 47,006,147 B/`097d4b65…`, 내부 330 개 명세는 일치 — 변조 단정도 전수 검증 완료도 아님). **전체 메시 수렴 미완 · 본 실행 보류**. 2026-09-14: 원문 묶음을 `reviews/r14_repros/codex63/mesh_axes/` 로 받음(사용자 커밋 `2fa058a`; ZIP sha `96321b94…` 일치 · 명세 139 항목 중 90 보존 sha 일치 · 49 제외 크기 일치) — 최대값·분해·시간표·native step 을 원시 CSV 에서 다시 계산해 같음 확인, §10 확정 (10-1~10-7). **초기 시간상한 비교 (§11, 원문 대조·재계산 완료)**: 시간상한 0.001→0.0005 s 반감의 차는 300/40 0.000193 mV · 300/80 0.001422 mV 로 **충족**인데 같은 상한에서 반경 40→80 은 2.5067 / 2.5060 mV 로 **초과 그대로** (둘 다 0.04 s) → §10-3 의 '시간 step 과 미분리' 가 대부분 풀렸고 반경축이 원인이라는 근거가 강해졌다. 초기 accepted step 111→209 로 실제로 걸렸고 0.0005 s 에서는 두 격자의 초기 accepted 시각이 같아도 차이가 남았다. **반경 300/160 (§12, 원문 대조·재계산 완료)**: 80→160 최대 전압 차 **1.248218114 mV @0.01 s** 로 **기준 초과** (표면 x 차 2.09e-5 는 이내). 0.04 s 만 보면 0.690 mV 지만 **최대 시각이 0.04→0.01 s 로 이동**했다 — 한 시각·끝점으로 통과 금지. 독립 검산은 187 시각 + 보조로 실제 저장 379 시각(보간 없음) 둘 다 같은 결론. 실제 메시 300/160/160 · 자유도 40765(+12) · 저장 388/accepted 387. 160 의 시간상한 반감은 **미실행** — 80 의 시간 민감도를 160 으로 이전하지 않는다. 다음 권고는 320 확대 전에 **300/160 @0.00025 s 1 회**. 수신본 식별은 이번엔 생성본과 **일치**(앞 두 건의 불일치 패턴 없음), payload 160+manifest 외부 검증 통과. **우리 정정**: 직전 판이 적은 '40→80 2.506 → 80→160 1.248 = 대략 절반' 은 **서로 다른 시각의 최대값**이라 수열이 아니다 — 같은 시각 비는 0.82(0.01 s)·0.275(0.04 s)로 전혀 다르다 (§12-3). 수렴 차수·320 통과 여부를 외삽하지 않는다. 보존 대조: time_caps 명세 201 중 136 보존 sha 전부 일치 · radial160 payload 160 중 112 일치, 불일치 0. §10-5 정정 — MESH_AXES 전달본만으로 재검증 가능했던 것은 333 중 **7** 개뿐이었다 (§11-3). 정정 1 — `radial160/comparison_contract.json` 의 `baseline_source_sha256` 가 옛 `dbcb95…` 로 남아 있다 (실제 baseline `Caps300R80H0500` 은 `6ab32b93…`); **식별 정보 불일치이지 계산 무효가 아니고**, 원본 ZIP 을 보존한 채 정정한다. 포장본 식별 미결 하나 더 — 생성 영수증 325,347,218 B/`beac1f1d…` vs 수신 325,367,172 B/`74aa78d2…`, 내부 201 payload·manifest 는 검증됐다 하므로 **내용 손상 단정 금지**, 생성본·수신본 영수증을 구분한다. 보존은 과거 333 개 바이트 재검증이지 **현지 468 개 전수 원격 검증이 아니다**. **160 요소 시간상한 반감 (§13, 원문 대조·재계산 완료)**: 160H0500→160H0250 최대 전압 차 **0.002175461073 mV @0.005 s** · 표면 x 차 4.3003216e-8 — **충족**. §12-4 가 요구한 시험이다. 전달본은 기존 `R160_TIMECAP` 과 **같은 식별**이라 **재확인이지 중복 계산이 아니고 새 320 결과도 아니다**. 수신 측 확인값(307,305,998 B · `481ce9eb…` · payload 267+manifest 1 · CRC·명부·역사적 333 확인)은 원본 영수증을 고치지 않고 **별도 기록**으로 덧붙였다 (원본의 수신 확인 필드 null 은 당시 기록). 현지 현재 파일 전수 외부 검증으로 확대하지 않는다. 재계산은 `requested_grid`(187/107 행)와 `all_exact_common_stored`(363/282 행) **둘 다** 같은 최대를 냈다. 명세 267 중 보존 186 개 sha 전부 일치. **부수 산물**: 전달본의 `corrections/` 가 §12-5 의 baseline 식별자 정정을 닫았다 — before `dbcb95c…` → 현행 `6ab32b93…` (우리가 지목한 값과 일치), before bytes 백업 보존·archive manifest 불변·회귀 24 PASS, 그리고 수치 분석 앞에서 불일치 메타데이터를 거부하는 가드가 추가됐다. **반경 300/320 (§14, ZIP `89703ec4…` 미첨부·전달 요약 기준)**: 160→320 최대 전압 차 **0.6170341087208 mV @0.002 s** · 표면 x 차 1.0361978499567e-5 — **이번 표본에서 충족** (지정 107/187 과 정확 공통 저장 490/571 둘 다 같은 최대). 메시 300/320/320 · 자유도 79485(+12) · 저장 593/accepted 592. **그러나 과거 80→160 의 초과 기록(1.248218114 mV)을 지우지 않고 전체 반경·시간 수렴 완료로도 바꾸지 않는다 — 320 자체의 시간반감은 미실행**이다. 다음 후보는 300/320 고정 + 초기 cap 0.00025→0.000125 s 1 회(결과 없음). 이전 TIME_CAPS raw ZIP 차이 원인은 계속 미확인. **320 의 초기 시간상한 반감 (§15, 원문 대조·재계산 완료 2026-09-14)**: 그 다음 후보가 도착했다 — 320H0250→320H0125 최대 전압 차 **0.0012699200233 mV @0.002 s** · 표면 x 차 -2.1349484521e-8 (음극 z=52 µm) — **이번 표본에서 충족**. 네 비교 파일(지정 107/187 · 정확 공통 저장 484/565) 전부 같은 최대이고 원시 CSV 에서 재계산해 확인했다. accepted 592→986(저장 593→987) · Time/Variables 1143 속성 중 승인된 상한식 하나만 다름 · ZIP `e38968f1…` · manifest `964b6817…` · 보존 114/160 sha 전부 일치. 반경 차 대비 **0.205810344250%** 는 **크기 비교이고 수렴 차수가 아니다**. **판정은 이번 표본의 초기 시간상한 반감 민감도에 한정** — 0.1 s 이후 시간 정확도·참값 오차·전체 수렴·장시간 GO 로 확대하지 않고, 80→160 초과 기록도 그대로. 전해질 양수는 후처리 검사이고 장기 보호 구현 완료가 아니며, 현지 967 개 전수 외부 검증도 아니다. 다음은 **계획만** — 후반 시간 민감도 · 고정밀 입자 메시와 물리축 교차 비교 (추가 계산 미승인). **H0125 이후 계획 검토 (§16, 2026-09-14 — 계획이고 새 계산 결과가 아니다)**: 그 두 축이 A·B 로 구체화됐다. **A** = `if(t<0.1[s],0.000125[s],if(t<1[s],0.005[s],0.025[s]))` (물리 300·입자 320/320 고정, 후기 시간상한만 강화, 5 초 1 회) · **B** = 같은 H0125 기준과 **원래 시간식**으로 물리 300→600 비교 (A 의 시간식을 섞지 않고 A 결과로 기준을 자동 교체하지 않는다). 권장 순서는 A 1 회 → 결과 검토 → B 별도 승인. 후기 간격 분포(0.1–1 s 98 개 최대 0.01 s · 1–5 s 81 개 최대 0.05 s, 합 179)를 보존 CSV 에서 재계산해 확인했고, 전달값 **제한 대상 87·80** 도 맞다 — 다만 **1e-12 s 반올림 허용으로 셀 때**만 87 이고 엄격히 `>` 면 88 이다 (간격 하나가 0.005 s 를 1e-17 s 넘는 부동소수 표현). **단계 구분**: 승인 문안 작성 = 완료 · 승인 전달/작업 제출/계산 완료 = **미확인**. 새 실행 결과 전에는 A·B 를 완료·충족으로 적지 않는다. 수신 확인은 생성 당시 영수증과 **분리** 보존이고 범위는 **직접 포함 56 개**(현지 967 전체 아님), 역사적 333 개 검증을 현재 파일 수에 **합산하지 않는다**. A 가 통과해도 **표본의 후기 시간상한 민감도 한정** — 두 후기 구간의 인과 분리나 참값 오차 증명으로 확대 금지. 이번 갱신에서 COMSOL 실행 없음. **후기 cap A 실행 (§17, 2026-09-14 — 원문 대조·재계산 완료)**: A 가 돌았는데 **코어가 2→16 으로 같이 바뀌었다**. 그래서 판정 문구를 좁힌다 — **"후기 시간상한·코어 수 변경을 포함한 두 실행의 지정 표본 차이가 기준 이내"** 이고 **동일 코어의 시간상한 단독 검증 종결이 아니다**. 여덟 비교 전부 기준 이내 (0.1–1 s·0–1 s max ΔV 0.0020165373344 mV @0.22 s · 1–5 s·0–5 s 0.0023442301413 mV @1.7 s · 표면 Δx 3.37e−8·3.87e−8, 전부 음극 z=52 µm). accepted 986→1154 · 후기 최대 간격 0.01→0.005 s, 0.05→0.025 s · 초기 807 간격 동일 · Time/Variables 1143 중 상한식 하나만 다름. **초기 차이가 5.8e−12 mV 로 작다는 것이 이후 코어 영향의 상한이 아니다.** 벽시계 예산 1200→1800 s 는 물리시간과 구분하고 solver 시간 감소를 성능 향상으로 읽지 않는다. 보존은 **현지 1,099 중 직접 포함 57 개**만 (56 불변 + 계획서 변경 전 사본 1 일치), 나머지 1,042 미검증이고 역사적 333 은 **합산 금지**. 이전 R320_TIMECAP manifest `964b6817…` 동일 확인. **다음 권고**: 원래 H0125 모델·원래 시간식을 **16 코어**로 돌린 통제 해 1 회 (승인 문안 작성=완료 · 전달/제출/완료=미확인), B 는 그 뒤 별도 승인. **2026-09-14 후속: 원문 대조·재계산 완료로 승격.** 사용자가 `scripts/preserve_handoff.sh` 로 보존했고 (ZIP `63bdb39c…` 780,744,308 B · manifest `d7c19bb0…` · payload **201/201 sha 일치** · 보존 140 · **커밋 안 bytes 140/140 일치**), 여덟 비교·성분 분해·간격 수를 전부 원시 CSV 에서 재계산해 같았다 (초기 0–0.1 s 808 시각 max 5.773e−12 mV @0.00425 s 도 확인). 묶음의 `authorization_scope.json` 이 **"병렬 부동소수 축약이 2 코어 기준과 다를 수 있다"** 를 스스로 신고했고 — 판정을 좁힌 근거가 이것이다. 20 코어 요청은 job 생성 **전에** 거부됐다(1..16). ⚠ 묶음에 manifest 가 **둘**(이번 `d7c19bb0…` · 이전 R320_TIMECAP `964b6817…`)이라 대조 때 이번 것을 명시해야 한다. ⚠ 묶음 자신의 판정문(`LATE_CAP_A_RESULTS_KO.md` 첫 줄)은 코어 변경을 문구에 안 담았다 — **우리는 좁힌 쪽을 채택**하고 원문은 안 고친다. **16 코어 통제 해 (§18, 2026-09-15 — 원문 대조·재계산 완료, 본진에서)**: §17-6 의 권고대로 원래 H0125 모델·원래 시간식을 16 코어로 돌린 통제 해 1 회가 도착했고(`Caps300R320H0125C16` / job `5d1a8765…`, 소스 `4db47e27…`), 이제 §17 이 하나로 묶여 있던 두 축을 **따로** 쟀다 — **① 코어 축 단독**(old2→control16) 최대 |δV| **4.0e−12 mV**(지정)·**4.8e−12 mV**(공통 0–1·0–5 s @0.044625 s), 표면 2.0e−15·2.4e−15(양극) → 충족 · **② cap 축 단독**(control16→A16, 16 코어 고정) **0.0020165373344 mV @0.22 s · 0.0023442301413 mV @1.7 s**, 표면 3.369e−8·3.870e−8(음극 z=52 µm) → 충족. ② 의 값이 §17-2 의 결합 최대값과 **표시 자리까지 같다** — 결합 차이의 사실상 전부가 cap 축이고 코어 축은 1e−12 mV 급. §17 의 A16−old2 는 **결합 표본 차이**로 정정된 채 보존(묶음의 `A_ASSESSMENT_CORRECTION.json`, 숫자 불변). 16 개 비교 전부 원시 CSV 재계산으로 원문 표와 일치(`scripts/recheck_core16_control.py` → `RECHECK_2026-09-15.json`) · 세 해 전압 항등식 986 시각 잔차 0(원시) · 표면 항등식 475,252 위치 잔차 0(**전달 파일** 검산) · old2 와 control16 의 accepted 986 간격이 **시작·끝 시각까지 동일** → 코어 비교는 같은 시간 격자 위이고 4e−15 V 는 병렬 부동소수 축약 차이의 이 한 쌍 크기(재현성 시험 아님). 소스 diff(이름 두 곳)는 java 미보존이라 **전달값**. 보존 162/162 sha 일치, 현지 1,247 중 직접 93 만 확인, **ZIP 크기는 기록에 없음**. 세 해만으로 core×cap 상호작용 부재를 주장하지 않는다. **물리축 B 300→600 (§19, 2026-09-15 — 수신 측 검토 접수, 원문 보존 전 · 전달값)**: control16 기준 물리 메시만 600(240/120/240) 으로 늘린 16 코어 해 `Caps600R320H0125C16` / job `56975e4d…` 가 돌았고 수신 측(Codex)이 ZIP(1,078,568,990 B · `53b4b2bd…` · payload 163 + manifest 1 · CRC 일치)을 검증해 원시 CSV 를 독립 재계산했다 — 여덟 창 전부 충족: 최대 |δV| **1.07714e−8 mV @0.00125 s**(공통 0–1·0–5 s) · 1.06511e−8 mV @0.001 s(지정) · 표면 5.23e−9(양극 121 µm @5 s). 자유도 79,485 → 158,325, 속성 1,143 동일, 저장 987/accepted 986 이력 §18 과 동일, cap 식 그대로. **작은 차이에 Eeq·과전압 상쇄가 들어 있어** 성분 오차 상한으로 읽지 않는다. 판정 문구는 "이번 표본의 물리축 300→600 민감도 기준 충족" 한정. **ZIP 은 아직 저장소에 없다** — `scripts/preserve_handoff.sh … physical600_b` (규칙은 `.gitattributes` 에 넣어 둠) 로 보존한 뒤 우리 재계산으로 §19-2 를 실측으로 바꾼다. 추가 계산 승인 0. **전체 메시 수렴 미완 · 본 실행 보류** |
| ② R13 하네스 | NO-GO (P1 4 · P2 5) | **P1-1~P2-5 · §5 Q6 전부 닫음** (262 passed). **U18 본 실행 끝남** (사용자 기계 2026-09-13 20:02–22:39, 13/13, STARTS=24, 소스 100·200·300_0009=GITT · 300_0147=step_005C). **숫자는 하나도 안 움직였다** (`numbers 0`, 명부 13/13). 드러난 발견 셋 — **U18-01** shape 가 `ne_shape_step_005C_Li.csv` 로 게시됨 (wrapper 의 `${SRC:-GITT}` 가 마지막 상태의 loop 변수를 샜다; 회귀 `test_g27`, 고침, 사용자가 GITT 로 재생성해 닫음) · **U18-02** 13 중 11 이 `git_state_changed_during_run: true` — 시작 provenance 가 `$OUT` 을 몰라 `out_u18/` 을 '코드 변경' 으로 셌다 (`test_g28`, 고침) · **U18-03** 옛 정본에 `env` 가 없는 것을 계약 위반(rc 2)으로 등급했다 — 정본의 나이는 새 산출의 위반이 아니다 (`env_uncomparable` 버킷 신설, `test_g29`, 고침). 1 차 산출은 승격하지 않았다 (고침은 다음 실행의 서명을 고칠 뿐이고 이미 적힌 sidecar 의 true 는 그대로다; `matrix_100` 은 실행 중 실제로 커밋이 바뀌었다 d07a77a→c9dd822). **U18b 재실행 → 승격 완료 (`37a889b`)**: `check_u14 --new out_u18b --old out` rc 4 · `numbers 0` · 명부 13/13/13 · 계약 축 전부 0 · 남은 것은 옛 정본의 나이인 `inputs_uncomparable 17` · `env_uncomparable 1` 뿐. 승격 뒤 `--schema-only` 는 사용자 기계와 이 컨테이너(fresh clone) **둘 다 rc 0** — 서명이 git 왕복을 견딘다(U14-01 축). 옛 정본은 `out/archive/legacy_r6_u14/` 에 얼렸다 (조건 7 의 보존). U18b 도중 `~/dd` 에서 git 을 돌려 `matrix_300_0147` 하나가 또 오염됐고 그 상태만 다시 돌려 닫았다 (13/13 clean). 승격이 드러낸 것: 살아 있는 정본 경로를 **표본으로 쓰던 테스트 셋**이 깨졌다 (아래 U18-04) |
| ③ BML α·β 난간 | NO-GO (B1~B5 전부 미증명/반박) | **주장 사슬 전부 철회** → 원인은 `rng(0)` 오염(§9) → **우리가 다시 뽑는다** (전권, `BML_R1_RESPONSE.md` §10): (a) `matlab/fit_cycles_driver.m` · (b) `scripts/fit_cycles.py` · 난간 `scripts/check_rails.py` (받은 xlsx 4 개에서 §6 재현). **닫힘 (§11)**: 같은 입력(HD_knee)에서 규진팀 표만 반복 패턴, 그들 파이프라인 rng 없이(a)·우리 포팅(b) 둘 다 경고 0 이고 서로 ~1e-3 (= scale 표본 크기) 안에서 일치 · 시작점 의존 1e-7. 원인 = `rng(0)` 오염 확정. 받은 L_* 표 4 개는 근거로 쓰지 않는다. **pyDMA 검증 (§12, 2026-09-14)**: 규진팀 폴더의 `validation_pydma_example/` 이 공개 도구 pyDMA 의 검증된 결과와 대조하는 예제였다 — **정답 있는 데이터**다. 외부 문헌 경로(`--si-source external --literature`)를 새로 만들어 우리 포팅을 걸었다. 결과: **LLI 는 세 구현이 0.18·0.09 %p 안에서 일치**하고, **LAM 두 축은 1.0~1.5 %p 로 흩어지며 CU2 음극은 부호까지 갈린다** — 우리만 다른 게 아니라 **pyDMA 자신의 두 방법도** 같은 축에서 부호가 갈린다. 축퇴 행렬의 'LLI 가 가장 좁다' 와 **같은 결론에 외부 데이터로 독립 도달**. **결정 실험 종료 (§12-5~12-8, 2026-09-14 사용자 기계)**: `fit_gamma_si` 를 포팅해 `--gamma-prefit --gamma-lb 0.02` 로 Track C 설정을 맞춰 재실행했다. **γ 초기값을 0.25→0.02 로, 하한을 0→0.02 로 바꿨는데 CU2 의 네 값이 표시 자리까지 전부 같다** (LLI 3.00 · LAM_ca 1.98 · LAM_an −1.26 · γ 0.2407). pyDMA blend 는 3.18 · 1.55 · +0.27 · 0.2240 — **차이는 설정이 아니라 식별 가능성**이다. §12-4 의 두 갈래 중 후자로 확정: 이 데이터에서 **LAM 분할은 점추정으로 보고할 수 없고 폭과 함께 보고해야 한다**. LLI 결론은 안 흔들린다. **§13 (2026-09-14): 결론을 도구에 반영했다** — `fit_cycles --widths` 가 사이클마다 근최적 집합 폭을 **점추정과 같은 행에** 낸다 (`width_status`·`width_tol`·`width_is_lower_bound`·`LAM_*_lo/hi`·`LLI_lo/hi` 아홉 열, `LLI` 바로 뒤). 별도 파일이면 표로 옮길 때 또 떨어지므로 같은 행에 뒀다. 계약은 **tagged union** — `measured` 면 여덟 칸이 전부 차 있고 `not_requested`·`failed` 면 전부 비어야 한다 (**안 잰 것과 0 은 다르다**; 0 은 '완벽히 식별됐다' 로 읽힌다). 폭은 `verify.near_optimal_extrema` 재사용이고 **하한**이다 — 행이 스스로 그렇게 말한다. 문헌 곡선 선택이 만드는 더 큰 폭은 여기 **안 들어간다** (두 축을 합치지 않는다). **새 열린 항목(우선순위 낮음)**: 우리 γ 사전 적합이 0.224 가 아니라 **하한 0.02 에 붙는다**(RMSE 0.473923) — 문헌 곡선 방향 규약·반쪽전지 선택·재정규화 구간을 의심하나 **미확인**. 5 파라미터 적합이 초기값과 무관하게 같은 곳에 앉으므로 이 항목이 LAM 결론을 바꾸지는 않는다. **→ §14·§15 (2026-09-15) 에서 이 갈래를 닫았다.** §14 **실데이터 폭 측정**: `--w-dqdv` 만 바꾼 두 실행(`width_report` rc 0 = 축 하나만 달랐음을 기계가 확인)에서 **dQ/dV 항은 폭을 안 좁힌다** — LAM_PE 3.137→3.388 · **LAM_NE 2.439→7.099 (2.91배)** · LLI 1.172→1.402 %p, 그리고 `w_dqdv 1` 의 cycle 1 에서 **LAM_NE 가 [−0.60, +6.50] %p 로 0 을 가로질러 부호 식별을 잃는다** (난간도 `a_NE` 하한 접촉으로 같은 자리를 독립으로 짚었다). LLI 가 두 설정 모두에서 가장 좁아 **세 번째 경로**로 같은 결론. **§14-8: 이것이 전수다** — 워크북의 사이클이 `[0,1,2]` 셋뿐이라 파일럿이 곧 전체였다 (설정 21/21·본문 digest 동일 실측). §15-1·15-2 `mode_profile_extrema` 를 `--width-grid N` 으로 붙였으나 **합집합 이득 0**·벽시계 +64 % 라 기본 꺼짐. **§15-3~15-6 γ 항목 닫음**: pyDMA 쌍에서 RMSE **0.473923** 을 자릿수까지 재현했고, 가설 셋(방향 규약·'늘 끝에 붙는다'·측정 전압 범위)을 전부 실측으로 배제했다. 진짜 원인은 **RMSE 의 크기** — 합성 대조군 0.00065 vs 실데이터 0.4739·0.4959 로 **세 자릿수** 차이이고, '하한에 붙는다' 는 하한의 문제가 아니라 **어느 γ 에서도 안 맞는다는 것의 증상**이다. 진단 `scripts/gamma_prefit_report.py` 가 스캔 모양·식별 띠·맞춤 정도를 찍는다. **남는 잔여(우선순위 낮음)**: 왜 설명하지 못하는가 (반쪽전지-문헌 물질계 짝 · dV/dQ 평활 인자). LAM 결론은 그대로다 |

**세 라운드 공통 교훈**: 정정이 또 다른 단정이 됐다. "세 모드 붕괴" 를 고치며 "LLI 는 독립"
이라 했는데 `c_lit = C_cell·(a_PE+b_PE−b_NE)` 항등식이 그것도 무너뜨렸다. 관측과 해석의
경계를 매 라운드 다시 그어야 한다.

**①·③ 이 요구하는 외부 자료** — 이것 없이는 더 못 닫는다:
- ~~COMSOL: `liion.pce*.pin1.cEeqref` 실효값~~ → 불필요해짐 (XML 선택자 `from_mat` 이 답, 문서 v3). 남는 외부 자료는 **없다** — ① 은 재구축 모델의 §8-5 순서, ③ 은 닫힘
- ~~MATLAB: 자유/고정 변수 · lb/ub · …~~ → 원본 확보로 닫힘 (§8). 이제 필요한 것은 **네 셀(ref1·ref2·PE1·PE5)의 원시
  사이클 워크북 + 그 셀들의 기준 반쪽전지** — 결과표에는 없다. 형식은 `<cycle>_capacity/<cycle>_voltage`.

**③ BML 다음 — 사용자 기계에서** (둘 다 `git pull` 뒤, `BMS_DATA_ROOT` 는 data/literature 가 있는 루트):

```bash
# 세트는 HD_knee (L_* 원자료는 없다 — BML_R1_RESPONSE §10-4). D = 규진팀 'degradation mode' 폴더, H = 하네스
# (b) 첫 실행은 끝났다 (§10-4 표). 깨끗한 시작점 실험은 scale 고정으로 다시:
python3 $H/scripts/fit_cycles.py --data-root "$D" --half-cell "$D/data/half_cell/GITT/pristine.xlsx" \
  --full-cell "$D/experiment/HD_ICA/300cycle knee point large cell.xlsx" --cell HD_knee --si-source Li \
  --starts 20 --seed 1 --scale-seed 0 --out ~/out_cycles/seed1s0
python3 $H/scripts/fit_cycles.py ... --seed 0 --scale-seed 0 --out ~/out_cycles/seed0s0
python3 $H/scripts/check_rails.py ~/out_cycles/seed0s0/cycles_HD_knee_Li.csv ~/out_cycles/seed1s0/cycles_HD_knee_Li.csv
python3 $H/scripts/check_u14.py --new ~/out_cycles/seed1s0 --old ~/out_cycles/seed0s0   # scale_* 같고 numbers 만 다르면 그 차이가 시작점의 것
# (a) MATLAB — D 폴더에서 (rng( 가 남아 있으면 드라이버가 거부한다). fit_cycles_driver.m 을 D 로 복사한 뒤:
#   cfg = struct('pipeline_dir',pwd,'data_root',pwd,'half_cell_file',fullfile(pwd,'data\half_cell\GITT\pristine.xlsx'), ...
#     'full_cell_file',fullfile(pwd,'experiment\HD_ICA\300cycle knee point large cell.xlsx'),'cycles',[], ...
#     'si_source','Li','label','HD_knee','out_dir','results_refit');
#   fit_cycles_driver(cfg)      % → results_refit/result_HD_knee_Li.xlsx + .settings.json
python3 $H/scripts/check_rails.py "$D/results_refit/result_HD_knee_Li.xlsx"   # 2 층 repeated_values 가 사라졌는가
```

### R13 §5 Q6 닫음 — shape 전용 kind · schema · sidecar 계약 (2026-09-13)

리뷰어 실측을 그대로 RED 로 옮겼다 (`test_g25`: 실제 `ne_shape.py` → 실제 `shape_step` → `check_u14 --schema-only`):
**schema 27 · provenance_cols 3 · content 1** — 리뷰어 숫자 그대로 재현됐다. 원인은 `check_u14._kind` 와
`schema.body_roster` 가 각자 "matrix 아니면 profile" 이라 `ne_shape_*.csv` 도 모르는 이름도 profile 로 읽힌 것.
"PROFILE_ROW 에 열 19 개를 허용" 이 아니라 **종류를 하나 더 만든다**:

| 축 | 어디 | 무엇 |
|---|---|---|
| kind 라우팅 | `schema.kind_of(name)` | 한 함수 · 모르는 이름은 `ValueError` (fail-closed). `check_u14._kind`·`body_roster` 가 이것만 쓴다; gate 는 모르는 이름을 "모르는 산출 종류" content 로 센다 |
| 열 정본 | `schema.SHAPE_ROW` (22) | 기존 20 + `inputs_sha`·`consumed_inputs`. producer 의 header 가 이 tuple 에서 나온다 |
| 행 key | `schema.shape_key` = `state` · `row_key(kind)` | 중복 상태는 중복 key |
| receipt | 행마다 역할 `SHAPE_ROLES` = matrix · half_cell · half_cell_pristine · literature.gr · literature.si | `_row_receipt` 가 sidecar 의 상태별 dict 를 역할 모양으로. 짝 없는 행은 빈 칸(receipt 를 지어내지 않는다) |
| 빈 칸 허용 | `SHAPE_MAY_BE_EMPTY` = witness 둘 | R3-03 의 "격자에서 증인 없음" — 둘이 **함께** 비어야 한다 |
| coverage | `check_shape_coverage` | 본문 상태 집합 ↔ `canonical_shape_states(source)` (= `data.declared_states`, producer 와 같은 함수). 선언 밖 상태 = content · 부분집합 = 자리 규칙(`CANONICAL_SLOT_PREFIX`) |
| sidecar | `check_shape_meta` | typed `status` · `pairing` 산술(available ⊎ missing_input = requested · paired ⊎ missing = available) · 본문 결속 · authority = 정본 · status = producer 판정식 |
| meta 계약 | `_write_csv` | env · started_utc · git_commit_at_start · git_state_changed_during_run · argv · roster(잠금 안 같은 bytes) — `write_meta` 와 같은 축. 실행 조건은 `meta_controls("shape")` = half_cell_source · si_source · grid_n · grid_range · gamma_grid (state/starts/seed 가 아니다) |

회귀 `test_g18~g25`. g25 가 producer→wrapper→U14 완주(합성 원자료 + fixture matrix)와 **두 번째 독립 실행의
승격 자격**(숫자·입력 identity·조건 동일, clean 트리면 `promotion_eligible: true`)까지 잰다.
리뷰어 스크립트의 `consumed={"synthetic": True}` 는 receipt 가 아니라 **receipt 축에서만** 막힌다 (g21) — 그 호출이
통과하지 않는 것이 맞다.

옛 정본(지금은 `out/archive/legacy_r6_u14/`, U18b 승격으로 얼렸다 — 그 경로에서 같은 수가 그대로 재현된다)의 blocked_by 는 59·27·5·1 → **40·25·6·1**: 옛 shape 가 이제 제 종류로 읽혀 "열 19 개 모름 + profile 열
21 개 누락" 이 사라지고, 대신 `inputs_sha`·`consumed_inputs` 누락 2 · `status`·`pairing` 없음 2 로 잡힌다.
**숫자는 여전히 하나도 안 움직였다.** 옛 sidecar 를 소급 보수하지 않는다 (리뷰어 §Q6 답 그대로) — 실데이터
재생성은 사용자 기계에서 아래 U18 4 단계로.

코드 `ef8e8f6` · 증거 `84ab3b3` (`reviews/r13_repros/replay_ours_after_fixes/`, leaf 별 판정은 직전 판과 동일) ·
회신 `reviews/R13_RESPONSE.md` — 발견 9 건 + Q6 · GO 조건 1~8 대응 · 열린 것(조건 6 동적 인증 · 조건 7 실데이터 재실행 · 조건 8 다섯 축).

---

### 다음 — Codex 토큰 복구, 리뷰 요청 3 건 대기 (2026-09-13)

Codex 를 다시 쓸 수 있게 되어 요청문 셋을 썼다. **보내는 순서도 이 순서다.**

| 순 | 요청문 | 대상 | 왜 이 순서 |
|---|---|---|---|
| 1 | `reviews/REQ_MPH_MICROSHORT.md` | 규진팀 마이크로 쇼츠 COMSOL 모델 분석 (`docs/MICROSHORT_MPH_REVIEW.md`) | 지금 제일 뜨겁고 반증 가능성이 명확하다 — `cEeqref` 가 SOC 분모라는 전제(A1) 하나가 무너지면 M1 이 통째로 무너진다. COMSOL 미실행 |
| 2 | `reviews/R13_REQUEST.md` | 하네스 13차 — 자체 리뷰 35 건 닫음 (`c7217c0` 코드 · `85038ee` 증거) | 쌓인 빚. R11 이후 외부 눈이 한 번도 없었다. 핵심 물음은 "§2 의 반쪽으로 닫음 패턴이 이번 35 건에도 있는가" |
| 3 | `reviews/REQ_FIT_RAILS.md` | α·β 적합 출력의 난간·축퇴 (xlsx 37 행) | MATLAB 원본을 봐야 결론이 나서 Codex 혼자로는 절반만 답한다 (B3 = `a_PE` 상한 존재가 유일한 약점) |

`reviews/R12_REQUEST.md` 는 **보내지 못한 문서**로 배너를 달아 보관했다 (R13 이 대신한다).

**1차 결과 (mph 트랙, 2026-09-13): NO-GO.** "M1 은 확정 버그이므로 `cEeqref` 두 줄부터 고친다" 가
당시 증거로 성립하지 않았다. 패키지는 `reviews/r14_repros/codex/` 에 원본 보존(zip sha256
`e2d74fb8390e…`), 대응 원장은 `reviews/MPH_R1_RESPONSE.md`, 문서는 v2 로 재작성했다.
**바뀐 결론 다섯**: (1) M1 은 조건부 진단 — 조건은 `liion.pce2.pin1.soc` t=0 값 한 번으로 끝난다
(2) 붕괴하는 것은 **두 LAM** 뿐, LLI 는 독립 (3) 휴지 후반 기울기는 쇼츠 전용축이 **아니다**
(`C_diff` 가 LLI/LAM 에 의존) (4) **Events 인터페이스 자체가 DISABLED** 였다 (5) `tau_short` 차원 오류.

**교훈**: v1 §7 의 정규식 추출기가 자식 flags 를 부모로 전파해 (4)를 틀리게 만들었다. 리뷰어가
원본 파일 없이 정적 반례만으로 잡았다. 교정 도구 `reviews/r14_repros/mph_dump.py` 는
`--self-test` 로 그 반례를 고정하고 태어났다 — `evidence_gate` 규율을 분석 스크립트에도 적용한다.

**mph 트랙 다음 순서** (2026-09-13 저녁, 6.3 재구축 검토 뒤 갱신 — `COMSOL_REBUILD_SPEC.md` §8-5):
① ~~baseline 보존, Eeq 분해·표면/평균 조성 export 로 검토 산술 현지 확인~~ → **됨** (§9-1: Eeq 3.578387/1.413053 V, 상한 4.185562 V)
→ ② 중단조건·CDC: 표면 조성 이탈 중단 **실제 발생**(`INCOMPLETE_RANGE_STOP`) · 2.7 V cutoff · 전이 확인됨(축소 조건). **메시 수렴은 미완**:
   축 분리 결과(§10, 원문 대조·재계산 완료) — 물리축은 충족, **반경축이 2.505 mV** 로 초과. 시간 step 과의 미분리는 **제안 A 4 회로
   대부분 풀렸다**(§11, 전달 요약): 시간상한 반감은 μV 수준(0.000193·0.001422 mV)인데 반경 차는 2.506 mV 로 남는다.
   → 300/160 @0.0005 s 도 돌았다(§12): **80→160 이 1.248 mV @0.01 s 로 또 초과**, 최대 시각이 앞당겨졌다.
   → 다음은 **320 확대 전에 300/160 @0.00025 s 1 회** (결과 없음). 600/80 은 계속 보류
→ ③ 범위 감시 있는 `sigma_short=1e-20` 단일 프로토콜 진단 승인 여부 — ② 의 메시 결과가 1 mV 안이어야 논한다 (아직 아니다: 2.506 mV)
→ ④ 본 계산·유한 sigma·sweep 은 원본/실험 OCP 대조 뒤. 원본 모델 쪽은 문서 v3 로 정리됐고(M1 철회) `COMSOL_CHECK_REQUEST.md` 의 확인은 불필요해졌다.

검증 재실행 (2026-09-13, `26c477c`): `236 passed in 200.29s` · `git diff c7217c0 HEAD -- '*.py' '*.sh'` **0 개** ·
`replay_codex_r7.py --expected-head 26c477c…` rc 0 · `evidence_eligible: true` · `closed: true` ·
`check_u14 --schema-only` rc 2 (59 · 27 · 5 · 1, 보관 증거와 일치).
⚠ `expected_tree` 는 커밋을 따라간다 — 보관 증거는 `ae9e4847…`, `26c477c` 재실행은 `16d44946…`. 불일치가 아니다.

---


## 직전 상태 — Codex 11차 NO-GO (P1 12 · P2 6) 열여덟 건 전부 닫음 (닫힘)

2026-09-13 Codex 11차(대상 `2add074`, `reviews/R11_CODEX.md`, 패키지 `reviews/r11_repros/codex/` sha256 13/13)의 요지:
R10 의 열다섯 수정은 **각 산출 안에서는** 참이 됐지만 세 축이 열려 있다 — (a) 두 실행 **사이**의 입력 identity 를
아무도 대지 않아 old/new 의 네 digest 가 전부 달라도 `promotion_eligible: true` 였고(P1-1), (b) caller 옵션이 권위
명부 자체를 줄여 `--only-source`·`--grid 1` 이 complete canonical 을 게시했으며(P1-2·3) 부재 allowlist 가 실제로 있는
파일을 요청에서 빼고(P1-4) hardlink 자기대조와 `--schema-only` 가 승격 증명서로 통했다(P1-5·6), (c) 증거 기계가 자기
startup 을 안 봉인해 gate 보다 먼저 load 된 위조 pyc·checkout smudge·rc 7 자식·무관한 AssertionError 가 전부
`closed: true` 를 냈다(P1-10~12). 그 밖에 production reader 가 `error` 행을 과학 입력으로 먹고(P1-7), 비유한 값이
스키마를 통과하고(P1-8), untracked `sitecustomize.py` 가 실행되는데 provenance 는 clean 이었다(P1-9). P2 는 sink 에
따라 갈리는 부분 rc(P2-1) · stale wildcard 를 읽는 `shape_step`(P2-2) · 중복 논리 역할(P2-3) · parse 안 하는
`gamma_roster`(P2-4) · 대문자 `S` skip-worktree(P2-5) · 짧은 expected head(P2-6).

열여덟 건 전부 수정 전 clean 트리에서 재현(`reviews/r11_repros/replay_ours_2add074_before/`) →
RED(`tests/test_r11_codex.py` e11_01~19) → 수정 → GREEN. 원장은 `reviews/R6_LEDGER.md` "Codex R11" 절, 요청문은
`reviews/R12_REQUEST.md`. 닫힘 재생기는 `reviews/r11_repros/replay_codex_r11.py` (case 별 **봉인한 술어**로만 닫힘을
센다 — 반례 소멸 32 · 전제 변경 2 · 환경상 불가 1).

**새 규약(11차에서 더한 것)**: 승격은 baseline↔candidate 의 `{역할: full sha256}` 이 **같아야** 하고 한쪽이 입력을 안
적었으면 "대조 불가" 로 승격 자격이 없다 · 권위 명부는 caller 옵션으로 줄지 않는다 (좁힌 실행은 `subset` rc 3 ·
`partial/`) · 정본 γ 격자는 `S.CANONICAL_GAMMA_GRID_N = 21` · 부재 allowlist 가 실제 파일과 모순되면 hard-fail ·
sidecar 는 `argv`·`roster` 를 반드시 담고 명부 유도는 `schema.body_roster` **한 자리** · production reader 는 checker 와
같은 validator 를 exact header 로 통과한 묶음만 먹는다 · 과학 값은 전부 유한해야 한다 · 산출 root **밖**의 untracked 는
코드다 · 증거 러너는 gate import **전에** bytecode 를 격리하고 materialize 한 bytes 를 blob 과 재대조하며 full 40 자
expected head 만 받고 자식 rc 0 을 강제한다 · 닫힘 판정은 case 별 반례 fingerprint 로만.

**정본 범위 (변화 없음)**: 현행 `out/` 12 개는 여전히 **provenance-incomplete** (출처 열 24 + profile `gamma_roster` 4 +
digest 규칙 변경으로 재계산과 안 맞는 degeneracy 4). 숫자는 하나도 안 움직였다 — 바뀐 것은 규칙이다. U18 재실행이
새 규칙으로 서명한다.

## 직전 상태 — Codex 10차 NO-GO (P1 8 · P2 7) 열다섯 건 전부 닫음 (닫힘)

2026-09-13 Codex 10차(대상 `bd6ba47`, 코드 정본 `554dad6`, `reviews/R10_CODEX.md`, 패키지 `reviews/r10_repros/codex/`
sha256 10/10)의 요지: R9 의 열두 수정은 허상이 아니지만 **그 문장이 게시 경계·승격 gate·증거 기계에서는 아직 참이
아니다** — `eval --out X --compare X` 가 독립 근거를 제 출력으로 덮고 자기대조를 `complete` 로 냈고(P1-1), `ne_shape
--states` 가 정본 roster 를 줄여 1 행을 complete canonical 로 게시했고(P1-2), profile 의 실패한 γ 와 matrix 의 전
조합 실패가 canonical 을 부수며 rc 0 이었고(P1-3·4), `error` 한 칸이 행 검증을 전부 껐고(P1-5), receipt 가 역할을
안 묶어 decoy 하나로 통과했고(P1-6), env·control 이 사실상 검사되지 않았고(P1-7), candidate 와 baseline 이 같은
디렉터리여도 승격 판정이 났다(P1-8). P2 는 subset 의 rc 0(P2-1) · stdout invalid rc 0(P2-2) · argv 평탄화와 production
결속 없는 회귀(P2-3) · `python -O` 에서 증거가 다 통과(P2-4) · 실행 bytes 미봉인(P2-5) · package digest 회귀 부재(P2-6)
· ne_shape typed status 를 쓰는 caller 부재(P2-7).

열다섯 건 전부 수정 전 clean 트리에서 재현(`reviews/r10_repros/replay_ours_bd6ba47_before/`) → RED(`tests/test_r10_codex.py`
d10_01~16) → 수정 → GREEN. 원장은 `reviews/R6_LEDGER.md` "Codex R10" 절, 요청문은 `reviews/R11_REQUEST.md`.

**새 규약**: 게시는 **완전성 판정 뒤에만** — matrix·profile·ne_shape 가 typed status(complete/partial/none/subset)를
내고 complete 만 canonical, 나머지는 `partial/` 에 (`PRODUCER_EXIT` 0/3/1) · 정본 roster 는 `D.declared_states(source)`
이고 caller 의 `--states` 는 좁히기만 하며 그 실행은 승격 대상이 아니다 · 알려진 부재는 `D.HALF_CELL_ABSENT` 로 명시
(실측 근거는 원장) · receipt 는 **역할**을 묶는다(`REQUIRED_ROLES`, digest 는 `(역할, sha256)`) · `error` 행이 있는
묶음은 success 가 아니다 · `check_u14` 는 env 를 값으로 대고 필수 control 이 양쪽에 있어야 하며 candidate·baseline
독립성을 요구하고 `--subset` 은 rc 3 + `PROMOTION {…}` 줄을 낸다 · degeneracy 는 sink 와 무관하게 invalid 면 rc 2 ·
증거 러너는 `reviews/evidence_gate.py` 한 자리에서 `-O` 거부 · git rc 확인 · index skip flag 거부 · `__pycache__` 격리 ·
**expected commit 의 sparse worktree 에서 대상 bytes 실행** · 도구 자신의 봉인(`instrument_sealed`)까지 본 뒤에만
`evidence_eligible: true`.

**정본 범위**: 현행 `out/` 12 개는 여전히 provenance-incomplete (출처 열 24 + profile `gamma_roster` 4). 여기에
**digest 규칙 변경**이 더해졌다 — `inputs_digest` 가 역할을 묶으면서 값이 달라져 커밋된 degeneracy 네 개의 옛
`inputs_sha` 가 재계산과 안 맞는다 ("내용 검사 실패 4"). 숫자는 하나도 안 움직였고 바뀐 것은 규칙이다; 소급해서 고쳐
넣지 않고 U18 재실행이 새 규칙으로 서명한다. `check_u14 --new out --schema-only` 가 rc 2 로 말한다.
자기 점검(`--new out --old out`)은 이제 **거부**된다 (P1-8) — 승격 대조는 독립 baseline 으로만.

## 직전 상태 — Codex 9차 NO-GO 열두 건 닫음 (닫힘)

2026-09-12 Codex 9차(대상 `29ef505`, `reviews/R9_CODEX.md`, 패키지 `reviews/r9_repros/codex/` sha256 11/11)의 요지: R8 의 여덟
수정은 허상이 아니지만 **"모집단을 먼저 세고, 검증 snapshot 만 검사하고, 부분은 부분이라 말한다" 가 아직 production 전체의
불변식이 아니다** — 같은 root label 이 앞 요청을 지우고(R9-01), `check_u14` 가 new 에 있는 파일만 세어 1/12 도 전수로 승인하며
(R9-02) 열 이름만 보고 내용·과학 열·실행 조건을 안 보고(R9-03), `ne_shape` 가 없는 반쪽전지 상태를 requested 전에 지우고(R9-04)
중복 matrix key 의 첫 행을 쓰고(R9-05) rc 3 을 내기 전에 완전 canonical 을 부분으로 덮고(R9-06), `eval --compare` 가 경로를 세 번
읽는다(R9-07). P2: 러너의 공허 성공(P2-1) · evidence identity 미집행(P2-2) · rc 2/3/4 를 CAUGHT(P2-3) · matrix sidecar 의
singular 범위(P2-4) · zero-pair 1 vs partial 3 계약(P2-5).

열두 건 전부 수정 전 HEAD 에서 재현(`reviews/r9_repros/replay_ours_29ef505_before/`) → RED(`tests/test_r9_codex.py` d9_01~12)
→ 수정 → GREEN. 원장은 `reviews/R6_LEDGER.md` "Codex R9" 절, 요청문은 `reviews/R10_REQUEST.md`. 수정 뒤 패키지 재실행과 닫힘
재생기(`reviews/r9_repros/replay_codex_r9.py`, R7 러너와 같은 `--expected-head`·dirty·digest 계약)는 `reviews/r9_repros/
replay_ours_after_fixes/`.

**새 규약**: 스키마의 정본은 `bms_balancing/schema.py` 하나 (producer 가 쓰기 직전에 assert, checker·reader 가 같은 함수) ·
`check_u14` 는 명부(정본 ∪ 새 산출)·필수 셀·receipt 내용·중복 key·실행 조건까지 보고 부분 재실행은 `--subset` 계약으로만
(k/N 표시, 승격 아님) · `compare_states` 는 중복 root label 을 판정 전에 거부 · `ne_shape` 는 requested 를 파일 존재 전에 고정하고
typed `status`(complete 0 / none 1 / partial 3) 로 complete 만 canonical 에, 나머지는 `<write>/partial/` 에 · `eval --compare`
는 한 번 읽은 `DdEvalText` snapshot 만 소비 · 두 러너(R7·R9)는 `--expected-head` 필수 + dirty 기본 거부 + 패키지 digest · 변이
감사 CAUGHT 는 rc 1 ∧ `N failed` 만 · `run_states.sh` sidecar 에 `argv`·`roster`.

**fixture 정정**: `_full_matrix_rows`·`_deg(schema=True)`·`_u14_dirs`·i6w_03 의 inline JSON 은 열 이름의 부분집합 + 가짜 receipt
였다 (checker 가 내용을 안 본다는 사실을 가려 줌 — 이 저장소 네 번째 실측). 전부 producer 스키마 + 진짜 receipt 로 다시 썼다.

**정본 범위 (변화 없음)**: 현행 `out/` 12 개는 내용·조건·자기 대조 숫자는 새 검사를 통과하지만 matrix/profile 8 개에 출처 열
3 개가 없다 — **provenance-incomplete** (`check_u14 --new out --schema-only` rc 2, 24 건). 보강은 U18 (사용자 기계, 별도 `OUT=`,
이제 `check_u14` 가 명부 12/12·스키마 내용·조건·수치 exact equality 를 강제한 뒤에만 승격). 열어 둔 것: export 공통 snapshot
계약(Codex Q3) · typed (root, state, si) identity (Q1).

## 직전 상태 — Codex 8차 NO-GO 여덟 건 닫음 (닫힘)

2026-09-12 Codex 8차(대상 `a22da33`, `reviews/R8_CODEX.md`, 패키지 `reviews/r8_repros/codex/`)의 요지: R7 반례는 닫혔지만
**"검증된 개별 묶음 → 완전한 모집단 → 전체 결론" 의 합성**이 안 이어진다 — 같은 state 의 다른 Si 가 서로 덮고 빈 요청
root 가 후보에 안 든다(R8-01), `check_u14` 가 data B/meta A 를 인증하고 출처 열을 요구하지 않는다(R8-02), `ne_shape`
요약이 γ-짝 부분집합에서 측정 최대를 잰다(R8-03), profile 의 전체 입력 identity 가 잘려 나가는 `.log` 에만 있다(R8-04).
P2: 중복 key 행 소실(R8-05) · 선택 0 을 CAUGHT(R8-06) · post-fix 재생 명령 부재(R8-07) · c6_01 의 callback 계수(R8-08).

여덟 건 전부 수정 전 HEAD 에서 재현(`reviews/r8_repros/replay_ours_a22da33_before/`) → RED(`tests/test_r8_codex.py`
d8_01~09) → 수정 → GREEN. 원장은 `reviews/R6_LEDGER.md` "Codex R8" 절, 요청문은 `reviews/R9_REQUEST.md`.

**정본 범위**: 현행 `out/` 12 개는 수치는 R7 과 바이트 동일하고 묶음 12/12 True 이지만 matrix/profile 8 개에
`ref_inputs_sha`·`consumed_inputs`·`ref_consumed_inputs` 가 없다 — **provenance-incomplete** (기준 입력의 출처는 그
묶음에서 회수되지 않는다; `check_u14 --new out --schema-only` 가 rc 2 로 말한다). 보강은 **U18**: 사용자 기계에서
`run_states.sh` 를 별도 `OUT=` 으로 돌려 수치 동일을 확인한 뒤 승격 — pathname 해시로 소급 채우지 않는다. 그때까지
인용은 "수치 그대로 · 기준 입력 출처 미기록" 으로 범위를 붙인다.

규약이 바뀐 것: `load_degeneracy` 는 Si 충돌 시 `state|si` key 로 전부 보존 · `compare_states` 는 요청 root roster 를
찍고 관측 0 인 root 가 있으면 미완 rc 2 · `check_u14` 는 검증 snapshot 만 검사하고 출처 열을 필수로 · `ne_shape` 는
`pairing` 을 남기고 짝이 빠지면 rc 3 · profile 행이 전체 입력 identity 를 실어 나른다 · 변이 감사는 선택 0 을 오류로.

## 직전 상태 — Codex 7차 NO-GO 여섯 건 닫음 (닫힘)

2026-09-12 Codex 7차(대상 `521be85`, `reviews/R7_CODEX.md`)는 **재현 패키지와 함께** 왔다 (`reviews/r7_repros/codex/`,
sha256 10/10). 판정 요지: R6 반례는 닫혔고, **올바르게 읽은 다음 단계**가 안 이어진다 — 반례 상태가 미완으로 빠지면
집계가 "아니오"를 "예"로 뒤집고(R7-01, 빈 디렉터리도 "예"), 잡음 진단이 적합과 **다른 snapshot** 으로 σ 를 재고
(R7-02), matrix/profile 행이 **기준** 입력 출처를 안 남긴다(R7-03). P2 셋은 `check_u14` 의 정책 혼선(R7-04),
우리 재생 스크립트의 baseline 기본값(R7-05), 변이 감사의 rc 0(R7-06).

여섯 건 전부 수정 전 트리에서 재현 → RED(`tests/test_r7_codex.py` d7_01~07) → 수정 → GREEN. 수정 뒤에는 패키지
probe 가 **자기 반례 assertion 에서** 멈춘다 (`reviews/r7_repros/replay_ours_*.json`). 원장은 `reviews/R6_LEDGER.md`
"Codex R7" 절, 요청문은 `reviews/R8_REQUEST.md`.

규약이 바뀐 것: 집계는 **후보/검증/제외**를 세고 제외가 있으면 전체 판정 대신 미완 + rc 2 · `cmd_noise` 는
`build` 가 소비한 원시 배열(`obj.full_cell_raw`)로만 σ 를 잰다 · matrix/profile 행이 `ref_inputs_sha`(+identity)를
남긴다 · `check_u14 --baseline-policy` 로 현행/역사 규칙을 **호출 모드로** 가른다.

## 직전 상태 — Codex 6차 NO-GO 여섯 건 닫음 (닫힘)

2026-09-12 Codex 6차 리뷰(대상 `d431404`, `reviews/R6_CODEX.md`)는 출처 결속 세 조건을 P1 으로 짚었다 — 독자가
검증한 snapshot 이 아니라 경로를 다시 읽는다(R6-01), 현행 산출에 meta 가 없으면 옛 산출로 흘러 들어간다(R6-02),
입력을 파싱한 뒤 경로를 다시 열어 해시한다(R6-03). P2 셋은 정본 선택 규칙이 옛 `_v2` 를 골랐다(R6-04), `-z`
경로를 " -> " 로 쪼갰다(R6-05), U14 판정문의 "적은 시작" 오기(R6-06 — 실제 γ당 25 회). 여섯 건 전부 우리 트리에서
RED 로 재현한 뒤 닫았다 (`tests/test_r6_internal.py` C 절 `test_c6_01`~`06` + Q3 pin). 원장은 `reviews/R6_LEDGER.md`
"Codex R6" 절, 요청문은 `reviews/R7_REQUEST.md`.

규약이 바뀐 것: 독자는 `provenance.read_unit` 이 돌려준 (data, meta) snapshot 만 소비한다 · `run_id` 가 있는
산출은 meta 없이는 미완(False) · 입력은 `data.read_input` 의 bytes 로 파싱과 해시를 같이 한다 · 정본은 unversioned
이름 하나이고 `_vN` 은 `out/archive/` 의 역사 자료다.

**Codex 재현 패키지는 닫은 뒤에 받았다** (`reviews/r6_repros/codex/`, 원본 10 파일 sha256 OK). 세 판으로 돌렸다:
대상 `d431404` 격리 worktree 에서 **일곱 probe 전부 재현** · HEAD 에서 원본 probe 는 전부 '안 재현' 이지만 넷은
hook 이 빗나간 것이라 **적응판**(hook 만 현행 코드로, 판정은 뒤집어)으로 다시 재 **6/6 닫힘** · 그 적응판을 변이로
검사해 **5/5 CAUGHT**. 적응판 변이가 두 군데를 고쳐 줬다 (R6-01a 가 한 순서만 쟀다 · R6-03b 변이를 원 결함이 아닌
자리에 넣었다). 재생 명령은 `R7_REQUEST.md` §0 의 블록.

## 직전 상태 — R6 내부 리뷰 30 건 닫음 · U13·U14·U15 실측 완료 (닫힘)

Codex 토큰 소진으로 6차는 `/self-review` 로 돌렸다 (네 렌즈 37 건 → 적대적 검증 CONFIRMED 30, 전부 RED → 수정 →
GREEN). 그 뒤 사용자 기계 실측 셋이 붙었다 — U13(scale 동치 18 build), U15(MATLAB `sprintf` 기준선), U14(네 상태
재실행). 원장은 `reviews/R6_LEDGER.md`, 요청문은 `reviews/R6_REQUEST.md`.

**U14 판정: 결론 숫자는 전부 재현됐다.** matrix 세 상태와 degeneracy 세 mode 폭이 **0.00e+00**, §5-1 문턱 표의
n 과 최악 비도 동일. 움직인 것은 γ 프로파일의 개별 행(LAM_NE 최대 2.8e-2)뿐이고 §5-1 폭은 넷째 자리에서만
바뀐다. 두 산출 모두 γ당 25 회를 썼고 **같은 예산 아래 일부 행이 달랐다 — 원인은 U16 미확정**이다 (Codex
R7 §5). 정본을 만든 라이브러리 조합은 모른다(그 산출에 `env` 가 없다) — "scipy 판 때문" 은 가설이고 U16(옛 조합
재실행)이 닫는다. **어떤 결론도 뒤집히지 않았다.**

U14 가 드러낸 다섯 건(U14-01 줄끝로 서명이 fresh clone 에서 깨짐 · 02 도구의 정본 선택 · 03 새 열을 소비 helper 가
못 읽음 · 04 충돌 표식 · 05 재실행이 §4-0 의 역사 자료를 덮음)은 전부 닫았다.

남은 것: Codex 6차 요청문 송부 (토큰 복귀) → 새 모델 설계 요구서 (문헌 입력은 `docs/LIT_19_20_FOR_NEW_MODEL.md`).
아래 명령은 실행 기록.

```bash
# ── 0. 받기 · 확인 (몇 분) ────────────────────────────────────────────────────────────────────────
cd ~/dd/bms-balancing && git pull --rebase origin claude/bms-alpha-beta-verify
source .venv/bin/activate && export BMS_DATA_ROOT='/mnt/d/가형 관련/degradation mode'
python3 -m pytest tests/ -q                       # 345 passed 기대 (원자료 불필요)

# ── 1. 배관 확인 — 새 스키마가 붙는지만 (몇 분, STARTS=6 이라 수치는 못 쓴다) ─────────────────────
STARTS=6 STATES=100 OUT=out_u14_smoke ./scripts/run_states.sh
python3 scripts/check_u14.py --new out_u14_smoke --schema-only     # 0 이어야 한다
# ↑ 0 이 아니면 여기서 멈추고 출력을 그대로 붙여 줘. 2 = 스키마 누락(옛 코드로 돈 것).
rm -rf out_u14_smoke

# ── 2. 본 실행 — 정본을 덮지 않고 **다른 디렉터리로** 받는다 (몇 시간) ────────────────────────────
#    정본(out/)을 먼저 덮으면 "숫자가 움직였나" 를 댈 대상이 사라진다. 네 상태 × 세 명령 = 12 회.
OUT=out_u14 STATES='100 200 300_0009 300_0147' ./scripts/run_states.sh 2>&1 | tee out_u14.log

# ── 2b. U18-01 뒷수습 — **닫힘** (2026-09-13, 첫 판에서 했다; U18b 는 wrapper 가 GITT 로 걸어 필요 없다) ──────
#    실측: 13 산출 중 shape 가 `ne_shape_step_005C_Li.csv` (정본은 `ne_shape_GITT_Li.csv`). 원인은 wrapper 의
#    `--source "${SHAPE_SRC:-${SRC:-GITT}}"` — loop 변수 `SRC` 가 300_0147 의 step_005C 로 남아 있었다. 고침(SHAPE_SRC 아니면
#    GITT, 요약 줄에 찍음; 회귀 `test_g27` 은 production 스크립트를 통째로 돌린다). shape 만 다시 만든다 — producer 가 자기
#    sidecar 를 스스로 쓰므로(`sidecar_dict`) 직접 불러도 wrapper 를 거친 것과 같은 산출이다. 잘못 만든 것은 지우지 않고
#    옆으로 치운다 (check_u14 는 하위 디렉터리를 안 본다 → 승격 대상에서만 빠진다).
git pull --rebase origin claude/bms-alpha-beta-verify
mkdir -p out_u18/wrong_source && mv out_u18/ne_shape_step_005C_Li.csv out_u18/ne_shape_step_005C_Li.csv.meta.json out_u18/wrong_source/
python3 scripts/ne_shape.py --out-dir out_u18 --write out_u18 --source GITT --si-source Li 2>&1 | tee out_u18/ne_shape_GITT.log | tail -3
python3 scripts/check_u14.py --new out_u18 --schema-only | tail -1      # 계약 위반 0 이어야 한다

# ── 2c. U18b 재실행 (U18-02·03 을 고친 뒤) — 승격하려면 이것이 필요하다 ────────────────────────────
#    왜 다시 도나: U18-02 의 고침은 **다음 실행의 서명**을 고친다. 이미 적힌 sidecar 의 `git_state_changed_during_run:
#    true` 11 개는 그대로이고(승격은 값 자체를 요구한다 — R11 P1-9), `matrix_100` 은 그 위에 **실제로** 실행 중
#    커밋이 바뀌었다 (d07a77a → c9dd822). 사면 규칙을 만들지 않는다 — 깨끗한 트리에서 다시 돈다 (~2 시간 40 분).
#    ⚠ 첫 판은 버리지 말고 저장소 **밖으로** 옮긴다: 저장소 안에 남기면 그것이 새 실행의 '코드 변경' 이 된다.
cd ~/dd/bms-balancing && git pull --rebase origin claude/bms-alpha-beta-verify && source .venv/bin/activate
export BMS_DATA_ROOT='/mnt/d/가형 관련/degradation mode'
mv out_u18 ~/u18_run1 && mv out_u18.log ~/u18_run1.log 2>/dev/null
git -C ~/dd status --short          # ★ 아무것도 안 나와야 한다 (나오면 그것이 '코드 변경' 으로 서명된다)
python3 -m pytest tests/ -q         # 277 passed
#    ⚠ 도는 동안 `~/dd` 에서 git 명령(pull·checkout·commit)을 **하지 않는다** — 그것이 첫 판 matrix_100 을 깬 것이다.
OUT=out_u18b STATES='100 200 300_0009 300_0147' ./scripts/run_states.sh 2>&1 | tee ~/out_u18b.log
#    shape 는 이제 wrapper 가 GITT 로 건다 (U18-01 고침) — `ne_shape_GITT_Li.csv` 가 나와야 한다. 끝나면 3 단계로.

### 14 차 결과 — **NO-GO · P2 3 건, 전부 닫음** (`reviews/R14_RESPONSE.md`, 2026-09-14)

리뷰어는 **U18b 이관을 수용**하고 **재계산을 요구하지 않았다** (옛 26 개 bytes·새 13 개 계약·공통 수치 5,184 개 차이 0 을
자기 기계에서 확인). 남은 셋은 좁은 P2 다.

| # | 반례 | 고침 | 회귀 |
|---|---|---|---|
| P2-1 | `OUT=reports/out_u18` 같은 **중첩** 산출 경로가 코드 변경으로 분류된다 — `git status -unormal` 이 `?? reports/` 로 접기 때문 | 접힌 항목이 지정 root 를 품으면 그 경로만 `-uall` 로 다시 물어 실제 파일로 펴서 분류 (`provenance._untracked_files`) | `test_h01` — 중첩 clean · root 밖 sibling 은 여전히 dirty 이고 **실제 파일명**을 지목 |
| P2-2 | 새 sidecar 에 `env={"python": …}` 만 남겨도 `--schema-only` rc 0 | baseline 과 무관하게 새 sidecar 전부에 `ENV_KEYS` 다섯 축 존재·비공백 요구 | `test_h02` — 네 종류 × 축 하나씩 뺀 다섯 + 리뷰어 반례 + 대조군 |
| P2-3 | 승격 **뒤** `--old-rev HEAD` 는 rc 4 가 아니라 **rc 2 · alias 13**(자기대조 거부, 맞는 동작). 증거 README 의 코드 동일성 명령은 17 개를 낸다 | 기준을 full commit 으로 고정 — `42314198…`(= `37a889b^`) 대비 rc 4, 증거 명령은 `df6413d…→1bb45b3…`(0 개) | 문서 정정 (실측 재현은 회신 §2) |

리뷰어 §7 답 처리: `env_uncomparable` 수용(P2-2 로 완성) · `--accept-uncomparable` 대신 **`legacy_transition_approved`**
별도 판정 권고는 **동의하되 이번엔 미구현**(게이트 계약 변경, 다음 라운드) · 승격 묶음은 **기본 단일 commit**, 이번
혼재는 범위 한정 예외로 기록(U18-05) · 기록용 CLI 인자 필수화는 열림 · 역사 bytes 유지.

`reviews/R14_REQUEST.md` 는 **고치지 않는다** — 리뷰어가 sha256 `17995cfd…` 로 고정해 심사한 원본이다. 정정은 회신과
현행 문서에 둔다.

**종결 (`3aca090`, 2026-09-14): R14 GO** — P2-1·P2-2·P2-3 전부 종결 인정. 리뷰어가 인용한 tree `84a4bac041643fb4dd9b5885ffa57f3f83eaefd8` 를 우리 쪽에서 확인했고 일치한다. 근거: 관련 회귀 9 개 통과(빈값 100 조합 포함) · 현행 rc 0 · legacy rc 2(40·25·6·1) · 기존 산출 52 파일 불변. 리뷰어는 **286 전수를 재실행하지 않았다**고 밝혔고 Octave·동적 재생도 안 돌렸다. 이 GO 는 **R14 범위 한정** — 전체 하네스·BML 과학 타당성·COMSOL·장시간 실행 승인이 아니다. 패키지 원문은 `reviews/r14_repros/codex/closure_3aca090/`.

**후속 확인 (`f21cb648`)**: P2-1·P2-3 **종결**, P2-2 는 공백값 하나 남았다 — `env.scipy` 가 `"   "`·`"\t\n"` 이어도 rc 0 이었다.
우리 검사가 `in (None, "")` 이라 **"존재·비공백" 이 절반만** 구현됐고, degeneracy 본문 검사는 이미 strip 을 쓰고 있었으니
**규칙이 두 벌**이었다. `schema.env_axes_missing` 한 자리로 합치고 두 곳이 같은 함수를 부르게 했다. `test_h02` 가 네 종류 ×
다섯 축 × 다섯 빈값(빈 문자열·공백·탭줄바꿈·NBSP·null)을 전부 rc 2 로 고정한다. 286 passed.

### 14 차 게이트 리뷰 요청 — `reviews/R14_REQUEST.md` (대상 `1bb45b3`, 2026-09-14)

조건 7 을 닫은 경로와 발견 U18-01~04 을 실은 요청문. **비싼 본 실행을 요구하지 않는다** — 실데이터 재실행은
이미 끝났고 승격됐으므로 GO 의 뜻은 "이 승격과 네 발견의 처리를 받아들인다" 다. 묻는 것 다섯(§7): `env_uncomparable`
등급 · 승격 근거를 사람 결정으로 둔 것(도구가 감사 가능한 판정을 내야 하는가) · **U18-05**(승격 묶음의 `git_commit`
혼재를 게이트가 막아야 하는가 — 우리가 찾고 **안 닫은** 것) · U18-02 고침 범위(기본값 제거·fail-closed) ·
U18-04 의 표본을 실제 bytes 로 둘 것인가. COMSOL 은 **범위 밖**으로 명시했다 (§8: §10 만 저장소로 검증 가능,
§11·§12 는 원문 미수령이라 전사일 뿐 — 원문이 오면 한 번에 묻는다).

### U18-04 — 승격이 깨뜨린 것: 살아 있는 정본을 표본으로 쓰던 테스트 (2026-09-14, 닫음)

승격 직후 전체 테스트가 **7 건** 빨갛다. 셋은 계약 변경, 셋은 표본 이동, 하나는 내 동시 실행이었다.

| 무엇 | 왜 | 고침 |
|---|---|---|
| `_ne_shape_csv` 가 `inputs_sha` 를 `float()` 로 읽어 ValueError (§1-12·§5-2·R3-03 표 대조 셋) | 헬퍼의 `NE_SHAPE_TEXT_COLS` 가 schema 와 **별개의 사본**이었다. 정본이 22 열 계약으로 바뀌자 모르는 열을 숫자로 읽었다 — `test_i6w_07` 이 2026-09-12 에 "커밋된 산출이 아직 옛 스키마라 fixture 가 진실을 가린다" 고 경고한 그 고장이 실제로 터진 것 | 목록을 `schema.SHAPE_NON_NUMERIC` 에서 **유도**한다 (열이 또 늘어도 안 깨진다) |
| `test_f26` 의 전제(reader 가 정본 matrix 를 거부한다)가 사라짐 | 승격으로 `out/matrix_*.csv` 가 새 계약이 됐다 — 거부될 이유가 없다 | 표본을 `out/archive/legacy_r6_u14/` 로. 얼린 묶음이라 다시는 안 움직인다 |
| `test_d8_02` 가 `out/` schema-only rc 2 를 기대 | 같은 이유 (이제 rc 0 이고 **그것이 승격의 뜻**이다) | 표본을 archive 로 + "현행 정본은 rc 0" 을 같이 고정 (검사가 "늘 rc 2" 를 재는 게 아님을 못박는다) |
| `test_d8_07` 이 전체 실행에서만 실패 | **내가 같은 `replay_codex_r7.py` 를 동시에 돌렸다** (증거 재생성). 단독 실행은 통과, 직렬 전체 실행도 277 passed | 고칠 것 없음 — 증거 재생성과 테스트를 겹쳐 돌리지 않는다 |

교훈은 U14-05 와 같은 축이다: **살아 있는 파이프라인 경로에 표본·역사 자료를 두면 재실행 한 번에 전제가 사라진다.**
archive 는 그래서 있다. 277 passed (승격 뒤 직렬 재실행).

# ── 3. 대조 — 새 스키마 + 정본과 같은 숫자인가 ───────────────────────────────────────────────────
python3 scripts/check_u14.py --new out_u18b --old out   # 0 = 승격 가능 · 1 = 숫자가 다름 · 2 = 계약 위반 · 3 = 부분 · 4 = 승격 불가
#    ⚠ 자체 리뷰 C11: **rc 만 보고 승격하지 말 것.** 정본이 옛 스키마라 입력 identity 를 댈 수 없으면 계약은 안
#      깨졌지만 승격 자격이 없다 (지금 `out/` 이 정확히 그 상태다 → 이번 U18 은 rc **4** 가 정상 결과다). 판정은
#      마지막 줄의 `PROMOTION` JSON 이다 — 붙여 줄 것은 그 줄과 `■` 블록 전부:
#         python3 scripts/check_u14.py --new out_u18b --old out | tail -1 \
#           | sed 's/^PROMOTION //' | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['promotion_eligible'], d['blocked_by'])"
#    승격 조건 (이번 U18 한정 — 옛 정본에 receipt 가 없어 gate 가 true 를 낼 수 없으므로 **기록된 결정**으로 한다):
#      numbers 0 · schema 0 · provenance_cols 0 · content 0 · unit 0 · controls 0 · env 0 · stale 0 ·
#      provenance 0 (dirty 면 안 된다 — 산출 root 자체는 무관하다; U18-02 뒤로 시작 provenance 도 $OUT 을 안다) · inputs 0 ·
#      **inputs_uncomparable 과 env_uncomparable 만 > 0** (둘 다 옛 정본의 나이다 — U18 실측 17 · 1, 후자는 ne_shape 정본에 env 가 없다)
#    out/ 을 이미 덮었으면 정본을 git 에서 읽는다 (손으로 `git show` 를 엮지 말 것 — `--name-only` 는 트리가 아니다):
#      python3 scripts/check_u14.py --new out --old-rev <재실행 커밋>^
#    ★ 1 이면 그것이 발견이다. 계산 경로는 안 고쳤으니 같아야 한다. 출력과 함께 이것도 붙여 줘:
python3 -c "import json;print(json.load(open('out_u18b/matrix_100.csv.meta.json'))['env'])"

# ── 3b. U14-01 뒷수습 (2026-09-12 실행에서 드러남) — 줄끝 때문에 서명이 깨진 산출을 다시 서명 ──────
#    writer 가 CRLF 를 썼고 git 은 LF 로 저장한다 → fresh clone 에서 meta 의 sha256 이 안 맞고, reader(F07)가
#    그 상태를 표에서 뺀다. 지금 코드는 LF 로 쓰지만 **이미 게시된 것**은 이 명령으로. 기록된 해시가 지금
#    bytes 의 줄끝 변형과 맞을 때만 다시 서명하고(=내용이 같다는 증명), 아니면 손대지 않는다.
python3 scripts/check_u14.py --new out --renormalize

# ── 4. 승격 — 위 조건을 다 만족했을 때만. 옛 정본은 **보존**한다 (Codex R13 조건 7: "기존 provenance-incomplete
#      out/ 는 보존하고 별도 출력에 실제 재실행") — git 이력만이 아니라 트리 안 archive 로. 새 묶음이 out/ 을 대신한다
#      (도구 기본값 `out/` 은 그대로). 이 절차는 `promotion_eligible` 이 아니라 3 단계 출력을 붙인 커밋 메시지가 근거다.
mkdir -p out/archive/legacy_r6_u14
git mv out/*.csv out/*.json out/archive/legacy_r6_u14/          # 13 산출 + sidecar (meta.json 도 *.json 에 든다)
mv out_u18b/*.csv out_u18b/*.json out/                          # 새 정본 (ne_shape_GITT_Li.csv + meta 포함 — 끝의 shape_step 이 만든 것)
ls out_u18b/                                                    # 로그만 남아야 한다; 로그는 ~/out_u18b.log 와 함께 커밋하지 않는다
#    ⚠ archive 는 **자기 문서를 갖는다** (`out/archive/README.md` — 왜 얼어붙었는지). 새 식구를 그 표에 적지 않으면
#      다음 사람은 legacy_r6_u14/ 가 무엇인지 모른다. 같은 커밋에 넣는다:
python3 - <<'PYARCH'
import pathlib
p = pathlib.Path("out/archive/README.md"); s = p.read_text(encoding="utf-8")
row = ("| `legacy_r6_u14/` (26 파일) | **U18 승격 전의 정본** — 게시·서명 계약이 R13 이전이라 receipt·env·argv·roster 가 없다 "
       "(`check_u14 --new out --schema-only` 가 rc 2 로 말하던 그 묶음). U18b 재실행이 **같은 숫자**를 새 계약으로 다시 서명해 "
       "정본이 됐고, 이것은 조건 7 의 보존 요구(\"기존 provenance-incomplete out/ 는 보존\")대로 얼려 둔다 | "
       "`R13_RESPONSE.md` §8 · `WORKING_STATE.md` U18 런북 |\n")
i = s.index("\n\n## 왜 여기로 왔나")
s = s[:i] + "\n" + row.rstrip("\n") + s[i:]
p.write_text(s, encoding="utf-8"); print("archive README 갱신")
PYARCH
python3 scripts/check_u14.py --new out --schema-only            # ★ 계약 위반 0 이어야 한다 — degeneracy digest 4 도 shape 4 도
#      사라지고 provenance 도 0 이다 (U18-02 고침) → **rc 0** 이 기대값이다 (schema-only 는 baseline_absent 만 남는다)
python3 scripts/check_u14.py --new out --old-rev HEAD           # 정본(git) 대 새 out/: 3 단계와 같은 판정이어야 한다
python3 scripts/compare_states.py out                           # §1-10 표 재생 — '묶음 불일치' 경고가 없어야 한다
git add out/ out/archive/README.md
git commit -m "U18b — 새 게시·서명 스키마로 네 상태 + shape 재실행 (숫자 동일; 옛 정본은 out/archive/legacy_r6_u14/)"
git push -u origin claude/bms-alpha-beta-verify
#    커밋 메시지 본문에 3 단계의 PROMOTION 줄을 그대로 붙인다 (승격의 근거는 그것이다).

# ── 5. ~~MATLAB 한 줄씩~~ → **닫힘 (U15, 2026-09-11)**: 둘 다 Python 과 일치 ────────────────────
#      sprintf('%.2f', 0.125)  → '0.12'                    (half-to-even, Python 과 같다)
#      sprintf('%.17g', 1e-5)  → '1.0000000000000001e-05'  (2 자리 지수, 원래 double 로 복원)
#    기준선은 tests/test_r6_internal.py 의 MATLAB_SPRINTF 에 고정. 다른 MATLAB 판·플랫폼의 산출을 댈 때는 다시 잰다.
```
줄마다 `equiv=1` 이면 그 build 에서 scale 이 원본 설명식과 상대 1e-9 안에서 같다 (유한 · 예외 없음 · eps_rel ≤ 1e-9).
`degeneracy`/`profile`/`matrix` 를 다시 돌릴 때는 `run_states.sh` 가 이제 id 를 **필드로** 확인하고 meta 를 잠금
안에서 재확인해 bytes 해시와 함께 쓴다 (R5-04 · R5-08). matrix 행에 target/ref scale·감사가 실린다 (R5-07).

## 직전 상태 — Codex R4 (닫힘, `reviews/R4_LEDGER.md`)

2026-09-11 Codex 4차 리뷰(대상 `39a5fe0`) 일곱 건을 전부 재현·닫았다. U12 실측(사용자 기계, 274f1f8):
4 루트 × 4 상태 16 build 전부 Inf 0 · NaN 0 (`out/scale_audit_eval.txt`) — 그 증거 수준은 R5-09 로 "보고 순서의
16 줄(식별자 없음)" 로 한정했고, 동치 조건에 eps_rel 이 빠져 있던 것은 R5-06 으로 정정했다.

## 직전 상태 — Codex R3 (닫힘, `reviews/R3_LEDGER.md`)

2026-09-11 Codex 3차 리뷰(대상 `a432d23`) 아홉 건을 전부 재현·닫았다. 사용자 기계 실측(`ne_shape.py`
재실행, fb62342)으로 §5-2 (d) 표를 채웠다 — 100·200 은 (a) 진폭을 내는 합법 γ 가 있고(줄이는 쪽),
300_0009 는 합법 최대 86.01 mV < 119.34 mV 로 없다 (정규화·모양 한정어). 그 meta 의 `git_dirty: true`
로 자체 발견 S-01(산출물 재작성이 플래그를 켬)을 잡아 닫았다.

## 직전 상태 — Codex R2 (닫힘, `reviews/R2_LEDGER.md`)

2026-09-11 Codex 2차 리뷰(P1 9 · P2 1)와 내부 리뷰 L2·L5 를 합친 20 항목이
`reviews/R2_LEDGER.md` 에 있고, **닫는 순서**가 거기 적혀 있다. 여기서는 되풀이하지
않는다 — 그 파일의 "닫는 순서" 1~7 을 위에서부터 진행하고, 끝난 항목은 그 표의
"상태" 열을 갱신한다.

가장 아픈 셋: (C1) 대조 실험이 LAM_PE 쪽에서는 원통형 패턴을 **재현**한다 — "대체는
원인이 아니다" 는 LLI 에만 성립 · (C2) 측정 음극은 목적함수가 **소비하지 않는다** —
"35.77 mV 를 지웠는데도" 강도 논증 무효 · (C3·C4) MATLAB 대조기가 비교 안 한 값도
"전부 일치" 로 찍는다 — 192 값 대조를 고친 비교기로 **다시 돌려야** 한다.

Codex 반례 재생: `python3 reviews/r2_repros/harness_r2_replay.py --target $(pwd) --output /tmp/r.json`.

**2026-09-11 저녁 기준 — 원장 20 항목 중 코드·문서 쪽은 닫혔다 (a8084ec, 이 커밋).**
남은 것은 사용자 기계에서 몇 분이면 되는 실측 셋과, 그 뒤 R3 요청문이다:

```bash
cd ~/dd/bms-balancing && git pull --rebase origin claude/bms-alpha-beta-verify
source .venv/bin/activate && export BMS_DATA_ROOT='/mnt/d/가형 관련/degradation mode'
# ① PE 축 개입 강도 (§1-12 조건 7) — 초 단위
python3 scripts/ne_shape.py
# ② interp 가드가 실데이터에서 켜지는가 (L0-7) — 각 수 초. 에러가 나면 그 자체가 발견이다
python3 -m bms_balancing.verify eval --state 100 --si-source Li
BMS_DATA_ROOT=~/dd/cells/c168 python3 -m bms_balancing.verify eval --state 100 --si-source Li
BMS_DATA_ROOT=~/dd/cells/c171 python3 -m bms_balancing.verify eval --state 100 --si-source Li
BMS_DATA_ROOT=~/dd/cells/pouch_fixedhc python3 -m bms_balancing.verify eval --state 100 --si-source Li
git add out/ne_shape_GITT_Li.csv* && git commit -m "ne_shape 재실행 — PE 축 변화량 추가" && git push
```
그 결과로 §1-12 조건 7 을 채우고(PE 강도), 가드가 켜졌으면 원통형 산출을 재검토한다.

## 닫힌 것

| | 어디 | 한 줄 |
|---|---|---|
| 포팅 forward model | §1-0 · §1-8 | MATLAB↔Python 192 값, 최대 4.04e-12 |
| 툴박스 vs 우리 shim | §1-7 | `rmse_dqdv` 1.78e-12 — `sgolayfilt` 에서 생겨 dQ/dV 가 증폭 |
| 최적화 절차 | §1-9 | 자유 조합 최대 0.17 %p. 갈린 두 점에서 이긴 건 **그들** |
| 97 행 원표 | §2 · §2-1 | `out/bms97/` 커밋. 음수 LAM 이 경계 산물이라는 것을 **산술로** |
| 상태 일반화 | §1-10 | 파우치 네 상태에서 LAM_NE 최광 · LLI 최협 (4/4). **절대 폭으로 말할 때만** |
| **셀 일반화** | **§1-12** | **넘어가지 않는다** — 기술적 결과만. 원통형 LLI 하한 폭이 raw 로 max/max 10.5 배; 파우치 PE 고정 실험은 그 폭을 만들지 않았으나 LAM_PE 에서는 원통형 패턴을 재현 (R2 정정). 외곽 범위는 원통형에서 LAM_PE 분리·LAM_NE·LLI 겹침 (공유 가능값 미확정). 잔차 증가는 관측, 원인 미확정 (R3-01) |
| 문서↔산출 정합 | `cb23dbf` | 여섯 문서 중 넷이 뒤처져 있었다. drift 테스트 둘로 고정 |

## 열려 있는 것 (셀 말고)

- ~~dQ/dV 항의 로컬 함수 둘은 전사다 … 규진팀이 눈으로 맞춰 주면 닫힌다~~ → **닫힘**
  (U1, §1-13): 사용자가 원본을 직접 열어 네 로컬 함수 전부를 줄 단위로 댔다 — 일치
  (lower_half_mean 은 빈-표본 가드만 다름).
- **pOCV 가 원자료인지 필터본인지 모른다** (U2). 한 곡선으로는 원리적으로 못 가른다
  (§`verify noise`). 두 해석을 다 적어 뒀다. 이제 원자료를 우리가 갖고 있으므로 워크북의
  간격 균일성 검사로 닫을 수 있다 (사용자 기계, 선택).
- **γ 직접 적합(표현력)·공유 가능값 증인** (U9) — 미구현. 새 모델 요구서의 구분 시험 항목.
- **held-out 예측 없음.** 다른 셀의 **독립** 반쪽전지가 있어야 한다.
- **`CODEX_REVIEW_REQUEST.md` 2차 판을 아직 안 썼다.** 1차 판은 배너로
  인용 금지를 박아 뒀고 상한 자리마다 `→` 갱신을 달았다. 셀 축이 닫히면 새로 쓴다.

## 기계 쪽 사실 (잊기 쉬운 것)

- 작업본은 **`~/dd/bms-balancing`** (브랜치 `claude/bms-alpha-beta-verify`).
  `~/bms/bms-balancing` 은 본체 브랜치 체크아웃이니 **건드리지 않는다.**
  ⚠ **2026-09-15 흡수 뒤에는 반대다** — 본진 체크아웃(`~/bms`)에서 고치고, `~/dd`
  의 서브 브랜치에는 새 커밋을 얹지 않는다. 사용자 기계에서 `~/dd` 를 계속 쓰려면
  그 clone 을 본진 브랜치로 옮기면 된다 (`git checkout claude/14-gate-code-review-9qkx05`).
- `BMS_DATA_ROOT='/mnt/d/가형 관련/degradation mode'` — 원자료는 저장소에 안 넣는다.
- MATLAB 은 `cd 'D:\가형 관련\degradation mode'` → `addpath('dd_shims','-end')`
  → `dd_verify('check')`. `-end` 없으면 진짜 툴박스 함수까지 가린다.
- 툴박스는 2026-09-10 에 전부 깔렸다. "없어서 못 한다" 는 더 이상 사유가 아니다.
- ⚠ **그 기계의 clone 루트는 `~/dd` 다.** 그래서 `~/dd/cells/` 가 **저장소 안**에
  있고, 그 안에는 규진팀 원자료 xlsx 사본이 들어간다. 저장소는 public 이다.
  `.git/info/exclude` 에 `cells/` 를 넣어 막아 뒀지만 그건 그 clone 에만
  적용된다. 루트 `.gitignore` 는 본체 소유라 못 고쳤고 `HANDOFF_TO_GATE.md`
  §2b 에 신고했다. **루트에서 `git add -A` 를 치지 않는다.**
- ⚠ **테스트는 전역을 되돌려 놓아야 한다** (W-07, 2026-09-14). `tests/test_review_findings.py::test_r5_08` 이
  `pytest.MonkeyPatch()` 손잡이를 버려 `verify.minimize`·`multistart`·`build` 패치가 **세션 끝까지 남았다**.
  알파벳 순으로 뒤 파일(`tests/test_widths.py`)의 세 건이 그걸 뒤집어써서 **단독 실행은 통과, 전체 실행은 실패**
  했다. 고쳤고 `tests/conftest.py` 의 autouse 가드가 재발을 막는다 (누출한 **범인** 테스트가 빨개진다).
- ⚠ **2026-09-14: `webapp/` 를 이 브랜치가 고쳤다** — 하드룰 1 의 경계를 넘은
  유일한 자리다 (사용자 직접 지시: 지금까지 이룬 것을 화면에 정리 · 협업 방향
  화면 제거). `/handover` → `/bms`, 새 템플릿 `webapp/templates/bms.html`.
  경위·충돌 위험·본체 선택지는 `HANDOFF_TO_GATE.md` §2c. **이 컨테이너에
  Flask 가 없어 화면을 띄워 본 것은 아니다** — 구문·배선·CSS 클래스까지만 확인했다.
