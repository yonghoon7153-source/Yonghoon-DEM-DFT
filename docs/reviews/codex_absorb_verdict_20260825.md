# Codex 흡수 리뷰 판정 — S1 `b306fac1` (2026-08-25)

**판정: 흡수 HOLD.**  단위 정리와 PTFE requested/applied 분리는 방향이 맞지만, S1 이 막으려는
false-green 을 **실제 실행 경로에서 여전히 만들 수 있다**.  Codex 가 mutant 로 독립 재현했고,
아래 ★ 표시는 claude 가 **직접 재현 확인**한 것이다.

| 항목 | 판정 | 요지 |
|---|---|---|
| R-1 `check_arm` 대체 | **HOLD** | defense-in-depth 로는 유용하나 producer fail-closed 를 **대체할 수 없다** |
| R-2 봉인/판정 분리 | **HOLD** ★ | 현재 CLI·러너는 blind seal 이 아니다 |
| ⑤ 단일 validator | **HOLD** | 같은-directory 일부만 공유.  cross-dir·bed·generation 은 갈라져 있다 |
| 소급 HOLD | **부분 타당** | 새 세대·CL-58 이온은 타당, legacy 전자 일괄 차단은 과하다 |
| exact-zero | **의도 타당, 생산 사용 HOLD** | plate 가 PTFE 를 **관통**하는 결함부터 |
| 회귀 판별력 | **부분 통과** | production-shaped 우회와 "테스트가 CI 에서 안 도는" 경우를 놓친다 |
| CDXR2-1 | **S1 에 포함** | Q7 기전 해석에 그 진단이 필요하다 |
| Q7 factorial | **정량·부호 모두 provisional** | 한 칸의 arm-0 편향으로 네 칸 상쇄를 가정할 수 없다 |

## 차단 사유 (독립)

1. ★ `--seal-only` 전에 결과가 노출되고, **옵션 조합으로 봉인 자체를 우회**할 수 있다
2. `check_arm` 은 producer nonzero exit 를 대체하지 못한다 — 부분·누락 실패, 모순된 CG 상태,
   실제 component backend 불일치를 통과시킨다
3. 러너가 요청한 PTFE mode 와 payload 의 applied mode 를 **end-to-end 로 대조하지 않는다**
4. ★ ionic seal 이 `cg_info != 0` ∧ `unconverged=False` 의 **모순**을 초록으로 통과시킨다
5. exact-zero 가 **표면 절연체를 건너 더 깊은 도체를 전극에 직접 연결**하는 기존 plate 결함을 노출한다
6. ★ `ARMS` 가 preregistered 8-arm 계약이 아니라 **런타임에서 자기 자신을 정답으로 정의**한다

## Codex 가 재현한 mutant (전부 통과 = false-green)

| mutant | 결과 |
|---|---|
| `manifest.status=partial` + electronic component `missing` | `check_arm`=None, 8팔 최종 봉인도 **통과** |
| `cg_info=99` + `unconverged=False` | `check_arm`=None |
| backend metadata 누락 | `check_arm`=None (expect 검사가 `got` 비면 통과) |
| electronic=cpu, last-solve=gpu, expect=gpu | `check_arm`=None, 16팔 봉인 **통과** |
| cross-dir `sigma_am_s_S_cm` 0.010→0.020 | `decision=measured` |
| cross-dir `ptfe_stamp`·`ptfe_zero_dof` 양쪽 삭제 | `decision=measured` |
| top PTFE column fixture | 더 깊은 도체가 plate contact=true |
| `ARMS=2` 정상 fixture | exit 0, `봉인: 통과` |

## 흡수 전 최소 종료 조건 (10)

1. blind contract seal **또는** immutable actual verdict 중 하나를 택하고, raw 결과·ratio
   역산·옵션 충돌을 막는 **CLI integration test** ★ (2026-08-25 `abe03766` 에서 닫음)
2. **producer required failure 의 nonzero exit 복구** + `check_arm` 을 aggregate/component/
   CG/residual/backend/finite-result 검사로 강화
3. canonical `physics_protocol_id` 와 expected applied config 를 runner·generated script·
   fresh/cache 검사·final seal 에 **end-to-end** 로 묶기
