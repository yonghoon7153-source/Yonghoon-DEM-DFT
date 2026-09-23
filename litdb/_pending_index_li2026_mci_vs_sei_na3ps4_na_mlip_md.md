# ⏸ 병합 대기 — `li2026_mci_vs_sei_na3ps4_na_mlip_md`

> 2026-09-23 · 지시에 따라 **`INDEX.md`·`comparison_vs_ours.md`·`db/` 직접 수정 금지 · 커밋 금지.** 넣을 내용을 여기 적어 둔다.
> **건드린 파일**: `litdb/papers/li2026_mci_vs_sei_na3ps4_na_mlip_md.md` · 이 파일 · 그리고 추출 도구가 만든 `litdb/figures/li2026_mci_vs_sei_na3ps4_na_mlip_md/`(25개 + `figures.json`) 와 **도구의 부수효과로 갱신된 `litdb/figures/_sources.json`**(이 slug 항목 1개 추가 — `git diff` 로 확인).
> 저자 코드는 `/home/user/bryantli-bli/naps-mic` @ **`85557efd5bf6ef62fb23fa584e11e2b79012c625`** 를 **읽기만** 했다 — 우리 repo 로 복사한 코드 없음(digest 에 경로·줄번호·해시로만 인용).
>
> **§J 번호 = `J-42`.** 2026-09-23 에 `comparison_vs_ours.md` 를 직접 열어 확인한 마지막 번호가 **J-41 ([Lomeli24], 5697줄)** 이었다(J-37 Chaney24SEI · J-38 Schw21 · J-39 Sjolin23AP · J-40 Jang26NaHSE · J-41 Lomeli24). repo 전체 `*.md` 에서 `J-4[2-9]` **0건**(다른 대기 파일이 선점하지 않았다). **병합자는 J-42 가 여전히 비어 있는지 다시 확인한다.**
> ⚠ J 절 머리의 `J-0` 색인(`| 약칭 | slug |`)에는 최근 관례(J-37~J-41 미등재)대로 **행을 제안하지 않는다** — 넣는다면 `| **[Li26MCI]** 🔧 | `li2026_mci_vs_sei_na3ps4_na_mlip_md` — … |` 2칸.
>
> **표 칸 수·열 순서는 아래 블록마다 머리글을 실제로 읽고 맞췄다** (2026-09-23):
> · `INDEX.md` `## ✅ Digest 완료` = **3칸** `slug | 논문 | 축`
> · `comparison_vs_ours.md` `📑 Reference key` = **4칸** `약칭 | 논문 (저자·년·저널) | digest/status | 유형`
> · `§E` = **4칸** `주장 | 출처 | 우리 | 일치`
> · `§H` = **3칸** `gap | 누가 필요로 함 | 보강책`
> 셀 안의 파이프는 전부 `\|` 로 이스케이프했다(절댓값 표기 포함).
>
> ⛔ **§A(이온전도)·§B(산화 4축)·§C(기계)·§D(전자구조) 에 넣지 않는다** — Na 계이고 포텐셜 원소가 **Na·P·S 뿐**이라 우리 계 값이 한 개도 없다. 들어갈 자리는 **§E · §H · §J-42** 셋이다.
> 약칭 **`[Li26MCI]`** — 충돌 확인 완료(`[Li25]`=CuBr₂ 도핑 · `[Li26NaRev]` · `[Li26FDI]` 와 **다른 논문·다른 저자**).
>
> 🎤 **talk 역링크 — 해당 없음.** `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `talks/lee2026_skku_mlip_materials_design.md` 하나이고 그 대기열(§99-10)에 이 논문이 **없다**(`Persson`·`Na3PS4`·`mixed conduct`·`MCI` 전부 0건). 덱과 어긋나는 것도 없다.
> ⛔⛔ **저자 혼동 방지**: 이 논문의 **Hwidong Jeon (UC Berkeley)** ≠ `jeon2026_concerted_li_motion_argyrodite_assi` 의 **Taegon Jeon (부경대)**. 병합 시 두 Jeon 을 잇지 말 것.

---

## ① `INDEX.md` 에 추가할 행 (**3칸** — `| slug | 논문 | 축 |`)

> `## ✅ Digest 완료 (paper-level)` 절, **88줄 `chaney2024_two_step_…` 행 바로 뒤**(같은 음극 계면상 축 · wang2022_resistive → chaney2024 → 이 편 순)가 자연스럽다.

