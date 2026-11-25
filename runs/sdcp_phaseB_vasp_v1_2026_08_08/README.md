# SDCP × LiNiO₂(104) Phase-B DFT+U v1 — 외주 결과 영수증 (2026-08-08 수령, 08-10 등재)

외주처 VASP 단일점 6잡. **원본 아카이브**: `phaseB_results.tar.gz` (2026-08-08 업로드 수령).
OUTCAR 는 gzip 으로 전량 보존 (`gunzip -k */OUTCAR.gz`). 기하는 MLIP(UMA,
freeze_frac 0.85, phaseA_top1free) 이완본의 **단일점** — 이완 없음.

## 숫자 (RESULTS.txt 그대로)

| 항목 | 값 | 인용 |
|---|---|---|
| **dE_extract(doped)** | **+0.3356 eV** (sigma→0 판독 +0.3395 — 부호 유지) | ⭕ **부호만 인용 가능** — Li 추출은 오르막 = UMA 의 −1.465 eV "추출 안정화" 는 아티팩트 |
| E_ads(doped) | −0.3204 eV | ⛔ 인용 금지 |
| E_ads(neutral) | −0.2880 eV | ⛔ 인용 금지 |
| Δ = E_ads(d)−E_ads(n) | −0.0324 eV | ⛔ 인용 금지 |
| dE_rxn(doped) | +0.0152 eV | ⛔ 독립 결과 아님 (= E_ads,d + dE_extract 재조합) |

## 왜 E_ads/Δ 는 못 쓰나 (2026-08-08 감사, 원 대화 + 세미나 빌드시트 리뷰로 확정)

1. **자세 불일치** — doped `r0_g20` vs neutral `r180_g22`: 회전·위치·접촉이 함께 달라
   32 meV 가 도핑 효과인지 자세 차이인지 분리 불가.
2. 고립 분자에 `ISMEAR=1 SIGMA=0.2` (표면용 smearing) — mol_doped 는 열린 껍질이라
   Δ 에서 상쇄 안 됨. 판독 열만 바꿔도(TOTEN→sigma→0) Δ 가 32→26 meV.
3. 쌍극자 보정 없음 · `LASPH` 없음 · 자기 초기값 1개 (complex_doped |mag| 2.38 의
   최저해 여부 미확인).
4. 기하 실측: doped 최근접 O···Li 3.077 Å(배위 없음) / neutral 2.094 Å(**배위 있음**)
   — "physisorbed" 라벨 자체가 neutral 쪽에서 틀림.

**dE_extract 가 살아남는 이유**: complex_doped ↔ complex_doped_extr 은 조성·셀·분자가
동일해 분자 smearing 오차가 정확히 상쇄되고 쌍극자도 거의 상쇄. 단, 자세는
`r0_g20 → r180_g20` 이라 순수 Li 이동 외에 분자 방위 변화가 섞여 있음 —
**"고정 MLIP 끝점 두 개의 전자에너지 차"** 가 정확한 이름이고, 장벽·자유에너지·
전극전위가 아니다.

## 재계산

수정 프로토콜 v2 (ISMEAR 0/0.05 · LDIPOL · LASPH · LREAL=F · LORBIT=11 ·
자기씨앗 3개 · 분자 1×1×1 k) 입력 패키지가 외주 발주 대기:
`sdcp_phaseB_vasp_recheck_vendor_v2_2026_08_08.zip` (12잡, site preference 는
의도적으로 제외 — SITE_BLOCKED.md 참조).
