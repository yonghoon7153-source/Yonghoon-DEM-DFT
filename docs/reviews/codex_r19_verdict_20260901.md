# Codex R19 판정 — 검사 배선과 "낡음" 판단 (2026-09-01)

**판정: PARTIAL STRENGTHENING — HOLD.**

요청서는 `docs/reviews/codex_review_request_r19_20260901.md`.  세 커밋(`49d2bd6d`
`1720d006` `7dbf38fb`)에 대해 *"검사를 강화한 것인가, 통과하도록 낮춘 것인가"* 를 물었고,
Codex 는 **방향은 강화가 맞지만 여러 자리에서 계약이 얇아졌다**고 판정했다.  아래는
받은 판정을 항목별로 옮긴 것이고, 우리 대응은 원장 `findings.json` R19-01~10 이 정본이다.

⚠ 이 문서는 **받은 판정의 기록**이다.  대응하며 알게 된 것은 원장에 적고 여기 섞지 않는다.

---

## P1-01 (Q1a) — 세미나 재작성이 긍정 계약을 잃었다

`?historical=1` 은 여전히 슬라이드를 준다 (`webapp/app.py`).  그런데 재작성된 테스트는
**장수·스키마·노트·차트·번호를 더는 보지 않는다**.  그리고 별도 창구인
`/api/seminar/deck` 의 fail-closed 게이트는 **검사가 아예 없다**.

반례: `sed -i '<게이트 행>s/.*/    if False:/' webapp/app.py` 를 넣어도 28/28 이 초록이고,
그 상태에서 기본 `/api/seminar/deck` 은 **표지 없는 철회 pptx** 를 그대로 내보낸다.

요구 = 네 경로를 다 고정할 것: ⓐ 기본 슬라이드 거부 ⓑ historical 슬라이드 긍정 스키마
ⓒ 기본 덱 거부 ⓓ historical 덱 내려받기.  검사 15 는 **파일명 접미어만** 본다
(`webapp/test_seminar_page.py`).

## Q1b — 근거를 문서로 옮긴 것은 바꿔치기다

API 거부는 CLAUDE.md / `claims.json` 을 가리키는데, 새 검사는 그 대신
`docs/mpm_platen_kinematic_stop_defect.md` 의 실재를 본다.  그 문서는 **스스로 rev6 에서
멈췄다고 적고 있고**, 이 철회의 근거도 아니다.  검사 17 의 *"독립성 철회"* 계약은
**대체 없이 사라졌다**.

요구 = 응답에 `evidence_ref` 를 실어 근거를 지목하고, 테스트가 그것을 따라갈 것.

## Q1c — 화면은 실제로 사유를 그린다.  검사가 그것을 안 본다

`webapp/templates/seminar.html` 이 오류+힌트를 렌더한다 (즉 Q1a(c) 의 걱정은 화면 쪽에서는
기우다).  다만 테스트가 **HTML 을 문자열로만 훑어** JS 를 안 돌리므로, `renderDeck()` 을
들어내도 초록이다.  요구 = DOM 회귀.

## Q2 — AST 는 낫지만 "실제 backend 를 기록한다" 를 증명하지 못한다

GPU 대입 **바로 뒤에** `LAST_BACKEND['used'] = None` 을 끼워도 검사 59 는 초록이다
(`scripts/step3_sigma.py`).  요구 = 가짜 cupy/cupyx 로 2×2 성공 경로를 태울 것.
⚠ 비용 논거는 약하다 — CI 가 이미 NumPy/SciPy 를 깐다.

## Q3a — 방향은 CONFIRMED.  다만 종결문이 자기모순이다

금지 규정을 절차로 바꾼 처분 자체는 옳다.  그러나 `lhs_ext_r14_closure_20260830.md` 가
65·81·120 행과 152·166 행에서 서로 다른 말을 한다.  요구 = 65~91 을 *"초판 당시 상태 —
superseded"* 로 봉인하고 120 을 닫을 것.

## Q3b — 결정을 구조화하라 (제안)

`decision_id` · `state` · `supersedes` · `approval_evidence` · `design_sha256` ·
`submission_receipt` 를 두면 검사기가 ⓐ 살아 있는 상태가 하나뿐인지 ⓑ 승인 증거가 있는지
ⓒ `superseded_by` 가 걸렸는지를 강제할 수 있고, 인계 문서는 산문을 복사하는 대신 ID 를
참조하면 된다.

## P1-02 — 접두 비교가 틀린 SHA 를 통과시킨다

`scripts/check_doc_refs.py:125` 가 앞 7/8 자만 본다 ⇒ `7dbf38f0` 과 `7dbf38f0abcd` 가
둘 다 통과한다.  요구 = `git rev-parse --verify "$token^{commit}"` 로 **토큰 전체**를 확인.

