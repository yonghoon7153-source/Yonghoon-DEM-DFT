---
title: "CS 프롬프트 — li2s 소셀 유리 대조 계: 담금질 시작 · ⚠ 비용 견적 오류 정정 (시드당 3 h → 실측 ≈ 33–39 h 벽시계) · 총상한 80 GPU-h 를 MD 전에 넘는다 · 셈법·새 상한 140·그 사이 처리 확인 요청 셋 (외부 1저자에게)"
tags: [review, li2s, lpscl_smallcell, glass, control-system, li3ps4, cost, gpu-hours, ledger, external-first-author, prompt, letter]
letter: CS
date: 2026-10-05
updated: 2026-10-05
track: li2s / lpscl_smallcell_glass
channel: li2s1a
kind: prompt
status: 발송됨 (사용자 · 2026-10-05 · 발송판 `kb/projects/li2s_glass_control_cost_letter_CS_send_2026_10_05.md` = 보내는 글 그대로) — 회신 CS 대기
confidence: medium
verificationStatus: verified
verifiedAt: 2026-10-05
verifiedBy: self
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> **회신 CR** (`li2s1a_CR_reply_li2s_glass_control_card_2026_10_05.md`) 뒤의 편지다. 대조 계 카드는 회신대로 개정해 사용자가 비준했고 (`D-2026-10-05-lpscl-smallcell-glass-control-li3ps4` active), B 담금질을 10-05 15:35 kgy 에서 시작했다.
> 트랙 = li2s (외부 1저자) → **사용자는 1저자가 아니다.** 요지는 **우리 쪽 비용 견적 오류**의 정정이다. 사용자 결정 (10-05 AskUserQuestion '계속 + 편지') 은 실행 승인이고, 상한·셈법은 이 편지의 회신이 정한다 → 결정 `D-2026-10-05-lpscl-smallcell-glass-control-cost` **proposed**.
> 근거: runlog `db/properties/lpscl_glass_control_li3ps4_runlog_2026_10_05.json` (`⚠_비용_견적_오류_2026_10_05`) · A 실측 장부 `db/properties/lpscl_smallcell_glass_md_gateA_erratum_2026_09_24.json` (`Q6_총상한_GPU_h_셈법.장부_h`) · `db/properties/lpscl_smallcell_glass_md_cc_followup_2026_09_26.json` (`A2_Q6_장부_점유환산`) · A 셈법 `db/properties/lpscl_smallcell_glass_md_amendment_cc_2026_09_26.json` (`8_Q6_셈법`).
> ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `li2s1a_CS_reply_…` 로 원문 보존 → 결정 갱신 (사용자 비준 뒤 active).

---

**[li2s 소셀 유리 MD] 대조 계 담금질 시작 · 비용 견적 정정 · 확인 요청 셋**

회신 CR 감사합니다. 카드를 회신대로 고쳐 결과 전에 확정했고, B 담금질을 시작했습니다. 이번 편지는 저희 쪽 **비용 견적 오류**를 바로잡는 것이 요지입니다.

**0. 회신 CR 이행 · 담금질 시작**
- 카드를 회신 CR 대로 고쳤습니다. 1 을 포함할 때 쓸 검출한계는 결과 전에 모의로 냈습니다: A 600 K 다섯 시드의 ln D 표본 SD 0.094 기준 R₅₀ 1.20 · R₈₀ 1.25, B 산포가 두 배면 1.30 · 1.50 (로그정규 모형 · R 구간과 같은 부트스트랩 함수).
- 발사 전에 담금질 러너의 중복 실행 가드가 실제 담금질 프로세스를 못 찾는 배선 오류를 찾아 고쳤습니다 (돌기 전 · 계산 인자 불변).
- B 담금질은 10-05 15:35 kgy (RTX 3090) 에서 시작했습니다. A 와 같은 인자 (1200 K 100 ps → 10¹² K/s 선형 → 300 K 50 ps · NPT 0 GPa · turbo) 로 시드 1→5 를 차례로 돌립니다.

