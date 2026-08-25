# Codex 5차 리뷰 요청 — A 트랙(코드 규율) 흡수 가부 (2026-08-25)

**리뷰어에게**: R4 의 NO-GO 조건을 닫았다고 주장한다.  이 문서는 그 주장의 **공격 지점**을
스스로 지목한 것이다.  정본은 `docs/reviews/codex_absorb_verdict_20260825.md` 와
`docs/reviews/findings.json`, 규율은 `CLAUDE.md` 최상단.

⚠ **이 요청의 범위는 코드 규율 층뿐이다.**  σ_e 절대값·SBE/DBE 이득 비는 여전히
격자 미수렴이고 **아무것도 주장하지 않는다** (그것은 C = GPU 재실행 이후의 일이다).

---

## 0. 재현 (단독, 한 줄씩)

```bash
git clone sdcp_review_<sha>.bundle repo && cd repo
git checkout claude/sdcp-dem-manuscript-si-pqwtv8
bash scripts/check_all.sh                    # 검사기 selftest 8 + 리포 실물 2
python3 scripts/mutation_sweep_20260825.py   # 돌연변이 배터리 41개 (~20 분)
```

★ R4 때 번들이 **incremental** 이라 빈 저장소에서 열리지 않았다.  이번 번들은
`make_review_bundle.sh` 가 만들고, 만드는 자리에서 **빈 디렉터리에 clone 해 보고**
그 안에서 **원장 검사를 실제로 돌려** 통과를 확인한다 (§3-③ 이 이 검증이 잡은 결함).

---

## 1. R4 조건별 상태

| R4 잔여 | 상태 | 무엇을 했나 |
|---|---|---|
| R4-CX-03 solver-affecting CLI 전수 | ✅ 규칙 M | 파서를 **실행해서** 잡고(`parse_args` 가로채기) `--help` 를 뺀 **전 79 옵션**이 9 범주 중 하나로 등재를 요구.  규약 축 24 전수 도달 검사 |
| R4-CX-05 cross-dir raw diff-set | ✅ | 레지스트리 대신 **매니페스트 전수 훑기**.  분류 안 된 키는 **값이 같아도** HOLD |
| R4-CX-05 선언 뒤집기 pass-mutant | 🔶 | ㊷ 가 레지스트리에서 거동 생성 · ㊹a `PROTOCOL_FIELDS ⊆ FIELD_CONTRACT` · ㊹f `계약 ∩ 면제 = ∅`.  **회계 범주 오선택**은 잔여 |
| R4-CX-06 구조화 selftest | ⬜ | 미착수 (harness 정확도 개선이지 봉인이 아니라 뒤로 미뤘다) |
| R4-CX-08 standalone bundle | ✅ | 위 §0 |
| 배터리 잔여 3건 | ✅ | 셋 다 **실제 결함**이었다 (기대집합 정정이 아니다) — §3-① |

---

## 2. 이 트랙이 실제로 적발한 것 (원장 SELF-02~06)

**규약 밖에서 σ 침대를 바꾸던 축 아홉 개**:

· `--dilate-z` — `vc.load_am(scaffold, dz=…)` 결과가 그대로 `_s3.rasterize` 로 들어간다
  (`mpm_webapp_payload.py:988` → `:1403`).  `input_digest` 는 **파일 내용만** 덮으므로
  같은 scaffold 를 다른 dz 로 늘린 두 팔이 digest 동일로 통과했다.
  ★ **가정이 아니다** — 생산 킷 둘 다 `--dilate-z 1.0719` 로 돈다 (실측 확인).
· SE 점구름 **합성 여부** — `if a.se_proxy or not a.se:` 라 `--se` 를 **빠뜨리기만 해도**
  proxy 구름이 되고 그것이 `se_pts=` 로 들어간다.  읽은 파일이 없어 digest 가 원리적으로
  못 덮는다.  (실측: 생산 킷은 `--se se_dump.npy` 를 넘긴다 = 실침대였다.  게이트는 재발 방지)
· `sigma_superp_S_cm`·`sigma_swcnt_S_cm`·`swcnt_ion_block` — σ 표에 실제로 들어가는데
  `PROTOCOL_FIELDS` 밖 (R4-CX-03 이 지목한 것의 전수판)
· `periodic_xy`·`plate_rule`(+위 다섯) — `PROTOCOL_FIELDS` 에는 있는데 **`FIELD_CONTRACT`
  밖**이라 `compare_dirs` 가 고정을 안 봤다 = 두 디렉터리 사이에서 자유롭게 달라져도 `measured`

