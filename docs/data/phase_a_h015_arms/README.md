# ⚠ 이것은 **지금 도는 Phase A 캠페인의 산출이 아니다**

`claude/phase-a-96arm-kgy` 에서 흡수해 온 **다른 세대**의 vox 0.15 32팔이다
(2026-09-15 흡수, 커밋 `c86fed4ab`).

```
receipt_code_sha : 70b9e37a
seal             : fibre_stamp=segment · ptfe_stamp=centerline · bridge_um=0.24
설계             : cells = [w, vox, origin] = 4 비율 × 8 origin = 32팔
파일             : arm_w1_v0.15_o0 … arm_w4_v0.15_o7 (+ _adapter_summary.json · run_receipt.json)
```

⛔ **지금(2026-09-15~) 도는 캠페인과 나란히 쓰지 말 것.**  그 캠페인은
`h025 → h020 → h015` 를 **한 체인·한 코드**로 돌리고 있고, 이 데이터는 `70b9e37a` 세대다.
`--compare-dir --expect-differ` 의 *"등록 밖 인자 불변"* 계약이 성립하는지 **확인된 적이 없다**.

★ 저자 결정 2026-09-15: *"걍 새로 돌려"* — h015 를 현행 체인에서 **새로 돌린다**.
  ⇒ 세대 문제가 원리적으로 사라지고, 세 격자가 같은 코드로 정렬된다.

⇒ 이 폴더의 쓰임은 **역사·교차참고**뿐이다.  payload 원본은 이미 삭제됐고 스칼라와
매니페스트만 회수된 상태다 (그것이 원 커밋 메시지의 *"payload 원본 삭제 전 회수"*).

⚠ 새 h015 가 끝난 뒤 **비교하고 싶다면** 먼저 `input_digest` 와 위 `seal` 세 값을 새 팔의
것과 대조할 것.  다르면 그것은 *"같은 격자의 두 측정"* 이 아니라 **두 규약의 비교**다.
