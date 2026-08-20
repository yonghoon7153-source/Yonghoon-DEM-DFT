# 22p 민감도 다리 인벤토리 — 단계 C (저비용 재분석)

작성: 2026-08-20 · 20차 게이트 리뷰 발견 9·10·14 대응의 **선행 단계**.
근거: 커밋된 `docs/22p_gap/*.txt` 69개 전수 파싱 + git 객체 대조.
**RUN_SCOPE 를 건드리지 않았다** — 파서는 스크래치패드에서 돌렸고 이 문서만
커밋한다. 영구 `leg_index.yaml` 생성기는 단계 B 에서 `tools/` 안에 만든다.

리뷰어 권고("새 계산 전에 기존 계산의 저비용 재분석부터")를 그대로 수행한 결과,
**재분석의 전제 자체가 성립하지 않는다**는 것이 먼저 드러났다. 아래 §1 이 그
내용이고, §2 가 그럼에도 커밋된 자료만으로 얻은 새 결과다.

---

## 1. 원시 fit 이 저장소에 없다 — 재분석 불가

> **⚠ 2차 갱신으로 부분 정정 (아래 §6~§10).** "이 저장소·이 컨테이너에 없다" 는
> 그대로 참이지만, **사용자 로컬에는 73개 디렉터리(1.9 GB)가 살아 있다.**
> 따라서 아래 "불가능" 목록은 *이 실행 환경에서* 불가능하다는 뜻이고, 로컬에서는
> 전부 실행 가능하다.

리뷰어 발견 9 는 "seed 202~606 의 noise 0.005 결과를 새 계산 없이 집계할 수
있는지 먼저 확인하라" 였다. 확인 결과:

| 확인 | 결과 |
|---|---|
| `results/` 의 다리 디렉터리 | `grid_curves_v4` `grid_fit_v4` `halfcell_fit_v4` `paired_fixed5_v4` **4개뿐** |
| `results/` 에 22p·bias 다리 | **0개** |
| `artifacts/artifact_index.yaml` 의 run | 위 4개뿐 — 22p 계열 **0개** |
| git 이력에 22p·bias artifact 가 커밋된 적 | **없음** (`--diff-filter=A` 전수 대조) |
| `fits.parquet` 보유 디렉터리 | v4 계열 + `grid_fine_v1/v2` + `halfcell_v1` 뿐 |

즉 **ocpbias 민감도 연구 전체가 커밋된 69개 `.txt` 로만 존재한다.** 원시
`fits.parquet` 이 없으므로 다음이 전부 불가능하다:

- 다른 `noise` 층으로 재집계 (`analyze_22p_gap.py --noise`)
- 다른 `tol`·`radius`·`--gap-bin` 으로 재판정
- 발견 14 가 요구하는 "봉인 fits 에서 재생성 후 diff"
- 발견 10 의 `leg_index.yaml` 을 **소급** 검증

> `results/` 는 `.gitignore:2` 로 추적 밖이고 이 컨테이너는 fresh clone 이다.
> **사용자의 로컬 머신·V100 에는 남아 있을 수 있다** — 이 문서의 주장은
> "이 저장소와 이 실행 환경에 없다" 까지다. 남아 있다면 §4 의 재분석 목록이
> 그대로 실행 가능해진다.

이것이 리뷰어 Q3 의 "Git 밖에서 실행하고 아무 정본도 커밋하지 않은 run 은
Git-object test 가 원천적으로 볼 수 없다" 는 관측 경계의 **실제 사례**다.

## 2. 그럼에도 나온 새 결과 — 22p 정확좌표의 잡음 층 (6격자 × 3오프셋)

블록 ③ 은 22p 정확좌표(0.13, 0.13, 0.17)를 **전 noise 층**으로 출력한다.
seed 격자 6개 × PE 오프셋 3종 = 18개 다리에서 이것을 추출하면 36개 관측이
나온다. 참 격차는 0 이므로 복원 격차 ≥ 2%p 이면 거짓 분리다.

**복원 격차 (%p) — 참 격차 0, 판정선 2%p**

| 오프셋 | noise | 101 | 202 | 303 | 404 | 505 | 606 | 거짓 분리 |
|---|---|---|---|---|---|---|---|---|
| 2 mV | 0 | 0.3 | 0.1 | 0.5 | 0.1 | 0.1 | 0.2 | **0/6** |
| 2 mV | 0.005 | 0.0 | 0.6 | 0.2 | 1.1 | 0.7 | 0.9 | **0/6** |
| 5 mV | 0 | 0.8 | 0.8 | 0.8 | 2.1 | 0.8 | 0.8 | **1/6** |
| 5 mV | 0.005 | 2.3 | 0.8 | 1.1 | 3.1 | 0.8 | 0.6 | **2/6** |
| 10 mV | 0 | 3.5 | 3.5 | 3.3 | 3.4 | 3.5 | 3.3 | **6/6** |
| 10 mV | 0.005 | 3.4 | 0.9 | 1.7 | 4.2 | 1.6 | 0.8 | **2/6** |

읽을 수 있는 것:

1. **2 mV 는 6격자 · 두 잡음 층에서 전부 무해하다** (0/6, 0/6). §7.10 이
   철회한 "2 mV 상전이" 가 폐기 다리의 산물이었다는 판정을 독립적으로
   뒷받침한다 — 건강한 격자 어디에서도 2 mV 는 아무 일도 하지 않는다.
2. **10 mV 는 noise 0 에서 6/6 으로 완전히 무너진다.** 이 다리들이 §7.10 의
   "전이는 5~10 mV 사이" 를 떠받치는 근거다.
3. **그런데 noise 0.005 에서는 같은 10 mV 가 2/6 로 떨어진다.** 잡음이 결과를
   **좋게** 만든 것처럼 보인다.

3번은 그대로 인용하면 안 된다. `noise_seed` 가 잡음 실현과 optimizer restart
draw 를 **동시에** 바꾸므로(리뷰 발견 4), 이 차이를 잡음의 인과효과로 읽을 수
없다. 말할 수 있는 것은 **"10 mV 파탄은 잡음 층에서 재현되지 않는다 —
따라서 5~10 mV 전이 주장은 noise 0 층에 조건부다"** 까지다.

이는 §8 한계 4 의 "seed_101 에서 noise 0/0.005 를 봤고 문턱은 불변" 과
어긋나지 않는다 — seed_101 만 보면 3.5 → 3.4 로 실제 불변이다. **한 격자로
일반화한 것이 문제였다.** 6격자로 넓히자 문턱은 잡음 층에서 불변이 아니다.

