# 외부 자료 — 이상욱 랩 argyrodite 가수분해 데이터셋 ([30])

> 출처 **`github.com/jhkimmmmm/Hydrolysis-argyrodite`** (commit `25d8c62`) · 입수 2026-08-26
> 대응 논문: `[CMS]` **Ji Hoon Kim**, **Sang Uck Lee\***, *"Deciphering Surface Hydrolysis Mechanism in
> Argyrodite via Large-Scale Machine Learning Potential Simulations"*, ***Adv. Funct. Mater.* 2026** —
> **accepted, production 대기**(권·쪽·DOI 미발급, 2026-08-26 랩 발표목록 기준). **논문 본문 미확보.**

## ⚠ 권리 — 먼저 읽을 것

**upstream repo 에 LICENSE 파일이 없다.** 공개돼 있지만 **재배포·재사용 조건이 명시돼 있지 않다.**

- ✅ 해도 되는 것: **우리 내부 분석**, 우리 도구 검증, 우리 계와의 대조.
- ⛔ 하면 안 되는 것: **재배포**, 이 수치를 **우리 결과로** 제시, 논문·발표에 **출처 없이** 인용.
- 원고에 쓸 일이 생기면 **논문이 출판된 뒤 논문을 인용**하고, 데이터는 저자에게 확인받는다.

## 무엇이 들어 있나 (upstream 원본 중 **우리가 고른 것만**)

| 경로 | 무엇 |
|---|---|
| `validation/*_MD_fidelity_DFTvsMLP.csv` | **MD 궤적 스냅샷의 MLP vs DFT 에너지** — 61·62점, 0–500/510 ps |
| `validation/*_combined.xyz` | 위 스냅샷의 **구조 62프레임씩** (LPSC 280원자 · LPSnSC 284원자) |
| `validation/*_fine-tuned.png` | upstream 이 그린 상관도 |
| `validation/correlation_upstream.py` | upstream 의 상관도 스크립트 |
| `md_products/500ps_*.cif` | **500 ps 최종 스냅샷 3종** (LPSC+H₂O · LPSC+H₃O⁺/OH⁻/H₂O · **LPSnSC**+H₃O⁺/OH⁻/H₂O) |
| `UPSTREAM_README.md` | 원본 README 그대로 |

**가져오지 않은 것**: `checkpoint_best.pth`(10.3 MB×2) · `*_model.pt`(3.5 MB×3) — 총 30 MB.
repo 를 무겁게 만들 이유가 없다. 필요하면 upstream 에서 다시 받는다.

## 🔬 우리가 이 데이터에서 읽은 것 (2026-08-26)

### ① 덱 슬 22 의 `8.8 meV/atom` 출처가 확인됐다 — 그리고 **읽는 법이 달라진다**

| 계 | 스냅샷 | MAE | RMSE | **부호있는 편향** | **편향 제거 후 산포** |
|---|---|---|---|---|---|
| **LPSC + H–O** | 61 (0–500 ps) | **8.77** | 8.96 | **+8.77** | **1.84** (MAE 1.35) |
| **LPSnSC + H–O** | 62 (0–510 ps) | **4.27** | 4.72 | **+4.27** | **2.03** (MAE 1.65) |

단위 meV/atom. 부호는 `MLP − DFT`.

🔑 **MAE ≈ RMSE ≈ |편향| 이고, 123 스냅샷 전부에서 부호가 같다(음수 0개).**
즉 이 오차는 **산포가 아니라 거의 순수한 상수 오프셋**이다.

**왜 중요한가** — 상수 에너지 오프셋은
**① 에너지 *차이*에서 상쇄되고 ② 힘에 전혀 기여하지 않는다**(위치 미분이 0).
따라서 *"fine-tuned SevenNet 의 오차 8.8 meV/atom"* 은 **동역학적으로 의미 있는 오차를 6배 과대평가**한다.
실제로 물리에 남는 산포는 **1.35 meV/atom** 이다.

⛔ **단 이건 에너지만이다.** 힘 오차는 이 CSV 에 없고, 덱 슬 22 의 **0.57 eV/Å** 이 그 값이다.
**동역학을 지배하는 것은 힘**이므로, 위 재해석이 *"이 포텐셜은 동역학에 충분하다"* 를 뜻하지는 **않는다**.

### ② **500 ps 반응 MD 동안 오차가 커지지 않는다** ← T1 이 묻던 것