4. run mode 에서 required components 파생 (LEAN=0/1 ionic · production digest · per-component backend)
5. ionic convergence 쌍의 누락·모순·residual fail-closed ★ (`abe03766`)
6. **두 conductivity solver에서 occupied-surface-first plate 접촉**으로 바꾸고 PTFE blocker/
   pore-gap 회귀 통과
7. production 은 `ARMS == 8` 만 허용, diagnostic 을 별도 namespace·비-production 상태로 ★ (`abe03766`)
8. **declarative field registry 하나**에서 same-dir·cross-dir·allowed-axis·required-since·
   legacy adapter 검사를 생성
9. CDXR2-1 에 plate dissipation 포함 + **finite-difference identity test**.  미루면 phase-share
   출력을 S1 에서 **사용 금지**
10. 새 CLI·runner·schema·solver selftest 를 `check_all.sh` 와 CI 에 **실제 배선**하고 각 test 가
    한 번 이상 실행됐음을 CI 로그에서 확인

## Codex 가 고친 우리 서술

★ **CDXR2-1 의 bias 방향을 고정할 수 없다.**  원장이 "plate 누락 때문에 SDCP 1 % 가 **과소**"
라고 적었는데, 현 함수는 포함한 내부 에너지끼리 **다시 정규화**하므로 plate 에너지의 phase 별
비중에 따라 SDCP share 는 **올라갈 수도 내려갈 수도** 있다.  SDCP 가 plate 에 전혀 닿지 않으면
분모가 커져 진짜 share 는 현재 1 % 보다 **작다**.  ⇒ 올바른 상태는 **항등식 불성립, bias 방향 미정**.

★ 반례: 3-cell 직렬 A,B,B (σ=1,10) 에서 plate 포함 로그미분 share 는 `(5/6, 1/6)` 인데
현 internal-only 진단은 `(10/13, 3/13)` 이다.  **합은 양쪽 다 1** 이라 `sum==1` 검사로는 못 잡는다
→ centered-log finite difference 가 필수.

★ **Q7 "부호·순서는 유효" 도 아직 강하다.**  factorial 에서 상쇄되려면 origin effect 가
조건에 독립인 additive common mode 여야 하는데, stamp·phase σ·plate contact 는 전도 경로를
**비선형**으로 바꾼다.  관측된 arm-0 보정량 **+0.007528** 이 기존 interaction **−0.0085** 와
**같은 차수**라 interaction 의 부호도 안정적이라고 할 수 없다.
⇒ `+0.13`·`+0.07` 은 **provisional direction** 으로만 적고 순서·크기를 주장하지 않는다.

## Codex 검토 한계 (자기 신고)

· Q7 raw 8팔 payload 를 받지 않아 통계를 원자료에서 재계산하지 않았다
· GPU backend 의 실제 수치·성능은 검증하지 않았다
· 판정은 `b306fac1` zip 에 한정 — 이후 커밋이 고쳤다고 간주하지 않았다
· 로컬에 SciPy 가 없어 payload temperature path 를 포함한 full suite 는 독립 완주하지 못했다

## 진행 (claude)

| 조건 | 상태 | 커밋 |
|---|---|---|
| 1 · 5 · 7 | ✅ 봉인/판정 분리 · 이온 conjunction · ARMS 상수 8 | `abe03766` |
| 2 | ✅ producer exit 3 · 원자적 쓰기 · check_arm 5종 강화 | `1c12e322` |
| **3 · 4** | ✅ `physics_protocol_id` end-to-end (exit 4 · EXPECT_PROTOCOL) | `6d933923` |
| **6** | ✅ occupied-surface-first plate (두 솔버) | `b5598999` |
| **8** | ✅ FIELD_CONTRACT 레지스트리 (scope·across_dir·required) | `10bdb1ae` |
| **9** | ✅ plate 소산 포함 + FD 항등식 (차 1.5e-10) | `4860eb24` |
| **10** | ✅ 규칙 K — selftest 배선 강제 | `e882ec95` |

