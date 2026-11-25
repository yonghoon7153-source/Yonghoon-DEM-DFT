# 끝 보고 — yang2021_atomistic_li_stripping_plating_interface_md (2026-11-24 · litdb-curator)

쓴 파일: `litdb/papers/yang2021_atomistic_li_stripping_plating_interface_md.md` (513 줄 · 표 15 개 칸수 검사 0 건) · `litdb/figures/yang2021_atomistic_li_stripping_plating_interface_md/` (그림 PNG 14 = 도구 12 + 손 크롭 2 · figures.json · 동영상 프레임 jpg 32 — 체크포인트 커밋 b8a8f070 에 이미 들어감 · digest 는 그 뒤 고친 분이 미커밋) · 이 보고 파일. `litdb/figures/_sources.json` 은 추출 도구가 다시 썼다. 다른 공유 파일 · git 은 안 건드렸다.

`build_index.py --check` (rc 1): 이 slug 는 "어느 인덱스에도 없음 [dft]" · "comparison_vs_ours.md 미편입" 두 곳에만 뜬다 (아래 (a) (b) 를 넣으면 풀린다 · rc 1 의 나머지는 배치 전체 미편입 + 기존 INDEX 표 칸수 경고).
웹앱 확인 (읽기만): `_paper_pis` → `[]` · 원소 태그 Li · O · 기법 dft · md · 그림 주석 14 키 (Figure set 행 17 개가 붙음) · `test_v3_literature.py` 20 통과 · `test_webapp.py`+`test_v3_surfaces.py` 의 paper · litdb · figure · claim · element · glossary 20 통과 · `test_recent_digests_are_on_every_litdb_surface` 는 오늘 배치 전부가 INDEX · comparison 미편입이라 실패 (이 편은 'INDEX, comparison_vs_ours' 두 칸만 빠짐 — 그림 칸은 통과).

웹앱 파서에서 찾은 것 (도구 쪽 메모 · 고치지 않았다):
- Figure set 표 첫 칸의 bare 파싱이 `Movie S1` 을 `fS1` 로 읽는다 → 동영상 설명이 Fig. S1 팝업에 잘못 붙는다. 이 digest 는 첫 칸을 `MovieS1` · `MovieS2` 로 붙여 써서 피했다.
- 그림당 주석 상한이 3 개라, 소제목의 `Fig.` 표기가 먼저 자리를 채우면 Figure set 행이 빠진다 (이 digest 의 Fig. 4 가 실제로 0 행이었다 → 소제목 3 곳에서 표기를 빼서 해결).
- Figure set 칸 안의 `\|` 를 webapp 주석 파서는 칸 경계로 자르고, build_index `_row_cells` 는 이스케이프로 본다 — 두 파서가 다르다 (Figure set 표에서는 `\|` 를 안 쓰는 게 안전).

---

## 핵심 (메인 세션 전달용 요약)