| `papers/li2026_mci_vs_sei_na3ps4_na_mlip_md.md` **(본문 13 pp + SI 15 pp + 저자 코드 @`85557ef` · ✅ 그림 25개 추출(`Fig. S6` 는 추출기 누락) 중 본문 6 + SI 6 실독 · `Fig. 2` 원본 래스터 픽셀 판독 · 표 6장은 의도적 텍스트 전사)** | **[외부·Na 계·SEI↔MCI 판별 *방법* 원전 · ⛔물성 4축 아님(우리 계 값 0) · ⛔포텐셜 원소 Na·P·S 뿐 → Li₆PS₅Cl 불가]** **Bryant Y Li**, **Hwidong Jeon**, **Kristin A Persson\*** (UC Berkeley MSE + LBNL), "**Distinguishing the mixed conduction interphase: a machine learning molecular dynamics study on the Na₃PS₄/Na battery interface**" (***Mach. Learn.: Sci. Technol.* 7, 055011 (2026)**, DOI `10.1088/2632-2153/aea2f0` · 접수 2026-06-11 / 게재 2026-09-14 · OA CC BY 4.0 · refs 53 · `Fig. 1`–`6` + `Table 1` + `Fig. S1`–`S14` + `Table S1`–`S5` · 코드 `github.com/BryantLi-BLI/naps-mic`, Onsager 핵심은 비공개 `py_oats`) — ⛔ **Hwidong Jeon(Berkeley) ≠ Taegon Jeon(부경대, `jeon2026_…`)**.<br>**핵심**: 자체학습 **ACE MLIP**(r²SCAN 라벨, 20,114 배열, E RMSE 36–40 meV/atom) · Na₃PS₄‖Na **≈50만 원자 · 10.5 ns · 300 K · NpT Nosé–Hoover** → 계면상이 **log 모양으로 감속하되 안 멈춤** + 세 표지 ① 비정질 대리조성 Onsager **L_PP 지배**(16.68×10²⁰ (eV·cm·s)⁻¹) ② **비정질 Na₂S**(τ 0.28 vs 결정 1.35) ③ **Na–P 결합그래프 0.23 ns 부터 관통, 99.8 % 유지** ⇒ **"MCI 부합 · 필요조건이지 충분조건 아님"**(저자 명시). **전자 전도·밴드갭 계산 0**(`Table 1` 은 전부 문헌).<br>🔴🔴 **1번 임무 판정**: 이 논문은 **Li₇P₃S₁₁‖Li 를 돌리지 않았다** — 그 "평탄" 은 **Li2025JPCC(ref 19 · PBEsol 라벨 포텐셜 E RMSE 119.5 meV/atom · Langevin 열욕)** 에서 가져와 겹친 것이고, ✎ 픽셀 판독상 **그 점선도 1→10.4 ns 에 ≈0.3 nm(≈8 %) 더 자란다**. Na 금속 쪽 decade 당 **≈0.74 vs Li ≈0.22 nm** — 차이는 **감속률 3–4배**이고 "멈춤" 의 조작적 정의는 **본문·SI·코드 어디에도 없다**. ⇒ 우리 `kb/concepts/cv_vs_dqdv_and_two_windows.md` §8-4 **부분 정정 필요**(증명 부재는 맞지만 `kim2026` 누락 · "분야 전체의 공백" 과장).<br>**✎ 우리 검산 핵심**: Onsager 행렬 — **Li(ref 19)는 이원계 운동량보존 질량비를 0.05–1.2 % 로 만족, Na 는 11.8·1.7배 위반** · Na/Li 컬러바 지수 **10²⁰ vs 10¹⁸**(본문 "약 한 자릿수" 는 지수 무시 7.1배, 지수 포함 ≈706배) · NaP₁₅ 900 K **J_P ≈0.034 인데 J_Na ≈0**(질량 플럭스 합 ≠ 0) · `Table S4` Δμ_P > 0(900/1200 K)이라 **L_PP 항은 P 를 전해질 쪽으로 민다** · Li 쪽 "P 를 가두는 P–S 반상관" 은 **운동량보존 역류와 0.05 % 로 같다** · 결정성 τ 기준이 **0 K 정적 CIF** — 열변위 0.15–0.20 Å 만으로 "5배" → ≈2.4–3.1배 · 관통은 **고정 평면 두 장(z_frac 0.55·0.59) 사이 · Na 다리만(P–P 컷오프 무관)** · `Fig. 3a`·`Fig. 6` 에 **결정 Na₂S 가 있다** · `Table 1` Li₃P **2.03 eV(1991)** vs 우리 PBE **0.7092** → **방법 일관 갭이면 Li₃P 도 "반도체" 칸**.<br>**🔴 우리에게 불리한 것**: 노트 §8-4 가 `kim2026`·`lomeli2024` 를 빠뜨렸다 · 우리 음극 판정축(산물 갭)은 이 논문이 "불충분" 이라 부르는 축이다 · `anode_interface_b2o3.json` 0 V b2o3 행이 이미 **LiB(0.0) leaky** — 이 틀에서 B 도핑은 음극 MCI 위험을 **더한다**(단 산물집합은 `HZ-anode-b2o3-reaction-direction` 로 재확인 대기). **🔎 확보 1순위 = Li2025JPCC ref 19**(우리 `[Li25]` 와 **다른 논문**). | **음극(알칼리 금속) 계면상 *분류 방법* — SEI↔MCI 판별 지표 · MLIP-MD 가 원리상 못 보는 것(전자 차단)의 원전 (Na 계, 값 이식 금지)** |

---

## ② `comparison_vs_ours.md` **§📑 Reference key** 행 (**4칸** — `| 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |`)