**10/10 완료.**  selftest: verdict **100** · sr01 **68** · discipline **59** · step3(+7) · payload.
⚠ 그러나 **흡수는 재리뷰 뒤**다 — Codex 가 *"이 조건을 충족한 수정 diff를 다시 보면 된다"*
라고 했고, 이 세션의 증거가 그것을 뒷받침한다: 내 자기검증이 **이 부류에서** 두 번 틀렸다
(누설 없음을 주장하며 누설 · R-1 이 덮는다고 했으나 안 덮음).  둘 다 내 selftest 는 초록이었다.

⚠⚠ **1차 리뷰 때 없던 것이 생겼다** — CDXR3-6 이 **σ_e 값을 바꾼다**.  게이트 수정이 아니라
**과학적 결과**이고, 특히 *비(ratio)가 공통모드로 살아남는지*는 **미측정**이다.

⚠ **GPU 8팔 재실행도 보류**다 — Codex: *"plate/contact 및 protocol seal 이 고정되기 전에
돌리면 계산비를 쓰고도 어느 물리·실행 계약을 측정했는지 다시 모호해진다."*

---

# 2차 재리뷰 (Codex, 2026-08-25) — **여전히 HOLD**

10/10 을 닫은 diff 를 다시 먹였더니 **새 mutant 16개**와 **새 최소 조건 8개**가 나왔다.
이것 자체가 이 세션의 교훈이다 — *"조건을 닫았다"* 는 **내 판단**이고, 그것을 근거로
흡수하면 같은 부류가 또 들어간다.

## 최소 종료 조건 (8) — 진행

| # | 조건 | 상태 | 커밋 |
|---|---|---|---|
| 1 | 봉인이 눈먼가: producer raw 로그·collect 를 봉인 뒤로 · 네 모드 CLI 배타 | ✅ | `d8d134a0` · `3e3cf2cb` |
| 2 | **게시 전 검증** · LEAN 의 disabled component · required 계획 | ✅ | `d8d134a0` |
| 3 | 수렴 계약 통일(`0 ≤ resid ≤ 1e-6`) + authoritative backend | ✅ | `d8d134a0` |
| 4 | 규약 기대값을 **러너 자기 설정**에서 계산 · `periodic_xy`·component 계획·plate 규칙판·관측 sid7 수 추가 | ✅ | `3e3cf2cb` |
| 5 | `verdict` 와 `compare_dirs` 가 **하나의** `validate_contract` 를 공유 · `required_since` | ✅ | `0db71bf9` |
| 6 | plate 회귀: 아래판 분기 · 반응 솔버 · 비단위 vox FD · plate 원장 없으면 fail-closed | ✅ | `c89ea13b` |
| 7 | 규칙 J 가 **정확히 exit 3** + 인과 코드 · 규칙 K 가 주석/echo/죽은 줄 거부 · 러너 통합 selftest | ✅ | `79165db0` |
| 8 | 각 수정의 **단일-되돌림** 검증 · SciPy 환경에서 full suite | ✅ | `b167edd2` |

## 자체발견 (재리뷰 조건 밖) — SELF-01

조건 2 의 게시-전-검증을 **실측으로** 확인하다가 (`--expect-protocol` 불일치 → exit 4)
로그에 `적용 unknown:vox_um` 이 찍혔다.  `PROTOCOL_FIELDS` 가 요구하는 `vox_um` 을
producer 의 매니페스트 리터럴이 **안 쓰고 있었다**.

· 영향 = **거짓 초록이 아니라 생산 과잉차단**.  판정기의 `PROTOCOL_UNKNOWN` 이
  fail-closed 라 현행 payload 로 도는 팔이 **전부 HOLD** 된다.
· `temp_c`(M-R3-02) · `thermal`(M-R3-03) 과 **같은 부류** — 내가 넣은 게이트가 생산을 막았다.
  이 부류만 세 번째다.
· 왜 안 잡혔나 = 규칙 J 가 매니페스트의 고정 인자는 봤지만 `physics_protocol_id`
  **자신은 한 번도 안 봤다**.
· 고침 = 값을 적고, 규칙 J 가 id 의 `p1-` 접두사를 요구한다.  `unknown:` 뒤에 빠진 필드
  이름이 실려 있으므로 한 줄이 이 부류를 전부 잡는다.  **필드 목록을 검사기에 다시 적지
  않는다** (backend·bridge_um 두 사고의 원인).
