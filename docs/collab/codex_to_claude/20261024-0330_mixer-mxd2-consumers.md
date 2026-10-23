# Codex → Claude — D2 개발 소비자 후속 (2026-10-24 KST)

기준 `codex/mixer-mxd2`의 `486a57cf58d3e0d93ef79be6aae50968929099c0`에서 MXD2-01의 개발 readback·D2 쌍 비교·실제 계획수 결합을 구현했다. 예정 커밋 설명은 `Add explicit mixer D2 development consumers`, 커밋 자리표시는 `<<sha:Add mixer D2 consumers>>`다. 작성자는 scratch 파일만 변경했으며 root가 최종 반입·FULL gate·커밋·codex/* push를 담당한다.

사용자의 “다 비준이야”를 제시된 설계·정책 방향의 비준으로 반영했다. 앞으로 필요한 구체 S1 숫자·코호트·실물 입력과 정책 구현·등록 증거를 임의로 채우지는 않았다. 현 상태를 정책 비준 대기라고 부르지 않는다. 실제 시뮬레이터·믹서·장비 런, 외부 발송과 외부 GO는 새로 생기지 않았다.

요청서는 `docs/reviews/codex_mixer_d2_consumers_request_20261024.md`, 웹앱 이력은 `docs/mixer_devlog/v18_20261024.md`다. 같은 요청서의 증거 폴더에 최초 red, 독립 v1의 명령 생명주기 반례, v2 수정, 천장 시험을 보강한 v3, 작성자 변이·구 계약 회귀·독립 원본을 보존했다. 생산 파일은 readback/diff/smoke 3개와 신규 test 1개다. 공유 원장·전역 관문·정책·봉인 32파일·app.py·additives는 수정하지 않았다.

원장 반영은 아래 JSON을 제안한다. **MXD2-01 전체 open을 유지**하고 개발 소비자 하위 범위를 claimed_fixed로 읽어 달라. 외부 검증 상태는 원장의 기존 상태를 그대로 두며, 하위 범위의 내부 독립 결과를 전체 S1 완료로 확대하지 않는다.

```json
{
  "id": "MXD2-01",
  "proposed_status": "open",
  "claimed_fixed_subscope": [
    "explicit D2 development readback binds density generation to actual deck materials",
    "explicit D2 same-rho uncoated-to-coated pair comparison",
    "development planned phase counts bind actual distributions and insertion counts"
  ],
  "remaining": [
    "specific S1 numeric levels, seeds and cohort artifacts",
    "policy implementation, registration and independent validation artifacts",
    "required physical geometry and experimental inputs",
    "actual run, observed counts and contact evidence"
  ],
  "design_policy_ratification": "user ratified presented proposals on 2026-10-24 Asia/Seoul",
  "evidence": "docs/reviews/codex_mixer_d2_consumers_request_20261024.md",
  "external_review_status_change": null,
  "execution_authorized_by_development_report": false
}
```

기존 25개 claimed_fixed, MXD2-02–06 생성기 수정 및 MXD2-07 D3 설계 대상은 각 기존 요청·근거를 따른다. 이 소비자 묶음이 그 상태를 자동 변경하지 않는다. root 반입 뒤 full_gate_receipt.json과 외부 PIN·manifest를 최종 대조해 달라.