| **[Li26MCI]** 🔧 **SEI↔MCI 판별을 MLIP-MD 로 시도한 첫 편 · 분석 코드 공개** · 🔴 **Li 대조군은 이 편의 결과가 아니다(ref 19 재수록)** · ⛔⛔ **Na 계 + 포텐셜 원소 Na·P·S → A–D 물성 4축 진입 금지** | **Bryant Y Li**/**Hwidong Jeon**/**Kristin A Persson\*** (UC Berkeley + LBNL) 2026 ***Mach. Learn.: Sci. Technol.* 7, 055011** (DOI 10.1088/2632-2153/aea2f0 · refs 53 · SI 15 pp `Fig. S1`–`S14`+`Table S1`–`S5` · 코드 `BryantLi-BLI/naps-mic` @85557ef) — "**Distinguishing the mixed conduction interphase: a machine learning molecular dynamics study on the Na₃PS₄/Na battery interface**". **ACE(pacemaker · 350/원소 · 7.0 Å · r²SCAN 라벨) · LAMMPS ML-PACE · ≈50만 원자 · 10.5 ns · 300 K · NpT Nosé–Hoover · dt 1 fs** + Onsager(용융급랭 대리조성 500–1500 K, 핵심 비공개 `py_oats`) + 결합그래프 퍼콜레이션 + Na–S RDF τ. ⛔ 전자구조·전기장 0 · 성장법칙 적합 0 · Li 계 재계산 0 · 생산 γ 통계 0 · 생산 계면 방위 미기재. ⛔⛔ **Hwidong Jeon(Berkeley) ≠ Taegon Jeon(부경대)** | ✅ `papers/li2026_mci_vs_sei_na3ps4_na_mlip_md.md` — 판정은 **§E 2행** + **§H 1행** + **§J-42**(방법 원전·코드 감사) | 계산 전용 (MLIP-MD + VASP AIMD(PBEsol)/r²SCAN 정적 라벨 + Onsager 후처리 · 실험 0 · 전자구조 0) |

---

## ③ `comparison_vs_ours.md` **§E. 환원 / 음극(Li 금속) 계면** 에 추가할 행 (**2행** · 4칸 `주장 | 출처 | 우리 | 일치`)

| 주장 | 출처 | 우리 | 일치 |
|---|---|---|---|
| **⭐⭐ 🆕 SEI↔MCI 를 MLIP-MD 로 가르는 첫 명시 시도 — 그러나 "멈췄다" 의 조작적 정의가 없고, 대조군(Li₇P₃S₁₁‖Li)은 다른 논문의 결과다** (2026-09-23 신설) — Na₃PS₄‖Na ≈50만 원자·10.5 ns: 계면상이 **log 모양으로 감속하되 계속 자람** vs Li₇P₃S₁₁‖Li **"plateau"(ref 19 재수록 · 이 편 포텐셜엔 Li 가 없다)**. 세 표지(Onsager L_PP 지배 · 비정질 Na₂S · Na–P 결합그래프 관통) = *"necessary but not sufficient"*(저자). ✎ **figure-read(원본 래스터 픽셀)**: Li 점선도 1→10.4 ns 에 **≈0.3 nm(≈8 %) 성장**, 금속 쪽 decade 당 **Na ≈0.74 vs Li ≈0.22 nm**, 창은 1 decade. **교란 7 항목**(`Table S5` 가 스스로 적은 것: 라벨 r²SCAN vs PBEsol · 컷오프 7.0 vs 6.0 Å · E RMSE 40 vs 120 meV/atom · 학습셋 20,114 vs 11,596 · **Nosé–Hoover vs Langevin** · Onsager 대리조성 · 연결성 분석 유무) | **[Li26MCI]** `Fig. 2` · §3.2 · §3.5 · SI `Table S5` · 코드 `interphase_analysis.py`(성장률 = 유한차분, log 적합 0) | `kb/concepts/cv_vs_dqdv_and_two_windows.md` §8-4: *"자기제한을 동역학으로 증명한 문헌을 litdb 안에서 못 찾았다"*(근거 `chaney2024` 하나). 우리 음극 자산 = **산물 갭뿐**(`sei_products.json` · `anode_interface_b2o3.json`), 계면 MD **0** | 🟡 **부분 정정.** *"증명 없음"* 은 **유지** — 이 편은 Li 계를 돌리지 않았고 그 점선도 자란다. 그러나 *"분야 전체의 공백"* · *"chaney 하나"* 는 **틀림** — 원자수송 정지를 *주장*한 MD 가 litdb 안(`kim2026` 프리프린트: PS₄ 20→6 층 평탄)·밖(ref 19)에 있다. **빠진 것 = 전자 차단 정지의 동역학 증거이고 MLIP 로는 원리상 불가**(*"not charge-aware"*, 저자). ⇒ **stepwise CV 필요 결론은 강화**된다 |
| **🔴 🆕 외부 표가 Li₃P 를 "넓은 갭 반도체(2.03 eV 간접 / 3.6 eV 직접)" 로 분류한다 — 방법이 달라 우리 누설 판정과 나란히 놓지 않는다** (2026-09-23 신설) — **[Li26MCI]** `Table 1` 의 Li₃P 값은 **1991 년 ab initio**(ref 50 Seel & Pandey, 방법 원문 미확인), 같은 표 Na₃P 는 **∼0.4 / 0.8 eV → "semiconducting"**. 논문은 이 대비로 *"Li 쪽 산물은 넓은 갭 → SEI · Na–P 는 반도체 → MCI"* 를 세운다. 표 출처는 섞여 있다(Na₂S 2.99 eV = **단층** 계산 ref 44 · NaP₇ = 나노튜브 기상성장 ref 47 · ᵃ 표시 불일치) | **[Li26MCI]** `Table 1` (PDF 텍스트 전사) · §3.4 | `db/properties/sei_electronic.json`(QE PBE fixed-occ nscf) **Li₃P 0.7092 eV** · `sei_products.json` MP **0.70 = `conductor-LEAK`** | ⛔ **나란히 금지**(방법 상이 · 우리 PBE 갭은 원장 규율상 **순위로만**). 🔴 그러나 **방법 일관 갭(PBE 계열)으로 놓으면 Li₃P 는 Na₃P 와 같은 "반도체" 칸**이다 — 논문의 Na↔Li 전자 대비는 **방법이 섞인 표** 위에 서 있다. ⇒ ① 그 1991 값을 근거로 **우리 Li₃P 를 비누설로 재분류하지 않는다** ② 이 틀을 **우리 값으로** 돌리면 우리 음극은 **더 불리**하다(§E "Li₃P 딜레마" 행과 같은 방향) ③ 게다가 Li₇P₃S₁₁‖Li 에는 **연결성 분석이 없다**(`Table S5` *"Not performed"*) — "Li 에서는 관통이 안 생긴다" 는 **검증되지 않았다** |