· 돌연변이 1:1 확인 — 매니페스트의 그 한 줄만 지우면 `J_PROTOCOL| … ('unknown:vox_um')`.

## 조건 1·4 를 닫으며 (2026-08-25)

**조건 1 의 남은 절반** — 러너가 `--collect-only` 로 **16 팔 σ_e 원값 표**를 찍은
**뒤에** 봉인을 걸고 있었다.  그러면 운영자가 결과를 다 보고 나서 봉인을 통과시킬지
고를 수 있다 = 눈먼 봉인이 아니다 (사전등록의 요점이 정확히 그것이다).
⇒ 순서를 뒤집었다.  봉인 통과 시에는 원값을 **안 찍고** 명령만 알려 주고, 봉인 실패
시에만 찍는다 (이미 기각된 데이터라 창을 옮길 여지가 없고, 진단에는 원값이 필요하다).
규칙 L 의 `L_SEALORDER` 가 이 순서를 강제한다 (음성 대조 L-7).

**조건 4** 는 두 조각이었다.

· **기대값을 첫 팔에서 읽지 않는다.**  `EXPECT_PROTOCOL` 의 표준 용법이 "첫 팔이 찍은
  id 를 나머지 일곱에 넘기기" 였는데, 그러면 **첫 팔이 진리를 정의한다** — 첫 팔이
  조용히 잘못된 규약으로 돌면 나머지가 그것에 일치해 전부 통과한다.  팔간 일치는
  옳음이 아니다.  ⇒ `--expect-physics KEY=VAL,…` 신설.  러너가 **자기가 인자로 넘긴
  축**만 선언하고 payload 가 적용값과 **필드별로** 대조한다 (해시가 아니라 필드라서
  어느 축이 갈렸는지도 말해 준다).  킷이 정하는 σ_AM·온도는 러너가 모르므로 선언하지
  않는다 — 모르는 것을 선언하면 그것이 새 거짓 보증이다.

· **네 필드 추가.**  `periodic_xy` 와 `plate_rule` 은 `PROTOCOL_FIELDS` 에 들어간다
  (물리 축이므로 갈리면 다른 실험이다).  ★ `plate_rule` 이 특히 중요하다 — CDXR3-6 이
  플레이트 결합 규칙을 바꿔 **σ_e 절대값이 달라졌으므로**, 옛 판 산출물과 새 판
  산출물은 같은 침대·같은 vox 라도 섞으면 안 된다.  `component_plan` 은 무엇을 돌리기로
  **했는지**(요청)를 남겨 `disabled` 가 "의도적으로 껐다" 인지 "조용히 죽었다" 인지
  가른다 (M-R3-03 이 정확히 그 혼동이었다).  `ptfe_cells_observed` 는 스탬프 **도장**과
  실제 효과를 가르는 유일한 증거다 (`centerline` 이라 적혀 있어도 0 셀이면 아무 일도
  안 났다).
  ⚠ 축을 늘리면 **모든 `physics_protocol_id` 가 바뀐다**.  그것이 의도다.

**신설 규칙 L** — 러너 배선을 **실행으로** 확인한다 (조건 7 에서 만들고 여기서 확장).
`RUNNER_CONFIG_END` 위쪽만 잘라 서브셸에서 돌리고, `--extra-flags` 리터럴은 러너에서
떼어 셸에 전개시킨다.  음성 대조 L-2~L-9.  ★ L-3·L-8 이 이 규칙의 존재 이유다 —
`$EP_FLAG`/`$XP_FLAG` 를 **인자열에서만** 빼면 변수는 그대로 있고 쓰이지 않을 뿐이라
grep 으로는 안 보인다.

## 조건 8 — 단일 되돌림 배터리 (2026-08-25)

`scripts/mutation_sweep_20260825.py` — 각 수정에 대해 **그 하나만** 옛 코드로 되돌린
사본을 만들고 대응 selftest 가 빨간불을 내는지 본다.  통과하는 회귀는 인증되지 않은
회귀다.  이 환경은 SciPy 1.17.1 · NumPy 2.4.6 이라 full suite 가 완주한다
(Codex 가 자기 신고한 한계 — 로컬에 SciPy 가 없어 못 돌린 것 — 이 여기서 해소된다).

