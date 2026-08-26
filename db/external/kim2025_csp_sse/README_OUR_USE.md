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
