# 교차리뷰 — Codex ↔ Claude, PTFE 8팔 요청서 (2026-08-24)

**입력**: 요청서 `codex_review_request_ptfe_8arm_20260824.md` ·
Claude 독립 리뷰 `claude_selfreview_ptfe_8arm_20260824.md` · Codex 리뷰(사용자 전달).
**방법**: 두 리뷰가 갈리는 지점을 **코드·산술로 독립 재현**했다.  아래 표의 "검증" 은 이
세션에서 실제로 돌린 결과다.

## 결론 (양쪽 최종 합의)

> **지금의 `1e-16` centerline 14 솔브는 돌리지 않는다.**  CL-49 arm 0 은 legacy 진단으로
> 동결하고, ⓐ PTFE 표현 규약 ⓑ exact-zero DOF ⓒ 전자·이온 fail-closed ⓓ SE 단위 를
> 먼저 닫은 뒤 새 protocol 로 L0→L1→L2 사다리를 탄다.

Claude 초판은 "안 A 를 돌리자" 였다.  **철회한다** — 근거는 D-2.

---

## Part 1 — Codex 주장 검증 (전부 이 세션에서 재현)

| # | Codex 주장 | 검증 | 결과 |
|---|---|---|---|
| B① | fresh arm 뒤 `--check-arm` 없음 | `sdcp_gain_vox015_8arm.sh:173-181` 의 검사가 **`if [ -s "$OUT" ]` 안에만** 있다.  262-268 의 신선 실행 뒤에는 bash exit 검사 + `mv` 뿐 | ✅ **확인** |
| B② | 이온 솔브 false-green | 전자: `:1195-1237` 이 `unconverged` 판정 + `cg_info`/`unconverged` 기록.  이온: `:1490-1536` 이 **무조건** `_s3mark('ionic','complete')`, `ion_resid` 만 남기고 `cg_info`/`unconverged` **없음** | ✅ **확인 — 비대칭 명백** |
| B③ | SE 단위 `%` 를 `%p` 로 표기 | `:363-365` 가 `100·hypot(se/mean, se/mean)` = **상대 %**.  `:383` 출력은 `%p` | ✅ **확인** (단 Part 4-①) |
| 10-3-b | ρ 민감도가 밴드를 지배 | 재현: ρ 1.10 → **+0.389** · 1.30 → **+0.0656** · 1.70 → **−0.505** mS/cm | ✅ **확인** |
| 10-3-b | contrast 이식 nominal ≈ 0.055 | σᵢ/σ_m = 0.01837 × 코드 SE 3.0 = **0.0551** | ✅ **확인** |
| 12-2 | n ∝ 1/ρ (문서 방향 반대) | ρ 1.10 → **+18.2 %** · 1.70 → **−23.5 %** | ✅ **확인** |
| 11-5 | centerline 부피비 0.458/0.318/0.269 | h²/[π(D/2)²] = **0.4584 / 0.3183 / 0.2694** | ✅ **확인** |
| 10-1 | CL-58 이 전자+이온 8팔 vox 0.15 완주 | CL-58 존재, LEAN=1, σ_e 가 `--no-ion` 값을 0.002 % 로 재현 | ✅ **확인** |
| 10-5 | `_FIXED_FIELDS` 불충분 | `:884-887` — `sigma_ion_sdcp` · `sigma_ion_se` · enable flags · `periodic` · `precond` **전부 없음** | ✅ **확인** |
| 12-3-a | AM 은 σᵢ=0 이라 이온 DOF 아님 | `_sig3i = [0,0,0,0,0, sdcp, se, 0, …]` — sid 1/2(AM) = 0 | ✅ **확인** |

**Codex 오류: 0 건.**  반박 가능한 것을 찾지 못했다.

---

## Part 2 — 독립 합의 (두 리뷰가 서로 모르고 같은 결론)

높은 신뢰도로 취급한다.