- **무엇**: LAMMPS 로 Li 금속 (Nichol–Ackland) | 강체 SE (Li₂O(001) O 끝 = 비정합 · 고정 BCC Li 판 = 정합) 계에서 첫 원자층 Li 를 지우고 (박리) 넣어 (도금) 공극 · 들뜸을 본 MD. W 는 8-6 퍼텐셜 깊이 ε (0.078–0.492 eV) 로 돌린 **모형 손잡이** 0.10–2.00 J m⁻² · P 는 피스톤 외력 0–450 MPa · 300 K · NVE.
- **지도 (`Fig. 5`, 마커 좌표 회수)**: 도금은 W ≳ 0.4 면 무압 안정 (W 0.20 → 300–325 · 0.10 → 425–450 MPa). 박리는 W 0.6 → 0.85 에서 325–350 → 20–30 MPa 로 급락, 0.85–1.4 평탄 20–30, 1.5–1.7 ≤ 10, ≥ 1.8 무압. 정합 계면은 무압 안정 (공공 · <111> 덤벨 주입 → ps 단위로 벌크로).
- **우리에게 가장 날카로운 점**: ① 같은 퍼텐셜의 Li|Li 분리일 0.77 (≈ 2γ_Li) 을 기준으로 Young–Dupré 로 옮기면 도금 무압 경계 W ≈ 0.4 ≈ γ_Li (θ ≈ 88°) 이고, θ = 0° 인 W 0.77 도 박리에는 30–50 MPa 가 든다 → **젖음각만으로는 박리 공극 억제를 말할 수 없다** (보고서 7 절 단서). ② 방법을 옮길 때는 절대 W 가 아니라 **W/W_Li|Li (같은 방법 · 같은 Li 면)** 로 견준다. ③ 임계압은 국부 10⁵–10⁶ A cm⁻² · ns 의 값이라 DEM 에 이식하지 않는다 (경향만).
- **원문 문제**: 본문 요약 "일반 SE 0.6–1.0 J m⁻² → ≈30 MPa" · "0.7–1.4 → 20–30 MPa" 가 자기 지도와 W 0.6–0.8 에서 모순 · `Fig. S6`/`Fig. S7` 그림 뒤바뀜 (캡션 '도금' 그림이 박리 모양) · `Table S1` 의 Li–Li₂O 1.153/1.218 과 본문 'SEI 성분 0.1–0.5' 모순 · 지도의 W 9 개가 ε 표에 없음 · 고전 퍼텐셜 결함 장벽 ≈0.12 eV (`Fig. S4` 기울기) 가 AIMD 45/24 meV 의 2.5–5 배.

---

## (a) INDEX.md 행

넣을 절: **`## 🧲 계면 점착 · 인터레이어 트랙`** 표 끝 (권고 — W_ad 보고서 §7 · DEM 점착 · 압력 입력). 절 머리 조건 'LPSCl 이 한쪽 면' 에 안 맞고, 절 전제 '⛔ G_c 부류' 와 달리 이 편은 **W_ad (분리일 · 모형) 부류**라서 행 안에 둘 다 ⛔ 로 적었다. 대안: `## ✅ Digest 완료 (paper-level)` (build_index 자동 분류 [dft]).
DEM 축 여부: 자동 트랙 판정 (`webapp/data.py::literature_track`, 키워드) 이 **dft** 라서 INDEX_DEM.md (자동 생성 · track == dem 만) 에는 안 뜬다. DEM 쪽에도 띄우려면 `LIT_TRACK_OVERRIDE` 에 'dem' 을 넣어야 한다 (공유 파일 — 메인 판단).