---

## ④ `comparison_vs_ours.md` **§H. 우리가 아직 못 하는 것 (정직 목록)** 에 추가할 행 (**1행** · 3칸 `gap | 누가 필요로 함 | 보강책`)

| gap | 누가 필요로 함 | 보강책 |
|---|---|---|
| **🔴🔴 🆕 우리는 SEI 와 MCI 를 가를 계산 수단이 하나도 없다 — 연결성·형태·교차수송·전자수송 전부 0** (2026-09-23 신설) | **[Li26MCI]** 가 최소 체크리스트를 보인다: (t,z) 배위수 지도 · 결합그래프 관통 · 결정성 τ · Onsager Lᵢⱼ — **그리고 그 구현의 함정 목록**(고정 평면 사이 관통 · 0 K 정적 결정 기준 · 기준틀 미선언 Lᵢⱼ · "멈춤" 정의 부재 · 전자 계산 0). 우리 음극 자산은 **산물 갭 한 축**(`sei_products.json` · `anode_interface_b2o3.json`)이고 반응 계면 MD 경험 **0**(`[Chaney24SEI]` §H 행과 같은 결손) | ① **표기부터**(무료·즉시): 음극 서사에 *"갭은 필요조건 · 연결성/형태 미계산"* 을 같이 적는다 ② ✎ **값싼 정적 계산 후보**: SQS 반형석 고용체(`Li₁₄PS₅Cl` 계, `[Chaney24SEI]` 그림)에서 **Li-다리 P 망의 두께별 관통확률** — 무작위 고용체면 P 음이온 분율 ≈0.14 < fcc 자리 퍼콜레이션 문턱 ≈0.20 이라 무한계 비관통이 예상된다(가정 명시, 얇은 층은 유한크기 효과) · ⚠ **보고량 카드(`kb/templates/estimand_card.md`) 먼저** — 배열 앙상블 집계 규칙·컷오프·두께 정의 선언 ③ 계면 MD 를 연다면 **첫날부터 게이트 셋**: Σᵢ mᵢ Lᵢⱼ = 0 검사 · **시간의존 경계 사이** 관통 · **동온도 결정 MD** 기준 τ ④ ⛔ UMA 에는 γ 가 정의되지 않는다 — 외삽 감시는 다른 대리지표로(`kim2026` digest §15.4) ⑤ ⛔ **"전자 차단 정지" 는 MD 과제가 아니다** — stepwise CV 등 실험이 답한다 |

---

## ⑤ `comparison_vs_ours.md` **§J-42** 블록 (신설 제안)

### J-42. 🔧🔴 **방법 원전 — [Li26MCI] 가 SEI↔MCI 를 MLIP-MD 로 가르는 세 표지, 그리고 코드 감사가 드러낸 것** (2026-09-23 신설 제안)

📎 **출처: `papers/li2026_mci_vs_sei_na3ps4_na_mlip_md.md`** · 초안 `_pending_index_li2026_mci_vs_sei_na3ps4_na_mlip_md.md` (병합 후 삭제) · 저자 코드 `github.com/BryantLi-BLI/naps-mic` @ `85557efd5bf6ef62fb23fa584e11e2b79012c625`

⛔ **A–D 물성 4축 표에 행을 만들지 않는다** — Na₃PS₄‖Na 한 계이고 **포텐셜 원소가 Na·P·S 뿐**(`mlip/input.yaml` L15)이라 우리 계로 옮길 수 있는 값이 **0** 이다. 옮기는 것은 **판별 지표의 설계와 그 함정**뿐이다.