| 항목 | Claude | Codex |
|---|---|---|
| **exact-zero DOF 가 정답, `1e-16` 은 우회로** | N-1 (`step3_sigma.py:447 cond = sig > 0`) | 5-1 / 10-2-c (`:446-447`) |
| 막는 것은 payload 게이트가 "찍는다"와 "σ>0"을 묶은 것 | N-1 (`:1016`) | 5-1 (`:1016-1020`) |
| `1e-16` 은 leakage 감도 팔로만 잔존 | N-1 | 5-1 |
| **arm 0 을 기술통계엔 포함, 버리는 것이 오히려 선별** | N-6 | 3-2 |
| fail-fast **정책**은 옳고 **구현**이 미흡 | N-6② | 5-3 |
| **CPU 원장을 GPU 앞에** | §11-5 / N-3 | 10-2-0 / 11-5 |
| **상쇄 vs 수렴 판별 필요, 총비만으로 불가** | N-3 | 11-3 |
| PTFE 절단 채널의 부호가 VGCF 채널과 **반대** | N-3 | 11-5 (h² 소실) |
| 44/56 분해의 **인과 해석 불가** | Part3 4-1 "경로 의존" | 4-1 "protocol×composition 상호작용" |
| CL-38 hold 유지, 실험값은 서술적 위치표시만 | Part3 7-1 | 7-1 |
| per-fibril 직경을 raster 까지 전달해야 | N-2 | 11-2-a |
| 안 C 는 HOLD (collector 버그 선행) | Part5 | 10-4 |

---

## Part 3 — Codex 가 잡고 Claude 가 놓친 것

### C-1. ★★★ 이온 false-green (B②) — 안 B 의 전제를 무너뜨린다
Claude 는 §10-1 에서 *"vox 0.15 에서 σ_ion 을 켜라"* 라고만 했다.  **켜면 안 되는 이유가
따로 있었다** — 이온 채널에는 수렴 봉인 자체가 없다.  안 B(σ_ion 포함)를 그대로 돌렸으면
미수렴 이온값을 `complete` 로 받아 원장에 넣었을 것이다.  Claude 리뷰의 **가장 큰 누락**.

### C-2. ★★ 4-2 — 분해의 두 값이 **둘 다 arm 0** 이다
Claude 는 *"생산 8팔 SE 는 있으니 PTFE 팔 SE 만 붙이면 된다"* 라고 썼다.  **틀렸다.**
생산 8팔 평균은 **1.123191**(CL-33/34)이고 분해에 쓴 **1.126267** 은 생산 **arm 0** 이다.
⇒ 44.1/55.9 % 는 **n=1 paired 대수값**이고, 생산 8팔 SE 를 붙이는 것은 **다른 추정량의
오차를 빌려오는 것**이다.  Codex 의 paired block jackknife 제안이 옳다.

### C-3. ρ 축이 σᵢ 밴드를 지배한다
Claude F-A 는 **측정오차 축만** 봤다 (±5 % → [0, 0.60]).  ρ 축은 그와 **동급 이상**이고
ρ=1.70 에서 음수(비물리)까지 간다 = MG/밀도 가정 불일치의 신호.
⇒ Claude 가 요청서에서 쓴 밴드 [0, 0.1] 은 **두 번 틀렸다** (초판 점추정 → F-A 측정오차 →
여기서 ρ 축).  Codex 의 "계산용 sweep 을 분리해 두라" 가 옳은 처방이다.

### C-4. 12-2 방향 오류 · 12-3-a 정밀화 · `_FIXED_FIELDS` 구체 목록
Claude 문서의 *"입자 개수 = 침대에 직접 비례"* 는 방향이 모호했고 실제는 **n ∝ 1/ρ**.
12-3-a 는 Claude F-C("R_ct 는 STEP4 소관") 를 한 단계 더 정확히 만든다 — AM 은 애초에
**이온 DOF 가 아니라서** "AM|SE 완전접촉 과대평가" 라는 크기가 **정의되지 않는다**.

---

## Part 4 — Claude 가 보강하는 것 (Codex 가 명시 안 한 것)

### ① ★ SE 단위 오류는 **과거 판정을 뒤집지 않는다** — 이 문장이 반드시 필요하다
Codex 는 *"먼저 수정해야 한다"* 라고만 했다.  그대로 읽으면 **CL-33/41/58 을 전부 재판정해야
한다는 오독**이 생긴다.  실제는:
- 게이트 상수 `SE_MAX_PCT = 1.17` 은 **같은 상대 % 단위로 런 전에 커밋된 조작적 정의**다
  (prereg §4).  비교 양쪽이 같은 단위이므로 **게이트 판정은 자기일관**이다.