```
| `papers/yang2021_atomistic_li_stripping_plating_interface_md.md` **(본문 12 pp + SI 15 pp + Movie S1 · S2 · 크롭 14장 (도구 12 + 손 크롭 2 `Fig. S1` · `Fig. S2`) 중 그림 13장 전부 실독 · `Table S1` 은 PDF 글자층 · 동영상 프레임 32장 중 18장 실독 · 2026-11-24)** | **[외부·MD+DFT/AIMD·⭐⭐⭐ Li\|SE 박리 공극 · 도금 들뜸의 (W, P) 안정 지도 — W_ad 보고서 §7 · DEM 점착/압력 입력의 원자 원형 · ⛔ W 는 모형 손잡이 (8-6 퍼텐셜 ε → 0.10–2.00 J m⁻²) — 실재 재료값 아님 · W_ad(분리일) 부류라 G_c 행과 같은 줄 금지 · ⛔ 임계압은 MD 속도 (국부 10⁵–10⁶ A cm⁻² · ns) 값 — 이식 금지 · ⛔ 아지로다이트 아님 (강체 Li₂O 모형 SE)]** ✅ Menghao Yang/Yunsheng Liu/Adelaide M. Nolan/**Yifei Mo\*** (Univ. of Maryland MSE · MEI), "**Interfacial Atomistic Mechanisms of Lithium Metal Stripping and Plating in Solid-State Batteries**" — ***Adv. Mater.* 33, 2008081 (2021)**, DOI `10.1002/adma.202008081`. LAMMPS (Nichol–Ackland Li · 강체 SE · 피스톤 외압 · NVE 300 K · 대형 > 10⁷ 원자 · 지도는 소형 3.6×10⁵) · 비정합 = Li₂O(001) O 끝 \| Li(001) (Born–Mayer + 8-6) · 정합 = 고정 BCC Li 판 (W 0.77 = Li\|Li 분리일). 박리 = 첫 층 Li 삭제 · 도금 = 삽입 · 공극 판정 = SE 위 3 Å 접촉층 원자 수비. 비정합 W 0.77 · 0 MPa: 1.6 ns (Q 0.28 µAh cm⁻² · 국부) 공극 핵생성 → 3.6 ns 지름 20 nm · 50 MPa 로 억제. `Fig. 5` (마커 좌표 회수): 도금 무압 W ≳ 0.4 (0.20 → 300–325 · 0.10 → 425–450 MPa) · 박리 W 0.6 → 0.85 에서 325–350 → 20–30 MPa 급락 · 0.85–1.4 평탄 20–30 · 1.5–1.7 ≤ 10 · ≥ 1.8 무압 · 정합은 무압 안정 (공공 · <111> 덤벨 주입). Li 결함 DFT/AIMD: 공공 0.497 eV / 45 ± 23 meV · 침입형 0.593 eV / 24 ± 21 meV · D_Li 3.05×10⁻¹¹ cm² s⁻¹. ⚠ 본문 요약 "0.6–1.0 J m⁻² → ≈30 MPa" 는 자기 지도와 W 0.6–0.8 에서 모순 · `Fig. S6`/`S7` 그림 뒤바뀜 · `Table S1` Li₂O 1.15–1.22 vs 본문 'SEI 0.1–0.5' 모순. ⚠ 같은 해 Yang & Qi *Chem. Mater.* 2021 (`yang2021_flat_li_stripping_lithiophilic_interface_design`) 과 다른 논문 | 점착 트랙 (W_ad 부류 · 모형 손잡이) · Li\|SE 박리 공극 · 도금 들뜸 (W, P) 지도 · Li 결함 수송 |
```

## (b) comparison_vs_ours*.md

build_index 는 두 비교 파일 중 **한 곳에만 slug 가 있어도 편입**으로 센다 (`build_index.py` 444–448 행). 아래 ①–③ 이 comparison_vs_ours.md (DFT 트랙), ④ 는 DEM 쪽 선택.

① `📑 Reference key` 표 행 (4 칸):
```
| **[YangMo21MD]** 🔧 **방법 원전 (Li\|SE 계면 MD · (W, P) 안정 지도) · ⛔ 아지로다이트 값 0 — A–D 물성 4축에 행을 만들지 않는다** (§E 정성 1 행 · §J-88) | Menghao Yang/Yunsheng Liu/Adelaide M. Nolan/**Yifei Mo\*** (Univ. of Maryland) 2021 ***Adv. Mater.* 33, 2008081** (DOI 10.1002/adma.202008081) — "Interfacial Atomistic Mechanisms of Lithium Metal Stripping and Plating in Solid-State Batteries" | ✅ `papers/yang2021_atomistic_li_stripping_plating_interface_md.md` (2026-11-24 · 그림 13 장 + 표 1 · 동영상 프레임 18 장 실독) | MD (LAMMPS · 고전) + DFT/AIMD (Li 벌크 결함) · 🔧 §J-88 |
```
⚠ `[Yang21…]` 키가 형제 편 (Yang & Qi 2021) 과 겹치지 않게 `[YangMo21MD]` 로 했다.