**J-42-a. 이 논문에서 *못* 가져오는 것 (먼저 못박는다)**

| 양 | 이 논문 | 결론 |
|---|---|---|
| **Li₇P₃S₁₁‖Li "자기제한"** | ❌ **이 논문의 결과가 아니다** — ref 19(Li2025JPCC) 재수록, 포텐셜에 Li 없음 | ⛔ *"[Li26MCI] 가 Li 계 부동태를 보였다"* 금지 |
| **"멈춤" 판정** | ❌ 적합·문턱 **0** — ✎ Li 점선도 1→10.4 ns ≈8 % 성장 | ⛔ |
| **전자 전도 · 밴드갭 · 폴라론** | ❌ **계산 0**, `Table 1` 전부 문헌 | ⛔ *"MCI 임이 밝혀졌다"* 금지 (저자도 안 쓴다) |
| **Onsager 수치** (L_PP 16.68×10²⁰ · 플럭스) | 🔴 운동량보존 위반 · 지수 불일치 · 핵심 계산 비공개 | ⛔ 인용 금지 (J-42-c) |
| **결정성 "∼5배"** | ⚠ 0 K 기준 과장 | 🟡 쓰려면 *"꼬리비 ≈3배, 0 K 결정 대비"* |
| **두께 · 성장속도** | *"undeniably faster than expected"* · *"we do not claim to predict quantitatively"* | ⛔ |

**J-42-b. 세 표지 × (정의 · 코드 · 판정)**

| 표지 | 무엇을 쟀나 (코드 @85557ef) | 원인? | 신호로서 |
|---|---|---|---|
| ① P–P 수송 상관 | 균질 비정질 대리조성 200–1000 원자 · 900/1200 K · **Lᵢⱼ = Einstein(MSD 기울기)형**, 드라이버 `analysis/onsager/` → **비공개 `py_oats`** · 플럭스 **J = −L·Δμ** (`onsager_plotting.py` `get_flux`) | ⛔ 검정 0 | 🔴 **흔들림** — 기준틀·부호 (J-42-c) |
| ② 비정질 Na₂S | `crystallinity.py`: 고정 z [460, 490) Å 의 **Na·S 만**(P 조성필터 미검사) · 30 Å 슬랩을 **z 주기** 처리 · 기준 = **정적 CIF + σ 0.1 Å** · 최종 5 프레임 | ⛔ 검정 0 (Li 쪽 기전 차용) | 🟡 **정도 차이로는 선다**, 크기는 과장 · Na–S 가 MLIP 최약 화학(RMSE 58.5 · 반응 99.3 meV/atom · 4–7 Å 인력 과소) |
| ③ Na–P 연결 | `percolation.py`: **고정 창 z_frac 0.54–0.60** · 간선 P–P ≤2.5 · Na–P ≤3.2 Å · **Na–Na 없음** · 관통 = 한 성분에 **z ≥0.59 원자 1개 + z ≤0.55 원자 1개** | ⛔ **MLIP 안에서는 원리상 불가**(전자 없음) | 🟡 동반 신호 · **P–P 무관(Na 다리만)** · 스윕 상단 ≳3.5 Å 는 반응 안 한 전해질의 Na–P 도 간선이 되는 구간(그 평탄은 견고성 증거 아님) · **Li 대조 분석 없음** |

**J-42-c. 🔴🔴 코드·그림 감사 결과 — ✎ 우리 검산 (논문 미보고)**

1. **운동량보존 검사**(총운동량 0 인 MD 의 이원 조성은 교차항이 질량비로 강제된다: A–B 이원에서 \|L_AB\|/L_BB = m_B/m_A):
   - Li(ref 19, `Fig. 4d`): **P–S 행 1.097/1.135 = 0.9665 vs m_P/m_S 0.9661** · **Li–P 행 0.523/2.362 = 0.2214 vs m_Li/m_P 0.2241** → **만족**
   - Na(`Fig. 4c`): **Na–P 행 16.68/1.91 = 8.73 vs m_Na/m_P 0.742 → 11.8배 위반** · **P–S 행 0.60/1.07 = 0.561 vs 0.966 → 1.7배 위반**
   - ⇒ **SI S5 의 "same Green–Kubo Onsager formalism" 이 숫자로 지지되지 않는다.** 원인(기준틀 · 질량중심 표류 · 집계)은 `py_oats` 비공개라 판정 불가.
