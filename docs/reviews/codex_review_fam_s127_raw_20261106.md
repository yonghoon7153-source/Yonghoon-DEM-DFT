# Codex 반박 리뷰 — FAM §12-7 원자료 확인 (2026-11-06)

- **받은 때**: 2026-11-06.  1저자가 원자료 tgz (`docs/data/fam_s127_gabia_20261106/README.md` · sha256 43f40d64… · 31,295 B) 를 첨부해 Codex 반박 리뷰 창에 보냈고, 답을 이 세션에 붙여 넣었다.  아래 원문은 그대로 옮겼다 (Codex 로컬 경로 링크는 글자만 남김).
- **앞선 판정**: `docs/reviews/codex_review_fam_s127_results_20261106.md` (제시값 전제의 조건부 판정) → 이 답으로 전제를 첨부 자료 범위에서 해제.
- **요지**: 네 팔 §12-4 분류 확인 (confirm_fb · corner_fb 적격 · corner_fa · corner_f0 EXECUTION_FAILED · 새 불일치 없음) · 두께 29.491 (I_b′ 참) · 12.715 (I_b 거짓) 확인 · JSON 3 자리 ↔ 로그 2 자리 = 같은 원값의 반올림 (불일치 아님) · 환경 · 봉인 · 발사 기록 = 등록 봉인 칸과 일치 (기록 대조 범위) · corner b 0.0 % = 로그 산술로 0 클립이 실제로 걸림 (절단 전 −0.7913 % ∼ −0.6947 %) · kgy 원자료는 첨부 밖 (kgy 대조로 넓히지 않음) · 새 실험 · 모형 변경 · 추가 등록 · 원고 문장 승인 = 범위 밖.

## 원문

원자료에서 네 팔의 분류와 두께 값을 확인했습니다. 이전 답의 “제시값이 맞다는 전제”는 첨부 자료 범위에서 해제할 수 있습니다. 새 분류 불일치는 없습니다.

압축파일은 31,295 B, SHA256은 제시한 43f40d64…b2b9032와 일치하며, 내부 합 파일에 기록된 8개 파일도 모두 일치합니다. 재실행·호스트 접속은 하지 않았습니다.

(1) 네 팔의 §12-4 분류 — 확인
팔	원자료 근거	확정 분류
confirm_fb	정확 수렴 표지 1회, frame 266, rc 0	적격
corner_fb	정확 수렴 표지 1회, frame 724, rc 0	적격
corner_fa	수렴 표지 없음, not_converged_frame_budget, rc 1, JSON 없음	EXECUTION_FAILED
corner_f0	수렴 표지 없음, 허용 플래그로 JSON 출력, rc 0	EXECUTION_FAILED


근거는 confirm 로그 63행부터 (line 63), corner b 로그 152행부터 (line 152), corner a 로그 609행부터 (line 609), 배치의 f0 종료 기록 203행 (line 203)입니다.

네 팔의 전체 argv도 등록 및 §12-7-2 개정과 일치합니다. corner만 --platen-mach 0.0099999, f0만 --allow-unconverged-servo가 있습니다. 실행 순서·각 1회도 배치 기록과 같습니다.

성공한 두 JSON에서 다음을 확인했습니다.
- porosity_at_target_pct 비null — corner의 0.0도 조건 충족
- stop_mode=freeze_probe
- am_load_applied_to=descend+servo_setpoint
- V/cP=0.01, quasistatic_ok=true
- confirm CFL 제한 없음, corner CFL 제한 있음
confirm JSON (line 3), corner b JSON (line 3)의 20·29–41·50행에 있습니다.

servo_status 필드 부재는 앞선 소스 판정 그대로입니다. 이번에는 정확한 원 로그와 동일 시도의 argv·종료·저장 경로까지 연결됐으므로 내부 수렴 상태의 충분조건을 확인했습니다. 배치 status는 같은 로그의 요약이며 독립 증거로 더하지 않았습니다.

따라서 \(I_a\), \(I_0\)는 미정의이고, corner 네 칸·순서는 미배정입니다. 실패 두 팔의 값은 적중 판정에 사용하지 않았습니다.