② `## E. 환원 / 음극(Li 금속) 계면` 표 행 (4 칸 · 주장 | 출처 | 우리 | 일치):
```
| **🆕 (2026-11-24) Li\|SE 박리 공극은 '첫 접촉층에서 지운 Li 를 확산 · 크리프가 못 채울 때' 생긴다 — 강체 · 불활성 SE 의 MD (W, P) 지도: 도금 들뜸은 W ≳ 0.4 J m⁻² 면 무압으로 막히지만 박리 공극은 W 0.77–1.4 에서도 20–50 MPa · 무압은 W ≥ 1.8 · Li 와 정합인 계면은 결함 주입 (공공 · <111> 덤벨) 으로 무압 안정** — ⚠ W 는 모형 손잡이 · 임계압은 MD 속도값 (국부 10⁵–10⁶ A cm⁻² · ns) · 우리 Li\|LPSCl (반응 계면 · SEI) 과 다른 계 | **[YangMo21MD]** `Fig. 5` (마커 좌표 회수) · `Fig. 3` · `Fig. 2` | 우리 Li 금속 쪽 계산 (환원 · SEI) 은 이 축 값 없음 — W_ad 보고서 §7 (Li 친화성 · Young–Dupré 제안) 의 기준 그림 · 견줄 때는 W/W_Li\|Li 비로만 | 정성 (방향만) |
```

③ `### J-88` 블록 (번호는 확인 당시 마지막이 J-87 — 합칠 때 다음 빈 번호로):
```
### J-88. 🔧 **방법 원전 — [YangMo21MD] Li|SE 계면 MD 의 (W, P) 안정 지도 (*Adv. Mater.* 33, 2008081 (2021)): W 는 모형 손잡이 · 공극 판정 = 접촉층 원자 수비 · 임계압은 MD 속도값** (2026-11-24 신설)

> **무엇을 주나.** 강체 SE (Li₂O(001) O 끝 · 비정합 / 고정 BCC Li · 정합) | Li 금속 MD 에서 박리 공극 · 도금 들뜸이 안 생기는 (W, P) 영역 (`Fig. 5`). W 는 8-6 퍼텐셜 깊이 ε 로 돌린 0.10–2.00 J m⁻², 같은 틀의 Li|Li 분리일 0.77 J m⁻² (≈ 2γ_Li).
> **우리 축에 닿는 곳.** ① W_ad 보고서 §7 의 Young–Dupré: 도금 무압 경계 W ≈ 0.4 ≈ γ_Li (θ ≈ 88°) · 박리는 θ = 0° 인 W 0.77 도 30–50 MPa → 젖음각은 박리 공극 억제의 판정 기준이 못 된다. ② 방법을 옮길 때는 W/W_Li|Li (같은 방법 · 같은 Li 면) — 우리 Li|X 를 내면 Li|Li 분리일을 같이 낸다. ③ Li 결함 상수 (DFT/AIMD · 외부값) 는 연속체 공공 확산 입력 후보.
> ⛔ **금지.** W 0.1–2.0 을 재료값으로 · 임계압 20–450 MPa 를 실험 · DEM 적층압으로 · 본문 요약 "0.6–1.0 J m⁻² → ≈30 MPa" (자기 지도와 모순) · `Fig. S6`/`S7` 캡션 그대로 (그림 뒤바뀜) · 우리 W_ad 값과 같은 줄.
```

④ (선택 · DEM 점착 트랙) `comparison_vs_ours_DEM.md` §I 끝 `### I-11` 블록:
```
### I-11. `yang2021_atomistic_li_stripping_plating_interface_md` — ★★★ Li|SE 박리 공극 · 도금 들뜸의 **원자 (W, P) 안정 지도** — **W_ad 부류 (분리일 · 모형 손잡이)** 라 G_c 행 (I-1 Liao 등) 과 같은 줄 금지 · 임계압은 MD 속도값

> **무엇을 주나.** P_c(W): 도금 W ≳ 0.4 무압 · 박리 W 0.6 → 0.85 에서 325–350 → 20–30 MPa · 0.85–1.4 평탄 20–30 · ≥ 1.8 무압 (`Fig. 5` 마커 회수 · 국부 1.6 nA nm⁻² · 300 K · 소형 셀 · 점마다 1 런).
> **★ 우리 축에 닿는 곳.** ① DEM 박리 시험 대조로는 **경향만** (P_c(W) 단조 감소 · 박리 경계가 도금보다 높은 W) — 절대 MPa 는 국부 10⁵–10⁶ A cm⁻² · ns 의 값. ② 이 논문에서도 P 는 Li 크리프를 통해서만 들어간다 — '적층압은 원자 W 가 아니라 DEM 층의 변수' 라는 §I 전제와 같다. ③ 압력만으로는 공극이 느리게 닫힌다 (`Fig. S8` · 100–400 MPa · 40 ns 에 다 못 닫음) — DEM 에서 '압력이 즉시 접촉을 회복' 가정 금지.
```

