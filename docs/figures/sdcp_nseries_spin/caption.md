# sdcp_nseries_spin_partition.png — caption (English, manuscript/SI-ready)

**Figure Sx. Spin partition of the H-removed doped state (D•) of SDCP oligomers.**
Löwdin spin populations from ORCA r2SCAN-3c geometry optimizations (doublet, total spin 1.000).
**(a)** n = 6: the whole spin split into four groups that together cover every atom — sulfonate
group (SO₃) 7.7 %, aryl (thiophene) ring atoms 79.7 %, ether O 12.1 %, other (ring H and linker H)
0.5 %. "Aryl rings" counts ring atoms only, the definition used for the July n = 1–3 series, which is
why SO₃ + rings alone give 87.4 %; the remaining 12.6 % is dominated by the ether oxygens.
**(b)** The same partition for n = 1, 2, 3 (end- and mid-doped) and 6. For n = 1–3 the July data
resolve only SO₃ and rings; the balance is drawn as one hatched, unresolved column (ether O + H).
The hole moves from the SO₃ radical (65 % at n = 1) to the backbone π system (79.7 % at n = 6),
crossing 50 % at n = 3 (mid).
**(c)** n = 6, spin per thiophene ring along the chain (ring atoms only, the same definition as the
table; sum 79.7 %). The spin is spread over rings 3–5 (59 % together) with its maximum on ring 4 (23.3 %);
no single ring carries more than a quarter of the spin.
The oxidized state is imposed; the figure is not evidence that self-doping occurs.

Source data: `db/properties/sdcp_nseries_spin_2026_09_08.json` · Origin CSVs:
`db/properties/sdcp_nseries_spin_partition_fig.csv`, `db/properties/sdcp_n6_ring_profile_fig.csv` ·
tool `tools/figures/fig_sdcp_nseries_spin.py`.

## 한국어 설명 (세미나·1저자용 — 그림 안 글자는 영어만)

- **(a) 100 % 까지 네 칸.** 도핑 상태(전자 하나 뺀 더블렛)의 스핀 1.000 을 원자 그룹으로 나눈 것.
  SO₃ 7.7 · 아릴 고리 79.7 · 에테르 O 12.1 · 기타 0.5 → 합 100.0. 표에는 앞 두 칸만 올리니까
  87.4 로 보이는 것이고, 나머지 12.6 은 거의 에테르 O 다. "기타 0.5" 는 고리 H −0.2(π 라디칼 옆 H 의
  음의 스핀 분극) + 알킬 링커·말단 H 0.7 이다.
- **(b) n 에 따른 이동.** 같은 분할로 n=1 → 6 을 나열. SO₃ 65 → 62 → 55/42 → 7.7 로 줄고, 고리는
  35 → 33 → 40/50 → 79.7 로 는다. 빗금 칸은 "7월 표에 이 분해가 없다" 는 표시다 — 값이 작아서가
  아니라 못 가른 것. n=1 은 모노머라 에테르가 없어 나머지가 0 이다. 점선 50 % 를 n=3(mid) 에서
  넘는 것이 7월의 크로스오버.
- **(c) 고리별.** n=6 의 79.7 이 어느 고리에 있나. ring4 23.3 > ring5 20.0 > ring3 15.9 순으로
  사슬 한쪽(3–5번 고리, 합 59.2)에 치우쳐 있고, 어느 한 고리도 25 % 를 넘지 않는다 — "ring4 에 국재"
  가 아니라 "세 고리에 걸친 폴라론". 2026-09-08 gabia 재분석(고리 원자만 · 합 79.7)으로 확정.
  말단 α-H 의 −0.2 는 ring5 의 H 에 있다(참고 열). 도핑 자리(떼어낸 H 의 고리)는 아직 미확인 —
  확인되면 "자리 근방인가" 를 붙인다.

⛔ 피할 표현: "자가도핑이 일어난다" (산화 상태를 준 계산) · "전역 최소" (fresh SCF 한 번) ·
strict/extended 값을 7월 표 옆에 놓기 · SP 값과 섞기 · "합이 100 이 아니니 계산이 이상하다".