| 돌연변이 | 결과 | 적발 회귀 |
|---|---|---|
| 조건5 `compare_dirs` 계약 제거 | 적발 | ㊳a 외 9건 — HOLD 가 **`measured`** 로 돌아간다 |
| 조건5 `where` 접두사 제거 | 적발 | ㊳a′ 외 5건 |
| 조건3 전자 수렴 게이트 제거 | 적발 | ㊳c 외 3건 |
| 조건3 resid 문턱 제거 | 적발 | ㉟h 외 8건 |
| 조건4 `periodic_xy` 규약축 제거 | 적발 | ㊴a 외 3건 |
| 조건6 아래판 occupied-first 되돌림 | 적발 | `plate-blocker-bottom` (σ 0 → **0.01**) |
| 조건6 반응 솔버 되돌림 | 적발 | `plate-blocker-rxn` (reason → `None`) |
| 조건6 plate 소산 vox 인자 제거 | 적발 | `plate-share-identity-vox` (0.8333 → **0.7850**) |
| 조건6 원장 fail-open 되돌림 | 적발 | `plate-share-failclosed` |
| 조건7 규칙 K 옛 부분문자열 | 적발 | K-7 외 2건 |
| SELF-01 `vox_um` 매니페스트 제거 | 적발 | J-1(J_PROTOCOL) 외 2건 |
| 조건2 게시-전-검증 되돌림 | 적발 | J-1(J_PUBLISHED·J_NODIAG) 외 2건 |

**놓친 돌연변이: 없음.**

⚠⚠ **초판 스윕은 하나를 놓쳤다** — 「조건7 규칙 K 옛 부분문자열」.  K-5/K-6 이
`k_live_invocation()` 을 **직접** 부르기 때문에, **호출부**가 옛 부분문자열 검사로
되돌아가도 둘 다 초록이었다.  helper 를 시험하는 것과 **검사기를 시험하는 것**은
다르다.  ⇒ K-7 신설: 죽은 줄만 남은 `check_all.sh` 사본을 만들어
`check_selftest_wiring` **자신**을 돌린다.
★ 이것이 조건 8 이 존재하는 이유 그 자체다 — 돌연변이 배터리가 없었으면 이 구멍은
**규칙 K 를 하드닝하는 커밋 안에** 그대로 남았을 것이다.

---

# 3차 재리뷰 (Codex, 2026-08-25) — **NO-GO / HOLD** → 9건 대응

Codex 판정: *"현재 snapshot 은 두 상태를 동시에 가진다 — 정상 producer payload 를
검사기가 못 읽어 **생산이 항상 막히는 false-red**, 그리고 그 한 줄을 고치면 곧바로
활성화되는 **false-green 여럿**."*  그 진단이 정확했다.

## R3-CX-01~09 대응

| # | 요지 | 커밋 |
|---|---|---|
| 01 | `check_arm` 이 `metrics` 오타로 **모든 실제 팔을 거부** (생산 전면 차단) | `79888279` |
| 02 | 봉인 전에 producer stdout 이 σ 를 노출 · 실패 후 raw 덤프 | `4cc032e1` |
| 03 | 규약 id 가 canonical identity 가 아니라 신뢰된 문자열 | `79888279` |
| 04 | `component_plan`·`ptfe_cells_observed` 가 미사용 metadata | `79888279` |
| 05 | 수치·backend validator 가 권위적이지 않음 | `79888279` |
| 06 | `FIELD_CONTRACT` 가 single source 가 아니고 양방향 오류 | `575a64f6` |
| 07 | plate 회귀 사각지대 4종 | `a99dd42e` |
| 08 | J/K/L·배터리가 "의도한 실패" 를 보증하지 않음 | `4cc032e1` · `a0a351d3` |
| 09 | 진단 런이 생산 이름공간을 쓸 수 있었다 | `4cc032e1` |

## 이 라운드가 남긴 것 (방법론)

★★★ **픽스처가 버그를 인코딩하면 selftest 는 그 버그를 지킨다.**  R3-CX-01 이 가장 순수한
사례다 — 소비자의 자리 목록이 `metrics` 오타였고, **픽스처도 같은 오타**를 썼기 때문에
75/75 가 초록인 채로 `check_arm` 이 실제 팔을 전부 거부했다.  손으로 만든 payload 는
producer 를 증명하지 못한다.  ⇒ `producer → check_arm → move` 통합 회귀(J_ARMCHK).