각 칸은 조건 1개의 단일 draw 다. 6격자는 독립 반복이지만 조건은 하나이므로,
이 표는 **22p 정확좌표에 한정**되고 근방 집계(①')로 확장되지 않는다.

## 3. 다리 구성 — 축이 심하게 치우쳐 있다

`bias_*.txt` 32개의 축 분포:

| 축 | 다리 수 | 격자 |
|---|---|---|
| PE OCP 오프셋 | **28** | dense 11 · seed_101 6 · seed_202~606 각 3 |
| NE OCP 오프셋 | **1** | dense (+2 mV) |
| PE stretch | **1** | dense (0.95) |
| NE stretch | **1** | dense (0.95, 원점 경계해) |
| PE+NE 동시 | **1** | dense (+2 mV) |

리뷰어의 "각 축 한 점씩이라 축의 모양을 모른다" 가 정확하다. PE 축에 28개가
몰려 있고 나머지 네 축은 **각각 단일 관측**이다. 축 순위를 세울 수 없었던
구조적 이유이기도 하다 (§7.10 철회[AXIS_RANK]).

## 4. code identity — 69개 중 42개가 불일치 경고를 달고 있다

`source_digest` 5종이 등장한다. git 객체에서 각 digest 를 재현해 커밋에
매핑했다 (RUN_SCOPE 만 `git archive` 로 추출 → `source_digest(root=...)`):

| digest | 커밋 | 무엇 |
|---|---|---|
| `8fe84240ad351594` | `a9469aab` (08-18) | seed 스윕·잡음층·bin 폭 + 격자 config |
| `c894eb1205dd62d5` | `8bd15bfa` (08-19) | OCP 오차 민감도 §7.10 초판 |
| `7250c6e689399381` | `9b8825d4` | half-cell 조밀·잡음 다리 완주 |
| `d842894dbbc2a0f9` | `58f53bb4` (08-19) | §7.10 재작성 (배선 수정 6건 **포함** 이후) |
| `a72c0f3a485c19bb` | `f53df360` (현재) | 20차 리뷰 대응 |

**seed 다리 18개는 전부 같은 쌍(`8fe84240`, `d842894`)을 쓴다.** 격자 간 비교가
코드 축에서 정합하다는 뜻이라 §2 의 표는 그 점에서는 문제없다.

그러나 두 커밋 사이 `src/` 는 **비어 있지 않다**:

```
src/fitting.py   +89
src/halfcell.py  +144
src/hessian.py   +37
src/io.py        +28
```

그리고 `a9469aab`(08-18)은 `42b8b5c2`(ocpbias 자체 리뷰 CONFIRMED 6건, 08-19)
**이전**이다 — 즉 "왜곡 실행이 조용히 무왜곡이 되는 경로" 가 아직 열려 있던
코드 상태다.

### 4.1 그런데 어느 digest 가 왜곡 다리인지 알 수 없다 — 새 발견

> **⚠ §6 에서 해소됨.** 로컬 manifest 실측으로 짝이 확정됐다 — 배선 수정 이전
> 코드로 돈 것은 **무왜곡 기준 다리**뿐이다. 아래는 그 판정에 이른 경위로 남긴다.
> 도구 수정(다리별 digest 출력)은 여전히 필요하다.

`tools/analyze_22p_gap.py:291` 이 경고를 이렇게 만든다:

```python
digests = {v for v in identity.values() if v}      # ← set
print("\n⚠ 두 다리의 code identity(source_digest) 가 다릅니다: " ...)
```

**`set` 이라 출력 순서가 비결정적이다.** 따라서 커밋된 txt 만으로는
`8fe84240`(배선 수정 이전)이 **기준 다리**의 것인지 **왜곡 다리**의 것인지
판정할 수 없다.

- 기준 다리(`fit_22p_seed_NNN`, 무왜곡)의 것이라면 무해하다 — 왜곡이 없으므로
  배선 수정과 무관하다. 정황은 이쪽이다: seed 격자 config 가 `a9469aab` 에서
  들어왔고, bias 정본은 `cc6b36d2`(08-19, 수정 이후)에 커밋됐다.
- 왜곡 다리의 것이라면 **그 다리는 왜곡이 fit 에 도달하지 않았을 수 있다** —
  민감도 0 을 조용히 보고하는 바로 그 실패 모드다.

정황은 전자를 가리키지만 **artifact 로 증명되지 않는다.** 이것이 리뷰어
발견 10(다리별 manifest)이 필요한 이유의 구체적 실례다. 단계 B 에서 두 가지를
같이 고친다:

1. 경고를 다리별로 출력한다 — `{leg_dir: digest}` 를 정렬해 찍는다 (한 줄 수정).
2. `leg_index.yaml` 에 다리마다 `source_digest` 를 기록한다.

## 5. 이 문서가 남기는 판정

| 항목 | 상태 |
|---|---|
| §2 의 6격자 잡음 표 | **인용 가능** — 단, 22p 정확좌표 한정, 잡음 인과는 미분리 |
| "2 mV 무해" | **강화됨** — 6격자 × 2잡음층 전부 0/6 |
| "전이 5~10 mV" | **noise 0 층에 조건부** 로 좁혀야 한다 |
| §8 한계 4 "잡음 층 문턱 불변" | **한 격자 일반화였다** — 6격자에서는 불변이 아니다 |
| 축 순위 | 세울 수 없다 — 네 축이 각각 단일 관측 |
| 원시 fits 기반 재분석 | **이 환경에서 불가** (§1). 로컬에 남아 있으면 가능 |
| 왜곡 다리의 code identity | **해소** (§6) — 인용된 왜곡 다리는 전부 배선 수정 이후 |
| 원시 fits 기반 재분석 (로컬) | **가능** — §10 의 두 항목이 새 fitting 없이 닫힌다 |

---

# 2차 갱신 (2026-08-20) — 로컬 원자료 73개 디렉터리 실측

`docs/22p_gap/leg_probe.py` 를 원자료가 있는 머신에서 실행한 결과. §1 의
"이 환경에 없다" 는 유지되지만, **사용자 로컬에는 살아 있다** (`results/` 1.9 GB,
73개 디렉터리). 아래는 그 manifest 실측이다.

## 6. 발견 4.1 해소 — 왜곡 다리는 전부 배선 수정 이후 코드다

§4.1 이 남긴 미결("어느 digest 가 왜곡 다리 것인지 알 수 없다")이 닫혔다.
다리별 `run_spec.source_digest` 를 직접 읽으니 짝이 확정된다:

| 다리 종류 | digest | 커밋 | 배선 수정(`42b8b5c2`) 기준 |
|---|---|---|---|
| grid 기준 (`fit_22p_seed_*`) | `8fe84240` | `a9469aab` | 이전 — **무왜곡이라 무관** |
| half-cell 기준 (`fit_22p_seed_*_hc`) | `7250c6e6` | `4001fa7b` | 무왜곡 |
| seed 왜곡 (`fit_seed*_pe*mv`, 18개) | `d842894` | `8ce869f0`·`1542688d` | **이후 ✓** |
| dense 왜곡 (`fit_dense_pe*mv` 등) | `c894eb12` | `1e67a82f`·`fb4a7718`·`b15502ce`·`0672c770` | **이후 ✓** |
| stretch (`fit_dense_pest095`) | `d842894` | `8ce869f0` | 이후 ✓ |
| stretch (`fit_dense_nest095`) | `a72c0f3a` | `b6369004` | 이후 ✓ |
| restart 20 (`fit_dense_pe2mv_r20`) | `a72c0f3a` | `cc6b36d2` | 이후 ✓ |

즉 seed 정본 txt 가 찍던 `8fe84240, d842894` 쌍은 **기준 다리 + 왜곡 다리**였고,
배선 수정 이전 코드로 돌아간 것은 무왜곡 기준 다리뿐이다. **인용된 왜곡 다리
중 배선 수정 이전 것은 없다.** §4.1 이 "정황은 무해, 증명은 없음" 으로 남긴
것을 artifact 로 확정했다.

계보는 `git merge-base --is-ancestor 42b8b5c2 <커밋>` 로 확인했다 (이력에 merge
가 있어 `git log` 순서로는 판정할 수 없다).

### 6.1 예외 하나 — `fit_dense_pe10mv_warm` 은 배선 수정 이전이다

| | |
|---|---|
| digest | `c2e7d8b9fd11b54e` |
| 커밋 | `29da46a3` |
| `42b8b5c2` 포함 | **아니오** |
| `99ce1267`·`2d38f384`·`13c37662` 포함 | 예 (ocpbias 구현 + 배선 2건은 있다) |
| 문서 인용 | **없음** |
| 정본 txt | **없음** |

갈라진 가지에서 돈 다리다. ocpbias 배선 자체는 있으나 13차 자체 리뷰가 닫은
6건이 빠져 있다. **어디에도 인용되지 않으므로 수치 영향은 없지만**, 조용히
버리면 안 된다 — `leg_index` 에 `excluded / code_identity_predates_fix` 로
기록한다.

## 7. 발견 3 확인 — "전부 restart 5" 는 사실이었다

문서 전체가 "이 문서의 모든 수치가 restart 5 산물" 이라는 가정 위에 서 있었다.
실측 결과 **가정이 맞다**: 73개 중 `n_restarts` 가 5 가 아닌 다리는
`fit_dense_pe2mv_r20`(20) **하나뿐**이다.

`fit_dense_pe2mv_r2` 는 이름과 달리 `n_restarts=5` 다 — **restart 2 가 아니라
재실행(re-run) 2회차**이고, `c894eb12` vs `d842894` 의 code identity 대조용이다
(§7.5 의 "dense +2 mV 재실행 대조" 가 이것). 이름이 오해를 부르므로
`leg_index` 에 목적을 명시한다.

다만 리뷰 발견 3 의 본체는 **여전히 열려 있다** — `n_restarts` 하나가 `p_ini`
최적화와 조건별 최적화 **양쪽**에 들어가고, adaptive early-stop 이 기본 on 이다.
"restart 5 였다" 가 "각 행이 5회를 다 돌았다" 를 뜻하지 않는다. 예산 분리는
단계 B 일감이다.

## 8. 승격 대상이 아닌 디렉터리 — 기록은 남긴다

| 디렉터리 | 상태 | 처리 |
|---|---|---|
| `fit_dense_off{0,5,10,20}_st{0.97,1.00}` (8개, 4 KB) | manifest·fits 없음 | `incomplete` — offset×stretch 2D 스윕 중단 흔적 |
| `fit_seed_pe{1,1p5,2}mv` (3개, 8 KB) | manifest·fits 없음 | `incomplete` |
| `_INVALID_paired_fixed5_v4_srcchanged` (45 MB) | fits 있음, 이름이 무효 표시 | `invalidated / src_changed` — fail-closed 가 실제로 작동한 증거 |
| `fit_22p_v1` · `grid_22p_v1` | 완결이나 정본 txt 없음 | `superseded` (v1 세대) |
| `grid_curves_v3` | 완결, v4 로 대체 | `superseded` |

`grid_22p_*` 와 `grid_curves_*` 에 `fits.parquet` 이 없는 것은 정상이다 —
곡선 생산자라 `curves.parquet` 을 갖는다. `source_digest` 가 `-` 로 나오는 것도
같은 이유다 (producer 는 `curves_manifest.yaml` 이 소유한다).

## 9. 추출기 결함 2건 — 발견하고 고쳤다

이 인벤토리를 만든 도구 자체가 두 번 틀렸다. 둘 다 **문서가 아니라 도구**의
결함이었으므로 기록해 둔다.

1. **무왜곡 판정이 축마다 다른 것을 무시했다.** 오프셋은 0 이 무왜곡이고
   stretch 는 1 이 무왜곡인데 둘 다 `(0, 1)` 로 걸렀다. 그 결과
   `fit_dense_pe1mv`(`pe_offset_mv = 1.0`)이 **"왜곡 없음"** 으로 찍혔다 —
   거짓 경보를 낼 뻔했다.
2. **`p_ini` 가 목적함수마다 다른 것(F26)을 무시했다.** dict 의 첫 항목을
   집었는데 그게 `pocv` 였고, 문서는 `pocv_dvdq_dqdv` 를 인용한다. 그래서
   `fit_dense_pe1p5mv` 가 **문서 1.0652 vs 도구 1.0274** 로 어긋나 보였다.
   같은 다리의 다른 목적함수 원점이었을 뿐 **문서는 옳다.**

   실측 예 (`halfcell_fit_v4`): `pocv=1.1216 · pocv_dvdq=1.0617 ·
   pocv_dvdq_dqdv=1.0626 · dqdv_only=1.0507`. 한 다리 안에서 원점이 이만큼
   갈린다 — "이 다리의 원점" 이라는 표현 자체가 목적함수를 밝히지 않으면
   모호하다.

고친 도구는 `pocv_dvdq_dqdv` 를 기본 열로 쓰고 나머지를 `a_ne_all` 로 병기한다.

## 10. 남은 구멍

- **seed 왜곡 다리 16개의 원점이 미검증이다.** `pini_all.txt` 는 12개 다리만
  담고 그중 seed 는 `fit_seed101_pe5mv`·`fit_seed101_pe10mv` 둘뿐이다.
  나머지 16개(seed 202~606 × 3오프셋 + seed101 pe2mv)는 원점 건강 여부가
  확인되지 않았다. §2 의 6격자 잡음 표가 이 다리들에 서 있으므로,
  원점 진단을 그 16개로 넓혀야 한다 — `diagnose_pini_transition.py` 를
  돌리면 되고 **새 fitting 이 필요 없다**.
- **`fit_22p_seed_404_hc` 가 다른 seed 기준 다리와 다르다.** 초판 도구
  (=`pocv` 축)에서 404 만 `1.0273` 이고 나머지 다섯은 `1.0617` 이었다.
  `pocv_dvdq_dqdv` 축에서도 그런지는 재실행해야 안다. **주목할 이유가 있다** —
  §2 잡음 표에서 404 가 유일한 이상치였다 (5 mV noise 0 에서 2.1, noise 0.005
  에서 3.1, 10 mV noise 0.005 에서 4.2). 원점 이상과 이상치가 같은 격자에서
  나온다면 우연이 아닐 수 있다.

---

# 3차 갱신 (2026-08-20) — seed 24다리 원점 진단

`tools/diagnose_pini_transition.py --objective pocv_dvdq_dqdv` 를 seed 대조 6 +
왜곡 18 = 24다리에 돌린 결과. **새 fitting 없음** — 기존 fit 을 읽기만 했다.
§10 의 두 구멍이 모두 닫혔다.

## 11. 원점은 왜곡을 따라 움직인다 — "원점이 다르다" 가 전부 교란은 아니다

Case 1 좌표 원점은 **왜곡된 half-cell** 에 맞춰 다시 잡힌다. 따라서 왜곡 수준이
다르면 원점이 다른 것이 정상이고, 그 자체가 왜곡이 작용하는 **경로**다:

| PE 오프셋 | 원점 `a_pe` 범위 | 거짓 분리 합 (①' n=8 × 6격자) |
|---|---|---|
| 0 mV | 1.5185 ~ 1.5191 | 1/48 |
| 2 mV | 1.5125 ~ 1.5151 | **0/48** |
| 5 mV | 1.5032 ~ 1.5206 | 6/48 |
| 10 mV | 1.4923 ~ 1.4953 | **32/48** |

교란이 되는 것은 **같은 왜곡 안에서 원점이 갈릴 때**다. 그것을 따로 본다.

## 12. 같은 왜곡 · 같은 원점이면 결과도 같다 — 5 mV 가 그것을 보여준다

| 왜곡 | 원점 종수 | 원점별 결과 |
|---|---|---|
| 0 mV | 3 | `a_pe 1.5191` → 101:0/8, 202:0/8, 505:0/8, **606:1/8** · `1.5187` → 303:0/8 · `1.5185` → 404:0/8 |
| 2 mV | 6 | 전부 다르지만 **전부 0/8** |
| **5 mV** | **2** | **`a_pe 1.5032` → 202·303·505·606 전부 0/8, 101 만 1/8** · **`a_pe 1.5206` → 404 만 5/8** |
| 10 mV | 4 | `1.4923` → 303:6/8, 606:6/8 · `1.4951` → 404:6/8, 505:5/8, 202:4/8 · `1.4953` → 101:5/8 |

**5 mV 가 가장 깨끗한 대조다.** 여섯 다리 중 **다섯이 원점을 소수점 4자리까지
공유**한다 (`[1.5032, -0.4203, 1.0693, -0.0661]`). 그 다섯 중 넷이 `0/8`, 하나가
`1/8` 이다. 유일하게 원점이 다른 seed_404 (`a_pe 1.5206`, `b_pe −0.4318`)만
`5/8` 로 무너진다.

주목할 것은 **404 의 원점이 왜곡 방향과 반대로 움직였다**는 점이다. 0 mV 대조가
`a_pe 1.5185` 인데, 다른 5 mV 다리는 전부 `1.5032` 로 **내려갔고** 404 만
`1.5206` 으로 **올라갔다**. 최적화가 다른 국소해에 앉은 것이다.

→ **5 mV 에서의 붕괴는 왜곡 크기가 아니라 원점 불안정의 산물이다.** 원점이
맞으면 5 mV 는 무해하다 (4/5 다리가 0/8).

10 mV 는 반대다 — 원점이 `1.4923~1.4953` 으로 좁게 모였는데도 **여섯 다리 전부**
4~6/8 로 무너진다. 원점이 맞아도 무너지므로 이쪽은 **왜곡 효과**로 읽을 수 있다.

## 13. ⚠ 2차 갱신 §2 의 6격자 잡음 표를 격하한다 — 자기 정정

§2 에서 저 표를 "**인용 가능** — 단, 22p 정확좌표 한정" 이라고 적었다.
**그 판정을 내린다.** 근거:

1. 5 mV 행의 여섯 다리는 **원점이 두 종류**다 (§12). 진단 도구 자신이
   `⚠ 원점이 여러 개다 … 그대로 문턱으로 인용하지 말 것` 을 출력한다.
   404 가 §2 표에서도 유일한 이상치였던 이유가 이것이다 — 잡음 seed 효과가
   아니라 좌표계 효과다.
2. §2 표의 **noise 0.005 열은 원점 진단이 아예 없다.** 진단은 noise 0 에서만
   돈다. 잡음 층의 원점이 어떤지 모르는 채로 6격자를 나란히 놓았다.

수정된 판정:

| §2 표의 행 | 상태 |
|---|---|
| 2 mV (0/6, 0/6) | **유지** — 원점이 갈려도 전 다리가 0 이라 결론이 원점에 의존하지 않는다 |
| 5 mV (1/6, 2/6) | **격하** — 원점 2종이 섞였다. 원점 맞춘 다섯만 보면 4/5 가 무해 |
| 10 mV noise 0 (6/6) | **유지** — 원점이 좁게 모였는데도 전부 무너진다 |
| 10 mV noise 0.005 (2/6) | **격하** — 잡음 층 원점 미진단. "잡음에서 재현 안 된다" 는 관측으로만 |

§7.10 본문도 같이 고쳤다.

## 14. 404 의 companion 목적함수 원점이 오염돼 있다 — 가설

`fit_22p_seed_404_hc` 의 원점을 목적함수별로 보면:

```
pocv_dvdq       a_ne = 1.0273     ← 여섯 격자 중 404 만 이 값
pocv_dvdq_dqdv  a_ne = 1.0633     ← 정상 (나머지 격자 1.0613~1.0633)
```

다른 다섯 격자는 `pocv_dvdq` 도 전부 `1.0617` 이다. 즉 **404 만 companion
목적함수의 원점이 오염 영역(≈1.03)에 있다.**

문서가 인용하는 축(`pocv_dvdq_dqdv`)은 정상이므로 §7.10 의 판정은 그대로다.
다만 이 실행은 `--objective pocv_dvdq,pocv_dvdq_dqdv` warm-start 연쇄이고,
warm start 는 앞 목적함수의 **해**를 뒤 목적함수의 초기값으로 넘긴다. 따라서
404 의 왜곡 다리들이 계속 이상한 국소해에 앉는 것과 연결될 수 있다.

**가설이지 증명이 아니다.** 확인하려면 404 를 `--no-warm-start` 로 다시 돌려
원점과 붕괴율이 다른 격자에 수렴하는지 보면 된다 (fitting 필요, 격자 1개분).

## 15. 이 갱신이 닫은 것

| §10 의 구멍 | 상태 |
|---|---|
| seed 왜곡 다리 16개 원점 미검증 | **닫힘** — 24다리 전부 진단. `a_ne` 는 전부 1.0582~1.0693 (오염 영역 ≈1.03 없음) |
| `fit_22p_seed_404_hc` 이상 | **닫힘** — 인용 축은 정상, 오염은 companion 축. §14 가설 |

---

# 16. 실행 지시 — §14 가설 검증 (404 warm-start)

**이 실행은 반드시 `source_digest = a72c0f3a485c19bb` 에서 해야 한다.** 단계 B
(코드 수정)가 들어가면 digest 가 바뀌어 기존 24다리와 나란히 놓을 수 없다.
→ **이 실행을 끝낸 뒤에 단계 B 를 pull 한다.**

## 무엇을 시험하나

§14 가설: `fit_22p_seed_404_hc` 의 companion 목적함수(`pocv_dvdq`) 원점이 홀로
오염(`a_ne` 1.0273, 다른 다섯 격자는 1.0617)돼 있고, warm start 가 앞 목적함수의
**해**를 뒤로 넘기므로 404 의 왜곡 다리들이 계속 이상한 국소해에 앉는다.

시험: **목적함수 집합은 그대로 두고 연쇄만 끊는다** (`--no-warm-start`).
단일 목적함수 실행으로 바꾸면 안 된다 — 13차 자체 리뷰가 그건 cold start 가 되어
민감도를 과소평가한다고 실측했다 (warm-start 축 교란).

## 명령 (인자 조립은 `RUN_SH_DRY=1` 로 검증했다)

```bash
cd ~/work/Yonghoon-DEM-DFT/degradation-degeneracy

# (1) 대조 — 무왜곡, 연쇄만 끊는다
./run.sh --mode fit --in results/grid_22p_seed_404 \
  --out results/fit_22p_seed_404_hc_nowarm --nproc 28 \
  --objective pocv_dvdq,pocv_dvdq_dqdv --n-restarts 5 \
  --reference halfcell --bounds halfcell --no-warm-start
./run.sh --mode score --in results/fit_22p_seed_404_hc_nowarm

# (2) 5 mV 왜곡 — 이상치가 나온 바로 그 다리
./run.sh --mode fit --in results/grid_22p_seed_404 \
  --out results/fit_seed404_pe5mv_nowarm --nproc 28 \
  --objective pocv_dvdq,pocv_dvdq_dqdv --n-restarts 5 \
  --reference halfcell --bounds halfcell \
  --halfcell-method ocpbias --halfcell-arg pe_offset_mv=5 --no-warm-start
./run.sh --mode score --in results/fit_seed404_pe5mv_nowarm

# (3) 원점·붕괴율을 원 다리와 나란히 본다
python3 tools/diagnose_pini_transition.py --objective pocv_dvdq_dqdv --legs \
  results/fit_22p_seed_404_hc        results/fit_seed404_pe5mv \
  results/fit_22p_seed_404_hc_nowarm results/fit_seed404_pe5mv_nowarm \
  results/fit_seed202_pe5mv          results/fit_seed505_pe5mv \
  | tee docs/22p_gap/pini_404_nowarm.txt

# (4) companion 축 원점도 본다 (오염이 여기 있었다)
python3 docs/22p_gap/leg_probe.py | grep -E '^leg|404'
```

## 판정 기준 (미리 못박는다 — 결과를 보고 정하지 않는다)

| 관측 | 해석 |
|---|---|
| `_nowarm` 5 mV 원점이 `a_pe ≈ 1.5032` (다른 다섯 격자 값)로 오고 붕괴가 0/8 로 떨어진다 | **가설 지지** — warm-start 연쇄가 404 를 이상 국소해로 끌었다. 처방에 `--no-warm-start` 또는 연쇄 순서 고정이 들어가야 한다 |
| `_nowarm` 5 mV 도 여전히 `a_pe ≈ 1.52` 이고 붕괴가 5/8 근방 | **가설 기각** — warm start 무관. 원점 불안정의 원인은 다른 축(restart 예산·난수 seed)이다 |
| 대조(무왜곡) 다리의 `pocv_dvdq` 원점이 1.0273 → 1.06 대로 바뀐다 | companion 오염이 warm start 산물이었다는 직접 증거 |
| 대조도 `_nowarm` 에서 결과가 크게 흔들린다 | 이 격자 자체가 최적화적으로 불안정하다 — 격자 수준 문제이고 404 만의 일이 아니다 |

비용: 격자 1개(640조건) × 2다리. 기존 seed 다리가 13 MB 였으므로 비슷한 규모다.

**주의**: `results/fit_22p_seed_404_hc_nowarm` 은 새 이름이다. 기존
`fit_22p_seed_404_hc` 를 덮어쓰지 않는다 — 대조가 사라지면 시험이 무의미해진다.


## 16.1 첫 시도가 fail-closed 로 막혔다 — 그리고 그게 옳았다

위 명령을 그대로 돌리니 두 다리 모두 fitting 진입 전에 거부됐다:

```
RuntimeError: half-cell 캐시 검증 실패 (F74):
  · 코드_identity: 실패 — meta c2e7d8b9fd11b54e ≠ 현재 a72c0f3a485c19bb
  · 코드_identity: 실패 — meta d842894dbbc2a0f9 ≠ 현재 a72c0f3a485c19bb
```

디스크의 half-cell 캐시가 **옛 digest 로 만들어졌다.** validator 는 캐시 생성
이후 코드가 바뀌면 거부한다 — 조용히 옛 배열로 계산하지 않는다.

### 이것이 드러낸 것 (리뷰 발견 14 의 실례)

**기존 22p 다리는 현재 코드에서 재실행할 수 없다.** 캐시를 먼저 재생성해야
하는데, §9 재현 절에 그 단계가 없다. 재현 명령을 그대로 따라 하면 여기서
막힌다. 왜곡 다리의 재현 명령이 §9 에 아예 없다는 것도 같은 구멍이다.

### 재생성이 물리를 바꾸는가 — git 으로 먼저 확인했다

`d842894`(8ce869f0) → `a72c0f3a`(HEAD) 사이 RUN_SCOPE 변경은 **두 개뿐**이다:

```
src/fitting.py                    +9    ← p_ini_cond 봉인 (provenance 전용)
tools/diagnose_pini_transition.py +159  ← 새 진단 도구
```

캐시를 만드는 코드는 **전부 불변**이다 — `src/halfcell.py` · `src/baseline.py` ·
`src/model.py` · `configs/base.yaml` 모두 변경 없음. `fitting.py` 의 9줄도
`p_ini_cond = ref_id` 를 `run_spec` 에 기록하는 것뿐이라 수치 경로를 안 건드린다.

**따라서 재생성해도 배열은 같아야 하고, 새 다리는 기존 24다리와 수치적으로
비교 가능하다.** 단 이것은 git diff 근거이고, runtime(numpy·scipy) 이 그 사이
바뀌었다면 배열이 달라질 수 있다 — 그래서 아래 A 단계로 **먼저 확인**한다.

### 고친 순서

```bash
cd ~/work/Yonghoon-DEM-DFT/degradation-degeneracy

# A. 진단 — "배열이 같은가" 를 본다 (캐시는 이 단계에서 이미 갱신된다, 아래 주의)
python -m src.halfcell --method ocp --verify
python -m src.halfcell --method ocpbias --pe-offset-mv 5 --verify
```

둘 다 **exit 1 로 끝나는 것이 정상**이다 (`코드_identity` 실패). 볼 것은 JSON 의
한 줄뿐이다:

| 출력 | 뜻 | 다음 |
|---|---|---|
| `"재생성_배열일치": true` | 배열 동일 — 코드 도장만 낡았다 | B 로 진행 |
| `"재생성_배열일치": false` | **배열이 달라졌다** | **멈춘다.** runtime 이 물리를 바꿨다는 뜻이고, 기존 24다리 전체의 재현성이 걸린 문제다 |

> **⚠ 정정 — A 는 비파괴가 아니다 (2026-08-20 실측).** 처음에 "덮어쓰지
> 않는다" 고 적었는데 **틀렸다.** 캐시 로드 경로는 코드 identity 불일치를
> **미스로 취급해 재계산하고 저장**한다 (자기치유). 실측 로그:
>
> ```
> WARNING: half-cell 캐시가 다른 코드로 계산됨 (c2e7d8b9… ≠ a72c0f3a…)
>          — 미스로 취급해 재계산: .cache/halfcell/…_ocp_b5009f515fb8.json
> INFO:    half-cell 기준 캐시 저장: .cache/halfcell/…_ocp_b5009f515fb8.json
> ```
>
> 결과적으로 해는 없다 — 배열이 같고(아래), 기존 다리는 자기 캐시 바이트를
> `_inputs/` 에 봉인해 두었다. 하지만 **B 단계(`--force`)는 불필요**하다.
> A 를 돌린 시점에 이미 갱신됐다.

**실측 결과 (두 캐시 모두)**:

```json
{ "구조검사": true, "구조검사_실패": [], "재생성_배열일치": true }
```

배열이 비트 단위로 같다 (`rtol=0, atol=1e-9`). 위 git diff 추론이 실측으로
확인됐다 — `d842894` 와 `a72c0f3a` 는 half-cell 물리가 동일하고, 새 다리는
기존 24다리와 수치적으로 비교 가능하다.

```bash
# B. (불필요 — A 가 이미 갱신했다)

# C. §16 의 (1)~(4) 를 그대로 다시
```

`--force` 는 캐시를 덮어쓰지만 기존 다리는 안전하다 — 각 다리가 자기 캐시
바이트를 `_inputs/` 에 content-addressed 로 봉인해 두었다 (F72).

---

# 4차 갱신 (2026-08-20) — §14 warm-start 가설: **기각**

`--no-warm-start` 로 404 의 대조·5 mV 두 다리를 재실행했다 (각 640조건, 3분).
판정 기준은 §16 에 **실행 전에** 표로 못박아 두었다.

## 17. 결과

| 다리 | warm | 원점 `p_ini` (dqdv) | 거짓 분리 | ①' 격차 bias |
|---|---|---|---|---|
| `fit_22p_seed_404_hc` (대조) | True | `[1.5185, −0.4219, 1.0633, −0.0602]` | 0/8 | −0.53%p |
| **`fit_22p_seed_404_hc_nowarm`** | **False** | `[1.5097, −0.418, **1.0872**, −0.0842]` | **7/8** | **−5.42%p** |
| `fit_seed404_pe5mv` (5 mV) | True | `[1.5206, −0.4318, 1.0665, −0.0634]` | 5/8 | +1.25%p |
| **`fit_seed404_pe5mv_nowarm`** | **False** | `[1.5206, −0.4318, 1.0665, −0.0634]` | 6/8 | −2.52%p |
| `fit_seed202_pe5mv` (대조군) | True | `[1.5032, −0.4203, 1.0693, −0.0661]` | 0/8 | −0.08%p |
| `fit_seed505_pe5mv` (대조군) | True | `[1.5032, −0.4203, 1.0693, −0.0661]` | 0/8 | −0.15%p |

## 18. 판정 — 사전 기준 대조

| 사전 기준 | 충족? | 실측 |
|---|---|---|
| nowarm 5 mV 원점이 `a_pe ≈ 1.5032` 로 오고 붕괴 0/8 → **가설 지지** | **아니오** | 원점이 `1.5206` 으로 **소수점 4자리까지 동일**, 붕괴 6/8 |
| nowarm 5 mV 도 `a_pe ≈ 1.52`, 붕괴 5/8 근방 → **가설 기각** | **예** | 정확히 이 경우다 |
| 대조의 `pocv_dvdq` 원점이 1.0273 → 1.06 대로 이동 | **아니오** | warm·nowarm 모두 `1.0273` 그대로 |
| 대조도 크게 흔들린다 → 격자 수준 불안정 | **예 (크게)** | 0/8 → **7/8**, bias −0.53 → **−5.42%p** |

**§14 가설 기각.** warm start 는 404 를 이상 국소해로 끌지 않았다 —
왜곡 다리의 원점은 warm 여부와 **무관하게 같다**. 404 의 `pocv_dvdq` 원점 오염
(1.0273)도 warm 산물이 아니라 **그 격자 pristine 조건 fit 자체의 성질**이다.

## 19. 대신 나온 것 — 무왜곡 대조가 warm 을 끄면 무너진다

가설을 기각한 실험이 더 큰 것을 냈다. **왜곡이 0 인 대조 다리**가
`--no-warm-start` 에서 0/8 → **7/8** 로 무너지고 격차 bias 가 −0.53 → **−5.42%p**
로 열 배가 됐다. 원점의 `a_ne` 도 1.0633 → **1.0872** 로 건강 범위(1.058~1.069)
밖으로 나갔다.

즉 이 셋업에서 **warm-start 연쇄가 결과를 떠받치고 있다.** 그것을 끄면 왜곡
없이도 두 전극이 갈린다.

이것이 중요한 이유:

1. **리뷰 발견 3 의 범위가 넓어진다.** 예산 축(restart)만이 아니라 **warm-start
   연쇄 자체**가 결론을 좌우하는 자유도다. 처방 설계에 반드시 들어가야 한다.
2. **`paired_fixed5_v4` 는 `warm_start=False` 다** (manifest 실측). §20.4 의 정본
   비교가 바로 이 regime 에서 나왔다는 뜻이다. 두 regime 의 차이가 이만큼
   크다면 그 정본의 해석도 다시 봐야 한다.
3. 원점 의존성은 **목적함수마다 다르다**: `pocv_dvdq` 원점은 warm·nowarm 이
   같고(대조 1.0273 / 5 mV 1.0624), 움직인 것은 `pocv_dvdq_dqdv` 뿐이며 그것도
   대조에서만이다. F26b 의 "연쇄된 `_fit_one` 한 번" 구조와 일치한다.

## 20. adaptive 조기 종료가 실제로 작동한다 — 발견 3 직접 확인

두 실행 모두 `--n-restarts 5` 를 줬는데 `restart_conditioned` 는 이렇게 나왔다:

```
대조 nowarm : n_restarts=2 → n=223,  n_restarts=5 → n=1057
5 mV nowarm : n_restarts=2 → n=200,  n_restarts=5 → n=1080
```

**약 17% 의 행이 2회에서 멈췄다.** 리뷰 발견 3 의 "`--n-restarts 20` 이라고 써도
각 행이 고정 20회를 수행한다는 보장이 없다" 가 실측으로 확인됐다. 따라서
§7 의 "전부 restart 5" 도 정확히는 **"restart 예산 5 로 지시했다"** 이지
"각 행이 5회를 돌았다" 가 아니다. 단계 B 의 예산 분리에 `--no-adaptive` 가
반드시 포함돼야 한다.

## 21. 한계 — 대조 비교는 digest 두 개를 건넌다

| 비교 | digest 구간 | 그 사이 RUN_SCOPE 변경 | 판정 |
|---|---|---|---|
| 5 mV warm vs nowarm | `d842894` → `a72c0f3a` | `fitting.py` +9 (p_ini_cond 봉인) + 새 진단 도구 | **깨끗** — 수치 경로 불변 |
| 대조 warm vs nowarm | `7250c6e6` → `a72c0f3a` | `fitting.py` +98, `halfcell.py` +144 (ocpbias 배선·stretch) | **주의** |

두 번째 구간의 변경은 전부 ocpbias 경로 추가이고, 무왜곡 `ocp` 캐시는 배열이
**비트 단위로 동일**함을 `--verify` 로 확인했다 (`재생성_배열일치: true`).
그래도 fit 경로 전체가 수치적으로 동일하다는 것을 증명하지는 않았다.

→ **§19 를 확정하려면 대조를 현재 digest 에서 `warm=True` 로 한 번 더 돌려야
한다** (3분). 그것이 0/8 을 재현하면 7/8 은 warm 때문이고, 아니면 digest 차이가
섞인 것이다. 명령:

```bash
./run.sh --mode fit --in results/grid_22p_seed_404 \
  --out results/fit_22p_seed_404_hc_warm_now --nproc 28 \
  --objective pocv_dvdq,pocv_dvdq_dqdv --n-restarts 5 \
  --reference halfcell --bounds halfcell
./run.sh --mode score --in results/fit_22p_seed_404_hc_warm_now
python3 tools/diagnose_pini_transition.py --objective pocv_dvdq_dqdv --legs \
  results/fit_22p_seed_404_hc results/fit_22p_seed_404_hc_nowarm \
  results/fit_22p_seed_404_hc_warm_now
```

---

# 5차 갱신 (2026-08-20) — §19 확정, 그리고 §20.4 정본으로 번진다

§21 이 요구한 대조 재실행(`warm=True`, 현재 digest)을 돌렸다.

## 22. digest 차이는 수치적으로 무해하다 — 완전 재현

| 다리 | digest | warm | 원점 `p_ini` | 거짓 분리 | ①' bias | 참0 중앙값 |
|---|---|---|---|---|---|---|
| `fit_22p_seed_404_hc` | `7250c6e6` | True | `[1.5185, −0.4219, 1.0633, −0.0602]` | 0/8 | −0.53%p | 0.24%p |
| **`fit_22p_seed_404_hc_warm_now`** | **`a72c0f3a`** | True | **`[1.5185, −0.4219, 1.0633, −0.0602]`** | **0/8** | **−0.53%p** | **0.24%p** |
| `fit_22p_seed_404_hc_nowarm` | `a72c0f3a` | False | `[1.5097, −0.418, 1.0872, −0.0842]` | 7/8 | −5.42%p | 2.6%p |

**네 값이 전부 일치한다.** `7250c6e6` → `a72c0f3a` 사이의 `fitting.py` +98 ·
`halfcell.py` +144 (ocpbias 배선·stretch 추가)는 **무왜곡 경로의 수치를 전혀
바꾸지 않았다.** §21 이 남긴 한계가 닫혔다 — diff 를 읽어서가 아니라 **완전
재현으로** 증명됐다.

부수 효과: 이것은 이 저장소에서 드문 **교차-digest 완전 재현** 실측이다.
"코드가 바뀌었으니 비교 불가" 가 항상 참은 아니라는 반례로 남긴다.

## 23. §19 확정 — 7/8 붕괴는 전적으로 warm-start 때문이다

digest 가 무해함이 증명됐으므로, `warm_now`(0/8) vs `nowarm`(7/8) 의 차이는
**`--no-warm-start` 하나**에 귀속된다. 왜곡이 0 인 대조가 warm 을 끄면 무너진다.

### 23.1 기전 — 연쇄의 **뒤쪽** 목적함수만 움직인다

`degeneracy_summary` 를 목적함수별로 보면 깨끗하게 갈린다:

| | `pocv_dvdq` (연쇄 1번째) | `pocv_dvdq_dqdv` (연쇄 2번째) |
|---|---|---|
| warm=True | `degen 0.800000` · `mae 0.032153303097964915` | `degen 0.184375` |
| warm=False | `degen 0.800000` · `mae 0.032153303097964915` | `degen 0.640625` |

**1번째 목적함수는 15자리까지 동일하다** — 앞이 없으니 warm 할 것이 없다.
움직인 것은 **2번째뿐이고, +0.457** 이다. F26b 의 "연쇄된 `_fit_one` 한 번"
구조와 정확히 일치한다.

## 24. ⚠ 이것이 §20.4 정본으로 번진다 — 새 열린 질문

`paired_fixed5_v4` 의 manifest 실측:

```
warm_start: False   adaptive: False   n_restarts: 5
```

**결론 1 철회의 근거가 된 그 정본이 warm=False regime 산물이다.**
`docs/08_REVIEW_RESPONSE.md` §20.4:

```
paired_fixed5_v4  pocv_dvdq       degen=0.619241
paired_fixed5_v4  pocv_dvdq_dqdv  degen=0.871951   (+25.27%p)
```

그런데 §23.1 에서 **warm-start 축 하나가 같은 통계를 +45.7%p 움직였다.**
결론이 서 있는 효과 크기(+25.27%p)보다 **크다.**

**이것은 정본이 틀렸다는 주장이 아니다.** 두 실행은 격자도 기준도 다르다:

| | `paired_fixed5_v4` | 이번 404 시험 |
|---|---|---|
| 조건 수 | 3,069 | 640 |
| 기준 곡선 | **grid** | **half-cell** |
| adaptive | False | **True** (기본) |
| warm | False | 양쪽 다 측정 |

효과가 그대로 옮겨간다고 말할 수 없다. 말할 수 있는 것은:

> **protocol 축(warm-start)이 측정 대상 효과와 같은 크기 이상으로 결과를
> 움직인다는 것이 직접 측정됐다.** §20.4 가 이미 달아 둔 유보("multimodal
> 97% 라 optimizer 가 그 목적함수를 못 푸는 효과가 섞여 있다")가 이제
> **정량적 근거**를 갖는다.

### 24.1 이걸 닫는 방법 — 비싸지 않다

`paired_fixed5_v4` 와 **같은 설정에서 warm 만 켠** 다리 하나면 된다:

```bash
./run.sh --mode fit --in results/grid_curves_v4 \
  --out results/paired_fixed5_v4_warm --nproc 28 \
  --objective pocv_dvdq,pocv_dvdq_dqdv --n-restarts 5 \
  --no-adaptive --reference grid
./run.sh --mode score --in results/paired_fixed5_v4_warm
```

(원 실행의 정확한 인자는 `results/paired_fixed5_v4/manifest.yaml` 의
`run_spec` 에서 확인해 맞출 것 — 위는 골자다. 3,069조건이라 404 보다 5배쯤
걸린다.)

판정: `pocv_dvdq_dqdv` 의 `degenerate_frac` 이 0.871951 에서 크게 내려오면
§20.4 의 +25.27%p 는 **protocol 산물**이고, 그대로면 목적함수 자체의 성질이다.
어느 쪽이든 결론 1 철회의 근거 서술을 다시 써야 한다.

## 25. adaptive 도 다시 확인

`warm_now` 실행도 `--n-restarts 5` 를 줬는데 `n_restarts=2 → 238행`,
`n_restarts=5 → 1042행` 이다 (약 19%). §20 과 같다. `paired_fixed5_v4` 는
`adaptive: False` 였으므로 그 정본에는 이 축이 없다 — 두 regime 이 **warm 과
adaptive 둘 다** 다르다는 뜻이고, §24.1 의 재실행은 반드시
`--no-adaptive` 를 포함해야 한다.

---

# 26. 실행 지시 — §24.1 (paired 정본에 warm 만 켠다)

**현재 digest `a72c0f3a485c19bb` 에서 실행한다.** 단계 3(코드 수정)이 들어가면
`paired_fixed5_v4` 와 나란히 놓을 수 없다.

## 인자를 manifest 에서 뽑았다

`results/paired_fixed5_v4/manifest.yaml` 의 `run_spec` 실측:

```
input        results/grid_curves_v4      reference     grid
bounds       expanded                    v_col         v_full_noisy
objectives   pocv_dvdq, pocv_dvdq_dqdv   n_restarts    5
adaptive     false                       warm_start    false   ← 이것만 뒤집는다
selection    full                        n_conditions  3069
```

`RUN_SH_DRY=1` 로 두 조립을 대조해 **`--no-warm-start` 하나만 다름**을 확인했다:

```
원 실행: … --n-restarts 5 --reference grid --no-adaptive --no-warm-start
새 실행: … --n-restarts 5 --reference grid --no-adaptive
```

## 명령

```bash
cd ~/work/Yonghoon-DEM-DFT/degradation-degeneracy

./run.sh --mode fit --in results/grid_curves_v4 \
  --out results/paired_fixed5_v4_warm --nproc 28 \
  --objective pocv_dvdq,pocv_dvdq_dqdv --n-restarts 5 \
  --no-adaptive --reference grid --bounds expanded
./run.sh --mode score --in results/paired_fixed5_v4_warm
```

3,069조건이라 404(640조건, 3분)의 약 5배 — **15~20분** 예상.

끝나면 두 줄만 있으면 된다:

```bash
python3 - <<'EOF'
import yaml
for n in ("paired_fixed5_v4", "paired_fixed5_v4_warm"):
    d = yaml.safe_load(open(f"results/{n}/degeneracy_summary.yaml"))["by_objective"]
    for o in ("pocv_dvdq", "pocv_dvdq_dqdv"):
        print(f"{n:26} {o:16} degen={d[o]['degenerate_frac']:.6f} "
              f"corr={d[o]['degenerate_frac_corrected']:.6f} "
              f"mae={d[o]['mean_abs_err']:.6f}")
EOF
```

## 판정 기준 (실행 전에 고정한다)

정본은 `pocv_dvdq 0.619241` / `pocv_dvdq_dqdv 0.871951`, 차이 **+25.27%p**.

| warm 켠 결과 | 해석 | 문서에 할 일 |
|---|---|---|
| `dqdv` 가 0.87 → 0.6 대 이하로 내려오고 차이가 **부호 반전**(dqdv 가 더 좋아짐) | **+25.27%p 는 protocol 산물이다** | 결론 1 철회의 *근거 서술*을 다시 쓴다 — 철회 자체는 유지하되 "warm=False regime 에서만 관측" 으로 한정 |
| `dqdv` 가 내려오지만 여전히 `dvdq` 보다 나쁨 | protocol 이 크기를 바꾸지만 **방향은 목적함수 성질** | 차이 수치를 regime 조건부로 표기 |
| `dqdv` 가 0.87 근처로 그대로 | **목적함수 자체의 성질** — protocol 무관 | §20.4 유지, 유보 문구만 정량화 |
| `dvdq`(1번째)가 움직인다 | **이상** — 연쇄 1번째는 warm 영향이 없어야 한다 (§23.1 에서 15자리 동일이었다) | 멈추고 원인부터 찾는다 |

마지막 줄이 중요하다. 404 시험에서 1번째 목적함수는 warm 여부와 무관하게
**15자리까지 동일**했다. 여기서도 `pocv_dvdq` 가 `0.619241` 그대로여야 하고,
아니라면 이 비교의 전제가 깨진 것이다.

---

# 6차 갱신 (2026-08-20) — §24.1 실행: 차이가 +25.27%p → +1.29%p 로 줄었다

## 27. 결과

```
paired_fixed5_v4       pocv_dvdq       degen=0.619241  corr=0.144309  mae=0.024227
paired_fixed5_v4       pocv_dvdq_dqdv  degen=0.871951  corr=0.945122  mae=0.065287
paired_fixed5_v4_warm  pocv_dvdq       degen=0.615854  corr=0.141599  mae=0.024220
paired_fixed5_v4_warm  pocv_dvdq_dqdv  degen=0.628726  corr=0.243902  mae=0.023653
```

| | `pocv_dvdq` | `pocv_dvdq_dqdv` | 차이 |
|---|---|---|---|
| **warm=False** (정본) | 0.619241 | 0.871951 | **+25.27%p** |
| **warm=True** (신규) | 0.615854 | 0.628726 | **+1.29%p** |

**결론 1 철회를 떠받치던 +25.27%p 가 warm 을 켜면 +1.29%p 로 줄어든다.**
부수 지표도 같은 방향이다 — `dqdv` 의 `mae` 0.065287 → 0.023653 (2.8배 개선),
`degenerate_frac_corrected` 0.945122 → 0.243902 (3.9배 개선).

모집단은 **정확히 일치**한다: 양쪽 다 `n_rows_total 6138`,
`n_rows_recoverable 2952`, `unrecoverable_frac 0.519062`. 비교 대상이 같은
조건 집합이라는 뜻이다.

## 28. ⚠ 그런데 사전 기준 4번에 걸렸다 — 이 결과는 아직 깨끗하지 않다

§26 에 실행 전 못박은 기준:

> `dvdq`(1번째)가 움직인다 → **이상** — 연쇄 1번째는 warm 영향이 없어야 한다
> (§23.1 에서 15자리 동일이었다). 멈추고 원인부터 찾는다.

실측: `0.619241` → `0.615854` (Δ **−0.0034**, 1,476조건 중 약 5조건).
`mae` 도 `0.024227` → `0.024220` 으로 6번째 자리에서 움직였다.
404 시험에서는 1번째 목적함수가 **15자리까지 동일**했는데 여기서는 아니다.

**원인은 digest 간격이다.** 404 비교는 `7250c6e6`→`a72c0f3a` 였고 그 구간이
수치적으로 무해함을 완전 재현으로 증명했다(§22). 이번 비교는
`d50295f9`(`c0f1daa0`, v4 본 실행) → `a72c0f3a` 로, **그 사이 RUN_SCOPE 가 크게
바뀌었다** (ocpbias 전체, stretch 재설계, p_ini_cond 봉인, 진단 도구 …).

즉 `paired_fixed5_v4_warm` 은 **warm 만 다른 것이 아니라 코드도 다르다.**

### 28.1 크기 비교는 warm 쪽을 강하게 시사한다 — 그러나 증명은 아니다

| 축 | 변화량 |
|---|---|
| `dvdq` (warm 영향 없어야 함 → 순수 코드 드리프트 추정치) | **0.0034** |
| `dqdv` (warm + 코드) | **0.2432** |

코드 드리프트가 `dvdq` 에서 0.0034 인데 `dqdv` 에서 0.2432 를 만들려면 **70배**
차이가 나야 한다. `dqdv` 가 multimodal 96% 라 교란에 훨씬 민감한 것은 사실이라
불가능하지는 않지만, warm 이 지배적이라고 보는 편이 자연스럽다.

**그래도 "자연스럽다" 는 증거가 아니다.** 이 저장소의 규율대로 빠진 대조를 채운다.

## 29. 빠진 대조 — 현재 digest 에서 warm 을 끈 다리

`paired_fixed5_v4` 를 **현재 코드에서 그대로 재현**하면 코드 축이 소거된다.
인자는 §26 에서 `RUN_SH_DRY=1` 로 이미 대조해 뒀다 (`--no-warm-start` 만 추가):

```bash
./run.sh --mode fit --in results/grid_curves_v4 \
  --out results/paired_fixed5_v4_nowarm_now --nproc 28 \
  --objective pocv_dvdq,pocv_dvdq_dqdv --n-restarts 5 \
  --no-adaptive --reference grid --bounds expanded --no-warm-start
./run.sh --mode score --in results/paired_fixed5_v4_nowarm_now
```

15~20분. 끝나면 세 다리를 한 줄씩 비교한다:

```bash
python3 - <<'EOF'
import yaml
for n in ("paired_fixed5_v4", "paired_fixed5_v4_nowarm_now", "paired_fixed5_v4_warm"):
    d = yaml.safe_load(open(f"results/{n}/degeneracy_summary.yaml"))["by_objective"]
    for o in ("pocv_dvdq", "pocv_dvdq_dqdv"):
        print(f"{n:30} {o:16} degen={d[o]['degenerate_frac']:.6f} "
              f"mae={d[o]['mean_abs_err']:.6f}")
EOF
```

### 판정 (다시, 실행 전에 고정)

| 관측 | 해석 |
|---|---|
| `nowarm_now` 가 정본(0.619241 / 0.871951)을 **재현** | 코드 축은 무해 → **+25.27%p → +1.29%p 축소는 전적으로 warm 때문** |
| `nowarm_now` 의 `dqdv` 가 0.87 이 아니라 0.6대 | 코드 변경이 `dqdv` 를 바꿨다 — **더 큰 문제**. v4 정본 전체의 재현성 문제로 격상 |
| `nowarm_now` 의 `dvdq` 만 0.6158 로 오고 `dqdv` 는 0.87 유지 | 코드는 `dvdq` 에만 영향 → warm 효과는 여전히 유효 |

## 30. 지금 시점에서 문서에 쓸 수 있는 것

§20.4 를 **아직 고치지 않는다.** §29 가 끝나야 무엇을 고칠지 정해진다.
다만 다음은 이미 확정이다:

- **`paired_fixed5_v4` 는 warm=False regime 산물이다** (manifest 실측).
  §20.4 가 그 사실을 밝히지 않는다 — regime 표기는 지금 추가해도 된다.
- **같은 조건 집합에서 warm 을 켜면 `dqdv` 가 크게 개선된다** (0.872 → 0.629).
  코드 축이 섞였지만 방향과 크기는 관측됐다.
- §20.4 의 기존 유보("multimodal 97% 라 optimizer 가 그 목적함수를 못 푸는
  효과가 섞여 있다")는 **정확했다.** warm start 가 바로 그 optimizer 축이다.
