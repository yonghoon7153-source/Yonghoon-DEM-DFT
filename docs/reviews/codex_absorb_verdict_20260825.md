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
| 8 | 각 수정의 **단일-되돌림** 검증 · SciPy 환경에서 full suite | ✅ | `<P8>` |

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