★★★ **계약 사본은 반드시 갈라진다.**  자리·수렴·backend·required·규약 정의가 세 파일에
따로 있었고 **넷 다** 조금씩 달랐다.  ⇒ `scripts/run_contract.py` 하나로 모으고 producer 와
두 소비자가 같은 함수를 부른다.

★★★ **선언은 거동이 아니다.**  `required`/`across_dir`/`generation` 을 뒤집어도 selftest 가
초록이었다 — 선언만 있고 시험되지 않았기 때문이다.  ⇒ 레지스트리를 **읽어 시험을 생성**하고,
선언을 뒤집는 mutant 는 선언과 **무관한** 불변식으로 잡는다.

★★★ **배터리도 검사 대상이다.**  엄격하게 만든 **첫 실행에서 harness 자신의
false-negative** 가 드러났다 (`_parse` 가 step3 표기를 못 읽어 실제로는 잡고 있던 두 건을
"회귀 없음" 으로 보고).  그리고 진짜 구멍 둘을 더 잡았다 — `[0] is False` 만 보던 시험이
다른 검사가 대신 물어 초록이던 것, faithful 하지 않던 mutant.

★ **생산 과잉차단이 이 라운드에만 두 번 더 났다** (`collector_geom` 도장 결손 · `vox_um`
누락).  둘 다 규칙 J 가 잡았다.  검사기를 느슨하게 하는 대신 **producer 의 기록 결손**을
고치는 것이 매번 옳은 방향이었다.

## 남은 것 (Codex 가 흡수 차단으로 세지 않은 항목)

· partial-volume/cut-cell PTFE 표현 · 독립 침대 seed (paired 5–8)
· `σ_SDCP = 250` 출처 (cast film ↔ pressed pellet) — **사용자 미회신**
· `ρ_SDCP` 확인 (코드 주석이 PROXY 라고 적고 원고 값을 요구한다)

## GPU 8팔 재실행 — 여전히 보류

Codex 조건: R3-CX-01~08 을 닫은 뒤, **하나의 새 protocol 스키마 · 하나의 clean code SHA ·
raw manifest 재계산을 통과한 receipt · input digest + required component/backend/convergence
seal · bed × origin × side × phase 별 p1→p2 접촉 수 census** 를 갖춰 돌린다.
옛 팔과 새 팔은 섞지 않는다 — 그리고 이제 `plate_rule` 이 규약 해시에 들어가 그 금지가
**기계로 집행된다** (옛 팔은 `p1-`, 새 팔은 `p2-`).

---

# 4차 독립 재리뷰 (Codex, 2026-08-25) — **NO-GO** → 9건 대응

Codex 판정의 핵심 문장: *"이번 22-mutant 영수증은 '그 22개가 그 실행에서 기대 prefix 를
냈다' 는 증거로는 유효할 수 있지만, **R3-CX-02~06/08 이 닫혔거나 새 8팔을 안전하게 봉인할
수 있다는 증거는 아니다.**"*  맞다.  Codex 는 실제 producer payload 를 8×2 로 확장해
`collect()` 의 **진짜 `_read()` 경로**로 재현했고, 내 회귀는 그 경로를 안 탔다.

| # | 요지 | 커밋 |
|---|---|---|
| 01 | `ideal_R0` 라는 **다른 이름으로 σ_e 노출** (대수적으로 같은 수) | `c0ac0ad8` |
| 02 | plan·PTFE·PNM·비전자 수치가 fail-open — 실제-read 16팔이 **전부 h0** | `c0ac0ad8` |
| 03 | argparse **축약**으로 금지 목록 우회 · 숨은 env · hash 밖 축 | `c0ac0ad8` |
| 04 | backend 가 `requested` 로 **실제 사용값을 위장** | `c0ac0ad8` |
| 05 | 타입을 **강제**해 `bool("false") == True` | `c0ac0ad8` |
| 06 | K 가 `true \|\|`·`\|\| echo`·`; true`·`\| tee`·`exit 0;`·`&` 를 live 로 셈 | `c0ac0ad8` |
| 07 | 반응 솔버 두 분기가 회귀 봉인 **밖** (구현은 옳으나 증인이 없다) | `c0ac0ad8` |
| 08 | 진단 namespace 접미사가 **문자열** — junction/symlink 우회 | `c0ac0ad8` |
| 09 | (=08 의 bundle 항목) 리뷰 bundle 이 base 를 안 실어 단독 재현 불가 | 다음 패키지 |