2. **질량 플럭스 합**: figure-read `Fig. S11` NaP₁₅(900 K) **J_P ≈ +0.034 · J_Na ≈ 0.000**, NaP₅(900 K) **J_P ≈ +0.009 · J_Na ≈ +0.003** → Σ Mᵢ Jᵢ ≠ 0. 질량중심 기준틀이면 나올 수 없다.
3. **부호**: SI Eq. S7(J = −LΔμ, 코드 동일) + `Table S4` **Δμ_P > 0 (900 K +0.121 · 1200 K +0.479)** ⇒ **L_PP 항은 P 를 전해질 쪽으로 민다.** 음극향 P 플럭스는 Na–P 교차항 몫이어야 하고, 조성족 평균 행렬로는 1200 K 에서 부호가 **음(−)** 이 나와야 하는데 그림은 양(+).
4. **단위**: 컬러바 **10²⁰(Na) vs 10¹⁸(Li)** — 본문 *"approximately an order of magnitude"* 는 지수를 뺀 7.1배, 지수 포함 **≈706배**.
5. **self/distinct**: 드라이버가 `L_tensor` 와 `L_tensor_self` 를 따로 뽑는데(`onsager_processing.py` L45–46) 논문은 L_PP 를 **안 나눴다** — L_PP > 0 은 정의상 항상 성립.
6. **"P 를 가두는 P–S 반상관"(Li)** = 운동량보존 역류와 0.05 % 로 같다 → **§J-31 `[Marc17NE]` 의 ② 유형(골격 역류, "빼야 한다")을 물리 기전으로 읽은 사례.**
7. **결정성 기준**: 우리 구현으로 정적 τ 1.347 · 꼬리비 0.817 을 **재현**(저자 1.35 / 0.82) → 원자별 독립 열변위 u = 0.15 / 0.20 Å 만 줘도 τ **0.86 / 0.67**(비 ≈3.1 / 2.4배), 꼬리비는 ≈0.81 불변.
8. **관통 판정선**: `Fig. 5b,c` 의 ±1.7 "Boundary" 점선 = **고정 source/sink 문턱**(0.57 ± 0.02 × ≈842 Å), 검출된 계면상 경계 아님 · y 축 **"Relative Z (Å)" → nm 오기** · `Fig. S14` z-span 이 **창 폭 0.06 에서 포화**.
9. **학습셋 필터 "80 meV Å⁻¹"**: `Table S2` 에 최대힘 ≥3 eV Å⁻¹ 배열 **4,592 개** → 문자 그대로면 모순(단위 오기 추정, 구축 코드 미포함).

**J-42-d. MD 규약 한 줄 대조** (판정 아님 — 나란히만)

| 항목 | [Li26MCI] | ref 19 (Li 대조군) | [Chaney24SEI] | 우리 (modelc/lpsocl) |
|---|---|---|---|---|
| MLIP | ACE 자체학습 7.0 Å | ACE 자체학습 6.0 Å | MTP 자체학습 5.0 Å | **UMA-s-1p1 (omat) 범용** |
| **라벨 범함수** | **r²SCAN** | **PBEsol** | 미기재 | **PBE(+U) 계열(omat)** |
| 앙상블 · 열욕 | NpT · Nosé–Hoover | NpT · **Langevin** | NPT · Nosé–Hoover | **NVT · Langevin** friction 0.02 |
| dt · T | 1 fs · 300 K | 1 fs · 300 K | 1 fs · 300–400 K | **2 fs · 600/800/1000 K** |
| 길이 · 크기 | 10.5 ns · ≈50만 | 10 ns · 50만 | 10 ns · ≤31,824 | **200 ps · 558** |
| 계면 · 반응 | ✅ · ✅ | ✅ · ✅ | ✅ · ✅ | ❌ · ❌ |
| 외삽 감시 | γ 1.5/5 (통계 0) | γ 1–2.5 | D-opt (학습 시) | ❌ (γ 정의 없음) |
| 확산 추출 | MSD 선형영역(창 미기재) | 같음 | — | **MSD 창 2–50 ps 고정** |

🔴 **온도·라벨 범함수·계면 유무가 전부 다르다** ⇒ 동역학 수치를 나란히 놓지 않는다.

**J-42-e. ⭐ 우리 규율을 *지지*하는 외부 사례 3건**
1. **보고량 먼저** — 이 편의 핵심 약점 셋(멈춤 정의 없음 · 관통이 고정 평면 · 결정성 기준 0 K)은 **보고량 카드 §1–3 에서 걸렸을** 문제다.
2. **검증 게이트는 결과 전에** — Σᵢ mᵢ Lᵢⱼ = 0 한 줄이면 Na 행렬 문제를 결과 전에 잡았다.
3. **교차상관은 기준틀을 선언해야 정의된다** — 우리 b2o3 1200 K Haven 제외 판정(*"골격이 흐르면 '무엇에 대한' 상관인지 정의되지 않는다"*)과 같은 논리의 외부 사례.

**J-42-f. ⛔ 이 논문을 인용할 때 반드시 같이 다는 단서 4개**
① **Li 대조군은 ref 19 의 결과**다(다른 포텐셜·Langevin) ② **전자 쪽은 계산 0**, 위상 + 문헌 결정상 갭 ③ **Onsager 수치는 운동량보존 불일치**로 인용 보류 ④ **Na 계 · 포텐셜 Na·P·S** — Li₆PS₅Cl 불가.