| 계 | 전반 MAE | 후반 MAE |
|---|---|---|
| LPSC | 9.02 (0–190 ps) | **8.53** (200–500 ps) |
| LPSnSC | 5.15 (0–200 ps) | **3.38** (210–510 ps) |

**둘 다 나빠지지 않고 오히려 좋아진다.** 반응이 진행되며 새 화학종(H₂S·PS₃OH 등)이 생기는데도
포텐셜이 훈련 분포 밖으로 밀려나지 않았다는 뜻이다 — **T1 의 "스냅샷 수준 외삽" 질문에 대한
외부 실측 사례 1건.**

⚠ 단 이건 **그들 fine-tune 모델**이 **그들 계**에서 그렇다는 것이다. 우리 UMA 가 우리 b2o3 에서
그렇다는 근거가 **아니다**. 그리고 **단일 궤적**이라 오차막대가 없다.

흥미로운 세부: LPSC 는 `t=0`(반응 전)에서 오차가 **1.92** 로 작다가 반응이 시작되면 ~9 로 올라가
그대로 유지된다. 오프셋이 **H/O 화학종이 들어오면서 생긴다**는 뜻으로 읽힌다(우리 해석, 미검증).

### ③ 엔진이 **SevenNet 이 맞다** — 아티팩트로 확인

`checkpoint_best.pth` 의 pickle 에 `sevennet`·`nequip`·`num_convolution`·`lmax`·`cutoff` 가 들어 있고,
레이어 인덱스가 `0_…`–`4_…` 로 **5 메시지패싱 층** — `park2024_sevennet_parallel_gnn_md` 의
**SevenNet-0 사양(5층)** 과 일치한다. ⇒ 덱의 *"가수분해 = SevenNet"* 표기가 **논문 없이 검증됐다.**

⚠ **`Sn`(주석) 은 여전히 덱 정보다** — 다만 파일명 `LPSnSC` 가 **Sn 치환계의 존재**를 확인해 준다.

## ★ 이 데이터로 **할 수 있는 것** (아직 안 함)

| | 무엇 | 왜 값어치가 있나 |
|---|---|---|
| **A** | `combined.xyz` 62프레임에 **우리 UMA 를 단일점**으로 돌려 그들 DFT 와 대조 | **T1 대리지표를 남의 정답지로 교정**할 수 있다. 황화물+물 반응계에서 **우리 포텐셜**의 실측 오차를 얻는다 — 우리가 지금 갖고 있지 않은 수치다 |
| **B** | `500ps_*.cif` 3종에서 **잔존 PS₄ 층수 · H 침투 깊이**를 우리 스크립트로 재집계 | 논문 없이도 슬 23–24 의 기구(H→S 결합, Sn scavenging)를 **우리 관측량으로** 확인 |
| **C** | LPSC vs LPSnSC 생성물 비교 | 우리 도펀트 축(Sn)에 **직접** 걸린다 |

⛔ **A 를 할 때 주의**: 그들 DFT 설정(functional·컷오프·k-점)을 모른다. 절대값 일치를 기대하면 안 되고,
**상수 오프셋을 뺀 산포**만 비교 가능하다. 그것이 위 ①이 알려준 읽는 법이다.

## 원본 확인용

- upstream: `github.com/jhkimmmmm/Hydrolysis-argyrodite` @ `25d8c62`
- 우리가 계산한 통계는 `validation/*.csv` 로 재현 가능 (열: `Step, DFT (eV), DFT_a (eV/atom), MLP (eV), MLP_a (eV/atom)`)

---

## ⛔ 원본 파일은 이 repo 에 없다 (2026-08-26 정정)

**이 repo 는 공개다**(`visibility: public`). LICENSE 없는 3자 자료를 커밋하면 **실제 재배포**가 된다.
한 번 커밋했다가 **추적을 해제**했다(`.gitignore` 의 `db/external/*` 규칙).

- **원본 재취득**: `github.com/jhkimmmmm/Hydrolysis-argyrodite` @ `25d8c62` 에서 다시 받는다.
- **여기 남은 것**: 우리가 쓴 문서 · **우리가 계산한 CSV** · 우리가 그린 그림뿐이다.
- ⚠ **git 히스토리에는 아직 남아 있다.** 지우려면 history rewrite + force-push 가 필요하고, 그건 사용자 판단 사항이다.