(2) 두께와 \(I_b′\), \(I_b\) — 확인. 로그 정밀도 설명만 명확히
팔	JSON 두께	로그 두께	등록 판정
confirm	29.491 µm	29.49 µm	창 안 → \(I_b′=\mathrm{true}\)
corner b	12.715 µm	12.71 µm	창 밖 → \(I_b=\mathrm{false}\)


근거: 각 JSON 4행, confirm 로그 65행, corner b 로그 154행입니다.

12.715와 12.71은 불일치가 아닙니다. 코드가 같은 원값을 JSON에는 3자리, 로그에는 2자리로 각각 반올림합니다. 예를 들어 원값 12.7149는 두 출력 모두를 만듭니다. JSON의 12.715를 다시 두 자리로 반올림해 비교하면 이중 반올림이 됩니다.

따라서 문구는 다음이 정확합니다.
JSON 두께와 로그 두께는 각 출력 정밀도에서 양립한다. Gabia의 29.491 µm는 등록에 보존된 kgy 값과 0.001 µm 저장 정밀도에서 일치한다.

이번 첨부에는 kgy 원자료가 없으므로, kgy까지 새로 원자료 대조했다고 확대하지 않습니다.

(3) 환경·봉인·발사 기록 — 확인, 기록 대조 범위

배치 1–4행 (line 1)이 등록 봉인 칸과 일치합니다.
항목	확인값
실행 HEAD	7f44d6534d864f7be2f3310fa55d213b65cc707d
코드 MD5	c31f0512021d416702e162709c6f4400
러너 MD5	6e4b12b8cd296ec7b00376de07cf46b4
Python / NumPy / SciPy / Taichi	3.10.21 / 2.2.6 / 1.15.3 / 1.7.3
Taichi 지문	LLVM 15.0.4, commit 5ec301be
GPU 총량 / 발사 전 여유	49,140 / 48,539 MiB
CSV	지정한 네 파일의 SHA256 대조 통과 기록
발사	2026-11-04 14:14:11 KST


등록 1155–1162행, 진행 기록 1294행과 맞습니다. 고정 소스의 코드·러너 MD5도 별도로 계산해 일치를 확인했습니다.

다만 gabia에서 사용한 CSV 실물과 장비 질의 원문은 첨부되지 않았습니다. 이번 확인은 실행 기록과 등록의 일치이며, 실제 호스트 파일 재해시나 GPU 모델 재탐지는 아닙니다.

(4) 이전 Q1–Q5 수정 문장 — 유지 가능. 0 클립은 더 강하게 확인됨

이번 원자료는 “클립 가능성이 있다”보다 한 단계 강한 결론을 줍니다.

corner b 로그 141행 (line 141)의 frame 670은 두께 12.83 µm, 공극률 **0.16%**입니다. 고정된 \(V_{\rm solid}/A\)와 인쇄 반올림 범위를 적용하면, 최종 두께에서 **절단 전 산술 공극률은 약 −0.7913%∼−0.6947%**입니다. 따라서 최종 0.0%는 작은 양수의 반올림이 아니라 max(0, …)가 실제로 활성화된 결과입니다.

고칠 문장은 다음처럼 확정할 수 있습니다.
Corner b의 출력 공극률 0.0%는 코드의 0 클립 결과임을 로그 산술로 확인했다. 이는 실제 기하에서 모든 공극이 소멸했다는 증거가 아니다.

