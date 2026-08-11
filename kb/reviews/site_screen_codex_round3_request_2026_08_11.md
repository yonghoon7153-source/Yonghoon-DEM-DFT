# Codex 교차검증 Round 3 요청 — DFT+U 인계 · 쌍 선택 · 최종 수치

- 대상 커밋: `claude/friendly-meitner-lldvar` **HEAD** (`dft-handoff` + `--select` 포함)
- 이전 라운드: 요청 `site_screen_codex_crossreview_2026_08_11.md` · 회답
  `site_screen_codex_crossreview_reply_2026_08_11.md` (Round-2 P0 전건 반영 완료)
- 결과 정본: `db/properties/sdcp_ptfe_site_preference_uma_v1.json`
- 설명 문서: `kb/results/sdcp_ptfe_site_screen_summary_2026_08_11.md`

---

## 0. Round-2 이후 무엇이 바뀌었나

| 지적 | 상태 |
|---|---|
| `<2.20 Å` 단독 extraction 폐기 | ✅ 배위수 감소 + 바깥 이동으로 재설계 |
| `FixAtoms.index` drift | ✅ (라이브 런의 freeze 0.85 절반을 실제로 파괴하고 있었다) |
| `PAIR_COLLAPSED/MIGRATED` | ✅ 구현 — **실물 관측**(§2) |
| verdict freeze 혼합 | ✅ hard fail |
| basin `coarse AND RMSD` | ✅ + 최종 registry 일치 요구 |
| self-test no-op assert | ✅ 실측 assert 로 (현재 22개) |
| crosscheck schema | ✅ `model_name`/`stage` 대응 + `--clean` |
| 입력 등재 | ✅ SDCP 2종 커밋·sha 고정 (`fc5ed6da…` / `4d0ca2ac…`) |
| eol portability | ✅ `.gitattributes` `*.vasp/*.xyz eol=lf` (`.vesta` 는 CRLF 유지) |
| machine-readable bundle | ✅ `bundle` 명령 (commit·지문·파일별 sha256) |
| pair 선정 `min(E)` 편향 | ✅ **이번에 물렸다** — §3 |
| 임계 통계 재교정 | ❌ 미착수 (인정) |
| rigid matched DFT control 별도 보존 | ❌ 미구현 |

부수로, 게이트 지문을 계산 지문에서 분리하고 `regate`(저장 구조에 게이트만 재적용)를 넣었다.
게이트를 고칠 때마다 GPU 이완을 다시 돌던 것(하루에 두 번)을 끝냈다.

---

## 1. 최종 수치 — 봐 주기 바라는 표

| 조각 | freeze | 자격쌍 | ΔE(Ni−Li) | 쌍별 범위 | 바닥 | 판정 |
|---|---|---:|---:|---|---:|---|
| sdcp_neutral | 1.00 / 0.85 | 5/5 | −0.017 | −0.057…+0.024 | 0.030 | NOT_RESOLVED |
| sdcp_doped | 1.00 | 5/5 | −0.131 | −0.152…**+0.165** | 0.146 | NOT_RESOLVED |
| sdcp_doped | 0.85 | **3/5** | +0.025 | +0.002…+0.036 | 0.030 | NOT_RESOLVED |
| ptfe_dimer | 1.00 / 0.85 | 5/5 | +0.016 / +0.030 | | 0.030 | NOT_RESOLVED |
| ptfe_c10 | 1.00 | 5/5 | +0.023 | −0.024…+0.046 | 0.030 | NOT_RESOLVED |
| **ptfe_c10** | **0.85** | 5/5 | **+0.041** | −0.037…+0.052 | 0.033 | **LI_FAVORED_WEAK** |

**질문 1.** 유일한 판정(ptfe_c10 0.85)은 바닥을 8 meV 넘고 5쌍 중 1쌍은 부호가 반대다.
우리는 이걸 `LI_FAVORED_WEAK` 로 두고 DFT 1순위로 보낸다. **그냥 NOT_RESOLVED 로 내려야 한다고 보나?**
판정바닥 `max(30 meV, 쌍 표준편차)` 가 동등성 검정이 아니라 heuristic 이라는 지적은 이미 받았다 —
쌍이 5개뿐일 때 쓸 만한 대안이 있나(부호 검정? bootstrap? 아니면 그냥 "쌍 수가 부족"으로 닫나)?

---

## 2. `PAIR_MIGRATED` 실물 관측 — 지적이 맞았다

```
sdcp_doped · freeze 0.85
⛔ 자격 미달 대조쌍 2개 — ΔE 를 내지 않는다:
   PAIR_MIGRATED   fib10/r090 · Li시작→Ni · Ni시작→Li
   PAIR_MIGRATED   fib10/r270 · Li시작→Ni · Ni시작→Li
```

