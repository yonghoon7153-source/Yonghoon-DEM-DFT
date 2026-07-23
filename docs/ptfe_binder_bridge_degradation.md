# PTFE 바인더-브릿지 열화 (#31) — F1-style OFF 기본 튜너블 훅

**기전:** PTFE(sid=7) 피브릴이 AM–SE / AM–AM 접촉을 브릿지해 기계적 접촉 유지.  사이클 진행 →
PTFE **defluorination**(Li⁺가 –CF₂– 환원 → LiF + 비정질 C), 취화·접착 상실 → 브릿지 파단 →
기계 접촉 감소 → R 상승.

## ⚠ 문헌 앵커 상태 — DIRECTION만, MAGNITUDE 미앵커 (정직 플래그)
- **lee2025**: SEM — 피브릴 바인더–VGCF 망이 SE/cathode 계면 **브릿지**(브릿지 존재 직접증거).
  PTFE가 σ_e 죽임(0.5/2/5wt% → 34/4.5/0.011 mS/cm) = 제조/pristine 효과.
- **kang2025**: CEI LiF 분율 PC_PTFE73 29.8% vs PTFE 37.4%@100cyc ("PTFE 자체분해→LiF 과다") —
  cathode-side 가장 근접값이나 **조성(XPS)** 측정이지 기계-접촉-손실 곡선 아님.
- **liu2025 review**: PTFE+Li→Li₂S+LiF 환원 defluorination — 반복적으로 "화학축, 모델 밖".
- **결론: cathode-side PTFE-브릿지 기계-R-vs-N 곡선의 litdb 앵커 없음** → 신규 digitize 필요.
  `docs/digest_model_application_backlog.md:121` F1 규약("날조 금지, conservative tunable hook only")
  준수 → **기본 OFF 튜너블 훅**으로만 shipping.

## 구현 (cycle_contact_ledger.py, 기본 OFF)

per-cycle 루프서 CZM 개구 문턱 `dcr`을 PTFE hold로 보정:
```
f_defluor(N) = 1 − e^(−N/τ)                                        # ASSUMED-FORM 감쇠
dcr_eff = dcr · (1 + ptfe_hold · ptfe_bridged_frac · (1 − f_defluor))
brk_now = opened & czm_kind & (gap_nm > dcr_eff)                   # dcr → dcr_eff
dmg[st] += clip(gap_nm[st] / dcr_eff, 0, 1)                        # Miner도 dcr_eff (지연)
```
- 브릿지가 초기(N 작을 때) dcr_eff↑ → 접촉을 **더 오래 잡음**(파단 지연); defluorination으로
  hold 감쇠 → dcr_eff→dcr → 지연됐던 파단 방출.
- CLI (F1-style, 모두 중립 기본): `--ptfe-bridge`(플래그) · `--ptfe-hold`(0=무영향) ·
  `--ptfe-defluor-tau`(30) · `--ptfe-bridged-frac`(0=무영향, 평균장).
- `--ptfe-bridge` 없거나 `ptfe_hold=0` → `dcr_eff≡dcr` → **byte 불변**.

## ★ 이중계산 가드
- PTFE 브릿지-손실 = **기계 접착** → **접촉 원장**(rct_holm_rel) → `dR_contact`.  화학 채널(dR_chem)과
  직교 — PTFE의 LiF 생성(화학 사실)이 `dR_chem`을 또 부풀리지 **않도록** 분리(같은 defluor 이중계상 금지).
- PTFE는 e/ion σ 격자서 **절연**(기본 --sigma-ptfe 0) → 브릿지-손실은 **기계 접촉만** 영향, σ 경로 이중계산 없음.
  PTFE의 σ_e-패널티(lee2025)는 pristine 제조 효과 = `--sigma-ptfe` 민감도 노브(별도 축·별도 런).
- dcr_eff는 **문턱만** 바꿈(gap_nm 기하 불변) → PTFE-브릿지와 AM-수축-파단은 같은 alive 계상, 가산 파단 없음.
  hold가 dcr_eff를 너무 키워 이미 열린 접촉을 **부활**시키지 않도록: hold는 **지연만**, defluor가 지연 제거(설계상).

## 검증
selftest 10/10 (신규 9): 같은 베드(gap 29nm > δcr 20)서 OFF f_brk 1.000(=selftest8 byte 불변) →
ON(hold=1,frac=1) 0.000(N=1 held 지연).  ⚠ magnitude 미앵커 → 값은 스윕 전용, 신규 digitize 대기.