## (c) pdf_map.tsv

**필요 없다** — digest 를 쓴 뒤 `extract_figures.py --inbox --only yang2021` 매칭표에서 이 편이 '1쪽 본문 69%' 로 `yang2021mo_li_strip_plate_md_main.pdf` · `_SI1.pdf` 에 맞게 붙고, 형제 Yang & Qi 편은 '제목 100%' 로 따로 붙는다. 두 'Yang 2021' 이 섞일 위험에 대비해 넣는다면 (선택):
```
yang2021_atomistic_li_stripping_plating_interface_md	yang2021mo_li_strip_plate_md
```
(.mov 두 개는 그림 도구가 안 본다 — 프레임은 ffmpeg 로 따로 뽑았고 명령은 figures.json `movies` 블록과 digest §9 에 적었다.)

## (d) 추가로 먹일 만한 논문 (8 편)

⚠ 인용 API (Semantic Scholar · OpenAlex) 가 프록시에서 막혀 (403 · 연결 거부) **2024–2026 후속을 조회하지 못했다.** 이번 배치가 이미 Sandoval 2025 · Lu 2026 · Metzler 2025/2026 · Shi 2026 · Cicvarić 2026 · Kim 2026 · Chatterjee 2025 를 덮고, Sakamoto 계열 (Sharafi 2017 · Wang 2019 · Masias 2019 · Lee 2022 · Kazyak 2020) 과 Seymour 2021 · Fuchs 2023 · Wang 2020 도 이번 배치에 있어서 뺐다. 아래는 이 논문 참고문헌 (서지 = PDF 확인) 과 제가 아는 후속 (서지 '확인 필요' 표시) — 최근 것 먼저.

| # | 논문 | 왜 | litdb |
|---|---|---|---|
| 1 | Singh, D. K. 외 (Janek 그룹), "Origin of the lithium metal anode instability in solid-state batteries during discharge", *Matter* 6, 1463 (2023) — 서지 확인 필요 | **방전 중 공극** · Li 확산 한계 실험 — 이 논문의 '공급 부족 공극' 그림의 실험 쪽 | 없음 (dixit2022 리뷰에 언급만) |
| 2 | Lewis, J. A. 외 (McDowell 그룹), "Linking void and interphase evolution to electrochemistry in solid-state batteries using operando X-ray tomography", *Nat. Mater.* 20, 503 (2021) — 서지 확인 권장 | **방전 중 공극**의 operando 3D 실측 · 공극 부피 ↔ 분극 | 없음 (리뷰 여러 편에 언급만) |
| 3 | Lee, Y.-G. 외, "High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes", *Nat. Energy* 5, 299 (2020) — 이 논문 ref 2 | **Ag–C 층 원전** (우리 W_ad 보고서의 대상 층) | 없음 · `_curation/wishlist.md` 에 [n] 으로 여러 번 |
| 4 | Kasemchainan, J. 외 (Bruce 그룹), "Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells", *Nat. Mater.* 18, 1105 (2019) — ref 12 | 박리 임계 전류 < 도금 · **차폐 공극** 실측 — 이 논문이 가장 많이 기대는 실험 | 없음 (리뷰 10 편에 언급) |
| 5 | Krauskopf, T.; Hartmann, H.; Zeier, W. G.; Janek, J., *ACS Appl. Mater. Interfaces* 11, 14463 (2019) (Li \| LLZO 전기화학–역학 연구 · 제목은 기억 — 확인 권장) — ref 24 | 이 논문이 '35 MPa 일치' 를 댄 실험 — 우리 쪽에서 그 비교를 다시 볼 때 원전 | 없음 |
| 6 | Krauskopf, T.; Mogwitz, B.; Rosenbach, C.; Zeier, W. G.; Janek, J., "Diffusion limitation of lithium metal and Li–Mg alloy anodes on LLZO type solid electrolytes as a function of temperature and pressure", *Adv. Energy Mater.* 9, 1902568 (2019) — SI ref 10 | **합금 (Li–Mg) 정합 계면**의 실험 근거 · Li 확산 한계의 온도 · 압력 의존 — Ag–Li 합금층 가설 (digest §12-4) 의 대조 | 없음 |
| 7 | Lepley, N. D.; Holzwarth, N. A. W., "Modeling interfaces between solids: Application to Li battery materials", *Phys. Rev. B* 92, 214201 (2015) — SI ref 3 | **DFT 계면 W 계산법** · `Table S1` 의 Li \| Li₂O 1.153/1.218 · Li \| Li₃PO₄ 원전 | 없음 (wishlist 에는 같은 저자 *PRB* 88, 104103 (2013) 만) |
| 8 | Liu, Z.; Qi, Y.; Lin, Y. X.; Chen, L.; Lu, P.; Chen, L. Q., "Interfacial study on solid electrolyte interphase at Li metal anode: implication for Li dendrite growth", *J. Electrochem. Soc.* 163, A592 (2016) — SI ref 4 | Li \| LiF · Li \| Li₂CO₃ 의 DFT W (`Table S1` 원전) · 점착 ↔ 덴드라이트 · Qi 그룹 계보 (형제 Yang & Qi 2021 의 앞 편) | 없음 |