- 틀린 것은 **보고 라벨**뿐이다.  예: CL-41 의 "0.354 %p" 는 실제로 **0.354 % 상대**이고
  절대 percentage-point 는 ×R = **0.409 %p**.  라벨이 값을 **작게** 보고했으므로 방향은
  보수적이고 문턱 통과 판정은 불변이다.
⇒ **행동: 라벨 수정 + 원장 3건에 각주.  재판정·재실행 불요.**

### ② D-1 은 **측정으로 갈린다** — CPU 원장에 넣으면 된다 (Part 5 참조)

### ③ Codex 3-3 의 등록 문구 보강 — range `W` 는 극값 통계다
`W = max−min` 은 8점 중 **양 극단만** 쓴다.  한 팔의 이상치가 그대로 `Q` 를 지배한다.
⇒ `W` 와 함께 **SD 와 IQR 을 병기**하고, `Q` 를 세 통계 전부로 계산해 **셋의 부호가 같을
때만** 읽는다.

### ④ Codex 12-4 의 bed seed 수에 **비용 추정이 없다**
"최소 5 · 선호 8" 은 통계적으로는 옳으나 DEM+MPM 침대 재생성 비용이 미상이다.
⇒ 사다리 마지막에 두되, **1 개 재생성 실측 시간**을 먼저 재고 수를 정한다.

---

## Part 5 — 진짜 불일치 3 건과 판별

### D-1. capsule 을 만들 것인가 — **미해결, 측정으로 갈린다**
- **Codex 11-2-a**: variable-radius capsule 을 만들고 per-fibril d 를 raster 까지 전달하라.
- **Claude N-2**: 만들지 마라 — 절연체는 부피가 옳은 불변량이 아니고(도체는 σ 로 보상
  가능했지만 σ=0 은 보상 불가), `vol_conserve` 인발이 만든 **가는 꼬리는 어떤 실행가능
  vox 에서도 sub-voxel** 이라 capsule 이 그것을 못 고친다.
- **양쪽 다 per-fibril d 전달에는 동의**한다.  갈리는 것은 *"capsule 로 부피를 맞추면
  문제가 닫히는가"* 다.
- **판별 (CPU, 솔브 0)**: 실침대에서 per-fibril d 분포를 뽑아
  **`d_i ≥ 2h` 인 fibril 의 부피 몫**을 세 격자에서 잰다.
  · 그 몫이 크면 → capsule 이 대부분을 고친다 = **Codex**
  · 작으면 → capsule 은 소수 굵은 stub 만 고치고 나머지는 여전히 centerline = **Claude**
  ⇒ 어느 쪽이든 **부분부피(partial-volume) 처리**가 필요할 수 있다 — Codex 12-5-c 가
  "hard-overwrite 대신 부분부피" 를 이미 언급했다.  이것이 실제 착지점일 가능성이 높다.

### D-2. 안 A 를 지금 돌릴 것인가 — **Claude 양보, Codex 채택**
Claude 초판은 "돌려라(14 솔브)" 였다.  **철회한다.**  두 가지 때문이다:
1. **C-2** — 분해의 두 값이 둘 다 arm 0 이라, Claude 가 상정한 "생산 8팔 SE + PTFE 8팔 SE"
   합성이 성립하지 않는다.  8팔을 돌려도 얻는 것은 **한 규약의 폭**이지 분해의 오차막대가
   아니다 (분해에는 생산 8팔도 같은 규약으로 다시 필요).
2. **11-5 산술** — centerline 표현부피가 0.458 → 0.269 로 **h² 로 무너진다**.
   그 규약을 8팔로 정밀화하는 것은 **잘못된 양을 정밀하게 재는 것**이다.
⇒ **안 A = DROP.**  단 Claude 가 하나 유지한다: **팔-폭(finite-origin 민감도) 자체는
여전히 미관측**이므로, 새 protocol 의 pilot 에서 그것을 **첫 산출물**로 잡는다.