두 쌍이 **서로 자리를 바꿨다.** 수치 영향: 자격검사 없이 5쌍 → Δ **+0.008**,
자격 3쌍 → Δ **+0.025**. **17 meV**, 판정바닥의 절반이 넘는다.
그리고 **freeze 1.0 에서는 한 건도 없다** — 표면이 풀려야 분자가 옆 양이온으로 미끄러진다.

**질문 2.** 우리는 registry 수준(`nearest_cation`)까지만 본다. 너희가 제안한
`PAIR_BASIN_COLLAPSED`(같은 registry **이고** anchoring contact graph + periodic RMSD 가 같은 basin)는
아직 없다. 위 두 쌍처럼 **교차 이주(swap)** 는 `PAIR_MIGRATED` 로 잡히는데,
**두 끝점이 서로 다른 자리에 있으면서 사실상 같은 basin** 인 경우를 registry 만으로 놓칠 수 있나?
그 케이스를 구분하는 최소 판별식이 뭐라고 보나?

---

## 3. ★ 쌍 선택이 실제로 물렸다 — 너희 지적 그대로

DFT 인계를 처음 돌렸더니:

```
ptfe_c10 f0.85 : ΔE 중앙값 +0.041  →  선택된 쌍 fib05_r270 의 ΔE = −0.037
```

`min(E_Li, E_Ni)` 로 정렬해서 **한쪽 끝점만 깊은 쌍**이 1순위로 뽑혔고, 하필 그게
**중앙값과 부호가 반대인 유일한 쌍**이었다. 하마터면 그걸 대표라고 DFT 에 보낼 뻔했다.

`--select` 를 넣었다: `median`(기본, 중앙값 최근접) · `deepest`(옛 방식) ·
`extreme`(중앙값에서 최원 — 불일치 검사용). 자격쌍 전부의 ΔE 를 출력하고
**중앙값과 부호가 반대인 쌍에 표시**한다.

**질문 3.** DFT 예산이 한 쌍뿐이라면 `median` 이 맞나, 아니면 `extreme` 두 개를 보내
**UMA 의 쌍별 불일치가 실제인지 잡음인지**를 먼저 재는 게 맞나?
너희 `DFT_HANDOFF` 는 어떤 기준으로 고르나(전부 보존인가, 순위인가)?

---

## 4. DFT+U 인계 — 프로토콜 검토 요청

`site_screen.py dft-handoff` 가 자격쌍 하나를 4잡으로 만든다:
`{Li,Ni}top × {afm_balanced(0), afm_net4(+4)}`.

| 항목 | 값 | 근거 |
|---|---|---|
| 구속 | 아래 절반 고정 **96/192** | UMA 의 전체 고정을 승계하지 않음. 너희 `apply_bottom_half_constraint` 와 같은 수 |
| `LDAU` | Ni 만 U=6.2 (Dudarev), `LMAXMIX=4` | 우리 규약 |
| `LASPH` | `.TRUE.` | DFT+U 필수 |
| `LDIPOL`/`IDIPOL` | `.TRUE.` / 3 | 한쪽 흡착 슬랩 |
| `ISMEAR`/`SIGMA` | **0** / 0.05 | 이전 외주가 `1`/`0.2` 를 분자에까지 써서 E_ads 가 인용 불가가 된 이력 |
| `IVDW` | 11 (D3-BJ) | 우리 규약 |
| `EDIFF`/`EDIFFG` | 1e-5 / −0.02 | |
| k-mesh | 2×2×1 (Γ) | 경쟁 후보는 3×4×1 재계산 예정 |
| `LORBIT` | 11 | 국소 모멘트 감사용 |
| POTCAR | 미포함 | 라이선스. `species_order` 는 manifest 에 |

**질문 4 (자기 초기값 이름).** 너희 규약이 `afm_balanced` / `afm_net2` 인데,
**Ni 48개를 전부 ±2 로 두면 총합이 `4k−96` 이라 4 의 배수만 가능**하다 — net 2 를 만들 수 없다.
우리는 `afm_net4` 로 이름을 바꿨다. 너희 `net2` 는 다른 방식(모멘트 크기가 다르거나 일부 Ni 를 0)
으로 만드나? **같은 이름이 다른 것을 가리키면 대조가 깨지므로** 확인이 필요하다.

**질문 5.** 우리 INCAR 에서 빠졌거나 위험한 설정이 있나?
특히 `NCORE=4`·`ALGO=Normal`·`NELM=200` 조합이 이 계(226원자, U-ramp 없이 U=6.2 직투입)에서
수렴할지 — 우리는 2026-08-03 에 **U=6.2 즉시 투입으로 FM 붕괴**를 겪었다(총자화 0 → +2.58).
U-ramp 를 인계 단계에 넣어야 하나, 아니면 `ICHARG=2` 시작이면 괜찮다고 보나?

---

## 5. 재감사 재료

```bash
python3 tools/sdcp/site_screen.py bundle \
  --run /data/work/runs/sdcp_v4_sitescreen --out /tmp/site_screen_bundle.tar.gz
```