나머지 해석도 그대로 유지됩니다.
- 지정된 corner b 조합의 두께 예측 실패는 확인됨.
- 모든 \(f_{\mathrm{AM}}\) 보정의 불가능·MPM 일반 기각·DEM 정답은 입증되지 않음.
- settled_over_target와 f_am_cut의 제시값도 JSON과 일치하지만 보고 전용 지위 유지.
- fa 로그의 “frames를 늘리라”는 자동 안내는 등록의 추가 실행 금지를 덮지 않음.
- 새 실험·모형 변경·추가 등록·원고 문장 승인은 이번 확인 범위 밖.
정적 대조 결과는 검산 기록 JSON에 남겼습니다.
{
  "scope": "static raw-file review only; no simulation or remote host access",
  "checks": [
    {
      "check": "sha256 batch_s127.log",
      "passed": true
    },
    {
      "check": "sha256 fam_s127_confirm_fb.log",
      "passed": true
    },
    {
      "check": "sha256 fam_s127_corner_f0.log",
      "passed": true
    },
    {
      "check": "sha256 fam_s127_corner_fa.log",
      "passed": true
    },
    {
      "check": "sha256 fam_s127_corner_fb.log",
      "passed": true
    },
    {
      "check": "sha256 fam_s127_confirm_fb.json",
      "passed": true
    },
    {
      "check": "sha256 fam_s127_corner_f0.json",
      "passed": true
    },
    {
      "check": "sha256 fam_s127_corner_fb.json",
      "passed": true
    },
    {
      "check": "sealed code md5",
      "passed": true
    },
    {
      "check": "runner md5",
      "passed": true
    },
    {
      "check": "one RUN per arm, registered order",
      "passed": true
    },
    {
      "check": "confirm_fb complete argv",
      "passed": true
    },
    {
      "check": "confirm_fb rc",
      "passed": true
    },
    {
      "check": "confirm_fb marker count",
      "passed": true
    },
    {
      "check": "confirm_fb stop_mode",
      "passed": true
    },
    {
      "check": "confirm_fb am_load_applied_to",
      "passed": true
    },
    {
      "check": "confirm_fb protocol",
      "passed": true
    },
    {
      "check": "confirm_fb readout",
      "passed": true
    },
    {
      "check": "confirm_fb quasistatic_ok",
      "passed": true
    },
    {
      "check": "confirm_fb dt_cfl_limited",
      "passed": true
    },
    {
      "check": "confirm_fb target exists",
      "passed": true
    },
    {
      "check": "confirm_fb rate",
      "passed": true
    },
    {
      "check": "corner_fb complete argv",
      "passed": true
    },
    {
      "check": "corner_fb rc",
      "passed": true
    },
    {
      "check": "corner_fb marker count",
      "passed": true
    },
    {
      "check": "corner_fb stop_mode",
      "passed": true
    },
    {
      "check": "corner_fb am_load_applied_to",
      "passed": true
    },
    {
      "check": "corner_fb protocol",
      "passed": true
    },
    {
      "check": "corner_fb readout",
      "passed": true
    },
    {
      "check": "corner_fb quasistatic_ok",
      "passed": true
    },
    {
      "check": "corner_fb dt_cfl_limited",
      "passed": true
    },
    {
      "check": "corner_fb target exists",
      "passed": true
    },
    {
      "check": "corner_fb rate",
      "passed": true
    },
    {
      "check": "corner_fa complete argv",
      "passed": true
    },
    {
      "check": "corner_fa rc",
      "passed": true
    },
    {
      "check": "corner_fa marker count",
      "passed": true
    },
    {
      "check": "fa JSON absent",
      "passed": true
    },
    {
      "check": "corner_f0 complete argv",
      "passed": true
    },
    {
      "check": "corner_f0 rc",
      "passed": true
    },
    {
      "check": "corner_f0 marker count",
      "passed": true
    },
    {
      "check": "successful corner zero clamp necessarily active under printed rounding bounds",
      "passed": true
    }
  ],
  "arms": [
    {
      "arm": "confirm_fb",
      "rc": 0,
      "exact_marker_lines": [
        64
      ],
      "classification": "QUALIFIED",
      "thickness_um": "29.491",
      "inside_registered_window": true
    },
    {
      "arm": "corner_fb",
      "rc": 0,
      "exact_marker_lines": [
        153
      ],
      "classification": "QUALIFIED",
      "thickness_um": "12.715",
      "inside_registered_window": false
    },
    {
      "arm": "corner_fa",
      "rc": 1,
      "exact_marker_lines": [],
      "classification": "EXECUTION_FAILED"
    },
    {
      "arm": "corner_f0",
      "rc": 0,
      "exact_marker_lines": [],
      "classification": "EXECUTION_FAILED"
    }
  ],
  "clamp_raw_porosity_percent_bounds_from_rounded_log": [
    "-0.791267843800385386763144400",
    "-0.694732806417364633714757600"
  ],
  "json_log_rounding_example": {
    "raw_example": 12.7149,
    "json_round3": 12.715,
    "log_format2": "12.71"
  },
  "limitations": [
    "CSV checks recorded by runner; actual executed CSV bytes absent",
    "kgy raw outputs absent; previous kgy value from fixed registration",
    "No original unrounded thickness reconstruction"
  ]
}