### D-3. σ_SDCP = 250 의 영향 크기 — **Claude 부분 철회, 🟡 → 🟠**
- **Claude N-4**: 변분 항등식 w = ∂ln σ_eff/∂ln σ_SDCP ≈ 소산 분담 ≈ 1 % ⇒ ÷3 에도 ~1 % 유계.
- **Codex 12-1**: CL-44 의 6.4 % 는 overlap assignment 만 바꾼 것이라 근거가 아니다.
- **판정**: Codex 의 CL-44 반박은 옳다(Claude N-4 는 CL-44 를 쓰지 않았으므로 그 부분은
  요청서 §12-1 을 겨눈 것이다).  그러나 **N-4 자체도 틀렸다** — 재계산:
  · w 는 **상수가 아니다**.  σ_SDCP 가 내려가면 커진다 (리포의 σ_SDCP 스윕이 그 형태를
    보인다; 그 스윕의 **절대값은 인용 금지 계열**이므로 여기서는 **형태만** 쓴다).
  · 따라서 Δln R = −∫ w d ln σ_SDCP 는 선형 추정 −1.1 % 보다 **크다**.
  · SBE 에는 SDCP 가 없으므로 이 변화는 **DBE 에만** 걸리고 곧바로 R 에 실린다.
  · ÷3 이면 R 1.1232 → 대략 **1.07~1.11**, 이득 **+12.3 % → +7 ~ +11 %**.
⇒ **헤드라인에 유의미하다.**  Claude 의 "🔴 → 🟡 강등" 을 **철회**하고 🟠 로 둔다.
  Codex 의 처방(시편 provenance 확보 **또는** 최종 geometry 에서 σ_SDCP sweep)이 맞다.

---

## Part 6 — 통합 사다리 (양쪽 합의 + D-1 판별 삽입)

```
S0. 동결·등록
    protocol id · code SHA · input digest · 사전등록 (Codex 3-3 문구 + Part4-③ 의 SD/IQR 병기)
S1. 코드 수정 (GPU 0)
    (a) ptfe_stamp={off,centerline,capsule} 를 sigma_ptfe 와 분리 + sid 7 zero-DOF
    (b) fresh arm 마다 --check-arm · payload failure 를 nonzero exit 로 전파 · 끝에 실제 verdict
    (c) 이온 cg_info/unconverged 기록 + fail-closed  ← C-1, 안 B 의 전제
    (d) SE 라벨 % 로 수정 + 원장 3건 각주 (Part4-①: 재판정 불요)
    (e) _FIXED_FIELDS 확장 (Codex 10-5 목록 전부) + missing field = HOLD
S2. CPU raster 감사 (3 grids × 8 origins × 2 beds × PTFE on/off, 솔브 0)
    Codex 10-2-0 지표 전부 +
    ★ D-1 판별: per-fibril d 분포와 `d_i ≥ 2h` fibril 의 부피 몫
    취소 규칙은 Codex 11-5 게이트를 **결과 보기 전에** 확정
S3. vox 0.15 한-origin 전자+이온 pilot — peak RSS · cg 봉인 · 팔-폭 첫 관측
S4. 사다리  L0 = no PTFE │ L1 = 새 PTFE 규약 + 동일 σ_ion │ L2 = 동일 mask + σ_ion(SDCP) sweep
    각 단계 --compare-dir --expect-differ (확장된 _FIXED_FIELDS 로)
S5. 통과 시 vox 0.15 전체 8 origins (arm 0 포함 재실행 — 규약이 달라 재사용 불가)
S6. 새 protocol 로 electron-only 격자 스터디 (0.125 · 0.115 + admissible 세 번째)
S7. paired bed seeds — 1개 재생성 실측 시간 먼저, 그 다음 수 결정 (Part4-④)
```

**제출 전 필수 (양쪽 합의)**: ρ_SDCP 실측 확정 · σ_e,SDCP 시편 provenance(또는 최종
geometry sweep) · PTFE 표현 규약.  AM|SE 는 STEP4/셀 임피던스를 주장할 때만.