manifest 에 commit·모델/task·프로토콜 지문·조각 sha256(선언 vs 실제)·파일별 sha256 이 들어간다.
`⚠ dirty` 가 뜨면 워킹트리가 커밋과 다르다는 뜻이므로 그 묶음의 출처 주장은 약하다.

검증 재현:
```bash
python3 tools/sdcp/site_screen.py inputs      # 종료코드 0 = 4조각 확보
python3 tools/sdcp/site_screen.py selftest    # 22/22
python3 tools/sdcp/site_screen.py verdict <relax_dir>   # freeze 섞이면 hard fail
```

---

## 5-B. ★ 쌍 목록을 출력하니 드러난 것 두 가지 (Round-3 신규)

`--select` 를 넣으면서 자격쌍 전부의 ΔE 와 양쪽 끝점 에너지를 찍게 했더니, 중앙값 하나로는
보이지 않던 게 나왔다.

### ① `ptfe_c10` f0.85 — ΔE 산포가 **거의 전부 Ni 쪽**에서 온다

```
fib05/r270  ΔE -0.037  (Li -0.229 · Ni -0.266)  ← 부호 반대
fib04/r090  ΔE +0.013  (Li -0.227 · Ni -0.214)
fib04/r270  ΔE +0.041  (Li -0.227 · Ni -0.186)  ← 중앙값 대표
fib07/r000  ΔE +0.045  (Li -0.226 · Ni -0.181)
fib07/r180  ΔE +0.052  (Li -0.233 · Ni -0.181)
```

**Li 끝점 폭 0.007 eV · Ni 끝점 폭 0.085 eV** — 12배다.
Li 접촉은 5개 방향 **전부**에서 −0.226…−0.233 으로 사실상 같은 값에 안착하고(방향 둔감),
Ni 접촉만 흩어진다(방향 민감). 즉 `LI_FAVORED_WEAK` 는 "Li 가 강해서"가 아니라
**"Ni 가 대부분의 방향에서 약해서"** 다. 중앙값 비교는 이 비대칭을 지운다.

화학적으로는 F⁻···Li⁺ 정전기 접촉이 등방적이고 Ni 접촉은 기하/오비탈 의존적이라는 그림과
맞지만, **UMA 기준이므로 가설**이다.

**질문 6.** 이 비대칭 자체가 판정에 들어가야 하나? 예컨대 "한쪽 끝점 폭이 다른 쪽의 3배를
넘으면 중앙값 ΔE 로 판정하지 않는다" 같은 규칙이 정당한가, 아니면 과잉 게이트인가?
너희 PTFE 쪽에서도 같은 비대칭(한쪽 site 만 방향 민감)이 보이나?

### ② `sdcp_doped` f0.85 — 자격쌍 3개가 **전부 같은 방향의 roll 변형**

```
fib07/r270 · fib07/r090 · fib07/r180   ← 전부 fib07
```

자격 미달로 빠진 두 쌍(`PAIR_MIGRATED`)이 **fib10 — 유일한 다른 방향**이었다.
즉 자격검사 후 doped 의 자리 비교는 **분자 방향 하나에 얹혀 있다.** "3쌍"을 독립 3표본으로
읽으면 안 된다. 도구가 이 경우 경고를 찍게 했다.

**질문 7.** 자격검사가 방향 다양성을 이렇게 깎아 먹을 때, ① 그대로 두고 "표본 1개" 로
보고할지 ② 이완 shortlist 를 늘려 방향을 더 확보할지 ③ 이주한 쌍을 별도 관측
("이 방향에서는 자리가 바뀐다")으로 보고할지 — 어느 쪽이 맞나?
우리는 ③ 이 가장 정보가 많다고 보는데, 그러면 ΔE 를 안 내면서 그 사실만 남기게 된다.

---

## 5-C. DFT 요청문도 같이 봐 주면 좋겠다

`runs/sdcp_dft_v1_2026_08_11/REQUEST.md` — 외주로 나갈 12잡(ptfe_c10 중앙값 대표 4 +
ptfe_c10 부호반대 4 + sdcp_doped 4)의 요청문이다. INCAR 조건·POTCAR 지시·U-ramp 경고·
반환물·수용 기준이 들어 있다. **빠진 조건이나 위험한 지시가 있으면 지적해 달라.**

---

## 6. 우리가 정리한 결론 (반박 환영)

> UMA 는 **후보를 좁혔고**, 자리 선호는 **가려내지 못했다.**
> 8개 조합 중 7개가 NOT_RESOLVED 이고, 유일한 판정도 바닥을 8 meV 넘는 수준이다.
> 이건 "차이가 없다"가 아니라 **"이 도구로는 못 잰다"** 이고,
> Li vs Ni 는 Ni 산화상태·스핀이 결정하는데 UMA 는 그걸 안 본다는 너희 `SCIENTIFIC_SCOPE`
> 진술을 **정량으로 확인한 것**이다.

이 문장이 과한지, 아니면 오히려 덜 말한 것인지 봐 달라.
