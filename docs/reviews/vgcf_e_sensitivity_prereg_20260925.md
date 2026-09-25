# 사전등록 — VGCF 탄성계수 (MPM 첨가제 강성) 민감도 · SBE 킷 3팔 (2026-09-25)

> 실행 계약.  **런 전에** 등록한다 (규율: 결과 보고 창을 옮기면 무효).
> 계기 = Methods SI 표 리뷰 (강준희 09-25): *"VGCF Young's modulus 10 GPa 도 그냥 Assumed?"* — 원장 `CL-42`
> (`ADD_E_SET_20260818`: *"사용자 지정 · 근거 문헌/측정 미기재"*).  문헌 단섬유값은 180–245 GPa (Ozkan 2010) 로 우리 값의 20 배.
> 비준 = 사용자 09-25 *"민감도 런을 kgy 에서 진행해보자"*.

## 0. 무엇을 묻나 (한 줄)

**VGCF 재료점의 탄성계수 E 를 1 → 10 → 100 GPa 로 바꿔 같은 침대를 다시 압밀하면 ε_sphere · 두께 · σ_e 가 얼마나 움직이나.**
움직임이 작으면 표의 10 GPa 는 "유효 강성 (2차 입력)" 으로 정직하게 라벨할 수 있고, 크면 앵커 (문헌 단섬유값 또는 섬유를
재료점 구름에서 제외) 없이는 표에 못 둔다.

## 1. E 가 들어가는 자리 (코드 실측)

- `scripts/mpm3d_compaction.py` `ADD_E_NU['VGCF'] = (10.00, 0.30)` — ① CFL dt 가드 (`_M = max(…, λ+2μ)`) ② ADD 표 → 섬유 재료점의 Lamé 상수.
  σ_y 2.0 GPa ≫ 가압 0.3 GPa 라 섬유는 **탄성**으로만 반응한다.
- STEP3 σ 에는 **직접 안 들어간다** — MPM 압밀 기하 (SE 형상 · 공극) 를 거쳐서만.
- 생산 침대 (Phase A 킷 · SDCP W2 SBE/DBE) 는 전부 `--dilate-z` + `--fibre-buckle` 모드 = **강체 strut 아님** (dilation 이 strut 을
  대체, `mpm_input_from_case.py:707`).  ⇒ 두께는 dilation (λ_dz, Cho 보정) 이 정하고 E 는 그 틀 안의 국소 형상만 바꾼다.
- 이미 있는 상한: 2026-07-02 `--fibre-stiff` (E→∞ 강체 핀) — `input_6mAh_real_4` · n_grid 256 · VGCF 4 wt%: porosity 8.63 → 9.38 % (+0.75 %p) ·
  두께 +0.9 µm · SE 소성변형 0.195 → 0.006 (`docs/additive_test_campaign.md` §해결).  σ_e 미측정 · 다른 침대.

## 2. 설계

| 항목 | 값 |
|---|---|
| 침대 | Phase A 킷 `VGCF_PTFE_3_1` (6 mAh · P:S 7:3 · VGCF 3 wt% · PTFE 1 wt% = SBE 조성) — `docs/data/phase_a_6mah/kits/VGCF_PTFE_3_1/` |
| 팔 | E_VGCF ∈ {**1**, **10** (생산값, 같은 코드로 재압밀), **100**} GPa — 킷을 세 폴더로 복사, `run_mpm.sh` 에 `--add-e-override VGCF=<E>` 만 추가.  seed · dilation · buckle · n_grid 256 · mach 0.03 · 그 밖 전부 동일 |
| STEP3 | `scripts/sdcp_gain_vox015_8arm.sh` · `VOX=0.15 BRIDGE_UM=0.24 PTFE_STAMP=centerline LEAN=2 ARMS=1` · 새 OUTDIR (SKIP 캐시 함정 회피) |
| 잰다 | ① `porosity_sphere` (ε_sphere, `mpm_metrics.json`) ② 두께 (`wall_z` → µm) ③ σ_e(SBE) (mS/cm, origin 0) ④ 부수: `settled_over_target` · SE 소성변형 합 · coverage AM |
| 대조 | 10 GPa 팔 = 기준.  1 · 100 의 차이를 기준 대비로 |
| 기계 | kgy (사용자 로컬 GPU) — 압밀 3 회 + STEP3 3 회 |