## P1-03 — 자연어 면제가 진짜 틀린 SHA 를 통과시킨다

`codex_absorb_verdict_20260825.md` 의 같은 표(284·290 행)에 있는 *"증인이 없다"* 하나로
**리베이스 이전이라 히스토리에 없는** `c0ac0ad8` 이 면제된다.  `findings.json:1151` 은 그
변경이 `8bcfbeff` 로 들어갔다고 **이미 적고 있다**.
요구 = (문서, 정확한 SHA, ref, 이유) 의 명시적 예외.
덧붙여 ⓐ 12자 상한은 13~15자 형태를 **구조적으로** 못 본다 ⓑ 길이로 내용 해시와 커밋을
가르면 안 된다 ⓒ `rev-list --all` 은 얕은 클론을 못 잡는다
(`git rev-parse --is-shallow-repository` 가 필요하다).

## Q5 — allowlist 는 22건이다 (23 은 한 경로를 두 번 센 것) · 이유 6건 이상이 거짓·오분류

- `xy_heatmap_summary.csv` — `PHASE_C_SUMMARY.md:67` 과 **충돌**한다
- `oh2026_sigma_ionic.csv` — 같은 값의 digitize CSV 가 **이미 있고**, 그 CSV 가 2.16/2.37
  **전치**를 안고 있다.  이 등재가 그것을 가린다
- `db/properties/…phaseA.csv` · `webapp/data.py` — `claude/friendly-meitner-lldvar` 에
  **실재**한다 ⇒ 확인 가능한 브랜치 간 참조지 "다른 저장소" 가 아니다
- `sdcp8_{v04,v03,v025}.json` — 실제로 **세 파일**이다.  고칠 것은 검사기가 아니라 **문서**다
  (⚠ Codex 원문은 세 파일을 슬래시로 이어 **가짜 경로꼴**로 적었다.  그대로 옮기면 이
  문서가 없는 경로를 가리키게 되므로 — 실제로 `check_doc_refs` 가 두 번 잡았다, 인용할 때
  한 번 그리고 그 사실을 설명할 때 또 한 번 — 뜻을 바꾸지 않는 중괄호 표기로 적는다)
- `sigma_electronic_stage21_close_out.md` — **개명된 적이 없다**
- `mpm_dem_match.csv` 와 LIGGGHTS 덤프 2건은 1차 증거다 ⇒ 단순 예외가 아니라
  `EXTERNAL_EVIDENCE(uri, sha256)` 가 필요하다

## Q6 — CONFIRMED, 그리고 내가 생각한 것보다 크다

`--selftest` 진입점 **106개 / 96 파일**.  `check_all` 과 CI **둘 다**에 있는 것 17 ·
한쪽 6 · **어느 쪽에도 없는 것 83** (`check_undefined_names.py` · `network_conductivity.py` ·
`step4_dyn.py` · `structure_predictor.py` · `predictor_engine.py` 포함).
원인 = 규칙 K 가 **손으로 적은 10개 목록**을 대조한다 (`check_method_discipline.py:788`).
요구 = `path, flag, class=fast|gpu|external|legacy, lane, owner, reason` 등재 —
분류되지 않았거나 사라진 항목에서 실패할 것.

**P2** — CI 는 NumPy/SciPy/Matplotlib 만 깐다 (`.github/workflows/discipline.yml:33`).
그런데 `webapp/app.py:58` 은 Flask 를, 그 아래는 requests 를 필요로 한다 ⇒ 웹앱 CI 배선은
**깨끗한 러너에서 import 부터 죽는다**.  즉 아직 실제로 도는 상태가 아니다.

---

## 확인해 준 것

`git fetch --unshallow` 뒤 `check_doc_refs --selftest` 17/17, 리포 전수(문서 272 · 커밋
7,786)도 초록임을 Codex 가 직접 확인했다.  ⇒ 위 판정은 **얕은 클론 인공물이 아니라 실제
false-green 반례**에 근거한다.

---

## 우리 대응

원장 `docs/reviews/findings.json` **R19-01 ~ R19-10** 이 정본 (커밋 `1c3f647e`).
각 항목은 Codex 가 제시한 반례를 **실행해** 빨간불이 되는 것을 확인한 뒤 닫았다.

⚠ 아직 안 한 것:
- **Q3b (결정 구조화)** — 제안이고, 스키마를 새로 세우는 일이라 이번에 손대지 않았다.
- **1차 증거 3건의 sha256** — 그 기계(사용자 WSL · ibb)에서 받아야 한다.  검사기가
  "없다" 고 **보고**하되 막지는 않는다.