대안 한 편: Gao, B.; Jalem, R.; Tateyama, Y., *ACS Appl. Mater. Interfaces* 12, 16350 (2020) — Li \| LLZO W 0.67–0.98 (SI ref 2 · `Table S1` 원전). 위 8 편에 Jeff Sakamoto 공저는 없다 (그의 편은 이번 배치에 이미 있다).

## (e) DEM-DFT 보고서에 쓸 거리 (W_ad 보고서 7 절 + 연속체 · DEM 입력)

전부 강체 · 불활성 SE 모형 · 300 K · MD 속도 (국부 10⁵–10⁶ A cm⁻² · ns) 한정. 쪽 = PDF 쪽 (본문 = 인쇄 '(n of 12)' · SI = 인쇄 쪽 +1).

| # | 쓸 점 | 위치 | 직접 봤나 |
|---|---|---|---|
| 1 | **Young–Dupré 기준점** — 같은 퍼텐셜의 정합 Li \| Li 분리일 W = 0.77 J m⁻² = 완전 젖음 (W = 2γ_Li) 기준 · γ_Li ≈ 0.385 J m⁻² 로 읽힘 (우리 해석 · 논문은 γ_Li 미기재) | 본문 p2 §2.1 · p10 Methods · `Fig. 1c` · `Fig. S1b` | 봄 |
| 2 | **친Li 경계 ↔ 도금 무압 경계** — W ≈ 0.40 ≈ γ_Li (θ ≈ 88° · 우리 산수) 에서 도금 들뜸이 무압으로 사라짐 · W 0.10 → 138° · 0.20 → 119° · 0.30 → 103° · 0.60 → 56° · 0.70 → 35° | p8 §2.6 · `Fig. 5a` (마커 회수) · `Fig. 4g` | 봄 |
| 3 | **점착 문턱 (박리)** — θ = 0° 인 W 0.77 도 30–50 MPa · 0.85–1.4 → 20–30 MPa · 1.5–1.7 → ≤ 10 · 무압은 W ≥ 1.8 (≈ 2.3 W_Li\|Li) → 보고서 문장 '젖음각은 도금 · 젖음 순서 지표이고, 박리 공극은 W 와 Li 수송 · 압력이 같이 정한다' 의 근거 · 0 MPa 에서는 W 가 '버티는 용량' 만 늘림 (개시 Q ≈ 0.07 → 0.47 µAh cm⁻² for W 0.40 → 0.80) | p8 · `Fig. 5b` (+삽도) · `Fig. 3d,e` | 봄 |
| 4 | **공극 억제 기전** — 지운 접촉층을 확산 · 크리프가 채우는 속도 경주 · 정합 계면은 공공 · <111> 덤벨을 주입 (홉 대기 ≈ 0.57 / 0.25 ps · ν₀ 10¹³ 가정) · 비정합 비정질 첫 층은 흡수원 · 전위 오름 = 크리프 | p3–5 · `Fig. 2` · `Fig. 3a–c` · `Fig. 1e–h` · Movie S1/S2 | 봄 (영상은 각 9 프레임) |
| 5 | **차폐 공극 · 압력만의 느린 회복** — 삼중점 도금으로 공극이 Li 안에 갇힘 · 100–400 MPa (항복 0.8 MPa 의 100 배+) 도 40 ns 에 못 닫음 → 연속체에서 '도금이 공극을 메운다' · DEM 에서 '압력이 즉시 접촉 회복' 가정 금지 | p7–8 · `Fig. 4e` · SI p13 Note 4 · `Fig. S8` | 봄 |
| 6 | **계산 설정 대조** — W 정의 식 3 (뗀 쪽 이완 · 0 K/300 K · 끝점 미기재) 대 우리 고정 기하 W_sep (10 Å · 이완 없음 · D3) · 계면 = Born–Mayer (컷오프 5 Å) + 8-6 (r_m 2.0 Å · 컷오프 10 Å) · ε → W 16 줄 (W 는 ε 에 초선형) · Li(001) 면 (우리 7 절 제안 Li(100) 과 같은 면) | p10 (식 1–3 은 쪽 렌더로 확인) · `Fig. S1` | 봄 |
| 7 | **방법 옮길 때 W/W_Li\|Li 정규화** (우리 제안) — 우리 Li \| X 를 낼 때 같은 방법 Li \| Li 분리일을 같이 → 경계 비: 도금 무압 ≈ 0.52 · 박리 30–50 MPa 1.00–1.04 · 20–30 MPa 1.10–1.82 · 무압 ≥ 2.34 | digest §7c (`Fig. 5` 기반) | 봄 |
| 8 | **DEM 입력 — 압력** — 경향만 (P_c(W) 단조 감소 · 박리 > 도금) · 절대 MPa 이식 금지: MD 국부 1.6×10⁵–5.1×10⁶ A cm⁻² 대 실험 ≤ 1 mA cm⁻² (실접촉 10⁻⁶–10⁻³ 을 감안해도 ≥ 10² 배) · 관측창 (300 K · ≤ 40 ns · n = 1 · ν₀ 10¹³ 가정): 기대 사건 1 ≈ 0.33 eV (검출 63 %) · 95 % 검출 ≈ 0.31 eV | p2 · p10 | 텍스트 |
| 9 | **DEM 입력 — 점착** — 실재 Li \| X 의 W 는 `Table S1` 문헌 DFT 뿐 (LLZO 0.67 / 0.67–0.98 · LiOH 0.19 · Li₂O 1.153 / 1.218 · Li₂CO₃ 0.100–0.167 · Li₃PO₄ 0.481–1.153 · LiF 0.065–0.093 · 방법 제각각 소환값) | SI p4 | PNG 안 열고 쪽 렌더 + 텍스트 |
| 10 | **DEM · 연속체 입력 — Li 물성 (외부값)** — 공공 E_f 0.497 eV · E_m 45 ± 23 meV · 침입형 (<111>) 0.593 eV / 24 ± 21 meV · 고전 300 K D_V 6.1×10⁻⁵ · D_I 1.4×10⁻⁴ cm² s⁻¹ · D_Li = C_eq D_V = 3.05×10⁻¹¹ (실험 5–9×10⁻¹¹) · C_eq 5×10⁻⁷ (문헌) · 항복 0.8 MPa (SI 서술 · 출처 없음) | SI p5 `Fig. S2` · p6 `Fig. S3` · p7–9 Note 3 + `Fig. S4` · p13 | 그림 봄 · 수치는 텍스트 |
| 11 | **주의** — 고전 퍼텐셜의 결함 이동 장벽 ≈ 0.12 eV (`Fig. S4` 기울기 · figure-read) 가 AIMD 의 2.5–5 배 → MD 지도의 확산이 DFT 보다 느릴 수 있음 · NVE 온도 미보고 · 판정 문턱 · 반복 수 미기재 | `Fig. S3` · `Fig. S4` · p10 | 봄 |