⚠ 100 GPa 는 SE 스택 (M ≈ 26.2 GPa) 을 넘어 CFL 가드가 dt 를 캡한다 (`mpm3d_compaction.py` 1686–1699) — 더 느릴 뿐 결과 해석에는
문제 없다 (가드가 그 목적).  E 는 재료점 Lamé 상수로만 들어가고 다른 상수는 안 바뀐다.

## 3. 판정선 (런 전 고정)

- **h0 "2차 입력"**: 1 ↔ 100 GPa 사이에서 **|Δε_sphere| ≤ 0.3 %p** **그리고** **|Δσ_e / σ_e(10)| ≤ 2 %** (팔-폭 0.68 % 의 3 배, `CL-33/34` 실측).
  ⇒ Methods 표: *"10 GPa — Assumed (effective compliance of sub-grid fibre material points; σ_e insensitive over 1–100 GPa, Δ ≤ x %)"*.
- **h1 "앵커 필요"**: 둘 중 하나라도 넘으면 ⇒ 표에 10 GPa 를 둘 수 없다.  후속 = 문헌 단섬유 245 GPa (Ozkan 2010) 로 재압밀하거나
  섬유를 재료점 구름에서 제외 (strut 또는 dilation 만).  이 사전등록은 그 후속을 **지시하지 않는다** (별도 등록).
- 두께: 보고만 (dilation 이 정하므로 판정 축이 아니다).  |Δ두께| 가 1 셀 (0.39 µm @256) 을 넘으면 원인 서술.
- 반올림 규약: ε %p 소수 둘째 · σ_e 상대 % 소수 둘째.  판정은 반올림 전 값으로.

## 4. 무효 조건

- 세 팔의 `mpm_metrics.json` 이 `add_e_override` · `E_anchor` 태그를 안 들고 있으면 (같은 코드 · 같은 seed 증명 실패) 무효.
- 어느 팔이든 `reached` 가 아니거나 (`porosity_at_target_pct` None) STEP3 미수렴이면 그 팔은 결측 — 판정 보류 (다른 팔로 대체 금지).
- 10 GPa 재압밀이 옛 `latest_run` 과 ε_sphere 0.05 %p 이상 다르면 **재현성 문제**로 먼저 기록 (판정은 세 새 팔끼리).

## 5. 예측 (기록용 — 판정 아님)

E 가 σ_y 아래 탄성 응답에만 들어가고 두께는 dilation 이 고정하므로 **h0 쪽**을 예상한다 (Δε < 0.1 %p · Δσ_e < 1 %).  strut 극한 (+0.75 %p @4 wt%,
frozen AM) 이 상한이므로 100 GPa 팔이 그것을 넘으면 코드 결함을 의심한다.

## 6. 산출물 · 등재

- 결과 = `docs/data/vgcf_e_sensitivity_20260925/` (팔별 `mpm_metrics.json` 발췌 + STEP3 영수증 + 요약 TSV) · 이 문서 §7 에 판정.
- 원장: `CL-42` (ADD_E_SET) 에 결과 링크 · Methods 표 라벨 (`scripts/build_methods_docx.py`).
- 코드: `--add-e-override` (`mpm3d_compaction.py`) — selftest 로 파서 · 적용 · 매니페스트 태그 · 거부 (미지 상 · 비수치 · 0 이하) 를 고정.

## 7. 결과 (런 뒤 채운다)

(비어 있음 — 런 전)