**1. 비용 견적 오류 — 정정합니다**
- 카드 §6 과 편지 CR 의 '담금질 시드당 ≈ 3 h · 합 15 GPU-h · 총 ≈ 55 GPU-h (상한 80)' 는 **틀렸습니다.** A 카드(09-21)에 있던 잰 적 없는 어림 ('5 개 다시 담금질 +15 h') 을 옮겼고, 같은 캠페인의 **실측 장부**를 보지 않았습니다. A 담금질은 공유 GPU 에서 시드당 벽시계 28.7–47.0 h · 점유 환산(등분 가정) 14.3–16.5 GPU-h 였습니다.
- B seed1 실측: melt 100 ps 에 222.9 분 (26.9 ps/h · kgy 를 GPU 잡 셋이 나눠 씀 · 사용률 100 %). A seed2 (kgy 세 잡 공유 · 1050 ps 에 47.0 h ≈ 22 ps/h) 와 같은 자리입니다 — 런은 정상이고 견적만 틀렸습니다.
- 어림: seed1 ≈ 33–39 h · 다섯 시드 ≈ 7–8 일 (공유 상태가 지금과 같다면).
- 상한 영향: A 셈법 (개정 CC §8 · 점유 환산) 으로 담금질 ≈ 70–80 + 600 K MD ≤ 40 (카드 견적 · v2 벽시계 실측 기반이라 점유로는 더 작을 수 있습니다) ⇒ ≈ 90–120 GPU-h 입니다. 총상한 80 을 **MD 전에** 넘습니다. 벽시계로 세면 담금질 2–3 시드째에 넘습니다.
- 지금까지 쓴 몫은 벽시계 ≈ 3.8 h 로 상한 근처가 아닙니다. 카드 규칙 ('넘으면 멈추고 보고한다 · 상한을 올려 계속하지 않는다') 에 따라 넘기 전에 보고드립니다.

**2. 회신 전까지 하는 것**
- 담금질은 계속 돌립니다 (회신 전까지는 잠정입니다). 시드가 끝날 때마다 장부 (벽시계 · 그 사이 같이 돈 GPU 잡 · 점유 환산) 를 남깁니다.
- 점유 환산 누적이 지금 상한 80 에 닿으면 그 시드가 끝난 자리에서 멈춥니다 (다음 시드를 띄우지 않습니다). 지금 어림으로는 다섯째 시드 무렵입니다.
- 계산 조건 (인자 · 시드 · 게이트 · 판독 규칙) 은 바꾸지 않습니다.

**3. 확인 요청 셋**
- **Q-CS-1 (셈법)** A 와 같은 점유 환산으로 셉니까? kgy 는 프로세스별 GPU 정보가 막혀 있어 nvidia-smi 표본으로 점유분율을 잴 수 없습니다 (A 의 kgy 런과 같은 한계). 그래서 '같이 돈 GPU 잡 수 등분' 을 가정으로 명시하고 벽시계를 같이 적으려 합니다. 회신 CD 는 등분 가정을 '병기용 — 상한 비교에 쓰지 않는다' 로 정했는데, kgy 에서는 다른 측정 수단이 없습니다. 이 경우 등분 가정으로 상한을 비교해도 됩니까, 아니면 벽시계로 셉니까?
- **Q-CS-2 (상한)** 총상한을 **140 GPU-h** (점유 환산 · 등분 가정) 로 올리는 개정을 제안합니다. 근거: 담금질 5 × A 실측 최대 16.5 = 82.5 + MD ≤ 40 ⇒ ≈ 123 · 여유 약 15 %. 판정에 쓰이는 결과는 아직 하나도 없습니다 (seed1 melt 단계). 결과 전 비용 정정으로 받아 주실 수 있습니까? 벽시계로 세라고 하시면 그 기준의 숫자를 다시 내겠습니다.
- **Q-CS-3 (그 사이)** 회신 전까지 위 2 처럼 계속 돌리고 80 에 닿으면 시드 끝에서 멈추는 처리로 됩니까?

근거 (저장소 `claude/evac-2026-10-02`): 카드 `db/properties/lpscl_smallcell_glass_control_li3ps4_estimand_2026_10_05.json` (§6 · 개정_회신_CR) · runlog `db/properties/lpscl_glass_control_li3ps4_runlog_2026_10_05.json` · A 장부 `lpscl_smallcell_glass_md_gateA_erratum_2026_09_24.json` · `lpscl_smallcell_glass_md_cc_followup_2026_09_26.json` · A 셈법 `lpscl_smallcell_glass_md_amendment_cc_2026_09_26.json` §8.