**상호참조**: **§J-37 `[Chaney24SEI]`**(같은 축 — Li 아르지로다이트, 결정화 후에도 대형 런 100 % 환원) · **§J-41 `[Lomeli24]`**(부동태 라벨 = 공간 국소성, 전자 판정 실패) · **§J-31 `[Marc17NE]`**(교차상관의 기준틀) · **§J-36 `[Wang22Res]`**(MLIP 학습창 밖 300 K 1709× 발산 — 이 편은 생산 MD 에 γ 감시를 **걸었다고 명시**하나 통계 0). 네 편을 합친 판정은 **§E 첫 행**(SEI↔MCI) 에 있다.

---

## ⑥ 🔴🔴 **우리 문서 정정 제안** — `kb/concepts/cv_vs_dqdv_and_two_windows.md` §8-4 (내가 고치지 않았다)

**판정 한 줄**: **부분적으로 고쳐야 한다** — *"증명한 문헌이 없다"* 는 맞지만, **근거로 `chaney2024` 하나만 들고 "분야 전체의 공백" 이라 쓴 것은 틀렸다**(작성 시점에 이미 litdb 에 `kim2026`·`lomeli2024` 가 있었다 — **이 논문과 무관한 누락**). 그리고 "계산으로 되는 것" 표가 **원자 수송 정지(MD 로 관측 가능)** 와 **전자 차단 정지(MD 로 불가)** 를 구분하지 않는다.

### ⑥-a. §8-4 의 표 — **교체 제안**

현재:
```
| | 계산으로 되는 것 | 실험이 필요한 것 |
|---|---|---|
| 분해산물이 절연인가 | ✅ 밴드갭 | — |
| 층이 **실제로 막는가** | ⛔ 안 됨 | **stepwise CV 2회차 전류 감쇠** |
```

제안:
```
| | 계산으로 되는 것 | 실험이 필요한 것 |
|---|---|---|
| 분해산물이 절연인가 | ✅ 밴드갭 (필요조건일 뿐) | — |
| 반응 전선의 **원자 수송이 멈추나** | 🟡 반응 MLIP-MD 로 **관측은 된다** — 단 고갈(유한 셀)·열욕·셀 크기·시간창과 분리해야 한다 | — |
| 층이 **전자를 실제로 막는가** | ⛔ 안 됨 — MLIP 에는 전자가 없다 | **stepwise CV 2회차 전류 감쇠** |
```

### ⑥-b. §8-4 의 ⚠ 문단 — **교체 제안** (현재 237–238 줄)

현재:
> ⚠ **분야 전체의 공백이기도 하다** — 2026-09-22 기준, 자기제한을 **동역학으로 증명한** 문헌을 우리 litdb 안에서 못 찾았다 (`[[litdb/papers/chaney2024_two_step_sei_growth_argyrodite_li_metal|Chaney 2024]]` 는 `self-limiting` 이라는 말이 0회이고, 그 계산의 6런이 전부 100 % 환원으로 끝난다).

제안:
> ⚠ **"동역학으로 보였다" 에는 두 층이 있고, 우리 litdb 에는 어느 쪽의 *증명*도 없다** (2026-09-23 정정 — 이전 문장은 `kim2026` 을 빠뜨렸고 "분야 전체의 공백" 이 과했다).
> - **① 원자 수송이 멈춘다 — *주장*은 있다, 깨끗한 증명은 없다.** `[[litdb/papers/kim2026_li_argyrodite_sei_reactive_md|Kim 2026]]`(⛔ 프리프린트)은 PS₄ 20→6 층 평탄(≈11 ns)을 "self-passivating" 이라 주장하지만 **고갈·단일 시드**를 배제하지 못한다. `[[litdb/papers/li2026_mci_vs_sei_na3ps4_na_mlip_md|Li 2026]]` 는 Li₇P₃S₁₁‖Li 의 평탄을 **다른 논문(Li 2025 JPCC)에서 가져와 겹쳤을 뿐**이고, 그 점선도 1→10 ns 에 ≈8 % 더 자란다(우리 픽셀 판독). `[[litdb/papers/chaney2024_two_step_sei_growth_argyrodite_li_metal|Chaney 2024]]` 는 `self-limiting` 0회이고 대형 6런이 전부 100 % 환원으로 끝난다. `[[litdb/papers/lomeli2024_predicting_reactivity_passivation_ssb_interfaces|Lomeli 2024]]` 는 40 ps AIMD 를 눈으로 "부동태" 라벨했다.
> - **② 전자가 막혀서 멈춘다 (§8-2 의 기전) — 증거가 없다.** MLIP 에는 전자가 없고(Li 2026 스스로 *"not charge-aware"* 라 적는다), AIMD 로 전자 판정을 시도한 Lomeli 2024 는 실패했다.
>
> ⇒ 계산이 줄 수 있는 것은 **①까지**이고 그것도 조건부다. **②는 stepwise CV 같은 실험이 답한다** — 이 절의 결론은 그대로 선다.

### ⑥-c. §10 "이 문서가 못 하는 것" 마지막 항목 — **교체 제안**

현재:
> ⚠ `confidence: medium` 인 이유 — 개념 정의는 표준 교과서 수준이지만, **§8 의 "자기제한을 증명한 문헌이 없다"** 는 우리 litdb 범위 안에서의 관찰이다. 더 넓게 보면 있을 수 있다.