## 이 라운드의 교훈

★★★ **이름을 바꾼 것은 가린 것이 아니다.**  `ideal_R0` 는 `L/(R_bulk+0)` 이고
`R_bulk = L/σ_e` 이므로 **σ_e 그 자체**다.  세 자리까지 그대로 찍히고 있었다.
⇒ 회귀를 **값 기반**으로 바꿨다 — payload 에서 결과값을 뽑아 stdout 을 훑는다.
이름 목록을 손으로 유지하는 방식은 다음 파생값에서 또 진다.

★★★ **"없으면 건너뛴다" 는 삭제로 무력화된다.**  `component_plan` 을 지우면 required 를
파생할 수 없어 검사가 통째로 꺼졌고, `ptfe_cells_observed` 를 지우면 `== 0` 검사가 안 돌았다.
⇒ **부재 자체가 위반**이어야 한다.  단, 소급 필수화는 과잉차단이므로 `schema_version`
세대 어댑터를 뒀다 (옛 세대는 옛 계약, **모르는 세대는 HOLD**).

★★★ **강제(coercion)는 기록을 바꾸는 것이다.**  `bool("false") == True` 라 리더의
`bool(...)` 이 JSON 문자열을 뒤집었다.  ⇒ 강제하지 않고 **거부**한다.

★★ **배터리를 강화하니 자기 구멍 셋이 더 나왔다** — 엄격 타입·계획 스키마·PTFE 기록
검사를 각각 꺼도 rc=0 이었다 (**다른 게이트가 대신 물어** 그 검사가 인증되지 않았다).
⇒ 그 검사만 물 수 있는 입력으로 ㊸a/b/c 를 세웠다.  R3 의 `B2` 와 같은 부류가 이번엔 셋.

★ **생산 과잉차단이 또 났다** (6번째) — `not_solvable` 을 `failed` 와 같이 취급했더니
full-component 팔이 exit 3.  SE 비퍼콜은 **정상 물리 결과**다.  매번 그렇듯, 검사기를
느슨하게 하는 대신 의미를 갈랐다.

★ **검사기의 sed 범위가 낡아 대상 밖으로 나가 있었다** — 규칙 L 의 P2_EXTRA probe 가
`sed -n "1,140p"` 라 러너가 길어지자 그 블록을 못 봤다.  표지 기준으로 바꿨다.

## 아직 못 한 것

· solver-affecting CLI **전수**를 parser 에서 생성해 schema 등재를 검사 (R4-CX-03 잔여)
· cross-dir raw diff-set 을 `expect_differ` 와 **정확히** 일치시키기 (R4-CX-05 잔여)
· `backend.across_dir` 류 **선언 뒤집기** pass-mutant (R4-CX-05 잔여)
· selftest 를 구조화 결과(JSON/JUnit)로 내고 harness 가 exact ID multiset 을 검증 (R4-CX-06 잔여)
· standalone full bundle (R4-CX-08 잔여)
· `σ_SDCP = 250` 출처 · `ρ_SDCP` — **사용자 회신 대기**

## Q1 재확인 (Codex 와 같은 결론)

CL-33/41/58 의 절대 σ_e 는 현재 규약의 과학값으로 인용 불가 — 역사 기록이면
`legacy conductive-surface tunnelling protocol` 이라고 명시한다.  ratio 의 공통모드
상쇄는 **보장되지 않는다** (`κ_DBE = κ_SBE` 의 근거가 없다).  합성 census 의
bottom −28.7 % · top −32.8 % 는 **합성 침대의 접촉 기둥 수**이지 실침대 σ 감소율이 아니다.
어느 면이 지배하는지도 실침대에서 따로 세기 전에는 말할 수 없다.

**흡수·GPU 재실행 모두 HOLD 유지.**
