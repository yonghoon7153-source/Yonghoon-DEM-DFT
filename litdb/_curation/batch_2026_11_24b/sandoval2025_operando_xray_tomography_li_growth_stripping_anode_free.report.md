# 끝 보고 — sandoval2025_operando_xray_tomography_li_growth_stripping_anode_free (배치 2026-11-24b · #7)

- digest: `litdb/papers/sandoval2025_operando_xray_tomography_li_growth_stripping_anode_free.md` (새 파일 · 639 줄 · 한국어 standalone · 세 줄 경고 + 요약 바로잡기 + §0–§16 · Figure set 표 + Video set 표 · 파생 계산 원장 §14)
- 그림: `litdb/figures/sandoval2025_operando_xray_tomography_li_growth_stripping_anode_free/` — 크롭 14 장 (본문 그림 6 + SI 그림 8 · 이 논문엔 표가 없어요) 전부 도구 한 번 (`--slug … --pdf 본문 SI --clean`) · 손 크롭 0 · 다시 자름 0 · 번호 공백 0 (`missing_labels` = []). `figures.json` 에 14 장 전부 `viewed` / `viewed_how` · 캡션 7 개 정리 (합자 fi · ff · 줄바꿈 하이픈 — 원문은 `caption_raw`) · `hand_notes` 3 줄.
- 영상: 다섯 개를 SI 영상 설명 (SI p. 14) 과 첫 장면으로 맞췄어요 — **sup4 = Video S1 · sup5 = S2 · sup6 = S3 · sup7 = S4 · sup8 = S5**. 프레임 JPG **58 장**을 `video_frames/` 에 남겼어요 (sup4 · 5 · 6 각 9 · sup7 17 = 0.5 s 간격 + 끝 장면 · sup8 14 = 프레임 차이로 찾은 다른 장면 13 개 전부 + 끝). 보기는 전 프레임 대조표 (scratch) + 확대로 했어요. ffmpeg 명령은 digest §7b 에 있어요.
- 원자료: sup1 'Summary' (세 셀 전압 133,277 행) · sup2 'Case A' · 'Case B' 를 openpyxl 로 읽어 단계 길이 · 두께 · 균열 부피를 본문 · 그림과 대조했어요 (digest §3.2 · §3.7 · §14).
- 공유 파일은 안 건드렸어요. `litdb/figures/_sources.json` 은 추출 도구가 이 slug 항목을 더해 다시 썼어요 (손 안 댐). git 작업 없음 — 메인 체크포인트 `7a9f8c62` · `98271324` 에 크롭 14 장 · 영상 프레임 58 장 · `figures.json` (viewed 판) 이 이미 들어가 있고, 그 뒤 `figures.json` 의 '57 JPG' → '58 JPG' 한 줄만 고쳐서 지금 수정 상태예요 · digest 는 미추적이에요.
- 점검 (읽기만): `build_index.py --check` → 이 digest 는 **[dem]** 으로 분류돼 "어느 인덱스에도 없음" + "`comparison_vs_ours_DEM.md` 미편입" (아래 (a) · (b-3) 을 넣으면 풀려요) · `extract_figures.py --inbox --only sandoval2025` (매칭표만) → 본문만 `[1쪽 본문 49%]` 로 붙고 **SI (`…_sup3.pdf`) 는 짝 못 찾음** → (c) 한 줄 필요 · `--audit` 경고 없음 (본문 6 · SI 8 · 표 0) · `--audit-src` 깨끗 · 웹앱 `paper_pis` = [] · `paper_figures` 14 · `paper_figure_notes` 14/14 · 원소 페이지 Li · P · S · Cl · Cu · Ag · Au 연결 ✓ · 기법 태그는 없음 (`methods: —` · 해당 기법 0) · 시험: `test_v3_literature` + `test_v3_markdown` 43 통과 · `test_webapp -k "sakamoto or litdb_figure or recent_digests or digest_date or element_papers or glossary_papers or figure_comment or video"` 7 통과 1 실패 = `test_recent_digests_are_on_every_litdb_surface` (이 묶음 전체가 INDEX · comparison 미편입 — 합치면 풀려요 · 그 시험은 두 INDEX · 두 comparison 파일 어디든 slug 가 있으면 통과해요).