## (f) 그림 · 동영상 크롭 요약

- 도구 크롭 12 (`Fig. 1`–`5` · `Fig. S3`–`S8` · `Table S1`) · 놓친 2 (`Fig. S1` · `Fig. S2` — 그림과 표가 한 쪽에 섞인 SI 쪽이라 '영역 없음') → 손 크롭 2 (figures.json `manual_crop` 사유 · `missing_labels` 에 `resolved`) = **14 항목 · 오탐 0**. `fig_S3.png` 가 작은 것은 원본 래스터가 346×260 px 라서 (정상).
- 본 것: 그림 13 장 전부 + `Fig. 5` 패널 2배 확대 · 마커 중심 색 분할로 (W, P) 시험점 회수. `Table S1` 은 SI 쪽 렌더 + PDF 텍스트 (PNG 미개봉 · figures.json `viewed: false`).
- 동영상: movie1 17 장 · movie2 15 장 (5 s 간격 jpg 32 장 · figures.json `movies` 블록) 중 각 9 장 실독 — S1: 001 · 003 · 005 · 007 · 009 · 011 · 013 · 015 · 017 / S2: 001 · 003 · 005 · 006 · 008 · 010 · 012 · 014 · 015. 시간 · 축척 표시 없음.
- 프레임 시각 정정: 처음에 '프레임 k ≈ (k−1)×5 s' 로 적었다가 **(k − 0.5)×5 s** 로 고쳤다 (digest §5.8 의 시각 5 곳 · §9 각주 · figures.json `movies.note`). 직접 실측 — `-ss` 정지 화면 0.1 s 간격과 MSE 대조: 001 = 2.4 s (MSE 0) · 010 = 47.4 s (MSE 0) — fps 필터가 10 fps 영상의 5 s 칸마다 마지막 프레임을 남긴다. 기술 내용 (무엇이 보이나) 은 안 바뀐다.
- 원문 오류 발견: `Fig. S6` / `Fig. S7` 그림 – 캡션 뒤바뀜 (캡션 '도금' 그림에 cyan 없이 슬랩이 얇아짐 · 두께 변화가 18.9 nA nm⁻² × 4 ns ≈ 10 nm 와 맞음) · `Fig. 5b` 의 W ≈ 0.735 등 9 개 W 가 `Fig. S1b` ε 표에 없음.
- 공용 scratch 점검: 처음 텍스트를 `scratchpad/yang/main.txt` · `si.txt` (slug 가 아닌 겹칠 수 있는 이름) 에 뽑아 읽었다 → PDF 에서 `scratchpad/<slug>/` 로 다시 뽑아 **md5 대조 = 두 파일 모두 바이트 동일** · 제목 · 저자 · DOI · '(n of 12)' 쪽 표기 확인 · digest 수치 50 여 개를 새 텍스트에서 공백 정규화 뒤 재대조 = **미스 0** (본문 p1–4 · SI p3–5 · p11–12 는 PDF 쪽 렌더로도 직접 봤다).

## (g) Jeff Sakamoto

**저자 아님** (Menghao Yang · Yunsheng Liu · Adelaide M. Nolan · Yifei Mo). 참고문헌에만 나온다 — ref 16 (Sharafi 2017) · 23 (Wang 2019 *Joule*) · 28 (Wang 2019 *Electrochim. Acta*) · 34 (Masias · *J. Mater. Sci.* 54, 2585) · 43 (Wang 2018 *J. Power Sources*) · SI ref 1. INDEX 행에 🏷 배지를 달지 않는다. digest 머리말 35 줄에 그 이름 (과 Zeier · Ceder 등 등록 별칭) 을 안 넣어 웹앱 배지 오탐이 없다 (`_paper_pis` = `[]`).