⇒ 규약 축 19 → **24**.  해시가 달라지므로 **옛 팔은 전부 HOLD** 된다 (p1→p2 로 이미
  전 팔 재실행이 필요했으므로 추가 비용은 없다).

---

## 3. ★ 공격해 달라 — 내 검사기가 세 번 가짜 초록을 냈다

이 세션에서 **내가 만든 게이트가 7번 과잉차단**을 냈고 **내 검사기 초판이 3번 가짜 초록**을
냈다.  전부 스스로 잡았지만, 그 사실 자체가 이 층의 신뢰도를 말해 준다.

**①  규칙 M 초판 (SELF-02)** — payload 파일만 AST 로 훑어 `se_material.temperature_argparse`
가 **다른 모듈**에서 등록하는 `--temp-c`·`--ea-ion-ev` 를 못 봤다.  오히려 "파서에 없다"
(M_STALE)로 **거꾸로** 보고했다.  이름 조각 필터는 `--dilate-z`·`--k-carbon`·`--i0-a-m2` 를
후보에서 뺐다.  ⇒ **"후보를 고르는 코드" 가 곧 사각지대다.**
→ **공격점**: 지금 판도 "실행해서 잡는" 방식인데, `main()` 이 `parse_args` 전에 조건부로
  옵션을 추가하는 경로가 있으면 여전히 샌다.  그런 경로가 있는가?

**②  `MANIFEST_RESULT_KEYS` 면제 (배터리가 알려 줌)** — σ_VGCF 를 "런 결과" 로 적어도
**아무 시험도 안 물었다** (레지스트리 루프가 먼저 잡기 때문).  즉 그 면제 목록은 계약된
축을 못 약화시킨다.  진짜 위험은 "계약된 축을 면제로 옮기는 것" 이라 ㊹f 로 막았다.
→ **공격점**: 면제 목록이 잡을 수 있는 축을 **다른 방향으로** 새게 하는 경로가 있는가?

**③  원장 SHA 검사 (SELF-06)** — `git cat-file -e` 로 **객체 존재**만 봤다.  리베이스로
버려진 커밋도 로컬 저장소에 객체가 남아 **통과한다**.  R4CX-01~08 이 rebase **이전**
SHA 를 가리키는데 로컬 8건 전부 초록이었다.  번들 안에서 검사를 **실제로 돌려서야** 드러났다.
→ 지금은 `merge-base --is-ancestor` 다.  회귀 19b 가 `git commit-tree` 로 **매달린 커밋**을
  만들어 그 상태를 재현한다.
→ **공격점**: 원장이 브랜치 밖을 가리키는 **다른** 형태(태그·서브모듈·squash)가 있는가?

**④  배터리 자신** — `broad` 표식을 새로 넣었다 (기전 제거형 돌연변이는 "기대 밖 실패 0"
이 원리적으로 성립하지 않는다).  ⚠ 이것이 **면죄부로 쓰이면** 배터리가 무의미해진다.
게이트 하나를 끄는 돌연변이에는 금지라고 적어 뒀지만, **강제하는 코드는 없다**.
→ **공격점**: `broad` 를 붙여 진짜 얽힘을 숨길 수 있는가?

---

## 4. 이 요청이 **주장하지 않는 것**

· σ_e 절대값 · SBE/DBE 이득 비 — 격자 미수렴.  인용 금지 목록은 `claims.json` `quotation_ban`.
· CPU census — 지금 있는 것은 **합성 침대** census 뿐이고 실침대 σ 감소율이 아니다.
· 킷 `run_mpm.sh` 는 이 리포에 **없다** (kgy 로컬).  §2 의 킷 실측은 사용자가 확인해 준 것이다.

## 5. 열린 항목

`findings.json` 의 `open`/`claimed_fixed` 전부.  특히:
· A3 잔여 — 회계 **범주 오선택**(physics 를 `numeric`/`mode` 로 선언)을 코드로 반증할 방법
· A4 — selftest 구조화 출력 + harness exact-ID multiset
· `σ_SDCP = 250` 출처(캐스트 필름 vs 압착 펠릿) · `ρ_SDCP` — **사용자 회신 대기**.
  펠릿이면 접촉저항이 이미 포함된 값인데 복셀 솔버는 접촉을 융합하므로 이중계상이 된다
  (CL-47 이 σ_VGCF 에서 지적한 것과 같은 부류).