⚠ **메인에 알릴 것**
1. **질문 4 답: 인터레이어가 있어요 — 맨 집전체 결과가 아니에요.** 세 셀 모두 10 µm Cu 위 100 nm **Au (A · C) · Ag (B)** (전자빔 증착 · SI p. 2) 이고 상대극은 Li 금속 (반쪽 셀) 이에요. 탄소 층은 없어요. 맨 Cu 대조 셀도 없어서, 같은 꼴 (Li \| LPSC \| Cu · operando CT) 에 **맨 Cu 대 Ag/Cu** 를 비교한 Xu 2026 *Small* 을 (d) 1 순위로 올렸어요.
2. **요청 요약의 '필라멘트가 원래 기공을 따라 자란다' 는 논문 주장과 반대예요.** 논문은 "*grow around pre-existing pores … rather than lithium filling these pores*" (초록) — 새 균열이 기공 **옆**에서 나며 원래 기공을 **닫아요** (`Fig. 2d,e` · 영상 S2 #9 → #16 으로 직접 봤어요). 저자가 "채우는 경우를 배제하지 않는다" 는 단서를 달았어요. '박리로 일부 되돌아간다' 는 맞아요 (새 균열 부피 ≈ 20 % 잔류).
3. **원자료 sup2 'Case A' 시트는 `Fig. 3c` 가 아니에요.** 시트는 82.6 → 243.5 × 10⁴ µm³ · 그림 · 본문은 266 → 461 × 10⁴. 시트 t = 0 값이 작은 부분 부피 (1116 × 368 × 364 µm · `Fig. S3b` 치수) 의 정확히 0.553 % (본문 '0.55 %') 이고, 그림 40 점 픽셀 판독 − 시트가 처음 ≈ 182 × 10⁴ 로 거의 일정하다가 6 h 근처만 217 로 커져서 '깊은 쪽 기공 + 늦게 자란 균열' 로 읽혀요 → **시트 = 집전체 쪽 작은 부분 부피**로 판정했어요 (✎). '≈ 20 % 잔류' 는 두 쪽 다에서 재현돼요 (그림 17–21 % · 시트 19.9 %).
4. **Case B 첫 박리 CE 92.9 % 가 원자료로 재현되지 않아요.** 전압이 양수인 박리 단계는 6.076 h (0.5 mA cm⁻² 면 3.04 mAh cm⁻² · CE 101 %) 이고, 첫 0.497 h (10 s 간격 기록 구간) 를 빼야 본문 (2.79 · 93.0 %) 과 맞아요. 그런데 그 구간 전압 (+0.080 V) 이 전류가 흐를 때 값과 같고 WE 두께도 6 → 7 h 에 −2.39 µm (1 시간 전류면 −2.43) 줄어서 전류가 흐른 쪽에 가까워요. 전류 열이 없어 판정은 못 했고, B 의 CE · '≈ 0.2 mAh 남음' 은 정밀값 인용 금지로 digest §13 에 걸었어요.
5. **'고전류에서 계면이 거칠어진다' (초록 주장) 의 근거가 약해요.** WE 두께의 절대 sd 는 2.60 → 2.76 → 3.28 µm 로 늘지만 CV 는 17.3 → 15.9 → 15.4 % 로 줄어요. 저전류 8 점의 sd–두께 추세 위로 확실히 벗어나는 건 단락 순간 마지막 한 점 (+0.42 µm) 뿐이에요 (✎ digest §3.5 · §14-7).
6. **`Fig. 1d` · `1e` 는 세로로 ≈ 1.4 배 늘어난 것으로 보여요.** 그 패널 막대로 재면 SE 두께 B 1.15 · C 1.54 mm 인데, 같은 셀의 원복셀 영상 (Video S4 · 1.70 µm px⁻¹ · 셀 폭 1.92 mm 로 축척 검증) · SI 단면 · `Fig. 6a` 는 B ≈ 0.82 · C ≈ 1.10–1.14 mm 예요. A 는 `Fig. 1c` 1.43 · `S1` 1.40 mm 로 맞아요. SE 두께 · 펠릿 밀도 · 기공률 · 온도는 본문 어디에도 없어요.
7. **영상에서만 본 것**: B 의 왼쪽 가장자리 렌즈 모양 균열이 **첫 0.5 mA cm⁻² 증착 초반 (Video S4 #6)** 부터 생겨 박리 뒤에도 남고, 마지막 사선 균열이 그 자리에서 뻗어요 — 본문은 가장자리 효과를 고전류 서술에만 붙였어요. Video S5 의 첫 균열 장면 (13 개 중 7 번째) 과 `Fig. 6a(ii)` (0.75 단계 뒤) 의 시각은 안 맞는데 영상에 시각 표지가 없어 판정 못 했어요.
8. 본문 안 숫자 엇갈림: 1.5 mA cm⁻² 단계 0.75 (p. 1812) 대 0.80 (p. 1816 · `Fig. 4e`) 대 원자료 0.83 ✎ · 주사 '≈ 5 분' 대 1200 × 400 ms = 8 분 ✎ · '면적 ≈ 75 % (지름 ≈ 1.5 mm)' — 75 % 는 지름 비 (면적 56 %) · 분말 '두 입도' (본문) 대 '세 분말 · 두 회사' (SI).
9. 이 묶음 #8 Ko 2025 *Nat. Commun.* · #9 Lee Y.-G. 2020 *Nat. Energy* (ref 4) · #10 Kasemchainan 2019 (ref 23) 는 (d) 에서 뺐어요. **Kotakadi 2025 *Joule* 9, 102175** 는 baer2026 보고 (d) #1 의 ChemRxiv 판이 저널에 실린 판이에요 (Crossref 'has-preprint' 확인).
10. `extract_figures.py --clean` 을 이 slug 로 다시 돌리면 `video_frames/` 가 지워져요 (`hand_notes` 에도 적었어요).
11. 발견 검색 (최근 2 년 먼저): Crossref 주제어 검색 4 번 + 저자 검색 1 번 + DOI 조회 16 번 (서로 다른 DOI 10 개 · 서지 · 초록 확인) (일반 UA · 개인정보 없음 · 실패 0).
12. W_ad 보고서 8 절 머리 · INDEX 🌱 절 머리가 '18 편 한 묶음' 이라 이 묶음 (11-24b) 을 넣으면 그 문구도 같이 고쳐야 할 거예요 (baer 보고 6 과 같은 얘기).

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` — 행 순서상 **'무음극 핵생성 · 성장' 묶음** · `sandoval2025_electro_chemo_mechanics_anode_free_ssb` 행 (지금 802 행) **바로 다음** · Ag/C 인터레이어 행 (`metzler2025_…`) 앞이에요. Jeff Sakamoto 저자가 아니라 🏷 를 달지 않아요.

| `papers/sandoval2025_operando_xray_tomography_li_growth_stripping_anode_free.md` **(본문 13 pp + SI 14 pp + 원자료 xlsx 2 + 영상 5 · 크롭 14장 (그림 14 · 표 0 · 전부 도구 · 번호 공백 0) 전부 원해상도 실독 · 영상 프레임 58장 저장 (5 편 전 프레임 대조표로 봄) · 원자료로 단계 길이 · 두께 · 균열 부피 대조 · 2026-11-24)** | **[외부·exp(operando 싱크로트론 μCT + 정전류)·⭐⭐ LPSCl 무음극 Li 석출 · 박리의 3D 정량 · ⛔ 맨 Cu 아님 (Au · Ag 100 nm/Cu) · 계산 0 · A–D 물성 4축 진입 금지]** ✅ **Stephanie Elizabeth Sandoval**/Douglas Lars Nelson/Hari Sridhara/Talia A. Thomas/John A. Lewis/Kelsey Anne Cavallaro/Pavel Shevchenko/Neil P. Dasgupta/Francois L. E. Usseglio-Viretta/Donal P. Finegan/**Matthew T. McDowell\*** (Georgia Tech · Argonne APS · Michigan · NREL), "**Visualizing diverse lithium growth and stripping behaviors in anode-free solid-state batteries with operando X-ray tomography**" — ***EES Batteries* 1, 1809–1821 (2025)**, DOI `10.1039/D5EB00111K` (CC-BY-NC 4.0). Li \| Li₆PS₅Cl \| (Au 또는 Ag 100 nm)/Cu 반쪽 셀 셋 (지름 2 mm · 225 MPa 압착 · ≈ 10 MPa · 온도 미기재 · 복셀 1.4–1.8 µm · 15 분 간격). **A** (굵은 < 100 µm · \|V\|/j ≈ 890 Ω cm² ✎): 0.5 mA cm⁻² · 3 mAh cm⁻² 에서 집전체 계면 전체에 Li 로 찬 균열 · 큰 부분 부피 기공 + 균열 266 → 461 × 10⁴ µm³ (같은 발자국 Li 의 49 %) · 균열이 원래 기공 옆에서 나며 기공을 닫음 · 박리로 끝부터 줄지만 새 균열 ≈ 20 % 잔류 · CE 79.9 %. **B · C** (고운 1–5 µm · ≈ 170–200 Ω cm² ✎): 평평한 막 14.2 ± 2.4 µm (이론 14.5) → 1.5–3.0 · 0.75–2.0 mA cm⁻² 에서 **가장자리** 필라멘트 · 단락 (C 누적 6.37 mAh cm⁻²). 🔴 원자료 'Case A' 시트 = 작은 부분 부피 (≠ `Fig. 3c`) · B CE 92.9 % 원자료로 재현 안 됨 · `Fig. 1d,e` 세로 ≈ 1.4 배 · 'roughening' 은 절대 sd (CV 는 감소) · '0.55 %' 는 해상 기공 분율 (펠릿 밀도 · 기공률 · SE 두께 없음) | 점착 트랙: W_ad 보고서 8-4 'Li 로 찬 균열이 열리며 자란다' 의 LPSCl 3D 근거 · 박리 중 Li–LPSC 점착 탓 새 균열 (`Fig. 3b` · Li \| LPSCl W 자리 · 값 없음) · DEM 대조 표적 T1–T10 (해상 기공 · 기공 자리 · '연결 기공 ≠ Li 길' · 가장자리 · 두께 CV · 분극) — 보정 금지 · 이웃 `kazyak2020_…` · `sandoval2025_electro_chemo_…` · `kim2026_operando_void_…` · `shi2026_…` · `doux2020_stack_pressure_assb` |

---

## (b) `comparison_vs_ours*.md` 에 넣을 줄

**A–D 물성 4축: 본 자리는 없어요** (실험 전용 · σ · Ea · 탄성 · 띠틈 값 0). `build_index.py --check` 가 **[dem]** 으로 분류하니 **실제 집은 b-3 (`comparison_vs_ours_DEM.md` §I)** 이고, b-1 · b-2 는 같은 묶음의 다른 Li 금속 카드 ([Kazyak20Op] 등) 와 맞추려면 넣는 선택이에요.

### b-1. `comparison_vs_ours.md` `📑 Reference key` 표에 한 행 (4 칸: 약칭 | 논문 | digest/status | 유형)

| **[Sandoval25CT]** ⭐⭐ **무음극 Li \| Li₆PS₅Cl \| (Au · Ag 100 nm)/Cu operando μCT — 고분극 · 굵은 분말 = 계면 전체 Li 로 찬 균열 (기공을 채우지 않고 닫음 · ≈ 20 % 잔류) · 저분극 · 고운 분말 = 평평한 막 → 가장자리 필라멘트** · ⛔ **exp 전용 · 맨 Cu 아님 · A–D 물성 4축 진입 금지 (§E 1 행만)** | Stephanie Elizabeth Sandoval/D. L. Nelson/H. Sridhara/T. A. Thomas/J. A. Lewis/K. A. Cavallaro/P. Shevchenko/N. P. Dasgupta/F. L. E. Usseglio-Viretta/D. P. Finegan/**Matthew T. McDowell\*** (Georgia Tech · Argonne APS · Univ. Michigan · NREL) 2025 ***EES Batteries* 1, 1809–1821** (DOI 10.1039/D5EB00111K · CC-BY-NC 4.0) — "**Visualizing diverse lithium growth and stripping behaviors in anode-free solid-state batteries with operando X-ray tomography**" | ✅ `papers/sandoval2025_operando_xray_tomography_li_growth_stripping_anode_free.md` | exp (operando 싱크로트론 μCT + 정전류 · 원자단위 계산 0) |

### b-2. `comparison_vs_ours.md` §E 표에 한 행 (4 칸: 주장 | 출처 | 우리 | 일치) — [Kazyak20Op] 행 다음

| **🆕 (2026-11-24) Li₆PS₅Cl 에서도 Li 침투는 Li 로 찬 균열이 열리며 자란다 — 굵은 분말 · 고분극 반쪽 셀 (≈ 10 MPa · Au 100 nm/Cu · 0.5 mA cm⁻² · 3 mAh cm⁻²) 에서 균열이 집전체 계면 전체에서 SE 속으로 자라고, 원래 기공을 채우지 않고 그 옆에서 나며 기공을 닫는다 · 박리 때 끝부터 줄지만 새 균열 부피의 ≈ 20 % 가 남는다 · 박리 중 Li–LPSC 균열 벽 점착 탓으로 보이는 새 균열 · 고운 분말 · 저분극 셀은 평평한 막 → 고전류에서 가장자리 필라멘트** | **[Sandoval25CT]** `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. 5` · `Fig. 6` · `Fig. S5` · `Fig. S7` · Video S1–S5 (실독) · p. 1811–1819 | 우리 DFT 는 균열 · 크리프를 재지 않는다 — 걸리는 곳: Li \| LPSCl 점착 · 젖음 = W_ad 보고서 §7 · §8-4 (Li \| LPSCl 쌍은 아직 없음 · 값 미계산 · 위치 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §2 · §7 · §8-4) · LPSCl 의 Li 환원 계면상은 이 논문이 보지 않는다 (CT 로 안 보임) | △ 정성 · 셀 하나씩 · 숫자 비교 없음 · ⛔ 'Li 가 기공을 따라 자란다' 로 인용 금지 (반대) · '0.55 %' 를 펠릿 기공률로 인용 금지 · 원자료 'Case A' 시트를 `Fig. 3c` 값으로 쓰지 않는다 · B CE 92.9 % 정밀값 인용 금지 |

### b-3. (권장 · 실제 집) `comparison_vs_ours_DEM.md` §I 에 블록 (지금 I-22 · baer 보고가 I-23 을 제안했으니 **I-24** 정도 — 번호는 메인이 정해 주세요)

### I-24. `sandoval2025_operando_xray_tomography_li_growth_stripping_anode_free` — ★★ (exp · operando μCT) **LPSCl 무음극 Li 석출 · 박리 3D — DEM 의 해상 기공 · 벽 효과 · 두께 비균일 · '연결 기공 ≠ Li 길' 대조 표적 (보정 아님)** · ⚠ 펠릿 밀도 · 기공률 · SE 두께 없음

> **무엇을 주나.** Li \| Li₆PS₅Cl \| (Au · Ag 100 nm)/Cu 반쪽 셀 셋 (지름 2 mm · 225 MPa 압착 · ≈ 10 MPa · 복셀 1.4–1.8 µm · 15 분). 굵은 분말 (< 100 µm) 셀 A: 집전체 쪽 부분 부피 (1116 × 368 × 364 µm) 의 해상 기공 0.55 % · 0.5 mA cm⁻² 2 mAh cm⁻² 동안 새 균열 = 같은 발자국 Li 의 49 % (✎ 새 균열의 82 % 가 집전체 쪽 364 µm 안) · 박리 뒤 ≈ 20 % 잔류. 고운 분말 (1–5 µm) 셀 B · C: 평평한 막 · 고전류에서 가장자리 필라멘트 · B 두께 sd 2.1–2.6 → 3.3 µm (CV 17 → 15 % ✎).
>
> **★ DEM 대조 표적 (digest §9-3 T1–T10 · 방향 · 차수만).**
> ① **해상 기공 분율** — DEM 침대에서 ≳ 2 복셀 (≈ 3.6 µm) 보다 큰 기공만 센 분율을 같은 크기 상자로 낸다 (0.55 % 는 펠릿 기공률이 아니다 · 작은 불변 기공은 필터로 지운 값).
> ② **'연결 기공 = Li 길' 을 쓰지 않는다** — 굵은 분말에서 새 균열은 원래 기공 옆에서 나며 기공을 닫았다 (`Fig. 2d,e`) · 접촉 응력 · 큰 입자 내부 파괴 쪽을 본다.
> ③ **벽 효과 두께** — 고운 분말 셀의 고장은 늘 가장자리 (B 렌즈 균열 벽에서 figure-read ≈ 0.15–0.3 mm · 첫 0.5 mA cm⁻² 증착부터). 다이 벽 근처 기공률 · 접촉 수 반경 분포를 같이 내고 '입자 지름 몇 개' 와 차수를 견준다.
> ④ **두께 CV** — 계면 접촉 분포 → 국부 전류 → 막 두께 CV 의 방향 (절대 sd 를 거칠기로 읽지 않는다).
> ⑤ **같은 전류 · 다른 분극** — A ≈ 890 대 B · C ≈ 170–200 Ω cm² (✎ \|V\|/j) · SE 두께로 나눠도 A/B ≈ 3 · A/C ≈ 4 ✎ — 분말 출처가 함께 바뀌어 교란.
>
> **⛔ 인용 금지 / 한정어**
> · 셀 하나씩 · 펠릿 밀도 · 기공률 · SE 두께 · 온도 없음 · 압력 변수 없음 → DEM 보정에 쓰지 않는다.
> · 원자료 sup2 'Case A' 시트는 작은 부분 부피 (≠ `Fig. 3c`) · B CE 92.9 % 는 원자료로 재현 안 됨.
> · `Fig. 1d,e` 로 층 두께를 재지 않는다 (세로 ≈ 1.4 배).
> · 우리 DEM 기준값 문서 (`litdb/our_dem_baseline.md`) 가 자리표시라 우리 숫자는 적지 않았다.

---

## (c) `pdf_map.tsv`

**필요해요** — 자동 매칭이 본문만 붙이고 SI (`sandoval2025b_operando_xct_li_growth_sup3.pdf`) 는 '짝 못 찾음' 으로 남겼어요. 본문 · SI 공통 조각 한 줄이면 둘 다 잡혀요 (다른 sandoval 파일 `afssb2024_…` 와 안 겹쳐요 · xlsx · 영상은 PDF 가 아니라 매칭 대상이 아니에요). 넣을 곳은 `sandoval2025_electro_chemo_mechanics_anode_free_ssb` 줄 (지금 666 행) 근처가 자연스러워요.

```
sandoval2025_operando_xray_tomography_li_growth_stripping_anode_free	sandoval2025b_operando_xct_li_growth
```

---

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

> 이 묶음이 이미 먹이는 이웃 (세지 않음): #8 Ko 2025 *Nat. Commun.* 16, 1066 (`ko2025_…` · inbox 에 PDF 있음) · #9 Lee Y.-G. 2020 *Nat. Energy* 5, 299 (ref 4) · #10 Kasemchainan 2019 *Nat. Mater.* 18, 1105 (ref 23 · digest 생김). litdb 에 있는 참고문헌: ref 1 · 5 · 14 · 18 · 24 · 26 · 30 · 41 (digest §16).
> 대조: `litdb/papers` 파일 이름 + digest 본문 grep · `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md` grep · 서지는 전부 Crossref 로 확인 (2026-11-24).

| # | 문헌 | 왜 (우리 축) | litdb | 목록 |
|---|---|---|---|---|
| 1 | Xu, Le Houx, Kachkanov, Zhang, Wullich, Fankhauser, Löffel, Schmidt, El Kazzi · *Small* 22, e12284 (2026) — *"Operando X-Ray Computed Tomography Reveals the Role of Interfacial Nucleation Nanolayers in Suppressing Mechanical Failure in Zero-Excess Lithium All-Solid-State Batteries"* · DOI 10.1002/smll.202512284 (ChemRxiv 판 10.26434/chemrxiv-2025-k4wd7) | 같은 꼴 (Li \| LPSC \| Cu · operando CT) 에 **맨 Cu 대 Ag/Cu** — 이 논문에 없는 맨 집전체 대조 (질문 4) · 초록: 맨 Cu 는 가장자리 국한 석출 · > 0.5 mA cm⁻² 에서 LPSC \| Cu 박리형 균열 · Ag 는 고장을 Li 쪽으로 옮김 · FEM 포함 | 없음 | 없음 |
| 2 | Xu, Le Houx, Manchester, Zhang, Wullich, Gomez, Ihli, Banerjee, Schmidt, El Kazzi · ChemRxiv (2026-06-22 · **미심사**) — *"Correlative Operando X-Ray Imaging and Diffraction Revealing Mechanical Failure Pathways in Lithium Metal Sulfide-Based All-Solid-State Batteries"* · DOI 10.26434/chemrxiv.15004995/v1 | NCM811 \| Li₆PS₅Cl \| Li 전지 XCT + XRD + **적층압 감시** — 이 논문에 없는 압력 기록 (8-4 압력) · ⚠ Crossref 의 저널판 연결 DOI (`10.1002/smll.76550`) 는 정상 꼴이 아니라 저널판 미확인 | 없음 | 없음 |
| 3 | Kotakadi, Aspinall, Burton, Liang, Aihara, Pasta · *Joule* 9, 102175 (2025) — *"Impact of metallic interlayers at the lithium-Li6PS5Cl solid electrolyte interface"* · DOI 10.1016/j.joule.2025.102175 | 금속 인터레이어를 Li \| LPSCl 에서 직접 — W_ad 7 절 · 8-3 정조준 · baer 보고 (d) #1 ChemRxiv 판의 저널판 | 없음 | 없음 |
| 4 | Yoon, Vishnugopi, Nelson, Yong, Wang, Sandoval, Thomas, Cavallaro, Shevchenko, Alsaç, Wang, Singla, Greer, Ertekin, Mukherjee, McDowell · *Science* 388, 1062–1068 (2025) — *"Interface morphogenesis with a deformable secondary phase in solid-state lithium batteries"* · DOI 10.1126/science.adt5229 | 같은 그룹 · Li 안 5–20 mol% Na 가 박리 중 계면에 모여 접촉 유지 (초록) — 박리 공극 · 접촉 상실의 다른 해법 · DEM 접촉 회복 시나리오 | 없음 | 없음 |
| 5 | Lin, Zhang, Zhang, Wang, Yan, Wang, Jiang, Xiao, Li, Liang, Fang, Wang, Zhao, Sun, Zhao · *Small Struct.* 6, 2500172 (2025) — *"Unveiling the Impact of Porosity on Electrolyte Electronic Conduction and Electric Potential Field in Sulfide-Based Solid-State Lithium Metal Batteries"* · DOI 10.1002/sstr.202500172 | 황화물 막 기공률 ↑ → 전자 전도 몇 배 ↑ → 덴드라이트 (초록 · 표면 · 벌크 DFT 포함) — DEM 기공률과 우리 DFT 표면 전자구조를 잇는 다리 | 없음 | 없음 |
| 6 | Park, Yang, Watanabe, Yamamoto, Sakuda, Hayashi, Tatsumisago, Kumar, Thakur, Matsunaga, Uchimoto · *Solid State Ionics* 429, 116975 (2025) — *"Investigating the impact of solid electrolyte particle size/void shape in modulating lithium-ion conduction pathways within graphite composite electrodes using in situ X-ray computed tomography"* · DOI 10.1016/j.ssi.2025.116975 | SE 입도 · 공극 모양 → 이온 경로를 in situ CT 로 — DEM 입도 · 기공 출력의 CT 대조 (복합 전극) | 없음 | 없음 |
| 7 | Sandoval … McDowell · *Joule* 7, 2054 (2023) — *"Structural and electrochemical evolution of alloy interfacial layers in anode-free solid-state batteries"* · DOI 10.1016/j.joule.2023.07.022 (ref 12) | Au · Ag 100 nm 층이 첫 도금에서 어떻게 바뀌나 · Case B 의 한 장면이 여기 먼저 — 이 논문의 인터레이어 전제 | 없음 | **목록에 있음** (표 2 #6) |
| 8 | Lewis, Cortes, Liu … McDowell · *Nat. Mater.* 20, 503 (2021) — *"Linking void and interphase evolution to electrochemistry in solid-state batteries using operando X-ray tomography"* · DOI 10.1038/s41563-020-00903-2 (ref 22) | 같은 그룹 operando CT 원형 · 박리 공극이 저항을 지배 | 없음 | **목록에 있음** (표 2 #5) |

다음 순번: Ning 2021 *Nat. Mater.* 20, 1121 (ref 42 · 균열 먼저 Li 뒤 · **목록에 있음** '그 밖') · Ning 2023 *Nature* 618, 287 (ref 44 · spallation · wedge-opening · **목록에 있음** '그 밖') · Hu 2024 *Joule* 8, 2623 (ref 51 · Li 대 공극 분할) · Nelson 2024 *ACS Energy Lett.* 9, 6085 (ref 39 · 같은 그룹 CT) · Lewis 2023 *Adv. Energy Mater.* 13, 2204186 (ref 13 · 무음극 공극) · Hao 2021 *Nano Energy* 82, 105744 (ref 43 · 황화물 필라멘트 CT).

---

## (e) DEM-DFT 보고서 (W_ad 보고서) 에 쓸 거리

**질문 1–4 짧은 답** (자세한 것은 digest §3.1 · §3.4–3.6 · §9-3)
1. **셀 · SE · CT 조건** — Li₆PS₅Cl 분말 셋 (A < 100 µm Ampcera · B NEI 손으로 갈아 ≈ 5 µm · C ≈ 1 µm Ampcera) · 셀 안 225 MPa 압착 · **펠릿 밀도 · 기공률 · SE 두께 n/a** (SE 두께 figure-read A ≈ 1.4 · B ≈ 0.82 · C ≈ 1.1 mm) · 적층압 ≈ 10 MPa (나사 · 감시 없음) · **온도 n/a** · 0.5 mA cm⁻² 3 mAh cm⁻² 첫 증착 → (B) 1.5 · 3.0 · (C) 0.75 · 1.0 · 2.0 mA cm⁻² · 집전체 10 µm Cu + Au/Ag 100 nm · Li 2 mm 상대극 (figure-read ≈ 0.25–0.34 mm) · CT 복셀 1.8 (0.9 binning) · 1.7 · 1.4 µm · 15 분 (B ≈ 30 분 ✎). **DEM 과 같은 눈금이 아니에요** — 고운 분말의 입자 사이 기공은 CT 해상 밖이고 '0.55 %' 는 해상 기공 분율이에요.
2. **성장 · 박리 숫자** — A: 기공 + 균열 266 → 461 × 10⁴ µm³ (+73 % · Li 의 49 %) · 원래 기공 80 × 10⁴ (0.55 %) · 박리로 끝부터 줄고 ≈ 20 % 잔류 · CE 79.9 % · 단락 없음. B: Li 막 14.2 ± 2.4 · 15.0 ± 2.6 · 17.4 ± 2.8 · 21.3 ± 3.3 µm · CE 92.9 % (원자료 재현 안 됨) · 3.0 mA cm⁻² 에서 단락. C: 누적 6.37 mAh cm⁻² 에서 단락 · 가장자리 단일 필라멘트 (분할 숫자 없음). 죽은 Li 는 A 의 끝 부피에 포함 (따로 정량 안 됨).
3. **기공 연결성 · 국부 전류 · 접촉 상실** — 논문은 기공 연결성 · 접촉 분율을 **재지 않았어요**. 쓸 수 있는 것은 대조 표적 T1–T10 (digest §9-3): 해상 기공 분율 · 기공 자리 (큰 입자 경계) · '연결 기공 ≠ Li 길' · 균열 부피 수지 · ≈ 20 % 잔류 · 가장자리 · 두께 CV · 상대극 가장자리 몫 · 같은 전류 다른 분극 · 시간 · 공간 눈금. 전부 방향 · 차수용이에요.
4. **인터레이어** — 있어요 (Au · Ag 100 nm · 탄소 없음 · 맨 Cu 대조 없음).

| 보고서 항목 | 이 논문에서 쓸 점 | 위치 (쪽 · 그림 · 표) | 직접 봤나 |
|---|---|---|---|
| **8-4 'Li 침투 = Li 로 찬 균열이 열리며 자란다'** (지금 LLZO · 유리 Li₃PS₄ 하나로 받침) | 결정 Li₆PS₅Cl 3D 근거: 균열이 한두 장 (15–30 분) 안에 넓어진 뒤 폭이 멈추고 길이만 자람 (`Fig. 2c` · 단 `Fig. 2d` 큰 균열은 폭도 계속) · 갈래 · 박리 때 끝부터 줄어듦 · 새 균열 ≈ 20 % 잔류 | p. 1811 · 1813–1815 · `Fig. 2` · `Fig. 3` · Video S1–S3 · digest §5.3 · §5.4 | ✅ `Fig. 2` · `3` 원해상도 · 영상 S1–S3 전 39 장 대조표 + 확대 (S2 #9 · #13 · #16 · #22 · #38) |
| **8-1 · 8-4 점착** (W 와 2γ_Li) | 박리 중 Li 로 찬 균열이 줄 때 **Li–LPSC 균열 벽 점착 탓으로 보이는 새 균열** (저자 'presumably' · 측정 아님) — Li \| LPSCl W 가 닿는 현상 · 우리 쌍 목록에 Li \| LPSCl 은 아직 없음 (값 없음 · 위치 보고서 §2 · §7) | p. 1815 · `Fig. 3b` 초록 화살표 · digest §9-2 ② | ✅ `Fig. 3` 원해상도 |
| **8-4 압력 단계** | 제조 225 MPa · 운전 ≈ 10 MPa (나사 · 감시 없음) 한 점 · 압력은 변수 아님 → '적층압이 균열을 닫았다' 는 시험된 적 없음 (저자 숙제) | SI p. 2 · p. 1811 · 1819 | ✅ 글자 |
| **8-3 Ag/C 층 · 인터레이어** | 100 nm Au/Ag 는 Li 를 거의 안 담음 (✎ ≲ 0.1 mAh cm⁻² = 3 mAh 의 ≲ 3 %) · B (Ag) 핵생성 과전압 없음 · C (Au) +0.14–0.15 V 합금 평탄부 (원자료) · A (고저항) 는 0 V 아래로 밀림 · Li 막은 SE \| Li \| CC 두 계면 (`Fig. 4b`) · CT 로 합금층 위치는 못 가름 | p. 1811–1812 · `Fig. 1b` · `Fig. 4` · 원자료 sup1 · digest §3.2 · §14-8 | ✅ `Fig. 1` · `4` 원해상도 · 원자료 |
| **8-5 실험 대조 (순서)** | 같은 0.5 mA cm⁻² 에서 고분극 (A ≈ 890 Ω cm² ✎) = 계면 전체 필라멘트 · 저분극 (B · C ≈ 170–200) = 평평한 막 · 굵은 셀 셋끼리도 ≈ 340–1360 Ω cm² (figure-read ✎) — 순서 대조용 | `Fig. 1b` · `Fig. S5a` · 원자료 sup1 · digest §3.2 | ✅ `Fig. 1` · `S5` 원해상도 · 원자료 |
| **8-6 가져오지 않는 것** | 셀 하나씩 · 펠릿 밀도 · 기공률 · SE 두께 · 온도 없음 · 맨 Cu 대조 없음 · 분말 출처 · 입도 · 저항이 함께 바뀜 · 원자료 'Case A' 시트 ≠ `Fig. 3c` · B CE 재현 안 됨 · `Fig. 1d,e` 세로 ≈ 1.4 배 | digest §10 · §13 | ✅ (판독 · 원자료 대조) |
| **4 절 (DEM 에서 지금 할 수 있는 것) · 6 절 (한계) 옆에 둘 DEM 대조 표적** | T1–T10 (b-3 요약) — 해상 기공 분율 · '연결 기공 ≠ Li 길' · 벽 효과 두께 대 관측 가장자리 띠 (figure-read ≈ 0.15–0.3 mm) · 두께 CV · 분극 축 — **보정 표적 아님** | digest §9-3 · `Fig. 2` · `Fig. 5` · `Fig. 6b` · `Fig. S7` · Video S4 · S5 | ✅ 그림 원해상도 · 영상 S4 (윗부분 · 왼쪽 가장자리 확대) · S5 (장면 13 개 + 확대) |

보고서 문장 후보 (공유 보고서 문체 · 출처는 랩 표준 꼴):
- *Li₆PS₅Cl 에서도 Li 는 Li 로 찬 균열이 열리면서 SE 속으로 자라고, 박리하면 균열이 끝부터 줄지만 손상의 일부 (새 균열 부피의 약 20 %) 가 남는다 (EES Batteries, 1, 1809 (2025)).*
- *같은 실험에서 Li 는 원래 있던 기공을 채우기보다 그 옆에 새 균열을 내며 기공을 닫았다 — 연결된 기공을 Li 길로 보는 가정은 이 관찰과 맞지 않는다.*
- *박리 중 Li 로 찬 균열이 줄어들 때 새 균열이 생겼고, 저자는 Li 와 균열 벽의 점착을 원인으로 보았다 — Li | Li₆PS₅Cl 점착 에너지가 닿는 현상이다 (값은 아직 계산하지 않았다).*

---

## (f) 그림 · 동영상 크롭 요약

- **그림 14 장** = 본문 그림 6 (`Fig. 1`–`6`) + SI 그림 8 (`Fig. S1`–`S8`) · 표 0 (이 논문에 표 없음). 도구 한 번 · 손 크롭 · 다시 자름 0 · 번호 공백 · 놓친 캡션 0. `Fig. S1` 크롭 위에 SI 쪽 머리글 'SUPPLEMENTARY FIGURES' 가 같이 들어왔지만 그림은 온전해서 그대로 뒀어요.
- **본 것: 그림 14/14 전부 원해상도.** 그중 픽셀 판독: `Fig. 3c` 40 점 (점 중심 · 축 눈금 맞춤) · 축척 막대 + 층 경계 단면 `Fig. 1c–e` · `S1` · `S6b` · `S7b` · `S8` · `Fig. 6a` · `Fig. 4b` · `Fig. 5b,c` 와 원자료 21 점 대조 · `Fig. 1b` 와 원자료 전압 대조.
- **그림이 본문 · 원자료와 어긋난 것**: `Fig. 3c` ≠ 원자료 'Case A' 시트 (다른 부분 부피) · `Fig. 1d` · `1e` 세로 ≈ 1.4 배 (SE 두께가 같은 셀의 다른 그림 · 원복셀 영상보다 1.35–1.41 배) · `Fig. 4e` 캡션 0.80 mAh cm⁻² 대 본문 0.75 (p. 1812) 대 원자료 0.83 ✎ · `Fig. 5d,e` 지도 지름 figure-read ≈ 1.45 mm (본문 '면적 75 %' 는 지름 비) · `Fig. S4` 두 y 축 (Li 0–70 · 공극 0–25 · 겹침이 덜 보임) · `Fig. 2` 범례 'Original Porosity' 대 `Fig. S2` 'Original Cracks' (이름만 다름) · `Fig. 6a(ii)` 의 0.75 단계 뒤 필라멘트 대 Video S5 첫 균열 장면 7/13 (시각 표지 없어 판정 못 함).
- **영상 5 편 (전부 봄)**: S1 (sup4 · 39 장) · S2 (sup5 · 39 장) · S3 (sup6 · 39 장) — 전 프레임 대조표 + #0 · #22 · #38 (S2 는 6 장 2 배) · S4 (sup7 · 78 장 · 대체로 두 장씩 같음) — 39 장 대조표 + 윗부분 10 장 + 왼쪽 가장자리 7 장 2 배 · S5 (sup8 · 128 장 · 다른 장면 13) — 13 장면 대조표 + 앞 8 장면 왼쪽 위 1.6 배 · 첫 장면 5 개 원크기. 저장 프레임 58 장 (`video_frames/` · 0.5 s 간격 + 끝 · sup8 장면 전부). 영상에만 있는 것: B 가장자리 렌즈 균열이 첫 증착 초반부터 (S4 #6) · C 첫 균열은 13 장면 중 7 번째.
- **임시 파일 점검 (병렬 충돌 주의)**: 글자 · 전 프레임 · 대조표 · 스크립트 · Crossref 응답은 전부 `scratchpad/sandoval2025_operando_xray_tomography_li_growth_stripping_anode_free/` 안에 `sandoval2025b_` 접두 이름으로만 썼어요 (공용 이름 없음). 본문 글자 파일 첫 줄 = 이 논문 표지 (*EES Batteries* · 'Published on 15 August 2025') · SI 첫 줄 = 이 SI 표지 · inbox 파일 9 개 sha256 = `batch.json` 값과 전부 일치 (`5158e6d9…` 본문 · `3538f290…` SI 등). 대조표 그림 내용 (LPSC 단면 · 균열 3D) 도 이 논문 것이었어요.

---

## (g) Jeff Sakamoto 저자 여부

**아니에요** — 저자는 Stephanie Elizabeth Sandoval · Douglas Lars Nelson · Hari Sridhara · Talia A. Thomas · John A. Lewis · Kelsey Anne Cavallaro · Pavel Shevchenko · Neil P. Dasgupta · Francois L. E. Usseglio-Viretta · Donal P. Finegan · Matthew T. McDowell (교신) 11 명이에요 (본문 · SI 저자 줄 둘 다 확인). 'Sakamoto' 는 참고문헌 10 편 (refs 3 · 14 · 16 · 17 · 18 · 24 · 26 · 30 · 31 · 46 · 'J. Sakamoto') 에만 나오고 SI 에는 0 건이에요. digest 머리말에는 그 이름을 쓰지 않았고 웹앱 `_paper_pis` = [] 예요 — INDEX 행에 `🏷 Jeff Sakamoto 공저` 를 달지 않아요. (같은 1저자의 관점 논문 `sandoval2025_electro_chemo_mechanics_anode_free_ssb` 은 공저라 🏷 가 붙어 있는데, 이 편과 다른 논문이에요.)