제안:
> ⚠ `confidence: medium` 인 이유 — 개념 정의는 표준 교과서 수준이지만, **§8-4 의 판정(원자 수송 정지는 주장만 있고, 전자 차단 정지는 증거가 없다)** 은 우리 litdb 4편(`chaney2024` · `kim2026` · `lomeli2024` · `li2026_mci…`) 범위의 관찰이다. 그 판정의 **원전 하나(Li 2025 *J. Phys. Chem. C* 129, 16043 — Li₇P₃S₁₁‖Li MLIP-MD)** 를 우리는 아직 읽지 않았다.

### ⑥-d. "관련 문서" 에 **추가 제안**
- `[[litdb/papers/li2026_mci_vs_sei_na3ps4_na_mlip_md|Li 2026 (Na₃PS₄‖Na)]]` — SEI↔MCI 를 MLIP-MD 로 가르려는 첫 시도. "멈춤" 의 정의와 전자 쪽 계산이 왜 빠질 수밖에 없는지의 사례
- `[[litdb/papers/kim2026_li_argyrodite_sei_reactive_md|Kim 2026]]` — "self-passivating" 을 주장한 반응 MD (⛔ 프리프린트, 구조적 격리일 뿐 전자 차단 아님)

### ⑥-e. 병합 시 같이 할 것
- frontmatter `updated: 2026-09-23` · `explored:` 는 **사람만** 바꾼다(kb 규율) · `confidence: medium` 유지(근거가 여럿이지만 원전 ref 19 미열람).
- `python3 tools/kb_wiki.py index` 재생성 + `lint` **0 errors** 확인.

---

## ⑦ (선택) **원장 문구 제안** — 직접 고치지 않았다

### ⑦-a. `db/properties/sei_products.json` `caveats` 에 **한 줄 추가 제안**
> *"⚠ 외부 문헌이 Li₃P 를 '넓은 갭 반도체(2.03 eV 간접 / 3.6 eV 직접)' 로 분류하는 사례가 있다([Li26MCI] `Table 1`, 원출처 1991 ab initio). 방법이 달라 우리 PBE 값(`sei_electronic.json` 0.7092 eV)과 나란히 두지 않고, **Li₃P 를 비누설로 재분류하는 근거로 쓰지 않는다.** 방법 일관 갭(PBE 계열)으로는 Li₃P 가 [Li26MCI] 의 '반도체' Na₃P(0.4–0.8 eV) 와 같은 칸이다."*

### ⑦-b. `HZ-anode-b2o3-reaction-direction` 에 대해 — **새 정보 없음, 참고 한 줄만**
이 논문은 Li 아르지로다이트 방향 판정에 새 근거를 주지 않는다(Na₃PS₄ 계). 다만 SI `Table S3` 이 **"원자당 최저 반응 = NaP(6 e⁻ 부분환원)"** 를 "바닥 반응" 으로 고르고, ✎ **화학식단위당**으로는 **Na₃P(8 e⁻ 완전환원) 경로가 더 발열적**(−7.09 vs −6.51 eV/f.u.)이다 — **"원자당 최저 ≠ 금속 과잉 종착"** 이라는 우리 방향 버그와 **같은 종류의 규약 함정**의 외부 사례로만 참고한다(원장 문구 변경 불필요).

### ⑦-c. `db/literature/refs.json` **추가 제안**
```json
{
  "id": "li2026_mci",
  "authors": "Li, B. Y.; Jeon, H.; Persson, K. A.",
  "title": "Distinguishing the mixed conduction interphase: a machine learning molecular dynamics study on the Na3PS4/Na battery interface",
  "journal": "Mach. Learn.: Sci. Technol.",
  "volume": 7,
  "article": "055011",
  "year": 2026,
  "DOI": "10.1088/2632-2153/aea2f0",
  "title_verified": "2026-09-23 (PDF 직독)",
  "code": "github.com/BryantLi-BLI/naps-mic @ 85557efd5bf6ef62fb23fa584e11e2b79012c625 (Onsager core in private py_oats)",
  "key_content": "Self-trained ACE MLIP (Na, P, S only; r2SCAN labels; 20,114 configs; E RMSE 36-40 meV/atom). Na3PS4/Na ~500,000 atoms, 10.5 ns, 300 K, NpT Nose-Hoover, 1 fs. Interphase grows log-like without stopping; three markers (Onsager L_PP dominance on amorphous proxies, amorphous Na2S tau 0.28 vs crystal 1.35, Na-P bond-graph percolation from 0.23 ns) called consistent with MCI, 'necessary but not sufficient'. NO electronic-structure or conductivity calculation; Li7P3S11/Li comparison is reprinted from Li et al. JPCC 2025 (different potential, Langevin). Our audit: Na Onsager matrix violates momentum-conservation mass ratios (Li matrix satisfies them).",
  "tags": ["Na3PS4", "Na-metal anode", "interphase", "MCI", "SEI", "MLIP", "ACE", "MD", "Onsager", "percolation"]
}
```
⚠ **저자 확인**: Hwidong Jeon ≠ Taegon Jeon — `refs.json` 에 `jeon` 키가 있으면 합치지 말 것.
