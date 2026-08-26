# kim2025_csp_sse — 사용 규칙 (우리 쪽 메모)

**출처**: upstream `github.com/jhkimmmmm/CSP_SSE` @ `e4a6fd4`
**논문**: Kim et al., *J. Am. Chem. Soc.* **2025**, 147, 47381–47391 (DOI 10.1021/jacs.5c15665)
**digest**: `litdb/papers/kim2025_csp_metastable_edge_sharing_sse.md` — **§21 이 이 폴더의 분석**

---

## ⛔ 사용 금지 사항 (2026-08-26 확정)

1. **LICENSE 가 없다.** upstream 저장소에 라이선스 파일이 존재하지 않는다.
   → **재배포 금지 · 우리 결과/그림/원고에 제시 금지 · 내부 분석 전용.**
2. **논문은 이 저장소를 밝히지 않는다.** Data Availability 는 figshare
   (`10.6084/m9.figshare.29468165.v4`) 만 적는다. 즉 이 폴더의 내용물은
   **논문의 주장과 같은 지위가 아니다.** 어긋나는 곳이 실제로 있다(아래 3).
3. 🔴 **`structures/Li2GeS3/` 는 논문 Fig. 3c·S5 와 대응이 맞지 않는다** (digest §21e, **Q9**).
   독립 판정 결과 배포된 10개 중 **edge-sharing 은 `7_stable.cif`(C2/m, Ge–Ge 3.23 Å) 하나뿐**인데,
   Fig. 3c 는 rank **6 과 10** 을 edge 로 찍는다. **개수 자체가 안 맞는다.**
   → **이 조성으로 논문 결과를 재현하려 하지 말 것.** 다른 3조성(Li₂SiS₃ · Li₄SiGeS₆ · Li₄SiSnS₆)은
   36/40 검증에서 안전하다.

---

## ✅ 쓸 수 있는 것

| 파일 | 우리 용도 | digest 절 |
|---|---|---|
| `mtp_provenance.json` | MTP 학습셋 크기·헤더 실측 (**Q6 부분 종결**) | §21b |
| `mtp/*_pot.mtp` | `max_dist 5.000 Å` = 본문 `R_cut 5 Å` 검증 통과. `min_dist` 비대칭 | §21b |
| `UPSTREAM_README.md` | AIMD supercell 규약 **"~10 Å lattice dimension"** (§11-9 부분 종결) | §21c |
| `scripts/dynamics_Li_CSM.py` | ★ **T14 참조 구현** — `chemenv` `T:4` CSM + 4-이웃 `ConvexHull` 부피 | §21d |
| `structures/` (Li₂GeS₃ 제외) | 연결방식·공간군·V/atom 독립 검증용 | §21e |

⚠ **`dynamics_Li_CSM.py` 를 그대로 돌리지 말 것** — 결함 C1(5이웃 시 거리순 아님)·C3(예외 자리에
직전 값 재사용)·C5(finder 재생성으로 매우 느림)를 고쳐서 이식한다. digest §21d 참조.

⛔ **V_dead / packing ratio α 를 계산하는 코드는 이 저장소에 없다.** 논문·SI 에도 없다(§20-M10).
→ **α 재구현은 하지 않는다** (우리 BVSE 채널 % 가 대체재이고 정의가 더 명확하다).

---

## ✅ 라이선스 확정 (2026-08-26 정정) — **CC BY 4.0**

**figshare 페이지에서 확인했다.** upstream **GitHub 에는 LICENSE 파일이 없지만**,
같은 내용이 **figshare 에 CC BY 4.0 으로 게시**돼 있다.

> **figshare**: `10.6084/m9.figshare.29468165` · **Version 4**, posted 2025-07-30 ·
> Software · authored by **Kim Ji Hoon, Sang Uck Lee** · **LICENCE: CC BY 4.0** ·
> RELATED MATERIALS → `github.com/jhkimmmmm/CSP_SSE`
> 파일: `CSP_SSE.zip` (7.61 MB) — 우리가 받은 `jhkimmmmm-CSP_SSE-e4a6fd4` 와 **동일**

⇒ **재배포 가능하다. 조건은 출처 표시(attribution)뿐이다.**
한 번 추적 해제했다가 **되돌렸다**(2026-08-26).

### 출처 표시 (이 자료를 쓸 때 반드시)
> Kim, J. H.; Lee, S. U. *Machine Learning-Assisted Crystal Structure Prediction of
> Solid-State Electrolytes: Revealing Superior Ionic Conductivity in Metastable
> Edge-Sharing Phases*. figshare (2025). **DOI 10.6084/m9.figshare.29468165** · **CC BY 4.0**.
> 대응 논문: *J. Am. Chem. Soc.* **2025**, 147, 47381–47391.

⚠ **다른 외부 자료에는 이 예외가 적용되지 않는다.**
- `db/external/kim2026_argyrodite_hydrolysis/` — upstream 에 LICENSE 없음, figshare 도 없음 ⇒ **추적 제외 유지**
- `db/external/omat24/` — Springer Nature 보충자료 ⇒ **추적 제외 유지**

## 🔴 Q9 는 figshare 로 못 닫는다 (2026-08-26 판정 정정)

내가 *"figshare 원자료를 받으면 Q9 가 닫힌다"* 고 했는데 **틀렸다.**
**figshare 가 곧 이 저장소다** — 같은 zip 이고, `RELATED MATERIALS` 가 GitHub 를 가리킨다.
**따로 존재하는 '원자료' 는 없다.**

Q9 = *"배포 CIF 의 Li₂GeS₃ 연결방식(#6·#7·#10)이 논문 `Fig. 3c` 와 어긋난다"* 인데,
어긋나는 두 쪽이 **① 이 배포본**과 **② 논문 그림**이다. 배포본을 다시 봐도 같은 답만 나온다.

**남는 경로는 셋뿐이다:**
| | 무엇 | 가능성 |
|---|---|---|
| **1** | **저자에게 문의** — *"배포 CIF 의 rank 번호가 Fig. 3c 의 rank 와 같은 것인가"* | ★ 가장 확실. 교신저자 `suleechem@skku.edu` |
| 2 | `Fig. 3c` 를 **원해상도로 재판독** — 마커를 우리가 잘못 읽었을 가능성 | 이미 3배 확대까지 봤다. 낮음 |
| 3 | **닫지 않고 캐비앳으로 남긴다** — *"Li₂GeS₃ 는 배포자료로 재현하지 말 것"* | **현재 판정**. 실무상 충분 |

⇒ **당장은 3번으로 유지한다.** 우리 T14(CSM 후처리)에는 영향이 없다 —
그건 `dynamics_Li_CSM.py` 의 **방법**을 쓰는 것이지 Li₂GeS₃ 의 rank 를 쓰는 게 아니다.
